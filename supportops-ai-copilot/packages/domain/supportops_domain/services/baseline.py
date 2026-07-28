# ============================================================================
# FILE: packages/domain/supportops_domain/services/baseline.py
#
# THINK OF THIS FILE AS: the "dumb but honest" ticket classifier. No AI at all —
# just a list of keywords and some rules about what they mean.
#
# WHY A PROJECT ABOUT AI CONTAINS A DELIBERATELY NON-AI CLASSIFIER:
#   This is the YARDSTICK. Before you can claim an AI is worth its cost, you have
#   to answer: worth it compared to WHAT? The honest comparison is not against
#   nothing — it is against the simplest thing that could possibly work. And that
#   is this: search the text for obvious words.
#
#   It is a genuinely useful benchmark because it is free, instant, and never
#   fails. If the expensive language model cannot clearly beat keyword matching,
#   the language model is not earning its keep. Every recommendation records
#   which method produced it (the `source` column), so that comparison is
#   available in the metrics at any time.
#
# ITS THREE JOBS IN THE RUNNING SYSTEM:
#   1. The /baseline-analysis endpoint — the comparison point
#   2. The pilot gate — routes/tickets.py uses this to work out a ticket's
#      category BEFORE deciding whether the AI is allowed to run. It must be free
#      and instant, since it runs before every AI call.
#   3. The mock provider's brain — providers/mock.py dresses this up as if an AI
#      had produced it, which is how the tests run without an API key
#
# WHAT IT PRODUCES: a category, a priority, whether a human must step in, a
# confidence score, extracted details, and plain-English reasons — the same shape
# an AI returns, which is exactly what makes them comparable.
#
# IT IS COMPLETELY DETERMINISTIC. Same ticket in, same answer out, every time.
# No network, no database, no clock. That is what makes it trivial to test and
# impossible for it to fail or be slow.
# ============================================================================

import re
from dataclasses import dataclass

# The version is part of the name on purpose. When these rules change, results
# from the old and new versions stay distinguishable in the database forever.
BASELINE_SOURCE = "baseline_v1"

# Order numbers like "ORD-12345" or "INVOICE-9981": two to eight capital letters,
# a dash, then at least two digits. `\b` marks a word boundary, so it will not
# match a fragment in the middle of a longer string.
ORDER_ID_PATTERN = re.compile(r"\b[A-Z]{2,8}-\d{2,}\b")

# Money: "$50", "$1,299.99", "USD 40". Handles thousands separators and optional
# cents.
AMOUNT_PATTERN = re.compile(r"(?:\$|USD\s*)\d+(?:,\d{3})*(?:\.\d{2})?", re.IGNORECASE)


# What goes in. Note how little it is — just two pieces of text. No tenant, no
# database object. That narrowness is what keeps this function pure and portable.
@dataclass(frozen=True)
class BaselineTicketInput:
    subject: str
    body: str


# What comes out. Deliberately mirrors the AI's result shape, so the two can be
# stored in the same table and compared directly.
@dataclass(frozen=True)
class BaselineRecommendation:
    source: str
    category: str
    priority: str
    requires_escalation: bool
    confidence: float
    extracted_fields: dict[str, object]
    reasons: list[str]


# A type alias, purely for readability: each rule is a category name paired with
# the keywords that indicate it.
CategoryRule = tuple[str, tuple[str, ...]]

