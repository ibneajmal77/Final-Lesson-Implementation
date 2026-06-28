# Model API Integration and Multi-Provider Reliability

## Lesson brief

| Item | Detail |
|---|---|
| What you learn | How to build a provider-independent model gateway with authentication boundaries, message/response contracts, streaming, structured output validation, tool-call controls, multimodal request handling, retries, fallback, tracing, usage, and cost attribution. |
| What you build | A runnable multi-provider AI gateway for the Northstar Support pilot with two provider adapters, schema-constrained JSON, streaming events, bounded retries, circuit breaking, usage ledger, OpenTelemetry hooks, Redis-ready state, FastAPI endpoint, Docker packaging, and tests. |
| Why it matters | Production applications cannot call hosted models as disposable scripts. They need a stable service boundary where provider-specific behavior, failures, cost, security, and output validity are controlled before business logic depends on model output. |
| Primary roles | Applied AI Engineer, Generative AI Engineer, Forward-Deployed AI Engineer, AI Solutions Architect, AI Platform Engineer. |
| Prerequisites | Lessons 01-08, especially Lesson 08 token/cost/model-behavior concepts; Python; HTTP; JSON; async basics; basic API authentication. |
| Tools | Python, FastAPI, HTTPX, Pydantic, pytest, OpenTelemetry, Redis, Docker, native provider SDKs as optional adapter variants. |
| Estimated time | 9-12 hours study, 12-18 hours implementation. |
| Final deliverable | A tested multi-provider gateway that returns validated support-draft JSON, streams output events, records usage by tenant/user, and makes fallback behavior observable. |
| Carries forward | Lesson 10 uses this gateway to manage prompt versions, prompt regression tests, context boundaries, and prompt injection controls. |
| Verified | Current API/tool guidance checked against official documentation on June 27, 2026. |

This lesson is an application-engineering lesson with deep reliability content. The core idea is not "learn one provider SDK." The core idea is to create a stable boundary between your product and changing model providers.

## Business target

Northstar Support wants to integrate a model candidate selected in Lesson 08 into a support-agent workflow. The model may classify a ticket, extract issue details, and draft a response, but it must not make customer-facing decisions by itself.

| Area | Decision |
|---|---|
| Current workflow | Experiments are run manually or through one-off scripts. Provider calls are not isolated, structured outputs are not guaranteed, and cost is not attributed to tenant/user/feature. |
| Target workflow | Applications call one internal gateway contract. The gateway routes to an approved provider, validates output, streams events, applies retry/fallback policy, records cost/usage, and exposes traces. |
| Inputs | Tenant/user identity, feature name, support ticket text, optional conversation state, optional multimodal parts, requested output schema, approved tool names, model route preference. |
| Outputs | Validated `DraftResponse`, stream events, provider metadata, usage record, trace identifiers, and explicit failure classification. |
| Constraints | No hard-coded secrets, no real customer data in the lesson, no model-authorized business actions, no invalid structured output passed downstream, retries only on safe failures. |
| Risk level | High. API integration failures can cause outages, hidden cost spikes, duplicate actions, privacy violations, or unsafe customer-facing output. |
| Acceptance metrics | Provider-specific code isolated; schema-invalid output rejected; fallback tested and observable; usage attributable by tenant/user; retry policy bounded and safe; traces include provider/model/request IDs. |

Non-goals:

- This lesson does not design the final prompt package; Lesson 10 handles prompt and context engineering.
- This lesson does not build RAG; retrieval begins later.
- This lesson does not allow autonomous write actions.
- This lesson does not claim one provider is globally best.
- This lesson does not require paid API credentials for the required path; real provider calls are optional.

## Starting checkpoint

You should already know:

- Token count drives cost and latency.
- Model outputs vary with decoding settings and provider/model revisions.
- Structured output still needs validation.
- Provider data policy, region, and model revision matter before production use.
- Human approval remains mandatory for customer-facing support responses.

Required setup:

- Python 3.11 or newer.
- A virtual environment.
- Docker only for the deployment section.
- Redis is optional for local learning; in-memory state is used in tests.
- Real provider API keys are optional. The required project runs with fake and mocked adapters.

Answer before continuing:

- Why should business code not call provider SDKs directly?
- Which failures are safe to retry, and which are not?
- What must happen when a provider returns malformed JSON?
- Why does fallback need to be visible in traces and reports?
- Why should usage be attributed to tenant and user, not only to provider account?

## System map and build roadmap

Content labels used in this lesson:

- **Concept:** API boundary and reliability ideas you must be able to explain.
- **Project:** code, tests, commands, and artifacts you can copy into the gateway.
- **Production:** operational controls required before real deployment.
- **Interview:** reasoning patterns you should defend without notes.

### Source compliance contract

| Source requirement | Where it is handled |
|---|---|
| Provider authentication | Business target, contracts, adapter config, security section. |
| Messages and responses | Module 1 and `schemas.py`. |
| Structured output | Module 4 and validation tests. |
| Function/tool calling | Module 4 and `tools.py`. |
| Streaming | Module 5 and stream tests. |
| Image, audio, document input | Module 5 as typed multimodal parts; adapter support is capability-gated. |
| Conversation state | Module 1 as explicit request state and next-lesson bridge. |
| Token accounting | Modules 2 and 7; usage ledger. |
| Rate limits, timeouts, retries | Module 6. |
| Provider error classification | Module 6 and `errors.py`. |
| Fallback models/providers | Modules 3 and 6. |
| Request tracing | Module 7 and OpenTelemetry hooks. |
| Usage and cost attribution | Module 7, evaluation, checklist. |
| Cost tracking | Module 7 records token usage and computes configurable estimated cost. |
| Provider-independent adapters | Modules 2 and 3 isolate provider-specific code behind the gateway interface. |
| Multi-provider model gateway | The project builds a gateway with primary and fallback provider adapters. |
| Provider outages | Module 6 and the failure-mode table cover outages, circuit breaking, and fallback. |
| Native provider SDK | Accounted as optional adapter variant; required path uses HTTPX/mocked adapters for reproducibility. |
| HTTPX | Core provider adapter transport. |
| Pydantic | Core schemas and validation. |
| OpenTelemetry | Tracing hooks. |
| Redis | Production-ready shared usage/circuit state; local tests use in-memory substitute. |

### Concept map

```text
application request
  -> identity and policy boundary
  -> provider-neutral GatewayRequest
  -> router selects provider/model
  -> adapter maps neutral request to provider API
  -> provider response or stream
  -> error classifier / retry / circuit breaker / fallback
  -> structured output validator and tool gate
  -> usage ledger and trace
  -> business logic receives only validated output
```

The key product rule:

```text
The model provider returns text/events.
The gateway decides whether those results are safe, valid, attributable, and usable.
```

### Project architecture

```text
FastAPI endpoint
  -> GatewayService
      -> Router
          -> FakeProviderAdapter
          -> HTTPXProviderAdapter
      -> StructuredOutputValidator
      -> ToolRegistry
      -> RetryPolicy + CircuitBreaker
      -> UsageLedger
      -> OpenTelemetry tracing
  -> DraftResponse or StreamEvent
```

### Trust boundaries

| Boundary | Rule |
|---|---|
| External caller | Must supply tenant/user/feature identity; never trust caller-provided cost or provider metadata. |
| Secrets | API keys come from environment/secret manager; never from request body. |
| Provider output | Untrusted until schema-validated and policy-checked. |
| Tool calls | Tool name and arguments are validated against an allowlist before execution. |
| Streaming | Partial chunks are not final validated business output. |
| Fallback | Must be logged and traced; hidden fallback makes debugging and cost attribution unreliable. |
| Usage ledger | Records metadata and token/cost estimates; it must not store raw sensitive customer text. |

### State ownership

| State | Owner | Persistence rule |
|---|---|---|
| Gateway request | Application caller | Immutable after accepted. |
| Provider credentials | Deployment environment/secret manager | Never committed. |
| Route policy | Gateway config | Version when changed. |
| Circuit state | In-memory for lesson, Redis in production | Shared state needed across replicas. |
| Usage/cost records | Usage ledger | Usage and cost attribution by tenant, user, feature, provider, model. |
| Conversation state | Application layer | Gateway accepts state but does not own long-term memory in this lesson. |
| Trace IDs | Observability stack | Propagate through logs and provider metadata when possible. |

### Failure boundaries

| Failure | Boundary | Expected containment |
|---|---|---|
| Missing API key | Adapter initialization/config | Gateway refuses provider route before request execution. |
| Provider timeout | Adapter/retry layer | Retry only if policy says safe; then fallback if configured. |
| Rate limit | Error classifier | Backoff, circuit signal, observable fallback. |
| Invalid structured output | Validation gate | Rejected before business logic receives it. |
| Tool hallucination | Tool registry | Unknown tool rejected; arguments schema-validated. |
| Stream cancellation | Stream event boundary | Caller receives terminal error/cancel event; usage marked partial. |
| Duplicate write risk | Retry policy | Non-idempotent requests are not retried automatically. |

### Tool choices

| Capability | Default tool | Why selected | Limitation | Alternative / switching point |
|---|---|---|---|---|
| HTTP transport | HTTPX | Explicit timeout, async client, mockable transport | You must map provider APIs yourself | Native SDK when it reduces boilerplate and still stays isolated |
| Native SDK | Optional adapter variant | Useful for provider-specific streaming/tool helpers | Can spread provider coupling if used directly in business code | Keep inside adapter package only |
| Schema validation | Pydantic | Strict request/response contracts | Validation is not semantic truth | JSON Schema for cross-language contracts |
| API surface | FastAPI | Clear typed local service boundary | Not a complete API platform | API Gateway, Cloud Run, ECS, Kubernetes |
| Tests | pytest | Fast unit/contract/failure tests | Not a load-testing tool | Locust/k6 for load tests |
| Shared circuit/usage state | Redis | Common low-latency shared state | Needs operational ownership | Managed Redis/Memorystore/ElastiCache |
| Tracing | OpenTelemetry | Provider-neutral traces | Backend setup still required | Cloud-native tracing SDKs |
| Packaging | Docker | Reproducible deployment artifact | Image/model cache size concerns | Native venv for local-only workflows |

### Project structure

```text
model-api-gateway/
├── pyproject.toml
├── .env.example
├── Dockerfile
├── model_gateway/
│   ├── __init__.py
│   ├── schemas.py
│   ├── errors.py
│   ├── validation.py
│   ├── tools.py
│   ├── reliability.py
│   ├── usage.py
│   ├── tracing.py
│   ├── streaming.py
│   ├── gateway.py
│   ├── api.py
│   └── providers/
│       ├── __init__.py
│       ├── base.py
│       ├── fake.py
│       └── httpx_provider.py
└── tests/
    ├── test_schemas.py
    ├── test_provider_adapter.py
    ├── test_validation.py
    ├── test_tools.py
    ├── test_reliability.py
    ├── test_gateway.py
    ├── test_streaming.py
    ├── test_usage.py
    └── test_api.py
```

### Environment setup

