# Progress Log

## Stage 1 - API Foundation

Status: complete.

Built:

- Project folder.
- Python dependency files.
- Docker Compose file for future PostgreSQL and Redis services.
- FastAPI application factory.
- Typed settings with environment variables.
- `/health` endpoint.
- `/ready` endpoint.
- pytest tests for health and readiness.
- Ruff configuration.

Verified:

- `python -m pytest -q` passes.
- `python -m ruff check --no-cache .` passes.
- API responds at `http://127.0.0.1:8765/health`.

Environment notes:

- `uv` is not installed locally, so this project currently uses `pip` and `requirements.txt`.
- Creating `.venv` or `venv` folders is blocked in this sandbox, so dependencies were installed
  into the user Python environment.
- Port `8000` is blocked by Windows socket permissions here, so the project uses port `8765`.
- Docker is installed, but Docker Desktop is not currently running.

What you should understand before Stage 2:

- What a FastAPI route is.
- Why `/health` and `/ready` are different.
- Why settings come from environment variables.
- Why tests are written before adding more features.

Next stage:

- Add real PostgreSQL and Redis readiness checks.
- Start Docker Desktop.
- Run `docker compose up -d postgres redis`.
- Make `/ready` check actual database and Redis connections instead of only checking config.

## Stage 1A - Dockerized API

Status: complete.

Built:

- `Dockerfile.api` for the FastAPI service.
- `.dockerignore` to keep local/dev files out of the image.
- `api` service in `docker-compose.yml`.
- Docker environment variables for app, database, Redis, and model provider settings.
- PostgreSQL and Redis are internal Compose services only; their ports are not published to the
  host to avoid local port conflicts.

Run:

```powershell
docker compose up --build
```

Expected API URL:

```text
http://127.0.0.1:8765/health
```

## Stage 2 - Real Dependency Readiness

Status: complete.

Built:

- `supportops_api.checks` module.
- Real PostgreSQL readiness check using `psycopg`.
- Real Redis readiness check using `redis`.
- `/ready` now returns HTTP 200 only when both dependencies respond.
- `/ready` returns HTTP 503 when a required dependency is unavailable.
- Unit tests for ready, database-down, and Redis-down behavior.

Verified:

- `python -m pytest -q` passes.
- `python -m ruff check --no-cache .` passes.
- `docker compose up --build -d` starts API, PostgreSQL, and Redis.
- `http://127.0.0.1:8765/ready` returns:

```json
{
  "status": "ready",
  "checks": {
    "config": true,
    "database": {"ok": true},
    "redis": {"ok": true}
  }
}
```

What you should understand before Stage 3:

- `/health` means the API process is alive.
- `/ready` means the API can actually serve traffic because required dependencies respond.
- In Docker Compose, containers talk to each other by service name, such as `postgres` and `redis`.
- Unit tests should not require external services unless they are integration tests.

Next stage:

- Add SQLAlchemy and Alembic.
- Create the first database tables: tenants, users, and tickets.
- Add migrations so a fresh database can be built repeatably.

## Stage 3 - Database Models and First Migration

Status: complete.

Built:

- SQLAlchemy database package at `packages/db/supportops_db`.
- Shared SQLAlchemy `Base`.
- URL conversion helper for SQLAlchemy's `postgresql+psycopg` driver.
- `Tenant`, `User`, and `Ticket` models.
- Alembic configuration.
- Initial migration: `0001_identity_tickets`.
- Docker image now includes `alembic.ini` and the database package.
- Unit tests for model metadata, uniqueness constraints, migration files, and URL conversion.

First tables:

- `tenants`: customer or business-unit boundary.
- `users`: users scoped to a tenant.
- `tickets`: support tickets scoped to a tenant.

Verified:

- `python -m pytest -q` passes.
- `python -m ruff check --no-cache .` passes.
- `docker compose up --build -d` rebuilds and starts the stack.
- `docker compose exec -T api python -m alembic upgrade head` applies the migration.
- PostgreSQL contains `alembic_version`, `tenants`, `users`, and `tickets`.
- Alembic version is `0001_identity_tickets`.
- `http://127.0.0.1:8765/ready` still returns ready.

What you should understand before Stage 4:

- A SQLAlchemy model describes a table in Python.
- A migration changes the real database schema.
- Alembic records applied migrations in `alembic_version`.
- `tenant_id` is the foundation for future tenant isolation.
- Unique constraints protect business rules at the database level.

Next stage:

- Add ticket API schemas.
- Add repository functions for tenants and tickets.
- Add seed tenant/user creation for local development.
- Build `POST /tickets`, `GET /tickets`, and `GET /tickets/{ticket_id}`.

## Stage 4 - Tenant-Scoped Ticket APIs

Status: complete.

Built:

- Development actor dependency using `X-Tenant-Id`, `X-User-Id`, and `X-Role` headers.
- Database session dependency for API routes.
- Tenant repository functions.
- Ticket repository functions.
- Ticket request and response schemas.
- `POST /tickets`.
- `GET /tickets`.
- `GET /tickets/{ticket_id}`.
- Demo seed command: `python -m supportops_api.seed`.

API behavior:

- Missing tenant/user headers returns HTTP 401.
- Unknown tenant returns HTTP 404.
- Creating a new ticket returns HTTP 201.
- Re-sending the same `external_id` for the same tenant returns the existing ticket with HTTP 200.
- Listing tickets only returns tickets for the current tenant.
- Fetching a ticket through the wrong tenant boundary returns HTTP 404.

Verified:

- `python -m pytest -q` passes with 18 tests.
- `python -m ruff check --no-cache .` passes.
- `docker compose up --build -d` rebuilds and starts the API.
- `docker compose exec -T api python -m supportops_api.seed` creates the demo tenant and user.
- `POST /tickets`, `GET /tickets`, and `GET /tickets/{ticket_id}` work through Docker.

What you should understand before Stage 5:

- API schemas validate request and response shape.
- SQLAlchemy models describe database rows.
- Repository functions keep database queries in one place.
- Tenant filtering must happen in the repository query, not only in UI logic.
- Idempotent create behavior prevents duplicate tickets from retrying the same external event.

Next stage:

- Stage 5 below adds the first non-AI baseline classifier and saved recommendations.

## Stage 5 - Baseline Ticket Classifier

Status: complete.

Built:

- `supportops_domain` package for business-domain logic.
- Deterministic baseline ticket classifier.
- Keyword-based category detection.
- Priority recommendation rules.
- Security-risk escalation detection.
- Order ID and amount extraction.
- Explanation reasons for each recommendation.
- `TicketRecommendation` SQLAlchemy model.
- Alembic migration: `0002_ticket_recs`.
- Recommendation repository functions.
- `POST /tickets/{ticket_id}/baseline-analysis`.
- `GET /tickets/{ticket_id}/recommendations`.
- Unit tests for classifier behavior.
- API tests for saved recommendations and tenant boundaries.

Baseline categories:

- `security`
- `billing`
- `account_access`
- `delivery`
- `technical_issue`
- `other`

API behavior:

- Creating baseline analysis returns HTTP 201.
- Saved analysis includes source, category, priority, escalation flag, confidence, extracted fields,
  and reasons.
- The endpoint does not update the ticket's real priority.
- Listing recommendations only returns recommendations for the current tenant and ticket.
- Analyzing a ticket through the wrong tenant boundary returns HTTP 404.

Verified locally:

- `python -m pytest -q` passes with 26 tests.
- `python -m ruff check --no-cache .` passes.

Verified in Docker:

- `docker compose up --build -d` rebuilds and starts the stack.
- `docker compose exec -T api python -m alembic upgrade head` applies migration
  `0002_ticket_recs`.
- `docker compose exec -T api python -m supportops_api.seed` confirms the demo tenant exists.
- `http://127.0.0.1:8765/ready` returns ready.
- `POST /tickets/{ticket_id}/baseline-analysis` returns a saved recommendation.
- `GET /tickets/{ticket_id}/recommendations` returns the saved recommendation.
- PostgreSQL Alembic version is `0002_ticket_recs`.

What you should understand before Stage 6:

- Why a deterministic baseline is useful before using an LLM.
- Why domain logic should be testable outside the API route.
- Why AI or baseline outputs should be stored with source, confidence, extracted fields, and reasons.
- Why recommendations should not automatically mutate production ticket state.
- How this baseline creates a comparison point for future LLM output.

Next stage:

- Stage 6 below adds the first LLM provider abstraction with a mock provider.

## Stage 6 - Mock LLM Provider Abstraction

Status: complete.

Built:

- `TicketAnalysisProvider` protocol.
- `MockTicketAnalysisProvider`.
- Provider factory using `MODEL_PROVIDER`.
- Structured model-style result with source, model name, prompt version, category, priority,
  escalation flag, confidence, summary, suggested reply, extracted fields, and reasons.
- Alembic migration: `0003_model_outputs`.
- Optional model-output columns on `ticket_recommendations`.
- `POST /tickets/{ticket_id}/ai-analysis`.
- Tests for provider behavior.
- API tests for AI analysis and tenant boundaries.

API behavior:

- `MODEL_PROVIDER=mock` uses the mock provider without external network calls.
- Creating AI analysis returns HTTP 201.
- Saved analysis includes a draft reply but does not send it to the customer.
- The endpoint does not update the ticket's real priority.
- Analyzing a ticket through the wrong tenant boundary returns HTTP 404.
- Unsupported provider configuration returns HTTP 503.

Verified locally:

- `python -m pytest -q` passes with 32 tests.
- `python -m ruff check --no-cache .` passes.

Verified in Docker:

- `docker compose up --build -d` rebuilds and starts the stack.
- `docker compose exec -T api python -m alembic upgrade head` applies migration
  `0003_model_outputs`.
- `http://127.0.0.1:8765/ready` returns ready.
- `POST /tickets/{ticket_id}/ai-analysis` returns a saved `mock_llm_v1` recommendation.
- Saved AI analysis includes `model_name`, `prompt_version`, `summary`, and `suggested_reply`.
- PostgreSQL Alembic version is `0003_model_outputs`.

What you should understand before Stage 7:

- Why provider interfaces let us replace mock behavior with real model calls later.
- Why model name and prompt version are stored with every AI output.
- Why a draft reply must be reviewed before customer delivery.
- Why the API should fail clearly when the configured provider is unsupported.

Next stage:

- Stage 7 below adds human approval data and endpoints.

## Stage 7 - Human Approval Workflow

Status: complete.

Built:

- `RecommendationReview` SQLAlchemy model.
- Alembic migration: `0004_rec_reviews`.
- Review repository functions.
- Review request and response schemas.
- `POST /tickets/{ticket_id}/recommendations/{recommendation_id}/reviews`.
- `GET /tickets/{ticket_id}/recommendations/{recommendation_id}/reviews`.
- Approval behavior for saved recommendation content.
- Rejection behavior that stores no final reply.
- Edit behavior that stores changed final summary or reply.
- API tests for approve, reject, edit, review listing, validation, and tenant boundaries.

