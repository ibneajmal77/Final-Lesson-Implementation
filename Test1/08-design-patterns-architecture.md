# 08 — Design Patterns, Algorithms & System Design

> JD must-haves: **"design patterns and algorithms proficiency"**, **"distributed design"**,
> **"service-oriented architecture"**, **"solution architecture background"**.

---

## PART A — DESIGN PATTERNS

Rule: **never define a pattern — give the problem it solved on your project.** A definition sounds
like revision; a war story sounds like experience.

### A1. Creational

| Pattern | One-liner | Real use |
|---|---|---|
| **Factory Method** | Subclass decides which concrete type | `IPartnerAdapterFactory` picking the right EDI/FIX adapter per counterparty |
| **Abstract Factory** | Families of related objects | Per-environment sets of providers |
| **Builder** | Step-by-step construction of a complex object | Building an order request with 20 optional fields; fluent test data builders |
| **Prototype** | Clone an existing instance | Copying a template order / strategy config |
| **Singleton** | One instance | ⚠️ Say: *"I use DI singleton lifetime, not the static Singleton pattern — it's testable and explicit."* Strong senior answer. |

### A2. Structural

| Pattern | One-liner | Real use |
|---|---|---|
| **Adapter** | Make an incompatible interface fit | Wrapping a vendor market-data SDK behind `IPriceSource` |
| **Facade** | Simple front over a complex subsystem | One `IBookingFacade` over five services |
| **Decorator** | Add behaviour without changing the type | **Caching / retry / logging decorators over a repository** — a great answer, and how MediatR pipeline behaviours work |
| **Proxy** | Stand-in controlling access | Lazy loading in EF; a remoting/gRPC client proxy |
| **Composite** | Tree of uniform parts | A portfolio containing sub-portfolios and positions — *perfect domain example, use it* |
| **Bridge** | Split abstraction from implementation | Report format × delivery channel |
| **Flyweight** | Share immutable state across many objects | Interning instrument/symbol reference data across millions of ticks — **great real-time example** |

### A3. Behavioural

| Pattern | One-liner | Real use |
|---|---|---|
| **Strategy** | Interchangeable algorithms | Pricing/fee/routing strategies chosen at runtime — *the* pattern for an OMS |
| **Observer** | Publish/subscribe to state change | `INotifyPropertyChanged`, .NET events, `IObservable`/Rx |
| **Command** | Encapsulate a request as an object | WPF `ICommand`; undo/redo; queued/deferred execution |
| **Chain of Responsibility** | Pass along a chain until handled | ASP.NET Core middleware; validation pipelines |
| **Mediator** | Objects talk via a hub | **MediatR** in your CQRS code |
| **State** | Behaviour changes with state | **Order lifecycle: New → PendingNew → PartiallyFilled → Filled/Cancelled** — use this example, it's exactly their domain |
| **Template Method** | Skeleton with overridable steps | Base import job with per-format parsing |
| **Visitor** | Operations over an object structure | Walking an expression tree / rule set |
| **Iterator** | Sequential access | `IEnumerable`/`yield return` |
| **Memento** | Capture/restore state | Undo in a UI; snapshotting |
| **Specification** | Composable business rules | `IsEligible.And(IsWithinLimit)` for order validation |

### A4. Enterprise & distributed patterns (your strong ground — lead with these)

- **Repository / Unit of Work** — ⚠️ be ready for the critique: *"EF Core's `DbSet` is already a
  repository and `DbContext` is already a unit of work, so I add one only when I want to hide
  persistence from the domain or make testing simpler — not by reflex."* That nuance reads as senior.
- **CQRS** — separate read and write models. Say clearly: *"CQRS is not event sourcing, and doesn't
  require two databases."*
- **Event Sourcing** — store the events, derive state. **Benefits:** perfect audit trail, temporal
  queries, replay. **Costs:** eventual consistency on projections, schema/event versioning, snapshots
  needed for long streams, and *it's hard to query without projections*. You did this at Calrom —
  **it's a superb capital-markets story** (regulators want to know *why* a number is what it is).
- **SAGA** (orchestration vs choreography) + compensating transactions.
- **Outbox** — atomically write state + the event in one DB transaction; a relay publishes. Solves
  the dual-write problem.
- **Idempotency** — the answer to at-least-once delivery. Idempotency keys, dedupe tables, natural
  idempotence (upserts).
- **Anti-Corruption Layer** — protect your domain model from a partner's/legacy model. You used this
  at Calrom against GDS. Perfect fit for broker/vendor integrations.
- **Strangler Fig** — incremental legacy replacement. **Say this if they mention modernising a WPF/
  .NET Framework estate.**
- **Circuit Breaker / Retry with jitter / Bulkhead / Timeout** — Polly. Explain *why jitter*: without
  it, retries synchronise into a thundering herd.
