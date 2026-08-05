"""Model gateway execution facade.

This class owns the end-to-end model call workflow: select a route, record an
`ai_runs` row, call the provider adapter with retry/fallback policy, redact
stored payloads, estimate cost, and return a stable gateway response.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Mapping
from typing import Any, NoReturn

from sqlalchemy.orm import Session

from packages.core.request_context import get_request_id
from packages.db.models.model_gateway import AIRun, CostRecord
from packages.model_gateway.errors import (
    BudgetExceededError,
    DataPolicyBlockedError,
    GatewayError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    RouteNotFoundError,
)
from packages.model_gateway.observability import genai_attributes
from packages.model_gateway.pricing import estimate_cost_lines, total_estimated_cost
from packages.model_gateway.providers.base import ProviderAdapter
from packages.model_gateway.providers.mock import MockProvider
from packages.model_gateway.providers.openai_compatible import OpenAICompatibleProvider
from packages.model_gateway.redaction import (
    redacted_request_json,
    redacted_response_json,
    request_hash,
    request_preview,
    response_preview,
)
from packages.model_gateway.router import ModelRouter
from packages.model_gateway.types import (
    GatewayResponse,
    ModelRequest,
    ProviderChatResponse,
    ProviderEmbeddingResponse,
    RunStatus,
    SelectedRoute,
)

logger = logging.getLogger(__name__)


class ModelGateway:
    """Application service for chat and embedding model calls."""

    def __init__(
        self,
        session: Session,
        *,
        provider_registry: Mapping[str, ProviderAdapter] | None = None,
    ) -> None:
        # Keyword-only parameters appear after `*`. Here `provider_registry` must
        # be passed by name, which keeps tests readable and avoids argument mixups.
        self._session = session
        self._router = ModelRouter(session)
        self._provider_registry = provider_registry or _default_provider_registry()

    def chat(self, request: ModelRequest) -> GatewayResponse:
        return self._execute(request, operation="chat")

    def embed(self, request: ModelRequest) -> GatewayResponse:
        return self._execute(request, operation="embed")

    def _execute(self, request: ModelRequest, *, operation: str) -> GatewayResponse:
        trace_id = request.trace_id or get_request_id()
        decision = self._router.select_route(request)
        route = decision.selected
        if route is None:
            # Even blocked selections get an AIRun row so operations can audit
            # why a request never reached a provider.
            ai_run = self._create_blocked_run(
                request,
                decision.error_code,
                decision.error_message,
                trace_id,
            )
            self._raise_selection_error(decision.error_code, decision.error_message, ai_run.id)
        logger.info(
            "model_gateway.route_selected",
            extra={
                "event": "model_gateway.route_selected",
                "use_case": request.use_case,
                "route_key": route.route_key,
                "provider_name": route.provider_name,
                "rejected_routes": list(decision.rejected_routes),
            },
        )
        ai_run = self._create_running_run(request, route, trace_id)
        started = time.perf_counter()
        attempts: list[dict[str, Any]] = []
        try:
            # Provider exceptions are allowed to bubble after the run is marked
            # failed; successful calls continue into the persistence/cost path.
            provider_result, served_route = self._call_with_policy(
                request=request,
                route=route,
                operation=operation,
                attempts=attempts,
            )
        except GatewayError as exc:
            latency_ms = _elapsed_ms(started)
            self._mark_failed(ai_run, exc, latency_ms, attempts)
            raise

        latency_ms = _elapsed_ms(started)
        response = self._finalize_success(
            ai_run=ai_run,
            request=request,
            route=served_route,
            provider_result=provider_result,
            latency_ms=latency_ms,
            attempts=attempts,
            trace_id=trace_id,
        )
        logger.info(
            "model_gateway.request_completed",
            extra={
                "event": "model_gateway.request_completed",
                "ai_run_id": str(ai_run.id),
                "route_key": served_route.route_key,
                "provider_name": served_route.provider_name,
                "latency_ms": latency_ms,
                "estimated_cost_usd": str(response.estimated_cost_usd),
            },
        )
        return response

    def _call_with_policy(
        self,
        *,
        request: ModelRequest,
        route: SelectedRoute,
        operation: str,
        attempts: list[dict[str, Any]],
    ) -> tuple[ProviderChatResponse | ProviderEmbeddingResponse, SelectedRoute]:
        current_route = route
        tried_fallback = False
        while True:
            try:
                result = self._call_route(
                    request=request,
                    route=current_route,
                    operation=operation,
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
                if should_fallback:
                    # Fallback is route-level, not provider-level. The fallback
                    # route is reselected so the same compliance checks apply.
                    fallback_route_id = current_route.fallback_route_id
                    if fallback_route_id is None:
                        raise exc
                    fallback_decision = self._router.select_fallback(
                        request,
                        fallback_route_id,
                    )
                    if fallback_decision.selected is None:
                        raise exc
                    current_route = fallback_decision.selected
                    tried_fallback = True
                    logger.info(
                        "model_gateway.fallback_used",
                        extra={
                            "event": "model_gateway.fallback_used",
                            "fallback_route_key": current_route.route_key,
                        },
                    )
                    continue
                raise

    def _call_route(
        self,
        *,
        request: ModelRequest,
        route: SelectedRoute,
        operation: str,
        attempts: list[dict[str, Any]],
    ) -> ProviderChatResponse | ProviderEmbeddingResponse:
        provider = self._provider_registry.get(route.provider_type)
        if provider is None:
            raise ProviderUnavailableError(
                retryable=False,
                details={"provider_type": route.provider_type},
            )
        max_retries = int(route.route_config.get("max_retries", 1))
        # `range(1, max_retries + 2)` gives the initial attempt plus retries.
        for attempt_number in range(1, max_retries + 2):
            logger.info(
                "model_gateway.attempt_started",
                extra={
                    "event": "model_gateway.attempt_started",
                    "route_key": route.route_key,
                    "attempt": attempt_number,
                },
            )
            try:
                result: ProviderChatResponse | ProviderEmbeddingResponse
                if operation == "embed":
                    result = provider.embed(request, route)
                else:
                    result = provider.chat(request, route)
                attempts.append(
                    {"route_key": route.route_key, "attempt": attempt_number, "status": "succeeded"}
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
                logger.info(
                    "model_gateway.attempt_failed",
                    extra={
                        "event": "model_gateway.attempt_failed",
                        "route_key": route.route_key,
                        "attempt": attempt_number,
                        "error_code": exc.code,
                        "retryable": getattr(exc, "retryable", False),
                    },
                )
                if not getattr(exc, "retryable", False) or attempt_number > max_retries:
                    raise
        raise ProviderUnavailableError(retryable=False, details={"route_key": route.route_key})

    def _create_running_run(
        self,
        request: ModelRequest,
        route: SelectedRoute,
        trace_id: str | None,
    ) -> AIRun:
        # `flush()` sends the INSERT so `ai_run.id` is available before commit;
        # the surrounding workflow still commits only after success/failure.
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
        self._session.flush()
        return ai_run

    def _create_blocked_run(
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
        self._session.commit()
        return ai_run

    def _finalize_success(
        self,
        *,
        ai_run: AIRun,
        request: ModelRequest,
        route: SelectedRoute,
        provider_result: ProviderChatResponse | ProviderEmbeddingResponse,
        latency_ms: int,
        attempts: list[dict[str, Any]],
        trace_id: str | None,
    ) -> GatewayResponse:
        usage = provider_result.usage
        cost_lines = estimate_cost_lines(usage)
        total_cost = total_estimated_cost(cost_lines)
        content = (
            provider_result.content
            if isinstance(provider_result, ProviderChatResponse)
            else None
        )
        embeddings = (
            provider_result.embeddings
            if isinstance(provider_result, ProviderEmbeddingResponse)
            else ()
        )

        ai_run.provider_name = route.provider_name
        ai_run.model_name = route.model_name
        ai_run.model_route_id = route.route_id
        ai_run.status = "succeeded"
        ai_run.output_preview = response_preview(content, restricted=request.restricted_data)
        ai_run.response_json = redacted_response_json(
            content=content,
            embeddings_count=len(embeddings),
            restricted=request.restricted_data,
            metadata={
                "finish_reason": getattr(provider_result, "finish_reason", None),
                "attempts": attempts,
            },
        )
        ai_run.input_tokens = usage.input_tokens
        ai_run.output_tokens = usage.output_tokens
        ai_run.reasoning_output_tokens = usage.reasoning_output_tokens
        ai_run.cache_creation_input_tokens = usage.cache_creation_input_tokens
        ai_run.cache_read_input_tokens = usage.cache_read_input_tokens
        ai_run.estimated_cost_usd = total_cost
        ai_run.latency_ms = latency_ms
        self._session.flush()
        # Cost rows are separate line items so later reporting can group by
        # token type or billing unit without reparsing raw provider responses.
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
            content=content,
            embeddings=embeddings,
            finish_reason=getattr(provider_result, "finish_reason", None),
            usage=usage,
            estimated_cost_usd=total_cost,
            latency_ms=latency_ms,
            trace_id=trace_id,
        )
        response.observability_attributes.update(
            genai_attributes(request=request, route=route, response=response)
        )
        # Store observability attributes after the response object is assembled
        # so the persisted ledger and HTTP response expose the same dimensions.
        ai_run.response_json = {
            **(ai_run.response_json or {}),
            "observability_attributes": response.observability_attributes,
        }
        self._session.commit()
        return response

    def _mark_failed(
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
        self._session.commit()

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


def _default_provider_registry() -> dict[str, ProviderAdapter]:
    """Build the default adapter map used by production/local gateway instances."""
    mock_provider = MockProvider()
    return {
        "mock": mock_provider,
        "openai_compatible": OpenAICompatibleProvider(),
    }


def _elapsed_ms(started: float) -> int:
    return max(0, int((time.perf_counter() - started) * 1000))


def _is_attempts_exhausted(attempts: list[dict[str, Any]], route: SelectedRoute) -> bool:
    max_retries = int(route.route_config.get("max_retries", 1))
    route_attempts = [
        attempt for attempt in attempts if attempt.get("route_key") == route.route_key
    ]
    return len(route_attempts) > max_retries


def run_status(value: str) -> RunStatus:
    """Coerce database/free-form status text into the known RunStatus values."""
    if value in {"queued", "running", "succeeded", "failed", "cancelled", "blocked"}:
        return value  # type: ignore[return-value]
    return "failed"
