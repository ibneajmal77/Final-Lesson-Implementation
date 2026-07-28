# AegisOps Governed Agent Platform Production Implementation Guide

Project codename: `AegisOps`

Build and operate a multilingual, multi-provider enterprise agent platform that handles operations cases in English and Arabic, retrieves permitted evidence, maintains governed memory, plans bounded workflows, uses MCP and A2A-connected tools, obtains exact human approval for consequential actions, and produces replayable audit evidence without storing hidden reasoning.

This is the capstone-grade governed-agent project. It is not a chat demo, not an unconstrained autonomous agent, and not a pile of framework integrations. The proof is that the platform can perform useful operational work while preserving authorization, privacy, residency, auditability, evaluation discipline, rollback, and human control.

## Source alignment

This guide is aligned to the local curriculum and roadmap documents:

- `deep-research-report.md`: standalone `AegisOps` project, required capability threads, implementation sequence, acceptance gates, and project package.
- `AI-Industry-Roadmap-and-Projects.md`: capstone `Atlas`, tools/agents/MCP phase, .NET lane evidence, IncidentPilot safety language, production rollout, and portfolio proof expectations.
- `AI-Industry-Curriculum.md`: controlled agents, governed memory, MCP, model gateways, security, observability, capstone, role branches, and .NET vertical slice.
- `AI-Industry-Complete-Lesson-Coverage-Map.md`: lessons 01-18, 28-36, 40, 42, 45-46, 51, 54, and 56-57 coverage.
- `AI-Industry-Detailed-Lessons.md`: explicit workflow state, memory lifecycle, MCP boundaries, human approval, idempotency, compensation, and agent evaluation requirements.

`AegisOps` is a new standalone proving ground. It can reuse concepts from SupportOps, Enterprise RAG, VoiceTriage, DomainTune, ModelMesh, and IncidentPilot, but it must produce its own coherent platform evidence.

## Evidence and verification vocabulary

Use these terms consistently:

- `case`: A user-submitted operations request that may require retrieval, reasoning, tools, approval, or escalation.
- `workflow run`: One bounded execution of the agent state graph for a case.
- `state transition`: A recorded movement between intake, retrieve, plan, propose, approve, act, verify, recover, escalate, and terminate states.
- `agent runtime`: Application-owned orchestration layer that controls model calls, tools, memory, budgets, and termination.
- `model provider`: Hosted or self-hosted model backend accessed through a provider-neutral interface.
- `framework adapter`: Optional runtime integration such as LangGraph or a provider-native agents SDK behind application-owned interfaces.
- `capability`: A versioned operation the platform may invoke, with owner, permissions, schemas, resource limits, and compatibility tests.
- `MCP tool`: A capability exposed through a secured MCP boundary.
- `A2A handoff`: An authenticated transfer to another specialist agent or service with identity and policy context.
- `consequential action`: A write, notification, configuration change, or external side effect requiring exact human approval.
- `approval package`: The exact tool, target, arguments, risk, evidence, expected effect, idempotency key, and rollback or compensation plan shown to the approver.
- `governed memory`: Policy-controlled memory with subject, tenant, purpose, consent, provenance, classification, version, expiry, correction, deletion, and evaluation.
- `request context`: Transient inputs for the current request.
- `session state`: Short-lived state for an active user session.
- `durable workflow state`: Checkpoints needed to resume or audit a workflow.
- `user-preference memory`: Durable preferences allowed by policy and consent.
- `retrieval-backed memory`: Durable references to approved evidence or facts derived from approved sources.
- `summarized memory`: Derived memory that must inherit provenance, retention, correction, and deletion behavior.
- `safe replay`: Authorized replay of redacted state transitions, inputs, outputs, policy decisions, tool calls, and summaries. It must not expose hidden chain-of-thought.

## 1. Production outcome

The final system is a governed enterprise operations agent platform where an authorized operator can:

1. Submit English or Arabic operations cases.
2. Classify and route cases by risk, urgency, language, tenant, and required capabilities.
3. Retrieve permitted evidence from policies, runbooks, tickets, assets, and prior approved memory.
4. Generate structured outputs with citations and abstention when evidence is insufficient.
5. Maintain governed memory under explicit consent, purpose, provenance, retention, correction, and deletion rules.
6. Plan bounded workflows using an explicit state graph.
7. Propose read-only and write actions with validated arguments.
8. Require exact human approval before consequential writes.
9. Execute approved tools through application authorization, MCP boundaries, or A2A handoff.
10. Verify effects, compensate or recover after partial failure, and escalate when needed.
11. Trace provider, retrieval, memory, policy, tool, MCP, A2A, cost, and approval decisions end to end.
12. Replay an authorized redacted run for audit and incident investigation.
13. Evaluate English and Arabic quality, safety, tool behavior, memory behavior, latency, and cost separately.
14. Deploy with provider failover, canary rollout, rollback, runbooks, and handoff evidence.

The platform is production-ready when a reviewer can run a full case from intake through evidence retrieval, proposal, approval, execution, verification, safe replay, evaluation, and rollback using documented commands and dashboards.

## 2. Business problem, users, scope, and non-goals

### Business problem

Enterprise operations teams handle cases that span policies, systems, customer or asset records, human judgment, and controlled actions. A model can summarize or draft text, but production automation requires much more:

- Authorization must live outside model instructions.
- Untrusted documents, tool results, and MCP descriptions must not control the system.
- Memory must not become an unbounded transcript or cross-tenant data leak.
- Actions need validated arguments, approval, idempotency, verification, compensation, and audit.
- Provider choice must consider quality, latency, cost, regional availability, data handling, and failover.
- English and Arabic behavior must be evaluated separately.
- Safe replay must help reviewers reconstruct what happened without exposing hidden reasoning or sensitive content.

`AegisOps` solves this by making the agent an application-owned workflow system with bounded model usage, explicit policy enforcement, governed memory, secured tool boundaries, and measured release gates.

### Primary users

- Operations analysts who submit and monitor cases.
- Human approvers who authorize exact consequential actions.
- Security reviewers who inspect policy, tool, memory, and audit controls.
- Data owners who approve retrieval and memory sources.
- Platform operators who watch health, latency, cost, and failure modes.
- Compliance reviewers who need evidence bundles and residency records.
- Developers who add capabilities, MCP tools, A2A handoffs, prompts, and policies.
- End users who may receive approved notifications or case updates.

