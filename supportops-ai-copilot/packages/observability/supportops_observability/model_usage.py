# ============================================================================
# FILE: packages/observability/supportops_observability/model_usage.py
#
# THINK OF THIS FILE AS: the single place that records "we just made an AI call
# and here is what it cost" — writing it down in BOTH places at once.
#
# THE TWO PLACES, and why both are needed:
#   1. The DATABASE (cost_events table) - permanent, per-customer, survives
#      restarts. Feeds GET /metrics/costs and the pilot report. This is what
#      answers "what did this customer cost us last month?"
#   2. The LIVE COUNTERS (metrics.py) - in memory, scraped by Prometheus every
#      few seconds. This is what answers "is spending spiking RIGHT NOW?"
#
#   Neither substitutes for the other. The database is authoritative but slow to
#   query and awkward to alert on; the counters are instant but reset on restart
#   and hold no per-customer detail.
#
# WHY IT MATTERS THAT THIS IS ONE FUNCTION:
#   Both AI paths call it — routes/tickets.py (synchronous) and
#   apps/worker/jobs.py (queued). If each recorded costs its own way, the two
#   would drift apart, and half the spending would eventually go unrecorded by
#   one of them. One function, called from both, keeps the accounting complete.
#
# WHERE IT SITS: this file is the joint between three packages. It takes a result
# from the model_gateway, prices it with that package's calculator, and writes it
# through the db package's repository. That is why it lives in observability
# rather than in any of them.
# ============================================================================

from sqlalchemy.orm import Session

from supportops_db.models import CostEvent
from supportops_db.repositories.cost_events import create_cost_event
from supportops_model_gateway.cost import estimate_model_usage_cost
from supportops_model_gateway.providers.base import TicketAnalysisResult
from supportops_observability.metrics import record_model_gateway_call


# Records one AI call's usage, everywhere it needs recording.
def record_ticket_analysis_usage(
    session: Session,
    *,
    tenant_id: str,
    ticket_id: str,
    analysis: TicketAnalysisResult,     # what came back from the AI, including token counts
    operation: str,                     # "sync_ticket_analysis" / "async_ticket_analysis"
    input_cost_per_1k_tokens: float,    # prices, from settings.py
    output_cost_per_1k_tokens: float,
    fallback_latency_seconds: float,    # our own stopwatch, used only if needed — see below
    # Optional because they are not always available: the synchronous path has no
    # job sheet, and a failed call produced no recommendation.
    ai_run_id: str | None = None,
    recommendation_id: str | None = None,
) -> CostEvent:
    # STEP 1: work out the money. Tokens x price, done in the model_gateway's
    # cost calculator so the arithmetic lives in exactly one place.
    usage_cost = estimate_model_usage_cost(
        input_tokens=analysis.input_tokens,
        output_tokens=analysis.output_tokens,
        input_cost_per_1k_tokens=input_cost_per_1k_tokens,
        output_cost_per_1k_tokens=output_cost_per_1k_tokens,
    )

    # STEP 2: settle on a duration. See the helper at the bottom for why there
    # are two possible sources.
    latency_ms = _latency_ms(analysis, fallback_latency_seconds=fallback_latency_seconds)

    # STEP 3: write the permanent database record.
    event = create_cost_event(
        session,
        tenant_id=tenant_id,
        ticket_id=ticket_id,
        ai_run_id=ai_run_id,
        recommendation_id=recommendation_id,
        # `analysis.source` is used as the provider, not the configured setting.
        # A meaningful difference: it records what ACTUALLY answered
        # ("openai_responses_v1", "mock_llm_v1") rather than what we asked for,
        # so mock-generated costs can never be mistaken for real ones.
        provider=analysis.source,
        model=analysis.model_name,
        prompt_version=analysis.prompt_version,
        operation=operation,
        input_tokens=usage_cost.input_tokens,      # the CLAMPED values from the
        output_tokens=usage_cost.output_tokens,    # calculator, never the raw ones
        estimated_cost_usd=usage_cost.estimated_cost_usd,
        latency_ms=latency_ms,
        metadata={
            # The provider's own ID for this call. Kept because it is what
            # identifies the request on the vendor's side if you ever need to
            # raise a support case about a bad or overcharged response.
            "raw_response_id": analysis.raw_response_id,
        },
    )

    # STEP 4: bump the live counters.
    #
    # NOTE THIS IS NOT INSIDE A TRANSACTION, and the database write above is.
    # The consequence is a small, deliberate inconsistency: if the caller's
    # transaction is later rolled back, the database row disappears but these
    # in-memory counters keep the increment.
    #
    # Acceptable, because live counters are for spotting trends and spikes, not
    # for accounting. The database remains the authoritative record. Trying to
    # keep the two perfectly in step would mean unwinding counter changes on
    # rollback, which is far more complexity than the benefit justifies.
    record_model_gateway_call(
        provider=analysis.source,
        model=analysis.model_name,
        input_tokens=usage_cost.input_tokens,
        output_tokens=usage_cost.output_tokens,
        estimated_cost_usd=usage_cost.estimated_cost_usd,
        latency_seconds=latency_ms / 1000,    # converted back to seconds: the database
                                              # stores milliseconds, Prometheus convention
                                              # is seconds
    )

    # The created row is returned, though both current callers ignore it. Useful
    # for tests, which assert on what was written.
    return event


# Decides which timing figure to trust.
#
# THERE ARE TWO POSSIBLE SOURCES, and they measure different things:
#   analysis.latency_ms       - reported BY THE AI PROVIDER. Measures their
#                               processing time only.
#   fallback_latency_seconds  - measured by US, wrapping the whole call. Includes
#                               network time to and from them.
#
# The provider's own figure is preferred when available, because it isolates
# their performance from our network conditions — which is the more actionable
# number when deciding whether a model is too slow.
#
# The `> 0` test doubles as the "is it available?" check: TicketAnalysisResult
# defaults latency_ms to 0, and the mock provider never sets it. So zero reliably
# means "not reported" rather than "took no time at all".
#
# `max(..., 0.0)` guards the fallback against a negative value from a clock
# adjustment, which would otherwise be stored as a nonsensical duration.
def _latency_ms(analysis: TicketAnalysisResult, *, fallback_latency_seconds: float) -> int:
    if analysis.latency_ms > 0:
        return analysis.latency_ms
    return int(max(fallback_latency_seconds, 0.0) * 1000)
