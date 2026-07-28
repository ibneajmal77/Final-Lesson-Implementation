# ============================================================================
# FILE: packages/db/supportops_db/repositories/pilot.py
#
# THINK OF THIS FILE AS: the judge that decides whether the AI rollout should
# widen, stay put, or be switched off.
#
# The most opinionated file in the project. The other repositories fetch and
# count; this one applies actual judgement — with thresholds written down in
# code — and produces a verdict.
#
# TWO PUBLIC FUNCTIONS:
#   get_tenant_pilot_metrics        - the scorecard, ending in a verdict
#   get_tenant_pilot_feedback_report - the specific drafts that went wrong,
#                                      so you can read them and improve things
#
# WHY THE VERDICT IS COMPUTED IN CODE RATHER THAN DECIDED IN A MEETING:
#   Because thresholds agreed in advance cannot be argued away afterwards. It is
#   very easy, having spent months building an AI feature, to look at an
#   uninspiring 55% acceptance rate and talk yourself into "that's promising".
#   Writing the rules down first — see _with_exit_decision at the bottom — means
#   the answer is the same whoever asks, and whatever they were hoping for.
#
# UNUSUAL FOR THIS FOLDER: much of the work here happens in PYTHON, not SQL.
#   The other repositories push all counting into the database. This one fetches
#   the rows and processes them in Python, because the calculations — edit
#   distance, keyword clustering, per-ticket earliest response — are not things
#   SQL expresses well. The trade-off is real: it will not scale to millions of
#   reviews. Acceptable for a pilot, which by definition involves modest volumes.
# ============================================================================

from dataclasses import dataclass
from datetime import datetime
from typing import Any, cast

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from supportops_db.models import (
    AIRun,
    CostEvent,
    RecommendationReview,
    Ticket,
    TicketRecommendation,
)

# The source value of the free keyword classifier. Used to EXCLUDE baseline
# results everywhere below — this file scores the AI, and including results the
# AI never produced would corrupt every figure in the report.
AI_BASELINE_SOURCE = "baseline_v1"

# What counts as the AI having been useful.
#
# Note "edited" is included here, unlike in cost_events.py where only "approved"
# counted. A deliberate difference of emphasis: an edited draft DID help — the
# human started from something rather than a blank page. The stricter reading is
# kept for the cost figure, where erring toward "the AI looks expensive" is the
# safer direction. Both are defensible; what matters is knowing which is which.
ACCEPTED_DECISIONS = frozenset({"approved", "edited"})

# Words that, appearing in an error code, mark a failure as safety-related
# rather than merely technical. Used by _safety_failure_count below.
SAFETY_ERROR_MARKERS = ("safety", "prompt", "injection", "evidence")

# The keyword dictionary for sorting reviewers' free-text complaints into themes.
#
# Crude, and worth being honest about: it is keyword matching, so "the tone was
# not rude at all" would be filed under "tone" regardless of meaning, and a
# complaint phrased in words absent from this list falls into "unspecified".
#
# It is nonetheless useful. Reading 200 free-text notes by hand is a task nobody
# does; seeing "incorrect: 47, tone: 12" points you at the real problem in
# seconds. Treat it as a signpost, then read the actual notes.
REJECTION_REASON_KEYWORDS = {
    "tone": ("tone", "rude", "robotic", "empathy"),
    "incorrect": ("wrong", "incorrect", "inaccurate", "not true"),
    "missing_context": ("missing", "incomplete", "context", "policy"),
    "unsafe": ("unsafe", "security", "privacy", "pii"),      # "pii" = personally
                                                             # identifiable information
    "too_long": ("too long", "verbose", "shorter"),
}


# One theme of complaint and how often it appeared.
@dataclass(frozen=True)
class PilotRejectionReason:
    reason: str
    count: int


