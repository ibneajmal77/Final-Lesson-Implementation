# SupportOps AI Copilot

This project is a production-style learning build for a support-ticket AI copilot.

The first goal is a tiny working backend:

```text
FastAPI app
-> typed settings
-> health endpoint
-> readiness endpoint
-> tests
-> Docker Compose dependencies
```

Real external LLM calls come after the backend foundation, deterministic baseline, and provider
contract are working and tested.

## Current Stage

Stage 8.5: guide-aligned structure realignment.

Next stage: Stage 9 - prompt contract and structured output design.

## Project Structure

The project now follows the main package boundaries from the technical implementation guide:

```text
apps/api                FastAPI application
apps/worker             future background worker
apps/web                future agent UI
packages/domain         business rules
packages/db             SQLAlchemy, repositories, migrations
packages/model_gateway  provider-neutral model access
packages/prompts        prompt templates and output schemas
packages/evals          evaluation datasets and scoring
packages/observability  logs, metrics, traces
infra                   future deployment/monitoring assets
```

## Local Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Run the API:

```powershell
python -m uvicorn supportops_api.main:app --reload --app-dir apps/api --host 127.0.0.1 --port 8765
```

Run tests:

```powershell
python -m pytest
```

Run lint:

```powershell
python -m ruff check --no-cache .
```

Run local dependencies:

```powershell
docker compose up -d postgres redis
```

PostgreSQL and Redis are available to other containers through the Compose network as `postgres`
and `redis`. They are not published to host ports by default, which avoids conflicts with local
PostgreSQL or Redis installs.

Run database and cache UIs:

```powershell
docker compose up -d postgres-ui redis-ui
```

Open PostgreSQL UI:

```text
http://127.0.0.1:8081
```

Adminer login values:

```text
System: PostgreSQL
Server: postgres
Username: supportops
Password: supportops
Database: supportops
```

Open Redis UI:

```text
http://127.0.0.1:8082
```

Run the full Docker stack:

```powershell
docker compose up --build
```

Open the containerized API:

```text
http://127.0.0.1:8765/health
http://127.0.0.1:8765/docs
```

Check real container dependency readiness:

```powershell
Invoke-WebRequest -Uri 'http://127.0.0.1:8765/ready' -UseBasicParsing
```

Expected response:

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

Apply database migrations:

```powershell
docker compose exec -T api python -m alembic upgrade head
```

Inspect database tables:

```powershell
docker compose exec -T postgres psql -U supportops -d supportops -c "\dt"
```

Seed demo tenant data:

```powershell
docker compose exec -T api python -m supportops_api.seed
```

Create a demo ticket:

```powershell
$headers = @{
  'X-Tenant-Id' = 'tenant_demo'
  'X-User-Id' = 'user_demo_agent'
  'X-Role' = 'agent'
}

$body = @{
  external_id = 'demo-ticket-001'
  channel = 'email'
  subject = 'Charged twice'
  body = 'I was charged twice for order ORD-123.'
  customer_id = 'customer-123'
  metadata = @{source = 'manual-test'}
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post `
  -Uri 'http://127.0.0.1:8765/tickets' `
  -Headers $headers `
  -Body $body `
  -ContentType 'application/json'
```

List tickets:

```powershell
Invoke-RestMethod -Method Get -Uri 'http://127.0.0.1:8765/tickets' -Headers $headers
```

Run baseline analysis for a ticket:

```powershell
$tickets = Invoke-RestMethod -Method Get `
  -Uri 'http://127.0.0.1:8765/tickets' `
  -Headers $headers

$ticketId = $tickets[0].id

Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8765/tickets/$ticketId/baseline-analysis" `
  -Headers $headers
```

Run mock AI analysis for a ticket:

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8765/tickets/$ticketId/ai-analysis" `
  -Headers $headers
```

List saved recommendations:

```powershell
$recommendations = Invoke-RestMethod -Method Get `
  -Uri "http://127.0.0.1:8765/tickets/$ticketId/recommendations" `
  -Headers $headers

$recommendationId = $recommendations[0].id
```

Approve a recommendation:

```powershell
$review = @{
  decision = 'approved'
  notes = 'Ready for agent use.'
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8765/tickets/$ticketId/recommendations/$recommendationId/reviews" `
  -Headers $headers `
  -Body $review `
  -ContentType 'application/json'
```

Edit a recommendation before use:

```powershell
$review = @{
  decision = 'edited'
  edited_reply = 'I reviewed the billing issue and will verify the duplicate charge.'
  notes = 'Adjusted reply before approval.'
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8765/tickets/$ticketId/recommendations/$recommendationId/reviews" `
  -Headers $headers `
  -Body $review `
  -ContentType 'application/json'
```

List review history:

```powershell
Invoke-RestMethod -Method Get `
  -Uri "http://127.0.0.1:8765/tickets/$ticketId/recommendations/$recommendationId/reviews" `
  -Headers $headers
```

View review metrics:

```powershell
Invoke-RestMethod -Method Get `
  -Uri 'http://127.0.0.1:8765/metrics/reviews' `
  -Headers $headers
```

## Learning Rule

For every feature:

1. Build the smallest working version.
2. Run it.
3. Test it.
4. Break it once and debug it.
5. Write a short note in `docs/learning-notes.md`.
