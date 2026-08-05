# Phase 01 - LLM Gateway

## 1. Phase Purpose

Phase 01 builds the LLM Gateway for the Atlas AI Platform.

The LLM Gateway is the single controlled entry point for every model call in the platform. After this phase, no other module is allowed to talk to an LLM provider, an embedding provider, or a local inference server directly.

The blueprint states the rule directly:

```text
No package should secretly call an LLM provider directly.
All model calls must go through model_gateway.
```

Phase 00 built the engineering foundation: repository layout, typed settings, structured logging, request ids, error envelope, database session, Alembic migrations, worker skeleton, Docker Compose, and tests. Phase 00 deliberately created an empty `packages/model_gateway` placeholder and reserved AI error categories such as `ai_provider_error` and `ai_output_invalid`.

Phase 01 fills that placeholder.

The purpose of Phase 01 is to make model access:

- Centralized, so there is one code path to review, test, and secure.
- Routable, so each use case can pick a different provider and model.
- Observable, so every call produces an `ai_runs` record with tokens, cost, and latency.
- Reliable, so timeouts, retries, and fallbacks are policy, not accident.
- Testable, so the whole platform can be tested without a real provider key.
- Governable, so tenant data policy can block a route before any bytes leave the system.

This phase is the difference between "the app can call an LLM" and "the company can operate an LLM".

## 2. Source Documents Used For This Phase

This document is derived from the Atlas documentation set in this folder. A few designs are Phase 01 originals that the set implies but never specifies — the circuit breaker, request-hash canonicalization, the SSRF controls on `base_url`, the stale-run sweep, and the error code catalogue. Each is argued where it appears.

| Source Document | What Phase 01 Takes From It |
|---|---|
| `00-Atlas-Documentation-Map.md` | Phase list, standard learning-phase structure, MVP execution order, current implementation status |
| `01-Atlas-Technical-Master-Blueprint.md` | §5 repository structure, §8 configuration, §9 request lifecycle, §10.4 AI operations domain, §11.5 prompt and model tables, §13.7 model gateway APIs, §15 model gateway design |
| `02-Atlas-Coverage-Matrix.md` | Which gateway topics belong to Phase 01 versus Phase 20 |
| `03-Atlas-Visual-Architecture-Diagrams.md` | Component and sequence placement of the gateway |
| `04-Atlas-Database-Schema-Specification.md` | Exact columns, constraints, indexes, migration order, deferred foreign keys for `model_providers`, `model_routes`, `ai_runs`, `cost_records` |
| `05-Atlas-Standards-Crosswalk.md` | OWASP LLM Top 10 mapping, AISVS mapping, OpenTelemetry GenAI attribute names |
| `06-Atlas-Implementation-Tickets.md` | Tickets P01-001 through P01-010 and their acceptance proofs |
| `07-Atlas-Model-Routing-And-Provider-Examples.md` | Provider registry examples, route examples, route selection algorithm, rejection examples, promotion checklist |
| `08-Atlas-Frontend-UX-Specification.md` | Models screen tabs and AI Runs detail fields |
| `10-Atlas-Operations-Runbooks.md` | Provider outage runbook and cost spike runbook |
| `learning-phases/phase-00-engineering-foundation.md` | The foundation this phase is allowed to assume |

## 3. What This Phase Builds

By the end of Phase 01, the platform should have:

- A `model_providers` table describing which providers exist, what they can do, and what data policy they carry.
- A `model_routes` table describing which model answers which use case, with limits, budgets, and fallback.
- An `ai_runs` table recording every model call attempt with status, usage, cost, latency, and trace id.
- A `cost_records` table recording billable line items per run.
- A provider adapter interface that every provider implements.
- At least one real managed provider adapter, disabled by default and enabled by environment flag.
- A mock/fake provider adapter that can simulate success, invalid output, timeout, rate limit, and unavailability.
- A router that selects a route by use case, tenant, capability, data policy, and budget.
- A gateway client that validates the request, selects a route, calls the provider, records the run, and returns a normalized response.
- Timeout, retry with backoff, and fallback policy.
- Token usage capture and cost estimation from a versioned pricing sheet.
- Structured logs and GenAI span attributes for each call.
- Internal API endpoints for chat, embed, route listing, and AI run lookup.
- Tests that cover the whole gateway without any real provider key.

Phase 01 is complete only when a developer can issue a model request, get a normalized response, and open the resulting `ai_runs` record showing provider, model, route, tokens, cost, latency, and trace id.

## 4. What Phase 01 Assumes From Phase 00

Phase 01 does not rebuild foundation work. It assumes Phase 00 delivered:

| Foundation Item | How Phase 01 Uses It |
|---|---|
| Typed settings via Pydantic settings | Provider keys, timeouts, cost limits, feature flags |
| Structured JSON logging | Model call logs with stable field names |
| Request id middleware and request context | Correlating an API request to an `ai_runs` row |
| Error envelope `{error: {code, message, details, request_id}}` | Uniform gateway failure responses |
| Reserved AI error classes (`AIProviderError`, `AIOutputValidationError`, `SafetyBlockedError`) | Gateway error mapping |
| SQLAlchemy engine, session factory, and request-scoped session dependency | Persisting runs and reading routes |
| Alembic migration chain starting from the foundation migration | Adding the four Phase 01 tables |
| `tenants` and `users` tables | Tenant ownership of routes, runs, and costs — **see 4.1, this is not currently a Phase 00 deliverable** |
| Worker skeleton | Later batch and embedding jobs, not required to run in Phase 01 |
| pytest layout with unit and integration folders | Gateway unit tests, contract tests, migration tests |
| Empty `packages/model_gateway` package | The home for all Phase 01 code |

If any of these is missing, finish Phase 00 first. Building a gateway on a weak foundation produces a gateway that cannot be traced, tested, or rolled back.

### 4.1 Blocking Prerequisite: The Identity Tables

One row in the table above is not actually safe to assume, and it blocks Phase 01 entirely. It is recorded here in the style of Section 19.2: state the conflict, choose a resolution, write a decision record.

The conflict:

| Document | Position |
|---|---|
| `04-Atlas-Database-Schema-Specification.md` §4.1 | `002_create_identity_tables` precedes `004_create_prompt_and_model_tables` |
| `04-…` §7.1 and §7.3 | `ai_runs.tenant_id` and `cost_records.tenant_id` are `not null references tenants(id)` |
| `01-Atlas-Technical-Master-Blueprint.md` §3.5 | "Every user-visible object must belong to a tenant", and AI runs are named explicitly |
| `02-Atlas-Coverage-Matrix.md` §6 | Tenant isolation is listed from Phase 00 onward |
| `learning-phases/phase-00-engineering-foundation.md` §24.1 | "it is also acceptable for Phase 00 to only prove migration infrastructure exists", and identity tables may "wait for tenant/user tables in the auth phase" |
| `06-Atlas-Implementation-Tickets.md` P00-006 | Names only SQLAlchemy engine, session, and Alembic — no identity tables |

So Phase 00, as written, may legitimately end with no `tenants` table. Phase 01's `ai_runs` migration then cannot apply, and ticket P01-001's acceptance proof — "migration applies cleanly" — is unachievable.

Resolution required before Phase 01 coding starts. Pick one:

**Option A, recommended.** Add a minimal `tenants` and `users` migration to Phase 00's done criteria, making `002_create_identity_tables` real and matching the canonical migration order. This is a small amount of work — two tables with no authentication logic attached — and it removes the contradiction with blueprint §3.5 and the coverage matrix. Phase 00's §24.1 already permits this reading; it simply does not require it. Full user management, authentication, RBAC, and API keys remain out of scope and stay in the auth phase, which is what Phase 00's "avoid building too early" list actually warns against.

**Option B.** Insert an explicit Phase 00a identity foundation phase between Phase 00 and Phase 01, delivering the same two tables. Cleaner if Phase 00 is considered frozen; costs an extra phase document.

**Not acceptable.** Making `ai_runs.tenant_id` nullable to sidestep the dependency. That contradicts the schema specification, breaks tenant scoping on every query in Section 34.2, and makes the cross-tenant tests meaningless.

Until this is resolved, treat Phase 01 as blocked rather than starting and discovering it at Step 3. Section 34.4 covers the related but separate question of when *tenant-scoped routes* become usable, which additionally depends on membership and RBAC.

## 5. Beginner-Friendly Definition Of A Model Gateway

A model gateway is a piece of backend code that sits between your application and every AI model provider.

Without a gateway:

```text
route A -> OpenAI SDK
route B -> OpenAI SDK with different settings
worker  -> another SDK
script  -> raw HTTP call
```

Four places to change when a model is renamed. Four places to add retries. Four places that might log a secret. No single place that knows what the platform spent today.

With a gateway:

```text
route A ->
route B ->  model_gateway.client -> router -> provider adapter -> provider
worker  ->
script  ->
```

One place that:

- Validates the request.
- Chooses the model.
- Applies timeouts and retries.
- Counts tokens.
- Estimates cost.
- Writes an audit record.
- Hides provider differences from the rest of the code.

A useful mental image: the gateway is the platform's airport control tower. Planes are model calls. The tower decides which runway each plane uses, refuses flights that violate policy, records every departure and arrival, and reroutes traffic when a runway closes.

## 6. Real Industry Example

A support team asks two questions about the same AI feature.

Question 1: "Why did last month's model bill triple?"

Without a gateway, the honest answer is "we do not know". The provider dashboard shows a total. It cannot tell you which tenant, which feature, which prompt, or which retry loop caused it.

With a gateway, the answer is a query:

```text
group ai_runs by tenant_id, use_case, model_name, created_at day
sum estimated_cost_usd
compare input_tokens, output_tokens, reasoning_output_tokens
count retries and failed runs
```

Question 2: "The provider is down. Can we keep serving customers?"

Without a gateway, every call site fails independently and the team edits code under pressure.

With a gateway, an operator changes one route's status to disabled, the router falls back to the configured fallback route, and the runbook validation steps confirm recovery.

The gateway is what turns a demo into something a business can answer questions about.

## 7. What You Must Understand Before Coding

These definitions are the vocabulary of the rest of this document.

### 7.1 Provider

A provider is a service that runs models. Examples used in the routing document: a managed API provider, an enterprise private deployment, and a local open-model server.

In Atlas, a provider is a database row in `model_providers` with a stable `name`, a `provider_type`, an optional `base_url`, a capability matrix, and a data policy.

### 7.2 Provider Type

`provider_type` describes the wire protocol, not the company. The schema specification lists: `openai_compatible`, `anthropic_compatible`, `azure_openai`, `local_vllm`, `local_tgi`, `mock`.

Two different vendors that both speak the same protocol can reuse one adapter.

### 7.3 Provider Adapter

An adapter is the Python class that translates Atlas's internal request into a provider's wire format and translates the provider's response back.

The blueprint defines the logical interface:

```text
chat(request) -> ChatResponse
structured(request, schema) -> StructuredResponse
embed(request) -> EmbeddingResponse
rerank(request) -> RerankResponse optional
```

Phase 01 implements `chat` and `embed`. `structured` is defined but implemented in Phase 03. `rerank` is optional and belongs to Phase 06.

### 7.4 Use Case

A use case is the reason for a model call, not the model name. The blueprint lists examples:

```text
rag_answer
query_rewrite
structured_extraction
agent_planning
agent_verification
embedding
safety_check
llm_judge
```

Ticket P01-005 requires routing for five use cases, which it names as "chat, classifier, rag_answer, embedding, judge".

Callers ask for a use case. Callers do not ask for a model. This is the core inversion of the gateway.

#### Canonical Use-Case Vocabulary

`use_case` is a stored routing key, so it cannot have three spellings. The source documents currently disagree:

| Concept | `06-…-Implementation-Tickets.md` P01-005 | `04-…-Database-Schema-Specification.md` §6.2 | `07-…-Model-Routing-And-Provider-Examples.md` §3 |
|---|---|---|---|
| Classification | `classifier` | not listed | `classification` |
| Judging | `judge` | `judge` | `llm_judge` |
| Chat | `chat` | `chat` | not shown |
| Grounded answer | `rag_answer` | `rag_answer` | `rag_answer` |
| Embedding | `embedding` | `embedding` | `embedding` |

This document adopts the routing document's spellings, because that document is the one that defines concrete route configuration and is therefore the closest thing the set has to a route registry:

```text
chat
classification
rag_answer
embedding
llm_judge
```

Treat `classifier` and `judge` as historical aliases appearing in the ticket and schema documents. This is the same reconciliation pattern used for token names in Section 16.5.

Whichever set the documentation owner ratifies, it must be ratified once and reflected in the tickets, the schema examples, and the route configuration together. A `use_case` mismatch between configuration and calling code produces `ai.route_not_found` at runtime with no compile-time warning.

### 7.5 Route

A route is a stored decision that binds a use case to a provider, a model name, and a set of limits. Routes live in `model_routes`.

A route carries: priority, token caps, temperature, timeout, fallback, caching flags, batch flags, embedding dimension, reasoning settings, cost ceiling, data policy flag, and status.

### 7.6 Route Key

`route_key` is the stable configuration name of a route, such as `rag_answer_primary` or `classification_private`. Configuration files refer to routes by `route_key`. The database stores identity as `route_key` and links fallback by `fallback_route_id`.

The routing document states the loader rule explicitly:

```text
Bootstrap YAML/JSON may use fallback_route_key, then the loader resolves it to fallback_route_id.
```

### 7.7 Fallback Route

A fallback route is the route to try when the primary route cannot serve the request. Fallback is a policy decision, not an automatic behavior. The private route example sets `fallback_route_key: null` because silently downgrading a private route to a public provider would be a data-policy violation.

### 7.8 Token

A token is the unit a model reads and writes. Roughly a word fragment. Providers bill per token and enforce context limits in tokens.

Atlas tracks five token families in `ai_runs`:

```text
input_tokens
output_tokens
reasoning_output_tokens
cache_creation_input_tokens
cache_read_input_tokens
```

### 7.9 Context Window

The context window is the maximum number of tokens a model can consider in one request. Routes express their own tighter caps with `max_input_tokens` and `max_output_tokens`, which may be lower than the model's physical limit for cost reasons.

### 7.10 Temperature

What temperature actually does to the probability distribution, and why `0.0` is still not deterministic, is Section 8.4.

Temperature controls randomness. The route examples use `0.0` for classification and judging, and `0.2` for RAG answers. Deterministic tasks should not be creative.

### 7.11 Finish Reason

The finish reason explains why generation stopped: completed normally, hit the output cap, was filtered, or called a tool. The blueprint lists `finish_reason` as a required gateway response field. Truncated output that is treated as complete output is a classic silent bug.

### 7.12 Timeout

A timeout is the maximum wall-clock time the gateway waits for a provider. Routes carry `timeout_seconds`. The route examples range from 8 seconds for a cheap classifier to 120 seconds for media generation.

### 7.13 Retry, Backoff, And Jitter

A retry re-sends a failed request. Backoff increases the wait between attempts. Jitter randomizes that wait so many clients do not retry in lockstep.

The cost runbook names the fix for retry storms:

```text
Add exponential backoff, jitter, max retry cap, and circuit breaker.
```

### 7.14 Circuit Breaker

A circuit breaker stops calling a provider that is clearly failing, waits, then allows a probe call. It prevents Atlas from making a provider outage worse and prevents queues from filling with doomed requests.

### 7.15 Idempotency

Idempotency means repeating a request does not repeat its effect. The blueprint requires idempotency for jobs and side effects. In Phase 01 the relevant rule is narrower: a retry inside one gateway call must not create a second `ai_runs` row. One logical model request equals one run record, with attempts recorded inside it.

### 7.16 Request Hash

`request_hash` in `ai_runs` is a normalized hash of the request. It groups identical requests without storing their content, which supports duplicate detection, cache work in Phase 20, and debugging without exposing user data.

### 7.17 Redaction

Redaction is removing or masking sensitive content before storage or logging. Phase 00 already forbids logging secrets and raw private documents. Phase 01 extends that to `input_preview`, `output_preview`, `request_json`, and `response_json`.

### 7.18 Capability Matrix

A capability matrix is the list of features a provider actually supports. The blueprint lists fields including `supports_chat`, `supports_structured_output`, `supports_streaming`, `supports_tool_calling`, `supports_prompt_caching`, `supports_batch_api`, `supports_reasoning_controls`, `supports_embeddings`, `max_context_tokens`, `max_output_tokens`, `data_retention_policy`, and `region_support`.

The purpose is stated plainly: the matrix "prevents accidental use of unsupported features and helps explain routing decisions".

### 7.19 Data Policy And Restricted Data

A data policy records whether a provider may receive sensitive content, whether the provider may train on it, which region it runs in, and how long it retains data.

`restricted_data_allowed` appears on both providers and routes. A request marked as restricted may only use a route that allows restricted data.

### 7.20 AI Run

An `ai_run` is the durable record of one model request. It is the platform's proof that a model call happened, what it cost, how long it took, and whether it succeeded.

Blueprint principle 3.3 makes this non-optional:

```text
No AI capability is complete unless it can be measured.
```

### 7.21 Trace Id

A trace id connects work across API request, gateway call, worker job, and later retrieval and agent steps. `ai_runs.trace_id` is indexed for this reason.

### 7.22 Reasoning Tokens

Some models spend extra tokens on internal reasoning. Routes may enable reasoning with `reasoning_enabled`, `reasoning_effort`, and `reasoning_budget_tokens`. Usage is recorded as `reasoning_output_tokens`.

Phase 01 stores and enforces these fields. Deciding when reasoning is worth its cost is Phase 20 work.

### 7.23 Prompt Cache Tokens

Section 8.5 explains the mechanism, and therefore why only a stable prefix can be cached.

Providers that support prompt caching report how many input tokens were written to cache and how many were read from cache. Atlas stores them as `cache_creation_input_tokens` and `cache_read_input_tokens`.

Phase 01 stores these fields when a provider returns them. Designing cacheable prefixes is Phase 20 work.

## 8. Concepts You Cannot Learn From The Code

Section 7 was vocabulary. This is mechanism.

None of it appears in a file, a test, or a migration. You can implement Phase 01 correctly and still not know why the first token takes 400 ms and the next forty take 40 ms each, or why p95 collapsed while p50 barely moved. It belongs to this phase because the gateway is where these forces become visible, and later phases assume you have it.

Read it before Step 1, and again after Step 17 when you have a baseline to look at.

### 8.1 Prefill And Decode

A model call has two phases with different performance characteristics.

**Prefill** reads your whole prompt in one parallel pass. Cost scales with input length.
**Decode** generates output one token at a time, each pass attending to everything before it. Sequential, and it dominates wall-clock time.

```text
request ──▶ [ PREFILL: 3,000 input tokens, one parallel pass ] ──▶ first token
              [ DECODE: 400 sequential passes, one per token  ] ──▶ final token
```

Three consequences:

- `time_to_first_chunk_ms` is its own column because it measures prefill. Slow first token means a long prompt or a queue. Slow tokens *after* the first means a loaded model.
- Output tokens are priced above input tokens everywhere, often several times. Not vendor greed — prefill is parallel and cheap per token, decode is sequential and expensive.
- Latency ≈ `prefill + (output_tokens × time_per_token)`. So capping `max_output_tokens` is a latency control as much as a cost control, and Section 22.2's clamp-don't-reject rule strictly improves latency.

### 8.2 Tokenization

Models read tokens produced by a subword algorithm, usually byte-pair encoding. BPE merges frequent adjacent byte pairs into a vocabulary of fragments: common words become one token, rare words shatter.

```text
"the"          -> 1 token
"tokenization" -> "token" + "ization" -> 2 tokens
"Þórshöfn"     -> 5-8 tokens
"1234567"      -> several; digits group oddly
```

- The 4-chars-per-token heuristic in Section 26.2 is an English-prose average. Code, JSON, and non-Latin scripts break it. A Hindi or Japanese document can cost 2–3× its English translation — meaning non-English tenants cost more to serve for identical work. That is a pricing question, not a footnote.
- Model families use different tokenizers, so the same string is a different token count per provider. You cannot precompute one number correct for every route.
- Hence Section 26.1's rule: an estimate never enters a usage column. The provider's tokenizer is the one that ran.

### 8.3 Context Windows Cost You Twice

The context window is a hard limit, but the limit is not the interesting part. Attention — each token considering every other — grows super-linearly with length. Doubling a prompt more than doubles prefill work.

So a long prompt costs twice: directly in billed input tokens, and indirectly in prefill latency, which the user experiences as "it hasn't started answering yet."

This is the mechanism behind the cost runbook's "tune top-k, chunk size, reranking cutoff", and why `max_input_tokens` is a first-class column the router filters on every request rather than a detail in `route_config_json`. Phase 06 will send this gateway 20,000-token RAG prompts; knowing the cost is doubled is what stops "retrieve more chunks" from becoming the default fix for every quality problem.

### 8.4 Sampling, And Why `temperature: 0.0` Is Not Deterministic

At each step the model produces a probability distribution over its vocabulary. Sampling picks from it.

