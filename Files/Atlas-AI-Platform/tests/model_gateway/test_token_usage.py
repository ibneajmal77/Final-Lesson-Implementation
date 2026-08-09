"""Token usage normalization tests.

Phase 01 planned this file and never wrote it, which left usage normalization
completely unasserted. That matters more than it sounds: `input_tokens` and
`output_tokens` are what `pricing.py` multiplies to produce every cost row, so a
silent normalization bug becomes a silent billing bug.

None of these tests need a database or a network call — provider adapters map
raw payloads to `TokenUsage` in pure code.
"""

from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

import pytest

from packages.model_gateway.pricing import estimate_cost_lines, total_estimated_cost
from packages.model_gateway.providers.mock import MockProvider
from packages.model_gateway.providers.openai_compatible import _as_int
from packages.model_gateway.types import (
    ChatMessage,
    ModelRequest,
    SelectedRoute,
    TokenUsage,
)


def _route(**overrides: object) -> SelectedRoute:
    """Build a SelectedRoute without touching the database."""
    defaults: dict[str, object] = {
        "route_id": uuid4(),
        "route_key": "chat_primary",
        "use_case": "chat",
        "provider_name": "mock_public",
        "provider_type": "mock",
        "model_name": "mock-chat-v1",
        "max_input_tokens": 4000,
        "max_output_tokens": 800,
        "timeout_seconds": 30,
        "temperature": Decimal("0.2"),
        "restricted_data_allowed": False,
        "fallback_route_id": None,
        "route_config": {},
        "capabilities": {"supports_chat": True, "supports_embeddings": True},
        "data_policy": {},
        "max_cost_usd": Decimal("0.05"),
        "embedding_dimension": 8,
    }
    defaults.update(overrides)
    return SelectedRoute(**defaults)  # type: ignore[arg-type]


def test_mock_chat_usage_counts_input_and_output_tokens() -> None:
    request = ModelRequest(
        tenant_id=uuid4(),
        use_case="chat",
        messages=(ChatMessage(role="user", content="one two three"),),
    )

    response = MockProvider().chat(request, _route())

    assert response.usage.input_tokens == 3
    # The mock echoes "mock:chat:<message>", which is one whitespace-delimited
    # token here, so output must never be reported as zero.
    assert response.usage.output_tokens is not None
    assert response.usage.output_tokens >= 1


def test_mock_embedding_usage_sums_tokens_across_all_inputs() -> None:
    request = ModelRequest(
        tenant_id=uuid4(),
        use_case="embedding",
        inputs=("alpha beta", "gamma"),
    )

    response = MockProvider().embed(request, _route(use_case="embedding"))

    assert response.usage.input_tokens == 3
    # Embeddings produce no generated text, so an output count would be wrong.
    assert response.usage.output_tokens is None


def test_unset_usage_fields_stay_none_rather_than_zero() -> None:
    """None and 0 must not collapse together.

    `None` means the provider did not report the field; `0` means it reported
    none used. Collapsing them would invent cost lines for fields that were
    never measured.
    """
    usage = TokenUsage(input_tokens=10)

    assert usage.output_tokens is None
    assert usage.reasoning_output_tokens is None
    assert usage.cache_creation_input_tokens is None
    assert usage.cache_read_input_tokens is None


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (12, 12),
        (None, None),
        ("12", None),
        (12.5, None),
        (True, True),
    ],
)
def test_openai_usage_parsing_rejects_non_integer_payloads(raw: object, expected: object) -> None:
    """Provider JSON is untrusted input, so a wrong type must not become a count.

    `True` is included deliberately: Python's `bool` is a subclass of `int`, so
    it passes an `isinstance(value, int)` check. This test pins that known
    quirk rather than pretending it does not exist.
    """
    assert _as_int(raw) == expected


def test_usage_without_output_tokens_produces_only_input_cost_lines() -> None:
    """Normalization feeds pricing directly, so the two are asserted together."""
    lines = estimate_cost_lines(TokenUsage(input_tokens=1000, output_tokens=None))

    assert [line.billing_unit for line in lines] == ["input_token"]
    assert total_estimated_cost(lines) == Decimal("0.000150")


def test_zero_and_negative_quantities_are_not_billed() -> None:
    lines = estimate_cost_lines(
        TokenUsage(input_tokens=0, output_tokens=-5, reasoning_output_tokens=None)
    )

    assert lines == ()
    assert total_estimated_cost(lines) == Decimal("0.000000")


def test_all_usage_fields_map_to_distinct_billing_units() -> None:
    usage = TokenUsage(
        input_tokens=10,
        output_tokens=20,
        reasoning_output_tokens=30,
        cache_creation_input_tokens=40,
        cache_read_input_tokens=50,
    )

    lines = estimate_cost_lines(usage)

    assert [line.billing_unit for line in lines] == [
        "input_token",
        "output_token",
        "reasoning_token",
        "cache_write_token",
        "cache_read_token",
    ]
    assert all(line.quantity > 0 for line in lines)
