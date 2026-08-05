# Atlas AI Platform - Implementation Tickets

## 1. Purpose

This document converts the phase plan into implementation tickets.

Ticket format:

```text
id
phase
area
title
description
status
priority
estimated_size
dependencies
target_files_or_folders
migrations
api_routes
verification_commands
done_criteria
proof_link
```

Every executable ticket must include:

- `dependencies`: ticket IDs or phase names that must be completed first.
- `priority`: P0 for MVP spine blockers, P1 for portfolio-critical work, P2 for production hardening, P3 for optional depth.
- `estimated_size`: XS less than 0.5 day, S 0.5-1 day, M 1-3 days, L 3-5 days, XL more than 5 days.
- `target_files_or_folders`: expected implementation paths before coding starts.
- `verification_commands`: exact commands the developer should run when the ticket is done.
- `done_criteria`: observable proof, not only a statement that code was written.

The short phase tables below are the readable planning view. The executable work-item tables later in this file add the fields needed before coding starts.

Status rule:

All tickets are target implementation tickets. Current status is `Not started` unless code, tests, eval output, screenshots, or deployment evidence exist.

## 2. Scope Freeze

Do not add Phase 26.

The platform is already broad enough. The execution priority is:

```text
Build MVP spine first: Phase 00 to Phase 07 plus light Phase 18 and Phase 19.
```

Recommended first delivery milestone:

```text
MVP-1: upload document -> ingest -> chunk -> embed -> RAG answer with citations -> AI run trace -> eval report.
```

## 3. MVP Spine Tickets

### Phase 00 - Engineering Foundation

Scope: Required MVP.

| Ticket | Area | Task | Acceptance Proof |
|---|---|---|---|
| P00-001 | Repo | Create repo layout with apps, packages, tests, infra, docs | tree matches blueprint |
| P00-002 | Config | Implement typed settings with `.env.example` | config unit tests pass |
| P00-003 | API | Build FastAPI app factory and health routes | `/health` test passes |
| P00-004 | Errors | Implement error envelope and app exceptions | error response test passes |
| P00-005 | Logging | Add request id middleware and structured logs | response includes request id |
| P00-006 | DB | Add SQLAlchemy engine/session and Alembic | migration test passes |
| P00-007 | Worker | Add worker skeleton | worker starts and logs config |
| P00-008 | Docker | Add Postgres and Redis Docker Compose | containers healthy |
| P00-009 | Tests | Add pytest setup and CI-style commands | test suite passes |
| P00-010 | Docs | README setup and run instructions | new developer can run locally |

### Phase 01 - LLM Gateway

Scope: Required MVP.

| Ticket | Area | Task | Acceptance Proof |
|---|---|---|---|
| P01-001 | Schema | Add `model_providers`, `model_routes`, `ai_runs` migration | migration applies cleanly |
| P01-002 | Gateway | Define provider adapter interface | mock provider implements interface |
| P01-003 | Provider | Add one managed chat provider adapter | smoke test behind env flag |
| P01-004 | Mocking | Add fake provider for tests | no tests require real model key |
| P01-005 | Routing | Route by use case: chat, classification, rag_answer, embedding, llm_judge | route unit tests pass |
| P01-006 | Cost | Track input/output/cache/reasoning tokens and estimated cost | ai_run stores usage fields |
| P01-007 | Reliability | Add retry, timeout, and fallback policy | simulated timeout test passes |
| P01-008 | API | Add internal model test endpoint or service call | endpoint returns ai_run id |
| P01-009 | Observability | Emit GenAI span fields | trace sample contains model/request attrs |
| P01-010 | Security | Block provider calls when tenant policy disallows route | restricted route test passes |

### Phase 02 - Prompt System

Scope: Required MVP.

| Ticket | Area | Task | Acceptance Proof |
|---|---|---|---|
| P02-001 | Schema | Add prompt template/version/test case tables plus one-active-version constraint | migration applies and second active version is rejected |
| P02-002 | Service | Build prompt registry and renderer | render test passes |
| P02-003 | Validation | Validate required prompt variables | missing variable test fails safely |
| P02-004 | API | Add prompt CRUD/version/activate endpoints | contract tests pass |
| P02-005 | Tests | Add prompt test runner | prompt test cases execute |
| P02-006 | Governance | Activation requires approved status and writes promotion audit event | draft activation blocked and audit_events row exists |
| P02-007 | AI Runs | Store prompt_version_id in ai_runs and fill prompt span attributes | database row and trace link to prompt version |
| P02-008 | Optimization | Add draft-only optimizer candidate seam; defer optimization job tables to Phase 20 | candidate prompt remains draft and optimizer cannot approve or activate |

