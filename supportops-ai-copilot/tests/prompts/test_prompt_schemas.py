# ============================================================================
# FILE: tests/prompts/test_prompt_schemas.py
#
# WHAT THIS TESTS: the strict output shape in packages/prompts/schemas.py — the
# definition of what a valid AI answer looks like.
#
# WHY IT MATTERS MORE THAN A TYPICAL VALIDATION TEST:
#   These schemas are the ONLY thing standing between a language model's output
#   and the database. A model can return anything: prose instead of JSON, an
#   invented category, a confidence of 95 where 0.95 was meant. Every one of
#   those, if accepted, becomes a wrong row that quietly corrupts the metrics.
#
#   So these four tests are really testing the boundary defence. The three
#   "must fail" tests are the important ones — it is easy to loosen a schema
#   while debugging and never notice the protection is gone.
#
# NOTE THE SHAPE OF THE FILE: one helper producing a known-good payload, then
# tests that break it in one specific way each. That is a good pattern for
# validation tests — each test changes exactly one thing, so a failure points
# straight at the rule that broke.
# ============================================================================

import pytest
from pydantic import ValidationError

from supportops_prompts.schemas import FullTicketAnalysis


# A complete, valid AI response — what a well-behaved model returns.
#
# Returns a FRESH dictionary each call, which is essential: every test below
# modifies it, and a shared object would let one test's damage leak into the
# next.
#
# Worth reading on its own as documentation. This is the exact structure the
# hosted provider asks the model to produce and then validates on arrival.
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
            "evidence_ids": ["ticket-body"],    # where the model claims it found these
        },
        "evidence_ids": ["ticket-body"],
        "draft_response": {
            "response_text": "Thanks for reaching out. I will review the billing details.",
            "tone": "empathetic",
            "needs_human_review": True,
            "forbidden_claims": [],
        },
        "abstain": False,
        "risk_flags": ["none"],       # "none" explicitly, rather than an empty list —
                                      # a positive statement that risks were considered
        "missing_information": [],
    }


# The happy path: a valid response parses, and the values survive intact.
#
# Note the last assertion reaches into the NESTED object
# (`result.extracted_fields.order_ids`). That confirms the nesting was parsed
# into a real typed object rather than left as a plain dictionary.
def test_valid_full_ticket_analysis_parses() -> None:
    result = FullTicketAnalysis.model_validate(valid_analysis_payload())

    assert result.category == "billing"
    assert result.priority == "high"
    assert result.extracted_fields.order_ids == ["ORD-123"]


# A missing required field must be rejected.
#
# Why it matters: without this, an incomplete response would be accepted with
# `category` absent, and every downstream report grouping by category would
# silently lose those rows. A gap in the data that nobody notices is worse than
# a loud failure.
def test_missing_required_fields_fail() -> None:
    payload = valid_analysis_payload()
    payload.pop("category")

    with pytest.raises(ValidationError):
        FullTicketAnalysis.model_validate(payload)


# THE MOST VALUABLE TEST HERE, and it checks two halves of one rule.
#
# First half: "refund" is rejected. It is a perfectly reasonable-sounding
# category that a model might invent — and if accepted, it would create a
# seventh category that no dashboard, no threshold, and no pilot rule knows
# about. The tickets in it would effectively vanish from every report.
#
# Second half: "other" IS accepted. Equally important, because it is the model's
# honest way of saying "none of these fit". Without a valid escape hatch, a model
# forced to choose would cram odd tickets into whichever category seemed nearest,
# which is worse than an explicit "other".
#
# Testing both halves in one function keeps the rule and its exception together,
# which is how they should be read.
def test_unknown_categories_fail_unless_other() -> None:
    payload = valid_analysis_payload()
    payload["category"] = "refund"

    with pytest.raises(ValidationError):
        FullTicketAnalysis.model_validate(payload)

    payload["category"] = "other"
    assert FullTicketAnalysis.model_validate(payload).category == "other"


# Confidence must stay within 0 to 1.
#
# The specific bug this guards against: a model returning 95 to mean "95%" when
# the field expects 0.95. Without the bounds, that value would be stored happily,
# and any code treating confidence as a fraction — a threshold of "only
# auto-handle above 0.8", say — would treat 95 as overwhelming certainty.
#
# 1.2 is chosen as the test value rather than something wildly wrong, because it
# is the kind of near-miss a rounding bug actually produces.
def test_confidence_outside_zero_to_one_fails() -> None:
    payload = valid_analysis_payload()
    payload["category_confidence"] = 1.2

    with pytest.raises(ValidationError):
        FullTicketAnalysis.model_validate(payload)