### Initial domain

Use a synthetic but realistic enterprise operations domain, such as:

- Customer support operations.
- IT operations.
- Cloud cost operations.
- Field service operations.
- Compliance operations.

The recommended scenario:

- A UAE-based enterprise operations team receives English and Arabic cases.
- Each case may require policy retrieval, asset lookup, ticket lookup, evidence synthesis, and a low-risk controlled write.
- The platform can update a ticket, send a notification, or change a low-risk configuration only after exact human approval.

### Required scope

The first production-style release must include:

- Tenant and user identity.
- Role-based access control.
- Case intake API and operator UI contract.
- Explicit workflow state graph.
- Provider-neutral model gateway with at least two providers and one open-model route or stub.
- Structured output validation.
- Streaming where useful.
- Prompt and output-contract versioning.
- Hybrid RAG with citations, metadata filters, freshness, and abstention.
- Governed memory with separate request, session, workflow, preference, retrieval-backed, and summary memory categories.
- Memory consent, purpose, provenance, expiration, correction, and deletion.
- Read tools and at least one approval-gated write tool.
- Idempotency, retries, timeouts, compensation, and verification.
- Secured MCP server or client integration.
- One A2A-style handoff with identity and policy context propagation.
- Capability allowlist and versioning.
- Human approval for consequential writes.
- Prompt-injection, malicious tool-output, data-exfiltration, cross-tenant, oversized-result, and SQL-injection tests.
- Bilingual English/Arabic evaluation and red-team pack.
- At least one multimodal input path, such as document attachment, scanned policy image, form, or voice-note transcript.
- OpenTelemetry traces and safe replay.
- Cost, token, step, time, and spend budgets.
- Provider failover, canary, rollback, restore, and failure-injection evidence.
- Data residency and retention control record.
- Agent capability card.
- Business-outcome report.
- Optional .NET vertical slice with contract and evaluation parity when the .NET lane is selected.

### Explicit non-goals for the first release

Do not attempt:

- Unsupervised high-impact writes.
- General-purpose autonomous web browsing.
- Arbitrary tool discovery from untrusted servers.
- Fully autonomous production remediation.
- Storing hidden chain-of-thought.
- Global multi-cloud production deployment.
- Every agent framework or provider.
- Feature parity between Python and .NET implementations.
- Real UAE legal compliance certification.
- Real production customer data.
- Real destructive infrastructure changes.

## 3. Business outcomes and metric tree

### Primary outcome

The platform reduces operations handling time and improves decision consistency while preserving privacy, authorization, auditability, human control, bilingual quality, and recoverability.

### Business metrics

- Case handling time.
- Time to evidence packet.
- Time to approved action.
- Task-completion rate.
- Human rework rate.
- Escalation rate.
- Approval turnaround time.
- Cost per successful case.
- Operator satisfaction.
- Safe automation rate for low-risk actions.
- Incident investigation time.

### Agent quality metrics

- Task completion.
- Correct route selection.
- Evidence sufficiency.
- Citation accuracy.
- Structured-output validity.
- Tool selection accuracy.
- Tool argument correctness.
- Verification success.
- Recovery success.
- Escalation appropriateness.
- Invalid-action rate.
- Step count.
- Over-budget stop rate.

### Retrieval and memory metrics

- Retrieval recall at K.
- Retrieval precision at K.
- MRR or NDCG.
- Citation resolution rate.
- Unauthorized evidence leakage.
- Abstention quality.
- Memory write precision.
- Memory usefulness.
- Stale-memory rate.
- Harmful-memory rate.
- Cross-tenant memory leakage.
- Correction propagation time.
- Verified forgetting success.

### Safety and governance metrics

- Unauthorized write attempts blocked.
- Approval bypass attempts blocked.
- Prompt-injection success rate.
- Malicious tool-output success rate.
- SQL-injection and excessive-fetch success rate.
- PII and secret leakage rate.
- Refusal quality.
- Over-refusal rate.
- Policy violation rate.
- Audit completeness.
- Manual override count and reasons.

### Bilingual and localization metrics

- English task-completion rate.
- Arabic task-completion rate.
- English citation accuracy.
- Arabic citation accuracy.
- English safety pass rate.
- Arabic safety pass rate.
- Arabic refusal and over-refusal rate.
- Translation drift rate if translation is used.
- RTL UI issue count.
- Locale-specific escalation rate.

### Operational metrics

- p50, p95, and p99 case latency.
- Model latency.
- Retrieval latency.
- Tool latency.
- MCP latency.
- A2A handoff latency.
- Provider error rate.
- Provider fallback rate.
- Cost per model call.
- Cost per successful case.
- Cache hit rate.
- Budget stop rate.
- Workflow recovery rate.
- Rollback duration.

## 4. What production-ready means

`AegisOps` is production-ready only if:

- The workflow is an explicit bounded state graph, not an unconstrained autonomous loop.
- The platform can run without a model for deterministic non-AI fallback paths.
- Model output never directly authorizes tool execution.
- Every consequential action requires exact human approval of tool, target, arguments, risk, and verification plan.
- Every tool call is authorized by application policy before execution.
- Every write has idempotency, audit, verification, and compensation or rollback behavior.
- The model cannot silently write durable memory.
- Memory categories, purposes, consent, retention, correction, deletion, and derived-summary invalidation are implemented.
- Retrieval applies authorization filters before evidence enters model context.
- Citations resolve to permitted evidence.
- MCP and A2A boundaries preserve identity and policy context.
- Provider routing and fallback are explicit and measured.
- English and Arabic evaluation results are separate.
- Safe replay exposes redacted state and decisions, not hidden reasoning.
- Failure drills prove provider outage, tool failure, MCP failure, A2A authorization failure, canary regression, rollback, and restore.

## 5. Non-negotiable requirements

