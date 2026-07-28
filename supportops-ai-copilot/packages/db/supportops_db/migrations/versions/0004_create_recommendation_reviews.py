"""create recommendation reviews

Revision ID: 0004_rec_reviews
Revises: 0003_model_outputs
Create Date: 2026-07-11
"""

# ============================================================================
# MIGRATION 4 — adds the human approval step.
#
# Created immediately after the AI arrived in migration 0003, and that ordering
# is the point: the moment the system could WRITE to customers, it needed a
# person standing between it and them.
#
# This table stores every verdict — approved, edited, or rejected — and it does
# double duty:
#   1. Safety. Nothing reaches a customer without a human saying so.
#   2. Measurement. The ratio between the three verdicts is the number that
#      decides whether the AI is worth running at all.
#
# WHY THIS TABLE HAS FOUR INDEXES, more than any other:
#   It is the table the metrics queries hammer. Every report in
#   repositories/metrics.py and repositories/pilot.py joins and groups it, from
#   several different directions, which is why it is worth indexing more heavily
#   than the tables that are merely read one row at a time.
#
# See 0001 for how migration files work in general.
# ============================================================================

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004_rec_reviews"
down_revision: str | None = "0003_model_outputs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "recommendation_reviews",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("ticket_id", sa.String(length=36), nullable=False),
        sa.Column("recommendation_id", sa.String(length=36), nullable=False),
        # WHO decided. Note it is String(200) and NOT a foreign key to users.id,
        # unlike the three IDs above. A loose reference on purpose: if the
        # reviewer later leaves and their user row is removed, the record of who
        # approved this reply must survive. A foreign key with CASCADE would
        # erase exactly the accountability this table exists to provide.
        sa.Column("reviewer_user_id", sa.String(length=200), nullable=False),
        # "approved" / "edited" / "rejected". Stored as plain text; the
        # restriction to those three lives in the API schema, which keeps adding
        # a fourth verdict a code change rather than another migration.
        sa.Column("decision", sa.String(length=50), nullable=False),
        # Nullable because a REJECTION has no agreed text — there is nothing to
        # record. For approvals and edits these hold a COPY of the final wording,
        # so the reply that was actually sent survives even if the original draft
        # is later removed by retention cleanup.
        sa.Column("final_summary", sa.Text(), nullable=True),
        sa.Column("final_reply", sa.Text(), nullable=True),
        # The reviewer's own explanation. Optional, and disproportionately
        # valuable — these notes are what get grouped in the feedback report and
        # usually reveal what the AI keeps getting wrong.
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        # Note there is no updated_at column, unlike tickets and policies. That
        # absence is deliberate and structural: reviews are never edited. A
        # supervisor who disagrees adds a second review; the first stays exactly
        # as recorded. An audit trail you can rewrite is not an audit trail.
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["recommendation_id"],
            ["ticket_recommendations.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # Four indexes, each serving a different question the reports ask:
    op.create_index(
        "ix_recommendation_reviews_tenant_id",         # "this company's reviews"
        "recommendation_reviews",
        ["tenant_id"],
    )
    op.create_index(
        "ix_recommendation_reviews_ticket_id",         # "this ticket's reviews"
        "recommendation_reviews",
        ["ticket_id"],
    )
    op.create_index(
        "ix_recommendation_reviews_recommendation_id", # "this draft's reviews" — the
        "recommendation_reviews",                      # listing endpoint's query
        ["recommendation_id"],
    )
    op.create_index(
        "ix_recommendation_reviews_tenant_ticket",     # both at once, for the reports
        "recommendation_reviews",
        ["tenant_id", "ticket_id"],
    )


# Reverse order: indexes, then the table.
# This would destroy the entire audit trail of human decisions.
def downgrade() -> None:
    op.drop_index("ix_recommendation_reviews_tenant_ticket", table_name="recommendation_reviews")
    op.drop_index(
        "ix_recommendation_reviews_recommendation_id",
        table_name="recommendation_reviews",
    )
    op.drop_index("ix_recommendation_reviews_ticket_id", table_name="recommendation_reviews")
    op.drop_index("ix_recommendation_reviews_tenant_id", table_name="recommendation_reviews")
    op.drop_table("recommendation_reviews")
