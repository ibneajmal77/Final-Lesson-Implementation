"""Evaluation package for SupportOps AI Copilot."""

# ============================================================================
# FILE: packages/evals/supportops_evals/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code.
#
# THIS IS THE REAL EVALUATION PACKAGE. Do not confuse it with the folder of the
# same name at the repository root, which is only an import shim pointing here.
#
# WHAT AN "EVALUATION" IS AND WHY IT MATTERS: a fixed set of test tickets with
# known correct answers, run BEFORE anything ships. Change a prompt, run the
# evaluation, and see immediately whether quality went up or down. Without it,
# "we improved the prompt" is an opinion rather than a measurement.
#
# THE FILES:
#   runner.py   - loads the datasets, calls the AI, writes the report. Its exit
#                 code is what makes CI fail on a quality regression
#   scoring.py  - the marker: accuracy, safety, and the GATES that block a release
#   reports.py  - turns the numbers into a readable Markdown document
#   datasets/   - the test tickets themselves, one JSON object per line
#
# THE THREE DATASETS:
#   golden    - normal tickets with known answers          (accuracy)
#   difficult - ambiguous ones, often built from drafts humans rejected
#   safety    - adversarial ones, including attempts to hijack the instructions
#
# THE IDEA WORTH TAKING AWAY — GATES. Certain results fail automatically
# regardless of how good everything else looks: any unsupported claim, any
# invalid output, any safety failure. CI refuses to ship on a gate failure, which
# turns "we should be careful about AI safety" into something the build enforces
# rather than something people remember.
# ============================================================================
