"""Request-id middleware and async request context wiring.

This is the Python/FastAPI equivalent of correlation-id middleware in ASP.NET
Core. It reads or creates an `x-request-id`, stores it on the request, and puts
it in a `ContextVar` so deeper code can log it without passing it everywhere.
"""

from collections.abc import Awaitable, Callable
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from packages.core.request_context import reset_request_id, set_request_id

REQUEST_ID_HEADER = "x-request-id"


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Starlette/FastAPI middleware class.

    Python note: inheriting `BaseHTTPMiddleware` is like deriving from a base
    middleware type. FastAPI calls `dispatch` for every HTTP request.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        # `self` is Python's explicit instance parameter, equivalent to `this`
        # in C# except it must be written in the method signature.
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid4())
        request.state.request_id = request_id
        # `set_request_id` returns a token so the previous async context can be
        # restored even when route handling raises an exception.
        token = set_request_id(request_id)
        try:
            response = await call_next(request)
        finally:
            reset_request_id(token)

        response.headers[REQUEST_ID_HEADER] = request_id
        return response
