# 08 — PATTERNS, ALGORITHMS & SYSTEM DESIGN, IN PLAIN ENGLISH

> Must-haves: **design patterns and algorithms**, **distributed design**, **service-oriented
> architecture**, **solution architecture background**.
>
> **The single most important rule in this file:**
> **Never define a pattern. Give the problem it solved on your project.**
> A definition sounds like revision. A story sounds like experience.

---

# EASY MEMORY NOTES

Read this first. Start with the short phrase. Say the simple line. Add the last column only if they
ask for more.

| Remember | Say it simply | If they ask more |
|---|---|---|
| **Problem first** | Start with the problem, not the pattern name. | Then say why that pattern helped. |
| **Singleton as lifetime** | I prefer DI singleton lifetime, not static singleton code. | It is easier to test and replace. |
| **Order has states** | An order should only move through valid states. | The order object should control its own status changes. |
| **Decorator wraps** | A decorator adds behavior around existing code. | Good for retry, logging, caching, and middleware. |
| **CQRS is split models** | CQRS separates reads from writes. | It does not automatically mean event sourcing. |
| **Outbox saves messages** | Save the data change and message record together. | Then a background worker publishes the message later. |
| **Exactly-once effect** | Messages can arrive more than once, so handle repeats safely. | Use idempotency keys or dedupe tables. |
| **CAP = choose in failure** | During network failure, choose consistency or availability. | PACELC adds that latency and consistency also trade off normally. |
| **Monolith first** | Start modular; split services only when needed. | Split for scale, release, or team ownership. |
| **Replace slowly** | Modernise legacy systems piece by piece. | Run old and new together and compare results before switching. |

---

# PART 0 — THE 10 ARCHITECTURE ANSWERS THAT WIN

| # | The question | Full answer in simple words |
|---|---|---|
| 1 | **Singleton** | "I prefer DI singleton lifetime instead of static singleton code. The container owns the one instance, dependencies stay visible, and tests can replace it." |
| 2 | **Order lifecycle** | "An order is a state machine. It moves through valid states like New, PartiallyFilled, Filled, Cancelled, or Rejected. The order object should own those transitions." |
| 3 | **Retry, caching, logging** | "Use a decorator or middleware to wrap behavior around the core code. The business code stays clean, and retry, logging, caching, or timing can be added outside it." |
| 4 | **CQRS** | "CQRS means separate models for reads and writes. It can be one database or many. It does not automatically mean event sourcing." |
| 5 | **Event sourcing** | "Event sourcing stores the facts that happened, then rebuilds current state from those facts. It gives strong audit and replay, but it adds work around projections, versions, and snapshots." |
| 6 | **Exactly-once delivery** | "Messages can be delivered more than once. The real goal is safe repeat handling: use idempotency keys, dedupe tables, or upserts so repeating the message has the same final effect." |
| 7 | **Dual writes** | "The outbox pattern avoids writing data and publishing a message separately. I save the data change and an outbox row in one database transaction, then a relay publishes the message later." |
| 8 | **CAP** | "When the network breaks between nodes, a distributed system must choose whether to stay consistent or stay available. In normal times, there is also a trade-off between low latency and stronger consistency." |
| 9 | **Microservices?** | "I start with a modular monolith by default. I split a service only when I need independent scaling, independent release, or clear team ownership. Every network call adds latency and failure risk." |
| 10 | **Legacy modernisation** | "Do not replace a legacy system in one big move. Replace it piece by piece, run old and new side by side, compare results, and switch traffic only when the new path is trusted." |

---

# PART A — DESIGN PATTERNS

## A1. Creational

| Pattern | In one line | The example to give |
|---|---|---|
| **Factory Method** | A subclass decides which concrete type to create | A factory picking the right FIX or EDI adapter per counterparty |
| **Abstract Factory** | Families of related objects | A whole set of providers per environment |
| **Builder** | Build a complex object step by step | An order request with twenty optional fields; fluent test-data builders |
| **Prototype** | Clone an existing instance | Copying a template order or a strategy config |
| **Singleton** | One instance | ⚠️ **Say:** *"I use DI singleton lifetime, not the static pattern — testable and explicit."* **Strong senior answer.** |

## A2. Structural

