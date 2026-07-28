# ============================================================================
# FILE: packages/prompts/supportops_prompts/registry.py
#
# THINK OF THIS FILE AS: the catalogue of instructions the AI can be given —
# what each one is called, which version it is, and what shape of answer it must
# produce.
#
# WHAT A "PROMPT" IS HERE:
#   The written instructions sent to the AI along with the ticket. Not a casual
#   question — a carefully worded document telling the model what to do, what
#   rules to follow, and exactly what JSON to return. They live as .md files in
#   the templates/ folder next door.
#
# WHY PROMPTS ARE TREATED AS VERSIONED ARTEFACTS RATHER THAN STRINGS IN CODE:
#   A prompt IS the program, as far as an AI feature is concerned. Change a
#   sentence in it and every answer changes. So it needs the same discipline as
#   code:
#     - a NAME and a VERSION, recorded on every result it produces
#     - a declared OUTPUT SHAPE, so the answer can be validated
#     - a CHANGELOG saying why it exists
#
#   The payoff is explainability. When approval rates drop next month, the
#   `prompt_version` stored on every recommendation tells you exactly which
#   instructions produced the bad results — instead of a guess about what
#   changed.
#
# THE THREE PUBLIC FUNCTIONS:
#   list_prompts()  - everything in the catalogue
#   get_prompt()    - look one up by name and version
#   render_prompt() - fill a template in with a real ticket's details
#
# NOTE ONLY ONE OF THE SIX IS ACTUALLY USED at present: "full_ticket_analysis",
# called by providers/hosted.py. The other five are single-purpose prompts from
# an earlier design where each step ran separately. They remain as a working
# alternative, and the contrast is instructive — one big call is cheaper and
# faster, several small ones are easier to debug and to score individually.
# ============================================================================

import json
from dataclasses import dataclass
from pathlib import Path
from string import Template

from pydantic import BaseModel

from supportops_prompts.schemas import (
    DraftResponse,
    FullTicketAnalysis,
    PriorityRecommendation,
    SafetyCheck,
    TicketClassification,
    TicketFieldExtraction,
)

PROMPT_PACKAGE_VERSION = "0.1.0"

# `Path(__file__).parent` means "the folder this file is in", so the templates
# are found however the application is started and from whatever working
# directory. A relative path like "templates/" would break the moment something
# ran from elsewhere.
TEMPLATE_DIR = Path(__file__).parent / "templates"


# One catalogue entry: everything known about a single prompt.
@dataclass(frozen=True)
class PromptSpec:
    name: str
    version: str
    template_path: str              # the .md file holding the actual instructions
    output_schema: type[BaseModel]  # the SHAPE the answer must take. Note this holds the
                                    # class itself, not an instance — that is what
                                    # `type[BaseModel]` means
    required_variables: tuple[str, ...]   # placeholders the template needs filling in
    changelog: str                        # why this version exists

    # A property, read like a plain value: `spec.prompt_id`.
    #
    # This produces strings like "full_ticket_analysis.v1", and THIS is the value
    # stored in the prompt_version column on every recommendation. Computing it
    # from the name and version means the stored identifier can never disagree
    # with the catalogue entry that produced it.
    @property
    def prompt_id(self) -> str:
        return f"{self.name}.v{self.version}"


