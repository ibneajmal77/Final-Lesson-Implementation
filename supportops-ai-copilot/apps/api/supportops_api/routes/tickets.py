# ============================================================================
# FILE: apps/api/supportops_api/routes/tickets.py
#
# THINK OF THIS FILE AS: the main counter of the whole application. Most of
# what this product actually does passes through here.
#
# WHAT A "TICKET" IS:
#   A customer's support request — "my payment failed", "how do I reset my
#   password". A human support agent has to read it, work out what it is about,
#   how urgent it is, and write a reply. This product's purpose is to have an
#   AI do a first draft of that work, which a human then approves or fixes.
#
# THE ENDPOINTS IN THIS FILE:
#   POST /tickets                          - record a new customer request
#   GET  /tickets                          - list this company's tickets
#   GET  /tickets/{id}                     - fetch one ticket
#   POST /tickets/{id}/baseline-analysis   - analyse using simple keyword rules
#   POST /tickets/{id}/ai-analysis         - analyse using the AI, WAIT for it
#   POST /tickets/{id}/analyze             - analyse using the AI, DON'T wait
#   GET  /tickets/{id}/analysis            - how did the queued jobs go?
#   GET  /tickets/{id}/recommendations     - the AI's suggestions for a ticket
#
# THE THREE WAYS TO ANALYSE A TICKET (the key idea in this file):
#
#   1. "baseline"  - no AI at all. Just keyword matching, in
#                    packages/domain/supportops_domain/services/baseline.py.
#                    It is instant, free, and never fails. Its real job is to
#                    be the yardstick: if the expensive AI can't beat simple
#                    keyword rules, it isn't worth paying for. The evaluation
#                    harness in packages/evals/ compares the two.
#
#   2. "ai-analysis" (synchronous) - calls the AI and makes the caller wait for
#                    the answer, maybe 2-10 seconds. Simple to reason about,
#                    and good for testing, but it ties up a connection the
#                    whole time and fails outright if the AI service is slow.
#
#   3. "analyze" (asynchronous) - the grown-up version, and the one the real UI
#                    uses. It writes down "this job needs doing" and replies
#                    immediately with 202 Accepted, meaning "I've taken your
#                    request, I haven't finished it yet". The background worker
#                    (apps/worker/) picks the job up and does the slow part.
#                    The page then polls /analysis to see when it is done.
#
# HOW A REQUEST FLOWS THROUGH THIS FILE:
#   dependencies.py checks the caller and opens a database session
#     -> a function below runs, checking the tenant and ticket exist
#          -> packages/db/.../repositories/*.py runs the actual SQL
#          -> packages/model_gateway/... talks to the AI (paths 2 and 3)
#          -> packages/observability/... records what happened
#     -> the result is converted to a schema object and sent back as JSON
# ============================================================================

import hashlib
import time
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

# --- The front desk helpers (see dependencies.py) ---
from supportops_api.dependencies import (
    Actor,
    get_ai_analysis_queue,
    get_current_actor,
    get_db_session,
)
from supportops_api.pilot import ai_analysis_eligibility  # "is the AI switched on for them?"

# --- "Schemas" define the exact shape of the JSON going in and out ---
from supportops_api.schemas.ai import AIAnalysisRunRead, TicketRecommendationRead
from supportops_api.schemas.tickets import TicketCreate, TicketRead
from supportops_api.settings import Settings, get_settings

# --- "Models" are the database tables, as Python objects ---
from supportops_db.models import AIRun, Ticket, TicketRecommendation

# --- "Repositories" hold all the actual database queries. Routes never write
#     SQL themselves; they always go through these, which keeps the database
#     details in one place and makes routes easy to test. ---
from supportops_db.repositories.ai_runs import (
    create_ai_run,
    list_ai_runs_for_ticket,
    mark_ai_run_failed,
)
from supportops_db.repositories.policies import tenant_policy_context
from supportops_db.repositories.recommendations import (
    create_ticket_recommendation,
    get_ticket_recommendation_by_id,
    list_ticket_recommendations,
)
from supportops_db.repositories.tenants import get_tenant
from supportops_db.repositories.tickets import (
    create_ticket,
    get_ticket_by_external_id,
    get_ticket_by_id,
    list_tickets,
)

