from fastapi import APIRouter
from fastapi.responses import JSONResponse

from supportops_api.checks import CheckResult, check_database, check_redis
from supportops_api.settings import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


@router.get("/ready")
def ready() -> JSONResponse:
    settings = get_settings()

    database = check_database(settings)
    redis_result = check_redis(settings)
    is_ready = database.ok and redis_result.ok

    payload = {
        "status": "ready" if is_ready else "not_ready",
        "checks": {
            "config": True,
            "database": _check_payload(database),
            "redis": _check_payload(redis_result),
        },
    }
    return JSONResponse(status_code=200 if is_ready else 503, content=payload)


def _check_payload(result: CheckResult) -> dict[str, object]:
    payload: dict[str, object] = {"ok": result.ok}
    if result.error:
        payload["error"] = result.error
    return payload
