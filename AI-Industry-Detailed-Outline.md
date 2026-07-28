# Detailed AI Industry Learning Outline

Updated: July 28, 2026

## Purpose

- Compact outline for practical AI careers
- Focused on employment, interviews, business applications, and production systems
- Begins with Applied AI and Generative AI
- Includes model training, MLOps, safety, and Machine Learning Engineering
- Excludes research-only material unless required by a specialist role

### Python and .NET implementation policy

- Python remains the primary reference for model, data, evaluation, and training work
- The parallel .NET lane covers model APIs, RAG, controlled agents and memory, MCP, production architecture, observability, and the capstone
- C# implementations preserve the Python reference's contracts, evaluation data, authorization rules, telemetry, budgets, and failure cases
- Provider and framework code stays behind application-owned interfaces
- Supported package versions are pinned; preview-only behavior is not a core dependency
- The selected backend supplies runnable code, automated tests, redacted traces, measured quality-latency-cost results, and design-decision evidence
- One full capstone backend is sufficient; learners do not duplicate the complete product in both languages

## Primary career target

- Applied AI Engineer
  - Business-problem discovery
  - AI solution selection
  - Generative AI applications
  - Retrieval-augmented generation
  - Tool-using workflows and agents
  - Model adaptation
  - Evaluation
  - Production deployment
  - Security and governance
  - Business-outcome measurement

## Related AI roles

- Generative AI Engineer
- LLM Engineer
- Machine Learning Engineer
- Model Training Engineer
- Post-Training Engineer
- Data Scientist for ML
- Applied Scientist
- MLOps Engineer
- ML Platform Engineer
- AI Infrastructure Engineer
- AI Inference Engineer
- AI Data Engineer
- AI Data and Annotation Engineer
- AI Evaluation Engineer
- AI Safety Engineer
- AI Security Engineer
- NLP Engineer
- Computer Vision Engineer
- Speech and Audio Engineer
- Multimodal AI Engineer
- Search and Ranking Engineer
- Recommender Systems Engineer
- Robotics and Autonomy Engineer
- Edge AI Engineer
- Forward-Deployed AI Engineer
- AI Solutions Architect
- AI Product Manager
- AI Governance Specialist
- AI UX and Conversation Designer

## Recommended learning sequence

- Engineering foundations
- Applied AI product engineering
- Foundation-model and LLM engineering
- Embeddings, retrieval, and RAG
- Evaluation and feedback engineering
- AI data engineering
- Tool calling, agent workflows, and MCP
- Model adaptation and post-training
- Multimodal, document, speech, and voice AI
- AI safety, security, privacy, and governance
- Production AI system engineering
- Cloud and infrastructure
- LLMOps and MLOps
- Open-model serving and inference optimization
- Classical machine learning
- Deep learning and complete ML engineering
- Selected role specialization
- Portfolio, interviews, and job preparation

## Standard structure for every lesson

- Business purpose
- Definitions
- Industry use cases
- Architecture
- Data flow
- Minimal implementation
- Tool-based implementation
- Configuration
- Testing
- Evaluation
- Edge cases
- Failure modes
- Debugging
- Security
- Privacy
- Performance
- Latency
- Cost
- Observability
- Alternatives and tradeoffs
- Interview questions
- Practical assignment
- Production-readiness checklist

## Standard structure for every project

- Business problem
- Target users
- Current workflow
- Baseline
- Functional requirements
- Non-functional requirements
- Architecture diagram
- Data contracts
- API contracts
- Model-selection decision
- Evaluation dataset
- Acceptance thresholds
- Automated tests
- Threat model
- Privacy controls
- Docker environment
- CI pipeline
- Deployment
- Logs, metrics, and traces
- Performance measurements
- Cost measurements
- Failure-recovery plan
- Technical documentation
- Business-outcome report

## Core industry tool stack

### Programming

- Python
- C# for the parallel .NET Applied AI lane
- SQL
- TypeScript fundamentals
- JavaScript fundamentals
- Bash or PowerShell fundamentals

### Python engineering

- uv
- Pydantic
- pytest
- Ruff
- mypy or Pyright
- HTTPX
- Jupyter

### Backend development

- FastAPI
- OpenAPI
- JSON Schema
- SQLAlchemy or SQLModel
- Alembic
- WebSockets
- Server-sent events

### Parallel .NET Applied AI stack

- .NET SDK and C#
- ASP.NET Core
- OpenAPI and JSON Schema-compatible contracts
- `System.Text.Json`
- Supported provider SDK or supported `Microsoft.Extensions.AI` abstraction
- Application-owned model, retrieval, tool, memory, and policy interfaces
- xUnit, NUnit, or an equivalent supported test framework
- OpenTelemetry for .NET
- Optional supported Semantic Kernel packages only after manual workflow implementation
- Established .NET MCP SDK selected against required protocol, identity, and security capabilities

### Data storage

- PostgreSQL
- Redis
- Parquet
- Object storage
- pgvector
- OpenSearch or Elasticsearch

### AI model integration

- Native model-provider SDKs
- Hosted foundation-model APIs
- Hugging Face Transformers
- Hugging Face Datasets
- sentence-transformers

### Model training

- PyTorch
- Transformers
- Datasets
- PEFT
- TRL
- Accelerate
- bitsandbytes
- FSDP
- DeepSpeed

### Model serving

- vLLM
- SGLang
- llama.cpp
- ONNX Runtime
- TensorRT-LLM
- Triton Inference Server

### Agent and workflow development

- Native tool-calling APIs
- Explicit state machines
- LangGraph
- Provider agents SDK
- Semantic Kernel
- LlamaIndex
- Model Context Protocol

### Experiment and lifecycle management

- MLflow
- DVC
- Weights & Biases awareness
- Model registries
- Prompt registries
- Dataset registries

### Data engineering

- Polars or pandas
- Apache Spark
- Kafka
- Airflow or Dagster
- dbt
- Databricks
- Snowflake or BigQuery

### Infrastructure

- Git
- GitHub
- Docker
- Docker Compose
- Kubernetes
- Helm
- Terraform
- GitHub Actions
- Argo CD
- Argo Workflows
- Kubeflow
- KServe
- Ray

### Observability

- OpenTelemetry
- Prometheus
- Grafana
- Cloud-native logging and monitoring
- LangSmith, Phoenix, or equivalent AI tracing platform

### Cloud

- AWS
  - Bedrock
  - SageMaker
  - ECS or EKS
  - Lambda
  - S3
  - RDS
  - ElastiCache
  - SQS
  - CloudWatch
- Azure
  - Azure AI Foundry
  - Azure Machine Learning
  - AKS
  - Functions
  - Blob Storage
  - Azure Database for PostgreSQL
  - Azure Cache for Redis
  - Service Bus
  - Azure Monitor
