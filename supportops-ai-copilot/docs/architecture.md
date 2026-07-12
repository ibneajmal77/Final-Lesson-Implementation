# Architecture

This project now follows the package boundaries from the technical implementation guide.

## Runtime Apps

- `apps/api`: FastAPI HTTP API.
- `apps/worker`: placeholder for future background jobs.
- `apps/web`: placeholder for future agent review UI.

## Packages

- `packages/domain`: business rules that do not depend on FastAPI.
- `packages/db`: SQLAlchemy models, repositories, and Alembic migrations.
- `packages/model_gateway`: provider-neutral model access layer.
- `packages/prompts`: future prompt templates and structured output schemas.
- `packages/evals`: future evaluation datasets, scoring, runner, and reports.
- `packages/observability`: future logging, metrics, and tracing helpers.

## Current Table Name Mapping

The guide uses conceptual names like `ai_outputs` and `approvals`.

Current implementation names:

- `ticket_recommendations` maps to the guide's `ai_outputs` concept.
- `recommendation_reviews` maps to the guide's `approvals` concept.

These names are intentionally not renamed yet. Renaming tables would require migration work and is
better done later only if exact database naming becomes important.

