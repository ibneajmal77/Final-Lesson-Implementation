"""create cost events

Revision ID: 0006_cost_events
Revises: 0005_ai_runs
Create Date: 2026-07-18
"""

# ============================================================================
# MIGRATION 6 — THE MOMENT SOMEONE ASKED WHAT THIS IS COSTING.
#
# A recognisable stage in the life of any AI feature. It works, it is running on
# real traffic, and then the first invoice arrives and nobody can explain it.
#
# WHY IT CANNOT BE ANSWERED WITHOUT THIS TABLE:
#   AI services charge per token, and tokens are invisible. Nothing in the
#   product surfaces them. Without recording each call, the only cost information
#   available is one monthly total with no breakdown — impossible to attribute to
#   a customer, a model, or a feature, and therefore impossible to act on.
#
#   One row per AI call turns that into a query. And because the rows carry
#   tenant, model, and provider, it answers the questions that actually matter:
#   which customer is expensive, which model is worth its price, and — combined
#   with the review data — what each USEFUL draft costs.
#
# THE DELETE RULES IN THIS FILE ARE THE INTERESTING PART. See the foreign keys
# below: the cost record deliberately outlives most of what it points at.
# ============================================================================

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0006_cost_events"
down_revision: str | None = "0005_ai_runs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "cost_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        # The ONLY required link. Costs must always be attributable to a company,
        # because that is what billing and budgeting depend on.
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        # The other three are optional, because not every call has all of them:
        # the synchronous path has no job sheet, and a failed call produced no
        # recommendation. The cost is recorded regardless — money spent is money
        # spent, whether or not anything usable came back.
        sa.Column("ticket_id", sa.String(length=36), nullable=True),
        sa.Column("ai_run_id", sa.String(length=36), nullable=True),
        sa.Column("recommendation_id", sa.String(length=36), nullable=True),
        # WHAT was called. Required — an unattributed cost cannot be analysed.
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=False),
        sa.Column("prompt_version", sa.String(length=100), nullable=True),
        # "sync_ticket_analysis" / "async_ticket_analysis", so the two paths'
        # costs can be compared separately.
        sa.Column("operation", sa.String(length=100), nullable=False),
        # THE NUMBERS. Input and output tokens are counted separately because
        # they are priced differently — output typically costs several times more
        # — so a single combined figure would hide where the money actually goes.
        sa.Column("input_tokens", sa.Integer(), nullable=False),
        sa.Column("output_tokens", sa.Integer(), nullable=False),
        # A Float, which is worth flagging: floating-point numbers are famously
        # imprecise for money, and real billing would use a fixed-precision
        # decimal type. Acceptable here only because these are ESTIMATES for
        # internal reporting — tokens multiplied by our own configured prices —
        # not amounts anyone is charged.
        sa.Column("estimated_cost_usd", sa.Float(), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=False),   # whole milliseconds
        sa.Column("metadata_json", sa.JSON(), nullable=False),   # room for extra detail
                                                                 # without another migration
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),

        # THE DELETE RULES — the most considered part of this table.
        #
        # Two use CASCADE, two use SET NULL, and the split is deliberate:
        #   tenant  CASCADE  - a deleted company's costs go too; nobody will ever
        #                      bill them again, and privacy law expects the data
        #                      to be removed
        #   ticket  CASCADE  - same reasoning; the cost is personal-adjacent data
        #                      tied to that customer's request
        #   ai_run  SET NULL - the SPEND SURVIVES, losing only its link
        #   recommendation SET NULL - likewise
        #
        # The principle: a payment that actually happened must not vanish from the
        # accounts because a related row was tidied up. The retention job removing
        # an old draft should never make last quarter's spending figures change.
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["ai_run_id"], ["ai_runs.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(
            ["recommendation_id"],
            ["ticket_recommendations.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_cost_events_tenant_id", "cost_events", ["tenant_id"])
    op.create_index("ix_cost_events_ticket_id", "cost_events", ["ticket_id"])
    op.create_index("ix_cost_events_ai_run_id", "cost_events", ["ai_run_id"])
    # The one that earns its keep: "what did this company spend LAST MONTH?" —
    # filtering by company and a date range together, which is the shape almost
    # every cost question takes.
    op.create_index(
        "ix_cost_events_tenant_created_at",
        "cost_events",
        ["tenant_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_cost_events_tenant_created_at", table_name="cost_events")
    op.drop_index("ix_cost_events_ai_run_id", table_name="cost_events")
    op.drop_index("ix_cost_events_ticket_id", table_name="cost_events")
    op.drop_index("ix_cost_events_tenant_id", table_name="cost_events")
    op.drop_table("cost_events")
