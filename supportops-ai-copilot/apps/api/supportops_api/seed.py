# ============================================================================
# FILE: apps/api/supportops_api/seed.py
#
# THINK OF THIS FILE AS: the "make the empty app usable" button.
#
# A freshly created database has tables but no rows in them. That is a problem,
# because every endpoint in this app starts by checking "does this company
# exist?" — and on an empty database the answer is always no. So a brand-new
# install rejects every request with "tenant not found", and there is no way in
# through the API itself, since there is no endpoint for creating a company.
#
# This script breaks that deadlock by inserting one demo company and one demo
# user directly, so you can immediately start making requests.
#
# "Seeding" is the usual name for this: planting the minimum starting data a
# system needs before it can grow.
#
# HOW TO RUN IT:
#   python -m supportops_api.seed
#   (or, with Docker:  docker compose exec api python -m supportops_api.seed)
#   It is also called in the setup steps in README.md and docs/stage-16-*.md.
#
# THE VALUES IT CREATES ARE THE ONES YOU SEND AS HEADERS:
#   X-Tenant-Id: tenant_demo
#   X-User-Id:   user_demo_agent
#   X-Role:      agent
#   ...which is exactly what dependencies.py expects on every request, and what
#   the demo web page in apps/web/src/app.js sends.
#
# NOTE THIS IS DEMO DATA, NOT PRODUCTION DATA. The IDs are fixed and publicly
# known, so a real deployment should create its companies properly rather than
# leaving "tenant_demo" in place.
# ============================================================================

from supportops_api.settings import get_settings
from supportops_db.repositories.tenants import create_tenant, create_user, get_tenant
from supportops_db.session import create_db_engine, create_session_factory

# Fixed IDs rather than randomly generated ones, so the documentation, the demo
# web page, and anyone following the README all refer to the same records — and
# so running this script twice can recognise its own earlier work.
DEMO_TENANT_ID = "tenant_demo"
DEMO_USER_ID = "user_demo_agent"


def main() -> None:
    # Builds its own database connection instead of reusing the one from
    # dependencies.py. This runs as a standalone script, not inside a web
    # request, so there is no FastAPI machinery here to hand it a session.
    settings = get_settings()
    engine = create_db_engine(settings.database_url)
    session_factory = create_session_factory(engine)

    with session_factory() as session:      # `with` guarantees the connection is closed
        # Check before creating. This makes the script "idempotent" — safe to
        # run any number of times. Important, because it tends to get run from
        # setup scripts and container startup, where it may fire on every boot.
        # Without this check, the second run would fail with a duplicate-key
        # error and could take a container restart down with it.
        tenant = get_tenant(session, DEMO_TENANT_ID)
        if not tenant:
            create_tenant(
                session,
                tenant_id=DEMO_TENANT_ID,
                name="Demo Tenant",    # the human-readable name
                slug="demo",           # a short URL-safe nickname
            )
            create_user(
                session,
                user_id=DEMO_USER_ID,
                tenant_id=DEMO_TENANT_ID,     # the user belongs to the company just created
                email="agent@example.com",    # example.com is reserved by standard for exactly
                                              # this — it can never be a real address
                role="agent",                 # the least powerful role; see dependencies.py.
                                              # Note it deliberately isn't "admin"
            )
            # One commit for both rows together, so you can never end up with a
            # company that has no users or a user with no company.
            session.commit()
            # `print` rather than the logger, on purpose: this is a command you
            # run by hand, so the feedback belongs on your screen, not in the
            # structured JSON logs meant for machines.
            print("created demo tenant and user")
            return

        print("demo tenant already exists")


# This line means "only run main() when this file is executed directly as a
# script, not when it is imported by another file". Without it, merely importing
# anything from this module would silently write to your database.
if __name__ == "__main__":
    main()
