# ============================================================================
# FILE: packages/db/supportops_db/repositories/metrics.py
#
# THINK OF THIS FILE AS: the counting machine behind the quality scoreboard.
# It answers one question — "of all the drafts the AI wrote, how many did humans
# approve, edit, or throw away?" — sliced several ways.
#
# This is where the numbers on GET /metrics/reviews actually come from.
#
# THE KEY IDEA: COUNT IN THE DATABASE, NOT IN PYTHON.
#   Every function here uses func.count() and GROUP BY, so the database does the
#   counting and sends back a handful of numbers. The naive alternative — fetch
#   every review row and count them in a Python loop — would work fine on a
#   hundred rows and fall over on a million: all that data would have to cross
#   the network and sit in memory to produce a result that is ultimately six
#   integers. Databases are extremely good at counting; let them.
#
# WHAT "GROUP BY" MEANS, if it is unfamiliar:
#   It tells the database "bundle the rows that share a value, and give me one
#   summary line per bundle". GROUP BY decision turns a million review rows into
#   three lines: approved 700,000 / edited 200,000 / rejected 100,000.
#
# ONE DELIBERATE OMISSION: no percentages are calculated here.
#   Only whole counts are returned. The rates are worked out one layer up, by
#   _rate() in routes/metrics.py. That split is on purpose — counts are facts
#   that can be added together and re-sliced, whereas rates are a presentation
#   choice and cannot be meaningfully averaged with each other later.
# ============================================================================

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, cast

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from supportops_db.models import RecommendationReview, TicketRecommendation


# The three verdict counts for one slice of the data.
#
# `key` says what this slice IS. The same class is reused for the overall
# figures (key="all"), for each source (key="baseline_v1", "hosted"), and for
# each category (key="billing", "technical"). One flexible shape rather than
# three nearly identical ones.
@dataclass(frozen=True)
class ReviewDecisionCounts:
    key: str
    total_reviews: int
    approved: int
    rejected: int
    edited: int


# The complete quality report for one company.
@dataclass(frozen=True)
class TenantReviewMetrics:
    # These two are about COVERAGE, and they come first because they tell you how
    # much to trust everything else. If only 20 of 1,000 drafts were ever
    # reviewed, an approval rate describes those 20 — and the 980 nobody looked
    # at may be quietly terrible.
    total_recommendations: int
    reviewed_recommendations: int

    overall: ReviewDecisionCounts             # the headline figures
    by_source: list[ReviewDecisionCounts]     # baseline rules vs the AI
    by_category: list[ReviewDecisionCounts]   # by ticket type


# The entry point. Runs four separate queries and assembles the result.
#
# Four round trips rather than one clever combined query. A reasonable trade:
# each query is simple enough to read and reason about, and at this scale the
# extra trips cost microseconds. A single query producing all of this would be
# considerably harder to understand and to change.
def get_tenant_review_metrics(session: Session, *, tenant_id: str) -> TenantReviewMetrics:
    # QUERY 1: how many drafts exist in total?
    total_recommendations = session.scalar(
        select(func.count())
        .select_from(TicketRecommendation)
        .where(TicketRecommendation.tenant_id == tenant_id)
    )

    # QUERY 2: how many DISTINCT drafts were reviewed at all?
    #
    # `func.distinct(...)` is the crucial word. Without it, a draft reviewed
    # twice — an agent's verdict plus a supervisor's — would be counted twice,
    # and the coverage figure could exceed 100%, which is nonsense. Counting
    # distinct recommendation IDs answers "how many drafts got looked at",
    # rather than "how many verdicts were recorded".
    reviewed_recommendations = session.scalar(
        select(func.count(func.distinct(RecommendationReview.recommendation_id))).where(
            RecommendationReview.tenant_id == tenant_id
        )
    )

    return TenantReviewMetrics(
        # `int(x or 0)` guards against the query returning None on an empty
        # table, so callers always get a real number to do arithmetic with.
        total_recommendations=int(total_recommendations or 0),
        reviewed_recommendations=int(reviewed_recommendations or 0),
        overall=_overall_counts(session, tenant_id=tenant_id),                    # QUERY 3

        # QUERIES 4 and 5. Note the same helper is called twice, with a different
        # COLUMN passed in each time. Passing a column as an argument is what
        # allows one function to serve both slices instead of two copies.
        by_source=_grouped_counts(
            session,
            tenant_id=tenant_id,
            group_field=TicketRecommendation.source,
        ),
        by_category=_grouped_counts(
            session,
            tenant_id=tenant_id,
            group_field=TicketRecommendation.category,
        ),
    )