- Google Cloud
  - Vertex AI
  - GKE
  - Cloud Run
  - Cloud Storage
  - Cloud SQL
  - Memorystore
  - Pub/Sub
  - Cloud Monitoring

## Engineering foundations

### Python language

- Variables and data types
- Lists, dictionaries, tuples, and sets
- Control flow
- Functions
- Comprehensions
- Modules
- Packages
- Classes
- Dataclasses
- Composition
- Interfaces
- Type hints
- Protocols
- Generics
- Exceptions
- Context managers
- Decorators
- Iterators
- Generators

### Concurrent Python

- Async and await
- Event loops
- Async HTTP
- Threads
- Processes
- Queues
- Cancellation
- Timeouts
- Resource cleanup

### Production Python

- Application configuration
- Environment variables
- Secret handling
- Structured logging
- Error classification
- Dependency injection
- Package management
- Dependency locking
- Reproducible environments
- Profiling
- Debugging

### Testing

- Unit testing
- Integration testing
- End-to-end testing
- Fixtures
- Mocks
- Parameterized tests
- Test coverage
- External API mocking
- Database testing
- Async testing
- Contract testing

### Backend APIs

- HTTP
- REST
- JSON
- OpenAPI
- JSON Schema
- Request validation
- Response validation
- Authentication
- Authorization
- OAuth
- OpenID Connect
- API keys
- Role-based access
- Streaming
- Webhooks
- Background jobs
- Rate limiting
- Idempotency
- Retries
- Exponential backoff
- Circuit breakers
- API versioning

### Databases

- Relational modelling
- Tables and relationships
- Primary and foreign keys
- Joins
- Aggregations
- Common table expressions
- Window functions
- Transactions
- Isolation
- Indexes
- Query plans
- Connection pooling
- Schema migrations
- JSON columns
- Row-level security

### Development workflow

- Git commits
- Branches
- Pull requests
- Code review
- Merge conflicts
- Release tags
- Semantic versioning
- Pre-commit hooks
- CI pipelines
- Dependency scanning
- Secret scanning

### Foundation project

- Production support-ticket backend
  - FastAPI
  - PostgreSQL
  - Redis
  - Authentication
  - Role-based authorization
  - Tests
  - Docker Compose
  - CI
  - Logs
  - API documentation

## Applied AI product engineering

### Business discovery

- User identification
- Workflow observation
- Pain-point discovery
- Time and cost baseline
- Error-rate baseline
- Repetitive-work identification
- Decision-support opportunities
- Automation opportunities
- Human-approval requirements
- Domain constraints
- Regulatory constraints

### Problem formulation

- User task
- Input
- Output
- Success criteria
- Failure criteria
- Allowed behavior
- Prohibited behavior
- Quality threshold
- Latency target
- Availability target
- Cost target
- Escalation path

### Solution selection

- Deterministic software
- Rules
- Search
- Classical machine learning
- Foundation-model API
- Open model
- RAG
- Tool calling
- Controlled agent workflow
- Fine-tuning
- Multimodal model
- Human operation
- Hybrid solution

### Product decisions

- Build versus buy
- Hosted versus self-hosted
- Model-provider selection
- Privacy requirements
- Regional deployment
- Vendor lock-in
- Time to market
- Total cost of ownership
- Maintenance ownership

### AI user experience

- Streaming output
- Editable drafts
- Source display
- Confidence communication
- Abstention
- Human confirmation
- Feedback controls
- Error explanations
- Accessibility
- Trust calibration
- Avoiding automation bias

### Business metrics

- Adoption
- Task completion
- Acceptance rate
- Edit rate
- Escalation rate
- Resolution time
- Error reduction
- Cost per task
- Revenue impact
- User satisfaction

### Applied AI discovery project

- Support-operations workflow analysis
- Current-state workflow map
- Candidate use cases
- Build-versus-buy report
- Proposed system architecture
- Evaluation plan
- Risk register
- Expected return on investment

## Foundation-model and LLM engineering

### Language-model concepts

- Tokens
- Vocabulary
- Tokenization
- Embeddings
- Logits
- Probabilities
- Autoregressive generation
- Context windows
- Attention
- Transformer blocks
- Positional information
- Feed-forward layers
- Residual connections
- Normalization

### Model types

- Encoder models
- Decoder models
- Encoder-decoder models
- Dense models
- Mixture-of-experts models
- Reasoning models
- Multimodal models
- Hosted models
- Open-weight models

### Model lifecycle

- Pretraining
- Continued pretraining
- Instruction tuning
- Supervised fine-tuning
- Preference optimization
- Distillation
- Quantization
- Inference

### Generation configuration

- Temperature
- Top-p
- Top-k
- Maximum tokens
- Stop sequences
- Repetition controls
- Deterministic output
- Sampled output
- Structured generation

### Model selection

- Task quality
- Reasoning quality
- Tool-use reliability
- Schema compliance
- Context capacity
- Multimodal support
- Latency
- Throughput
- Cost
- Data policy
- Regional support
- Fine-tuning support
- Rate limits

### Model APIs

- API authentication
- Message formats
- Response formats
- Streaming
- Structured outputs
- Tool calling
- Image input
- Audio input
- Document input
- Conversation state
- Token accounting
- Rate-limit handling
- Retries
- Timeouts
- Fallback models
- Request tracing
- Cost attribution

### Parallel .NET model-API lab

- Authenticated ASP.NET Core endpoints for synchronous and server-sent-event responses
- Application-owned provider interface with two replaceable adapters
- Typed structured-output validation before domain use
- Cancellation and deadline propagation through streamed model calls
- Safe retry, circuit-breaker, and observable fallback behavior
- Correlated model, token, latency, tenant, version, and cost telemetry with content redaction
- Shared valid, invalid-schema, rate-limit, timeout, cancellation, and fallback fixtures
- Acceptance evidence: API contract, automated test report, redacted trace, and quality-latency-cost comparison

### Prompt and context engineering

- Instruction hierarchy
- Task definition
- Output contracts
- Few-shot examples
- Prompt templates
- Delimiters
- Untrusted context
- Context selection
- Context compression
- Prompt versioning
- Prompt testing
- Multilingual prompting
- Injection awareness

### LLM application project

- AI support-ticket assistant
  - Classification
  - Structured extraction
  - Urgency recommendation
  - Response drafting
  - Streaming
  - Human approval
  - Conversation persistence
  - Retry and fallback
  - Token and cost tracking
  - Prompt registry
  - Regression tests

## Embeddings, retrieval, and RAG

### Embeddings

- Embedding models
- Vector dimensions
- Normalization
- Cosine similarity
- Dot product
- Euclidean distance
- Domain-specific embeddings
- Multilingual embeddings
- Multimodal embeddings

### Information retrieval

