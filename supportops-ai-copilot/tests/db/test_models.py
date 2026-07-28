# ============================================================================
# FILE: tests/db/test_models.py
#
# THINK OF THIS FILE AS: a building inspector checking the blueprints — not
# whether anyone lives there, just that the rooms and doors are where the plans
# say they are.
#
# WHAT THIS TESTS: the table definitions in
# packages/db/supportops_db/models.py, plus one small URL helper from
# packages/db/supportops_db/session.py.
#
# THE UNUSUAL THING ABOUT THIS FILE: no database is ever created. Nothing is
# inserted, nothing is queried, there is no fixture at all. Every test reads
# `SomeModel.__table__`, which is the description SQLAlchemy builds in memory
# the moment models.py is imported.
#
# HOW THAT WORKS: SQLAlchemy models are two things at once — a normal Python
# class you create rows with, and a machine-readable SCHEMA describing columns,
# indexes and constraints. These tests inspect the second half. That is why they
# run in milliseconds and need no Postgres.
#
# WHY BOTHER TESTING A SCHEMA AT ALL, given it is just declarations? Because
# several of these details are SAFETY properties rather than conveniences, and
# nothing else in the suite would notice if one quietly disappeared:
#   - tenant_id columns and their indexes are what keep customers separated,
#   - the unique constraints are what stop duplicate rows,
#   - retention_expires_at is what makes deletion-on-schedule possible.
# A dropped index degrades performance silently; a dropped unique constraint
# corrupts data silently. Both are cheap to assert and expensive to discover in
# production.
#
# WHAT THIS FILE CANNOT TELL YOU: whether the real database matches these
# models. It only checks the Python definitions. Keeping the actual migrations
# in step is the job of tests/db/test_migration_files.py.
# ============================================================================

from sqlalchemy import UniqueConstraint

from supportops_db.models import (
    AIRun,
    Base,
    CostEvent,
    RecommendationReview,
    Tenant,
    TenantPolicy,
    Ticket,
    TicketRecommendation,
    User,
)
from supportops_db.session import to_sqlalchemy_url


# THE INVENTORY TEST — does the schema contain all eight expected tables?
#
# `Base.metadata` is SQLAlchemy's registry: every model that inherits from Base
# adds itself to it on import. So this is really asking "did every model file get
# imported and registered?"
#
# WHY IT CATCHES A REAL BUG: a model that is never imported is invisible to
# SQLAlchemy. Its table would simply not be created, and the failure would only
# surface much later as a confusing "no such table" error at runtime.
#
# NOTE `>=` RATHER THAN `==`. Read as "contains at least these". Adding a ninth
# table will not break this test, but removing one of the eight will. That is
# the right trade-off for a growing schema — it guards the essentials without
# forcing an edit here every time the project gains a table.
def test_core_tables_are_registered() -> None:
    assert set(Base.metadata.tables) >= {
        "tenants",
        "users",
        "support_policies",
        "tickets",
        "ticket_recommendations",
        "recommendation_reviews",
        "ai_runs",
        "cost_events",
    }


# The tenant table is the root of the whole multi-tenant design — nearly every
# other table points back to it — so its basic columns are worth pinning down.
#
# `slug` is the URL-safe short name ("tenant-a") used in place of the raw ID in
# addresses and configuration, where a long opaque identifier would be unusable.
def test_tenant_table_columns() -> None:
    columns = Tenant.__table__.columns

    assert "id" in columns
    assert "name" in columns
    assert "slug" in columns
    assert "created_at" in columns


# A UNIQUE CONSTRAINT is a rule the database itself enforces: no two rows may
# share these values. It is a genuine guarantee, not a check the application code
# has to remember to perform.
#
# THE IMPORTANT DETAIL is that this one covers (tenant_id, email) TOGETHER, not
# email alone. So the same address may appear once per tenant but never twice
# within one — which is exactly right for a system where separate customer
# companies may legitimately both employ someone with that address.
#
# A plain unique-on-email rule would be a real bug: one tenant signing up a
# person would block every other tenant from ever adding them.
#
# The comprehension filters to unique constraints specifically, because
# `__table__.constraints` also holds primary keys and foreign keys.
def test_user_table_has_tenant_email_unique_constraint() -> None:
    constraints = {
        constraint.name
        for constraint in User.__table__.constraints
        if isinstance(constraint, UniqueConstraint)
    }

    assert "uq_users_tenant_email" in constraints


