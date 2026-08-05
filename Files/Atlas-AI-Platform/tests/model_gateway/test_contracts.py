"""Tests that provider adapters satisfy the gateway request/response contracts."""

from uuid import uuid4

from packages.model_gateway.providers.mock import MockProvider
from packages.model_gateway.types import ChatMessage, ModelRequest, SelectedRoute


def test_mock_provider_implements_chat_and_embedding_contracts() -> None:
    provider = MockProvider()
    route = SelectedRoute(
        route_id=uuid4(),
        route_key="chat_primary",
        use_case="chat",
        provider_name="mock_public",
        provider_type="mock",
        model_name="mock-chat-v1",
        max_input_tokens=4000,
        max_output_tokens=800,
        timeout_seconds=30,
        temperature=None,
        restricted_data_allowed=False,
        fallback_route_id=None,
        route_config={},
        capabilities={"supports_chat": True, "supports_embeddings": True},
        data_policy={"restricted_data_allowed": False},
        max_cost_usd=None,
        embedding_dimension=4,
    )
    request = ModelRequest(
        tenant_id=uuid4(),
        use_case="chat",
        messages=(ChatMessage(role="user", content="hello"),),
        inputs=("alpha", "beta"),
    )

    chat = provider.chat(request, route)
    embedding = provider.embed(request, route)

    assert chat.content == "mock:chat:hello"
    assert chat.usage.input_tokens == 1
    assert len(embedding.embeddings) == 2
    assert all(len(vector) == 4 for vector in embedding.embeddings)
