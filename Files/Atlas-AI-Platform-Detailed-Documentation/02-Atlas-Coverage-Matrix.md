# Atlas AI Platform - Coverage Matrix

## 1. Purpose

This matrix proves what the Atlas AI Platform covers from Python, backend engineering, Generative AI, RAG, agents, safety, evaluation, governance, model operations, deployment, and portfolio perspectives.

This document is not a marketing checklist. Each topic should map to:

- A phase where it is built.
- A module or service where it lives.
- A concrete implementation artifact.
- A test or evaluation proof.
- A portfolio/interview proof.
- A scope level: required MVP, required portfolio, required production, advanced depth, optional breadth, or research depth.

If a topic is only named but has no implementation artifact or proof, then it is not considered truly covered.

## 2. Coverage Levels

Use these levels when judging the platform.

| Level | Meaning |
|---|---|
| Mentioned | Topic is named only. Not enough. |
| Designed | Architecture and interfaces are described. |
| Implementable | Modules, data objects, APIs, and flows are specified. |
| Testable | Tests/evals/acceptance criteria are specified. |
| Portfolio Proof | A reviewer can see working evidence. |
| Production Ready | Monitoring, safety, governance, rollback, and operations are specified. |

Target standard:

```text
Core topics must reach Implementable + Testable + Portfolio Proof.
Production topics must reach Production Ready.
Optional advanced topics can reach Designed or Implementable depending on final scope.
```

## 3. Updated Phase Map

| Phase | Name | Scope Label | Main Purpose |
|---|---|---|---|
| 00 | Engineering Foundation | Required MVP | Python backend foundation, FastAPI, config, DB, logging, tests, Docker. |
| 01 | LLM Gateway | Required MVP | Central controlled model access, provider adapters, cost/latency tracking. |
| 02 | Prompt System | Required MVP | Versioned prompts, rendering, prompt tests, prompt lifecycle. |
| 03 | Structured Outputs | Required MVP | Schema-based LLM outputs, validation, repair, typed backend integration. |
| 04 | Document Ingestion | Required MVP | Upload, extraction, OCR baseline, cleaning, chunking, metadata. |
| 05 | Embeddings And Vector DB | Required MVP | Embedding generation, vector storage, semantic search, metadata filters. |
| 06 | RAG, Reranking, Citations | Required MVP | Grounded answers with retrieval, reranking, context packing, citations. |
| 07 | Evaluation Platform | Required Portfolio | Datasets, scorers, regression runs, judge calibration, thresholds. |
| 08 | Tool Calling | Required Agent Portfolio | Typed tool registry, permissions, dry-run, audit, approval hooks. |
| 09 | Controlled Agents | Required Agent Portfolio | Agent state machine, planning, execution, verification, trace viewer. |
| 10 | Agent Memory | Advanced Depth | Session memory, long-term memory, summarization, retention. |
| 11 | Safety And Guardrails | Required Production | Prompt injection defense, PII, policy checks, red-team tests. |
| 12 | Multimodal AI | Advanced Depth | OCR confidence, document vision, bounding boxes, tables, image redaction. |
| 13 | Voice AI | Advanced Depth | STT, TTS, realtime speech-to-speech, diarization, consent, retention. |
| 14 | Fine-Tuning And Adaptation | Optional Advanced Depth | Managed fine-tuning, LoRA/QLoRA, dataset prep, distillation. |
| 15 | Model Serving And LLMOps | Optional Advanced Depth | Model registry, serving, quantization, batching, canary, rollback. |
| 16 | Classical ML | Optional Breadth | Non-LLM prediction, classification, regression, feature pipelines. |
| 17 | Search, Ranking, And Recommendation | Required Advanced RAG | Hybrid search, ranking signals, recommendation, retrieval tuning. |
| 18 | Deployment And Monitoring | Required Production | CI/CD, Docker, staging, observability, alerts, SLOs. |
| 19 | Capstone Integration | Required Portfolio | End-to-end demo, docs, reports, interview presentation. |
| 20 | LLM Optimization And Caching | Required Production | Prompt caching, semantic caching, batch APIs, reasoning routes, streaming. |
| 21 | MCP And External Tool Ecosystem | Required Agent Portfolio | MCP server registry, tool mapping, permissions, audit, disablement. |
| 22 | Multi-Agent Orchestration | Advanced Depth | Supervisor/worker agents, handoffs, scoped context, multi-agent eval. |
| 23 | Advanced RAG And Retrieval | Advanced Depth | Parent-child, contextual retrieval, HyDE, multi-hop, GraphRAG/RAPTOR optional. |
| 24 | Generative Media | Optional Gen AI Completeness | Image, video, audio/music generation, media safety, provenance, evaluation. |
| 25 | Governance And Compliance | Required Enterprise Maturity | System cards, model cards, risk register, provider policy, incident process. |

