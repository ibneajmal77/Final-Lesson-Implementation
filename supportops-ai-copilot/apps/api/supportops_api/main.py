# ============================================================================
# FILE: apps/api/supportops_api/main.py
#
# THINK OF THIS FILE AS: the front door and the assembly line of the API.
#
# This is the starting point of the whole web service. When the server is
# started (see Dockerfile.api, which runs `uvicorn supportops_api.main:app`),
# this file runs and builds the application object. Its jobs are:
#   1. Switch logging on
#   2. Decide which web pages are allowed to call us (CORS)
#   3. Install the "middleware" that times and logs every single request
#   4. Plug in all the route files, which hold the actual endpoints
#
# WHAT "MIDDLEWARE" MEANS:
#   A wrapper that sits around every request, like airport security everyone
#   must pass through both on the way in and on the way out. It runs before the
#   route does its work and again after, which makes it the perfect place to
#   start a stopwatch and write a log line.
#
# THE FULL PICTURE:
#   web page (apps/web/src/app.js)
#     -> nginx (apps/web/nginx.conf) forwards /api requests here
#          -> THIS FILE: log, time, and tag the request
#               -> dependencies.py: check who is calling, open the database
#                    -> routes/*.py: the actual work
# ============================================================================

import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Each route file groups related endpoints together. They are all imported here
# and switched on below. "router as X_router" simply renames each one on import
# so the five identically-named `router` objects don't clash.
from supportops_api.routes.approvals import router as approvals_router  # approve/reject AI drafts
from supportops_api.routes.health import router as health_router  # "are you alive?" checks
from supportops_api.routes.metrics import router as metrics_router  # usage and cost numbers
from supportops_api.routes.policies import router as policies_router  # safety rules
from supportops_api.routes.tickets import router as tickets_router  # tickets and AI analysis
from supportops_api.settings import Settings, get_settings
from supportops_observability.logging import configure_json_logging, get_logger, log_context
from supportops_observability.tracing import trace_span

# The name of the header carrying a unique ID for each request. If one request
# touches the API, then the worker, then the database, this shared ID is what
# lets you search the logs and follow that single journey end to end. It is
# read from the incoming request if present, and always sent back in the reply.
REQUEST_ID_HEADER = "X-Request-Id"
logger = get_logger(__name__)


# Builds the application. Kept as a function (rather than written straight out
# at the top level) so that the tests can call it to create their own fresh,
# isolated copy of the app — see tests/test_health.py.
def create_app() -> FastAPI:
    settings = get_settings()
    configure_json_logging(settings.log_level)   # logs as machine-readable JSON, not loose text,
                                                 # so tools can search and filter them
    app = FastAPI(title=settings.app_name)
    _add_cors_middleware(app, settings)
    _add_observability_middleware(app)

    # Registering the route files. Order matters only in unusual cases, but the
    # cheap, dependency-free health checks are deliberately put first.
    app.include_router(health_router)
    app.include_router(metrics_router)
    app.include_router(policies_router)
    app.include_router(approvals_router)
    app.include_router(tickets_router)
    return app


# Tells browsers which web pages are permitted to call this API.
#
# Browsers block a page hosted at one address from calling an API at a
# different address unless the API explicitly permits it. That rule is called
# CORS. Without this, the dashboard would silently fail to load any data.
def _add_cors_middleware(app: FastAPI, settings: Settings) -> None:
    origins = _cors_origins(settings.cors_origins)
    if not origins:
        return          # nothing configured -> permit nothing. The safe default.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,       # only these exact web addresses
        allow_credentials=False,     # don't let browsers attach cookies to these calls
        allow_methods=["*"],         # any action (GET, POST, ...) is fine from those addresses
        allow_headers=["*"],         # any header is fine — needed for our X-Tenant-Id etc.
    )


# Turns the single setting string "http://a.com, http://b.com" into a proper
# list ["http://a.com", "http://b.com"]. The `if origin.strip()` at the end
# throws away empty pieces, so a stray trailing comma doesn't create a blank
# entry that would never match anything.
def _cors_origins(raw_origins: str) -> list[str]:
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

# Installs the wrapper that measures and records every request.
#
# This is where "observability" comes from — the ability to look at a running
# system and understand what it is doing. Three things are produced for every
# single request: a stopwatch reading, a log line, and a trace.
def _add_observability_middleware(app: FastAPI) -> None:
    # The "@app.middleware("http")" line registers the function below as the
    # wrapper described in the file header. `call_next` is the rest of the app:
    # calling it is what actually lets the request through to its route.
    @app.middleware("http")
    async def observability_middleware(request: Request, call_next):
        # Reuse the caller's request ID if they supplied one — that way a
        # journey that began in another service keeps the same ID all the way
        # through, and the logs of both services line up.
        request_id = request.headers.get(REQUEST_ID_HEADER) or request.scope.get("request_id")
        if not isinstance(request_id, str) or not request_id:
            # No usable ID supplied, so invent a fresh one. Imported here rather
            # than at the top purely to keep this rarely-needed helper out of
            # the startup path.
            from supportops_observability.logging import new_request_id

            request_id = new_request_id()

        route = request.url.path
        started = time.perf_counter()    # perf_counter is a precise stopwatch, meant for
                                         # measuring durations (unlike a wall clock, it can't
                                         # jump backwards when the system clock is adjusted)

        # Two wrappers, both from the observability package:
        #   log_context - attaches these details to EVERY log line written
        #                 while inside this block, including ones written deep
        #                 inside route and database code. Saves passing them
        #                 down through every function by hand.
        #   trace_span  - records this request as one timed step in a "trace",
        #                 the timeline view of a request crossing services.
        with log_context(
            request_id=request_id,
            tenant_id=request.headers.get("X-Tenant-Id"),
            user_id=request.headers.get("X-User-Id"),
            route=route,
        ), trace_span(
            "api.request",
            request_id=request_id,
            route=route,
            method=request.method,
        ):
            try:
                response = await call_next(request)   # <-- the route runs here
            except Exception as exc:
                # Something broke. Record how long it took and what went wrong...
                duration_ms = int((time.perf_counter() - started) * 1000)
                logger.exception(       # .exception also captures the full error trace
                    "api_request_failed",
                    extra={
                        "method": request.method,
                        "duration_ms": duration_ms,
                        "error_code": exc.__class__.__name__,   # the error's type name
                    },
                )
                raise                   # ...then let the error continue upwards. We are only
                                        # observing here, never swallowing failures — hiding one
                                        # would leave the caller with no idea anything went wrong.

            # The happy path: stop the clock, stamp the reply with the request
            # ID (so a user reporting a problem can quote it), and log the result.
            duration_ms = int((time.perf_counter() - started) * 1000)
            response.headers[REQUEST_ID_HEADER] = request_id
            logger.info(
                "api_request_completed",
                extra={
                    "method": request.method,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                },
            )
            return response


# The finished application object. The web server (uvicorn) looks for exactly
# this name — "supportops_api.main:app" in Dockerfile.api means "the thing
# called `app` inside the file supportops_api/main.py".
app = create_app()