1. Authorization outside the model: no prompt instruction can grant permission.
2. Exact-action approval: every consequential write needs approval of exact action and arguments.
3. Deterministic baseline: a non-agentic baseline must exist before adding agent planning.
4. Bounded runtime: step, time, token, context, tool, and spend limits are enforced.
5. Structured contracts: cases, plans, tool calls, approvals, memory writes, handoffs, and replay events are schema-validated.
6. Governed memory: no durable memory write without policy, consent or allowed basis, purpose, provenance, retention, and deletion handling.
7. Permission-aware retrieval: unauthorized evidence never reaches model context.
8. Secured MCP: only approved servers, capabilities, schemas, versions, and identities are accepted.
9. Controlled A2A: handoffs carry identity, tenant, policy, purpose, and allowed action scope.
10. Safe replay: no hidden chain-of-thought, no unredacted sensitive data, and no replay access without authorization.
11. Bilingual proof: English and Arabic evals, red-team cases, and locale failures are reported separately.
12. Release gates: quality, safety, tool, memory, retrieval, bilingual, latency, cost, and security gates block release.
13. Rollback and failover: provider, prompt, policy, tool capability, memory policy, and deployment rollback are documented and tested.

## 6. Core journeys and required UX

### Case intake and triage journey

The operator should be able to:

1. Submit a case in English or Arabic.
2. Attach a document, image, form, or voice-note transcript for the selected multimodal slice.
3. See detected language, tenant, risk level, requested outcome, and required capabilities.
4. See whether the case can proceed, needs more information, or must escalate.
5. See deterministic baseline output before agentic behavior is enabled.

Required UX:

- Case list.
- Case detail.
- Language and risk badge.
- Evidence and action status.
- Budget and step counter.
- Escalation reason.

### Evidence and RAG journey

The analyst should be able to:

1. See retrieved policy, runbook, ticket, asset, and memory evidence.
2. See citations with source, version, access decision, freshness, and confidence.
3. See abstention when evidence is insufficient.
4. See why a document was not used when access or freshness blocks it.
5. Export a scoped evidence bundle.

Required UX:

- Evidence table.
- Citation verifier.
- Access decision log.
- Freshness indicator.
- Retrieval debug trace.

### Plan, approve, act, and verify journey

The approver should be able to:

1. Review the proposed plan.
2. Review exact tool, target, arguments, risk, evidence, expected result, idempotency key, and verification method.
3. Approve, reject, request changes, or escalate.
4. See the execution result.
5. See verification and compensation status.

Required UX:

- Approval package.
- Diff or proposed change view where relevant.
- Approve and reject controls.
- Execution timeline.
- Verification checklist.
- Compensation or rollback status.

### Governed memory journey

The data owner or operator should be able to:

1. Inspect memory items by subject, tenant, purpose, source, classification, consent, and expiry.
2. See which workflow wrote each item.
3. Correct a memory item.
4. Delete or expire a memory item.
5. Verify derived summaries, indexes, and caches were invalidated.

Required UX:

- Memory inventory.
- Memory write-policy decision view.
- Correction and deletion controls.
- Verified forgetting report.

### MCP and A2A journey

The platform engineer should be able to:

1. Register a capability.
2. Map it to an MCP tool, resource, or prompt.
3. Approve capability version, owner, schema, permissions, and limits.
4. Execute through an allowlisted client.
5. Send one A2A handoff to a specialist service with identity and policy context.
6. Inspect audit logs and failure behavior.

Required UX:

- Capability registry.
- MCP allowlist.
- A2A handoff trace.
- Version compatibility status.
- Tool trust and policy decision log.

### Safe replay and incident journey

The auditor should be able to:

1. Open a completed workflow run.
2. Replay redacted state transitions.
3. Inspect model, retrieval, memory, policy, tool, MCP, A2A, approval, and cost events.
4. Reconstruct a failure timeline.
5. Export a scoped audit package.

Required UX:

- Replay timeline.
- Redacted state snapshot.
- Trace and log correlation.
- Cost and latency waterfall.
- Export controls.

### Arabic and RTL journey

The operator should be able to:

1. Submit Arabic cases.
2. Retrieve Arabic or English evidence as allowed.
3. See Arabic output with right-to-left presentation where relevant.
4. Escalate language uncertainty.
5. Compare Arabic and English quality reports.

Required UX:

- Locale indicator.
- RTL-friendly case and evidence view.
- Translation provenance if translation is used.
- Arabic eval and safety dashboard.

## 7. Governance, authorization, and exact-action control

### Governance invariants

- Model output is advisory until validated by application policy.
- Tool authorization checks run with user, tenant, purpose, action, target, and argument context.
- Read tools and write tools have separate permissions.
- Every write has a unique idempotency key.
- Approval is bound to exact tool, target, and arguments.
- Changing arguments after approval invalidates approval.
- Approval expires after a configured time.
- Approval cannot be reused for a different workflow run.
- Tool results are untrusted inputs.
- Memory writes require explicit policy evaluation.
- MCP tool descriptions and results are untrusted.
- A2A handoff recipients receive only the allowed context.
- Policy changes are versioned and audited.

### Action risk levels

Use a risk taxonomy:

- `read_only`: no side effects.
- `draft_only`: creates a draft, no external side effect.
- `low_risk_write`: updates low-risk internal state after approval.
- `external_notification`: sends user-facing or external message after approval.
- `configuration_change`: changes operational configuration after approval and verification.
- `high_impact`: out of scope for autonomous execution; human-run only.
- `prohibited`: never executable through the platform.

### Canonical approval sequence

1. Agent proposes action.
2. Application validates schema.
3. Policy service evaluates user, tenant, target, action, and arguments.
4. Risk service classifies action.
5. Approval package is built.
6. Human approver reviews exact package.
7. Approval is recorded with policy version and expiration.
8. Execution service revalidates policy and approval.
9. Tool executes with idempotency key.
10. Verification service confirms effect.
11. Compensation or escalation runs if verification fails.
12. Audit and replay records are finalized.

### Policy-change SLO

Policy changes must be effective quickly:

- User access change: within 5 minutes.
- Tool disable: within 1 minute.
- Provider disable: within 1 minute.
- Memory-write policy change: within 5 minutes for new writes.
- Retrieval access revocation: blocks new evidence retrieval within 5 minutes.
- Emergency deployment freeze: within 1 minute.

Document cache invalidation, policy refresh, and degraded behavior that make these SLOs true.

## 8. Reference architecture and project boundaries

### Recommended stack

Minimal local path:

- FastAPI for platform APIs.
- Pydantic for contracts.
- PostgreSQL for workflow, audit, memory metadata, approvals, and policy state.
- pgvector or FAISS for local vector retrieval.
- OpenSearch or Elasticsearch for hybrid retrieval where available.
- Redis for queues, locks, budget counters, and cache metadata.
- Object storage for documents, reports, replay exports, and artifacts.
- Provider-neutral model interface with fake provider for tests.
- One hosted provider adapter.
- One alternate provider adapter or deterministic substitute.
- One open-model route or stub compatible with the ModelMesh path.
- Explicit state graph implementation; optional LangGraph adapter after the manual graph works.
- MCP SDK for one secured capability.
- A2A handoff implemented as an authenticated service-to-service protocol or compatible SDK if available.
- OpenTelemetry, Prometheus, and Grafana or Application Insights/ELK.
- Docker Compose for local development.

Full production-style path:

- Azure OpenAI plus one alternate hosted provider.
- vLLM or TensorRT-LLM route for open model where available.
- Production retrieval backend plus FAISS baseline.
- Kubernetes deployment.
- Terraform infrastructure.
- Secretless workload identity where supported.
- Feature flags.
- Canary and rollback.
- Provider failover.
- Load and failure-injection tests.
- Optional `Atlas.DotNet` vertical slice using ASP.NET Core and provider-neutral chat abstraction when selected.

### Component responsibilities

Case API:

- Owns case intake, case state, operator views, and request validation.

Agent runtime:

- Owns state graph, model calls, planning, verification, recovery, escalation, budget enforcement, and termination.

Model gateway:

- Owns provider routing, structured output enforcement, streaming, retries, fallback, caching, cost, and provider metadata.

Retrieval service:

- Owns ingestion, indexing, hybrid retrieval, reranking, citations, metadata filters, freshness, and abstention evidence.

Memory service:

- Owns memory categories, write policy, consent, provenance, expiry, correction, deletion, derived-summary invalidation, and memory evaluation.

Policy service:

- Owns authorization, risk classification, capability allowlists, tool permissions, memory permissions, and approval requirements.

Tool service:

- Owns tool schemas, argument validation, read/write separation, idempotency, retries, timeouts, compensation, and verification.

MCP boundary:

- Owns secured server or client integration, capability allowlists, version pinning, identity propagation, and audit.

A2A boundary:

- Owns specialist handoff contract, identity and policy context propagation, response validation, and cross-agent authorization.

Approval service:

- Owns approval packages, approver roles, decisions, expirations, invalidation, and audit.

Replay service:

- Owns redacted state snapshots, replay permissions, export bundles, and incident reconstruction.

Evaluation service:

- Owns bilingual golden cases, adversarial cases, tool and memory metrics, judge calibration, regression gates, and release reports.

Observability service:

- Owns traces, metrics, logs, cost events, dashboards, redaction, alerts, and runbooks.

### Architecture decision requirement

The project must contain ADRs for:

- Modular monolith versus event-driven workers versus microservices.
- Manual explicit state graph versus one framework adapter.
- Provider-neutral interface versus provider-native SDK.
- Retrieval backend selection.
- Memory storage and deletion strategy.
- MCP server/client trust model.
- A2A handoff protocol.
- Safe replay storage and redaction.
- UAE data residency and provider routing.
- Python-only versus optional .NET vertical slice.

Do not choose multi-agent orchestration by default. Use one controlled workflow unless the A2A handoff has a measurable reason.

### Queue isolation

Use separate queues or workflow pools for:

- Case intake enrichment.
- Document ingestion.
- Retrieval indexing.
- Evaluation.
- Tool execution.
- Approval timeouts.
- Memory expiry and deletion.
- Replay export.
- Report generation.
- Provider failover checks.

Each queue needs idempotency, retries, dead-letter handling, timeouts, owner, and dashboard.

### Durable handoff and reconciliation

Use durable handoff for:

- Case accepted.
- Plan generated.
- Approval requested.
- Tool execution requested.
- Memory write requested.
- A2A handoff requested.
- Replay export requested.
- Evaluation requested.
- Deployment rollback requested.

Reconciliation must detect:

- Approval requested but not visible to approver.
- Approval expired but execution still pending.
- Tool executed but verification missing.
- Memory delete requested but derived summary still active.
- Retrieval source revoked but cached evidence still available.
- MCP capability disabled but client still advertises it.
- A2A handoff completed but source workflow not resumed.
- Provider disabled but routing still sends traffic.
- Canary failed but traffic still routes to candidate.

## 9. Documentation and evidence system

Required living documents:

- `docs/problem-statement.md`
- `docs/product-requirements.md`
- `docs/workflow-map.md`
- `docs/architecture.md`
- `docs/adr-architecture-boundaries.md`
- `docs/adr-agent-runtime.md`
- `docs/adr-provider-framework-portability.md`
- `docs/adr-retrieval-memory.md`
- `docs/adr-mcp-a2a.md`
- `docs/adr-residency.md`
- `docs/data-model.md`
- `docs/api-contracts.md`
- `docs/tool-contracts.md`
- `docs/mcp-contract.md`
- `docs/a2a-contract.md`
- `docs/memory-policy.md`
- `docs/approval-policy.md`
- `docs/security-threat-model.md`
- `docs/evaluation-plan.md`
- `docs/bilingual-evaluation-plan.md`
- `docs/observability-replay.md`
- `docs/deployment-runbook.md`
- `docs/rollback-runbook.md`
- `docs/platform-handoff.md`
- `docs/progress-log.md`

Required generated reports:

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

Required portfolio cards:

- Agent capability card.
- System card.
- Dataset card.
- Model/provider card.
- Tool capability card.
- Memory policy card.
- Operating limitations card.

## 10. Data, event, and API contracts

### Case contract

```json
{
  "case_id": "case_20260728_001",
  "tenant_id": "tenant_ops_uae",
  "submitted_by": "user_123",
  "language": "ar",
  "channel": "operator_console",
  "risk_hint": "low",
  "requested_outcome": "Update the ticket with the approved remediation plan.",
  "content": "Arabic or English case text goes here.",
  "attachments": [
    {
      "attachment_id": "att_001",
      "type": "pdf",
      "uri": "s3://aegisops/cases/case_20260728_001/att_001.pdf",
      "classification": "internal"
    }
  ]
}
```