- **Greedy / temperature 0** — always take the highest-probability token.
- **Temperature > 0** — flatten the distribution first; higher values raise the chance of unlikely tokens. This is what "creative" means.
- **Top-p (nucleus)** — keep the smallest set of tokens summing to *p*, sample within it. Cuts the nonsense tail without a rigid candidate count.

Hence Section 20.3's `0.0` for classification and judging, `0.2` for RAG answers: classification wants the argmax, answers want phrasing flexibility without invention.

But temperature 0 does not guarantee identical output. Floating-point addition is not associative and GPU kernels sum in nondeterministic order; your request is batched with strangers' requests, changing the arithmetic; mixture-of-experts models route differently depending on batch composition; and the provider may swap the model under a floating alias (Section 8.16).

```text
You cannot write assertEqual(model_output, expected_string).
```

That one fact is why Phase 07 exists, why the mock in Section 24.4 must be deterministic when the real thing is not, and why Section 35's tests assert on structure, status, and usage rather than generated text.

### 8.5 The KV Cache Behind Prompt Caching

During decode the model would otherwise recompute its representation of every earlier token at every step. Instead it caches those key/value tensors. Provider prompt caching extends this across requests: if your prompt starts with a prefix recently processed, prefill on that prefix can be skipped.

Every odd property of prompt caching follows from that:

| Behavior | Why |
|---|---|
| Only a **prefix** caches | Built left to right; changing token 5 invalidates everything after |
| Order matters enormously | Moving a variable forward destroys reuse for the whole remainder |
| Caches expire in minutes | Provider memory is finite and shared |
| Tiny prompts gain nothing | Lookup overhead exceeds the prefill saved — hence `cacheable_prefix_min_tokens` |
| Reads cheap, writes slightly above normal input | Small premium to populate, large discount to reuse |

This is why Section 15.5 tracks cache-creation and cache-read tokens separately, and why the blueprint puts instructions, policy, and tool schemas *before* the user question. Phase 20 designs those prefixes; Phase 01 only records the counts — but recording numbers you cannot interpret makes the Phase 20 work impossible to reason about.

### 8.6 Reasoning Tokens

Some models deliberate internally before answering. Those tokens are generated, billed, and counted against limits, but often not returned — or returned only as a summary.

- You are billed for output you may never see: 200 visible tokens might carry 3,000 reasoning tokens. Hence a separate usage field and a separate billing unit rather than folding into `output_tokens`.
- `reasoning_budget_tokens` is what stops a hard question costing twenty times a normal one.
- Hidden traces may be subject to provider policy on display and storage; the blueprint forbids exposing them where policy does.

Whether reasoning is worth its cost is Phase 20. Recording it is Phase 01.

### 8.7 Rate Limits: RPM, TPM, Token Buckets

Providers enforce at least two independent limits: **RPM** (requests per minute) and **TPM** (tokens per minute). You can breach either alone. Many tiny classification calls trip RPM while TPM idles; a few enormous RAG calls do the reverse. Which one you hit tells you which fix applies — batching for the first, prompt trimming for the second.

Limits are usually **token buckets**: a bucket refills at a steady rate, each request draws from it. Short bursts above the average rate are allowed, then throttling is abrupt. This is why traffic can be fine for thirty seconds and then fail in a cluster — you were spending burst capacity accumulated while idle.

### 8.8 Queueing Theory: Why p95 Explodes While p50 Barely Moves

The most useful theory here, and entirely invisible in code.

**Little's Law**: `L = λ × W` — items in system = arrival rate × time in system. If arrivals rise and capacity does not, time-in-system must rise.

The important part is *how* it rises. Near capacity, waiting grows asymptotically, not linearly:

```text
utilization   50%   70%   80%   90%   95%   99%
wait time      1x    2x    3x    6x   12x   50x+
```

Two consequences you would otherwise misdiagnose:

**p50 looks healthy while p95 is on fire.** Most requests sail through; unlucky ones queue behind everything. An averages-only dashboard shows nothing wrong — which is why the runbooks alert on p95 and why Section 34.2's baseline records percentiles.

**Retries during saturation make it worse.** *Congestion collapse*: the system slows, clients time out and retry, offered load rises, throughput falls toward zero.

Everything defensive in Section 25 answers this one dynamic:

| Control | Prevents |
|---|---|
| Bounded retries | Unbounded load amplification |
| Exponential backoff | Retrying into a queue that has not drained |
| Jitter | Every client retrying in the same instant |
| Honoring `Retry-After` | Overriding the provider's own recovery estimate |
| Circuit breaker | Sending more load to something already saturated |

A retry policy without backoff and a breaker is not a reliability feature. It is a load-amplification feature that happens to work when nothing is wrong.

### 8.9 A Taxonomy Of Failure

You cannot decide what to retry until you can name what failed.

| Class | Meaning | Response |
|---|---|---|
| **Transient** | Likely succeeds on repeat: blip, 503, throttle | Retry with backoff |
| **Permanent** | Fails identically forever: bad auth, oversized input | Fail fast, never retry |
| **Partial** | Some work succeeded: 60 of 100 embeddings | Resume, do not restart |
| **Gray** | Responding, but wrongly or slowly | Detect by evaluation, not error codes |

Gray failure is the class health checks miss. A provider returning HTTP 200 with degraded quality passes every check in Section 30 and every alert in Section 39.2. Nothing in Phase 01 detects it — that is the argument for Phase 07, and why the outage runbook lists "judge/human score drops after model change" beside error rates.

### 8.10 Stability Patterns

From the distributed-systems literature, long predating LLMs.

**Timeout** — the foundational one. Without it, one slow dependency exhausts your resources and your failure is indistinguishable from a hang.

**Circuit breaker** — stop calling something clearly broken, probe occasionally. Protects the caller from wasting capacity and the callee from being hammered while recovering.

**Bulkhead** — named for ship compartments: partition resources so one flooded compartment does not sink the vessel. Phase 01 does not build this, but if a hanging embedding provider ever starves chat traffic routed elsewhere, the missing pattern is the bulkhead — and you will not diagnose that without the word.

**Fail fast** — rejecting early is a feature. Section 22's "fail before the model call, not after" is this pattern.

### 8.11 Delivery Semantics

**At-most-once** never duplicates and may lose. **At-least-once** never loses and may duplicate. **Exactly-once** is not achievable end to end; it is approximated by at-least-once delivery plus idempotent handling.

A gateway retry is at-least-once. The twist absent from ordinary API work: **the provider may have finished before your timeout fired.** You retry, it runs again, you are billed twice — and because generation is non-deterministic, the second answer differs from the first.

For read-only generation that is waste. Once Phase 08 lets a model trigger real side effects it is dangerous, which is why the blueprint's non-retry list includes "the tool action would cause duplicate side effects".

### 8.12 Unit Economics

Cost per call is a number, not an insight. The metric is cost per unit of business value — per resolved ticket, per document processed, per correct extraction.

| | Cheap model | Expensive model |
|---|---|---|
| Cost per call | $0.001 | $0.010 |
| First-pass resolution | 40% | 85% |
| Calls per resolution | 2.5 | 1.18 |
| **Cost per resolution** | **$0.0025** | **$0.0118** |

The expensive model still loses here — but at 30% versus 90% resolution the picture inverts and the "cheap" model becomes the expensive one. You cannot know which world you are in without a cost number *and* a quality number.

Phase 01 produces the cost half, Phase 07 the quality half. That is why Step 17's baseline is a deliverable: it is the denominator every later optimization argument divides by. It is also why per-billing-unit `cost_records` beat a single total — "cache hit rate fell" and "prompts got longer" are different problems, and only the granular table separates them.

### 8.13 Vendor Lock-In And The Cost Of Abstraction

The adapter pattern is an abstraction, and abstractions are not free.

Lock-in has dimensions: API shape, prompts tuned to one model family, embedding vectors meaningless outside the model that made them, fine-tuned weights that cannot move at all.

Against over-abstracting: a common interface drifts toward the lowest common denominator, hiding provider strengths; every new provider feature needs interface changes; one more layer to debug.

For it, here: provider outage is a documented operational scenario with a runbook; testing without a mock would be slow, costly, and unable to simulate failure; cost and quality tradeoffs across providers are the whole point of routing.

The tension is resolved by escape hatches — `route_config_json` for provider-specific settings, `capabilities_json` for feature negotiation. Note also what Atlas refuses to abstract: embedding dimensions are pinned per route and index, because that lock-in is real and cannot be papered over.

### 8.14 Data Governance Vocabulary

Section 18.1 stores `data_policy_json` and Section 22 filters on it. These are legal terms with operational consequences.

| Term | Meaning | Why the gateway cares |
|---|---|---|
| **Controller / Processor** | Controller decides why data is processed; processor acts on instructions | Atlas is processor for tenant data, controller for its own operational data |
| **Sub-processor** | A third party the processor uses — every model provider is one | Adding a provider may require tenant notice; hence providers are configuration, not code |
| **DPA** | The contract governing the above | Determines what `restricted_data_allowed` may legally be |
| **Data residency** | Jurisdiction of processing and storage | The `region` field; some tenants may not leave a jurisdiction |
| **Retention** | How long the provider keeps payloads | The `retention` field; zero-retention endpoints process without storing |
| **Training opt-out** | Whether your data improves their models | `training_usage_allowed`; usually an enterprise buyer's first question |

Why this sits in Phase 01 rather than a governance phase: **route selection is where the policy is enforced.** By the time a request reaches the adapter the decision is made and the bytes are moving. Section 22.2's rule that route *and* provider must both allow restricted data is a legal control expressed as a boolean AND, and Section 38.4a's blocked run is the evidence it fired.

### 8.15 SLI, SLO, Error Budget

- **SLI** — a measured number. "p95 latency for `rag_answer` was 1,840 ms."
- **SLO** — an internal target. "p95 under 3,000 ms for 99% of 30-day windows."
- **SLA** — a contractual promise with financial consequences; usually looser than the SLO.
- **Error budget** — the allowed shortfall. A 99.9% SLO grants ~43 minutes of failure per month, and the remaining budget is a release decision: spend it shipping, or stop and stabilize.

The complication unique to this domain: for a normal API, availability and correctness are nearly the same question. For an AI feature they are separate. A gateway at 99.99% availability serving confidently wrong answers fails the user while passing every Phase 01 SLO. So Phase 01 can define availability and latency SLIs and cannot define a quality SLI — and knowing precisely which guarantees you do not yet have is the learning outcome.

### 8.16 Model Aliases And Silent Drift

Providers expose **pinned** identifiers (a frozen snapshot) and **aliases** (a floating pointer to "current best" that moves without warning).

An alias is convenient and, under evaluation and audit obligations, hazardous: behavior changes with no deploy, no changelog, no error. Prompts tuned to the old snapshot silently regress, and your `ai_runs` records show the model name never changed — because it genuinely did not.

This is the outage runbook's "a provider silently changes a model alias and output quality drops", whose prevention item — "add model alias pinning rule" — only makes sense once you know the mechanism. Two defenses: pin `model_routes.model_name` to a snapshot so changes become reviewed configuration with audit records (Phase 01 owns this), and detect drift with evaluation (Phase 07, and the only real detector — no error code will ever tell you the model got worse).

### 8.17 The Six To Carry Forward

```text
1. Prefill and decode differ           -> time_to_first_chunk_ms, output token pricing
2. Provider token counts are truth     -> estimates never enter usage columns
3. temperature 0 is not deterministic  -> never assert equality on model output
4. Latency degrades non-linearly       -> p95 alerts, backoff, jitter, breaker
5. Cost per call ≠ cost per outcome    -> the baseline report is a denominator
6. Aliases drift silently              -> pin models, treat evals as the detector
```

If a decision in Sections 21 through 31 looks arbitrary, the reason is almost always here.

## 9. Business Perspective

Phase 01 is where AI stops being an experiment and becomes a controllable expense with an audit trail.

Business questions Phase 01 makes answerable:

- What did AI cost today, this week, this month?
- Which tenant, feature, or model drives that cost?
- What is our p95 model latency per use case?
- What percentage of model calls fail, and why?
- Can we switch providers without a rewrite?
- Can we prove that a tenant's restricted data never left the approved region?
- Can we turn a feature off without a deploy?

Business value delivered:

| Value | Mechanism |
|---|---|
| Cost control | Route token caps, `max_cost_usd`, cost records, budget alerts |
| Vendor independence | Adapter interface plus route configuration |
| Incident recovery | Fallback routes and route status toggles |
| Compliance evidence | Provider data policy, restricted-data enforcement, audit trail |
| Predictable quality | Per-use-case model selection instead of one model for everything |
| Faster delivery | Feature teams call one client instead of learning provider SDKs |

The coverage matrix labels Phase 01 as **Required MVP**: "Central controlled model access, provider adapters, cost/latency tracking."

## 10. User Perspective

End users never see the gateway. They see its consequences.

| User Experience | Gateway Behavior Behind It |
|---|---|
| The assistant answers instead of hanging forever | Route timeout |
| A transient provider hiccup does not surface as an error | Bounded retry with backoff |
| During an outage the user gets a clear message, not a stack trace | Error envelope with a stable code and graceful degradation |
| Cheap features stay fast, hard features stay accurate | Per-use-case routing |
| Sensitive tenants stay on approved infrastructure | Restricted-data routing |

Internal users see more. The UX specification defines a Models screen with tabs `Providers`, `Routes`, `AI Runs`, `Costs`, `Capabilities`, and an Observability screen where AI run detail shows provider, model, prompt version, operation name, token usage, cache tokens, reasoning tokens, cost, latency, and linked records.

Phase 01 produces the data those screens read.

## 11. Architecture Perspective

### 11.1 Position In The System

```text
Web Console / API client
  -> API Service (apps/api)
      -> Auth and tenant context
      -> Feature service (chat, rag, evals, agents later)
          -> MODEL GATEWAY (packages/model_gateway)
              -> Router (route selection)
              -> Provider adapter
                  -> Provider HTTP API
              -> Usage and cost calculation
              -> AI run persistence
  -> PostgreSQL (model_providers, model_routes, ai_runs, cost_records)
```

### 11.2 Where Phase 01 Sits In The AI Request Lifecycle

The blueprint's AI request lifecycle is:

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

Phase 01 owns these steps:

```text
model route selected
model request created
provider called through gateway
retry attempted if allowed
run record stored
cost and latency stored
```

Phase 01 leaves hooks, but not implementations, for:

```text
prompt version resolved      -> Phase 02
output parsed and validated  -> Phase 03
input/output safety checked  -> Phase 11
```

The hooks are concrete: `ai_runs.prompt_version_id` exists as a nullable column now, and the gateway accepts an optional `prompt_version_id` and an optional `response_schema` field that Phase 03 will honor.

### 11.3 Module Boundaries

```text
apps/api/routes/model_gateway.py   -> HTTP only: parse, authorize, delegate, serialize
packages/model_gateway/client.py   -> orchestration of one model request
packages/model_gateway/router.py   -> route selection and rejection
packages/model_gateway/providers/  -> wire-format translation only
packages/model_gateway/cost.py     -> pricing arithmetic only
packages/model_gateway/token_usage.py -> usage normalization only
packages/db/models/                -> table definitions
packages/db/repositories/          -> queries for routes, providers, runs, costs
```

Rules that keep the boundary honest:

- Adapters never touch the database.
- Adapters never decide which model to use.
- The router never performs I/O against providers.
- Routes never contain secrets; secrets come from settings.
- No module outside `packages/model_gateway` imports a provider SDK or opens an HTTP connection to a model endpoint.

### 11.4 What The Gateway Does Not Own

The blueprint's "application owns the system" principle draws these lines:

| Not Owned By The Gateway | Owner |
|---|---|
| Who the user is and which tenant they belong to | `packages/auth` |
| Which prompt text is sent | `packages/prompts` (Phase 02) |
| Whether output matches a schema | Phase 03 — see the package-location note below |
| Whether content is safe | `packages/safety` (Phase 11) |
| Whether an answer is grounded | `packages/rag` (Phase 06) |
| Whether a tool may run | `packages/tools` (Phase 08) |

The gateway is a controlled pipe with a meter and a logbook. It is not the brain of the platform.

#### Note On Structured Output Package Location

The source documents place structured outputs in two different locations. `06-Atlas-Implementation-Tickets.md` lists both `packages/structured_outputs` and `packages/model_gateway/structured.py` for Phase 03, and `02-Atlas-Coverage-Matrix.md` §7 lists the artifact under `model_gateway/structured`. The blueprint's repository structure §5 shows only `model_gateway/structured.py`.

Phase 01 resolves this the only way it can without pre-empting Phase 03: it creates the `structured.py` placeholder inside `model_gateway`, per the blueprint, and leaves the question of whether schema definition and repair logic later deserve their own package to Phase 03. The distinction that will matter then is that *calling a provider in structured mode* is gateway work, while *defining schemas and repairing invalid output* is not.

## 12. Technical Scope Of Phase 01

### 12.1 In Scope

Build now:

- `model_providers`, `model_routes`, `ai_runs`, `cost_records` tables and migrations.
- Provider adapter interface for `chat` and `embed`.
- One managed provider adapter, gated behind an environment flag.
- Mock provider with programmable behaviors.
- Router with priority, capability, data policy, and budget filtering.
- Fallback resolution.
- Timeout, bounded retry with exponential backoff and jitter, and a simple circuit breaker.
- Usage normalization across providers.
- Versioned pricing sheet and cost estimation.
- AI run creation, update, and terminal status recording.
- Cost record creation per billable unit.
- Redaction of previews and payloads.
- Structured logs plus GenAI span attributes.
- API endpoints for chat, embed, route listing, and AI run lookup.
- Bootstrap loader for providers and routes from configuration.
- Full test suite using only the mock provider by default.

### 12.2 Out Of Scope

Do not build yet. The coverage matrix assigns these elsewhere:

| Deferred Item | Phase |
|---|---|
| Prompt templates, versions, rendering | 02 |
| Structured output schemas and repair loops | 03 |
| Embedding jobs, vector storage, indexes | 05 |
| RAG answer orchestration and citations | 06 |
| LLM-as-judge scoring | 07 |
| Tool calling and streaming tool calls | 08 and 20 |
| Prompt caching strategy, semantic cache, batch API, reasoning routing decisions | 20 |
| Media, voice, fine-tuning, self-hosted serving routes | 24, 13, 14, 15 |
| Canary percentage routing | 15 and 18 |

Phase 01 creates the *columns and flags* for prompt caching, reasoning, batching, and async media routes because they live in `model_routes`. It does not create the *behavior* behind them. This is deliberate: the schema is designed once, the behavior arrives when its phase arrives.

#### Divergence From The Coverage Matrix

`02-Atlas-Coverage-Matrix.md` §7 assigns two rows to Phase 20 alone:

```text
| Reasoning token tracking     | 20 | ai_runs       | reasoning token fields  | run metadata proof      |
| Provider capability matrix   | 20 | model_gateway | provider feature flags  | unsupported feature test |
```

Phase 01 cannot honor that split, because the tickets require both earlier:

- P01-006 requires tracking "input/output/cache/reasoning tokens", with the proof "ai_run stores usage fields".
- P01-002 and P01-005 require an adapter interface and route filtering, which cannot reject an unsupported feature without a capability matrix.

The workable division, and the one this document implements:

| Concern | Phase 01 | Phase 20 |
|---|---|---|
| Reasoning tokens | Store `reasoning_output_tokens`; enforce route budgets | Decide when reasoning is worth its cost; tune effort levels |
| Capability matrix | Store capabilities; enforce the minimal set in Section 17 | Use the full matrix for optimization and feature negotiation |
| Prompt caching | Store cache token counts and route flags | Design cacheable prefixes and measure hit rates |

Recommended documentation edit, outside this document's scope: change those two coverage matrix rows from `20` to `01, 20`, matching how the same file already handles "Model routing", "Token tracking", and "Streaming text".

### 12.3 Scope Boundary Rule

If a question sounds like "which model and under what limits", it is Phase 01.

If it sounds like "what text do we send" or "is the answer good", it is a later phase.

## 13. Recommended Libraries And Why

| Library | Role In Phase 01 | Why |
|---|---|---|
| Python 3.11+ | Language | Foundation choice from Phase 00 |
| Pydantic | Gateway request/response models, capability and policy models, pricing sheet validation | Typed contracts across module boundaries; the same models are reused for structured outputs in Phase 03 |
| pydantic-settings | Provider keys, flags, timeouts, budgets | Continues the Phase 00 typed settings pattern; fails fast at startup |
| FastAPI | Gateway endpoints | Already the API framework; automatic OpenAPI for the internal model endpoints |
| httpx | Provider HTTP calls | Phase 00 already added it for testing; supports sync and async, explicit timeouts, and connection pooling; using a plain HTTP client instead of a vendor SDK keeps `provider_type` adapters symmetrical |
| SQLAlchemy | Provider, route, run, and cost models | Existing persistence layer |
| Alembic | Four new tables plus deferred foreign keys | Existing migration discipline |
| pytest | Unit, integration, and contract tests | Existing test layout |
| Standard library `hashlib` | `request_hash` | No dependency needed |
| Standard library `decimal` | Cost arithmetic | Money must not be computed in binary floating point; the schema uses `numeric(12,6)` and `numeric(18,9)` |
| Standard library `random`, `time` | Backoff jitter and latency measurement | No dependency needed |

