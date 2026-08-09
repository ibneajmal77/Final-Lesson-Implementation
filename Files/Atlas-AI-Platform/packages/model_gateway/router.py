"""Database-backed route selection policy for model requests.

This is the gateway's routing engine. It chooses the best active route for a
use case, tenant, data policy, and budget, then reports why other candidates
were rejected.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, cast
from uuid import UUID

from sqlalchemy import Select, or_, select
from sqlalchemy.orm import Session, joinedload

from packages.auth.gates import enforce_tenant_rbac_gate
from packages.db.models.model_gateway import ModelProvider, ModelRoute
from packages.model_gateway.types import ModelRequest, RouteDecision, SelectedRoute, UseCase

# The statement builders and the policy evaluation below are module-level rather
# than methods because the async router in `async_router.py` reuses them
# verbatim. Only the *execution* of a statement differs between sync and async;
# the routing policy itself must not be written twice, or the two paths will
# drift and start selecting different routes for the same request.


def select_route_statement(request: ModelRequest) -> Select[tuple[ModelRoute]]:
    """Build the candidate-route query for a request."""
    # SQLAlchemy builds SQL through chained Python calls. This is similar to
    # LINQ query composition, but it produces a SQLAlchemy Select object.
    return (
        select(ModelRoute)
        .join(ModelProvider, ModelProvider.id == ModelRoute.provider_id)
        # `joinedload` fetches the provider in the same round trip. On the async
        # path this is mandatory, not an optimization: touching `route.provider`
        # lazily inside a coroutine raises MissingGreenlet, because the implicit
        # lazy-load would be blocking I/O on the event loop.
        .options(joinedload(ModelRoute.provider))
        .where(
            ModelRoute.use_case == request.use_case,
            ModelRoute.status == "active",
            ModelProvider.status == "active",
            or_(ModelRoute.tenant_id.is_(None), ModelRoute.tenant_id == request.tenant_id),
        )
        .order_by(
            # Tenant-specific rows should win over global rows, then lower
            # priority numbers win, then route_key makes the order stable.
            ModelRoute.tenant_id.desc().nulls_last(),
            ModelRoute.priority,
            ModelRoute.route_key,
        )
    )


def fallback_route_statement(fallback_route_id: UUID) -> Select[tuple[ModelRoute]]:
    """Build the query for one specific fallback route."""
    return (
        select(ModelRoute)
        .join(ModelProvider, ModelProvider.id == ModelRoute.provider_id)
        .options(joinedload(ModelRoute.provider))
        .where(
            ModelRoute.id == fallback_route_id,
            ModelRoute.status == "active",
            ModelProvider.status == "active",
        )
    )


def list_routes_statement() -> Select[tuple[ModelRoute]]:
    """Build the operational route-listing query."""
    return (
        select(ModelRoute)
        .join(ModelProvider, ModelProvider.id == ModelRoute.provider_id)
        .options(joinedload(ModelRoute.provider))
        .where(ModelProvider.status == "active")
        .order_by(ModelRoute.use_case, ModelRoute.priority, ModelRoute.route_key)
    )


def evaluate_candidates(
    request: ModelRequest,
    routes: Sequence[ModelRoute],
) -> RouteDecision:
    """Apply routing policy to already-loaded rows.

    This is the whole selection decision, and it performs no I/O. Both routers
    hand it the rows they fetched, which is what keeps sync and async agreeing.
    """
    rejected: list[dict[str, Any]] = []
    for route in routes:
        # Keep rejection details for observability; the final error code is
        # derived after all candidate routes have been evaluated.
        rejection = rejection_reason(request, route)
        if rejection is None:
            return RouteDecision(
                selected=to_selected_route(route),
                rejected_routes=tuple(rejected),
            )
        rejected.append(rejection)
    return _decision_for_rejections(tuple(rejected))


class ModelRouter:
    """Select eligible `ModelRoute` rows for a `ModelRequest`."""

    def __init__(self, session: Session) -> None:
        # A SQLAlchemy Session is the unit-of-work object, comparable to an EF
        # DbContext scoped to one request/test.
        self._session = session

    def select_route(self, request: ModelRequest) -> RouteDecision:
        return self._select_from_statement(request, select_route_statement(request))

    def select_fallback(self, request: ModelRequest, fallback_route_id: UUID) -> RouteDecision:
        return self._select_from_statement(request, fallback_route_statement(fallback_route_id))

    def list_routes(self) -> list[SelectedRoute]:
        return [
            # List comprehensions are Python's concise projection syntax.
            to_selected_route(route)
            for route in self._session.scalars(list_routes_statement()).unique().all()
        ]

    def _select_from_statement(
        self,
        request: ModelRequest,
        statement: Select[tuple[ModelRoute]],
    ) -> RouteDecision:
        return evaluate_candidates(request, self._session.scalars(statement).unique().all())


def rejection_reason(
    request: ModelRequest,
    route: ModelRoute,
) -> dict[str, Any] | None:
    """Return why this route cannot serve the request, or None if it can."""
    provider = route.provider
    if route.tenant_id is not None:
        try:
            enforce_tenant_rbac_gate(
                "model_gateway.tenant_route",
                request.granted_permissions,
            )
        except Exception as exc:
            return {
                "route_key": route.route_key,
                "reason": "tenant_rbac_gate",
                "error": exc.__class__.__name__,
            }
    required_capability = _required_capability(request.use_case)
    if not provider.capabilities_json.get(required_capability, False):
        return {
            "route_key": route.route_key,
            "reason": "capability_missing",
            "capability": required_capability,
        }
    provider_allows_restricted = bool(
        provider.data_policy_json.get("restricted_data_allowed", False)
    )
    if request.restricted_data and (
        not route.restricted_data_allowed or not provider_allows_restricted
    ):
        return {"route_key": route.route_key, "reason": "data_policy"}
    if request.max_cost_usd is not None and route.max_cost_usd is not None:
        if route.max_cost_usd > request.max_cost_usd:
            return {
                "route_key": route.route_key,
                "reason": "budget",
                "route_max_cost_usd": str(route.max_cost_usd),
                "request_max_cost_usd": str(request.max_cost_usd),
            }
    return None


def _required_capability(use_case: UseCase) -> str:
    if use_case == "embedding":
        return "supports_embeddings"
    return "supports_chat"


def to_selected_route(route: ModelRoute) -> SelectedRoute:
    provider = route.provider
    return SelectedRoute(
        route_id=route.id,
        route_key=route.route_key,
        use_case=cast(UseCase, route.use_case),
        provider_name=provider.name,
        provider_type=cast(Any, provider.provider_type),
        model_name=route.model_name,
        max_input_tokens=route.max_input_tokens,
        max_output_tokens=route.max_output_tokens,
        timeout_seconds=route.timeout_seconds,
        temperature=route.temperature,
        restricted_data_allowed=route.restricted_data_allowed,
        fallback_route_id=route.fallback_route_id,
        route_config=route.route_config_json,
        capabilities=provider.capabilities_json,
        data_policy=provider.data_policy_json,
        max_cost_usd=route.max_cost_usd,
        embedding_dimension=route.embedding_dimension,
    )


def _decision_for_rejections(rejections: tuple[dict[str, Any], ...]) -> RouteDecision:
    """Collapse detailed route rejections into the public gateway error code."""
    reasons = {str(rejection.get("reason")) for rejection in rejections}
    if "data_policy" in reasons:
        return RouteDecision(
            selected=None,
            rejected_routes=rejections,
            error_code="ai.data_policy_blocked",
            error_message="No compliant model route can handle restricted data.",
        )
    if "budget" in reasons:
        return RouteDecision(
            selected=None,
            rejected_routes=rejections,
            error_code="ai.budget_exceeded",
            error_message="No eligible model route fits the requested cost budget.",
        )
    return RouteDecision(
        selected=None,
        rejected_routes=rejections,
        error_code="ai.route_not_found",
        error_message="No eligible model route is available.",
    )
