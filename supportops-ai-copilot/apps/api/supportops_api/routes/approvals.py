from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from supportops_api.dependencies import Actor, get_current_actor, get_db_session
from supportops_api.schemas.approvals import (
    TicketRecommendationReviewCreate,
    TicketRecommendationReviewRead,
)
from supportops_db.models import RecommendationReview, TicketRecommendation
from supportops_db.repositories.approvals import (
    create_recommendation_review,
    list_recommendation_reviews,
)
from supportops_db.repositories.recommendations import get_ticket_recommendation_by_id
from supportops_db.repositories.tenants import get_tenant
from supportops_db.repositories.tickets import get_ticket_by_id

router = APIRouter(prefix="/tickets", tags=["approvals"])

ActorDep = Annotated[Actor, Depends(get_current_actor)]
SessionDep = Annotated[Session, Depends(get_db_session)]


@router.post(
    "/{ticket_id}/recommendations/{recommendation_id}/reviews",
    response_model=TicketRecommendationReviewRead,
    status_code=status.HTTP_201_CREATED,
)
def create_recommendation_review_endpoint(
    ticket_id: str,
    recommendation_id: str,
    payload: TicketRecommendationReviewCreate,
    actor: ActorDep,
    session: SessionDep,
) -> TicketRecommendationReviewRead:
    _require_tenant(session, actor.tenant_id)
    recommendation = _get_recommendation_for_ticket_or_404(
        session,
        tenant_id=actor.tenant_id,
        ticket_id=ticket_id,
        recommendation_id=recommendation_id,
    )
    final_summary, final_reply = _review_final_content(payload, recommendation)
    review = create_recommendation_review(
        session,
        tenant_id=actor.tenant_id,
        ticket_id=ticket_id,
        recommendation_id=recommendation.id,
        reviewer_user_id=actor.user_id,
        decision=payload.decision,
        final_summary=final_summary,
        final_reply=final_reply,
        notes=payload.notes,
    )
    session.commit()
    session.refresh(review)
    return _review_to_read(review)


@router.get(
    "/{ticket_id}/recommendations/{recommendation_id}/reviews",
    response_model=list[TicketRecommendationReviewRead],
)
def list_recommendation_reviews_endpoint(
    ticket_id: str,
    recommendation_id: str,
    actor: ActorDep,
    session: SessionDep,
) -> list[TicketRecommendationReviewRead]:
    _require_tenant(session, actor.tenant_id)
    _get_recommendation_for_ticket_or_404(
        session,
        tenant_id=actor.tenant_id,
        ticket_id=ticket_id,
        recommendation_id=recommendation_id,
    )
    reviews = list_recommendation_reviews(
        session,
        tenant_id=actor.tenant_id,
        ticket_id=ticket_id,
        recommendation_id=recommendation_id,
    )
    return [_review_to_read(review) for review in reviews]


def _require_tenant(session: Session, tenant_id: str) -> None:
    if not get_tenant(session, tenant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tenant not found")


def _get_recommendation_for_ticket_or_404(
    session: Session,
    *,
    tenant_id: str,
    ticket_id: str,
    recommendation_id: str,
) -> TicketRecommendation:
    ticket = get_ticket_by_id(session, tenant_id=tenant_id, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    recommendation = get_ticket_recommendation_by_id(
        session,
        tenant_id=tenant_id,
        ticket_id=ticket.id,
        recommendation_id=recommendation_id,
    )
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="recommendation not found",
        )
    return recommendation


def _review_final_content(
    payload: TicketRecommendationReviewCreate,
    recommendation: TicketRecommendation,
) -> tuple[str | None, str | None]:
    if payload.decision == "rejected":
        return None, None
    if payload.decision == "approved":
        return recommendation.summary, recommendation.suggested_reply
    if not payload.edited_summary and not payload.edited_reply:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="edited decision requires edited_summary or edited_reply",
        )
    return (
        payload.edited_summary if payload.edited_summary is not None else recommendation.summary,
        (
            payload.edited_reply
            if payload.edited_reply is not None
            else recommendation.suggested_reply
        ),
    )


def _review_to_read(review: RecommendationReview) -> TicketRecommendationReviewRead:
    return TicketRecommendationReviewRead(
        id=review.id,
        tenant_id=review.tenant_id,
        ticket_id=review.ticket_id,
        recommendation_id=review.recommendation_id,
        reviewer_user_id=review.reviewer_user_id,
        decision=review.decision,
        final_summary=review.final_summary,
        final_reply=review.final_reply,
        notes=review.notes,
        created_at=review.created_at,
    )

