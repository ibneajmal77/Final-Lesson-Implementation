"""Async route selection.

This is deliberately thin. Every routing *decision* lives in `router.py` as a
pure function; the only thing that has to be written twice is the statement
execution, because `session.scalars(...)` and `await session.scalars(...)` are
genuinely different calls.

Keeping it this small is the guardrail: if selection policy were duplicated
here, the sync and async paths would drift and eventually pick different routes
for identical requests, which is close to impossible to debug from a trace.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from packages.db.models.model_gateway import ModelRoute
from packages.model_gateway.router import (
    evaluate_candidates,
    fallback_route_statement,
    list_routes_statement,
    select_route_statement,
    to_selected_route,
)
from packages.model_gateway.types import ModelRequest, RouteDecision, SelectedRoute


class AsyncModelRouter:
    """`ModelRouter` over an AsyncSession."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def select_route(self, request: ModelRequest) -> RouteDecision:
        return await self._select_from_statement(request, select_route_statement(request))

    async def select_fallback(
        self,
        request: ModelRequest,
        fallback_route_id: UUID,
    ) -> RouteDecision:
        return await self._select_from_statement(
            request,
            fallback_route_statement(fallback_route_id),
        )

    async def list_routes(self) -> list[SelectedRoute]:
        result = await self._session.scalars(list_routes_statement())
        return [to_selected_route(route) for route in result.unique().all()]

    async def _select_from_statement(
        self,
        request: ModelRequest,
        statement: Select[tuple[ModelRoute]],
    ) -> RouteDecision:
        result = await self._session.scalars(statement)
        # The rows are fully loaded here, including each route's provider via
        # the joinedload in the shared statement builders. Policy evaluation
        # therefore touches no lazy attribute and needs no await.
        return evaluate_candidates(request, result.unique().all())
