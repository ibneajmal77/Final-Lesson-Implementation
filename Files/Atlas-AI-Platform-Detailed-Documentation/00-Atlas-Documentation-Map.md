# Atlas AI Platform - Documentation Map

## Purpose Of This Document

This document is the starting point for the complete Atlas AI Platform documentation set.

The goal of the documentation set is not only to describe a project. The goal is to teach how a real industry-grade Generative AI platform is designed before coding begins.

This map explains:

- What each document will contain.
- The correct order to read the documents.
- How the technical project plan and learning plan stay separate.
- How every Gen AI, Python, backend, data, safety, evaluation, and production topic fits into one end-to-end system.
- How a beginner can move from understanding concepts to implementing a real portfolio-level project.

The Atlas AI Platform should be treated as one large project that grows phase by phase. Each phase adds a real capability that exists in modern AI products: LLM chat, prompt management, structured outputs, RAG, agents, tool calling, memory, evaluation, guardrails, fine-tuning, model serving, monitoring, deployment, multimodal AI, voice AI, and classical ML support.

## Main Documentation Folder

All detailed documents will live under this folder:

```text
C:\Users\muhammad.awais\OneDrive - 7x\Documents\Files\Atlas-AI-Platform-Detailed-Documentation
```

Expected structure:

```text
Atlas-AI-Platform-Detailed-Documentation/
  00-Atlas-Documentation-Map.md
  01-Atlas-Technical-Master-Blueprint.md
  02-Atlas-Coverage-Matrix.md
  03-Atlas-Visual-Architecture-Diagrams.md
  04-Atlas-Database-Schema-Specification.md
  05-Atlas-Standards-Crosswalk.md
  06-Atlas-Implementation-Tickets.md
  07-Atlas-Model-Routing-And-Provider-Examples.md
  08-Atlas-Frontend-UX-Specification.md
  09-Atlas-Seed-Datasets.md
  10-Atlas-Operations-Runbooks.md
  seed-datasets/
    rag_eval.jsonl
    structured_output_tickets.jsonl
    tool_calling.jsonl
    agent_tasks.jsonl
    safety_redteam.jsonl
    voice_eval.jsonl
    media_generation.jsonl
    judge_calibration.jsonl
  learning-phases/
    phase-00-engineering-foundation.md
    phase-01-llm-gateway.md
    phase-02-prompt-system.md
    phase-03-structured-outputs.md
    phase-04-document-ingestion.md
    phase-05-embeddings-vector-db.md
    phase-06-rag-reranking-citations.md
    phase-07-evaluation-platform.md
    phase-08-tool-calling.md
    phase-09-controlled-agents.md
    phase-10-agent-memory.md
    phase-11-safety-guardrails.md
    phase-12-multimodal-ai.md
    phase-13-voice-ai.md
    phase-14-fine-tuning-model-adaptation.md
    phase-15-model-serving-llmops.md
    phase-16-classical-ml.md
    phase-17-search-ranking-recommendation.md
    phase-18-deployment-monitoring-reliability.md
    phase-19-capstone-integration.md
    phase-20-llm-optimization-and-caching.md
    phase-21-mcp-and-external-tool-ecosystem.md
    phase-22-multi-agent-orchestration.md
    phase-23-advanced-rag-and-retrieval-systems.md
    phase-24-generative-media.md
    phase-25-governance-compliance-risk-management.md
```

## Implementation Repository

The Phase 00 starter implementation now lives beside the documentation set:

```text
C:\Users\muhammad.awais\OneDrive - 7x\Documents\Files\Atlas-AI-Platform
```

Current implementation status:

```text
Phase 00 scaffold created: project config, FastAPI shell, settings, errors, request-id middleware, DB/Alembic skeleton, worker entry point, tests, Docker Compose.
MVP spine not complete yet: Phases 01 through 07 still need implementation.
```

## Why The Documentation Is Split

The documentation is split into two major types because mixing them makes the learning path confusing.

### 1. Technical Implementation Documents

These documents explain what the system is and how it should be built.

They cover:

