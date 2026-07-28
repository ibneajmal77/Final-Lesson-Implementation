# ============================================================================
# FILE: tests/deployment/test_staging_deployment_docs.py
#
# THINK OF THIS FILE AS: the rehearsal checklist and emergency card for staging.
#
# WHAT THIS TESTS: that the staging Compose file uses released images and
# external settings, its environment template names required values, and the
# deployment and rollback guides retain every required operational step.
#
# STAGING is a safe rehearsal environment shaped like production. Docker Compose
# still coordinates the programs, but it uses images already built and pushed by
# CI, connects to external Postgres and Redis services, and receives secrets from
# outside the repository.
#
# WHERE THIS SITS IN THE RELEASE FLOW:
#   .github/workflows/ci.yml tests and builds the application
#     -> image tags and runtime values are placed in the staging environment
#       -> infra/staging/docker-compose.staging.yml migrates and starts the stack
#         -> scripts/deployment-smoke.ps1 and the eval suite check the release
#           -> docs/rollback-runbook.md explains how to recover if checks fail
#
# An IMAGE is the packaged application used to create containers. A MIGRATION is
# an ordered database-shape change. Running the migration command again is
# intended to be IDEMPOTENT: repeating it leaves an already-current database in
# the same state rather than applying the same revision twice.
#
# TESTING APPROACH: these are repository contract checks. They search committed
# YAML, environment-template, and Markdown files for details the deployment
# process depends on. YAML is a configuration format whose indentation defines
# nesting; an environment variable is a named value supplied when a process
# starts rather than hard-coded into its image.
#
# HONEST LIMITATION: most assertions are text searches. They do not parse Compose
# YAML, pull an image, connect to external services, run a migration, protect a
# secret, or perform a rollback. A phrase in a comment or wrong section can pass.
# Real staging deployment, smoke tests, evals, and operator review remain
# necessary.
#
# No pytest FIXTURE is needed. A fixture is reusable setup supplied to tests;
# these checks only read committed files and create no service or shared state.
#
# WHO USES IT / WHAT LIVES HERE: infra/staging/docker-compose.staging.yml defines
# the stack; infra/staging/env.example documents its inputs; stage-17's guide
# describes deployment; docs/rollback-runbook.md covers recovery; settings.py
# consumes the application environment values.
# ============================================================================
from pathlib import Path


# This test protects the staging file's main differences from local Compose:
# pre-built images, shared external configuration, startup ordering, and restarts.
def test_staging_compose_uses_pushed_images_and_external_config() -> None:
    # Reading with an explicit UTF-8 encoding makes the result independent of
    # the Windows or Linux machine running the tests.
    compose = Path("infra/staging/docker-compose.staging.yml").read_text(encoding="utf-8")

    # Six managed processes belong in this file. Postgres and Redis are absent on
    # purpose because staging expects externally operated data services.
    for service_name in ("migrate", "api", "worker", "web", "prometheus", "grafana"):
        # The spaces and colon resemble a service key under YAML's "services:"
        # mapping, but this remains a substring test rather than structural parsing.
        assert f"  {service_name}:" in compose

    # API and web image locations must be supplied by the deployer. Required-value
    # expansion makes Compose stop instead of silently choosing an untested image.
    assert "${SUPPORTOPS_API_IMAGE:?Set SUPPORTOPS_API_IMAGE}" in compose
    assert "${SUPPORTOPS_WEB_IMAGE:?Set SUPPORTOPS_WEB_IMAGE}" in compose
    # The extension block writes common application settings once and reuses them
    # for migrate, API, and worker, preventing those three processes from drifting.
    assert "x-app-environment:" in compose
    assert "DATABASE_URL: ${DATABASE_URL:?Set DATABASE_URL}" in compose
    assert "AI_ANALYSIS_ENABLED: ${AI_ANALYSIS_ENABLED:-true}" in compose
    assert "AI_ANALYSIS_ENABLED_TENANTS: ${AI_ANALYSIS_ENABLED_TENANTS:-tenant_demo}" in compose
    assert "AI_ANALYSIS_ENABLED_CATEGORIES: ${AI_ANALYSIS_ENABLED_CATEGORIES:-billing}" in compose
    # The migration runs to Alembic's newest revision before application services
    # start. Waiting for successful completion avoids serving against an old schema.
    assert 'command: ["python", "-m", "alembic", "upgrade", "head"]' in compose
    assert "condition: service_completed_successfully" in compose
    # "unless-stopped" brings a crashed long-running service back, while respecting
    # an operator who intentionally stopped it.
    assert "restart: unless-stopped" in compose