Optional, and explicitly optional:

| Library | When To Add |
|---|---|
| A vendor SDK | Only if a provider's protocol is genuinely hard to speak over plain HTTP. Keep it inside one adapter file. |
| A tokenizer library | When you need pre-call token estimates rather than post-call provider counts. Phase 01 can rely on provider-reported usage and a rough character heuristic for pre-call caps. |
| OpenTelemetry SDK | Phase 18 wires real exporters. Phase 01 can emit the same attribute names through structured logs so the migration is a transport change, not a naming change. |

Deliberately not added in Phase 01: LangChain-style orchestration frameworks, agent frameworks, vector clients, and ML training stacks. Phase 00 gave the reason: each later phase should teach its own tools clearly.

## 14. Folder Structure To Create

The blueprint's repository structure defines the target. Phase 01 fills it in:

```text
packages/
  model_gateway/
    __init__.py
    client.py              # ModelGatewayClient: orchestrates one request
    router.py              # route selection, filtering, fallback resolution
    contracts.py           # ChatRequest, ChatResponse, EmbeddingRequest, Usage, RouteDecision
    capabilities.py        # capability matrix model and capability checks
    policies.py            # data policy and budget checks
    retries.py             # backoff, jitter, retry classification, circuit breaker
    token_usage.py         # normalize provider usage into Atlas usage fields
    cost.py                # pricing sheet loading and cost calculation
    pricing/
      pricing_v1.yaml      # versioned pricing sheet
    runs.py                # ai_run creation/update and redaction
    bootstrap.py           # load providers/routes from config into database
    streaming.py           # stream assembler (thin in Phase 01)
    structured.py          # placeholder for Phase 03
    cache.py               # placeholder for Phase 20
    errors.py              # gateway-specific error codes
    providers/
      __init__.py
      base.py              # ModelProviderAdapter protocol/ABC
      openai_compatible.py # one real managed adapter
      mock.py              # fake provider for tests
      registry.py          # provider_type -> adapter class

packages/db/
  models/
    model_providers.py
    model_routes.py
    ai_runs.py
    cost_records.py
  repositories/
    model_routes.py
    ai_runs.py
    cost_records.py
  migrations/versions/
    0002_create_model_provider_and_route_tables.py
    0003_create_ai_run_and_cost_tables.py

apps/api/
  routes/
    model_gateway.py
    ai_runs.py
  schemas/
    model_gateway.py

config/
  model_providers.yaml
  model_routes.yaml

tests/
  model_gateway/
    test_contracts.py
    test_router_selection.py
    test_router_rejection.py
    test_provider_interface.py
    test_mock_provider.py
    test_retries.py
    test_fallback.py
    test_token_usage.py
    test_cost.py
    test_ai_run_persistence.py
    test_redaction.py
    test_observability_fields.py
  api/
    test_model_gateway.py
    test_ai_runs.py
  migrations/
    test_phase01_migrations.py
```

The ticket document's Phase 01 row expects exactly these locations:

```text
packages/model_gateway
packages/db/models/model_routes.py
apps/api/routes/model_gateway.py
tests/model_gateway
tests/migrations
```

## 15. File Responsibilities

### 15.1 `packages/model_gateway/contracts.py`

Purpose: the vocabulary every other module uses to talk to the gateway.

Contains the Pydantic models in Section 16. No I/O, no database, no provider knowledge. This file should be importable by any package without side effects.

### 15.2 `packages/model_gateway/client.py`

Purpose: orchestrate exactly one logical model request.

Responsibilities, in order:

```text
validate request
resolve tenant policy
select route (router)
enforce route limits
create ai_run in queued/running state
execute with retry and timeout
normalize response and usage
calculate cost
write cost records
finalize ai_run
return normalized response
```

Must not contain: HTTP calls, SQL strings, provider branching, pricing tables, prompt text.

The client is the only place that knows the full lifecycle. Everything else is a helper it calls.

### 15.3 `packages/model_gateway/router.py`

Purpose: turn `(tenant_id, use_case, requirements)` into a `RouteDecision`.

Implements the selection algorithm in Section 22 and the rejection rules in Section 23. Pure decision logic plus route reads. Raises typed rejection errors rather than returning `None`, so callers cannot ignore a rejection by accident.

### 15.4 `packages/model_gateway/providers/base.py`

Purpose: define the adapter contract.

```text
class ModelProviderAdapter:
    provider_type: str

    def chat(self, request: ProviderChatRequest) -> ProviderChatResponse: ...
    def embed(self, request: ProviderEmbeddingRequest) -> ProviderEmbeddingResponse: ...
    def structured(self, request, schema): raise NotImplementedError  # Phase 03
    def rerank(self, request): raise NotImplementedError              # optional, Phase 06
    def capabilities(self) -> ProviderCapabilities: ...
```

Ticket P01-002's acceptance proof is that the mock provider implements this interface. If the mock cannot implement it, the interface is leaking provider-specific details.

### 15.5 `packages/model_gateway/providers/openai_compatible.py`

Purpose: one real adapter for an OpenAI-compatible endpoint.

Responsibilities:

- Build the provider request body from the Atlas request.
- Send it with the route's timeout using `httpx`.
- Map provider HTTP status codes and error bodies to Atlas gateway errors.
- Extract text, finish reason, and usage counts.
- Report capabilities.

Ticket P01-003 requires this to be behind an env flag: no test run should require a real key.

### 15.6 `packages/model_gateway/providers/mock.py`

Purpose: the provider that makes the platform testable.

The blueprint's test-provider requirements:

```text
Fixed text responses.
Fixed structured responses.
Simulated invalid JSON.
Simulated timeout.
Simulated rate limit.
Simulated unsafe output.
```

Phase 01 adds two more that the runbooks imply: simulated 5xx unavailability and simulated slow-but-successful responses for latency tests.

Behavior selection should be explicit and deterministic, driven by a scenario key in the request metadata or route config. Random mock behavior produces flaky tests.

### 15.7 `packages/model_gateway/retries.py`

Purpose: decide whether an error is retryable, how long to wait, and when to stop calling a provider entirely.

Holds the retry classification table from Section 26, the backoff formula, and the circuit breaker state.

### 15.8 `packages/model_gateway/token_usage.py`

Purpose: convert whatever shape a provider returns into Atlas's five token fields.

Providers disagree on names. This file is where that disagreement ends. It must handle missing usage gracefully by recording `null` rather than guessing zero, because zero and unknown mean different things in a cost report.

### 15.9 `packages/model_gateway/cost.py`

Purpose: load a versioned pricing sheet and compute cost in `Decimal`.

Produces both the single `estimated_cost_usd` on `ai_runs` and the per-unit `cost_records` line items.

### 15.10 `packages/model_gateway/runs.py`

Purpose: create, update, and finalize `ai_runs` rows, and apply redaction before anything is written.

Keeping redaction here, next to persistence, means there is one place to audit for data leaks.

### 15.11 `packages/model_gateway/bootstrap.py`

Purpose: load `config/model_providers.yaml` and `config/model_routes.yaml` into the database.

Key job, stated by the routing document: resolve `provider_key` to `provider_id` and `fallback_route_key` to `fallback_route_id`. Must be idempotent so re-running it does not duplicate routes, and must validate that every referenced key exists before writing anything.

### 15.12 `apps/api/routes/model_gateway.py`

Purpose: HTTP surface only.

Parses and validates the request body, resolves tenant and user context, calls the gateway client, and serializes the response. It contains no routing logic, no provider names, and no cost math.

## 16. Gateway Data Contracts

The blueprint specifies the required request and response fields. Phase 01 turns them into typed models.

### 16.1 Chat Request

Blueprint fields:

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

Implementation shape:

| Field | Type | Required | Notes |
|---|---|---|---|
| request_id | str | yes | From Phase 00 request id middleware |
| trace_id | str | no | Propagated when present, generated when absent |
| tenant_id | UUID | yes | Every AI run is tenant-owned |
| user_id | UUID | no | Absent for system and worker calls |
| use_case | str | yes | Must match a route `use_case` |
| messages | list[ChatMessage] | yes | Each has `role` and `content` |
| prompt_version_id | UUID | no | Stored on the run; Phase 02 populates it |
| model_override | str | no | Admin/debug only, must be audited and permission-gated |
| temperature | float | no | Falls back to the route value, then provider default |
| max_output_tokens | int | no | Clamped to the route cap, never raised above it |
| response_schema | dict | no | Accepted and stored; enforced in Phase 03 |
| restricted_data | bool | no | Defaults to the tenant policy value, not to `false` |
| stream | bool | no | Defaults to `false` in Phase 01 |
| metadata | dict | no | Feature name, conversation id, agent run id, mock scenario |

Two rules worth stating in code comments:

- `model_override` is not a normal caller feature. It exists for operators and tests. It must be rejected unless the caller has an explicit permission, and its use must appear in the run record.
- `restricted_data` defaulting to `false` would be a data-policy bug. The safe default is whatever the tenant's policy says.

### 16.2 Chat Message

| Field | Type | Notes |
|---|---|---|
| role | str | `system`, `user`, `assistant` |
| content | str | Phase 01 is text-only; multimodal parts arrive in Phase 12 |

### 16.3 Chat Response

Blueprint fields:

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

Implementation shape:

| Field | Type | Notes |
|---|---|---|
| ai_run_id | UUID | Always returned, including on failure paths that produced a run |
| provider_name | str | Actual provider used, which may be the fallback |
| model_name | str | Actual model used |
| route_key | str | Which route served the request; essential for debugging |
| output_text | str | Assembled final text |
| output_json | dict or null | Populated in Phase 03 |
| finish_reason | str | Normalized across providers |
| usage | Usage | See 15.5 |
| estimated_cost_usd | Decimal | Matches the run record |
| latency_ms | int | Total gateway latency including retries |
| time_to_first_chunk_ms | int or null | Streaming only |
| attempts | int | How many provider attempts were made |
| used_fallback | bool | Whether the primary route failed |
| raw_response_reference | str or null | Pointer to stored raw response, not the response itself |

`raw_response_reference` is a pointer by design. Inlining full provider responses into every API reply enlarges payloads and risks echoing sensitive content back to callers who did not ask for it.

One deliberate omission: the blueprint's §15.5 field list includes `total_tokens`, which this table does not carry. The reason is that a single total cannot represent five token families that are priced differently — summing input, output, reasoning, cache-write, and cache-read tokens produces a number no cost report can use. Callers that want a total should sum the `Usage` object themselves. If a total is later wanted on the wire, add it as a derived convenience field, never as a stored column.

### 16.4 Embedding Request And Response

Request:

| Field | Type | Notes |
|---|---|---|
| request_id, trace_id, tenant_id, user_id | as above | |
| use_case | str | Typically `embedding` |
| inputs | list[str] | Batch of texts |
| restricted_data | bool | Same policy rules as chat |
| metadata | dict | Document id, chunk ids, job id |

Response:

| Field | Type | Notes |
|---|---|---|
| ai_run_id | UUID | One run per gateway call, not per input |
| provider_name, model_name, route_key | str | |
| embeddings | list[list[float]] | Order matches `inputs` exactly |
| embedding_dimension | int | Must equal the route's `embedding_dimension` |
| usage | Usage | Embedding calls report input tokens only |
| estimated_cost_usd | Decimal | |
| latency_ms | int | |

Two hard rules for embeddings, both drawn from the runbooks:

- Output order must match input order. Silent reordering corrupts a vector index in a way that is very hard to detect later.
- If the returned dimension does not match `model_routes.embedding_dimension`, fail the request. The schema specification warns that ANN indexes require a fixed dimension and that dimensions must not be mixed in one index.

### 16.5 Usage

| Field | Type | Maps To `ai_runs` |
|---|---|---|
| input_tokens | int or null | `input_tokens` |
| output_tokens | int or null | `output_tokens` |
| reasoning_output_tokens | int or null | `reasoning_output_tokens` |
| cache_creation_input_tokens | int or null | `cache_creation_input_tokens` |
| cache_read_input_tokens | int or null | `cache_read_input_tokens` |

Naming note worth recording in the code: §15.10 of the blueprint uses the older names `cache_read_tokens` and `cache_write_tokens`. The database schema specification uses the OpenTelemetry-aligned names `cache_read_input_tokens` and `cache_creation_input_tokens`, and the crosswalk confirms `gen_ai.usage.cache_read.input_tokens` and `gen_ai.usage.cache_creation.input_tokens`. Use the schema specification names everywhere. Treat the blueprint's names as historical aliases only.

The same applies to reasoning tokens: use `reasoning_output_tokens`, matching `gen_ai.usage.reasoning.output_tokens`.

### 16.6 Route Decision

The router's output, and the most useful object to log when someone asks "why did it pick that model?".

| Field | Type | Notes |
|---|---|---|
| route_id | UUID | |
| route_key | str | |
| use_case | str | |
| provider_id, provider_name, provider_type | | |
| model_name | str | |
| max_input_tokens, max_output_tokens | int | |
| temperature | Decimal or null | |
| timeout_seconds | int | |
| reasoning_enabled, reasoning_effort, reasoning_budget_tokens | | |
| prompt_caching_enabled, cacheable_prefix_min_tokens | | |
| restricted_data_allowed | bool | |
| max_cost_usd | Decimal or null | |
| fallback_route_id | UUID or null | |
| selection_reason | str | Why this route won |
| rejected_routes | list[(route_key, reason)] | Why the others lost |

`rejected_routes` is the field that makes routing explainable instead of magical. It answers the support question "why is this tenant on the expensive model?" without a debugger.

## 17. Provider Capability Matrix

Capabilities are stored in `model_providers.capabilities_json`. The blueprint's field list:

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

Phase 01 uses a subset for enforcement and stores the rest for later phases:

| Capability | Enforced In Phase 01 | Why |
|---|---|---|
| supports_chat | yes | Chat use cases require it |
| supports_embeddings | yes | Embedding use cases require it |
| supports_streaming | yes | Only when `stream=true` |
| supports_reasoning_controls | yes | Only when the route enables reasoning |
| supports_structured_output | stored, checked in Phase 03 | Rejection example 5.3 belongs to structured outputs |
| supports_tool_calling | stored | Phase 08 |
| supports_prompt_caching, supports_batch_api | stored | Phase 20 |
| max_context_tokens, max_output_tokens | yes, as an upper bound on route caps | Prevents a route configured above the model's physical limit |
| data_retention_policy, region_support | stored, surfaced in the UI | Governance evidence |

Validation rule at bootstrap time: a route may not require a capability its provider lacks. Catching this when configuration loads is far better than catching it during a customer request.

## 18. Database Objects

Phase 01 creates four tables. Column definitions come from the schema specification and are reproduced here so this phase can be implemented without switching documents.

### 18.1 `model_providers`

The terms inside `data_policy_json` — sub-processor, residency, retention, training opt-out — are defined in Section 8.14.

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key, `gen_random_uuid()` |
| name | text | no | stable provider key used by bootstrap `provider_key` |
| provider_type | text | no | `openai_compatible`, `anthropic_compatible`, `azure_openai`, `local_vllm`, `local_tgi`, `mock` |
| base_url | text | yes | provider endpoint |
| capabilities_json | jsonb | no | capability matrix |
| data_policy_json | jsonb | no | retention/training/region policy |
| status | text | no | `active`, `disabled` |
| created_at | timestamptz | no | |
| updated_at | timestamptz | no | |

Constraints:

```sql
unique(name)
check (provider_type in ('openai_compatible','anthropic_compatible','azure_openai','local_vllm','local_tgi','mock'))
check (status in ('active','disabled'))
```

The schema specification mandates `unique(name)` and notes that `name` is the provider key referenced by bootstrap configuration. The two `check` constraints follow the document's stated preference for text columns with check constraints over database enums during learning, because they are easier to migrate.

Note what is absent: there is no API key column. Keys are configuration and secrets, never database rows. Section 20 covers key resolution.

### 18.2 `model_routes`

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | yes | null means a global route |
| use_case | text | no | `chat`, `rag_answer`, `embedding`, `judge`, `media_generation`, and the other use cases in use |
| route_key | text | no | stable config key such as `rag_answer_primary` |
| provider_id | uuid | no | references `model_providers(id)` |
| model_name | text | no | model id |
| priority | int | no | lower number first |
| max_input_tokens | int | no | request cap |
| max_output_tokens | int | no | output cap |
| temperature | numeric(4,3) | yes | null means provider default |
| timeout_seconds | int | no | model timeout |
| fallback_route_id | uuid | yes | self-reference; loaders resolve it from `fallback_route_key` |
| prompt_caching_enabled | boolean | no | default false |
| cacheable_prefix_min_tokens | int | yes | provider-specific minimum useful cached prefix |
| semantic_cache_enabled | boolean | no | default false |
| batch_enabled | boolean | no | default false |
| max_batch_items | int | yes | provider batch limit for this route |
| embedding_dimension | int | yes | required for embedding routes |
| async_only | boolean | no | default false; true for long media/video/batch jobs |
| cost_estimate_required | boolean | no | true for expensive or async routes |
| max_cost_usd | numeric(12,6) | yes | per-request or per-job route budget |
| route_config_json | jsonb | no | provider-specific settings not promoted to columns |
| reasoning_enabled | boolean | no | default false |
| reasoning_effort | text | yes | `low`, `medium`, `high` |
| reasoning_budget_tokens | int | yes | max reasoning tokens |
| restricted_data_allowed | boolean | no | default false |
| status | text | no | `active`, `disabled` |
| created_at | timestamptz | no | |
| updated_at | timestamptz | no | |

Unique indexes and checks, exactly as specified:

```sql
create unique index uq_model_routes_global_route_key
on model_routes(route_key)
where tenant_id is null;

create unique index uq_model_routes_tenant_route_key
on model_routes(tenant_id, route_key)
where tenant_id is not null;

check (priority > 0)
check (max_input_tokens > 0)
check (max_output_tokens > 0 or use_case in ('embedding','image_generation','video_generation','audio_generation'))
check (cacheable_prefix_min_tokens is null or cacheable_prefix_min_tokens > 0)
check (max_batch_items is null or max_batch_items > 0)
check (embedding_dimension is null or embedding_dimension > 0)
check (max_cost_usd is null or max_cost_usd >= 0)
```

Indexes:

```sql
idx_model_routes_use_case_status(use_case, status)
idx_model_routes_tenant_use_case(tenant_id, use_case)
idx_model_routes_route_key(tenant_id, route_key)
```

Why the two partial unique indexes instead of one plain `unique(tenant_id, route_key)`: the schema document explains that PostgreSQL treats nulls as distinct, so a plain unique constraint would allow many global routes with the same `route_key`. Partial indexes give global routes and tenant routes different, correct uniqueness rules.

The route-config rule from the schema document is worth following strictly:

```text
Use first-class columns for routing decisions that the gateway filters on frequently.
Use route_config_json only for provider-specific optional settings.
```

If the router filters on it, it is a column. If only an adapter reads it, it belongs in `route_config_json`.

### 18.3 `ai_runs`

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references `tenants(id)` |
| user_id | uuid | yes | references `users(id)` |
| conversation_id | uuid | yes | soft reference until `008a_add_ai_runs_conversation_fk` |
| agent_run_id | uuid | yes | soft reference until `012a_add_ai_runs_agent_run_fk` |
| use_case | text | no | route use case |
| provider_name | text | no | provider used |
| model_name | text | no | model used |
| model_route_id | uuid | yes | references `model_routes(id)` |
| prompt_version_id | uuid | yes | references `prompt_versions(id)` once that table exists |
| request_hash | text | no | normalized hash |
| input_preview | text | yes | redacted preview |
| output_preview | text | yes | redacted preview |
| request_json | jsonb | yes | redacted full request if allowed |
| response_json | jsonb | yes | redacted full response if allowed |
| status | text | no | `queued`, `running`, `succeeded`, `failed`, `cancelled`, `blocked` |
| error_code | text | yes | stable error code |
| error_message | text | yes | safe message |
| input_tokens | int | yes | |
| output_tokens | int | yes | |
| reasoning_output_tokens | int | yes | OTel-aligned reasoning token name |
| cache_creation_input_tokens | int | yes | provider cache write tokens |
| cache_read_input_tokens | int | yes | provider cache read tokens |
| estimated_cost_usd | numeric(12,6) | yes | calculated cost |
| latency_ms | int | yes | total model latency |
| time_to_first_chunk_ms | int | yes | streaming latency |
| trace_id | text | yes | distributed trace id |
| created_at | timestamptz | no | |

Indexes:

```sql
idx_ai_runs_tenant_created(tenant_id, created_at desc)
idx_ai_runs_use_case_created(use_case, created_at desc)
idx_ai_runs_prompt_version(prompt_version_id)
idx_ai_runs_model_route(model_route_id)
idx_ai_runs_trace_id(trace_id)
```

The `ai_run_status` enum from §3.1 of the schema document is:

```text
queued, running, succeeded, failed, cancelled, blocked
```

