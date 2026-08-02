# 16 — MOCK DRILLS: RAPID-FIRE, CODING & SCRIPTS

> ⚠️ **Use this out loud, timed, camera on.**
> Reading it silently is worth about 20% of the value. Speaking is what builds recall under pressure.

---

# PART A — 120 RAPID-FIRE (answer each in 20 seconds or less)

**How to use it:** cover the right column. Say the answer out loud. **Target: 100+ with no
hesitation.** Anything you miss, go back to the source file.

### C# / .NET → `03`

| # | Q | A |
|---|---|---|
| 1 | Value vs reference type | Holds the data vs holds a reference |
| 2 | Is a struct always on the stack? | **No** — a struct field of a class lives on the heap, inline |
| 3 | Boxing cost | Heap allocation, copy, indirection. Kills hot loops |
| 4 | Avoid boxing on a struct | Implement `IEquatable<T>` |
| 5 | `readonly struct` benefit | No defensive copies; compiler-enforced immutability |
| 6 | `Span<T>` restriction | Stack-only. No heap, no `await`, no lambda capture |
| 7 | `Span<T>` vs `Memory<T>` | Stack-only, sync vs heap-storable, works across `await` |
| 8 | GC generations | 0, 1, 2, plus the LOH (≥ 85 KB) and POH |
| 9 | Why is the LOH a problem? | Not compacted → fragmentation → OOM with free memory |
| 10 | Server vs workstation GC | Throughput, a heap per core vs lower pause |
| 11 | Low latency: tune the GC? | **No — reduce allocation** |
| 12 | `IDisposable` vs finalizer | Deterministic vs GC-driven; finalizers cost an extra cycle |
| 13 | `GC.SuppressFinalize` | "Already cleaned up" — skip the finalizer queue |
| 14 | #1 .NET memory leak | Event handler subscriptions |
| 15 | `IEnumerable` vs `IQueryable` | In-memory vs an expression tree translated to SQL |
| 16 | Deferred execution | The query runs on enumeration, not definition |
| 17 | Why override `GetHashCode` with `Equals`? | Hash collections bucket by hash — lookups fail otherwise |
| 18 | Never hash on… | A mutable field |
| 19 | `const` vs `readonly` | Compile-time, baked into callers vs runtime, set in the constructor |
| 20 | `ref` / `out` / `in` | Initialise before / assign inside / read-only by reference |
| 21 | `virtual`+`override` vs `new` | Polymorphic dispatch vs hiding by static type |
| 22 | `throw;` vs `throw ex;` | Preserves the stack trace vs resets it |
| 23 | Exception filter | `catch (X e) when (…)` — runs before the stack unwinds |
| 24 | Are exceptions cheap in .NET? | **No.** Never for control flow in a hot loop |
| 25 | `decimal` vs `double` | **Money vs science. Never float for money** |
| 26 | `string` `==` | Value equality — an operator overload |
| 27 | Interning risk | Locking on a string locks a process-global object |
| 28 | `out` vs `in` generics | Covariant producer vs contravariant consumer |
| 29 | Array covariance flaw | Compiles, throws at runtime. Generics fixed it |
| 30 | `record` gives you | Value equality, `ToString`, `with`, init-only |
| 31 | DI lifetimes | Singleton / Scoped / Transient |
| 32 | Captive dependency | A Scoped injected into a Singleton — lives forever |
| 33 | Why `IHttpClientFactory`? | Socket exhaustion **and** stale DNS |
| 34 | EF N+1 fix | Projection with `Select`, or `Include`, or `AsSplitQuery` |
| 35 | `AsNoTracking` | Skips change tracking — faster read-only queries |
| 36 | EF version conflict | `rowversion` in the `WHERE`; 0 rows means someone changed it first |
| 37 | EF vs Dapper | Writes with a unit of work vs hand-tuned reads |
| 38 | `ValueTask` | Avoids an allocation when usually synchronous. Don't await twice |
| 39 | `ArrayPool<T>` | Rent and return buffers. Return in `finally` |
| 40 | .NET LTS versions | **8 and 10** |
| 41 | Is WPF supported on .NET 10? | **Yes** — Windows-only |

