"""Database repository modules."""

# ============================================================================
# FILE: packages/db/supportops_db/repositories/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code.
#
# WHAT A "REPOSITORY" IS: every file here follows one rule — ALL database
# queries live in this folder and nowhere else. Route files, the worker, and the
# scripts never write SQL; they call one of these functions.
#
# THREE THINGS THAT BUYS:
#   1. One place to look. Wondering how tickets are fetched? It is in
#      tickets.py, not scattered across five route handlers.
#   2. Security you cannot forget. tenant_id is a REQUIRED argument on these
#      functions, so it is impossible to write a query that omits the filter
#      keeping one company's data away from another's.
#   3. Testability. Routes can be tested without a database at all.
#
# THE FILES:
#   tenants.py         - companies and their people
#   tickets.py         - customer support requests
#   recommendations.py - what an analysis concluded
#   approvals.py       - human verdicts on AI drafts
#   ai_runs.py         - job sheets for queued analysis, and their state changes
#   policies.py        - company rules, plus the function that formats them for the AI
#   cost_events.py     - recording and totalling AI spending
#   metrics.py         - the counting queries behind the quality scoreboard
#   pilot.py           - the rollout verdict: expand, iterate, stop, or roll back
#
# ONE CONVENTION SHARED BY ALL OF THEM: they call session.flush() but NEVER
# session.commit(). Committing is left to the caller, which is what lets a route
# save several related rows and have them succeed or fail together as one unit.
# ============================================================================
