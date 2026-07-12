from pathlib import Path


def test_alembic_configuration_exists() -> None:
    assert Path("alembic.ini").exists()


def test_initial_migration_exists() -> None:
    migration = Path(
        "packages/db/supportops_db/migrations/versions/"
        "0001_create_identity_and_ticket_tables.py"
    )

    assert migration.exists()


def test_ticket_recommendation_migration_exists() -> None:
    migration = Path(
        "packages/db/supportops_db/migrations/versions/"
        "0002_create_ticket_recommendations.py"
    )

    assert migration.exists()


def test_model_output_migration_exists() -> None:
    migration = Path(
        "packages/db/supportops_db/migrations/versions/"
        "0003_add_model_output_fields.py"
    )

    assert migration.exists()


def test_recommendation_review_migration_exists() -> None:
    migration = Path(
        "packages/db/supportops_db/migrations/versions/"
        "0004_create_recommendation_reviews.py"
    )

    assert migration.exists()
