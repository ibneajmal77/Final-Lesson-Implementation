"""Shared application exceptions and API error payload formatting.

Python code raises these typed exceptions instead of returning error objects.
The FastAPI exception handlers in `apps.api.app` convert them into HTTP status
codes and JSON, much like custom exception middleware in ASP.NET Core.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class AppError(Exception):
    """Base exception carrying the stable error contract used by API clients.

    Python note: `@dataclass` generates the constructor and attribute storage.
    `slots=True` prevents accidental new attributes and saves memory.
    """

    code: str
    message: str
    status_code: int = 400
    details: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        # Dataclasses do not automatically initialize the base Exception message.
        Exception.__init__(self, self.message)


class ValidationAppError(AppError):
    def __init__(
        self,
        message: str = "Validation failed.",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="validation_error",
            message=message,
            status_code=422,
            details=details,
        )


class NotFoundError(AppError):
    def __init__(
        self,
        message: str = "Resource not found.",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="not_found",
            message=message,
            status_code=404,
            details=details,
        )


class PermissionDeniedError(AppError):
    def __init__(
        self,
        message: str = "Permission denied.",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="permission_denied",
            message=message,
            status_code=403,
            details=details,
        )


class ConflictError(AppError):
    def __init__(
        self,
        message: str = "Resource conflict.",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="conflict",
            message=message,
            status_code=409,
            details=details,
        )


class AIProviderError(AppError):
    def __init__(
        self,
        message: str = "AI provider request failed.",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="ai.provider_error",
            message=message,
            status_code=502,
            details=details,
        )


class AIOutputValidationError(AppError):
    def __init__(
        self,
        message: str = "AI output validation failed.",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="ai.output_validation_error",
            message=message,
            status_code=422,
            details=details,
        )


class SafetyBlockedError(AppError):
    def __init__(
        self,
        message: str = "AI request blocked by safety policy.",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="ai.safety_blocked",
            message=message,
            status_code=403,
            details=details,
        )


class ToolExecutionError(AppError):
    def __init__(
        self,
        message: str = "Tool execution failed.",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="tool.execution_error",
            message=message,
            status_code=502,
            details=details,
        )


def error_payload(error: AppError, request_id: str | None = None) -> dict[str, Any]:
    """Build the shared JSON error envelope returned by the API layer."""
    return {
        "error": {
            "code": error.code,
            "message": error.message,
            "details": error.details or {},
            "request_id": request_id,
        }
    }
