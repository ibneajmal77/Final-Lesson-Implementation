"""create ai runs

Revision ID: 0005_ai_runs
Revises: 0004_rec_reviews
Create Date: 2026-07-15
"""

# ============================================================================
# MIGRATION 5 — THE MOMENT ANALYSIS BECAME ASYNCHRONOUS.
#
# Note the date gap: four days after migration 0004, where the earlier ones came
# a day apart. That gap is the background worker being built.
#
# WHAT PROBLEM THIS SOLVED:
#   Until now, asking the AI to analyse a ticket meant making the caller WAIT for
#   the answer — several seconds of a frozen web page, with a whole server
#   connection tied up doing nothing. That does not survive contact with real
#   traffic.
#
#   The fix was to hand the work to a separate background program. But the moment
#   work happens somewhere else, it needs a JOB SHEET: something recording that
#   the job exists, whether it has started, and how it ended. Nothing in the
#   database could express that before — a recommendation only exists once the
#   work SUCCEEDED, so there was nowhere to record "in progress" or "failed".
#
#   This table is that job sheet, and it is what makes the whole queued path in
#   apps/worker/ possible.
#
# THE STATE MACHINE IT STORES:
#   queued -> running -> succeeded / abstained / failed
#
# See 0001 for how migration files work in general.
# ============================================================================

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0005_ai_runs"
down_revision: str | None = "0004_rec_reviews"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ai_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("ticket_id", sa.String(length=36), nullable=False),
        # Points at the result, once there is one. Nullable because the job sheet
        # is created BEFORE the work runs — and stays null forever if it failed.
        sa.Column("output_recommendation_id", sa.String(length=36), nullable=True),
        sa.Column("run_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        # All nullable for the same reason: none of these are known at the moment
        # the job sheet is written. The worker fills them in when it actually runs.
        sa.Column("prompt_version", sa.String(length=100), nullable=True),
        sa.Column("model_provider", sa.String(length=50), nullable=True),
        sa.Column("model_name", sa.String(length=100), nullable=True),
        # Exactly 64 characters — the length of a SHA-256 hash in hexadecimal.
        # A fingerprint of the ticket text, so identical inputs are recognisable
        # without storing customer text a second time.
        sa.Column("input_hash", sa.String(length=64), nullable=True),
        # Two error columns: a short stable code for counting in dashboards, and
        # the full message for a human debugging.
        sa.Column("error_code", sa.String(length=100), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        # THREE timestamps, which is what makes this table genuinely useful for
        # operations:
        #   created -> started   = time spent waiting in the queue (worker overloaded?)
        #   started -> finished  = time the AI itself took (provider slow?)
        # Two very different problems, distinguishable only because both moments
        # are recorded separately.
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"], ondelete="CASCADE"),
        # NOTE "SET NULL" HERE, not CASCADE — the one place in this file where the
        # delete behaviour differs, and it is a considered choice.
        #
        # If the recommendation is deleted, this link is cleared but THE JOB SHEET
        # SURVIVES. That is what you want: the record that an analysis ran, how
        # long it took, and what it cost should outlive the text it produced.
        # CASCADE here would quietly erase that history every time retention
        # cleanup removed a recommendation.
        sa.ForeignKeyConstraint(
            ["output_recommendation_id"],
            ["ticket_recommendations.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_runs_tenant_id", "ai_runs", ["tenant_id"])
    op.create_index("ix_ai_runs_ticket_id", "ai_runs", ["ticket_id"])
    # The polling query: "this company's jobs for this ticket", asked every couple
    # of seconds by any web page waiting on an analysis.
    op.create_index("ix_ai_runs_tenant_ticket", "ai_runs", ["tenant_id", "ticket_id"])
    # An index on status ALONE, with no tenant column — unusual in this project,
    # and deliberate. It serves the operational question "are any jobs stuck?",
    # which means finding everything still marked "running" across every company
    # at once. A monitoring query rather than a user-facing one.
    op.create_index("ix_ai_runs_status", "ai_runs", ["status"])


def downgrade() -> None:
    op.drop_index("ix_ai_runs_status", table_name="ai_runs")
    op.drop_index("ix_ai_runs_tenant_ticket", table_name="ai_runs")
    op.drop_index("ix_ai_runs_ticket_id", table_name="ai_runs")
    op.drop_index("ix_ai_runs_tenant_id", table_name="ai_runs")
    op.drop_table("ai_runs")
