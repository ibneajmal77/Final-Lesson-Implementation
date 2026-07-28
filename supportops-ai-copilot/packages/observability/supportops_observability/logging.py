# ============================================================================
# FILE: packages/observability/supportops_observability/logging.py
#
# THINK OF THIS FILE AS: the app's diary — and its censor.
#
# It does two jobs at once, and the second is the more important one:
#   1. Writes logs as machine-readable JSON, with useful context attached
#   2. STRIPS PERSONAL DATA AND SECRETS out of every line before it is written
#
# WHY JSON RATHER THAN PLAIN SENTENCES:
#   A line like "handled request in 42ms" is fine to read and useless to search.
#   A JSON object with named fields can be filtered — "show every request for
#   tenant X that took over a second" becomes a query rather than an afternoon
#   with grep. Every serious log system expects this shape.
#
# WHY THE REDACTION MATTERS SO MUCH HERE:
#   This app handles support tickets, which are full of email addresses, phone
#   numbers, and occasionally card numbers people should not have typed. Logs
#   get copied into search systems, shipped to third-party providers, and kept
#   for months — so a personal detail written into a log has effectively escaped
#   your control.
#
#   The functions at the bottom scrub four categories out of EVERY log line, so
#   the protection does not depend on each developer remembering.
#
# THE THREE PUBLIC PIECES:
#   configure_json_logging() - called once at startup by both the API and worker
#   get_logger()             - what every other file uses to get a logger
#   log_context()            - attaches IDs to everything logged inside a block
#
# HOW log_context IS THE CLEVER BIT:
#   Normally, getting a request ID into a log line written deep inside database
#   code means passing it down through every function in between. This uses a
#   "context variable" instead — a value that is invisibly available to
#   everything running inside a block, and automatically kept separate between
#   concurrent requests. See main.py, which sets it once per request.
# ============================================================================

import contextvars
import json
import logging
import re
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from uuid import uuid4

# The fields that identify WHERE a log line came from. Only these may be set via
# log_context — the allow-list is enforced by _clean_context at the bottom.
#
# An allow-list rather than "anything goes" is deliberate: it keeps log shape
# consistent enough to search, and stops someone casually attaching a whole
# ticket body as context.
LOG_CONTEXT_FIELDS = (
    "request_id",     # follows one request across the API, worker, and database
    "tenant_id",
    "user_id",
    "ticket_id",
    "ai_run_id",
    "job_id",
    "route",
    "error_code",
)

# Fields that describe WHAT HAPPENED. Passed per log call via `extra={...}`
# rather than through the context.
LOG_EXTRA_FIELDS = (
    "method",
    "status_code",
    "duration_ms",
    "model_provider",
    "model_name",
    "decision",
    "candidate_count",
)

# --- THE REDACTION PATTERNS ------------------------------------------------
#
# These are "regular expressions" — compact patterns describing text shapes to
# search for. Compiled once here, at import, rather than on every log line,
# because they run against every message the app writes.

# Email addresses: something@something.something
_EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)

# Phone numbers, in various common shapes: 555-123-4567, (555) 123 4567, +1...
# The `(?<!\d)` and `(?!\d)` at the ends are "look-arounds" — they require that
# no digit sits immediately before or after, so a long ID number is not mistaken
# for a phone number and mangled.
_PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?){2}\d{4}(?!\d)")

# Payment cards: 13 to 19 digits, allowing spaces or dashes between them, which
# covers every major card format.
_PAYMENT_CARD_PATTERN = re.compile(r"(?<!\d)(?:\d[ -]*?){13,19}(?!\d)")

# API keys and tokens, matched two ways:
#   - known key prefixes (sk-, pk-, sess-, ...) followed by a long random string
#   - anything after "api_key:", "authorization=", or "bearer "
# This is the pattern that stops a misconfigured debug log from writing your
# OpenAI key into a file that later gets shared.
_SECRET_PATTERN = re.compile(
    r"\b(?:sk|rk|pk|sess|org|proj)-[A-Za-z0-9_-]{8,}\b|"
    r"(api[_-]?key|authorization|bearer)\s*[:=]\s*[^\s,;]+",
    re.IGNORECASE,
)

