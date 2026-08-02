# 15 — ⭐ THE CRAM SHEET

> **If you read one file on interview day, read this one.**
> Everything that matters, in plain words. Keep it open during the call.

---

# 1. THE 12 SIMPLE ANSWERS TO REMEMBER

Learn these first. They are short on purpose.

| # | If they ask about… | Say |
|---|---|---|
| **1** | **Money** | "Use decimal types for money. Never float." |
| **2** | **10k ticks/sec into a WPF grid** | "Do not update the UI per tick. Keep latest values, batch them, and flush on a timer." |
| **3** | **Producer/consumer in .NET** | "Use a bounded `Channel`. Prices can drop old values; orders must not be dropped." |
| **4** | **The async deadlock** | "Do not block the UI thread with `.Result`. Use async all the way." |
| **5** | **`volatile`** | "`volatile` is visibility, not safety for `x++`. Use `Interlocked`." |
| **6** | **Deadlock prevention** | "Take locks in the same order every time." |
| **7** | **Exactly-once** | "Messages may repeat. Make processing safe to repeat." |
| **8** | **A slow query** | "Check the actual plan, fix one clear problem, then measure again." |
| **9** | **Latest row per group** | "Use `ROW_NUMBER()` per group and keep row 1." |
| **10** | **Desktop OAuth** | "Use Authorization Code with PKCE. A desktop app cannot keep a secret." |
| **11** | **Order lifecycle** | "Create, check, route, fill, allocate, settle, reconcile. Dedupe executions." |
| **12** | **Architecture default** | "Start with a modular monolith. Split services only for a real reason." |

---

# 2. 🎤 YOUR OPENING (60 seconds — say it, don't read it)

> *"Senior engineer, nine-plus years, and **.NET the whole way** — ASP.NET MVC and WCF early, .NET 9
> now.*
>
> *The thread is **modernising business-critical platforms without breaking them**. At Calrom, airline
> reservation modules off .NET Framework and WCF onto ASP.NET Core with CQRS and **event sourcing**,
> because we needed a replayable audit trail. At GAC, the logistics platform as .NET microservices
> with DDD, integrated with SAP and partner EDI. Now, leading backend architecture across content,
> billing and subscription domains, plus a real-time pipeline doing **200,000 events a day under 100
> milliseconds**.*
>
> *Alongside .NET: **Python** — FastAPI, Pandas, NumPy — and **Azure Solutions Architect Expert**.*
>
> *I've also done production AI work. I mention it last on purpose — it's a tool I bring, not what
> I'm chasing.*
>
> *What draws me here is real-time data, a proper desktop client, and a domain where the numbers have
> to be right."*

## The calibration line — say it in the first five minutes

> *"Quick calibration so I don't waste your time: deepest in .NET backend, distributed and
> event-driven systems, and Azure. Python and SQL are strong and hands-on.*
>
> *On WPF I'll be honest — I've been in web UI for years, and I've been rebuilding WPF hands-on
> recently rather than claiming it as day-job depth. And I've no capital markets background, which
> I'd like to talk about."*

⚠️ **Why this works:** interviewers don't punish honest calibration. They punish **discovering** a
gap themselves. Saying it early turns an interrogation into a conversation.

---

# 3. 🔴 THE TWO HONEST ANSWERS

**Know the shape, not a script.** Both must **end well** — never let the answer stop on the gap.

## WPF
Haven't been in it recently → **but** MVVM, binding and change notification is the same model I use
daily in Angular and React → **built a real-time positions blotter this week: 5,000 rows, 20 ticks a
second, `ObservableCollection`, dispatcher marshalling, virtualisation. What I learned is you *have
to* batch onto a channel and flush on a timer or you flood the dispatcher** → I'd be productive
quickly, and **WPF isn't where the difficulty in this system lives.**

