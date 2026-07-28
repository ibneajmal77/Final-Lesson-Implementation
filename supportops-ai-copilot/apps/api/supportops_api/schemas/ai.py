# ============================================================================
# FILE: apps/api/supportops_api/schemas/ai.py
#
# THINK OF THIS FILE AS: the shape of the AI's output as the outside world sees
# it. Two things live here:
#
#   TicketRecommendationRead - WHAT the AI decided about a ticket
#   AIAnalysisRunRead        - HOW THE JOB WENT that produced it
#
# WHY BOTH, AND WHY THE SPLIT MATTERS:
#   In the queued path (POST /tickets/{id}/analyze), a request comes back before
#   any AI work has happened. At that instant there is no recommendation to
#   show — only a job sheet saying "pending". So the two facts must be separate:
#     - the RUN always exists, from the moment the job is created
#     - the RECOMMENDATION only exists once the run succeeds
#   That is why AIAnalysisRunRead can carry a recommendation but does not have
#   to, and why a failed run has an error but no result.
#
# NOTE THERE ARE NO "Create" CLASSES HERE, unlike the other schema files. That
# is because nothing is ever posted in: both AI endpoints take their input from
# the ticket already in the database, so their request bodies are empty.
# Everything here is output-only.
#
# USED BY: routes/tickets.py — the AI analysis and listing endpoints.
# ============================================================================

from datetime import datetime
from typing import Any

from pydantic import BaseModel


# --- WHAT THE AI DECIDED ---------------------------------------------------
#
# One "recommendation" — the AI's read on a ticket, plus its draft reply.
# Produced by all three analysis paths in routes/tickets.py, though the
# baseline path leaves the AI-only fields empty.
class TicketRecommendationRead(BaseModel):
    id: str
    tenant_id: str
    ticket_id: str

    # WHERE this came from: "baseline" for the keyword rules, or the AI
    # provider's name. Crucial for reading the metrics — comparing approval
    # rates by source is how you tell whether the AI beats simple rules.
    source: str

    # The judgement itself.
    category: str                  # what it is about: billing / technical / account...
    priority: str                  # how urgent: low / medium / high
    requires_escalation: bool      # does a specialist human need to take this over?

    # How sure the AI is, from 0.0 to 1.0. Useful for triage — a low-confidence
    # draft is worth a closer human read. Treat with healthy suspicion though:
    # language models are known for being confidently wrong, so this is a hint,
    # not a guarantee.
    confidence: float

    # --- The four AI-only fields. All are None for baseline results ---------
    #
    # These two record exactly WHICH model and WHICH version of our instructions
    # produced this text. That pairing is what makes quality changes explainable:
    # when the approval rate drops, these tell you what changed underneath.
    model_name: str | None
    prompt_version: str | None

    summary: str | None           # a short recap of the customer's problem
    suggested_reply: str | None   # the draft reply. Never sent to anyone until a human
                                  # approves it in routes/approvals.py

    # Structured details pulled out of the ticket text — an order number, a date,
    # an error code. A dictionary rather than fixed fields because what is worth
    # extracting differs completely between a billing query and a crash report.
    extracted_fields: dict[str, Any]

    # WHY it decided this, in plain sentences. Possibly the most important field
    # for the humans doing reviews: a verdict with no reasoning is hard to trust
    # or to argue with, and this is what lets a reviewer judge in seconds rather
    # than re-reading the whole ticket.
    reasons: list[str]

    created_at: datetime

# --- HOW THE JOB WENT ------------------------------------------------------
#
# The job sheet for one analysis attempt, successful or not. This is what the
# web page polls while it waits for a queued analysis to finish.
class AIAnalysisRunRead(BaseModel):
    id: str
    tenant_id: str
    ticket_id: str
    run_type: str        # what kind of work this was, e.g. "ticket_analysis". Room for
                         # other AI jobs to be added later without a new table

    # The field the polling loop watches: pending -> running -> succeeded/failed.
    status: str

    # Optional because the job sheet is created BEFORE the work starts, so some
    # of these are simply not known yet at that moment.
    model_provider: str | None
    model_name: str | None
    prompt_version: str | None    # not known until the worker picks a prompt template
    input_hash: str | None        # fingerprint of the ticket text; see _ticket_input_hash()
                                  # in routes/tickets.py for what it is for

    # Points at the result, once there is one. Empty while pending, and empty
    # forever if the run failed.
    output_recommendation_id: str | None

    # Filled in only on failure. Two fields rather than one, on purpose:
    #   error_code    - a short, stable label like "queue_unavailable", safe to
    #                   count and group by in dashboards
    #   error_message - the full human-readable detail, for someone debugging
    error_code: str | None
    error_message: str | None

    # Three timestamps, which together tell the whole story of the job:
    #   created -> started   = how long it sat waiting in the queue
    #   started -> finished  = how long the AI actually took
    # A large gap in the first means the worker is overloaded; a large gap in
    # the second means the AI service is slow. Very different problems.
    created_at: datetime
    started_at: datetime | None     # still None while queued
    finished_at: datetime | None    # still None while queued or running

    # The result, nested right inside — a convenience so the polling page gets
    # the answer in the same reply that tells it the job is done, rather than
    # having to make a second request. Defaults to None so it can simply be left
    # out while the job is still in progress.
    output_recommendation: TicketRecommendationRead | None = None
