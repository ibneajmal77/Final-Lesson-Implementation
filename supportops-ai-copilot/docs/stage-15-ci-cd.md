# Stage 15 - CI/CD

## Guide Mapping

The technical implementation guide lists this work as `Part 16 - CI/CD`, `Stage 16.1 - GitHub
Actions`. In this project log it is Stage 15 because earlier stages included the guide-aligned
structure realignment as Stage 8.5.

## Goal

Add pull-request gates that run the same checks used locally:

- dependency installation
- Ruff linting
- type checking
- unit tests
- integration tests with PostgreSQL and Redis
- Alembic migration checks
- offline eval smoke tests with the mock provider
- Docker image build

## Workflow

The workflow lives at:

```text
.github/workflows/ci.yml
```

It runs on:

- pull requests
- pushes to `main`

Jobs:

- `lint`: installs dependencies and runs Ruff.
- `typecheck`: installs dependencies and runs mypy over `apps` and `packages`.
- `test`: runs unit tests while excluding external dependency integration tests.
- `integration`: starts PostgreSQL and Redis service containers, then runs integration tests.
- `migrations`: starts PostgreSQL, applies Alembic migrations to head, and checks schema drift.
- `eval-smoke`: runs the mock-provider evaluation gate without writing a report.
- `docker-build`: builds the API image from `Dockerfile.api`.

## Type Checking

Stage 15 adds `mypy` to development requirements and configures mypy in `pyproject.toml`.

Local command:

```powershell
python -m mypy apps packages
```

The command intentionally checks the real app and package roots, not the repo-root
`supportops_evals` import shim. The shim exists so `python -m supportops_evals.runner` works from a
source checkout.

## Integration Tests

Integration tests live in:

```text
tests/integration
```

They are skipped by default during local pytest runs. To run them manually, start PostgreSQL and
Redis first, then set:

```powershell
$env:RUN_INTEGRATION_TESTS = '1'
$env:DATABASE_URL = 'postgresql://supportops:supportops@localhost:5432/supportops'
$env:REDIS_URL = 'redis://localhost:6379/0'
python -m pytest -q tests/integration
```

In GitHub Actions, the `integration` job provides PostgreSQL and Redis as service containers and sets
those variables automatically.

## Migration Check

The CI `migrations` job runs:

```powershell
python -m alembic upgrade head
python -m alembic check
```

This proves a clean database can migrate to the current schema and that model metadata does not have
uncommitted migration drift.

## Eval Smoke

The CI `eval-smoke` job runs:

```powershell
python -m supportops_evals.runner --dataset all --no-write-report
```

The mock provider keeps this deterministic and safe for pull requests without hosted model secrets.

## Docker Build

The CI `docker-build` job runs:

```powershell
docker build -f Dockerfile.api -t supportops-ai-copilot-api:ci .
```

It verifies the API image can be built from checked-in files and pinned requirements.

## Branch Protection

The workflow runs the required checks, but GitHub branch protection must still be enabled in the
repository settings to make pull requests unmergeable when any required job fails.

Recommended required jobs:

- `lint`
- `typecheck`
- `test`
- `integration`
- `migrations`
- `eval-smoke`
- `docker-build`

## Verification

Local verification commands:

```powershell
python -m ruff check --no-cache .
python -m mypy apps packages
python -m pytest -q
python -m supportops_evals.runner --dataset all --no-write-report
docker compose config
docker build -f Dockerfile.api -t supportops-ai-copilot-api:ci .
git diff --check
```

The external integration test is skipped locally unless `RUN_INTEGRATION_TESTS=1` is set. The Alembic migration gate was also smoke-tested locally against a temporary SQLite database; CI runs it against PostgreSQL.

## Files Added and Changed in This Stage

### New files
- `.github/workflows/ci.yml` — seven parallel jobs (lint, typecheck, test, integration, migrations, eval-smoke, docker-build).
- `tests/integration/` — PostgreSQL/Redis readiness tests (opt-in via `RUN_INTEGRATION_TESTS=1`).
- `tests/` CI-contract tests asserting required jobs/commands are present.
- `docs/stage-15-ci-cd.md` (this file)

### Changed files
- `pyproject.toml` — mypy configuration for `apps` and `packages`.
- `requirements-dev.txt` — pinned `mypy`.
- `packages/observability/supportops_observability/metrics.py` — small typing fixes.
- `packages/db/supportops_db/repositories/cost_events.py` — aggregation typing fixes.
- `apps/worker/supportops_worker/retention.py` — typing fixes.
- `apps/api/supportops_api/routes/approvals.py` — response-mapping typing fixes.
- `apps/worker/supportops_worker/queues.py` — RQ import typing fixes.
- `docs/architecture.md` — CI/CD flow.
- `docs/progress-log.md`, `README.md` — Stage 15 updates.

> Stage-by-stage verification counts and commands live under **Stage 15** in
> [progress-log.md](progress-log.md). The cumulative map of every stage's files is in
> [file-change-log.md](file-change-log.md).
