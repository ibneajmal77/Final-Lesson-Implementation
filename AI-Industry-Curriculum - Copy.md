# Industry AI Engineering Curriculum and Career Map

Updated: June 25, 2026

## Purpose

This curriculum is designed for practical employment in the AI industry. It prioritizes skills repeatedly required in production systems, technical interviews, current AI job descriptions, and enterprise deployments.

It is not an academic AI degree and does not attempt to teach every research topic. It begins with Applied AI and Generative AI, progresses through model adaptation and production operations, and introduces classical machine learning later.

The central career target is **Applied AI Engineer**.

An Applied AI Engineer converts a business problem into a reliable AI product. Depending on the problem, the solution may use hosted foundation models, open models, retrieval, agents, fine-tuning, classical machine learning, computer vision, speech, or a combination of them.

**Generative AI Engineer** and **LLM Engineer** are specializations within or adjacent to Applied AI Engineering. Applied AI is broader because it includes business discovery, product integration, data pipelines, evaluation, deployment, monitoring, security, and measurable operational outcomes.

## Industry findings that shape the curriculum

Current job titles are inconsistent. Two companies may advertise the same work as Applied AI Engineer, AI Engineer, Generative AI Engineer, Machine Learning Engineer, Product Engineer for AI, Forward-Deployed Engineer, or Solutions Engineer for AI. Responsibilities are more reliable than titles.

The recurring requirements across practical AI roles are:

- Strong Python and production software engineering
- SQL, data modelling, data quality, and data pipelines
- API design, backend integration, testing, and debugging
- Foundation-model APIs and open-model ecosystems
- Structured generation, tool calling, retrieval, and agent workflows
- Evaluation datasets, quality metrics, regression testing, and human review
- Cloud deployment, containers, observability, reliability, and cost control
- Security, privacy, permissions, auditability, and responsible AI
- Model adaptation through SFT, LoRA, QLoRA, and preference optimization for training-focused roles
- PyTorch and distributed computing for model, platform, and infrastructure roles
- Product judgment, domain understanding, stakeholder communication, and business metrics

Applied AI and forward-deployed roles increasingly require engineers who can work directly with users, identify valuable workflows, build prototypes quickly, integrate with existing enterprise systems, and turn successful prototypes into reusable production systems.

Agentic AI is important, but production employers need controlled workflows, permissions, evaluation, and observability. Knowing an agent framework without understanding reliability and security is not sufficient.

Model training remains important, but the required depth differs by role:

- Applied AI Engineers need to select between prompting, retrieval, tools, fine-tuning, and classical ML.
- LLM Engineers need to build and evaluate SFT, LoRA, QLoRA, preference optimization, and serving pipelines.
- Machine Learning Engineers need complete training, deployment, monitoring, and retraining pipelines.
- Model Training and Post-Training Engineers need deeper distributed training, data curation, optimization, and alignment.
- AI Infrastructure Engineers need GPU, distributed systems, inference, and performance engineering.

## Practical AI role map

| Role family | Primary responsibility | Required depth |
|---|---|---|
| Applied AI Engineer | Solves business problems with AI and owns the product from discovery through production | Broad AI, backend, data, evaluation, cloud, product judgment |
| Generative AI Engineer | Builds LLM, RAG, agent, document, voice, and multimodal applications | Deep GenAI application engineering |
| LLM Engineer | Adapts, evaluates, serves, and optimizes language models | Open models, training, post-training, evaluation, serving |
| Machine Learning Engineer | Builds and operates predictive and learning systems | Classical ML, deep learning, pipelines, deployment, monitoring |
| Model Training Engineer | Trains or continues training foundation and domain models | PyTorch, distributed training, data, optimization, GPU systems |
| Post-Training Engineer | Improves model behavior after pretraining | SFT, preferences, reward models, DPO/RL methods, evaluations |
| Data Scientist for ML | Uses statistics, experiments, and models to influence decisions | SQL, statistics, experimentation, ML, communication |
| Applied Scientist | Develops advanced modelling methods for product problems | Strong ML/deep learning, experimentation, papers, production collaboration |
| MLOps Engineer | Automates training, deployment, monitoring, and governance | Cloud, CI/CD, orchestration, registries, observability |
| ML Platform Engineer | Builds internal platforms used by ML teams | Distributed systems, APIs, Kubernetes, developer experience |
| AI Infrastructure Engineer | Operates GPU clusters and large-scale training or inference | Systems, accelerators, networking, scheduling, reliability |
| AI Inference Engineer | Optimizes model-serving latency, throughput, memory, and cost | vLLM/SGLang, quantization, GPU profiling, distributed inference |
| AI Data Engineer | Builds datasets and pipelines for training and evaluation | Data systems, quality, lineage, Spark, orchestration |
| AI Data or Annotation Engineer | Creates instruction, preference, multimodal, and evaluation data | Labelling systems, quality control, privacy, active learning |
| AI Evaluation Engineer | Measures model and system quality in realistic tasks | Dataset design, statistics, judges, human evaluation, regression systems |
| AI Safety Engineer | Tests and mitigates harmful or unreliable model behavior | Safety evaluations, red teaming, alignment, monitoring |
| AI Security Engineer | Secures AI applications, agents, data, models, and infrastructure | Application security, prompt injection, identity, sandboxing |
| NLP Engineer | Builds language understanding and generation systems | NLP, transformers, retrieval, language evaluation |
| Computer Vision Engineer | Builds image and video perception systems | Vision models, data pipelines, augmentation, deployment |
| Speech and Audio Engineer | Builds transcription, synthesis, diarization, and audio systems | Signal processing, speech models, streaming inference |
| Multimodal AI Engineer | Builds systems combining language, image, audio, video, or documents | Multimodal models, modality pipelines, cross-modal evaluation |
| Search and Ranking Engineer | Builds retrieval, relevance, and ranking systems | Information retrieval, embeddings, learning to rank, experimentation |
| Recommender Systems Engineer | Builds personalization and recommendation systems | Candidate generation, ranking, feedback loops, online evaluation |
| Robotics and Autonomy Engineer | Builds AI for physical systems | Perception, planning, control, simulation, real-time software |
| Edge AI Engineer | Deploys models to constrained devices | Quantization, ONNX, TensorRT, mobile/embedded runtimes |
| Forward-Deployed AI Engineer | Works directly with customers to deploy valuable AI workflows | Applied AI breadth, integrations, communication, delivery |
| AI Solutions Architect | Designs enterprise AI systems and adoption patterns | Architecture, cloud, security, governance, stakeholder work |
| AI Product Manager | Defines valuable AI products, metrics, risk boundaries, and delivery | Product discovery, AI capabilities, evaluation, UX, business metrics |
| AI Governance Specialist | Defines controls, risk processes, documentation, and compliance | NIST, ISO, regulation, audit, model inventory |
| AI UX or Conversation Designer | Designs human interaction with AI systems | Interaction design, conversation flows, trust, testing |

Research Scientist and frontier Research Engineer are legitimate industry roles, but they are not the main target of this curriculum because they usually require deeper mathematics, publications, or specialized research experience.

## Recommended career positioning

The strongest broad positioning is:

> Applied AI Engineer with Generative AI, model adaptation, evaluation, and production MLOps capability.

This positioning can branch into:

- Generative AI and agent systems
- LLM training and post-training
- Machine learning engineering
- MLOps and ML platform engineering
- AI evaluation, safety, and security
- Search, recommendation, NLP, vision, speech, or multimodal AI
- Forward-deployed AI and solutions architecture

## Learning order

Use this sequence:

