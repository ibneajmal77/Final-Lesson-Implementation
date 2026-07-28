# Feedback-to-Eval Loop

Use this weekly during the pilot.

## Inputs

- `GET /metrics/pilot/feedback` for rejected and heavily edited drafts.
- `GET /metrics/pilot` for acceptance, edit distance, cost, safety, and exit decision.
- Review notes from agents.
- Current eval datasets in `packages/evals/supportops_evals/datasets`.

## Process

1. Pull rejected drafts weekly.
2. Pull heavily edited drafts weekly.
3. Cluster failure reasons by notes and ticket pattern.
4. Choose representative failures, not every duplicate failure.
5. Add those cases to `packages/evals/supportops_evals/datasets/difficult_cases.jsonl`.
6. Update the prompt template or model route in a versioned change.
7. Run `python -m supportops_evals.runner --dataset all --no-write-report`.
8. Release only if gates pass.
9. Record the change and result in `docs/progress-log.md` and `docs/eval-report.md` when reports are refreshed.

## Failure Clusters

Current automatic clusters are intentionally simple:

- `tone`
- `incorrect`
- `missing_context`
- `unsafe`
- `too_long`
- `unspecified`

These clusters are triage aids. A human should still read the ticket, draft, final reply, and notes before changing the eval dataset.

## Release Rule

A prompt or model route change should not ship because one example looked better manually. It should ship only when the changed system improves the relevant cases and still passes the full eval gate.