### Phase 03 - Structured Outputs

Scope: Required MVP.

| Ticket | Area | Task | Acceptance Proof |
|---|---|---|---|
| P03-001 | Schemas | Define base structured-output models | type tests pass |
| P03-002 | Gateway | Add structured output call method | mock returns parsed object |
| P03-003 | Parser | Validate model output with Pydantic | invalid JSON rejected |
| P03-004 | Repair | Add bounded repair loop | one repair attempt works |
| P03-005 | Logging | Store validation failure metadata | failure visible in ai_runs |
| P03-006 | Tests | Add classification/extraction examples | schema tests pass |
| P03-007 | Safety | Block invalid tool/action fields | unsafe enum test passes |

### Phase 04 - Document Ingestion

Scope: Required MVP.

| Ticket | Area | Task | Acceptance Proof |
|---|---|---|---|
| P04-001 | Schema | Add collection, document, version, page, chunk, job tables | migration applies |
| P04-002 | API | Upload document endpoint with idempotency | duplicate upload handled |
| P04-003 | Storage | Object storage adapter local implementation | file stored and retrievable |
| P04-004 | Worker | Ingestion job pipeline | job moves queued -> processed |
| P04-005 | Extraction | PDF/TXT/MD extraction baseline | text preview stored |
| P04-006 | Cleaning | Normalize whitespace, headers, duplicate text | cleaning tests pass |
| P04-007 | Chunking | Token/page-aware chunker | chunk sizes within limits |
| P04-008 | Lineage | Store parser/chunker/content hash metadata | lineage fields populated |
| P04-009 | UI | Documents list and ingestion status | user sees processing status |
| P04-010 | Failure | Failed ingestion stores error and allows reingest | failure test passes |

### Phase 05 - Embeddings And Vector Database

Scope: Required MVP.

| Ticket | Area | Task | Acceptance Proof |
|---|---|---|---|
| P05-001 | Schema | Add chunk_embeddings and vector extension migration | pgvector migration applies |
| P05-002 | Gateway | Add embedding provider route | embedding mock test passes |
| P05-003 | Worker | Embed chunks in batches | embeddings stored |
| P05-004 | VectorStore | Implement pgvector adapter | semantic search returns chunks |
| P05-005 | Filters | Tenant, collection, metadata filters | cross-tenant search blocked |
| P05-006 | Versioning | Track model, dimension, content hash | changed chunk re-embeds |
| P05-007 | API | Add semantic search endpoint | contract tests pass |
| P05-008 | Debug | Retrieval debug payload includes scores | UI/API shows top-k scores |
| P05-009 | Eval | Add small retrieval eval dataset | recall@k calculated |

### Phase 06 - RAG, Reranking, And Citations

Scope: Required MVP.

| Ticket | Area | Task | Acceptance Proof |
|---|---|---|---|
| P06-001 | Schema | Add rag_queries, retrieval_results, answers, citations | migration applies |
| P06-002 | Query | Build query classification and optional rewrite | rewrite stored |
| P06-003 | Retrieval | Retrieve top-k chunks with ACL filters | tenant isolation test passes |
| P06-004 | Rerank | Add reranker interface and optional mock | reranked order stored |
| P06-005 | Context | Implement context packer with token budget | context trace stored |
| P06-006 | Prompt | Build RAG answer prompt with citation rules | answer references source ids |
| P06-007 | Answer | Generate answer through gateway | ai_run linked to answer |
| P06-008 | Citations | Build citation records from source chunks | citations show document/page/chunk |
| P06-009 | Unknowns | Return not-enough-information when unsupported | hallucination test passes |
| P06-010 | UI | Chat with citation drawer and retrieval trace | demo question works |

### Phase 07 - Evaluation Platform

Scope: Required portfolio.

| Ticket | Area | Task | Acceptance Proof |
|---|---|---|---|
| P07-001 | Schema | Add eval datasets/cases/runs/results | migration applies |
| P07-002 | Import | JSONL eval dataset importer | seed dataset imports |
| P07-003 | Runner | Build eval runner for RAG cases | eval job completes |
| P07-004 | Metrics | Implement correctness, groundedness, citation accuracy | scores stored |
| P07-005 | Retrieval | Implement recall@k and MRR | retrieval report produced |
| P07-006 | Judge | Add LLM-as-judge behind gateway | judge ai_runs stored |
| P07-007 | Calibration | Add human review sample workflow | agreement report exists |
| P07-008 | Thresholds | Candidate promotion threshold check | failing candidate blocked |
| P07-009 | UI | Evaluation dashboard with filters and failed cases | reviewer can inspect failures |
| P07-010 | CI | Add small eval smoke test using fake provider | CI-safe eval passes |

