# ============================================================================
# FILE: tests/model_gateway/test_cost.py
#
# WHAT THIS TESTS: the price calculator in
# packages/model_gateway/supportops_model_gateway/cost.py — tokens in, dollars
# out.
#
# TWO TESTS, and they cover the two things that can go wrong with a calculation
# like this: getting the arithmetic wrong, and getting bad input.
#
# WHY A TWO-LINE SUM DESERVES ITS OWN TESTS: because the output is MONEY, and
# money that is quietly wrong is the worst kind of wrong. A cost report showing
# half the true figure looks entirely plausible, so nobody investigates — and the
# error surfaces months later as a surprising invoice. There is no natural
# feedback loop to catch it, which is exactly when automated tests earn their
# place.
# ============================================================================

from supportops_model_gateway.cost import estimate_model_usage_cost


# Does the arithmetic actually work?
#
# The numbers are chosen so the expected result can be verified by hand, which is
# the point — a test asserting a value you cannot check yourself proves nothing.
#
#   input:  1500 tokens / 1000 x $0.01 = $0.015
#   output:  250 tokens / 1000 x $0.03 = $0.0075
#   total:                               $0.0225
#
# Note the input and output rates DIFFER (0.01 against 0.03), which is what makes
# this test meaningful: a bug that applied the input rate to both, or summed the
# tokens before pricing them, would produce a different total and be caught. With
# equal rates, both bugs would slip through.
def test_estimate_model_usage_cost_uses_configured_per_1k_rates() -> None:
    usage_cost = estimate_model_usage_cost(
        input_tokens=1500,
        output_tokens=250,
        input_cost_per_1k_tokens=0.01,
        output_cost_per_1k_tokens=0.03,
    )

    # The token counts pass through unchanged. Worth asserting: they are stored
    # alongside the cost precisely so a later price correction can be applied by
    # recalculating, rather than leaving historical figures permanently wrong.
    assert usage_cost.input_tokens == 1500
    assert usage_cost.output_tokens == 250
    assert usage_cost.estimated_cost_usd == 0.0225


# THE DEFENSIVE TEST, and the more interesting of the two.
#
# It feeds in negative values for all four arguments and confirms everything is
# floored at zero.
#
# WHY THAT MATTERS SO MUCH: a negative cost would SUBTRACT from the running
# totals, making the whole AI feature look cheaper than it is. Nobody investigates
# a cost report that looks pleasingly low, so the error could persist for months.
#
# And negative values are not hypothetical. Token counts come from the AI
# provider's response — an outside system we do not control — and the rates come
# from environment variables, where a typo producing "-0.03" is entirely
# possible. This test locks in the max(..., 0) guards in cost.py that make the
# worst case "one call understated" rather than "every total corrupted".
def test_estimate_model_usage_cost_clamps_negative_values() -> None:
    usage_cost = estimate_model_usage_cost(
        input_tokens=-10,
        output_tokens=-20,
        input_cost_per_1k_tokens=-1,
        output_cost_per_1k_tokens=-1,
    )

    assert usage_cost.input_tokens == 0
    assert usage_cost.output_tokens == 0
    # Note this would be POSITIVE without the guards: a negative token count
    # multiplied by a negative rate gives a positive cost. So the naive
    # calculation would not merely be wrong, it would silently invent spending
    # that never happened — a good illustration of why clamping both the counts
    # and the rates matters, rather than just one of them.
    assert usage_cost.estimated_cost_usd == 0.0
