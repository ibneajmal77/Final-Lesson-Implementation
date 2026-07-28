# ============================================================================
# FILE: tests/observability/test_observability.py
#
# THINK OF THIS FILE AS: checking both the flight recorder and the dashboard
# gauges before the service takes off.
#
# WHAT THIS TESTS: the two visibility tools in
# packages/observability/supportops_observability/:
#   logging.py -> emits searchable JSON while censoring customer data and keys
#   metrics.py -> counts events and renders numbers Prometheus can collect
#
# OBSERVABILITY means evidence about what a running system is doing. Logs tell a
# detailed story about individual events; metrics turn many events into totals
# and timings suitable for alerts and graphs. Neither changes a ticket or an AI
# result, but both are essential when the API and worker fail in different
# processes and an operator has to connect the story.
#
# RUNTIME FLOW:
#   API middleware or worker job enters log_context with safe IDs
#     -> JsonLogFormatter writes one redacted JSON line to standard output
#   routes and model gateway call record_* helpers
#     -> the in-process registry updates counters and summaries
#       -> routes/metrics.py exposes Prometheus text
#         -> infra/prometheus collects it and infra/grafana displays it
#
# These are deliberately fast unit tests: no API, database, Prometheus server,
# or Grafana instance starts. That leaves two honest limits. Pattern-based
# redaction cannot recognize every possible secret format, and these in-memory
# metrics reset whenever a process restarts. Database-backed historical metrics
# in packages/db/supportops_db/repositories/metrics.py serve a different need.
#
# WHO USES IT / WHAT LIVES HERE: both apps/api and apps/worker import this
# package; operators consume the resulting logs, alerts, and dashboards.
# ============================================================================
import json
import logging

from supportops_observability.logging import JsonLogFormatter, log_context, redact_for_logs
from supportops_observability.metrics import (
    record_model_gateway_call,
    record_ticket_created,
    render_prometheus_metrics,
    reset_metrics,
)


# A LogRecord is Python logging's envelope for one event. Constructing it by
# hand isolates the formatter: no logger configuration, output stream, or API
# request is needed. The context manager temporarily pins request, tenant, and
# ticket IDs to the current task, then removes them when the with-block ends.
#
# json.loads turns the rendered line back into a dictionary so assertions check
# fields rather than fragile character ordering. Safe correlation IDs must be
# present; raw ticket text and model credentials must not appear by default.
# The next tests exercise actual redaction, since absence alone would not prove
# a sensitive value is scrubbed when someone explicitly logs it.
def test_json_log_formatter_includes_safe_context_fields() -> None:
    formatter = JsonLogFormatter()
    record = logging.LogRecord(
        name="supportops.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="ticket_created",
        args=(),
        exc_info=None,
    )

    with log_context(request_id="req-1", tenant_id="tenant_a", ticket_id="ticket-1"):
        payload = json.loads(formatter.format(record))

    assert payload["message"] == "ticket_created"
    assert payload["request_id"] == "req-1"
    assert payload["tenant_id"] == "tenant_a"
    assert payload["ticket_id"] == "ticket-1"
    assert "ticket_body" not in payload
    assert "model_api_key" not in payload


# PII means personally identifiable information: data such as an email address
# or phone number that can point back to a person. This one string deliberately
# includes every protected shape recognized by logging.py: email, US-style
# phone, payment-card digits, and an API-key assignment.
#
# Each original value is asserted absent AND each visible replacement marker is
# asserted present. Both halves matter: deletion would hide the secret but also
# hide the fact that useful data was intentionally censored.
#
# This is representative rather than exhaustive. The implementation uses regular
# expressions, which are text-shape matchers; unusual international numbers or
# a provider's brand-new key prefix can still escape them.
def test_redact_for_logs_masks_pii_and_secrets() -> None:
    raw = (
        "Customer jane@example.com called 212-555-0199 with card "
        "4111 1111 1111 1111 and api_key=sk-stage14secret."
    )

    redacted = redact_for_logs(raw)

    assert "jane@example.com" not in redacted
    assert "212-555-0199" not in redacted
    assert "4111 1111 1111 1111" not in redacted
    assert "sk-stage14secret" not in redacted
    assert "[REDACTED_EMAIL]" in redacted
    assert "[REDACTED_PHONE]" in redacted
    assert "[REDACTED_PAYMENT_CARD]" in redacted
    assert "[REDACTED_SECRET]" in redacted


# Sensitive text can enter a log through three doors, all covered here:
#   message     -> the main sentence supplied to the logger
#   context     -> IDs carried automatically with the current request or job
#   extra field -> structured data attached to this one event
#
# Assigning model_name directly to the LogRecord imitates Python logging's
# extra-field mechanism. Serializing the whole payload again creates one string
# that can be searched for any leaked original, while exact field assertions
# prove each door received the intended replacement rather than being discarded.
def test_json_log_formatter_redacts_message_context_and_extra_fields() -> None:
    formatter = JsonLogFormatter()
    record = logging.LogRecord(
        name="supportops.test",
        level=logging.WARNING,
        pathname=__file__,
        lineno=1,
        msg="provider failed for alice@example.com with sk-stage14secret",
        args=(),
        exc_info=None,
    )
    record.model_name = "Bearer sk-nestedsecret"

    with log_context(user_id="bob@example.com"):
        payload = json.loads(formatter.format(record))

    rendered = json.dumps(payload)
    assert "alice@example.com" not in rendered
    assert "bob@example.com" not in rendered
    assert "sk-stage14secret" not in rendered
    assert "sk-nestedsecret" not in rendered
    assert payload["message"] == "provider failed for [REDACTED_EMAIL] with [REDACTED_SECRET]"
    assert payload["user_id"] == "[REDACTED_EMAIL]"
    assert payload["model_name"] == "Bearer [REDACTED_SECRET]"


# Metrics live in a module-level registry shared by every test in this Python
# process. Resetting first prevents an earlier test's counts from leaking in and
# making the result depend on execution order.
#
# A COUNTER only moves upward, such as tickets or tokens. A SUMMARY records a
# distribution of observations, such as model latency, and Prometheus exposes
# helper series including a sample count. Labels split one metric into useful
# dimensions; here tokens are identified by provider, model, and input/output.
#
# The exact token line also locks in stable alphabetical label rendering, while
# the latency-name check proves a summary was emitted. This does not test
# concurrent updates, HTTP scraping, persistence across restarts, or Grafana;
# it checks the plain-text contract consumed by routes/metrics.py.
def test_prometheus_metrics_renderer_exposes_counters_and_summaries() -> None:
    reset_metrics()

    record_ticket_created(tenant_id="tenant_a")
    record_model_gateway_call(
        provider="mock_llm_v1",
        model="mock-ticket-analyzer",
        input_tokens=3,
        output_tokens=5,
        estimated_cost_usd=0.01,
        latency_seconds=0.25,
    )

    output = render_prometheus_metrics()

    assert 'tickets_created_total{tenant_id="tenant_a"} 1' in output
    assert (
        'model_tokens_total{model="mock-ticket-analyzer",provider="mock_llm_v1",'
        'token_type="input"} 3'
    ) in output
    assert "model_gateway_latency_seconds_count" in output