# The full pilot scorecard.
@dataclass(frozen=True)
class PilotMetrics:
    pilot_categories: list[str]
    reviewed_drafts: int
    accepted_drafts: int
    rejected_drafts: int
    edited_drafts: int
    draft_acceptance_rate: float
    average_edit_distance: float                      # how heavily humans rewrote things
    average_time_to_first_response_seconds: float     # the business benefit
    escalation_accuracy: float                        # did it spot the urgent ones?
    escalated_reviewed_drafts: int
    cost_per_accepted_draft: float
    safety_failures: int                              # expected to be 0
    agent_rejection_reasons: list[PilotRejectionReason]
    exit_decision: str                                # expand / iterate / stop / roll_back
    exit_reason: str


# One specific draft that went wrong, kept for someone to read.
@dataclass(frozen=True)
class PilotFeedbackCandidate:
    ticket_id: str
    recommendation_id: str
    review_id: str
    category: str
    decision: str
    notes: str | None
    edit_distance: int
    suggested_reply: str | None    # what the AI wrote...
    final_reply: str | None        # ...and what the human actually sent. Comparing
                                   # these two is the point of the whole report
    created_at: datetime


@dataclass(frozen=True)
class PilotFeedbackReport:
    candidates: list[PilotFeedbackCandidate]
    reason_clusters: list[PilotRejectionReason]
    recommended_next_step: str


# ---------------------------------------------------------------------------
# PUBLIC FUNCTION 1: the scorecard.
# ---------------------------------------------------------------------------
def get_tenant_pilot_metrics(
    session: Session,
    *,
    tenant_id: str,
    pilot_categories: list[str],
) -> PilotMetrics:
    # One database query fetches everything; all the analysis below is Python.
    rows = _review_rows(session, tenant_id=tenant_id, pilot_categories=pilot_categories)

    reviewed_drafts = len(rows)
    # `sum(1 for ... if ...)` is the compact way to count matching items.
    accepted_drafts = sum(1 for row in rows if row.review.decision in ACCEPTED_DECISIONS)
    rejected_drafts = sum(1 for row in rows if row.review.decision == "rejected")
    edited_drafts = sum(1 for row in rows if row.review.decision == "edited")

    # How much text changed, measured ONLY on edited drafts. Including approvals
    # (always distance 0) and rejections (which have no final text at all) would
    # drag the average toward zero and make heavy rewriting look mild.
    edit_distances = [
        _edit_distance(row.recommendation.suggested_reply or "", row.review.final_reply or "")
        for row in rows
        if row.review.decision == "edited"
    ]

    first_response_seconds = _first_response_seconds(rows)

    # Escalation accuracy, computed only over the drafts that ASKED to be
    # escalated. It answers "when the AI said this needs a specialist, was it
    # right?" — measured by whether the human agreed with that draft.
    #
    # Worth being clear about what this does NOT measure: the tickets the AI
    # should have escalated but didn't. Those are the more dangerous errors, and
    # they are invisible to this calculation, because nothing in the data marks
    # a missed escalation. A known limitation of the metric.
    escalated_rows = [row for row in rows if row.recommendation.requires_escalation]
    accepted_escalations = sum(
        1 for row in escalated_rows if row.review.decision in ACCEPTED_DECISIONS
    )

    estimated_cost = _estimated_cost(
        session,
        tenant_id=tenant_id,
        pilot_categories=pilot_categories,
    )
    rejection_reasons = _cluster_rejection_reasons(
        [row.review.notes for row in rows if row.review.decision == "rejected"]
    )

    metrics = PilotMetrics(
        pilot_categories=pilot_categories,
        reviewed_drafts=reviewed_drafts,
        accepted_drafts=accepted_drafts,
        rejected_drafts=rejected_drafts,
        edited_drafts=edited_drafts,
        draft_acceptance_rate=_ratio(accepted_drafts, reviewed_drafts),
        average_edit_distance=_average(edit_distances),
        average_time_to_first_response_seconds=_average(first_response_seconds),
        escalation_accuracy=_ratio(accepted_escalations, len(escalated_rows)),
        escalated_reviewed_drafts=len(escalated_rows),
        cost_per_accepted_draft=_ratio_float(estimated_cost, accepted_drafts),
        safety_failures=_safety_failure_count(session, tenant_id=tenant_id),
        agent_rejection_reasons=rejection_reasons,
        exit_decision="iterate",     # placeholders, replaced on the next line. The object is
        exit_reason="",              # frozen, so the verdict cannot be filled in afterwards —
                                     # a whole new one is built instead
    )
    return _with_exit_decision(metrics)


