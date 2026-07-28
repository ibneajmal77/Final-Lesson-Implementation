# ============================================================================
# FILE: packages/prompts/supportops_prompts/schemas.py
#
# THINK OF THIS FILE AS: the exact shape the AI's answer is required to take.
#
# WHY THIS FILE IS MORE IMPORTANT THAN IT LOOKS:
#   A language model, left to itself, replies in prose. You ask for a category
#   and get "This appears to be a billing issue, though it could also relate to
#   delivery." That is unusable — it cannot be stored in a column, counted in a
#   report, or acted on by code.
#
#   These classes are how that is prevented, and they are used TWICE for the same
#   definition:
#     1. BEFORE the call — registry.py converts them into a JSON description that
#        is embedded in the prompt, and providers/hosted.py sends the same
#        description to the API with "strict" mode on, so the service ENFORCES it
#        during generation.
#     2. AFTER the call — providers/hosted.py validates the reply against them
#        again.
#
#   One definition, used to ask and to check. They cannot drift apart, which is
#   the entire point of generating rather than hand-writing the description.
#
# THE SIX CLASSES:
#   The first five each describe one step's output. FullTicketAnalysis at the
#   bottom combines them into the single-call version, which is the one actually
#   in use.
#
# THREE DESIGN CHOICES WORTH NOTICING as you read:
#   - Literal types, so a category is one of six values and never free text
#   - `extra="forbid"`, so an invented field is a hard failure
#   - Explicit "I don't know" fields (abstain, missing_information), so the model
#     has an honest way out instead of being forced to guess
# ============================================================================

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# THE FIXED VOCABULARIES. `Literal` means the value must be EXACTLY one of these
# strings — not merely a string.
#
# This is what makes the results countable. If the model could return "billing",
# "Billing", "billing issue", and "payment/billing" freely, the reports counting
# by category would silently split one real category into four, and every
# per-category figure would be wrong in an unnoticeable way.
#
# Note these mirror the categories in the keyword classifier
# (packages/domain/.../baseline.py) exactly. That is deliberate and necessary:
# the two are compared against each other in the metrics, which would be
# meaningless if they used different vocabularies.
TicketCategory = Literal[
    "security",
    "billing",
    "account_access",
    "delivery",
    "technical_issue",
    "other",              # the honest fallback, so the model is never forced to
                          # squeeze an odd ticket into a category that does not fit
]

TicketPriority = Literal["low", "normal", "high", "urgent"]

# Things the model should raise a hand about.
RiskFlag = Literal[
    "prompt_injection",   # the ticket text tries to hijack the AI's instructions
    "pii",                # personal data is present that needs careful handling
    "payment_risk",
    "security_risk",
    "policy_gap",         # no company rule covers this situation
    "none",               # explicitly nothing. Included so "no risks" is a positive
                          # statement rather than an empty list, which could equally
                          # mean the model simply forgot to check
]


# The shared parent of every schema below.
#
# `extra="forbid"` is the whole reason it exists, and it is a strict choice. By
# default Pydantic IGNORES unexpected fields; this makes them a hard error.
#
# Why be that strict with an AI's output: an unexpected field means the model did
# not follow the contract. Perhaps it hallucinated a "confidence_level" alongside
# the real "category_confidence" — and if the extra one were silently dropped,
# the reply would look valid while the model was demonstrably not doing as told.
# Better to reject and find out.
class StrictPromptModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


# --- Step 1: what is this ticket about? ------------------------------------
class TicketClassification(StrictPromptModel):
    category: TicketCategory
    # `ge=0, le=1` means "greater or equal to 0, less or equal to 1". Without
    # these bounds a model could return 95 meaning 95%, and downstream code
    # treating it as a 0-1 fraction would read it as 9500% confidence.
    category_confidence: float = Field(ge=0, le=1)

    # `min_length=1` forces an actual explanation — an empty string is refused.
    # The maximum stops a model that decides to write an essay, which would cost
    # real money in output tokens.
    rationale: str = Field(min_length=1, max_length=1000)

    # THE HONEST-UNCERTAINTY FIELDS, and among the most valuable things in this
    # file. They give the model a legitimate way to say "I don't know".
    #
    # Without them, a model asked for a category will always produce one, because
    # that is what it was asked for — including for a ticket that says only
    # "help". A confident wrong answer is considerably worse than an admission of
    # uncertainty, because nobody thinks to check it.
    #
    # `abstain` is read by apps/worker/jobs.py, which records the run as
    # "abstained" rather than "succeeded" — a distinct, honestly-labelled outcome.
    abstain: bool
    # What the model felt it needed. Often directly actionable: a human can
    # frequently supply exactly the missing piece.
    missing_information: list[str] = Field(default_factory=list)