```text
Engineering foundations
→ Applied AI product thinking
→ Foundation-model applications
→ Retrieval and RAG
→ Evaluation and feedback data
→ Tool use, agents, and MCP
→ Model adaptation and post-training
→ Multimodal and voice systems
→ Safety and security
→ Production deployment
→ LLMOps and MLOps
→ Open-model serving and inference
→ Classical machine learning
→ Deep learning and complete ML engineering
→ Selected role specialization
```

Do not attempt every specialization simultaneously. Complete the shared Applied AI core, then select a primary branch and one supporting branch.

## Standard lesson format

Every lesson in this curriculum must contain:

- Business reason for learning the topic
- Concept definitions and mental model
- Architecture and data flow
- Implementation from a minimal version
- Implementation using the selected industry tool
- Configuration and environment management
- Tests and evaluation criteria
- Edge cases and failure modes
- Security and privacy considerations
- Performance, latency, and cost considerations
- Observability and operational requirements
- Comparison with alternatives
- Interview questions
- Practical assignment
- Production-readiness checklist

Every project must contain:

- Business problem and target user
- Functional and non-functional requirements
- Architecture diagram
- Data contracts and API contracts
- Baseline solution
- Evaluation dataset and acceptance thresholds
- Automated tests
- Security threat model
- Docker environment
- CI pipeline
- Deployment instructions
- Logs, metrics, and traces
- Cost and performance measurements
- Failure recovery plan
- README explaining tradeoffs

## Tool-selection policy

Tools are divided into three categories.

**Required tools** are common enough to justify direct implementation experience.

**Choose-one tools** solve the same type of problem. Learn one deeply and understand the alternatives.

**Role-dependent tools** are learned only when pursuing the relevant specialization.

Frameworks change quickly. Learn protocols, architecture, data flow, and failure handling before framework-specific abstractions.

## Shared industry technology stack

### Required programming and engineering tools

- Python
- SQL
- Git and GitHub
- Linux and shell usage
- HTTP, REST, JSON, JSON Schema, and OpenAPI
- Python type hints
- Pydantic
- FastAPI
- pytest
- Ruff
- PostgreSQL
- Redis
- Docker and Docker Compose
- GitHub Actions or an equivalent CI system

### Required AI application tools

- At least one major hosted model API
- Native provider SDKs
- Hugging Face Transformers
- Hugging Face Datasets
- sentence-transformers or equivalent embedding models
- pgvector
- OpenSearch or Elasticsearch fundamentals
- MLflow
- OpenTelemetry

### Required open-model training tools

- PyTorch
- Transformers
- Datasets
- PEFT
- TRL
- Accelerate
- bitsandbytes where supported
- Safetensors

### Required model-serving tools

- vLLM or SGLang as the primary high-throughput server
- llama.cpp for local, CPU, desktop, or edge-oriented serving awareness
- ONNX Runtime fundamentals

### Choose-one orchestration approach

- Native tool-calling and workflow code first
- LangGraph
- A provider-supported agents SDK
- Semantic Kernel for Microsoft-heavy enterprise environments
- LlamaIndex for retrieval-heavy systems

Only one orchestration framework needs deep study. Native APIs and explicit state machines come first.

### Choose-one cloud platform

- AWS with Bedrock, SageMaker, ECS/EKS, S3, RDS, and CloudWatch
- Azure with Azure AI Foundry, Azure Machine Learning, AKS, Blob Storage, PostgreSQL, and Azure Monitor
- Google Cloud with Vertex AI, GKE, Cloud Storage, Cloud SQL, and Cloud Monitoring

Learn one cloud deeply. Learn the service mapping for the others rather than duplicating every exercise.

### Role-dependent data and streaming tools

- Apache Spark
- Kafka
- Airflow
- Dagster
- dbt
- Snowflake
- BigQuery
- Databricks
- Feature stores such as Feast or a managed equivalent

### Role-dependent platform tools

- Kubernetes
- Helm
- Terraform
- Argo CD
- Argo Workflows
- Kubeflow
- KServe
- Ray
- Prometheus
- Grafana

### Role-dependent performance tools

- CUDA
- NVIDIA Nsight
- PyTorch Profiler
- TensorRT-LLM
- Triton Inference Server
- DeepSpeed
- FSDP
- NCCL

### Product integration tools

- TypeScript and Node.js fundamentals
- React fundamentals for building AI interfaces
- WebSockets and server-sent events
- OAuth and OpenID Connect
- Enterprise identity providers

Python remains the primary language. TypeScript is a supporting skill for Applied AI Engineers who integrate AI into user-facing products.

## Engineering foundations

### Python for production AI

Learn:

- Data types, collections, functions, modules, and packages
- Classes, dataclasses, composition, and interfaces
- Type hints, protocols, generics, and validation
- Exceptions and error classification
- Logging and structured logs
- Configuration and environment variables
- Secrets and credential handling
- Iterators, generators, decorators, and context managers
- Async I/O
- Threads and processes
- Memory and resource management
- Packaging with `pyproject.toml`
- Dependency locking and reproducible environments
- Unit tests, integration tests, mocks, fixtures, and parameterization
- Profiling and debugging

Use:

- Python
- uv
- Pydantic
- pytest
- Ruff
- mypy or Pyright

Build:

- A command-line document processor
- A typed configuration system
- External API clients with retries and timeouts
- Unit and integration tests
- Structured logs

Interview coverage:

- Python data structures
- Iterators and generators
- Async behavior
- Error handling
- Testing external dependencies
- Time and space complexity

### Backend and API engineering

Learn:

- HTTP methods, headers, status codes, and caching
- REST API design
- OpenAPI and JSON Schema
- Authentication and authorization
- OAuth and OpenID Connect fundamentals
- Request validation
- Synchronous and asynchronous endpoints
- Streaming responses
- Background jobs
- Webhooks
- Idempotency
- Rate limiting
- Timeouts, retries, backoff, and circuit breakers
- API versioning
- Multi-tenant API design

Use:

- FastAPI
- Pydantic
- HTTPX
- PostgreSQL
- Redis

Build:

- A production-style support-ticket API
- Authentication and role-based access
- PostgreSQL persistence
- Redis caching
- Streaming endpoint
- Background processing
- API documentation

### Databases and data fundamentals

Learn:

- Relational modelling
- Primary and foreign keys
- Joins, aggregations, CTEs, and window functions
- Transactions and isolation
- Indexes and query plans
- Connection pools
- Schema migrations
- JSON columns
- Row-level security
- Object storage
- Data validation
- Batch and stream concepts
- Data lineage and provenance

Use:

- PostgreSQL
- SQLAlchemy or SQLModel
- Alembic
- Redis
- Parquet
- One object-storage service

### Git, delivery, and development workflow

Learn:

- Commits, branches, merge strategies, and pull requests
- Code review
- Release tags
- Semantic versioning
- Pre-commit checks
- CI pipelines
- Dependency and secret scanning
- Reproducible local development

## Applied AI product engineering

### Business problem discovery

Learn:

- Identify the user and workflow
- Find costly, slow, repetitive, or error-prone work
- Define the current baseline
- Distinguish automation from decision support
- Identify where human approval is mandatory
- Estimate expected business value
- Identify legal, security, and data constraints
- Determine whether AI is necessary

### AI solution selection

Learn when to use:

- Deterministic software
- Rules and search
- Hosted foundation-model APIs
- Retrieval-augmented generation
- Tool calling
- Controlled agent workflows
- Fine-tuning
- Classical machine learning
- Computer vision or speech models
- Human operations
- A hybrid system

### Product requirements for AI

Define:

- User task and success criteria
- Quality threshold
- Allowed and prohibited behavior
- Latency target
- Availability target
- Cost per task
- Data-retention policy
- Human escalation path
- Audit requirements
- Failure fallback

### AI user experience

Learn:

- Progressive disclosure
- Streaming and perceived latency
- Showing sources and uncertainty
- Editable AI drafts
- Human confirmation for actions
- Feedback collection
- Failure explanations
- Accessibility
- Avoiding automation bias

