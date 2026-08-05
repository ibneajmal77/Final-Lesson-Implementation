---
document_key: admin-policy-v2
collection_id: admin_policies
source_type: synthetic
review_status: draft
effective_date: 2026-03-15
owner: platform_administration
---

# Admin Policy v2

## Suspension

Suspended accounts cannot export audit logs until an administrator restores access. The export button should remain hidden or disabled for suspended accounts.

A billing user cannot override suspension. Only an administrator with the `account.restore_access` permission can restore access for the tenant.

## Audit Log Export

Active enterprise tenants may export audit logs if the requester has the `audit_log.export` permission and the account is not suspended.

## Citation Rule

When answering whether a suspended account can export audit logs, cite this document and the Suspension section.