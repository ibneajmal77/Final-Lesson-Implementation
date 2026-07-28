# ============================================================================
# FILE: apps/api/supportops_api/routes/approvals.py
#
# THINK OF THIS FILE AS: the human sign-off desk.
#
# This is where a person decides what to do with something the AI wrote. It is
# arguably the most important file in the product, because it is the safety
# mechanism: the AI never replies to a customer by itself. Everything it
# produces stops here and waits for a human verdict.
#
# That arrangement has a name — "human in the loop" — and the reason for it is
# simple. An AI will occasionally produce a reply that is confidently wrong,
# rude, or promises a refund nobody authorised. A person spending ten seconds
# reading it catches that before a customer ever sees it.
#
# THE THREE POSSIBLE VERDICTS:
#   approved - the draft is good, send it as-is
#   edited   - close, but the human fixed some wording
#   rejected - no good, throw it away and write from scratch
#
# WHY EACH VERDICT IS STORED PERMANENTLY:
#   1. Accountability — a record of which person approved which reply.
#   2. Measurement — the approve/edit/reject ratio is THE number telling you
#      whether the AI is any good. Lots of rejections means it isn't working.
#      That calculation happens in packages/db/.../repositories/metrics.py
#      and is written up in docs/feedback-to-eval-loop.md.
#   3. Improvement — the human's edits show exactly HOW the AI fell short, which
#      is the raw material for improving the instructions given to it.
#
# THE ENDPOINTS:
#   POST .../reviews  - record a verdict on a draft
#   GET  .../reviews  - list the verdicts already recorded for a draft
#
# The paths are deliberately deeply nested:
#   /tickets/{ticket_id}/recommendations/{recommendation_id}/reviews
# which reads as "the reviews of this suggestion, on this ticket". Every level
# is verified in turn, so you cannot reach a suggestion via the wrong ticket.
# ============================================================================