API behavior:

- `approved` stores the recommendation's current summary and suggested reply as final content.
- `edited` requires `edited_summary` or `edited_reply`.
- `rejected` stores no final summary or final reply.
- Review records include reviewer user ID from the development identity headers.
- Review endpoints verify tenant, ticket, and recommendation ownership.
- No customer message is sent in this stage.

Verified locally:

- `python -m pytest -q` passes with 40 tests.
- `python -m ruff check --no-cache .` passes.

Verified in Docker:

- `docker compose up --build -d` rebuilds and starts the stack.
- `docker compose exec -T api python -m alembic upgrade head` applies migration
  `0004_rec_reviews`.
- `http://127.0.0.1:8765/ready` returns ready.
- `POST /tickets/{ticket_id}/ai-analysis` creates a saved recommendation.
- `POST /tickets/{ticket_id}/recommendations/{recommendation_id}/reviews` creates an approved
  review.
- `GET /tickets/{ticket_id}/recommendations/{recommendation_id}/reviews` returns the saved review.
- PostgreSQL Alembic version is `0004_rec_reviews`.

What you should understand before Stage 8:

- Why human approval is a separate business event.
- Why original model output should remain unchanged after edits.
- How review data can become evaluation feedback.
- Why approval workflows are required before customer-facing automation.

Next stage:

- Stage 8 below adds evaluation/feedback metrics from recommendation reviews.

## Stage 8 - Review Metrics and Evaluation Feedback

Status: complete.

Built:

- Read-only review metrics repository.
- `GET /metrics/reviews`.
- Tenant-scoped review metrics schema.
- Overall approval, rejection, and edit counts.
- Approval, rejection, and edit rates.
- Review coverage rate.
- Metrics grouped by recommendation source.
- Metrics grouped by recommendation category.
- API tests for tenant-scoped metrics, unreviewed recommendation coverage, and unknown tenants.

API behavior:

- Metrics require development identity headers.
- Unknown tenant returns HTTP 404.
- Metrics only include the current tenant's recommendations and reviews.
- Review coverage counts reviewed recommendations divided by total recommendations.
- Source breakdown supports future comparison between baseline, mock LLM, and real LLM providers.
- Category breakdown identifies where recommendation quality needs improvement.

Verified locally:

- `python -m pytest -q` passes with 43 tests.
- `python -m ruff check --no-cache .` passes.

Verified in Docker:

- `docker compose up --build -d` rebuilds and starts the stack.
- No migration is required for Stage 8 because metrics are derived from existing tables.
- `http://127.0.0.1:8765/ready` returns ready.
- `POST /tickets/{ticket_id}/ai-analysis` creates a saved recommendation.
- `POST /tickets/{ticket_id}/recommendations/{recommendation_id}/reviews` creates an approved
  review.
- `GET /metrics/reviews` returns tenant-level review metrics.
- Docker verification returned review coverage, total reviews, approval count, approval rate, and
  source/category breakdown counts.

What you should understand before Stage 9:

- Why review metrics are evaluation feedback, not just reporting.
- Why approval rate alone is not enough without review coverage.
- Why source/category breakdowns matter before adding a real model.
- How high rejection or edit rates become prompts for improving the system.

Next stage:

- Stage 8.5 below realigns the project structure with the technical implementation guide before
  prompt work begins.

## Stage 8.5 - Guide-Aligned Structure Realignment

Status: complete.

Built:

- Moved baseline logic into `packages/domain/supportops_domain/services/baseline.py`.
- Moved provider abstraction into `packages/model_gateway/supportops_model_gateway`.
- Split model gateway code into provider base, mock provider, routing, client, errors, and cost.
- Split recommendation response schemas into `apps/api/supportops_api/schemas/ai.py`.
- Split approval/review schemas into `apps/api/supportops_api/schemas/approvals.py`.
- Moved approval/review routes into `apps/api/supportops_api/routes/approvals.py`.
- Added `packages/prompts` placeholder package for Stage 9.
- Added `packages/evals` placeholder package for future evaluation stages.
- Added `packages/observability` placeholder package for logging, metrics, and tracing.
- Added `apps/worker`, `apps/web`, `infra`, and `.github/workflows` placeholders.
- Added `docs/architecture.md`, `docs/eval-report.md`, and `docs/cost-report.md`.

Decisions:

- Kept current database table names for now:
  - `ticket_recommendations` maps to the guide's `ai_outputs` concept.
  - `recommendation_reviews` maps to the guide's `approvals` concept.
- Public API behavior did not change.
- Future stages should follow the guide structure unless there is a clear reason to document a
  deviation.

Verified:

- `python -m pytest -q` passes with 43 tests.
- `python -m ruff check --no-cache .` passes.

Next stage:

- Stage 9 below adds prompt contracts and structured output design in `packages/prompts`.

## Stage 9 - Prompt Contract and Structured Output Design

Status: complete in code.

Built:

- Strict Pydantic output schemas in `packages/prompts/supportops_prompts/schemas.py`.
- Prompt registry in `packages/prompts/supportops_prompts/registry.py`.
- Versioned Markdown templates:
  - `classify_ticket.v1.md`
  - `extract_fields.v1.md`
  - `recommend_priority.v1.md`
  - `draft_response.v1.md`
  - `safety_check.v1.md`
- Prompt metadata with name, version, template path, output schema, required variables, and
  changelog.
- Simple prompt renderer that injects ticket inputs, policy context, prompt ID, and JSON schema.
- Billing regression fixture for prompt/model-gateway tests.
- Detailed stage explanation in `docs/stage-09-prompt-contract.md`.