### Stakeholder and domain work

Learn:

- Requirement interviews
- Domain-language mapping
- Workflow observation
- Translating model metrics into business impact
- Communicating uncertainty
- Writing design documents
- Running demos and pilots
- Measuring adoption

### Applied AI discovery project

Business problem:

A support organization wants to reduce handling time without allowing AI to make unauthorized customer-impacting decisions.

Deliver:

- Workflow map
- Baseline time and cost
- Candidate AI use cases
- Risk classification
- Build-versus-buy analysis
- Proposed architecture
- Evaluation plan
- Human-approval boundaries
- Expected return on investment

## Foundation-model and LLM engineering

### Foundation-model concepts

Learn:

- Tokens and tokenization
- Embeddings
- Autoregressive generation
- Logits and probabilities
- Transformer blocks
- Self-attention
- Positional information
- Context windows
- Encoder, decoder, and encoder-decoder models
- Dense and mixture-of-experts models
- Reasoning models
- Multimodal models
- Pretraining
- Continued pretraining
- Supervised fine-tuning
- Preference optimization
- Inference

The objective is operational understanding, not reproducing a transformer paper from scratch.

### Generation behavior

Learn:

- Temperature
- Top-p and top-k
- Stop conditions
- Maximum output
- Repetition behavior
- Deterministic and sampled generation
- Structured decoding
- Context limits
- Lost-in-the-middle behavior
- Hallucination and uncertainty

### Model selection

Compare:

- Task quality
- Tool-use reliability
- Structured-output reliability
- Multimodal capability
- Context capacity
- Latency
- Throughput
- Price
- Data handling
- Regional availability
- Fine-tuning support
- Open-weight versus hosted
- Vendor lock-in

### Model API engineering

Learn:

- Authentication
- Message and response formats
- Streaming
- Structured outputs
- Tool calling
- Image, audio, and document inputs
- Conversation state
- Token counting
- Rate limits
- Retry policy
- Timeout policy
- Provider errors
- Fallback models
- Request tracing
- Cost attribution

### Prompt and context engineering

Learn:

- Instruction hierarchy
- Clear task and output contracts
- Few-shot examples
- Prompt templates
- Delimiters and untrusted context
- Structured outputs
- Context selection
- Context compression
- Prompt versioning
- Prompt regression testing
- Multilingual prompts
- Prompt injection awareness

### LLM application project

Business problem:

Support agents manually classify requests, extract customer issues, assign urgency, and draft repetitive replies.

Build:

- Classification
- Structured extraction
- Priority recommendation
- Response drafting
- Streaming UI or API
- Human approval
- Conversation persistence
- Retry and fallback
- Token and cost tracking
- Prompt registry
- Regression test suite

Acceptance requirements:

- Valid schema output
- Measured classification quality
- Defined abstention behavior
- No automatic customer-facing action
- Traceable prompt and model version

## Retrieval, embeddings, and RAG

### Information retrieval foundations

Learn:

- Lexical retrieval
- BM25
- Dense retrieval
- Embedding spaces
- Cosine similarity and dot product
- Approximate nearest-neighbour search
- Hybrid retrieval
- Metadata filters
- Cross-encoder reranking
- Query expansion
- Query rewriting
- Retrieval latency

### Document and content ingestion

Learn:

- PDF, HTML, email, Office, and plain-text parsing
- OCR
- Scanned-document handling
- Tables
- Images and captions
- Cleaning and normalization
- Language detection
- Deduplication
- Metadata enrichment
- Chunk identifiers
- Document versions
- Incremental indexing
- Delete propagation
- Permission metadata

### Chunking

Compare:

- Fixed-token chunking
- Structure-aware chunking
- Semantic chunking
- Parent-child retrieval
- Sentence-window retrieval
- Table-aware chunking
- Code-aware chunking

Evaluate chunking rather than selecting it by intuition alone.

### Production RAG architecture

Learn:

- Ingestion pipeline
- Embedding pipeline
- Index design
- Query classification
- Query rewriting
- Hybrid retrieval
- Reranking
- Context assembly
- Source citations
- Answer generation
- Abstention
- Conversational retrieval
- Multi-query retrieval
- Knowledge freshness
- Caching
- Tenant isolation
- Document permissions
- Retrieval observability

### Advanced retrieval used in industry

Learn when needed:

- Multi-stage retrieval
- Hierarchical retrieval
- Graph-enhanced retrieval
- SQL and structured-data retrieval
- Federated retrieval across sources
- Multimodal document retrieval
- Code retrieval
- Personalized retrieval

Graph RAG is role-dependent. It is not a default replacement for a well-evaluated hybrid retrieval system.

### Retrieval tools

Required:

- pgvector
- OpenSearch or Elasticsearch
- sentence-transformers

Choose according to scale:

- FAISS for local or embedded retrieval
- Managed vector database when operational requirements justify it
- Cloud-native search services in the selected cloud

### RAG evaluation

Measure:

- Recall at K
- Precision at K
- Mean reciprocal rank
- NDCG
- Context relevance
- Answer correctness
- Groundedness
- Citation accuracy
- Completeness
- Abstention quality
- Latency
- Cost

Perform failure attribution:

- Ingestion failure
- Parsing failure
- Chunking failure
- Embedding failure
- Retrieval failure
- Reranking failure
- Context-construction failure
- Generation failure
- Permission failure

### Enterprise RAG project

Business problem:

Employees cannot reliably locate answers across policies, product manuals, contracts, and internal procedures.

Build:

- Multi-format ingestion
- OCR and table extraction
- Hybrid retrieval
- Reranking
- Citations
- Role-based access
- Incremental updates
- Delete handling
- User feedback
- Retrieval and answer evaluation
- Prompt-injection controls
- Monitoring dashboard

Production requirements:

- Users can access only authorized documents
- Every factual answer links to evidence
- Unsupported questions produce abstention
- Content updates become searchable within a defined service level
- Retrieval and generation failures are independently traceable

## Evaluation and feedback engineering

### Evaluation design

Learn:

- Convert requirements into testable behavior
- Define evaluation slices
- Create positive, negative, boundary, and adversarial cases
- Separate model evaluation from system evaluation
- Define minimum quality gates
- Measure business outcomes separately from model metrics

### Evaluation datasets

Learn:

- Golden datasets
- Representative sampling
- Difficult-case mining
- Production-feedback sampling
- Test-set contamination
- Versioning
- Dataset review
- Annotation guidelines
- Inter-annotator agreement
- Privacy review

### Deterministic evaluation

Use:

- Exact match
- Schema validation
- Unit tests
- Tool-call argument validation
- Citation verification
- Database-state verification
- Task completion checks

### Model-based evaluation

Learn:

- Pointwise judging
- Pairwise comparison
- Rubric-based judging
- Multi-judge evaluation
- Judge calibration
- Position and verbosity bias
- Reference-based and reference-free evaluation
- Human audit of judge decisions

### Human evaluation

Learn:

- Review interfaces
- Rubrics
- Blind comparison
- Sampling
- Escalation
- Quality assurance
- Measuring reviewer agreement

### Online evaluation

Learn:

- User feedback
- Task success
- Acceptance and edit rate
- Escalation rate
- Conversion or resolution rate
- A/B testing
- Canary analysis
- Production incident review

### Evaluation tools

Required:

- pytest
- MLflow
- Custom evaluation scripts
- OpenTelemetry traces

Choose as useful:

- Ragas
- DeepEval
- promptfoo
- LangSmith
- Phoenix
- Weights & Biases
- Cloud-native evaluation services

Do not allow an evaluation framework to replace a task-specific test design.

### AI evaluation platform project

Business problem:

Teams cannot reliably compare prompts, models, retrieval changes, fine-tuned adapters, or agent versions.

