"""OpenTelemetry tracer setup and the gateway span helper.

Phase 01 built the right GenAI attribute dictionary and then only wrote it into
a JSON column. That is a dead end for operations: you cannot chart a JSONB blob
across services, and the one dimension people actually ask for — "which model is
burning the latency budget?" — needs a real span.

Configuration is deliberately three-state:

- unset  -> a no-op tracer. Nothing is exported, nothing has to be running, and
            local development and CI stay dependency-free.
- console-> spans printed to stdout, which is enough to see the shape of a trace
            without standing up a collector.
- otlp   -> spans exported to a collector. This needs the `otlp` extra
            installed; if it is missing, the process logs and degrades to no-op
            rather than failing to start. Telemetry must never be the reason an
            API cannot boot.

Python notes for .NET reviewers:
- `contextmanager` turns a generator into a `with`-usable object.
- The `yield` inside is where the caller's block runs.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import Any

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

logger = logging.getLogger(__name__)

_configured = False


def configure_tracing(
    *,
    exporter: str = "none",
    service_name: str = "atlas-ai-platform",
    endpoint: str | None = None,
) -> None:
    """Install a tracer provider. Safe to call more than once."""
    global _configured
    if _configured:
        return

    if exporter == "none":
        # No provider is installed at all. `trace.get_tracer` then returns the
        # API's no-op tracer, so instrumented code runs unchanged and costs
        # almost nothing.
        _configured = True
        return

    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    span_exporter: Any
    if exporter == "otlp":
        try:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                OTLPSpanExporter,
            )
        except ImportError:
            logger.warning(
                "OTLP exporter requested but not installed; tracing disabled. "
                "Install the 'otlp' extra to enable it."
            )
            _configured = True
            return
        span_exporter = OTLPSpanExporter(endpoint=endpoint) if endpoint else OTLPSpanExporter()
    else:
        span_exporter = ConsoleSpanExporter()

    provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(provider)
    _configured = True
    logger.info("Tracing configured", extra={"exporter": exporter, "service": service_name})


def reset_tracing_for_tests() -> None:
    """Allow a test to reconfigure tracing. Not for production use."""
    global _configured
    _configured = False


@contextmanager
def gateway_span(name: str, attributes: Mapping[str, Any] | None = None) -> Iterator[Any]:
    """Wrap a gateway call in a span carrying the GenAI attributes.

    Attribute values are filtered to the primitives OTel accepts. A raw UUID or
    Decimal either raises at export time or is coerced differently by different
    exporters, so they are dropped here rather than corrupting a trace.
    """
    tracer = trace.get_tracer("packages.model_gateway")
    with tracer.start_as_current_span(name) as span:
        for key, value in (attributes or {}).items():
            if value is None:
                continue
            if isinstance(value, str | bool | int | float):
                span.set_attribute(key, value)
            elif isinstance(value, list | tuple) and all(
                isinstance(item, str | bool | int | float) for item in value
            ):
                span.set_attribute(key, list(value))
        yield span
