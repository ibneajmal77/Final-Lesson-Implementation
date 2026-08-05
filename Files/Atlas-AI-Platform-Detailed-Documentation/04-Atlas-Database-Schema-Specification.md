# Atlas AI Platform - Database Schema Specification

## 1. Purpose

This document converts the blueprint database design into implementation-ready schema specifications.

It defines:

- Naming conventions.
- ID strategy.
- Timestamp conventions.
- Enums.
- Tables.
- Columns.
- Foreign keys.
- Indexes.
- Unique constraints.
- Migration order.
- Deletion/reindexing rules.

Recommended database:

```text
PostgreSQL 15+
pgvector extension for MVP vector search
Qdrant optional later behind VectorStore interface
```

## 2. Global Schema Conventions

### 2.1 ID Types

Use UUID primary keys.

```sql
id uuid primary key default gen_random_uuid()
```

Reason:

- Safe for distributed creation.
- Harder to guess than integer ids.
- Works across services later.

### 2.2 Timestamps

Common fields:

```sql
created_at timestamptz not null default now()
updated_at timestamptz not null default now()
deleted_at timestamptz null
```

Rules:

- `created_at` is immutable.
- `updated_at` changes on updates.
- `deleted_at` is used for soft delete where audit matters.

### 2.3 Tenant Ownership

Tenant-owned tables include:

```sql
tenant_id uuid not null references tenants(id)
```

Index rule:

```sql
create index idx_<table>_tenant_id on <table>(tenant_id);
```

Access rule:

Every application query for tenant-owned data must filter by `tenant_id`.

### 2.3.1 Nullable Global/Tenant Uniqueness

Some tables allow `tenant_id` to be null for global records and non-null for tenant overrides. PostgreSQL regular `unique(tenant_id, key)` allows multiple rows where `tenant_id is null`, so do not use it alone for global/tenant uniqueness.

Use one of these patterns:

```sql
-- Preferred explicit pattern.
create unique index uq_<table>_global_<key>
on <table>(<key>)
where tenant_id is null;

create unique index uq_<table>_tenant_<key>
on <table>(tenant_id, <key>)
where tenant_id is not null;
```

Or, on PostgreSQL 15+ where appropriate:

```sql
unique nulls not distinct (tenant_id, <key>)
```

Atlas should prefer partial unique indexes when global and tenant records have different operational meaning.

### 2.4 JSON Fields

Use `jsonb` for flexible metadata.

Rules:

- Use `jsonb` for metadata, provider raw responses, schemas, and trace objects.
- Do not use `jsonb` as a replacement for important searchable columns.
- Add GIN indexes only for fields that are actually queried.

### 2.5 Text Search

For hybrid search, use PostgreSQL full-text search with a generated `tsvector` column or maintained search vector.

Example:

```sql
search_vector tsvector
```

Index:

```sql
create index idx_document_chunks_search_vector on document_chunks using gin(search_vector);
```

### 2.6 Vector Storage

If using pgvector for the MVP:

```sql
embedding vector(1536) not null
```

Dimension must match the indexed embedding model. pgvector ANN indexes require a fixed vector dimension on the indexed column. If Atlas supports Matryoshka embeddings, multiple embedding dimensions, or quantized variants, do not mix them in one ANN index. Use one of these patterns:

- Separate physical table per indexed dimension, for example `chunk_embeddings_1536`, `chunk_embeddings_768`, and `chunk_embeddings_256`.
- Separate fixed-dimension columns per supported dimension, with one ANN index per column.
- External vector store collections per model, dimension, quantization, and index version.

The generic `chunk_embeddings` logical schema can still record `embedding_dimension` and `embedding_dimension_used`, but the concrete pgvector migration must create a fixed-dimension indexed column.

## 3. Enums

Use PostgreSQL enums or text columns with check constraints. For flexibility during learning, text + check constraints are easier to migrate.

### 3.1 Common Status Enums

```sql
document_status: uploaded, queued, processing, processed, failed, archived, deleted
job_status: queued, running, succeeded, failed, cancelled, retrying
prompt_version_status: draft, testing, approved, active, retired
ai_run_status: queued, running, succeeded, failed, cancelled, blocked
agent_run_status: created, planning, waiting_for_approval, running_tool, verifying, completed, failed, cancelled, blocked, expired
approval_status: pending, approved, rejected, expired, cancelled
tool_risk_level: low, medium, high, critical
safety_status: allowed, blocked, needs_review, redacted, failed
eval_run_status: queued, running, completed, failed, cancelled
media_generation_status: queued, running, completed, failed, blocked, cancelled
```

## 4. Migration Order

### 4.1 MVP Migration Order

```text
001_enable_extensions
002_create_identity_tables
003_create_audit_and_observability_base
004_create_prompt_and_model_tables
005_create_document_tables
006_create_ingestion_jobs
007_create_vector_tables
008_create_conversation_and_rag_tables
009_create_eval_tables
010_create_feedback_tables
```

### 4.2 Agent And Safety Migration Order

```text
011_create_tool_tables
012_create_agent_tables
013_create_memory_tables
014_create_safety_tables
015_create_approval_tables
016_create_mcp_tables
017_create_multi_agent_tables
```

### 4.3 Advanced AI Migration Order

```text
018_create_model_adaptation_tables
019_create_model_serving_tables
020_create_cache_and_batch_tables
021_create_media_generation_tables
022_create_voice_tables
023_create_governance_tables
024_create_index_versioning_tables
```

Migration rule:

```text
Never create a table that references a table which has not been created in an earlier migration.
```

### 4.4 Deferred Foreign Key Migrations

Some records need to link across domains that are created later. These must be implemented as nullable UUID columns first, then upgraded with explicit later `ALTER TABLE ... ADD CONSTRAINT` migrations.

| Deferred Constraint | Create Column In | Add FK After | Migration |
|---|---|---|---|
| `ai_runs.prompt_version_id -> prompt_versions(id)` | Phase 01 `ai_runs` migration | Phase 02 `prompt_versions` migration | `0005_add_ai_runs_prompt_version_fk` |
| `ai_runs.conversation_id -> conversations(id)` | `004_create_prompt_and_model_tables` | `008_create_conversation_and_rag_tables` | `008a_add_ai_runs_conversation_fk` |
| `ai_runs.agent_run_id -> agent_runs(id)` | `004_create_prompt_and_model_tables` | `012_create_agent_tables` | `012a_add_ai_runs_agent_run_fk` |
| `tool_calls.approval_id -> human_approvals(id)` | `011_create_tool_tables` | `015_create_approval_tables` | `015a_add_tool_calls_approval_fk` |
| `chunk_embeddings.index_version_id -> vector_index_versions(id)` | `007_create_vector_tables` | `024_create_index_versioning_tables` | `024a_add_chunk_embeddings_index_version_fk` |

Before the deferred FK is added, the column is a soft reference. Application code may write it only after the referenced table exists, and tests must prove the final FK migration succeeds on a clean database.

## 5. Identity Tables

### 5.1 tenants

