"""create audit events table

Revision ID: 0003_audit_events
Revises: 0002_model_gateway
Create Date: 2026-07-31 00:00:00.000000
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003_audit_events"
down_revision: str | None = "0002_model_gateway"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Audit events are append-only operational history for important state
    # changes. JSONB before/after columns keep the table generic across domains.
    op.create_table(
        "audit_events",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("actor_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("actor_type", sa.Text(), nullable=False),
        sa.Column("action", sa.Text(), nullable=False),
        sa.Column("subject_type", sa.Text(), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("request_id", sa.Text(), nullable=True),
        sa.Column("trace_id", sa.Text(), nullable=True),
        sa.Column("idempotency_key", sa.Text(), nullable=True),
        sa.Column("before_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("after_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "metadata_json",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "actor_type in ('user','agent','system','worker','provider','optimizer')",
            name="actor_type",
        ),
        sa.ForeignKeyConstraint(
            ["actor_user_id"],
            ["users.id"],
            name="fk_audit_events_actor_user_id_users",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_audit_events_tenant_id_tenants",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_audit_events"),
    )
    op.create_index(
        "idx_audit_events_tenant_created",
        "audit_events",
        ["tenant_id", "created_at"],
    )
    op.create_index("idx_audit_events_subject", "audit_events", ["subject_type", "subject_id"])
    op.create_index("idx_audit_events_actor", "audit_events", ["actor_user_id", "created_at"])
    op.create_index(
        "idx_audit_events_trace_id",
        "audit_events",
        ["trace_id"],
        postgresql_where=sa.text("trace_id is not null"),
    )


def downgrade() -> None:
    # Downgrade reverses the indexes first, then the table.
    op.drop_index("idx_audit_events_trace_id", table_name="audit_events")
    op.drop_index("idx_audit_events_actor", table_name="audit_events")
    op.drop_index("idx_audit_events_subject", table_name="audit_events")
    op.drop_index("idx_audit_events_tenant_created", table_name="audit_events")
    op.drop_table("audit_events")