```toml
# pyproject.toml
[project]
name = "model-api-gateway"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "fastapi>=0.111,<1.0",
  "httpx>=0.27,<1.0",
  "opentelemetry-api>=1.25,<2.0",
  "opentelemetry-sdk>=1.25,<2.0",
  "pydantic>=2.7,<3.0",
  "redis>=5.0,<7.0",
  "uvicorn>=0.30,<1.0"
]

[project.optional-dependencies]
dev = ["pytest>=8.0,<9.0", "pytest-asyncio>=0.23,<1.0"]
provider-sdk = ["openai>=1.0", "anthropic>=0.25"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

```text
# .env.example
GATEWAY_ENV=local
DEFAULT_PROVIDER=fake-primary
FALLBACK_PROVIDER=fake-fallback
OPENAI_API_KEY=replace-in-secret-manager-not-here
ANTHROPIC_API_KEY=replace-in-secret-manager-not-here
REDIS_URL=redis://localhost:6379/0
```

Run after creating files:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

### Data/API contract

The gateway contract is provider-neutral. It does not expose provider-specific SDK objects to product code.

Valid request example:

```json
{
  "request_id": "req_001",
  "tenant_id": "northstar-demo",
  "user_id": "agent-42",
  "feature": "support_draft",
  "messages": [
    {"role": "system", "content": "Draft cautious support replies."},
    {"role": "user", "content": "Customer asks for refund but no order date is available."}
  ],
  "response_schema": "draft_response",
  "allowed_tools": ["lookup_order_status"],
  "idempotency_key": "tenant-demo:req_001"
}
```

Invalid request examples:

- missing `tenant_id`;
- no user message;
- unknown tool name;
- non-idempotent request marked retryable;
- request asks the model to perform a customer-facing write action.

Boundary example:

- streaming can emit partial text chunks, but only the terminal validated response may reach downstream business logic.

### Baseline

The baseline is a deterministic fake provider. It proves the gateway contract, validation, retry, fallback, usage, and tracing behavior before any real provider credentials are used. It does not prove model quality.

### Build milestones

| Module | Type | Concept focus | Implementation artifact | Tests |
|---|---|---|---|---|
| 1 | Concept-build | Provider boundary, messages, conversation state | request/response schemas | schema tests |
| 2 | Hybrid | Provider interface and adapters | base adapter, fake adapter, HTTPX adapter | adapter contract tests |
| 3 | Hybrid | Routing and fallback | gateway service and router | fallback tests |
| 4 | Hybrid | Structured output and tools | validator and tool registry | validation/tool tests |
| 5 | Hybrid | Streaming and multimodal requests | stream event model and capability checks | streaming tests |
| 6 | Hybrid | Errors, timeouts, retries, circuit breaker | error classifier and reliability policy | retry/circuit tests |
| 7 | Implementation | Usage, cost, tracing, Redis | usage ledger and trace hooks | usage tests |
| 8 | Implementation | API, deployment, operations | FastAPI app, Dockerfile, runbook | API/health tests |

### Implementation assembly checklist

At the end of this lesson, your project should contain:

- `model_gateway/schemas.py`
- `model_gateway/errors.py`
- `model_gateway/providers/base.py`
- `model_gateway/providers/fake.py`
- `model_gateway/providers/httpx_provider.py`
- `model_gateway/validation.py`
- `model_gateway/tools.py`
- `model_gateway/reliability.py`
- `model_gateway/usage.py`
- `model_gateway/tracing.py`
- `model_gateway/streaming.py`
- `model_gateway/gateway.py`
- `model_gateway/api.py`
- tests for schemas, validation, tools, reliability, gateway, streaming, and usage

After each module, run:

```bash
pytest
```

Final verification:

```bash
pytest
uvicorn model_gateway.api:app --reload
```

Expected final artifact: a local gateway that accepts a support-draft request, returns only validated structured output, records usage by tenant/user, and can fall back from one provider adapter to another.

## Concept-build module 1: API boundary, messages, and conversation state

### Core question

What contract should product code depend on so provider APIs can change without breaking the application?

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| API boundary | The API boundary is the stable contract your product code depends on. It keeps provider changes from spreading through the application. | Product code sends `GatewayRequest` instead of calling one provider SDK directly. |
| Provider authentication | Provider authentication proves your gateway is allowed to call a hosted model. It must be handled as secret infrastructure, not normal request data. | An API key lives in environment configuration, not inside a support ticket payload. |
| Message format | A message format describes roles and content sent to a model. A neutral internal format prevents provider-specific quirks from leaking outward. | `role="user"` with text content can later be translated into Provider A or Provider B's format. |
| Response format | A response format is the gateway's validated output contract. Downstream services should not depend on raw provider JSON. | The UI receives `draft`, `category`, and `needs_human_review`, not a provider-specific JSON blob. |
| Conversation state | Conversation state is the prior context needed for this request. It must have a clear owner because state can contain sensitive data and cost tokens. | The caller sends the ticket and prior messages explicitly instead of assuming the gateway remembers them. |
| Idempotency key | An idempotency key identifies a logical request so retries do not accidentally duplicate side effects. | Retrying `draft-req-123` should not create two usage records or two external tool actions. |

### Connected dry run

Northstar wants one cautious support draft, but it does not want product code tied to a single provider's SDK.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | Product code creates one internal request. | API boundary, `GatewayRequest` |
| 2 | The request carries role-based messages and explicit context. | Message format, conversation state |
| 3 | The gateway adds provider credentials outside the request body. | Provider authentication, secret handling |
| 4 | The provider returns raw output in its own shape. | Provider response, adapter boundary |
| 5 | The gateway validates and normalizes the output. | Response format, schema validation |
| 6 | Retries use a stable request identity. | Idempotency key |
| 7 | Product code receives only the stable gateway response. | `GatewayResponse`, API boundary |

Input situation:

```text
Product workflow:
Agent asks for a support draft for ticket T-1001.
```

Step 1: product code creates one internal request.

The product should not start by asking, "Which provider SDK method do I call?" It should build a gateway request:

```text
tenant_id = northstar-demo
user_id = agent-42
feature = support_draft
```

This is the API boundary. Product services depend on this boundary because it is owned by Northstar's application, not by any model provider.

Step 2: the request carries role-based messages and explicit context.

The request includes messages:

```text
system: Draft cautious replies for support agents.
user: Customer says order A-1049 was charged twice.
```

If previous ticket history matters, the caller includes it explicitly. The gateway does not silently remember private conversation state. That prevents hidden cost, hidden privacy risk, and hard-to-debug behavior.

Step 3: the gateway adds provider authentication outside the request body.

The provider key is not part of the support ticket. It comes from environment configuration or a secret manager. This keeps credentials out of logs, test fixtures, and user-controlled input.

Step 4: the provider returns raw output in its own shape.

Provider A might return `output_text`. Provider B might return `content[0].text`. The raw response is not the product contract. It belongs inside the adapter.

Step 5: the gateway validates and normalizes the output.

The gateway converts provider output into a validated `GatewayResponse`. If the provider returns malformed JSON or an unsafe draft, the gateway rejects it before business logic receives it.

Step 6: retries use a stable request identity.

If a timeout occurs before a response arrives, the gateway may retry. The idempotency key tells the system, "this is still the same logical request." Without it, retries can double-count usage or duplicate side effects.

Step 7: product code receives only the stable gateway response.

The UI or workflow service receives:

```text
draft
category
needs_human_review
usage metadata
provider/model metadata
```

The product does not need to know which provider field contained the text. That is the core value of the boundary.

### Mental model

Do not make the provider SDK your product boundary. The product should depend on a stable internal contract:

```text
Product code -> GatewayRequest -> GatewayResponse
Provider SDK/API -> hidden inside adapter
```

A message is one turn or instruction in a conversation-like model request. A response is what the gateway returns after provider output is validated and attributed. Conversation state is prior context, but this lesson keeps state explicit in each request rather than storing long-term memory inside the gateway.

### Worked example

Northstar wants a support draft. Product code should not decide whether the request goes to Provider A or Provider B. It should send:

```text
tenant_id = northstar-demo
user_id = agent-42
feature = support_draft
messages = system + user ticket
response_schema = draft_response
allowed_tools = lookup_order_status
```

The gateway decides:

- which provider/model is allowed for that tenant;
- whether the request may be retried;
- whether fallback is allowed;
- whether the output matches `DraftResponse`;
- how usage is recorded.

### Mini-implementation

```python
# model_gateway/__init__.py
__all__ = []
```

```python
# model_gateway/schemas.py
from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


Role = Literal["system", "user", "assistant", "tool"]
Modality = Literal["text", "image", "audio", "document"]


class MessagePart(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Modality
    text: str | None = None
    media_url: str | None = None
    mime_type: str | None = None

    @field_validator("media_url")
    @classmethod
    def reject_local_file_urls(cls, value: str | None) -> str | None:
        if value and value.startswith("file:"):
            raise ValueError("local file URLs are not allowed in provider requests")
        return value


class Message(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: Role
    content: str | list[MessagePart]

    def plain_text(self) -> str:
        if isinstance(self.content, str):
            return self.content
        return "\n".join(part.text or "" for part in self.content if part.type == "text")


class DraftResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: Literal["refund", "shipping", "account", "technical", "other"]
    urgency: Literal["low", "medium", "high"]
    draft: str = Field(min_length=1, max_length=2_000)
    needs_human_review: bool = True
    missing_information: list[str] = Field(default_factory=list)
    unsupported_claims: list[str] = Field(default_factory=list)


class ToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)


class GatewayRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str = Field(min_length=1)
    tenant_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    feature: str = Field(min_length=1)
    messages: list[Message] = Field(min_length=1)
    response_schema: Literal["draft_response"] = "draft_response"
    allowed_tools: list[str] = Field(default_factory=list)
    requested_provider: str | None = None
    idempotency_key: str | None = None
    stream: bool = False
    retry_safe: bool = True
    max_output_tokens: int = Field(default=400, ge=1, le=4_000)

    @field_validator("messages")
    @classmethod
    def require_user_message(cls, value: list[Message]) -> list[Message]:
        if not any(message.role == "user" for message in value):
            raise ValueError("at least one user message is required")
        return value


class ProviderUsage(BaseModel):
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)
    estimated_cost_usd: float = Field(default=0.0, ge=0)


class ProviderResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str
    text: str
    usage: ProviderUsage = Field(default_factory=ProviderUsage)
    provider_request_id: str | None = None
    finish_reason: str | None = None
    tool_calls: list[ToolCall] = Field(default_factory=list)
    raw_metadata: dict[str, Any] = Field(default_factory=dict)


class StreamEventType(str, Enum):
    START = "start"
    DELTA = "delta"
    TOOL_CALL = "tool_call"
    ERROR = "error"
    DONE = "done"


class StreamEvent(BaseModel):
    event: StreamEventType
    request_id: str
    text_delta: str = ""
    tool_call: ToolCall | None = None
    error_type: str | None = None
    provider: str | None = None
    model: str | None = None
    usage: ProviderUsage | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class GatewayResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    tenant_id: str
    user_id: str
    feature: str
    provider: str
    model: str
    validated: DraftResponse
    usage: ProviderUsage
    fallback_used: bool = False
    provider_request_id: str | None = None
    trace_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
```

### Tests

```python
# tests/test_schemas.py
from __future__ import annotations

import pytest
from pydantic import ValidationError

from model_gateway.schemas import GatewayRequest, Message, MessagePart


def test_gateway_request_requires_user_message() -> None:
    with pytest.raises(ValidationError):
        GatewayRequest(
            request_id="r1",
            tenant_id="t1",
            user_id="u1",
            feature="support_draft",
            messages=[Message(role="system", content="Only system text.")],
        )


def test_multimodal_part_rejects_local_file_url() -> None:
    with pytest.raises(ValidationError):
        MessagePart(type="image", media_url="file:///secret.png", mime_type="image/png")


def test_gateway_request_accepts_valid_message() -> None:
    request = GatewayRequest(
        request_id="r1",
        tenant_id="northstar-demo",
        user_id="agent-42",
        feature="support_draft",
        messages=[Message(role="user", content="Draft a cautious reply.")],
        allowed_tools=["lookup_order_status"],
        idempotency_key="northstar-demo:r1",
    )
    assert request.messages[0].plain_text() == "Draft a cautious reply."
```

### Verify

```bash
pytest tests/test_schemas.py
```

Expected result: all schema tests pass; invalid conversation and local file URL are rejected.

### Module completion checkpoint

At this point, your project should:

- contain `model_gateway/schemas.py`;
- define provider-neutral requests, responses, messages, multimodal parts, tool calls, stream events, and usage metadata;
- reject malformed request state before provider execution.

### Common misconception

Misconception: "A gateway is just a thin wrapper around an SDK."

Why it seems plausible: Early prototypes often call one SDK and return the result.

Correct model: A production gateway is a policy boundary. It owns validation, routing, retries, fallback, usage, tracing, and security controls.

Test case: Ask where structured output validation happens. If the answer is "after business logic receives it," the boundary is wrong.

### Guided practice and independent transfer

- Guided: Add a `feature="ticket_classification"` request and explain which fields should stay identical across providers.
- Independent transfer: Design a provider-neutral request for a summarization feature without adding provider-specific fields.

### Recall

- Why should provider SDK objects not leak into business code?
- What is an idempotency key?
- Why is a stream delta not a validated business response?
- Who owns conversation state in this lesson?

## Hybrid module 2: Provider interface and adapters

### Core question

How do you isolate provider-specific request and response shapes while keeping the gateway contract stable?

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Provider adapter | A provider adapter translates between the gateway contract and one provider's API. It keeps provider details isolated. | `OpenAIAdapter` and `FakeAdapter` both return `ProviderResponse`. |
| Provider request shape | Each provider expects its own payload format. The adapter owns that translation. | One provider uses `messages`; another may use `input` or `contents`. |
| Provider response shape | Each provider returns output, usage, and request IDs differently. The adapter normalizes them. | `id`, `request_id`, and `trace_id` may all represent provider request identity. |
| Fake adapter | A fake adapter gives deterministic local behavior for tests. It lets the gateway be tested without credentials or network calls. | A fake provider always returns a known support draft. |
| HTTP client adapter | An HTTP client adapter makes explicit network calls with timeouts and mockable transports. It exposes real API failure behavior. | `httpx` can simulate a 429 or timeout in tests. |
| Native SDK adapter | A native SDK adapter wraps a provider SDK behind the same interface. It can be useful, but it should not become the product boundary. | A provider SDK call still returns a normalized `ProviderResponse`. |

### Connected dry run

Trace one request through two different providers while product code sees one stable contract.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | Product code sends a gateway request. | API boundary |
| 2 | The gateway chooses an adapter. | Provider adapter |
| 3 | The adapter converts the request to provider-specific JSON or SDK input. | Provider request shape |
| 4 | The provider returns raw provider-specific output. | Provider response shape |
| 5 | The adapter normalizes the raw output. | `ProviderResponse` |
| 6 | Tests use a fake adapter to prove gateway behavior without network calls. | Fake adapter |
| 7 | Integration tests use an HTTP adapter with a mock transport. | HTTP client adapter |

Step 1: product code sends a gateway request.

The caller sends a `GatewayRequest` with messages, tenant, feature, response schema, and tool permissions. It does not construct Provider A's exact JSON payload.

Step 2: the gateway chooses an adapter.

Routing may select `fake-primary` for local tests or `provider-a` for a real environment. Both must satisfy the same adapter interface.

Step 3: the adapter converts the request.

Provider A might need:

```json
{"messages":[{"role":"user","content":"..."}]}
```

Provider B might need:

```json
{"input":[{"speaker":"user","parts":[{"text":"..."}]}]}
```

The adapter owns this difference. If provider formatting changes, the adapter and its tests change, not the product workflow.

Step 4: the provider returns raw output.

Provider output may contain text, usage, safety metadata, request IDs, or error details in provider-specific fields. Raw output is useful for debugging but unsafe as a product contract.

Step 5: the adapter normalizes the response.

The adapter returns:

```text
ProviderResponse(provider, model, text, usage, provider_request_id)
```

Now the rest of the gateway can validate structured output, record usage, and apply fallback without knowing the provider's field names.

Step 6: tests use a fake adapter.

The fake adapter makes behavior deterministic. It proves routing, validation, usage recording, and error handling without a network dependency.

Step 7: HTTP adapter tests simulate real provider behavior.

The HTTPX adapter can be tested with mock transports for timeouts, rate limits, invalid JSON, and changed response fields. This catches provider-integration failures before production traffic sees them.

### Concept model

An adapter translates between the gateway contract and one provider's API. The adapter is the only place where provider-specific endpoints, headers, payloads, SDK calls, response fields, and request IDs should appear.

Two adapter types are useful:

- **Fake adapter:** deterministic local behavior for tests and baseline.
- **HTTPX adapter:** explicit provider HTTP calls with timeout and mockable transport.

Native SDKs are also valid, but they should live behind the same adapter interface. This lesson keeps the required path runnable without credentials by implementing fake and HTTPX adapters; native SDK adapters are a production variant, not the boundary itself.

### Product consequence

If provider-specific code spreads into product services, fallback becomes expensive, testing becomes brittle, and model deprecation becomes a product outage. If it is isolated, changing provider request format means changing one adapter and its contract tests.

### Worked example

Provider A might return:

```json
{"id":"a-123","output_text":"...","usage":{"input_tokens":100}}
```

Provider B might return:

```json
{"request_id":"b-123","content":[{"text":"..."}],"usage":{"input_tokens":100}}
```

The gateway should normalize both into:

```text
ProviderResponse(provider, model, text, usage, provider_request_id)
```

### Build

```python
# model_gateway/errors.py
from __future__ import annotations

from enum import Enum


class ProviderErrorKind(str, Enum):
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    TRANSIENT = "transient"
    INVALID_REQUEST = "invalid_request"
    SERVER_ERROR = "server_error"
    CONTENT_FILTER = "content_filter"
    UNKNOWN = "unknown"


class GatewayError(Exception):
    pass