# THE CATALOGUE. Every prompt the system knows about.
#
# All six share the same four required variables, which is deliberate: any prompt
# can be swapped for another without the calling code changing what it passes in.
PROMPTS: tuple[PromptSpec, ...] = (
    # --- The five single-purpose prompts, from the earlier step-by-step design ---
    PromptSpec(
        name="classify_ticket",             # what is this ticket about?
        version="1",
        template_path="classify_ticket.v1.md",
        output_schema=TicketClassification,
        required_variables=("ticket_subject", "ticket_body", "customer_id", "policy_context"),
        changelog="Initial classification prompt contract.",
    ),
    PromptSpec(
        name="extract_fields",              # pull out order numbers, amounts, and so on
        version="1",
        template_path="extract_fields.v1.md",
        output_schema=TicketFieldExtraction,
        required_variables=("ticket_subject", "ticket_body", "customer_id", "policy_context"),
        changelog="Initial field extraction prompt contract.",
    ),
    PromptSpec(
        name="recommend_priority",          # how urgent is it?
        version="1",
        template_path="recommend_priority.v1.md",
        output_schema=PriorityRecommendation,
        required_variables=("ticket_subject", "ticket_body", "customer_id", "policy_context"),
        changelog="Initial priority recommendation prompt contract.",
    ),
    PromptSpec(
        name="draft_response",              # write the reply
        version="1",
        template_path="draft_response.v1.md",
        output_schema=DraftResponse,
        required_variables=("ticket_subject", "ticket_body", "customer_id", "policy_context"),
        changelog="Initial draft response prompt contract.",
    ),
    PromptSpec(
        name="safety_check",                # is any of this risky?
        version="1",
        template_path="safety_check.v1.md",
        output_schema=SafetyCheck,
        required_variables=("ticket_subject", "ticket_body", "customer_id", "policy_context"),
        changelog="Initial safety check prompt contract.",
    ),

    # --- THE ONE ACTUALLY IN USE: all five jobs in a single call ---
    #
    # Combining them trades some debuggability for a large saving. Five separate
    # calls would mean sending the ticket text five times over — paying for those
    # input tokens five times, and waiting five round trips. One call does it
    # once. For a per-ticket operation running at volume, that difference is the
    # whole cost model.
    PromptSpec(
        name="full_ticket_analysis",
        version="1",
        template_path="full_ticket_analysis.v1.md",
        output_schema=FullTicketAnalysis,
        required_variables=("ticket_subject", "ticket_body", "customer_id", "policy_context"),
        changelog="Initial full ticket analysis prompt contract for hosted providers.",
    ),
)


# Everything in the catalogue.
#
# Returns a `list(...)` COPY rather than the tuple itself — so a caller cannot
# hold on to and interfere with the real catalogue. Used by the tests in
# tests/prompts/, which check every registered prompt has a template file that
# actually exists.
def list_prompts() -> list[PromptSpec]:
    return list(PROMPTS)


# Looks up one prompt by name and version.
#
# `version="1"` as a default means callers can just say get_prompt("safety_check")
# today, while leaving room for a version 2 to be added and requested explicitly.
#
# Raises KeyError rather than returning None for an unknown name. The right
# choice: a missing prompt is a programming error, not a runtime condition to
# handle, and failing loudly beats a confusing None reaching the caller.
def get_prompt(name: str, version: str = "1") -> PromptSpec:
    for prompt in PROMPTS:
        if prompt.name == name and prompt.version == version:
            return prompt
    raise KeyError(f"unknown prompt: {name}.v{version}")


# THE MAIN FUNCTION: takes a template and a real ticket's details, and produces
# the finished text to send to the AI.
def render_prompt(name: str, variables: dict[str, str], version: str = "1") -> str:
    prompt = get_prompt(name, version=version)

    # CHECKS FOR MISSING VARIABLES FIRST, before touching the file.
    #
    # Worth doing explicitly rather than letting the substitution fail later: this
    # reports EVERY missing variable at once, sorted, whereas the substitution
    # would complain about only the first one and send you round the loop.
    #
    # It is also a safety measure. A prompt sent with an unfilled placeholder
    # would reach the model with a literal "$ticket_body" in it — producing a
    # confidently wrong analysis of nothing at all, which is far worse than a
    # clean failure.
    missing = sorted(set(prompt.required_variables) - set(variables))
    if missing:
        raise KeyError(f"missing prompt variables: {', '.join(missing)}")

    template_text = (TEMPLATE_DIR / prompt.template_path).read_text(encoding="utf-8")

    # THE CLEVER BIT: the required output shape is generated FROM the Pydantic
    # class and embedded into the prompt text.
    #
    # So the model is shown the exact JSON structure it must produce, and that
    # description is derived from the same class used to VALIDATE the answer
    # afterwards (in providers/hosted.py). One definition, used for both asking
    # and checking — they cannot drift apart.
    #
    # `sort_keys=True` keeps the generated text identical between runs, so the
    # prompt sent today matches the one sent yesterday. That matters more than it
    # sounds: an unstable prompt means results are not reproducible, and
    # comparing two evaluation runs becomes meaningless.
    output_schema = json.dumps(
        prompt.output_schema.model_json_schema(),
        indent=2,
        sort_keys=True,
    )

    # `Template` uses $variable placeholders and, importantly, `.substitute()`
    # RAISES on any placeholder it cannot fill — unlike `.safe_substitute()`,
    # which would quietly leave it in place. Failing here is exactly right, for
    # the reason given above.
    #
    # Two extra values are always supplied on top of the caller's: prompt_id and
    # output_schema, so every template can refer to them without every caller
    # having to remember.
    return Template(template_text).substitute(
        **variables,
        prompt_id=prompt.prompt_id,
        output_schema=output_schema,
    )
