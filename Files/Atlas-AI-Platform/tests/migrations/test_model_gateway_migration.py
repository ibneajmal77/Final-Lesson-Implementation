"""Migration metadata tests for model gateway and prompt table registration."""

from pathlib import Path

from packages.db import models
from packages.db.base import Base


def test_model_gateway_models_are_registered_for_alembic() -> None:
    assert models.ModelProvider.__tablename__ == "model_providers"
    assert models.ModelRoute.__tablename__ == "model_routes"
    assert models.AIRun.__tablename__ == "ai_runs"
    assert models.CostRecord.__tablename__ == "cost_records"
    assert {"model_providers", "model_routes", "ai_runs", "cost_records"}.issubset(
        Base.metadata.tables.keys()
    )


def test_phase02_models_are_registered_for_alembic() -> None:
    assert models.AuditEvent.__tablename__ == "audit_events"
    assert models.PromptTemplate.__tablename__ == "prompt_templates"
    assert models.PromptVersion.__tablename__ == "prompt_versions"
    assert models.PromptTestCase.__tablename__ == "prompt_test_cases"
    assert {
        "audit_events",
        "prompt_templates",
        "prompt_versions",
        "prompt_test_cases",
    }.issubset(Base.metadata.tables.keys())


def test_model_gateway_migration_includes_cost_records() -> None:
    migration = Path("packages/db/migrations/versions/0002_model_gateway.py").read_text(
        encoding="utf-8"
    )
    assert 'down_revision: str | None = "0001_initial_foundation"' in migration
    assert '"cost_records"' in migration
    assert "uq_model_routes_global_route_key" in migration