## 4. Current Status Versus Target Status

Important honesty rule:

The matrix describes the target implementation coverage. Current repository status is documentation/design unless code, tests, evals, screenshots, deployed URLs, or run outputs exist.

| Area | Current Status | Target Status |
|---|---|---|
| Master architecture | Designed | Implementation reference used by developers |
| Phase 00 learning guide | Written; matching scaffold created | Implemented code plus tests |
| Phases 01-07 learning guides | Not yet written | Written as MVP spine teaching docs |
| MVP code | Phase 00 scaffold created in sibling `Atlas-AI-Platform` folder; Phases 01-07 not implemented | Running local app with tests and demo |
| Proof cells in this matrix | Target proof | Actual proof after implementation |
| Standards controls | Mapped in docs | Verified by tests/reviews/audit artifacts |

Status labels to use later:

```text
Not started
Designed
Ticketed
Implemented
Tested
Evaluated
Portfolio proof
Production ready
```

### 4.1 Supporting Implementation Artifact Documents

These documents improve the matrix from broad design toward implementable and reviewable specifications.

| File | Current Status | Target Proof It Enables |
|---|---|---|
| `03-Atlas-Visual-Architecture-Diagrams.md` | Designed | Architecture review, onboarding, C4/system walkthrough, sequence validation |
| `04-Atlas-Database-Schema-Specification.md` | Designed | Alembic migration tickets, ERD review, schema tests, index review |
| `05-Atlas-Standards-Crosswalk.md` | Designed | Security/governance review against OWASP, AISVS, NIST, MCP, OTel |
| `06-Atlas-Implementation-Tickets.md` | Ticketed target backlog plus executable phase metadata | Phase-by-phase implementation planning with dependencies, priority, estimated size, target files, and verification commands |
| `07-Atlas-Model-Routing-And-Provider-Examples.md` | Designed | Gateway route tests, provider fallback tests, cost/latency route review |
| `08-Atlas-Frontend-UX-Specification.md` | Designed | Frontend screen implementation, empty/loading/error-state checks, UX demo |
| `09-Atlas-Seed-Datasets.md` + `seed-datasets/*.jsonl` + `seed-documents/*.md` | Designed plus starter files and RAG source documents created | JSONL seed files, near-miss RAG source documents, transcript-only voice cases, and source documents for end-to-end RAG, safety, tool, media, voice, and judge evals |
| `10-Atlas-Operations-Runbooks.md` | Designed operations playbook | Incident simulations, on-call checklist, rollback drills, production readiness review |

## 5. Critical Path Coverage

| Path | Phases | What It Proves |
|---|---|---|
| MVP Spine | 00-07 + light 18 + 19 | Practical RAG app with real backend, logging, cost tracking, and evals. |
| RAG Engineer | 00-07 + 17 + 23 + 19 | Deep retrieval, chunking, ranking, citations, retrieval evals. |
| Agentic AI Engineer | 00-11 + 21 + optional 22 + 19 | Tools, agents, memory, MCP, approvals, safety, traces. |
| Production AI Platform | 00-11 + 18 + 20 + 25 + 19 | SLOs, caching, monitoring, governance, incident response. |
| Full Gen AI Breadth | 00-25 | Enterprise LLMs plus media generation, voice, model adaptation, governance. |

## 6. Python And Backend Coverage

