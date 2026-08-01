# 15 — CRAM SHEET (read Monday afternoon, keep open during the call)

> Everything that matters, compressed. If you only read one file on interview day, read this one.

---

## ⚡ THE 12 ANSWERS THAT WIN THIS INTERVIEW

1. **Money** → `decimal` in C#, `Decimal`/minor units in Python, `DECIMAL` in SQL. **Never float.**
   Explicit rounding, instrument-specific precision.
2. **10k ticks/sec into a WPF grid** → don't touch the UI per tick → **conflate latest-per-instrument
   → batch flush on a `DispatcherTimer` (~150 ms) → equality guard in the setter → UI virtualisation
   with recycling → bounded channel, drop-oldest.**
3. **Producer/consumer in .NET today** → `System.Threading.Channels`, bounded for backpressure.
   Prices: drop oldest. Orders: never drop.
4. **async deadlock** → `.Result` on the UI thread + a continuation needing the UI thread.
   Fix: async all the way, or `ConfigureAwait(false)` in libraries.
5. **`volatile` ≠ atomic** → use `Interlocked` for compound operations.
6. **Deadlock prevention** → consistent lock ordering.
7. **Exactly-once** → doesn't exist. At-least-once delivery + **idempotent processing** =
   exactly-once *effects*.
8. **Slow query** → actual execution plan → scans, key lookups, estimate-vs-actual row errors →
   covering index / SARGable predicate / stale stats. Measure, fix one thing, re-measure.
9. **Latest row per group** → `ROW_NUMBER() OVER (PARTITION BY x ORDER BY ts DESC) = 1`.
10. **Desktop OAuth** → Authorization Code + **PKCE**, public client, no secret in the binary, tokens
    in the OS secure store.
11. **Order lifecycle** → order → pre-trade compliance → route → partial fills → allocate → settle →
    reconcile. Dedupe execution reports on **ExecID**.
12. **Architecture default** → modular monolith with clean bounded contexts; split out a service only
    for independent scale, independent release, or team ownership. Every hop is latency + a failure mode.

---

## 🎤 YOUR OPENING (60 seconds — say it, don't read it)

> *Senior engineer, 9+ years, **.NET the whole way** — ASP.NET MVC and WCF early, .NET 9 now.
> The thread is **modernising business-critical platforms without breaking them**: Calrom — airline
> reservation modules off .NET Framework/WCF onto ASP.NET Core with CQRS and **event sourcing** for a
> replayable audit trail; GAC — logistics platform as .NET microservices with DDD, integrated with
> SAP and partner EDI; now — lead backend architecture across content, billing and subscription
> domains, plus a real-time pipeline doing **200,000 events a day under 100 ms**.
> Alongside .NET: **Python** (FastAPI, Pandas, NumPy) and **Azure Solutions Architect Expert**.
> I've also done production AI — I mention it last on purpose; it's a tool I bring, not what I'm
> chasing. What draws me here is real-time data, a proper desktop client, and a domain where the
> numbers have to be right.*

**Calibration line (use it in the first 5 minutes):**
> *"Quick calibration: deepest in .NET backend, distributed/event-driven systems and Azure. Python
> and SQL strong and hands-on. On WPF I'll be honest — I've been in web UI for years and I've been
> rebuilding WPF hands-on recently. And I've no capital markets background, which I'd like to talk
> about."*

---

## 🔴 THE TWO HONEST ANSWERS (know the shape, not the script)

**WPF:** haven't been in it recently → but MVVM/binding/change-notification is the same model I use
daily in Angular/React → **built a real-time positions blotter this week: 5,000 rows, 20 ticks/sec,
`ObservableCollection`, dispatcher marshalling, virtualisation; learned you must batch on a channel
and flush on a timer or you flood the dispatcher** → I'd be productive quickly; WPF isn't where the
difficulty in this system lives.

**Finance:** no capital markets → but airline reservations at Calrom is closer than it looks —
mission-critical inventory under concurrency, GDS/IATA partner integration, and a compliance
requirement that drove event sourcing → I've started on the domain (order lifecycle, OMS vs EMS vs
PMS, FIX, NAV) → I've learned two hard domains from scratch before → *"how much domain knowledge do
you expect on day one?"*

---

