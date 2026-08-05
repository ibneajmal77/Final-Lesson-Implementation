"""Shared pytest fixtures for prompt tests.

`conftest.py` is pytest's convention-based fixture file. Tests in this folder
can request `db_session` or `tenant` by parameter name without importing them.
"""

from __future__ import annotations

from collections.abc import Generator
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from packages.db.models.identity import Tenant
from packages.db.session import get_engine, get_session_factory
from packages.model_gateway.bootstrap import ensure_default_gateway_config
from packages.prompts.registry import PromptRegistry


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Yield a database session or skip tests when PostgreSQL is unavailable."""
    try:
        with get_engine().connect() as connection:
            connection.execute(text("select 1"))
    except SQLAlchemyError as exc:
        pytest.skip(f"database unavailable for prompt tests: {exc.__class__.__name__}")

    session = get_session_factory()()
    try:
        ensure_default_gateway_config(session)
        PromptRegistry.clear_cache()
        yield session
    finally:
        session.close()
        PromptRegistry.clear_cache()


@pytest.fixture()
def tenant(db_session: Session) -> Tenant:
    """Create a unique tenant row for each test that asks for `tenant`."""
    suffix = uuid4().hex
    tenant = Tenant(name=f"Prompt Tenant {suffix}", slug=f"prompt-tenant-{suffix}")
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)
    return tenant
