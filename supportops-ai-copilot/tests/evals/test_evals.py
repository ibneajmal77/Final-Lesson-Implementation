# ============================================================================
# FILE: tests/evals/test_evals.py
#
# THINK OF THIS FILE AS: the examiner and the door guard for AI quality.
#
# WHAT THIS TESTS: the evaluation pipeline in packages/evals/supportops_evals/:
#   runner.py  -> loads fixed examples and asks a model provider to analyse them
#   scoring.py -> compares each answer with the expected facts and safety rules
#   reports.py -> turns those results into a Markdown report a person can read
#
# An evaluation, shortened to eval, is a repeatable exam for the AI. Unlike a
# normal unit test with one exact string answer, it measures rates such as
# category accuracy and checks hard gates. A GATE is a minimum standard: if it
# fails, runner.py returns exit code 1 and .github/workflows/ci.yml blocks the
# change from merging.
#
# EVALUATION FLOW:
#   fixed JSONL cases in packages/evals/supportops_evals/datasets/
#     -> load_dataset creates TicketEvalCase objects
#       -> the model gateway analyses each ticket
#         -> score_case compares expected and actual behaviour
#           -> aggregate_scores applies release-blocking gates
#             -> reports.py writes the evidence to a Markdown file
#
# JSONL means JSON Lines: one complete JSON object per line. The data files have
# no comments because JSON does not allow them. Their purpose and expectations
# are documented here and in runner.py instead.
#
# The tests use the deterministic mock provider from packages/model_gateway/.
# That keeps them free, fast, and offline. It also means they cannot prove a
# hosted model still behaves well today; a real-provider evaluation must be run
# separately before trusting a model or prompt change.
#
# WHO USES IT / WHAT LIVES HERE: CI calls supportops_evals.runner; the generated
# report is consumed by reviewers deciding whether AI quality is safe to ship.
# ============================================================================
from pathlib import Path

from supportops_evals.reports import render_markdown_report, write_markdown_report
from supportops_evals.runner import load_dataset, main, run_dataset
from supportops_evals.scoring import aggregate_scores, score_case
from supportops_model_gateway.providers.base import TicketAnalysisResult


# The loader test checks the boundary between hand-written JSONL and Python.
# The golden set is the ordinary-accuracy dataset: representative tickets with
# answers the team has agreed are correct. A non-empty subject and expected
# category are the minimum pieces needed for a meaningful classification case.
#
# The at-least-three check leaves room to add cases without changing this test.
# The ID prefix is a naming convention that keeps cases identifiable when all
# datasets are combined into one report. This samples the first case; runner.py
# performs the full structural validation for every line.
def test_load_golden_dataset() -> None:
    cases = load_dataset("golden")

    assert len(cases) >= 3
    assert cases[0].id.startswith("golden_")
    assert cases[0].subject
    assert cases[0].expected["category"]


# Tests the marker independently from any provider. TicketAnalysisResult is the
# same structured answer returned through packages/model_gateway/, but building
# one directly makes each expected comparison visible and removes model noise.
#
# Extracted fields become sets of (field name, value) pairs so order and list
# layout cannot create a false mismatch. An unsupported claim is a promise not
# backed by ticket evidence, such as inventing that a refund was issued.
# A draft-rubric score of 1.0 means this small reply meets every programmed rule;
# it is not proof that every human would consider the prose perfect.
def test_score_case_detects_category_fields_and_escalation() -> None:
    case = load_dataset("golden")[0]
    result = TicketAnalysisResult(
        source="test",
        model_name="test-model",
        prompt_version="test-prompt",
        category="billing",
        priority="high",
        requires_escalation=False,
        confidence=0.9,
        summary="Customer reported a billing issue.",
        suggested_reply="Thanks for reaching out. I will review the billing details.",
        extracted_fields={"order_ids": ["ORD-123"]},
        reasons=["matched billing"],
    )

    score = score_case(case, result)

    assert score.category_correct is True
    assert score.escalation_correct is True
    assert score.expected_fields == {("order_ids", "ORD-123")}
    assert score.actual_fields == {("order_ids", "ORD-123")}
    assert score.unsupported_claims == []
    assert score.draft_rubric_score == 1.0


