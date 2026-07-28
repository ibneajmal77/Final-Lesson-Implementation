# Stage 13 - Observability and Cost Tracking

## Goal

Add basic production observability around the AI ticket workflow.

Stage 13 adds structured JSON logs, process-level Prometheus text metrics, OpenTelemetry span
helpers, and durable `cost_events` rows that connect model usage back to tenants, tickets, async
runs, and recommendations.

## Structured Logs

Logging helpers live in:

```text
packages/observability/supportops_observability/logging.py
```

The API configures JSON logging during app creation, and the worker configures the same formatter at
startup. Request middleware adds a request id to every response through `X-Request-Id`.

Log context supports:

- `request_id`
- `tenant_id`
- `user_id`
- `ticket_id`
- `ai_run_id`
- `job_id`
- `route`
- `error_code`

Rules followed in this stage:

- Ticket body is not logged by default.
- Model API keys are never logged.
- Full prompts are not logged.

## Runtime Metrics

Metrics helpers live in:

```text
packages/observability/supportops_observability/metrics.py
```

The API exposes process-local Prometheus text at:

```text
GET /metrics/runtime
```

Implemented metric names:

- `tickets_created_total`
- `ai_analysis_started_total`
- `ai_analysis_succeeded_total`
- `ai_analysis_failed_total`
- `ai_analysis_latency_seconds`
- `model_gateway_latency_seconds`
- `model_tokens_total`
- `model_cost_usd_total`
- `draft_approved_total`
- `draft_rejected_total`
- `draft_escalated_total`
- `eval_regression_total`
- `prompt_injection_failures_total`

The implementation renders Prometheus-compatible text directly and also lists `prometheus-client` in
runtime requirements for deployments that later want a standard collector registry.

## Cost Events

Stage 13 adds:

```text
packages/db/supportops_db/repositories/cost_events.py
packages/db/supportops_db/migrations/versions/0006_create_cost_events.py
```

New table:

```text
cost_events
```

Important columns:

- `id`
- `tenant_id`
- `ticket_id`
- `ai_run_id`
- `recommendation_id`
- `provider`
- `model`
- `prompt_version`
- `operation`
- `input_tokens`
- `output_tokens`
- `estimated_cost_usd`
- `latency_ms`
- `metadata_json`
- `created_at`

Synchronous `/tickets/{ticket_id}/ai-analysis` and async worker analysis both write a cost event
when they create a recommendation.

Cost estimation is intentionally configuration-driven:

```text
MODEL_INPUT_COST_PER_1K_TOKENS
MODEL_OUTPUT_COST_PER_1K_TOKENS
```

Both default to `0.0`. This avoids hardcoding hosted-model pricing in source code.

## Tenant Cost Endpoint

The API exposes tenant-scoped cost aggregation at:

```text
GET /metrics/costs
```

The response includes:

- total events
- input and output tokens
- estimated cost
- average latency
- accepted draft count
- cost per accepted draft
- breakdown by provider
- breakdown by model

## Tracing

Tracing helpers live in:

```text
packages/observability/supportops_observability/tracing.py
```

Current spans cover:

- API request middleware.
- Ticket creation DB write.
- Baseline analysis.
- Synchronous AI analysis.
- Queue enqueue.
- Worker AI analysis.
- Model gateway calls.
- Approval actions.

No exporter is configured yet, so spans are ready for the next deployment/observability deepening
without requiring an external collector during local tests.

## Verification

Local verification:

```powershell
python -m pytest -q
python -m ruff check --no-cache .
python -m supportops_evals.runner --dataset all --no-write-report
```

Verified result:

```text
80 passed
Ruff: all checks passed
All evaluation datasets pass release gates
```

Not verified yet:

- A live hosted-provider cost run was not executed because no model API key was provided.
- Prometheus scraping and OpenTelemetry export were not run against external collector services.
- Docker rebuild was not run after adding observability dependencies.

## Files Added and Changed in This Stage

### New files
- `packages/observability/supportops_observability/__init__.py`
- `packages/observability/supportops_observability/logging.py` — JSON logs + `log_context`.
- `packages/observability/supportops_observability/metrics.py` — in-memory registry + Prometheus text.
- `packages/observability/supportops_observability/tracing.py` — optional OpenTelemetry spans.
- `packages/observability/supportops_observability/model_usage.py` — writes `cost_events`.
- `packages/db/supportops_db/repositories/cost_events.py` — cost writes + tenant aggregation.
- `packages/db/supportops_db/migrations/versions/0006_create_cost_events.py`
- `packages/model_gateway/supportops_model_gateway/cost.py` — token→USD estimator.
- `docs/stage-13-observability-cost.md` (this file)

### Changed files
- `packages/db/supportops_db/models.py` — added `CostEvent` / `cost_events` table.
- `apps/api/supportops_api/main.py` — observability middleware, `X-Request-Id`.
- `apps/api/supportops_api/routes/metrics.py` — `GET /metrics/runtime`, `GET /metrics/costs`.
- `apps/api/supportops_api/schemas/metrics.py` — cost response schemas.
- `apps/api/supportops_api/settings.py` — `MODEL_INPUT/OUTPUT_COST_PER_1K_TOKENS`.
- `apps/api/supportops_api/routes/tickets.py` — cost recording, spans, structured logs.
- `apps/worker/supportops_worker/jobs.py` — cost recording, spans, logs.
- `apps/worker/supportops_worker/main.py` — JSON logging at startup.
- `requirements.txt` — `prometheus-client`, `opentelemetry-api`, `opentelemetry-sdk`.
- `docker-compose.yml` — cost-rate environment variables.
- `docs/cost-report.md`, `docs/progress-log.md`, `README.md`, `docs/architecture.md` — Stage 13 updates.

> Stage-by-stage verification counts and commands live under **Stage 13** in
> [progress-log.md](progress-log.md). The cumulative map of every stage's files is in
> [file-change-log.md](file-change-log.md).
