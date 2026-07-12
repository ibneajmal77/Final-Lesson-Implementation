"""create ticket recommendations

Revision ID: 0002_ticket_recs
Revises: 0001_identity_tickets
Create Date: 2026-07-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_ticket_recs"
down_revision: str | None = "0001_identity_tickets"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ticket_recommendations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("ticket_id", sa.String(length=36), nullable=False),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("requires_escalation", sa.Boolean(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("extracted_fields_json", sa.JSON(), nullable=False),
        sa.Column("reasons_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ticket_recommendations_tenant_id",
        "ticket_recommendations",
        ["tenant_id"],
    )
    op.create_index(
        "ix_ticket_recommendations_ticket_id",
        "ticket_recommendations",
        ["ticket_id"],
    )
    op.create_index(
        "ix_ticket_recommendations_tenant_ticket",
        "ticket_recommendations",
        ["tenant_id", "ticket_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_ticket_recommendations_tenant_ticket", table_name="ticket_recommendations")
    op.drop_index("ix_ticket_recommendations_ticket_id", table_name="ticket_recommendations")
    op.drop_index("ix_ticket_recommendations_tenant_id", table_name="ticket_recommendations")
    op.drop_table("ticket_recommendations")

