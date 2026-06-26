# Model API Integration and Multi-Provider Reliability

## Lesson metadata

| Field | Value |
|---|---|
| Curriculum position | Core Lesson 09 |
| Primary roles | Applied AI Engineer, Generative AI Engineer, Forward-Deployed AI Engineer, AI Solutions Architect |
| Supporting roles | LLM Engineer, AI Evaluation Engineer, AI Platform Engineer, Site Reliability Engineer |
| Difficulty | Intermediate |
| Estimated study time | 9-13 hours |
| Estimated implementation time | 12-18 hours |
| Prerequisite lessons | Lessons 01-08 |
| Project increment | Multi-provider model gateway for the Northstar Support drafting pilot |
| Primary tools | Python, OpenAI Python SDK, Anthropic Python SDK, HTTPX, Pydantic, Redis, OpenTelemetry, pytest |
| Technical guidance verified | June 25, 2026 |
| Learning design | Eight-module cognitive path plus complete implementation and production reference |

## How to use this lesson

This lesson has two layers.

### Essential first pass

Complete the eight learning modules in order. Each module contains:

- One central engineering question
- A small concept set
- A worked example
- Guided practice
- Independent transfer
- A closed-book retrieval checkpoint
- A misconception check

Stop after each checkpoint and answer without looking back. Recommended sessions:

| Session | Modules | Approximate time | Output |
|---|---|---:|---|
| A | API boundary; contracts and adapters | 75-100 minutes | Provider-neutral request flow |
| B | Structured output; streaming | 75-105 minutes | Schema gate and stream event model |
| C | Errors and retries; circuits and fallback | 90-120 minutes | Retry matrix and routing policy |
| D | Tools and multimodal input; tracing and cost | 90-120 minutes | Tool boundary and usage ledger |

### Hands-on path

After the modules:

1. Add the gateway package to `ai-industry-labs`.
2. Implement one milestone at a time.
3. Run unit tests before enabling real credentials.
4. Exercise one provider in a development project.
5. Enable the second provider only after contract tests pass.
6. Run the failure-injection and fallback evaluation.

### Production and reference path

The reference layer includes:

- Provider API differences
- Complete data contracts
- OpenAI and Anthropic adapters
- Retry and circuit-breaker behavior
- Tool-call controls
- Usage and cost accounting
- Testing, deployment, observability, and incident response

The provider APIs and SDKs change. Recheck the official references and regenerate the lockfile
before using this lesson in a later environment.

### Retrieval rule

When recall is difficult, reconstruct the flow before rereading:

```text
business request
→ gateway contract
→ policy and routing
→ provider adapter
→ validated provider result
→ usage ledger and trace
→ business logic
```

## Why this lesson exists

Lesson 08 established how language models tokenize, generate, and fail. It also produced a
shortlist of hosted candidates for the Northstar Support pilot.

A direct provider call is sufficient for a disposable experiment:

```python
response = client.responses.create(model=model, input=prompt)
```

It is not a sufficient production boundary.

A production application must answer questions the model provider cannot answer for it:

- Which tenant and user initiated this request?
- Which provider and model are approved for this data?
- What timeout is appropriate for this user interaction?
- Which failures can be retried safely?
- Did the provider receive the request but lose the response?
- Can another provider receive semantically equivalent input?
- Was structured output validated before business code used it?
- Did a stream end normally, fail, or get cancelled?
- Which tool may be called, with which identity and permissions?
- How many tokens and dollars belong to this customer and feature?
- Which provider request ID helps diagnose an incident?
- What happens when a model or API is deprecated?

This lesson builds that boundary.

Use a gateway when several application capabilities need consistent:

- Authentication and secret handling
- Provider isolation
- Validation
- Reliability policy
- Routing
- Tracing
- Usage accounting
- Safety controls

Do not create a large centralized platform merely because one script calls one model. A gateway
is justified when shared policy and operational ownership outweigh the added network hop and
abstraction cost.

## Business problem

### Organization and workflow

Northstar Support is implementing the bounded pilot selected in Lesson 07:

> Permission-aware, evidence-backed response drafting for eligible support cases, with mandatory
> agent approval and no autonomous financial or account action.

Lesson 08 selected one hosted primary candidate and one fallback candidate. The support service
now needs to request:

- Ticket classification
- Structured issue extraction
- Priority recommendation
- Draft text streamed to the agent interface
- Read-only policy lookup through a controlled tool

Lesson 10 will design the prompts. This lesson builds the reliable provider boundary that those
prompts will use.

### Current baseline

The prototype has provider calls embedded directly in application handlers:

```text
HTTP handler
→ provider SDK
→ raw model text
→ application code parses or displays it
```

Observed risks:

- Provider-specific objects leak into business code.
- Default provider timeouts are much longer than the product latency budget.
- SDK retries and application retries can multiply each other.
- Raw JSON-like text is parsed inconsistently.
- Streaming failures produce partial drafts without a final status.
- Usage is visible in provider dashboards but not attributable to a tenant or feature.
- Fallback behavior is manual and untested.
- Conversation history may be trapped in provider-specific state.
- Tool arguments can reach execution code before validation.

### Target workflow

```text
Support API
→ authenticate user and resolve tenant
→ authorize requested capability
→ build provider-neutral ModelRequest
→ gateway applies data, budget, and routing policy
→ adapter calls approved provider
→ validate response or stream events
→ record trace, usage, cost, and outcome
→ return safe result to support workflow
→ agent reviews before any customer-facing action
```

### Inputs

- Tenant and user identifiers supplied by trusted application middleware
- Synthetic or approved ticket content
- Canonical conversation messages
- Requested operation
- Output schema when structured data is required
- Approved model tier
- Latency and output-token budgets
- Optional read-only tools
- Optional image or document references that passed upload validation

### Outputs

- Validated text or typed structured data
- Normalized tool-call proposals
- Normalized stream events
- Provider and model identity
- Provider request ID
- Token usage
- Estimated cost from a dated price catalog
- Trace and gateway request IDs
- Explicit final status or normalized failure

### Constraints

- Provider secrets never reach a browser or model prompt.
- Customer text is not logged by default.
- Tenant and user identity are supplied by trusted code, not by the model.
- Model output is untrusted.
- Invalid structured output cannot reach business logic.
- Automatic retry and fallback are allowed only for side-effect-free model generation.
- Write-capable tools are not automatically replayed.
- Every request has bounded time, output, retry, and spending budgets.
- The application owns canonical conversation state.
- The pilot remains human-reviewed.

### Acceptance metrics

| Area | Acceptance requirement |
|---|---|
| Contract | Provider-specific types do not cross the adapter boundary |
| Structured output | 100% of downstream records pass the declared Pydantic schema |
| Reliability | Retryable, terminal, and ambiguous failures are classified correctly in the fixed fault set |
| Retry safety | No unsafe or ambiguous write action is automatically replayed |
| Fallback | Every fallback records the failed provider, reason, selected provider, and added latency |
| Attribution | 100% of successful and failed calls include tenant, user, operation, provider, and model |
| Streaming | Every stream emits exactly one terminal `completed`, `failed`, or `cancelled` event |
| Cost | Token usage comes from provider response metadata; prices come from a dated external catalog |
| Security | Keys remain server-side; tool names and arguments are allowlisted and validated |
| Operations | Provider request IDs and gateway trace IDs are available for incident diagnosis |

## Learning outcomes

After completing this lesson, you will be able to:

- Design a provider-neutral model request and response contract.
- Isolate provider SDK behavior behind adapters.
- Configure server-side authentication, explicit timeouts, and bounded output.
- Normalize text, structured output, streams, tool calls, usage, and provider request IDs.
- Validate schema-constrained output before business use.
- Distinguish transport, timeout, rate-limit, authentication, validation, safety, and provider
  failures.
- Decide which failures are terminal, retryable, or ambiguous.
- Prevent hidden retry multiplication across SDK and gateway layers.
- Implement exponential backoff with jitter and provider-directed delay.
- Implement a Redis-backed circuit breaker.
- Route to a fallback provider without hiding degraded behavior.
- Keep canonical conversation state provider-independent.
- Validate tool arguments and enforce permissions outside the model.
- Handle image, document, and audio capability differences explicitly.
- Attribute token usage and estimated cost by tenant, user, feature, provider, and model.
- Add OpenTelemetry spans without leaking prompts or secrets.
- Test normal, boundary, failure, adversarial, and cancellation paths.
- Deploy and operate the gateway with canary release, rollback, alerts, and incident procedures.

## Prerequisites

### Knowledge

- Production Python, typing, and async programming
- HTTP clients and APIs
- Pydantic validation
- Unit and integration testing
- SQL and durable records
- Authentication and authorization boundaries
- Token accounting and model behavior from Lesson 08

### Existing project

Continue using `ai-industry-labs`. Earlier lessons should already provide:

- A source package and test layout
- Locked dependencies
- Application configuration
- FastAPI or another server boundary
- Structured logging
- SQL persistence
- Docker and CI
- The Lesson 08 model catalog and hosted candidate

### Accounts and services

For the complete integration:

- One approved OpenAI API project
- One approved Anthropic workspace
- Redis for shared circuit state
- An OpenTelemetry collector or console exporter
- A development database for usage records

Provider credentials are optional for unit tests. Mocked adapters are the default learning path.

### Fallback when paid services are unavailable

Implement the gateway and run all contract, retry, circuit, fallback, and accounting tests with
fake adapters. A local OpenAI-compatible server may be added as an extension, but do not claim it
proves compatibility with a hosted provider.

### Data

Use the synthetic support cases from Lesson 08. Do not send real customer data until:

- The provider and region are approved.
- Contractual data handling is reviewed.
- Retention and deletion behavior are documented.
- Logging and tracing redaction are verified.
- The use case passes security and privacy review.

## Activate prior knowledge

Answer without looking back:

1. Why is deterministic decoding not equivalent to a correct response?
2. Which parts of the context budget must be counted before a model request?
3. Why must model output be treated as untrusted input?
4. What is the difference between a timeout and proof that no provider-side work occurred?
5. Which identity made the support agent eligible for the pilot: the model, the gateway, or the
   application?

Do not continue until you can explain questions 1, 3, and 5.

## Lesson concept map

```text
Lessons 01-06
Python + async + tests + APIs + SQL
                 │
Lesson 07        │       Lesson 08
bounded use case │       model behavior and candidate selection
        └────────┴──────────────┐
                               ▼
                    provider-neutral contract
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       provider adapters   reliability      control plane
       text/JSON/stream    timeout/retry    identity/budget
       tools/multimodal    circuit/fallback tracing/cost
              └────────────────┼────────────────┘
                               ▼
                validated model capability
                               │
                               ▼
               Lesson 10: versioned prompts
```

## Learning module map

| Module | Central question | Time | New concepts | Practice artifact |
|---|---|---:|---|---|
| API boundary | What belongs between business code and a provider SDK? | 35 min | gateway, policy boundary, trust boundary, canonical state | Responsibility map |
| Contracts and adapters | How can two providers implement one application capability? | 45 min | port, adapter, capability matrix, normalization | Provider-neutral contract |
| Structured output | How does typed data become safe for business logic? | 45 min | schema constraint, parse, validation gate, refusal | Schema gate |
| Streaming | How do partial events remain observable and correct? | 40 min | SSE, delta, accumulator, terminal event, cancellation | Unified stream |
| Errors and retries | Which failures may be tried again? | 50 min | error taxonomy, retry safety, ambiguity, backoff, jitter | Retry matrix |
| Circuits and fallback | When should traffic stop going to a failing provider? | 45 min | circuit breaker, degraded mode, fallback, semantic parity | Routing policy |
| Tools and multimodal input | How are model-proposed actions and non-text inputs controlled? | 50 min | tool proposal, argument validation, approval, media capability | Tool boundary |
| Tracing, usage, and cost | How is every call attributable without leaking data? | 45 min | correlation, span, usage ledger, price catalog, unit cost | Trace and usage record |

## Essential learning modules

## Learning module: The model API boundary

### Module question

If an HTTP handler can call a provider SDK directly, why add another layer?

### Essential concepts

- A **gateway** is a service or library boundary that applies shared policy before and after model
  calls.
- A **trust boundary** is a point where data crosses between components with different authority
  or reliability assumptions.
- A **policy boundary** is the component responsible for enforcing rules such as allowed
  providers, data classes, budgets, and retries.
- **Canonical state** is the application-owned representation that remains valid when providers
  change.
- A **provider request ID** is the provider's identifier for one API request; it is not the same
  as the application's request or trace ID.

### Mental model

The provider generates. The gateway governs the call. The application owns the workflow.

```text
Application authority     Gateway policy          Provider capability
---------------------     --------------          -------------------
user and tenant           routing                 generation
permissions               timeout and retry       provider tools
business state            validation              token usage
human approval            tracing and cost        provider request ID
```

### Worked example

A support agent requests a draft. The incoming JSON claims `tenant_id="enterprise-a"`.

Incorrect flow:

```text
request JSON tenant_id
→ send directly to provider
→ trust returned draft
```

Correct flow:

1. Authentication middleware resolves the agent identity.
2. Authorization resolves the tenant and draft permission.
3. The handler ignores tenant identity supplied by untrusted request content.
4. The gateway receives trusted identity attributes from server context.
5. The gateway selects only providers approved for that tenant's data class.
6. The result remains a draft requiring agent approval.

The model never decides tenant membership or approval authority.

### Guided practice

Assign each responsibility to application, gateway, or provider:

- Verify the support agent may access ticket `T-104`.
- Select a model approved for confidential support text.
- Generate a draft.
- Validate extracted issue fields.
- Approve a refund.
- Report provider input and output tokens.

Hint: only one item belongs solely to the provider.

### Independent practice

Draw the boundary for an internal legal summarization tool. Mark where document permission,
provider selection, generation, citation validation, and final legal review occur.

### Retrieval checkpoint

Close the lesson and answer:

1. What three responsibilities remain outside the model?
2. Why should canonical conversation state remain application-owned?
3. How does a provider request ID differ from a trace ID?
4. What justifies a gateway instead of a direct SDK call?

### Misconception check

**Misconception:** A provider abstraction makes providers interchangeable.

Why it seems plausible: both accept text and return text.

Correct model: an adapter normalizes a selected common capability. Models still differ in
quality, role semantics, tool behavior, structured-output support, context limits, safety
behavior, latency, and data policy.

Test case: send the same tool schema and ambiguous support ticket through both adapters. Compare
normalized shape and semantic behavior separately.

