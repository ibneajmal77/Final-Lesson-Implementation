# Stage 18 - Pilot and Improvement Loop

Status: implemented locally.

## Guide Mapping

This stage implements Part 18 of the technical guide:

- Stage 18.1: pilot mode.
- Stage 18.2: feedback-to-eval loop.

## Pilot Scope

AI analysis still has the global kill switch from Stage 17:

```text
AI_ANALYSIS_ENABLED=false
```

Stage 18 adds two narrower controls:

```text
AI_ANALYSIS_ENABLED_TENANTS=tenant_demo
AI_ANALYSIS_ENABLED_CATEGORIES=billing
```

Empty allowlists mean no tenant or category restriction. The local Docker stack and staging template start with the demo tenant and the billing category so the pilot begins with duplicate-charge/refund style tickets.

## Enforcement

Synchronous AI analysis uses this gate before calling the provider:

```text
POST /tickets/{ticket_id}/ai-analysis
-> tenant exists
-> ticket belongs to tenant
-> baseline category is detected
-> global, tenant, and category pilot gates pass
-> provider is called
```

Asynchronous AI analysis uses the same gate before enqueueing:

```text
POST /tickets/{ticket_id}/analyze
-> tenant exists
-> ticket belongs to tenant
-> baseline category is detected
-> pilot gates pass
-> ai_runs row is created and queued
```

The worker also checks the same gate after it loads the queued ticket. If the pilot scope changes while a job is waiting, the worker marks the run failed with one of these error codes:

- `ai_analysis_disabled`
- `ai_analysis_tenant_not_enabled`
- `ai_analysis_category_not_enabled`

## Pilot Metrics

`GET /metrics/pilot` returns tenant-scoped pilot metrics for non-baseline AI drafts:

- Draft acceptance rate.
- Average edit distance.
- Time to first response.
- Escalation accuracy.
- Cost per accepted draft.
- Safety failures.
- Agent rejection reasons.
- Exit decision: `expand`, `iterate`, `roll_back`, or `stop`.

The initial exit decision is conservative. Fewer than five reviewed pilot drafts returns `iterate` because there is not enough signal to expand safely.

## Feedback-to-Eval Loop

`GET /metrics/pilot/feedback` returns rejected drafts and heavily edited drafts. Use it weekly:

1. Pull rejected drafts.
2. Pull heavily edited drafts.
3. Cluster failure reasons.
4. Add representative failures to `packages/evals/supportops_evals/datasets/difficult_cases.jsonl`.
5. Update the prompt or model route.
6. Run evals.
7. Release only if gates pass.

## Verification

Stage 18 adds tests for:

- Tenant allowlist blocking synchronous AI analysis.
- Category allowlist blocking async enqueue.
- Worker-side category gate enforcement.
- Pilot metrics for accepted drafts.
- Feedback candidates for rejected drafts.

## Files Added and Changed in This Stage

### New files
- `apps/api/supportops_api/pilot.py` — shared `ai_analysis_eligibility` gate (tenant + category).
- `packages/db/supportops_db/repositories/pilot.py` — pilot metrics + feedback-candidate queries.
- `docs/stage-18-pilot-improvement-loop.md` (this file)
- `docs/pilot-report.md`
- `docs/feedback-to-eval-loop.md`

### Changed files
- `apps/api/supportops_api/settings.py` — `ai_analysis_enabled_tenants`, `ai_analysis_enabled_categories`.
- `apps/api/supportops_api/routes/tickets.py` — call the pilot gate before sync analysis and enqueue.
- `apps/api/supportops_api/routes/metrics.py` — `GET /metrics/pilot`, `GET /metrics/pilot/feedback`.
- `apps/api/supportops_api/schemas/metrics.py` — pilot report / feedback schemas.
- `apps/worker/supportops_worker/jobs.py` — re-check the pilot gate after dequeue.
- `apps/web/src/app.js` — pilot metrics + feedback panel.
- `docker-compose.yml`, `infra/staging/env.example` — default pilot scope (`tenant_demo`, `billing`).
- `packages/evals/supportops_evals/datasets/difficult_cases.jsonl` — target for mined feedback cases.
- `docs/api-contracts.md`, `docs/architecture.md`, `docs/learning-notes.md`, `docs/progress-log.md`, `README.md` — Stage 18 updates.

> Stage-by-stage verification counts and commands live under **Stage 18** in
> [progress-log.md](progress-log.md). The cumulative map of every stage's files is in
> [file-change-log.md](file-change-log.md).