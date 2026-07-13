# Stage 10 - Real Hosted LLM Provider Integration

## Goal

Add one real hosted model provider behind `packages/model_gateway` without changing the API route
contract or the default local mock behavior.

## Provider

The hosted provider uses the OpenAI Responses API with Structured Outputs:

- Endpoint: `POST /v1/responses`.
- Provider route: `MODEL_PROVIDER=openai`.
- Default model: `gpt-5.6`.
- Output mode: strict `json_schema` through `text.format`.
- Prompt: `full_ticket_analysis.v1`.
- Local validation: `FullTicketAnalysis` Pydantic schema.

The provider sends `store: false` so local analysis calls do not opt in to response storage.

## Configuration

Required for real hosted calls:

```env
MODEL_PROVIDER=openai
MODEL_API_KEY=your-api-key
```

Optional overrides:

```env
MODEL_NAME=gpt-5.6
MODEL_BASE_URL=https://api.openai.com/v1
MODEL_TIMEOUT_SECONDS=30
MODEL_MAX_OUTPUT_TOKENS=1200
```

The default remains:

```env
MODEL_PROVIDER=mock
MODEL_API_KEY=
```

## Failure Behavior

- Missing API key or unsupported provider raises a controlled configuration error.
- HTTP failures and timeouts raise a controlled request error.
- Malformed JSON, refused responses, incomplete responses, or schema-invalid output raise a
  controlled response error.
- The API maps invalid model output to HTTP 502 and provider availability/configuration failures to
  HTTP 503.

## Why This Matters

The API route still saves the same recommendation shape as the mock provider: category, priority,
escalation flag, confidence, extracted fields, reasons, summary, suggested reply, model name, and
prompt version. That keeps approval metrics and review workflows stable while allowing real hosted
model output to be compared against mock and baseline behavior.

## Official References

- OpenAI Structured Outputs: https://developers.openai.com/api/docs/guides/structured-outputs
- OpenAI Responses API: https://developers.openai.com/api/reference/resources/responses/methods/create
