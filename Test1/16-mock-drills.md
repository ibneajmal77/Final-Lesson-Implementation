# 16 — Mock Drills: Rapid-Fire, Coding Exercises & Interview Scripts

> Use this **out loud**, timed, camera on. Reading it silently is worth about 20% of the value.

---

## PART A — 80 rapid-fire questions (answer in ≤20 seconds each)

Cover the answer column. Target: **70+ correct, no hesitation.** Anything you miss → go back to the
source file.

### C# / .NET (`03`)
| # | Q | A |
|---|---|---|
| 1 | Value vs reference type | Data vs reference; location depends on declaration, not the kind |
| 2 | Is a struct always on the stack? | **No** — a struct field of a class lives on the heap inline |
| 3 | Boxing cost | Heap alloc + copy + indirection; kills hot loops |
| 4 | `readonly struct` benefit | No defensive copies, compiler-enforced immutability |
| 5 | `Span<T>` restriction | `ref struct` — stack only, no heap, no `await`, no lambda capture |
| 6 | GC generations | 0/1/2 + LOH (≥85 KB) + POH |
| 7 | Why is LOH a problem | Not compacted by default → fragmentation → OOM with free memory |
| 8 | Server vs workstation GC | Per-core heaps & threads, throughput vs lower pause |
| 9 | `IDisposable` vs finalizer | Deterministic vs GC-driven; finalizers add a GC cycle |
| 10 | `GC.SuppressFinalize` why | Already cleaned up — skip the finalizer queue |
| 11 | `IEnumerable` vs `IQueryable` | In-memory delegates vs expression tree translated to SQL |
| 12 | Deferred execution | Query runs on enumeration, not definition |
| 13 | Why override `GetHashCode` with `Equals` | Hash collections bucket by hash; otherwise lookups fail |
| 14 | Never hash on… | A mutable field |
| 15 | `const` vs `readonly` | Compile-time baked into callers vs runtime, set in ctor |
| 16 | `ref` / `out` / `in` | Init before / assign inside / readonly by-ref |
| 17 | `virtual`+`override` vs `new` | Polymorphic dispatch vs hiding by static type |
| 18 | `throw;` vs `throw ex;` | Preserves vs resets stack trace |
| 19 | Exception filter | `catch (X e) when (cond)` — runs before unwinding |
| 20 | `decimal` vs `double` | Money vs science. **Never float for money** |
| 21 | `string` `==` | Value equality (operator overload) |
| 22 | Interning risk | `lock` on a string locks a process-global object |
| 23 | Covariance `out` / contravariance `in` | Producer / consumer positions |
| 24 | Array covariance flaw | Compiles, throws `ArrayTypeMismatchException` at runtime |
| 25 | `record` gives you | Value equality, `ToString`, `with` expressions, init-only |
| 26 | DI lifetimes | Singleton / Scoped / Transient |
| 27 | Captive dependency | Scoped injected into Singleton → lives forever, breaks scoping |
| 28 | Why `IHttpClientFactory` | Socket exhaustion + DNS staleness |
| 29 | EF N+1 fix | Projection with `Select`, or `Include`, or `AsSplitQuery` |
| 30 | `AsNoTracking` | Skips change tracking — faster read-only queries |
| 31 | EF optimistic concurrency | `rowversion` in the WHERE; 0 rows → `DbUpdateConcurrencyException` |
| 32 | `ValueTask` vs `Task` | Avoids alloc when usually-synchronous; don't await twice |
| 33 | `ArrayPool<T>` | Rent/return buffers to avoid LOH churn; return in `finally` |
| 34 | .NET LTS versions | 8 and 10 (3 yrs); 9 is STS |
| 35 | Is WPF supported on .NET 10? | Yes — Windows-only |