- Inverted indexes
- Lexical retrieval
- BM25
- Dense retrieval
- Hybrid retrieval
- Approximate nearest neighbours
- Metadata filters
- Query expansion
- Query rewriting
- Reranking
- Cross-encoders

### Document ingestion

- PDF parsing
- HTML parsing
- Email parsing
- Office document parsing
- OCR
- Scanned documents
- Tables
- Images
- Captions
- Cleaning
- Normalization
- Language detection
- Deduplication
- Metadata enrichment
- Document versioning
- Incremental indexing
- Delete propagation
- Permission metadata

### Chunking

- Fixed-token chunks
- Structure-aware chunks
- Semantic chunks
- Parent-child chunks
- Sentence windows
- Table-aware chunks
- Code-aware chunks
- Chunk overlap
- Chunk-size evaluation

### RAG pipeline

- Content ingestion
- Embedding generation
- Indexing
- Query classification
- Query rewriting
- Query decomposition
- Retrieval
- Reranking
- Context construction
- Answer generation
- Citations
- Abstention
- Feedback collection

### Production RAG

- Conversational retrieval
- Multi-query retrieval
- Multi-stage retrieval
- Hierarchical retrieval
- Structured-data retrieval
- SQL retrieval
- Graph-enhanced retrieval
- Federated retrieval
- Multimodal retrieval
- Knowledge freshness
- Caching
- Tenant isolation
- Permission-aware retrieval

### Classic-versus-agentic retrieval lab

- Classic hybrid retrieval remains the default baseline
- A measured query classifier selects agentic retrieval only for complex or multi-part questions
- Retrieval is exposed through approved tools with authorization on every derived query and result
- Query planning produces a bounded number of focused subqueries
- Independent subqueries run in parallel under concurrency, latency, token, step, and spending limits
- Evidence is merged, deduplicated, reranked, cited, and checked before generation
- Explicit stopping and classic-fallback behavior handles sufficient evidence, planner failure, partial retrieval, or exhausted budgets
- One versioned evaluation set compares retrieval quality, answer correctness, groundedness, citation accuracy, latency, tokens, and cost
- Failure tests cover decomposition explosion, loops, repeated queries, retriever outage, permission changes, timeouts, citation mismatch, and adversarial input

### Parallel .NET RAG lab

- ASP.NET Core query service with application-owned planner and retrieval interfaces
- Bounded asynchronous concurrency and cancellation propagation
- Compatible vector or search client selected by product requirements
- Shared evaluation, authorization, citation, budget, trace, and fallback fixtures
- Acceptance evidence: classic-versus-agentic report, budget-limit tests, redacted trace, and a decision stating when the extra latency and cost are justified

### RAG metrics

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

### RAG tools

- pgvector
- OpenSearch or Elasticsearch
- FAISS
- sentence-transformers
- Cross-encoder rerankers
- Managed vector databases when justified

### Enterprise RAG project

- Internal knowledge assistant
  - Multi-format ingestion
  - OCR
  - Table extraction
  - Hybrid retrieval
  - Selective bounded agentic retrieval
  - Reranking
  - Citations
  - Role-based access
  - Incremental updates
  - Delete handling
  - Evaluation
  - User feedback
  - Injection controls
  - Monitoring

## Evaluation and feedback engineering

### Evaluation requirements

- User-task definition
- Expected behavior
- Prohibited behavior
- Evaluation slices
- Boundary cases
- Negative cases
- Adversarial cases
- Quality gates
- Business metrics

### Evaluation datasets

- Golden datasets
- Representative sampling
- Difficult examples
- Production samples
- Synthetic cases
- Versioning
- Contamination checks
- Annotation guidelines
- Inter-annotator agreement
- Privacy review

### Deterministic evaluation

- Exact match
- Schema validation
- Regex validation
- Citation verification
- Tool-argument validation
- Database-state validation
- Task-completion checks
- Unit tests

### Model-based evaluation

- Pointwise judging
- Pairwise judging
- Rubric-based judging
- Reference-based judging
- Reference-free judging
- Multi-judge evaluation
- Judge calibration
- Position bias
- Verbosity bias
- Human auditing

### Human evaluation

- Review interface
- Rubrics
- Blind comparison
- Sampling
- Escalation
- Reviewer quality control
- Agreement measurement

### Online evaluation

- Explicit feedback
- Implicit feedback
- Acceptance rate
- Edit rate
- Completion rate
- Escalation rate
- A/B testing
- Canary analysis
- Incident analysis

### Agent evaluation

- Task completion
- Tool selection
- Argument correctness
- Invalid actions
- Policy compliance
- Step count
- Recovery
- Human intervention
- Latency
- Cost

### Evaluation tools

- pytest
- MLflow
- Custom evaluation code
- OpenTelemetry
- Ragas
- DeepEval
- promptfoo
- LangSmith
- Phoenix
- Weights & Biases

### Evaluation platform project

- Versioned test datasets
- Deterministic tests
- Model judges
- Human-review queue
- Retrieval metrics
- Agent metrics
- Safety tests
- Cost report
- Latency report
- Experiment comparison
- CI quality gates
- Regression dashboard

## AI data engineering

### Data governance

- Acquisition
- Consent
- Licensing
- Provenance
- Ownership
- Retention
- Deletion
- Access controls
- Audit trails

### Data processing

- Schema definition
- Validation
- Cleaning
- Normalization
- Deduplication
- PII detection
- Redaction
- Quality filtering
- Dataset splitting
- Leakage prevention
- Versioning
- Lineage

### Training-data formats

- Raw text
- Domain corpora
- Instruction-response pairs
- Multi-turn conversations
- Tool trajectories
- Preference pairs
- Ranking data
- Reward-model data
- Image-text pairs
- Audio-text pairs
- Evaluation cases
- Safety cases

### Data creation

- Human annotation
- Expert annotation
- Synthetic data
- Rejection sampling
- Data augmentation
- Weak supervision
- Active learning
- Difficult-example mining
- Production-feedback loops

### Data-quality metrics

- Correctness
- Relevance
- Coverage
- Diversity
- Duplication
- Safety
- Privacy
- Formatting
- Label consistency
- Distribution drift

### Data tools

- Python
- SQL
- Polars or pandas
- Hugging Face Datasets
- Parquet
- DVC
- Spark
- Kafka
- Airflow or Dagster
- dbt
- Databricks
- Labelling platforms

### Training-data project

- Source registry
- Data contracts
- Validation
- PII redaction
- Deduplication
- Quality scoring
- Dataset splits
- Leakage checks
- Versioning
- Dataset card
- Approval workflow

## Tool use, agents, and MCP

### Tool calling

- Tool definitions
- JSON Schema
- Argument validation
- Tool selection
- Sequential calls
- Parallel calls
- Result normalization
- Read operations
- Write operations
- Idempotency
- Retries
- Timeouts
- Error handling
- Permissions
- Audit logging

### Workflow architecture