- **BFF / API Gateway**, **Cache-aside / write-through / write-behind**, **Bulk/Batch**, **DLQ +
  replay**, **Leader election**, **Sidecar**.

### A5. Questions they'll actually ask
- *"Explain a pattern you've used and one you've regretted."* — Have a real regret ready. Suggested:
  *"I over-applied the Repository pattern on a project — a generic repository over EF Core that
  leaked `IQueryable` anyway and just added indirection. I'd now put persistence behind
  intention-revealing methods on the aggregate root, or use `DbContext` directly in a vertical slice."*
- *"How do patterns relate to SOLID?"* — patterns are recurring applications of the principles;
  Strategy and Decorator are Open/Closed in practice.
- *"When is a pattern the wrong answer?"* — when it adds indirection without changing what can vary.
  Quote YAGNI. Interviewers love a candidate who resists over-engineering.

---

## PART B — ALGORITHMS & THE CODE EXERCISE

The invitation says *"code exercise could be done"*. For a senior enterprise role expect a **practical**
problem (parsing, aggregation, a small class design, a concurrency fix) more than a LeetCode-hard.
But be safe on fundamentals.

### B1. Complexity — state it for every solution you give

| Structure | Access | Search | Insert | Delete |
|---|---|---|---|---|
| Array | O(1) | O(n) | O(n) | O(n) |
| Sorted array | O(1) | O(log n) | O(n) | O(n) |
| Hash table | — | O(1) avg / O(n) worst | O(1) avg | O(1) avg |
| Balanced BST | — | O(log n) | O(log n) | O(log n) |
| Heap | O(1) min/max | O(n) | O(log n) | O(log n) |

Sorting: quicksort O(n log n) avg / O(n²) worst, in-place, not stable · mergesort O(n log n) always,
stable, O(n) space · heapsort O(n log n), in-place, not stable. .NET's `Array.Sort` uses introsort
(quick → heap on deep recursion → insertion for small); `OrderBy` in LINQ is **stable** mergesort.

**Say complexity out loud** — *"that's O(n log n) time, O(n) space"* — every single time.

### B2. Patterns that solve 80% of interview problems
1. **Hash map for O(1) lookup** — two-sum, dedupe, grouping, frequency.
2. **Two pointers / sliding window** — subarray sums, longest-substring, moving windows over ticks.
3. **Sort then scan** — merge intervals, closest pair, matching orders by price/time.
4. **Heap / priority queue** — top-K, k-way merge, and **an order book is literally two heaps**
   (max-heap of bids, min-heap of asks). `PriorityQueue<TElement,TPriority>` exists in .NET 6+.
5. **BFS/DFS + recursion** — trees, graphs, hierarchies (portfolio → sub-portfolio → position).
6. **Dynamic programming** — only if they push; know memoisation vs tabulation.
7. **Binary search** — on a sorted array *and* on an answer space.

### B3. Domain-flavoured problems to rehearse (most likely for this role)

1. **Order book**: maintain bids/asks, support add/cancel/match, return best bid/ask.
   → `SortedDictionary<decimal, LinkedList<Order>>` per side (price levels), plus a
   `Dictionary<orderId, node>` for O(1) cancel. Price-time priority: FIFO within a price level.
   **Be able to sketch this — it's the classic capital-markets question.**
2. **VWAP** over a trade stream: running Σ(price×qty)/Σqty; do it in one pass, O(1) memory.
3. **Moving average / rolling window** of the last N ticks: circular buffer + running sum (O(1) per
   tick, not O(N)).
4. **Merge two sorted trade files** by timestamp (k-way merge with a heap).
5. **Group trades by symbol and compute P&L** — LINQ `GroupBy` + `Aggregate`, then state complexity.
6. **Deduplicate messages by ID** with a bounded window (LRU / `HashSet` + queue).
7. **Rate limiter** — token bucket or sliding window (`04` §9.3).
8. **Parse a fixed-width / FIX-like message** with `ReadOnlySpan<char>`, zero allocation (`03` §1).
9. **LRU cache** — `Dictionary` + doubly-linked list, O(1) get/put. Classic.
10. **Find a race condition in given code and fix it** (`04` §9.4).

### B4. How to run a live coding exercise (the meta-skill that scores points)
1. **Restate the problem**, then ask 2 clarifying questions (input size? duplicates? sorted? threading?
   null/empty? error behaviour?).
2. **State a brute force + its complexity**, then the better approach. *"Naively that's O(n²); with a
   dictionary it's O(n) time, O(n) space."*
