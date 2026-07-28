# ============================================================================
# FILE: apps/worker/supportops_worker/jobs.py
#
# THINK OF THIS FILE AS: what the background worker actually DOES when it picks
# a job off the queue. This is the heart of the worker.
#
# WHERE IT FITS:
#   routes/tickets.py POST /analyze creates a job sheet and queues its ID
#     -> queues.py pushed the ID onto the Redis list
#          -> main.py's worker loop pulled it off
#               -> THIS FILE runs, does the AI call, and writes the result
#                    -> the web page, polling GET /analysis, sees it appear
#
# HOW IT COMPARES TO THE SYNCHRONOUS VERSION:
#   The equivalent code in routes/tickets.py (create_ai_analysis_endpoint) does
#   nearly the same work. The differences are what make this the more capable
#   path, and they are worth understanding:
#
#     - NOBODY IS WAITING. So failures cannot be reported by returning an HTTP
#       error. Instead every outcome is WRITTEN TO THE DATABASE, onto the job
#       sheet, where the polling page will find it. That is why this file never
#       raises for an expected failure — it records and returns.
#
#     - IT ALSO RUNS THE BASELINE, and stores that result alongside the AI's.
#       Free, instant, and it means every AI answer arrives with a second
#       opinion attached for comparison.
#
#     - IT UNDERSTANDS "ABSTAIN". If the AI says it isn't sure enough to answer,
#       that is recorded as its own distinct outcome — neither success nor
#       failure. More on this below; it is the most interesting idea here.
#
# THE STATE MACHINE THIS FILE DRIVES:
#   pending -> running -> succeeded
#                      -> abstained
#                      -> failed
#   The job sheet is updated at each step, so the database always reflects
#   reality even if the worker is killed mid-job.
# ============================================================================

import time

from sqlalchemy.orm import Session

# The worker deliberately reuses the API's pilot rules and settings, so both
# programs make identical decisions about when the AI may run.
from supportops_api.pilot import ai_analysis_eligibility
from supportops_api.settings import Settings, get_settings
from supportops_db.repositories.ai_runs import (
    get_ai_run_by_id,
    mark_ai_run_abstained,  # the four functions that move the job sheet
    mark_ai_run_failed,  # through its states
    mark_ai_run_running,
    mark_ai_run_succeeded,
)
from supportops_db.repositories.policies import tenant_policy_context
from supportops_db.repositories.recommendations import create_ticket_recommendation
from supportops_db.repositories.tickets import get_ticket_by_id
from supportops_db.session import create_db_engine, create_session_factory
from supportops_domain.services.baseline import BaselineTicketInput, classify_ticket
from supportops_model_gateway.errors import ModelGatewayError, UnsupportedModelProviderError
from supportops_model_gateway.providers.base import TicketAnalysisInput
from supportops_model_gateway.routing import build_ticket_analysis_provider
from supportops_observability.logging import get_logger, log_context
from supportops_observability.metrics import (
    record_ai_analysis_failed,
    record_ai_analysis_latency,
    record_ai_analysis_succeeded,
    record_draft_escalated,
)
from supportops_observability.model_usage import record_ticket_analysis_usage
from supportops_observability.tracing import trace_span

logger = get_logger(__name__)


# THE ENTRY POINT. This exact function name is written as text into the queue by
# queues.py ("supportops_worker.jobs.analyze_ticket_job"), and RQ imports and
# calls it here. Renaming it would break every job already sitting in the queue.
#
# It is a thin wrapper whose only job is to set up a database connection, then
# hand over to run_ticket_analysis below.
#
# WHY THE SPLIT INTO TWO FUNCTIONS: this one creates its own engine and session,
# which is what you need when running standalone in a worker process. The real
# logic underneath simply ACCEPTS a session, so tests can pass in one pointing
# at a temporary test database. Mixing the two would make the logic untestable
# without a live Redis and Postgres.
def analyze_ticket_job(ai_run_id: str) -> str:
    settings = get_settings()
    # A fresh engine per job. Slightly wasteful compared to the API's cached one,
    # but correct here: RQ runs each job in a forked child process, and a database
    # connection inherited across a fork cannot be safely shared.
    engine = create_db_engine(settings.database_url)
    session_factory = create_session_factory(engine)

    with session_factory() as session:      # `with` guarantees the connection is closed
        run = run_ticket_analysis(session=session, settings=settings, ai_run_id=ai_run_id)
        return run.id     # RQ stores whatever is returned as the job's result


