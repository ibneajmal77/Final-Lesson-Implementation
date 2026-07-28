# ============================================================================
# FILE: tests/db/test_migration_files.py
#
# THINK OF THIS FILE AS: a roll call for the database's construction history.
#
# WHAT THIS TESTS: that alembic.ini and every expected migration file from
# packages/db/supportops_db/migrations/versions/ still exist at their agreed
# repository paths.
#
# A MIGRATION is a numbered instruction for changing a live database's shape:
# create a table, add a column, or add an index. Alembic is the tool that follows
# those instructions in order. It records which revisions already ran, so asking
# it to upgrade again does not repeat completed work. That property is called
# IDEMPOTENCE: repeating an operation has the same result as doing it once.
#
# WHERE THIS SITS IN THE DATABASE FLOW:
#   packages/db/supportops_db/models.py describes the schema Python expects
#     -> a new file in migrations/versions/ records how an existing database
#        reaches that schema
#       -> alembic.ini and migrations/env.py tell Alembic how to connect and run
#         -> the "migrate" service in docker-compose.yml applies the chain
#
# WHY EXISTENCE TESTS HELP: deleting or misnaming a migration can break a fresh
# installation even when an already-upgraded developer database still works.
# These checks make each historical step an explicit repository contract.
#
# HONEST LIMITATION: existence is all this file proves. It does not import the
# revisions, inspect their "down_revision" links, execute their upgrade code, or
# compare the resulting database with models.py. The "migrations" job in
# .github/workflows/ci.yml supplies those stronger checks with "alembic upgrade
# head" and "alembic check".
#
# No pytest FIXTURE is used. A fixture is shared setup provided to tests; these
# tests only need Path, Python's file-location helper.
#
# WHO USES IT / WHAT LIVES HERE: alembic.ini is the entry configuration;
# packages/db/supportops_db/migrations/env.py connects Alembic to application
# settings and metadata; migrations 0001 through 0007 are the history checked
# below; tests/db/test_models.py separately inspects the in-memory model schema.
# ============================================================================
from pathlib import Path


# The chain is unusable without its root configuration. This path is also what
# lets commands such as "python -m alembic upgrade head" find migration settings.
def test_alembic_configuration_exists() -> None:
    assert Path("alembic.ini").exists()


# Migration 0001 lays the foundation: tenants, users, and support tickets.
# Everything later points back to one or more of these tables.
def test_initial_migration_exists() -> None:
    # Python joins adjacent string literals inside parentheses. Splitting this long
    # path keeps the code readable without changing the path value.
    migration = Path(
        "packages/db/supportops_db/migrations/versions/"
        "0001_create_identity_and_ticket_tables.py"
    )

    # Path.exists asks the file system whether anything is present at this location.
    # It deliberately does not open the file or decide whether its Python is valid.
    assert migration.exists()


# Migration 0002 adds ticket_recommendations, where baseline or AI analysis
# results are stored against a tenant and ticket.
def test_ticket_recommendation_migration_exists() -> None:
    migration = Path(
        "packages/db/supportops_db/migrations/versions/"
        "0002_create_ticket_recommendations.py"
    )

    assert migration.exists()


# Migration 0003 adds model name, prompt version, summary, and suggested reply
# fields to recommendations. That is the schema step that introduced AI output.
def test_model_output_migration_exists() -> None:
    migration = Path(
        "packages/db/supportops_db/migrations/versions/"
        "0003_add_model_output_fields.py"
    )

    assert migration.exists()


# Migration 0004 creates recommendation_reviews, the audit record for the human
# approval, edit, or rejection required before a draft reaches a customer.
def test_recommendation_review_migration_exists() -> None:
    migration = Path(
        "packages/db/supportops_db/migrations/versions/"
        "0004_create_recommendation_reviews.py"
    )

    assert migration.exists()

# Migration 0005 creates ai_runs. That table tracks queued background work from
# routes/tickets.py through apps/worker/supportops_worker/jobs.py, including
# running, successful, abstained, and failed outcomes.
def test_ai_run_migration_exists() -> None:
    migration = Path(
        "packages/db/supportops_db/migrations/versions/"
        "0005_create_ai_runs.py"
    )

    assert migration.exists()

# Migration 0006 creates cost_events: one traceable usage record per model call,
# linked back to the tenant and, when available, its ticket, run, and result.
def test_cost_event_migration_exists() -> None:
    migration = Path(
        "packages/db/supportops_db/migrations/versions/"
        "0006_create_cost_events.py"
    )

    assert migration.exists()

# Migration 0007 adds tenant support policies and data-expiry columns.
#
# CANDOUR: its retention columns only mark when data expires. The cleanup code
# in apps/worker/supportops_worker/retention.py currently counts expired rows but
# does not delete them, so this file must not be mistaken for proof of deletion.
def test_security_policy_and_retention_migration_exists() -> None:
    migration = Path(
        "packages/db/supportops_db/migrations/versions/"
        "0007_security_policies_and_retention.py"
    )

    assert migration.exists()