`blocked` is the status for policy rejections: restricted data on a public route, budget exceeded, or, later, a safety block. Blocked is not failed. Failed means Atlas tried and something broke. Blocked means Atlas correctly refused. Conflating them makes both the reliability dashboard and the governance report wrong.

Note also that `ai_runs` has `created_at` but no `updated_at` in the specification. The row is written at creation and finalized once. If you want a completion timestamp, derive it from `created_at + latency_ms`, or propose an explicit schema change rather than adding an undocumented column.

### 18.4 `cost_records`

| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key |
| tenant_id | uuid | no | references `tenants(id)` |
| ai_run_id | uuid | yes | references `ai_runs(id)` |
| batch_job_id | uuid | yes | soft reference until `batch_model_jobs` exists |
| media_generation_job_id | uuid | yes | soft reference until `media_generation_jobs` exists |
| use_case | text | no | |
| provider_name | text | no | |
| model_name | text | no | |
| billing_unit | text | no | `input_token`, `output_token`, `reasoning_token`, `cache_write_token`, `cache_read_token`, `image`, `audio_second`, `video_second`, `request` |
| quantity | numeric(18,6) | no | billable quantity |
| unit_cost_usd | numeric(18,9) | no | cost per unit |
| estimated_cost_usd | numeric(12,6) | no | estimated line cost |
| actual_cost_usd | numeric(12,6) | yes | actual provider cost when known |
| currency | text | no | `USD` |
| pricing_version | text | yes | pricing sheet version |
| created_at | timestamptz | no | |

Constraints and indexes:

```sql
check (quantity >= 0)
check (estimated_cost_usd >= 0)
check (actual_cost_usd is null or actual_cost_usd >= 0)

idx_cost_records_tenant_created(tenant_id, created_at desc)
idx_cost_records_ai_run(ai_run_id)
idx_cost_records_use_case_created(use_case, created_at desc)
```

Why a separate table when `ai_runs.estimated_cost_usd` already exists: the run column answers "what did this call cost". The cost records answer "what was it made of". Cache-read tokens are cheaper than fresh input tokens, reasoning tokens may be priced differently from output tokens, and pricing changes over time. The cost spike runbook requires comparing "input, output, reasoning, cache-read, and cache-write token counts", and per-unit rows make that a straightforward query instead of a reconstruction.

Naming and shape note, in the same spirit as Section 16.5. The blueprint's §11.9 defines an earlier, flatter `cost_records`:

```text
id, tenant_id, ai_run_id nullable, provider_name, model_name, use_case,
input_tokens, output_tokens, cost_usd, created_at
```

That shape has one row per run and cannot express cache-read or reasoning tokens as separately priced units, so it cannot answer the cost runbook's diagnosis questions. The schema specification's line-item model supersedes it. Use the schema specification's columns; treat the blueprint's version as historical.

### 18.5 Entity Relationships Introduced

```text
tenants (1) ----< model_routes (0..n)        tenant_id nullable = global route
model_providers (1) ----< model_routes (0..n)
model_routes (1) ----< model_routes (0..n)   fallback_route_id, self-reference
tenants (1) ----< ai_runs (0..n)
users (0..1) ----< ai_runs (0..n)
model_routes (0..1) ----< ai_runs (0..n)
ai_runs (1) ----< cost_records (0..n)
prompt_versions (0..1) ----< ai_runs (0..n)  soft until Phase 02
conversations (0..1) ----< ai_runs (0..n)    soft until Phase 06
agent_runs (0..1) ----< ai_runs (0..n)       soft until Phase 09
```

The self-reference on `model_routes.fallback_route_id` deserves attention: it makes a fallback cycle physically possible. Section 23 covers cycle detection.

## 19. Migration Plan And Deferred Foreign Keys

### 19.1 The Canonical Migration Order

The schema specification's MVP migration order is:

```text
001_enable_extensions
002_create_identity_tables
003_create_audit_and_observability_base
004_create_prompt_and_model_tables
005_create_document_tables
006_create_ingestion_jobs
007_create_vector_tables
008_create_conversation_and_rag_tables
009_create_eval_tables
010_create_feedback_tables
```

The governing rule:

```text
Never create a table that references a table which has not been created in an earlier migration.
```

### 19.2 A Conflict In The Source Documents, And How To Resolve It

There is a genuine ordering conflict between two statements in the schema specification, and Phase 01 is where it surfaces:

- `cost_records` is grouped under `003_create_audit_and_observability_base`.
- `cost_records.ai_run_id` references `ai_runs(id)`.
- `ai_runs` is created in `004_create_prompt_and_model_tables`.

A table created in migration 003 cannot carry a foreign key to a table created in migration 004 without violating the ordering rule.

Recommended resolution, consistent with the pattern the document already uses elsewhere:

Create `cost_records.ai_run_id` as a nullable UUID **soft reference** in the audit/observability migration, then add the foreign key in a follow-up migration after `ai_runs` exists. This mirrors the documented deferred-FK pattern for `ai_runs.conversation_id` and `ai_runs.agent_run_id`.

Proposed addition to the deferred foreign key table:

| Deferred Constraint | Create Column In | Add FK After | Migration |
|---|---|---|---|
| `cost_records.ai_run_id -> ai_runs(id)` | `003_create_audit_and_observability_base` | `004_create_prompt_and_model_tables` | `004a_add_cost_records_ai_run_fk` |

The alternative — creating `cost_records` in the same migration as `ai_runs` — also works and is simpler if the audit migration has not been written yet. Pick one, write it down as a decision record, and make the migration test prove it applies cleanly on an empty database. Do not leave it ambiguous.

### 19.3 A Second Deferred Foreign Key Phase 01 Creates

`ai_runs.prompt_version_id` references `prompt_versions(id)`. In the canonical order both tables are created inside migration 004, so the constraint is satisfiable there.

Phase 01, however, deliberately does **not** build the prompt system. That is Phase 02, and ticket P02-007 is the ticket that stores `prompt_version_id` in `ai_runs`.

So if Phase 01 is implemented before Phase 02, `prompt_version_id` must be a nullable UUID soft reference now, with the foreign key added when the prompt tables land:

| Deferred Constraint | Create Column In | Add FK After | Migration |
|---|---|---|---|
| `ai_runs.prompt_version_id -> prompt_versions(id)` | Phase 01 model/run migration | Phase 02 prompt tables migration | `add_ai_runs_prompt_version_fk` |

Record this decision explicitly. A soft reference that nobody documents becomes a soft reference that nobody ever hardens.

### 19.4 Practical Migration Files For Phase 01

If you follow the canonical numbering, Phase 01's work is the model and run half of `004_create_prompt_and_model_tables`, plus the observability base that carries `cost_records`.

If the repository already started its own numbering with a foundation migration that created `tenants` and `users`, then Phase 01 adds:

```text
0002_create_model_provider_and_route_tables
  - model_providers
  - model_routes, with both partial unique indexes, all check constraints, and all indexes
  - fallback_route_id self-referencing foreign key

0003_create_ai_run_and_cost_tables
  - ai_runs, with conversation_id, agent_run_id, prompt_version_id as nullable soft references
  - cost_records, with ai_run_id foreign key created in the same migration so no deferral is needed
  - all indexes from the specification
```

Whichever numbering is used, keep a mapping table in the repository so a reviewer can line the migrations up against the canonical order. Divergent numbering with no map is how two developers end up with different databases.

### 19.5 Migration Test Requirements

Ticket P01-001's acceptance proof is "migration applies cleanly". Make that a real test, in `tests/migrations`:

```text
test_migrations_upgrade_head_on_empty_database
test_model_routes_global_route_key_uniqueness_enforced
test_model_routes_tenant_route_key_uniqueness_enforced
test_model_routes_priority_check_rejects_zero
test_model_routes_embedding_use_case_allows_zero_output_tokens
test_ai_runs_status_check_rejects_unknown_status
test_cost_records_quantity_check_rejects_negative
test_downgrade_then_upgrade_returns_to_head
```

The uniqueness tests matter most. Partial unique indexes are easy to write incorrectly, and their failure mode is silent duplication rather than an error.

## 20. Configuration And Secrets

### 20.1 Configuration Rules From The Blueprint

```text
Never hard-code secrets.
Never expose provider keys to frontend code.
Validate config at startup.
Fail fast if required config is missing.
Use separate config for local, test, staging, and production.
Keep .env.example complete but without secrets.
```

The blueprint's configuration group list already reserves the AI settings Phase 01 needs:

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
DEFAULT_CHAT_MODEL
DEFAULT_EMBEDDING_MODEL
MAX_INPUT_TOKENS
MAX_OUTPUT_TOKENS
REQUEST_TIMEOUT_SECONDS
DAILY_MODEL_COST_LIMIT
ENABLE_LOCAL_MODEL_SERVER
```

Phase 00 reserved the same idea in its `.env.example`, with placeholder chat and embedding model entries marked as unused.

### 20.2 Settings Phase 01 Adds

Group these in the settings class rather than scattering them:

| Setting | Purpose | Safe Default |
|---|---|---|
| `MODEL_GATEWAY_ENABLED` | Master switch for real provider calls | `false` |
| `MODEL_GATEWAY_DEFAULT_PROVIDER` | Provider used when configuration is minimal | `mock` |
| `REQUEST_TIMEOUT_SECONDS` | Ceiling applied above any route timeout | `60` |
| `MAX_INPUT_TOKENS` | Platform ceiling above any route input cap | `32000` |
| `MAX_OUTPUT_TOKENS` | Platform ceiling above any route output cap | `4000` |
| `MODEL_MAX_RETRIES` | Hard retry cap | `2` |
| `MODEL_RETRY_BASE_DELAY_MS` | Backoff base | `200` |
| `MODEL_RETRY_MAX_DELAY_MS` | Backoff ceiling | `5000` |
| `MODEL_CIRCUIT_BREAKER_THRESHOLD` | Consecutive failures before opening | `5` |
| `MODEL_CIRCUIT_BREAKER_COOLDOWN_SECONDS` | Wait before a probe attempt | `30` |
| `MODEL_PRICING_VERSION` | Which pricing sheet to load | `pricing_v1` |
| `DAILY_MODEL_COST_LIMIT` | Platform-level guard, in USD | `10` locally |
| `AI_RUN_STORE_REQUEST_JSON` | Whether redacted request payloads are stored | `false` |
| `AI_RUN_STORE_RESPONSE_JSON` | Whether redacted response payloads are stored | `false` |
| `AI_RUN_PREVIEW_MAX_CHARS` | Preview truncation length | `500` |
| `<PROVIDER_NAME>_API_KEY` | One key per provider name | unset |

Every default above is chosen so that a fresh clone with no secrets runs the full test suite against the mock provider and never contacts a real provider. That is ticket P01-004's acceptance proof: "no tests require real model key".

Naming discipline: the first four settings above reuse the blueprint §8 names exactly — `REQUEST_TIMEOUT_SECONDS`, `MAX_INPUT_TOKENS`, `MAX_OUTPUT_TOKENS`, `DAILY_MODEL_COST_LIMIT` — rather than inventing gateway-prefixed variants. Phase 00's §13.1 reserved the same concepts under different names (`MODEL_REQUEST_TIMEOUT_SECONDS`, `MAX_MODEL_INPUT_TOKENS`, `DAILY_AI_COST_LIMIT`), which means the set currently has three names for two of these settings. The blueprint is the architectural authority for configuration, so its names win; Phase 00's reserved names should be corrected to match. Settings whose concept the blueprint never named — the retry, circuit breaker, pricing, and `ai_run` storage flags — are new and take the `MODEL_` or `AI_RUN_` prefix.

All of these are read through the Phase 00 typed settings class with its existing environment prefix, so the actual environment variables carry that prefix.

### 20.3 How A Provider Adapter Gets Its Key

The key is not in `model_providers`. Resolution order:

```text
provider row gives:  name, provider_type, base_url
settings give:       <PROVIDER_NAME>_API_KEY
adapter factory:     looks up the key by provider name at construction time
if the key is missing and the provider is active and not mock:
    fail fast with ai.provider_not_configured
```

Failing at startup or during bootstrap validation is better than failing on a user's first request. The Phase 00 argument for typed settings applies exactly: with typed settings, startup fails immediately.

### 20.4 Secrets Hygiene Checklist

```text
[ ] No provider key appears in any database table
[ ] No provider key appears in any log line, including debug logs
[ ] No provider key appears in an error message or error details object
[ ] No provider key is returned by any API endpoint, including admin endpoints
[ ] .env.example lists every new variable with a placeholder value
[ ] Provider request headers are excluded from any stored request_json
[ ] Test fixtures use obviously fake keys
```

The crosswalk ties this to the AISVS chapter "Infrastructure, Configuration & Deployment Security" and to OWASP LLM02 Sensitive Information Disclosure.

## 21. Bootstrap Route Configuration

### 21.1 Why Configuration Files, Not Code

Routes change more often than code. An operator following the provider outage runbook needs to disable a route or repoint a fallback quickly, and needs an audit trail of what changed. Storing routes in the database and seeding them from reviewed configuration files gives both.

### 21.2 Provider Configuration

Following the routing document's registry examples:

```yaml
providers:
  - name: openai_primary
    provider_type: openai_compatible
    base_url: https://api.openai.com/v1
    status: active
    capabilities:
      supports_chat: true
      supports_structured_output: true
      supports_streaming: true
      supports_tool_calling: true
      supports_prompt_caching: true
      supports_batch_api: true
      supports_reasoning_controls: true
      supports_embeddings: true
    data_policy:
      restricted_data_allowed: false
      training_usage_allowed: false
      region: provider_default
      retention: provider_policy

  - name: azure_private_llm
    provider_type: azure_openai
    base_url: https://tenant-resource.openai.azure.com
    status: active
    capabilities:
      supports_chat: true
      supports_structured_output: true
      supports_streaming: true
      supports_prompt_caching: true
      supports_embeddings: true
      supports_reasoning_controls: false
    data_policy:
      restricted_data_allowed: true
      training_usage_allowed: false
      region: tenant_region
      retention: enterprise_contract

  - name: local_vllm
    provider_type: local_vllm
    base_url: http://model-server:8000/v1
    status: active
    capabilities:
      supports_chat: true
      supports_structured_output: false
      supports_streaming: true
      supports_prompt_caching: false
      supports_embeddings: false
      supports_tool_calling: false
    data_policy:
      restricted_data_allowed: true
      training_usage_allowed: false
      region: private_network
      retention: self_managed

  - name: mock_provider
    provider_type: mock
    base_url: null
    status: active
    capabilities:
      supports_chat: true
      supports_embeddings: true
      supports_streaming: true
      supports_structured_output: true
      supports_reasoning_controls: true
    data_policy:
      restricted_data_allowed: true
      training_usage_allowed: false
      region: local
      retention: none
```

The mock provider is registered like any other provider. That is what lets integration tests exercise the real router, the real run persistence, and the real cost path without a network call.

### 21.3 Route Configuration

The Phase 01 use cases from ticket P01-005 — chat, classifier, rag_answer, embedding, judge — expressed with the routing document's fields:

```yaml
routes:
  - route_key: classification_primary
    use_case: classification
    provider_key: openai_primary
    model_name: cheap-fast-model
    priority: 1
    max_input_tokens: 2000
    max_output_tokens: 300
    temperature: 0.0
    timeout_seconds: 8
    reasoning_enabled: false
    prompt_caching_enabled: false
    restricted_data_allowed: false
    fallback_route_key: classification_private

  - route_key: rag_answer_primary
    use_case: rag_answer
    provider_key: openai_primary
    model_name: high-quality-chat-model
    priority: 1
    max_input_tokens: 24000
    max_output_tokens: 1800
    temperature: 0.2
    timeout_seconds: 30
    reasoning_enabled: false
    prompt_caching_enabled: true
    cacheable_prefix_min_tokens: 1024
    restricted_data_allowed: false
    fallback_route_key: rag_answer_private

  - route_key: rag_answer_private
    use_case: rag_answer          # NOT rag_answer_private - see the note below
    provider_key: azure_private_llm
    model_name: private-chat-model
    priority: 2                   # loses to the primary for unrestricted requests
    max_input_tokens: 16000
    max_output_tokens: 1600
    temperature: 0.2
    timeout_seconds: 35
    reasoning_enabled: false
    prompt_caching_enabled: true
    restricted_data_allowed: true
    fallback_route_key: null

  - route_key: classification_private
    use_case: classification
    provider_key: azure_private_llm
    model_name: private-chat-model
    priority: 2
    max_input_tokens: 2000
    max_output_tokens: 300
    temperature: 0.0
    timeout_seconds: 10
    reasoning_enabled: false
    prompt_caching_enabled: false
    restricted_data_allowed: true
    fallback_route_key: null

  - route_key: embedding_primary
    use_case: embedding
    provider_key: openai_primary
    model_name: embedding-model-large
    priority: 1
    max_input_tokens: 8192
    max_output_tokens: 0
    embedding_dimension: 1536
    batch_enabled: true
    max_batch_items: 2048
    timeout_seconds: 60
    restricted_data_allowed: false
    fallback_route_key: embedding_private

  - route_key: embedding_private
    use_case: embedding
    provider_key: azure_private_llm
    model_name: private-embedding-model
    priority: 2
    max_input_tokens: 8192
    max_output_tokens: 0
    embedding_dimension: 1536     # MUST match embedding_primary - see the note below
    batch_enabled: true
    max_batch_items: 1024
    timeout_seconds: 60
    restricted_data_allowed: true
    fallback_route_key: null

  - route_key: llm_judge_primary
    use_case: llm_judge
    provider_key: openai_primary
    model_name: judge-capable-model
    priority: 1
    max_input_tokens: 12000
    max_output_tokens: 1200
    temperature: 0.0
    timeout_seconds: 30
    reasoning_enabled: true
    reasoning_effort: medium
    reasoning_budget_tokens: 2000
    prompt_caching_enabled: true
    restricted_data_allowed: false

  - route_key: chat_primary
    use_case: chat
    provider_key: openai_primary
    model_name: high-quality-chat-model
    priority: 1
    max_input_tokens: 12000
    max_output_tokens: 1200
    temperature: 0.3
    timeout_seconds: 30
    restricted_data_allowed: false
    fallback_route_key: chat_mock

  - route_key: chat_mock
    use_case: chat
    provider_key: mock_provider
    model_name: mock-chat-model
    priority: 9
    max_input_tokens: 12000
    max_output_tokens: 1200
    temperature: 0.3
    timeout_seconds: 10
    restricted_data_allowed: true
    fallback_route_key: null
```

This is a complete, loadable registry: every `fallback_route_key` above resolves to a route defined in the same file, and no chain forms a cycle. That is a requirement, not a nicety — Section 21.4 has bootstrap reject the whole file if a referenced key is missing, so a config with dangling fallbacks fails on the first run.

Five details here are easy to get wrong:

- `embedding_primary` sets `max_output_tokens: 0`. That is legal only because the check constraint exempts `use_case in ('embedding','image_generation','video_generation','audio_generation')`.
- The private routes set `fallback_route_key: null` deliberately. The routing document explains why: "Fallback should not silently downgrade to less private provider." A private route is where fallback must stop.
- Every private route carries `priority: 2` so it loses to its public counterpart for ordinary traffic and wins only when the data-policy filter has removed the public route. Priority does the selection; the policy filter does the exclusion.
- `embedding_private` declares the same `embedding_dimension` as `embedding_primary`. Falling back to a different embedding dimension would silently poison the vector index, which the vector runbook forbids: "do not mix embedding dimensions/models in same index version." If no private model matches the dimension, the correct configuration is no fallback at all.
- `chat_mock` gives the chat route a fallback that always works locally. In staging and production this route should be disabled or removed; a mock answering real user traffic during an outage is worse than a clean error.

#### Why `rag_answer_private` Uses `use_case: rag_answer`

`07-Atlas-Model-Routing-And-Provider-Examples.md` §3.6 gives this route `use_case: rag_answer_private`. This document deliberately changes it to `rag_answer`, and the reason is worth understanding because it is the kind of configuration bug that reads as correct.

The router loads candidates with `where use_case = :use_case` (Section 22.2). A caller asking for a grounded answer asks for `rag_answer` — it does not know or care whether the tenant is restricted. If the private route is registered under a different `use_case`, then:

- It is never a candidate for any real request.
- `rag_answer_primary` can never fall back to it, because the fallback must pass the same filters.
- A restricted-data `rag_answer` request finds no compliant route and is always blocked.

That last outcome would make ticket P01-010 unsatisfiable in the direction that matters. P01-010 is about blocking a call when policy disallows the route — not about making compliant routing impossible.

The correct model is: **`use_case` describes what the caller wants; `restricted_data_allowed` and `priority` describe who may serve it.** Data sensitivity is a filter, not a different use case. Registering both routes under `rag_answer` lets the router do exactly what §4 of the routing document describes — filter by data policy, then select by priority.

If the documentation owner prefers to keep the routing document's spelling, then the router must be changed to map a restricted `rag_answer` request onto the `rag_answer_private` use case explicitly. That is more machinery for the same result, and it puts policy logic in two places. This document takes the simpler path.

### 21.4 Bootstrap Loader Behavior

```text
read provider config
validate provider schema and capability keys
upsert providers by name

