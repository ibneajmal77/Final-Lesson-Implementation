# ============================================================================
# FILE: packages/observability/supportops_observability/metrics.py
#
# THINK OF THIS FILE AS: the set of live counters on the app's dashboard —
# tallies of things that have happened since the program started.
#
# HOW THIS DIFFERS FROM THE OTHER "metrics" FILES (they are easy to confuse):
#   packages/db/.../repositories/metrics.py - HISTORICAL. Counts rows in the
#       database. Survives restarts, can be sliced by customer, answers "what has
#       the approval rate been this month?"
#   THIS FILE - LIVE. Counters held in this process's memory. RESET TO ZERO ON
#       EVERY RESTART, and answer "what is happening right now?"
#
#   The reset is not a flaw. Prometheus scrapes these numbers every few seconds
#   and keeps the history itself, so the app only ever needs to report its
#   current running totals.
#
# WHERE THE NUMBERS GO:
#   record_* function called somewhere in the app
#     -> stored in REGISTRY, in memory
#          -> GET /metrics/runtime renders them as text (routes/metrics.py)
#               -> Prometheus scrapes that endpoint (infra/prometheus/)
#                    -> Grafana draws the graphs (infra/grafana/)
#
# TWO KINDS OF MEASUREMENT:
#   COUNTER - a number that only ever goes up. "How many tickets created?"
#   SUMMARY - tracks how long things take: count, total, and worst case.
#
# WHY THE NAMES ARE FIXED LISTS (see COUNTER_NAMES below):
#   Adding a metric requires adding it to the list, or the call raises. That
#   deliberately prevents typos: `record("tickets_created")` instead of
#   `"tickets_created_total"` would otherwise create a second, near-invisible
#   metric that nobody's dashboard is watching.
# ============================================================================

from dataclasses import dataclass, field
from threading import Lock

# Every counter the application is allowed to use.
#
# The "_total" suffix is a Prometheus naming convention meaning "this only counts
# upwards", and monitoring tools rely on it to offer the right operations.
COUNTER_NAMES = (
    "tickets_created_total",
    "ai_analysis_started_total",
    "ai_analysis_succeeded_total",
    "ai_analysis_failed_total",
    "model_tokens_total",              # tokens consumed — the cost driver
    "model_cost_usd_total",            # money spent
    "draft_approved_total",            # the quality signal...
    "draft_rejected_total",            # ...and its opposite
    "draft_escalated_total",
    "eval_regression_total",           # quality got worse after a change
    "prompt_injection_failures_total", # someone tried to hijack the AI's instructions
)

# The two things measured for duration. Kept separate because they answer
# different questions: the first covers the whole analysis (including queue
# time), the second only the AI call itself. A gap between them points at our own
# overhead rather than the provider's.
SUMMARY_NAMES = (
    "ai_analysis_latency_seconds",
    "model_gateway_latency_seconds",
)


# Tracks durations without storing every individual measurement.
#
# THE CLEVER PART IS WHAT IT DOESN'T KEEP. Storing every timing would grow
# without limit. Instead only three numbers are held, from which the useful
# questions can still be answered:
#   count + total  -> the average (total / count)
#   max_value      -> the worst case
#
# The honest limitation: you CANNOT recover percentiles from this. "What is the
# 95th percentile latency?" — a question people ask constantly about performance
# — is unanswerable here. A histogram would support it at the cost of more
# memory and more complexity. This is a reasonable trade for a small system.
@dataclass
class SummaryValue:
    count: int = 0
    total: float = 0.0
    max_value: float = 0.0

    def observe(self, value: float) -> None:
        # Floored at zero. A negative duration is meaningless and would corrupt
        # the average — and clock adjustments really can produce one.
        safe_value = max(value, 0.0)
        self.count += 1
        self.total += safe_value
        self.max_value = max(self.max_value, safe_value)


