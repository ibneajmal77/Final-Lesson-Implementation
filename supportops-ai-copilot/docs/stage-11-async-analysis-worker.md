# Stage 11 - Background Worker and Asynchronous AI Analysis

## Goal

Move ticket analysis from a synchronous API call into an asynchronous run lifecycle.

The API now creates an `ai_runs` row and enqueues a worker job. The worker later loads the run,
analyzes the ticket, writes a recommendation, and marks the run as complete or failed.

## Runtime Flow

```text
POST /tickets/{ticket_id}/analyze
-> validate tenant and ticket access
-> create ai_runs row with queued status
-> enqueue ai_analysis worker job
-> return HTTP 202 with run status

worker job
-> load ai_run
-> mark run running
-> load ticket
-> run deterministic baseline preview
-> call configured model gateway provider
-> write ticket_recommendations row
-> mark run succeeded, abstained, or failed

GET /tickets/{ticket_id}/analysis
-> list runs for the ticket
-> include linked recommendation when available
```

## Data Model

Stage 11 added `ai_runs`.

Important columns:

- `id`
- `tenant_id`
- `ticket_id`
- `output_recommendation_id`
- `run_type`
- `status`
- `model_provider`
- `model_name`
- `prompt_version`
- `input_hash`
- `error_code`
- `error_message`
- `created_at`
- `started_at`
- `finished_at`

Run statuses:

- `queued`
- `running`
- `succeeded`
- `failed`
- `abstained`

Current table mapping remains unchanged:

- `ticket_recommendations` still maps to the guide's `ai_outputs` concept.
- `recommendation_reviews` still maps to the guide's `approvals` concept.
- `ai_runs` now tracks the async execution lifecycle around recommendation creation.

## Queue Design

Queue code lives in:

```text
apps/worker/supportops_worker/queues.py
```

Queues defined:

- `ai_analysis`
- `evals`
- `maintenance`

The API depends on a queue adapter, not directly on RQ. That makes the API easy to test with a fake
queue while still supporting RQ at runtime.

The real adapter is `RQAnalysisQueue`. It lazily imports RQ only when a job is enqueued, so unit
tests can import the package without requiring a live Redis server or RQ worker process.

## Worker Job

Worker code lives in:

```text
apps/worker/supportops_worker/jobs.py
```

The main job is:

```text
analyze_ticket_job(ai_run_id)
```

The testable core function is:

```text
run_ticket_analysis(session, settings, ai_run_id)
```

The worker writes the recommendation through the existing recommendation repository. It also adds a
`baseline_preview` and `ai_run_id` to extracted fields so the saved recommendation can be traced
back to the async run.

## API Endpoints

New endpoints:

```text
POST /tickets/{ticket_id}/analyze
GET /tickets/{ticket_id}/analysis
```

`POST /analyze` returns HTTP 202 because the work is queued, not finished during the request.

`GET /analysis` returns all analysis runs for that ticket. If a run has completed and produced a
recommendation, the response includes the linked recommendation.

## Docker Runtime

Docker Compose now includes a `worker` service that runs:

```powershell
python -m supportops_worker.main
```

The worker listens to the `ai_analysis` queue and uses the same database, Redis, and model provider
environment configuration as the API service.

## Failure Behavior

If queue enqueue fails:

- The run is marked `failed`.
- The API returns HTTP 503.

If the worker cannot find the ticket:

- The run is marked `failed`.
- No recommendation is written.

If the model gateway raises a controlled provider error:

- The run is marked `failed`.
- `error_code` stores the exception class name.
- `error_message` stores the failure message.
- The ticket remains usable.

If the model output says it abstained:

- A recommendation can still be written.
- The run is marked `abstained`.

## Verification

Local verification:

```powershell
python -m pytest -q
python -m ruff check --no-cache .
```

Verified result:

```text
63 passed
Ruff: all checks passed
```

Docker verification still needs to be run after rebuilding with the new `rq` dependency.

## Files Added and Changed in This Stage

### New files
- `apps/worker/supportops_worker/__init__.py`
- `apps/worker/supportops_worker/main.py` — worker process entrypoint (RQ `Worker.work()`).
- `apps/worker/supportops_worker/queues.py` — `AnalysisQueue` protocol + `RQAnalysisQueue`.
- `apps/worker/supportops_worker/jobs.py` — `analyze_ticket_job` / `run_ticket_analysis`.
- `packages/db/supportops_db/repositories/ai_runs.py` — create/list/state-transition helpers.
- `packages/db/supportops_db/migrations/versions/0005_create_ai_runs.py`
- `tests/worker/test_jobs.py`, `tests/api/` fake-queue tests.
- `docs/stage-11-async-analysis-worker.md` (this file)

### Changed files
- `packages/db/supportops_db/models.py` — added the `AIRun` model / `ai_runs` table.
- `apps/api/supportops_api/routes/tickets.py` — `POST /analyze` (202) and `GET /analysis`.
- `apps/api/supportops_api/dependencies.py` — `get_ai_analysis_queue` injected dependency.
- `apps/api/supportops_api/schemas/ai.py` — `AIAnalysisRunRead`.
- `docker-compose.yml` — added the `worker` service.
- `requirements.txt` — added `rq` runtime dependency.
- `docs/progress-log.md`, `README.md`, `docs/architecture.md`, `docs/data-model.md` — Stage 11 updates.

> Stage-by-stage verification counts and commands live under **Stage 11** in
> [progress-log.md](progress-log.md). The cumulative map of every stage's files is in
> [file-change-log.md](file-change-log.md).
