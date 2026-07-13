import pytest
from pydantic import ValidationError

from supportops_prompts.schemas import FullTicketAnalysis


def valid_analysis_payload() -> dict[str, object]:
    return {
        "category": "billing",
        "category_confidence": 0.91,
        "priority": "high",
        "requires_escalation": False,
        "extracted_fields": {
            "order_ids": ["ORD-123"],
            "amounts": ["USD 42.00"],
            "product_names": [],
            "account_identifiers": [],
            "evidence_ids": ["ticket-body"],
        },
        "evidence_ids": ["ticket-body"],
        "draft_response": {
            "response_text": "Thanks for reaching out. I will review the billing details.",
            "tone": "empathetic",
            "needs_human_review": True,
            "forbidden_claims": [],
        },
        "abstain": False,
        "risk_flags": ["none"],
        "missing_information": [],
    }


def test_valid_full_ticket_analysis_parses() -> None:
    result = FullTicketAnalysis.model_validate(valid_analysis_payload())

    assert result.category == "billing"
    assert result.priority == "high"
    assert result.extracted_fields.order_ids == ["ORD-123"]


def test_missing_required_fields_fail() -> None:
    payload = valid_analysis_payload()
    payload.pop("category")

    with pytest.raises(ValidationError):
        FullTicketAnalysis.model_validate(payload)


def test_unknown_categories_fail_unless_other() -> None:
    payload = valid_analysis_payload()
    payload["category"] = "refund"

    with pytest.raises(ValidationError):
        FullTicketAnalysis.model_validate(payload)

    payload["category"] = "other"
    assert FullTicketAnalysis.model_validate(payload).category == "other"


def test_confidence_outside_zero_to_one_fails() -> None:
    payload = valid_analysis_payload()
    payload["category_confidence"] = 1.2

    with pytest.raises(ValidationError):
        FullTicketAnalysis.model_validate(payload)