# --- The no-AI keyword classifier, used by the baseline endpoint ---
from supportops_domain.services.baseline import BaselineTicketInput, classify_ticket

# --- Talking to the AI. The "gateway" wraps the AI service so the rest of the
#     app never deals with it directly, and can swap real AI for a fake one. ---
from supportops_model_gateway.errors import (
    ModelProviderConfigurationError,  # we set it up wrong (e.g. missing API key)
    ModelProviderRequestError,  # couldn't reach it / it timed out
    ModelProviderResponseError,  # it replied, but with nonsense we can't use
    UnsupportedModelProviderError,  # asked for a provider that doesn't exist
)
from supportops_model_gateway.providers.base import TicketAnalysisInput
from supportops_model_gateway.routing import build_ticket_analysis_provider

# --- Logging, counters, and traces: how we see what the app is doing ---
from supportops_observability.logging import get_logger, log_context
from supportops_observability.metrics import (
    record_ai_analysis_failed,
    record_ai_analysis_latency,
    record_ai_analysis_started,
    record_ai_analysis_succeeded,
    record_draft_escalated,
    record_ticket_created,
)
from supportops_observability.model_usage import record_ticket_analysis_usage
from supportops_observability.tracing import trace_span

# "prefix" means every path below automatically starts with /tickets, so the
# route written as "/{ticket_id}" is really /tickets/{ticket_id}.
router = APIRouter(prefix="/tickets", tags=["tickets"])
logger = get_logger(__name__)

# Shorthand names for the four things routes ask for. Reading one of these:
#   "ActorDep" means "an Actor, obtained by running get_current_actor first".
# Defining them once here keeps every route signature below short and readable,
# instead of repeating the full Annotated[...] spelling in each one.
ActorDep = Annotated[Actor, Depends(get_current_actor)]      # who is calling
SessionDep = Annotated[Session, Depends(get_db_session)]     # database connection
SettingsDep = Annotated[Settings, Depends(get_settings)]     # configuration
QueueDep = Annotated[Any, Depends(get_ai_analysis_queue)]    # the job queue for the worker


# ---------------------------------------------------------------------------
# Record a new customer support request.
# 201 Created is the correct HTTP code for "a new thing now exists".
# ---------------------------------------------------------------------------
@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket_endpoint(
    payload: TicketCreate,     # the JSON body sent in, already checked against schemas/tickets.py
    response: Response,        # asked for so the status code can be changed on the fly, below
    actor: ActorDep,
    session: SessionDep,
) -> TicketRead:
    _require_tenant(session, actor.tenant_id)

    # Have we already stored this one? "external_id" is the ID the ticket had
    # in the customer's own helpdesk system (Zendesk, Freshdesk, ...), which is
    # how we recognise a repeat.
    #
    # This makes the endpoint "idempotent": sending the same request twice has
    # the same effect as sending it once. That matters because the systems
    # feeding us tickets will retry when a reply gets lost in transit — without
    # this check, every retry would create a duplicate ticket.
    existing = get_ticket_by_external_id(
        session,
        tenant_id=actor.tenant_id,
        external_id=payload.external_id,
    )
    if existing:
        # 200 OK, not 201 Created — nothing new was created this time, and the
        # caller deserves to be told the difference honestly.
        response.status_code = status.HTTP_200_OK
        return _ticket_to_read(existing)

    with trace_span("db.create_ticket", tenant_id=actor.tenant_id):
        ticket = create_ticket(
            session,
            tenant_id=actor.tenant_id,        # stamped with the caller's company, always
            external_id=payload.external_id,
            channel=payload.channel,          # where it came from: email, chat, web form...
            subject=payload.subject,
            body=payload.body,
            customer_id=payload.customer_id,
            metadata=payload.metadata,        # any extra free-form details
        )
        session.commit()          # actually save it. Until this line, nothing is permanent.
        session.refresh(ticket)   # re-read the row, to pick up values the database filled in
                                  # itself (the generated id, created_at timestamp, and so on)

    record_ticket_created(tenant_id=actor.tenant_id)     # bump a counter, for the dashboards
    logger.info("ticket_created", extra={"ticket_id": ticket.id})
    return _ticket_to_read(ticket)


