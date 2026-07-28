# ============================================================================
# FILE: packages/model_gateway/supportops_model_gateway/providers/mock.py
#
# THINK OF THIS FILE AS: a stand-in for the AI. It honours the same contract as
# the real provider, but never touches the network and costs nothing.
#
# WHY A FAKE AI IS WORTH ITS OWN FILE:
#   1. THE TESTS RUN FREE AND OFFLINE. The entire test suite exercises the real
#      routes, the real worker, and the real database, with this in place of the
#      AI. No API key, no network, no bill, no rate limits.
#   2. IT IS DETERMINISTIC. Given the same ticket it returns the SAME answer,
#      every time. A real language model does not, which makes it useless as a
#      thing to write assertions against.
#   3. LOCAL DEVELOPMENT WORKS OUT OF THE BOX. `model_provider` defaults to
#      "mock" in settings.py, so someone cloning this project can run the whole
#      system without signing up for anything.
#
# HOW IT PRETENDS:
#   It runs the free keyword classifier from packages/domain/, then dresses the
#   result up in the shape a real AI would return — inventing a summary and a
#   draft reply from templates chosen by category.
#
#   Crucially, the replies are HONEST-LOOKING BUT GENERIC. They say "I will look
#   into this" rather than answering anything, which is the right choice for a
#   fake: it is obviously placeholder text if it ever escaped into production,
#   rather than something that could be mistaken for real advice.
#
# THE TELLTALE FIELDS, so mock output is always identifiable in the database:
#   source = "mock_llm_v1", model_name = "mock-ticket-analyzer". Any metrics
#   report can filter these out — and if they ever show up in a production
#   report, that itself is the alarm.
# ============================================================================

from supportops_domain.services.baseline import BaselineTicketInput, classify_ticket
from supportops_model_gateway.providers.base import TicketAnalysisInput, TicketAnalysisResult

MOCK_PROVIDER_NAME = "mock"                          # the setting value that selects this
MOCK_SOURCE = "mock_llm_v1"                          # recorded on every result it produces
MOCK_MODEL_NAME = "mock-ticket-analyzer"
PROMPT_VERSION = "supportops_ticket_analysis_v1"     # a pretend version, so the field is
                                                     # never empty and downstream code that
                                                     # expects a value still works


class MockTicketAnalysisProvider:
    # The same single method the real provider implements. Note it does not
    # inherit from anything — the Protocol in base.py describes a shape, not a
    # base class, so simply having this method is enough.
    def analyze_ticket(self, ticket: TicketAnalysisInput) -> TicketAnalysisResult:
        # The "thinking" is entirely the free keyword classifier.
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

            # A small, knowing joke: the mock claims to be slightly MORE confident
            # than the keyword rules it is secretly using, capped at 0.9.
            #
            # It serves a real purpose beyond humour. If confidence were passed
            # through unchanged, mock results would be numerically identical to
            # baseline results, and a test meant to distinguish "the AI path" from
            # "the baseline path" could pass while actually comparing nothing. The
            # small offset keeps them distinguishable.
            #
            # The 0.9 cap is the sensible touch: never claim certainty.
            confidence=min(baseline.confidence + 0.05, 0.9),

            summary=summary,
            suggested_reply=suggested_reply,
            extracted_fields={
                # `**` copies everything from the baseline's findings into this
                # new dictionary, then the two lines below are added on top.
                **baseline.extracted_fields,
                "customer_id": ticket.customer_id,
                "provider": MOCK_PROVIDER_NAME,      # the label marking this as fake
            },
            reasons=[
                # The first reason states plainly what this is. Anyone reading a
                # draft in the UI can see immediately that no real AI was involved
                # — which is exactly what you want from a stand-in.
                "Mock provider used deterministic baseline analysis.",
                *baseline.reasons,
            ],
            # Note it does NOT set input_tokens, output_tokens, or latency_ms.
            # They default to zero, which is honest: nothing was spent and nothing
            # was waited for. Inventing plausible-looking numbers would quietly
            # corrupt the cost reports with fictional spending.
        )


# ===========================================================================
# THE TEMPLATE TEXT
#
# Everything below simply picks a sentence based on the category. There is no
# intelligence here at all, and that is the point.
# ===========================================================================


# Builds a one-line summary, mentioning an order number if the classifier found one.
def _summary_for_category(
    *,
    category: str,
    priority: str,
    extracted_fields: dict[str, object],
) -> str:
    order_ids = _string_list(extracted_fields.get("order_ids"))
    # The conditional expression means the phrase only appears when there is
    # actually an order to mention — otherwise you would get an awkward dangling
    # "involving order ." at the end.
    order_text = f" involving order {', '.join(order_ids)}" if order_ids else ""
    return f"Customer reported a {priority} priority {category} issue{order_text}."


# Picks a draft reply based on the category.
#
# NOTE THE ORDER OF THE CHECKS. Escalation is tested FIRST, before any category,
# which means an escalated billing ticket gets the escalation reply rather than
# the billing one. That is the correct priority: "a specialist is taking this
# over" is more important for the customer to hear than the subject matter, and
# it also mirrors how the real prompt is expected to behave.
#
# Every reply is deliberately non-committal — "I will review", "I will check".
# None of them promise anything, quote a policy, or state a fact that could be
# wrong. Exactly right for placeholder text.
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

    # Checked first — see the note above.
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
    # The catch-all, for a category with no specific template — including
    # "unknown" from the classifier. Having a fallback means a new category can
    # be added to the classifier without breaking this file.
    return (
        "Thanks for reaching out. I will review your request and make sure it is routed to the "
        "right support path."
    )


# Safely pulls a list of strings out of the loosely-typed extracted_fields bag.
#
# Two layers of checking, because that dictionary is declared as holding
# `object` values and could in principle contain anything. The list
# comprehension filters out any non-string entries rather than letting one
# reach a `', '.join(...)` call, which would fail on a non-string item.
def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]