# THE KEYWORD RULES — the heart of the file.
#
# ORDER MATTERS ENORMOUSLY. _detect_category below stops at the FIRST category
# with a match, so this list is a priority order, not just a collection.
#
# "security" is first for a reason worth understanding. A ticket saying "my
# account was hacked and I was charged twice" contains both security and billing
# keywords. Classifying it as billing would route a fraud report into a refunds
# queue — where nobody is watching for a compromised account. Putting security
# first means the more serious reading always wins.
#
# The general principle: when a ticket could be two things, treat it as the one
# where being wrong costs the most.
CATEGORY_RULES: tuple[CategoryRule, ...] = (
    (
        "security",           # FIRST: the highest-stakes category
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
        "billing",            # money problems: upsetting, and time-sensitive
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
        "account_access",     # locked out: frustrating but rarely dangerous
        (
            "login",
            "password",
            "locked out",
            "cannot access",
            "can't access",     # both spellings, since people write both
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
        "technical_issue",    # LAST: the vaguest terms, so it only wins when
        (                     # nothing more specific matched. "error" and
            "bug",            # "failed" appear in all sorts of tickets, so
            "error",          # placing this first would swallow many of them
            "crash",
            "broken",
            "not working",
            "failed",
            "timeout",
        ),
    ),
)

# Words suggesting the customer is upset, or that the situation is about to
# escalate on its own. These raise the PRIORITY without changing the category —
# an angry billing question is still a billing question, it just needs answering
# sooner.
#
# "cancel", "lawsuit", and "manager" are the tells of a customer about to leave
# or complain formally; "charged twice" appears here as well as in the billing
# category, because a double charge is both a topic and an urgency signal.
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

# Words that force a human specialist to take over, whatever else is true.
#
# Note this list is IDENTICAL to the security category's keywords. That
# duplication is deliberate rather than sloppy: the two lists answer different
# questions ("what is this about?" and "must a human handle it?"), and keeping
# them separate means one can change without silently altering the other.
SECURITY_ESCALATION_TERMS = (
    "account hacked",
    "hacked",
    "unauthorized",
    "fraud",
    "stolen card",
    "compromised",
    "breach",
)


# THE MAIN FUNCTION. Reads as a straight sequence: gather the signals, then
# decide.
def classify_ticket(ticket: BaselineTicketInput) -> BaselineRecommendation:
    text = _combined_text(ticket)
    category, matched_category_terms = _detect_category(text)

    # Note these two search the ORIGINAL text, not the lower-cased version,
    # because both patterns depend on capital letters and formatting.
    order_ids = _extract_unique(ORDER_ID_PATTERN, ticket.subject, ticket.body)
    amounts = _extract_unique(AMOUNT_PATTERN, ticket.subject, ticket.body)

    high_priority_terms = _matched_terms(text, HIGH_PRIORITY_TERMS)
    escalation_terms = _matched_terms(text, SECURITY_ESCALATION_TERMS)

    # Any security term at all means a human takes over. No thresholds, no
    # judgement — the right posture when the cost of being wrong is a real fraud
    # going unhandled.
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
        # THE MATCHED TERMS ARE STORED, not just the conclusions. That is what
        # makes this classifier auditable: you can look at any past result and
        # see exactly which words produced it. Debugging a misclassification
        # becomes reading a list rather than guessing.
        extracted_fields={
            "order_ids": order_ids,
            "amounts": amounts,
            "matched_category_terms": matched_category_terms,
            "matched_priority_terms": high_priority_terms,
            "matched_escalation_terms": escalation_terms,
        },
        reasons=reasons,
    )


# ===========================================================================
# HELPERS
# ===========================================================================


# Joins subject and body, lower-cased.
#
# Lower-casing once here — rather than at each comparison — is why every keyword
# list above is written in lower case. Get that wrong and a capitalised "Refund"
# at the start of a subject line would never match.
def _combined_text(ticket: BaselineTicketInput) -> str:
    return f"{ticket.subject}\n{ticket.body}".lower()


# Finds the category, using the priority order described above.
#
# The `return` inside the loop is the important line: it stops at the FIRST
# category with any match. Not the best match, not the most matches — the first.
# Simple, predictable, and it makes the ordering of CATEGORY_RULES the whole
# policy.
#
# Falls back to "other" with no matched terms, which is what drives the low
# confidence score below.
def _detect_category(text: str) -> tuple[str, list[str]]:
    for category, keywords in CATEGORY_RULES:
        matched = _matched_terms(text, keywords)
        if matched:
            return category, matched
    return "other", []


# Returns every term from the list that appears in the text.
#
# `term in text` is a plain substring check, and its limits are worth being
# honest about: "cancel" matches inside "cancellation policy", and a ticket
# saying "I do NOT want to cancel" is matched just as strongly as one saying "I
# want to cancel". Keyword matching has no notion of negation or context.
#
# That is precisely the weakness a language model is supposed to fix — which is
# what makes this a fair and informative baseline rather than a straw man.
def _matched_terms(text: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if term in text]


