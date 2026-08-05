"""OpenTelemetry-style GenAI attribute helpers.

The gateway stores these attributes with each run so traces, logs, and database
records can use the same dimensions for provider/model/prompt analysis.
"""

from typing import Any

from packages.model_gateway.types import GatewayResponse, ModelRequest, SelectedRoute


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
