# Atlas AI Platform - Technical Master Blueprint

## 1. Document Purpose

This document is the complete technical implementation blueprint for the Atlas AI Platform.

The purpose is to define the full system before coding starts. A developer should be able to read this document and understand:

- What the platform is supposed to do.
- Why each subsystem exists.
- Where every subsystem fits in the architecture.
- Which modules, services, APIs, database tables, background jobs, and AI pipelines are required.
- How requests move through the system.
- How the LLM is controlled by the application.
- How RAG, agents, tools, memory, safety, evaluation, fine-tuning, model serving, multimodal AI, voice AI, classical ML, and production operations fit together.
- How to build the system phase by phase without guessing the design.

This is not a code file. It is the engineering design document that should guide implementation.

The separate learning phase documents will explain each phase as a lesson. This file focuses on the system architecture and implementation plan.

## 2. Core Product Definition

### 2.1 Project Name

Atlas AI Platform.

### 2.2 Product Type

Atlas is an enterprise Generative AI platform for support, operations, document intelligence, knowledge search, agentic workflows, evaluation, safety, and production AI operations.

It is designed as one complete project that proves practical AI engineering skill across the full Gen AI job market.

### 2.3 Main Business Problem

Companies have private knowledge, tickets, documents, policies, customer conversations, operational workflows, and internal systems. Employees need AI assistance, but the AI must be accurate, auditable, safe, permission-aware, and measurable.

A simple chatbot is not enough because real companies need:

- Private document search.
- Answers with citations.
- Structured extraction.
- Workflow automation.
- Human approval for risky actions.
- Audit logs.
- Evaluation datasets.
- Safety controls.
- Cost and latency tracking.
- Multi-tenant security.
- Deployment and monitoring.
- Model/provider flexibility.

Atlas solves this by combining backend engineering, data engineering, Gen AI pipelines, agent orchestration, evaluation, safety, and production operations into one controlled platform.

### 2.4 Target Users

Primary user types:

- Support agent: asks questions, summarizes tickets, drafts responses, reviews customer history.
- Operations analyst: uploads documents, searches policies, runs workflow automation, reviews AI suggestions.
- Team lead: reviews quality, cost, feedback, escalations, and agent performance.
- Admin: manages users, tenants, policies, prompts, tools, model settings, and approvals.
- AI engineer: manages prompts, datasets, evaluations, experiments, model routing, fine-tuning, and deployments.
- Compliance reviewer: audits tool calls, safety decisions, approvals, and generated outputs.

### 2.5 Core User Workflows

Atlas must support these user-facing workflows:

1. User signs in and belongs to a tenant.
2. User uploads documents into a workspace.
3. System extracts, cleans, chunks, embeds, and indexes documents.
4. User asks a question over tenant knowledge.
5. System retrieves relevant chunks and reranks them.
6. System builds grounded context and calls an LLM.
7. System returns an answer with citations, confidence, and source references.
8. User gives feedback on the answer.
9. Admin reviews answer quality and evaluation results.
10. User asks an agent to perform a task.
11. Agent plans the task, retrieves context, requests tools, and validates outputs.
12. Risky actions require human approval.
13. System logs all model calls, tool calls, safety checks, costs, and traces.
14. AI engineer runs offline evaluations and compares prompt/model versions.
15. AI engineer prepares fine-tuning datasets if prompting or RAG are not enough.
16. Operations team deploys and monitors the system.

### 2.6 Corrected Gen AI Scope

The original Atlas scope was strongest in enterprise LLM application engineering. That includes LLM gateway design, prompt systems, structured outputs, RAG, agents, tool calling, evaluation, safety, fine-tuning, model serving, and LLMOps.

However, Generative AI is broader than LLM applications. A complete Gen AI roadmap must also acknowledge and place these capabilities:

- Text generation with LLMs.
- Code generation with LLMs.
- Image generation with diffusion or image generation APIs.
- Image editing, inpainting, outpainting, and variation generation.
- Video generation and video editing.
- Audio generation and music generation.
- Speech generation and real-time speech-to-speech.
- Multimodal understanding across text, image, audio, and video.
- Synthetic data generation.
- Evaluation and safety for generated media.
- Model serving, caching, routing, and governance across all generated content types.

Atlas should therefore describe itself as:

```text
an enterprise Gen AI engineering platform centered on LLM applications, RAG, agents, safety, evaluation, and production AI operations, with optional generative media tracks for image, audio, and video generation.
```

The project does not need to train a frontier image, video, or audio foundation model from scratch. That would be research-lab scope. It should, however, teach how generated media systems are designed, integrated, evaluated, governed, and deployed in real products.

### 2.7 Minimum Viable Spine

The full Atlas platform is intentionally broad. To make it buildable, the project must have a minimum viable spine.

The minimum viable spine is the smallest complete end-to-end system that proves real Gen AI engineering.

MVP spine:

```text
dev auth or simple auth
-> tenant/workspace context
-> document upload
-> ingestion job
-> text extraction
-> chunking
-> embedding generation
-> vector storage
-> RAG query
-> reranking optional for MVP+
-> grounded answer with citations
-> AI run logging
-> token/cost/latency tracking
-> user feedback
-> small evaluation dataset
-> local Docker Compose run
```

MVP phases:

```text
Phase 00: Engineering foundation
Phase 01: LLM gateway
Phase 02: Prompt system
Phase 03: Structured outputs
Phase 04: Document ingestion
Phase 05: Embeddings and vector database
Phase 06: RAG, reranking, citations
Phase 07: Evaluation platform light version
Phase 18: Deployment/monitoring light version
```

MVP success demo:

```text
1. Start system locally.
2. Upload a policy PDF.
3. Watch ingestion status move from queued to processed.
4. Inspect extracted chunks.
5. Ask a question over the document.
6. Receive an answer with citations.
7. Open retrieval trace and AI run metadata.
8. See model, prompt version, token usage, cost, latency, retrieved chunks, and answer feedback.
9. Run an evaluation suite with 10 to 25 examples.
10. Compare a baseline prompt against an improved prompt.
```

This MVP alone is enough for a serious backend-plus-GenAI portfolio piece if built cleanly.

### 2.8 Job-Ready Stopping Points

The platform should define stopping points so a learner does not get stuck trying to finish every advanced topic before applying for jobs.

#### Stopping Point A: Backend LLM Application Engineer

Scope:

```text
Phases 00 to 07 plus light deployment from Phase 18
```

What it proves:

- Python backend engineering.
- FastAPI APIs.
- SQL database design.
- LLM provider abstraction.
- Prompt versioning.
- Structured outputs.
- Document ingestion.
- Embeddings.
- Vector search.
- RAG with citations.
- Basic evaluation.
- Cost and latency logging.

#### Stopping Point B: RAG Engineer

Scope:

```text
Phases 00 to 07 plus advanced RAG parts from Phase 23
```

What it proves:

- Chunking strategies.
- Embedding model selection.
- Hybrid search.
- Reranking.
- Query rewrite.
- Parent-child retrieval.
- Contextual retrieval.
- Multi-hop retrieval.
- Citation verification.
- Retrieval evaluation.
- ACL-filtered retrieval.

#### Stopping Point C: Agentic AI Engineer

Scope:

```text
Phases 00 to 11 plus Phase 21 MCP and Phase 22 multi-agent orchestration
```

What it proves:

- Tool calling.
- Agent state machines.
- Human approvals.
- Memory.
- MCP integration.
- Scoped tool credentials.
- Agent identity.
- Multi-agent supervisor/worker design.
- Prompt-injection defense.
- Agent audit traces.

#### Stopping Point D: Production AI Platform Engineer

Scope:

```text
Phases 00 to 11 plus Phase 18 and Phase 25 governance
```

What it proves:

- SLOs.
- Observability.
- AI run traces.
- Cost controls.
- Safety controls.
- Risk register.
- Incident response.
- CI/CD.
- Deployment and rollback.
- Governance artifacts.

#### Stopping Point E: Full Gen AI Platform Engineer

Scope:

```text
Phases 00 to 25
```

What it proves:

- Enterprise LLM systems.
- RAG.
- Agents.
- MCP.
- Advanced retrieval.
- Model adaptation.
- Model serving.
- Multimodal understanding.
- Voice.
- Generative media.
- Governance.
- Production readiness.

### 2.9 Effort Reality

A full platform with backend, frontend, RAG, agents, evaluation, safety, model adaptation, serving, multimodal, voice, generative media, governance, and deployment is large.

Realistic solo estimates:

```text
MVP spine: 6 to 10 weeks part-time, 3 to 5 weeks full-time
Agentic version: 3 to 5 months part-time, 8 to 12 weeks full-time
Production platform version: 6 to 9 months part-time, 4 to 6 months full-time
Full 25-phase advanced version: 12 to 24 months part-time, 8 to 14 months full-time
```

These estimates assume real tests, documentation, database migrations, working APIs, and demos. A shallow demo can be built faster, but it will not prove the same industry skill.

### 2.10 Required, Advanced, And Optional Scope Labels

Every phase should carry a scope label.

Scope labels:

```text
Required MVP
Required portfolio
Required production
Advanced depth
Optional breadth
Research depth
```

Recommended labels:

```text
Phase 00 Foundation: Required MVP
Phase 01 LLM Gateway: Required MVP
Phase 02 Prompt System: Required MVP
Phase 03 Structured Outputs: Required MVP
Phase 04 Document Ingestion: Required MVP
Phase 05 Embeddings and Vector DB: Required MVP
Phase 06 RAG: Required MVP
Phase 07 Evaluation: Required portfolio
Phase 08 Tool Calling: Required agent portfolio
Phase 09 Controlled Agents: Required agent portfolio
Phase 10 Agent Memory: Advanced depth
Phase 11 Safety and Guardrails: Required production
Phase 12 Multimodal Understanding: Advanced depth
Phase 13 Voice AI: Advanced depth
Phase 14 Fine-Tuning and Adaptation: Optional advanced depth
Phase 15 Model Serving and LLMOps: Optional advanced depth
Phase 16 Classical ML: Optional breadth
Phase 17 Search and Ranking: Required advanced RAG
Phase 18 Deployment and Monitoring: Required production
Phase 19 Capstone Integration: Required portfolio
Phase 20 LLM Optimization and Caching: Required production
Phase 21 MCP and External Tool Ecosystem: Required agent portfolio
Phase 22 Multi-Agent Orchestration: Advanced depth
Phase 23 Advanced RAG and Retrieval Systems: Advanced depth
Phase 24 Generative Media: Optional Gen AI completeness
Phase 25 Governance, Compliance, and Risk Management: Required enterprise maturity
```

## 3. Engineering Principles

### 3.1 Application Owns The System

The most important rule:

The application owns the system. The LLM does not own the system.

The LLM can reason, summarize, classify, extract, draft, rank, and suggest. It must not independently own:

- Authentication.
- Authorization.
- Tool permissions.
- Database writes.
- Business rule decisions.
- Safety policy enforcement.
- Memory persistence.
- Evaluation scoring.
- Deployment routing.
- Cost limits.
- Audit history.

Every LLM action must pass through controlled application code.

### 3.2 Modular Monolith First

The first implementation should be a modular monolith.

Reason:

- Easier local development.
- Easier debugging.
- Lower infrastructure complexity.
- Clear code boundaries without premature distributed systems complexity.
- Easier learning path.

The architecture must still use service-ready module boundaries so that later these modules can become separate services if needed.

Initial deployment:

```text
web app + api app + worker app + postgres + redis + vector database + object storage
```

Later scalable deployment:

```text
web service
api service
worker service
ingestion workers
evaluation workers
model gateway service
agent service
model serving service
observability stack
```

### 3.3 AI Features Must Be Measurable

No AI capability is complete unless it can be measured.

For every AI workflow, store:

- Input.
- Prompt version.
- Model used.
- Retrieved context.
- Output.
- Token usage.
- Cost.
- Latency.
- Safety checks.
- Tool calls.
- Evaluation score when available.
- User feedback when available.

### 3.4 Prefer Explicit State Over Hidden Magic

Agent workflows, ingestion workflows, evaluation workflows, and tool workflows must use explicit states.

Bad design:

```text
User asks model -> model does everything -> response returned
```

Good design:

```text
User request
-> classify intent
-> check permissions
-> retrieve context
-> create plan
-> validate plan
-> call approved tools
-> verify results
-> run safety checks
-> produce final answer
-> log trace
-> store evaluation hooks
```

### 3.5 Design For Multi-Tenancy From The Start

Every user-visible object must belong to a tenant or workspace.

This includes:

- Documents.
- Chunks.
- Embeddings.
- Conversations.
- AI runs.
- Tool calls.
- Evaluation datasets.
- Prompts.
- Safety policies.
- Memory items.
- Files.
- Audit logs.

Every query must enforce tenant boundaries.

### 3.6 Separate Online Runtime From Offline Experimentation

Online runtime handles real user requests.

Offline experimentation handles:

- Prompt tests.
- Batch evaluations.
- Fine-tuning data preparation.
- Model comparisons.
- Retrieval experiments.
- Safety red-team tests.

The same database can store results, but online paths must stay fast and reliable.

## 4. High-Level Architecture

### 4.1 Architecture Diagram

```text
Browser / Web Console
  |
  v
API Service - FastAPI
  |
  |-- Auth and RBAC
  |-- Request validation
  |-- Tenant isolation
  |-- Rate limits
  |-- API contracts
  |
  |---> Model Gateway
  |       |-- Provider adapters
  |       |-- Model routing
  |       |-- Token and cost tracking
  |       |-- Retries and timeouts
  |       |-- Structured output enforcement
  |
  |---> Prompt Service
  |       |-- Prompt templates
  |       |-- Prompt versions
  |       |-- Prompt test cases
  |       |-- Prompt release metadata
  |
  |---> RAG Service
  |       |-- Query rewriting
  |       |-- Retrieval
  |       |-- Reranking
  |       |-- Context packing
  |       |-- Citation generation
  |       |-- Grounded answer generation
  |
  |---> Agent Orchestrator
  |       |-- State machine
  |       |-- Planning
  |       |-- Tool selection
  |       |-- Tool execution requests
  |       |-- Verification
  |       |-- Human approval gates
  |
  |---> Tool Service
  |       |-- Typed tool registry
  |       |-- Permission checks
  |       |-- Dry-run execution
  |       |-- Write action approval
  |       |-- Audit trail
  |
  |---> Safety Service
  |       |-- Input checks
  |       |-- Prompt injection detection
  |       |-- PII handling
  |       |-- Output checks
  |       |-- Policy enforcement
  |
  |---> Evaluation Service
  |       |-- Golden datasets
  |       |-- Regression runs
  |       |-- LLM-as-judge
  |       |-- Retrieval metrics
  |       |-- Human feedback
  |
  |---> Worker Service
          |-- Document ingestion
          |-- OCR and parsing
          |-- Embedding jobs
          |-- Batch evaluations
          |-- Fine-tuning jobs
          |-- Long-running agent tasks

Storage Layer
  |-- PostgreSQL for relational data
  |-- pgvector or Qdrant for vectors
  |-- Redis for cache and queues
  |-- Object storage for documents and artifacts
  |-- Metrics/logs/traces backend
```

### 4.2 Main Runtime Applications

The implementation should have separate runnable applications even if they share packages.

```text
apps/api
apps/worker
apps/web
apps/eval-runner
apps/model-server
```

#### apps/api

Responsible for:

- HTTP APIs.
- Authentication entry points.
- Tenant and role enforcement.
- Calling internal services.
- Returning validated responses.
- Request-level logging and tracing.
- Synchronous AI flows that can complete quickly.

It should not do heavy parsing, OCR, batch evaluations, or model training directly.

#### apps/worker

Responsible for:

- Background jobs.
- Document processing.
- Embedding generation.
- Long-running evaluations.
- Dataset processing.
- Fine-tuning job orchestration.
- Cleanup and scheduled tasks.

The worker should consume jobs from Redis-backed queues or another queue system.

#### apps/web

Responsible for:

- Chat UI.
- Document management.
- Agent run viewer.
- Evaluation dashboard.
- Prompt management UI.
- Admin settings.
- Approval queue.
- Cost and latency views.

The web app calls the API only. It does not call LLM providers directly.

#### apps/eval-runner

Responsible for:

- Running offline evaluation suites.
- Comparing prompt versions.
- Comparing model versions.
- Comparing retrieval strategies.
- Exporting reports.

This can start as a CLI and later become a scheduled service.

#### apps/model-server

Responsible for:

- Serving local or fine-tuned open models when needed.
- Exposing an internal inference API.
- Supporting batching where possible.
- Supporting versioned model deployment.

This phase appears later. The first version can use managed providers through the model gateway.

## 5. Repository Structure

The codebase should be organized by application entry points and reusable domain packages.

Recommended structure:

```text
atlas-ai-platform/
  README.md
  pyproject.toml
  docker-compose.yml
  .env.example
  .gitignore

  apps/
    api/
      main.py
      routes/
      dependencies/
      middleware/
      schemas/
      lifespan.py

    worker/
      main.py
      jobs/
      schedules/

    eval_runner/
      main.py
      commands/
      reports/

    model_server/
      main.py
      adapters/

    web/
      package.json
      src/
        app/
        components/
        features/
        lib/
        styles/

  packages/
    core/
      config.py
      errors.py
      logging.py
      time.py
      ids.py
      pagination.py
      result.py

    db/
      session.py
      base.py
      migrations/
      repositories/
      models/

    auth/
      users.py
      tenants.py
      roles.py
      permissions.py
      api_keys.py

    model_gateway/
      client.py
      router.py
      providers/
      token_usage.py
      cost.py
      retries.py
      streaming.py
      structured.py
      cache.py

    prompts/
      templates.py
      registry.py
      renderer.py
      versions.py
      tests.py

    ingestion/
      upload.py
      extraction.py
      ocr.py
      cleaning.py
      chunking.py
      metadata.py
      pipeline.py

    retrieval/
      embeddings.py
      vector_store.py
      hybrid_search.py
      reranking.py
      context_packing.py
      citations.py

    rag/
      query_understanding.py
      answer_generation.py
      grounding.py
      response_builder.py

    agents/
      state.py
      planner.py
      executor.py
      policies.py
      approvals.py
      traces.py
      verifier.py

    tools/
      registry.py
      schemas.py
      permissions.py
      executor.py
      builtins/

    memory/
      session_memory.py
      long_term_memory.py
      summarization.py
      retention.py

    safety/
      policies.py
      input_checks.py
      output_checks.py
      prompt_injection.py
      pii.py
      moderation.py
      approval_rules.py

    evals/
      datasets.py
      runners.py
      scorers.py
      retrieval_metrics.py
      judge.py
      reports.py
      regression.py

    ml/
      features.py
      classical_models.py
      training.py
      inference.py
      registry.py

    adaptation/
      datasets.py
      sft.py
      lora.py
      qlora.py
      preference.py
      export.py

    serving/
      registry.py
      deployments.py
      health.py
      routing.py

    multimodal/
      image_input.py
      document_vision.py
      ocr_validation.py
      visual_evidence.py

    voice/
      transcription.py
      synthesis.py
      diarization.py
      call_summary.py
      escalation.py

    observability/
      traces.py
      metrics.py
      audit.py
      costs.py
      dashboards.py

    integrations/
      crm.py
      ticketing.py
      email.py
      storage.py
      webhooks.py

  tests/
    unit/
    integration/
    contract/
    evals/
    security/
    load/

  infra/
    docker/
    k8s/
    terraform/
    monitoring/
    ci/

  docs/
    architecture/
    api/
    runbooks/
    decisions/
```

### 5.1 Ownership Rules

Each package should have a clear responsibility.

- `core` owns shared primitives only.
- `db` owns persistence infrastructure and repository patterns.
- `auth` owns identity, tenants, roles, and permissions.
- `model_gateway` owns all model provider communication.
- `prompts` owns prompt templates and versions.
- `ingestion` owns turning files into clean text and metadata.
- `retrieval` owns embeddings, search, reranking, and context packing.
- `rag` owns grounded answer workflows.
- `agents` owns stateful multi-step AI workflows.
- `tools` owns executable actions and tool schemas.
- `memory` owns conversation and long-term memory rules.
- `safety` owns AI risk checks and policy enforcement.
- `evals` owns quality measurement.
- `adaptation` owns fine-tuning workflows.
- `serving` owns model deployment metadata and inference routing.
- `multimodal` owns image/document-vision flows.
- `voice` owns speech workflows.
- `observability` owns traces, metrics, audit, and cost records.
- `integrations` owns external business systems.

No package should secretly call an LLM provider directly. All model calls must go through `model_gateway`.

## 6. Technology Stack

### 6.1 Backend Stack

Primary backend language:

- Python.

Core Python tools:

- FastAPI for HTTP APIs.
- Pydantic for request, response, settings, and structured AI output validation.
- SQLAlchemy for ORM and database access.
- Alembic for database migrations.
- PostgreSQL for relational storage.
- pgvector or Qdrant for vector search.
- Redis for caching, rate limits, queues, and transient state.
- Celery, RQ, or Arq for workers.
- httpx for outbound HTTP calls.
- tenacity for retry policies.
- structlog or standard logging with JSON format.
- pytest for tests.
- pytest-asyncio for async tests.
- ruff for linting.
- mypy or pyright for typing.

### 6.2 AI Stack

Managed model providers:

- OpenAI-compatible chat and embedding APIs.
- Anthropic-compatible chat APIs if required.
- Azure OpenAI if enterprise deployment requires it.

Open model tooling:

- Hugging Face Transformers.
- Sentence Transformers.
- PyTorch.
- PEFT for LoRA/QLoRA.
- bitsandbytes where supported for quantized fine-tuning.
- vLLM or Text Generation Inference for serving.
- MLflow for experiments and model registry.

RAG tooling:

- pgvector for simple Postgres-native vector search, or Qdrant for dedicated vector database behavior.
- BM25 or Postgres full-text search for keyword retrieval.
- Reranking model or reranking API.
- Custom context packing logic.

Agent tooling:

