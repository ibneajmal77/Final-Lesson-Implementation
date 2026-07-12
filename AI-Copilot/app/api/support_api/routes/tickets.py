from typing import Annotated

from fastapi import APIRouter, Depends
from pytest import Session

from app.api.support_api.dependencies import Actor, get_current_actor, get_db_session
from app.api.support_api.schemas.tickets import TicketRead
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from supportops_api.dependencies import Actor, get_current_actor, get_db_session
from supportops_api.schemas.tickets import TicketCreate, TicketRead
from supportops_db.models import Ticket
from supportops_db.repositories.tenants import get_tenant
from supportops_db.repositories.tickets import (
    create_ticket,
    get_ticket_by_external_id,
    get_ticket_by_id,
    list_tickets,
)

router = APIRouter(prefix="/tickets", tags=["tickets"])

ActorDep = Annotated[Actor, Depends(get_current_actor)]
SessionDep = Annotated[Session, Depends(get_db_session)]

@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket_endpoint(
    payload: TicketCreate,
    response: Response,
    actor: ActorDep,
    session: Session
) -> TicketRead:
    
    _require_tenant(session, actor.tenant_id)

    existing = get_ticket_by_external_id(
    session,
    tenant_id= actor.tenant_id,
    external_id=payload.e
    )

    if existing:
        response.status_code = status.HTTP_200_OK
        return _ticket_to_read()
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

@router.get("", response_model=list[Ticket])
def list_tickets_endpoint(
actor: ActorDep,
session: SessionDep
) -> list[TicketRead]:
    _require_tenant(session, actor.tenant_id)
    return [_ticket_to_read(session) for ticket in list_tickets(session, actor.tenant_id)]

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










