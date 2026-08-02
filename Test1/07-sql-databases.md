# 07 — SQL & DATABASES, IN PLAIN ENGLISH

> Must-haves: **SQL proficiency**, **MongoDB or similar**. Nice-to-have: **columnar databases**.
> Luxoft screens very often include *"write this query"*. **Practise Part 8 by hand, on paper.**
>
> **Format:** **Q:** what they ask → **Say:** the words you speak → **Remember:** the hook.

---

# EASY MEMORY NOTES

Read this first. Start with the short phrase. Say the simple line. Add the last column only if they
ask for more.

| Remember | Say it simply | If they ask more |
|---|---|---|
| **Plan first** | For a slow query, check the actual execution plan. | Look for scans, lookups, bad row estimates, and missing indexes. |
| **WHERE can break LEFT** | A `WHERE` filter on the right table can turn `LEFT JOIN` into `INNER JOIN`. | Put that filter in the `ON` clause. |
| **Avoid `NOT IN` with NULL** | `NOT IN` can return nothing if null appears. | Use `NOT EXISTS`. |
| **Window keeps rows** | Window functions add calculations without removing rows. | Use them for ranking, latest row, running totals, and previous value. |
| **Latest row = rank 1** | Use `ROW_NUMBER()` per group and keep row 1. | Partition by the group and order by newest timestamp. |
| **Index covers query** | A covering index has all columns the query needs. | Then SQL can avoid going back to the table. |
| **Index order matters** | In a multi-column index, the first column matters most. | `(symbol, time)` helps symbol searches, not time-only searches. |
| **Do not wrap columns** | Functions around indexed columns can stop index use. | Use date ranges instead of `YEAR(date)`. |
| **Cursor for deep pages** | For big paging, use the last seen id/time. | It stays fast when the page number is huge. |
| **Columnar = reporting** | Columnar databases are good for analytics. | They are not the first choice for live order updates. |

---

# PART 0 — THE 10 SQL ANSWERS THAT WIN

| # | The question | Full answer in simple words |
|---|---|---|
| 1 | **This query is slow. What do you do?** | "I get the actual execution plan first. I look for scans, lookups, bad row estimates, missing indexes, and filters that stop index use. Then I fix one thing and measure again." |
| 2 | **Latest row per group** | "Use `ROW_NUMBER()` over each group, order newest first, and keep row 1. Example: latest price per symbol is partition by symbol and order by timestamp descending." |
| 3 | **The `LEFT JOIN` trap** | "If I put a filter on the right table in `WHERE`, I can accidentally remove the null rows and turn the `LEFT JOIN` into an `INNER JOIN`. The right-side filter belongs in `ON`." |
| 4 | **The `NOT IN` trap** | "`NOT IN` behaves badly when the subquery contains `NULL`; it can return no rows. I use `NOT EXISTS` because it handles this safely." |
| 5 | **Covering index** | "A covering index contains all columns the query needs. Then SQL can answer from the index and does not need to go back to the table for missing columns." |
| 6 | **Composite index order** | "In a multi-column index, the first column matters most. An index on `(symbol, time)` helps queries by symbol, but not a query filtering only by time." |
| 7 | **SARGable** | "The simple idea is: write filters so indexes can be used. Do not wrap indexed columns in functions. Use date ranges instead of `YEAR(date)`." |
| 8 | **Deadlocks** | "A deadlock happens when two transactions each hold something the other needs. I reduce this by touching tables in the same order and retrying safely if the database picks my transaction as the victim." |
| 9 | **Money in the database** | "Use `DECIMAL` for money, never `FLOAT`. This matches `decimal` in C# and `Decimal` in Python." |
| 10 | **Deep pagination** | "`OFFSET` gets slower on deep pages because the database still walks past earlier rows. Cursor or keyset paging uses the last seen key and stays fast." |

---

# PART 1 — JOINS

