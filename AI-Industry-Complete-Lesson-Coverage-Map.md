# Complete AI Industry Lesson Coverage and Production Plan

Updated: June 25, 2026

## Purpose

This file is the master teaching and generation map for the complete AI industry curriculum. It
connects every teachable lesson to the topics in:

- [AI-Industry-Curriculum.md](AI-Industry-Curriculum.md)
- [AI-Industry-Detailed-Lessons.md](AI-Industry-Detailed-Lessons.md)
- [AI-Industry-Detailed-Outline.md](AI-Industry-Detailed-Outline.md)

It defines:

- The complete lesson order
- What each lesson teaches
- Which tools each lesson uses
- What practical business capability each lesson builds
- Which earlier lessons are prerequisites
- Which AI roles use each lesson
- Which project artifact proves completion
- Where every major curriculum topic is covered
- How the specialization, interview, and readiness sections connect to the core

This is not a replacement for the three source files. It is the traceability layer used to make
sure no required topic is omitted when individual lesson files are generated.

## Corrected curriculum count

| Category | Count |
|---|---:|
| Core lessons | 40 |
| Specialization lessons | 11 |
| Interview-preparation lessons | 6 |
| Total teachable lessons | 57 |
| Junior entry checkpoint | 1 |
| Formal role-readiness assessments | 5 |
| Total readiness gates preserved from the source files | 6 |

The detailed lesson source contains six readiness headings. To preserve the requested five
job-readiness assessments without dropping content:

- **Junior Applied AI or Generative AI readiness** is treated as an entry checkpoint.
- The remaining five are formal role-readiness assessments.

## Corrected numbering

The complete sequence is:

- Lessons 01-40: shared core
- Lessons 41-51: optional specializations
- Lessons 52-57: interview preparation
- Entry Checkpoint: junior Applied AI or Generative AI
- Assessments 01-05: role readiness

The missing entries from the supplied list are:

- Lesson 43: LLM Engineer Specialization
- Lesson 44: MLOps and ML Platform Specialization
- Lesson 52: Coding and Python Interviews
- Lesson 53: SQL Interviews
- Lesson 54: Applied AI Case Interviews
- Lesson 55: LLM and Model-Training Interviews

## How individual lesson files will be written

Every generated lesson must follow:

```text
Understand → Build → Operate
```

Every lesson file must contain:

- Lesson metadata
- Industry and role relevance
- Business problem
- Measurable learning outcomes
- Prerequisites
- Terminology and mental model
- Architecture and data flow
- Tool decisions and alternatives
- Project structure
- Environment setup
- Data or API contracts
- Baseline
- Minimal implementation
- Production implementation
- Unit, integration, failure, security, and evaluation tests
- Evaluation metrics
- Debugging guide
- Security, privacy, and governance
- Performance and cost
- Deployment and rollback
- Observability and operations
- Practical assignment
- Interview preparation
- Production-readiness checklist
- Summary and next lesson

## Lesson file organization

Recommended layout:

```text
Final-Lesson-Implementation/
├── AI-Industry-Curriculum.md
├── AI-Industry-Detailed-Outline.md
├── AI-Industry-Detailed-Lessons.md
├── AI-Industry-Complete-Lesson-Coverage-Map.md
├── lessons/
│   ├── core/
│   │   ├── 01-learning-environment.md
│   │   ├── 02-python-for-production-ai.md
│   │   └── ...
│   ├── specializations/
│   │   ├── 41-applied-ai-engineer-specialization.md
│   │   └── ...
│   ├── interviews/
│   │   ├── 52-coding-and-python-interviews.md
│   │   └── ...
│   └── assessments/
│       ├── entry-junior-applied-ai-readiness.md
│       ├── 01-applied-ai-engineer-readiness.md
│       └── ...
└── generate-ai-industry-lesson/
```

Lesson 01 already exists as:

- [Learning Environment for Production AI Engineering](lessons/learning-environment-for-production-ai.md)

It can later be moved into `lessons/core/` when the full folder structure is created.

## Cumulative business project

The lessons use one evolving business context:

> Build an enterprise customer-operations AI platform that helps support teams classify cases,
> retrieve evidence, draft answers, use approved tools, adapt models, operate securely, and
> measure business results.

The platform grows through the curriculum:

```text
Reproducible repository
→ production Python package
→ async processing
→ tested backend
→ database and storage
→ AI use-case design
→ LLM integration
→ RAG
→ evaluation platform
→ tool-using workflow
→ model adaptation
→ multimodal and voice
→ safety controls
→ cloud production
→ MLOps
→ optimized serving
→ predictive ML
→ enterprise capstone
```

# Core lessons

## Engineering foundations

### Lesson 01 — Learning Environment

**Purpose**

Create the reproducible development environment used by all later lessons.

**Topics covered**

- Python versions and project pinning
- Virtual environments
- `pyproject.toml`
- Dependency constraints and resolution
- `uv.lock`
- Runtime and development dependency groups
- Environment variables
- Typed configuration
- Secret handling
- Git repository setup
- Branches, commits, and pull requests
- Ruff, mypy, pytest, and pre-commit
- Docker and Docker Compose
- PostgreSQL and Redis local services
- GitHub Actions
- Dependency auditing
- Reproducible builds

**Primary tools**

- Python
- uv
- Git and GitHub
- Pydantic Settings
- Ruff
- mypy
- pytest
- pre-commit
- Docker
- Docker Compose
- GitHub Actions
- pip-audit

**Business implementation**

Create the `ai-industry-labs` repository with a typed health-check application, locked
dependencies, local services, container build, tests, and CI.

**Completion evidence**

- Fresh-clone setup succeeds
- Local and container health checks pass
- CI passes on Windows and Linux
- No secrets are committed

**Primary roles**

- Every technical AI role

### Lesson 02 — Python for Production AI

**Prerequisite**

- Lesson 01

**Topics covered**

- Python collections and functions
- Modules and packages
- Classes and dataclasses
- Composition and interfaces
- Protocols and abstract boundaries
- Type hints, generics, and validation
- Exceptions and explicit error categories
- Context managers
- Iterators and generators
- Decorators
- Dependency injection
- Structured logging
- Configuration boundaries
- Memory-aware file processing
- Provider-independent interfaces

**Primary tools**

- Python
- Pydantic
- Ruff
- mypy or Pyright
- pytest

**Business implementation**

Build a typed document-processing package with replaceable providers, safe resource handling,
structured output, and partial-failure reporting.

**Completion evidence**

- Typed public interfaces
- Unit tests without live external dependencies
- Safe malformed-input handling
- Structured logs without sensitive data

**Primary roles**

- Applied AI Engineer
- Generative AI Engineer
- LLM Engineer
- Machine Learning Engineer
- MLOps Engineer
- AI Data Engineer

### Lesson 03 — Asynchronous and Concurrent AI Services

**Prerequisites**

- Lessons 01-02

**Topics covered**

- Synchronous and asynchronous execution
- Event loops
- Coroutines and tasks
- Async HTTP
- Async context managers
- Semaphores and bounded concurrency
- Cancellation
- Timeouts
- Backpressure
- Threads and processes
- CPU-bound versus I/O-bound work
- Background workers
- Job queues
- Graceful shutdown

**Primary tools**

- asyncio
- HTTPX
- FastAPI
- Redis
- A queue or background-worker system

**Business implementation**

Build an asynchronous document-analysis service with upload, background processing, progress,
streaming results, cancellation, and concurrency limits.

**Completion evidence**

- Slow work does not block unrelated requests
- Cancellation releases resources
- Concurrency remains bounded under load
- Retry behavior is observable

**Primary roles**

- Applied AI Engineer
- Generative AI Engineer
- ML Platform Engineer
- AI Infrastructure Engineer
- Speech and Voice Engineer

### Lesson 04 — Testing and Code Quality for AI Systems

**Prerequisites**

- Lessons 01-03

**Topics covered**

- Unit, integration, contract, and end-to-end tests
- Fixtures, mocks, and fakes
- Async testing
- Database isolation
- External API mocking
- Schema tests
- Streaming tests
- Failure-path tests
- Deterministic software tests
- Probabilistic system evaluation
- Test coverage
- CI quality gates
- Flaky-test prevention

**Primary tools**

- pytest
- pytest-asyncio
- Pydantic
- HTTP mocking
- Docker Compose

**Business implementation**

Create a reusable test harness for AI-backed APIs and provider integrations.

**Completion evidence**

- Tests run without paid API access
- Failure paths and schema violations are covered
- Software testing is clearly separated from model evaluation

**Primary roles**

