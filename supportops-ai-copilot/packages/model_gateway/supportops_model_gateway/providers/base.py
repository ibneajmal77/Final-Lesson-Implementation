from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class TicketAnalysisInput:
    subject: str
    body: str
    customer_id: str | None = None


@dataclass(frozen=True)
class TicketAnalysisResult:
    source: str
    model_name: str
    prompt_version: str
    category: str
    priority: str
    requires_escalation: bool
    confidence: float
    summary: str
    suggested_reply: str
    extracted_fields: dict[str, object]
    reasons: list[str]


class TicketAnalysisProvider(Protocol):
    def analyze_ticket(self, ticket: TicketAnalysisInput) -> TicketAnalysisResult:
        """Analyze a support ticket and return structured output."""

