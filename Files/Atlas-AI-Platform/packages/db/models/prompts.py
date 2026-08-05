"""ORM models for prompt templates, immutable versions, and test cases.

The prompt system stores a template as the named business concept and versions
as immutable revisions. Database constraints enforce uniqueness and the rule
that only one version per template can be active.
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from packages.db.base import Base


class PromptTemplate(Base):
    """Named prompt family for a use case, optionally scoped to a tenant."""

    __tablename__ = "prompt_templates"
    __table_args__ = (
        CheckConstraint("status in ('active','archived')", name="status"),
        # Partial unique indexes model "global names are unique globally" and
        # "tenant prompt names are unique within the tenant".
        Index(
            "uq_prompt_templates_id_tenant",
            "id",
            "tenant_id",
            unique=True,
        ),
        Index(
            "uq_prompt_templates_global_name",
            "name",
            unique=True,
            postgresql_where=text("tenant_id is null"),
        ),
        Index(
            "uq_prompt_templates_tenant_name",
            "tenant_id",
            "name",
            unique=True,
            postgresql_where=text("tenant_id is not null"),
        ),
        Index("idx_prompt_templates_tenant_use_case", "tenant_id", "use_case", "status"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    tenant_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    use_case: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_user_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'active'"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # ORM relationships are navigation properties; they let service code move
    # between template, versions, and test cases without hand-writing joins.
    versions: Mapped[list["PromptVersion"]] = relationship(back_populates="template")
    test_cases: Mapped[list["PromptTestCase"]] = relationship(
        back_populates="template",
        foreign_keys="PromptTestCase.prompt_template_id",
    )


class PromptVersion(Base):
    """Immutable prompt revision with lifecycle status and model defaults."""

    __tablename__ = "prompt_versions"
    __table_args__ = (
        UniqueConstraint(
            "prompt_template_id",
            "version_number",
            name="uq_prompt_versions_template_version_number",
        ),
        CheckConstraint("version_number > 0", name="version_number_positive"),
        CheckConstraint(
            "status in ('draft','testing','approved','active','retired')",
            name="status",
        ),
        CheckConstraint(
            "created_by_actor_type in ('user','system','optimizer')",
            name="created_by_actor_type",
        ),
        Index("idx_prompt_versions_template_status", "prompt_template_id", "status"),
        Index(
            "uq_prompt_versions_one_active",
            "prompt_template_id",
            unique=True,
            postgresql_where=text("status = 'active'"),
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    prompt_template_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("prompt_templates.id"),
        nullable=False,
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    user_template: Mapped[str] = mapped_column(Text, nullable=False)
    developer_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    input_variables_json: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'[]'::jsonb"),
    )
    output_schema_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    model_defaults_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'draft'"))
    created_by_user_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    created_by_actor_type: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        server_default=text("'user'"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    template: Mapped[PromptTemplate] = relationship(back_populates="versions")


class PromptTestCase(Base):
    """Stored prompt test input plus expected behavior/check metadata."""

    __tablename__ = "prompt_test_cases"
    __table_args__ = (
        ForeignKeyConstraint(
            ["prompt_template_id", "tenant_id"],
            ["prompt_templates.id", "prompt_templates.tenant_id"],
            name="fk_prompt_test_cases_prompt_template_id_tenant_prompt_templates",
        ),
        CheckConstraint(
            "case_type in ('happy_path','edge_case','adversarial','format','regression')",
            name="case_type",
        ),
        CheckConstraint("status in ('active','archived')", name="status"),
        Index(
            "uq_prompt_test_cases_template_name",
            "prompt_template_id",
            "name",
            unique=True,
        ),
        Index("idx_prompt_test_cases_template_status", "prompt_template_id", "status"),
        Index("idx_prompt_test_cases_tenant_id", "tenant_id"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    tenant_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=True,
    )
    prompt_template_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("prompt_templates.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    case_type: Mapped[str] = mapped_column(Text, nullable=False)
    input_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )
    expected_behavior: Mapped[str] = mapped_column(Text, nullable=False)
    expected_output_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'active'"))
    created_by_user_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    template: Mapped[PromptTemplate] = relationship(
        back_populates="test_cases",
        foreign_keys=[prompt_template_id],
    )
