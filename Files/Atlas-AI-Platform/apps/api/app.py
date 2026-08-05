"""FastAPI application factory and global exception handling.

For a .NET reviewer, this file plays the role of `Program.cs` plus global
exception middleware: it creates the web host, registers middleware, maps
feature routers, and converts domain exceptions into stable JSON responses.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from apps.api.middleware.request_id import REQUEST_ID_HEADER, RequestIdMiddleware
from apps.api.routes.ai_runs import router as ai_runs_router
from apps.api.routes.health import legacy_router as legacy_health_router
from apps.api.routes.health import router as health_router
from apps.api.routes.model_gateway import router as model_gateway_router
from apps.api.routes.prompts import router as prompts_router
from packages.core.config import Settings, get_settings
from packages.core.errors import AppError, error_payload
from packages.core.logging import configure_logging

logger = logging.getLogger(__name__)


def _error_response(error: AppError, request_id: str | None) -> JSONResponse:
    """Translate an application exception into the shared API error envelope."""
    response = JSONResponse(
        status_code=error.status_code,
        content=error_payload(error, request_id=request_id),
    )
    if request_id:
        response.headers[REQUEST_ID_HEADER] = request_id
    return response


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and configure the FastAPI application.

    Python note: `Settings | None` means "Settings or null" and is the same idea
    as `Settings?` in C#. The default `None` lets tests pass custom settings
    while production uses environment-loaded settings.
    """
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title=settings.app_name, version="0.1.0")
    # `app.state` is FastAPI's small application-wide bag, similar to storing
    # validated options on ASP.NET Core's service container for later retrieval.
    app.state.settings = settings
    app.add_middleware(RequestIdMiddleware)
    # Routers are feature modules. The app-level prefix keeps route modules free
    # to declare only their local paths such as `/health` or `/model-gateway`.
    app.include_router(health_router, prefix=settings.api_prefix)
    app.include_router(model_gateway_router, prefix=settings.api_prefix)
    app.include_router(ai_runs_router, prefix=settings.api_prefix)
    app.include_router(prompts_router, prefix=settings.api_prefix)
    app.include_router(legacy_health_router)

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        # `@app.exception_handler(...)` is a decorator. It registers the function
        # with FastAPI, similar to applying configuration in ASP.NET middleware.
        # `async def` declares an awaitable handler even though this body does not
        # currently await anything; FastAPI supports both sync and async handlers.
        request_id = getattr(request.state, "request_id", None)
        return _error_response(exc, request_id)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        # FastAPI/Pydantic validation errors are normalized to the same envelope
        # used by domain errors so clients have one response shape to parse.
        error = AppError(
            code="validation_error",
            message="Request validation failed.",
            status_code=422,
            details={"errors": jsonable_encoder(exc.errors())},
        )
        return _error_response(error, request_id)

    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        # Log the real exception server-side, but do not leak internals to the
        # HTTP client. This mirrors production ASP.NET Core exception handling.
        logger.exception(
            "Unhandled API exception",
            extra={"path": request.url.path, "request_id": request_id},
        )
        error = AppError(
            code="internal_error",
            message="An unexpected error occurred.",
            status_code=500,
        )
        return _error_response(error, request_id)

    return app
