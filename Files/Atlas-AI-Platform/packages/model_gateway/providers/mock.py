"""Deterministic in-process provider used by tests and local development.

The mock implements the same provider protocol as real adapters, so gateway
retry/fallback/cost logic can be tested without network calls or API keys.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict

from packages.model_gateway.errors import ProviderTimeoutError, ProviderUnavailableError
from packages.model_gateway.types import (
    ModelRequest,
    ProviderChatResponse,
    ProviderEmbeddingResponse,
    SelectedRoute,
    TokenUsage,
)


class MockProvider:
    """Simple provider adapter with configurable failure scenarios."""

    def __init__(self) -> None:
        self._scenario_attempts: dict[str, int] = defaultdict(int)
        self.call_count = 0

    def chat(self, request: ModelRequest, route: SelectedRoute) -> ProviderChatResponse:
        self.call_count += 1
        self._maybe_fail(route)
        content = self._chat_content(request, route)
        return ProviderChatResponse(
            content=content,
            usage=TokenUsage(
                input_tokens=self._count_message_tokens(request),
                output_tokens=max(1, len(content.split())),
            ),
            finish_reason="stop",
            raw_response={"provider": "mock", "route_key": route.route_key},
        )

    def embed(self, request: ModelRequest, route: SelectedRoute) -> ProviderEmbeddingResponse:
        self.call_count += 1
        self._maybe_fail(route)
        dimension = route.embedding_dimension or 8
        embeddings = tuple(
            self._embedding_for_text(value, dimension=dimension) for value in request.inputs
        )
        return ProviderEmbeddingResponse(
            embeddings=embeddings,
            usage=TokenUsage(input_tokens=sum(len(value.split()) for value in request.inputs)),
            raw_response={"provider": "mock", "route_key": route.route_key},
        )

    def _maybe_fail(self, route: SelectedRoute) -> None:
        """Raise configured synthetic failures for retry/fallback tests."""
        scenario = str(route.route_config.get("mock_scenario", "success"))
        key = f"{route.route_key}:{scenario}"
        self._scenario_attempts[key] += 1
        attempt = self._scenario_attempts[key]
        if scenario == "timeout_once" and attempt == 1:
            raise ProviderTimeoutError({"route_key": route.route_key, "attempt": attempt})
        if scenario == "timeout_always":
            raise ProviderTimeoutError({"route_key": route.route_key, "attempt": attempt})
        if scenario == "unavailable":
            raise ProviderUnavailableError(
                retryable=False,
                details={"route_key": route.route_key, "attempt": attempt},
            )

    def _chat_content(self, request: ModelRequest, route: SelectedRoute) -> str:
        last_user_message = next(
            (message.content for message in reversed(request.messages) if message.role == "user"),
            "",
        )
        return f"mock:{route.use_case}:{last_user_message}".strip()

    def _count_message_tokens(self, request: ModelRequest) -> int:
        return sum(len(message.content.split()) for message in request.messages)

    def _embedding_for_text(self, value: str, *, dimension: int) -> tuple[float, ...]:
        # Hash-based vectors are deterministic: identical text produces identical
        # embeddings, which keeps tests stable across machines.
        digest = hashlib.sha256(value.encode("utf-8")).digest()
        numbers = []
        for index in range(dimension):
            byte = digest[index % len(digest)]
            numbers.append((byte / 255.0) * 2.0 - 1.0)
        return tuple(numbers)