- Every technical AI role
- AI Evaluation Engineer
- AI Safety Engineer

### Lesson 05 — API and Backend Engineering

**Prerequisites**

- Lessons 01-04

**Topics covered**

- HTTP and REST
- OpenAPI and JSON Schema
- Request and response validation
- Authentication and authorization
- API keys
- OAuth and OpenID Connect
- Role-based access control
- Streaming with server-sent events
- WebSockets
- Background jobs
- Webhooks
- Rate limiting
- Idempotency
- Timeouts, retries, and backoff
- Circuit breakers
- API versioning
- Multi-tenant design

**Primary tools**

- FastAPI
- Pydantic
- HTTPX
- PostgreSQL
- Redis
- Alembic

**Business implementation**

Build the production customer-support API with users, tickets, conversations, background jobs,
streaming, authentication, and authorization.

**Completion evidence**

- OpenAPI contract exists
- Authorization and idempotency are tested
- Streaming disconnects safely
- Database migrations are reproducible

**Primary roles**

- Applied AI Engineer
- Generative AI Engineer
- Forward-Deployed AI Engineer
- AI Solutions Architect
- ML Platform Engineer

### Lesson 06 — SQL, Data Modelling, and Storage

**Prerequisites**

- Lessons 01-05

**Topics covered**

- Relational modelling
- Primary and foreign keys
- Joins and aggregations
- Common table expressions
- Window functions
- Transactions and isolation
- Indexes and query plans
- Connection pooling
- Schema migrations
- JSON columns
- Row-level security
- Object storage
- Redis caching
- Data lineage
- Retention and deletion
- Multi-tenant data boundaries

**Primary tools**

- PostgreSQL
- SQLAlchemy or SQLModel
- Alembic
- Redis
- Parquet
- Object storage

**Business implementation**

Create the data layer for users, tenants, tickets, documents, chunks, conversations, model
runs, tool calls, and feedback.

**Completion evidence**

- Cross-tenant access tests pass
- Important queries use appropriate indexes
- Deletion propagates to derived records
- Migrations work on a fresh database

**Primary roles**

- Applied AI Engineer
- Data Scientist
- AI Data Engineer
- Machine Learning Engineer
- MLOps Engineer

## Applied AI and Generative AI

### Lesson 07 — Applied AI Problem Discovery

**Prerequisites**

- Lessons 01-06

**Topics covered**

- User and stakeholder discovery
- Workflow mapping
- Pain-point and bottleneck analysis
- Current-state baseline
- Automation versus decision support
- Human-in-the-loop boundaries
- AI suitability
- Build versus buy
- Risk classification
- Product requirements
- Success metrics
- Adoption metrics
- Cost and expected return
- Domain and regulatory constraints

**Primary tools**

- Process diagrams
- Product-requirements documents
- Architecture decision records
- Risk registers
- Cost models

**Business implementation**

Produce an Applied AI discovery package for the customer-support organization.

**Completion evidence**

- AI use is tied to measurable workflow value
- Rejected use cases are documented
- High-impact actions retain human approval
- Non-AI fallback exists

**Primary roles**

- Applied AI Engineer
- Forward-Deployed AI Engineer
- AI Product Manager
- AI Solutions Architect

### Lesson 08 — Foundation Models and LLM Fundamentals

**Prerequisites**

- Lessons 01-07

**Topics covered**

- Tokens and tokenization
- Embeddings
- Logits and probabilities
- Autoregressive generation
- Transformer blocks
- Self-attention
- Queries, keys, and values
- Positional information
- Context windows
- Encoder, decoder, and encoder-decoder models
- Dense and mixture-of-experts models
- Base, instruction, reasoning, and multimodal models
- Pretraining
- Supervised fine-tuning
- Preference optimization
- Inference
- Temperature, top-p, top-k, and stopping
- Hallucination and uncertainty
- Hosted versus open-weight models

**Primary tools**

- Hugging Face Transformers
- Tokenizer inspection tools
- Hosted model API
- Jupyter for controlled experiments

**Business implementation**

Create a model-behavior laboratory comparing models, tokenization, generation settings, context,
latency, and cost.

**Completion evidence**

- Fixed comparison dataset
- Reproducible generation settings
- Model-selection report
- No unsupported benchmark claims

**Primary roles**

- Every model-facing AI role

### Lesson 09 — Model API Integration

**Prerequisites**

- Lessons 01-08

**Topics covered**

- Provider authentication
- Message and response formats
- Streaming
- Structured output
- Tool or function calling
- Image, audio, and document input
- Conversation state
- Token accounting
- Rate limits
- Retry policy
- Timeout policy
- Provider error classification
- Fallback models
- Request tracing
- Usage and cost attribution
- Provider-independent adapters

**Primary tools**

- Native provider SDKs
- HTTPX
- Pydantic
- Redis
- OpenTelemetry

**Business implementation**

Build a multi-provider model gateway supporting streaming, schema-constrained output, bounded
retries, tracing, and cost tracking.

**Completion evidence**

- Provider-specific code is isolated
- Invalid structured output cannot reach business logic
- Fallback behavior is tested
- Cost is attributable by user and tenant

**Primary roles**

- Applied AI Engineer
- Generative AI Engineer
- Forward-Deployed AI Engineer
- AI Solutions Architect

### Lesson 10 — Prompt and Context Engineering

**Prerequisites**

- Lessons 08-09

**Topics covered**

- Instruction hierarchy
- Task definition
- Output contracts
- Few-shot examples
- Prompt templates
- Delimiters
- Untrusted content separation
- Context selection
- Context compression
- Structured generation
- Prompt versioning
- Prompt regression tests
- Multilingual prompts
- Prompt injection awareness
- Prompting versus RAG or fine-tuning

**Primary tools**

- Provider SDK
- Pydantic
- Prompt registry
- MLflow or equivalent experiment tracker
- Evaluation harness

**Business implementation**

Create a tested prompt package for ticket classification, extraction, prioritization, and draft
responses.

**Completion evidence**

- Every prompt has a version and evaluation set
- Untrusted text is separated from instructions
- Cost and failure behavior are measured
- Prompt changes run through regression tests

**Primary roles**

- Applied AI Engineer
- Generative AI Engineer
- NLP Engineer
- AI UX and Conversation Designer

### Lesson 11 — Applied LLM Product

**Prerequisites**

- Lessons 01-10

**Topics covered**

- End-to-end LLM product architecture
- Classification
- Structured extraction
- Priority recommendation
- Draft generation
- Human editing and approval
- Streaming user experience
- Conversation persistence
- Feedback capture
- Prompt and model version traceability
- Cost tracking
- Abstention
- Product metrics
- Deployment of a model-backed feature

**Primary tools**

- FastAPI
- PostgreSQL
- Redis
- Hosted model API
- Pydantic
- OpenTelemetry
- React or a minimal user interface

**Business implementation**

Build the first complete AI support-ticket assistant.

**Completion evidence**

- Business and model metrics exist
- Drafts require human approval
- Feedback and edits are recorded
- Every output is traceable

**Primary roles**

- Applied AI Engineer
- Generative AI Engineer
- AI Product Manager
- Forward-Deployed AI Engineer

## Retrieval and RAG

### Lesson 12 — Embeddings and Semantic Retrieval

**Prerequisites**

- Lessons 06, 08-11

**Topics covered**

- Embedding models
- Vector dimensions and normalization
- Cosine similarity, dot product, and Euclidean distance
- Lexical retrieval
- BM25
- Dense retrieval
- Hybrid retrieval
- Approximate nearest-neighbour indexes
- Metadata filters
- Cross-encoder reranking
- Query expansion
- Retrieval latency
- Relevance labelling
- Retrieval metrics

**Primary tools**

- sentence-transformers
- pgvector
- OpenSearch or Elasticsearch
- FAISS for local experiments
- Cross-encoder reranker

**Business implementation**

Build a policy-search service and compare lexical, dense, hybrid, and reranked results.

**Completion evidence**

- Labelled query set
- Baseline comparison
- Permission filtering
- Retrieval latency and quality report

**Primary roles**

- Applied AI Engineer
- Generative AI Engineer
- Search and Ranking Engineer
- NLP Engineer

### Lesson 13 — Document Ingestion and Chunking

**Prerequisites**

- Lessons 03, 06, 12

**Topics covered**

- PDF, HTML, email, and Office parsing
- OCR and scanned pages
- Tables, images, and captions
- Cleaning and normalization
- Language detection
- Exact and near deduplication
- Metadata enrichment
- Document versions
- Chunk identifiers
- Fixed, semantic, structure-aware, parent-child, table-aware, and code-aware chunking
- Incremental indexing
- Delete propagation
- Permission metadata
- Queue-based ingestion

