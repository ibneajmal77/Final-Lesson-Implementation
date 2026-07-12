from support_api.settings import get_settings
from packages.db.support_ops_db.repositories.tenants import create_tenant, create_user, get_tenant
from packages.db.support_ops_db.session import create_db_engine, create_session_factory


DEMO_TENANT_ID = "tenant_demo"
DEMO_USER_ID = "user_demo_agent"


def main() -> None:
    settings = get_settings()
    engine = create_db_engine(settings.database_url)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        tenant = get_tenant(session, DEMO_TENANT_ID)
        if not tenant:
            create_tenant(
                session,
                tenant_id=DEMO_TENANT_ID,
                name="Demo Tenant",
                slug="demo",
            )
            create_user(
                session,
                user_id=DEMO_USER_ID,
                tenant_id=DEMO_TENANT_ID,
                email="agent@example.com",
                role="agent",
            )
            session.commit()
            print("created demo tenant and user")
            return

        print("demo tenant already exists")


if __name__ == "__main__":
    main()