# This is the small end-to-end evaluation test: load all four golden cases, run
# the same provider factory used by the application, score the answers, and
# apply the gates. The mock provider is deterministic, meaning identical input
# always produces identical output, so a failure indicates code or dataset drift
# rather than a changing remote service.
#
# The exact count intentionally makes adding or losing a golden case visible.
# Accuracy may be imperfect down to 80 percent, but malformed model output is
# never allowed; passed_gates combines those rules into the CI verdict.
def test_run_golden_dataset_with_mock_provider_passes_gates() -> None:
    evaluation = run_dataset(dataset="golden", provider_name="mock")

    assert evaluation.metrics.total_cases == 4
    assert evaluation.metrics.invalid_output_count == 0
    assert evaluation.metrics.category_accuracy >= 0.8
    assert evaluation.metrics.passed_gates is True


# The safety dataset contains hostile or risky requests rather than routine
# support questions. Every case must pass: a safety rate of 99 percent still
# means one unsafe customer interaction. Zero unsupported claims also prevents
# a polite-looking refusal from quietly inventing facts or promises.
#
# As above, this proves the local mock and scoring rules agree. It does not
# replace periodically challenging the configured hosted model with this set.
def test_run_safety_dataset_with_mock_provider_passes_safety_gate() -> None:
    evaluation = run_dataset(dataset="safety", provider_name="mock")

    assert evaluation.metrics.total_cases == 2
    assert evaluation.metrics.safety_pass_rate == 1.0
    assert evaluation.metrics.unsupported_claim_rate == 0.0
    assert evaluation.metrics.passed_gates is True


# Guards the empty-run edge case. With no scored cases, the category ratio helper
# returns 0 rather than dividing by zero, and the golden 80-percent gate still
# fails closed. In other words, running no exam cannot be reported as success.
#
# CANDOUR: the test name says invalid output, but an empty score list produces an
# invalid_output_count of zero. The assertion actually proves the category gate
# fails on an empty dataset; it does not exercise invalid_case_score. Renaming
# would be clearer, but this task deliberately changes comments only.
def test_aggregate_scores_fails_gate_on_invalid_output() -> None:
    metrics = aggregate_scores(
        dataset="golden",
        case_scores=[],
        latencies_ms=[],
    )

    assert metrics.passed_gates is False
    assert "golden category accuracy must be at least 0.80" in metrics.gate_failures


# Checks both halves of reports.py: rendering text in memory and writing that
# exact text to disk. tmp_path is a pytest FIXTURE, a ready-made test resource
# supplied through the function argument. It is a fresh temporary directory for
# this test and pytest removes it later, so no real report is overwritten.
#
# The heading checks pin the human-facing structure while the final equality
# proves the writer did not alter encoding or content. This does not ask a
# Markdown renderer to display the file; it verifies the source text contract.
def test_render_and_write_markdown_report(tmp_path: Path) -> None:
    evaluation = run_dataset(dataset="difficult", provider_name="mock")
    report = render_markdown_report(evaluation)
    path = tmp_path / "eval-report.md"

    write_markdown_report(path, report)

    assert "# Evaluation Report" in report
    assert "Dataset: `difficult`" in report
    assert "Gate status" in report
    assert path.read_text(encoding="utf-8") == report

# Exercises the command-line entry point without launching a second Python
# process. Passing an argument list is equivalent to the named CLI flags, and
# the default mock provider runs difficult, golden, and safety in sorted order.
#
# capsys is another pytest fixture. It captures text printed to the console so
# the test output stays quiet; readouterr consumes that captured output. The
# test then checks the more durable report file and the process-style exit code:
# zero means every gate passed, while runner.py returns one on any regression.
#
# Pinning all three names also catches an accidentally omitted dataset. It does
# not inspect every metric in the combined report; earlier tests cover scoring.
def test_runner_all_dataset_writes_combined_report(tmp_path: Path, capsys) -> None:
    path = tmp_path / "eval-report.md"

    exit_code = main(["--dataset", "all", "--report-path", str(path)])
    capsys.readouterr()

    report = path.read_text(encoding="utf-8")
    assert exit_code == 0
    assert "Datasets: `difficult`, `golden`, `safety`" in report
    assert "`golden` PASS: all configured gates passed" in report
    assert "`safety` PASS: all configured gates passed" in report
