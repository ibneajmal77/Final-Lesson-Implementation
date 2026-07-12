from pytest import Session
from sqlalchemy import select

from packages.db.support_ops_db.models import Tenant, User


def get_tenant(session: Session, tenant_id: str) ->  Tenant | None:
    return session.scalar(select(Tenant).where(Tenant.id == tenant_id))

def create_tenant(session: Session, *, tenant_id: str, name: str, slug: str) -> Tenant:
    tenant = Tenant(id=tenant_id, name=name, slug=slug)
    session.add(tenant);
    session.flush()
    return tenant

def create_user(
        session: Session,
        *,
        user_id: str,
        tenant_id: str,
        email: str,
        role: str
) ->  User:
    user = User(id=user_id, tenant_id=tenant_id,email=email, role=role)
    session.add(user)
    session.flush()
    return user
