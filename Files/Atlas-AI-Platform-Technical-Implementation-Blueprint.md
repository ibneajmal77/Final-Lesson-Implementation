# Atlas AI Platform - Technical Implementation Blueprint

Updated: July 31, 2026

## 1. Purpose

Atlas is a single flagship AI platform designed to prove practical industry readiness across Python, Generative AI, Applied AI, LLM applications, RAG, AI agents, evaluation, safety, MLOps, multimodal AI, voice AI, model adaptation, classical machine learning, search, ranking, and recommendation systems.

The project is intentionally one coherent product, not many disconnected demos. It starts as a modular monolith so a learner can understand the full system end to end. Each internal package has a clean boundary, so later it can be extracted into a service when scale, GPU needs, ownership, or reliability require it.

Core rule:

```text
The application owns permissions, validation, tools, memory, evaluation, audit, and actions.
The LLM generates, extracts, ranks, reasons, or proposes inside controlled boundaries.
```

This document is the engineering source of truth before coding. The companion learning document explains the same project in teaching form.

## 2. Business Scenario

A company has support tickets, internal policies, contracts, invoices, scanned forms, product data, images, voice calls, operational logs, and customer records spread across disconnected systems. Teams waste time finding evidence, drafting replies, extracting fields, checking policies, deciding next actions, and proving whether AI changes improved or harmed quality.

Atlas provides one AI operations platform that can:

- ingest tickets, documents, tables, forms, images, and audio;
- answer questions using evidence and citations;
- summarize, classify, extract, and risk-score support work;
- call tools safely through application-owned permission checks;
- run controlled agent workflows with approval, memory, audit, retry, and rollback;
- evaluate prompts, RAG, agents, safety, cost, and latency;
- fine-tune or adapt open models when prompting/RAG are not enough;
- serve hosted and local models through one gateway;
- add classical ML, search, ranking, and recommendation where they are better than LLMs;
- deploy, monitor, and operate AI features like production software.

Target users:

| User | Needs |
|---|---|
| Support agent | Draft responses, find policy evidence, summarize tickets. |
| Operations lead | Review risky cases, approve AI-suggested actions, track quality. |
| Knowledge manager | Upload policies, manage document versions, inspect retrieval quality. |
| AI engineer | Build prompts, RAG, tools, agents, evals, safety, and adaptation. |
| Platform engineer | Operate model gateway, workers, observability, deployments, and cost controls. |
| Data scientist / ML engineer | Build prediction, ranking, evaluation, drift, and retraining workflows. |
| Auditor / reviewer | Inspect traces, citations, approvals, model versions, risk controls, and incidents. |

## 3. Coverage Goal

Atlas should cover practical AI from all sides. It does not claim to train frontier models from scratch or replace a PhD research program, but it does cover the skills needed for industry Gen AI and AI engineering roles.

Required coverage:

| Area | Atlas Coverage |
|---|---|
| Python engineering | Project structure, packages, typing, validation, tests, async, APIs, workers. |
| Backend and data | FastAPI, SQL, PostgreSQL, Redis, migrations, auth, tenant isolation. |
| LLM applications | Gateway, prompts, structured outputs, streaming, model routing, costs. |
| RAG/search | Documents, chunking, embeddings, vector DB, hybrid search, reranking, citations. |
| Agents | Tool calling, workflows, memory, approval, audit, evaluation, MCP boundary. |
| Evaluation | LLM eval, RAG eval, agent eval, human review, judge models, CI gates. |
| Safety/security | Prompt injection, PII, tenant leaks, tool abuse, guardrails, governance. |
| Fine-tuning | Datasets, SFT, LoRA, QLoRA, optional DPO, MLflow, serving. |
| Multimodal/voice | OCR, images, document vision, STT, TTS, transcripts, realtime flow. |
| MLOps/LLMOps | Registries, monitoring, canary, rollback, cost/latency, dashboards. |
| Classical ML | Features, baselines, XGBoost/LightGBM, calibration, drift, retraining. |
| Search/recommendation | Candidate generation, ranking, similar items, feedback loops. |
| Portfolio/interview | Architecture docs, eval reports, cost reports, demo, incident notes. |

## 4. Architecture Strategy

Atlas starts as a modular monolith:

