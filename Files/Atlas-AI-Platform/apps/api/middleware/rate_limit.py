"""Per-client rate limiting for expensive endpoints.

An LLM gateway is not a normal API surface: one request can cost real money and
occupy a worker for tens of seconds. Without a limit, a single misbehaving
client — or a retry loop in someone else's code — can drain a budget before
anyone notices.

The implementation is a fixed-window counter held **in process memory**, and
that limitation is deliberate and worth stating plainly: with more than one
worker process, each has its own counters, so the effective limit is the
configured value multiplied by the number of workers. That is acceptable as a
blunt safety valve and is not acceptable as a billing control. A shared limiter
belongs in Redis (the dependency is already present); this is the local
guardrail, not the finished feature.

Disabled by default (`ATLAS_RATE_LIMIT_REQUESTS_PER_MINUTE=0`), so tests and
local development are unaffected.

Python notes for .NET reviewers:
- `BaseHTTPMiddleware` is Starlette's middleware base, similar to an ASP.NET
  Core middleware component with `InvokeAsync`.
- `defaultdict(list)` returns an empty list for a key that was never set.
"""

from __future__ import annotations

import time
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from packages.core.errors import AppError, error_payload

WINDOW_SECONDS = 60.0


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Reject a client that exceeds `requests_per_minute` on guarded paths."""

    def __init__(
        self,
        app: Callable[..., Awaitable[None]],
        *,
        requests_per_minute: int,
        guarded_path_fragments: tuple[str, ...] = ("/model-gateway", "/prompts"),
    ) -> None:
        super().__init__(app)
        self._requests_per_minute = requests_per_minute
        self._guarded = guarded_path_fragments
        self._hits: dict[str, list[float]] = defaultdict(list)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Any]],
    ) -> Any:
        if self._requests_per_minute <= 0 or not self._is_guarded(request.url.path):
            return await call_next(request)

        client_key = self._client_key(request)
        now = time.monotonic()
        recent = [stamp for stamp in self._hits[client_key] if now - stamp < WINDOW_SECONDS]

        if len(recent) >= self._requests_per_minute:
            # Keep the pruned list so a client that keeps hammering does not
            # grow the bucket without bound while it is being refused.
            self._hits[client_key] = recent
            retry_after = int(WINDOW_SECONDS - (now - recent[0])) + 1
            return self._too_many_requests(request, retry_after)

        recent.append(now)
        self._hits[client_key] = recent
        return await call_next(request)

    def _is_guarded(self, path: str) -> bool:
        return any(fragment in path for fragment in self._guarded)

    def _client_key(self, request: Request) -> str:
        """Identify the caller.

        Until real authentication exists, the client host is the only stable
        identifier available. Once tenant identity is bound to a request, this
        should key on tenant so one tenant cannot exhaust another's allowance.
        """
        client = request.client
        return client.host if client else "unknown"

    def _too_many_requests(self, request: Request, retry_after: int) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        error = AppError(
            code="rate_limited",
            message="Too many requests. Slow down and retry later.",
            status_code=429,
            details={"retry_after_seconds": retry_after},
        )
        response = JSONResponse(
            status_code=429,
            content=error_payload(error, request_id=request_id),
        )
        # `Retry-After` is what makes a 429 actionable for a well-behaved
        # client, instead of an invitation to retry immediately.
        response.headers["Retry-After"] = str(retry_after)
        return response
