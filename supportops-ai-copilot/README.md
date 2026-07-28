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

Stage 18: pilot mode and feedback-to-eval improvement loop.

Next stage: Part 19 - minimal viable build path review.

## Project Structure

The project now follows the main package boundaries from the technical implementation guide:

```text
apps/api                FastAPI application
apps/worker             background worker for async analysis jobs
apps/web                static local agent console
packages/domain         business rules
packages/db             SQLAlchemy, repositories, migrations
packages/model_gateway  provider-neutral model access
packages/prompts        prompt templates and output schemas
packages/evals          evaluation datasets, scoring, reports, and gates
packages/observability  structured logs, runtime metrics, traces, cost helpers
infra                   deployment and monitoring assets
```

Detailed stage docs:

- `docs/stage-09-prompt-contract.md`
- `docs/stage-10-hosted-llm-provider.md`
- `docs/stage-11-async-analysis-worker.md`
- `docs/stage-12-evaluation-harness.md`
- `docs/stage-13-observability-cost.md`
- `docs/stage-14-security-implementation.md`
- `docs/stage-15-ci-cd.md`
- `docs/stage-16-local-deployment.md`
- `docs/stage-17-staging-deployment.md`
- `docs/stage-18-pilot-improvement-loop.md`
- `docs/pilot-report.md`
- `docs/feedback-to-eval-loop.md`
- `docs/rollback-runbook.md`
- `docs/threat-model.md`

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

Run type checks:

```powershell
python -m mypy apps packages
```

Run offline evaluation gates:

```powershell
python -m supportops_evals.runner --dataset golden
python -m supportops_evals.runner --dataset difficult
python -m supportops_evals.runner --dataset safety
python -m supportops_evals.runner --dataset all
```

`--dataset all` writes the combined report to `docs/eval-report.md`.

Run the CI gate locally:

```powershell
python -m ruff check --no-cache .
python -m mypy apps packages
python -m pytest -q
python -m supportops_evals.runner --dataset all --no-write-report
docker compose config
docker build -f Dockerfile.api -t supportops-ai-copilot-api:ci .
docker build -f Dockerfile.web -t supportops-ai-copilot-web:ci .
git diff --check
```


View pilot metrics:

```powershell
Invoke-RestMethod -Method Get `
  -Uri 'http://127.0.0.1:8765/metrics/pilot' `
  -Headers $headers

Invoke-RestMethod -Method Get `
  -Uri 'http://127.0.0.1:8765/metrics/pilot/feedback' `
  -Headers $headers
```

Pilot controls:

```text
AI_ANALYSIS_ENABLED=true
AI_ANALYSIS_ENABLED_TENANTS=tenant_demo
AI_ANALYSIS_ENABLED_CATEGORIES=billing
```
Run staging deployment checks:

```powershell
docker compose --env-file infra/staging/env.example -f infra/staging/docker-compose.staging.yml config
Get-Content -LiteralPath docs/rollback-runbook.md
```

Disable AI analysis during staging rollback:

```text
AI_ANALYSIS_ENABLED=false
```
GitHub Actions workflow:

```text
.github/workflows/ci.yml
```

View runtime Prometheus metrics:

```powershell
Invoke-WebRequest -Uri 'http://127.0.0.1:8765/metrics/runtime' -UseBasicParsing
```

View tenant cost metrics:

```powershell
Invoke-RestMethod -Method Get `
  -Uri 'http://127.0.0.1:8765/metrics/costs' `
  -Headers $headers
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

Run the full local production-like Docker stack:

```powershell
docker compose up --build -d
docker compose ps
```

Open the local deployment:

```text
Web console: http://127.0.0.1:3000
API docs:    http://127.0.0.1:8765/docs
Prometheus:  http://127.0.0.1:9090
Grafana:     http://127.0.0.1:3001
Adminer:     http://127.0.0.1:8081
Redis UI:    http://127.0.0.1:8082
```

Open the containerized API health endpoints:

```text
http://127.0.0.1:8765/health
http://127.0.0.1:8765/ready
```

Run the deployment smoke test:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\deployment-smoke.ps1 -TimeoutSeconds 120
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

Create tenant support policy context for hosted analysis:

```powershell
$leadHeaders = @{
  'X-Tenant-Id' = 'tenant_demo'
  'X-User-Id' = 'user_demo_lead'
  'X-Role' = 'lead'
}

$policy = @{
  name = 'Refund review'
  content = 'Agents must verify duplicate charges before promising refunds.'
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post `
  -Uri 'http://127.0.0.1:8765/policies' `
  -Headers $leadHeaders `
  -Body $policy `
  -ContentType 'application/json'
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

Run hosted OpenAI analysis instead of the mock provider:

```powershell
$env:MODEL_PROVIDER = 'openai'
$env:MODEL_API_KEY = '<your-api-key>'
$env:MODEL_NAME = 'gpt-5.6'
$env:MODEL_INPUT_COST_PER_1K_TOKENS = '<input-rate>'
$env:MODEL_OUTPUT_COST_PER_1K_TOKENS = '<output-rate>'

python -m uvicorn supportops_api.main:app --reload --app-dir apps/api --host 127.0.0.1 --port 8765
```

Then call the same endpoint:

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8765/tickets/$ticketId/ai-analysis" `
  -Headers $headers
```

Queue async AI analysis for a ticket:

```powershell
$analysisRun = Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8765/tickets/$ticketId/analyze" `
  -Headers $headers

$analysisRun.id
$analysisRun.status
```

List async analysis runs for a ticket:

```powershell
Invoke-RestMethod -Method Get `
  -Uri "http://127.0.0.1:8765/tickets/$ticketId/analysis" `
  -Headers $headers
```

Run the worker in Docker:

```powershell
docker compose up --build api worker postgres redis
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
