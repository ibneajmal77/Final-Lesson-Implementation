# ============================================================================
# FILE: tests/ci/test_github_actions.py
#
# THINK OF THIS FILE AS: an inspection checklist for the automated gatekeeper.
#
# WHAT THIS TESTS: that .github/workflows/ci.yml still names every required
# GitHub Actions job, runs the commands that protect the project, and starts on
# both pull requests and pushes.
#
# "CI" means CONTINUOUS INTEGRATION: a remote service checks each proposed
# change automatically. A "workflow" is the YAML file describing those checks.
# YAML is a human-readable configuration format where indentation gives entries
# their structure, much as indentation gives Python blocks their structure.
#
# WHERE THIS SITS IN THE DELIVERY FLOW:
#   a developer pushes code or opens a pull request
#     -> GitHub reads .github/workflows/ci.yml
#       -> its seven jobs lint, type-check, test, evaluate, and build the project
#         -> a failed job blocks the change from being treated as safe to merge
#
# TESTING APPROACH: these are fast CONTRACT tests. A contract test checks that
# two parts still agree about their shared interface. Here the interface is the
# set of job names, commands, and triggers this repository promises CI will use.
# The tests read the workflow as plain text; they do not contact GitHub or run
# the jobs.
#
# HONEST LIMITATION: finding text is weaker than parsing and executing YAML. A
# required phrase could exist in a comment or the wrong section and still pass.
# GitHub's real workflow run remains the definitive proof that the configuration
# is valid and the commands succeed.
#
# No pytest FIXTURE is needed. A fixture is reusable setup supplied to a test;
# these tests need only the committed workflow file and Python's Path helper.
#
# WHO USES IT / WHAT LIVES HERE: .github/workflows/ci.yml is the file inspected;
# pyproject.toml configures Ruff and mypy; packages/evals/supportops_evals/runner.py
# implements the AI quality command; Dockerfile.api and Dockerfile.web are the
# two images the final CI job builds.
# ============================================================================
from pathlib import Path

# One shared path avoids five spellings of the workflow location drifting apart.
# Path is Python's operating-system-aware way to represent a file location.
WORKFLOW_PATH = Path(".github/workflows/ci.yml")


# The smallest guard: fail clearly if the workflow is deleted or moved.
#
# This does not say whether the contents are useful. The next three tests add
# that meaning one layer at a time.
def test_ci_workflow_exists() -> None:
    assert WORKFLOW_PATH.exists()


# Job names are the top-level tasks under "jobs:" in .github/workflows/ci.yml.
# Each protects against a different kind of release failure, so accidentally
# dropping one should fail the ordinary Python test suite immediately.
def test_ci_workflow_runs_required_jobs() -> None:
    # UTF-8 is named explicitly so every operating system decodes the file the same
    # way instead of relying on a machine-specific default.
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

    # This is a TABLE-DRIVEN assertion: one loop applies the same rule to every
    # required job. Adding a job to the contract means adding one string, not
    # copying another test function.
    for job_name in (
        # Static checks that catch style errors and incompatible type annotations.
        "lint",
        "typecheck",
        # Fast unit tests and slower tests backed by real Postgres and Redis services.
        "test",
        "integration",
        # Database-history consistency and deterministic AI-quality regression checks.
        "migrations",
        "eval-smoke",
        # Packaging check: both deployable container images must still build.
        "docker-build",
    ):
        # The two leading spaces and trailing colon match a YAML mapping key at the
        # workflow's normal job indentation. This is deliberately a narrow text check,
        # not proof that the key is under "jobs:" or that the job itself is valid.
        assert f"  {job_name}:" in workflow


# A job label alone is not enough: a job named "test" could silently stop
# running pytest. These exact strings pin the useful work each gate must do.
def test_ci_workflow_runs_project_gates() -> None:
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

    required_commands = (
        # Ruff is the linter: it reports common mistakes and enforces agreed style.
        "python -m ruff check --no-cache .",
        # Mypy checks whether values match the Python type annotations in app code.
        "python -m mypy apps packages",
        # Unit tests stay fast by excluding the real-service integration directory.
        "python -m pytest -q tests --ignore=tests/integration",
        # The integration job runs that directory separately with Postgres and Redis.
        "python -m pytest -q tests/integration",
        # A MIGRATION is a numbered, repeatable database-schema change. "upgrade head"
        # applies the whole Alembic migration chain through its newest revision.
        "python -m alembic upgrade head",
        # "alembic check" catches drift between supportops_db/models.py and that chain.
        "python -m alembic check",
        # The eval runner scores fixed AI examples and exits non-zero if a gate regresses.
        "python -m supportops_evals.runner --dataset all --no-write-report",
        # Compose validation reads docker-compose.yml without starting the stack.
        "docker compose config",
        # These commands prove both deployable Docker images can be assembled.
        "docker build -f Dockerfile.api -t supportops-ai-copilot-api:ci .",
        "docker build -f Dockerfile.web -t supportops-ai-copilot-web:ci .",
    )
    # Exact containment is intentional: replacing a gate with a weaker command
    # should require an explicit update to this test, making the policy change visible.
    for command in required_commands:
        assert command in workflow


# CI must protect proposed changes before merge and also verify the main branch
# after changes land. The "on:" section of ci.yml declares those two triggers.
def test_ci_workflow_runs_on_pull_requests() -> None:
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

    # These remain substring checks, so they prove the trigger words are present,
    # not that GitHub interprets their surrounding YAML exactly as intended.
    assert "pull_request:" in workflow
    assert "push:" in workflow