## 4. Agent Portfolio Tickets

### Phase 08 - Tool Calling

| Ticket | Area | Task | Acceptance Proof |
|---|---|---|---|
| P08-001 | Schema | Add tool_definitions/tool_calls | migration applies |
| P08-002 | Registry | Build typed tool registry | tool list returns enabled tools |
| P08-003 | Validation | Validate tool input/output schemas | invalid args rejected |
| P08-004 | Permissions | Enforce required permissions | unauthorized user blocked |
| P08-005 | Dry Run | Add dry-run execution | dry-run has no side effect |
| P08-006 | Audit | Store tool call intent before execution and result after | audit record exists |
| P08-007 | Approval | Create approval request for write tools | approval queue item appears |

### Phase 09 - Controlled Agents

| Ticket | Area | Task | Acceptance Proof |
|---|---|---|---|
| P09-001 | Schema | Add agent_definitions/runs/steps | migration applies |
| P09-002 | State | Implement explicit state machine | state transition tests pass |
| P09-003 | Planner | Generate structured plan | plan schema validates |
| P09-004 | Executor | Execute step loop with max limits | runaway test stops |
| P09-005 | Tools | Connect tool service | tool call appears in trace |
| P09-006 | Verification | Verify tool result and final answer | wrong result caught |
| P09-007 | UI | Agent run trace viewer | step-by-step demo visible |
| P09-008 | Evals | Add agent task dataset | task success scored |

### Phase 10 - Agent Memory

| Ticket | Area | Task | Acceptance Proof |
|---|---|---|---|
| P10-001 | Schema | Add memory_items | migration applies |
| P10-002 | Session | Add conversation summary memory | long chat compacts safely |
| P10-003 | Policy | Add memory write policy | sensitive memory blocked |
| P10-004 | Retrieval | Retrieve scoped memory | no cross-tenant/user leak |
| P10-005 | Retention | Expire memory items | retention job test passes |

### Phase 11 - Safety And Guardrails

| Ticket | Area | Task | Acceptance Proof |
|---|---|---|---|
| P11-000 | Policy | Add minimum safety policy interface for memory/tool risk checks | Phase 10 can call policy without full guardrail system |
| P11-001 | Schema | Add safety_policies/checks | migration applies |
| P11-002 | Input | Prompt-injection input checks | red-team cases blocked |
| P11-003 | Context | Retrieved-context injection checks | malicious document neutralized |
| P11-004 | Output | Output safety and PII checks | leakage test blocked |
| P11-005 | Tools | Tool risk policy and approvals | risky write requires approval |
| P11-006 | Red Team | Red-team catalog and runner | safety report produced |

## 5. Advanced And Production Tickets

| Phase | Ticket Group | Required Tickets |
|---|---|---|
| 12 Multimodal AI | OCR/vision | OCR confidence, bounding boxes, table extraction, image redaction, review UI, evals |
| 13 Voice AI | audio | STT, TTS, realtime session, diarization, consent, retention, voice evals |
| 14 Fine-Tuning | adaptation | managed fine-tune job, LoRA/QLoRA job metadata, dataset redaction, distillation, eval comparison |
| 15 Model Serving | serving | model registry, quantization config, batching, canary routing, rollback drill |
| 16 Classical ML | ML | feature pipeline, classifier/regressor, model eval, inference endpoint, drift monitor |
| 17 Search, Ranking, And Recommendation | ranking | hybrid weighting, feedback signals, recommendation endpoint, ranking eval |
| 18 Deployment And Monitoring | ops | Docker, CI/CD, staging, OTel traces, dashboards, alerts, SLOs, runbooks |
| 19 Capstone Integration | portfolio | demo script, screenshots, architecture docs, eval report, safety report |
| 20 LLM Optimization And Caching | optimization | prompt caching, semantic cache, batch APIs, reasoning routes, streaming tool calls |
| 21 MCP And External Tool Ecosystem | MCP | server registry, discovery, schema mapping, enable/disable, audit, MCP tests |
| 22 Multi-Agent Orchestration | agents | supervisor, handoffs, scoped context, loop prevention, multi-agent eval |
| 23 Advanced RAG And Retrieval Systems | retrieval | parent-child, contextual, HyDE, multi-hop, citation verification, index tuning |
| 24 Generative Media | media | text-to-image, image editing, video/audio generation, safety, provenance, eval |
| 25 Governance And Compliance | governance | system cards, model cards, risk register, provider policy, incident process |

