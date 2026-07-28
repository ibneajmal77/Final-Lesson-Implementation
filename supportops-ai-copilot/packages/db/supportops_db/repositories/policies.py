# ============================================================================
# FILE: packages/db/supportops_db/repositories/policies.py
#
# THINK OF THIS FILE AS: the database queries for a company's written rules —
# plus, at the bottom, the function that turns those rules into text the AI
# actually reads.
#
# That last function is the interesting one. The first three are routine
# create/read queries like the other repositories; tenant_policy_context() is
# where the rules stop being data and become part of the AI's instructions.
#
# THE PATH A RULE TRAVELS:
#   a supervisor writes it via POST /policies
#     -> create_support_policy() stores it here
#          -> later, a ticket needs analysing
#               -> tenant_policy_context() gathers that company's rules into one
#                  block of text                                  <- BOTTOM OF THIS FILE
#                    -> routes/tickets.py or the worker passes it into the AI call
#                         -> the prompt template in packages/prompts/ places it
#                            in the instructions the model reads
#
# WHO CALLS THESE:
#   routes/policies.py   - the create and read endpoints
#   routes/tickets.py    - tenant_policy_context, on the synchronous AI path
#   apps/worker/jobs.py  - tenant_policy_context, on the queued path
# ============================================================================

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from supportops_db.models import TenantPolicy

# What the AI is told when a company has written no rules at all.
#
# A deliberate sentence rather than an empty string. The prompt template expects
# something in that slot, and leaving a blank gap could confuse the model or, at
# worst, let the surrounding instructions run together into something
# nonsensical. Stating plainly that there are no rules is unambiguous.
DEFAULT_POLICY_CONTEXT = "No tenant policy context configured."


# Stores a new rule.
#
# Note there is no update function anywhere in this file. Rules are added, never
# rewritten in place, so the record of what the AI was told at any point in time
# stays intact. Superseding a rule means adding a new one.
def create_support_policy(
    session: Session,
    *,
    tenant_id: str,
    name: str,                                    # a short label: "refund-limits"
    content: str,                                 # the rule itself, in plain English
    created_by_user_id: str,
    retention_expires_at: datetime | None = None, # optional expiry; see below
) -> TenantPolicy:
    policy = TenantPolicy(
        tenant_id=tenant_id,
        name=name,
        content=content,
        created_by_user_id=created_by_user_id,
        # Once this date passes, apps/worker/retention.py counts the row for
        # deletion. It exists because temporary rules are dangerous when
        # forgotten: "during the December sale, allow free returns" would
        # otherwise keep instructing the AI the following June.
        retention_expires_at=retention_expires_at,
    )
    session.add(policy)
    session.flush()
    return policy


# Fetches one rule. Tenant-filtered, like every other lookup in the project.
def get_support_policy_by_id(
    session: Session,
    *,
    tenant_id: str,
    policy_id: str,
) -> TenantPolicy | None:
    return session.scalar(
        select(TenantPolicy).where(
            TenantPolicy.tenant_id == tenant_id,
            TenantPolicy.id == policy_id,
        )
    )


# Lists a company's rules, newest first.
#
# The default limit of 50 is not just a guard against huge responses here — it
# also caps how much text can be fed into an AI call by the function below.
def list_support_policies(
    session: Session,
    *,
    tenant_id: str,
    limit: int = 50,
) -> list[TenantPolicy]:
    return list(
        session.scalars(
            select(TenantPolicy)
            .where(TenantPolicy.tenant_id == tenant_id)
            .order_by(TenantPolicy.created_at.desc())
            .limit(limit)
        )
    )


# THE IMPORTANT ONE: turns a company's rules into a single block of text for the
# AI's instructions.
#
# Three details here are each doing real work, and none of them are obvious.
#
# 1. `limit: int = 10` — TEN, not the 50 used everywhere else in this file.
#    This is a cost and quality control. Every character returned here is sent
#    to the AI on EVERY ticket analysis for this company, and AI services charge
#    by the amount of text. Fifty rules would mean a large recurring bill on
#    every single request. It also protects quality: a rule buried in ten pages
#    is far more likely to be overlooked by the model than one in a short list.
#
#    The consequence is worth knowing: a company with more than ten rules will
#    silently have some of them ignored. The newest ten win, since that is what
#    list_support_policies returns.
#
# 2. `reversed(policies)` — the list arrives newest-first, and this flips it to
#    oldest-first. Deliberate. Language models weight the END of their
#    instructions more heavily than the beginning, so putting the newest rules
#    last gives them the strongest influence. Newer rules are the ones most
#    likely to be corrections of earlier behaviour, so that is the right way
#    round.
#
# 3. The formatting — each rule is written as "Policy: name" then its text, with
#    blank lines between. Structure the model can parse: it can tell where one
#    rule ends and the next begins, rather than reading a wall of run-together
#    sentences.
def tenant_policy_context(session: Session, *, tenant_id: str, limit: int = 10) -> str:
    policies = list_support_policies(session, tenant_id=tenant_id, limit=limit)
    if not policies:
        return DEFAULT_POLICY_CONTEXT
    return "\n\n".join(f"Policy: {policy.name}\n{policy.content}" for policy in reversed(policies))

