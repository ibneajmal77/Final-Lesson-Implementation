"""SQLAlchemy engine and session helpers.

The `Engine` is like a pooled ADO.NET connection factory. A `Session` is the
short-lived unit-of-work object, similar in lifetime to an EF Core `DbContext`.

Python note: a function that uses `yield` is a generator. FastAPI treats
`get_db_session` as a dependency with setup before `yield` and cleanup after it.
"""

from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from packages.core.config import get_settings

_engine: Engine | None = None
_engine_url: str | None = None
_SessionLocal: sessionmaker[Session] | None = None
_session_engine: Engine | None = None


def get_engine(database_url: str | None = None) -> Engine:
    """Return a cached SQLAlchemy engine for the configured database URL."""
    global _engine, _engine_url

    resolved_database_url = database_url or get_settings().database_url
    if _engine is None or _engine_url != resolved_database_url:
        # Tests can override the database URL; dispose the old pool when that
        # happens so connections never point at the previous database.
        if _engine is not None:
            _engine.dispose()
        _engine = create_engine(resolved_database_url, pool_pre_ping=True)
        _engine_url = resolved_database_url
    return _engine


def get_session_factory(database_url: str | None = None) -> sessionmaker[Session]:
    """Return a cached factory that creates request-scoped Session objects."""
    global _SessionLocal, _session_engine

    engine = get_engine(database_url)
    if _SessionLocal is None or _session_engine is not engine:
        _SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        _session_engine = engine
    return _SessionLocal


def get_db_session() -> Generator[Session, None, None]:
    """FastAPI dependency that yields one database session per request."""
    session = get_session_factory()()
    try:
        yield session
    finally:
        # This runs after the endpoint returns or raises, like disposing DbContext.
        session.close()
