"""Typed gateway exceptions.

These specialize the shared `AppError` contract with model-routing and provider
failure codes, giving API handlers status codes without string parsing.
"""

from packages.core.errors import AppError


class GatewayError(AppError):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int = 502,
        details: dict[str, object] | None = None,
    ) -> None:
        super().__init__(code=code, message=message, status_code=status_code, details=details)


class RouteNotFoundError(GatewayError):
    def __init__(self, details: dict[str, object] | None = None) -> None:
        super().__init__(
            code="ai.route_not_found",
            message="No eligible model route is available.",
            status_code=404,
            details=details,
        )


class DataPolicyBlockedError(GatewayError):
    def __init__(self, details: dict[str, object] | None = None) -> None:
        super().__init__(
            code="ai.data_policy_blocked",
            message="No compliant model route can handle restricted data.",
            status_code=403,
            details=details,
        )


class BudgetExceededError(GatewayError):
    def __init__(self, details: dict[str, object] | None = None) -> None:
        super().__init__(
            code="ai.budget_exceeded",
            message="No eligible model route fits the requested cost budget.",
            status_code=402,
            details=details,
        )


class ProviderUnavailableError(GatewayError):
    def __init__(
        self,
        *,
        retryable: bool,
        message: str = "Model provider is unavailable.",
        details: dict[str, object] | None = None,
    ) -> None:
        super().__init__(
            code="ai.provider_unavailable",
            message=message,
            status_code=503,
            details=details,
        )
        # Retry/fallback policy reads this flag. It is intentionally an instance
        # attribute because availability failures can be retryable or terminal.
        self.retryable = retryable


class ProviderTimeoutError(GatewayError):
    def __init__(self, details: dict[str, object] | None = None) -> None:
        super().__init__(
            code="ai.provider_timeout",
            message="Model provider timed out.",
            status_code=504,
            details=details,
        )
        # Timeouts are considered retryable by default.
        self.retryable = True