- LangGraph for graph/state-machine based agent orchestration, or a custom state machine if strict control is preferred.
- Pydantic schemas for tool inputs and outputs.
- Internal tool registry.

Evaluation tooling:

- pytest-based regression tests.
- Custom retrieval metrics.
- LLM-as-judge for qualitative scoring.
- Human feedback tables.
- MLflow or stored eval reports for experiment comparison.

### 6.3 Frontend Stack

Recommended frontend:

- React or Next.js.
- TypeScript.
- TanStack Query for server-state management.
- Zod for client-side schema validation if TypeScript is used.
- A restrained component system for dashboard UX.

Frontend pages:

- Login and workspace selection.
- Chat and RAG assistant.
- Document library.
- Document ingestion status.
- Agent tasks.
- Agent run trace viewer.
- Tool call approval queue.
- Prompt management.
- Evaluation dashboard.
- Model and cost dashboard.
- Safety review dashboard.
- Admin settings.

### 6.4 Infrastructure Stack

Local development:

- Docker Compose.
- Local Postgres.
- Local Redis.
- Local vector store.
- Local object storage emulator if needed.

Production path:

- Containerized apps.
- Managed Postgres.
- Managed Redis.
- Managed object storage.
- Managed or self-hosted vector store.
- CI/CD pipeline.
- Staging environment.
- Production environment.
- OpenTelemetry traces.
- Metrics and logs dashboard.
- Alerting.

## 7. Runtime Environments

### 7.1 Local Environment

Local environment should allow one developer to run the core system.

Required services:

```text
api
worker
web
postgres
redis
vector database
object storage emulator optional
```

Local goals:

- Upload sample documents.
- Run ingestion.
- Generate embeddings.
- Ask RAG questions.
- Run prompt tests.
- Run agent tool calls in dry-run mode.
- View logs and traces.

### 7.2 Test Environment

Test environment should run automatically in CI.

Required behavior:

- Unit tests run without external model calls by using fake providers.
- Integration tests can run against local containers.
- AI eval tests should run in controlled mode with fixed datasets.
- Expensive provider tests should be opt-in.

### 7.3 Staging Environment

Staging should mirror production as closely as possible.

Required behavior:

- Real auth.
- Real database migrations.
- Real queues.
- Real model gateway configuration.
- Limited model budget.
- Test tenant data.
- Full observability.
- Deployment rollback practice.

### 7.4 Production Environment

Production should require:

- Managed secrets.
- Proper network controls.
- Backups.
- Alerts.
- Audit logs.
- Rate limits.
- Cost budgets.
- Human approval controls.
- Incident runbooks.

## 8. Configuration And Secrets

Configuration should use environment variables loaded into typed settings.

Example configuration groups:

```text
APP_ENV
APP_NAME
LOG_LEVEL
DATABASE_URL
REDIS_URL
VECTOR_STORE_URL
OBJECT_STORAGE_ENDPOINT
OBJECT_STORAGE_BUCKET
JWT_SECRET
ENCRYPTION_KEY
OPENAI_API_KEY
ANTHROPIC_API_KEY
DEFAULT_CHAT_MODEL
DEFAULT_EMBEDDING_MODEL
MAX_INPUT_TOKENS
MAX_OUTPUT_TOKENS
REQUEST_TIMEOUT_SECONDS
DAILY_MODEL_COST_LIMIT
ENABLE_FINE_TUNING
ENABLE_LOCAL_MODEL_SERVER
```

Rules:

- Never hard-code secrets.
- Never expose provider keys to frontend code.
- Validate config at startup.
- Fail fast if required config is missing.
- Use separate config for local, test, staging, and production.
- Keep `.env.example` complete but without secrets.

## 9. Request Lifecycle Standards

Every API request should follow this general lifecycle:

```text
HTTP request
-> request id assigned
-> auth checked
-> tenant resolved
-> permissions checked
-> request schema validated
-> service method called
-> database transaction opened when needed
-> domain logic executed
-> AI call routed through model gateway when needed
-> safety checks applied when needed
-> response schema validated
-> audit and metrics recorded
-> response returned
```

For AI requests, add:

```text
AI request
-> prompt version resolved
-> model route selected
-> input safety checked
-> model request created
-> provider called through gateway
-> output parsed and validated
-> repair or retry attempted if allowed
-> output safety checked
-> run record stored
-> cost and latency stored
-> response returned
```

## 10. Domain Boundaries

### 10.1 Identity Domain

Owns:

- Users.
- Tenants.
- Workspaces.
- Memberships.
- Roles.
- Permissions.
- API keys.
- Sessions.

Must answer:

- Who is the user?
- Which tenant are they acting in?
- What are they allowed to do?
- Are they allowed to see this document, run this agent, call this tool, or approve this action?

### 10.2 Knowledge Domain

Owns:

- Documents.
- Versions.
- Extracted text.
- Chunks.
- Metadata.
- Embeddings.
- Source references.
- Knowledge collections.

Must answer:

- What private knowledge exists?
- Where did it come from?
- What text was extracted?
- Which chunks are searchable?
- Which user or tenant can access them?

### 10.3 Conversation Domain

Owns:

- Chat sessions.
- Messages.
- AI responses.
- Citations.
- User feedback.
- Conversation-level memory.

Must answer:

- What did the user ask?
- What did the AI answer?
- Which sources supported the answer?
- Was the answer useful?

### 10.4 AI Operations Domain

Owns:

- Model providers.
- Model routes.
- AI runs.
- Token usage.
- Costs.
- Latency.
- Prompt versions.
- Structured output schemas.

Must answer:

- Which model produced this output?
- What prompt version was used?
- How much did it cost?
- How long did it take?
- Did the output validate?

### 10.5 Agent Domain

Owns:

- Agent definitions.
- Agent runs.
- Agent steps.
- Plans.
- Tool calls.
- Verification results.
- Approvals.

Must answer:

- What task did the agent try to complete?
- What steps did it take?
- Which tools did it request?
- Which actions were approved?
- What was the final result?

### 10.6 Evaluation Domain

Owns:

- Evaluation datasets.
- Test cases.
- Evaluation runs.
- Scores.
- Judge results.
- Retrieval metrics.
- Regression reports.

Must answer:

- Is the system improving?
- Did a prompt/model/retrieval change break behavior?
- Which examples are failing?
- Why are they failing?

### 10.7 Safety Domain

Owns:

- Policies.
- Safety checks.
- Prompt injection checks.
- PII handling.
- Approval rules.
- Risk scoring.
- Red-team tests.

Must answer:

- Is the input safe?
- Is the retrieved context suspicious?
- Is the output allowed?
- Does an action need approval?
- Was sensitive data exposed?

### 10.8 Model Adaptation Domain

Owns:

- Training datasets.
- Fine-tuning jobs.
- Adapter models.
- Model experiments.
- Model registry entries.
- Deployment candidates.

Must answer:

- Is fine-tuning actually needed?
- Which dataset was used?
- Which model version was produced?
- Did it beat the baseline?
- Is it safe to deploy?


## 11. Database Architecture

The database should be designed as a system of records for business entities, AI activity, evaluations, safety decisions, and audit history.

PostgreSQL is the primary relational database. Vector data can live in pgvector for a simpler first version or in Qdrant if a dedicated vector store is preferred. If Qdrant is used, PostgreSQL still stores the relational metadata and vector ids.

### 11.1 Database Design Rules

Rules:

- Every tenant-owned table includes `tenant_id`.
- Every important table includes `created_at` and `updated_at`.
- User actions include `created_by_user_id` where possible.
- AI-generated records include model, prompt, and run references.
- Destructive operations should prefer soft delete where audit matters.
- Large binary files do not belong in PostgreSQL; store them in object storage and save references.
- Embeddings should be versioned by embedding model and chunk version.
- Evaluation results must reference the exact prompt, model, retriever, and dataset version.
- Tool calls must be auditable and replayable where safe.

### 11.2 Identity Tables

#### tenants

Purpose: company/account boundary.

Fields:

```text
id
name
slug
status
plan_name
created_at
updated_at
```

Important behavior:

- All business data belongs to a tenant.
- Tenant status can disable access.
- Tenant-level limits can control storage, users, model cost, and agent capabilities.

#### users

Purpose: human identity.

Fields:

```text
id
email
name
status
password_hash or external_auth_subject
last_login_at
created_at
updated_at
```

Important behavior:

- User identity is global.
- User access to tenant data is through membership.

#### tenant_memberships

Purpose: connects users to tenants.

Fields:

```text
id
tenant_id
user_id
role_id
status
created_at
updated_at
```

Important behavior:

- A user can belong to multiple tenants.
- Every request must resolve active tenant membership.

#### roles

Purpose: named permission groups.

Fields:

```text
id
tenant_id nullable for system roles
name
description
created_at
updated_at
```

Example roles:

- admin.
- ai_engineer.
- support_agent.
- reviewer.
- viewer.

#### permissions

Purpose: atomic permissions.

Fields:

```text
id
code
description
```

Example permissions:

```text
documents.read
documents.write
documents.delete
rag.query
agents.run
agents.approve_action
tools.execute_read
tools.execute_write
prompts.manage
evals.run
models.manage
safety.manage
admin.manage_users
```

#### role_permissions

Purpose: maps roles to permissions.

Fields:

```text
role_id
permission_id
```

#### api_keys

Purpose: programmatic access.

Fields:

```text
id
tenant_id
name
key_hash
scopes
status
last_used_at
created_by_user_id
created_at
expires_at
```

Important behavior:

- Store only a hash of the key.
- Keys must have scopes.
- Keys should be revocable.

### 11.3 Knowledge And Document Tables

#### knowledge_collections

Purpose: group documents by workspace, department, use case, or access policy.

Fields:

```text
id
tenant_id
name
description
visibility
metadata_json
created_by_user_id
created_at
updated_at
```

Examples:

- Support policies.
- Product manuals.
- Legal contracts.
- Internal SOPs.

#### documents

Purpose: uploaded or connected source document.

Fields:

```text
id
tenant_id
collection_id
title
source_type
source_uri
file_object_key
mime_type
status
checksum
metadata_json
created_by_user_id
created_at
updated_at
deleted_at
```

Statuses:

```text
uploaded
queued
processing
processed
failed
archived
```

#### document_versions

Purpose: preserve changes when a document is replaced or reprocessed.

Fields:

```text
id
document_id
tenant_id
version_number
file_object_key
checksum
parser_name
parser_version
status
created_at
```

#### document_pages

Purpose: page-level extracted text and metadata.

Fields:

```text
id
tenant_id
document_id
document_version_id
page_number
text
layout_json
ocr_confidence
image_object_key
created_at
```

#### document_chunks

Purpose: searchable text units.

Fields:

```text
id
tenant_id
document_id
document_version_id
page_start
page_end
chunk_index
text
normalized_text
token_count
metadata_json
content_hash
created_at
```

Important behavior:

- Chunk ids must be stable enough for citations.
- Store token count for context packing.
- Keep metadata for filters.

#### chunk_embeddings

Purpose: vector representation of chunks.

Fields if using pgvector:

```text
id
tenant_id
chunk_id
embedding_model
embedding_dimension
embedding vector
content_hash
created_at
```

Fields if using Qdrant:

```text
id
tenant_id
chunk_id
vector_store_name
vector_point_id
embedding_model
embedding_dimension
content_hash
created_at
```

Important behavior:

- Embeddings must be regenerated when chunk text or embedding model changes.
- Index by tenant, model, and vector.

#### ingestion_jobs

Purpose: background processing state.

Fields:

```text
id
tenant_id
document_id
document_version_id
job_type
status
attempt_count
error_message
started_at
finished_at
created_at
updated_at
```

Job types:

```text
extract_text
ocr
clean_text
chunk
embed
index
full_ingestion
```

### 11.4 Conversation And RAG Tables

#### conversations

Purpose: chat session container.

Fields:

```text
id
tenant_id
user_id
title
mode
created_at
updated_at
archived_at
```

Modes:

```text
chat
rag
agent
voice
multimodal
```

#### conversation_messages

Purpose: message history.

Fields:

```text
id
tenant_id
conversation_id
role
content
content_json
created_at
```

Roles:

```text
user
assistant
system
tool
approval
```

#### rag_queries

Purpose: stores RAG request metadata.

Fields:

```text
id
tenant_id
conversation_id
user_id
query_text
rewritten_query
retrieval_strategy
collection_ids
filters_json
created_at
```

#### rag_retrieval_results

Purpose: stores retrieved chunks before and after reranking.

Fields:

```text
id
tenant_id
rag_query_id
chunk_id
rank_initial
rank_final
score_initial
score_final
retriever_name
reranker_name
included_in_context
created_at
```

#### rag_answers

Purpose: final answer and citation metadata.

Fields:

```text
id
tenant_id
rag_query_id
ai_run_id
answer_text
answer_json
confidence_label
citation_count
groundedness_score
created_at
```

#### answer_citations

Purpose: citation spans or source references.

Fields:

```text
id
tenant_id
rag_answer_id
chunk_id
document_id
page_start
page_end
quote_or_summary
support_type
created_at
```

Support types:

```text
supports_claim
partial_support
background
conflict
```

### 11.5 Prompt And Model Tables

#### prompt_templates

Purpose: named prompt asset.

Fields:

```text
id
tenant_id nullable
name
use_case
description
owner_user_id
status
created_at
updated_at
```

#### prompt_versions

Purpose: versioned prompt text.

Fields:

```text
id
prompt_template_id
version_number
system_prompt
user_template
developer_notes
input_variables_json
output_schema_json
model_defaults_json
status
created_at
created_by_user_id
```

Statuses:

```text
draft
testing
approved
active
retired
```

#### prompt_test_cases

Purpose: examples used to test prompts.

Fields:

```text
id
tenant_id
prompt_template_id
name
input_json
expected_behavior
expected_output_json
created_at
```

#### model_providers

Purpose: provider configuration metadata.

Fields:

```text
id
name
provider_type
base_url
status
created_at
updated_at
```

Provider types:

```text
openai_compatible
anthropic_compatible
azure_openai
local_vllm
local_tgi
mock
```

#### model_routes

Purpose: routing rules from use case to model.

Fields:

```text
id
tenant_id nullable
use_case
provider_id
model_name
priority
max_input_tokens
max_output_tokens
temperature
timeout_seconds
fallback_route_id
status
created_at
updated_at
```

Use cases:

```text
chat
rag_answer
query_rewrite
structured_extraction
classification
agent_planning
agent_verification
summarization
embedding
reranking
safety_check
llm_judge
```

#### ai_runs

Purpose: every model call.

Fields:

```text
id
tenant_id
user_id nullable
conversation_id nullable
agent_run_id nullable
use_case
provider_name
model_name
prompt_version_id nullable
input_hash
input_preview
output_preview
request_json
response_json
status
error_message
input_tokens
output_tokens
total_tokens
estimated_cost
latency_ms
created_at
```

Important behavior:

- Store enough to debug and evaluate.
- Avoid storing sensitive full prompts where policy forbids it.
- Support redaction.

### 11.6 Agent And Tool Tables

#### agent_definitions

Purpose: reusable agent configuration.

Fields:

```text
id
tenant_id
name
description
allowed_tool_ids
max_steps
requires_approval_for_writes
status
created_at
updated_at
```

#### agent_runs

Purpose: one execution of an agent task.

Fields:

```text
id
tenant_id
agent_definition_id
conversation_id nullable
user_id
task_text
status
risk_level
final_result
error_message
started_at
finished_at
created_at
```

Statuses:

```text
created
planning
waiting_for_approval
running_tool
verifying
completed
failed
cancelled
blocked
```

#### agent_steps

Purpose: step-by-step trace.

Fields:

```text
id
tenant_id
agent_run_id
step_number
step_type
input_json
output_json
status
started_at
finished_at
created_at
```

Step types:

```text
classify_task
retrieve_context
create_plan
validate_plan
select_tool
execute_tool
verify_tool_result
ask_user_clarification
request_approval
final_answer
```

#### tool_definitions

Purpose: typed tool registry.

Fields:

```text
id
tenant_id nullable
name
description
tool_type
input_schema_json
output_schema_json
risk_level
requires_approval
status
created_at
updated_at
```

Tool types:

```text
read_only
write_action
external_api
internal_action
human_handoff
```

#### tool_calls

Purpose: every tool request and result.

Fields:

```text
id
tenant_id
agent_run_id nullable
conversation_id nullable
tool_definition_id
requested_by
input_json
output_json
status
risk_level
dry_run
approval_id nullable
error_message
started_at
finished_at
created_at
```

#### human_approvals

Purpose: review gate for risky actions.

Fields:

```text
id
tenant_id
requested_by_user_id nullable
reviewer_user_id nullable
subject_type
subject_id
approval_status
risk_summary
request_json
decision_reason
created_at
decided_at
```

Statuses:

```text
pending
approved
rejected
expired
cancelled
```

### 11.7 Memory Tables

#### memory_items

Purpose: persistent information allowed by policy.

Fields:

```text
id
tenant_id
user_id nullable
scope
memory_type
content
content_json
source_type
source_id
importance_score
expires_at
created_at
updated_at
```

Scopes:

```text
conversation
user
tenant
agent
```

Memory types:

```text
preference
fact
summary
workflow_state
exception
```

Rules:

- Memory must be permission-aware.
- Memory should have retention controls.
- Sensitive memory should be avoided or explicitly approved.
- Memory should be retrievable and explainable.

### 11.8 Safety And Evaluation Tables

#### safety_policies

Purpose: configurable rules.

Fields:

```text
id
tenant_id nullable
name
policy_type
rules_json
severity
status
created_at
updated_at
```

Policy types:

```text
prompt_injection
pii
unsafe_output
tool_action
retrieval_context
model_usage
```

#### safety_checks

Purpose: results of checks.

Fields:

```text
id
tenant_id
subject_type
subject_id
check_type
status
risk_score
findings_json
action_taken
created_at
```

#### eval_datasets

Purpose: named evaluation collection.

Fields:

```text
id
tenant_id
name
description
use_case
version
status
created_at
updated_at
```

#### eval_cases

Purpose: individual test example.

Fields:

```text
id
tenant_id
dataset_id
input_json
expected_output_json
reference_context_json
tags
created_at
updated_at
```

#### eval_runs

Purpose: one evaluation execution.

Fields:

```text
id
tenant_id
dataset_id
run_name
run_type
candidate_config_json
baseline_config_json
status
started_at
finished_at
created_at
```

#### eval_results

Purpose: scores per case.

Fields:

```text
id
tenant_id
eval_run_id
eval_case_id
output_json
scores_json
pass_fail
error_message
created_at
```

#### feedback

Purpose: online user signal.

Fields:

```text
id
tenant_id
user_id
subject_type
subject_id
rating
comment
feedback_tags
created_at
```

### 11.9 Observability And Audit Tables

#### audit_events

Purpose: immutable business and security audit trail.

Fields:

```text
id
tenant_id
actor_user_id nullable
event_type
subject_type
subject_id
metadata_json
ip_address
user_agent
created_at
```

#### cost_records

Purpose: cost accounting.

Fields:

```text
id
tenant_id
ai_run_id nullable
provider_name
model_name
use_case
input_tokens
output_tokens
cost_usd
created_at
```

#### background_jobs

Purpose: generic async job tracking.

Fields:

```text
id
tenant_id nullable
job_name
payload_json
status
attempt_count
max_attempts
error_message
scheduled_at
started_at
finished_at
created_at
updated_at
```

### 11.10 Entity Relationship Map

The database should be implemented with explicit relationships. This map is the implementation guide before drawing a visual ERD.

Identity relationships:

```text
tenants 1 -> many tenant_memberships
tenants 1 -> many roles
users 1 -> many tenant_memberships
roles many -> many permissions through role_permissions
```

Knowledge relationships:

```text
tenants 1 -> many knowledge_collections
knowledge_collections 1 -> many documents
documents 1 -> many document_versions
document_versions 1 -> many document_pages
document_versions 1 -> many document_chunks
document_chunks 1 -> many chunk_embeddings
```

RAG relationships:

```text
conversations 1 -> many conversation_messages
conversations 1 -> many rag_queries
rag_queries 1 -> many rag_retrieval_results
rag_queries 1 -> one or many rag_answers
rag_answers 1 -> many answer_citations
answer_citations many -> one document_chunks
ai_runs 1 -> many rag_answers optional
```

Prompt/model relationships:

```text
prompt_templates 1 -> many prompt_versions
prompt_templates 1 -> many prompt_test_cases
model_providers 1 -> many model_routes
prompt_versions 1 -> many ai_runs
model_routes 1 -> many ai_runs optional
```

Agent/tool relationships:

```text
agent_definitions 1 -> many agent_runs
agent_runs 1 -> many agent_steps
agent_runs 1 -> many tool_calls optional
tool_definitions 1 -> many tool_calls
tool_calls many -> one human_approvals optional
agent_steps many -> one ai_runs optional
```

Evaluation relationships:

```text
eval_datasets 1 -> many eval_cases
eval_datasets 1 -> many eval_runs
eval_runs 1 -> many eval_results
eval_cases 1 -> many eval_results
ai_runs 1 -> many eval_results optional
```

Safety/governance relationships:

```text
safety_policies 1 -> many safety_checks optional
ai_runs 1 -> many safety_checks optional
agent_runs 1 -> many safety_checks optional
tool_calls 1 -> many safety_checks optional
audit_events references many subject types by subject_type + subject_id
```

Implementation rules:

- Use foreign keys where relationships are stable and direct.
- Use `subject_type` plus `subject_id` only for audit and polymorphic records.
- Add indexes on every foreign key.
- Add composite indexes on `tenant_id` plus common filters.
- Use unique constraints for idempotency keys where side effects exist.
- Avoid cascade deletes for audit-sensitive data; prefer soft delete plus retention jobs.

### 11.11 Data Lineage And Provenance

Data lineage means the system can explain where data came from and how it changed.

Atlas must track lineage for:

- Original uploaded document.
- Document version.
- Parser used.
- OCR engine used.
- Cleaning rules used.
- Chunking strategy used.
- Embedding model used.
- Vector index used.
- Retrieval strategy used.
- Prompt version used.
- Model used.
- Evaluation dataset used.
- Fine-tuning dataset used.