| Topic | Phase | Module/Service | Implementation Artifact | Proof |
|---|---|---|---|---|
| Python project structure | 00 | apps, packages | Modular monolith repo layout | Tree, README, imports work |
| Python typing | 00 onward | all packages | Type hints, Pydantic models | type check passes |
| Dependency management | 00 | root | pyproject.toml | install instructions work |
| FastAPI | 00 onward | apps/api | App factory, routers, dependencies | health/API tests |
| Pydantic settings | 00 | packages/core | Settings class | config tests |
| API schemas | 00 onward | apps/api/schemas | Request/response models | contract tests |
| Error handling | 00 | packages/core | AppError, error envelope | error tests |
| Middleware | 00 | apps/api/middleware | request id middleware | response header test |
| SQLAlchemy | 00 onward | packages/db | engine, session, models | DB tests |
| Alembic migrations | 00 onward | packages/db/migrations | migration scripts | migration CI check |
| PostgreSQL | 00 onward | db service | relational schema | integration tests |
| Redis | 00, 04, 07, 18 | worker/queues/cache | queue/cache config | worker/job tests |
| Background workers | 00, 04, 05, 07, 14, 20, 24 | apps/worker | jobs for ingestion/evals/batch/media | job status tests |
| Docker Compose | 00, 18 | infra | local Postgres/Redis/vector stack | local run proof |
| API pagination | 00 onward | apps/api | cursor pagination standard used by list APIs | list endpoint tests |
| Idempotency | 08, 13, 21, 24 | tools/API | idempotency keys | duplicate action tests |
| Frontend console | 19 | apps/web | dashboard pages | demo walkthrough |

## 7. LLM And Prompt Engineering Coverage

| Topic | Phase | Module/Service | Implementation Artifact | Proof |
|---|---|---|---|---|
| LLM API calls | 01 | model_gateway | chat adapter | mocked and real call test |
| Provider abstraction | 01 | model_gateway/providers | common provider interface | provider swap test |
| Model routing | 01, 20 | model_gateway/router | route by use case | route config test |
| Token tracking | 01, 20 | model_gateway | ai_runs token fields | AI run record |
| Cost tracking | 01, 18, 20 | observability/costs | cost_records | dashboard/report |
| Retry and timeout | 01 | model_gateway | retry policy | simulated timeout test |
| Streaming text | 01, 20 | model_gateway | stream assembler | streaming test |
| Streaming tool calls | 20 | model_gateway/tools | tool-call delta assembler | partial tool arg test |
| Partial structured streaming | 20 | model_gateway/structured | final validation after stream | invalid stream test |
| Prompt templates | 02 | prompts | prompt_templates table | prompt version UI/API |
| Prompt versioning | 02 | prompts | prompt_versions table | version activation test |
| Prompt tests | 02, 07 | prompts/evals | prompt test cases | regression report |
| Prompt variables | 02 | prompts/renderer | variable validation | missing variable test |
| Automatic prompt optimization | 02, 07, 20 | prompts/evals | draft-only candidate seam in Phase 02; optimization jobs/candidates in Phase 20 | candidate remains draft; baseline vs candidate report |
| Structured outputs | 03 | model_gateway/structured | Pydantic schemas | schema validation test |
| JSON repair loop | 03 | structured outputs | repair prompt | invalid JSON repair test |
| Function/tool call schemas | 03, 08 | tools | input/output schemas | schema contract tests |
| Reasoning models | 20 | model_gateway/router | reasoning budget fields | quality/cost eval |
| Reasoning token tracking | 20 | ai_runs | reasoning token fields | run metadata proof |
| Provider capability matrix | 20 | model_gateway | provider feature flags | unsupported feature test |

## 8. RAG, Search, And Retrieval Coverage

