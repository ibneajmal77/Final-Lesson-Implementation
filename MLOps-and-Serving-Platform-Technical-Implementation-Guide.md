# MLOps and Serving Platform Technical Implementation Guide

Project codename: `ModelMesh`

This guide turns the production plan into an executable implementation sequence. The target system is a self-service MLOps and model-serving platform for classical ML model packages and LLM adapters. It includes artifact lineage, workflow orchestration, evaluation gates, model gateway routing, vLLM or SGLang serving, Kubernetes deployment, observability, cost attribution, canary release, and rollback.

## How to use this guide

Build the project in stages. Do not skip directly to Kubernetes or vLLM. The platform only becomes defensible when the lifecycle is coherent:

1. Registry and lineage.
2. Reproducible workflows.
3. Evaluation gates.
4. Gateway policy.
5. Serving.
6. Observability and cost.
7. Canary and rollback.
8. Kubernetes and cloud proof.

For each stage:

- Implement only the required scope.
- Add tests before moving on.
- Update docs and stage evidence.
- Keep stage IDs stable.
- Do not mark the stage complete if reviewer proof is missing.

## 0. Scope, non-goals, and prerequisites

### In scope

The implementation must include:

- Tenant-aware platform API.
- Registry database for artifacts, release candidates, approvals, deployments, audit, and outbox events.
- Object storage abstraction for datasets, model packages, adapters, reports, and lineage manifests.
- MLflow or equivalent experiment tracking.
- DVC or equivalent dataset versioning.
- Classical ML training and scoring path.
- LLM adapter registration and validation path.
- Evaluation harness with quality, safety, schema, latency, throughput, and cost gates.
- Provider-neutral model gateway.
- Hosted provider adapter or deterministic local substitute.
- Self-hosted open-model serving path using vLLM or SGLang for the full build.
- Shadow or canary release controller.
- Rollback.
- OpenTelemetry traces and Prometheus metrics.
- Grafana dashboards.
- Docker Compose local environment.
- Kubernetes deployment for the full path.
- Terraform or equivalent IaC for one selected cloud.

### Non-goals for the first production-style version

Do not build:

- Full enterprise feature store.
- Full multi-cloud platform.
- Unsupervised production remediation.
- Distributed training across many GPUs.
- A marketplace billing system.
- Every possible serving backend.
- A replacement for all prior portfolio projects.
- Fine-grained GPU scheduling optimization beyond a documented baseline.

### Local prerequisites

Use versions pinned in the repository:

- Python 3.11 or 3.12.
- FastAPI.
- Pydantic.
- SQLAlchemy or SQLModel.
- Alembic.
- PostgreSQL.
- Redis.
- MinIO or cloud object storage.
- MLflow.
- DVC or equivalent.
- scikit-learn plus XGBoost or LightGBM.
- Transformers, PEFT, and optional TRL for adapter artifacts.
- OpenTelemetry SDK.
- Prometheus client.
- Docker and Docker Compose.
- Kubernetes tooling for the full path.
- Terraform for the full path.

Optional:

- vLLM or SGLang.
- KServe.
- Grafana provisioning.
- Locust, k6, vegeta, or another load-test tool.
- NVIDIA tooling for specialist GPU profiling.

### Pre-build discovery gate

Before writing platform code, create:

- `docs/problem-statement.md`
- `docs/platform-scope.md`
- `docs/adr-platform-boundaries.md`
- `docs/data-platform-contracts.md`
- `docs/developer-experience.md`
- `docs/release-tuple.md`
- `docs/evidence-package.md`

The discovery gate is complete when these questions are answered:

- What classical ML workload will be used?
- What LLM adapter or base model path will be used?
- Which tenant and feature will demonstrate the platform?
- Which artifacts must be immutable?
- Which metrics block release?
- Which rollout path is required?
- Which rollback target is valid?
- Which deployment path is local-only and which is Kubernetes/cloud?

### Canonical executable stack

Use this stack unless the repository already has a stronger local pattern:

- `apps/platform-api`: FastAPI service for registry, approvals, deployments, and admin APIs.
- `apps/model-gateway`: FastAPI service for hosted and self-hosted model routing.
- `apps/worker`: async worker for registry events, evaluation jobs, reconciliation, and reports.
- `apps/classical-scorer`: scoring service for the classical ML package.
- `packages/modelmesh-db`: database models, migrations, and repositories.
- `packages/modelmesh-contracts`: shared Pydantic contracts.
- `packages/modelmesh-evals`: evaluation harness.
- `packages/modelmesh-workflows`: Airflow, Dagster, or local DAG definitions.
- `packages/modelmesh-observability`: traces, metrics, logs, and cost events.
- `infra`: Docker Compose, Kubernetes, Terraform, Prometheus, and Grafana.
- `docs`: living docs and runbooks.
- `reports`: generated evidence.

## 1. Final system and invariants

### Final system

The final system has these runtime components:

- Platform API.
- Model gateway.
- Worker.
- Workflow orchestrator.
- Classical scorer.
- Self-hosted LLM server.
- PostgreSQL.
- Redis.
- Object storage.
- MLflow tracking server.
- Prometheus.
- Grafana.
- Optional Kubernetes ingress.

### Core invariants

Artifact invariants:

- Every dataset version has a checksum.
- Every model package has a checksum and training run ID.
- Every adapter has a checksum, base model ID, tokenizer ID, and license review.
- Every evaluation result references a candidate or deployment.
- Every release candidate references immutable artifact versions.
- No artifact referenced by an approved release can be mutated.

Release invariants:

- A release candidate cannot be approved if lineage is incomplete.
- A release candidate cannot be deployed if any required gate failed.
- A canary cannot start without a rollback target.
- A rollback cannot complete without post-rollback verification.
- A manual override must include approver, reason, expiration, and follow-up.

Gateway invariants:

- Gateway resolves tenant and feature before selecting a model.
- Gateway enforces spend and request limits before provider invocation.
- Gateway records deployment ID for every request.
- Gateway cannot route to an unapproved deployment.
- Gateway cannot use a cache entry across tenant boundaries.
- Gateway emits cost events even for failed requests when cost was incurred.

Observability invariants:

