from pytest import Session
from sqlalchemy import select

from packages.db.support_ops_db.models import Ticket


def create_ticket(
        session: Session,
        *,
        tenant_id: str,
        external_id: str,
        channel: str,
        subject: str,
        body: str,
        customer_id: str | None,
        metadata: dict[str, object],
) -> Ticket:
    ticket = Ticket(
        tenant_id=tenant_id,
        external_id=external_id,
        channel=channel,
        subject=subject,
        body=body,
        customer_id=customer_id,
        metadata_json=metadata,
    )

    session.add(ticket)
    session.flush()
    return ticket;

def get_ticket_by_id(session: Session, *, tenant_id: str, ticket_id: str) -> Ticket | None:
                     return session.scalar(
                         select(Ticket).where(
                             Ticket.tenant_id == tenant_id,
                             Ticket.id == ticket_id
                         )
                     )

def get_ticket_by_external_id(
    session: Session,
    *,
    tenant_id: str,
    external_id: str,
) -> Ticket | None:
    return session.scalar(
        select(Ticket).where(
            Ticket.tenant_id == tenant_id,
            Ticket.external_id == external_id,
        )
    )

def list_tickets(session:Session, *, tenant_id: str, limit:int = 100) -> list[Ticket]:
        return list(
                session.scalars(
                        select(Ticket)
                        .where(Ticket.tenant_id == tenant_id)
                        .order_by(Ticket.created_at.desc())
                        .limit(limit)
                )
        )