| Column | Type | Null | Default | Notes |
|---|---|---|---|---|
| id | uuid | no | gen_random_uuid() | primary key |
| name | text | no | none | display name |
| slug | text | no | none | unique URL-safe slug |
| status | text | no | active | active, suspended, deleted |
| plan_name | text | yes | null | free/pro/team/enterprise |
| settings_json | jsonb | no | '{}' | tenant config |
| created_at | timestamptz | no | now() | created time |
| updated_at | timestamptz | no | now() | updated time |
| deleted_at | timestamptz | yes | null | soft delete |

Constraints:

```sql
unique(slug)
check (status in ('active','suspended','deleted'))
```

Indexes:

```sql
idx_tenants_status(status)
```

### 5.2 users

| Column | Type | Null | Default | Notes |
|---|---|---|---|---|
| id | uuid | no | gen_random_uuid() | primary key |
| email | citext | no | none | login email |
| name | text | no | none | display name |
| status | text | no | active | active, disabled, deleted |
| password_hash | text | yes | null | local auth only |
| external_auth_subject | text | yes | null | OIDC subject later |
| last_login_at | timestamptz | yes | null | last login |
| created_at | timestamptz | no | now() | created time |
| updated_at | timestamptz | no | now() | updated time |

Constraints:

```sql
unique(email)
check (status in ('active','disabled','deleted'))
```

### 5.3 roles, permissions, memberships

`roles`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | null for system role |
| name | text | no | role name |
| description | text | yes | details |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

Unique indexes:

```sql
create unique index uq_roles_global_name
on roles(name)
where tenant_id is null;

create unique index uq_roles_tenant_name
on roles(tenant_id, name)
where tenant_id is not null;
```

`permissions`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| code | text | no | permission code |
| description | text | yes | details |

Constraints:

```sql
unique(code)
```

`role_permissions`:

| Column | Type | Null | Notes |
|---|---|---|---|
| role_id | uuid | no | references roles(id) |
| permission_id | uuid | no | references permissions(id) |

Constraints:

```sql
primary key(role_id, permission_id)
```

`tenant_memberships`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| user_id | uuid | no | references users(id) |
| role_id | uuid | no | references roles(id) |
| status | text | no | active, invited, disabled |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

Constraints:

```sql
unique(tenant_id, user_id)
check (status in ('active','invited','disabled'))
```

## 6. Prompt And Model Tables

### 6.1 prompt_templates

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | nullable for global prompts |
| name | text | no | prompt name |
| use_case | text | no | shared route use case; ratified values are chat, classification, rag_answer, embedding, llm_judge; reserved values require a matching route before activation |
| description | text | yes | purpose |
| owner_user_id | uuid | yes | references users(id) |
| status | text | no | active, archived |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

Constraints:

```sql
check (status in ('active','archived'))
```

Unique indexes:

```sql
create unique index uq_prompt_templates_id_tenant
on prompt_templates(id, tenant_id);

create unique index uq_prompt_templates_global_name
on prompt_templates(name)
where tenant_id is null;

create unique index uq_prompt_templates_tenant_name
on prompt_templates(tenant_id, name)
where tenant_id is not null;
```

Indexes:

```sql
idx_prompt_templates_tenant_use_case(tenant_id, use_case, status)
```

### 6.2 prompt_versions

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| prompt_template_id | uuid | no | references prompt_templates(id) |
| version_number | int | no | incremental version |
| system_prompt | text | no | stable instructions |
| user_template | text | no | template with variables |
| developer_notes | text | yes | rationale |
| input_variables_json | jsonb | no | variable schema |
| output_schema_json | jsonb | yes | required output schema |
| model_defaults_json | jsonb | no | temperature, max tokens, route |
| status | text | no | draft/testing/approved/active/retired |
| created_by_user_id | uuid | yes | references users(id) |
| created_by_actor_type | text | no | user, system, optimizer |
| created_at | timestamptz | no | created time |

Constraints:

```sql
unique(prompt_template_id, version_number)
check (status in ('draft','testing','approved','active','retired'))
check (version_number > 0)
check (created_by_actor_type in ('user','system','optimizer'))
```

Indexes:

```sql
idx_prompt_versions_template_status(prompt_template_id, status)

create unique index uq_prompt_versions_one_active
on prompt_versions(prompt_template_id)
where status = 'active';
```

### 6.2a prompt_test_cases

This table fills the Phase 02 gap between the blueprint, which requires prompt test cases, and the original implementation-ready schema, which only listed templates and versions.

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | must match the template tenant_id; null for global-template cases |
| prompt_template_id | uuid | no | references prompt_templates(id) |
| name | text | no | case name, unique within the template |
| case_type | text | no | happy_path, edge_case, adversarial, format, regression |
| input_json | jsonb | no | variable map used to render |
| expected_behavior | text | no | human-readable expectation |
| expected_output_json | jsonb | yes | machine-checkable shape; enforced in Phase 03 |
| status | text | no | active, archived |
| created_by_user_id | uuid | yes | references users(id) |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

Constraints:

```sql
foreign key (prompt_template_id, tenant_id)
  references prompt_templates(id, tenant_id)
check (case_type in ('happy_path','edge_case','adversarial','format','regression'))
check (status in ('active','archived'))
```

The composite foreign key uses PostgreSQL's default `MATCH SIMPLE` behavior, so global cases with `tenant_id is null` still need an application-level check that they attach only to global templates.

Indexes:

```sql
create unique index uq_prompt_test_cases_template_name
on prompt_test_cases(prompt_template_id, name);

create index idx_prompt_test_cases_template_status
on prompt_test_cases(prompt_template_id, status);

create index idx_prompt_test_cases_tenant_id
on prompt_test_cases(tenant_id);
```

### 6.3 model_providers and model_routes

`model_providers`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| name | text | no | stable provider key, e.g. openai, anthropic, local_vllm |
| provider_type | text | no | openai_compatible, anthropic_compatible, azure_openai, local_vllm, local_tgi, mock |
| base_url | text | yes | provider endpoint |
| capabilities_json | jsonb | no | provider capability matrix |
| data_policy_json | jsonb | no | retention/training/region policy |
| status | text | no | active, disabled |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

Constraints:

```sql
unique(name) -- `name` is the provider key used by bootstrap `provider_key` values
```

`model_routes`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | nullable for global route |
| use_case | text | no | shared route use case; ratified values are chat, classification, rag_answer, embedding, llm_judge; later phases add media and voice use cases |
| route_key | text | no | stable config key, e.g. `rag_answer_primary` |
| provider_id | uuid | no | references model_providers(id) |
| model_name | text | no | model id |
| priority | int | no | lower number first |
| max_input_tokens | int | no | request cap |
| max_output_tokens | int | no | output cap |
| temperature | numeric(4,3) | yes | nullable for provider default |
| timeout_seconds | int | no | model timeout |
| fallback_route_id | uuid | yes | references model_routes(id); config loaders may resolve from `fallback_route_key` |
| prompt_caching_enabled | boolean | no | false |
| cacheable_prefix_min_tokens | int | yes | provider-specific minimum useful cached prefix size |
| semantic_cache_enabled | boolean | no | false |
| batch_enabled | boolean | no | false |
| max_batch_items | int | yes | max provider batch size for route |
| embedding_dimension | int | yes | required for embedding routes |
| async_only | boolean | no | false, true for long media/video/batch jobs |
| cost_estimate_required | boolean | no | true for expensive or async routes |
| max_cost_usd | numeric(12,6) | yes | per-request or per-job route budget |
| route_config_json | jsonb | no | provider-specific safe config not promoted to first-class columns |
| reasoning_enabled | boolean | no | false |
| reasoning_effort | text | yes | low/medium/high |
| reasoning_budget_tokens | int | yes | max reasoning tokens |
| restricted_data_allowed | boolean | no | false |
| status | text | no | active, disabled |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

