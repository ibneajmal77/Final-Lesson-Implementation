"""Unit tests for structured logging helpers.

Python testing note: pytest discovers functions whose names start with `test_`.
Assertions use plain `assert` statements instead of a separate Assert class.
"""

import json
import logging

from packages.core.logging import JsonFormatter, RequestIdFilter


def test_json_formatter_outputs_structured_log_record() -> None:
    record = logging.LogRecord(
        name="atlas.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="hello %s",
        args=("atlas",),
        exc_info=None,
    )
    record.__dict__["request_id"] = "req-123"
    record.__dict__["path"] = "/api/v1/health"

    payload = json.loads(JsonFormatter().format(record))

    assert payload["level"] == "INFO"
    assert payload["logger"] == "atlas.test"
    assert payload["message"] == "hello atlas"
    assert payload["request_id"] == "req-123"
    assert payload["extra"]["path"] == "/api/v1/health"


def test_request_id_filter_adds_default_when_no_context_exists() -> None:
    record = logging.LogRecord(
        name="atlas.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="hello",
        args=(),
        exc_info=None,
    )

    assert RequestIdFilter().filter(record) is True
    assert record.__dict__["request_id"] == "-"