| Pattern | In one line | The example to give |
|---|---|---|
| **Adapter** | Make an incompatible interface fit | Wrapping a vendor market-data SDK behind `IPriceSource` |
| **Facade** | A simple front over a complex subsystem | One booking facade over five services |
| **Decorator** | Add behaviour without changing the type | **Caching, retry and logging decorators over a repository.** Also how MediatR pipeline behaviours work |
| **Proxy** | A stand-in that controls access | EF lazy loading; a gRPC client proxy |
| **Composite** | A tree where parts and wholes look the same | **A portfolio containing sub-portfolios and positions.** Perfect domain example — use it |
| **Flyweight** | Share immutable state across many objects | **Interning instrument reference data across millions of ticks.** Great real-time example |

## A3. Behavioural

| Pattern | In one line | The example to give |
|---|---|---|
| **Strategy** | Interchangeable algorithms | Pricing, fee and routing strategies chosen at runtime — *the* pattern for an OMS |
| **Observer** | Publish/subscribe on state change | `INotifyPropertyChanged`, .NET events, Rx |
| **Command** | A request wrapped as an object | WPF `ICommand`; undo/redo; deferred execution |
| **Chain of Responsibility** | Pass along until someone handles it | ASP.NET Core middleware; validation pipelines |
| **Mediator** | Objects talk through a hub | **MediatR** in your CQRS code |
| **State** | Behaviour changes with state | **The order lifecycle.** Use this example — it's exactly their domain |
| **Template Method** | A skeleton with overridable steps | A base import job with per-format parsing |
| **Specification** | Composable business rules | `IsEligible.And(IsWithinLimit)` for order validation |

## A4. Enterprise & distributed patterns — **lead with these, it's your strong ground**

**Repository / Unit of Work** — ⚠️ **be ready for the critique, and get there first:**
> *"EF Core's `DbSet` is already a repository and `DbContext` is already a unit of work. So I add one
> only when I want to hide persistence from the domain or genuinely simplify testing — not by
> reflex."*
That nuance reads as senior.

**CQRS** — *"Separate the read model from the write model. Two things people get wrong: **CQRS is not
event sourcing**, and it doesn't require two databases. It can be two sets of classes over one
database."*

**Event Sourcing** — *"Store the events; derive the state.*
- ***Benefits:*** *a perfect audit trail, temporal queries, and replay.*
- ***Costs:*** *eventual consistency on projections, event schema versioning, snapshots for long
  streams, and it's hard to query without building projections."*

⚠️ **You did this at Calrom. It's a superb capital-markets story** — regulators don't just want to know
what a number is, they want to know **why** it is what it is. Say that.

**SAGA** — *"A long-running transaction across services, with compensating actions instead of a
rollback. Orchestration means one coordinator drives it; choreography means services react to each
other's events."*

**Outbox** — *"Solves the dual-write problem. You can't atomically write to your database and publish
to a broker. So you write the state change **and** the outbox row in one transaction, and a relay
publishes from the outbox afterwards."*

**Idempotency** — *"The answer to at-least-once delivery. Idempotency keys, a dedupe table, or making
the operation naturally idempotent with an upsert."*

**Anti-Corruption Layer** — *"Protect your domain model from a partner's or a legacy model. I used
this against GDS at Calrom. It's the right fit for broker and vendor integrations."*

**Strangler Fig** — *"Incremental legacy replacement."* **Say this the moment they mention modernising
a WPF or .NET Framework estate.**

**Circuit Breaker / Retry with jitter / Bulkhead / Timeout** — Polly.
⚠️ **Explain why jitter:** *"Without it, all the retries synchronise and you get a thundering herd —
you've turned one outage into a self-inflicted denial of service."*

**Also worth naming:** API Gateway / BFF, cache-aside vs write-through, dead-letter queue with replay,
leader election.

## A5. The pattern questions they actually ask

**Q: "Tell me a pattern you've used and one you regret."**
**Have a real regret ready. Say:**
> *"I over-applied the Repository pattern once — a generic repository over EF Core that leaked
> `IQueryable` anyway, so it added indirection without adding abstraction. I'd now put persistence
> behind intention-revealing methods on the aggregate root, or just use `DbContext` directly in a
> vertical slice."*

**Q: "When is a pattern the wrong answer?"**
**Say:** *"When it adds indirection without changing what can actually vary. If nothing is going to
vary, a pattern is just extra code to read."* **Interviewers love a candidate who resists
over-engineering.**

---

# PART B — ALGORITHMS AND THE CODE EXERCISE

