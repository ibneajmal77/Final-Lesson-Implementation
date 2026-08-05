# Atlas AI Platform - Visual Architecture Diagrams

## 1. Purpose

This document gives architecture reviewers the visual view of Atlas. The master blueprint explains the system in text; this file shows how the parts connect.

All diagrams use Mermaid so they can be rendered by Markdown tools that support Mermaid and can be edited as the architecture changes.

## 2. C4 Context Diagram

```mermaid
flowchart LR
  User[Support Agent / Analyst / Admin]
  Engineer[AI Engineer]
  Reviewer[Compliance Reviewer]
  Atlas[Atlas AI Platform]
  LLM[Managed LLM Providers]
  Media[Media Generation Providers]
  Storage[Object Storage]
  External[CRM / Ticketing / Email / MCP Servers]
  Observability[Logs / Metrics / Traces]

  User --> Atlas
  Engineer --> Atlas
  Reviewer --> Atlas
  Atlas --> LLM
  Atlas --> Media
  Atlas --> Storage
  Atlas --> External
  Atlas --> Observability
```

Key idea:

```text
Users and engineers interact only with Atlas. Atlas controls provider calls, external tools, safety, evaluation, audit, and permissions.
```

## 3. C4 Container Diagram

```mermaid
flowchart TB
  Web[Web Console]
  API[FastAPI API Service]
  Worker[Worker Service]
  Eval[Eval Runner]
  Gateway[Model Gateway]
  Prompt[Prompt Service]
  Ingestion[Document Ingestion]
  Retrieval[Retrieval Service]
  RAG[RAG Service]
  Agents[Agent Orchestrator]
  Tools[Tool Service]
  MCP[MCP Adapter]
  Safety[Safety Service]
  MediaGen[Media Generation Service]
  Voice[Voice Service]
  Gov[Governance Service]
  DB[(PostgreSQL)]
  Vector[(pgvector / Qdrant)]
  Redis[(Redis)]
  Objects[(Object Storage)]
  OTel[OpenTelemetry Collector]
  Providers[LLM / Embedding / Media Providers]
  External[External Business Systems]

  Web --> API
  API --> Prompt
  API --> Gateway
  API --> RAG
  API --> Agents
  API --> Tools
  API --> Safety
  API --> Gov
  API --> DB
  API --> Redis
  Worker --> Ingestion
  Worker --> Retrieval
  Worker --> Eval
  Worker --> MediaGen
  Worker --> Voice
  Ingestion --> Objects
  Ingestion --> DB
  Retrieval --> Vector
  Retrieval --> Gateway
  RAG --> Retrieval
  RAG --> Prompt
  RAG --> Gateway
  RAG --> Safety
  Agents --> RAG
  Agents --> Tools
  Agents --> Safety
  Tools --> MCP
  MCP --> External
  Tools --> External
  Gateway --> Providers
  MediaGen --> Gateway
  Voice --> Gateway
  Gov --> DB
  API --> OTel
  Worker --> OTel
  Gateway --> OTel
```

## 4. Module Boundary Diagram

```mermaid
flowchart LR
  subgraph Apps
    api[apps/api]
    worker[apps/worker]
    web[apps/web]
    evalrunner[apps/eval_runner]
  end

  subgraph Packages
    core[core]
    db[db]
    auth[auth]
    gateway[model_gateway]
    prompts[prompts]
    ingestion[ingestion]
    retrieval[retrieval]
    rag[rag]
    agents[agents]
    tools[tools]
    memory[memory]
    safety[safety]
    evals[evals]
    media[media_generation]
    voice[voice]
    gov[governance]
    obs[observability]
  end

  api --> core
  api --> auth
  api --> db
  api --> gateway
  api --> rag
  api --> agents
  api --> tools
  api --> safety
  api --> evals
  api --> media
  api --> gov
  worker --> ingestion
  worker --> retrieval
  worker --> evals
  worker --> media
  worker --> voice
  gateway --> obs
  rag --> retrieval
  agents --> tools
  agents --> memory
  tools --> safety
  gov --> evals
```

Boundary rule:

```text
Application entry points call packages. Packages do not import route files. All model calls go through model_gateway.
```

## 5. ERD Overview

