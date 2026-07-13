import json
from pathlib import Path

import pytest
from pydantic import BaseModel

from supportops_model_gateway.providers.base import TicketAnalysisInput
from supportops_model_gateway.routing import build_ticket_analysis_provider
from supportops_prompts.registry import get_prompt, list_prompts, render_prompt


def render_variables() -> dict[str, str]:
    return {
        "ticket_subject": "Charged twice",
        "ticket_body": "I was charged twice for order ORD-123.",
        "customer_id": "customer-123",
        "policy_context": "Do not promise refunds before billing verification.",
    }


def test_prompt_versions_exist() -> None:
    prompt_ids = {prompt.prompt_id for prompt in list_prompts()}

    assert prompt_ids == {
        "classify_ticket.v1",
        "extract_fields.v1",
        "recommend_priority.v1",
        "draft_response.v1",
        "safety_check.v1",
        "full_ticket_analysis.v1",
    }


def test_each_prompt_has_output_schema() -> None:
    for prompt in list_prompts():
        assert issubclass(prompt.output_schema, BaseModel)
        assert prompt.changelog


def test_templates_render_with_required_variables() -> None:
    for prompt in list_prompts():
        rendered = render_prompt(prompt.name, render_variables(), version=prompt.version)

        assert prompt.prompt_id in rendered
        assert "UNTRUSTED_TICKET_TEXT_START" in rendered
        assert "UNTRUSTED_TICKET_TEXT_END" in rendered
        assert "Output Schema" in rendered
        assert "Abstention Rule" in rendered
        assert "Safety Rule" in rendered
        assert "Charged twice" in rendered
        assert '"properties"' in rendered


def test_missing_template_variable_fails() -> None:
    variables = render_variables()
    variables.pop("ticket_body")

    with pytest.raises(KeyError):
        render_prompt("classify_ticket", variables)


def test_prompt_schema_is_associated_with_prompt() -> None:
    prompt = get_prompt("classify_ticket")

    assert prompt.output_schema.__name__ == "TicketClassification"


def test_regression_fixture_matches_mock_provider_category() -> None:
    fixture_path = Path(
        "packages/prompts/supportops_prompts/tests/fixtures/billing_ticket.json"
    )
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    provider = build_ticket_analysis_provider("mock")

    result = provider.analyze_ticket(
        TicketAnalysisInput(
            subject=fixture["subject"],
            body=fixture["body"],
            customer_id=fixture["customer_id"],
        )
    )

    assert result.category == fixture["expected_category"]