- System architecture.
- Service boundaries.
- Folder structure.
- Database schema.
- API design.
- AI pipeline design.
- Model gateway design.
- RAG architecture.
- Agent orchestration.
- Tool execution.
- Memory design.
- Evaluation design.
- Safety and guardrails.
- Observability and monitoring.
- Deployment.
- Production readiness.

These are the documents a software engineer uses before coding.

### 2. Learning Phase Documents

These documents explain how to understand each part before implementing it.

Each phase will teach:

- The concept in simple language.
- Why it matters in real companies.
- Where it fits in the system.
- How the data flows.
- Which Python concepts are needed.
- Which Gen AI concepts are needed.
- Which libraries are used and why.
- What APIs and database tables are involved.
- How to build the phase step by step.
- What can fail.
- How to test it.
- What interview knowledge the phase proves.

These are the documents a learner uses before and during coding.

## Current Written Versus Planned Learning Docs

Current written learning documents:

```text
learning-phases/phase-00-engineering-foundation.md
learning-phases/phase-01-llm-gateway.md
```

Planned learning documents:

```text
learning-phases/phase-02-prompt-system.md through phase-25-governance-compliance-risk-management.md
```

The planned list is intentional. It shows the complete learning path, but it should not be read as completed documentation. New phase learning docs should be written only when implementation is ready to move into that phase, starting with Phase 01 through Phase 07 for the MVP spine.

## Correct Reading Order

Read the documents in this order.

### Step 1: Read This Map

Start here to understand the full documentation structure.

This file tells you where everything belongs and prevents confusion between project design, learning, implementation, and coverage.

### Step 2: Read The Technical Master Blueprint

Next read:

```text
01-Atlas-Technical-Master-Blueprint.md
```

This document will explain the complete system from an engineering perspective.

It will answer:

- What are we building?
- Who uses it?
- What problem does it solve?
- What are the major components?
- How do services communicate?
- Where does each AI feature live?
- Which libraries and frameworks are selected?
- What database tables are required?
- What APIs are required?
- How will the system move from local development to production?

### Step 3: Read The Coverage Matrix

Then read:

```text
02-Atlas-Coverage-Matrix.md
```

This document will map every major topic to the project.

It will answer:

- Where is Python covered?
- Where is backend engineering covered?
- Where is prompt engineering covered?
- Where is RAG covered?
- Where are agents covered?
- Where is fine-tuning covered?
- Where is model serving covered?
- Where are evaluation and guardrails covered?
- Where are deployment, monitoring, CI/CD, and production operations covered?

This document is useful when checking whether the project covers industry skills.

### Step 4: Read The Implementation-Ready Specification Documents

Then read the supporting implementation documents. These files turn the blueprint into artifacts that can be coded, reviewed, tested, and operated.

| File | What It Gives You | Why It Exists |
|---|---|---|
| `03-Atlas-Visual-Architecture-Diagrams.md` | C4 diagrams, sequence diagrams, ERD, RAG flow, agent flow, MCP flow, evaluation flow, deployment diagram | Makes architecture reviewable visually before code starts |
| `04-Atlas-Database-Schema-Specification.md` | Exact tables, columns, types, enums, indexes, unique constraints, foreign keys, migration order | Gives the database implementation plan, not only table descriptions |
| `05-Atlas-Standards-Crosswalk.md` | Atlas controls mapped to OWASP LLM Top 10, OWASP AISVS, OWASP Agentic risks, NIST AI RMF GenAI Profile, MCP security, OpenTelemetry GenAI | Shows how the platform lines up with industry security, governance, and observability expectations |
| `06-Atlas-Implementation-Tickets.md` | Small build tickets for every phase with models, migrations, services, routes, tests, evals, UI, and done criteria | Converts the plan into executable engineering work |
| `07-Atlas-Model-Routing-And-Provider-Examples.md` | Concrete provider and route examples for cheap classifier, RAG answer, embeddings, judge, reasoning, private route, media route | Makes model routing and provider abstraction implementable |
| `08-Atlas-Frontend-UX-Specification.md` | Screens, states, filters, trace views, approvals, eval dashboard, admin workflows | Makes the frontend console buildable, not only conceptually described |
| `09-Atlas-Seed-Datasets.md` | Starter JSONL examples for RAG, structured output, tool calling, agents, safety, voice, media, judge calibration | Gives test/eval data shape before implementation starts |
| `10-Atlas-Operations-Runbooks.md` | Provider outage, bad RAG answer, prompt injection, cost spike, vector corruption, unsafe tool execution, eval regression, media, voice, MCP runbooks | Gives production incident procedures and acceptance criteria |

