from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

TicketCategory = Literal[
    "security",
    "billing",
    "account_access",
    "delivery",
    "technical_issue",
    "other",
]

TicketPriority = Literal["low", "normal", "high", "urgent"]

RiskFlag = Literal[
    "prompt_injection",
    "pii",
    "payment_risk",
    "security_risk",
    "policy_gap",
    "none",
]


class StrictPromptModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TicketClassification(StrictPromptModel):
    category: TicketCategory
    category_confidence: float = Field(ge=0, le=1)
    rationale: str = Field(min_length=1, max_length=1000)
    abstain: bool
    missing_information: list[str] = Field(default_factory=list)


class TicketFieldExtraction(StrictPromptModel):
    order_ids: list[str] = Field(default_factory=list)
    amounts: list[str] = Field(default_factory=list)
    product_names: list[str] = Field(default_factory=list)
    account_identifiers: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)


class PriorityRecommendation(StrictPromptModel):
    priority: TicketPriority
    requires_escalation: bool
    confidence: float = Field(ge=0, le=1)
    reasons: list[str] = Field(min_length=1)


class DraftResponse(StrictPromptModel):
    response_text: str = Field(min_length=1, max_length=5000)
    tone: Literal["empathetic", "direct", "formal", "neutral"]
    needs_human_review: bool
    forbidden_claims: list[str] = Field(default_factory=list)


class SafetyCheck(StrictPromptModel):
    safe_to_draft: bool
    risk_flags: list[RiskFlag] = Field(default_factory=list)
    blocked_reasons: list[str] = Field(default_factory=list)
    pii_detected: bool


class FullTicketAnalysis(StrictPromptModel):
    category: TicketCategory
    category_confidence: float = Field(ge=0, le=1)
    priority: TicketPriority
    requires_escalation: bool
    extracted_fields: TicketFieldExtraction
    evidence_ids: list[str] = Field(default_factory=list)
    draft_response: DraftResponse | None
    abstain: bool
    risk_flags: list[RiskFlag] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
