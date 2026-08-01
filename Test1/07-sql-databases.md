# 07 — SQL, MongoDB, Columnar & Data

> Must-haves: **SQL proficiency**, **MongoDB or similar unstructured**. Nice-to-have:
> **columnar and relational databases**. Luxoft screens often include *"write this query"*.
> Practise §9 **by hand, on paper**.

---

## 1. Joins & set operations — no hesitation allowed

| Join | Returns |
|---|---|
| `INNER` | Rows matching in both |
| `LEFT` | All left + matched right (NULLs where no match) |
| `RIGHT` | Mirror of left |
| `FULL OUTER` | Everything, NULLs on both sides |
| `CROSS` | Cartesian product |
| `SELF` | Table joined to itself (manager/employee, prev/next trade) |

⚠️ Classic trap: a predicate on the right table in the **`WHERE`** clause turns a `LEFT JOIN` into an
`INNER JOIN`. Put it in the **`ON`** clause instead.

`UNION` (dedupes, sorts — costly) vs `UNION ALL` (no dedupe, fast — use unless you need dedupe).
`EXCEPT`/`INTERSECT`. `EXISTS` vs `IN` vs `JOIN`: `EXISTS` short-circuits and handles NULLs safely;
⚠️ **`NOT IN` with a NULL in the subquery returns no rows** — a famous production bug. Use
`NOT EXISTS`.

---

## 2. Window functions — the senior differentiator

```sql
SELECT
    trade_id, symbol, trade_ts, price, quantity,
    ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY trade_ts DESC)      AS rn,
    RANK()       OVER (PARTITION BY symbol ORDER BY quantity DESC)      AS qty_rank,
    SUM(quantity) OVER (PARTITION BY symbol ORDER BY trade_ts
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_qty,
    AVG(price)   OVER (PARTITION BY symbol ORDER BY trade_ts
                        ROWS BETWEEN 19 PRECEDING AND CURRENT ROW)      AS ma20,
    LAG(price)   OVER (PARTITION BY symbol ORDER BY trade_ts)           AS prev_price,
    price - LAG(price) OVER (PARTITION BY symbol ORDER BY trade_ts)     AS price_delta
FROM trades;
```

- `ROW_NUMBER` (1,2,3) vs `RANK` (1,1,3 — gaps) vs `DENSE_RANK` (1,1,2 — no gaps) vs `NTILE(n)`.
- `LAG`/`LEAD`, `FIRST_VALUE`/`LAST_VALUE`, `PERCENTILE_CONT`.
- **`ROWS` vs `RANGE`**: `ROWS` counts physical rows; `RANGE` groups peer values (ties). Default frame
  when you specify `ORDER BY` is `RANGE UNBOUNDED PRECEDING AND CURRENT ROW` — a subtle bug source.
- **"Latest row per group"** — the most common real interview question:
  ```sql
  WITH ranked AS (
      SELECT *, ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY trade_ts DESC) rn
      FROM trades
  ) SELECT * FROM ranked WHERE rn = 1;
  ```
  (Alternatives: `CROSS APPLY (SELECT TOP 1 ...)` in SQL Server, `DISTINCT ON` in PostgreSQL.)

**CTEs**: `WITH x AS (...)` for readability; **recursive CTEs** for hierarchies:
```sql
WITH RECURSIVE org AS (
    SELECT id, manager_id, name, 0 AS lvl FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.manager_id, e.name, org.lvl + 1
    FROM employees e JOIN org ON e.manager_id = org.id
) SELECT * FROM org;
```
(SQL Server: `WITH org AS` — no `RECURSIVE` keyword.)

---

## 3. Indexes — how to talk about them

- **Clustered index** = the physical row order; **one per table**; the leaf *is* the data. In SQL
  Server the PK is clustered by default.
- **Non-clustered** = separate B-tree of key + a pointer (the clustering key / RID). A lookup back to
  the base table is a **key lookup** — often the thing to eliminate.