## Finance
No capital markets → **but** airline reservations at Calrom is closer than it looks: mission-critical
inventory under concurrency, GDS/IATA partner integration, and a compliance requirement that drove
event sourcing → I've started on the domain: order lifecycle, OMS vs EMS vs PMS, FIX, NAV → I've
learned two hard domains from scratch before → **"How much domain knowledge do you expect on day
one?"**

---

# 4. 📌 C# / .NET

- **Value vs reference:** where it lives depends on **where it's declared**. A struct field of a class
  is on the heap, inline.
- **Boxing** = heap allocation + copy. Avoid in hot loops. `IEquatable<T>` on structs.
- `readonly struct`, `in` params, `Span<T>` / `stackalloc` = **zero-allocation parsing**.
- **GC:** gen 0/1/2 + **LOH at 85 KB, not compacted** + POH. Server GC = a heap per core.
  ⚠️ **Low latency → reduce allocation, don't tune the GC.**
- `IDisposable` is deterministic. Finalizers cost an extra GC cycle. `GC.SuppressFinalize`.
- **`IEnumerable`** (memory) vs **`IQueryable`** (expression tree → SQL). `ToList()` too early is a
  disaster.
- Override `Equals` → **must** override `GetHashCode`. **Never hash a mutable field.**
- `throw;` preserves the stack; `throw ex;` resets it. Exception filters with `when`.
- **DI:** Singleton / Scoped / Transient. **Captive dependency.** `IHttpClientFactory` for sockets
  **and** DNS.
- **EF:** `AsNoTracking`, projection kills N+1, `rowversion` for version checks, Dapper on hot
  reads.
- **`decimal` vs `double`.** `checked` for money arithmetic.
- **LTS: .NET 8 and 10.** WPF **is** supported on modern .NET, Windows-only.

# 5. 📌 CONCURRENCY

- ⚠️ **"Waiting → async. Working → threads." Say this first, always.**
- `await` = a state machine plus a continuation. `ConfigureAwait(false)` in libraries.
- `async void` = **event handlers only**. Never `.Result` or `.Wait()` on a UI thread.
- Thread-pool starvation: injection is about **1 thread per 500 ms**.
- `lock` on a **private** object. **Can't `await` inside a `lock`** → `SemaphoreSlim.WaitAsync`.
- **`volatile` = ordering. `Interlocked` = atomic.** CAS is `CompareExchange`.
- **Deadlock:** mutual exclusion + hold-and-wait + no preemption + **circular wait** → break the last
  one with consistent ordering.
- `ConcurrentDictionary.GetOrAdd` — the factory can run twice.
- **`Channel<T>` bounded = backpressure.**
- ⚠️ **Single-writer principle:** partition state per instrument or account → **parallelism without
  shared mutable state.** *The best architectural answer in this whole area.*
- **Latency = p99 / p99.9, never averages.** LMAX Disruptor / ring buffer for the extreme case.

# 6. 📌 WPF

- Retained-mode, GPU-composed. **XAML is object construction.**
- ⚠️ **DP precedence:** animation > **local value** > triggers > style > inherited > default.
  *A local value set in code beats a style trigger — that's "my trigger stopped working".*
- **DPs for controls. `INotifyPropertyChanged` for view-models.**
- `[CallerMemberName]` + **an equality guard** (this is what survives 20 ticks/sec).
- ⚠️ **`ObservableCollection` notifies add/remove — NOT item property changes.**
- Binding: `Mode`, `UpdateSourceTrigger` (**`PropertyChanged` for live filters**), `RelativeSource`,
  converters.
- **MVVM:** the VM has no `System.Windows.Controls`. `ICommand` + `CanExecute`. Dialogs via
  `IDialogService`. **CommunityToolkit.Mvvm** today; **Prism** is common in trading apps.
- **Threading:** UI thread affinity → `Dispatcher.InvokeAsync`;
  `BindingOperations.EnableCollectionSynchronization` for background collection edits; `Freeze()`
  brushes.
