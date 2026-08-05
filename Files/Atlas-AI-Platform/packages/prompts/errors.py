"""Prompt-system exception types and common error factories."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from packages.core.errors import AppError


class PromptError(AppError):
    """Base class for prompt-specific API/domain errors."""

    pass


class PromptNotFoundError(PromptError):
    def __init__(
        self,
        *,
        code: str = "prompts.not_found",
        message: str = "Prompt resource not found.",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(code=code, message=message, status_code=404, details=details)


class PromptValidationError(PromptError):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(code=code, message=message, status_code=422, details=details)


class PromptConflictError(PromptError):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(code=code, message=message, status_code=409, details=details)


def no_active_version_error(*, tenant_id: UUID | None, use_case: str) -> PromptNotFoundError:
    return PromptNotFoundError(
        code="prompts.no_active_version",
        message="No active prompt version is available.",
        details={"tenant_id": str(tenant_id) if tenant_id else None, "use_case": use_case},
    )


def version_not_approved_error(
    *,
    prompt_version_id: UUID,
    current_status: str,
) -> PromptConflictError:
    return PromptConflictError(
        code="prompts.version_not_approved",
        message="Only an approved version can be activated.",
        details={
            "prompt_version_id": str(prompt_version_id),
            "current_status": current_status,
            "required_status": "approved",
        },
    )
