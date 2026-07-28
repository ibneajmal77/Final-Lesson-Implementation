# ============================================================================
# FILE: packages/db/supportops_db/repositories/tickets.py
#
# THINK OF THIS FILE AS: every database query about customer support requests,
# gathered in one place.
#
# Four functions: one to create, two to look up, one to list.
#
# THE PATTERN TO NOTICE, AND THE REASON IT MATTERS MOST HERE:
#   Every single lookup below takes `tenant_id` as a REQUIRED argument and puts
#   it in the WHERE clause. That is not politeness — it is the mechanism keeping
#   one company's tickets away from another's.
#
#   Tickets are the most sensitive data in the system: customer names, email
#   addresses, order numbers, complaints. Because every company's tickets sit in
#   one shared table, a single query that forgets this filter would hand one
#   customer's support inbox to another. Making the argument required means that
#   mistake cannot be made by accident — you would have to deliberately pass a
#   tenant_id you had no right to.
#
# WHO CALLS THESE: apps/api/.../routes/tickets.py and apps/worker/.../jobs.py
# ============================================================================

from sqlalchemy import select
from sqlalchemy.orm import Session

from supportops_db.models import Ticket


# Creates a ticket.
#
# Note which fields are absent: no id, no status, no priority, no timestamps.
# All of those come from the `default=` settings on the columns in models.py, so
# a new ticket automatically gets a fresh UUID, status "open", priority
# "normal", and the current time. Defining defaults in one place beats repeating
# them at every call site, where they would eventually drift apart.
def create_ticket(
    session: Session,
    *,                        # everything after this must be passed by name. With five
                              # strings in a row, that prevents a whole class of silent bugs
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
        metadata_json=metadata,     # the argument is "metadata", the column is
                                    # "metadata_json" — the rename happens right here
    )
    session.add(ticket)
    # Sends the INSERT but does not commit. After this line the ticket's
    # generated id and created_at are readable, which is what lets the caller
    # log them. The caller decides when to commit; see session.py for why.
    session.flush()
    return ticket


# Fetches one ticket by its internal ID.
#
# TWO conditions, not one. Filtering by id alone would be enough to find the row
# — ids are unique — but adding the tenant check is what makes a request for
# another company's ticket return nothing at all.
#
# Multiple arguments to .where() are combined with AND, so this reads as
# "belongs to this company AND has this id".
def get_ticket_by_id(session: Session, *, tenant_id: str, ticket_id: str) -> Ticket | None:
    return session.scalar(
        select(Ticket).where(
            Ticket.tenant_id == tenant_id,
            Ticket.id == ticket_id,
        )
    )


# Fetches one ticket by the ID it has in the customer's own helpdesk system.
#
# This is the duplicate check. When a ticket arrives, routes/tickets.py calls
# this first: a match means "we already have this one", so it returns the
# existing ticket rather than creating a second copy. The helpdesk systems
# feeding us tickets retry when a reply gets lost, so without this, every retry
# would create a duplicate.
#
# It can safely return a single result because of the uniqueness rule on
# (tenant_id, external_id) declared in models.py — the database guarantees there
# can never be two.
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


# Lists a company's tickets, newest first.
#
# Two details worth understanding:
#
# `.order_by(Ticket.created_at.desc())` — newest first, because that is what
# someone looking at a support queue wants. Without an explicit order, a database
# may return rows in ANY order, and that order can change between runs; relying
# on it happening to look right is a bug waiting to surface.
#
# `limit: int = 100` — a safety valve. A company with 50,000 tickets would
# otherwise load all of them into memory and try to serialise the lot into one
# JSON response, which is slow at best and exhausts the server's memory at worst.
#
# Worth being honest about the limitation: this is a cap, not real paging. There
# is no way to ask for the NEXT 100. Fine for a demonstration; a production
# system would need proper pagination.
#
# `session.scalars(...)` — plural, unlike the single-result lookups above.
# Wrapped in `list(...)` because scalars returns a lazy iterator that stays tied
# to the session; converting it now means the caller holds real data that stays
# valid after the session closes.
def list_tickets(session: Session, *, tenant_id: str, limit: int = 100) -> list[Ticket]:
    return list(
        session.scalars(
            select(Ticket)
            .where(Ticket.tenant_id == tenant_id)
            .order_by(Ticket.created_at.desc())
            .limit(limit)
        )
    )
