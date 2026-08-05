"""Tests that optimizer-created prompt versions remain behind human review."""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from packages.prompts.contracts import VariableDeclaration
from packages.prompts.errors import PromptConflictError
from packages.prompts.optimization import create_candidate_version
from packages.prompts.service import PromptService


def test_optimizer_candidate_is_created_as_draft(db_session: Session, tenant) -> None:
    service = PromptService(db_session)
    template = service.create_template(
        tenant_id=tenant.id,
        name=f"phase02_optimizer_{tenant.slug}",
        use_case="chat",
    )

    candidate = create_candidate_version(
        db_session,
        template_id=template.id,
        system_prompt="Optimized system",
        user_template="${question}",
        input_variables=(VariableDeclaration(name="question", required=True, trusted=False),),
    )

    assert candidate.status == "draft"
    assert candidate.created_by_actor_type == "optimizer"


def test_optimizer_candidate_cannot_be_approved_or_activated(
    db_session: Session,
    tenant,
) -> None:
    service = PromptService(db_session)
    template = service.create_template(
        tenant_id=tenant.id,
        name=f"phase02_optimizer_blocked_{tenant.slug}",
        use_case="chat",
    )
    candidate = create_candidate_version(
        db_session,
        template_id=template.id,
        system_prompt="Optimized system",
        user_template="${question}",
        input_variables=(VariableDeclaration(name="question", required=True, trusted=False),),
    )

    with pytest.raises(PromptConflictError) as approve_error:
        service.approve_version(
            template_id=template.id,
            version_id=candidate.id,
            actor_user_id=None,
        )
    with pytest.raises(PromptConflictError) as activate_error:
        service.activate_version(
            template_id=template.id,
            version_id=candidate.id,
            actor_user_id=None,
            reason="should not activate",
        )

    assert approve_error.value.code == "prompts.optimizer_cannot_approve"
    assert activate_error.value.code == "prompts.optimizer_cannot_activate"