Constraints and unique indexes:

```sql
create unique index uq_model_routes_global_route_key
on model_routes(route_key)
where tenant_id is null;

create unique index uq_model_routes_tenant_route_key
on model_routes(tenant_id, route_key)
where tenant_id is not null;

check (priority > 0)
check (max_input_tokens > 0)
check (max_output_tokens > 0 or use_case in ('embedding','image_generation','video_generation','audio_generation'))
check (cacheable_prefix_min_tokens is null or cacheable_prefix_min_tokens > 0)
check (max_batch_items is null or max_batch_items > 0)
check (embedding_dimension is null or embedding_dimension > 0)
check (max_cost_usd is null or max_cost_usd >= 0)
```

Indexes:

```sql
idx_model_routes_use_case_status(use_case, status)
idx_model_routes_tenant_use_case(tenant_id, use_case)
idx_model_routes_route_key(tenant_id, route_key)
```

Route config rule:

```text
Use first-class columns for routing decisions that the gateway filters on frequently.
Use route_config_json only for provider-specific optional settings.
Use fallback_route_id in the database. Bootstrap YAML/JSON may use fallback_route_key, then the loader resolves it to fallback_route_id.
```

## 7. AI Run And Observability Tables

### 7.1 ai_runs

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| user_id | uuid | yes | references users(id) |
| conversation_id | uuid | yes | soft reference until `008a_add_ai_runs_conversation_fk` |
| agent_run_id | uuid | yes | soft reference until `012a_add_ai_runs_agent_run_fk` |
| use_case | text | no | route use case |
| provider_name | text | no | provider used |
| model_name | text | no | model used |
| model_route_id | uuid | yes | references model_routes(id) |
| prompt_version_id | uuid | yes | soft reference until `0005_add_ai_runs_prompt_version_fk`; then references prompt_versions(id) |
| request_hash | text | no | normalized hash |
| input_preview | text | yes | redacted preview |
| output_preview | text | yes | redacted preview |
| request_json | jsonb | yes | redacted full request if allowed |
| response_json | jsonb | yes | redacted full response if allowed |
| status | text | no | queued/running/succeeded/failed/cancelled/blocked |
| error_code | text | yes | stable error code |
| error_message | text | yes | safe message |
| input_tokens | int | yes | normal input tokens |
| output_tokens | int | yes | output tokens |
| reasoning_output_tokens | int | yes | current OTel-aligned reasoning token name |
| cache_creation_input_tokens | int | yes | provider cache write tokens |
| cache_read_input_tokens | int | yes | provider cache read tokens |
| estimated_cost_usd | numeric(12,6) | yes | calculated cost |
| latency_ms | int | yes | total model latency |
| time_to_first_chunk_ms | int | yes | streaming latency |
| trace_id | text | yes | distributed trace id |
| created_at | timestamptz | no | created time |

Indexes:

```sql
idx_ai_runs_tenant_created(tenant_id, created_at desc)
idx_ai_runs_use_case_created(use_case, created_at desc)
idx_ai_runs_prompt_version(prompt_version_id)
idx_ai_runs_model_route(model_route_id)
idx_ai_runs_trace_id(trace_id)
```


### 7.2 conversations and conversation_messages

`conversations`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| user_id | uuid | yes | references users(id), creator/current owner |
| title | text | yes | user-visible title |
| channel | text | no | web, api, voice, eval, agent |
| status | text | no | active, archived, deleted |
| metadata_json | jsonb | no | '{}' |
| last_message_at | timestamptz | yes | latest message timestamp |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |
| deleted_at | timestamptz | yes | soft delete |

Constraints:

```sql
check (channel in ('web','api','voice','eval','agent'))
check (status in ('active','archived','deleted'))
```

Indexes:

```sql
idx_conversations_tenant_updated(tenant_id, updated_at desc)
idx_conversations_user_updated(user_id, updated_at desc)
idx_conversations_tenant_status(tenant_id, status)
```

`conversation_messages`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| conversation_id | uuid | no | references conversations(id) |
| role | text | no | user, assistant, system, tool, approval |
| content_text | text | yes | redacted visible text |
| content_json | jsonb | yes | structured/multimodal content |
| ai_run_id | uuid | yes | references ai_runs(id) |
| tool_call_id | uuid | yes | soft reference until tool_calls exists |
| approval_id | uuid | yes | soft reference until human_approvals exists |
| sequence_number | int | no | order inside conversation |
| token_count | int | yes | token estimate/count |
| metadata_json | jsonb | no | '{}' |
| created_at | timestamptz | no | created time |
| deleted_at | timestamptz | yes | soft delete |

Constraints:

```sql
unique(conversation_id, sequence_number)
check (role in ('user','assistant','system','tool','approval'))
check (content_text is not null or content_json is not null)
```

Indexes:

```sql
idx_conversation_messages_conversation_sequence(conversation_id, sequence_number)
idx_conversation_messages_tenant_created(tenant_id, created_at desc)
idx_conversation_messages_ai_run(ai_run_id)
```

### 7.3 audit_events, cost_records, and background_jobs

`audit_events`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | nullable for platform/global events |
| actor_user_id | uuid | yes | references users(id) |
| actor_type | text | no | user, agent, system, worker, provider, optimizer |
| action | text | no | stable action name |
| subject_type | text | no | model_route, prompt_template, prompt_version, document, tool_call, agent_run, etc. |
| subject_id | uuid | yes | polymorphic subject id |
| request_id | text | yes | API request id |
| trace_id | text | yes | distributed trace id |
| idempotency_key | text | yes | side-effect dedupe key |
| before_json | jsonb | yes | redacted previous state |
| after_json | jsonb | yes | redacted new state |
| metadata_json | jsonb | no | '{}' |
| created_at | timestamptz | no | created time |

Indexes:

```sql
idx_audit_events_tenant_created(tenant_id, created_at desc)
idx_audit_events_subject(subject_type, subject_id)
idx_audit_events_actor(actor_user_id, created_at desc)
idx_audit_events_trace_id(trace_id) where trace_id is not null
```