**Primary tools**

- Document parsers
- OCR engine or cloud document service
- PostgreSQL
- Object storage
- Queue and worker

**Business implementation**

Build a versioned, permission-aware document-ingestion service.

**Completion evidence**

- Every chunk retains provenance
- Reprocessing is idempotent
- Deleted content leaves the index
- Chunking strategies are evaluated

**Primary roles**

- Applied AI Engineer
- AI Data Engineer
- Document AI Engineer
- Search Engineer

### Lesson 14 — Production RAG

**Prerequisites**

- Lessons 01-13

**Topics covered**

- RAG architecture
- Query classification
- Query rewriting
- Query decomposition
- Hybrid retrieval
- Reranking
- Context assembly
- Evidence packets
- Grounded generation
- Citations
- Abstention
- Conversational retrieval
- Multi-query and multi-stage retrieval
- Hierarchical retrieval
- Structured-data and SQL retrieval
- Graph-enhanced retrieval selection
- Multimodal retrieval awareness
- Knowledge freshness
- Permission-aware caching
- Tenant isolation
- Retrieval observability

**Primary tools**

- FastAPI
- PostgreSQL and pgvector
- OpenSearch
- Redis
- Reranking model
- Model API
- OpenTelemetry

**Business implementation**

Build the enterprise knowledge assistant with citations, access control, evaluation, incremental
updates, and feedback.

**Completion evidence**

- Retrieval and generation evaluated separately
- Citations are verifiable
- Unsupported questions abstain
- Unauthorized documents never enter context

**Primary roles**

- Applied AI Engineer
- Generative AI Engineer
- Search Engineer
- Forward-Deployed AI Engineer

## Evaluation, data, and agents

### Lesson 15 — AI Evaluation Engineering

**Prerequisites**

- Lessons 04, 07-14

**Topics covered**

- Evaluation requirements
- Golden datasets
- Representative sampling
- Difficult-case mining
- Test contamination
- Annotation guidelines
- Inter-annotator agreement
- Exact-match and schema checks
- Retrieval metrics
- Groundedness and citation checks
- Pointwise and pairwise judges
- Rubric-based evaluation
- Judge calibration
- Human evaluation
- Online feedback
- A/B and canary evaluation
- Agent evaluation foundations
- Cost and latency evaluation
- CI regression gates

**Primary tools**

- pytest
- MLflow
- Custom evaluation code
- Ragas or DeepEval
- promptfoo
- Phoenix, LangSmith, or equivalent

**Business implementation**

Build an evaluation platform for prompts, models, RAG changes, adapters, and agents.

**Completion evidence**

- Versioned evaluation datasets
- Calibrated model judges
- Human-review workflow
- CI quality gates
- Slice-level reporting

**Primary roles**

- AI Evaluation Engineer
- AI Safety Engineer
- Applied AI Engineer
- Every model-building role

### Lesson 16 — AI Data Engineering

**Prerequisites**

- Lessons 06, 13, 15

**Topics covered**

- Data acquisition and provenance
- Consent and licensing
- Data contracts
- Schema validation
- Cleaning and normalization
- Deduplication
- PII detection and redaction
- Quality filtering
- Train, validation, and test splits
- Leakage prevention
- Raw, instruction, conversation, tool, preference, ranking, reward, multimodal, evaluation, and safety data
- Human and expert annotation
- Synthetic data
- Rejection sampling
- Weak supervision
- Active learning
- Difficult-example mining
- Dataset versioning and lineage
- Retention and deletion

**Primary tools**

- Python
- SQL
- Polars or pandas
- Hugging Face Datasets
- Parquet
- DVC
- Spark when required
- Airflow or Dagster

**Business implementation**

Build an auditable training- and evaluation-data pipeline.

**Completion evidence**

- Source registry and data contracts
- PII and deduplication reports
- Leakage tests
- Dataset card
- Rebuildable versioned dataset

**Primary roles**

- AI Data Engineer
- Model Training Engineer
- Post-Training Engineer
- AI Evaluation Engineer
- Machine Learning Engineer

### Lesson 17 — Tool Calling and Controlled Workflows

**Prerequisites**

- Lessons 03-06, 09-11, 15

**Topics covered**

- Tool schemas
- JSON Schema
- Argument validation
- Tool selection
- Sequential and parallel calls
- Result normalization
- Read versus write tools
- State machines
- Workflow graphs
- Durable state
- Checkpointing
- Idempotency
- Retries and timeouts
- Compensation
- Human approval
- Step, time, and spending limits
- Tool permissions
- Audit logs
- Task-completion evaluation

**Primary tools**

- Native provider tool calling
- Pydantic
- PostgreSQL
- Redis
- Explicit workflow code
- LangGraph or one selected workflow framework

**Business implementation**

Build a support-resolution workflow that reads customer and order data, proposes a refund,
requires approval, and updates the ticket.

**Completion evidence**

- Unauthorized actions fail
- Duplicate actions are prevented
- Partial failures recover or compensate
- Task and invalid-action metrics exist

**Primary roles**

- Applied AI Engineer
- Generative AI Engineer
- AI Security Engineer
- Forward-Deployed AI Engineer

### Lesson 18 — MCP and Agent Integration

**Prerequisites**

- Lessons 09, 15, 17

**Topics covered**

- MCP clients and servers
- Tools, resources, and prompts
- Transport
- Capability negotiation
- Tool discovery
- Authentication and authorization
- Identity propagation
- Server trust
- Allowlists
- Logging and audit
- Prompt injection through tool results
- Agent-to-agent concepts
- Workflow handoffs
- Shared-context risks
- Cross-agent authorization
- Multi-agent selection criteria

**Primary tools**

- MCP SDK
- OAuth or service identity
- JSON Schema
- OpenTelemetry

**Business implementation**

Expose the policy-search tool through a secured MCP server and integrate it into the support
workflow.

**Completion evidence**

- Only approved servers are trusted
- User identity reaches authorization
- Capabilities are restricted
- Every operation is traceable

**Primary roles**

- Applied AI Engineer
- Generative AI Engineer
- Forward-Deployed AI Engineer
- AI Security Engineer
- AI Solutions Architect

## Model training and post-training

### Lesson 19 — PyTorch and Training Fundamentals

**Prerequisites**

- Lessons 01-04, 08, 15-16

**Topics covered**

- Tensors
- Parameters
- Activations
- Gradients
- Forward pass
- Loss
- Backpropagation
- Optimizers
- Learning rates and schedules
- Batch size
- Gradient accumulation
- Validation
- Checkpoints
- Early stopping
- Overfitting
- Gradient clipping
- FP32, FP16, and BF16
- GPU memory
- Profiling
- Experiment tracking

**Primary tools**

- PyTorch
- MLflow or TensorBoard
- PyTorch Profiler

**Business implementation**

Build a reproducible small text-classifier training pipeline before using high-level LLM
trainers.

**Completion evidence**

- Training resumes from checkpoints
- Validation controls checkpoint selection
- Numerical and memory behavior are measured
- Runs record code, data, parameters, and metrics

**Primary roles**

- LLM Engineer
- Model Training Engineer
- Machine Learning Engineer
- Applied Scientist

### Lesson 20 — Tokenizers and Language-Model Training Data

**Prerequisites**

- Lessons 08, 16, 19

**Topics covered**

- Tokenizer configuration
- Vocabulary
- Special tokens
- Chat templates
- Instruction formatting
- Padding and truncation
- Attention masks
- Label masks
- Completion-only loss
- Maximum sequence length
- Sequence packing
- Data collators
- Token-length distribution
- Training-data validation

**Primary tools**

- Transformers
- Hugging Face Datasets
- TRL
- Tokenizer inspection scripts

**Business implementation**

Create and validate the support instruction dataset used by SFT and adapter training.

**Completion evidence**

- Chat template matches the model
- Labels cover only intended tokens
- Length and truncation report exists
- Test data remains isolated

**Primary roles**

- LLM Engineer
- Model Training Engineer
- Post-Training Engineer
- NLP Engineer

### Lesson 21 — Supervised Fine-Tuning

**Prerequisites**

- Lessons 15-16, 19-20

**Topics covered**

- Adaptation decision framework
- Prompting versus RAG versus SFT
- Base versus instruction models
- SFT objective
- Dataset formatting
- Training configuration
- Warmup and schedules
- Loss monitoring
- Validation
- Checkpoint selection
- Catastrophic forgetting
- Behavior regression
- Safety regression
- Full fine-tuning costs and risks

