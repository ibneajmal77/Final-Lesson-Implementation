"""API tests for prompt template, version, rendering, and test-run endpoints."""

from __future__ import annotations

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from apps.api.app import create_app
from packages.core.config import Settings
from packages.db.models.identity import Tenant
from packages.db.session import get_engine, get_session_factory


def _client() -> TestClient:
    return TestClient(create_app(Settings(_env_file=None)))


def _tenant_id() -> str:
    try:
        with get_engine().connect() as connection:
            connection.execute(text("select 1"))
    except SQLAlchemyError as exc:
        pytest.skip(f"database unavailable for prompt API tests: {exc.__class__.__name__}")
    session = get_session_factory()()
    try:
        suffix = uuid4().hex
        tenant = Tenant(name=f"Prompt API Tenant {suffix}", slug=f"prompt-api-{suffix}")
        session.add(tenant)
        session.commit()
        session.refresh(tenant)
        return str(tenant.id)
    finally:
        session.close()


def test_prompt_crud_activation_and_test_run_contract() -> None:
    tenant_id = _tenant_id()
    client = _client()
    suffix = uuid4().hex

    create_template = client.post(
        "/api/v1/prompts",
        json={
            "tenant_id": tenant_id,
            "name": f"api_prompt_{suffix}",
            "use_case": "chat",
            "description": "Prompt API contract test",
        },
    )
    assert create_template.status_code == 201
    prompt_id = create_template.json()["id"]

    create_version = client.post(
        f"/api/v1/prompts/{prompt_id}/versions",
        json={
            "system_prompt": "You are a support assistant.",
            "user_template": "Question: ${question}",
            "input_variables": [
                {"name": "question", "required": True, "trusted": False}
            ],
            "output_schema_json": {"type": "object"},
            "model_defaults": {"temperature": "0.200", "max_output_tokens": 200},
            "status": "active",
        },
    )
    version_body = create_version.json()
    assert create_version.status_code == 201
    assert version_body["status"] == "draft"
    assert version_body["output_schema_json"] == {"type": "object"}
    version_id = version_body["id"]

    activate_draft = client.post(
        f"/api/v1/prompts/{prompt_id}/versions/{version_id}/activate",
        json={"reason": "should be refused"},
    )
    assert activate_draft.status_code == 409
    assert activate_draft.json()["error"]["code"] == "prompts.version_not_approved"

    approve = client.post(
        f"/api/v1/prompts/{prompt_id}/versions/{version_id}/approve",
        json={"reason": "reviewed"},
    )
    assert approve.status_code == 200
    assert approve.json()["status"] == "approved"

    activate = client.post(
        f"/api/v1/prompts/{prompt_id}/versions/{version_id}/activate",
        json={"reason": "contract test activation"},
    )
    assert activate.status_code == 200
    assert activate.json()["prompt_version_id"] == version_id
    assert activate.json()["audit_event_id"]

    create_case = client.post(
        f"/api/v1/prompts/{prompt_id}/tests",
        json={
            "name": "basic_question",
            "case_type": "happy_path",
            "input_json": {"question": "What is Atlas?"},
            "expected_behavior": "Completes the request.",
            "expected_output_json": {"contains": "What is Atlas?"},
        },
    )
    assert create_case.status_code == 201
    assert create_case.json()["expected_output_json"] == {"contains": "What is Atlas?"}

    run_tests = client.post(
        f"/api/v1/prompts/{prompt_id}/test",
        json={"tenant_id": tenant_id, "prompt_version_id": version_id},
    )
    run_body = run_tests.json()
    assert run_tests.status_code == 200
    assert run_body["provider_mode"] == "mock"
    assert run_body["summary"]["total"] == 1
    assert run_body["summary"]["passed"] == 1


def test_create_version_rejects_untrusted_variable_in_system_prompt() -> None:
    tenant_id = _tenant_id()
    client = _client()
    suffix = uuid4().hex
    prompt_id = client.post(
        "/api/v1/prompts",
        json={
            "tenant_id": tenant_id,
            "name": f"api_prompt_reject_{suffix}",
            "use_case": "chat",
        },
    ).json()["id"]

    response = client.post(
        f"/api/v1/prompts/{prompt_id}/versions",
        json={
            "system_prompt": "Policy: ${question}",
            "user_template": "Question: ${question}",
            "input_variables": [
                {"name": "question", "required": True, "trusted": False}
            ],
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "prompts.invalid_template_contract"