## 📌 C# / .NET
- Value vs ref: **location depends on declaration** (struct field of a class → heap, inline).
- Boxing = heap alloc + copy. Avoid in hot loops. `IEquatable<T>` on structs.
- `readonly struct`, `in` params, `Span<T>`/`stackalloc` = zero-allocation parsing.
- GC: gen 0/1/2 + **LOH ≥ 85 KB (not compacted)** + POH. Server GC = per-core heaps.
  Low latency → **reduce allocation**, don't tune the GC.
- `IDisposable` deterministic; finalizers cost an extra GC cycle; `GC.SuppressFinalize`.
- `IEnumerable` (memory) vs `IQueryable` (expression tree → SQL). `ToList()` too early = disaster.
- Override `Equals` → **must** override `GetHashCode`. Never hash a mutable field.
- `throw;` preserves the stack; `throw ex;` resets it. Exception filters `when`.
- DI: Singleton/Scoped/Transient; **captive dependency**; `IHttpClientFactory` (sockets + DNS).
- EF: `AsNoTracking`, projection kills N+1, `rowversion` optimistic concurrency, Dapper on hot reads.
- `decimal` vs `double`. `checked` for money arithmetic.
- LTS: **.NET 8 and 10**. WPF supported on modern .NET (Windows-only).

## 📌 Concurrency
- **I/O-bound → async. CPU-bound → threads/`Parallel`.** Say this first, always.
- `await` = state machine + continuation. `ConfigureAwait(false)` in libraries.
- `async void` = event handlers only. Never `.Result`/`.Wait()` on a UI thread.
- Thread-pool starvation: injection ~1 thread/500 ms.
- `lock` on a **private** object. Can't `await` in a `lock` → `SemaphoreSlim.WaitAsync`.
- `volatile` = ordering/visibility, **not** atomicity. `Interlocked` = atomic. CAS =
  `CompareExchange`.
- Deadlock: mutual exclusion + hold-and-wait + no preemption + **circular wait** → break the last one.
- `ConcurrentDictionary.GetOrAdd` factory can run twice.
- `Channel<T>` bounded = backpressure. **Single-writer principle**: partition state per
  instrument/account → parallelism without shared mutable state.
- Latency = **p99/p99.9**, never averages. LMAX Disruptor / ring buffer for the extreme case.

## 📌 WPF
- Retained-mode, GPU-composed, XAML = object construction.
- **DP value precedence**: animation > **local value** > triggers > style > inherited > default.
  (Local value set in code beats a style trigger — the classic "my trigger stopped working".)
- DPs for controls; `INotifyPropertyChanged` for view-models. `[CallerMemberName]` + equality guard.
- `ObservableCollection` notifies add/remove — **not** item property changes.
- Binding: `Mode`, `UpdateSourceTrigger` (`PropertyChanged` for live filters), `RelativeSource`,
  `ElementName`, converters, `IDataErrorInfo`/`INotifyDataErrorInfo`.
- MVVM: VM has no `System.Windows.Controls`. `ICommand`/`RelayCommand` + `CanExecute`.
  Dialogs via `IDialogService`. **CommunityToolkit.Mvvm** today; **Prism** common in trading apps.
- Threading: **UI thread affinity**; `Dispatcher.InvokeAsync`;
  `BindingOperations.EnableCollectionSynchronization` for background collection edits; `Freeze()`
  brushes.
- Perf: virtualisation + **recycling**, never a `StackPanel` items panel, watch the Output window for
  silent binding errors, `ICollectionView` for sort/filter/group.
- Leaks: **event handlers** (`WeakEventManager`), `DispatcherTimer`, static resources.

## 📌 SQL
- `LEFT JOIN` + right-table predicate in `WHERE` = silent `INNER JOIN`.
- `NOT IN` + NULL = no rows → `NOT EXISTS`.
- Window fns: `ROW_NUMBER`/`RANK`/`DENSE_RANK`, `LAG`/`LEAD`, `SUM() OVER (… ROWS BETWEEN …)`.
- Clustered = data order (one). Non-clustered + `INCLUDE` = **covering** → no key lookup.
- Composite index = **leftmost prefix**. SARGability: no functions on the column.
- Parameter sniffing; stale statistics; `SET STATISTICS IO ON` → logical reads.
- Isolation: RC (default) → RR → Serializable; **Snapshot/RCSI = MVCC**. Deadlock = **1205**, retry.
- Keyset paging beats `OFFSET` at depth. Temporal tables / SCD Type 2 for point-in-time.
- Mongo: `$match` first, **ESR** compound index order, `w:"majority"`, 16 MB doc limit, don't embed
  unbounded arrays.