| Join | Returns |
|---|---|
| `INNER` | Only rows that match in both |
| `LEFT` | Everything on the left, plus matches on the right (`NULL` where there's no match) |
| `RIGHT` | The mirror image |
| `FULL OUTER` | Everything from both, `NULL` where there's no match |
| `CROSS` | Every combination — the cartesian product |
| `SELF` | A table joined to itself (manager/employee, previous/next trade) |

## ⚠️ The trap they use

```sql
-- This is secretly an INNER JOIN. The WHERE removes every NULL row the LEFT JOIN created.
SELECT * FROM orders o LEFT JOIN fills f ON f.order_id = o.id
WHERE f.venue = 'LSE';

-- Correct: the condition belongs in the ON clause
SELECT * FROM orders o LEFT JOIN fills f ON f.order_id = o.id AND f.venue = 'LSE';
```

**Remember:** **A `WHERE` on the right table cancels the `LEFT`.**

## `UNION`, `EXISTS`, `NOT IN`

- **`UNION` removes duplicates and sorts to do it — that costs.** `UNION ALL` doesn't. Use `UNION ALL`
  unless you genuinely need deduplication.
- **`EXISTS` short-circuits** — it stops at the first match — and it handles `NULL` safely.
- ⚠️ **`NOT IN` with a `NULL` in the subquery returns no rows at all.**
  **Say:** *"It's because `x NOT IN (1, NULL)` evaluates to unknown, not true. It's a famous
  production bug. I use `NOT EXISTS`, which behaves correctly."*

---

# PART 2 — WINDOW FUNCTIONS (the senior differentiator)

**Say what they are, simply:** *"A window function calculates across a set of rows related to the
current row, but **without collapsing them** the way `GROUP BY` does. You keep every row and get the
aggregate alongside it."*

```sql
SELECT
    trade_id, symbol, trade_ts, price, quantity,

    ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY trade_ts DESC)        AS rn,
    RANK()       OVER (PARTITION BY symbol ORDER BY quantity DESC)        AS qty_rank,

    SUM(quantity) OVER (PARTITION BY symbol ORDER BY trade_ts
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_qty,

    AVG(price)    OVER (PARTITION BY symbol ORDER BY trade_ts
                        ROWS BETWEEN 19 PRECEDING AND CURRENT ROW)        AS ma20,

    LAG(price)    OVER (PARTITION BY symbol ORDER BY trade_ts)            AS prev_price,
    price - LAG(price) OVER (PARTITION BY symbol ORDER BY trade_ts)       AS price_change
FROM trades;
```

**The three ranking functions — know the difference exactly:**

| Given values 10, 10, 9 | Result |
|---|---|
| `ROW_NUMBER()` | 1, 2, 3 — always distinct |
| `RANK()` | 1, 1, 3 — ties share, then it **skips** |
| `DENSE_RANK()` | 1, 1, 2 — ties share, **no gap** |

⚠️ **`ROWS` vs `RANGE`:** *"`ROWS` counts physical rows. `RANGE` groups rows with the same value — the
peers. And the default frame when you write `ORDER BY` is `RANGE`, not `ROWS`, which quietly changes
your running total when there are ties. I always specify `ROWS` explicitly."*

## The most common real interview question: latest row per group

```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY trade_ts DESC) AS rn
    FROM trades
)
SELECT * FROM ranked WHERE rn = 1;
```
**Alternatives to name:** `CROSS APPLY (SELECT TOP 1 ...)` in SQL Server, `DISTINCT ON` in PostgreSQL.

## CTEs and recursion

```sql
WITH org AS (
    SELECT id, manager_id, name, 0 AS lvl FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.manager_id, e.name, org.lvl + 1
    FROM employees e JOIN org ON e.manager_id = org.id
)
SELECT * FROM org;
```
**Say:** *"A CTE is a named subquery — mostly for readability. A **recursive** CTE walks a hierarchy:
an anchor query, then a part that joins back to the CTE itself. Org charts, bills of materials,
portfolio trees."*

---

# PART 3 — INDEXES

## 3.1 The two kinds

**Say:** *"A **clustered** index is the physical order of the rows — the leaf level **is** the data,
so you only get one per table. In SQL Server the primary key is clustered by default.*

*A **non-clustered** index is a separate B-tree of the key plus a pointer back. If the query needs a
column that isn't in the index, the engine has to go back to the table — that's a **key lookup**, and
eliminating it is often the whole optimisation."*

## 3.2 Covering index — the answer to "make this faster"

```sql
CREATE INDEX IX_trades_symbol_ts
    ON trades (symbol, trade_ts)
    INCLUDE (price, quantity);       -- now the query never touches the table
```

**Say:** *"A covering index contains every column the query needs. The key columns go in the key, the
rest go in `INCLUDE`. The query is answered from the index alone — no key lookup. That's usually the
single biggest win available."*

## 3.3 Composite index order — leftmost prefix

**Say:** *"Column order matters enormously. An index on `(symbol, trade_ts)` helps a query filtering
on `symbol`, and helps one filtering on `symbol` **and** `trade_ts`. It does **nothing** for a query
filtering only on `trade_ts` — because you can't use the second column without the first. That's the
leftmost-prefix rule. Think of a phone book sorted by surname then first name."*

**Remember:** **Phone book. Surname first, or it's useless.**

## 3.4 SARGability — the word to use

**Say:** *"SARGable means the predicate can use an index seek. Wrap the column in a function and it
can't."*

```sql
WHERE YEAR(trade_ts) = 2026                                    -- ✗ scan
WHERE trade_ts >= '2026-01-01' AND trade_ts < '2027-01-01'     -- ✓ seek

WHERE CAST(id AS varchar) = '5'                                -- ✗
WHERE id = 5                                                   -- ✓

WHERE symbol LIKE '%BM'                                        -- ✗ leading wildcard
WHERE symbol LIKE 'IB%'                                        -- ✓
```

## 3.5 The rest, ready to go

- **Selectivity:** an index only helps if it eliminates most rows. An index on a yes/no column is
  usually useless.
- **Cost:** every index slows every `INSERT`, `UPDATE` and `DELETE`, and takes space and memory.
  *"I index the reads I actually run — and I check `sys.dm_db_index_usage_stats` for indexes nobody
  uses."*
- **Filtered index** — `WHERE status='OPEN'`. Small and hot.
- **Statistics** — the optimiser guesses row counts from statistics. **Stale statistics give bad
  plans.** That's a common answer to "it was fast last week".
- ⚠️ **Parameter sniffing** — *"SQL Server caches the plan built for the **first** parameter value it
  saw. If that value was unusual, every later execution gets a terrible plan. Fixes are
  `OPTIMIZE FOR UNKNOWN`, `RECOMPILE`, or a local variable."*
  **Naming parameter sniffing unprompted is a strong senior signal.**

---

# PART 4 — EXECUTION PLANS

**State a method, not tricks. Say:**

> *"I take the **actual** execution plan, not the estimated one. I look for the operator consuming the
> most cost, and — more importantly — where the **estimated row count is badly different from the
> actual**, because that's where the optimiser was misled. Then I work out whether it's a missing
> index, an index-unfriendly filter, stale statistics, or a bad join choice.
> **Fix one thing,
> re-measure.**"*

**Operators to recognise:**

| Operator | Means |
|---|---|
| **Index Seek** | Good — going straight to the rows |
| **Table / Index Scan** | Reading everything. Fine on a small table, bad on a big one |
| **Key Lookup** | Going back to the table for missing columns → **fix with a covering index** |
| **Nested Loops** | Good when the outer input is small |
| **Hash Match** | Big unsorted sets; needs memory, and spills to disk if it doesn't get enough |
| **Merge Join** | Both inputs already sorted |
| **Sort / Spool** | Often a smell |

⚠️ **Say this:** *"The percentages in the plan are estimates and can lie. **Thick arrows and
estimated-versus-actual row mismatches are the real clues.**"*

**Tools:** `SET STATISTICS IO, TIME ON` — *"logical reads is the honest metric, because it doesn't
change with caching"* — plus Query Store and Extended Events. PostgreSQL:
`EXPLAIN (ANALYZE, BUFFERS)` and `pg_stat_statements`.

---

# PART 5 — TRANSACTIONS AND ISOLATION

**ACID:** Atomic (all or nothing) · Consistent (invariants hold) · Isolated (as if alone) ·
Durable (survives a crash).

| Level | Stops | Still allows |
|---|---|---|
| Read Uncommitted | nothing | Dirty reads |
| **Read Committed** (default) | Dirty reads | Non-repeatable reads, phantoms |
| Repeatable Read | + non-repeatable reads | Phantoms |
| **Serializable** | everything | (lowest concurrency) |
| **Snapshot / RCSI** | Readers never block writers (MVCC) | You must handle write conflicts |

**Define the anomalies crisply — they may just ask:**
- **Dirty read** — you read data another transaction hasn't committed yet.
- **Non-repeatable read** — you read the same row twice and get different values.
- **Phantom read** — you run the same range query twice and new rows have appeared.
- **Lost update** — two transactions read, both write, one silently wins.

## Deadlocks

**Say:** *"Two transactions each hold a lock the other needs. Prevention is **consistent access
order** — the same answer as in threading. Plus short transactions, and good indexes so you lock fewer
rows. SQL Server detects it and kills one as the victim with **error 1205**, so the application should
catch that specific number and retry with jittered backoff."*

```csharp
catch (SqlException ex) when (ex.Number == 1205) { /* retry with jitter */ }
```

**Q: Optimistic or pessimistic for an order or position update?**
**Say:** *"Optimistic, with a `rowversion` token, retrying on conflict. Holding database locks across
user think-time destroys throughput — and in a trading system, contention on a hot instrument would
be exactly where it hurts most."*

---

# PART 6 — MODELLING AND SCALE

- **Normalisation to 3NF:** *"Every non-key attribute depends on **the key, the whole key, and nothing
  but the key**."* Then: *"and I denormalise deliberately for read performance, and say why."*
- **OLTP vs OLAP:** normalised row store with short transactions, versus a star schema on columnar
  storage doing scans and aggregates. **This role almost certainly has both** — an order/position
  store and an analytics side.
- **Star schema:** a fact table (trades, positions) surrounded by dimensions (instrument,
  counterparty, date).
- **Slowly Changing Dimension Type 2** — *"a new row with valid-from and valid-to dates. That's how
  you keep **point-in-time correctness**, which finance cares about deeply: 'what did we believe the
  credit rating was on 12 March?' You need the answer as of then, not as of now."* **Raise this — it
  shows domain instinct.**
- **Temporal tables** (SQL Server `SYSTEM_VERSIONING`) — automatic history. A strong answer for audit.
- **Partitioning by date** on huge trade/tick tables → partition elimination, and archival becomes
  switching a partition out rather than deleting millions of rows.
- **Bitemporal data** — valid time versus transaction time. *"It's the gold standard in finance and
  few candidates know the term."* Mention it if the domain comes up.

---

# PART 7 — MONGODB AND COLUMNAR

## 7.1 MongoDB

**Q: When would you use it — and when not?**
**Say:** *"I'd use it when the schema varies or evolves, when the aggregate is read as a whole, for
high write throughput, or for denormalised read models. I would **not** use it for multi-entity
transactional consistency, heavy ad-hoc joins, or reporting."*

**That second half is what they're actually checking — knowing when *not* to use it.**

**Embed vs reference:** *"Embed when the data is accessed together and is **bounded**. Reference when
it's shared, unbounded, or updated independently."*

⚠️ *"The two traps are the **16 MB document limit** and the **unbounded array anti-pattern** — like
embedding every trade inside a client document. It works for six months and then it doesn't."*

**Indexes:** single, compound, multikey (arrays), text, geo, **TTL** (auto-expiry — good for market
data snapshots), partial.
**The compound key order rule is ESR: Equality, then Sort, then Range.**

**Aggregation pipeline** — ⚠️ **put `$match` first** so it can use an index and cut the working set:
```js
db.trades.aggregate([
  { $match: { ts: { $gte: ISODate("2026-07-01") }, status: "FILLED" } },
  { $group: { _id: "$symbol", notional: { $sum: { $multiply: ["$qty", "$price"] } } } },
  { $sort: { notional: -1 } },
  { $limit: 20 }
])
```

**Consistency:** replica sets with a primary and secondaries, **write concern** (`w:1` vs
`w:"majority"` vs `j:true`) and read concern.
**Say:** *"`w:majority` for anything I can't afford to lose."*

**Sharding:** *"The shard key is effectively irreversible and it decides everything. Avoid a
monotonically increasing key — every write lands on the same shard. It's the identical lesson as
partition key design in Cosmos DB."*

**The line to say:** *"I choose the store against the access pattern"* — then give one concrete
example from your own work.

## 7.2 Columnar and time-series (the nice-to-have that impresses)

| | Row store (OLTP) | Column store (OLAP) |
|---|---|---|
| Layout | The whole row is contiguous | The whole **column** is contiguous |
| Great at | Reading or writing one full record | Scanning a few columns across billions of rows |
| Compression | Poor | **Excellent** — similar values sit next to each other |
| Extras | | Vectorised execution, column pruning, predicate pushdown |

**Names to know:** **SQL Server columnstore indexes** (*the one to mention in a Microsoft shop*),
**ClickHouse**, **kdb+/q** (*the classic tick database in capital markets — knowing the name is a real
signal*), **DuckDB**, **Parquet** + Arrow, TimescaleDB, QuestDB.

**Say this — it's a complete, senior answer:**
> *"For a tick store I'd separate the workloads. An OLTP row store for orders and positions, where
> correctness and point updates matter. And a **columnar** store — columnstore indexes, or
> Parquet/ClickHouse depending on scale — for tick history and analytics, because those queries scan
> two or three columns across billions of rows and compress ten times or better. Partition by date,
> and the analytics side is append-only, which makes archival trivial."*

**Time-series specifics worth naming:** irregular timestamps, **as-of joins** (the `merge_asof`
concept from `06`), gap filling, downsampling into OHLC bars, retention and rollup policies. And
*"never join tick data with an equals on the timestamp"* — the timestamps never match exactly.

---

# PART 8 — ✍️ WRITE THESE BY HAND (the classics)

1. **Second-highest value per group** — with and without window functions.
2. **Latest row per group** (Part 2).
3. **Find duplicates and delete all but one:**
   ```sql
   WITH d AS (
       SELECT *, ROW_NUMBER() OVER (PARTITION BY symbol, trade_ts, qty ORDER BY id) rn
       FROM trades
   )
   DELETE FROM d WHERE rn > 1;
   ```
4. **Running total and moving average** (Part 2).
5. **Employees earning more than their manager** — a self-join.
6. **Gaps in a sequence / missing dates** — a calendar table with a `LEFT JOIN`.
7. **Pivot monthly totals by symbol** — `PIVOT`, or conditional `SUM(CASE WHEN ...)`.
8. **Day-over-day change** with `LAG`.
9. **Top N per category** — `ROW_NUMBER() <= N`.
10. **Customers with no orders** — `NOT EXISTS`, and be ready to explain why not `NOT IN`.

Also be able to write an **upsert** (`MERGE`), a transaction with error handling
(`BEGIN TRY / ROLLBACK / THROW`), and a simple stored procedure with parameters.

---

# PART 9 — RAPID-FIRE: 40 QUESTIONS

| # | Q | A |
|---|---|---|
| 1 | `WHERE` vs `HAVING` | Before aggregation vs after |
| 2 | `DELETE` vs `TRUNCATE` vs `DROP` | Row by row and triggers fire / fast, minimally logged, resets identity / removes the object |
| 3 | `INNER` vs `LEFT` join | Only matches vs everything on the left |
| 4 | The `LEFT JOIN` trap | A `WHERE` on the right table makes it an `INNER JOIN` |
| 5 | `UNION` vs `UNION ALL` | Deduplicates (costs a sort) vs doesn't |
| 6 | `NOT IN` with `NULL` | Returns **no rows**. Use `NOT EXISTS` |
| 7 | `EXISTS` vs `IN` | Short-circuits, NULL-safe vs materialises the list |
| 8 | `NULL = NULL` | Unknown, not true. Use `IS NULL` |
| 9 | `COUNT(*)` vs `COUNT(col)` | All rows vs non-null values only |
| 10 | `ROW_NUMBER` / `RANK` / `DENSE_RANK` | 1,2,3 / 1,1,3 / 1,1,2 |
| 11 | Latest row per group | `ROW_NUMBER() OVER (PARTITION BY … ORDER BY ts DESC) = 1` |
| 12 | `LAG` / `LEAD` | The previous / next row's value |
| 13 | `ROWS` vs `RANGE` | Physical rows vs value peers. Default is `RANGE` — specify `ROWS` |
| 14 | CTE | A named subquery; recursive ones walk hierarchies |
| 15 | Clustered index | The physical row order. One per table. The leaf **is** the data |
| 16 | Non-clustered index | A separate B-tree plus a pointer back |
| 17 | Key lookup | Going back to the table for missing columns. Kill it with a covering index |
| 18 | Covering index | Contains every column the query needs — `INCLUDE` |
| 19 | Composite index order | Leftmost prefix. Like a phone book |
| 20 | SARGable | The predicate can seek. Functions on a column kill it |
| 21 | Selectivity | An index only helps if it eliminates most rows |
| 22 | Cost of an index | Slows every write, uses space and memory |
| 23 | Statistics | The optimiser's row-count estimates. Stale stats → bad plans |
| 24 | Parameter sniffing | The plan is cached for the first parameter value seen |
| 25 | Tuning method | Actual plan → biggest estimate error → one fix → re-measure |
| 26 | Honest perf metric | **Logical reads** — unaffected by caching |
| 27 | ACID | Atomic, Consistent, Isolated, Durable |
| 28 | Default isolation level | Read Committed |
| 29 | Dirty read | Reading uncommitted data |
| 30 | Phantom read | New rows appear in the same range query |
| 31 | Snapshot / RCSI | MVCC — readers never block writers |
| 32 | Deadlock prevention | **Consistent access order**, short transactions, better indexes |
| 33 | Deadlock error number | **1205** — catch it and retry with jitter |
| 34 | Optimistic concurrency | A `rowversion` in the `WHERE`; zero rows affected means conflict |
| 35 | Money type | `DECIMAL`. **Never `FLOAT`** |
| 36 | Deep pagination | `OFFSET` degrades. Use **keyset** paging |
| 37 | Preventing SQL injection | Parameterised queries, always. Never string concatenation |
| 38 | Scalar UDF in a `SELECT` | A classic performance killer (though 2019+ can inline them) |
| 39 | View vs indexed view | A stored query vs a stored **result** |
| 40 | Cursor | Almost always replaceable by a set-based query — say so |
