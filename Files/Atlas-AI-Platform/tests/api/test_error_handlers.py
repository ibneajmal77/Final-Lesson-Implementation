"""API tests for global validation, domain, and unexpected-error handlers."""

from fastapi.testclient import TestClient
from pydantic import BaseModel

from apps.api.app import create_app
from packages.core.config import Settings
from packages.core.errors import AppError


class DemoPayload(BaseModel):
    count: int


def _test_settings() -> Settings:
    return Settings(_env_file=None)


def test_validation_errors_use_standard_error_envelope() -> None:
    app = create_app(_test_settings())

    @app.post("/demo/validated")
    def validated(payload: DemoPayload) -> dict[str, int]:
        return {"count": payload.count}

    client = TestClient(app)

    response = client.post("/demo/validated", json={"count": "not-an-int"})

    body = response.json()
    assert response.status_code == 422
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["message"] == "Request validation failed."
    assert body["error"]["request_id"] == response.headers["x-request-id"]
    assert body["error"]["details"]["errors"]


def test_unexpected_errors_are_hidden_and_traced() -> None:
    app = create_app(_test_settings())

    @app.get("/demo/unexpected")
    def unexpected() -> None:
        raise RuntimeError("secret database password is atlas")

    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/demo/unexpected")

    body = response.json()
    assert response.status_code == 500
    assert body["error"]["code"] == "internal_error"
    assert body["error"]["message"] == "An unexpected error occurred."
    assert body["error"]["details"] == {}
    assert body["error"]["request_id"] == response.headers["x-request-id"]
    assert "secret database password" not in response.text


def test_app_errors_use_standard_error_envelope() -> None:
    app = create_app(_test_settings())

    @app.get("/demo/app-error")
    def app_error() -> None:
        raise AppError(code="demo_failed", message="Demo failed.", status_code=409)

    client = TestClient(app)

    response = client.get("/demo/app-error")

    body = response.json()
    assert response.status_code == 409
    assert body["error"]["code"] == "demo_failed"
    assert body["error"]["request_id"] == response.headers["x-request-id"]
