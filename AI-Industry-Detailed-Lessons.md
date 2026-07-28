# Detailed AI Industry Lessons

Updated: July 28, 2026

## How to use this file

This file converts the separate industry outline into an implementation-focused lesson plan. It is ordered for a learner who wants to begin with Applied AI and Generative AI, move into model adaptation and production operations, and learn classical machine learning afterward.

Each lesson contains:

- Employment outcome
- Business problem
- Learning objectives
- Required concepts
- Tools
- Guided implementation
- Practical assignment
- Required deliverables
- Evaluation criteria
- Production concerns
- Interview preparation

Complete the lessons in order until the role-selection section. After the shared core, choose one primary specialization and one supporting specialization.

## Completion standards

A lesson is complete only when the learner can:

- Explain the topic without relying on framework terminology
- Implement a minimal version
- Implement the production version with the selected tools
- Test normal, boundary, and failure cases
- Measure quality, latency, and cost
- Explain security and privacy risks
- Defend the design in an interview
- Document the implementation for another engineer

A project is complete only when it includes:

- Source code
- Reproducible setup
- Automated tests
- Evaluation data
- Measured results
- Docker configuration
- CI checks
- Security notes
- Architecture documentation
- Deployment instructions
- Monitoring plan
- Cost estimate

### Python and .NET implementation policy

Python remains the primary teaching and reference path for model, data, evaluation, and training work. Learners targeting .NET roles complete the parallel application-engineering labs in model APIs, RAG, controlled agents, MCP, production architecture, observability, and the capstone.

The .NET lane must:

- Use C# and ASP.NET Core with a supported provider SDK or supported `Microsoft.Extensions.AI` abstraction
- Preserve the same API contracts, evaluation data, authorization rules, telemetry fields, and failure cases as the Python reference
- Keep provider and framework code behind application-owned interfaces
- Pin supported package versions and avoid depending on preview-only behavior
- Produce runnable code, automated tests, traces, measured quality-latency-cost results, and a short design decision record

The learner does not need to duplicate the entire capstone in two languages. The chosen backend must satisfy the same acceptance evidence.

## Learning environment

### Employment outcome

Create a reproducible workstation for all later AI engineering work.

### Business problem

AI projects frequently fail to reproduce because developers mix package versions, credentials, local services, datasets, and generated artifacts.

### Learning objectives

- Create isolated Python environments
- Lock dependencies
- Manage configuration without committing secrets
- Run local databases and services
- Use Git branches and pull requests
- Enforce code quality automatically

### Required concepts

- Python versions
- Virtual environments
- Package resolution
- Dependency locking
- Environment variables
- Secret management
- Git history
- Branching
- Continuous integration
- Local and production configuration

### Tools

- Python
- uv
- Git
- GitHub
- Docker
- Docker Compose
- Ruff
- mypy or Pyright
- pre-commit
- GitHub Actions

### Guided implementation

- Install and verify Python
- Create a project with `pyproject.toml`
- Add development and production dependency groups
- Create typed application settings
- Load local settings from environment variables
- Add `.gitignore`
- Add linting, formatting, type checking, and tests
- Create a Dockerfile
- Create a Compose configuration
- Add a CI workflow

### Practical assignment

Create an `ai-industry-labs` repository containing:

- Application package
- Test package
- Configuration module
- Health-check command
- Dockerfile
- Compose file
- CI workflow
- Developer setup instructions

### Evaluation criteria

- A new user can run the project from the README
- Dependencies are locked
- Secrets are absent from Git history
- Linting, typing, and tests pass in CI
- The application behaves consistently locally and in Docker

### Production concerns

- Dependency vulnerabilities
- Secret rotation
- Base-image updates
- Reproducible builds
- Environment-specific configuration
- Licence compliance

### Interview preparation

- Why lock dependencies?
- Why should secrets not be stored in source control?
- What is the difference between an image and a container?
- What belongs in CI?

## Python for production AI

### Employment outcome

Write maintainable Python services, model integrations, pipelines, and training code.

### Business problem

AI prototypes often become unreliable production systems because the code has weak typing, hidden state, poor error handling, and no testable boundaries.

### Learning objectives

- Use Python collections and functions correctly
- Design modules and packages
- Use classes and composition where appropriate
- Apply typing and validation
- Handle resources and failures safely
- Build reusable interfaces around model providers

### Required concepts

- Lists, dictionaries, tuples, sets
- Functions and closures
- Comprehensions
- Modules and imports
- Classes and dataclasses
- Composition
- Protocols and abstract interfaces
- Type variables and generics
- Exceptions
- Context managers
- Iterators and generators
- Decorators
- Dependency injection

### Tools

- Python
- Pydantic
- Ruff
- mypy or Pyright
- pytest

### Guided implementation

- Define typed document and message models
- Create a provider-independent model interface
- Implement a fake provider for tests
- Add explicit exception classes
- Add retryable and non-retryable error categories
- Implement a generator for streaming output
- Use a context manager for temporary resources
- Add structured logging

### Practical assignment

Build a document-processing command-line application that:

- Accepts text, JSON, and Markdown
- Validates metadata
- Processes files through a configurable pipeline
- Produces structured output
- Continues safely when one input fails
- Records a processing report

### Evaluation criteria

- Public functions are typed
- Invalid inputs produce useful errors
- Components can be replaced through interfaces
- Tests do not require live external services
- Processing does not load every file into memory unnecessarily

### Production concerns

- Memory growth
- Partial failures
- Unicode
- Malformed input
- Logging sensitive content
- File-size limits

### Interview preparation

- Iterator versus generator
- Composition versus inheritance
- Protocol versus abstract base class
- Checked validation versus runtime exceptions
- How to test code that calls an external model

## Asynchronous and concurrent AI services

### Employment outcome

Build responsive AI services that handle streaming, network calls, and background work correctly.

### Business problem

AI applications wait on model providers, search services, databases, and tools. Incorrect concurrency creates blocked requests, duplicate actions, and resource exhaustion.

### Learning objectives

- Understand synchronous and asynchronous execution
- Use async HTTP and database clients
- Stream model output
- Limit concurrency
- Apply cancellation and timeouts
- Choose threads, processes, or workers appropriately

### Required concepts

- Event loop
- Coroutines
- Tasks
- Async context managers
- Semaphores
- Cancellation
- Timeouts
- Backpressure
- Threads
- Processes
- CPU-bound and I/O-bound work
- Worker queues

### Tools

- asyncio
- HTTPX
- FastAPI
- Redis
- A background-worker library or cloud queue

### Guided implementation

- Call multiple read-only tools concurrently
- Limit requests with a semaphore
- Stream partial responses
- Cancel downstream tasks when the client disconnects
- Add per-operation timeouts
- Move long processing into a worker
- Return job status through an API

### Practical assignment

Build an asynchronous document-analysis service with:

- Upload endpoint
- Background processing
- Progress endpoint
- Streaming result endpoint
- Cancellation
- Concurrency limits
- Retry policy

### Evaluation criteria

- Slow tasks do not block unrelated requests
- Duplicate submissions are controlled
- Cancelled jobs stop consuming resources
- Timeouts are visible in logs and metrics
- Load tests do not create unbounded concurrency

### Production concerns

- Connection-pool exhaustion
- Provider rate limits
- Duplicate jobs
- Lost worker messages
- Backpressure
- Graceful shutdown

### Interview preparation

- Async versus threading
- Why CPU-heavy work should not run on the event loop
- Backpressure
- Idempotent background jobs

## Testing and code quality for AI systems

### Employment outcome

Create deterministic tests around probabilistic AI behavior.

### Business problem

Traditional unit tests alone cannot establish whether an AI system is useful, but AI quality tests alone cannot establish whether the software is correct.

### Learning objectives

- Separate software tests from model evaluations
- Mock external providers
- Test streaming and tool calls
- Validate schemas
- Test retries and failures
- Add contract and integration tests

### Required concepts

- Unit tests
- Integration tests
- End-to-end tests
- Contract tests
- Fixtures
- Mocks
- Fakes
- Property-based testing awareness
- Test isolation
- Deterministic seeds
- Regression tests

### Tools

- pytest
- pytest-asyncio
- Pydantic
- HTTP mocking tools
- Docker Compose

### Guided implementation

- Unit-test prompt construction
- Fake model responses
- Validate structured output
- Test provider timeout and retry behavior
- Test database rollback
- Test streaming interruption
- Run integration tests against local PostgreSQL and Redis

### Practical assignment

Create a reusable test harness for model-backed APIs.

### Evaluation criteria

- Tests run without paid API access
- Failure paths are covered
- Integration tests use isolated state
- Evaluation tests are not confused with unit tests
- CI reports useful failures

### Production concerns

- Flaky tests
- Hidden network dependencies
- Leaked credentials
- Non-isolated databases
- Test-data privacy

### Interview preparation

- What should be mocked?
- How do you test nondeterministic output?
- Unit test versus evaluation
- Contract testing for provider integrations

## API and backend engineering

### Employment outcome

Expose AI capabilities through secure, documented, scalable APIs.

### Business problem

Models become useful only when integrated into products and business workflows.

### Learning objectives

- Design REST APIs
- Validate requests and responses
- Authenticate users and services
- Support streaming and background jobs
- Implement reliability controls
- Publish OpenAPI contracts

### Required concepts

- HTTP methods
- Status codes
- Headers
- REST resources
- JSON Schema
- OpenAPI
- Authentication
- Authorization
- OAuth
- OpenID Connect
- API keys
- Rate limiting
- Idempotency
- Webhooks
- Server-sent events
- WebSockets
- Circuit breakers

### Tools

- FastAPI
- Pydantic
- HTTPX
- PostgreSQL
- Redis
- Alembic

### Guided implementation

- Create ticket and conversation resources
- Add user authentication
- Add role-based authorization
- Add request IDs
- Add rate limits
- Add a streaming endpoint
- Add background jobs
- Add database migrations
- Generate API documentation

### Practical assignment

Build a production-style customer-support backend.

### Evaluation criteria

- API contracts are explicit
- Invalid requests fail safely
- Authorization is tested
- Write operations support idempotency
- Streaming clients can disconnect safely
- Database migrations are repeatable

### Production concerns

- Broken access control
- Rate-limit bypass
- Request-size limits
- Abuse
- Database connection pools
- Backward compatibility

### Interview preparation

- Authentication versus authorization
- Idempotency
- Retry-safe API design
- SSE versus WebSockets
- Why use connection pooling?

## SQL, data modelling, and storage

### Employment outcome

