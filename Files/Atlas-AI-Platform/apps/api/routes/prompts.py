"""HTTP API for prompt templates, prompt versions, rendering, and tests.

This route module is the prompt-system controller layer. It accepts JSON DTOs,
calls `PromptService`, `PromptRegistry`, or `PromptTestRunner`, and maps domain
objects back into response DTOs.

Python notes for .NET reviewers:
- `BaseModel` classes are Pydantic DTOs with validation.
- `Field(...)` and `Query(...)` declare validation constraints.
- `ConfigDict(extra="forbid")` rejects unknown JSON properties.
- `default_factory=list` or `default_factory=dict` creates a fresh collection
  per request. This avoids the shared-mutable-default trap in Python.
"""

from __future__ import annotations

from dataclasses import asdict
from decimal import Decimal
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from packages.db.models.prompts import PromptTemplate, PromptTestCase, PromptVersion
from packages.db.session import get_db_session
from packages.model_gateway.bootstrap import ensure_default_gateway_config
from packages.prompts.contracts import (
    ModelDefaults,
    PromptTestCaseType,
    VariableDeclaration,
    model_defaults_to_json,
)
from packages.prompts.registry import PromptRegistry
from packages.prompts.service import ActivationResult, PromptService
from packages.prompts.tests import PromptTestRunner

router = APIRouter(prefix="/prompts", tags=["prompts"])


class VariablePayload(BaseModel):
    """API DTO for one declared prompt variable."""

    name: str = Field(pattern=r"^[A-Za-z_][A-Za-z0-9_]*$")
    required: bool
    trusted: bool
    description: str | None = None
    max_tokens: int | None = Field(default=None, gt=0)


class ModelDefaultsPayload(BaseModel):
    temperature: Decimal | None = None
    max_output_tokens: int | None = Field(default=None, gt=0)
    route_key: str | None = None


class CreateTemplateRequest(BaseModel):
    """Request DTO for creating a prompt template/family."""

    model_config = ConfigDict(extra="forbid")

    tenant_id: UUID | None = None
    name: str = Field(min_length=1)
    use_case: str = Field(min_length=1)
    description: str | None = None
    owner_user_id: UUID | None = None
    actor_user_id: UUID | None = None


class CreateVersionRequest(BaseModel):
    """Request DTO for adding an immutable prompt version."""

    system_prompt: str = Field(min_length=1)
    user_template: str = Field(min_length=1)
    developer_notes: str | None = None
    input_variables: list[VariablePayload] = Field(default_factory=list)
    output_schema_json: dict[str, Any] | None = None
    model_defaults: ModelDefaultsPayload = Field(default_factory=ModelDefaultsPayload)
    created_by_user_id: UUID | None = None


class ReasonRequest(BaseModel):
    reason: str = Field(min_length=1)
    actor_user_id: UUID | None = None


class ApproveRequest(BaseModel):
    reason: str | None = None
    actor_user_id: UUID | None = None


class RenderRequest(BaseModel):
    tenant_id: UUID | None = None
    variables: dict[str, Any] = Field(default_factory=dict)
    prompt_version_id: UUID | None = None


class CreateTestCaseRequest(BaseModel):
    tenant_id: UUID | None = None
    name: str = Field(min_length=1)
    case_type: PromptTestCaseType
    input_json: dict[str, Any]
    expected_behavior: str = Field(min_length=1)
    expected_output_json: dict[str, Any] | None = None
    created_by_user_id: UUID | None = None


class RunTestsRequest(BaseModel):
    tenant_id: UUID | None = None
    prompt_version_id: UUID
    case_types: list[PromptTestCaseType] = Field(default_factory=list)
    compare_to_active: bool = False


class PromptTemplatePayload(BaseModel):
    id: UUID
    tenant_id: UUID | None
    name: str
    use_case: str
    description: str | None
    owner_user_id: UUID | None
    status: str
    active_version: UUID | None
    version_count: int


class PromptTemplateDetailPayload(PromptTemplatePayload):
    versions: list[PromptVersionPayload]


class PromptVersionPayload(BaseModel):
    id: UUID
    prompt_template_id: UUID
    version_number: int
    status: str
    developer_notes: str | None
    input_variables_json: list[dict[str, Any]]
    output_schema_json: dict[str, Any] | None
    model_defaults_json: dict[str, Any]
    created_by_user_id: UUID | None
    created_by_actor_type: str


