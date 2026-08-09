"""Root pytest fixtures shared by every test package.

Two problems are solved here.

First, cost. Each test module used to probe PostgreSQL itself. With the local
`connect_timeout=3` and two candidate addresses (`::1` then `127.0.0.1`), every
probe cost about six seconds, and the suite spent over two minutes doing nothing
but timing out. `database_status()` is cached, so the probe happens once per
process no matter how many tests ask.

Second, consistency. Modules that forgot to probe reported a hard failure while
their siblings skipped, for the same missing dependency. `require_database` is
the single guard, and a module applies it once via `pytestmark`.

Python notes for .NET reviewers:
- `conftest.py` is discovered by pytest automatically; nothing imports it.
- `@lru_cache` memoizes a function, so the body runs once per argument set.
"""

from __future__ import annotations

from functools import lru_cache

import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from packages.db.session import get_engine


@lru_cache(maxsize=1)
def database_status() -> str | None:
    """Return None when PostgreSQL is reachable, otherwise the failure class name.

    The result is cached for the whole test session. That is safe because a
    database that is down when the suite starts is not expected to come up
    halfway through, and it turns N slow probes into exactly one.
    """
    try:
        with get_engine().connect() as connection:
            connection.execute(text("select 1"))
    except SQLAlchemyError as exc:
        return exc.__class__.__name__
    return None


def skip_without_database(context: str) -> None:
    """Skip the calling test when PostgreSQL is unavailable."""
    status = database_status()
    if status is not None:
        pytest.skip(f"database unavailable for {context}: {status}")


@pytest.fixture()
def require_database() -> None:
    """Guard fixture for database-backed tests.

    Apply it to a whole module with:

        pytestmark = pytest.mark.usefixtures("require_database")

    which is how a module-level guard stays impossible to forget for one test.
    """
    skip_without_database("database-backed tests")
