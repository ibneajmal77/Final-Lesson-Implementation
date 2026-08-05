"""HTTP API for model gateway chat, embedding, and route inspection.

FastAPI models below are request/response DTOs. They convert JSON payloads into
the internal dataclass contracts used by `packages.model_gateway`.

Python notes for .NET reviewers:
- `@router.post(...)` and `@router.get(...)` are decorators, similar in purpose
  to ASP.NET route attributes.
- `BaseModel` classes are Pydantic models, similar to validated request/response
  DTOs.
- `UUID | None` means a nullable UUID.
- `list[ChatMessagePayload]` is Python's generic-list type hint.
"""

from __future__ import annotations

from dataclasses import asdict
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from packages.db.session import get_db_session
from packages.model_gateway.bootstrap import ensure_default_gateway_config
from packages.model_gateway.client import ModelGateway
from packages.model_gateway.router import ModelRouter
from packages.model_gateway.types import ChatMessage, ModelRequest, UseCase

router = APIRouter(prefix="/model-gateway", tags=["model-gateway"])


class ChatMessagePayload(BaseModel):
    """External JSON shape for one chat message."""

    role: Literal["system", "user", "assistant", "tool"]
    # `Field(min_length=1)` adds runtime validation, like a data annotation.
    content: str = Field(min_length=1)


class GatewayChatRequest(BaseModel):
    """Request DTO for chat/completion calls."""

    tenant_id: UUID
    user_id: UUID | None = None
    use_case: UseCase = "chat"
    messages: list[ChatMessagePayload] = Field(min_length=1)
    restricted_data: bool = False
    max_cost_usd: Decimal | None = None
    prompt_version_id: UUID | None = None


class GatewayEmbedRequest(BaseModel):
    """Request DTO for embedding calls."""

    tenant_id: UUID
    user_id: UUID | None = None
    use_case: Literal["embedding"] = "embedding"
    inputs: list[str] = Field(min_length=1)
    restricted_data: bool = False
    max_cost_usd: Decimal | None = None
    prompt_version_id: UUID | None = None


class UsagePayload(BaseModel):
    """Token usage DTO nested inside gateway responses."""

    input_tokens: int | None
    output_tokens: int | None
    reasoning_output_tokens: int | None
    cache_creation_input_tokens: int | None
    cache_read_input_tokens: int | None


class GatewayChatResponse(BaseModel):
    ai_run_id: UUID
    use_case: UseCase
    provider_name: str
    model_name: str
    route_key: str
    status: str
    content: str
    finish_reason: str | None
    usage: UsagePayload
    estimated_cost_usd: Decimal | None
    latency_ms: int | None
    trace_id: str | None
    observability_attributes: dict[str, object]


class GatewayEmbedResponse(BaseModel):
    ai_run_id: UUID
    use_case: Literal["embedding"]
    provider_name: str
    model_name: str
    route_key: str
    status: str
    embeddings: list[list[float]]
    usage: UsagePayload
    estimated_cost_usd: Decimal | None
    latency_ms: int | None
    trace_id: str | None
    observability_attributes: dict[str, object]


class RoutePayload(BaseModel):
    route_id: UUID
    route_key: str
    use_case: str
    provider_name: str
    provider_type: str
    model_name: str
    max_input_tokens: int
    max_output_tokens: int
    timeout_seconds: int
    restricted_data_allowed: bool
    max_cost_usd: Decimal | None
    embedding_dimension: int | None


@router.post("/chat", response_model=GatewayChatResponse)
def chat(
    payload: GatewayChatRequest,
    session: Annotated[Session, Depends(get_db_session)],
) -> GatewayChatResponse:
    """Execute a chat request through the gateway.

    `Depends(get_db_session)` is FastAPI dependency injection. It is comparable
    to asking ASP.NET Core DI for a scoped DbContext.
    """
    # The bootstrap makes local/dev and CI deterministic by seeding mock routes
    # before the request reaches the gateway selection logic.
    ensure_default_gateway_config(session)
    request = ModelRequest(
        tenant_id=payload.tenant_id,
        user_id=payload.user_id,
        use_case=payload.use_case,
        messages=tuple(
            # This generator expression converts API DTOs into immutable internal
            # dataclasses. It is like a LINQ projection into domain records.
            ChatMessage(role=message.role, content=message.content)
            for message in payload.messages
        ),
        restricted_data=payload.restricted_data,
        max_cost_usd=payload.max_cost_usd,
        prompt_version_id=payload.prompt_version_id,
    )
    response = ModelGateway(session).chat(request)
    return GatewayChatResponse(
        ai_run_id=response.ai_run_id,
        use_case=response.use_case,
        provider_name=response.provider_name,
        model_name=response.model_name,
        route_key=response.route_key,
        status=response.status,
        content=response.content or "",
        finish_reason=response.finish_reason,
        usage=UsagePayload(**asdict(response.usage)),
        estimated_cost_usd=response.estimated_cost_usd,
        latency_ms=response.latency_ms,
        trace_id=response.trace_id,
        observability_attributes=response.observability_attributes,
    )


@router.post("/embed", response_model=GatewayEmbedResponse)
def embed(
    payload: GatewayEmbedRequest,
    session: Annotated[Session, Depends(get_db_session)],
) -> GatewayEmbedResponse:
    ensure_default_gateway_config(session)
    # Convert list inputs from JSON to tuples for immutable internal contracts.
    request = ModelRequest(
        tenant_id=payload.tenant_id,
        user_id=payload.user_id,
        use_case=payload.use_case,
        inputs=tuple(payload.inputs),
        restricted_data=payload.restricted_data,
        max_cost_usd=payload.max_cost_usd,
        prompt_version_id=payload.prompt_version_id,
    )
    response = ModelGateway(session).embed(request)
    return GatewayEmbedResponse(
        ai_run_id=response.ai_run_id,
        use_case="embedding",
        provider_name=response.provider_name,
        model_name=response.model_name,
        route_key=response.route_key,
        status=response.status,
        embeddings=[list(vector) for vector in response.embeddings],
        usage=UsagePayload(**asdict(response.usage)),
        estimated_cost_usd=response.estimated_cost_usd,
        latency_ms=response.latency_ms,
        trace_id=response.trace_id,
        observability_attributes=response.observability_attributes,
    )


@router.get("/routes", response_model=list[RoutePayload])
def list_routes(
    session: Annotated[Session, Depends(get_db_session)],
) -> list[RoutePayload]:
    ensure_default_gateway_config(session)
    # This endpoint is an operational view of active provider/model routing, not
    # a mutating administration surface.
    return [
        RoutePayload(
            route_id=route.route_id,
            route_key=route.route_key,
            use_case=route.use_case,
            provider_name=route.provider_name,
            provider_type=route.provider_type,
            model_name=route.model_name,
            max_input_tokens=route.max_input_tokens,
            max_output_tokens=route.max_output_tokens,
            timeout_seconds=route.timeout_seconds,
            restricted_data_allowed=route.restricted_data_allowed,
            max_cost_usd=route.max_cost_usd,
            embedding_dimension=route.embedding_dimension,
        )
        for route in ModelRouter(session).list_routes()
    ]
