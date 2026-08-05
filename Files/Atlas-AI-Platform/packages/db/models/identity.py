"""Foundation identity ORM models.

These are intentionally minimal Phase 00 tables. Full membership and RBAC are
not implemented yet, which is why tenant-aware AI features are guarded elsewhere.
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, Index, Text, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import CITEXT, JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from packages.db.base import Base


class Tenant(Base):
    """Customer/account boundary for tenant-scoped data."""

    __tablename__ = "tenants"
    __table_args__ = (
        CheckConstraint("status in ('active', 'suspended', 'deleted')", name="status"),
        UniqueConstraint("slug", name="uq_tenants_slug"),
        Index("idx_tenants_status", "status"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'active'"))
    plan_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    settings_json: Mapped[dict[str, Any]] = mapped_column(
        # PostgreSQL JSONB stores structured settings without a separate table.
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class User(Base):
    """Platform user record, independent from future tenant membership tables."""

    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("status in ('active', 'disabled', 'deleted')", name="status"),
        UniqueConstraint("email", name="uq_users_email"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    # CITEXT is PostgreSQL's case-insensitive text type, useful for email keys.
    email: Mapped[str] = mapped_column(CITEXT, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'active'"))
    password_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    external_auth_subject: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
