# ============================================================================
# FILE: apps/api/supportops_api/schemas/metrics.py
#
# THINK OF THIS FILE AS: the layout of the scoreboard — the exact shape of
# every number returned by the /metrics endpoints.
#
# All of these are output-only. There are no "Create" classes here, because
# nobody submits metrics; they are counted from data the app already holds.
#
# A PATTERN REPEATED THREE TIMES BELOW — "totals plus breakdowns":
#   Each report has a summary class holding the overall figures, which then
#   carries LISTS of smaller "breakdown" classes holding the same figures
#   sliced by one dimension.
#
#   That shape exists because an overall number can lie by averaging. An 80%
#   approval rate can hide the AI being excellent at password resets and useless
#   at billing disputes. Only the breakdown reveals it, and that is usually the
#   difference between "the AI is fine" and "the AI is fine for these two ticket
#   types and should be switched off for the third".
#
# USED BY: routes/metrics.py, which fills these in from the database results.
# ============================================================================

from pydantic import BaseModel

# --- REPORT 1: QUALITY — do humans accept what the AI writes? ---------------

# One slice of the review figures. The same class is reused for slicing by
# source and by category, which is what `key` is for: it holds whatever this
# particular row is about — "baseline", "hosted", "billing", "technical".
#
# One reusable class rather than two nearly identical ones, because the numbers
# are the same either way; only the labelling differs.
class ReviewMetricBreakdownRead(BaseModel):
    key: str
    total_reviews: int
    approved: int
    rejected: int
    edited: int
    # The three rates always add up to 1.0, since every review is exactly one of
    # the three verdicts. Sent as ready-made fractions (0.8333 = 83.33%) so every
    # caller displays the same figure rather than each recomputing it slightly
    # differently. Worked out by _rate() in routes/metrics.py.
    approval_rate: float
    rejection_rate: float
    edit_rate: float


# The full quality report for one company.
class TenantReviewMetricsRead(BaseModel):
    tenant_id: str

    # These three are about COVERAGE, not quality, and they belong first because
    # they tell you how much to trust everything below. If only 20 of 1,000
    # drafts were ever reviewed, the approval rate describes those 20 — and the
    # 980 nobody looked at may be quietly terrible.
    total_recommendations: int        # drafts the AI produced
    reviewed_recommendations: int     # drafts a human actually judged
    review_coverage_rate: float       # the second divided by the first

    # The headline figures. Deliberately flattened to the top level rather than
    # nested inside an "overall" object, because these are what most callers
    # want and they should not have to dig for them.
    total_reviews: int
    approved: int
    rejected: int
    edited: int
    approval_rate: float
    rejection_rate: float
    edit_rate: float

    # The same figures sliced two ways — where the actionable detail lives.
    by_source: list[ReviewMetricBreakdownRead]      # baseline rules vs the AI. This comparison
                                                    # is the one that justifies the AI's cost
    by_category: list[ReviewMetricBreakdownRead]    # by ticket type. This one tells you where
                                                    # to widen or withdraw the rollout


# --- REPORT 2: MONEY — what is the AI costing? -----------------------------

# One slice of the cost figures, sliced by provider or by model.
class CostMetricBreakdownRead(BaseModel):
    key: str                      # a provider name, or a model name
    total_events: int             # how many AI calls
    input_tokens: int             # text sent TO the AI
    output_tokens: int            # text received BACK. Usually charged at a higher rate,
                                  # which is why the two are counted separately
    estimated_cost_usd: float     # "estimated" because it is computed from our own configured
                                  # prices (see settings.py), not read from a real invoice
    average_latency_ms: float     # typical wait for an answer. Sitting alongside cost on
                                  # purpose: the cheapest model is no bargain if it is so slow
                                  # that agents stop waiting for it


# The full cost report for one company.
class TenantCostMetricsRead(BaseModel):
    tenant_id: str
    total_events: int
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float
    average_latency_ms: float

    # The value-for-money calculation, and the most important pair of numbers in
    # this file. Rejected drafts still cost real money but produced nothing
    # usable, so dividing total spend by ACCEPTED drafts — not by all drafts —
    # is the honest figure. If it exceeds what a human costs to write the reply
    # from scratch, the feature is not paying for itself.
    accepted_drafts: int
    cost_per_accepted_draft: float

    # Sliced by provider and model, which is what makes a switching decision
    # possible: if a cheaper model shows a comparable approval rate in the
    # quality report above, moving to it is a straight saving.
    by_provider: list[CostMetricBreakdownRead]
    by_model: list[CostMetricBreakdownRead]