`cost_records`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| ai_run_id | uuid | yes | references ai_runs(id) |
| batch_job_id | uuid | yes | soft reference until batch_model_jobs exists |
| media_generation_job_id | uuid | yes | soft reference until media_generation_jobs exists |
| use_case | text | no | route/use case |
| provider_name | text | no | provider key/name |
| model_name | text | no | model id |
| billing_unit | text | no | input_token, output_token, reasoning_token, cache_write_token, cache_read_token, image, audio_second, video_second, request |
| quantity | numeric(18,6) | no | billable quantity |
| unit_cost_usd | numeric(18,9) | no | cost per unit |
| estimated_cost_usd | numeric(12,6) | no | estimated line cost |
| actual_cost_usd | numeric(12,6) | yes | actual provider cost when known |
| currency | text | no | USD |
| pricing_version | text | yes | pricing sheet/model version |
| created_at | timestamptz | no | created time |

Constraints:

```sql
check (quantity >= 0)
check (estimated_cost_usd >= 0)
check (actual_cost_usd is null or actual_cost_usd >= 0)
```

Indexes:

```sql
idx_cost_records_tenant_created(tenant_id, created_at desc)
idx_cost_records_ai_run(ai_run_id)
idx_cost_records_use_case_created(use_case, created_at desc)
```

`background_jobs`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | nullable for platform jobs |
| queue_name | text | no | ingestion, embeddings, evals, media, voice, maintenance |
| job_type | text | no | stable job type |
| subject_type | text | yes | document, eval_run, media_job, index_version, etc. |
| subject_id | uuid | yes | polymorphic subject id |
| status | text | no | queued, running, succeeded, failed, cancelled, retrying |
| priority | int | no | lower number first |
| attempts | int | no | retry count |
| max_attempts | int | no | retry limit |
| input_json | jsonb | no | redacted job input |
| result_json | jsonb | yes | redacted job result |
| error_code | text | yes | stable error code |
| error_message | text | yes | safe error |
| idempotency_key | text | yes | duplicate prevention |
| scheduled_at | timestamptz | no | earliest start |
| started_at | timestamptz | yes | start time |
| finished_at | timestamptz | yes | finish time |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

Unique indexes and constraints:

```sql
create unique index uq_background_jobs_global_idempotency
on background_jobs(idempotency_key)
where tenant_id is null and idempotency_key is not null;

create unique index uq_background_jobs_tenant_idempotency
on background_jobs(tenant_id, idempotency_key)
where tenant_id is not null and idempotency_key is not null;

check (status in ('queued','running','succeeded','failed','cancelled','retrying'))
check (attempts >= 0)
check (max_attempts > 0)
```

Indexes:

```sql
idx_background_jobs_queue_status(queue_name, status, scheduled_at)
idx_background_jobs_tenant_created(tenant_id, created_at desc)
idx_background_jobs_subject(subject_type, subject_id)
```

## 8. Document And RAG Tables

### 8.1 knowledge_collections

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| name | text | no | collection name |
| description | text | yes | details |
| visibility | text | no | private, tenant, restricted |
| metadata_json | jsonb | no | '{}' |
| knowledge_index_version | int | no | 1 |
| created_by_user_id | uuid | yes | references users(id) |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |
| deleted_at | timestamptz | yes | soft delete |

Constraints:

```sql
unique(tenant_id, name)
check (visibility in ('private','tenant','restricted'))
```

### 8.2 documents

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| collection_id | uuid | no | references knowledge_collections(id) |
| title | text | no | title |
| source_type | text | no | upload, url, ticket, email |
| source_uri | text | yes | source location |
| file_object_key | text | yes | object storage key |
| mime_type | text | no | file type |
| status | text | no | document_status |
| checksum | text | no | content hash |
| metadata_json | jsonb | no | '{}' |
| created_by_user_id | uuid | yes | references users(id) |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |
| deleted_at | timestamptz | yes | soft delete |

Indexes:

```sql
idx_documents_tenant_collection(tenant_id, collection_id)
idx_documents_tenant_status(tenant_id, status)
idx_documents_checksum(checksum)
```

### 8.3 document_versions, pages, chunks, embeddings

`document_versions`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| document_id | uuid | no | references documents(id) |
| version_number | int | no | document version |
| file_object_key | text | yes | object key |
| checksum | text | no | content hash |
| parser_name | text | yes | parser |
| parser_version | text | yes | parser version |
| status | text | no | queued/processing/processed/failed |
| created_at | timestamptz | no | created time |

Constraints:

```sql
unique(document_id, version_number)
```

`document_pages`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| document_id | uuid | no | references documents(id) |
| document_version_id | uuid | no | references document_versions(id) |
| page_number | int | no | page number |
| text | text | yes | extracted text |
| layout_json | jsonb | yes | layout/bounding boxes |
| ocr_confidence | numeric(5,4) | yes | OCR confidence |
| image_object_key | text | yes | rendered page image |
| created_at | timestamptz | no | created time |

Constraints:

```sql
unique(document_version_id, page_number)
```

`document_chunks`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| document_id | uuid | no | references documents(id) |
| document_version_id | uuid | no | references document_versions(id) |
| parent_chunk_id | uuid | yes | references document_chunks(id) |
| chunk_level | text | no | child, parent, section, document |
| page_start | int | yes | citation start |
| page_end | int | yes | citation end |
| chunk_index | int | no | order within version |
| text | text | no | source text |
| normalized_text | text | yes | cleaned text |
| contextual_text | text | yes | generated retrieval helper, not citation truth |
| token_count | int | no | token count |
| search_vector | tsvector | yes | keyword search |
| metadata_json | jsonb | no | '{}' |
| content_hash | text | no | chunk hash |
| active | boolean | no | true |
| created_at | timestamptz | no | created time |
| deleted_at | timestamptz | yes | soft delete |

Indexes:

```sql
idx_chunks_tenant_document(tenant_id, document_id)
idx_chunks_version_active(document_version_id, active)
idx_chunks_parent(parent_chunk_id)
idx_chunks_search_vector using gin(search_vector)
```

`chunk_embeddings`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| chunk_id | uuid | no | references document_chunks(id) |
| embedding_model | text | no | model name |
| embedding_dimension | int | no | full dimension |
| embedding_dimension_used | int | no | stored/search dimension |
| embedding | vector(1536) | yes | MVP pgvector column; use fixed-dimension table/column per index dimension |
| vector_store_name | text | yes | qdrant/pgvector |
| vector_point_id | text | yes | external vector id |
| quantization | text | yes | float32, int8, binary, pq |
| content_hash | text | no | source chunk hash |
| index_version_id | uuid | yes | soft reference until `024a_add_chunk_embeddings_index_version_fk` |
| created_at | timestamptz | no | created time |

Constraints:

```sql
unique(chunk_id, embedding_model, embedding_dimension_used, quantization)
```

Indexes:

```sql
idx_chunk_embeddings_tenant_model(tenant_id, embedding_model)
idx_chunk_embeddings_chunk(chunk_id)
```

### 8.4 ingestion_jobs