- Every request has a trace ID.
- Every workflow run has a run ID.
- Every deployment change has an audit event.
- Every cost event is attributable to tenant, feature, provider, model, and deployment.
- Sensitive prompt, output, feature, and user data are redacted before export.

## 2. Starter quality gates

Use starter gates first, then tighten after the system runs.

Classical ML release candidate:

- Holdout metric is no worse than current production by more than 2 percent relative unless approved.
- Calibration error does not regress by more than approved tolerance.
- Slice metric does not regress on any named protected or business-critical slice.
- Feature freshness check passes.
- Schema validation passes.
- Prediction p95 latency is within objective.

LLM release candidate:

- Golden functional prompt pass rate is no worse than current production.
- Structured-output validity is at least 98 percent.
- Safety regression pass rate is 100 percent for critical cases.
- p95 end-to-end latency is within objective.
- TTFT is within objective for interactive route.
- Cost per successful task is within objective.
- Quality is measured again after quantization or serving optimization.

Platform release candidate:

- Authorization tests pass.
- Tenant spend-limit tests pass.
- Routing fallback tests pass.
- Canary simulation passes.
- Rollback simulation passes.
- Telemetry redaction tests pass.
- Lineage manifest validates.

## 3. Build order

1. Create repository skeleton and local dependencies.
2. Add platform contracts.
3. Add database schema and migrations.
4. Add tenants, identity stub, authorization, audit, and outbox.
5. Add artifact registry and object storage abstraction.
6. Add dataset and feature set registration.
7. Add classical ML training workflow.
8. Add LLM adapter registration and validation.
9. Add evaluation harness.
10. Add release candidate and approval workflow.
11. Add model gateway contract.
12. Add hosted-provider and mock provider adapters.
13. Add classical scorer route.
14. Add self-hosted vLLM or SGLang route.
15. Add routing, fallback, caching, limits, and cost events.
16. Add canary, shadow, promotion, and rollback.
17. Add observability dashboards.
18. Add Kubernetes deployment.
19. Add load tests and capacity report.
20. Add failure drills and final proof package.

## 4. Beginner milestones

Milestone 1:

- Platform API starts.
- PostgreSQL migrations run.
- Tenant, dataset, and artifact records can be created.

Milestone 2:

- Classical ML workflow trains a model.
- MLflow records parameters, metrics, and artifacts.
- Model package is registered.

Milestone 3:

- LLM adapter artifact is registered.
- Compatibility checks run.
- Evaluation report is produced.

Milestone 4:

- Release candidate is created.
- Gates block or pass correctly.
- Approval is recorded.

Milestone 5:

- Gateway routes to mock, hosted, or local model path.
- Request trace and cost event are emitted.

Milestone 6:

- Canary shifts traffic.
- Failed canary rolls back.
- Rollback report is generated.

Milestone 7:

- Kubernetes deployment runs.
- Load test and cost comparison are documented.

## 5. Target repository and artifact manifest

### Repository structure

```text
modelmesh/
  README.md
  pyproject.toml
  requirements.txt
  requirements-dev.txt
  docker-compose.yml
  .env.example
  apps/
    platform-api/
      modelmesh_platform_api/
        __init__.py
        main.py
        settings.py
        dependencies.py
        auth.py
        routes/
          health.py
          tenants.py
          artifacts.py
          datasets.py
          training_runs.py
          evaluations.py
          releases.py
          deployments.py
          costs.py
          lineage.py
    model-gateway/
      modelmesh_gateway/
        __init__.py
        main.py
        settings.py
        auth.py
        routing.py
        limits.py
        cache.py
        costs.py
        providers/
          base.py
          mock.py
          hosted.py
          vllm.py
          classical.py
        routes/
          health.py
          chat.py
          responses.py
          score.py
          metrics.py
    worker/
      modelmesh_worker/
        __init__.py
        main.py
        queues.py
        jobs/
          artifact_validation.py
          dataset_validation.py
          classical_training.py
          adapter_validation.py
          evaluation.py
          release.py
          rollback.py
          reconciliation.py
          reports.py
    classical-scorer/
      modelmesh_classical_scorer/
        __init__.py
        main.py
        model_loader.py
        scoring.py
        schemas.py
  packages/
    modelmesh-contracts/
      modelmesh_contracts/
        __init__.py
        artifacts.py
        datasets.py
        training.py
        evaluations.py
        releases.py
        gateway.py
        telemetry.py
    modelmesh-db/
      modelmesh_db/
        __init__.py
        models.py
        repositories.py
        session.py
        migrations/
    modelmesh-evals/
      modelmesh_evals/
        __init__.py
        classical.py
        llm.py
        safety.py
        performance.py
        gates.py
        reports.py
    modelmesh-workflows/
      modelmesh_workflows/
        __init__.py
        dags/
          classical_training.py
          adapter_release.py
        local_runner.py
    modelmesh-observability/
      modelmesh_observability/
        __init__.py
        tracing.py
        metrics.py
        logging.py
        costs.py
        redaction.py
  infra/
    docker/
      Dockerfile.platform-api
      Dockerfile.gateway
      Dockerfile.worker
      Dockerfile.classical-scorer
    prometheus/
      prometheus.yml
    grafana/
      dashboards/
      provisioning/
    k8s/
      namespace.yaml
      platform-api.yaml
      model-gateway.yaml
      worker.yaml
      classical-scorer.yaml
      vllm.yaml
      prometheus.yaml
      grafana.yaml
    terraform/
      environments/
        staging/
          main.tf
          variables.tf
          outputs.tf
  data/
    raw/
    processed/
    manifests/
  docs/
    problem-statement.md
    platform-scope.md
    adr-platform-boundaries.md
    architecture.md
    data-platform-contracts.md
    developer-experience.md
    data-model.md
    api-contracts.md
    model-gateway-contract.md
    evaluation-plan.md
    security-and-privacy.md
    threat-model.md
    observability-cost.md
    deployment-runbook.md
    rollback-runbook.md
    capacity-plan.md
    cost-comparison.md
    platform-handoff.md
    progress-log.md
  reports/
    evals/
    lineage/
    load-tests/
    cost/
    canary/
    rollback/
    security/
    drift/
  tests/
    api/
    auth/
    db/
    gateway/
    worker/
    evals/
    workflows/
    deployment/
    security/
```

