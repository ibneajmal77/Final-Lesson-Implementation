# Learning Notes

Use this file to write short notes as you build.

## Stage 1 - API Foundation

Answer these after running the first API:

1. What does FastAPI do in this project?
2. What is the difference between `/health` and `/ready`?
3. Why do we keep settings in environment variables?
4. What did a test catch or prove?

## Stage 2 - Real Readiness Checks

Answer these after running `/ready` through Docker:

1. Why does `/ready` return 503 when a dependency is unavailable?
2. Why does the API use `postgres` and `redis` as hostnames inside Docker?
3. What is the difference between checking that a URL exists and checking that a service responds?
4. Why do the unit tests mock Postgres and Redis instead of requiring Docker?

## Stage 3 - Database Models and Migrations

Answer these after running the first Alembic migration:

1. What is the difference between a SQLAlchemy model and a real database table?
2. Why do we need Alembic migrations instead of manually creating tables?
3. Why does every tenant-owned table need `tenant_id`?
4. Why is `tickets(tenant_id, external_id)` unique instead of just `external_id`?
5. What would break if two tenants could see each other's tickets?

## Stage 4 - Tenant-Scoped Ticket APIs

Answer these after creating and listing tickets:

1. Why does every ticket API require `X-Tenant-Id`?
2. Why do repository queries filter by both `tenant_id` and `ticket_id`?
3. Why does duplicate `external_id` return the existing ticket instead of creating another row?
4. What is the difference between a Pydantic schema and a SQLAlchemy model?
5. Why do tests use an in-memory SQLite database instead of the Docker Postgres database?

## Stage 5 - Baseline Ticket Classifier

Answer these after creating a baseline analysis:

1. Why do we build a deterministic baseline before calling an LLM?
2. Why is the classifier in `packages/domain` instead of inside the FastAPI route?
3. Why are recommendations stored in a separate table instead of updating the ticket directly?
4. What extracted fields did the baseline find from your test ticket?
5. What ticket text would make the baseline assign `urgent` priority?
6. What are two weaknesses of keyword-based classification that an LLM may improve later?

## Stage 6 - Mock LLM Provider Abstraction

Answer these after creating an AI analysis:

1. Why do we create a provider interface before connecting a real model API?
2. What fields does the mock provider return that the baseline does not naturally produce?
3. Why do we store `model_name` and `prompt_version` with each recommendation?
4. Why should a suggested reply be saved for review instead of sent automatically?
5. What would need to change when replacing the mock provider with a real provider?
6. What failure should the API return if `MODEL_PROVIDER` is unsupported?

## Stage 7 - Human Approval Workflow

Answer these after approving, editing, and rejecting recommendations:

1. Why do we store review events instead of overwriting the recommendation?
2. What final content is stored when a recommendation is approved?
3. What final content is stored when a recommendation is rejected?
4. Why does an `edited` decision require edited summary or reply content?
5. Why do review endpoints still filter by tenant, ticket, and recommendation?
6. What business metric could we calculate from approved, rejected, and edited counts?

## Stage 8 - Review Metrics and Evaluation Feedback

Answer these after calling `/metrics/reviews`:

1. What is the difference between total recommendations and reviewed recommendations?
2. What does review coverage rate tell you?
3. Why is approval rate useful before connecting a real LLM?
4. What does a high edit rate suggest about the generated reply?
5. Why do we break metrics down by source?
6. Why do we break metrics down by category?
7. How could these metrics help compare baseline, mock LLM, and future real LLM output?

## Stage 8.5 - Guide-Aligned Structure Realignment

Answer these after reviewing the folder structure:

1. Why should model provider code live outside the API route layer?
2. Why should prompt templates live in their own package?
3. Why do approval schemas belong outside ticket schemas?
4. Why did we keep database table names unchanged during this refactor?
5. What future code belongs in `packages/evals`?
6. What future code belongs in `packages/observability`?

## Stage 9 - Prompt Contract and Structured Output Design

Answer these after reviewing `packages/prompts`:

1. Why should LLM output be parsed with Pydantic before it is saved?
2. Why do unknown categories fail unless the model returns `other`?
3. Why must confidence scores be constrained between `0` and `1`?
4. Why does each prompt include an untrusted ticket text boundary?
5. What is the purpose of a prompt changelog?
6. What should happen in Stage 10 if a real model returns malformed JSON?

## Stage 10 - Real Hosted LLM Provider Integration

Answer these after running hosted analysis with a real API key:

1. Why does the hosted provider live in `packages/model_gateway` instead of the FastAPI route?
2. Why is `MODEL_PROVIDER=mock` still the default?
3. Why should `MODEL_API_KEY` come from the environment and never be committed?
4. What does strict structured output add beyond asking the model to return JSON?
5. Why does the API validate the model output with Pydantic after the provider returns it?
6. What should happen if the hosted model returns malformed JSON or schema-invalid output?
7. Why do we store the prompt version and model name with every saved recommendation?