The invitation says *"code exercise could be done"*. For a senior enterprise role expect something
**practical** — parsing, aggregation, a small class design, fixing a concurrency bug — rather than a
hard LeetCode puzzle. But be safe on fundamentals.

## B1. Complexity — state it out loud, every time

| Structure | Access | Search | Insert | Delete |
|---|---|---|---|---|
| Array | O(1) | O(n) | O(n) | O(n) |
| Sorted array | O(1) | O(log n) | O(n) | O(n) |
| Hash table | — | O(1) average | O(1) average | O(1) average |
| Balanced tree | — | O(log n) | O(log n) | O(log n) |
| Heap | O(1) for min/max | O(n) | O(log n) | O(log n) |

**Sorting:** quicksort is O(n log n) average, O(n²) worst, in place, **not stable**. Mergesort is
O(n log n) always, **stable**, needs O(n) space. .NET's `Array.Sort` is introsort; **LINQ's `OrderBy`
is a stable mergesort.**

**Say the complexity out loud every single time** — *"that's O(n log n) time and O(n) space."*
It costs you two seconds and it's what a senior sounds like.

## B2. The seven patterns that solve 80% of interview problems

1. **Hash map for O(1) lookup** — two-sum, dedupe, grouping, frequency counts.
2. **Two pointers / sliding window** — subarray sums, longest substring, rolling windows over ticks.
3. **Sort then scan** — merge intervals, closest pair, matching orders by price and time.
4. **Heap / priority queue** — top-K, k-way merge. ⚠️ **An order book is literally two heaps** — a
   max-heap of bids and a min-heap of asks. `PriorityQueue<T,TPriority>` exists in .NET 6+.
5. **BFS / DFS** — trees, graphs, hierarchies (portfolio → sub-portfolio → position).
6. **Binary search** — on a sorted array, *and* on an answer space.
7. **Dynamic programming** — only if they push. Know memoisation vs tabulation.

## B3. Domain-flavoured problems to rehearse (most likely for this role)

1. **Order book** — add, cancel and match; return the best bid and ask.
   → A `SortedDictionary<decimal, LinkedList<Order>>` per side for the price levels, plus a
   `Dictionary<orderId, node>` so cancels are O(1). **Price-time priority: FIFO within a price
   level.** **Be able to sketch this — it's the classic capital-markets question.**
2. **VWAP over a trade stream** — running Σ(price×qty) ÷ Σqty. One pass, O(1) memory.
3. **Rolling window over the last N ticks** — circular buffer plus running sums. O(1) per tick, not
   O(N). *(The Python version is in `06` §15.1.)*
4. **Merge two sorted trade files** by timestamp — k-way merge with a heap.
5. **Group trades and compute P&L** — then state the complexity.
6. **Deduplicate messages by ID** with a bounded window — LRU, or a `HashSet` plus a queue.
7. **Rate limiter** — token bucket or sliding window (`04` §9.3).
8. **LRU cache** — a `Dictionary` plus a doubly-linked list. O(1) get and put. A classic.
9. **Find and fix a race condition** in code they show you (`04` §9.4).

## B4. 🎯 How to run a live coding exercise — the meta-skill that scores points

**This matters as much as the code.**

1. **Restate the problem**, then ask two clarifying questions. *Input size? Duplicates? Already
   sorted? Threading? What should empty input do?*
2. **State a brute force and its complexity first**, then the better approach.
   *"Naively that's O(n²). With a dictionary it's O(n) time and O(n) space."*
3. **Narrate as you type.** ⚠️ **Silence is the single biggest scoring loss in a live exercise.**
4. Write **clean, named, testable** code — guard clauses, real names, no magic numbers.
5. **Walk a small example through it by hand.**
6. **Name the edge cases:** empty, one element, duplicates, overflow, nulls, concurrency.
7. Say what you'd add in production: tests, logging, cancellation, input validation.
8. **If you get stuck:** *"Let me think about this differently"* — and reason out loud.
   **Never freeze silently.**

---

# PART C — SYSTEM DESIGN

## C1. The framework — say the headings out loud as you go

1. **Requirements.** Functional, then **non-functional: throughput, p99 latency, data volume,
   consistency, availability, retention, compliance.** ⚠️ **Ask before you design.**