- **Covering index** = includes every column the query needs (`INCLUDE (...)`) → **index-only scan**,
  no lookup. *The* answer to "how do you speed up this query".
- **Composite index column order matters**: leftmost-prefix rule. `(symbol, trade_ts)` serves
  `WHERE symbol=?` and `WHERE symbol=? AND trade_ts>?`, but **not** `WHERE trade_ts>?` alone.
- **Filtered/partial index** (`WHERE status='OPEN'`) — small and hot.
- **Selectivity**: indexes help when they eliminate most rows. A gender column index is useless.
- **Costs**: every index slows `INSERT/UPDATE/DELETE` and consumes space and memory. Index the reads
  you actually run — check `sys.dm_db_index_usage_stats` for unused ones.
- **SARGability** ⚠️: wrapping a column in a function kills index use.
  ```sql
  WHERE YEAR(trade_ts) = 2026                    -- ✗ scan
  WHERE trade_ts >= '2026-01-01' AND trade_ts < '2027-01-01'   -- ✓ seek
  ```
  Same for `WHERE CAST(id AS varchar) = '5'` and leading-wildcard `LIKE '%abc'`.
- **Fragmentation**, `FILLFACTOR`, statistics and `UPDATE STATISTICS` — stale stats → bad plans.
- **Parameter sniffing** (SQL Server): the plan is cached for the first parameter value and may be
  terrible for others. Fixes: `OPTIMIZE FOR UNKNOWN`, `RECOMPILE`, local variables, or plan guides.
  **Naming parameter sniffing unprompted is a strong senior signal.**

---

## 4. Execution plans & tuning method

State a **method**, not tricks:
> *"Capture the actual plan, find the operator consuming the most cost and the biggest row-count
> estimate error, then work out whether it's a missing index, a non-SARGable predicate, stale
> statistics, or a bad join type. Fix one thing, re-measure."*

Operators to recognise: **Table/Clustered Index Scan** (reading everything — often fine for small
tables, bad for big), **Index Seek** (good), **Key Lookup** (fix with a covering index), **Nested
Loops** (small outer), **Hash Match** (big unsorted sets, needs memory), **Merge Join** (both sorted),
**Sort** / **Spool** (often a smell), **parallelism** operators.
⚠️ **Thick arrows and estimated-vs-actual row mismatches are the real clues**, not the percentages.

Tools: `SET STATISTICS IO, TIME ON` (logical reads is the honest metric), Query Store,
`sys.dm_exec_query_stats`, Extended Events; PostgreSQL: `EXPLAIN (ANALYZE, BUFFERS)`, `pg_stat_statements`.

---

## 5. Transactions, isolation & locking

**ACID**: Atomicity, Consistency, Isolation, Durability.

| Isolation level | Prevents | Still allows |
|---|---|---|
| Read Uncommitted | — | Dirty reads |
| **Read Committed** (default) | Dirty reads | Non-repeatable reads, phantoms |
| Repeatable Read | + non-repeatable reads | Phantoms |
| **Serializable** | everything | (lowest concurrency) |
| **Snapshot / RCSI** (MVCC) | readers never block writers | write conflicts must be handled |

Anomalies to define crisply: **dirty read** (uncommitted data), **non-repeatable read** (same row,
different value), **phantom read** (new rows appear in the same range), **lost update**.

**Deadlocks**: two transactions each holding a lock the other needs. Prevention: **consistent access
order** (same as `04` §5), short transactions, appropriate indexes (lock fewer rows), lower isolation
where safe. Detection: SQL Server picks a victim (error **1205**) — retry with backoff:
```csharp
catch (SqlException ex) when (ex.Number == 1205) { /* retry with jitter */ }
```

**Pessimistic vs optimistic** — for an order book / position update, the standard answer is
optimistic concurrency with a `rowversion`, retrying on conflict, because holding locks across user
think-time destroys throughput.

---

## 6. Modelling & scale