- State machines
- Workflow graphs
- Routing
- Planning
- Execution
- Durable state
- Checkpointing
- Human approval
- Compensating actions
- Step limits
- Time limits
- Spending limits
- Escalation

### Memory

- Request context
- Session state
- Durable workflow state
- User preferences
- Retrieval-backed memory
- Summarized memory
- Typed separation between workflow checkpoints and user memory
- Allowlist-based memory write policy
- Consent and purpose limitation
- Subject, tenant, source, provenance, classification, and version
- Expiration
- User correction
- User deletion
- Derived-summary, index, and cache invalidation
- Privacy
- Poisoning and stale-memory resistance
- Relevance, consistency, isolation, correction, and verified-forgetting evaluation

### Governed memory acceptance evidence

- Memory schema and write-policy decision table
- Tests for missing consent, duplicate writes, poisoning, expiration, revoked access, cross-tenant access, correction, deletion, and summary drift
- Documented retention and deletion objective
- Evaluation report for relevance, factual consistency, stale-memory handling, and verified forgetting

### Model Context Protocol

- MCP architecture
- Client
- Server
- Tools
- Resources
- Prompts
- Transport
- Capability negotiation
- Authentication
- Authorization
- Server trust
- Tool discovery
- Permission boundaries
- Logging
- Security risks

### Agent interoperability

- Workflow handoffs
- Agent-to-agent concepts
- Identity propagation
- Shared-context risks
- Cross-agent authorization
- Multi-agent selection criteria

### Reusable versioned capabilities or skills

- Capability name, semantic version, owner, and compatibility range
- Input and output schema
- Allowed data and declared purpose
- Required identity, permissions, and resource limits
- Pinning, allowlisting, review, and upgrade tests
- No assumption that one vendor-specific skill-file convention is universal
- Deliberate mapping to MCP tools, resources, or prompts
- No implicit transfer of user or server authority
- Compatibility, authorization, injection, cancellation, and audit fixtures

### Sandboxed computer and coding-agent lab

- Disposable test repository and restricted execution environment
- One read-only inspection and one proposed source patch
- Filesystem path, process, network, credential, CPU, memory, output, time, and step restrictions
- Host credentials, privileged processes, unrestricted paths, and network denied by default
- Exact diff and command plan presented before any side effect
- Named human authorization before a write or command execution
- Repository content, screenshots, tool descriptions, and output treated as untrusted
- Capability version, requester, authorization, proposal, approval, execution, and artifact audit trail
- No autonomous destructive or production remediation actions

### Parallel .NET agent and MCP labs

- ASP.NET Core controlled workflow with typed memory policy, authorization, idempotency, approval, and recovery
- Workflow checkpoints persisted separately from user-profile memory
- Authenticated .NET MCP server for one read-only versioned capability
- Allowlisted client with user and tenant identity propagation
- Shared approval, isolation, expiration, correction, deletion, discovery, schema, injection, version-mismatch, cancellation, and audit fixtures
- Acceptance evidence: memory schema, policy table, capability manifest, MCP mapping, compatibility tests, sandbox policy, proposed diff, approval record, and trace

### Agent tools

- Native provider tool calling
- Explicit workflow code
- LangGraph
- Provider agents SDK
- Semantic Kernel
- LlamaIndex
- MCP SDKs

### Agent project

- Support-resolution agent
  - RAG
  - Customer lookup
  - Order lookup
  - Refund proposal
  - Human approval
  - Ticket update
  - Persistent state
  - Governed memory with consent, provenance, expiration, correction, and deletion
  - Retry logic
  - Compensation logic
  - Permission model
  - Audit trail
  - MCP tool
  - Versioned capability and explicit MCP mapping
  - Restricted computer or coding-agent exercise in a disposable sandbox
  - Task evaluation

## Model adaptation and post-training

### Adaptation options

- Prompt improvement
- Context improvement
- RAG
- Tool calling
- Supervised fine-tuning
- LoRA
- QLoRA
- Full fine-tuning
- Continued pretraining
- Preference optimization
- Knowledge distillation

### Training fundamentals

- GPU memory
- Parameters
- Activations
- Gradients
- Optimizer state
- Forward pass
- Loss
- Backpropagation
- Batch size
- Gradient accumulation
- Learning rate
- Schedulers
- Epochs
- Steps
- Validation
- Checkpoints
- Early stopping
- Overfitting
- Gradient clipping
- Gradient checkpointing

### Numerical formats

- FP32
- FP16
- BF16
- FP8 awareness
- INT8
- INT4
- Numerical stability
- Training precision
- Inference quantization

### Tokenization for training

- Tokenizer configuration
- Vocabulary
- Special tokens
- Chat templates
- Padding
- Truncation
- Attention masks
- Label masks
- Sequence length
- Sequence packing
- Completion-only loss
- Data collators

### Supervised fine-tuning

- Base model selection
- Instruct model selection
- SFT use cases
- Dataset formatting
- Training configuration
- Loss monitoring
- Validation
- Checkpoint selection
- Behavior regression
- Safety regression

### LoRA

- Parameter-efficient fine-tuning
- Low-rank adapters
- Rank
- Scaling
- Target modules
- Adapter dropout
- Trainable parameters
- Adapter checkpoints
- Adapter loading
- Adapter merging
- Multiple adapters
- Adapter routing
- Adapter serving

### QLoRA

- Quantized base models
- Four-bit loading
- NF4
- Double quantization awareness
- Compute data type
- Paged optimizer awareness
- Gradient checkpointing
- Memory-quality tradeoffs
- Checkpointing
- Merging constraints

### Preference optimization

- Preference-data design
- Chosen responses
- Rejected responses
- Preference rubrics
- Human preferences
- AI-generated preferences
- Quality control
- Bias
- Leakage
- DPO
- Policy model
- Reference model
- Preference overfitting
- Safety evaluation

### Advanced post-training

- Reward models
- RLHF
- PPO awareness
- GRPO
- RLOO
- Verifiable rewards
- Process rewards
- Outcome rewards

### Continued pretraining

- Domain corpus
- Data mixture
- Causal language modelling
- Learning rate
- Catastrophic forgetting
- Domain evaluation
- Infrastructure cost

### Distillation

- Teacher model
- Student model
- Synthetic targets
- Response distillation
- Logit-distillation awareness
- Quality-cost tradeoffs

### Distributed training

- Data parallelism
- DistributedDataParallel
- FSDP
- DeepSpeed ZeRO
- Tensor-parallel awareness
- Pipeline-parallel awareness
- Mixed precision
- Distributed checkpointing
- NCCL fundamentals
- Failure recovery
- Utilization
- Cost tracking

### Training tools

- PyTorch
- Transformers
- Datasets
- PEFT
- TRL
- Accelerate
- bitsandbytes
- FSDP
- DeepSpeed
- MLflow
- DVC