### Connection

This module used Lesson 07's authority boundaries. The next module turns the boundary into typed
contracts.

## Learning module: Provider-neutral contracts and adapters

### Module question

Which information should be common across providers, and which information must stay inside an
adapter?

### Essential concepts

- A **port** is an interface defined by the application.
- An **adapter** translates a provider-specific API into that interface.
- **Normalization** maps provider-specific objects into a stable application model.
- A **capability matrix** records which providers support required text, structured, streaming,
  tool, and media features.
- **Semantic parity** means the fallback can satisfy the same business contract, not merely accept
  similar parameters.

### Mental model

Normalize the business capability, not every provider feature.

```text
ModelRequest ──> ModelProvider port ──> OpenAI adapter
                              └───────> Anthropic adapter

Provider response ──> normalized result ──> schema and policy gate
```

### Worked example

The application needs structured issue extraction:

```text
category: billing | account | technical | security
requires_approval: boolean
summary: short string
```

Common contract:

- Messages
- Output schema
- Maximum output
- Tenant, user, and operation metadata
- Usage and request identity in the result

Adapter-owned details:

- OpenAI Responses API request shape
- Anthropic Messages API system-message handling
- Provider event classes
- Provider exception classes
- Provider usage object fields

The application receives the same `ModelResult[IssueExtraction]` from either adapter.

### Guided practice

For each field, decide common contract or adapter detail:

- `tenant_id`
- `previous_response_id`
- `max_output_tokens`
- `request-id` header
- `messages`
- Anthropic content blocks
- `operation`
- OpenAI output items

Hint: provider-specific continuation IDs may be recorded, but must not become canonical state.

### Independent practice

Design a capability matrix for:

- Text generation
- Typed structured output
- Streaming text
- Client-side tools
- Image input
- PDF input
- Audio input

Use `supported`, `unsupported`, or `provider-specific`. Do not infer support from marketing names.

### Retrieval checkpoint

1. Define port and adapter.
2. What does normalization protect?
3. Why is a lowest-common-denominator API dangerous?
4. What is semantic parity?
5. Name two details that must stay inside an adapter.

### Misconception check

**Misconception:** A provider-independent interface should expose every feature from every
provider.

Correct model: expose stable business capabilities. Add explicit provider extensions only when
the business case accepts reduced portability.

Test case: an audio-specific parameter appears in the common text request. The contract is now
coupled to a feature other providers may not support.

### Connection

The adapter contract is useful only if its outputs are safe. The next module builds the schema
gate.

## Cumulative retrieval: Boundary and contract

Without looking back:

1. Draw application, gateway, adapter, and provider.
2. Place identity, authorization, generation, validation, and approval.
3. Explain why provider neutrality does not imply model equivalence.
4. Give one field that belongs in the common request and one that does not.
5. Predict what breaks if business code imports provider response classes.

## Learning module: Structured output as a validation gate

### Module question

If a provider offers schema-constrained output, why validate again in the application?

### Essential concepts

- **Structured output** asks a model to produce data conforming to a declared schema.
- **Constrained generation** restricts allowable output tokens according to a grammar or schema.
- A **validation gate** prevents unvalidated output from crossing into business logic.
- A **refusal** is a provider or model decision not to produce the requested content.
- **Repair** is a second attempt to transform invalid output; it is a new model call, not proof
  the original output was safe.

### Mental model

```text
schema sent to provider
→ provider generation
→ SDK parse
→ application Pydantic validation
→ domain validation
→ business use
```

Provider schema support improves reliability. The application still owns correctness.

### Worked example

Schema:

```python
class IssueExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: Literal["billing", "account", "technical", "security"]
    requires_approval: bool
    summary: str = Field(min_length=1, max_length=240)
```

Provider output:

```json
{
  "category": "billing",
  "requires_approval": false,
  "summary": "Customer reports a duplicate charge."
}
```

Pydantic accepts the shape, but domain policy adds:

```text
duplicate charge + possible refund
→ requires_approval must be true
```

Schema validation checks shape. Domain validation checks business meaning.

### Guided practice

Add these constraints:

- Reject unknown fields.
- Limit summary length.
- Allow only four categories.
- Require approval when the requested action is financial.

Hint: the first three are schema constraints; the last is a domain invariant.

### Independent practice

Create a schema for security-ticket triage with:

- Severity
- Indicators
- Account-compromise suspicion
- Escalation requirement

Add one invariant that cannot safely be delegated to the model.

### Retrieval checkpoint

1. Why validate after constrained generation?
2. What is the difference between schema and domain validation?
3. When should invalid output be rejected instead of repaired?
4. Why must refusal be represented separately from parse failure?

### Misconception check

**Misconception:** Valid JSON is valid business data.

Correct model: JSON parsing proves syntax. Schema validation proves declared shape. Domain
validation enforces business invariants. Authorization determines allowed action.

Test case: a valid record says `requires_approval=false` for a $500 refund request.

### Connection

Structured output is consumed after completion. Streaming introduces partial, non-final data.

## Learning module: Streaming without losing correctness

### Module question

How can a UI display partial text without treating partial text as a completed result?

### Essential concepts

- **Server-Sent Events (SSE)** is an HTTP streaming format where a server sends a sequence of
  events.
- A **delta** is an incremental piece of output.
- An **accumulator** reconstructs the complete output from ordered deltas.
- A **terminal event** explicitly marks completion, failure, or cancellation.
- **Backpressure** occurs when a consumer processes events more slowly than they arrive.
- **Cancellation** is the deliberate termination of work after a user disconnect or deadline.

### Mental model

```text
started
→ zero or more text deltas
→ optional usage or metadata
→ exactly one terminal event
```

Partial text is presentation state, not committed business state.

### Worked example

The draft stream emits:

```text
started
text_delta("I understand")
text_delta(" you were charged twice.")
failed(provider_timeout)
```

The UI may show the partial text as interrupted. It must not:

- Mark the draft complete
- Persist it as approved
- Send it to the customer
- Assume usage is zero
- silently retry and splice a second provider's text into the first stream

A fallback stream begins as a new attempt with a new attempt ID.

### Guided practice

Define four normalized stream events:

- `started`
- `text_delta`
- `completed`
- `failed`

Add fields needed to distinguish gateway request, attempt, provider, model, and sequence.

### Independent practice

Design cancellation behavior when an agent closes the browser after 200 tokens. Specify:

- Which coroutine is cancelled
- What final status is stored
- Whether provider billing may still occur
- Which metrics increment

### Retrieval checkpoint

1. Why is a delta not a result?
2. What invariant applies to terminal events?
3. Why should fallback not splice into an existing stream?
4. What is backpressure?
5. What evidence should a cancelled request retain?

### Misconception check

**Misconception:** Streaming only changes the user interface.

Correct model: streaming changes connection lifetime, timeout behavior, cancellation, partial
state, event ordering, usage collection, and failure handling.

Test case: disconnect the client after the first delta and inspect stored status and open
provider connections.

### Connection

Streams expose failures over time. The next module classifies those failures and decides whether
another attempt is safe.

## Cumulative retrieval: Validated output and streams

1. Reconstruct the structured-output gate.
2. Explain why a domain invariant is not a prompt instruction.
3. Draw the legal stream-event sequence.
4. Diagnose a stream that has two `completed` events.
5. Explain what the UI may do with partial text and what business logic may not do.

## Learning module: Error taxonomy and bounded retries

### Module question

Which failures should be retried, and what can a timeout not prove?

### Essential concepts

- A **terminal failure** should not be retried without changing the request or configuration.
- A **retryable failure** may succeed when attempted again after a bounded delay.
- An **ambiguous completion** means the caller does not know whether remote work completed.
- **Exponential backoff** increases delay after successive failures.
- **Jitter** adds randomness so clients do not retry simultaneously.
- A **retry budget** caps attempts, elapsed time, and added cost.

### Mental model

Retry only when all three are true:

```text
failure is transient
AND operation is safe to repeat
AND retry budget remains
```

### Worked example

| Failure | Retry? | Reason |
|---|---|---|
| Invalid API key | No | Configuration or secret error |
| Invalid schema request | No | Same request will fail again |
| Rate limit with delay | Yes, bounded | Capacity may recover |
| Provider 503 | Yes, bounded | Usually transient |
| Connection failed before send | Yes, bounded | No response received |
| Read timeout during pure generation | Maybe | Duplicate provider work and cost are possible, but no business write occurs |
| Timeout after `send_refund` tool | No automatic replay | Remote side effect may have completed |
| Model refusal | No transport retry | This is a behavior outcome, not network failure |

For Northstar's draft generation, a duplicated provider request costs money but does not send a
customer response. The gateway may retry within budget and record every attempt.

### Guided practice

Classify:

- 401 authentication
- 429 rate limit
- 400 invalid request
- 529 overloaded provider
- socket connect timeout
- read timeout after a write-capable tool call
- schema validation failure

Use `terminal`, `retryable`, or `policy decision`.

### Independent practice

Create a retry policy for a batch classification job where latency is less important than cost.
Compare it with the interactive drafting policy.

### Retrieval checkpoint

1. State the three retry conditions.
2. Why is timeout not proof that no remote work occurred?
3. What problem does jitter prevent?
4. Why disable SDK retries when the gateway owns retries?
5. What three dimensions bound a retry budget?

### Misconception check

**Misconception:** `POST` requests must never be retried.

Correct model: HTTP method alone is insufficient. A side-effect-free generation request may be
repeated under policy, while a tool-driven financial write may be unsafe even if wrapped in a
different method.

Test case: compare a duplicate draft generation with a duplicate refund command.

### Connection

Retries help isolated transient failures. A circuit breaker handles sustained provider failure.

## Learning module: Circuit breakers and observable fallback

### Module question

When should the gateway stop sending requests to a provider before every caller waits for a
timeout?

### Essential concepts

- A **circuit breaker** temporarily blocks calls after repeated qualifying failures.
- **Closed** means calls are allowed.
- **Open** means calls fail fast or route elsewhere.
- **Half-open** means limited probes test recovery.
- **Fallback** selects an alternate provider or model.
- **Degraded mode** is a deliberate reduced-capability operating state.

### Mental model

```text
closed --failure threshold--> open
open --cooldown--> half-open
half-open --success--> closed
half-open --failure--> open
```

### Worked example

The primary provider returns five overload failures in 30 seconds.

Without a circuit:

- Every interactive request waits through timeout and retry.
- The gateway increases load on the failing provider.
- User latency and cost rise.

With a circuit:

1. Qualifying failures increment shared state.
2. The circuit opens for a short cooldown.
3. New eligible draft requests route to the approved fallback.
4. Fallback is recorded as degraded operation.
5. A bounded probe later tests the primary.
6. Success closes the circuit; failure reopens it.

Authentication and invalid-request errors do not prove provider unavailability and should not
open the provider-wide circuit.

### Guided practice

Choose whether each error contributes to a provider circuit:

- Rate limit
- 503 or 529 overload
- Invalid API key
- Invalid request schema
- Connection failure
- Model refusal

Hint: separate provider health from your configuration and content policy.

### Independent practice

Design fallback for a tenant whose data may use provider A but not provider B. Include the
behavior when A is unavailable.

### Retrieval checkpoint

1. Name the three circuit states.
2. Which failures should not open a provider-wide circuit?
3. What is degraded mode?
4. Why must fallback be observable?
5. What does semantic parity require?

### Misconception check

**Misconception:** Fallback guarantees availability.

Correct model: fallback helps only when the alternate provider is approved, healthy, capable,
within budget, and semantically acceptable. Correlated cloud, network, prompt, or data failures
can affect both providers.

Test case: both providers reject the same invalid schema. Fallback adds latency but cannot solve
the defect.

### Connection

Fallback handles generation providers. The next module addresses tool actions and media inputs,
where provider capability and authority differ more sharply.

## Cumulative retrieval: Reliability policy

1. Build a retry table from memory.
2. Explain ambiguous completion using a tool write.
3. Draw circuit states and transitions.
4. Give one case where fallback is prohibited by data policy.
5. Predict the result of SDK retries set to two plus gateway attempts set to three.

## Learning module: Tool calls and multimodal inputs

### Module question

What does a model tool call authorize?

### Essential concepts

- A **tool call** is a model-generated proposal containing a tool name and arguments.
- A **tool registry** is an application-owned allowlist of callable tools and schemas.
- **Least privilege** grants only the permissions required for the current task.
- **Idempotency** ensures repeated requests produce one intended side effect.
- **Multimodal input** contains more than text, such as images, audio, or documents.
- A **capability check** rejects a request when the selected provider cannot satisfy the required
  modality or control.

### Mental model

```text
model proposes
→ gateway validates name and arguments
→ application authorizes user and resource
→ approval policy runs
→ tool executes with bounded credentials
→ result is returned to model or workflow
```

The model has no authority merely because it emitted a valid tool call.

### Worked example

Allowed tool:

```text
lookup_policy(policy_id)
```

The model proposes:

```json
{"policy_id": "refund-duplicate-charge"}
```

The gateway:

1. Confirms `lookup_policy` is enabled for the operation.
2. Validates arguments.
3. Uses the authenticated tenant context.
4. Enforces document permission before retrieval.
5. Limits result size.
6. Records tool name, duration, and outcome.
7. Returns content as untrusted evidence.

The model is not allowed to choose a different tenant or bypass policy filters.

### Guided practice

For a `create_refund` tool, add:

- Required arguments
- User permission
- Maximum amount
- Idempotency key
- Human approval
- Audit event
- Retry rule

### Independent practice

Design input controls for a customer-uploaded PDF:

- File size
- Media type
- Malware scanning
- Tenant ownership
- Retention
- Provider capability
- Prompt-injection treatment

### Retrieval checkpoint

1. What does a tool call authorize?
2. Where are tool names and arguments validated?
3. Why must tenant permission be checked before tool execution?
4. What makes a write tool safely retryable?
5. Why is a PDF still untrusted after malware scanning?

### Misconception check

**Misconception:** Strict tool schemas make tool execution safe.

Correct model: schemas constrain shape. Authorization, business limits, approval, idempotency,
network egress, and auditability control effects.

Test case: a perfectly valid `create_refund` call requests another tenant's order.

### Connection

Tool and media controls create events that must be attributable. The final module connects
requests, attempts, usage, and cost.

## Learning module: Tracing, token usage, and cost attribution

### Module question

How can the team diagnose and charge back a model request without storing sensitive prompts in
telemetry?

### Essential concepts