### Concurrency (`04`)
| # | Q | A |
|---|---|---|
| 36 | async for CPU work? | No — async is for I/O; use the pool/`Parallel` for CPU |
| 37 | What does `await` compile to | A state machine + continuation registered on the task |
| 38 | `ConfigureAwait(false)` | Don't resume on the captured context — libraries yes, UI no |
| 39 | The classic deadlock | `.Result` on the UI thread + a continuation needing the UI thread |
| 40 | `async void` allowed when | Event handlers only |
| 41 | Thread pool starvation | Blocking pool threads; injection is ~1/500 ms |
| 42 | `lock` on `this`/string/Type? | Never — use a private dedicated object |
| 43 | Can you `await` inside `lock`? | No — use `SemaphoreSlim.WaitAsync` |
| 44 | `volatile` guarantees | No reordering, fresh read — **not** atomicity |
| 45 | Make `x++` atomic | `Interlocked.Increment` |
| 46 | Lock-free primitive | `Interlocked.CompareExchange` (CAS) |
| 47 | Deadlock prevention (main) | Consistent lock ordering |
| 48 | Four Coffman conditions | Mutual exclusion, hold-and-wait, no preemption, circular wait |
| 49 | False sharing | Hot vars share a cache line → invalidation storms; pad to 64 B |
| 50 | `ConcurrentDictionary.GetOrAdd` trap | Factory may run more than once |
| 51 | Modern producer/consumer | `System.Threading.Channels` |
| 52 | Bounded channel gives you | Backpressure, with an explicit full-mode policy |
| 53 | Market data full-buffer policy | **Drop oldest** — stale prices are worthless |
| 54 | Order messages full-buffer policy | Never drop — real backpressure + persist |
| 55 | Single-writer principle | Partition state so one thread owns it → most locks vanish |
| 56 | Latency is measured as | Percentiles (p99/p99.9), never averages |
| 57 | Thread-safe singleton in C# | `Lazy<T>` or a static readonly field |
| 58 | Why `while` not `if` around `Monitor.Wait` | Spurious wakeups / lost races |

### WPF (`05`)
| # | Q | A |
|---|---|---|
| 59 | Dependency property purpose | Sparse storage, inheritance, change notification, value precedence |
| 60 | DP value precedence top | Animation > local value > triggers > style > inherited > default |
| 61 | Why did my style trigger stop working | A local value was set in code — it wins |
| 62 | DP vs `INotifyPropertyChanged` | Controls vs view-models |
| 63 | `ObservableCollection` limitation | Doesn't notify on item *property* changes |
| 64 | Default `UpdateSourceTrigger` for `TextBox.Text` | `LostFocus` |
| 65 | Logical vs visual tree | Authored vs template-expanded |
| 66 | `StaticResource` vs `DynamicResource` | Once at load vs re-resolved on change |
| 67 | `DataTemplate` vs `ControlTemplate` | How data looks vs how a control looks |
| 68 | Routed event kinds | Bubbling, tunnelling (`Preview*`), direct |
| 69 | UI thread rule | Only the creating thread may touch a `DispatcherObject` |
| 70 | Update UI from a background thread | `Dispatcher.InvokeAsync`, or `EnableCollectionSynchronization` for collections |
| 71 | 10k ticks/sec into a grid — what do you do | Conflate latest-per-instrument, batch flush on a timer, virtualise, equality guards |
| 72 | Virtualisation killer | Putting the items control in a `StackPanel`/unconstrained `ScrollViewer` |
| 73 | `Freeze()` | Makes a `Freezable` immutable, shareable across threads, faster |
| 74 | #1 WPF memory leak | Event handler subscriptions → `WeakEventManager` |
| 75 | Dialog from a VM without breaking MVVM | Inject an `IDialogService` |