Store conversations, documents, model runs, permissions, feedback, and business outcomes correctly.

### Business problem

AI quality depends on traceable data, but many systems lose the relationship among users, prompts, retrieved evidence, model versions, actions, and feedback.

### Learning objectives

- Design relational schemas
- Write analytical and transactional SQL
- Use indexes
- Model multi-tenant permissions
- Store large artifacts outside the database
- Preserve lineage

### Required concepts

- Normalization
- Relationships
- Transactions
- Isolation
- Joins
- CTEs
- Window functions
- Indexes
- Query plans
- Row-level security
- JSON columns
- Object storage
- Caching

### Tools

- PostgreSQL
- SQLAlchemy or SQLModel
- Alembic
- Redis
- Parquet
- Object storage

### Guided implementation

- Model users, tenants, documents, chunks, conversations, model runs, tool calls, and feedback
- Add tenant-aware queries
- Add indexes for frequent access
- Store binary artifacts in object storage
- Use Redis for ephemeral state
- Analyze slow queries

### Practical assignment

Create the data layer for an enterprise AI assistant.

### Evaluation criteria

- Cross-tenant access is prevented
- Data lineage is queryable
- Important queries use appropriate indexes
- migrations work on a fresh database
- Deletion propagates to derived data

### Production concerns

- Tenant isolation
- Retention
- Deletion
- Backup
- Restore
- Index growth
- Cache invalidation

### Interview preparation

- Index tradeoffs
- Transaction isolation
- Relational versus document storage
- Redis use cases
- How to model document permissions

## Applied AI problem discovery

### Employment outcome

Identify AI projects that create measurable business value.

### Business problem

Teams frequently begin with a model or framework and later discover that the workflow does not need AI or cannot tolerate its failure modes.

### Learning objectives

- Map a business workflow
- Establish a baseline
- Identify decision and automation boundaries
- Define measurable outcomes
- Select AI only where justified
- Create a build-versus-buy recommendation

### Required concepts

- User and stakeholder discovery
- Workflow mapping
- Process bottlenecks
- Error costs
- Human-in-the-loop design
- Return on investment
- Build versus buy
- Risk classification
- Adoption metrics

### Tools

- Process diagrams
- Product-requirements documents
- Architecture decision records
- Risk registers
- Cost spreadsheets

### Guided implementation

- Interview a simulated support manager
- Map the current ticket-resolution workflow
- Measure time, cost, and error baseline
- Identify candidate AI interventions
- Classify actions by consequence
- Define human-approval points
- Estimate expected value

### Practical assignment

Produce an Applied AI discovery package for a support organization.

### Required deliverables

- Current-state workflow
- Candidate use cases
- Rejected use cases
- Success metrics
- Risk register
- Build-versus-buy analysis
- Proposed architecture
- Pilot plan

### Evaluation criteria

- Proposed AI use is tied to an actual bottleneck
- Metrics measure business value
- High-risk actions retain human control
- The design includes a non-AI fallback

### Interview preparation

- When should AI not be used?
- How do you estimate ROI?
- What is a useful baseline?
- How do you handle uncertain model output in a business workflow?

## Foundation models and LLM fundamentals

### Employment outcome

Explain and operate modern language models without relying on marketing terminology.

### Business problem

Applied engineers must predict how model architecture, context, sampling, and post-training affect product behavior.

### Learning objectives

- Explain tokenization and autoregressive generation
- Explain transformer attention operationally
- Distinguish base, instruct, reasoning, and multimodal models
- Understand pretraining and post-training
- Configure generation
- Recognize model limitations

### Required concepts

- Tokens
- Vocabulary
- Embeddings
- Logits
- Softmax
- Autoregressive decoding
- Self-attention
- Queries, keys, values
- Positional information
- Context windows
- Dense and mixture-of-experts models
- Pretraining
- SFT
- Preference optimization
- Inference

### Tools

- Tokenizer visualizers
- Hugging Face Transformers
- A hosted model API
- Jupyter

### Guided implementation

- Tokenize different languages and document types
- Inspect token counts
- Run a small open model
- Compare greedy and sampled decoding
- Compare base and instruction models
- Measure context-length effects
- Record latency and output variation

### Practical assignment

Create a model-behavior laboratory comparing at least three models.

### Evaluation criteria

- Comparison uses a fixed test set
- Sampling settings are recorded
- Cost and latency are measured
- Conclusions distinguish observations from assumptions

### Production concerns

- Context overflow
- Unexpected token cost
- Output variability
- Model-version changes
- Regional availability
- Provider data policy

### Interview preparation

- Why do LLMs hallucinate?
- What does temperature change?
- Base versus instruction model
- Dense versus mixture of experts
- Why does context length affect latency and cost?

## Model API integration

### Employment outcome

Build provider-independent model integrations with structured output, streaming, tools, reliability, and cost tracking.

### Business problem

Production applications cannot assume that every request succeeds, every response follows instructions, or one provider remains optimal.

### Learning objectives

- Call hosted models securely
- Stream output
- Validate structured responses
- Invoke tools
- Handle rate limits and failures
- Support provider fallback
- Track tokens and cost

### Required concepts

- Provider authentication
- Messages and responses
- Structured output
- Function calling
- Streaming
- Multimodal requests
- Rate limits
- Timeouts
- Retries
- Fallback
- Request tracing

### Tools

- Native provider SDK
- HTTPX
- Pydantic
- OpenTelemetry
- Redis
- Parallel .NET lane: C#, ASP.NET Core, `System.Text.Json`, a supported provider SDK or supported `Microsoft.Extensions.AI` abstraction, and OpenTelemetry for .NET

### Guided implementation

- Implement a provider interface
- Add two provider adapters
- Stream output
- Request schema-constrained JSON
- Validate and repair or reject invalid output
- Classify provider errors
- Add exponential backoff
- Add a circuit breaker
- Record usage and cost

### Parallel .NET implementation lab

- Implement the same provider-owned boundaries behind an application-owned C# interface
- Expose authenticated ASP.NET Core endpoints for synchronous, server-sent-event streaming, and schema-constrained requests
- Validate structured output before it reaches domain code
- Propagate cancellation and deadlines through model calls and streamed responses
- Classify provider errors and apply retry, circuit-breaker, and fallback policies only where safe
- Emit correlated traces plus token, latency, model-version, tenant, and cost attributes without recording sensitive prompt content
- Run the shared contract fixtures against the Python reference and the .NET implementation

### Practical assignment

Build a multi-provider AI gateway.

### Evaluation criteria

- Provider-specific code is isolated
- Invalid output cannot reach downstream business logic
- Retries apply only to safe failures
- Usage is attributed to user and tenant
- Fallback is observable
- The .NET lab passes the same valid, invalid-schema, rate-limit, timeout, cancellation, and fallback fixtures as the Python path
- Acceptance evidence includes an API contract, automated test report, one redacted trace, and a quality-latency-cost comparison

### Production concerns

- Provider outages
- Rate limits
- Duplicate writes after retry
- Data residency
- Secret management
- Model deprecation

### Interview preparation

- How would you design provider fallback?
- When should a request not be retried?
- How do structured outputs improve reliability?
- How do you track cost by customer?
- How do ASP.NET Core cancellation, streaming, dependency injection, and typed serialization affect a model integration?
- When should a .NET service use a provider SDK directly versus a provider-neutral abstraction?

## Prompt and context engineering

### Employment outcome

Design prompts as versioned, testable application components.

### Business problem

Uncontrolled prompt changes can silently alter quality, safety, cost, and downstream behavior.

### Learning objectives

- Write clear instructions and output contracts
- Use examples intentionally
- Separate instructions from untrusted content
- Manage context
- Version and test prompts
- Detect when prompting is insufficient

### Required concepts

- Instruction hierarchy
- Task definition
- Constraints
- Few-shot examples
- Delimiters
- Context selection
- Context compression
- Schema-first prompting
- Prompt injection
- Prompt versioning

### Tools

- Prompt templates
- Pydantic
- MLflow or prompt registry
- Evaluation harness

### Guided implementation

- Create prompts for classification, extraction, and drafting
- Add schema contracts
- Test ambiguous inputs
- Test malicious instructions inside documents
- Compare zero-shot and few-shot behavior
- Measure prompt-token cost
- Store prompt versions

### Practical assignment

Create a tested prompt package for support-ticket automation.

### Evaluation criteria

- Prompts have explicit purposes
- Inputs and untrusted content are separated
- Changes run through regression evaluation
- Prompt version appears in traces
- Failure and abstention behavior is defined

### Interview preparation

- Prompt engineering versus context engineering
- When examples help
- How to reduce prompt injection risk
- When to replace prompt work with RAG or fine-tuning

## Applied LLM product

### Employment outcome

Combine backend engineering, model APIs, prompts, evaluation, and human review into a working product.

### Business problem

Support agents spend time classifying tickets, extracting details, assigning urgency, and drafting repetitive replies.

### Required capabilities

- Ticket classification
- Structured issue extraction
- Priority recommendation
- Response drafting
- Human editing and approval
- Streaming
- Conversation history
- Feedback
- Cost tracking
- Audit trail

### Tools

- FastAPI
- PostgreSQL
- Redis
- Hosted model API
- Pydantic
- OpenTelemetry
- React or a minimal user interface

### Implementation sequence

- Define business and quality metrics
- Create evaluation cases
- Implement deterministic baseline
- Implement model calls
- Add structured output
- Add human review
- Add persistence
- Add traces
- Add cost tracking
- Add security controls
- Deploy

### Evaluation criteria

- Classification and extraction meet stated thresholds
- Drafts are never sent automatically
- Every output is linked to prompt and model versions
- User edits are recorded as feedback
- Cost per handled ticket is reported

### Interview preparation

- Why use AI for each capability?
- What is the fallback?
- How is quality measured?
- How do user edits improve the system?

## Embeddings and semantic retrieval

### Employment outcome

Build and evaluate semantic, lexical, and hybrid search.

### Business problem

Keyword search misses relevant content, while pure vector search can return semantically similar but operationally incorrect documents.

### Learning objectives

- Generate and store embeddings
- Compare similarity measures
- Implement lexical and dense search
- Build hybrid retrieval
- Add metadata filtering
- Evaluate retrieval

### Required concepts

- Embedding vectors
- Normalization
- Cosine similarity
- Dot product
- BM25
- Inverted indexes
- Approximate nearest neighbours
- Metadata filters
- Reranking

### Tools

- sentence-transformers
- pgvector
- OpenSearch or Elasticsearch
- FAISS for local experiments