Lineage fields to include where relevant:

```text
source_type
source_uri
source_checksum
parser_name
parser_version
chunker_name
chunker_version
embedding_model
embedding_dimension
prompt_version_id
model_route_id
model_name
dataset_version
created_by_user_id
job_id
trace_id
```

Why this matters:

- Debugging bad answers.
- Reproducing evaluations.
- Proving compliance.
- Rebuilding vector indexes.
- Removing deleted data.
- Preventing contaminated training datasets.

### 11.12 Document Deletion And Reindexing Lifecycle

Deleting a document in a Gen AI platform is more complex than deleting one row.

Delete flow:

```text
user requests delete
-> permission check
-> document marked deleted
-> chunks marked deleted
-> embedding delete job queued
-> vector points removed or tombstoned
-> object storage retention rule applied
-> audit event recorded
-> downstream eval/training datasets checked
```

Reindex flow:

```text
document changes or embedding model changes
-> new document_version created if content changed
-> old chunks marked inactive
-> new chunks generated
-> new embeddings generated
-> vector index updated
-> retrieval tests run
-> old vectors deleted after validation
```

Rules:

- Do not return deleted chunks in retrieval.
- Vector deletion must be verified.
- If data was used in fine-tuning dataset, mark the dataset lineage and decide whether model withdrawal is required.
- If legal or tenant policy requires hard deletion, object storage and vector store must be included.

### 11.13 Tenant Data Export

Enterprise systems often need tenant export.

Export should include:

- Documents metadata.
- Extracted text references where policy allows.
- Conversations.
- AI runs metadata.
- Feedback.
- Agent runs.
- Tool calls.
- Audit events.
- Evaluation datasets owned by tenant.

Export rules:

- Require admin permission.
- Record audit event.
- Run as background job.
- Store export artifact with expiration.
- Redact secrets and internal provider credentials.

### 11.14 Retention Enforcement

Retention means automatically deleting or archiving data after a policy period.

Retention applies to:

- Raw uploads.
- Extracted text.
- Chunks.
- Embeddings.
- Conversations.
- AI run payloads.
- Tool call payloads.
- Audio files.
- Generated media.
- Evaluation datasets.

Implementation requirements:

- Add retention policy configuration per tenant.
- Store `expires_at` where relevant.
- Run scheduled retention jobs.
- Record audit events for deletion.
- Keep aggregated metrics when raw content must be deleted.

### 11.15 Dataset Contamination Prevention

Dataset contamination happens when evaluation or training data is polluted by examples that make results misleading.

Risks:

- Evaluation answers accidentally included in prompts.
- Test cases used in training datasets.
- Production user data used without consent.
- Generated synthetic data treated as human-labeled truth.
- Prompt-injection examples included without labels.

Controls:

- Separate dataset purpose: eval, training, red-team, synthetic, production feedback.
- Store dataset source and review status.
- Keep train/validation/test split ids stable.
- Never evaluate on examples used to train the candidate model.
- Redact or exclude sensitive data before training.
- Add contamination checks before model promotion.

## 12. Storage Architecture

### 12.1 Relational Storage

Use PostgreSQL for:

- Users.
- Tenants.
- Documents.
- Chunks metadata.
- AI runs.
- Agent runs.
- Tool calls.
- Evaluations.
- Safety records.
- Audit events.

### 12.2 Vector Storage

Option A: pgvector.

Use when:

- You want simpler local development.
- You want fewer moving parts.
- Dataset is not massive.
- You want transactional alignment with document metadata.

Option B: Qdrant.

Use when:

- You want a dedicated vector database.
- You expect larger scale.
- You need payload filters and vector-specific operations.
- You want easier experimentation with vector index settings.

Recommended first implementation:

- Start with pgvector because it keeps architecture simpler.
- Keep a `VectorStore` interface so Qdrant can be added later.

### 12.3 Object Storage

Use object storage for:

- Original uploaded files.
- Extracted page images.
- OCR artifacts.
- Evaluation reports.
- Fine-tuning datasets.
- Model artifacts if not handled by a model registry.

Local option:

- MinIO.

Cloud options:

- AWS S3.
- Azure Blob Storage.
- Google Cloud Storage.

### 12.4 Cache And Queue Storage

Use Redis for:

- Rate limits.
- Short-lived request cache.
- Background job broker.
- Temporary agent state if needed.
- Idempotency keys.
- Distributed locks for ingestion jobs.

Redis should not be the source of truth for business data.

## 13. API Architecture

All APIs should be versioned.

Base path:

```text
/api/v1
```

API rules:

- All request bodies use Pydantic schemas.
- All responses use explicit response schemas.
- All authenticated routes require tenant context.
- Dangerous operations require permissions.
- AI actions should return run ids for traceability.
- Long-running operations should return job ids.
- Pagination should be consistent.
- Errors should use a consistent error envelope.

### 13.1 Error Envelope

Standard error shape:

```json
{
  "error": {
    "code": "documents.not_found",
    "message": "Document not found.",
    "details": {},
    "request_id": "req_123"
  }
}
```

### 13.2 Auth APIs

Endpoints:

```text
POST /api/v1/auth/login
POST /api/v1/auth/logout
GET  /api/v1/auth/me
GET  /api/v1/tenants
POST /api/v1/tenants/{tenant_id}/switch
```

Implementation notes:

- Use JWT or secure session cookies.
- Include tenant selection in request context.
- Return permissions to the frontend for UI gating.

### 13.3 Document APIs

Endpoints:

```text
POST   /api/v1/documents
GET    /api/v1/documents
GET    /api/v1/documents/{document_id}
DELETE /api/v1/documents/{document_id}
GET    /api/v1/documents/{document_id}/versions
GET    /api/v1/documents/{document_id}/chunks
POST   /api/v1/documents/{document_id}/reingest
GET    /api/v1/ingestion-jobs/{job_id}
```

Responsibilities:

- Upload file.
- Store metadata.
- Queue ingestion.
- Show processing status.
- Show extracted chunks.
- Reprocess documents.

### 13.4 Search And RAG APIs

Endpoints:

```text
POST /api/v1/search/semantic
POST /api/v1/search/hybrid
POST /api/v1/rag/query
GET  /api/v1/rag/queries/{query_id}
GET  /api/v1/rag/answers/{answer_id}
POST /api/v1/rag/answers/{answer_id}/feedback
```

`POST /api/v1/rag/query` request:

```json
{
  "conversation_id": "conv_123",
  "query": "What is the refund policy for enterprise customers?",
  "collection_ids": ["col_123"],
  "filters": {
    "document_type": "policy"
  },
  "include_citations": true
}
```

Response:

```json
{
  "answer_id": "ans_123",
  "answer": "...",
  "citations": [
    {
      "document_id": "doc_123",
      "chunk_id": "chunk_123",
      "page_start": 2,
      "page_end": 3,
      "support_type": "supports_claim"
    }
  ],
  "confidence_label": "medium",
  "ai_run_id": "run_123"
}
```

### 13.5 Conversation APIs

Endpoints:

```text
POST /api/v1/conversations
GET  /api/v1/conversations
GET  /api/v1/conversations/{conversation_id}
POST /api/v1/conversations/{conversation_id}/messages
POST /api/v1/conversations/{conversation_id}/summarize
```

Responsibilities:

- Manage chat sessions.
- Store messages.
- Support chat, RAG, agent, voice, and multimodal modes.

### 13.6 Prompt APIs

Endpoints:

```text
POST /api/v1/prompts
GET  /api/v1/prompts
GET  /api/v1/prompts/{prompt_id}
POST /api/v1/prompts/{prompt_id}/versions
POST /api/v1/prompts/{prompt_id}/versions/{version_id}/activate
POST /api/v1/prompts/{prompt_id}/test
GET  /api/v1/prompts/{prompt_id}/tests
```

Responsibilities:

- Create prompt templates.
- Version prompt changes.
- Test prompt outputs.
- Activate approved versions.

### 13.7 Model Gateway APIs

These can be internal first, public later.

Endpoints:

```text
POST /api/v1/models/chat
POST /api/v1/models/structured
POST /api/v1/models/embed
GET  /api/v1/models/routes
POST /api/v1/models/routes
GET  /api/v1/ai-runs/{ai_run_id}
```

Responsibilities:

- Controlled model access.
- Model routing.
- Run logging.
- Cost tracking.

### 13.8 Agent APIs

Endpoints:

```text
POST /api/v1/agents
GET  /api/v1/agents
GET  /api/v1/agents/{agent_id}
POST /api/v1/agents/{agent_id}/runs
GET  /api/v1/agent-runs/{run_id}
GET  /api/v1/agent-runs/{run_id}/steps
POST /api/v1/agent-runs/{run_id}/cancel
```

Run request:

```json
{
  "task": "Find open refund tickets and draft escalation notes.",
  "mode": "supervised",
  "dry_run": true
}
```

### 13.9 Tool APIs

Endpoints:

```text
GET  /api/v1/tools
POST /api/v1/tools/{tool_id}/dry-run
POST /api/v1/tools/{tool_id}/execute
GET  /api/v1/tool-calls/{tool_call_id}
```

Rules:

- Tool execution requires permission.
- Write tools require approval unless policy says otherwise.
- Tool inputs and outputs must validate against schemas.
- Tool calls must be logged.

### 13.10 Approval APIs

Endpoints:

```text
GET  /api/v1/approvals
GET  /api/v1/approvals/{approval_id}
POST /api/v1/approvals/{approval_id}/approve
POST /api/v1/approvals/{approval_id}/reject
```

Responsibilities:

- Show pending risky actions.
- Allow reviewers to approve or reject.
- Resume blocked agent runs after approval.

### 13.11 Evaluation APIs

Endpoints:

```text
POST /api/v1/eval-datasets
GET  /api/v1/eval-datasets
POST /api/v1/eval-datasets/{dataset_id}/cases
POST /api/v1/eval-runs
GET  /api/v1/eval-runs
GET  /api/v1/eval-runs/{eval_run_id}
GET  /api/v1/eval-runs/{eval_run_id}/results
```

Responsibilities:

- Manage eval datasets.
- Run prompt/model/RAG/agent evals.
- Compare scores.
- Identify regressions.

### 13.12 Safety APIs

Endpoints:

```text
GET  /api/v1/safety/policies
POST /api/v1/safety/policies
POST /api/v1/safety/check-input
POST /api/v1/safety/check-output
GET  /api/v1/safety/checks
GET  /api/v1/safety/red-team-cases
POST /api/v1/safety/red-team-runs
```

Responsibilities:

- Manage safety policy.
- Run safety checks.
- Review violations.
- Test defenses.

### 13.13 Admin And Observability APIs

Endpoints:

```text
GET /api/v1/admin/users
GET /api/v1/admin/audit-events
GET /api/v1/admin/costs
GET /api/v1/admin/latency
GET /api/v1/admin/model-usage
GET /api/v1/admin/jobs
GET /api/v1/admin/health
```

Responsibilities:

- Operational dashboards.
- Cost visibility.
- Job health.
- Audit review.

### 13.14 Concrete API Contract Standards

Endpoint lists are not enough. Every API must define headers, auth rules, request body, response body, pagination behavior, error cases, idempotency rules, and audit behavior.

Standard headers:

```text
Authorization: Bearer <token>
X-Tenant-ID: <tenant_id>
X-Request-ID: <request_id>
Idempotency-Key: <key for side-effect operations>
```

Rules:

- `Authorization` is required for protected APIs.
- `X-Tenant-ID` is required when the user belongs to more than one tenant.
- `X-Request-ID` is accepted from clients or generated by the API.
- `Idempotency-Key` is required for uploads, write tool calls, approvals, generated media jobs, and external side effects.

Standard success envelope:

```json
{
  "data": {},
  "meta": {
    "request_id": "req_123"
  }
}
```

Standard list envelope:

```json
{
  "data": [],
  "pagination": {
    "limit": 50,
    "cursor": "next_cursor",
    "has_more": true
  },
  "meta": {
    "request_id": "req_123"
  }
}
```

Standard error envelope:

```json
{
  "error": {
    "code": "rag.no_supporting_context",
    "message": "The answer could not be grounded in the available documents.",
    "details": {
      "query_id": "ragq_123"
    },
    "request_id": "req_123"
  }
}
```

### 13.15 Pagination, Filtering, And Sorting

Use cursor pagination for tables that grow continuously:

- documents.
- conversations.
- AI runs.
- agent runs.
- agent steps.
- tool calls.
- eval results.
- safety checks.
- audit events.

Request pattern:

```text
GET /api/v1/documents?limit=50&cursor=abc&sort=-created_at
```

Filter rules:

- Validate filter fields against an allowlist.
- Always inject tenant filter server-side.
- Do not trust tenant filters from the client.
- Use indexed fields for common filters.

### 13.16 Document Upload API Contract

Endpoint:

```text
POST /api/v1/documents
```

Request:

```text
multipart/form-data
file: binary
title: string
collection_id: string
metadata_json: optional JSON string
```

Response:

```json
{
  "data": {
    "document_id": "doc_123",
    "document_version_id": "docv_123",
    "ingestion_job_id": "job_123",
    "status": "queued"
  },
  "meta": {
    "request_id": "req_123"
  }
}
```

Required checks:

- User has `documents.write` permission.
- File extension and MIME type are allowed.
- File size is below tenant limit.
- Collection belongs to tenant.
- Idempotency key is new or matches same upload intent.
- Object storage write succeeds before job is queued.

Failure cases:

```text
documents.unsupported_file_type
documents.file_too_large
documents.collection_not_found
storage.write_failed
validation.invalid_metadata
```

### 13.17 RAG Query API Contract

Endpoint:

```text
POST /api/v1/rag/query
```

Request:

```json
{
  "conversation_id": "conv_123",
  "query": "What is the refund policy for enterprise customers?",
  "collection_ids": ["col_123"],
  "filters": {
    "document_type": "policy",
    "effective_after": "2026-01-01"
  },
  "retrieval": {
    "strategy": "hybrid_rerank",
    "top_k": 20,
    "rerank_top_k": 8
  },
  "response": {
    "include_citations": true,
    "format": "answer_with_sources"
  }
}
```

Response:

```json
{
  "data": {
    "query_id": "ragq_123",
    "answer_id": "ansa_123",
    "answer": "Enterprise refunds require approval when the amount exceeds the configured threshold.",
    "citations": [
      {
        "document_id": "doc_123",
        "chunk_id": "chunk_123",
        "page_start": 4,
        "page_end": 4,
        "support_type": "supports_claim"
      }
    ],
    "confidence_label": "medium",
    "ai_run_id": "airun_123",
    "retrieval_trace_id": "retr_123"
  }
}
```

Required checks:

- User has `rag.query` permission.
- All collections belong to tenant.
- Retrieval applies tenant and ACL filters.
- Input safety check passes.
- Retrieved context is treated as untrusted data.
- Final answer has citations or a clear not-enough-information response.

### 13.18 Agent Run API Contract

Endpoint:

```text
POST /api/v1/agents/{agent_id}/runs
```

Request:

```json
{
  "task": "Find open refund tickets and draft escalation notes.",
  "mode": "supervised",
  "dry_run": true,
  "limits": {
    "max_steps": 12,
    "max_tool_calls": 5,
    "max_cost_usd": 1.50
  }
}
```

Response:

```json
{
  "data": {
    "agent_run_id": "arun_123",
    "status": "planning",
    "trace_url": "/agents/runs/arun_123"
  }
}
```

Required checks:

- User has `agents.run` permission.
- Agent definition is active.
- Requested mode is allowed for tenant.
- Tool limits do not exceed policy.
- Risk level is calculated before write actions.

### 13.19 Evaluation Run API Contract

Endpoint:

```text
POST /api/v1/eval-runs
```

Request:

```json
{
  "dataset_id": "evalds_123",
  "run_name": "rag-prompt-v4-vs-v3",
  "candidate": {
    "prompt_version_id": "pv_4",
    "model_route": "rag_answer_default",
    "retrieval_strategy": "hybrid_rerank"
  },
  "baseline": {
    "prompt_version_id": "pv_3",
    "model_route": "rag_answer_default",
    "retrieval_strategy": "vector_only"
  },
  "scorers": ["correctness", "groundedness", "citation_accuracy", "safety"]
}
```

Response:

```json
{
  "data": {
    "eval_run_id": "evalrun_123",
    "status": "queued"
  }
}
```

Promotion rule:

- A candidate cannot become active unless its eval run meets the configured promotion thresholds.

### 13.20 Generated Media Job API Contract

Endpoint:

```text
POST /api/v1/media/generations
```

Request:

```json
{
  "media_type": "image",
  "prompt": "Create a clean product support workflow diagram in a modern enterprise style.",
  "style_preset": "enterprise_diagram",
  "size": "1024x1024",
  "count": 1,
  "safety": {
    "allow_brand_logos": false,
    "allow_real_person_likeness": false
  }
}
```

Response:

```json
{
  "data": {
    "generation_job_id": "genjob_123",
    "status": "queued"
  }
}
```

Required checks:

- User has `media.generate` permission.
- Prompt safety check passes.
- Cost estimate is within tenant budget.
- Generated output is stored with provenance and safety metadata.

## 14. Service Communication

### 14.1 Synchronous Calls

Use synchronous calls for:

- User login.
- Listing documents.
- Asking short chat/RAG questions.
- Reading agent run status.
- Creating prompt versions.
- Fetching evaluation results.

### 14.2 Asynchronous Jobs

Use background jobs for:

- Large document ingestion.
- OCR.
- Embedding generation.
- Batch evaluations.
- Fine-tuning dataset preparation.
- Fine-tuning execution orchestration.
- Large report generation.
- Long-running agent workflows.

### 14.3 Job Pattern

Standard job flow:

```text
API receives request
-> validates permission
-> writes database record
-> queues job with job id
-> returns job id
-> worker processes job
-> worker updates status
-> frontend polls or subscribes to status
```

### 14.4 Idempotency

Use idempotency keys for:

- Document uploads.
- Tool write actions.
- Agent actions.
- Payment or billing operations if added.
- External API calls that could duplicate side effects.

### 14.5 Transaction Boundaries

Rules:

- Database writes for business state should be atomic.
- External provider calls should not be inside long database transactions.
- For tool calls, record intent before execution and result after execution.
- For background jobs, use status records to recover from failure.

## 15. Model Gateway Design

The model gateway is the only place where the system talks to LLMs, embedding models, rerankers, or local inference servers.

### 15.1 Responsibilities

The model gateway owns:

- Provider adapters.
- Model routing.
- Request validation.
- Timeout policy.
- Retry policy.
- Rate-limit handling.
- Streaming support.
- Token counting.
- Cost estimation.
- AI run logging.
- Structured output validation.
- Provider fallback.
- Mock model behavior for tests.

### 15.2 Provider Adapter Interface

Every provider adapter should implement the same logical interface:

```text
chat(request) -> ChatResponse
structured(request, schema) -> StructuredResponse
embed(request) -> EmbeddingResponse
rerank(request) -> RerankResponse optional
```

The rest of the application must not care which provider is used.

### 15.3 Model Routing

Routing is selected by use case.

Example:

```text
rag_answer -> high quality chat model
query_rewrite -> cheaper fast model
structured_extraction -> model with strong schema following
agent_planning -> reasoning-capable model
agent_verification -> cheaper verifier model or judge model
embedding -> embedding model
safety_check -> classifier or policy model
llm_judge -> judge model
```

Routing can depend on:

- Tenant.
- Use case.
- Cost budget.
- Latency requirement.
- Model availability.
- Data sensitivity.
- Fallback rules.

### 15.4 Gateway Request Fields

A model request should include:

```text
request_id
tenant_id
user_id optional
use_case
messages or input
prompt_version_id optional
model_override optional
temperature
max_tokens
response_schema optional
metadata
trace_id
```

### 15.5 Gateway Response Fields

A model response should include:

```text
ai_run_id
provider_name
model_name
output_text
output_json optional
finish_reason
input_tokens
output_tokens
total_tokens
estimated_cost
latency_ms
raw_response_reference
```

### 15.6 Retry Policy

Retry only when useful.

Retry cases:

- Temporary network failure.
- Provider timeout.
- Rate limit with backoff.
- Invalid structured output if repair is allowed.

Do not retry blindly when:

- The request violates policy.
- The input is too large.
- Authentication with provider fails.
- The output is unsafe.
- The tool action would cause duplicate side effects.

### 15.7 Cost Control

Cost controls:

- Per-tenant monthly budget.
- Per-user daily budget.
- Per-request max token limit.
- Cheaper model routing for simple tasks.
- Cache safe repeated operations.
- Truncate or summarize long contexts.
- Warn or block expensive evaluations.

### 15.8 Streaming

Streaming is useful for chat UX but should still preserve logging.

Flow:

```text
API receives chat request
-> gateway starts provider stream
-> chunks sent to frontend
-> final text assembled server-side
-> final ai_run stored with usage and metadata
```

### 15.9 Test Provider

A fake provider is required for tests.

It should support:

- Fixed text responses.
- Fixed structured responses.
- Simulated invalid JSON.
- Simulated timeout.
- Simulated rate limit.
- Simulated unsafe output.

This allows backend tests without real model calls.


### 15.10 Provider-Level Prompt Caching

Prompt caching is a major cost and latency control for long prompts, RAG prompts, agent instructions, and repeated system/developer instructions.

Definition:

Prompt caching lets a model provider reuse previously processed prompt prefixes so repeated long context is cheaper or faster when the provider supports it.

Use cases:

- Long system prompts.
- Stable agent instructions.
- Large tool schema lists.
- Repeated policy context.
- RAG workflows with stable instruction prefix.
- Evaluation runs with repeated task instructions.

Implementation requirements:

- The model gateway should mark cacheable prompt segments where provider APIs support it.
- Prompt rendering should separate stable prefix from dynamic user content.
- AI run records should store cache-read/cache-write token counts when providers return them.
- Cost calculator should account for cached-token pricing separately when available.
- Evaluation reports should compare cached and uncached latency/cost.

