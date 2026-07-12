from sqlalchemy import select
from sqlalchemy.orm import Session

from supportops_db.models import TicketRecommendation


def create_ticket_recommendation(
    session: Session,
    *,
    tenant_id: str,
    ticket_id: str,
    source: str,
    category: str,
    priority: str,
    requires_escalation: bool,
    confidence: float,
    extracted_fields: dict[str, object],
    reasons: list[str],
    model_name: str | None = None,
    prompt_version: str | None = None,
    summary: str | None = None,
    suggested_reply: str | None = None,
) -> TicketRecommendation:
    recommendation = TicketRecommendation(
        tenant_id=tenant_id,
        ticket_id=ticket_id,
        source=source,
        category=category,
        priority=priority,
        requires_escalation=requires_escalation,
        confidence=confidence,
        model_name=model_name,
        prompt_version=prompt_version,
        summary=summary,
        suggested_reply=suggested_reply,
        extracted_fields_json=extracted_fields,
        reasons_json=reasons,
    )
    session.add(recommendation)
    session.flush()
    return recommendation


def list_ticket_recommendations(
    session: Session,
    *,
    tenant_id: str,
    ticket_id: str,
    limit: int = 50,
) -> list[TicketRecommendation]:
    return list(
        session.scalars(
            select(TicketRecommendation)
            .where(
                TicketRecommendation.tenant_id == tenant_id,
                TicketRecommendation.ticket_id == ticket_id,
            )
            .order_by(TicketRecommendation.created_at.desc())
            .limit(limit)
        )
    )


def get_ticket_recommendation_by_id(
    session: Session,
    *,
    tenant_id: str,
    ticket_id: str,
    recommendation_id: str,
) -> TicketRecommendation | None:
    return session.scalar(
        select(TicketRecommendation).where(
            TicketRecommendation.tenant_id == tenant_id,
            TicketRecommendation.ticket_id == ticket_id,
            TicketRecommendation.id == recommendation_id,
        )
    )