| Topic | Phase | Module/Service | Implementation Artifact | Proof |
|---|---|---|---|---|
| Document upload | 04 | ingestion/API | upload endpoint | uploaded doc record |
| Text extraction | 04 | ingestion | parser pipeline | extracted text preview |
| OCR baseline | 04, 12 | ingestion/multimodal | OCR job | OCR confidence output |
| Cleaning | 04 | ingestion | normalization rules | cleaned text diff |
| Chunking | 04 | ingestion/chunking | chunk table | chunk viewer |
| Metadata capture | 04 | ingestion | metadata_json | filtered retrieval test |
| Embeddings | 05 | retrieval/model_gateway | embedding jobs | vectors stored |
| Vector DB | 05 | retrieval | pgvector/Qdrant adapter | semantic search test |
| Embedding versioning | 05 | retrieval | model + hash fields | re-embed test |
| Vector index tuning | 05, 23 | retrieval | vector_index_versions | recall/latency benchmark |
| HNSW/IVF tradeoffs | 23 | retrieval | index params | p95 vs recall report |
| Matryoshka embeddings | 23 | retrieval | dimension-used metadata | dimension eval |
| Quantized embeddings | 23 | retrieval | quantized index option | recall drop report |
| ColBERT/late interaction | 23 | retrieval | optional retriever plugin | quality/cost report |
| Semantic search | 05 | retrieval | search endpoint | top-k result test |
| Hybrid search | 17, 23 | retrieval | vector + keyword merge | hybrid beats baseline eval |
| Query rewrite | 06 | rag/prompts | rewrite prompt | retrieval eval |
| Multi-query retrieval | 06, 23 | retrieval | query variants | recall improvement report |
| Reranking | 06 | retrieval/reranking | reranker adapter | rank quality test |
| Context packing | 06 | rag | token budget packer | context trace |
| Citations | 06 | rag | answer_citations | citation display |
| Citation verification | 23 | rag/evals | claim-support verifier | citation accuracy score |
| Parent-child retrieval | 23 | retrieval | parent_chunk_id | answer completeness eval |
| Contextual retrieval | 23 | retrieval | generated chunk context | retrieval lift report |
| HyDE | 23 | retrieval | hypothetical doc query | strategy eval |
| Multi-hop retrieval | 23 | rag | subquestion records | multi-hop eval |
| GraphRAG/RAPTOR | 23 | retrieval | optional experiments | proof only if beats baseline |
| ACL-filtered retrieval | 06, 11, 23 | retrieval/auth | tenant/permission filters | cross-tenant test |
| Delete/reindex lifecycle | 11, 23 | ingestion/retrieval | index versions/tombstones | deleted doc not retrieved |


## 9. Agents, Tools, MCP, And Memory Coverage

| Topic | Phase | Module/Service | Implementation Artifact | Proof |
|---|---|---|---|---|
| Tool registry | 08 | tools | tool_definitions | tool list/API |
| Tool schemas | 08 | tools/schemas | input/output JSON schema | schema validation test |
| Tool permissions | 08 | tools/auth | permission mapping | unauthorized call fails |
| Dry-run tool execution | 08 | tools | dry-run endpoint | dry-run result |
| Tool audit trail | 08 | tools/observability | tool_calls table | trace view |
| Human approval | 08, 09, 11 | approvals/tools/agents | human_approvals table | approval demo |
| Agent state machine | 09 | agents | explicit states | step trace |
| Agent planning | 09, 20 | agents/planner | structured AgentPlan | plan validation test |
| Agent verification | 09 | agents/verifier | verifier step | wrong tool result caught |
| Agent limits | 09 | agents/policies | max steps/cost/tool calls | runaway test |
| Agent trace viewer | 09, 19 | web/agents | step timeline | demo trace |
| Agent memory | 10 | memory | memory_items | scoped memory test |
| Conversation summarization | 10 | memory | summary job | long conversation test |
| Memory retention | 10, 25 | memory/governance | expires_at/retention jobs | retention test |
| Memory poisoning defense | 10, 11 | memory/safety | write policy | malicious memory blocked |
| Agent identity | 22 | agents/auth | scoped execution context | scope enforcement test |
| Scoped credentials | 22 | tools/integrations | per-run tool scope | tool access test |
| Multi-agent supervisor | 22 | agents | collaboration records | supervisor demo |
| Agent handoffs | 22 | agents | agent_handoffs table | handoff trace |
| Agent-to-agent rules | 22 | agents/safety | structured handoff schema | loop prevention test |
| MCP server registry | 21 | tools/integrations | mcp_servers table | server registration demo |
| MCP discovery | 21 | tools | discover and map tools | schema import test |
| MCP tool mapping | 21 | tools | mcp_tool_mappings | mapped tool proof |
| MCP disablement | 21 | admin/tools | disable controls | disabled call fails |
| MCP audit | 21 | observability | audit_events/tool_calls | audit trace |

