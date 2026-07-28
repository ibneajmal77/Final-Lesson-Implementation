# Pilot Report

This report describes the current pilot instrumentation and decision rules. It does not contain live production pilot results.

## Active Local Pilot Scope

```text
AI_ANALYSIS_ENABLED=true
AI_ANALYSIS_ENABLED_TENANTS=tenant_demo
AI_ANALYSIS_ENABLED_CATEGORIES=billing
```

The initial category is billing because duplicate charge and refund tickets are easy to validate, common in support workflows, and already covered by the baseline, mock provider, hosted provider contract, eval datasets, smoke test, and agent review path.

## Metrics

| Metric | Source | Use |
| --- | --- | --- |
| Draft acceptance rate | `recommendation_reviews` | Measures approved or edited AI drafts divided by reviewed AI drafts. |
| Average edit distance | `recommendation_reviews` and `ticket_recommendations` | Estimates how much agents change accepted drafts. |
| Time to first response | ticket creation time and first review time | Tracks pilot speed from ticket intake to human action. |
| Escalation accuracy | escalation flag and review decision | Checks whether escalated drafts are accepted by agents. |
| Cost per accepted draft | `cost_events` and accepted reviews | Connects model spend to useful drafts. |
| Safety failures | failed `ai_runs` error codes | Surfaces safety, prompt-injection, evidence, or privacy failures. |
| Agent rejection reasons | review notes | Shows why agents rejected drafts. |

## Exit Decisions

- `expand`: at least five reviewed drafts, acceptance rate is at least 80 percent, edit distance is low, and no safety failures are present.
- `iterate`: data is insufficient or quality needs improvement before expansion.
- `roll_back`: safety failures were detected.
- `stop`: draft acceptance is too low for the current pilot scope.

## Current Local Status

The local dataset is synthetic. After the Stage 18 smoke run, `GET /metrics/pilot` returned a billing-only `tenant_demo` report with 4 reviewed drafts, 4 accepted drafts, no rejected drafts, no safety failures, and `iterate` as the exit decision because at least five reviewed drafts are required before expansion.

`GET /metrics/pilot/feedback` returned no current feedback candidates and recommended continuing to collect pilot reviews.

The weekly improvement loop should use `GET /metrics/pilot/feedback` to identify rejected and heavily edited drafts before adding representative cases to the difficult eval dataset.