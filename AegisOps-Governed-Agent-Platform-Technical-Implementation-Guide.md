# AegisOps Governed Agent Platform Technical Implementation Guide

Project codename: `AegisOps`

This guide turns the production plan into an executable implementation sequence for a governed, multilingual, multi-provider enterprise agent platform. The target system supports case intake, provider routing, permission-aware RAG, governed memory, bounded agent workflows, approval-gated tools, secured MCP integration, A2A handoff, bilingual evaluation, safe replay, observability, rollout, rollback, and failover.

## How to use this guide

Build the project in stages. Do not start with an autonomous agent loop. Start with typed services, deterministic workflow state, authorization, audit, and evaluation fixtures. Add model planning only after the platform can reject unsafe actions without help from the model.

The recommended order:

1. Contracts, data model, and deterministic workflow.
2. Identity, authorization, audit, and approval.
3. Provider gateway and structured output.
4. Permission-aware retrieval.
5. Governed memory.
6. Bounded agent runtime.
7. Tools, MCP, and A2A.
8. Safety, bilingual evaluation, and red teaming.
9. Safe replay, observability, cost, and release gates.
10. Deployment, canary, rollback, failover, and final proof.

## 0. Scope, non-goals, and prerequisites

### In scope

The implementation must include:

- Tenant and user identity.
- Case intake API.
- Explicit workflow state graph.
- Provider-neutral model interface.
- Fake provider for tests.
- Primary provider adapter.
- Alternate provider adapter or deterministic substitute.
- Open-model route or stub.
- Prompt and output schema registry.
- Permission-aware hybrid retrieval.
- Citation validation and abstention.
- Governed memory categories and policy.
- Read tools.
- At least one approval-gated write tool.
- Tool argument validation.
- Idempotency, retries, timeouts, verification, and compensation.
- Secured MCP capability.
- One authenticated A2A handoff.
- Human approval package.
- Safe replay.
- English and Arabic evaluation datasets.
- Prompt-injection, malicious tool-output, unauthorized-write, cross-tenant, and memory tests.
- Multimodal input slice.
- Observability, cost, and budgets.
- Canary, rollback, failover, restore, and failure drills.

### Non-goals for the first production-style version

Do not build:

- Unsupervised high-impact actions.
- General web browsing.
- Arbitrary dynamic tool discovery.
- Real destructive infrastructure remediation.
- Real regulated production data handling.
- Legal compliance certification.
- Every agent framework.
- Every model provider.
- Feature parity across Python and .NET.
- Hidden chain-of-thought capture.

### Local prerequisites

Use pinned versions:

- Python 3.11 or 3.12.
- FastAPI.
- Pydantic.
- SQLAlchemy or SQLModel.
- Alembic.
- PostgreSQL.
- pgvector or FAISS.
- OpenSearch or Elasticsearch where available.
- Redis.
- Object storage such as MinIO.
- OpenTelemetry.
- Prometheus and Grafana or equivalent.
- Docker and Docker Compose.
- Pytest.
- Mypy.

Optional:

- LangGraph or one selected workflow framework after manual graph implementation.
- MCP SDK.
- A2A SDK or authenticated service-to-service implementation.
- vLLM or TensorRT-LLM route from a prior ModelMesh path.
- Kubernetes.
- Terraform.
- ASP.NET Core vertical slice for .NET lane.

### Pre-build discovery gate

Create:

- `docs/problem-statement.md`
- `docs/product-requirements.md`
- `docs/workflow-map.md`
- `docs/risk-taxonomy.md`
- `docs/allowed-prohibited-actions.md`
- `docs/residency-assumptions.md`
- `docs/evidence-package.md`

Answer:

- Which domain does the operations case represent?
- Which actions are read-only, draft-only, low-risk write, high-impact, or prohibited?
- Which human roles can approve which actions?
- Which tenant and language cases are supported?
- Which sources can be retrieved?
- Which memory categories are allowed?
- Which MCP capability is implemented?
- Which A2A handoff is implemented?
- Which provider paths are real and which are stubs?
- Which failure drills prove readiness?

### Canonical executable stack

Use this repository shape:

- `apps/case-api`: case intake, operator APIs, approvals, replay, admin APIs.
- `apps/agent-runtime`: state graph executor, provider calls, budget enforcement, transitions.
- `apps/worker`: ingestion, indexing, evaluation, memory expiry, replay export, reports.
- `apps/mcp-server`: secured MCP capability, such as read-only policy search.
- `apps/a2a-specialist`: specialist handoff service.
- `packages/aegisops-contracts`: Pydantic contracts.
- `packages/aegisops-db`: models, migrations, repositories.
- `packages/aegisops-gateway`: provider interfaces, adapters, routing, cost.
- `packages/aegisops-retrieval`: ingestion, hybrid retrieval, reranking, citations.
- `packages/aegisops-memory`: memory policy, stores, correction, deletion, evaluation.
- `packages/aegisops-policy`: authorization, risk, approval, capability policy.
- `packages/aegisops-tools`: tool schemas, implementations, idempotency, verification.
- `packages/aegisops-evals`: bilingual, tool, memory, safety, red-team, judge calibration.
- `packages/aegisops-observability`: traces, metrics, redaction, replay, cost.
- `infra`: Docker Compose, Kubernetes, Terraform, Prometheus, Grafana.
- `docs`: living docs.
- `reports`: generated evidence.

## 1. Final system and invariants

### Final system

Runtime services:

- Case API.
- Agent runtime.
- Model gateway.
- Retrieval service.
- Memory service.
- Policy service.
- Tool service.
- Approval service.
- MCP server or client.
- A2A specialist service.
- Worker.
- Replay service.
- Evaluation service.
- Observability stack.

Storage:

- PostgreSQL.
- Vector store.
- Search index.
- Redis.
- Object storage.
- Audit log storage.

### Core invariants

Authorization:

- Model output never grants permission.
- Every retrieval, memory, tool, MCP, and A2A request has user, tenant, purpose, policy version, and trace ID.
- A consequential write cannot execute without exact approval.
- Approval is invalid if tool, target, or arguments change.

Workflow:

- Every workflow run uses explicit states.
- Every transition is recorded.
- Every loop has max step, time, token, context, tool, and spend limits.
- Every terminal state records outcome and reason.

Memory:

- Request context, session state, workflow state, preferences, retrieval-backed memory, and summaries are separated.
- Durable memory writes require policy decision, purpose, provenance, classification, retention, and deletion behavior.
- Derived summaries, indexes, and caches inherit correction and deletion behavior.

Tooling:

- Tool inputs and outputs are schema-validated.
- Writes use idempotency keys.
- Tool results are untrusted.
- MCP capabilities are allowlisted and version pinned.
- A2A handoff propagates identity and policy context.

Replay:

- Safe replay stores redacted state and decisions.
- Safe replay does not store hidden chain-of-thought.
- Replay access is authorized and audited.

## 2. Starter quality gates

Baseline gates:

- Deterministic workflow path works without agent planning.
- Identity and tenant authorization tests pass.
- Audit events exist for case, approval, tool, memory, MCP, A2A, release, and rollback actions.
- Structured output validity reaches at least 95 percent on the starter set.

Agent gates:

- Task-completion threshold is defined from baseline.
- Invalid-action rate is zero for critical cases.
- Step, time, token, and spend budgets stop runs.
- Escalation happens when evidence or policy is insufficient.

Retrieval and memory gates:

- Unauthorized evidence leakage is zero.
- Citation validation passes threshold.
- Memory cross-tenant leakage is zero.
- Memory expiry and deletion tests pass.
- Memory write policy blocks poisoned or unsupported writes.

Tool and approval gates:

- Unauthorized writes are blocked.
- Approval bypass attempts fail.
- Duplicate writes are prevented.
- Tool argument mutation after approval fails.
- Verification and compensation paths are tested.

MCP and A2A gates:

- Unapproved MCP server is rejected.
- Malicious MCP tool description is contained.
- MCP result-size and schema limits are enforced.
- A2A handoff without valid identity or policy is rejected.

Bilingual and safety gates:

- English and Arabic results are reported separately.
- Arabic prompt-injection cases are included.
- Refusal and over-refusal are measured.
- PII and secret redaction tests pass.

## 3. Build order

1. Repository and local services.
2. Contracts and schema.
3. Identity, tenant, roles, audit.
4. Case intake and deterministic workflow.
5. Approval package and policy service.
6. Provider gateway and structured output.
7. Retrieval ingestion and evidence packets.
8. Governed memory.
9. Agent state graph.
10. Read tools.
11. Approval-gated write tools.
12. MCP capability.
13. A2A handoff.
14. Bilingual and red-team evaluation.
15. Multimodal slice.
16. Safe replay.
17. Observability and cost.
18. Release gates.
19. Deployment, failover, rollback, restore.
20. Final evidence manifest.

## 4. Beginner milestones

Milestone 1:

- Case API starts.
- Database migrations run.
- Case can be created and audited.

Milestone 2:

- Deterministic workflow reaches terminal state.
- Approval-gated write proposal is produced but not executed.

Milestone 3:

- Fake provider returns structured output.
- Invalid structured output is blocked.

Milestone 4:

- Retrieval returns permitted citations.
- Unauthorized document is excluded.

Milestone 5:

- Memory write policy allows and denies seeded cases.
- Deletion invalidates derived summary.

Milestone 6:

- Tool executes only after approval.
- Duplicate write is blocked by idempotency.

Milestone 7:

- MCP capability and A2A handoff are tested.
- Malicious MCP fixture is blocked.

Milestone 8:

- English and Arabic evals run.
- Safe replay exports a redacted timeline.

## 5. Target repository and artifact manifest

### Repository structure