## Stage 11 - Background Worker and Asynchronous AI Analysis

Answer these after queueing and processing an async analysis run:

1. Why does `POST /tickets/{ticket_id}/analyze` return HTTP 202 instead of HTTP 201?
2. Why does the API create an `ai_runs` row before enqueueing the worker job?
3. What is the difference between `queued`, `running`, `succeeded`, `failed`, and `abstained`?
4. Why should worker failures update run status instead of only failing silently in Redis?
5. Why do tests override the queue dependency instead of requiring Redis and RQ?
6. Why does the worker write a recommendation instead of changing the ticket priority directly?
7. How does `GET /tickets/{ticket_id}/analysis` help an agent understand async progress?
## Stage 12 - Evaluation Harness and Quality Gates

Answer these after running the eval runner:

1. Why do eval datasets use labelled JSONL cases instead of ad hoc manual prompts?
2. What is the difference between golden, difficult, and safety eval cases?
3. Why should invalid structured output fail a release gate?
4. Why is unsupported claim rate tracked separately from category accuracy?
5. Why does the mock provider remain useful for offline eval harness tests?
6. What does `--dataset all` add beyond running one dataset at a time?
7. What would need to change before using live hosted-provider evals as a release gate?
## Stage 13 - Observability and Cost Tracking

Answer these after calling `/metrics/runtime` and `/metrics/costs`:

1. Why should logs include identifiers like `request_id`, `ticket_id`, and `ai_run_id`?
2. Why should ticket bodies, prompts, and API keys be excluded from production logs?
3. What is the difference between process-local Prometheus metrics and persisted `cost_events`?
4. Why does cost estimation use configurable token rates instead of hardcoded model pricing?
5. How does `cost_events` connect a model call back to a tenant, ticket, async run, and recommendation?
6. Why do API and worker paths both need to record model usage?
7. What external service would be needed before OpenTelemetry spans become visible outside the process?
## Stage 14 - Security Implementation

Answer these after reviewing the security tests and threat model:

1. Why should cross-tenant access return `404` instead of saying another tenant owns the row?
2. Why does support policy creation require `lead` or `admin` instead of any agent role?
3. Why must customer ticket text be marked as untrusted inside prompts?
4. Why should model output be prevented from choosing tools or permissions?
5. Why do hosted-provider evidence IDs need an allowlist?
6. What kinds of PII and secrets does `redact_for_logs` mask?
7. Why does the retention job count expired rows before implementing destructive deletion?
8. What sensitive data is sent to the hosted model provider when it is enabled?
## Stage 15 - CI/CD

Answer these after reviewing the GitHub Actions workflow:

1. Why should lint, typecheck, unit tests, integration tests, migrations, evals, and Docker build be separate jobs?
2. Why does CI use `MODEL_PROVIDER=mock` instead of a hosted model API key?
3. Why should integration tests require explicit PostgreSQL and Redis service containers?
4. What does `python -m alembic check` catch that `python -m alembic upgrade head` does not?
5. Why is branch protection still needed after adding `.github/workflows/ci.yml`?
6. What failure should block a pull request before a human reviews the code?
## Stage 16 - Local Production-Like Deployment

Answer these after running the full Docker stack and smoke test:

1. Why does the `migrate` service run before `api` and `worker` start?
2. What does a healthy Compose stack prove that unit tests do not prove?
3. Why does the web console need CORS configuration from the API?
4. Why should the smoke test create a real ticket instead of only checking `/health`?
5. How does the smoke test prove that Redis, the worker, and PostgreSQL are wired together?
6. Why are Prometheus and Grafana useful before deploying to staging?
7. What would you check first if the smoke test queued an AI run but it never completed?
## Stage 17 - Staging Deployment and Rollback Runbook

Answer these after reading the staging deployment guide and rollback runbook:

1. Why does staging use pushed image tags instead of local Docker build contexts?
2. Why should real staging secrets live outside the repository?
3. Why does rollback separate app image, prompt version, model route, feature flag, and database state?
4. What user workflow must keep working when `AI_ANALYSIS_ENABLED=false`?
5. Why is database rollback treated differently from app image rollback?
6. What should the smoke test prove after a rollback?
7. What information should be recorded in the deployment channel after rollback finishes?

## Stage 18 - Pilot Mode and Improvement Loop

Answer these after reviewing pilot metrics and feedback candidates:

1. Why should pilot rollout be restricted by tenant and category instead of enabling every ticket at once?
2. Why must the worker enforce the same pilot gate as the API?
3. What does draft acceptance rate measure that review coverage does not?
4. Why is edit distance useful but not enough to judge draft quality by itself?
5. What rejection reasons should become difficult eval cases?
6. Why should prompt or model route changes ship only after eval gates pass?
7. When would you expand, iterate, roll back, or stop a pilot?