read route config
validate that every provider_key exists
validate that every fallback_route_key exists in this file or in the database
validate that no route requires a capability its provider lacks
validate that embedding routes declare embedding_dimension
detect fallback cycles
upsert routes by (tenant_id, route_key)
resolve provider_key       -> provider_id
resolve fallback_route_key -> fallback_route_id in a second pass
write an audit entry for each created or changed route
```

Two-pass resolution is required because a route can reference a fallback that appears later in the file.

Idempotency requirement: running bootstrap twice must produce no changes the second time. The proof is a test that runs it twice and asserts route count and content are stable.

## 22. Route Selection Algorithm

### 22.1 The Documented Algorithm

The routing document specifies:

```text
receive model request
-> resolve tenant policy
-> resolve use_case
-> load active routes ordered by priority
-> filter routes by required capability
-> filter routes by data policy
-> filter routes by cost budget
-> select first route
-> resolve bootstrap provider_key to provider_id and fallback_route_key to fallback_route_id
-> if provider unavailable, apply fallback if policy allows
-> create ai_run record
-> execute provider call
-> store usage, cost, latency, cache tokens, reasoning tokens
```

### 22.2 Implementation Detail Per Step

**Resolve tenant policy.** Load the tenant's settings. The outputs that matter are whether this tenant requires restricted-data handling and whether the tenant has route overrides. Every AI run is tenant-owned, so a request with no tenant is a programming error, not a default-to-global case.

**Resolve use case.** Reject an unknown use case immediately with `ai.route_not_found`. Do not silently fall back to a generic chat route; that is how classification traffic ends up on an expensive model.

**Load candidate routes.**

```sql
select * from model_routes
where use_case = :use_case
  and status = 'active'
  and (tenant_id = :tenant_id or tenant_id is null)
order by
  case when tenant_id is null then 1 else 0 end,   -- tenant routes before global
  priority asc,
  created_at asc                                    -- deterministic tie-break
```

Tenant-specific routes must outrank global routes; that is the point of allowing `tenant_id` to be non-null. The `created_at` tie-break makes selection deterministic when two routes share a priority, which matters for reproducible tests.

**Filter by capability.** For each candidate, check the provider capability matrix against what the request needs: chat or embeddings, streaming if requested, reasoning controls if the route enables reasoning. Record every rejection with a reason.

**Filter by data policy.** If the request is restricted, keep only routes where `model_routes.restricted_data_allowed = true` **and** the provider's `data_policy_json.restricted_data_allowed = true`. Both must agree. A permissive route pointing at a non-compliant provider is a configuration error that should never be able to serve traffic.

**Filter by cost budget.** Two checks:

- Route level: if `max_cost_usd` is set, the pre-call estimate must not exceed it.
- Tenant or platform level: if spend today already exceeds the budget, reject with `ai.budget_exceeded`.

The blueprint's cost control list includes per-tenant monthly budgets and per-user daily budgets. Phase 01 can implement a simple daily aggregate over `cost_records`; richer budget accounting belongs to Phases 18 and 20.

**Select first route.** After filtering, the first remaining candidate wins. Build the `RouteDecision`, including `selection_reason` and the full `rejected_routes` list.

**Resolve identifiers.** In a database-backed system this is already done: `provider_id` and `fallback_route_id` are columns. Key resolution belongs to bootstrap time, not request time. Resolving keys per request would be a performance bug.

### 22.3 Route Caching

Route lookups happen on every model call. Caching them in process with a short TTL is reasonable, but only with an explicit invalidation path, because the outage runbook depends on route changes taking effect quickly.

Rules if you cache:

```text
TTL measured in seconds, not minutes.
Route changes through the admin API invalidate the cache immediately.
Cache key includes tenant_id, use_case, and status.
Every ai_run records the route_id actually used, so a stale cache is detectable after the fact.
```

If in doubt in Phase 01, do not cache. A single indexed query is cheap next to a model call that takes hundreds of milliseconds.

## 23. Route Rejection Rules

### 23.1 Documented Rejection Examples

```text
Restricted data on public route:
  Request has restricted_data=true, route restricted_data_allowed=false
  -> reject or route to private route

Reasoning budget too high:
  Requested reasoning_budget_tokens=8000, route maximum 4000
  -> reject or reduce by policy

Provider does not support structured output:
  Use case requires structured output, provider capability is false
  -> select another route or fail before model call
```

The third example is Phase 03's to enforce, but its principle applies now, and in general form it is the most valuable sentence in the routing document: **fail before the model call, not after**. A rejected request should cost nothing.

### 23.2 Full Rejection Table For Phase 01

| Condition | Error Code | HTTP | Run Status |
|---|---|---|---|
| Unknown `use_case` | `ai.route_not_found` | 400 | no run created |
| All routes for the use case are disabled | `ai.route_unavailable` | 503 | `blocked` |
| Restricted data with no compliant route | `ai.restricted_data_not_allowed` | 403 | `blocked` |
| Provider lacks a required capability | `ai.capability_unsupported` | 400 | `blocked` |
| Input exceeds `max_input_tokens` | `ai.input_too_large` | 413 | `blocked` |
| Requested output above `max_output_tokens` | clamp, do not reject | — | — |
| Reasoning budget above route budget | clamp or `ai.reasoning_budget_exceeded` | 400 | `blocked` |
| Estimated cost above `max_cost_usd` | `ai.cost_limit_exceeded` | 402 | `blocked` |
| Tenant budget exhausted | `ai.budget_exceeded` | 402 | `blocked` |
| `model_override` without permission | `permission_denied` | 403 | no run created |
| Embedding route missing `embedding_dimension` | `ai.route_misconfigured` | 500 | `blocked` |
| Fallback cycle detected | `ai.route_misconfigured` | 500 | `blocked` |

Clamp versus reject is a real design decision, so here is the reasoning. Exceeding an *output* cap is usually a caller convenience issue, and clamping is harmless and helpful. Exceeding an *input* cap changes what the model actually sees, so silent truncation would corrupt the request; reject instead and let the caller decide what to drop.

Whether to clamp or reject an over-budget reasoning request is a policy choice — the routing document permits both ("reject or reduce by policy"). Pick one, express it in settings or route config, and test it. Do not decide it per call site.

### 23.3 Fallback Cycle Detection

Because `fallback_route_id` is a self-reference, `A -> B -> A` is physically possible.

Protections:

```text
Bootstrap validation: walk the fallback chain and fail if a route is visited twice.
Runtime: cap fallback depth at 1 in Phase 01, 2 at most.
Runtime: track visited route ids within a single request.
```

Depth 1 is the right Phase 01 default. Deep fallback chains multiply latency and cost during exactly the incidents when both are already under pressure.

## 24. Provider Adapter Design

### 24.1 The Contract

Every adapter implements the same logical interface, and the blueprint's requirement is absolute: "The rest of the application must not care which provider is used."

Concretely, an adapter:

- Receives an already-resolved request. It does not select models, apply budgets, or read the database.
- Applies the timeout it is given. It does not invent its own.
- Returns normalized output: text, finish reason, usage, and a provider response id.
- Raises typed Atlas errors, never provider-specific exceptions.
- Reports its capabilities.

### 24.2 Normalization Responsibilities

| Provider Variation | Adapter Normalizes To |
|---|---|
| Different message array shapes | Atlas `messages` list |
| Different token usage field names | Atlas `Usage` |
| Different finish reason strings | `completed`, `max_tokens`, `content_filter`, `tool_calls`, `error` |
| Different error body shapes | Atlas error codes |
| Different streaming event formats | Atlas stream events |
| Different embedding response shapes | Ordered vector list plus dimension |

The finish-reason mapping is small and boring and saves a great deal of pain. Once every provider's stop condition maps to five known values, downstream code can detect truncation without knowing who served the request.

### 24.3 Error Mapping

| Provider Outcome | Gateway Error | Retryable |
|---|---|---|
| Connection error, DNS failure, reset | `ai.provider_unavailable` | yes |
| Request timeout | `ai.provider_timeout` | yes |
| HTTP 429 | `ai.provider_rate_limited` | yes, honor `Retry-After` |
| HTTP 500, 502, 503, 504 | `ai.provider_unavailable` | yes |
| HTTP 401, 403 | `ai.provider_auth_failed` | no |
| HTTP 400 invalid request | `ai.provider_bad_request` | no |
| HTTP 413 or context-length error | `ai.input_too_large` | no |
| Provider content filter | `ai.provider_content_filtered` | no |
| Malformed or unparseable body | `ai.provider_invalid_response` | no |

The blueprint's non-retry list is the source of the "no" column:

```text
The request violates policy.
The input is too large.
Authentication with provider fails.
The output is unsafe.
The tool action would cause duplicate side effects.
```

Retrying an authentication failure is pure waste. Retrying an oversized input is worse — it burns quota to fail identically.

### 24.4 The Mock Provider

The mock is a first-class deliverable, not test scaffolding.

The blueprint's required behaviors:

```text
Fixed text responses.
Fixed structured responses.
Simulated invalid JSON.
Simulated timeout.
Simulated rate limit.
Simulated unsafe output.
```

Phase 01 adds the cases the runbooks imply:

| Scenario | Behavior | Used By |
|---|---|---|
| `success` | Deterministic text and usage | Happy path, API contract tests |
| `success_slow` | Sleeps below the route timeout | Latency measurement tests |
| `timeout` | Sleeps past the route timeout | P01-007 "simulated timeout test" |
| `rate_limited` | Rate-limit error, optionally with `Retry-After` | Backoff tests |
| `unavailable` | 5xx equivalent | Fallback and circuit breaker tests |
| `auth_failed` | Authentication error | No-retry tests |
| `invalid_json` | Text that is not valid JSON | Phase 03 groundwork |
| `unsafe_output` | Content flagged as unsafe | Phase 11 groundwork |
| `truncated` | `finish_reason: max_tokens` | Truncation handling |
| `usage_missing` | Omits usage fields | Null-usage handling |
| `fail_then_succeed` | Fails N times, then succeeds | Retry-succeeds tests |

Determinism rules:

```text
Same scenario plus same input produces the same output.
Failure counts are explicit, not probabilistic.
Nothing depends on wall-clock time of day.
Token counts follow a simple documented rule, for example characters divided by four.
```

The last rule matters more than it looks. If mock usage is a fixed constant, cost tests pass while the cost calculation is wrong. If mock usage varies with input, cost tests actually test arithmetic.

### 24.5 Adapter Registry

```text
provider_type        -> adapter class

openai_compatible    -> OpenAICompatibleAdapter
azure_openai         -> AzureOpenAIAdapter, may subclass the above
anthropic_compatible -> AnthropicCompatibleAdapter
local_vllm           -> OpenAICompatibleAdapter with local defaults
local_tgi            -> TGIAdapter
mock                 -> MockAdapter
```

An unknown `provider_type` must fail loudly at bootstrap, not at request time.

## 25. Error Model And Error Codes

### 25.1 The Envelope Is Already Defined

Phase 00 established the response shape. Phase 01 adds codes; it does not invent a new envelope.

```json
{
  "error": {
    "code": "ai.provider_timeout",
    "message": "The model provider did not respond in time.",
    "details": {
      "route_key": "rag_answer_primary",
      "attempts": 3,
      "ai_run_id": "0f2c3d8e-..."
    },
    "request_id": "req_123"
  }
}
```

### 25.2 Phase 01 Error Code Catalogue

| Code | Meaning | HTTP |
|---|---|---|
| `ai.route_not_found` | No route exists for the use case | 400 |
| `ai.route_unavailable` | Routes exist but none are active | 503 |
| `ai.route_misconfigured` | Route configuration is internally invalid | 500 |
| `ai.capability_unsupported` | Provider cannot do what the request needs | 400 |
| `ai.restricted_data_not_allowed` | No compliant route for restricted data | 403 |
| `ai.input_too_large` | Input exceeds the route or model cap | 413 |
| `ai.reasoning_budget_exceeded` | Requested reasoning exceeds route budget | 400 |
| `ai.cost_limit_exceeded` | Estimated cost exceeds route ceiling | 402 |
| `ai.budget_exceeded` | Tenant or platform budget exhausted | 402 |
| `ai.provider_not_configured` | Provider is active but has no credentials | 500 |
| `ai.provider_timeout` | Provider exceeded the route timeout | 504 |
| `ai.provider_rate_limited` | Provider returned a rate limit | 429 |
| `ai.provider_unavailable` | Provider connection failure or 5xx | 502 |
| `ai.provider_auth_failed` | Provider rejected credentials | 502 |
| `ai.provider_bad_request` | Provider rejected the request shape | 502 |
| `ai.provider_content_filtered` | Provider filtered the content | 422 |
| `ai.provider_invalid_response` | Response could not be parsed | 502 |
| `ai.all_routes_failed` | Primary and fallback both failed | 502 |
| `ai.embedding_dimension_mismatch` | Returned dimension differs from the route | 502 |

Phase 00 reserved the general categories `ai_provider_error`, `ai_output_invalid`, and `safety_blocked`. Phase 01's codes are the specific cases beneath the provider-error category; keep a general code available for anything unclassified.

### 25.3 Why Provider Failures Return 502, Not 500

A 500 says Atlas broke. A 502 says an upstream dependency broke. The distinction drives on-call routing, alert severity, and the message the user sees. The runbooks assume provider incidents can be told apart from Atlas incidents on a dashboard.

### 25.4 What Error Details May Contain

Safe: `route_key`, `use_case`, `provider_name`, `model_name`, `attempts`, `ai_run_id`, `retry_after_seconds`, and the `limit` and `actual` values for cap violations.

Never: API keys, raw provider error bodies, prompt text, user content, stack traces, or base URLs with embedded credentials.

Phase 00's rule stands — full detail is logged internally, a safe subset is returned.

## 26. Retry, Timeout, And Fallback Policy

### 26.1 Timeouts

Section 8.8 explains why these numbers matter more than they look: near saturation, latency grows asymptotically, so a timeout is the only thing bounding your own queue.

```text
effective_timeout = min(route.timeout_seconds, REQUEST_TIMEOUT_SECONDS)
```

Rules:

- The timeout applies per attempt, not to the whole retry sequence.
- Track a total deadline too, so three retries of a 30-second route cannot block a caller for 90 seconds or more.
- Streaming needs both a connect timeout and an inter-chunk timeout; a stream that stalls must not hang forever.

### 26.2 Retry Classification

The classes come from Section 8.9; the reason bounded retries matter is Section 8.8's congestion collapse.

The blueprint retries temporary network failures, provider timeouts, rate limits with backoff, and invalid structured output where repair is allowed. Structured-output repair is Phase 03, so Phase 01 retries the three transport cases:

```text
retryable = error in {
  ai.provider_timeout,
  ai.provider_rate_limited,
  ai.provider_unavailable
}
```

### 26.3 Backoff Formula

```text
delay_ms = min(base_delay_ms * (2 ** (attempt - 1)), max_delay_ms)
delay_ms = delay_ms * random.uniform(0.5, 1.5)      # jitter

if the provider supplied Retry-After:
    delay_ms = max(delay_ms, retry_after_ms)
```

With `base_delay_ms = 200` and `MODEL_MAX_RETRIES = 2`, worst-case added latency is roughly 200 ms plus 400 ms plus jitter — bounded and predictable.

Honoring `Retry-After` is not optional politeness. Ignoring it during a rate-limit event extends the outage.

### 26.4 Circuit Breaker

Pattern background, and its untouched sibling the bulkhead, are in Section 8.10.

```text
state: closed -> open -> half_open -> closed

closed:    calls pass through; count consecutive failures per (provider, model)
open:      calls fail immediately with ai.provider_unavailable, no provider call is made
half_open: after the cooldown, allow one probe; success closes, failure reopens
```

Threshold and cooldown come from settings. The breaker key should be `(provider_id, model_name)`, not the provider alone: one bad model should not disable a healthy provider's other models.

The breaker's real job is the outage runbook's instruction: "Increase retry backoff to avoid making the provider outage worse."

Modular-monolith caveat worth writing down: breaker state held in process memory means each API worker has its own view. That is acceptable in Phase 01. Sharing it through Redis is a Phase 18 improvement, and the limitation should be documented rather than discovered during an incident.

### 26.5 Fallback

Fallback is attempted only when all of these hold:

```text
the primary route failed with a retryable error and retries are exhausted,
   OR the circuit breaker for the primary route is open,
AND route.fallback_route_id is not null,
AND the fallback route passes every filter the original request passed,
AND fallback depth has not been reached.
```

The critical clause is the third. A fallback route must be re-validated against data policy and capability. A restricted-data request must never reach a non-compliant fallback — which is exactly why `rag_answer_private` declares no fallback at all.

If primary and fallback both fail, return `ai.all_routes_failed` and record both attempts on the run.

### 26.6 One Run, Many Attempts

```text
ai_run                      <- one row per logical gateway request
  attempt 1: primary route, timeout
  attempt 2: primary route, timeout
  attempt 3: fallback route, success
```

The run's `provider_name`, `model_name`, and `model_route_id` record the attempt that ultimately served the request. `latency_ms` covers the whole sequence. Attempt-level detail belongs in the redacted `response_json`, in logs, and in spans.

The reasoning: one caller request should produce one row in cost and reliability reports. A row per attempt would triple-count failures and make "how many AI requests did we serve" unanswerable. The outage runbook's diagnosis step — "`ai_runs` grouped by provider, model, route, status, and error type" — works precisely because of this convention.

## 27. Token Counting And Cost Estimation

### 27.1 Two Different Numbers

| Number | When | Purpose | Accuracy |
|---|---|---|---|
| Pre-call estimate | Before the provider call | Enforce `max_input_tokens`, `max_cost_usd`, budgets | Approximate |
| Post-call actual | After the response | `ai_runs`, `cost_records`, dashboards | Provider-reported |

Never overwrite an actual with an estimate. If a provider returns no usage, store `null` and record why. Cost reporting must be able to distinguish "cost zero" from "cost unknown".

### 27.2 Pre-Call Estimation In Phase 01

Section 8.2 explains why this can only ever be a heuristic, and why the provider's count is authoritative.

A character-based heuristic is sufficient and honest:

```text
estimated_input_tokens ≈ total_characters / 4
```

Document it as a heuristic, use it only for guard rails, and never write it into a usage column. A real tokenizer improves the estimate and can be added later without changing any interface — which is exactly why the estimate lives behind a function instead of being inlined at call sites.

### 27.3 The Pricing Sheet

Output tokens cost several times input tokens in every real pricing sheet. Section 8.1 explains why that asymmetry is physical, not commercial.

```yaml
pricing_version: pricing_v1
currency: USD
effective_from: 2026-01-01
models:
  high-quality-chat-model:
    input_token: 0.0000030
    output_token: 0.0000150
    reasoning_token: 0.0000150
    cache_write_token: 0.0000038
    cache_read_token: 0.0000003
  cheap-fast-model:
    input_token: 0.0000002
    output_token: 0.0000008
  embedding-model-large:
    input_token: 0.0000001
  judge-capable-model:
    input_token: 0.0000030
    output_token: 0.0000150
    reasoning_token: 0.0000150
```

Rules:

- The sheet is versioned, and `pricing_version` is written to every cost record.
- A missing model entry is a loud failure at bootstrap, not a silent zero at runtime.
- Prices are `Decimal`, never `float`. The schema uses `numeric(18,9)` for unit cost for a reason.
- When prices change, add a new sheet version. Never edit historical rates, because that silently rewrites past reports.

The `billing_unit` values map directly onto the schema's enumerated list: `input_token`, `output_token`, `reasoning_token`, `cache_write_token`, `cache_read_token`, `image`, `audio_second`, `video_second`, `request`.

### 27.4 Cost Calculation

```text
for each usage field with a non-null value:
    billing_unit = mapping[field]
    quantity     = usage value
    unit_cost    = pricing[model][billing_unit]
    line_cost    = quantity * unit_cost
    write cost_record(...)

ai_runs.estimated_cost_usd = sum(line_cost), rounded once to 6 decimal places
```

Field-to-unit mapping:

| Usage Field | `billing_unit` |
|---|---|
| input_tokens | `input_token` |
| output_tokens | `output_token` |
| reasoning_output_tokens | `reasoning_token` |
| cache_creation_input_tokens | `cache_write_token` |
| cache_read_input_tokens | `cache_read_token` |

Rounding rule: compute every line at full `numeric(18,9)` precision, sum, then round once. Rounding each line first accumulates error across millions of calls.

Double-counting warning: some providers report cached input tokens inside `input_tokens`, others report them separately. The adapter normalizes this so the same tokens are not billed twice. Write an adapter-level test for it, because the bug is invisible until someone reconciles against a provider invoice.

### 27.5 Actual Versus Estimated Cost

`cost_records.actual_cost_usd` is nullable because Atlas usually knows the estimate at call time and the real invoice much later. Phase 01 writes `estimated_cost_usd` and leaves `actual_cost_usd` null. A future reconciliation job fills it in. The column exists now so that job does not require a migration later.

## 28. AI Run Lifecycle And Persistence

### 28.1 State Machine

```text
                 policy rejection
request  ------------------------> blocked (terminal)
   |
   v