### Guided implementation

- Embed a document collection
- Create a vector index
- Implement BM25 search
- Combine lexical and dense scores
- Add metadata filters
- Add a cross-encoder reranker
- Create relevance judgments

### Practical assignment

Build a semantic policy-search service.

### Evaluation criteria

- Search is evaluated against labelled queries
- Hybrid retrieval is compared with dense and lexical baselines
- Permission filters are applied before results reach the model
- Index and query latency are measured

### Production concerns

- Embedding-model migration
- Reindexing
- Permission leakage
- Stale content
- Index growth
- Multilingual content

### Interview preparation

- BM25 versus embeddings
- Cosine similarity versus dot product
- Why use a reranker?
- How do you evaluate retrieval independently of generation?

## Document ingestion and chunking

### Employment outcome

Create reliable pipelines that turn enterprise content into searchable, permission-aware units.

### Business problem

RAG quality is frequently limited by parsing, metadata, and chunking rather than the language model.

### Learning objectives

- Parse common enterprise formats
- Handle scans, tables, and images
- Preserve document structure and provenance
- Compare chunking strategies
- Process updates and deletions

### Required concepts

- Parsing
- OCR
- Layout
- Tables
- Metadata
- Deduplication
- Chunk identifiers
- Parent-child relationships
- Incremental processing
- Delete propagation

### Tools

- Document parsers
- OCR engine or cloud document service
- PostgreSQL
- Object storage
- Queue and worker

### Guided implementation

- Parse PDF, HTML, email, and Office files
- Detect scanned pages
- Run OCR
- Extract tables
- Preserve page and section metadata
- Implement fixed, structure-aware, and parent-child chunking
- Detect duplicate documents
- Process updates and deletes

### Practical assignment

Build a versioned document-ingestion service.

### Evaluation criteria

- Every chunk links to source, page, section, tenant, and document version
- Failed pages are reported
- Reprocessing is idempotent
- Deleted content disappears from retrieval
- Chunking strategies are compared on retrieval metrics

### Production concerns

- Corrupt files
- Large documents
- OCR cost
- Unsupported formats
- Duplicate content
- Malware scanning
- Data retention

### Interview preparation

- Why does chunk size matter?
- How do you process document updates?
- How do you handle tables?
- How do you prevent deleted content from being retrieved?

## Production RAG

### Employment outcome

Build an enterprise RAG system with citations, permissions, evaluation, freshness, and observability.

### Business problem

Employees need reliable answers from changing internal sources without exposing unauthorized content.

### Learning objectives

- Build end-to-end RAG
- Rewrite and classify queries
- Use hybrid retrieval and reranking
- Assemble evidence
- Produce citations and abstentions
- Enforce access control
- Diagnose failures
- Select classic retrieval or bounded agentic retrieval from measured requirements
- Compare retrieval quality, answer quality, latency, and cost across both paths

### Required concepts

- Query rewriting
- Query decomposition
- Hybrid retrieval
- Reranking
- Context assembly
- Grounded generation
- Citations
- Conversational retrieval
- Retrieval as a tool
- Query planning
- Parallel focused subqueries
- Iterative retrieval with explicit stopping conditions
- Freshness
- Caching
- Tenant isolation

### Tools

- FastAPI
- PostgreSQL
- pgvector
- OpenSearch
- Redis
- Reranking model
- Model API
- OpenTelemetry
- Parallel .NET lane: ASP.NET Core, a supported model SDK or provider-neutral AI abstraction, and a compatible vector or search client

### Guided implementation

- Create ingestion and query services
- Add query classification
- Add hybrid retrieval
- Add reranking
- Construct evidence packets
- Generate page-level citations
- Add abstention
- Add user and document permissions
- Add retrieval traces
- Add feedback
- Establish classic hybrid retrieval as the default baseline
- Add a planner that invokes agentic retrieval only for complex or multi-part questions
- Decompose an approved question into a bounded number of focused subqueries
- Run independent subqueries in parallel with concurrency, time, token, and spending limits
- Merge, deduplicate, rerank, and cite evidence before generation
- Stop when evidence is sufficient or any step, latency, token, or cost budget is exhausted

### Classic-versus-agentic retrieval lab

- Evaluate both paths on the same simple, multi-part, ambiguous, insufficient-evidence, and adversarial query set
- Record retrieval metrics, answer correctness, groundedness, citation accuracy, end-to-end latency, token use, and cost
- Route simple questions to classic RAG unless measured evidence justifies extra planning
- Test decomposition explosion, repeated queries, unavailable retrievers, partial results, permission changes, timeouts, citation mismatch, and attempts to exceed limits
- Require permission checks on every derived subquery and every retrieved item

### Parallel .NET implementation lab

- Implement the query planner and retrieval tools behind C# interfaces
- Use bounded asynchronous concurrency and cancellation propagation for focused subqueries
- Reuse the shared evaluation set and emit compatible retrieval, model, citation, and cost traces
- Demonstrate classic fallback when planning fails or the agentic budget is exhausted

### Practical assignment

Build an enterprise knowledge assistant with a classic RAG baseline and a selectively invoked, bounded agentic-retrieval path.

### Evaluation criteria

- Retrieval and generation have separate metrics
- Unauthorized evidence is never included
- Unsupported questions abstain
- Citations are verifiable
- Updates meet a defined freshness objective
- Failures are attributed to pipeline stages
- Classic and agentic paths are compared on the same versioned evaluation set
- The report states when agentic retrieval improves quality enough to justify its additional latency and cost
- Maximum subqueries, iterations, concurrency, latency, tokens, and spending are enforced in automated failure tests
- The .NET lab, when selected, passes the same authorization, citation, budget, and fallback acceptance fixtures

### Production concerns

- Prompt injection in documents
- Permission-aware caching
- Stale indexes
- Citation mismatch
- Provider outages
- Long-context cost
- Unbounded planning or retrieval loops
- Permission leakage through derived subqueries
- Planner-generated irrelevant or adversarial queries

### Interview preparation

- Walk through the RAG pipeline
- How do you diagnose a wrong answer?
- Why hybrid retrieval?
- How do you enforce document access?
- RAG versus fine-tuning
- When is classic RAG preferable to agentic retrieval?
- How do you stop, evaluate, and safely fall back from an agentic retrieval loop?

## AI evaluation engineering

### Employment outcome

Build evaluation systems that prevent unmeasured model, prompt, retrieval, and agent changes from reaching production.

### Business problem

Teams cannot improve AI systems if they cannot consistently measure task quality and business outcomes.

### Learning objectives

- Define evaluation requirements
- Build golden datasets
- Use deterministic, model-based, and human evaluation
- Calibrate judges
- Run regression gates
- Connect offline and online metrics

### Required concepts

- Evaluation slices
- Representative sampling
- Annotation rubrics
- Exact match
- Semantic metrics
- Retrieval metrics
- Pairwise judging
- Judge bias
- Human review
- Confidence intervals
- A/B testing

### Tools

- pytest
- MLflow
- Custom evaluation code
- Ragas, DeepEval, or equivalent
- promptfoo
- Phoenix or LangSmith

### Guided implementation

- Define task-specific rubrics
- Create golden test cases
- Add schema and citation checks
- Add retrieval metrics
- Add a model judge
- Compare judge decisions with humans
- Add cost and latency
- Add CI quality thresholds

### Practical assignment

Build an evaluation platform for prompts, RAG versions, adapters, and agents.

### Evaluation criteria

- Dataset versions are immutable
- Metrics align with user tasks
- Model judges are calibrated
- CI blocks meaningful regressions
- Results include confidence and slices
- Business metrics remain separate from model metrics

### Production concerns

- Test contamination
- Judge drift
- Biased datasets
- Overfitting to benchmarks
- Expensive evaluations
- Sensitive evaluation data

### Interview preparation

- How do you evaluate an LLM application?
- LLM-as-judge limitations
- Offline versus online evaluation
- How do you evaluate an agent?
- How do you build a golden dataset?

## AI data engineering

### Employment outcome

Create trustworthy datasets for evaluation, SFT, preferences, and multimodal systems.

### Business problem

Model adaptation fails when data is duplicated, low quality, improperly licensed, privacy-sensitive, or contaminated across train and test sets.

### Learning objectives

- Define data contracts
- Collect and validate data
- Remove PII and duplicates
- Create training and evaluation splits
- Build annotation workflows
- Track provenance and versions

### Required concepts

- Data provenance
- Consent
- Licensing
- Schemas
- Validation
- Deduplication
- PII
- Quality scoring
- Annotation
- Synthetic data
- Active learning
- Leakage
- Lineage

### Tools

- Python
- SQL
- Polars or pandas
- Hugging Face Datasets
- Parquet
- DVC
- Spark when scale requires it
- Airflow or Dagster

### Guided implementation

- Register source datasets
- Validate schemas
- Detect and redact PII
- Deduplicate exact and near-duplicate records
- Create instruction and preference formats
- Create train, validation, and test splits
- Add leakage checks
- Generate a dataset card

### Practical assignment

Build an auditable training-data pipeline.

### Evaluation criteria

- Every record has source and processing lineage
- Test data is isolated
- PII handling is documented
- Quality filters are measured
- The dataset can be rebuilt from approved sources

### Production concerns

- Copyright
- Consent withdrawal
- Data deletion
- Annotator access
- Synthetic-data collapse
- Distribution drift

### Interview preparation

- How do you prevent leakage?
- Human versus synthetic data
- How do you assess training-data quality?
- What belongs in a dataset card?

## Tool calling and controlled workflows

### Employment outcome

Build AI workflows that read systems, propose actions, and safely execute approved operations.

### Business problem

A model can generate text, but business automation requires validated arguments, permissions, idempotency, recovery, and audit logs.

### Learning objectives

- Define tools and schemas
- Validate model-selected arguments
- Separate reads from writes
- Build explicit workflow state
- Add approval and compensation
- Evaluate execution
- Design governed request, session, durable, preference, retrieval-backed, and summarized memory
- Enforce consent, provenance, retention, correction, and deletion for memory writes

### Required concepts

- Tool schema
- Argument validation
- State machine
- Workflow graph
- Idempotency
- Retry
- Compensation
- Human approval
- Durable state
- Request context
- Session memory
- Durable workflow memory
- User-preference memory
- Retrieval-backed memory
- Summarized memory
- Memory write policy
- Consent and purpose limitation
- Provenance and versioning
- Expiration, correction, and deletion
- Audit log
- Step and spending limits

### Tools