`ingestion_jobs`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| background_job_id | uuid | yes | references background_jobs(id) |
| document_id | uuid | no | references documents(id) |
| document_version_id | uuid | yes | references document_versions(id) |
| requested_by_user_id | uuid | yes | references users(id) |
| job_type | text | no | ingest, reingest, delete, reindex |
| status | text | no | queued, running, succeeded, failed, cancelled, retrying |
| parser_name | text | yes | parser selected |
| parser_version | text | yes | parser version |
| chunker_name | text | yes | chunker selected |
| chunker_version | text | yes | chunker version |
| input_object_key | text | yes | source object key |
| output_summary_json | jsonb | yes | pages/chunks/tokens summary |
| error_code | text | yes | stable error code |
| error_message | text | yes | safe error |
| idempotency_key | text | yes | duplicate prevention |
| started_at | timestamptz | yes | start time |
| finished_at | timestamptz | yes | finish time |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

Constraints:

```sql
unique(tenant_id, idempotency_key) where idempotency_key is not null
check (job_type in ('ingest','reingest','delete','reindex'))
check (status in ('queued','running','succeeded','failed','cancelled','retrying'))
```

Indexes:

```sql
idx_ingestion_jobs_tenant_created(tenant_id, created_at desc)
idx_ingestion_jobs_document(document_id)
idx_ingestion_jobs_status(status)
idx_ingestion_jobs_background(background_job_id)
```
### 8.5 RAG tables

`rag_queries`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| conversation_id | uuid | yes | references conversations(id) |
| user_id | uuid | yes | references users(id) |
| query_text | text | no | original query |
| rewritten_query | text | yes | retrieval rewrite |
| retrieval_strategy | text | no | vector_only, hybrid_rerank, hyde, etc. |
| collection_ids | uuid[] | no | selected collections |
| filters_json | jsonb | no | filters |
| knowledge_index_version | int | no | source index version |
| created_at | timestamptz | no | created time |

`rag_retrieval_results`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| rag_query_id | uuid | no | references rag_queries(id) |
| chunk_id | uuid | no | references document_chunks(id) |
| rank_initial | int | yes | initial rank |
| rank_final | int | yes | final rank |
| score_initial | numeric(10,6) | yes | initial score |
| score_final | numeric(10,6) | yes | final/rerank score |
| retriever_name | text | no | retriever |
| reranker_name | text | yes | reranker |
| included_in_context | boolean | no | false |
| created_at | timestamptz | no | created time |

Indexes:

```sql
idx_rag_results_query_rank(rag_query_id, rank_final)
idx_rag_results_chunk(chunk_id)
```

`rag_answers`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| rag_query_id | uuid | no | references rag_queries(id) |
| ai_run_id | uuid | yes | references ai_runs(id) |
| answer_text | text | no | final answer |
| answer_json | jsonb | yes | structured answer |
| confidence_label | text | yes | low, medium, high |
| citation_count | int | no | 0 |
| groundedness_score | numeric(5,4) | yes | optional score |
| created_at | timestamptz | no | created time |

`answer_citations`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| rag_answer_id | uuid | no | references rag_answers(id) |
| chunk_id | uuid | no | references document_chunks(id) |
| document_id | uuid | no | references documents(id) |
| page_start | int | yes | start page |
| page_end | int | yes | end page |
| quote_or_summary | text | yes | short support text |
| support_type | text | no | supports_claim, partial_support, background, conflict |
| created_at | timestamptz | no | created time |



### 8.6 feedback

`feedback`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| user_id | uuid | yes | references users(id) |
| conversation_id | uuid | yes | references conversations(id) |
| conversation_message_id | uuid | yes | references conversation_messages(id) |
| rag_answer_id | uuid | yes | references rag_answers(id) |
| ai_run_id | uuid | yes | references ai_runs(id) |
| tool_call_id | uuid | yes | soft reference until tool_calls exists |
| feedback_type | text | no | rating, correction, report, thumbs |
| rating | int | yes | 1-5 star rating |
| vote | text | yes | up, down |
| issue_type | text | yes | incorrect_answer, bad_citation, unsafe, slow, irrelevant, formatting, other |
| comment | text | yes | user/reviewer comment |
| correction_json | jsonb | yes | expected answer/citation/tool correction |
| tags | text[] | no | '{}' |
| review_status | text | no | new, triaged, accepted, rejected, converted_to_eval |
| created_at | timestamptz | no | created time |
| reviewed_at | timestamptz | yes | review time |

Constraints:

```sql
check (feedback_type in ('rating','correction','report','thumbs'))
check (rating is null or rating between 1 and 5)
check (vote in ('up','down') or vote is null)
check (review_status in ('new','triaged','accepted','rejected','converted_to_eval'))
check (rag_answer_id is not null or ai_run_id is not null or conversation_message_id is not null or tool_call_id is not null)
```

Indexes:

```sql
idx_feedback_tenant_created(tenant_id, created_at desc)
idx_feedback_ai_run(ai_run_id)
idx_feedback_rag_answer(rag_answer_id)
idx_feedback_issue_type(issue_type)
idx_feedback_review_status(review_status)
```

## 9. Tool, Agent, MCP, And Approval Tables

### 9.1 tool_definitions

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | nullable for global tools |
| name | text | no | stable tool name |
| description | text | no | tool description |
| tool_type | text | no | read_only, write_action, external_api, internal_action, human_handoff, mcp |
| input_schema_json | jsonb | no | JSON Schema |
| output_schema_json | jsonb | no | JSON Schema |
| risk_level | text | no | low, medium, high, critical |
| requires_approval | boolean | no | false |
| required_permissions | text[] | no | required permission codes |
| timeout_seconds | int | no | execution timeout |
| status | text | no | active, disabled, pending_review |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

Unique indexes and constraints:

```sql
create unique index uq_tool_definitions_global_name
on tool_definitions(name)
where tenant_id is null;

create unique index uq_tool_definitions_tenant_name
on tool_definitions(tenant_id, name)
where tenant_id is not null;

check (risk_level in ('low','medium','high','critical'))
```

### 9.2 agent_definitions, runs, steps

`agent_definitions`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| name | text | no | agent name |
| description | text | yes | purpose |
| allowed_tool_ids | uuid[] | no | tool allowlist |
| allowed_collection_ids | uuid[] | yes | knowledge scope |
| max_steps | int | no | step limit |
| max_cost_usd | numeric(12,6) | yes | run cost limit |
| requires_approval_for_writes | boolean | no | true |
| status | text | no | active, disabled |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

`agent_runs`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| agent_definition_id | uuid | no | references agent_definitions(id) |
| conversation_id | uuid | yes | references conversations(id) |
| user_id | uuid | no | initiating user |
| task_text | text | no | user task |
| execution_context_json | jsonb | no | scoped permissions/tools/budgets |
| status | text | no | agent_run_status |
| risk_level | text | no | low, medium, high, critical |
| final_result | text | yes | final output |
| error_code | text | yes | stable error |
| error_message | text | yes | safe error |
| started_at | timestamptz | yes | start time |
| finished_at | timestamptz | yes | end time |
| created_at | timestamptz | no | created time |

Indexes:

```sql
idx_agent_runs_tenant_created(tenant_id, created_at desc)
idx_agent_runs_status(status)
```