### Concurrency → `04`

| # | Q | A |
|---|---|---|
| 42 | The framing sentence | **Waiting → async. Working → threads** |
| 43 | Async for CPU work? | No — that's what the pool and `Parallel` are for |
| 44 | What does `await` compile to? | A state machine plus a continuation on the task |
| 45 | Does `await` block a thread? | **No** — that's the whole point |
| 46 | `ConfigureAwait(false)` | Don't resume on the captured context. Libraries yes, UI no |
| 47 | The classic deadlock | `.Result` on the UI thread + a continuation needing that thread |
| 48 | `async void` allowed when? | **Event handlers only** |
| 49 | Thread pool starvation | Blocking pool threads; injection is ~1 per 500 ms |
| 50 | Lock on `this` / a string / a Type? | **Never.** Use a private dedicated object |
| 51 | Can you `await` inside a `lock`? | No — `SemaphoreSlim.WaitAsync` |
| 52 | `volatile` guarantees | Ordering and visibility. **Not atomicity** |
| 53 | Make `x++` atomic | `Interlocked.Increment` |
| 54 | The lock-free primitive | `Interlocked.CompareExchange` — compare and swap |
| 55 | Deadlock prevention | **Consistent lock ordering** |
| 56 | Four Coffman conditions | Mutual exclusion, hold-and-wait, no preemption, circular wait |
| 57 | False sharing | Hot variables sharing a cache line → invalidation storms |
| 58 | `ConcurrentDictionary.GetOrAdd` trap | The factory may run more than once |
| 59 | Modern producer/consumer | **`System.Threading.Channels`** |
| 60 | A bounded channel gives you | **Backpressure**, with an explicit full policy |
| 61 | Market data full-buffer policy | **Drop oldest** — a stale price is worthless |
| 62 | Order messages full-buffer policy | **Never drop.** Real backpressure and persist |
| 63 | Single-writer principle | Partition state so one thread owns it — locks vanish |
| 64 | Latency measurement | **Percentiles — p99, p99.9. Never averages** |
| 65 | Thread-safe singleton | `Lazy<T>`, or a static readonly field |
| 66 | Why `while` not `if` around `Monitor.Wait`? | Spurious wakeups and lost races |
| 67 | Is async parallelism? | No. Two awaits in a row are sequential |

### WPF → `05`

| # | Q | A |
|---|---|---|
| 68 | What is WPF? | Retained-mode, vector, GPU-composed. XAML is object construction |
| 69 | Dependency property, why? | Sparse storage, inheritance, change notification, value precedence |
| 70 | DP precedence order | Animation > **local value** > triggers > style > inherited > default |
| 71 | Why did my style trigger stop working? | **A local value was set in code — it wins** |
| 72 | DP vs `INotifyPropertyChanged` | Controls vs view-models |
| 73 | `ObservableCollection` limitation | **Doesn't notify on item *property* changes** |
| 74 | Default `UpdateSourceTrigger` for `TextBox.Text` | `LostFocus` |
| 75 | Live filter box needs | `UpdateSourceTrigger=PropertyChanged` |
| 76 | Logical vs visual tree | What you wrote vs template-expanded |
| 77 | `StaticResource` vs `DynamicResource` | Once at load vs re-resolved on change |
| 78 | `DataTemplate` vs `ControlTemplate` | How **data** looks vs how a **control** looks |
| 79 | Routed event kinds | Bubbling, tunnelling (`Preview*`), direct |
| 80 | UI thread rule | Only the creating thread may touch a `DispatcherObject` |
| 81 | Update UI from a background thread | `Dispatcher.InvokeAsync`; `EnableCollectionSynchronization` for collections |
| 82 | ⭐ **10k ticks/sec into a grid?** | **Conflate → batch → flush on a timer → equality guard → virtualise → bounded channel** |
| 83 | Virtualisation killer | Putting the items control in a `StackPanel` or unconstrained `ScrollViewer` |
| 84 | `Freeze()` | Immutable, shareable across threads, faster |
| 85 | #1 WPF memory leak | Event handler subscriptions → `WeakEventManager` |
| 86 | Dialog from a VM? | Inject an `IDialogService` |
| 87 | Why MVVM? | **Testability** — the view-model is a plain testable class |