## 6. Executable Ticket Fields For Coding

Each ticket must become an executable issue/card with these fields before coding starts:

```text
id
phase
area
title
description
status
owner
priority
estimated_size
dependencies
target_files_or_folders
files_to_create
files_to_modify
migrations
api_routes
tests_required
evals_required
ui_required
security_review_required
verification_commands
done_criteria
proof_link
```

Every executable ticket must include:

- `dependencies`: ticket IDs or phase names that must be completed first.
- `priority`: P0 for MVP spine blockers, P1 for portfolio-critical work, P2 for production hardening, P3 for optional depth.
- `estimated_size`: XS less than 0.5 day, S 0.5-1 day, M 1-3 days, L 3-5 days, XL more than 5 days.
- `target_files_or_folders`: expected implementation paths before coding starts.
- `verification_commands`: exact commands the developer should run when the ticket is done.
- `done_criteria`: observable proof, not only a statement that code was written.

Status values:

```text
Not started
In progress
Implemented
Tests passing
Evaluated
Reviewed
Portfolio proof
Production ready
```

## 7. MVP-1 Executable Work Items

These rows make the first build milestone executable. The detailed tickets in Section 3 are the task list; this table gives the missing engineering metadata needed before coding starts.

| Phase | Tickets | Depends On | Priority | Est. Size | Target Files Or Folders | Exact Verification Commands |
|---|---|---|---|---|---|---|
| 00 Engineering Foundation | P00-001 to P00-010 | none | P0 | L | `pyproject.toml`, `.env.example`, `apps/api`, `apps/worker`, `packages/core`, `packages/db`, `tests`, `infra/docker-compose.yml` | `python -m ruff check .`<br>`python -m mypy apps packages`<br>`python -m pytest tests/unit tests/api`<br>`docker compose -f infra/docker-compose.yml config` |
| 01 LLM Gateway | P01-001 to P01-010 | Phase 00 | P0 | L | `packages/model_gateway`, `packages/db/models/model_routes.py`, `apps/api/routes/model_gateway.py`, `tests/model_gateway`, `tests/migrations` | `python -m alembic upgrade head`<br>`python -m pytest tests/model_gateway tests/migrations`<br>`python -m pytest tests/api/test_model_gateway.py` |
| 02 Prompt System | P02-001 to P02-008 | Phase 00, Phase 01 | P0 | M | `packages/prompts`, `apps/api/routes/prompts.py`, `packages/db/models/prompts.py`, `tests/prompts`, `tests/migrations` | `python -m alembic upgrade head`<br>`python -m pytest tests/prompts tests/migrations tests/api/test_prompts.py` |
| 03 Structured Outputs | P03-001 to P03-007 | Phase 01, Phase 02 | P0 | M | `packages/structured_outputs`, `packages/model_gateway/structured.py`, `tests/structured_outputs` | `python -m pytest tests/structured_outputs tests/model_gateway/test_structured_outputs.py` |
| 04 Document Ingestion | P04-001 to P04-010 | Phase 00 | P0 | L | `packages/ingestion`, `packages/storage`, `apps/api/routes/documents.py`, `apps/worker/jobs/ingestion.py`, `packages/db/models/documents.py`, `tests/ingestion` | `python -m alembic upgrade head`<br>`python -m pytest tests/ingestion tests/api/test_documents.py tests/worker/test_ingestion_jobs.py` |
| 05 Embeddings And Vector DB | P05-001 to P05-009 | Phase 01, Phase 04 | P0 | L | `packages/retrieval/vector_store.py`, `packages/retrieval/embeddings.py`, `apps/worker/jobs/embeddings.py`, `packages/db/models/embeddings.py`, `tests/retrieval` | `python -m alembic upgrade head`<br>`python -m pytest tests/retrieval/test_embeddings.py tests/retrieval/test_vector_store.py tests/retrieval/test_tenant_filters.py` |
| 06 RAG, Reranking, And Citations | P06-001 to P06-010 | Phase 02, Phase 03, Phase 05 | P0 | XL | `packages/retrieval/retrieval.py`, `packages/retrieval/rerank.py`, `packages/rag/context.py`, `packages/rag/answering.py`, `packages/rag/citations.py`, `apps/api/routes/rag.py`, `tests/retrieval`, `tests/rag` | `python -m alembic upgrade head`<br>`python -m pytest tests/retrieval/test_retrieval.py tests/retrieval/test_rerank.py tests/rag/test_rag_answers.py tests/rag/test_citations.py tests/rag/test_unknowns.py` |
| 07 Evaluation Platform | P07-001 to P07-010 | Phase 03, Phase 06 | P1 | L | `packages/evals`, `apps/worker/jobs/evals.py`, `apps/api/routes/evals.py`, `seed-datasets`, `tests/evals` | `python -m alembic upgrade head`<br>`python scripts/import_eval_dataset.py --path seed-datasets/rag_eval.jsonl --dataset rag_eval`<br>`python -m pytest tests/evals tests/api/test_evals.py` |

