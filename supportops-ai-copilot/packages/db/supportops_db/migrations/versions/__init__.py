"""Alembic migration versions."""

# ============================================================================
# FILE: packages/db/supportops_db/migrations/versions/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code.
#
# WHAT LIVES HERE: the numbered migration scripts. Each one records a single
# change to the database structure, and each names the one before it, forming a
# chain. Run them in order against an empty database and you arrive at the
# current schema.
#
# THE SEVEN, IN ORDER — and read together they are a decent history of how this
# project grew:
#   0001 - tenants, users, tickets            (the foundation)
#   0002 - ticket_recommendations             (analysis results, keyword rules only)
#   0003 - model_name, summary, suggested_reply columns   <- THE AI ARRIVES
#   0004 - recommendation_reviews             (human approval, added immediately
#                                              after the AI could write to customers)
#   0005 - ai_runs                            (job sheets: analysis becomes queued)
#   0006 - cost_events                        (someone asked what it was costing)
#   0007 - support_policies + retention dates (security and privacy)
#
# THE RULE THAT MATTERS MOST: never edit a migration that has already been
# applied anywhere. Those databases have recorded it as done and will not run it
# again, so your change would only affect databases built afterwards — leaving
# two installations with silently different schemas. Always add a new migration
# instead.
#
# Start with 0001, which explains the file format in detail.
# ============================================================================