- A **correlation ID** links records belonging to one application operation.
- A **trace** represents a distributed request as related spans.
- A **span** represents one timed operation within a trace.
- A **usage ledger** is a durable record of measured provider usage and attribution.
- A **price catalog** is dated configuration used to estimate cost from usage.
- **Cost per successful task** divides total cost by accepted business outcomes, not raw calls.

### Mental model

```text
gateway request
  ├─ attempt 1: primary provider
  ├─ retry wait
  ├─ attempt 2: fallback provider
  ├─ optional tool spans
  └─ usage records for every billable attempt
```

### Worked example

One user request causes:

- Primary attempt: timeout after provider work may have started
- Fallback attempt: successful
- One policy lookup tool

Required records:

| Record | Outcome |
|---|---|
| Gateway operation | Completed in degraded mode |
| Primary attempt | Timeout, ambiguous provider completion |
| Fallback attempt | Success |
| Tool call | Success |
| Usage ledger | One record for each provider usage object received |
| Cost estimate | Based on model-specific, effective-dated catalog |

Do not log the ticket text. Record:

- Hash or case identifier where approved
- Tenant and user internal IDs
- Operation
- Provider and model
- Attempt count
- Token counts
- Latency
- Error category
- Provider request ID
- Prompt and schema versions later added in Lesson 10

### Guided practice

Choose which values belong in standard telemetry:

- API key
- Raw ticket body
- Tenant ID
- Provider request ID
- Input tokens
- Model name
- Full generated draft
- Error category

Hint: content requires a separate, explicit retention and access policy.

### Independent practice

Define a daily report for:

- Cost per tenant
- Cost per successful draft
- Fallback rate
- Schema failure rate
- P95 latency
- Provider error rate

Specify numerator and denominator for each metric.

### Retrieval checkpoint

1. Distinguish gateway request ID, trace ID, attempt ID, and provider request ID.
2. Why is provider-reported usage preferable to a character estimate?
3. Why should prices not be hard-coded in application logic?
4. What should a fallback trace show?
5. Why is cost per request weaker than cost per successful task?

### Misconception check

**Misconception:** Observability requires logging prompts and responses.

Correct model: operational diagnosis begins with identity-safe metadata, request IDs, versions,
usage, timings, errors, and sampled redacted content under separate access controls.

Test case: diagnose a rate-limit spike using provider, model, tenant, token, status, and request-ID
metadata without opening customer text.

### Connection

This module completes the gateway control loop. Lesson 10 will add prompt and schema versions to
the same request, trace, evaluation, and cost records.

## Final cumulative retrieval before the reference layer

Close the lesson and reconstruct:

1. The complete request flow from authenticated user to validated result.
2. The boundary between application authority, gateway policy, and provider capability.
3. The structured-output validation layers.
4. The legal streaming event sequence.
5. The three retry conditions.
6. Circuit states and fallback prerequisites.
7. The tool-call authorization flow.
8. The relationship among trace, attempt, usage, and cost.

If more than two parts are missing, repeat the relevant checkpoint before implementing.

## Reference and production depth

The remainder is the implementation and operational reference.

## Reference glossary

| Term | Definition |
|---|---|
| Adapter | Provider-specific translation behind an application-defined interface |
| Ambiguous completion | State where the caller cannot prove whether remote work completed |
| Backoff | Delay before another attempt |
| Backpressure | Slow-consumer pressure on a producer or stream |
| Canonical state | Application-owned state independent of a provider |
| Capability matrix | Explicit record of supported provider capabilities |
| Circuit breaker | State machine that blocks calls during sustained failure |
| Constrained generation | Output generation restricted by a grammar or schema |
| Correlation ID | Identifier connecting records for one operation |
| Delta | Incremental streamed output |
| Fallback | Approved alternate provider or model |
| Gateway | Shared boundary for model call policy and normalization |
| Idempotency | Property that repeated execution has one intended effect |
| Jitter | Random variation added to retry delay |
| Port | Application-defined interface implemented by adapters |
| Provider request ID | Provider-generated identifier for one API request |
| Retry budget | Bound on attempts, elapsed time, or added cost |
| Semantic parity | Ability of an alternate route to satisfy the same business contract |
| Span | Timed operation within a distributed trace |
| Structured output | Model output constrained to a declared data structure |
| Terminal event | Final stream event indicating completed, failed, or cancelled |
| Tool call | Model-generated proposal to invoke a named capability with arguments |
| Usage ledger | Durable attribution record for measured model use |
| Validation gate | Boundary that rejects unvalidated output before business use |

## Cumulative mental model

```text
TRUSTED APPLICATION CONTEXT
user ─ tenant ─ permissions ─ business operation
                    │
                    ▼
GATEWAY CONTROL PLANE
validate request
→ apply data and budget policy
→ select approved route
→ check circuit
→ create trace and attempt
                    │
                    ▼
PROVIDER ADAPTER
translate request
→ call with explicit timeout
→ normalize result, usage, request ID, or error
                    │
                    ▼
RESULT CONTROL
schema + domain validation
→ tool authorization if proposed
→ usage and cost record
→ completed, failed, or degraded outcome
                    │
                    ▼
BUSINESS WORKFLOW
agent review remains mandatory
```

## Architecture and data flow

```text
┌───────────────────────────────────────────────────────────────┐
│ Support application trust boundary                            │
│ authn → tenant resolution → authz → request construction      │
└───────────────────────────────┬───────────────────────────────┘
                                │ trusted identity context
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ Model gateway                                                  │
│ request validation                                             │
│ data/model/budget policy                                       │
│ routing → retry → circuit → fallback                           │
│ tool registry and approval boundary                            │
│ tracing → usage → cost                                         │
└──────────────┬──────────────────────────────┬─────────────────┘
               │                              │
               ▼                              ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│ OpenAI adapter           │      │ Anthropic adapter        │
│ Responses API            │      │ Messages API             │
│ SDK types and errors     │      │ SDK types and errors     │
└──────────────┬───────────┘      └─────────────┬────────────┘
               │ external provider trust boundary│
               └──────────────────┬───────────────┘
                                  ▼
                        Hosted model providers

Shared state:
- SQL: canonical conversations, usage ledger, route decisions
- Redis: circuit and short-lived coordination state
- Telemetry backend: traces, metrics, redacted logs
- Secret manager: provider credentials
```

### Request flow

1. The application authenticates the user.
2. Authorization resolves tenant, ticket, and operation permission.
3. The handler creates a provider-neutral request.
4. The gateway validates limits and data policy.
5. The router selects an approved provider/model route.
6. The circuit breaker allows, blocks, or probes the route.
7. The adapter translates canonical messages into the provider API.
8. The provider returns output, usage, and a provider request ID or an error.
9. The adapter normalizes the result.
10. The gateway validates schema and domain invariants.
11. Tool proposals pass through registry, authorization, and approval.
12. Usage, estimated cost, trace, and outcome are persisted.
13. The application receives a typed result or normalized failure.

### Trust boundaries

| Boundary | Untrusted input | Enforcement |
|---|---|---|
| Client to application | Claimed identity, tenant, ticket, media | Authentication, authorization, upload validation |
| Application to gateway | Messages, limits, operation | Pydantic contract, policy engine |
| Gateway to provider | Sensitive content, schemas, tools | Provider allowlist, data policy, secret manager |
| Provider to gateway | Text, JSON, tool arguments, usage metadata | Adapter normalization, schema validation |
| Gateway to tools | Tool name and arguments | Registry, authz, approval, idempotency |
| Telemetry boundary | Metadata and optional content | Redaction, sampling, access control, retention |

### State ownership

| State | Owner |
|---|---|
| User session and tenant membership | Application identity system |
| Ticket and approval status | Support application database |
| Canonical conversation messages | Application database |
| Provider continuation ID | Optional gateway metadata |
| Circuit state | Redis |
| Retry attempt state | Gateway request context and trace |
| Usage and cost records | Durable usage ledger |
| Provider secrets | Secret manager |

### Failure boundaries

- Application auth failure: provider is never called.
- Contract failure: request is rejected before routing.
- Provider failure: normalized by adapter.
- Schema failure: raw output is quarantined or redacted; business code receives no typed result.
- Tool failure: tool result is explicit; no hidden replay of consequential writes.
- Telemetry failure: request policy decides whether to continue; usage must be recoverable.
- Database failure: avoid returning a completed consequential workflow without required audit
  persistence.

## Design decisions

### Selected approach

- Async Python gateway library inside the existing service first
- OpenAI Responses API adapter
- Anthropic Messages API adapter
- Pydantic models as the common contract
- Gateway-owned retry policy with provider SDK retries disabled
- Redis-backed shared circuit breaker
- Application-owned conversation history
- SQL usage ledger
- OpenTelemetry spans and structured logs
- Configuration-owned model IDs and prices

### Deterministic baseline

The baseline is a fake provider implementing the same port:

- Returns fixed outputs
- Emits deterministic stream events
- Injects selected failures
- Reports fixed usage

This proves gateway behavior without depending on model quality or network availability.

### Alternatives

| Approach | Strength | Limitation | Use when |
|---|---|---|---|
| Direct SDK calls | Lowest initial complexity | Duplicated policy and provider leakage | One bounded experiment |
| In-process gateway library | No extra network hop | Shared release cycle with application | One product and one owning team |
| Dedicated gateway service | Central policy and independent scaling | Added hop and operational ownership | Several products share controls |
| Third-party gateway | Fast provider coverage | External dependency and policy fit | Vendor passes security and reliability review |
| OpenAI-compatible common protocol | Broad ecosystem support | Compatibility may be partial or semantic only | Tested subset is sufficient |
| Agent framework abstraction | Integrated tools and orchestration | More behavior than required here | Agent workflow is already justified |

### Rejected decisions

- Do not expose raw provider clients to handlers.
- Do not hard-code one "latest" model alias as permanent policy.
- Do not retry at both SDK and gateway layers.
- Do not parse arbitrary JSON with `json.loads` and trust it.
- Do not use provider conversation state as the only source of history.
- Do not route solely by lowest token price.
- Do not automatically replay write-capable tools after ambiguous failure.
- Do not hide fallback from traces or business metrics.

## Tooling

| Tool | Purpose | Why selected | Limitation | Alternative |
|---|---|---|---|---|
| OpenAI Python SDK | OpenAI Responses API | Typed async client, streaming, structured output, request IDs | Provider-specific | Direct HTTPX for unsupported SDK needs |
| Anthropic Python SDK | Anthropic Messages API | Typed async client, streaming, token counting, structured output | Provider-specific | Direct HTTPX |
| HTTPX | Explicit timeout model and SDK transport | Connect/read/write/pool controls | Does not define business retry safety | aiohttp |
| Pydantic | Contracts and validation | Typed schemas and JSON Schema generation | Shape validation is not authorization | Dataclasses plus JSON Schema library |
| Redis | Shared circuit state | Low-latency atomic state across instances | Requires availability and expiry design | Managed key-value store |
| OpenTelemetry | Traces and attributes | Vendor-neutral telemetry model | Requires collector and backend | Cloud-native tracing SDK |
| pytest | Unit and integration tests | Existing project standard | Real provider tests still cost money | unittest |

## Provider capability matrix

Verify this matrix against approved models, regions, and current provider documentation before
deployment.

| Capability | OpenAI adapter | Anthropic adapter | Gateway behavior |
|---|---|---|---|
| Text | Responses API | Messages API | Normalize text |
| Typed structured output | `responses.parse` with Pydantic | `messages.parse` with Pydantic | Revalidate and apply domain rules |
| Streaming | Typed response events | Message stream and text stream | Normalize event sequence |
| Client tools | Function calling | Tool use | Normalize proposals; execute outside model |
| Image input | Provider content part | Provider image content | Validate and map |
| Document input | File or input-file capability | File/PDF capability | Validate capability and retention |
| Audio input | Model/API dependent | Not assumed in common contract | Reject or use explicit extension |
| Conversation continuation | Provider response/conversation state available | Canonical messages commonly resent | Application history remains canonical |
| Token usage | Response usage metadata | Message usage metadata | Normalize usage |
| Provider request ID | `x-request-id` exposed as `_request_id` | `request-id` exposed as `_request_id` | Persist on attempt |

## Project structure

Add:

```text
ai-industry-labs/
├── model-gateway/
│   ├── price-catalog.yaml
│   ├── provider-routes.yaml
│   └── evaluation-cases.yaml
├── src/
│   └── ai_industry_labs/
│       └── model_gateway/
│           ├── __init__.py
│           ├── adapters/
│           │   ├── __init__.py
│           │   ├── anthropic_adapter.py
│           │   └── openai_adapter.py
│           ├── circuit.py
│           ├── config.py
│           ├── errors.py
│           ├── gateway.py
│           ├── models.py
│           ├── pricing.py
│           ├── provider.py
│           ├── retry.py
│           ├── routing.py
│           ├── telemetry.py
│           ├── tools.py
│           └── usage.py
└── tests/
    └── model_gateway/
        ├── fakes.py
        ├── test_adapters.py
        ├── test_circuit.py
        ├── test_gateway.py
        ├── test_models.py
        ├── test_retry.py
        ├── test_streaming.py
        └── test_tools.py
```

## Environment setup

### Dependencies

As verified on June 25, 2026, PyPI listed OpenAI Python SDK `2.44.0` and Anthropic Python SDK
`0.112.0`. Use compatible ranges and commit the exact lockfile:

```powershell
uv add "openai>=2.44,<3" "anthropic>=0.112,<1" "httpx>=0.28,<1" `
    "redis>=6,<7" "opentelemetry-api>=1.38,<2" `
    "opentelemetry-sdk>=1.38,<2"
uv lock
uv sync --locked
```

Do not assume these versions remain current. Recheck official SDK release notes when rebuilding.

### Environment variables

**`.env.example`**

```dotenv
OPENAI_API_KEY=
OPENAI_MODEL=
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=
REDIS_URL=redis://localhost:6379/0
MODEL_GATEWAY_ENV=development
MODEL_GATEWAY_MAX_ATTEMPTS=3
MODEL_GATEWAY_TOTAL_TIMEOUT_SECONDS=30
MODEL_GATEWAY_MAX_COST_USD=0.10
OTEL_SERVICE_NAME=ai-industry-model-gateway
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
```

Never commit `.env`. Production secrets must come from the deployment secret manager or an
approved workload-identity mechanism.

### Local Redis

**`compose.yaml`**

```yaml
services:
  redis:
    image: redis:8-alpine
    command: ["redis-server", "--appendonly", "no"]
    ports:
      - "127.0.0.1:6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 2s
      retries: 10
```

