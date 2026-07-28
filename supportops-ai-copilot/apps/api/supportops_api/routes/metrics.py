# ============================================================================
# FILE: apps/api/supportops_api/routes/metrics.py
#
# THINK OF THIS FILE AS: the scoreboard — "is this AI actually any good, and
# what is it costing us?"
#
# Everything else in the app DOES things. This file only reports on what was
# done. Nothing here writes to the database; every endpoint is read-only.
#
# THE FOUR QUESTIONS IT ANSWERS:
#
#   GET /metrics/reviews  - Quality. Of all the drafts the AI wrote, how many
#                           did humans approve, edit, or throw away? The
#                           approval rate is the headline number of the whole
#                           product. Fed by routes/approvals.py.
#
#   GET /metrics/pilot    - The rollout verdict. Narrower than /reviews: it
#                           looks only at the ticket types in the pilot, and
#                           ends with an actual recommendation — widen the
#                           rollout, hold, or stop. See docs/pilot-report.md.
#
#   GET /metrics/pilot/feedback
#                         - The "how do we improve it?" view. Lists specific
#                           drafts humans rejected or heavily edited, so you can
#                           read them and work out what went wrong. Described
#                           in docs/feedback-to-eval-loop.md.
#
#   GET /metrics/costs    - Money. Tokens used and dollars spent, broken down
#                           by AI provider and model. Fed by the cost records
#                           written during each AI call.
#
#   GET /metrics/runtime  - A different beast entirely; see its note below.
#
# THE NUMBER THAT MATTERS MOST:
#   cost_per_accepted_draft, which appears in both /pilot and /costs. Total
#   money spent divided by the number of drafts humans actually accepted.
#   Drafts that got rejected still cost money but produced nothing, so this is
#   the honest measure of value. If it exceeds what a human costs to write the
#   reply themselves, the feature is not worth running.
#
# WHERE THE REAL WORK HAPPENS:
#   Not here. The counting and averaging is all SQL, living in
#   packages/db/supportops_db/repositories/{metrics,cost_events,pilot}.py.
#   This file only calls those and reshapes the answers into JSON.
# ============================================================================

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from supportops_api.dependencies import Actor, get_current_actor, get_db_session
from supportops_api.pilot import parse_csv_setting  # reused to read the pilot category list
from supportops_api.schemas.metrics import (
    CostMetricBreakdownRead,
    PilotFeedbackCandidateRead,
    PilotFeedbackReportRead,
    PilotRejectionReasonRead,
    ReviewMetricBreakdownRead,
    TenantCostMetricsRead,
    TenantPilotMetricsRead,
    TenantReviewMetricsRead,
)
from supportops_api.settings import Settings, get_settings
from supportops_db.repositories.cost_events import (
    CostMetricBreakdown,
    get_tenant_cost_metrics,
)
from supportops_db.repositories.metrics import ReviewDecisionCounts, get_tenant_review_metrics
from supportops_db.repositories.pilot import (
    PilotFeedbackCandidate,
    PilotRejectionReason,
    get_tenant_pilot_feedback_report,
    get_tenant_pilot_metrics,
)
from supportops_db.repositories.tenants import get_tenant
from supportops_observability.metrics import render_prometheus_metrics

router = APIRouter(prefix="/metrics", tags=["metrics"])

