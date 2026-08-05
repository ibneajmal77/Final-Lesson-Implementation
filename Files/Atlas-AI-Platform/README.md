# Atlas AI Platform

Phase 00 foundation, Phase 01 LLM Gateway, and Phase 02 Prompt System implementation for the Atlas AI Platform.

## Detailed Documentation

The implementation is tied to the detailed blueprint and learning guides in the sibling documentation folder:

```text
..\Atlas-AI-Platform-Detailed-Documentation\00-Atlas-Documentation-Map.md
..\Atlas-AI-Platform-Detailed-Documentation\01-Atlas-Technical-Master-Blueprint.md
..\Atlas-AI-Platform-Detailed-Documentation\learning-phases\phase-00-engineering-foundation.md
..\Atlas-AI-Platform-Detailed-Documentation\learning-phases\phase-01-llm-gateway.md
..\Atlas-AI-Platform-Detailed-Documentation\learning-phases\phase-02-prompt-system.md
```

Read the phase guides before changing the scaffold, gateway, or prompt system so the code stays aligned with the architecture, done criteria, and learning path.

For a project-local reading path aimed at experienced .NET developers who are
new to Python, see:

```text
docs\python-for-dotnet-reviewers.md
```

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
copy .env.example .env
```

Important local settings:

```text
ATLAS_API_PREFIX=/api/v1
ATLAS_DATABASE_URL=postgresql+psycopg://atlas:atlas@localhost:55432/atlas?connect_timeout=3
ATLAS_REDIS_URL=redis://localhost:6379/0
```

## Local Infrastructure

```bash
docker compose -f infra/docker-compose.yml up -d
```

## Phase Gates

Tenant-aware AI features are blocked until tenant membership and RBAC are implemented. Before adding tenant-scoped model routes, RAG collections, eval runs, MCP tools, or agent actions, use `packages.auth.gates.enforce_tenant_rbac_gate(...)` and implement the `roles`, `permissions`, and `tenant_memberships` tables from the database schema spec.

## LLM Gateway

Phase 01 routes every model request through `packages.model_gateway`. The local bootstrap seeds mock providers and global routes for `chat`, `classification`, `rag_answer`, `embedding`, and `llm_judge`, so tests do not require a real provider key.

Internal endpoints:

```text
POST /api/v1/model-gateway/chat
POST /api/v1/model-gateway/embed
GET /api/v1/model-gateway/routes
GET /api/v1/ai-runs/{ai_run_id}
```

Managed OpenAI-compatible calls are disabled by default. To run an opt-in smoke test later, set:

```text
ATLAS_MODEL_GATEWAY_ENABLE_MANAGED_PROVIDER=true
ATLAS_OPENAI_COMPATIBLE_API_KEY=...
```

## Prompt System

Phase 02 stores prompt templates, immutable prompt versions, prompt test cases, and prompt activation audit records. Activation is refused until a version is approved, every activation writes `audit_events`, and the database enforces one active version per template.

Internal endpoints:

```text
POST /api/v1/prompts
GET /api/v1/prompts
GET /api/v1/prompts/{prompt_id}
POST /api/v1/prompts/{prompt_id}/versions
POST /api/v1/prompts/{prompt_id}/versions/{version_id}/approve
POST /api/v1/prompts/{prompt_id}/versions/{version_id}/activate
POST /api/v1/prompts/{prompt_id}/versions/{version_id}/deactivate
POST /api/v1/prompts/{prompt_id}/versions/{version_id}/retire
POST /api/v1/prompts/{prompt_id}/render
POST /api/v1/prompts/{prompt_id}/tests
GET /api/v1/prompts/{prompt_id}/tests
POST /api/v1/prompts/{prompt_id}/test
```

Prompt test runs go through the LLM Gateway and use the mock provider by default, so CI can prove rendering, variable validation, gateway execution, and `ai_runs.prompt_version_id` attribution without a provider key.

## Database Migrations

```bash
alembic upgrade head
alembic current
```

The migrations create Phase 00 identity tables, Phase 01 model gateway tables, and Phase 02 `audit_events`, prompt tables, and the hardened `ai_runs.prompt_version_id -> prompt_versions(id)` foreign key. Live migration verification requires the local PostgreSQL container or another reachable PostgreSQL database at `ATLAS_DATABASE_URL`.

## Run API

```bash
uvicorn apps.api.main:app --reload
```

Health checks use `ATLAS_API_PREFIX`, which defaults to `/api/v1`:

```text
GET /api/v1/health
GET /api/v1/health/live
GET /api/v1/health/ready
```

`/health` remains available as a legacy local alias.

## Logging

Application logs are emitted as JSON with stable fields such as `timestamp`, `level`, `logger`, `message`, `request_id`, and optional `extra`. This satisfies the Phase 00 structured logging requirement and prepares the project for Phase 18 observability.

## Run Worker

```bash
python -m apps.worker.main
```

## Run Tests And Quality Checks

```bash
python -m ruff check .
python -m mypy apps packages
python -m pytest
```

## Graphify Knowledge Graph

Graphify can be installed as the `graphifyy` Python package, which provides the `graphify` command. This project also has a local project-scoped Codex skill. The local Codex files are ignored by git unless you intentionally decide to version them:

```text
.codex\skills\graphify\SKILL.md
.codex\hooks.json
AGENTS.md
.graphifyignore
```

Use this from the project root when you want to build or refresh the local knowledge graph:

```bash
graphify .
graphify update .
graphify query "how is the API wired?"
```

If the CLI is not on PATH, verify the local install first:

```bash
python -m pip install graphifyy
python -m pip show graphifyy
Get-Command graphify
```

If `graphify` is not on PATH after installation, add the Python Scripts directory reported by your Python install to PATH.
