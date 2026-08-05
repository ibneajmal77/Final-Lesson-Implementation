"""Integration-style tests for prompt test runs going through the model gateway."""

from __future__ import annotations

from sqlalchemy.orm import Session

from packages.db.models.model_gateway import AIRun
from packages.prompts.contracts import VariableDeclaration
from packages.prompts.service import PromptService
from packages.prompts.tests import PromptTestRunner


def test_prompt_runner_executes_cases_and_stores_prompt_version_id(
    db_session: Session,
    tenant,
) -> None:
    service = PromptService(db_session)
    template = service.create_template(
        tenant_id=tenant.id,
        name=f"phase02_runner_{tenant.slug}",
        use_case="chat",
    )
    version = service.create_version(
        template_id=template.id,
        system_prompt="You are a support assistant.",
        user_template="Question: ${question}",
        input_variables=(VariableDeclaration(name="question", required=True, trusted=False),),
    )
    service.approve_version(template_id=template.id, version_id=version.id, actor_user_id=None)
    service.activate_version(
        template_id=template.id,
        version_id=version.id,
        actor_user_id=None,
        reason="runner setup",
    )
    service.create_test_case(
        template_id=template.id,
        name="basic_question",
        case_type="happy_path",
        input_json={"question": "What is Atlas?"},
        expected_behavior="Completes the request.",
        expected_output_json={"contains": "What is Atlas?"},
    )

    summary = PromptTestRunner(db_session).run_prompt_tests(
        template_id=template.id,
        prompt_version_id=version.id,
        tenant_id=tenant.id,
    )

    assert summary.total == 1
    assert summary.passed == 1
    assert summary.results[0].ai_run_id is not None
    ai_run = db_session.get(AIRun, summary.results[0].ai_run_id)
    assert ai_run is not None
    assert ai_run.prompt_version_id == version.id
    assert ai_run.response_json is not None
    attrs = ai_run.response_json["observability_attributes"]
    assert attrs["gen_ai.prompt.name"] == template.name
    assert attrs["gen_ai.prompt.version"] == version.version_number
    assert attrs["atlas.prompt.version_id"] == str(version.id)
