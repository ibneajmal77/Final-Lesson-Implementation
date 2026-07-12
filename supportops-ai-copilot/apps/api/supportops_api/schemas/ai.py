from datetime import datetime
from typing import Any

from pydantic import BaseModel


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

