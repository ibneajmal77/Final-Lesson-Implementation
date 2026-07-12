from dataclasses import dataclass
from typing import Protocol

from supportops_domain.baseline_classifier import BaselineTicketInput, classify_ticket

MOCK_PROVIDER_NAME = "mock"
MOCK_SOURCE = "mock_llm_v1"
MOCK_MODEL_NAME = "mock-ticket-analyzer"
PROMPT_VERSION = "supportops_ticket_analysis_v1"


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


class UnsupportedModelProviderError(ValueError):
    pass


class MockTicketAnalysisProvider:
    def analyze_ticket(self, ticket: TicketAnalysisInput) -> TicketAnalysisResult:
        baseline = classify_ticket(BaselineTicketInput(subject=ticket.subject, body=ticket.body))
        summary = _summary_for_category(
            category=baseline.category,
            priority=baseline.priority,
            extracted_fields=baseline.extracted_fields,
        )
        suggested_reply = _suggested_reply_for_category(
            category=baseline.category,
            requires_escalation=baseline.requires_escalation,
            extracted_fields=baseline.extracted_fields,
        )

        return TicketAnalysisResult(
            source=MOCK_SOURCE,
            model_name=MOCK_MODEL_NAME,
            prompt_version=PROMPT_VERSION,
            category=baseline.category,
            priority=baseline.priority,
            requires_escalation=baseline.requires_escalation,
            confidence=min(baseline.confidence + 0.05, 0.9),
            summary=summary,
            suggested_reply=suggested_reply,
            extracted_fields={
                **baseline.extracted_fields,
                "customer_id": ticket.customer_id,
                "provider": MOCK_PROVIDER_NAME,
            },
            reasons=[
                "Mock provider used deterministic baseline analysis.",
                *baseline.reasons,
            ],
        )


def build_ticket_analysis_provider(provider_name: str) -> TicketAnalysisProvider:
    normalized = provider_name.strip().lower()
    if normalized == MOCK_PROVIDER_NAME:
        return MockTicketAnalysisProvider()
    raise UnsupportedModelProviderError(f"unsupported model provider: {provider_name}")


def _summary_for_category(
    *,
    category: str,
    priority: str,
    extracted_fields: dict[str, object],
) -> str:
    order_ids = _string_list(extracted_fields.get("order_ids"))
    order_text = f" involving order {', '.join(order_ids)}" if order_ids else ""
    return f"Customer reported a {priority} priority {category} issue{order_text}."


def _suggested_reply_for_category(
    *,
    category: str,
    requires_escalation: bool,
    extracted_fields: dict[str, object],
) -> str:
    order_ids = _string_list(extracted_fields.get("order_ids"))
    order_sentence = (
        f" I can see this relates to order {', '.join(order_ids)}." if order_ids else ""
    )

    if requires_escalation:
        return (
            "Thanks for reporting this. I am escalating this to a specialist for immediate review."
            f"{order_sentence} We will follow up with the next secure step shortly."
        )
    if category == "billing":
        return (
            "Thanks for reaching out. I will review the billing details and check the "
            "charge history."
            f"{order_sentence} I will update you with the next step after verification."
        )
    if category == "account_access":
        return (
            "Thanks for contacting us. I will help verify the account access issue and guide you "
            "through the safest recovery step."
        )
    if category == "delivery":
        return (
            "Thanks for the details. I will check the delivery and tracking information."
            f"{order_sentence} I will share the latest status once it is confirmed."
        )
    if category == "technical_issue":
        return (
            "Thanks for flagging this. I will review the technical issue and gather the details "
            "needed to reproduce or route it correctly."
        )
    return (
        "Thanks for reaching out. I will review your request and make sure it is routed to the "
        "right support path."
    )


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]