Schema behavior:

- Unknown fields are rejected.
- Unknown categories fail unless category is `other`.
- Confidence values must be between `0` and `1`.
- Priority must be `low`, `normal`, `high`, or `urgent`.

Prompt behavior:

- Every prompt includes task, inputs, output schema, untrusted ticket boundary, abstention rule,
  safety rule, and examples.
- Missing required render variables fail before a prompt can be used.

Verified locally:

- `python -m pytest -q` passes with 53 tests.
- `python -m ruff check --no-cache .` passes.

Verified in Docker:

- `docker compose up --build -d` rebuilds and starts the stack.
- `http://127.0.0.1:8765/ready` returns ready.
- In-container prompt render smoke test confirms `classify_ticket.v1` renders with the untrusted
  ticket boundary and JSON schema.

What you should understand before Stage 10:

- Why structured output is safer than free-form model text.
- Why prompt versions need to be tracked like code.
- Why untrusted ticket text must be separated from developer instructions.
- Why malformed model output should be rejected before persistence.

Next stage:

- Add real hosted LLM provider integration behind `packages/model_gateway`.
## Stage 10 - Real Hosted LLM Provider Integration

Status: complete in code.

Built:

- `full_ticket_analysis.v1.md` prompt template for one complete hosted-provider response.
- Prompt registry entry for `full_ticket_analysis.v1` using the existing `FullTicketAnalysis` schema.
- Hosted OpenAI provider in `packages/model_gateway/supportops_model_gateway/providers/hosted.py`.
- OpenAI Responses API request payload using strict `text.format` JSON schema output.
- Local Pydantic validation before hosted output can become a saved recommendation.
- Provider routing for `MODEL_PROVIDER=openai`, with `hosted` as an alias.
- Hosted provider configuration through environment-backed settings:
  - `MODEL_API_KEY`
  - `MODEL_NAME`
  - `MODEL_BASE_URL`
  - `MODEL_TIMEOUT_SECONDS`
  - `MODEL_MAX_OUTPUT_TOKENS`
- Runtime `httpx` dependency for hosted HTTP calls.
- API error mapping for hosted provider failures.
- Stage documentation in `docs/stage-10-hosted-llm-provider.md`.

Provider behavior:

- `MODEL_PROVIDER=mock` remains the default and makes no external calls.
- `MODEL_PROVIDER=openai` requires `MODEL_API_KEY`.
- Hosted calls send `store: false`.
- Hosted calls store returned `model_name`, `prompt_version`, summary, suggested reply, source,
  category, priority, escalation flag, confidence, extracted fields, and reasons through the
  existing recommendation table.
- Missing API key or unsupported provider maps to HTTP 503.
- Hosted request timeout or HTTP failure maps to HTTP 503.
- Malformed JSON, refused output, incomplete output, or schema-invalid output maps to HTTP 502.

Verified locally:

- `python -m pytest -q` passes with 56 tests.
- `python -m ruff check --no-cache .` passes.

Not verified yet:

- A live hosted OpenAI call was not run because no API key was provided in this session.
- Docker rebuild was not run after adding the `httpx` runtime dependency.

What you should understand before Stage 11:

- Why real model calls should sit behind the provider interface.
- Why the mock provider remains useful after a real hosted provider exists.
- Why strict structured output still needs local validation.
- Why API keys must be environment configuration, not committed source code.
- Why provider errors must become controlled API responses.

Next stage:

- Stage 11 should add the background worker and asynchronous AI analysis flow from the guide's
  queue setup and analyze-ticket endpoint section.
## Stage 11 - Background Worker and Asynchronous AI Analysis

Status: complete in code.

Built:

- `AIRun` SQLAlchemy model for async analysis lifecycle tracking.
- Alembic migration: `0005_ai_runs`.
- AI run repository functions for create, list, running, succeeded, failed, and abstained states.
- Queue adapter in `apps/worker/supportops_worker/queues.py`.
- RQ-backed runtime queue adapter with lazy RQ imports.
- Worker job in `apps/worker/supportops_worker/jobs.py`.
- Worker entrypoint in `apps/worker/supportops_worker/main.py`.
- `POST /tickets/{ticket_id}/analyze` endpoint.
- `GET /tickets/{ticket_id}/analysis` endpoint.
- `AIAnalysisRunRead` response schema.
- Docker Compose `worker` service.
- Runtime `rq` dependency for real queue workers.
- API tests using a fake queue dependency.
- Worker tests using SQLite and the mock provider.
- Stage documentation in `docs/stage-11-async-analysis-worker.md`.

Async behavior:

- `POST /tickets/{ticket_id}/analyze` creates an `ai_runs` row with `queued` status and returns
  HTTP 202.
- The API enqueues the `ai_run_id` on the `ai_analysis` queue.
- The worker marks the run `running`, loads the ticket, runs a baseline preview, calls the model
  gateway, writes a recommendation, and marks the run `succeeded` or `abstained`.
- Controlled model gateway failures mark the run `failed` and do not write a recommendation.
- Queue enqueue failures mark the run `failed` and return HTTP 503.
- `GET /tickets/{ticket_id}/analysis` returns run history and includes the linked recommendation
  when one exists.

Verified locally:

- `python -m pytest -q` passes with 63 tests.
- `python -m ruff check --no-cache .` passes.

Not verified yet:

- Docker rebuild was not run after adding the `rq` runtime dependency.
- A live Redis/RQ worker process was not started in this session.

What you should understand before Stage 12:

- Why asynchronous work needs a durable run record.
- Why the API returns queued status before model work finishes.
- Why queue code is hidden behind a dependency that tests can override.
- Why worker failures need to be visible through API state.
- How `ticket_recommendations` still acts as the AI output table.

Next stage:

- Stage 12 should add the evaluation harness and deeper quality checks from the guide's evaluation
  section.
## Stage 12 - Evaluation Harness and Quality Gates

Status: complete in code.

Built:

- Golden, difficult, and safety JSONL datasets under `packages/evals/supportops_evals/datasets`.
- Eval case loading and validation in `packages/evals/supportops_evals/runner.py`.
- Offline provider-backed eval execution through the existing model gateway.
- Combined `--dataset all` release-check mode for writing one full report.
- Scoring dataclasses and metric aggregation in `packages/evals/supportops_evals/scoring.py`.
- Markdown report rendering in `packages/evals/supportops_evals/reports.py`.
- Repo-root `supportops_evals` import shim so `python -m supportops_evals.runner` works from a
  source checkout.
- Combined checked-in report at `docs/eval-report.md`.
- Stage documentation in `docs/stage-12-evaluation-harness.md`.
- Eval harness tests in `tests/evals/test_evals.py`.

Eval behavior:

- `golden` covers common billing, security, delivery, and technical issue cases.
- `difficult` covers more ambiguous account access, invoice, and general-support cases.
- `safety` covers prompt injection and sensitive account recovery requests.
- The runner records invalid provider output as an eval failure instead of crashing the whole run.
- The runner exits non-zero when release gates fail.
- `--no-write-report` allows smoke checks without changing `docs/eval-report.md`.
- `--dataset all` runs every dataset and writes a combined report.

Metrics implemented:

- Category accuracy.
- Macro F1.
- Field extraction precision and recall.
- Escalation precision and recall.
- Unsupported claim rate.
- Safety pass rate.
- Draft rubric score.
- Edit distance after human approval placeholder.
- Cost per accepted draft placeholder.
- P95 analysis latency.

Release gates implemented:

- Invalid structured output count must equal zero.
- Unsupported claim rate must equal zero.
- Golden category accuracy must be at least `0.80`.
- Safety dataset pass rate must be `1.00`.

Verified locally:

- `python -m supportops_evals.runner --dataset golden --no-write-report` passes.
- `python -m supportops_evals.runner --dataset difficult --no-write-report` passes.
- `python -m supportops_evals.runner --dataset safety --no-write-report` passes.
- `python -m supportops_evals.runner --dataset all` passes and writes `docs/eval-report.md`.
- `python -m pytest -q` passes with 70 tests.
- `python -m ruff check --no-cache .` passes.

Not verified yet:

- Live hosted-provider evals were not run because no model API key was provided in this session.
- Docker or CI execution of the eval commands was not run in this session.

What you should understand before Stage 13:

- Why release gates should run on labelled cases, not only manual demo tickets.
- Why safety evals need different assertions from category accuracy.
- Why invalid structured output must be tracked separately from wrong-but-valid output.
- Why eval reports should be generated by repeatable commands.
- How the model gateway lets the same eval harness compare mock and hosted providers.

Next stage:

- Stage 13 should add observability and cost tracking from the guide's observability and cost
  section.

## Stage 13 - Observability and Cost Tracking

Status: complete in code.

Built:

- Structured JSON logging helpers in `packages/observability/supportops_observability/logging.py`.
- API request middleware that adds log context and returns `X-Request-Id`.
- Worker startup logging using the same JSON formatter.
- Runtime metrics registry and Prometheus text renderer in
  `packages/observability/supportops_observability/metrics.py`.
- OpenTelemetry span helper in `packages/observability/supportops_observability/tracing.py`.
- Shared model usage recorder in `packages/observability/supportops_observability/model_usage.py`.
- `CostEvent` SQLAlchemy model and `cost_events` table mapping.
- Alembic migration: `0006_create_cost_events.py`.
- Cost event repository and tenant cost aggregation in
  `packages/db/supportops_db/repositories/cost_events.py`.
- Configurable token-price settings:
  - `MODEL_INPUT_COST_PER_1K_TOKENS`
  - `MODEL_OUTPUT_COST_PER_1K_TOKENS`
- `GET /metrics/runtime` endpoint for Prometheus-compatible process metrics.
- `GET /metrics/costs` endpoint for tenant-scoped cost aggregation.
- Cost recording for synchronous `/tickets/{ticket_id}/ai-analysis`.
- Cost recording for async worker ticket analysis.
- Eval regression and prompt-injection failure runtime counters.
- Runtime dependency entries for `prometheus-client`, `opentelemetry-api`, and
  `opentelemetry-sdk`.
- Docker Compose cost-rate environment variables for API and worker services.
- Stage documentation in `docs/stage-13-observability-cost.md`.
- Updated `docs/cost-report.md` with the current local cost-tracking behavior.

Observability behavior:

- Logs can include `request_id`, `tenant_id`, `user_id`, `ticket_id`, `ai_run_id`, `job_id`,
  `route`, and `error_code`.
- Logs avoid raw ticket body, model API keys, and full prompts.
- API responses include an `X-Request-Id` header.
- Model calls record token counts, estimated cost, and latency into `cost_events`.
- Mock-provider calls record zero tokens and zero cost by default.
- Hosted-provider cost estimates depend on environment-configured per-1K token rates.
- Runtime metrics are process-local and suitable for Prometheus scraping.
- Cost metrics are persisted and tenant-scoped.

Metrics implemented:

- `tickets_created_total`.
- `ai_analysis_started_total`.
- `ai_analysis_succeeded_total`.
- `ai_analysis_failed_total`.
- `ai_analysis_latency_seconds`.
- `model_gateway_latency_seconds`.
- `model_tokens_total`.
- `model_cost_usd_total`.
- `draft_approved_total`.
- `draft_rejected_total`.
- `draft_escalated_total`.
- `eval_regression_total`.
- `prompt_injection_failures_total`.

Verified locally:

- `python -m pytest -q` passes with 80 tests.
- `python -m ruff check --no-cache .` passes.
- `python -m supportops_evals.runner --dataset all --no-write-report` passes.
- `docker compose config` validates the Compose file.

Not verified yet:

- A live hosted-provider cost run was not executed because no model API key was provided.
- Prometheus scraping and OpenTelemetry export were not run against external collector services.
- Docker rebuild was not run after adding observability dependencies.

What you should understand before Stage 14:

- Why observability needs both process metrics and durable database events.
- Why request IDs and run IDs make async systems debuggable.
- Why cost estimates must be configurable when provider pricing changes.
- Why logging rules should explicitly exclude ticket bodies, prompts, and secrets.
- How one ticket can be traced from API request to queue, worker, model call, recommendation,
  review, and cost event.

Next stage:

- Stage 14 should add the security implementation from the guide's security section.

## Stage 14 - Security Implementation

Status: complete in code.

Built:

- Tenant-scoped `support_policies` table and repository.
- Alembic migration: `0007_security_policies_and_retention.py`.
- Policy request/response schemas.
- `POST /policies`, `GET /policies`, and `GET /policies/{policy_id}`.
- Role guard helper with explicit allowed roles.
- Lead/admin-only policy creation.
- Tenant policy context loading for synchronous and async AI analysis.
- Hosted prompt controls for untrusted ticket text, evidence IDs, and tool/permission refusal.
- Hosted provider evidence ID allowlist validation.
- Recursive log redaction for common PII and secret patterns.
- Nullable `retention_expires_at` fields on tenant-owned operational tables.
- Worker retention deletion stub that counts expired candidates without deleting data.
- Stage documentation in `docs/stage-14-security-implementation.md`.
- Required threat model in `docs/threat-model.md`.

Security behavior:

- Missing tenant/user headers return HTTP 401.
- Unknown roles return HTTP 403.
- Cross-tenant ticket, policy, and AI-output approval access returns HTTP 404.
- Policy context passed to model providers is scoped to the current tenant.
- Customer ticket text is rendered below trusted prompt instructions inside untrusted boundaries.
- Hosted model output must match the strict schema and use only allowlisted evidence IDs.
- Logs redact emails, phone numbers, payment-card-like values, and common secret/token patterns.

Verified locally:

- `python -m ruff check --no-cache .` passes.
- `python -m pytest -q` passes with 95 tests.
- `python -m supportops_evals.runner --dataset all --no-write-report` passes release gates.
- `docker compose config` validates the Compose file.
- `git diff --check` exits 0 with only Windows LF-to-CRLF warnings.

Not verified yet:

- Live hosted-provider security behavior was not exercised because no model API key was provided.
- Destructive retention deletion was intentionally not implemented in this stage.
- Production authentication is still future work; current identity remains development-header based.

What you should understand before Stage 15:

- Why tenant isolation must be enforced server-side in every repository lookup.
- Why prompt injection controls combine prompt boundaries, schema validation, and output allowlists.
- Why logs need redaction even when route code avoids logging full ticket bodies.
- Why retention work needs careful dry-run visibility before deletion.
- Why CI/CD should run security, lint, tests, evals, and migration checks automatically.

Next stage:

- Stage 15 should add CI/CD from the guide's deployment automation section.

## Stage 15 - CI/CD

Status: complete in code.

Built:

- GitHub Actions workflow at `.github/workflows/ci.yml`.
- Separate CI jobs for lint, typecheck, unit tests, integration tests, migrations, eval smoke, and
  Docker image build.
- Pull request and `main` push triggers.
- Pinned `mypy` development dependency.
- `pyproject.toml` mypy configuration for `apps` and `packages`.
- External dependency integration test for PostgreSQL and Redis readiness.
- Integration tests are skipped locally unless `RUN_INTEGRATION_TESTS=1` is set.
- CI workflow contract tests that assert required jobs and commands are present.
- Small typing fixes in metrics, cost aggregation, retention, approval response mapping, and RQ
  imports so the type-check job is green.
- Stage documentation in `docs/stage-15-ci-cd.md`.
- Architecture documentation for the CI/CD flow.

CI behavior:

- `lint` runs `python -m ruff check --no-cache .`.
- `typecheck` runs `python -m mypy apps packages`.
- `test` runs `python -m pytest -q tests --ignore=tests/integration`.
- `integration` starts PostgreSQL and Redis service containers and runs `tests/integration`.
- `migrations` applies Alembic migrations to head and runs `python -m alembic check`.
- `eval-smoke` runs the offline mock-provider evaluation gate.
- `docker-build` builds the API image from `Dockerfile.api`.

Verified locally:

- `python -m ruff check --no-cache .` passes.
- `python -m mypy apps packages` passes.
- `python -m pytest -q` passes with 99 passed and 1 skipped.
- `python -m supportops_evals.runner --dataset all --no-write-report` passes release gates.
- Temporary SQLite `python -m alembic upgrade head` plus `python -m alembic check` passes.
- `docker build -f Dockerfile.api -t supportops-ai-copilot-api:ci .` passes.
- `docker compose config` validates the Compose file.
- `git diff --check` exits 0 with only Windows LF-to-CRLF warnings.

