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

TEMPLATE_DIR = Path(__file__).parent / "templates"


@dataclass(frozen=True)
class PromptSpec:
    name: str
    version: str
    template_path: str
    output_schema: type[BaseModel]
    required_variables: tuple[str, ...]
    changelog: str

    @property
    def prompt_id(self) -> str:
        return f"{self.name}.v{self.version}"


PROMPTS: tuple[PromptSpec, ...] = (
    PromptSpec(
        name="classify_ticket",
        version="1",
        template_path="classify_ticket.v1.md",
        output_schema=TicketClassification,
        required_variables=("ticket_subject", "ticket_body", "customer_id", "policy_context"),
        changelog="Initial classification prompt contract.",
    ),
    PromptSpec(
        name="extract_fields",
        version="1",
        template_path="extract_fields.v1.md",
        output_schema=TicketFieldExtraction,
        required_variables=("ticket_subject", "ticket_body", "customer_id", "policy_context"),
        changelog="Initial field extraction prompt contract.",
    ),
    PromptSpec(
        name="recommend_priority",
        version="1",
        template_path="recommend_priority.v1.md",
        output_schema=PriorityRecommendation,
        required_variables=("ticket_subject", "ticket_body", "customer_id", "policy_context"),
        changelog="Initial priority recommendation prompt contract.",
    ),
    PromptSpec(
        name="draft_response",
        version="1",
        template_path="draft_response.v1.md",
        output_schema=DraftResponse,
        required_variables=("ticket_subject", "ticket_body", "customer_id", "policy_context"),
        changelog="Initial draft response prompt contract.",
    ),
    PromptSpec(
        name="safety_check",
        version="1",
        template_path="safety_check.v1.md",
        output_schema=SafetyCheck,
        required_variables=("ticket_subject", "ticket_body", "customer_id", "policy_context"),
        changelog="Initial safety check prompt contract.",
    ),
    PromptSpec(
        name="full_ticket_analysis",
        version="1",
        template_path="full_ticket_analysis.v1.md",
        output_schema=FullTicketAnalysis,
        required_variables=("ticket_subject", "ticket_body", "customer_id", "policy_context"),
        changelog="Initial full ticket analysis prompt contract for hosted providers.",
    ),
)


def list_prompts() -> list[PromptSpec]:
    return list(PROMPTS)


def get_prompt(name: str, version: str = "1") -> PromptSpec:
    for prompt in PROMPTS:
        if prompt.name == name and prompt.version == version:
            return prompt
    raise KeyError(f"unknown prompt: {name}.v{version}")


def render_prompt(name: str, variables: dict[str, str], version: str = "1") -> str:
    prompt = get_prompt(name, version=version)
    missing = sorted(set(prompt.required_variables) - set(variables))
    if missing:
        raise KeyError(f"missing prompt variables: {', '.join(missing)}")

    template_text = (TEMPLATE_DIR / prompt.template_path).read_text(encoding="utf-8")
    output_schema = json.dumps(
        prompt.output_schema.model_json_schema(),
        indent=2,
        sort_keys=True,
    )
    return Template(template_text).substitute(
        **variables,
        prompt_id=prompt.prompt_id,
        output_schema=output_schema,
    )