### SQL / data / API (`07`, `09`)
| # | Q | A |
|---|---|---|
| 76 | Why did my LEFT JOIN become an INNER JOIN | Right-table predicate in `WHERE` instead of `ON` |
| 77 | `NOT IN` with NULLs | Returns nothing — use `NOT EXISTS` |
| 78 | Latest row per group | `ROW_NUMBER() OVER (PARTITION BY … ORDER BY … DESC) = 1` |
| 79 | Covering index | Includes all needed columns → no key lookup |
| 80 | SARGable | Don't wrap the column in a function; use a range instead |
| 81 | Parameter sniffing | Cached plan from the first param value; `RECOMPILE`/`OPTIMIZE FOR` |
| 82 | Deadlock error number (SQL Server) | 1205 — retry with backoff |
| 83 | Snapshot isolation | MVCC; readers don't block writers |
| 84 | Keyset vs offset paging | Constant cost vs degrades with depth |
| 85 | Mongo aggregation first stage | `$match` — so it can use an index |
| 86 | Mongo compound index order | ESR: Equality, Sort, Range |
| 87 | Row vs columnar | Point reads vs scans/aggregates + compression |
| 88 | 401 vs 403 | Not authenticated vs not permitted |
| 89 | Idempotent verbs | GET, PUT, DELETE (POST isn't — use an Idempotency-Key) |
| 90 | OAuth flow for a desktop app | Authorization Code + **PKCE**, public client, no secret |
| 91 | OIDC vs OAuth | Identity (ID token) vs delegated access (access token) |
| 92 | JWT validation checklist | Signature via JWKS, `iss`, `aud`, `exp`/`nbf`, pin the algorithm |
| 93 | JWT downside | Can't revoke before expiry → short TTL + refresh rotation |
| 94 | #1 API vulnerability | BOLA/IDOR — re-check object-level authorisation every request |
| 95 | Exactly-once delivery | Doesn't exist — at-least-once + idempotent processing |

---

## PART B — Coding exercises (do 4 of these, timed 25 min, on paper or in a plain editor)

The invite says *"code exercise could be done"*. Most likely: something practical, 20–30 minutes,
shared screen or a collaborative editor. **Narrate constantly.**

### B1. ⭐ Position keeper (most likely shape for this role)
> *"Given a stream of trades `(symbol, side, quantity, price)`, maintain the current position and
> average cost per symbol, and compute realised and unrealised P&L given a latest-price lookup."*

```csharp
public sealed class PositionKeeper
{
    private readonly Dictionary<string, Position> _positions = new(StringComparer.Ordinal);

    public void Apply(Trade t)
    {
        ref var p = ref CollectionsMarshal.GetValueRefOrAddDefault(_positions, t.Symbol, out _);
        var signed = t.Side == Side.Buy ? t.Quantity : -t.Quantity;

        if (p.Quantity == 0 || Math.Sign(p.Quantity) == Math.Sign(signed))
        {
            // opening or increasing: weighted-average cost
            var newQty = p.Quantity + signed;
            p.AvgCost = (p.AvgCost * p.Quantity + t.Price * signed) / newQty;
            p.Quantity = newQty;
        }
        else
        {
            // reducing or closing: realise P&L on the closed amount
            var closing = Math.Min(Math.Abs(signed), Math.Abs(p.Quantity));
            p.Realised += (t.Price - p.AvgCost) * closing * Math.Sign(p.Quantity);
            p.Quantity += signed;
            if (p.Quantity == 0) p.AvgCost = 0m;
            // NOTE: a flip through zero should re-open at t.Price — worth calling out
        }
    }

    public decimal Unrealised(string symbol, decimal lastPrice)
        => _positions.TryGetValue(symbol, out var p) ? (lastPrice - p.AvgCost) * p.Quantity : 0m;
}
```
**Say while coding:** `decimal` not `double` (money); ordinal string comparison; O(1) per trade;
the sign/flip edge case; thread safety is out of scope unless they ask (then: single-writer per
symbol partition, or a lock per symbol).

### B2. ⭐ Rolling VWAP / moving average over a window
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
**Point to make:** O(1) per update by maintaining running sums, not recomputing the window.
Mention floating-point drift if they'd used `double` — another reason for `decimal` here.

### B3. ⭐ Order book: best bid/ask with O(1) cancel
```csharp
// Price levels sorted; FIFO within a level (price-time priority)
private readonly SortedDictionary<decimal, LinkedList<Order>> _bids =
    new(Comparer<decimal>.Create((a, b) => b.CompareTo(a)));   // descending
private readonly SortedDictionary<decimal, LinkedList<Order>> _asks = new();  // ascending
private readonly Dictionary<long, LinkedListNode<Order>> _index = new();      // O(1) cancel

public decimal? BestBid => _bids.Count > 0 ? _bids.First().Key : null;
```
Talk through: add O(log n), cancel O(1) via the index, best bid/ask O(1)–O(log n), matching walks the
opposite side while prices cross. Mention that a real venue uses arrays of price levels for speed.

### B4. LRU cache — O(1) get/put
`Dictionary<K, LinkedListNode<(K,V)>>` + `LinkedList` for recency; on get, move to front; on put over
capacity, evict the tail. State both complexities. (In .NET you'd reach for `MemoryCache` in
production — say so.)

### B5. Find and fix the concurrency bug
```csharp
private int _count;
private Dictionary<string, decimal> _prices = new();
public void OnTick(string sym, decimal px) { _count++; _prices[sym] = px; }   // called from 3 threads
```
Answer: `_count++` is not atomic → `Interlocked.Increment`; `Dictionary` is not thread-safe for
concurrent writes and can **corrupt/infinite-loop** on resize → `ConcurrentDictionary`, or a lock, or
partition by symbol so each thread owns a shard (best).

### B6. Merge k sorted trade files by timestamp
Min-heap of the head of each file: O(n log k). `PriorityQueue<T,TPriority>` in .NET 6+.

### B7. SQL on the spot
- Top 5 symbols by traded notional today.
- Each trade with the previous trade's price for the same symbol (`LAG`).
- Accounts with no trades in the last 30 days (`NOT EXISTS`).
- Running position per symbol (`SUM(...) OVER (PARTITION BY ... ORDER BY ...)`).

### B8. Design-in-code
> *"Design the classes for an order and its lifecycle."* → `Order` aggregate with private setters,
> a `Status` enum, intention-revealing methods (`Ack`, `ApplyFill`, `RequestCancel`), invariants
> enforced inside, domain events raised out, `rowversion` for concurrency. Talk about why you *don't*
> expose a public `Status` setter.

---

## PART C — Mock interview scripts

### C1. The Luxoft technical round (Monday) — likely 60-minute shape

| Minutes | What | Your move |
|---|---|---|
| 0–3 | Intros, small talk | Warm, brief, energy up. Camera on, smile. |
| 3–8 | *"Tell me about yourself"* | The 60-second pitch (`02` §3). **Do not ramble to 4 minutes.** |
| 8–18 | *"Walk me through your current project"* | C.A.R.D.S. (`02` §4). End with *"happy to go deeper on any part."* |
| 18–40 | Deep technical Q&A | `03`, `04`, `05`, `07`, `08`. **Depth-first: project → problem → decision.** |
| 40–52 | Code exercise (if run) | Part B. Clarify → brute force + complexity → clean code → edge cases. |
| 52–58 | Your questions | `14`. Ask 3, listen properly, react. |
| 58–60 | Close | Express clear interest + ask about next steps. |

### C2. Ten questions they are most likely to ask (rehearse full answers out loud)
1. Tell me about yourself / your current project.
2. How much WPF have you done? *(→ `02` §5.1 — the honest script)*
3. How would you update a WPF grid from a high-frequency background feed without freezing the UI?
   *(→ `05` §7, the layered answer)*
4. Explain `async`/`await` and where it deadlocks. *(→ `04` §3)*
5. How do you make a class thread-safe? What would you use for producer/consumer? *(→ `04` §4, §6)*
6. Tell me about the GC. How would you reduce pauses in a latency-sensitive app? *(→ `03` §2)*
7. This query is slow — how do you approach it? *(→ `07` §4, `12` §7)*
8. Design a system that streams live prices to 200 desktop users. *(→ `08` §C4)*
9. Tell me about a design pattern you used and one you regret. *(→ `08` §A5)*
10. You have no capital markets background — why should we put you in front of this client?
    *(→ `02` §5.2 + `11` §12)*

### C3. Self-run mock — 45 minutes, camera on, no notes
1. Record yourself answering C2 #1, #2, #3, #6, #8. (25 min)
2. Watch it back. Score yourself on: **filler words, rambling past 90 seconds, saying "basically"
   /"kind of", eye contact, and whether you gave a *specific example* or a definition.** (10 min)
3. Redo the two worst answers. (10 min)

**The three habits that raise your score most:**
- **Answer, then stop.** Silence after a complete answer is confidence. Don't fill it.
- **One concrete example per answer**, with a number in it.
- **"Let me check I understand the question"** when it's ambiguous — it never looks weak, and it
  stops you answering the wrong thing for two minutes.

### C4. Recovery lines (memorise — these save interviews)
- Don't know it: *"I haven't worked with that directly. What I do know that's adjacent is X — is that
  the direction you're probing?"*
- Went blank: *"Let me take that from first principles."*
- Realise you're wrong mid-answer: *"Actually, let me correct that —"* and correct it. **This scores
  points, it doesn't lose them.**
- Rambled: *"Short version: [one sentence]."*
- Question too vague: *"Are you asking about X or Y? I'd answer those differently."*
- Technical trouble: have your phone ready as a hotspot/backup, and the recruiter's number
  (+380 66 008 2016) to hand.