# ---------------------------------------------------------------------------
# PUBLIC FUNCTION 2: the specific drafts worth reading.
#
# The scorecard tells you THAT something is wrong. This tells you WHAT.
# ---------------------------------------------------------------------------
def get_tenant_pilot_feedback_report(
    session: Session,
    *,
    tenant_id: str,
    pilot_categories: list[str],
    minimum_edit_distance: int = 25,     # how much rewriting counts as "worth looking at"
    limit: int = 25,                     # a readable number of examples, not an exhaustive dump
) -> PilotFeedbackReport:
    candidates = _feedback_candidates(
        session,
        tenant_id=tenant_id,
        pilot_categories=pilot_categories,
        minimum_edit_distance=minimum_edit_distance,
        limit=limit,
    )
    reason_clusters = _cluster_rejection_reasons([candidate.notes for candidate in candidates])
    # A plain-English suggestion rather than raw data. The intended workflow is
    # explicitly to feed bad drafts back into the evaluation dataset in
    # packages/evals/, so that a future fix can be PROVEN rather than hoped for.
    # See docs/feedback-to-eval-loop.md.
    next_step = (
        "Add representative rejected or heavily edited drafts to the difficult eval dataset."
        if candidates
        else "No feedback candidates yet; keep collecting pilot reviews."
    )
    return PilotFeedbackReport(
        candidates=candidates,
        reason_clusters=reason_clusters,
        recommended_next_step=next_step,
    )


# ===========================================================================
# HELPERS
# ===========================================================================


# Three related rows bundled together: a verdict, the draft it judged, and the
# ticket both belong to. Just a convenience so later code can write
# `row.ticket.created_at` instead of juggling three parallel lists.
@dataclass(frozen=True)
class _ReviewRow:
    review: RecommendationReview
    recommendation: TicketRecommendation
    ticket: Ticket


# THE one database query in this file. Everything else works on its output.
#
# It joins three tables because the analysis needs a column from each:
#   the review        - the verdict and the final text
#   the recommendation - what the AI suggested, and its category
#   the ticket        - when the customer first wrote in
def _review_rows(
    session: Session,
    *,
    tenant_id: str,
    pilot_categories: list[str],
) -> list[_ReviewRow]:
    # Conditions built as a list first, so an optional one can be added below.
    conditions = [
        RecommendationReview.tenant_id == tenant_id,
        TicketRecommendation.tenant_id == tenant_id,
        Ticket.tenant_id == tenant_id,
        # THE CRITICAL EXCLUSION: baseline results are left out entirely. This
        # report scores the AI, and including keyword-rule results — which humans
        # also review — would blend two completely different things into one
        # meaningless average.
        TicketRecommendation.source != AI_BASELINE_SOURCE,
    ]
    # Added only if a category list was supplied. Empty means "no restriction",
    # matching the same convention used in pilot.py's eligibility rules.
    # `.in_(...)` becomes SQL's IN clause: "category is any one of these".
    if pilot_categories:
        conditions.append(TicketRecommendation.category.in_(pilot_categories))

    rows = session.execute(
        select(RecommendationReview, TicketRecommendation, Ticket)
        .join(
            TicketRecommendation,
            TicketRecommendation.id == RecommendationReview.recommendation_id,
        )
        .join(Ticket, Ticket.id == RecommendationReview.ticket_id)
        # `*conditions` spreads the list out as separate arguments. All are ANDed.
        .where(*conditions)
        # Oldest first. Matters for _feedback_candidates below, which stops at a
        # limit — so the examples returned are the EARLIEST problems, which tend
        # to be the most representative of a systematic issue.
        .order_by(RecommendationReview.created_at.asc())
    ).all()
    return [
        _ReviewRow(
            # `cast(...)` is a note to the type checker only; it produces no code
            # and changes nothing at runtime.
            review=cast(RecommendationReview, row[0]),
            recommendation=cast(TicketRecommendation, row[1]),
            ticket=cast(Ticket, row[2]),
        )
        for row in rows
    ]


