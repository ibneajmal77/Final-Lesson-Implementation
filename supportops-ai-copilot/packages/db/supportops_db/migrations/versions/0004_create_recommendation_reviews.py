"""create recommendation reviews

Revision ID: 0004_rec_reviews
Revises: 0003_model_outputs
Create Date: 2026-07-11
"""

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
        sa.Column("reviewer_user_id", sa.String(length=200), nullable=False),
        sa.Column("decision", sa.String(length=50), nullable=False),
        sa.Column("final_summary", sa.Text(), nullable=True),
        sa.Column("final_reply", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["recommendation_id"],
            ["ticket_recommendations.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_recommendation_reviews_tenant_id",
        "recommendation_reviews",
        ["tenant_id"],
    )
    op.create_index(
        "ix_recommendation_reviews_ticket_id",
        "recommendation_reviews",
        ["ticket_id"],
    )
    op.create_index(
        "ix_recommendation_reviews_recommendation_id",
        "recommendation_reviews",
        ["recommendation_id"],
    )
    op.create_index(
        "ix_recommendation_reviews_tenant_ticket",
        "recommendation_reviews",
        ["tenant_id", "ticket_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_recommendation_reviews_tenant_ticket", table_name="recommendation_reviews")
    op.drop_index(
        "ix_recommendation_reviews_recommendation_id",
        table_name="recommendation_reviews",
    )
    op.drop_index("ix_recommendation_reviews_ticket_id", table_name="recommendation_reviews")
    op.drop_index("ix_recommendation_reviews_tenant_id", table_name="recommendation_reviews")
    op.drop_table("recommendation_reviews")

