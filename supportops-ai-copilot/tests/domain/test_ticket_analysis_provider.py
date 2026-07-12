import pytest

from supportops_domain.ticket_analysis_provider import (
    MOCK_MODEL_NAME,
    MOCK_SOURCE,
    PROMPT_VERSION,
    TicketAnalysisInput,
    UnsupportedModelProviderError,
    build_ticket_analysis_provider,
)


def test_mock_provider_returns_model_shaped_analysis() -> None:
    provider = build_ticket_analysis_provider("mock")

    result = provider.analyze_ticket(
        TicketAnalysisInput(
            subject="Charged twice",
            body="I was charged twice for order ORD-123 and need a refund.",
            customer_id="customer-123",
        )
    )

    assert result.source == MOCK_SOURCE
    assert result.model_name == MOCK_MODEL_NAME
    assert result.prompt_version == PROMPT_VERSION
    assert result.category == "billing"
    assert result.priority == "high"
    assert result.summary
    assert "billing" in result.suggested_reply.lower()
    assert result.extracted_fields["order_ids"] == ["ORD-123"]
    assert result.extracted_fields["customer_id"] == "customer-123"


def test_unknown_provider_is_rejected() -> None:
    with pytest.raises(UnsupportedModelProviderError):
        build_ticket_analysis_provider("not-real")

