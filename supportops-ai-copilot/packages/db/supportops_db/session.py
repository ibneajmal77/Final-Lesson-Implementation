# ============================================================================
# FILE: packages/db/supportops_db/session.py
#
# THINK OF THIS FILE AS: the plumbing that opens the connection to Postgres.
#
# Three small functions, each doing one job:
#   to_sqlalchemy_url     - fix up the address format
#   create_db_engine      - open the pool of connections
#   create_session_factory - make the thing that hands out sessions
#
# WHO CALLS THESE:
#   apps/api/.../dependencies.py     - the API, once, cached for the process
#   apps/worker/.../jobs.py          - the worker, once per job
#   apps/api/.../seed.py             - the seeding script
#   packages/db/migrations/env.py    - the migration tool
#   the tests, pointing at a temporary test database
#
# TWO WORDS THAT GET CONFUSED CONSTANTLY:
#   ENGINE  - one per program. Owns a pool of open connections to the database.
#             Expensive to create, so it is made once and reused.
#   SESSION - one per unit of work (usually one web request). Borrows a
#             connection from the engine's pool, tracks the changes you make,
#             and hands the connection back when closed. Cheap and disposable.
# ============================================================================

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


# Converts a standard Postgres address into the form SQLAlchemy wants.
#
# The address in settings.py starts "postgresql://", which is the normal form
# understood by every Postgres tool. But SQLAlchemy can talk to Postgres through
# several different driver libraries, and the part after the "+" is how you tell
# it which one to use. This project uses "psycopg" (version 3).
#
# Without this rewrite SQLAlchemy would pick its default driver — psycopg2, the
# older version — which is not installed here, and the failure would be a
# confusing "module not found" at startup.
#
# The `1` in .replace(...) limits it to the FIRST occurrence. A small but real
# safeguard: a password containing the text "postgresql://" would otherwise be
# mangled too.
def to_sqlalchemy_url(database_url: str) -> str:
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    # Anything else is passed through untouched — notably "sqlite://" addresses,
    # which is what the tests use to run against a fast throwaway database
    # instead of a real Postgres server.
    return database_url


# Creates the engine: the connection pool for one program.
#
# `pool_pre_ping=True` is the one setting here, and it earns its place. Pooled
# connections are kept open between uses, and they can go stale — the database
# restarted, or a firewall silently dropped an idle connection. Without this,
# the first request after such an event fails with a baffling "server closed the
# connection" error.
#
# With it, SQLAlchemy sends a tiny test query before handing a connection out,
# and quietly replaces any that has died. It costs a fraction of a millisecond
# per checkout and removes an entire category of intermittent, hard-to-reproduce
# failures — a very good trade.
def create_db_engine(database_url: str) -> Engine:
    return create_engine(to_sqlalchemy_url(database_url), pool_pre_ping=True)


# Creates the session factory — a callable that produces new sessions.
#
# Both settings are deliberate departures from convenience toward predictability.
#
# `autoflush=False`:
#   By default, SQLAlchemy quietly sends your pending changes to the database
#   just before any query, so that the query sees them. Convenient, but it means
#   writes happen at moments you did not choose, which makes surprising ordering
#   bugs and hard-to-place constraint errors. Switched off, nothing reaches the
#   database until code explicitly calls flush() or commit() — which is why the
#   repository functions below all call session.flush() by hand.
#
# `autocommit=False`:
#   Nothing is made permanent until session.commit() is called. This is what
#   gives every request a transaction: a group of changes that all succeed or
#   all fail together. It is the reason routes/tickets.py can save a
#   recommendation and its cost record in one commit and be certain you never
#   end up with one without the other.
def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
