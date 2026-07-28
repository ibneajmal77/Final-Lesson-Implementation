# ============================================================================
# FILE: apps/api/supportops_api/schemas/policies.py
#
# THINK OF THIS FILE AS: the form for writing a company rule, and the shape you
# get back when reading one.
#
# A reminder of what these rules are (routes/policies.py has the full story):
# plain-English instructions like "never promise a refund over $100", which get
# pasted into the question sent to the AI so it can read them before drafting a
# reply.
#
# USED BY: routes/policies.py
# ============================================================================

from datetime import datetime

from pydantic import BaseModel, Field


# --- GOING IN: writing a new rule ------------------------------------------
class SupportPolicyCreate(BaseModel):
    # A short label, e.g. "refund-limits" or "tone-of-voice". Used to identify
    # the rule at a glance in a list.
    name: str = Field(min_length=1, max_length=200)

    # The rule itself, in plain English. This exact text is what gets placed
    # into the AI's instructions.
    #
    # The 10,000-character limit is doing more than preventing storage bloat.
    # Every character here is sent to the AI on EVERY ticket analysis for this
    # company, and AI services charge by the amount of text. A bloated rulebook
    # is therefore a recurring bill on every single request. It also crowds out
    # the model's attention: a rule buried in ten pages of text is far more
    # likely to be overlooked than one in a short, sharp list.
    content: str = Field(min_length=1, max_length=10000)

    # Optional expiry date. Once it passes, the cleanup job in
    # apps/worker/retention.py deletes the rule.
    #
    # This exists because temporary rules are dangerous when forgotten. "During
    # the December sale, allow free returns" would otherwise keep instructing
    # the AI the following June, with nobody remembering it was ever added.
    # Leave it as None for a permanent rule.
    retention_expires_at: datetime | None = None


# --- COMING OUT: reading a rule back ---------------------------------------
class SupportPolicyRead(BaseModel):
    id: str
    tenant_id: str          # rules are per-company; nobody sees another company's

    name: str
    content: str

    # Who wrote it. Recorded because these rules directly steer what the AI
    # tells customers, so "who added this instruction, and when?" is a question
    # that will eventually be asked.
    created_by_user_id: str
    created_at: datetime
    updated_at: datetime

    retention_expires_at: datetime | None = None
