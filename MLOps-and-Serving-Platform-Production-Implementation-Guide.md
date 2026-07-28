# MLOps and Serving Platform Production Implementation Guide

Project codename: `ModelMesh`

Build a self-service platform that lets AI teams train, evaluate, approve, deploy, monitor, and roll back both classical ML models and LLM adapters. The finished project should prove that you can operate models as production software: reproducible artifacts, lineage, quality gates, cost controls, Kubernetes deployment, inference benchmarking, canary release, and rollback evidence.

This is not a notebook project and it is not just a vLLM demo. It is a platform project. The core value is the controlled lifecycle around models, prompts, datasets, adapters, evaluation results, deployments, telemetry, and operational decisions.

## Source alignment

This guide is aligned to the local curriculum and roadmap documents:

- `AI-Industry-Roadmap-and-Projects.md`: Phase 8 `ModelMesh`, lessons 30-36, optional `IncidentPilot`, and portfolio proof requirements.
- `deep-research-report.md`: compressed portfolio project `MLOps and serving platform`, required workflow DAG, registry, canary demo, rollback demo, and platform README.
- `AI-Industry-Curriculum.md`: cloud, containers, infrastructure, LLMOps/MLOps, open-model serving, inference engineering, model monitoring, and cost-per-successful-task outcomes.
- `AI-Industry-Complete-Lesson-Coverage-Map.md`: lesson 30 production architecture, lesson 31 observability and cost, lesson 32 cloud, lesson 33 Kubernetes, lesson 34 LLMOps/MLOps, lesson 35 open-model serving, lesson 36 inference optimization, and lesson 44 MLOps platform specialization.
- `AI-Industry-Detailed-Lessons.md`: guided implementation expectations for deployment, Kubernetes workloads, registries, canary evaluation, open-model serving, and optimization.

The project should support the prior `DomainTune` artifact path, but it must also include one classical ML path so the platform is not only an LLM adapter registry.

## Evidence and verification vocabulary

Use these terms consistently across the repository:

- `dataset version`: Immutable dataset or feature snapshot used by a run.
- `feature set`: Versioned classical ML feature contract, transformation code, and freshness rule.
- `prompt version`: Immutable prompt template or system instruction set.
- `base model version`: Immutable hosted or self-hosted model identifier.
- `adapter version`: Immutable LoRA, QLoRA, or other adapter artifact.
- `model package`: Deployable classical ML artifact with preprocessing, model weights, schema, thresholds, and metadata.
- `evaluation run`: Versioned quality, safety, performance, drift, or cost assessment.
- `release candidate`: Artifact tuple proposed for staging or production.
- `deployment version`: Approved release candidate currently routed by the gateway or model endpoint.
- `lineage manifest`: The complete chain from code, data, configuration, prompts, models, adapters, evaluation results, approval, and deployment.
- `rollback proof`: Evidence that the platform returned traffic to the previous known-good version and verified service and quality status afterward.

## 1. Production outcome

The final system is a production-style AI platform where internal teams can:

1. Register datasets, feature sets, prompts, base models, adapters, and classical ML model packages.
2. Launch reproducible training and evaluation workflows.
3. Compare candidates against baselines and previous production versions.
4. Require approval before promotion.
5. Deploy model artifacts to staging and production-like environments.
6. Serve LLM adapters through an OpenAI-compatible gateway with routing, streaming, caching, cost attribution, and fallback.
7. Serve a classical ML model through a predictable scoring API.
8. Roll out changes with shadow and canary traffic.
9. Roll back automatically or with operator approval when quality, safety, latency, error, or cost gates fail.
10. Trace every request, cost, model decision, and deployment event back to a lineage manifest.

The project is production-ready when a reviewer can run a workflow, inspect the registry, approve a release, route traffic to a candidate, observe traces and metrics, trigger a failure, roll back, and read an evidence report that explains what happened.

## 2. Business problem, users, scope, and non-goals

### Business problem

Many teams call models directly, deploy adapters manually, keep experiments in notebooks, and cannot answer basic operational questions:

- Which dataset, prompt, model, and adapter produced this behavior?
- Did quality regress after quantization, routing, or a new release?
- Which tenant or feature created this cost spike?
- Can the previous version be restored quickly?
- Are hosted APIs cheaper or more reliable than self-hosted serving for this workload?
- Which release should be approved, rejected, or rolled back?

`ModelMesh` solves this by centralizing lifecycle control, serving policy, observability, and evidence without forcing every team to understand the full infrastructure stack.

### Primary users

- Applied AI teams who need to ship model-backed features.
- ML engineers who need repeatable training and evaluation.
- Platform engineers who operate shared inference and workflow infrastructure.
- Product owners who need quality, cost, and rollout reports.
- Security and governance reviewers who need lineage, approvals, and audit trails.
- On-call operators who need alerts, rollback controls, and runbooks.

### Initial domain

Use two deliberately small but representative workloads:

- Classical ML workload: a tabular business-risk model, such as churn, SLA breach risk, fraud risk, or lead conversion.
- LLM workload: one `DomainTune` style adapter or a small instruction-following adapter served through vLLM or a compatible local mock in the minimal path.

The exact domain can change, but both workload types must be present:

- Batch or workflow-driven training and evaluation for classical ML.
- LLM adapter registration, serving, inference benchmarking, and release gating.

### Required scope

The first production-style release must include:

- Tenant-aware platform API.
- Artifact registry for datasets, prompts, models, adapters, model packages, evaluation runs, and releases.
- Workflow orchestration using Airflow, Dagster, or a clear local substitute.
- MLflow or equivalent experiment tracking.
- DVC or equivalent data versioning for reproducible dataset snapshots.
- Classical ML training path with model package registration.
- LLM adapter import path with artifact validation.
- Evaluation gates for quality, safety, schema validity, latency, throughput, and cost.
- Model gateway with provider-neutral request contract.
- Hosted-provider path and self-hosted open-model path.
- vLLM or SGLang serving path for the full version.
- Kubernetes deployment for gateway, worker, workflow, and inference services.
- Terraform or equivalent IaC for cloud resources.
- OpenTelemetry traces, Prometheus metrics, and Grafana dashboards.
- Shadow or canary release controller.
- Rollback path with evidence.
- Cost attribution by tenant, feature, model, and deployment version.
- Load-test report with TTFT, tokens/sec, p95 latency, queue time, GPU utilization, and cost.
- Hosted-versus-self-hosted cost comparison.

