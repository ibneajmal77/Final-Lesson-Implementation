from pydantic import BaseModel


class ReviewMetricBreakdownRead(BaseModel):
    key: str
    total_reviews: int
    approved: int
    rejected: int
    edited: int
    approval_rate: float
    rejection_rate: float
    edit_rate: float


class TenantReviewMetricsRead(BaseModel):
    tenant_id: str
    total_recommendations: int
    reviewed_recommendations: int
    review_coverage_rate: float
    total_reviews: int
    approved: int
    rejected: int
    edited: int
    approval_rate: float
    rejection_rate: float
    edit_rate: float
    by_source: list[ReviewMetricBreakdownRead]
    by_category: list[ReviewMetricBreakdownRead]