from typing import Annotated, cast

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from supportops_api.dependencies import Actor, get_current_actor, get_db_session
from supportops_api.schemas.approvals import (
    ReviewDecision,
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
from supportops_observability.logging import get_logger, log_context
from supportops_observability.metrics import record_draft_review
from supportops_observability.tracing import trace_span

# Same /tickets prefix as routes/tickets.py — the two files split up the
# endpoints under one shared address space. The "approvals" tag is what puts
# them under their own heading in the automatic API documentation page.
router = APIRouter(prefix="/tickets", tags=["approvals"])
logger = get_logger(__name__)

# The same shorthand as in routes/tickets.py: "give me the verified caller" and
# "give me a database connection". Defined per-file rather than shared, so each
# route file can be read on its own.
ActorDep = Annotated[Actor, Depends(get_current_actor)]
SessionDep = Annotated[Session, Depends(get_db_session)]


# ---------------------------------------------------------------------------
# Record a human's verdict on an AI draft.
# ---------------------------------------------------------------------------
@router.post(
    "/{ticket_id}/recommendations/{recommendation_id}/reviews",
    response_model=TicketRecommendationReviewRead,
    status_code=status.HTTP_201_CREATED,
)
def create_recommendation_review_endpoint(
    ticket_id: str,
    recommendation_id: str,
    payload: TicketRecommendationReviewCreate,   # the verdict, plus any edits
    actor: ActorDep,
    session: SessionDep,
) -> TicketRecommendationReviewRead:
    # Two checks before anything else: the company exists, and this suggestion
    # genuinely belongs to this ticket and this company. The second helper does
    # the whole chain, and is explained further down.
    _require_tenant(session, actor.tenant_id)
    recommendation = _get_recommendation_for_ticket_or_404(
        session,
        tenant_id=actor.tenant_id,
        ticket_id=ticket_id,
        recommendation_id=recommendation_id,
    )
    with log_context(ticket_id=ticket_id), trace_span(
        "approval.action",
        tenant_id=actor.tenant_id,
        ticket_id=ticket_id,
        recommendation_id=recommendation.id,
        decision=payload.decision,
    ):
        # Work out what text should be saved as the final, agreed version.
        # The rules differ per verdict — see the helper at the bottom.
        final_summary, final_reply = _review_final_content(payload, recommendation)
        review = create_recommendation_review(
            session,
            tenant_id=actor.tenant_id,
            ticket_id=ticket_id,
            recommendation_id=recommendation.id,
            reviewer_user_id=actor.user_id,     # WHO decided. Taken from the verified caller,
                                                # never from the request body — otherwise anyone
                                                # could record a decision under someone else's name
            decision=payload.decision,
            final_summary=final_summary,
            final_reply=final_reply,
            notes=payload.notes,                # optional free text: "changed the tone"
        )
        session.commit()
        session.refresh(review)

    # Bump the counter for this verdict. This is what feeds the approval-rate
    # graph — the single clearest signal of whether the AI is earning its keep.
    record_draft_review(decision=payload.decision)
    logger.info(
        "recommendation_review_created",
        extra={"ticket_id": ticket_id, "decision": payload.decision},
    )
    return _review_to_read(review)


# ---------------------------------------------------------------------------
# List the verdicts already recorded for one suggestion.
#
# A list rather than a single item, because reviews are never overwritten. If a
# supervisor disagrees with an agent's call, that becomes a SECOND review — the
# first one stays exactly as it was. An audit trail you can edit isn't an audit
# trail, so nothing here ever updates or deletes.
# ---------------------------------------------------------------------------
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
    # The return value is thrown away here — this line is called purely for its
    # checking side effect. It raises a 404 if the ticket or suggestion doesn't
    # belong to this caller, which stops the listing below from ever running.
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


# ===========================================================================
# HELPERS
# ===========================================================================


# The company in the caller's headers must be one we recognise.
# Same helper, same reasoning, as the one in routes/tickets.py.
def _require_tenant(session: Session, tenant_id: str) -> None:
    if not get_tenant(session, tenant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tenant not found")


# Walks the whole chain — company, then ticket, then suggestion — and fails
# with a 404 at whichever link is broken.
#
# Why check the ticket at all, when the suggestion ID alone would be enough to
# find the row? Because the address CLAIMS a relationship: "suggestion X, which
# belongs to ticket Y". If that claim is false, the address is wrong and should
# be refused. Skipping the check would let someone pair a real suggestion ID
# with any ticket ID at all and still get an answer — a classic access-control
# hole, where the object you asked for is real but you had no legitimate route
# to reach it.
def _get_recommendation_for_ticket_or_404(
    session: Session,
    *,                        # everything after this must be passed by name, so
                              # ticket_id and recommendation_id can never be swapped
    tenant_id: str,
    ticket_id: str,
    recommendation_id: str,
) -> TicketRecommendation:
    ticket = get_ticket_by_id(session, tenant_id=tenant_id, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    # Note this lookup is filtered by BOTH tenant and ticket. A suggestion
    # belonging to a different ticket simply won't be found.
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


# Decides what text to store as the final, human-approved version.
#
# This little function holds the real business rules of the approval step. It
# returns two values: the agreed summary and the agreed reply.
#
#   rejected -> store nothing. The draft was no good; there is no agreed text.
#               The rejection itself is still recorded, which is the point.
#
#   approved -> copy the AI's text across unchanged. Copying rather than merely
#               pointing at it matters: if the suggestion is later cleaned up by
#               the retention job (apps/worker/retention.py), the reply that was
#               actually sent to the customer is still on record.
#
#   edited   -> keep whatever the human changed, and fall back to the AI's
#               version for whatever they left alone. So editing only the reply
#               keeps the AI's summary rather than blanking it.
def _review_final_content(
    payload: TicketRecommendationReviewCreate,
    recommendation: TicketRecommendation,
) -> tuple[str | None, str | None]:
    if payload.decision == "rejected":
        return None, None
    if payload.decision == "approved":
        return recommendation.summary, recommendation.suggested_reply

    # Only "edited" reaches here. An edit with nothing edited is contradictory,
    # so it is refused rather than silently stored as an approval.
    #
    # 422 Unprocessable Entity is the right code: the request was well-formed
    # JSON (or it would have failed earlier), but what it says doesn't make
    # sense as a request.
    if not payload.edited_summary and not payload.edited_reply:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="edited decision requires edited_summary or edited_reply",
        )
    # The test is "is not None", NOT a plain truth test — an important
    # distinction. An empty string is a real, deliberate edit meaning "delete
    # this text entirely". A plain `if payload.edited_summary` would treat that
    # empty string as "nothing supplied" and silently restore the AI's version,
    # overriding what the human actually asked for.
    return (
        payload.edited_summary if payload.edited_summary is not None else recommendation.summary,
        (
            payload.edited_reply
            if payload.edited_reply is not None
            else recommendation.suggested_reply
        ),
    )


# Converts a database row into the shape sent back as JSON — the same
# deliberate hand-conversion used in routes/tickets.py, keeping the public API
# shape separate from the internal table layout.
def _review_to_read(review: RecommendationReview) -> TicketRecommendationReviewRead:
    return TicketRecommendationReviewRead(
        id=review.id,
        tenant_id=review.tenant_id,
        ticket_id=review.ticket_id,
        recommendation_id=review.recommendation_id,
        reviewer_user_id=review.reviewer_user_id,
        # "cast" is a note to the type checker, not a conversion — it produces no
        # code at all and changes nothing at runtime. The database column is a
        # plain string, while ReviewDecision means specifically one of
        # "approved"/"edited"/"rejected". This line says "trust me, the value in
        # this column is one of those three", which is true because every write
        # path above goes through the validated schema.
        decision=cast(ReviewDecision, review.decision),
        final_summary=review.final_summary,
        final_reply=review.final_reply,
        notes=review.notes,
        created_at=review.created_at,
    )
