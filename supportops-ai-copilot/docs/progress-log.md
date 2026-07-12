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

- Add prompt contract and structured output design for the future real LLM provider.
