"""Prompt optimizer entry points.

Optimizer-created versions are intentionally marked with actor type `optimizer`.
The service layer then prevents those versions from being approved or activated
without human intervention.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from packages.db.models.prompts import PromptVersion
from packages.prompts.contracts import VariableDeclaration
from packages.prompts.service import PromptService


def create_candidate_version(
    session: Session,
    *,
    template_id: UUID,
    system_prompt: str,
    user_template: str,
    input_variables: tuple[VariableDeclaration, ...],
    developer_notes: str | None = None,
    output_schema_json: dict[str, Any] | None = None,
    model_defaults_json: dict[str, Any] | None = None,
) -> PromptVersion:
    """Create a draft candidate version produced by an automated optimizer."""
    return PromptService(session).create_version(
        template_id=template_id,
        system_prompt=system_prompt,
        user_template=user_template,
        input_variables=input_variables,
        developer_notes=developer_notes,
        output_schema_json=output_schema_json,
        model_defaults_json=model_defaults_json,
        created_by_user_id=None,
        created_by_actor_type="optimizer",
    )