```mermaid
erDiagram
  TENANTS ||--o{ TENANT_MEMBERSHIPS : has
  USERS ||--o{ TENANT_MEMBERSHIPS : joins
  ROLES ||--o{ TENANT_MEMBERSHIPS : grants
  ROLES ||--o{ ROLE_PERMISSIONS : includes
  PERMISSIONS ||--o{ ROLE_PERMISSIONS : maps

  TENANTS ||--o{ KNOWLEDGE_COLLECTIONS : owns
  KNOWLEDGE_COLLECTIONS ||--o{ DOCUMENTS : groups
  DOCUMENTS ||--o{ DOCUMENT_VERSIONS : versions
  DOCUMENT_VERSIONS ||--o{ DOCUMENT_PAGES : pages
  DOCUMENT_VERSIONS ||--o{ DOCUMENT_CHUNKS : chunks
  DOCUMENT_CHUNKS ||--o{ CHUNK_EMBEDDINGS : embeds

  TENANTS ||--o{ CONVERSATIONS : owns
  CONVERSATIONS ||--o{ CONVERSATION_MESSAGES : contains
  CONVERSATIONS ||--o{ RAG_QUERIES : asks
  RAG_QUERIES ||--o{ RAG_RETRIEVAL_RESULTS : retrieves
  RAG_QUERIES ||--o{ RAG_ANSWERS : answers
  RAG_ANSWERS ||--o{ ANSWER_CITATIONS : cites
  DOCUMENT_CHUNKS ||--o{ ANSWER_CITATIONS : supports

  PROMPT_TEMPLATES ||--o{ PROMPT_VERSIONS : versions
  PROMPT_VERSIONS ||--o{ AI_RUNS : used_by
  MODEL_PROVIDERS ||--o{ MODEL_ROUTES : provides
  MODEL_ROUTES ||--o{ AI_RUNS : routes

  AGENT_DEFINITIONS ||--o{ AGENT_RUNS : runs
  AGENT_RUNS ||--o{ AGENT_STEPS : traces
  TOOL_DEFINITIONS ||--o{ TOOL_CALLS : called_as
  AGENT_RUNS ||--o{ TOOL_CALLS : uses
  TOOL_CALLS ||--o{ HUMAN_APPROVALS : may_require

  EVAL_DATASETS ||--o{ EVAL_CASES : contains
  EVAL_DATASETS ||--o{ EVAL_RUNS : runs
  EVAL_RUNS ||--o{ EVAL_RESULTS : scores
  EVAL_CASES ||--o{ EVAL_RESULTS : evaluated_by

  MCP_SERVERS ||--o{ MCP_TOOL_MAPPINGS : exposes
  TOOL_DEFINITIONS ||--o{ MCP_TOOL_MAPPINGS : maps

  MEDIA_GENERATION_JOBS ||--o{ MEDIA_ASSETS : creates
  MEDIA_ASSETS ||--o{ MEDIA_SAFETY_CHECKS : checked_by

  SYSTEM_CARDS ||--o{ GOVERNANCE_REVIEWS : reviewed_by
  MODEL_CARDS ||--o{ GOVERNANCE_REVIEWS : reviewed_by
  RISK_REGISTER_ITEMS ||--o{ GOVERNANCE_REVIEWS : reviewed_by
```

## 6. RAG Sequence Diagram

```mermaid
sequenceDiagram
  participant U as User
  participant W as Web Console
  participant A as API
  participant S as Safety Service
  participant R as RAG Service
  participant V as Retrieval Service
  participant G as Model Gateway
  participant P as Prompt Service
  participant DB as PostgreSQL
  participant VS as Vector DB

  U->>W: Ask document question
  W->>A: POST /api/v1/rag/query
  A->>A: Auth, tenant, permission checks
  A->>S: Check user input
  S-->>A: allow or block
  A->>R: run_rag_query
  R->>P: load query rewrite prompt
  R->>G: optional query rewrite
  R->>V: retrieve candidates
  V->>G: embed query
  G-->>V: query embedding
  V->>VS: vector or hybrid search with tenant ACL
  VS-->>V: candidate chunks
  V->>G: optional rerank
  G-->>V: reranked chunks
  V-->>R: retrieval result
  R->>P: render RAG answer prompt
  R->>G: generate answer
  G-->>R: answer + usage
  R->>S: output and citation checks
  S-->>R: safety decision
  R->>DB: store rag_query, retrieval results, ai_run, answer, citations
  R-->>A: answer with citations
  A-->>W: response
  W-->>U: Display answer and evidence
```

## 7. Document Ingestion Sequence Diagram

```mermaid
sequenceDiagram
  participant U as User
  participant API as API
  participant OBJ as Object Storage
  participant DB as PostgreSQL
  participant Q as Redis Queue
  participant Worker as Worker
  participant Gateway as Model Gateway
  participant Vector as Vector DB

  U->>API: Upload document
  API->>API: Validate type, size, tenant, idempotency
  API->>OBJ: Store original file
  API->>DB: Create document/version records
  API->>Q: Queue ingestion job
  API-->>U: document_id + job_id
  Worker->>Q: Dequeue ingestion job
  Worker->>OBJ: Read file
  Worker->>Worker: Extract text / OCR / clean
  Worker->>DB: Store pages and chunks
  Worker->>Gateway: Create embeddings in batches
  Gateway-->>Worker: Embeddings
  Worker->>Vector: Upsert vectors with tenant filters
  Worker->>DB: Mark processed, store lineage
```

## 8. Agent Flow Diagram