3. **Narrate as you type.** Silence is the biggest scoring loss.
4. Write **clean, named, testable code**: guard clauses, meaningful names, no magic numbers.
5. **Walk a small example through it by hand.**
6. Name the edge cases: empty, single element, duplicates, overflow, nulls, concurrency.
7. Say what you'd add in production: tests, logging, cancellation, input validation.
8. If stuck: *"Let me think about this differently"* and reason aloud. Never freeze silently.

---

## PART C — SYSTEM DESIGN

### C1. A framework to use every time (say the headings out loud)
1. **Requirements** — functional; then **non-functional: throughput, latency (p99), data volume,
   consistency, availability, retention, security/compliance**. *Ask before designing.*
2. **Constraints & scale estimate** — messages/sec, rows/day, GB/year. Even rough numbers show rigour.
3. **High-level components** — draw boxes and arrows; name the boundaries.
4. **Data model & storage choice per access pattern.**
5. **The critical path** — trace one request/message end to end.
6. **Failure modes** — what breaks, what happens then, how you recover.
7. **Cross-cutting** — security, observability, deployment, testing.
8. **Trade-offs and what you'd do differently at 10×.**

### C2. Distributed fundamentals (be crisp)

- **CAP**: under a network **partition** you choose consistency or availability. ⚠️ The senior version:
  *"CAP is about partitions only; the real everyday trade-off is PACELC — even without a partition
  you're trading latency against consistency."* Few candidates say this.
- **Consistency models**: strong, eventual, causal, **read-your-writes**, monotonic reads.
- **Idempotency, exactly-once**: *"exactly-once delivery doesn't exist; you get at-least-once delivery
  plus idempotent processing, which gives exactly-once **effects**."* Excellent line — use it.
- **Ordering**: per-key/partition ordering is achievable, global ordering is expensive. Kafka orders
  within a partition only.
- **Two-phase commit vs SAGA**: 2PC blocks and couples; SAGA trades atomicity for compensations.
- **Consensus**: Raft/Paxos, leader election, quorum, split-brain.
- **Backpressure & load shedding**: bounded queues, drop policy, `429`, circuit breakers.
- **Failure**: timeouts everywhere, retries **with jitter**, bulkheads, graceful degradation,
  health/readiness probes, blue-green and canary.
- **Clock**: never trust wall clocks across machines; logical clocks/sequence numbers.
  In finance: **timestamping and clock sync (NTP/PTP) is a regulatory matter** (MiFID II RTS 25) —
  a strong detail to drop.

### C3. SOA vs microservices vs modular monolith (they explicitly ask about SOA)

| | SOA (classic) | Microservices | Modular monolith |
|---|---|---|---|
| Granularity | Coarse business services | Fine, one bounded context | One deployable, strong internal modules |
| Integration | Often ESB, shared canonical schema, SOAP/WSDL | Smart endpoints, dumb pipes; REST/gRPC/events | In-process |
| Data | Often shared DB | **Database per service** | One DB, module-owned schemas |
| Best for | Enterprise integration across systems | Independent scale & deploy, many teams | Most teams, most of the time |

**Say this:** *"I'd default to a modular monolith with clean bounded contexts and split out services
where there's a real reason — independent scaling, independent release cadence, or team ownership.
Microservices buy you organisational scaling and cost you a distributed system. In a trading context
I'd be especially careful: every network hop is latency and a new failure mode."* That answer is
mature and fits an enterprise finance shop far better than "microservices everything".

---

### C4. 🎯 Walkthrough 1 — Real-time market data → trading blotter *(most likely question)*

> *"Design a system that consumes a market data feed and shows live prices and P&L to 200 traders on
> a WPF desktop, with position and order data behind it."*

**Requirements to establish (ask these!):** how many instruments? updates/sec? acceptable staleness
(is 250 ms fine, or is this latency-sensitive execution)? do all users see all instruments? intraday
only or history too? recovery on disconnect?

**Design:**
```
 Exchange/Vendor feed (Bloomberg/Refinitiv/FIX/multicast)
        │
   [Feed Handler]  ── normalises to a canonical Tick, single-writer per instrument partition
        │  (bounded channel, drop-oldest for prices)
   [Conflation / Distribution service]  ── keeps latest-per-instrument, publishes deltas
        │                                   ├── tick archive → columnar store (Parquet/ClickHouse/columnstore)
        │
   [Real-time transport]  SignalR / WebSocket (or a vendor bus: Solace/Kafka/29West)
        │   • per-user subscription: only instruments they're watching
        │   • server-side throttling: max N updates/sec/client
        │
   [WPF client]  ── conflates again locally, batches on a DispatcherTimer, virtualised grid
        │
   [Order/Position services (.NET)]  ── SQL Server system of record, EF Core writes
        └── P&L computed server-side (authoritative) and/or client-side (responsive)
```

**Decisions to justify:**
- **Push, not poll** — polling 200 clients × 5,000 instruments is hopeless. SignalR with WebSocket
  transport; fall back gracefully.