# ---------------------------------------------------------------------------
# List every ticket belonging to the caller's company.
# Note tenant_id comes from the verified `actor`, never from the caller's own
# request. That is the rule that stops one company reading another's tickets,
# and it is repeated in every single function in this file.
# ---------------------------------------------------------------------------
@router.get("", response_model=list[TicketRead])
def list_tickets_endpoint(
    actor: ActorDep,
    session: SessionDep,
) -> list[TicketRead]:
    _require_tenant(session, actor.tenant_id)
    return [_ticket_to_read(ticket) for ticket in list_tickets(session, tenant_id=actor.tenant_id)]


# ---------------------------------------------------------------------------
# Fetch one specific ticket.
# ---------------------------------------------------------------------------
@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket_endpoint(
    ticket_id: str,           # taken from the web address, because {ticket_id} is in the path
    actor: ActorDep,
    session: SessionDep,
) -> TicketRead:
    _require_tenant(session, actor.tenant_id)
    # The lookup is filtered by tenant, so requesting another company's ticket
    # ID returns "not found" — the same answer as an ID that doesn't exist.
    # That is on purpose: replying "exists, but not yours" would quietly confirm
    # that a competitor's ticket ID is real.
    ticket = get_ticket_by_id(session, tenant_id=actor.tenant_id, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")
    return _ticket_to_read(ticket)


# ---------------------------------------------------------------------------
# ANALYSIS PATH 1: the baseline. No AI, just keyword rules.
#
# Instant, free, and it cannot fail — so there is no error handling here at
# all, in sharp contrast to the AI endpoint below. Its value is as a
# comparison point: any AI we pay for must do better than this.
# ---------------------------------------------------------------------------
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

    with log_context(ticket_id=ticket.id), trace_span(
        "baseline.analysis",
        tenant_id=actor.tenant_id,
        ticket_id=ticket.id,
    ):
        # The whole "analysis" is this one call: pure keyword matching.
        analysis = classify_ticket(BaselineTicketInput(subject=ticket.subject, body=ticket.body))
        recommendation = create_ticket_recommendation(
            session,
            tenant_id=actor.tenant_id,
            ticket_id=ticket.id,
            source=analysis.source,                       # "baseline", so we can tell later
                                                          # which method produced this
            category=analysis.category,                   # billing / technical / account...
            priority=analysis.priority,                   # low / medium / high
            requires_escalation=analysis.requires_escalation,   # does a human need to step in?
            confidence=analysis.confidence,               # how sure it is, 0.0 to 1.0
            extracted_fields=analysis.extracted_fields,   # useful details found in the text
            reasons=analysis.reasons,                     # why it decided this — so a human
                                                          # can judge whether to trust it
            # Note: no model_name, prompt_version, summary or suggested_reply.
            # Keyword rules can't write a reply; only the AI path fills those in.
        )
        session.commit()
        session.refresh(recommendation)

    if recommendation.requires_escalation:
        record_draft_escalated(provider=analysis.source, category=analysis.category)
    return _recommendation_to_read(recommendation)


# ---------------------------------------------------------------------------
# ANALYSIS PATH 2: real AI, and the caller waits for the answer.
#
# This is the longest function in the file, and almost all of the extra length
# is error handling. That is the honest cost of depending on an outside
# service: it can be misconfigured, unreachable, slow, or simply return
# rubbish, and each case deserves a different answer to the caller.
# ---------------------------------------------------------------------------
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

    # Work out roughly what this ticket is about (using the free keyword rules)
    # so we can check whether the AI is switched on for this kind of ticket.
    # This is the "pilot" mechanism: roll the AI out to a few companies and a
    # few ticket types first, rather than to everyone at once. See pilot.py.
    pilot_category = _pilot_category(ticket)
    _require_ai_analysis_enabled(
        settings,
        tenant_id=actor.tenant_id,
        category=pilot_category,
    )

    analysis_started = time.perf_counter()   # stopwatch for the WHOLE endpoint
    model_elapsed_seconds = 0.0              # separate stopwatch, for just the AI call
    record_ai_analysis_started(provider=settings.model_provider, mode="sync")
    with log_context(ticket_id=ticket.id), trace_span(
        "api.ai_analysis",
        tenant_id=actor.tenant_id,
        ticket_id=ticket.id,
        model_provider=settings.model_provider,
    ):
        try:
            # Build the object that knows how to talk to the AI. Which one you
            # get depends on the model_provider setting — "mock" gives a fake
            # that returns canned answers, "hosted" calls a real paid service.
            # The decision is made in model_gateway/routing.py.
            provider = build_ticket_analysis_provider(
                settings.model_provider,
                api_key=settings.model_api_key,
                model_name=settings.model_name,
                base_url=settings.model_base_url,
                timeout_seconds=settings.model_timeout_seconds,
                max_output_tokens=settings.model_max_output_tokens,
            )
            model_started = time.perf_counter()
            with trace_span(
                "model_gateway.call",
                ticket_id=ticket.id,
                model_provider=settings.model_provider,
            ):
                # THE ACTUAL AI CALL. This is the slow line — everything else in
                # this function is milliseconds; this can take several seconds.
                analysis = provider.analyze_ticket(
                    TicketAnalysisInput(
                        subject=ticket.subject,
                        body=ticket.body,
                        customer_id=ticket.customer_id,
                        # The company's own rules — refund limits, tone of voice,
                        # things never to promise — fetched from the database and
                        # included in the question so the AI's answer obeys them.
                        policy_context=tenant_policy_context(
                            session,
                            tenant_id=actor.tenant_id,
                        ),
                    )
                )
            model_elapsed_seconds = time.perf_counter() - model_started

        # Three separate catches, because the three kinds of failure mean
        # genuinely different things and deserve different HTTP codes.

        # (a) OUR fault — bad configuration, e.g. no API key set.
        # 503 tells the caller "unavailable, try later" rather than blaming them.
        except (UnsupportedModelProviderError, ModelProviderConfigurationError) as exc:
            _record_analysis_failure(settings.model_provider, "sync", exc)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="model provider is not configured",
            ) from exc      # "from exc" keeps the original error attached underneath,
                            # so the logs still show the real cause

        # (b) We couldn't reach the AI service, or it timed out.
        # 503 again: temporary, and retrying later is reasonable.
        except ModelProviderRequestError as exc:
            _record_analysis_failure(settings.model_provider, "sync", exc)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="model provider is unavailable",
            ) from exc

        # (c) It answered, but with something we can't use — malformed JSON, or
        # missing fields. 502 Bad Gateway is the precise code for "a service
        # further upstream gave me a broken answer". Retrying probably won't
        # help here, which is why it isn't lumped in with the 503s.
        except ModelProviderResponseError as exc:
            _record_analysis_failure(settings.model_provider, "sync", exc)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="model provider returned invalid output",
            ) from exc

        # Success. Save the AI's suggestion. Note this stores the same fields as
        # the baseline path PLUS four more that only an AI can produce.
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
            model_name=analysis.model_name,          # exactly which model wrote this...
            prompt_version=analysis.prompt_version,  # ...and which version of our instructions.
                                                     # Both recorded so that when quality shifts,
                                                     # you can tell what changed.
            summary=analysis.summary,                # a short recap of the customer's problem
            suggested_reply=analysis.suggested_reply,  # the draft reply, for a human to approve
        )

        # Record what this call cost us: how many tokens, and how much money.
        # Feeds the metrics endpoint and docs/cost-report.md.
        record_ticket_analysis_usage(
            session,
            tenant_id=actor.tenant_id,
            ticket_id=ticket.id,
            analysis=analysis,
            operation="sync_ticket_analysis",
            input_cost_per_1k_tokens=settings.model_input_cost_per_1k_tokens,
            output_cost_per_1k_tokens=settings.model_output_cost_per_1k_tokens,
            # If the AI service didn't tell us how long it took, fall back on
            # our own stopwatch reading.
            fallback_latency_seconds=model_elapsed_seconds,
            recommendation_id=recommendation.id,
        )
        # One commit saves BOTH the recommendation and the cost record together.
        # Deliberate: they are one fact, so either both are stored or neither is.
        # Never a suggestion with no record of what it cost.
        session.commit()
        session.refresh(recommendation)

    if recommendation.requires_escalation:
        record_draft_escalated(provider=analysis.source, category=analysis.category)
    record_ai_analysis_succeeded(provider=analysis.source, mode="sync")
    record_ai_analysis_latency(          # how long the whole thing took, for the dashboards
        time.perf_counter() - analysis_started,
        provider=analysis.source,
        mode="sync",
    )
    logger.info(
        "ai_analysis_succeeded",
        extra={
            "ticket_id": ticket.id,
            "model_provider": analysis.source,
            "model_name": analysis.model_name,
        },
    )
    return _recommendation_to_read(recommendation)


