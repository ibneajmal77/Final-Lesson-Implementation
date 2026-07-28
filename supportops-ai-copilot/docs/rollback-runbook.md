# Rollback Runbook

Purpose: restore a safe staging state when a deployment, prompt, model route, or AI-analysis path
causes failures. This runbook prioritizes keeping the manual support workflow available.

Scope: staging deployment for SupportOps AI Copilot. Production rollback would need the same shape
plus production approval, customer communication, and backup/restore controls.

## Required Inputs

Before rollback, identify these values:

```powershell
$EnvFile = 'infra/staging/.env.staging'
$ComposeFile = 'infra/staging/docker-compose.staging.yml'
$StagingApiBaseUrl = 'https://supportops-staging.example.com'
$LastGoodApiImage = 'ghcr.io/OWNER/supportops-ai-copilot-api:LAST_GOOD_SHA'
$LastGoodWebImage = 'ghcr.io/OWNER/supportops-ai-copilot-web:LAST_GOOD_SHA'
```

Also record:

- Current deployed API image tag.
- Current deployed web image tag.
- Current Alembic revision before rollback.
- Last known good prompt version.
- Last known good `MODEL_PROVIDER`, `MODEL_NAME`, and model cost-rate settings.
- Whether `AI_ANALYSIS_ENABLED` is currently `true` or `false`.

## 1. Freeze New Deployments

1. Stop any in-progress deploy job.
2. Announce rollback in the deployment channel.
3. Assign one person to run commands and one person to verify smoke checks.
4. Do not run another migration until the database state is understood.

## 2. Capture Current State

Run these before changing anything:

```powershell
docker compose --env-file $EnvFile -f $ComposeFile ps
docker compose --env-file $EnvFile -f $ComposeFile logs --tail 200 api worker web
Invoke-WebRequest -Uri "$StagingApiBaseUrl/ready" -UseBasicParsing
```

If Grafana or Prometheus is reachable, capture the current error-rate, latency, and cost panels.

## 3. Fast AI Kill Switch

Use this first when model output, model latency, model cost, prompt behavior, or queue processing is
unsafe but ticket intake still needs to work.

Set this in the staging secret manager or `infra/staging/.env.staging`:

```text
AI_ANALYSIS_ENABLED=false
```

Restart API and worker so both processes load the flag:

```powershell
docker compose --env-file $EnvFile -f $ComposeFile up -d api worker
docker compose --env-file $EnvFile -f $ComposeFile ps
```

Expected behavior:

- `POST /tickets/{ticket_id}/ai-analysis` returns 503 with `ai analysis is disabled`.
- `POST /tickets/{ticket_id}/analyze` returns 503 with `ai analysis is disabled`.
- A worker that receives a queued run while disabled marks it failed with `ai_analysis_disabled`.
- Ticket creation, ticket listing, baseline analysis, recommendation listing, review creation, and
  review metrics stay available.

If queued jobs must stop immediately, scale the worker to zero:

```powershell
docker compose --env-file $EnvFile -f $ComposeFile up -d --scale worker=0 worker
```

## 4. Revert App Image

Use this when the API, worker, or web image introduced the failure.

Update image tags in the staging secret manager or `infra/staging/.env.staging`:

```text
SUPPORTOPS_API_IMAGE=ghcr.io/OWNER/supportops-ai-copilot-api:LAST_GOOD_SHA
SUPPORTOPS_WEB_IMAGE=ghcr.io/OWNER/supportops-ai-copilot-web:LAST_GOOD_SHA
```

Pull and restart the app services:

```powershell
docker compose --env-file $EnvFile -f $ComposeFile pull api worker web
docker compose --env-file $EnvFile -f $ComposeFile up -d api worker web
docker compose --env-file $EnvFile -f $ComposeFile ps
```

Verify:

