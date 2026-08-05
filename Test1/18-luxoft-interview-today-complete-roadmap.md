# Luxoft Interview Today - Complete Quick Review Roadmap

Use this as the one file to read before the interview. It is built for quick recall, not long study.

Role: Senior Full Stack Developer, Luxoft, Abu Dhabi
Core stack: .NET/C#, WPF, Python, JavaScript/TypeScript/React, SQL, MongoDB, real-time/multithreading, distributed systems, REST/auth, Azure, DevOps, Windows development
Domain: Banking and Capital Markets, likely portfolio/order/execution management
Interview goal: prove senior engineering depth, honesty on gaps, and readiness for a finance client

---

# 0. First 10 Minutes - All Perspectives Dashboard

Read this section first. It is the full interview map from every important angle.

## 0.1 What They Are Really Hiring For

They are not just hiring a generic full stack developer.

They likely need a senior engineer for a capital markets platform with:

- a WPF desktop client
- .NET backend services
- Python analytics or data processing
- SQL plus Mongo/unstructured data
- real-time market/order/position data
- multithreaded and distributed design
- secure REST APIs
- Azure or hybrid deployment
- DevOps/CI-CD
- finance domain awareness: PMS, OMS, EMS, orders, executions, positions, P&L

Your positioning:

> "I am a senior .NET-heavy full stack engineer who modernises business-critical systems, builds distributed and event-driven services, works hands-on with Python and SQL, and can ramp into finance with honesty and speed."

Do not lead with AI. Mention AI as a bonus only after .NET, data, real-time systems, and architecture.

## 0.2 The Interviewer Lens

Luxoft is a consultancy. The first technical interviewer is checking:

- Can you really code?
- Are you strong enough technically for the client?
- Will you be honest about gaps?
- Can you explain trade-offs clearly?
- Can you work on old and modern systems together?
- Can you talk to a capital markets client without sounding generic?

The safest strategy:

- Be strong on .NET, concurrency, architecture, SQL.
- Be honest on WPF/finance gaps, but show you prepared.
- Use business-critical examples from your background.
- Quantify: latency, volume, reliability, performance, audit.

## 0.3 The Client Lens

For banking and capital markets, every answer should connect to four values:

1. Correct numbers
2. Responsive under load
3. Auditable history
4. Do not break the users' screens

Example:

> "For money, I use decimal types, not float, because correctness matters more than tiny speed gains."

Example:

> "For a high-frequency WPF grid, I would not update the UI per tick. I would conflate updates, batch them, and flush on a timer so the desktop stays responsive."

## 0.4 Your Risk Areas

Risk 1: WPF

Say:

> "I have not been in WPF as my main day-to-day UI recently. My recent UI work has been web, but the concepts transfer: MVVM, binding, change notification, state, commands, and threading. I have been refreshing WPF hands-on, especially Dispatcher, ObservableCollection, virtualisation, and batching real-time updates. I would be honest that my deepest strength is backend and distributed systems, but WPF is not an area I would bluff on or avoid."

Risk 2: Capital markets

Say:

> "I do not claim to be a capital markets domain expert. What I understand is the engineering shape: orders, partial fills, positions, P&L, audit, idempotency, and real-time updates. I have learned hard domains before, including airline/logistics systems, where correctness, integration, and audit mattered. I would expect to learn the business rules from domain experts and implement them precisely."

Risk 3: Low-level threading

Say:

> "My default is to avoid shared mutable state. For real-time systems I prefer partitioning by key, bounded channels, backpressure, idempotent processing, and single-writer ownership where possible. Locks are useful, but the best design is often the one with fewer shared writes."

## 0.5 One-Minute Pitch

Say this naturally:

> "I am a senior full stack engineer with around nine years of experience, strongest in .NET, backend architecture, distributed systems, SQL, Python, and Azure. My main pattern has been modernising business-critical systems without breaking production: moving legacy .NET and WCF-style platforms toward ASP.NET Core, event-driven services, clean APIs, CI/CD, and better observability.
>
> I have worked on systems where correctness and integration matter: reservations, logistics, billing, subscriptions, and real-time data pipelines. I am also hands-on with Python for APIs and data work, and I can work across the front end, though my deepest craft is backend and architecture.
>
> For this Luxoft role, the interesting part is the combination of .NET, WPF, real-time data, Python, SQL, and finance. I know I need to be honest about WPF and capital markets depth, but I have prepared the key concepts and I can ramp fast because I have learned complex domains before."

## 0.6 Project Walkthrough Formula

Use C.A.R.D.S:

- Context: What system and business problem?
- Architecture: Main components and data flow.
- Responsibility: What did you personally own?
- Decisions: Key trade-offs.
- Scale: Numbers, latency, volume, reliability.

Template:

> "The system was [business-critical platform]. The problem was [legacy, scale, reliability, latency, audit]. Architecturally we had [APIs/services/events/database/frontend]. I owned [specific areas]. The key decision was [trade-off], because [reason]. We measured success by [numbers]. The result was [impact]."

## 0.7 Top 20 Must-Remember Lines

1. Money: use decimal, never float.
2. WPF real-time grid: conflate, batch, flush on timer, virtualise.
3. Async: waiting means async; CPU work means threads/processes.
4. UI deadlock: never block UI thread with `.Result` or `.Wait()`.
5. Volatile is visibility, not atomicity; use `Interlocked`.
6. Locks: private lock object, consistent ordering, no `await` inside `lock`.
7. Producer/consumer: bounded `Channel<T>` gives backpressure.
8. Prices may drop stale updates; orders must never be dropped.
9. Exactly-once is not real; make processing idempotent.
10. SQL slow query: actual plan, logical reads, indexes, N+1, measure again.
11. LEFT JOIN trap: right-table predicate in WHERE turns it into inner join.
12. Latest row per group: use `ROW_NUMBER()`.
13. OAuth desktop: Authorization Code with PKCE; desktop apps cannot keep secrets.
14. JWT: validate signature, issuer, audience, expiry, algorithm.
15. Python GIL: one thread runs bytecode; I/O uses async/threads, CPU uses processes/NumPy.
16. React: UI is a function of state; do not mutate state directly.
17. Architecture default: modular monolith first; microservices only for real reasons.
18. Outbox solves dual-write between DB and message broker.
19. Order lifecycle: create, check, route, fill, allocate, settle, reconcile.
20. Audit: be able to explain why a number was true at a specific time.

---

# 1. Job Description Mapped To Interview Questions

## .NET C# Advanced

They may ask:

- CLR, GC, memory, value/reference types
- async/await
- LINQ and EF
- DI lifetimes
- exceptions
- `decimal` vs `double`
- performance and allocations

Your answer theme:

> ".NET is my strongest area. I think in correctness, allocation, async safety, and maintainable architecture."

## WPF Advanced

They may ask:

- MVVM
- XAML binding
- DependencyProperty
- `INotifyPropertyChanged`
- `ObservableCollection`
- Dispatcher/UI thread
- virtualisation
- real-time grid update
- memory leaks

Your answer theme:

> "I know the WPF model: MVVM, binding, commands, Dispatcher, and virtualisation. For real-time UI the main rule is never update the UI per message."

## Python Advanced

They may ask:

- GIL
- asyncio
- threads vs processes
- FastAPI
- Pandas/NumPy
- performance
- typing

Your answer theme:

> "Python is strong for APIs, orchestration, analytics, and data processing. I avoid blocking async loops and use vectorised libraries for numeric/data work."

## JavaScript/TypeScript/React Medium

They may ask:

- event loop
- promises
- TypeScript runtime limitations
- React state/effects

Your answer theme:

> "I can work across front end, but I am backend-heavy. I understand component architecture, state, async calls, and TypeScript boundaries."

## SQL

They may ask:

- joins
- indexes
- execution plans
- isolation
- transactions
- window functions
- slow query tuning

Your answer theme:

> "I approach SQL by reading the actual plan, checking logical reads, using good indexes, avoiding N+1, and validating with measurement."

## MongoDB / Unstructured Data

They may ask:

- document modelling
- embedding vs referencing
- indexes
- aggregation
- consistency

Your answer theme:

> "Mongo is good when the aggregate is naturally document-shaped. I avoid unbounded arrays and design indexes around query patterns."

## Real-Time And Multithreaded Systems

They may ask:

- race conditions
- locks
- deadlocks
- channels
- producer/consumer
- backpressure
- latency
- thread pool starvation

Your answer theme:

> "Real-time systems need bounded queues, backpressure, idempotency, and percentiles. I avoid global locks by partitioning state."

## Distributed Design

They may ask:

- microservices
- CAP/PACELC
- eventual consistency
- outbox
- saga
- retries
- idempotency

Your answer theme:

> "Distributed systems fail in partial ways. I design for retries, duplicates, ordering issues, observability, and recovery."

## REST APIs With Auth

They may ask:

- REST design
- status codes
- idempotency
- OAuth2/OIDC/JWT
- Kerberos/mTLS
- desktop auth

Your answer theme:

> "I separate identity from access, validate tokens properly, and enforce object-level authorization on every request."

## Azure / DevOps / CI-CD

They may ask:

- App Service, AKS, Functions
- Service Bus vs Event Hubs vs Event Grid
- Key Vault
- managed identity
- CI/CD pipeline
- database migration
- desktop rollout

Your answer theme:

> "First ask on-prem, Azure, or hybrid. In finance, data residency, release windows, and rollback matter."

## Finance Domain

They may ask:

- buy-side vs sell-side
- PMS/OMS/EMS
- order lifecycle
- FIX
- positions
- P&L
- audit

Your answer theme:

> "I am not claiming quant expertise. I understand the engineering shape and can implement domain rules precisely with audit and tests."

---

# 2. C# And .NET - Quick Review

## 2.1 Memory Hooks

- Value type holds data; reference type holds a reference.
- A struct is not always on stack. A struct field inside a class lives inline on the heap.
- Boxing creates heap allocation and copy.
- Use `decimal` for money, not `double`.
- `IEnumerable` is in-memory/deferred; `IQueryable` is expression tree translated by provider.
- `ToList()` too early can pull too much data.
- `throw;` preserves stack; `throw ex;` resets stack.
- Override `Equals` means override `GetHashCode`.
- Never hash mutable fields.
- `IDisposable` is deterministic cleanup; finalizer is GC-driven cleanup.
- `IHttpClientFactory` avoids socket exhaustion and stale DNS.
- DI lifetimes: Singleton, Scoped, Transient.
- Captive dependency: scoped injected into singleton.

## 2.2 GC Interview Answer

Say:

> ".NET GC is generational: gen 0 for short-lived objects, gen 1 as a buffer, gen 2 for long-lived objects. Large objects go to LOH around 85 KB. In low-latency systems I first reduce allocation instead of tuning GC. Fewer temporary objects means fewer collections and fewer pauses."

If pushed:

- LOH fragmentation can cause memory problems.
- Server GC improves throughput with heaps per core.
- Workstation GC can favor responsiveness.
- Avoid allocations in hot paths using pooling, `Span<T>`, structs carefully, and avoiding LINQ/closures in tight loops.

## 2.3 Async/Await Answer

Say:

> "`await` does not block a thread. The method is compiled into a state machine. When the awaited operation completes, the continuation runs. For I/O-bound work I use async; for CPU-bound work I use threads, parallelism, or separate processes."

Classic deadlock:

> "Blocking on `.Result` or `.Wait()` on a UI thread can deadlock because the continuation tries to resume on that same UI context, but the UI thread is blocked waiting."

Rules:

- Async all the way.
- `async void` only for event handlers.
- In libraries, use `ConfigureAwait(false)` when UI context is not needed.
- Do not use async for CPU work by itself.

## 2.4 EF / Data Access

Say:

> "For EF performance I start with projection, `AsNoTracking` for read-only queries, avoid N+1 queries, check generated SQL, and use indexes. I use Dapper when I need hand-tuned hot read paths."

Key points:

- `Include` can fix N+1 but may over-fetch.
- Projection with `Select` is often better.
- `AsSplitQuery` can avoid cartesian explosion.
- `rowversion` handles optimistic concurrency.
- Unit of Work fits writes; CQRS can separate read models.

## 2.5 C# Rapid Q&A

Q: `decimal` vs `double`?
A: `decimal` for money because base-10 precision. `double` for scientific/measurement calculations.

Q: `const` vs `readonly`?
A: `const` is compile-time and baked into callers. `readonly` is runtime and set in constructor.

Q: `record`?
A: Value equality, generated `ToString`, `with`, and init-style immutable modelling.

Q: Boxing?
A: Converting a value type to object/interface; creates allocation and copy.

Q: `Span<T>`?
A: Stack-only view over contiguous memory; useful for zero-allocation parsing; cannot be stored on heap or used across await.

Q: `ValueTask`?
A: Avoids allocation when result is often synchronous; use carefully and do not await twice.

Q: Why not throw exceptions for control flow?
A: Exceptions are expensive and hide expected branches.

Q: When use Dapper over EF?
A: Hot read paths or exact SQL control; EF for richer unit-of-work and domain writes.

---

# 3. WPF And Windows Desktop - Quick Review

## 3.1 WPF Mental Model

WPF is:

- retained-mode UI
- XAML object construction
- data binding heavy
- MVVM-friendly
- single UI thread with Dispatcher
- vector/GPU-composed
- Windows-only

Say:

> "WPF is a retained-mode desktop UI framework. The main design pattern is MVVM: the view is XAML, the view model exposes state and commands, and binding keeps them connected. UI objects have thread affinity, so background updates must marshal to the Dispatcher."

## 3.2 MVVM

View:

- XAML
- visual layout
- minimal code-behind

ViewModel:

- properties
- `INotifyPropertyChanged`
- `ICommand`
- validation
- no direct `Button`, `Grid`, `TextBox`

Model:

- domain data and rules

Say:

> "MVVM makes the UI testable because the view model is plain code. The view binds to properties and commands. I avoid putting business logic in code-behind."

## 3.3 Binding And Change Notification

Key points:

- `INotifyPropertyChanged` tells binding that a property changed.
- Use `[CallerMemberName]` to avoid string property names.
- Use equality guard before raising change notifications.
- `ObservableCollection<T>` notifies add/remove/reset.
- It does not notify when an item property changes unless the item itself implements `INotifyPropertyChanged`.

Say:

> "For real-time data I always add an equality guard before raising `PropertyChanged`; otherwise the UI re-renders even when the displayed value did not change."

## 3.4 DependencyProperty

Use DependencyProperty for controls because it supports:

- binding
- styling
- animation
- inheritance
- default values
- value precedence

Precedence memory:

> animation beats local value, local value beats style/triggers, then inherited/default.

Trap:

> "If a style trigger stops working, often a local value was set in code or XAML and local value has higher precedence."

## 3.5 Dispatcher And UI Thread

Say:

> "WPF UI elements can only be touched by the thread that created them. For background data I compute off the UI thread, then marshal only the minimal UI update using `Dispatcher.InvokeAsync`."

Do:

- keep background work off UI thread
- update UI in batches
- use `DispatcherPriority.Background` for non-urgent updates
- keep input responsive

Do not:

- call `.Result` on UI thread
- update UI per tick
- perform heavy layout on every message

## 3.6 High-Frequency WPF Grid Answer

This is one of the most likely questions.

Q: How do you update a WPF grid with 10k price ticks/sec?

Say:

> "I would not update the UI per tick. I would receive ticks on a background pipeline, keep only the latest value per instrument, and batch updates. A timer, maybe every 50 to 100 ms, flushes the latest snapshot to the UI thread through the Dispatcher. I would use equality guards so unchanged cells do not notify, enable row and column virtualisation, avoid a StackPanel items host, and use a bounded channel so the system has backpressure. For market data, stale prices can be conflated; for orders and executions, messages must not be dropped."

Memory:

> conflate -> batch -> Dispatcher -> equality guard -> virtualise -> bounded channel

## 3.7 WPF Performance

Know these:

- Enable virtualisation and recycling.
- Never place a virtualised grid inside unconstrained `StackPanel` or nested `ScrollViewer`.
- Binding errors are silent and expensive; check Output window.
- Freeze brushes/geometries when possible.
- Keep visual tree shallow.
- Avoid too many converters in hot paths.
- Use `ICollectionView` for sort/filter/group.
- Profile with Visual Studio UI responsiveness tools.

## 3.8 WPF Leaks

Common leaks:

- event handlers not unsubscribed
- static events
- `DispatcherTimer`
- long-lived collections holding view models
- commands/events capturing view models

Fix:

- unsubscribe
- use weak events
- dispose timers/subscriptions
- avoid static references

## 3.9 WPF Rapid Q&A

Q: `ObservableCollection` limitation?
A: It notifies collection changes, not item property changes.

Q: `DataTemplate` vs `ControlTemplate`?
A: DataTemplate defines how data looks. ControlTemplate defines how a control is built.

Q: `StaticResource` vs `DynamicResource`?
A: Static resolved once at load; dynamic can update when resource changes.

Q: Routed events?
A: Bubbling, tunnelling/Preview, and direct events.

Q: Dialog from ViewModel?
A: Use an injected dialog service, not direct UI control access.

Q: Why MVVM?
A: Testability, separation, binding, maintainability.

---

# 4. Multithreading, Async, Real-Time - Quick Review

## 4.1 The First Sentence

Say:

> "Waiting means async. Working means threads."

Meaning:

- Waiting for I/O: `async/await`
- CPU work: thread pool, parallelism, processes, native/vectorised libraries
- UI: keep Dispatcher free
- Real-time: bounded queues and backpressure

## 4.2 Locks

Rules:

- Lock on private readonly object.
- Do not lock on `this`, string, or `typeof`.
- Keep critical section short.
- Take locks in consistent order.
- Do not `await` inside `lock`.
- Use `SemaphoreSlim.WaitAsync` for async-compatible waiting.

Say:

> "A lock protects an invariant, not just a line of code. I keep the locked region small and avoid calling external code while holding it."

## 4.3 Volatile vs Interlocked

Say:

> "`volatile` is about visibility and ordering. It does not make compound operations like `x++` atomic. For counters I use `Interlocked.Increment`. For more complex shared state I use locks, concurrent collections, or better, partitioned ownership."

## 4.4 Deadlocks

Coffman conditions:

- mutual exclusion
- hold and wait
- no preemption
- circular wait

Prevention:

- consistent lock ordering
- timeout/cancellation
- avoid nested locks
- avoid blocking async

## 4.5 Producer/Consumer

Say:

> "In modern .NET I would use `System.Threading.Channels`. A bounded channel gives backpressure, and the full policy depends on the message. Market prices can drop stale values; order and execution messages must be persisted or backpressured, never silently dropped."

## 4.6 Real-Time Design

Use these concepts:

- bounded queues
- backpressure
- conflation for latest-value data
- idempotency for repeated messages
- partition by key
- single-writer principle
- p99/p99.9 latency, not average
- separate command data from telemetry/market data

Say:

> "For real-time state, my preferred design is partition by instrument or account so one worker owns that slice of state. That reduces locks and makes reasoning easier."

## 4.7 Thread Pool Starvation

Symptoms:

- request latency rises
- queue length grows
- CPU may not be high
- many blocked threads

Causes:

- `.Result` / `.Wait()`
- sync-over-async
- blocking I/O on thread pool
- long CPU work in request threads

Fix:

- async all the way
- move CPU work to background workers
- bounded queues
- avoid blocking calls

## 4.8 Concurrency Rapid Q&A

Q: Race condition?
A: Result depends on timing/interleaving of threads.

Q: Make `x++` thread-safe?
A: `Interlocked.Increment`.

Q: Can `ConcurrentDictionary.GetOrAdd` factory run twice?
A: Yes. The factory may run more than once, so keep it side-effect free.

