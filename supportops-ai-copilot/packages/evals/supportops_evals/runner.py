# ============================================================================
# FILE: packages/evals/supportops_evals/runner.py
#
# THINK OF THIS FILE AS: the exam invigilator. It loads the test tickets, puts
# each one to the AI, hands the answers to the marker, and writes the report.
#
# HOW TO RUN IT:
#   python -m supportops_evals.runner --dataset all
#   python -m supportops_evals.runner --dataset safety --provider hosted \
#          --model-api-key sk-...
#
# THE MOST IMPORTANT LINE IN THE FILE is the very last one:
#   return 0 if passed_gates else 1
#
#   A program's "exit code" is how it reports success to whatever ran it: 0 means
#   fine, anything else means failed. Because this returns 1 when a quality gate
#   fails, the CI pipeline (.github/workflows/ci.yml) treats a quality regression
#   exactly like a failing test — the build goes red and the change does not
#   ship.
#
#   That single line is what turns "we should evaluate our prompts" from an
#   intention into something enforced automatically.
#
# THE THREE DATASETS:
#   golden    - normal tickets with known-correct answers (accuracy)
#   difficult - ambiguous ones, often built from drafts humans rejected
#   safety    - adversarial ones, including attempts to hijack the instructions
#
# WHY IT DEFAULTS TO THE MOCK PROVIDER:
#   So it runs in CI with no API key, no network, and no cost, on every commit.
#   That makes it a genuine regression guard rather than something run
#   occasionally by hand. The trade-off is honest and stated in the report
#   itself: a mock run proves the machinery works and catches structural
#   breakage, but says nothing about a real model's quality. For that you pass
#   --provider hosted with a real key.
# ============================================================================

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from supportops_evals.reports import (
    render_markdown_report,
    render_markdown_reports,
    write_markdown_report,
)
from supportops_evals.scoring import (
    CaseScore,
    EvaluationMetrics,
    TicketEvalCase,
    aggregate_scores,
    invalid_case_score,
    score_case,
)
from supportops_model_gateway.providers.base import TicketAnalysisInput
from supportops_model_gateway.routing import build_ticket_analysis_provider
from supportops_observability.metrics import (
    record_eval_regression,
    record_prompt_injection_failure,
)

# Found relative to THIS file, so the command works from any directory.
DATASET_DIR = Path(__file__).parent / "datasets"

# The datasets are ".jsonl" — JSON Lines — one complete JSON object per line.
# Chosen over a single big JSON array for two practical reasons: a file can be
# read one case at a time without loading it all, and adding a case is a
# one-line diff in version control rather than a change that also touches the
# surrounding punctuation.
DATASET_FILES = {
    "golden": "golden_cases.jsonl",
    "difficult": "difficult_cases.jsonl",
    "safety": "safety_cases.jsonl",
}
# What --dataset will accept: the three names, plus "all".
DATASET_CHOICES = (*sorted(DATASET_FILES), "all")
DEFAULT_REPORT_PATH = Path("docs/eval-report.md")


# The complete result of evaluating one dataset.
@dataclass(frozen=True)
class EvaluationRun:
    dataset: str
    provider_name: str      # recorded because a score is meaningless without knowing
                            # whether a real model or the mock produced it
    case_scores: list[CaseScore]
    metrics: EvaluationMetrics


# Reads one dataset file into test cases.
def load_dataset(dataset: str, dataset_dir: Path = DATASET_DIR) -> list[TicketEvalCase]:
    dataset_file = DATASET_FILES.get(dataset)
    if dataset_file is None:
        # The error lists the valid options. A small thing that saves the reader
        # from going to look them up.
        choices = ", ".join(sorted(DATASET_FILES))
        raise ValueError(f"unknown dataset {dataset!r}; expected one of: {choices}")

    path = dataset_dir / dataset_file
    cases = []
    # `encoding="utf-8-sig"` handles a "byte order mark" — an invisible marker
    # some Windows editors put at the start of a file. Without the "-sig", that
    # marker would be read as part of the first line and JSON parsing of line 1
    # would fail with a baffling message. A real papercut on Windows, quietly
    # solved here.
    #
    # `start=1` makes line numbers human-style, so an error points at the line a
    # text editor would show.
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        if not line.strip():
            continue        # skip blank lines, so the file can be spaced for readability
        payload = json.loads(line)
        # The file and line number are passed down, so a malformed case produces
        # "golden_cases.jsonl:42: subject must be a non-empty string" rather than
        # an error with no indication of which of a hundred cases is at fault.
        cases.append(_case_from_payload(payload, source=f"{path}:{line_number}"))
    return cases


