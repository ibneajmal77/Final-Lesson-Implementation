"""Async-local request context.

`ContextVar` is Python's async-safe equivalent of storing correlation data in
`AsyncLocal<T>` in .NET. Middleware sets the request id once, and logging can
read it later from any code running in the same request context.
"""

from contextvars import ContextVar, Token

_request_id: ContextVar[str | None] = ContextVar("atlas_request_id", default=None)


def set_request_id(request_id: str) -> Token[str | None]:
    """Set the request id and return a token that can restore the old value."""
    return _request_id.set(request_id)


def reset_request_id(token: Token[str | None]) -> None:
    _request_id.reset(token)


def get_request_id() -> str | None:
    return _request_id.get()
