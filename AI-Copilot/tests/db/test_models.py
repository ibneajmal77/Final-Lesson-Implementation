from sqlalchemy import UniqueConstraint

from supportops_db.models import Base, Tenant, Ticket, User
from supportops_db.session import to_sqlalchemy_url


def test_core_tables_are_registered() -> None:
    assert set(Base.metadata.tables) >= {"tenants", "users", "tickets"}


def test_tenant_table_columns() -> None:
    columns = Tenant.__table__.columns

    assert "id" in columns
    assert "name" in columns
    assert "slug" in columns
    assert "created_at" in columns


def test_user_table_has_tenant_email_unique_constraint() -> None:
    constraints = {
        constraint.name
        for constraint in User.__table__.constraints
        if isinstance(constraint, UniqueConstraint)
    }

    assert "uq_users_tenant_email" in constraints


def test_ticket_table_has_tenant_external_id_unique_constraint() -> None:
    constraints = {
        constraint.name
        for constraint in Ticket.__table__.constraints
        if isinstance(constraint, UniqueConstraint)
    }

    assert "uq_tickets_tenant_external_id" in constraints


def test_database_url_is_converted_for_sqlalchemy_psycopg_driver() -> None:
    url = "postgresql://supportops:supportops@postgres:5432/supportops"

    assert (
        to_sqlalchemy_url(url)
        == "postgresql+psycopg://supportops:supportops@postgres:5432/supportops"
    )


def test_non_postgres_url_is_not_changed() -> None:
    url = "sqlite:///local.db"

    assert to_sqlalchemy_url(url) == url
