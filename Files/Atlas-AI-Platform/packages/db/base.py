"""SQLAlchemy declarative base and naming conventions.

This is the closest equivalent to the shared EF Core `DbContext` metadata setup:
every ORM model inherits from `Base`, so Alembic can discover tables and create
deterministic constraint names in migrations.
"""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

NAMING_CONVENTION = {
    # Stable names make migrations reviewable and avoid database-generated names
    # that differ between machines or PostgreSQL versions.
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Common base class for all mapped ORM entities."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)
