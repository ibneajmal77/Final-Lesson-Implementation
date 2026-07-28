# ============================================================================
# FILE: packages/evals/supportops_evals/reports.py
#
# THINK OF THIS FILE AS: the report writer. It takes the numbers the scorer
# produced and turns them into a readable Markdown document.
#
# WHY MARKDOWN RATHER THAN JSON OR A DASHBOARD:
#   Because the audience is people, and the places this lands are places people
#   already read: docs/eval-report.md in the repository, and the output of a CI
#   run. Markdown renders as formatted tables on GitHub while remaining perfectly
#   readable as plain text in a terminal — and it lives in version control, so
#   two runs can be compared with a plain diff.
#
#   That last point is the real value. "The prompt change moved category accuracy
#   from 0.82 to 0.79" shows up as a one-line diff, which is far harder to
#   overlook than a number on a dashboard nobody opened.
#
# THE REPORT'S STRUCTURE, top to bottom:
#   Summary      - pass or fail, and how many cases
#   Metrics      - two tables of numbers
#   Gates        - exactly which rules failed, if any
#   Case Results - a row per test case, so a failure can be traced to one ticket
#   Notes        - how to reproduce it
#
# The order is deliberate: the verdict first, the detail afterwards. Someone
# glancing at a CI run should learn pass-or-fail in the first two lines.
#
# WHY EVERY TYPE HERE IS `Any`:
#   This file deliberately knows nothing about the evaluation classes. It just
#   reads attributes off whatever it is given. That is a loose arrangement — a
#   renamed attribute would fail at runtime rather than being caught by the type
#   checker — chosen so the reporting layer never has to change when the
#   evaluation structures do.
# ============================================================================

from collections.abc import Sequence
from pathlib import Path
from typing import Any


# Renders one evaluation run.
# A thin wrapper over the multi-run version, so there is only one implementation
# to maintain.
def render_markdown_report(evaluation: Any) -> str:
    return _render_report([evaluation])


# Renders several runs into ONE report — the usual case, since the runner
# evaluates the golden, safety, and difficult datasets together.
#
# Combining them matters: seeing all three side by side is what reveals a change
# that improved accuracy while weakening safety, which is exactly the trade-off
# worth catching.
def render_markdown_reports(evaluations: Sequence[Any]) -> str:
    return _render_report(list(evaluations))


# Writes the report to a file.
#
# `parents=True` creates any missing folders in the path; `exist_ok=True` means
# an existing folder is fine rather than an error. Together they make this safe
# to call on a fresh checkout where docs/ may not exist yet.
#
# `encoding="utf-8"` is specified rather than left to the system default —
# necessary on Windows, where the default is still a legacy codepage and any
# non-ASCII character in a ticket would fail to write.
def write_markdown_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# Assembles the whole document.
#
# THE PATTERN HERE: a list of lines is built up, each section appending to it,
# and everything is joined at the end. Far more efficient than repeatedly
# concatenating strings — each concatenation would copy the entire document so
# far — and it keeps each section function small and independently readable.
def _render_report(evaluations: list[Any]) -> str:
    if not evaluations:
        return "# Evaluation Report\n\nNo evaluation runs were provided.\n"

    lines = ["# Evaluation Report", ""]
    _append_summary(lines, evaluations)
    _append_metrics(lines, evaluations)
    _append_gates(lines, evaluations)
    _append_case_results(lines, evaluations)
    _append_notes(lines)
    return "\n".join(lines)


# The headline section: the verdict, and the scale of the run.
def _append_summary(lines: list[str], evaluations: list[Any]) -> None:
    total_cases = sum(evaluation.metrics.total_cases for evaluation in evaluations)
    valid_cases = sum(evaluation.metrics.valid_cases for evaluation in evaluations)
    invalid_outputs = sum(evaluation.metrics.invalid_output_count for evaluation in evaluations)
    gate_status = "PASS" if _all_gates_passed(evaluations) else "FAIL"
    providers = sorted({evaluation.provider_name for evaluation in evaluations})

    lines.extend(["## Summary", ""])
    # Singular or plural wording depending on how many datasets ran. A small
    # courtesy that makes the report read as though written rather than generated.
    if len(evaluations) == 1:
        lines.append(f"- Dataset: `{evaluations[0].dataset}`")
    else:
        datasets = ", ".join(f"`{evaluation.dataset}`" for evaluation in evaluations)
        lines.append(f"- Datasets: {datasets}")
    lines.extend(
        [
            # The provider is recorded because a result means nothing without it:
            # a perfect score from the mock provider proves only that the fake
            # works. Anyone reading the report needs to see this immediately.
            f"- Provider: `{', '.join(providers)}`",
            # Bold, because it is the one line most readers will act on.
            f"- Gate status: **{gate_status}**",
            f"- Total cases: {total_cases}",
            f"- Valid cases: {valid_cases}",
            # Called out separately from the accuracy figures, since these are
            # calls that failed outright rather than answered wrongly.
            f"- Invalid structured outputs: {invalid_outputs}",
            "",
        ]
    )