Q: What is false sharing?
A: Separate hot variables share a CPU cache line and cause invalidation contention.

Q: Async means parallel?
A: No. Async is non-blocking waiting. Parallel means work at the same time.

Q: `Task.WhenAll`?
A: Starts/awaits multiple tasks concurrently and fails if any task fails.

---

# 5. SQL Databases - Quick Review

## 5.1 SQL Must-Knows

- `INNER JOIN`: matching rows only
- `LEFT JOIN`: all left rows plus matching right rows
- Right-table filter in `WHERE` after `LEFT JOIN` can turn it into inner join
- `NOT IN` with NULL is dangerous; use `NOT EXISTS`
- Window functions solve ranking, previous row, running totals
- Indexes speed reads but slow writes and take storage
- SARGable predicates allow index usage
- Transactions require correct isolation
- Use `DECIMAL` for money

## 5.2 Slow Query Answer

Say:

> "I do not guess. I capture the actual execution plan, check logical reads and row estimates, look for scans, key lookups, bad joins, missing indexes, parameter sniffing, stale statistics, and N+1 patterns. Then I fix one clear issue and measure again."

Checklist:

- actual plan
- logical reads
- missing/wrong index
- covering index
- key lookup
- bad estimates
- stale stats
- parameter sniffing
- non-SARGable predicate
- implicit conversion
- N+1
- over-fetching

## 5.3 Indexes

Clustered:

- data stored in that order
- usually primary key
- one per table

Non-clustered:

- separate structure pointing to rows
- can include extra columns

Composite:

- leftmost prefix matters

Covering:

- index contains all needed columns, avoiding lookup

Say:

> "An index should match the query shape: equality columns, then sort/join columns, then range columns, with includes for covering when appropriate."

## 5.4 Isolation

Levels:

- Read Uncommitted: dirty reads
- Read Committed: default, no dirty reads
- Repeatable Read: same row stable
- Serializable: strongest locking
- Snapshot/RCSI: MVCC, readers do not block writers

Deadlock:

> "SQL Server deadlock error 1205 should be retried with jitter if the operation is safe and idempotent."

## 5.5 SQL Snippets To Remember

Latest row per group:

```sql
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY symbol
               ORDER BY trade_time DESC
           ) AS rn
    FROM trades
)
SELECT *
FROM ranked
WHERE rn = 1;
```

Previous trade price:

```sql
SELECT symbol,
       trade_time,
       price,
       LAG(price) OVER (
           PARTITION BY symbol
           ORDER BY trade_time
       ) AS previous_price
FROM trades;
```

Accounts with no trades:

```sql
SELECT a.account_id
FROM accounts a
WHERE NOT EXISTS (
    SELECT 1
    FROM trades t
    WHERE t.account_id = a.account_id
      AND t.trade_time >= DATEADD(day, -30, SYSUTCDATETIME())
);
```

Running position:

```sql
SELECT symbol,
       trade_time,
       SUM(CASE WHEN side = 'BUY' THEN quantity ELSE -quantity END)
           OVER (PARTITION BY symbol ORDER BY trade_time) AS running_position
FROM trades;
```

## 5.6 SQL Rapid Q&A

Q: `ROW_NUMBER` vs `RANK` vs `DENSE_RANK`?
A: Row number is unique; rank leaves gaps after ties; dense rank does not leave gaps.

Q: SARGable?
A: Search-argument-able; predicate can use index. Avoid functions on indexed column.

Q: Parameter sniffing?
A: Cached plan based on first parameter is bad for later parameter values.

Q: Keyset paging?
A: Use last seen key instead of large OFFSET; better at deep pages.

Q: Temporal table?
A: Keeps history for point-in-time queries.

---

# 6. MongoDB And Unstructured Data - Quick Review

## 6.1 When Mongo Fits

Use Mongo when:

- data is naturally document-shaped
- schema varies
- reads usually fetch the whole aggregate
- high write/read flexibility is needed

Avoid Mongo when:

- heavy cross-document transactions are core
- relational joins dominate
- strict reporting over many entities is primary
- unbounded arrays would grow forever

Say:

> "I model Mongo around query patterns. I embed when data is owned and read together. I reference when data is shared, large, or unbounded."

## 6.2 Indexing

Rules:

- `$match` early in aggregation
- compound indexes follow query pattern
- ESR rule: Equality, Sort, Range
- avoid unindexed regex
- monitor index size

Say:

> "For aggregation I try to put `$match` early so the pipeline can reduce data and use indexes before expensive stages."

## 6.3 Consistency

Know:

- document-level atomicity
- replica sets
- write concern, e.g. `w: majority`
- read concern
- transactions exist but are not the default modelling goal
- 16 MB document limit

## 6.4 Mongo Rapid Q&A

Q: Embed or reference?
A: Embed owned bounded data read together; reference shared or unbounded data.

Q: Unbounded array problem?
A: Document grows forever and hits performance/document-size issues.

Q: Write concern majority?
A: Write acknowledged by majority of replica set.

Q: Good use in finance?
A: flexible reference documents, audit metadata, workflow documents, user layouts/preferences.

---

# 7. Python - Quick Review

## 7.1 Python Mental Model

Python is useful here for:

- analytics
- data pipelines
- FastAPI services
- scripting
- Pandas/NumPy processing
- integration glue

Say:

> "I use Python where it is strong: APIs, data processing, automation, and analytics. For CPU-heavy numeric work I rely on vectorised libraries or processes rather than plain Python threads."

## 7.2 GIL

Say:

> "The GIL means only one thread executes Python bytecode at a time in the standard interpreter. Threads can still help I/O-bound work because they release the GIL while waiting. For CPU-bound work I use multiprocessing, NumPy, Numba, or native extensions."

## 7.3 asyncio

Say:

> "`asyncio` is single-threaded cooperative concurrency. It is good for many I/O tasks, but one blocking call freezes the event loop. For blocking work I use `asyncio.to_thread`, an executor, or move it out of the async path."

Tools:

- `asyncio.Queue(maxsize=N)` for backpressure
- `TaskGroup` for structured concurrency
- timeouts and cancellation
- avoid blocking DB/HTTP clients in async endpoints

## 7.4 FastAPI

Say:

> "FastAPI is ASGI-based. `async def` runs on the event loop and must not block. Normal `def` endpoints can run in a thread pool. I use Pydantic at boundaries for validation and keep domain logic separate."

## 7.5 Pandas / NumPy

Say:

> "In Pandas I avoid row-by-row loops. I vectorise, use correct dtypes, categorical columns where useful, and Parquet for efficient storage. For time-series finance data, `merge_asof` is useful for point-in-time joins."

Key points:

- never `iterrows` in hot paths
- vectorise
- use `Decimal` or integer minor units for exact money, not float
- be careful with lookahead bias in time-series
- Parquet beats CSV for typed analytics storage
- Polars/DuckDB are useful modern tools for local analytics

## 7.6 Python Rapid Q&A

Q: Mutable default argument?
A: Default object is created once at function definition; use `None` then create inside.

Q: `is` vs `==`?
A: `is` identity, `==` value equality.

Q: Generator?
A: Lazy sequence, constant memory.

Q: Type hints?
A: Mostly static; not runtime validation unless using libraries like Pydantic.

Q: `dataclass` vs Pydantic?
A: Dataclass for internal domain data; Pydantic for input/output validation.

Q: CPU-bound Python?
A: processes, NumPy, native extensions, Numba/Cython.

---

# 8. JavaScript, TypeScript, React - Quick Review

## 8.1 Honest Calibration

Say if needed:

> "I am comfortable across frontend work, but my depth is backend. I understand React/component architecture, TypeScript, state, effects, API integration, and build tooling. If you need a pure frontend specialist, that is not my positioning; if you need a full stack engineer with backend depth, that is me."

## 8.2 JavaScript

Memory:

- one main thread
- sync code first
- promises/microtasks before timers/macrotasks
- `const` locks binding, not object
- use `===`
- `??` is null/undefined fallback; `||` treats `0` and empty string as false
- Promise is like `Task<T>`

Say:

> "JavaScript is single-threaded but non-blocking. Slow I/O is handled by the runtime, and callbacks run later. If I block the main thread, the page freezes, similar to blocking the WPF Dispatcher."

## 8.3 TypeScript

Say:

> "TypeScript improves design-time safety, but types are erased at runtime. API data still needs runtime validation at the boundary, for example with Zod or explicit validation."

Know:

- interfaces/types
- generics
- union types
- optional chaining
- strict mode
- compile-time only

## 8.4 React

Say:

> "React is UI as a function of state. Props flow down, events flow up. State should be treated immutably so React can detect changes. `useEffect` is for external work like fetches, timers, and subscriptions, and it needs cleanup like `Dispose` in .NET."

Pitfalls:

- mutating state directly
- missing effect cleanup
- wrong dependency array
- too much global state
- unnecessary re-renders
- not handling failed HTTP responses

## 8.5 JS/React Rapid Q&A

Q: Event loop order?
A: synchronous code, promise microtasks, then timers/macrotasks.

Q: Does `fetch` throw on HTTP 404?
A: No. It resolves; check `response.ok`.

Q: `useMemo`?
A: Cache expensive calculated value; not for correctness.

Q: `useCallback`?
A: Stable function reference, useful for memoized children/effects.

Q: TypeScript runtime validation?
A: Types disappear; validate external data.

---

# 9. REST APIs And Security - Quick Review

## 9.1 REST Basics

Know:

- resources as nouns
- HTTP verbs
- status codes
- pagination/filtering/sorting
- idempotency
- versioning
- Problem Details for errors
- ETag for concurrency

Say:

> "Good REST design uses resource-based URLs, correct verbs, predictable status codes, idempotency where needed, and clear error contracts."

## 9.2 Status Codes

- 200 OK
- 201 Created
- 204 No Content
- 400 Bad Request
- 401 Unauthenticated
- 403 Authenticated but not allowed
- 404 Not found
- 409 Conflict
- 412 Precondition failed
- 422 Validation error, depending on API convention
- 429 Rate limited
- 500 Server error

## 9.3 Idempotency

Say:

> "GET, PUT, and DELETE are idempotent by definition. POST is not automatically idempotent, so for payment/order-style operations I use an idempotency key and store the result for safe retries."

## 9.4 OAuth2 / OIDC / JWT

OAuth2:

- authorization/delegated access
- access token

OIDC:

- identity layer over OAuth2
- ID token

JWT validation:

- verify signature using JWKS
- validate issuer
- validate audience
- validate expiry
- pin algorithm
- handle clock skew carefully

Desktop auth:

> "Desktop apps are public clients and cannot keep a client secret. Use Authorization Code with PKCE."

Service-to-service:

> "Use client credentials, managed identity, mTLS, or workload identity depending on environment."

## 9.5 Security Traps

- Do not use ID token to call APIs.
- Do not trust JWT without validating signature and claims.
- Do not trust object IDs from user; enforce object-level authorization.
- Do not put secrets in code/config.
- Use Key Vault/managed identity.
- Use least privilege.
- Validate input at boundaries.
- Log security events without leaking secrets.

Say:

> "BOLA/IDOR is a serious API risk: even if the user is authenticated, every request must check whether that user can access that specific object."

## 9.6 Auth Rapid Q&A

Q: 401 vs 403?
A: 401 means not authenticated; 403 means authenticated but forbidden.

Q: OAuth vs OIDC?
A: OAuth is delegated access; OIDC is identity.

Q: Access token vs ID token?
A: Access token goes to API; ID token is for client login identity.

Q: Desktop OAuth?
A: Authorization Code with PKCE.

Q: mTLS?
A: Both client and server authenticate with certificates.

Q: Kerberos?
A: Windows/domain authentication common in enterprise/on-prem banking environments.

---

# 10. Architecture, Patterns, Distributed Systems - Quick Review

## 10.1 Architecture Default

Say:

> "I do not start with microservices by default. I start with clear boundaries, often a modular monolith, and split services only when scale, ownership, deployment independence, or fault isolation justify it."

## 10.2 Patterns To Know With Examples

Strategy:

- pricing algorithm
- routing strategy
- validation rules

Decorator:

- retry, caching, logging around service calls

State:

- order lifecycle: New, PartiallyFilled, Filled, Cancelled

Command:

- WPF `ICommand`
- action/request object

Observer:

- `INotifyPropertyChanged`
- event subscriptions

Adapter:

- wrapper around FIX/vendor SDK/legacy service

Facade:

- simplify complex subsystem

Factory:

- create instrument/order handlers based on type

Mediator:

- decouple commands/handlers, e.g. MediatR

Repository:

- abstract persistence, but avoid hiding query needs too much

Unit of Work:

- commit related changes as one transaction

Outbox:

- save DB change and outgoing event in same transaction

Saga:

- long-running workflow with compensating actions

CQRS:

- separate write model from read model

Event Sourcing:

- store events as source of truth; replay for audit/projections

## 10.3 Distributed Systems

Say:

> "Distributed systems fail by timeout, duplication, reordering, partial success, and stale reads. I design consumers to be idempotent, use retries with backoff, isolate failures, add observability, and provide replay or reconciliation."

Key ideas:

- at-least-once delivery means duplicates
- exactly-once is usually a marketing phrase
- idempotency is required
- outbox avoids DB/message dual-write
- DLQ for poison messages
- replay must be controlled
- correlation IDs for traceability
- eventual consistency must be explained to users

## 10.4 CAP / PACELC

CAP:

> "During a network partition, a distributed system must choose between consistency and availability."

PACELC:

> "Even when there is no partition, you still trade latency against consistency."

## 10.5 Design A Live Price System

Question:

> "Design a system that streams live prices to 200 desktop users."

Answer shape:

> "I would separate ingestion, normalization, distribution, and UI updates. Market data enters through adapters, is normalized to an internal schema, partitioned by instrument, and published through a streaming layer. Services maintain latest prices and maybe history. Desktop clients subscribe only to needed instruments. I would conflate latest-value prices, apply backpressure, and measure p99 latency. Orders/executions are separate from prices because they cannot be dropped. Everything has correlation IDs, health checks, metrics, and replay/reconnect handling."

Mention:

- backpressure
- conflation
- reconnect snapshots
- sequence numbers
- idempotency
- authorization by user/portfolio
- p99 latency
- desktop batching

## 10.6 Design Rapid Q&A

Q: CQRS vs Event Sourcing?
A: CQRS separates read and write models. Event sourcing stores events as source of truth. They can be used together but are not the same.

Q: Outbox?
A: Save business change and outgoing message in same DB transaction; background publisher sends later.

Q: Saga?
A: Coordinates distributed workflow using local transactions and compensating actions.

Q: Idempotency?
A: Same request/message can be safely processed more than once.

Q: Circuit breaker?
A: Stop calling failing dependency temporarily to protect system.

Q: Bulkhead?
A: Isolate resources so one failure does not consume everything.

---

# 11. Azure, DevOps, CI-CD, Windows Deployment - Quick Review

## 11.1 Azure Question Strategy

Say first:

> "Before choosing Azure services, I would ask where this runs today: on-prem, Azure, or hybrid. For financial clients, data residency, network boundaries, and release control matter."

## 11.2 Azure Services Map

- App Service: simple web/API hosting
- Container Apps: containerized workloads with scaling
- AKS: Kubernetes when full orchestration control is needed
- Functions: event-driven serverless compute
- Durable Functions: orchestrations/Saga-like workflows
- Service Bus: reliable business messages, queues/topics, DLQ, sessions
- Event Hubs: high-throughput event stream ingestion
- Event Grid: lightweight event notifications
- Azure SQL: relational data
- Cosmos DB: global document/key-value workloads
- Blob Storage: object storage, archive, immutable retention
- Redis: cache, pub/sub, distributed coordination with care
- Key Vault: secrets, certificates, keys
- Managed Identity: avoid stored secrets
- Entra ID: identity
- API Management: API gateway, policies, quotas
- Application Insights/Monitor/Log Analytics: observability
- VNet/Private Endpoint/ExpressRoute: private networking

## 11.3 Service Bus vs Event Hubs vs Event Grid

Say:

> "Service Bus is for important business messages and workflows I cannot lose. Event Hubs is for high-volume streams like telemetry or market-data ingestion. Event Grid is for lightweight notifications that something happened."

## 11.4 CI/CD

Pipeline:

1. build
2. unit tests
3. static analysis
4. secret scan
5. package/containerize
6. dependency/image scan
7. deploy dev
8. integration/contract tests
9. deploy QA with approval
10. database migration
11. deploy production
12. smoke tests
13. rollback/monitoring

Principles:

- build once, promote same artifact
- config from environment
- no secrets in pipeline variables unless secured
- approvals for regulated production
- automated rollback where possible
- feature flags separate deploy from release

## 11.5 Database Migration Strategy

Say:

> "Database migrations are the riskiest part of release. I use expand-and-contract: add new schema in a backward-compatible way, backfill, deploy code that can read/write both if needed, switch reads, then remove old schema later."

## 11.6 Desktop Deployment

Say:

> "A WPF desktop app is a distribution problem. I need MSI/MSIX, code signing, versioning, staged rollout, rollback, and probably SCCM/Intune or an enterprise deployment channel. I also need to consider users who cannot restart during market hours."

## 11.7 Observability

Say:

> "I want logs, metrics, and traces with correlation IDs. For services I watch RED: rate, errors, duration. For resources I watch USE: utilization, saturation, errors. I alert on symptoms users feel, especially p99 latency and error rate."

Include desktop observability:

- crash reports
- UI freezes
- client latency
- version adoption
- failed updates

## 11.8 DevOps Rapid Q&A

Q: Blue/green?
A: Two production environments; switch traffic for quick rollback.

Q: Canary?
A: Release to small percentage first.

Q: Feature flag?
A: Deploy code without enabling feature.

Q: Managed identity?
A: Azure identity for resource access without stored secrets.

Q: Key Vault?
A: Secure secrets/certificates/keys with access control and rotation.

Q: Release timing in finance?
A: Avoid market hours unless controlled emergency process.

---

# 12. Performance And Profiling - Quick Review

## 12.1 Main Answer

Say:

> "I define the target, measure the real workload, find the dominant cost, fix one thing, and measure again. I care about p95, p99, and p99.9, not just average."

## 12.2 Usual Bottlenecks

Check:

- database time
- network calls
- N+1 queries
- over-fetching
- allocations
- GC pauses
- lock contention
- thread pool starvation
- UI rendering/layout
- slow external dependency

## 12.3 .NET Tools

- BenchmarkDotNet: proper microbenchmarks
- dotnet-counters: live runtime counters
- dotnet-trace: tracing
- PerfView: GC/CPU analysis
- dotnet-dump/gcdump: heap analysis
- Visual Studio profiler: CPU, memory, WPF UI responsiveness
- Application Insights/OpenTelemetry: production traces

Say:

> "Sampling profilers are lower overhead and useful in production. Instrumenting profilers are more detailed but can distort timings."

## 12.4 WPF Performance

Focus:

- dispatcher queue
- UI thread work
- layout/render passes
- binding errors
- virtualisation
- batch updates
- shallow visual tree

## 12.5 Python Performance

Tools:

- cProfile
- line_profiler
- tracemalloc
- py-spy

Fixes:

- vectorise
- avoid loops over rows
- use correct dtypes
- use Parquet
- move CPU work to processes/native libraries

## 12.6 Performance Rapid Q&A

Q: Average vs p99?
A: Average hides tail latency; users feel slow tail.

Q: Amdahl's law?
A: Optimizing a small part gives limited total gain; attack dominant cost.

Q: GC pause fix?
A: Reduce allocation and object survival before tuning GC.

Q: Cache what?
A: Cache stable reference data more freely; be careful caching live prices or money-sensitive data.

Q: Load vs stress vs soak?
A: Load is expected traffic; stress finds breaking point; soak checks long-running stability.

