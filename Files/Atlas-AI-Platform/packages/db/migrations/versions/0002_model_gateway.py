"""create model gateway tables

Revision ID: 0002_model_gateway
Revises: 0001_initial_foundation
Create Date: 2026-07-31 00:00:00.000000
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_model_gateway"
down_revision: str | None = "0001_initial_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Phase 01 adds provider configuration, route policy, AI run ledgers, and
    # cost records. Migrations are explicit so schema review does not depend on
    # reading runtime ORM code.
    op.create_table(
        "model_providers",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("provider_type", sa.Text(), nullable=False),
        sa.Column("base_url", sa.Text(), nullable=True),
        sa.Column(
            "capabilities_json",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "data_policy_json",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("status", sa.Text(), server_default=sa.text("'active'"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "provider_type in ("
            "'openai_compatible','anthropic_compatible','azure_openai',"
            "'local_vllm','local_tgi','mock'"
            ")",
            name="provider_type",
        ),
        sa.CheckConstraint("status in ('active','disabled')", name="status"),
        sa.PrimaryKeyConstraint("id", name="pk_model_providers"),
        sa.UniqueConstraint("name", name="uq_model_providers_name"),
    )

    op.create_table(
        "model_routes",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("use_case", sa.Text(), nullable=False),
        sa.Column("route_key", sa.Text(), nullable=False),
        sa.Column("provider_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("model_name", sa.Text(), nullable=False),
        sa.Column("priority", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("max_input_tokens", sa.Integer(), nullable=False),
        sa.Column("max_output_tokens", sa.Integer(), nullable=False),
        sa.Column("temperature", sa.Numeric(4, 3), nullable=True),
        sa.Column("timeout_seconds", sa.Integer(), nullable=False),
        sa.Column("fallback_route_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "prompt_caching_enabled",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("cacheable_prefix_min_tokens", sa.Integer(), nullable=True),
        sa.Column(
            "semantic_cache_enabled",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("batch_enabled", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("max_batch_items", sa.Integer(), nullable=True),
        sa.Column("embedding_dimension", sa.Integer(), nullable=True),
        sa.Column("async_only", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column(
            "cost_estimate_required",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("max_cost_usd", sa.Numeric(12, 6), nullable=True),
        sa.Column(
            "route_config_json",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "reasoning_enabled",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("reasoning_effort", sa.Text(), nullable=True),
        sa.Column("reasoning_budget_tokens", sa.Integer(), nullable=True),
        sa.Column(
            "restricted_data_allowed",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("status", sa.Text(), server_default=sa.text("'active'"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("priority > 0", name="priority_positive"),
        sa.CheckConstraint("max_input_tokens > 0", name="max_input_tokens_positive"),
        sa.CheckConstraint(
            "max_output_tokens > 0 or use_case in ("
            "'embedding','image_generation','video_generation','audio_generation'"
            ")",
            name="max_output_tokens_positive_unless_generator",
        ),
        sa.CheckConstraint(
            "cacheable_prefix_min_tokens is null or cacheable_prefix_min_tokens > 0",
            name="cacheable_prefix_min_tokens_positive",
        ),
        sa.CheckConstraint(
            "max_batch_items is null or max_batch_items > 0",
            name="max_batch_items_positive",
        ),
        sa.CheckConstraint(
            "embedding_dimension is null or embedding_dimension > 0",
            name="embedding_dimension_positive",
        ),
        sa.CheckConstraint(
            "max_cost_usd is null or max_cost_usd >= 0",
            name="max_cost_usd_nonnegative",
        ),
        sa.CheckConstraint("status in ('active','disabled')", name="status"),
        sa.ForeignKeyConstraint(
            ["fallback_route_id"],
            ["model_routes.id"],
            name="fk_model_routes_fallback_route_id_model_routes",
        ),
        sa.ForeignKeyConstraint(
            ["provider_id"],
            ["model_providers.id"],
            name="fk_model_routes_provider_id_model_providers",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_model_routes_tenant_id_tenants",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_model_routes"),
    )
    op.create_index("idx_model_routes_use_case_status", "model_routes", ["use_case", "status"])
    op.create_index("idx_model_routes_tenant_use_case", "model_routes", ["tenant_id", "use_case"])
    op.create_index("idx_model_routes_route_key", "model_routes", ["tenant_id", "route_key"])
    op.create_index(
        "uq_model_routes_global_route_key",
        "model_routes",
        ["route_key"],
        unique=True,
        postgresql_where=sa.text("tenant_id is null"),
    )
    # PostgreSQL partial unique indexes model separate uniqueness rules for
    # global routes and tenant-scoped routes.
    op.create_index(
        "uq_model_routes_tenant_route_key",
        "model_routes",
        ["tenant_id", "route_key"],
        unique=True,
        postgresql_where=sa.text("tenant_id is not null"),
    )

    op.create_table(
        "ai_runs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("agent_run_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("use_case", sa.Text(), nullable=False),
        sa.Column("provider_name", sa.Text(), nullable=False),
        sa.Column("model_name", sa.Text(), nullable=False),
        sa.Column("model_route_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("prompt_version_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("request_hash", sa.Text(), nullable=False),
        sa.Column("input_preview", sa.Text(), nullable=True),
        sa.Column("output_preview", sa.Text(), nullable=True),
        sa.Column("request_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("response_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("status", sa.Text(), server_default=sa.text("'queued'"), nullable=False),
        sa.Column("error_code", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("output_tokens", sa.Integer(), nullable=True),
        sa.Column("reasoning_output_tokens", sa.Integer(), nullable=True),
        sa.Column("cache_creation_input_tokens", sa.Integer(), nullable=True),
        sa.Column("cache_read_input_tokens", sa.Integer(), nullable=True),
        sa.Column("estimated_cost_usd", sa.Numeric(12, 6), nullable=True),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("time_to_first_chunk_ms", sa.Integer(), nullable=True),
        sa.Column("trace_id", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "status in ('queued','running','succeeded','failed','cancelled','blocked')",
            name="status",
        ),
        sa.ForeignKeyConstraint(
            ["model_route_id"],
            ["model_routes.id"],
            name="fk_ai_runs_model_route_id_model_routes",
        ),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_ai_runs_tenant_id_tenants"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_ai_runs_user_id_users"),
        sa.PrimaryKeyConstraint("id", name="pk_ai_runs"),
    )
    op.create_index("idx_ai_runs_tenant_created", "ai_runs", ["tenant_id", "created_at"])
    op.create_index("idx_ai_runs_use_case_created", "ai_runs", ["use_case", "created_at"])
    op.create_index("idx_ai_runs_prompt_version", "ai_runs", ["prompt_version_id"])
    op.create_index("idx_ai_runs_model_route", "ai_runs", ["model_route_id"])
    op.create_index("idx_ai_runs_trace_id", "ai_runs", ["trace_id"])

    op.create_table(
        "cost_records",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ai_run_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("batch_job_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("media_generation_job_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("use_case", sa.Text(), nullable=False),
        sa.Column("provider_name", sa.Text(), nullable=False),
        sa.Column("model_name", sa.Text(), nullable=False),
        sa.Column("billing_unit", sa.Text(), nullable=False),
        sa.Column("quantity", sa.Numeric(18, 6), nullable=False),
        sa.Column("unit_cost_usd", sa.Numeric(18, 9), nullable=False),
        sa.Column("estimated_cost_usd", sa.Numeric(12, 6), nullable=False),
        sa.Column("actual_cost_usd", sa.Numeric(12, 6), nullable=True),
        sa.Column("currency", sa.Text(), server_default=sa.text("'USD'"), nullable=False),
        sa.Column("pricing_version", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("quantity >= 0", name="quantity_nonnegative"),
        sa.CheckConstraint("estimated_cost_usd >= 0", name="estimated_cost_usd_nonnegative"),
        sa.CheckConstraint(
            "actual_cost_usd is null or actual_cost_usd >= 0",
            name="actual_cost_usd_nonnegative",
        ),
        sa.ForeignKeyConstraint(
            ["ai_run_id"],
            ["ai_runs.id"],
            name="fk_cost_records_ai_run_id_ai_runs",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_cost_records_tenant_id_tenants",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_cost_records"),
    )
    op.create_index("idx_cost_records_tenant_created", "cost_records", ["tenant_id", "created_at"])
    op.create_index("idx_cost_records_ai_run", "cost_records", ["ai_run_id"])
    op.create_index("idx_cost_records_use_case_created", "cost_records", ["use_case", "created_at"])


def downgrade() -> None:
    # Drop dependent tables/indexes before the tables they reference.
    op.drop_index("idx_cost_records_use_case_created", table_name="cost_records")
    op.drop_index("idx_cost_records_ai_run", table_name="cost_records")
    op.drop_index("idx_cost_records_tenant_created", table_name="cost_records")
    op.drop_table("cost_records")

    op.drop_index("idx_ai_runs_trace_id", table_name="ai_runs")
    op.drop_index("idx_ai_runs_model_route", table_name="ai_runs")
    op.drop_index("idx_ai_runs_prompt_version", table_name="ai_runs")
    op.drop_index("idx_ai_runs_use_case_created", table_name="ai_runs")
    op.drop_index("idx_ai_runs_tenant_created", table_name="ai_runs")
    op.drop_table("ai_runs")

    op.drop_index("uq_model_routes_tenant_route_key", table_name="model_routes")
    op.drop_index("uq_model_routes_global_route_key", table_name="model_routes")
    op.drop_index("idx_model_routes_route_key", table_name="model_routes")
    op.drop_index("idx_model_routes_tenant_use_case", table_name="model_routes")
    op.drop_index("idx_model_routes_use_case_status", table_name="model_routes")
    op.drop_table("model_routes")
    op.drop_table("model_providers")
