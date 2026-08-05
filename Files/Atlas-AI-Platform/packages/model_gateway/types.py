"""Typed contracts shared by gateway routers, providers, and API routes.

These frozen dataclasses act like immutable C# record types: they move data
between layers without bringing in ORM behavior or HTTP framework concerns.

Python notes for .NET reviewers:
- `Literal[...]` restricts a string type hint to known values.
- `tuple[T, ...]` means an immutable sequence of zero or more `T` values.
- `field(default_factory=...)` creates a fresh default object per instance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Literal
from uuid import UUID

UseCase = Literal["chat", "classification", "rag_answer", "embedding", "llm_judge"]
"""Allowed gateway use cases. Static checking catches misspelled known strings."""
ProviderType = Literal[
    "openai_compatible",
    "anthropic_compatible",
    "azure_openai",
    "local_vllm",
    "local_tgi",
    "mock",
]
RunStatus = Literal["queued", "running", "succeeded", "failed", "cancelled", "blocked"]
FinishReason = Literal["stop", "length", "content_filter", "tool_calls", "error"]


@dataclass(frozen=True, slots=True)
class ChatMessage:
    """One role/content message sent to a chat model."""

    role: Literal["system", "user", "assistant", "tool"]
    content: str


@dataclass(frozen=True, slots=True)
class ModelRequest:
    """Internal request object accepted by the gateway facade."""

    tenant_id: UUID
    use_case: UseCase
    messages: tuple[ChatMessage, ...] = ()
    inputs: tuple[str, ...] = ()
    user_id: UUID | None = None
    prompt_version_id: UUID | None = None
    prompt_name: str | None = None
    prompt_version_number: int | None = None
    prompt_template_id: UUID | None = None
    prompt_resolution: Literal["tenant", "global", "pinned"] | None = None
    prompt_cache_hit: bool | None = None
    restricted_data: bool = False
    max_cost_usd: Decimal | None = None
    trace_id: str | None = None
    granted_permissions: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class TokenUsage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    reasoning_output_tokens: int | None = None
    cache_creation_input_tokens: int | None = None
    cache_read_input_tokens: int | None = None


@dataclass(frozen=True, slots=True)
class ProviderChatResponse:
    """Provider adapter result for chat/completion calls."""

    content: str
    usage: TokenUsage
    finish_reason: FinishReason = "stop"
    # `default_factory=dict` avoids sharing one mutable dictionary across all
    # instances, a common Python pitfall.
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ProviderEmbeddingResponse:
    embeddings: tuple[tuple[float, ...], ...]
    usage: TokenUsage
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class GatewayResponse:
    ai_run_id: UUID
    use_case: UseCase
    provider_name: str
    model_name: str
    route_key: str
    status: RunStatus
    content: str | None = None
    embeddings: tuple[tuple[float, ...], ...] = ()
    finish_reason: FinishReason | None = None
    usage: TokenUsage = field(default_factory=TokenUsage)
    estimated_cost_usd: Decimal | None = None
    latency_ms: int | None = None
    trace_id: str | None = None
    observability_attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class SelectedRoute:
    """Route row plus provider policy, converted out of the ORM model."""

    route_id: UUID
    route_key: str
    use_case: UseCase
    provider_name: str
    provider_type: ProviderType
    model_name: str
    max_input_tokens: int
    max_output_tokens: int
    timeout_seconds: int
    temperature: Decimal | None
    restricted_data_allowed: bool
    fallback_route_id: UUID | None
    route_config: dict[str, Any]
    capabilities: dict[str, Any]
    data_policy: dict[str, Any]
    max_cost_usd: Decimal | None
    embedding_dimension: int | None


@dataclass(frozen=True, slots=True)
class RouteDecision:
    selected: SelectedRoute | None
    rejected_routes: tuple[dict[str, Any], ...]
    error_code: str | None = None
    error_message: str | None = None


@dataclass(frozen=True, slots=True)
class CostLine:
    billing_unit: str
    quantity: Decimal
    unit_cost_usd: Decimal
    estimated_cost_usd: Decimal
    pricing_version: str