### Required artifact outputs

At minimum, the repo must produce:

- `reports/lineage/<release_id>.json`
- `reports/evals/<release_id>.md`
- `reports/load-tests/<run_id>.md`
- `reports/cost/<comparison_id>.md`
- `reports/canary/<release_id>.md`
- `reports/rollback/<rollback_id>.md`
- `reports/security/<run_id>.md`
- `reports/drift/<monitor_id>.md`

### Required source-controlled docs

Keep these docs updated:

- Architecture.
- Data platform contracts.
- Developer experience.
- Data model.
- API contracts.
- Gateway contract.
- Evaluation plan.
- Threat model.
- Observability and cost plan.
- Deployment runbook.
- Rollback runbook.
- Capacity plan.
- Platform handoff.
- Progress log.

## 6. Data model

### Core tables

Tenancy and access:

- `tenants`
- `users`
- `roles`
- `tenant_memberships`
- `service_accounts`
- `api_keys` or `client_credentials`
- `policy_versions`

Artifacts:

- `artifact_namespaces`
- `datasets`
- `dataset_versions`
- `data_source_refs`
- `feature_sets`
- `feature_freshness_checks`
- `pipeline_run_refs`
- `prompt_versions`
- `base_models`
- `adapter_artifacts`
- `model_packages`
- `container_images`
- `artifact_checksums`

Workflows:

- `workflow_runs`
- `training_runs`
- `evaluation_runs`
- `benchmark_runs`
- `job_events`
- `dead_letters`

Release:

- `release_candidates`
- `release_candidate_artifacts`
- `gate_results`
- `approvals`
- `deployments`
- `deployment_events`
- `traffic_weights`
- `rollback_events`

Serving:

- `gateway_policies`
- `provider_configs`
- `routing_rules`
- `cache_policies`
- `spend_limits`
- `request_limits`
- `cost_events`
- `request_summaries`

Operations:

- `audit_events`
- `outbox_events`
- `reconciliation_findings`
- `incident_notes`
- `runbook_executions`

### Required constraints

Implement these constraints:

- Artifact records are immutable after `approved` or `used_by_release`.
- `release_candidates.tenant_id` must match artifact tenant or an allowed shared namespace.
- `data_source_refs` must record source type, source ID, snapshot or checkpoint ID, and freshness timestamp when available.
- `feature_freshness_checks` must reference a feature set, source reference, observed timestamp, threshold, and decision.
- `deployments.release_candidate_id` must reference an approved release candidate.
- `traffic_weights` must sum to 100 percent per tenant and feature route.
- `rollback_events.rollback_target_deployment_id` must reference a healthy prior deployment.
- `cost_events.deployment_id` is required when a request reached a provider or serving backend.
- `gate_results` must include metric value, threshold, comparator, and decision.
- `approvals` must include approver, role, policy version, reason, and timestamp.
- `audit_events` must exist for artifact registration, approval, deployment, traffic change, rollback, policy change, and provider disable.

### Example release tuple

```json
{
  "tenant_id": "tenant_support_ops",
  "feature_id": "support_triage_assist",
  "gateway_policy_version": "gateway-policy-v11",
  "prompt_version": "support-prompt-v18",
  "base_model_version": "llama-3.1-8b-instruct",
  "adapter_version": "support-adapter-qlora-0.4.1",
  "model_package_version": null,
  "serving_backend_version": "vllm-0.6.x",
  "container_image_digest": "sha256:...",
  "dataset_version": "golden-prompts-v9",
  "evaluation_run_id": "eval-20260728-004",
  "approval_id": "approval-20260728-002",
  "deployment_id": "deploy-20260728-003"
}
```

### Data invariants

- A dataset version cannot be deleted if it is referenced by a release candidate unless retention policy marks the release invalid and traffic is removed first.
- A model package cannot point to a missing feature set.
- An adapter cannot point to an unknown base model.
- A gateway policy cannot reference a provider config that is disabled.
- A deployment cannot be `serving_primary` if post-deploy smoke checks failed.
- A rollback cannot be `verified` until the gateway route and smoke checks confirm the target.

### Outbox and reconciliation

Use outbox events for:

- Dataset validation requested.
- Training requested.
- Evaluation requested.
- Benchmark requested.
- Release approval granted.
- Deployment requested.
- Canary traffic requested.
- Rollback requested.
- Report generation requested.

Each outbox event should include:

- `event_id`
- `event_type`
- `aggregate_type`
- `aggregate_id`
- `tenant_id`
- `idempotency_key`
- `payload`
- `attempt_count`
- `next_attempt_at`
- `created_at`

Reconciliation jobs should check:

- Registry row exists but object storage artifact is missing.
- Object storage artifact exists but registry row is missing.
- Outbox event is stuck.
- Workflow run is running beyond timeout.
- Deployment desired state differs from gateway observed state.
- Canary weight differs from routing configuration.
- Rollback report missing after rollback.
- Cost events missing for provider calls.

## 7. API contracts

### Register dataset version

Request:

```json
{
  "tenant_id": "tenant_support_ops",
  "name": "sla-risk",
  "source_uri": "s3://modelmesh/datasets/sla-risk/raw/2026-07-28/",
  "schema_version": "sla-risk-schema-v3",
  "version_hash": "sha256:...",
  "retention_class": "training-review",
  "split_manifest_uri": "s3://modelmesh/datasets/sla-risk/splits/v7.json"
}
```

Response:

```json
{
  "dataset_version_id": "dataset-version-20260728-001",
  "status": "registered",
  "validation_status": "queued"
}
```

### Create classical training run

Request:

```json
{
  "tenant_id": "tenant_support_ops",
  "dataset_version_id": "dataset-version-20260728-001",
  "feature_set_id": "sla-risk-features-v12",
  "algorithm": "xgboost",
  "params": {
    "max_depth": 4,
    "learning_rate": 0.05,
    "n_estimators": 200
  },
  "tracking_backend": "mlflow"
}
```

Response:

```json
{
  "training_run_id": "train-20260728-001",
  "workflow_run_id": "workflow-20260728-001",
  "status": "queued"
}
```

### Register adapter

Request:

```json
{
  "tenant_id": "tenant_support_ops",
  "adapter_id": "support-adapter-qlora-0.4.1",
  "base_model_id": "llama-3.1-8b-instruct",
  "artifact_uri": "s3://modelmesh/adapters/support-adapter-qlora-0.4.1/",
  "adapter_type": "qlora",
  "tokenizer_id": "llama-3.1-tokenizer",
  "chat_template_id": "chat-template-v2",
  "context_limit_tokens": 8192,
  "checksum": "sha256:..."
}
```

Response:

```json
{
  "adapter_id": "support-adapter-qlora-0.4.1",
  "status": "registered",
  "validation_status": "queued"
}
```

### Create release candidate

Request:

```json
{
  "tenant_id": "tenant_support_ops",
  "feature_id": "support_triage_assist",
  "candidate_type": "llm_adapter",
  "artifact_refs": {
    "prompt_version": "support-prompt-v18",
    "base_model_version": "llama-3.1-8b-instruct",
    "adapter_version": "support-adapter-qlora-0.4.1",
    "gateway_policy": "gateway-policy-v11"
  },
  "baseline_deployment_id": "deploy-prod-20260720-002"
}
```

Response:

```json
{
  "release_candidate_id": "rc-20260728-007",
  "status": "submitted",
  "lineage_status": "queued",
  "evaluation_status": "queued"
}
```

### Approve release candidate

Request:

```json
{
  "approver_id": "user_platform_reviewer_01",
  "decision": "approved",
  "policy_version": "release-policy-v4",
  "reason": "Quality, safety, latency, and cost gates passed against current production."
}
```

Response:

```json
{
  "approval_id": "approval-20260728-002",
  "release_candidate_id": "rc-20260728-007",
  "status": "approved"
}
```

### Gateway chat request

Request:

```json
{
  "tenant_id": "tenant_support_ops",
  "feature_id": "support_triage_assist",
  "messages": [
    {"role": "user", "content": "Summarize this ticket and suggest next action."}
  ],
  "response_format": {
    "type": "json_schema",
    "schema_id": "ticket-summary-v3"
  },
  "stream": true
}
```

Response metadata:

```json
{
  "trace_id": "trace-01J5...",
  "deployment_id": "deploy-20260728-003",
  "provider": "self_hosted_vllm",
  "model": "llama-3.1-8b-instruct",
  "adapter": "support-adapter-qlora-0.4.1",
  "cache_status": "miss",
  "cost_event_id": "cost-20260728-8821"
}
```

### Start canary

Request:

```json
{
  "release_candidate_id": "rc-20260728-007",
  "initial_weight_percent": 5,
  "max_weight_percent": 25,
  "observation_window_minutes": 30,
  "rollback_on_gate_failure": true
}
```

Response:

```json
{
  "deployment_id": "deploy-20260728-003",
  "status": "serving_canary",
  "traffic_weight_percent": 5
}
```

### Rollback deployment

Request:

```json
{
  "requested_by": "user_operator_01",
  "reason": "Canary p95 latency exceeded objective and timeout rate increased.",
  "rollback_target_deployment_id": "deploy-prod-20260720-002"
}
```

Response:

```json
{
  "rollback_id": "rollback-20260728-001",
  "status": "rolling_back",
  "verification_status": "queued"
}
```

### Capability-aware readiness

Readiness must report actual capability state:

```json
{
  "status": "ready",
  "capabilities": {
    "registry": "ready",
    "workflow_runner": "ready",
    "mlflow": "ready",
    "object_storage": "ready",
    "gateway": "ready",
    "hosted_provider": "degraded",
    "self_hosted_llm": "ready",
    "classical_scorer": "ready",
    "telemetry": "ready"
  }
}
```

The gateway should stop accepting traffic for a route if the route's required capability is not ready.

## 8. Stage 1 - Reproducible repository and dependencies

### Objective

Create a repository that can run locally and support repeatable development.

### Implement

- `pyproject.toml` or equivalent package configuration.
- `requirements.txt` and `requirements-dev.txt`.
- `docker-compose.yml` with PostgreSQL, Redis, MinIO, MLflow, Prometheus, and Grafana.
- `.env.example` with safe placeholders.
- Basic package directories.
- Formatting, linting, type checks, and test command.
- README with local setup.

### Tests and commands

Provide commands for:

```powershell
python -m pytest
python -m mypy packages apps
docker compose config
docker compose up
```

### Done when

- A fresh checkout can create the environment.
- All services start locally.
- Health checks return expected status.
- No secret values are committed.

## 9. Stage 2 - API foundation and operational baseline

### Objective

Start platform API and gateway API with consistent settings, health, readiness, logging, and tracing.

### Implement

- `apps/platform-api/.../main.py`
- `apps/model-gateway/.../main.py`
- Settings modules.
- Health routes.
- Readiness routes.
- Structured logging.
- OpenTelemetry trace initialization.
- Prometheus metrics endpoint.
- Correlation ID middleware.

### Done when

- Platform API returns `200` for health.
- Gateway returns `200` for health.
- Readiness distinguishes missing dependencies from healthy service.
- Logs include trace ID and service name.
- Metrics endpoint exposes process and request metrics.

## 10. Stage 3 - Schema, migrations, and seed data

### Objective

Create the registry schema that owns platform truth.

### Implement

- SQLAlchemy or SQLModel models.
- Alembic migrations.
- Repository layer.
- Seed script for one tenant, one feature, one admin user, one reviewer, one operator, one shared namespace.
- Tests for constraints and migrations.

### Done when

- Migrations run from empty database.
- Seed data is deterministic.
- Database tests prove required constraints.
- Docs include entity relationship summary.

## 11. Stage 4 - Identity, authorization, audit, and retention

### Objective

Prevent cross-tenant and unauthorized platform actions before artifacts exist.

### Implement

- Local identity stub with user ID, tenant ID, roles, and service account.
- Authorization dependency.
- Role checks for admin, ML engineer, reviewer, operator, and auditor.
- Audit-event writer.
- Retention classes for datasets, telemetry, reports, and artifacts.
- Negative authorization tests.

### Done when

- Tenant A cannot read or deploy Tenant B artifacts.
- ML engineer cannot approve own release if policy forbids it.
- Operator can request rollback but cannot approve a new release unless assigned.
- Auditor has read-only access.
- Every denied consequential action is auditable.

