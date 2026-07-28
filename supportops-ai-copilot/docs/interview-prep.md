# SupportOps AI Copilot — Complete Interview Prep

A single reference to understand this project end-to-end, map it to the curriculum, and
defend every part of it in an interview. Written from a full read of the codebase.

> **One-line pitch:** *A production-shaped, multi-tenant support-ticket AI copilot. It classifies
> tickets, extracts fields, sets priority, drafts replies, and requires a human to approve every
> draft — with a keyword baseline to prove the AI earns its cost, an offline evaluation harness
> with hard release gates, full cost/observability instrumentation, and a pilot kill-switch.*

---

## 1. How to read this document

- **Section 2** — the 30-second and 3-minute elevator pitches (memorize these).
- **Section 3** — lesson coverage map: what's *covered*, *partial*, and *deliberately not built*.
- **Section 4** — architecture and the three analysis paths (the spine of any deep-dive).
- **Section 5** — concept-by-concept deep dives, each with *what / why / where in code*.
- **Section 6** — the data model.
- **Section 7** — the design trade-offs that interviewers dig into.
- **Section 8** — a big Q&A bank grouped by topic.
- **Section 9** — honest gaps (say these before they ask).
- **Section 10** — glossary.

---

## 2. Elevator pitches

**30 seconds:**
> "It's a customer-support AI copilot built like a real production service. A support agent files a
> ticket; the system runs it through a hosted LLM that returns a *strictly structured* analysis —
> category, priority, extracted fields, a draft reply, and honest 'I don't know' signals. A human
> always approves the draft before it's used. Around that core I built the production concerns:
> multi-tenancy, an async worker, an evaluation harness with release gates, cost tracking per
> tenant, observability, and a pilot kill-switch to roll it out safely."

**3 minutes** (add the reasoning):
> "The design principle throughout is *never trust the model blindly*. Three defenses: (1) I ask the
> provider for JSON-schema-constrained output in strict mode, (2) I re-validate the reply against
> the same Pydantic schema on arrival, and (3) I make the model cite evidence IDs and reject any
> citation of a source that wasn't actually supplied — an anti-hallucination check. I also keep a
> deterministic keyword baseline as a yardstick: if the paid LLM can't beat free keyword matching,
> it isn't worth running, and every recommendation records which method produced it so I can compare
> approval rates. The evaluation harness runs golden/difficult/safety datasets in CI and blocks
> release on hard gates — zero unsupported claims, zero invalid output, 100% safety pass. And the
> whole thing is instrumented: structured logs with a request ID, Prometheus metrics, cost events
> per tenant, and a pilot switch scoped by tenant and category so I can turn the AI off instantly
> during an incident."

---

## 3. Lesson coverage map

This project is the **Applied AI / Generative AI Engineer production track**. It implements the
"understand → build → operate" spine for an LLM product and stops deliberately before model
training, RAG, multimodal, and orchestration frameworks.

Legend: ✅ built and demonstrable · 🟡 partial / simplified · ⬜ intentionally out of scope.