### Explicit non-goals for the first release

Do not attempt these until the core lifecycle works:

- Multi-cloud abstraction across all providers.
- A general-purpose feature store.
- Fully automated unsupervised remediation.
- Large-scale distributed training.
- Full enterprise marketplace billing.
- Fine-grained GPU bin-packing optimization beyond a demonstrated scheduling path.
- Support for every serving framework.
- Rewriting prior portfolio projects to depend on this platform.
- Claiming production safety without rollback, audit, and failure-injection evidence.

## 3. Business outcomes and metric tree

### Primary outcome

Teams can ship model changes with less risk because every release is reproducible, evaluated, approved, observable, cost-attributed, and reversible.

### Business metrics

- Time from candidate model to approved staging release.
- Time from staging release to production-like canary decision.
- Percentage of releases with complete lineage.
- Percentage of failed gates caught before production traffic.
- Mean time to rollback.
- Cost per successful task.
- Hosted versus self-hosted cost at expected traffic.
- Platform consumer setup time.
- On-call time spent diagnosing model or provider regressions.

### Quality metrics

Classical ML:

- Accuracy, precision, recall, F1, AUC, or domain-appropriate score.
- Calibration error.
- Threshold utility by business cost.
- Slice performance by tenant, segment, or cohort.
- Feature freshness.
- Data-quality failures.
- Drift indicators.

LLM and adapter:

- Task success.
- Structured-output validity.
- Refusal and over-refusal rate.
- Safety policy violation rate.
- Regression pass rate on golden prompts.
- Human preference win rate where applicable.
- Groundedness or citation quality if a RAG-backed path is used.
- Tool-call success if the served model path supports tools.

Serving and infrastructure:

- Time to first token.
- Inter-token latency.
- End-to-end latency.
- Tokens per second.
- Requests per second.
- Queue time.
- p50, p95, and p99 latency.
- GPU utilization and memory.
- Cache hit rate.
- Error rate.
- Saturation.
- Cost per request.
- Cost per successful task.

### Guardrail metrics

- Release candidates blocked by missing lineage.
- Release candidates blocked by stale datasets.
- Release candidates blocked by quality regression.
- Release candidates blocked by safety regression.
- Rollbacks completed and verified.
- Failed rollback drills.
- Unauthorized deployment attempts denied.
- Sensitive telemetry redaction failures.
- Tenant spend-limit enforcement events.

## 4. What production-ready means

`ModelMesh` is production-ready only if:

- A release cannot be promoted without a complete lineage manifest.
- Every deployed artifact is immutable and versioned.
- Every deployment has a previous known-good version unless it is an explicitly documented first release.
- Evaluation gates compare the candidate against the prior production version, not only against a generic threshold.
- A model that passes quality but fails latency or cost gates cannot be promoted silently.
- A model that passes latency but loses quality after quantization cannot be promoted silently.
- Gateway traffic records the tenant, feature, release version, provider, model, prompt, adapter, trace ID, cost, and outcome.
- A failed provider or model can degrade to a documented fallback.
- Canary traffic can be stopped and rolled back.
- Operators have dashboards and runbooks, not only logs.
- Sensitive prompts, outputs, feature values, and telemetry fields are redacted according to policy.
- The platform can explain why a release was approved, rejected, rolled forward, or rolled back.

## 5. Non-negotiable requirements

1. Complete lineage: code, data, prompt, model, adapter, config, evaluation, approval, and deployment must be connected.
2. Immutable artifacts: registered datasets, model packages, adapters, prompts, and evaluation results must not be mutated in place.
3. Reproducible workflows: a reviewer must be able to rerun or replay the key workflow from manifest references.
4. Quality gates: quality, safety, schema, performance, cost, and reliability gates must block releases.
5. Tenant isolation: tenants cannot see, modify, deploy, or route traffic to artifacts they do not own or have permission to use.
6. Gateway policy: provider routing, fallback, caching, spend limits, and context limits must be explicit and versioned.
7. Rollback: rollback must be implemented, tested, documented, and demonstrated.
8. Observability: one request must be traceable end to end through gateway, provider or serving service, registry, cost accounting, and release metadata.
9. Cost attribution: cost must be visible by tenant, feature, provider, model, adapter, and deployment version.
10. Security: no long-lived cloud or provider secrets in code, images, notebooks, logs, or artifacts.
11. Kubernetes proof: the full path must deploy gateway, worker, training job, and inference service to Kubernetes with health checks and resource limits.
12. Evidence package: the repo must contain load-test, cost, rollback, quality, and platform handoff reports.

## 6. Core journeys and required UX

### Platform consumer onboarding journey

The consumer should be able to:

1. Create or select a tenant and feature.
2. Register a use case with expected traffic, latency, quality, and budget goals.
3. Choose a hosted-provider route, a self-hosted route, or a comparison route.
4. Register prompts, datasets, or adapters.
5. Submit a release candidate.
6. View status, gates, and required fixes.
7. Receive a stable gateway endpoint and API contract after approval.

Required UX:

- Dashboard view of current deployments by tenant and feature.
- Release-candidate view with lineage, gates, metrics, approvals, and rollback target.
- Cost view by tenant, provider, model, adapter, and release.
- Request trace view with correlated gateway, model, cache, and cost events.

### Classical ML lifecycle journey

The ML engineer should be able to:

1. Register a dataset or feature snapshot.
2. Validate schema, freshness, leakage rules, and data quality.
3. Launch a training workflow.
4. Track parameters, metrics, artifacts, and code version.
5. Register a model package with preprocessing and threshold configuration.
6. Run evaluation against holdout and slice datasets.
7. Submit the package as a release candidate.
8. Deploy to staging, shadow, canary, or production-like route.
9. Monitor drift, calibration, latency, and business impact.
10. Trigger retraining only through reviewed data and release gates.