Build:

- Versioned evaluation datasets
- Deterministic checks
- Model-based judges
- Human-review queue
- Retrieval metrics
- Tool-use metrics
- Safety tests
- Cost and latency reports
- Experiment comparison
- CI quality gates
- Regression dashboard

## AI data engineering

### Data lifecycle

Learn:

- Data acquisition
- Consent and licensing
- Source provenance
- Schema definition
- Validation
- Cleaning
- Deduplication
- PII detection and removal
- Quality filtering
- Versioning
- Lineage
- Retention and deletion

### Training-data types

Learn:

- Raw pretraining corpora
- Domain-adaptation corpora
- Instruction-response data
- Multi-turn conversation data
- Tool-use trajectories
- Chosen and rejected preferences
- Ranking data
- Reward-model data
- Multimodal pairs
- Evaluation data
- Adversarial and safety data

### Data creation

Learn:

- Human annotation
- Expert annotation
- Synthetic data
- Rejection sampling
- Data augmentation
- Weak supervision
- Active learning
- Difficult-example mining
- Production-feedback loops

### Data quality

Measure:

- Correctness
- Relevance
- Coverage
- Diversity
- Duplication
- Toxicity and unsafe content
- Privacy
- Formatting compliance
- Label consistency
- Distribution drift

### Data pipeline tools

Required:

- Python
- SQL
- Polars or pandas
- Hugging Face Datasets
- Parquet
- DVC or an equivalent versioning method

Role-dependent:

- Spark
- Kafka
- Airflow or Dagster
- dbt
- Databricks
- Data warehouses
- Labelling platforms

### Training-data pipeline project

Business problem:

A company needs auditable, privacy-reviewed data for model adaptation and evaluation.

Build:

- Source registry
- Data contracts
- Validation rules
- PII redaction
- Deduplication
- Quality scoring
- Train-validation-test splits
- Leakage checks
- Dataset versioning
- Dataset card
- Approval workflow

## Tool use, agent workflows, and MCP

### Tool calling

Learn:

- Tool schemas
- JSON Schema
- Argument validation
- Tool selection
- Sequential and parallel calls
- Tool-result normalization
- Read and write operations
- Idempotency
- Retries and timeouts
- Error recovery
- Permissions
- Audit logs

### Controlled workflows

Learn:

- State machines
- Directed workflow graphs
- Routing
- Planning and execution
- Checkpointing
- Durable execution
- Human approval
- Compensating actions
- Maximum-step limits
- Time and spending budgets
- Escalation

### Agent memory

Learn:

- Request context
- Session state
- Durable state
- User preferences
- Retrieval-backed memory
- Summarized memory
- Memory expiration
- Privacy and deletion

Memory is a product and data-governance decision, not simply a vector database.

### Model Context Protocol

Learn:

- MCP architecture
- Clients and servers
- Tools, resources, and prompts
- Transport
- Capability negotiation
- Authentication and authorization
- Server trust
- Tool discovery
- Permission boundaries
- Logging and auditing
- MCP security risks

MCP is relevant to modern Applied AI and agent integration, but secure tool design remains more important than protocol familiarity.

### Agent interoperability awareness

Understand:

- Agent-to-agent communication concepts
- Workflow handoffs
- Identity propagation
- Shared context risks
- Cross-agent authorization

Do not make multi-agent design the default. Use it only when independent ownership or parallel specialization justifies the added complexity.

### Agent evaluation

Measure:

- Task-completion rate
- Tool-selection accuracy
- Argument accuracy
- Invalid-action rate
- Policy compliance
- Number of steps
- Recovery rate
- Human-intervention rate
- Latency
- Cost per successful task

### Support-resolution agent project

Business problem:

Support staff must inspect customer data, search policies, check orders, propose actions, issue approved refunds, and update tickets.

Build:

- Document retrieval
- Customer lookup
- Order API
- Refund tool
- Ticket-update tool
- Human approval before financial action
- Persistent workflow state
- Retry and compensation logic
- Permission model
- Audit trail
- Step and cost limits
- MCP integration for at least one tool
- Task-completion evaluation

## Model adaptation and post-training

### Adaptation decision framework

Compare:

- Better prompting
- Better context
- Retrieval
- Tool calling
- Supervised fine-tuning
- LoRA
- QLoRA
- Full fine-tuning
- Continued pretraining
- Preference optimization
- Knowledge distillation

Use fine-tuning when the problem involves stable behavior, format, style, task specialization, tool behavior, or domain patterns that are not solved efficiently through prompting or retrieval.

Do not use fine-tuning as a substitute for current factual knowledge, access control, or a broken retrieval pipeline.

### GPU and training fundamentals

Learn:

- GPU architecture at an operational level
- Parameters
- Activations
- Gradients
- Optimizer state
- Memory estimation
- Forward pass
- Loss
- Backpropagation
- Batch size
- Gradient accumulation
- Learning rate
- Schedulers
- Epochs and steps
- Checkpoints
- Validation
- Overfitting
- Gradient clipping
- Gradient checkpointing

### Numerical formats

Learn:

- FP32
- FP16
- BF16
- FP8 awareness
- INT8
- INT4
- Training precision versus inference quantization
- Numerical stability

### Tokenizers and chat data

Learn:

- Tokenizer loading
- Vocabulary
- Special tokens
- Chat templates
- Padding
- Truncation
- Attention masks
- Label masks
- Maximum sequence length
- Sequence packing
- Completion-only loss
- Data collators

### Supervised fine-tuning

Learn:

- Base versus instruction models
- SFT use cases
- Instruction-data formatting
- Training configuration
- Loss curves
- Validation
- Checkpoint selection
- Behavior regression
- Safety regression
- Full fine-tuning cost

Use:

- PyTorch
- Transformers
- Datasets
- TRL SFTTrainer
- Accelerate

### LoRA

Learn:

- Parameter-efficient fine-tuning
- Low-rank adaptation intuition
- Rank
- Alpha or scaling
- Target modules
- Adapter dropout
- Trainable parameter count
- Adapter checkpoints
- Adapter loading
- Adapter merging
- Multiple adapters
- Adapter routing
- LoRA serving

### QLoRA

Learn:

- Quantized base-model loading
- Four-bit weights
- NF4 concepts
- Double quantization awareness
- Compute data types
- Paged optimizers awareness
- Gradient checkpointing
- Memory-quality tradeoffs
- QLoRA checkpointing
- Merging and deployment constraints

Use:

- PEFT
- bitsandbytes
- Transformers
- TRL

### Preference data

Learn:

- Chosen and rejected responses
- Preference rubrics
- Pair construction
- Human preference collection
- AI-generated preferences
- Quality assurance
- Bias
- Leakage
- Safety preferences

### Direct Preference Optimization

Learn:

- DPO objective intuition
- Policy and reference models
- Preference strength
- Training configuration
- Over-optimization
- Behavior and safety evaluation
- Comparison with SFT

Use:

- TRL DPOTrainer

### Reward models and RL-based post-training

Industry awareness:

- Reward-model data
- Reward-model training
- PPO-based RLHF
- GRPO
- RLOO
- Verifiable rewards
- Process and outcome rewards

Direct implementation is role-dependent. It is required for Post-Training Engineer roles but not for most Applied AI Engineer positions.

### Continued pretraining

Learn when pursuing LLM or Model Training roles:

- Domain corpus preparation
- Causal language-modelling objective
- Data mixture
- Learning-rate selection
- Catastrophic forgetting
- Domain evaluation
- Infrastructure cost

### Knowledge distillation

Learn:

- Teacher and student models
- Synthetic target generation
- Logit and response distillation concepts
- Quality-cost tradeoffs
- Distillation evaluation

### Distributed training

Learn when pursuing training or platform roles:

