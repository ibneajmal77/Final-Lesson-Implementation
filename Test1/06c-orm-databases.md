# 06c — ORMs AND DATA ACCESS, FROM ZERO

> **Pure SQL is in `07-sql-databases.md`.** This file is about the **layer between your objects
> and the database** — SQLAlchemy, Django ORM, Entity Framework, and the ideas they share.
>
> Same format: **What** → **Code** → **Why** → **Say** → **Hook** → ⚠️ **Trap**
>
> **Your angle:** you already know EF Core. Every ORM concept below has an EF equivalent.
> Answer in both languages and you sound like someone who's actually shipped both.

**30 minutes?** Part 0 → Part 5 (N+1) → Part 7 (transactions) → Part 13.

---

# 📑 MAP

| Part | Topic |
|---|---|
| 0 | The 15 answers that win |
| 1 | What an ORM is, and the two patterns |
| 2 | SQLAlchemy — Core vs ORM |
| 3 | Defining models |
| 4 | Querying |
| 5 | **Relationships and N+1** ⭐ |
| 6 | The session / unit of work |
| 7 | **Transactions and isolation** ⭐ |
| 8 | Concurrency: optimistic vs pessimistic |
| 9 | Connection pooling |
| 10 | Migrations with Alembic |
| 11 | Async SQLAlchemy |
| 12 | Performance |
| 13 | When NOT to use an ORM |
| 14 | The repository pattern |
| 15 | NoSQL and the alternatives |
| 16 | ORM comparison table |
| 17 | 80 rapid-fire questions |

---

# FULL TECH LOAD MEMORY HOOKS

Use these as labels for the full detail below. Say the hook first, then expand only where the
interviewer pushes.

| Hook | Simple wording | Full tech load to keep |
|---|---|---|
| **ORM for the 90%** | Use objects for normal transactions; use SQL for hard queries. | Boilerplate removal, parameterisation, hidden SQL risk, reporting/window queries. |
| **Two ORM families** | Active Record saves itself; Data Mapper uses a session. | Django/Rails vs SQLAlchemy/EF Core/Hibernate. |
| **N+1 hides in relations** | One list query can become one query per row. | Lazy loading, eager loading, joins, `IN` prefetch, query-count tests. |
| **Session tracks work** | Changes gather, then commit together. | Unit of work, identity map, flush vs commit, rollback. |
| **Flush is not commit** | SQL can be sent before the transaction ends. | DB-generated IDs, rollback still possible, transaction boundaries. |
| **Optimistic first** | Version column for normal contention. | Pessimistic `SELECT FOR UPDATE` for high-value/high-contention money operations. |
| **Pool with a limit** | Connections are expensive and finite. | Worker count times pool size must fit database limits; timeouts and recycling. |
| **Expand, migrate, contract** | Zero-downtime schema change is staged. | Nullable add, batched backfill, dual writes, switch reads, drop old column later. |
| **Repository is not automatic** | EF and SQLAlchemy already give repositories of a sort. | Add only when it hides persistence or clarifies domain intent. |

---

# PART 0 — THE 15 ANSWERS THAT WIN

| # | Question | Say this |
|---|---|---|
| 1 | **What is an ORM?** | "It maps database rows to objects, so I write Python instead of SQL. It handles change tracking, relationships and transactions. The cost is a layer of indirection between me and the query plan." |
| 2 | **Two patterns?** | "**Active Record** — the object knows how to save itself. Django, Rails. **Data Mapper** — a separate session tracks objects. SQLAlchemy, EF Core, Hibernate." |
| 3 | **N+1 in one line?** | "One query for the list, then one more per row when I touch a relation. Fixed by eager loading — a JOIN, or a second query with an `IN` clause." |
| 4 | **Lazy vs eager loading?** | "Lazy fetches the relation when you touch it. Eager fetches it upfront. Lazy is the default and it's the default cause of N+1." |
| 5 | **Unit of work?** | "The session collects changes in memory and flushes them in one transaction on commit. That's `DbContext.SaveChanges`." |
| 6 | **Identity map?** | "One object per primary key per session. Query the same row twice and you get the same instance." |
| 7 | **Flush vs commit?** | "Flush sends the SQL. Commit ends the transaction. A flush is still rollback-able." |
| 8 | **Optimistic vs pessimistic locking?** | "Optimistic: a version column, and the update fails if someone else changed the row. Pessimistic: `SELECT FOR UPDATE`, holding a real lock. Optimistic for low contention, pessimistic for money movements." |
| 9 | **Isolation levels?** | "Read Uncommitted, Read Committed, Repeatable Read, Serializable — trading concurrency for consistency. Postgres defaults to Read Committed, SQL Server too." |
| 10 | **Why pool connections?** | "A TCP connection plus authentication costs milliseconds. A pool reuses them. Size it so workers × pool ≤ the database's connection limit." |
| 11 | **Migrations?** | "Versioned, reviewable schema changes in source control. Alembic for SQLAlchemy, built in for Django, EF Migrations for .NET." |
| 12 | **Zero-downtime schema change?** | "Expand, migrate, contract. Add the nullable column, backfill in batches, deploy code writing both, then make it required and drop the old one." |
| 13 | **When not to use an ORM?** | "Bulk loads, complex reporting, window functions, recursive CTEs. I drop to SQL there — the ORM is for the transactional 90%." |
| 14 | **Biggest ORM risk?** | "It hides how much SQL you're generating. I log queries in development and assert query counts in tests." |
| 15 | **SQLAlchemy vs EF Core?** | "Same pattern — Data Mapper with a unit of work. SQLAlchemy Core gives you an explicit SQL expression language underneath, which EF doesn't really have. LINQ-to-Entities is closer to the SQLAlchemy ORM layer." |

