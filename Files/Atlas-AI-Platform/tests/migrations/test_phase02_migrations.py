"""Migration tests for Phase 02 prompt-system database rules."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from packages.db.models.identity import Tenant
from packages.db.models.model_gateway import AIRun
from packages.db.models.prompts import PromptTemplate, PromptVersion
from packages.db.session import get_engine, get_session_factory


def _session_or_skip():
    try:
        with get_engine().connect() as connection:
            connection.exec_driver_sql("select 1")
    except SQLAlchemyError as exc:
        pytest.skip(f"database unavailable for migration tests: {exc.__class__.__name__}")
    return get_session_factory()()


def test_phase02_migration_files_include_required_constraints() -> None:
    audit_migration = Path("packages/db/migrations/versions/0003_audit_events.py").read_text(
        encoding="utf-8"
    )
    prompt_migration = Path("packages/db/migrations/versions/0004_prompt_system.py").read_text(
        encoding="utf-8"
    )
    assert 'down_revision: str | None = "0002_model_gateway"' in audit_migration
    assert 'down_revision: str | None = "0003_audit_events"' in prompt_migration
    assert "uq_prompt_versions_one_active" in prompt_migration
    assert "fk_ai_runs_prompt_version_id_prompt_versions" in prompt_migration
    assert "created_by_actor_type in ('user','system','optimizer')" in prompt_migration


def test_second_active_version_rejected() -> None:
    session = _session_or_skip()
    try:
        suffix = uuid4().hex
        tenant = Tenant(name=f"Migration Tenant {suffix}", slug=f"migration-{suffix}")
        session.add(tenant)
        session.flush()
        template = PromptTemplate(
            tenant_id=tenant.id,
            name=f"migration_prompt_{suffix}",
            use_case="chat",
        )
        session.add(template)
        session.flush()
        session.add_all(
            [
                _active_version(template.id, 1),
                _active_version(template.id, 2),
            ]
        )
        with pytest.raises(IntegrityError):
            session.commit()
    finally:
        session.rollback()
        session.close()


def test_ai_runs_prompt_version_fk_rejects_unknown_version() -> None:
    session = _session_or_skip()
    try:
        suffix = uuid4().hex
        tenant = Tenant(name=f"FK Tenant {suffix}", slug=f"fk-tenant-{suffix}")
        session.add(tenant)
        session.flush()
        session.add(
            AIRun(
                tenant_id=tenant.id,
                use_case="chat",
                provider_name="mock_public",
                model_name="mock-chat-v1",
                prompt_version_id=uuid4(),
                request_hash=uuid4().hex,
                status="succeeded",
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()
    finally:
        session.rollback()
        session.close()


def _active_version(template_id, version_number: int) -> PromptVersion:
    return PromptVersion(
        prompt_template_id=template_id,
        version_number=version_number,
        system_prompt=f"System {version_number}",
        user_template="${question}",
        input_variables_json=[{"name": "question", "required": True, "trusted": False}],
        model_defaults_json={},
        status="active",
        created_by_actor_type="user",
    )