# The real work. Long, but it is a straight line: check, decide, call the AI,
# save. The length comes from every step having a recorded failure path.
def run_ticket_analysis(session: Session, settings: Settings, ai_run_id: str):
    run = get_ai_run_by_id(session, ai_run_id=ai_run_id)
    if not run:
        # The one case that DOES raise rather than recording a failure — and for
        # a good reason. Every other failure is written onto the job sheet, but
        # here there is no job sheet to write on. Raising lets RQ mark the job
        # failed in its own records, which is the only place left to put it.
        raise ValueError(f"ai run not found: {ai_run_id}")

    analysis_started = time.perf_counter()     # stopwatch for the whole job
    with log_context(
        # Attaches these IDs to every log line written from here on, including
        # ones from deep inside the model gateway and database code. This is
        # what lets you search the logs for one ticket and see its whole story.
        tenant_id=run.tenant_id,
        ticket_id=run.ticket_id,
        ai_run_id=run.id,
    ), trace_span(
        "worker.ai_analysis",
        tenant_id=run.tenant_id,
        ticket_id=run.ticket_id,
        ai_run_id=run.id,
        model_provider=settings.model_provider,
    ):
        # STEP 1: mark it "running", and commit immediately.
        #
        # The immediate commit matters. It makes the change visible to everyone
        # else right away, so the polling web page shows "running" rather than
        # sitting on "pending", and a second worker cannot mistake this for
        # unclaimed work.
        mark_ai_run_running(session, run)
        session.commit()

        # STEP 2: fetch the ticket. It existed when the job was created, but time
        # has passed — it may have been deleted by the retention cleanup since.
        ticket = get_ticket_by_id(session, tenant_id=run.tenant_id, ticket_id=run.ticket_id)
        if not ticket:
            mark_ai_run_failed(
                session,
                run,
                error_code="ticket_not_found",
                error_message="ticket was not found for queued AI run",
            )
            session.commit()
            record_ai_analysis_failed(
                provider=settings.model_provider,
                mode="async",              # "async" throughout this file, so the dashboards can
                                           # compare queued work against the synchronous path
                error_code="ticket_not_found",
            )
            logger.warning(
                "ai_analysis_failed",
                extra={"error_code": "ticket_not_found"},
            )
            # RETURNS rather than raising. The failure is recorded, the page will
            # show it, and there is nothing here that retrying would fix — so
            # there is no reason to make RQ treat this as a crash.
            return run

        # STEP 3: run the free keyword classifier.
        #
        # It serves two purposes at once here. First, its category decides
        # whether the AI is allowed to run at all (next step). Second, the result
        # is kept and stored beside the AI's answer as a second opinion.
        baseline = classify_ticket(BaselineTicketInput(subject=ticket.subject, body=ticket.body))

        # STEP 4: is the AI switched on for this company and this ticket type?
        #
        # Checked again even though routes/tickets.py already checked before
        # queueing. Not redundant: the job may have sat in the queue for minutes
        # while someone switched the AI off — perhaps because it started
        # misbehaving. Re-checking at the moment of use is what makes the kill
        # switch actually immediate.
        eligibility = ai_analysis_eligibility(
            settings,
            tenant_id=run.tenant_id,
            category=baseline.category,
        )
        if not eligibility.enabled:
            error_code = eligibility.reason or "ai_analysis_not_enabled"
            mark_ai_run_failed(
                session,
                run,
                error_code=error_code,     # the precise reason, so "we turned it off" and
                                           # "this company isn't in the pilot" stay distinguishable
                error_message="AI analysis is not enabled for this tenant or category",
            )
            session.commit()
            record_ai_analysis_failed(
                provider=settings.model_provider,
                mode="async",
                error_code=error_code,
            )
            logger.warning("ai_analysis_failed", extra={"error_code": error_code})
            return run

        try:
            # STEP 5: build the AI client and make the call. The slow part.
            provider = build_ticket_analysis_provider(
                settings.model_provider,
                api_key=settings.model_api_key,
                model_name=settings.model_name,
                base_url=settings.model_base_url,
                timeout_seconds=settings.model_timeout_seconds,
                max_output_tokens=settings.model_max_output_tokens,
            )
            model_started = time.perf_counter()      # a second stopwatch, timing only the AI
            with trace_span(
                "model_gateway.call",
                tenant_id=run.tenant_id,
                ticket_id=run.ticket_id,
                ai_run_id=run.id,
                model_provider=settings.model_provider,
            ):
                analysis = provider.analyze_ticket(
                    TicketAnalysisInput(
                        subject=ticket.subject,
                        body=ticket.body,
                        customer_id=ticket.customer_id,
                        # The company's own written rules, pulled from the database
                        # and included so the AI's answer respects them.
                        policy_context=tenant_policy_context(
                            session,
                            tenant_id=run.tenant_id,
                        ),
                    )
                )
            model_elapsed_seconds = time.perf_counter() - model_started

            # STEP 6: bundle the AI's extracted details together with the
            # baseline's opinion and this job's ID. See the helper at the bottom.
            extracted_fields = _worker_extracted_fields(
                analysis_fields=analysis.extracted_fields,
                baseline_category=baseline.category,
                baseline_priority=baseline.priority,
                baseline_confidence=baseline.confidence,
                ai_run_id=run.id,
            )

            # STEP 7: save the AI's suggestion.
            recommendation = create_ticket_recommendation(
                session,
                tenant_id=run.tenant_id,
                ticket_id=run.ticket_id,
                source=analysis.source,
                category=analysis.category,
                priority=analysis.priority,
                requires_escalation=analysis.requires_escalation,
                confidence=analysis.confidence,
                extracted_fields=extracted_fields,
                # The AI's own reasons, plus one extra line stating what the
                # keyword rules thought. The `*` unpacks the existing list into
                # this new one. A reviewer reading the reasons therefore sees
                # both opinions, and a disagreement between them is a useful
                # prompt to look more carefully.
                reasons=[
                    *analysis.reasons,
                    _baseline_reason(baseline.category, baseline.priority),
                ],
                model_name=analysis.model_name,
                prompt_version=analysis.prompt_version,
                summary=analysis.summary,
                suggested_reply=analysis.suggested_reply,
            )

            # STEP 8: record tokens used and money spent.
            record_ticket_analysis_usage(
                session,
                tenant_id=run.tenant_id,
                ticket_id=run.ticket_id,
                ai_run_id=run.id,                       # the async path can link the cost to a
                                                        # specific job; the sync path cannot
                recommendation_id=recommendation.id,
                analysis=analysis,
                operation="async_ticket_analysis",      # distinguishes these costs from the
                                                        # synchronous endpoint's in reports
                input_cost_per_1k_tokens=settings.model_input_cost_per_1k_tokens,
                output_cost_per_1k_tokens=settings.model_output_cost_per_1k_tokens,
                fallback_latency_seconds=model_elapsed_seconds,
            )

            # STEP 9: SUCCEEDED, or ABSTAINED?
            #
            # "Abstain" means the AI declined to answer — the ticket was
            # ambiguous, or it lacked the information to be confident. A model
            # that says "I don't know" is behaving WELL, and treating that as a
            # failure would be actively harmful: it would push the system toward
            # models that always guess, which is exactly what you don't want in
            # something drafting replies to customers.
            #
            # So it gets its own state. The recommendation is still saved (its
            # reasons explain why it abstained, which is useful to a human), the
            # cost is still recorded (it was still a paid call), but the outcome
            # is honestly labelled as neither success nor failure. Scoring
            # abstentions as successes would inflate the quality figures.
            if analysis.extracted_fields.get("abstain") is True:
                mark_ai_run_abstained(
                    session,
                    run,
                    output_recommendation_id=recommendation.id,
                    model_name=analysis.model_name,
                    prompt_version=analysis.prompt_version,
                )
            else:
                mark_ai_run_succeeded(
                    session,
                    run,
                    output_recommendation_id=recommendation.id,   # links the job sheet to
                                                                  # its result
                    model_name=analysis.model_name,
                    prompt_version=analysis.prompt_version,       # now known, unlike when the
                                                                  # job sheet was first created
                )

            # ONE commit for everything in steps 7-9: the recommendation, the
            # cost record, and the status change. Deliberate — all three are one
            # fact. A crash between them would otherwise leave, say, a completed
            # recommendation attached to a job still claiming to be "running".
            session.commit()

            if recommendation.requires_escalation:
                record_draft_escalated(provider=analysis.source, category=analysis.category)
            record_ai_analysis_succeeded(provider=analysis.source, mode="async")
            record_ai_analysis_latency(
                # The WHOLE job's duration, not just the AI call. From the
                # queue's point of view this is the number that matters; the
                # AI-only timing was recorded separately in step 8.
                time.perf_counter() - analysis_started,
                provider=analysis.source,
                mode="async",
            )
            logger.info(
                "ai_analysis_succeeded",
                extra={"model_provider": analysis.source, "model_name": analysis.model_name},
            )
            return run

        # Every AI-related failure caught in one place, unlike routes/tickets.py
        # which splits them into three. The reason for the difference: the API
        # had to pick a different HTTP status code per failure type, whereas here
        # there is nobody to answer — every case leads to the same action, namely
        # "write the failure onto the job sheet". The specific error type is
        # still recorded in error_code, so no information is lost.
        except (ModelGatewayError, UnsupportedModelProviderError) as exc:
            mark_ai_run_failed(
                session,
                run,
                error_code=exc.__class__.__name__,   # the short, stable type name, safe to
                                                     # group and count in dashboards
                error_message=str(exc),              # the full detail, for a human debugging.
                                                     # Note this is stored in the database, not
                                                     # sent to the browser, so it can afford to
                                                     # be more revealing than an API error
            )
            session.commit()
            record_ai_analysis_failed(
                provider=settings.model_provider,
                mode="async",
                error_code=exc.__class__.__name__,
            )
            logger.warning(
                "ai_analysis_failed",
                extra={
                    "model_provider": settings.model_provider,
                    "error_code": exc.__class__.__name__,
                },
            )
            # Again: returns rather than raises. The failure is fully recorded
            # where the user will see it, so there is nothing to be gained by
            # also making RQ treat the job as crashed.
            return run


