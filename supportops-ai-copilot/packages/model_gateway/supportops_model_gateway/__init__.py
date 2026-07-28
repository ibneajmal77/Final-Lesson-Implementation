"""Model gateway package for provider-neutral model access."""

# ============================================================================
# FILE: packages/model_gateway/supportops_model_gateway/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code.
#
# WHAT A "GATEWAY" IS AND WHY THE WHOLE PACKAGE EXISTS: everything about talking
# to an AI service is confined to this package. The rest of the application sends
# a TicketAnalysisInput, receives a TicketAnalysisResult, and has no idea whether
# a paid model or a hard-coded fake produced it.
#
# THREE THINGS THAT INDIRECTION BUYS:
#   1. The tests run free and offline, using the mock provider in place of the AI.
#   2. Switching providers is ONE SETTING — no route or worker code changes.
#   3. The blast radius is small: everything specific to one AI vendor lives in
#      one file.
#
# THE FILES:
#   providers/base.py   - the contract every provider must honour. No logic at all
#   providers/mock.py   - the fake, for tests and local development
#   providers/hosted.py - the real one, calling a paid service. The longest file,
#                         and almost all of it is defensive: an AI's reply is not
#                         guaranteed to be anything in particular
#   routing.py          - the switchboard: turns a setting into a provider object
#   errors.py           - the vocabulary for the different ways an AI call fails
#   cost.py             - tokens x price = money
#   client.py           - a convenience wrapper (currently unused by the app)
#
# START WITH providers/base.py. It is short, has no logic, and defines the shape
# everything else in this package is built around.
# ============================================================================