```powershell
Invoke-WebRequest -Uri "$StagingApiBaseUrl/ready" -UseBasicParsing
powershell -ExecutionPolicy Bypass -File scripts\deployment-smoke.ps1 `
  -ApiBaseUrl $StagingApiBaseUrl `
  -TenantId 'tenant_staging_smoke' `
  -AgentUserId 'user_staging_agent' `
  -LeadUserId 'user_staging_lead' `
  -SkipSeed `
  -TimeoutSeconds 180
```

## 5. Revert Prompt Version

Current implementation bundles prompt templates and the prompt registry into the API image. For the
current build, prompt rollback is therefore an app image rollback to the last known good API image.

Run the app image rollback steps in section 4 with the API image that contains the last known good
prompt version.

If a future stage externalizes prompt routing through a setting such as `PROMPT_VERSION`, set that
setting back to the last known good prompt version, restart `api` and `worker`, then run the smoke
and eval checks.

## 6. Revert Model Route

Use this when the image is healthy but the hosted model provider, model name, base URL, or cost-rate
configuration is unsafe.

Set these in the staging secret manager or `infra/staging/.env.staging`:

```text
MODEL_PROVIDER=mock
MODEL_API_KEY=
MODEL_INPUT_COST_PER_1K_TOKENS=0
MODEL_OUTPUT_COST_PER_1K_TOKENS=0
```

Then restart API and worker:

```powershell
docker compose --env-file $EnvFile -f $ComposeFile up -d api worker
```

Verify with:

```powershell
python -m supportops_evals.runner --dataset all --no-write-report
powershell -ExecutionPolicy Bypass -File scripts\deployment-smoke.ps1 `
  -ApiBaseUrl $StagingApiBaseUrl `
  -TenantId 'tenant_staging_smoke' `
  -AgentUserId 'user_staging_agent' `
  -LeadUserId 'user_staging_lead' `
  -SkipSeed `
  -TimeoutSeconds 180
```

## 7. Database Migration Rollback Decision

Default rule: do not run destructive database rollback commands automatically.

If the migration failed before completion, keep the previous app version running and fix the failed
migration before retrying.

If the migration completed and the new app is broken, first revert the app image. Migrations should
be backward compatible for this project stage.

If the migration is not backward compatible and staging must be restored:

1. Stop API and worker:

```powershell
docker compose --env-file $EnvFile -f $ComposeFile stop api worker
```

2. Restore the managed database or VM database from the snapshot taken immediately before migration.
3. Set `SUPPORTOPS_API_IMAGE` and `SUPPORTOPS_WEB_IMAGE` to the last known good tags.
4. Start services:

```powershell
docker compose --env-file $EnvFile -f $ComposeFile up -d api worker web prometheus grafana
```

5. Run smoke and dashboard checks.

## 8. Keep Manual Support Workflow Working

After any rollback path, verify these manually or with API calls:

- `POST /tickets` creates a ticket.
- `GET /tickets` lists tickets.
- `POST /tickets/{ticket_id}/baseline-analysis` still works.
- `GET /tickets/{ticket_id}/recommendations` still works for existing recommendations.
- `POST /tickets/{ticket_id}/recommendations/{recommendation_id}/reviews` still stores a review.
- `GET /metrics/reviews` still returns tenant metrics.

If AI analysis remains disabled, tell agents to use baseline analysis and manual drafting until the
incident is resolved.

## 9. Rollback Exit Criteria

Rollback is complete when:

- `/ready` returns 200.
- Web health returns 200.
- Smoke test passes or AI is intentionally disabled and the manual workflow checks pass.
- Prometheus is ready.
- Grafana health returns 200.
- Error rate and latency return to expected staging levels.
- The deployment channel has the final image tags, model route, prompt version, and feature-flag
  state.

## 10. Post-Rollback Follow-Up

1. Open an incident note with the failed image tag and rollback image tag.
2. Add a representative failure to the eval dataset if model or prompt behavior caused the rollback.
3. Add or update an automated test for the failed path.
4. Keep `AI_ANALYSIS_ENABLED=false` until the fix passes tests, evals, smoke, and dashboard checks.