# ===========================================================================
# HELPERS
# ===========================================================================


# Bundles three things into the "extracted fields" bag stored with the result:
#   1. whatever the AI itself pulled out of the ticket
#   2. the ID of the job that produced it
#   3. the baseline's opinion, for comparison
#
# Point 3 is the interesting one. Storing the free classifier's verdict beside
# every paid AI verdict means the comparison data accumulates automatically, on
# real production traffic, with no extra cost. When someone later asks "is the
# AI actually better than keyword matching?", the evidence is already there in
# every row rather than needing a special study.
def _worker_extracted_fields(
    *,                        # all arguments must be named — there are five of them, and
                              # several are strings that would be easy to transpose
    analysis_fields: dict[str, object],
    baseline_category: str,
    baseline_priority: str,
    baseline_confidence: float,
    ai_run_id: str,
) -> dict[str, object]:
    # `dict(...)` makes a COPY rather than using the original. Without it, the
    # lines below would modify the analysis object that the caller still holds
    # and passes to record_ticket_analysis_usage — a quiet, confusing bug.
    fields: dict[str, object] = dict(analysis_fields)
    fields["ai_run_id"] = ai_run_id
    fields["baseline_preview"] = {
        "category": baseline_category,
        "priority": baseline_priority,
        "confidence": baseline_confidence,
    }
    return fields


# One readable sentence recording what the keyword rules thought, added to the
# reasons a human reviewer sees.
#
# Written as a plain sentence rather than raw data because that is where it ends
# up: on screen, in front of a support agent deciding whether to trust the
# draft. "Worker baseline comparison classified ticket as billing with high
# priority" is immediately usable; a raw dictionary would not be.
def _baseline_reason(category: str, priority: str) -> str:
    return f"Worker baseline comparison classified ticket as {category} with {priority} priority."