class PromptVersionDetailPayload(PromptVersionPayload):
    system_prompt: str
    user_template: str


class ActivationPayload(BaseModel):
    prompt_version_id: UUID
    version_number: int
    status: str
    previous_version_id: UUID | None
    previous_version_number: int | None
    previous_version_status: str | None
    audit_event_id: UUID


class RenderedPromptPayload(BaseModel):
    messages: list[dict[str, str]]
    prompt_version_id: UUID
    prompt_name: str
    prompt_version_number: int
    prompt_template_id: UUID
    use_case: str
    resolution: str
    cache_hit: bool
    render_hash: str
    estimated_input_tokens: int


class PromptTestCasePayload(BaseModel):
    id: UUID
    tenant_id: UUID | None
    prompt_template_id: UUID
    name: str
    case_type: str
    input_json: dict[str, Any]
    expected_behavior: str
    expected_output_json: dict[str, Any] | None
    status: str


class PromptTestRunPayload(BaseModel):
    prompt_version_id: UUID
    version_number: int
    baseline_version_id: UUID | None
    baseline_version_number: int | None
    provider_mode: Literal["mock", "provider"]
    summary: dict[str, int]
    results: list[dict[str, Any]]


@router.post("", response_model=PromptTemplatePayload, status_code=status.HTTP_201_CREATED)
def create_template(
    payload: CreateTemplateRequest,
    session: Annotated[Session, Depends(get_db_session)],
) -> PromptTemplatePayload:
    """Create a new prompt template.

    The decorator above registers the route; the function name is for Python
    readability/tests and does not become the URL.
    """
    template = PromptService(session).create_template(
        tenant_id=payload.tenant_id,
        name=payload.name,
        use_case=payload.use_case,
        description=payload.description,
        owner_user_id=payload.owner_user_id,
        actor_user_id=payload.actor_user_id,
    )
    return _template_payload(PromptService(session), template)


@router.get("", response_model=list[PromptTemplatePayload])
def list_templates(
    session: Annotated[Session, Depends(get_db_session)],
    tenant_id: UUID | None = None,
    use_case: str | None = None,
    template_status: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=100, gt=0, le=500),
) -> list[PromptTemplatePayload]:
    # `Query(...)` applies validation to query-string values rather than JSON
    # body fields. Here it limits page size to a safe range.
    service = PromptService(session)
    templates = service.list_templates(
        tenant_id=tenant_id,
        use_case=use_case,
        status=template_status,
        limit=limit,
    )
    return [_template_payload(service, template) for template in templates]


@router.get("/{prompt_id}", response_model=PromptTemplateDetailPayload)
def get_template(
    prompt_id: UUID,
    session: Annotated[Session, Depends(get_db_session)],
) -> PromptTemplateDetailPayload:
    service = PromptService(session)
    template = service.get_template(prompt_id)
    versions = service.list_versions(template_id=prompt_id)
    base = _template_payload(service, template)
    return PromptTemplateDetailPayload(
        **base.model_dump(),
        versions=[_version_payload(version) for version in versions],
    )


@router.post(
    "/{prompt_id}/versions",
    response_model=PromptVersionPayload,
    status_code=status.HTTP_201_CREATED,
)
def create_version(
    prompt_id: UUID,
    payload: CreateVersionRequest,
    session: Annotated[Session, Depends(get_db_session)],
) -> PromptVersionPayload:
    version = PromptService(session).create_version(
        template_id=prompt_id,
        system_prompt=payload.system_prompt,
        user_template=payload.user_template,
        developer_notes=payload.developer_notes,
        # Convert mutable API lists into immutable tuples for the domain layer.
        input_variables=tuple(_variable_declaration(item) for item in payload.input_variables),
        output_schema_json=payload.output_schema_json,
        model_defaults_json=model_defaults_to_json(_model_defaults(payload.model_defaults)),
        created_by_user_id=payload.created_by_user_id,
    )
    return _version_payload(version)


@router.get(
    "/{prompt_id}/versions/{version_id}",
    response_model=PromptVersionDetailPayload,
)
def get_version(
    prompt_id: UUID,
    version_id: UUID,
    session: Annotated[Session, Depends(get_db_session)],
) -> PromptVersionDetailPayload:
    version = PromptService(session).get_version(template_id=prompt_id, version_id=version_id)
    return _version_detail_payload(version)