- Data parallelism
- DistributedDataParallel
- FSDP
- DeepSpeed ZeRO
- Tensor and pipeline parallelism awareness
- Mixed precision
- Gradient accumulation
- Activation checkpointing
- Distributed checkpointing
- NCCL fundamentals
- Failure recovery
- Training utilization
- Cost calculation

Use:

- Accelerate
- FSDP or DeepSpeed
- PyTorch distributed

### Domain-model adaptation project

Business problem:

A general model does not consistently follow company support policy, tone, escalation rules, or output schemas.

Build:

- Baseline prompted model
- RAG baseline
- Versioned instruction dataset
- SFT run
- LoRA run
- QLoRA run
- Preference dataset
- DPO run
- Adapter registry
- Reproducible training configuration
- Evaluation report
- Safety regression report
- Serving endpoint

Compare:

- Base model
- Prompted model
- RAG system
- LoRA model
- QLoRA model
- RAG plus adapted model
- DPO-adjusted model

Measure:

- Task correctness
- Schema compliance
- Policy compliance
- Hallucination rate
- Abstention
- Safety behavior
- Training time
- GPU memory
- Inference latency
- Throughput
- Cost per successful task

## Multimodal, document, speech, and voice AI

### Multimodal application fundamentals

Learn:

- Image and text inputs
- Audio and text inputs
- Video sampling
- Cross-modal context
- Modality-specific preprocessing
- Structured multimodal extraction
- Multimodal evaluation

### Document intelligence

Learn:

- OCR
- Layout analysis
- Tables and forms
- Key-value extraction
- Document classification
- Page-level citations
- Human review
- Confidence thresholds

### Speech systems

Learn:

- Speech-to-text
- Text-to-speech
- Voice activity detection
- Speaker diarization
- Noise and audio quality
- Streaming audio
- Turn detection
- Interruptions
- Real-time latency
- Consent and voice privacy

### Voice agents

Learn:

- Real-time transport
- Audio buffering
- Interruption handling
- Tool calls during a conversation
- Conversation state
- Escalation to humans
- Call recording policy
- Safety and disclosure

### Computer vision branch

Learn when selected:

- Image preprocessing
- Classification
- Object detection
- Segmentation
- OCR
- Vision transformers
- Data augmentation
- Labelling
- Vision metrics
- Edge and batch inference

Use:

- PyTorch
- torchvision
- OpenCV
- Hugging Face vision models
- YOLO ecosystem when appropriate

### Multimodal operations project

Business problem:

An insurance operations team manually reviews claim forms, photographs, scanned receipts, and customer calls.

Build:

- Document classification
- OCR and structured extraction
- Image understanding
- Speech transcription
- Evidence-linked summary
- Missing-information detection
- Human-review queue
- Confidence-based routing
- Audit trail
- Multimodal evaluation

## AI safety, security, privacy, and governance

### AI application security

Learn:

- Direct prompt injection
- Indirect prompt injection
- Jailbreaking
- Sensitive-information disclosure
- Improper output handling
- Excessive agency
- Tool abuse
- System-prompt leakage
- Retrieval poisoning
- Data poisoning
- Model extraction
- Membership inference awareness
- Model denial of service
- Supply-chain risk

### Identity and permission design

Learn:

- User identity
- Service identity
- Agent identity
- OAuth scopes
- Least privilege
- Per-tool permissions
- Tenant isolation
- Row-level and document-level security
- Approval for consequential actions
- Credential rotation

### Secure execution

Learn:

- Sandboxing
- Network restrictions
- Filesystem restrictions
- Command allowlists
- Resource limits
- Time limits
- Secret isolation
- Output validation
- Browser and computer-use isolation

### Privacy

Learn:

- PII and sensitive data
- Data minimization
- Consent
- Retention
- Deletion
- Encryption
- Redaction
- Provider data policies
- Training opt-out
- Privacy impact assessments

### Safety evaluation

Learn:

- Harm taxonomies
- Misuse cases
- Refusal evaluation
- Over-refusal
- Bias and subgroup analysis
- Hallucination
- Persuasion and manipulation risks
- Dangerous capability evaluation awareness
- Adversarial testing
- Red-team operations

### Governance

Learn:

- AI system inventory
- Risk classification
- Model cards
- System cards
- Dataset cards
- Impact assessments
- Approval gates
- Audit logs
- Incident management
- Vendor assessment
- Change management
- Human oversight

### Industry frameworks and standards

Required awareness:

- NIST AI Risk Management Framework
- NIST Generative AI Profile
- OWASP guidance for LLM and Generative AI applications
- Model Context Protocol security guidance
- OpenTelemetry Generative AI semantic conventions

Role-dependent:

- ISO/IEC 42001
- ISO/IEC 23894
- EU AI Act
- Sector-specific healthcare, finance, insurance, employment, and privacy requirements

### AI safety gateway project

Business problem:

An enterprise assistant handles confidential documents and can trigger internal actions.

Build:

- Threat model
- Adversarial test set
- Prompt-injection tests
- PII redaction
- Content and policy checks
- Tool-permission service
- Human approval
- Rate and spending controls
- Audit logs
- Security regression pipeline
- Incident dashboard

## Production AI system engineering

### Production architecture

Learn:

- API gateway
- Model gateway
- Retrieval service
- Tool service
- Evaluation service
- Queue and worker design
- Object storage
- Relational storage
- Cache
- Event streaming
- Multi-tenancy
- Regional deployment

### Reliability

Learn:

- Service-level indicators and objectives
- Health and readiness checks
- Retries and backoff
- Circuit breakers
- Bulkheads
- Load shedding
- Graceful degradation
- Provider fallback
- Model fallback
- Dead-letter queues
- Idempotency
- Disaster recovery

### Caching

Learn:

- Response caching
- Prompt-prefix caching
- Retrieval caching
- Embedding caching
- Semantic caching
- Cache invalidation
- Permission-aware caching

### Background work

Learn:

- Job queues
- Scheduled jobs
- Long-running tasks
- Workflow orchestration
- Cancellation
- Progress reporting
- Retry safety

### Observability

Collect:

- Structured logs
- Metrics
- Distributed traces
- Prompt and response metadata
- Model and prompt versions
- Retrieval traces
- Tool-call traces
- Token usage
- Latency
- Cost
- Cache hits
- User feedback
- Safety events

Use:

- OpenTelemetry
- Prometheus
- Grafana
- Cloud-native monitoring

Protect sensitive prompt and response data through redaction and access control.

### Cost engineering

Learn:

- Cost per request
- Cost per successful task
- Token budgets
- Context reduction
- Model routing
- Small-model fallbacks
- Batch processing
- Caching
- Provider comparison
- GPU utilization
- Capacity planning

### Production Applied AI platform project

Business problem:

Multiple company teams need a governed platform for AI applications without duplicating model integrations, tracing, evaluation, and security.

Build:

- Multi-provider model gateway
- Authentication
- Request and spending limits
- Model routing
- Structured-output support
- Tool-call support
- Prompt registry
- Evaluation hooks
- Tracing
- Usage attribution
- Caching
- Provider fallback
- Safety controls
- Operational dashboard

## Cloud, containers, and infrastructure

### Containers

Learn:

- Docker images
- Multi-stage builds
- Non-root containers
- Dependency caching
- Health checks
- Docker Compose
- Container scanning
- Image registries

### Cloud foundations

Learn:

- Identity and access management
- Virtual networks
- Load balancers
- DNS
- Object storage
- Managed databases
- Secrets managers
- Queues
- Container services
- GPU instances
- Serverless functions
- Logging and monitoring
- Cost allocation

### Infrastructure as code

Role-dependent:

- Terraform
- Cloud-native templates
- Environment separation
- State management
- Secret references
- Review and deployment pipelines

### Kubernetes