- **Perf:** virtualisation **with recycling**; never a `StackPanel` items panel; watch the Output
  window for silent binding errors; `ICollectionView` for sort/filter/group.
- **Leaks:** **event handlers** (`WeakEventManager`), `DispatcherTimer`, static resources.

# 7. 📌 SQL

- ⚠️ `LEFT JOIN` + a right-table predicate in `WHERE` = a silent `INNER JOIN`.
- ⚠️ `NOT IN` + NULL = **no rows**. Use `NOT EXISTS`.
- Window functions: `ROW_NUMBER` / `RANK` / `DENSE_RANK`, `LAG` / `LEAD`, `SUM() OVER (… ROWS …)`.
- Clustered = the data order (one per table). Non-clustered + `INCLUDE` = **covering** → no key
  lookup.
- Composite index = **leftmost prefix**. SARGability: **no functions on the column**.
- **Parameter sniffing.** Stale statistics. `SET STATISTICS IO ON` → **logical reads**.
- Isolation: Read Committed (default) → Repeatable Read → Serializable. **Snapshot/RCSI = MVCC.**
  Deadlock = **1205**, retry with jitter.
- **Keyset paging beats `OFFSET` at depth.** Temporal tables / SCD Type 2 for point-in-time.
- **Mongo:** `$match` first, **ESR** compound order, `w:"majority"`, 16 MB document limit, don't embed
  unbounded arrays.
- **Columnar** (columnstore / ClickHouse / Parquet / **kdb+**) for scans and compression; row store
  for OLTP.

# 8. 📌 PATTERNS & DESIGN

- **Strategy** (pricing/routing) · **Decorator** (retry/cache/logging) · ⭐ **State (the order
  lifecycle)** · **Command** (WPF `ICommand`) · **Observer** (`INotifyPropertyChanged`) ·
  **Mediator** (MediatR) · **Composite** (portfolio → positions) · **Flyweight** (shared instrument
  reference data) · **Adapter / ACL** (vendor SDK, FIX, GDS).
- **CQRS ≠ event sourcing.** Event sourcing = audit + replay; costs = projections, versioning,
  snapshots.
- **SAGA** + compensations · **Outbox** for the dual-write problem · **idempotency keys** · DLQ +
  replay.
- **Strangler Fig** for legacy modernisation. **Shadow mode** to de-risk — run both, compare, then
  ship.
- **CAP is about partitions. PACELC is the everyday latency-vs-consistency trade.**
- **SOLID with *examples*, not definitions.** Singleton → *"I use DI singleton lifetime."*

# 9. 📌 API & AUTH

- **401 = who are you. 403 = you're not allowed.**
- **PUT/DELETE idempotent. POST isn't** → `Idempotency-Key`.
- **Problem Details** for errors. **`ETag` + `If-Match` → 412** for version checks.
- **OAuth flows:** **Auth Code + PKCE** (including desktop), **Client Credentials** (service to
  service). Implicit and password grant are **deprecated**.
- **OIDC = identity.** ID token → the client. Access token → the API. **Never mix them.**
- **JWT:** verify via **JWKS**, check `iss` / `aud` / `exp`, **pin the algorithm**. Can't revoke →
  short TTL.
- **Kerberos / Windows auth + mTLS = the on-prem bank world.**
- ⚠️ **BOLA/IDOR is the #1 API vulnerability** — re-check object-level authorisation every request.

# 10. 📌 PYTHON

- **GIL:** one thread runs bytecode at a time. **I/O → asyncio or threads. CPU → processes or NumPy**
  (which releases the lock). 3.13 has an experimental free-threaded build.
- **asyncio:** `TaskGroup` (3.11+), `asyncio.Queue(maxsize=N)` for backpressure — *"Python's
  `Channel<T>`"* — and ⚠️ **one blocking call freezes the whole loop** → `asyncio.to_thread`.
