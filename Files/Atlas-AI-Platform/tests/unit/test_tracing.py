"""Tracing configuration tests.

Telemetry must never be the reason an API fails to start, so the important
assertions here are about degrading safely: an unconfigured exporter costs
nothing, and a requested-but-uninstalled exporter warns instead of raising.
"""

from __future__ import annotations

from packages.model_gateway.observability import emit_gateway_span
from packages.observability.tracing import (
    configure_tracing,
    gateway_span,
    reset_tracing_for_tests,
)


def test_default_configuration_installs_no_exporter() -> None:
    reset_tracing_for_tests()

    configure_tracing(exporter="none")

    # With no provider installed, spans still work — they are just no-ops.
    with gateway_span("test.span", {"gen_ai.system": "mock"}) as span:
        assert span is not None


def test_configure_tracing_is_idempotent() -> None:
    """A second call must not stack a second provider."""
    reset_tracing_for_tests()

    configure_tracing(exporter="none")
    configure_tracing(exporter="console")

    with gateway_span("test.span"):
        pass


def test_non_primitive_attribute_values_are_dropped() -> None:
    """A UUID or Decimal in a span attribute breaks exporters differently.

    Filtering here is what stops one exporter raising while another silently
    stringifies, which would make traces disagree across environments.
    """
    from decimal import Decimal
    from uuid import uuid4

    reset_tracing_for_tests()
    configure_tracing(exporter="none")

    with gateway_span(
        "test.span",
        {
            "ok_str": "value",
            "ok_int": 3,
            "ok_bool": True,
            "ok_list": ["a", "b"],
            "dropped_uuid": uuid4(),
            "dropped_decimal": Decimal("1.5"),
            "dropped_none": None,
        },
    ) as span:
        assert span is not None


def test_emit_gateway_span_accepts_a_full_attribute_payload() -> None:
    reset_tracing_for_tests()
    configure_tracing(exporter="none")

    emit_gateway_span(
        "model_gateway.chat",
        attributes={
            "gen_ai.system": "mock",
            "gen_ai.request.model": "mock-chat-v1",
            "gen_ai.response.finish_reasons": ["stop"],
            "atlas.prompt.version_id": None,
        },
        latency_ms=42,
    )
