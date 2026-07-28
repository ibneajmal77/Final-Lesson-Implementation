"""Domain services."""

# ============================================================================
# FILE: packages/domain/supportops_domain/services/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code.
#
# WHAT IS HERE: baseline.py, and nothing else.
#
# It holds classify_ticket() — the free, instant, deterministic keyword
# classifier. It has THREE distinct jobs in the running system, which is more
# than its size suggests:
#
#   1. The /baseline-analysis endpoint: the comparison point for judging the AI.
#   2. The pilot gate: routes/tickets.py uses it to work out a ticket's category
#      BEFORE deciding whether the AI is allowed to run. It has to be free and
#      instant, because it runs ahead of every AI call.
#   3. The mock provider's brain: providers/mock.py dresses its output up as if
#      an AI had produced it, which is how the whole test suite runs with no API
#      key and no network.
# ============================================================================