Prompt construction pattern:

```text
cacheable stable prefix:
  system instructions
  safety policy summary
  output format rules
  tool schema descriptions

dynamic suffix:
  user query
  retrieved context
  current conversation turn
```

Rules:

- Do not cache tenant-private content unless provider policy and tenant configuration allow it.
- Do not assume every provider supports prompt caching in the same way.
- Provider prompt caches usually have TTL behavior measured in minutes or provider-defined windows, so the gateway must treat cache reuse as opportunistic.
- Prompt caching only pays off above provider-specific minimum token thresholds; do not over-engineer caching for tiny prompts.
- Store provider capability metadata for cache TTL, cacheable token floor, cache-write tokens, cache-read tokens, and unsupported-cache behavior.
- Gateway adapters should expose provider capability flags.

Data fields to add to `ai_runs`:

```text
cache_read_tokens
cache_write_tokens
cache_hit_rate optional
cache_strategy
```

### 15.11 Semantic Caching

Semantic caching is different from provider prompt caching.

Definition:

Semantic caching stores answers or intermediate results for semantically similar requests.

Use cases:

- Repeated support policy questions.
- Repeated query rewrites.
- Repeated classifications.
- Expensive retrieval plus answer generation where documents have not changed.

Architecture:

```text
incoming request
-> normalize request
-> create embedding for query or cache key
-> search semantic cache
-> if high confidence hit and data version is valid, return cached result
-> otherwise run normal workflow
-> store result with source versions and expiration
```

Cache safety requirements:

- Cache entries must include tenant id.
- Cache entries must include permission scope.
- Cache entries must include document index version when RAG is involved.
- Cache entries must expire.
- Cache entries must not bypass safety checks.
- Cached RAG answers must remain valid only while source documents and prompt/model versions are valid.

Suggested table:

```text
semantic_cache_entries
  id
  tenant_id
  use_case
  cache_key_hash
  query_embedding_id optional
  input_summary
  output_json
  source_version_hash
  prompt_version_id
  model_name
  safety_status
  expires_at
  created_at
```

### 15.12 Batch APIs And Batch Processing

Batch APIs reduce cost and operational overhead for offline work.

Use batch processing for:

- Embedding many chunks.
- Running evaluation datasets.
- Classifying historical tickets.
- Preparing fine-tuning datasets.
- Running synthetic data generation.
- Running safety red-team suites.

Gateway requirements:

- Support single request and batch request interfaces.
- Track batch job id.
- Store per-item results and failures.
- Retry failed items selectively.
- Respect provider batch limits.
- Estimate cost before submitting large batches.

Batch flow:

```text
worker creates batch request
-> gateway validates batch size and budget
-> provider batch job submitted or local batch executed
-> batch job status stored
-> worker polls or receives completion
-> per-item results stored
-> failed items retried or marked failed
```

### 15.13 Reasoning And Extended-Thinking Models

Some models expose deeper reasoning modes or consume extra reasoning/thinking tokens. They should be used deliberately, not as the default for everything.

Use reasoning models for:

- Complex agent planning.
- Multi-step policy analysis.
- Hard evaluation judging.
- Complex tool-use verification.
- Ambiguous document comparison.
- Multi-hop RAG questions.

Avoid reasoning models for:

- Simple classification.
- Query rewrite.
- Embedding.
- Basic summarization.
- Simple extraction when a cheaper model works.

Gateway routing must include:

```text
reasoning_enabled
reasoning_budget_tokens
reasoning_effort low|medium|high where provider supports it
max_total_cost
```

AI run records should track:

```text
reasoning_tokens
reasoning_budget_tokens
reasoning_effort
```

Safety rules:

- Do not expose hidden reasoning traces to end users if provider policy or product policy forbids it.
- Store only allowed reasoning summaries when needed for audit.
- Evaluate whether reasoning mode improves outcomes enough to justify cost.

### 15.14 Streaming Tool Calls And Partial Structured Outputs

Streaming is not only text streaming. Real applications also need to handle tool-call streams and partial structured outputs.

Streaming cases:

- Chat token streaming.
- Tool-call argument streaming.
- Partial JSON object streaming.
- Agent step progress streaming.
- Voice real-time response streaming.

Implementation requirements:

- Keep a server-side stream assembler.
- Validate final tool arguments before execution.
- Never execute a tool from partial arguments.
- If partial structured output is invalid mid-stream, wait until final output or use incremental parser carefully.
- Store final assembled output in `ai_runs`.
- Send frontend progress events with event type and run id.

Suggested event types:

```text
message.delta
tool_call.started
tool_call.arguments_delta
tool_call.ready_for_validation
tool_call.executed
agent_step.started
agent_step.completed
run.completed
run.failed
```

### 15.15 Provider Capability Matrix

The model gateway should track provider capabilities instead of assuming all providers are equal.

Capability fields:

```text
supports_chat
supports_structured_output
supports_streaming
supports_tool_calling
supports_prompt_caching
supports_batch_api
supports_reasoning_controls
supports_embeddings
supports_reranking
supports_image_input
supports_image_generation
supports_audio_input
supports_audio_output
supports_video_generation
supports_fine_tuning
supports_managed_batch
max_context_tokens
max_output_tokens
data_retention_policy
region_support
```

This matrix prevents accidental use of unsupported features and helps explain routing decisions.

### 15.16 LLM Optimization Decision Tree

When cost or latency is too high, optimize in this order:

1. Reduce unnecessary prompt text.
2. Separate stable prompt prefix for provider prompt caching.
3. Improve context packing.
4. Use cheaper model for query rewrite/classification.
5. Add semantic caching for repeated safe workflows.
6. Use batch APIs for offline jobs.
7. Distill or fine-tune smaller models if evaluation supports it.
8. Serve optimized open models when cost justifies operational complexity.
9. Add quantization or batching at inference layer.

Do not jump to fine-tuning or self-hosting before measuring the bottleneck.

## 16. Prompt System Design

Prompts are production assets. They must be versioned, tested, reviewed, and traceable.

### 16.1 Prompt Types

Atlas should support these prompt types:

```text
system prompts
user templates
developer instructions
query rewrite prompts
classification prompts
extraction prompts
RAG answer prompts
agent planning prompts
agent verification prompts
safety prompts
LLM judge prompts
summarization prompts
voice summary prompts
multimodal extraction prompts
```

### 16.2 Prompt Lifecycle

Prompt lifecycle:

```text
draft
-> local test
-> eval dataset test
-> review
-> approved
-> active
-> monitored
-> retired
```

### 16.3 Prompt Rendering

Prompt rendering flow:

```text
service requests prompt by use case
-> prompt registry finds active version
-> renderer validates required variables
-> renderer injects variables
-> rendered prompt is passed to model gateway
-> prompt_version_id is stored in ai_runs
```

### 16.4 Prompt Variables

Prompt templates should declare variables explicitly.

Examples:

```text
user_question
retrieved_context
conversation_summary
current_date
tenant_policy
output_schema
tool_list
agent_state
```

Rules:

- Missing variables fail before model call.
- Large variables must be token-counted.
- Retrieved context must be separated from instructions.
- User-provided text must never be treated as system instructions.

### 16.5 Prompt Testing

Each important prompt should have:

- Happy path examples.
- Edge cases.
- Adversarial examples.
- Output format tests.
- Regression examples from real failures.

Prompt tests should verify:

- Output follows schema.
- Refusal behavior is correct.
- Citations are used when required.
- Unknown answers are not hallucinated.
- Tool calls are valid.
- Tone and business constraints are followed.

### 16.6 Automatic Prompt Optimization

Manual prompt versioning is required, but mature systems can also test optimizer-assisted prompt improvement.

Definition:

Automatic prompt optimization means using examples, metrics, and search/optimization methods to propose better prompts instead of relying only on human edits.

Examples:

- Generate candidate instructions from failed eval cases.
- Use few-shot example selection.
- Tune prompt wording against an evaluation dataset.
- Use DSPy-style module optimization where a program is optimized against metrics.
- Compare system prompt variants automatically.

Architecture:

```text
eval failures collected
-> prompt optimization job created
-> optimizer proposes candidate prompt versions
-> candidate versions run against eval dataset
-> results compared against baseline
-> human reviews winning candidate
-> approved prompt version is activated
```

Implementation requirements:

- Optimizer cannot directly activate production prompts.
- Every generated candidate prompt becomes a draft prompt version.
- Candidate prompt must be evaluated against safety and quality datasets.
- Promotion requires human approval.
- Prompt optimizer runs as offline job, not inside user request path.

Data additions:

```text
prompt_optimization_jobs
  id
  tenant_id
  prompt_template_id
  baseline_prompt_version_id
  dataset_id
  optimizer_type
  status
  created_at

prompt_optimization_candidates
  id
  job_id
  candidate_prompt_version_id
  scores_json
  rank
  reviewer_decision
```

When to use:

- After enough eval failures exist.
- When a prompt has measurable quality problems.
- When output format or citation behavior needs improvement.

When not to use:

- Before defining evaluation metrics.
- When the task lacks a stable objective.
- When the prompt handles high-risk policy without human review.

## 17. Structured Output Design

Structured outputs make LLM results usable by backend code.

### 17.1 Use Cases

Use structured outputs for:

- Intent classification.
- Ticket classification.
- Entity extraction.
- Document field extraction.
- Query rewriting.
- Agent planning.
- Tool selection.
- Safety risk scoring.
- Evaluation judging.
- Citation claim mapping.

### 17.2 Schema-First Design

Every structured output should start with a schema.

Example object types:

```text
IntentClassification
DocumentExtractionResult
QueryRewriteResult
AgentPlan
ToolSelection
SafetyDecision
EvaluationScore
```

Rules:

- Define schema before writing prompts.
- Include required and optional fields clearly.
- Use enums for controlled values.
- Validate model output with Pydantic.
- Store parsed output and raw output when allowed.
- Do not let invalid model JSON move forward silently.

### 17.3 Repair Loop

Structured output repair flow:

```text
model returns output
-> parser validates schema
-> if valid, continue
-> if invalid and repair allowed, call repair prompt with validation error
-> parse again
-> if still invalid, fail gracefully
```

Repair should be limited to avoid endless loops and cost spikes.

### 17.4 Failure Handling

Failure modes:

- Missing required field.
- Wrong enum value.
- Invalid JSON.
- Unsupported action.
- Unsafe instruction inside output.
- Tool arguments fail validation.

System response:

- Return clear error for internal workflows.
- Ask user a clarification if user input is incomplete.
- Log validation failure for prompt improvement.
- Add failed case to evaluation dataset if important.

## 18. Document Ingestion Design

Document ingestion turns raw business files into searchable, citeable knowledge.

### 18.1 Supported Inputs

Initial supported files:

```text
PDF
DOCX
TXT
Markdown
CSV
HTML
images for OCR later
```

Later inputs:

```text
email threads
support tickets
web pages
CRM notes
call transcripts
scanned forms
```

### 18.2 Ingestion Flow

```text
user uploads file
-> API validates file type and permissions
-> file stored in object storage
-> document record created
-> ingestion job queued
-> worker extracts text
-> worker extracts metadata
-> worker normalizes text
-> worker splits into pages or sections
-> worker chunks text
-> worker calculates content hashes
-> worker creates embeddings
-> worker stores vectors
-> document status becomes processed
```

### 18.3 Extraction Strategy

Extraction should depend on file type.

PDF:

- Try text extraction first.
- Use OCR only when text extraction is empty or low quality.
- Preserve page numbers for citations.

DOCX:

- Extract paragraphs, tables, headings.
- Preserve section structure where possible.

CSV:

- Treat each row or logical group as structured text.
- Preserve column names.

HTML:

- Remove scripts and navigation.
- Keep headings and meaningful text.

Images:

- Use OCR.
- Store OCR confidence.
- Preserve bounding boxes if available.

### 18.4 Cleaning And Normalization

Cleaning steps:

- Remove repeated headers and footers where possible.
- Normalize whitespace.
- Remove broken hyphenation.
- Preserve lists and tables when useful.
- Remove empty pages.
- Detect language.
- Detect duplicate content.
- Calculate checksum.

### 18.5 Chunking Strategy

Chunking must balance retrieval quality and context size.

Chunking options:

- Fixed token chunks.
- Sliding window chunks.
- Heading-aware chunks.
- Page-aware chunks.
- Semantic chunks.

Recommended initial strategy:

```text
heading-aware when structure exists
page-aware for PDFs
fallback to token chunks with overlap
```

Chunk metadata should include:

```text
document_id
document_version_id
page_start
page_end
section_title
chunk_index
token_count
source_uri
content_hash
```

### 18.6 Ingestion Quality Checks

Check:

- Was text extracted?
- Is OCR confidence acceptable?
- Are chunks too small or too large?
- Were embeddings generated?
- Are vector ids stored?
- Are citations possible?
- Is the document searchable?

## 19. Embeddings And Vector Search Design

Embeddings convert text into vectors so semantic search can find relevant meaning.

### 19.1 Embedding Flow

```text
chunk created
-> embedding job queued
-> embedding model selected
-> chunk text sent to model gateway embed endpoint
-> vector returned
-> vector stored in pgvector or Qdrant
-> chunk embedding record stored
```

### 19.2 Embedding Versioning

Embeddings must track:

- Embedding model name.
- Embedding dimension.
- Chunk content hash.
- Creation time.

If the embedding model changes, old embeddings should not be silently mixed with new ones unless intentionally supported.

### 19.3 Vector Search Inputs

Search request should include:

```text
tenant_id
query_text
collection_ids
filters
top_k
embedding_model
retrieval_strategy
```

### 19.4 Retrieval Strategies

Support:

- Vector-only semantic search.
- Keyword-only search.
- Hybrid search.
- Metadata-filtered search.
- Multi-query retrieval.
- Query rewrite then retrieval.

Recommended progression:

1. Start with vector-only search.
2. Add metadata filters.
3. Add hybrid search.
4. Add reranking.
5. Add retrieval evaluation.

### 19.5 Retrieval Debugging

For every search, store or expose:

- Query text.
- Rewritten query.
- Filters.
- Top retrieved chunks.
- Scores.
- Reranked scores.
- Included/excluded context.

This is required because RAG failures often come from retrieval, not answer generation.

### 19.6 Embedding Model Selection Depth

Embedding quality controls retrieval quality. The platform should compare embedding models instead of treating embeddings as a fixed commodity.

Track for each embedding model:

```text
model_name
dimension
provider
max_input_tokens
language_support
cost_per_1k_tokens
latency_profile
normalization_required
supports_matryoshka
supports_quantization
recommended_distance_metric
```

Selection criteria:

- Domain quality on evaluation set.
- Latency.
- Cost.
- Dimension size.
- Multilingual performance.
- Compatibility with vector store.
- Ability to support quantization or truncation.

### 19.7 Matryoshka Embeddings

Matryoshka embeddings are embeddings trained so shorter prefix dimensions can still perform well.

Use case:

- Store full dimension for high-quality retrieval.
- Experiment with shorter dimensions for lower memory and faster search.
- Support tiered retrieval where cheap search runs first and richer search runs later.

Implementation requirements:

- Store `embedding_dimension_used` separately from model full dimension.
- Evaluation must compare recall/latency/cost across dimensions.
- Do not change dimension without reindexing or separate index metadata.

### 19.8 Embedding Quantization

Quantization reduces memory and can improve search speed.

Types:

```text
float32
float16
int8
binary
product quantization depending on vector DB
```

Use case:

- Large vector indexes.
- Lower-cost retrieval.
- Memory-constrained environments.

Risks:

- Lower recall.
- Lower ranking quality.
- More difficult debugging.

Implementation rule:

Quantized indexes must be evaluated against full-precision baseline before promotion.

### 19.9 Vector Index Tuning

Vector index settings affect recall, latency, and cost.

HNSW concepts:

```text
m: graph connectivity
 ef_construction: build-time search depth
 ef_search: query-time search depth
```

Tradeoff:

```text
higher ef_search -> better recall, slower latency
lower ef_search -> faster latency, lower recall risk
```

IVF concepts:

```text
lists or clusters
probe count
training data quality
```

Implementation requirements:

- Store index configuration version.
- Benchmark recall and p95 latency.
- Evaluate by tenant-scale dataset.
- Keep index rebuild process documented.

Suggested table:

```text
vector_index_versions
  id
  tenant_id nullable
  vector_store_name
  embedding_model
  dimension
  index_type
  index_params_json
  status
  created_at
```

### 19.10 Late-Interaction Retrieval

Late-interaction retrieval, such as ColBERT-style retrieval, scores token-level interactions instead of only one dense vector per chunk.

Use case:

- Higher retrieval precision.
- Complex technical documents.
- Queries where exact token-level evidence matters.

Tradeoffs:

- More storage.
- More compute.
- More complex serving.

Atlas should treat late-interaction retrieval as an advanced retrieval plugin behind the same retrieval interface.

### 19.11 Embedding Evaluation Requirements

Embedding changes must be evaluated with:

- Recall at K.
- MRR.
- Query latency p50/p95.
- Index size.
- Cost per 1,000 queries.
- Performance by document type.
- Performance by language if multilingual.

No embedding model or index change should be promoted based only on intuition.

## 20. RAG Design

RAG means retrieval augmented generation. The system retrieves relevant private knowledge and gives it to the LLM so answers are grounded.

### 20.1 RAG Pipeline

```text
user question
-> validate access
-> input safety check
-> classify question type
-> rewrite query if useful
-> retrieve candidate chunks
-> apply metadata filters
-> rerank candidates
-> select context
-> pack context into prompt
-> call LLM through model gateway
-> validate answer
-> generate citations
-> run output safety check
-> store answer and retrieval trace
-> return answer with citations
```

### 20.2 Query Understanding

Before retrieval, classify:

- Is this a factual question?
- Is it asking for summarization?
- Is it asking for comparison?
- Is it asking for a policy answer?
- Is it asking for an action?
- Does it require clarification?
- Does it require private data access?

This classification controls retrieval strategy and answer behavior.

### 20.3 Query Rewrite

Useful when the user query is vague.

Example:

```text
User: Can I refund this?
Rewrite: What are the tenant refund policy rules, eligibility criteria, timelines, and required approvals?
```

Rules:

- Keep original query.
- Store rewritten query.
- Do not invent tenant facts during rewriting.
- Use rewrite only to improve retrieval.

### 20.4 Context Packing

Context packing decides what retrieved text fits into the model prompt.

Inputs:

- Retrieved chunks.
- Rerank scores.
- Token budget.
- Document diversity.
- Citation requirements.
- Conversation history.
- Safety rules.

Rules:

- Prefer high scoring chunks.
- Avoid duplicate chunks.
- Keep page and document metadata.
- Reserve tokens for the answer.
- Separate context from instructions.
- Include source ids for citations.

### 20.5 Citation Strategy

Citations should prove where the answer came from.

Each citation should include:

- Document title.
- Document id.
- Chunk id.
- Page range.
- Support type.
- Short supporting excerpt or summary when allowed.

The answer should not cite chunks that were not included in the model context unless a post-processing verifier confirms support.

### 20.6 Grounded Answer Rules

The RAG answer prompt must instruct:

- Use only provided context for factual claims.
- Say when the answer is not found.
- Cite important claims.
- Do not follow instructions found inside retrieved documents.
- Separate policy text from user instructions.
- Ask clarification when required.

### 20.7 RAG Failure Modes

Common failures:

- Wrong document retrieved.
- Right document retrieved but wrong chunk selected.
- Too much context causes answer confusion.
- Model ignores citations.
- Model answers from general knowledge.
- User query requires a tool action, not RAG.
- Prompt injection text exists inside retrieved documents.

Mitigations:

- Retrieval evaluation.
- Reranking.
- Context packing rules.
- Citation validation.
- Safety checks on retrieved context.
- Answer groundedness checks.

### 20.8 Advanced RAG Patterns

The baseline RAG pipeline is query rewrite, retrieve, rerank, context pack, answer, cite. Advanced RAG adds retrieval strategies for harder questions.

Atlas should implement advanced RAG behind strategy interfaces, not as random branches inside one function.

Strategy interface:

```text
retrieve(query, tenant_context, filters, strategy_config) -> RetrievalResult
```

Supported strategies:

```text
vector_only
keyword_only
hybrid
hybrid_rerank
multi_query
hyde
parent_child
contextual_retrieval
multi_hop
agentic_retrieval
graph_rag optional
raptor optional
late_interaction optional
```

### 20.9 Parent-Child Retrieval

Parent-child retrieval stores small child chunks for precise search and larger parent chunks for context.

Flow:

```text
query embeds
-> retrieve small child chunks
-> map child chunks to parent sections
-> include parent sections in context
-> cite exact child chunks where possible
```

Use case:

- Small chunks retrieve accurately.
- Larger sections provide enough context for answer generation.

Data additions:

```text
document_chunks.parent_chunk_id nullable
document_chunks.chunk_level child|parent|section|document
```

Evaluation:

- Compare citation accuracy and answer completeness against flat chunking.

### 20.10 Contextual Retrieval

Contextual retrieval enriches chunks with generated context before embedding.

Example:

```text
Original chunk: "Refunds above this amount need approval."
Contextualized chunk: "In the enterprise refund policy, refunds above the configured approval threshold need manager approval."
```

Flow:

```text
chunk created
-> context generation prompt sees document title/section
-> contextual summary created
-> embedding text = contextual summary + chunk text
-> original chunk remains citation source
```

Rules:

- Store generated context separately.
- Do not cite generated context as source truth.
- Evaluate retrieval lift before enabling broadly.

### 20.11 HyDE Retrieval

HyDE means hypothetical document embedding.

Flow:

```text
user query
-> LLM writes a hypothetical answer/document
-> embed hypothetical text
-> retrieve chunks similar to hypothetical text
-> answer using real retrieved chunks only
```

Use case:

- Short or vague questions.
- Questions where direct query embedding performs poorly.

Risks:

- Hypothetical text can bias retrieval.
- Cost increases.
- Not always better than query rewrite.

Rule:

HyDE output is retrieval helper text, not evidence.

### 20.12 Multi-Hop Retrieval

