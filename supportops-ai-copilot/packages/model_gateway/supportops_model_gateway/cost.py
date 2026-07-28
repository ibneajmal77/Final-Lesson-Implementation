# ============================================================================
# FILE: packages/model_gateway/supportops_model_gateway/cost.py
#
# THINK OF THIS FILE AS: the price calculator. Tokens in, dollars out.
#
# HOW AI BILLING WORKS, briefly:
#   AI services charge by the TOKEN — roughly three-quarters of a word. Prices
#   are quoted per 1,000 tokens, and input (what you send) is charged at a
#   different, usually much lower, rate than output (what comes back). A model
#   might cost $0.03 per 1,000 input tokens and $0.06 per 1,000 output tokens.
#
#   So: (tokens / 1000) x rate, done separately for each direction, then added.
#   That is the entire calculation below.
#
# WHY THIS IS ITS OWN FILE FOR ONE SMALL SUM:
#   Because the sum is repeated in several places — both AI paths and the
#   evaluation harness — and a cost calculation that disagrees with itself
#   between code paths is worse than no calculation at all. One implementation,
#   used everywhere, keeps the reports internally consistent.
#
# WHERE THE PRICES COME FROM: settings.py, as model_input_cost_per_1k_tokens and
# model_output_cost_per_1k_tokens. They default to 0.0, because the mock
# provider is free.
#
# WHO CALLS IT: packages/observability/model_usage.py, which then writes the
# result into the cost_events table.
# ============================================================================

from dataclasses import dataclass


# The answer: tokens counted, and the money they came to.
#
# The token counts are returned alongside the cost, rather than only the cost,
# on purpose. Prices change; token counts do not. Storing both means a later
# price correction can be applied to historical data by recalculating, instead
# of leaving the old figures permanently wrong.
@dataclass(frozen=True)
class ModelUsageCost:
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0


# Works out what one AI call cost.
#
# THE FOUR max(...) CALLS ARE THE INTERESTING PART. Every input is floored at
# zero before use, and each guards against a different bad input:
#
#   Token counts come from the AI PROVIDER'S response — an outside system we do
#   not control. A bug or an odd edge case there could yield a negative or absent
#   value.
#
#   Rates come from OUR OWN environment variables, which anyone can set. A typo
#   producing "-0.03" is entirely possible.
#
# Why it matters so much: a single negative value would SUBTRACT from the running
# totals, making the whole feature look cheaper than it is. Nobody investigates a
# cost report that looks pleasingly low, so the error could persist for months.
# Clamping means the worst case is understating one call rather than corrupting
# every total derived from it.
def estimate_model_usage_cost(
    *,                        # all arguments named. Four numbers in a row — two token
                              # counts and two rates — would otherwise be trivially easy
                              # to transpose, and the result would still look plausible
    input_tokens: int,
    output_tokens: int,
    input_cost_per_1k_tokens: float = 0.0,
    output_cost_per_1k_tokens: float = 0.0,
) -> ModelUsageCost:
    safe_input_tokens = max(input_tokens, 0)
    safe_output_tokens = max(output_tokens, 0)
    safe_input_rate = max(input_cost_per_1k_tokens, 0.0)
    safe_output_rate = max(output_cost_per_1k_tokens, 0.0)

    # The calculation itself: each direction priced separately, then summed.
    # Note the division by 1000 happens BEFORE multiplying by the rate, matching
    # how prices are quoted ("per 1,000 tokens").
    estimated_cost = (safe_input_tokens / 1000 * safe_input_rate) + (
        safe_output_tokens / 1000 * safe_output_rate
    )

    return ModelUsageCost(
        input_tokens=safe_input_tokens,
        output_tokens=safe_output_tokens,
        # Rounded to EIGHT decimal places, which looks excessive until you do the
        # arithmetic: a short ticket analysis might use 500 input tokens at
        # $0.03/1k, costing $0.000015. Round that to the usual two places and it
        # becomes $0.00 — every call free, every total zero, the entire cost
        # report useless.
        #
        # Eight places keeps small amounts meaningful while trimming the long
        # floating-point tails (0.000015000000000000002) that would otherwise
        # differ slightly between machines and break test comparisons.
        estimated_cost_usd=round(estimated_cost, 8),
    )
