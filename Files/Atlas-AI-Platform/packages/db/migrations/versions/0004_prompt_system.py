"""create prompt system tables

Revision ID: 0004_prompt_system
Revises: 0003_audit_events
Create Date: 2026-07-31 00:00:00.000000
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0004_prompt_system"
down_revision: str | None = "0003_audit_events"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Phase 02 adds prompt templates, immutable versions, test cases, and a
    # foreign key from AI runs back to the prompt version that produced them.
    op.create_table(
        "prompt_templates",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("use_case", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("owner_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("status", sa.Text(), server_default=sa.text("'active'"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("status in ('active','archived')", name="status"),
        sa.ForeignKeyConstraint(
            ["owner_user_id"],
            ["users.id"],
            name="fk_prompt_templates_owner_user_id_users",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_prompt_templates_tenant_id_tenants",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_prompt_templates"),
    )
    op.create_index(
        "uq_prompt_templates_id_tenant",
        "prompt_templates",
        ["id", "tenant_id"],
        unique=True,
    )
    op.create_index(
        "uq_prompt_templates_global_name",
        "prompt_templates",
        ["name"],
        unique=True,
        postgresql_where=sa.text("tenant_id is null"),
    )
    op.create_index(
        "uq_prompt_templates_tenant_name",
        "prompt_templates",
        ["tenant_id", "name"],
        unique=True,
        postgresql_where=sa.text("tenant_id is not null"),
    )
    op.create_index(
        "idx_prompt_templates_tenant_use_case",
        "prompt_templates",
        ["tenant_id", "use_case", "status"],
    )

    op.create_table(
        "prompt_versions",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("prompt_template_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("system_prompt", sa.Text(), nullable=False),
        sa.Column("user_template", sa.Text(), nullable=False),
        sa.Column("developer_notes", sa.Text(), nullable=True),
        sa.Column(
            "input_variables_json",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column("output_schema_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "model_defaults_json",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("status", sa.Text(), server_default=sa.text("'draft'"), nullable=False),
        sa.Column("created_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "created_by_actor_type",
            sa.Text(),
            server_default=sa.text("'user'"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("version_number > 0", name="version_number_positive"),
        sa.CheckConstraint(
            "status in ('draft','testing','approved','active','retired')",
            name="status",
        ),
        sa.CheckConstraint(
            "created_by_actor_type in ('user','system','optimizer')",
            name="created_by_actor_type",
        ),
        sa.ForeignKeyConstraint(
            ["created_by_user_id"],
            ["users.id"],
            name="fk_prompt_versions_created_by_user_id_users",
        ),
        sa.ForeignKeyConstraint(
            ["prompt_template_id"],
            ["prompt_templates.id"],
            name="fk_prompt_versions_prompt_template_id_prompt_templates",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_prompt_versions"),
        sa.UniqueConstraint(
            "prompt_template_id",
            "version_number",
            name="uq_prompt_versions_template_version_number",
        ),
    )
    op.create_index(
        "idx_prompt_versions_template_status",
        "prompt_versions",
        ["prompt_template_id", "status"],
    )
    op.create_index(
        "uq_prompt_versions_one_active",
        "prompt_versions",
        ["prompt_template_id"],
        unique=True,
        postgresql_where=sa.text("status = 'active'"),
    )
    # The partial unique index above enforces one active version per template.

    op.create_table(
        "prompt_test_cases",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("prompt_template_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("case_type", sa.Text(), nullable=False),
        sa.Column(
            "input_json",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("expected_behavior", sa.Text(), nullable=False),
        sa.Column("expected_output_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("status", sa.Text(), server_default=sa.text("'active'"), nullable=False),
        sa.Column("created_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "case_type in ('happy_path','edge_case','adversarial','format','regression')",
            name="case_type",
        ),
        sa.CheckConstraint("status in ('active','archived')", name="status"),
        sa.ForeignKeyConstraint(
            ["created_by_user_id"],
            ["users.id"],
            name="fk_prompt_test_cases_created_by_user_id_users",
        ),
        sa.ForeignKeyConstraint(
            ["prompt_template_id"],
            ["prompt_templates.id"],
            name="fk_prompt_test_cases_prompt_template_id_prompt_templates",
        ),
        sa.ForeignKeyConstraint(
            ["prompt_template_id", "tenant_id"],
            ["prompt_templates.id", "prompt_templates.tenant_id"],
            name="fk_prompt_test_cases_prompt_template_id_tenant_prompt_templates",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_prompt_test_cases_tenant_id_tenants",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_prompt_test_cases"),
    )
    op.create_index(
        "uq_prompt_test_cases_template_name",
        "prompt_test_cases",
        ["prompt_template_id", "name"],
        unique=True,
    )
    op.create_index(
        "idx_prompt_test_cases_template_status",
        "prompt_test_cases",
        ["prompt_template_id", "status"],
    )
    op.create_index("idx_prompt_test_cases_tenant_id", "prompt_test_cases", ["tenant_id"])

    op.execute(
        """
        alter table ai_runs
          add constraint fk_ai_runs_prompt_version_id_prompt_versions
          foreign key (prompt_version_id) references prompt_versions(id)
          not valid
        """
    )
    op.execute(
        "alter table ai_runs validate constraint fk_ai_runs_prompt_version_id_prompt_versions"
    )


def downgrade() -> None:
    # Downgrade removes prompt objects and then relaxes the AI run foreign-key
    # hardening introduced by this phase.
    op.drop_constraint(
        "fk_ai_runs_prompt_version_id_prompt_versions",
        "ai_runs",
        type_="foreignkey",
    )
    op.drop_index("idx_prompt_test_cases_tenant_id", table_name="prompt_test_cases")
    op.drop_index("idx_prompt_test_cases_template_status", table_name="prompt_test_cases")
    op.drop_index("uq_prompt_test_cases_template_name", table_name="prompt_test_cases")
    op.drop_table("prompt_test_cases")

    op.drop_index("uq_prompt_versions_one_active", table_name="prompt_versions")
    op.drop_index("idx_prompt_versions_template_status", table_name="prompt_versions")
    op.drop_table("prompt_versions")

    op.drop_index("idx_prompt_templates_tenant_use_case", table_name="prompt_templates")
    op.drop_index("uq_prompt_templates_tenant_name", table_name="prompt_templates")
    op.drop_index("uq_prompt_templates_global_name", table_name="prompt_templates")
    op.drop_index("uq_prompt_templates_id_tenant", table_name="prompt_templates")
    op.drop_table("prompt_templates")