Required UX:

- Model comparison table.
- Calibration and threshold decision report.
- Feature freshness and data-quality status.
- Drift monitor view.
- Rollback status for the scoring endpoint.

### LLM adapter and serving journey

The LLM engineer should be able to:

1. Register a base model and license metadata.
2. Register an adapter artifact with checksum and provenance.
3. Validate tokenizer, chat template, context length, and compatibility.
4. Run functional, safety, and regression evaluations.
5. Run inference benchmark at multiple sequence lengths and concurrency levels.
6. Compare hosted-provider, self-hosted base model, and adapter routes.
7. Submit a release candidate.
8. Release through shadow or canary traffic.
9. Roll back if quality, latency, error, or cost gates fail.

Required UX:

- Adapter compatibility status.
- Prompt and model version view.
- Streaming request test console.
- TTFT, tokens/sec, queue time, GPU utilization, and cost charts.
- Quantization comparison table with quality deltas.

### Operator and incident journey

The operator should be able to:

1. See active deployments and health status.
2. See SLO burn, error rate, latency, saturation, queue depth, GPU utilization, cache hit rate, and cost anomalies.
3. Open a deployment timeline and recent-change list.
4. Stop a canary.
5. Roll back to the previous known-good version.
6. Verify that traffic, health checks, quality smoke tests, and cost accounting returned to expected behavior.
7. Write an incident note linked to traces, deployment events, and rollback evidence.

Required UX:

- Operator dashboard with golden signals, RED, and USE metrics.
- Release timeline.
- Rollback control with confirmation and required reason.
- Runbook links.
- Post-rollback verification checklist.

### Governance and audit journey

The reviewer should be able to:

1. Inspect artifact lineage for any deployment.
2. Confirm approvals, policy versions, and gate outcomes.
3. Verify data retention and telemetry redaction.
4. Export a scoped evidence bundle.
5. Deny a release with a required remediation reason.

Required UX:

- Read-only audit view.
- Evidence export with tenant and retention filtering.
- Approval history.
- Policy decision log.

## 7. Governance, identity, tenancy, and artifact-first architecture

The platform must treat artifacts, not requests, as the core unit of governance. Requests are transient. Artifacts and release decisions are durable.

### Governance invariants

- Every artifact belongs to exactly one owning tenant or to a shared platform namespace.
- Shared artifacts require explicit allow-list policy.
- A release candidate may reference shared artifacts only if the tenant has permission at submission and at deployment time.
- Approval decisions must record approver, role, timestamp, policy version, candidate version, and gate summary.
- A model package or adapter cannot be overwritten after approval.
- A dataset version cannot be changed after it is used by an evaluation or training run.
- A deployment cannot route traffic to an unapproved release candidate.
- Rollback cannot route traffic to an artifact whose retention policy has made it unavailable.
- Telemetry must use stable IDs and redact sensitive values before leaving the trust boundary.
- Spend and request limits must be enforced before provider or model invocation.

### Canonical approval sequence

Use this sequence for every production-like release:

1. Candidate submitted.
2. Lineage manifest assembled.
3. Artifact integrity verified.
4. Compatibility checks run.
5. Quality gates run.
6. Safety and security gates run.
7. Performance and cost gates run.
8. Reviewer approves or rejects.
9. Candidate deployed to staging.
10. Shadow or canary traffic begins.
11. Canary metrics are evaluated.
12. Candidate is promoted, held, or rolled back.
13. Release report is generated.

### Policy-change SLO

Policy changes must take effect predictably:

- Tenant access changes: effective within 5 minutes for new requests.
- Spend-limit changes: effective within 1 minute for new requests.
- Deployment freezes: effective within 1 minute.
- Artifact revocation: blocks new release candidates immediately and blocks new traffic after gateway policy refresh.
- Emergency provider disable: effective within 1 minute.

Document the cache behavior that makes these SLOs true.

## 8. Reference architecture and project boundaries

### Recommended stack

Minimal local path:

- FastAPI for platform API and model gateway.
- PostgreSQL for registry, approvals, audit, and release state.
- Redis for queues, rate limits, cache metadata, and distributed locks.
- Object storage compatible with S3 semantics for artifacts.
- MLflow for experiment tracking.
- DVC or equivalent for dataset versioning.
- scikit-learn, XGBoost, or LightGBM for the classical ML path.
- Transformers, PEFT, or existing `DomainTune` artifacts for the LLM adapter path.
- Docker Compose for local dependencies.
- OpenTelemetry SDK, Prometheus, and Grafana.

Full platform path:

- Airflow, Dagster, or cloud workflows for orchestration.
- Kubernetes for gateway, API, workers, workflow jobs, and inference service.
- vLLM or SGLang for OpenAI-compatible self-hosted LLM serving.
- KServe where useful for model-serving abstraction.
- Terraform for cloud networking, registry, storage, secrets, Kubernetes, monitoring, and budgets.
- Private container registry.
- Cloud identity or workload identity.
- GPU node pool or GPU instance for inference benchmarks.
- GitHub Actions or equivalent CI/CD.

### Component responsibilities

Platform API:

- Owns tenants, features, registry metadata, approvals, release candidates, deployment state, and audit.
- Does not run long training jobs inside request handlers.

Workflow orchestrator:

- Owns training, evaluation, packaging, benchmark, and promotion workflows.
- Emits structured events to the platform registry.

Training workers:

- Run classical ML training and adapter validation jobs.
- Produce immutable artifacts and metrics.

Evaluation workers:

- Run quality, safety, schema, drift, performance, and cost evaluations.
- Produce evaluation artifacts and gate decisions.

Model gateway:

- Receives application inference requests.
- Enforces authentication, authorization, rate limits, spend limits, context limits, routing policy, caching policy, and fallback policy.
- Streams LLM responses and records telemetry.

Serving backends:

- Hosted provider adapter.
- Self-hosted vLLM or SGLang adapter.
- Classical ML scoring service.
- Optional KServe inference service.

Observability stack:

- Collects traces, metrics, logs, deployment events, cost events, and quality events.
- Presents operator, product, and executive dashboards.

Release controller:

- Manages staging, shadow, canary, promotion, freeze, and rollback.
- Verifies health after traffic changes.

### Architecture decision requirement

The project must contain an ADR comparing:

- Modular monolith.
- Event-driven workers.
- Separately deployable microservices.

The decision must evaluate:

- Scaling needs.
- Failure isolation.
- Latency.
- Data ownership.
- Security boundary.
- Deployment complexity.
- Observability complexity.
- Cost.
- Team ownership.
- Migration path.

Do not choose microservices only because the system contains AI. The default should be a modular service plus separate workers and serving runtimes unless measured constraints justify more separation.

### Data platform and developer-experience boundaries

Lesson 44 expects MLOps platform depth, but the portfolio project should keep that depth bounded. `ModelMesh` should expose data-platform contracts without trying to become a full warehouse, lakehouse, dbt, Kafka, feature-store, and model-serving company at once.

Required data-platform contracts:

- Dataset versions can reference warehouse tables, object-storage snapshots, lakehouse table versions, or local files.
- Feature sets include schema version, transform code reference, freshness SLA, leakage checks, and quality checks.
- Workflow runs can record upstream dbt-style job IDs, batch pipeline IDs, or streaming checkpoint IDs when they exist.
- Lineage manifests can include Delta, Iceberg, Hudi, or equivalent table snapshot IDs when the selected data source supports them.
- Evaluation gates can block release when feature freshness, source completeness, or data-quality checks fail.
- Drift monitors record reference window, current window, metric, threshold, and affected slices.

Optional advanced contracts:

- Kafka or event-stream topic contract for online features or feedback events.
- Warehouse quality check summary.
- Lakehouse snapshot retention record.
- Feature freshness dashboard.
- Backfill run record.

Developer experience requirements:

- Platform consumers should have a short SDK or CLI path for registering artifacts and checking release status.
- Local development must run without cloud-only services.
- Gateway contracts should be documented with examples that application teams can copy.
- Error messages should tell teams which gate, artifact, policy, or permission blocked them.
- The platform README should include "first release in 30 minutes" local steps.

### Queue isolation

Use separate queues or workflow pools for:

- Dataset validation.
- Classical ML training.
- LLM adapter validation.
- Evaluation.
- Performance benchmark.
- Release promotion.
- Rollback verification.
- Telemetry aggregation.

Each queue needs:

- Idempotency key.
- Retry policy.
- Dead-letter queue.
- Timeout.
- Concurrency limit.
- Ownership dashboard.

### Durable handoff and reconciliation

Any handoff between API, workflow, worker, serving backend, or release controller must be recoverable.

Required pattern:

1. Write desired state to PostgreSQL.
2. Write an outbox event in the same transaction.
3. Worker or dispatcher processes the event.
4. Worker writes result and artifact references.
5. Reconciliation job compares desired state, observed state, and artifact existence.
6. Drifted state is repaired or escalated.

Examples:

- A release candidate exists but no evaluation workflow started.
- An evaluation passed but the release record was not updated.
- A canary was requested but traffic weights did not change.
- A rollback was requested but gateway policy still routes candidate traffic.
- An artifact is referenced by a registry row but is missing from object storage.

### Documentation and evidence system

Required living documents:

- `docs/problem-statement.md`
- `docs/architecture.md`
- `docs/adr-platform-boundaries.md`
- `docs/data-platform-contracts.md`
- `docs/developer-experience.md`
- `docs/data-model.md`
- `docs/api-contracts.md`
- `docs/model-gateway-contract.md`
- `docs/security-and-privacy.md`
- `docs/threat-model.md`
- `docs/evaluation-plan.md`
- `docs/observability-cost.md`
- `docs/deployment-runbook.md`
- `docs/rollback-runbook.md`
- `docs/capacity-plan.md`
- `docs/cost-comparison.md`
- `docs/platform-handoff.md`
- `docs/progress-log.md`

Required generated evidence:

- `reports/lineage/<release_id>.json`
- `reports/evals/<release_id>.md`
- `reports/load-tests/<run_id>.md`
- `reports/cost/<comparison_id>.md`
- `reports/canary/<release_id>.md`
- `reports/rollback/<rollback_id>.md`
- `reports/security/<run_id>.md`
- `reports/drift/<monitor_id>.md`

## 9. Data, artifact, event, and API contracts

### Tenant contract

```json
{
  "tenant_id": "tenant_support_ops",
  "display_name": "Support Ops",
  "allowed_artifact_namespaces": ["tenant_support_ops", "shared"],
  "monthly_budget_usd": 500.0,
  "request_limit_per_minute": 120,
  "policy_version": "tenant-policy-2026-07-28"
}
```

### Dataset manifest

```json
{
  "dataset_id": "sla-risk-2026-07-28",
  "tenant_id": "tenant_support_ops",
  "source_uri": "s3://modelmesh/datasets/sla-risk/raw/2026-07-28/",
  "version_hash": "sha256:...",
  "schema_version": "sla-risk-schema-v3",
  "split_manifest_uri": "s3://modelmesh/datasets/sla-risk/splits/v7.json",
  "row_count": 50000,
  "label_distribution": {
    "breach": 0.18,
    "no_breach": 0.82
  },
  "retention_class": "training-review",
  "created_by": "user_ml_eng_01"
}
```

### Feature set contract

```json
{
  "feature_set_id": "sla-risk-features-v12",
  "dataset_id": "sla-risk-2026-07-28",
  "schema_version": "feature-contract-v5",
  "freshness_sla_minutes": 60,
  "transform_code_ref": "git:abc123",
  "leakage_checks": ["no_future_status", "no_resolution_timestamp"],
  "quality_checks": ["not_null", "range", "category_membership", "drift_baseline"]
}
```

### Model package contract

