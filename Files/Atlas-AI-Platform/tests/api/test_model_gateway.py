"""API tests for model gateway chat, embedding, route listing, and AI run lookup."""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from apps.api.app import create_app
from packages.core.config import Settings
from packages.db.models.identity import Tenant
from packages.db.session import get_engine, get_session_factory


def _client() -> TestClient:
    return TestClient(create_app(Settings(_env_file=None)))


def _tenant_id() -> str:
    try:
        with get_engine().connect() as connection:
            connection.execute(text("select 1"))
    except SQLAlchemyError as exc:
        pytest.skip(f"database unavailable for model gateway API tests: {exc.__class__.__name__}")
    session = get_session_factory()()
    try:
        suffix = uuid4().hex
        tenant = Tenant(name=f"API Tenant {suffix}", slug=f"api-tenant-{suffix}")
        session.add(tenant)
        session.commit()
        session.refresh(tenant)
        return str(tenant.id)
    finally:
        session.close()


def test_model_gateway_chat_endpoint_returns_ai_run_id() -> None:
    tenant_id = _tenant_id()
    response = _client().post(
        "/api/v1/model-gateway/chat",
        json={
            "tenant_id": tenant_id,
            "messages": [{"role": "user", "content": "hello from api"}],
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ai_run_id"]
    assert body["content"] == "mock:chat:hello from api"
    assert body["provider_name"] == "mock_public"
    assert body["usage"]["input_tokens"] == 3


def test_model_gateway_embed_endpoint_returns_vectors() -> None:
    tenant_id = _tenant_id()
    response = _client().post(
        "/api/v1/model-gateway/embed",
        json={"tenant_id": tenant_id, "inputs": ["alpha", "beta"]},
    )

    body = response.json()
    assert response.status_code == 200
    assert len(body["embeddings"]) == 2
    assert len(body["embeddings"][0]) == 8


def test_ai_run_detail_endpoint_returns_usage_and_cost() -> None:
    tenant_id = _tenant_id()
    client = _client()
    chat_response = client.post(
        "/api/v1/model-gateway/chat",
        json={
            "tenant_id": tenant_id,
            "messages": [{"role": "user", "content": "show run"}],
        },
    )
    ai_run_id = chat_response.json()["ai_run_id"]

    response = client.get(f"/api/v1/ai-runs/{ai_run_id}")

    body = response.json()
    assert response.status_code == 200
    assert body["id"] == ai_run_id
    assert body["status"] == "succeeded"
    assert body["input_tokens"] == 2
    assert body["estimated_cost_usd"] is not None


def test_route_listing_returns_gateway_columns() -> None:
    response = _client().get("/api/v1/model-gateway/routes")

    body = response.json()
    assert response.status_code == 200
    route_keys = {route["route_key"] for route in body}
    assert {"chat_primary", "embedding_primary", "llm_judge_primary"}.issubset(route_keys)