## 12. Stage 5 - Artifact store, checksums, and registries

### Objective

Register immutable artifacts with object storage references and checksums.

### Implement

- Object storage client abstraction.
- Artifact namespace model.
- Dataset version registry.
- Prompt version registry.
- Base model registry.
- Adapter artifact registry.
- Model package registry.
- Container image registry record.
- Checksum validation.
- Immutable-state enforcement.

### Done when

- Artifacts can be registered.
- Artifact checksums are validated.
- Approved or used artifacts cannot be mutated.
- Missing object storage references fail validation.
- Shared namespace access is explicit.

## 13. Stage 6 - Dataset, feature, and data-quality validation

### Objective

Make data fit for release gates, not just training.

### Implement

- Dataset manifest parser.
- Schema validation.
- Split validation.
- Row-count and label-distribution checks.
- Feature-set registry.
- Feature freshness rule.
- Leakage checks for the selected tabular domain.
- Data source reference model for local files, warehouse tables, object-storage snapshots, and lakehouse table versions.
- Optional upstream pipeline references for dbt-style jobs, batch pipeline runs, streaming checkpoints, or backfills.
- Optional open table snapshot fields for Delta, Iceberg, Hudi, or equivalent systems.
- Data-platform contract documentation.
- Developer-facing blocked-gate messages.
- DVC or equivalent versioning.
- Dataset card generator.

### Done when

- Dataset version registration triggers validation.
- Invalid schema blocks training.
- Leakage check fails on seeded bad data.
- Feature freshness is recorded.
- Source snapshot or checkpoint metadata is recorded when provided.
- A stale feature set blocks release with a clear gate result.
- Data-platform contracts explain which integrations are implemented and which are placeholders.
- Dataset card is generated.

## 14. Stage 7 - Classical ML workflow and model package

### Objective

Build the classical ML path from dataset to registered model package.

### Implement

- Baseline model.
- Candidate model using scikit-learn, XGBoost, or LightGBM.
- Preprocessing pipeline.
- Training script or workflow task.
- MLflow run tracking.
- Model artifact export.
- Threshold policy.
- Model package registration.
- Calibration and slice report.

### Done when

- Training produces a reproducible model package.
- MLflow records parameters, metrics, artifacts, and code reference.
- Model package includes preprocessor and schema.
- Evaluation can compare candidate to baseline.
- Scoring smoke test passes.

## 15. Stage 8 - LLM artifact import and adapter validation

### Objective

Register one LLM adapter or small open-model artifact with enough metadata to serve and evaluate safely.

### Implement

- Base model registry.
- Tokenizer registry.
- Chat template registry.
- Adapter artifact registry.
- License review record.
- Context limit validation.
- Checksum validation.
- Adapter compatibility check.
- Minimal golden prompt set.

### Done when

- Adapter registration triggers validation.
- Invalid base model or tokenizer blocks release.
- License metadata is recorded.
- Chat template mismatch fails validation.
- Golden prompt evaluation can run against a mock or real serving backend.

## 16. Stage 9 - Workflow orchestration

### Objective

Move long-running jobs out of request handlers.

### Implement

- Airflow, Dagster, cloud workflow, or local DAG runner.
- DAG for classical training.
- DAG for adapter release validation.
- DAG for evaluation and gate decision.
- DAG for benchmark.
- Outbox dispatch.
- Idempotency keys.
- Retries and dead-letter records.
- Run-state transitions.

### Done when

- API writes desired state and outbox event in one transaction.
- Worker or workflow runner processes jobs idempotently.
- Failed job records error and retry state.
- Dead-letter item is visible through API or admin command.
- Reconciliation finds a seeded stuck workflow.

## 17. Stage 10 - Evaluation harness and gate engine

### Objective

Centralize release checks so approval depends on evidence.

### Implement

- Gate definition schema.
- Comparator functions.
- Baseline comparison logic.
- Classical metrics.
- Calibration metrics.
- Slice metrics.
- LLM functional metrics.
- Structured-output validity checks.
- Safety regression checks.
- Latency and cost checks.
- Report generator.

### Done when

- Gate engine can pass and fail seeded candidates.
- Candidate compares against current production.
- Gate result includes metric, threshold, comparator, and decision.
- Release report is generated.
- Manual override requires approver, reason, expiration, and follow-up.

## 18. Stage 11 - Release candidates, approvals, and lineage manifests

### Objective

Create the release lifecycle.

### Implement

- Release candidate API.
- Artifact-reference validation.
- Lineage manifest builder.
- Approval API.
- Rejection API.
- Approval policy.
- Release report skeleton.
- Audit events.

### Done when

- Candidate cannot submit with missing artifacts.
- Candidate cannot approve with failed required gates.
- Candidate cannot deploy before approval.
- Approval records policy version.
- Lineage manifest includes code, data, prompt, model, adapter, evaluation, approval, and deployment references.

## 19. Stage 12 - Model gateway contracts and provider adapters

### Objective

Create a stable gateway contract that can route to different providers without changing application callers.

### Implement

- Gateway request and response schemas.
- Provider interface.
- Mock provider.
- Hosted provider adapter or deterministic substitute.
- Classical scoring provider.
- vLLM provider adapter.
- Streaming abstraction.
- Structured-output validation.
- Error mapping.
- Timeout and retry policy.

### Done when

- Gateway resolves deployment from tenant and feature.
- Mock provider path passes.
- Hosted or substitute path passes.
- Classical scoring path passes.
- Streaming path is tested.
- Structured-output failure is surfaced predictably.

## 20. Stage 13 - Routing, limits, fallback, caching, and cost

### Objective

Turn the gateway into a controlled platform entry point.

### Implement

- Gateway policy registry.
- Provider configs.
- Routing rules.
- Tenant spend limits.
- Request limits.
- Context-length limits.
- Circuit breaker.
- Provider fallback.
- Cache policy.
- Prefix cache metadata where available.
- Cost event writer.
- Cost aggregation query.

### Done when

- Spend limit blocks before provider call.
- Request limit blocks excess traffic.
- Disabled provider is not selected.
- Fallback emits telemetry.
- Tenant cache isolation is tested.
- Cost report can group by tenant, feature, provider, model, adapter, and deployment.