**Primary tools**

- PyTorch
- Transformers
- Datasets
- TRL SFTTrainer
- Accelerate
- MLflow

**Business implementation**

Fine-tune a model for support policy, tone, escalation rules, and structured output.

**Completion evidence**

- Untouched baseline and held-out test set
- Checkpoint comparison
- Task and safety evaluation
- Prompting and RAG comparison

**Primary roles**

- LLM Engineer
- Generative AI Engineer
- Model Training Engineer
- NLP Engineer

### Lesson 22 — LoRA and QLoRA

**Prerequisites**

- Lessons 19-21

**Topics covered**

- Parameter-efficient fine-tuning
- Low-rank adaptation
- Rank and scaling
- Target modules
- Adapter dropout
- Trainable parameter calculation
- Four-bit base-model loading
- NF4
- Double-quantization awareness
- Compute data types
- Paged-optimizer awareness
- Gradient checkpointing
- Adapter checkpoints
- Adapter loading and merging
- Multiple adapters
- Adapter routing
- Adapter serving
- Memory and quality comparison

**Primary tools**

- PEFT
- Transformers
- TRL
- bitsandbytes
- Accelerate
- MLflow

**Business implementation**

Create LoRA and QLoRA versions of the support-policy model and compare them with the SFT and RAG
baselines.

**Completion evidence**

- Target modules and hyperparameters documented
- GPU-memory report
- Quality comparison
- Versioned adapter artifacts
- Serving decision documented

**Primary roles**

- LLM Engineer
- Generative AI Engineer
- Post-Training Engineer
- Model Training Engineer

### Lesson 23 — Preference Data and DPO

**Prerequisites**

- Lessons 15-16, 19-22

**Topics covered**

- Chosen and rejected responses
- Preference rubrics
- Human and AI-generated preference data
- Pair validation
- Bias and annotator disagreement
- DPO intuition
- Policy and reference models
- Preference strength
- Over-optimization
- Helpfulness evaluation
- Policy compliance
- Refusal and over-refusal
- Safety regression

**Primary tools**

- TRL DPOTrainer
- PEFT
- Datasets
- MLflow
- Human annotation interface

**Business implementation**

Preference-optimize the support model for useful, policy-compliant, safe answers.

**Completion evidence**

- Documented preference rubric
- Audited pair quality
- SFT versus DPO comparison
- Refusal and over-refusal results

**Primary roles**

- Post-Training Engineer
- LLM Engineer
- AI Safety Engineer
- Generative AI Engineer

### Lesson 24 — Advanced Post-Training Decisions

**Prerequisites**

- Lessons 19-23

**Topics covered**

- Continued pretraining
- Domain corpus and data mixtures
- Catastrophic forgetting
- Knowledge distillation
- Teacher and student models
- Synthetic training targets
- Reward-model data
- Reward-model training
- PPO-based RLHF awareness
- GRPO
- RLOO
- Verifiable rewards
- Process and outcome rewards
- Model merging
- Multimodal adaptation awareness
- Compute and data decision analysis

**Primary tools**

- PyTorch
- Transformers
- TRL
- Distributed-training framework
- Experiment tracker

**Business implementation**

Produce an adaptation decision report and run a small response-distillation experiment.

**Completion evidence**

- Simpler methods remain baselines
- Compute and data costs are estimated
- Forgetting and safety risks are covered
- Evaluation is defined before training

**Primary roles**

- Post-Training Engineer
- Model Training Engineer
- LLM Engineer
- Applied Scientist

### Lesson 25 — Distributed and Efficient Training

**Prerequisites**

- Lessons 19-24

**Topics covered**

- Data parallelism
- DistributedDataParallel
- FSDP
- DeepSpeed ZeRO
- Tensor- and pipeline-parallel awareness
- Mixed precision
- Gradient accumulation
- Activation checkpointing
- Distributed checkpointing
- NCCL fundamentals
- Multi-GPU launch
- Failure recovery
- Job preemption
- GPU utilization
- Communication overhead
- Training-cost calculation

**Primary tools**

- PyTorch distributed
- Accelerate
- FSDP or DeepSpeed
- NCCL
- GPU monitoring

**Business implementation**

Run a reproducible multi-device QLoRA or small-model training job with checkpoint recovery.

**Completion evidence**

- Multi-device execution
- Checkpoint restore
- Effective batch-size calculation
- Utilization and communication report
- Failure-recovery demonstration

**Primary roles**

- Model Training Engineer
- LLM Engineer
- AI Infrastructure Engineer
- ML Platform Engineer

## Multimodal AI

### Lesson 26 — Multimodal and Document AI

**Prerequisites**

- Lessons 08-16, 19

**Topics covered**

- Image, document, and video inputs
- OCR
- Layout analysis
- Tables and forms
- Key-value extraction
- Document classification
- Vision-language models
- Image preprocessing
- Page and region evidence
- Confidence thresholds
- Human-review routing
- Computer-vision fundamentals
- Classification, detection, segmentation, and tracking awareness
- Multimodal datasets and evaluation

**Primary tools**

- OpenCV
- OCR engine or cloud document service
- Multimodal model API or open model
- PyTorch
- Transformers
- torchvision

**Business implementation**

Build an insurance claim-document review assistant using forms, receipts, and photographs.

**Completion evidence**

- Field extraction and visual understanding evaluated separately
- Evidence links to source page or region
- Low-confidence cases reach human review
- Sensitive images are protected

**Primary roles**

- Multimodal AI Engineer
- Computer Vision Engineer
- Document AI Engineer
- Applied AI Engineer

### Lesson 27 — Speech, Audio, and Voice AI

**Prerequisites**

- Lessons 03, 08-11, 15, 17, 19

**Topics covered**

- Audio fundamentals
- Speech-to-text
- Text-to-speech
- Voice activity detection
- Speaker diarization
- Noise handling
- Streaming audio
- Turn detection
- Interruption and barge-in
- Real-time transport
- Conversation state
- Tool calls during voice sessions
- Human escalation
- Consent and recording policy
- Voice privacy
- Speech and task evaluation

**Primary tools**

- Speech or realtime model APIs
- WebSockets or WebRTC
- Voice activity detector
- Audio-processing library

**Business implementation**

Build a voice support-triage assistant with interruption handling and human escalation.

**Completion evidence**

- End-to-end latency measured
- Turn-taking works
- Transcription and task quality evaluated
- Disclosure and retention policy implemented

**Primary roles**

- Speech and Audio Engineer
- Multimodal AI Engineer
- Generative AI Engineer
- AI UX and Conversation Designer

## Safety and governance

### Lesson 28 — AI Security and Privacy

**Prerequisites**

- Lessons 05-18

**Topics covered**

- Direct and indirect prompt injection
- Jailbreaking
- Sensitive-information disclosure
- Improper output handling
- Excessive agency
- Tool abuse
- System-prompt leakage
- Retrieval poisoning
- Training-data poisoning
- Model extraction
- Membership-inference awareness
- Denial of service
- Supply-chain risk
- User, service, and agent identity
- Least privilege
- Tenant isolation
- Sandboxing
- Network and filesystem restrictions
- PII and data minimization
- Encryption, retention, and deletion
- Security regression testing

**Primary tools**

- OWASP GenAI guidance
- Threat-model templates
- Identity provider
- Secret manager
- promptfoo or equivalent
- PII detection and redaction
- Container sandboxing

**Business implementation**

Build an AI security gateway and adversarial test suite for the support agent.

**Completion evidence**

- Authorization remains outside model control
- Cross-tenant tests pass
- Consequential tools require approval
- Security tests run in CI

**Primary roles**

- AI Security Engineer
- AI Safety Engineer
- Applied AI Engineer
- MLOps Engineer

### Lesson 29 — Responsible AI and Governance

**Prerequisites**

- Lessons 07, 15-16, 23, 28

**Topics covered**

- AI inventory
- Risk classification
- Impact assessments
- Model, system, and dataset cards
- Human oversight
- Bias and subgroup evaluation
- Hallucination risk
- Vendor assessment
- Approval gates
- Audit trails
- Change management
- Incident management
- User recourse
- NIST AI Risk Management Framework
- NIST Generative AI Profile
- ISO/IEC 42001 awareness
- ISO/IEC 23894 awareness
- EU AI Act awareness
- Sector-specific regulatory controls

**Primary tools**

- AI inventory template
- Risk register
- Impact-assessment template
- Documentation templates
- Audit and incident workflows

**Business implementation**

Produce the governance package for the customer-operations AI platform.

**Completion evidence**