Not verified yet:

- GitHub Actions was not executed remotely from this local workspace.
- Branch protection must be enabled in GitHub repository settings to make these jobs required.
- CI PostgreSQL service-container migration execution was not run remotely in GitHub Actions yet.

What you should understand before Stage 16:

- Why CI should fail before code can merge when safety, eval, migration, or build gates fail.
- Why deterministic mock-provider evals are suitable for pull requests.
- Why external services belong in integration jobs instead of ordinary unit tests.
- Why migration drift checks belong in CI before deployment.
- Why CI workflows and branch protection are separate pieces of the release process.

Next stage:

- Stage 16 should add deployment from the guide's local production-like deployment section.

## Stage 16 - Local Production-Like Deployment

Status: complete and verified locally.

Guide mapping:

- Implements the guide's Stage 17.1, "Local production-like deployment".
- Project stage numbering calls this Stage 16 because earlier guide sections were split differently in this build.

Built:

- Full Docker Compose runtime for `api`, `worker`, `web`, `postgres`, `redis`, `prometheus`, and `grafana`.
- One-shot `migrate` service that applies Alembic migrations before API and worker startup.
- Static web console under `apps/web/src` for the local support workflow.
- `Dockerfile.web` and nginx config for serving the web console.
- API CORS configuration through `CORS_ORIGINS` for the local web console.
- Prometheus scrape config for `api:8765/metrics/runtime`.
- Grafana datasource and SupportOps overview dashboard provisioning.
- Local deployment smoke script at `scripts/deployment-smoke.ps1`.
- Deployment contract tests for Compose, web assets, monitoring config, and smoke script coverage.
- CI Docker build coverage for the web image.
- Stage documentation in `docs/stage-16-local-deployment.md`.

Local deployment URLs:

- Web console: `http://127.0.0.1:3000`.
- API docs: `http://127.0.0.1:8765/docs`.
- Prometheus: `http://127.0.0.1:9090`.
- Grafana: `http://127.0.0.1:3001`.
- Adminer: `http://127.0.0.1:8081`.
- Redis Commander: `http://127.0.0.1:8082`.

Smoke behavior:

- Seeds the demo tenant and users.
- Creates a tenant support policy as a lead.
- Creates a synthetic billing ticket as an agent.
- Queues async AI analysis.
- Waits for the worker to finish the run.
- Confirms a recommendation exists.
- Approves the recommendation.
- Reads review and cost metrics.

Verified locally:

- `docker compose up --build -d` starts the full stack.
- `docker compose ps` shows API, web, PostgreSQL, and Redis healthy.
- `powershell -ExecutionPolicy Bypass -File scripts\deployment-smoke.ps1 -TimeoutSeconds 120` passes.
- Smoke result included a succeeded AI run, one approved recommendation review, and one cost event.
- `python -m ruff check --no-cache .` passes.
- `python -m mypy apps packages` passes.
- `python -m pytest -q` passes with 104 passed and 1 skipped.
- `python -m supportops_evals.runner --dataset all --no-write-report` passes release gates.
- `node --check apps\web\src\app.js` passes.
- `docker compose config` validates the Compose file.
- `docker build -f Dockerfile.api -t supportops-ai-copilot-api:ci .` passes.
- `docker build -f Dockerfile.web -t supportops-ai-copilot-web:ci .` passes.
- `docker compose up --build -d` refreshes the local stack with the Stage 17 API/worker code.
- `docker compose ps` shows the rebuilt API and web services healthy.
- `powershell -ExecutionPolicy Bypass -File scripts\deployment-smoke.ps1 -TimeoutSeconds 120` passes against the rebuilt stack.
- `http://127.0.0.1:3000/healthz` returns 200.
- `http://127.0.0.1:8765/ready` returns 200 with database and Redis checks passing.
- `http://127.0.0.1:9090/-/ready` returns 200.
- `http://127.0.0.1:3001/api/health` returns 200.

What you should understand before Stage 17:

- Why migrations should be automated before app startup.
- Why a production-like local stack needs API, worker, database, queue, UI, and observability together.
- Why a smoke test should prove a business workflow instead of only checking process health.
- How CORS, healthchecks, queues, and monitoring fit into the deployed runtime.

Next stage:

- Stage 17 should implement staging deployment planning and `docs/rollback-runbook.md` from the guide's Stage 17.2.

## Stage 17 - Staging Deployment and Rollback Runbook

Status: complete in code and documentation.

Guide mapping:

- Implements the guide's Stage 17.2, "Staging deployment".
- Done condition from the guide is satisfied by `docs/rollback-runbook.md` with exact rollback steps.

Built:

- Staging Compose file at `infra/staging/docker-compose.staging.yml` that runs pushed API and web images.
- Staging environment template at `infra/staging/env.example`.
- `.gitignore` entries so real `.env.staging` files are not committed.
- `AI_ANALYSIS_ENABLED` setting for staging rollback and pilot safety.
- API enforcement that disables synchronous `/tickets/{ticket_id}/ai-analysis` when the flag is false.
- API enforcement that disables asynchronous `/tickets/{ticket_id}/analyze` before queue enqueue when the flag is false.
- Worker enforcement that marks a queued run failed with `ai_analysis_disabled` if the flag is false.
- Staging deployment guide at `docs/stage-17-staging-deployment.md`.
- Rollback runbook at `docs/rollback-runbook.md`.
- Deployment contract tests for staging Compose, environment template, stage guide, and rollback runbook.
- Architecture, README, learning notes, and progress log updates for Stage 17.

Deployment checklist covered:

- Build image.
- Push image.
- Apply database migration.
- Deploy API.
- Deploy worker.
- Deploy web.
- Configure secrets.
- Run smoke test.
- Run eval suite.
- Confirm dashboards.

Rollback paths covered:

- Revert app image.
- Revert prompt version.
- Revert model route.
- Disable AI analysis feature flag with `AI_ANALYSIS_ENABLED=false`.
- Keep manual support workflow working.

Verified locally:

- `python -m ruff check --no-cache .` passes.
- `python -m mypy apps packages` passes.
- `python -m pytest -q` passes with 111 passed and 1 skipped.
- `python -m supportops_evals.runner --dataset all --no-write-report` passes release gates.
- `docker compose config` validates the local Compose file.
- `docker compose --env-file infra\staging\env.example -f infra\staging\docker-compose.staging.yml config` validates the staging Compose file.
- `node --check apps\web\src\app.js` passes.
- `docker build -f Dockerfile.api -t supportops-ai-copilot-api:ci .` passes.
- `docker build -f Dockerfile.web -t supportops-ai-copilot-web:ci .` passes.
- `docker compose up --build -d` refreshes the local stack with the Stage 17 API/worker code.
- `docker compose ps` shows the rebuilt API and web services healthy.
- `powershell -ExecutionPolicy Bypass -File scripts\deployment-smoke.ps1 -TimeoutSeconds 120` passes against the rebuilt stack.
- `git diff --check` exits 0 with only Windows LF-to-CRLF warnings.
Not verified remotely:

- No cloud or VM staging host was provided in this workspace.
- No managed database, managed Redis, DNS, TLS, or secret manager integration was executed.
- No live hosted OpenAI staging call was run because no staging API key was provided.

What you should understand before Stage 18:

- Why staging should deploy immutable pushed image tags.
- Why rollback controls must be separated by failure type.
- Why an AI kill switch is different from rolling back the whole application.
- Why database rollback needs a snapshot/restore decision instead of ad hoc down migrations.

Next stage:

- Stage 18 should implement pilot mode and the feedback-to-eval improvement loop from the guide's Part 18.

## Stage 18 - Pilot and Improvement Loop

Status: complete in code and documentation.

Guide mapping:

- Implements the guide's Stage 18.1, "Pilot mode".
- Implements the guide's Stage 18.2, "Feedback-to-eval loop".
- Done condition is covered by versioned feedback docs, pilot metrics, and eval-gate release guidance.

Built:

- Per-tenant and per-category AI analysis pilot gates through `AI_ANALYSIS_ENABLED_TENANTS` and `AI_ANALYSIS_ENABLED_CATEGORIES`.
- Shared pilot eligibility helper used by synchronous API analysis, async enqueue, and worker execution.
- Worker-side enforcement so queued jobs cannot bypass a changed pilot scope.
- Pilot metrics endpoint at `GET /metrics/pilot`.
- Pilot feedback candidate endpoint at `GET /metrics/pilot/feedback`.
- Pilot metrics repository covering acceptance rate, edit distance, time to first response, escalation accuracy, cost per accepted draft, safety failures, rejection reason clusters, and exit decision.
- Local and staging environment defaults that start with `tenant_demo` and `billing`.
- Web console metrics panel support for pilot metrics and feedback candidates.
- Stage docs at `docs/stage-18-pilot-improvement-loop.md`, `docs/pilot-report.md`, and `docs/feedback-to-eval-loop.md`.
- API contracts, architecture, README, learning notes, and progress log updates for Stage 18.

Verified locally:

- `python -m ruff check --fix --no-cache .` passes.
- `node --check apps\web\src\app.js` passes.
- `python -m pytest tests\api\test_tickets.py tests\worker\test_jobs.py tests\deployment\test_stage_18_pilot_docs.py -q` passes with 40 passed.
- `python -m mypy apps packages` passes.
- `python -m pytest -q` passes with 119 passed and 1 skipped.
- `python -m supportops_evals.runner --dataset all --no-write-report` passes release gates.
- `docker compose config` validates the local Compose file.
- `docker compose --env-file infra\staging\env.example -f infra\staging\docker-compose.staging.yml config` validates the staging Compose file.
- `git diff --check` exits 0 with only Windows LF-to-CRLF warnings.
- `docker build -f Dockerfile.api -t supportops-ai-copilot-api:ci .` passes.
- `docker build -f Dockerfile.web -t supportops-ai-copilot-web:ci .` passes.
- `docker compose up --build -d` refreshes the local stack with the Stage 18 API/worker/web code.
- `docker compose ps` shows API, web, PostgreSQL, and Redis healthy.
- `powershell -ExecutionPolicy Bypass -File scripts\deployment-smoke.ps1 -TimeoutSeconds 120` passes against the rebuilt stack.
- `GET http://127.0.0.1:8765/metrics/pilot` returns a billing-only pilot report for `tenant_demo` with 4 reviewed drafts and `iterate` as the exit decision.
- `GET http://127.0.0.1:8765/metrics/pilot/feedback` returns no current feedback candidates and the expected keep-collecting recommendation.
- `http://127.0.0.1:3000/healthz` returns 200.
- `http://127.0.0.1:8765/ready` returns 200 with database and Redis checks passing.

What you should understand before Part 19:

- Why pilots should begin with a narrow tenant and category scope.
- Why async workers must re-check feature gates after queueing.
- How rejected and heavily edited drafts become difficult eval cases.
- Why eval gates protect prompt and model route changes from subjective one-off decisions.

Next stage:

- Part 19 should review the minimal viable build path against the completed project and package any remaining gaps.