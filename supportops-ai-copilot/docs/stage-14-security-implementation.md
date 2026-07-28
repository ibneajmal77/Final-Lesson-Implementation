# Stage 14 - Security Implementation

## Goal

Add security controls around tenant data, role-based access, prompt injection, logging, and data
retention before the project moves into CI/CD.

Stage 14 keeps the current development-header authentication model, but makes the expected security
rules explicit and covered by tests.

## Authentication and Roles

Development identity still comes from headers:

```text
X-Tenant-Id
X-User-Id
X-Role
```

The API rejects requests that do not include tenant and user headers with `401`.

Allowed roles are:

- `agent`
- `lead`
- `admin`
- `service`

Unknown roles return `403`. Support policy creation is stricter: only `lead` and `admin` can create
policy records.

Implementation:

```text
apps/api/supportops_api/dependencies.py
apps/api/supportops_api/routes/policies.py
```

## Tenant Isolation

Tenant boundaries are enforced in repository queries and route lookups. A caller can only load rows
that match the current actor's `tenant_id`.

Stage 14 adds tenant-scoped support policies:

```text
support_policies
```

Policy endpoints:

```text
POST /policies
GET /policies
GET /policies/{policy_id}
```

Cross-tenant access returns `404` instead of revealing that a row exists under another tenant.

The hosted and mock AI analysis paths now load policy context only for the current tenant before
calling the model provider.

Implementation:

```text
packages/db/supportops_db/repositories/policies.py
apps/api/supportops_api/routes/tickets.py
apps/worker/supportops_worker/jobs.py
```

## Prompt Injection Controls

The hosted prompt keeps system/developer-style instructions above the customer ticket text. Customer
text is marked as untrusted with explicit boundaries:

```text
UNTRUSTED_TICKET_TEXT_START
UNTRUSTED_TICKET_TEXT_END
```

The prompt tells the model not to obey ticket text that asks it to ignore instructions, reveal hidden
instructions, change the output format, or make unsupported promises.

The prompt also defines an evidence allowlist:

```text
ticket-subject
ticket-body
customer-id
policy-context
```

The model output is not allowed to choose tools, permissions, or actions outside the JSON schema.
This project does not execute model-selected tools.

Implementation:

```text
packages/prompts/supportops_prompts/templates/full_ticket_analysis.v1.md
packages/model_gateway/supportops_model_gateway/providers/hosted.py
```

## Hosted Output Validation

Hosted model output must pass local Pydantic validation before it can become a saved
recommendation. Prompt schemas forbid unknown fields, so unexpected tool calls or permission fields
are rejected.

Stage 14 adds hosted-provider evidence validation. If the model returns any evidence ID outside the
allowlist, the provider raises a controlled `ModelProviderResponseError`.

## Log Redaction

Structured logging now redacts common PII and secrets before JSON logs are emitted.

The helper is:

```text
redact_for_logs(text)
```

It masks:

- email addresses
- US-style phone numbers
- payment-card-like numbers
- common API key and bearer-token patterns

The JSON formatter applies redaction to messages, context fields, selected extra fields, and
exceptions.

Implementation:

```text
packages/observability/supportops_observability/logging.py
```

## Retention Hook

Stage 14 adds nullable `retention_expires_at` fields to tenant-owned data tables:

- `tickets`
- `ai_runs`
- `ticket_recommendations`
- `recommendation_reviews`
- `cost_events`
- `support_policies`

The worker package includes a deletion-job stub that counts expired records without deleting them by
default. This keeps the stage testable while leaving destructive deletion policy for a later
production hardening pass.

Implementation:

```text
apps/worker/supportops_worker/retention.py
packages/db/supportops_db/migrations/versions/0007_security_policies_and_retention.py
```

## What Is Sent To The Hosted Model Provider

When `MODEL_PROVIDER=openai` or `MODEL_PROVIDER=hosted`, the provider sends:

- the rendered `full_ticket_analysis.v1` prompt
- the strict JSON schema for the expected output
- ticket subject
- ticket body
- optional customer ID
- tenant-scoped support policy context
- request metadata containing prompt/schema identifiers

The request sets `store: false`.

The provider request does not include:

- database credentials
- Redis credentials
- `MODEL_API_KEY` in the JSON body
- application logs
- cross-tenant policy context
- review history
- cost event history

## Verification

Local verification commands:

```powershell
python -m ruff check --no-cache .
python -m pytest -q
python -m supportops_evals.runner --dataset all --no-write-report
docker compose config
git diff --check
```

Stage 14 security tests cover:

- cross-tenant ticket access
- cross-tenant policy access
- cross-tenant AI output approval
- missing authentication
- wrong role
- prompt injection in ticket text
- PII redaction in logs
- secret redaction in logs
- hosted output evidence allowlist validation
- hosted output rejection for unexpected tool/permission fields

## Files Added and Changed in This Stage

### New files
- `apps/api/supportops_api/routes/policies.py` — `POST/GET /policies`, `GET /policies/{id}`.
- `apps/api/supportops_api/schemas/policies.py` — policy request/response schemas.
- `packages/db/supportops_db/repositories/policies.py` — policy CRUD + `tenant_policy_context`.
- `packages/db/supportops_db/migrations/versions/0007_security_policies_and_retention.py`
- `apps/worker/supportops_worker/retention.py` — retention candidate counter (non-destructive stub).
- `docs/stage-14-security-implementation.md` (this file)
- `docs/threat-model.md`

### Changed files
- `packages/db/supportops_db/models.py` — `TenantPolicy` / `support_policies`; `retention_expires_at` columns on tenant-owned tables.
- `apps/api/supportops_api/dependencies.py` — role guard, `POLICY_WRITE_ROLES`.
- `apps/api/supportops_api/routes/tickets.py` — tenant-scoped policy context into analysis.
- `apps/worker/supportops_worker/jobs.py` — tenant-scoped policy context into analysis.
- `packages/model_gateway/supportops_model_gateway/providers/hosted.py` — evidence-ID allowlist validation.
- `packages/prompts/supportops_prompts/templates/full_ticket_analysis.v1.md` — untrusted-text boundaries, refusal rules.
- `packages/observability/supportops_observability/logging.py` — recursive PII/secret redaction.
- `tests/security/` — cross-tenant, auth, injection, redaction, evidence tests.
- `docs/progress-log.md`, `README.md`, `docs/architecture.md`, `docs/data-model.md` — Stage 14 updates.

> Stage-by-stage verification counts and commands live under **Stage 14** in
> [progress-log.md](progress-log.md). The cumulative map of every stage's files is in
> [file-change-log.md](file-change-log.md).