queued -> running -> succeeded (terminal)
             |
             +-----> failed (terminal)
             |
             +-----> cancelled (terminal)
```

### 28.2 Write Points

| Moment | Action |
|---|---|
| After route selection succeeds | Insert run with `status='running'`, route, provider, model, use case, request hash, redacted input preview, trace id |
| Policy rejection before any provider call | Insert run with `status='blocked'`, error code, no usage |
| Provider call succeeds | Update to `succeeded` with usage, cost, latency, output preview, finish reason |
| All attempts fail | Update to `failed` with error code, safe message, and consumed latency |
| Caller cancels or abandons | Update to `cancelled` |

Why insert before the call rather than after: a process that dies mid-call leaves a visible `running` row. Writing only on completion means crashed calls vanish — and the money they spent vanishes with them.

Why create a row even for `blocked`: governance. "Show me every restricted-data request that was refused" is a compliance question, and it is answerable only if refusals are recorded.

Practical note: commit the initial insert in its own short transaction. Holding a database transaction open across a 30-second model call ties a connection to network latency and will exhaust the pool under load.

### 28.3 Stuck Runs

A run left in `running` after a crash needs cleanup. Phase 01 can keep it simple:

```text
A run in 'running' older than (route timeout + margin) is stale.
A maintenance query or worker job marks stale runs as 'failed'
with error_code = 'ai.run_abandoned'.
```

Document the rule even if the job is not built yet, so nobody misreads a stale row as an active call.

### 28.4 Request Hash

```text
request_hash = sha256(
    canonical_json({
        use_case,
        model_name,
        normalized_messages_or_inputs,
        temperature,
        max_output_tokens,
        response_schema_id or null
    })
)
```

Canonicalization must be stable: sorted keys, normalized whitespace, fixed number formatting. An unstable hash produces different values for identical requests and destroys its own usefulness.

The hash intentionally excludes `tenant_id`, `user_id`, `request_id`, and timestamps, so identical work is recognizable across tenants and time. Phase 20 semantic caching will need per-tenant scoping in its own cache key — that is a cache concern, not a hash concern.

### 28.5 Linking To Later Phases

`conversation_id`, `agent_run_id`, and `prompt_version_id` are nullable in Phase 01 and populated by Phases 06, 09, and 02. The gateway should accept them in request metadata and store them when present. Doing this now means those phases require no gateway change — only a caller change.

## 29. Redaction Rules

### 29.1 Why This Section Exists

`ai_runs` will hold the highest concentration of sensitive content in the platform: user questions, document excerpts, and model answers. Phase 00 already forbade logging raw private documents and sensitive prompts. Phase 01 makes those rules concrete at the storage layer.

The crosswalk maps this to OWASP LLM02 Sensitive Information Disclosure and to LLM07 System Prompt Leakage, whose listed controls include "prompt redaction in logs" and "redacted ai_runs".

The crosswalk also states the rule directly, in its privacy note under the GenAI attribute list:

```text
Do not capture full prompts, messages, memory records, retrieved documents, or
tool arguments by default. These may contain sensitive or private data. Capture
only redacted previews unless a tenant explicitly opts in.
```

Two words in that rule set the defaults for this whole section: **by default**, and **opts in**. Full capture is off unless a tenant turns it on, which is why `AI_RUN_STORE_REQUEST_JSON` and `AI_RUN_STORE_RESPONSE_JSON` default to `false` and are additionally gated on tenant policy.

### 29.2 The Four Content Columns

| Column | Default | Rule |
|---|---|---|
| `input_preview` | populated | Truncate to `AI_RUN_PREVIEW_MAX_CHARS`, strip detected secrets |
| `output_preview` | populated | Same treatment |
| `request_json` | null | Stored only when `AI_RUN_STORE_REQUEST_JSON=true` and tenant policy allows |
| `response_json` | null | Stored only when `AI_RUN_STORE_RESPONSE_JSON=true` and tenant policy allows |

The schema comments say it directly: "redacted full request if allowed". Both conditions matter — a platform flag and a tenant policy.

### 29.3 Always Stripped

```text
Authorization headers and any header carrying a credential
API keys matching known key patterns
Provider base URLs containing embedded credentials
System prompt text when the tenant marks prompts confidential
Any field the tenant policy names as sensitive
```

### 29.4 Never Redacted

Metadata is not content, and redacting it destroys the operational value of the table:

```text
use_case, provider_name, model_name, model_route_id
status, error_code, all token counts, cost, latency
trace_id, request_hash, timestamps
```

### 29.5 Restricted-Data Tenants

For a tenant flagged as restricted, the safe default is:

```text
input_preview  = null
output_preview = null
request_json   = null
response_json  = null
metadata       = retained in full
```

The run still proves the call happened, what it cost, and how it performed, without retaining content. This is the pattern that lets a regulated tenant use the platform while still appearing in cost and reliability reports.

### 29.6 Testing Redaction

Redaction that is not tested is redaction that does not exist:

```text
test_api_key_pattern_removed_from_preview
test_preview_truncated_to_configured_length
test_request_json_absent_when_flag_disabled
test_restricted_tenant_stores_no_content
test_error_details_never_include_provider_body
test_logs_never_contain_message_content
```

## 30. Streaming In Phase 01

### 30.1 What The Blueprint Requires

```text
API receives chat request
-> gateway starts provider stream
-> chunks sent to frontend
-> final text assembled server-side
-> final ai_run stored with usage and metadata
```

The rule embedded in that flow: streaming must not weaken logging. A streamed response produces the same `ai_runs` row as a non-streamed one.

### 30.2 Phase 01 Scope

Build:

- A server-side stream assembler that accumulates text deltas.
- `time_to_first_chunk_ms` measurement.
- Final usage capture from the stream's terminal event when the provider sends one.
- Normalized stream events for the API layer.
- An inter-chunk timeout that fails a stalled stream.

Defer, per the coverage matrix:

- Streaming tool calls — Phase 20.
- Partial structured output streaming — Phase 20.
- Frontend streaming UI — Phase 19.

### 30.3 Event Names

The blueprint's suggested event types, of which Phase 01 needs the first and the last two:

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

Using the documented names now, even for a subset, means Phases 08 and 09 extend a vocabulary instead of replacing one.

### 30.4 The Usage Problem

Some providers do not report token usage on streamed responses, or report it only in a final event that is missed if the client disconnects.

```text
stream completes with a usage event -> store actual usage
stream completes without usage      -> store null usage and set a metadata flag
client disconnects mid-stream       -> finalize the run from server-side
                                       accumulated text; never lose the row
```

Never substitute an estimate into the usage columns. A null with an explanation is more useful than a number that looks authoritative and is wrong.

## 31. API Design

### 31.1 Endpoints

The blueprint's §13.7 list:

```text
POST /api/v1/models/chat
POST /api/v1/models/structured
POST /api/v1/models/embed
GET  /api/v1/models/routes
POST /api/v1/models/routes
GET  /api/v1/ai-runs/{ai_run_id}
```

Phase 01 implements:

| Endpoint | Phase 01 Status |
|---|---|
| `POST /api/v1/models/chat` | implemented |
| `POST /api/v1/models/embed` | implemented |
| `GET /api/v1/models/routes` | implemented, read-only listing |
| `GET /api/v1/ai-runs/{ai_run_id}` | implemented |
| `POST /api/v1/models/routes` | admin-only, required — see below |
| `POST /api/v1/models/structured` | deferred to Phase 03 |

The blueprint notes these "can be internal first, public later". Phase 01 treats them as internal, admin- and developer-facing. Ticket P01-008 asks only for "an internal model test endpoint or service call" whose proof is that it returns an `ai_run` id.

#### Why Route Mutation Is Not Optional

It is tempting to defer `POST /api/v1/models/routes` to the admin UI phase, since Phase 01 has no frontend. It cannot be deferred, because three other parts of this phase assume routes can change at runtime:

- Section 22.3 requires that "route changes through the admin API invalidate the cache immediately".
- Section 33.7 requires an audit event on every route create, update, enable, and disable — which needs a code path that performs those changes.
- Section 40.3's entire operator-actions table depends on disabling a route, repointing a fallback, or pinning a model back **without a deploy**. That is the capability the provider outage runbook assumes exists.

So Phase 01 needs one of these, and must state which:

**Option A, recommended.** Implement route mutation as an admin-only endpoint, with permission checks and audit records. Small surface — status toggle, model name, priority, limits, fallback — and it satisfies the runbook.

**Option B.** Operators change routes by editing configuration and re-running bootstrap. Legitimate for a single-operator local build, but it means route changes require filesystem access and a deploy, the audit trail is the git history rather than `audit_events`, and Section 22.3's cache invalidation has no trigger. If this is chosen, say so plainly in the runbook and drop the "without a deploy" claim from Section 40.3.

The minimum honest position is that Phase 01 cannot claim runbook-ready operability while leaving route mutation unbuilt.

### 31.2 Chat Request Example

```json
POST /api/v1/models/chat
{
  "use_case": "chat",
  "messages": [
    {"role": "system", "content": "You are a support assistant."},
    {"role": "user", "content": "How long is the refund window?"}
  ],
  "temperature": 0.2,
  "max_output_tokens": 500,
  "restricted_data": false,
  "metadata": {
    "feature": "support_console",
    "conversation_id": null
  }
}
```

`tenant_id` and `user_id` come from the authenticated context, never from the body. Accepting a caller-supplied `tenant_id` would be a tenant-isolation hole.

### 31.3 Chat Response Example

```json
200 OK
{
  "ai_run_id": "8b0f3a2e-1c44-4d8a-9f0b-2b5f1c7a44e1",
  "route_key": "chat_primary",
  "provider_name": "openai_primary",
  "model_name": "high-quality-chat-model",
  "output_text": "Refunds are available within 30 days of purchase.",
  "finish_reason": "completed",
  "usage": {
    "input_tokens": 48,
    "output_tokens": 17,
    "reasoning_output_tokens": null,
    "cache_creation_input_tokens": null,
    "cache_read_input_tokens": null
  },
  "estimated_cost_usd": "0.000399",
  "latency_ms": 812,
  "attempts": 1,
  "used_fallback": false
}
```

`estimated_cost_usd` is serialized as a string. Sending a decimal money value as a JSON number invites float rounding in any client that parses it naively.

### 31.4 Embed Request And Response

```json
POST /api/v1/models/embed
{
  "use_case": "embedding",
  "inputs": ["first chunk of text", "second chunk of text"],
  "metadata": {"document_id": "...", "job_id": "..."}
}
```

```json
200 OK
{
  "ai_run_id": "…",
  "route_key": "embedding_primary",
  "provider_name": "openai_primary",
  "model_name": "embedding-model-large",
  "embedding_dimension": 1536,
  "embeddings": [[0.013, -0.208], [0.041, 0.117]],
  "usage": {"input_tokens": 214, "output_tokens": null},
  "estimated_cost_usd": "0.000021",
  "latency_ms": 143
}
```

The vectors above are truncated for readability; a real response returns `embedding_dimension` values per input, in input order.

### 31.5 Routes Listing

```json
GET /api/v1/models/routes?use_case=rag_answer
{
  "items": [
    {
      "route_key": "rag_answer_primary",
      "use_case": "rag_answer",
      "provider_name": "openai_primary",
      "model_name": "high-quality-chat-model",
      "priority": 1,
      "status": "active",
      "reasoning_enabled": false,
      "prompt_caching_enabled": true,
      "restricted_data_allowed": false,
      "fallback_route_key": "rag_answer_private"
    }
  ]
}
```

These are exactly the columns the UX specification lists for the Routes tab: use case, provider, model, priority, status, reasoning, prompt caching, restricted data allowed, fallback.

### 31.6 AI Run Detail

```json
GET /api/v1/ai-runs/{ai_run_id}
{
  "id": "…",
  "use_case": "rag_answer",
  "provider_name": "openai_primary",
  "model_name": "high-quality-chat-model",
  "route_key": "rag_answer_primary",
  "prompt_version_id": null,
  "status": "succeeded",
  "usage": {
    "input_tokens": 3120,
    "output_tokens": 412,
    "reasoning_output_tokens": null,
    "cache_creation_input_tokens": 1024,
    "cache_read_input_tokens": 0
  },
  "estimated_cost_usd": "0.004512",
  "latency_ms": 1840,
  "time_to_first_chunk_ms": 410,
  "trace_id": "…",
  "created_at": "2026-01-01T10:00:00Z",
  "input_preview": "How long is the refund window?",
  "output_preview": "Refunds are available within 30 days…"
}
```

The UX specification's AI run detail expects provider, model, prompt version, operation name, token usage, cache tokens, reasoning tokens, cost, latency, and linked records. Phase 01 supplies everything except the links that later phases create.

Authorization rule: a run may only be read by a caller in the run's tenant. This deserves an explicit cross-tenant test, since the crosswalk lists cross-tenant tests as required evidence for tenant isolation.

### 31.7 Pagination

Route listings, and any later run listings, follow the blueprint's pagination standards rather than inventing a new scheme. Even a small list should paginate from the start; retrofitting pagination after clients depend on an unbounded array is a breaking change.

## 32. Observability

### 32.1 Ticket P01-009

```text
P01-009 | Observability | Emit GenAI span fields | trace sample contains model/request attrs
```

The crosswalk explains the naming discipline: the OpenTelemetry GenAI conventions live in a separate semantic conventions repository, "Atlas should use current names from that repository and keep provider-specific attributes separate from generic Atlas fields."

### 32.2 Span Attributes Phase 01 Emits

From the crosswalk's recommended generic attribute list, these apply to a gateway call:

```text
gen_ai.operation.name
gen_ai.provider.name
gen_ai.request.model
gen_ai.response.model
gen_ai.request.max_tokens
gen_ai.request.temperature
gen_ai.request.top_p
gen_ai.request.stream
gen_ai.request.reasoning.level
gen_ai.response.finish_reasons
gen_ai.response.id
gen_ai.response.time_to_first_chunk
gen_ai.usage.input_tokens
gen_ai.usage.output_tokens
gen_ai.usage.reasoning.output_tokens
gen_ai.usage.cache_creation.input_tokens
gen_ai.usage.cache_read.input_tokens
gen_ai.prompt.name
gen_ai.prompt.version
gen_ai.output.type
```

`gen_ai.prompt.name` and `gen_ai.prompt.version` stay empty until Phase 02. `gen_ai.retrieval.*`, `gen_ai.tool.*`, and `gen_ai.agent.*` belong to Phases 06, 08, and 09.

### 32.3 Atlas-Specific Attributes

Keep Atlas fields under their own namespace so they are never confused with standard ones. The crosswalk §8 already defines part of this namespace, so Phase 01 reuses its exact names rather than inventing parallel ones:

Defined by the crosswalk, used by Phase 01:

```text
atlas.tenant.id
atlas.user.id
atlas.ai_run.id
atlas.cost.estimated_usd
```

New in Phase 01, following the same dotted-segment convention:

```text
atlas.route.key
atlas.route.id
atlas.use_case
atlas.attempts
atlas.used_fallback
atlas.circuit_breaker.state
atlas.pricing.version
```

The naming convention matters as much as the names. The crosswalk uses dotted segments (`atlas.ai_run.id`, not `atlas.ai_run_id`), so new attributes must follow that shape or the namespace stops being queryable as a hierarchy. Any attribute added here should be proposed back into the crosswalk's list, so the two documents do not diverge again — Section 16.5 exists because exactly that drift happened with token names.

The crosswalk's rule — keep provider-specific attributes separate from generic Atlas fields — is what this namespace separation implements.

### 32.4 Span Structure

```text
span: atlas.model_gateway.request        (one per logical gateway call)
  |
  +-- span: atlas.model_gateway.route_selection
  +-- span: gen_ai.chat  (attempt 1, may fail)
  +-- span: gen_ai.chat  (attempt 2, retry)
  +-- span: atlas.model_gateway.cost_calculation
  +-- span: atlas.model_gateway.run_persistence
```

The parent span mirrors the `ai_runs` row; child attempt spans mirror the attempts. This is what makes a trace and a run record line up during an incident.

### 32.5 Transport In Phase 01

The blueprint puts the full observability stack in Phase 18. Phase 01 should not build exporters, collectors, or dashboards.

Phase 01's obligation is smaller and more important: emit the correct attribute **names** through structured logs now, so that Phase 18 changes the transport without renaming anything.

Log line shape:

```json
{
  "timestamp": "2026-01-01T10:00:00Z",
  "level": "INFO",
  "event": "model_gateway.request_completed",
  "request_id": "req_123",
  "trace_id": "…",
  "atlas.ai_run.id": "…",
  "atlas.tenant.id": "…",
  "atlas.use_case": "rag_answer",
  "atlas.route.key": "rag_answer_primary",
  "gen_ai.provider.name": "openai_primary",
  "gen_ai.request.model": "high-quality-chat-model",
  "gen_ai.usage.input_tokens": 3120,
  "gen_ai.usage.output_tokens": 412,
  "gen_ai.response.finish_reasons": ["completed"],
  "atlas.cost.estimated_usd": "0.004512",
  "latency_ms": 1840,
  "status": "succeeded"
}
```

No message content appears anywhere in that line. That is deliberate and should be enforced by a test.

### 32.6 Metrics Worth Counting Now

Even without a metrics backend, count these in a way Phase 18 can export:

| Metric | Type | Labels |
|---|---|---|
| `model_requests_total` | counter | use_case, route_key, provider, model, status |
| `model_request_duration_ms` | histogram | use_case, route_key, provider, model |
| `model_tokens_total` | counter | use_case, model, token_type |
| `model_cost_usd_total` | counter | tenant, use_case, model |
| `model_retries_total` | counter | route_key, error_code |
| `model_fallbacks_total` | counter | from_route, to_route |
| `circuit_breaker_state` | gauge | provider, model |

These are precisely the signals the runbooks alert on: provider error rate, p95 latency, timeout rate, fallback usage, retry count, and cost per minute.

### 32.7 The Events Every Gateway Call Logs

```text
model_gateway.request_received
model_gateway.route_selected        (includes rejected_routes)
model_gateway.attempt_started
model_gateway.attempt_failed        (includes error_code, retryable, delay_ms)
model_gateway.fallback_used
model_gateway.request_completed
model_gateway.request_failed
model_gateway.request_blocked       (includes policy reason)
```

`model_gateway.route_selected` with its rejection list is the single most useful log line in the whole phase. It converts "why that model?" from an investigation into a lookup.

## 33. Safety And Security Perspective

### 33.1 What Phase 01 Is Responsible For

Content safety — prompt injection, PII, harmful output — is Phase 11. Phase 01 owns the security of the *pipe*: credentials, isolation, policy enforcement, resource limits, and audit.

### 33.2 OWASP LLM Top 10 Mapping For Phase 01

From the crosswalk, the risks Phase 01 materially addresses:

| Risk | Phase 01 Contribution |
|---|---|
| LLM02 Sensitive Information Disclosure | Provider data policy, restricted-data routing, redacted `ai_runs`, no keys in database or logs |
| LLM03 Supply Chain | `model_providers` is the provider registry the crosswalk names as the implementation artifact; pinned model names instead of floating aliases |
| LLM05 Improper Output Handling | Normalized finish reasons and provider response validation; full schema validation arrives in Phase 03 |
| LLM10 Unbounded Consumption | Route token caps, `max_cost_usd`, tenant budgets, retry caps, circuit breaker, timeouts — the crosswalk lists `cost_records` and model route limits as the artifacts and "cost spike tests, budget alert tests" as the proof |

### 33.3 Model Alias Pinning

Section 8.16 explains the drift mechanism this defends against.

The outage runbook lists this failure explicitly: "A provider silently changes a model alias and output quality drops." Its recovery action is "Pin route to previous known model ID; avoid floating aliases", and its prevention item is "Add model alias pinning rule".

Phase 01 implementation:

```text
model_routes.model_name stores a specific, versioned model identifier.
Changing model_name is a reviewed configuration change with an audit record.
The ai_run stores the model name actually used, so a change is visible in history.
```

This is a small rule that prevents a whole category of unexplainable quality regressions.

### 33.4 Server-Side Request Forgery Risk

`model_providers.base_url` is an operator-supplied URL that the server then requests. That is a classic SSRF surface.

Controls:

```text
Only administrators may create or modify providers.
Validate the scheme: https for external providers; http only for explicitly
  allowed internal hosts such as a local model server.
Maintain an allowlist of permitted hosts per environment.
Do not follow redirects to different hosts on provider calls.
Never echo the resolved base_url in an error returned to a caller.
```

The routing document's own examples include `http://model-server:8000/v1`, so plain HTTP must be permitted for private-network providers — which is exactly why the control is an allowlist rather than a blanket scheme rule.

### 33.5 Authorization Rules

| Action | Required |
|---|---|
| Call `POST /models/chat` or `/models/embed` | Authenticated user with a tenant context |
| Use `model_override` | Explicit elevated permission, plus an audit record |
| Read `GET /ai-runs/{id}` | Caller must belong to the run's tenant |
| List routes | Authenticated user; global plus own-tenant routes only |
| Create or modify routes | Administrator only, with an audit record |
| Run bootstrap | Administrator or deployment process only |

