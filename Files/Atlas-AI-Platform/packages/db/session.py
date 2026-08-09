"""SQLAlchemy engine and session helpers, in both a sync and an async flavor.

The `Engine` is like a pooled ADO.NET connection factory. A `Session` is the
short-lived unit-of-work object, similar in lifetime to an EF Core `DbContext`.

Both flavors exist on purpose, and they are not interchangeable:

- `get_db_session` serves `def` endpoints. Starlette runs those on a threadpool,
  so blocking database I/O there is safe and only costs a thread.
- `get_async_db_session` serves `async def` endpoints. Those run directly on the
  event loop, where a blocking call would stall *every* request in the process,
  not just its own. Anything reached from an `async def` must be awaitable all
  the way down.

The same `postgresql+psycopg://` URL drives both: psycopg3 ships a sync and an
async driver, and SQLAlchemy 2.0 picks the right one based on which engine
factory is used. No second database driver is involved.

Python note: a function that uses `yield` is a generator. FastAPI treats
`get_db_session` as a dependency with setup before `yield` and cleanup after it.
`async def` + `yield` is an async generator, and FastAPI handles it the same way.
"""

from collections.abc import AsyncGenerator, Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from packages.core.config import get_settings

_engine: Engine | None = None
_engine_url: str | None = None
_SessionLocal: sessionmaker[Session] | None = None
_session_engine: Engine | None = None

_async_engine: AsyncEngine | None = None
_async_engine_url: str | None = None
_AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None
_async_session_engine: AsyncEngine | None = None


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


def get_async_engine(database_url: str | None = None) -> AsyncEngine:
    """Return a cached async engine for the configured database URL."""
    global _async_engine, _async_engine_url

    resolved_database_url = database_url or get_settings().database_url
    if _async_engine is None or _async_engine_url != resolved_database_url:
        if _async_engine is not None:
            # `dispose()` on an AsyncEngine returns a coroutine. The engine is
            # only replaced when a test swaps the URL, so the old pool is
            # dropped rather than awaited here; awaiting would require this
            # accessor to become async and infect every caller.
            _async_engine.sync_engine.dispose()
        _async_engine = create_async_engine(resolved_database_url, pool_pre_ping=True)
        _async_engine_url = resolved_database_url
    return _async_engine


def get_async_session_factory(
    database_url: str | None = None,
) -> async_sessionmaker[AsyncSession]:
    """Return a cached factory that creates request-scoped AsyncSession objects."""
    global _AsyncSessionLocal, _async_session_engine

    engine = get_async_engine(database_url)
    if _AsyncSessionLocal is None or _async_session_engine is not engine:
        _AsyncSessionLocal = async_sessionmaker(
            bind=engine,
            autoflush=False,
            expire_on_commit=False,
        )
        _async_session_engine = engine
    return _AsyncSessionLocal


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields one async database session per request.

    Use this only from `async def` endpoints. Handing an AsyncSession to a
    synchronous code path does not fail loudly — it fails at the first implicit
    lazy load, with a MissingGreenlet error far from the actual mistake.
    """
    session = get_async_session_factory()()
    try:
        yield session
    finally:
        await session.close()