### SQL → `07`

| # | Q | A |
|---|---|---|
| 88 | Why did my `LEFT JOIN` become an `INNER JOIN`? | Right-table predicate in `WHERE` instead of `ON` |
| 89 | `NOT IN` with NULLs | Returns nothing. Use `NOT EXISTS` |
| 90 | Latest row per group | `ROW_NUMBER() OVER (PARTITION BY … ORDER BY … DESC) = 1` |
| 91 | `RANK` vs `DENSE_RANK` | 1,1,3 (gap) vs 1,1,2 (no gap) |
| 92 | Covering index | Contains every column needed → no key lookup |
| 93 | Composite index rule | **Leftmost prefix** — like a phone book |
| 94 | SARGable | Don't wrap the column in a function; use a range |
| 95 | Parameter sniffing | The plan is cached from the first parameter value |
| 96 | Stale statistics | Bad row estimates → bad plans. "It was fast last week" |
| 97 | Deadlock error number | **1205** — retry with jitter |
| 98 | Snapshot isolation | MVCC — readers never block writers |
| 99 | Keyset vs offset paging | Constant cost vs degrades with depth |
| 100 | Honest perf metric | **Logical reads** |
| 101 | Money in SQL | `DECIMAL`. **Never `FLOAT`** |
| 102 | Mongo aggregation first stage | **`$match`** — so it can use an index |
| 103 | Mongo compound index order | **ESR** — Equality, Sort, Range |
| 104 | Row vs columnar | Point reads vs scans, aggregates and compression |
| 105 | The tick database everyone names | **kdb+** |

### API, architecture & Python → `08`, `09`, `06`

| # | Q | A |
|---|---|---|
| 106 | 401 vs 403 | Don't know you vs know you and you can't |
| 107 | Idempotent verbs | GET, PUT, DELETE. **Not POST** — use an `Idempotency-Key` |
| 108 | OAuth flow for a desktop app | **Authorization Code + PKCE**, public client, no secret |
| 109 | OIDC vs OAuth | Identity (ID token) vs delegated access (access token) |
| 110 | JWT validation | JWKS signature, `iss`, `aud`, `exp`, **pin the algorithm** |
| 111 | JWT downside | Can't revoke before expiry → short TTL plus refresh rotation |
| 112 | #1 API vulnerability | **BOLA/IDOR** — re-check object access every request |
| 113 | Exactly-once delivery | **Doesn't exist** — messages can repeat, so processing must be safe to repeat |
| 114 | The dual-write fix | **Outbox pattern** |
| 115 | CAP, the senior version | **PACELC** — latency vs consistency even without a partition |
| 116 | Microservices or monolith? | **Modular monolith by default**; split for scale, release or ownership |
| 117 | What is the GIL? | One lock — only one thread runs Python bytecode at a time |
| 118 | Python: CPU vs I/O | Processes or NumPy vs asyncio or threads |
| 119 | The asyncio trap | **One blocking call freezes the whole loop** |
| 120 | Money in Python | `Decimal` from a string, or integer minor units |

---

# PART B — CODING EXERCISES (do four, timed at 25 minutes each)

The invite says *"code exercise could be done"*. Most likely: something practical, 20–30 minutes, on a
shared screen. ⚠️ **Narrate constantly.**

## B1. ⭐ Position keeper — the most likely shape for this role

> *"Given a stream of trades (symbol, side, quantity, price), maintain the current position and average
> cost per symbol, and compute realised and unrealised P&L."*

