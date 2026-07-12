from sqlalchemy import select
from sqlalchemy.orm import Session

from supportops_db.models import RecommendationReview


def create_recommendation_review(
    session: Session,
    *,
    tenant_id: str,
    ticket_id: str,
    recommendation_id: str,
    reviewer_user_id: str,
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
            .order_by(RecommendationReview.created_at.desc())
            .limit(limit)
        )
    )