### 33.6 Denial-Of-Wallet

An authenticated user who can call the gateway can spend money. Cost limits are therefore a security control, not only a finance control.

Minimum Phase 01 defenses:

```text
Route max_input_tokens and max_output_tokens
Route max_cost_usd where configured
Tenant daily budget check before route selection completes
Hard retry cap
Circuit breaker
Request size limit at the API layer, before token estimation
```

The crosswalk's LLM10 verification proof is "cost spike tests, budget alert tests" — write both.

### 33.7 Audit

Route and provider changes are governance events. The blueprint's `audit_events` table records `subject_type` values including `model_route`. Every create, update, enable, and disable of a provider or route should write one, with `before_json` and `after_json`.

The outage runbook's validation step requires it directly: "Confirm route change audit records exist."

## 34. Multi-Tenancy

### 34.1 The Rule

Blueprint principle 3.5: every user-visible object belongs to a tenant, and the list of such objects explicitly includes AI runs.

```text
ai_runs.tenant_id      not null
cost_records.tenant_id not null
model_routes.tenant_id nullable, where null means a global route
```

`model_routes` is the deliberate exception, and the reason is operational: most routes are platform defaults, and only some tenants need overrides. The two partial unique indexes exist to make that dual meaning safe.

### 34.2 Enforcement Points

```text
Route selection: filter to tenant_id = :tenant or tenant_id is null
Run creation:    tenant_id from the authenticated context, never from the body
Run reads:       filter by tenant_id, always
Cost queries:    group by tenant_id
Budget checks:   scope to tenant_id
```

### 34.3 Cross-Tenant Tests Are Required Evidence

The crosswalk lists tenant isolation evidence as "cross-tenant tests, ACL-filtered retrieval proof". For Phase 01 that means at minimum:

```text
test_tenant_a_cannot_read_tenant_b_ai_run
test_tenant_route_not_selected_for_other_tenant
test_global_route_available_to_all_tenants
test_tenant_override_beats_global_route
test_cost_records_scoped_to_tenant
```

### 34.4 Ordering Note On Tenant-Scoped Routes

Global routes work with the identity tables Phase 00 already created. Tenant-scoped routes, tenant budgets, and per-tenant policy all depend on knowing which tenant a caller belongs to and what they are allowed to do — that is membership and role-based access control, which the blueprint places in the identity domain.

Practical sequencing advice: build and ship global routes first. Treat tenant-scoped routing as gated on tenant membership and RBAC being real, not on a `tenant_id` value being present in a request body. A tenant column that anyone can set is not isolation.

This is a narrower question than the one in Section 4.1, and the two should not be confused:

| Question | Needs | Blocks |
|---|---|---|
| Can `ai_runs` and `cost_records` be written at all? | The `tenants` table to exist | All of Phase 01 — resolve via Section 4.1 |
| Can a *tenant-scoped route* be trusted? | Membership and RBAC, so the caller's tenant is proven rather than asserted | Only tenant overrides; global routes work without it |

The tests in Section 36 reflect that split. `test_global_route_available_to_all_tenants` runs as soon as the identity tables exist. `test_tenant_route_beats_global_route` exercises router logic and can run against fixtures with a seeded tenant context, but shipping tenant-scoped routing to real traffic should wait for real membership checks. Write both tests now; gate the *feature*, not the *test*.

## 35. Evaluation Perspective

### 35.1 What Can And Cannot Be Evaluated Yet

Phase 00 drew the distinction:

```text
Software test:   Given input X, function returns exactly Y.
AI evaluation:   Given input X, model output is judged for correctness,
                 groundedness, citation accuracy, safety, and usefulness.
```

Phase 01 has no prompts, no retrieval, and no ground truth. Answer quality cannot be evaluated yet — that is Phase 07.

What Phase 01 can and must measure is *engineering* quality of model access.

### 35.2 Phase 01 Measurements

| Measurement | Source | Why It Matters |
|---|---|---|
| Success rate per route | `ai_runs.status` | Reliability baseline |
| p50 and p95 latency per route | `ai_runs.latency_ms` | The SLO baseline the runbooks alert against |
| Retry rate | attempt counts | Early warning of provider trouble |
| Fallback rate | `used_fallback` | Primary route health |
| Cost per call and per 1,000 calls | `cost_records` | Budget planning |
| Token distribution | usage columns | Input growth detection |
| Block rate by reason | `status='blocked'` plus `error_code` | Policy friction and misconfiguration |

### 35.3 Why This Baseline Matters Later

Section 8.12 is the argument for why this is a deliverable: it is the denominator of every later cost-versus-quality comparison.

Every later phase changes these numbers. Phase 02 changes prompts and therefore input tokens. Phase 06 adds retrieved context and multiplies them. Phase 20 tries to reduce them.

Without a Phase 01 baseline, no later phase can prove improvement. The cost runbook's diagnosis step — "p95 input tokens jumps after deploy" — presupposes that someone recorded what p95 was before.

Capture and commit a baseline report at the end of Phase 01. It is a portfolio artifact and a debugging tool.

### 35.4 The Judge Route Exists But Is Not Used

`llm_judge_primary` is configured in Phase 01 because ticket P01-005 lists judge routing. Ticket P07-006 is what actually adds "LLM-as-judge behind gateway", with the proof "judge ai_runs stored".

Configuring the route now and using it later is correct sequencing: Phase 07 will need no gateway change.

## 36. Testing Strategy

### 36.1 The Governing Constraint

Ticket P01-004: "no tests require real model key."

Every test below runs against the mock provider. The real adapter is exercised only by an opt-in smoke test, per ticket P01-003's "smoke test behind env flag".

### 36.2 Unit Tests

```text
tests/model_gateway/test_contracts.py
  test_chat_request_rejects_missing_use_case
  test_chat_request_rejects_empty_messages
  test_restricted_data_defaults_from_tenant_policy_not_false
  test_usage_allows_null_fields

tests/model_gateway/test_router_selection.py
  test_selects_highest_priority_active_route
  test_tenant_route_beats_global_route
  test_disabled_route_is_skipped
  test_tie_break_is_deterministic
  test_route_decision_records_rejected_routes
  test_restricted_request_selects_compliant_private_route
  test_unrestricted_request_still_prefers_public_primary_route

tests/model_gateway/test_router_rejection.py
  test_unknown_use_case_raises_route_not_found
  test_restricted_data_rejected_on_public_route
  test_missing_capability_rejected_before_provider_call
  test_input_over_max_tokens_rejected
  test_output_over_max_tokens_is_clamped
  test_reasoning_budget_over_route_budget_handled_by_policy
  test_cost_over_route_ceiling_rejected
  test_fallback_cycle_detected

tests/model_gateway/test_retries.py
  test_timeout_is_retryable
  test_rate_limit_is_retryable
  test_auth_failure_is_not_retryable
  test_input_too_large_is_not_retryable
  test_backoff_grows_exponentially
  test_backoff_applies_jitter_within_bounds
  test_retry_after_header_is_honored
  test_max_retries_is_enforced
  test_circuit_breaker_opens_after_threshold
  test_circuit_breaker_half_open_probe_closes_on_success

tests/model_gateway/test_token_usage.py
  test_provider_usage_names_normalized
  test_missing_usage_becomes_null_not_zero
  test_cached_tokens_not_double_counted

tests/model_gateway/test_cost.py
  test_cost_uses_decimal_not_float
  test_cost_rounds_once_at_the_end
  test_missing_model_price_fails_loudly
  test_cost_records_created_per_billing_unit
  test_pricing_version_recorded
```

### 36.3 Integration Tests

```text
tests/model_gateway/test_ai_run_persistence.py
  test_run_created_before_provider_call
  test_run_finalized_with_usage_and_cost
  test_failed_run_records_error_code
  test_blocked_run_created_for_policy_rejection
  test_retries_produce_one_run_not_three
  test_fallback_run_records_fallback_provider

tests/model_gateway/test_fallback.py
  test_primary_failure_uses_fallback
  test_null_fallback_does_not_downgrade_private_route
  test_fallback_revalidates_data_policy
  test_both_routes_failing_returns_all_routes_failed

tests/model_gateway/test_bootstrap.py
  test_loading_twice_changes_nothing
  test_dangling_fallback_route_key_rejected
  test_unknown_provider_key_rejected
  test_fallback_cycle_rejected
  test_route_requiring_missing_capability_rejected
  test_embedding_route_without_dimension_rejected
  test_fallback_key_resolved_to_fallback_route_id
  test_nothing_written_when_validation_fails

tests/model_gateway/test_redaction.py       (Section 29.6 list)
tests/model_gateway/test_observability_fields.py
  test_completed_log_contains_required_gen_ai_attributes
  test_logs_never_contain_message_content
```

### 36.4 Contract And API Tests

```text
tests/api/test_model_gateway.py
  test_chat_returns_ai_run_id
  test_chat_response_matches_schema
  test_embed_preserves_input_order
  test_embed_dimension_mismatch_returns_error
  test_error_envelope_shape_on_provider_failure
  test_request_id_header_present_on_error
  test_routes_listing_filters_by_use_case
  test_caller_cannot_set_tenant_id_in_body

tests/api/test_ai_runs.py
  test_run_detail_returns_usage_and_cost
  test_tenant_a_cannot_read_tenant_b_run
  test_unknown_run_returns_not_found
```

### 36.5 Migration Tests

Listed in Section 19.5.

### 36.6 Optional Smoke Test

```text
tests/smoke/test_real_provider.py
  skipped unless ATLAS_ENABLE_PROVIDER_SMOKE_TEST=true
  performs one minimal request against the configured real provider
  asserts a run is created with non-null usage
```

Keep it minimal and cheap. Its purpose is to prove the adapter speaks the real protocol, not to test the gateway.

### 36.7 Test Fixtures

```text
tenant_fixture              -> a tenant row
restricted_tenant_fixture   -> a tenant with restricted-data policy
provider_fixtures           -> mock plus one disabled provider
route_fixtures              -> the nine routes from Section 21.3
mock_scenario(name)         -> configures mock behavior for one test
frozen_clock                -> deterministic latency and backoff assertions
pricing_fixture             -> a small deterministic pricing sheet
```

A frozen clock is what turns flaky timing tests into deterministic ones. Phase 00 already warned that "tests depend on real time" is a cause of flakiness.

## 37. Implementation Sequence

Build in this order. Each step leaves the repository in a working, testable state.

### Step 0: Resolve The Blocking Prerequisites

Before writing code, settle the four questions this document could not settle on its own. Each becomes a short decision record in `docs/decisions/`.

```text
[ ] Identity tables: Option A or Option B from Section 4.1
[ ] cost_records migration position: deferred FK or co-location, per Section 19.2
[ ] Canonical use_case vocabulary, per Section 7.4
[ ] Route mutation: admin endpoint or bootstrap-only, per Section 31.1
```

Steps 3 and 6 will fail without the first and third of these. Resolving them now costs an hour; discovering them mid-migration costs a day.

### Step 1: Write The Contracts

Create `contracts.py` with `ChatRequest`, `ChatMessage`, `ChatResponse`, `EmbeddingRequest`, `EmbeddingResponse`, `Usage`, and `RouteDecision`.

No dependencies, no I/O. Write `test_contracts.py` alongside.

Doing this first forces the interface decisions before any implementation locks them in.

### Step 2: Add Database Models

Create SQLAlchemy models for `model_providers`, `model_routes`, `ai_runs`, and `cost_records`, matching Section 18 exactly — every column, check constraint, and index.

### Step 3: Write The Migrations

Generate migrations, then review the generated SQL by hand. Autogeneration will not produce the partial unique indexes correctly; write those explicitly.

Run the Section 19.5 migration tests. Prove upgrade, downgrade, and re-upgrade on an empty database.

Ticket P01-001 is now provable.

### Step 4: Build The Adapter Interface And Mock Provider

Create `providers/base.py`, then `providers/mock.py` with every scenario from Section 24.4.

Test the mock directly: each scenario produces the documented behavior.

Tickets P01-002 and P01-004 are now provable.

Building the mock before the real adapter is deliberate. It forces the interface to be provider-neutral. An interface designed around one real provider always leaks that provider's assumptions.

### Step 5: Build The Bootstrap Loader

Create the two configuration files and `bootstrap.py` with two-pass key resolution, validation, cycle detection, and idempotent upsert.

Test that loading twice changes nothing and that every invalid configuration is rejected with a clear message.

### Step 6: Build The Router

Implement Section 22's algorithm and Section 23's rejection rules. Return a full `RouteDecision` including rejected routes.

Ticket P01-005 is now provable.

### Step 7: Build Usage Normalization And Cost

Create `token_usage.py`, the pricing sheet, and `cost.py`. Use `Decimal` throughout.

Ticket P01-006 is now provable once runs are persisted.

### Step 8: Build Run Persistence And Redaction

Create `runs.py`: create, finalize, and redact. Short transactions. Preview truncation. Restricted-tenant handling.

### Step 9: Build Retry, Timeout, And Circuit Breaker

Create `retries.py`. Wire the mock's `timeout`, `rate_limited`, `unavailable`, and `fail_then_succeed` scenarios into tests.

Ticket P01-007's "simulated timeout test" is now provable.

### Step 10: Assemble The Client

Create `client.py`, wiring Steps 1 through 9 into the lifecycle from Section 15.2.

This is the first point where an end-to-end mock request works. It should now be possible to make a chat call and open the resulting run record.

### Step 11: Add Fallback

Extend the client with fallback selection, re-validation, and depth limiting.

### Step 12: Build The Real Provider Adapter

Create `providers/openai_compatible.py`. Gate it behind `MODEL_GATEWAY_ENABLED` and a provider key. Map every error case in Section 24.3.

Ticket P01-003 is now provable via the opt-in smoke test.

### Step 13: Add Observability

Emit the Section 32 log events, attribute names, and counters.

Ticket P01-009 is now provable.

### Step 14: Add The API Layer

Create `apps/api/routes/model_gateway.py` and `apps/api/routes/ai_runs.py` plus their schemas. Wire tenant context, authorization, and the error envelope.

Ticket P01-008 is now provable.

### Step 15: Enforce Data Policy End To End

Add the restricted-data tests, the cross-tenant tests, and the provider data-policy checks.

Ticket P01-010 is now provable.

### Step 16: Add Streaming

Add the stream assembler, `time_to_first_chunk_ms`, and inter-chunk timeout. Keep run persistence identical to the non-streaming path.

### Step 17: Capture The Baseline

Run a small scripted workload against the mock provider. Record success rate, latency percentiles, token distribution, and cost per call. Commit the report.

### Step 18: Update Documentation

Update the README with gateway setup, bootstrap instructions, and new environment variables. Update `.env.example`. Write a short decision record for every choice this document flagged as a policy decision: the `cost_records` ordering resolution, clamp-versus-reject for reasoning budgets, fallback depth, and route caching.

## 38. Detailed Data Flows

### 38.1 Successful Chat Request

```text
client sends POST /api/v1/models/chat
-> request id middleware assigns request_id
-> auth resolves user and tenant
-> API schema validates the body
-> route handler builds a ChatRequest
-> gateway client validates and estimates input tokens
-> router loads candidate routes for use_case and tenant
-> router filters by capability, data policy, and budget
-> router returns RouteDecision(rag_answer_primary)
-> client clamps max_output_tokens to the route cap
-> runs.create() inserts ai_run with status='running'
-> adapter factory resolves provider_type and the API key
-> adapter builds the provider request and sends it with the route timeout
-> provider responds
-> adapter normalizes text, finish reason, and usage
-> token_usage maps usage into Atlas fields
-> cost calculates line items and the total
-> cost_records rows are written
-> runs.finalize() updates status='succeeded' with usage, cost, latency, preview
-> span and structured log are emitted
-> API serializes ChatResponse
-> response returns with X-Request-ID
```

### 38.2 Timeout With Successful Retry

```text
attempt 1 -> provider exceeds route timeout
          -> adapter raises ai.provider_timeout
          -> retries classifies it retryable
          -> delay = 200ms * jitter
          -> log model_gateway.attempt_failed
attempt 2 -> provider responds successfully
          -> run finalized: status='succeeded', attempts=2
          -> latency_ms includes both attempts and the delay
          -> exactly one ai_run row exists
```

### 38.3 Fallback

```text
attempt 1 -> ai.provider_unavailable
attempt 2 -> ai.provider_unavailable
          -> retries exhausted
          -> circuit breaker records failures
          -> fallback_route_id is present
          -> fallback route re-validated for capability and data policy
          -> log model_gateway.fallback_used
attempt 3 -> fallback provider responds successfully
          -> run finalized with the fallback provider and model
          -> used_fallback = true
          -> model_fallbacks_total incremented
```

### 38.4 Restricted Data Routed To A Compliant Provider

This is the path that must work. It is the reason `rag_answer_private` shares the `rag_answer` use case.

```text
request arrives for use_case = rag_answer
-> tenant policy resolves restricted_data = true
-> router loads candidates for rag_answer, ordered by priority:
     rag_answer_primary (priority 1), rag_answer_private (priority 2)
-> capability filter: both providers support chat            -> both survive
-> data policy filter:
     rag_answer_primary.restricted_data_allowed = false      -> rejected
     openai_primary.data_policy.restricted_data_allowed=false -> rejected
     rag_answer_private.restricted_data_allowed = true       -> survives
     azure_private_llm.data_policy.restricted_data_allowed=true -> survives
-> budget filter passes
-> first surviving candidate wins: rag_answer_private
-> RouteDecision records selection_reason and the rejection of the primary
-> ai_run created, provider called, run finalized as usual
-> no restricted content ever reached the public provider
```

Note that priority never had to be consulted to exclude the public route — the data policy filter did that. Priority only decides among routes that are all compliant. This is why an unrestricted request from the same tenant still gets `rag_answer_primary`: nothing filtered it out, and it has the lower priority number.

### 38.4a Restricted-Data Rejection

The rejection path is a genuine misconfiguration or a genuine policy gap, not a routing artifact. The clearest real case is a use case that has no private route at all.

```text
request arrives for use_case = llm_judge
-> tenant policy resolves restricted_data = true
-> router loads candidates for llm_judge:
     llm_judge_primary (priority 1)
-> capability filter passes
-> data policy filter:
     llm_judge_primary.restricted_data_allowed = false       -> rejected
-> no compliant route remains
-> runs.create() inserts ai_run with status='blocked',
   error_code='ai.restricted_data_not_allowed'
-> no provider call is made, no cost is incurred
-> 403 with the error envelope
-> the blocked run is available as governance evidence
```

The correct operational response is not to relax the flag on `llm_judge_primary`. It is either to add a private judge route or to accept that this tenant cannot use judged evaluation. A blocked run is the system working, and the record of it is what makes the gap visible instead of silent.

### 38.5 Budget Exhaustion

```text
request arrives
-> router resolves the route
-> budget check sums today's cost_records for the tenant
-> the sum exceeds the tenant budget
-> ai_run created with status='blocked', error_code='ai.budget_exceeded'
-> 402 returned
-> budget alert metric incremented
```

### 38.6 Embedding Batch

```text
worker calls the gateway with 100 inputs
-> router selects embedding_primary
-> batch size checked against max_batch_items
-> one ai_run created for the whole call
-> adapter sends the batch
-> response returns 100 vectors
-> order verified against input order
-> dimension verified against route embedding_dimension
-> usage recorded: input tokens only
-> one run, one cost record for input_token
-> vectors returned to the caller; storage is Phase 05's job
```

### 38.7 Total Failure

```text
attempt 1 -> ai.provider_unavailable
attempt 2 -> ai.provider_unavailable
fallback  -> ai.provider_unavailable
-> run finalized: status='failed', error_code='ai.all_routes_failed'
-> latency_ms reflects total elapsed time
-> usage null, cost null
-> 502 with the error envelope
-> circuit breaker opens for both provider/model pairs
-> provider outage runbook conditions are now visible on the dashboard
```

## 39. Failure Modes And Fixes

### 39.1 Every Request Costs More Than Expected

Causes: retries not counted in the mental model; the route's `max_output_tokens` too high; a fallback route more expensive than the primary; cached tokens double-counted.

Fixes: check `attempts` on the runs; compare cost by route; verify the adapter's cached-token handling; apply the cost runbook's corrective actions table.

### 39.2 Runs Stuck In `running`

Causes: the process died mid-call; an exception path skipped finalization; a transaction held open across the provider call.

Fixes: finalize in a `finally` block; commit the initial insert separately; add the stale-run sweep from Section 28.3.

### 39.3 Retry Storm During A Provider Outage

Causes: no circuit breaker; no jitter; `Retry-After` ignored; retry cap too high.

Fixes: exactly the runbook's list — exponential backoff, jitter, max retry cap, and circuit breaker.

### 39.4 Fallback Leaks Restricted Data

Cause: the fallback route was selected without re-validating data policy.

Fix: re-run every filter on the fallback route. Add `test_fallback_revalidates_data_policy`. This is the failure with the worst consequences in this phase; treat the test as mandatory, not optional.

### 39.5 Wrong Model Serving Traffic