The local instance holds disposable circuit state only. Production Redis requires authentication,
encryption, network restriction, monitoring, and an availability decision.

### Verification

```powershell
uv run python -c "import openai, anthropic, httpx, redis; print('imports ok')"
uv run pytest tests/model_gateway -q
```

Do not run live-provider tests in ordinary CI. Use a separately approved, budget-limited job.

## Data and API contract

### Gateway request

| Field | Rule |
|---|---|
| `request_id` | Application-generated UUID |
| `tenant_id` | Trusted server context; never accepted from model output |
| `user_id` | Trusted server context |
| `operation` | Allowlisted feature name |
| `messages` | Canonical role/content sequence |
| `model_tier` | Policy name, not provider model ID |
| `max_output_tokens` | Positive and bounded |
| `temperature` | Optional and policy-bounded |
| `data_class` | Drives provider and logging policy |
| `retry_safe` | Derived from operation, not client-controlled |
| `required_capabilities` | Structured, stream, tools, image, document, or audio |
| `metadata` | Non-sensitive attribution tags |

### Valid request

```json
{
  "request_id": "4cae529f-b63f-4dca-8f70-13b7be240c36",
  "tenant_id": "northstar-demo",
  "user_id": "agent-104",
  "operation": "issue-extraction",
  "messages": [
    {
      "role": "user",
      "content": "I was charged twice for order DEMO-42."
    }
  ],
  "model_tier": "interactive-standard",
  "max_output_tokens": 200,
  "data_class": "synthetic",
  "retry_safe": true,
  "required_capabilities": ["structured"],
  "metadata": {
    "case_id": "duplicate-charge-01"
  }
}
```

### Invalid request

```json
{
  "tenant_id": "",
  "user_id": "agent-104",
  "operation": "anything-the-client-wants",
  "messages": [],
  "max_output_tokens": 1000000,
  "retry_safe": true,
  "metadata": {
    "api_key": "secret"
  }
}
```

It fails because identity, operation, message, limit, and metadata rules are violated. In a real
API, `retry_safe` is derived after authorization and is not exposed as a writable client field.

### Boundary examples

- Empty assistant history with one valid user message: allowed.
- Maximum approved message length: allowed after token preflight.
- One byte over upload limit: rejected before provider upload.
- Unknown structured field: rejected because schemas use `extra="forbid"`.
- Stream cancelled before first delta: stored as cancelled with zero or unknown usage.
- Provider returns usage but no text because of refusal: normalized as refusal, not success.

### Output contract

Every completed result contains:

- Gateway request and attempt IDs
- Provider and model
- Provider request ID when available
- Normalized finish status
- Typed data or text
- Tool-call proposals
- Measured token usage
- Latency
- Fallback and degraded-mode indicators

### Application endpoint contracts

The gateway is internal. The support API exposes business endpoints rather than a public
provider-shaped proxy:

```text
POST /v1/support/tickets/{ticket_id}/issue-extraction
GET  /v1/support/tickets/{ticket_id}/draft-stream
```

For both endpoints:

- Authentication middleware supplies the actor.
- The ticket lookup supplies the tenant and verifies access.
- The server selects operation, model tier, retry safety, and capabilities.
- Client input may select an approved user preference, but cannot select an arbitrary provider.
- The response exposes gateway status and trace correlation, not provider credentials.

The extraction endpoint returns typed issue data. The stream endpoint uses SSE and forwards
normalized `started`, `text_delta`, and terminal events. Map failures deliberately:

| Gateway outcome | Application behavior |
|---|---|
| Invalid request or unsupported capability | `422` |
| Unauthenticated or unauthorized | `401` or `403` before gateway call |
| All approved routes unavailable | `503` with correlation ID |
| Request deadline exceeded | `504` |
| Structured output rejected | Controlled `502` or domain-specific failure response |
| Stream failure after headers | SSE `failed` terminal event |
| User cancellation | Close upstream stream and persist `cancelled` |

### Privacy and retention

- Canonical support data follows the application's retention policy.
- Gateway logs omit prompt and response bodies by default.
- Usage records retain identifiers and counts needed for audit and billing.
- Provider-side storage settings and retention are reviewed per route.
- Deletion workflows include provider files and stored response objects when those features are
  used.
- Evaluation datasets use synthetic or approved redacted data.

### Versioning

Version:

- Request contract
- Output schemas
- Route configuration
- Model identifiers
- Provider SDK lockfile
- Price catalog
- Tool schemas
- Prompt versions beginning in Lesson 10

## Establish the baseline

### Baseline implementation

The prototype calls one provider directly, accepts raw text, and logs latency:

```text
handler → provider SDK → raw text
```

### Baseline measurements

Run the fixed cases and record:

| Metric | Baseline result |
|---|---|
| Schema-valid rate | |
| Provider-specific imports outside integration module | |
| Timeout configured | |
| Hidden SDK retry count | |
| Error categories distinguished | |
| Fallback tested | |
| Tenant/user usage attribution | |
| Provider request ID captured | |
| Stream terminal-state correctness | |

Do not fill values until the baseline is executed.

### Baseline failure injection

Simulate:

- Invalid JSON-like output
- 429 rate limit
- Connect timeout
- Read timeout
- 503 or 529 overload
- Invalid API key
- Client cancellation

The baseline is expected to expose missing controls. Keep the results as evidence for the gateway
change.

## Minimal working implementation

The vertical slice implements:

- Typed provider-neutral contracts
- OpenAI and Anthropic structured calls
- Normalized provider errors
- Gateway-owned retries
- Provider fallback
- Usage and trace metadata

Streaming, circuits, tools, and durable accounting are added immediately afterward.

### Package initialization

**`src/ai_industry_labs/model_gateway/__init__.py`**

```python
"""Provider-neutral model access with explicit reliability and policy."""
```

### Core models

**`src/ai_industry_labs/model_gateway/models.py`**

```python
from enum import StrEnum
from typing import Any, Generic, Literal, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

T = TypeVar("T")


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ProviderName(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class Capability(StrEnum):
    TEXT = "text"
    STRUCTURED = "structured"
    STREAM = "stream"
    TOOLS = "tools"
    IMAGE = "image"
    DOCUMENT = "document"
    AUDIO = "audio"


class Message(StrictModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1, max_length=100_000)


class GatewayRequest(StrictModel):
    request_id: UUID
    tenant_id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{1,62}$")
    user_id: str = Field(min_length=1, max_length=128)
    operation: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{1,63}$")
    messages: list[Message] = Field(min_length=1, max_length=100)
    model_tier: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{1,63}$")
    max_output_tokens: int = Field(ge=1, le=4096)
    temperature: float | None = Field(default=None, ge=0, le=2)
    data_class: Literal["synthetic", "internal", "confidential"]
    retry_safe: bool
    required_capabilities: set[Capability] = Field(
        default_factory=lambda: {Capability.TEXT}
    )
    metadata: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_metadata(self) -> "GatewayRequest":
        prohibited = {"api_key", "authorization", "prompt", "response"}
        if prohibited.intersection(key.casefold() for key in self.metadata):
            raise ValueError("metadata contains a prohibited key")
        if len(self.metadata) > 20:
            raise ValueError("metadata may contain at most 20 entries")
        return self


class Usage(StrictModel):
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    cached_input_tokens: int = Field(default=0, ge=0)


class ToolCall(StrictModel):
    call_id: str = Field(min_length=1, max_length=256)
    name: str = Field(pattern=r"^[a-zA-Z][a-zA-Z0-9_-]{0,63}$")
    arguments: dict[str, Any]


class ModelResult(StrictModel, Generic[T]):
    request_id: UUID
    attempt_id: UUID
    provider: ProviderName
    model: str
    provider_request_id: str | None
    status: Literal["completed", "refused"]
    text: str | None = None
    data: T | None = None
    tool_calls: list[ToolCall] = Field(default_factory=list)
    usage: Usage
    latency_ms: float = Field(ge=0)
    degraded: bool = False


class StreamEvent(StrictModel):
    request_id: UUID
    attempt_id: UUID
    provider: ProviderName
    model: str
    sequence: int = Field(ge=0)
    type: Literal["started", "text_delta", "completed", "failed", "cancelled"]
    delta: str | None = None
    usage: Usage | None = None
    error_kind: str | None = None
```

Verification:

```powershell
uv run python -c "from ai_industry_labs.model_gateway.models import GatewayRequest; print(GatewayRequest.model_json_schema()['title'])"
```

Expected result: `GatewayRequest`.

### Domain schema

**`src/ai_industry_labs/model_gateway/schemas.py`**

```python
from typing import Literal

from pydantic import Field, model_validator

from ai_industry_labs.model_gateway.models import StrictModel


class IssueExtraction(StrictModel):
    category: Literal["billing", "account", "technical", "security"]
    requires_approval: bool
    requested_action: Literal[
        "information", "refund", "account_change", "security_review", "none"
    ]
    summary: str = Field(min_length=1, max_length=240)

    @model_validator(mode="after")
    def require_approval_for_consequential_action(self) -> "IssueExtraction":
        if (
            self.requested_action in {"refund", "account_change"}
            and not self.requires_approval
        ):
            raise ValueError("consequential actions require approval")
        return self
```

This validator is deterministic policy. Do not replace it with a prompt instruction.

### Normalized errors

**`src/ai_industry_labs/model_gateway/errors.py`**

```python
from enum import StrEnum


class ErrorKind(StrEnum):
    AUTHENTICATION = "authentication"
    PERMISSION = "permission"
    INVALID_REQUEST = "invalid_request"
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    CONNECTION = "connection"
    PROVIDER_OVERLOAD = "provider_overload"
    PROVIDER_INTERNAL = "provider_internal"
    REFUSAL = "refusal"
    INVALID_OUTPUT = "invalid_output"
    CIRCUIT_OPEN = "circuit_open"
    BUDGET_EXCEEDED = "budget_exceeded"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


class GatewayError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        kind: ErrorKind,
        retryable: bool,
        ambiguous_completion: bool = False,
        provider_request_id: str | None = None,
        retry_after_seconds: float | None = None,
    ) -> None:
        super().__init__(message)
        self.kind = kind
        self.retryable = retryable
        self.ambiguous_completion = ambiguous_completion
        self.provider_request_id = provider_request_id
        self.retry_after_seconds = retry_after_seconds
```

### Provider port

**`src/ai_industry_labs/model_gateway/provider.py`**

```python
from collections.abc import AsyncIterator
from typing import Protocol, TypeVar

from pydantic import BaseModel

from ai_industry_labs.model_gateway.models import (
    Capability,
    GatewayRequest,
    ModelResult,
    ProviderName,
    StreamEvent,
)

T = TypeVar("T", bound=BaseModel)


class ModelProvider(Protocol):
    @property
    def name(self) -> ProviderName: ...

    @property
    def model(self) -> str: ...

    @property
    def capabilities(self) -> set[Capability]: ...

    async def generate_text(self, request: GatewayRequest) -> ModelResult[str]: ...

    async def generate_structured(
        self,
        request: GatewayRequest,
        schema: type[T],
    ) -> ModelResult[T]: ...

    def stream_text(
        self,
        request: GatewayRequest,
    ) -> AsyncIterator[StreamEvent]: ...
```

The port does not expose provider response classes.

## Production implementation

The production-learning implementation adds provider adapters, centralized retries, shared
circuit state, controlled fallback, tool enforcement, durable usage records, and telemetry.

### OpenAI adapter

OpenAI's current Python SDK recommends the Responses API as its primary model interface. The
official SDK supports async calls, SSE streaming, typed structured parsing, explicit timeouts,
typed errors, and provider request IDs.

**`src/ai_industry_labs/model_gateway/adapters/openai_adapter.py`**

