"""Unit tests for shared application error classes and JSON envelopes."""

from packages.core.errors import (
    AIOutputValidationError,
    AIProviderError,
    AppError,
    PermissionDeniedError,
    SafetyBlockedError,
    ToolExecutionError,
    error_payload,
)


def test_app_error_initializes_base_exception_message() -> None:
    error = AppError(code="demo_failed", message="Demo failed.", status_code=409)

    assert str(error) == "Demo failed."
    assert error.args == ("Demo failed.",)


def test_error_payload_includes_request_id_and_details() -> None:
    error = AppError(
        code="demo_failed",
        message="Demo failed.",
        details={"field": "value"},
    )

    payload = error_payload(error, request_id="req-123")

    assert payload == {
        "error": {
            "code": "demo_failed",
            "message": "Demo failed.",
            "details": {"field": "value"},
            "request_id": "req-123",
        }
    }


def test_ai_error_subclasses_have_stable_codes_and_statuses() -> None:
    errors = [
        AIProviderError(),
        AIOutputValidationError(),
        SafetyBlockedError(),
        ToolExecutionError(),
    ]

    assert [(error.code, error.status_code) for error in errors] == [
        ("ai.provider_error", 502),
        ("ai.output_validation_error", 422),
        ("ai.safety_blocked", 403),
        ("tool.execution_error", 502),
    ]


def test_permission_denied_error_supports_rbac_gate() -> None:
    error = PermissionDeniedError(details={"feature_key": "rag.collection"})

    assert error.code == "permission_denied"
    assert error.status_code == 403
    assert error.details == {"feature_key": "rag.collection"}