# --- REPORT 3: THE PILOT VERDICT — should the rollout widen or stop? --------

# One grouped rejection reason and how often it came up. Built from the free-text
# notes reviewers wrote when rejecting a draft. Simple, but usually the fastest
# route to understanding what the AI is actually getting wrong.
class PilotRejectionReasonRead(BaseModel):
    reason: str
    count: int


# The pilot scorecard. Broader than the other two reports: it mixes quality,
# speed, cost, and safety, because the decision to widen a rollout depends on
# all four at once — and a failure in any one of them should stop it.
class TenantPilotMetricsRead(BaseModel):
    tenant_id: str
    pilot_categories: list[str]      # which ticket types were in scope for this scoring

    # Quality
    reviewed_drafts: int
    accepted_drafts: int
    rejected_drafts: int
    edited_drafts: int
    draft_acceptance_rate: float

    # HOW MUCH humans changed the text, not merely whether they did. Edit
    # distance counts the individual character changes needed to turn the AI's
    # draft into the sent version. A small number means a typo fix — effectively
    # a success. A large one means a rewrite that was only nominally an "edit",
    # and lumping those in with real edits would flatter the AI considerably.
    average_edit_distance: float

    # Speed — the business reason the product exists. If the customer's wait for
    # a first reply doesn't fall, the AI isn't helping, however well it writes.
    average_time_to_first_response_seconds: float

    # Safety judgement: did the AI correctly spot the tickets needing a human
    # specialist? Scored separately from general accuracy because the two ways of
    # being wrong are not equally bad. Escalating an easy ticket wastes a few
    # minutes; failing to escalate an urgent one can genuinely harm a customer.
    escalation_accuracy: float
    escalated_reviewed_drafts: int

    cost_per_accepted_draft: float

    # Drafts that broke a hard safety rule. This number is expected to be 0. Any
    # other value is a stop signal on its own, regardless of how good every other
    # figure here looks — which is why it is a plain count and not a rate.
    safety_failures: int

    agent_rejection_reasons: list[PilotRejectionReasonRead]

    # The computed verdict — e.g. "expand" / "hold" / "rollback" — and the
    # reasoning behind it. Deciding this in code rather than by eye means the
    # criteria were fixed in advance, which is what stops the conclusion from
    # being argued into whatever people were hoping for.
    exit_decision: str
    exit_reason: str


# --- REPORT 4: THE IMPROVEMENT LOOP — which drafts went wrong, and why? -----

# One specific draft that a human rejected or heavily rewrote.
#
# The other reports give you aggregate numbers, which tell you THAT something is
# wrong. This gives you individual examples, which tell you WHAT is wrong. Each
# one is a candidate to become a permanent test case in packages/evals/, so a
# future fix can be proven rather than assumed.
class PilotFeedbackCandidateRead(BaseModel):
    # All three IDs, so a reader can jump straight to the full records.
    ticket_id: str
    recommendation_id: str
    review_id: str

    category: str
    decision: str          # a plain str here, not the strict ReviewDecision type used in
                           # schemas/approvals.py. A looser choice: this is a read-only
                           # report, so there is no incoming value to police
    notes: str | None      # the reviewer's own words about what was wrong
    edit_distance: int     # how heavily it was rewritten; the biggest numbers are the
                           # most instructive cases to read

    # The heart of it: what the AI wrote, and what the human actually sent.
    # Reading these two side by side is the single most useful thing in the
    # entire metrics system for working out how to improve the prompt.
    suggested_reply: str | None
    final_reply: str | None

    # Note this is `str`, not `datetime`, unlike every other timestamp in the
    # schemas. routes/metrics.py converts it with .isoformat() before it gets
    # here, because this report is built for reading and exporting rather than
    # for further computation.
    created_at: str


# The wrapper holding the examples plus the summarised patterns.
class PilotFeedbackReportRead(BaseModel):
    tenant_id: str
    pilot_categories: list[str]
    candidates: list[PilotFeedbackCandidateRead]       # the individual cases, worth reading
    reason_clusters: list[PilotRejectionReasonRead]    # the same complaints grouped, so
                                                       # recurring themes stand out
    recommended_next_step: str                         # a suggested action, e.g. "revise the
                                                       # prompt template for billing tickets"
