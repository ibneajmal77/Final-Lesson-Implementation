"""ORM models for provider routing, AI run ledgers, and cost records.

This file maps the Phase 01 gateway schema. SQLAlchemy's `Mapped[...]` and
`mapped_column(...)` are the typed ORM style, roughly equivalent to EF entity
properties plus Fluent API column configuration.

Python notes for .NET reviewers:
- Class attributes become mapped columns because these classes inherit `Base`.
- `list["ModelRoute"]` uses a string forward reference because `ModelRoute` is
  defined later in the same file.
- `Decimal` is used for money/cost fields to avoid floating-point rounding.
"""

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from packages.db.base import Base


class ModelProvider(Base):
    """Configured vendor/runtime that can serve one or more model routes."""

    __tablename__ = "model_providers"
    __table_args__ = (
        CheckConstraint(
            "provider_type in ("
            "'openai_compatible','anthropic_compatible','azure_openai',"
            "'local_vllm','local_tgi','mock'"
            ")",
            name="provider_type",
        ),
        CheckConstraint("status in ('active','disabled')", name="status"),
        UniqueConstraint("name", name="uq_model_providers_name"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    provider_type: Mapped[str] = mapped_column(Text, nullable=False)
    base_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    capabilities_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )
    data_policy_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'active'"))
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

    # Relationships are navigation properties. They do not create columns here;
    # the actual foreign-key columns are declared on `ModelRoute`.
    routes: Mapped[list["ModelRoute"]] = relationship(back_populates="provider")


class ModelRoute(Base):
    """Policy row deciding which provider/model handles a use case."""

    __tablename__ = "model_routes"
    __table_args__ = (
        # Check constraints protect domain invariants in the database, not only
        # in Python service code.
        CheckConstraint("priority > 0", name="priority_positive"),
        CheckConstraint("max_input_tokens > 0", name="max_input_tokens_positive"),
        CheckConstraint(
            "max_output_tokens > 0 or use_case in ("
            "'embedding','image_generation','video_generation','audio_generation'"
            ")",
            name="max_output_tokens_positive_unless_generator",
        ),
        CheckConstraint(
            "cacheable_prefix_min_tokens is null or cacheable_prefix_min_tokens > 0",
            name="cacheable_prefix_min_tokens_positive",
        ),
        CheckConstraint(
            "max_batch_items is null or max_batch_items > 0",
            name="max_batch_items_positive",
        ),
        CheckConstraint(
            "embedding_dimension is null or embedding_dimension > 0",
            name="embedding_dimension_positive",
        ),
        CheckConstraint(
            "max_cost_usd is null or max_cost_usd >= 0",
            name="max_cost_usd_nonnegative",
        ),
        CheckConstraint("status in ('active','disabled')", name="status"),
        Index("idx_model_routes_use_case_status", "use_case", "status"),
        Index("idx_model_routes_tenant_use_case", "tenant_id", "use_case"),
        Index("idx_model_routes_route_key", "tenant_id", "route_key"),
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
    use_case: Mapped[str] = mapped_column(Text, nullable=False)
    route_key: Mapped[str] = mapped_column(Text, nullable=False)
    provider_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("model_providers.id"),
        nullable=False,
    )
    model_name: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("1"))
    max_input_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    max_output_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    temperature: Mapped[Decimal | None] = mapped_column(Numeric(4, 3), nullable=True)
    timeout_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    fallback_route_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("model_routes.id"),
        nullable=True,
    )
    prompt_caching_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    cacheable_prefix_min_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    semantic_cache_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    batch_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    max_batch_items: Mapped[int | None] = mapped_column(Integer, nullable=True)
    embedding_dimension: Mapped[int | None] = mapped_column(Integer, nullable=True)
    async_only: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    cost_estimate_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    max_cost_usd: Mapped[Decimal | None] = mapped_column(Numeric(12, 6), nullable=True)
    route_config_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )
    reasoning_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    reasoning_effort: Mapped[str | None] = mapped_column(Text, nullable=True)
    reasoning_budget_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    restricted_data_allowed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'active'"))
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

    # `relationship(...)` loads related ORM objects, similar to EF navigation
    # properties. The foreign key column is `provider_id` above.
    provider: Mapped[ModelProvider] = relationship(back_populates="routes")
    fallback_route: Mapped["ModelRoute | None"] = relationship(remote_side=[id])


class AIRun(Base):
    """Durable ledger entry for one gateway execution attempt."""

    __tablename__ = "ai_runs"
    __table_args__ = (
        CheckConstraint(
            "status in ('queued','running','succeeded','failed','cancelled','blocked')",
            name="status",
        ),
        Index("idx_ai_runs_tenant_created", "tenant_id", "created_at"),
        Index("idx_ai_runs_use_case_created", "use_case", "created_at"),
        Index("idx_ai_runs_prompt_version", "prompt_version_id"),
        Index("idx_ai_runs_model_route", "model_route_id"),
        Index("idx_ai_runs_trace_id", "trace_id"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    tenant_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=False,
    )
    user_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    conversation_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    agent_run_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    use_case: Mapped[str] = mapped_column(Text, nullable=False)
    provider_name: Mapped[str] = mapped_column(Text, nullable=False)
    model_name: Mapped[str] = mapped_column(Text, nullable=False)
    model_route_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("model_routes.id"),
        nullable=True,
    )
    prompt_version_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    request_hash: Mapped[str] = mapped_column(Text, nullable=False)
    input_preview: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_preview: Mapped[str | None] = mapped_column(Text, nullable=True)
    request_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    response_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'queued'"))
    error_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reasoning_output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cache_creation_input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cache_read_input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estimated_cost_usd: Mapped[Decimal | None] = mapped_column(Numeric(12, 6), nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    time_to_first_chunk_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    trace_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class CostRecord(Base):
    """Line-item cost estimate tied to an AI run or future batch/media job."""

    __tablename__ = "cost_records"
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="quantity_nonnegative"),
        CheckConstraint("estimated_cost_usd >= 0", name="estimated_cost_usd_nonnegative"),
        CheckConstraint(
            "actual_cost_usd is null or actual_cost_usd >= 0",
            name="actual_cost_usd_nonnegative",
        ),
        Index("idx_cost_records_tenant_created", "tenant_id", "created_at"),
        Index("idx_cost_records_ai_run", "ai_run_id"),
        Index("idx_cost_records_use_case_created", "use_case", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    tenant_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=False,
    )
    ai_run_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai_runs.id"),
        nullable=True,
    )
    batch_job_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    media_generation_job_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
    )
    use_case: Mapped[str] = mapped_column(Text, nullable=False)
    provider_name: Mapped[str] = mapped_column(Text, nullable=False)
    model_name: Mapped[str] = mapped_column(Text, nullable=False)
    billing_unit: Mapped[str] = mapped_column(Text, nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    unit_cost_usd: Mapped[Decimal] = mapped_column(Numeric(18, 9), nullable=False)
    estimated_cost_usd: Mapped[Decimal] = mapped_column(Numeric(12, 6), nullable=False)
    actual_cost_usd: Mapped[Decimal | None] = mapped_column(Numeric(12, 6), nullable=True)
    currency: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'USD'"))
    pricing_version: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