MVP-1 is complete only when these end-to-end commands pass together:

```bash
python -m ruff check .
python -m mypy apps packages
python -m alembic upgrade head
python -m pytest tests/unit tests/api tests/model_gateway tests/prompts tests/structured_outputs tests/ingestion tests/retrieval tests/rag tests/evals
python scripts/import_eval_dataset.py --path seed-datasets/rag_eval.jsonl --dataset rag_eval
python scripts/run_eval.py --dataset rag_eval --candidate local_mvp --output artifacts/evals/rag_eval_report.json
```

## 8. Agent, Production, And Advanced Executable Work Items

These phases should not start until MVP-1 is working unless a specific portfolio goal requires them earlier.

| Phase | Depends On | Priority | Est. Size | Target Files Or Folders | Exact Verification Commands |
|---|---|---|---|---|---|
| 08 Tool Calling | Phase 03, Phase 07 | P1 | L | `packages/tools`, `apps/api/routes/tools.py`, `packages/db/models/tools.py`, `tests/tools` | `python -m alembic upgrade head`<br>`python -m pytest tests/tools tests/api/test_tools.py` |
| 09 Controlled Agents | Phase 06, Phase 08 | P1 | XL | `packages/agents`, `apps/api/routes/agents.py`, `packages/db/models/agents.py`, `tests/agents` | `python -m alembic upgrade head`<br>`python -m pytest tests/agents tests/api/test_agents.py`<br>`python scripts/run_eval.py --dataset agent_tasks --candidate agent_mvp --output artifacts/evals/agent_eval_report.json` |
| 10 Agent Memory | Phase 09, P11-000 Safety Policy Minimum | P2 | M | `packages/memory`, `packages/db/models/memory.py`, `tests/memory` | `python -m alembic upgrade head`<br>`python -m pytest tests/memory tests/agents/test_memory_scope.py` |
| 11 Safety And Guardrails | Phase 06, Phase 08 | P1 | XL | `packages/safety`, `apps/api/routes/safety.py`, `tests/safety`, `seed-datasets/safety_redteam.jsonl` | `python -m alembic upgrade head`<br>`python -m pytest tests/safety`<br>`python scripts/run_eval.py --dataset safety_redteam --candidate safety_v1 --output artifacts/evals/safety_report.json` |
| 12 Multimodal AI | Phase 04, Phase 06 | P2 | L | `packages/multimodal`, `apps/worker/jobs/ocr.py`, `apps/api/routes/multimodal.py`, `tests/multimodal` | `python -m pytest tests/multimodal` |
| 13 Voice AI | Phase 01, Phase 06, Phase 11 | P2 | L | `packages/voice`, `apps/api/routes/voice.py`, `apps/worker/jobs/voice.py`, `tests/voice` | `python -m alembic upgrade head`<br>`python -m pytest tests/voice`<br>`python scripts/run_eval.py --dataset voice_eval --candidate voice_v1 --output artifacts/evals/voice_report.json` |
| 14 Fine-Tuning And Adaptation | Phase 07, Phase 11 | P3 | XL | `packages/training`, `apps/worker/jobs/training.py`, `tests/training` | `python -m pytest tests/training`<br>`python scripts/validate_training_dataset.py --path artifacts/training/sample.jsonl` |
| 15 Model Serving And LLMOps | Phase 01, Phase 14 optional | P3 | XL | `packages/model_serving`, `infra/model-serving`, `tests/model_serving` | `python -m pytest tests/model_serving`<br>`docker compose -f infra/model-serving/docker-compose.yml config` |
| 16 Classical ML | Phase 00, Phase 07 | P3 | M | `packages/classical_ml`, `apps/api/routes/ml.py`, `tests/classical_ml` | `python -m pytest tests/classical_ml` |
| 17 Search, Ranking, And Recommendation | Phase 05, Phase 06, Phase 07 | P2 | L | `packages/retrieval/search.py`, `packages/retrieval/ranking.py`, `tests/retrieval`, `tests/ranking` | `python -m pytest tests/retrieval tests/ranking`<br>`python scripts/run_eval.py --dataset rag_eval --candidate hybrid_ranker --output artifacts/evals/ranking_report.json` |
| 18 Deployment And Monitoring | Phase 00, Phase 01, Phase 06 | P1 | L | `infra`, `deploy`, `packages/observability`, `tests/ops` | `docker compose -f infra/docker-compose.yml config`<br>`python -m pytest tests/ops tests/observability` |
| 19 Capstone Integration | Phase 07, light Phase 18 | P1 | M | `apps/web`, `docs/demo`, `artifacts/screenshots`, `artifacts/evals` | `python -m pytest tests/e2e`<br>`python scripts/run_demo_smoke.py --scenario mvp_spine` |
| 20 LLM Optimization And Caching | Phase 01, Phase 06, Phase 07 | P2 | L | `packages/model_gateway/cache.py`, `packages/cache`, `tests/cache` | `python -m pytest tests/cache tests/model_gateway/test_prompt_caching.py` |
| 21 MCP And External Tool Ecosystem | Phase 08, Phase 11 | P1 | L | `packages/mcp`, `packages/tools/mcp_adapter.py`, `tests/mcp` | `python -m pytest tests/mcp tests/tools/test_mcp_tools.py` |
| 22 Multi-Agent Orchestration | Phase 09, Phase 21 | P3 | XL | `packages/agents/orchestration`, `tests/agents/test_multi_agent.py` | `python -m pytest tests/agents/test_multi_agent.py`<br>`python scripts/run_eval.py --dataset agent_tasks --candidate multi_agent_v1 --output artifacts/evals/multi_agent_report.json` |
| 23 Advanced RAG And Retrieval Systems | Phase 06, Phase 17 | P2 | XL | `packages/retrieval/advanced`, `packages/retrieval/graph.py`, `packages/rag/citation_verification.py`, `tests/retrieval/advanced`, `tests/rag` | `python -m pytest tests/retrieval/advanced tests/rag`<br>`python scripts/run_eval.py --dataset rag_eval --candidate advanced_rag --output artifacts/evals/advanced_rag_report.json` |
| 24 Generative Media | Phase 01, Phase 07, Phase 11 | P3 | XL | `packages/media`, `apps/api/routes/media.py`, `apps/worker/jobs/media.py`, `tests/media`, `seed-datasets/media_generation.jsonl` | `python -m alembic upgrade head`<br>`python -m pytest tests/media`<br>`python scripts/run_eval.py --dataset media_generation --candidate media_v1 --output artifacts/evals/media_report.json` |
| 25 Governance And Compliance | Phase 05, Phase 11, Phase 18 | P2 | L | `packages/governance`, `docs/governance`, `tests/governance` | `python -m pytest tests/governance tests/safety`<br>`python scripts/export_governance_pack.py --output artifacts/governance` |

## 9. Dependency Rules For Individual Tickets

Use these rules when converting a row like `P06-001 to P06-010` into issue tracker items:

- Schema tickets normally depend on all schema tickets from earlier required phases.
- API tickets depend on schema and service tickets in the same phase.
- Worker tickets depend on schema, config, and service tickets.
- UI tickets depend on API contract tests for the same feature.
- Eval tickets depend on seed data import plus the feature being evaluated.
- Security tests are not last-minute tasks; they must be attached to the first ticket that creates a risky behavior.
- Any side-effect tool ticket depends on idempotency, permission checks, audit logging, and approval policy.
- Any model route ticket depends on provider policy, token/cost tracking, timeout, fallback, and mock-provider tests.
- Any RAG ticket depends on tenant ACL tests before answer generation is exposed through the UI.

## 10. Execution Discipline

Do not mark a ticket complete because the code compiles. A ticket is complete only when:

- Required migrations run on a clean database.
- Unit and API tests pass.
- Relevant evals run and produce an artifact.
- Logs/traces include required IDs and route/model information.
- Failure paths are tested, not only success paths.
- Docs are updated if a contract, schema, route, or workflow changed.
- The proof link points to a test run, eval report, screenshot, trace, or deployed/demo artifact.