class ProviderError(GatewayError):
    def __init__(
        self,
        message: str,
        *,
        kind: ProviderErrorKind,
        provider: str,
        retryable: bool = False,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.kind = kind
        self.provider = provider
        self.retryable = retryable
        self.status_code = status_code


class StructuredOutputError(GatewayError):
    pass


class ToolPolicyError(GatewayError):
    pass


class CircuitOpenError(GatewayError):
    pass
```

```python
# model_gateway/providers/base.py
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from model_gateway.schemas import GatewayRequest, ProviderResponse, StreamEvent


class ProviderAdapter(ABC):
    provider_name: str
    model_name: str

    @abstractmethod
    async def complete(self, request: GatewayRequest) -> ProviderResponse:
        raise NotImplementedError

    @abstractmethod
    async def stream(self, request: GatewayRequest) -> AsyncIterator[StreamEvent]:
        raise NotImplementedError
```

```python
# model_gateway/providers/fake.py
from __future__ import annotations

from collections.abc import AsyncIterator

from model_gateway.errors import ProviderError, ProviderErrorKind
from model_gateway.providers.base import ProviderAdapter
from model_gateway.schemas import GatewayRequest, ProviderResponse, ProviderUsage, StreamEvent, StreamEventType


class FakeProviderAdapter(ProviderAdapter):
    def __init__(
        self,
        provider_name: str = "fake-primary",
        model_name: str = "fake-support-model",
        *,
        fail_with: ProviderErrorKind | None = None,
        malformed: bool = False,
    ) -> None:
        self.provider_name = provider_name
        self.model_name = model_name
        self.fail_with = fail_with
        self.malformed = malformed

    async def complete(self, request: GatewayRequest) -> ProviderResponse:
        if self.fail_with is not None:
            raise ProviderError(
                f"{self.provider_name} failed with {self.fail_with.value}",
                kind=self.fail_with,
                provider=self.provider_name,
                retryable=self.fail_with in {
                    ProviderErrorKind.RATE_LIMIT,
                    ProviderErrorKind.TIMEOUT,
                    ProviderErrorKind.TRANSIENT,
                    ProviderErrorKind.SERVER_ERROR,
                },
            )

        if self.malformed:
            text = '{"category": "refund", "urgency": "medium", "draft": ""}'
        else:
            text = (
                '{"category":"refund","urgency":"medium",'
                '"draft":"I can help draft a cautious reply. Please verify the order date and policy before approving any refund.",'
                '"needs_human_review":true,'
                '"missing_information":["order date","policy evidence"],'
                '"unsupported_claims":[]}'
            )

        input_tokens = sum(len(message.plain_text().split()) for message in request.messages)
        output_tokens = max(1, len(text.split()))
        return ProviderResponse(
            provider=self.provider_name,
            model=self.model_name,
            text=text,
            usage=ProviderUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
            ),
            provider_request_id=f"{self.provider_name}-{request.request_id}",
            finish_reason="stop",
        )

    async def stream(self, request: GatewayRequest) -> AsyncIterator[StreamEvent]:
        yield StreamEvent(
            event=StreamEventType.START,
            request_id=request.request_id,
            provider=self.provider_name,
            model=self.model_name,
        )
        response = await self.complete(request)
        for token in response.text.split():
            yield StreamEvent(
                event=StreamEventType.DELTA,
                request_id=request.request_id,
                text_delta=token + " ",
                provider=self.provider_name,
                model=self.model_name,
            )
        yield StreamEvent(
            event=StreamEventType.DONE,
            request_id=request.request_id,
            provider=self.provider_name,
            model=self.model_name,
            usage=response.usage,
        )
```

```python
# model_gateway/providers/httpx_provider.py
from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

import httpx

from model_gateway.errors import ProviderError, ProviderErrorKind
from model_gateway.providers.base import ProviderAdapter
from model_gateway.schemas import DraftResponse, GatewayRequest, Message, ProviderResponse, ProviderUsage, StreamEvent, StreamEventType


def classify_http_error(status_code: int) -> tuple[ProviderErrorKind, bool]:
    if status_code == 401:
        return ProviderErrorKind.AUTHENTICATION, False
    if status_code == 403:
        return ProviderErrorKind.AUTHORIZATION, False
    if status_code == 408:
        return ProviderErrorKind.TIMEOUT, True
    if status_code == 429:
        return ProviderErrorKind.RATE_LIMIT, True
    if 400 <= status_code < 500:
        return ProviderErrorKind.INVALID_REQUEST, False
    if status_code >= 500:
        return ProviderErrorKind.SERVER_ERROR, True
    return ProviderErrorKind.UNKNOWN, False


class HTTPXProviderAdapter(ProviderAdapter):
    def __init__(
        self,
        *,
        provider_name: str,
        model_name: str,
        endpoint: str,
        api_key: str,
        client: httpx.AsyncClient | None = None,
        timeout_seconds: float = 20.0,
        supports_multimodal: bool = False,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        self.provider_name = provider_name
        self.model_name = model_name
        self.endpoint = endpoint
        self.api_key = api_key
        self._client = client
        self.timeout = httpx.Timeout(timeout_seconds)
        self.supports_multimodal = supports_multimodal

    def _content_payload(self, message: Message) -> str | list[dict[str, Any]]:
        if isinstance(message.content, str):
            return message.content
        if not self.supports_multimodal and any(part.type != "text" for part in message.content):
            raise ProviderError(
                f"{self.provider_name} route does not support multimodal input",
                kind=ProviderErrorKind.INVALID_REQUEST,
                provider=self.provider_name,
                retryable=False,
            )
        return [part.model_dump(exclude_none=True) for part in message.content]

    def _messages_payload(self, messages: list[Message]) -> list[dict[str, Any]]:
        payload: list[dict[str, Any]] = []
        for message in messages:
            payload.append({"role": message.role, "content": self._content_payload(message)})
        return payload

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _payload(self, request: GatewayRequest) -> dict[str, Any]:
        return {
            "model": self.model_name,
            "messages": self._messages_payload(request.messages),
            "max_output_tokens": request.max_output_tokens,
            "response_format": {
                "type": "json_schema",
                "name": request.response_schema,
                "schema": DraftResponse.model_json_schema(),
            },
            "metadata": {
                "request_id": request.request_id,
                "tenant_id": request.tenant_id,
                "feature": request.feature,
            },
        }

    async def complete(self, request: GatewayRequest) -> ProviderResponse:
        owns_client = self._client is None
        client = self._client or httpx.AsyncClient(timeout=self.timeout)
        try:
            response = await client.post(self.endpoint, headers=self._headers(), json=self._payload(request))
            if response.status_code >= 400:
                kind, retryable = classify_http_error(response.status_code)
                raise ProviderError(
                    f"{self.provider_name} returned HTTP {response.status_code}",
                    kind=kind,
                    provider=self.provider_name,
                    retryable=retryable,
                    status_code=response.status_code,
                )
            data = response.json()
        except httpx.TimeoutException as exc:
            raise ProviderError(
                f"{self.provider_name} timed out",
                kind=ProviderErrorKind.TIMEOUT,
                provider=self.provider_name,
                retryable=True,
            ) from exc
        finally:
            if owns_client:
                await client.aclose()

        usage_data = data.get("usage", {})
        input_tokens = int(usage_data.get("input_tokens", usage_data.get("prompt_tokens", 0)) or 0)
        output_tokens = int(usage_data.get("output_tokens", usage_data.get("completion_tokens", 0)) or 0)
        text = str(data.get("output_text") or data.get("text") or "")
        return ProviderResponse(
            provider=self.provider_name,
            model=str(data.get("model") or self.model_name),
            text=text,
            usage=ProviderUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
            ),
            provider_request_id=str(data.get("id") or data.get("request_id") or ""),
            finish_reason=data.get("finish_reason"),
            raw_metadata={"status_code": response.status_code},
        )

    async def stream(self, request: GatewayRequest) -> AsyncIterator[StreamEvent]:
        response = await self.complete(request)
        yield StreamEvent(
            event=StreamEventType.START,
            request_id=request.request_id,
            provider=self.provider_name,
            model=response.model,
        )
        yield StreamEvent(
            event=StreamEventType.DELTA,
            request_id=request.request_id,
            text_delta=response.text,
            provider=self.provider_name,
            model=response.model,
        )
        yield StreamEvent(
            event=StreamEventType.DONE,
            request_id=request.request_id,
            provider=self.provider_name,
            model=response.model,
            usage=response.usage,
        )
```

### Tests

```python
# tests/test_provider_adapter.py
from __future__ import annotations

import json

import httpx
import pytest

from model_gateway.providers.fake import FakeProviderAdapter
from model_gateway.providers.httpx_provider import HTTPXProviderAdapter
from model_gateway.schemas import GatewayRequest, Message, MessagePart


def make_request() -> GatewayRequest:
    return GatewayRequest(
        request_id="r1",
        tenant_id="tenant-a",
        user_id="user-a",
        feature="support_draft",
        messages=[Message(role="user", content="Customer asks for a refund without evidence.")],
        idempotency_key="tenant-a:r1",
    )


@pytest.mark.asyncio
async def test_fake_provider_returns_normalized_response() -> None:
    provider = FakeProviderAdapter()
    response = await provider.complete(make_request())
    assert response.provider == "fake-primary"
    assert response.usage.total_tokens > 0