### Model-adaptation project

- Business-policy support model
  - Prompt baseline
  - RAG baseline
  - Instruction dataset
  - SFT
  - LoRA
  - QLoRA
  - Preference dataset
  - DPO
  - Adapter registry
  - Evaluation
  - Safety regression
  - Serving endpoint
  - Cost and performance comparison

## Multimodal, document, speech, and voice AI

### Multimodal foundations

- Image inputs
- Audio inputs
- Video inputs
- Document inputs
- Cross-modal context
- Modality preprocessing
- Structured extraction
- Multimodal evaluation

### Document intelligence

- OCR
- Layout analysis
- Table extraction
- Form understanding
- Key-value extraction
- Document classification
- Page-level citations
- Confidence thresholds
- Human review

### Speech and audio

- Speech-to-text
- Text-to-speech
- Voice activity detection
- Speaker diarization
- Noise handling
- Streaming audio
- Turn detection
- Interruptions
- Real-time latency
- Voice privacy

### Voice agents

- Real-time transport
- Audio buffering
- Turn management
- Tool calls
- Conversation state
- Human escalation
- Recording policy
- Disclosure
- Safety

### Computer vision

- Image preprocessing
- Classification
- Object detection
- Segmentation
- Tracking
- OCR
- Vision transformers
- Data augmentation
- Labelling
- Vision metrics
- Batch inference
- Edge inference

### Multimodal project

- Insurance claim operations assistant
  - Document classification
  - OCR
  - Structured extraction
  - Image understanding
  - Speech transcription
  - Evidence-linked summary
  - Missing-information detection
  - Human review
  - Confidence routing
  - Audit trail
  - Evaluation

## AI safety, security, privacy, and governance

### AI threats

- Direct prompt injection
- Indirect prompt injection
- Jailbreaking
- Sensitive-data disclosure
- Improper output handling
- Excessive agency
- Tool abuse
- System-prompt leakage
- Retrieval poisoning
- Training-data poisoning
- Model extraction
- Membership inference awareness
- Denial of service
- Supply-chain attacks

### Identity and authorization

- User identity
- Service identity
- Agent identity
- OAuth scopes
- Least privilege
- Tool permissions
- Tenant isolation
- Row-level security
- Document-level security
- Approval workflows
- Credential rotation

### Secure execution

- Sandboxing
- Network restrictions
- Filesystem restrictions
- Command allowlists
- Resource limits
- Time limits
- Secret isolation
- Output validation
- Browser isolation
- Computer-use isolation

### Privacy

- PII
- Sensitive data
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

- Harm taxonomies
- Misuse cases
- Refusal quality
- Over-refusal
- Bias
- Subgroup evaluation
- Hallucination
- Manipulation
- Adversarial testing
- Red teaming

### Governance

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

### Standards

- NIST AI Risk Management Framework
- NIST Generative AI Profile
- OWASP Generative AI guidance
- Model Context Protocol security guidance
- OpenTelemetry Generative AI semantic conventions
- ISO/IEC 42001
- ISO/IEC 23894
- EU AI Act
- Sector-specific regulations

### Safety project

- Enterprise AI safety gateway
  - Threat model
  - Adversarial tests
  - Prompt-injection tests
  - PII redaction
  - Policy checks
  - Tool-permission service
  - Human approval
  - Rate limits
  - Spending limits
  - Audit logs
  - Regression pipeline
  - Incident dashboard

## Production AI system engineering

### System components

- API gateway
- Model gateway
- Retrieval service
- Tool service
- Evaluation service
- Queue
- Worker
- Scheduler
- Object storage
- Relational database
- Cache
- Event stream
- Identity service
- Policy service

### Architecture evolution and decision exercise

- Start with explicit model, retrieval, tool, evaluation, and policy modules inside a deployable modular monolith
- Use event-driven workers for justified asynchronous or long-running work with defined delivery, replay, cancellation, and idempotency semantics
- Extract independently deployed services only when scaling, isolation, ownership, compliance, or release evidence justifies the operational cost
- Write one ADR comparing a modular monolith, event-driven workers, and microservices for the same workload
- Evaluate team ownership, deployment coupling, latency, data consistency, scaling, failure isolation, security, operability, and cost
- Record context, constraints, measured evidence, decision, rejected options, consequences, migration triggers, and reversal plan
- Diagram request, event, data-ownership, failure, and identity-propagation flows

### Parallel .NET production-architecture lab

- ASP.NET Core API with explicit application modules
- One justified long-running operation moved through a durable queue to a hosted or background worker
- Correlation, cancellation, idempotency, tenant identity, and authorization preserved across the boundary
- Separately deployed service added only if selected by the ADR
- Acceptance evidence: ADR, diagrams, benchmark, operating-cost estimate, failure-injection and replay report, migration triggers, and recovery test

### Reliability

- Service-level indicators
- Service-level objectives
- Health checks
- Readiness checks
- Retries
- Backoff
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

- Response caching
- Prefix caching
- Retrieval caching
- Embedding caching
- Semantic caching
- Cache invalidation
- Permission-aware caching

### Background processing

- Job queues
- Scheduled jobs
- Long-running tasks
- Workflow orchestration
- Cancellation
- Progress reporting
- Retry safety

### Observability

- Structured logs
- Metrics
- Distributed traces
- Prompt traces
- Model versions
- Prompt versions
- Retrieval traces
- Tool traces
- Token use
- Latency
- Cost
- Cache hit rate
- User feedback
- Safety events
- RED for request-driven services: request rate, errors, and duration
- USE for resources: utilization, saturation, and errors
- Four golden signals: latency, traffic, errors, and saturation
- Deployment and configuration change events
- Alert owners, thresholds, runbook links, and test fixtures

### Optional AIOps project: IncidentPilot

- Controlled, redacted logs, metrics, traces, alerts, deployment events, and configuration events
- Deterministic correlation and anomaly baseline before AI assistance
- Ranked root-cause hypotheses with cited evidence, confidence, contradictions, and unknowns
- Draft incident timeline, impact, diagnostic steps, and proposed versioned runbook
- Named human approval of the exact runbook step before any permitted test execution
- Execution disabled by default and no autonomous remediation
- Audit of inputs, model and prompt version, evidence, hypotheses, approvals, execution, and artifacts
- Evaluation with known incidents, misleading correlations, missing telemetry, prompt injection in logs, repeated alerts, false positives, and provider failure

### Parallel .NET observability lab

- OpenTelemetry instrumentation for ASP.NET Core, outbound model calls, retrieval, MCP, tools, memory, database, queue, and workers
- Compatible RED, USE, golden-signal, AI-quality, safety, and cost telemetry
- One end-to-end incident trace and one telemetry-redaction test
- Acceptance evidence: dashboard exports, alert tests, queries and thresholds, incident fixtures, hypothesis-scoring report, redaction result, and immutable approval/audit example