```text
Browser
  -> apps/web
  -> apps/api
      -> packages/auth
      -> packages/db
      -> packages/model_gateway
      -> packages/prompts
      -> packages/ingestion
      -> packages/rag
      -> packages/evals
      -> packages/agents
      -> packages/tools
      -> packages/safety
      -> packages/observability
      -> packages/ml_training
      -> packages/multimodal
      -> packages/voice
      -> packages/ml
  -> apps/worker
      -> ingestion jobs
      -> embedding jobs
      -> eval jobs
      -> training jobs
      -> reporting jobs
```

Use a separate deployable service only when there is a concrete reason:

- ingestion or evaluation needs independent scaling;
- model serving needs GPU hardware;
- realtime voice needs a different latency/reliability profile;
- agent execution needs isolation from the API;
- security or ownership boundaries require separation.

Production runtime target:

```text
Browser
  -> ingress/API gateway
  -> Atlas API containers
  -> Atlas worker containers
  -> PostgreSQL + pgvector
  -> Redis
  -> object storage
  -> hosted model providers and/or local model server
  -> optional vLLM/SGLang server
  -> MLflow tracking/registry
  -> OpenTelemetry collector
  -> Prometheus/Grafana
```

## 5. Repository Structure

Target structure:

```text
atlas/
  apps/
    api/atlas_api/
      main.py
      dependencies.py
      routes/
      schemas/
    worker/atlas_worker/
      main.py
      queues.py
      jobs/
    web/src/
  packages/
    auth/atlas_auth/
    db/atlas_db/
      models.py
      repositories/
      migrations/
    model_gateway/atlas_model_gateway/
    prompts/atlas_prompts/
      templates/
    ingestion/atlas_ingestion/
    rag/atlas_rag/
    evals/atlas_evals/
      datasets/
    agents/atlas_agents/
    tools/atlas_tools/
    safety/atlas_safety/
    observability/atlas_observability/
    ml_training/atlas_ml_training/
    multimodal/atlas_multimodal/
    voice/atlas_voice/
    ml/atlas_ml/
  infra/
    docker/
    prometheus/
    grafana/
    k8s/
    terraform/
  docs/
    architecture.md
    api-contracts.md
    data-model.md
    threat-model.md
    eval-report.md
    cost-report.md
    rollback-runbook.md
```

Package responsibilities:

| Package | Responsibility |
|---|---|
| `auth` | Tenants, users, roles, permissions, approval policy. |
| `db` | SQLAlchemy models, Alembic migrations, repositories, transactions. |
| `model_gateway` | Provider-neutral LLM, embedding, multimodal, streaming, and local-model access. |
| `prompts` | Prompt templates, prompt versions, schemas, prompt tests. |
| `ingestion` | File parsing, OCR handoff, chunking, document metadata. |
| `rag` | Embeddings, vector search, hybrid search, reranking, citations, answer assembly. |
| `evals` | Golden datasets, scorers, judge prompts, human review, reports, CI gates. |
| `agents` | Controlled workflows, planning, state transitions, memory use, approval waits. |
| `tools` | Tool schemas, execution adapters, idempotency, permission checks, audit records. |
| `safety` | Prompt injection checks, PII redaction, policy enforcement, guardrails. |
| `observability` | Logs, metrics, traces, cost records, run correlation. |
| `ml_training` | SFT, LoRA, QLoRA, optional DPO, datasets, MLflow tracking. |
| `multimodal` | OCR/layout, document vision, image understanding, visual evidence references. |
| `voice` | STT, TTS, call state, transcript summary, realtime latency, consent. |
| `ml` | Classical ML, feature pipelines, ranking, recommendation, drift monitoring. |

## 6. Technology Stack

Core engineering stack:

| Capability | Default | Reason |
|---|---|---|
| Language | Python 3.11+ | Best shared ecosystem for AI, APIs, data, and ML. |
| API | FastAPI | Typed APIs, async support, OpenAPI, easy tests. |
| Validation | Pydantic | Runtime validation for requests, configs, and structured outputs. |
| ORM | SQLAlchemy | Explicit production-grade database modelling. |
| Migrations | Alembic | Versioned schema changes. |
| Database | PostgreSQL | Reliable app data, JSON support, indexes, transactions. |
| Vector store | pgvector first | Keeps SQL and vector search together while learning. |
| Cache/queue state | Redis | Jobs, locks, cache, rate limits, circuit state. |
| Tests | pytest | Standard Python test runner. |
| Lint/type checks | Ruff + mypy/Pyright | Fast quality checks and interface safety. |
| Local runtime | Docker Compose | Reproducible local stack. |
| CI | GitHub Actions | Runs lint, types, tests, eval gates, builds. |

