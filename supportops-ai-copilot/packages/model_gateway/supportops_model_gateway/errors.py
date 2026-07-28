# ============================================================================
# FILE: packages/model_gateway/supportops_model_gateway/errors.py
#
# THINK OF THIS FILE AS: the vocabulary for describing the different ways
# talking to an AI can go wrong.
#
# WHY FOUR SEPARATE ERROR TYPES INSTEAD OF ONE:
#   Because the four situations call for genuinely different responses, and code
#   catching them needs to tell them apart without inspecting error messages.
#   Look at how routes/tickets.py uses these — each maps to a different HTTP
#   status code, which is exactly the information a caller needs:
#
#     UnsupportedModelProviderError    -> 503. Our configuration is wrong.
#     ModelProviderConfigurationError  -> 503. Our configuration is wrong.
#     ModelProviderRequestError        -> 503. Couldn't reach them; retrying may help.
#     ModelProviderResponseError       -> 502. They answered with rubbish; retrying
#                                              probably won't help.
#
#   The 503/502 distinction is not pedantry. 503 says "temporarily unavailable,
#   come back shortly", and automated clients will retry on it. 502 says "the
#   service upstream is broken", and retrying a broken answer just wastes money.
#   Collapsing these into one error type would make that judgement impossible.
#
# WHY DEFINING YOUR OWN ERROR TYPES IS WORTH THE FILE:
#   The alternative is catching the AI library's own exceptions throughout the
#   application. That would spread knowledge of which library we use into route
#   files and worker code — so swapping providers would mean editing all of them.
#   Translating to our own vocabulary at the boundary keeps that knowledge inside
#   this package.
#
# A NOTE ON THE `pass` BODIES: an exception class needs no code. Its NAME is the
# information. `pass` simply means "nothing more to add here".
# ============================================================================


# The shared parent of the three "something went wrong while using a provider"
# errors.
#
# Having a common parent means code can catch broadly OR narrowly. The worker in
# apps/worker/jobs.py catches this one type and handles all three the same way,
# because it has nobody to answer and every case leads to the same action.
# routes/tickets.py catches the three children separately, because it must
# choose a different status code for each. Both are served by this hierarchy.
#
# It inherits from RuntimeError rather than plain Exception, which places it
# correctly among "things that went wrong while running" as opposed to
# programming mistakes like TypeError.
class ModelGatewayError(RuntimeError):
    """Base class for controlled model gateway failures."""


# Someone asked for a provider that does not exist — e.g. model_provider was set
# to "claude" when only "mock" and "hosted" are implemented.
#
# NOTE THIS ONE IS DIFFERENT: it inherits from ValueError, NOT from
# ModelGatewayError. That is a considered choice, not an oversight. The other
# three describe a provider failing while in use; this one means a bad VALUE was
# supplied before anything was attempted. It is closer to a typo in a settings
# file than to a service outage.
#
# The practical consequence is that catching ModelGatewayError does NOT catch
# this — which is why routes/tickets.py and jobs.py both list it explicitly
# alongside. Easy to overlook when adding a new call site.
class UnsupportedModelProviderError(ValueError):
    pass


# The provider exists, but we set it up wrong — most often a missing API key.
#
# Distinct from a request failure because retrying is pointless: the
# configuration will still be wrong in ten seconds. It usually indicates a
# deployment problem, such as an environment variable that was never set.
class ModelProviderConfigurationError(ModelGatewayError):
    pass


# We could not reach the provider, or it did not answer in time.
#
# The classic transient failure: network trouble, the service being down, or our
# timeout expiring. Retrying later is entirely reasonable, which is why this maps
# to 503 rather than 502.
class ModelProviderRequestError(ModelGatewayError):
    pass


# The provider answered, but with something unusable.
#
# In practice this means the model returned text that was not valid JSON, or JSON
# missing required fields. It happens more than newcomers expect: language models
# are asked to produce structured output but are not guaranteed to, so the
# response must always be validated rather than trusted.
#
# Separated from the request error because the meaning differs sharply. A request
# error means "we could not ask". This means "we asked, they replied, and the
# reply was no good" — which points at the prompt or the model rather than at the
# network, and which retrying identically is unlikely to fix.
class ModelProviderResponseError(ModelGatewayError):
    pass
