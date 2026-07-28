# API Contracts

This document records the current API contract.

## Authentication model for current stage

This project currently uses development headers:

```text
X-Tenant-Id: tenant_demo
X-User-Id: user_demo_agent
X-Role: agent
```

This is not final production auth. It exists so we can learn tenant isolation before adding OAuth
or JWTs.

Allowed roles for this stage:

- `agent`
- `lead`
- `admin`
- `service`

Unknown roles return `403`. Support policy creation requires `lead` or `admin`.

## Health

```http
GET /health
```

Returns whether the API process is alive.

## Readiness

```http
GET /ready
```

Returns whether required dependencies are reachable.

Current checks:

- configuration loaded
- PostgreSQL responds
- Redis responds

## Support Policies

Support policies are tenant-scoped context records that can be included in hosted AI analysis.

### Create Support Policy

```http
POST /policies
```

Headers require a `lead` or `admin` role.

Request:

```json
{
  "name": "Refund review",
  "content": "Agents must verify duplicate charges before promising refunds.",
  "retention_expires_at": null
}
```

Response:

```json
{
  "id": "generated-policy-id",
  "tenant_id": "tenant_demo",
  "name": "Refund review",
  "content": "Agents must verify duplicate charges before promising refunds.",
  "created_by_user_id": "user_demo_lead",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "retention_expires_at": null
}
```

Status codes:

- `201`: policy created
- `401`: identity headers are missing
- `403`: actor role is not allowed to create policies
- `404`: tenant does not exist
- `422`: request body is invalid

### List Support Policies

```http
GET /policies
```

Returns support policies for the current tenant only.

### Get Support Policy

```http
GET /policies/{policy_id}
```

Returns one support policy for the current tenant.

Important tenant rule:

- If the policy exists under another tenant, this endpoint returns `404`.
- It does not reveal that another tenant owns the policy.
## Create Ticket

```http
POST /tickets
```

Headers:

```text
X-Tenant-Id: tenant_demo
X-User-Id: user_demo_agent
X-Role: agent
```

Request:

```json
{
  "external_id": "demo-ticket-001",
  "channel": "email",
  "subject": "Charged twice",
  "body": "I was charged twice for order ORD-123.",
  "customer_id": "customer-123",
  "metadata": {
    "source": "manual-test"
  }
}
```

Response:

```json
{
  "id": "generated-ticket-id",
  "tenant_id": "tenant_demo",
  "external_id": "demo-ticket-001",
  "channel": "email",
  "subject": "Charged twice",
  "body": "I was charged twice for order ORD-123.",
  "status": "open",
  "priority": "normal",
  "customer_id": "customer-123",
  "metadata": {
    "source": "manual-test"
  },
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

Status codes:

- `201`: ticket created
- `200`: same tenant and `external_id` already exists, so existing ticket is returned
- `401`: identity headers are missing
- `404`: tenant does not exist
- `422`: request body is invalid

## List Tickets

```http
GET /tickets
```

Returns tickets for the current tenant only.

## Get Ticket

```http
GET /tickets/{ticket_id}
```

Returns one ticket for the current tenant.

Important tenant rule:

- If the ticket exists under another tenant, this endpoint returns `404`.
- It does not reveal that another tenant owns the ticket.

## Create Baseline Analysis

```http
POST /tickets/{ticket_id}/baseline-analysis
```

Runs the deterministic baseline classifier for one ticket and saves the recommendation.

Current baseline output:

- category
- recommended priority
- escalation flag
- confidence score
- extracted fields
- explanation reasons

Response:

```json
{
  "id": "generated-recommendation-id",
  "tenant_id": "tenant_demo",
  "ticket_id": "generated-ticket-id",
  "source": "baseline_v1",
  "category": "billing",
  "priority": "high",
  "requires_escalation": false,
  "confidence": 0.85,
  "model_name": null,
  "prompt_version": null,
  "summary": null,
  "suggested_reply": null,
  "extracted_fields": {
    "order_ids": ["ORD-123"],
    "amounts": [],
    "matched_category_terms": ["charged twice"],
    "matched_priority_terms": ["charged twice"],
    "matched_escalation_terms": []
  },
  "reasons": [
    "Category 'billing' matched keywords: charged twice.",
    "Extracted order IDs: ORD-123.",
    "Priority 'high' matched terms: charged twice."
  ],
  "created_at": "timestamp"
}
```

Status codes:

- `201`: recommendation created
- `401`: identity headers are missing
- `404`: tenant or ticket does not exist for the current tenant

Important behavior:

- This endpoint does not change the ticket's real `priority`.
- It only saves a recommendation for later review or comparison.

## Create AI Analysis

```http
POST /tickets/{ticket_id}/ai-analysis
```

Runs the configured ticket-analysis provider and saves the recommendation.

Current default provider:

- `MODEL_PROVIDER=mock`
- no external API call
- deterministic output shaped like future LLM output

Hosted provider option:

- `MODEL_PROVIDER=openai` or `MODEL_PROVIDER=hosted`
- sends the rendered prompt, strict JSON schema, ticket subject, ticket body, optional customer ID,
  and tenant-scoped policy context
- sets `store: false`
- rejects malformed output, unknown JSON fields, and unsupported evidence IDs before persistence

Response:

```json
{
  "id": "generated-recommendation-id",
  "tenant_id": "tenant_demo",
  "ticket_id": "generated-ticket-id",
  "source": "mock_llm_v1",
  "category": "billing",
  "priority": "high",
  "requires_escalation": false,
  "confidence": 0.9,
  "model_name": "mock-ticket-analyzer",
  "prompt_version": "supportops_ticket_analysis_v1",
  "summary": "Customer reported a high priority billing issue involving order ORD-123.",
  "suggested_reply": "Thanks for reaching out. I will review the billing details...",
  "extracted_fields": {
    "order_ids": ["ORD-123"],
    "customer_id": "customer-123",
    "provider": "mock"
  },
  "reasons": [
    "Mock provider used deterministic baseline analysis."
  ],
  "created_at": "timestamp"
}
```

Status codes:

- `201`: recommendation created
- `401`: identity headers are missing
- `404`: tenant or ticket does not exist for the current tenant
- `403`: AI analysis is not enabled for the current tenant or detected ticket category
- `503`: AI analysis is disabled or the configured model provider is unavailable/unsupported

Important behavior:

- `AI_ANALYSIS_ENABLED=false` disables this endpoint for staging rollback and returns HTTP 503.
- `AI_ANALYSIS_ENABLED_TENANTS` optionally restricts AI analysis to a comma-separated tenant allowlist.
- `AI_ANALYSIS_ENABLED_CATEGORIES` optionally restricts AI analysis to comma-separated baseline categories.
- It stores a draft reply but does not send it to the customer.
- It does not change the ticket's real `priority`.

## Queue Async AI Analysis

```http
POST /tickets/{ticket_id}/analyze
```

Creates an AI run record and queues background ticket analysis.

Status codes:

- `202`: analysis run queued
- `401`: identity headers are missing
- `404`: tenant or ticket does not exist for the current tenant
- `403`: AI analysis is not enabled for the current tenant or detected ticket category
- `503`: AI analysis is disabled or the analysis queue is unavailable

Important behavior:

- `AI_ANALYSIS_ENABLED=false` returns HTTP 503 before a run is created or enqueued.
- Tenant/category pilot gates return HTTP 403 before a run is created or enqueued.
- Successful requests create an `ai_runs` row with `queued` status.
- The worker updates the run to `running`, `succeeded`, `failed`, or `abstained`.

```http
GET /tickets/{ticket_id}/analysis
```

Returns analysis run history for one ticket under the current tenant.
## List Ticket Recommendations

```http
GET /tickets/{ticket_id}/recommendations
```

Returns saved recommendations for one ticket under the current tenant.

Important tenant rule:

- If the ticket exists under another tenant, this endpoint returns `404`.
- It does not reveal that another tenant owns the ticket.

## Create Recommendation Review

```http
POST /tickets/{ticket_id}/recommendations/{recommendation_id}/reviews
```

Creates a human review event for a saved recommendation.

Allowed decisions:

- `approved`
- `rejected`
- `edited`

Approve request:

```json
{
  "decision": "approved",
  "notes": "Ready for agent use."
}
```

Edit request:

```json
{
  "decision": "edited",
  "edited_reply": "I reviewed the billing issue and will verify the duplicate charge.",
  "notes": "Adjusted before use."
}
```

Reject request:

```json
{
  "decision": "rejected",
  "notes": "Incorrect tone for this customer."
}
```

Response:

```json
{
  "id": "generated-review-id",
  "tenant_id": "tenant_demo",
  "ticket_id": "generated-ticket-id",
  "recommendation_id": "generated-recommendation-id",
  "reviewer_user_id": "user_demo_agent",
  "decision": "approved",
  "final_summary": "Customer reported a high priority billing issue involving order ORD-123.",
  "final_reply": "Thanks for reaching out. I will review the billing details...",
  "notes": "Ready for agent use.",
  "created_at": "timestamp"
}
```

Status codes:

- `201`: review created
- `401`: identity headers are missing
- `404`: tenant, ticket, or recommendation does not exist for the current tenant
- `422`: request body is invalid, or `edited` is missing edited content

Important behavior:

- `approved` stores the recommendation's current summary and suggested reply as final content.
- `edited` stores the edited summary or edited reply as final content.
- `rejected` stores no final summary or final reply.
- No customer message is sent in this stage.

## List Recommendation Reviews

```http
GET /tickets/{ticket_id}/recommendations/{recommendation_id}/reviews
```

Returns human review events for one recommendation under the current tenant.

## Review Metrics

```http
GET /metrics/reviews
```

Returns review and feedback metrics for the current tenant.

Response:

```json
{
  "tenant_id": "tenant_demo",
  "total_recommendations": 10,
  "reviewed_recommendations": 8,
  "review_coverage_rate": 0.8,
  "total_reviews": 8,
  "approved": 5,
  "rejected": 1,
  "edited": 2,
  "approval_rate": 0.625,
  "rejection_rate": 0.125,
  "edit_rate": 0.25,
  "by_source": [
    {
      "key": "mock_llm_v1",
      "total_reviews": 8,
      "approved": 5,
      "rejected": 1,
      "edited": 2,
      "approval_rate": 0.625,
      "rejection_rate": 0.125,
      "edit_rate": 0.25
    }
  ],
  "by_category": [
    {
      "key": "billing",
      "total_reviews": 8,
      "approved": 5,
      "rejected": 1,
      "edited": 2,
      "approval_rate": 0.625,
      "rejection_rate": 0.125,
      "edit_rate": 0.25
    }
  ]
}
```

Status codes:

- `200`: metrics returned
- `401`: identity headers are missing
- `404`: tenant does not exist

Important behavior:

- Metrics are scoped to the current tenant.
- `review_coverage_rate` measures reviewed recommendations divided by total recommendations.
- `by_source` helps compare baseline, mock LLM, and future real LLM outputs.
- `by_category` helps identify categories that need better prompts, rules, or training data.

## Pilot Metrics

```http
GET /metrics/pilot
```

Returns pilot-only metrics for the current tenant. If `AI_ANALYSIS_ENABLED_CATEGORIES` is set, the report is filtered to those categories; otherwise it includes all non-baseline AI drafts.

Response fields:

- `pilot_categories`: active pilot category filters.
- `draft_acceptance_rate`: approved or edited drafts divided by reviewed AI drafts.
- `average_edit_distance`: average character-level edit distance for edited drafts.
- `average_time_to_first_response_seconds`: time between ticket creation and first review.
- `escalation_accuracy`: accepted escalated drafts divided by reviewed escalated drafts.
- `cost_per_accepted_draft`: persisted model cost divided by accepted drafts.
- `safety_failures`: failed AI runs with safety-related error markers.
- `agent_rejection_reasons`: keyword-clustered rejection notes.
- `exit_decision`: one of `expand`, `iterate`, `roll_back`, or `stop`.

## Pilot Feedback Candidates

```http
GET /metrics/pilot/feedback
```

Returns rejected drafts and heavily edited drafts for the current tenant and active pilot categories. These candidates feed the weekly feedback-to-eval loop and should be reviewed before adding representative failures to `packages/evals/supportops_evals/datasets/difficult_cases.jsonl`.