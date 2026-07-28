"""security policies and retention fields

Revision ID: 0007_security
Revises: 0006_cost_events
Create Date: 2026-07-21
"""

# ============================================================================
# MIGRATION 7 — the newest one, and the security and privacy migration.
#
# It does two separate jobs at once:
#
#   1. Creates the `support_policies` table — the per-company written rules that
#      get pasted into the AI's instructions ("never promise a refund over
#      $100"). This is how each customer shapes what the AI is allowed to say.
#
#   2. Adds a `retention_expires_at` column to FIVE existing tables — the expiry
#      date after which a row must be deleted, for privacy compliance.
#
# WHY THE TWO ARE IN ONE MIGRATION:
#   They arrived together as one piece of work: the security and privacy stage
#   (docs/stage-14-security-implementation.md). Grouping related changes in one
#   migration is reasonable — they are applied or rolled back as a unit.
#
# A CAVEAT WORTH KNOWING: adding the retention COLUMNS is not the same as
# actually deleting anything. The cleanup job in apps/worker/retention.py counts
# expired rows and logs the number, but its deletion half is unimplemented. The
# schema is ready; the enforcement is not.
#
# See 0001 for how migration files work in general.
# ============================================================================

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0007_security"
down_revision: str | None = "0006_cost_events"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# The five tables getting a retention column, listed once as a constant rather
# than repeated in both functions below.
#
# Note which tables are NOT here: `tenants` and `users`. Deliberate — deleting a
# company or a person on a timer would break every row that points at them.
# Those are removed by an explicit decision, not by an expiry date.
RETENTION_TABLES = (
    "tickets",                  # the most sensitive: customer names, emails, complaints
    "ai_runs",
    "ticket_recommendations",
    "recommendation_reviews",
    "cost_events",
)


def upgrade() -> None:
    # --- Job 1: the company rulebook table ---
    op.create_table(
        "support_policies",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        # The rule itself, in plain English. `Text` so there is no arbitrary
        # cap — the API applies its own 10,000-character limit instead, for cost
        # reasons rather than storage ones.
        sa.Column("content", sa.Text(), nullable=False),
        # Who wrote it. A loose reference rather than a foreign key, so the
        # record survives the author leaving. Recorded because this text directly
        # steers what the AI tells customers, and "who added this instruction?"
        # is a question that eventually gets asked.
        sa.Column("created_by_user_id", sa.String(length=200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        # This table gets its retention column built in from the start, since it
        # is being created new. The five older tables have theirs added below.
        sa.Column("retention_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        # Rule names unique per company, so "refund-limits" identifies exactly one
        # rule and cannot quietly exist twice with contradictory text — which
        # would be genuinely dangerous when both copies get fed to the AI.
        sa.UniqueConstraint("tenant_id", "name", name="uq_support_policies_tenant_name"),
    )
    op.create_index("ix_support_policies_tenant_id", "support_policies", ["tenant_id"])

    # --- Job 2: add the expiry column to the five existing tables ---
    #
    # A LOOP inside a migration, which is unusual but sensible here: the same
    # column, added identically five times. Writing it out longhand would be five
    # near-identical blocks with an obvious risk of one being missed.
    #
    # `nullable=True` is essential, and for the same reason as in migration 0003:
    # these tables already hold data, and a required column cannot be added to
    # populated rows. Here nullable also carries real meaning — null means "keep
    # this indefinitely", which is the correct default for existing data nobody
    # has yet decided an expiry for.
    for table_name in RETENTION_TABLES:
        op.add_column(
            table_name,
            sa.Column("retention_expires_at", sa.DateTime(timezone=True), nullable=True),
        )


def downgrade() -> None:
    # `reversed(...)` mirrors the upgrade order, keeping the convention. For
    # dropping columns the order is not actually enforced by the database, but
    # every migration reading the same way is worth more than the saved word.
    for table_name in reversed(RETENTION_TABLES):
        op.drop_column(table_name, "retention_expires_at")

    op.drop_index("ix_support_policies_tenant_id", table_name="support_policies")
    op.drop_table("support_policies")