# Picks out the drafts worth a human reading.
#
# THE FILTER, stated plainly: keep it if it was rejected, OR if it was changed
# by at least `minimum_edit_distance` characters. Everything else is skipped.
#
# The reasoning is that approvals and trivial edits teach you nothing. A draft
# accepted verbatim, or with a comma moved, is a success — there is nothing to
# learn from it. The instructive cases are the ones humans threw away or
# substantially rewrote.
def _feedback_candidates(
    session: Session,
    *,
    tenant_id: str,
    pilot_categories: list[str],
    minimum_edit_distance: int,
    limit: int,
) -> list[PilotFeedbackCandidate]:
    candidates: list[PilotFeedbackCandidate] = []
    for row in _review_rows(session, tenant_id=tenant_id, pilot_categories=pilot_categories):
        edit_distance = _edit_distance(
            row.recommendation.suggested_reply or "",
            row.review.final_reply or "",
        )
        # `continue` skips to the next row. Read as: "not rejected AND barely
        # changed -> nothing to learn here".
        if row.review.decision != "rejected" and edit_distance < minimum_edit_distance:
            continue
        candidates.append(
            PilotFeedbackCandidate(
                ticket_id=row.ticket.id,
                recommendation_id=row.recommendation.id,
                review_id=row.review.id,
                category=row.recommendation.category,
                decision=row.review.decision,
                notes=row.review.notes,
                edit_distance=edit_distance,
                suggested_reply=row.recommendation.suggested_reply,
                final_reply=row.review.final_reply,
                created_at=row.review.created_at,
            )
        )
        # Stop once enough examples are gathered. Note this happens in Python
        # rather than as a SQL LIMIT, because the filter above depends on edit
        # distance, which the database cannot compute.
        if len(candidates) >= limit:
            break
    return candidates


# Total AI spending attributable to the pilot.
#
# Note the query is built up in two stages. Without a category list it is a
# simple sum of everything; with one, a join is added so only costs tied to
# pilot-category drafts are counted. Building it conditionally avoids paying for
# a join that isn't needed.
#
# A limitation worth knowing: costs with no recommendation_id — failed calls that
# produced nothing — are DROPPED once the join is added. So the filtered figure
# slightly understates true spending, because failed attempts cost money too.
def _estimated_cost(session: Session, *, tenant_id: str, pilot_categories: list[str]) -> float:
    conditions = [CostEvent.tenant_id == tenant_id]
    statement = select(func.coalesce(func.sum(CostEvent.estimated_cost_usd), 0.0)).where(
        *conditions
    )
    if pilot_categories:
        statement = (
            statement.join(
                TicketRecommendation,
                TicketRecommendation.id == CostEvent.recommendation_id,
            )
            .where(TicketRecommendation.category.in_(pilot_categories))
            .where(TicketRecommendation.source != AI_BASELINE_SOURCE)
        )
    value = session.scalar(statement)
    return float(cast(Any, value) or 0.0)


# Counts failures that look safety-related rather than merely technical.
#
# The approach is admittedly rough: fetch the failure counts grouped by error
# code, then check each code for one of the marker words. A network timeout is
# an operational annoyance; a prompt-injection block is a safety event, and the
# two must not be lumped together — because a single safety failure is enough to
# trigger a rollback in the verdict logic below.
#
# The weakness is that it depends on error codes being NAMED helpfully. A safety
# failure reported as "ValidationError" would slip past unnoticed.
def _safety_failure_count(session: Session, *, tenant_id: str) -> int:
    rows = session.execute(
        select(AIRun.error_code, func.count())
        .where(AIRun.tenant_id == tenant_id, AIRun.status == "failed")
        .group_by(AIRun.error_code)
    ).all()
    count = 0
    for error_code, row_count in rows:
        error_text = str(error_code or "").lower()
        # `any(... for ...)` is true if ANY marker word appears in the code.
        if any(marker in error_text for marker in SAFETY_ERROR_MARKERS):
            count += int(cast(Any, row_count) or 0)
    return count


