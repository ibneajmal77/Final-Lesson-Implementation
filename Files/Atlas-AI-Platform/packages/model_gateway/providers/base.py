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