## 21. Stage 14 - Self-hosted open-model serving

### Objective

Serve the LLM adapter through a production-compatible open-model server.

### Implement

- vLLM or SGLang service configuration.
- OpenAI-compatible route.
- Adapter loading path.
- Streaming.
- Concurrency limit.
- Context limit.
- Prefix or KV cache metrics if supported.
- Prometheus scrape.
- Health and readiness checks.
- Functional evaluation against served adapter.

### Done when

- Adapter can be served.
- Gateway can call self-hosted backend.
- Streaming works.
- Context limit is enforced.
- Functional evaluation passes.
- Metrics include latency and throughput indicators.

## 22. Stage 15 - Kubernetes workload deployment

### Objective

Deploy the platform shape expected from the curriculum.

### Implement

- Namespace.
- Platform API deployment and service.
- Gateway deployment and service.
- Worker deployment.
- Classical scorer deployment and service.
- vLLM or SGLang deployment and service.
- ConfigMaps and secrets.
- Resource requests and limits.
- Liveness and readiness checks.
- Horizontal autoscaling where appropriate.
- GPU scheduling for inference workload.
- Persistent volume or object storage references as needed.
- Ingress.

### Done when

- Unhealthy pod leaves service.
- Resource requests and limits are explicit.
- Secret values are not baked into images.
- GPU workload schedules predictably or documented local fallback is used.
- Rolling update and rollback are demonstrated.

## 23. Stage 16 - Terraform and cloud environment

### Objective

Make cloud infrastructure reproducible.

### Implement

- Terraform environment for staging.
- Network.
- Container registry.
- Object storage.
- Managed PostgreSQL or documented local substitute.
- Redis or cache service.
- Secret manager.
- Kubernetes cluster or selected container service.
- GPU node pool or documented GPU-host substitute.
- Monitoring integration.
- Budget and tags.
- Outputs for deployment.

### Done when

- Terraform plan is documented.
- No long-lived secret is in code.
- Network access is restricted.
- Resource ownership and cost tags exist.
- Restore and teardown are documented.

## 24. Stage 17 - Canary, shadow, promotion, and rollback

### Objective

Prove that releases can change traffic gradually and recover.

### Implement

- Deployment desired-state table.
- Traffic weight table.
- Shadow route mode.
- Canary route mode.
- Promotion endpoint.
- Rollback endpoint.
- Gateway policy refresh.
- Post-change smoke checks.
- Canary metrics evaluator.
- Rollback report generator.

### Done when

- Shadow traffic can run without user-visible response change.
- Canary starts at configured weight.
- Canary gate failure stops traffic and rolls back.
- Rollback target receives 100 percent traffic.
- Post-rollback smoke checks pass.
- Rollback report is generated.

## 25. Stage 18 - Observability, dashboards, alerts, and cost reports

### Objective

Make the platform operable.

### Implement

- OpenTelemetry spans for API, gateway, provider calls, workflow jobs, evaluations, release changes, and rollback.
- Prometheus metrics.
- Structured logs with redaction.
- Grafana dashboards.
- Cost events.
- Cost aggregation.
- Alert rules for latency, error rate, saturation, workflow failures, provider failures, cost spike, canary regression, and rollback failure.
- Runbook links.

### Done when

- One request is traceable end to end.
- One workflow run is traceable end to end.
- Cost appears by tenant and feature.
- Dashboards show golden signals, RED, USE, AI quality, and cost.
- Sensitive telemetry redaction test passes.
- Alerts map to owners and runbooks.

## 26. Stage 19 - Drift, feedback, and continuous training trigger

### Objective

Close the loop without allowing raw feedback to train models automatically.

### Implement

- Feedback collection table.
- Feedback review state.
- Drift reference for classical ML.
- Input and output distribution monitors.
- Accuracy proxy where available.
- Human correction tracking.
- Reviewed training candidate export.
- Retraining trigger proposal.
- Gate preventing unreviewed feedback from training.

### Done when

- Feedback is linked to trace, tenant, feature, and deployment.
- Reviewed examples can create a new dataset version.
- Unreviewed feedback cannot enter training data.
- Drift report is generated.
- Retraining trigger creates a proposal, not an automatic production deployment.

## 27. Stage 20 - Security, privacy, and governance tests

### Objective

Prove the platform does not bypass its own controls.

### Implement

- Threat model.
- Secret scanning.
- Dependency scan.
- Container scan.
- Tenant isolation tests.
- Approval-bypass tests.
- Spend-limit tests.
- Telemetry redaction tests.
- Artifact mutation tests.
- Cache isolation tests.
- Provider disable tests.
- Rollback authorization tests.
- Audit completeness tests.

### Done when

- Critical security tests pass.
- Unauthorized release cannot deploy.
- Unauthorized rollback cannot run.
- Tenant data cannot leak through registry, gateway, cache, or reports.
- Secrets are not present in committed files or images.
- Audit log covers consequential actions.

## 28. Stage 21 - Load testing, capacity planning, and optimization

### Objective

Measure performance and cost under realistic load.

### Implement

- Load-test scenarios for short, medium, and long prompts.
- Load-test scenarios for classical scoring.
- Concurrency levels.
- TTFT capture.
- Inter-token latency capture.
- End-to-end p95 and p99 latency.
- Tokens per second.
- Queue time.
- GPU utilization and memory.
- Cache hit rate.
- Cost per request.
- Cost per successful task.
- Hosted-versus-self-hosted comparison.
- Quality check after optimization.

### Done when

- Load-test report is generated.
- Capacity assumptions are documented.
- Bottlenecks are identified from evidence.
- Quantization or cache changes include quality comparison.
- Cost report explains when self-hosting wins or loses.

## 29. Stage 22 - CI/CD, deployment, restore, and pilot

### Objective

Make delivery reproducible and reviewer-friendly.

### Implement

- CI workflow.
- Unit, integration, security, eval, and deployment checks.
- Container build.
- Migration check.
- Staging deploy.
- Smoke test.
- Release report generation.
- Backup and restore drill.
- Pilot checklist.
- Platform handoff document.
- Local quickstart that registers an artifact, creates a release candidate, and checks release status.
- Minimal SDK, CLI, or scripted API examples for platform consumers.

