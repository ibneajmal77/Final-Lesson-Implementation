"""OpenTelemetry-style GenAI attribute helpers.

The gateway stores these attributes with each run so traces, logs, and database
records can use the same dimensions for provider/model/prompt analysis.
"""

from collections.abc import Mapping
from typing import Any

from packages.model_gateway.types import GatewayResponse, ModelRequest, SelectedRoute
from packages.observability.tracing import gateway_span


def genai_attributes(
    *,
    request: ModelRequest,
    route: SelectedRoute,
    response: GatewayResponse | None = None,
) -> dict[str, Any]:
    """Build a stable attribute dictionary from request, route, and response data."""
    attributes: dict[str, Any] = {
        "gen_ai.operation.name": request.use_case,
        "gen_ai.system": route.provider_type,
        "gen_ai.request.model": route.model_name,
        "gen_ai.response.model": route.model_name,
        "gen_ai.provider.name": route.provider_name,
        "gen_ai.route.key": route.route_key,
        "gen_ai.prompt.name": request.prompt_name,
        "gen_ai.prompt.version": request.prompt_version_number,
        "atlas.prompt.template_id": (
            str(request.prompt_template_id) if request.prompt_template_id else None
        ),
        "atlas.prompt.version_id": (
            str(request.prompt_version_id) if request.prompt_version_id else None
        ),
        "atlas.prompt.use_case": request.use_case if request.prompt_version_id else None,
        "atlas.prompt.resolution": request.prompt_resolution,
        "atlas.prompt.cache_hit": request.prompt_cache_hit,
    }
    if response is not None:
        attributes.update(
            {
                "gen_ai.usage.input_tokens": response.usage.input_tokens,
                "gen_ai.usage.output_tokens": response.usage.output_tokens,
                "gen_ai.response.finish_reasons": [response.finish_reason],
            }
        )
    return attributes


def emit_gateway_span(
    name: str,
    *,
    attributes: Mapping[str, Any],
    latency_ms: int,
) -> None:
    """Record one completed gateway call as a span.

    The span is opened and closed immediately because the work has already
    happened by the time attributes are known. That costs a timestamp pair
    rather than a real duration, which is the honest trade for not threading a
    span context through the whole gateway workflow; `atlas.latency_ms` carries
    the measured duration instead.

    With tracing unconfigured this resolves to OpenTelemetry's no-op tracer, so
    the call is effectively free.
    """
    with gateway_span(name, {**attributes, "atlas.latency_ms": latency_ms}):
        pass