# THE CONTEXT VARIABLE. Think of it as a note pinned to the current task, which
# any code running as part of that task can read without being handed it.
#
# The important property is ISOLATION: each request, and each async task, gets
# its own value automatically. Two requests being handled at the same time never
# see each other's IDs — which an ordinary global variable would not guarantee.
_LOG_CONTEXT: contextvars.ContextVar[dict[str, object] | None] = contextvars.ContextVar(
    "supportops_log_context",
    default=None,
)


# Turns each log record into one line of JSON.
#
# EVERY log line in the application passes through this method, which is what
# makes it the right place to enforce redaction — there is no way around it.
class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            # Always UTC, for the same reasons set out in packages/db/base.py:
            # servers in different regions must be comparable, and local time is
            # ambiguous for one hour every autumn.
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,          # INFO / WARNING / ERROR
            "logger": record.name,              # which module wrote this
            "message": redact_for_logs(record.getMessage()),   # scrubbed
        }
        # Add the ambient context (request_id, tenant_id, ...), also scrubbed.
        payload.update(_redacted_fields(current_log_context()))

        # Add any per-call fields passed as `extra={...}`. `getattr(record, ...)`
        # is how those arrive — the logging library attaches them to the record
        # object. Absent fields are skipped rather than written as null, keeping
        # lines compact.
        for field in (*LOG_CONTEXT_FIELDS, *LOG_EXTRA_FIELDS):
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = _redact_value(value)

        # Exception details, when logger.exception() was used. Redacted too, and
        # for good reason: a stack trace often includes the values of local
        # variables, which in this app can mean a customer's ticket text.
        if record.exc_info:
            payload["exception"] = redact_for_logs(self.formatException(record.exc_info))

        # `default=str` stops the whole log line failing if a value cannot be
        # converted to JSON — it is turned into text instead. Losing detail beats
        # losing the log entry.
        # `sort_keys=True` gives every line the same field order, which makes
        # eyeballing them and comparing them far easier.
        return json.dumps(payload, default=str, sort_keys=True)


# Switches JSON logging on. Called once at startup by BOTH main.py files — the
# API and the worker are separate processes, so each must configure its own.
def configure_json_logging(level: str = "INFO") -> None:
    # The "root" logger sits at the top of the hierarchy; configuring it means
    # every logger in the application inherits the setting, including ones inside
    # third-party libraries.
    root_logger = logging.getLogger()
    root_logger.setLevel(_level_name(level))
    handler = _json_handler(root_logger)
    handler.setFormatter(JsonLogFormatter())


# What every other file calls. A thin wrapper over the standard library, but
# routing all logger creation through one function means the implementation
# could be swapped later without touching thirty files.
#
# Called as get_logger(__name__), so each module's logs are tagged with the
# module they came from.
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


# A fresh random ID for a request that arrived without one. See main.py.
def new_request_id() -> str:
    return str(uuid4())


# Reads the current context.
#
# `dict(...)` returns a COPY. Important: it means a caller cannot modify the
# real context by editing what they were given, which would otherwise leak
# changes into unrelated code running in the same task.
def current_log_context() -> dict[str, object]:
    return dict(_LOG_CONTEXT.get() or {})


# Adds fields to the context, MERGING with whatever is already there.
#
# Merging rather than replacing is what allows nesting: main.py sets request_id
# and tenant_id for the whole request, then routes/tickets.py adds ticket_id for
# part of it, and log lines inside that inner block carry all three.
#
# It returns a "token" — a bookmark of the previous state, needed to restore it
# afterwards. That is what log_context uses below.
def set_log_context(**fields: object) -> contextvars.Token[dict[str, object] | None]:
    context = current_log_context()
    context.update(_clean_context(fields))
    return _LOG_CONTEXT.set(context)


