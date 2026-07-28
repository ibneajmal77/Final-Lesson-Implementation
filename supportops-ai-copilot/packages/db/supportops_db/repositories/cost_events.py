# ============================================================================
# FILE: packages/db/supportops_db/repositories/cost_events.py
#
# THINK OF THIS FILE AS: the accounts ledger for AI spending — writing down what
# each call cost, and adding it all up afterwards.
#
# TWO HALVES:
#   Top    - create_cost_event: record one AI call's tokens, money, and speed
#   Bottom - get_tenant_cost_metrics: total it up, sliced by provider and model
#
# WHY THIS EXISTS AT ALL:
#   AI services charge per token, and tokens are invisible. Without recording
#   them yourself, the first you know about a runaway cost is the monthly
#   invoice. Writing a row per call turns "how much is this feature costing us?"
#   into a query rather than a guess — and, combined with the approval figures,
#   turns it into "what does each USEFUL draft cost?", which is the question
#   that actually decides whether the feature survives.
#
# THE NUMBER THIS FILE EXISTS TO PRODUCE: cost_per_accepted_draft.
#   Total money spent, divided by the number of drafts humans actually accepted.
#   Rejected drafts still cost money but produced nothing, so dividing by
#   accepted drafts — rather than by all drafts — is the honest figure. If it
#   exceeds what a human costs to write the reply themselves, the AI is not
#   paying for itself.
#
# WHO CALLS THESE:
#   packages/observability/model_usage.py - writes the events
#   routes/metrics.py                     - reads the totals for GET /metrics/costs
# ============================================================================

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, cast

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from supportops_db.models import CostEvent, RecommendationReview


# The cost figures for one slice of the data — all events, or one provider, or
# one model. `key` says which.
@dataclass(frozen=True)
class CostMetricBreakdown:
    key: str
    total_events: int
    input_tokens: int             # text sent TO the AI
    output_tokens: int            # text received BACK. Counted separately because it is
                                  # usually charged at several times the input rate, so
                                  # one combined number would hide where the money goes
    estimated_cost_usd: float
    average_latency_ms: float     # sits alongside cost deliberately: the cheapest model is
                                  # no bargain if it is too slow for anyone to wait for


# The complete cost report for one company.
@dataclass(frozen=True)
class TenantCostMetrics:
    total_events: int
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float
    average_latency_ms: float
    accepted_drafts: int              # from the REVIEWS table, not the cost table
    cost_per_accepted_draft: float    # the value-for-money figure
    by_provider: list[CostMetricBreakdown]
    by_model: list[CostMetricBreakdown]


# Records what one AI call cost.
#
# THE INTERESTING PART IS THE max(...) CALLS. Every number is floored at zero
# before storage. That is not paranoia about our own arithmetic — it is defence
# against the AI provider's response. Token counts come from an outside service,
# and a bug or an odd edge case there could yield a negative or missing value.
#
# A single negative row would be quietly poisonous: it would SUBTRACT from the
# totals, making the whole feature look cheaper than it really is. Nobody
# investigates a cost report that looks pleasingly low. Clamping at zero means
# the worst case is understating one call, rather than corrupting every total
# derived from it.
def create_cost_event(
    session: Session,
    *,
    tenant_id: str,               # required: costs must always be attributable to a company
    provider: str,
    model: str,
    operation: str,               # "sync_ticket_analysis" / "async_ticket_analysis"
    input_tokens: int,
    output_tokens: int,
    estimated_cost_usd: float,
    latency_ms: int,
    # The links below are all optional, because not every call has all of them:
    # the synchronous path has no job sheet, and a failed call produced no
    # recommendation. The cost is still recorded either way — money spent is
    # money spent.
    ticket_id: str | None = None,
    ai_run_id: str | None = None,
    recommendation_id: str | None = None,
    prompt_version: str | None = None,
    metadata: dict[str, object] | None = None,
) -> CostEvent:
    event = CostEvent(
        tenant_id=tenant_id,
        ticket_id=ticket_id,
        ai_run_id=ai_run_id,
        recommendation_id=recommendation_id,
        provider=provider,
        model=model,
        prompt_version=prompt_version,
        operation=operation,
        input_tokens=max(input_tokens, 0),                  # never below zero
        output_tokens=max(output_tokens, 0),
        estimated_cost_usd=max(estimated_cost_usd, 0.0),
        latency_ms=max(latency_ms, 0),
        metadata_json=metadata or {},     # `or {}` turns a missing value into an empty
                                          # dictionary, since the column cannot be null
    )
    session.add(event)
    session.flush()
    return event


# Every cost recorded for one analysis job, oldest first.
#
# Note `.asc()` — oldest first, the opposite of every other listing in the
# project. Deliberate: this reads as a sequence of steps in one job, and a
# sequence makes sense in the order it happened. The other listings show "most
# recent activity", where newest-first is what a reader wants.
#
# Note also there is NO tenant filter. Like get_ai_run_by_id, this is internal
# plumbing keyed by an ID the caller already holds, not a user-facing lookup.
def list_cost_events_for_ai_run(session: Session, *, ai_run_id: str) -> list[CostEvent]:
    return list(
        session.scalars(
            select(CostEvent)
            .where(CostEvent.ai_run_id == ai_run_id)
            .order_by(CostEvent.created_at.asc())
        )
    )


