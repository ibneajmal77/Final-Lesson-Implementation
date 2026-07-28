# Stage 17 - Staging Deployment and Rollback Runbook

Status: complete in code and documentation. A remote staging host was not available in this
workspace, so this stage provides the VM-ready staging deployment path and exact rollback runbook.

Guide mapping: this implements the guide's Stage 17.2, "Staging deployment."

## Goal

Create a repeatable staging deployment process that can run on one cloud VM or local VM, with
runtime secrets kept outside the repository and a rollback path that preserves the manual support
workflow.

## Chosen Staging Shape

The staging target is a single Docker Compose host:

```text
pushed API image
-> migrate service applies Alembic migrations
-> API service starts
-> worker service starts
-> pushed web image starts
-> Prometheus scrapes API metrics
-> Grafana loads the SupportOps dashboard
```

PostgreSQL and Redis are expected to be managed services when available. For a small VM-only staging
setup, they can also be separate infrastructure services, but they should not reuse the local
development credentials from `docker-compose.yml`.

## Files Added

- `infra/staging/docker-compose.staging.yml`: staging Compose file that uses pushed image tags.
- `infra/staging/env.example`: non-secret template for staging runtime configuration.
- `docs/rollback-runbook.md`: exact rollback steps required by the guide.

## Build Images

From the repository root:

```powershell
$Registry = 'ghcr.io/OWNER'
$ImageTag = git rev-parse --short HEAD

$ApiImage = "$Registry/supportops-ai-copilot-api:$ImageTag"
$WebImage = "$Registry/supportops-ai-copilot-web:$ImageTag"

docker build -f Dockerfile.api -t $ApiImage .
docker build -f Dockerfile.web -t $WebImage .
```

## Push Images

```powershell
docker push $ApiImage
docker push $WebImage
```

Record both image tags in the deployment ticket or release notes. These image tags are the primary
rollback handles.

## Configure Secrets

On the staging host, create `infra/staging/.env.staging` from `infra/staging/env.example`, or load
the same keys from a secret manager.

Required values:

- `SUPPORTOPS_API_IMAGE`.
- `SUPPORTOPS_WEB_IMAGE`.
- `DATABASE_URL`.
- `REDIS_URL`.
- `CORS_ORIGINS`.
- `AI_ANALYSIS_ENABLED`.
- `MODEL_PROVIDER`.
- `MODEL_API_KEY` when `MODEL_PROVIDER=openai`.
- `GF_SECURITY_ADMIN_PASSWORD`.

Do not commit `.env.staging`.

## Apply Database Migration

The staging Compose file runs migrations through a one-shot `migrate` service. To run migration
explicitly before starting app traffic:

```powershell
$EnvFile = 'infra/staging/.env.staging'
$ComposeFile = 'infra/staging/docker-compose.staging.yml'

docker compose --env-file $EnvFile -f $ComposeFile pull migrate
docker compose --env-file $EnvFile -f $ComposeFile up migrate
```

The command must exit with code 0 before API or worker rollout continues.

## Deploy API, Worker, and Web

```powershell
docker compose --env-file $EnvFile -f $ComposeFile pull api worker web prometheus grafana
docker compose --env-file $EnvFile -f $ComposeFile up -d api worker web prometheus grafana
docker compose --env-file $EnvFile -f $ComposeFile ps
```

Expected state:

- `api` is running and healthy.
- `worker` is running.
- `web` is running and healthy.
- `prometheus` is running.
- `grafana` is running.

## Run Smoke Test

Use a staging tenant and staging users that are safe for synthetic tickets:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\deployment-smoke.ps1 `
  -ApiBaseUrl 'https://supportops-staging.example.com' `
  -TenantId 'tenant_staging_smoke' `
  -AgentUserId 'user_staging_agent' `
  -LeadUserId 'user_staging_lead' `
  -SkipSeed `
  -TimeoutSeconds 180
```

The smoke test should produce a succeeded or abstained AI run, at least one saved recommendation,
one recommendation review, and cost metrics.

## Run Eval Suite

Run evals before promoting the image tag and again after staging configuration changes that affect
model routing or prompts:

```powershell
python -m supportops_evals.runner --dataset all --no-write-report
```

For hosted-provider staging evals, set `MODEL_PROVIDER=openai` and `MODEL_API_KEY` only in the
staging environment or secret manager.

## Confirm Dashboards

Check these after deploy:

```powershell
Invoke-WebRequest -Uri 'https://supportops-staging.example.com/ready' -UseBasicParsing
Invoke-WebRequest -Uri 'https://supportops-staging-prometheus.example.com/-/ready' -UseBasicParsing
Invoke-WebRequest -Uri 'https://supportops-staging-grafana.example.com/api/health' -UseBasicParsing
```

Then confirm Grafana shows the SupportOps overview dashboard with API, AI analysis, and cost panels.

## AI Rollback Control

Stage 17 adds a real `AI_ANALYSIS_ENABLED` setting so rollback can disable AI analysis without
turning off the support-ticket workflow. When the flag is false:

- `POST /tickets/{ticket_id}/ai-analysis` returns HTTP 503.
- `POST /tickets/{ticket_id}/analyze` returns HTTP 503 before queue enqueue.
- A worker that receives an already queued run marks it failed with `ai_analysis_disabled`.
- Ticket creation, ticket listing, baseline analysis, recommendation review, and metrics remain
  available.
## Rollback

Use `docs/rollback-runbook.md`. The fastest rollback for AI-specific incidents is:

```text
AI_ANALYSIS_ENABLED=false
```

Then restart `api` and `worker`. Ticket creation, listing, baseline analysis, saved recommendation
review, and manual support workflow remain available.

## Verification

Verified locally on July 21, 2026:

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
## Not Verified

- No remote VM or cloud staging deployment was executed in this workspace.
- No real hosted OpenAI staging call was run because no staging API key was provided.
- Managed database, managed Redis, TLS, DNS, and secret-manager integrations are environment-specific
  and must be configured on the chosen staging platform.

## What You Should Understand Before Stage 18

- Why staging uses pushed immutable image tags instead of local build contexts.
- Why secrets and image tags must be configurable without editing source code.
- Why rollback needs separate paths for app image, prompt version, model route, feature flag, and
  database state.
- Why the manual support workflow must survive even when AI analysis is disabled.

## Next Stage

Stage 18 should add pilot-mode controls and the improvement loop from the guide's Part 18.

## Files Added and Changed in This Stage

> This stage already documents its new files under [Files Added](#files-added) above. The list below
> is the complete added/changed set, including modified files, for consistency with the other stages.

### New files
- `infra/staging/docker-compose.staging.yml` — staging Compose using pushed image tags.
- `infra/staging/env.example` — non-secret staging config template.
- `docs/rollback-runbook.md` — exact rollback steps by failure type.
- `docs/stage-17-staging-deployment.md` (this file)

### Changed files
- `apps/api/supportops_api/settings.py` — `ai_analysis_enabled` master flag.
- `apps/api/supportops_api/routes/tickets.py` — enforce the flag on sync `/ai-analysis` and async `/analyze`.
- `apps/worker/supportops_worker/jobs.py` — mark queued run failed (`ai_analysis_disabled`) when the flag is off.
- `.gitignore` — ignore real `.env.staging`.
- `tests/deployment/` — staging Compose / env / runbook contract tests.
- `docs/architecture.md`, `docs/learning-notes.md`, `docs/progress-log.md`, `README.md` — Stage 17 updates.

> Stage-by-stage verification counts and commands live under **Stage 17** in
> [progress-log.md](progress-log.md). The cumulative map of every stage's files is in
> [file-change-log.md](file-change-log.md).