AI stack:

| Capability | Default | Notes |
|---|---|---|
| Hosted LLM | OpenAI adapter first | Add Anthropic/Azure through same gateway interface. |
| Local/open model | Hugging Face Transformers | Used for labs, adaptation, and local inference. |
| Embeddings | Hosted embeddings or sentence-transformers | Always accessed through gateway/adapters. |
| Reranking | sentence-transformers cross-encoder first | Replaceable later. |
| Agent orchestration | Explicit state machine first | LangGraph optional after workflow is understood. |
| Tool boundary | Internal registry first, MCP later | MCP added for external tool/server boundaries. |
| Fine-tuning | Transformers + Datasets + PEFT + TRL + PyTorch | Covers SFT, LoRA, QLoRA, DPO. |
| Experiment tracking | MLflow | Tracks datasets, params, metrics, artifacts, models/adapters. |
| Serving | Hosted APIs first, vLLM/SGLang later | vLLM/SGLang for efficient open-model serving. |
| Voice | STT/TTS adapters, realtime later | Consent and latency must be measured. |
| Multimodal | OCR + vision/multimodal adapter | Store page/region evidence. |

Operations stack:

| Capability | Default |
|---|---|
| Logs | structured JSON logs |
| Traces | OpenTelemetry |
| Metrics | Prometheus |
| Dashboards | Grafana |
| Local deploy | Docker Compose |
| Production path | one cloud provider, then Kubernetes |
| Infrastructure as code | Terraform after local/staging works |
| Rollout | feature flags, canary, rollback |

## 7. Data Architecture

Core tables:

| Group | Tables |
|---|---|
| Identity | `tenants`, `users`, `roles`, `permissions`, `user_roles` |
| Work items | `tickets`, `ticket_messages`, `ticket_events`, `customer_profiles` |
| Knowledge | `documents`, `document_versions`, `document_chunks`, `chunk_embeddings` |
| AI control | `prompts`, `prompt_versions`, `model_routes`, `provider_configs` |
| AI execution | `ai_runs`, `model_outputs`, `structured_outputs`, `cost_events` |
| RAG | `retrieval_runs`, `retrieved_chunks`, `citations`, `rerank_scores` |
| Agents | `agent_runs`, `agent_steps`, `agent_state_snapshots`, `agent_memories` |
| Tools | `tool_definitions`, `tool_calls`, `tool_results`, `idempotency_keys` |
| Human control | `approval_requests`, `approval_decisions`, `review_comments` |
| Evaluation | `eval_datasets`, `eval_cases`, `eval_runs`, `eval_scores`, `judge_runs` |
| Safety | `safety_cases`, `policy_checks`, `pii_findings`, `security_events` |
| ML | `features`, `training_datasets`, `model_versions`, `prediction_runs` |
| Feedback | `user_feedback`, `correction_events`, `dataset_promotion_events` |
| Observability | `trace_links`, `latency_events`, `audit_logs` |

Storage rules:

- PostgreSQL stores business records, AI control data, audit, permissions, evals, and feedback.
- pgvector stores embeddings connected to document chunks and tenant permissions.
- Object storage stores original files, extracted artifacts, audio, images, and model artifacts.
- Redis stores queue state, locks, rate limits, cache, and circuit-breaker state.
- MLflow stores experiment metrics, model/adaptor artifacts, and training runs.

Security rules:

- Every business row carries `tenant_id`.
- Document chunks inherit document permissions.
- Retrieval filters unauthorized chunks before prompt context assembly.
- Tool execution checks application permissions before execution.
- Write tools require approval and idempotency.
- Customer-facing final messages require review unless explicitly low-risk and policy-approved.

## 8. AI Architecture

### LLM Gateway

Only `model_gateway` calls model providers directly.

Responsibilities:

- provider-neutral request/response contracts;
- model routing by feature, tenant, privacy, cost, and latency;
- streaming events;
- structured output validation hooks;
- retry, timeout, circuit breaker, fallback;
- token usage and cost attribution;
- provider metadata and trace correlation;
- hosted model, embedding, multimodal, and local model adapters.

Flow:

```text
Feature service
  -> GatewayRequest
  -> route policy
  -> provider adapter
  -> provider response
  -> validation
  -> usage/cost/tracing
  -> GatewayResponse
```

### Prompt System

Prompts are versioned application assets.

Responsibilities:

- system prompts;
- task prompts;
- few-shot examples;
- output schema instructions;
- untrusted-content boundaries;
- prompt version history;
- regression tests.

### Structured Outputs

Rules:

- every structured output has a Pydantic schema;
- invalid JSON is rejected or retried;
- valid JSON is still policy-checked;
- downstream business logic never uses raw model text for decisions.

Examples:

- ticket classification;
- priority recommendation;
- field extraction;
- risk flags;
- citation-backed answer;
- tool-call proposal.

### Embeddings and Vector Search

```text
Document text
  -> chunking
  -> embedding model
  -> pgvector
  -> query embedding
  -> vector similarity search
  -> candidate chunks
```

### Hybrid Search and Reranking

```text
User question
  -> lexical search
  -> vector search
  -> merge and deduplicate
  -> permission filter
  -> reranker
  -> top evidence chunks
```

### RAG

Rules:

- retrieve before generating;
- cite evidence;
- abstain when evidence is missing;
- evaluate retrieval and generation separately;
- never send unauthorized chunks to the model.

```text
Question
  -> optional query rewriting
  -> retrieval
  -> reranking
  -> context assembly
  -> prompt
  -> LLM answer
  -> citation validation
  -> safety check
  -> response
```

### Tool Calling

Rules:

- tools have schemas;
- tools have permission policies;
- read tools are separate from write tools;
- write tools require approval and idempotency;
- tool results are treated as untrusted text until checked.

### Controlled Agents

Default workflow:

```text
receive task
  -> classify intent
  -> retrieve context
  -> create plan
  -> choose allowed tool
  -> propose action
  -> request approval if needed
  -> execute approved action
  -> verify
  -> summarize
  -> store trace and eval signals
```

Limits:

- max steps;
- max tokens;
- max cost;
- max tool calls;
- timeouts;
- approved tool allowlist;
- explicit stop conditions.

### Agent Memory

Memory types:

- request context;
- session state;
- durable workflow state;
- user preferences;
- retrieval-backed memory;
- summarized memory.

Rules:

- writes require policy;
- sensitive memory has retention;
- users can correct or delete memory;
- memory poisoning tests are required;
- memory never overrides permissions.

### Evaluation

Evaluation types:

- schema validity;
- classification accuracy;
- extraction accuracy;
- retrieval recall@k, MRR, nDCG;
- context relevance;
- answer groundedness;
- citation accuracy;
- hallucination checks;
- LLM-as-judge;
- human review;
- agent task completion;
- tool-call correctness;
- safety and red-team scores;
- latency and cost.

### Safety and Guardrails

Controls:

- input validation;
- prompt injection detection;
- PII detection and redaction;
- tenant boundary checks;
- tool permission service;
- output policy checks;
- jailbreak cases;
- red-team suite;
- audit logging;
- incident process.

### Fine-Tuning and Model Adaptation

Fine-tune only after baselines, prompting, RAG, and evals exist.

```text
feedback and labels
  -> dataset validation
  -> baseline comparison
  -> SFT
  -> LoRA
  -> QLoRA
  -> optional DPO
  -> eval comparison
  -> safety regression
  -> MLflow registry
  -> serving route
```

### Multimodal and Voice

Multimodal flow:

```text
Image or scanned PDF
  -> OCR/layout extraction
  -> vision model analysis
  -> structured extraction
  -> evidence region references
  -> human review if low confidence
```

Voice flow:

```text
Audio stream
  -> speech-to-text
  -> conversation state
  -> LLM/tool/RAG step
  -> text-to-speech
  -> transcript summary
  -> consent and audit record
```

### Classical ML and Recommendation

Non-LLM AI proves tool selection judgment:

- SLA risk prediction;
- ticket priority prediction;
- churn risk;
- similar-ticket search;
- recommended documents;
- recommended replies;
- ranking model.

## 9. Main Communication Flows

### Ticket Draft Flow

```text
Agent opens ticket
  -> API loads ticket and permissions
  -> prompt package prepares task
  -> model gateway calls selected model
  -> structured output validator checks result
  -> safety checks run
  -> draft saved as recommendation
  -> human reviews before customer use
```

### Document Ingestion Flow

```text
User uploads file
  -> API validates tenant, role, file type
  -> original stored in object storage
  -> ingestion job queued
  -> worker extracts text/tables/OCR
  -> chunker creates chunks
  -> embedding job creates vectors
  -> chunks and vectors stored
  -> document version marked searchable
```

### RAG Question Flow

