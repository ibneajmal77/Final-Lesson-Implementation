# ============================================================================
# FILE: apps/api/supportops_api/dependencies.py
#
# THINK OF THIS FILE AS: the front desk of the API.
#
# Before any request is allowed to do real work, it stops here for two things:
#   1. "Who are you, and are you allowed in?"    (the security check)
#   2. "Here is your connection to the database." (the tool it needs to work)
#
# In FastAPI (the web framework this project uses), these reusable helpers are
# called "dependencies". A route says what it needs by listing it as one of its
# arguments, and FastAPI automatically runs the matching function from this
# file first, then passes the result in.
#
# HOW A REQUEST TRAVELS THROUGH THE APP:
#   Someone clicks a button in the web page (apps/web/src/app.js)
#     -> the request lands in one of the route files (routes/tickets.py, etc.)
#          -> it stops HERE first: caller is checked, database handed over
#               -> the route asks the "repository" files to talk to the database
#                    (packages/db/supportops_db/repositories/...)
#                      -> the actual Postgres database
#
# Nearly every route file uses the three helpers below, so anything you change
# here changes how the whole API behaves.
# ============================================================================

from collections.abc import Generator, Iterable
from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated, Any

from fastapi import Header, HTTPException, status
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from supportops_api.settings import get_settings  # reads settings like the database address
from supportops_db.session import create_db_engine, create_session_factory

# --- Who is allowed to do what ----------------------------------------------
# This one app serves several different customer companies at the same time.
# Each company is called a "tenant", and every row of data is stamped with the
# tenant it belongs to, so one company can never see another company's tickets.
#
# On top of that, each person has a job title ("role") that decides what they
# can do:
#   agent   - a regular support worker: reads tickets, asks the AI for a draft
#   lead    - a supervisor: can also approve or reject drafts, and change rules
#   admin   - can do everything
#   service - not a person at all; this is the background program (apps/worker)
#             logging in to do its own work
#
# "frozenset" just means a set (a bag of unique values) that can never be
# changed after it is created — a safety measure, so no stray code can quietly
# add "guest" to the list of allowed roles while the app is running.
ALLOWED_ROLES = frozenset({"agent", "lead", "admin", "service"})   # allowed to use the API at all
WRITE_ROLES = frozenset({"agent", "lead", "admin", "service"})     # allowed to save changes
POLICY_WRITE_ROLES = frozenset({"lead", "admin"})                  # only these can change the
                                                                   # safety rules (used in
                                                                   # routes/policies.py)


# A small container holding "who is making this request right now".
#
# "@dataclass" is a shortcut that writes the boring setup code for a simple
# data-holding class. "frozen=True" means: once filled in, it can never be
# edited. That matters because tenant_id is the thing keeping one company's
# data away from another's — we never want a piece of code to quietly swap it
# halfway through handling a request.
@dataclass(frozen=True)
class Actor:
    tenant_id: str   # which company they belong to
    user_id: str     # which person they are (saved on approvals, so we know who decided what)
    role: str        # their job title, from the list above


# Opens the connection to the database.
#
# An "engine" in SQLAlchemy (the database library used here) is the object that
# owns a pool of ready-made connections to Postgres. Making one is expensive.
#
# "@lru_cache" is a memory trick: it means "run this once, then keep giving
# back the same result forever". We want that here, because building a fresh
# engine on every request would slowly use up every available connection.
@lru_cache
def get_engine() -> Engine:
    settings = get_settings()
    return create_db_engine(settings.database_url)


# Makes the little factory that produces "sessions" (see the next function).
# Cached for the same reason: we only ever want one of these, attached to the
# one engine above.
@lru_cache
def get_session_factory():
    return create_session_factory(get_engine())


# Hands a fresh database "session" to a request, then cleans it up afterwards.
#
# A session is best imagined as a short phone call with the database: you dial
# in, ask your questions, then hang up. Borrowing one connection from the pool
# for the length of one request, then giving it back.
#
# The word "yield" below is what makes the cleanup automatic. The code runs
# down to `yield`, pauses there and lets the request do its work, and once the
# reply has been sent it wakes back up and finishes the `finally` part. So the
# connection is ALWAYS handed back — even if the request crashed partway.
#
# Notice it never saves anything by itself. Each route decides when to save
# (you'll see `session.commit()` in routes/approvals.py). That way, if
# something goes wrong halfway, nothing half-finished gets written down.
def get_db_session() -> Generator[Session, None, None]:
    session = get_session_factory()()
    try:
        yield session          # <-- the request does its work at this point
    finally:
        session.close()        # always runs: hang up the call


# The security check at the front desk.
#
# WORTH KNOWING IF YOU ARE NEW: the caller's identity arrives as plain text
# labels attached to the request (called "headers"). There is no password or
# cryptographic signature here, so in theory anyone could simply claim to be an
# admin. That is only acceptable because another program (an API gateway) is
# expected to sit in front of this one and fill these labels in honestly, after
# doing the real login check. This trade-off is written up in
# docs/threat-model.md. Because of it, this service must never be placed
# directly on the public internet.
def get_current_actor(
    # These three lines say: "read these values from the request's headers".
    # `Annotated[type, Header(alias=...)]` is how FastAPI is told where a value
    # comes from — here the headers, rather than the web address or the body.
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-Id")] = None,
    x_user_id: Annotated[str | None, Header(alias="X-User-Id")] = None,
    x_role: Annotated[str, Header(alias="X-Role")] = "agent",   # if not stated, assume the
                                                                # least powerful role
) -> Actor:
    # No name badge at all -> error 401, which means "I don't know who you are".
    if not x_tenant_id or not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-Tenant-Id and X-User-Id headers are required",
        )

    role = x_role.strip().lower()          # tidy it up, so " Admin " counts the same as "admin"
    actor = Actor(tenant_id=x_tenant_id, user_id=x_user_id, role=role)
    require_role(actor, ALLOWED_ROLES)     # unrecognised job title gets rejected below
    return actor


# The "are you allowed to do this?" check.
# Used here for the broad check (are you allowed in at all?), and again inside
# individual routes for stricter ones — for example routes/policies.py calls it
# with POLICY_WRITE_ROLES so only leads and admins may change safety rules.
#
# Error 403 means something different from 401: here we DO know who you are,
# you simply aren't permitted to do this particular thing.
def require_role(actor: Actor, allowed_roles: Iterable[str]) -> None:
    if actor.role not in set(allowed_roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="actor role is not allowed for this action",
        )


# The link between the two halves of this system.
#
# Asking an AI model a question is slow — often several seconds. Far too slow
# to keep someone staring at a spinning web page. So instead of doing it right
# away, the API drops a note into a waiting list (a "queue", kept in a fast
# in-memory storage system called Redis) and replies immediately.
#
# Meanwhile a separate background program (apps/worker/) sits watching that
# waiting list, picks the note up, and does the slow AI work on its own time.
# That program is the one logging in with the "service" role mentioned above.
# The queue itself is built in apps/worker/supportops_worker/queues.py.
#
# The import sitting INSIDE the function is deliberate, not a mistake. Putting
# it here means the API only loads the worker's code at the moment it is truly
# needed — so the API can still start up fine even if the worker package or
# Redis is unavailable.
@lru_cache
def get_ai_analysis_queue() -> Any:
    settings = get_settings()
    from supportops_worker.queues import build_analysis_queue

    return build_analysis_queue(settings.redis_url)
