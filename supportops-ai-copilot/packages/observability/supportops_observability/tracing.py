# ============================================================================
# FILE: packages/observability/supportops_observability/tracing.py
#
# THINK OF THIS FILE AS: the stopwatch that records a request's journey as a
# timeline, step by step.
#
# WHAT "TRACING" IS, AND HOW IT DIFFERS FROM LOGGING:
#   Logging records EVENTS: "request started", "AI call failed". Tracing records
#   NESTED DURATIONS — which step contained which, and how long each took:
#
#     api.request                              1,240ms
#       +- api.ai_analysis                     1,180ms
#           +- model_gateway.call              1,050ms   <- here is the time
#           +- db.create_recommendation           15ms
#
#   Each of those bars is a "span". The value is immediate and hard to get any
#   other way: when someone says "the app is slow", this shows you exactly WHICH
#   part is slow, including across process boundaries — the API's span and the
#   worker's span join up into one picture.
#
# HOW IT IS USED ELSEWHERE:
#     with trace_span("model_gateway.call", ticket_id=ticket.id):
#         ...the timed work...
#   You will see this wrapping every meaningful step in routes/tickets.py and
#   apps/worker/jobs.py.
#
# THE DESIGN CHOICE THAT DEFINES THIS FILE — IT IS ENTIRELY OPTIONAL:
#   The whole thing is built so that if the tracing library is not installed, or
#   no trace collector is running, everything still works and nothing fails. See
#   the try/except immediately below. Observability tooling should never be able
#   to take down the application it is observing.
#
#   The trade-off, worth stating: a missing library produces NO warning. Traces
#   simply do not appear, and someone may spend a while wondering why.
# ============================================================================

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

# OpenTelemetry is the industry-standard tracing library — vendor-neutral, so the
# traces can be sent to any compatible backend (Jaeger, Grafana Tempo, and others)
# without changing this code.
#
# The `try` makes it OPTIONAL. If the import fails for any reason, `trace` becomes
# None and every function below quietly does nothing.
#
# Catching bare `Exception` rather than just ImportError is unusually broad, and
# deliberate: some tracing setups fail during import for reasons other than being
# absent — a misconfigured exporter, an incompatible version — and none of those
# should stop the application from starting.
#
# `# pragma: no cover` tells the test coverage tool to ignore this branch, since
# it only runs in an environment where the library is missing.
try:
    from opentelemetry import trace
except Exception:  # pragma: no cover - fallback for minimal environments.
    trace = None  # type: ignore[assignment]

# The name identifying this application in the trace viewer, so its spans are
# distinguishable from those of every other service reporting to the same backend.
TRACER_NAME = "supportops-ai-copilot"


# Records one step of the timeline.
#
# `@contextmanager` makes it usable with `with`. The code before `yield` runs on
# entry, the code after on exit — which is exactly the shape a timer needs, since
# the span is closed automatically however the block ends, including when it
# raises.
#
# `**attributes` accepts any number of named extras — ticket_id, model_provider,
# and so on — which are attached to the span and become searchable in the viewer.
# That is what lets you ask "show me the slowest AI calls for this customer".
@contextmanager
def trace_span(name: str, **attributes: object) -> Iterator[None]:
    tracer = trace.get_tracer(TRACER_NAME) if trace is not None else None

    # THE FALLBACK PATH. No tracing available, so `yield` immediately and let the
    # caller's block run untouched. From the caller's point of view the `with`
    # statement behaves identically — it simply records nothing.
    if tracer is None:
        yield
        return

    # The real path. `start_as_current_span` both starts the span and makes it
    # the "current" one, so any span started inside the block automatically
    # becomes its child. That automatic nesting is what builds the tree shape at
    # the top of this file, with no need to pass a parent around by hand.
    with tracer.start_as_current_span(name) as span:
        _set_attributes(span, attributes)
        yield


# Adds attributes to whichever span is currently open, without starting a new one.
#
# Useful when a detail only becomes known partway through a step — a token count,
# say, which you cannot know until after the call returns. Rather than opening a
# second span for it, the fact is attached to the one already running.
def add_trace_attributes(**attributes: object) -> None:
    if trace is None:
        return
    span = trace.get_current_span()
    _set_attributes(span, attributes)


# Attaches attributes to a span, safely.
#
# Two rules, and both matter:
#
#   1. `None` values are SKIPPED. The tracing library rejects None outright, and
#      an optional field being absent should not cause an error in code whose
#      entire purpose is passive observation.
#
#   2. Only simple types are passed through directly; everything else is
#      converted to text with `str(...)`. Span attributes must be simple values,
#      and handing over a dictionary or a database object would raise. Converting
#      instead means a slightly less useful attribute rather than a failure.
#
# Together these make the function accept whatever it is given. That is the right
# posture for instrumentation: it must never be the thing that breaks a request.
def _set_attributes(span: Any, attributes: dict[str, object]) -> None:
    for key, value in attributes.items():
        if value is None:
            continue
        # `str | bool | int | float` is the modern way to write "any of these
        # types" in an isinstance check.
        if isinstance(value, str | bool | int | float):
            span.set_attribute(key, value)
        else:
            span.set_attribute(key, str(value))
