"""Rate limiting middleware tests.

A gateway request can cost real money and hold a worker for tens of seconds, so
the limiter is a budget control as much as a traffic control.

The tests build a minimal app with the same middleware stack as `create_app`
rather than calling the real gateway endpoints. Those endpoints reach
PostgreSQL, and the limiter's behavior has nothing to do with the database —
routing a middleware test through it would only make the test slow and
skip-dependent.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.api.app import create_app
from apps.api.middleware.rate_limit import RateLimitMiddleware
from apps.api.middleware.request_id import RequestIdMiddleware
from packages.core.config import Settings

GUARDED_PATH = "/api/v1/model-gateway/chat"
UNGUARDED_PATH = "/api/v1/health/live"


def _app(requests_per_minute: int) -> TestClient:
    """Build a test app with the production middleware order."""
    app = FastAPI()

    @app.post(GUARDED_PATH)
    def guarded() -> dict[str, str]:
        return {"status": "ok"}

    @app.get(UNGUARDED_PATH)
    def unguarded() -> dict[str, str]:
        return {"status": "ok"}

    # Same order as create_app: the limiter is added first, so RequestIdMiddleware
    # wraps it and request_id is already set when a 429 is built.
    app.add_middleware(RateLimitMiddleware, requests_per_minute=requests_per_minute)
    app.add_middleware(RequestIdMiddleware)
    return TestClient(app)


def test_limiter_is_disabled_by_default() -> None:
    """Zero must mean off, so local development and tests are unaffected."""
    assert Settings(_env_file=None).rate_limit_requests_per_minute == 0

    client = _app(0)
    for _ in range(10):
        assert client.post(GUARDED_PATH).status_code == 200


def test_unguarded_paths_are_never_limited() -> None:
    """Health checks must keep working while the gateway is being throttled.

    A limiter that also throttles liveness would get the process killed by its
    own orchestrator during exactly the traffic spike it is meant to survive.
    """
    client = _app(2)

    for _ in range(10):
        assert client.get(UNGUARDED_PATH).status_code == 200


def test_guarded_path_is_refused_after_the_limit() -> None:
    client = _app(3)

    statuses = [client.post(GUARDED_PATH).status_code for _ in range(5)]

    assert statuses == [200, 200, 200, 429, 429]


def test_rate_limited_response_uses_the_standard_error_envelope() -> None:
    client = _app(1)

    client.post(GUARDED_PATH)
    response = client.post(GUARDED_PATH)

    assert response.status_code == 429
    body = response.json()
    assert body["error"]["code"] == "rate_limited"
    assert body["error"]["details"]["retry_after_seconds"] >= 1
    # Retry-After is what makes a 429 actionable instead of an invitation to
    # retry immediately.
    assert int(response.headers["Retry-After"]) >= 1


def test_request_id_is_present_on_a_rate_limited_response() -> None:
    """Middleware ordering regression guard.

    RequestIdMiddleware has to wrap the limiter, or a 429 loses the one field
    that makes it traceable back to a log line.
    """
    client = _app(1)

    client.post(GUARDED_PATH)
    response = client.post(GUARDED_PATH)

    assert response.json()["error"]["request_id"]


def test_the_real_app_wires_the_limiter_from_settings() -> None:
    """The middleware must actually be installed by create_app, not just exist."""
    app = create_app(Settings(_env_file=None, rate_limit_requests_per_minute=5))

    installed = [middleware.cls for middleware in app.user_middleware]

    assert RateLimitMiddleware in installed
    assert RequestIdMiddleware in installed