```csharp
public sealed class PositionKeeper
{
    private readonly Dictionary<string, Position> _positions = new(StringComparer.Ordinal);

    public void Apply(Trade t)
    {
        var p = _positions.TryGetValue(t.Symbol, out var existing) ? existing : new Position();
        var signed = t.Side == Side.Buy ? t.Quantity : -t.Quantity;

        if (p.Quantity == 0 || Math.Sign(p.Quantity) == Math.Sign(signed))
        {
            // opening or increasing → weighted-average cost
            var newQty = p.Quantity + signed;
            p.AvgCost  = (p.AvgCost * p.Quantity + t.Price * signed) / newQty;
            p.Quantity = newQty;
        }
        else
        {
            // reducing or closing → realise P&L on the closed amount
            var closing = Math.Min(Math.Abs(signed), Math.Abs(p.Quantity));
            p.Realised += (t.Price - p.AvgCost) * closing * Math.Sign(p.Quantity);
            p.Quantity += signed;
            if (p.Quantity == 0) p.AvgCost = 0m;
            // a flip THROUGH zero should re-open at t.Price — call this out
        }
        _positions[t.Symbol] = p;
    }

    public decimal Unrealised(string symbol, decimal lastPrice)
        => _positions.TryGetValue(symbol, out var p) ? (lastPrice - p.AvgCost) * p.Quantity : 0m;
}
```

**Say all of this while you type:**
- *"`decimal`, not `double` — this is money."*
- *"Ordinal string comparison for symbols."*
- *"O(1) per trade."*
- *"The edge case is a position flipping through zero — I'd confirm the expected behaviour."*
- *"Thread safety is out of scope unless you want it — and then I'd partition by symbol so each
  symbol is single-writer, rather than take a global lock."*

## B2. ⭐ Rolling VWAP

```csharp
public sealed class RollingVwap
{
    private readonly Queue<(decimal px, decimal qty)> _window = new();
    private readonly int _size;
    private decimal _notional, _qty;

    public RollingVwap(int size) => _size = size;

    public decimal Add(decimal price, decimal qty)
    {
        _window.Enqueue((price, qty));
        _notional += price * qty; _qty += qty;
        if (_window.Count > _size)
        {
            var (p, q) = _window.Dequeue();
            _notional -= p * q; _qty -= q;      // O(1), not O(n)
        }
        return _qty == 0 ? 0m : _notional / _qty;
    }
}
```
**The point to make:** *"O(1) per update, because I maintain running sums instead of recomputing the
window."*

## B3. ⭐ Order book — best bid/ask with O(1) cancel

```csharp
private readonly SortedDictionary<decimal, LinkedList<Order>> _bids =
    new(Comparer<decimal>.Create((a, b) => b.CompareTo(a)));            // descending
private readonly SortedDictionary<decimal, LinkedList<Order>> _asks = new();  // ascending
private readonly Dictionary<long, LinkedListNode<Order>> _index = new();      // O(1) cancel

public decimal? BestBid => _bids.Count > 0 ? _bids.First().Key : null;
```
**Talk through:** add is O(log n) · cancel is O(1) via the index · best bid/ask is O(1) to O(log n) ·
matching walks the opposite side while the prices cross · **FIFO within a price level — that's
price-time priority.** Then: *"A real venue would use arrays of price levels for speed."*

## B4. Find and fix the concurrency bug

```csharp
private int _count;
private Dictionary<string, decimal> _prices = new();
public void OnTick(string sym, decimal px) { _count++; _prices[sym] = px; }   // 3 threads call this
```
**Answer:** *"Two bugs. `_count++` isn't atomic — that's `Interlocked.Increment`. And `Dictionary`
isn't thread-safe for concurrent writes; it can **corrupt itself or spin forever on a resize**. Fix
with `ConcurrentDictionary`, or a lock — or best, **partition by symbol so each thread owns a
shard**."*

## B5. LRU cache — O(1) get and put
A `Dictionary<K, LinkedListNode<(K,V)>>` plus a `LinkedList` for recency. On get, move to the front.
On put over capacity, evict the tail. **State both complexities.** Then: *"In production I'd reach for
`MemoryCache`."*

## B6. Merge k sorted trade files by timestamp
A min-heap of the head of each file. O(n log k). `PriorityQueue<T,TPriority>` in .NET 6+.

