"""Non-blocking adapter for OpenAI-compatible chat completion APIs.

This is the async counterpart to `openai_compatible.py`, and the contrast
between the two files is the point of the whole async slice.

The sync adapter calls `urllib.request.urlopen(..., timeout=30)`. On a `def`
endpoint that is fine: Starlette runs the handler on a threadpool, so the call
occupies one thread for up to thirty seconds and nothing else notices.

Putting that same call inside an `async def` would be a serious bug. It would
block the event loop for the full thirty seconds, freezing every other request
in the process — health checks included. `httpx.AsyncClient` is what makes the
wait yield instead.

The API key is read from settings rather than `os.getenv`, so configuration has
exactly one source and the value is validated at startup.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

import httpx

from packages.core.config import get_settings
from packages.model_gateway.errors import ProviderTimeoutError, ProviderUnavailableError
from packages.model_gateway.types import (
    FinishReason,
    ModelRequest,
    ProviderChatResponse,
    ProviderEmbeddingResponse,
    SelectedRoute,
    TokenUsage,
)

DEFAULT_BASE_URL = "https://api.openai.com/v1"


class AsyncOpenAICompatibleProvider:
    """Awaitable OpenAI-compatible adapter built on httpx."""

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        # An injected client lets tests supply a MockTransport, and lets a
        # long-lived process share one connection pool instead of paying for a
        # new TLS handshake on every request.
        self._client = client

    async def chat(self, request: ModelRequest, route: SelectedRoute) -> ProviderChatResponse:
        api_key = get_settings().openai_compatible_api_key
        if not api_key:
            raise ProviderUnavailableError(
                retryable=False,
                message="OpenAI-compatible provider key is not configured.",
                details={"provider_name": route.provider_name},
            )
        base_url = (
            route.data_policy.get("base_url") or route.route_config.get("base_url") or ""
        ).strip() or DEFAULT_BASE_URL
        payload: dict[str, object] = {
            "model": route.model_name,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in request.messages
            ],
            "temperature": float(route.temperature) if route.temperature is not None else None,
            "max_tokens": route.max_output_tokens,
        }
        response = await self._post_json(
            f"{base_url.rstrip('/')}/chat/completions",
            payload,
            api_key,
            timeout_seconds=route.timeout_seconds,
        )
        choices = response.get("choices")
        choice = choices[0] if isinstance(choices, list) and choices else {}
        choice_payload = choice if isinstance(choice, dict) else {}
        message = choice_payload.get("message")
        message_payload = message if isinstance(message, dict) else {}
        usage = response.get("usage")
        usage_payload = usage if isinstance(usage, dict) else {}
        finish_reason = cast(FinishReason, choice_payload.get("finish_reason") or "stop")
        return ProviderChatResponse(
            content=str(message_payload.get("content", "")),
            usage=TokenUsage(
                input_tokens=_as_int(usage_payload.get("prompt_tokens")),
                output_tokens=_as_int(usage_payload.get("completion_tokens")),
            ),
            finish_reason=finish_reason,
            raw_response={"id": response.get("id"), "object": response.get("object")},
        )

    async def embed(
        self,
        request: ModelRequest,
        route: SelectedRoute,
    ) -> ProviderEmbeddingResponse:
        # Kept deliberately disabled, matching the sync adapter. The async slice
        # covers the chat path, which is the one where the waiting actually is.
        raise ProviderUnavailableError(
            retryable=False,
            message="OpenAI-compatible embedding calls are not enabled.",
            details={"provider_name": route.provider_name},
        )

    async def _post_json(
        self,
        url: str,
        payload: Mapping[str, object],
        api_key: str,
        *,
        timeout_seconds: int,
    ) -> dict[str, Any]:
        body = {key: value for key, value in payload.items() if value is not None}
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        client = self._client
        # Only close a client this adapter created. Closing an injected one
        # would break the caller's connection pool on the first request.
        owns_client = client is None
        if client is None:
            client = httpx.AsyncClient(timeout=timeout_seconds)
        try:
            response = await client.post(url, json=body, headers=headers)
            response.raise_for_status()
            loaded = response.json()
        except httpx.TimeoutException as exc:
            # A timeout is retryable; a refused connection may not be. Mapping
            # them to different gateway errors is what lets the retry policy
            # tell "try again" apart from "stop".
            raise ProviderTimeoutError(
                {"provider_name": "openai_compatible", "reason": str(exc)}
            ) from exc
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code
            raise ProviderUnavailableError(
                # 429 and 5xx are worth another attempt. A 4xx is a bad request
                # and will fail identically no matter how often it is retried.
                retryable=status_code == 429 or status_code >= 500,
                message="OpenAI-compatible provider returned an error status.",
                details={"status_code": status_code},
            ) from exc
        except httpx.HTTPError as exc:
            raise ProviderUnavailableError(
                retryable=True,
                message="OpenAI-compatible provider request failed.",
                details={"reason": str(exc)},
            ) from exc
        finally:
            if owns_client:
                await client.aclose()
        return loaded if isinstance(loaded, dict) else {}


def _as_int(value: object) -> int | None:
    """Defensively parse usage fields from provider JSON."""
    if isinstance(value, int):
        return value
    return None
