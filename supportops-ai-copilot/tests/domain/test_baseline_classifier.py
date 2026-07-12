from supportops_domain.baseline_classifier import BaselineTicketInput, classify_ticket


def test_baseline_classifier_detects_billing_order_context() -> None:
    result = classify_ticket(
        BaselineTicketInput(
            subject="Charged twice",
            body="I was charged twice for order ORD-123 and need a refund.",
        )
    )

    assert result.source == "baseline_v1"
    assert result.category == "billing"
    assert result.priority == "high"
    assert result.requires_escalation is False
    assert result.extracted_fields["order_ids"] == ["ORD-123"]
    assert result.confidence >= 0.8


def test_baseline_classifier_escalates_security_risk() -> None:
    result = classify_ticket(
        BaselineTicketInput(
            subject="Unauthorized login",
            body="My account was hacked and I see fraud on my payment method.",
        )
    )

    assert result.category == "security"
    assert result.priority == "urgent"
    assert result.requires_escalation is True
    assert "hacked" in result.extracted_fields["matched_escalation_terms"]


def test_baseline_classifier_uses_other_for_unknown_issue() -> None:
    result = classify_ticket(
        BaselineTicketInput(
            subject="Question",
            body="I have a general question about my plan.",
        )
    )

    assert result.category == "other"
    assert result.priority == "normal"
    assert result.requires_escalation is False
