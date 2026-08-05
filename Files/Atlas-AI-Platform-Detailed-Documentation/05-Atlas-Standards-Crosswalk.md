# Atlas AI Platform - Standards Crosswalk

## 1. Purpose

This document maps Atlas controls to current AI security, governance, and observability standards.

Referenced standards and guidance:

- OWASP Top 10 for LLMs and Gen AI Apps 2025.
- OWASP Artificial Intelligence Security Verification Standard, AISVS 1.0.
- OWASP agentic AI risk patterns.
- NIST AI RMF Generative AI Profile, NIST AI 600-1.
- Model Context Protocol security and 2026-07-28 final specification concerns.
- OpenTelemetry GenAI semantic conventions repository.

Important implementation rule:

```text
A control is not complete because it appears in this crosswalk. It is complete only when it has code, tests, audit evidence, and operational ownership.
```

## 2. Atlas Control Families

| Atlas Control Family | Modules | Evidence Required |
|---|---|---|
| Input validation | api, safety, schemas | validation tests, blocked unsafe payloads |
| Output validation | model_gateway, structured, safety | schema validation tests, unsafe output tests |
| Prompt governance | prompts, evals, governance | prompt versions, eval reports, approval records |
| RAG grounding | ingestion, retrieval, rag, evals | citations, retrieval traces, citation evals |
| Tenant isolation | auth, db, retrieval, cache | cross-tenant tests, ACL-filtered retrieval proof |
| Tool control | tools, agents, approvals | tool schemas, permission tests, approval logs |
| MCP control | tools, integrations, safety | server registry, schema snapshots, audit, disablement |
| Agent control | agents, safety, observability | state machine, step limits, scoped identity, traces |
| Memory control | memory, safety, governance | memory policy, retention tests, poisoning tests |
| Model lifecycle | model_gateway, adaptation, serving | model cards, eval gates, canary, rollback |
| Data governance | ingestion, evals, adaptation, governance | lineage, retention, export, contamination checks |
| Observability | observability, gateway, agents | GenAI spans, metrics, logs, alerts, SLOs |
| Incident response | governance, observability | runbooks, incident records, drills |

## 3. OWASP LLM Top 10 2025 Crosswalk

| OWASP LLM Risk | Atlas Controls | Implementation Artifacts | Verification Proof |
|---|---|---|---|
| LLM01 Prompt Injection | instruction/data separation, context safety checks, tool validation outside model | safety.prompt_injection, RAG context scanner, tool call validator | direct and indirect prompt-injection red-team suite |
| LLM02 Sensitive Information Disclosure | tenant ACLs, PII detection, provider data policy, output redaction | auth permissions, safety.pii, provider policies, audit logs | PII leakage tests, cross-tenant tests |
| LLM03 Supply Chain | provider registry, model cards, MCP registry, dependency scanning | model_providers, mcp_servers, model_cards | provider review, schema change review, SBOM/dependency scan |
| LLM04 Data and Model Poisoning | dataset lineage, document provenance, memory write policy, eval/train split control | dataset purpose/split fields, document checksums, memory_items review status | contamination checks, poisoned document/memory tests |
| LLM05 Improper Output Handling | structured output validation, output safety checks, tool result sanitization | Pydantic schemas, output_checks, tool output sanitizer | invalid JSON tests, XSS/unsafe output tests |
| LLM06 Excessive Agency | tool allowlists, scoped agent identity, max steps/cost, human approval | agent execution context, approval workflow, tool risk levels | approval bypass tests, max-step tests |
| LLM07 System Prompt Leakage | prompt access control, prompt redaction in logs, output checks | prompt_permissions, redacted ai_runs | prompt extraction red-team tests |
| LLM08 Vector and Embedding Weaknesses | ACL-filtered retrieval, index versioning, vector deletion, retrieval poisoning defense | tenant filters, knowledge_index_versions, safety checks | cross-tenant vector tests, deleted doc retrieval tests |
| LLM09 Misinformation | RAG grounding, citations, unknown-answer behavior, eval thresholds | rag_answers, citations, groundedness scorer | hallucination/citation eval reports |
| LLM10 Unbounded Consumption | cost budgets, token limits, rate limits, batch estimates, queue controls | cost_records, model route limits, SLO alerts | cost spike tests, budget alert tests |

## 4. OWASP AISVS 1.0 Crosswalk

