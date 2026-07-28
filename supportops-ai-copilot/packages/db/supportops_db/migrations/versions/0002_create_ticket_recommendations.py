"""create ticket recommendations

Revision ID: 0002_ticket_recs
Revises: 0001_identity_tickets
Create Date: 2026-07-11
"""

# ============================================================================
# MIGRATION 2 — adds the table that holds analysis results.
#
# WHAT IT ADDS: `ticket_recommendations`, where every analysis conclusion is
# stored — what the ticket is about, how urgent, and whether a human specialist
# is needed.
#
# THE STORY THE MIGRATION NUMBERS TELL:
#   At this point in the project's history, only the free keyword classifier
#   existed. That is why this table has NO columns for a model name, a summary,
#   or a draft reply — there was no AI yet. Those arrive in migration 0003, and
#   the gap between the two is the moment the AI was introduced.
#
#   Reading migrations in order is often the clearest way to understand how a
#   system grew and why it is shaped as it is.
#
# See 0001 for how migration files work in general — the chain, upgrade/downgrade,
# and why applied migrations must never be edited.
# ============================================================================

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_ticket_recs"
down_revision: str | None = "0001_identity_tickets"   # runs after migration 1
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ticket_recommendations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("ticket_id", sa.String(length=36), nullable=False),
        # Which method produced this: "baseline_v1" at this point in history.
        # The column that later makes it possible to compare the AI against the
        # keyword rules.
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("requires_escalation", sa.Boolean(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),          # 0.0 to 1.0
        sa.Column("extracted_fields_json", sa.JSON(), nullable=False),
        sa.Column("reasons_json", sa.JSON(), nullable=False),         # why it decided this
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        # TWO foreign keys. Strictly the ticket alone would identify the company,
        # but storing tenant_id directly means the security filter can be applied
        # without joining to the tickets table on every query.
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        # Note: NO unique constraint. Deliberate — a ticket may have many
        # recommendations, from different methods or repeated attempts, and none
        # is ever overwritten.
    )
    # Three indexes, matching the three ways this table actually gets searched:
    # by company, by ticket, and by both together (which is what the listing
    # endpoint does).
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


# Reverse order, as always: indexes first, then the table.
# Reminder: this DELETES every recommendation ever recorded.
def downgrade() -> None:
    op.drop_index("ix_ticket_recommendations_tenant_ticket", table_name="ticket_recommendations")
    op.drop_index("ix_ticket_recommendations_ticket_id", table_name="ticket_recommendations")
    op.drop_index("ix_ticket_recommendations_tenant_id", table_name="ticket_recommendations")
    op.drop_table("ticket_recommendations")
