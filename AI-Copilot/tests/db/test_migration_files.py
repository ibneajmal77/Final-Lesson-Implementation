from pathlib import Path


def test_alembic_configuration_exists() -> None:
    assert Path("alembic.ini").exists()


def test_initial_migration_exists() -> None:
    migration = Path(
        "packages/db/supportops_db/migrations/versions/"
        "0001_create_identity_and_ticket_tables.py"
    )

    assert migration.exists()
