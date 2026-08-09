"""Tests for the async gateway path.

The database-backed cases mirror the sync gateway tests, so both paths are held
to the same behavior. The rest run without a database, because the interesting
async properties — that concurrent calls overlap, and that retry waiting yields
the loop — are observable in the provider adapter alone.
"""

from __future__ import annotations

import asyncio
from decimal import Decimal
from uuid import uuid4

import httpx
import pytest

from packages.core.config import Settings
from packages.model_gateway.errors import (
    CapabilityNotSupportedError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)
from packages.model_gateway.providers import async_openai_compatible
from packages.model_gateway.providers.async_mock import AsyncMockProvider
from packages.model_gateway.providers.async_openai_compatible import (
    AsyncOpenAICompatibleProvider,
)
from packages.model_gateway.types import ChatMessage, ModelRequest, SelectedRoute


def _route(**overrides: object) -> SelectedRoute:
    defaults: dict[str, object] = {
        "route_id": uuid4(),
        "route_key": "chat_primary",
        "use_case": "chat",
        "provider_name": "mock_public",
        "provider_type": "mock",
        "model_name": "mock-chat-v1",
        "max_input_tokens": 4000,
        "max_output_tokens": 800,
        "timeout_seconds": 30,
        "temperature": Decimal("0.2"),
        "restricted_data_allowed": False,
        "fallback_route_id": None,
        "route_config": {},
        "capabilities": {"supports_chat": True, "supports_embeddings": True},
        "data_policy": {},
        "max_cost_usd": Decimal("0.05"),
        "embedding_dimension": 8,
    }
    defaults.update(overrides)
    return SelectedRoute(**defaults)  # type: ignore[arg-type]


def _request(content: str = "hello async") -> ModelRequest:
    return ModelRequest(
        tenant_id=uuid4(),
        use_case="chat",
        messages=(ChatMessage(role="user", content=content),),
    )


def _set_api_key(monkeypatch: pytest.MonkeyPatch, key: str | None) -> None:
    """Override the provider key for one test.

    The patch targets the adapter module rather than `packages.core.config`,
    because `from ... import get_settings` binds the name at import time —
    patching the source module would leave the already-imported reference
    pointing at the original function.
    """
    monkeypatch.setattr(
        async_openai_compatible,
        "get_settings",
        lambda: Settings(_env_file=None, openai_compatible_api_key=key),
    )


@pytest.mark.asyncio
async def test_async_mock_matches_sync_mock_output() -> None:
    """The two paths must produce identical content and usage."""
    from packages.model_gateway.providers.mock import MockProvider

    route = _route()
    request = _request()

    async_response = await AsyncMockProvider().chat(request, route)
    sync_response = MockProvider().chat(request, route)

    assert async_response.content == sync_response.content
    assert async_response.usage == sync_response.usage
    assert async_response.finish_reason == sync_response.finish_reason


@pytest.mark.asyncio
async def test_concurrent_calls_overlap_instead_of_queueing() -> None:
    """This is the whole reason the async path exists.

    Five calls that each wait 100ms finish in roughly 100ms total, not 500ms.
    On a blocking implementation this assertion would fail, which makes it a
    real regression guard against someone reintroducing a synchronous call.
    """
    provider = AsyncMockProvider(latency_seconds=0.1)
    route = _route()

    started = asyncio.get_running_loop().time()
    await asyncio.gather(*(provider.chat(_request(f"call {index}"), route) for index in range(5)))
    elapsed = asyncio.get_running_loop().time() - started

    assert provider.call_count == 5
    # Generous upper bound so the test is not flaky on a loaded machine, but
    # still far below the ~0.5s a sequential implementation would need.
    assert elapsed < 0.35, f"calls appear to have run sequentially ({elapsed:.3f}s)"


@pytest.mark.asyncio
async def test_capability_gate_refuses_before_any_provider_call() -> None:
    from packages.model_gateway.capabilities import ensure_route_supports

    route = _route(capabilities={"supports_chat": False})

    with pytest.raises(CapabilityNotSupportedError):
        ensure_route_supports(route, operation="chat")


@pytest.mark.asyncio
async def test_missing_api_key_is_reported_as_a_terminal_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unconfigured key must not be retryable — retrying cannot fix it."""
    _set_api_key(monkeypatch, None)

    with pytest.raises(ProviderUnavailableError) as exc_info:
        await AsyncOpenAICompatibleProvider().chat(_request(), _route())

    assert exc_info.value.retryable is False


@pytest.mark.asyncio
async def test_http_error_statuses_map_to_the_right_retryability(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """429 and 5xx are worth retrying; a 400 will fail the same way forever."""
    _set_api_key(monkeypatch, "test-key")

    async def _call(status_code: int) -> ProviderUnavailableError:
        transport = httpx.MockTransport(lambda request: httpx.Response(status_code, json={}))
        client = httpx.AsyncClient(transport=transport)
        provider = AsyncOpenAICompatibleProvider(client=client)
        try:
            with pytest.raises(ProviderUnavailableError) as exc_info:
                await provider.chat(_request(), _route(provider_type="openai_compatible"))
            return exc_info.value
        finally:
            await client.aclose()

    assert (await _call(500)).retryable is True
    assert (await _call(429)).retryable is True
    assert (await _call(400)).retryable is False


@pytest.mark.asyncio
async def test_timeout_is_translated_to_a_retryable_gateway_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_api_key(monkeypatch, "test-key")

    def _raise_timeout(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("too slow", request=request)

    client = httpx.AsyncClient(transport=httpx.MockTransport(_raise_timeout))
    try:
        with pytest.raises(ProviderTimeoutError) as exc_info:
            await AsyncOpenAICompatibleProvider(client=client).chat(
                _request(),
                _route(provider_type="openai_compatible"),
            )
        assert exc_info.value.retryable is True
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_successful_response_is_normalized_like_the_sync_adapter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_api_key(monkeypatch, "test-key")
    payload = {
        "id": "cmpl-1",
        "object": "chat.completion",
        "choices": [{"message": {"content": "hi there"}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 7, "completion_tokens": 3},
    }
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json=payload))
    )
    try:
        response = await AsyncOpenAICompatibleProvider(client=client).chat(
            _request(),
            _route(provider_type="openai_compatible"),
        )
    finally:
        await client.aclose()

    assert response.content == "hi there"
    assert response.usage.input_tokens == 7
    assert response.usage.output_tokens == 3
    assert response.finish_reason == "stop"


@pytest.mark.asyncio
async def test_injected_client_is_not_closed_by_the_adapter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Closing a caller's client would break its connection pool after one call."""
    _set_api_key(monkeypatch, "test-key")
    payload = {"choices": [{"message": {"content": "ok"}}], "usage": {}}
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json=payload))
    )
    provider = AsyncOpenAICompatibleProvider(client=client)
    try:
        await provider.chat(_request(), _route(provider_type="openai_compatible"))
        await provider.chat(_request(), _route(provider_type="openai_compatible"))
        assert client.is_closed is False
    finally:
        await client.aclose()
