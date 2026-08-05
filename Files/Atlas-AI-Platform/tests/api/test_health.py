"""API tests for health, liveness, readiness, and configurable route prefixes."""

from typing import Any

from fastapi.testclient import TestClient

from apps.api.app import create_app
from packages.core.config import Settings


def _test_settings() -> Settings:
    return Settings(_env_file=None)


def test_versioned_health_returns_status_and_request_id() -> None:
    client = TestClient(create_app(_test_settings()))

    response = client.get("/api/v1/health")

    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "ok"
    assert body["environment"] == "local"
    assert "env" not in body
    assert "x-request-id" in response.headers


def test_legacy_health_alias_still_works() -> None:
    client = TestClient(create_app(_test_settings()))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_liveness_returns_process_status() -> None:
    client = TestClient(create_app(_test_settings()))

    response = client.get("/api/v1/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Atlas AI Platform"}


def test_readiness_returns_ready_when_dependencies_are_available(monkeypatch: Any) -> None:
    monkeypatch.setattr(
        "apps.api.routes.health.check_database",
        lambda settings: {"status": "ok"},
    )
    monkeypatch.setattr(
        "apps.api.routes.health.check_redis",
        lambda settings: {"status": "ok"},
    )
    client = TestClient(create_app(_test_settings()))

    response = client.get("/api/v1/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["checks"]["database"] == {"status": "ok"}
    assert response.json()["checks"]["redis"] == {"status": "ok"}


def test_readiness_returns_503_when_dependency_fails(monkeypatch: Any) -> None:
    monkeypatch.setattr(
        "apps.api.routes.health.check_database",
        lambda settings: {"status": "error", "detail": "OperationalError"},
    )
    monkeypatch.setattr(
        "apps.api.routes.health.check_redis",
        lambda settings: {"status": "ok"},
    )
    client = TestClient(create_app(_test_settings()))

    response = client.get("/api/v1/health/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["checks"]["database"]["detail"] == "OperationalError"

def test_health_router_uses_configured_api_prefix() -> None:
    client = TestClient(create_app(Settings(_env_file=None, api_prefix="/internal")))

    response = client.get("/internal/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
