from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    external_id: str = Field(min_length=1, max_length=200)
    channel: str = Field(min_length=1, max_length=50)
    subject: str = Field(min_length=1, max_length=500)
    body: str = Field(min_length=1)
    customer_id: str | None = Field(default=None, max_length=200)
    metadata: dict[str, Any] = Field(default_factory=dict)


class TicketRead(BaseModel):
    id: str
    tenant_id: str
    external_id: str
    channel: str
    subject: str
    body: str
    status: str
    priority: str
    customer_id: str | None
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class TicketRecommendationRead(BaseModel):
    id: str
    tenant_id: str
    ticket_id: str
    source: str
    category: str
    priority: str
    requires_escalation: bool
    confidence: float
    model_name: str | None
    prompt_version: str | None
    summary: str | None
    suggested_reply: str | None
    extracted_fields: dict[str, Any]
    reasons: list[str]
    created_at: datetime


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
