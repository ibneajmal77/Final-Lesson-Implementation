"""API schema modules."""

# ============================================================================
# FILE: apps/api/supportops_api/schemas/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code.
#
# WHAT A "SCHEMA" IS HERE: a strict description of a JSON shape, written as a
# Pydantic class. FastAPI uses them to do three jobs at once — validate incoming
# requests before any route code runs, generate the interactive API docs, and
# define exactly what may leave the application.
#
# THE FILES:
#   tickets.py   - creating and reading customer support requests
#   ai.py        - the AI's conclusions, and the job sheets for queued analysis
#   approvals.py - the human verdict form (approved / edited / rejected)
#   policies.py  - the company rulebook entries
#   metrics.py   - the shape of every number the /metrics endpoints return
#
# THE PATTERN REPEATED THROUGHOUT: separate "Create" and "Read" classes for the
# same thing. They are genuinely different shapes — when creating a ticket you
# must not be able to set its id or tenant_id, and when reading one back those
# must be present. Two classes make each rule impossible to get wrong.
# ============================================================================
