"""Prompt-system value objects and JSON conversion helpers.

The dataclasses here are immutable DTOs used inside the prompt subsystem. They
separate domain contracts from SQLAlchemy ORM rows and FastAPI request models.

Python notes for .NET reviewers:
- `frozenset(...)` creates an immutable set.
- `@dataclass(frozen=True)` creates record-like objects that cannot be mutated.
- `Any` means the value is intentionally dynamic, similar to `object` with less
  static checking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Literal
from uuid import UUID

from packages.model_gateway.types import ChatMessage

RATIFIED_USE_CASES = frozenset(
    {"chat", "classification", "rag_answer", "embedding", "llm_judge"}
)
RESERVED_USE_CASES = frozenset(
    # Reserved names let future phases define prompts without changing the
    # database contract or accepting arbitrary free-form use-case strings.
    {
        "query_rewrite",
        "structured_extraction",
        "agent_planning",
        "agent_verification",
        "safety_check",
        "summarization",
        "voice_summary",
        "multimodal_extraction",
    }
)
KNOWN_PROMPT_USE_CASES = RATIFIED_USE_CASES | RESERVED_USE_CASES

PromptVersionStatus = Literal["draft", "testing", "approved", "active", "retired"]
PromptTemplateStatus = Literal["active", "archived"]
PromptActorType = Literal["user", "system", "optimizer"]
PromptResolution = Literal["tenant", "global", "pinned"]
PromptTestCaseType = Literal["happy_path", "edge_case", "adversarial", "format", "regression"]
PromptTestOutcome = Literal["passed", "failed", "error", "needs_review"]


@dataclass(frozen=True, slots=True)
class VariableDeclaration:
    """One variable a prompt template expects at render time."""

    name: str
    required: bool
    trusted: bool
    description: str | None = None
    max_tokens: int | None = None


@dataclass(frozen=True, slots=True)
class ModelDefaults:
    temperature: Decimal | None = None
    max_output_tokens: int | None = None
    route_key: str | None = None


@dataclass(frozen=True, slots=True)
class PromptVersionSpec:
    id: UUID
    prompt_template_id: UUID
    tenant_id: UUID | None
    template_name: str
    use_case: str
    version_number: int
    system_prompt: str
    user_template: str
    input_variables: tuple[VariableDeclaration, ...]
    output_schema: dict[str, Any] | None
    model_defaults: ModelDefaults
    status: str
    created_by_user_id: UUID | None
    created_by_actor_type: str


@dataclass(frozen=True, slots=True)
class ResolvedPromptVersion:
    version: PromptVersionSpec
    resolution: PromptResolution
    cache_hit: bool = False


@dataclass(frozen=True, slots=True)
class RenderedPrompt:
    """Rendered chat messages plus attribution back to the prompt version used."""

    messages: tuple[ChatMessage, ...]
    prompt_version_id: UUID
    prompt_name: str
    prompt_version_number: int
    prompt_template_id: UUID
    use_case: str
    resolution: PromptResolution
    cache_hit: bool
    model_defaults: ModelDefaults
    render_hash: str
    estimated_input_tokens: int


@dataclass(frozen=True, slots=True)
class CheckResult:
    check: str
    result: Literal["passed", "failed"]
    argument: Any | None = None
    message: str | None = None


@dataclass(frozen=True, slots=True)
class PromptTestResult:
    case_id: UUID
    case_name: str
    case_type: str
    outcome: PromptTestOutcome
    ai_run_id: UUID | None = None
    output_preview: str | None = None
    checks: tuple[CheckResult, ...] = ()
    duration_ms: int = 0
    error_code: str | None = None
    error_message: str | None = None
    baseline_outcome: PromptTestOutcome | None = None


@dataclass(frozen=True, slots=True)
class PromptTestSummary:
    prompt_version_id: UUID
    version_number: int
    baseline_version_id: UUID | None
    baseline_version_number: int | None
    provider_mode: Literal["mock", "provider"]
    total: int
    passed: int
    failed: int
    error: int
    needs_review: int
    regressions: int
    fixed: int
    results: tuple[PromptTestResult, ...] = field(default_factory=tuple)


def variable_declaration_from_json(value: dict[str, Any]) -> VariableDeclaration:
    """Rehydrate one variable declaration from PostgreSQL JSONB data."""
    return VariableDeclaration(
        name=str(value["name"]),
        required=bool(value["required"]),
        trusted=bool(value["trusted"]),
        description=str(value["description"]) if value.get("description") is not None else None,
        max_tokens=int(value["max_tokens"]) if value.get("max_tokens") is not None else None,
    )


def model_defaults_from_json(value: dict[str, Any] | None) -> ModelDefaults:
    """Rehydrate persisted JSON into typed model defaults."""
    value = value or {}
    raw_temperature = value.get("temperature")
    temperature = Decimal(str(raw_temperature)) if raw_temperature is not None else None
    raw_max_output_tokens = value.get("max_output_tokens")
    max_output_tokens = (
        int(raw_max_output_tokens) if raw_max_output_tokens is not None else None
    )
    raw_route_key = value.get("route_key")
    return ModelDefaults(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        route_key=str(raw_route_key) if raw_route_key is not None else None,
    )


def model_defaults_to_json(value: ModelDefaults) -> dict[str, Any]:
    return {
        "temperature": str(value.temperature) if value.temperature is not None else None,
        "max_output_tokens": value.max_output_tokens,
        "route_key": value.route_key,
    }


def variable_declaration_to_json(value: VariableDeclaration) -> dict[str, Any]:
    """Serialize a variable declaration to JSON-safe primitives for storage."""
    return {
        "name": value.name,
        "required": value.required,
        "trusted": value.trusted,
        "description": value.description,
        "max_tokens": value.max_tokens,
    }