# Support policies are the tenant's own written rules — the guidance the AI is
# expected to follow when drafting a reply for that customer.
#
# THE NAMING TRAP HERE, worth flagging: the Python class is `TenantPolicy` but
# the actual table is `support_policies`. The two names differ, which is easy to
# trip over when searching the codebase — grepping for one will not find the
# other.
#
# THREE KINDS OF THING ARE ASSERTED AT ONCE, and each is checked differently:
#   - COLUMNS      : the data itself.
#   - CONSTRAINT   : one policy name per tenant, so names cannot collide.
#   - INDEX        : a lookup shortcut. Without an index on tenant_id, filtering
#                    by tenant means scanning every row of the table — which is
#                    fine at ten rows and ruinous at ten million. Since EVERY
#                    query in this system filters by tenant, this index is on the
#                    hot path for essentially all traffic.
#
# `retention_expires_at` is the "delete me after this date" marker used by the
# data-retention job. Be honest about the state of that: the marker is written
# and asserted here, but the deletion job that acts on it is not implemented yet.
def test_support_policy_table_has_tenant_scope_and_retention_columns() -> None:
    columns = TenantPolicy.__table__.columns
    constraints = {
        constraint.name
        for constraint in TenantPolicy.__table__.constraints
        if isinstance(constraint, UniqueConstraint)
    }
    index_names = {index.name for index in TenantPolicy.__table__.indexes}

    assert "tenant_id" in columns
    assert "name" in columns
    assert "content" in columns
    assert "created_by_user_id" in columns
    assert "retention_expires_at" in columns
    assert "uq_support_policies_tenant_name" in constraints
    assert "ix_support_policies_tenant_id" in index_names


# THE IDEMPOTENCY GUARANTEE — the most consequential constraint in the schema.
#
# "Idempotent" means doing something twice has the same effect as doing it once.
# `external_id` is the ID the ticket carries in the customer's OWN system, so if
# the same ticket is submitted twice — a retried webhook, a network hiccup, a
# duplicated import — the second insert is rejected by the database rather than
# creating a twin.
#
# WHY THAT MATTERS BEYOND TIDINESS: a duplicated ticket means a duplicated AI
# analysis, which means paying the model twice for identical work and showing a
# reviewer the same ticket twice.
#
# Scoped per tenant again, for the same reason as the users table: two unrelated
# customer companies may easily both number a ticket "1001".
def test_ticket_table_has_tenant_external_id_unique_constraint() -> None:
    constraints = {
        constraint.name
        for constraint in Ticket.__table__.constraints
        if isinstance(constraint, UniqueConstraint)
    }

    assert "uq_tickets_tenant_external_id" in constraints


# THREE indexes, and the third is the interesting one.
#
# Two single-column indexes (tenant_id, ticket_id) plus a COMPOSITE index across
# both together. That is not redundant: a database can only use one index per
# lookup, so an index on the exact pair of columns you filter by is markedly
# faster than an index on either one alone.
#
# And "recommendations for ticket X belonging to tenant Y" is precisely the query
# the review screen runs every time someone opens a ticket, so it earns a
# dedicated index. The single-column ones still serve broader queries such as
# "everything for this tenant".
def test_ticket_recommendation_table_has_tenant_and_ticket_indexes() -> None:
    index_names = {index.name for index in TicketRecommendation.__table__.indexes}

    assert "ix_ticket_recommendations_tenant_id" in index_names
    assert "ix_ticket_recommendations_ticket_id" in index_names
    assert "ix_ticket_recommendations_tenant_ticket" in index_names


# These four fields preserve both the AI output and enough information to explain
# where it came from. `model_name` and `prompt_version` make an old draft
# reproducible for an audit; `summary` and `suggested_reply` are the two pieces
# a support agent sees and reviews through routes/tickets.py.
#
# This test checks that the storage slots exist. It deliberately says nothing
# about whether the text inside them is accurate; packages/evals/ owns that job.
def test_ticket_recommendation_table_has_model_output_columns() -> None:
    columns = TicketRecommendation.__table__.columns

    assert "model_name" in columns
    assert "prompt_version" in columns
    assert "summary" in columns
    assert "suggested_reply" in columns