ActorDep = Annotated[Actor, Depends(get_current_actor)]
SessionDep = Annotated[Session, Depends(get_db_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]

# The exact content type Prometheus expects. Prometheus is the monitoring tool
# that scrapes numbers out of running services (see infra/prometheus/). It
# refuses to parse a response unless this header matches precisely, version
# number and all — hence the odd-looking string.
PROMETHEUS_CONTENT_TYPE = "text/plain; version=0.0.4; charset=utf-8"


# ---------------------------------------------------------------------------
# QUALITY: how often do humans accept what the AI wrote?
# ---------------------------------------------------------------------------
@router.get("/reviews", response_model=TenantReviewMetricsRead)
def get_review_metrics_endpoint(
    actor: ActorDep,
    session: SessionDep,
) -> TenantReviewMetricsRead:
    _require_tenant(session, actor.tenant_id)

    # One database call does all the counting; this function just relabels it.
    metrics = get_tenant_review_metrics(session, tenant_id=actor.tenant_id)
    overall = _breakdown_to_read(metrics.overall)
    return TenantReviewMetricsRead(
        tenant_id=actor.tenant_id,
        total_recommendations=metrics.total_recommendations,      # drafts the AI produced
        reviewed_recommendations=metrics.reviewed_recommendations,  # drafts a human looked at

        # A number that is easy to overlook but vital when reading the rest:
        # what fraction of drafts were reviewed at all. If only 5% were looked
        # at, a 90% approval rate means very little — it is 90% of a tiny,
        # possibly unrepresentative sample.
        review_coverage_rate=_rate(
            metrics.reviewed_recommendations,
            metrics.total_recommendations,
        ),

        # The headline figures, flattened out of `overall` so callers don't have
        # to dig into a nested object for the numbers they want most.
        total_reviews=overall.total_reviews,
        approved=overall.approved,
        rejected=overall.rejected,
        edited=overall.edited,
        approval_rate=overall.approval_rate,
        rejection_rate=overall.rejection_rate,
        edit_rate=overall.edit_rate,

        # The same figures sliced two ways, which is where the useful detail
        # lives. An overall 80% approval rate can hide the AI being excellent at
        # password resets and useless at billing — only the breakdowns show that.
        by_source=[_breakdown_to_read(item) for item in metrics.by_source],       # baseline vs AI
        by_category=[_breakdown_to_read(item) for item in metrics.by_category],   # by ticket type
    )


# ---------------------------------------------------------------------------
# THE ROLLOUT VERDICT: should the pilot widen, hold, or stop?
#
# The richest endpoint here. It answers with numbers AND with a recommendation.
# ---------------------------------------------------------------------------
@router.get("/pilot", response_model=TenantPilotMetricsRead)
def get_pilot_metrics_endpoint(
    actor: ActorDep,
    session: SessionDep,
    settings: SettingsDep,
) -> TenantPilotMetricsRead:
    _require_tenant(session, actor.tenant_id)

    # Which ticket types count as "in the pilot" comes from the same setting
    # pilot.py uses to decide whether the AI may run. Reading it from one place
    # keeps the measurement honest — you are always scoring exactly the tickets
    # the AI was actually allowed to touch.
    pilot_categories = _pilot_categories(settings)
    metrics = get_tenant_pilot_metrics(
        session,
        tenant_id=actor.tenant_id,
        pilot_categories=pilot_categories,
    )
    return TenantPilotMetricsRead(
        tenant_id=actor.tenant_id,
        pilot_categories=metrics.pilot_categories,
        reviewed_drafts=metrics.reviewed_drafts,
        accepted_drafts=metrics.accepted_drafts,
        rejected_drafts=metrics.rejected_drafts,
        edited_drafts=metrics.edited_drafts,
        draft_acceptance_rate=metrics.draft_acceptance_rate,

        # How MUCH humans changed the text, not just whether they changed it.
        # "Edit distance" counts the individual character changes needed to turn
        # the AI's draft into the final version. A tiny distance means a typo
        # fix — basically a success. A huge one means the human rewrote it from
        # scratch and only nominally "edited" it.
        average_edit_distance=metrics.average_edit_distance,

        # How long the customer waited for a first reply. The business reason
        # the whole product exists: if this doesn't fall, the AI isn't helping,
        # however good its drafts read.
        average_time_to_first_response_seconds=metrics.average_time_to_first_response_seconds,

        # Did the AI correctly spot the tickets needing a human specialist?
        # Judged separately because the two ways of being wrong are not equally
        # bad: needlessly escalating an easy ticket wastes a little time, while
        # failing to escalate an urgent one can genuinely harm a customer.
        escalation_accuracy=metrics.escalation_accuracy,
        escalated_reviewed_drafts=metrics.escalated_reviewed_drafts,

        cost_per_accepted_draft=metrics.cost_per_accepted_draft,   # the value-for-money figure

        # Count of drafts that broke a safety rule. This one is expected to be
        # zero. Any non-zero value is a stop-the-rollout signal regardless of
        # how good every other number looks.
        safety_failures=metrics.safety_failures,

        # The humans' own words about why they rejected drafts, grouped so the
        # common complaints stand out.
        agent_rejection_reasons=[
            _pilot_rejection_reason_to_read(reason)
            for reason in metrics.agent_rejection_reasons
        ],

        # The computed verdict, e.g. "expand" / "hold" / "rollback", plus the
        # reasoning. Deciding it in code rather than by eye means the criteria
        # were fixed in advance, which stops the outcome being argued into
        # whatever people hoped for.
        exit_decision=metrics.exit_decision,
        exit_reason=metrics.exit_reason,
    )


# ---------------------------------------------------------------------------
# THE IMPROVEMENT LOOP: which specific drafts went wrong, and why?
#
# The others give aggregate numbers, which tell you THAT something is wrong.
# This one hands back individual examples, which tell you WHAT is wrong — the
# drafts humans rejected or rewrote heavily, with the before and after text
# side by side. Those examples become new test cases for packages/evals/, so a
# fix can be proven rather than hoped for.
# ---------------------------------------------------------------------------
@router.get("/pilot/feedback", response_model=PilotFeedbackReportRead)
def get_pilot_feedback_endpoint(
    actor: ActorDep,
    session: SessionDep,
    settings: SettingsDep,
) -> PilotFeedbackReportRead:
    _require_tenant(session, actor.tenant_id)

    pilot_categories = _pilot_categories(settings)
    report = get_tenant_pilot_feedback_report(
        session,
        tenant_id=actor.tenant_id,
        pilot_categories=pilot_categories,
    )
    return PilotFeedbackReportRead(
        tenant_id=actor.tenant_id,
        pilot_categories=pilot_categories,
        candidates=[            # the individual problem drafts, worth reading one by one
            _pilot_feedback_candidate_to_read(candidate)
            for candidate in report.candidates
        ],
        reason_clusters=[       # the same complaints grouped, so patterns surface
            _pilot_rejection_reason_to_read(reason) for reason in report.reason_clusters
        ],
        recommended_next_step=report.recommended_next_step,   # e.g. "revise the prompt template"
    )

# ---------------------------------------------------------------------------
# MONEY: tokens used and dollars spent.
#
# Reads the cost records written during every AI call by
# record_ticket_analysis_usage (see routes/tickets.py and the worker).
# ---------------------------------------------------------------------------
@router.get("/costs", response_model=TenantCostMetricsRead)
def get_cost_metrics_endpoint(
    actor: ActorDep,
    session: SessionDep,
) -> TenantCostMetricsRead:
    _require_tenant(session, actor.tenant_id)

    metrics = get_tenant_cost_metrics(session, tenant_id=actor.tenant_id)
    return TenantCostMetricsRead(
        tenant_id=actor.tenant_id,
        total_events=metrics.total_events,          # how many AI calls were made
        input_tokens=metrics.input_tokens,          # text sent TO the AI
        output_tokens=metrics.output_tokens,        # text received BACK (usually priced higher)
        estimated_cost_usd=metrics.estimated_cost_usd,   # "estimated" because it is computed from
                                                         # our own price settings, not from an
                                                         # actual invoice — treat as a close guide
        average_latency_ms=metrics.average_latency_ms,   # typical wait for an AI answer
        accepted_drafts=metrics.accepted_drafts,
        cost_per_accepted_draft=metrics.cost_per_accepted_draft,

        # Split by provider and by model, which is what makes cost decisions
        # possible: if a cheaper model shows a similar approval rate in
        # /metrics/reviews, switching to it is free money.
        by_provider=[_cost_breakdown_to_read(item) for item in metrics.by_provider],
        by_model=[_cost_breakdown_to_read(item) for item in metrics.by_model],
    )


# ---------------------------------------------------------------------------
# THE ODD ONE OUT: live counters for the monitoring system.
#
# Different from every other endpoint in this file, in three ways:
#
#   1. NO LOGIN REQUIRED. No `actor` argument, so anyone who can reach it can
#      read it. That is normal for this kind of endpoint — Prometheus has no
#      user account — and it is why the port it sits on must not be exposed to
#      the internet. The numbers here are app-wide totals, with no ticket text
#      and no customer data.
#
#   2. NOT JSON. It returns Prometheus's own plain-text format, which is why the
#      content type is set by hand.
#
#   3. NOT FROM THE DATABASE. These counters live in this process's memory, put
#      there by all the record_* calls scattered through the app. They reset to
#      zero whenever the app restarts — fine, because Prometheus scrapes them
#      every few seconds and keeps the history itself.
#
# "include_in_schema=False" hides it from the automatic API docs page, since it
# is plumbing for machines rather than part of the product's API.
#
# The flow: this endpoint -> infra/prometheus/prometheus.yml scrapes it every
# few seconds -> Grafana (infra/grafana/) draws the graphs.
# ---------------------------------------------------------------------------
@router.get("/runtime", include_in_schema=False)
def get_runtime_metrics_endpoint() -> Response:
    return Response(
        content=render_prometheus_metrics(),
        media_type=PROMETHEUS_CONTENT_TYPE,
    )


# ===========================================================================
# HELPERS
# ===========================================================================


# Reads the pilot ticket types from settings, tidied and sorted.
# Sorted purely so the output is stable — the same list always appears in the
# same order, which keeps API responses and test comparisons predictable.
def _pilot_categories(settings: Settings) -> list[str]:
    return sorted(parse_csv_setting(settings.ai_analysis_enabled_categories))


# The next few functions all do the same small job: take an object from the
# database layer and rebuild it as the matching outgoing-JSON object. Tedious,
# but it is what keeps the public API shape independent of internal structures.
def _pilot_rejection_reason_to_read(reason: PilotRejectionReason) -> PilotRejectionReasonRead:
    return PilotRejectionReasonRead(reason=reason.reason, count=reason.count)


def _pilot_feedback_candidate_to_read(
    candidate: PilotFeedbackCandidate,
) -> PilotFeedbackCandidateRead:
    return PilotFeedbackCandidateRead(
        ticket_id=candidate.ticket_id,
        recommendation_id=candidate.recommendation_id,
        review_id=candidate.review_id,
        category=candidate.category,
        decision=candidate.decision,
        notes=candidate.notes,                    # the reviewer's own explanation
        edit_distance=candidate.edit_distance,    # how heavily it was rewritten
        suggested_reply=candidate.suggested_reply,  # what the AI wrote...
        final_reply=candidate.final_reply,          # ...and what the human actually sent.
                                                    # Comparing these two is the whole point
        # Converted to text here (e.g. "2026-07-21T14:30:00"). ISO format is the
        # international standard, so it sorts correctly as plain text and is
        # understood by every language without ambiguity about day/month order.
        created_at=candidate.created_at.isoformat(),
    )

# The same tenant check as the other route files.
def _require_tenant(session: Session, tenant_id: str) -> None:
    if not get_tenant(session, tenant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tenant not found")


# Turns raw counts into counts PLUS percentages.
#
# The database layer deliberately returns only whole counts; the rates are
# worked out here. That division of labour is on purpose — counts are facts
# that can be summed and re-sliced, while rates are a presentation choice, and
# rates cannot be meaningfully averaged together later.
def _breakdown_to_read(counts: ReviewDecisionCounts) -> ReviewMetricBreakdownRead:
    return ReviewMetricBreakdownRead(
        key=counts.key,        # what this row is about: a source name, or a category name
        total_reviews=counts.total_reviews,
        approved=counts.approved,
        rejected=counts.rejected,
        edited=counts.edited,
        approval_rate=_rate(counts.approved, counts.total_reviews),
        rejection_rate=_rate(counts.rejected, counts.total_reviews),
        edit_rate=_rate(counts.edited, counts.total_reviews),
    )


# Same idea for the cost figures. No rates to compute here — the averages were
# already worked out in SQL, since averaging correctly needs every row, and by
# this point we only have the summary.
def _cost_breakdown_to_read(counts: CostMetricBreakdown) -> CostMetricBreakdownRead:
    return CostMetricBreakdownRead(
        key=counts.key,          # a provider name, or a model name
        total_events=counts.total_events,
        input_tokens=counts.input_tokens,
        output_tokens=counts.output_tokens,
        estimated_cost_usd=counts.estimated_cost_usd,
        average_latency_ms=counts.average_latency_ms,
    )


# Works out a fraction, safely.
#
# The `if denominator == 0` guard is the entire reason this exists. On day one
# there are no reviews at all, and dividing by zero would crash the endpoint —
# so the metrics page would break precisely when someone first opens it. It
# returns 0.0 instead, which reads honestly as "nothing yet".
#
# Rounded to 4 decimal places, so 0.8333333333333334 becomes 0.8333 (83.33%).
# Far enough for a percentage, and it avoids long floating-point tails in the
# JSON that would differ slightly between machines and break test comparisons.
def _rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)