- Columnar (columnstore/ClickHouse/Parquet/**kdb+**) for scans + compression; row store for OLTP.

## 📌 Patterns & design
- Strategy, Decorator (retry/cache/logging), **State (order lifecycle)**, Command (WPF `ICommand`),
  Observer (`INotifyPropertyChanged`), Mediator (MediatR), Composite (portfolio → positions),
  Flyweight (shared instrument reference data), Adapter/ACL (vendor SDK, FIX, GDS).
- CQRS ≠ event sourcing. Event sourcing = audit + replay, costs = projections, versioning, snapshots.
- SAGA + compensations; **Outbox** for the dual-write problem; idempotency keys; DLQ + replay.
- Strangler Fig for legacy modernisation; shadow/parallel-run to de-risk.
- CAP is about partitions; **PACELC** for the everyday latency-vs-consistency trade.
- SOLID with *examples*, not definitions. Singleton → "I use DI singleton lifetime."

## 📌 API & auth
- 401 (who?) vs 403 (not allowed). PUT/DELETE idempotent; POST + `Idempotency-Key`.
- RFC 7807 Problem Details. ETag + `If-Match` → 412 for optimistic concurrency.
- OAuth flows: **Auth Code + PKCE** (apps incl. desktop), **Client Credentials** (service-to-service).
  Implicit/ROPC deprecated.
- OIDC = identity layer; **ID token → client, access token → API**.
- JWT: verify signature via **JWKS**, `iss`/`aud`/`exp`, **pin the algorithm**. Can't revoke → short TTL.
- Kerberos/Windows auth + mTLS = the on-prem bank world.
- **BOLA/IDOR is the #1 API vuln** — re-check object-level authorisation every request.

## 📌 Python
- **GIL**: one thread executes bytecode. I/O → threads/asyncio fine; CPU → processes or C extensions
  (NumPy releases the GIL). 3.13 has an experimental free-threaded build.
- asyncio: `TaskGroup` (3.11+), `asyncio.Queue` for backpressure, **one blocking call freezes the loop**
  → `asyncio.to_thread`.
- Mutable default args; `is` vs `==`; generators for constant memory; `__slots__`; `Protocol`;
  pydantic at the edges, dataclasses in the core.
- Pandas: vectorise, never `iterrows`; categorical dtypes; **Parquet**; `merge_asof` for point-in-time
  joins (no lookahead bias). Polars/DuckDB if you want to sound current.
- FastAPI: `def` → threadpool, `async def` → event loop (don't block it).

## 📌 Finance (enough for Monday)
- Buy-side (owns the money) vs sell-side. Front/middle/back office.
- Order → compliance → route → **partial fills** → allocate → settle (T+1/T+2) → reconcile.
- **PMS** what should I own · **OMS** manage the order + audit · **EMS** execute it well.
- FIX: tag=value, sequenced session; `35=D` new order, `35=8` execution report, `11=ClOrdID`.
- Position, market value = qty × price × FX; realised vs unrealised P&L; mark-to-market; NAV.
- VaR, volatility (×√252), Sharpe, beta, tracking error, drawdown. Greeks: delta/gamma/vega/theta.
- Mean-variance optimisation = constrained quadratic program → efficient frontier.
- *"I'm an engineer, not a quant — my job is to implement the models correctly, precisely and fast."*

---

## ❓ ASK THESE (pick 3)
1. Is this greenfield or extending an existing platform? What's the split between the desktop client,
   the services, and the Python/analytics side?
2. Who's the end client and what does the team look like day to day?
3. Where does WPF sit — one flagship app, or several tools? And is any of it still .NET Framework?
4. What's the hardest technical problem the team has right now?
5. How much domain knowledge do you expect on day one versus picking it up?
6. What does success look like for this person in the first six months?

**Close with:** *"This is genuinely the kind of engineering I want to be doing — real-time, correctness
-critical, with a proper desktop client. What are the next steps?"*

---

## ✅ 60 MINUTES BEFORE
- [ ] Camera, mic, headphones, lighting tested · link opens · **screen share tested**
- [ ] IDE open with the WPF blotter project (so you can show it if invited)
- [ ] This file + your 5 questions on screen. Nothing else. Notifications off.
- [ ] Water. Phone silent but reachable. Recruiter's number: **+380 66 008 2016**
- [ ] Say the 60-second pitch out loud once
- [ ] Breathe. You have 9 years of real evidence. **Answer, then stop talking.**
