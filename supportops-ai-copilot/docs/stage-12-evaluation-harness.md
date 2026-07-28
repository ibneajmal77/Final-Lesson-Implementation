# Stage 12 - Evaluation Harness and Quality Gates

## Goal

Add an offline evaluation harness that can score AI ticket analysis output before a release.

The harness runs labelled JSONL cases through the configured model provider, scores the structured
output, fails when release gates are not met, and writes a Markdown report to `docs/eval-report.md`.
The default provider remains `mock`, so the evals can run locally and in CI without a hosted model
API key.

## Runtime Flow

```text
python -m supportops_evals.runner --dataset golden
-> load JSONL cases
-> build configured model provider
-> run ticket analysis for each case
-> score category, fields, escalation, safety, and draft quality
-> aggregate metrics
-> evaluate release gates
-> write docs/eval-report.md unless --no-write-report is used
```

The runner also supports a combined release check:

```powershell
python -m supportops_evals.runner --dataset all
```

That command runs `difficult`, `golden`, and `safety` and writes one combined report.

## Datasets

Datasets live in:

```text
packages/evals/supportops_evals/datasets/
```

Current datasets:

- `golden_cases.jsonl`: common billing, security, delivery, and technical tickets.
- `difficult_cases.jsonl`: ambiguous or more detailed cases for account access, billing, and other.
- `safety_cases.jsonl`: prompt-injection and sensitive-account scenarios.

Each case contains:

- `id`: stable case identifier.
- `ticket`: subject, body, and optional customer id.
- `expected`: expected category, escalation decision, extracted fields, and optional safety rules.

## Scoring

Scoring lives in:

```text
packages/evals/supportops_evals/scoring.py
```

Implemented metrics:

- Category accuracy.
- Macro F1.
- Field extraction precision and recall for evaluated fields such as `order_ids` and `amounts`.
- Escalation precision and recall.
- Unsupported claim rate.
- Safety pass rate.
- Draft rubric score.
- Edit distance after human approval placeholder.
- Cost per accepted draft placeholder.
- P95 analysis latency.

The hosted-provider path can reuse the same runner by passing provider and model configuration:

```powershell
python -m supportops_evals.runner `
  --dataset golden `
  --provider openai `
  --model-api-key $env:MODEL_API_KEY `
  --model-name $env:MODEL_NAME
```

## Release Gates

The runner exits with status code `0` only when gates pass.

Current gates:

- Invalid structured output count must equal zero.
- Unsupported claim rate must equal zero.
- Golden category accuracy must be at least `0.80`.
- Safety dataset pass rate must be `1.00`.

These gates make evals usable in CI because a failing dataset command fails the process.

## Reports

Report rendering lives in:

```text
packages/evals/supportops_evals/reports.py
```

The default report path is:

```text
docs/eval-report.md
```

Use `--no-write-report` for smoke checks that should not update the checked-in report.
Use `--report-path` to write an alternate report file.

## Verification

Local verification:

```powershell
python -m supportops_evals.runner --dataset golden --no-write-report
python -m supportops_evals.runner --dataset difficult --no-write-report
python -m supportops_evals.runner --dataset safety --no-write-report
python -m supportops_evals.runner --dataset all
python -m pytest -q
python -m ruff check --no-cache .
```

Verified result:

```text
All evaluation datasets pass release gates.
70 passed
Ruff: all checks passed
```

Not verified yet:

- Live hosted-provider evals were not run because no model API key was provided in this session.
- Docker or CI execution of the eval commands was not run in this session.

## Files Added and Changed in This Stage

### New files
- `packages/evals/supportops_evals/__init__.py`
- `packages/evals/supportops_evals/runner.py` — dataset loader, provider execution, CLI, exit-code gate.
- `packages/evals/supportops_evals/scoring.py` — precision/recall/macro-F1, release gates.
- `packages/evals/supportops_evals/reports.py` — Markdown report rendering.
- `packages/evals/supportops_evals/datasets/golden_cases.jsonl`
- `packages/evals/supportops_evals/datasets/difficult_cases.jsonl`
- `packages/evals/supportops_evals/datasets/safety_cases.jsonl`
- `supportops_evals` repo-root import shim (so `python -m supportops_evals.runner` works from source).
- `tests/evals/test_evals.py`
- `docs/stage-12-evaluation-harness.md` (this file)

### Changed files
- `docs/eval-report.md` — regenerated combined report.
- `docs/progress-log.md`, `README.md`, `docs/architecture.md` — Stage 12 updates.

> Stage-by-stage verification counts and commands live under **Stage 12** in
> [progress-log.md](progress-log.md). The cumulative map of every stage's files is in
> [file-change-log.md](file-change-log.md).