---

# PART 1 — WHAT AN ORM IS

## 1.1 The idea

**What.** Database tables become classes. Rows become objects. Columns become attributes.

```
┌──────────────┐            ┌──────────────┐
│ orders TABLE │  ←── ORM ──→│ Order CLASS  │
│ id  symbol   │            │ .id .symbol  │
└──────────────┘            └──────────────┘
```

**What you get:**
- No hand-written SQL for the common 90%.
- Automatic parameterisation → SQL injection is gone by default.
- Relationships as attributes: `order.account.name`.
- Change tracking and transactions.
- Database portability (in theory).

**What it costs:**
- You stop seeing the SQL. Performance problems become invisible.
- Complex queries get harder, not easier.
- Another abstraction to learn and debug.

**Say:** *"An ORM removes the boilerplate for the transactional 90% and gives me parameterised queries for free. The risk is that it hides the SQL — so I log generated queries in development and I'm comfortable dropping to raw SQL for reporting."*

**Hook:** **ORM for the 90%. SQL for the rest.**

---

## 1.2 The two patterns ⭐

### Active Record — Django, Rails

The object **is** the row and knows how to persist itself.

```python
order = Order(symbol="VOD", qty=10)
order.save()                    # the object talks to the database
Order.objects.filter(...)       # the class carries the query manager
```

### Data Mapper — SQLAlchemy, EF Core, Hibernate

The object is plain. A **session** maps it to the database.

```python
order = Order(symbol="VOD", qty=10)      # pure Python object. Knows nothing
session.add(order)                       # the SESSION persists it
session.commit()
```

| | Active Record | Data Mapper |
|---|---|---|
| Persistence lives in | the model | the session/context |
| Simplicity | ✅ less code | more setup |
| Domain purity | model coupled to the DB | ✅ model is plain |
| Testability | needs the DB | ✅ test the model alone |
| Examples | Django, Rails | SQLAlchemy, **EF Core**, Hibernate |

**Say:** *"Active Record is faster to write and fine for CRUD-shaped apps. Data Mapper keeps the domain model free of persistence concerns, which matters when the business logic is the complicated part. EF Core and SQLAlchemy are both Data Mapper — that's why they both have a context or session you commit."*

**Hook:** **Active Record: the object saves itself. Data Mapper: the session saves it.**

---

# PART 2 — SQLALCHEMY: CORE vs ORM

SQLAlchemy is **two libraries stacked**.

| Layer | What it is | Use for |
|---|---|---|
| **Core** | a Python expression language that generates SQL. No objects | bulk work, reporting, ETL |
| **ORM** | maps classes to tables, adds a session and change tracking | normal application code |

```python
# Core — you're writing SQL, in Python
from sqlalchemy import select, insert
stmt = select(orders_table).where(orders_table.c.symbol == "VOD")
conn.execute(stmt)

# ORM — you're working with objects
session.execute(select(Order).where(Order.symbol == "VOD")).scalars().all()
```

**Say:** *"Core is a typed, composable SQL builder — it protects me from injection and from string-concatenated SQL without pretending the database isn't there. The ORM sits on top and adds identity mapping and change tracking. Being able to drop from ORM to Core in the same session is SQLAlchemy's real advantage."*

**Hook:** **Core = SQL in Python. ORM = objects on top.**

**Version note:** SQLAlchemy 2.0 unified the API. `select()` everywhere,
`session.execute(...).scalars()` instead of the old `session.query(...)`.
Saying "2.0 style" signals you're current.

---

# PART 3 — DEFINING MODELS

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Numeric, DateTime, Index, CheckConstraint
from decimal import Decimal
from datetime import datetime

class Base(DeclarativeBase): pass

