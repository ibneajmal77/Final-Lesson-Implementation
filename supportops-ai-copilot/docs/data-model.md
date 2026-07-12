# Data Model

This document explains the current database tables.

## Tenants

`tenants` represent the customer or business-unit boundary.

Important columns:

- `id`: internal tenant identifier.
- `name`: display name.
- `slug`: stable short identifier.
- `created_at`: creation timestamp.

Why it matters:

- Later, every support ticket, user, AI output, and approval must belong to a tenant.
- Tenant boundaries prevent one customer or business unit from seeing another tenant's data.

## Users

`users` represent support agents, leads, admins, or service users.

Important columns:

- `id`: internal user identifier.
- `tenant_id`: the tenant this user belongs to.
- `email`: user email.
- `role`: current role such as agent, lead, admin, or service.
- `created_at`: creation timestamp.

Important constraint:

- `uq_users_tenant_email`: the same email cannot be duplicated inside one tenant.

## Tickets

`tickets` represent support requests from customers.

Important columns:

- `id`: internal ticket identifier.
- `tenant_id`: the tenant that owns the ticket.
- `external_id`: ID from an outside support system.
- `channel`: email, chat, web, phone, or API.
- `subject`: ticket title.
- `body`: full ticket text.
- `status`: open, pending, closed, or similar.
- `priority`: low, normal, high, urgent.
- `customer_id`: optional external customer ID.
- `metadata_json`: extra structured data.
- `created_at`: creation timestamp.
- `updated_at`: last update timestamp.

Important constraint:

- `uq_tickets_tenant_external_id`: one tenant cannot ingest the same external ticket twice.

Why the uniqueness includes `tenant_id`:

- Two different tenants may both have an external ticket named `123`.
- The pair `(tenant_id, external_id)` is unique, not `external_id` globally.

## Ticket Recommendations

`ticket_recommendations` represent saved machine-generated suggestions for a ticket.

Important columns:

- `id`: internal recommendation identifier.
- `tenant_id`: the tenant that owns the recommendation.
- `ticket_id`: the ticket this recommendation belongs to.
- `source`: producer name, such as `baseline_v1` or `mock_llm_v1`.
- `category`: predicted ticket category.
- `priority`: recommended priority.
- `requires_escalation`: whether a human escalation path should be triggered.
- `confidence`: recommendation confidence score from 0 to 1.
- `model_name`: optional model identifier for provider-generated recommendations.
- `prompt_version`: optional prompt or analysis contract version.
- `summary`: optional short summary of the customer issue.
- `suggested_reply`: optional draft reply for an agent to review.
- `extracted_fields_json`: structured data found in the ticket text.
- `reasons_json`: plain-language reasons explaining the recommendation.
- `created_at`: creation timestamp.

Why recommendations are separate from tickets:

- The baseline should not silently change the real ticket priority.
- Mock LLM, real LLM, retrieval, or human-reviewed recommendations can be stored beside the
  baseline.
- Keeping reasons and extracted fields makes the output auditable.

## Recommendation Reviews

`recommendation_reviews` represent human decisions on saved recommendations.

Important columns:

- `id`: internal review identifier.
- `tenant_id`: the tenant that owns the review.
- `ticket_id`: the ticket being reviewed.
- `recommendation_id`: the recommendation being reviewed.
- `reviewer_user_id`: the user who made the decision.
- `decision`: `approved`, `rejected`, or `edited`.
- `final_summary`: final reviewed summary, if used.
- `final_reply`: final reviewed reply, if used.
- `notes`: optional reviewer notes.
- `created_at`: creation timestamp.

Why reviews are separate from recommendations:

- The original AI output remains unchanged for audit and evaluation.
- Multiple review events can be stored over time.
- Approval, rejection, and edits become traceable business events.

## Review Metrics

Review metrics are derived from existing tables. Stage 8 does not add a new table.

Current metrics use:

- `ticket_recommendations` for total recommendations and source/category grouping.
- `recommendation_reviews` for approval, rejection, and edit counts.

Why this matters:

- The system can measure whether recommendations are actually useful.
- Future real LLM output can be compared against the baseline and mock provider.
- Low approval or high edit rates identify where prompts, rules, or retrieval need improvement.

## Current schema relationship

```text
tenants
  |-- users
  `-- tickets
      `-- ticket_recommendations
          `-- recommendation_reviews
```

This is enough for the next stage: measuring how often recommendations are accepted, rejected, or
edited.