| Lesson | Topic | Status | Where in this repo |
|---|---|---|---|
| 01 | Learning environment | ✅ | `requirements-dev.txt`, `ruff`/`mypy`/`pytest`, `docker-compose.yml`, `.github/workflows/ci.yml`, `.env.example` |
| 02 | Python for production AI | ✅ | dataclasses (`Actor`, `Baseline*`), Protocol providers, typed config, explicit error classes, context managers (`log_context`, `trace_span`, DB session) |
| 03 | Async & concurrent services | 🟡 | Redis + RQ worker, `POST /analyze` → `202 Accepted`, job state machine, graceful queue-down handling. (Queue-based, not deep asyncio.) |
| 04 | Testing & code quality | ✅ | mock provider + fake queue, failure-path tests, schema validation tests, software-tests vs model-evaluation kept separate |
| 05 | API & backend engineering | ✅ | FastAPI, OpenAPI docs, Pydantic request/response schemas, header auth, RBAC, **idempotency** on ticket create, multi-tenant, status-code discipline (200/201/202/401/403/404/502/503) |
| 06 | SQL, data modeling, storage | ✅ | SQLAlchemy models, Alembic migrations 0001–0007, PK/FK, `ondelete` CASCADE vs SET NULL, composite indexes, JSON columns, retention columns, tenant isolation |
| 07 | Applied AI problem discovery | 🟡 | baseline-vs-AI framing, human-in-the-loop, pilot plan, `docs/pilot-report.md`, adoption/approval metrics |
| 08 | Foundation-model fundamentals | 🟡 | token accounting, `max_output_tokens`, context assembly, hallucination/uncertainty via `abstain`. (No tokenizer lab / attention internals.) |
| 09 | Model API integration | ✅ | `packages/model_gateway`: provider auth (Bearer), streaming-free structured output, token accounting, timeout/error classification, mock fallback, provider-independent adapter, cost attribution |
| 10 | Prompt & context engineering | ✅ | `packages/prompts`: versioned templates, output contracts from Pydantic schemas, untrusted-content separation, prompt-injection awareness, regression via evals |
| 11 | Applied LLM product | ✅ | **the whole product** — classify/extract/prioritize/draft, human approval, feedback capture, cost tracking, abstention, full traceability |
| 12–14 | Embeddings / RAG | ⬜ | Not built. "Policy context" is a plain DB fetch, not retrieval. |
| 15 | AI evaluation engineering | ✅ | `packages/evals`: golden/difficult/safety datasets, precision/recall/macro-F1, p95 latency, **release gates**, CI regression. (Rule-based scoring, no LLM-judge.) |
| 16 | AI data engineering | 🟡 | feedback-to-eval loop (`docs/feedback-to-eval-loop.md`), difficult-case mining. (No warehouse/dbt/streaming.) |
| 17 | Tool calling & controlled workflows | 🟡 | human approval, durable state machine (`ai_runs`), idempotency, audit trail. (No live tool execution.) |
| 18 | MCP & agent integration | ⬜ | Not built. |
| 19–27 | Training, post-training, multimodal, voice | ⬜ | Out of scope. |
| 28 | AI security & privacy | ✅ | prompt-injection separation, PII/secret log redaction, least privilege, tenant isolation, "excessive agency" prevention (model can't pick tools), `docs/threat-model.md`, security regression tests |
| 29 | Responsible AI & governance | 🟡 | threat model, human oversight, retention/deletion scaffolding. (No formal governance package.) |
| 30 | Production architecture & reliability | ✅ | health/readiness, retries/timeouts, graceful degradation, provider fallback, kill-switch, DLQ-style failed-run records |
| 31 | Observability, feedback & cost | ✅ | `packages/observability`: JSON logs + request ID, Prometheus `/metrics/runtime`, trace spans, cost per tenant, Grafana dashboard, sensitive redaction |
| 32 | Cloud deployment | 🟡 | staging compose (`infra/staging`), pushed-image config, rollback runbook, Terraform placeholder. (Not a real cloud deploy.) |
| 33 | Kubernetes | ⬜ | Not built. |
| 34 | LLMOps / MLOps | 🟡 | CI/CD quality+safety gates, prompt/model versioning, `docs/rollback-runbook.md`, feedback loop. (No model registry / continuous training.) |
| 35+ | Open-model serving & beyond | ⬜ | Out of scope. |

**How to say this in an interview:** *"I went deep on the applied-engineering and operations half of
the curriculum — everything needed to ship and run an LLM feature responsibly — and deliberately
left RAG, fine-tuning, and Kubernetes as separate tracks so this stayed a coherent, well-tested
product rather than a shallow tour of everything."*

---

## 4. Architecture

### 4.1 Package boundaries (why the repo is shaped this way)

```
apps/api                FastAPI HTTP layer (routes, schemas, dependencies, settings)
apps/worker             background worker for async analysis + retention job
apps/web                static agent-review console (nginx)
packages/domain         business rules with no framework dependency (the baseline classifier)
packages/db             SQLAlchemy models, repositories, Alembic migrations
packages/model_gateway  provider-neutral model access (mock + hosted OpenAI)
packages/prompts        versioned prompt templates + Pydantic output schemas
packages/evals          datasets, scoring, runner, release gates
packages/observability  structured logs, metrics, traces, cost helpers
infra                   prometheus, grafana, staging compose, terraform placeholder
```

The point of the split: **the model provider, the database, and the web framework are all
replaceable behind boundaries.** Routes never write SQL (they call repositories); nothing outside
`model_gateway` knows which LLM is used; nothing outside `db` knows the table layout. This is the
"provider-independent interfaces" idea from Lessons 02 and 09 made concrete.

### 4.2 The three ways to analyze a ticket (memorize this — it's the core of the design)

| Path | Endpoint | Speed | Fails how? | Purpose |
|---|---|---|---|---|
| **Baseline** | `POST /tickets/{id}/baseline-analysis` | instant, free | can't fail | the **yardstick** — proves the AI is worth paying for |
| **Sync AI** | `POST /tickets/{id}/ai-analysis` | 2–10 s, blocks | HTTP error to caller | simple, good for testing |
| **Async AI** | `POST /tickets/{id}/analyze` → `202` | returns instantly | recorded on the job sheet | what the real UI uses |

The **async path** is the grown-up one:

```
POST /analyze
  1. write an ai_runs "job sheet" row (status=pending)   <- DB first, then queue
  2. push only the run_id onto the Redis queue           <- not the ticket text
  3. return 202 Accepted with the job sheet
  ...worker...
  4. worker pulls the id, marks running, calls the LLM
  5. state -> succeeded | abstained | failed  (all written to the row)
  6. web page polls GET /analysis until the status changes
```

**Two details interviewers love here:**
- *DB row before queue push.* If the process crashes after queueing but before writing, the worker
  would hold an ID for a row that doesn't exist. Writing the row first means a lost job is at worst
  a visible `pending` row someone can retry. (`routes/tickets.py`, `enqueue_ticket_analysis_endpoint`)
- *Only the ID travels on the queue.* The worker re-reads current data from the DB, so it never acts
  on a stale copy, and the queue stays tiny.

### 4.3 Request lifecycle (every request)

```
web/app.js click
  -> route in apps/api/supportops_api/routes/*.py
       -> dependencies.py: get_current_actor (who?) + get_db_session (tools)
            -> repositories/*.py run the SQL (always filtered by tenant_id)
            -> model_gateway/* talks to the LLM (AI paths only)
            -> observability/* logs, counts, traces, records cost
       -> hand-written converter -> Pydantic *Read schema -> JSON out
```

---

## 5. Concept deep-dives (what / why / where)

### 5.1 Structured output & the three anti-hallucination defenses
**What:** the LLM must return JSON matching `FullTicketAnalysis`, not prose.
**Why:** prose ("this looks like a billing issue, maybe delivery") can't be stored in a column,
counted, or acted on. Structure makes results machine-usable *and* checkable.
**Where:** `packages/prompts/schemas.py`, `packages/model_gateway/providers/hosted.py`.
**The three defenses (say all three):**
1. **Constrain at generation** — request sends `text.format = {type: json_schema, strict: true,
   schema: FullTicketAnalysis.model_json_schema()}`. The provider enforces the shape while generating.
2. **Validate on arrival** — `FullTicketAnalysis.model_validate_json(...)` re-checks it. Defense in
   depth: never trust a remote system validated on your behalf when the output faces customers.
3. **Evidence checking** — the model must cite where each conclusion came from; `_validate_evidence_ids`
   rejects any citation outside the four sources actually supplied (`ticket-subject`, `ticket-body`,
   `customer-id`, `policy-context`). A fabricated citation means the model is confabulating, so the
   whole response is rejected.

Supporting schema choices: `Literal` types (fixed vocabularies → countable), `extra="forbid"` (an
invented field is a hard failure), and explicit `abstain` / `missing_information` (an honest "I don't
know" instead of a forced guess).

### 5.2 Abstention (honest uncertainty)
**What:** the model can decline to answer.
**Why:** a model *asked* for a category will always produce one — even for a ticket that just says
"help". A confident wrong answer is worse than an admission of uncertainty, because nobody
double-checks it. Treating "I don't know" as a *failure* would push you toward models that always
guess — exactly wrong for drafting customer replies.
**Where:** `schemas.py` (`abstain: bool`), `worker/jobs.py` records a distinct `abstained` state —
neither success nor failure. The recommendation and cost are still saved; the outcome is labeled
honestly so quality metrics aren't inflated.

### 5.3 The deterministic baseline (the yardstick)
**What:** a no-AI keyword/regex classifier producing the *same shape* as the AI.
**Why:** "is the AI worth it?" needs a *compared-to-what*. The honest comparison isn't against
nothing — it's against the simplest thing that works. Free, instant, never fails.
**Where:** `packages/domain/services/baseline.py`. Three jobs: (1) the `/baseline-analysis`
comparison endpoint, (2) the **pilot gate** — it classifies the ticket *before* deciding if the AI
may run (you can't ask the AI what a ticket is about to decide whether to pay for asking the AI),
(3) the **mock provider's brain** so tests run with no API key.
Key detail: **category order = priority order** — `security` is checked first, so "account hacked
and charged twice" is treated as security, not billing. The rule: *when a ticket could be two
things, treat it as the one where being wrong costs the most.* Its keyword weakness ("cancel"
matches "I do NOT want to cancel") is exactly what the LLM is meant to fix — which makes it a fair
baseline, not a straw man.

### 5.4 Evaluation harness & release gates
**What:** fixed datasets with known answers, scored *before* shipping.
**Why:** without it, "we improved the prompt" is an opinion. Human review is the truest signal but
slow and only tells you *after* customers are affected.
**Where:** `packages/evals/`. Three datasets: `golden` (accuracy), `safety` (adversarial/injection),
`difficult` (ambiguous, mined from rejected drafts).
**Metrics:** category accuracy, **macro-F1** (each category weighted equally, so a "classify
everything as billing" model is exposed), field precision/recall, escalation precision/recall
(recall matters most — missing a fraud escalation is harmful), unsupported-claim rate, safety pass
rate, draft rubric, p95 latency.
**Gates (the philosophy in one line — "accuracy may be imperfect, safety may not"):**
- Universal, must be **zero**: invalid structured output; unsupported claims.
- Per-dataset: golden accuracy ≥ 0.80; **safety pass rate = 1.0**.
CI fails the build on any gate failure, turning "we should be careful" into something enforced.

### 5.5 Prompt versioning
**What:** prompts are versioned artifacts, not strings in code.
**Why:** *a prompt is the program* for an AI feature — change a sentence and every answer changes.
So it gets a name, a version, a declared output shape, and a changelog. The `prompt_version`
(`full_ticket_analysis.v1`) is stored on every recommendation, so when approval rates drop next
month you know exactly which instructions produced the bad results.
**Where:** `packages/prompts/registry.py`. The output schema is generated *from* the Pydantic class
and embedded in the prompt, so "what we ask for" and "what we validate" cannot drift.

### 5.6 Multi-tenancy & authorization
**What:** many customer companies share one database; every row carries `tenant_id`.
**Why:** shared-DB multi-tenancy is cheaper than a DB per customer, but isolation is only as good as
the discipline of *always* filtering by tenant. So repositories take `tenant_id` as a **required**
argument, and `tenant_id` always comes from the verified `Actor`, never from caller-supplied body data.
**Where:** `dependencies.py` (`Actor`, `get_current_actor`, `require_role`), every repository, every
route. Cross-tenant reads return **404, not 403** — replying "exists but not yours" would confirm a
competitor's ID is real.
**Auth honesty:** identity arrives as trusted headers (`X-Tenant-Id`, `X-User-Id`, `X-Role`) set by
an API gateway that does the real login. This service must never face the public internet directly —
documented in `docs/threat-model.md`. RBAC roles: `agent`, `lead`, `admin`, `service`; policy writes
require `lead`/`admin`.

### 5.7 Idempotency
**What:** sending the same ticket twice has the same effect as once.
**Why:** upstream helpdesks retry on lost replies; without this every retry makes a duplicate.
**Where:** two layers — `routes/tickets.py` checks for an existing `external_id` and returns it with
**200 (not 201)**; and a DB `UniqueConstraint(tenant_id, external_id)` holds the line even under a race.

### 5.8 Cost tracking
**What:** every AI call writes a `cost_events` row (tokens in/out, estimated USD, latency, provider,
model, prompt version, operation).
**Why:** makes "is this feature worth what we pay?" answerable, not an opinion. Input/output tokens
are separate because output is priced higher. Cost is always attributable to a tenant.
**Where:** `observability/model_usage.py`, `models.py::CostEvent`, `GET /metrics/costs`,
`docs/cost-report.md`. `estimated_cost_usd` is honestly labeled *estimated* (tokens × configured
rate, not an invoice) and stored as float — fine for reporting, *wrong* for real billing (you'd use
a decimal type).

### 5.9 Observability
**What:** structured JSON logs with a request/correlation ID, Prometheus metrics, trace spans, all
carrying tenant/ticket/run IDs.
**Why:** you must be able to follow one ticket through the API, the queue, and the worker; and
business outcomes (approval rate, cost per accepted draft) must sit beside infra metrics.
**Where:** `packages/observability/`, `/metrics/runtime` (Prometheus text), Grafana dashboard in
`infra/grafana`. Logs **redact PII/secret patterns** before emission; the input hash is logged
instead of the ticket text.

### 5.10 The pilot kill-switch
**What:** `AI_ANALYSIS_ENABLED` (master), `AI_ANALYSIS_ENABLED_TENANTS`, `AI_ANALYSIS_ENABLED_CATEGORIES`.
**Why:** roll a risky feature out to a few tenants/categories first, and turn it off instantly during
an incident. Checked in **both** the API (before enqueue) *and* the worker (after dequeue) — so a job
that sat in the queue while you flipped the switch off still won't run. That double-check is what
makes the kill-switch *actually* immediate.
**Where:** `apps/api/supportops_api/pilot.py`, re-used by `worker/jobs.py`.

### 5.11 Error taxonomy (why one call has three catches)
The sync AI endpoint maps failure *type* to HTTP *code*:
- config error / unknown provider → **503** "not configured" (our fault, retry later)
- request error / timeout → **503** "unavailable" (couldn't reach it)
- response error / bad JSON / refusal → **502** "invalid output" (they answered badly; retrying won't help)

The worker catches them all in one place instead — because *nobody is waiting*, so there's no HTTP
code to choose; every failure is written to the job sheet with a stable `error_code` (for counting)
plus `error_message` (for humans). Provider exceptions never leak httpx types past `model_gateway` —
that translation at the boundary keeps the HTTP library out of routes and workers.

---

## 6. Data model (7 tables)

```
Tenant (a customer company) — root of everything
 ├── User               people at that company (role: agent/lead/admin/service). No passwords —
 │                       identity is trusted from the gateway.
 ├── TenantPolicy        the company's written rules fed to the AI as policy_context
 └── Ticket             a customer's support request (the product's center)
      ├── AIRun          job sheet for one async analysis; state machine + failure record
      ├── TicketRecommendation   what an analysis concluded + the draft reply (append-only)
      │    └── RecommendationReview   a human's verdict: approved/edited/rejected (write-once)
      └── CostEvent      what an AI call cost (tokens, money, latency)
```

**Points worth reciting:**
- **UUID primary keys** — generatable anywhere (API, worker, test) without a DB round-trip, and they
  leak no volume information (ticket #4317 tells a competitor how many tickets exist; a UUID doesn't).
- **`ondelete` is chosen per relationship.** Ticket→children: `CASCADE` (delete the ticket, delete
  its analysis). But `AIRun.output_recommendation_id` and `CostEvent.*` use **`SET NULL`** — the
  *record that a call happened and what it cost must outlive the text it produced.* Money that left
  the account shouldn't vanish from the books because retention cleaned up a draft.
- **Append-only history.** Recommendations and reviews are never overwritten. A supervisor who
  disagrees creates a *second* review, so the full decision history survives.
- **Indexes are deliberate.** Every table has an index on `tenant_id` (every query filters by it);
  composite `(tenant_id, status)` on tickets serves "this company's open tickets"; `ai_runs.status`
  alone serves the cross-tenant operational question "are any jobs stuck?".
- **JSON columns** (`metadata_json`, `extracted_fields_json`, `reasons_json`) for shapes not known in
  advance — flexible but not efficiently queryable, so only for "extra stuff", never for things you
  filter or sum.
- **Migrations are the source of truth**, not `models.py`. Editing the model without a migration
  (0001–0007) means the code expects a column the database doesn't have.

---

## 7. Design trade-offs (interviewers dig here — have an opinion on each)

| Decision | Chosen | Alternative | Why this one |
|---|---|---|---|
| One big analysis call vs 5 small prompts | one `full_ticket_analysis` call | 5 step prompts (still in registry) | one call sends the ticket once → ~5× cheaper input + one round-trip; the 5 remain for debuggability |
| Structured output enforcement | provider strict mode **+** local re-validate | trust one or the other | defense in depth; the output faces customers |
| Baseline classifier kept in an AI product | yes | delete it | it's the yardstick, the pilot gate, and the test brain — three jobs |
| Shared-DB multi-tenancy | one DB, `tenant_id` everywhere | DB per tenant | cheaper/simpler; isolation enforced by required `tenant_id` args |
| Cross-tenant access response | 404 | 403 | 403 confirms the ID exists |
| Cost as float | float, labeled "estimated" | decimal | fine for reporting; you'd switch to decimal for real billing |
| Abstain as its own state | yes | success or failure | scoring it either way distorts quality metrics |
| Sync vs async AI | both, async for UI | only one | teaches the trade-off; async is production-correct |
| Queue carries only the run ID | yes | carry the ticket payload | small queue + always-fresh data |
| DB row before queue push | yes | queue first | a lost job is a visible `pending` row, not a phantom ID |
| Kill-switch re-checked in worker | yes | check only at API | makes rollback actually immediate for queued jobs |

---

## 8. Q&A bank

### Product / applied AI
**Q: What problem does this solve?**
Support agents spend time triaging and drafting. The copilot does a first pass — category, priority,
extracted details, draft reply — and a human approves it. It's *decision support*, not automation:
every draft is reviewed.

**Q: How do you know the AI is actually helping?**
Approval/edit rates from `recommendation_reviews`, compared against the free baseline by `source`,
plus cost per accepted draft. The pilot report (`/metrics/pilot`) computes acceptance, edit distance,
time-to-first-response, escalation accuracy, and an exit decision.

**Q: Why require human approval at all?**
The model drafts customer-facing text and can be wrong or manipulated. Human-in-the-loop keeps a
person accountable for anything sent, and the reviews are also the truest quality signal.

### LLM integration
**Q: How do you stop the model returning garbage?**
Strict JSON-schema output + local Pydantic re-validation + evidence-ID checking + `extra="forbid"`.
Anything off-contract is rejected as a `ModelProviderResponseError`, mapped to 502.

**Q: What's the evidence-ID check?**
The model cites which of the 4 supplied inputs each conclusion came from. Citing anything else means
it invented a source → reject the whole response. Anti-hallucination.

**Q: How do you handle a refusal vs a timeout vs bad JSON?**
Distinct paths: refusal and bad JSON are *response* errors (502, retry won't help); timeouts and
unreachable service are *request* errors (503, retry later); missing API key is a *config* error (503).

**Q: How would you add a second provider (e.g., Anthropic)?**
Add a provider class implementing the `TicketAnalysisProvider` contract in `model_gateway/providers/`,
register it in `routing.py`. Nothing else changes — routes/worker only know the contract. (I'd also
build the request against that provider's structured-output API and reuse the same schema.)

### Evaluation
**Q: Why macro-F1 and not accuracy?**
Accuracy is gamed by class imbalance — 90% billing tickets means "always say billing" scores 90%
while being useless on security. Macro-F1 weights each category equally and exposes that.

**Q: Why is the safety gate 1.0 but accuracy 0.80?**
Accuracy is allowed to be imperfect; safety isn't. One reply falsely promising a refund is one
customer told something untrue — no aggregate makes that acceptable.

**Q: How do evals run without paying for the LLM?**
CI uses `MODEL_PROVIDER=mock`; the mock wraps the deterministic baseline, so CI is free and
reproducible. Hosted eval is a separate, opt-in run.

### Backend / data
**Q: Walk me through the async path.** — see §4.2.
**Q: Why UUIDs?** — generatable anywhere, leak no counts (§6).
**Q: CASCADE vs SET NULL?** — children cascade with the ticket; cost/run records SET NULL so financial
and audit history outlives deleted drafts (§6).
**Q: How is idempotency guaranteed?** — app-level check returns 200 + DB unique constraint under races (§5.7).

### Security
**Q: Biggest risks and mitigations?**
Prompt injection (untrusted ticket text is delimited and never placed above instructions; injection
is a scored safety dataset); excessive agency (the model returns data only — it can't choose tools or
permissions, and `extra="forbid"` blocks smuggled fields); cross-tenant leakage (required `tenant_id`
filtering, 404 on foreign IDs); PII in logs (redaction; hash instead of text); secret leakage (API
key never logged; error bodies truncated to 500 chars).

**Q: Why trust identity headers?**
An API gateway authenticates and sets them; this service sits behind it, never on the public internet.
It's a documented boundary decision (`threat-model.md`), not an oversight.

### Operations
**Q: How do you roll back a bad prompt?**
Prompts are versioned and shipped in the API image; roll back to the image with the last-good prompt
registry. Broader controls in `docs/rollback-runbook.md`: app-image pin, `MODEL_PROVIDER=mock` for a
model incident, `AI_ANALYSIS_ENABLED=false` for an AI-specific incident.

**Q: How do you trace one ticket end-to-end?**
`log_context`/`trace_span` attach tenant/ticket/run IDs to every log line and span from API through
worker, so you filter by ticket ID and see the whole story.

---

## 9. Honest gaps (say these *before* they're asked — it reads as maturity)

- **No RAG / embeddings.** "Policy context" is a plain DB fetch. Retrieval is a separate track.
- **No fine-tuning / post-training.** Pure prompt + structured output on a hosted model.
- **No live tool execution / MCP.** The "workflow" is the analysis state machine, not an agent that
  acts on external systems.
- **No LLM-as-judge.** Eval scoring is rule/keyword-based — cheap and deterministic, but the draft
  rubric is a crude proxy ("Thanks, I'll review this" scores 1.0). Human approval is the real signal.
- **Retention is a non-destructive stub** — it counts candidates and logs; it doesn't delete yet
  (deliberate, to avoid irreversible deletion in a learning build).
- **Cloud deploy is staging-shaped**, not a real cloud footprint; Terraform is a placeholder.
- **Cost is float/estimated**, not billing-grade decimal.
- **Streaming isn't implemented** for the model call (structured single response instead).

Each of these is a *scoping* choice, not a bug — and each is the natural "what would you do next."

---

## 10. Glossary

- **Tenant** — one customer company; the isolation unit. Every row carries `tenant_id`.
- **Actor** — the verified caller (tenant + user + role) built from request headers.
- **Baseline** — the deterministic keyword classifier; the comparison yardstick.
- **Recommendation** — one analysis result (baseline or AI) + optional draft reply.
- **Review** — a human verdict on a recommendation: approved / edited / rejected.
- **AIRun** — the async job sheet; drives `pending → running → succeeded/abstained/failed`.
- **Abstain** — the model honestly declining; a distinct outcome, not a failure.
- **Evidence IDs** — the model's citations of which supplied input backed each conclusion.
- **Gate** — an automatic release blocker in the eval harness (zero unsupported claims, 100% safety…).
- **Pilot switch** — env-var kill-switch scoping the AI by tenant/category, checked in API *and* worker.
- **Cost event** — a per-call record of tokens, estimated USD, latency, provider, model, prompt version.
- **Idempotency** — same request twice = same effect once (via `external_id` + unique constraint).
- **Provider / model gateway** — the swappable boundary to the LLM; the rest of the app is provider-agnostic.

---

### Fast pre-interview checklist
1. Recite the 30-second pitch and the three analysis paths.
2. Name the three anti-hallucination defenses.
3. Explain macro-F1 and the 0.80-vs-1.0 gate asymmetry.
4. Explain CASCADE vs SET NULL and why UUIDs.
5. Explain why the kill-switch is re-checked in the worker.
6. Volunteer two honest gaps and what you'd build next (RAG and LLM-judge evals are good picks).
