"""Awaitable mock provider for the async gateway path.

It delegates every decision to the synchronous `MockProvider` so the two paths
cannot disagree about content, token counts, or failure scenarios. Only the
waiting is different: `asyncio.sleep` yields control back to the event loop,
which is the entire behavioral difference this slice exists to demonstrate.
"""

from __future__ import annotations

import asyncio

from packages.model_gateway.providers.mock import MockProvider
from packages.model_gateway.types import (
    ModelRequest,
    ProviderChatResponse,
    ProviderEmbeddingResponse,
    SelectedRoute,
)


class AsyncMockProvider:
    """Async adapter wrapping the deterministic mock behavior."""

    def __init__(self, *, latency_seconds: float = 0.0) -> None:
        self._inner = MockProvider()
        # A configurable fake latency lets a test prove that two concurrent
        # calls overlap instead of running one after the other.
        self._latency_seconds = latency_seconds

    @property
    def call_count(self) -> int:
        return self._inner.call_count

    async def chat(self, request: ModelRequest, route: SelectedRoute) -> ProviderChatResponse:
        await self._simulate_network()
        # The inner call is pure CPU work on in-memory data, so running it
        # directly on the loop is correct. Only I/O needs to be awaited.
        return self._inner.chat(request, route)

    async def embed(
        self,
        request: ModelRequest,
        route: SelectedRoute,
    ) -> ProviderEmbeddingResponse:
        await self._simulate_network()
        return self._inner.embed(request, route)

    async def _simulate_network(self) -> None:
        if self._latency_seconds > 0:
            await asyncio.sleep(self._latency_seconds)