```python
import asyncio
from collections.abc import AsyncIterator
from time import perf_counter
from typing import Any, TypeVar
from uuid import uuid4

import httpx
import openai
from openai import AsyncOpenAI
from pydantic import BaseModel, ValidationError

from ai_industry_labs.model_gateway.errors import ErrorKind, GatewayError
from ai_industry_labs.model_gateway.models import (
    Capability,
    GatewayRequest,
    ModelResult,
    ProviderName,
    StreamEvent,
    Usage,
)

T = TypeVar("T", bound=BaseModel)


class OpenAIAdapter:
    def __init__(self, *, api_key: str, model: str) -> None:
        self._model = model
        self._client = AsyncOpenAI(
            api_key=api_key,
            max_retries=0,
            timeout=httpx.Timeout(
                timeout=30.0,
                connect=3.0,
                read=25.0,
                write=10.0,
                pool=3.0,
            ),
        )

    @property
    def name(self) -> ProviderName:
        return ProviderName.OPENAI

    @property
    def model(self) -> str:
        return self._model

    @property
    def capabilities(self) -> set[Capability]:
        return {
            Capability.TEXT,
            Capability.STRUCTURED,
            Capability.STREAM,
            Capability.TOOLS,
            Capability.IMAGE,
            Capability.DOCUMENT,
        }

    @staticmethod
    def _input(request: GatewayRequest) -> list[dict[str, str]]:
        return [
            {"role": message.role, "content": message.content}
            for message in request.messages
        ]

    @staticmethod
    def _usage(value: Any) -> Usage:
        return Usage(
            input_tokens=int(getattr(value, "input_tokens", 0)),
            output_tokens=int(getattr(value, "output_tokens", 0)),
            cached_input_tokens=int(
                getattr(
                    getattr(value, "input_tokens_details", None),
                    "cached_tokens",
                    0,
                )
            ),
        )

    def _request_options(self, request: GatewayRequest) -> dict[str, Any]:
        options: dict[str, Any] = {
            "model": self._model,
            "input": self._input(request),
            "max_output_tokens": request.max_output_tokens,
            "store": False,
        }
        if request.temperature is not None:
            options["temperature"] = request.temperature
        return options

    async def generate_text(self, request: GatewayRequest) -> ModelResult[str]:
        attempt_id = uuid4()
        started = perf_counter()
        try:
            response = await self._client.responses.create(
                **self._request_options(request),
            )
            return ModelResult[str](
                request_id=request.request_id,
                attempt_id=attempt_id,
                provider=self.name,
                model=self.model,
                provider_request_id=response._request_id,
                status="completed",
                text=response.output_text,
                data=response.output_text,
                usage=self._usage(response.usage),
                latency_ms=(perf_counter() - started) * 1000,
            )
        except Exception as exc:
            raise self._map_error(exc) from exc

    async def generate_structured(
        self,
        request: GatewayRequest,
        schema: type[T],
    ) -> ModelResult[T]:
        attempt_id = uuid4()
        started = perf_counter()
        try:
            options = self._request_options(request)
            options["text_format"] = schema
            response = await self._client.responses.parse(
                **options,
            )
            if response.output_parsed is None:
                raise GatewayError(
                    "provider returned no parsed output",
                    kind=ErrorKind.INVALID_OUTPUT,
                    retryable=False,
                    provider_request_id=response._request_id,
                )
            data = schema.model_validate(response.output_parsed)
            return ModelResult[T](
                request_id=request.request_id,
                attempt_id=attempt_id,
                provider=self.name,
                model=self.model,
                provider_request_id=response._request_id,
                status="completed",
                data=data,
                usage=self._usage(response.usage),
                latency_ms=(perf_counter() - started) * 1000,
            )
        except ValidationError as exc:
            raise GatewayError(
                "structured output failed application validation",
                kind=ErrorKind.INVALID_OUTPUT,
                retryable=False,
            ) from exc
        except GatewayError:
            raise
        except Exception as exc:
            raise self._map_error(exc) from exc

    async def stream_text(
        self,
        request: GatewayRequest,
    ) -> AsyncIterator[StreamEvent]:
        attempt_id = uuid4()
        sequence = 0
        yield StreamEvent(
            request_id=request.request_id,
            attempt_id=attempt_id,
            provider=self.name,
            model=self.model,
            sequence=sequence,
            type="started",
        )
        try:
            options = self._request_options(request)
            options["stream"] = True
            stream = await self._client.responses.create(
                **options,
            )
            async for event in stream:
                if event.type == "response.output_text.delta":
                    sequence += 1
                    yield StreamEvent(
                        request_id=request.request_id,
                        attempt_id=attempt_id,
                        provider=self.name,
                        model=self.model,
                        sequence=sequence,
                        type="text_delta",
                        delta=event.delta,
                    )
                elif event.type == "response.completed":
                    sequence += 1
                    yield StreamEvent(
                        request_id=request.request_id,
                        attempt_id=attempt_id,
                        provider=self.name,
                        model=self.model,
                        sequence=sequence,
                        type="completed",
                        usage=self._usage(event.response.usage),
                    )
                    return
            sequence += 1
            yield StreamEvent(
                request_id=request.request_id,
                attempt_id=attempt_id,
                provider=self.name,
                model=self.model,
                sequence=sequence,
                type="failed",
                error_kind=ErrorKind.UNKNOWN,
            )
        except asyncio.CancelledError:
            sequence += 1
            yield StreamEvent(
                request_id=request.request_id,
                attempt_id=attempt_id,
                provider=self.name,
                model=self.model,
                sequence=sequence,
                type="cancelled",
                error_kind=ErrorKind.CANCELLED,
            )
            raise
        except Exception as exc:
            error = self._map_error(exc)
            sequence += 1
            yield StreamEvent(
                request_id=request.request_id,
                attempt_id=attempt_id,
                provider=self.name,
                model=self.model,
                sequence=sequence,
                type="failed",
                error_kind=error.kind,
            )

    @staticmethod
    def _map_error(exc: Exception) -> GatewayError:
        if isinstance(exc, openai.AuthenticationError):
            return GatewayError(
                "OpenAI authentication failed",
                kind=ErrorKind.AUTHENTICATION,
                retryable=False,
                provider_request_id=exc.request_id,
            )
        if isinstance(exc, openai.PermissionDeniedError):
            return GatewayError(
                "OpenAI permission denied",
                kind=ErrorKind.PERMISSION,
                retryable=False,
                provider_request_id=exc.request_id,
            )
        if isinstance(exc, openai.RateLimitError):
            return GatewayError(
                "OpenAI rate limit",
                kind=ErrorKind.RATE_LIMIT,
                retryable=True,
                provider_request_id=exc.request_id,
            )
        if isinstance(exc, openai.APITimeoutError):
            return GatewayError(
                "OpenAI request timed out",
                kind=ErrorKind.TIMEOUT,
                retryable=True,
                ambiguous_completion=True,
            )
        if isinstance(exc, openai.APIConnectionError):
            return GatewayError(
                "OpenAI connection failed",
                kind=ErrorKind.CONNECTION,
                retryable=True,
            )
        if isinstance(exc, openai.BadRequestError):
            return GatewayError(
                "OpenAI rejected the request",
                kind=ErrorKind.INVALID_REQUEST,
                retryable=False,
                provider_request_id=exc.request_id,
            )
        if isinstance(exc, openai.APIStatusError):
            retryable = exc.status_code >= 500
            return GatewayError(
                f"OpenAI status {exc.status_code}",
                kind=(
                    ErrorKind.PROVIDER_INTERNAL
                    if retryable
                    else ErrorKind.UNKNOWN
                ),
                retryable=retryable,
                provider_request_id=exc.request_id,
            )
        return GatewayError(
            "unexpected OpenAI adapter failure",
            kind=ErrorKind.UNKNOWN,
            retryable=False,
        )
```

The SDK has its own default retries. `max_retries=0` prevents hidden multiplication because this
gateway implements and records retries centrally.

### Anthropic adapter

Anthropic's current Python SDK supports async Messages API calls, streaming helpers, token
usage, typed exceptions, request IDs, and Pydantic structured parsing.

**`src/ai_industry_labs/model_gateway/adapters/anthropic_adapter.py`**

```python
import asyncio
from collections.abc import AsyncIterator
from time import perf_counter
from typing import Any, TypeVar
from uuid import uuid4

import anthropic
import httpx
from anthropic import AsyncAnthropic
from pydantic import BaseModel, ValidationError

from ai_industry_labs.model_gateway.errors import ErrorKind, GatewayError
from ai_industry_labs.model_gateway.models import (
    Capability,
    GatewayRequest,
    ModelResult,
    ProviderName,
    StreamEvent,
    Usage,
)

T = TypeVar("T", bound=BaseModel)


class AnthropicAdapter:
    def __init__(self, *, api_key: str, model: str) -> None:
        self._model = model
        self._client = AsyncAnthropic(
            api_key=api_key,
            max_retries=0,
            timeout=httpx.Timeout(
                timeout=30.0,
                connect=3.0,
                read=25.0,
                write=10.0,
                pool=3.0,
            ),
        )

    @property
    def name(self) -> ProviderName:
        return ProviderName.ANTHROPIC

    @property
    def model(self) -> str:
        return self._model

    @property
    def capabilities(self) -> set[Capability]:
        return {
            Capability.TEXT,
            Capability.STRUCTURED,
            Capability.STREAM,
            Capability.TOOLS,
            Capability.IMAGE,
            Capability.DOCUMENT,
        }

    @staticmethod
    def _parts(
        request: GatewayRequest,
    ) -> tuple[str | None, list[dict[str, str]]]:
        system = "\n\n".join(
            message.content
            for message in request.messages
            if message.role == "system"
        ) or None
        messages = [
            {"role": message.role, "content": message.content}
            for message in request.messages
            if message.role != "system"
        ]
        return system, messages

    @staticmethod
    def _usage(value: Any) -> Usage:
        return Usage(
            input_tokens=int(getattr(value, "input_tokens", 0)),
            output_tokens=int(getattr(value, "output_tokens", 0)),
            cached_input_tokens=int(
                getattr(value, "cache_read_input_tokens", 0) or 0
            ),
        )

    def _request_options(self, request: GatewayRequest) -> dict[str, Any]:
        system, messages = self._parts(request)
        options: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "max_tokens": request.max_output_tokens,
        }
        if system is not None:
            options["system"] = system
        if request.temperature is not None:
            options["temperature"] = request.temperature
        return options

    async def generate_text(self, request: GatewayRequest) -> ModelResult[str]:
        attempt_id = uuid4()
        started = perf_counter()
        try:
            response = await self._client.messages.create(
                **self._request_options(request),
            )
            text = "".join(
                block.text
                for block in response.content
                if block.type == "text"
            )
            return ModelResult[str](
                request_id=request.request_id,
                attempt_id=attempt_id,
                provider=self.name,
                model=self.model,
                provider_request_id=response._request_id,
                status="completed",
                text=text,
                data=text,
                usage=self._usage(response.usage),
                latency_ms=(perf_counter() - started) * 1000,
            )
        except Exception as exc:
            raise self._map_error(exc) from exc

    async def generate_structured(
        self,
        request: GatewayRequest,
        schema: type[T],
    ) -> ModelResult[T]:
        attempt_id = uuid4()
        started = perf_counter()
        try:
            options = self._request_options(request)
            options["output_format"] = schema
            response = await self._client.messages.parse(
                **options,
            )
            data = schema.model_validate(response.parsed_output)
            return ModelResult[T](
                request_id=request.request_id,
                attempt_id=attempt_id,
                provider=self.name,
                model=self.model,
                provider_request_id=response._request_id,
                status="completed",
                data=data,
                usage=self._usage(response.usage),
                latency_ms=(perf_counter() - started) * 1000,
            )
        except ValidationError as exc:
            raise GatewayError(
                "structured output failed application validation",
                kind=ErrorKind.INVALID_OUTPUT,
                retryable=False,
            ) from exc
        except Exception as exc:
            raise self._map_error(exc) from exc

    async def stream_text(
        self,
        request: GatewayRequest,
    ) -> AsyncIterator[StreamEvent]:
        attempt_id = uuid4()
        sequence = 0
        yield StreamEvent(
            request_id=request.request_id,
            attempt_id=attempt_id,
            provider=self.name,
            model=self.model,
            sequence=sequence,
            type="started",
        )
        try:
            async with self._client.messages.stream(
                **self._request_options(request),
            ) as stream:
                async for text in stream.text_stream:
                    sequence += 1
                    yield StreamEvent(
                        request_id=request.request_id,
                        attempt_id=attempt_id,
                        provider=self.name,
                        model=self.model,
                        sequence=sequence,
                        type="text_delta",
                        delta=text,
                    )
                final = await stream.get_final_message()
            sequence += 1
            yield StreamEvent(
                request_id=request.request_id,
                attempt_id=attempt_id,
                provider=self.name,
                model=self.model,
                sequence=sequence,
                type="completed",
                usage=self._usage(final.usage),
            )
        except asyncio.CancelledError:
            sequence += 1
            yield StreamEvent(
                request_id=request.request_id,
                attempt_id=attempt_id,
                provider=self.name,
                model=self.model,
                sequence=sequence,
                type="cancelled",
                error_kind=ErrorKind.CANCELLED,
            )
            raise
        except Exception as exc:
            error = self._map_error(exc)
            sequence += 1
            yield StreamEvent(
                request_id=request.request_id,
                attempt_id=attempt_id,
                provider=self.name,
                model=self.model,
                sequence=sequence,
                type="failed",
                error_kind=error.kind,
            )

    @staticmethod
    def _map_error(exc: Exception) -> GatewayError:
        if isinstance(exc, anthropic.AuthenticationError):
            return GatewayError(
                "Anthropic authentication failed",
                kind=ErrorKind.AUTHENTICATION,
                retryable=False,
                provider_request_id=exc.request_id,
            )
        if isinstance(exc, anthropic.PermissionDeniedError):
            return GatewayError(
                "Anthropic permission denied",
                kind=ErrorKind.PERMISSION,
                retryable=False,
                provider_request_id=exc.request_id,
            )
        if isinstance(exc, anthropic.RateLimitError):
            return GatewayError(
                "Anthropic rate limit",
                kind=ErrorKind.RATE_LIMIT,
                retryable=True,
                provider_request_id=exc.request_id,
            )
        if isinstance(exc, anthropic.APITimeoutError):
            return GatewayError(
                "Anthropic request timed out",
                kind=ErrorKind.TIMEOUT,
                retryable=True,
                ambiguous_completion=True,
            )
        if isinstance(exc, anthropic.APIConnectionError):
            return GatewayError(
                "Anthropic connection failed",
                kind=ErrorKind.CONNECTION,
                retryable=True,
            )
        if isinstance(exc, anthropic.BadRequestError):
            return GatewayError(
                "Anthropic rejected the request",
                kind=ErrorKind.INVALID_REQUEST,
                retryable=False,
                provider_request_id=exc.request_id,
            )
        if isinstance(exc, anthropic.APIStatusError):
            retryable = exc.status_code >= 500
            return GatewayError(
                f"Anthropic status {exc.status_code}",
                kind=(
                    ErrorKind.PROVIDER_OVERLOAD
                    if exc.status_code == 529
                    else ErrorKind.PROVIDER_INTERNAL
                ),
                retryable=retryable,
                provider_request_id=exc.request_id,
            )
        return GatewayError(
            "unexpected Anthropic adapter failure",
            kind=ErrorKind.UNKNOWN,
            retryable=False,
        )
```

### Adapter verification

Before real calls:

- Type-check both adapters.
- Mock the SDK clients.
- Assert provider objects never escape.
- Assert `max_retries=0`.
- Assert explicit timeout values.
- Assert output is revalidated.
- Assert request IDs and usage are normalized.

## Reliability implementation

### Bounded retry

**`src/ai_industry_labs/model_gateway/retry.py`**

```python
import asyncio
import random
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from time import monotonic
from typing import Any, TypeVar

from ai_industry_labs.model_gateway.errors import GatewayError

T = TypeVar("T")


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay_seconds: float = 0.25
    max_delay_seconds: float = 4.0
    total_timeout_seconds: float = 30.0


async def call_with_retry(
    operation: Callable[[], Awaitable[T]],
    *,
    policy: RetryPolicy,
    retry_safe: bool,
    on_failure: Callable[[int, GatewayError], Awaitable[None]],
) -> T:
    started = monotonic()
    last_error: GatewayError | None = None

    for attempt in range(1, policy.max_attempts + 1):
        try:
            remaining = policy.total_timeout_seconds - (monotonic() - started)
            if remaining <= 0:
                break
            return await asyncio.wait_for(operation(), timeout=remaining)
        except GatewayError as exc:
            last_error = exc
            await on_failure(attempt, exc)
            if not retry_safe or not exc.retryable:
                raise
            if attempt >= policy.max_attempts:
                raise

            exponential = min(
                policy.max_delay_seconds,
                policy.base_delay_seconds * (2 ** (attempt - 1)),
            )
            jittered = random.uniform(0, exponential)
            delay = max(jittered, exc.retry_after_seconds or 0)
            remaining = policy.total_timeout_seconds - (monotonic() - started)
            if delay >= remaining:
                raise
            await asyncio.sleep(delay)

    if last_error is not None:
        raise last_error
    raise TimeoutError("retry budget expired")
```

