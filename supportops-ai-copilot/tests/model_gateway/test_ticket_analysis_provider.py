# ============================================================================
# FILE: tests/model_gateway/test_ticket_analysis_provider.py
#
# WHAT THIS TESTS: the boundary around AI providers: selecting mock versus
# hosted implementations, building a privacy-conscious structured request,
# translating a hosted reply into the common result shape, and rejecting unsafe
# or malformed configuration and output.
#
# THINK OF THIS FILE AS: checking both the universal plug socket and the adapter
# for a paid AI service, without ever connecting to the public electricity grid.
#
# providers/base.py defines a Protocol: a contract based on available methods,
# not inheritance. Any object with the right `analyze_ticket` method can stand
# behind the gateway. routing.py chooses an implementation; mock.py supplies the
# free deterministic one; hosted.py owns every HTTP- and provider-specific detail.
#
#     provider setting -> routing.py
#       -> mock.py -> deterministic TicketAnalysisResult
#       -> hosted.py -> versioned prompt + strict JSON request
#          -> injected MockTransport -> fabricated provider response
#             -> validation -> the same TicketAnalysisResult shape
#
# `httpx.MockTransport` intercepts requests and calls a local handler. That is
# dependency injection: supplying a controlled collaborator from outside. It is
# not MONKEYPATCHING, which means temporarily replacing a name at runtime.
#
# HONEST LIMITATIONS: no case contacts a real model, proves that a model follows
# the safety instructions, or covers every HTTP timeout, refusal, and malformed
# response shape. These tests prove request construction and local validation;
# live-provider evaluation remains a separate, deliberately non-default check.
# ============================================================================
#
import json

import httpx
import pytest

from supportops_model_gateway.errors import (
    ModelProviderConfigurationError,
    ModelProviderResponseError,
    UnsupportedModelProviderError,
)
from supportops_model_gateway.providers.base import TicketAnalysisInput
from supportops_model_gateway.providers.hosted import (
    OPENAI_SOURCE,
    HostedTicketAnalysisProvider,
)
from supportops_model_gateway.providers.mock import MOCK_MODEL_NAME, MOCK_SOURCE, PROMPT_VERSION
from supportops_model_gateway.routing import build_ticket_analysis_provider


# A canonical piece of model output containing every required field from
# packages/prompts/supportops_prompts/schemas.py. This is a helper function, not
# a pytest FIXTURE: a fixture is setup marked with `@pytest.fixture` and injected
# by name, while callers here ask for a fresh mutable dictionary explicitly.
#
# Keeping one known-good example makes failure tests precise: each can change
# one field and know that any rejection came from that change, not missing setup.
def valid_hosted_payload() -> dict[str, object]:
    # Both evidence lists cite only sources that hosted.py actually supplied.
    # The validator rejects invented source names later in this file.
    return {
        "category": "billing",
        "category_confidence": 0.92,
        "priority": "high",
        "requires_escalation": False,
        "extracted_fields": {
            "order_ids": ["ORD-123"],
            "amounts": ["USD 42.00"],
            "product_names": [],
            "account_identifiers": [],
            "evidence_ids": ["ticket-body"],
        },
        "evidence_ids": ["ticket-body"],
        "draft_response": {
            "response_text": "Thanks for reaching out. I will review the billing details.",
            "tone": "empathetic",
            "needs_human_review": True,
            "forbidden_claims": [],
        },
        "abstain": False,
        "risk_flags": ["none"],
        "missing_information": [],
    }


# Wrap the analysis text in the nested shape returned by the hosted Responses
# API. Supplying `output_text` lets negative tests keep the outer HTTP response
# valid while replacing only the model's inner answer.
def hosted_response(output_text: str | None = None) -> dict[str, object]:
    # `json.dumps` serializes the good Python dictionary into the text a remote
    # model would send. Passing a string bypasses that conversion deliberately.
    text = output_text if output_text is not None else json.dumps(valid_hosted_payload())
    # The nested output exercises hosted.py's fallback text extractor rather
    # than a simpler top-level `output_text` shortcut. Usage counts and provider
    # IDs below are later checked all the way through the result conversion.
    return {
        "id": "resp_test_123",
        "status": "completed",
        "model": "gpt-test",
        "output": [
            {
                "type": "message",
                "content": [
                    {
                        "type": "output_text",
                        "text": text,
                    }
                ],
            }
        ],
        "usage": {
            "input_tokens": 111,
            "output_tokens": 222,
            "total_tokens": 333,
        },
    }


