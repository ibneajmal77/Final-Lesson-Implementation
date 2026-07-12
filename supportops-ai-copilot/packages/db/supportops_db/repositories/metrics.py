from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from supportops_db.models import RecommendationReview, TicketRecommendation


@dataclass(frozen=True)
class ReviewDecisionCounts:
    key: str
    total_reviews: int
    approved: int
    rejected: int
    edited: int


@dataclass(frozen=True)
class TenantReviewMetrics:
    total_recommendations: int
    reviewed_recommendations: int
    overall: ReviewDecisionCounts
    by_source: list[ReviewDecisionCounts]
    by_category: list[ReviewDecisionCounts]


def get_tenant_review_metrics(session: Session, *, tenant_id: str) -> TenantReviewMetrics:
    total_recommendations = session.scalar(
        select(func.count())
        .select_from(TicketRecommendation)
        .where(TicketRecommendation.tenant_id == tenant_id)
    )
    reviewed_recommendations = session.scalar(
        select(func.count(func.distinct(RecommendationReview.recommendation_id))).where(
            RecommendationReview.tenant_id == tenant_id
        )
    )

    return TenantReviewMetrics(
        total_recommendations=int(total_recommendations or 0),
        reviewed_recommendations=int(reviewed_recommendations or 0),
        overall=_overall_counts(session, tenant_id=tenant_id),
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


def _overall_counts(session: Session, *, tenant_id: str) -> ReviewDecisionCounts:
    rows = session.execute(
        select(RecommendationReview.decision, func.count())
        .where(RecommendationReview.tenant_id == tenant_id)
        .group_by(RecommendationReview.decision)
    ).all()
    return _counts_from_rows("all", rows)


def _grouped_counts(
    session: Session,
    *,
    tenant_id: str,
    group_field: object,
) -> list[ReviewDecisionCounts]:
    rows = session.execute(
        select(group_field, RecommendationReview.decision, func.count())
        .join(
            TicketRecommendation,
            TicketRecommendation.id == RecommendationReview.recommendation_id,
        )
        .where(
            RecommendationReview.tenant_id == tenant_id,
            TicketRecommendation.tenant_id == tenant_id,
        )
        .group_by(group_field, RecommendationReview.decision)
        .order_by(group_field)
    ).all()

    grouped: dict[str, list[tuple[str, int]]] = {}
    for key, decision, count in rows:
        grouped.setdefault(str(key), []).append((str(decision), int(count)))

    return [_counts_from_rows(key, decision_rows) for key, decision_rows in grouped.items()]


def _counts_from_rows(key: str, rows: list[tuple[str, int]]) -> ReviewDecisionCounts:
    counts = {"approved": 0, "rejected": 0, "edited": 0}
    for decision, count in rows:
        if decision in counts:
            counts[decision] = int(count)

    total_reviews = counts["approved"] + counts["rejected"] + counts["edited"]
    return ReviewDecisionCounts(
        key=key,
        total_reviews=total_reviews,
        approved=counts["approved"],
        rejected=counts["rejected"],
        edited=counts["edited"],
    )