`agent_steps`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| agent_run_id | uuid | no | references agent_runs(id) |
| step_number | int | no | sequence number |
| step_type | text | no | classify, plan, tool, verify, final |
| ai_run_id | uuid | yes | references ai_runs(id) |
| input_json | jsonb | no | redacted input |
| output_json | jsonb | yes | redacted output |
| status | text | no | queued/running/succeeded/failed/blocked |
| started_at | timestamptz | yes | start time |
| finished_at | timestamptz | yes | end time |
| created_at | timestamptz | no | created time |

Constraints:

```sql
unique(agent_run_id, step_number)
```

### 9.3 agent_handoffs

`agent_handoffs`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| source_agent_run_id | uuid | no | references agent_runs(id) |
| target_agent_definition_id | uuid | yes | references agent_definitions(id) |
| target_agent_run_id | uuid | yes | references agent_runs(id) |
| handoff_reason | text | no | capability_gap, approval_needed, escalation, specialization |
| handoff_context_json | jsonb | no | minimized context passed to next agent |
| allowed_tool_ids | uuid[] | yes | scoped tool set for target |
| allowed_collection_ids | uuid[] | yes | scoped knowledge set for target |
| status | text | no | proposed, accepted, rejected, completed, failed |
| created_at | timestamptz | no | created time |
| completed_at | timestamptz | yes | completion time |

Constraints:

```sql
check (handoff_reason in ('capability_gap','approval_needed','escalation','specialization'))
check (status in ('proposed','accepted','rejected','completed','failed'))
```

Indexes:

```sql
idx_agent_handoffs_tenant_created(tenant_id, created_at desc)
idx_agent_handoffs_source(source_agent_run_id)
idx_agent_handoffs_target(target_agent_run_id)
```
### 9.4 tool_calls and human_approvals

`tool_calls`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| agent_run_id | uuid | yes | references agent_runs(id) |
| conversation_id | uuid | yes | references conversations(id) |
| tool_definition_id | uuid | no | references tool_definitions(id) |
| requested_by | text | no | user, agent, system |
| input_json | jsonb | no | validated input |
| output_json | jsonb | yes | result |
| status | text | no | requested, waiting_approval, running, succeeded, failed, blocked |
| risk_level | text | no | low, medium, high, critical |
| dry_run | boolean | no | false |
| idempotency_key | text | yes | side-effect safety |
| approval_id | uuid | yes | soft reference until `015a_add_tool_calls_approval_fk` |
| error_code | text | yes | stable error |
| error_message | text | yes | safe error |
| started_at | timestamptz | yes | start time |
| finished_at | timestamptz | yes | end time |
| created_at | timestamptz | no | created time |

Indexes and constraints:

```sql
unique(tenant_id, idempotency_key) where idempotency_key is not null
idx_tool_calls_agent_run(agent_run_id)
idx_tool_calls_tenant_created(tenant_id, created_at desc)
```

`human_approvals`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| requested_by_user_id | uuid | yes | references users(id) |
| reviewer_user_id | uuid | yes | references users(id) |
| subject_type | text | no | tool_call, agent_run, model_route, media_job |
| subject_id | uuid | no | polymorphic subject id |
| approval_status | text | no | pending, approved, rejected, expired, cancelled |
| risk_summary | text | no | risk explanation |
| request_json | jsonb | no | action details |
| decision_reason | text | yes | reviewer note |
| expires_at | timestamptz | yes | approval deadline |
| created_at | timestamptz | no | created time |
| decided_at | timestamptz | yes | decision time |

### 9.5 MCP tables

`mcp_servers`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | nullable for global server |
| name | text | no | server name |
| description | text | yes | purpose |
| transport_type | text | no | stdio, streamable_http, remote_gateway |
| protocol_version | text | no | e.g. 2026-07-28 when adopted |
| connection_config_ref | text | no | secret/config reference |
| allowed_scopes | text[] | no | allowed external scopes |
| cache_ttl_ms | int | yes | tools/list/resource cache ttl |
| cache_scope | text | yes | user, tenant, global |
| status | text | no | pending_review, active, disabled |
| version | text | yes | server version |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

`mcp_tool_mappings`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| mcp_server_id | uuid | no | references mcp_servers(id) |
| tool_definition_id | uuid | no | references tool_definitions(id) |
| mcp_tool_name | text | no | external MCP tool name |
| schema_snapshot_json | jsonb | no | original schema snapshot |
| normalized_schema_json | jsonb | no | Atlas normalized schema |
| schema_hash | text | no | detects changes |
| risk_level | text | no | low, medium, high, critical |
| enabled | boolean | no | false |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

Constraints:

```sql
unique(tenant_id, mcp_server_id, mcp_tool_name)
```


### 9.6 memory_items

`memory_items`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| user_id | uuid | yes | references users(id), null for tenant/shared memory |
| conversation_id | uuid | yes | references conversations(id) |
| agent_run_id | uuid | yes | references agent_runs(id) |
| memory_type | text | no | session_summary, preference, fact, task_state, tool_result_summary |
| scope | text | no | user, conversation, tenant, agent |
| content_text | text | no | redacted memory text |
| content_json | jsonb | yes | structured memory |
| embedding_id | uuid | yes | soft reference to chunk_embeddings or memory embedding table |
| source_type | text | no | user_message, assistant_summary, tool_result, human_review |
| source_id | uuid | yes | source row id |
| confidence | numeric(5,4) | yes | confidence score |
| review_status | text | no | draft, approved, rejected, expired |
| retention_expires_at | timestamptz | yes | retention deadline |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |
| deleted_at | timestamptz | yes | soft delete |

Constraints:

```sql
check (memory_type in ('session_summary','preference','fact','task_state','tool_result_summary'))
check (scope in ('user','conversation','tenant','agent'))
check (review_status in ('draft','approved','rejected','expired'))
```

Indexes:

```sql
idx_memory_items_tenant_user(tenant_id, user_id)
idx_memory_items_conversation(conversation_id)
idx_memory_items_agent_run(agent_run_id)
idx_memory_items_scope_type(scope, memory_type)
idx_memory_items_retention(retention_expires_at) where retention_expires_at is not null
```

### 9.7 safety_policies and safety_checks

`safety_policies`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | nullable for global policy |
| policy_key | text | no | stable policy key |
| version | int | no | policy version |
| policy_type | text | no | prompt_injection, pii, tool_risk, media, voice, memory, output |
| config_json | jsonb | no | thresholds/rules/classifiers |
| status | text | no | draft, testing, active, retired |
| owner_user_id | uuid | yes | references users(id) |
| created_at | timestamptz | no | created time |
| activated_at | timestamptz | yes | activation time |

Unique indexes:

```sql
create unique index uq_safety_policies_global_key_version
on safety_policies(policy_key, version)
where tenant_id is null;

create unique index uq_safety_policies_tenant_key_version
on safety_policies(tenant_id, policy_key, version)
where tenant_id is not null;
```

Constraints:

```sql
check (policy_type in ('prompt_injection','pii','tool_risk','media','voice','memory','output'))
check (status in ('draft','testing','active','retired'))
```

