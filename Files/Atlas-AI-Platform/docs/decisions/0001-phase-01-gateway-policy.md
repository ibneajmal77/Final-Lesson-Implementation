# Phase 01 Gateway Policy Decisions

## Status

Accepted.

## Decisions

1. Identity tables use Phase 00 Option A.
   Phase 00 owns minimal `tenants` and `users` tables. Phase 01 keeps `ai_runs.tenant_id` non-null and does not defer tenant ownership.

2. `cost_records` are co-located with the Phase 01 gateway migration.
   `cost_records.ai_run_id` can reference `ai_runs(id)` immediately because both tables are created in `0002_model_gateway`. This makes P01-006 provable without waiting for a later audit migration.

3. Canonical route use cases are `chat`, `classification`, `rag_answer`, `embedding`, and `llm_judge`.
   Historical aliases such as `classifier` and `judge` are not stored.

4. Route mutation is bootstrap-only in Phase 01.
   Admin route mutation endpoints wait for RBAC and audit workflow work. The Phase 01 API exposes route listing and model test calls, not writes.

5. Fallback depth is one hop.
   A route may fall back once, and the fallback is revalidated against capability, budget, and data policy before use.

6. Input budget excess is rejected. Output cap excess is controlled by the route.
   Phase 01 does not silently truncate caller input. Reasoning budget requests beyond a route cap are rejected until Phase 20 adds richer reasoning routing.

7. Routes are read per request.
   Phase 01 does not cache routes in process. Later phases may add a short TTL plus explicit invalidation after route mutation exists.