- **Normalisation** 1NF→3NF (each non-key attribute depends on the key, the whole key, and nothing
  but the key); **denormalise deliberately** for read performance and say why.
- **OLTP vs OLAP**: normalised, row-store, short transactions vs star/snowflake schema, columnar,
  scans and aggregates. **This role likely has both** — an OLTP order/position store and an
  analytics/reporting side.
- **Star schema**: fact table (trades, positions) + dimensions (instrument, counterparty, date).
- **Slowly changing dimensions** — Type 2 (a new row with valid-from/valid-to) is how you keep
  **point-in-time correctness**, which finance cares about deeply (*"what did we think the rating was
  on 12 March?"*). Great thing to raise.
- **Temporal tables** (SQL Server `SYSTEM_VERSIONING`) — automatic history; a strong answer for audit
  requirements.
- **Partitioning** by date for large trade/tick tables → partition elimination and cheap archival
  (switch out a partition instead of deleting rows).
- **Sharding**, read replicas, CQRS read models — your CV already covers these; connect them.
- **Bitemporal** data (valid time vs transaction time) — mention it if the domain comes up; it's the
  gold standard in finance and few candidates know the term.

---

## 7. MongoDB / document stores

**When to use it:** varying or evolving schema, aggregates read as a whole, high write throughput,
denormalised read models. **When NOT to:** multi-entity transactional consistency, heavy ad-hoc joins,
reporting — say this, because "knows when *not* to use Mongo" is what they're checking.

- **Document model**: embed when data is accessed together and bounded; reference when it's shared,
  unbounded, or independently updated. ⚠️ **16 MB document limit** and the *unbounded array
  anti-pattern* (e.g. embedding every trade in a client document).
- **Indexes**: single, compound (**ESR rule**: Equality → Sort → Range for compound key order),
  multikey (arrays), text, geo, **TTL** (auto-expiry — good for market data snapshots), partial,
  wildcard.
- **Aggregation pipeline**: `$match` → `$group` → `$sort` → `$project` → `$lookup` → `$facet`.
  ⚠️ Put `$match` **first** so it can use an index and cut the working set.
  ```js
  db.trades.aggregate([
    { $match: { ts: { $gte: ISODate("2026-07-01") }, status: "FILLED" } },
    { $group: { _id: "$symbol", notional: { $sum: { $multiply: ["$qty", "$price"] } }, n: { $sum: 1 } } },
    { $sort: { notional: -1 } }, { $limit: 20 }
  ])
  ```
- **Consistency**: replica sets, primary/secondary, **write concern** (`w:1`, `w:"majority"`,
  `j:true`) and **read concern**/read preference. Say: *"`w:majority` for anything I can't lose."*
- **Transactions** exist (4.0 single-replica-set, 4.2 sharded) but are a smell if you need them
  constantly — that usually means a relational model.
- **Sharding**: shard key choice is irreversible-ish and decisive; avoid monotonically increasing keys
  (hot shard) — same lesson as Cosmos DB partition keys, which you already have on your CV.
- Cross-reference: **Cosmos DB** RU/s, partition key design, change feed; **DynamoDB** single-table
  design and access-pattern-first modelling. You have all three — say *"I choose the store against the
  access pattern"* and give one concrete example.

---

## 8. Columnar & time-series (the nice-to-have that impresses)

**Row-store vs column-store:**

| | Row (OLTP) | Column (OLAP) |
|---|---|---|
| Layout | Whole row contiguous | Whole column contiguous |
| Great at | Point reads/writes of a full record | Scanning/aggregating a few columns over billions of rows |
| Compression | Poor | **Excellent** — like values adjacent (RLE, dictionary, delta) |
| Extras | | Vectorised execution, column pruning, predicate pushdown, min/max zone maps |

Names to know: **SQL Server columnstore indexes** (clustered for the fact table, non-clustered for
real-time operational analytics on an OLTP table — *this is the one to mention for a Microsoft shop*),
**ClickHouse**, **kdb+/q** (the classic tick database in capital markets — knowing the name is a real
signal), **DuckDB**, Snowflake, Redshift, BigQuery, **Apache Parquet** + Arrow, TimescaleDB,
InfluxDB, QuestDB.

**Say this:**
> *"For a tick store I'd separate the workloads: an OLTP row store for orders and positions where
> correctness and point updates matter, and a columnar store — columnstore indexes, or Parquet/
> ClickHouse depending on scale — for tick history and analytics, because those queries scan a couple
> of columns over billions of rows and compress 10× or better. Partition by date, and the analytics
> side becomes append-only which makes archival trivial."*

Also worth knowing: **time-series specifics** — irregular timestamps, as-of joins (`merge_asof` in
`06`), gap filling, downsampling to OHLC bars, retention/rollup policies, and *never* joining
tick-level data with `=` on timestamps.

---

## 9. ✍️ Write these by hand this weekend (they're the classics)

1. **Second-highest salary / price** per group — with and without window functions.
2. **Latest row per group** (§2).
3. **Find duplicates** and delete all but one:
   ```sql
   WITH d AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY symbol, trade_ts, qty ORDER BY id) rn FROM trades)
   DELETE FROM d WHERE rn > 1;
   ```
4. **Running total / moving average** (§2).
5. **Employees earning more than their manager** (self-join).
6. **Gaps in a sequence** / missing dates (calendar table `LEFT JOIN`).
7. **Pivot** monthly totals by symbol (`PIVOT` or conditional `SUM(CASE WHEN ...)`).
8. **Day-over-day change** with `LAG`.
9. **Top-N per category** (`ROW_NUMBER` ≤ N, or `CROSS APPLY TOP N`).
10. **Anti-join**: customers with no orders (`NOT EXISTS`, and explain why not `NOT IN`).

Also be able to write: a `MERGE`/upsert, a transaction with error handling
(`BEGIN TRY / ROLLBACK / THROW`), and a simple stored procedure with parameters.

---

## 10. Rapid-fire

1. `WHERE` vs `HAVING` → before vs after aggregation.
2. `DELETE` vs `TRUNCATE` vs `DROP` → logged row-by-row & triggers fire / fast, minimally logged,
   resets identity, needs no FK references / removes the object.
3. `CHAR` vs `VARCHAR` vs `NVARCHAR` → fixed / variable / Unicode.
4. `NULL` semantics → `NULL = NULL` is unknown; use `IS NULL`; aggregates ignore NULLs except
   `COUNT(*)`.
5. `COUNT(*)` vs `COUNT(col)` → all rows vs non-null values.
6. Primary vs unique key → one, not null vs many, allows one NULL (SQL Server).
7. Stored procedure vs function → can modify data & has side effects vs must be deterministic-ish and
   usable in a query; ⚠️ scalar UDFs in a `SELECT` are a classic performance killer (though SQL Server
   2019+ can inline them).
8. View vs materialised/indexed view → stored query vs stored *result* (fast reads, write cost).
9. Trigger → use sparingly; hidden control flow, hard to debug.
10. Cursor → almost always replaceable by a set-based query; say so.
11. `OFFSET/FETCH` pagination vs **keyset/seek** pagination → deep offsets get slow; keyset
    (`WHERE (ts, id) < (@ts, @id) ORDER BY ts DESC, id DESC`) stays constant-time. Great answer.
12. `sp_executesql` vs dynamic string SQL → parameterised, plan-cacheable, injection-safe.
13. How do you prevent SQL injection? → parameterised queries always; never string concatenation;
    least-privilege DB accounts; ORMs parameterise by default (but `FromSqlRaw` with interpolation
    does not — use `FromSqlInterpolated`).
14. Connection pooling → pools are per connection-string; leaked connections exhaust the pool; always
    dispose.
15. Read replica lag → eventual consistency; don't read-your-own-write from a replica without care.
