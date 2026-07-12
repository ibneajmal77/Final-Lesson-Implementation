from fastapi.testclient import TestClient

from supportops_api.checks import CheckResult
from supportops_api.main import create_app


def test_health_returns_ok() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["app"] == "supportops-ai-copilot"


def test_ready_returns_ok_when_dependencies_are_available(monkeypatch) -> None:
    monkeypatch.setattr(
        "supportops_api.routes.health.check_database",
        lambda settings: CheckResult(ok=True),
    )
    monkeypatch.setattr(
        "supportops_api.routes.health.check_redis",
        lambda settings: CheckResult(ok=True),
    )

    with TestClient(create_app()) as client:
        response = client.get("/ready")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["checks"]["config"] is True
    assert body["checks"]["database"]["ok"] is True
    assert body["checks"]["redis"]["ok"] is True


def test_ready_returns_503_when_database_is_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(
        "supportops_api.routes.health.check_database",
        lambda settings: CheckResult(ok=False, error="OperationalError"),
    )
    monkeypatch.setattr(
        "supportops_api.routes.health.check_redis",
        lambda settings: CheckResult(ok=True),
    )

    with TestClient(create_app()) as client:
        response = client.get("/ready")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "not_ready"
    assert body["checks"]["database"]["ok"] is False
    assert body["checks"]["database"]["error"] == "OperationalError"
    assert body["checks"]["redis"]["ok"] is True


def test_ready_returns_503_when_redis_is_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(
        "supportops_api.routes.health.check_database",
        lambda settings: CheckResult(ok=True),
    )
    monkeypatch.setattr(
        "supportops_api.routes.health.check_redis",
        lambda settings: CheckResult(ok=False, error="ConnectionError"),
    )

    with TestClient(create_app()) as client:
        response = client.get("/ready")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "not_ready"
    assert body["checks"]["database"]["ok"] is True
    assert body["checks"]["redis"]["ok"] is False
    assert body["checks"]["redis"]["error"] == "ConnectionError"
