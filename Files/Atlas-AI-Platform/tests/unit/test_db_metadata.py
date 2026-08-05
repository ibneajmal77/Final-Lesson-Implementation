"""Unit tests for SQLAlchemy metadata configuration.

These tests protect migration stability by verifying deterministic constraint
names, similar to checking EF model conventions.
"""

from packages.db import models
from packages.db.base import NAMING_CONVENTION, Base


def test_foundation_models_are_registered_for_alembic() -> None:
    assert models.Tenant.__tablename__ == "tenants"
    assert models.User.__tablename__ == "users"
    assert {
        "tenants",
        "users",
        "ai_runs",
        "cost_records",
        "audit_events",
        "prompt_templates",
        "prompt_versions",
        "prompt_test_cases",
    }.issubset(Base.metadata.tables.keys())


def test_base_metadata_has_stable_naming_convention() -> None:
    assert Base.metadata.naming_convention == NAMING_CONVENTION
    assert NAMING_CONVENTION["pk"] == "pk_%(table_name)s"
    assert NAMING_CONVENTION["fk"] == "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