class Account(Base):
    __tablename__ = "accounts"
    id:   Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    orders: Mapped[list["Order"]] = relationship(back_populates="account",
                                                 cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"
    id:         Mapped[int]      = mapped_column(primary_key=True)
    account_id: Mapped[int]      = mapped_column(ForeignKey("accounts.id"), index=True)
    symbol:     Mapped[str]      = mapped_column(String(10), index=True)
    qty:        Mapped[int]
    price:      Mapped[Decimal]  = mapped_column(Numeric(18, 4))   # ⭐ money
    created:    Mapped[datetime] = mapped_column(server_default=func.now())
    version:    Mapped[int]      = mapped_column(default=0)        # optimistic lock

    account: Mapped["Account"] = relationship(back_populates="orders")

    __table_args__ = (
        Index("ix_symbol_created", "symbol", "created"),
        CheckConstraint("qty > 0", name="qty_positive"),
        {"mysql_engine": "InnoDB"},
    )
    __mapper_args__ = {"version_id_col": version}      # ⭐ optimistic concurrency
```

**Points to make:**
- `Mapped[...]` typing is the 2.0 style — mypy understands the model.
- `Numeric`/`DECIMAL` for money, **never `Float`**.
- `back_populates` keeps both sides of the relationship in sync in memory.
- Constraints in `__table_args__` are enforced by the **database**, not just the app.

⚠️ **Trap: "`Mapped[str]` vs `Mapped[str | None]`?"** → *"The Optional in the annotation sets `nullable`. `Mapped[str]` is NOT NULL, `Mapped[str | None]` is nullable. The type hint is the schema."*

---

# PART 4 — QUERYING

```python
from sqlalchemy import select, func, and_, or_

# one row
session.get(Order, 1)                                   # ⭐ checks identity map first
session.execute(select(Order).where(Order.id == 1)).scalar_one_or_none()

# many
session.execute(
    select(Order)
    .where(Order.symbol == "VOD", Order.qty > 100)      # comma = AND
    .order_by(Order.created.desc())
    .limit(50)
).scalars().all()

# OR
select(Order).where(or_(Order.symbol == "VOD", Order.symbol == "BP"))

# join
select(Order, Account).join(Account).where(Account.name == "HSBC")

# aggregate / GROUP BY
select(Order.symbol, func.sum(Order.qty).label("total")) \
    .group_by(Order.symbol) \
    .having(func.sum(Order.qty) > 1000)

# subquery
sub = select(Order.account_id).where(Order.qty > 1000).subquery()
select(Account).where(Account.id.in_(select(sub.c.account_id)))

# window function ⭐ says "I know SQL"
select(Order.symbol, Order.price,
       func.row_number().over(partition_by=Order.symbol,
                              order_by=Order.created.desc()).label("rn"))
```

**Writes:**
```python
session.add(order)                     # one
session.add_all([o1, o2])
session.delete(order)
session.execute(update(Order).where(Order.id == 1).values(filled=True))   # bulk
session.execute(insert(Order), [{...}, {...}])                            # bulk insert
session.commit()
```

⚠️ **Bulk `update()`/`delete()` bypass the ORM.** No events fire, and objects already loaded in
the session are stale. Use `synchronize_session="fetch"` or expire the session afterwards.

**Say:** *"Bulk operations go straight to SQL — they don't load objects, so they're fast, but they skip ORM events and leave loaded instances stale. That's a deliberate trade and it needs to be a conscious one."*

---

# PART 5 — RELATIONSHIPS AND N+1 ⭐⭐

**The single most asked ORM question in any language.**

## 5.1 The problem

```python
orders = session.execute(select(Order).limit(100)).scalars().all()   # 1 query
for o in orders:
    print(o.account.name)          # ⚠️ 100 MORE queries — one per order
```
**101 queries.** Locally with a 1ms database it looks fine. In production with 20ms latency
it's 2 seconds.

## 5.2 The fixes

```python
from sqlalchemy.orm import selectinload, joinedload, subqueryload, raiseload

# JOIN — one query. Best for many-to-one
select(Order).options(joinedload(Order.account))

# Second query with WHERE id IN (...) — best for one-to-many ⭐ usually the default choice
select(Account).options(selectinload(Account.orders))

# Nested
select(Account).options(selectinload(Account.orders).joinedload(Order.instrument))

# ⭐ THE SENIOR MOVE: make lazy loading raise instead of silently N+1ing
select(Order).options(raiseload("*"))
```

| Strategy | SQL | Best for |
|---|---|---|
| `lazy` (default) | one per access | ⚠️ causes N+1 |
| `joinedload` | one query, LEFT JOIN | many-to-one, one-to-one |
| `selectinload` | two queries, `IN (...)` | ⭐ one-to-many, many-to-many |
| `subqueryload` | two queries, subquery | legacy; selectin is usually better |
| `raiseload` | raises on lazy access | ⭐ enforcing it in tests |

⚠️ **Why not `joinedload` for one-to-many?** A JOIN multiplies rows — 100 accounts × 50 orders
is 5,000 rows to deduplicate in Python. `selectinload` sends two clean queries instead.

**Say the whole thing:**
> *"N+1 is one query for the collection, then one more per row when you touch a lazy relation. The fix is eager loading. For many-to-one I use `joinedload` — a single JOIN. For one-to-many I use `selectinload`, because a JOIN multiplies rows and you pay for deduplication. In Django it's `select_related` and `prefetch_related`; in EF Core it's `Include`. And I catch them by logging SQL in development and asserting query counts in tests."*

**Hook:** **JOIN for many-to-one. Second query for one-to-many.**

## 5.3 The equivalents — say all three

| Concept | SQLAlchemy | Django | EF Core |
|---|---|---|---|
| JOIN eager load | `joinedload` | `select_related` | `.Include()` |
| Second-query eager load | `selectinload` | `prefetch_related` | `.Include()` + split query |
| Disable lazy | `raiseload` | — | `NoTracking` + explicit |
| See the SQL | `echo=True` | `django-debug-toolbar` | `.ToQueryString()` |

## 5.4 Relationship options

```python
orders: Mapped[list["Order"]] = relationship(
    back_populates="account",
    cascade="all, delete-orphan",     # deleting the parent deletes the children
    lazy="selectin",                  # default strategy for this relationship
    order_by="Order.created",
)
```

**Many-to-many:**
```python
tags = relationship("Tag", secondary=order_tags_table, back_populates="orders")
```

---

# PART 6 — THE SESSION (UNIT OF WORK)

## 6.1 What it does — four jobs

1. **Identity map** — one object per primary key. Same row queried twice → same instance.
2. **Change tracking** — it watches loaded objects for modifications.
3. **Unit of work** — batches all changes and flushes them in dependency order.
4. **Transaction scope** — begin, commit, rollback.

```python
with Session(engine) as session:
    with session.begin():             # commit on success, rollback on exception
        order = session.get(Order, 1)
        order.qty = 20                # ⭐ no save() call — it's tracked
    # committed here
```

**Object states — worth naming:**

| State | Meaning |
|---|---|
| **Transient** | new object, not in a session |
| **Pending** | added, not yet flushed |
| **Persistent** | in the session and in the database |
| **Detached** | was persistent, session closed |
| **Deleted** | marked for deletion |

⚠️ **`DetachedInstanceError`** — accessing a lazy relationship after the session closed.
Fix: eager load before closing, or keep the session open for the request.
`expire_on_commit=False` avoids the related surprise where every attribute reloads after commit.

**Say:** *"The session is the unit of work — it tracks loaded objects, so mutating an attribute is enough; there's no explicit save. On commit it works out the insert, update and delete order and flushes in one transaction. It's `DbContext` with `SaveChanges`."*

**Hook:** **Session = DbContext. Commit = SaveChanges.**

## 6.2 Flush vs commit

- **Flush** — sends the pending SQL. Still inside the transaction. Still rollback-able.
- **Commit** — flushes, then commits the transaction.

A flush happens automatically before a query, so your own uncommitted changes are visible to it.

**Say:** *"Flush emits the SQL, commit ends the transaction. I sometimes flush deliberately to get a generated primary key before commit."*

## 6.3 Session scope

**One session per request.** Not global, not shared between threads or async tasks.

⚠️ **The interview trap:** *"A `Session` isn't thread-safe or task-safe. In FastAPI I create it in a dependency with `yield`, so it's per request and always closed. Sharing one session across concurrent tasks corrupts the identity map — it's the same rule as one `DbContext` per request in ASP.NET."*

---

# PART 7 — TRANSACTIONS AND ISOLATION ⭐

## 7.1 ACID

| Letter | Meaning |
|---|---|
| **A**tomicity | all of it, or none of it |
| **C**onsistency | constraints hold before and after |
| **I**solation | concurrent transactions don't see each other's mess |
| **D**urability | committed means it survives a crash |

## 7.2 The isolation levels

| Level | Prevents | Still allows |
|---|---|---|
| **Read Uncommitted** | nothing | dirty reads |
| **Read Committed** ⭐ default | dirty reads | non-repeatable reads, phantoms |
| **Repeatable Read** | + non-repeatable reads | phantoms (not in Postgres/MySQL) |
| **Serializable** | everything | nothing — but expensive |

**The three anomalies — define them cleanly:**
- **Dirty read** — you read data another transaction hasn't committed.
- **Non-repeatable read** — you read the same **row** twice and it changed.
- **Phantom read** — you run the same **query** twice and new rows appeared.

**Say:** *"Read Committed is the default in Postgres and SQL Server. It prevents dirty reads but a row can change between two reads inside your transaction. If I need a consistent snapshot for a report I use Repeatable Read; for a strict invariant across rows, Serializable — and then I need retry logic, because Serializable fails transactions rather than blocking."*

**Hook:** **Default = Read Committed. Serializable = retry on failure.**

```python
with engine.connect().execution_options(isolation_level="SERIALIZABLE") as conn:
    ...
```

## 7.3 Nested transactions and savepoints

```python
with session.begin():
    session.add(a)
    with session.begin_nested():     # SAVEPOINT
        session.add(b)               # can roll back just this part
```

---

# PART 8 — CONCURRENCY: OPTIMISTIC vs PESSIMISTIC ⭐

## 8.1 Optimistic locking

**Assume no conflict.** Detect it at write time with a version column.

```python
class Order(Base):
    version: Mapped[int] = mapped_column(default=0)
    __mapper_args__ = {"version_id_col": version}
```
SQLAlchemy emits:
```sql
UPDATE orders SET qty=20, version=2 WHERE id=1 AND version=1
```
Zero rows updated → someone else changed it → `StaleDataError`.

## 8.2 Pessimistic locking

**Assume conflict.** Take a real database lock.

```python
order = session.execute(
    select(Order).where(Order.id == 1).with_for_update()      # SELECT ... FOR UPDATE
).scalar_one()
order.qty -= 10
session.commit()                                             # lock released
```

Variants: `with_for_update(nowait=True)` fails immediately instead of waiting;
`skip_locked=True` skips locked rows — that's the queue-worker pattern.

| | Optimistic | Pessimistic |
|---|---|---|
| Lock held | none | a real row lock |
| Conflict found | at write | at read |
| Best when | conflicts are rare | conflicts are likely |
| Cost | retry logic | blocking, deadlock risk |
| Example | editing a profile | debiting a balance |

**Say:** *"Optimistic uses a version column and fails the update if someone else changed the row — cheap when conflicts are rare, but I need a retry path. Pessimistic takes `SELECT FOR UPDATE` and holds a lock, which is what I'd use for a balance debit or position update where a lost update is a real financial error. It's the same choice as EF Core's `[ConcurrencyCheck]` versus an explicit transaction with locking hints."*

**Hook:** **Version column = optimistic. `FOR UPDATE` = pessimistic.**

⚠️ **Deadlocks.** Two transactions locking the same rows in different orders.
*"I prevent them by always acquiring locks in a consistent order — sort by primary key — keeping transactions short, and adding a retry with backoff, because the database will pick a victim and abort it."*

---

# PART 9 — CONNECTION POOLING

```python
engine = create_engine(
    DSN,
    pool_size=20,          # kept open
    max_overflow=10,       # extra, temporary
    pool_timeout=30,       # wait before raising
    pool_recycle=1800,     # recycle before the DB/firewall times them out
    pool_pre_ping=True,    # ⭐ test the connection before handing it out
    echo=False,            # True logs every SQL statement (dev only)
)
```

**Why.** Opening a connection means a TCP handshake, TLS and authentication — milliseconds
each time. A pool reuses them.

**The maths — say it, it shows production experience:**
> *"Total connections is workers × (pool_size + max_overflow). Four Gunicorn workers with a pool of twenty and ten overflow is 120 connections, and Postgres defaults to 100. That's an outage waiting to happen. Either size the pool to fit, or put PgBouncer in front in transaction-pooling mode."*

**Hook:** **workers × pool ≤ the database limit.**

⚠️ **`pool_pre_ping=True` matters in the cloud.** Load balancers and firewalls kill idle
connections silently. Without pre-ping the first request after an idle period fails.

⚠️ **Never fork after creating an engine.** Gunicorn preload plus a pool means children share
file descriptors and corrupt each other. Dispose the pool in the post-fork hook.

---

# PART 10 — MIGRATIONS WITH ALEMBIC

```bash
alembic init migrations
alembic revision --autogenerate -m "add orders table"
alembic upgrade head
alembic downgrade -1
alembic current / history
```

```python
def upgrade():
    op.add_column("orders", sa.Column("venue", sa.String(10), nullable=True))
    op.create_index("ix_orders_venue", "orders", ["venue"])

def downgrade():
    op.drop_index("ix_orders_venue")
    op.drop_column("orders", "venue")
```

⚠️ **Autogenerate is a draft, not an answer.** It misses server defaults, some type changes,
and index renames. **Always read the generated file before committing it.**

## Zero-downtime schema change — the expand/contract answer ⭐

Say all four steps:
> *"**Expand, migrate, contract.** One — add the new column as nullable, with an index created
> concurrently. Two — deploy code that writes both old and new. Three — backfill in batches so
> you never hold a long transaction or lock the table. Four — once everything reads the new
> column, make it non-null and drop the old one in a later release. Every step is
> backwards-compatible, so a rollback never breaks the running version."*

**Hook:** **Add nullable → dual write → backfill → drop.**

**Other production points:**
- Run migrations as a **job before the rollout**, never at app startup — workers would race.
- `CREATE INDEX CONCURRENTLY` in Postgres, so you don't lock writes. It can't run inside a
  transaction, so Alembic needs `autocommit_block()`.
- Adding a NOT NULL column **with a default** rewrites the whole table on older engines.
- Migrations belong in code review. They're the riskiest thing in a deployment.

---

# PART 11 — ASYNC SQLALCHEMY

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine("postgresql+asyncpg://...", pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_orders(symbol: str):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Order).where(Order.symbol == symbol)
                         .options(selectinload(Order.account))   # ⭐ MUST eager load
        )
        return result.scalars().all()
```

⚠️ **Two async-specific traps. Say both:**
1. **Lazy loading doesn't work in async.** Touching an unloaded relationship raises
   `MissingGreenlet`, because a lazy load would need blocking I/O. You must eager load, or use
   `await session.refresh(obj, ["account"])`.
2. **`expire_on_commit=False` is effectively required.** Otherwise every attribute is expired
   after commit and the next access triggers a lazy reload — which then raises.

**Say:** *"Async SQLAlchemy forces you to be explicit about loading, which is arguably a feature — the N+1 becomes a crash in development rather than a slow endpoint in production."*

---

# PART 12 — PERFORMANCE

| Problem | Fix |
|---|---|
| **N+1 queries** | ⭐ `selectinload` / `joinedload`. Always the first thing to check |
| Loading full objects for a report | `select(Order.symbol, Order.qty)` — columns only |
| Loading columns you don't need | `load_only(...)` / `defer(...)` |
| Inserting in a loop | `session.execute(insert(Order), rows)` — bulk |
| Updating in a loop | `update()` statement, not per-object |
| Huge result set in memory | `.yield_per(1000)` / server-side cursors |
| No index on the filter/join column | add it. Match the query's column order |
| Reopening connections | pooling, `pool_pre_ping` |
| Same query repeatedly | cache in Redis |
| Complex reporting through the ORM | drop to Core or raw SQL |
| Can't see what's happening | `echo=True`, or `EXPLAIN ANALYZE` |

**Say:** *"I profile by logging generated SQL and counting queries per request. The order of fixes is: kill the N+1, select fewer columns, batch the writes, then indexes, then caching. Rewriting in raw SQL is last, and only for reporting."*

**Test guard:**
```python
from sqlalchemy import event
# count queries in a test and assert the number — stops N+1 regressions in CI
```

---

# PART 13 — WHEN NOT TO USE AN ORM

**Say this — it shows judgement, and it's a question that separates levels:**

> *"I'd drop out of the ORM for four things. Bulk loads — `COPY` or a bulk insert beats
> thousands of round trips. Complex reporting — window functions, recursive CTEs, pivots are
> clearer as SQL than as ORM contortions. Database-specific features — Postgres JSONB
> operators, full-text search, `LISTEN/NOTIFY`. And anything where the query plan matters more
> than the object model. The ORM earns its place on the transactional path; it doesn't have to
> own everything."*

**The middle ground:** SQLAlchemy Core, or a query builder, or a thin layer like **asyncpg**
directly. You get parameterisation without the object mapping.

**Name the alternatives:**

| Tool | What it is |
|---|---|
| **SQLAlchemy Core** | SQL expression language, no ORM |
| **asyncpg** | fast async Postgres driver, raw SQL |
| **psycopg3** | modern sync/async Postgres driver |
| **Tortoise ORM** | async-native, Django-like API |
| **SQLModel** | Pydantic + SQLAlchemy in one model. FastAPI's author |
| **Peewee** | small Active Record ORM |
| **Dapper** (.NET) | the same philosophy — micro-ORM, you write the SQL |

⚠️ **On SQLModel, have a view:** *"It's elegant because one class is both the API schema and the table. But merging the persistence model and the API contract is exactly the coupling `response_model` exists to prevent, so I'd keep them separate on anything non-trivial."*

---

# PART 14 — THE REPOSITORY PATTERN

```python
class OrderRepository:
    def __init__(self, session: Session):
        self._session = session

    def get(self, order_id: int) -> Order | None:
        return self._session.get(Order, order_id)

    def open_for_account(self, account_id: int) -> list[Order]:
        return self._session.execute(
            select(Order)
            .where(Order.account_id == account_id, Order.filled.is_(False))
            .options(selectinload(Order.account))
        ).scalars().all()

    def add(self, order: Order) -> None:
        self._session.add(order)
```

**The balanced answer — interviewers are looking for the "but":**
> *"A repository puts query logic in one place, keeps ORM imports out of the service layer, and
> makes the data access mockable. The counter-argument is that the SQLAlchemy session and EF's
> `DbContext` are already a repository plus a unit of work, so wrapping them can be a pointless
> layer. My rule: add a repository when the domain logic is complex enough to deserve isolation,
> or when the queries are reused across services. For a CRUD app it's ceremony."*

**Hook:** **The session already is a repository. Add another only when it earns its place.**

---

# PART 15 — NoSQL AND THE ALTERNATIVES

| Type | Examples | Use for |
|---|---|---|
| **Relational** | Postgres, SQL Server, MySQL | ⭐ the default. Transactions, joins, constraints |
| **Document** | MongoDB, Cosmos | flexible schema, denormalised aggregates |
| **Key-value** | Redis, DynamoDB | cache, sessions, rate limits, pub/sub |
| **Columnar** | ClickHouse, kdb+, Redshift | ⭐ analytics, tick data, aggregations over billions of rows |
| **Time-series** | TimescaleDB, InfluxDB | metrics, market data |
| **Graph** | Neo4j | relationship traversal |
| **Search** | Elasticsearch, OpenSearch | full text, log search |
| **Vector** | pgvector, Pinecone | embeddings, semantic search |

**Say:** *"I default to Postgres, because it does JSON, full text, time-series with Timescale and vectors with pgvector — one operational burden instead of five. I'd add a specialist store when a specific access pattern justifies it: Redis for hot reads and rate limiting, a columnar store like ClickHouse or kdb+ for tick-level analytics, because scanning billions of rows column-wise is a fundamentally different shape from row-oriented OLTP."*

**Hook:** **Postgres until a pattern forces otherwise.**

⚠️ **Finance angle worth one line:** *"In capital markets the classic split is a row store for orders and executions — where transactions and constraints matter — and a columnar or time-series store for tick data and analytics, where you scan huge ranges of a few columns. kdb+ is the traditional answer there; ClickHouse and Timescale are the modern open ones."*

---

# PART 16 — ORM COMPARISON

| | **SQLAlchemy** | **Django ORM** | **EF Core** |
|---|---|---|---|
| Pattern | Data Mapper | Active Record | Data Mapper |
| Context | `Session` | implicit | `DbContext` |
| Save | `session.commit()` | `obj.save()` | `SaveChanges()` |
| Query | `select()` | `objects.filter()` | LINQ |
| Eager, many-to-one | `joinedload` | `select_related` | `.Include()` |
| Eager, one-to-many | `selectinload` | `prefetch_related` | `.Include()` |
| Migrations | Alembic | built in | EF Migrations |
| Raw SQL | `text()` | `.raw()` | `FromSqlRaw` |
| Async | yes (2.0) | partial (4.1+) | yes |
| Lazy default | yes | yes | ⚠️ **no** — must opt in |
| Change tracking | session | per instance | context |
| Optimistic lock | `version_id_col` | manual | `[Timestamp]` |
| Bulk | `insert()` executemany | `bulk_create` | `ExecuteUpdate` (EF7+) |

⚠️ **A great detail to drop:** *"EF Core disabled lazy loading by default, precisely because it caused so many N+1 bugs in EF6. SQLAlchemy and Django still default to lazy — which is why `raiseload` and `assertNumQueries` exist."*

---

# PART 17 — RAPID-FIRE: 80 QUESTIONS

| # | Q | A |
|---|---|---|
| 1 | What's an ORM? | Maps rows to objects |
| 2 | Two patterns? | Active Record, Data Mapper |
| 3 | Django's pattern? | Active Record |
| 4 | SQLAlchemy's? | Data Mapper |
| 5 | EF Core's? | Data Mapper |
| 6 | Main ORM benefit? | No boilerplate, parameterised by default |
| 7 | Main ORM risk? | Hides the generated SQL |
| 8 | SQLAlchemy Core? | SQL expression language, no objects |
| 9 | Current API style? | 2.0 — `select()` + `session.execute()` |
| 10 | Money column type? | `Numeric` / `DECIMAL` |
| 11 | Never for money? | `Float` |
| 12 | Nullable in 2.0 typing? | `Mapped[str \| None]` |
| 13 | N+1 problem? | One query per row on a lazy relation |
| 14 | Fix, many-to-one? | `joinedload` — a JOIN |
| 15 | Fix, one-to-many? | `selectinload` — a second query |
| 16 | Why not JOIN for one-to-many? | It multiplies rows |
| 17 | Django equivalents? | `select_related` / `prefetch_related` |
| 18 | EF equivalent? | `.Include()` |
| 19 | Ban lazy loading? | `raiseload("*")` |
| 20 | See the SQL? | `echo=True` |
| 21 | Catch N+1 in CI? | Assert query counts |
| 22 | Session's four jobs? | Identity map, change tracking, unit of work, transaction |
| 23 | Identity map? | One object per PK per session |
| 24 | Unit of work? | Batch changes, flush in one transaction |
| 25 | .NET equivalent? | `DbContext` |
| 26 | Flush vs commit? | Emit SQL vs end the transaction |
| 27 | Why flush early? | To get a generated primary key |
| 28 | Do you call `save()`? | No — attributes are tracked |
| 29 | Session scope? | One per request |
| 30 | Is a session thread-safe? | **No** |
| 31 | Object states? | Transient, pending, persistent, detached, deleted |
| 32 | `DetachedInstanceError`? | Lazy load after the session closed |
| 33 | `expire_on_commit=False`? | Stops attribute reload after commit |
| 34 | ACID? | Atomicity, Consistency, Isolation, Durability |
| 35 | Default isolation? | Read Committed |
| 36 | Dirty read? | Reading uncommitted data |
| 37 | Non-repeatable read? | Same row changes between reads |
| 38 | Phantom read? | Same query returns new rows |
| 39 | Strictest level? | Serializable |
| 40 | Serializable cost? | Failed transactions — needs retry |
| 41 | Savepoint? | `begin_nested()` |
| 42 | Optimistic locking? | Version column, fail on write |
| 43 | Pessimistic locking? | `SELECT ... FOR UPDATE` |
| 44 | Which for a balance debit? | Pessimistic |
| 45 | Which for low contention? | Optimistic |
| 46 | SQLAlchemy optimistic config? | `version_id_col` |
| 47 | Skip locked rows? | `with_for_update(skip_locked=True)` |
| 48 | Queue-worker pattern? | `FOR UPDATE SKIP LOCKED` |
| 49 | Deadlock cause? | Locks acquired in different orders |
| 50 | Deadlock fix? | Consistent order, short transactions, retry |
| 51 | Why pool connections? | Handshake + auth cost per connect |
| 52 | Total connections formula? | workers × (pool_size + overflow) |
| 53 | `pool_pre_ping`? | Test before use. Survives idle drops |
| 54 | `pool_recycle`? | Rotate before the server times them out |
| 55 | Too many connections fix? | PgBouncer |
| 56 | Fork + engine? | Dispose the pool after fork |
| 57 | Migration tool for SQLAlchemy? | Alembic |
| 58 | Generate a migration? | `alembic revision --autogenerate` |
| 59 | Apply? | `alembic upgrade head` |
| 60 | Autogenerate caveat? | It's a draft — always review it |
| 61 | Zero-downtime pattern? | Expand, migrate, contract |
| 62 | Step one? | Add the column nullable |
| 63 | Run migrations when? | A job before rollout |
| 64 | Postgres index without locking? | `CREATE INDEX CONCURRENTLY` |
| 65 | Async engine URL? | `postgresql+asyncpg://` |
| 66 | Async lazy loading? | Fails — `MissingGreenlet` |
| 67 | So you must? | Eager load explicitly |
| 68 | Required async setting? | `expire_on_commit=False` |
| 69 | Bulk insert? | `session.execute(insert(M), rows)` |
| 70 | Bulk update caveat? | Skips events, leaves objects stale |
| 71 | Stream a huge result? | `yield_per` |
| 72 | Fetch fewer columns? | `load_only` / column-only select |
| 73 | When to leave the ORM? | Bulk loads, reporting, DB-specific features |
| 74 | Middle ground? | SQLAlchemy Core |
| 75 | SQLModel? | Pydantic + SQLAlchemy in one class |
| 76 | SQLModel concern? | Couples API contract to the table |
| 77 | Repository pattern gives? | Centralised queries, mockable data access |
| 78 | Counter-argument? | The session already is one |
| 79 | Columnar store use? | Analytics over billions of rows |
| 80 | Default database choice? | Postgres, until a pattern forces otherwise |

---

## ✅ Before you close this file

- [ ] Say the **Part 0** table, all 15
- [ ] Say the **N+1 answer** (Part 5.2) in all three ORMs
- [ ] Say **optimistic vs pessimistic** with the finance example
- [ ] Say the **expand/migrate/contract** four steps
- [ ] Say the **connection maths** (workers × pool)
- [ ] Run the **Part 17** rapid-fire, target 65/80

**Then go back to `07-sql-databases.md` for the SQL itself.**