# Runs every case in ONE dataset.
def run_dataset(
    *,
    dataset: str,
    provider_name: str = "mock",     # free and offline by default
    model_api_key: str = "",
    model_name: str = "gpt-5.6",
    model_base_url: str = "https://api.openai.com/v1",
    timeout_seconds: float = 30.0,
    max_output_tokens: int = 1200,
) -> EvaluationRun:
    # The same factory the real application uses, so the evaluation exercises the
    # actual code path rather than a parallel one that could drift out of step.
    provider = build_ticket_analysis_provider(
        provider_name,
        api_key=model_api_key,
        model_name=model_name,
        base_url=model_base_url,
        timeout_seconds=timeout_seconds,
        max_output_tokens=max_output_tokens,
    )
    case_scores: list[CaseScore] = []
    latencies_ms: list[float] = []

    for case in load_dataset(dataset):
        started = time.perf_counter()
        try:
            result = provider.analyze_ticket(
                TicketAnalysisInput(
                    subject=case.subject,
                    body=case.body,
                    customer_id=case.customer_id,
                    # Note: no policy_context. Evaluation runs without company
                    # rules, so results are comparable across tenants and over
                    # time. The cost is that policy-following is not tested here.
                )
            )
            latencies_ms.append((time.perf_counter() - started) * 1000)
            case_scores.append(score_case(case, result))
        except Exception as exc:  # Evaluation should record model failure as invalid output.
            # CATCHING EVERYTHING IS RIGHT HERE, and unusual enough to explain.
            # One case failing must not abandon the run — the whole point is to
            # get a complete picture, including of the failures. A crash on case
            # 3 of 50 would tell you far less than a report showing exactly which
            # cases failed and why.
            #
            # The failure is recorded as an invalid output, which is an automatic
            # gate failure. So nothing is swallowed: the run completes AND the
            # build still goes red.
            #
            # The timing is recorded even on failure, so a provider that fails
            # slowly is distinguishable from one that fails instantly.
            latencies_ms.append((time.perf_counter() - started) * 1000)
            case_scores.append(invalid_case_score(case.id, f"{exc.__class__.__name__}: {exc}"))

    metrics = aggregate_scores(dataset=dataset, case_scores=case_scores, latencies_ms=latencies_ms)
    return EvaluationRun(
        dataset=dataset,
        provider_name=provider_name,
        case_scores=case_scores,
        metrics=metrics,
    )


# Runs all three datasets, in sorted order for a reproducible report.
def run_all_datasets(
    *,
    provider_name: str = "mock",
    model_api_key: str = "",
    model_name: str = "gpt-5.6",
    model_base_url: str = "https://api.openai.com/v1",
    timeout_seconds: float = 30.0,
    max_output_tokens: int = 1200,
) -> list[EvaluationRun]:
    return [
        run_dataset(
            dataset=dataset,
            provider_name=provider_name,
            model_api_key=model_api_key,
            model_name=model_name,
            model_base_url=model_base_url,
            timeout_seconds=timeout_seconds,
            max_output_tokens=max_output_tokens,
        )
        for dataset in sorted(DATASET_FILES)
    ]


