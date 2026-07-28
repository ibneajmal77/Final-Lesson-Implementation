# ============================================================================
# FILE: packages/db/supportops_db/models.py
#
# THINK OF THIS FILE AS: the blueprint of the database. Every table, every
# column, every rule about what may be stored, described in one place.
#
# WHAT AN "ORM MODEL" IS:
#   Each class below describes one database table, and each `mapped_column`
#   line is one column in it. The library doing this (SQLAlchemy) is an ORM —
#   Object Relational Mapper — which lets you work with database rows as
#   ordinary Python objects: `ticket.subject` instead of writing SQL by hand.
#
# THE SEVEN TABLES AND HOW THEY CONNECT:
#
#   Tenant  (a customer company)
#     |
#     +-- User                  people who work at that company
#     +-- TenantPolicy          that company's written rules for the AI
#     +-- Ticket                a customer's support request
#           |
#           +-- AIRun                  one attempt at analysing the ticket
#           +-- TicketRecommendation   what the analysis concluded
#                 |
#                 +-- RecommendationReview   a human's verdict on it
#           +-- CostEvent              what an AI call cost us
#
#   Read down that tree and you have the whole product: a company's ticket is
#   analysed, producing a suggestion, which a human judges, and the AI call
#   that produced it cost money.
#
# THE ONE RULE REPEATED EVERYWHERE — tenant_id:
#   Almost every table carries a tenant_id. This is a "shared database"
#   multi-tenant design: all companies live in the same tables, kept apart by
#   that column being included in every single query. It is simpler and cheaper
#   than a database per customer, but it means the separation is only as good
#   as the discipline of always filtering by it — which is exactly why the
#   repository functions in repositories/ take tenant_id as a required argument
#   rather than an optional one.
#
# IMPORTANT — THIS FILE DOES NOT CREATE THE TABLES:
#   Changing a line here does NOT change a running database. The actual changes
#   are applied by the numbered migration files in migrations/versions/, and
#   this file must be kept in step with them by hand. Editing only this file is
#   a classic mistake: the code expects a column the database doesn't have.
#
# WHO USES IT: every repository in repositories/, the worker, and the tests.
# ============================================================================

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from supportops_db.base import Base, utc_now


# Generates a new unique ID.
#
# A UUID is a 36-character random string like "f47ac10b-58cc-4372-a567-0e02b2c3d479".
# The project uses these instead of the more common auto-incrementing 1, 2, 3
# for two solid reasons:
#   1. They can be generated ANYWHERE — by the API, by the worker, in a test —
#      without asking the database for the next number first.
#   2. They leak nothing. A ticket numbered 4,317 tells a competitor roughly how
#      many tickets exist; a UUID tells them nothing at all.
def new_id() -> str:
    return str(uuid4())


# ---------------------------------------------------------------------------
# TENANT — one customer company. The root of everything.
# ---------------------------------------------------------------------------
class Tenant(Base):
    __tablename__ = "tenants"      # the real table name in Postgres

    # `primary_key=True` means this uniquely identifies the row.
    # `default=new_id` passes the FUNCTION, not a call to it — note there are no
    # brackets. SQLAlchemy calls it afresh for each new row. Writing
    # `default=new_id()` would call it once at import time and give every row
    # the same ID.
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String(200), nullable=False)     # "Acme Corporation"

    # A short URL-safe nickname, e.g. "acme".
    #   unique=True - no two companies may share one
    #   index=True  - makes lookups by slug fast (see the note on indexes below)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)

    # `nullable=False` means this column can never be empty — the database
    # itself will refuse such a row, whatever the application code does.
    # `default=utc_now` fills it in automatically; see base.py for why it is
    # always UTC.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