# The `with` block version, and the one nearly all the code actually uses:
#
#     with log_context(ticket_id=ticket.id):
#         ...everything logged in here carries ticket_id...
#
# `@contextmanager` turns a function with a `yield` into something usable with
# `with`. The code before `yield` runs on entry, the code after runs on exit —
# and `finally` guarantees the exit half runs even if the block raised.
#
# That guaranteed reset is essential. Without it, an exception would leave the
# ticket_id stuck in the context, and it would then be wrongly attached to
# unrelated log lines afterwards.
@contextmanager
def log_context(**fields: object) -> Iterator[None]:
    token = set_log_context(**fields)
    try:
        yield                        # the `with` block's body runs here
    finally:
        _LOG_CONTEXT.reset(token)    # always restore the previous state


# THE CENSOR. Runs all four patterns over a piece of text, in order.
#
# Note the ORDER IS SIGNIFICANT. Secrets are scrubbed LAST, after emails and
# phone numbers, so an earlier pattern cannot partially mangle a key and leave
# a recognisable fragment that the secret pattern then fails to match.
#
# Each match is replaced with a visible marker rather than being deleted, so a
# reader can still tell that a value was there — which is often the useful part.
#
# Worth being honest about the limits: regular expressions catch common shapes,
# not every possible one. An unusual international phone format, or a key with an
# unfamiliar prefix, will slip through. This reduces exposure substantially; it
# does not eliminate it. The stronger protection is not logging the data at all,
# which is why the code elsewhere logs IDs and hashes rather than ticket text.
def redact_for_logs(text: str) -> str:
    redacted = _EMAIL_PATTERN.sub("[REDACTED_EMAIL]", text)
    redacted = _PHONE_PATTERN.sub("[REDACTED_PHONE]", redacted)
    redacted = _PAYMENT_CARD_PATTERN.sub("[REDACTED_PAYMENT_CARD]", redacted)
    return _SECRET_PATTERN.sub("[REDACTED_SECRET]", redacted)


# Applies redaction across a whole dictionary of fields.
def _redacted_fields(fields: dict[str, object]) -> dict[str, object]:
    return {key: _redact_value(value) for key, value in fields.items()}


# Redacts a value of ANY shape, digging into nested structures.
#
# It calls ITSELF for the contents of dictionaries, lists, and tuples — a
# "recursive" function. That matters because a log field might hold a nested
# structure several levels deep, and a sensitive value could be at the bottom of
# it. Scrubbing only the top level would miss exactly the cases most likely to
# contain something you did not intend to log.
#
# Anything that is not one of these types (a number, a boolean, None) is returned
# untouched — none of those can carry a hidden email address.
def _redact_value(value: object) -> object:
    if isinstance(value, str):
        return redact_for_logs(value)
    if isinstance(value, dict):
        return {key: _redact_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_redact_value(item) for item in value)
    return value


# Finds or creates the thing that actually writes log lines out.
#
# Reuses an existing handler if one is present, rather than adding another. That
# check prevents DUPLICATE LOG LINES — a classic and confusing bug where calling
# the setup function twice makes every message appear twice over.
#
# Writes to stdout, not to a file. That is the modern convention for containers:
# the program prints to its output, and the surrounding platform (Docker,
# Kubernetes) is responsible for collecting and storing it. Managing log files
# inside the container would mean managing rotation and disk space too.
def _json_handler(root_logger: logging.Logger) -> logging.Handler:
    if root_logger.handlers:
        return root_logger.handlers[0]
    handler = logging.StreamHandler(sys.stdout)
    root_logger.addHandler(handler)
    return handler


# Validates the configured log level, falling back to INFO for anything
# unrecognised.
#
# Falling back rather than failing is the right call here: a typo in LOG_LEVEL
# should not prevent the application from starting. The consequence is that a
# misspelled level is silently ignored, which is worth knowing if your DEBUG
# logs never appear.
def _level_name(level: str) -> str:
    cleaned = level.upper().strip()
    return cleaned if cleaned in logging.getLevelNamesMapping() else "INFO"


# Filters what may go into the log context. TWO conditions, both meaningful:
#
#   `key in LOG_CONTEXT_FIELDS` - only approved field names. Keeps the log shape
#                                 predictable enough to search, and prevents
#                                 arbitrary data being attached to every line.
#   `and value`                 - drops empty values, so a missing tenant_id
#                                 simply does not appear rather than showing up
#                                 as an empty string on every line.
def _clean_context(fields: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in fields.items() if key in LOG_CONTEXT_FIELDS and value}