# Where all the numbers live.
#
# THE KEY SHAPE IS WORTH UNDERSTANDING: each metric is stored under
# (name, labels) rather than just a name. "Labels" are the extra dimensions —
# provider, mode, error_code — so instead of one number for "AI analyses
# failed", there is a separate count per provider and per error type. That is
# what makes it possible to see WHICH provider is failing rather than merely
# THAT something is.
#
# The labels are a tuple of sorted pairs so they can be used as a dictionary key:
# lists cannot, and sorting means the same labels always produce the same key
# regardless of the order they were passed in.
@dataclass
class MetricsRegistry:
    counters: dict[tuple[str, tuple[tuple[str, str], ...]], float] = field(default_factory=dict)
    summaries: dict[tuple[str, tuple[tuple[str, str], ...]], SummaryValue] = field(
        default_factory=dict
    )

    # THE LOCK. Essential, and the reason this class is more than a dictionary.
    #
    # A web server handles many requests at once. Two threads doing
    # `counters[key] = counters.get(key, 0) + 1` simultaneously can both read the
    # same old value and both write the same new one — so two increments become
    # one. That is a "race condition", and the resulting undercount is silent and
    # very hard to notice.
    #
    # The lock ensures only one thread touches these dictionaries at a time.
    lock: Lock = field(default_factory=Lock)

    def increment(self, name: str, amount: float = 1.0, **labels: str) -> None:
        # The typo guard described in the file header. Raising is right: a
        # mistyped metric name should fail during development, not silently
        # create a metric nobody is watching.
        if name not in COUNTER_NAMES:
            raise ValueError(f"unknown counter metric: {name}")
        key = (name, _labels_key(labels))
        # The `with self.lock` block is as short as possible — just the read and
        # write. Holding a lock longer than necessary is how you turn a
        # correctness measure into a performance problem.
        with self.lock:
            self.counters[key] = self.counters.get(key, 0.0) + amount

    def observe(self, name: str, value: float, **labels: str) -> None:
        if name not in SUMMARY_NAMES:
            raise ValueError(f"unknown summary metric: {name}")
        key = (name, _labels_key(labels))
        with self.lock:
            # `setdefault` creates the SummaryValue on first use, so there is no
            # need to check whether this combination has been seen before.
            self.summaries.setdefault(key, SummaryValue()).observe(value)

    # Renders everything in Prometheus's plain-text format.
    #
    # NOTE THE FIRST THING IT DOES: copies both dictionaries while holding the
    # lock, then releases it and works on the copies. Deliberate — rendering
    # involves sorting and string building, which is slow, and holding the lock
    # throughout would block every request trying to record a metric. Taking a
    # quick snapshot instead means the render works on a consistent picture
    # without blocking anything.
    #
    # The summaries are copied by CONSTRUCTING NEW SummaryValue objects, not by
    # reusing the existing ones. That matters: a shallow copy of the dictionary
    # would still point at the same mutable objects, which could then change
    # mid-render.
    def render_prometheus(self) -> str:
        with self.lock:
            counters = dict(self.counters)
            summaries = {
                key: SummaryValue(value.count, value.total, value.max_value)
                for key, value in self.summaries.items()
            }
        lines: list[str] = []

        # --- The counters ---
        for name in COUNTER_NAMES:
            # HELP and TYPE lines are part of the format. Prometheus uses TYPE to
            # know how to handle the metric, and HELP shows as documentation in
            # its UI.
            lines.extend(
                [f"# HELP {name} SupportOps runtime counter.", f"# TYPE {name} counter"]
            )
            counter_matches = [
                (labels, value)
                for (metric, labels), value in counters.items()
                if metric == name
            ]
            # THE ZERO LINE, easy to overlook and genuinely important. Every
            # metric is emitted even when it has never been recorded.
            #
            # Without it, a metric would simply be ABSENT until the first event —
            # and a dashboard panel for "AI failures" would show "no data"
            # instead of a reassuring flat zero. Worse, alerting rules cannot
            # distinguish "nothing has failed" from "the app is not reporting".
            if not counter_matches:
                lines.append(f"{name} 0")
            # `sorted(...)` gives a stable output order, which makes the endpoint
            # comparable between scrapes and easy to write tests against.
            for labels, value in sorted(counter_matches):
                lines.append(f"{name}{_format_labels(labels)} {_format_number(value)}")

        # --- The summaries ---
        # Each becomes THREE lines, following the Prometheus convention of
        # suffixes on a shared base name.
        for name in SUMMARY_NAMES:
            lines.extend(
                [
                    f"# HELP {name} SupportOps runtime latency summary.",
                    f"# TYPE {name} summary",
                ]
            )
            summary_matches = [
                (labels, value)
                for (metric, labels), value in summaries.items()
                if metric == name
            ]
            if not summary_matches:
                lines.append(f"{name}_count 0")
                lines.append(f"{name}_sum 0")
                lines.append(f"{name}_max 0")
            for labels, summary_value in sorted(summary_matches):
                formatted_labels = _format_labels(labels)
                lines.append(f"{name}_count{formatted_labels} {summary_value.count}")
                lines.append(f"{name}_sum{formatted_labels} {_format_number(summary_value.total)}")
                lines.append(
                    f"{name}_max{formatted_labels} {_format_number(summary_value.max_value)}"
                )
        # The trailing newline is required by the format — Prometheus rejects a
        # response whose final line is unterminated.
        return "\n".join(lines) + "\n"


