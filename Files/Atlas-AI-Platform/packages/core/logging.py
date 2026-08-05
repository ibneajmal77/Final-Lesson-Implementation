"""Structured JSON logging with request-id enrichment.

The standard `logging` module is configured here to produce one JSON object per
line. The request-id filter behaves like a logging scope in .NET, adding the
current correlation id without every caller passing it explicitly.
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any

from packages.core.request_context import get_request_id

_STANDARD_LOG_RECORD_ATTRS = set(logging.makeLogRecord({}).__dict__)


class RequestIdFilter(logging.Filter):
    """Add the async request id to each log record before formatting."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.__dict__["request_id"] = get_request_id() or record.__dict__.get("request_id", "-")
        return True


class JsonFormatter(logging.Formatter):
    """Format Python log records as compact JSON for container log collectors."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
        }

        extras = {
            key: value
            for key, value in record.__dict__.items()
            if key not in _STANDARD_LOG_RECORD_ATTRS and key != "request_id"
        }
        # Anything supplied via `logger.info(..., extra={...})` is preserved in a
        # nested `extra` object so downstream systems can index structured fields.
        if extras:
            payload["extra"] = extras
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str, separators=(",", ":"))


def _ensure_request_id_filter(handler: logging.Handler) -> None:
    if not any(isinstance(existing_filter, RequestIdFilter) for existing_filter in handler.filters):
        handler.addFilter(RequestIdFilter())


def configure_logging(level: str) -> None:
    """Configure root logging once for both API and worker processes."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=log_level)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    for handler in root_logger.handlers:
        handler.setFormatter(JsonFormatter())
        _ensure_request_id_filter(handler)