### Workflow state contract

```json
{
  "workflow_run_id": "run_20260728_001",
  "case_id": "case_20260728_001",
  "state": "awaiting_approval",
  "step": 7,
  "budget": {
    "max_steps": 12,
    "max_tokens": 12000,
    "max_cost_usd": 1.25,
    "deadline_seconds": 180
  },
  "current_summary": "Redacted workflow summary for replay.",
  "next_allowed_states": ["approved_action", "rejected_action", "escalated"]
}
```

### Action proposal contract

```json
{
  "proposal_id": "proposal_001",
  "workflow_run_id": "run_20260728_001",
  "risk_level": "low_risk_write",
  "tool_name": "ticket.update_status",
  "target": {
    "ticket_id": "TCK-10021"
  },
  "arguments": {
    "status": "waiting_customer",
    "note": "Approved remediation plan summary."
  },
  "evidence_refs": ["ev_001", "ev_002"],
  "idempotency_key": "idem_run_20260728_001_ticket_update",
  "verification_method": "read_ticket_status_after_write",
  "compensation_plan": "append correction note and restore previous status if verification fails"
}
```

### Approval contract

```json
{
  "approval_id": "approval_001",
  "proposal_id": "proposal_001",
  "approver_id": "user_manager_01",
  "decision": "approved",
  "policy_version": "approval-policy-v8",
  "expires_at": "2026-07-28T11:00:00Z",
  "approved_tool": "ticket.update_status",
  "approved_arguments_hash": "sha256:...",
  "reason": "Evidence is sufficient and action is low risk."
}
```

### Memory item contract

```json
{
  "memory_id": "mem_001",
  "tenant_id": "tenant_ops_uae",
  "subject_id": "customer_123",
  "memory_type": "user_preference",
  "purpose": "case_resolution",
  "content_ref": "s3://aegisops/memory/mem_001.redacted.json",
  "source_refs": ["case_20260728_001", "ev_001"],
  "provenance": "human_approved_case_summary",
  "consent_state": "allowed_by_policy",
  "classification": "internal",
  "created_by_workflow_run_id": "run_20260728_001",
  "expires_at": "2026-10-28T00:00:00Z",
  "version": 1
}
```

### MCP capability contract

```json
{
  "capability_id": "policy_search.read.v1",
  "transport": "mcp",
  "owner": "knowledge-platform",
  "server_id": "mcp_policy_search_prod",
  "allowed_tenants": ["tenant_ops_uae"],
  "required_permissions": ["policy.read"],
  "input_schema_id": "policy-search-input-v1",
  "output_schema_id": "policy-search-output-v1",
  "max_result_bytes": 65536,
  "timeout_ms": 5000,
  "version": "1.0.0",
  "approval_required": false
}
```

### A2A handoff contract

```json
{
  "handoff_id": "a2a_001",
  "source_workflow_run_id": "run_20260728_001",
  "target_agent": "billing_specialist",
  "tenant_id": "tenant_ops_uae",
  "identity_context": {
    "user_id": "user_123",
    "roles": ["ops_analyst"]
  },
  "policy_context": {
    "allowed_actions": ["billing.read"],
    "prohibited_actions": ["billing.refund"]
  },
  "purpose": "read_only_billing_check",
  "payload_ref": "s3://aegisops/a2a/a2a_001.redacted.json",
  "expires_at": "2026-07-28T11:00:00Z"
}
```

### Minimum API surface

Application APIs:

- `POST /cases`
- `GET /cases/{case_id}`
- `POST /cases/{case_id}/run`
- `GET /workflow-runs/{run_id}`
- `POST /workflow-runs/{run_id}/cancel`
- `GET /workflow-runs/{run_id}/replay`
- `GET /workflow-runs/{run_id}/evidence`
- `GET /workflow-runs/{run_id}/proposals`
- `POST /approvals/{proposal_id}`
- `POST /events/feedback`

Admin and governance APIs:

- `POST /sources`
- `POST /sources/{source_id}/ingest`
- `POST /memory/{memory_id}/correct`
- `POST /memory/{memory_id}/delete`
- `POST /capabilities`
- `POST /capabilities/{capability_id}/disable`
- `POST /mcp/servers`
- `POST /a2a/handoffs`
- `POST /evals/run`
- `POST /releases`
- `POST /releases/{release_id}/approve`
- `POST /releases/{release_id}/canary`
- `POST /releases/{release_id}/rollback`
- `GET /metrics`
- `GET /healthz`
- `GET /readyz`

## 11. Agent runtime and workflow lifecycle

### Required state graph

Use explicit states:

- `accepted`
- `classified`
- `context_loaded`
- `evidence_retrieved`
- `evidence_verified`
- `plan_drafted`
- `plan_checked`
- `action_proposed`
- `awaiting_approval`
- `approval_rejected`
- `approved_action`
- `executing_tool`
- `verifying_effect`
- `compensating`
- `recovering`
- `escalated`
- `completed`
- `terminated_budget`
- `terminated_policy`
- `failed`

### Runtime rules

- Every transition is recorded.
- Every model call has a prompt version and output schema.
- Every tool call has a validated schema and policy decision.
- Every memory read and write has a policy decision.
- Every retrieval call has tenant and access filters.
- Every loop has max steps, max time, max cost, and stop conditions.
- Reflection or verifier steps are bounded and measured.
- The runtime must terminate safely when evidence, policy, budget, or tools are insufficient.

### Agent pattern comparison

Compare:

- Deterministic baseline.
- Bounded ReAct-style loop.
- Plan-and-execute.
- Reflection or verifier variant.
- One selected framework adapter.

Report:

- Task success.
- Tool correctness.
- Invalid-action rate.
- Step count.
- Latency.
- Cost.
- Recovery behavior.
- Failure modes.

## 12. Provider gateway and framework portability

### Provider requirements

Implement:

- Provider-neutral chat interface.
- Structured output interface.
- Streaming interface.
- Tool-call response normalization.
- Provider error taxonomy.
- Retry and circuit-breaker policy.
- Fallback policy.
- Cost attribution.
- Context and token budget enforcement.
- Provider metadata in traces.

Provider paths:

- Azure OpenAI or selected primary enterprise provider.
- One alternate hosted provider or compatible substitute.
- One open-model route through vLLM, TensorRT-LLM, or deterministic local stub.
- Fake provider for tests.