2. **Scale estimate.** Messages per second, rows per day, GB per year. Even rough numbers show rigour.
3. **High-level components.** Boxes and arrows. Name the boundaries.
4. **Data model and storage choice — per access pattern.**
5. **Trace one request end to end.** The critical path.
6. **Failure modes.** What breaks, what happens, how you recover.
7. **Cross-cutting.** Security, observability, deployment, testing.
8. **Trade-offs, and what you'd change at 10× the scale.**

## C2. Distributed fundamentals

- **CAP** — *"Under a network **partition**, you choose consistency or availability."*
  ⚠️ **The senior version:** *"CAP is only about partitions. The real everyday trade-off is
  **PACELC** — even with no partition, you're trading latency against consistency."*
  **Few candidates say this.**
- **Exactly-once** — *"Exactly-once **delivery** doesn't exist. Messages can repeat, so the handler
  must be safe to run twice. That gives exactly-once **effects**."* **Excellent line. Use it.**
- **Ordering** — per-key or per-partition ordering is achievable; global ordering is expensive.
  Kafka orders within a partition only.
- **2PC vs SAGA** — two-phase commit blocks and couples everything; SAGA trades atomicity for
  compensating actions.
- **Backpressure and load shedding** — bounded queues with an explicit drop policy, `429`, circuit
  breakers.
- **Failure handling** — timeouts everywhere, retries **with jitter**, bulkheads, graceful
  degradation, health and readiness probes, blue-green and canary.
- **Clocks** — *"Never trust wall clocks across machines. And in finance, **timestamping and clock
  synchronisation is a regulatory matter** — MiFID II RTS 25."* **A strong detail to drop.**

## C3. SOA vs microservices vs modular monolith (they explicitly ask about SOA)

| | SOA (classic) | Microservices | Modular monolith |
|---|---|---|---|
| Granularity | Coarse business services | Fine — one bounded context | One deployable, strong modules |
| Integration | Often an ESB, canonical schema, SOAP | Smart endpoints, dumb pipes; REST/gRPC/events | In-process |
| Data | Often a shared database | **Database per service** | One database, module-owned schemas |
| Best for | Integration across enterprise systems | Independent scale and deploy, many teams | **Most teams, most of the time** |

**Say this — it's mature and it fits an enterprise finance shop far better than "microservices
everything":**
> *"I'd default to a **modular monolith with clean bounded contexts**, and split out a service where
> there's a real reason: independent scaling, independent release cadence, or team ownership.
> Microservices buy you organisational scaling and cost you a distributed system. In a trading context
> I'd be especially careful — **every network hop is latency and a new failure mode.**"*

---

## C4. 🎯 WALKTHROUGH 1 — Market data feed → trading blotter *(most likely question)*

> *"Design a system that consumes a market data feed and shows live prices and P&L to 200 traders on a
> WPF desktop, with position and order data behind it."*

**First, ask these:** *How many instruments? Updates per second? Is 250 ms staleness acceptable, or is
this latency-sensitive execution? Does everyone see everything? Intraday only, or history too? What
happens on disconnect?*

```
 Exchange / vendor feed  (Bloomberg, Refinitiv, FIX, multicast)
        │
   [Feed Handler]  — normalise to a canonical Tick; single-writer per instrument partition
        │           bounded channel, drop-oldest for prices
   [Conflation / Distribution]  — keep latest-per-instrument, publish deltas
        │                        └── tick archive → columnar store (Parquet / ClickHouse)
   [Real-time transport]  SignalR / WebSocket
        │   • per-user subscription — only the instruments they're watching
        │   • server-side throttle — max N updates/sec/client
   [WPF client]  — conflate AGAIN locally, batch on a DispatcherTimer, virtualised grid
        │
   [Order / Position services]  — SQL Server system of record
        └── P&L: server-side authoritative, client-side responsive
```

**The decisions to justify — this is what they're marking:**

- **Push, not poll.** *"Polling 200 clients across 5,000 instruments is hopeless. SignalR over
  WebSocket."*
- **Subscription-based fan-out.** *"Send each client only what it's displaying, or you saturate the
  network with data nobody is looking at."*
- **Conflate on both server and client.** *"The server can't push 10,000 a second to a UI, and a human
  couldn't use it anyway."*
- ⚠️ **Snapshot then deltas, with sequence numbers.**
  **Say:** *"On connect, send a full snapshot. After that, send only changes, each with a sequence
  number, so the client can detect a gap and re-request a snapshot."*
  **This is the correct, expected answer for a market data system. Say those words.**