# ---------------------------------------------------------------------------
# ANALYSIS PATH 3: real AI, but nobody waits. This is what the real UI uses.
#
# Instead of doing the slow work now, it writes down a job and hands it off.
# The reply is 202 Accepted, which means precisely: "I've taken your request
# and it is valid, but it is not finished yet. Check back later."
#
# THE HAND-OFF, STEP BY STEP:
#   1. Write an "AIRun" row in the database — the job sheet, marked "pending"
#   2. Push its ID into the Redis queue
#   3. Reply 202 with the job sheet, so the caller can track it
#   ...later...
#   4. apps/worker/ picks the ID out of the queue, does the AI call, and
#      updates that same row to "succeeded" or "failed"
#   5. The page polls GET /analysis (below) until it changes
# ---------------------------------------------------------------------------
@router.post(
    "/{ticket_id}/analyze",
    response_model=AIAnalysisRunRead,
    status_code=status.HTTP_202_ACCEPTED,
)
def enqueue_ticket_analysis_endpoint(
    ticket_id: str,
    actor: ActorDep,
    session: SessionDep,
    settings: SettingsDep,
    queue: QueueDep,
) -> AIAnalysisRunRead:
    _require_tenant(session, actor.tenant_id)
    ticket = get_ticket_by_id(session, tenant_id=actor.tenant_id, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")
    pilot_category = _pilot_category(ticket)
    _require_ai_analysis_enabled(
        settings,
        tenant_id=actor.tenant_id,
        category=pilot_category,
    )

    with log_context(ticket_id=ticket.id), trace_span(
        "api.enqueue_ai_analysis",
        tenant_id=actor.tenant_id,
        ticket_id=ticket.id,
        model_provider=settings.model_provider,
    ):
        # STEP 1: create the job sheet and save it FIRST, before queueing.
        # The order is deliberate. Written first, a job that never reaches the
        # queue still leaves a visible record stuck in "pending", which someone
        # can find and retry. Queued first, a crash before writing would leave
        # the worker holding an ID for a row that doesn't exist.
        run = create_ai_run(
            session,
            tenant_id=actor.tenant_id,
            ticket_id=ticket.id,
            run_type="ticket_analysis",
            model_provider=settings.model_provider,
            model_name=settings.model_name,
            prompt_version=None,      # not known yet — the worker fills this in when it runs
            input_hash=_ticket_input_hash(ticket),   # fingerprint of the input; see below
        )
        session.commit()
        session.refresh(run)
        record_ai_analysis_started(provider=settings.model_provider, mode="async")

        try:
            # STEP 2: push the job ID onto the queue. Note only the ID travels —
            # not the ticket text. The worker fetches whatever it needs from the
            # database itself, which keeps the queue small and means the worker
            # always reads the current data rather than a stale copy.
            with log_context(ai_run_id=run.id), trace_span(
                "queue.enqueue",
                tenant_id=actor.tenant_id,
                ticket_id=ticket.id,
                ai_run_id=run.id,
            ):
                job = queue.enqueue_ai_analysis(run.id)
        except Exception as exc:
            # Redis is down, so the job will never be picked up. Rather than
            # leaving the row sitting in "pending" forever — where it would look
            # like work still in progress — mark it failed immediately, so the
            # database tells the truth about what happened.
            mark_ai_run_failed(
                session,
                run,
                error_code="queue_unavailable",
                error_message=str(exc),
            )
            session.commit()
            record_ai_analysis_failed(
                provider=settings.model_provider,
                mode="async",
                error_code="queue_unavailable",
            )
            logger.warning(
                "ai_analysis_enqueue_failed",
                extra={
                    "ticket_id": ticket.id,
                    "ai_run_id": run.id,
                    "error_code": "queue_unavailable",
                },
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="analysis queue is unavailable",
            ) from exc

    logger.info(
        "ai_analysis_enqueued",
        extra={"ticket_id": ticket.id, "ai_run_id": run.id, "job_id": _job_id(job)},
    )
    # STEP 3: hand back the job sheet, so the caller knows what to poll for.
    return _analysis_run_to_read(session, run)


# ---------------------------------------------------------------------------
# "How are my queued jobs getting on?" — the other half of path 3.
#
# The web page calls this every couple of seconds after starting an analysis,
# watching for the status to change from "pending" to "succeeded" or "failed".
# This repeated asking is called polling: cruder than having the server push an
# update, but far simpler, and perfectly adequate at this scale.
# ---------------------------------------------------------------------------
@router.get("/{ticket_id}/analysis", response_model=list[AIAnalysisRunRead])
def list_ticket_analysis_endpoint(
    ticket_id: str,
    actor: ActorDep,
    session: SessionDep,
) -> list[AIAnalysisRunRead]:
    _require_tenant(session, actor.tenant_id)
    ticket = get_ticket_by_id(session, tenant_id=actor.tenant_id, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    runs = list_ai_runs_for_ticket(
        session,
        tenant_id=actor.tenant_id,
        ticket_id=ticket.id,
    )
    return [_analysis_run_to_read(session, run) for run in runs]


# ---------------------------------------------------------------------------
# Every AI suggestion made for this ticket, from any of the three paths.
# A ticket can have several — a baseline one and an AI one, or several AI
# attempts. Nothing is ever overwritten or deleted, so the full history of what
# was suggested stays available for review.
# ---------------------------------------------------------------------------
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


# ===========================================================================
# HELPERS BELOW THIS LINE
#
# By convention in Python, a leading underscore means "internal to this file" —
# these are not meant to be imported elsewhere.
# ===========================================================================


# Turns a job sheet from the database into the shape sent back as JSON.
#
# If the job finished successfully, it also fetches the resulting suggestion and
# nests it inside. That is a convenience for the web page: once the status flips
# to "succeeded", the answer is right there in the same reply, with no need for
# a second request.
def _analysis_run_to_read(session: Session, run: AIRun) -> AIAnalysisRunRead:
    output_recommendation = None
    if run.output_recommendation_id:      # empty until the worker has finished
        recommendation = get_ticket_recommendation_by_id(
            session,
            tenant_id=run.tenant_id,
            ticket_id=run.ticket_id,
            recommendation_id=run.output_recommendation_id,
        )
        if recommendation:                # defensive: the ID could point at a row that
                                          # retention cleanup has since removed
            output_recommendation = _recommendation_to_read(recommendation)

    return AIAnalysisRunRead(
        id=run.id,
        tenant_id=run.tenant_id,
        ticket_id=run.ticket_id,
        run_type=run.run_type,
        status=run.status,                # pending / running / succeeded / failed
        model_provider=run.model_provider,
        model_name=run.model_name,
        prompt_version=run.prompt_version,
        input_hash=run.input_hash,
        output_recommendation_id=run.output_recommendation_id,
        error_code=run.error_code,        # filled in only on failure
        error_message=run.error_message,
        created_at=run.created_at,        # these three timestamps let you see how long the
        started_at=run.started_at,        # job waited in the queue (created -> started) and
        finished_at=run.finished_at,      # how long the work itself took (started -> finished)
        output_recommendation=output_recommendation,
    )


# Digs the ID out of whatever the queue handed back, for logging purposes.
#
# It handles two shapes because the real queue library returns an object with
# an `.id` attribute, while the fake queue used in tests returns a plain
# dictionary. Rather than force both to match, this just copes with either, and
# returns None if it recognises neither — a missing log detail is never worth
# failing a request over.
def _job_id(job: object) -> str | None:
    if isinstance(job, dict):
        value = job.get("id")
        return value if isinstance(value, str) else None
    value = getattr(job, "id", None)
    return value if isinstance(value, str) else None


# Makes a short fingerprint of a ticket's text.
#
# A "hash" turns any amount of text into a fixed-length code. Same text in,
# same code out; even a one-character change gives a completely different code.
#
# Why bother? Two reasons:
#   1. You can tell whether two analysis runs were given identical input, which
#      matters when comparing results or spotting needless repeat work.
#   2. The code can be logged safely. It cannot be turned back into the original
#      text, so it never leaks a customer's private words into the logs.
#
# The "\0" between the pieces is a separator character that can't appear in
# normal text. Without it, subject "ab" + body "c" and subject "a" + body "bc"
# would produce the same fingerprint, wrongly looking like the same ticket.
def _ticket_input_hash(ticket: Ticket) -> str:
    raw_input = "\0".join(
        [
            ticket.subject,
            ticket.body,
            ticket.customer_id or "",     # "or" handles a missing customer, since you
                                          # cannot join None into a string
        ]
    )
    return hashlib.sha256(raw_input.encode("utf-8")).hexdigest()

# Works out what a ticket is about, using the free keyword rules, purely so the
# pilot check below can ask "is the AI switched on for this type of ticket?".
# We can't ask the AI itself what the ticket is about — that would mean paying
# for the very call we are still deciding whether to allow.
def _pilot_category(ticket: Ticket) -> str:
    return classify_ticket(BaselineTicketInput(subject=ticket.subject, body=ticket.body)).category


# Blocks the request unless the AI is switched on for this company and this
# ticket type. The actual rules live in pilot.py; this function's job is only
# to turn the answer into the right HTTP error.
#
# Note the two different codes, which is a genuinely useful distinction:
#   503 - the AI is off for EVERYONE right now (e.g. we switched it off during
#         an incident). Temporary; try again later.
#   403 - the AI works fine, you specifically aren't in the pilot group. No
#         amount of retrying will change that.
def _require_ai_analysis_enabled(
    settings: Settings,
    *,                        # the bare * forces every argument after it to be named at the
                              # call site, so you can never mix up tenant_id and category
    tenant_id: str,
    category: str,
) -> None:
    eligibility = ai_analysis_eligibility(settings, tenant_id=tenant_id, category=category)
    if eligibility.enabled:
        return                # allowed — carry on
    if eligibility.reason == "ai_analysis_disabled":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ai analysis is disabled",
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="ai analysis is not enabled for this tenant or category",
    )


# One place to record an AI failure, so the counter and the log line always
# agree with each other. Called from all three error branches above.
#
# It records the error's TYPE name rather than its full message, for the same
# reason as in checks.py: the message may contain the API key, the request
# body, or a customer's text, none of which belong in a metrics label.
def _record_analysis_failure(provider: str, mode: str, exc: Exception) -> None:
    error_code = exc.__class__.__name__
    record_ai_analysis_failed(provider=provider, mode=mode, error_code=error_code)
    logger.warning(
        "ai_analysis_failed",
        extra={"model_provider": provider, "error_code": error_code},
    )


# Confirms the company in the caller's headers is one we actually know about.
#
# Remember from dependencies.py that those headers are trusted, not verified —
# so this is the check that an unknown or made-up tenant ID gets no further
# than here. Every endpoint in this file calls it first, without exception.
def _require_tenant(session: Session, tenant_id: str) -> None:
    if not get_tenant(session, tenant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tenant not found")


# --- The two converters, database row -> outgoing JSON ---------------------
#
# Why not just return the database object directly? Because that would tie the
# public API to the internal table layout: rename a column and every caller
# breaks. Converting by hand means these functions are the one place where the
# public shape is decided, and it can stay stable while the database changes
# underneath. It is also a safety net — a column added to the table is NOT
# automatically exposed to the outside world.
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
        metadata=ticket.metadata_json,    # renamed on the way out: the column is
                                          # metadata_json, but callers see "metadata"
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
    )


def _recommendation_to_read(recommendation: TicketRecommendation) -> TicketRecommendationRead:
    return TicketRecommendationRead(
        id=recommendation.id,
        tenant_id=recommendation.tenant_id,
        ticket_id=recommendation.ticket_id,
        source=recommendation.source,                # "baseline" or the AI provider's name
        category=recommendation.category,
        priority=recommendation.priority,
        requires_escalation=recommendation.requires_escalation,
        confidence=recommendation.confidence,
        model_name=recommendation.model_name,        # these four are empty for baseline
        prompt_version=recommendation.prompt_version,  # results, and filled in for AI ones
        summary=recommendation.summary,
        suggested_reply=recommendation.suggested_reply,
        extracted_fields=recommendation.extracted_fields_json,   # again, the "_json" suffix is
        reasons=recommendation.reasons_json,                     # internal and dropped here
        created_at=recommendation.created_at,
    )