- Native provider tool calling
- Pydantic
- PostgreSQL
- Redis
- LangGraph or another selected workflow framework after manual implementation
- Parallel .NET lane: ASP.NET Core, application-owned workflow interfaces, and optionally supported Semantic Kernel packages after the manual workflow is understood

### Guided implementation

- Define customer, order, policy, and refund tools
- Validate arguments
- Add per-tool permissions
- Implement explicit workflow states
- Add human approval before writes
- Add retries for read failures
- Add compensation for partial writes
- Record complete traces

### Governed agent-memory lab

- Keep request context, session state, durable workflow checkpoints, user preferences, retrieval-backed facts, and summaries in separate stores or explicitly typed records
- Define an allowlist-based write policy describing what may be remembered, for which purpose, for how long, and with whose consent
- Store subject, tenant, source, provenance, purpose, consent state, classification, version, creation time, and expiration with every durable memory item
- Provide user-visible correction and deletion operations and invalidate derived summaries, indexes, and caches
- Prevent the model from silently converting untrusted tool output into durable memory
- Evaluate relevance, factual consistency, stale-memory handling, cross-tenant isolation, correction propagation, and verified forgetting
- Test missing consent, poisoning, duplicate writes, expired records, revoked access, deletion during an active session, and summary drift

### Parallel .NET implementation lab

- Implement the controlled workflow and typed memory policy behind ASP.NET Core services
- Require authorization and idempotency checks at the application boundary before every tool or memory write
- Persist workflow checkpoints separately from user-profile memory
- Run the same approval, recovery, isolation, expiration, correction, and deletion fixtures as the Python implementation

### Practical assignment

Build a support-resolution workflow with governed memory and an equivalent .NET service slice when the .NET lane is selected.

### Evaluation criteria

- Unauthorized actions are rejected
- Duplicate requests do not duplicate business actions
- Partial failures can resume or compensate
- Human approval captures the exact proposed action
- Task completion and invalid-action rates are measured
- Durable memory is written only under an explicit policy with recorded consent, purpose, provenance, and expiration
- Correction and deletion remove or invalidate derived memory within a documented objective
- Automated tests prove that memory cannot cross tenant, user, or purpose boundaries
- Acceptance evidence includes a memory schema, write-policy decision table, retention/deletion test report, and memory-quality evaluation

### Production concerns

- Excessive agency
- Hidden side effects
- Duplicate writes
- Long-running state
- Credential scope
- Audit retention
- Memory poisoning and stale preferences
- Sensitive-data retention
- Confusing resumable workflow state with user memory

### Interview preparation

- Workflow versus autonomous agent
- How do you make tool calls safe?
- Why is idempotency important?
- How do you recover after partial failure?
- What should an agent remember, and what must it never write?
- How do consent, provenance, expiration, correction, and deletion change a memory design?

## MCP and agent integration

### Employment outcome

Expose and consume standardized AI tools without weakening identity, permission, or security controls.

### Business problem

Organizations need reusable integrations, but dynamic tool discovery increases trust and supply-chain risks.

### Learning objectives

- Understand MCP clients and servers
- Expose tools and resources
- Authenticate connections
- Restrict capabilities
- Log and evaluate MCP operations
- Understand agent interoperability
- Package reusable, versioned agent capabilities, sometimes called skills, with explicit contracts and permissions
- Map approved capabilities to MCP tools, resources, or prompts without granting implicit authority
- Explain the additional controls required for computer-use and coding agents

### Required concepts

- MCP client
- MCP server
- Tools
- Resources
- Prompts
- Transport
- Capability negotiation
- Authentication
- Authorization
- Server trust
- Dynamic discovery
- Capability or skill manifest without treating one vendor-specific file convention as universal
- Version compatibility
- Permission and resource declaration
- Capability-to-MCP mapping
- Sandboxed execution
- Filesystem, process, network, and credential boundaries
- Proposed change, approval, execution, and audit separation

### Tools

- Official or established MCP SDK
- OAuth or service identity
- JSON Schema
- OpenTelemetry
- Parallel .NET lane: an established .NET MCP SDK and ASP.NET Core identity and authorization components
- Disposable container or equivalent restricted sandbox for the automation lab

### Guided implementation

- Build an MCP server for read-only policy search
- Add authentication
- Restrict tenant access
- Connect an MCP client
- Add audit logs
- Test malicious tool descriptions and inputs
- Define an allowlist
- Create a reusable capability package with a name, semantic version, input/output schema, owner, allowed data, required permissions, resource limits, and compatibility tests
- Pin and approve capability versions instead of accepting arbitrary dynamic upgrades
- Map each capability deliberately to an MCP tool, resource, or prompt and document identity propagation

### Sandboxed computer and coding-agent lab

- Run one read-only inspection and one proposed source change against a disposable test repository
- Deny host credentials, unrestricted filesystem access, privileged processes, and network access by default
- Restrict paths, commands, CPU, memory, time, output, and step count
- Present the exact diff and command plan for human approval before any write or execution with side effects
- Log the capability version, requesting identity, authorization decision, proposed action, approval, execution result, and produced artifact
- Treat screenshots, repository text, tool descriptions, and command output as untrusted input
- Never permit autonomous destructive or production remediation actions in this lab

### Parallel .NET MCP lab

- Expose the read-only policy capability through an authenticated .NET MCP server
- Consume it from an allowlisted client while preserving user and tenant identity
- Run the shared discovery, schema, authorization, injection, version-mismatch, cancellation, and audit fixtures

### Practical assignment

Integrate one versioned production capability through MCP and complete the restricted automation lab in a disposable environment.

### Evaluation criteria

- The client trusts only approved servers
- User identity reaches authorization checks
- Tool capabilities are restricted
- Every operation is traceable
- Untrusted tool content cannot override application policy
- Capability versions, schemas, owners, permissions, and resource limits are reviewable and pinned
- A capability receives only the authority explicitly granted to its MCP mapping
- The automation lab proves that denied paths, commands, networks, credentials, and unapproved writes remain blocked
- Acceptance evidence includes the capability manifest, MCP mapping, compatibility tests, sandbox policy, proposed diff, approval record, and audit trace

### Production concerns

- Malicious servers
- Tool substitution
- Credential forwarding
- Capability escalation
- Cross-tenant data
- Prompt injection through tool results
- Capability supply-chain changes
- Sandbox escape and credential theft
- Confusing model intent with user authorization

### Interview preparation

- What problem does MCP solve?
- What security risks does dynamic tool discovery introduce?
- How should identity propagate?
- MCP versus a direct API integration
- How do reusable agent capabilities differ from tools, prompts, and MCP resources?
- How would you sandbox a computer-use or coding agent and preserve meaningful user authorization?

## PyTorch and training fundamentals

### Employment outcome

Understand and implement model training before using high-level fine-tuning trainers.

### Business problem

Training frameworks hide memory, optimization, and data problems that engineers must diagnose when runs fail or quality regresses.

### Learning objectives

- Use tensors and autograd
- Build a training loop
- Understand optimizer behavior
- Estimate memory
- Use mixed precision
- Save and resume checkpoints

### Required concepts

- Tensors
- Parameters
- Activations
- Gradients
- Loss
- Backpropagation
- Optimizers
- Learning rate
- Batch size
- Gradient accumulation
- Validation
- Checkpoints
- Overfitting
- FP32, FP16, and BF16

### Tools

- PyTorch
- TensorBoard or MLflow
- PyTorch Profiler

### Guided implementation

- Train a small classifier
- Inspect gradients
- Compare optimizers
- Add validation
- Add early stopping
- Use mixed precision
- Add gradient clipping
- Save and resume a checkpoint
- Profile CPU and GPU work

### Practical assignment

Build a reproducible training pipeline for a small text classifier.

### Evaluation criteria

- Training resumes from checkpoints
- Validation controls model selection
- Runs record code, data, parameters, and metrics
- Numerical issues are detected
- Memory use is measured

### Production concerns

- Out-of-memory failures
- NaN loss
- Checkpoint corruption
- Non-reproducible data order
- Hardware differences

### Interview preparation

- Backpropagation
- Batch size versus gradient accumulation
- Learning-rate effects
- Mixed precision
- Training versus validation loss

## Tokenizers and language-model training data

### Employment outcome

Prepare correctly formatted data for SFT and preference optimization.

### Business problem

Incorrect chat templates, masks, padding, and sequence handling can train a model on the wrong tokens while still producing a decreasing loss.

### Learning objectives

- Inspect tokenizers
- Apply chat templates
- Create attention and label masks
- Pack sequences
- Control maximum length
- Validate training records

### Required concepts

- Vocabulary
- Special tokens
- Chat template
- Padding
- Truncation
- Attention mask
- Label mask
- Completion-only loss
- Sequence packing
- Data collator

### Tools

- Transformers
- Datasets
- TRL
- Tokenizer inspection scripts

### Guided implementation

- Format single-turn and multi-turn data
- Apply the model's chat template
- Mask prompt tokens
- Compare padded and packed batches
- Calculate token-length distributions
- Filter or truncate long examples
- Visualize labels

### Practical assignment

Create a validated support instruction dataset.

### Evaluation criteria

- Templates match the selected model
- Labels train only intended tokens
- Length distributions are reported
- Truncation does not silently remove required answers
- Data splits are isolated

### Production concerns

- Incorrect special tokens
- Excess padding
- Lost supervision
- Test leakage
- Long-example memory spikes

### Interview preparation

- Why do chat templates matter?
- Padding versus packing
- What is label masking?
- How does sequence length affect memory?

## Supervised fine-tuning

### Employment outcome

Adapt an open model to stable task behavior, format, style, and policy.

### Business problem

A general model may understand a task but fail to follow a specialized output schema or operational policy consistently.

### Learning objectives

- Select a base or instruction model
- Configure SFT
- Track training and validation
- Select checkpoints
- Evaluate behavior and safety
- Compare SFT with prompting and RAG

### Required concepts

- SFT objective
- Base versus instruction model
- Training split
- Validation split
- Learning rate
- Epochs
- Warmup
- Checkpoint selection
- Catastrophic forgetting
- Behavior regression

### Tools

- PyTorch
- Transformers
- Datasets
- TRL SFTTrainer
- Accelerate
- MLflow

### Guided implementation

- Establish an untouched baseline
- Configure the dataset
- Run a small SFT experiment
- Monitor loss and validation
- Evaluate multiple checkpoints
- Compare task and general behavior
- Record cost and hardware use

### Practical assignment

Fine-tune a support policy and structured-response model.

