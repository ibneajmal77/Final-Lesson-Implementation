from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from supportops_api.dependencies import Actor, get_current_actor, get_db_session
from supportops_api.schemas.ai import TicketRecommendationRead
from supportops_api.schemas.tickets import TicketCreate, TicketRead
from supportops_api.settings import Settings, get_settings
from supportops_db.models import Ticket, TicketRecommendation
from supportops_db.repositories.recommendations import (
    create_ticket_recommendation,
    list_ticket_recommendations,
)
from supportops_db.repositories.tenants import get_tenant
from supportops_db.repositories.tickets import (
    create_ticket,
    get_ticket_by_external_id,
    get_ticket_by_id,
    list_tickets,
)
from supportops_domain.services.baseline import BaselineTicketInput, classify_ticket
from supportops_model_gateway.errors import UnsupportedModelProviderError
from supportops_model_gateway.providers.base import TicketAnalysisInput
from supportops_model_gateway.routing import build_ticket_analysis_provider

router = APIRouter(prefix="/tickets", tags=["tickets"])

ActorDep = Annotated[Actor, Depends(get_current_actor)]
SessionDep = Annotated[Session, Depends(get_db_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]


@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket_endpoint(
    payload: TicketCreate,
    response: Response,
    actor: ActorDep,
    session: SessionDep,
) -> TicketRead:
    _require_tenant(session, actor.tenant_id)

    existing = get_ticket_by_external_id(
        session,
        tenant_id=actor.tenant_id,
        external_id=payload.external_id,
    )
    if existing:
        response.status_code = status.HTTP_200_OK
        return _ticket_to_read(existing)

    ticket = create_ticket(
        session,
        tenant_id=actor.tenant_id,
        external_id=payload.external_id,
        channel=payload.channel,
        subject=payload.subject,
        body=payload.body,
        customer_id=payload.customer_id,
        metadata=payload.metadata,
    )
    session.commit()
    session.refresh(ticket)
    return _ticket_to_read(ticket)


@router.get("", response_model=list[TicketRead])
def list_tickets_endpoint(
    actor: ActorDep,
    session: SessionDep,
) -> list[TicketRead]:
    _require_tenant(session, actor.tenant_id)
    return [_ticket_to_read(ticket) for ticket in list_tickets(session, tenant_id=actor.tenant_id)]


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket_endpoint(
    ticket_id: str,
    actor: ActorDep,
    session: SessionDep,
) -> TicketRead:
    _require_tenant(session, actor.tenant_id)
    ticket = get_ticket_by_id(session, tenant_id=actor.tenant_id, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")
    return _ticket_to_read(ticket)


@router.post(
    "/{ticket_id}/baseline-analysis",
    response_model=TicketRecommendationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_baseline_analysis_endpoint(
    ticket_id: str,
    actor: ActorDep,
    session: SessionDep,
) -> TicketRecommendationRead:
    _require_tenant(session, actor.tenant_id)
    ticket = get_ticket_by_id(session, tenant_id=actor.tenant_id, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    analysis = classify_ticket(BaselineTicketInput(subject=ticket.subject, body=ticket.body))
    recommendation = create_ticket_recommendation(
        session,
        tenant_id=actor.tenant_id,
        ticket_id=ticket.id,
        source=analysis.source,
        category=analysis.category,
        priority=analysis.priority,
        requires_escalation=analysis.requires_escalation,
        confidence=analysis.confidence,
        extracted_fields=analysis.extracted_fields,
        reasons=analysis.reasons,
    )
    session.commit()
    session.refresh(recommendation)
    return _recommendation_to_read(recommendation)


@router.post(
    "/{ticket_id}/ai-analysis",
    response_model=TicketRecommendationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_ai_analysis_endpoint(
    ticket_id: str,
    actor: ActorDep,
    session: SessionDep,
    settings: SettingsDep,
) -> TicketRecommendationRead:
    _require_tenant(session, actor.tenant_id)
    ticket = get_ticket_by_id(session, tenant_id=actor.tenant_id, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    try:
        provider = build_ticket_analysis_provider(settings.model_provider)
    except UnsupportedModelProviderError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="model provider is not configured",
        ) from exc

    analysis = provider.analyze_ticket(
        TicketAnalysisInput(
            subject=ticket.subject,
            body=ticket.body,
            customer_id=ticket.customer_id,
        )
    )
    recommendation = create_ticket_recommendation(
        session,
        tenant_id=actor.tenant_id,
        ticket_id=ticket.id,
        source=analysis.source,
        category=analysis.category,
        priority=analysis.priority,
        requires_escalation=analysis.requires_escalation,
        confidence=analysis.confidence,
        extracted_fields=analysis.extracted_fields,
        reasons=analysis.reasons,
        model_name=analysis.model_name,
        prompt_version=analysis.prompt_version,
        summary=analysis.summary,
        suggested_reply=analysis.suggested_reply,
    )
    session.commit()
    session.refresh(recommendation)
    return _recommendation_to_read(recommendation)


@router.get("/{ticket_id}/recommendations", response_model=list[TicketRecommendationRead])
def list_ticket_recommendations_endpoint(
    ticket_id: str,
    actor: ActorDep,
    session: SessionDep,
) -> list[TicketRecommendationRead]:
    _require_tenant(session, actor.tenant_id)
    ticket = get_ticket_by_id(session, tenant_id=actor.tenant_id, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    recommendations = list_ticket_recommendations(
        session,
        tenant_id=actor.tenant_id,
        ticket_id=ticket.id,
    )
    return [_recommendation_to_read(recommendation) for recommendation in recommendations]


def _require_tenant(session: Session, tenant_id: str) -> None:
    if not get_tenant(session, tenant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tenant not found")


def _ticket_to_read(ticket: Ticket) -> TicketRead:
    return TicketRead(
        id=ticket.id,
        tenant_id=ticket.tenant_id,
        external_id=ticket.external_id,
        channel=ticket.channel,
        subject=ticket.subject,
        body=ticket.body,
        status=ticket.status,
        priority=ticket.priority,
        customer_id=ticket.customer_id,
        metadata=ticket.metadata_json,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
    )


def _recommendation_to_read(recommendation: TicketRecommendation) -> TicketRecommendationRead:
    return TicketRecommendationRead(
        id=recommendation.id,
        tenant_id=recommendation.tenant_id,
        ticket_id=recommendation.ticket_id,
        source=recommendation.source,
        category=recommendation.category,
        priority=recommendation.priority,
        requires_escalation=recommendation.requires_escalation,
        confidence=recommendation.confidence,
        model_name=recommendation.model_name,
        prompt_version=recommendation.prompt_version,
        summary=recommendation.summary,
        suggested_reply=recommendation.suggested_reply,
        extracted_fields=recommendation.extracted_fields_json,
        reasons=recommendation.reasons_json,
        created_at=recommendation.created_at,
    )

