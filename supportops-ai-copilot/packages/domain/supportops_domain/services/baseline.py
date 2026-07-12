import re
from dataclasses import dataclass

BASELINE_SOURCE = "baseline_v1"

ORDER_ID_PATTERN = re.compile(r"\b[A-Z]{2,8}-\d{2,}\b")
AMOUNT_PATTERN = re.compile(r"(?:\$|USD\s*)\d+(?:,\d{3})*(?:\.\d{2})?", re.IGNORECASE)


@dataclass(frozen=True)
class BaselineTicketInput:
    subject: str
    body: str


@dataclass(frozen=True)
class BaselineRecommendation:
    source: str
    category: str
    priority: str
    requires_escalation: bool
    confidence: float
    extracted_fields: dict[str, object]
    reasons: list[str]


CategoryRule = tuple[str, tuple[str, ...]]

CATEGORY_RULES: tuple[CategoryRule, ...] = (
    (
        "security",
        (
            "account hacked",
            "hacked",
            "unauthorized",
            "fraud",
            "stolen card",
            "compromised",
            "breach",
        ),
    ),
    (
        "billing",
        (
            "charged twice",
            "double charged",
            "refund",
            "invoice",
            "billing",
            "payment",
            "chargeback",
        ),
    ),
    (
        "account_access",
        (
            "login",
            "password",
            "locked out",
            "cannot access",
            "can't access",
            "reset",
            "two factor",
            "2fa",
        ),
    ),
    (
        "delivery",
        (
            "shipping",
            "delivery",
            "tracking",
            "delayed",
            "late order",
            "where is my order",
        ),
    ),
    (
        "technical_issue",
        (
            "bug",
            "error",
            "crash",
            "broken",
            "not working",
            "failed",
            "timeout",
        ),
    ),
)

HIGH_PRIORITY_TERMS = (
    "angry",
    "complaint",
    "escalate",
    "manager",
    "lawsuit",
    "chargeback",
    "cancel",
    "charged twice",
    "double charged",
)

SECURITY_ESCALATION_TERMS = (
    "account hacked",
    "hacked",
    "unauthorized",
    "fraud",
    "stolen card",
    "compromised",
    "breach",
)


def classify_ticket(ticket: BaselineTicketInput) -> BaselineRecommendation:
    text = _combined_text(ticket)
    category, matched_category_terms = _detect_category(text)
    order_ids = _extract_unique(ORDER_ID_PATTERN, ticket.subject, ticket.body)
    amounts = _extract_unique(AMOUNT_PATTERN, ticket.subject, ticket.body)
    high_priority_terms = _matched_terms(text, HIGH_PRIORITY_TERMS)
    escalation_terms = _matched_terms(text, SECURITY_ESCALATION_TERMS)

    requires_escalation = bool(escalation_terms)
    priority = _determine_priority(
        category=category,
        requires_escalation=requires_escalation,
        high_priority_terms=high_priority_terms,
        order_ids=order_ids,
        amounts=amounts,
    )
    confidence = _confidence(category=category, matched_terms=matched_category_terms)
    reasons = _build_reasons(
        category=category,
        priority=priority,
        requires_escalation=requires_escalation,
        matched_category_terms=matched_category_terms,
        high_priority_terms=high_priority_terms,
        order_ids=order_ids,
        amounts=amounts,
    )

    return BaselineRecommendation(
        source=BASELINE_SOURCE,
        category=category,
        priority=priority,
        requires_escalation=requires_escalation,
        confidence=confidence,
        extracted_fields={
            "order_ids": order_ids,
            "amounts": amounts,
            "matched_category_terms": matched_category_terms,
            "matched_priority_terms": high_priority_terms,
            "matched_escalation_terms": escalation_terms,
        },
        reasons=reasons,
    )


def _combined_text(ticket: BaselineTicketInput) -> str:
    return f"{ticket.subject}\n{ticket.body}".lower()


def _detect_category(text: str) -> tuple[str, list[str]]:
    for category, keywords in CATEGORY_RULES:
        matched = _matched_terms(text, keywords)
        if matched:
            return category, matched
    return "other", []


def _matched_terms(text: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if term in text]


def _extract_unique(pattern: re.Pattern[str], subject: str, body: str) -> list[str]:
    values = [match.group(0) for match in pattern.finditer(f"{subject}\n{body}")]
    return sorted(set(values))


def _determine_priority(
    *,
    category: str,
    requires_escalation: bool,
    high_priority_terms: list[str],
    order_ids: list[str],
    amounts: list[str],
) -> str:
    if requires_escalation:
        return "urgent"
    if high_priority_terms:
        return "high"
    if category == "billing" and (order_ids or amounts):
        return "high"
    return "normal"


def _confidence(*, category: str, matched_terms: list[str]) -> float:
    if category == "other":
        return 0.35
    if len(matched_terms) >= 2:
        return 0.85
    return 0.72


def _build_reasons(
    *,
    category: str,
    priority: str,
    requires_escalation: bool,
    matched_category_terms: list[str],
    high_priority_terms: list[str],
    order_ids: list[str],
    amounts: list[str],
) -> list[str]:
    reasons = []
    if matched_category_terms:
        reasons.append(
            f"Category '{category}' matched keywords: {', '.join(matched_category_terms)}."
        )
    else:
        reasons.append("No specific category keywords matched, so category is 'other'.")

    if order_ids:
        reasons.append(f"Extracted order IDs: {', '.join(order_ids)}.")
    if amounts:
        reasons.append(f"Extracted money amounts: {', '.join(amounts)}.")
    if high_priority_terms:
        reasons.append(f"Priority '{priority}' matched terms: {', '.join(high_priority_terms)}.")
    elif priority == "high":
        reasons.append("Priority 'high' was assigned because billing context included order data.")
    else:
        reasons.append(f"Priority '{priority}' was assigned by baseline rules.")

    if requires_escalation:
        reasons.append("Human escalation is required because security-risk terms were found.")

    return reasons

