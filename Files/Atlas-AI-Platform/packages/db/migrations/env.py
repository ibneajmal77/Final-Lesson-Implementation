"""Alembic migration environment.

Alembic is SQLAlchemy's migration tool, similar to EF Core migrations. This file
runs whenever `alembic upgrade`, `alembic downgrade`, or autogeneration needs to
know how to connect to the database and which ORM metadata to compare.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from packages.core.config import get_settings
from packages.db import models as _models  # noqa: F401
from packages.db.base import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = get_settings()
# Override the placeholder URL in `alembic.ini` with the same settings object the
# application uses, so migrations and runtime point at the same database.
config.set_main_option("sqlalchemy.url", settings.database_url)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Generate SQL without opening a live database connection."""
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against a live database connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