@router.post(
    "/{prompt_id}/versions/{version_id}/approve",
    response_model=PromptVersionPayload,
)
def approve_version(
    prompt_id: UUID,
    version_id: UUID,
    payload: ApproveRequest,
    session: Annotated[Session, Depends(get_db_session)],
) -> PromptVersionPayload:
    version = PromptService(session).approve_version(
        template_id=prompt_id,
        version_id=version_id,
        actor_user_id=payload.actor_user_id,
        reason=payload.reason,
    )
    return _version_payload(version)


@router.post(
    "/{prompt_id}/versions/{version_id}/activate",
    response_model=ActivationPayload,
)
def activate_version(
    prompt_id: UUID,
    version_id: UUID,
    payload: ReasonRequest,
    session: Annotated[Session, Depends(get_db_session)],
) -> ActivationPayload:
    # Activation checks that a model route exists for the prompt's use case, so
    # local/default routes are seeded before the service enforces that rule.
    ensure_default_gateway_config(session)
    result = PromptService(session).activate_version(
        template_id=prompt_id,
        version_id=version_id,
        actor_user_id=payload.actor_user_id,
        reason=payload.reason,
    )
    return _activation_payload(result)


@router.post(
    "/{prompt_id}/versions/{version_id}/deactivate",
    response_model=PromptVersionPayload,
)
def deactivate_version(
    prompt_id: UUID,
    version_id: UUID,
    payload: ReasonRequest,
    session: Annotated[Session, Depends(get_db_session)],
) -> PromptVersionPayload:
    version = PromptService(session).deactivate_version(
        template_id=prompt_id,
        version_id=version_id,
        actor_user_id=payload.actor_user_id,
        reason=payload.reason,
    )
    return _version_payload(version)


@router.post(
    "/{prompt_id}/versions/{version_id}/retire",
    response_model=PromptVersionPayload,
)
def retire_version(
    prompt_id: UUID,
    version_id: UUID,
    payload: ReasonRequest,
    session: Annotated[Session, Depends(get_db_session)],
) -> PromptVersionPayload:
    version = PromptService(session).retire_version(
        template_id=prompt_id,
        version_id=version_id,
        actor_user_id=payload.actor_user_id,
        reason=payload.reason,
    )
    return _version_payload(version)


@router.post("/{prompt_id}/render", response_model=RenderedPromptPayload)
def render_prompt(
    prompt_id: UUID,
    payload: RenderRequest,
    session: Annotated[Session, Depends(get_db_session)],
) -> RenderedPromptPayload:
    template = PromptService(session).get_template(prompt_id)
    # The registry handles tenant/global/pinned resolution and returns already
    # rendered chat messages that can be sent to the gateway.
    rendered = PromptRegistry(session).render(
        tenant_id=payload.tenant_id or template.tenant_id,
        use_case=template.use_case,
        variables=payload.variables,
        prompt_version_id=payload.prompt_version_id,
    )
    return RenderedPromptPayload(
        messages=[
            {"role": message.role, "content": message.content}
            for message in rendered.messages
        ],
        prompt_version_id=rendered.prompt_version_id,
        prompt_name=rendered.prompt_name,
        prompt_version_number=rendered.prompt_version_number,
        prompt_template_id=rendered.prompt_template_id,
        use_case=rendered.use_case,
        resolution=rendered.resolution,
        cache_hit=rendered.cache_hit,
        render_hash=rendered.render_hash,
        estimated_input_tokens=rendered.estimated_input_tokens,
    )


@router.post(
    "/{prompt_id}/tests",
    response_model=PromptTestCasePayload,
    status_code=status.HTTP_201_CREATED,
)
def create_test_case(
    prompt_id: UUID,
    payload: CreateTestCaseRequest,
    session: Annotated[Session, Depends(get_db_session)],
) -> PromptTestCasePayload:
    test_case = PromptService(session).create_test_case(
        template_id=prompt_id,
        tenant_id=payload.tenant_id,
        name=payload.name,
        case_type=payload.case_type,
        input_json=payload.input_json,
        expected_behavior=payload.expected_behavior,
        expected_output_json=payload.expected_output_json,
        created_by_user_id=payload.created_by_user_id,
    )
    return _test_case_payload(test_case)