### Evaluation criteria

- Baseline and adapted model use the same test set
- Training data does not contain test answers
- Checkpoint selection uses validation data
- Safety and general-capability regressions are reported
- SFT is compared with prompting and RAG

### Production concerns

- Overfitting
- Memorization
- Licence restrictions
- Model artefact size
- Evaluation gaps
- Unexpected behavior changes

### Interview preparation

- When is SFT appropriate?
- Base versus instruct model for SFT
- How do you select a checkpoint?
- Why might training loss improve while product quality worsens?

## LoRA and QLoRA

### Employment outcome

Fine-tune models economically and serve reusable domain adapters.

### Business problem

Full fine-tuning may require more GPU memory and storage than an application team can justify.

### Learning objectives

- Explain low-rank adaptation
- Select target modules and rank
- Train LoRA and QLoRA adapters
- Compare memory and quality
- Merge or dynamically serve adapters

### Required concepts

- Parameter-efficient fine-tuning
- Low-rank matrices
- Rank
- Scaling
- Target modules
- Adapter dropout
- Four-bit base model
- NF4
- Compute dtype
- Gradient checkpointing
- Adapter merging

### Tools

- PEFT
- Transformers
- TRL
- bitsandbytes
- Accelerate
- MLflow

### Guided implementation

- Inspect model modules
- Configure LoRA targets
- Calculate trainable parameters
- Train a LoRA adapter
- Load a four-bit base model
- Train QLoRA
- Compare memory and quality
- Merge an adapter
- Serve an unmerged adapter

### Practical assignment

Build LoRA and QLoRA versions of the support model.

### Evaluation criteria

- Hyperparameters and target modules are documented
- GPU memory is measured
- LoRA, QLoRA, and baseline quality are compared
- Adapter artefacts are versioned
- Merged and dynamic-serving options are evaluated

### Production concerns

- Hardware compatibility
- Quantization differences
- Adapter/base-model mismatch
- Merge precision
- Multi-tenant adapter isolation

### Interview preparation

- How does LoRA work?
- LoRA versus QLoRA
- What does rank control?
- Why select target modules?
- Merge versus dynamic adapter serving

## Preference data and DPO

### Employment outcome

Improve response preferences such as policy compliance, style, usefulness, and refusal behavior.

### Business problem

SFT teaches demonstrations but does not directly express that one acceptable response is preferred over another.

### Learning objectives

- Build preference pairs
- Define annotation rubrics
- Train with DPO
- Understand reference-model behavior
- Detect preference overfitting
- Evaluate helpfulness and safety

### Required concepts

- Chosen response
- Rejected response
- Preference rubric
- Policy model
- Reference model
- DPO objective intuition
- Preference strength
- Over-optimization
- Reward models awareness

### Tools

- TRL DPOTrainer
- PEFT
- Datasets
- MLflow
- Human annotation interface

### Guided implementation

- Define a preference rubric
- Collect and validate pairs
- Train a DPO adapter
- Compare SFT and DPO behavior
- Evaluate policy compliance
- Evaluate refusal and over-refusal
- Review difficult examples with humans

### Practical assignment

Create a preference-optimized support model.

### Evaluation criteria

- Preference data follows a documented rubric
- Pair quality is audited
- DPO is compared with the SFT checkpoint
- Safety and task quality are both measured
- Over-refusal is reported

### Production concerns

- Biased preferences
- Annotator disagreement
- Reward hacking
- Narrow optimization
- Safety regressions

### Interview preparation

- SFT versus DPO
- What is the reference model?
- How do you create preference data?
- Why can preference optimization overfit?

## Advanced post-training decisions

### Employment outcome

Select continued pretraining, distillation, reward modelling, or RL-based methods only when business and model requirements justify them.

### Business problem

Teams can spend substantial compute on advanced training methods without proving that simpler adaptation methods are insufficient.

### Learning objectives

- Identify continued-pretraining use cases
- Understand distillation
- Understand reward-model pipelines
- Understand RLHF, GRPO, and verifiable rewards
- Estimate data and infrastructure cost

### Required concepts

- Domain-adaptive pretraining
- Data mixtures
- Catastrophic forgetting
- Teacher and student models
- Synthetic targets
- Reward model
- PPO-based RLHF
- GRPO
- RLOO
- Verifiable rewards
- Process and outcome rewards

### Tools

- PyTorch
- Transformers
- TRL
- Distributed-training framework
- Experiment tracker

### Guided implementation

- Write decision documents for several adaptation scenarios
- Run a small response-distillation experiment
- Design a reward-data schema
- Define verifiable rewards for a structured task
- Estimate training resources

### Practical assignment

Produce an adaptation decision report and one small distillation experiment.

### Evaluation criteria

- Simpler approaches are used as baselines
- Expected gains justify compute and data cost
- Forgetting and safety risks are covered
- Evaluation is defined before training

### Production concerns

- High compute cost
- Data rights
- Catastrophic forgetting
- Reward exploitation
- Complex rollback

### Interview preparation

- Continued pretraining versus SFT
- Distillation use cases
- DPO versus RLHF
- What makes a reward verifiable?

## Distributed and efficient training

### Employment outcome

Run and recover multi-GPU training workloads for LLM, platform, or training-engineering roles.

### Business problem

Larger models and sequences exceed one device, while poor distributed configuration wastes expensive GPU capacity.

### Learning objectives

- Use data parallelism
- Understand sharded training
- Configure mixed precision
- Save distributed checkpoints
- Monitor utilization
- Recover failed runs

### Required concepts

- DistributedDataParallel
- FSDP
- DeepSpeed ZeRO
- Data parallelism
- Tensor-parallel awareness
- Pipeline-parallel awareness
- NCCL
- Gradient accumulation
- Activation checkpointing
- Distributed checkpointing

### Tools

- PyTorch distributed
- Accelerate
- FSDP or DeepSpeed
- NCCL
- GPU monitoring

### Guided implementation

- Launch a two-device training job
- Compare DDP and sharding concepts
- Add mixed precision
- Add activation checkpointing
- Save and resume distributed state
- Record utilization
- Simulate a failed worker

### Practical assignment

Run a reproducible distributed QLoRA or small-model training job.

### Evaluation criteria

- The run scales beyond one device
- Checkpoints restore correctly
- Effective batch size is calculated
- Utilization and communication overhead are reported
- Failure recovery is demonstrated

### Production concerns

- Worker failure
- Network bottlenecks
- Stragglers
- Checkpoint size
- Job preemption
- GPU underutilization

### Interview preparation

- DDP versus FSDP
- What does ZeRO shard?
- Why use activation checkpointing?
- How do you calculate effective batch size?

## Multimodal and document AI

### Employment outcome

Build workflows that combine text, images, scanned documents, tables, and structured outputs.

### Business problem

Important enterprise information often exists in forms, receipts, diagrams, photographs, and scanned records rather than clean text.

### Learning objectives

- Process images and documents
- Use OCR and layout
- Extract structured fields
- Combine visual and textual evidence
- Route uncertain cases to humans

### Required concepts

- OCR
- Layout analysis
- Table extraction
- Vision-language models
- Image preprocessing
- Document classification
- Confidence routing
- Multimodal evaluation

### Tools

- OpenCV
- OCR engine or cloud document service
- Multimodal model API or open model
- PyTorch and Transformers where required

### Guided implementation

- Classify documents
- Extract text and layout
- Extract tables and fields
- Send selected visual context to a multimodal model
- Generate evidence-linked JSON
- Add confidence and review routing

### Practical assignment

Build a claim-document review assistant.

### Evaluation criteria

- Field extraction is evaluated separately
- Evidence links to page and region
- Low-confidence cases reach human review
- Images are resized and processed efficiently
- Sensitive images are protected

### Production concerns

- OCR errors
- Rotated and damaged scans
- Image-token cost
- Unsupported formats
- PII
- Human-review workload

### Interview preparation

- OCR versus vision-language models
- How do you evaluate document extraction?
- How do you handle tables?
- When should a case be routed to a human?

## Speech, audio, and voice AI

### Employment outcome

Build real-time voice workflows with transcription, synthesis, tools, interruption handling, and privacy controls.

### Business problem

Voice applications have stricter latency, turn-taking, consent, and failure-recovery requirements than text chat.

### Learning objectives

- Stream audio
- Use speech recognition and synthesis
- Detect turns and interruptions
- Call tools during conversations
- Escalate to humans
- Measure voice quality and latency

### Required concepts

- Audio frames
- Sampling rate awareness
- Voice activity detection
- Speech-to-text
- Text-to-speech
- Diarization
- Turn detection
- Barge-in
- Real-time transport
- End-to-end latency

### Tools

- Realtime model or speech APIs
- WebSockets or WebRTC
- Voice activity detector
- Audio-processing library

### Guided implementation

- Stream microphone or recorded audio
- Transcribe partial speech
- Detect the end of a turn
- Generate a response
- Synthesize speech
- Interrupt playback on user speech
- Call a read-only business tool
- Escalate to a human

### Practical assignment

Build a voice support triage assistant.

### Evaluation criteria

- End-to-end latency is measured
- Interruptions behave correctly
- Transcription and task quality are evaluated
- Users receive AI and recording disclosure
- Sensitive audio follows retention policy

### Production concerns

- Network jitter
- Background noise
- Accent variation
- Consent
- Recording laws
- Emergency escalation

### Interview preparation

- Why is voice latency different from chat latency?
- How does interruption handling work?
- How do you evaluate a voice agent?
- What privacy controls are required?

## AI security and privacy

### Employment outcome

Threat-model and secure LLM, RAG, agent, training, and model-serving systems.

### Business problem

AI systems process untrusted language and may hold credentials or perform actions, creating new paths around traditional security controls.

### Learning objectives

- Identify AI-specific attack paths
- Enforce least privilege
- Secure retrieval and tools
- Sandbox execution
- Protect sensitive data
- Build security regression tests

### Required concepts

- Direct and indirect prompt injection
- Jailbreaking
- Sensitive-data disclosure
- Improper output handling
- Excessive agency
- Retrieval poisoning
- Data poisoning
- Model extraction
- Denial of service
- Supply-chain risk
- Tenant isolation
- Sandboxing

### Tools

- OWASP GenAI guidance
- Threat-model templates
- Secret manager
- Identity provider
- promptfoo or equivalent adversarial testing
- PII detection and redaction
- Container sandboxing

### Guided implementation