---

# 13. Finance Domain - Quick Review

## 13.1 Honest Domain Position

Say:

> "I am an engineer, not a quant. I do not pretend to know every capital markets product. What I can do is understand the domain rules from experts, implement them exactly, test edge cases, preserve audit history, and build systems that are correct under concurrency and failure."

## 13.2 Buy-Side vs Sell-Side

Buy-side:

- asset managers
- pension funds
- sovereign wealth funds
- hedge funds
- they own/invest money

Sell-side:

- banks
- brokers
- market makers
- they execute/provide liquidity/research

Say:

> "Abu Dhabi plus portfolio/order systems suggests buy-side or investment arm, but I would ask rather than assume."

## 13.3 PMS / OMS / EMS

PMS:

- Portfolio Management System
- what do I own?
- what should I own?
- exposures, cash, risk, rebalancing

OMS:

- Order Management System
- order creation
- compliance
- approvals
- lifecycle
- allocation
- audit

EMS:

- Execution Management System
- routing
- brokers/venues
- execution quality
- algo execution
- live market interaction

Memory:

> PMS decides, OMS manages, EMS executes.

## 13.4 Order Lifecycle

Flow:

1. idea/model/rebalance
2. create order
3. pre-trade compliance
4. release to trader/OMS
5. route to broker/venue
6. receive execution reports
7. handle partial fills
8. allocate across accounts/funds
9. confirm
10. settle
11. update positions/cash
12. reconcile with custodian

Order states:

- New
- PendingNew
- Acknowledged
- PartiallyFilled
- Filled
- PendingCancel
- Cancelled
- Rejected
- Expired
- Replaced

Engineering risks:

- partial fills
- duplicate executions
- out-of-order messages
- cancel/fill race
- idempotency
- audit trail
- reconciliation

## 13.5 FIX

Say:

> "FIX is a trading protocol using tag=value fields over a sequenced session. `35=D` is a new order single, `35=8` is an execution report, and `11=ClOrdID` is client order ID. The engineering issues are sequencing, reconnect, replay, duplicate handling, and idempotency."

## 13.6 Positions And P&L

Position:

- quantity held per instrument/account

Market value:

- quantity x price x FX

Realised P&L:

- profit/loss from closed trades

Unrealised P&L:

- profit/loss on open positions marked to market

Use decimal:

- C#: `decimal`
- Python: `Decimal` or integer minor units
- SQL: `DECIMAL`

## 13.7 Financial Math Awareness

Know words:

- volatility
- VaR
- Sharpe ratio
- beta
- tracking error
- drawdown
- duration
- yield
- delta/gamma/vega/theta
- mean-variance optimization

Say:

> "I know the vocabulary and the implementation concerns, but I would rely on quant/domain experts for model definitions. My role is to implement the model correctly, test it, and make results explainable."

## 13.8 Finance Rapid Q&A

Q: PMS vs OMS vs EMS?
A: PMS decides holdings; OMS manages order lifecycle/audit; EMS executes orders.

Q: Partial fill?
A: One order fills in multiple executions; update position after each fill.

Q: Dedupe execution?
A: Use unique execution ID, often `ExecID`.

Q: Cancel/fill race?
A: Cancel request and fill can cross; venue result wins; system must handle both.

Q: Why audit?
A: Need to explain why a number/status was true at a specific time.

Q: Corporate action?
A: Event like split/dividend that can affect holdings and historical reporting.

---

# 14. Coding Exercises Most Likely Today

## 14.1 How To Behave During Coding

Do this:

1. Clarify requirements.
2. State simple approach.
3. Mention complexity.
4. Code cleanly.
5. Talk while coding.
6. Cover edge cases.
7. Discuss thread safety only if relevant.

Say:

> "I'll first implement the simple correct version, then we can discuss performance and concurrency."

## 14.2 Position Keeper

Likely because finance + real-time.

Problem:

> Given trades with symbol, side, quantity, price, maintain position and average cost.

Key things to say:

- `decimal`, not `double`
- dictionary by symbol
- O(1) per trade
- handle buy/sell
- edge case: position flips through zero
- thread safety: partition by symbol or lock per symbol

Skeleton:

```csharp
public enum Side { Buy, Sell }

public sealed record Trade(string Symbol, Side Side, decimal Quantity, decimal Price);

public sealed class Position
{
    public decimal Quantity { get; set; }
    public decimal AvgCost { get; set; }
    public decimal RealisedPnl { get; set; }
}
```

Say:

> "The tricky part is reducing or flipping a position. I would clarify whether average cost resets when crossing zero."

## 14.3 Rolling VWAP

Problem:

> Keep rolling volume-weighted average price.

Formula:

> VWAP = sum(price x quantity) / sum(quantity)

Efficient approach:

- queue for window
- running notional
- running quantity
- O(1) per update

## 14.4 LRU Cache

Data structures:

- `Dictionary<TKey, LinkedListNode<...>>`
- `LinkedList` for recency

Operations:

- get: O(1), move node to front
- put: O(1), update or insert, evict tail

Say:

> "In production I would use MemoryCache unless this is an algorithm exercise."

## 14.5 Concurrency Bug

Code:

```csharp
private int _count;
private Dictionary<string, decimal> _prices = new();

public void OnTick(string symbol, decimal price)
{
    _count++;
    _prices[symbol] = price;
}
```

Answer:

> "`_count++` is not atomic, so use `Interlocked.Increment`. `Dictionary` is not safe for concurrent writes, so use a lock, `ConcurrentDictionary`, or better partition by symbol so each shard is single-writer."

## 14.6 SQL Exercise

Be ready to write:

- latest trade per symbol
- top 5 symbols by notional
- previous trade using `LAG`
- accounts with no trades using `NOT EXISTS`
- running position using `SUM OVER`

## 14.7 Order Lifecycle Classes

Say:

> "I would model Order as an aggregate. I would not expose a public status setter. State changes go through methods like Ack, ApplyFill, RequestCancel, Reject, because each transition has invariants and may raise domain events."

Key:

- private setters
- allowed transitions
- fill quantity cannot exceed order quantity
- idempotent execution application
- domain events
- optimistic concurrency

---

# 15. Likely Interview Questions And Easy Answers

## 15.1 Tell Me About Yourself

Answer:

> "I am a senior full stack engineer, strongest in .NET backend, distributed systems, SQL, Python, and Azure. I have modernised business-critical platforms, worked with event-driven systems and APIs, and handled systems where correctness and reliability matter. I can work across UI and frontend too, but my deepest strength is backend and architecture. This role interests me because it combines .NET, WPF, real-time data, Python, and finance."

## 15.2 Why Luxoft / Why This Role?