```text
aegisops/
  README.md
  pyproject.toml
  requirements.txt
  requirements-dev.txt
  docker-compose.yml
  .env.example
  apps/
    case-api/
      aegisops_case_api/
        __init__.py
        main.py
        settings.py
        dependencies.py
        auth.py
        routes/
          health.py
          cases.py
          workflow_runs.py
          approvals.py
          evidence.py
          memory.py
          capabilities.py
          replay.py
          evals.py
          releases.py
    agent-runtime/
      aegisops_agent_runtime/
        __init__.py
        main.py
        state_graph.py
        executor.py
        budgets.py
        transitions.py
        planner.py
        verifier.py
        recovery.py
    worker/
      aegisops_worker/
        __init__.py
        main.py
        queues.py
        jobs/
          ingest_sources.py
          build_indexes.py
          run_evals.py
          expire_memory.py
          delete_memory.py
          export_replay.py
          release.py
          rollback.py
          reports.py
    mcp-server/
      aegisops_mcp_server/
        __init__.py
        main.py
        auth.py
        tools.py
        audit.py
    a2a-specialist/
      aegisops_a2a_specialist/
        __init__.py
        main.py
        handoff.py
        auth.py
  packages/
    aegisops-contracts/
      aegisops_contracts/
        __init__.py
        cases.py
        workflow.py
        providers.py
        retrieval.py
        memory.py
        tools.py
        approvals.py
        mcp.py
        a2a.py
        evals.py
        telemetry.py
        releases.py
    aegisops-db/
      aegisops_db/
        __init__.py
        models.py
        repositories.py
        session.py
        migrations/
    aegisops-gateway/
      aegisops_gateway/
        __init__.py
        providers/
          base.py
          fake.py
          primary.py
          alternate.py
          open_model.py
        routing.py
        schemas.py
        costs.py
        errors.py
    aegisops-retrieval/
      aegisops_retrieval/
        __init__.py
        ingestion.py
        chunking.py
        embeddings.py
        lexical.py
        dense.py
        hybrid.py
        reranking.py
        citations.py
        access.py
        reports.py
    aegisops-memory/
      aegisops_memory/
        __init__.py
        policy.py
        stores.py
        writes.py
        correction.py
        deletion.py
        expiry.py
        summaries.py
        evals.py
    aegisops-policy/
      aegisops_policy/
        __init__.py
        authorization.py
        risk.py
        approvals.py
        capabilities.py
        residency.py
    aegisops-tools/
      aegisops_tools/
        __init__.py
        registry.py
        schemas.py
        policy_search.py
        ticket_lookup.py
        asset_lookup.py
        ticket_update.py
        notification.py
        verification.py
        compensation.py
    aegisops-evals/
      aegisops_evals/
        __init__.py
        datasets.py
        agent.py
        retrieval.py
        memory.py
        tools.py
        mcp.py
        a2a.py
        safety.py
        bilingual.py
        judge_calibration.py
        reports.py
    aegisops-observability/
      aegisops_observability/
        __init__.py
        tracing.py
        metrics.py
        logging.py
        redaction.py
        replay.py
        costs.py
  infra/
    docker/
      Dockerfile.case-api
      Dockerfile.agent-runtime
      Dockerfile.worker
      Dockerfile.mcp-server
      Dockerfile.a2a-specialist
    prometheus/
      prometheus.yml
    grafana/
      dashboards/
      provisioning/
    k8s/
      namespace.yaml
      case-api.yaml
      agent-runtime.yaml
      worker.yaml
      mcp-server.yaml
      a2a-specialist.yaml
    terraform/
      environments/
        staging/
  docs/
    problem-statement.md
    product-requirements.md
    workflow-map.md
    architecture.md
    adr-architecture-boundaries.md
    adr-agent-runtime.md
    adr-provider-framework-portability.md
    adr-retrieval-memory.md
    adr-mcp-a2a.md
    adr-residency.md
    data-model.md
    api-contracts.md
    tool-contracts.md
    mcp-contract.md
    a2a-contract.md
    memory-policy.md
    approval-policy.md
    security-threat-model.md
    evaluation-plan.md
    bilingual-evaluation-plan.md
    observability-replay.md
    deployment-runbook.md
    rollback-runbook.md
    platform-handoff.md
    progress-log.md
  reports/
    evals/
    retrieval/
    memory/
    tools/
    security/
    mcp/
    a2a/
    replay/
    cost/
    localization/
    residency/
    failure-injection/
    release/
    business/
  tests/
    api/
    auth/
    db/
    providers/
    retrieval/
    memory/
    runtime/
    tools/
    mcp/
    a2a/
    evals/
    security/
    deployment/
```

### Required artifact outputs

Generate:

- `reports/evals/agent-eval-report.md`
- `reports/evals/bilingual-eval-report.md`
- `reports/evals/judge-calibration-report.md`
- `reports/retrieval/retrieval-benchmark.md`
- `reports/memory/memory-quality-report.md`
- `reports/memory/deletion-expiry-report.md`
- `reports/tools/tool-contract-report.md`
- `reports/security/red-team-report.md`
- `reports/security/unauthorized-action-report.md`
- `reports/mcp/mcp-security-report.md`
- `reports/a2a/a2a-handoff-report.md`
- `reports/replay/safe-replay-report.md`
- `reports/cost/cache-cost-report.md`
- `reports/localization/arabic-rtl-report.md`
- `reports/residency/residency-control-record.md`
- `reports/failure-injection/failure-drill-report.md`
- `reports/release/canary-rollback-failover-report.md`
- `reports/business/business-outcome-report.md`
- `reports/final-evidence-manifest.json`

## 6. Data model

### Core tables

Identity and tenancy:

- `tenants`
- `users`
- `roles`
- `tenant_memberships`
- `service_accounts`
- `policy_versions`

Cases and workflow:

- `cases`
- `case_attachments`
- `workflow_runs`
- `workflow_transitions`
- `workflow_budgets`
- `workflow_checkpoints`
- `workflow_failures`

Providers and prompts:

- `model_providers`
- `model_routes`
- `prompt_versions`
- `output_schema_versions`
- `provider_calls`
- `cost_events`
- `cache_events`

Retrieval:

- `sources`
- `source_versions`
- `documents`
- `chunks`
- `embeddings`
- `indexes`
- `retrieval_runs`
- `evidence_items`
- `citation_checks`
- `access_decisions`

Memory:

- `memory_items`
- `memory_policy_decisions`
- `memory_write_requests`
- `memory_corrections`
- `memory_deletions`
- `memory_expiry_events`
- `memory_derived_artifacts`