# A review is the permanent record of the required human checkpoint. An AUDIT
# TRAIL means someone can later reconstruct who decided, what they decided, what
# final wording they sent, and any explanation they left.
#
# The two indexes are lookup shortcuts for the common questions asked by
# repositories/recommendation_reviews.py: find the review for this recommendation,
# or find reviews for this tenant and ticket without scanning every customer.
def test_recommendation_review_table_has_audit_columns_and_indexes() -> None:
    columns = RecommendationReview.__table__.columns
    index_names = {index.name for index in RecommendationReview.__table__.indexes}

    assert "reviewer_user_id" in columns
    assert "decision" in columns
    assert "final_summary" in columns
    assert "final_reply" in columns
    assert "notes" in columns
    assert "ix_recommendation_reviews_recommendation_id" in index_names
    assert "ix_recommendation_reviews_tenant_ticket" in index_names


# An AI run is the tracking record for work handed from routes/tickets.py to
# apps/worker/supportops_worker/jobs.py through Redis. The status and timestamps
# describe its lifecycle; success points at an output recommendation, while
# failure keeps a machine-readable code and a human-readable message.
#
# Indexing both tenant-plus-ticket and status supports the two main views:
# history for one ticket, and operational searches for queued or failed work.
def test_ai_run_table_has_status_and_output_columns() -> None:
    columns = AIRun.__table__.columns
    index_names = {index.name for index in AIRun.__table__.indexes}

    assert "run_type" in columns
    assert "status" in columns
    assert "output_recommendation_id" in columns
    assert "error_code" in columns
    assert "error_message" in columns
    assert "started_at" in columns
    assert "finished_at" in columns
    assert "ix_ai_runs_tenant_ticket" in index_names
    assert "ix_ai_runs_status" in index_names


# Every paid model call needs to be traceable back to the tenant, ticket, run,
# and recommendation that caused it. Without those links, a total cost could not
# be investigated or assigned to the customer whose work incurred it.
#
# Token counts are the provider-reported units used for pricing; latency is how
# long the call took. `estimated_cost_usd` is an estimate calculated from the
# rates in apps/api/supportops_api/settings.py, not a provider invoice.
#
# The composite tenant-and-time index makes period reports in
# repositories/cost_events.py practical without scanning the whole ledger.
def test_cost_event_table_has_traceable_usage_columns() -> None:
    columns = CostEvent.__table__.columns
    index_names = {index.name for index in CostEvent.__table__.indexes}

    assert "tenant_id" in columns
    assert "ticket_id" in columns
    assert "ai_run_id" in columns
    assert "recommendation_id" in columns
    assert "provider" in columns
    assert "model" in columns
    assert "input_tokens" in columns
    assert "output_tokens" in columns
    assert "estimated_cost_usd" in columns
    assert "latency_ms" in columns
    assert "ix_cost_events_tenant_created_at" in index_names


# Retention is the rule that customer data should not live forever. Each
# tenant-owned table below must carry the date after which its row may be removed,
# so apps/worker/supportops_worker/retention.py can eventually find expired data.
#
# CANDOUR: that worker currently reports what is due but does not delete it. This
# test proves the schema is prepared for deletion; it does not prove deletion
# happens. Treating those as the same would give a false sense of compliance.
#
# One loop applies the same contract to six models. If a new tenant-owned table is
# added, it also needs adding here or it will escape this schema safety net.
def test_retention_columns_exist_on_tenant_owned_data_tables() -> None:
    models = (
        Ticket,
        AIRun,
        TicketRecommendation,
        RecommendationReview,
        CostEvent,
        TenantPolicy,
    )

    # `model` is a SQLAlchemy class; `__table__.columns` is its in-memory
    # blueprint, so this loop still makes no database connection.
    for model in models:
        assert "retention_expires_at" in model.__table__.columns


# A database URL begins with a DIALECT, the kind of database, and may also name a
# DRIVER, the specific Python library that speaks to it. Configuration uses the
# familiar `postgresql://` form, while SQLAlchemy must be told explicitly to use
# the installed psycopg driver through `postgresql+psycopg://`.
#
# This is a pure string test: it catches a startup-breaking connection mismatch
# without needing Postgres to be running.
def test_database_url_is_converted_for_sqlalchemy_psycopg_driver() -> None:
    url = "postgresql://supportops:supportops@postgres:5432/supportops"

    assert (
        to_sqlalchemy_url(url)
        == "postgresql+psycopg://supportops:supportops@postgres:5432/supportops"
    )


# The helper in packages/db/supportops_db/session.py must be narrow. SQLite URLs
# are useful for lightweight tools and must not be rewritten as though they were
# Postgres. This locks in the leave-unknown-input-alone half of that contract.
def test_non_postgres_url_is_not_changed() -> None:
    url = "sqlite:///local.db"

    assert to_sqlalchemy_url(url) == url