# Two tables of numbers.
#
# Split into two rather than one wide table because a single table with eleven
# columns would scroll horizontally and become unreadable. The split is also
# meaningful: the first table is ACCURACY, the second is SAFETY AND COST.
def _append_metrics(lines: list[str], evaluations: list[Any]) -> None:
    lines.extend(
        [
            "## Metrics",
            "",
            "| Dataset | Cases | Category | Macro F1 | Field P/R | Escalation P/R |",
            # The Markdown separator row. The `---:` entries mean "align right",
            # which is what makes columns of numbers line up on their decimal
            # points and become comparable at a glance.
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for evaluation in evaluations:
        metrics = evaluation.metrics
        # Precision and recall are shown as a pair ("0.9000 / 0.8000") rather
        # than as separate columns, because neither means much alone — the
        # relationship between them is the information.
        lines.append(
            f"| `{evaluation.dataset}` | {metrics.total_cases} | "
            f"{_format_rate(metrics.category_accuracy)} | {_format_rate(metrics.macro_f1)} | "
            f"{_format_rate(metrics.field_precision)} / {_format_rate(metrics.field_recall)} | "
            f"{_format_rate(metrics.escalation_precision)} / "
            f"{_format_rate(metrics.escalation_recall)} |"
        )

    lines.extend(
        [
            "",
            "| Dataset | Unsupported claims | Safety | Draft | Cost | P95 latency ms |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for evaluation in evaluations:
        metrics = evaluation.metrics
        # Note the Cost column will read $0.0000 — cost_per_accepted_draft is a
        # placeholder that an offline evaluation cannot fill in. See scoring.py.
        lines.append(
            f"| `{evaluation.dataset}` | {_format_rate(metrics.unsupported_claim_rate)} | "
            f"{_format_rate(metrics.safety_pass_rate)} | "
            f"{_format_rate(metrics.draft_rubric_score)} | "
            f"${metrics.cost_per_accepted_draft:.4f} | {metrics.p95_latency_ms:.4f} |"
        )
    lines.append("")


# Which rules passed or failed, stated in words.
#
# The numbers above tell you WHAT happened; this tells you whether it is
# ACCEPTABLE, and names the specific rule broken. That is the difference between
# a developer seeing "0.79" and having to remember the threshold, and seeing
# "golden category accuracy must be at least 0.80".
#
# Passing datasets are listed too, not just failing ones — so the report shows
# the checks actually ran, rather than leaving silence to be read as success.
def _append_gates(lines: list[str], evaluations: list[Any]) -> None:
    lines.extend(["## Gates", ""])
    for evaluation in evaluations:
        metrics = evaluation.metrics
        if metrics.gate_failures:
            for failure in metrics.gate_failures:
                lines.append(f"- `{evaluation.dataset}` FAIL: {failure}")
        else:
            lines.append(f"- `{evaluation.dataset}` PASS: all configured gates passed")
    lines.append("")


# A row per test case — the section you scroll to when something failed.
#
# The aggregate numbers say "safety pass rate 0.95"; this says WHICH case failed,
# by ID, so you can open that exact ticket and look at it. Without this, a
# failing evaluation tells you there is a problem but not where.
def _append_case_results(lines: list[str], evaluations: list[Any]) -> None:
    lines.extend(
        [
            "## Case Results",
            "",
            "| Dataset | Case | Category | Escalation | Safety | Draft | Error |",
            "|---|---|---|---|---|---:|---|",
        ]
    )
    for evaluation in evaluations:
        for score in evaluation.case_scores:
            # PASS/FAIL rather than True/False. Deliberate: the words scan much
            # faster down a long column, and FAIL is visually distinct in a way
            # that "False" is not.
            category = "PASS" if score.category_correct else "FAIL"
            escalation = "PASS" if score.escalation_correct else "FAIL"
            safety = "PASS" if score.safety_passed else "FAIL"
            error = score.error or ""      # empty rather than "None" for the usual case
            lines.append(
                f"| `{evaluation.dataset}` | {score.case_id} | {category} | {escalation} | "
                f"{safety} | {score.draft_rubric_score:.2f} | {error} |"
            )
    lines.append("")


# The footer, and it earns its place by stating two things a reader needs:
#   1. HOW TO REPRODUCE THIS. Someone finding a surprising result should not have
#      to hunt for the command.
#   2. THAT THE DEFAULT RUN IS OFFLINE. Without this caveat, a reader could
#      easily take a perfect score as evidence the real AI is performing well,
#      when the mock provider produced it. Given that CI runs without an API key,
#      this warning is load-bearing.
def _append_notes(lines: list[str]) -> None:
    note = (
        "This report is generated by `python -m supportops_evals.runner`. The current "
        "implementation uses deterministic offline cases by default so it can run in CI "
        "without a hosted model API key."
    )
    lines.extend(["## Notes", "", note, ""])


# True only if EVERY dataset passed. `all(...)` is short-circuiting, so one
# failure is enough to fail the whole run — which is the correct standard when
# one of the datasets is the safety suite.
def _all_gates_passed(evaluations: list[Any]) -> bool:
    return all(evaluation.metrics.passed_gates for evaluation in evaluations)


# Formats every rate to exactly four decimal places.
#
# Fixed width, always — so 0.8000 and 0.7900 line up in a column and can be
# compared by eye. Trimming to "0.8" would break that alignment, and the
# consistency is worth more than the saved characters in a table meant for
# scanning.
def _format_rate(value: float) -> str:
    return f"{value:.4f}"
