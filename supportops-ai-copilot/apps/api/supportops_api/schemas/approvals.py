# ============================================================================
# FILE: apps/api/supportops_api/schemas/approvals.py
#
# THINK OF THIS FILE AS: the sign-off form a human fills in when judging an AI
# draft, and the receipt they get back.
#
# This is the input and output shape for routes/approvals.py — the human review
# step that stands between the AI and a real customer.
#
# USED BY: routes/approvals.py
# ============================================================================

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

# The only three verdicts that exist. `Literal` means "this value must be
# EXACTLY one of these strings" — not just any string.
#
# That distinction does real work. A caller sending "approve" (missing the "d")
# or "APPROVED" is rejected with a clear error, rather than being silently
# stored as an unrecognised value that would then be invisible to the metrics
# queries counting approvals. Since the whole product is judged on the ratio
# between these three, a typo quietly corrupting the count would be a serious
# problem.
#
# Defined once here and reused in both classes below, plus in routes/approvals.py,
# so the list of valid verdicts exists in exactly one place.
ReviewDecision = Literal["approved", "rejected", "edited"]


# --- GOING IN: the verdict a reviewer submits ------------------------------
class TicketRecommendationReviewCreate(BaseModel):
    # Required. Everything else is optional.
    decision: ReviewDecision

    # The corrected text, when the reviewer chose "edited".
    #
    # Note both are optional HERE, even though an "edited" verdict is meaningless
    # without at least one of them. That rule is enforced in code instead, by
    # _review_final_content() in routes/approvals.py, because it is a rule about
    # the RELATIONSHIP between fields — "if decision is edited, then at least one
    # of these must be present" — which a per-field schema cannot express.
    #
    # The differing length limits reflect what each field is for: a summary is a
    # couple of sentences, while a full customer reply can run much longer.
    edited_summary: str | None = Field(default=None, min_length=1, max_length=2000)
    edited_reply: str | None = Field(default=None, min_length=1, max_length=5000)

    # Optional free text: "changed the tone", "the AI invented a refund policy".
    # Small field, large value — these notes are grouped and counted in
    # /metrics/pilot/feedback, and they are usually the fastest way to learn
    # what the AI is getting wrong.
    notes: str | None = Field(default=None, min_length=1, max_length=2000)


# --- COMING OUT: the recorded verdict --------------------------------------
class TicketRecommendationReviewRead(BaseModel):
    id: str
    tenant_id: str

    # Both IDs are kept, so a review can be traced to its exact draft AND its
    # ticket without extra lookups.
    ticket_id: str
    recommendation_id: str

    # WHO decided. Taken from the verified caller, never from the submitted
    # form — which is what makes this a trustworthy audit record rather than a
    # self-reported claim.
    reviewer_user_id: str

    decision: ReviewDecision

    # The agreed final text. Which values land here depends on the verdict, per
    # the rules in _review_final_content() in routes/approvals.py:
    #   approved -> a copy of the AI's text
    #   edited   -> the human's version, with the AI's text filling any gaps
    #   rejected -> both None; there is no agreed text
    #
    # Stored as a COPY rather than a pointer back to the draft, deliberately:
    # if the original draft is later removed by the retention cleanup, the reply
    # that was actually approved is still on record.
    final_summary: str | None
    final_reply: str | None

    notes: str | None
    created_at: datetime      # when the verdict was recorded. Combined with the ticket's
                              # own timestamps, this is what makes the
                              # "time to first response" figure possible.