Tools and approvals:

- `capabilities`
- `tool_definitions`
- `tool_calls`
- `tool_results`
- `action_proposals`
- `approvals`
- `idempotency_keys`
- `verification_results`
- `compensation_events`

MCP and A2A:

- `mcp_servers`
- `mcp_capabilities`
- `mcp_sessions`
- `mcp_calls`
- `a2a_agents`
- `a2a_handoffs`
- `a2a_results`

Evaluation and release:

- `eval_datasets`
- `eval_cases`
- `eval_runs`
- `eval_results`
- `judge_calibration_runs`
- `red_team_runs`
- `release_candidates`
- `deployments`
- `rollback_events`

Observability and audit:

- `audit_events`
- `replay_snapshots`
- `replay_exports`
- `outbox_events`
- `dead_letters`
- `reconciliation_findings`

### Required constraints

- `workflow_transitions` must reference valid previous and next states.
- `action_proposals` must include tool, target, arguments hash, evidence refs, idempotency key, verification method, and compensation plan.
- `approvals` must include approver, policy version, expiry, approved tool, and approved arguments hash.
- `tool_calls` cannot execute unless required approval exists and is unexpired.
- `memory_items` must include tenant, subject, purpose, provenance, classification, consent state, version, and expiry.
- `retrieval_runs` must include tenant and access filter policy.
- `mcp_calls` must reference an approved capability version.
- `a2a_handoffs` must include identity context and policy context.
- `replay_snapshots` must be redaction-checked before export.
- `release_candidates` must reference prompt, provider route, retrieval, memory, tool, policy, eval, and deployment versions.

### Data invariants

- No workflow can transition from proposed action to execution without approval.
- No approval can be reused with changed arguments.
- No durable memory can be written from untrusted tool output without policy and provenance.
- No retrieval evidence can enter context if access is denied.
- No MCP capability can run if disabled or version-mismatched.
- No A2A result can update source workflow state without response schema validation.
- No replay export can include hidden chain-of-thought or unredacted sensitive data.

### Outbox and reconciliation

Outbox events:

- `case_accepted`
- `workflow_run_requested`
- `retrieval_requested`
- `memory_write_requested`
- `approval_requested`
- `tool_execution_requested`
- `mcp_call_requested`
- `a2a_handoff_requested`
- `eval_run_requested`
- `replay_export_requested`
- `rollback_requested`

Reconciliation checks:

- Approval package missing after proposal.
- Approval expired but tool execution queued.
- Tool executed but verification missing.
- Memory deletion requested but derived artifacts active.
- Source access revoked but cache still valid.
- MCP server disabled but capability still advertised.
- A2A handoff succeeded but workflow not resumed.
- Provider route disabled but traffic still present.
- Safe replay report missing for audited run.

## 7. API contracts

### Create case

Request:

```json
{
  "tenant_id": "tenant_ops_uae",
  "language": "ar",
  "content": "Case text",
  "requested_outcome": "Draft and approve a ticket update",
  "attachments": []
}
```

Response:

```json
{
  "case_id": "case_20260728_001",
  "status": "accepted",
  "workflow_run_id": null
}
```

### Start workflow run

Request:

```json
{
  "case_id": "case_20260728_001",
  "runtime_policy_version": "runtime-policy-v3",
  "max_steps": 12,
  "max_cost_usd": 1.25
}
```

Response:

```json
{
  "workflow_run_id": "run_20260728_001",
  "state": "accepted"
}
```

### Approval decision

Request:

```json
{
  "proposal_id": "proposal_001",
  "decision": "approved",
  "approver_id": "user_manager_01",
  "reason": "Evidence supports the low-risk ticket update."
}
```

Response:

```json
{
  "approval_id": "approval_001",
  "status": "approved",
  "expires_at": "2026-07-28T11:00:00Z"
}
```

### Memory deletion

Request:

```json
{
  "memory_id": "mem_001",
  "requested_by": "user_123",
  "reason": "User correction request",
  "delete_derived_artifacts": true
}
```

Response:

```json
{
  "deletion_id": "memdel_001",
  "status": "queued",
  "verification_status": "pending"
}
```

### Safe replay

Response:

```json
{
  "workflow_run_id": "run_20260728_001",
  "redaction_policy_version": "replay-redaction-v4",
  "events": [
    {
      "state": "evidence_retrieved",
      "summary": "Retrieved two permitted policy chunks.",
      "trace_id": "trace_001",
      "timestamp": "2026-07-28T10:05:00Z"
    }
  ],
  "contains_hidden_reasoning": false
}
```

### Capability-aware readiness

Response:

```json
{
  "status": "ready",
  "capabilities": {
    "database": "ready",
    "model_gateway": "ready",
    "retrieval": "ready",
    "memory": "ready",
    "policy": "ready",
    "tools": "ready",
    "mcp": "ready",
    "a2a": "degraded",
    "replay": "ready",
    "evals": "ready"
  }
}
```

## 8. Stage 1 - Reproducible repository and local services

### Objective

Create a fresh-clone runnable project.

### Implement

- Repository skeleton.
- Dependency files.
- Docker Compose with PostgreSQL, Redis, object storage, vector/search substitute, Prometheus, Grafana.
- `.env.example`.
- Health and readiness routes.
- Formatting, linting, type, and test commands.

### Done when

- Services boot locally.
- Tests run.
- Health and readiness work.
- No secrets are committed.

## 9. Stage 2 - Contracts, schema, and migrations

### Objective

