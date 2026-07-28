"""Shared observability helpers."""

# ============================================================================
# FILE: packages/observability/supportops_observability/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code.
#
# WHAT "OBSERVABILITY" MEANS: the ability to look at a running system and
# understand what it is doing. Not a feature users see — it is what makes the
# difference between "the app is slow" being a mystery and being a question you
# can answer in two minutes.
#
# THE THREE PILLARS, one file each:
#
#   logging.py - LOGS: what happened, as machine-readable JSON. It also does the
#                more important job of REDACTING personal data and secrets from
#                every line before it is written — email addresses, phone
#                numbers, card numbers, API keys. That matters because this app
#                handles support tickets, and logs get copied into search
#                systems and kept for months.
#
#   metrics.py - NUMBERS: live counters (tickets created, analyses failed, money
#                spent) held in memory and scraped by Prometheus. They reset on
#                restart, which is fine — Prometheus keeps the history.
#
#   tracing.py - TIMELINES: how long each step of a request took, nested. This is
#                what shows you WHICH part is slow, including across the API and
#                worker boundary.
#
#   model_usage.py - the joint between all of the above and the database: records
#                what one AI call cost, in both the permanent cost_events table
#                AND the live counters.
#
# A DESIGN PRINCIPLE VISIBLE IN ALL OF THEM: instrumentation must never break the
# thing it observes. tracing.py works fine if the tracing library is absent;
# _set_attributes accepts values of any type rather than raising; missing token
# counts degrade to zero rather than failing an otherwise successful analysis.
# ============================================================================