- Threat-model the support agent
- Create injection attacks
- Apply permission checks outside the model
- Sanitize or isolate tool output
- Redact PII
- Restrict execution
- Add rate and spending limits
- Add security logs

### Practical assignment

Build an AI security gateway and adversarial test suite.

### Evaluation criteria

- Business authorization never depends on model text
- Cross-tenant tests pass
- Dangerous tools require approval
- Sensitive data is redacted from logs
- Security tests run in CI

### Production concerns

- Identity propagation
- Third-party tools
- Logging exposure
- Provider retention
- Training-data poisoning
- Incident response

### Interview preparation

- Direct versus indirect prompt injection
- How do you secure an agent?
- Why are model guardrails not authorization?
- How do you secure RAG?

## Responsible AI and governance

### Employment outcome

Operate AI systems with traceable ownership, risk controls, documentation, and human oversight.

### Business problem

Organizations need to know which AI systems exist, who owns them, what data they use, how they were approved, and what happens after an incident.

### Learning objectives

- Maintain an AI inventory
- Classify risk
- Create model, system, and dataset documentation
- Define approval and change processes
- Monitor bias and harmful behavior
- Prepare incident workflows

### Required concepts

- AI inventory
- Risk classification
- Impact assessment
- Model card
- System card
- Dataset card
- Human oversight
- Audit
- Vendor assessment
- Incident management

### Standards

- NIST AI Risk Management Framework
- NIST Generative AI Profile
- ISO/IEC 42001 awareness
- ISO/IEC 23894 awareness
- Applicable privacy and sector regulations
- EU AI Act awareness when relevant

### Guided implementation

- Register the support assistant in an AI inventory
- Create an impact assessment
- Document data and model dependencies
- Define approval gates
- Define monitoring ownership
- Create an incident runbook

### Practical assignment

Produce a governance package for the capstone system.

### Evaluation criteria

- Ownership is explicit
- Risks map to controls
- Change approval is defined
- User recourse exists
- Incident reporting and rollback are documented

### Interview preparation

- What belongs in a system card?
- How does governance affect engineering?
- How do you define human oversight?
- What is an AI impact assessment?

## Production architecture and reliability

### Employment outcome

Design AI services that remain available and degrade safely when providers, tools, retrieval, or workers fail.

### Business problem

AI systems combine many slow and failure-prone dependencies, making reliability an architectural requirement.

### Learning objectives

- Decompose production services
- Choose between a modular monolith, event-driven workers, and independently deployed services
- Define service objectives
- Add retries, fallbacks, and circuit breakers
- Design queues and background processing
- Implement graceful degradation
- Plan disaster recovery

### Required concepts

- API gateway
- Model gateway
- Retrieval service
- Tool service
- Queue
- Worker
- SLI
- SLO
- Retry
- Backoff
- Circuit breaker
- Bulkhead
- Load shedding
- Dead-letter queue
- Disaster recovery
- Modular monolith
- Event-driven worker
- Independently deployed service
- Service and data ownership
- Architecture decision record

### Tools

- FastAPI
- Redis or managed cache
- Queue service
- PostgreSQL
- Object storage
- Docker
- Cloud load balancer
- Parallel .NET lane: ASP.NET Core, hosted or background workers, a supported queue client, and OpenTelemetry for .NET

### Guided implementation

- Begin with explicit model, retrieval, tool, evaluation, and policy modules inside a deployable modular monolith
- Separate asynchronous or long-running work through events and workers where delivery, replay, and cancellation semantics are defined
- Extract an independently deployed service only when scaling, isolation, ownership, compliance, or release evidence justifies the operational cost
- Define health and readiness checks
- Add retry budgets
- Add circuit breakers
- Add provider and model fallback
- Add dead-letter handling
- Test dependency failures
- Define recovery objectives

### Architecture decision exercise

- Write an ADR comparing a modular monolith, event-driven workers, and microservices for the same model, retrieval, and agent workload
- Evaluate team ownership, deployment coupling, latency, data consistency, independent scaling, failure isolation, security boundaries, operability, and cost
- Include context and constraints, options, measured evidence, decision, rejected alternatives, consequences, migration triggers, and reversal plan
- Draw request, event, data-ownership, failure, and identity-propagation flows for the selected design

### Parallel .NET implementation lab

- Implement the selected architecture as an ASP.NET Core API with explicit application modules
- Move one justified long-running operation to a background worker through a durable queue
- Preserve correlation, cancellation, idempotency, tenant identity, and authorization across the API-to-worker boundary
- Do not introduce a separately deployed service unless the ADR evidence selects it

### Practical assignment

Harden the production Applied AI platform with failure injection.

### Evaluation criteria

- SLOs are explicit
- Failures degrade predictably
- Write operations remain safe under retries
- Queued work can be replayed
- Recovery procedures are tested
- The ADR makes a defensible choice from measured constraints rather than assuming microservices
- A failure-injection report demonstrates the selected topology's isolation, replay, and degradation behavior
- Acceptance evidence includes the ADR, diagrams, benchmark, operating-cost estimate, migration triggers, and recovery test

### Interview preparation

- How would your RAG system behave if the model provider fails?
- Retry versus circuit breaker
- Readiness versus liveness
- Graceful degradation
- When should an AI system remain a modular monolith, add event-driven workers, or extract microservices?
- Which measurements would cause you to reverse that architecture decision?

## Observability, feedback, and cost

### Employment outcome

Measure software health, AI quality, user outcomes, safety events, and unit economics in one system.

### Business problem

Infrastructure metrics can look healthy while AI task quality declines or costs become unsustainable.

### Learning objectives

- Instrument distributed traces
- Track prompt, model, retrieval, and tool versions
- Protect sensitive telemetry
- Connect traces to feedback
- Calculate cost per successful task
- Apply RED, USE, and the four golden signals
- Correlate software, AI-quality, deployment, and resource evidence during incidents

### Required concepts

- Logs
- Metrics
- Traces
- Correlation IDs
- Semantic conventions
- Quality telemetry
- Feedback
- Cost attribution
- Sampling
- Redaction
- RED: request rate, errors, and duration
- USE: utilization, saturation, and errors
- Four golden signals: latency, traffic, errors, and saturation
- Deployment and configuration change events
- Incident evidence, hypotheses, and runbook approvals

### Tools

- OpenTelemetry
- Prometheus
- Grafana
- Cloud monitoring
- AI tracing platform
- Parallel .NET lane: OpenTelemetry for ASP.NET Core, outbound HTTP, database, queue, and custom AI spans

### Guided implementation

- Trace a request through API, retrieval, model, and tool calls
- Add token and cost metrics
- Add retrieval-quality metadata
- Add user feedback
- Add safety-event metrics
- Redact sensitive content
- Build operational and product dashboards
- Build RED views for each request-driven service
- Build USE views for CPU, memory, network, queue, database, and accelerator resources where present
- Alert on actionable golden-signal symptoms and link alerts to traces, deployments, model, prompt, index, and capability versions, and runbooks

### Optional AIOps project: IncidentPilot

- Correlate redacted logs, metrics, traces, alerts, deployment changes, and configuration changes for a controlled incident dataset
- Use deterministic correlation and anomaly rules as the baseline before adding an AI-assisted explanation
- Produce ranked root-cause hypotheses with cited evidence, confidence, contradictions, and explicit unknowns
- Draft an incident timeline, impact statement, recommended diagnostic steps, and a proposed versioned runbook
- Require a named human to approve the exact runbook step before any execution
- Keep execution disabled in the default project; never perform autonomous remediation
- Audit inputs, model and prompt version, retrieved evidence, hypotheses, approvals, and any permitted test-environment execution
- Evaluate known incidents, misleading correlations, missing telemetry, prompt injection in logs, repeated alerts, false positives, and provider failure

### Parallel .NET observability lab

- Instrument the ASP.NET Core request, model, retrieval, MCP, tool, memory, database, and queued-work paths
- Export compatible RED, USE, golden-signal, AI-quality, safety, and cost telemetry
- Demonstrate one end-to-end incident trace and one redaction test

### Practical assignment

Create observability dashboards for the enterprise assistant and optionally build IncidentPilot against a controlled incident dataset.

### Evaluation criteria

- One request can be followed end to end
- Model and prompt versions are visible
- Costs are attributed by tenant and feature
- Sensitive content is controlled
- Alerts correspond to actionable conditions
- RED, USE, and golden-signal dashboards use documented queries, thresholds, owners, and runbook links
- Alerts correlate with model, prompt, retrieval-index, capability, deployment, and configuration versions
- IncidentPilot, when selected, cites evidence, exposes uncertainty, resists hostile telemetry, and cannot remediate without explicit human approval
- Acceptance evidence includes dashboard exports, alert tests, a redaction test, incident fixtures, hypothesis-scoring results, and an immutable approval/audit example

### Interview preparation

- What should be monitored in an LLM application?
- Cost per token versus cost per successful task
- How do you trace RAG failures?
- How do you prevent telemetry from leaking PII?
- How do RED, USE, and the four golden signals complement AI-quality metrics?
- How would you evaluate an AI incident assistant without letting it become an unsafe remediation agent?

## Cloud deployment and infrastructure

### Employment outcome

Deploy AI services securely to one major cloud platform.

### Business problem

Production deployment requires identity, networking, storage, secrets, scaling, monitoring, and cost controls beyond application code.

### Learning objectives

- Containerize services
- Configure cloud identity and networking
- Use managed storage and databases
- Deploy CPU and GPU workloads
- Manage secrets
- Automate infrastructure

### Required concepts

- Container image
- Registry
- IAM
- Virtual network
- Load balancer
- DNS
- Object storage
- Managed database
- Secret manager
- Queue
- Autoscaling
- Infrastructure as code

### Tools

- Docker
- Selected cloud platform
- Terraform
- GitHub Actions
- Cloud monitoring

### Guided implementation

- Build a non-root image
- Push to a registry
- Provision network and storage
- Provision PostgreSQL and Redis
- Store secrets
- Deploy the API and worker
- Configure HTTPS and identity
- Add autoscaling and budgets

### Practical assignment

Deploy the enterprise assistant to the selected cloud.

### Evaluation criteria

- No long-lived credentials are stored in code
- Infrastructure is reproducible
- Network access is restricted
- Backups and restore are configured
- Costs and resource ownership are tagged

### Interview preparation

- How do you deploy an AI API?
- Managed service versus Kubernetes
- How do workloads access secrets?
- How do you control cloud cost?

## Kubernetes for AI workloads

### Employment outcome

Operate training, inference, and pipeline workloads on Kubernetes when role or scale requires it.