`Retry-After` or provider-specific delay headers should be normalized by adapters where exposed.
The delay is still bounded by the total request budget.

### Redis-backed circuit

**`src/ai_industry_labs/model_gateway/circuit.py`**

```python
from dataclasses import dataclass
from time import time

from redis.asyncio import Redis

from ai_industry_labs.model_gateway.models import ProviderName


@dataclass(frozen=True)
class CircuitPolicy:
    failure_threshold: int = 5
    failure_window_seconds: int = 30
    open_seconds: int = 20
    probe_seconds: int = 10


class RedisCircuitBreaker:
    def __init__(self, redis: Redis, policy: CircuitPolicy) -> None:
        self._redis = redis
        self._policy = policy

    def _key(self, provider: ProviderName, suffix: str) -> str:
        return f"model-gateway:circuit:{provider}:{suffix}"

    async def allow(self, provider: ProviderName) -> bool:
        open_key = self._key(provider, "open-until")
        value = await self._redis.get(open_key)
        if value is None:
            return True

        if float(value) > time():
            return False

        probe_key = self._key(provider, "probe")
        acquired = await self._redis.set(
            probe_key,
            "1",
            ex=self._policy.probe_seconds,
            nx=True,
        )
        return bool(acquired)

    async def record_success(self, provider: ProviderName) -> None:
        await self._redis.delete(
            self._key(provider, "failures"),
            self._key(provider, "open-until"),
            self._key(provider, "probe"),
        )

    async def record_failure(self, provider: ProviderName) -> None:
        failures_key = self._key(provider, "failures")
        failures = await self._redis.incr(failures_key)
        if failures == 1:
            await self._redis.expire(
                failures_key,
                self._policy.failure_window_seconds,
            )
        if failures >= self._policy.failure_threshold:
            await self._redis.set(
                self._key(provider, "open-until"),
                str(time() + self._policy.open_seconds),
                ex=self._policy.open_seconds + self._policy.probe_seconds,
            )
            await self._redis.delete(self._key(provider, "probe"))
```

This vertical slice uses atomic Redis commands but does not make threshold transition a single
transaction. For very high concurrency, move failure transition to a Lua script or a managed
circuit implementation and test race behavior.

Only connection, timeout, rate-limit, overload, and provider-internal failures contribute.
Authentication, invalid request, refusal, and schema failures do not indicate provider-wide
unavailability.

### Route configuration

**`model-gateway/provider-routes.yaml`**

```yaml
routes:
  interactive-standard:
    synthetic:
      - provider: openai
        model_env: OPENAI_MODEL
      - provider: anthropic
        model_env: ANTHROPIC_MODEL
    confidential:
      - provider: openai
        model_env: OPENAI_MODEL

policies:
  issue-extraction:
    required_capabilities: [structured]
    retry_safe: true
    max_attempts: 3
    total_timeout_seconds: 20
  response-drafting:
    required_capabilities: [text, stream]
    retry_safe: true
    max_attempts: 2
    total_timeout_seconds: 30
```

Routes are policy, not user input. A missing approved fallback must produce a controlled
unavailable outcome.

### Gateway orchestration

**`src/ai_industry_labs/model_gateway/gateway.py`**

```python
from collections.abc import Awaitable, Callable
from typing import TypeVar

from opentelemetry import trace
from pydantic import BaseModel

from ai_industry_labs.model_gateway.circuit import RedisCircuitBreaker
from ai_industry_labs.model_gateway.errors import ErrorKind, GatewayError
from ai_industry_labs.model_gateway.models import GatewayRequest, ModelResult
from ai_industry_labs.model_gateway.provider import ModelProvider
from ai_industry_labs.model_gateway.retry import RetryPolicy, call_with_retry

T = TypeVar("T", bound=BaseModel)
tracer = trace.get_tracer(__name__)


class ModelGateway:
    def __init__(
        self,
        *,
        routes: dict[str, list[ModelProvider]],
        circuit: RedisCircuitBreaker,
        record_attempt: Callable[
            [GatewayRequest, ModelProvider, ModelResult[Any] | None, GatewayError | None],
            Awaitable[None],
        ],
    ) -> None:
        self._routes = routes
        self._circuit = circuit
        self._record_attempt = record_attempt

    async def generate_structured(
        self,
        request: GatewayRequest,
        schema: type[T],
        *,
        retry_policy: RetryPolicy,
    ) -> ModelResult[T]:
        providers = self._routes.get(request.model_tier, [])
        if not providers:
            raise GatewayError(
                "no approved provider route",
                kind=ErrorKind.INVALID_REQUEST,
                retryable=False,
            )

        last_error: GatewayError | None = None
        for route_index, provider in enumerate(providers):
            if not request.required_capabilities.issubset(provider.capabilities):
                continue
            if not await self._circuit.allow(provider.name):
                last_error = GatewayError(
                    f"circuit open for {provider.name}",
                    kind=ErrorKind.CIRCUIT_OPEN,
                    retryable=True,
                )
                continue

            async def operation() -> ModelResult[T]:
                result = await provider.generate_structured(request, schema)
                await self._circuit.record_success(provider.name)
                return result

            async def on_failure(attempt: int, error: GatewayError) -> None:
                del attempt
                if error.kind in {
                    ErrorKind.RATE_LIMIT,
                    ErrorKind.TIMEOUT,
                    ErrorKind.CONNECTION,
                    ErrorKind.PROVIDER_OVERLOAD,
                    ErrorKind.PROVIDER_INTERNAL,
                }:
                    await self._circuit.record_failure(provider.name)
                await self._record_attempt(request, provider, None, error)

            with tracer.start_as_current_span("model_gateway.request") as span:
                span.set_attribute("gen_ai.operation.name", request.operation)
                span.set_attribute("gen_ai.provider.name", provider.name)
                span.set_attribute("gen_ai.request.model", provider.model)
                span.set_attribute("app.tenant_id", request.tenant_id)
                span.set_attribute("app.gateway_request_id", str(request.request_id))
                try:
                    result = await call_with_retry(
                        operation,
                        policy=retry_policy,
                        retry_safe=request.retry_safe,
                        on_failure=on_failure,
                    )
                    result.degraded = route_index > 0
                    await self._record_attempt(request, provider, result, None)
                    return result
                except GatewayError as exc:
                    last_error = exc
                    span.record_exception(exc)
                    if not request.retry_safe:
                        raise

        if last_error is not None:
            raise last_error
        raise GatewayError(
            "no route satisfies required capabilities",
            kind=ErrorKind.INVALID_REQUEST,
            retryable=False,
        )
```

Do not mutate a frozen result in production. Either make `ModelResult` mutable intentionally, as
above, or use `result.model_copy(update={"degraded": route_index > 0})`.

### Milestone verification

Use fake providers to verify:

1. Primary success returns without fallback.
2. Retryable primary failure retries within the same route.
3. Exhausted primary failure uses the approved fallback.
4. Terminal primary failure is not retried.
5. Unsafe request is not retried or routed after ambiguous failure.
6. Open circuit skips the route.
7. Missing capability rejects the route.
8. Every attempt is recorded.

## Tool calling and controlled execution

### Provider-neutral tool definition

**`src/ai_industry_labs/model_gateway/tools.py`**

```python
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from ai_industry_labs.model_gateway.errors import ErrorKind, GatewayError
from ai_industry_labs.model_gateway.models import ToolCall

ArgsT = TypeVar("ArgsT", bound=BaseModel)


@dataclass(frozen=True)
class ToolContext:
    tenant_id: str
    user_id: str
    operation: str


@dataclass(frozen=True)
class RegisteredTool(Generic[ArgsT]):
    name: str
    arguments_model: type[ArgsT]
    handler: Callable[[ToolContext, ArgsT], Awaitable[dict[str, Any]]]
    read_only: bool
    requires_human_approval: bool


class ToolRegistry:
    def __init__(self, tools: list[RegisteredTool[Any]]) -> None:
        self._tools = {tool.name: tool for tool in tools}
        if len(self._tools) != len(tools):
            raise ValueError("duplicate tool names")

    async def execute(
        self,
        call: ToolCall,
        *,
        context: ToolContext,
        approved: bool,
    ) -> dict[str, Any]:
        tool = self._tools.get(call.name)
        if tool is None:
            raise GatewayError(
                "tool is not allowed",
                kind=ErrorKind.INVALID_REQUEST,
                retryable=False,
            )
        if tool.requires_human_approval and not approved:
            raise GatewayError(
                "tool requires approval",
                kind=ErrorKind.PERMISSION,
                retryable=False,
            )
        arguments = tool.arguments_model.model_validate(call.arguments)
        return await tool.handler(context, arguments)
```

Provider adapters translate their tool schema and call objects into `RegisteredTool` schemas and
`ToolCall` records. The registry remains the execution authority.

### Tool safety rules

- Read and write tools use separate credentials.
- Tenant and resource authorization use trusted context.
- Write tools require idempotency keys.
- Consequential writes require explicit approval.
- Tool loops have step, time, and cost limits.
- Unknown tools fail closed.
- Tool results are size-bounded and treated as untrusted context.
- Automatic provider fallback stops if a write may have executed.
- Tool arguments and outcomes are audited without secrets.

### Multimodal request policy

Before sending image, document, or audio input:

1. Validate the requested capability against the route.
2. Verify tenant ownership and user permission.
3. Validate media type and byte size.
4. Scan files according to security policy.
5. Remove unsupported metadata where required.
6. Apply retention and deletion policy.
7. Record file identifiers, not raw bytes, in telemetry.
8. Treat document instructions as untrusted content.

Do not silently convert unsupported modalities in the adapter. Use an explicit preprocessing
service and record the transformation.

## Conversation state

Use application-owned canonical messages:

```text
conversation
├── tenant_id
├── participants and permissions
├── ordered canonical messages
├── attachments
├── prompt version
└── optional provider continuation metadata
```

OpenAI's Responses API supports chaining with `previous_response_id`, but prior input tokens in a
chain are still relevant to billing and context management. Provider response storage and
retention settings must be reviewed. A gateway may use provider continuation as an optimization,
but fallback requires sufficient canonical state to reconstruct the request for another
provider.

Conversation controls:

- Reauthorize ticket access on every request.
- Bound history by token and policy budgets.
- Summaries are derived state, not replacements for required audit history.
- Delete provider files or stored objects where policy requires.
- Never use a provider conversation ID as authorization.

## Usage and cost accounting

### Price catalog

Do not hard-code prices in adapters.

**`model-gateway/price-catalog.yaml`**

```yaml
catalog_version: "2026-06-25-example"
currency: "USD"
verified_at: "REPLACE_WITH_ACTUAL_VERIFICATION_TIME"
prices:
  - provider: "openai"
    model: "REPLACE_WITH_APPROVED_MODEL"
    effective_from: "REPLACE_WITH_PROVIDER_EFFECTIVE_DATE"
    input_per_million: null
    cached_input_per_million: null
    output_per_million: null
  - provider: "anthropic"
    model: "REPLACE_WITH_APPROVED_MODEL"
    effective_from: "REPLACE_WITH_PROVIDER_EFFECTIVE_DATE"
    input_per_million: null
    cached_input_per_million: null
    output_per_million: null
```

`null` prevents fabricated cost. Deployment fails its cost-readiness gate until approved values
are supplied from current provider pricing.

### Cost calculation

```text
estimated cost =
uncached input tokens × input rate
+ cached input tokens × cached-input rate
+ output tokens × output rate
+ provider-specific tool or service charges
```

Use decimal arithmetic for currency.

**`src/ai_industry_labs/model_gateway/pricing.py`**

```python
from decimal import Decimal

from pydantic import BaseModel, Field

from ai_industry_labs.model_gateway.models import Usage


class ModelPrice(BaseModel):
    input_per_million: Decimal = Field(ge=0)
    cached_input_per_million: Decimal = Field(ge=0)
    output_per_million: Decimal = Field(ge=0)


def estimate_cost(usage: Usage, price: ModelPrice) -> Decimal:
    million = Decimal(1_000_000)
    uncached = max(usage.input_tokens - usage.cached_input_tokens, 0)
    return (
        Decimal(uncached) * price.input_per_million
        + Decimal(usage.cached_input_tokens) * price.cached_input_per_million
        + Decimal(usage.output_tokens) * price.output_per_million
    ) / million
```

### Usage ledger schema

```sql
CREATE TABLE model_usage (
    usage_id UUID PRIMARY KEY,
    gateway_request_id UUID NOT NULL,
    attempt_id UUID NOT NULL,
    tenant_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    operation TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    provider_request_id TEXT,
    input_tokens INTEGER NOT NULL CHECK (input_tokens >= 0),
    cached_input_tokens INTEGER NOT NULL CHECK (cached_input_tokens >= 0),
    output_tokens INTEGER NOT NULL CHECK (output_tokens >= 0),
    estimated_cost_usd NUMERIC(18, 8),
    price_catalog_version TEXT,
    status TEXT NOT NULL,
    error_kind TEXT,
    latency_ms DOUBLE PRECISION NOT NULL,
    degraded BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (gateway_request_id, attempt_id)
);

CREATE INDEX model_usage_tenant_created_idx
ON model_usage (tenant_id, created_at);
```

Record failed attempts even when usage is unknown. Use `NULL`, not zero, when the provider did not
report usage.

## Testing

### Fake provider

**`tests/model_gateway/fakes.py`**

```python
from collections.abc import AsyncIterator
from typing import TypeVar
from uuid import uuid4

from pydantic import BaseModel

from ai_industry_labs.model_gateway.errors import GatewayError
from ai_industry_labs.model_gateway.models import (
    Capability,
    GatewayRequest,
    ModelResult,
    ProviderName,
    StreamEvent,
    Usage,
)

T = TypeVar("T", bound=BaseModel)


class FakeProvider:
    def __init__(
        self,
        *,
        name: ProviderName,
        structured_value: dict[str, object] | None = None,
        failures: list[GatewayError] | None = None,
    ) -> None:
        self._name = name
        self._value = structured_value or {}
        self._failures = list(failures or [])
        self.calls = 0

    @property
    def name(self) -> ProviderName:
        return self._name

    @property
    def model(self) -> str:
        return "fake-model"

    @property
    def capabilities(self) -> set[Capability]:
        return {Capability.TEXT, Capability.STRUCTURED, Capability.STREAM}

    async def generate_structured(
        self,
        request: GatewayRequest,
        schema: type[T],
    ) -> ModelResult[T]:
        self.calls += 1
        if self._failures:
            raise self._failures.pop(0)
        value = schema.model_validate(self._value)
        return ModelResult[T](
            request_id=request.request_id,
            attempt_id=uuid4(),
            provider=self.name,
            model=self.model,
            provider_request_id="fake-request",
            status="completed",
            data=value,
            usage=Usage(input_tokens=10, output_tokens=5),
            latency_ms=1,
        )

    async def generate_text(self, request: GatewayRequest) -> ModelResult[str]:
        raise NotImplementedError

    async def stream_text(
        self,
        request: GatewayRequest,
    ) -> AsyncIterator[StreamEvent]:
        if False:
            yield
        raise NotImplementedError
```

