"""Domain logic for the SupportOps AI Copilot."""

# ============================================================================
# FILE: packages/domain/supportops_domain/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code.
#
# WHAT "DOMAIN" MEANS: the business rules themselves, independent of any
# database, web framework, or AI service. Code here knows what a support ticket
# IS and how to judge one — and knows nothing about HTTP, SQL, or JSON.
#
# Keeping that separate matters because it can then be tested with no
# infrastructure at all, and reused by anything: the API, the worker, and the
# mock AI provider all call into it.
#
# WHAT IS ACTUALLY IN HERE: services/baseline.py, the keyword classifier — the
# deliberately simple, non-AI way of categorising a ticket.
#
# WHY A PROJECT ABOUT AI CONTAINS A NON-AI CLASSIFIER: it is the yardstick.
# Claiming an AI is worth its cost requires answering "worth it compared to
# what?", and the honest comparison is against the simplest thing that could
# work. If the expensive model cannot clearly beat keyword matching, it is not
# earning its keep. Every recommendation records which method produced it, so
# that comparison is always available in the metrics.
# ============================================================================