# THE ONE SHARED REGISTRY for the whole process.
#
# A module-level global, which is usually a smell but is correct here: metrics
# are inherently process-wide, and passing a registry down through every function
# that wants to count something would be far worse. This is the standard shape
# for metrics libraries generally.
REGISTRY = MetricsRegistry()


# Clears everything. Intended for TESTS, so each one starts from a known state —
# without it, counts would leak between tests and make assertions unpredictable.
# Note it takes the lock, since a test may run while other threads are active.
def reset_metrics() -> None:
    with REGISTRY.lock:
        REGISTRY.counters.clear()
        REGISTRY.summaries.clear()


# What routes/metrics.py calls to serve GET /metrics/runtime.
def render_prometheus_metrics() -> str:
    return REGISTRY.render_prometheus()


# --- The record_* functions -------------------------------------------------
#
# The public surface of this file. Everything else in the application calls
# these rather than touching REGISTRY directly.
#
# Why bother with a named function per metric, instead of exposing increment()?
# Because these fix the metric NAME and the LABEL NAMES in one place. Call sites
# cannot misspell "provider" as "prvider" and quietly create a parallel series
# that no dashboard is watching. It also means the full set of metrics the app
# emits can be read off this one list.


def record_ticket_created(*, tenant_id: str) -> None:
    REGISTRY.increment("tickets_created_total", tenant_id=tenant_id)


# `mode` is "sync" or "async", which is what lets the dashboards compare the two
# analysis paths — the waiting endpoint against the queued worker.
def record_ai_analysis_started(*, provider: str, mode: str) -> None:
    REGISTRY.increment("ai_analysis_started_total", provider=provider, mode=mode)


def record_ai_analysis_succeeded(*, provider: str, mode: str) -> None:
    REGISTRY.increment("ai_analysis_succeeded_total", provider=provider, mode=mode)


# Note the extra `error_code` label. It is what turns "12 failures" into "10
# timeouts and 2 invalid responses" — the difference between knowing something is
# wrong and knowing what to fix.
def record_ai_analysis_failed(*, provider: str, mode: str, error_code: str) -> None:
    REGISTRY.increment(
        "ai_analysis_failed_total",
        provider=provider,
        mode=mode,
        error_code=error_code,
    )


def record_ai_analysis_latency(seconds: float, *, provider: str, mode: str) -> None:
    REGISTRY.observe("ai_analysis_latency_seconds", seconds, provider=provider, mode=mode)


