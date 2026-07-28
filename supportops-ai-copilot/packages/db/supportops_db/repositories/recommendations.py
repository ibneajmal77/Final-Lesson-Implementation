# ============================================================================
# FILE: packages/db/supportops_db/repositories/recommendations.py
#
# THINK OF THIS FILE AS: the database queries for the AI's conclusions and
# draft replies.
#
# A "recommendation" is the output of one analysis: what the ticket is about,
# how urgent it is, whether a human specialist is needed, and — for AI results —
# a summary and a draft reply.
#
# THE ONE THING TO UNDERSTAND HERE: nothing is ever updated or deleted.
#   There is a create, and there are two ways to read. No update, no delete.
#   That is deliberate. A recommendation records what was suggested at a
#   particular moment, by a particular model, under a particular version of our
#   instructions. Editing it would destroy the evidence needed to answer "what
#   did the AI actually say, and was it any good?"
#
#   So a ticket accumulates recommendations rather than replacing them: a
#   baseline one alongside an AI one, or several AI attempts over time. A human
#   who disagrees creates a REVIEW (repositories/approvals.py), which sits
#   alongside the original without altering it.
#
# WHO CALLS THESE:
#   routes/tickets.py    - all three analysis paths create one; the listing
#                          endpoint reads them
#   routes/approvals.py  - fetches the one being reviewed
#   apps/worker/jobs.py  - creates one after a queued analysis
# ============================================================================

from sqlalchemy import select
from sqlalchemy.orm import Session

from supportops_db.models import TicketRecommendation


# Records one analysis result.
#
# NOTE THE SPLIT IN THE ARGUMENT LIST. Everything down to `reasons` is required;
# the four after it have `= None` defaults. That divide is exactly the
# difference between the two kinds of analysis:
#
#   - Required fields are ones ANY analysis can produce, including the free
#     keyword classifier: category, priority, escalation, confidence.
#   - The optional four can only come from an AI: which model, which prompt
#     version, the summary, and the draft reply. Keyword rules cannot write
#     prose, so the baseline path simply omits them.
#
# The defaults are what let routes/tickets.py call this from the baseline path
# with a short argument list and from the AI path with the full one.
def create_ticket_recommendation(
    session: Session,
    *,
    tenant_id: str,
    ticket_id: str,
    source: str,                            # "baseline_v1", or the AI provider's name.
                                            # The column everything in the metrics hinges on
    category: str,
    priority: str,
    requires_escalation: bool,
    confidence: float,
    extracted_fields: dict[str, object],
    reasons: list[str],
    model_name: str | None = None,          # from here down: AI-only
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
        extracted_fields_json=extracted_fields,   # the "_json" suffix is the column name;
        reasons_json=reasons,                     # callers use the plainer names
    )
    session.add(recommendation)
    session.flush()      # send the INSERT, but leave committing to the caller — which is
                         # what lets a route save this and its cost record as one unit
    return recommendation


# Lists every recommendation for one ticket, newest first.
#
# Newest first matters here more than in most listings: it means the most recent
# analysis appears at the top of the screen, which is almost always the one the
# agent wants. The older ones remain below as history.
#
# The limit of 50 is generous — a ticket with 50 analysis attempts indicates
# something has gone wrong — so in practice it never truncates anything real. It
# is a guard against a runaway loop, not a paging mechanism.
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


# Fetches one specific recommendation.
#
# THREE conditions in the WHERE clause, where the id alone would suffice to find
# the row. Both extra conditions are doing security work:
#
#   tenant_id  - stops one company reading another's data
#   ticket_id  - stops a real recommendation ID being paired with an unrelated
#                ticket ID in the URL and still returning a result
#
# The second is subtler and easy to leave out. routes/approvals.py builds paths
# like /tickets/A/recommendations/B/reviews, which CLAIM that B belongs to A. If
# that claim is false the URL is wrong and should return nothing — otherwise
# someone can reach an object by a route they were never entitled to use.
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
