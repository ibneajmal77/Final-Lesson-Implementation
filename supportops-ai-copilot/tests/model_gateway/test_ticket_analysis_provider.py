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


def valid_hosted_payload() -> dict[str, object]:
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


def hosted_response(output_text: str | None = None) -> dict[str, object]:
    text = output_text if output_text is not None else json.dumps(valid_hosted_payload())
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


def test_mock_provider_returns_model_shaped_analysis() -> None:
    provider = build_ticket_analysis_provider("mock")

    result = provider.analyze_ticket(
        TicketAnalysisInput(
            subject="Charged twice",
            body="I was charged twice for order ORD-123 and need a refund.",
            customer_id="customer-123",
        )
    )

    assert result.source == MOCK_SOURCE
    assert result.model_name == MOCK_MODEL_NAME
    assert result.prompt_version == PROMPT_VERSION
    assert result.category == "billing"
    assert result.priority == "high"
    assert result.summary
    assert "billing" in result.suggested_reply.lower()
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
    assert "UNTRUSTED_TICKET_TEXT_START" in request_body["input"]

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
