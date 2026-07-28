"""add model output fields

Revision ID: 0003_model_outputs
Revises: 0002_ticket_recs
Create Date: 2026-07-11
"""

# ============================================================================
# MIGRATION 3 — THE MOMENT THE AI ARRIVED.
#
# This short file is the most historically significant migration in the project.
# It adds the four columns that only a language model can fill in:
#
#   model_name      - which model produced this
#   prompt_version  - which version of our instructions it was given
#   summary         - a short recap of the customer's problem
#   suggested_reply - the draft reply itself
#
# Before this, the system could only CLASSIFY tickets using keyword rules. After
# it, the system can WRITE. Everything else in the product — the human approval
# step, the pilot rollout, the cost tracking — exists because of what these four
# columns made possible.
#
# WHY EVERY NEW COLUMN IS nullable=True — THE MOST IMPORTANT LESSON HERE:
#   This table already contained rows when this migration ran. Adding a required
#   (NOT NULL) column to a table with existing data is REJECTED by the database:
#   it cannot invent values for rows that predate the column.
#
#   There are only three ways to add a column to a populated table:
#     1. Make it nullable (what happened here) — simple and safe
#     2. Give it a default value, which is written into every existing row —
#        safe, but on a very large table it rewrites every row and can lock it
#        for a long time
#     3. Add it nullable, backfill the values in batches, then make it required
#        — three separate migrations, and the correct approach when a column
#        genuinely must not be null
#
#   Here, nullable is not merely a workaround — it is CORRECT. Baseline
#   recommendations legitimately have no model name and no draft reply, so these
#   columns stay empty for them forever. The nullability carries real meaning:
#   "this row came from keyword rules, not from an AI".
#
# Note also that adding a nullable column is one of the cheapest possible schema
# changes: modern Postgres records it in metadata without touching existing rows,
# so it completes almost instantly even on a huge table.
# ============================================================================

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_model_outputs"
down_revision: str | None = "0002_ticket_recs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Which specific model wrote this, e.g. "gpt-5.6". Recorded so that when
    # quality shifts, you can tell whether the model changed underneath you.
    op.add_column(
        "ticket_recommendations",
        sa.Column("model_name", sa.String(length=100), nullable=True),
    )
    # Which version of OUR instructions it was given. The essential companion to
    # model_name: an identical model produces very different results under
    # different prompts, so knowing one without the other explains nothing.
    op.add_column(
        "ticket_recommendations",
        sa.Column("prompt_version", sa.String(length=100), nullable=True),
    )
    # `Text` rather than `String(n)` for both of these — no length limit, because
    # any cap on a piece of prose would be arbitrary. The API schema applies its
    # own limits; the database chooses not to.
    op.add_column(
        "ticket_recommendations",
        sa.Column("summary", sa.Text(), nullable=True),
    )
    op.add_column(
        "ticket_recommendations",
        sa.Column("suggested_reply", sa.Text(), nullable=True),
    )


# Removes the four columns, in reverse order.
#
# The reverse order is cosmetic here — dropping columns has no ordering
# requirement the way dropping tables does — but keeping the convention makes
# every migration read the same way.
#
# Worth stating plainly: this would delete every draft reply the AI has ever
# written.
def downgrade() -> None:
    op.drop_column("ticket_recommendations", "suggested_reply")
    op.drop_column("ticket_recommendations", "summary")
    op.drop_column("ticket_recommendations", "prompt_version")
    op.drop_column("ticket_recommendations", "model_name")