Learn after Docker and a real cloud deployment:

- Pods
- Deployments
- Services
- Ingress
- ConfigMaps and secrets
- Resource requests and limits
- Health checks
- Autoscaling
- Jobs and scheduled jobs
- Persistent storage
- GPU scheduling
- Rolling releases
- Failure diagnosis

Kubernetes is required for MLOps, platform, and infrastructure paths. It is useful but not mandatory for the first Applied AI role.

## LLMOps and MLOps

### Experiment management

Learn:

- Run tracking
- Parameters
- Metrics
- Artifacts
- Dataset references
- Prompt versions
- Model versions
- Adapter versions
- Reproducibility

Use:

- MLflow
- DVC or equivalent data versioning

### Registries

Learn:

- Model registry
- Adapter registry
- Prompt registry
- Dataset registry
- Evaluation-result registry
- Approval status
- Lineage

### AI CI/CD

Automate:

- Unit tests
- Integration tests
- Schema tests
- Prompt regression tests
- Retrieval tests
- Model-quality tests
- Safety tests
- Container builds
- Vulnerability scans
- Staging deployment
- Canary release
- Rollback

### Continuous training

Learn:

- Trigger criteria
- New-data validation
- Retraining
- Evaluation gates
- Approval
- Deployment
- Monitoring
- Rollback

### Model monitoring

Monitor:

- Input distribution
- Output distribution
- Drift
- Accuracy proxies
- Human feedback
- Calibration
- Model errors
- Data-quality failures
- Fairness slices
- Cost and latency

### LLM monitoring

Monitor:

- Task success
- Groundedness
- Tool-call failures
- Citation failures
- Schema failures
- Refusals and over-refusals
- Prompt injection
- Token usage
- User corrections

### LLMOps platform project

Business problem:

AI teams cannot consistently train, evaluate, approve, deploy, and roll back prompts and adapters.

Build:

- Versioned datasets
- Automated QLoRA training
- MLflow tracking
- Prompt and adapter registries
- Evaluation quality gates
- Safety gates
- Container build
- Staging deployment
- Canary release
- Monitoring
- Automated or operator-approved rollback

## Open-model serving and inference engineering

### Model artifacts

Learn:

- Model configuration
- Tokenizer files
- Safetensors
- Adapter artifacts
- Quantized formats
- Model licences
- Checksums and provenance

### Serving

Learn:

- OpenAI-compatible APIs
- Continuous batching
- Dynamic batching
- KV cache
- Prefix caching
- Chunked prefill
- Streaming
- Structured generation
- Tool calling
- LoRA serving
- Multi-model serving

Use:

- vLLM or SGLang
- llama.cpp for local or edge use cases

### Quantization

Learn:

- Weight-only quantization
- INT8 and INT4
- GPTQ awareness
- AWQ awareness
- GGUF awareness
- Accuracy and throughput evaluation
- Hardware compatibility

### Distributed inference

Learn when pursuing infrastructure roles:

- Tensor parallelism
- Pipeline parallelism
- Data parallel serving
- Expert parallelism awareness
- Multi-node inference
- Network bottlenecks
- Scheduler behavior

### Inference metrics

Measure:

- Time to first token
- Inter-token latency
- End-to-end latency
- Tokens per second
- Requests per second
- Queue time
- GPU utilization
- GPU memory
- Cache utilization
- Cost per token
- Cost per successful task

### Performance tools

Use as role requires:

- vLLM
- SGLang
- PyTorch Profiler
- NVIDIA Nsight
- TensorRT-LLM
- Triton Inference Server
- Prometheus
- Load-testing tools

### Multi-model inference project

Business problem:

A company needs private, cost-controlled serving for several domain-specific adapters.

Build:

- Open base model
- Multiple LoRA adapters
- High-throughput serving
- Quantization
- Continuous batching
- Prefix caching
- Authentication
- Model routing
- Autoscaling
- Load tests
- Quality comparison
- Capacity plan
- Cost report
- Production dashboard

## Classical machine learning

Classical ML comes later in this path, but it remains essential for complete Applied AI and Machine Learning Engineering. Many business problems are cheaper, faster, and more reliable with traditional models.

### Practical mathematics

Learn:

- Vectors and matrices
- Dot products
- Matrix multiplication
- Distances and similarity
- Probability distributions
- Conditional probability
- Bayes theorem
- Expectation and variance
- Sampling
- Confidence intervals
- Hypothesis testing
- Gradients
- Loss functions
- Regularization
- Optimization

### Problem formulation

Learn:

- Classification
- Regression
- Ranking
- Clustering
- Forecasting
- Anomaly detection
- Target definition
- Label definition
- Baselines
- Offline and online metrics
- False-positive and false-negative cost

### Data preparation

Learn:

- Exploratory analysis
- Missing values
- Outliers
- Categorical encoding
- Scaling
- Feature engineering
- Feature selection
- Class imbalance
- Train-validation-test splits
- Time-based splits
- Leakage prevention

### Core models

Learn:

- Linear regression
- Logistic regression
- Decision trees
- Random forests
- Gradient boosting
- XGBoost
- LightGBM
- CatBoost
- Support-vector machines
- Nearest neighbours
- Naive Bayes
- K-means
- PCA
- Isolation forests

### Evaluation

Learn:

- Precision
- Recall
- F1
- ROC-AUC
- PR-AUC
- Log loss
- Calibration
- MAE
- MSE
- RMSE
- Ranking metrics
- Cross-validation
- Threshold selection
- Error analysis
- Subgroup analysis
- A/B testing

### ML tools

Use:

- NumPy
- Polars or pandas
- scikit-learn
- XGBoost, LightGBM, or CatBoost
- Optuna
- MLflow

### Predictive ML project

Business problem:

A support organization needs to predict which cases will breach service-level agreements.

Build:

- Data validation
- Feature pipeline
- Simple baseline
- Linear baseline
- Tree-based models
- Gradient-boosted model
- Cross-validation
- Calibration
- Explainability
- Batch inference
- Online inference
- Drift monitoring
- Retraining pipeline
- Canary release

## Deep learning and complete ML engineering

### Neural-network foundations

Learn:

- Tensors
- Layers
- Activation functions
- Forward propagation
- Backpropagation
- Loss functions
- Optimizers
- Initialization
- Normalization
- Dropout
- Gradient clipping
- Learning-rate schedules

### PyTorch

Learn:

- Tensor operations
- Autograd
- Dataset and DataLoader
- Model modules
- Training loops
- Validation loops
- Checkpoints
- GPU use
- Mixed precision
- Distributed fundamentals
- Profiling

### Important architectures

Learn:

- Feed-forward networks
- Convolutional networks
- Recurrent models at an awareness level
- Attention
- Transformers
- Vision transformers
- Embedding models
- Multimodal architectures at an operational level

### Production ML pipelines

Learn:

- Feature pipelines
- Training pipelines
- Hyperparameter optimization
- Model registries
- Batch inference
- Online inference
- Shadow deployment
- Canary deployment
- Monitoring
- Drift
- Retraining

### Deep-learning project

Business problem:

A marketplace needs automated classification and semantic matching for product listings.

Build:

- Dataset pipeline
- Baseline model
- Embedding model
- Fine-tuned transformer
- Evaluation slices
- Batch pipeline
- Online service
- Monitoring
- Cost and latency comparison

## Role specialization tracks

### Applied AI Engineer

Complete deeply:

- Engineering foundations
- Applied AI product engineering
- LLM applications
- Retrieval and RAG
- Evaluation
- Tool use and controlled agents
- Model-adaptation decision making
- Production system engineering
- Cloud deployment
- Security and privacy
- LLMOps fundamentals
- Classical ML fundamentals

Supporting skills:

- TypeScript and React
- MCP
- Multimodal APIs
- Stakeholder discovery
- Business metrics