### Framework comparison

Compare:

- Explicit custom state graph.
- LangGraph or equivalent.
- Semantic Kernel where relevant to .NET lane.
- Provider-native agent SDK spike.
- LlamaIndex, LangChain, AutoGen, CrewAI, or OpenAI Agents SDK as limited comparison candidates.

Implement only one deeply behind local interfaces. The durable evidence is contracts, tests, and operational behavior, not framework branding.

### Prompt and context controls

Required:

- Prompt registry.
- Output schema registry.
- Zero-shot versus few-shot comparison.
- Edge-case regression suite.
- Context assembly policy.
- Token and cost preflight.
- Prompt caching where supported.
- Semantic or tool-result cache with authorization-aware keys.
- Cache invalidation on policy, source, memory, and release changes.

## 13. Retrieval and governed memory

### Retrieval requirements

Implement:

- Source registry.
- Document ingestion.
- Chunking.
- Embeddings.
- BM25 or lexical retrieval.
- Dense retrieval.
- Hybrid retrieval.
- Reranking.
- Metadata filters.
- Permission filters.
- Freshness checks.
- Citation validation.
- Abstention taxonomy.
- Retrieval benchmark.
- Production backend plus FAISS local baseline.

### Memory categories

Keep separate:

- Request context.
- Session state.
- Durable workflow state.
- User-preference memory.
- Retrieval-backed memory.
- Summarized memory.

### Memory write policy

A memory write must include:

- Subject.
- Tenant.
- Purpose.
- Source.
- Provenance.
- Consent state or allowed policy basis.
- Classification.
- Version.
- Creation time.
- Expiration time.
- Correction behavior.
- Deletion behavior.
- Derived artifacts to invalidate.

### Memory tests

Required tests:

- Missing consent.
- Poisoned memory proposal.
- Duplicate write.
- Expired memory.
- Revoked access.
- Cross-tenant access.
- Deletion during active session.
- Correction propagation.
- Summary drift.
- Verified forgetting.

## 14. Tools, MCP, and A2A

### Tool requirements

Every tool needs:

- Name.
- Owner.
- Risk level.
- Input schema.
- Output schema.
- Required permissions.
- Rate limit.
- Timeout.
- Retry policy.
- Idempotency policy.
- Result-size limit.
- Compensation plan.
- Verification method.
- Audit event.

### Required tools

Implement at least:

- `policy.search` read tool.
- `ticket.lookup` read tool.
- `asset.lookup` or `customer.lookup` read tool.
- `ticket.update_status` approval-gated write tool.
- `notification.draft` draft tool.
- `notification.send` approval-gated external action or simulated equivalent.

### MCP requirements

The MCP integration must:

- Trust only approved servers.
- Pin capability versions.
- Propagate user and tenant identity.
- Enforce authorization in the application.
- Validate schemas.
- Bound result size.
- Treat tool descriptions and results as untrusted.
- Log operations.
- Support cancellation.
- Test malicious descriptions and payloads.

### A2A requirements

The A2A handoff must:

- Authenticate source and target.
- Carry identity context.
- Carry tenant context.
- Carry policy context.
- Limit allowed actions.
- Record purpose and expiration.
- Validate response schema.
- Deny unauthorized escalation.
- Resume source workflow or escalate on failure.

## 15. Safety, privacy, security, and governance

### Required controls

- Prompt-injection detection and containment.
- Untrusted content labelling.
- PII and secret detection.
- Output DLP.
- Tool permission service.
- Tenant isolation.
- Retrieval permission enforcement.
- Memory permission enforcement.
- Rate and spend limits.
- Sandbox for any automation or code-like capability.
- Capability allowlists.
- Supply-chain and dependency scanning.
- Container image scanning.
- Secret scanning.
- Audit logs.
- Evidence export scoping.

### Red-team categories

Include:

- Prompt injection in retrieved documents.
- Malicious MCP tool description.
- Malicious MCP tool result.
- A2A context escalation.
- Approval bypass attempt.
- Tool argument mutation after approval.
- Duplicate write attempt.
- SQL injection.
- Excessive fetch.
- Cross-tenant data request.
- Memory poisoning.
- Expired memory use.
- PII exfiltration.
- Arabic prompt injection.
- Translation ambiguity.
- Denial-of-service through large inputs.

### Prohibited claims

Do not claim:

- Autonomous remediation without human approval.
- Compliance certification without legal review.
- Memory safety without deletion and cross-tenant tests.
- Arabic readiness without separate Arabic eval results.
- Tool safety from prompts alone.
- MCP safety without allowlists and identity propagation.
- Provider portability from a wrapper interface alone.
- Safe replay if hidden reasoning or sensitive content is stored.
- Production readiness without rollback, failover, and failure drills.

## 16. Evaluation and release gates

### Required datasets

Create versioned datasets for:

- English happy paths.
- Arabic happy paths.
- Difficult cases.
- Boundary cases.
- Tool failures.
- Provider failures.
- Retrieval failures.
- Permission violations.
- Memory write and deletion cases.
- MCP malicious cases.
- A2A authorization cases.
- Adversarial prompt-injection cases.
- Escalation cases.
- Multimodal attachment cases.

### Required metrics

Measure:

- Task completion.
- Structured-output validity.
- Evidence sufficiency.
- Citation accuracy.
- Tool selection.
- Argument correctness.
- Approval requirement accuracy.
- Invalid-action rate.
- Recovery success.
- Escalation correctness.
- Memory usefulness.
- Memory stale rate.
- Unauthorized evidence leakage.
- Unauthorized action leakage.
- English and Arabic quality.
- Refusal and over-refusal.
- Latency.
- Cost per successful task.

### Starter release gates

Initial gates:

- Structured output validity at least 95 percent.
- Zero successful unauthorized writes.
- Zero unauthorized evidence in model context.
- Zero cross-tenant memory reads.
- Critical prompt-injection cases blocked.
- Approval package exactness tests pass.
- Tool argument correctness meets threshold.
- English and Arabic task-completion thresholds defined and reported.
- Memory deletion and expiration tests pass.
- Safe replay redaction tests pass.
- Provider failover drill passes.
- Rollback target exists and is tested.