`safety_checks`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| safety_policy_id | uuid | yes | references safety_policies(id) |
| ai_run_id | uuid | yes | references ai_runs(id) |
| agent_run_id | uuid | yes | references agent_runs(id) |
| tool_call_id | uuid | yes | references tool_calls(id) |
| conversation_message_id | uuid | yes | references conversation_messages(id) |
| check_stage | text | no | input, retrieved_context, tool_arguments, tool_output, model_output, memory_write, media_prompt, media_output |
| input_hash | text | yes | hash of checked content |
| decision | text | no | allowed, blocked, needs_review, redacted, failed |
| score | numeric(5,4) | yes | classifier/judge score |
| findings_json | jsonb | no | policy findings |
| redaction_json | jsonb | yes | redaction details |
| created_at | timestamptz | no | created time |

Constraints:

```sql
check (check_stage in ('input','retrieved_context','tool_arguments','tool_output','model_output','memory_write','media_prompt','media_output'))
check (decision in ('allowed','blocked','needs_review','redacted','failed'))
check (ai_run_id is not null or agent_run_id is not null or tool_call_id is not null or conversation_message_id is not null)
```

Indexes:

```sql
idx_safety_checks_tenant_created(tenant_id, created_at desc)
idx_safety_checks_policy(safety_policy_id)
idx_safety_checks_ai_run(ai_run_id)
idx_safety_checks_agent_run(agent_run_id)
idx_safety_checks_tool_call(tool_call_id)
idx_safety_checks_decision(decision)
```

## 10. Evaluation Tables

### 10.1 eval_datasets and eval_cases

`eval_datasets`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| name | text | no | dataset name |
| use_case | text | no | rag, structured_output, agent, safety, media, voice |
| version | int | no | version number |
| purpose | text | no | eval, training, red_team, synthetic |
| status | text | no | draft, approved, retired |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

`eval_cases`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| dataset_id | uuid | no | references eval_datasets(id) |
| case_id_external | text | yes | stable import id |
| input_json | jsonb | no | test input |
| expected_output_json | jsonb | yes | expected output |
| reference_context_json | jsonb | yes | reference docs/context |
| tags | text[] | no | tags |
| difficulty | text | no | easy, medium, hard |
| source_type | text | no | human, production_failure, synthetic, red_team |
| review_status | text | no | draft, reviewed, approved |
| split | text | yes | train, validation, test |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

Constraints:

```sql
unique(dataset_id, case_id_external)
check (split in ('train','validation','test') or split is null)
```

### 10.2 eval_runs and eval_results

`eval_runs`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| dataset_id | uuid | no | references eval_datasets(id) |
| run_name | text | no | display name |
| run_type | text | no | prompt, rag, agent, safety, media, voice |
| candidate_config_json | jsonb | no | candidate config |
| baseline_config_json | jsonb | yes | baseline config |
| threshold_config_json | jsonb | no | pass/fail thresholds |
| status | text | no | queued/running/completed/failed/cancelled |
| started_at | timestamptz | yes | start time |
| finished_at | timestamptz | yes | finish time |
| created_at | timestamptz | no | created time |

`eval_results`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| eval_run_id | uuid | no | references eval_runs(id) |
| eval_case_id | uuid | no | references eval_cases(id) |
| ai_run_id | uuid | yes | references ai_runs(id) |
| output_json | jsonb | yes | output being scored |
| scores_json | jsonb | no | scorer scores |
| pass_fail | text | no | pass, fail, error |
| error_message | text | yes | error |
| reviewer_override_json | jsonb | yes | human review override |
| created_at | timestamptz | no | created time |

Constraints:

```sql
unique(eval_run_id, eval_case_id)
```

## 11. Cache, Batch, Index Versioning Tables

### 11.1 semantic_cache_entries

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| use_case | text | no | classification, query_rewrite, rag_answer |
| cache_key_hash | text | no | exact/structured key |
| query_embedding_id | uuid | yes | optional embedding reference |
| input_summary | text | no | redacted summary |
| output_json | jsonb | no | cached output |
| source_version_hash | text | yes | doc/prompt/model/index versions |
| permission_scope_hash | text | no | prevents permission leaks |
| similarity_threshold | numeric(5,4) | yes | calibrated threshold |
| prompt_version_id | uuid | yes | references prompt_versions(id) |
| model_name | text | yes | model used |
| safety_status | text | no | allowed, blocked, needs_review |
| expires_at | timestamptz | no | cache expiry |
| created_at | timestamptz | no | created time |

Constraints:

```sql
unique(tenant_id, use_case, cache_key_hash, source_version_hash, permission_scope_hash)
```

### 11.2 batch_model_jobs and items

`batch_model_jobs`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| use_case | text | no | embeddings, eval, classification |
| provider_name | text | no | provider |
| model_name | text | no | model |
| provider_batch_id | text | yes | external id |
| status | text | no | queued, submitted, running, completed, failed, cancelled |
| item_count | int | no | total items |
| estimated_cost_usd | numeric(12,6) | yes | estimate |
| actual_cost_usd | numeric(12,6) | yes | actual |
| created_at | timestamptz | no | created time |
| completed_at | timestamptz | yes | done time |

`batch_model_job_items`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| batch_job_id | uuid | no | references batch_model_jobs(id) |
| item_index | int | no | position |
| input_json | jsonb | no | redacted input |
| output_json | jsonb | yes | output |
| status | text | no | queued, succeeded, failed |
| error_message | text | yes | safe error |
| ai_run_id | uuid | yes | references ai_runs(id) |

Constraints:

```sql
unique(batch_job_id, item_index)
```

### 11.3 vector_index_versions and knowledge_index_versions

`vector_index_versions`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | nullable for global index config |
| vector_store_name | text | no | pgvector, qdrant |
| embedding_model | text | no | model |
| dimension | int | no | dimension used |
| index_type | text | no | hnsw, ivf, flat |
| index_params_json | jsonb | no | m, ef_search, lists, probes |
| quantization | text | yes | float32, int8, binary |
| status | text | no | building, active, retired, failed |
| created_at | timestamptz | no | created time |

`knowledge_index_versions`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| collection_id | uuid | no | references knowledge_collections(id) |
| version_number | int | no | index version |
| vector_index_version_id | uuid | yes | references vector_index_versions(id) |
| status | text | no | building, active, retired, failed |
| created_at | timestamptz | no | created time |

## 12. Media, Voice, And Governance Tables

### 12.1 media_generation_jobs and media_assets

`media_generation_jobs`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| user_id | uuid | no | references users(id) |
| media_type | text | no | image, video, audio, music |
| input_prompt | text | no | generation prompt, redacted if needed |
| input_media_object_key | text | yes | source image/video/audio |
| provider_name | text | no | provider |
| model_name | text | no | model |
| status | text | no | queued/running/completed/failed/blocked/cancelled |
| safety_status | text | no | allowed/blocked/needs_review |
| cost_estimate_usd | numeric(12,6) | yes | estimate |
| actual_cost_usd | numeric(12,6) | yes | actual |
| idempotency_key | text | yes | duplicate prevention |
| error_message | text | yes | safe error |
| created_at | timestamptz | no | created time |
| completed_at | timestamptz | yes | completed time |