```json
{
  "model_package_id": "sla-risk-xgb-0.8.0",
  "tenant_id": "tenant_support_ops",
  "model_type": "xgboost",
  "artifact_uri": "s3://modelmesh/models/sla-risk-xgb-0.8.0/model.joblib",
  "preprocessor_uri": "s3://modelmesh/models/sla-risk-xgb-0.8.0/preprocessor.joblib",
  "feature_set_id": "sla-risk-features-v12",
  "training_run_id": "train-20260728-001",
  "threshold_policy": {
    "default_threshold": 0.67,
    "business_cost_false_negative": 8.0,
    "business_cost_false_positive": 1.0
  },
  "checksum": "sha256:..."
}
```

### Adapter artifact contract

```json
{
  "adapter_id": "support-adapter-qlora-0.4.1",
  "tenant_id": "tenant_support_ops",
  "base_model_id": "llama-3.1-8b-instruct",
  "artifact_uri": "s3://modelmesh/adapters/support-adapter-qlora-0.4.1/",
  "adapter_type": "qlora",
  "training_run_id": "train-20260728-llm-003",
  "tokenizer_id": "llama-3.1-tokenizer",
  "chat_template_id": "chat-template-v2",
  "context_limit_tokens": 8192,
  "license_review_id": "license-review-021",
  "checksum": "sha256:..."
}
```

### Evaluation result contract

```json
{
  "evaluation_run_id": "eval-20260728-004",
  "candidate_id": "rc-20260728-007",
  "baseline_deployment_id": "prod-support-adapter-0.4.0",
  "dataset_versions": ["golden-prompts-v9", "safety-regression-v6"],
  "metrics": {
    "task_success": 0.82,
    "schema_validity": 0.98,
    "safety_violation_rate": 0.0,
    "p95_latency_ms": 1900,
    "cost_per_successful_task_usd": 0.018
  },
  "gate_decisions": {
    "quality": "pass",
    "safety": "pass",
    "latency": "pass",
    "cost": "pass"
  }
}
```

### Release candidate contract

```json
{
  "release_candidate_id": "rc-20260728-007",
  "tenant_id": "tenant_support_ops",
  "feature_id": "support_triage_assist",
  "artifact_refs": {
    "prompt_version": "support-prompt-v18",
    "base_model_version": "llama-3.1-8b-instruct",
    "adapter_version": "support-adapter-qlora-0.4.1",
    "gateway_policy": "gateway-policy-v11"
  },
  "lineage_manifest_uri": "s3://modelmesh/lineage/rc-20260728-007.json",
  "approval_status": "pending",
  "rollback_target_deployment_id": "deploy-prod-20260720-002"
}
```

### Gateway request contract

```json
{
  "tenant_id": "tenant_support_ops",
  "feature_id": "support_triage_assist",
  "trace_id": "trace-01J5...",
  "input": {
    "messages": [
      {"role": "user", "content": "Summarize this support ticket."}
    ]
  },
  "response_format": {
    "type": "json_schema",
    "schema_id": "ticket-summary-v3"
  },
  "stream": true
}
```

### Minimum API surface

Platform API:

- `POST /tenants`
- `GET /tenants/{tenant_id}/deployments`
- `POST /datasets`
- `POST /feature-sets`
- `POST /training-runs`
- `POST /model-packages`
- `POST /adapters`
- `POST /evaluation-runs`
- `POST /release-candidates`
- `POST /release-candidates/{id}/approve`
- `POST /deployments/{id}/canary`
- `POST /deployments/{id}/promote`
- `POST /deployments/{id}/rollback`
- `GET /lineage/{release_id}`
- `GET /costs`

Gateway API:

- `POST /v1/chat/completions`
- `POST /v1/responses` if implemented by the chosen SDK contract
- `POST /v1/embeddings` only if retrieval use cases require it
- `POST /v1/classical/score`
- `GET /healthz`
- `GET /readyz`
- `GET /metrics`

## 10. MLOps lifecycle

### End-to-end lifecycle

1. Register dataset or adapter artifact.
2. Validate schema, checksum, license, and policy.
3. Create workflow run.
4. Train or import artifact.
5. Register model package or adapter.
6. Run quality and safety evaluation.
7. Run serving performance evaluation.
8. Build lineage manifest.
9. Submit release candidate.
10. Approve or reject.
11. Deploy to staging.
12. Run smoke and shadow evaluation.
13. Start canary.
14. Promote or roll back.
15. Monitor drift, cost, errors, latency, and feedback.
16. Convert reviewed feedback into future training candidates.

### Required run states

Workflow run:

- `created`
- `queued`
- `running`
- `artifact_written`
- `evaluating`
- `gate_failed`
- `candidate_created`
- `completed`
- `failed`
- `cancelled`

Release candidate:

- `draft`
- `submitted`
- `lineage_verified`
- `evaluating`
- `blocked`
- `approved`
- `rejected`
- `staging`
- `shadow`
- `canary`
- `promoted`
- `rolled_back`
- `archived`

Deployment:

- `desired`
- `applying`
- `warming`
- `serving_shadow`
- `serving_canary`
- `serving_primary`
- `degraded`
- `rollback_requested`
- `rolling_back`
- `rolled_back`
- `failed`

### Release tuple

Each production-like deployment must have a release tuple:

```text
tenant_id
feature_id
gateway_policy_version
prompt_version
base_model_version
adapter_version or model_package_version
serving_backend_version
container_image_digest
dataset_version
evaluation_run_id
approval_id
deployment_id
```

## 11. Model gateway and serving lifecycle

### Gateway responsibilities

The gateway must:

- Authenticate caller.
- Resolve tenant and feature.
- Enforce request and spend limits.
- Resolve active deployment.
- Validate input size and schema.
- Apply routing policy.
- Check semantic, prefix, or response cache where permitted.
- Select hosted provider, self-hosted vLLM service, or classical ML scoring service.
- Stream response where supported.
- Validate structured output where required.
- Record token usage, latency, cache status, model version, and cost.
- Emit traces and metrics.
- Apply fallback if the configured policy allows it.

### Routing policy

A routing policy should include:

- Allowed providers.
- Preferred provider.
- Fallback provider order.
- Allowed models and adapters.
- Context-length limits.
- Timeout.
- Retry count.
- Circuit-breaker thresholds.
- Cache policy.
- Data-retention policy.
- Spend limit.
- Canary traffic weight.
- Shadow traffic setting.