Multi-hop retrieval handles questions requiring multiple pieces of evidence.

Example:

```text
Which enterprise refund rule applies if the customer is in region X and the ticket is older than 30 days?
```

Flow:

```text
classify as multi-hop
-> decompose question into subquestions
-> retrieve for each subquestion
-> rerank combined evidence
-> synthesize answer with citations per claim
```

Implementation objects:

```text
rag_query_subquestions
  id
  rag_query_id
  subquestion
  retrieval_result_id
```

Evaluation:

- Score per subquestion retrieval success.
- Score final answer correctness.
- Score citation coverage per claim.

### 20.13 GraphRAG And RAPTOR As Optional Advanced Strategies

GraphRAG builds graph relationships among entities, documents, and concepts. RAPTOR-style retrieval builds hierarchical summaries for retrieval at multiple abstraction levels.

Atlas should treat these as optional advanced retrieval strategies.

Use GraphRAG when:

- Documents contain many linked entities.
- Questions require relationship traversal.
- Knowledge graph adds measurable value.

Use RAPTOR-style hierarchy when:

- Corpus is large.
- Questions need both summary-level and detail-level retrieval.
- Multi-level abstraction improves answer quality.

Required proof before adopting:

- Better eval scores than hybrid rerank baseline.
- Acceptable index build complexity.
- Explainable citations back to source chunks.

### 20.14 ACL-Filtered Retrieval

Access control must apply inside retrieval.

Rules:

- Every vector search includes tenant filter.
- Every document collection check enforces user permissions.
- Restricted documents are excluded before reranking.
- Agent retrieval uses agent identity and user delegation rules.
- Cached results must include permission scope.

Failure to apply ACL filtering is a data breach, not a retrieval bug.

### 20.15 Citation Verification

Citation verification checks whether cited chunks actually support answer claims.

Flow:

```text
answer generated
-> split answer into claims
-> map claims to cited chunks
-> verifier checks support level
-> unsupported claims removed, corrected, or flagged
```

Support labels:

```text
fully_supported
partially_supported
unsupported
contradicted
```

Promotion rule:

RAG prompt or retriever changes cannot be promoted if citation accuracy drops below threshold.

### 20.16 Retrieval Deletion And Reindex Safety

RAG must respect document lifecycle.

When documents change:

- Inactive chunks are excluded from retrieval.
- Embeddings are regenerated for changed chunks.
- Vector points are deleted or tombstoned.
- Retrieval cache is invalidated.
- Eval cases referencing old source versions are marked stale.

Implementation requirement:

Store a `knowledge_index_version` per collection and include it in cache keys, RAG traces, and eval reports.

## 21. Tool Calling Design

Tool calling lets models request structured actions, but the application controls execution.

### 21.1 Tool Categories

Read-only tools:

```text
search_documents
get_document
search_tickets
get_customer_profile
get_order_status
calculate_refund_estimate
```

Write-action tools:

```text
create_ticket_note
update_ticket_status
draft_email
send_email
create_escalation
assign_ticket
create_task
```

Internal tools:

```text
run_rag_query
run_safety_check
create_eval_case
summarize_conversation
```

Human tools:

```text
request_approval
ask_user_clarification
handoff_to_human
```

### 21.2 Tool Definition Requirements

Every tool must define:

- Name.
- Description.
- Input schema.
- Output schema.
- Required permissions.
- Risk level.
- Approval requirement.
- Timeout.
- Idempotency behavior.
- Audit fields.
- Dry-run support where possible.

### 21.3 Tool Execution Flow

```text
model suggests tool call
-> application validates tool name
-> application validates arguments against schema
-> application checks user permissions
-> application checks tenant boundaries
-> application checks safety policy
-> if write/risky, create approval request
-> if approved or safe, execute tool
-> store tool call record
-> return tool result to agent or user
```

### 21.4 Tool Safety Rules

Rules:

- The model cannot call arbitrary code.
- The model can only select registered tools.
- Tool arguments must validate.
- Tools must enforce permissions independently of the model.
- Write tools should support dry-run.
- Risky tools require approval.
- Tool output should be sanitized before returning to the model.

### 21.5 MCP Integration Design

MCP, or Model Context Protocol, should be treated as a first-class external tool and context integration pattern.

Definition:

MCP standardizes how AI applications connect to external tools, resources, prompts, and context providers. In Atlas, MCP should not bypass the existing tool governance model. MCP servers become external capability providers that are registered, permissioned, audited, and controlled by the application.

Architecture:

```text
Agent Orchestrator
-> Tool Service
-> MCP Adapter
-> Registered MCP Server
-> MCP Tool/Resource/Prompt
-> Result returned to Tool Service
-> Safety and audit checks
-> Result returned to Agent
```

### 21.6 MCP Server Registry

Suggested table:

```text
mcp_servers
  id
  tenant_id nullable
  name
  description
  transport_type
  connection_config_ref
  allowed_scopes
  status
  version
  created_at
  updated_at
```

Transport examples:

```text
stdio
http_sse
streamable_http
local_process
remote_gateway
```

Registry rules:

- MCP servers must be explicitly registered.
- MCP servers must be disabled by default until reviewed.
- Tenant-specific MCP servers cannot be visible to other tenants.
- Connection secrets must be stored in secret manager, not database plaintext.
- MCP server versions and tool schemas should be snapshotted.

### 21.7 MCP Tool Discovery And Schema Mapping

Flow:

```text
admin registers MCP server
-> Atlas connects in discovery mode
-> lists available tools/resources/prompts
-> maps MCP tools into Atlas tool_definitions
-> stores schema snapshot
-> marks tools pending approval
-> admin enables approved tools
```

Schema mapping requirements:

- Convert MCP tool input schema into Atlas tool input schema.
- Store original schema and normalized schema.
- Require a risk level for each tool.
- Require permission mapping for each tool.
- Require approval policy for write-capable tools.

Suggested table:

```text
mcp_tool_mappings
  id
  tenant_id
  mcp_server_id
  tool_definition_id
  mcp_tool_name
  schema_snapshot_json
  normalized_schema_json
  risk_level
  enabled
  created_at
  updated_at
```

### 21.8 MCP Security Rules

MCP tools are powerful and must be controlled.

Rules:

- The LLM cannot connect to arbitrary MCP servers.
- Only registered MCP servers are available.
- Only enabled MCP tools are exposed to agents.
- Tool calls still pass through Atlas permission checks.
- Write-capable MCP tools require approval unless explicitly allowed.
- MCP tool results are treated as untrusted data before being placed back into model context.
- MCP server errors are isolated and do not crash the agent orchestrator.
- MCP server credentials are scoped by tenant and use case.
- Tool schema changes trigger review before use.

### 21.9 MCP Audit And Disablement

Audit every MCP event:

- Server registered.
- Server disabled.
- Tool discovered.
- Tool enabled.
- Tool schema changed.
- Tool called.
- Tool failed.
- Tool result blocked by safety.

Emergency controls:

- Disable one MCP tool.
- Disable one MCP server.
- Disable MCP for one tenant.
- Disable MCP globally.
- Revoke MCP credentials.

### 21.10 MCP Testing

Tests:

- Mock MCP server returns tool list.
- Tool schema maps correctly.
- Unauthorized MCP tool call fails.
- Disabled MCP server cannot be called.
- Changed MCP schema requires review.
- MCP result with prompt injection is sanitized.
- Write MCP tool creates approval request.

Portfolio proof:

- Register a sample MCP server.
- Import one read-only tool.
- Import one write tool.
- Run agent using read-only MCP tool.
- Show approval flow for write MCP tool.
- Show audit trace.

## 22. Agent Orchestration Design

An agent is a controlled workflow that uses an LLM plus application state, tools, retrieval, memory, verification, and approval gates.

### 22.1 Agent Modes

Atlas should support three modes:

```text
assistive
supervised
autonomous_limited
```

Assistive:

- Agent suggests next steps.
- Human executes actions.

Supervised:

- Agent can prepare actions.
- Human approves writes.

Autonomous limited:

- Agent can execute low-risk actions within strict limits.
- High-risk actions still require approval.

### 22.2 Agent State Machine

Recommended state machine:

```text
created
-> classify_task
-> check_permissions
-> retrieve_context
-> create_plan
-> validate_plan
-> execute_next_step
-> if tool_needed: validate_tool_call
-> if approval_needed: wait_for_approval
-> run_tool
-> observe_tool_result
-> verify_progress
-> continue_or_finish
-> final_response
-> complete
```

Failure states:

```text
blocked
failed
cancelled
expired
```

### 22.3 Agent Planning

Agent plan should be structured.

Fields:

```text
goal
assumptions
steps
required_tools
risk_level
approval_points
success_criteria
fallback_plan
```

Rules:

- Plans must be validated before execution.
- Plans should be short enough to inspect.
- Plans should not include tools the agent is not allowed to use.
- Plans should identify approval points before action.

### 22.4 Agent Execution Loop

```text
load agent run
-> load current state
-> choose next step
-> if retrieval needed, call RAG/retrieval service
-> if model reasoning needed, call model gateway
-> if tool needed, call tool service
-> store step result
-> verify result
-> decide continue/finish/block
```

Limits:

- Max steps.
- Max tool calls.
- Max cost.
- Max runtime.
- Max repeated failures.

### 22.5 Agent Verification

Verification checks:

- Did the tool call succeed?
- Did the output match the schema?
- Did the action solve the intended subtask?
- Is the result consistent with retrieved evidence?
- Is another step needed?
- Did the agent exceed limits?

### 22.6 Agent Trace Viewer

The frontend should show:

- User task.
- Agent plan.
- Each step.
- Model calls.
- Tool calls.
- Approvals.
- Errors.
- Final result.
- Cost and latency.

This is important for debugging and interviews.

### 22.7 Agent Identity And Scoped Credentials

An agent must have an identity boundary. It should not inherit unlimited user power.

Identity model:

```text
human user
-> delegates task to agent
-> agent run receives scoped execution context
-> tools execute with least-privilege credentials
-> risky actions require human approval
```

Agent execution context should include:

```text
agent_run_id
tenant_id
initiating_user_id
agent_definition_id
allowed_tools
allowed_collections
allowed_external_scopes
max_cost_usd
max_steps
approval_policy
expires_at
```

Rules:

- Agent credentials expire.
- Agent scope is narrower than or equal to user permissions.
- Agent cannot grant itself new tools.
- Agent cannot change its own approval policy.
- Agent cannot access hidden system prompts or secrets as tool context.

### 22.8 Tool Sandboxing And Failure Containment

Agent tool execution should be isolated.

Controls:

- Execute tools through Tool Service only.
- Apply timeout per tool.
- Apply retries only for idempotent tools.
- Use dry-run for write tools where possible.
- Sanitize tool output before sending back to model.
- Store tool input/output with redaction rules.
- Stop agent after repeated tool failures.

Failure containment:

```text
tool fails
-> record tool_call failed
-> verifier decides retry, alternative tool, ask human, or block
-> agent state updates explicitly
```

### 22.9 Multi-Agent Orchestration

Multi-agent orchestration is an advanced pattern where multiple specialized agents collaborate under controlled rules.

Do not start with multi-agent systems. Build single controlled agents first. Add multi-agent orchestration only when there is a real need.

Patterns:

```text
supervisor_agent -> delegates to worker agents
planner_agent -> creates plan, executor_agent -> executes
research_agent -> retrieves evidence, writer_agent -> drafts answer, verifier_agent -> checks result
triage_agent -> routes task to specialist agent
```

Architecture:

```text
User task
-> Supervisor Agent
-> task decomposition
-> specialist agent assignment
-> each specialist runs with scoped tools
-> results returned to supervisor
-> verifier checks final output
-> human approval if needed
-> final answer/action
```

Required controls:

- Supervisor cannot bypass tenant/user permissions.
- Specialist agents receive limited context only.
- Agent-to-agent messages are logged.
- Each agent has max steps and cost budget.
- Final verifier checks consistency and evidence.
- Human approval still gates risky actions.

Suggested tables:

```text
agent_collaborations
  id
  tenant_id
  parent_agent_run_id
  pattern
  status
  created_at

agent_handoffs
  id
  collaboration_id
  from_agent_run_id
  to_agent_run_id
  handoff_reason
  context_summary
  status
  created_at
```

### 22.10 Agent-To-Agent Communication Rules

Agent-to-agent messages are not free-form hidden magic. They are structured handoffs.

Handoff schema:

```text
source_agent
 target_agent
 task
 context_summary
 evidence_refs
 constraints
 allowed_tools
 expected_output_schema
 deadline_or_step_limit
```

Rules:

- Do not pass unnecessary raw private data.
- Pass references to evidence where possible.
- Record every handoff.
- Validate output from specialist agent before supervisor uses it.
- Prevent loops between agents.

### 22.11 Multi-Agent Evaluation

Evaluate:

- End-to-end task success.
- Correct specialist selection.
- Handoff clarity.
- Tool misuse rate.
- Cost compared with single-agent baseline.
- Latency compared with single-agent baseline.
- Final answer correctness.
- Approval policy compliance.

Promotion rule:

Multi-agent orchestration should be kept only if it improves quality or maintainability enough to justify cost and complexity.

## 23. Memory Design

Memory improves continuity, but it is risky if uncontrolled.

### 23.1 Memory Types

Short-term memory:

- Conversation messages.
- Current task state.
- Recent tool results.

Long-term memory:

- User preferences.
- Tenant policies.
- Reusable workflow notes.
- Stable facts approved for storage.

Derived memory:

- Conversation summaries.
- Ticket summaries.
- Agent progress summaries.

### 23.2 Memory Write Rules

Memory should be written only when:

- User explicitly asks to remember something.
- Policy allows the memory type.
- The information is useful beyond the current conversation.
- Sensitive data rules allow storage.

Do not store:

- Secrets.
- Passwords.
- Payment details.
- Unnecessary PII.
- Sensitive personal details unless policy explicitly allows it.

### 23.3 Memory Retrieval Rules

Memory retrieval should be scoped by:

- Tenant.
- User.
- Conversation.
- Agent.
- Permission.
- Relevance.
- Expiration.

Memory must not leak across tenants.

### 23.4 Memory Summarization

Long conversations should be summarized.

Flow:

```text
conversation grows past token threshold
-> summarize older messages
-> store summary with source message range
-> use summary plus recent messages in future prompts
```

Rules:

- Keep summary traceable.
- Do not summarize away important decisions.
- Do not include unsafe or disallowed memory.

## 24. Safety And Guardrails Design

Safety must exist throughout the system, not only after the model response.

### 24.1 Safety Check Points

Checkpoints:

```text
user input
retrieved documents
prompt construction
tool call request
tool call result
model output
memory write
evaluation dataset creation
fine-tuning dataset creation
```

### 24.2 Prompt Injection Defense

Prompt injection can come from:

- User input.
- Uploaded documents.
- Web pages.
- Tool outputs.
- Emails or tickets.
- Retrieved context.

Defenses:

- Separate instructions from data.
- Mark retrieved context as untrusted data.
- Use system prompts that tell the model not to follow context instructions.
- Run injection checks on retrieved chunks.
- Restrict tool permissions.
- Validate tool calls outside the model.
- Require approval for risky writes.
- Log suspicious attempts.

### 24.3 PII And Sensitive Data

PII handling:

- Detect common PII types.
- Redact where required.
- Avoid sending sensitive data to providers when policy disallows it.
- Store redaction metadata.
- Control access by tenant and role.
- Apply retention rules.

PII examples:

```text
email
phone
address
national id
passport
payment data
health information
personal customer notes
```

### 24.4 Output Safety

Output checks:

- Harmful content.
- Disallowed legal/medical/financial advice depending on product policy.
- Unsupported factual claims.
- Missing citations in RAG mode.
- PII leakage.
- Tool instruction leakage.
- Internal prompt leakage.

### 24.5 Approval Gates

Approval required for:

- Sending external emails.
- Updating customer records.
- Closing tickets.
- Issuing refunds.
- Deleting data.
- Exporting sensitive data.
- Running high-cost operations.
- Deploying model changes.

Approval record should include:

- What action is requested.
- Why the agent wants it.
- Input parameters.
- Risk summary.
- Evidence.
- Reviewer decision.

### 24.6 AI Threat Model

Atlas must include an explicit AI threat model. This is different from ordinary web security because LLM systems can be manipulated through text, retrieved documents, tool outputs, memory, and agent workflows.

Threat categories:

```text
prompt injection
indirect prompt injection from documents/tool outputs
sensitive information disclosure
data exfiltration through model responses
insecure output handling
excessive agency
tool misuse
agent identity abuse
memory poisoning
retrieval poisoning
model denial of service through long inputs
supply-chain risk from external tools/MCP servers
unsafe generated media
training data contamination
model/provider policy mismatch
```

### 24.7 Threat-To-Control Matrix

Prompt injection:

```text
control: separate instructions from data
control: treat retrieved context as untrusted
control: run input/context checks
control: validate tool calls outside model
proof: red-team prompts cannot override system policy
```

Data exfiltration:

```text
control: tenant filters
control: role permissions
control: retrieval ACLs
control: output PII checks
proof: cross-tenant retrieval tests fail safely
```

Tool misuse:

```text
control: registered tools only
control: schema validation
control: approval gates
control: idempotency keys
proof: unauthorized tool calls are rejected and audited
```

Memory poisoning:

```text
control: memory write policy
control: sensitive-data filters
control: memory review and expiration
proof: malicious user cannot store system-changing instructions as memory
```

MCP supply-chain risk:

```text
control: MCP server registry
control: schema snapshot review
control: tool disablement
control: scoped credentials
proof: changed MCP schema cannot run without review
```

Unsafe generated media:

```text
control: prompt safety check
control: output safety check
control: watermark/provenance metadata where supported
control: human review for sensitive media
proof: disallowed generation requests are blocked
```

### 24.8 Red-Team Test Catalog

Maintain a red-team dataset with categories:

```text
direct prompt injection
indirect prompt injection in document
indirect prompt injection in tool result
jailbreak attempts
system prompt extraction attempts
cross-tenant data access attempts
PII extraction attempts
unsafe tool action attempts
approval bypass attempts
memory poisoning attempts
MCP tool abuse attempts
RAG citation manipulation attempts
generated media policy violations
voice impersonation attempts
```

Each red-team case should include:

```text
input
attack_type
expected_defense
expected_response
severity
related_policy
result
reviewer_notes
```

### 24.9 Safety Engineering Gates

Before production release:

- Red-team suite passes required threshold.
- No known critical prompt-injection bypass exists.
- Cross-tenant data access tests pass.
- Tool approval bypass tests pass.
- PII leakage tests pass.
- Unsafe generated media tests pass where media generation is enabled.
- Incident escalation process is documented.

## 25. Evaluation Platform Design

Evaluation is how the team proves quality.

### 25.1 Evaluation Types

Support:

- Prompt evaluation.
- Structured output evaluation.
- RAG retrieval evaluation.
- RAG answer evaluation.
- Agent task evaluation.
- Tool-call evaluation.
- Safety evaluation.
- Fine-tuning evaluation.
- Model serving evaluation.
- Latency and cost evaluation.

### 25.2 Golden Datasets

Golden datasets should include:

- Input.
- Expected output.
- Reference context.
- Tags.
- Difficulty level.
- Source of example.
- Known failure reason if added from bug reports.

Sources:

- Hand-written examples.
- Production failures after redaction.
- User feedback.
- Synthetic examples reviewed by humans.
- Red-team cases.

### 25.3 RAG Metrics

Retrieval metrics:

- Recall at K.
- Precision at K.
- Mean reciprocal rank.
- Hit rate.
- Context relevance.

Answer metrics:

- Correctness.
- Groundedness.
- Citation accuracy.
- Completeness.
- Refusal correctness.
- Helpfulness.

### 25.4 Agent Metrics

Agent metrics:

- Task success rate.
- Step count.
- Tool success rate.
- Invalid tool call rate.
- Approval rate.
- Rejection rate.
- Cost per task.
- Latency per task.
- Recovery from tool errors.

### 25.5 Safety Metrics

Safety metrics:

- Prompt injection detection rate.
- Unsafe output block rate.
- False positive rate.
- PII leakage rate.
- Approval bypass attempts.
- Policy violation rate.

### 25.6 Regression Evaluation

Before activating a new prompt, retriever, model, agent, or safety policy, run regression tests.

Compare:

```text
baseline version vs candidate version
```

Track:

- Overall score.
- Score by tag.
- New failures.
- Fixed failures.
- Cost difference.
- Latency difference.

Deployment rule:

- Do not promote a change if quality falls below threshold or safety failures increase.

### 25.7 Evaluation Dataset Format

Every evaluation dataset should be stored in a structured format.

Recommended JSONL format:

```json
{"case_id":"case_001","use_case":"rag_answer","input":{"question":"What is the refund approval threshold?","collection_ids":["col_policy"]},"reference":{"answer":"Refunds above the configured threshold require manager approval.","required_sources":["doc_refund_policy_v2"],"required_facts":["manager approval required above threshold"]},"tags":["refund","policy","citation_required"],"difficulty":"medium"}
```

Required fields:

```text
case_id
use_case
input
reference
tags
difficulty
created_from
review_status
```

Use-case-specific references:

- RAG: required sources, required facts, forbidden unsupported claims.
- Structured output: expected JSON fields and allowed values.
- Agent: expected final state, allowed tools, forbidden tools, approval expectations.
- Safety: expected block/allow decision and policy reason.
- Media generation: expected prompt compliance, policy constraints, quality rubric.

### 25.8 Scoring Rubrics

Each scorer must have a rubric.

Correctness rubric:

```text
5 = fully correct and complete
4 = mostly correct with minor omission
3 = partially correct but missing important detail
2 = mostly incorrect
1 = incorrect or misleading
0 = no useful answer
```

Groundedness rubric:

```text
5 = every factual claim supported by provided context
4 = nearly all important claims supported
3 = mixed supported and unsupported claims
2 = mostly unsupported
1 = hallucinated answer
0 = unsafe or fabricated answer
```

Citation accuracy rubric:

```text
5 = citations directly support all key claims
4 = citations support most key claims
3 = citations are relevant but incomplete
2 = citations weakly related
1 = citations wrong
0 = no citations when required
```

Tool-use rubric:

```text
5 = correct tool, valid arguments, correct timing
4 = correct tool with minor inefficiency
3 = correct general direction but incomplete
2 = unnecessary or weak tool use
1 = wrong tool
0 = unsafe or unauthorized tool attempt
```

### 25.9 Judge Calibration

LLM-as-judge must be calibrated.

Calibration process:

```text
select representative eval cases
-> humans score cases independently
-> judge scores same cases
-> compare agreement
-> adjust rubric or judge prompt
-> lock judge prompt version
-> rerun calibration periodically
```

Track:

- Human/judge agreement.
- Disagreement by tag.
- Judge bias toward longer answers.
- Judge sensitivity to citations.
- Judge consistency across reruns.

Rules:

- Do not trust judge scores without sampling human review.
- Use deterministic settings when possible.
- Store judge prompt version and model version.

### 25.10 Promotion Thresholds

A candidate prompt, model, retriever, or agent should not be promoted without thresholds.

Example RAG thresholds:

```text
correctness_average >= 4.0/5
groundedness_average >= 4.2/5
citation_accuracy_average >= 4.2/5
unsafe_output_rate = 0 critical cases
p95_latency <= 8 seconds
cost_per_answer <= configured budget
no regression greater than 5% on critical tags
```

Example agent thresholds:

```text
task_success_rate >= 85%
invalid_tool_call_rate <= 2%
approval_bypass_rate = 0%
max_steps_exceeded_rate <= 5%
critical_safety_failures = 0
```

### 25.11 Bias, Fairness, And Toxicity Evaluation

Responsible AI evaluation should include more than prompt injection and PII.

Evaluate:

- Toxicity.
- Stereotyping.
- Unfair treatment across user groups.
- Unequal refusal behavior.
- Biased prioritization or routing.
- Language and dialect robustness.
- Accessibility of generated content.

Implementation requirements:

- Add fairness/toxicity tags to eval datasets.
- Include sensitive attribute handling policy.
- Avoid collecting sensitive attributes unless legally and ethically justified.
- Review high-impact workflows manually.

### 25.12 Human Review Flow

Human review is required for:

- New eval dataset approval.
- Judge calibration sample.
- Safety critical failures.
- Prompt/model promotion.
- High-risk agent behavior.
- Generated media policy edge cases.

Human review records should store:

```text
reviewer_user_id
subject_type
subject_id
decision
score_override optional
notes
created_at
```

## 26. Fine-Tuning And Model Adaptation Design

Fine-tuning is not the first answer to most Gen AI problems. Atlas should use fine-tuning only when there is evidence that prompting, RAG, structured outputs, and routing are not enough.

### 26.1 When Fine-Tuning Is Useful

Use fine-tuning for:

- Stable output style.
- Repeated structured extraction patterns.
- Domain-specific classification.
- Tool-use behavior when enough examples exist.
- Smaller model adaptation for cost reduction.

Do not use fine-tuning to store frequently changing facts. Use RAG for that.

### 26.2 Fine-Tuning Workflow

```text
collect candidate examples
-> filter sensitive data
-> normalize format
-> split train/validation/test
-> create baseline evaluation
-> train adapter or fine-tuned model
-> evaluate against baseline
-> safety test
-> cost and latency test
-> register model
-> deploy to staging
-> canary or limited production route
-> monitor
```

### 26.3 Dataset Requirements

Dataset examples should include:

- Input.
- Desired output.
- Task type.
- Source.
- Human review status.
- Safety labels.
- Version.

Dataset quality matters more than dataset size.

### 26.4 LoRA And QLoRA

Use LoRA or QLoRA when adapting open models efficiently.

Track:

- Base model.
- Adapter version.
- Training config.
- Dataset version.
- Evaluation result.
- Safety result.
- Deployment status.

### 26.5 Model Registry

Model registry should store:

- Model name.
- Version.
- Base model.
- Adapter path.
- Training dataset.
- Metrics.
- Approval status.
- Deployment target.
- Rollback version.

### 26.6 Managed Provider Fine-Tuning Vs Open-Model Adaptation

Fine-tuning has two major paths.

Managed provider fine-tuning:

```text
training examples prepared
-> uploaded to provider
-> provider fine-tuning job runs
-> managed fine-tuned model id returned
-> gateway routes selected traffic to managed fine-tuned model
```

Pros:

- Less infrastructure.
- Easier deployment.
- Provider handles serving.
- Good first fine-tuning path for many teams.

Cons:

- Less control.
- Provider-specific format.
- Data-sharing/legal review required.
- Limited architecture customization.

Open-model adaptation:

```text
base open model selected
-> dataset prepared
-> LoRA/QLoRA training runs
-> adapter artifact stored
-> model evaluated
-> model served through local or cloud endpoint
```

Pros:

- More control.
- Can optimize cost at scale.
- Can run in private infrastructure.
- Useful for specialized behavior.

Cons:

- Requires ML infrastructure.
- Requires GPU access.
- Serving and monitoring are harder.
- More operational burden.

Recommended learning path:

1. Understand when fine-tuning is needed.
2. Try managed provider fine-tuning first when available and allowed.
3. Add LoRA/QLoRA open-model adaptation as advanced depth.
4. Serve open/adapted model only after evaluation proves value.

### 26.7 Model Distillation

Model distillation trains or adapts a smaller model to imitate a stronger model or system.

Use cases:

- Reduce cost.
- Reduce latency.
- Move repeated classification/extraction away from expensive models.
- Create a smaller domain model for stable tasks.

Distillation flow:

```text
strong teacher model or best current pipeline produces outputs
-> human review or filtering cleans examples
-> student dataset created
-> smaller model trained or fine-tuned
-> student evaluated against teacher and human references
-> student deployed only for matching use case
```

Risks:

- Student copies teacher mistakes.
- Synthetic labels may be low quality.
- Distilled model may fail out-of-distribution.
- Legal/provider terms must allow generated outputs for training.

Data additions:

```text
distillation_jobs
  id
  tenant_id
  teacher_model
  student_base_model
  dataset_id
  status
  metrics_json
  created_at
```

Promotion criteria:

- Student must meet quality threshold.
- Student must be cheaper or faster enough to justify maintenance.
- Safety performance must not regress.

## 27. Model Serving And LLMOps Design

Model serving is needed when the platform hosts open or adapted models.

### 27.1 Serving Options

Options:

- Managed provider only.
- Local development server with Ollama or similar tooling.
- vLLM for production-style open model serving.
- Text Generation Inference for Hugging Face model serving.
- Cloud model endpoint.

Recommended path:

1. Start with managed providers through model gateway.
2. Add local open model testing later.
3. Add vLLM or managed endpoint when fine-tuned models need serving.

### 27.2 Serving Concerns

Serving must handle:

- Model loading time.
- GPU memory.
- Batching.
- Concurrency.
- Timeout.
- Queueing.
- Streaming.
- Health checks.
- Rollback.
- Cost tracking.
- Version routing.

### 27.3 Model Deployment Flow

```text
model registered
-> staging deployment created
-> smoke tests run
-> eval suite runs
-> safety tests run
-> canary route enabled
-> metrics monitored
-> production route increased
-> old model kept for rollback
```

### 27.4 Inference Quantization

Inference quantization reduces memory and can improve serving cost and latency.

Common serving formats and methods:

```text
FP16 or BF16 for common GPU inference
INT8 quantization for memory reduction
INT4 quantization for stronger compression
GPTQ for post-training quantized transformer weights
AWQ for activation-aware quantization
GGUF for local CPU/GPU inference ecosystems
```

Use cases:

- Serving smaller open models locally.
- Reducing GPU memory requirements.
- Increasing throughput.
- Supporting local development without expensive hardware.

Risks:

- Lower output quality.
- Worse structured output reliability.
- Worse multilingual behavior.
- Different latency by hardware.

Promotion rule:

Quantized model deployment must pass the same eval suite as the unquantized baseline, with explicit quality/cost/latency comparison.

### 27.5 Serving Batching And Concurrency

Serving systems must handle concurrent requests.

Concepts:

```text
continuous batching
max batch size
queue timeout
max concurrent requests
KV cache memory
prefill latency
decode latency
```

Implementation requirements:

- Store serving configuration per deployment.
- Expose health endpoint per model deployment.
- Track queue time separately from model time.
- Track p50/p95/p99 latency.
- Reject or shed load when queues exceed limits.

### 27.6 Model Rollback And Canary Routing

Model changes should be deployed gradually.

Flow:

```text
candidate model deployed to staging
-> smoke tests
-> evaluation suite
-> safety suite
-> canary 5% traffic
-> monitor quality/cost/latency/errors
-> increase traffic or rollback
```

Rollback requirements:

- Previous model version remains available.
- Gateway route can switch back quickly.
- AI runs record route version.
- Incident note records reason for rollback.

## 28. Multimodal AI Design

Multimodal AI handles images, scanned documents, screenshots, charts, forms, and visual evidence.

### 28.1 Use Cases

Use cases:

- Extract fields from scanned forms.
- Compare document image with extracted OCR text.
- Understand screenshots from support tickets.
- Classify document images.
- Summarize charts or tables from images.
- Validate visual evidence in claims or support cases.

### 28.2 Multimodal Pipeline

```text
user uploads image or PDF
-> file stored
-> image or page preview generated
-> OCR extracts text where needed
-> vision model analyzes image
-> structured extraction schema validates result
-> confidence and evidence stored
-> human review if low confidence
```

### 28.3 Data To Store

Store:

- Original file.
- Page image.
- OCR text.
- OCR confidence.
- Vision model output.
- Extracted fields.
- Bounding boxes if available.
- Human corrections.

### 28.4 Multimodal Safety

Check:

- Sensitive document images.
- PII in images.
- Unsafe visual content.
- Prompt injection hidden in images or screenshots.
- Mismatch between OCR text and visual extraction.

### 28.5 OCR Confidence And Human Review

OCR output must include confidence and review status.

Fields:

```text
ocr_engine
ocr_engine_version
page_number
text
confidence_score
bounding_boxes_json
requires_review
review_status
reviewer_user_id optional
```

Rules:

- Low-confidence OCR should not silently become trusted RAG context.
- Low-confidence extracted fields should be flagged for review.
- RAG answers using low-confidence OCR should show lower confidence.
- Human corrections should create new document extraction versions.

### 28.6 Bounding-Box Evidence

For scanned documents and images, text evidence should preserve visual location.

Use cases:

- Claims review.
- Invoice extraction.
- Contract review.
- Form processing.

Store:

```text
page_number
x_min
y_min
x_max
y_max
text_span
confidence
field_name optional
```

Frontend should support:

- Highlight cited region on page image.
- Show OCR text and original image side by side.
- Allow human correction.

### 28.7 Table Extraction

Tables require special handling because row/column meaning is easily lost.

Approaches:

- Extract tables as structured data.
- Preserve headers.
- Convert rows to textual chunks with column labels.
- Store raw table JSON.
- Use vision model when normal parser fails.

Example chunk text:

```text
Table: Refund Thresholds. Row: Region = EU, Customer Type = Enterprise, Approval Required = Manager, Threshold = 5000.
```

### 28.8 Image Redaction

Before sending images to external providers, apply policy checks.

Potential redactions:

- Faces.
- IDs.
- addresses.
- signatures.
- payment data.
- account numbers.

Rules:

- Keep redaction metadata.
- Store original only if tenant policy allows.
- Use redacted copy for model calls when required.

## 29. Voice AI Design

Voice AI adds speech-based workflows.

### 29.1 Use Cases

Use cases:

- Transcribe customer support calls.
- Summarize calls.
- Extract action items.
- Detect escalation reasons.
- Draft follow-up notes.
- Convert AI response to speech.
- Build voice assistant workflows.

### 29.2 Voice Pipeline

```text
audio uploaded or streamed
-> speech-to-text transcription
-> optional diarization
-> transcript cleanup
-> summarization
-> extraction of action items
-> safety check
-> storage with conversation
-> optional text-to-speech response
```

### 29.3 Voice Data Concerns

Track:

- Audio file reference.
- Transcript.
- Speaker segments.
- Timestamps.
- Confidence.
- Language.
- Summary.
- Extracted actions.
- Human corrections.

### 29.4 Voice Evaluation

Evaluate:

- Transcription accuracy.
- Speaker attribution.
- Summary correctness.
- Action item extraction.
- Escalation classification.
- Latency.

### 29.5 Realtime Speech-To-Speech

The baseline voice flow is cascaded:

```text
speech-to-text
-> LLM
-> text-to-speech
```

Realtime speech-to-speech can be different because the model may process and generate audio directly or operate over streaming audio tokens.

Use cases:

- Voice assistant.
- Live support copilot.
- Real-time translation.
- Accessibility workflows.

Architecture:

```text
microphone/audio stream
-> realtime session gateway
-> audio input buffer
-> speech activity detection
-> realtime model or STT stream
-> partial transcript/events
-> LLM/tool/RAG calls where needed
-> audio response stream
-> transcript and trace storage
```

Implementation requirements:

- WebSocket or realtime transport.
- Session state tracking.
- Turn detection.
- Interruption handling.
- Low-latency tool/RAG fallbacks.
- Audio retention policy.
- Consent capture.
- Safety checks on transcript and generated audio.

### 29.6 Diarization And Speaker-Aware Summaries

Diarization identifies who spoke when.

Use cases:

- Customer support call review.
- Meeting notes.
- Escalation analysis.

Store:

```text
speaker_id
start_time_ms
end_time_ms
text
confidence
```

Summaries should distinguish:

- Customer complaint.
- Agent response.
- Commitments made.
- Follow-up actions.
- Escalation triggers.

### 29.7 Voice Consent And Retention

Voice data is sensitive.

Controls:

- Capture consent status.
- Store audio retention period.
- Allow transcript retention separate from audio retention.
- Redact sensitive transcript content if policy requires.
- Audit audio access.
- Disable voice workflows for tenants without policy approval.

## 30. Classical ML Design

Classical ML remains important. Not every AI task needs an LLM.

### 30.1 Use Cases

Use classical ML for:

- Ticket priority prediction.
- Churn risk scoring.
- SLA breach prediction.
- Spam or duplicate detection.
- Simple intent classification.
- Routing recommendations.
- Cost anomaly detection.

### 30.2 Classical ML Pipeline

```text
collect labeled data
-> build features
-> split dataset
-> train baseline model
-> evaluate
-> store model artifact
-> expose inference function
-> monitor drift
```

### 30.3 Tools

Use:

- pandas for data processing.
- scikit-learn for baseline models.
- XGBoost or LightGBM when useful.
- MLflow for tracking.
- FastAPI endpoint or internal service for inference.

### 30.4 When Classical ML Beats Gen AI

Use classical ML when:

- Inputs are structured.
- Output is a label or score.
- Latency must be very low.
- Cost must be low.
- Behavior must be highly stable.
- Training data is available.

## 31. Search, Ranking, And Recommendation Design

Search and ranking directly affect RAG quality and user experience.

### 31.1 Hybrid Search

Hybrid search combines:

- Semantic vector search.
- Keyword search.
- Metadata filtering.
- Recency signals.
- Popularity or feedback signals.

### 31.2 Ranking Signals

Potential ranking signals:

- Vector similarity.
- Keyword score.
- Document freshness.
- Source authority.
- User feedback.
- Prior successful citation usage.
- Tenant-specific priority.
- Exact phrase match.

### 31.3 Recommendation Use Cases

Recommendations:

- Suggested documents for a ticket.
- Suggested next actions for an agent.
- Suggested prompt improvements.
- Suggested eval cases from failures.
- Suggested similar incidents.

### 31.4 Evaluation

Evaluate search/ranking with:

- Human-labeled relevant chunks.
- Click feedback.
- Citation usage.
- RAG answer quality.
- Search result satisfaction.


## 32. Generative Media Design

Generative media covers AI systems that create or edit images, video, audio, music, and other synthetic media.

This section exists because enterprise LLM applications are not the full scope of Generative AI. If Atlas claims broad Gen AI coverage, it must include generative media as an optional but real track.

### 32.1 Generative Media Capabilities

Atlas should support or at least architect these capabilities:

```text
text-to-image generation
image-to-image generation
image editing
inpainting
outpainting
image variations
text-to-video generation
video editing or transformation
audio generation
music generation
sound effect generation
voice generation
synthetic data generation
```

Initial implementation should focus on API-based integration rather than training media models from scratch.

### 32.2 Generative Media Architecture

```text
User prompt or source media
-> API validates request
-> safety service checks prompt/media
-> media generation service selects provider/model
-> cost estimate calculated
-> job created
-> worker calls media model provider
-> output stored in object storage
-> output safety check runs
-> metadata/provenance stored
-> user reviews result
-> feedback/evaluation captured
```

Core modules:

```text
packages/media_generation
packages/model_gateway
packages/safety
packages/evals
packages/observability
packages/storage
apps/worker/jobs/media_generation.py
apps/api/routes/media.py
```

### 32.3 Media Generation Tables

Suggested tables:

```text
media_generation_jobs
  id
  tenant_id
  user_id
  media_type
  input_prompt
  input_media_object_key nullable
  provider_name
  model_name
  status
  safety_status
  cost_estimate
  error_message
  created_at
  completed_at

media_assets
  id
  tenant_id
  generation_job_id nullable
  asset_type
  object_key
  mime_type
  width nullable
  height nullable
  duration_ms nullable
  metadata_json
  provenance_json
  created_at

media_safety_checks
  id
  tenant_id
  media_asset_id nullable
  generation_job_id nullable
  check_type
  status
  findings_json
  created_at
```

### 32.4 Text-To-Image Generation

Use cases:

- Create knowledge-base illustrations.
- Generate support training visuals.
- Create product workflow diagrams.
- Create synthetic screenshots for testing.
- Create marketing-safe internal assets if product scope allows.

Request fields:

```text
prompt
negative_prompt optional
style_preset
size
count
seed optional
reference_image optional
safety_options
```

Safety checks:

- No unauthorized real-person likeness.
- No disallowed brand/logo generation.
- No sensitive document reproduction.
- No unsafe content.
- No hidden prompt injection in source image metadata.

Evaluation:

- Prompt adherence.
- Visual quality.
- Safety compliance.
- Brand policy compliance.
- User rating.

### 32.5 Image Editing, Inpainting, And Outpainting

Image editing uses source image plus instruction.

Flow:

```text
source image uploaded
-> image safety and PII scan
-> mask uploaded or generated
-> edit prompt validated
-> model generates edited image
-> output safety check
-> provenance stored
```

Use cases:

- Redact private data from screenshots.
- Produce clean UI examples.
- Modify diagrams.
- Create image variations for training material.

Rules:

- Preserve original asset lineage.
- Never overwrite original image.
- Keep edit instruction and mask reference.
- Store before/after safety checks.

### 32.6 Video Generation

Video generation is more expensive and harder to evaluate than image generation.

Use cases:

- Short workflow demonstration clips.
- Training scenario clips.
- Animated explanation of support processes.
- Synthetic media for internal education.

Data fields:

```text
prompt
reference_image optional
duration_seconds
resolution
fps
style_preset
provider_job_id
output_video_object_key
thumbnail_object_key
```

Evaluation:

- Prompt adherence.
- Temporal consistency.
- Visual artifacts.
- Safety compliance.
- Cost per generation.
- Render time.

Production rule:

Video generation should be asynchronous only. It should never block an API request.

### 32.7 Audio And Music Generation

Audio generation creates sound, speech, or music.

Use cases:

- Generate voice prompts for training simulations.
- Generate notification sounds.
- Generate audio examples for QA.
- Create synthetic call examples for testing when policy allows.

Safety requirements:

- Voice cloning requires explicit consent.
- Generated speech should be labeled as synthetic where policy requires.
- Store voice consent metadata.
- Block impersonation use cases.
- Review generated audio for unsafe content.

### 32.8 Synthetic Data Generation

Synthetic data can support testing and evaluation but must be labeled.

Use cases:

- Generate fake support tickets.
- Generate fake policy questions.
- Generate red-team examples.
- Generate training examples for low-risk classifiers.

Rules:

- Mark synthetic data clearly.
- Do not mix synthetic data with human-labeled ground truth without labels.
- Review synthetic examples before using in eval or training.
- Track generator model and prompt version.

### 32.9 Generative Media Provider Abstraction

The model gateway should support media provider routes.

Interface:

```text
generate_image(request) -> MediaGenerationResponse
edit_image(request) -> MediaGenerationResponse
generate_video(request) -> MediaGenerationJobResponse
generate_audio(request) -> MediaGenerationResponse
```

Provider capability fields:

```text
supports_text_to_image
supports_image_editing
supports_video_generation
supports_audio_generation
supports_seed
supports_reference_image
supports_safety_metadata
max_resolution
max_duration_seconds
```

### 32.10 Generative Media Done Criteria

This track is done when:

- Media generation API exists.
- Jobs are asynchronous for expensive media.
- Outputs are stored in object storage.
- Prompt and output safety checks run.
- Cost and latency are tracked.
- Asset provenance is stored.
- User feedback is captured.
- Evaluation rubric exists.
- Generated media can be disabled per tenant.

## 33. Frontend Product Architecture

The frontend should be a serious product console, not a landing page.

### 32.1 Main Navigation

Recommended navigation:

```text
Dashboard
Chat
Documents
Agents
Approvals
Prompts
Evaluations
Models
Safety
Observability
Admin
```

### 32.2 Core Screens

#### Dashboard

Shows:

- Recent AI runs.
- Cost this month.
- Average latency.
- Failed jobs.
- Pending approvals.
- Evaluation health.
- Safety warnings.

#### Chat And RAG Screen

Shows:

- Conversation list.
- Message thread.
- Source citations.
- Retrieved evidence drawer.
- Feedback controls.
- Model/run metadata for debugging users.

#### Documents Screen

Shows:

- Upload control.
- Document table.
- Processing status.
- Extraction preview.
- Chunk viewer.
- Search test panel.