### Step 5: Read The Learning Phase Documents One By One

After the blueprint and coverage matrix, read the learning documents in sequence.

Each phase builds on the previous phase. Do not skip phases if the goal is deep understanding.

Example:

```text
phase-00-engineering-foundation.md
phase-01-llm-gateway.md
phase-02-prompt-system.md
phase-03-structured-outputs.md
```

A beginner should read each phase first, understand it, then implement that phase in code, then test it, then move to the next phase.

## Scope Freeze And Execution Focus

The documentation now intentionally stops at Phase 25. Do not add Phase 26 before the MVP spine is running with code, tests, evals, traces, and a demo.

The execution priority is:

1. Build the MVP spine first: Phase 00 through Phase 07, plus light Phase 18 observability and light Phase 19 frontend integration.
2. Add the agent portfolio layer next: Phase 08 through Phase 11.
3. Add advanced, expensive, or specialized tracks only after the spine works: multimodal, voice, fine-tuning, serving, advanced RAG, media, and governance hardening.

The reason is practical: the architecture can cover the full GenAI landscape, but the first portfolio proof must be finishable. The MVP spine proves the most important industry skills: backend API, model gateway, prompt system, structured outputs, ingestion, embeddings, RAG, citations, evals, observability, and a usable frontend path.

## Project Story

The project is called Atlas AI Platform.

Atlas is a full-stack enterprise AI platform for support, operations, document intelligence, and automation.

The system will allow users to:

- Upload documents.
- Extract and normalize text.
- Create embeddings.
- Search knowledge with semantic retrieval.
- Ask questions over private data.
- Get answers with citations.
- Run controlled AI agents.
- Let agents call tools safely.
- Track every model request, cost, latency, token usage, and result.
- Evaluate answer quality.
- Detect hallucination and unsafe behavior.
- Support human approval before risky actions.
- Fine-tune or adapt open models where useful.
- Serve models behind a controlled gateway.
- Add multimodal and voice workflows.
- Deploy the system with monitoring and reliability controls.

The project should feel like a real company platform, not a collection of disconnected demos.

## Core Architecture Summary

The final platform will use a modular monolith first, with clear boundaries that can later become services.

High-level components:

```text
User
  -> Web Console
  -> API Service
  -> Auth and Permissions
  -> Model Gateway
  -> Prompt System
  -> RAG Service
  -> Agent Orchestrator
  -> Tool Service
  -> Safety Service
  -> Evaluation Service
  -> Worker Service
  -> Databases and Storage
  -> Monitoring Stack
```

Main runtime components:

- Web console: user interface for chat, documents, agents, evaluations, and admin views.
- API service: FastAPI backend that exposes authenticated endpoints.
- Worker service: background jobs for ingestion, embeddings, batch evals, and long-running AI tasks.
- Model gateway: single controlled entry point for all LLM and embedding providers.
- Prompt service: versioned prompt templates, variables, and prompt tests.
- RAG service: retrieval, reranking, context packing, citation creation, and answer generation.
- Agent orchestrator: controlled planning, tool selection, execution loops, and approvals.
- Tool service: typed business actions that agents can request but not freely control.
- Safety service: prompt-injection checks, policy checks, output validation, and risk scoring.
- Evaluation service: offline datasets, online feedback, regression tests, and quality dashboards.
- Model adaptation service: fine-tuning, LoRA/QLoRA experiments, dataset preparation, and model registry.
- Serving layer: self-hosted or managed inference endpoints behind the gateway.
- Observability stack: logs, traces, metrics, token usage, cost, latency, and failure analysis.

## Main Technology Stack

The exact stack can be adjusted later, but the documentation will assume this practical industry stack.