## 10. Safety, Security, And Responsible AI Coverage

| Topic | Phase | Module/Service | Implementation Artifact | Proof |
|---|---|---|---|---|
| Input safety checks | 11 | safety | input_checks | blocked input test |
| Output safety checks | 11 | safety | output_checks | unsafe output test |
| Prompt injection defense | 11 | safety/rag/agents | prompt_injection checks | red-team pass report |
| Indirect prompt injection | 11, 21, 23 | safety | context/tool result checks | malicious document test |
| PII detection | 11, 12, 13 | safety/pii | redaction/checks | PII test suite |
| Cross-tenant isolation | 00, 05, 06, 11 | auth/db/retrieval | tenant filters | isolation tests |
| Tool misuse prevention | 08, 11, 21 | tools/safety | approval/risk checks | bypass attempt fails |
| Excessive agency controls | 09, 11, 22 | agents/safety | max steps, approvals | runaway blocked |
| Memory poisoning | 10, 11 | memory/safety | memory write policy | poisoned memory rejected |
| Retrieval poisoning | 11, 23 | safety/retrieval | context risk checks | malicious doc test |
| MCP supply-chain risk | 21, 25 | tools/governance | schema review/disable | changed schema blocked |
| Generated media safety | 24 | media/safety | prompt/output media checks | disallowed media blocked |
| Voice consent | 13 | voice/governance | consent metadata | no consent block |
| Bias/fairness eval | 07, 11, 25 | evals/safety | fairness tags/rubrics | fairness report |
| Toxicity eval | 07, 11 | evals/safety | toxicity scorer | toxicity report |
| Red-team catalog | 11, 25 | safety/evals | red_team_cases | red-team results |
| Incident process | 18, 25 | governance | incident records | incident drill |
| Provider data policy | 25 | governance/model_gateway | provider policy table | route blocked by policy |

## 11. Evaluation Coverage

| Topic | Phase | Module/Service | Implementation Artifact | Proof |
|---|---|---|---|---|
| Eval datasets | 07 | evals | eval_datasets | dataset UI/API |
| Eval cases | 07 | evals | eval_cases | JSONL import |
| Prompt evals | 02, 07 | prompts/evals | prompt test cases | prompt comparison |
| RAG retrieval eval | 07, 23 | evals/retrieval | recall/MRR metrics | retrieval report |
| RAG answer eval | 07 | evals/rag | correctness/groundedness | answer score report |
| Citation eval | 07, 23 | evals/rag | citation accuracy scorer | citation report |
| Agent eval | 09, 22 | evals/agents | task datasets | task success report |
| Tool eval | 08, 09 | evals/tools | tool-call scorer | invalid call rate |
| Safety eval | 11 | evals/safety | red-team suite | safety score |
| Media eval | 24 | evals/media | media rubric | media quality report |
| Voice eval | 13 | evals/voice | WER/summary/action scoring | voice report |
| Judge calibration | 07 | evals/judge | calibration samples | human/judge agreement |
| Human review | 07, 25 | evals/governance | review records | reviewer audit |
| Promotion thresholds | 07, 18, 25 | evals/governance | threshold config | failed candidate not promoted |
| Regression testing | 07, 18 | evals/ci | baseline vs candidate | CI eval report |
| Cost/latency eval | 18, 20 | observability/evals | cost comparison | optimization report |

## 12. Model Adaptation, Serving, And Optimization Coverage