### Judge calibration

If model judges are used:

- Calibrate against human labels.
- Report agreement.
- Report failure slices.
- Keep human labels for release-critical safety and action cases.
- Do not let uncalibrated judges approve releases alone.

### Required release report

Each release report must include:

- Release tuple.
- Prompt, model, policy, tool, memory, retrieval, eval, and deployment versions.
- English and Arabic evaluation.
- Safety and red-team results.
- Retrieval and memory results.
- Tool and approval results.
- MCP and A2A results.
- Latency and cost.
- Failure drills.
- Canary plan.
- Rollback plan.
- Known limitations.
- Approval record.

## 17. Multimodal and localization profile

### Multimodal slice

Implement at least one:

- Document attachment.
- Scanned policy image.
- Form image.
- Voice-note transcript.

The slice must:

- Extract structured evidence.
- Preserve modality provenance.
- Measure extraction quality.
- Route low-confidence cases to human review.
- Apply privacy and retention controls.
- Allow downstream tool use only from validated outputs.

### Arabic and UAE-style profile

Support:

- Arabic case intake.
- Arabic prompt and output evaluation.
- Arabic retrieval cases.
- Arabic safety cases.
- RTL operator UX evidence.
- Locale-specific failure analysis.
- Provider regional availability record.
- Data-flow and residency diagram.
- Retention and cross-border transfer assumptions.
- UAE deployment/control decision record.

This is a technical control record, not legal advice or certification.

## 18. Observability, safe replay, and cost

### Correlation model

Every run should record:

- `trace_id`
- `case_id`
- `workflow_run_id`
- `tenant_id`
- `user_id`
- `language`
- `provider`
- `model`
- `prompt_version`
- `retrieval_index_version`
- `memory_policy_version`
- `tool_policy_version`
- `approval_policy_version`
- `capability_version`
- `deployment_version`
- `cost_event_id`

### Trace spans

Trace:

- Case intake.
- Classification.
- Retrieval.
- Citation validation.
- Memory read.
- Memory write proposal.
- Memory policy decision.
- Model call.
- Structured-output validation.
- Plan validation.
- Tool policy decision.
- Approval request.
- Tool execution.
- Verification.
- Compensation.
- MCP call.
- A2A handoff.
- Replay snapshot.
- Evaluation run.

### Safe replay requirements

Safe replay must:

- Require auditor authorization.
- Show redacted state transitions.
- Show policy decisions.
- Show tool inputs and outputs after redaction.
- Show citations and evidence references.
- Show approval records.
- Show cost and latency.
- Avoid hidden chain-of-thought.
- Avoid raw sensitive prompts where policy forbids them.
- Support export with retention and tenant filters.

### Cost model

Track:

- Cost per case.
- Cost per successful task.
- Cost by provider.
- Cost by model.
- Cost by tenant.
- Cost by capability.
- Retrieval and reranking cost.
- Tool and MCP cost.
- A2A handoff cost.
- Cache savings.
- Budget stops.

## 19. Reliability, deployment, rollback, and failover

### Required service indicators

Define SLIs and objectives for:

- Case API availability.
- Workflow completion.
- Approval latency.
- Model provider latency.
- Retrieval latency.
- Tool execution latency.
- MCP success rate.
- A2A handoff success rate.
- Safe replay availability.
- Evaluation run success.
- Cost event completeness.
- Rollback duration.

### Degraded modes

Document and test:

- Primary provider unavailable.
- Alternate provider unavailable.
- Open-model route unavailable.
- Retrieval backend unavailable.
- Memory service unavailable.
- Tool service unavailable.
- MCP server unavailable.
- A2A target unavailable.
- Approval service unavailable.
- Replay export unavailable.
- Observability pipeline unavailable.
- Policy cache stale.

### Rollback options

Support rollback for:

- Prompt version.
- Output schema.
- Provider routing policy.
- Model selection.
- Retrieval index.
- Memory write policy.
- Tool capability version.
- MCP server version.
- A2A handoff policy.
- Approval policy.
- Agent runtime version.
- Deployment image.
- Feature flag.

### Failure drills

Demonstrate:

- Provider outage and failover.
- Tool failure and recovery.
- MCP failure and fallback or escalation.
- A2A authorization failure.
- Prompt-injection attack blocked.
- Memory deletion during active session.
- Canary regression and rollback.
- Backup restore.
- Safe disable of write tools.

## 20. Step-by-step implementation plan

### Phase 0: Discovery and control map

- Define domain, users, tenants, actions, prohibited actions, risk taxonomy, approval boundaries, success metrics, residency constraints, and non-AI fallback.
- Write PRD, workflow map, threat model, and first golden cases.

### Phase 1: Deterministic baseline and service foundation

- Build typed async services.
- Implement case intake.
- Implement deterministic workflow path.
- Add identity, tenant, roles, audit, and structured errors.
- Add CI quality gates.

### Phase 2: Provider gateway

- Implement provider-neutral interface.
- Add fake provider, primary hosted provider, alternate provider, and open-model route or stub.
- Add structured output, streaming, provider errors, retries, fallback, token and cost budgets.

### Phase 3: Retrieval and evidence

- Add source registry, ingestion, hybrid retrieval, reranking, citations, filters, freshness, and abstention.
- Compare production backend and FAISS baseline.

### Phase 4: Governed memory

- Implement memory schema, write policy, consent, purpose, provenance, expiry, correction, deletion, and derived-summary invalidation.
- Add memory quality and deletion tests.

### Phase 5: Agent runtime

- Add explicit state graph.
- Add bounded planning, execution, verification, recovery, escalation, and termination.
- Compare deterministic, bounded ReAct, plan-and-execute, verifier, and framework-adapter variants.

### Phase 6: Tools, approval, MCP, and A2A

- Implement read tools and approval-gated write tools.
- Add idempotency, retries, compensation, verification, and audit.
- Add secured MCP server or client.
- Add one A2A handoff.

### Phase 7: Safety, evaluation, and feedback

- Add bilingual golden, difficult, adversarial, permission, tool failure, memory, and escalation datasets.
- Add red-team tests.
- Add judge calibration.
- Add reviewed feedback-to-dataset-to-release loop.

### Phase 8: Multimodal and localization