# Pulls every match for a pattern out of the text, deduplicated and sorted.
#
# `set(...)` removes duplicates — an order number mentioned in both the subject
# and the body should appear once. `sorted(...)` makes the output stable, so the
# same ticket always produces the same list, which matters for tests and for
# comparing two results by eye.
def _extract_unique(pattern: re.Pattern[str], subject: str, body: str) -> list[str]:
    values = [match.group(0) for match in pattern.finditer(f"{subject}\n{body}")]
    return sorted(set(values))


# Decides urgency. Checks run in order of severity, first match wins.
def _determine_priority(
    *,
    category: str,
    requires_escalation: bool,
    high_priority_terms: list[str],
    order_ids: list[str],
    amounts: list[str],
) -> str:
    # Security always outranks everything else.
    if requires_escalation:
        return "urgent"
    # An upset or escalating customer.
    if high_priority_terms:
        return "high"
    # THE SUBTLE RULE, and the only one using more than keywords: a billing
    # ticket that cites a specific order number or amount is treated as more
    # urgent than a general billing question.
    #
    # The reasoning is sound — "why was I charged $89.99 on order ORD-4471?" is a
    # concrete, actionable dispute, whereas "how does billing work?" is a
    # question. Concrete disputes turn into chargebacks if left alone.
    if category == "billing" and (order_ids or amounts):
        return "high"
    return "normal"


# Assigns a confidence score.
#
# The numbers are hand-picked judgements, not anything statistical, and the
# reasoning behind each is straightforward:
#   0.35 for "other"          - we genuinely have no idea. Deliberately below
#                               0.5, so it reads as "do not rely on this"
#   0.85 for two or more hits - several independent signals agreeing is
#                               meaningfully stronger evidence than one
#   0.72 for a single hit     - probably right, but one keyword could easily be
#                               incidental
#
# Note the ceiling: it never returns 1.0. Keyword matching should never claim
# certainty, and reserving the top of the range is a small piece of honesty that
# also leaves room for the mock provider to sit slightly above it.
def _confidence(*, category: str, matched_terms: list[str]) -> float:
    if category == "other":
        return 0.35
    if len(matched_terms) >= 2:
        return 0.85
    return 0.72


# Builds the plain-English explanation a human reviewer reads.
#
# WHY THIS FUNCTION EXISTS AT ALL: a bare verdict ("billing, high priority") is
# something a reviewer has to verify from scratch. A verdict with its reasoning
# ("matched keywords: refund, invoice; extracted order ORD-4471") can be checked
# in seconds. For a system whose whole safety model rests on humans reviewing
# quickly, that difference is the difference between review being real and being
# a rubber stamp.
#
# It also sets the standard the AI must meet: the AI's results carry a `reasons`
# list too, precisely so the two remain comparable.
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
    # Always explains the category, INCLUDING when nothing matched. Saying "no
    # keywords matched" is genuinely more useful than silence, because it tells
    # the reviewer the classifier had nothing to go on rather than that it
    # positively concluded "other".
    if matched_category_terms:
        reasons.append(
            f"Category '{category}' matched keywords: {', '.join(matched_category_terms)}."
        )
    else:
        reasons.append("No specific category keywords matched, so category is 'other'.")

    # These two only appear when there is something to report, keeping routine
    # explanations short.
    if order_ids:
        reasons.append(f"Extracted order IDs: {', '.join(order_ids)}.")
    if amounts:
        reasons.append(f"Extracted money amounts: {', '.join(amounts)}.")

    # The priority explanation has three branches, mirroring the three ways
    # _determine_priority can reach its answer — so the stated reason always
    # matches the rule that actually fired.
    if high_priority_terms:
        reasons.append(f"Priority '{priority}' matched terms: {', '.join(high_priority_terms)}.")
    elif priority == "high":
        # Reached only via the billing-with-order-data rule.
        reasons.append("Priority 'high' was assigned because billing context included order data.")
    else:
        reasons.append(f"Priority '{priority}' was assigned by baseline rules.")

    # Last, so it is the final thing read — the most consequential conclusion
    # sits closest to the reviewer's decision.
    if requires_escalation:
        reasons.append("Human escalation is required because security-risk terms were found.")

    return reasons
