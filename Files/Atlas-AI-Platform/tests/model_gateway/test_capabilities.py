"""Capability gating tests.

The point of gating is to refuse an impossible request locally instead of paying
a provider to reject it. These tests assert the refusal happens, that it names
every missing capability at once, and that unknown keys in a provider's
capability JSON are tolerated rather than fatal.
"""

from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

import pytest

from packages.model_gateway.capabilities import (
    Capability,
    ensure_route_supports,
    matrix_from_capabilities,
    required_capabilities_for_operation,
)
from packages.model_gateway.errors import CapabilityNotSupportedError
from packages.model_gateway.types import SelectedRoute


def _route(capabilities: dict[str, object]) -> SelectedRoute:
    return SelectedRoute(
        route_id=uuid4(),
        route_key="chat_primary",
        use_case="chat",
        provider_name="mock_public",
        provider_type="mock",
        model_name="mock-chat-v1",
        max_input_tokens=4000,
        max_output_tokens=800,
        timeout_seconds=30,
        temperature=Decimal("0.2"),
        restricted_data_allowed=False,
        fallback_route_id=None,
        route_config={},
        capabilities=capabilities,
        data_policy={},
        max_cost_usd=Decimal("0.05"),
        embedding_dimension=8,
    )


def test_matrix_reads_the_keys_bootstrap_already_writes() -> None:
    """The enum values must match the seeded JSON, or nothing is ever supported."""
    matrix = matrix_from_capabilities(
        {"supports_chat": True, "supports_embeddings": True, "supports_streaming": False}
    )

    assert matrix.supports(Capability.CHAT)
    assert matrix.supports(Capability.EMBEDDINGS)
    assert not matrix.supports(Capability.STREAMING)


def test_absent_keys_are_treated_as_unsupported() -> None:
    """Defaulting to unsupported is the safe direction for a missing flag."""
    matrix = matrix_from_capabilities({})

    assert not matrix.supports(Capability.CHAT)
    assert not matrix.supports(Capability.STRUCTURED_OUTPUT)


def test_unknown_capability_keys_are_ignored_not_rejected() -> None:
    """A provider row written by a newer version must stay readable."""
    matrix = matrix_from_capabilities(
        {"supports_chat": True, "supports_time_travel": True, "nonsense": 42}
    )

    assert matrix.supports(Capability.CHAT)
    assert matrix.supported == frozenset({Capability.CHAT})


def test_missing_reports_every_gap_at_once() -> None:
    """Reporting one gap at a time makes the caller fix them one at a time."""
    matrix = matrix_from_capabilities({"supports_embeddings": True})

    missing = matrix.missing([Capability.CHAT, Capability.STRUCTURED_OUTPUT])

    assert set(missing) == {Capability.CHAT, Capability.STRUCTURED_OUTPUT}


def test_operation_requirements_are_distinct_per_operation() -> None:
    assert required_capabilities_for_operation("chat") == frozenset({Capability.CHAT})
    assert required_capabilities_for_operation("embed") == frozenset({Capability.EMBEDDINGS})
    assert required_capabilities_for_operation("structured") == frozenset(
        {Capability.CHAT, Capability.STRUCTURED_OUTPUT}
    )


def test_capable_route_passes_the_gate_silently() -> None:
    route = _route({"supports_chat": True, "supports_embeddings": True})

    ensure_route_supports(route, operation="chat")
    ensure_route_supports(route, operation="embed")


def test_embedding_on_a_chat_only_route_is_refused_before_the_provider_call() -> None:
    route = _route({"supports_chat": True, "supports_embeddings": False})

    with pytest.raises(CapabilityNotSupportedError) as exc_info:
        ensure_route_supports(route, operation="embed")

    error = exc_info.value
    # 400, not 502: nothing downstream failed, the request was simply asking a
    # model for something it does not do.
    assert error.status_code == 400
    assert error.code == "ai.capability_not_supported"
    assert error.details["missing_capabilities"] == ["supports_embeddings"]
    assert error.details["route_key"] == "chat_primary"
    assert error.details["operation"] == "embed"


def test_structured_output_refusal_names_both_missing_capabilities() -> None:
    route = _route({})

    with pytest.raises(CapabilityNotSupportedError) as exc_info:
        ensure_route_supports(route, operation="structured")

    missing = exc_info.value.details["missing_capabilities"]
    assert set(missing) == {"supports_chat", "supports_structured_output"}