# --- Step 2: pull the specifics out of the text ----------------------------
#
# All lists, all optional. A ticket may mention no order numbers at all, and
# `default_factory=list` gives each instance its own new empty list rather than
# one shared between them.
class TicketFieldExtraction(StrictPromptModel):
    order_ids: list[str] = Field(default_factory=list)
    amounts: list[str] = Field(default_factory=list)
    product_names: list[str] = Field(default_factory=list)
    account_identifiers: list[str] = Field(default_factory=list)

    # THE ANTI-HALLUCINATION FIELD. The model must state WHERE each extracted
    # value came from — "ticket-body", "ticket-subject", and so on.
    #
    # providers/hosted.py checks these against a fixed list of the four things
    # actually supplied, and rejects the whole response if the model cites
    # anything else. A fabricated source is strong evidence the model is
    # confabulating rather than reading, which makes its other conclusions
    # suspect too. See _validate_evidence_ids there.
    evidence_ids: list[str] = Field(default_factory=list)


# --- Step 3: how urgent is it? ---------------------------------------------
class PriorityRecommendation(StrictPromptModel):
    priority: TicketPriority
    requires_escalation: bool
    confidence: float = Field(ge=0, le=1)
    # `min_length=1` on a LIST means at least one item. So a priority decision
    # can never arrive unexplained — which matters, because a human reviewer
    # needs to judge it in seconds.
    reasons: list[str] = Field(min_length=1)


# --- Step 4: write the reply -----------------------------------------------
class DraftResponse(StrictPromptModel):
    # 5,000 characters, matching the limit in the API schema
    # (schemas/approvals.py) so an approved draft always fits the field a human
    # edits it in.
    response_text: str = Field(min_length=1, max_length=5000)
    tone: Literal["empathetic", "direct", "formal", "neutral"]

    # The model's own judgement that this one needs a careful look. Note EVERY
    # draft is reviewed by a human regardless — this is a hint about which
    # deserve more than a glance, not a switch that bypasses review.
    needs_human_review: bool

    # Anything the model believes it must NOT say — a refund it cannot authorise,
    # a delivery date it cannot promise. Useful to a reviewer, who can check the
    # draft honoured its own list.
    forbidden_claims: list[str] = Field(default_factory=list)


# --- Step 5: is any of this risky? -----------------------------------------
class SafetyCheck(StrictPromptModel):
    safe_to_draft: bool
    risk_flags: list[RiskFlag] = Field(default_factory=list)
    blocked_reasons: list[str] = Field(default_factory=list)
    pii_detected: bool      # flagged separately from the general risk list because it
                            # carries specific legal obligations, not just caution


# --- THE ONE ACTUALLY IN USE: all five steps in a single answer -------------
#
# Composed from the pieces above rather than repeating their fields, so the
# combined version and the individual ones can never disagree about what a
# field means.
class FullTicketAnalysis(StrictPromptModel):
    category: TicketCategory
    category_confidence: float = Field(ge=0, le=1)
    priority: TicketPriority
    requires_escalation: bool

    # A nested object — the whole extraction schema embedded as one field.
    extracted_fields: TicketFieldExtraction
    # Evidence at the top level too, for the overall conclusions rather than the
    # individual extracted values. hosted.py checks BOTH lists.
    evidence_ids: list[str] = Field(default_factory=list)

    # `| None` and — note carefully — NO DEFAULT. So the field must be present in
    # the reply, but is allowed to be null.
    #
    # That distinction is deliberate. The model must consciously decide "no draft"
    # and say so, rather than being able to omit the field and have a default
    # quietly fill in. It is null when the model abstains, or when the safety
    # check says drafting is not appropriate.
    draft_response: DraftResponse | None

    abstain: bool
    risk_flags: list[RiskFlag] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