@pytest.mark.asyncio
async def test_httpx_provider_normalizes_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        assert payload["response_format"]["type"] == "json_schema"
        assert payload["response_format"]["name"] == "draft_response"
        return httpx.Response(
            200,
            json={
                "id": "provider-123",
                "model": "test-model",
                "output_text": '{"category":"refund","urgency":"medium","draft":"Verify policy.","needs_human_review":true}',
                "usage": {"input_tokens": 10, "output_tokens": 20},
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = HTTPXProviderAdapter(
        provider_name="mock-http",
        model_name="test-model",
        endpoint="https://provider.example.test/responses",
        api_key="test-key",
        client=client,
    )
    response = await provider.complete(make_request())
    await client.aclose()

    assert response.provider_request_id == "provider-123"
    assert response.usage.total_tokens == 30


@pytest.mark.asyncio
async def test_httpx_provider_serializes_multimodal_parts_when_supported() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        content = payload["messages"][0]["content"]
        assert content[1]["type"] == "image"
        assert content[1]["media_url"] == "https://example.test/screenshot.png"
        return httpx.Response(
            200,
            json={
                "id": "provider-456",
                "model": "test-model",
                "output_text": '{"category":"technical","urgency":"low","draft":"Screenshot noted.","needs_human_review":true}',
                "usage": {"input_tokens": 12, "output_tokens": 8},
            },
        )

    request = GatewayRequest(
        request_id="r2",
        tenant_id="tenant-a",
        user_id="user-a",
        feature="support_draft",
        messages=[
            Message(
                role="user",
                content=[
                    MessagePart(type="text", text="Inspect this screenshot."),
                    MessagePart(type="image", media_url="https://example.test/screenshot.png", mime_type="image/png"),
                ],
            )
        ],
    )
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = HTTPXProviderAdapter(
        provider_name="mock-http",
        model_name="test-model",
        endpoint="https://provider.example.test/responses",
        api_key="test-key",
        client=client,
        supports_multimodal=True,
    )
    response = await provider.complete(request)
    await client.aclose()

    assert response.provider_request_id == "provider-456"
```

### Experiment

Input: same support-draft request.

Settings: fake adapter and mocked HTTPX adapter.

Metric: both return `ProviderResponse` with provider, model, text, usage, and provider request ID.

Expected evidence: product code can switch adapters without changing request schema.

Failure signal: business code imports provider SDKs or parses raw provider JSON.

### Verify

```bash
pytest tests/test_provider_adapter.py
```

### Module completion checkpoint

At this point, your project should:

- contain provider base, fake, and HTTPX adapter files;
- normalize provider response shapes;
- keep provider-specific details inside adapter code;
- pass adapter tests without real API credentials.

### Failure drill

Failure: a provider returns HTTP 429.

Evidence: adapter raises `ProviderError(kind=RATE_LIMIT, retryable=True)`.

Fix: route through the gateway reliability policy that applies retries, circuit checks, and fallback.

Prevention: contract tests for every adapter error class.

### Common misconception

Misconception: "Native SDKs make provider abstraction unnecessary."

Why it seems plausible: SDKs hide raw HTTP details.

Correct model: SDKs simplify one provider; they do not define your product's reliability, validation, fallback, cost, or tracing contract.

### Guided practice and independent transfer

- Guided: Add a provider metadata field to `ProviderResponse` without changing `GatewayRequest`.
- Independent transfer: Sketch how an Anthropic-style or OpenAI-style native SDK adapter would map into the same `ProviderResponse`.

### Recall

- What belongs inside an adapter?
- Why is a fake adapter valuable?
- What should happen if a provider changes its response field names?
- Why is HTTPX useful even if native SDKs exist?

## Hybrid module 3: Routing and fallback

### Core question

How do you choose a provider and recover from provider failure without hiding risk?

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Routing | Routing chooses which approved provider/model handles a request. It enforces tenant, feature, policy, and availability rules. | Northstar's support drafts use `provider-a` unless it is unhealthy. |
| Fallback | Fallback tries another approved provider after an allowed failure. It improves availability but can change behavior, cost, and policy exposure. | If Provider A times out, Provider B may generate the draft. |
| Retry safety | Retry safety asks whether repeating the request can duplicate side effects. It controls when fallback is allowed. | Retrying a pure draft is safer than retrying a tool call that refunds money. |
| Provider policy | Provider policy defines which provider/model is allowed for a tenant, data type, and feature. | Sensitive enterprise data may be restricted to an approved region/provider. |
| Validation gate | A validation gate checks the fallback output against the same schema and business rules as the primary output. | Provider B's output still must pass `DraftResponse`. |
| Fallback observability | Fallback observability records that a secondary path was used. It is required for debugging, cost analysis, and incident review. | A trace shows `provider-a timeout -> provider-b success`. |

### Connected dry run

Follow one support draft request when the primary provider fails.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | The gateway receives a request with tenant and feature metadata. | Routing context |
| 2 | Policy selects the first approved provider. | Provider policy, routing |
| 3 | The primary provider fails before a usable response. | Provider error |
| 4 | The gateway checks whether fallback is allowed. | Retry safety, idempotency |
| 5 | A secondary provider is selected. | Fallback |
| 6 | The fallback response is validated exactly like the primary response. | Validation gate |
| 7 | Usage and traces record the fallback path. | Fallback observability |

Step 1: the gateway receives routing context.

The request includes tenant, feature, risk level, idempotency key, and allowed tools. Routing decisions should use this metadata, not only a hard-coded provider name.

Step 2: policy selects the first approved provider.

For example:

```text
tenant = northstar-demo
feature = support_draft
primary = provider-a
fallback = provider-b
```

This selection is a product and governance decision, not just a load-balancing decision.

Step 3: the primary provider fails.

Provider A times out before returning a response body. This is different from a completed unsafe response or a content-policy rejection.

Step 4: the gateway checks fallback safety.

The gateway asks:

```text
Was the request idempotent?
Was there any external side effect?
Is the failure type allowed for fallback?
Is the fallback provider approved for this tenant/data?
```

If the answer is no, fallback stops.

Step 5: the gateway tries the secondary provider.

Fallback improves availability, but Provider B may have different latency, model behavior, context limits, cost, and data policy. The gateway treats it as a controlled alternate path, not as an invisible equivalent.

Step 6: fallback output passes through the same validation gate.

Provider B's response must still produce valid structured output and respect business policy. Fallback is not allowed to bypass schema validation just because the primary failed.

Step 7: the gateway records what happened.

Usage records and traces should show:

```text
primary_provider = provider-a
primary_error = timeout
fallback_provider = provider-b
final_status = success
```

This makes fallback auditable instead of invisible.

### Concept model

Routing selects the first approved provider. Fallback selects a secondary provider after an allowed failure. Fallback is not a quality guarantee; it is an availability strategy. It must be observable because a fallback response may have different latency, cost, model behavior, region, data policy, or schema reliability.

### Product consequence

For Northstar, fallback is acceptable only if:

- the provider is approved for the tenant and data type;
- the failure is safe to retry or reroute;
- the output still passes the same schema and policy gate;
- usage and traces show fallback occurred.

### Worked example

If Provider A times out before any response body is received, fallback may be safe. If Provider A accepted a tool call that may create an external action, fallback could duplicate the action unless an idempotency key and tool-level safeguards exist.

### Build

```python
# model_gateway/validation.py
from __future__ import annotations

import json

from pydantic import ValidationError

from model_gateway.errors import StructuredOutputError
from model_gateway.schemas import DraftResponse, ProviderResponse


def extract_json_object(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        return stripped
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start >= 0 and end > start:
        return stripped[start : end + 1]
    raise StructuredOutputError("provider output did not contain a JSON object")


def validate_draft_response(response: ProviderResponse) -> DraftResponse:
    try:
        data = json.loads(extract_json_object(response.text))
        draft = DraftResponse.model_validate(data)
    except (json.JSONDecodeError, ValidationError, StructuredOutputError) as exc:
        raise StructuredOutputError(f"invalid draft response from {response.provider}") from exc

    if draft.unsupported_claims:
        raise StructuredOutputError("draft contains unsupported claims")
    if not draft.needs_human_review:
        raise StructuredOutputError("support drafts must require human review")
    return draft
```

```python
# model_gateway/reliability.py
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from enum import Enum
from time import monotonic
from typing import Awaitable, Callable, TypeVar

from model_gateway.errors import CircuitOpenError, ProviderError

T = TypeVar("T")


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay_seconds: float = 0.05
    max_delay_seconds: float = 1.0

    def delay_for_attempt(self, attempt: int) -> float:
        return min(self.max_delay_seconds, self.base_delay_seconds * (2 ** max(0, attempt - 1)))


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class InMemoryCircuitBreaker:
    def __init__(self, *, failure_threshold: int = 3, reset_after_seconds: float = 30.0) -> None:
        self.failure_threshold = failure_threshold
        self.reset_after_seconds = reset_after_seconds
        self.failures: dict[str, int] = {}
        self.opened_at: dict[str, float] = {}

    def state(self, provider: str) -> CircuitState:
        opened = self.opened_at.get(provider)
        if opened is None:
            return CircuitState.CLOSED
        if monotonic() - opened >= self.reset_after_seconds:
            return CircuitState.HALF_OPEN
        return CircuitState.OPEN

    def before_call(self, provider: str) -> None:
        if self.state(provider) == CircuitState.OPEN:
            raise CircuitOpenError(f"circuit open for {provider}")

    def record_success(self, provider: str) -> None:
        self.failures.pop(provider, None)
        self.opened_at.pop(provider, None)

    def record_failure(self, provider: str) -> None:
        count = self.failures.get(provider, 0) + 1
        self.failures[provider] = count
        if count >= self.failure_threshold:
            self.opened_at[provider] = monotonic()


async def call_with_retries(
    operation: Callable[[], Awaitable[T]],
    *,
    retry_policy: RetryPolicy,
    retry_safe: bool,
) -> T:
    last_error: ProviderError | None = None
    for attempt in range(1, retry_policy.max_attempts + 1):
        try:
            return await operation()
        except ProviderError as exc:
            last_error = exc
            if not retry_safe or not exc.retryable or attempt >= retry_policy.max_attempts:
                raise
            await asyncio.sleep(retry_policy.delay_for_attempt(attempt))
    assert last_error is not None
    raise last_error
```

Create the usage ledger now so Module 3 can run immediately. Module 7 returns to this file to explain Redis persistence and configurable cost tracking in more depth.

```python
# model_gateway/usage.py
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime

from pydantic import BaseModel, Field

from model_gateway.schemas import GatewayRequest, GatewayResponse


class TokenPrice(BaseModel):
    input_per_1m_tokens_usd: float = Field(ge=0)
    output_per_1m_tokens_usd: float = Field(ge=0)
    verified_on: str = "example-not-provider-pricing"


class PriceTable:
    def __init__(self, prices: dict[tuple[str, str], TokenPrice] | None = None) -> None:
        self.prices = prices or {}

    def estimate(self, *, provider: str, model: str, input_tokens: int, output_tokens: int) -> float:
        price = self.prices.get((provider, model))
        if price is None:
            return 0.0
        input_cost = (input_tokens / 1_000_000) * price.input_per_1m_tokens_usd
        output_cost = (output_tokens / 1_000_000) * price.output_per_1m_tokens_usd
        return round(input_cost + output_cost, 8)


class UsageRecord(BaseModel):
    request_id: str
    tenant_id: str
    user_id: str
    feature: str
    provider: str
    model: str
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    total_tokens: int = Field(ge=0)
    estimated_cost_usd: float = Field(ge=0)
    fallback_used: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UsageLedger(ABC):
    @abstractmethod
    async def record(self, request: GatewayRequest, response: GatewayResponse) -> None:
        raise NotImplementedError


class InMemoryUsageLedger(UsageLedger):
    def __init__(self, price_table: PriceTable | None = None) -> None:
        self.records: list[UsageRecord] = []
        self.price_table = price_table or PriceTable()

    async def record(self, request: GatewayRequest, response: GatewayResponse) -> None:
        estimated_cost = response.usage.estimated_cost_usd or self.price_table.estimate(
            provider=response.provider,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )
        self.records.append(
            UsageRecord(
                request_id=request.request_id,
                tenant_id=request.tenant_id,
                user_id=request.user_id,
                feature=request.feature,
                provider=response.provider,
                model=response.model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                total_tokens=response.usage.total_tokens,
                estimated_cost_usd=estimated_cost,
                fallback_used=response.fallback_used,
            )
        )
```

```python
# model_gateway/gateway.py
from __future__ import annotations

from collections.abc import AsyncIterator, Iterable

from model_gateway.errors import CircuitOpenError, ProviderError, ProviderErrorKind
from model_gateway.providers.base import ProviderAdapter
from model_gateway.reliability import InMemoryCircuitBreaker, RetryPolicy, call_with_retries
from model_gateway.schemas import GatewayRequest, GatewayResponse, StreamEvent, StreamEventType
from model_gateway.usage import UsageLedger
from model_gateway.validation import validate_draft_response


class GatewayService:
    def __init__(
        self,
        providers: Iterable[ProviderAdapter],
        *,
        usage_ledger: UsageLedger,
        fallback_order: list[str] | None = None,
        retry_policy: RetryPolicy | None = None,
        circuit_breaker: InMemoryCircuitBreaker | None = None,
    ) -> None:
        self.providers = {provider.provider_name: provider for provider in providers}
        self.usage_ledger = usage_ledger
        self.fallback_order = fallback_order or list(self.providers)
        self.retry_policy = retry_policy or RetryPolicy()
        self.circuit_breaker = circuit_breaker or InMemoryCircuitBreaker()

    def _route_order(self, request: GatewayRequest) -> list[str]:
        if request.requested_provider:
            ordered = [request.requested_provider]
            ordered.extend(name for name in self.fallback_order if name != request.requested_provider)
            return ordered
        return list(self.fallback_order)

    async def complete(self, request: GatewayRequest) -> GatewayResponse:
        errors: list[ProviderError] = []
        for index, provider_name in enumerate(self._route_order(request)):
            provider = self.providers.get(provider_name)
            if provider is None:
                continue
            try:
                self.circuit_breaker.before_call(provider_name)
                provider_response = await call_with_retries(
                    lambda: provider.complete(request),
                    retry_policy=self.retry_policy,
                    retry_safe=request.retry_safe,
                )
                self.circuit_breaker.record_success(provider_name)
                validated = validate_draft_response(provider_response)
                gateway_response = GatewayResponse(
                    request_id=request.request_id,
                    tenant_id=request.tenant_id,
                    user_id=request.user_id,
                    feature=request.feature,
                    provider=provider_response.provider,
                    model=provider_response.model,
                    validated=validated,
                    usage=provider_response.usage,
                    fallback_used=index > 0,
                    provider_request_id=provider_response.provider_request_id,
                )
                await self.usage_ledger.record(request, gateway_response)
                return gateway_response
            except CircuitOpenError:
                continue
            except ProviderError as exc:
                errors.append(exc)
                self.circuit_breaker.record_failure(provider_name)
                if not exc.retryable:
                    break
                continue
        if errors:
            raise errors[-1]
        raise ProviderError(
            "no provider route available",
            kind=ProviderErrorKind.INVALID_REQUEST,
            provider="gateway",
            retryable=False,
        )

    async def stream(self, request: GatewayRequest) -> AsyncIterator[StreamEvent]:
        for provider_name in self._route_order(request):
            provider = self.providers.get(provider_name)
            if provider is None:
                continue
            try:
                self.circuit_breaker.before_call(provider_name)
                async for event in provider.stream(request):
                    yield event
                self.circuit_breaker.record_success(provider_name)
                return
            except CircuitOpenError:
                continue
            except ProviderError as exc:
                self.circuit_breaker.record_failure(provider_name)
                yield StreamEvent(
                    event=StreamEventType.ERROR,
                    request_id=request.request_id,
                    error_type=exc.kind.value,
                    provider=provider_name,
                )
                return
        yield StreamEvent(
            event=StreamEventType.ERROR,
            request_id=request.request_id,
            error_type="no_provider_route_available",
        )
```

### Tests

```python
# tests/test_gateway.py
from __future__ import annotations

import pytest

from model_gateway.errors import ProviderErrorKind
from model_gateway.gateway import GatewayService
from model_gateway.providers.fake import FakeProviderAdapter
from model_gateway.reliability import InMemoryCircuitBreaker, RetryPolicy
from model_gateway.schemas import GatewayRequest, Message
from model_gateway.usage import InMemoryUsageLedger


def make_request() -> GatewayRequest:
    return GatewayRequest(
        request_id="r1",
        tenant_id="tenant-a",
        user_id="user-a",
        feature="support_draft",
        messages=[Message(role="user", content="Refund request with missing evidence.")],
        idempotency_key="tenant-a:r1",
    )


@pytest.mark.asyncio
async def test_gateway_falls_back_after_retryable_provider_failure() -> None:
    primary = FakeProviderAdapter("primary", fail_with=ProviderErrorKind.RATE_LIMIT)
    fallback = FakeProviderAdapter("fallback")
    ledger = InMemoryUsageLedger()
    gateway = GatewayService([primary, fallback], usage_ledger=ledger, fallback_order=["primary", "fallback"])

    response = await gateway.complete(make_request())

    assert response.provider == "fallback"
    assert response.fallback_used is True
    assert len(ledger.records) == 1


@pytest.mark.asyncio
async def test_gateway_opens_circuit_and_skips_failed_provider() -> None:
    primary = FakeProviderAdapter("primary", fail_with=ProviderErrorKind.RATE_LIMIT)
    fallback = FakeProviderAdapter("fallback")
    breaker = InMemoryCircuitBreaker(failure_threshold=1)
    gateway = GatewayService(
        [primary, fallback],
        usage_ledger=InMemoryUsageLedger(),
        fallback_order=["primary", "fallback"],
        retry_policy=RetryPolicy(max_attempts=1, base_delay_seconds=0),
        circuit_breaker=breaker,
    )

    first = await gateway.complete(make_request())
    second = await gateway.complete(make_request())

    assert first.provider == "fallback"
    assert second.provider == "fallback"
    assert breaker.state("primary").value == "open"


@pytest.mark.asyncio
async def test_gateway_rejects_malformed_provider_output() -> None:
    provider = FakeProviderAdapter("primary", malformed=True)
    gateway = GatewayService([provider], usage_ledger=InMemoryUsageLedger())

    with pytest.raises(Exception):
        await gateway.complete(make_request())
```

### Experiment

Input: same support-draft request.

Settings: primary fails with rate limit, fallback succeeds.

Metric: fallback flag and usage ledger record.

Expected evidence: fallback is visible in response and usage record.

Failure signal: downstream code receives fallback output without knowing fallback occurred.

### Verify

```bash
pytest tests/test_gateway.py
```

### Module completion checkpoint

At this point, your project should:

- route through approved adapters;
- apply bounded retry policy before fallback;
- skip providers with open circuits;
- fallback only after retryable provider failures;
- validate output after fallback;
- record usage after successful validated completion.

### Failure drill

Failure: fallback silently changes model behavior.

Evidence: traces show a different provider/model, but product metrics were aggregated without provider dimension.

Fix: include provider/model/fallback fields in usage and evaluation.

Prevention: make fallback observable in response, logs, traces, and reports.

### Common misconception

Misconception: "Fallback always improves reliability."

Why it seems plausible: another provider can respond when the first one fails.

Correct model: fallback improves availability only when the fallback provider is approved, compatible, safe, and observable. It can harm quality, cost, privacy, or latency.

### Guided practice and independent transfer

- Guided: Add a route order where `requested_provider="fallback"` starts with fallback.
- Independent transfer: Design a policy where high-risk tenant data cannot fall back to providers outside an approved region.

### Recall

- Why must fallback be observable?
- Which provider failures should stop fallback?
- Why does fallback still need schema validation?
- What extra dimensions should usage records include?

## Hybrid module 4: Structured output and tool/function calling

### Core question

How do you prevent malformed structured output and unsafe tool calls from reaching business logic?

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Structured output | Structured output is model output expected to match a schema. It is not safe until validated by application code. | The model returns JSON with `category`, `draft`, and `needs_human_review`. |
| Schema validation | Schema validation checks that fields, types, enums, and required values match the contract. | `needs_human_review` must be a boolean, not `"maybe"`. |
| Business validation | Business validation checks domain rules beyond syntax. | A draft that says "refund approved" is rejected if evidence is missing. |
| Tool/function calling | Tool/function calling means the model proposes an action and arguments; the application decides whether to execute it. | The model proposes `lookup_order_status({"order_id":"A-1049"})`. |
| Tool allowlist | A tool allowlist restricts which tools are available in this request. | Support drafts may call `lookup_order_status` but not `issue_refund`. |
| Argument validation | Argument validation checks tool arguments before execution. | `order_id` must match `A-1049`, not arbitrary text. |
| Authorization check | Authorization verifies the current user/tenant may use the tool on the requested resource. | Agent 42 may view Northstar order status but not another tenant's orders. |

### Connected dry run

Trace a model output that is valid JSON but still unsafe.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | The provider returns text that appears to be JSON. | Structured output |
| 2 | The gateway extracts and parses the JSON object. | JSON parsing |
| 3 | The gateway validates field names, types, and enums. | Schema validation |
| 4 | The gateway applies business policy. | Business validation |
| 5 | The model proposes a tool call. | Tool/function calling |
| 6 | The application checks allowed tools and argument shape. | Tool allowlist, argument validation |
| 7 | The application checks identity and tenant permission. | Authorization check |
| 8 | Only safe validated output reaches business logic. | Validation gate |

Step 1: the provider returns JSON-looking text.

The model returns:

```json
{"category":"refund","draft":"Your refund is approved.","needs_human_review":false}
```

This looks structured, but it is only model text until the application validates it.

Step 2: the gateway parses the JSON.

If the text has extra prose, missing braces, or invalid JSON, parsing fails before schema validation even begins.

Step 3: schema validation checks the contract.

The gateway checks that required fields exist and have correct types. If `needs_human_review` is a string instead of a boolean, the response is rejected.

Step 4: business validation checks meaning.

Even if the JSON is syntactically valid, "Your refund is approved" may violate policy if evidence is missing. Business validation rejects the draft because schema validity is not the same as business safety.

Step 5: the model proposes a tool call.

The model may propose:

```text
lookup_order_status(order_id="A-1049")
```

The model proposes the call; it does not get authority to execute it.

Step 6: the application checks the allowlist and arguments.

If `lookup_order_status` is allowed and `order_id` matches the schema, the request can proceed to authorization. If the model proposes `issue_refund`, the gateway blocks it if that tool is not allowed.

Step 7: the application checks authorization.

The current tenant and user must be allowed to access that order. This decision belongs to application security policy, not the LLM.

Step 8: only safe validated output reaches business logic.

The business service receives either validated output or a controlled error. It never receives raw provider text as truth.

### Concept model

Structured output is not trustworthy because a provider says "JSON." It is trustworthy only after your application validates it against a schema and business policy. Tool/function calling means the model proposes a tool name and arguments; the application decides whether that tool exists, whether the arguments are valid, and whether the current identity has permission.

### Product consequence

For support workflows, invalid structured output can misclassify tickets, hide missing information, or draft unsafe commitments. Unsafe tool calls can leak data or trigger actions under the wrong user identity.

### Worked example

Model output:

```json
{
  "category": "refund",
  "urgency": "medium",
  "draft": "Your refund is approved.",
  "needs_human_review": false,
  "unsupported_claims": ["refund approved without evidence"]
}
```

This is syntactically valid JSON but still rejected because it violates business policy.

### Build

```python
# model_gateway/tools.py
from __future__ import annotations

from typing import Any, Callable

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from model_gateway.errors import ToolPolicyError
from model_gateway.schemas import ToolCall


class LookupOrderStatusArgs(BaseModel):
    order_id: str = Field(pattern=r"^[A-Z]-\d{4,}$")


class ToolSpec(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    description: str
    args_model: type[BaseModel]
    executor: Callable[[BaseModel], dict[str, Any]] | None = None
    read_only: bool = True


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, tool: ToolSpec) -> None:
        self._tools[tool.name] = tool

    def validate_call(self, call: ToolCall, *, allowed_tools: list[str]) -> BaseModel:
        if call.name not in allowed_tools:
            raise ToolPolicyError(f"tool {call.name!r} is not allowed for this request")
        tool = self._tools.get(call.name)
        if tool is None:
            raise ToolPolicyError(f"tool {call.name!r} is not registered")
        if not tool.read_only:
            raise ToolPolicyError(f"tool {call.name!r} is not read-only")
        try:
            return tool.args_model.model_validate(call.arguments)
        except ValidationError as exc:
            raise ToolPolicyError(f"invalid arguments for tool {call.name!r}") from exc

    def execute_call(self, call: ToolCall, *, allowed_tools: list[str]) -> dict[str, Any]:
        args = self.validate_call(call, allowed_tools=allowed_tools)
        tool = self._tools[call.name]
        if tool.executor is None:
            raise ToolPolicyError(f"tool {call.name!r} has no executor")
        return tool.executor(args)


def lookup_order_status(args: BaseModel) -> dict[str, Any]:
    typed = LookupOrderStatusArgs.model_validate(args.model_dump())
    return {
        "order_id": typed.order_id,
        "status": "requires_agent_verification",
        "source": "synthetic_order_store",
    }


def default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        ToolSpec(
            name="lookup_order_status",
            description="Read-only lookup of order status for support drafting.",
            args_model=LookupOrderStatusArgs,
            executor=lookup_order_status,
            read_only=True,
        )
    )
    return registry
```

### Tests

```python
# tests/test_validation.py
from __future__ import annotations

import pytest

from model_gateway.errors import StructuredOutputError
from model_gateway.schemas import ProviderResponse
from model_gateway.validation import validate_draft_response


def test_valid_structured_output_passes() -> None:
    response = ProviderResponse(
        provider="fake",
        model="fake",
        text='{"category":"refund","urgency":"medium","draft":"Please verify policy first.","needs_human_review":true}',
    )
    assert validate_draft_response(response).category == "refund"


def test_unsupported_claim_is_rejected() -> None:
    response = ProviderResponse(
        provider="fake",
        model="fake",
        text=(
            '{"category":"refund","urgency":"medium","draft":"Approved.",'
            '"needs_human_review":false,"unsupported_claims":["approved without evidence"]}'
        ),
    )
    with pytest.raises(StructuredOutputError):
        validate_draft_response(response)
```

```python
# tests/test_tools.py
from __future__ import annotations

import pytest

from model_gateway.errors import ToolPolicyError
from model_gateway.schemas import ToolCall
from model_gateway.tools import default_tool_registry


def test_allowed_read_only_tool_call_passes() -> None:
    registry = default_tool_registry()
    args = registry.validate_call(
        ToolCall(name="lookup_order_status", arguments={"order_id": "A-1049"}),
        allowed_tools=["lookup_order_status"],
    )
    assert args.order_id == "A-1049"


def test_allowed_read_only_tool_can_execute() -> None:
    registry = default_tool_registry()
    result = registry.execute_call(
        ToolCall(name="lookup_order_status", arguments={"order_id": "A-1049"}),
        allowed_tools=["lookup_order_status"],
    )
    assert result["status"] == "requires_agent_verification"
    assert result["source"] == "synthetic_order_store"


def test_unknown_tool_is_rejected() -> None:
    registry = default_tool_registry()
    with pytest.raises(ToolPolicyError):
        registry.validate_call(
            ToolCall(name="issue_refund", arguments={"order_id": "A-1049"}),
            allowed_tools=["issue_refund"],
        )


def test_invalid_tool_arguments_are_rejected() -> None:
    registry = default_tool_registry()
    with pytest.raises(ToolPolicyError):
        registry.validate_call(
            ToolCall(name="lookup_order_status", arguments={"order_id": "../../../etc/passwd"}),
            allowed_tools=["lookup_order_status"],
        )
```

### Experiment

Input: provider output with valid JSON but unsafe business content.

Settings: same gateway, same schema.

Metric: rejection before business logic.

Expected evidence: `StructuredOutputError`.

Failure signal: downstream code receives a refund approval without evidence.

### Verify

```bash
pytest tests/test_validation.py tests/test_tools.py
```

### Module completion checkpoint

At this point, your project should:

- validate provider JSON against `DraftResponse`;
- reject syntactically valid but unsafe output;
- allow only registered read-only tools;
- validate tool arguments before execution.

### Failure drill

Failure: model proposes `issue_refund`.

Evidence: tool call name is not registered or not read-only.

Fix: reject and return a controlled error; do not execute.

Prevention: tool registry allowlist and permission checks outside the model.

### Common misconception

Misconception: "Tool calling means the model executes tools."

Why it seems plausible: provider APIs label the model's output as a tool call.

Correct model: the model proposes a structured request. Your application validates and executes or rejects it under real identity and permissions.

### Guided practice and independent transfer

- Guided: Add `lookup_policy` as another read-only tool with a strict `policy_id`.
- Independent transfer: Define why a write tool such as `issue_refund` requires human approval and idempotency.

### Recall

- Why can valid JSON still be unsafe?
- What checks happen before executing a tool call?
- Why should authorization not be delegated to the model?
- What is the difference between schema validity and business validity?

## Hybrid module 5: Streaming and multimodal requests

### Core question

How do you expose streaming and multimodal requests without confusing partial output with final validated output?

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Streaming | Streaming emits model output as events over time. It improves perceived latency but creates partial, unvalidated states. | The UI receives `"Draft"` before the full draft is complete. |
| Stream event | A stream event is one message in the stream lifecycle. It can be a text delta, error, tool request, or done signal. | `delta: "I can help"` arrives before `done`. |
| Delta | A delta is a partial output chunk. It should not be treated as a final answer. | `"Your refund"` appears before the model later says `"requires review"`. |
| Finalization | Finalization happens when the stream ends and the full output can be validated. | Only after `DONE` does the gateway validate the complete draft. |
| Multimodal request | A multimodal request includes text plus image, audio, or document parts. It increases provider, privacy, and validation complexity. | A support ticket includes a screenshot of a billing page. |
| Modality metadata | Modality metadata records file type, source, size, and policy decisions. It is needed for audit and safety. | A document part records `type=document`, `mime=application/pdf`, and source. |

### Connected dry run

Trace a streaming support draft that includes a screenshot reference.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | The request includes text and an optional non-text part. | Multimodal request, modality metadata |
| 2 | The provider begins returning events. | Streaming, stream event |
| 3 | The UI receives partial text chunks. | Delta |
| 4 | Partial chunks are marked provisional. | Partial output boundary |
| 5 | The stream finishes or errors. | Finalization, stream lifecycle |
| 6 | The gateway validates the complete output. | Structured output validation |
| 7 | Only validated output becomes ready for agent review. | Final response boundary |

Step 1: the request includes text and optional non-text content.

The ticket may include:

```text
text: "I was charged twice."
image: billing_screenshot.png
```

The gateway records modality metadata before sending anything to a provider. This matters because not every provider, region, or model is approved for every modality.

Step 2: the provider starts returning stream events.

Instead of waiting for the full response, the provider may emit events over time:

```text
START
DELTA "I can"
DELTA " help review"
DONE
```

Each event is useful for user experience but not yet a validated business answer.

Step 3: the UI receives deltas.

The user might see partial text appear quickly. This reduces perceived latency, but a partial sentence can be misleading.

Step 4: partial chunks are marked provisional.

The UI should show streaming text as draft/provisional. It should not enable "send to customer" while the stream is incomplete.

Step 5: the stream finishes or errors.

If the stream errors, the gateway returns a controlled error. If the stream reaches `DONE`, the gateway can assemble the full text.

Step 6: the gateway validates the complete output.

Only the complete output can be checked against the response schema and business rules. A valid-looking early delta is not enough.

Step 7: validated output becomes ready for review.

After validation, the UI can mark the draft as ready for agent review. It is still not automatically sent to the customer.

### Concept model

Streaming returns events over time. A stream can begin, emit deltas, request a tool, fail, or finish. Multimodal requests include text plus image, audio, or document parts. Both features increase product complexity because intermediate events may not be valid final output.

### Product consequence

Streaming is useful for user experience, but Northstar must not show unreviewed claims as final decisions. Multimodal input is useful for screenshots or documents, but provider capability, data policy, file handling, and content safety must be checked before enabling it.

### Worked example

Safe streaming UI pattern:

```text
show "drafting..."
show partial text as provisional
on DONE -> validate full response
only then mark "ready for agent review"
```

Unsafe pattern:

```text
stream partial model text directly into approved customer reply
```

### Build

The fake adapter already implements `stream`. Add a stream collector helper for tests and callers.

```python
# model_gateway/streaming.py
from __future__ import annotations

from collections.abc import AsyncIterator

from model_gateway.schemas import StreamEvent, StreamEventType


async def collect_text(stream: AsyncIterator[StreamEvent]) -> str:
    chunks: list[str] = []
    async for event in stream:
        if event.event == StreamEventType.ERROR:
            raise RuntimeError(event.error_type or "stream failed")
        if event.event == StreamEventType.DELTA:
            chunks.append(event.text_delta)
    return "".join(chunks)
```

### Tests

```python
# tests/test_streaming.py
from __future__ import annotations

import pytest

from model_gateway.providers.fake import FakeProviderAdapter
from model_gateway.schemas import GatewayRequest, Message, MessagePart, StreamEventType
from model_gateway.streaming import collect_text


@pytest.mark.asyncio
async def test_fake_stream_emits_start_delta_done() -> None:
    request = GatewayRequest(
        request_id="r1",
        tenant_id="tenant-a",
        user_id="user-a",
        feature="support_draft",
        messages=[Message(role="user", content="Draft a reply.")],
    )
    provider = FakeProviderAdapter()
    events = [event async for event in provider.stream(request)]
    assert events[0].event == StreamEventType.START
    assert events[-1].event == StreamEventType.DONE
    assert any(event.event == StreamEventType.DELTA for event in events)


@pytest.mark.asyncio
async def test_collect_text_collects_stream_delta() -> None:
    request = GatewayRequest(
        request_id="r1",
        tenant_id="tenant-a",
        user_id="user-a",
        feature="support_draft",
        messages=[Message(role="user", content="Draft a reply.")],
    )
    provider = FakeProviderAdapter()
    text = await collect_text(provider.stream(request))
    assert "missing_information" in text


def test_multimodal_request_uses_typed_parts() -> None:
    request = GatewayRequest(
        request_id="r2",
        tenant_id="tenant-a",
        user_id="user-a",
        feature="support_draft",
        messages=[
            Message(
                role="user",
                content=[
                    MessagePart(type="text", text="Read this screenshot if provider supports images."),
                    MessagePart(type="image", media_url="https://example.test/screenshot.png", mime_type="image/png"),
                ],
            )
        ],
    )
    assert isinstance(request.messages[0].content, list)
```

### Experiment

Input: streaming support-draft request.

Settings: fake stream adapter.

Metric: event sequence and final collected text.

Expected evidence: stream emits `START`, `DELTA`, and `DONE`.

Failure signal: partial deltas are treated as validated final JSON.

### Verify

```bash
pytest tests/test_streaming.py
```

### Module completion checkpoint

At this point, your project should:

- define stream event types;
- collect provisional stream text safely;
- represent text, image, audio, and document input parts;
- treat provider support for each modality as adapter capability, not as a universal guarantee.

### Failure drill

Failure: stream disconnects mid-response.

Evidence: no `DONE` event and no validated final response.

Fix: mark the attempt failed or partial; do not send downstream business output.

Prevention: terminal stream events, timeout policy, and retry only when safe.

### Common misconception

Misconception: "Streaming is just faster non-streaming."

Why it seems plausible: both produce text.

Correct model: streaming exposes intermediate state. Intermediate text is not necessarily valid JSON, safe, complete, or policy-compliant.

### Guided practice and independent transfer

- Guided: Add a UI state table for `START`, `DELTA`, `ERROR`, and `DONE`.
- Independent transfer: Decide whether an audio-input request should be allowed for a tenant with strict data residency constraints.

### Recall

- Why are stream deltas provisional?
- What must happen before streamed output reaches business logic?
- Why is multimodal support provider-specific?
- What metadata should be recorded for document or image input?

## Hybrid module 6: Errors, timeouts, retries, and circuit breakers

### Core question

Which failures should be retried, which should fail fast, and when should a provider be temporarily removed from routing?

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Timeout | A timeout limits how long the gateway waits. It prevents one provider call from exhausting request workers. | Stop waiting after 20 seconds. |
| Retry | A retry repeats a request after an allowed failure. It can improve reliability but can also multiply cost and side effects. | Retry once after a network timeout. |
| Exponential backoff | Exponential backoff waits longer between retry attempts. It avoids hammering an unhealthy provider. | Wait 0.5s, then 1s, then 2s. |
| Error classification | Error classification turns provider failures into policy decisions. | 429 may retry; authentication failure should fail fast. |
| Circuit breaker | A circuit breaker stops sending traffic to an unhealthy provider temporarily. | After repeated timeouts, route away for 60 seconds. |
| Half-open probe | A half-open probe tests whether a provider has recovered. | Send one cautious request before fully reopening traffic. |
| Idempotency | Idempotency means repeating a logical request should not duplicate side effects. | A retried draft request keeps the same idempotency key. |

### Connected dry run

Follow one provider outage from first timeout to circuit-breaker recovery.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | The gateway sends a provider request with a timeout. | Timeout |
| 2 | The provider does not respond in time. | Provider timeout |
| 3 | The gateway classifies the failure. | Error classification |
| 4 | The gateway decides whether retry is safe. | Retry, idempotency |
| 5 | The retry waits before trying again. | Exponential backoff |
| 6 | Repeated failures open the circuit. | Circuit breaker |
| 7 | A later probe tests recovery. | Half-open probe |
| 8 | Routing either reopens the provider or keeps it isolated. | Recovery policy |

Step 1: the gateway sends a bounded request.

The request includes a timeout. Without a timeout, one provider call can hang long enough to tie up workers and degrade the whole application.

Step 2: the provider times out.

The gateway receives no usable response within the configured limit. This is usually different from a provider saying "your API key is invalid" or "content was blocked."

Step 3: the gateway classifies the error.

The timeout is classified as temporary and potentially retryable. An authentication failure would be non-retryable because repeating the same bad credential does not help.

Step 4: the gateway checks retry safety.

If the request is idempotent and no side effect occurred, retry may be allowed. If the model already triggered a non-idempotent tool action, retry may be unsafe.

Step 5: exponential backoff spaces retry attempts.

The gateway waits briefly before retrying. This protects the provider and the gateway from retry storms.

Step 6: repeated failures open the circuit.

If several calls fail, the circuit breaker temporarily blocks that provider. New requests route elsewhere or fail fast instead of repeatedly hitting a known-bad dependency.

Step 7: a half-open probe tests recovery.

After a cooldown, the gateway sends a limited probe. A success can close the circuit; another failure keeps it open.

Step 8: routing follows recovery policy.

The final routing decision is observable through logs, metrics, and traces. Operators can see whether failures are transient, provider-specific, or caused by the gateway.

### Concept model

Retries are safe only when repeating the request cannot create duplicate side effects and the failure is likely temporary. Timeouts prevent resource exhaustion. Exponential backoff spreads retry load. A circuit breaker stops sending traffic to a provider after repeated failures and later probes it cautiously.

### Product consequence

Retrying every failure can multiply cost, overload providers, duplicate tool actions, and hide incidents. Not retrying safe transient failures creates avoidable user-facing errors. The gateway must classify failures and apply bounded policy.

### Worked example

Safe to retry:

- timeout before response;
- HTTP 429;
- HTTP 500/503;
- connection reset before provider accepted work.

Usually not safe to retry automatically:

- authentication failure;
- malformed request;
- content policy rejection;
- non-idempotent tool execution;
- request without an idempotency key when side effects are possible.

### Build

```python
# model_gateway/reliability.py
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from enum import Enum
from time import monotonic
from typing import Awaitable, Callable, TypeVar

from model_gateway.errors import CircuitOpenError, ProviderError

T = TypeVar("T")


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay_seconds: float = 0.05
    max_delay_seconds: float = 1.0

    def delay_for_attempt(self, attempt: int) -> float:
        return min(self.max_delay_seconds, self.base_delay_seconds * (2 ** max(0, attempt - 1)))


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class InMemoryCircuitBreaker:
    def __init__(self, *, failure_threshold: int = 3, reset_after_seconds: float = 30.0) -> None:
        self.failure_threshold = failure_threshold
        self.reset_after_seconds = reset_after_seconds
        self.failures: dict[str, int] = {}
        self.opened_at: dict[str, float] = {}

    def state(self, provider: str) -> CircuitState:
        opened = self.opened_at.get(provider)
        if opened is None:
            return CircuitState.CLOSED
        if monotonic() - opened >= self.reset_after_seconds:
            return CircuitState.HALF_OPEN
        return CircuitState.OPEN

    def before_call(self, provider: str) -> None:
        if self.state(provider) == CircuitState.OPEN:
            raise CircuitOpenError(f"circuit open for {provider}")

    def record_success(self, provider: str) -> None:
        self.failures.pop(provider, None)
        self.opened_at.pop(provider, None)

    def record_failure(self, provider: str) -> None:
        count = self.failures.get(provider, 0) + 1
        self.failures[provider] = count
        if count >= self.failure_threshold:
            self.opened_at[provider] = monotonic()


async def call_with_retries(
    operation: Callable[[], Awaitable[T]],
    *,
    retry_policy: RetryPolicy,
    retry_safe: bool,
) -> T:
    last_error: ProviderError | None = None
    for attempt in range(1, retry_policy.max_attempts + 1):
        try:
            return await operation()
        except ProviderError as exc:
            last_error = exc
            if not retry_safe or not exc.retryable or attempt >= retry_policy.max_attempts:
                raise
            await asyncio.sleep(retry_policy.delay_for_attempt(attempt))
    assert last_error is not None
    raise last_error
```

### Tests

```python
# tests/test_reliability.py
from __future__ import annotations

import pytest

from model_gateway.errors import CircuitOpenError, ProviderError, ProviderErrorKind
from model_gateway.reliability import InMemoryCircuitBreaker, RetryPolicy, call_with_retries


@pytest.mark.asyncio
async def test_retry_policy_retries_retryable_error() -> None:
    attempts = 0

    async def flaky() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise ProviderError(
                "rate limited",
                kind=ProviderErrorKind.RATE_LIMIT,
                provider="test",
                retryable=True,
            )
        return "ok"

    result = await call_with_retries(flaky, retry_policy=RetryPolicy(max_attempts=3, base_delay_seconds=0), retry_safe=True)
    assert result == "ok"
    assert attempts == 2


@pytest.mark.asyncio
async def test_retry_policy_does_not_retry_unsafe_request() -> None:
    attempts = 0

    async def always_fails() -> str:
        nonlocal attempts
        attempts += 1
        raise ProviderError(
            "timeout",
            kind=ProviderErrorKind.TIMEOUT,
            provider="test",
            retryable=True,
        )

    with pytest.raises(ProviderError):
        await call_with_retries(always_fails, retry_policy=RetryPolicy(max_attempts=3), retry_safe=False)
    assert attempts == 1


def test_circuit_opens_after_threshold() -> None:
    breaker = InMemoryCircuitBreaker(failure_threshold=2)
    breaker.record_failure("provider-a")
    breaker.record_failure("provider-a")
    with pytest.raises(CircuitOpenError):
        breaker.before_call("provider-a")
```

### Experiment

Input: retryable timeout error.

Settings: `max_attempts=3`, retry-safe request.

Metric: attempts count and final result.

Expected evidence: transient error is retried, unsafe request is not.

Failure signal: authentication errors or invalid requests are retried repeatedly.

### Verify

```bash
pytest tests/test_reliability.py
```

### Module completion checkpoint

At this point, your project should:

- classify retryable and non-retryable provider errors;
- use bounded exponential backoff;
- avoid retrying unsafe requests;
- open a circuit after repeated provider failures.

### Failure drill

Failure: duplicate write after retry.

Evidence: the same tool action appears twice with different provider request IDs.

Fix: require idempotency keys for side-effecting requests and do not auto-retry write tools.

Prevention: separate read-only draft generation from write actions; keep customer-impacting writes outside model discretion.

### Common misconception

Misconception: "Retries make systems reliable."

Why it seems plausible: retries often fix transient network failures.

Correct model: retries improve reliability only when bounded, classified, idempotent, observable, and combined with timeouts and circuit breakers.

### Guided practice and independent transfer

- Guided: Add `CONTENT_FILTER` as non-retryable and explain why.
- Independent transfer: Design a retry policy for a streaming request that disconnects after partial output.

### Recall

- When should a request not be retried?
- What does a circuit breaker prevent?
- Why do timeouts matter even when providers are reliable?
- How does idempotency change retry safety?

## Implementation module 7: Usage, cost attribution, tracing, and Redis

### Purpose

The gateway must know who used which provider/model for which feature and what it cost. This is required for customer billing, product economics, abuse detection, capacity planning, and incident response.

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Usage record | A usage record captures who used which model, for what feature, and with how many tokens. | Tenant `northstar-demo` used `provider-a/model-x` for one support draft. |
| Cost attribution | Cost attribution assigns estimated spend to tenant, user, feature, provider, and model. | Support drafts cost more this week because fallback used a pricier model. |
| Price table | A price table stores dated token pricing or internal cost assumptions. It must be versioned because prices change. | `input_per_1m_tokens_usd` is configured with a verified date. |
| Trace | A trace follows one request across gateway components. | One trace links API request, provider call, validation, and usage write. |
| Span | A span is one timed operation inside a trace. | `provider.generate` is a span inside the gateway request trace. |
| Redis ledger | A Redis-backed ledger provides shared usage state across gateway replicas. | Two API containers write usage to the same Redis instance. |

### Connected dry run

Trace one successful support draft from response to cost and observability records.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | The gateway receives a completed validated response. | Gateway response |
| 2 | Token counts and model metadata are extracted. | Usage record |
| 3 | The price table estimates cost. | Price table, cost attribution |
| 4 | The usage ledger stores the event. | In-memory ledger or Redis ledger |
| 5 | A trace links API, provider, validation, and usage write. | Trace, span |
| 6 | Operators query usage by tenant, feature, provider, or model. | Cost attribution, auditability |

Step 1: a validated response is ready.

The gateway has a final `GatewayResponse` with provider, model, token usage, latency, and validation status.

Step 2: usage metadata is extracted.

The gateway records:

```text
tenant_id
user_id
feature
provider
model
input_tokens
output_tokens
```

This turns a model call into an accountable product event.

Step 3: the price table estimates cost.

The gateway uses configured pricing or internal cost assumptions. The lesson does not hard-code real provider prices because they change. The price table must carry a verification date or source.

Step 4: the ledger stores the event.

Local tests use an in-memory ledger. A production-like multi-replica deployment needs shared state such as Redis so all gateway replicas write to the same place.

Step 5: tracing links the operation.

The trace connects the incoming API request, selected provider, validation, and usage write. This lets engineers answer, "Where did time go?" and "Which step failed?"

Step 6: operators query usage.

Product and operations teams can review usage by tenant, feature, provider, and model. This supports billing, abuse detection, incident response, and model migration decisions.

### Design decision

Use an in-memory ledger for local tests and a Redis-backed ledger for shared production-like state. Do not hard-code pricing. The gateway records tokens and a configurable cost estimate; real prices must come from dated provider configuration.

### Build

```python
# model_gateway/usage.py
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from model_gateway.schemas import GatewayRequest, GatewayResponse


class TokenPrice(BaseModel):
    input_per_1m_tokens_usd: float = Field(ge=0)
    output_per_1m_tokens_usd: float = Field(ge=0)
    verified_on: str = "example-not-provider-pricing"


class PriceTable:
    def __init__(self, prices: dict[tuple[str, str], TokenPrice] | None = None) -> None:
        self.prices = prices or {}

    def estimate(self, *, provider: str, model: str, input_tokens: int, output_tokens: int) -> float:
        price = self.prices.get((provider, model))
        if price is None:
            return 0.0
        input_cost = (input_tokens / 1_000_000) * price.input_per_1m_tokens_usd
        output_cost = (output_tokens / 1_000_000) * price.output_per_1m_tokens_usd
        return round(input_cost + output_cost, 8)


class UsageRecord(BaseModel):
    request_id: str
    tenant_id: str
    user_id: str
    feature: str
    provider: str
    model: str
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    total_tokens: int = Field(ge=0)
    estimated_cost_usd: float = Field(ge=0)
    fallback_used: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UsageLedger(ABC):
    @abstractmethod
    async def record(self, request: GatewayRequest, response: GatewayResponse) -> None:
        raise NotImplementedError


class InMemoryUsageLedger(UsageLedger):
    def __init__(self, price_table: PriceTable | None = None) -> None:
        self.records: list[UsageRecord] = []
        self.price_table = price_table or PriceTable()

    async def record(self, request: GatewayRequest, response: GatewayResponse) -> None:
        estimated_cost = response.usage.estimated_cost_usd or self.price_table.estimate(
            provider=response.provider,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )
        self.records.append(
            UsageRecord(
                request_id=request.request_id,
                tenant_id=request.tenant_id,
                user_id=request.user_id,
                feature=request.feature,
                provider=response.provider,
                model=response.model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                total_tokens=response.usage.total_tokens,
                estimated_cost_usd=estimated_cost,
                fallback_used=response.fallback_used,
            )
        )


class RedisUsageLedger(UsageLedger):
    def __init__(
        self,
        redis_client: Any,
        *,
        stream_name: str = "model_gateway_usage",
        price_table: PriceTable | None = None,
    ) -> None:
        self.redis = redis_client
        self.stream_name = stream_name
        self.price_table = price_table or PriceTable()

    async def record(self, request: GatewayRequest, response: GatewayResponse) -> None:
        estimated_cost = response.usage.estimated_cost_usd or self.price_table.estimate(
            provider=response.provider,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )
        record = UsageRecord(
            request_id=request.request_id,
            tenant_id=request.tenant_id,
            user_id=request.user_id,
            feature=request.feature,
            provider=response.provider,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.total_tokens,
            estimated_cost_usd=estimated_cost,
            fallback_used=response.fallback_used,
        )
        await self.redis.xadd(
            self.stream_name,
            {key: str(value) for key, value in record.model_dump(mode="json").items()},
        )
```

```python
# model_gateway/tracing.py
from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator

from opentelemetry import trace


@contextmanager
def gateway_span(name: str, **attributes: object) -> Iterator[None]:
    tracer = trace.get_tracer("model_gateway")
    with tracer.start_as_current_span(name) as span:
        for key, value in attributes.items():
            if value is not None:
                span.set_attribute(key, str(value))
        yield
```

### Unit tests

```python
# tests/test_usage.py
from __future__ import annotations

import pytest

from model_gateway.schemas import DraftResponse, GatewayRequest, GatewayResponse, Message, ProviderUsage
from model_gateway.usage import InMemoryUsageLedger, PriceTable, TokenPrice


@pytest.mark.asyncio
async def test_usage_is_attributed_by_tenant_user_feature() -> None:
    request = GatewayRequest(
        request_id="r1",
        tenant_id="tenant-a",
        user_id="user-a",
        feature="support_draft",
        messages=[Message(role="user", content="Draft.")],
    )
    response = GatewayResponse(
        request_id="r1",
        tenant_id="tenant-a",
        user_id="user-a",
        feature="support_draft",
        provider="fake",
        model="fake-model",
        validated=DraftResponse(category="refund", urgency="medium", draft="Verify first."),
        usage=ProviderUsage(input_tokens=5, output_tokens=7, total_tokens=12),
    )
    ledger = InMemoryUsageLedger()
    await ledger.record(request, response)

    assert ledger.records[0].tenant_id == "tenant-a"
    assert ledger.records[0].user_id == "user-a"
    assert ledger.records[0].total_tokens == 12


@pytest.mark.asyncio
async def test_usage_estimates_cost_from_configurable_price_table() -> None:
    request = GatewayRequest(
        request_id="r-cost",
        tenant_id="tenant-a",
        user_id="user-a",
        feature="support_draft",
        messages=[Message(role="user", content="Draft.")],
    )
    response = GatewayResponse(
        request_id="r-cost",
        tenant_id="tenant-a",
        user_id="user-a",
        feature="support_draft",
        provider="fake",
        model="fake-model",
        validated=DraftResponse(category="refund", urgency="medium", draft="Verify first."),
        usage=ProviderUsage(input_tokens=500_000, output_tokens=250_000, total_tokens=750_000),
    )
    ledger = InMemoryUsageLedger(
        price_table=PriceTable(
            {
                ("fake", "fake-model"): TokenPrice(
                    input_per_1m_tokens_usd=1.0,
                    output_per_1m_tokens_usd=2.0,
                    verified_on="example-for-lesson-only",
                )
            }
        )
    )

    await ledger.record(request, response)

    assert ledger.records[0].estimated_cost_usd == 1.0
```

### Verify in runtime

```bash
pytest tests/test_usage.py
```

### Module completion checkpoint

At this point, your project should:

- record usage by tenant, user, feature, provider, and model;
- estimate cost from a configurable dated price table when a provider supplies token counts;
- support Redis-backed usage records for production-like shared state;
- avoid hard-coded provider pricing;
- expose a trace span helper.

### Failure drill

Failure: cost spike cannot be attributed.

Evidence: provider invoice rose, but usage records only contain aggregate provider totals.

Fix: record tenant, user, feature, provider, model, token counts, and fallback usage.

Prevention: make usage recording part of the gateway success path.

### Production note

Redis is not magic storage. Define retention, stream trimming, backup expectations, access controls, and PII policy. Usage records should carry metadata and counts, not raw ticket text.

### Guided practice and independent transfer

- Guided: Add `trace_id` to usage records.
- Independent transfer: Design a per-tenant spending limit check that happens before provider execution.

### Recall

- Why is cost attribution a product requirement?
- Why should pricing be configurable and dated?
- What data should not be stored in usage records?
- Why is Redis useful when multiple gateway replicas run?

## Implementation module 8: FastAPI gateway, deployment path, and operations

### Purpose

Expose the gateway through a local HTTP API so application teams call one contract instead of provider-specific SDKs.

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| HTTP gateway | An HTTP gateway gives applications one stable network contract for model calls. | `POST /draft` calls the gateway instead of a provider SDK. |
| FastAPI endpoint | A FastAPI endpoint validates requests and returns typed responses in the lesson app. | `/draft` accepts `GatewayRequest` and returns `GatewayResponse`. |
| Health check | A health check proves the service is running and can be monitored by deployment platforms. | `GET /healthz` returns `ok`. |
| Container image | A container image packages code and dependencies consistently. | Docker builds the gateway for local or cloud deployment. |
| Configuration injection | Configuration injection supplies secrets and environment-specific settings at runtime. | API keys come from env vars or a secret manager. |
| Rollout | A rollout moves a new gateway version into traffic gradually. | Send 10% of traffic to the new version first. |
| Rollback | A rollback returns traffic to a previous known-good version. | Revert if structured output errors spike. |

### Connected dry run

Follow one request through the deployed gateway path.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | A client sends a request to the HTTP API. | HTTP gateway, FastAPI endpoint |
| 2 | The API validates the request body. | Pydantic validation, API contract |
| 3 | The service calls the gateway core. | Gateway service |
| 4 | The gateway selects provider, validates output, and records usage. | Routing, validation, usage ledger |
| 5 | The API returns a stable response or controlled error. | `GatewayResponse`, error mapping |
| 6 | Deployment checks service health. | Health check |
| 7 | The container runs with injected configuration. | Container image, configuration injection |
| 8 | Operators roll forward or roll back based on metrics. | Rollout, rollback, observability |

Step 1: a client calls the HTTP gateway.

The client sends `POST /draft` with a `GatewayRequest`. It does not call Provider A or Provider B directly.

Step 2: FastAPI validates the request body.

Invalid request shapes fail at the API boundary before any provider call. This reduces provider spend and prevents ambiguous downstream errors.

Step 3: the API calls the gateway core.

The endpoint delegates to the same gateway service tested in earlier modules. The API layer is transport glue, not a separate business implementation.

Step 4: the gateway runs the provider workflow.

The core service routes to a provider, handles fallback if allowed, validates structured output, and records usage.

Step 5: the API maps output or errors.

Successful calls return the stable response contract. Provider and gateway errors become controlled HTTP errors instead of raw stack traces.

Step 6: deployment checks health.

A platform such as Cloud Run, ECS, Kubernetes, or a local smoke test can call `/healthz` to decide whether the service starts.

Step 7: the container receives runtime configuration.

Secrets and provider settings are injected at runtime. They are not baked into code or committed to the repository.

Step 8: operators roll forward or roll back.

If latency, error rate, or structured-output failures spike after rollout, operators can revert to the previous known-good image.

### Design decision

Use FastAPI for the lesson API, fake providers for local execution, and Docker for packaging. Real provider credentials should be injected by deployment environment or secret manager, not committed.

### Build

```python
# model_gateway/api.py
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from model_gateway.errors import GatewayError, ProviderError
from model_gateway.gateway import GatewayService
from model_gateway.providers.fake import FakeProviderAdapter
from model_gateway.schemas import GatewayRequest, GatewayResponse
from model_gateway.usage import InMemoryUsageLedger


def build_gateway() -> GatewayService:
    return GatewayService(
        providers=[
            FakeProviderAdapter("fake-primary"),
            FakeProviderAdapter("fake-fallback"),
        ],
        usage_ledger=InMemoryUsageLedger(),
        fallback_order=["fake-primary", "fake-fallback"],
    )


app = FastAPI(title="Northstar Model API Gateway", version="0.1.0")
gateway = build_gateway()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/draft", response_model=GatewayResponse)
async def create_draft(request: GatewayRequest) -> GatewayResponse:
    try:
        return await gateway.complete(request)
    except ProviderError as exc:
        raise HTTPException(
            status_code=503 if exc.retryable else 400,
            detail={"kind": exc.kind.value, "provider": exc.provider, "retryable": exc.retryable},
        ) from exc
    except GatewayError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/v1/draft/stream")
async def stream_draft(request: GatewayRequest) -> StreamingResponse:
    async def event_source():
        async for event in gateway.stream(request):
            yield f"data: {event.model_dump_json()}\n\n"

    return StreamingResponse(event_source(), media_type="text/event-stream")
```

```dockerfile
# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml ./
COPY model_gateway ./model_gateway

RUN pip install --no-cache-dir .

EXPOSE 8080

CMD ["uvicorn", "model_gateway.api:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Unit tests

```python
# tests/test_api.py
from __future__ import annotations

from fastapi.testclient import TestClient

from model_gateway.api import app


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_draft_endpoint_returns_validated_response() -> None:
    client = TestClient(app)
    response = client.post(
        "/v1/draft",
        json={
            "request_id": "r1",
            "tenant_id": "tenant-a",
            "user_id": "user-a",
            "feature": "support_draft",
            "messages": [{"role": "user", "content": "Customer asks for refund without evidence."}],
            "idempotency_key": "tenant-a:r1",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["validated"]["needs_human_review"] is True
    assert body["tenant_id"] == "tenant-a"


def test_stream_endpoint_returns_server_sent_events() -> None:
    client = TestClient(app)
    response = client.post(
        "/v1/draft/stream",
        json={
            "request_id": "r-stream",
            "tenant_id": "tenant-a",
            "user_id": "user-a",
            "feature": "support_draft",
            "messages": [{"role": "user", "content": "Draft cautiously."}],
        },
    )
    assert response.status_code == 200
    assert "data:" in response.text
    assert '"event":"start"' in response.text
```

### Verify in runtime

```bash
pytest
uvicorn model_gateway.api:app --reload
```

Manual request:

```bash
curl -X POST http://127.0.0.1:8000/v1/draft \
  -H "Content-Type: application/json" \
  -d "{\"request_id\":\"r1\",\"tenant_id\":\"tenant-a\",\"user_id\":\"user-a\",\"feature\":\"support_draft\",\"messages\":[{\"role\":\"user\",\"content\":\"Customer asks for refund without evidence.\"}],\"idempotency_key\":\"tenant-a:r1\"}"
```

### Module completion checkpoint

At this point, your project should:

- expose `/health`;
- expose `/v1/draft`;
- expose `/v1/draft/stream`;
- return only validated `GatewayResponse`;
- stream provisional server-sent events without treating them as final validated output;
- package as a Docker image;
- keep secrets out of source code.

### Failure drill

Failure: endpoint returns raw provider JSON.

Evidence: API response contains unvalidated provider-specific fields and no `validated` object.

Fix: return `GatewayResponse` only after validation.

Prevention: response model and API tests.

### Production note

Deploy behind authentication, rate limits, request-size limits, and tenant policy enforcement. FastAPI is the application framework, not the entire production perimeter.

### Guided practice and independent transfer

- Guided: Add a heartbeat or cancellation event to `/v1/draft/stream` and describe how the UI should handle it.
- Independent transfer: Design the gateway route for a classification feature with a different response schema.

### Recall

- Why should `/health` not call every provider?
- Why should secrets not appear in `.env.example` values?
- What should the API return when validation fails?
- What must be added before real customer traffic?

## Reference glossary

| Term | Definition |
|---|---|
| Adapter | Code that maps gateway contracts to one provider API or SDK. |
| Circuit breaker | Reliability control that temporarily stops traffic to a failing dependency. |
| Conversation state | Prior context needed for a request; explicitly passed or owned by application state. |
| Fallback | Switching to another approved provider/model after an allowed failure. |
| Function/tool calling | Model-produced structured request for application-owned tool execution. |
| Gateway | Internal service boundary for routing, validation, reliability, usage, and observability around model providers. |
| Idempotency key | Stable identifier used to make retries safe or detect duplicate operations. |
| Provider error classification | Mapping provider failures to retryable/non-retryable categories. |
| Request tracing | Correlating gateway, provider, logs, usage, and errors through trace/span/request IDs. |
| Schema-constrained output | A requested structured output shape; still must be validated. |
| Streaming | Incremental event delivery before the final response is complete. |
| Usage attribution | Assigning token/cost usage to tenant, user, feature, provider, and model. |

## Full test suite

Command:

```bash
pytest
```

Expected result:

```text
all tests pass
```

Test map:

| Test file | What it proves |
|---|---|
| `test_schemas.py` | Gateway request and multimodal contracts reject invalid data. |
| `test_provider_adapter.py` | Provider adapters normalize responses and are mockable. |
| `test_gateway.py` | Fallback is observable and invalid output is rejected. |
| `test_validation.py` | Structured JSON must pass schema and business gates. |
| `test_tools.py` | Tool calls are allowlisted and argument-validated. |
| `test_streaming.py` | Stream events are explicit and partial output is handled separately. |
| `test_reliability.py` | Retries are bounded and circuits open after failures. |
| `test_usage.py` | Usage is attributed by tenant, user, feature, provider, and model. |
| `test_api.py` | FastAPI endpoints expose the gateway contract. |

What this suite proves:

- provider-specific code is isolated;
- malformed structured output cannot reach successful gateway response;
- retry/fallback behavior is testable;
- usage records are attributed.

What this suite does not prove:

- real provider quality;
- real provider uptime;
- actual provider pricing;
- production load capacity;
- provider-specific SDK compatibility for every model.

## Experiment playbook

| Experiment | Input | Settings | Metric | Expected evidence | Failure signal |
|---|---|---|---|---|---|
| Adapter contract | Same request across fake and mocked HTTPX providers | fixed request, fixed model route | normalized fields | same `ProviderResponse` fields | business code parses raw provider JSON |
| Structured output rejection | malformed JSON and unsafe valid JSON | same provider | rejection count | invalid output raises error | invalid output reaches API success |
| Streaming lifecycle | `/v1/draft/stream` and fake stream | collect server-sent events | event sequence | `START`, `DELTA`, `DONE` | no terminal event |
| Tool execution gate | `lookup_order_status` and rejected `issue_refund` | allowlist read-only tool only | validation and execution result | read-only tool executes; write tool rejected | model-named write tool executes |
| Multimodal serialization | text plus image part | adapter with `supports_multimodal=True` | outbound payload shape | typed parts serialize as JSON objects | Pydantic objects leak into HTTP payload |
| Retry policy | transient timeout | max attempts 3 | attempts and result | retry succeeds or bounded failure | unbounded retries |
| Unsafe retry | retryable provider error but `retry_safe=false` | max attempts 3 | attempts | one attempt only | duplicate attempts |
| Fallback | primary rate limited | fallback enabled | fallback flag | fallback used and recorded | fallback hidden |
| Cost tracking | multiple tenants/users | same provider and example dated price table | ledger grouping and cost estimate | usage separated by tenant/user with estimated cost | only aggregate provider totals |
| Provider deprecation drill | route points to disabled model | config update | failure handling | controlled error and rollback | silent production break |
| Data residency check | tenant requires region | provider route metadata | policy result | only approved region selected | fallback violates region policy |

## Evaluation and acceptance

Use held-out request cases that do not change during a comparison:

- normal support draft;
- missing evidence;
- adversarial user instruction;
- malformed provider output;
- retryable provider failure;
- non-retryable provider failure;
- streaming cancellation;
- tenant requiring specific region/provider policy;
- cost attribution by tenant/user.

Acceptance thresholds:

| Requirement | Acceptance gate |
|---|---|
| Provider isolation | Product code imports gateway contracts, not provider SDKs. |
| Structured output | Invalid or unsafe output cannot reach business logic. |
| Schema-constrained request | Adapter payload includes a response schema request and final output is validated locally. |
| Streaming endpoint | `/v1/draft/stream` emits server-sent events with terminal state. |
| Tool execution | Only registered read-only tools execute; unknown/write tools are rejected. |
| Retry safety | Non-idempotent or unsafe requests are not retried automatically. |
| Fallback | Fallback is visible in response, usage, logs, and traces. |
| Usage attribution | Every successful request records tenant, user, feature, provider, model, token counts. |
| Cost tracking | Cost estimate is derived from configurable dated price data or explicitly left as zero/not measured. |
| Secret handling | No API keys in code, tests, Dockerfile, logs, or examples. |
| Data residency | Provider route can be constrained by tenant policy before real deployment. |
| Model deprecation | Provider/model ID is config-driven and rollback is documented. |

Never fabricate provider uptime, price, or latency. Measure with your own runs or leave fields blank.

## System-decision memo

Use this memo before promoting the gateway from local prototype to pilot service.

```text
Decision:
Candidate design:
Evidence:
Measured strengths:
Measured failures:
Blocked risks:
Cost/latency notes:
Privacy/security notes:
Provider or serving location:
Regional availability:
Provider data policy:
Operational notes:
Decision:
Next experiment:
```

Example:

```text
Decision: Do not promote until real provider adapter contract tests pass.
Candidate design: Gateway with fake primary, mocked HTTPX adapter, Redis-ready usage ledger.
Evidence: Local tests pass; fallback and invalid-output rejection verified.
Measured strengths: Provider-specific code isolated; usage attribution exists.
Measured failures: No real provider latency measurement yet.
Blocked risks: Provider region/data policy not approved for real customer data.
Cost/latency notes: Token counts recorded; no dated provider price config loaded.
Privacy/security notes: No customer data used; secrets externalized.
Decision: Continue to provider sandbox testing.
Next experiment: Run fixed Lesson 08 cases through one real provider with synthetic data only.
```

## Failure modes and debugging

| Symptom | Likely causes | Diagnostic evidence | Corrective action | Prevention |
|---|---|---|---|---|
| 401 from provider | Missing/rotated API key | provider error kind authentication | refresh secret; verify env injection | secret manager and startup checks |
| 429 spikes | Rate limit, traffic burst, retry storm | provider error kind rate limit; retry counts | backoff; open circuit; reduce concurrency | rate limits and per-tenant budgets |
| Invalid JSON reaches app | Missing validation gate | API response lacks validated object | block release; add validation tests | response model and schema gate |
| Duplicate writes after retry | unsafe retry after partial execution or write tool without idempotency | same idempotency key reused incorrectly or missing key | compensate; disable retry for writes | idempotency and read-only tools |
| Fallback invisible | response/usage lacks fallback field | usage records aggregate provider only | add fallback metadata | fallback test and trace attributes |
| Cost cannot be attributed | missing tenant/user/feature metadata | ledger lacks dimensions | update contract; reprocess logs if possible | reject requests missing attribution |
| Streaming UI shows unsafe partial claim | stream delta treated as final | UI sends partial output | require terminal validation state | separate provisional and final UI states |
| Circuit never closes | reset policy wrong or no probe path | circuit state remains open | tune reset and half-open behavior | circuit metrics and runbook |
| Data residency violation | fallback route ignores tenant policy | trace shows provider/region mismatch | disable route; incident review | policy check before routing |
| Model deprecation outage | hard-coded model ID | provider returns invalid model | config update and rollback | model registry and deprecation watch |

## Security, privacy, and governance

| Area | Control |
|---|---|
| Authentication | API keys are injected from environment or secret manager; never passed by caller. |
| Authorization | Tenant/user identity is checked before routing; model output cannot authorize actions. |
| Tenant isolation | Usage, traces, route policy, and logs include tenant but avoid raw sensitive text. |
| Secret handling | No secrets in code, Dockerfile, `.env.example`, tests, or traces. |
| Data residency | Route policy must restrict providers/regions for regulated tenants before real data. |
| Provider data policy | Review retention and training-on-input terms before sending production data. |
| Tool permissions | Tool calls are allowlisted, argument-validated, read-only by default, and executed under application identity. |
| Prompt injection | User/ticket text is untrusted; prompt-specific defenses continue in Lesson 10. |
| Auditability | Record request ID, provider request ID, tenant, user, feature, model, fallback, and trace ID. |
| Human approval | Drafts are suggestions for agents; no automatic customer-facing action. |
| Retention | Usage metadata can be retained; raw customer content needs a separate retention policy. |

## Performance and cost

Measure:

- request latency by provider/model;
- stream time-to-first-token and time-to-final-validation;
- retry attempts;
- fallback rate;
- input, output, and total tokens;
- estimated cost by tenant/user/feature;
- Redis latency for usage/circuit state;
- provider error rate and timeout rate.

Optimization options:

| Lever | Benefit | Risk |
|---|---|---|
| Shorter prompts | Lower input tokens and latency | Reduced instruction clarity |
| Streaming | Better perceived latency | More UI/error-state complexity |
| Smaller fallback model | Lower cost | Lower quality or schema reliability |
| Circuit breaker | Avoids failing provider overload | Can over-block if thresholds wrong |
| Request batching | Higher throughput for batch jobs | Not suitable for interactive support draft |
| Redis shared state | Consistent multi-replica control | Adds dependency and ops cost |

Cost policy:

- Prices must be loaded from dated config, not hard-coded in business logic.
- If pricing is unknown, record tokens and set estimated cost to `0.0` or `not measured`.
- Attribute cost before aggregating totals.

## Deployment and operations

Packaging:

- Build Docker image from the included `Dockerfile`.
- Inject provider keys and Redis URL through deployment environment.
- Do not bake credentials into image layers.

Simple deployment target:

- Cloud Run or equivalent container service for low-ops HTTP deployment.
- Managed Redis for shared usage/circuit state when running more than one replica.
- OpenTelemetry exporter connected to the platform tracing backend.

Health checks:

- `/health` verifies the process is alive.
- A deeper readiness check may verify config, Redis connectivity, and route policy.
- Do not make every health check call external model providers; that can create cost and rate-limit noise.

Rollout:

- Deploy with fake provider disabled only after sandbox provider tests pass.
- Start with one tenant and synthetic/non-production data.
- Shadow or compare before routing agent-visible traffic.
- Roll back by restoring previous route config or container revision.

Alerts:

- provider error rate high;
- fallback rate high;
- validation rejection rate changed;
- p95 latency high;
- cost per tenant/feature above budget;
- Redis unavailable;
- circuit open too long;
- model deprecation or invalid model errors.

Runbook:

1. Identify request ID, trace ID, tenant, provider, model, and fallback flag.
2. Classify the error: auth, rate limit, timeout, invalid request, server, validation, tool policy.
3. Check whether retries were safe and bounded.
4. Check whether fallback happened and whether the fallback provider is approved.
5. Check usage ledger for token/cost spike.
6. Roll back route or model config if provider/model behavior changed.

## Bridge to the next lesson

Lesson 10 assumes you can:

- call a stable gateway contract instead of provider SDKs directly;
- pass messages, schema requests, tool allowlists, and tenant/user metadata;
- receive only validated structured output;
- stream provisional events safely;
- record prompt/model/version/usage metadata;
- observe fallback, retries, and validation failures;
- separate provider integration concerns from prompt design.

Prompt and context engineering will build on this by making instructions, output contracts, examples, untrusted content boundaries, and prompt versions testable.

## Practical assignment

### Scenario

Northstar wants the gateway to support two application features:

- `support_draft`
- `ticket_classification`

Both must use the same provider boundary and usage ledger.

### Requirements

- Add a second response schema for ticket classification.
- Add route policy by feature.
- Add one fake provider and one mocked HTTPX provider contract test.
- Add structured output validation for both schemas.
- Add fallback test for rate limit.
- Add cost/usage attribution by tenant, user, feature, provider, and model.
- Add at least one streaming test.

### Constraints

- No real customer data.
- No hard-coded API keys.
- Invalid output must not reach business logic.
- Write tools are forbidden.
- Retry only safe failures.

### Required artifacts

- Updated schema file.
- Updated gateway service.
- Test suite.
- System-decision memo.
- Failure-mode table for your added feature.
- Runbook update.

### Acceptance criteria

- `pytest` passes.
- Provider-specific code remains isolated.
- Fallback is observable.
- Usage is attributable.
- Invalid structured output is rejected.

### Stretch goals

- Add Redis-backed circuit breaker state.
- Add server-sent events endpoint.
- Add dated price config and cost calculation.
- Add provider-region route policy.
- Add native SDK adapter behind the same interface.

## Interview preparation

### Concept questions

| Question | Strong answer expectation |
|---|---|
| Why build a gateway instead of calling one SDK directly? | Stable contract, provider isolation, validation, reliability, tracing, cost, governance. |
| What is provider-independent design? | Product code depends on internal request/response contracts; adapters handle provider specifics. |
| What does structured output solve and not solve? | Solves parse shape when validated; does not guarantee truth, safety, or business correctness. |
| Why is streaming harder than non-streaming? | Partial output, terminal state, cancellation, validation timing, UI safety. |

### Coding or implementation questions

| Question | Strong answer expectation |
|---|---|
| Implement a retry policy. | Bounded attempts, classified errors, backoff, idempotency awareness. |
| Add a provider adapter. | Implement interface, map payload, normalize response, classify errors, test with mocked transport. |
| Validate tool calls. | Allowlist name, validate args, enforce permissions, no model-owned authorization. |

### Debugging questions

| Question | Strong answer expectation |
|---|---|
| Requests suddenly cost 3x more. | Check token counts, prompt/context growth, fallback provider, model changes, usage by tenant/feature. |
| Fallback seems to work but quality drops. | Inspect provider/model/fallback dimensions, run fixed eval set, gate promotion. |
| Provider returns 429. | Backoff, circuit breaker, concurrency/rate limits, fallback if approved, alert if sustained. |

### System-design question

Design a multi-provider AI gateway for a support product serving multiple tenants.

Strong answer should include:

- provider-neutral contract;
- adapter isolation;
- schema validation;
- stream event model;
- tool-call allowlist;
- retries, timeouts, circuit breaker;
- fallback route policy;
- tenant/user usage ledger;
- OpenTelemetry traces;
- secret management;
- data residency/provider policy controls;
- rollout and rollback.

### Tradeoff questions

| Tradeoff | Strong answer expectation |
|---|---|
| Native SDK vs HTTPX | SDK convenience vs explicit portability/testability; either must stay inside adapters. |
| Fallback vs fail fast | Availability vs quality/privacy/cost/regional differences. |
| In-memory vs Redis circuit state | Simplicity vs multi-replica consistency. |
| Streaming vs non-streaming | Perceived latency vs validation/UI complexity. |

## Mastery check

### One-page memory model

```text
product request
  -> tenant/user/feature identity
  -> GatewayRequest
  -> route policy
  -> provider adapter
  -> timeout/error classification
  -> retry if safe
  -> fallback if approved
  -> provider response/stream
  -> schema + tool validation
  -> usage ledger + trace
  -> GatewayResponse to business logic
```

Do not let raw provider output, hidden fallback, unvalidated tool calls, or unattributed cost cross the gateway boundary.

### Retrieval bank

- Explain why provider-specific code belongs in adapters.
- Draw the request flow from product service to provider and back.
- Predict what happens when a provider returns malformed JSON.
- Diagnose a 429 spike with rising cost.
- Compare native SDK and HTTPX adapters.
- Explain why retries require idempotency.
- Explain why fallback must be observable.
- Predict what happens if a stream ends without `DONE`.
- Diagnose a data-residency fallback violation.
- Design a cost attribution record.
- Explain why tool calling is not tool authorization.
- Transfer the gateway design to a classification feature.

### Self-assessment

You are ready to continue if you can:

- implement a provider adapter without changing product contracts;
- reject invalid structured output before business logic;
- classify retryable and non-retryable provider errors;
- explain when fallback is unsafe;
- record usage by tenant/user/feature/provider/model;
- keep secrets out of code and logs;
- describe how Lesson 10 prompt versions will use gateway metadata.

### Spaced-review plan

| Time | Retrieval task |
|---|---|
| 1 day | Recreate the gateway request flow and error/fallback decision tree from memory. |
| 3 days | Write a new adapter contract test for a hypothetical provider response shape. |
| 1 week | Diagnose three failures: malformed JSON, hidden fallback, duplicate retry. |
| 3-4 weeks | Design a gateway for a different domain with tenant policy, usage ledger, and streaming. |

## Production-readiness checklist

- [ ] Provider-neutral request/response contract exists.
- [ ] Provider-specific code is isolated in adapters.
- [ ] Secrets are externalized.
- [ ] Tenant/user/feature identity is required.
- [ ] Structured output is schema-validated.
- [ ] Unsafe valid JSON is policy-rejected.
- [ ] Tool calls are allowlisted and argument-validated.
- [ ] Write tools require external approval and idempotency.
- [ ] Streaming has terminal states and partial-output handling.
- [ ] Multimodal inputs are capability-gated.
- [ ] Timeouts are configured.
- [ ] Retry policy is bounded and safe.
- [ ] Circuit breaker exists.
- [ ] Fallback is approved by policy and observable.
- [ ] Usage is attributed by tenant/user/feature/provider/model.
- [ ] Cost uses dated configurable price data or is marked not measured.
- [ ] Traces include request ID, provider, model, fallback, and error kind.
- [ ] Redis or equivalent shared state is configured for multi-replica deployment.
- [ ] Data residency and provider data policy are reviewed.
- [ ] Rollback path is documented.
- [ ] Lesson 10 handoff includes prompt/model/version metadata.

## Lesson summary

You learned and built the production boundary around hosted model APIs:

- provider authentication and adapter isolation;
- message and response contracts;
- structured output validation;
- tool/function-call control;
- streaming and multimodal request modeling;
- provider error classification;
- timeouts, bounded retries, circuit breakers, and fallback;
- request tracing, token accounting, and cost attribution;
- Redis-ready shared state;
- FastAPI and Docker deployment path.

The gateway now gives Northstar a controlled integration layer. Lesson 10 will use this layer to make prompts and context into versioned, testable application components.

## Official references

- OpenAI Responses API reference: https://platform.openai.com/docs/api-reference/responses
- OpenAI function calling guide: https://platform.openai.com/docs/guides/function-calling
- OpenAI streaming guide: https://platform.openai.com/docs/guides/streaming-responses
- Anthropic Messages API reference: https://docs.anthropic.com/en/api/messages
- Anthropic tool use guide: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview
- HTTPX timeout documentation: https://www.python-httpx.org/advanced/timeouts/
- Pydantic documentation: https://docs.pydantic.dev/
- FastAPI documentation: https://fastapi.tiangolo.com/
- pytest documentation: https://docs.pytest.org/
- Redis Streams documentation: https://redis.io/docs/latest/develop/data-types/streams/
- OpenTelemetry Python documentation: https://opentelemetry.io/docs/languages/python/
- Dockerfile reference: https://docs.docker.com/reference/dockerfile/
- Google Cloud Run documentation: https://cloud.google.com/run/docs
