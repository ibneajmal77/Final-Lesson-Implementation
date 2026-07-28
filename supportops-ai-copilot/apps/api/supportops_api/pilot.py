# ============================================================================
# FILE: apps/api/supportops_api/pilot.py
#
# THINK OF THIS FILE AS: the dimmer switch for the AI feature.
#
# It answers exactly one question: "is the AI allowed to run for THIS company,
# on THIS kind of ticket, right now?"
#
# WHY A DIMMER RATHER THAN AN ON/OFF SWITCH:
#   Turning a brand-new AI feature on for every customer at once is reckless.
#   If it writes something wrong, it writes it to everybody, at once, before
#   anyone notices. Instead this lets you start tiny — one friendly customer,
#   one low-risk ticket type like password resets — watch the approval rate for
#   a week, then widen it. That cautious rollout is what "pilot" means here,
#   and the results of ours are written up in docs/pilot-report.md.
#
#   It also gives you a kill switch. If the AI starts misbehaving at 2am, one
#   environment variable switches it off for everyone, with no code change and
#   no deployment. The rest of the app keeps working normally.
#
# THE THREE GATES, CHECKED IN ORDER (all must pass):
#   1. Is the AI on at all?              -> AI_ANALYSIS_ENABLED
#   2. Is this company in the pilot?     -> AI_ANALYSIS_ENABLED_TENANTS
#   3. Is this ticket type in the pilot? -> AI_ANALYSIS_ENABLED_CATEGORIES
#
# WHO USES IT:
#   routes/tickets.py - calls this before BOTH AI endpoints, via its own
#                       _require_ai_analysis_enabled helper, which turns a "no"
#                       from here into the right HTTP error code
#   settings.py       - defines the three settings being read
# ============================================================================

from dataclasses import dataclass

from supportops_api.settings import Settings


# The answer: yes or no, plus WHY when the answer is no.
#
# The reason is not decoration. routes/tickets.py acts on it, replying 503
# ("switched off for everyone, try later") for one case and 403 ("you're just
# not in the pilot group") for the others — genuinely different situations that
# deserve different answers. It also lands in the logs, so a support question
# of "why is the AI not working for me?" has a precise answer.
@dataclass(frozen=True)
class AIAnalysisEligibility:
    enabled: bool
    reason: str | None = None      # only set when enabled is False


# The decision itself.
#
# Note what this function does NOT do: no database, no network, no clock. Given
# the same inputs it always returns the same answer, which makes it trivial to
# test and impossible for it to fail or be slow. Deliberate — this runs before
# every single AI request, so it must never become a bottleneck.
def ai_analysis_eligibility(
    settings: Settings,
    *,                        # forces tenant_id and category to be named at the call site,
                              # since both are strings and would otherwise be easy to swap
    tenant_id: str,
    category: str,
) -> AIAnalysisEligibility:
    # GATE 1: the master switch. Checked first because it overrides everything
    # else — no point examining pilot lists if the whole feature is off.
    if not settings.ai_analysis_enabled:
        return AIAnalysisEligibility(enabled=False, reason="ai_analysis_disabled")

    # GATE 2: is this company on the list?
    #
    # The `if enabled_tenants and ...` is the important subtlety. An EMPTY list
    # means "no restriction — every company is allowed", not "no company is
    # allowed". That is what makes the setting optional: leave it blank and
    # this gate simply doesn't apply.
    #
    # Getting this backwards would be a nasty bug: an empty list treated as
    # "allow nobody" would silently switch the feature off for everyone the
    # moment someone cleared the setting.
    enabled_tenants = parse_csv_setting(settings.ai_analysis_enabled_tenants)
    if enabled_tenants and tenant_id.strip().lower() not in enabled_tenants:
        return AIAnalysisEligibility(enabled=False, reason="ai_analysis_tenant_not_enabled")

    # GATE 3: is this TYPE of ticket on the list? Same empty-means-all rule.
    #
    # This gate is what lets you say "the AI may handle password resets, but
    # keep it away from billing disputes" — limiting the blast radius by
    # subject matter rather than by customer.
    enabled_categories = parse_csv_setting(settings.ai_analysis_enabled_categories)
    if enabled_categories and category.strip().lower() not in enabled_categories:
        return AIAnalysisEligibility(enabled=False, reason="ai_analysis_category_not_enabled")

    # All three gates passed.
    return AIAnalysisEligibility(enabled=True)


# Turns a settings string like " Acme, Globex ,, Initech " into a clean set:
#   {"acme", "globex", "initech"}
#
# Settings arrive as one long line of text, so every entry needs tidying:
#   .strip()          - removes stray spaces around each entry
#   .lower()          - so "ACME" in the setting matches "acme" in the request.
#                       The comparisons above lower-case their side too, so both
#                       ends always agree.
#   if item.strip()   - throws away empty pieces, which is what stops a trailing
#                       comma from adding a blank "" entry to the set
#   frozenset(...)    - a set, so lookups are instant no matter how long the
#                       list grows; frozen so it can never be modified by accident
def parse_csv_setting(raw_value: str) -> frozenset[str]:
    return frozenset(item.strip().lower() for item in raw_value.split(",") if item.strip())