AISVS 1.0 organizes AI security requirements into chapters. Atlas should target AISVS Level 2 for production systems handling sensitive data or customer-facing workflows.

| AISVS Chapter | Atlas Coverage | Evidence |
|---|---|---|
| Training Data Governance & Bias Management | dataset source, purpose, split, redaction, contamination checks, fairness evals | dataset lineage report, fairness/toxicity eval report |
| User Input Validation | API schemas, file validation, prompt injection checks, media prompt checks | validation tests, red-team input tests |
| Model Lifecycle Management & Change Control | model registry, prompt/model versioning, eval gates, canary, rollback | model cards, promotion records, rollback drill |
| Infrastructure, Configuration & Deployment Security | typed config, secrets, CI/CD, Docker, staging, alerts | deployment checklist, secret scan, CI logs |
| Access Control & Identity | tenants, RBAC, API keys, scoped agent credentials | permission tests, audit records |
| Supply Chain Security for Models, Frameworks & Data | provider registry, dependency scanning, dataset provenance, MCP review | SBOM, provider policy register, MCP schema snapshots |
| Model Behavior, Output Control & Safety Assurance | structured outputs, moderation, output checks, refusal tests | safety eval suite, output validation reports |
| Memory, Embeddings & Vector Database Security | memory policy, retention, ACL-filtered vector search, vector deletion | memory poisoning tests, cross-tenant vector tests |
| Autonomous Orchestration & Agentic Action Security | state machine, tool governance, approvals, max steps/cost | agent trace, approval audit, agent eval report |
| MCP Security | MCP server registry, schema review, scoped credentials, disablement | MCP tests, schema drift review, audit logs |
| Adversarial Robustness & Attack Resistance | red-team catalog, prompt-injection tests, retrieval poisoning tests | red-team report, regression suite |
| Monitoring, Logging & Anomaly Detection | AI runs, GenAI spans, SLOs, alerts, incident process | traces, dashboards, incident drills |

## 5. Agentic AI Risk Crosswalk

| Agentic Risk | Atlas Control | Required Implementation |
|---|---|---|
| Agent takes unauthorized action | Tool Service enforces permissions and approvals outside the model | tool permissions, approval workflow, audit records |
| Agent receives too much authority | Scoped execution context per agent run | max tools, max cost, max steps, allowed collections |
| Agent loops or consumes resources | Agent state machine limits | max-step failure test, cost cap test |
| Agent trusts poisoned tool output | Tool output sanitizer and safety check | malicious tool output test |
| Agent leaks data across handoffs | Structured handoff schema with limited context | multi-agent handoff audit |
| Agent identity abuse | Agent credentials expire and cannot exceed user scope | scoped credential tests |
| Agent-to-agent confusion | Supervisor/worker protocol and final verifier | multi-agent eval suite |
| Human approval bypass | Approval required for risky writes | bypass red-team tests |
| MCP tool misuse | MCP mapping through Atlas tool registry | disabled MCP tool call fails |
| Long-running task loss of control | Explicit job/task status, cancel, audit, and ownership | cancel/resume tests |

## 6. NIST AI RMF GenAI Profile Crosswalk

The NIST AI RMF uses Govern, Map, Measure, and Manage functions. Atlas should map each function to concrete system artifacts.

| NIST Function | Atlas Implementation | Evidence |
|---|---|---|
| Govern | system cards, model cards, risk register, review cadence, provider data policy | governance review records |
| Map | use-case definitions, data lineage, tenant policy, risk classification | system card, data lineage report |
| Measure | eval datasets, safety tests, RAG metrics, agent metrics, SLOs | eval reports, dashboards |
| Manage | incident runbooks, rollback, model route disablement, approval gates, retention jobs | incident records, rollback drills |

GenAI-specific risk dimensions covered:

- Confabulation and misinformation through RAG grounding and evals.
- Data privacy through PII controls and provider policy.
- Harmful content through safety checks and red-team tests.
- Intellectual property/media risk through generated media policy and provenance.
- Security risk through OWASP LLM, AISVS, and MCP controls.
- Environmental/cost risk through cost budgets and optimization.

## 7. MCP Security Crosswalk

