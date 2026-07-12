from collections.abc import Generator
from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated

from fastapi import Header, HTTPException, status
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from supportops_api.settings import get_settings
from supportops_db.session import create_db_engine, create_session_factory


@dataclass(frozen=True)
class Actor:
    tenant_id: str
    user_id: str
    role: str


@lru_cache
def get_engine() -> Engine:
    settings = get_settings()
    return create_db_engine(settings.database_url)


@lru_cache
def get_session_factory():
    return create_session_factory(get_engine())


def get_db_session() -> Generator[Session, None, None]:
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()


def get_current_actor(
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-Id")] = None,
    x_user_id: Annotated[str | None, Header(alias="X-User-Id")] = None,
    x_role: Annotated[str, Header(alias="X-Role")] = "agent",
) -> Actor:
    if not x_tenant_id or not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-Tenant-Id and X-User-Id headers are required",
        )

    return Actor(tenant_id=x_tenant_id, user_id=x_user_id, role=x_role)