- Add one multimodal input slice.
- Add Arabic and RTL evaluation.
- Add residency, retention, and regional provider control record.

### Phase 9: Observability and safe replay

- Add OpenTelemetry traces, redacted logs, cost events, dashboards, safe replay, replay export, and incident reconstruction.

### Phase 10: Production rollout

- Add Docker, Kubernetes, Terraform, secrets, workload identity, feature flags, canary, rollback, provider failover, backups, load tests, failure drills, and handoff docs.

### Phase 11: Portfolio defense

- Generate all reports.
- Write agent capability card.
- Write business-outcome report.
- Prepare 10-minute technical presentation.

## 21. Completion evidence checklist

### Product and workflow

- Product requirements.
- Workflow map.
- Risk taxonomy.
- Allowed and prohibited actions.
- Non-AI fallback.
- Business-outcome report.

### Architecture and engineering

- Architecture ADRs.
- State graph.
- Provider/framework decision matrix.
- API contracts.
- CI quality gates.
- Fresh-clone deployment proof.

### Retrieval and memory

- Retrieval benchmark.
- Citation validation.
- Access-control tests.
- Memory schema.
- Memory policy.
- Memory quality report.
- Deletion and expiry report.

### Tools and protocols

- Tool contracts.
- Approval package examples.
- MCP security report.
- Capability allowlist.
- A2A handoff report.
- Tool failure and compensation tests.

### Safety and governance

- Threat model.
- Red-team report.
- Unauthorized action report.
- PII and DLP tests.
- Prompt-injection tests.
- Audit records.
- Agent capability card.

### Evaluation

- English golden dataset.
- Arabic golden dataset.
- Adversarial dataset.
- Agent evaluation report.
- Bilingual evaluation report.
- Judge calibration report.
- Blocked release demonstration.

### Observability and operations

- OpenTelemetry traces.
- Dashboards.
- Safe replay report.
- Cost and cache report.
- Failure-injection report.
- Canary, rollback, and failover report.
- Runbooks.
- Platform handoff.

### Localization and residency

- Arabic/RTL report.
- Locale-specific failure analysis.
- Data-flow and residency diagram.
- Retention controls.
- Cross-border transfer assumptions.
- UAE deployment/control decision record.

### Optional .NET lane

- ASP.NET Core OpenAPI contract.
- Provider adapter tests.
- Streaming cancellation test.
- Structured-output validation tests.
- Entra or workload identity diagram.
- Retrieval authorization test.
- MCP/tool approval test.
- OpenTelemetry trace.
- Deployment/rollback runbook.
- Contract/evaluation parity report.

## 22. Industry-level implementation order

Build in this order:

1. Define controls, risk, and non-AI fallback.
2. Build deterministic services and contracts.
3. Add identity, tenant authorization, audit, and CI gates.
4. Add provider gateway and structured outputs.
5. Add permission-aware retrieval.
6. Add governed memory.
7. Add explicit agent state graph.
8. Add read tools.
9. Add approval-gated write tools.
10. Add MCP and A2A after local tool controls are proven.
11. Add bilingual and adversarial evaluation.
12. Add safe replay and observability.
13. Add production rollout, failover, and rollback.

This order prevents the common mistake of adding multi-agent complexity before the platform can safely execute one controlled workflow.

## 23. Common failure modes

- Authorization implemented as prompt text.
- Tool calls executed before policy checks.
- Approval package omits exact arguments.
- Approved arguments change before execution.
- Duplicate writes due to missing idempotency.
- Compensation plan is undocumented.
- Memory is just a saved transcript.
- Memory deletion does not invalidate summaries or indexes.
- Retrieval filters are applied after model context assembly.
- MCP dynamic discovery accepts unapproved tools.
- A2A handoff drops identity or policy context.
- Arabic cases are translated but not evaluated separately.
- Safe replay stores hidden reasoning.
- Logs contain sensitive prompts or unredacted tool outputs.
- Provider fallback changes behavior without evaluation.
- A framework adapter bypasses local policy gates.
- Canary rollback only rolls back code, not prompts, tools, policies, or memory rules.

## 24. Interview defense questions

Product and control:

- What workflow does `AegisOps` automate?
- Which actions are prohibited?
- Which actions require approval?
- What is the non-AI fallback?

Agent architecture:

- Why use an explicit state graph?
- How do you terminate loops?
- What did the pattern comparison show?
- Why is multi-agent handoff not the default?

Authorization and tools:

- Where does authorization run?
- How is approval bound to exact arguments?
- How do you prevent duplicate writes?
- How do you recover from partial failure?

Retrieval and memory:

- How do you prevent unauthorized evidence in context?
- What memory categories exist?
- How does correction and deletion propagate?
- How do you evaluate stale or harmful memory?

MCP and A2A:

- What does MCP add and what risk does it create?
- How do you trust an MCP server?
- What identity reaches the tool?
- What context is sent during A2A handoff?

Evaluation and safety:

- How do English and Arabic results differ?
- Which red-team cases failed initially?
- How are model judges calibrated?
- What blocks a release?

Operations:

- How does safe replay work without chain-of-thought?
- What happens during provider outage?
- How do you roll back a bad prompt, tool, or memory policy?
- How do you explain the residency control record?

## 25. Final definition of done

`AegisOps` is done when:

- A full English and Arabic case can run through intake, retrieval, planning, approval, execution, verification, and safe replay.
- The workflow is an explicit bounded state graph with deterministic fallback.
- Provider gateway supports primary, alternate, open-model or stub, and fake provider routes.
- Permission-aware retrieval and citations prevent unauthorized evidence in context.
- Governed memory supports consent, purpose, provenance, expiry, correction, deletion, and verified forgetting.
- Read tools and approval-gated write tools are schema-validated, authorized, idempotent, audited, verified, and recoverable.
- One secured MCP boundary and one authenticated A2A handoff are implemented and tested.
- English and Arabic evaluation, red-team, memory, retrieval, tool, MCP, A2A, latency, cost, and safety reports exist.
- Safe replay is authorized, redacted, and free of hidden reasoning.
- Provider outage, tool failure, MCP failure, A2A failure, canary regression, rollback, restore, and safe disable drills are demonstrated.
- The repo contains the required docs, cards, runbooks, dashboards, final evidence manifest, and interview-ready business-outcome report.