Causes: two active routes share a priority with a non-deterministic tie-break; a tenant route was created accidentally; a floating model alias changed under you.

Fixes: deterministic tie-break; audit records on route changes; pinned model identifiers; inspect `ai_runs.model_route_id` for the affected period.

### 39.6 Embeddings Corrupt The Index Later

Causes: output order not preserved; dimension mismatch not validated; the route's model changed without reindexing.

Fixes: order and dimension assertions in the adapter; treat an embedding model change as an index-version change. The vector runbook's rule is unambiguous: "do not mix embedding dimensions/models in same index version."

### 39.7 Cost Records Do Not Match The Provider Invoice

Causes: pricing sheet out of date; cached tokens billed at the wrong rate; rounding per line; missing usage silently treated as zero.

Fixes: version the pricing sheet; round once; store null for unknown usage; use `actual_cost_usd` for reconciliation.

### 39.8 Tests Pass But Real Calls Fail

Cause: the mock is too forgiving — it never returns unusual finish reasons, missing usage, or malformed bodies.

Fix: expand mock scenarios to cover the ugly cases. A mock that only models success is a mock that hides bugs.

### 39.9 Secrets Appear In Logs

Causes: logging the whole request object; including the provider error body in error details; debug logging added during an incident and never removed.

Fixes: log allowlisted fields only, never whole objects; sanitize provider errors at the adapter boundary; add the redaction tests from Section 29.6.

### 39.10 Route Changes Do Not Take Effect

Causes: an in-process route cache with no invalidation; bootstrap not re-run; the change applied to a tenant route while traffic uses a global route.

Fixes: short TTL plus explicit invalidation, or no cache at all; check `ai_runs.model_route_id` to see which route actually served traffic.

## 40. Operations Perspective

### 40.1 Questions Phase 01 Must Be Able To Answer

```text
Which routes are active right now?
Which provider served this specific user request?
What did we spend today, by tenant and by route?
What is p95 latency per route?
What is the provider error rate over the last hour?
How often are we falling back?
Which route is the circuit breaker holding open?
How do I disable a route without a deploy?
How do I roll a route back to the previous model?
```

If any of these requires reading code, the phase is not operationally complete.

### 40.2 Alert Conditions

Straight from the runbooks:

| Signal | Condition |
|---|---|
| Provider error rate | `> 5% for 5 minutes` |
| p95 latency | `> route SLO for 10 minutes` |
| Timeout rate | `> 2% for 5 minutes` |
| Fallback usage | sharp increase |
| Cost per minute | exceeds budget envelope |
| Cost per tenant | daily budget threshold exceeded |
| Retry count | average retries per request increases |

Phase 01 produces the data. Phase 18 wires the alerting. Documenting the thresholds now means Phase 18 is configuration, not design.

### 40.3 Operator Actions Phase 01 Enables

| Situation | Action |
|---|---|
| Provider degraded | Set the route status to `disabled`; traffic moves to fallback |
| Model quality regressed | Change `model_name` back to the previous pinned identifier |
| Cost spike | Lower `max_output_tokens`, lower `max_cost_usd`, or disable an expensive route |
| Tenant abuse | Lower the tenant budget |
| Provider outage over | Re-enable the route and watch the error rate for 30 minutes |

Each of these is a data change with an audit record, not a code change.

### 40.4 Route Promotion Checklist

Before activating any new route, the routing document requires:

```text
[ ] Provider capability verified
[ ] Tenant data policy reviewed
[ ] Cost estimate configured
[ ] Timeout configured
[ ] Fallback policy configured
[ ] Eval suite passes
[ ] Safety suite passes
[ ] Observability fields tested
[ ] Rollback route exists where appropriate
[ ] Model card updated
```

In Phase 01, "eval suite passes" and "safety suite passes" cannot yet be satisfied — those arrive in Phases 07 and 11. Mark them as not-applicable-yet rather than deleting them. A checklist that quietly loses items is worse than one with honest gaps.

### 40.5 Graceful Degradation

The outage runbook specifies per-route behavior when no fallback exists:

```text
RAG answer route: return retrieval evidence with a temporary service message
Agent route:      pause planning and tool execution
Evaluation route: queue eval jobs for retry
Embedding route:  pause ingestion, keep read-only search available
Media route:      disable generation, preserve prompts for retry
```

Most of those routes do not exist yet. What Phase 01 must provide is the mechanism: a stable error code the caller can branch on, and a route status an operator can flip. Callers in Phases 06 and 09 implement their own degradation on top of it.

## 41. Frontend Surface

Phase 19 builds the console. Phase 01 makes its data real. The UX specification defines a Models screen:

```text
Tabs: Providers | Routes | AI Runs | Costs | Capabilities
```

| Tab | Backed By |
|---|---|
| Providers | `model_providers` including capability and data policy |
| Routes | `model_routes` with the nine listed columns |
| AI Runs | `ai_runs` |
| Costs | `cost_records` |
| Capabilities | `capabilities_json` |

Route detail is specified to show capabilities, token limits, reasoning budget, cache configuration, data policy, eval score, cost profile, and rollback route. Of those eight:

| Route Detail Field | Phase 01 Status |
|---|---|
| Capabilities | `capabilities_json` |
| Token limits | `max_input_tokens`, `max_output_tokens` |
| Reasoning budget | `reasoning_enabled`, `reasoning_effort`, `reasoning_budget_tokens` |
| Cache configuration | `prompt_caching_enabled`, `cacheable_prefix_min_tokens`, `semantic_cache_enabled` |
| Data policy | `restricted_data_allowed` plus the provider's `data_policy_json` |
| Cost profile | Derived, not stored — aggregate `cost_records` by route, or read `max_cost_usd` for the ceiling |
| Rollback route | Not a column. `fallback_route_id` is the *runtime failover* route, which is not the same concept as the route an operator rolls back to. Phase 01 supplies the raw material; naming and modelling this belongs to whoever builds the screen |
| Eval score | Phase 07 |

So six of eight are direct Phase 01 fields, one is a Phase 01 aggregate, and two need work elsewhere. The distinction between fallback and rollback is worth preserving rather than collapsing: conflating them would let an outage failover be mistaken for a deliberate version rollback in the audit trail.

The dashboard KPI row includes "AI runs today" and "cost today", and the empty state is "No AI runs yet". Both read Phase 01 tables.

Phase 01's frontend obligation is therefore narrow and concrete: make sure the API returns these fields with these names. Nothing needs to be rendered yet.

## 42. Common Mistakes

### Mistake 1: Calling The Provider SDK From A Route Handler

Why it happens: it is faster for the first feature.

Consequence: no run record, no cost tracking, no retry policy, no route control, and a second call site to migrate later.

Fix: the blueprint's rule, enforced by review — all model calls go through `model_gateway`.

### Mistake 2: Letting Callers Pass A Model Name

Why it happens: it feels flexible.

Consequence: routing becomes meaningless, cost control evaporates, and no one can answer which model serves which feature.

Fix: callers pass a use case. `model_override` exists but is permission-gated and audited.

### Mistake 3: Writing The AI Run Only On Success

Consequence: failures, timeouts, and blocks are invisible, so the reliability dashboard shows a perfect success rate.

Fix: create the run before the call, finalize in `finally`.

### Mistake 4: Treating `blocked` As `failed`

Consequence: policy refusals inflate the error rate, and governance cannot count refusals.

Fix: separate terminal statuses, as the schema already defines.

### Mistake 5: Retrying Everything

Consequence: authentication failures and oversized inputs are retried, tripling latency and cost to produce the same error.

Fix: the retry classification table, and the blueprint's explicit non-retry list.

### Mistake 6: Float Money

Consequence: cost totals drift from the invoice and nobody can explain why.

Fix: `Decimal` everywhere; round once at the end.

### Mistake 7: Skipping The Mock Provider

Why it happens: the real provider works, so a mock feels redundant.

Consequence: tests become slow, expensive, network-dependent, and impossible to run in CI. Failure paths go untested because you cannot make a real provider time out on demand.

Fix: build the mock first, as Step 4 does.

### Mistake 8: One Run Row Per Attempt

Consequence: costs and request counts triple-count during incidents.

Fix: one run, attempts recorded inside it.

### Mistake 9: Storing Provider Keys In The Database

Consequence: keys leak through admin endpoints, backups, and database dumps.

Fix: keys come from settings, keyed by provider name.

### Mistake 10: Building Phase 20 Features Now

Why it happens: prompt caching and semantic caching are interesting.

Consequence: Phase 01 never finishes, and optimization is built before there is a baseline to optimize against.

Fix: create the columns, defer the behavior. The optimization decision tree explicitly warns against jumping ahead: "Do not jump to fine-tuning or self-hosting before measuring the bottleneck."

## 43. Ticket Mapping

| Ticket | Task | Where In This Document | Acceptance Proof |
|---|---|---|---|
| P01-001 | Add `model_providers`, `model_routes`, `ai_runs` migration | Sections 17, 18; Steps 2–3 | Migration applies cleanly |
| P01-001 gap | `cost_records` is not named in the ticket | Section 18.4 | See the note below |
| P01-002 | Define provider adapter interface | Sections 14.4, 23; Step 4 | Mock provider implements the interface |
| P01-003 | Add one managed chat provider adapter | Sections 14.5, 23.3; Step 12 | Smoke test behind env flag |
| P01-004 | Add fake provider for tests | Sections 14.6, 23.4; Step 4 | No test requires a real model key |
| P01-005 | Route by use case | Sections 20, 21, 22; Step 6 | Route unit tests pass |
| P01-006 | Track input/output/cache/reasoning tokens and estimated cost | Sections 15.5, 26; Step 7 | `ai_run` stores usage fields |
| P01-007 | Add retry, timeout, and fallback policy | Section 26; Steps 9, 11 | Simulated timeout test passes |
| P01-008 | Add internal model test endpoint or service call | Section 31; Step 14 | Endpoint returns an `ai_run` id |
| P01-009 | Emit GenAI span fields | Section 32; Step 13 | Trace sample contains model and request attributes |
| P01-010 | Block provider calls when tenant policy disallows route | Sections 21, 22, 32, 33; Step 15 | Restricted route test passes |

Ticket gap worth raising with the documentation owner: P01-001 names only `model_providers`, `model_routes`, and `ai_runs`, but P01-006 requires estimated cost to be tracked, and the cost runbook requires cost to be broken down by billing unit. That breakdown needs `cost_records`, which no Phase 01 ticket creates. Either extend P01-001 to four tables or add a P01-011 cost schema ticket. This document treats `cost_records` as in scope regardless, because P01-006 is not satisfiable in a useful form without it.

The tickets document also lists the phase-level verification commands:

```text
alembic upgrade head
pytest tests/model_gateway tests/migrations
pytest tests/api/test_model_gateway.py
```

## 44. Quality Gates And Done Criteria

Phase 01 is done when every gate below passes. Not before.

### 44.1 Functional Gates

```text
[ ] The four Step 0 decisions are recorded in docs/decisions/
[ ] Identity tables exist, so ai_runs.tenant_id can be not null
[ ] Migrations apply and roll back cleanly on an empty database
[ ] Bootstrap loads providers and routes idempotently
[ ] Every fallback_route_key in the config resolves; bootstrap rejects a dangling key
[ ] A restricted-data request is served by the compliant private route (Section 38.4)
[ ] A chat request through the mock provider returns a response and an ai_run id
[ ] An embed request returns vectors in input order with the expected dimension
[ ] Route listing returns the UX-specified columns
[ ] AI run detail returns usage, cost, and latency
[ ] A simulated timeout retries and then succeeds
[ ] A simulated outage falls back to a route that re-passes every filter
[ ] A restricted-data request is blocked with the correct code
[ ] A budget-exhausted request is blocked with the correct code
[ ] A circuit breaker opens, cools down, probes, and closes
[ ] Every model request produces exactly one ai_run row, retries included
[ ] Usage is normalized across providers, with null for unknown
[ ] Deferred foreign keys are documented, including the cost_records ordering
    resolution and the prompt_versions soft reference
```

### 44.2 Code Quality Gates

```text
[ ] Linter passes
[ ] Formatter passes
[ ] Type checker passes
[ ] No provider SDK import outside packages/model_gateway/providers
[ ] No raw HTTP call to a model endpoint outside the adapters
[ ] No float used for money
[ ] No secret in code, database, logs, or errors
```

### 44.3 Test Gates

```text
[ ] Full suite runs with no provider key set
[ ] Unit, integration, contract, and migration tests pass
[ ] Redaction tests pass
[ ] Cross-tenant tests pass
[ ] Retry and circuit breaker tests are deterministic, not timing-flaky
```

### 44.4 Documentation Gates

```text
[ ] README covers gateway setup, bootstrap, and new environment variables
[ ] .env.example lists every new variable
[ ] Decision records exist for every policy choice this document flagged,
    including the four from Step 0 plus fallback depth, clamp-versus-reject
    for reasoning budgets, and whether routes are cached
[ ] Migration numbering is mapped to the canonical order
[ ] The baseline measurement report is committed
```

### 44.5 Readiness Gates For Phase 02

```text
[ ] ai_runs.prompt_version_id exists and is nullable
[ ] The gateway accepts and stores prompt_version_id when supplied
[ ] gen_ai.prompt.name and gen_ai.prompt.version are emitted, empty for now
[ ] No prompt text is hard-coded anywhere in the gateway
```

## 45. Portfolio Evidence

Phase 01 produces unusually good portfolio material because it is the phase where AI work starts to look like engineering.

```text
[ ] The routing configuration files, showing use-case-based model selection
[ ] A route decision log line including rejected routes and reasons
[ ] An ai_run record showing provider, model, route, tokens, cost, and latency
[ ] Cost records broken down by billing unit
[ ] A test run showing the whole suite passing with no provider key
[ ] A simulated timeout test showing retry and recovery
[ ] A fallback test showing a switch to a secondary provider
[ ] A restricted-data test showing a blocked run with no provider call
[ ] The baseline report: success rate, p50/p95 latency, cost per 1,000 calls
[ ] A structured log line proving no message content is logged
[ ] The migration test output proving upgrade and downgrade
```

Phase 00's evidence proved you can structure a backend. Phase 01's evidence proves you can operate a model.

## 46. Interview Perspective

### 46.1 How To Present This Phase

```text
I built a model gateway as the single controlled entry point for every LLM and
embedding call. Callers request a use case, not a model. A router selects a route
from the database by tenant, priority, provider capability, data policy, and cost
budget, and records why it rejected the alternatives. Every call produces one
ai_run row with normalized token usage, cost computed in Decimal from a versioned
pricing sheet, latency, and a trace id, plus per-billing-unit cost records.
Reliability is policy: per-attempt timeouts, classified retries with exponential
backoff and jitter, a circuit breaker per provider and model, and policy-revalidated
fallback. Everything is testable without a provider key because the mock provider
is a first-class component that can simulate timeouts, rate limits, outages, and
truncation. Content is redacted before storage, and restricted-data tenants store
metadata only.
```

### 46.2 Questions This Phase Prepares You For

```text
Why route by use case instead of model name?
How do you switch providers without changing application code?
How do you know what an AI feature costs?
What do you retry, and what do you never retry?
What is a circuit breaker and why does a gateway need one?
How do you test AI code without calling a real model?
How do you keep one tenant's data off a non-compliant provider?
How do you make sure a retry does not double-count a request?
Why store both an ai_run and separate cost records?
What breaks when a provider changes a model alias?
Why is a blocked request different from a failed one?
```

### 46.3 Strong Answers

Question:

```text
Why not let each service call the provider SDK directly?
```

Answer:

```text
Because then there is no single place that knows what the platform spent, which
model served a request, or how failures are handled. Centralizing gives one place
to enforce timeouts, retries, budgets, data policy, and audit — and one place to
change when a provider changes. It also makes the whole platform testable, because
one mock replaces every provider.
```

Question:

```text
A retry succeeded on the third attempt. How many rows are in ai_runs?
```

Answer:

```text
One. A logical request is one run. Attempts are recorded inside it, with the
run's provider, model, and route reflecting the attempt that actually served the
request, and latency covering the whole sequence. Otherwise every incident would
inflate request counts and cost reports.
```

Question:

```text
How do you stop sensitive tenant data reaching a public provider?
```

Answer:

```text
Data policy is enforced at route selection, before any bytes leave the process.
The request carries a restricted-data flag defaulted from tenant policy, and a
route only qualifies if both the route and the provider allow restricted data.
Fallback re-runs the same check, which is why the private route is configured with
no fallback at all — a silent downgrade to a public provider would be the exact
failure the control exists to prevent. Rejections are recorded as blocked runs so
there is evidence that the refusal happened.
```

Question:

```text
Why is cost stored in two places?
```

Answer:

```text
The run column answers what a call cost. The cost records answer what it was made
of — input, output, reasoning, cache-write, and cache-read tokens, each with its
own unit price and pricing version. When cost spikes, the second question is the
one that actually leads to a fix.
```

## 47. Glossary

### Model Gateway

The single controlled component through which all model provider communication passes.

### Provider

A service that runs models, represented by a row in `model_providers`.

### Provider Type

The wire protocol a provider speaks, which determines which adapter handles it.

### Adapter

Code that translates between Atlas's internal request format and one provider protocol.

### Use Case

The reason for a model call, used as the routing key.

### Route

A stored binding of a use case to a provider, model, and limits.

### Route Key

The stable configuration name of a route.

### Fallback Route

The route used when the primary route cannot serve a request, subject to policy re-validation.

### Capability Matrix

The stored list of features a provider supports.

### Data Policy

Stored rules about whether a provider may receive restricted data, may train on it, where it runs, and how long it retains it.

### Restricted Data

Content that may only be sent to routes and providers explicitly approved for it.

### AI Run

The durable record of one logical model request.

### Cost Record

A per-billing-unit line item attached to an AI run.

### Billing Unit

The unit a provider charges for: input token, output token, reasoning token, cache write token, cache read token, image, audio second, video second, or request.

### Pricing Sheet

A versioned mapping of model and billing unit to unit price.

### Token

The unit models read and write, and the unit providers bill.

### Reasoning Tokens

Extra tokens a model spends on internal reasoning, recorded as `reasoning_output_tokens`.

### Cache Creation Tokens

Input tokens written to a provider's prompt cache.

### Cache Read Tokens

Input tokens served from a provider's prompt cache.

### Finish Reason

The normalized reason generation stopped.

### Timeout

The maximum wait for one provider attempt.

### Retry

A repeated attempt after a classified retryable failure.

### Backoff

The increasing delay between retries.

### Jitter

Randomization applied to backoff so clients do not retry in lockstep.

### Circuit Breaker

A mechanism that stops calling a failing provider and probes for recovery.

### Request Hash

A stable hash of the normalized request, used for grouping without storing content.

### Redaction

Removing or masking sensitive content before storage or logging.

### Soft Reference

A nullable id column pointing at a table that does not exist yet, hardened into a foreign key by a later migration.

### Blocked Run

A run refused by policy before any provider call.

### Span Attribute

A named field attached to a trace span, following the GenAI semantic conventions.

## 48. Connection To Phase 02

Phase 02 is the Prompt System: versioned prompt templates with variables, test cases, and change history.

What Phase 01 hands to Phase 02:

```text
ai_runs.prompt_version_id           -> nullable column, ready to be populated
gen_ai.prompt.name / .version       -> span attributes already emitted, currently empty
A gateway that accepts messages     -> prompts render into those messages
Cost and latency baselines          -> so a prompt change's cost impact is measurable
A mock provider                     -> so prompt tests need no provider key
Route selection by use case         -> so a prompt can target the right model
```

What Phase 02 adds on top:

```text
prompt_templates and prompt_versions tables
A renderer with required-variable validation
Prompt lifecycle: draft, testing, approved, active, retired
Activation gated on approved status (ticket P02-006)
prompt_version_id stored on every ai_run (ticket P02-007)
The deferred foreign key from ai_runs to prompt_versions
```

The sequencing logic is worth internalizing: Phase 01 makes model calls controlled and measurable, so that when Phase 02 changes what is sent, the effect on cost, latency, and reliability is immediately visible. Building the prompt system first would mean changing prompts with no way to measure the consequence.

## 49. Final Mental Model

Phase 00 built the building. Phase 01 installs the meter, the circuit breaker, and the logbook before switching the power on.

The rule that makes this phase coherent is the platform's founding rule, applied to model access:

```text
The application owns the system. The LLM does not own the system.
```

In Phase 01 that means:

```text
The application chooses the provider.
The application chooses the model.
The application sets the timeout.
The application decides what may be retried.
The application enforces the budget.
The application enforces the data policy.
The application records what happened.
The provider generates text and returns usage numbers, inside those boundaries.
```

The end state to aim for:

```text
Strong backend foundation           (Phase 00)
-> controlled model gateway          (Phase 01)
-> reliable versioned prompts        (Phase 02)
-> validated structured outputs      (Phase 03)
-> ingested and searchable knowledge (Phases 04-05)
-> grounded RAG with citations       (Phase 06)
-> measurable evaluation             (Phase 07)
```

Every one of those later phases makes model calls. All of them go through what Phase 01 builds. That is why this phase is worth building carefully rather than quickly.