### Core Backend

- Python.
- FastAPI.
- Pydantic.
- SQLAlchemy.
- Alembic.
- PostgreSQL.
- Redis.
- Celery, RQ, or Arq for background jobs.
- Docker and Docker Compose.

### AI And Gen AI

- OpenAI or other managed LLM providers through a gateway abstraction.
- Hugging Face Transformers for open model experiments.
- Sentence Transformers or provider embeddings.
- pgvector or Qdrant for vector search.
- Rerankers from Cohere, Jina, BGE, or local cross-encoders depending on final choice.
- LangGraph for agent workflow orchestration, or a custom state machine if simpler control is preferred.
- Instructor, PydanticAI, or native structured-output APIs for typed model outputs.
- MLflow for experiments and model tracking.
- PEFT, LoRA, and QLoRA for model adaptation.
- PyTorch for model training and inference foundations.

### Frontend

- React or Next.js.
- TypeScript.
- A component library if useful.
- TanStack Query for API state.
- Forms with validation.
- Dashboard pages for AI runs, documents, evaluations, and admin workflows.

### Production And Operations

- Docker Compose for local development.
- CI pipeline for tests, linting, type checks, and security checks.
- Staging environment before production.
- Kubernetes later, only after the architecture is stable.
- OpenTelemetry for traces.
- Prometheus and Grafana for metrics.
- Centralized logs.
- Secret management.
- Rollback strategy.

## Phase List

The full project will be built in 26 phases, numbered Phase 00 through Phase 25.

### Phase 00: Engineering Foundation

Build the project skeleton, environment setup, configuration, logging, error handling, testing layout, and database migration foundation.

This phase teaches professional Python backend structure before adding AI complexity.

### Phase 01: LLM Gateway

Create a controlled gateway for all model calls.

This phase teaches provider abstraction, request validation, retry policy, timeout handling, token tracking, cost tracking, and model routing.

### Phase 02: Prompt System

Create versioned prompt templates with variables, test cases, and change history.

This phase teaches that prompts are production assets, not random strings hidden inside code.

### Phase 03: Structured Outputs

Add typed AI responses using schemas and validation.

This phase teaches JSON schema, Pydantic validation, repair loops, and reliable LLM integration with backend systems.

### Phase 04: Document Ingestion

Add upload, parsing, extraction, cleaning, metadata capture, and ingestion jobs.

This phase teaches how unstructured business documents become usable AI data.

### Phase 05: Embeddings And Vector Database

Generate embeddings, store vectors, and support semantic search.

This phase teaches vector search, metadata filters, indexing, distance metrics, and retrieval debugging.

### Phase 06: RAG, Reranking, And Citations

Build retrieval-augmented generation with context selection, reranking, citation generation, and grounded answers.

This phase teaches the most common production Gen AI architecture used in companies.

### Phase 07: Evaluation Platform

Build datasets, expected answers, scoring, regression tests, and evaluation dashboards.

This phase teaches how to prove whether an AI system is improving or getting worse.

### Phase 08: Tool Calling

Define typed tools that models can request.

This phase teaches function calling, tool schemas, authorization checks, dry-run mode, and auditable execution.

### Phase 09: Controlled Agents

Build agent workflows that can plan, retrieve, call tools, verify results, and stop safely.

This phase teaches agent design without giving uncontrolled power to the model.

### Phase 10: Agent Memory

Add short-term session memory and long-term user or tenant memory.

This phase teaches memory types, summarization, retrieval, privacy boundaries, and retention rules.

### Phase 11: Safety And Guardrails

Add policy checks, prompt-injection defense, PII handling, harmful output prevention, and approval gates.

This phase teaches safety as part of architecture, not a final extra layer.

### Phase 12: Multimodal AI

Add image and document-vision workflows.

This phase teaches OCR, image understanding, multimodal prompts, document screenshots, evidence extraction, and visual validation.

### Phase 13: Voice AI

Add speech-to-text, text-to-speech, call summaries, escalation notes, and voice workflow evaluation.

This phase teaches voice pipelines and real-time or near-real-time AI product design.

