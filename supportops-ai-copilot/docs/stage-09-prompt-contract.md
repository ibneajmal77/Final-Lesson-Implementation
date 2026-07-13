# Stage 9 - Prompt Contract and Structured Output Design

## Goal

Stage 9 creates the contract that future real LLM output must follow.

This stage still does not call a real hosted LLM. It prepares the system so that when a real model
is added, its output can be validated, tested, versioned, and compared safely.

## Why This Stage Exists

Calling an LLM is easy. Trusting its output in a production workflow is not.

Before the real LLM provider is added, the project needs:

- strict output schemas;
- versioned prompt templates;
- prompt metadata;
- tests that fail when output shape changes unexpectedly;
- untrusted-ticket boundaries inside prompts;
- abstention and safety rules in every prompt.

This keeps future model output from becoming unstructured text that is hard to validate, review, or
debug.

## What Was Implemented

Prompt package:

```text
packages/prompts/supportops_prompts/
  registry.py
  schemas.py
  templates/
    classify_ticket.v1.md
    extract_fields.v1.md
    recommend_priority.v1.md
    draft_response.v1.md
    safety_check.v1.md
  tests/
    fixtures/
      billing_ticket.json
```

Tests:

```text
tests/prompts/test_prompt_schemas.py
tests/prompts/test_prompt_registry.py
```

## Structured Output Schemas

The schemas are Pydantic models in:

```text
packages/prompts/supportops_prompts/schemas.py
```

Implemented schemas:

- `TicketClassification`
- `TicketFieldExtraction`
- `PriorityRecommendation`
- `DraftResponse`
- `SafetyCheck`
- `FullTicketAnalysis`

Important schema rules:

- Unknown fields are rejected.
- Unknown categories are rejected unless category is `other`.
- Priority must be one of `low`, `normal`, `high`, or `urgent`.
- Confidence scores must be between `0` and `1`.
- Draft responses must be marked for human review.

## Prompt Templates

Each prompt template includes:

- task;
- inputs;
- output schema;
- untrusted ticket text boundary;
- abstention rule;
- safety rule;
- examples.

The untrusted boundary matters because customer ticket text can contain prompt-injection attempts.
Every prompt makes it explicit that ticket text must be treated as customer-provided data, not as
developer instructions.

## Prompt Registry

The prompt registry lives in:

```text
packages/prompts/supportops_prompts/registry.py
```

It records:

- prompt name;
- version;
- template path;
- output schema;
- required render variables;
- changelog.

The renderer injects:

- ticket subject;
- ticket body;
- customer ID;
- policy context;
- generated JSON schema.

## Current Render Variables

Every prompt currently requires:

```text
ticket_subject
ticket_body
customer_id
policy_context
```

If a required variable is missing, rendering fails.

## Tests Added

The tests verify:

- valid `FullTicketAnalysis` output parses;
- missing required fields fail;
- unknown categories fail unless `other`;
- confidence outside `0` to `1` fails;
- all prompt versions exist;
- every prompt has an output schema;
- templates render with required variables;
- missing render variables fail;
- the billing regression fixture still maps to `billing` with the mock provider.

## How This Connects To Stage 10

Stage 10 can now add a real provider behind the model gateway.

The expected future flow is:

```text
ticket
-> render prompt from registry
-> call real model provider
-> parse model JSON with Pydantic schema
-> reject malformed output
-> save validated recommendation
-> human approval
-> metrics/evaluation
```

Without Stage 9, Stage 10 would only be a raw API call. With Stage 9, Stage 10 becomes a controlled
LLM integration.