Portfolio emphasis:

- End-to-end business workflow
- User-facing product
- Integration with enterprise systems
- Evaluation and feedback
- Deployment and measurable value

### Generative AI Engineer

Complete deeply:

- LLM behavior
- Hosted and open models
- Prompt and context engineering
- RAG
- Agents
- Multimodal applications
- Evaluations
- Safety
- Cost and latency
- Production deployment

Complete practically:

- SFT
- LoRA
- QLoRA
- DPO fundamentals
- vLLM serving

### LLM Engineer

Complete deeply:

- PyTorch
- Tokenizers
- Training data
- SFT
- LoRA and QLoRA
- Preference optimization
- Evaluation
- Distributed training
- Quantization
- Serving
- Performance analysis

Add:

- Continued pretraining
- Distillation
- Reward models
- RL-based post-training according to job requirements

### Model Training Engineer

Complete deeply:

- Data pipelines at scale
- PyTorch distributed
- FSDP or DeepSpeed
- Mixed precision
- Checkpointing
- Cluster scheduling
- Training observability
- Failure recovery
- GPU utilization
- Data mixtures
- Evaluation

Add when required:

- Tensor parallelism
- Pipeline parallelism
- Custom kernels
- JAX

### Post-Training Engineer

Complete deeply:

- Instruction data
- Preference data
- SFT
- DPO
- Reward modelling
- RLHF methods
- Verifiable rewards
- Safety and capability evaluations
- Data flywheels
- Human review operations

This track is more specialized and often expects strong ML fundamentals.

### Machine Learning Engineer

Complete deeply:

- Classical ML
- Deep learning
- Data and feature pipelines
- Training systems
- Serving
- Monitoring
- Drift and retraining
- Cloud and MLOps
- ML system design

Add Applied AI and LLM capability because many current ML roles now include foundation-model systems.

### Data Scientist for ML

Complete deeply:

- SQL
- Statistics
- Experimentation
- Business metrics
- Feature engineering
- Classical ML
- Causal reasoning fundamentals
- Visualization
- Stakeholder communication

Add:

- Foundation-model prototyping
- Text analytics
- Evaluation

### Applied Scientist

Complete deeply:

- Mathematics
- Statistics
- Classical ML
- Deep learning
- Experimental design
- Literature implementation
- Ablations
- Advanced domain modelling
- Production collaboration

This role commonly requires a graduate degree or equivalent evidence of advanced work.

### MLOps Engineer

Complete deeply:

- Docker
- Kubernetes
- Cloud
- CI/CD
- Workflow orchestration
- Experiment tracking
- Registries
- Data and model versioning
- Deployment strategies
- Monitoring
- Security
- Infrastructure as code

### ML Platform Engineer

Complete deeply:

- Distributed systems
- Platform APIs
- Kubernetes
- Workflow engines
- Training job scheduling
- Feature and data platforms
- Model serving
- Multi-tenancy
- Identity
- Observability
- Developer experience

### AI Infrastructure Engineer

Complete deeply:

- Linux
- Networking
- Containers
- Kubernetes
- GPU architecture
- CUDA awareness or depth
- NCCL
- Distributed training
- Distributed inference
- Storage
- Scheduling
- Reliability

### AI Inference Engineer

Complete deeply:

- C++ and Python
- GPU profiling
- KV cache
- Batching
- Quantization
- vLLM or SGLang internals
- TensorRT-LLM
- Triton
- Distributed inference
- Capacity planning
- Benchmarking

### AI Data Engineer

Complete deeply:

- SQL
- Python
- Spark
- Kafka
- Airflow or Dagster
- Data warehouses
- Data validation
- Lineage
- Training-data formats
- Dataset versioning
- Privacy

### AI Evaluation Engineer

Complete deeply:

- Evaluation design
- Golden datasets
- Human evaluation
- Model judges
- Statistical analysis
- Agent evaluation
- Safety evaluation
- Production feedback
- Regression infrastructure

Add domain expertise for the evaluated workflow.

### AI Safety Engineer

Complete deeply:

- Safety taxonomies
- Adversarial testing
- Red teaming
- Evaluation datasets
- Model behavior analysis
- Monitoring
- Incident response
- Alignment methods at an appropriate depth

### AI Security Engineer

Complete deeply:

- Application security
- Identity and authorization
- Prompt injection
- Agent and tool security
- Data protection
- Sandboxing
- Cloud security
- Supply-chain security
- Threat modelling
- Security testing

### Search and Ranking Engineer

Complete deeply:

- Information retrieval
- BM25
- Embeddings
- Approximate nearest neighbours
- Reranking
- Learning to rank
- Query understanding
- Search evaluation
- Online experimentation
- Low-latency systems

### Recommender Systems Engineer

Complete deeply:

- Candidate generation
- Collaborative filtering
- Content-based methods
- Embeddings
- Ranking
- Exploration and exploitation
- Feedback bias
- Offline evaluation
- A/B testing
- Feature pipelines
- Low-latency serving

### NLP Engineer

Complete deeply:

- Text preprocessing
- Classification
- Information extraction
- Named entities
- Embeddings
- Transformers
- Retrieval
- Fine-tuning
- Multilingual evaluation
- LLM integration

### Computer Vision Engineer

Complete deeply:

- Image and video pipelines
- Classification
- Detection
- Segmentation
- Tracking when needed
- Vision transformers
- Data augmentation
- Labelling
- Model optimization
- Edge or cloud serving

### Speech and Audio Engineer

Complete deeply:

- Audio fundamentals
- Speech recognition
- Speech synthesis
- Diarization
- Voice activity detection
- Streaming
- Real-time systems
- Speech evaluation
- Privacy and consent

### Multimodal AI Engineer

Complete deeply:

- Vision-language models
- Audio-language models
- Document models
- Multimodal data
- Multimodal retrieval
- Evaluation
- Streaming and serving

### Robotics and Autonomy Engineer

Complete deeply:

- C++
- Python
- ROS
- Computer vision
- Sensor fusion
- Localization and mapping
- Planning
- Control
- Simulation
- Real-time systems
- Safety

### Edge AI Engineer

Complete deeply:

- Model compression
- Quantization
- ONNX
- TensorRT
- Core ML or mobile runtimes
- Hardware constraints
- Power and memory profiling
- Offline behavior
- Device security

### Forward-Deployed AI Engineer

Complete deeply:

- Applied AI core
- Rapid prototyping
- Enterprise integrations
- Data discovery
- Cloud deployment
- Security
- Workflow redesign
- User training
- Stakeholder communication
- Reusable implementation patterns

This is not a less-technical role. It combines engineering with customer-facing delivery and requires strong judgment under incomplete requirements.

### AI Solutions Architect

Complete deeply:

- Enterprise architecture
- Cloud AI services
- Security and identity
- Data architecture
- Integration patterns
- Build-versus-buy decisions
- Cost modelling
- Governance
- Technical communication

### AI Product Manager

Complete deeply:

- AI capability and limitation
- User discovery
- Workflow design
- Metrics
- Evaluation
- Human oversight
- Safety and governance
- Experimentation
- Business cases

Coding depth is lower, but the role must understand how AI quality is measured and how production failures occur.

### AI Governance Specialist

Complete deeply:

- AI inventory
- Risk classification
- Impact assessment
- Documentation
- Vendor review
- Audit
- Incident management
- NIST and ISO frameworks
- Applicable regulation
- Cross-functional governance

## Project portfolio sequence

Build these projects in this order:

- Production backend for support workflows
- LLM-powered support assistant
- Enterprise RAG platform
- AI evaluation platform
- Controlled tool-using support agent
- LoRA, QLoRA, and DPO model-adaptation pipeline
- Multimodal document and voice operations system
- AI security and safety gateway
- Production multi-provider AI platform
- LLMOps training and deployment platform
- Optimized open-model inference service
- Traditional production ML prediction system