### Phase 14: Fine-Tuning And Model Adaptation

Prepare datasets, train adapters, evaluate model variants, and compare them against prompting or RAG.

This phase teaches when fine-tuning is useful and when it is the wrong tool.

### Phase 15: Model Serving And LLMOps

Serve open models or adapted models through controlled inference endpoints.

This phase teaches model registry, deployment, versioning, routing, latency, batching, and rollback.

### Phase 16: Classical ML

Add predictive models where LLMs are not the best solution.

This phase teaches classification, regression, feature engineering, scikit-learn, model evaluation, and when classical ML beats Gen AI.

### Phase 17: Search, Ranking, And Recommendation

Add hybrid search, learning-to-rank style thinking, recommendations, and retrieval quality tuning.

This phase teaches the connection between information retrieval, recommendations, RAG quality, and user experience.

### Phase 18: Deployment, Monitoring, And Reliability

Package the system, deploy it, monitor it, and make it maintainable.

This phase teaches CI/CD, Docker, cloud readiness, metrics, traces, alerts, rate limits, cost budgets, and incident response.

### Phase 19: Capstone Integration

Connect everything into one coherent platform and prepare it as a portfolio project.

This phase teaches system integration, documentation, demo flows, tradeoff explanation, and interview presentation.


### Phase 20: LLM Optimization And Caching

Add provider-level prompt caching, semantic caching, batch APIs, reasoning model routing, reasoning token budgets, streaming tool-call handling, and cost/latency optimization.

### Phase 21: MCP And External Tool Ecosystem

Add Model Context Protocol integration with server registration, tool discovery, schema mapping, permissions, scoped credentials, audit, and disablement controls.

### Phase 22: Multi-Agent Orchestration

Add supervisor/worker agent patterns, structured handoffs, specialist agents, agent identity, loop prevention, and multi-agent evaluation.

### Phase 23: Advanced RAG And Retrieval Systems

Add parent-child retrieval, contextual retrieval, HyDE, multi-hop retrieval, query decomposition, ACL-filtered retrieval, citation verification, index tuning, and optional GraphRAG/RAPTOR experiments.

### Phase 24: Generative Media

Add text-to-image, image editing/inpainting, video generation, audio/music generation, synthetic data generation, media safety, provenance, and media evaluation.

### Phase 25: Governance, Compliance, And Risk Management

Add AI system cards, model cards, risk register, provider data-sharing policy, governance review cadence, incident process, and compliance export.
## Standard Structure For Every Learning Phase

The authoritative rules for writing a phase document now live in:

```text
learning-phases/PHASE-AUTHORING-STANDARD.md
```

That file defines the full section skeleton used by the written phases, the traceability and conflict-resolution rules, and the mandatory "Concepts You Cannot Learn From The Code" section — the phase-scoped theory that cannot be expressed in code and would otherwise never be taught. Give it to any phase author together with a short per-phase brief; `learning-phases/HOW-TO-WRITE-phase-02-prompt-system.md` is the worked example of such a brief.

The 21 topics below remain the required coverage. The written phases arrange them into a richer skeleton, so treat this list as the checklist and the authoring standard as the layout.

```text
1. Phase Goal
2. What You Must Understand Before Coding
3. Business Perspective
4. User Perspective
5. Architecture Perspective
6. Python And Backend Perspective
7. Data Perspective
8. Gen AI Perspective
9. Safety And Security Perspective
10. Evaluation Perspective
11. Operations Perspective
12. Interview And Portfolio Perspective
13. Detailed Data Flow
14. Libraries And Tools
15. APIs To Design
16. Database And Storage Objects
17. Implementation Sequence
18. Tests And Evaluations
19. Failure Modes
20. Done Criteria
21. Connection To Next Phase
```

This structure is important because real AI engineering is not only model usage. A strong Gen AI engineer must understand backend engineering, data movement, validation, safety, product behavior, deployment, monitoring, and evaluation.

## What The Project Is Expected To Cover

The complete documentation set is intended to cover the practical job-market side of Generative AI and AI engineering.

It will cover:

- Python project structure.
- Python typing.
- Pydantic models.
- Async APIs.
- FastAPI architecture.
- Background workers.
- SQL database design.
- Database migrations.
- Redis caching and queues.
- File storage.
- Authentication and authorization.
- LLM API integration.
- Model abstraction.
- Prompt engineering.
- Prompt versioning.
- Structured outputs.
- JSON schema validation.
- Function calling.
- Tool calling.
- Document ingestion.
- OCR and parsing.
- Chunking.
- Embeddings.
- Vector databases.
- Semantic search.
- Hybrid search.
- Reranking.
- Retrieval augmented generation.
- Citations and grounding.
- Hallucination reduction.
- AI agents.
- Agent state machines.
- Planning and execution loops.
- Human approval workflows.
- Agent memory.
- Safety policies.
- Prompt injection defense.
- PII detection.
- Evaluation datasets.
- LLM-as-judge.
- Human feedback.
- Cost and latency measurement.
- Fine-tuning.
- LoRA and QLoRA.
- Model serving.
- Model registry.
- MLOps and LLMOps.
- Multimodal AI.
- Voice AI.
- Generative media.
- MCP integration.
- Advanced RAG.
- Governance and compliance.
- Production SLOs.
- Classical ML.
- Search and ranking.
- Recommendations.
- Docker.
- CI/CD.
- Monitoring.
- Observability.
- Production operations.
- Portfolio and interview preparation.

## What This Project Will Not Try To Do

The project should be broad and deep, but it should stay practical.

It will not try to teach every research topic in artificial intelligence.

It will not focus heavily on old symbolic AI, robotics theory, theoretical neuroscience, theorem proving, or advanced research mathematics unless those topics directly support practical Gen AI engineering.

The focus is job-market AI engineering, especially Generative AI systems used in real software products.

## How To Use This As A Beginner

If you are learning from the start, use this process:

1. Read the current phase document fully.
2. Rewrite the phase goal in your own words.
3. Draw the data flow before coding.
4. Identify which database tables or files will be touched.
5. Identify which APIs will be created.
6. Identify which AI model calls happen and why.
7. Implement the simplest working version.
8. Add validation and error handling.
9. Add tests.
10. Add evaluation where AI output quality matters.
11. Add logging and observability.
12. Write notes about what failed and what you fixed.
13. Only then move to the next phase.

This approach prevents copy-paste learning and forces real engineering understanding.

## How To Use This For Job Preparation

For job preparation, each phase should produce evidence.

Evidence means something you can show or explain in an interview.

Examples:

- A clean architecture diagram.
- A clear database schema.
- A working API.
- A tested ingestion pipeline.
- A RAG evaluation report.
- A prompt version comparison.
- A tool-call audit trail.
- An agent execution trace.
- A safety test suite.
- A cost and latency dashboard.
- A deployment plan.
- A final demo script.

The goal is not to say "I used AI". The goal is to explain exactly how the system works, why each decision was made, what tradeoffs exist, and how quality is measured.

## Quality Standard For The Remaining Documents

Every remaining document should be detailed enough that a new developer can understand:

- What to build.
- Why to build it.
- Where it fits.
- Which files are involved.
- Which database objects are involved.
- Which APIs are involved.
- Which AI concepts are involved.
- How the data moves.
- How to test it.
- How to debug it.
- How to make it production-ready.

A phase is not complete just because code runs locally.

A phase is complete only when it has:

- Clear behavior.
- Clear boundaries.
- Validated inputs and outputs.
- Tests.
- Logging.
- Error handling.
- Security checks where needed.
- Evaluation where AI quality matters.
- Documentation explaining the design.

## Final Mental Model

The most important design rule for this project is:

The application owns the system. The LLM does not own the system.

That means:

- The application owns authentication.
- The application owns permissions.
- The application owns tool execution.
- The application owns validation.
- The application owns memory rules.
- The application owns safety policy.
- The application owns evaluation.
- The application owns logging and audit history.
- The LLM generates, reasons, summarizes, extracts, ranks, and suggests only inside controlled boundaries.

This mental model is what separates a serious AI engineering project from a fragile chatbot demo.