# ---------------------------------------------------------------------------
# USER — a person who works at one of those companies.
#
# Note what is NOT here: no password, no password hash, no login tokens. This
# app never authenticates anyone. It trusts identity headers set by a gateway
# in front of it (see dependencies.py and docs/threat-model.md). This table
# only records who exists and what they are allowed to do.
# ---------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    # __table_args__ holds table-wide rules, as opposed to per-column ones.
    __table_args__ = (
        # An email must be unique WITHIN a company, not globally. That
        # distinction is deliberate: the same person may legitimately work for
        # two customer companies, and a global unique rule would block that.
        UniqueConstraint("tenant_id", "email", name="uq_users_tenant_email"),

        # AN INDEX is like the index at the back of a book: without one the
        # database reads every row to find matches; with one it jumps straight
        # there. Since EVERY query in this app filters by tenant_id, this index
        # is what stops each query scanning every company's rows.
        # The cost is that writes get slightly slower and storage grows — a
        # trade that is almost always worth it for a column filtered this often.
        Index("ix_users_tenant_id", "tenant_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)

    # A FOREIGN KEY is a promise enforced by the database: this value must match
    # a real id in the tenants table. It makes an orphaned user — belonging to a
    # company that doesn't exist — impossible rather than merely unlikely.
    #
    # `ondelete="CASCADE"` says what happens if that company is deleted: delete
    # this row too. Sensible here, and it is what makes deleting a company
    # actually remove its data rather than leaving unreachable rows behind.
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    # 320 characters is the maximum length an email address may have by the
    # relevant internet standard (64 for the local part + @ + 255 for the domain).
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    # "agent" / "lead" / "admin" / "service" — the list in dependencies.py.
    # Stored as plain text rather than a database enum type, which keeps adding
    # a new role a code change rather than a database migration.
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )


# ---------------------------------------------------------------------------
# TENANT POLICY — one company's written rule for the AI.
#
# Note the class name and table name disagree: TenantPolicy vs "support_policies",
# and the API calls it SupportPolicy again. The names drifted during development.
# All three refer to the same thing.
# ---------------------------------------------------------------------------
class TenantPolicy(Base):
    __tablename__ = "support_policies"
    __table_args__ = (
        # Rule names must be unique per company, so "refund-limits" identifies
        # exactly one rule and cannot quietly exist twice with different text.
        UniqueConstraint("tenant_id", "name", name="uq_support_policies_tenant_name"),
        Index("ix_support_policies_tenant_id", "tenant_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # `Text` rather than `String(n)`: unlimited length. Used for anything that
    # is genuinely free-form prose, where any limit would be arbitrary. The API
    # schema still caps it at 10,000 characters — the database allows more, but
    # the application chooses not to.
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Note this is NOT a foreign key to users.id, and it is 200 characters
    # rather than 36. A loose reference on purpose: if the person who wrote the
    # rule later leaves and their user row is removed, the record of who wrote
    # it survives. A strict foreign key with CASCADE would erase that history.
    created_by_user_id: Mapped[str] = mapped_column(String(200), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    # `onupdate=utc_now` is the interesting part: the database refreshes this
    # automatically every time the row changes, with no need for the application
    # to remember. Only tables whose rows can be MODIFIED have this column —
    # tickets and policies do; reviews and cost events, which are write-once
    # records, do not.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )
    # The privacy expiry date, read by apps/worker/retention.py. Nullable, and
    # null means "keep indefinitely". Added across the tables by migration 0007.
    retention_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


# ---------------------------------------------------------------------------
# TICKET — a customer's support request. The centre of the product.
# ---------------------------------------------------------------------------
class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        # THE RULE THAT PREVENTS DUPLICATES. The sending helpdesk system will
        # retry when a reply gets lost, and this makes a duplicate impossible at
        # the database level. routes/tickets.py checks for an existing ticket
        # first and returns it politely — but even if that check were removed or
        # two requests raced each other, this constraint would still hold the line.
        UniqueConstraint("tenant_id", "external_id", name="uq_tickets_tenant_external_id"),

        Index("ix_tickets_tenant_id", "tenant_id"),

        # A COMPOSITE INDEX, covering two columns together. It exists for the
        # query the app actually runs most: "this company's OPEN tickets". A
        # database can use one index on (tenant_id, status) far more efficiently
        # than combining two separate single-column ones.
        #
        # Column order matters: this index also serves a search on tenant_id
        # alone (the leftmost column), but NOT one on status alone.
        Index("ix_tickets_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    # The ID this ticket has in the customer's own helpdesk (Zendesk etc.).
    external_id: Mapped[str] = mapped_column(String(200), nullable=False)
    channel: Mapped[str] = mapped_column(String(50), nullable=False)     # email / chat / web
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    # Text rather than a length-capped column: support emails run long.
    body: Mapped[str] = mapped_column(Text, nullable=False)

    # `default="open"` is applied when a new row omits the value, which is why
    # routes/tickets.py never sets these two on creation.
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="normal")

    # Nullable: not every ticket comes from a registered customer.
    customer_id: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # A JSON column — a whole structured document inside one column. Useful for
    # data whose shape isn't known in advance, such as extra fields from whatever
    # helpdesk sent the ticket.
    #
    # The trade-off is real: JSON columns are flexible but awkward to query and
    # index, and the database cannot check their contents. Good for "extra stuff
    # we might want later", bad for anything you will filter or sum.
    #
    # `default=dict` passes the function (no brackets) for the same reason as
    # new_id above — each row must get its OWN empty dictionary.
    metadata_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )
    retention_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


# ---------------------------------------------------------------------------
# AI RUN — the job sheet for one analysis attempt.
#
# This table exists purely because the queued path is asynchronous. In the
# synchronous path there is nothing to record: the work happens inside one
# request and either returns a result or an error. Queued work has a LIFETIME —
# created, started, finished — and something has to hold that state while the
# user waits. That something is this table.
#
# It is also the record of failures. A recommendation row only exists if the
# analysis worked; an AIRun exists even when it didn't, which is what lets you
# ask "how often does this fail, and why?"
# ---------------------------------------------------------------------------
class AIRun(Base):
    __tablename__ = "ai_runs"
    __table_args__ = (
        Index("ix_ai_runs_tenant_id", "tenant_id"),
        Index("ix_ai_runs_ticket_id", "ticket_id"),
        Index("ix_ai_runs_tenant_ticket", "tenant_id", "ticket_id"),   # the polling query
        # An index on status alone, unlike the others. It serves the operational
        # question "are any jobs stuck?" — find everything still marked
        # "running" across all companies, which is a search that deliberately
        # ignores tenant boundaries.
        Index("ix_ai_runs_status", "status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    ticket_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tickets.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Points at the result, once there is one.
    #
    # `ondelete="SET NULL"` rather than CASCADE — an important difference. If the
    # recommendation is deleted, this becomes empty but THE JOB SHEET SURVIVES.
    # That is what you want: the record that an analysis ran, and what it cost,
    # should outlive the text it produced. CASCADE here would quietly erase the
    # history whenever retention cleanup removed a recommendation.
    output_recommendation_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("ticket_recommendations.id", ondelete="SET NULL"),
        nullable=True,
    )

    run_type: Mapped[str] = mapped_column(String(50), nullable=False)   # "ticket_analysis" today;
                                                                        # room for other AI jobs
    # The state machine: queued -> running -> succeeded / abstained / failed.
    # Note the default is "queued" here, while the API schema calls the same
    # state "pending" — a small naming inconsistency between the two layers.
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="queued")

    # All nullable, because the job sheet is created BEFORE the work starts, so
    # none of these are known at that moment.
    prompt_version: Mapped[str | None] = mapped_column(String(100), nullable=True)
    model_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Exactly 64 characters, because that is the length of a SHA-256 hash written
    # in hexadecimal. See _ticket_input_hash() in routes/tickets.py.
    input_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Two error columns rather than one, on purpose:
    #   error_code    - short and stable, safe to GROUP BY and count in dashboards
    #   error_message - the full detail, for a human debugging. Text, so it can
    #                   hold a long message
    error_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Three timestamps telling the whole story:
    #   created -> started   = time spent waiting in the queue (worker overloaded?)
    #   started -> finished  = time the work itself took (AI service slow?)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retention_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


# ---------------------------------------------------------------------------
# TICKET RECOMMENDATION — what an analysis concluded, and the draft reply.
#
# Produced by all three analysis paths. Several may exist for one ticket — a
# baseline one plus an AI one, or repeated AI attempts. Nothing is ever
# overwritten, so the full history of what was suggested stays intact.
# ---------------------------------------------------------------------------
class TicketRecommendation(Base):
    __tablename__ = "ticket_recommendations"
    __table_args__ = (
        Index("ix_ticket_recommendations_tenant_id", "tenant_id"),
        Index("ix_ticket_recommendations_ticket_id", "ticket_id"),
        Index("ix_ticket_recommendations_tenant_ticket", "tenant_id", "ticket_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    ticket_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tickets.id", ondelete="CASCADE"),
        nullable=False,
    )

    # WHICH method produced this: "baseline_v1", or an AI provider's name. The
    # single most useful column for the metrics, since comparing approval rates
    # by source is what tells you whether the AI beats simple keyword rules.
    # The version suffix in the default matters — when the baseline logic
    # changes, its results stay distinguishable from the old ones.
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="baseline_v1")

    # The judgement. All required — every analysis must reach a conclusion.
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False)
    requires_escalation: Mapped[bool] = mapped_column(Boolean, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)     # 0.0 to 1.0

    # The four AI-only columns. Nullable precisely because the baseline path
    # leaves them empty — keyword rules cannot name a model or write a reply.
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(100), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    suggested_reply: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Structured details found in the ticket — an order number, an error code.
    # JSON because what is worth extracting differs entirely between a billing
    # query and a crash report, so fixed columns would not fit.
    extracted_fields_json: Mapped[dict[str, object]] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    # WHY it decided this, as a list of sentences. `default=list` gives each row
    # its own new empty list, for the same reason as `default=dict` above.
    reasons_json: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    # No updated_at here, unlike tickets and policies. Deliberate: a
    # recommendation is a record of what was suggested at a moment in time, and
    # is never edited. A human disagreeing creates a REVIEW instead (next table).
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    retention_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


# ---------------------------------------------------------------------------
# RECOMMENDATION REVIEW — a human's verdict on an AI draft.
#
# The safety record of the whole system, and the source of the approval-rate
# figures that decide whether the AI stays switched on. Write-once: never
# updated, never deleted (except by retention). A supervisor who disagrees with
# an agent creates a second review rather than altering the first.
# ---------------------------------------------------------------------------
class RecommendationReview(Base):
    __tablename__ = "recommendation_reviews"
    __table_args__ = (
        # Four indexes — more than any other table. Justified because this is
        # the table the metrics queries hammer, joining and grouping it in
        # several different directions.
        Index("ix_recommendation_reviews_tenant_id", "tenant_id"),
        Index("ix_recommendation_reviews_ticket_id", "ticket_id"),
        Index("ix_recommendation_reviews_recommendation_id", "recommendation_id"),
        Index(
            "ix_recommendation_reviews_tenant_ticket",
            "tenant_id",
            "ticket_id",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    # Both the ticket AND the recommendation are recorded. Strictly the ticket
    # could be found via the recommendation, but storing it directly saves a
    # join on the metrics queries that run most often — a deliberate, modest
    # duplication in exchange for speed.
    ticket_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tickets.id", ondelete="CASCADE"),
        nullable=False,
    )
    recommendation_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("ticket_recommendations.id", ondelete="CASCADE"),
        nullable=False,
    )

    # WHO decided. Like created_by_user_id on policies, a loose reference rather
    # than a foreign key, so the accountability record survives the reviewer
    # leaving the company.
    reviewer_user_id: Mapped[str] = mapped_column(String(200), nullable=False)

    # "approved" / "rejected" / "edited". The database accepts any string; the
    # restriction to those three is enforced by the API schema
    # (schemas/approvals.py). A stricter database enum would have been possible
    # but would make adding a fourth verdict a migration rather than a code change.
    decision: Mapped[str] = mapped_column(String(50), nullable=False)

    # The agreed final text. Null for a rejection — there is no agreed text.
    # Stored as a COPY of the wording rather than a pointer back to the draft, so
    # that if the draft is later removed by retention, the reply actually
    # approved is still on record.
    final_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    final_reply: Mapped[str | None] = mapped_column(Text, nullable=True)

    # The reviewer's own explanation. Small column, large value — these notes are
    # grouped in the /metrics/pilot/feedback report and are usually the quickest
    # route to understanding what the AI keeps getting wrong.
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    retention_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


# ---------------------------------------------------------------------------
# COST EVENT — what one AI call cost, in tokens and money.
#
# Written on every AI call by record_ticket_analysis_usage. This is what makes
# "is this feature worth what we pay for it?" an answerable question rather than
# a matter of opinion, and it feeds both /metrics/costs and docs/cost-report.md.
# ---------------------------------------------------------------------------
class CostEvent(Base):
    __tablename__ = "cost_events"
    __table_args__ = (
        Index("ix_cost_events_tenant_id", "tenant_id"),
        Index("ix_cost_events_ticket_id", "ticket_id"),
        Index("ix_cost_events_ai_run_id", "ai_run_id"),
        # For "what did this company spend LAST MONTH?" — filtering by company
        # and a date range at once, which is the shape almost every cost
        # question takes.
        Index("ix_cost_events_tenant_created_at", "tenant_id", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    # Only tenant_id is required. Costs must always be attributable to a company,
    # because that is what billing and budgeting depend on.
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )

    # The next three are all nullable, and their delete behaviour is chosen
    # carefully — this is the most subtle part of the file.
    #
    # ticket_id uses CASCADE: delete the ticket, delete its cost records too.
    # The others use SET NULL: the cost record SURVIVES, merely losing its link.
    #
    # The reasoning is that a spend that actually happened must not disappear
    # from the accounts because a related row was cleaned up. Money left our
    # account; the record of it should outlive the text it bought.
    ticket_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("tickets.id", ondelete="CASCADE"),
        nullable=True,
    )
    ai_run_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("ai_runs.id", ondelete="SET NULL"),
        nullable=True,        # null for the SYNCHRONOUS path, which has no job sheet
    )
    recommendation_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("ticket_recommendations.id", ondelete="SET NULL"),
        nullable=True,        # null when the call failed before producing anything
    )

    # WHAT was called. Required, since a cost with no attribution cannot be
    # analysed or acted on.
    provider: Mapped[str] = mapped_column(String(50), nullable=False)     # e.g. "hosted", "mock"
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt_version: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Which kind of operation: "sync_ticket_analysis" / "async_ticket_analysis".
    # Lets the two paths' costs be compared separately.
    operation: Mapped[str] = mapped_column(String(100), nullable=False)

    # THE ACTUAL NUMBERS.
    # Input and output tokens are counted separately because they are priced
    # differently — output usually costs several times more than input, so a
    # single combined total would hide where the money is going.
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # "estimated" is an honest label: this is tokens multiplied by our configured
    # prices (see settings.py), not a figure from a real invoice. Prices change,
    # and providers apply volume discounts — treat it as a close guide.
    #
    # Note it is a Float. Floating-point numbers are famously imprecise for
    # money, and for actual billing a fixed-precision decimal type would be
    # correct. It is acceptable here only because these are estimates for
    # reporting rather than amounts anyone is charged.
    estimated_cost_usd: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Stored as whole milliseconds. Sub-millisecond precision would be noise for
    # a call that takes seconds.
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Room for extra details without needing a migration for each new one.
    metadata_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    retention_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