Select at least one specialist project:

- Search and ranking system
- Recommender system
- Computer vision quality-inspection system
- Speech and voice assistant
- Fraud or anomaly detection system
- Edge AI application
- Robotics perception component

## Capstone: enterprise customer-operations AI platform

### Business problem

A company wants to reduce support handling time, improve answer consistency, and automate low-risk operations while preserving privacy, authorization, auditability, and human control.

### Required capabilities

- Customer and employee authentication
- Role-based access
- Ticket ingestion
- Document ingestion
- Hybrid search and reranking
- Evidence-backed responses
- Structured extraction
- Tool use
- Human approval for consequential actions
- Prompt and model versioning
- Evaluation datasets
- LoRA or QLoRA adapter
- Preference optimization experiment
- Multi-provider model routing
- Open-model serving
- Cost controls
- Security controls
- Logs, metrics, and traces
- Canary deployment
- Feedback collection
- Incident handling

### Required engineering artifacts

- Product requirements
- Architecture decision records
- Threat model
- Data model
- API specification
- Evaluation plan
- Training-data card
- Model or adapter card
- System card
- Runbooks
- Cost model
- Load-test report
- Failure-injection report
- Demo and technical presentation

### Success measures

- Task completion
- Answer correctness
- Citation accuracy
- Policy compliance
- Human acceptance
- Reduced handling time
- Safe-action rate
- Latency
- Availability
- Cost per resolved case

## Interview preparation

### Coding

Prepare:

- Python
- Arrays and strings
- Hash maps and sets
- Stacks and queues
- Trees and graphs
- Heaps
- Sorting and searching
- Basic dynamic programming
- Complexity
- Async and concurrency
- Testing

### SQL

Prepare:

- Joins
- Aggregation
- CTEs
- Window functions
- Query debugging
- Indexes
- Data modelling

### Applied AI

Be able to explain:

- Whether AI is appropriate
- Prompting versus RAG versus fine-tuning
- Workflow versus agent
- Hosted versus open models
- Quality, latency, cost, and privacy tradeoffs
- Human approval boundaries
- Business success metrics

### LLM and RAG

Be able to explain:

- Tokenization and attention
- Embeddings
- Chunking
- Hybrid retrieval
- Reranking
- Evaluation
- Hallucination
- Context limitations
- Prompt injection
- Failure attribution

### Training

Be able to explain:

- SFT
- LoRA
- QLoRA
- DPO
- Dataset design
- Learning rate
- Batch size
- Gradient accumulation
- Checkpoints
- Overfitting
- Distributed training fundamentals
- Evaluation before and after adaptation

### Production system design

Practice designing:

- Enterprise RAG
- Customer-support agent
- Recommendation system
- Search system
- Fraud detection
- Model gateway
- Training platform
- Inference platform
- Evaluation platform

Discuss:

- Requirements
- Data
- Models
- Evaluation
- APIs
- Storage
- Scalability
- Reliability
- Security
- Monitoring
- Cost
- Rollback

### Project deep dive

For every portfolio project, answer:

- What business problem did it solve?
- Why was AI required?
- What baseline did you use?
- How did you create the evaluation dataset?
- Why did you select the model and architecture?
- What failed?
- How did you prevent leakage?
- How did you secure data and tools?
- How did you deploy it?
- How did you monitor it?
- What were the latency and cost?
- What would you change at larger scale?

### Behavioral and delivery interviews

Prepare examples covering:

- Ambiguous requirements
- Disagreement over technical direction
- Failed experiment
- Production incident
- Security concern
- Cost reduction
- Working with domain experts
- Explaining limitations
- Prioritizing user value

## Job-readiness gates

### Ready for junior Applied AI or Generative AI roles

Demonstrate:

- Strong Python
- Backend APIs
- SQL
- Hosted model integration
- Structured outputs
- RAG
- Basic tool calling
- Evaluation
- Docker
- One deployed project
- Security fundamentals

### Ready for Applied AI Engineer roles

Demonstrate:

- End-to-end product ownership
- Business problem selection
- Production RAG and agents
- Evaluation and feedback loops
- Cloud deployment
- Reliability
- Security
- Cost measurement
- Stakeholder communication
- At least one model-adaptation project

### Ready for LLM Engineer roles

Demonstrate:

- PyTorch
- Training data
- SFT
- LoRA and QLoRA
- DPO
- Distributed-training fundamentals
- Open-model serving
- Quality and performance evaluation

### Ready for MLOps or platform roles

Demonstrate:

- Cloud
- Docker
- Kubernetes
- CI/CD
- Registries
- Workflow orchestration
- Monitoring
- Infrastructure as code
- Multi-tenant platform design

### Ready for AI evaluation or safety roles

Demonstrate:

- Evaluation dataset design
- Human and model-based evaluation
- Statistical analysis
- Adversarial testing
- Safety and security tests
- Production regression systems
- Incident analysis

### Ready for Machine Learning Engineer roles

Demonstrate:

- Classical ML
- Deep learning
- Data and feature pipelines
- Training
- Deployment
- Monitoring
- Drift
- Retraining
- ML system design

## Topics deliberately deprioritized

Do not prioritize these unless a target job explicitly requires them:

- Training a frontier model from scratch
- Reimplementing every neural architecture from papers
- Mathematical proofs unrelated to engineering decisions
- Exotic PEFT algorithms before LoRA and QLoRA
- Custom CUDA kernels before mastering serving and profiling
- Multi-agent simulations without a real need
- Novel reinforcement-learning algorithms
- GANs outside relevant image roles
- Robotics outside autonomy roles
- Every cloud provider
- Every vector database
- Every agent framework
- Benchmark chasing without a business evaluation

## Maintenance policy

Review this curriculum every six months because model APIs, agent protocols, inference engines, cloud products, and job titles change rapidly.

Keep stable concepts:

- Software engineering
- Data quality
- Evaluation
- Security
- Reliability
- Cost
- Product judgment
- Model and system tradeoffs

Replace tools when the industry changes, but do not remove the underlying competency.

## Primary references and standards

- Stanford HAI, 2026 AI Index Report: https://hai.stanford.edu/ai-index/2026-ai-index-report
- World Economic Forum, Future of Jobs Report 2025: https://www.weforum.org/publications/the-future-of-jobs-report-2025/
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- NIST Generative AI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- OWASP Generative AI Security Project: https://genai.owasp.org/
- Model Context Protocol specification: https://modelcontextprotocol.io/specification/
- OpenTelemetry Generative AI semantic conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- PyTorch documentation: https://docs.pytorch.org/
- Hugging Face Transformers: https://huggingface.co/docs/transformers/
- Hugging Face Datasets: https://huggingface.co/docs/datasets/
- Hugging Face PEFT: https://huggingface.co/docs/peft/
- Hugging Face TRL: https://huggingface.co/docs/trl/
- Hugging Face Accelerate: https://huggingface.co/docs/accelerate/
- vLLM documentation: https://docs.vllm.ai/
- MLflow documentation: https://mlflow.org/docs/latest/

## Final recommendation

Begin with the Applied AI core and present yourself as:

> Applied AI Engineer focused on Generative AI, RAG, agents, model adaptation, evaluation, and production systems.

Then choose one primary specialization:

- LLM training and post-training
- MLOps and ML platform
- AI evaluation, safety, and security
- Machine learning engineering
- Search and recommendation
- Multimodal, vision, or speech
- AI infrastructure and inference
- Forward-deployed enterprise AI

The objective is not to collect frameworks. The objective is to prove that you can identify a valuable problem, select the correct AI approach, build it, evaluate it, deploy it, secure it, monitor it, and improve it using real user and production feedback.