- **Where is P&L computed?** *"Server-side is authoritative and consistent across users. Client-side is
  instant. The usual split is: the server owns realised P&L and positions, the client computes
  unrealised mark-to-market from the price it already holds. **That's a deliberate trade-off between
  consistency and responsiveness** — and I'd flag it as one."* ← exactly the judgement they're testing.
- ⚠️ **Staleness is a safety feature.** *"Heartbeat the feed, detect staleness, and show a clear visual
  'stale' state. A trader must never act on a stale price believing it's live."*
  **That's a UX decision with real money attached — saying it is gold.**
- **Observability.** *"Latency histograms at every hop — p50, p99, p99.9 — message gap counters, and
  **queue depth as the key backpressure signal**."*

---

## C5. 🎯 WALKTHROUGH 2 — Order Management System

**Requirements:** capture orders, validate against limits and compliance, route to brokers, track
executions, maintain positions, full audit.

- **Domain model.** *"An `Order` aggregate root with a **state machine**. Nothing external mutates the
  status — the aggregate exposes intention-revealing methods: `Amend`, `Cancel`, `ApplyFill`.
  Invariants are enforced inside."*
- **Concurrency.** *"Optimistic concurrency with a `rowversion` on the order aggregate, and partition
  by instrument or account so **each partition is single-writer**."*
- **Correctness and audit.** *"Every state change is an event — event sourcing, or at minimum an
  append-only audit table. Regulators and ops need who changed what, when, and why."*
- **Integration.** *"A FIX gateway to the brokers, behind an anti-corruption layer. Execution reports
  can be **duplicated or arrive out of order**, so I dedupe on `ExecID` and sequence on `MsgSeqNum`."*
- **Reconciliation.** ⚠️ *"An end-of-day job comparing our positions to the broker's and the
  custodian's."* **Finance systems always reconcile. Mentioning it unprompted shows domain instinct.**
- **The failure modes to raise yourself:**
  - Broker disconnects mid-order — *"you don't know whether it was accepted. You send an order status
    request on reconnect."*
  - Duplicate fills, and partial fills.
  - **Cancel/replace races** — *"a cancel and a fill crossing in flight. That's the classic OMS race
    condition."*

---

## C6. 🎯 WALKTHROUGH 3 — Modernising a legacy WPF/.NET Framework estate

**This is *your* strongest design story — you've done it twice, and it's very likely to come up.**

1. **Assess first.** *"What's the actual pain — deployment, performance, testability, hiring, or a
   vendor going end-of-life? I wouldn't rewrite for aesthetics."*
2. **Strangler Fig, never big bang.** Stand up the new alongside the old and move features across.
3. **Step 1: extract the domain from the UI.** *"Legacy desktop apps usually have business logic sitting
   in code-behind. Pulling it into a testable library is the highest-value, lowest-risk first move —
   and it's what makes everything after it possible."*
4. **Step 2: put a service tier behind it** so the desktop stops talking to the database directly.
   That also unblocks a future web client.
5. **Step 3: migrate the shell** from .NET Framework to .NET 8/10. *"WPF is supported on modern .NET.
   The .NET Upgrade Assistant, `app.config` changes, WCF to CoreWCF or gRPC, and `BinaryFormatter`
   removal are the usual work."*
6. **Step 4: re-platform screens incrementally.**

**De-risking — and this is the part that sounds senior:**
- Characterisation tests around the legacy behaviour **before** touching it.
- Feature flags, staged rollout by user group, and a rollback plan.
- ⚠️ **Shadow mode.** *"Run old and new in parallel, compare the outputs, and only ship when they
  agree. In finance that's the standard technique for anything that produces a number."*
  **Naming shadow mode is a strong signal.**
- **Define what 'done' means** — deployment time, crash rate, p99 screen load, defect rate.

---

# PART D — VOCABULARY TO SPRINKLE (accurately, not as decoration)

SLI / SLO / SLA and error budgets · RPO and RTO · p50/p99/p99.9 · throughput vs latency ·
availability maths (**three nines is 8.7 hours a year, four nines is 52 minutes**) · horizontal vs
vertical scaling · stateless services · cache-aside · queue-based load levelling · graceful
degradation · blue-green vs canary · feature flags · chaos testing · capacity planning.
