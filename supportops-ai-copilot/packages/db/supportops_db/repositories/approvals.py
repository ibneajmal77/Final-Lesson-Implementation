# ============================================================================
# FILE: packages/db/supportops_db/repositories/approvals.py
#
# THINK OF THIS FILE AS: the database queries for human verdicts on AI drafts.
#
# The smallest repository file here, and that shortness is itself the point.
# There are exactly two operations: write a verdict, and read the verdicts.
#
# NO UPDATE. NO DELETE.
#   This is an audit trail, and an audit trail you can edit is not an audit
#   trail. Once someone records that they approved a reply to a customer, that
#   fact is permanent. A supervisor who disagrees adds a SECOND review; the
#   first stays exactly as it was, so the disagreement itself becomes part of
#   the record rather than erasing history.
#
#   The functions that would let you rewrite the past simply do not exist, which
#   is a stronger guarantee than a rule saying nobody should call them.
#
# WHY THESE ROWS MATTER MORE THAN MOST:
#   1. Accountability - which person approved which reply to which customer.
#   2. Measurement - the approve/edit/reject ratio is the number that decides
#      whether the AI stays switched on. Counted in repositories/metrics.py.
#   3. Improvement - the humans' edits and notes show HOW the AI fell short,
#      which is the raw material for improving it. See repositories/pilot.py.
#
# WHO CALLS THESE: apps/api/.../routes/approvals.py, and nothing else.
# ============================================================================

from sqlalchemy import select
from sqlalchemy.orm import Session

from supportops_db.models import RecommendationReview


# Records one human verdict.
#
# The three text fields are all `| None` because what they hold depends on the
# verdict, per the rules in _review_final_content() in routes/approvals.py:
#   approved -> final text copied from the AI's draft
#   edited   -> the human's wording, with the AI's filling any gaps
#   rejected -> both None; there is no agreed text to record
#
# Note the decision itself arrives as a plain `str` here, even though only three
# values are valid. The restriction is enforced one layer up, by the Literal type
# in schemas/approvals.py, so anything invalid is rejected before it ever reaches
# this function.
def create_recommendation_review(
    session: Session,
    *,
    tenant_id: str,
    ticket_id: str,
    recommendation_id: str,
    reviewer_user_id: str,     # WHO decided. The route takes this from the verified
                               # caller, never from the submitted form — which is what
                               # makes this a trustworthy record rather than a claim
    decision: str,
    final_summary: str | None,
    final_reply: str | None,
    notes: str | None,
) -> RecommendationReview:
    review = RecommendationReview(
        tenant_id=tenant_id,
        ticket_id=ticket_id,
        recommendation_id=recommendation_id,
        reviewer_user_id=reviewer_user_id,
        decision=decision,
        final_summary=final_summary,
        final_reply=final_reply,
        notes=notes,
    )
    session.add(review)
    session.flush()
    return review


# Lists the verdicts recorded for one draft, newest first.
#
# FOUR conditions in the WHERE clause — the most of any query in the project.
# Each one checks a different link in the chain the URL claims:
#   "the reviews (4) of THIS recommendation (3), on THIS ticket (2),
#    belonging to THIS company (1)"
#
# Any link being false means the URL was wrong, and the correct answer is
# nothing at all.
#
# Usually this returns just one row. It returns a list because it CAN be more:
# an agent's verdict and a supervisor's later disagreement both live here, and
# seeing both is precisely the point.
def list_recommendation_reviews(
    session: Session,
    *,
    tenant_id: str,
    ticket_id: str,
    recommendation_id: str,
    limit: int = 50,
) -> list[RecommendationReview]:
    return list(
        session.scalars(
            select(RecommendationReview)
            .where(
                RecommendationReview.tenant_id == tenant_id,
                RecommendationReview.ticket_id == ticket_id,
                RecommendationReview.recommendation_id == recommendation_id,
            )
            .order_by(RecommendationReview.created_at.desc())   # most recent verdict first
            .limit(limit)
        )
    )