### Business problem

AI platforms often need independent scaling, GPU scheduling, batch jobs, and controlled rollouts.

### Learning objectives

- Deploy services and jobs
- Configure resources and health checks
- Schedule GPU workloads
- Autoscale
- Perform rolling and canary releases
- Diagnose failures

### Required concepts

- Pod
- Deployment
- Service
- Ingress
- ConfigMap
- Secret
- Job
- CronJob
- Persistent volume
- Resource requests and limits
- GPU scheduling
- Autoscaling

### Tools

- Kubernetes
- Helm
- KServe awareness
- Prometheus
- Grafana

### Guided implementation

- Deploy the model gateway
- Deploy a worker
- Add resource requests and limits
- Add readiness and liveness checks
- Add horizontal autoscaling
- Schedule a GPU inference service
- Perform a rolling update
- Diagnose crash and scheduling failures

### Practical assignment

Create a Kubernetes deployment for an AI service and one training job.

### Evaluation criteria

- Workloads have correct resources
- Unhealthy pods leave service
- Deployments roll back
- Secrets are not stored in images
- GPU workloads schedule predictably

### Interview preparation

- Request versus limit
- Deployment versus Job
- How do GPUs schedule?
- Why can autoscaling an LLM service be difficult?

## LLMOps and MLOps

### Employment outcome

Automate the versioning, evaluation, approval, deployment, monitoring, and rollback of prompts, datasets, models, and adapters.

### Business problem

AI changes are unsafe when teams cannot reproduce which data, code, prompt, model, and configuration produced a deployed behavior.

### Learning objectives

- Track experiments and artifacts
- Maintain registries
- Build evaluation gates
- Automate training and deployment
- Use canary and shadow releases
- Roll back regressions

### Required concepts

- Experiment
- Artifact
- Lineage
- Registry
- Continuous integration
- Continuous delivery
- Continuous training
- Canary
- Shadow deployment
- Rollback
- Drift

### Tools

- MLflow
- DVC
- GitHub Actions
- Airflow, Dagster, or cloud workflows
- Model registry
- Prompt registry
- Kubernetes when applicable

### Guided implementation

- Track prompt and model runs
- Version datasets
- Register adapters
- Add evaluation gates
- Trigger QLoRA training
- Build a container
- Deploy to staging
- Run canary evaluation
- Promote or roll back

### Practical assignment

Build an adapter lifecycle pipeline.

### Evaluation criteria

- Every deployment has complete lineage
- Failed quality or safety gates block release
- Rollback restores the previous version
- Production feedback can create reviewed training candidates
- Training and deployment are reproducible

### Interview preparation

- MLOps versus DevOps
- What should be versioned?
- Canary versus shadow deployment
- How do you trigger retraining safely?

## Open-model serving

### Employment outcome

Serve open models and LoRA adapters through production-compatible APIs.

### Business problem

Self-hosting provides control and potential cost savings but requires capacity planning, batching, cache management, and operational ownership.

### Learning objectives

- Understand model artifacts
- Launch an OpenAI-compatible server
- Configure batching and caches
- Serve adapters
- Authenticate and observe requests
- Compare self-hosted and managed cost

### Required concepts

- Safetensors
- Tokenizer artifacts
- Continuous batching
- KV cache
- Prefix caching
- Chunked prefill
- Streaming
- Adapter serving
- Multi-model routing

### Tools

- vLLM or SGLang
- llama.cpp for local use
- Hugging Face Hub or private registry
- Prometheus

### Guided implementation

- Validate model licence and artifacts
- Launch a server
- Stream output
- Load a LoRA adapter
- Enable prefix caching
- Add authentication
- Add metrics
- Test multiple sequence lengths

### Practical assignment

Deploy the adapted support model through an OpenAI-compatible API.

### Evaluation criteria

- Server passes functional evaluation
- Adapter and base versions are traceable
- Concurrency and context limits are enforced
- Throughput and latency are reported
- Self-hosted cost is compared with hosted APIs

### Interview preparation

- What is continuous batching?
- What is the KV cache?
- Why does long context reduce capacity?
- How do you serve multiple adapters?

## Inference optimization

### Employment outcome

Optimize latency, throughput, memory, and cost without unacceptable quality loss.

### Business problem

A model that works in a notebook may be too slow or expensive under concurrent production traffic.

### Learning objectives

- Benchmark correctly
- Quantize models
- Tune batching and scheduling
- Use parallelism
- Plan capacity
- Connect performance to product objectives

### Required concepts

- Time to first token
- Inter-token latency
- End-to-end latency
- Throughput
- Queue time
- Quantization
- INT8
- INT4
- AWQ and GPTQ awareness
- Tensor parallelism
- Data-parallel serving
- Speculative decoding awareness

### Tools

- vLLM or SGLang
- PyTorch Profiler
- NVIDIA Nsight for specialist roles
- TensorRT-LLM for specialist roles
- Triton Inference Server
- Load-testing tools

### Guided implementation

- Establish a quality baseline
- Benchmark one-user latency
- Load test concurrent users
- Quantize the model
- Compare quality and memory
- Tune batch and cache settings
- Test tensor parallelism where hardware permits
- Calculate capacity and cost

### Practical assignment

Produce an inference optimization report and deployment configuration.

### Evaluation criteria

- Benchmarks use realistic prompts and outputs
- Warm and cold behavior are reported
- Quality is measured after every optimization
- Bottlenecks are identified through profiling
- Capacity assumptions are explicit

### Interview preparation

- Latency versus throughput
- Quantization tradeoffs
- Tensor parallelism
- How would you capacity-plan an LLM service?

## Classical machine-learning foundations

### Employment outcome

Recognize and solve problems where traditional ML is more reliable and economical than a foundation model.

### Business problem

Many forecasting, risk, ranking, and tabular prediction tasks do not need an LLM.

### Learning objectives

- Formulate supervised and unsupervised problems
- Prepare tabular data
- Train baselines and tree models
- Select metrics
- Prevent leakage
- Explain errors and uncertainty

### Required concepts

- Classification
- Regression
- Ranking
- Clustering
- Anomaly detection
- Features and labels
- Train, validation, and test sets
- Leakage
- Bias and variance
- Regularization
- Calibration

### Tools

- NumPy
- Polars or pandas
- scikit-learn
- XGBoost, LightGBM, or CatBoost
- Optuna
- MLflow

### Guided implementation

- Create a simple baseline
- Train logistic regression
- Train a tree model
- Train gradient boosting
- Use cross-validation
- Tune thresholds
- Calibrate probabilities
- Perform error and subgroup analysis

### Practical assignment

Build a service-level breach predictor.

### Evaluation criteria

- A simple baseline is included
- Splits reflect production timing
- Leakage checks are documented
- Metrics match business costs
- Probabilities are calibrated when used for decisions

### Interview preparation

- Precision versus recall
- ROC-AUC versus PR-AUC
- Why cross-validation?
- What is leakage?
- Why can boosting outperform deep learning on tabular data?

## Production machine learning

### Employment outcome

Build complete training, batch, online, monitoring, and retraining systems.

### Business problem

A good offline model can fail after deployment because features, populations, labels, and operational conditions change.

### Learning objectives

- Build reproducible feature and training pipelines
- Serve batch and online predictions
- Monitor inputs and performance
- Detect drift
- Retrain and deploy safely

### Required concepts

- Feature pipeline
- Feature store awareness
- Model registry
- Batch inference
- Online inference
- Shadow deployment
- Canary deployment
- Data drift
- Concept drift
- Delayed labels
- Retraining trigger

### Tools

- scikit-learn or boosting library
- MLflow
- Airflow or Dagster
- FastAPI
- Docker
- Monitoring stack

### Guided implementation

- Build a reproducible feature pipeline
- Register the model
- Add batch scoring
- Add an online endpoint
- Add input monitoring
- Add delayed-label evaluation
- Add retraining
- Deploy as shadow then canary

### Practical assignment

Productionize the service-level breach predictor.

### Evaluation criteria

- Training-serving feature consistency is tested
- Predictions are traceable to model and feature versions
- Drift alerts have response procedures
- Retraining requires evaluation gates
- Rollback is tested

### Interview preparation

- Training-serving skew
- Data drift versus concept drift
- Batch versus online inference
- How do you monitor a model without immediate labels?

## Deep learning for AI engineers

### Employment outcome

Train and productionize neural models used in language, vision, speech, and embeddings.

### Business problem

Specialist AI roles require understanding neural architectures and training behavior beyond high-level APIs.

### Learning objectives

- Build neural networks in PyTorch
- Understand common architectures
- Train with GPUs
- Evaluate and deploy models
- Diagnose overfitting and optimization issues

### Required concepts

- Layers
- Activations
- Initialization
- Normalization
- Dropout
- CNNs
- Recurrent-model awareness
- Attention
- Transformers
- Vision transformers
- Embedding models

### Tools

- PyTorch
- torchvision
- Transformers
- MLflow
- ONNX Runtime

### Guided implementation

- Build a feed-forward model
- Build or fine-tune an image classifier
- Fine-tune a text encoder
- Compare frozen and full fine-tuning
- Export a model
- Serve it

### Practical assignment

Build product classification and semantic matching.

### Evaluation criteria

- A non-neural baseline is included
- Model and data choices are justified
- Training and validation are reproducible
- Serving latency and cost are measured
- Failure slices are reported

### Interview preparation

- Backpropagation
- Dropout
- Batch normalization versus layer normalization
- CNN versus transformer
- Transfer learning

## Capstone implementation

### Employment outcome

Demonstrate end-to-end capability expected from an Applied AI Engineer.

### Business problem

A company wants to reduce support handling time, improve answer consistency, and automate low-risk operations while preserving privacy, authorization, auditability, and human control.

### Required product capabilities

- User authentication
- Tenant and role-based authorization
- Ticket ingestion
- Multi-format document ingestion
- Hybrid retrieval
- Classic-versus-agentic retrieval routing with enforced budgets
- Reranking
- Evidence-backed generation
- Structured extraction
- Tool calling
- MCP integration
- Human approval
- Governed agent memory with consent, provenance, expiration, correction, and deletion
- Versioned reusable capabilities with explicit MCP mappings and permissions
- Feedback collection
- Prompt versioning
- Model and adapter versioning
- LoRA or QLoRA adaptation
- DPO experiment
- Multi-provider model routing
- Open-model serving
- Safety controls
- Cost controls
- Logs, metrics, and traces
- RED, USE, and four-golden-signal dashboards
- Canary deployment
- Incident handling

