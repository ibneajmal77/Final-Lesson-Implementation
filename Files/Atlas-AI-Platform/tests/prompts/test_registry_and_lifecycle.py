"""Prompt registry and lifecycle tests.

These tests cover tenant/global resolution, approval/activation rules, cache
invalidation, and audit events.
"""

from __future__ import annotations

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from packages.db.models.audit import AuditEvent
from packages.db.models.prompts import PromptVersion
from packages.prompts.contracts import VariableDeclaration
from packages.prompts.errors import PromptConflictError, PromptNotFoundError
from packages.prompts.registry import PromptRegistry
from packages.prompts.service import PromptService


def test_activation_requires_approval_and_writes_audit_event(
    db_session: Session,
    tenant,
) -> None:
    service = PromptService(db_session)
    template = service.create_template(
        tenant_id=tenant.id,
        name=f"phase02_chat_{tenant.slug}",
        use_case="chat",
    )
    version = service.create_version(
        template_id=template.id,
        system_prompt="You are helpful.",
        user_template="${question}",
        input_variables=(VariableDeclaration(name="question", required=True, trusted=False),),
    )

    with pytest.raises(PromptConflictError) as exc_info:
        service.activate_version(
            template_id=template.id,
            version_id=version.id,
            actor_user_id=None,
            reason="attempt draft activation",
        )
    assert exc_info.value.code == "prompts.version_not_approved"

    service.approve_version(template_id=template.id, version_id=version.id, actor_user_id=None)
    result = service.activate_version(
        template_id=template.id,
        version_id=version.id,
        actor_user_id=None,
        reason="initial prompt promotion",
    )

    audit_event = db_session.get(AuditEvent, result.audit_event_id)
    assert audit_event is not None
    assert audit_event.action == "prompt_version.activated"
    assert audit_event.subject_id == version.id
    assert audit_event.metadata_json["reason"] == "initial prompt promotion"


def test_second_activation_leaves_exactly_one_active_version(
    db_session: Session,
    tenant,
) -> None:
    service = PromptService(db_session)
    template = service.create_template(
        tenant_id=tenant.id,
        name=f"phase02_one_active_{tenant.slug}",
        use_case="chat",
    )
    first = service.create_version(
        template_id=template.id,
        system_prompt="System v1",
        user_template="${question}",
        input_variables=(VariableDeclaration(name="question", required=True, trusted=False),),
    )
    second = service.create_version(
        template_id=template.id,
        system_prompt="System v2",
        user_template="${question}",
        input_variables=(VariableDeclaration(name="question", required=True, trusted=False),),
    )
    service.approve_version(template_id=template.id, version_id=first.id, actor_user_id=None)
    service.approve_version(template_id=template.id, version_id=second.id, actor_user_id=None)
    service.activate_version(
        template_id=template.id,
        version_id=first.id,
        actor_user_id=None,
        reason="v1",
    )
    service.activate_version(
        template_id=template.id,
        version_id=second.id,
        actor_user_id=None,
        reason="v2",
    )

    active_count = db_session.scalar(
        select(func.count(PromptVersion.id)).where(
            PromptVersion.prompt_template_id == template.id,
            PromptVersion.status == "active",
        )
    )
    db_session.refresh(first)
    db_session.refresh(second)
    assert active_count == 1
    assert first.status == "approved"
    assert second.status == "active"


def test_registry_resolves_tenant_override_before_global(
    db_session: Session,
    tenant,
) -> None:
    service = PromptService(db_session)
    global_template = service.create_template(
        tenant_id=None,
        name=f"phase02_global_{tenant.slug}",
        use_case="classification",
    )
    tenant_template = service.create_template(
        tenant_id=tenant.id,
        name=f"phase02_tenant_{tenant.slug}",
        use_case="classification",
    )
    global_version = _approved_active_version(service, global_template.id, "Global")
    tenant_version = _approved_active_version(service, tenant_template.id, "Tenant")

    resolved_for_tenant = PromptRegistry(db_session).resolve(
        tenant_id=tenant.id,
        use_case="classification",
    )
    resolved_global = PromptRegistry(db_session).resolve(
        tenant_id=None,
        use_case="classification",
    )

    assert resolved_for_tenant.version.id == tenant_version.id
    assert resolved_for_tenant.resolution == "tenant"
    assert resolved_global.version.id == global_version.id
    assert resolved_global.resolution == "global"


def test_no_active_version_raises_typed_error(db_session: Session, tenant) -> None:
    service = PromptService(db_session)
    service.create_template(
        tenant_id=tenant.id,
        name=f"phase02_no_active_{tenant.slug}",
        use_case="llm_judge",
    )

    with pytest.raises(PromptNotFoundError) as exc_info:
        PromptRegistry(db_session).resolve(tenant_id=tenant.id, use_case="llm_judge")

    assert exc_info.value.code == "prompts.no_active_version"


def _approved_active_version(
    service: PromptService,
    template_id,
    system_prompt: str,
) -> PromptVersion:
    version = service.create_version(
        template_id=template_id,
        system_prompt=system_prompt,
        user_template="${question}",
        input_variables=(VariableDeclaration(name="question", required=True, trusted=False),),
    )
    service.approve_version(template_id=template_id, version_id=version.id, actor_user_id=None)
    service.activate_version(
        template_id=template_id,
        version_id=version.id,
        actor_user_id=None,
        reason=f"activate {system_prompt}",
    )
    return version