```text
User asks question
  -> API checks permissions
  -> RAG service rewrites query if useful
  -> hybrid retrieval searches permitted chunks
  -> reranker orders evidence
  -> context builder creates prompt context
  -> LLM gateway generates answer
  -> citation validator checks claims
  -> safety layer checks output
  -> answer, citations, trace, and eval signals are stored
```

### Agent Action Flow

```text
User requests task
  -> agent orchestrator creates run
  -> workflow state machine plans next step
  -> RAG/tool/memory calls run under policy
  -> write action creates approval request
  -> human approves exact tool and arguments
  -> tool executes with idempotency key
  -> verification checks result
  -> audit log and agent eval record are saved
```

### Evaluation Flow

```text
Engineer starts eval
  -> eval dataset selected
  -> runner executes model/RAG/agent path
  -> deterministic scorers run
  -> optional judge model scores outputs
  -> human review handles sampled cases
  -> report compares versions
  -> CI gate passes or blocks release
```

### Fine-Tuning Flow

```text
Approved feedback
  -> dataset promotion
  -> training dataset version
  -> SFT/LoRA/QLoRA run
  -> MLflow metrics and artifact
  -> offline eval
  -> safety regression
  -> serving test
  -> route decision
```

## 10. Public API Surface

| Resource | Operations |
|---|---|
| `/health`, `/ready` | service and dependency health |
| `/auth/session` | current user and tenant context |
| `/tickets` | create, list, read, update tickets |
| `/tickets/{id}/analysis` | run baseline or AI ticket analysis |
| `/tickets/{id}/recommendations` | list AI recommendations |
| `/recommendations/{id}/reviews` | approve, edit, reject recommendations |
| `/documents` | upload, list, read metadata |
| `/documents/{id}/versions` | manage document versions |
| `/search` | semantic and hybrid search |
| `/rag/answer` | answer with citations |
| `/prompts` | list prompt versions and metadata |
| `/models/routes` | inspect model routing |
| `/agents/runs` | start and inspect agent runs |
| `/approvals` | list and decide approval requests |
| `/tools` | list available tools and schemas |
| `/evals/runs` | start evals and read reports |
| `/safety/checks` | run policy and safety checks |
| `/ml/predictions` | classical ML predictions |
| `/voice/sessions` | start voice sessions and inspect transcripts |
| `/metrics/runtime` | Prometheus metrics endpoint |

## 11. Phase-by-Phase Technical Plan

Each phase must end with tests, docs, measurable proof, and a short decision note.

| Phase | Build | Proof |
|---:|---|---|
| 0 | FastAPI, settings, PostgreSQL, Redis, SQLAlchemy, Alembic, auth, ticket CRUD, Docker Compose, CI. | health/ready pass, migrations run, cross-tenant tests pass, CI green. |
| 1 | provider-neutral LLM gateway, mock provider, hosted adapter, routing, streaming, token/cost, retries, fallback. | invalid output rejected, fallback visible, usage attributed, tests avoid paid API. |
| 2 | prompt registry, templates, versions, few-shot examples, prompt tests, untrusted-content boundaries. | every AI run records prompt version, prompt tests pass, injection boundary visible. |
| 3 | structured schemas for classification, extraction, summaries, risk, citations, tool proposals. | invalid JSON blocked, unsafe valid output rejected, schema validity tracked. |
| 4 | upload API, object storage abstraction, PDF/DOCX/HTML/CSV/Excel parsing, OCR path, metadata, document versions, worker jobs. | files ingest, parser errors visible, permissions preserved. |
| 5 | chunking, embedding adapter, pgvector schema, vector CRUD, metadata filters, semantic search. | relevant chunks retrieve, delete propagation works, unauthorized chunks blocked. |
| 6 | hybrid retrieval, reranking, context builder, citation model, answer generation, abstention, classic vs bounded agentic retrieval comparison. | answers cite permitted evidence, missing evidence abstains, retrieval and generation evals separate. |
| 7 | golden/difficult/safety datasets, scorers, LLM judge, human review, reports, CI gates. | bad change can fail a gate, reports compare versions, cost/latency included. |
| 8 | tool registry, schemas, read tools, write proposals, permissions, idempotency, audit, optional MCP boundary. | unknown tools rejected, writes need approval, tool calls traced. |
| 9 | state-machine agent, plan/retrieve/tool/propose/approve/act/verify, budgets, retry/compensation, traces. | unapproved write blocked, limits stop runs, agent eval reports completion and unsafe-action rate. |
| 10 | session memory, durable workflow state, user preferences, retrieval-backed memory, write policy, expiry/correction/deletion. | memory cannot bypass permissions, deletion works, poisoning tests fail safely. |
| 11 | injection checks, jailbreak tests, PII redaction, tenant leak tests, tool abuse tests, threat model, risk register. | direct/indirect injection tests fail safely, security suite runs in CI. |
| 12 | image/document upload, OCR/layout extraction, multimodal adapter, invoice/form extraction, visual evidence refs, review routing. | fields link to source page/region, low-confidence review works, OCR/model evals separate. |
| 13 | STT/TTS adapters, voice sessions, transcript summary, RAG/tool handoff, interruption path, consent policy. | transcript and consent stored, latency measured, human escalation works. |
| 14 | instruction dataset, validation, SFT, LoRA, QLoRA, optional DPO, MLflow, adapter registry, eval comparison. | base vs prompt vs RAG vs adapter report, safety regression passes, config reproducible. |
| 15 | vLLM/SGLang serving, model registry, route canary, hosted-vs-self-hosted cost report, rollback. | p95 latency/throughput/cost reported, rollback shown, quality checked after optimization. |
| 16 | feature pipeline, baseline model, XGBoost/LightGBM, calibration, batch prediction, drift, retraining trigger. | leakage checks pass, model beats baseline, business threshold documented. |
| 17 | similar-ticket search, recommended docs/replies, candidate generation, ranking model, feedback loop. | offline ranking metrics exist, recommendations traceable, feedback stored. |
| 18 | local Compose, staging, secrets, OpenTelemetry, Prometheus, Grafana, load/failure tests, rollback runbook, cloud/K8s path. | fresh clone runs, staging smoke passes, dashboards show AI and runtime metrics. |
| 19 | one end-to-end workflow using auth, ingestion, RAG, LLM, tools, agent, safety, evals, monitoring, approval. | demo works and links answer/action to prompt, model, retrieval, tool, approval, eval, cost, trace. |

