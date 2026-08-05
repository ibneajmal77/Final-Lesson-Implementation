"""Seed deterministic model gateway providers and routes.

This is development/CI bootstrap data, similar to EF seed data. It creates mock
providers and default routes so the gateway and prompt tests can run without
real AI-provider credentials.
"""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.db.models.model_gateway import ModelProvider, ModelRoute


def ensure_default_gateway_config(session: Session) -> None:
    """Insert missing default providers/routes and wire fallback route ids."""
    providers = {
        "mock_public": _provider(
            name="mock_public",
            restricted_data_allowed=False,
        ),
        "mock_private": _provider(
            name="mock_private",
            restricted_data_allowed=True,
        ),
        "openai_primary": _provider(
            name="openai_primary",
            provider_type="openai_compatible",
            restricted_data_allowed=False,
            status="disabled",
        ),
    }
    existing_provider_names = set(
        session.scalars(select(ModelProvider.name).where(ModelProvider.name.in_(providers))).all()
    )
    for name, provider in providers.items():
        if name not in existing_provider_names:
            session.add(provider)
    session.flush()

    provider_by_name = {
        provider.name: provider
        for provider in session.scalars(
            select(ModelProvider).where(ModelProvider.name.in_(providers))
        ).all()
    }

    default_routes = [
        _route(
            "chat_primary",
            "chat",
            provider_by_name["mock_public"],
            "mock-chat-v1",
            max_input_tokens=4000,
            max_output_tokens=800,
            temperature=Decimal("0.200"),
            fallback_route_key="chat_private",
        ),
        _route(
            "chat_private",
            "chat",
            provider_by_name["mock_private"],
            "mock-private-chat-v1",
            max_input_tokens=4000,
            max_output_tokens=800,
            temperature=Decimal("0.200"),
            restricted_data_allowed=True,
        ),
        _route(
            "classification_primary",
            "classification",
            provider_by_name["mock_public"],
            "mock-classifier-v1",
            max_input_tokens=2000,
            max_output_tokens=300,
            temperature=Decimal("0.000"),
            fallback_route_key="classification_private",
        ),
        _route(
            "classification_private",
            "classification",
            provider_by_name["mock_private"],
            "mock-private-classifier-v1",
            max_input_tokens=2000,
            max_output_tokens=300,
            temperature=Decimal("0.000"),
            restricted_data_allowed=True,
        ),
        _route(
            "rag_answer_primary",
            "rag_answer",
            provider_by_name["mock_public"],
            "mock-rag-v1",
            max_input_tokens=24000,
            max_output_tokens=1800,
            temperature=Decimal("0.200"),
            fallback_route_key="rag_answer_private",
        ),
        _route(
            "rag_answer_private",
            "rag_answer",
            provider_by_name["mock_private"],
            "mock-private-rag-v1",
            max_input_tokens=16000,
            max_output_tokens=1600,
            temperature=Decimal("0.200"),
            restricted_data_allowed=True,
        ),
        _route(
            "embedding_primary",
            "embedding",
            provider_by_name["mock_public"],
            "mock-embedding-v1",
            max_input_tokens=8192,
            max_output_tokens=0,
            embedding_dimension=8,
            batch_enabled=True,
            max_batch_items=2048,
            fallback_route_key="embedding_private",
        ),
        _route(
            "embedding_private",
            "embedding",
            provider_by_name["mock_private"],
            "mock-private-embedding-v1",
            max_input_tokens=8192,
            max_output_tokens=0,
            embedding_dimension=8,
            restricted_data_allowed=True,
            batch_enabled=True,
            max_batch_items=2048,
        ),
        _route(
            "llm_judge_primary",
            "llm_judge",
            provider_by_name["mock_public"],
            "mock-judge-v1",
            max_input_tokens=12000,
            max_output_tokens=1200,
            temperature=Decimal("0.000"),
            reasoning_enabled=True,
            reasoning_effort="medium",
            reasoning_budget_tokens=2000,
        ),
    ]

    existing_route_keys = set(session.scalars(select(ModelRoute.route_key)).all())
    routes_to_add = [
        route for route in default_routes if route.route_key not in existing_route_keys
    ]
    session.add_all(routes_to_add)
    session.flush()

    # Fallbacks reference route ids, so routes are inserted first and linked in a
    # second pass after every route has a database-generated primary key.
    routes_by_key = {
        route.route_key: route for route in session.scalars(select(ModelRoute)).all()
    }
    for route in routes_by_key.values():
        fallback_route_key = route.route_config_json.get("fallback_route_key")
        if isinstance(fallback_route_key, str) and route.fallback_route_id is None:
            fallback = routes_by_key.get(fallback_route_key)
            if fallback is not None:
                route.fallback_route_id = fallback.id

    session.commit()


def _provider(
    *,
    name: str,
    restricted_data_allowed: bool,
    provider_type: str = "mock",
    status: str = "active",
) -> ModelProvider:
    """Build a provider ORM row without adding it to the session yet."""
    return ModelProvider(
        name=name,
        provider_type=provider_type,
        base_url=None,
        capabilities_json={
            "supports_chat": True,
            "supports_structured_output": provider_type == "mock",
            "supports_streaming": False,
            "supports_tool_calling": False,
            "supports_prompt_caching": False,
            "supports_batch_api": True,
            "supports_reasoning_controls": provider_type == "mock",
            "supports_embeddings": True,
        },
        data_policy_json={
            "restricted_data_allowed": restricted_data_allowed,
            "training_usage_allowed": False,
            "region": "local" if provider_type == "mock" else "provider_default",
            "retention": "none" if provider_type == "mock" else "provider_policy",
        },
        status=status,
    )


def _route(
    route_key: str,
    use_case: str,
    provider: ModelProvider,
    model_name: str,
    *,
    max_input_tokens: int,
    max_output_tokens: int,
    timeout_seconds: int = 30,
    priority: int = 1,
    temperature: Decimal | None = None,
    fallback_route_key: str | None = None,
    embedding_dimension: int | None = None,
    restricted_data_allowed: bool = False,
    batch_enabled: bool = False,
    max_batch_items: int | None = None,
    reasoning_enabled: bool = False,
    reasoning_effort: str | None = None,
    reasoning_budget_tokens: int | None = None,
) -> ModelRoute:
    """Build a route ORM row for default bootstrap configuration."""
    route_config: dict[str, object] = {}
    if fallback_route_key:
        route_config["fallback_route_key"] = fallback_route_key
    return ModelRoute(
        tenant_id=None,
        use_case=use_case,
        route_key=route_key,
        provider_id=provider.id,
        model_name=model_name,
        priority=priority,
        max_input_tokens=max_input_tokens,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        timeout_seconds=timeout_seconds,
        fallback_route_id=None,
        prompt_caching_enabled=False,
        cacheable_prefix_min_tokens=None,
        semantic_cache_enabled=False,
        batch_enabled=batch_enabled,
        max_batch_items=max_batch_items,
        embedding_dimension=embedding_dimension,
        async_only=False,
        cost_estimate_required=True,
        max_cost_usd=Decimal("0.050000"),
        route_config_json=route_config,
        reasoning_enabled=reasoning_enabled,
        reasoning_effort=reasoning_effort,
        reasoning_budget_tokens=reasoning_budget_tokens,
        restricted_data_allowed=restricted_data_allowed,
        status="active",
    )
