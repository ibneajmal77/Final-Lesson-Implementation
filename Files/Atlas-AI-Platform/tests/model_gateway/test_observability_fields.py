"""Tests for the OpenTelemetry GenAI attribute payload.

Phase 01 planned this file and never wrote it, so `genai_attributes()` built a
dictionary that nothing checked. These attributes are the dimensions every
provider/model/prompt dashboard groups by, and a renamed or dropped key breaks
those dashboards silently — the calls still succeed, the charts just go empty.

The function is pure, so no database is needed.
"""

from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from packages.model_gateway.observability import genai_attributes
from packages.model_gateway.types import (
    ChatMessage,
    GatewayResponse,
    ModelRequest,
    SelectedRoute,
    TokenUsage,
)

# The stable contract. Renaming any of these is a breaking change for anything
# querying traces, so the names are pinned here rather than only in the source.
REQUIRED_ATTRIBUTE_KEYS = {
    "gen_ai.operation.name",
    "gen_ai.system",
    "gen_ai.request.model",
    "gen_ai.response.model",
    "gen_ai.provider.name",
    "gen_ai.route.key",
    "gen_ai.prompt.name",
    "gen_ai.prompt.version",
    "atlas.prompt.template_id",
    "atlas.prompt.version_id",
    "atlas.prompt.use_case",
    "atlas.prompt.resolution",
    "atlas.prompt.cache_hit",
}


def _route() -> SelectedRoute:
    return SelectedRoute(
        route_id=uuid4(),
        route_key="chat_primary",
        use_case="chat",
        provider_name="mock_public",
        provider_type="mock",
        model_name="mock-chat-v1",
        max_input_tokens=4000,
        max_output_tokens=800,
        timeout_seconds=30,
        temperature=Decimal("0.2"),
        restricted_data_allowed=False,
        fallback_route_id=None,
        route_config={},
        capabilities={"supports_chat": True},
        data_policy={},
        max_cost_usd=Decimal("0.05"),
        embedding_dimension=None,
    )


def _request(**overrides: object) -> ModelRequest:
    defaults: dict[str, object] = {
        "tenant_id": uuid4(),
        "use_case": "chat",
        "messages": (ChatMessage(role="user", content="hello"),),
    }
    defaults.update(overrides)
    return ModelRequest(**defaults)  # type: ignore[arg-type]


def _response(route: SelectedRoute) -> GatewayResponse:
    return GatewayResponse(
        ai_run_id=uuid4(),
        use_case="chat",
        provider_name=route.provider_name,
        model_name=route.model_name,
        route_key=route.route_key,
        status="succeeded",
        content="hi",
        finish_reason="stop",
        usage=TokenUsage(input_tokens=11, output_tokens=22),
    )


def test_request_only_attributes_include_every_required_key() -> None:
    attributes = genai_attributes(request=_request(), route=_route())

    assert REQUIRED_ATTRIBUTE_KEYS.issubset(attributes.keys())


def test_route_identity_is_reported_from_the_served_route() -> None:
    route = _route()

    attributes = genai_attributes(request=_request(), route=route)

    assert attributes["gen_ai.system"] == "mock"
    assert attributes["gen_ai.provider.name"] == "mock_public"
    assert attributes["gen_ai.request.model"] == "mock-chat-v1"
    assert attributes["gen_ai.route.key"] == "chat_primary"


def test_prompt_attributes_are_none_when_no_prompt_version_was_used() -> None:
    """A direct gateway call has no prompt attribution, and must say so.

    The keys still have to be present. Emitting the key with a null value keeps
    the attribute schema stable across calls; omitting it makes every consumer
    handle two different payload shapes.
    """
    attributes = genai_attributes(request=_request(), route=_route())

    assert attributes["atlas.prompt.version_id"] is None
    assert attributes["atlas.prompt.template_id"] is None
    assert attributes["atlas.prompt.use_case"] is None
    assert attributes["gen_ai.prompt.name"] is None


def test_prompt_attributes_are_populated_for_a_prompt_backed_call() -> None:
    version_id = uuid4()
    template_id = uuid4()
    request = _request(
        prompt_version_id=version_id,
        prompt_template_id=template_id,
        prompt_name="rag_answer_support",
        prompt_version_number=4,
        prompt_resolution="tenant",
        prompt_cache_hit=True,
    )

    attributes = genai_attributes(request=request, route=_route())

    assert attributes["atlas.prompt.version_id"] == str(version_id)
    assert attributes["atlas.prompt.template_id"] == str(template_id)
    assert attributes["gen_ai.prompt.name"] == "rag_answer_support"
    assert attributes["gen_ai.prompt.version"] == 4
    assert attributes["atlas.prompt.resolution"] == "tenant"
    assert attributes["atlas.prompt.cache_hit"] is True
    # `atlas.prompt.use_case` is only set when a prompt version was attributed.
    assert attributes["atlas.prompt.use_case"] == "chat"


def test_response_attributes_are_added_only_when_a_response_exists() -> None:
    route = _route()

    without_response = genai_attributes(request=_request(), route=route)
    with_response = genai_attributes(
        request=_request(),
        route=route,
        response=_response(route),
    )

    assert "gen_ai.usage.input_tokens" not in without_response
    assert with_response["gen_ai.usage.input_tokens"] == 11
    assert with_response["gen_ai.usage.output_tokens"] == 22
    assert with_response["gen_ai.response.finish_reasons"] == ["stop"]


def test_attribute_values_are_telemetry_safe_primitives() -> None:
    """No UUID or Decimal may leak into the attribute payload.

    OTel exporters accept strings, numbers, booleans, None, and sequences of
    those. A raw UUID or Decimal either raises at export time or is coerced
    inconsistently by different exporters, so it is caught here instead.
    """
    route = _route()
    request = _request(prompt_version_id=uuid4(), prompt_template_id=uuid4())

    attributes = genai_attributes(request=request, route=route, response=_response(route))

    for key, value in attributes.items():
        assert isinstance(value, str | int | float | bool | list | None), (
            f"attribute {key} has non-telemetry-safe type {type(value).__name__}"
        )