@router.get("/{prompt_id}/tests", response_model=list[PromptTestCasePayload])
def list_test_cases(
    prompt_id: UUID,
    session: Annotated[Session, Depends(get_db_session)],
    case_type: str | None = None,
    limit: int = Query(default=100, gt=0, le=500),
) -> list[PromptTestCasePayload]:
    test_cases = PromptService(session).list_test_cases(
        template_id=prompt_id,
        case_type=case_type,
        limit=limit,
    )
    return [_test_case_payload(test_case) for test_case in test_cases]


@router.post("/{prompt_id}/test", response_model=PromptTestRunPayload)
def run_prompt_tests(
    prompt_id: UUID,
    payload: RunTestsRequest,
    session: Annotated[Session, Depends(get_db_session)],
) -> PromptTestRunPayload:
    # Tests execute through the gateway, so they use the same routing, AI run
    # ledger, and cost-estimation path as real prompt executions.
    ensure_default_gateway_config(session)
    summary = PromptTestRunner(session).run_prompt_tests(
        template_id=prompt_id,
        prompt_version_id=payload.prompt_version_id,
        tenant_id=payload.tenant_id,
        case_types=tuple(payload.case_types),
        compare_to_active=payload.compare_to_active,
    )
    return PromptTestRunPayload(
        prompt_version_id=summary.prompt_version_id,
        version_number=summary.version_number,
        baseline_version_id=summary.baseline_version_id,
        baseline_version_number=summary.baseline_version_number,
        provider_mode=summary.provider_mode,
        summary={
            "total": summary.total,
            "passed": summary.passed,
            "failed": summary.failed,
            "error": summary.error,
            "needs_review": summary.needs_review,
            "regressions": summary.regressions,
            "fixed": summary.fixed,
        },
        results=[asdict(result) for result in summary.results],
    )


def _template_payload(
    service: PromptService,
    template: PromptTemplate,
) -> PromptTemplatePayload:
    """Map an ORM row to the API response DTO.

    Python note: helper functions prefixed with `_` are conventionally private
    to this module, similar to `private` methods in C# but not enforced.
    """
    versions = service.list_versions(template_id=template.id)
    active_version = next((version.id for version in versions if version.status == "active"), None)
    return PromptTemplatePayload(
        id=template.id,
        tenant_id=template.tenant_id,
        name=template.name,
        use_case=template.use_case,
        description=template.description,
        owner_user_id=template.owner_user_id,
        status=template.status,
        active_version=active_version,
        version_count=len(versions),
    )


def _version_payload(version: PromptVersion) -> PromptVersionPayload:
    return PromptVersionPayload(
        id=version.id,
        prompt_template_id=version.prompt_template_id,
        version_number=version.version_number,
        status=version.status,
        developer_notes=version.developer_notes,
        input_variables_json=version.input_variables_json,
        output_schema_json=version.output_schema_json,
        model_defaults_json=version.model_defaults_json,
        created_by_user_id=version.created_by_user_id,
        created_by_actor_type=version.created_by_actor_type,
    )


def _version_detail_payload(version: PromptVersion) -> PromptVersionDetailPayload:
    return PromptVersionDetailPayload(
        **_version_payload(version).model_dump(),
        system_prompt=version.system_prompt,
        user_template=version.user_template,
    )


def _activation_payload(result: ActivationResult) -> ActivationPayload:
    return ActivationPayload(
        prompt_version_id=result.prompt_version_id,
        version_number=result.version_number,
        status=result.status,
        previous_version_id=result.previous_version_id,
        previous_version_number=result.previous_version_number,
        previous_version_status=result.previous_version_status,
        audit_event_id=result.audit_event_id,
    )


def _test_case_payload(test_case: PromptTestCase) -> PromptTestCasePayload:
    return PromptTestCasePayload(
        id=test_case.id,
        tenant_id=test_case.tenant_id,
        prompt_template_id=test_case.prompt_template_id,
        name=test_case.name,
        case_type=test_case.case_type,
        input_json=test_case.input_json,
        expected_behavior=test_case.expected_behavior,
        expected_output_json=test_case.expected_output_json,
        status=test_case.status,
    )


def _variable_declaration(payload: VariablePayload) -> VariableDeclaration:
    return VariableDeclaration(
        name=payload.name,
        required=payload.required,
        trusted=payload.trusted,
        description=payload.description,
        max_tokens=payload.max_tokens,
    )


def _model_defaults(payload: ModelDefaultsPayload) -> ModelDefaults:
    return ModelDefaults(
        temperature=payload.temperature,
        max_output_tokens=payload.max_output_tokens,
        route_key=payload.route_key,
    )