## 12. Testing Strategy

| Test Type | What It Proves |
|---|---|
| Unit tests | schemas, business logic, prompts, scorers, chunking. |
| Integration tests | API + DB + Redis + gateway + RAG + tools. |
| Contract tests | provider adapters, tool schemas, API responses. |
| Prompt tests | prompt versions do not regress golden cases. |
| RAG tests | retrieval, citations, permissions, abstention. |
| Agent tests | workflow steps, approval, limits, rollback, memory. |
| Safety tests | injection, jailbreak, PII, tenant leaks, tool abuse. |
| Eval tests | scoring correctness and CI gate behavior. |
| Load tests | latency, throughput, queue behavior, token/cost growth. |
| Deployment tests | Docker Compose config, health, readiness, smoke tests. |

## 13. Observability and Cost

Every AI run records:

- tenant, user, feature;
- prompt version;
- model provider and model name/version;
- input tokens, output tokens, estimated cost;
- latency and trace ID;
- retrieval IDs, citation IDs, tool-call IDs, approval IDs;
- safety results;
- eval dataset version when applicable.

Dashboards show:

- request rate, error rate, p50/p95 latency;
- token usage and cost by tenant/feature;
- validation failure rate and fallback rate;
- retrieval quality and citation accuracy;
- agent task completion and unsafe-action attempts;
- human approval acceptance rate;
- eval regression status.

## 14. Deployment Plan

Local:

- Docker Compose runs API, worker, PostgreSQL, Redis, Prometheus, Grafana, optional MLflow.
- Mock model provider is default.
- Real provider keys are optional and loaded from environment.

Staging:

- same containers with staging settings;
- real provider sandbox or controlled tenant;
- seeded demo data;
- smoke tests and eval gates before release.

Production path:

- one cloud provider first;
- managed PostgreSQL, managed Redis, object storage;
- container deployment first, Kubernetes after local/staging maturity;
- Terraform for infrastructure;
- OpenTelemetry collector;
- canary release and rollback.

## 15. Completion Standard

Atlas is complete only when:

- every phase has working code;
- every AI feature has tests and eval evidence;
- every consequential action requires approval;
- every RAG answer has citations or abstention behavior;
- every model/prompt/retrieval/tool/agent change is traceable;
- safety tests run in CI;
- cost and latency are measured;
- deployment and rollback are documented;
- one capstone workflow can be demonstrated from UI to database, AI trace, approval, evaluation, monitoring, and rollback evidence.
