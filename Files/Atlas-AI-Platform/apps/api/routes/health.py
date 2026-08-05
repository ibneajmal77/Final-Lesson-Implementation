"""Health, liveness, and readiness HTTP endpoints.

The split follows common cloud hosting semantics: liveness answers "is the
process up?", while readiness also checks dependencies such as PostgreSQL and
Redis before traffic should be routed here.

Python notes for .NET reviewers:
- Functions can return plain dictionaries; FastAPI serializes them to JSON.
- `dict[str, str]` is a type hint for a dictionary with string keys and values.
- `with ... as ...` is a context manager, similar to C# `using`.
"""

from collections.abc import Callable
from typing import Any, cast

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from redis import Redis
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from packages.core.config import Settings, get_settings
from packages.db.session import get_engine

router = APIRouter(tags=["health"])
legacy_router = APIRouter(tags=["health"])


def _settings_from_request(request: Request) -> Settings:
    """Prefer test-injected app settings, otherwise use cached environment settings."""
    settings = getattr(request.app.state, "settings", None)
    if isinstance(settings, Settings):
        return settings
    return get_settings()


def check_configuration(settings: Settings) -> dict[str, str]:
    missing = []
    if not settings.api_prefix:
        missing.append("api_prefix")
    if not settings.database_url:
        missing.append("database_url")
    if not settings.redis_url:
        missing.append("redis_url")

    if missing:
        return {"status": "error", "detail": "missing:" + ",".join(missing)}
    return {"status": "ok"}


def check_database(settings: Settings) -> dict[str, str]:
    try:
        # `select 1` is the minimal database round-trip, like an EF Core
        # `CanConnect` check without touching domain tables.
        with get_engine(settings.database_url).connect() as connection:
            connection.execute(text("select 1"))
    except SQLAlchemyError as exc:
        return {"status": "error", "detail": exc.__class__.__name__}

    return {"status": "ok"}


def _close_redis_client(client: Redis) -> None:
    # `cast(...)` is only for static type checkers; it does not change the value
    # at runtime. Here it tells mypy that `client.close` is callable.
    close = cast(Callable[[], None], client.close)
    close()


def check_redis(settings: Settings) -> dict[str, str]:
    client = Redis.from_url(
        settings.redis_url,
        socket_connect_timeout=1.0,
        socket_timeout=1.0,
    )
    try:
        client.ping()
    except RedisError as exc:
        return {"status": "error", "detail": exc.__class__.__name__}
    finally:
        # `finally` always runs, even when an exception occurs, like C# finally.
        _close_redis_client(client)

    return {"status": "ok"}


@router.get("/health")
def health(request: Request) -> dict[str, str]:
    settings = _settings_from_request(request)
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.env,
    }


@legacy_router.get("/health", include_in_schema=False)
def legacy_health(request: Request) -> dict[str, str]:
    return health(request)


@router.get("/health/live")
def liveness(request: Request) -> dict[str, str]:
    settings = _settings_from_request(request)
    return {"status": "ok", "service": settings.app_name}


@router.get("/health/ready", response_model=None)
def readiness(request: Request) -> JSONResponse:
    settings = _settings_from_request(request)
    # Keep individual check results in the payload so operations can see which
    # dependency caused the 503, rather than only getting a boolean failure.
    checks = {
        "configuration": check_configuration(settings),
        "database": check_database(settings),
        "redis": check_redis(settings),
    }
    is_ready = all(check["status"] == "ok" for check in checks.values())
    payload: dict[str, Any] = {
        "status": "ready" if is_ready else "not_ready",
        "service": settings.app_name,
        "environment": settings.env,
        "checks": checks,
    }

    status_code = 200 if is_ready else 503
    return JSONResponse(status_code=status_code, content=payload)