- Owners and approval paths are explicit
- Risks map to controls
- Change and incident processes exist
- Human oversight and user recourse are documented

**Primary roles**

- AI Governance Specialist
- AI Product Manager
- AI Safety Engineer
- AI Solutions Architect

## Production and infrastructure

### Lesson 30 — Production Architecture and Reliability

**Prerequisites**

- Lessons 01-18, 28

**Topics covered**

- API, model, retrieval, tool, and evaluation services
- Queue and worker design
- Object, relational, and cache storage
- Multi-tenancy
- Service-level indicators and objectives
- Health and readiness checks
- Retries and backoff
- Circuit breakers
- Bulkheads
- Load shedding
- Graceful degradation
- Provider and model fallback
- Dead-letter queues
- Idempotency
- High availability
- Disaster recovery
- Failure injection

**Primary tools**

- FastAPI
- PostgreSQL
- Redis
- Queue service
- Object storage
- Docker
- Cloud load balancer

**Business implementation**

Harden the Applied AI platform against provider, retrieval, tool, worker, and storage failures.

**Completion evidence**

- SLOs are defined
- Failure behavior is tested
- Retryable writes are safe
- Recovery procedure is demonstrated

**Primary roles**

- Applied AI Engineer
- AI Solutions Architect
- MLOps Engineer
- ML Platform Engineer

### Lesson 31 — Observability, Feedback, and Cost

**Prerequisites**

- Lessons 11, 14-18, 30

**Topics covered**

- Structured logs
- Metrics
- Distributed traces
- Correlation identifiers
- OpenTelemetry Generative AI conventions
- Prompt and model versions
- Retrieval and tool traces
- Token usage
- Latency and throughput
- Cache metrics
- Safety events
- User feedback
- Acceptance and edit rates
- Task-completion metrics
- Cost per request
- Cost per successful task
- Tenant and feature attribution
- Dashboards and alerts
- Sensitive-telemetry redaction

**Primary tools**

- OpenTelemetry
- Prometheus
- Grafana
- Cloud monitoring
- AI tracing platform

**Business implementation**

Create operational, quality, safety, product, and cost dashboards for the enterprise assistant.

**Completion evidence**

- One request is traceable end to end
- Quality and business outcomes appear beside infrastructure metrics
- Cost is attributable
- Sensitive content is protected

**Primary roles**

- Applied AI Engineer
- AI Evaluation Engineer
- MLOps Engineer
- AI Product Manager

### Lesson 32 — Cloud Deployment and Infrastructure

**Prerequisites**

- Lessons 01-06, 28-31

**Topics covered**

- Container registries
- Cloud identity and access management
- Virtual networks
- Load balancers and DNS
- Object storage
- Managed databases and caches
- Queues
- Container and serverless services
- CPU and GPU instances
- Secret managers
- Logging and monitoring
- Cost allocation
- Infrastructure as code
- Environment separation
- Terraform state and modules
- Backups and restore

**Primary tools**

- Docker
- One selected cloud: AWS, Azure, or Google Cloud
- Terraform
- GitHub Actions
- Cloud-native monitoring

**Business implementation**

Deploy the enterprise assistant to one cloud with identity, networking, managed data services,
secrets, monitoring, and budget controls.

**Completion evidence**

- Infrastructure is reproducible
- No long-lived credential is stored in code
- Network access is restricted
- Restore and cost ownership are documented

**Primary roles**

- Applied AI Engineer
- MLOps Engineer
- Forward-Deployed AI Engineer
- AI Solutions Architect

### Lesson 33 — Kubernetes for AI Workloads

**Prerequisites**

- Lessons 25, 30-32

**Topics covered**

- Pods
- Deployments
- Services
- Ingress
- ConfigMaps and Secrets
- Resource requests and limits
- Health checks
- Horizontal autoscaling
- Jobs and scheduled jobs
- Persistent storage
- GPU scheduling
- Rolling deployments
- Canary deployment
- Failure diagnosis
- Helm awareness
- KServe awareness

**Primary tools**

- Kubernetes
- Helm
- Prometheus
- Grafana
- KServe where useful

**Business implementation**

Deploy the model gateway, worker, GPU inference service, and training job to Kubernetes.

**Completion evidence**

- Resources are explicit
- Unhealthy pods leave service
- Rollback works
- GPU scheduling is demonstrated

**Primary roles**

- MLOps Engineer
- ML Platform Engineer
- AI Infrastructure Engineer
- AI Inference Engineer

### Lesson 34 — LLMOps and MLOps

**Prerequisites**

- Lessons 15-16, 21-23, 30-33

**Topics covered**

- Experiment tracking
- Code, data, prompt, model, and adapter versions
- Dataset, prompt, model, adapter, and evaluation registries
- Artifact lineage
- Reproducibility
- AI CI/CD
- Prompt, retrieval, model, and safety gates
- Continuous training
- Trigger criteria
- Staging
- Shadow and canary deployment
- Approval
- Rollback
- Model monitoring
- LLM monitoring
- Data and output drift
- Feedback-to-training workflow

**Primary tools**

- MLflow
- DVC
- GitHub Actions
- Airflow, Dagster, or cloud workflows
- Model registry
- Prompt registry
- Kubernetes when appropriate

**Business implementation**

Build an automated adapter lifecycle from reviewed data through QLoRA training, evaluation,
approval, canary release, monitoring, and rollback.

**Completion evidence**

- Complete lineage
- Quality and safety gates
- Rollback demonstration
- Reviewed feedback-data loop

**Primary roles**

- MLOps Engineer
- ML Platform Engineer
- LLM Engineer
- Applied AI Engineer

### Lesson 35 — Open-Model Serving

**Prerequisites**

- Lessons 19-25, 30-34

**Topics covered**

- Model configuration and tokenizer artifacts
- Safetensors
- Model licences
- Adapter artifacts
- OpenAI-compatible APIs
- Continuous and dynamic batching
- KV cache
- Prefix caching
- Chunked prefill
- Streaming
- Structured generation
- Tool calling
- LoRA serving
- Multi-model serving
- Authentication
- Model and adapter provenance

**Primary tools**

- vLLM or SGLang
- llama.cpp for local or edge awareness
- Hugging Face Hub or private registry
- Prometheus

**Business implementation**

Serve the adapted support model and multiple adapters through a production-compatible API.

**Completion evidence**

- Functional evaluation passes
- Versions are traceable
- Concurrency limits are enforced
- Hosted and self-hosted costs are compared

**Primary roles**

- LLM Engineer
- AI Inference Engineer
- Generative AI Engineer
- AI Infrastructure Engineer

### Lesson 36 — Inference Optimization

**Prerequisites**

- Lessons 25, 31, 33, 35

**Topics covered**

- Time to first token
- Inter-token latency
- End-to-end latency
- Throughput and queue time
- GPU utilization and memory
- INT8 and INT4 quantization
- GPTQ, AWQ, and GGUF awareness
- Continuous batching
- Cache tuning
- Tensor parallelism
- Data-parallel serving
- Distributed inference
- Speculative-decoding awareness
- Model routing
- Load testing
- Capacity planning
- Cost per token and successful task

**Primary tools**

- vLLM or SGLang
- PyTorch Profiler
- NVIDIA Nsight for specialist work
- TensorRT-LLM
- Triton Inference Server
- Load-testing tools

**Business implementation**

Optimize the self-hosted model service and produce a quality, latency, throughput, memory, and
cost report.

**Completion evidence**

- Realistic load test
- Quality measured after every optimization
- Bottlenecks identified through evidence
- Capacity assumptions documented

**Primary roles**

- AI Inference Engineer
- AI Infrastructure Engineer
- LLM Engineer
- MLOps Engineer

## Machine learning

### Lesson 37 — Classical Machine-Learning Foundations

**Prerequisites**

- Lessons 01-07, 15-16

**Topics covered**

- Practical vectors, matrices, probability, and statistics
- Classification, regression, ranking, clustering, forecasting, and anomaly detection
- Features and labels
- Baselines
- Missing values and outliers
- Categorical encoding
- Scaling
- Feature engineering and selection
- Class imbalance
- Dataset and time-based splitting
- Leakage
- Linear and logistic regression
- Decision trees and random forests
- Gradient boosting
- XGBoost, LightGBM, and CatBoost
- Support-vector machines
- Nearest neighbours
- Naive Bayes
- K-means
- PCA
- Isolation forests
- Classification, regression, ranking, and calibration metrics
- Cross-validation
- Error and subgroup analysis
- A/B testing

**Primary tools**

- NumPy
- Polars or pandas
- scikit-learn
- XGBoost, LightGBM, or CatBoost
- Optuna
- MLflow