#### Agent Screen

Shows:

- Agent definitions.
- New task form.
- Run status.
- Step trace.
- Tool calls.
- Approval status.
- Final result.

#### Approvals Screen

Shows:

- Pending risky actions.
- Agent reason.
- Tool input.
- Evidence.
- Approve/reject actions.

#### Prompt Screen

Shows:

- Prompt templates.
- Version history.
- Test cases.
- Eval score comparison.
- Active version.

#### Evaluation Screen

Shows:

- Datasets.
- Runs.
- Scores.
- Failed cases.
- Baseline vs candidate comparison.

#### Safety Screen

Shows:

- Policies.
- Safety checks.
- Red-team runs.
- Violations.
- Blocked outputs.

#### Observability Screen

Shows:

- AI run traces.
- Cost by model.
- Latency by route.
- Error rate.
- Token usage.
- Job failures.

### 32.3 Frontend Data Rules

Rules:

- Frontend never calls LLM providers directly.
- Frontend displays citations and evidence clearly.
- Frontend shows long-running job status.
- Frontend must handle failed AI runs gracefully.
- Frontend must not expose internal prompts to unauthorized users.
- Frontend should show run ids for debugging.

## 34. Authentication And Authorization

### 33.1 Authentication

Authentication options:

- Email/password for local learning.
- OAuth/OIDC for enterprise production.
- API keys for programmatic access.

Recommended implementation path:

1. Start with email/password or simple dev auth.
2. Add JWT or secure session cookies.
3. Add tenant membership.
4. Add role-based permissions.
5. Add API keys with scopes.
6. Add SSO/OIDC later if needed.

### 33.2 Authorization

Authorization must happen at service layer, not only frontend.

Check permissions for:

- Reading documents.
- Uploading documents.
- Running RAG queries.
- Running agents.
- Executing tools.
- Approving actions.
- Managing prompts.
- Running evaluations.
- Managing model routes.
- Viewing costs and audit logs.

### 33.3 Tenant Isolation

Tenant isolation rules:

- Every query filters by tenant id.
- Vector search must include tenant filter.
- Object storage keys should include tenant id.
- AI run logs must include tenant id.
- Background jobs must include tenant id.
- Admin APIs must not accidentally cross tenant boundaries.

### 33.4 Audit Requirements

Audit these events:

- Login.
- Document upload/delete.
- Prompt activation.
- Model route change.
- Agent run started.
- Tool call requested.
- Tool action approved/rejected.
- Sensitive data accessed.
- Evaluation run started.
- Safety policy changed.
- User/role changed.

## 35. Security Architecture

### 34.1 Security Layers

Security layers:

```text
network security
authentication
authorization
tenant isolation
input validation
output validation
secret management
provider access control
PII policy
prompt injection defense
tool execution control
audit logging
monitoring and alerting
```

### 34.2 Input Validation

Validate:

- API request schemas.
- File type and file size.
- Tool arguments.
- Prompt variables.
- Structured model outputs.
- Query filters.
- Pagination parameters.

### 34.3 File Upload Security

File upload controls:

- Allowlist file extensions and MIME types.
- Limit file size.
- Scan or quarantine files where required.
- Store outside web root.
- Generate random object keys.
- Do not execute uploaded files.
- Extract text in worker process.

### 34.4 Secrets

Rules:

- Store secrets in environment or secret manager.
- Rotate provider keys.
- Do not log secrets.
- Do not send secrets into LLM context.
- Separate dev/staging/prod secrets.

### 34.5 Tool Action Security

Tool execution requires:

- Registered tool.
- Valid schema.
- User permission.
- Tenant check.
- Risk check.
- Approval if required.
- Idempotency key for side effects.
- Audit record.

### 34.6 AI-Specific Security

AI-specific risks:

- Prompt injection.
- Data exfiltration through model output.
- Tool misuse.
- Hallucinated policy.
- Insecure memory writes.
- Model provider leakage risk.
- Unsafe fine-tuning data.
- Evaluation contamination.

Controls:

- Trust boundaries in prompts.
- Data minimization.
- Retrieval filtering.
- Output validation.
- Approval gates.
- Safety datasets.
- Audit logs.

### 34.7 Governance And Compliance Package

Governance means the organization can explain, review, control, and improve AI behavior responsibly.

Atlas should include these governance artifacts:

```text
AI system card
model card
risk register
data lineage report
evaluation report
red-team report
incident report template
prompt/model change log
tenant AI policy
provider data-sharing register
```

### 34.8 AI System Card

The AI system card explains the full product behavior.

Template:

```text
System name
Purpose
Users
Supported use cases
Out-of-scope use cases
Models/providers used
Data sources
RAG behavior
Agent capabilities
Tool permissions
Safety controls
Evaluation approach
Known limitations
Human oversight points
Monitoring and incident process
Last review date
Owner
```

### 34.9 Model Card

Each deployed model or important model route should have a model card.

Template:

```text
Model name
Provider
Version
Use case
Input types
Output types
Training/adaptation data if applicable
Evaluation results
Safety results
Known weaknesses
Cost/latency profile
Approved tenants/use cases
Rollback model
Owner
Review date
```

### 34.10 Risk Register

The risk register tracks AI risks and mitigation status.

Fields:

```text
risk_id
risk_name
category
severity
likelihood
impact
owner
mitigation
status
last_reviewed_at
next_review_at
```

Example risks:

```text
RISK-001: prompt injection causes unauthorized tool call
RISK-002: RAG answer leaks cross-tenant data
RISK-003: generated image violates brand or likeness policy
RISK-004: fine-tuning dataset contains sensitive data
RISK-005: MCP server schema changes without review
```

### 34.11 Review Cadence

Recommended review cadence:

```text
weekly: production incidents and high-severity safety events
biweekly: eval failures and prompt/model changes
monthly: risk register review
quarterly: system card and model card review
before release: red-team and regression suite review
```

### 34.12 Provider Data-Sharing Policy

For every provider/model route, document:

```text
provider name
data sent
region
retention policy
training usage policy
sensitive-data allowance
tenant opt-out support
encryption status
contract/legal review status
```

Rules:

- Tenant policy can block specific providers.
- Sensitive workflows can require private/local model routes.
- Provider policy changes require review.

### 34.13 Incident Process

AI incident examples:

- Wrong answer caused business action.
- Safety bypass.
- PII leakage.
- Cross-tenant data leak.
- Unauthorized tool execution.
- Generated media policy violation.
- Model route deployed with severe regression.

Incident flow:

```text
detect incident
-> classify severity
-> freeze or disable risky route/tool/model
-> preserve logs and traces
-> notify owner
-> investigate root cause
-> patch prompt/model/tool/policy
-> run regression and red-team tests
-> document incident
-> update risk register
```

## 36. Observability Architecture

Observability is required for debugging and production operation.

### 35.1 Logs

Use structured JSON logs.

Include:

```text
request_id
trace_id
tenant_id
user_id where allowed
route
status_code
latency_ms
error_code
ai_run_id
agent_run_id
job_id
```

Do not log secrets or raw sensitive content unless explicitly allowed and redacted.

### 35.2 Metrics

Metrics:

- Request count.
- Error rate.
- Latency percentiles.
- AI call count.
- AI token usage.
- AI cost.
- Provider errors.
- RAG retrieval latency.
- Agent step count.
- Tool failure rate.
- Queue depth.
- Job duration.
- Evaluation pass rate.
- Safety block rate.

### 35.3 Traces

Trace important workflows:

```text
rag query trace
agent run trace
ingestion trace
evaluation trace
fine-tuning trace
model serving trace
```

A RAG trace should show:

```text
request
query rewrite
retrieval
reranking
context packing
model call
citation generation
safety checks
response
```

An agent trace should show:

```text
task
plan
step decisions
tool calls
approval waits
verification
final result
```

### 35.4 Cost Observability

Track cost by:

- Tenant.
- User.
- Use case.
- Model.
- Provider.
- Prompt version.
- Agent run.
- Evaluation run.

Cost dashboard should answer:

- Which workflow costs the most?
- Which model is expensive?
- Which tenant is near budget?
- Did a new prompt increase token usage?
- Did RAG context packing become too large?

### 35.5 Production SLOs

SLO means service level objective. It is a measurable reliability or quality target.

Atlas should define SLOs for both software behavior and AI behavior.

API SLO examples:

```text
monthly uptime >= 99.5% for MVP, 99.9% for production
p95 non-AI API latency <= 500 ms
p95 RAG answer latency <= 8 seconds
p95 agent supervised step latency <= 15 seconds excluding human approval wait
5xx error rate <= 1%
```

Ingestion SLO examples:

```text
p95 small document ingestion <= 2 minutes
p95 100-page PDF ingestion <= 10 minutes
embedding job retry success >= 98%
failed ingestion jobs visible within 1 minute
```

RAG quality SLO examples:

```text
retrieval hit rate at 5 >= 85% on golden set
citation accuracy >= 90% on golden set
critical hallucination rate = 0 on safety-critical eval cases
unknown-answer correctness >= 90%
```

Agent SLO examples:

```text
task success rate >= 85% for supported tasks
invalid tool call rate <= 2%
approval bypass rate = 0%
max-step failure rate <= 5%
```

Cost SLO examples:

```text
average MVP RAG answer cost <= configured tenant budget
monthly tenant cost does not exceed budget without admin warning
batch eval cost estimate required before execution
```

Safety SLO examples:

```text
critical PII leakage rate = 0
cross-tenant data leak rate = 0
critical unsafe media generation rate = 0
prompt injection test pass rate >= configured threshold
```

### 35.6 Alerts

Alert on:

- Provider error rate spike.
- RAG latency spike.
- Cost budget threshold crossed.
- Queue depth too high.
- Ingestion failure spike.
- Safety critical event.
- Tool failure spike.
- Approval bypass attempt.
- Evaluation regression after deployment.
- Model serving GPU memory pressure.

### 35.7 GenAI Observability Semantic Fields

GenAI traces should include consistent fields:

```text
gen_ai.provider.name
gen_ai.request.model
gen_ai.response.model
gen_ai.operation.name
gen_ai.output.type
gen_ai.prompt.name
gen_ai.prompt.version
gen_ai.request.reasoning.level
gen_ai.response.finish_reasons
gen_ai.response.time_to_first_chunk
gen_ai.usage.input_tokens
gen_ai.usage.output_tokens
gen_ai.usage.reasoning.output_tokens
gen_ai.usage.cache_read.input_tokens
gen_ai.usage.cache_creation.input_tokens
```

Atlas-specific values must use the `atlas.*` namespace so they do not pretend to be OpenTelemetry standard attributes:

```text
atlas.tenant.id
atlas.user.id
atlas.ai_run.id
atlas.model_route.id
atlas.cost.estimated_usd
atlas.cost.budget_usd
atlas.retrieval.strategy
atlas.retrieval.top_k
atlas.retrieval.reranker
atlas.retrieval.index_version
atlas.retrieval.hit_count
atlas.citation.count
atlas.groundedness.score
atlas.safety.status
atlas.approval.required
```

Agent traces should include:

```text
agent.definition_id
agent.run_id
agent.step_number
agent.tool_name
agent.approval_required
agent.cost_so_far
agent.max_steps
agent.stop_reason
```

## 37. Testing Strategy

Testing must cover backend correctness and AI behavior.

### 36.1 Unit Tests

Unit test:

- Config parsing.
- Permission checks.
- Prompt rendering.
- Schema validation.
- Chunking.
- Context packing.
- Cost calculation.
- Tool validation.
- Agent state transitions.
- Safety policy logic.

### 36.2 Integration Tests

Integration test:

- API routes with database.
- Document ingestion with worker.
- Vector search.
- RAG query flow with fake model provider.
- Agent tool flow with fake tools.
- Approval flow.
- Evaluation run creation.

### 36.3 Contract Tests

Contract test:

- Provider adapter interface.
- Tool input/output schemas.
- API response schemas.
- Frontend API expectations.
- Structured output schemas.

### 36.4 AI Evaluation Tests

AI eval tests:

- Prompt behavior tests.
- RAG answer tests.
- Retrieval quality tests.
- Agent task tests.
- Safety adversarial tests.
- Fine-tuned model comparison tests.

### 36.5 Security Tests

Security tests:

- Tenant isolation.
- Permission enforcement.
- Prompt injection attempts.
- Tool bypass attempts.
- File upload validation.
- PII redaction.
- API key scopes.

### 36.6 Load And Reliability Tests

Load tests:

- Concurrent RAG queries.
- Large document ingestion.
- Many embedding jobs.
- Agent task bursts.
- Evaluation batch runs.

Reliability tests:

- Provider timeout.
- Provider rate limit.
- Worker crash and retry.
- Vector database unavailable.
- Redis unavailable.
- Partial ingestion failure.

## 38. CI/CD Design

### 37.1 Pull Request Checks

Run:

```text
format check
lint
unit tests
type check
migration check
contract tests
security checks
small AI eval smoke tests with fake provider
```

### 37.2 Main Branch Checks

Run:

```text
full unit tests
integration tests
eval regression suite
container build
migration validation
security scan
```

### 37.3 Deployment Pipeline

Pipeline:

```text
merge to main
-> build containers
-> push images
-> deploy to staging
-> run smoke tests
-> run selected evals
-> require approval for production
-> deploy production
-> monitor canary
-> rollback if error thresholds exceeded
```

### 37.4 Migration Strategy

Rules:

- Migrations are reviewed.
- Migrations are reversible where practical.
- Large migrations are split.
- Production migrations are tested in staging.
- Data backfills run as jobs.

## 39. Deployment Architecture

### 38.1 Local Docker Compose

Services:

```text
web
api
worker
postgres
redis
qdrant optional
minio optional
```

Local command should start the platform with sample data.

### 38.2 Staging

Staging includes:

- Same services as production.
- Lower scale.
- Test data.
- Real model provider keys with limited budget.
- Full observability.

### 38.3 Production

Production includes:

- Web app service.
- API service.
- Worker service.
- Managed database.
- Managed Redis.
- Object storage.
- Vector database.
- Model gateway routes.
- Optional model serving GPU nodes.
- Monitoring.
- Alerting.
- Backups.

### 38.4 Kubernetes Later

Kubernetes is useful later for:

- Scaling workers independently.
- Running model serving separately.
- GPU workloads.
- Zero-downtime deploys.
- Cron jobs.
- Secrets and config maps.

Do not start with Kubernetes if local development and product design are not stable.

## 40. Phase-By-Phase Implementation Blueprint

The system should be built in phases. Each phase must leave the system working.

### Phase 00: Engineering Foundation

Goal:

- Build the project skeleton and backend foundation.

Build:

- Python package structure.
- FastAPI app.
- Settings system.
- Logging.
- Error handling.
- Health endpoint.
- Database connection.
- Alembic migrations.
- Test setup.
- Docker Compose.

Primary modules:

```text
apps/api
packages/core
packages/db
tests/unit
tests/integration
infra/docker
```

Completion criteria:

- API starts locally.
- Database migration runs.
- Health check passes.
- Tests run in CI style.
- Config is typed.
- Logs include request ids.

### Phase 01: LLM Gateway

Goal:

- All model calls go through one controlled gateway.

Build:

- Provider adapter interface.
- Mock provider.
- Managed provider adapter.
- Chat request/response schemas.
- Embedding request/response schemas.
- AI run table.
- Token and cost tracking.
- Timeout and retry logic.

Primary modules:

```text
packages/model_gateway
packages/observability
apps/api/routes/models
```

Completion criteria:

- API can call a model through gateway.
- Tests can use mock provider.
- AI run record is stored.
- Cost and latency are recorded.

### Phase 02: Prompt System

Goal:

- Prompts become versioned production assets.

Build:

- Prompt templates.
- Prompt versions.
- Prompt renderer.
- Prompt test cases.
- Activation workflow.

Primary modules:

```text
packages/prompts
apps/api/routes/prompts
```

Completion criteria:

- Prompt variables validate.
- Active prompt version resolves by use case.
- Prompt changes are traceable.
- Prompt tests can run.

### Phase 03: Structured Outputs

Goal:

- LLM output can be consumed reliably by backend code.

Build:

- Structured output schemas.
- Parser and validator.
- Repair loop.
- Failure records.
- Example extraction/classification workflow.

Primary modules:

```text
packages/model_gateway/structured.py
packages/prompts
packages/evals
```

Completion criteria:

- Invalid model output fails safely.
- Structured schema is enforced.
- Repair loop is tested.

### Phase 04: Document Ingestion

Goal:

- Documents become extracted, cleaned, chunked text.

Build:

- Upload API.
- Object storage adapter.
- Document tables.
- Worker ingestion job.
- Text extraction.
- Cleaning.
- Chunking.
- Status tracking.

Primary modules:

```text
packages/ingestion
apps/worker/jobs
apps/api/routes/documents
```

Completion criteria:

- User can upload document.
- Worker processes it.
- Chunks are stored with source metadata.
- Failures are visible.

### Phase 05: Embeddings And Vector Database

Goal:

- Chunks become semantically searchable.

Build:

- Embedding jobs.
- Vector store interface.
- pgvector or Qdrant implementation.
- Semantic search endpoint.
- Retrieval debug view.

Primary modules:

```text
packages/retrieval
packages/model_gateway
```

Completion criteria:

- Chunks have embeddings.
- Query returns relevant chunks.
- Search respects tenant and metadata filters.

### Phase 06: RAG, Reranking, And Citations

Goal:

- User gets grounded answers from private documents.

Build:

- Query classification.
- Query rewrite.
- Retrieval.
- Reranking.
- Context packing.
- RAG prompt.
- Citation builder.
- Answer storage.

Primary modules:

```text
packages/rag
packages/retrieval
packages/prompts
packages/model_gateway
```

Boundary rule: `packages/retrieval` owns embeddings, vector store adapters, hybrid search, reranking, ranking signals, and retrieval traces. `packages/rag` owns answer generation, context packing, grounded response policy, citation building, citation verification, and RAG orchestration.

Completion criteria:

- User asks a question and receives answer with citations.
- Unknown answers are handled correctly.
- Retrieval trace is stored.

### Phase 07: Evaluation Platform

Goal:

- AI quality becomes measurable.

Build:

- Eval datasets.
- Eval cases.
- Eval runner.
- RAG metrics.
- LLM judge.
- Regression comparison.

Primary modules:

```text
packages/evals
apps/eval_runner
apps/api/routes/evals
```

Completion criteria:

- Eval run can compare baseline and candidate.
- Results are stored.
- Failed cases are visible.

### Phase 08: Tool Calling

Goal:

- Models can request safe structured actions.

Build:

- Tool registry.
- Tool schemas.
- Tool execution service.
- Permission checks.
- Dry-run mode.
- Tool call audit.

Primary modules:

```text
packages/tools
packages/auth
packages/safety
```

Completion criteria:

- Tool calls validate.
- Unauthorized calls fail.
- Tool results are logged.

### Phase 09: Controlled Agents

Goal:

- Build multi-step agent workflows with bounded control.

Build:

- Agent definitions.
- Agent run table.
- Agent state machine.
- Planner.
- Executor.
- Step trace.
- Verification.

Primary modules:

```text
packages/agents
packages/tools
packages/rag
```

Completion criteria:

- Agent can plan and execute a low-risk task.
- Trace is stored.
- Limits stop runaway loops.

### Phase 10: Agent Memory

Goal:

- Add scoped memory without leaking sensitive data.

Build:

- Session memory.
- Conversation summaries.
- Long-term memory table.
- Memory write policy.
- Memory retrieval policy.

Primary modules:

```text
packages/memory
packages/agents
packages/safety
```

Completion criteria:

- Memory is scoped.
- Memory can be retrieved.
- Sensitive memory is blocked.

### Phase 11: Safety And Guardrails

Goal:

- Add safety across inputs, retrieval, outputs, tools, and memory.

Build:

- Safety policies.
- Input checks.
- Output checks.
- Prompt injection checks.
- PII detection.
- Approval rules.
- Red-team tests.

Primary modules:

```text
packages/safety
packages/agents
packages/rag
packages/tools
```

Completion criteria:

- Injection examples are detected or neutralized.
- Risky actions require approval.
- Safety checks are logged.

### Phase 12: Multimodal AI

Goal:

- Handle images and scanned documents.

Build:

- Image upload.
- OCR pipeline.
- Vision model extraction.
- Multimodal structured outputs.
- Evidence storage.

Primary modules:

```text
packages/multimodal
packages/ingestion
packages/model_gateway
```

Completion criteria:

- Image or scanned document can be processed.
- Extracted fields are validated.
- Evidence is stored.

### Phase 13: Voice AI

Goal:

- Add speech workflows.

Build:

- Audio upload.
- Transcription.
- Call summary.
- Action extraction.
- Optional text-to-speech.

Primary modules:

```text
packages/voice
packages/model_gateway
packages/rag
```

Completion criteria:

- Audio becomes transcript.
- Transcript becomes summary/action items.
- Results are evaluable.

### Phase 14: Fine-Tuning And Model Adaptation

Goal:

- Adapt models only when evaluation proves it is useful.

Build:

- Dataset builder.
- Data redaction.
- Train/validation/test splits.
- LoRA/QLoRA job metadata.
- Evaluation comparison.

Primary modules:

```text
packages/adaptation
packages/evals
packages/safety
```

Completion criteria:

- Fine-tuning dataset is versioned.
- Candidate model is evaluated against baseline.
- Unsafe or low-quality models are not promoted.

### Phase 15: Model Serving And LLMOps

Goal:

- Serve and route model versions safely.

Build:

- Model registry.
- Model deployment records.
- Local model server integration.
- Gateway routing to served model.
- Health checks.
- Rollback.

Primary modules:

```text
packages/serving
apps/model_server
packages/model_gateway
```

Completion criteria:

- Model version can be deployed to staging route.
- Gateway can route to it.
- Rollback path exists.

### Phase 16: Classical ML

Goal:

- Use traditional ML for prediction problems where it fits better than LLMs.

Build:

- Feature pipeline.
- Baseline classifier/regressor.
- Model evaluation.
- Inference endpoint.
- Monitoring metrics.

