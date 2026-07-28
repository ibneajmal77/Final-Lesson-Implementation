# Cost Report

## Current Status

Stage 13 added durable model usage and cost tracking.

Current local/default configuration:

- Provider: `mock`
- Input token cost per 1K tokens: `0.0`
- Output token cost per 1K tokens: `0.0`
- Mock provider token usage: `0` input, `0` output
- Mock provider estimated cost: `$0.00000000`

## Where Costs Are Recorded

Model usage is stored in `cost_events` with tenant, ticket, optional `ai_run_id`, optional
recommendation id, provider, model, prompt version, token counts, estimated cost, latency, and
created timestamp.

## How To View Cost Metrics

Tenant-scoped JSON aggregation:

```powershell
Invoke-RestMethod -Method Get `
  -Uri 'http://127.0.0.1:8765/metrics/costs' `
  -Headers $headers
```

Process-local Prometheus text:

```powershell
Invoke-WebRequest -Uri 'http://127.0.0.1:8765/metrics/runtime' -UseBasicParsing
```

## Pricing Configuration

Set these environment variables before running hosted-provider analysis:

```powershell
$env:MODEL_INPUT_COST_PER_1K_TOKENS = '<input-rate>'
$env:MODEL_OUTPUT_COST_PER_1K_TOKENS = '<output-rate>'
```

The project does not hardcode hosted model pricing because pricing can change outside the codebase.
