# ============================================================================
# FILE: apps/api/supportops_api/schemas/tickets.py
#
# THINK OF THIS FILE AS: the forms for tickets — what you must fill in to
# create one, and what you get back when you read one.
#
# WHAT A "SCHEMA" IS AND WHY IT EARNS ITS KEEP:
#   A schema is a strict description of a JSON shape. This project uses Pydantic
#   for it, and FastAPI wires it in automatically, which buys three things at
#   once from these few lines:
#
#     1. VALIDATION. Incoming JSON is checked against the rules below BEFORE any
#        route code runs. Wrong type, missing field, or text too long, and the
#        caller gets a clear 422 error explaining exactly which field was wrong.
#        By the time a route function starts, its input is already known-good —
#        which is why you will not find a single `if not subject:` check in
#        routes/tickets.py.
#
#     2. DOCUMENTATION. FastAPI generates the interactive API docs page at /docs
#        straight from these classes, so the docs cannot drift out of date.
#
#     3. A DELIBERATE BOUNDARY. Nothing leaves the app unless it is listed here.
#        Add a column to the database and it stays invisible to the outside
#        world until someone adds it below — which is exactly what you want for
#        a column holding something private.
#
# WHY TWO CLASSES FOR ONE THING (the "Create" / "Read" split):
#   They are genuinely different shapes, and merging them would be a bug waiting
#   to happen. When creating a ticket you must NOT be able to set its `id` or
#   `tenant_id` — the server decides those. When reading one back, those fields
#   must be present. Separate classes make each rule impossible to get wrong.
#
# USED BY: routes/tickets.py, on every endpoint that handles tickets.
# ============================================================================

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# --- GOING IN: the JSON body accepted by POST /tickets ----------------------
#
# `Field(...)` attaches rules to a field. The length limits are not fussiness —
# they are the first line of defence. Without a maximum, someone could post a
# 50-megabyte "subject", filling the database and then being sent to the AI as
# a very expensive question.
class TicketCreate(BaseModel):
    # The ticket's ID in the customer's own helpdesk system. Required, because
    # routes/tickets.py uses it to recognise repeat submissions and avoid
    # creating duplicates.
    external_id: str = Field(min_length=1, max_length=200)

    # Where it arrived from: "email", "chat", "web", and so on. Kept as free
    # text rather than a fixed list, so a new channel doesn't need a code change.
    channel: str = Field(min_length=1, max_length=50)

    # min_length=1 on both of these matters more than it looks: without it, an
    # empty string would pass as "present", and the AI would be asked to analyse
    # nothing at all.
    subject: str = Field(min_length=1, max_length=500)
    body: str = Field(min_length=1)          # no maximum — support emails legitimately run long,
                                             # and the AI call caps its own input anyway

    # Optional, hence `| None`. Some tickets arrive from people who aren't
    # registered customers.
    customer_id: str | None = Field(default=None, max_length=200)

    # A free-form bag for anything else the sending system wants to attach —
    # tags, a priority hint, the original mailbox.
    #
    # `default_factory=dict` rather than `default={}` is important, and a classic
    # Python trap. A plain `{}` default would create ONE dictionary shared by
    # every ticket ever made, so anything added to one would appear in all of
    # them. `default_factory` builds a fresh empty dictionary each time.
    metadata: dict[str, Any] = Field(default_factory=dict)


# --- COMING OUT: the JSON shape returned by every ticket endpoint -----------
#
# No `Field(...)` rules here, because this data is ours: it came from our own
# database, so there is nothing to validate. The class exists to define the
# shape, not to police it.
class TicketRead(BaseModel):
    # These two are assigned by the server, never by the caller — the reason
    # this class is separate from TicketCreate above.
    id: str
    tenant_id: str

    # Everything the caller supplied, echoed back.
    external_id: str
    channel: str
    subject: str
    body: str

    # Set by the server on creation and changed as the ticket progresses:
    # status is "open"/"closed"/..., priority is "low"/"medium"/"high". Defaults
    # for both are defined on the database table in packages/db/.../models.py.
    status: str
    priority: str

    customer_id: str | None
    metadata: dict[str, Any]   # named "metadata" here, though the database column is
                               # "metadata_json"; the rename happens in _ticket_to_read()

    # Sent as ISO-format text in the JSON, e.g. "2026-07-21T14:30:00Z".
    # Comparing these two tells you whether a ticket has been touched since it
    # was created.
    created_at: datetime
    updated_at: datetime