# The headline counts: every review for this company, grouped by verdict.
#
# Returns at most three rows — one per verdict — however many millions of reviews
# exist. That is the whole value of GROUP BY.
def _overall_counts(session: Session, *, tenant_id: str) -> ReviewDecisionCounts:
    rows = session.execute(
        select(RecommendationReview.decision, func.count())
        .where(RecommendationReview.tenant_id == tenant_id)
        .group_by(RecommendationReview.decision)
    ).all()
    # `session.execute(...)` rather than `.scalar(...)` because each row has TWO
    # values — the verdict and its count — not one.
    return _counts_from_rows("all", [(row[0], row[1]) for row in rows])


# The sliced counts: reviews grouped by verdict AND by some other column.
#
# `group_field: Any` is what makes this reusable. The caller passes an actual
# column object (TicketRecommendation.source or .category) and this builds the
# query around it. The type is left loose because SQLAlchemy column objects are
# awkward to describe precisely without hurting readability.
def _grouped_counts(
    session: Session,
    *,
    tenant_id: str,
    group_field: Any,
) -> list[ReviewDecisionCounts]:
    rows = session.execute(
        select(group_field, RecommendationReview.decision, func.count())
        # A JOIN links two tables. The reviews table records the verdict but not
        # the category; the recommendations table records the category but not
        # the verdict. Joining them on the shared ID lets the database group by a
        # column from one table while counting rows from the other.
        .join(
            TicketRecommendation,
            TicketRecommendation.id == RecommendationReview.recommendation_id,
        )
        .where(
            # BOTH tables are filtered by tenant, not just one. Strictly the
            # second is redundant — a review and its recommendation always share
            # a company. Keeping it is cheap insurance: if the data were ever
            # inconsistent, this stops one company's numbers leaking into
            # another's report rather than silently blending them.
            RecommendationReview.tenant_id == tenant_id,
            TicketRecommendation.tenant_id == tenant_id,
        )
        # Grouping by TWO columns gives one row per combination, e.g.
        # ("billing", "approved", 42) — which is exactly the shape needed.
        .group_by(group_field, RecommendationReview.decision)
        .order_by(group_field)      # stable ordering, so the same data always produces
                                    # the same output — which matters for tests and for
                                    # anyone comparing two reports by eye
    ).all()

    # The database returns flat rows; the report wants them nested one level.
    # This loop reshapes:
    #   ("billing", "approved", 42), ("billing", "rejected", 5), ...
    # into:
    #   {"billing": [("approved", 42), ("rejected", 5)], ...}
    grouped: dict[str, list[tuple[str, int]]] = {}
    for key, decision, count in rows:
        # `setdefault(k, [])` means "give me the list for this key, creating an
        # empty one first if it isn't there yet" — the compact way to build a
        # dictionary of lists without checking for each key first.
        grouped.setdefault(str(key), []).append((str(decision), int(count)))

    return [_counts_from_rows(key, decision_rows) for key, decision_rows in grouped.items()]


# Turns a handful of (verdict, count) pairs into a filled-in counts object.
#
# The important job here is HANDLING WHAT IS MISSING. The database only returns
# rows for verdicts that actually occurred: if nothing was ever rejected, there
# is simply no "rejected" row. Reading that value directly would fail.
#
# Starting from a dictionary with all three set to zero means every verdict
# always has a value, and an absent one correctly reads as 0 rather than
# crashing or being left out of the report entirely.
def _counts_from_rows(key: str, rows: Iterable[tuple[object, object]]) -> ReviewDecisionCounts:
    counts = {"approved": 0, "rejected": 0, "edited": 0}
    for decision, count in rows:
        decision_text = str(decision)
        # `if decision_text in counts` quietly ignores any verdict that is not one
        # of the expected three. Defensive: if a stray value ever reached the
        # database, this report degrades gracefully rather than crashing.
        # The trade-off is that such a value would be invisible here — the total
        # simply would not include it.
        if decision_text in counts:
            counts[decision_text] = int(cast(Any, count))

    # The total is computed by adding the three, NOT by a separate COUNT query.
    # That guarantees the parts always add up to the whole — with two independent
    # queries they could disagree if rows were written between them.
    total_reviews = counts["approved"] + counts["rejected"] + counts["edited"]
    return ReviewDecisionCounts(
        key=key,
        total_reviews=total_reviews,
        approved=counts["approved"],
        rejected=counts["rejected"],
        edited=counts["edited"],
    )
