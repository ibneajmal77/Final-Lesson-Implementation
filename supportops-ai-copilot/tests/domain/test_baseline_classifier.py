# ============================================================================
# FILE: tests/domain/test_baseline_classifier.py
#
# WHAT THIS TESTS: the keyword classifier in
# packages/domain/supportops_domain/services/baseline.py — the free, non-AI way
# of categorising a ticket.
#
# THE SIMPLEST TESTS IN THE PROJECT, and deliberately so. No database, no fake
# browser, no monkeypatching. Just: give it text, check the answer.
#
# That simplicity is a direct consequence of how baseline.py was written. It is
# a "pure function" — same input, same output, no network, no clock, no state.
# Code shaped that way is trivially testable, which is one of the strongest
# practical arguments for keeping business logic separate from infrastructure.
#
# WHY IT DESERVES TESTING AT ALL, given it is "just keyword matching":
#   1. It is the YARDSTICK the AI is judged against. If it silently broke, every
#      comparison in the metrics would be meaningless.
#   2. It runs BEFORE every AI call, deciding a ticket's category for the pilot
#      gate. A wrong category here means the AI is wrongly allowed or refused.
#   3. Its escalation rule is a genuine safety mechanism — see the second test.
#
# THREE TESTS, covering the three meaningfully different paths: a normal match,
# the security override, and no match at all.
# ============================================================================

from supportops_domain.services.baseline import BaselineTicketInput, classify_ticket


# The ordinary case, and it checks several rules at once because they interact.
def test_baseline_classifier_detects_billing_order_context() -> None:
    result = classify_ticket(
        BaselineTicketInput(
            subject="Charged twice",
            body="I was charged twice for order ORD-123 and need a refund.",
        )
    )

    # Version is part of the source name, so results from an older version of
    # these rules stay distinguishable in the database.
    assert result.source == "baseline_v1"
    assert result.category == "billing"

    # "high", not "normal" — and this is the interesting assertion. It exercises
    # the one rule in baseline.py that uses more than keywords: a billing ticket
    # citing a specific order number or amount is treated as more urgent, because
    # a concrete dispute is likelier to become a chargeback than a general
    # question.
    assert result.priority == "high"

    # False, because being annoyed about billing is not a security matter. Worth
    # asserting explicitly — over-escalating would waste specialist time on every
    # refund request.
    assert result.requires_escalation is False

    # Confirms the order-number pattern actually matched. This value is what the
    # AI later receives as extracted context.
    assert result.extracted_fields["order_ids"] == ["ORD-123"]

    # `>=` rather than an exact value. A deliberately loose assertion: the test
    # cares that confidence is HIGH when several keywords matched, not that it is
    # precisely 0.85. Pinning the exact number would make the test fail on a
    # harmless tuning change, which is how test suites become a burden.
    assert result.confidence >= 0.8


# THE SAFETY TEST, and the most important one in the file.
#
# Note the ticket contains billing words ("payment", "fraud") AND security words.
# Under a naive first-match-wins rule with billing listed first, this would be
# classified as billing — routing a compromised-account report into a refunds
# queue where nobody is watching for it.
#
# This test locks in the ordering decision in CATEGORY_RULES that puts security
# first. Reorder that list and this test fails immediately, which is exactly what
# you want protecting a rule whose whole purpose is to catch the serious cases.
def test_baseline_classifier_escalates_security_risk() -> None:
    result = classify_ticket(
        BaselineTicketInput(
            subject="Unauthorized login",
            body="My account was hacked and I see fraud on my payment method.",
        )
    )

    assert result.category == "security"
    assert result.priority == "urgent"       # security always outranks everything else
    assert result.requires_escalation is True    # a human specialist must take this

    # Checks the AUDIT TRAIL, not just the verdict. baseline.py records which
    # words triggered the decision, which is what lets a human reviewer see why
    # a ticket was escalated rather than having to take it on trust.
    assert "hacked" in result.extracted_fields["matched_escalation_terms"]


# The fallback: nothing matched.
#
# Easy to skip and worth having, because "no match" is a genuinely different code
# path — _detect_category returns early on a match and only reaches its fallback
# when the entire loop finds nothing.
#
# It also confirms the classifier does not GUESS. Being honestly uncertain
# ("other", normal priority) is the correct behaviour, and much better than
# confidently filing a general question under a specific category.
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
    # Note the confidence is NOT asserted here. baseline.py returns a
    # deliberately low 0.35 for "other", and leaving it unchecked keeps this test
    # focused on the classification rather than the tuning.