Primary modules:

```text
packages/ml
apps/api/routes/ml
```

Completion criteria:

- Classical model trains and predicts.
- Metrics are stored.
- LLM is not misused for simple structured prediction.

### Phase 17: Search, Ranking, And Recommendation

Goal:

- Improve retrieval and recommendations.

Build:

- Hybrid search.
- Ranking signals.
- Feedback-based improvements.
- Similar item recommendations.
- Search evaluation.

Primary modules:

```text
packages/retrieval
packages/evals
```

Completion criteria:

- Hybrid search beats vector-only baseline on eval set.
- Ranking improvements are measured.

### Phase 18: Deployment, Monitoring, And Reliability

Goal:

- Make the system production-operable.

Build:

- CI/CD.
- Docker packaging.
- Staging deployment.
- Monitoring.
- Alerts.
- Runbooks.
- Backups.
- Cost controls.

Primary modules:

```text
infra
packages/observability
docs/runbooks
```

Completion criteria:

- System deploys from pipeline.
- Health checks and alerts exist.
- Rollback is documented and tested.

### Phase 19: Capstone Integration

Goal:

- Present the full system as a portfolio-ready industry project.

Build:

- End-to-end demo.
- Architecture docs.
- API docs.
- Evaluation report.
- Safety report.
- Deployment notes.
- Interview explanation.

Completion criteria:

- A reviewer can run the project.
- A reviewer can understand the architecture.
- A reviewer can see AI quality evidence.
- A reviewer can inspect traces, costs, safety, and evaluations.

### Phase 20: LLM Optimization And Caching

Goal:

- Reduce cost and latency while preserving quality and safety.

Build:

- Provider-level prompt caching support.
- Semantic cache service.
- Batch API support in model gateway.
- Reasoning model routing.
- Reasoning token budget controls.
- Streaming tool-call assembly.
- Partial structured-output handling.
- Cost/latency comparison reports.

Primary modules:

```text
packages/model_gateway
packages/prompts
packages/evals
packages/observability
packages/cache optional
```

Database/storage objects:

```text
semantic_cache_entries
ai_runs.cache_read_input_tokens
ai_runs.cache_creation_input_tokens
ai_runs.reasoning_output_tokens
batch_model_jobs
batch_model_job_items
```

APIs:

```text
GET  /api/v1/models/capabilities
GET  /api/v1/models/optimization-report
POST /api/v1/models/batch-jobs
GET  /api/v1/models/batch-jobs/{job_id}
```

Tests/evals:

- Cached and uncached cost comparison.
- Semantic cache tenant isolation test.
- Reasoning model quality/cost comparison.
- Batch partial-failure test.
- Streaming tool-call validation test.

Completion criteria:

- Gateway tracks cache tokens where supported.
- Semantic cache never leaks across tenants or permissions.
- Batch jobs store per-item results.
- Reasoning mode is used only by route policy.
- Optimization decisions are backed by eval/cost data.

### Phase 21: MCP And External Tool Ecosystem

Goal:

- Add MCP as a controlled, auditable, permissioned external tool integration layer.

Build:

- MCP server registry.
- MCP discovery flow.
- MCP tool schema mapping.
- MCP credentials handling.
- MCP tool enable/disable controls.
- MCP audit events.
- MCP safety checks.
- MCP mock server for tests.

Primary modules:

```text
packages/tools
packages/agents
packages/safety
packages/integrations
packages/observability
```

Database/storage objects:

```text
mcp_servers
mcp_tool_mappings
tool_definitions
tool_calls
audit_events
```

APIs:

```text
POST /api/v1/mcp/servers
GET  /api/v1/mcp/servers
POST /api/v1/mcp/servers/{server_id}/discover
POST /api/v1/mcp/tools/{mapping_id}/enable
POST /api/v1/mcp/tools/{mapping_id}/disable
```

Tests/evals:

- MCP schema import test.
- Disabled server cannot be called.
- Schema change requires review.
- MCP result prompt injection is blocked.
- Write MCP tool requires approval.

Completion criteria:

- Agents can use approved MCP tools only.
- MCP tool calls are audited.
- MCP credentials are scoped.
- MCP can be disabled per tool/server/tenant.

### Phase 22: Multi-Agent Orchestration

Goal:

- Add supervisor/worker and specialist-agent workflows without losing control.

Build:

- Multi-agent collaboration records.
- Agent handoff schema.
- Supervisor agent workflow.
- Specialist agent definitions.
- Handoff validation.
- Agent-to-agent trace viewer.
- Multi-agent eval suite.

Primary modules:

```text
packages/agents
packages/tools
packages/rag
packages/evals
packages/safety
```

Database/storage objects:

```text
agent_collaborations
agent_handoffs
agent_runs
agent_steps
```

APIs:

```text
POST /api/v1/agent-collaborations
GET  /api/v1/agent-collaborations/{id}
GET  /api/v1/agent-collaborations/{id}/handoffs
```

Tests/evals:

- Supervisor delegates to correct specialist.
- Specialist receives limited context.
- Agent loop prevention works.
- Multi-agent cost compared with single-agent baseline.
- Final verifier catches unsupported output.

Completion criteria:

- Multi-agent run is traceable.
- Handoffs are structured.
- Specialist agents cannot exceed delegated scope.
- Multi-agent flow improves target evals enough to justify complexity.

### Phase 23: Advanced RAG And Retrieval Systems

Goal:

- Implement advanced retrieval strategies beyond baseline RAG.

Build:

- Parent-child retrieval.
- Contextual retrieval.
- HyDE retrieval.
- Multi-hop retrieval.
- Query decomposition.
- ACL-filtered indexes.
- Citation verification.
- Knowledge index versioning.
- Optional GraphRAG/RAPTOR experiment.
- Vector index tuning dashboard.

Primary modules:

```text
packages/retrieval
packages/rag
packages/evals
packages/safety
packages/observability
```

Database/storage objects:

```text
rag_query_subquestions
vector_index_versions
knowledge_index_versions
citation_verification_results
```

APIs:

```text
POST /api/v1/retrieval/experiments
GET  /api/v1/retrieval/experiments/{id}
POST /api/v1/rag/citations/{answer_id}/verify
GET  /api/v1/vector-indexes
```

Tests/evals:

- Recall at K by strategy.
- p95 latency by strategy.
- Citation verification accuracy.
- ACL retrieval isolation test.
- Reindex cache invalidation test.

Completion criteria:

- Advanced strategy beats baseline on defined eval set.
- Tradeoff report exists.
- Unsafe or expensive strategy is not used by default.

### Phase 24: Generative Media

Goal:

- Add image, video, and audio generation as optional Gen AI completeness track.

Build:

- Media generation service.
- Text-to-image job API.
- Image editing/inpainting flow.
- Video generation job design.
- Audio/music generation job design.
- Synthetic data generation workflow.
- Media safety checks.
- Media provenance storage.
- Media evaluation rubrics.

Primary modules:

```text
packages/media_generation
packages/model_gateway
packages/safety
packages/evals
packages/observability
apps/worker/jobs
apps/api/routes/media
```

Database/storage objects:

```text
media_generation_jobs
media_assets
media_safety_checks
media_feedback
```

APIs:

```text
POST /api/v1/media/generations
GET  /api/v1/media/generations/{job_id}
GET  /api/v1/media/assets/{asset_id}
POST /api/v1/media/assets/{asset_id}/feedback
```

Tests/evals:

- Prompt safety blocks disallowed request.
- Output safety metadata stored.
- Generated asset stored in object storage.
- Job status transitions correctly.
- Cost and latency recorded.
- Synthetic data is labeled and separated from human-labeled eval data.

Completion criteria:

- At least one media generation capability is implemented end to end.
- Safety and provenance are stored.
- Tenant can disable media generation.
- Evaluation rubric exists.

### Phase 25: Governance, Compliance, And Risk Management

Goal:

- Make the platform reviewable and governable for enterprise use.

Build:

- AI system card.
- Model cards.
- Risk register.
- Provider data-sharing register.
- Governance review workflow.
- Incident report workflow.
- Release approval checklist.
- Compliance export package.

Primary modules:

```text
packages/governance
packages/safety
packages/evals
packages/observability
apps/api/routes/governance
apps/web/features/governance
```

Database/storage objects:

```text
governance_reviews
risk_register_items
model_cards
system_cards
provider_data_policies
ai_incidents
```

APIs:

```text
GET  /api/v1/governance/system-card
POST /api/v1/governance/system-card/reviews
GET  /api/v1/governance/model-cards
POST /api/v1/governance/risk-register
POST /api/v1/governance/incidents
GET  /api/v1/governance/compliance-export
```

Tests/evals:

- Risk item lifecycle test.
- Model card required fields test.
- Provider policy enforcement test.
- Incident disables risky route/tool test.
- Compliance export contains required artifacts.

Completion criteria:

- Governance artifacts exist and are versioned.
- Owners and review cadence are defined.
- Incident process is actionable.
- Provider data policies affect routing decisions.
- Enterprise reviewer can inspect system behavior and controls.

## 41. Cross-Phase Dependency Map

Dependency order:

```text
Foundation
-> Gateway
-> Prompts
-> Structured outputs
-> Ingestion
-> Embeddings
-> RAG
-> Evaluation
-> Tools
-> Agents
-> Memory
-> Safety
-> Multimodal
-> Voice
-> Fine-tuning
-> Serving
-> Classical ML
-> Ranking
-> Deployment
-> Capstone
```

Important dependencies:

- RAG requires ingestion and embeddings.
- Agents require tool calling and model gateway.
- Safe agents require permissions, approvals, and safety checks.
- Fine-tuning requires datasets and evaluation.
- Model serving requires model registry and gateway routing.
- Deployment requires observability and configuration maturity.
- Capstone requires every major flow to be traceable and demonstrable.

### 41.1 Updated Dependency Order With New Phases

Updated dependency order:

```text
Foundation
-> Gateway
-> Prompts
-> Structured outputs
-> Ingestion
-> Embeddings
-> Baseline RAG
-> Evaluation
-> Tools
-> Controlled agents
-> Memory
-> Safety
-> LLM optimization and caching
-> MCP integration
-> Multi-agent orchestration
-> Advanced RAG
-> Multimodal understanding
-> Voice
-> Fine-tuning
-> Model serving
-> Classical ML
-> Search/ranking
-> Deployment/monitoring
-> Generative media
-> Governance/compliance
-> Capstone
```

Important updated dependencies:

- Prompt caching requires prompt templates to separate stable and dynamic sections.
- Semantic caching requires tenant isolation, permission scope, source versioning, and safety checks.
- Batch APIs require worker infrastructure and per-item result storage.
- Reasoning model routing requires model capability metadata and cost controls.
- MCP requires tool registry, permissions, audit logs, and safety checks.
- Multi-agent orchestration requires controlled single-agent execution first.
- Advanced RAG requires baseline RAG plus evaluation datasets.
- Generative media requires object storage, safety checks, cost tracking, and async jobs.
- Governance requires observability, evaluation, safety, model registry, and audit history.

### 41.2 Critical Path Vs Optional Depth

Critical MVP path:

```text
00 -> 01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07 -> light 18 -> 19
```

Agent portfolio path:

```text
00 -> 01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07 -> 08 -> 09 -> 10 -> 11 -> 21 -> optional 22 -> 19
```

Advanced RAG path:

```text
00 -> 01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07 -> 17 -> 23 -> 19
```

Production platform path:

```text
00 -> 01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07 -> 08 -> 09 -> 11 -> 18 -> 20 -> 25 -> 19
```

Full Gen AI breadth path:

```text
00 through 25
```

## 42. Implementation Readiness Checklist

Before coding each phase, define:

- User story.
- Data model changes.
- API endpoints.
- Service methods.
- Background jobs.
- AI prompts.
- Model routes.
- Safety checks.
- Tests.
- Evaluation criteria.
- Observability events.
- Error handling.
- Documentation update.

During coding each phase, implement in this order:

1. Database schema.
2. Domain models and repositories.
3. Service logic.
4. API schemas and routes.
5. Worker jobs if needed.
6. AI gateway or prompt integration if needed.
7. Tests.
8. Logging and metrics.
9. Frontend UI.
10. Evaluation and acceptance checks.

## 43. Production Readiness Checklist

The platform is not production-ready until these exist:

- Authentication.
- Authorization.
- Tenant isolation.
- Database migrations.
- Backups.
- Secrets management.
- Structured logs.
- Metrics.
- Traces.
- Error monitoring.
- Rate limits.
- Cost budgets.
- Model provider timeout policy.
- Model provider retry policy.
- AI run logging.
- Prompt versioning.
- Evaluation datasets.
- Regression evaluation.
- Safety checks.
- Approval workflow.
- Audit logs.
- Deployment pipeline.
- Rollback process.
- Incident runbooks.

## 44. Data Flow Reference

### 43.1 RAG Question Flow

```text
User enters question
-> Web sends POST /api/v1/rag/query
-> API authenticates user
-> API resolves tenant
-> API checks rag.query permission
-> Safety service checks input
-> RAG service classifies query
-> Prompt service loads query rewrite prompt if needed
-> Model gateway rewrites query if needed
-> Retrieval service embeds query
-> Vector store returns candidate chunks
-> Keyword search returns candidate chunks if hybrid enabled
-> Reranker reorders candidates
-> Context packer selects final chunks
-> Prompt service renders RAG answer prompt
-> Model gateway calls answer model
-> Structured validator checks answer shape if schema used
-> Citation builder maps claims to chunks
-> Safety service checks output
-> RAG answer and ai_run are stored
-> API returns answer and citations
-> Frontend displays answer with evidence
-> User feedback is stored
```

### 43.2 Agent Task Flow

```text
User submits task
-> API authenticates user and tenant
-> API checks agents.run permission
-> Agent run is created
-> Agent state starts at classify_task
-> Model gateway classifies task
-> Safety service scores task risk
-> Agent retrieves context if needed
-> Agent creates structured plan
-> Plan validator checks allowed tools and limits
-> Agent selects next tool
-> Tool service validates tool schema
-> Tool service checks permission and tenant boundaries
-> Approval service creates approval if required
-> Human approves or rejects
-> Tool executes if allowed
-> Tool result is returned to agent
-> Agent verifies result
-> Agent continues or finishes
-> Final answer is generated
-> Full trace is stored
-> Evaluation hooks capture result
```

### 43.3 Document Ingestion Flow

```text
User uploads file
-> API validates file
-> Object storage stores original
-> Document record created
-> Ingestion job queued
-> Worker extracts text
-> Worker creates page records
-> Worker cleans text
-> Worker chunks text
-> Worker stores chunks
-> Worker creates embedding jobs
-> Embedding worker calls model gateway
-> Vector store saves embeddings
-> Document status becomes processed
-> Search and RAG can now use document
```

### 43.4 Fine-Tuning Flow

```text
AI engineer selects use case
-> Evaluation shows baseline weakness
-> Candidate examples are collected
-> Safety redaction runs
-> Dataset version is created
-> Training job is configured
-> LoRA or QLoRA training runs
-> Model artifact is saved
-> Evaluation compares candidate with baseline
-> Safety tests run
-> Model registry records result
-> Staging route is created
-> Canary deployment starts
-> Monitoring decides promote or rollback
```

## 45. Failure Mode Matrix

### 44.1 Model Provider Failure

Failure:

- Provider timeout.
- Rate limit.
- Invalid API key.
- Model unavailable.

Mitigation:

- Timeout and retry policy.
- Fallback model route.
- Circuit breaker.
- User-facing graceful error.
- Alert if repeated.

### 44.2 Retrieval Failure

Failure:

- No chunks found.
- Wrong chunks found.
- Tenant filter missing.
- Embeddings stale.

Mitigation:

- Return not enough information.
- Retrieval debug logs.
- Metadata filters.
- Embedding version checks.
- Retrieval evals.

### 44.3 Agent Failure

Failure:

- Invalid plan.
- Repeated tool error.
- Unsafe action request.
- Infinite loop.
- Wrong assumption.

Mitigation:

- Max steps.
- Plan validation.
- Tool schema validation.
- Human approval.
- Verification step.
- Blocked state.

### 44.4 Safety Failure

Failure:

- Prompt injection bypass.
- PII leakage.
- Unsafe output.
- Tool misuse.

Mitigation:

- Defense in depth.
- Red-team dataset.
- Output checks.
- Approval gates.
- Audit and alerts.

### 44.5 Data Failure

Failure:

- Bad OCR.
- Duplicate chunks.
- Corrupt file.
- Wrong metadata.
- Failed embedding job.

Mitigation:

- Ingestion status.
- Retry jobs.
- Quality checks.
- Reingestion endpoint.
- Manual review.

## 46. Interview And Portfolio Proof

This project should prove the following job skills:

- Python backend engineering.
- FastAPI service design.
- SQL database design.
- Background workers.
- API schema design.
- Authentication and RBAC.
- LLM provider abstraction.
- Prompt versioning.
- Structured outputs.
- RAG architecture.
- Vector databases.
- Reranking.
- Citation generation.
- Evaluation systems.
- LLM-as-judge.
- Agent state machines.
- Tool calling.
- Human approval workflows.
- AI safety and prompt injection defense.
- Memory design.
- Fine-tuning decision-making.
- LoRA/QLoRA workflow.
- Model serving.
- MLOps and LLMOps.
- Multimodal AI.
- Voice AI.
- Classical ML.
- Search and ranking.
- Observability.
- Cost control.
- Deployment and CI/CD.
- Production reliability.

A strong interview explanation should answer:

- Why did you build a model gateway?
- How do you prevent prompt injection?
- How do you know your RAG system is accurate?
- Why not fine-tune instead of RAG?
- How do agents call tools safely?
- How do you measure hallucination?
- How do you control cost?
- How do you debug a bad answer?
- How do you deploy a new prompt or model safely?
- How do you keep tenant data isolated?

## 47. Final System Completion Standard

The full Atlas AI Platform is complete only when these are true:

1. A user can sign in and work inside a tenant.
2. A user can upload documents.
3. Documents are extracted, chunked, embedded, and searchable.
4. A user can ask RAG questions and receive cited answers.
5. RAG behavior is evaluated with datasets.
6. Prompts are versioned and testable.
7. Structured outputs are validated.
8. Agents can run controlled multi-step tasks.
9. Agents can call tools through schemas and permission checks.
10. Risky actions require human approval.
11. Memory is scoped and policy-controlled.
12. Safety checks exist for input, context, output, tools, and memory.
13. AI runs store model, prompt, cost, latency, and trace data.
14. Evaluation can compare baseline and candidate versions.
15. Fine-tuning workflow exists and is used only when justified.
16. Model serving path exists for adapted/open models.
17. Multimodal document/image workflow exists.
18. Voice workflow exists.
19. Classical ML workflow exists for non-LLM prediction tasks.
20. Search/ranking improvements are measurable.
21. System runs locally through Docker Compose.
22. Tests cover unit, integration, contract, security, and AI evaluation cases.
23. CI/CD runs quality checks.
24. Staging deployment exists.
25. Production design includes monitoring, alerts, backups, rollback, cost budgets, and incident runbooks.
26. Final documentation explains architecture, APIs, data flows, safety, evaluation, and deployment.

Additional completion requirements after the 2026 gap-closure update:

27. MVP critical path is explicitly documented and buildable.
28. API contracts include headers, envelopes, pagination, errors, auth rules, and sample payloads.
29. Database design includes ERD relationship map and data lineage.
30. Document deletion, reindexing, export, retention, and dataset contamination controls exist.
31. Provider-level prompt caching is supported where providers allow it.
32. Semantic caching exists with tenant, permission, source-version, and safety controls.
33. Batch model APIs are supported for embeddings, evaluations, and offline jobs.
34. Reasoning model routes include explicit reasoning budgets and cost controls.
35. Streaming supports text, tool-call deltas, agent progress, and partial structured-output handling.
36. Advanced RAG strategies are implemented behind strategy interfaces and evaluated against baseline.
37. Embedding/index tuning includes HNSW or equivalent recall/latency tradeoff measurement.
38. MCP servers and tools are registered, permissioned, audited, versioned, and disableable.
39. Agent identity and scoped credentials are enforced.
40. Multi-agent orchestration exists only with structured handoffs, limits, and evaluation.
41. Threat model includes prompt injection, data exfiltration, tool misuse, MCP risk, memory poisoning, and media risk.
42. Evaluation playbook includes dataset format, rubrics, judge calibration, thresholds, and human review.
43. Bias, fairness, and toxicity checks exist for relevant workflows.
44. Governance package includes system card, model cards, risk register, provider data policy, review cadence, and incident process.
45. Production SLOs define latency, quality, cost, safety, and reliability targets.
46. Generative media track includes image, video, audio/music, synthetic data, safety, provenance, and evaluation.
47. Voice track includes realtime speech-to-speech architecture, diarization, consent, and retention.
48. Model adaptation distinguishes managed fine-tuning, open LoRA/QLoRA, and distillation.
49. Model serving includes quantization, batching, canary routing, and rollback.
50. Final portfolio explains which path was completed: MVP, RAG, agentic, production, or full Gen AI breadth.

## 48. Final Implementation Philosophy

Atlas should not be built as many disconnected demos.

It should be built as one platform where every Gen AI topic has a real place:

- LLMs live behind the model gateway.
- Prompts live in the prompt system.
- Structured outputs live in schema validation.
- Documents live in ingestion and storage.
- Embeddings live in retrieval.
- RAG lives in grounded answer workflows.
- Agents live in controlled state machines.
- Tools live in a permissioned registry.
- Memory lives behind retention and privacy rules.
- Safety lives across the whole request lifecycle.
- Evaluation lives beside every AI behavior.
- Fine-tuning lives after evidence shows it is needed.
- Serving lives behind model routing.
- Monitoring lives across every request and job.
- Deployment lives in repeatable infrastructure.

The final mental model remains:

```text
The application controls the system.
The model assists inside controlled boundaries.
Every AI output is validated, measured, logged, and improved.
```

This is the difference between a beginner chatbot and an industry-ready Gen AI engineering platform.
























