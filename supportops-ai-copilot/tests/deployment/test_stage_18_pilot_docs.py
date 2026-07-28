# ============================================================================
# FILE: tests/deployment/test_stage_18_pilot_docs.py
#
# THINK OF THIS FILE AS: the checklist beside a cautious AI trial's playbook.
#
# WHAT THIS TESTS: that the stage-18 pilot guide, feedback-loop guide, and pilot
# report still document rollout limits, measurements, evaluation steps, and the
# allowed decisions at the end of the trial.
#
# A PILOT is a deliberately small real-world release. Here the AI is enabled for
# selected tenant companies and ticket categories, while a human still reviews
# every draft. The goal is to gather evidence before exposing more traffic.
#
# WHERE THIS SITS IN THE IMPROVEMENT LOOP:
#   apps/api/supportops_api/pilot.py decides which tickets may use AI
#     -> routes/metrics.py and repositories/pilot.py report cost and review data
#       -> rejected or heavily edited drafts reveal failure patterns
#         -> packages/evals/ turns those patterns into repeatable test cases
#           -> the team expands, iterates, rolls back, or stops the pilot
#
# A QUALITY GATE is a pass/fail threshold that prevents a weaker prompt or model
# from shipping. A DATASET is the fixed collection of example tickets and
# expected outcomes scored by that gate.
#
# TESTING APPROACH: these tests treat Markdown documents as operational
# contracts. They make it difficult to remove a required switch, metric, command,
# or decision word without the normal pytest run drawing attention to the change.
#
# HONEST LIMITATION: keyword presence does not prove the prose is correct,
# internally consistent, or followed by operators. These tests do not calculate
# pilot metrics, inspect real review data, or run an evaluation. In particular,
# they cannot prove repositories/pilot.py scales to production data or that every
# edited draft is counted correctly; implementation and integration tests must
# cover those concerns.
#
# No pytest FIXTURE is needed. A fixture is reusable test setup; each test simply
# reads one committed document through Python's Path helper.
#
# WHO USES IT / WHAT LIVES HERE: docs/stage-18-pilot-improvement-loop.md defines
# rollout and decision rules; docs/feedback-to-eval-loop.md turns human feedback
# into eval cases; docs/pilot-report.md records the outcome; supportops_evals/runner.py
# executes the quality gates named in those documents.
# ============================================================================
from pathlib import Path


# The main guide must connect three concerns that are easy to separate by
# accident: limiting exposure, measuring results, and making an explicit decision.
def test_stage_18_doc_maps_to_pilot_guide_requirements() -> None:
    doc = Path("docs/stage-18-pilot-improvement-loop.md").read_text(encoding="utf-8")

    # The first two values are environment-variable controls read by settings.py
    # and applied by pilot.py. They restrict companies and ticket categories.
    for expected in (
        "AI_ANALYSIS_ENABLED_TENANTS",
        "AI_ANALYSIS_ENABLED_CATEGORIES",
        # These HTTP endpoints expose summary metrics and review-level feedback.
        "GET /metrics/pilot",
        "GET /metrics/pilot/feedback",
        # Acceptance says how often drafts are approved. EDIT DISTANCE measures
        # how much wording changed between the AI draft and the reviewed result.
        "Draft acceptance rate",
        "Average edit distance",
        # Cost only has value in context: this ratio asks what each accepted draft
        # costs, while safety failures remain a separate stop signal.
        "Cost per accepted draft",
        "Safety failures",
        # Every review period must end with one of four named actions rather than
        # the vague and risky default of letting the experiment continue.
        "expand",
        "iterate",
        "roll_back",
        "stop",
    ):
        # Exact, case-sensitive containment makes these terms a documentation
        # contract, but it does not prove they occur under the right heading.
        assert expected in doc


# Human review is valuable twice: it protects customers immediately and produces
# examples that can prevent the same model mistake in a future release.
def test_feedback_loop_doc_contains_weekly_eval_steps() -> None:
    doc = Path("docs/feedback-to-eval-loop.md").read_text(encoding="utf-8")

    # This table describes the intended weekly feedback-to-evaluation loop.
    for expected in (
        # Rejections and large edits are the clearest evidence that a draft failed.
        "Pull rejected drafts weekly",
        "Pull heavily edited drafts weekly",
        # Clustering means grouping similar failures so one root cause can become
        # a focused regression example rather than many unrelated anecdotes.
        "Cluster failure reasons",
        # JSONL means JSON Lines: one complete JSON object per line. The difficult
        # dataset stores ambiguous or previously mishandled tickets in that form.
        "difficult_cases.jsonl",
        # The next command runs golden, difficult, and safety cases without
        # rewriting the checked-in Markdown report as a side effect.
        "Run `python -m supportops_evals.runner --dataset all --no-write-report`",
        # A release should proceed only when measurable thresholds still pass.
        "Release only if gates pass",
    ):
        # As above, this proves the required phrase exists, not that operators
        # perform the steps in this order or on the stated weekly schedule.
        assert expected in doc


# A pilot report should end in an operational choice, not merely present numbers.
# "billing" also anchors the report to the deliberately narrow first category.
def test_pilot_report_documents_exit_decisions() -> None:
    doc = Path("docs/pilot-report.md").read_text(encoding="utf-8")

    # One compact loop enforces the same vocabulary used by the main pilot guide.
    # It does not verify which decision was selected or whether evidence supports it.
    for expected in ("expand", "iterate", "roll_back", "stop", "billing"):
        assert expected in doc