**Business implementation**

Build a service-level breach predictor and compare simple, linear, tree, and boosted baselines.

**Completion evidence**

- Production-realistic split
- Leakage checks
- Business-aligned metrics
- Calibration and error analysis

**Primary roles**

- Machine Learning Engineer
- Data Scientist
- Applied Scientist
- Applied AI Engineer

### Lesson 38 — Production Machine Learning

**Prerequisites**

- Lessons 06, 15-16, 30-34, 37

**Topics covered**

- Feature pipelines
- Feature-store awareness
- Training pipelines
- Hyperparameter optimization
- Model registry
- Batch inference
- Online inference
- Training-serving consistency
- Shadow and canary deployment
- Input, feature, and output monitoring
- Data and concept drift
- Delayed labels
- Retraining triggers
- Evaluation gates
- Rollback

**Primary tools**

- scikit-learn or boosting library
- MLflow
- Airflow or Dagster
- FastAPI
- Docker
- Monitoring stack

**Business implementation**

Productionize the service-level breach predictor with batch and online scoring, monitoring,
retraining, and controlled release.

**Completion evidence**

- Feature consistency tests
- Version-traceable predictions
- Drift response procedure
- Retraining and rollback demonstration

**Primary roles**

- Machine Learning Engineer
- MLOps Engineer
- ML Platform Engineer
- Data Scientist

### Lesson 39 — Deep Learning for AI Engineers

**Prerequisites**

- Lessons 19, 25, 37-38

**Topics covered**

- Neural layers
- Activations
- Initialization
- Normalization
- Dropout
- Forward and backpropagation
- Losses and optimizers
- CNNs
- Recurrent-model awareness
- Attention and transformers
- Vision transformers
- Embedding models
- Transfer learning
- Frozen versus full fine-tuning
- GPU training
- Export and serving
- Deep-learning monitoring

**Primary tools**

- PyTorch
- torchvision
- Transformers
- MLflow
- ONNX Runtime

**Business implementation**

Build product classification and semantic matching with classical, embedding, and fine-tuned
transformer baselines.

**Completion evidence**

- Non-neural baseline
- Reproducible training
- Evaluation slices
- Serving latency and cost report

**Primary roles**

- Machine Learning Engineer
- Applied Scientist
- NLP Engineer
- Computer Vision Engineer
- Multimodal AI Engineer

## Final core project

### Lesson 40 — Enterprise Applied AI Capstone Implementation

**Prerequisites**

- Lessons 01-39

**Topics covered**

- Product requirements
- Workflow and architecture design
- Authentication and tenant authorization
- Ticket and document ingestion
- Hybrid retrieval and reranking
- Evidence-backed generation
- Structured extraction
- Tool calling and MCP
- Human approval
- Prompt, model, dataset, and adapter versioning
- Evaluation datasets
- LoRA or QLoRA
- DPO experiment
- Multi-provider routing
- Open-model serving
- Security and safety controls
- Cloud deployment
- Logs, metrics, and traces
- Cost controls
- Canary deployment
- Feedback
- Incident management
- Technical and business documentation

**Primary tools**

- The complete selected stack from Lessons 01-39

**Business implementation**

Build and defend the enterprise customer-operations AI platform.

**Completion evidence**

- Product-requirements document
- Architecture decisions
- Threat model
- API and data contracts
- Evaluation dataset and report
- Dataset, adapter, and system cards
- Deployment and rollback
- Load and failure-injection reports
- Business-outcome report
- Technical presentation

**Primary roles**

- Applied AI Engineer
- Generative AI Engineer
- LLM Engineer
- Machine Learning Engineer
- Forward-Deployed AI Engineer
- AI Solutions Architect

# Optional specialization lessons

The specialization lessons do not repeat the core. Each combines the relevant core lessons into
one role-specific production project.

### Lesson 41 — Applied AI Engineer Specialization

**Core prerequisites**

- Lessons 01-40

**Topics deepened**

- Product discovery
- Enterprise APIs and data integration
- User-facing AI product design
- RAG and controlled agents
- Evaluation and feedback loops
- Model-adaptation decisions
- TypeScript and React fundamentals
- Cloud delivery
- Security
- Business metrics
- Product ownership

**Specialization project**

Deploy a user-facing AI workflow to real infrastructure and measure user and business outcomes.

**Roles additionally covered**

- AI Product Manager technical bridge
- AI Solutions Architect implementation bridge
- AI UX and Conversation Designer engineering bridge

### Lesson 42 — Generative AI Engineer Specialization

**Core prerequisites**

- Lessons 01-36 and 40

**Topics deepened**

- LLM behavior
- Prompt and context systems
- Advanced RAG
- Agent workflows
- Multimodal APIs
- Voice and document inputs
- Evaluation
- Safety
- Cost optimization
- SFT, LoRA, QLoRA, and DPO practical use
- Open-model serving

**Specialization project**

Build a multi-model, multimodal production GenAI product.

**Roles additionally covered**

- NLP Engineer application path
- AI UX and Conversation Designer

### Lesson 43 — LLM Engineer Specialization

**Core prerequisites**

- Lessons 15-25 and 34-36

**Topics deepened**

- Training-data systems
- Tokenizers
- SFT
- LoRA and QLoRA
- DPO
- Continued pretraining
- Distillation
- Reward-model and RL-based method selection
- Distributed training
- Quantization
- Serving and performance

**Specialization project**

Build a complete domain-model adaptation, evaluation, registry, and serving pipeline.

**Roles additionally covered**

- Model Training Engineer
- Post-Training Engineer
- NLP Engineer training path
- Applied Scientist bridge

### Lesson 44 — MLOps and ML Platform Specialization

**Core prerequisites**

- Lessons 01-06, 15-16, 25, 30-39

**Topics deepened**

- Kubernetes
- Terraform
- Workflow orchestration
- Registries and lineage
- Training-job scheduling
- Feature and data platforms
- Multi-tenancy
- Identity
- Observability
- CI/CD and continuous training
- Developer experience
- Platform APIs

**Specialization project**

Build a self-service training, evaluation, approval, deployment, and monitoring platform.

**Roles additionally covered**

- MLOps Engineer
- ML Platform Engineer
- AI Data Engineer platform path

### Lesson 45 — AI Evaluation and Safety Specialization

**Core prerequisites**

- Lessons 15-16, 23-24, 28-31, 34, 40

**Topics deepened**

- Evaluation dataset design
- Human evaluation
- Judge calibration
- Statistics and uncertainty
- Agent evaluation
- Safety taxonomies
- Adversarial testing
- Red teaming
- Refusal and over-refusal
- Capability and misuse evaluation
- Release gates
- Incident analysis

**Specialization project**

Build an evaluation and adversarial-testing service that blocks unsafe or regressed releases.

**Roles additionally covered**

- AI Evaluation Engineer
- AI Safety Engineer
- AI Data and Annotation Engineer
- AI Governance Specialist technical bridge

### Lesson 46 — AI Security Specialization

**Core prerequisites**

- Lessons 05-06, 17-18, 28-34, 40

**Topics deepened**

- User, service, and agent identity
- Authorization and policy enforcement
- Tool permissions
- Prompt injection
- Retrieval security
- Sandboxing
- Cloud security
- Supply-chain security
- Tenant isolation
- Threat modelling
- Security tests
- Incident response

**Specialization project**

Build a secured agent execution environment with centralized policy enforcement.

**Roles additionally covered**

- AI Security Engineer
- AI Solutions Architect security path

### Lesson 47 — Machine Learning Engineer Specialization

**Core prerequisites**

- Lessons 01-07, 15-16, 19, 30-40

**Topics deepened**

- Classical ML
- Deep learning
- Feature and training pipelines
- Batch and online inference
- Feature-store decisions
- Monitoring
- Drift
- Retraining
- Experimentation
- ML system design
- Applied LLM integration

**Specialization project**

Build a complete predictive ML product and platform.

**Roles additionally covered**

- Data Scientist for ML
- Applied Scientist production bridge

### Lesson 48 — AI Infrastructure and Inference Specialization

**Core prerequisites**

- Lessons 01-06, 19, 25, 30-36

**Topics deepened**

- Linux
- Networking
- C++ fundamentals
- GPU architecture
- CUDA
- NCCL
- GPU profiling
- vLLM or SGLang internals
- TensorRT-LLM
- Triton
- Distributed training infrastructure
- Distributed inference
- Storage and scheduling
- Capacity planning
- Reliability

**Specialization project**

Build and benchmark a multi-GPU or multi-node inference service.

