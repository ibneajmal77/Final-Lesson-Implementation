# ============================================================================
# FILE: packages/model_gateway/supportops_model_gateway/providers/base.py
#
# THINK OF THIS FILE AS: the contract every AI provider must honour. It defines
# what goes IN to an analysis and what must come OUT — and nothing else.
#
# THE IDEA THIS FILE EXISTS TO SERVE:
#   The rest of the application must never know which AI service it is talking
#   to. It sends a TicketAnalysisInput, it gets back a TicketAnalysisResult, and
#   whether that came from a paid model or a hard-coded fake is invisible to it.
#
#   That indirection buys three concrete things:
#     1. TESTS RUN FREE AND FAST. The mock provider satisfies this contract with
#        canned answers, so the whole application can be tested with no API key,
#        no network, and no bill.
#     2. SWITCHING PROVIDERS IS ONE SETTING. Changing model_provider is the whole
#        change; no route or worker code is touched.
#     3. THE BLAST RADIUS IS SMALL. Everything specific to one AI service is
#        confined to one file in this folder.
#
# THE THREE FILES THAT IMPLEMENT OR USE THIS:
#   providers/mock.py   - the fake, for tests and local development
#   providers/hosted.py - the real one, calling a paid service
#   routing.py          - picks between them based on settings
#
# NOTE THIS FILE CONTAINS NO LOGIC AT ALL. Just shapes and a contract. That is
# what makes it safe for everything else to depend on.
# ============================================================================

from dataclasses import dataclass
from typing import Protocol


# --- WHAT GOES IN ----------------------------------------------------------
#
# Everything the AI needs to analyse one ticket. Note what is ABSENT: no
# tenant_id, no ticket_id, no database objects. Only the text itself.
#
# That is deliberate. A provider should not be able to reach into the database
# or make decisions based on which customer this is — it takes text and returns
# an analysis. Keeping the input this narrow is what makes providers simple to
# write, simple to test, and impossible to entangle with the rest of the system.
@dataclass(frozen=True)
class TicketAnalysisInput:
    subject: str
    body: str
    customer_id: str | None = None    # optional; some tickets have no registered customer

    # The company's own written rules, gathered by tenant_policy_context() in
    # repositories/policies.py and pasted into the AI's instructions.
    #
    # Defaults to an empty string so a provider can be called without it — which
    # the tests rely on. In production it is always supplied.
    policy_context: str = ""


# --- WHAT MUST COME OUT ----------------------------------------------------
#
# The result every provider must return, whatever service it used underneath.
# Three groups of fields: where it came from, what it decided, and what it cost.
@dataclass(frozen=True)
class TicketAnalysisResult:
    # --- Group 1: provenance. Where did this answer come from? ---
    #
    # All three are required, and that is a deliberate discipline. When quality
    # shifts — better or worse — these are what let you explain it. An answer
    # with no record of which model and which prompt produced it is an answer
    # you cannot learn anything from.
    source: str            # the provider's name, e.g. "mock" or "openai"
    model_name: str        # the specific model
    prompt_version: str    # which version of OUR instructions it was given

    # --- Group 2: the judgement itself ---
    category: str                  # billing / technical / account...
    priority: str                  # low / medium / high
    requires_escalation: bool      # does a human specialist need to take over?
    confidence: float              # 0.0 to 1.0. A hint, not a guarantee — language
                                   # models are well known for being confidently wrong
    summary: str                   # a short recap of the customer's problem
    suggested_reply: str           # the draft reply. Never sent to anyone until a human
                                   # approves it in routes/approvals.py
    extracted_fields: dict[str, object]   # structured details found in the text: an order
                                          # number, a date, an error code. A dictionary
                                          # because what is worth extracting differs
                                          # completely between ticket types.
                                          # ALSO carries the "abstain" flag the worker
                                          # checks — see apps/worker/jobs.py
    reasons: list[str]             # WHY it decided this, in plain sentences. Arguably the
                                   # most important field for the humans doing reviews:
                                   # a verdict with no reasoning is hard to trust quickly

    # --- Group 3: what it cost. All optional, defaulting to zero ---
    #
    # Optional because the mock provider has no real cost and no real timing, and
    # forcing it to invent values would be dishonest. Zero reads correctly as
    # "nothing was spent".
    #
    # For real providers these are filled from the AI service's own response,
    # which is what makes the cost tracking in cost_events accurate rather than
    # estimated from our side.
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: int = 0
    raw_response_id: str | None = None   # the provider's own ID for this call. Worth
                                         # keeping: when you need to raise a support
                                         # ticket with the AI vendor about a bad answer,
                                         # this is what identifies it on their side


# --- THE CONTRACT ----------------------------------------------------------
#
# A "Protocol" describes a shape rather than demanding inheritance: anything with
# a method that looks like this counts as a TicketAnalysisProvider, whether or
# not it knows this class exists.
#
# The practical effect is that a test can define a tiny throwaway class with one
# `analyze_ticket` method and pass it straight in — no imports from here, no base
# class to inherit. That is the pattern used in
# tests/model_gateway/test_ticket_analysis_provider.py.
#
# The whole contract is ONE method. Deliberately minimal: the smaller the
# interface, the less there is for a new provider to get wrong.
class TicketAnalysisProvider(Protocol):
    def analyze_ticket(self, ticket: TicketAnalysisInput) -> TicketAnalysisResult:
        """Analyze a support ticket and return structured output."""