- **Subscription-based fan-out** — send a client only what it's displaying, or you saturate the
  network with data nobody sees.
- **Conflation on both server and client** — the server can't push 10k/sec to a UI; the human eye
  can't use it either.
- **Snapshot + delta protocol** — on connect, send a snapshot; then send only changes; sequence
  numbers so the client can detect a gap and re-request a snapshot. **This is the correct, expected
  answer for a market data system — say "snapshot then deltas with sequence numbers".**
- **Where is P&L computed?** Server-side is authoritative and consistent across users; client-side is
  instant. Common answer: server owns realised P&L and positions; client computes unrealised mark-to-
  market from the latest price it holds. **Flag it as a deliberate trade-off between consistency and
  responsiveness** — exactly the judgement they're testing.
- **Recovery**: heartbeat, detect stale feed, show a visual "stale" state (traders must *never* act on
  a stale price believing it's live — a UX decision with real money attached; saying this is gold).
- **Persistence split**: OLTP row store for orders/positions; columnar/append-only for tick history.
- **Observability**: latency histograms at each hop (p50/p99/p99.9), message gap counters, queue
  depth as the key backpressure signal.

### C5. 🎯 Walkthrough 2 — Order Management System (OMS)

**Core requirements:** capture orders, validate against limits/compliance, route to brokers, track
executions, maintain positions, full audit.

- **Domain model** (DDD): `Order` aggregate root with a **state machine** (see §A3 State) — never let
  external code mutate status directly; expose intention-revealing methods (`Amend`, `Cancel`,
  `ApplyFill`). Invariants enforced inside the aggregate.
- **Concurrency**: optimistic concurrency (`rowversion`) on the order aggregate; **partition by
  instrument or by account so each partition is single-writer** (`04` §8.4).
- **Correctness**: every state change is an **event**; event sourcing or an append-only audit table.
  Regulators and ops need "who changed what, when, and why".
- **Integration**: FIX gateway to brokers (see `11`), wrapped in an **anti-corruption layer**;
  idempotent handling of execution reports (they can be duplicated or out of order — dedupe on
  `ExecID`, sequence by `MsgSeqNum`).
- **Consistency across services**: SAGA + outbox for anything spanning order/position/compliance.
- **Reconciliation**: an end-of-day job comparing internal positions to the broker/custodian —
  **finance systems always reconcile; mentioning it shows domain instinct.**
- **Failure modes to talk about**: broker disconnect mid-order (you don't know if it was accepted →
  order status request / recovery on reconnect), duplicate fills, partial fills, cancel/replace races
  (a cancel and a fill crossing in flight — the classic OMS race condition).

### C6. 🎯 Walkthrough 3 — Modernising a legacy WPF/.NET Framework desktop estate
*(Very likely, given "expanding with multiple initiatives" + the C#/VB.NET tag. This is **your**
strongest design story — you've done it twice.)*

- **Assess**: what's the actual pain — deployment, performance, testability, hiring, or a vendor EOL?
  Don't rewrite for aesthetics.
- **Strangler Fig**, not big-bang: stand up new services alongside, route features across gradually.
- **Step 1: extract the domain from the UI.** Legacy desktop apps usually have business logic in
  code-behind. Pull it into a testable .NET library first — that's the highest-value, lowest-risk move
  and it's what makes everything after it possible.
- **Step 2: put a service tier behind it** (ASP.NET Core + REST/gRPC), so the desktop stops talking to
  the database directly. This also unblocks a future web client.
- **Step 3: migrate the shell** .NET Framework → .NET 8/10 (WPF is supported on modern .NET; use the
  .NET Upgrade Assistant, deal with `app.config`, WCF → CoreWCF or gRPC, `BinaryFormatter` removal).
- **Step 4: incrementally re-platform screens** to modern MVVM; consider WinUI/web only if there's a
  business reason.
- **De-risking**: characterisation tests around legacy behaviour before touching it, feature flags,
  parallel-run and diff outputs (**shadow mode** — run old and new, compare results, ship when they
  agree; in finance this is the standard technique and naming it is a strong signal), staged rollout
  by user group, and a rollback plan.
- **Measure**: define what "done" means — deployment time, crash rate, p99 screen load, defect rate.

---

## C7. Non-functional vocabulary to sprinkle (accurately)
SLI/SLO/SLA and error budgets · RPO/RTO · p50/p99/p99.9 latency · throughput vs latency · availability
maths (three nines = 8.7 h/yr, four nines = 52 min/yr) · horizontal vs vertical scaling · stateless
services · cache-aside · queue-based load levelling · graceful degradation · blue-green vs canary ·
feature flags · multi-tenancy and tenant isolation · chaos testing · capacity planning.