| MCP Concern | Atlas Control | Implementation Detail | Proof |
|---|---|---|---|
| Untrusted MCP server | MCP server registry and review | `mcp_servers.status=pending_review` by default | server cannot be called before approval |
| Tool schema drift | schema hash and snapshot | `mcp_tool_mappings.schema_hash` | changed schema requires review |
| Unauthorized MCP tool | Atlas permission checks | MCP mapped into `tool_definitions` | unauthorized call rejected |
| Risky write MCP tool | human approval | `requires_approval=true` | approval trace |
| Tool result injection | safety check on MCP results | tool output sanitizer | malicious result blocked |
| Stateless protocol state loss | explicit handles in tool arguments | task/resource handles stored as data | multi-step MCP flow test |
| Routing and rate limiting | protocol/method metadata | record MCP method/name/protocol version | gateway routing logs |
| Cache safety | ttl/cache-scope respected | cache entries scoped by user/tenant/global | cache leak test |
| Trace propagation | W3C trace context through MCP metadata | trace ids attached to MCP calls | cross-system trace proof |
| MCP Apps UI risk | sandboxed UI review and consent | app templates reviewed before render | UI action audit |
| Long-running tasks | task handle lifecycle | task status/cancel/update | task cancellation test |

## 8. OpenTelemetry GenAI Crosswalk

The OpenTelemetry GenAI conventions are maintained in a separate GenAI semantic conventions repository. Atlas should use current names from that repository and keep provider-specific attributes separate from generic Atlas fields.

Recommended generic GenAI attributes:

```text
gen_ai.operation.name
gen_ai.provider.name
gen_ai.request.model
gen_ai.response.model
gen_ai.request.max_tokens
gen_ai.request.temperature
gen_ai.request.top_p
gen_ai.request.stream
gen_ai.request.reasoning.level
gen_ai.response.finish_reasons
gen_ai.response.id
gen_ai.response.time_to_first_chunk
gen_ai.usage.input_tokens
gen_ai.usage.output_tokens
gen_ai.usage.reasoning.output_tokens
gen_ai.usage.cache_creation.input_tokens
gen_ai.usage.cache_read.input_tokens
gen_ai.prompt.name
gen_ai.prompt.version
gen_ai.output.type
gen_ai.retrieval.query.text
gen_ai.retrieval.top_k
gen_ai.retrieval.documents
gen_ai.tool.name
gen_ai.tool.type
gen_ai.tool.call.id
gen_ai.tool.call.arguments
gen_ai.tool.call.result
gen_ai.tool.definitions
gen_ai.agent.id
gen_ai.agent.name
gen_ai.agent.version
gen_ai.workflow.name
gen_ai.conversation.id
gen_ai.conversation.compacted
gen_ai.memory.store.id
gen_ai.memory.record.count
```

Recommended MCP attributes:

```text
mcp.protocol.version
mcp.method.name
mcp.session.id where applicable to older protocol versions
mcp.resource.uri
```

Atlas custom attributes should use a separate namespace:

```text
atlas.tenant.id
atlas.user.id
atlas.ai_run.id
atlas.rag.query_id
atlas.rag.answer_id
atlas.retrieval.strategy
atlas.retrieval.index_version
atlas.citation.count
atlas.groundedness.score
atlas.agent.run_id
atlas.agent.step_number
atlas.tool.risk_level
atlas.approval.required
atlas.safety.status
atlas.cost.estimated_usd
```

Privacy rule:

Do not capture full prompts, messages, memory records, retrieved documents, or tool arguments by default. These may contain sensitive or private data. Capture only redacted previews unless a tenant explicitly opts in.

## 9. Implementation Evidence Checklist

A standards crosswalk is complete only when these artifacts exist:

```text
[ ] OWASP LLM red-team suite
[ ] AISVS Level 2 checklist
[ ] NIST Govern/Map/Measure/Manage evidence folder
[ ] MCP server review checklist
[ ] Provider data-sharing register
[ ] System card
[ ] Model cards
[ ] Risk register
[ ] Incident runbooks
[ ] OpenTelemetry GenAI trace sample
[ ] Cross-tenant security test report
[ ] Prompt/model promotion record
[ ] Evaluation threshold report
```

## 10. Source Links

- OWASP LLM Top 10 2025: https://genai.owasp.org/llm-top-10/
- OWASP AISVS 1.0: https://owasp.org/www-project-artificial-intelligence-security-verification-standard-aisvs-docs/
- NIST AI RMF Generative AI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- OpenTelemetry GenAI semantic conventions: https://github.com/open-telemetry/semantic-conventions-genai
- MCP 2026-07-28 final specification: https://modelcontextprotocol.io/specification/2026-07-28
