# Threat Model

Last updated: 2026-07-21

## Scope

This threat model covers the current SupportOps AI Copilot backend, worker, model gateway, prompt
package, database models, and observability helpers.

The current authentication model is still development-header based. Production OAuth/JWT identity,
secret rotation, and network policy are out of scope for this stage.

## Assets

Protected assets:

- tenant tickets and customer text
- tenant support policies
- AI recommendations and draft replies
- human review decisions
- model provider API keys
- logs, metrics, traces, and cost events
- database and Redis credentials

## Actors

Expected actors:

- support agents
- support leads
- tenant admins
- internal service workers
- hosted model provider

Potential attackers:

- unauthenticated callers
- users with the wrong role
- users from another tenant
- customers embedding prompt-injection text in tickets
- compromised or malformed hosted model responses
- operators accidentally logging PII or secrets

## Trust Boundaries

Primary trust boundaries:

- HTTP request headers to API actor identity
- API to database session
- API to Redis queue
- worker to database and model gateway
- model gateway to hosted provider
- application runtime to logs and metrics

Customer ticket text is always treated as untrusted input.

## Threats And Controls

| Threat | Control | Tests |
| --- | --- | --- |
| Missing authentication | `get_current_actor` requires tenant and user headers. | API security tests assert `401`. |
| Wrong role | Unknown roles are rejected with `403`; policy writes require lead/admin. | API security tests assert `403`. |
| Cross-tenant ticket access | Ticket repository lookups filter by actor tenant. | API security tests assert `404`. |
| Cross-tenant policy access | Policy repository lookups filter by actor tenant. | API security tests assert `404` and empty tenant lists. |
| Cross-tenant AI output approval | Approval route resolves ticket and recommendation under actor tenant before writing review. | API security tests assert `404`. |
| Prompt injection in customer text | Hosted prompt puts instructions above `UNTRUSTED_TICKET_TEXT_START`; tests include injection text. | API and hosted provider tests. |
| Model-selected tools or permissions | Prompt forbids tool/permission selection; strict schemas reject unknown fields. | Hosted provider tests reject `tool_calls`. |
| Unsupported evidence claims | Hosted provider validates evidence IDs against an allowlist. | Hosted provider tests reject unknown evidence IDs. |
| PII in logs | `redact_for_logs` masks emails, phone numbers, and payment-card-like values. | Observability tests. |
| Secrets in logs | JSON formatter redacts API-key and bearer-token patterns. | Observability tests. |
| Excessive provider data exposure | Hosted request uses `store: false` and sends only prompt, schema, ticket input, customer ID, and tenant policy context. | Hosted request tests and docs. |
| Retention drift | Tenant-owned records have `retention_expires_at`; worker stub counts expired rows. | DB and worker retention tests. |

## Hosted Provider Data Sharing

Hosted ticket analysis sends customer ticket subject, ticket body, optional customer ID, and
current-tenant support policy context to the configured model provider. The request also includes the
JSON output schema and prompt metadata.

It does not send database credentials, Redis credentials, raw logs, cross-tenant policy context,
review history, or cost history. The API key is sent only in the HTTP `Authorization` header.

## Residual Risks

Remaining risks after Stage 14:

- Development-header auth is not production-grade identity.
- Retention deletion is a dry-run/counting stub, not a destructive deletion workflow.
- Live hosted-provider calls still transmit ticket text to an external provider when enabled.
- There is no rate limiting, WAF, or abuse detection yet.
- There is no end-to-end secret scanning or dependency vulnerability gate yet.
- Prompt-injection controls reduce risk but do not prove every future model output will be safe.

These residual risks are candidates for Stage 15 CI/CD and later production hardening work.
