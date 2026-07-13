# Stage 9 and Stage 10 Combined Implementation Guide

This guide explains how Stage 9 and Stage 10 work together, why they were implemented this way,
and how to follow the code step by step.

## Combined Goal

Stage 9 and Stage 10 connect the prompt system to a real hosted model provider.

Stage 9 creates the contract:

- What prompt should be sent.
- What JSON shape the model must return.
- How the model output is validated before use.

Stage 10 creates the provider integration:

- How the app chooses between mock and hosted providers.
- How the OpenAI Responses API is called.
- How structured model output is parsed.
- How model failures are mapped to controlled API errors.
- How the validated result is saved as a ticket recommendation.

The full flow is:

```text
Ticket
-> render versioned prompt
-> call provider selected by MODEL_PROVIDER
-> receive structured JSON
-> validate with Pydantic
-> convert into TicketAnalysisResult
-> save as ticket recommendation
-> human review workflow continues unchanged
```

## Stage 9 - Prompt Contract and Structured Output

Stage 9 lives mostly in:

```text
packages/prompts/supportops_prompts/
```

### Step 1 - Define Allowed Values

File:

```text
packages/prompts/supportops_prompts/schemas.py
```

The prompt schemas define allowed values for categories and priorities.

Allowed categories:

```text
security
billing
account_access
delivery
technical_issue
other
```

Allowed priorities:

```text
low
normal
high
urgent
```

This prevents the model from returning random values like `refund_problem`, `medium-high`, or
`customer_angry`.

### Step 2 - Define Strict Output Schemas

The most important schema for Stage 10 is `FullTicketAnalysis`.

It requires the hosted model to return:

```text
category
category_confidence
priority
requires_escalation
extracted_fields
evidence_ids
draft_response
abstain
risk_flags
missing_information
```

The schema uses Pydantic with `extra="forbid"`, which means unknown fields are rejected.

That matters because model output should not be trusted just because it looks like JSON. It must
match the exact application contract before it can be saved.

### Step 3 - Create Versioned Prompt Templates

Prompt templates live in:

```text
packages/prompts/supportops_prompts/templates/
```

Stage 9 created separate prompt templates for smaller tasks:

```text
classify_ticket.v1.md
extract_fields.v1.md
recommend_priority.v1.md
draft_response.v1.md
safety_check.v1.md
```

Stage 10 added:

```text
full_ticket_analysis.v1.md
```

The full-analysis prompt asks for one complete recommendation that includes classification,
priority, extracted fields, safety behavior, and draft response.

### Step 4 - Use an Untrusted Ticket Boundary

Every prompt separates system instructions from customer text:

```text
UNTRUSTED_TICKET_TEXT_START

Subject: ...

Body:
...

UNTRUSTED_TICKET_TEXT_END
```

This helps defend against prompt injection. If a customer writes, "Ignore the above instructions",
that text is inside the untrusted boundary and should not override the developer instructions.

### Step 5 - Register Prompts

File:

```text
packages/prompts/supportops_prompts/registry.py
```

Each prompt has a `PromptSpec`:

```text
name
version
template_path
output_schema
required_variables
changelog
```

For Stage 10, the important registry entry is:

```text
full_ticket_analysis.v1
```

It points to:

```text
template_path = full_ticket_analysis.v1.md
output_schema = FullTicketAnalysis
```

### Step 6 - Render the Prompt

The `render_prompt()` function loads the template and injects:

```text
ticket_subject
ticket_body
customer_id
policy_context
prompt_id
output_schema
```

It also inserts the JSON schema generated from the Pydantic model.

This means the model sees the exact JSON shape it must return.

## Stage 10 - Real Hosted LLM Provider Integration

Stage 10 lives mostly in:

```text
packages/model_gateway/supportops_model_gateway/
```

The purpose is to add a real provider without changing the rest of the application.

## Step 1 - Keep the Provider Interface Stable

File:

```text
packages/model_gateway/supportops_model_gateway/providers/base.py
```

The app already had:

```text
TicketAnalysisInput
TicketAnalysisResult
TicketAnalysisProvider
```

The API route only needs a provider that can do this:

```text
analyze_ticket(ticket) -> TicketAnalysisResult
```

That is why the API does not need to know whether the provider is mock or OpenAI.

## Step 2 - Add Hosted Provider Configuration

File:

```text
apps/api/supportops_api/settings.py
```

Stage 10 added:

```env
MODEL_PROVIDER=mock
MODEL_API_KEY=
MODEL_NAME=gpt-5.6
MODEL_BASE_URL=https://api.openai.com/v1
MODEL_TIMEOUT_SECONDS=30
MODEL_MAX_OUTPUT_TOKENS=1200
```

The default is still:

```env
MODEL_PROVIDER=mock
```

That is intentional. Local tests and development should not require a real API key.

To use the hosted provider:

```env
MODEL_PROVIDER=openai
MODEL_API_KEY=your-api-key
```

## Step 3 - Add Provider Routing

File:

```text
packages/model_gateway/supportops_model_gateway/routing.py
```

The provider factory now works like this:

```text
MODEL_PROVIDER=mock
-> MockTicketAnalysisProvider

MODEL_PROVIDER=openai
-> HostedTicketAnalysisProvider

MODEL_PROVIDER=hosted
-> HostedTicketAnalysisProvider
```

Unsupported providers raise `UnsupportedModelProviderError`.

## Step 4 - Build the Hosted Provider

File:

```text
packages/model_gateway/supportops_model_gateway/providers/hosted.py
```

The main class is:

```text
HostedTicketAnalysisProvider
```

The main method is:

```text
analyze_ticket()
```

It does these steps:

```text
1. Load full_ticket_analysis.v1 from the prompt registry.
2. Render the prompt with ticket subject, body, customer ID, and policy context.
3. Build an OpenAI Responses API request.
4. Send POST /responses.
5. Extract the output text.
6. Validate the output as FullTicketAnalysis.
7. Convert it into TicketAnalysisResult.
```

## Step 5 - Send a Strict Structured Output Request

The hosted provider sends a request like this conceptually:

```json
{
  "model": "gpt-5.6",
  "input": "rendered prompt text",
  "max_output_tokens": 1200,
  "store": false,
  "metadata": {
    "prompt_id": "full_ticket_analysis.v1",
    "schema_name": "supportops_full_ticket_analysis"
  },
  "text": {
    "format": {
      "type": "json_schema",
      "name": "supportops_full_ticket_analysis",
      "strict": true,
      "schema": "FullTicketAnalysis JSON schema"
    }
  }
}
```

Important decisions:

- `store: false` avoids opting in to hosted response storage for these local calls.
- `strict: true` asks the model to follow the JSON schema.
- The schema comes from `FullTicketAnalysis.model_json_schema()`.

## Step 6 - Handle Hosted Provider Errors

File:

```text
packages/model_gateway/supportops_model_gateway/errors.py
```

Stage 10 added controlled gateway errors:

```text
ModelGatewayError
ModelProviderConfigurationError
ModelProviderRequestError
ModelProviderResponseError
```

These keep provider-specific failures from leaking directly into the API.

Examples:

```text
missing API key
-> ModelProviderConfigurationError

timeout or HTTP failure
-> ModelProviderRequestError

malformed JSON or schema-invalid output
-> ModelProviderResponseError
```

## Step 7 - Validate the Model Output Locally

Even though the OpenAI request uses strict structured output, the app still validates locally:

```text
FullTicketAnalysis.model_validate_json(output_text)
```

This is important because the database should only receive trusted application data.

If validation fails, the provider raises:

```text
ModelProviderResponseError
```

## Step 8 - Convert Model Output Into App Output

The hosted provider converts `FullTicketAnalysis` into `TicketAnalysisResult`.

That result contains:

```text
source
model_name
prompt_version
category
priority
requires_escalation
confidence
summary
suggested_reply
extracted_fields
reasons
input_tokens
output_tokens
latency_ms
raw_response_id
```

The API route already knows how to save `TicketAnalysisResult`, so the rest of the app does not need
to change.

## Step 9 - Wire the API Route

File:

```text
apps/api/supportops_api/routes/tickets.py
```

The endpoint is still:

```text
POST /tickets/{ticket_id}/ai-analysis
```

The route now:

```text
1. Loads the ticket by tenant.
2. Builds the configured provider.
3. Calls analyze_ticket().
4. Saves the returned recommendation.
5. Returns the saved recommendation.
```

The route maps errors like this:

```text
Unsupported provider or missing API key
-> HTTP 503

Hosted provider timeout or HTTP failure
-> HTTP 503

Malformed or schema-invalid model output
-> HTTP 502
```

This means model failures are controlled and predictable.

## Step 10 - Save the Recommendation

The saved recommendation includes:

```text
source
category
priority
requires_escalation
confidence
extracted_fields
reasons
model_name
prompt_version
summary
suggested_reply
```

This lets later stages compare:

```text
baseline_v1
mock_llm_v1
openai_responses_v1
```

It also keeps the human approval workflow unchanged.

## How To Run Mock Mode

Use mock mode when developing locally:

```powershell
$env:MODEL_PROVIDER = 'mock'

python -m uvicorn supportops_api.main:app `
  --reload `
  --app-dir apps/api `
  --host 127.0.0.1 `
  --port 8765
```

Then call:

```text
POST http://127.0.0.1:8765/tickets/{ticket_id}/ai-analysis
```

## How To Run Hosted OpenAI Mode

Use hosted mode only when you have an API key:

```powershell
$env:MODEL_PROVIDER = 'openai'
$env:MODEL_API_KEY = '<your-api-key>'
$env:MODEL_NAME = 'gpt-5.6'

python -m uvicorn supportops_api.main:app `
  --reload `
  --app-dir apps/api `
  --host 127.0.0.1 `
  --port 8765
```

Then call the same endpoint:

```text
POST http://127.0.0.1:8765/tickets/{ticket_id}/ai-analysis
```

The API endpoint does not change. Only the provider behind it changes.

## Tests

Stage 9 tests verify:

```text
valid FullTicketAnalysis parses
missing required fields fail
unknown categories fail unless category is other
confidence outside 0 to 1 fails
prompt versions exist
templates render with required variables
missing render variables fail
```

Stage 10 tests verify:

```text
mock provider still works
hosted provider builds the expected structured-output request
hosted provider parses valid structured output
missing OpenAI API key fails cleanly
invalid hosted output fails cleanly
unknown providers are rejected
```

The hosted provider tests use `httpx.MockTransport`, so they do not make real network calls.

## Verification Commands

Run tests:

```powershell
python -m pytest -q
```

Run lint:

```powershell
python -m ruff check --no-cache .
```

Current verified result:

```text
56 passed
Ruff: all checks passed
```

## Why This Design Is Good

The design keeps responsibilities separate:

```text
packages/prompts
-> prompt templates and schema contracts

packages/model_gateway
-> provider selection, hosted API calls, model parsing

apps/api
-> HTTP request handling and database persistence

packages/db
-> stored recommendations and review data
```

This makes the system easier to test, safer to extend, and easier to debug.

The most important idea:

```text
Never let raw model text go directly into business logic or the database.
Render a versioned prompt, request structured output, validate locally, then save.
```