### Required test categories

| Category | Protects |
|---|---|
| Unit | Validation, pricing, error mapping, retry delay, route selection |
| Adapter contract | Equivalent normalized output from mocked provider SDKs |
| Integration | Redis circuit behavior and usage database writes |
| End-to-end | Application request through fake provider to typed result |
| Security | Secret redaction, tenant spoofing, unknown tools, oversized input |
| Failure | Timeouts, 429, overload, invalid output, open circuit, cancellation |
| Streaming | Sequence, exactly one terminal event, partial failure |
| Live smoke | Current provider credentials, model, schema, and request ID |

### Critical tests

**`tests/model_gateway/test_retry.py`**

```python
import pytest

from ai_industry_labs.model_gateway.errors import ErrorKind, GatewayError
from ai_industry_labs.model_gateway.retry import RetryPolicy, call_with_retry


@pytest.mark.asyncio
async def test_terminal_error_is_not_retried() -> None:
    calls = 0

    async def operation() -> str:
        nonlocal calls
        calls += 1
        raise GatewayError(
            "bad request",
            kind=ErrorKind.INVALID_REQUEST,
            retryable=False,
        )

    async def observe(attempt: int, error: GatewayError) -> None:
        assert attempt == 1
        assert error.kind is ErrorKind.INVALID_REQUEST

    with pytest.raises(GatewayError):
        await call_with_retry(
            operation,
            policy=RetryPolicy(max_attempts=3),
            retry_safe=True,
            on_failure=observe,
        )

    assert calls == 1


@pytest.mark.asyncio
async def test_unsafe_operation_is_not_retried() -> None:
    calls = 0

    async def operation() -> str:
        nonlocal calls
        calls += 1
        raise GatewayError(
            "read timeout",
            kind=ErrorKind.TIMEOUT,
            retryable=True,
            ambiguous_completion=True,
        )

    async def observe(attempt: int, error: GatewayError) -> None:
        assert attempt == 1
        assert error.ambiguous_completion

    with pytest.raises(GatewayError):
        await call_with_retry(
            operation,
            policy=RetryPolicy(max_attempts=3),
            retry_safe=False,
            on_failure=observe,
        )

    assert calls == 1
```

Additional assertions:

- Invalid provider output never returns a `ModelResult`.
- A fallback result has `degraded=true`.
- Fallback is blocked when the alternate route is not approved for the data class.
- Authentication errors do not open the provider circuit.
- A stream with a failure has one terminal event.
- Cancellation closes the provider stream.
- Unknown tool names fail before handler execution.
- Tool arguments reject extra fields.
- Usage rows are unique by gateway request and attempt.
- Telemetry contains no API key, raw prompt, or full response.

## Evaluation

### Held-out evaluation set

Create at least:

- 20 structured extraction cases
- 10 streaming cases
- 12 injected provider failures
- 6 fallback-policy cases
- 8 tool-call cases
- 6 media-policy cases
- 4 cancellation cases
- 4 tenant-isolation attacks

Keep the fault set unchanged while comparing baseline and gateway.

### Functional metrics

- Valid request success rate
- Schema gate pass rate
- Correct error classification
- Correct retry decision
- Correct fallback decision
- Stream terminal-event validity
- Tool argument validation rate
- Usage attribution completeness

### Reliability metrics

- Requests by provider and outcome
- Attempts per gateway request
- Retry success rate
- Circuit-open rate
- Fallback rate
- Degraded success rate
- Cancellation rate
- Unknown-outcome rate

### Performance metrics

- End-to-end P50, P95, and P99 latency
- Time to first text delta
- Inter-delta gap
- Retry-added latency
- Fallback-added latency
- Gateway overhead with fake provider
- Concurrent request throughput
- Redis and database latency

### Cost metrics

- Cost per request
- Cost per completed request
- Cost per accepted agent draft
- Duplicate-attempt cost
- Fallback cost delta
- Cost by tenant, operation, provider, and model

### Security gates

- No client-supplied tenant override
- No secret in source, logs, spans, or exceptions
- No unknown tool execution
- No unapproved provider route
- No raw customer content in default telemetry
- No automatic replay of ambiguous consequential writes

### Comparison table

Do not fill values until tests run.

| Metric | Direct SDK baseline | Gateway primary only | Gateway with fallback | Acceptance |
|---|---:|---:|---:|---|
| Schema-valid downstream records | | | | 100% |
| Correct fault classification | | | | 100% fixed set |
| Unsafe automatic replays | | | | 0 |
| Complete attribution | | | | 100% |
| P95 gateway overhead with fake provider | | | | Team-defined |
| Stream terminal validity | | | | 100% |
| Fallback trace completeness | | | | 100% |
| Cost per accepted draft | | | | Measure |

### Evaluation integrity

- Provider quality is not the focus of this lesson.
- Do not compare providers with different prompts and call it a gateway comparison.
- Record all attempts, including failed and fallback calls.
- Do not report unknown usage as zero.
- Separate gateway overhead from provider latency.
- Use dated price configuration.
- Mark live smoke tests separately from mocked reliability tests.

## Failure modes and debugging

| Symptom | Likely causes | Diagnostic evidence | Corrective action | Prevention |
|---|---|---|---|---|
| Three configured attempts create nine calls | SDK and gateway both retry | Attempt trace versus provider request IDs | Disable one retry layer | Retry ownership test |
| Invalid record reaches database | Raw text path bypassed schema gate | Trace lacks validation span | Require typed gateway method | Type and integration gates |
| Fallback changes answer shape | Semantic mismatch or schema mapping defect | Adapter contract diff | Fix adapter or prohibit route | Capability and parity tests |
| High latency during outage | Circuit never opens or wrong errors counted | Circuit keys and error histogram | Correct qualification and threshold | Failure injection |
| Circuit opens on bad requests | 400 errors counted as health failures | Error-kind metrics | Exclude caller defects | Circuit unit tests |
| Circuit never recovers | Probe lock or TTL defect | Redis key TTLs | Clear state and fix half-open logic | Recovery test |
| Stream ends without status | Disconnect or unhandled event | Missing terminal event | Emit failed/cancelled in `finally` | Stream invariant test |
| Two completed events | Provider completion plus wrapper completion | Sequence trace | Centralize terminal emission | Property test |
| Usage is zero after fallback | Only final attempt recorded | Multiple provider request IDs | Record every attempt | Ledger completeness check |
| Cost spikes without traffic growth | More retries, longer outputs, model route change | Attempts and token histograms | Roll back route; reduce budgets | Cost alerts |
| Provider says request ID unknown | Wrong ID logged or content redacted incorrectly | Attempt record | Capture provider public request ID | Adapter contract test |
| 429 retry storm | No jitter or ignored retry delay | Synchronized retry timestamps | Add full jitter and delay header | Load fault test |
| Timeout repeats a write | Tool execution inside retryable provider loop | Tool audit and attempt trace | Separate generation from execution | Write-safety architecture |
| Tenant data reaches wrong route | Client-controlled route or policy bug | Route decision audit | Derive route server-side | Tenant isolation tests |
| Tool has valid shape but wrong resource | Authorization omitted | Tool context and target IDs | Enforce resource authz | Security test |
| Redis unavailable blocks all requests | Fail policy undefined | Redis errors | Choose fail-open or fail-closed by operation | Dependency runbook |
| Provider model changed silently | Floating alias | Model ID/version trace | Pin or detect change; reevaluate | Change-control gate |
| Provider structured parser returns none | Refusal, unsupported model, or incomplete output | Raw status and request ID | Normalize refusal/failure | Provider-specific tests |
| Logs contain ticket text | Broad object serialization | Log sample | Allowlist log fields and redact | Telemetry test |

## Security, privacy, and governance

### Authentication and authorization

- The gateway accepts trusted service identity or verified application context.
- Browser clients never receive provider keys.
- Tenant and user IDs are resolved server-side.
- Route and model tier are policy decisions.
- Tool execution rechecks resource-level authorization.
- Model output never grants permission.

### Secret handling

- Store provider keys in a secret manager.
- Use separate development and production projects.
- Restrict secret access to the gateway runtime identity.
- Rotate and revoke keys.
- Do not place keys in prompts, logs, traces, images, container layers, or exception messages.
- Prefer approved short-lived workload identity where supported.

### Tenant isolation

- Query and tool filters include trusted tenant ID.
- Usage rows include tenant ID.
- Cache and circuit keys do not store customer content.
- Provider route policy is evaluated by tenant and data class.
- Fallback cannot widen data permissions.

### Sensitive data

- Classify content before routing.
- Minimize what is sent.
- Redact or tokenize identifiers when the task allows.
- Review provider storage, training-use, region, subprocessors, and deletion terms.
- Keep content telemetry disabled by default.
- Apply access-controlled sampling only for approved debugging and evaluation.

### Prompt injection

Documents and tool results are untrusted content. The gateway:

- Does not treat document text as authorization.
- Does not permit documents to select tools or routes.
- Restricts tools independently of model instructions.
- Preserves source labels for Lesson 10 prompt separation.

### Auditability

Audit:

- Identity and tenant
- Operation and route decision
- Provider and model
- Schema and tool versions
- Attempts, errors, and fallback
- Tool approvals and outcomes
- Usage and estimated cost
- Deployment version

Do not use audit logs as a raw prompt archive.

### Governance decisions

Maintain:

- Approved provider/model registry
- Data-class route matrix
- Model and provider change review
- Price catalog owner
- Incident owner
- Retention and deletion schedule
- Live-test budget
- Deprecation and exit plan

## Performance and cost

### Latency budget

```text
end-to-end latency =
queue
+ gateway validation
+ circuit and route lookup
+ provider connection and generation
+ retry delays
+ fallback delay
+ output validation
+ usage persistence
```

Set operation-specific deadlines. Interactive drafts and batch extraction should not share one
timeout.

### Connection management

- Reuse async SDK clients.
- Configure connect, read, write, and pool timeouts.
- Bound connection pools.
- Close clients during application shutdown.
- Do not create one client per request.
- Test proxy and DNS behavior in the deployment environment.

### Concurrency

- Bound concurrent provider calls per instance.
- Apply tenant and operation quotas before provider calls.
- Use provider rate-limit headers where available.
- Avoid holding database transactions during generation.
- Cancel abandoned streams.
- Protect Redis and database pools from gateway fan-out.

### Token and cost budgets

Before a request:

- Bound message count and bytes.
- Estimate or count tokens where supported.
- Reserve output tokens.
- Enforce per-request cost ceiling.
- Apply tenant daily and monthly budgets.

After a request:

- Record provider-reported usage.
- Reconcile provider billing exports.
- Alert on token, retry, fallback, and cost drift.

### Measurement procedure

1. Run fake-provider tests to measure gateway overhead.
2. Run controlled live calls with fixed input and output bounds.
3. Separate cold and warm connections.
4. Measure no-retry, retry, and fallback paths.
5. Report time to first delta and total stream time.
6. Measure database and Redis contribution.
7. Calculate cost per accepted draft, not only per call.

## Deployment

### Packaging

- Build the existing service image from the locked environment.
- Run as a non-root user.
- Include no `.env` or credentials.
- Scan dependencies and image.
- Emit build and commit identifiers.

### Configuration

Validate at startup:

- Required provider credentials for enabled routes
- Non-empty approved model IDs
- Route capability consistency
- Retry and timeout bounds
- Redis and database connectivity
- Complete price entries for cost-enforced routes
- OpenTelemetry exporter configuration

Do not expose secret values in readiness errors.

### Health endpoints

- **Liveness:** process event loop is responsive.
- **Readiness:** configuration is valid and required local dependencies are reachable.
- **Dependency status:** provider state is reported separately; do not make liveness depend on an
  external provider.

### Release strategy

```text
unit and contract tests
→ fake-provider end-to-end
→ development live smoke
→ shadow request metadata
→ internal canary tenants
→ bounded pilot
```

Do not send duplicate live shadow traffic with customer content unless privacy, cost, and provider
policy explicitly approve it.

### Migration

1. Add gateway behind a feature flag.
2. Keep direct integration available for rollback.
3. Route synthetic and internal tests first.
4. Compare output contracts and usage records.
5. Canary a small eligible agent group.
6. Remove direct provider imports from business handlers.

### Rollback

Rollback can restore:

- Previous service image
- Previous route configuration
- Previous model identifier
- Previous timeout and retry policy
- Single-provider mode
- Direct integration temporarily, if still maintained and safe

Circuit and retry state may need clearing after a policy rollback. Preserve audit records.

## Observability and operations

### Structured logs

Allowlisted fields:

- Trace, gateway request, and attempt IDs
- Tenant and user internal IDs
- Operation
- Provider and model
- Status and error kind
- Provider request ID
- Latency and token counts
- Retry and fallback indicators
- Circuit decision

Default-deny prompt, response, tool-result, secret, and raw file content.

### Traces

Suggested spans:

```text
support.request
└── model_gateway.request
    ├── route.select
    ├── provider.attempt
    ├── retry.wait
    ├── fallback.select
    ├── output.validate
    ├── tool.execute
    └── usage.persist
```

Do not attach high-cardinality raw content as attributes.

### Metrics

- `gateway_requests_total`
- `provider_attempts_total`
- `provider_errors_total`
- `gateway_retries_total`
- `gateway_fallbacks_total`
- `circuit_open_total`
- `gateway_latency_seconds`
- `time_to_first_token_seconds`
- `input_tokens_total`
- `output_tokens_total`
- `estimated_cost_usd_total`
- `schema_validation_failures_total`
- `tool_calls_total`
- `streams_cancelled_total`

Label cardinality must be bounded. Do not use raw request, user, or ticket IDs as metric labels.

### Alerts

