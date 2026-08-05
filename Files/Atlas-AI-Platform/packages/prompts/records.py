"""Convert ORM prompt rows into immutable prompt contracts.

This keeps SQLAlchemy models at the persistence boundary and gives render/test
code record-like dataclasses to work with.
"""

from __future__ import annotations

from typing import Any

from packages.db.models.prompts import PromptTemplate, PromptVersion
from packages.prompts.contracts import (
    ModelDefaults,
    PromptVersionSpec,
    VariableDeclaration,
    model_defaults_from_json,
    variable_declaration_from_json,
)


def version_spec_from_models(
    *,
    version: PromptVersion,
    template: PromptTemplate,
) -> PromptVersionSpec:
    """Map a PromptVersion ORM row plus its template row to a domain contract."""
    return PromptVersionSpec(
        id=version.id,
        prompt_template_id=version.prompt_template_id,
        tenant_id=template.tenant_id,
        template_name=template.name,
        use_case=template.use_case,
        version_number=version.version_number,
        system_prompt=version.system_prompt,
        user_template=version.user_template,
        input_variables=_variables_from_json(version.input_variables_json),
        output_schema=_dict_or_none(version.output_schema_json),
        model_defaults=_model_defaults_from_json(version.model_defaults_json),
        status=version.status,
        created_by_user_id=version.created_by_user_id,
        created_by_actor_type=version.created_by_actor_type,
    )


def _variables_from_json(values: list[dict[str, Any]]) -> tuple[VariableDeclaration, ...]:
    return tuple(variable_declaration_from_json(value) for value in values)


def _model_defaults_from_json(value: dict[str, Any]) -> ModelDefaults:
    return model_defaults_from_json(value)


def _dict_or_none(value: dict[str, Any] | None) -> dict[str, Any] | None:
    return dict(value) if value is not None else None
