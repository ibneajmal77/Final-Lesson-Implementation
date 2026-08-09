"""Provider adapter protocol.

`Protocol` is Python's structural interface: a class is accepted if it exposes
compatible `chat` and `embed` methods, even without explicit inheritance.
"""

from typing import Protocol

from packages.model_gateway.types import (
    ModelRequest,
    ProviderChatResponse,
    ProviderEmbeddingResponse,
    SelectedRoute,
)


class ProviderAdapter(Protocol):
    def chat(self, request: ModelRequest, route: SelectedRoute) -> ProviderChatResponse:
        """Execute a chat/completion style request."""

    def embed(self, request: ModelRequest, route: SelectedRoute) -> ProviderEmbeddingResponse:
        """Execute an embedding request."""


class AsyncProviderAdapter(Protocol):
    """The awaitable counterpart to `ProviderAdapter`.

    This is a separate protocol rather than an optional method on the sync one
    so the type checker refuses the mix-up outright: an `AsyncModelGateway`
    cannot be handed a blocking adapter, which is exactly the mistake that
    would stall the event loop while looking perfectly fine in review.
    """

    async def chat(self, request: ModelRequest, route: SelectedRoute) -> ProviderChatResponse:
        """Execute a chat/completion style request without blocking the loop."""

    async def embed(
        self,
        request: ModelRequest,
        route: SelectedRoute,
    ) -> ProviderEmbeddingResponse:
        """Execute an embedding request without blocking the loop."""
