from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

ReviewDecision = Literal["approved", "rejected", "edited"]


class TicketRecommendationReviewCreate(BaseModel):
    decision: ReviewDecision
    edited_summary: str | None = Field(default=None, min_length=1, max_length=2000)
    edited_reply: str | None = Field(default=None, min_length=1, max_length=5000)
    notes: str | None = Field(default=None, min_length=1, max_length=2000)


class TicketRecommendationReviewRead(BaseModel):
    id: str
    tenant_id: str
    ticket_id: str
    recommendation_id: str
    reviewer_user_id: str
    decision: ReviewDecision
    final_summary: str | None
    final_reply: str | None
    notes: str | None
    created_at: datetime

