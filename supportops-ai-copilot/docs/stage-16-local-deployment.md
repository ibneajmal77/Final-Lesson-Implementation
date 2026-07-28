# Stage 16 - Local Production-Like Deployment

Status: complete in code and verified locally.

Guide mapping: this implements the guide's Stage 17.1, "Local production-like deployment." The
project stage number is Stage 16 because earlier guide sections were split differently in this
learning build.

## Goal

Run the whole SupportOps AI Copilot stack from Docker Compose and prove that a synthetic support
ticket can move through the operational workflow:

```text
web console / API request
-> API
-> PostgreSQL
-> Redis queue
-> worker AI analysis
-> saved recommendation
-> human review
-> runtime and cost metrics
```

## Services

`docker-compose.yml` now starts the full local stack:

- `migrate`: one-shot Alembic migration service.
- `api`: FastAPI API on `http://127.0.0.1:8765`.
- `worker`: RQ worker for async AI analysis jobs.
- `web`: static agent console on `http://127.0.0.1:3000`.
- `postgres`: PostgreSQL 16 with persistent local volume.
- `redis`: Redis 7 with persistent local volume.
- `prometheus`: Prometheus on `http://127.0.0.1:9090`.
- `grafana`: Grafana on `http://127.0.0.1:3001`.
- `postgres-ui`: Adminer on `http://127.0.0.1:8081`.
- `redis-ui`: Redis Commander on `http://127.0.0.1:8082`.

The guide required `api`, `worker`, `web`, `postgres`, `redis`, `prometheus`, and `grafana`. The
database/cache UI services remain as local developer helpers.

## Deployment Behavior

- `migrate` runs `python -m alembic upgrade head` before the API or worker starts.
- `api` waits for successful migrations and healthy Redis.
- `web` waits for the API healthcheck and serves static files through nginx.
- `prometheus` scrapes `api:8765/metrics/runtime`.
- `grafana` provisions a Prometheus datasource and the SupportOps overview dashboard.
- `MODEL_PROVIDER=mock` remains the local default so the deployment works without external API
  keys.
- `CORS_ORIGINS` allows the local web console to call the API from `127.0.0.1:3000` or
  `localhost:3000`.

## Web Console

The local web app is a dependency-free static console under `apps/web/src`. It supports the core
operator workflow:

- Check API health and readiness.
- Create and list tickets.
- Queue async AI analysis.
- View analysis run history.
- View saved recommendations.
- Approve a recommendation.
- Create and list support policies.
- View review, cost, and runtime metrics.

## Run

Start or rebuild the full stack:

```powershell
docker compose up --build -d
```

Check service status:

```powershell
docker compose ps
```

Open the local surfaces:

```text
Web console: http://127.0.0.1:3000
API docs:    http://127.0.0.1:8765/docs
Prometheus:  http://127.0.0.1:9090
Grafana:     http://127.0.0.1:3001
```

Grafana local login:

```text
Username: admin
Password: supportops
```

## Smoke Test

Run the deployment smoke script after the stack is up:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\deployment-smoke.ps1 -TimeoutSeconds 120
```

The script:

- Seeds the demo tenant and users.
- Creates a tenant support policy as a lead.
- Creates a synthetic billing ticket as an agent.
- Queues async AI analysis.
- Polls until the worker completes the run.
- Verifies that a recommendation was saved.
- Approves the recommendation.
- Reads review and cost metrics.
- Prints IDs and counters as JSON.

Latest local smoke result:

```json
{
  "ai_run_status": "succeeded",
  "reviewed_recommendations": 1,
  "cost_events": 1
}
```

## Verification

Verified locally on July 21, 2026:

- `docker compose up --build -d` starts the full stack.
- `docker compose ps` shows `api`, `web`, `postgres`, and `redis` healthy.
- `scripts\deployment-smoke.ps1` completes a synthetic ticket workflow with a succeeded async run.
- `node --check apps\web\src\app.js` passes.
- `docker compose config` passes.
- `docker build -f Dockerfile.web -t supportops-ai-copilot-web:ci .` passes.
- `http://127.0.0.1:3000/healthz` returns 200.
- `http://127.0.0.1:8765/ready` returns 200 with database and Redis checks passing.
- `http://127.0.0.1:9090/-/ready` returns 200.
- `http://127.0.0.1:3001/api/health` returns 200.

Additional checks verified locally:

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

## Not Verified

- A live hosted OpenAI deployment path was not run because no API key was provided.
- Remote staging or cloud deployment is intentionally left for the next stage.

## What You Should Understand Before Stage 17

- Why migrations should run before API and worker processes accept traffic.
- Why Docker healthchecks are different from unit tests.
- Why the worker needs Redis and a durable `ai_runs` table to make async progress visible.
- Why a smoke test should exercise the business workflow, not only `/health`.
- Why local observability should be available before moving to staging.

## Next Stage

Stage 17 should implement the staging deployment checklist and `docs/rollback-runbook.md`.

## Files Added and Changed in This Stage

### New files
- `apps/web/src/index.html`, `apps/web/src/app.js`, `apps/web/src/styles.css` — static agent console.
- `apps/web/nginx.conf` — static serving + `/healthz`.
- `Dockerfile.web` — web image.
- `infra/prometheus/prometheus.yml` — scrape config for `api:8765/metrics/runtime`.
- `infra/grafana/provisioning/datasources/prometheus.yml`
- `infra/grafana/provisioning/dashboards/dashboards.yml`
- `infra/grafana/dashboards/supportops-overview.json`
- `scripts/deployment-smoke.ps1` — end-to-end business-workflow smoke test.
- `tests/deployment/` — Compose/web/monitoring/smoke contract tests.
- `docs/stage-16-local-deployment.md` (this file)

### Changed files
- `docker-compose.yml` — added `migrate`, `web`, `prometheus`, `grafana`, `postgres-ui`, `redis-ui`; startup ordering and healthchecks.
- `apps/api/supportops_api/main.py` — CORS middleware.
- `apps/api/supportops_api/settings.py` — `cors_origins`.
- `.github/workflows/ci.yml` — web image build coverage.
- `docs/progress-log.md`, `README.md`, `docs/architecture.md` — Stage 16 updates.

> Stage-by-stage verification counts and commands live under **Stage 16** in
> [progress-log.md](progress-log.md). The cumulative map of every stage's files is in
> [file-change-log.md](file-change-log.md).