Answer:

> "The role is interesting because it is not just CRUD full stack. It has real-time data, desktop UI, distributed backend, Python analytics, and a correctness-critical finance domain. That is the kind of engineering where architecture and detail both matter."

## 15.3 Your WPF Experience?

Answer:

> "I have not used WPF as my primary day-to-day UI recently, so I will not overstate it. My recent UI work has been web, but the same architectural concepts apply: state, binding, change notification, commands, and separation of UI from logic. I have refreshed WPF specifically around MVVM, DependencyProperty, Dispatcher, ObservableCollection, and high-frequency grid updates. My strongest area is still backend and real-time services, but I can be productive in WPF and I know where the traps are."

## 15.4 How Would You Keep A WPF App Responsive?

Answer:

> "Do heavy work off the UI thread, update via Dispatcher only when needed, batch frequent updates, enable virtualisation, avoid unnecessary property changes, and profile layout/render time. For real-time feeds, never update UI per tick."

## 15.5 Explain Async/Await

Answer:

> "`await` lets the thread return while I/O is pending. The compiler creates a state machine and continues after the task completes. It is for waiting, not CPU work. The classic mistake is blocking with `.Result` on a UI/request context, which can deadlock or starve threads."

## 15.6 How Do You Make Code Thread-Safe?

Answer:

> "First I ask what invariant must be protected. Options are immutability, single-writer ownership, partitioning, locks, concurrent collections, channels, or atomic operations. I prefer designs that reduce shared mutable state instead of adding global locks."

## 15.7 Producer/Consumer Design?

Answer:

> "Use a bounded channel. Producers write into it, consumers process from it. Bounded capacity gives backpressure. The full behavior depends on business semantics: drop stale market prices if allowed, but never drop orders or executions."

## 15.8 Slow SQL Query?

Answer:

> "Actual plan first, then logical reads, row estimates, missing indexes, key lookups, joins, parameter sniffing, stale stats, implicit conversions, non-SARGable predicates, and N+1. Fix one thing and measure again."

## 15.9 Microservices Or Monolith?

Answer:

> "I prefer clear boundaries first. A modular monolith can be the right starting point. I split into services when there is a real need: independent scaling, deployment, team ownership, fault isolation, or integration boundary."

## 15.10 How Do You Handle Distributed Consistency?

Answer:

> "I avoid pretending distributed transactions are easy. I use local transactions, outbox for reliable publish, idempotent consumers, retries with backoff, DLQ, reconciliation, and clear eventual consistency rules."

## 15.11 OAuth For Desktop App?

Answer:

> "Authorization Code with PKCE. A desktop app is a public client and cannot safely store a client secret."

## 15.12 Python GIL?

Answer:

> "The GIL allows only one thread to run Python bytecode at once. Threads are still useful for I/O. For CPU work, I use processes or native/vectorized libraries like NumPy."

## 15.13 React Basics?

Answer:

> "React renders UI from state. Props go down, events go up. State should be updated immutably. `useEffect` is for side effects like fetches/subscriptions and must clean up."

## 15.14 Finance Domain Gap?

Answer:

> "I am not a capital markets expert, but I understand the engineering shape: orders, fills, positions, P&L, audit, idempotency, reconciliation, and real-time updates. I have learned complex domains before and I would rely on domain experts for business rules while making the implementation correct and testable."

## 15.15 Why Should We Put You In Front Of The Client?

Answer:

> "Because I am honest about what I know, strong in the core engineering areas, and experienced in client-facing delivery. I can explain trade-offs clearly, ask good questions, and I will not bluff domain knowledge. That reduces risk for Luxoft and for the client."

---

# 16. Questions You Should Ask Them

Pick three.

1. "Is this greenfield or extending an existing platform?"
2. "What is the split between WPF desktop, .NET services, and Python analytics?"
3. "Is the system mostly on-prem, Azure, or hybrid?"
4. "Where does WPF sit: one main trading/portfolio app or multiple internal tools?"
5. "What are the highest-volume real-time data flows in the system?"
6. "How much capital markets domain knowledge do you expect on day one?"
7. "What is the hardest technical problem the team is solving right now?"
8. "What does success look like after six months?"

Best early question:

> "Is this greenfield or extending an existing platform, and roughly what is the split between the desktop client, backend services, and Python/analytics side?"

Close with:

> "This role is interesting to me because it combines real-time, correctness-critical engineering, desktop UI, and backend architecture. What are the next steps?"

---

# 17. Final 60-Minute Checklist

## 60 Minutes Before

- Camera tested
- Mic tested
- Headphones ready
- Screen share tested
- IDE open
- This file open
- Recruiter contact available
- Phone silent
- Water nearby
- Notes page ready

## 15 Minutes Before

Say out loud:

1. one-minute pitch
2. WPF honest answer
3. finance honest answer
4. WPF grid real-time answer
5. async deadlock answer
6. slow SQL query answer
7. producer/consumer answer

## During Interview

Rules:

- Answer first, then explain.
- Give one concrete example.
- Use numbers when possible.
- If you do not know, say it fast and connect to adjacent knowledge.
- Do not ramble.
- Ask clarification if question is vague.
- Keep cloud answers short unless they ask deeper.
- Do not bluff WPF or finance.

Recovery lines:

> "Let me take that from first principles."

> "I have not used that directly, but the adjacent thing I know is..."

> "Actually, let me correct that."

> "Short version: ..."

> "Are you asking about X or Y? I would answer those differently."

---

# 18. Ultra-Fast Memory Sheet

Read this in the final five minutes.

- My headline: .NET-heavy senior full stack engineer, modernising critical systems.
- Do not lead with AI.
- WPF gap: honest, prepared, MVVM/Dispatcher/batching.
- Finance gap: honest, engineering-focused, orders/fills/P&L/audit.
- Money: decimal.
- UI thread: never block; Dispatcher only for minimal UI update.
- Real-time grid: conflate, batch, flush, virtualise.
- Async: waiting not working.
- Deadlock: `.Result` on UI thread.
- Thread safety: avoid shared mutable state.
- Producer/consumer: bounded channel.
- Prices can conflate; orders cannot drop.
- SQL: actual plan and logical reads.
- Security: 401 vs 403, OAuth PKCE, validate JWT, object-level auth.
- Distributed: retries create duplicates, so idempotency.
- Outbox: DB change plus event safely.
- Azure: ask on-prem/hybrid first.
- DevOps: build once, promote artifact.
- Desktop deploy: MSI/MSIX, signing, staged rollout.
- Performance: p99, not average.
- PMS/OMS/EMS: decides, manages, executes.
- Order lifecycle: create, check, route, fill, allocate, settle, reconcile.
- Close: show interest and ask next steps.

