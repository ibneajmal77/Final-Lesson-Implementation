"""create identity and ticket tables

Revision ID: 0001_identity_tickets
Revises:
Create Date: 2026-07-10
"""

# ============================================================================
# FILE: migrations/versions/0001_create_identity_and_ticket_tables.py
#
# THIS IS MIGRATION NUMBER 1 — the very first one. It builds the foundation:
# companies, their people, and their tickets.
#
# HOW TO READ ANY MIGRATION FILE (they all share this shape):
#   - The docstring above names it and dates it.
#   - The four variables below say WHERE this migration sits in the chain.
#   - upgrade()   applies the change, moving the database forwards.
#   - downgrade() undoes it, moving the database backwards.
#
# THE CHAIN — the idea that makes migrations reliable:
#   Each migration names the one before it (`down_revision`), forming a linked
#   list: 0001 <- 0002 <- 0003 ... Alembic follows that chain to work out what to
#   run and in which order. It also records in the database which ones have been
#   applied, so running the command twice does nothing the second time.
#
#   This one has `down_revision = None`, which marks it as the beginning.
#
# THE RULE THAT MATTERS MOST: NEVER EDIT AN APPLIED MIGRATION.
#   Once a migration has run anywhere — a colleague's laptop, staging,
#   production — changing it is meaningless: those databases already recorded it
#   as done and will not run it again. Your change would apply only to databases
#   built from scratch afterwards, so two installations would silently end up
#   with different schemas. Always add a NEW migration instead.
#
# THIS FILE MUST STAY IN STEP WITH models.py. Migrations create the real tables;
# models.py describes what the code expects. Changing one without the other is
# the classic mistake: the code confidently reads a column that does not exist.
# The test in tests/db/test_migration_files.py exists to catch some of that drift.
# ============================================================================

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# --- The chain metadata -----------------------------------------------------
revision: str = "0001_identity_tickets"     # this migration's own name
down_revision: str | None = None            # None = this is the first. 0002 will name this one
branch_labels: str | Sequence[str] | None = None   # for parallel migration branches;
                                                    # unused here, and rarely needed
depends_on: str | Sequence[str] | None = None      # for cross-branch dependencies; also unused


# Applies the change: creates three tables and their indexes.
#
# The ORDER IS NOT OPTIONAL. Tenants must exist before users and tickets, because
# both point at tenants with a foreign key, and a database will refuse to create
# a reference to a table that is not there yet.
def upgrade() -> None:
    # --- TENANTS: the customer companies ---
    op.create_table(
        "tenants",
        # Note that every column is spelled out again here, even though models.py
        # already describes them. That duplication is deliberate, not an
        # oversight: this file is a historical record of a change that was
        # applied on a particular date. It must keep working forever, exactly as
        # written, even after models.py has moved on. Importing from models.py
        # instead would mean this migration's behaviour changed retroactively
        # whenever someone edited a model — which would make the whole chain
        # untrustworthy.
        sa.Column("id", sa.String(length=36), nullable=False),        # 36 = a UUID's length
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # A unique index on slug: makes lookups fast AND forbids duplicates, both in
    # one object. `unique=True` is what does the second part.
    op.create_index("ix_tenants_slug", "tenants", ["slug"], unique=True)

    # --- USERS: people who work at those companies ---
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),    # 320 = the maximum
                                                                      # length of an email
                                                                      # address by standard
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        # The database itself now guarantees a user cannot belong to a
        # non-existent company, and that deleting a company removes its users.
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        # Unique WITHIN a company, not globally — so the same person can work for
        # two different customer companies.
        sa.UniqueConstraint("tenant_id", "email", name="uq_users_tenant_email"),
    )
    op.create_index("ix_users_tenant_id", "users", ["tenant_id"])

    # --- TICKETS: the customer support requests ---
    op.create_table(
        "tickets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("external_id", sa.String(length=200), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=False),
        sa.Column("subject", sa.String(length=500), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),                 # Text = unlimited length
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("customer_id", sa.String(length=200), nullable=True),   # the only optional one
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        # THE DUPLICATE GUARD. The application checks for an existing ticket
        # before creating one, but this constraint is what makes a duplicate
        # genuinely impossible — including when two requests arrive at the same
        # instant and both pass the application's check.
        sa.UniqueConstraint("tenant_id", "external_id", name="uq_tickets_tenant_external_id"),
    )
    op.create_index("ix_tickets_tenant_id", "tickets", ["tenant_id"])
    # A two-column index, for the query the app runs most: "this company's OPEN
    # tickets". See models.py for why column order matters in a composite index.
    op.create_index("ix_tickets_tenant_status", "tickets", ["tenant_id", "status"])


# Undoes the change. Run by `alembic downgrade`.
#
# NOTE THE ORDER IS EXACTLY REVERSED from upgrade(). That is required, not
# stylistic: tickets and users point at tenants, so dropping tenants first would
# be refused by the database. Anything created last must be destroyed first.
#
# A SERIOUS WARNING WORTH INTERNALISING: `drop_table` DELETES ALL THE DATA IN IT.
# Running downgrade on a production database destroys everything those tables
# held, permanently. Migrations are usually written forwards-only in practice,
# and a downgrade is treated as a last resort with a backup already in hand.
def downgrade() -> None:
    op.drop_index("ix_tickets_tenant_status", table_name="tickets")
    op.drop_index("ix_tickets_tenant_id", table_name="tickets")
    op.drop_table("tickets")
    op.drop_index("ix_users_tenant_id", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_tenants_slug", table_name="tenants")
    op.drop_table("tenants")