```mermaid
flowchart TD
  Task[User task] --> Auth[Auth and tenant checks]
  Auth --> Risk[Safety risk score]
  Risk --> Plan[Structured plan]
  Plan --> Validate[Plan validation]
  Validate --> Step[Execute next step]
  Step --> NeedRAG{Need retrieval?}
  NeedRAG -- yes --> RAG[Run RAG]
  NeedRAG -- no --> NeedTool{Need tool?}
  RAG --> NeedTool
  NeedTool -- yes --> ToolCheck[Validate tool schema and permission]
  ToolCheck --> Risky{Risky write?}
  Risky -- yes --> Approval[Human approval]
  Approval --> ToolExec[Execute tool]
  Risky -- no --> ToolExec
  NeedTool -- no --> Verify[Verify progress]
  ToolExec --> Verify
  Verify --> Done{Done?}
  Done -- no --> Limits{Limits exceeded?}
  Limits -- no --> Step
  Limits -- yes --> Blocked[Blocked / failed]
  Done -- yes --> Final[Final response]
  Final --> Trace[Store trace, cost, eval hooks]
```

## 9. MCP Tool Call Sequence Diagram

```mermaid
sequenceDiagram
  participant Agent as Agent Orchestrator
  participant Tool as Tool Service
  participant Safety as Safety Service
  participant MCP as MCP Adapter
  participant Server as Registered MCP Server
  participant Audit as Audit Log

  Agent->>Tool: request tool call
  Tool->>Tool: validate Atlas tool schema
  Tool->>Tool: check user/agent/tenant permissions
  Tool->>Safety: check tool risk and arguments
  Safety-->>Tool: allow / approval_required / block
  Tool->>MCP: call mapped MCP tool
  MCP->>Server: tools/call with protocol metadata
  Server-->>MCP: structured result or input_required
  MCP-->>Tool: normalized result
  Tool->>Safety: sanitize result before model context
  Tool->>Audit: record call, result, trace ids
  Tool-->>Agent: safe tool result
```

## 10. Evaluation Flow Diagram

```mermaid
flowchart LR
  Dataset[Eval Dataset] --> Runner[Eval Runner]
  Candidate[Candidate Config] --> Runner
  Baseline[Baseline Config] --> Runner
  Runner --> Cases[Run Cases]
  Cases --> Scorers[Scorers]
  Scorers --> Judge[LLM Judge Optional]
  Scorers --> Metrics[Metrics]
  Metrics --> Compare[Baseline vs Candidate]
  Compare --> Threshold{Thresholds met?}
  Threshold -- yes --> Review[Human review]
  Review --> Promote[Promote prompt/model/retriever]
  Threshold -- no --> Reject[Reject or revise]
  Reject --> Dataset
```

## 11. Deployment Diagram

```mermaid
flowchart TB
  subgraph Client
    Browser[Browser]
  end

  subgraph Edge
    CDN[CDN / Static Hosting]
    LB[Load Balancer / API Gateway]
  end

  subgraph AppCluster
    Web[Web App]
    API1[API Instance 1]
    API2[API Instance 2]
    Worker1[Worker Pool]
    Eval[Eval Runner]
    ModelServer[Optional Model Server GPU]
  end

  subgraph Data
    PG[(Managed PostgreSQL)]
    Redis[(Managed Redis)]
    Vector[(Vector DB)]
    Obj[(Object Storage)]
  end

  subgraph Observability
    OTel[OpenTelemetry Collector]
    Metrics[Metrics Store]
    Logs[Log Store]
    Alerts[Alerting]
  end

  subgraph Providers
    LLM[LLM Providers]
    Media[Media Providers]
    MCP[MCP Servers]
  end

  Browser --> CDN
  Browser --> LB
  CDN --> Web
  LB --> API1
  LB --> API2
  API1 --> PG
  API2 --> PG
  API1 --> Redis
  API2 --> Redis
  Worker1 --> Redis
  Worker1 --> PG
  Worker1 --> Vector
  Worker1 --> Obj
  API1 --> LLM
  API2 --> LLM
  Worker1 --> Media
  API1 --> MCP
  API2 --> MCP
  API1 --> OTel
  API2 --> OTel
  Worker1 --> OTel
  OTel --> Metrics
  OTel --> Logs
  Metrics --> Alerts
```

## 12. MVP Spine Diagram

```mermaid
flowchart LR
  A[Phase 00 Foundation] --> B[Phase 01 LLM Gateway]
  B --> C[Phase 02 Prompt System]
  C --> D[Phase 03 Structured Outputs]
  D --> E[Phase 04 Document Ingestion]
  E --> F[Phase 05 Embeddings]
  F --> G[Phase 06 RAG]
  G --> H[Phase 07 Evaluation]
  H --> I[Phase 18 Light Deployment]
  I --> J[Phase 19 Portfolio Demo]
```

Scope rule:

```text
Do not add Phase 26 before the MVP spine has working code, tests, evals, and a demo.
```
