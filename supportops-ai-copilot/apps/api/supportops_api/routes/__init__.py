"""API route modules."""

# ============================================================================
# FILE: apps/api/supportops_api/routes/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code; see the note in the parent package's __init__.py.
#
# WHAT LIVES HERE: the endpoints, grouped by subject. Each file defines a
# `router` object, and main.py plugs all five into the application.
#
#   health.py    - GET /health, GET /ready. Liveness and readiness, for machines
#   tickets.py   - the biggest one: create and read tickets, plus the THREE ways
#                  to analyse them (baseline, synchronous AI, queued AI)
#   approvals.py - the human sign-off on AI drafts. The product's safety step
#   policies.py  - the per-company written rules fed to the AI
#   metrics.py   - the scoreboard: quality, cost, and the pilot verdict
#
# A pattern shared by all five: they never write SQL themselves. Every database
# access goes through packages/db/supportops_db/repositories/, which keeps the
# queries in one place and the tenant filtering impossible to forget.
# ============================================================================