### Cost engineering

- Cost per request
- Cost per successful task
- Token budgets
- Context reduction
- Model routing
- Smaller-model fallback
- Batch processing
- Caching
- GPU utilization
- Capacity planning

### Production platform project

- Multi-provider AI gateway
  - Authentication
  - Request limits
  - Spending limits
  - Model routing
  - Structured outputs
  - Tool calling
  - Prompt registry
  - Evaluation hooks
  - Tracing
  - Usage attribution
  - Caching
  - Provider fallback
  - Safety controls
  - Dashboard

## Cloud, containers, and infrastructure

### Docker

- Dockerfiles
- Multi-stage builds
- Non-root containers
- Dependency caching
- Health checks
- Docker Compose
- Image scanning
- Container registries

### Cloud foundations

- Identity and access management
- Virtual networks
- Load balancers
- DNS
- Object storage
- Managed databases
- Secret managers
- Queues
- Container services
- Serverless services
- GPU instances
- Logging
- Monitoring
- Cost allocation

### Infrastructure as code

- Terraform
- Environment separation
- State management
- Modules
- Secret references
- Review workflows
- Deployment workflows

### Kubernetes

- Pods
- Deployments
- Services
- Ingress
- ConfigMaps
- Secrets
- Resource requests
- Resource limits
- Health checks
- Autoscaling
- Jobs
- Scheduled jobs
- Persistent storage
- GPU scheduling
- Rolling deployments
- Failure diagnosis

## LLMOps and MLOps

### Experiment tracking

- Parameters
- Metrics
- Artifacts
- Dataset references
- Prompt versions
- Model versions
- Adapter versions
- Environment versions
- Reproducibility

### Registries

- Dataset registry
- Prompt registry
- Model registry
- Adapter registry
- Evaluation registry
- Approval status
- Lineage

### AI CI/CD

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
- Shadow deployment
- Rollback

### Continuous training

- Trigger conditions
- New-data validation
- Training
- Evaluation gates
- Human approval
- Deployment
- Monitoring
- Rollback

### Monitoring

- Input drift
- Output drift
- Feature drift
- Quality proxies
- Human feedback
- Calibration
- Model errors
- Data-quality failures
- Fairness slices
- Groundedness
- Tool failures
- Citation failures
- Schema failures
- Refusal behavior
- Token usage
- Cost
- Latency

### LLMOps project

- Automated adapter lifecycle
  - Versioned data
  - QLoRA training
  - MLflow tracking
  - Prompt registry
  - Adapter registry
  - Evaluation gates
  - Safety gates
  - Container build
  - Staging deployment
  - Canary release
  - Monitoring
  - Rollback

## Open-model serving and inference optimization

### Model artifacts

- Model configuration
- Tokenizer files
- Safetensors
- Adapter files
- Quantized formats
- Licences
- Checksums
- Provenance

### Serving

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

### Quantization

- Weight-only quantization
- INT8
- INT4
- GPTQ awareness
- AWQ awareness
- GGUF awareness
- Quality evaluation
- Throughput evaluation
- Hardware compatibility

### Distributed inference

- Tensor parallelism
- Pipeline parallelism
- Data-parallel serving
- Expert-parallel awareness
- Multi-node serving
- Network bottlenecks
- Scheduling

### Inference metrics

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

### Inference project

- Private multi-model platform
  - Open base model
  - LoRA adapters
  - vLLM or SGLang
  - Quantization
  - Continuous batching
  - Prefix caching
  - Authentication
  - Routing
  - Autoscaling
  - Load testing
  - Capacity planning
  - Cost report
  - Dashboard

## Classical machine learning

### Mathematics

- Vectors
- Matrices
- Dot products
- Matrix multiplication
- Distances
- Probability distributions
- Conditional probability
- Bayes theorem
- Expectation
- Variance
- Sampling
- Confidence intervals
- Hypothesis testing
- Gradients
- Loss functions
- Regularization
- Optimization

### Problem types

- Classification
- Regression
- Ranking
- Clustering
- Forecasting
- Anomaly detection

### Data preparation

- Exploratory analysis
- Missing values
- Outliers
- Categorical encoding
- Scaling
- Feature engineering
- Feature selection
- Class imbalance
- Dataset splitting
- Time-based splitting
- Leakage prevention

### Core models

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

### Metrics

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

- NumPy
- Polars or pandas
- scikit-learn
- XGBoost
- LightGBM
- CatBoost
- Optuna
- MLflow

### Classical ML project

- Service-level breach predictor
  - Validation
  - Feature pipeline
  - Baselines
  - Tree models
  - Gradient boosting
  - Cross-validation
  - Calibration
  - Explainability
  - Batch inference
  - Online inference
  - Drift monitoring
  - Retraining
  - Canary release

## Deep learning and complete ML engineering

### Neural networks

- Tensors
- Layers
- Activations
- Forward propagation
- Backpropagation
- Losses
- Optimizers
- Initialization
- Normalization
- Dropout
- Gradient clipping
- Learning-rate schedules

### PyTorch

- Tensor operations
- Autograd
- Dataset
- DataLoader
- Model modules
- Training loops
- Validation loops
- Checkpoints
- GPU use
- Mixed precision
- Distributed fundamentals
- Profiling

### Architectures

- Feed-forward networks
- Convolutional networks
- Recurrent models
- Attention
- Transformers
- Vision transformers
- Embedding models
- Multimodal architectures

### ML pipelines

- Feature pipelines
- Training pipelines
- Hyperparameter optimization
- Model registry
- Batch inference
- Online inference
- Shadow deployment
- Canary deployment
- Monitoring
- Drift
- Retraining

### Deep-learning project

- Product classification and semantic matching
  - Dataset pipeline
  - Baseline
  - Embedding model
  - Fine-tuned transformer
  - Evaluation slices
  - Batch inference
  - Online serving
  - Monitoring
  - Cost comparison

## Role-specific learning branches

### Applied AI Engineer

- Production Python
- APIs and SQL
- Product discovery
- LLM APIs
- RAG
- Agents and MCP
- Evaluation
- Model-adaptation decisions
- Cloud deployment
- Security
- LLMOps fundamentals
- Classical ML fundamentals
- TypeScript and React fundamentals

### Generative AI Engineer

- LLM behavior
- Prompt and context engineering
- RAG
- Agents
- Multimodal applications
- Evaluation
- Safety
- Production deployment
- SFT
- LoRA
- QLoRA
- DPO fundamentals
- Open-model serving

### LLM Engineer

- PyTorch
- Tokenizers
- Training data
- SFT
- LoRA
- QLoRA
- Preference optimization
- Distributed training
- Quantization
- Serving
- Performance
- Continued pretraining
- Distillation

### Model Training Engineer