# How long each customer waited for their first human-checked reply.
#
# The subtlety: a ticket can have several reviews, and only the FIRST one counts
# as the first response. The loop keeps, per ticket, the EARLIEST review seen —
# that is what the `row.review.created_at < current[1]` comparison is doing.
#
# `max(..., 0.0)` at the end floors the result at zero. It guards against clock
# oddities producing a review timestamped fractionally before its ticket, which
# would otherwise yield a negative wait and quietly pull the average down.
def _first_response_seconds(rows: list[_ReviewRow]) -> list[float]:
    by_ticket: dict[str, tuple[datetime, datetime]] = {}
    for row in rows:
        current = by_ticket.get(row.ticket.id)
        if current is None or row.review.created_at < current[1]:
            by_ticket[row.ticket.id] = (row.ticket.created_at, row.review.created_at)
    return [
        max((reviewed_at - ticket_created_at).total_seconds(), 0.0)
        for ticket_created_at, reviewed_at in by_ticket.values()
    ]


# Sorts free-text complaints into themes by keyword.
#
# Note the `break`: the FIRST matching theme wins, so a note saying "wrong tone"
# is filed under whichever of "incorrect" or "tone" is checked first — and
# dictionary order decides that. Each note counts exactly once, which keeps the
# totals honest, but the assignment is somewhat arbitrary for notes mentioning
# several problems.
#
# Anything unmatched becomes "unspecified". A large "unspecified" count is itself
# informative: it means either reviewers are not writing useful notes, or the
# keyword lists above need extending.
def _cluster_rejection_reasons(notes: list[str | None]) -> list[PilotRejectionReason]:
    counts: dict[str, int] = {}
    for note in notes:
        note_text = (note or "").lower()      # `or ""` handles a missing note
        reason = "unspecified"
        for candidate_reason, keywords in REJECTION_REASON_KEYWORDS.items():
            if any(keyword in note_text for keyword in keywords):
                reason = candidate_reason
                break
        counts[reason] = counts.get(reason, 0) + 1
    # Sorted alphabetically, so the same data always produces the same order.
    return [
        PilotRejectionReason(reason=reason, count=count)
        for reason, count in sorted(counts.items())
    ]


# ===========================================================================
# THE VERDICT. The most consequential function in the file.
#
# The rules are checked IN ORDER, and the first match wins. That order encodes a
# priority, and it is worth reading carefully:
#
#   1. Too little data      -> iterate    (checked FIRST: with four reviews, a
#                                          100% acceptance rate means nothing)
#   2. Any safety failure   -> roll_back  (overrides every good number below)
#   3. High acceptance AND  -> expand
#      light editing
#   4. Low acceptance       -> stop
#   5. Anything else        -> iterate
#
# Two things that order gets right:
#   - Sample size before quality. A tiny sample cannot justify anything, however
#     flattering it looks.
#   - Safety before success. Even a 95% acceptance rate cannot outvote a single
#     safety failure. That is the correct priority for a system writing to
#     customers, and putting it second in the chain is what enforces it.
#
# The thresholds (5 reviews, 80%, 80 characters, 40%) are judgement calls, not
# laws. What matters is that they were written down BEFORE the results came in.
# ===========================================================================
def _with_exit_decision(metrics: PilotMetrics) -> PilotMetrics:
    if metrics.reviewed_drafts < 5:
        decision = "iterate"
        reason = "Collect at least five reviewed pilot drafts before expanding."
    elif metrics.safety_failures > 0:
        decision = "roll_back"
        reason = "Safety failures were detected during the pilot window."
    elif metrics.draft_acceptance_rate >= 0.8 and metrics.average_edit_distance <= 80:
        # BOTH conditions are required. Acceptance alone would be misleading:
        # humans might be marking drafts "edited" and then rewriting them almost
        # entirely, which counts as acceptance but represents no real saving.
        # The edit-distance condition is what catches that.
        decision = "expand"
        reason = "Acceptance is high and average edit distance is low."
    elif metrics.draft_acceptance_rate < 0.4:
        decision = "stop"
        reason = "Draft acceptance is too low for the current pilot scope."
    else:
        # The middle ground — better than useless, not yet good enough.
        decision = "iterate"
        reason = "Pilot needs prompt, model route, or workflow improvements before expansion."

    # A whole new object is built rather than two fields being changed, because
    # PilotMetrics is frozen and cannot be modified. Verbose, but it guarantees
    # nothing else can quietly alter the figures on their way out.
    return PilotMetrics(
        pilot_categories=metrics.pilot_categories,
        reviewed_drafts=metrics.reviewed_drafts,
        accepted_drafts=metrics.accepted_drafts,
        rejected_drafts=metrics.rejected_drafts,
        edited_drafts=metrics.edited_drafts,
        draft_acceptance_rate=metrics.draft_acceptance_rate,
        average_edit_distance=metrics.average_edit_distance,
        average_time_to_first_response_seconds=metrics.average_time_to_first_response_seconds,
        escalation_accuracy=metrics.escalation_accuracy,
        escalated_reviewed_drafts=metrics.escalated_reviewed_drafts,
        cost_per_accepted_draft=metrics.cost_per_accepted_draft,
        safety_failures=metrics.safety_failures,
        agent_rejection_reasons=metrics.agent_rejection_reasons,
        exit_decision=decision,
        exit_reason=reason,
    )