Define the platform contracts before model behavior.

### Implement

- Pydantic contracts for cases, workflow, providers, retrieval, memory, tools, approvals, MCP, A2A, evals, and telemetry.
- Database models.
- Alembic migrations.
- Seed tenant, users, roles, policies, and fake provider.
- Constraint tests.

### Done when

- Empty database migrates.
- Seed data is deterministic.
- Contracts validate happy and failing fixtures.
- Docs match implemented schema.

## 10. Stage 3 - Identity, authorization, audit, and risk policy

### Objective

Make authorization and audit work before agent planning.

### Implement

- Local identity stub.
- Role checks.
- Tenant checks.
- Risk taxonomy.
- Authorization policy service.
- Audit writer.
- Policy versioning.
- Negative authorization tests.

### Done when

- Cross-tenant case access is denied.
- Unauthorized tool request is denied.
- Policy decision is audited.
- Risk taxonomy maps actions to approval requirements.

## 11. Stage 4 - Case intake and deterministic workflow baseline

### Objective

Implement a non-agentic baseline workflow.

### Implement

- Case intake route.
- Workflow run creation.
- Explicit state transition table.
- Deterministic classification.
- Deterministic evidence-needed decision.
- Deterministic escalation for unsupported cases.
- State transition audit.

### Done when

- A case reaches terminal state without model calls.
- Unsupported case escalates.
- State transitions are replayable.
- Baseline metrics are captured.

## 12. Stage 5 - Approval package and exact-action control

### Objective

Build approval before write tools execute.

### Implement

- Action proposal schema.
- Approval package builder.
- Approval route.
- Approval expiry.
- Arguments hash.
- Approval invalidation on argument changes.
- Approval audit.

### Done when

- Proposal displays exact tool, target, arguments, risk, evidence, idempotency key, verification, and compensation.
- Mutated arguments invalidate approval.
- Expired approval cannot execute.
- Rejected approval terminates or revises workflow.

## 13. Stage 6 - Provider gateway and structured output

### Objective

Add controlled model access behind local interfaces.

### Implement

- Provider-neutral interface.
- Fake provider.
- Primary provider adapter.
- Alternate provider adapter or substitute.
- Open-model route or stub.
- Prompt registry.
- Output schema registry.
- Structured output validation.
- Streaming where useful.
- Provider error taxonomy.
- Retry, circuit breaker, fallback.
- Cost and token tracking.

### Done when

- Fake provider tests pass.
- Invalid JSON or schema output is blocked.
- Provider timeout and fallback are tested.
- Cost event is recorded.
- Prompt and model versions appear in trace.

## 14. Stage 7 - Retrieval ingestion and evidence packets

### Objective

Build permission-aware retrieval.

### Implement

- Source registry.
- Document ingestion.
- Chunking.
- Lexical retrieval.
- Dense retrieval.
- Hybrid retrieval.
- Reranking.
- Metadata filters.
- Access filters.
- Citation validation.
- Evidence packet contract.
- Abstention taxonomy.

### Done when

- Permitted source appears in evidence.
- Unauthorized source is excluded before model context.
- Citation resolves to source version.
- Retrieval benchmark report is generated.
- Freshness failures trigger abstention or escalation.

## 15. Stage 8 - Governed memory

### Objective

Implement memory as policy-controlled records, not transcript storage.

### Implement

- Memory category schema.
- Memory write policy.
- Consent or allowed-basis field.
- Purpose limitation.
- Provenance.
- Expiration.
- Correction.
- Deletion.
- Derived summary invalidation.
- Memory read policy.
- Memory evaluation fixtures.

### Done when

- Missing consent or policy basis blocks write.
- Poisoned tool output cannot become durable memory silently.
- Cross-tenant memory read fails.
- Expired memory is ignored.
- Deletion invalidates derived summaries and indexes.
- Deletion/expiry report is generated.

## 16. Stage 9 - Agent runtime state graph

### Objective

Add bounded model-assisted planning and recovery.

### Implement

- State graph executor.
- Planner.
- Plan validator.
- Verifier.
- Recovery path.
- Escalation path.
- Budget enforcement.
- Loop termination tests.
- Pattern comparison harness.
- Optional framework adapter behind local interface.

### Done when

- Bounded workflow completes happy path.
- Budget stops runaway case.
- Insufficient evidence escalates.
- Invalid plan is rejected.
- Pattern comparison report is generated.

## 17. Stage 10 - Read tools and write tools

### Objective

Add tools with schema validation, authorization, idempotency, verification, and compensation.

### Implement

- Tool registry.
- `policy.search`.
- `ticket.lookup`.
- `asset.lookup` or `customer.lookup`.
- `ticket.update_status` write tool.
- `notification.draft`.
- `notification.send` simulated write tool.
- Argument validation.
- Result-size limits.
- Timeouts and retries.
- Idempotency keys.
- Verification.
- Compensation.

### Done when

- Read tools work without write permissions.
- Write tool cannot execute without approval.
- Duplicate write is blocked.
- Verification success and failure paths are tested.
- Compensation event is audited.

## 18. Stage 11 - MCP secured capability

### Objective

Expose or consume one capability through MCP without weakening controls.

### Implement

- MCP server or client.
- Server allowlist.
- Capability registration.
- Version pinning.
- Identity propagation.
- Tenant authorization.
- Schema validation.
- Result-size limits.
- Cancellation.
- Audit.
- Malicious tool description fixture.
- Malicious tool result fixture.

### Done when

