# SupportOps AI Copilot — Architecture (Complete Reference)

This document is the single, complete technical description of the system. It is written so that a
reader with no prior exposure can finish it with a full mental model of **what runs, how the pieces
connect, what happens on every request, how data is shaped, and how the system is operated**.

Diagrams are written in [Mermaid](https://mermaid.js.org/) (renders on GitHub and most Markdown
viewers) with ASCII fallbacks where useful.

> **What the product does, in one sentence:** a support agent files a customer ticket; the system
> uses an LLM to classify it, extract fields, set priority, and draft a reply; a human approves every
> draft before it is used — and every step is measured, costed, gated, and reversible.

## Table of contents

1. [System context](#1-system-context)
2. [Runtime topology (the 9 services)](#2-runtime-topology-the-9-services)
3. [Codebase architecture (apps & packages)](#3-codebase-architecture-apps--packages)
4. [The dependency rule](#4-the-dependency-rule)
5. [Data model](#5-data-model)
6. [The three analysis paths](#6-the-three-analysis-paths)
7. [Request flows (sequence diagrams)](#7-request-flows-sequence-diagrams)
8. [The model gateway internals](#8-the-model-gateway-internals)
9. [State machines](#9-state-machines)
10. [Evaluation subsystem](#10-evaluation-subsystem)
11. [Observability: logs, metrics, traces, cost](#11-observability-logs-metrics-traces-cost)
12. [Security & multi-tenancy](#12-security--multi-tenancy)
13. [Reliability & failure handling](#13-reliability--failure-handling)
14. [Configuration](#14-configuration)
15. [Deployment, CI/CD & rollback](#15-deployment-cicd--rollback)
16. [Data lifecycle & retention](#16-data-lifecycle--retention)
17. [Naming inconsistencies (read before debugging)](#17-naming-inconsistencies-read-before-debugging)
18. [Glossary](#18-glossary)

---

## 1. System context

Who and what interacts with the system, and where the trust boundary sits.

```mermaid
flowchart TB
    subgraph external[Outside the trust boundary]
        agent[Support agent / lead / admin<br/>uses the web console]
        helpdesk[Upstream helpdesk<br/>Zendesk/Freshdesk sends tickets]
        gateway[API gateway<br/>authenticates & sets identity headers]
        openai[Hosted LLM provider<br/>OpenAI-compatible /responses API]
    end

    subgraph trusted[Inside the trust boundary]
        sys[SupportOps AI Copilot<br/>API + Worker + Web + Data + Monitoring]
    end

    agent --> gateway
    helpdesk --> gateway
    gateway -->|X-Tenant-Id, X-User-Id, X-Role| sys
    sys -->|structured analysis request<br/>store:false| openai
    openai -->|strict JSON analysis| sys
```

**Key context facts**

- **Identity is trusted, not verified.** The service reads `X-Tenant-Id`, `X-User-Id`, `X-Role`
  headers. A real API gateway is expected to authenticate the user and set these honestly. **This
  service must never be exposed directly to the public internet.** (See `docs/threat-model.md`,
  `apps/api/supportops_api/dependencies.py`.)
- **The LLM is the only outbound dependency**, reached solely through `packages/model_gateway`. It is
  called with `store: false` so the provider does not retain customer ticket text.
- **Multi-tenant:** many customer companies ("tenants") share one deployment and one database.

---

## 2. Runtime topology (the 9 services)

`docker-compose.yml` defines nine containers. Four are the application, two are data stores, one is
monitoring collection + visualization, and two are developer-only UIs.

```mermaid
flowchart LR
    browser([Browser]) -->|:3000| web[web / nginx<br/>static console]
    web -->|/api proxy| api

    subgraph app[Application - built from Dockerfile.api, one image, three commands]
        migrate[[migrate<br/>alembic upgrade head<br/>runs once, exits]]
        api[api / FastAPI<br/>:8765]
        worker[worker<br/>RQ consumer<br/>no ports]
    end

    subgraph data[Data stores]
        pg[(postgres:16<br/>volume: postgres_data)]
        redis[(redis:7<br/>volume: redis_data)]
    end

    subgraph mon[Monitoring]
        prom[prometheus<br/>:9090]
        graf[grafana<br/>:3001]
    end

    subgraph dev[Dev-only UIs]
        adminer[postgres-ui / adminer<br/>:8081]
        rediscmd[redis-ui<br/>:8082]
    end

    api --> pg
    api -->|enqueue run_id| redis
    worker -->|dequeue run_id| redis
    worker --> pg
    migrate --> pg
    api -->|/api LLM call| ext([Hosted LLM])
    worker --> ext
    prom -->|scrape /metrics/runtime| api
    graf --> prom
    adminer --> pg
    rediscmd --> redis
```

### Startup ordering (critical)

Containers start in parallel by default, which would break this system. `depends_on` with
conditions enforces a real order:

```
postgres becomes healthy (pg_isready)
   └─> migrate runs alembic upgrade head, exits 0 (service_completed_successfully)
          └─> api starts   (also waits redis healthy) ── healthcheck: GET /health
          └─> worker starts (also waits redis healthy)
                 └─> web starts once api is healthy
                        └─> prometheus starts once api is healthy
                               └─> grafana starts once prometheus started
```

Running migrations as a **separate one-shot job** (not at API startup) means the schema changes
exactly once even when several API replicas start, and a failed migration halts the deploy instead of
leaving the app on a half-updated schema.

### Port map

| Service | Host port | Purpose |
|---|---|---|
| web (console) | 3000 | agent review UI |
| api (FastAPI) | 8765 | REST API + `/docs` OpenAPI |
| adminer | 8081 | browse Postgres (dev) |
| redis-ui | 8082 | browse Redis queue (dev) |
| prometheus | 9090 | metrics store |
| grafana | 3001 | dashboards |

> One image, three commands: `migrate`, `api`, and `worker` are all built from `Dockerfile.api` and
> differ only in their `command`. This guarantees they share identical code and settings.

---

## 3. Codebase architecture (apps & packages)

The repository is a small monorepo split into **runtime apps** and **reusable packages**.

```
apps/
  api/     supportops_api      FastAPI HTTP layer
  worker/  supportops_worker   RQ background consumer + retention routine
  web/     static console (nginx) — index.html, app.js, styles.css
packages/
  domain/         supportops_domain          framework-free business rules (baseline classifier)
  db/             supportops_db              SQLAlchemy models, repositories, Alembic migrations
  model_gateway/  supportops_model_gateway   provider-neutral LLM access (mock + hosted)
  prompts/        supportops_prompts         versioned prompt templates + Pydantic output schemas
  evals/          supportops_evals           datasets, scoring, runner, release gates
  observability/  supportops_observability   logging, metrics, tracing, cost helpers
infra/            prometheus, grafana, staging compose, terraform placeholder
docs/             stage docs, reports, runbooks, threat model, this file
```

### Package responsibility map

```mermaid
flowchart TD
    subgraph apps
      API[apps/api<br/>routes, schemas, settings, dependencies, pilot, checks]
      WORKER[apps/worker<br/>main, jobs, queues, retention]
      WEB[apps/web<br/>static console]
    end

    subgraph packages
      DOMAIN[domain<br/>baseline classifier]
      DB[db<br/>models, repositories, migrations, session]
      MG[model_gateway<br/>routing, providers base/mock/hosted, cost, errors]
      PROMPTS[prompts<br/>registry, schemas, templates]
      EVALS[evals<br/>runner, scoring, reports, datasets]
      OBS[observability<br/>logging, metrics, tracing, model_usage]
    end

    WEB --> API
    API --> DOMAIN & DB & MG & OBS
    API -.imports queue.-> WORKER
    WORKER --> DOMAIN & DB & MG & OBS
    WORKER --> API
    MG --> PROMPTS
    EVALS --> MG & OBS
    API --> PROMPTS
```

Notable edges:
- **`apps/worker` imports `apps/api`** for `settings.py` and `pilot.py`, so both processes make
  identical configuration and pilot-gate decisions (no drift).
- **`model_gateway` depends on `prompts`** — the hosted provider renders a versioned template and
  validates against the same Pydantic schema used to build it.
- **`evals` reuses `model_gateway.routing`** — evaluation exercises the *real* provider code path.

---

## 4. The dependency rule

The architecture's guiding principle: **the LLM provider, the database, and the web framework are all
replaceable behind boundaries.** This is enforced by convention, and it explains almost every design
choice in the repo.

| Boundary | Contract | Concrete implementations | Who is kept ignorant |
|---|---|---|---|
| LLM | `TicketAnalysisProvider` protocol (`providers/base.py`) | `MockTicketAnalysisProvider`, `HostedTicketAnalysisProvider` | routes, worker, evals never name a vendor |
| Queue | `AnalysisQueue` protocol (`queues.py`) | `RQAnalysisQueue`, test fakes | routes accept the queue as an injected dependency |
| Database | repository functions (`packages/db/repositories/*`) | SQLAlchemy + Postgres | routes never write SQL; they call `create_ticket(...)` etc. |
| HTTP shape | hand-written `*Read` converters | Pydantic response schemas | table layout never leaks to API clients |

**Consequences you can state plainly:**
- Switching from a fake AI to a real paid one is **one environment variable** (`MODEL_PROVIDER`), no
  code change.
- The **entire test suite runs with no API key, no network, no cost**, because the mock provider
  satisfies the same contract.
- A renamed database column does not break API clients, because conversion happens in one place.

---

## 5. Data model

Seven tables, all rooted at `Tenant`. Defined in `packages/db/supportops_db/models.py`; created by
migrations `0001`–`0007` (migrations are the source of truth, **not** the model file).

### Entity-relationship diagram

```mermaid
erDiagram
    TENANT ||--o{ USER : has
    TENANT ||--o{ TENANT_POLICY : has
    TENANT ||--o{ TICKET : has
    TICKET ||--o{ AI_RUN : "analysis attempts"
    TICKET ||--o{ TICKET_RECOMMENDATION : "suggestions"
    TICKET_RECOMMENDATION ||--o{ RECOMMENDATION_REVIEW : "human verdicts"
    AI_RUN }o--|| TICKET_RECOMMENDATION : "output (SET NULL)"
    TICKET ||--o{ COST_EVENT : "spend"

    TENANT {
        string id PK
        string name
        string slug UK
    }
    USER {
        string id PK
        string tenant_id FK
        string email
        string role "agent|lead|admin|service"
    }
    TENANT_POLICY {
        string id PK
        string tenant_id FK
        string name
        text content
        datetime retention_expires_at
    }
    TICKET {
        string id PK
        string tenant_id FK
        string external_id "UK with tenant_id"
        string subject
        text body
        string status "open default"
        string priority "normal default"
        json metadata_json
    }
    AI_RUN {
        string id PK
        string tenant_id FK
        string ticket_id FK
        string output_recommendation_id FK "SET NULL"
        string status "queued|running|succeeded|abstained|failed"
        string input_hash "sha256"
        string error_code
        datetime started_at
        datetime finished_at
    }
    TICKET_RECOMMENDATION {
        string id PK
        string tenant_id FK
        string ticket_id FK
        string source "baseline_v1|openai_..."
        string category
        string priority
        bool requires_escalation
        float confidence
        text suggested_reply
        json extracted_fields_json
        json reasons_json
    }
    RECOMMENDATION_REVIEW {
        string id PK
        string tenant_id FK
        string ticket_id FK
        string recommendation_id FK
        string reviewer_user_id
        string decision "approved|edited|rejected"
        text final_reply
        text notes
    }
    COST_EVENT {
        string id PK
        string tenant_id FK
        string ticket_id FK "CASCADE"
        string ai_run_id FK "SET NULL"
        string recommendation_id FK "SET NULL"
        string provider
        int input_tokens
        int output_tokens
        float estimated_cost_usd
        int latency_ms
    }
```

### Design decisions worth knowing

| Decision | Rationale |
|---|---|
| **UUID string PKs** | Generatable in API, worker, or test without a DB round-trip; leak no volume information (a ticket "#4317" reveals counts, a UUID does not). |
| **`tenant_id` on every table + index** | Shared-DB multi-tenancy; isolation depends on *always* filtering by tenant, so repositories require it as an argument. |
| **`ondelete` chosen per relationship** | Ticket→children `CASCADE`; but `AIRun.output_recommendation_id` and `CostEvent.*` use `SET NULL` — the *record that a call happened and what it cost must outlive the text it produced.* |
| **Append-only history** | Recommendations and reviews are never overwritten. A disagreeing supervisor creates a *second* review; the audit trail is immutable. |
| **Composite indexes** | `(tenant_id, status)` on tickets serves "this company's open tickets"; `ai_runs.status` alone serves the cross-tenant "are any jobs stuck?". |
| **JSON columns** | `metadata_json`, `extracted_fields_json`, `reasons_json` for shapes not known ahead of time — flexible, but not for anything you filter or sum. |
| **`estimated_cost_usd` is `Float`** | Honest "estimate" for reporting; a real billing system would use fixed-precision decimal. |
| **Loose refs for accountability** (`created_by_user_id`, `reviewer_user_id` are plain strings, not FKs) | The record of *who decided* survives that user being deleted. |

### Transaction & session model (`packages/db/session.py`)

- **Engine** = one per process (connection pool), cached. `pool_pre_ping=True` silently replaces
  stale connections after a DB restart.
- **Session** = one per unit of work (one request / one job). `autoflush=False` + `autocommit=False`
  mean nothing hits the DB until an explicit `flush()`/`commit()`. This is what lets a route save a
  recommendation **and** its cost event in a single commit — you never get one without the other.
- The API uses a `yield`-based dependency (`get_db_session`) that always closes the session, even on
  crash. The worker creates a fresh engine/session per job (RQ forks a child process per job, and a
  DB connection cannot be safely shared across a fork).

---

## 6. The three analysis paths

The core idea of the whole product. A ticket can be analyzed three ways, and each exists for a reason.

```mermaid
flowchart TB
    T[Ticket] --> B & S & A
    B[1 - Baseline<br/>POST /baseline-analysis]
    S[2 - Sync AI<br/>POST /ai-analysis]
    A[3 - Async AI<br/>POST /analyze -> 202]

    B -->|instant, free, cannot fail| RB[Recommendation<br/>source=baseline_v1]
    S -->|blocks 2-10s, HTTP error on failure| RS[Recommendation<br/>source=openai_...]
    A -->|returns immediately<br/>worker does the slow part| Q[(Redis queue)]
    Q --> W[Worker] --> RA[Recommendation + AIRun state]
```

| Path | Endpoint | Latency | On failure | Purpose |
|---|---|---|---|---|
| **Baseline** | `POST /tickets/{id}/baseline-analysis` | instant | cannot fail | the **yardstick** — proves the AI beats free keyword rules |
| **Sync AI** | `POST /tickets/{id}/ai-analysis` | 2–10 s, blocks | HTTP 502/503 | simple, good for testing |
| **Async AI** | `POST /tickets/{id}/analyze` → `202` | returns instantly | recorded on `ai_runs` row | what the real UI uses |

The **baseline** (`packages/domain/services/baseline.py`) is deliberately non-AI: keyword + regex
matching, fully deterministic. It has three jobs: (1) the comparison endpoint, (2) the **pilot gate**
— it classifies a ticket *before* deciding whether the AI may run (you can't ask the AI what a ticket
is about to decide whether to pay for asking it), and (3) the **mock provider's brain**.

Its category order **is** its priority order: `security` is checked first, so "account hacked and
charged twice" is treated as security, not billing — *when a ticket could be two things, treat it as
the one where being wrong costs the most.*

---

## 7. Request flows (sequence diagrams)

### 7.1 Create a ticket (idempotent)

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant MW as Observability middleware
    participant R as tickets route
    participant Repo as tickets repository
    participant DB as Postgres

    C->>MW: POST /tickets (X-Tenant-Id, X-User-Id, X-Role)
    MW->>MW: assign request_id, start span, log_context
    MW->>R: get_current_actor + get_db_session
    R->>Repo: get_ticket_by_external_id(tenant, external_id)
    alt already exists (retry)
        Repo-->>R: existing ticket
        R-->>C: 200 OK (not 201) — same effect as first time
    else new
        R->>Repo: create_ticket(...)
        Repo->>DB: INSERT (UNIQUE(tenant_id, external_id) guards races)
        R->>DB: commit + refresh
        R-->>C: 201 Created
    end
    MW->>MW: log api_request_completed (status, duration_ms, request_id header)
```

Idempotency is enforced at **two** layers: the app-level `external_id` check (returns 200), and a DB
`UniqueConstraint(tenant_id, external_id)` that holds even under a race.

### 7.2 Synchronous AI analysis

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant R as tickets route
    participant P as pilot gate
    participant MG as model_gateway (hosted)
    participant LLM as Hosted LLM
    participant DB as Postgres

    C->>R: POST /tickets/{id}/ai-analysis
    R->>R: _require_tenant, load ticket (404 if foreign/missing)
    R->>P: classify with baseline -> category; ai_analysis_eligibility?
    alt disabled globally
        P-->>C: 503 ai analysis is disabled
    else not in pilot scope
        P-->>C: 403 not enabled for tenant/category
    else allowed
        R->>MG: build provider (routing), analyze_ticket(subject, body, policy_context)
        MG->>LLM: POST /responses (strict json_schema, store:false)
        alt config error / unknown provider
            MG-->>R: raise -> 503 not configured
        else timeout / unreachable
            MG-->>R: raise -> 503 unavailable
        else bad JSON / refusal / invalid
            MG-->>R: raise -> 502 invalid output
        else success
            MG-->>R: TicketAnalysisResult
            R->>DB: create_ticket_recommendation + record cost (one commit)
            R-->>C: 201 Created (recommendation)
        end
    end
```

### 7.3 Asynchronous AI analysis (enqueue → worker → poll)

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant R as tickets route
    participant DB as Postgres
    participant Q as Redis (RQ)
    participant W as Worker (jobs.py)
    participant MG as model_gateway
    participant LLM as Hosted LLM

    C->>R: POST /tickets/{id}/analyze
    R->>R: pilot gate (as above)
    R->>DB: create ai_runs row (status=queued) + commit   %% DB FIRST
    R->>Q: enqueue_call("...analyze_ticket_job", run_id)   %% then queue
    alt Redis down
        R->>DB: mark_ai_run_failed(queue_unavailable)
        R-->>C: 503 analysis queue unavailable
    else queued
        R-->>C: 202 Accepted (job sheet)
    end

    W->>Q: dequeue run_id
    W->>DB: mark_ai_run_running + commit (visible immediately)
    W->>DB: load ticket (fail row if gone)
    W->>W: baseline classify (2nd opinion) + re-check pilot gate
    W->>MG: analyze_ticket(...)
    MG->>LLM: POST /responses
    MG-->>W: result OR ModelGatewayError
    alt success
        W->>DB: recommendation + cost + status(succeeded|abstained), one commit
    else failure
        W->>DB: mark_ai_run_failed(error_code, error_message)
    end

    loop poll every ~2s
        C->>R: GET /tickets/{id}/analysis
        R->>DB: list ai_runs (+ nested recommendation if finished)
        R-->>C: statuses (pending->running->succeeded/abstained/failed)
    end
```

**Two decisions to note:**
- **DB row before queue push.** A lost job is at worst a visible `pending` row someone can retry —
  never a queued ID pointing at a nonexistent row.
- **Only the `run_id` travels on the queue.** The worker re-reads current data from the DB, so it
  never acts on a stale copy, and the queue stays tiny.
- **The pilot gate is re-checked in the worker**, so a job that sat in the queue while the kill-switch
  was flipped off still won't run.

### 7.4 Human approval (the safety mechanism)

```mermaid
sequenceDiagram
    autonumber
    participant C as Reviewer (agent/lead)
    participant R as approvals route
    participant DB as Postgres

    C->>R: POST /tickets/{tid}/recommendations/{rid}/reviews {decision, edits?, notes}
    R->>R: _require_tenant; walk tenant->ticket->recommendation (404 at any broken link)
    alt decision = rejected
        R->>R: final_summary/reply = None (nothing agreed)
    else decision = approved
        R->>R: copy AI's summary + reply verbatim (survives retention of the draft)
    else decision = edited
        R->>R: require at least one edit (else 422); keep edits, fall back to AI text per-field
    end
    R->>DB: create_recommendation_review(reviewer_user_id from Actor) + commit
    R->>R: record_draft_review(decision)  %% feeds approval-rate metric
    R-->>C: 201 Created (review)
```

The nested path `/tickets/{tid}/recommendations/{rid}/reviews` is verified at **every** level, so you
cannot reach a real recommendation via the wrong ticket (a classic access-control hole closed).

---

## 8. The model gateway internals

`packages/model_gateway` is the entire boundary to the LLM. `routing.py` is the switchboard:

```
build_ticket_analysis_provider(name) ->
   "mock"            -> MockTicketAnalysisProvider()      (ignores all config, needs none)
   "openai"/"hosted" -> HostedTicketAnalysisProvider(...) (real, paid)
   anything else     -> raise UnsupportedModelProviderError  (never silently fall back)
```

### The hosted call, step by step (`providers/hosted.py`)

```mermaid
flowchart TD
    A[analyze_ticket] --> B[get_prompt + render_prompt<br/>fill template with ticket + policy]
    B --> C[build payload:<br/>strict json_schema, store:false, max_output_tokens, metadata]
    C --> D[POST /responses with Bearer key, 30s timeout]
    D -->|httpx.TimeoutException| E1[ModelProviderRequestError]
    D -->|HTTPStatusError| E2[ModelProviderRequestError + body 500 chars]
    D -->|HTTPError| E3[ModelProviderRequestError]
    D -->|non-JSON / not dict| E4[ModelProviderResponseError]
    D --> F[_extract_output_text<br/>error? incomplete? refusal? nested content]
    F -->|refusal / no text / bad status| E5[ModelProviderResponseError]
    F --> G[_parse_analysis<br/>Pydantic validate against FullTicketAnalysis]
    G -->|ValidationError| E6[ModelProviderResponseError]
    G --> H[_validate_evidence_ids<br/>reject citations outside 4 allowed sources]
    H -->|unsupported ids| E7[ModelProviderResponseError]
    H --> I[_analysis_to_result<br/>OpenAI-specific -> standard TicketAnalysisResult]
    I --> J[Return result: category, priority, escalation,<br/>confidence, reply, extracted_fields, tokens, latency]
```

### The three anti-hallucination defenses (name all three in interviews)

1. **Constrain at generation** — the request sends `text.format = {type: json_schema, strict: true,
   schema: FullTicketAnalysis.model_json_schema()}`. The provider enforces the shape *while generating*.
2. **Validate on arrival** — `FullTicketAnalysis.model_validate_json(...)` re-checks it. Defense in
   depth: never trust a remote system to have validated on your behalf when output faces customers.
3. **Evidence checking** — the model must cite which of four supplied inputs (`ticket-subject`,
   `ticket-body`, `customer-id`, `policy-context`) backed each conclusion. `_validate_evidence_ids`
   rejects any other citation as fabricated → the whole response is discarded.

Supporting schema discipline in `packages/prompts/schemas.py`:
- `Literal` types → fixed vocabularies (category is one of six values), so results are **countable**.
- `extra="forbid"` → an invented field is a hard failure (blocks smuggled fields / excessive agency).
- Explicit `abstain` + `missing_information` → the model has an honest way to say "I don't know".
- One schema, used to **ask** (embedded in the prompt via `model_json_schema()`) and to **check** — so
  the request and the validation can never drift apart.

### The error taxonomy → HTTP status mapping

| Gateway exception | Meaning | Sync HTTP | Worker action |
|---|---|---|---|
| `ModelProviderConfigurationError`, `UnsupportedModelProviderError` | our misconfiguration | **503** | `mark_ai_run_failed(error_code)` |
| `ModelProviderRequestError` | couldn't reach / timeout | **503** | `mark_ai_run_failed(error_code)` |
| `ModelProviderResponseError` | reached them, unusable answer / refusal | **502** | `mark_ai_run_failed(error_code)` |

The sync path splits these into three HTTP codes (the caller must know which). The worker catches
them all in one place — nobody is waiting, so every case leads to the same action: write the failure
to the job sheet with a stable `error_code` (countable) + `error_message` (for humans). **httpx
exceptions never leak past `model_gateway`.**

### Cost calculation (`cost.py`)

`(input_tokens/1000 × input_rate) + (output_tokens/1000 × output_rate)`, rounded to 8 decimals (a
single call can cost a fraction of a cent — 2 decimals would round everything to `$0.00`). All four
inputs are `max(x, 0)`-clamped, because token counts come from the provider and rates come from env
vars — a single negative value would silently *subtract* from cost totals.

---

## 9. State machines

### AIRun lifecycle (async analysis)

```mermaid
stateDiagram-v2
    [*] --> queued: POST /analyze creates row
    queued --> running: worker mark_ai_run_running (committed immediately)
    running --> succeeded: model answered, abstain=false
    running --> abstained: model returned abstain=true
    running --> failed: ticket gone / pilot off / ModelGatewayError
    queued --> failed: Redis enqueue failed (queue_unavailable)
    succeeded --> [*]
    abstained --> [*]
    failed --> [*]
```

`abstained` is a **distinct outcome, not a failure**. A model that declines when unsure is behaving
well; scoring that as failure would push toward models that always guess. The recommendation and cost
are still saved; the outcome is labeled honestly so quality metrics aren't inflated.

> Naming note: the DB default status is `queued`; the API schema calls the same state `pending`.

### Review decision → stored content

```mermaid
stateDiagram-v2
    [*] --> rejected: store nothing (no agreed text)
    [*] --> approved: copy AI summary + reply verbatim
    [*] --> edited: keep human edits, fall back to AI text per-field
    edited --> error422: no edits supplied -> 422 Unprocessable
```

`edited` uses `is not None` (not a truthiness test) so an empty string is respected as a deliberate
"delete this text" rather than treated as "unchanged".

---

## 10. Evaluation subsystem

`packages/evals` answers "did quality go up or down?" *before* shipping, and blocks releases that
regress.

```mermaid
flowchart LR
    DS[JSONL datasets<br/>golden / difficult / safety] --> RUN[runner.py<br/>load -> analyze -> score]
    RUN -->|build_ticket_analysis_provider| MG[same provider as prod<br/>mock in CI]
    RUN --> SCORE[scoring.py<br/>precision / recall / macro-F1 / gates]
    SCORE --> REP[reports.py -> docs/eval-report.md]
    SCORE --> EXIT{passed_gates?}
    EXIT -->|yes| Z0[exit 0]
    EXIT -->|no| Z1[exit 1 -> CI build red]
    EXIT -->|no| MET[record_eval_regression + prompt_injection_failure metrics]
```

### The three datasets

| Dataset | Measures | Example content |
|---|---|---|
| `golden` | accuracy on normal tickets | known category/priority/fields |
| `difficult` | ambiguous cases | often mined from drafts humans rejected |
| `safety` | adversarial robustness | prompt-injection, must-abstain, must-not-reveal-prompt |

### Metrics (`scoring.py`)

- **Category accuracy** and **macro-F1** — macro-F1 weights each category equally, so "classify
  everything as billing" (which scores well on plain accuracy under class imbalance) is exposed.
- **Field precision/recall** (order IDs, amounts) via set intersection.
- **Escalation precision/recall** — recall matters most (missing a fraud escalation is harmful).
- **Unsupported-claim rate**, **safety pass rate**, **draft rubric** (a crude 4-part proxy), **p95 latency**.

### The gates (the philosophy: *accuracy may be imperfect, safety may not*)

```
Universal (any dataset), must be ZERO:
  - invalid structured output count
  - unsupported claim rate
Per-dataset:
  - golden: category accuracy >= 0.80
  - safety: safety pass rate == 1.0
```

`runner.py`'s final line, `return 0 if passed_gates else 1`, is what turns "we should evaluate our
prompts" into an enforced CI gate. It defaults to the **mock provider** so CI is free, offline, and
deterministic — honestly limited to proving the machinery, not a real model's quality.

---

## 11. Observability: logs, metrics, traces, cost

Four instrumentation streams, all carrying tenant/ticket/run IDs so one ticket can be followed
end-to-end across API and worker.

```mermaid
flowchart TD
    REQ[Any request or job] --> LOG & TR & MET & COST
    LOG[Structured JSON logs<br/>logging.py] -->|stdout| COLLECT[Docker/K8s log collector]
    LOG -. redaction .-> RED[emails, phones, cards, secrets scrubbed]
    TR[Trace spans<br/>tracing.py / OpenTelemetry optional] --> BACKEND[Jaeger/Tempo if configured]
    MET[In-memory counters + summaries<br/>metrics.py] --> EP[GET /metrics/runtime]
    EP --> PROM[Prometheus scrape] --> GRAF[Grafana dashboard]
    COST[cost_events row<br/>model_usage.py + cost.py] --> DB[(Postgres)]
    DB --> CEP[GET /metrics/costs per tenant]
    DB --> CREP[docs/cost-report.md]
```

### Logs (`observability/logging.py`)

- **JSON per line** (searchable), always UTC, written to **stdout** (container convention).
- **`log_context(...)`** uses a `contextvars` context variable to attach `request_id`, `tenant_id`,
  `ticket_id`, `ai_run_id` to *every* line inside a block — including deep in DB code — without
  threading them through every function. Isolated per request/task.
- **Redaction is unavoidable:** every line passes through `JsonLogFormatter.format`, which scrubs
  emails, phone numbers, payment cards, and API-key/token patterns (recursively, including exception
  tracebacks and nested fields). Ticket text is never logged — an **input hash** is logged instead.

### Metrics (`observability/metrics.py`)

- **Live, in-process, reset on restart** — Prometheus keeps the history, so the app only reports
  current totals. (Distinct from the *historical* DB-backed metrics in `db/repositories/metrics.py`.)
- Counters (`*_total`) and summaries (count/total/max — **no percentiles**, an accepted limitation).
- Thread-safe via a `Lock`; metric names are an allow-list (`COUNTER_NAMES`) so a typo raises instead
  of creating an invisible parallel series.
- Labels (provider, mode, error_code, token_type…) turn "12 failures" into "10 timeouts + 2 invalid".
- Zero-lines are emitted for never-fired metrics so dashboards show a flat zero, not "no data".
- **Known gap:** `record_draft_review` counts approved/rejected but **not edited** — the live
  dashboard and the DB-backed report will disagree on total reviews.

### Traces (`observability/tracing.py`)

- OpenTelemetry, **entirely optional** — if the library or a collector is absent, `trace_span` yields
  as a no-op and the app is unaffected (observability must never break what it observes). Trade-off: a
  missing library produces no warning; traces just don't appear.
- Nested spans build a timeline: `api.request → api.ai_analysis → model_gateway.call → db.*`.

### Cost (`observability/model_usage.py` + `model_gateway/cost.py`)

Every AI call writes a `cost_events` row (tokens in/out separately, estimated USD, latency, provider,
model, prompt version, `sync_`/`async_ticket_analysis` operation). Token counts are stored alongside
cost so a later price correction can be recomputed on historical data.

---

## 12. Security & multi-tenancy

```mermaid
flowchart TD
    REQ[Request] --> H{X-Tenant-Id + X-User-Id present?}
    H -->|no| E401[401 Unauthorized]
    H -->|yes| ROLE{role in agent/lead/admin/service?}
    ROLE -->|no| E403[403 Forbidden]
    ROLE -->|yes| ACT[Actor tenant_id, user_id, role]
    ACT --> TEN{tenant exists?}
    TEN -->|no| E404[404 tenant not found]
    TEN -->|yes| SCOPE[repository query filtered by tenant_id]
    SCOPE --> OWN{row belongs to tenant?}
    OWN -->|no| E404b[404 not found - never 403]
    OWN -->|yes| WORK[do the work]
```

| Threat (OWASP-LLM aligned) | Mitigation | Where |
|---|---|---|
| Prompt injection | untrusted ticket text delimited, never placed above instructions; scored `safety` dataset | prompts, evals |
| Excessive agency | model returns **data only** — cannot pick tools/permissions; `extra="forbid"` blocks smuggled fields | schemas |
| Cross-tenant leakage | required `tenant_id` filter; foreign IDs → **404 not 403** (403 confirms the ID exists) | dependencies, routes |
| Sensitive-info disclosure (logs) | recursive redaction; hashes instead of text; error bodies truncated to 500 chars | logging, hosted |
| Secret leakage | API key never logged; health-check errors return only the exception *type*, not the message (which may contain the DSN/password) | checks |
| Provider data retention | `store: false` on every call | hosted |
| Unsafe roles for policy writes | `POLICY_WRITE_ROLES = {lead, admin}` | dependencies, policies route |

**Trust boundary reminder:** identity headers are trusted because a gateway sets them; the service is
never public-facing. Documented in `docs/threat-model.md`.

---

## 13. Reliability & failure handling

| Concern | Mechanism |
|---|---|
| Liveness vs readiness | `GET /health` (no external checks → restart if failing) vs `GET /ready` (checks DB + Redis with 2s timeouts → stop routing traffic, don't restart). Getting these backwards causes restart storms. |
| Timeouts | 30s LLM call timeout; 2s DB/Redis health-check timeouts. |
| Idempotency | `external_id` app check + DB unique constraint. |
| Bounded queue failure | Redis down → job marked `failed(queue_unavailable)` + 503, never a phantom `pending`. |
| Stale-job safety | worker re-checks the pilot kill-switch and re-loads the ticket at execution time. |
| Partial-failure atomicity | recommendation + cost + status committed together (one fact, one commit). |
| Provider fallback | `MODEL_PROVIDER=mock` as an instant, free, deterministic fallback during an incident. |
| Crash isolation | RQ runs each job in a forked child; a crashing/leaking job cannot take the worker down. |
| Stale connections | `pool_pre_ping=True` replaces dead pooled connections transparently. |

---

## 14. Configuration

All configuration is centralized in `apps/api/supportops_api/settings.py` (`pydantic-settings`),
filled from environment variables (uppercased field names) or a local `.env`. Invalid values fail at
boot (fail loud, not weird-later). `@lru_cache` means one settings object per process — changing an
env var requires a restart.

| Variable | Default | Effect |
|---|---|---|
| `DATABASE_URL` | local Postgres | rewritten to `postgresql+psycopg://` in `session.py` |
| `REDIS_URL` | local Redis /0 | queue + readiness check |
| `CORS_ORIGINS` | `""` (allow nothing) | comma-separated allowed browser origins (API only) |
| `AI_ANALYSIS_ENABLED` | `true` | master kill-switch |
| `AI_ANALYSIS_ENABLED_TENANTS` | `""` (all) | pilot tenant allowlist |
| `AI_ANALYSIS_ENABLED_CATEGORIES` | `""` (all) | pilot category allowlist |
| `MODEL_PROVIDER` | `mock` | `mock` \| `openai`/`hosted` |
| `MODEL_API_KEY` | `""` | never hard-code; env only |
| `MODEL_NAME` / `MODEL_BASE_URL` | `gpt-5.6` / OpenAI v1 | which model, which endpoint |
| `MODEL_TIMEOUT_SECONDS` | `30.0` | LLM call timeout |
| `MODEL_MAX_OUTPUT_TOKENS` | `1200` | caps reply length and cost |
| `MODEL_*_COST_PER_1K_TOKENS` | `0.0` | prices for the cost report only |

### The pilot kill-switch (defense against a misbehaving feature)

```mermaid
flowchart LR
    A{AI_ANALYSIS_ENABLED?} -->|false| OFF[503 disabled - everyone]
    A -->|true| T{tenant in ENABLED_TENANTS<br/>or list empty?}
    T -->|no| DENY[403 not in pilot]
    T -->|yes| Cc{category in ENABLED_CATEGORIES<br/>or list empty?}
    Cc -->|no| DENY
    Cc -->|yes| GO[allowed]
```

Checked in **both** the API (before enqueue) **and** the worker (after dequeue) via the shared
`apps/api/supportops_api/pilot.py`, so the switch is genuinely immediate for in-flight jobs.

---

## 15. Deployment, CI/CD & rollback

### CI (`.github/workflows/ci.yml`) — seven parallel jobs

```mermaid
flowchart LR
    PR[pull_request / push main] --> L[lint - ruff]
    PR --> T[typecheck - mypy apps packages]
    PR --> U[test - unit, no services]
    PR --> I[integration - real Postgres + Redis]
    PR --> M[migrations - upgrade head + alembic check drift]
    PR --> E[eval-smoke - runner --dataset all, mock]
    PR --> D[docker-build - compose config + build api/web images]
```

All jobs run with `MODEL_PROVIDER=mock` (no secret, no cost, deterministic). Two standouts:
- **`migrations`** runs `alembic check` — catches "changed `models.py`, forgot the migration" before
  it reaches production as "column does not exist".
- **`eval-smoke`** fails the build on any AI quality-gate regression, exactly like a failing test.

### Environments

| Environment | Compose file | Model | Secrets | Notes |
|---|---|---|---|---|
| Local | `docker-compose.yml` | mock | committed placeholders | full stack incl. dev UIs + monitoring |
| CI | GitHub services | mock | none | ephemeral Postgres/Redis |
| Staging | `infra/staging/docker-compose.staging.yml` | configurable | env/secret manager | pushed images by tag, `docs/rollback-runbook.md` |
| Cloud | `infra/terraform/` (placeholder) | — | — | not yet implemented |

### Rollback controls (`docs/rollback-runbook.md`), by failure type

| Failure | Action |
|---|---|
| App regression | pin `SUPPORTOPS_API_IMAGE` / `SUPPORTOPS_WEB_IMAGE` to last-good tags |
| Prompt regression | roll back to the API image carrying the last-good prompt registry |
| Model-route incident | `MODEL_PROVIDER=mock`, clear hosted cost/API-key settings |
| AI-specific incident | `AI_ANALYSIS_ENABLED=false`, restart api + worker |
| Database incident | prefer forward-compatible migrations; restore a snapshot only if app rollback can't run on the migrated schema |

---

## 16. Data lifecycle & retention

```mermaid
flowchart LR
    CREATE[row created with optional retention_expires_at] --> LIVE[in use]
    LIVE --> EXPIRE{retention_expires_at <= now?}
    EXPIRE -->|no / null| KEEP[kept - null means keep indefinitely]
    EXPIRE -->|yes| COUNT[collect_retention_candidates counts per table]
    COUNT --> LOG[log candidate_count every run]
    COUNT --> DEL{dry_run?}
    DEL -->|true default| NOOP[delete nothing]
    DEL -->|false| WARN[log retention_deletion_not_implemented - still deletes nothing]
```

**Honest status:** `apps/worker/retention.py` **counts and logs** expired rows but **deletes
nothing** — the deletion half is deliberately unimplemented so the counts can be watched before any
irreversible deletion runs against production. The GDPR-style promise is scaffolded, not yet kept.
`dry_run=True` is the default so destructive behaviour must be explicitly requested.

---

## 17. Naming inconsistencies (read before debugging)

These drifted during development and are documented rather than renamed (renaming tables means
migration work). Knowing them saves real confusion:

| Concept | Names in the wild |
|---|---|
| AI output table | `ticket_recommendations` (DB) ≈ guide's `ai_outputs` |
| Human verdict table | `recommendation_reviews` (DB) ≈ guide's `approvals` |
| Support policy | `TenantPolicy` (model) / `support_policies` (table) / `SupportPolicy` (API) — all the same thing |
| Async job status | `queued` (DB default) = `pending` (API schema) |
| Provider names | `openai` and `hosted` are aliases for the same implementation |
| Two `metrics` modules | `observability/metrics.py` (live, in-memory) vs `db/repositories/metrics.py` (historical, DB) |

---

## 18. Glossary

- **Tenant** — one customer company; the isolation unit. Every row carries `tenant_id`.
- **Actor** — the verified caller (tenant + user + role) built from request headers.
- **Baseline** — the deterministic keyword/regex classifier; yardstick, pilot gate, and mock brain.
- **Recommendation** — one analysis result (baseline or AI) + optional draft reply. Append-only.
- **Review** — a human verdict on a recommendation: approved / edited / rejected. Write-once.
- **AIRun** — the async job sheet; drives `queued → running → succeeded/abstained/failed`.
- **Abstain** — the model honestly declining; a distinct outcome, not a failure.
- **Evidence IDs** — the model's citations of which supplied input backed each conclusion.
- **Gate** — an automatic release blocker in the eval harness (zero unsupported claims, 100% safety…).
- **Pilot switch** — env-var kill-switch scoping the AI by tenant/category, checked in API *and* worker.
- **Cost event** — a per-call record of tokens, estimated USD, latency, provider, model, prompt version.
- **Provider / model gateway** — the swappable boundary to the LLM; the rest of the app is provider-agnostic.
- **Liveness / readiness** — `/health` (is the process alive?) vs `/ready` (are DB + Redis reachable?).
- **Engine / Session** — SQLAlchemy: one connection pool per process / one unit of work per request.

---

### Appendix: file-to-responsibility index

| Area | Primary files |
|---|---|
| HTTP entry, middleware | `apps/api/supportops_api/main.py` |
| Auth, DB session, queue injection | `apps/api/supportops_api/dependencies.py` |
| Ticket + analysis endpoints | `apps/api/supportops_api/routes/tickets.py` |
| Approval endpoints | `apps/api/supportops_api/routes/approvals.py` |
| Policies, metrics, health routes | `apps/api/supportops_api/routes/{policies,metrics,health}.py` |
| Pilot gate | `apps/api/supportops_api/pilot.py` |
| Health checks | `apps/api/supportops_api/checks.py` |
| Config | `apps/api/supportops_api/settings.py` |
| Worker loop / job logic / queue | `apps/worker/supportops_worker/{main,jobs,queues}.py` |
| Retention | `apps/worker/supportops_worker/retention.py` |
| Baseline classifier | `packages/domain/supportops_domain/services/baseline.py` |
| ORM models / repositories / migrations / session | `packages/db/supportops_db/{models.py,repositories/,migrations/,session.py}` |
| LLM contract / routing / providers / cost / errors | `packages/model_gateway/supportops_model_gateway/*` |
| Prompt registry + output schemas | `packages/prompts/supportops_prompts/{registry,schemas}.py` |
| Eval runner / scoring / reports / datasets | `packages/evals/supportops_evals/*` |
| Logs / metrics / traces / cost usage | `packages/observability/supportops_observability/*` |
| Local stack / CI | `docker-compose.yml`, `.github/workflows/ci.yml` |
```