# THE FREE PATH. Ask routing.py for `mock`, analyze an ordinary billing ticket,
# and check that the object returned through the provider Protocol has the full
# shape downstream routes and workers rely on.
def test_mock_provider_returns_model_shaped_analysis() -> None:
    # The caller receives the contract, without needing to know the concrete
    # MockTicketAnalysisProvider class selected inside the factory.
    provider = build_ticket_analysis_provider("mock")

    # TicketAnalysisInput is the deliberately narrow cross-provider input type
    # from providers/base.py: ticket text and optional context, no database object.
    result = provider.analyze_ticket(
        TicketAnalysisInput(
            subject="Charged twice",
            body="I was charged twice for order ORD-123 and need a refund.",
            customer_id="customer-123",
        )
    )

    # Provenance keeps fake output unmistakable in stored recommendations and
    # metrics. A mock accidentally enabled in production should be easy to spot.
    assert result.source == MOCK_SOURCE
    assert result.model_name == MOCK_MODEL_NAME
    assert result.prompt_version == PROMPT_VERSION
    # These checks cover meaningful analysis shape without pinning every word of
    # the canned summary and reply, which would make harmless wording edits noisy.
    assert result.category == "billing"
    assert result.priority == "high"
    assert result.summary
    assert "billing" in result.suggested_reply.lower()
    # The mock delegates extraction to the baseline classifier and then preserves
    # caller context, proving both kinds of data survive the gateway boundary.
    assert result.extracted_fields["order_ids"] == ["ORD-123"]
    assert result.extracted_fields["customer_id"] == "customer-123"


def test_hosted_provider_sends_structured_responses_request() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["authorization"] = request.headers["Authorization"]
        captured["body"] = json.loads(request.content.decode("utf-8"))
        return httpx.Response(200, json=hosted_response())

    provider = HostedTicketAnalysisProvider(
        api_key="test-key",
        model_name="gpt-test",
        base_url="https://models.example/v1",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    result = provider.analyze_ticket(
        TicketAnalysisInput(
            subject="Charged twice",
            body="I was charged twice for order ORD-123.",
            customer_id="customer-123",
            policy_context="Do not promise refunds before billing verification.",
        )
    )

    request_body = captured["body"]
    assert isinstance(request_body, dict)
    assert captured["url"] == "https://models.example/v1/responses"
    assert captured["authorization"] == "Bearer test-key"
    assert request_body["model"] == "gpt-test"
    assert request_body["store"] is False
    assert request_body["metadata"]["prompt_id"] == "full_ticket_analysis.v1"
    assert request_body["text"]["format"]["type"] == "json_schema"
    assert request_body["text"]["format"]["strict"] is True
    prompt_input = str(request_body["input"])
    assert "Do not choose tools, permissions, or actions outside the JSON schema." in prompt_input
    assert "Do not promise refunds before billing verification." in prompt_input
    assert prompt_input.index("Do not choose tools") < prompt_input.index(
        "UNTRUSTED_TICKET_TEXT_START"
    )
    assert prompt_input.index("Policy context:") < prompt_input.index(
        "UNTRUSTED_TICKET_TEXT_START"
    )

    assert result.source == OPENAI_SOURCE
    assert result.model_name == "gpt-test"
    assert result.prompt_version == "full_ticket_analysis.v1"
    assert result.category == "billing"
    assert result.priority == "high"
    assert result.confidence == 0.92
    assert result.suggested_reply.startswith("Thanks for reaching out")
    assert result.extracted_fields["provider"] == "openai"
    assert result.extracted_fields["raw_response_id"] == "resp_test_123"
    assert result.input_tokens == 111
    assert result.output_tokens == 222
    assert result.raw_response_id == "resp_test_123"


def test_openai_provider_requires_api_key() -> None:
    with pytest.raises(ModelProviderConfigurationError):
        build_ticket_analysis_provider("openai", api_key="")


def test_hosted_provider_rejects_invalid_structured_output() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=hosted_response(output_text="not json"))

    provider = HostedTicketAnalysisProvider(
        api_key="test-key",
        model_name="gpt-test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    with pytest.raises(ModelProviderResponseError):
        provider.analyze_ticket(
            TicketAnalysisInput(
                subject="Charged twice",
                body="I was charged twice for order ORD-123.",
            )
        )


def test_unknown_provider_is_rejected() -> None:
    with pytest.raises(UnsupportedModelProviderError):
        build_ticket_analysis_provider("not-real")

def test_hosted_provider_rejects_unsupported_evidence_ids() -> None:
    payload = valid_hosted_payload()
    payload["evidence_ids"] = ["ticket-body", "tool-delete-user"]

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=hosted_response(output_text=json.dumps(payload)))

    provider = HostedTicketAnalysisProvider(
        api_key="test-key",
        model_name="gpt-test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    with pytest.raises(ModelProviderResponseError, match="unsupported evidence ids"):
        provider.analyze_ticket(
            TicketAnalysisInput(
                subject="Charged twice",
                body="I was charged twice for order ORD-123.",
            )
        )


def test_hosted_provider_rejects_tool_or_permission_selection_output() -> None:
    payload = valid_hosted_payload()
    payload["tool_calls"] = [{"name": "delete_ticket", "arguments": {"ticket_id": "123"}}]

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=hosted_response(output_text=json.dumps(payload)))

    provider = HostedTicketAnalysisProvider(
        api_key="test-key",
        model_name="gpt-test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    with pytest.raises(ModelProviderResponseError, match="invalid ticket analysis"):
        provider.analyze_ticket(
            TicketAnalysisInput(
                subject="Charged twice",
                body="I was charged twice for order ORD-123.",
            )
        )
