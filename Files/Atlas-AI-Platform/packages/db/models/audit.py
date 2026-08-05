"""Audit-event ORM model.

Audit rows provide an append-only trail for important state transitions such as
prompt activation. The JSON columns store before/after snapshots without needing
a separate table per audited domain object.
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from packages.db.base import Base


class AuditEvent(Base):
    """Single recorded action against a subject in the platform.

    SQLAlchemy note: `Mapped[UUID | None]` is a type hint for a nullable mapped
    column. `mapped_column(...)` supplies database details such as type, foreign
    key, nullability, and defaults.
    """

    __tablename__ = "audit_events"
    __table_args__ = (
        # `__table_args__` is where SQLAlchemy keeps table-level constraints and
        # indexes, similar to EF Core Fluent API configuration.
        CheckConstraint(
            "actor_type in ('user','agent','system','worker','provider','optimizer')",
            name="actor_type",
        ),
        Index("idx_audit_events_tenant_created", "tenant_id", "created_at"),
        Index("idx_audit_events_subject", "subject_type", "subject_id"),
        Index("idx_audit_events_actor", "actor_user_id", "created_at"),
        Index(
            "idx_audit_events_trace_id",
            "trace_id",
            postgresql_where=text("trace_id is not null"),
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    tenant_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=True,
    )
    actor_user_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    actor_type: Mapped[str] = mapped_column(Text, nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    subject_type: Mapped[str] = mapped_column(Text, nullable=False)
    subject_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    request_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    trace_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    before_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    after_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
