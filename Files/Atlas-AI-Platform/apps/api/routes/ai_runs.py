"""Read-only API endpoints for AI run audit records.

An `AIRun` is the persisted ledger row for one model gateway request. Reviewers
can use this route to inspect request/response metadata, token counts, cost, and
trace ids without reading provider-specific code.

Python notes for .NET reviewers:
- `BaseModel` is Pydantic's validated DTO base class.
- `UUID | None` is a nullable UUID type hint, similar to `Guid?`.
- `@router.get(...)` is a decorator that registers the function as an endpoint.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from packages.core.errors import NotFoundError
from packages.db.models.model_gateway import AIRun
from packages.db.session import get_db_session

router = APIRouter(prefix="/ai-runs", tags=["ai-runs"])


class AIRunPayload(BaseModel):
    """Response DTO for persisted model execution metadata."""

    id: UUID
    tenant_id: UUID
    user_id: UUID | None
    use_case: str
    provider_name: str
    model_name: str
    model_route_id: UUID | None
    prompt_version_id: UUID | None
    request_hash: str
    input_preview: str | None
    output_preview: str | None
    request_json: dict[str, object] | None
    response_json: dict[str, object] | None
    status: str
    error_code: str | None
    error_message: str | None
    input_tokens: int | None
    output_tokens: int | None
    reasoning_output_tokens: int | None
    cache_creation_input_tokens: int | None
    cache_read_input_tokens: int | None
    estimated_cost_usd: Decimal | None
    latency_ms: int | None
    trace_id: str | None


@router.get("/{ai_run_id}", response_model=AIRunPayload)
def get_ai_run(
    ai_run_id: UUID,
    session: Annotated[Session, Depends(get_db_session)],
) -> AIRunPayload:
    """Return one persisted AI run by id.

    `Annotated[Session, Depends(...)]` declares dependency injection. FastAPI
    calls `get_db_session()` and passes the yielded Session, similar to a scoped
    EF `DbContext` resolved from ASP.NET Core DI.
    """
    ai_run = session.get(AIRun, ai_run_id)
    if ai_run is None:
        raise NotFoundError(message="AI run not found.", details={"ai_run_id": str(ai_run_id)})
    # The API shape is explicit instead of returning the ORM row directly, which
    # keeps database-only columns from accidentally becoming part of the contract.
    return AIRunPayload(
        id=ai_run.id,
        tenant_id=ai_run.tenant_id,
        user_id=ai_run.user_id,
        use_case=ai_run.use_case,
        provider_name=ai_run.provider_name,
        model_name=ai_run.model_name,
        model_route_id=ai_run.model_route_id,
        prompt_version_id=ai_run.prompt_version_id,
        request_hash=ai_run.request_hash,
        input_preview=ai_run.input_preview,
        output_preview=ai_run.output_preview,
        request_json=ai_run.request_json,
        response_json=ai_run.response_json,
        status=ai_run.status,
        error_code=ai_run.error_code,
        error_message=ai_run.error_message,
        input_tokens=ai_run.input_tokens,
        output_tokens=ai_run.output_tokens,
        reasoning_output_tokens=ai_run.reasoning_output_tokens,
        cache_creation_input_tokens=ai_run.cache_creation_input_tokens,
        cache_read_input_tokens=ai_run.cache_read_input_tokens,
        estimated_cost_usd=ai_run.estimated_cost_usd,
        latency_ms=ai_run.latency_ms,
        trace_id=ai_run.trace_id,
    )
