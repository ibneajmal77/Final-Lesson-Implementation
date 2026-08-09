"""Async model gateway: the same workflow as `client.py`, without blocking.

This is the async half of the deliberate sync/async pair. Read it beside
`client.py` — the two are meant to be compared.

What is shared, because it is pure and must never diverge:
  route selection policy   -> router.evaluate_candidates
  retry timing             -> retries.compute_backoff_delay
  capability gating        -> capabilities.ensure_route_supports
  redaction and previews   -> redaction.*
  cost lines               -> pricing.*
  telemetry attributes     -> observability.genai_attributes

What is written twice, because it is I/O and genuinely differs:
  session calls   `session.scalars(...)`  ->  `await session.scalars(...)`
  commits         `session.commit()`      ->  `await session.commit()`
  provider calls  blocking urllib         ->  awaited httpx
  retry waiting   `time.sleep`            ->  `await asyncio.sleep`

That last line is the one that matters. `time.sleep` inside a coroutine holds
the event loop for its whole duration, so a single retrying request would stall
every other request in the process. Ruff's ASYNC ruleset is enabled to catch
that class of mistake automatically.

Only chat is implemented here. Embeddings stay on the sync path on purpose: the
async version earns its complexity on long provider waits, and there is no
reason to duplicate a code path that gains nothing from it.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Mapping
from typing import Any, NoReturn

from sqlalchemy.ext.asyncio import AsyncSession

from packages.core.request_context import get_request_id
from packages.db.models.model_gateway import AIRun, CostRecord
from packages.model_gateway.async_router import AsyncModelRouter
from packages.model_gateway.capabilities import ensure_route_supports
from packages.model_gateway.errors import (
    BudgetExceededError,
    DataPolicyBlockedError,
    GatewayError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    RouteNotFoundError,
)
from packages.model_gateway.observability import emit_gateway_span, genai_attributes
from packages.model_gateway.pricing import estimate_cost_lines, total_estimated_cost
from packages.model_gateway.providers.async_mock import AsyncMockProvider
from packages.model_gateway.providers.async_openai_compatible import (
    AsyncOpenAICompatibleProvider,
)
from packages.model_gateway.providers.base import AsyncProviderAdapter
from packages.model_gateway.redaction import (
    redacted_request_json,
    redacted_response_json,
    request_hash,
    request_preview,
    response_preview,
)
from packages.model_gateway.retries import compute_backoff_delay, policy_from_route_config
from packages.model_gateway.types import (
    GatewayResponse,
    ModelRequest,
    ProviderChatResponse,
    SelectedRoute,
)

logger = logging.getLogger(__name__)


class AsyncModelGateway:
    """Non-blocking application service for chat model calls."""

    def __init__(
        self,
        session: AsyncSession,
        *,
        provider_registry: Mapping[str, AsyncProviderAdapter] | None = None,
    ) -> None:
        self._session = session
        self._router = AsyncModelRouter(session)
        self._provider_registry = provider_registry or default_async_provider_registry()

    async def chat(self, request: ModelRequest) -> GatewayResponse:
        trace_id = request.trace_id or get_request_id()
        decision = await self._router.select_route(request)
        route = decision.selected
        if route is None:
            ai_run = await self._create_blocked_run(
                request,
                decision.error_code,
                decision.error_message,
                trace_id,
            )
            self._raise_selection_error(decision.error_code, decision.error_message, ai_run.id)
        logger.info(
            "async_model_gateway.route_selected",
            extra={
                "event": "async_model_gateway.route_selected",
                "use_case": request.use_case,
                "route_key": route.route_key,
                "provider_name": route.provider_name,
                "rejected_routes": list(decision.rejected_routes),
            },
        )
        ai_run = await self._create_running_run(request, route, trace_id)
        started = time.perf_counter()
        attempts: list[dict[str, Any]] = []
        try:
            provider_result, served_route = await self._call_with_policy(
                request=request,
                route=route,
                attempts=attempts,
            )
        except GatewayError as exc:
            latency_ms = _elapsed_ms(started)
            await self._mark_failed(ai_run, exc, latency_ms, attempts)
            raise

        latency_ms = _elapsed_ms(started)
        response = await self._finalize_success(
            ai_run=ai_run,
            request=request,
            route=served_route,
            provider_result=provider_result,
            latency_ms=latency_ms,
            attempts=attempts,
            trace_id=trace_id,
        )
        logger.info(
            "async_model_gateway.request_completed",
            extra={
                "event": "async_model_gateway.request_completed",
                "ai_run_id": str(ai_run.id),
                "route_key": served_route.route_key,
                "latency_ms": latency_ms,
            },
        )
        return response

    async def _call_with_policy(
        self,
        *,
        request: ModelRequest,
        route: SelectedRoute,
        attempts: list[dict[str, Any]],
    ) -> tuple[ProviderChatResponse, SelectedRoute]:
        current_route = route
        tried_fallback = False
        while True:
            try:
                result = await self._call_route(
                    request=request,
                    route=current_route,
                    attempts=attempts,
                )
                return result, current_route
            except (ProviderTimeoutError, ProviderUnavailableError) as exc:
                should_fallback = (
                    current_route.fallback_route_id is not None
                    and not tried_fallback
                    and (
                        not getattr(exc, "retryable", False)
                        or _is_attempts_exhausted(attempts, current_route)
                    )
                )
                if not should_fallback:
                    raise
                fallback_route_id = current_route.fallback_route_id
                if fallback_route_id is None:
                    raise
                # The fallback route is reselected rather than trusted, so the
                # same data-policy and budget checks apply to it.
                fallback_decision = await self._router.select_fallback(request, fallback_route_id)
                if fallback_decision.selected is None:
                    raise
                current_route = fallback_decision.selected
                tried_fallback = True
                logger.info(
                    "async_model_gateway.fallback_used",
                    extra={
                        "event": "async_model_gateway.fallback_used",
                        "fallback_route_key": current_route.route_key,
                    },
                )

    async def _call_route(
        self,
        *,
        request: ModelRequest,
        route: SelectedRoute,
        attempts: list[dict[str, Any]],
    ) -> ProviderChatResponse:
        provider = self._provider_registry.get(route.provider_type)
        if provider is None:
            raise ProviderUnavailableError(
                retryable=False,
                details={"provider_type": route.provider_type},
            )
        ensure_route_supports(route, operation="chat")
        policy = policy_from_route_config(route.route_config)
        for attempt_number in range(1, policy.max_attempts + 1):
            try:
                result = await provider.chat(request, route)
                attempts.append(
                    {
                        "route_key": route.route_key,
                        "attempt": attempt_number,
                        "status": "succeeded",
                    }
                )
                return result
            except (ProviderTimeoutError, ProviderUnavailableError) as exc:
                attempts.append(
                    {
                        "route_key": route.route_key,
                        "attempt": attempt_number,
                        "status": "failed",
                        "error_code": exc.code,
                        "retryable": getattr(exc, "retryable", False),
                    }
                )
                if not getattr(exc, "retryable", False) or attempt_number > policy.max_retries:
                    raise
                delay_seconds = compute_backoff_delay(attempt_number, policy)
                # `asyncio.sleep`, never `time.sleep`. This hands control back
                # to the loop so other requests keep being served during the
                # wait; the blocking version would freeze all of them.
                if delay_seconds > 0:
                    await asyncio.sleep(delay_seconds)
        raise ProviderUnavailableError(retryable=False, details={"route_key": route.route_key})

    async def _create_running_run(
        self,
        request: ModelRequest,
        route: SelectedRoute,
        trace_id: str | None,
    ) -> AIRun:
        ai_run = AIRun(
            tenant_id=request.tenant_id,
            user_id=request.user_id,
            use_case=request.use_case,
            provider_name=route.provider_name,
            model_name=route.model_name,
            model_route_id=route.route_id,
            prompt_version_id=request.prompt_version_id,
            request_hash=request_hash(request),
            input_preview=request_preview(request),
            request_json=redacted_request_json(request),
            status="running",
            trace_id=trace_id,
        )
        self._session.add(ai_run)
        await self._session.flush()
        return ai_run

    async def _create_blocked_run(
        self,
        request: ModelRequest,
        error_code: str | None,
        error_message: str | None,
        trace_id: str | None,
    ) -> AIRun:
        ai_run = AIRun(
            tenant_id=request.tenant_id,
            user_id=request.user_id,
            use_case=request.use_case,
            provider_name="blocked",
            model_name="none",
            model_route_id=None,
            prompt_version_id=request.prompt_version_id,
            request_hash=request_hash(request),
            input_preview=request_preview(request),
            request_json=redacted_request_json(request),
            status="blocked",
            error_code=error_code,
            error_message=error_message,
            trace_id=trace_id,
        )
        self._session.add(ai_run)
        await self._session.commit()
        return ai_run

    async def _finalize_success(
        self,
        *,
        ai_run: AIRun,
        request: ModelRequest,
        route: SelectedRoute,
        provider_result: ProviderChatResponse,
        latency_ms: int,
        attempts: list[dict[str, Any]],
        trace_id: str | None,
    ) -> GatewayResponse:
        usage = provider_result.usage
        cost_lines = estimate_cost_lines(usage)
        total_cost = total_estimated_cost(cost_lines)

        ai_run.provider_name = route.provider_name
        ai_run.model_name = route.model_name
        ai_run.model_route_id = route.route_id
        ai_run.status = "succeeded"
        ai_run.output_preview = response_preview(
            provider_result.content,
            restricted=request.restricted_data,
        )
        ai_run.response_json = redacted_response_json(
            content=provider_result.content,
            embeddings_count=0,
            restricted=request.restricted_data,
            metadata={
                "finish_reason": provider_result.finish_reason,
                "attempts": attempts,
                "execution_mode": "async",
            },
        )
        ai_run.input_tokens = usage.input_tokens
        ai_run.output_tokens = usage.output_tokens
        ai_run.reasoning_output_tokens = usage.reasoning_output_tokens
        ai_run.cache_creation_input_tokens = usage.cache_creation_input_tokens
        ai_run.cache_read_input_tokens = usage.cache_read_input_tokens
        ai_run.estimated_cost_usd = total_cost
        ai_run.latency_ms = latency_ms
        await self._session.flush()
        for line in cost_lines:
            self._session.add(
                CostRecord(
                    tenant_id=request.tenant_id,
                    ai_run_id=ai_run.id,
                    use_case=request.use_case,
                    provider_name=route.provider_name,
                    model_name=route.model_name,
                    billing_unit=line.billing_unit,
                    quantity=line.quantity,
                    unit_cost_usd=line.unit_cost_usd,
                    estimated_cost_usd=line.estimated_cost_usd,
                    pricing_version=line.pricing_version,
                )
            )
        response = GatewayResponse(
            ai_run_id=ai_run.id,
            use_case=request.use_case,
            provider_name=route.provider_name,
            model_name=route.model_name,
            route_key=route.route_key,
            status="succeeded",
            content=provider_result.content,
            finish_reason=provider_result.finish_reason,
            usage=usage,
            estimated_cost_usd=total_cost,
            latency_ms=latency_ms,
            trace_id=trace_id,
        )
        response.observability_attributes.update(
            genai_attributes(request=request, route=route, response=response)
        )
        # `execution_mode` is recorded so a trace can tell which of the two
        # gateway implementations served a run.
        response.observability_attributes["atlas.execution_mode"] = "async"
        emit_gateway_span(
            "async_model_gateway.chat",
            attributes=response.observability_attributes,
            latency_ms=latency_ms,
        )
        ai_run.response_json = {
            **(ai_run.response_json or {}),
            "observability_attributes": response.observability_attributes,
        }
        await self._session.commit()
        return response

    async def _mark_failed(
        self,
        ai_run: AIRun,
        exc: GatewayError,
        latency_ms: int,
        attempts: list[dict[str, Any]],
    ) -> None:
        ai_run.status = "failed"
        ai_run.error_code = exc.code
        ai_run.error_message = exc.message
        ai_run.latency_ms = latency_ms
        ai_run.response_json = {"attempts": attempts}
        await self._session.commit()

    def _raise_selection_error(
        self,
        error_code: str | None,
        error_message: str | None,
        ai_run_id: object,
    ) -> NoReturn:
        details: dict[str, object] = {"ai_run_id": str(ai_run_id)}
        if error_code == "ai.data_policy_blocked":
            raise DataPolicyBlockedError(details)
        if error_code == "ai.budget_exceeded":
            raise BudgetExceededError(details)
        if error_code == "ai.route_not_found":
            raise RouteNotFoundError(details)
        raise GatewayError(
            code=error_code or "ai.route_not_found",
            message=error_message or "No eligible model route is available.",
            status_code=404,
            details=details,
        )


def default_async_provider_registry() -> dict[str, AsyncProviderAdapter]:
    """Build the adapter map used by production/local async gateway instances."""
    return {
        "mock": AsyncMockProvider(),
        "openai_compatible": AsyncOpenAICompatibleProvider(),
    }


def _elapsed_ms(started: float) -> int:
    return max(0, int((time.perf_counter() - started) * 1000))


def _is_attempts_exhausted(attempts: list[dict[str, Any]], route: SelectedRoute) -> bool:
    max_retries = policy_from_route_config(route.route_config).max_retries
    route_attempts = [
        attempt for attempt in attempts if attempt.get("route_key") == route.route_key
    ]
    return len(route_attempts) > max_retries