### Caching policy

Caching must be explicit:

- Prefix caching for self-hosted serving is an inference optimization, not a product cache.
- Semantic or response caching can change user-visible behavior and must be enabled only for approved use cases.
- Cached responses must include artifact and policy versions.
- Tenant data cannot leak through shared cache keys.
- Cache hit rate must be visible in dashboards.
- Cache invalidation must be part of rollback.

### Self-hosted serving path

The full build should serve at least one LLM adapter through vLLM or SGLang with:

- OpenAI-compatible endpoint.
- Streaming.
- Continuous batching.
- Prefix or KV cache reporting.
- Adapter loading.
- Context and concurrency limits.
- Prometheus metrics.
- Resource requests and GPU scheduling.
- Quality check after any quantization or serving optimization.

### Classical ML serving path

The classical ML scoring path must include:

- Request schema.
- Feature validation.
- Model package version.
- Threshold policy.
- Score explanation or feature contribution summary where appropriate.
- Latency and error metrics.
- Drift and calibration monitoring plan.
- Rollback to prior package.

## 12. Evaluation and release gates

### Required datasets

Classical ML:

- Training split.
- Validation split.
- Holdout test split.
- Slice test set.
- Drift reference window.
- Business-threshold analysis set.

LLM:

- Golden functional prompts.
- Structured-output prompts.
- Safety regression set.
- Latency benchmark prompts with short, medium, and long contexts.
- Cost benchmark set.
- Optional human preference comparison set.

Platform:

- Gateway contract tests.
- Tenant isolation tests.
- Spend-limit tests.
- Provider fallback tests.
- Canary and rollback tests.
- Telemetry redaction tests.

### Starter release gates

Every release candidate must satisfy:

- Lineage manifest complete.
- Artifact checksums verified.
- License and policy checks complete.
- Dataset and feature freshness pass.
- Baseline quality is not worse than current production beyond an approved tolerance.
- Safety regression passes.
- Schema validity meets threshold.
- p95 latency within objective.
- Error rate within objective.
- Cost per successful task within objective.
- No unresolved critical security findings.
- Rollback target exists and is healthy.
- Approval recorded.

### Release comparison rules

Use these comparison rules:

- Candidate must compare against current production, not only against a static baseline.
- Candidate must include confidence intervals or repeated-run stability for noisy metrics.
- Quantized or optimized variants must rerun quality evaluation.
- A cheaper candidate that hurts task success must fail unless the business explicitly accepts the trade-off.
- A faster candidate that increases unsafe output must fail.
- A candidate that relies on stale data must fail.
- Manual override must require approver, reason, expiration, and follow-up task.

### Required release report

Each release report must include:

- Release tuple.
- Business objective.
- Candidate summary.
- Baseline deployment summary.
- Dataset and artifact lineage.
- Evaluation results.
- Gate decisions.
- Latency and throughput results.
- Cost comparison.
- Risk assessment.
- Approval record.
- Canary plan.
- Rollback target.
- Post-release monitoring plan.

### Minimum release dataset shape

For a portfolio project, keep datasets small enough to run but large enough to reveal real failures:

- At least 500 rows for the classical ML path, with clear labels and slices.
- At least 50 golden LLM prompts.
- At least 20 safety or policy regression cases.
- At least 3 sequence-length buckets for LLM latency tests.
- At least 2 traffic levels for load testing.
- At least 3 seeded failure drills.

## 13. Security, privacy, and governance

### Trust boundaries

Treat these as separate trust boundaries:

- User or application clients.
- Platform API.
- Gateway.
- Hosted model providers.
- Self-hosted inference service.
- Training jobs.
- Workflow orchestrator.
- Object storage.
- Registry database.
- Observability pipeline.
- Kubernetes control plane.
- Cloud provider account.

### Required controls

- Least-privilege service accounts.
- Workload identity or short-lived credentials.
- No secrets in code, images, notebooks, logs, or artifacts.
- Per-tenant authorization on every registry and gateway request.
- Artifact checksum validation.
- Container image scanning.
- Dependency vulnerability scanning.
- Signed or digest-pinned images for deployment.
- Network restrictions between components.
- Sensitive telemetry redaction.
- Audit logs for artifact registration, approval, deployment, rollback, and policy changes.
- Human approval for production-like promotion and rollback unless automated rollback policy is explicitly approved.
- Retention policy for datasets, prompts, outputs, telemetry, and model artifacts.

### Governance documents

The repo must include:

- Dataset card.
- Model card or adapter card.
- Classical ML threshold decision memo.
- Serving decision memo.
- Security and privacy checklist.
- Threat model.
- Release approval policy.
- Rollback policy.
- Data retention policy.
- Cost allocation policy.

### Prohibited claims

Do not claim:

- Production readiness without demonstrated rollback.
- Cost optimization without quality-after-optimization evaluation.
- Tenant safety without negative authorization tests.
- Reproducibility without immutable artifacts and lineage.
- MLOps maturity from MLflow screenshots alone.
- Kubernetes competence from a single untested manifest.
- Inference optimization from a single happy-path latency number.
- Autonomous remediation unless all authorization, approval, audit, idempotency, and rollback rules are proven.

## 14. Observability, feedback, and cost

### Correlation model

Every request should carry:

- `trace_id`
- `tenant_id`
- `feature_id`
- `gateway_policy_version`
- `deployment_id`
- `release_candidate_id`
- `model_package_id` or `adapter_id`
- `prompt_version`
- `provider`
- `serving_backend`
- `cache_status`
- `cost_event_id`

### Metrics

Gateway:

- Request rate.
- Error rate.
- p50, p95, and p99 latency.
- Timeout rate.
- Retry count.
- Circuit-breaker state.
- Cache hit rate.
- Input and output tokens.
- Cost per request.
- Cost per successful task.
- Spend-limit blocks.

Serving:

- TTFT.
- Inter-token latency.
- Tokens per second.
- Queue time.
- Batch size.
- GPU utilization.
- GPU memory.
- KV cache utilization.
- Prefix cache hit rate.
- Context length distribution.