**Roles additionally covered**

- AI Infrastructure Engineer
- AI Inference Engineer
- Edge AI serving bridge

### Lesson 49 — Search and Recommendation Specialization

**Core prerequisites**

- Lessons 06, 12-16, 30-39

**Topics deepened**

- Query understanding
- BM25 and dense retrieval
- Approximate nearest neighbours
- Candidate generation
- Collaborative and content-based recommendation
- Reranking
- Learning to rank
- Personalization
- Exploration and exploitation
- Feedback bias
- Offline evaluation
- A/B testing
- Low-latency serving

**Specialization project**

Build a two-stage retrieval, recommendation, and ranking system with online metrics.

**Roles additionally covered**

- Search and Ranking Engineer
- Recommender Systems Engineer

### Lesson 50 — Multimodal AI Specialization

**Core prerequisites**

- Lessons 03, 08-18, 19, 25-27, 35-40

**Topics deepened**

- Computer vision
- Document intelligence
- Speech and audio
- Video
- Vision-language and audio-language models
- Multimodal datasets
- Multimodal retrieval
- Streaming
- Modality-specific evaluation
- Human review
- Edge deployment awareness
- Robotics and autonomy prerequisite bridge

**Specialization project**

Build a multimodal business workflow combining documents, images, audio, and human review.

**Roles additionally covered**

- Computer Vision Engineer
- Speech and Audio Engineer
- Multimodal AI Engineer
- Edge AI Engineer bridge
- Robotics and Autonomy Engineer bridge

**Scope boundary**

The current 57-lesson curriculum does not provide a complete robotics or embedded-systems career
specialization. A full robotics path would additionally require dedicated C++, ROS, control,
sensor fusion, localization, mapping, planning, simulation, and real-time lessons. A full Edge
AI path would require dedicated mobile and embedded runtime, power, memory, and device-security
lessons. These topics are not silently omitted; they are recorded as extensions.

### Lesson 51 — Forward-Deployed AI Engineer Specialization

**Core prerequisites**

- Lessons 01-18, 28-34, and 40

**Topics deepened**

- Customer discovery
- Rapid prototyping
- Enterprise data discovery
- API and system integrations
- Cloud delivery
- Security and compliance
- Workflow redesign
- User training
- Stakeholder communication
- Technical presentations
- Reusable deployment patterns
- Adoption and business metrics

**Specialization project**

Build a reusable customer deployment package for one industry.

**Roles additionally covered**

- Forward-Deployed AI Engineer
- AI Solutions Architect
- Applied AI consultant path

# Interview-preparation lessons

### Lesson 52 — Coding and Python Interviews

**Prerequisites**

- Lessons 01-06 and relevant implementation lessons

**Topics covered**

- Arrays and strings
- Hash maps and sets
- Stacks and queues
- Trees and graphs
- Heaps
- Sorting and searching
- Basic dynamic programming
- Time and space complexity
- Python iterators and generators
- Async behavior
- Error handling
- Testing
- API implementation
- AI-oriented coding exercises

**Practice format**

- Timed coding
- Code review
- Debugging
- Follow-up optimization
- Production-quality extension

### Lesson 53 — SQL Interviews

**Prerequisites**

- Lesson 06 and data-focused lessons

**Topics covered**

- Joins
- Aggregations
- Subqueries and CTEs
- Window functions
- Query debugging
- Indexes and query plans
- Transactions
- Schema design
- Analytics queries
- Multi-tenant data questions
- Model and feedback data queries

**Practice format**

- Query writing
- Result validation
- Performance discussion
- Data-model design

### Lesson 54 — Applied AI Case Interviews

**Prerequisites**

- Lessons 07-18, 28-32, and 40

**Topics covered**

- Determine whether AI is appropriate
- Define users, workflow, and baseline
- Select prompting, RAG, tools, fine-tuning, or ML
- Define human approval
- Select metrics
- Estimate latency and cost
- Identify privacy and security risks
- Plan pilot, rollout, feedback, and rollback
- Communicate uncertainty

**Practice format**

- Ambiguous business cases
- Build-versus-buy decisions
- Whiteboard architecture
- Executive and engineering explanation

### Lesson 55 — LLM and Model-Training Interviews

**Prerequisites**

- Lessons 08-25 and 35-36

**Topics covered**

- Tokens and attention
- Context limitations
- Embeddings
- Retrieval and reranking
- SFT
- LoRA and QLoRA
- DPO
- Continued pretraining
- Distillation
- Distributed training
- Quantization
- Serving
- Evaluation
- Training and inference debugging

**Practice format**

- Concept questions
- Training failure scenarios
- Data and evaluation design
- Adaptation decision cases
- Performance tradeoffs

### Lesson 56 — AI System-Design Interviews

**Prerequisites**

- Lessons 05-40

**Systems covered**

- Enterprise RAG
- Support agent
- Model gateway
- Evaluation platform
- Training platform
- Inference platform
- Search system
- Recommendation system
- Fraud or anomaly detection
- Multimodal workflow

**Design dimensions**

- Requirements
- Scale
- Data
- Models
- Evaluation
- APIs
- Storage
- Reliability
- Security
- Monitoring
- Cost
- Deployment
- Rollback

### Lesson 57 — Portfolio and Project Deep-Dive Interviews

**Prerequisites**

- At least three completed portfolio projects
- Lesson 40

**Topics covered**

- Business problem
- User and baseline
- Architecture
- Data
- Model choice
- Evaluation
- Failure analysis
- Security
- Deployment
- Monitoring
- Cost
- Scaling
- Tradeoffs
- Lessons learned
- Technical presentation
- Behavioral examples

**Practice format**

- Five-minute project summary
- Thirty-minute technical defense
- Architecture review
- Incident and failure questions
- Improvement proposal

# Readiness checkpoints and assessments

## Entry Checkpoint — Junior Applied AI or Generative AI Readiness

This is preserved as an entry checkpoint rather than counted among the five formal assessments.

**Required evidence**

- Production Python
- API development
- SQL
- Model API integration
- Structured outputs
- RAG
- Basic tool calling
- Evaluation
- Docker
- One deployed project
- Security fundamentals

**Minimum lesson coverage**

- Lessons 01-18
- Lesson 28
- Lessons 30-32
- One deployed project

## Assessment 01 — Applied AI Engineer Readiness

**Required evidence**

- Business discovery
- End-to-end product ownership
- Production RAG
- Controlled agent
- Evaluation platform
- Feedback loop
- Cloud deployment
- Reliability
- Security
- Cost analysis
- Model-adaptation project
- Technical presentation

**Minimum lesson coverage**

- Lessons 01-40
- Lesson 41 recommended
- Interview Lessons 52-57

## Assessment 02 — LLM Engineer Readiness

**Required evidence**

- PyTorch
- Training data
- SFT
- LoRA
- QLoRA
- DPO
- Distributed-training fundamentals
- Open-model serving
- Quality benchmarks
- Performance benchmarks

**Minimum lesson coverage**

- Lessons 01-25
- Lessons 31 and 34-36
- Lesson 43
- Interview Lessons 52, 55-57

## Assessment 03 — MLOps or ML Platform Readiness

**Required evidence**

- Docker
- Cloud
- Kubernetes
- CI/CD
- Workflow orchestration
- Registries
- Monitoring
- Terraform
- Multi-tenant design
- Rollback demonstration

**Minimum lesson coverage**

- Lessons 01-06
- Lessons 15-16
- Lesson 25
- Lessons 30-36
- Lesson 44
- Interview Lessons 52, 53, 56-57

## Assessment 04 — Evaluation, Safety, or Security Readiness

**Required evidence**

- Golden datasets
- Human evaluation
- Model judges
- Statistical analysis
- Adversarial tests
- Security tests
- Regression gates
- Incident analysis

**Minimum lesson coverage**

- Lessons 04, 07-18, 23-24, and 28-34
- Lesson 45 or 46
- Interview Lessons 54-57

## Assessment 05 — Machine Learning Engineer Readiness

**Required evidence**

- Classical ML
- Deep learning
- Data and feature pipelines
- Training
- Batch and online deployment
- Monitoring
- Drift
- Retraining
- ML system design

**Minimum lesson coverage**

- Lessons 01-07
- Lessons 15-16
- Lessons 19 and 30-40
- Lesson 47
- Interview Lessons 52-57

# Role-to-lesson coverage

This matrix maps every role branch in the detailed outline to the lessons that provide its
required knowledge.