`media_assets`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| generation_job_id | uuid | yes | references media_generation_jobs(id) |
| asset_type | text | no | image, video, audio |
| object_key | text | no | object storage key |
| mime_type | text | no | MIME type |
| width | int | yes | image/video width |
| height | int | yes | image/video height |
| duration_ms | int | yes | audio/video duration |
| metadata_json | jsonb | no | media metadata |
| provenance_json | jsonb | no | provider/model/prompt lineage |
| created_at | timestamptz | no | created time |

`media_safety_checks`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| generation_job_id | uuid | yes | references media_generation_jobs(id) |
| media_asset_id | uuid | yes | references media_assets(id) |
| check_stage | text | no | prompt_precheck, provider_filter, output_moderation, human_review |
| policy_name | text | no | media safety policy name |
| policy_version | text | no | policy version/hash |
| decision | text | no | allowed, blocked, needs_review, redacted |
| scores_json | jsonb | no | classifier/provider scores |
| findings_json | jsonb | no | detected risks and entities |
| reviewer_user_id | uuid | yes | references users(id) |
| created_at | timestamptz | no | created time |

Constraints:

```sql
check (check_stage in ('prompt_precheck','provider_filter','output_moderation','human_review'))
check (decision in ('allowed','blocked','needs_review','redacted'))
check (generation_job_id is not null or media_asset_id is not null)
```

Indexes:

```sql
idx_media_safety_checks_tenant_created(tenant_id, created_at desc)
idx_media_safety_checks_job(generation_job_id)
idx_media_safety_checks_asset(media_asset_id)
idx_media_safety_checks_decision(decision)
```

### 12.2 voice_sessions and transcripts

`voice_sessions`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| user_id | uuid | yes | references users(id) |
| conversation_id | uuid | yes | references conversations(id) |
| mode | text | no | upload, streaming, realtime |
| consent_status | text | no | captured, not_required, missing |
| audio_object_key | text | yes | stored audio key |
| retention_expires_at | timestamptz | yes | retention deadline |
| created_at | timestamptz | no | created time |

`voice_transcript_segments`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references tenants(id) |
| voice_session_id | uuid | no | references voice_sessions(id) |
| speaker_id | text | yes | speaker label |
| start_time_ms | int | no | segment start |
| end_time_ms | int | no | segment end |
| text | text | no | transcript text |
| confidence | numeric(5,4) | yes | STT confidence |
| created_at | timestamptz | no | created time |

### 12.3 governance tables

`system_cards`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | nullable for global system |
| name | text | no | system name |
| version | int | no | card version |
| content_json | jsonb | no | full system card |
| status | text | no | draft, approved, retired |
| owner_user_id | uuid | yes | references users(id) |
| created_at | timestamptz | no | created time |
| approved_at | timestamptz | yes | approval time |

`model_cards`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| model_route_id | uuid | yes | references model_routes(id) |
| model_name | text | no | model |
| provider_name | text | no | provider |
| version | int | no | card version |
| content_json | jsonb | no | model card content |
| status | text | no | draft, approved, retired |
| created_at | timestamptz | no | created time |
| approved_at | timestamptz | yes | approval time |

`risk_register_items`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | nullable for global risk |
| risk_code | text | no | e.g. RISK-001 |
| title | text | no | risk name |
| category | text | no | prompt_injection, tool_misuse, etc. |
| severity | text | no | low, medium, high, critical |
| likelihood | text | no | low, medium, high |
| impact | text | no | business impact |
| owner_user_id | uuid | yes | references users(id) |
| mitigation | text | no | mitigation plan |
| status | text | no | open, mitigated, accepted, closed |
| last_reviewed_at | timestamptz | yes | last review |
| next_review_at | timestamptz | yes | next review |
| created_at | timestamptz | no | created time |

`governance_reviews`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | nullable for global review |
| subject_type | text | no | system_card, model_card, risk_register_item, model_route, safety_policy, mcp_server |
| subject_id | uuid | no | polymorphic subject id |
| review_type | text | no | approval, periodic, incident_followup, pre_launch |
| status | text | no | pending, approved, rejected, changes_requested, expired |
| reviewer_user_id | uuid | yes | references users(id) |
| requested_by_user_id | uuid | yes | references users(id) |
| checklist_json | jsonb | no | review checklist answers |
| evidence_links_json | jsonb | no | traces, evals, runbooks, screenshots, PRs |
| decision_reason | text | yes | reviewer decision notes |
| due_at | timestamptz | yes | review deadline |
| decided_at | timestamptz | yes | decision time |
| created_at | timestamptz | no | created time |
| updated_at | timestamptz | no | updated time |

Constraints:

```sql
check (subject_type in ('system_card','model_card','risk_register_item','model_route','safety_policy','mcp_server'))
check (review_type in ('approval','periodic','incident_followup','pre_launch'))
check (status in ('pending','approved','rejected','changes_requested','expired'))
```

Indexes:

```sql
idx_governance_reviews_tenant_created(tenant_id, created_at desc)
idx_governance_reviews_subject(subject_type, subject_id)
idx_governance_reviews_status_due(status, due_at)
```

`ai_incidents`:

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | tenant or global |
| severity | text | no | sev1, sev2, sev3, sev4 |
| category | text | no | safety, cost, outage, data_leak, tool_misuse |
| summary | text | no | short summary |
| status | text | no | open, investigating, mitigated, closed |
| detected_at | timestamptz | no | detection time |
| resolved_at | timestamptz | yes | resolved time |
| owner_user_id | uuid | yes | incident owner |
| timeline_json | jsonb | no | timeline |
| root_cause | text | yes | final RCA |
| corrective_actions_json | jsonb | no | action list |

## 13. Index Strategy Summary

Every high-volume table needs tenant/time indexes.

Required index patterns:

```sql
idx_<table>_tenant_created(tenant_id, created_at desc)
idx_<table>_tenant_status(tenant_id, status)
idx_<table>_trace_id(trace_id) where trace_id is not null
idx_<child>_<foreign_key>(foreign_key_column)
```

Vector indexes:

```sql
-- pgvector HNSW example for a fixed-dimension MVP column.
-- Do not create this on a generic variable-dimension logical column.
create index idx_chunk_embeddings_1536_embedding_hnsw
on chunk_embeddings using hnsw (embedding vector_cosine_ops);
```

If Atlas later supports multiple indexed dimensions, each dimension needs a separate table, fixed-dimension column, or external vector collection with its own ANN index and `vector_index_versions` row.

Full-text index:

```sql
create index idx_document_chunks_search_vector
on document_chunks using gin(search_vector);
```

JSONB indexes should be added only when queries require them:

```sql
create index idx_documents_metadata_gin
on documents using gin(metadata_json);
```

## 14. Schema Acceptance Criteria

The schema is implementation-ready when:

- All MVP tables have exact columns and types.
- Foreign keys are valid in migration order.
- Tenant-owned tables have tenant indexes.
- Status fields have constraints or enum validation.
- Idempotency keys are unique where side effects exist.
- Vector indexes are created only after extension setup.
- Deletion and retention fields exist where needed.
- Eval/training datasets track purpose, split, and source.
- AI run fields align with current GenAI observability naming.
- Migration tests run against a clean database.