- Large-scale data pipelines
- PyTorch distributed
- FSDP
- DeepSpeed
- Mixed precision
- Checkpointing
- Cluster scheduling
- Training observability
- GPU utilization
- Data mixtures
- Failure recovery

### Post-Training Engineer

- Instruction data
- Preference data
- SFT
- DPO
- Reward modelling
- RLHF
- GRPO or related methods
- Verifiable rewards
- Safety evaluations
- Capability evaluations
- Data flywheels

### Machine Learning Engineer

- Classical ML
- Deep learning
- Feature pipelines
- Training pipelines
- Serving
- Monitoring
- Drift
- Retraining
- Cloud
- MLOps
- ML system design
- Applied LLM systems

### Data Scientist for ML

- SQL
- Statistics
- Experimentation
- Business metrics
- Feature engineering
- Classical ML
- Causal reasoning
- Visualization
- Communication
- Foundation-model prototyping

### Applied Scientist

- Mathematics
- Statistics
- Classical ML
- Deep learning
- Experimental design
- Paper implementation
- Ablation studies
- Domain modelling
- Production collaboration

### MLOps Engineer

- Docker
- Kubernetes
- Cloud
- CI/CD
- Orchestration
- Experiment tracking
- Registries
- Data versioning
- Model versioning
- Deployment strategies
- Monitoring
- Terraform

### ML Platform Engineer

- Distributed systems
- Platform APIs
- Kubernetes
- Workflow engines
- Job scheduling
- Feature platforms
- Model serving
- Multi-tenancy
- Identity
- Observability
- Developer experience

### AI Infrastructure Engineer

- Linux
- Networking
- Containers
- Kubernetes
- GPUs
- CUDA awareness
- NCCL
- Distributed training
- Distributed inference
- Storage
- Scheduling
- Reliability

### AI Inference Engineer

- C++
- Python
- GPU profiling
- KV cache
- Batching
- Quantization
- vLLM
- SGLang
- TensorRT-LLM
- Triton
- Distributed inference
- Capacity planning

### AI Data Engineer

- Python
- SQL
- Spark
- Kafka
- Airflow or Dagster
- Data warehouses
- Validation
- Lineage
- Training-data formats
- Dataset versioning
- Privacy

### AI Evaluation Engineer

- Evaluation design
- Golden datasets
- Human evaluation
- Model judges
- Statistics
- Agent evaluation
- Safety evaluation
- Production feedback
- Regression infrastructure

### AI Safety Engineer

- Safety taxonomies
- Adversarial tests
- Red teaming
- Evaluation datasets
- Model behavior
- Monitoring
- Incident response
- Alignment methods

### AI Security Engineer

- Application security
- Identity
- Authorization
- Prompt injection
- Agent security
- Tool security
- Data protection
- Sandboxing
- Cloud security
- Supply-chain security
- Threat modelling

### Search and Ranking Engineer

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

- Candidate generation
- Collaborative filtering
- Content-based recommendation
- Embeddings
- Ranking
- Exploration and exploitation
- Feedback bias
- Offline evaluation
- A/B testing
- Low-latency serving

### NLP Engineer

- Text processing
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

- Image pipelines
- Video pipelines
- Classification
- Detection
- Segmentation
- Tracking
- Vision transformers
- Augmentation
- Labelling
- Optimization
- Serving

### Speech and Audio Engineer

- Audio fundamentals
- Speech recognition
- Speech synthesis
- Diarization
- Voice activity detection
- Streaming
- Real-time systems
- Evaluation
- Privacy

### Multimodal AI Engineer

- Vision-language models
- Audio-language models
- Document models
- Multimodal datasets
- Multimodal retrieval
- Evaluation
- Streaming
- Serving

### Robotics and Autonomy Engineer

- C++
- Python
- ROS
- Computer vision
- Sensor fusion
- Localization
- Mapping
- Planning
- Control
- Simulation
- Real-time systems
- Safety

### Edge AI Engineer

- Compression
- Quantization
- ONNX
- TensorRT
- Mobile runtimes
- Embedded runtimes
- Hardware constraints
- Power profiling
- Memory profiling
- Device security

### Forward-Deployed AI Engineer

- Applied AI core
- Rapid prototyping
- Enterprise integration
- Data discovery
- Cloud deployment
- Security
- Workflow redesign
- User training
- Stakeholder communication
- Reusable solutions

### AI Solutions Architect

- Enterprise architecture
- Cloud AI services
- Security
- Identity
- Data architecture
- Integration patterns
- Build-versus-buy decisions
- Cost modelling
- Governance
- Technical communication

### AI Product Manager

- AI capabilities
- AI limitations
- User discovery
- Workflow design
- Metrics
- Evaluation
- Human oversight
- Safety
- Governance
- Experimentation
- Business cases

### AI Governance Specialist

- AI inventory
- Risk classification
- Impact assessment
- Documentation
- Vendor review
- Audit
- Incident management
- NIST
- ISO
- Regulation

## Portfolio sequence

- Production support-workflow backend
- LLM support assistant
- Enterprise RAG platform
- AI evaluation platform
- Training-data pipeline
- Controlled tool-using agent
- LoRA, QLoRA, and DPO pipeline
- Multimodal operations assistant
- AI security gateway
- Multi-provider AI platform
- LLMOps deployment platform
- Open-model inference platform
- Classical ML prediction system
- One specialist project

## Specialist project options

- Search and ranking system
- Recommendation system
- Computer-vision quality inspection
- Speech and voice assistant
- Fraud detection
- Anomaly detection
- Forecasting system
- Edge AI application
- Robotics perception component
- Multimodal document workflow

## Capstone

### Enterprise customer-operations AI platform

- Authentication
- Role-based access
- Ticket ingestion
- Document ingestion
- Hybrid retrieval
- Classic-versus-agentic retrieval routing with enforced limits
- Reranking
- Evidence-backed responses
- Structured extraction
- Tool calling
- MCP integration
- Human approval
- Governed memory with consent, provenance, expiration, correction, and deletion
- Versioned reusable capabilities with explicit MCP mappings and permissions
- Prompt versioning
- Model versioning
- Evaluation datasets
- LoRA or QLoRA adapter
- Preference-optimization experiment
- Multi-provider routing
- Open-model serving
- Cost controls
- Security controls
- Logs
- Metrics
- Traces
- RED, USE, and four-golden-signal dashboards
- Canary deployment
- User feedback
- Incident handling

### Capstone artifacts

- Product requirements
- Architecture diagram
- Architecture decisions
- Topology ADR comparing a modular monolith, event-driven workers, and microservices
- Threat model
- Data model
- API specification
- Evaluation plan
- Dataset card
- Model or adapter card
- System card
- Runbooks
- Cost model
- Load-test report
- Failure-injection report
- Classic-versus-agentic RAG quality-latency-cost report
- Memory governance and verified-deletion report
- Capability manifest, MCP mapping, and sandbox-policy evidence
- Business-outcome report