| Topic | Phase | Module/Service | Implementation Artifact | Proof |
|---|---|---|---|---|
| Managed fine-tuning | 14 | adaptation/model_gateway | provider fine-tune job | managed model route |
| LoRA | 14 | adaptation | adapter training job | eval comparison |
| QLoRA | 14 | adaptation | quantized adapter training | training report |
| Dataset redaction | 14, 25 | safety/adaptation | redaction pipeline | sensitive data excluded |
| Train/val/test split | 14 | adaptation | dataset version | split integrity test |
| DPO/preference optional | 14 | adaptation | preference dataset | optional eval |
| Model distillation | 14, 20 | adaptation | distillation_jobs | cheaper model eval |
| Model registry | 15 | serving | model registry records | model card link |
| Local/open model serving | 15 | model_server | vLLM/TGI route | inference endpoint |
| Inference quantization | 15 | serving | GPTQ/AWQ/GGUF option | quality/cost report |
| Continuous batching | 15 | serving | serving config | throughput report |
| Canary routing | 15, 18 | gateway/serving | route percentage | canary trace |
| Rollback | 15, 18 | serving/deployment | previous model route | rollback drill |
| Prompt caching | 20 | model_gateway | cache token fields | cost reduction report |
| Semantic caching | 20 | cache/gateway | semantic_cache_entries | cache hit/miss tests |
| Batch APIs | 20 | model_gateway/worker | batch job records | batch eval run |
| Reasoning model routing | 20 | model_gateway | reasoning budget config | cost/quality comparison |

## 13. Multimodal, Voice, And Generative Media Coverage

| Topic | Phase | Module/Service | Implementation Artifact | Proof |
|---|---|---|---|---|
| Image/document understanding | 12 | multimodal | vision extraction pipeline | extracted fields |
| OCR confidence | 12 | multimodal/ingestion | confidence fields | low-confidence review |
| Bounding-box evidence | 12 | multimodal/web | box coordinates | source highlight demo |
| Table extraction | 12 | ingestion/multimodal | table JSON/chunks | table QA test |
| Image redaction | 12, 24 | safety/multimodal | redacted asset | redaction proof |
| STT | 13 | voice | transcription job | transcript output |
| TTS | 13 | voice | audio response | generated audio proof |
| Realtime speech-to-speech | 13 | voice/gateway | realtime session | low-latency demo |
| Diarization | 13 | voice | speaker segments | speaker summary |
| Voice consent/retention | 13, 25 | voice/governance | consent metadata | policy test |
| Text-to-image | 24 | media_generation | generation job | generated image asset |
| Image editing/inpainting | 24 | media_generation | edit job with mask | before/after asset |
| Video generation | 24 | media_generation | async video job | video job trace |
| Audio/music generation | 24 | media_generation | audio generation job | generated audio asset |
| Synthetic data generation | 24 | media_generation/evals | labeled synthetic dataset | contamination check |
| Media provenance | 24, 25 | media/governance | provenance_json | asset lineage report |
| Media safety eval | 24 | safety/evals | media safety checks | blocked unsafe prompt |

## 14. Production, Operations, And Governance Coverage

| Topic | Phase | Module/Service | Implementation Artifact | Proof |
|---|---|---|---|---|
| Structured logs | 00, 18 | observability | JSON logs | request log sample |
| Request tracing | 00, 18 | observability | request/trace id | trace correlation |
| AI run traces | 01, 06, 09, 18 | observability | ai_runs | AI trace view |
| OpenTelemetry-style GenAI fields | 18, 20 | observability | semantic fields | trace export |
| Metrics | 18 | observability | Prometheus/Grafana or equivalent | dashboard |
| Alerts | 18 | observability | alert rules | alert test |
| SLOs | 18 | operations | SLO document/config | SLO dashboard |
| Cost budgets | 01, 18, 20 | observability/model_gateway | cost limits | budget alert |
| CI/CD | 18 | infra/ci | pipeline | passing checks |
| Docker deployment | 18 | infra/docker | containers | local/staging run |
| Staging environment | 18 | infra | staging config | smoke tests |
| Rollback | 15, 18 | deployment | rollback procedure | rollback drill |
| Backups | 18 | operations | backup plan | restore test |
| Runbooks | 18 | docs/runbooks | incident runbooks | simulated incident |
| System card | 25 | governance | system_cards | system card artifact |
| Model cards | 25 | governance | model_cards | model card artifact |
| Risk register | 25 | governance | risk_register_items | risk review |
| Provider data-sharing register | 25 | governance | provider policies | route policy proof |
| Governance review cadence | 25 | governance | review records | review history |
| AI incident report | 25 | governance | ai_incidents | incident workflow |