# The example environment file is a map of required knobs, not a place for real
# credentials. An operator copies it or transfers the names into a secret manager.
def test_staging_env_template_documents_required_runtime_values() -> None:
    env = Path("infra/staging/env.example").read_text(encoding="utf-8")

    # One table-driven loop checks the minimum deployer-facing contract.
    for expected in (
        # Immutable image references connect this deployment to artifacts built by CI.
        "SUPPORTOPS_API_IMAGE=",
        "SUPPORTOPS_WEB_IMAGE=",
        # These values identify the environment and connect the two backing services.
        "APP_ENV=staging",
        "DATABASE_URL=",
        "REDIS_URL=",
        # CORS means Cross-Origin Resource Sharing: the browser addresses allowed
        # to call the API must be named explicitly.
        "CORS_ORIGINS=",
        # Pilot gates keep exposure narrow even though the feature is switched on.
        "AI_ANALYSIS_ENABLED=true",
        "AI_ANALYSIS_ENABLED_TENANTS=tenant_demo",
        "AI_ANALYSIS_ENABLED_CATEGORIES=billing",
        # Mock is the safe default: deterministic responses, no provider key, no cost.
        "MODEL_PROVIDER=mock",
        # Grafana needs an admin password supplied outside the Compose file.
        "GF_SECURITY_ADMIN_PASSWORD=",
    ):
        # Presence does not prove a value is secret, reachable, or suitable. In
        # particular, this test cannot tell whether the placeholder password was changed.
        assert expected in env


# A ROLLBACK returns a failed release to a known safer state. The guide must cover
# application, prompt, provider, and feature-switch recovery rather than only code.
def test_rollback_runbook_contains_required_guide_steps() -> None:
    runbook = Path("docs/rollback-runbook.md").read_text(encoding="utf-8")

    for expected in (
        # These are three independent release surfaces. A bad prompt or provider
        # route may need reverting even when the application image itself is sound.
        "Revert App Image",
        "Revert Prompt Version",
        "Revert Model Route",
        # A KILL SWITCH disables the risky capability quickly without taking down
        # ordinary ticket handling; mock routing offers a second no-cost fallback.
        "Fast AI Kill Switch",
        "AI_ANALYSIS_ENABLED=false",
        "MODEL_PROVIDER=mock",
        # Human support must remain available while automated analysis is disabled.
        "Keep Manual Support Workflow Working",
        # Pull fetches the selected older images before Compose replaces services.
        "docker compose --env-file $EnvFile -f $ComposeFile pull api worker web",
        # Recovery is not complete until the broad HTTP smoke workflow passes.
        "scripts\\deployment-smoke.ps1",
    ):
        # This validates the runbook's vocabulary, not that commands are safe for
        # every incident or that an operator has rehearsed them.
        assert expected in runbook


# The stage-17 guide is the forward path paired with the rollback path above.
# It should cover artifact creation through post-deployment observation.
def test_stage_17_doc_covers_deployment_checklist() -> None:
    doc = Path("docs/stage-17-staging-deployment.md").read_text(encoding="utf-8")

    for expected in (
        # Build once and push the exact artifacts that staging will later pull.
        "Build Images",
        "Push Images",
        # Change the database before starting code that expects the new schema.
        "Apply Database Migration",
        "Deploy API, Worker, and Web",
        # Runtime credentials and provider keys belong outside version control.
        "Configure Secrets",
        # Smoke tests catch broken wiring; evals catch AI-quality regressions.
        "Run Smoke Test",
        "Run Eval Suite",
        # Dashboards reveal errors, latency, and cost that a one-time check misses.
        "Confirm Dashboards",
        # Every forward checklist needs a named escape route before deployment starts.
        "docs/rollback-runbook.md",
    ):
        # The test cannot prove any checklist item was performed. It only prevents
        # the committed guide from silently dropping the instruction.
        assert expected in doc