## B7. SQL on the spot
- Top 5 symbols by traded notional today.
- Each trade with the previous trade's price for the same symbol (`LAG`).
- Accounts with no trades in the last 30 days (`NOT EXISTS`).
- Running position per symbol (`SUM(...) OVER (PARTITION BY ... ORDER BY ...)`).

## B8. Design-in-code
> *"Design the classes for an order and its lifecycle."*

An `Order` aggregate with **private setters**, a `Status` enum, intention-revealing methods (`Ack`,
`ApplyFill`, `RequestCancel`), invariants enforced inside, domain events raised out, and a
`rowversion` for concurrency.
⚠️ **Explicitly say why you don't expose a public `Status` setter** — that's the whole point of the
exercise.

---

# PART C — MOCK INTERVIEW SCRIPTS

## C1. The likely 60-minute shape

| Minutes | What | Your move |
|---|---|---|
| 0–3 | Intros | Warm, brief, energy up. **Write the interviewer's name down.** |
| 3–8 | *"Tell me about yourself"* | The 60-second pitch. **Do not ramble to four minutes.** |
| 8–18 | *"Walk me through your current project"* | C.A.R.D.S. End with *"happy to go deeper on any part."* |
| 18–40 | Deep technical Q&A | `03`, `04`, `05`, `07`, `08`. **Project → problem → decision.** |
| 40–52 | Code exercise (if run) | Part B. Clarify → brute force + complexity → clean code → edge cases. |
| 52–58 | Your questions | Ask three, listen properly, react to the answers. |
| 58–60 | Close | Clear interest, then ask about next steps. |

## C2. The 10 questions most likely to come up

**Rehearse full answers out loud. These ten cover most of the interview.**

1. Tell me about yourself / your current project. → `02`
2. **How much WPF have you done?** → `13` Part 4 — the honest script
3. **How would you update a WPF grid from a high-frequency feed without freezing the UI?** → `05` Part 7
4. **Explain `async`/`await`, and where it deadlocks.** → `04` Part 3
5. How do you make a class thread-safe? What would you use for producer/consumer? → `04` Parts 4, 6
6. Tell me about the GC. How would you reduce pauses in a latency-sensitive app? → `03` Part 2
7. **This query is slow — how do you approach it?** → `07` Part 4
8. **Design a system that streams live prices to 200 desktop users.** → `08` C4
9. Tell me about a pattern you've used and one you regret. → `08` A5
10. **You have no capital markets background — why should we put you in front of this client?**
    → `13` Part 4 + `11` Part 11

## C3. Self-run mock — 45 minutes, camera on, no notes

1. **Record yourself** answering C2 numbers 1, 2, 3, 6 and 8. *(25 minutes)*
2. **Watch it back.** Score yourself on:
   - filler words
   - rambling past 90 seconds
   - saying "basically" and "kind of"
   - eye contact
   - ⚠️ **whether you gave a *specific example* or just a definition** *(10 minutes)*
3. **Redo the two worst answers.** *(10 minutes)*

## C4. The three habits that raise your score most

1. ⚠️ **Answer, then stop.** Silence after a complete answer reads as confidence. Don't fill it.
2. **One concrete example per answer, with a number in it.**
3. **"Let me check I understand the question"** when it's ambiguous. It never looks weak, and it stops
   you answering the wrong thing for two minutes.

## C5. Recovery lines — memorise these, they save interviews

| Situation | Say |
|---|---|
| **You don't know it** | *"I haven't worked with that directly. What I do know that's adjacent is X — is that the direction you're probing?"* |
| **You go blank** | *"Let me take that from first principles."* |
| **You realise you're wrong mid-answer** | *"Actually, let me correct that —"* and correct it. ⚠️ **This scores points. It does not lose them.** |
| **You rambled** | *"Short version: [one sentence]."* |
| **The question is vague** | *"Are you asking about X or Y? I'd answer those differently."* |
| **Technical trouble** | Have your phone ready as a hotspot, and the recruiter's number to hand. |