### Parallel .NET capstone variant

- Python remains the reference path; a learner targeting .NET roles may implement the production backend in C# and ASP.NET Core
- Supported provider integrations remain behind application-owned interfaces for structured output, streaming, RAG, tools, and fallback
- Authenticated MCP consumption or serving, governed memory, queued work, and OpenTelemetry are required
- The same schemas, evaluation set, permission model, safety controls, quality thresholds, latency and cost budgets, and failure fixtures apply
- The selected backend must prove agentic-retrieval bounds, correction and deletion propagation, capability authorization, sandboxing where executable, and auditable human approval
- Acceptance evidence includes reproducible build, automated tests, container configuration, API contract, redacted trace, topology ADR, dashboards, failure report, and runbooks
- A second full capstone implementation is not required; only shared contract and benchmark slices are compared

## Interview outline

### Python and coding

- Arrays
- Strings
- Hash maps
- Sets
- Stacks
- Queues
- Trees
- Graphs
- Heaps
- Sorting
- Searching
- Basic dynamic programming
- Complexity
- Async
- Concurrency
- Testing

### SQL

- Joins
- Aggregations
- CTEs
- Window functions
- Query debugging
- Indexes
- Data modelling

### Applied AI

- AI suitability
- Problem formulation
- Baselines
- Prompting versus RAG
- RAG versus fine-tuning
- Workflow versus agent
- Hosted versus open models
- Quality-latency-cost tradeoffs
- Privacy
- Human approval
- Business metrics

### LLM and RAG

- Tokenization
- Attention
- Embeddings
- Chunking
- Hybrid retrieval
- Reranking
- Hallucination
- Evaluation
- Context limits
- Prompt injection
- Failure attribution

### Training

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
- Distributed training
- Before-and-after evaluation

### ML

- Model selection
- Bias and variance
- Leakage
- Cross-validation
- Metrics
- Calibration
- Feature engineering
- Drift
- A/B testing

### AI system design

- Enterprise RAG
- Support agent
- Search system
- Recommendation system
- Fraud detection
- Model gateway
- Training platform
- Inference platform
- Evaluation platform
- Classic versus bounded agentic RAG
- Governed agent memory
- MCP capability and identity propagation
- Modular monolith versus event-driven workers versus microservices
- AI incident assistance with human-approved runbooks

### Production discussion

- Requirements
- Data
- Model
- Evaluation
- APIs
- Storage
- Scalability
- Reliability
- Security
- Monitoring
- Cost
- Rollback

### .NET Applied AI and AI API design

- Provider-independent model integration in ASP.NET Core
- Structured-output validation and typed contracts
- Server-sent-event streaming, cancellation, timeouts, safe retries, and observable fallback
- Token, context, rate-limit, and cost budgeting
- Embeddings, ingestion, hybrid retrieval, reranking, citations, and agentic-retrieval bounds
- Tool calling, governed memory, MCP identity propagation, authorization, idempotency, and audit
- Prompt-injection defenses across documents, tools, memory, and telemetry
- Evaluation gates, OpenTelemetry traces, RED, USE, and golden signals
- Queue, batch, accelerator, and provider failure modes
- Architecture evolution from modular monolith to workers or services

### Behavioral and delivery

- Ambiguous requirements
- Technical disagreement
- Failed experiment
- Production incident
- Security issue
- Cost reduction
- Domain-expert collaboration
- Communicating limitations
- Prioritizing business value

## Job-readiness gates

### Junior Applied AI or Generative AI

- Python
- APIs
- SQL
- Hosted model integration
- Structured outputs
- RAG
- Basic tools
- Evaluation
- Docker
- Deployed project
- Security fundamentals

### Applied AI Engineer

- End-to-end product ownership
- Business discovery
- Production RAG
- Controlled agents
- Evaluation
- Feedback loops
- Cloud deployment
- Reliability
- Security
- Cost analysis
- Model-adaptation project
- Stakeholder communication

### Parallel .NET Applied AI

- Authenticated ASP.NET Core model API with structured output, streaming, cancellation, retry, and observable fallback
- Production RAG slice with authorization, citations, evaluation, and classic-versus-agentic comparison
- Controlled tool workflow with governed memory
- Authenticated MCP client or server with identity propagation and capability-version controls
- OpenTelemetry traces plus RED, USE, golden-signal, AI-quality, safety, and cost dashboards
- Architecture ADR, containerized deployment, failure tests, security tests, and interview defense

### LLM Engineer

- PyTorch
- Training data
- SFT
- LoRA
- QLoRA
- DPO
- Distributed fundamentals
- Open-model serving
- Quality evaluation
- Performance evaluation

### MLOps or platform

- Cloud
- Docker
- Kubernetes
- CI/CD
- Registries
- Orchestration
- Monitoring
- Infrastructure as code
- Multi-tenancy

### Evaluation, safety, or security

- Evaluation design
- Golden datasets
- Human evaluation
- Model judges
- Statistical analysis
- Adversarial testing
- Security tests
- Regression systems
- Incident analysis

### Machine Learning Engineer

- Classical ML
- Deep learning
- Feature pipelines
- Training
- Deployment
- Monitoring
- Drift
- Retraining
- ML system design

## Topics to deprioritize

- Diffusion and generative image or video engineering unless required by a media-generation specialization
- General reinforcement learning beyond LLM post-training literacy unless required by an RL or autonomy role
- Symbolic and neuro-symbolic AI unless required by a planning, knowledge-representation, or research role
- Frontier-model pretraining from scratch
- Reimplementing every paper
- Unnecessary mathematical proofs
- Exotic PEFT methods before LoRA and QLoRA
- Custom CUDA kernels before serving fundamentals
- Multi-agent systems without a business need
- Novel reinforcement-learning research
- GANs outside relevant image roles
- Robotics outside autonomy roles
- Learning every cloud
- Learning every vector database
- Learning every agent framework
- Benchmark optimization without business evaluation

## Recommended final positioning

> Applied AI Engineer specializing in Generative AI, RAG, agents, model adaptation, evaluation, and production systems.

## Recommended supporting specialization

Choose one:

- LLM training and post-training
- MLOps and ML platform
- AI evaluation, safety, and security
- Machine Learning Engineering
- Search and recommendation
- Multimodal, vision, or speech
- AI infrastructure and inference
- Forward-deployed enterprise AI

## Reference standards

- Stanford AI Index
- World Economic Forum Future of Jobs
- NIST AI Risk Management Framework
- NIST Generative AI Profile
- OWASP Generative AI Security Project
- Model Context Protocol specification
- OpenTelemetry Generative AI semantic conventions
- ISO/IEC 42001
- ISO/IEC 23894
- Applicable AI and privacy regulations