# The entry point for the cost report. Runs four queries and assembles them.
def get_tenant_cost_metrics(session: Session, *, tenant_id: str) -> TenantCostMetrics:
    overall = _overall_breakdown(session, tenant_id=tenant_id)
    accepted_drafts = _accepted_draft_count(session, tenant_id=tenant_id)
    return TenantCostMetrics(
        total_events=overall.total_events,
        input_tokens=overall.input_tokens,
        output_tokens=overall.output_tokens,
        estimated_cost_usd=overall.estimated_cost_usd,
        average_latency_ms=overall.average_latency_ms,
        accepted_drafts=accepted_drafts,
        # THE HEADLINE CALCULATION: money spent divided by useful output.
        # Note the two numbers come from entirely different tables — cost from
        # cost_events, acceptances from recommendation_reviews. Joining spending
        # to human judgement is what makes this figure meaningful rather than
        # merely descriptive.
        cost_per_accepted_draft=_ratio(overall.estimated_cost_usd, accepted_drafts),
        by_provider=_grouped_breakdowns(
            session,
            tenant_id=tenant_id,
            group_field=CostEvent.provider,
        ),
        by_model=_grouped_breakdowns(
            session,
            tenant_id=tenant_id,
            group_field=CostEvent.model,
        ),
    )


# The overall totals: one row of five numbers, computed entirely by the database.
def _overall_breakdown(session: Session, *, tenant_id: str) -> CostMetricBreakdown:
    row = session.execute(
        select(
            func.count(),                                              # how many calls
            func.coalesce(func.sum(CostEvent.input_tokens), 0),        # total tokens in
            func.coalesce(func.sum(CostEvent.output_tokens), 0),       # total tokens out
            func.coalesce(func.sum(CostEvent.estimated_cost_usd), 0.0),  # total money
            func.coalesce(func.avg(CostEvent.latency_ms), 0.0),        # typical speed
        ).where(CostEvent.tenant_id == tenant_id)
        # `coalesce(x, 0)` means "use x, but if it is NULL, use 0 instead". Needed
        # because SUM and AVG over ZERO rows return NULL in SQL, not 0 — so on a
        # brand-new company, without this, the report would come back full of
        # nulls and the arithmetic above would fail. This is the database-side
        # twin of the `or 0` guards in the Python code.
    ).one()      # `.one()` insists on exactly one row, which aggregates always produce.
                 # It fails loudly if that assumption is ever wrong, rather than
                 # silently returning the first of several
    return _breakdown_from_row("all", tuple(row))


# The same five numbers, but grouped by provider or by model.
#
# Same reusable-column trick as in metrics.py: the caller passes the column to
# group by, so one function serves both slices.
def _grouped_breakdowns(
    session: Session,
    *,
    tenant_id: str,
    group_field: Any,
) -> list[CostMetricBreakdown]:
    rows = session.execute(
        select(
            group_field,          # the extra first column: which provider/model this row is
            func.count(),
            func.coalesce(func.sum(CostEvent.input_tokens), 0),
            func.coalesce(func.sum(CostEvent.output_tokens), 0),
            func.coalesce(func.sum(CostEvent.estimated_cost_usd), 0.0),
            func.coalesce(func.avg(CostEvent.latency_ms), 0.0),
        )
        .where(CostEvent.tenant_id == tenant_id)
        .group_by(group_field)
        .order_by(group_field)     # stable ordering, so repeated calls agree
    ).all()
    # `tuple(row)[1:]` drops the first column — the grouping key — because it is
    # passed separately as the `key` argument, leaving the five numbers the
    # helper expects.
    return [_breakdown_from_row(str(row[0]), tuple(row)[1:]) for row in rows]


# Counts approved drafts — the denominator of the value-for-money figure.
#
# Only "approved" counts. Edited drafts are deliberately excluded, which is a
# judgement worth noticing: an edited draft did provide some value, so this is
# the STRICTER reading. Erring toward making the AI look expensive rather than
# cheap is the safer direction for a number used to justify continued spending.
def _accepted_draft_count(session: Session, *, tenant_id: str) -> int:
    accepted = session.scalar(
        select(func.count()).where(
            RecommendationReview.tenant_id == tenant_id,
            RecommendationReview.decision == "approved",
        )
    )
    return int(accepted or 0)


# Turns one database row of five values into a typed object.
#
# The line below is "tuple unpacking": five names on the left, one row of five
# values on the right, assigned in order. Compact, but it means the ORDER of
# columns in the two queries above must exactly match the order here. Change one
# without the other and the figures silently swap places — a bug that produces
# plausible-looking wrong numbers rather than an error.
def _breakdown_from_row(key: str, row: Sequence[object]) -> CostMetricBreakdown:
    total_events, input_tokens, output_tokens, estimated_cost_usd, average_latency_ms = row
    return CostMetricBreakdown(
        key=key,
        # `cast(Any, x)` is a note to the type checker only — it produces no code
        # and changes nothing at runtime. Needed because the database returns
        # loosely-typed values and the checker cannot know they are numbers.
        total_events=int(cast(Any, total_events) or 0),
        input_tokens=int(cast(Any, input_tokens) or 0),
        output_tokens=int(cast(Any, output_tokens) or 0),
        # Rounded to EIGHT decimal places, unusually many. Justified: individual
        # AI calls can cost fractions of a cent, so rounding to the usual two
        # would record almost every call as $0.00 and the totals would all be
        # zero. Eight places keeps the small numbers meaningful while trimming
        # the long floating-point tails that would otherwise differ between
        # machines and break test comparisons.
        estimated_cost_usd=round(float(cast(Any, estimated_cost_usd) or 0.0), 8),
        average_latency_ms=round(float(cast(Any, average_latency_ms) or 0.0), 4),
    )


# Divides safely.
#
# The zero check is the whole reason this exists. On day one there are no
# approved drafts, and dividing by zero would crash the cost report precisely
# when someone first opens it. Returning 0.0 reads honestly as "nothing yet".
def _ratio(numerator: float, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 8)
