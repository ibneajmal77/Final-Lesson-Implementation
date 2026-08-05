"""Prompt management application service.

This is the prompt subsystem's transaction boundary. It creates templates and
versions, enforces lifecycle rules, records audit events, and invalidates the
active prompt cache when status changes.

Python notes for .NET reviewers:
- Methods include `self` explicitly; it is Python's equivalent of `this`.
- Parameters after `*` are keyword-only, so callers must pass names.
- SQLAlchemy `flush()` writes pending changes without committing the transaction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from packages.core.request_context import get_request_id
from packages.db.models.audit import AuditEvent
from packages.db.models.model_gateway import ModelRoute
from packages.db.models.prompts import PromptTemplate, PromptTestCase, PromptVersion
from packages.prompts.contracts import (
    KNOWN_PROMPT_USE_CASES,
    PromptActorType,
    PromptTestCaseType,
    VariableDeclaration,
    variable_declaration_to_json,
)
from packages.prompts.errors import (
    PromptConflictError,
    PromptNotFoundError,
    PromptValidationError,
    version_not_approved_error,
)
from packages.prompts.registry import PromptRegistry
from packages.prompts.renderer import validate_template_contract


@dataclass(frozen=True, slots=True)
class ActivationResult:
    """Return object for activation, including the audit row created."""

    prompt_version_id: UUID
    version_number: int
    status: str
    previous_version_id: UUID | None
    previous_version_number: int | None
    previous_version_status: str | None
    audit_event_id: UUID


class PromptService:
    """Application service for prompt template/version/test-case mutations."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create_template(
        self,
        *,
        name: str,
        use_case: str,
        tenant_id: UUID | None,
        description: str | None = None,
        owner_user_id: UUID | None = None,
        actor_user_id: UUID | None = None,
        actor_type: str = "user",
    ) -> PromptTemplate:
        """Create a prompt family and audit the new record."""
        _validate_use_case(use_case)
        template = PromptTemplate(
            tenant_id=tenant_id,
            name=name,
            use_case=use_case,
            description=description,
            owner_user_id=owner_user_id,
            status="active",
        )
        self._session.add(template)
        self._session.flush()
        # Flush assigns database-generated ids before commit, so the audit event
        # can reference the new template id in the same transaction.
        self._audit(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            actor_type=actor_type,
            action="prompt_template.created",
            subject_type="prompt_template",
            subject_id=template.id,
            before_json=None,
            after_json={
                "name": template.name,
                "use_case": template.use_case,
                "owner_user_id": str(template.owner_user_id) if template.owner_user_id else None,
                "status": template.status,
            },
            metadata_json={},
        )
        self._session.commit()
        return template

    def list_templates(
        self,
        *,
        tenant_id: UUID | None = None,
        use_case: str | None = None,
        status: str | None = None,
        limit: int = 100,
    ) -> list[PromptTemplate]:
        statement = select(PromptTemplate)
        if tenant_id is not None:
            statement = statement.where(PromptTemplate.tenant_id == tenant_id)
        if use_case is not None:
            statement = statement.where(PromptTemplate.use_case == use_case)
        if status is not None:
            statement = statement.where(PromptTemplate.status == status)
        return list(
            self._session.scalars(statement.order_by(PromptTemplate.created_at).limit(limit)).all()
        )

    def get_template(self, template_id: UUID) -> PromptTemplate:
        template = self._session.get(PromptTemplate, template_id)
        if template is None:
            raise PromptNotFoundError(
                code="prompts.template_not_found",
                message="Prompt template not found.",
                details={"prompt_template_id": str(template_id)},
            )
        return template

    def get_version(self, *, template_id: UUID, version_id: UUID) -> PromptVersion:
        version = self._session.get(PromptVersion, version_id)
        if version is None or version.prompt_template_id != template_id:
            raise PromptNotFoundError(
                code="prompts.version_not_found",
                message="Prompt version not found.",
                details={
                    "prompt_template_id": str(template_id),
                    "prompt_version_id": str(version_id),
                },
            )
        return version

    def list_versions(self, *, template_id: UUID, limit: int = 100) -> list[PromptVersion]:
        return list(
            self._session.scalars(
                select(PromptVersion)
                .where(PromptVersion.prompt_template_id == template_id)
                .order_by(PromptVersion.version_number)
                .limit(limit)
            ).all()
        )

    def create_version(
        self,
        *,
        template_id: UUID,
        system_prompt: str,
        user_template: str,
        input_variables: tuple[VariableDeclaration, ...],
        developer_notes: str | None = None,
        output_schema_json: dict[str, Any] | None = None,
        model_defaults_json: dict[str, Any] | None = None,
        created_by_user_id: UUID | None = None,
        created_by_actor_type: PromptActorType = "user",
    ) -> PromptVersion:
        template = self.get_template(template_id)
        validate_template_contract(
            system_prompt=system_prompt,
            user_template=user_template,
            input_variables=input_variables,
        )
        # Versions are append-only revisions from a review perspective. New
        # content starts in draft and must be approved before activation.
        version_number = self._next_version_number(template_id)
        version = PromptVersion(
            prompt_template_id=template.id,
            version_number=version_number,
            system_prompt=system_prompt,
            user_template=user_template,
            developer_notes=developer_notes,
            input_variables_json=[
                variable_declaration_to_json(variable) for variable in input_variables
            ],
            output_schema_json=output_schema_json,
            model_defaults_json=model_defaults_json or {},
            status="draft",
            created_by_user_id=created_by_user_id,
            created_by_actor_type=created_by_actor_type,
        )
        self._session.add(version)
        self._session.flush()
        self._audit(
            tenant_id=template.tenant_id,
            actor_user_id=created_by_user_id,
            actor_type=created_by_actor_type,
            action="prompt_version.created",
            subject_type="prompt_version",
            subject_id=version.id,
            before_json=None,
            after_json={
                "prompt_template_id": str(template.id),
                "version_number": version.version_number,
                "status": version.status,
                "created_by_actor_type": version.created_by_actor_type,
            },
            metadata_json={},
        )
        self._session.commit()
        return version

    def approve_version(
        self,
        *,
        template_id: UUID,
        version_id: UUID,
        actor_user_id: UUID | None,
        actor_type: str = "user",
        reason: str | None = None,
    ) -> PromptVersion:
        version = self.get_version(template_id=template_id, version_id=version_id)
        template = self.get_template(template_id)
        # Optimizer-created versions cannot approve themselves into production;
        # this keeps automated prompt search behind a human review gate.
        if actor_type == "optimizer" or version.created_by_actor_type == "optimizer":
            raise PromptConflictError(
                code="prompts.optimizer_cannot_approve",
                message=(
                    "Optimizer-created prompt versions require a human rewrite "
                    "before approval."
                ),
                details={"prompt_version_id": str(version.id)},
            )
        if version.status == "retired":
            raise PromptConflictError(
                code="prompts.version_retired",
                message="A retired prompt version cannot be approved.",
                details={"prompt_version_id": str(version.id)},
            )
        if version.status != "approved":
            old_status = version.status
            version.status = "approved"
            self._audit_status_change(
                template=template,
                version=version,
                old_status=old_status,
                actor_user_id=actor_user_id,
                actor_type=actor_type,
                reason=reason,
            )
        self._session.commit()
        return version

    def activate_version(
        self,
        *,
        template_id: UUID,
        version_id: UUID,
        actor_user_id: UUID | None,
        reason: str,
        actor_type: str = "user",
    ) -> ActivationResult:
        # Lock the template row while swapping active versions, similar to using
        # a transaction plus concurrency control around "only one active" state.
        template = self._session.scalars(
            select(PromptTemplate)
            .where(PromptTemplate.id == template_id)
            .with_for_update()
        ).one_or_none()
        if template is None:
            raise PromptNotFoundError(
                code="prompts.template_not_found",
                message="Prompt template not found.",
                details={"prompt_template_id": str(template_id)},
            )
        version = self.get_version(template_id=template_id, version_id=version_id)
        if version.created_by_actor_type == "optimizer" or actor_type == "optimizer":
            raise PromptConflictError(
                code="prompts.optimizer_cannot_activate",
                message="Optimizer-created prompt versions cannot be activated.",
                details={"prompt_version_id": str(version.id)},
            )
        if template.status != "active":
            raise PromptConflictError(
                code="prompts.template_archived",
                message="An archived prompt template cannot activate versions.",
                details={"prompt_template_id": str(template.id)},
            )
        if version.status != "approved":
            raise version_not_approved_error(
                prompt_version_id=version.id,
                current_status=version.status,
            )
        if not self._has_active_route(template):
            raise PromptConflictError(
                code="prompts.no_active_route",
                message="A prompt version cannot be activated until an active route exists.",
                details={"use_case": template.use_case, "tenant_id": str(template.tenant_id)},
            )

        previous = self._session.scalars(
            select(PromptVersion)
            .where(
                PromptVersion.prompt_template_id == template.id,
                PromptVersion.status == "active",
            )
            .with_for_update()
        ).one_or_none()
        previous_status: str | None = None
        if previous is not None:
            # The prior active version remains approved so rollback is a normal
            # activation operation, not a recreation of retired content.
            previous_status = "approved"
            previous.status = previous_status
            self._session.flush()

        version.status = "active"
        audit_event = self._audit(
            tenant_id=template.tenant_id,
            actor_user_id=actor_user_id,
            actor_type=actor_type,
            action="prompt_version.activated",
            subject_type="prompt_version",
            subject_id=version.id,
            before_json=(
                None
                if previous is None
                else {
                    "prompt_version_id": str(previous.id),
                    "version_number": previous.version_number,
                    "status": "active",
                }
            ),
            after_json={
                "prompt_version_id": str(version.id),
                "version_number": version.version_number,
                "status": "active",
            },
            metadata_json={"reason": reason, "use_case": template.use_case},
        )
        self._session.commit()
        # Active prompt resolution is cached; status-changing commands must clear
        # the relevant key after the database transaction succeeds.
        PromptRegistry.invalidate(tenant_id=template.tenant_id, use_case=template.use_case)
        return ActivationResult(
            prompt_version_id=version.id,
            version_number=version.version_number,
            status=version.status,
            previous_version_id=previous.id if previous else None,
            previous_version_number=previous.version_number if previous else None,
            previous_version_status=previous_status,
            audit_event_id=audit_event.id,
        )

    def deactivate_version(
        self,
        *,
        template_id: UUID,
        version_id: UUID,
        actor_user_id: UUID | None,
        reason: str,
        actor_type: str = "user",
    ) -> PromptVersion:
        version = self.get_version(template_id=template_id, version_id=version_id)
        template = self.get_template(template_id)
        if version.status != "active":
            raise PromptConflictError(
                code="prompts.version_not_active",
                message="Only an active prompt version can be deactivated.",
                details={"prompt_version_id": str(version.id), "status": version.status},
            )
        old_status = version.status
        version.status = "approved"
        self._audit_status_change(
            template=template,
            version=version,
            old_status=old_status,
            actor_user_id=actor_user_id,
            actor_type=actor_type,
            reason=reason,
        )
        self._session.commit()
        PromptRegistry.invalidate(tenant_id=template.tenant_id, use_case=template.use_case)
        return version

    def retire_version(
        self,
        *,
        template_id: UUID,
        version_id: UUID,
        actor_user_id: UUID | None,
        reason: str,
        actor_type: str = "user",
    ) -> PromptVersion:
        version = self.get_version(template_id=template_id, version_id=version_id)
        template = self.get_template(template_id)
        if version.status == "retired":
            return version
        old_status = version.status
        version.status = "retired"
        self._audit_status_change(
            template=template,
            version=version,
            old_status=old_status,
            actor_user_id=actor_user_id,
            actor_type=actor_type,
            reason=reason,
        )
        self._session.commit()
        PromptRegistry.invalidate(tenant_id=template.tenant_id, use_case=template.use_case)
        return version

    def create_test_case(
        self,
        *,
        template_id: UUID,
        name: str,
        case_type: PromptTestCaseType,
        input_json: dict[str, Any],
        expected_behavior: str,
        tenant_id: UUID | None = None,
        expected_output_json: dict[str, Any] | None = None,
        created_by_user_id: UUID | None = None,
    ) -> PromptTestCase:
        template = self.get_template(template_id)
        effective_tenant_id = template.tenant_id if tenant_id is None else tenant_id
        if effective_tenant_id != template.tenant_id:
            raise PromptValidationError(
                code="prompts.test_case_tenant_mismatch",
                message="Prompt test case tenant must match its template tenant.",
                details={
                    "prompt_template_id": str(template.id),
                    "template_tenant_id": str(template.tenant_id) if template.tenant_id else None,
                    "test_case_tenant_id": (
                        str(effective_tenant_id) if effective_tenant_id else None
                    ),
                },
            )
        test_case = PromptTestCase(
            tenant_id=effective_tenant_id,
            prompt_template_id=template.id,
            name=name,
            case_type=case_type,
            input_json=input_json,
            expected_behavior=expected_behavior,
            expected_output_json=expected_output_json,
            status="active",
            created_by_user_id=created_by_user_id,
        )
        self._session.add(test_case)
        self._session.commit()
        return test_case

    def list_test_cases(
        self,
        *,
        template_id: UUID,
        case_type: str | None = None,
        status: str = "active",
        limit: int = 100,
    ) -> list[PromptTestCase]:
        statement = select(PromptTestCase).where(
            PromptTestCase.prompt_template_id == template_id,
            PromptTestCase.status == status,
        )
        if case_type is not None:
            statement = statement.where(PromptTestCase.case_type == case_type)
        return list(
            self._session.scalars(statement.order_by(PromptTestCase.created_at).limit(limit)).all()
        )

    def mark_testing(
        self,
        *,
        version: PromptVersion,
        template: PromptTemplate,
        actor_type: str = "system",
        reason: str = "Prompt test run executed.",
    ) -> None:
        if version.status != "draft":
            return
        old_status = version.status
        version.status = "testing"
        self._audit_status_change(
            template=template,
            version=version,
            old_status=old_status,
            actor_user_id=None,
            actor_type=actor_type,
            reason=reason,
        )

    def _next_version_number(self, template_id: UUID) -> int:
        """Find the next one-based version number for a template."""
        latest = self._session.scalar(
            select(func.max(PromptVersion.version_number)).where(
                PromptVersion.prompt_template_id == template_id
            )
        )
        return int(latest or 0) + 1

    def _has_active_route(self, template: PromptTemplate) -> bool:
        """Ensure a prompt cannot activate unless the gateway can run its use case."""
        statement = select(ModelRoute.id).where(
            ModelRoute.use_case == template.use_case,
            ModelRoute.status == "active",
        )
        if template.tenant_id is None:
            statement = statement.where(ModelRoute.tenant_id.is_(None))
        else:
            statement = statement.where(
                (ModelRoute.tenant_id == template.tenant_id)
                | (ModelRoute.tenant_id.is_(None))
            )
        return self._session.scalar(statement.limit(1)) is not None

    def _audit_status_change(
        self,
        *,
        template: PromptTemplate,
        version: PromptVersion,
        old_status: str,
        actor_user_id: UUID | None,
        actor_type: str,
        reason: str | None,
    ) -> AuditEvent:
        return self._audit(
            tenant_id=template.tenant_id,
            actor_user_id=actor_user_id,
            actor_type=actor_type,
            action="prompt_version.status_changed",
            subject_type="prompt_version",
            subject_id=version.id,
            before_json={"status": old_status, "version_number": version.version_number},
            after_json={"status": version.status, "version_number": version.version_number},
            metadata_json={"reason": reason} if reason else {},
        )

    def _audit(
        self,
        *,
        tenant_id: UUID | None,
        actor_user_id: UUID | None,
        actor_type: str,
        action: str,
        subject_type: str,
        subject_id: UUID,
        before_json: dict[str, Any] | None,
        after_json: dict[str, Any] | None,
        metadata_json: dict[str, Any],
    ) -> AuditEvent:
        """Insert an audit event in the same database transaction as the change."""
        audit_event = AuditEvent(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            actor_type=actor_type,
            action=action,
            subject_type=subject_type,
            subject_id=subject_id,
            request_id=get_request_id(),
            trace_id=None,
            idempotency_key=None,
            before_json=before_json,
            after_json=after_json,
            metadata_json=metadata_json,
        )
        self._session.add(audit_event)
        self._session.flush()
        return audit_event


def _validate_use_case(use_case: str) -> None:
    """Reject use cases outside the shared prompt vocabulary."""
    if use_case not in KNOWN_PROMPT_USE_CASES:
        raise PromptValidationError(
            code="prompts.unknown_use_case",
            message="Prompt use case is not in the shared Atlas AI vocabulary.",
            details={"use_case": use_case},
        )
