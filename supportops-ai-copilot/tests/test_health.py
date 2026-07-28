# ============================================================================
# FILE: tests/test_health.py
#
# WHAT THIS TESTS: the /health and /ready endpoints, plus the CORS setup.
#
# HOW TESTS WORK IN THIS PROJECT, since this is a good first one to read:
#   - Any function named test_* is run automatically by pytest.
#   - `assert X == Y` states what must be true. If it is not, the test fails and
#     pytest shows both values.
#   - No test touches a real database or a real network. The tricks that make
#     that possible are explained below.
#
# THE TWO TOOLS USED HERE:
#
#   TestClient - a fake browser. It sends requests straight into the application
#     object without starting a real web server or opening a network port. So
#     the tests exercise the genuine routing, validation, and response code, and
#     still run in milliseconds.
#
#   monkeypatch - pytest's tool for temporarily REPLACING something during one
#     test. Here it swaps the real "is the database reachable?" function for one
#     that simply returns a chosen answer. That is what allows a test of
#     "behaviour when the database is down" WITHOUT having to break a database.
#
#     The important part: monkeypatch undoes itself automatically when the test
#     finishes, so the replacement cannot leak into other tests.
#
# WHY THESE ENDPOINTS ARE WORTH TESTING AT ALL: their STATUS CODES are what
# deployment systems act on. A /ready that wrongly answers 200 while the
# database is down would have the load balancer send real users to an app that
# cannot serve them. That is precisely what the two 503 tests below protect.
# ============================================================================

from fastapi.testclient import TestClient

from supportops_api.checks import CheckResult
from supportops_api.main import create_app
from supportops_api.settings import get_settings


# The simplest case: is the app alive and answering?
#
# Note `create_app()` builds a FRESH application for this test, rather than
# importing the shared one. That is why main.py keeps app creation in a function
# — each test gets its own isolated instance.
def test_health_returns_ok() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    # Checks the app name too, confirming the settings were actually loaded
    # rather than the endpoint returning a hard-coded string.
    assert response.json()["app"] == "supportops-ai-copilot"


# Everything is reachable -> 200 and "ready".
def test_ready_returns_ok_when_dependencies_are_available(monkeypatch) -> None:
    # Replaces the real check functions with ones that always report success.
    #
    # NOTE THE PATH BEING PATCHED: "supportops_api.routes.health.check_database",
    # not "supportops_api.checks.check_database". A subtle and commonly-mistaken
    # point — you must patch the name WHERE IT IS USED, not where it is defined.
    # health.py did `from ...checks import check_database`, which made its own
    # reference to that function, and it is that reference which must be
    # replaced.
    #
    # `lambda settings: ...` is a one-line throwaway function accepting the same
    # argument the real one does.
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
    # Checks the full structure of the reply, not just the status. That matters
    # because monitoring tools read these individual fields to work out WHICH
    # dependency is broken.
    assert body["checks"]["config"] is True
    assert body["checks"]["database"]["ok"] is True
    assert body["checks"]["redis"]["ok"] is True


# The database is down -> 503, and the reply says which one failed.
#
# THE MOST IMPORTANT TEST IN THIS FILE. 503 is what tells a load balancer to stop
# sending traffic here. If this ever regressed to returning 200, the failure
# would be invisible in normal operation and only surface as users hitting errors
# during an outage.
def test_ready_returns_503_when_database_is_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(
        "supportops_api.routes.health.check_database",
        lambda settings: CheckResult(ok=False, error="OperationalError"),
    )
    # Redis is deliberately left healthy, so this proves ONE failure is enough.
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
    # Confirms the healthy dependency is still reported as healthy — so the
    # response identifies exactly what is broken rather than condemning
    # everything at once.
    assert body["checks"]["redis"]["ok"] is True


# The mirror image: Redis down, database fine. Written separately rather than
# combined, because each dependency needs proving independently — a bug that
# only checked the database would pass a combined test.
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


# CORS: can the web console actually call this API from a browser?
#
# Worth testing because a CORS misconfiguration produces a particularly nasty
# failure — the API works perfectly when tested with curl, and the browser
# silently blocks every request. Symptoms that look like a front-end bug.
def test_cors_allows_configured_web_origin(monkeypatch) -> None:
    origin = "http://127.0.0.1:3000"
    # Sets the environment variable for the duration of this test only.
    monkeypatch.setenv("CORS_ORIGINS", origin)

    # THE CACHE-CLEARING IS ESSENTIAL, and easy to overlook.
    #
    # get_settings() is decorated with @lru_cache, so it reads the environment
    # ONCE and returns the same object forever. Without clearing that cache, this
    # test would get whatever settings a previous test had already loaded, and
    # the new CORS_ORIGINS value would be ignored entirely.
    get_settings.cache_clear()

    try:
        with TestClient(create_app()) as client:
            # An OPTIONS request is the browser's "preflight" — the permission
            # check it sends BEFORE the real request, asking whether it is
            # allowed. Testing this is testing what the browser actually does.
            response = client.options(
                "/health",
                headers={
                    "Origin": origin,
                    "Access-Control-Request-Method": "GET",
                },
            )
    finally:
        # `finally` guarantees the cache is cleared again even if the assertions
        # fail. Without it, a failing test would leave the modified settings
        # cached and cause unrelated tests afterwards to fail mysteriously —
        # the classic symptom of test pollution.
        get_settings.cache_clear()

    assert response.status_code == 200
    # The header the browser looks for. Its absence is exactly what makes a
    # browser refuse the call.
    assert response.headers["access-control-allow-origin"] == origin