- Provider error rate above threshold
- P95 latency above SLO
- Circuit remains open
- Fallback rate rises materially
- Schema validation failures appear
- Usage ledger write failures
- Token or cost spike
- Unknown model identifier
- Authentication failures after deployment
- Stream terminal-state defects

### SLO example

For eligible interactive drafting during the pilot:

- 99% gateway availability excluding rejected invalid requests
- 95% of successful streams produce first text within the approved threshold
- 100% typed outputs pass schema validation
- 100% attempts have attribution records
- 0 unauthorized tool executions

Set numeric latency thresholds from measured pilot data, not invention.

### Incident runbook

1. Confirm affected operation, tenants, providers, and deployment.
2. Check error kind, circuit state, rate-limit state, and provider status.
3. Inspect provider request IDs and trace samples.
4. Disable a failing route or model through configuration.
5. Confirm fallback data policy and capacity before enabling it broadly.
6. Reduce concurrency or output budget during rate pressure.
7. Roll back if schema, authorization, or tool safety regressed.
8. Reconcile usage and cost after recovery.
9. Preserve redacted evidence and write a post-incident review.

## Practical assignment

### Scenario

Northstar adds an internal security-ticket assistant. Security tickets are confidential, cannot
use the general fallback provider, and may call a read-only account-risk tool. The output must be
typed and the analyst must approve any escalation.

### Requirements

Build a gateway extension that:

- Adds a `security-triage` operation.
- Defines a strict `SecurityTriage` schema.
- Allows only approved confidential-data routes.
- Uses a different timeout and retry policy from drafting.
- Adds a read-only `lookup_account_risk` tool.
- Validates tenant and account access before tool execution.
- Emits normalized streaming progress or a typed final result.
- Records all attempts and usage.
- Rejects fallback to an unapproved provider.
- Adds failure injection for rate limit, timeout, invalid output, and Redis unavailability.

### Constraints

- No real customer or security incident data.
- No write-capable security action.
- No raw content in standard telemetry.
- Maximum two provider attempts.
- No fabricated price or measured result.

### Required artifacts

- Architecture decision record
- Capability and route matrix
- Pydantic request and output schemas
- Provider adapter contract tests
- Retry and circuit tests
- Tool authorization tests
- Usage schema and sample redacted record
- Evaluation table
- Deployment and rollback plan
- Incident runbook

### Acceptance criteria

- All downstream triage records are schema-valid.
- No confidential request reaches an unapproved route.
- No unsafe operation is automatically replayed.
- Every stream has exactly one terminal event.
- All attempts are attributable.
- Unknown tools and extra arguments fail closed.
- Failure and recovery paths are tested.
- Conclusions distinguish measured results from design expectations.

### Stretch goals

- Add a local OpenAI-compatible adapter and document tested compatibility.
- Use a Lua script for atomic circuit transitions.
- Add workload identity for a supported provider.
- Reconcile the usage ledger with a provider usage export.
- Implement per-tenant token-bucket admission control.

## Interview preparation

### Concept questions

**Why use a provider adapter?**

A strong answer explains isolation of API shapes, errors, usage, streaming, and capability
differences while preserving explicit semantic differences.

**What is the difference between structured output and validation?**

Structured output constrains generation. Validation checks the returned object. Domain rules and
authorization remain application responsibilities.

**Why can a timeout be ambiguous?**

The client may stop waiting after the provider accepted or completed work. This matters especially
for tool side effects and cost.

**Why disable SDK retries?**

When the gateway owns retries, hidden SDK retries obscure attempts, multiply latency and cost,
and complicate safety decisions.

### Coding questions

- Implement full-jitter exponential backoff with a deadline.
- Normalize two provider error hierarchies.
- Validate a generic Pydantic response type.
- Enforce exactly one terminal stream event.
- Calculate cost with decimal arithmetic.

Strong solutions include bounds, cancellation, observability, and tests.

### Debugging scenarios

**Calls tripled after a release.**

Check SDK retry defaults, gateway attempt count, queue redelivery, and duplicate client requests.
Use provider request IDs and attempt traces.

**Fallback succeeds but costs doubled.**

Inspect primary ambiguous attempts, output lengths, fallback model rates, and whether every retry
was necessary.

**Circuit opens during a bad deployment.**

Determine whether 400 or authentication errors were incorrectly counted as provider health
failures.

**Valid JSON caused an unauthorized action.**

Identify missing domain authorization and approval controls. Schema compliance is not authority.

### System-design question

Design a model gateway for:

- 100 tenants
- Two hosted providers
- Interactive and batch workloads
- Confidential-data route restrictions
- Structured extraction and streaming drafts
- Read and write tools
- Tenant chargeback
- Provider outages and deprecations

A strong answer covers requirements, trust boundaries, canonical state, routing, rate limits,
retry safety, circuits, tool controls, observability, usage reconciliation, rollout, and rollback.

### Tradeoff questions

- In-process library versus dedicated gateway service
- Provider-native state versus application-owned state
- Primary retry versus immediate fallback
- Shared abstraction versus provider-specific features
- Fail-open versus fail-closed when Redis is unavailable
- Content logging versus privacy

## One-page memory sheet

### Central model

```text
authenticate and authorize
→ create canonical request
→ validate policy and budget
→ choose approved capable route
→ check circuit
→ call adapter with explicit timeout
→ normalize result or error
→ retry only if transient + safe + budgeted
→ fallback only if approved + capable + observable
→ validate schema and domain rules
→ authorize tools outside model
→ record trace, usage, cost, and outcome
```

### Decision table

| Situation | Action |
|---|---|
| Invalid key or request | Fail; do not retry |
| Rate limit or overload | Bounded retry; respect delay; consider circuit/fallback |
| Timeout during pure generation | Retry only within latency and cost policy |
| Timeout after possible write | Do not replay automatically |
| Invalid structured output | Reject; optional bounded repair policy |
| Open circuit | Fail fast or use approved fallback |
| Unsupported capability | Reject or select explicit capable route |
| Unknown tool | Fail closed |
| Missing usage | Store unknown, not zero |
| Provider model changes | Rerun contract and quality evaluation |

### Five common misconceptions

1. Provider-neutral means providers are equivalent.
2. Valid JSON means safe business data.
3. Every timeout is safe to retry.
4. Strict tool arguments authorize execution.
5. Observability requires storing prompts and responses.

### Essential constraints

```text
retry = transient ∧ repeat-safe ∧ within budget
fallback = approved ∧ capable ∧ healthy ∧ semantically acceptable
tool execution = allowlisted ∧ validated ∧ authorized ∧ approved when required
cost = measured usage × dated price configuration
stream = started → deltas* → exactly one terminal event
```

### Essential commands

```powershell
docker compose up -d redis
uv sync --locked
uv run pytest tests/model_gateway -q
uv run pytest tests/model_gateway/test_retry.py -q
uv run pytest tests/model_gateway/test_streaming.py -q
```

## Retrieval bank

Answer closed-book:

1. Draw the gateway request flow.
2. Separate application, gateway, adapter, and provider responsibilities.
3. Explain canonical conversation state.
4. Define semantic parity.
5. List structured-output validation layers.
6. Draw a valid stream event sequence.
7. State the three retry conditions.
8. Explain ambiguous completion.
9. Draw the circuit state machine.
10. Give three fallback prerequisites.
11. Explain why provider-wide circuits ignore bad requests.
12. Describe tool-call authorization.
13. Explain why a PDF remains untrusted.
14. Distinguish four request identifiers.
15. Explain why usage may be unknown rather than zero.
16. Diagnose hidden retry multiplication.
17. Compare an in-process gateway with a gateway service.
18. Design a confidential-data route with no fallback.
19. Predict how cancellation affects usage and status.
20. Defend a policy for content-free telemetry.

## Spaced-review plan

### One day later

- Draw the full request flow.
- Recreate the retry decision table.
- Explain schema validation versus authorization.
- Write the legal stream-event sequence.

### Three days later

- Implement `call_with_retry` from memory.
- Classify ten example failures.
- Draw the circuit states.
- Explain one unsafe tool replay.

### One week later

- Design a new provider adapter contract.
- Create a route matrix for confidential data.
- Diagnose a retry and cost spike.
- Reconstruct the usage ledger fields.

### Three to four weeks later

- Complete the security-ticket transfer assignment without copying the worked example.
- Run a failure-injection review.
- Defend the architecture in a 30-minute system-design interview.
- Add prompt and schema versions from Lesson 10 to traces and usage records.

## Self-assessment

Score each item:

- `0`: cannot explain
- `1`: recognize with notes
- `2`: explain and implement with minor reference
- `3`: implement, test, diagnose, and defend independently

| Capability | Score |
|---|---:|
| Draw the gateway boundary | |
| Design provider-neutral contracts | |
| Implement an adapter | |
| Enforce structured validation | |
| Normalize streaming | |
| Classify provider errors | |
| Implement safe bounded retries | |
| Operate a circuit breaker | |
| Design observable fallback | |
| Control tool execution | |
| Attribute usage and cost | |
| Deploy and debug the gateway | |

Do not proceed to prompt engineering until contract, validation, retry safety, and tracing score
at least `2`.

## Production-readiness checklist

- [ ] Identity and tenant come from trusted application context.
- [ ] Operations, routes, providers, and models are allowlisted.
- [ ] Provider SDK objects do not cross adapter boundaries.
- [ ] Canonical conversation state is application-owned.
- [ ] Provider secrets are server-side and externally managed.
- [ ] Separate development and production credentials exist.
- [ ] Provider data handling, region, retention, and deletion are approved.
- [ ] Message, byte, token, output, time, attempt, and spending limits exist.
- [ ] Connect, read, write, pool, and total deadlines are explicit.
- [ ] Exactly one layer owns retries.
- [ ] Retryable and terminal errors are tested.
- [ ] Ambiguous completion is represented.
- [ ] Unsafe or consequential writes are not automatically replayed.
- [ ] Retry delay uses bounded backoff and jitter.
- [ ] Circuit failures are qualified correctly.
- [ ] Circuit recovery and Redis failure behavior are tested.
- [ ] Fallback routes satisfy data policy and capabilities.
- [ ] Fallback is visible in traces, metrics, records, and user behavior where relevant.
- [ ] Structured output is revalidated.
- [ ] Domain invariants are deterministic.
- [ ] Refusal and invalid output are distinct outcomes.
- [ ] Every stream has one terminal event.
- [ ] Cancellation closes resources and records status.
- [ ] Tool names and arguments are allowlisted and validated.
- [ ] Resource authorization occurs before tool execution.
- [ ] Consequential tools require approval and idempotency.
- [ ] Multimodal uploads are validated, scanned, permissioned, and retained correctly.
- [ ] Provider request IDs are captured.
- [ ] Every attempt has tenant, user, operation, provider, and model attribution.
- [ ] Unknown usage is not recorded as zero.
- [ ] Prices are external, dated, and complete before cost enforcement.
- [ ] Logs and spans exclude secrets and raw content by default.
- [ ] Metric labels have bounded cardinality.
- [ ] Contract, integration, security, streaming, and failure tests pass.
- [ ] Live tests use synthetic data and a spending limit.
- [ ] Canary and rollback procedures are documented.
- [ ] Model and SDK changes trigger reevaluation.
- [ ] Provider deprecation and exit plans exist.
- [ ] Incident owner and runbook are assigned.

## Lesson summary

You converted a hosted model from an SDK dependency into a controlled production capability.

You learned:

- The application owns identity, authorization, business state, and human approval.
- The gateway owns routing, validation, reliability, tracing, and usage policy.
- Adapters isolate provider API shapes, events, errors, and usage objects.
- Provider neutrality normalizes contracts but does not erase semantic differences.
- Structured generation still requires application and domain validation.
- Streaming requires explicit event ordering, cancellation, and terminal status.
- Retry is valid only for transient, repeat-safe work within a bounded budget.
- Timeouts can create ambiguous completion.
- Circuit breakers reduce repeated pressure during sustained failures.
- Fallback must be approved, capable, observable, and semantically acceptable.
- Tool calls are proposals; application controls authorize effects.
- Canonical conversation state enables provider change and fallback.
- Token usage comes from provider metadata.
- Cost comes from measured usage and dated configuration.
- Useful observability does not require default storage of sensitive content.

The cumulative project now has a provider-independent gateway with structured output, streaming,
timeouts, bounded retries, circuit state, fallback, tool controls, tracing, and cost attribution.

The next lesson, **Prompt and Context Engineering**, will add versioned task instructions, output
contracts, untrusted-content separation, prompt regression tests, and prompt identifiers to this
gateway.

## Official references

Technical behavior was verified on June 25, 2026.

### OpenAI

- OpenAI Python SDK:
  <https://github.com/openai/openai-python>
- Responses API reference:
  <https://developers.openai.com/api/reference/resources/responses/methods/create>
- Structured model outputs:
  <https://developers.openai.com/api/docs/guides/structured-outputs>
- Streaming API responses:
  <https://developers.openai.com/api/docs/guides/streaming-responses>
- Function calling:
  <https://developers.openai.com/api/docs/guides/function-calling>
- Conversation state:
  <https://developers.openai.com/api/docs/guides/conversation-state>
- Images and vision:
  <https://developers.openai.com/api/docs/guides/images-vision>
- File inputs:
  <https://developers.openai.com/api/docs/guides/file-inputs>
- Rate limits:
  <https://developers.openai.com/api/docs/guides/rate-limits>
- Production best practices:
  <https://developers.openai.com/api/docs/guides/production-best-practices>

### Anthropic

- Anthropic Python SDK:
  <https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python>
- Messages API:
  <https://platform.claude.com/docs/en/api/messages>
- Streaming messages:
  <https://platform.claude.com/docs/en/build-with-claude/streaming>
- Structured outputs:
  <https://platform.claude.com/docs/en/build-with-claude/structured-outputs>
- Define tools:
  <https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools>
- API errors:
  <https://platform.claude.com/docs/en/api/errors>
- Rate limits:
  <https://platform.claude.com/docs/en/api/rate-limits>

### Supporting tools

- HTTPX timeouts:
  <https://www.python-httpx.org/advanced/timeouts/>
- HTTPX exceptions:
  <https://www.python-httpx.org/exceptions/>
- Pydantic models:
  <https://docs.pydantic.dev/latest/concepts/models/>
- Redis Python client:
  <https://redis.io/docs/latest/develop/clients/redis-py/>
- OpenTelemetry Python instrumentation:
  <https://opentelemetry.io/docs/languages/python/instrumentation/>
