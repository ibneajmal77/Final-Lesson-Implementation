# ============================================================================
# FILE: packages/db/supportops_db/repositories/tenants.py
#
# THINK OF THIS FILE AS: the database queries for companies and their people.
#
# WHAT A "REPOSITORY" IS, AND WHY THE PROJECT USES ONE:
#   Every file in this folder follows the same idea: ALL database queries live
#   here, and nowhere else. Route files, the worker, and the scripts never write
#   a query themselves — they call one of these functions.
#
#   Three things that buys:
#     1. One place to look. Wondering how tickets are fetched? It is in
#        repositories/tickets.py, not scattered across five route handlers.
#     2. Enforceable rules. Because tenant_id is a REQUIRED argument on these
#        functions, it is impossible to write a query that forgets to filter by
#        it — which is the mechanism keeping companies' data apart.
#     3. Testability. Swap these out and the routes can be tested with no
#        database at all.
#
# THE FILES IN THIS FOLDER:
#   tenants.py         - this file: companies and users
#   tickets.py         - customer support requests
#   recommendations.py - what the analysis concluded
#   approvals.py       - human verdicts
#   ai_runs.py         - job sheets for queued analysis
#   cost_events.py     - money and token records
#   policies.py        - company rules for the AI
#   metrics.py, pilot.py - the counting and reporting queries
#
# A NOTE ON WHAT IS MISSING HERE: there is no update and no delete for tenants
# or users. Companies are created by the seeding script and by hand. This is a
# demonstration project, not a full administrative system.
# ============================================================================

from sqlalchemy import select
from sqlalchemy.orm import Session

from supportops_db.models import Tenant, User


# Fetches one company by its ID, or None if there is no such company.
#
# Small function, heavily used: EVERY endpoint in the API calls this first, via
# its _require_tenant helper. It is the check that turns an unrecognised or
# invented tenant header into a clean 404 rather than letting it reach anything
# further in.
#
# `session.scalar(...)` means "run this query and give me the single value" —
# here one Tenant object, or None when nothing matches. The alternative,
# `session.scalars(...)` with an s, returns many; the difference is one letter
# and easy to misread.
def get_tenant(session: Session, tenant_id: str) -> Tenant | None:
    return session.scalar(select(Tenant).where(Tenant.id == tenant_id))


# Creates a company.
#
# Note the `*` after `session`: every argument following it MUST be passed by
# name at the call site. With three strings in a row, that is genuine protection
# — create_tenant(s, "Acme", "acme", "tenant_1") with the arguments shuffled
# would otherwise be accepted silently and store nonsense.
#
# Note also that `tenant_id` is passed IN rather than generated. Everywhere else
# IDs come from the new_id() default in models.py, but the seeding script needs
# a fixed, predictable ID ("tenant_demo") so the documentation and demo page can
# refer to it.
def create_tenant(session: Session, *, tenant_id: str, name: str, slug: str) -> Tenant:
    tenant = Tenant(id=tenant_id, name=name, slug=slug)
    session.add(tenant)      # stage it — nothing has reached the database yet

    # `flush()` sends the INSERT to the database but does NOT commit it. The
    # distinction matters:
    #   - after flush, the row exists inside this transaction, so any values the
    #     database fills in (timestamps, defaults) are now readable
    #   - it is still invisible to everyone else, and a rollback would erase it
    #
    # This is why NONE of the repository functions commit. Committing is the
    # caller's decision, which is what lets a route save several related rows and
    # commit them together as one all-or-nothing unit.
    session.flush()
    return tenant


# Creates a person belonging to a company.
#
# Same shape as create_tenant. `tenant_id` is a foreign key to tenants.id, so
# the database itself will reject a user pointing at a company that does not
# exist — the check is not left to hopeful application code.
#
# Note again what is absent: no password, no password hash. This app does not
# perform logins; it trusts identity headers set by a gateway in front of it.
# See dependencies.py and docs/threat-model.md.
def create_user(
    session: Session,
    *,
    user_id: str,
    tenant_id: str,
    email: str,
    role: str,        # "agent" / "lead" / "admin" / "service" — see dependencies.py
) -> User:
    user = User(id=user_id, tenant_id=tenant_id, email=email, role=role)
    session.add(user)
    session.flush()
    return user
