# ============================================================================
# FILE: apps/api/supportops_api/routes/health.py
#
# THINK OF THIS FILE AS: the app's pulse check, for machines rather than people.
#
# It provides two endpoints that nobody browses to by hand, but that automated
# systems call constantly:
#
#   GET /health  - "is this program running at all?"      (liveness)
#   GET /ready   - "is it able to do useful work yet?"    (readiness)
#
# WHY TWO, AND WHY THE DIFFERENCE MATTERS:
#   They trigger different reactions from the systems watching them.
#     /health failing  -> the program is stuck or dead. RESTART it.
#     /ready  failing  -> the program is fine, but something it depends on
#                         (the database, Redis) is not. Do NOT restart it —
#                         restarting wouldn't fix a broken database. Just stop
#                         sending it traffic until it recovers.
#   Getting this pair backwards is a classic cause of restart storms, where a
#   brief database outage makes every copy of the app restart in a loop.
#
#   That is also why /health deliberately checks NOTHING external. It only
#   proves this process is awake and able to answer.
#
# WHO USES IT:
#   apps/api/supportops_api/checks.py - supplies the actual test functions
#   docker-compose.yml                - its `healthcheck:` sections call these
#   tests/test_health.py              - the tests covering this file
# ============================================================================

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from supportops_api.checks import CheckResult, check_database, check_redis
from supportops_api.settings import get_settings

# An APIRouter is a group of related endpoints, collected here and then plugged
# into the main app by main.py. The "tags" value only affects presentation: it
# is the heading these endpoints appear under in the automatic API docs page
# that FastAPI generates at /docs.
#
# Unlike the other route files, this one sets no `prefix`, so the paths below
# are exactly /health and /ready, sitting at the very top level.
router = APIRouter(tags=["health"])


# Liveness. Answers immediately, touching no database and no network.
#
# Note there is no `actor` argument here, which means this endpoint requires no
# identity headers — anyone can call it. That is intentional: the monitoring
# system checking it has no user account, and this reveals nothing sensitive.
@router.get("/health")
def health() -> dict[str, str]:
    settings = get_settings()
    # Returning the app name and environment is a small but genuinely useful
    # touch: when you can reach *something* but aren't sure what, this tells you
    # whether you are looking at staging or production.
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


# Readiness. Actually goes and pokes each dependency, then reports back.
@router.get("/ready")
def ready() -> JSONResponse:
    settings = get_settings()

    # Try both, always. Note it does not stop at the first failure — knowing
    # "the database is down AND Redis is down" is far more useful when
    # diagnosing a problem than only ever hearing about the first one.
    database = check_database(settings)
    redis_result = check_redis(settings)
    is_ready = database.ok and redis_result.ok      # ready only if EVERYTHING is ready

    payload = {
        "status": "ready" if is_ready else "not_ready",
        "checks": {
            # "config" is always True by the time we get here: the settings
            # were loaded successfully at startup, or the app would never have
            # started at all. It is listed so the report covers every
            # dependency, rather than silently omitting one.
            "config": True,
            "database": _check_payload(database),
            "redis": _check_payload(redis_result),
        },
    }

    # A plain JSONResponse is returned instead of a dictionary because the HTTP
    # status code needs to be set by hand. That code is the part machines act
    # on, and it must be honest:
    #   200 = OK, send me traffic
    #   503 = Service Unavailable, hold off for now
    # Returning 200 with a body saying "not_ready" would be worse than useless:
    # most load balancers only look at the code, so they would keep sending
    # users to an app that cannot serve them.
    return JSONResponse(status_code=200 if is_ready else 503, content=payload)


# Turns one CheckResult into the small dictionary shown in the reply.
# The "error" key is left out entirely when things are fine, so a healthy
# response stays clean rather than carrying a row of empty fields.
def _check_payload(result: CheckResult) -> dict[str, object]:
    payload: dict[str, object] = {"ok": result.ok}
    if result.error:
        payload["error"] = result.error
    return payload