## 15. Coverage Gaps Now Closed

| Previous Gap | New Placement | Coverage Status |
|---|---|---|
| Generative media absent | Phase 24, Section 32 | Designed and implementable |
| Prompt caching thin | Phase 20, Model Gateway | Implementable and testable |
| Reasoning models thin | Phase 20, Model Gateway | Implementable and measurable |
| MCP thin | Phase 21, Tool Calling | Implementable, permissioned, auditable |
| Multi-agent orchestration absent | Phase 22, Agent Orchestration | Designed and testable |
| Advanced RAG shallow | Phase 23, RAG/Retrieval | Implementable with eval proof |
| Embedding/index depth shallow | Phase 23, Embeddings | Implementable with benchmark proof |
| Semantic caching absent | Phase 20 | Implementable with safety controls |
| Batch APIs absent | Phase 20 | Implementable with worker proof |
| Distillation absent | Phase 14/20 | Designed and implementable |
| Inference quantization thin | Phase 15 | Designed and evaluable |
| Automatic prompt optimization absent | Phase 02/07/20 | Designed and governed |
| Bias/fairness/toxicity eval absent | Phase 07/11/25 | Evaluation rubric added |
| Realtime speech-to-speech absent | Phase 13 | Designed and implementable |
| Governance maturity thin | Phase 25 | System cards, model cards, risk register |
| Data governance thin | Section 11, Phase 25 | Lineage, retention, export, contamination |
| Production SLOs absent | Phase 18, Section 35 | SLO targets added |
| Concrete API contracts thin | Section 13 | Headers, envelopes, examples, errors |
| MVP path absent | Section 2, Phase map | Critical paths and effort added |

## 16. Data Governance Coverage

| Topic | Phase | Module/Service | Implementation Artifact | Proof |
|---|---|---|---|---|
| Data Lineage | 04, 05, 06, 07, 14, 25 | ingestion/retrieval/evals/governance | source, parser, chunker, embedding, prompt, model, dataset version fields | lineage report for one RAG answer |
| Document deletion lifecycle | 04, 05, 23, 25 | ingestion/retrieval/governance | soft delete, vector tombstone/delete job, object retention | deleted document cannot be retrieved |
| Reindexing lifecycle | 05, 23 | retrieval | knowledge_index_versions, vector_index_versions | reindex job and retrieval eval |
| Tenant data export | 25 | governance/admin | export job and artifact | export package generated |
| Retention enforcement | 10, 11, 13, 24, 25 | memory/safety/voice/media/governance | expires_at fields and retention jobs | expired records removed or archived |
| Dataset Contamination prevention | 07, 14, 24, 25 | evals/adaptation/media/governance | dataset purpose, source, split, synthetic labels, review status | train/eval overlap check |
| Provider data-sharing policy | 01, 15, 25 | model_gateway/governance | provider policy table | restricted tenant route test |

## 17. Remaining Honest Scope Limits

Even after this expansion, Atlas should be honest about research boundaries.

Not required for implementation-ready industry portfolio:

- Training frontier LLMs from scratch.
- Training diffusion foundation models from scratch.
- Training video foundation models from scratch.
- Building GPU clusters from bare metal.
- Formal AI research proofs.
- Robotics control systems.

Covered at practical engineering level:

- Using and controlling frontier models.
- Integrating media generation APIs.
- Fine-tuning or adapting smaller/open models.
- Serving models where practical.
- Evaluating quality and safety.
- Governing AI systems in enterprise workflows.

Final coverage statement:

```text
Atlas covers enterprise Gen AI engineering from implementation, architecture, evaluation, safety, governance, deployment, and portfolio perspectives. It includes LLM applications as the required core and media generation as an optional completeness track.
```