# Measures how different two pieces of text are, as a number of character edits.
#
# This is the LEVENSHTEIN DISTANCE: the minimum number of single-character
# insertions, deletions, or substitutions needed to turn one string into the
# other. "cat" -> "cart" is 1 (insert an r). "cat" -> "dog" is 3.
#
# Why it matters here: it distinguishes a human fixing a typo from a human
# rewriting the whole reply. Both are recorded as "edited", but they mean
# entirely different things about how well the AI performed.
#
# HOW THE ALGORITHM WORKS, in plain terms:
#   Imagine a grid with one string along the top and the other down the side.
#   Each cell holds "the cost of matching these two prefixes". Every cell is one
#   step worse than one of its neighbours — insert, delete, or substitute — so
#   each is computed as the cheapest of those three options. Fill the grid, and
#   the bottom-right cell is the answer.
#
#   The code keeps only the PREVIOUS row rather than the whole grid, because
#   each row depends solely on the one above it. That reduces memory use from
#   (length x length) to just (length), which matters for long replies.
#
# COST WARNING: this is O(n x m) — for two 2,000-character replies that is four
# million operations. Fine for a pilot's worth of reviews; it would need
# rethinking at scale.
def _edit_distance(left: str, right: str) -> int:
    # Three shortcuts, each avoiding the expensive loop entirely for a common case.
    if left == right:
        return 0                # identical: an approval, or an unchanged draft
    if not left:
        return len(right)       # one side empty: every character must be inserted
    if not right:
        return len(left)        # ...or deleted

    # The first row: turning an empty string into the first N characters of
    # `right` costs exactly N insertions.
    previous = list(range(len(right) + 1))
    for left_index, left_char in enumerate(left, start=1):
        current = [left_index]      # first cell of this row: N deletions
        for right_index, right_char in enumerate(right, start=1):
            insert_cost = current[right_index - 1] + 1        # from the cell to the left
            delete_cost = previous[right_index] + 1           # from the cell above
            # From the cell diagonally above-left. `(left_char != right_char)` is a
            # boolean used as a number: 1 when the characters differ (a
            # substitution is needed), 0 when they match (free).
            replace_cost = previous[right_index - 1] + (left_char != right_char)
            current.append(min(insert_cost, delete_cost, replace_cost))
        previous = current          # this row becomes the "previous" for the next
    return previous[-1]             # the bottom-right cell: the answer


# --- Three small maths helpers, all guarding against division by zero -------
#
# Each returns 0.0 rather than crashing on an empty dataset. That matters most on
# day one, when every one of these would otherwise fail and take the whole
# metrics page down at exactly the moment someone first looks at it.


def _average(values: list[float] | list[int]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 4)


# For counts. Four decimal places is ample for a percentage.
def _ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


# For money. Eight decimal places, because a single AI call can cost a tiny
# fraction of a cent and rounding to four would flatten those to zero.
def _ratio_float(numerator: float, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 8)
