from datetime import datetime
from typing import Any

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