| Role | Primary lessons | Specialization or boundary |
|---|---|---|
| Applied AI Engineer | 01-18, 28-40 | Lesson 41 |
| Generative AI Engineer | 08-18, 21-36, 40 | Lesson 42 |
| LLM Engineer | 15-25, 31, 34-36 | Lesson 43 |
| Model Training Engineer | 16, 19-25, 31, 33-36 | Lessons 43 and 48 |
| Post-Training Engineer | 15-16, 19-25, 28-29, 34-36 | Lessons 43 and 45 |
| Machine Learning Engineer | 01-07, 15-16, 19, 30-40 | Lesson 47 |
| Data Scientist for ML | 06-07, 15-16, 31, 37-39 | Lesson 47 supports production depth |
| Applied Scientist | 15-16, 19-25, 37-39 | Lessons 43 or 47; research depth may require further study |
| MLOps Engineer | 01-06, 25, 30-39 | Lesson 44 |
| ML Platform Engineer | 01-06, 16, 25, 30-39 | Lesson 44 |
| AI Infrastructure Engineer | 01-06, 25, 30-36 | Lesson 48 |
| AI Inference Engineer | 19, 22, 25, 30-36 | Lesson 48 |
| AI Data Engineer | 03, 06, 13, 16, 32-34, 38 | Lesson 44 supports platform depth |
| AI Data or Annotation Engineer | 15-16, 20, 23, 26-27 | Lesson 45 supports evaluation depth |
| AI Evaluation Engineer | 04, 15, 23, 28-31, 34 | Lesson 45 |
| AI Safety Engineer | 15, 23-24, 28-31, 34 | Lesson 45 |
| AI Security Engineer | 05-06, 17-18, 28-34 | Lesson 46 |
| NLP Engineer | 08-25, 35-39 | Lessons 42 or 43 |
| Computer Vision Engineer | 19, 25-26, 35-36, 39 | Lesson 50 |
| Speech and Audio Engineer | 03, 19, 25, 27, 35-36, 39 | Lesson 50 |
| Multimodal AI Engineer | 08-18, 26-27, 35-36, 39 | Lesson 50 |
| Search and Ranking Engineer | 06, 12-16, 30-38 | Lesson 49 |
| Recommender Systems Engineer | 06, 15-16, 30-39 | Lesson 49 |
| Robotics and Autonomy Engineer | 03, 19, 25-33, 36, 39, 50 | Career bridge only; dedicated robotics extension required |
| Edge AI Engineer | 19, 22, 26-27, 35-36, 39, 48, 50 | Career bridge only; dedicated edge extension required |
| Forward-Deployed AI Engineer | 01-18, 28-34, 40 | Lesson 51 |
| AI Solutions Architect | 05-18, 28-36, 40-41, 51 | Architecture and customer-delivery route |
| AI Product Manager | 07, 11, 15, 28-31, 40-41, 51 | Technical product route |
| AI Governance Specialist | 15-16, 28-29, 31, 34, 40, 45-46 | Governance and assurance route |
| AI UX or Conversation Designer | 07-11, 15, 17, 27-29, 40-42 | Interaction-design route |

# Portfolio coverage

| Portfolio artifact | Primary lesson |
|---|---:|
| Reproducible AI engineering repository | 01 |
| Typed production Python package | 02 |
| Async processing service | 03 |
| AI testing harness | 04 |
| Support-workflow backend | 05-06 |
| Applied AI discovery package | 07 |
| Model-behavior laboratory | 08 |
| Multi-provider model gateway | 09 |
| Tested prompt package | 10 |
| LLM support assistant | 11 |
| Semantic and hybrid search service | 12 |
| Document-ingestion pipeline | 13 |
| Enterprise RAG platform | 14 |
| AI evaluation platform | 15 |
| Training-data pipeline | 16 |
| Controlled tool-using agent | 17 |
| Secured MCP integration | 18 |
| PyTorch training pipeline | 19 |
| Validated language-model dataset | 20 |
| SFT model | 21 |
| LoRA and QLoRA adapters | 22 |
| DPO model | 23 |
| Adaptation and distillation report | 24 |
| Distributed training run | 25 |
| Multimodal document workflow | 26 |
| Voice support assistant | 27 |
| AI security gateway | 28 |
| Governance package | 29 |
| Reliable production architecture | 30 |
| Quality and cost dashboards | 31 |
| Cloud deployment | 32 |
| Kubernetes AI workloads | 33 |
| LLMOps pipeline | 34 |
| Open-model serving platform | 35 |
| Inference benchmark and capacity plan | 36 |
| Classical ML prediction system | 37 |
| Production ML platform | 38 |
| Deep-learning application | 39 |
| Enterprise Applied AI capstone | 40 |

# Source-topic traceability

## Detailed outline section mapping

| Detailed outline section | Lessons |
|---|---|
| Purpose and primary career target | 07, 40-41, 51 |
| Related AI roles | 41-51 and role-to-lesson matrix |
| Recommended learning sequence | 01-57 in this file |
| Standard lesson and project structures | Applied to every generated lesson |
| Core industry tool stack | 01-39; consolidated in 40 |
| Engineering foundations | 01-06 |
| Applied AI product engineering | 07 and 11; deepened in 41 and 51 |
| Foundation-model and LLM engineering | 08-11 |
| Embeddings, retrieval, and RAG | 12-14 |
| Evaluation and feedback engineering | 15 and 31; deepened in 45 |
| AI data engineering | 16; platform extension in 44 |
| Tool use, agents, and MCP | 17-18 |
| Model adaptation and post-training | 19-25; deepened in 43 |
| Multimodal, document, speech, and voice AI | 26-27; deepened in 50 |
| AI safety, security, privacy, and governance | 28-29; deepened in 45-46 |
| Production AI system engineering | 30-31 |
| Cloud, containers, and infrastructure | 01, 32-33 |
| LLMOps and MLOps | 34; deepened in 44 |
| Open-model serving and inference optimization | 35-36; deepened in 48 |
| Classical machine learning | 37-38; deepened in 47 |
| Deep learning and complete ML engineering | 19, 25, 39; deepened in 47 |
| Role-specific learning branches | 41-51 and role matrix |
| Portfolio sequence | Practical artifacts from 01-40 |
| Specialist project options | 42-50 |
| Capstone | 40 |
| Interview outline | 52-57 |
| Job-readiness gates | Entry Checkpoint and Assessments 01-05 |
| Topics to deprioritize | Boundary table below |
| Recommended final positioning | 40-41 and 51 |
| Recommended supporting specialization | Select one of 42-50 |
| Reference standards | 28-29 and current-source checks in each lesson |

## Deprioritized-topic boundaries

| Topic | Curriculum treatment |
|---|---|
| Frontier-model pretraining from scratch | Architecture and decision awareness in 24-25 and 43; not a core implementation |
| Reimplementing every research paper | Excluded; implement only methods required by a lesson or role |
| Mathematical proofs unrelated to engineering | Excluded; practical mathematics appears in 19, 24-25, 37, and 39 |
| Exotic PEFT algorithms | LoRA and QLoRA are implemented in 22; alternatives are awareness-only |
| Custom CUDA kernels | Awareness in 36; advanced only in Specialization 48 |
| Multi-agent systems without business need | Selection criteria and risks in 17-18; not a default architecture |
| Novel reinforcement-learning research | Decision awareness in 24 and Specialization 43 |
| GANs outside relevant media roles | Not included in the core; add only for a specific image-generation role |
| Robotics outside autonomy roles | Career bridge in 50; dedicated extension required |
| Every cloud provider | One cloud implemented deeply in 32; service mapping for others |
| Every vector database | pgvector and OpenSearch implemented in 12-14; alternatives compared |
| Every agent framework | Native workflows first in 17; one framework selected |
| Benchmark optimization without business evaluation | Explicitly prohibited in 15, 31, 36, and 40 |

# Generation order and status

| Lesson range | Status |
|---|---|
| Lesson 01 | Generated |
| Lessons 02-40 | Generate sequentially |
| Lessons 41-51 | Generate after the learner selects a role |
| Lessons 52-57 | Generate after core projects exist |
| Entry checkpoint | Run after the minimum junior lesson set |
| Assessments 01-05 | Run after the corresponding specialization path |

## Final completeness rule

The curriculum is complete only when:

- All 40 core lessons have separate lesson files.
- Every source topic in the traceability tables has a lesson location.
- At least one specialization lesson is completed.
- The six interview areas are practiced.
- The appropriate readiness assessment is passed.
- Every generated lesson meets the production lesson standard.
- No tool is taught without its business use, limitations, testing, security, and operational
  implications.
- No project is called production-ready without evaluation, deployment, monitoring, cost, and
  rollback evidence.
