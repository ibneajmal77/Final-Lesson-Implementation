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