### Required engineering artifacts

- Product-requirements document
- Workflow map
- Architecture diagram
- Architecture decision records
- A topology ADR comparing a modular monolith, event-driven workers, and microservices
- Data model
- API specification
- Threat model
- Evaluation plan
- Golden dataset
- Dataset card
- Adapter or model card
- System card
- Deployment configuration
- Runbooks
- Cost model
- Load-test report
- Failure-injection report
- Classic-versus-agentic RAG quality-latency-cost report
- Memory governance and verified-deletion report
- Capability manifest, MCP mapping, and sandbox-policy evidence
- Business-outcome report

### Implementation milestones

- Establish deterministic and human baselines
- Build the secure backend
- Build ingestion and retrieval
- Benchmark classic RAG before adding bounded agentic retrieval
- Add model generation
- Add evaluation
- Add tools and approval
- Add governed memory and versioned capability controls
- Add feedback
- Build training data
- Train LoRA or QLoRA
- Run DPO experiment
- Deploy hosted and open-model options
- Add observability
- Add RED, USE, and golden-signal views
- Add security tests
- Run load and failure tests
- Release a canary
- Measure user and business outcomes

### Acceptance criteria

- Quality thresholds are met on a held-out dataset
- Unauthorized content is never retrieved
- Consequential actions require approval
- Every response and action is traceable
- The system abstains when evidence is insufficient
- Deployment can roll back
- Cost per resolved case is reported
- Failure behavior is demonstrated
- Documentation allows another engineer to operate the system
- The selected backend passes shared API, RAG, agent, MCP, authorization, evaluation, and telemetry acceptance fixtures
- Agentic retrieval cannot exceed configured subquery, iteration, concurrency, latency, token, or spending limits
- Memory correction and deletion propagate to derived summaries, indexes, and caches within a tested objective
- Every capability and MCP operation is versioned, authorized, sandboxed where executable, and auditable
- The topology ADR is supported by measurements and includes migration and reversal triggers

### Parallel .NET capstone variant

- Python remains the reference path; learners targeting .NET roles may implement the production backend in C# and ASP.NET Core
- Use supported provider integrations behind application-owned interfaces for structured output, streaming, RAG, tools, and fallback
- Implement authenticated MCP consumption or serving, governed memory, background work, and OpenTelemetry instrumentation
- Preserve the same schemas, evaluation set, permission model, safety controls, quality thresholds, latency and cost budgets, and failure tests as the reference path
- Include a reproducible build, automated tests, container configuration, API contract, redacted trace, and deployment/runbook evidence
- Do not require both full Python and full .NET capstones; compare only the shared contract and benchmark slices needed to prove equivalence

### Capstone interview defense

Prepare to explain:

- Why AI was used
- Which parts remain deterministic
- Why RAG, tools, and fine-tuning were selected
- How evaluation data was created
- How access control works
- How prompt injection is handled
- How training changed behavior
- How deployment and rollback work
- How quality, latency, cost, and business value are measured
- Why the selected Python or .NET implementation preserves domain boundaries and avoids framework lock-in
- Why classic or agentic retrieval was selected for each query class
- How memory, capabilities, MCP, sandboxing, and human authorization are governed

## Role-selection lessons

After the shared lessons, choose one primary specialization.

### Core scope boundary

Diffusion and generative image or video engineering, general reinforcement learning beyond LLM post-training literacy, and symbolic or neuro-symbolic AI are legitimate specialist domains but are deferred from the required core. Add them only for a role or project that needs them; they are not prerequisites for the Applied AI, RAG, agent, .NET AI, or production-system outcomes in this curriculum.

### Applied AI Engineer specialization

Deepen:

- Product discovery
- Enterprise integrations
- RAG
- Controlled agents
- Evaluation
- Cloud deployment
- Security
- TypeScript and React
- User feedback
- Business metrics

Build:

- A user-facing AI workflow deployed to real infrastructure

### Generative AI Engineer specialization

Deepen:

- LLM behavior
- Prompt and context engineering
- RAG
- Agents
- Multimodal APIs
- Evaluation
- Safety
- Cost optimization
- Open-model serving

Build:

- A production GenAI product with multiple models and modalities

### LLM Engineer specialization

Deepen:

- Training data
- SFT
- LoRA
- QLoRA
- DPO
- Continued pretraining
- Distillation
- Distributed training
- Serving
- Performance

Build:

- A complete domain-model adaptation and serving pipeline

### MLOps and ML Platform specialization

Deepen:

- Kubernetes
- Terraform
- Workflow orchestration
- Registries
- Training jobs
- Multi-tenancy
- Observability
- CI/CD
- Developer experience

Build:

- A self-service training, evaluation, and deployment platform

### AI Evaluation and Safety specialization

Deepen:

- Dataset design
- Human evaluation
- Model judges
- Statistics
- Agent evaluation
- Red teaming
- Safety behavior
- Incident analysis

Build:

- An evaluation and adversarial-testing service with release gates

### AI Security specialization

Deepen:

- Identity
- Authorization
- Agent permissions
- Prompt injection
- Sandboxing
- Cloud security
- Supply-chain security
- Threat modelling

Build:

- A secured agent execution environment with policy enforcement

### Machine Learning Engineer specialization

Deepen:

- Classical ML
- Deep learning
- Feature pipelines
- Batch and online inference
- Monitoring
- Drift
- Retraining
- ML system design

Build:

- A complete predictive ML platform and application

### AI Infrastructure and Inference specialization

Deepen:

- Linux
- Networking
- C++
- GPUs
- CUDA
- NCCL
- vLLM or SGLang internals
- TensorRT-LLM
- Triton
- Distributed inference

Build:

- A benchmarked multi-node or multi-GPU inference service

### Search and Recommendation specialization

Deepen:

- Information retrieval
- Candidate generation
- Learning to rank
- Personalization
- Feedback bias
- Online experimentation
- Low-latency serving

Build:

- A two-stage retrieval and ranking system with online metrics

### Multimodal specialization

Deepen:

- Computer vision
- Document intelligence
- Speech
- Audio
- Video
- Multimodal retrieval
- Streaming
- Modality-specific evaluation

Build:

- A multimodal business workflow with human review

### Forward-Deployed AI specialization

Deepen:

- Customer discovery
- Rapid prototyping
- Enterprise data
- Integrations
- Security
- Cloud delivery
- Workflow change
- User training
- Technical communication

Build:

- A reusable customer deployment package for one industry

## Interview preparation lessons

### Coding and Python

Practice:

- Arrays and strings
- Hash maps and sets
- Stacks and queues
- Trees and graphs
- Heaps
- Sorting and searching
- Basic dynamic programming
- Complexity
- Async behavior
- Testing
- API implementation

### SQL

Practice:

- Joins
- Aggregations
- CTEs
- Window functions
- Query debugging
- Indexes
- Schema design

### Applied AI cases

Practice:

- Determine whether AI is appropriate
- Define a baseline
- Choose prompting, RAG, tools, fine-tuning, or ML
- Define human approval
- Select metrics
- Estimate cost
- Identify security risks

### LLM and training

Practice:

- Tokens and attention
- Context limits
- Embeddings
- Retrieval
- Reranking
- SFT
- LoRA
- QLoRA
- DPO
- Distributed training
- Quantization

### AI system design

Practice:

- Enterprise RAG
- Support agent
- Model gateway
- Evaluation platform
- Training platform
- Inference platform
- Search system
- Recommendation system
- Fraud detection
- Classic versus bounded agentic RAG
- Governed agent memory
- MCP capability and identity propagation
- Modular monolith versus event-driven workers versus microservices
- AI incident-assistance system with human-approved runbooks

### .NET Applied AI and AI API design

Practice:

- Provider-independent model integration in ASP.NET Core
- Structured-output validation and typed contracts
- Server-sent-event streaming, cancellation, timeouts, retries, and fallback
- Token, context, rate-limit, and cost budgeting
- Embeddings, ingestion, hybrid retrieval, reranking, and citations
- Classic-versus-agentic retrieval tradeoffs and bounded execution
- Tool calling, governed memory, MCP identity, authorization, and audit
- Prompt-injection defenses across documents, tools, memory, and telemetry
- Evaluation gates, OpenTelemetry traces, RED, USE, and golden signals
- Queue, batch, accelerator, and provider failure modes
- Architecture evolution from modular monolith to workers or services

### Project deep dives

For every project, prepare:

- Business problem
- Baseline
- Architecture
- Data
- Model selection
- Evaluation
- Failure analysis
- Security
- Deployment
- Monitoring
- Cost
- Scaling
- Lessons learned

## Job-readiness assessment

### Junior Applied AI or Generative AI readiness

Required evidence:

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

### Applied AI Engineer readiness

Required evidence:

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

### Parallel .NET Applied AI readiness

Required evidence:

- Authenticated ASP.NET Core model API with structured output, streaming, cancellation, retry, and observable fallback
- Production RAG slice with authorization, citations, evaluation, and classic-versus-agentic comparison
- Controlled tool workflow with governed memory
- Authenticated MCP client or server with identity propagation and capability-version controls
- OpenTelemetry traces plus RED, USE, golden-signal, AI-quality, safety, and cost dashboards
- Architecture ADR, containerized deployment, failure tests, security tests, and interview defense

### LLM Engineer readiness

Required evidence:

- PyTorch
- Training data
- SFT
- LoRA
- QLoRA
- DPO
- Distributed fundamentals
- Open-model serving
- Quality benchmarks
- Performance benchmarks

### MLOps or platform readiness

Required evidence:

- Docker
- Cloud
- Kubernetes
- CI/CD
- Orchestration
- Registries
- Monitoring
- Terraform
- Multi-tenant design
- Rollback demonstration

### Evaluation, safety, or security readiness

Required evidence:

- Golden datasets
- Human evaluation
- Model judges
- Statistical analysis
- Adversarial tests
- Security tests
- Regression gates
- Incident analysis

### Machine Learning Engineer readiness

Required evidence:

- Classical ML
- Deep learning
- Data and feature pipelines
- Training
- Batch and online deployment
- Monitoring
- Drift
- Retraining
- ML system design

## Ongoing maintenance

Review the lessons every six months.

Update:

- Provider APIs
- Model families
- Training frameworks
- Agent protocols
- Serving engines
- Cloud services
- Security guidance
- Regulations
- Common job requirements

Retain:

- Software engineering
- Data quality
- Evaluation
- Security
- Reliability
- Cost engineering
- Product judgment
- Human oversight
- Model and system tradeoffs
