"""Model provider implementations."""

# ============================================================================
# FILE: packages/model_gateway/supportops_model_gateway/providers/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code.
#
# WHAT IS HERE: one contract, and two things that honour it.
#
#   base.py   - the CONTRACT. Defines what goes into an analysis and what must
#               come out, and nothing else. No logic, which is what makes it safe
#               for everything else to depend on.
#   mock.py   - THE FAKE. Runs the free keyword classifier and dresses the result
#               up as if an AI had produced it. No network, no cost, and the same
#               answer every time — which is what lets the whole test suite run
#               offline and makes assertions possible at all.
#   hosted.py - THE REAL ONE. The only place in the entire project that makes an
#               HTTP request to a paid AI service.
#
# HOW THEY CAN BE INTERCHANGEABLE: base.py defines a Protocol, which describes a
# SHAPE rather than demanding inheritance. Anything with an `analyze_ticket`
# method counts as a provider — including a three-line throwaway class in a test.
#
# WHY hosted.py IS SO MUCH LONGER THAN mock.py: because a language model's reply
# is not guaranteed to be valid JSON, complete, or even an answer — it might be a
# refusal, or truncated halfway. Nearly all of that file is checking for those
# cases and turning each into a clear error rather than a crash or, worse, a
# plausible-looking wrong result.
# ============================================================================