### Done when

- CI blocks broken contracts.
- Deployment is reproducible.
- Restore procedure is demonstrated.
- Pilot has clear entry and exit criteria.
- Handoff docs explain operations, rollback, cost, and known limits.
- A reviewer can complete the first release workflow from documented commands.

## 30. Documentation governance and stage records

### Stage record format

Each stage should create or update a record:

```markdown
# Stage NN - Name

## Objective

## Implemented

## Tests

## Evidence

## Open risks

## Next step
```

### Canonical stage IDs

Use stable IDs:

- `MM-01-repo`
- `MM-02-api-baseline`
- `MM-03-schema`
- `MM-04-auth-audit`
- `MM-05-artifacts`
- `MM-06-data-validation`
- `MM-07-classical-workflow`
- `MM-08-llm-adapter`
- `MM-09-orchestration`
- `MM-10-evaluation-gates`
- `MM-11-release-lineage`
- `MM-12-gateway`
- `MM-13-routing-cost`
- `MM-14-open-serving`
- `MM-15-kubernetes`
- `MM-16-terraform`
- `MM-17-canary-rollback`
- `MM-18-observability-cost`
- `MM-19-feedback-drift`
- `MM-20-security-governance`
- `MM-21-load-capacity`
- `MM-22-cicd-pilot`

### Documentation checks

Before final review, verify:

- Every stage has a record.
- Every release has a lineage manifest.
- Every report references source artifacts.
- Every public claim has evidence.
- Docs match implemented endpoints and commands.

## 31. Minimal and full build paths

### Smallest complete portfolio build

The smallest complete build may use:

- Local Docker Compose.
- Local workflow runner.
- Mock hosted provider.
- Small scikit-learn model.
- Existing adapter artifact or deterministic LLM mock.
- Local gateway and scoring route.
- Simulated canary traffic.
- Simulated cost events.
- Generated reports.

It must still include:

- Artifact registry.
- Lineage manifest.
- Evaluation gates.
- Approval.
- Canary.
- Rollback.
- Observability.
- Cost attribution.
- Security tests.

### Full production-style path

The full path adds:

- Airflow or Dagster.
- vLLM or SGLang.
- Kubernetes.
- Terraform.
- Cloud object storage, registry, secrets, and monitoring.
- GPU scheduling or documented GPU-host equivalent.
- Real load test.
- Hosted-versus-self-hosted cost comparison.
- Rolling update and Kubernetes rollback demonstration.

## 32. Requirement traceability matrix

### Production requirement crosswalk

| Requirement | Evidence |
|---|---|
| Self-service train-evaluate-approve-deploy-monitor workflow | Workflow DAG, platform API, release report |
| Classical ML support | Dataset, feature set, training run, model package, scoring API |
| LLM adapter support | Base model, tokenizer, adapter registry, gateway route |
| Registries and lineage | Registry tables, lineage manifest |
| Evaluation gates | Gate result records and eval report |
| Canary release | Traffic weights and canary report |
| Rollback | Rollback endpoint and rollback report |
| Kubernetes | Manifests, health checks, resource limits, GPU scheduling proof |
| Observability | Trace export, Prometheus metrics, Grafana dashboards |
| Cost attribution | Cost events and cost report |
| Security and governance | Threat model, auth tests, audit logs |
| Inference benchmark | Load-test report with TTFT, tokens/sec, p95, queue time, GPU util |

### Curriculum crosswalk

| Curriculum area | Implementation evidence |
|---|---|
| Lesson 30 production architecture | ADR, queues, SLOs, failure injection, rollback |
| Lesson 31 observability and cost | OpenTelemetry, dashboards, RED, USE, cost per successful task |
| Lesson 32 cloud infrastructure | Docker, Terraform, secrets, network, budgets |
| Lesson 33 Kubernetes | Deployments, services, health checks, autoscaling, GPU scheduling |
| Lesson 34 LLMOps and MLOps | MLflow, DVC, registries, gates, continuous training proposal |
| Lesson 35 open-model serving | vLLM or SGLang, streaming, adapter serving, provenance |
| Lesson 36 inference optimization | Load tests, batching, cache, quantization quality check, capacity plan |
| Lesson 38 classical ML path | Feature validation, model package, calibration, drift |
| Lesson 44 MLOps platform | Self-service platform API, multi-tenancy, workflows, lineage, developer experience |

### Requirement-to-evidence manifest

Create `reports/final-evidence-manifest.json`:

```json
{
  "project": "ModelMesh",
  "requirements": [
    {
      "id": "registry-lineage",
      "status": "met",
      "evidence": [
        "docs/data-model.md",
        "reports/lineage/rc-20260728-007.json"
      ]
    },
    {
      "id": "canary-rollback",
      "status": "met",
      "evidence": [
        "reports/canary/rc-20260728-007.md",
        "reports/rollback/rollback-20260728-001.md"
      ]
    }
  ]
}
```

## 33. Test strategy

### Unit tests

Cover:

- Gate comparators.
- Release tuple validation.
- Lineage manifest builder.
- Cost calculator.
- Gateway routing policy.
- Cache key generation.
- Redaction functions.
- Artifact checksum validation.
- Threshold utility calculations.
- Drift detector basics.

### Integration tests

Cover:

- Register dataset to validation job.
- Train classical model to model package.
- Register adapter to compatibility check.
- Create release candidate to gate results.
- Approve candidate to deployment.
- Gateway request to provider call to cost event.
- Canary failure to rollback.
- Reconciliation repair or alert.

### API tests

Cover:

- Tenants.
- Datasets.
- Feature sets.
- Training runs.
- Adapters.
- Evaluations.
- Releases.
- Deployments.
- Rollback.
- Costs.
- Lineage.
- Gateway chat.
- Gateway score.

### Security tests

Cover:

- Cross-tenant read denial.
- Cross-tenant deployment denial.
- Unauthorized approval denial.
- Unauthorized rollback denial.
- Artifact mutation denial.
- Cache isolation.
- Spend limit.
- Secret leakage scan.
- Telemetry redaction.
- Audit completeness.

### Evaluation tests

Cover:

- Candidate passes all gates.
- Candidate fails quality.
- Candidate fails safety.
- Candidate fails latency.
- Candidate fails cost.
- Candidate fails missing lineage.
- Quantized candidate requires quality rerun.
- Manual override records required fields.

### Deployment tests

Cover:

- Docker Compose config.
- API health.
- Gateway health.
- Worker boot.
- Migration from empty DB.
- Kubernetes manifests parse.
- Readiness fails when dependency unavailable.
- Rollback command updates route.

## 34. Data and annotation plan

### Classical ML data

Use a public or synthetic tabular dataset with:

- Stable schema.
- Binary or multiclass label.
- Enough rows for train, validation, and holdout.
- At least three meaningful slices.
- Business-cost interpretation.
- Drift reference window.

Required docs:

- Dataset card.
- Feature contract.
- Leakage checklist.
- Threshold decision memo.
- Drift plan.

### LLM data

Use:

- Existing `DomainTune` adapter if available.
- Small instruction-following sample if training locally.
- Golden prompt set.
- Structured-output set.
- Safety regression set.
- Latency benchmark prompt set.

Required docs:

- Adapter card.
- Base model license record.
- Tokenizer and chat-template record.
- Prompt registry.
- Evaluation plan.
- Serving decision memo.

### Feedback data

Feedback must include:

- Trace ID.
- Tenant ID.
- Feature ID.
- Deployment ID.
- Feedback type.
- Reviewer status.
- Redaction status.
- Dataset candidate status.

Unreviewed feedback cannot enter training.

## 35. Operational runbooks

### Provider outage

1. Confirm provider error rate and timeout metrics.
2. Check circuit-breaker state.
3. Verify fallback policy.
4. Disable provider if policy allows.
5. Confirm gateway routes to fallback.
6. Watch cost, latency, and quality smoke tests.
7. Write incident note.

### Self-hosted inference saturation

1. Check queue time, TTFT, GPU utilization, memory, and context length distribution.
2. Check active canary or recent deployment.
3. Reduce canary weight or route to hosted fallback.
4. Confirm latency recovers.
5. Record capacity finding.

### Failed canary

1. Identify failing gate.
2. Stop canary traffic.
3. Roll back to target deployment.
4. Run smoke evaluation.
5. Verify metrics.
6. Generate rollback report.
7. Create follow-up issue.

### Bad model package

1. Freeze promotion for feature.
2. Roll back scoring route.
3. Verify schema and threshold.
4. Check drift and feature freshness.
5. Generate incident note.

### Missing artifact

1. Check registry reference.
2. Check object storage URI.
3. Run reconciliation.
4. Block dependent release candidates.
5. Restore from backup or mark artifact unavailable.

## 36. Optional IncidentPilot technical extension

Add this only after baseline observability is working.

### Scope

`IncidentPilot` is read-only by default:

- Reads logs, metrics, traces, deployment events, queue state, provider status, and runbooks.
- Builds incident timeline.
- Produces ranked hypotheses.
- Links supporting and contradicting evidence.
- Drafts incident update.
- Retrieves runbook steps.

### Consequential actions

Any restart, scale, rollback, feature flag, or traffic-routing change requires:

- Normal platform authorization.
- Exact arguments.
- Human approval.
- Idempotency key.
- Audit record.
- Verification result.
- Compensation or rollback path.

### Tests

- Provider throttling drill.
- Queue saturation drill.
- Retrieval or evaluation regression drill.
- Telemetry prompt-injection red-team test.
- False-action-rate test.
- Evidence precision test.

## 37. Final reviewer proof

The reviewer should be able to run or inspect equivalent commands:

```powershell
python -m pytest
python -m mypy packages apps
docker compose config
docker compose up
```

Then verify:

- Platform API health.
- Gateway health.
- Database migrations.
- Seed data.
- Dataset registration.
- Classical training workflow.
- Model package registration.
- Adapter registration.
- Evaluation run.
- Release candidate creation.
- Approval.
- Canary.
- Rollback.
- Cost report.
- Trace export.
- Load-test report.

Final evidence files:

- `docs/platform-handoff.md`
- `docs/capacity-plan.md`
- `docs/cost-comparison.md`
- `reports/final-evidence-manifest.json`
- `reports/load-tests/<run_id>.md`
- `reports/canary/<release_id>.md`
- `reports/rollback/<rollback_id>.md`
- `reports/lineage/<release_id>.json`

## 38. First practical assignment

Build the first useful slice:

1. Create platform API with tenants, datasets, artifacts, and releases.
2. Add PostgreSQL migrations.
3. Add local identity stub.
4. Add object storage abstraction.
5. Register one dataset version.
6. Train one classical ML baseline.
7. Register one model package.
8. Run one evaluation.
9. Create one release candidate.
10. Block approval if lineage is incomplete.

This assignment proves the lifecycle before gateway, Kubernetes, or GPU work.

## 39. Final definition of done and interview defense

The technical build is complete when:

- The repo can be started from a fresh checkout.
- Migrations create the registry schema.
- Tenancy, authorization, audit, and retention controls are implemented.
- Immutable artifact registration works.
- Classical ML workflow registers a model package.
- LLM adapter validation works.
- Evaluation gates block bad releases.
- Release candidate lifecycle includes approval, staging, canary, promotion, and rollback.
- Gateway routes tenant-aware traffic and emits cost and trace events.
- vLLM or SGLang serving is demonstrated in the full path.
- Kubernetes deployment includes health checks, resource requests, limits, and GPU scheduling proof.
- Load-test report includes TTFT, tokens/sec, p95 latency, queue time, GPU utilization, and cost.
- Quality is reevaluated after every serving optimization.
- Rollback is demonstrated and documented.
- Security tests prove tenant isolation and approval enforcement.
- Final evidence manifest maps claims to files and reports.

For interview defense, be ready to explain:

- Why the platform is not just an MLflow demo.
- Why the architecture boundaries are justified.
- How lineage is enforced.
- How gate decisions are calculated.
- How traffic shifts during canary.
- How rollback changes gateway policy.
- How hosted and self-hosted cost comparison was measured.
- How Kubernetes resource controls affect reliability.
- How feedback becomes training data safely.
- What you would change before real production use.
