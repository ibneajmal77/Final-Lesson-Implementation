"""add model output fields

Revision ID: 0003_model_outputs
Revises: 0002_ticket_recs
Create Date: 2026-07-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_model_outputs"
down_revision: str | None = "0002_ticket_recs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "ticket_recommendations",
        sa.Column("model_name", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "ticket_recommendations",
        sa.Column("prompt_version", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "ticket_recommendations",
        sa.Column("summary", sa.Text(), nullable=True),
    )
    op.add_column(
        "ticket_recommendations",
        sa.Column("suggested_reply", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("ticket_recommendations", "suggested_reply")
    op.drop_column("ticket_recommendations", "summary")
    op.drop_column("ticket_recommendations", "prompt_version")
    op.drop_column("ticket_recommendations", "model_name")