- Mutable default args · `is` vs `==` · generators for constant memory · `__slots__` · `Protocol` ·
  **Pydantic at the edges, dataclasses in the core**.
- **Type hints are erased at runtime — exactly like TypeScript.**
- **Pandas:** vectorise, **never `iterrows`**, categorical dtypes, **Parquet**, **`merge_asof` for
  point-in-time joins** (no lookahead bias). Polars / DuckDB to sound current.
- **FastAPI:** `def` → thread pool, `async def` → event loop. **Don't block the loop.**

# 11. 📌 JAVASCRIPT (light — it's only "Medium" on the spec)

- **One thread, non-blocking.** Event loop: **sync → promises → timers.**
- `const` by default; `const` isn't immutability.
- **Array methods are LINQ with different names** — `map`/`filter`/`reduce`/`find`.
- **A Promise is a `Task<T>`.** ⚠️ **`fetch` does not throw on a 404** — check `res.ok`.
- **TypeScript types are erased at runtime** → validate with **Zod** at the boundary.
- **React: UI = f(state). Props down, events up.** `useEffect` cleanup **is `Dispose()`**.
- ⚠️ **Say the honest line:** *"My depth is backend."*

# 12. 📌 FINANCE (enough for the technical round)

- **Buy-side owns the money.** Sell-side executes. Front / middle / back office.
- Order → compliance → route → **partial fills** → allocate → settle (T+1/T+2) → reconcile.
- **PMS** = what should I own · **OMS** = manage the order and the audit · **EMS** = execute it well.
- **FIX:** tag=value over a sequenced session. `35=D` new order, `35=8` execution report,
  `11=ClOrdID`.
- Market value = qty × price × FX. **Realised vs unrealised P&L.** Mark-to-market. NAV.
- VaR · volatility **× √252** · Sharpe · beta · tracking error · drawdown.
  Greeks: **delta, gamma, vega, theta**.
- Mean-variance optimisation = choose portfolio weights to balance return and risk.
- ⚠️ **"I'm an engineer, not a quant — my job is to implement the models correctly, precisely and
  fast."**

---

# 13. ❓ ASK THESE (pick three)

1. ⭐ **"Is this greenfield or extending an existing platform? And what's the split between the
   desktop client, the services, and the Python/analytics side?"** *(Ask early — the answer tells you
   where to aim everything else.)*
2. *"Who's the end client, and what does the team look like day to day?"*
3. *"Where does WPF sit — one flagship app or several tools? Is any of it still .NET Framework?"*
4. *"What's the hardest technical problem the team has right now?"*
5. *"How much domain knowledge do you expect on day one versus picking it up?"*
6. *"What does success look like for this person at six months?"*

**Close with:**
> *"This is genuinely the kind of engineering I want to be doing — real-time, correctness-critical,
> with a proper desktop client. **What are the next steps?**"*

---

# 14. ✅ 60 MINUTES BEFORE

- [ ] Camera, mic, headphones, lighting tested · the link opens · **screen share tested**
- [ ] IDE open with the WPF blotter project, in case you're invited to show it
- [ ] **This file** plus your five questions on screen. Nothing else. Notifications off.
- [ ] Water on the desk. Phone silent but reachable. **Recruiter's number to hand.**
- [ ] Say the 60-second pitch out loud, once
- [ ] Pen and paper ready — **write the interviewer's name down in the first minute**

---

# 15. 🧠 THE FIVE THINGS TO REMEMBER WHEN YOUR MIND GOES BLANK

1. **Answer, then stop talking.** Silence is confidence.
2. **Give an example, not a definition.** One project, one problem, one decision.
3. **Say "I don't know" fast, then say what you *do* know that's adjacent.** It reduces their risk.
   A bluff increases it.
4. **Say the number.** 200,000 events a day. Under 100 milliseconds. 99.99%. Nine years.
5. **You have nine years of real evidence.** You are not guessing. Breathe.