# The command-line entry point.
def main(argv: list[str] | None = None) -> int:
    # `argparse` builds the command-line interface, and generates --help for free
    # from these definitions.
    parser = argparse.ArgumentParser(description="Run SupportOps AI Copilot evaluation datasets.")
    # `choices=` means a mistyped dataset name is rejected with a helpful message
    # before anything runs. `required=True` forces an explicit choice rather than
    # silently defaulting to one.
    parser.add_argument("--dataset", choices=DATASET_CHOICES, required=True)
    parser.add_argument("--provider", default="mock")
    parser.add_argument("--model-api-key", default="")
    parser.add_argument("--model-name", default="gpt-5.6")
    parser.add_argument("--model-base-url", default="https://api.openai.com/v1")
    # `type=` converts and validates the text from the command line, so
    # "--timeout-seconds abc" fails cleanly instead of crashing later.
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    parser.add_argument("--max-output-tokens", type=int, default=1200)
    parser.add_argument("--report-path", type=Path, default=DEFAULT_REPORT_PATH)
    # `action="store_true"` makes this a flag with no value: present means True.
    # Useful for trying something without overwriting the committed report.
    parser.add_argument("--no-write-report", action="store_true")
    args = parser.parse_args(argv)

    if args.dataset == "all":
        evaluations = run_all_datasets(
            provider_name=args.provider,
            model_api_key=args.model_api_key,
            model_name=args.model_name,
            model_base_url=args.model_base_url,
            timeout_seconds=args.timeout_seconds,
            max_output_tokens=args.max_output_tokens,
        )
        report = render_markdown_reports(evaluations)
        # ALL datasets must pass. One safety failure fails the whole run, however
        # well the others scored.
        passed_gates = all(evaluation.metrics.passed_gates for evaluation in evaluations)
    else:
        evaluation = run_dataset(
            dataset=args.dataset,
            provider_name=args.provider,
            model_api_key=args.model_api_key,
            model_name=args.model_name,
            model_base_url=args.model_base_url,
            timeout_seconds=args.timeout_seconds,
            max_output_tokens=args.max_output_tokens,
        )
        report = render_markdown_report(evaluation)
        passed_gates = evaluation.metrics.passed_gates

    # A failure is also recorded in the live metrics, so a regression is visible
    # on the monitoring dashboards and not only in whoever's CI log.
    if not passed_gates:
        failed_evaluations = evaluations if args.dataset == "all" else [evaluation]
        _record_failed_eval_metrics(failed_evaluations)

    if not args.no_write_report:
        write_markdown_report(args.report_path, report)
    # Printed as well as written, so a CI log shows the result inline without
    # anyone needing to fetch a file.
    print(report)

    # THE LINE THAT MAKES THIS A GATE. 0 = success, 1 = failure. CI reads this
    # and fails the build on 1.
    return 0 if passed_gates else 1


# Records a failed evaluation in the live Prometheus counters.
#
# The safety dataset gets extra treatment: each individual failing case bumps the
# prompt-injection counter. That granularity is deliberate — "the safety suite
# failed" is one alert, but "seven cases failed" tells you the scale of the
# problem, and this is a metric that should be alerted on aggressively.
def _record_failed_eval_metrics(evaluations: list[EvaluationRun]) -> None:
    for evaluation in evaluations:
        record_eval_regression(dataset=evaluation.dataset)
        if evaluation.dataset == "safety":
            for score in evaluation.case_scores:
                if not score.safety_passed:
                    record_prompt_injection_failure(dataset=evaluation.dataset)



# Converts one line of the dataset file into a test case, checking its shape.
#
# Validation matters here because these files are written BY HAND. A typo in a
# key name would otherwise produce a case that silently tests nothing — an
# expectation that never fires looks exactly like an expectation that passed,
# which is the worst possible failure mode for a test suite.
def _case_from_payload(payload: dict[str, Any], *, source: str) -> TicketEvalCase:
    case_id = _required_string(payload, "id", source=source)
    ticket = payload.get("ticket")
    expected = payload.get("expected")
    if not isinstance(ticket, dict):
        raise ValueError(f"{source}: ticket must be an object")
    if not isinstance(expected, dict):
        raise ValueError(f"{source}: expected must be an object")

    # customer_id is genuinely optional, so a missing or wrongly-typed value
    # quietly becomes None rather than failing the whole run.
    customer_id = ticket.get("customer_id")
    if not isinstance(customer_id, str):
        customer_id = None

    return TicketEvalCase(
        id=case_id,
        subject=_required_string(ticket, "subject", source=source),
        body=_required_string(ticket, "body", source=source),
        customer_id=customer_id,
        # `expected` is passed through unvalidated, deliberately: different
        # datasets assert different things, so there is no single correct shape.
        # scoring.py reads it defensively for that reason.
        expected=expected,
    )


# Reads a required text field, failing clearly if it is missing, the wrong type,
# or empty. `not value` catches the empty string, which would otherwise pass the
# type check while being useless as a subject or body.
def _required_string(payload: dict[str, Any], key: str, *, source: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{source}: {key} must be a non-empty string")
    return value


# `SystemExit` with main's return value is what actually sets the process exit
# code — the mechanism that lets CI see pass or fail. Simply calling main()
# without this would run the evaluation and then always report success,
# defeating the entire purpose of the gates.
if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
