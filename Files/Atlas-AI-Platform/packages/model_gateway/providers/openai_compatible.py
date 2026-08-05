"""Opt-in adapter for OpenAI-compatible chat completion APIs.

The project defaults to mock providers. This adapter is intentionally small and
disabled unless an API key is configured, so CI never depends on paid providers.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from collections.abc import Mapping
from typing import Any, cast

from packages.model_gateway.errors import ProviderUnavailableError
from packages.model_gateway.providers.base import ProviderAdapter
from packages.model_gateway.types import (
    FinishReason,
    ModelRequest,
    ProviderChatResponse,
    ProviderEmbeddingResponse,
    SelectedRoute,
    TokenUsage,
)


class OpenAICompatibleProvider:
    def chat(self, request: ModelRequest, route: SelectedRoute) -> ProviderChatResponse:
        api_key = os.getenv("ATLAS_OPENAI_COMPATIBLE_API_KEY")
        if not api_key:
            raise ProviderUnavailableError(
                retryable=False,
                message="OpenAI-compatible provider key is not configured.",
                details={"provider_name": route.provider_name},
            )
        base_url = (
            route.data_policy.get("base_url") or route.route_config.get("base_url") or ""
        ).strip()
        if not base_url:
            base_url = "https://api.openai.com/v1"
        # Build an OpenAI-compatible `/chat/completions` payload while omitting
        # keys with `None` later in `_post_json`.
        payload: dict[str, object] = {
            "model": route.model_name,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in request.messages
            ],
            "temperature": float(route.temperature) if route.temperature is not None else None,
            "max_tokens": route.max_output_tokens,
        }
        response = self._post_json(f"{base_url.rstrip('/')}/chat/completions", payload, api_key)
        choices = response.get("choices")
        choice = choices[0] if isinstance(choices, list) and choices else {}
        choice_payload = choice if isinstance(choice, dict) else {}
        message = choice_payload.get("message")
        message_payload = message if isinstance(message, dict) else {}
        content = str(message_payload.get("content", ""))
        usage = response.get("usage")
        usage_payload = usage if isinstance(usage, dict) else {}
        finish_reason = cast(FinishReason, choice_payload.get("finish_reason") or "stop")
        return ProviderChatResponse(
            content=content,
            usage=TokenUsage(
                input_tokens=_as_int(usage_payload.get("prompt_tokens")),
                output_tokens=_as_int(usage_payload.get("completion_tokens")),
            ),
            finish_reason=finish_reason,
            raw_response={"id": response.get("id"), "object": response.get("object")},
        )

    def embed(self, request: ModelRequest, route: SelectedRoute) -> ProviderEmbeddingResponse:
        # Embeddings are deliberately disabled for this provider in the current
        # phase; the mock provider covers embedding contract tests locally.
        raise ProviderUnavailableError(
            retryable=False,
            message="OpenAI-compatible embedding calls are not enabled in Phase 01 smoke tests.",
            details={"provider_name": route.provider_name},
        )

    def _post_json(
        self,
        url: str,
        payload: Mapping[str, object],
        api_key: str,
    ) -> dict[str, Any]:
        """POST JSON with the Python standard library to avoid extra SDK dependencies."""
        data = json.dumps({k: v for k, v in payload.items() if v is not None}).encode("utf-8")
        http_request = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(http_request, timeout=30) as response:
                decoded = response.read().decode("utf-8")
        except urllib.error.URLError as exc:
            raise ProviderUnavailableError(
                retryable=True,
                message="OpenAI-compatible provider request failed.",
                details={"reason": str(exc.reason)},
            ) from exc
        loaded = json.loads(decoded)
        if isinstance(loaded, dict):
            return loaded
        return {}


def _as_int(value: object) -> int | None:
    """Defensively parse usage fields from provider JSON."""
    if isinstance(value, int):
        return value
    return None


def create_managed_provider() -> ProviderAdapter:
    """Factory kept for future provider-management wiring."""
    return OpenAICompatibleProvider()