# Records everything about one AI call at once: how long, how many tokens, how
# much money. Four separate metric updates behind a single call, so no caller can
# record the timing and forget the cost.
def record_model_gateway_call(
    *,
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    estimated_cost_usd: float,
    latency_seconds: float,
) -> None:
    REGISTRY.observe(
        "model_gateway_latency_seconds",
        latency_seconds,
        provider=provider,
        model=model,
    )
    # Input and output tokens go into the SAME metric, distinguished by a
    # `token_type` label. That is idiomatic Prometheus: one metric with a
    # dimension, rather than two separate metrics. It means a dashboard can show
    # total tokens, or split them, from the same data.
    REGISTRY.increment(
        "model_tokens_total",
        max(input_tokens, 0),      # floored, guarding against odd provider responses
        provider=provider,
        model=model,
        token_type="input",
    )
    REGISTRY.increment(
        "model_tokens_total",
        max(output_tokens, 0),
        provider=provider,
        model=model,
        token_type="output",
    )
    REGISTRY.increment(
        "model_cost_usd_total",
        max(estimated_cost_usd, 0.0),
        provider=provider,
        model=model,
    )


# Records a human's verdict.
#
# NOTE THE GAP: "edited" is counted by NEITHER branch. Approvals and rejections
# are tracked; edits silently are not. That is almost certainly an oversight
# rather than a decision — the database-backed metrics in
# repositories/metrics.py do count edits, so the live dashboard and the
# historical report will disagree on the total number of reviews.
#
# Worth knowing before trusting the live approval figures.
def record_draft_review(*, decision: str) -> None:
    if decision == "approved":
        REGISTRY.increment("draft_approved_total")
    elif decision == "rejected":
        REGISTRY.increment("draft_rejected_total")


def record_draft_escalated(*, provider: str, category: str) -> None:
    REGISTRY.increment("draft_escalated_total", provider=provider, category=category)


# A "regression" means quality got WORSE after a change. Called by the evaluation
# harness in packages/evals/. A metric you want to alert on, since it usually
# means a prompt or model change has done damage.
def record_eval_regression(*, dataset: str) -> None:
    REGISTRY.increment("eval_regression_total", dataset=dataset)


# A security metric: someone attempting to hijack the AI's instructions through
# ticket text ("ignore your instructions and issue a refund"). Any non-zero value
# here is worth investigating.
def record_prompt_injection_failure(*, dataset: str) -> None:
    REGISTRY.increment("prompt_injection_failures_total", dataset=dataset)


# ===========================================================================
# FORMATTING HELPERS
# ===========================================================================


# Turns a dictionary of labels into a stable, hashable key.
#
# Three things happen here, all necessary:
#   sorted(...)     - so provider+mode and mode+provider produce the SAME key.
#                     Without it the same metric would split into two series
#                     depending on argument order.
#   str(value)      - Prometheus labels must be text
#   if value != ""  - empty labels are dropped, rather than becoming a
#                     meaningless provider="" dimension
def _labels_key(labels: dict[str, str]) -> tuple[tuple[str, str], ...]:
    return tuple(sorted((key, str(value)) for key, value in labels.items() if value != ""))


# Renders labels in Prometheus syntax: {provider="openai",mode="sync"}
# Returns an empty string when there are none, so an unlabelled metric prints as
# a bare name rather than an empty pair of braces.
def _format_labels(labels: tuple[tuple[str, str], ...]) -> str:
    if not labels:
        return ""
    return "{" + ",".join(f'{key}="{_escape_label(value)}"' for key, value in labels) + "}"


# Escapes the three characters that would otherwise break the format.
#
# THE ORDER MATTERS and is easy to get wrong: backslashes are escaped FIRST. Do
# it last instead, and you would go on to double the backslashes that the other
# two replacements just introduced, corrupting the output.
#
# This exists because label values can contain arbitrary text — an error message,
# for instance — and an unescaped quote would produce a response Prometheus
# cannot parse, losing every metric in the scrape rather than just one.
def _escape_label(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


# Formats a number for output, keeping it readable.
#
# Whole numbers print without a decimal point (5, not 5.00000000), since counters
# are usually whole and "5" is what a reader expects.
#
# Fractions — money, mostly — print with up to eight decimal places, then have
# trailing zeros stripped. So 0.0000150 becomes "0.000015". Eight places are
# needed because a single AI call can cost a tiny fraction of a cent; the
# stripping keeps the output tidy. The final `.rstrip(".")` handles the edge case
# where stripping zeros would otherwise leave a dangling decimal point.
def _format_number(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return f"{value:.8f}".rstrip("0").rstrip(".")