Workflow:

- Run success rate.
- Run duration.
- Queue latency.
- Artifact write failures.
- Gate pass or fail counts.
- Dead-letter count.

Classical ML:

- Score distribution.
- Calibration.
- Drift.
- Feature freshness.
- Data-quality failures.
- Prediction latency.

Release:

- Canary conversion status.
- Rollback events.
- Gate failures by reason.
- Manual overrides.
- Approval latency.

### Dashboards

Build at least:

- Platform overview dashboard.
- Gateway traffic and cost dashboard.
- Inference performance dashboard.
- Release and canary dashboard.
- Workflow and registry dashboard.
- Classical ML drift dashboard.
- Tenant cost dashboard.
- Operator incident dashboard.

### Feedback loop

Feedback must be reviewed before training:

1. User or operator feedback is collected.
2. Feedback is linked to deployment version and trace ID.
3. Sensitive content is redacted or excluded.
4. Candidate training examples are reviewed.
5. Approved examples are added to a new dataset version.
6. Retraining or adapter update runs through normal gates.

## 15. Reliability, deployment, and rollback

### Required service indicators

Define SLIs and objectives for:

- Gateway availability.
- Gateway p95 latency.
- Gateway error rate.
- Inference TTFT.
- Tokens per second.
- Queue time.
- Workflow success rate.
- Evaluation run success rate.
- Canary decision latency.
- Rollback duration.
- Cost attribution completeness.

### Degraded modes

Document and test:

- Hosted provider unavailable.
- Self-hosted inference saturated.
- GPU unavailable.
- Registry database unavailable.
- Object storage unavailable.
- Workflow orchestrator unavailable.
- Evaluation worker dead-letter backlog.
- Cost service unavailable.
- Telemetry collector unavailable.
- Stale policy cache.

### Rollback options

The platform must support:

- Gateway traffic rollback to previous release.
- Prompt version rollback.
- Adapter version rollback.
- Model package rollback.
- Routing policy rollback.
- Canary stop.
- Provider disable.
- Cache bypass or clear.
- Kubernetes deployment rollback.
- Configuration rollback.

### Rollback verification

After rollback, verify:

- Gateway policy points to previous known-good deployment.
- Health checks pass.
- Smoke evaluation passes.
- Error rate returns to normal.
- Latency returns to normal.
- Cost events continue to emit.
- No canary traffic remains on the failed candidate.
- Rollback report is written.

## 16. Step-by-step implementation plan

### Phase 0: Discovery, platform scope, and acceptance criteria

- Select one classical ML workload and one LLM adapter workload.
- Define tenants, features, traffic expectations, quality objectives, latency objectives, and cost budget.
- Write problem statement and platform boundary ADR.
- Define release tuple and evidence package.

### Phase 1: Repository, contracts, and local platform

- Create monorepo structure.
- Add platform API, gateway API, worker, workflow, registry package, and docs directories.
- Add Docker Compose for PostgreSQL, Redis, object storage, MLflow, Prometheus, and Grafana.
- Add lint, type, test, and format gates.

### Phase 2: Identity, tenancy, and registry database

- Implement tenants, users, roles, features, artifacts, approvals, releases, deployments, audit, and outbox.
- Add authorization tests.
- Seed a shared namespace and one tenant namespace.

### Phase 3: Artifact store and lineage manifest

- Add object storage bucket layout.
- Register datasets, prompts, model packages, adapters, and evaluation artifacts.
- Enforce checksums and immutable records.
- Generate lineage manifests.

### Phase 4: Classical ML workflow

- Add tabular dataset validation.
- Train baseline and candidate models.
- Track runs in MLflow.
- Register model package.
- Evaluate quality, calibration, threshold utility, slices, and drift reference.

### Phase 5: LLM adapter validation

- Import or create one adapter artifact.
- Validate base model, tokenizer, chat template, context length, license, and checksum.
- Run golden prompt, structured-output, safety, latency, and cost evaluations.

### Phase 6: Workflow orchestration

- Implement Airflow, Dagster, or a local workflow runner with explicit DAGs.
- Add idempotent jobs, retries, dead-letter handling, and run-state updates.
- Add reconciliation.

### Phase 7: Gateway and provider abstraction

- Implement provider-neutral gateway contract.
- Add hosted-provider adapter or mock for local path.
- Add self-hosted serving adapter.
- Add classical scoring route.
- Enforce limits, routing policy, fallback, cache rules, and telemetry.

### Phase 8: Serving backend and inference benchmark

- Run vLLM or SGLang in the full path.
- Serve the adapter.
- Test streaming, concurrency, context limits, batching, and cache metrics.
- Benchmark TTFT, tokens/sec, p95 latency, queue time, GPU utilization, and cost.

### Phase 9: Release controller and canary

- Create release candidate lifecycle.
- Add approval workflow.
- Deploy to staging.
- Route shadow or canary traffic.
- Evaluate canary metrics.
- Promote or roll back.

### Phase 10: Observability and cost

- Add OpenTelemetry traces.
- Export Prometheus metrics.
- Build Grafana dashboards.
- Emit cost events by tenant, feature, provider, model, adapter, and deployment.
- Add redaction tests.

### Phase 11: Kubernetes and cloud IaC

- Containerize services as non-root images.
- Add Kubernetes manifests or Helm chart.
- Add resource requests, limits, liveness, readiness, autoscaling, and GPU scheduling.
- Add Terraform for selected cloud resources.
- Add budget and tagging controls.

### Phase 12: Reliability and failure injection

- Test provider throttling.
- Test gateway timeout.
- Test worker dead-letter behavior.
- Test object storage failure.
- Test registry unavailable behavior.
- Test saturated inference service.
- Test failed canary and rollback.

### Phase 13: Portfolio proof and handoff

- Generate load-test report.
- Generate hosted-versus-self-hosted cost report.
- Generate rollback report.
- Generate release report.
- Write platform README and handoff docs.
- Record demo script or walkthrough.

## 17. Completion evidence checklist

### Product and platform