- Approved MCP capability runs.
- Unapproved server is rejected.
- Version mismatch is rejected.
- Malicious description does not change permissions.
- Oversized result is blocked.
- MCP security report is generated.

## 19. Stage 12 - A2A specialist handoff

### Objective

Implement one controlled handoff to a specialist agent or service.

### Implement

- Specialist service.
- Handoff contract.
- Authentication.
- Identity context.
- Tenant context.
- Policy context.
- Purpose and expiration.
- Response schema validation.
- Resume or escalate behavior.
- Unauthorized handoff tests.

### Done when

- Authorized read-only handoff succeeds.
- Unauthorized action scope is denied.
- Expired handoff is rejected.
- Source workflow resumes with validated result.
- A2A report is generated.

## 20. Stage 13 - Bilingual evaluation, safety, and red team

### Objective

Evaluate the agent as a product and a control system.

### Implement

- English golden cases.
- Arabic golden cases.
- Difficult and boundary cases.
- Tool-failure cases.
- Permission-violation cases.
- Memory cases.
- MCP malicious cases.
- A2A malicious cases.
- Prompt-injection cases.
- PII and secret leakage cases.
- Refusal and over-refusal metrics.
- Judge calibration.
- Evaluation reports.

### Done when

- English and Arabic results are separate.
- Unauthorized writes are zero on critical suite.
- Judge calibration report is generated.
- Red-team report is generated.
- Blocked release demonstration exists.

## 21. Stage 14 - Multimodal input slice

### Objective

Support one non-text input without losing provenance or review controls.

### Implement

- Attachment ingest.
- OCR or transcript path.
- Structured extraction.
- Evidence provenance.
- Confidence score.
- Low-confidence human review.
- Privacy and retention policy.
- Multimodal eval slice.

### Done when

- Attachment can be processed.
- Extracted evidence carries modality provenance.
- Low confidence routes to human.
- Tool use from extracted data requires validation.
- Multimodal slice appears in eval report.

## 22. Stage 15 - Safe replay and redaction

### Objective

Make runs auditable without storing hidden reasoning or sensitive content.

### Implement

- Replay event schema.
- Redaction policy.
- State snapshot writer.
- Tool input/output redaction.
- Evidence reference redaction.
- Replay authorization.
- Replay export.
- Incident timeline view.
- Sensitive telemetry tests.

### Done when

- Replay shows state transitions and decisions.
- Replay does not include hidden chain-of-thought.
- Sensitive content is redacted.
- Unauthorized replay access is denied.
- Safe replay report is generated.

## 23. Stage 16 - Observability, cost, and budgets

### Objective

Make the platform operable and cost-controlled.

### Implement

- OpenTelemetry spans.
- Structured logs.
- Prometheus metrics.
- Dashboards.
- Cost events.
- Token budgets.
- Step budgets.
- Time budgets.
- Spend budgets.
- Cache events.
- Alerts and runbooks.

### Done when

- One run is traceable end to end.
- Cost per successful task is reported.
- Budget stop is tested.
- Dashboards show agent success, errors, latency, cost, retrieval, memory, tools, MCP, A2A, approvals, and providers.
- Sensitive telemetry tests pass.

## 24. Stage 17 - Release gates, canary, rollback, and failover

### Objective

Deploy changes safely and recover.

### Implement

- Release candidate table.
- Release tuple.
- Evaluation gate runner.
- Feature flags.
- Canary mode.
- Provider failover.
- Rollback for prompt, model route, retrieval index, memory policy, tool capability, MCP version, A2A policy, runtime, and deployment image.
- Smoke tests.
- Restore drill.
- Report generator.

### Done when

- Candidate cannot release with failed gates.
- Canary regression rolls back.
- Provider failover works.
- Tool disable works.
- Restore drill is documented.
- Canary, rollback, and failover report is generated.

## 25. Stage 18 - Deployment and infrastructure

### Objective

Package and deploy the platform.

### Implement

- Non-root container images.
- Docker Compose local deployment.
- Kubernetes manifests.
- Resource requests and limits.
- Health and readiness checks.
- Secrets handling.
- Workload identity where supported.
- Terraform staging environment.
- Backup and restore docs.
- Load and failure-injection tests.

### Done when

- Local deploy works from fresh clone.
- Kubernetes manifests are valid.
- Secrets are not in images or code.
- Failure-injection report is generated.
- Another engineer can operate and disable the platform from runbooks.

## 26. Documentation governance and stage records

### Stage record format

Each stage should create or update:

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

Use:

- `AO-01-repo`
- `AO-02-contracts`
- `AO-03-auth-audit`
- `AO-04-deterministic-workflow`
- `AO-05-approval`
- `AO-06-provider-gateway`
- `AO-07-retrieval`
- `AO-08-memory`
- `AO-09-agent-runtime`
- `AO-10-tools`
- `AO-11-mcp`
- `AO-12-a2a`
- `AO-13-bilingual-redteam`
- `AO-14-multimodal`
- `AO-15-safe-replay`
- `AO-16-observability-cost`
- `AO-17-release-failover`
- `AO-18-deployment`

### Documentation checks

Before final review:

- Every stage has a record.
- Every contract has tests.
- Every consequential action has approval proof.
- Every release has a tuple.
- Every safety claim maps to evidence.
- Every English metric has an Arabic counterpart or documented reason.
- Every replay export is redaction-checked.

## 27. Minimal and full build paths

### Smallest complete portfolio build

The smallest complete build may use:

- Fake provider plus one real or stub provider.
- FAISS and local lexical retrieval.
- Simulated ticket and asset systems.
- Local MCP server.
- Local A2A specialist service.
- Simulated notification send.
- Docker Compose.
- Static bilingual datasets.

It must still include:

- Exact-action approval.
- Governed memory.
- Permission-aware retrieval.
- MCP allowlist.
- A2A identity and policy propagation.
- Red-team tests.
- Safe replay.
- Bilingual evaluation.
- Rollback and failover simulation.

### Full production-style path

The full path adds:

- Primary hosted provider.
- Alternate hosted provider.
- Open-model route.
- Production retrieval backend.
- Kubernetes.
- Terraform.
- Workload identity.
- Real dashboards.
- Failure drills.
- Canary and rollback.
- Optional ASP.NET Core vertical slice.

## 28. Requirement traceability matrix

### Production requirement crosswalk

| Requirement | Evidence |
|---|---|
| Governed enterprise agent | State graph, case workflow, capability card |
| Provider portability | Provider adapters, decision matrix, failover report |
| Permission-aware RAG | Retrieval benchmark, access tests, citation checks |
| Governed memory | Memory policy, memory quality report, deletion report |
| Exact-action approval | Approval package tests and audit records |
| Secure tools | Tool contract report and unauthorized action report |
| MCP | MCP security report |
| A2A | A2A handoff report |
| Bilingual operation | Bilingual eval and Arabic RTL report |
| Safe replay | Safe replay report and redaction tests |
| Residency profile | Residency control record |
| Production rollout | Canary, rollback, failover, restore reports |

### Curriculum crosswalk

| Curriculum area | Implementation evidence |
|---|---|
| Lessons 01-06 engineering foundation | Typed services, tests, CI, deployment |
| Lessons 08-11 model APIs | Provider gateway, streaming, structured output, cost |
| Lessons 12-15 retrieval and evaluation | RAG, citations, eval gates |
| Lessons 16-18 tools, agents, MCP | State graph, approval, tools, memory, MCP, A2A |
| Lessons 28-29 safety and governance | Threat model, red-team, DLP, policy controls |
| Lessons 30-36 production and MLOps | Observability, cloud, K8s, failover, rollback |
| Lesson 40 capstone | End-to-end business workflow and outcome report |
| Lessons 45-46 evaluation and security | Judge calibration, red-team, release gates |
| Lesson 51 domain/localization | UAE/Arabic control record and bilingual UX |
| Lessons 54, 56-57 interviews | Architecture, system design, portfolio defense |

### Requirement-to-evidence manifest

Create `reports/final-evidence-manifest.json`:

```json
{
  "project": "AegisOps",
  "requirements": [
    {
      "id": "exact-action-approval",
      "status": "met",
      "evidence": [
        "reports/security/unauthorized-action-report.md",
        "reports/tools/tool-contract-report.md"
      ]
    },
    {
      "id": "bilingual-evaluation",
      "status": "met",
      "evidence": [
        "reports/evals/bilingual-eval-report.md",
        "reports/localization/arabic-rtl-report.md"
      ]
    }
  ]
}
```

## 29. Test strategy

### Unit tests

Cover:

- State transitions.
- Budget enforcement.
- Structured-output validation.
- Policy decisions.
- Approval hash binding.
- Tool schema validation.
- Idempotency keys.
- Memory write policy.
- Memory deletion invalidation.
- Citation validation.
- Redaction.
- Provider error classification.
- Gate comparators.

### Integration tests

Cover:

- Case intake to deterministic terminal state.
- Case intake to retrieval to evidence packet.
- Action proposal to approval to tool execution.
- Tool failure to compensation.
- Memory write to correction to deletion.
- MCP call with identity propagation.
- A2A handoff with policy context.
- Safe replay export.
- Release candidate to failed gate.
- Canary regression to rollback.

### Security tests

Cover:

- Cross-tenant retrieval denial.
- Cross-tenant memory denial.
- Unauthorized approval denial.
- Approval argument mutation denial.
- Prompt injection in retrieved document.
- Malicious MCP description.
- Malicious MCP result.
- SQL injection in tool input.
- Excessive result fetch.
- PII exfiltration.
- Hidden reasoning leakage in replay.

### Evaluation tests

Cover:

- English happy path.
- Arabic happy path.
- Tool failure.
- Provider failure.
- Permission violation.
- Memory stale case.
- Escalation case.
- Multimodal low-confidence case.
- Refusal and over-refusal.
- Judge calibration.

### Deployment tests

Cover:

- Docker Compose config.
- Health and readiness.
- Migration from empty DB.
- Kubernetes manifest validation.
- Provider failover.
- Tool disable.
- Rollback.
- Restore.

## 30. Data and evaluation plan

### Golden datasets

Create:

- English happy cases.
- Arabic happy cases.
- English difficult cases.
- Arabic difficult cases.
- Tool failure cases.
- Permission violation cases.
- Retrieval insufficiency cases.
- Memory correction/deletion cases.
- MCP malicious cases.
- A2A authorization cases.
- Prompt-injection cases.
- Multimodal cases.

### Annotation guidance

Each case needs:

- Expected route.
- Expected evidence.
- Expected citation IDs.
- Expected tool selection.
- Expected action risk.
- Whether approval is required.
- Expected arguments.
- Expected escalation behavior.
- Safety notes.
- Language and locale notes.

### Feedback loop

Operator feedback flow:

1. Feedback is linked to case, run, language, tenant, prompt, model, tool, and policy versions.
2. Sensitive content is redacted.
3. Reviewer accepts or rejects feedback as training/eval candidate.
4. Accepted feedback creates a new dataset version.
5. Regression suite runs.
6. Release candidate is approved or rejected.

## 31. Operational runbooks

### Provider outage

1. Confirm provider error and latency.
2. Check circuit breaker.
3. Route to alternate provider.
4. Run smoke eval.
5. Watch cost and quality.
6. Write incident note.

### Unauthorized action attempt

1. Confirm policy denial.
2. Confirm no tool execution event exists.
3. Inspect prompt, retrieval, tool, and MCP inputs.
4. Add red-team fixture if new.
5. Keep release blocked until regression passes.

### Memory deletion request

1. Validate requester authority.
2. Mark memory item deletion pending.
3. Invalidate derived summaries, indexes, and caches.
4. Run verified forgetting check.
5. Generate deletion report.

### MCP failure

1. Disable affected capability if needed.
2. Confirm server trust and version.
3. Check schema and result-size errors.
4. Route to fallback or escalate.
5. Add fixture if malicious payload is new.

### A2A authorization failure

1. Confirm source and target identity.
2. Check policy context.
3. Deny handoff result mutation.
4. Resume workflow in escalation state.
5. Record handoff report.

### Canary regression

1. Freeze promotion.
2. Stop candidate traffic.
3. Roll back affected prompt, model route, memory policy, tool capability, MCP version, or deployment image.
4. Run smoke eval.
5. Verify telemetry and cost events.
6. Generate rollback report.

## 32. Optional .NET vertical slice

Implement only when the .NET lane is selected.

### Scope

The .NET slice should include one coherent business path:

- ASP.NET Core API.
- Provider-neutral model access where supported.
- Streaming cancellation.
- Structured-output validation.
- Permission-aware retrieval.
- Controlled tool/MCP boundary.
- Exact-action approval.
- OpenTelemetry trace.
- Workload identity where supported.
- Contract and evaluation parity with Python path.

### Evidence

- OpenAPI contract.
- Provider adapter tests.
- Streaming cancellation test.
- Structured-output validation failure test.
- Retrieval authorization test.
- MCP/tool approval test.
- Trace screenshot or export.
- Deployment and rollback runbook.
- Contract/evaluation parity report.

## 33. Final reviewer proof

The reviewer should be able to run or inspect equivalent commands:

```powershell
python -m pytest
python -m mypy packages apps
docker compose config
docker compose up
```

Then verify:

- Case creation.
- Deterministic workflow.
- Provider gateway with fake provider.
- Retrieval with permitted citations.
- Memory write, correction, expiry, and deletion.
- Action proposal.
- Approval.
- Approved tool execution.
- Duplicate-write block.
- MCP capability.
- A2A handoff.
- English eval.
- Arabic eval.
- Red-team eval.
- Safe replay export.
- Provider failover.
- Canary rollback.

Final evidence files:

- `reports/evals/agent-eval-report.md`
- `reports/evals/bilingual-eval-report.md`
- `reports/security/red-team-report.md`
- `reports/security/unauthorized-action-report.md`
- `reports/memory/deletion-expiry-report.md`
- `reports/mcp/mcp-security-report.md`
- `reports/a2a/a2a-handoff-report.md`
- `reports/replay/safe-replay-report.md`
- `reports/residency/residency-control-record.md`
- `reports/release/canary-rollback-failover-report.md`
- `reports/business/business-outcome-report.md`
- `reports/final-evidence-manifest.json`

## 34. First practical assignment

Build the first safe slice:

1. Create case API.
2. Add users, tenants, roles, and audit.
3. Implement deterministic workflow states.
4. Add fake provider with structured output.
5. Add one read-only policy search fixture.
6. Add one proposed ticket update.
7. Require approval before execution.
8. Execute only after approval.
9. Verify the ticket update.
10. Export redacted replay.

This proves the core control loop before MCP, A2A, multilingual evaluation, or deployment.

## 35. Final definition of done and interview defense

The technical build is complete when:

- Fresh clone can start the local stack.
- Case intake and deterministic workflow work.
- Identity, tenant authorization, and audit are enforced.
- Provider gateway supports fake, primary, alternate, and open-model or stub routes.
- Structured output is validated before business logic.
- Retrieval is permission-aware and citation-validated.
- Governed memory supports policy-controlled writes, correction, expiry, deletion, and verified forgetting.
- Agent runtime is a bounded state graph with budget enforcement and escalation.
- Read and write tools are schema-validated, authorized, idempotent, verified, and auditable.
- Exact-action approval blocks all consequential writes until approved.
- Secured MCP capability and A2A handoff preserve identity and policy context.
- English and Arabic evals, red-team tests, memory tests, tool tests, MCP tests, A2A tests, and safe replay tests run.
- Multimodal slice preserves evidence provenance and routes low-confidence cases to human review.
- Observability, cost, safe replay, canary, rollback, failover, restore, and handoff evidence exist.
- Final evidence manifest maps claims to reports.

For interview defense, be ready to explain:

- Why authorization is outside the model.
- Why the state graph is explicit.
- How exact-action approval works.
- How idempotency and compensation prevent duplicate or partial writes.
- How governed memory differs from transcript storage.
- How MCP and A2A boundaries preserve trust.
- How Arabic quality and safety were measured.
- How safe replay works without hidden reasoning.
- How you roll back a bad prompt, tool, memory policy, or provider route.
