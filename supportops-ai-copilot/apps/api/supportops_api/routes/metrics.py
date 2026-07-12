from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from supportops_api.dependencies import Actor, get_current_actor, get_db_session
from supportops_api.schemas.metrics import ReviewMetricBreakdownRead, TenantReviewMetricsRead
from supportops_db.repositories.metrics import ReviewDecisionCounts, get_tenant_review_metrics
from supportops_db.repositories.tenants import get_tenant

router = APIRouter(prefix="/metrics", tags=["metrics"])

ActorDep = Annotated[Actor, Depends(get_current_actor)]
SessionDep = Annotated[Session, Depends(get_db_session)]


@router.get("/reviews", response_model=TenantReviewMetricsRead)
def get_review_metrics_endpoint(
    actor: ActorDep,
    session: SessionDep,
) -> TenantReviewMetricsRead:
    if not get_tenant(session, actor.tenant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tenant not found")

    metrics = get_tenant_review_metrics(session, tenant_id=actor.tenant_id)
    overall = _breakdown_to_read(metrics.overall)
    return TenantReviewMetricsRead(
        tenant_id=actor.tenant_id,
        total_recommendations=metrics.total_recommendations,
        reviewed_recommendations=metrics.reviewed_recommendations,
        review_coverage_rate=_rate(
            metrics.reviewed_recommendations,
            metrics.total_recommendations,
        ),
        total_reviews=overall.total_reviews,
        approved=overall.approved,
        rejected=overall.rejected,
        edited=overall.edited,
        approval_rate=overall.approval_rate,
        rejection_rate=overall.rejection_rate,
        edit_rate=overall.edit_rate,
        by_source=[_breakdown_to_read(item) for item in metrics.by_source],
        by_category=[_breakdown_to_read(item) for item in metrics.by_category],
    )


def _breakdown_to_read(counts: ReviewDecisionCounts) -> ReviewMetricBreakdownRead:
    return ReviewMetricBreakdownRead(
        key=counts.key,
        total_reviews=counts.total_reviews,
        approved=counts.approved,
        rejected=counts.rejected,
        edited=counts.edited,
        approval_rate=_rate(counts.approved, counts.total_reviews),
        rejection_rate=_rate(counts.rejected, counts.total_reviews),
        edit_rate=_rate(counts.edited, counts.total_reviews),
    )


def _rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)