- Problem statement.
- Platform boundary ADR.
- Tenant and feature model.
- Self-service workflow description.
- Platform consumer README.

### Data and artifacts

- Dataset card.
- Feature set contract.
- Prompt registry entries.
- Model package record.
- Adapter record.
- Checksums and immutable artifact URIs.
- Lineage manifests.

### Training and orchestration

- Workflow DAG.
- MLflow run records.
- DVC or equivalent dataset versioning.
- Classical ML model package.
- Adapter validation workflow.
- Reconciliation job.

### Evaluation

- Quality report.
- Safety regression report.
- Classical ML calibration and threshold report.
- Slice and drift reference report.
- LLM benchmark report.
- Gate decision report.

### Serving and release

- Model gateway.
- Hosted-provider route.
- Self-hosted route.
- Classical scoring route.
- Routing and fallback policy.
- Shadow or canary demo.
- Rollback demo.
- Release report.

### Infrastructure

- Docker Compose local stack.
- Container images.
- Kubernetes manifests or Helm chart.
- Terraform or IaC modules.
- Health and readiness checks.
- GPU scheduling demonstration.
- Backup and restore notes.

### Observability and cost

- Trace screenshot or trace export.
- Prometheus metrics.
- Grafana dashboards.
- Cost report.
- Capacity plan.
- Alerts and runbooks.

### Security and governance

- Threat model.
- Authorization tests.
- Secret handling proof.
- Telemetry redaction tests.
- Audit log examples.
- Approval records.
- Retention policy.

### Portfolio

- README.
- Demo script.
- What failed and what changed section.
- Interview defense notes.
- Final definition of done.

## 18. Industry-level implementation order

Build in this order:

1. Define platform contract, release tuple, and evidence package.
2. Implement registry, artifact store, tenancy, audit, and immutable lineage.
3. Add the smallest useful classical ML workflow.
4. Add the smallest useful LLM adapter registration and validation path.
5. Add evaluation gates before release automation.
6. Add gateway routing and cost attribution.
7. Add local serving and hosted-provider comparison.
8. Add release candidate, approval, staging, canary, and rollback.
9. Add observability dashboards and runbooks.
10. Add Kubernetes and IaC.
11. Add load tests, capacity plan, and failure drills.
12. Add optional `IncidentPilot` only after deterministic operational telemetry works.

This order prevents the common mistake of deploying a flashy serving endpoint before the platform can prove lineage, gates, cost, and rollback.

## 19. Optional IncidentPilot satellite

For MLOps, platform, or SRE targeting, add `IncidentPilot` only after the baseline platform is working.

It should:

- Correlate logs, metrics, traces, queue state, provider failures, deployment events, and evaluation regressions.
- Build an incident timeline.
- Produce ranked hypotheses with supporting and contradicting evidence.
- Retrieve relevant runbook steps.
- Draft an incident update or postmortem.
- Remain read-only by default.
- Require human approval for any restart, scale, rollback, feature flag, or traffic-routing action.
- Record exact arguments, approver, result, verification, and rollback status.

Required proof:

- Three seeded failure drills.
- Evidence-backed hypothesis report.
- Human-approved non-production runbook simulation.
- Red-team test proving telemetry text cannot inject unauthorized actions.

## 20. Common failure modes

- MLflow exists but artifacts are not connected to releases.
- Datasets are versioned but features, prompts, or adapters are not.
- Candidate is compared to a weak baseline instead of current production.
- Quantized model is benchmarked for speed but not reevaluated for quality.
- Canary routing changes traffic but cannot be verified.
- Rollback changes code but not gateway routing policy.
- Cache leaks tenant data or hides release regressions.
- Cost report uses cost per token but ignores task success.
- Kubernetes manifests omit resource requests, limits, readiness, or rollback.
- GPU benchmark uses unrealistic context length or concurrency.
- Gateway fallback silently changes behavior without telemetry.
- Human approval is stored in a note but not enforced in code.
- Observability captures sensitive prompts or feature values.
- Continuous training uses raw feedback without review.
- Platform claims multi-tenancy but authorization tests cover only read paths.

## 21. Interview defense questions

Product and platform:

- What platform problem does `ModelMesh` solve?
- Why is this a platform project instead of a single app?
- Which workflows are self-service and which require approval?
- What did you deliberately leave out?

Architecture:

- Why did you choose modular monolith, workers, or services?
- What owns artifact state?
- Where are transaction boundaries?
- How do you recover from partial workflow failure?

MLOps:

- What is included in your release tuple?
- How do you prove lineage?
- What blocks a release?
- How does production feedback become training data safely?

Serving:

- What is continuous batching?
- What is KV cache?
- How do context length and concurrency affect capacity?
- How do you serve multiple adapters?
- Why compare hosted and self-hosted routes?

Reliability:

- How does canary rollout work?
- How does rollback work?
- What degraded modes did you test?
- What are your SLIs and SLOs?

Cost:

- Why use cost per successful task?
- How do you attribute cost by tenant and feature?
- How does caching affect cost and quality?
- When is self-hosting not worth it?

Security:

- How do tenants stay isolated?
- How are secrets handled?
- What telemetry is redacted?
- How do you prevent unauthorized deployment or rollback?

## 22. Final definition of done

`ModelMesh` is done when:

- The platform can register and version datasets, prompts, model packages, adapters, evaluations, release candidates, deployments, approvals, and rollback records.
- A classical ML model can move from dataset to training run to model package to evaluation to approved release to scoring endpoint.
- An LLM adapter can move from artifact registration to validation to evaluation to gateway route to benchmark to canary.
- A release candidate cannot promote without lineage, gates, approval, and rollback target.
- Gateway requests are tenant-aware, cost-attributed, traceable, and policy-controlled.
- The full path deploys to Kubernetes with resource controls and health checks.
- Inference benchmarks report TTFT, tokens/sec, p95 latency, queue time, GPU utilization, quality deltas, and cost.
- A failed canary can be rolled back and verified.
- Observability, cost, security, and handoff reports are present.
- A reviewer can reproduce the core workflow and defend the trade-offs in an interview.
