# 04 — Multithreading, Concurrency & Real-Time Systems

> **The JD says "real-time and multithreaded systems expertise" as a must-have.** In a capital-markets
> desktop/services team this is *the* differentiating round. Expect 15–20 minutes on this alone.

---

## 1. The mental model to state up front

> *"There are two different problems people call concurrency. One is **I/O-bound** — you're waiting on
> a network, disk or database, and the right tool is `async/await`, which frees the thread while you
> wait. The other is **CPU-bound** — you have real work to parallelise, and the right tool is the
> thread pool, `Parallel`/PLINQ, or dedicated threads. Using async for CPU work buys you nothing;
> using threads for I/O wastes ~1 MB of stack each and kills scalability."*

Say that once and you've framed every subsequent question correctly.

---

## 2. Thread vs ThreadPool vs Task

| | `Thread` | `ThreadPool` | `Task` (TPL) |
|---|---|---|---|
| Cost | ~1 MB stack, expensive to create | Reused, pre-warmed | Abstraction *over* the pool |
| Control | Priority, foreground/background, `IsBackground`, name | Little | Rich: continuations, cancellation, exceptions, results |
| Use when | Long-running, dedicated, needs priority/STA — e.g. **a dedicated market-data receive thread** | Short work items | Almost always |

- Threads are **foreground by default** and keep the process alive; thread-pool threads are background.
- The pool grows slowly past `MinThreads` (**~1 thread per 500 ms** hill-climbing). This causes
  *thread pool starvation*: block pool threads on I/O and latency collapses because new threads are
  injected at a crawl. **Naming this earns senior credit.**
- `Task.Run` (queue to pool) vs `Task.Factory.StartNew` — prefer `Task.Run`; `StartNew` with an async
  delegate returns `Task<Task>` and needs `.Unwrap()`, a classic bug. Use `StartNew` only when you
  need `TaskCreationOptions.LongRunning` (which gives a dedicated thread, not a pool thread).

```csharp
// Dedicated, long-lived, high-priority feed handler thread — legitimate use of raw Thread
var t = new Thread(ReceiveLoop) {
    IsBackground = true, Priority = ThreadPriority.AboveNormal, Name = "MarketDataRx"
};
t.Start();
```

---

## 3. async/await — how it actually works

**Q: What does `await` do?**
The compiler rewrites the method into a **state machine**. At an `await` on an incomplete task, the
method *returns to its caller*; the remainder is registered as a continuation on the awaited task.
When the task completes, the continuation is scheduled — onto the captured `SynchronizationContext`
if there is one, otherwise the thread pool. **No thread is blocked while waiting.**

**Q: `ConfigureAwait(false)` — what and why?**
Tells the awaiter *not* to marshal the continuation back to the captured context. In library code
you should use it: it avoids an unnecessary context switch and prevents deadlocks. In WPF/UI code
you generally **do** want the context (so you can touch UI after the await). ASP.NET Core has no
`SynchronizationContext`, so it doesn't matter there.

**Q: The classic async deadlock — explain it.** *(Very likely, especially in a desktop shop.)*

```csharp
// WPF button handler — DEADLOCKS
private void Button_Click(object s, RoutedEventArgs e)
{
    var data = LoadAsync().Result;      // ← blocks the UI thread
}
private async Task<string> LoadAsync()
{
    await _http.GetStringAsync(url);    // captures the UI SynchronizationContext
    return "done";                      // ← continuation needs the UI thread… which is blocked
}
```

The UI thread is blocked in `.Result`; the continuation is queued to the UI thread; neither can
proceed. **Fixes:** `await` all the way up (`private async void Button_Click`), or
`.ConfigureAwait(false)` inside `LoadAsync`. **Rule: never `.Result` / `.Wait()` on a UI or ASP.NET
classic thread.**

**Q: `async void` — when is it acceptable?**
Only for **event handlers**, because the signature is fixed. Otherwise it's poison: you can't await
it, you can't catch its exceptions (they're raised on the sync context and usually crash the process),
and you can't compose it. Even in event handlers, wrap the body in try/catch.

**Other async points worth having ready:**
- `Task.WhenAll` for fan-out; `Task.WhenAny` for first-wins/timeouts.
- `CancellationToken` should be threaded through **every** async API you write.
- `IAsyncEnumerable<T>` + `await foreach` for streaming results (e.g. a tick stream).
- `TaskCompletionSource<T>` to bridge callback/event-based APIs into tasks — use
  `TaskCreationOptions.RunContinuationsAsynchronously` to avoid running continuations inline on your
  I/O thread.
- Async is not parallelism: `await a; await b;` is sequential; `await Task.WhenAll(a, b)` is concurrent.

---

## 4. Synchronisation primitives — pick the right one

| Primitive | Scope | Cost | Use for |
|---|---|---|---|
| `lock` / `Monitor` | In-process | Cheap uncontended (~20 ns) | Default mutual exclusion |
| `Interlocked` | In-process | Cheapest (single CPU instruction) | Counters, CAS, atomic swap |
| `SemaphoreSlim` | In-process (+`WaitAsync`) | Cheap | **Throttling/limit concurrency; the only async-friendly lock** |
| `Mutex` | Cross-process (named) | Expensive (kernel) | Single-instance app enforcement |
| `ReaderWriterLockSlim` | In-process | Moderate | Many readers, rare writer |
| `SpinLock` | In-process | Burns CPU | Only for extremely short, uncontended critical sections |
| `Barrier`, `CountdownEvent` | In-process | — | Phase coordination |
| `ManualResetEventSlim` / `AutoResetEvent` | Signalling | — | Wait-for-signal |

**Key facts:**
- `lock(x)` is `Monitor.Enter/Exit` in a try/finally. **It is reentrant** for the same thread.
- ⚠️ **Never `lock` on:** `this`, a `Type`, a `string` (interned → shared globally!), or any public
  object. Use a dedicated `private readonly object _gate = new();`.
- ⚠️ **You cannot `await` inside a `lock`** — the compiler forbids it, because Monitor has thread
  affinity (the releasing thread must be the acquiring thread). Use `SemaphoreSlim.WaitAsync()`:

```csharp
private readonly SemaphoreSlim _gate = new(1, 1);

async Task UpdateAsync()
{
    await _gate.WaitAsync(ct);
    try { await DoWorkAsync(ct); }
    finally { _gate.Release(); }     // ALWAYS release in finally
}
```

**Q: `volatile` — what does it actually guarantee?**
It prevents the compiler/JIT/CPU from reordering reads and writes around that field, and forces reads
from memory rather than a register (acquire on read, release on write). It does **not** make
compound operations atomic — `volatile int x; x++;` is still a race. For that, `Interlocked.Increment`.

```csharp
// Atomic operations without a lock
Interlocked.Increment(ref _messageCount);
Interlocked.Exchange(ref _latestPrice, newPrice);
// Compare-and-swap loop — the basis of all lock-free algorithms
long original, updated;
do { original = _max; updated = Math.Max(original, candidate); }
while (Interlocked.CompareExchange(ref _max, updated, original) != original);
```

---

## 5. The failure modes — define each crisply

| Problem | Definition | Prevention |
|---|---|---|
| **Race condition** | Result depends on timing of unsynchronised access | Lock, atomic ops, or immutability |
| **Deadlock** | Two+ threads each hold a lock the other needs, forever | **Consistent lock ordering** (the main answer), lock timeouts (`Monitor.TryEnter`), reduce lock scope, avoid nested locks |
| **Livelock** | Threads active but making no progress (endlessly retrying/backing off) | Randomised backoff |
| **Starvation** | A thread never gets the resource | Fair locks, avoid priority abuse |
| **Priority inversion** | Low-priority thread holds a lock a high-priority thread needs | Priority inheritance; avoid mixed priorities |
| **Torn read** | Non-atomic read of a >word-sized value (e.g. `long`/`decimal` on 32-bit) sees half old/half new | `Interlocked.Read`, or lock, or make it a reference to an immutable object |
| **False sharing** | Two hot variables share a 64-byte cache line; cores invalidate each other | Pad to cache-line size (`[StructLayout(LayoutKind.Explicit)]` / 64-byte padding) |
| **Thread pool starvation** | Blocking calls consume pool threads faster than injection | Never block on async; async all the way |

**The four Coffman conditions for deadlock** (mutual exclusion, hold-and-wait, no preemption,
circular wait) — quoting these and then saying *"in practice we break circular wait with a global
lock ordering"* is a strong answer.

---

## 6. Concurrent collections & producer/consumer

| Type | Use |
|---|---|
| `ConcurrentDictionary<K,V>` | Thread-safe map. ⚠️ `GetOrAdd`'s factory can run **more than once** — make it idempotent/cheap; for expensive creation store `Lazy<T>`. |
| `ConcurrentQueue/Stack/Bag<T>` | Lock-free-ish collections |
| `BlockingCollection<T>` | Classic bounded producer/consumer, blocking API |
| **`System.Threading.Channels`** | **Modern async producer/consumer — the answer to give** |
| `ImmutableList/Dictionary` | Snapshot semantics; readers never lock |

**Channels — the pattern to demo (learn this; it maps directly onto market data):**

```csharp
// Bounded channel = built-in BACKPRESSURE. When full, producers wait (or drop).
var channel = Channel.CreateBounded<Tick>(new BoundedChannelOptions(10_000)
{
    FullMode = BoundedChannelFullMode.DropOldest,   // for market data, newest price wins
    SingleReader = true,
    SingleWriter = false
});

// Producer (feed handler thread)
await channel.Writer.WriteAsync(tick, ct);

// Consumer
await foreach (var tick in channel.Reader.ReadAllAsync(ct))
    ProcessTick(tick);
```

⚠️ **Say this out loud in the interview** — it's the single best answer to *"how would you handle a
high-frequency data feed?"*:
> *"Bounded channel with a drop-oldest policy. For prices, backpressure that blocks the producer is
> wrong — you can't slow the exchange down, and a stale price is worthless. So you bound the buffer
> and drop stale ticks, keeping the latest per instrument. For orders you'd do the opposite: never
> drop, apply real backpressure and persist, because every order message matters."*

That answer shows you understand **the domain drives the concurrency policy** — exactly what a
capital-markets interviewer is listening for.

---

## 7. Parallelism for CPU-bound work

```csharp
Parallel.For(0, n, i => Compute(i));
Parallel.ForEach(items, new ParallelOptions { MaxDegreeOfParallelism = 8 }, Process);
await Parallel.ForEachAsync(items, ct, async (x, t) => await ProcessAsync(x, t)); // .NET 6+
var results = source.AsParallel().WithDegreeOfParallelism(4).Where(...).ToArray(); // PLINQ
```

- Partitioning: range partitioning for arrays, chunk partitioning for `IEnumerable`.
- ⚠️ Parallel is *slower* for small workloads — overhead of partitioning + coordination.
- Aggregation must be thread-safe: use the `localInit`/`localFinally` overload of `Parallel.For`, or
  `Interlocked`, not a shared `+=`.
- `Parallel.For` exceptions surface as `AggregateException`.
- Amdahl's law: speedup is capped by the serial fraction — worth quoting if asked "will more cores
  help?"

---

## 8. Real-time / low-latency .NET — the differentiator section

If they're doing market data or an OMS, these points make you sound like you've been there:

1. **GC pauses are the enemy.** Reduce allocation in the hot path rather than tuning the GC:
   structs, `Span<T>`, `ArrayPool<T>`, object pooling, pre-sized collections, no LINQ/closures in the
   tick handler, no string concatenation in logging (use structured logging with `{Placeholders}` and
   check `IsEnabled` first).
2. **Object pooling**: `ObjectPool<T>` (Microsoft.Extensions.ObjectPool) or `ArrayPool<T>.Shared` for
   buffers, so per-message allocations don't hit gen 0 at 50k/sec.
3. **Ring buffers / LMAX Disruptor pattern** — a pre-allocated circular array with sequence numbers,
   no locks, single-writer principle, mechanical sympathy for CPU caches. Name-dropping LMAX in a
   capital-markets interview is a genuine signal.
4. **Single-writer principle** — if only one thread ever writes a piece of state, most locking
   disappears. Partition work by instrument/symbol so each partition is single-threaded, then you get
   parallelism *without* shared mutable state. **This is the best architectural answer to
   "how do you make a tick processor both fast and correct?"**
5. **Latency is measured in percentiles, never averages.** Talk about p50/p99/p99.9 and
   *tail latency*. Coordinated omission if you want to go further (mention `HdrHistogram`).
6. **Warm-up / JIT**: first calls are slow (JIT, cold caches). Pre-JIT hot paths, or use ReadyToRun /
   Native AOT where applicable.
7. **Thread affinity / core pinning** for feed handlers in extreme cases; server GC on, tiered
   compilation considerations.
8. **Batching and coalescing**: don't process every tick individually to the UI — conflate to the
   latest per instrument and flush on a timer (see `05` §8 — this is the same problem WPF-side).

---

## 9. Code you should be able to write on the spot

### 9.1 Thread-safe singleton
```csharp
public sealed class Cache
{
    private static readonly Lazy<Cache> _instance = new(() => new Cache(), LazyThreadSafetyMode.ExecutionAndPublication);
    public static Cache Instance => _instance.Value;
    private Cache() { }
}
// Also know: static-readonly-field version (CLR guarantees thread-safe static init),
// and be able to explain why double-checked locking needs a volatile field.
```

### 9.2 Bounded blocking queue (classic whiteboard problem)
```csharp
public class BoundedQueue<T>
{
    private readonly Queue<T> _q = new();
    private readonly int _capacity;
    private readonly object _gate = new();
    public BoundedQueue(int capacity) => _capacity = capacity;

    public void Enqueue(T item)
    {
        lock (_gate)
        {
            while (_q.Count == _capacity) Monitor.Wait(_gate);   // release lock, wait
            _q.Enqueue(item);
            Monitor.PulseAll(_gate);                             // wake consumers
        }
    }
    public T Dequeue()
    {
        lock (_gate)
        {
            while (_q.Count == 0) Monitor.Wait(_gate);
            var item = _q.Dequeue();
            Monitor.PulseAll(_gate);
            return item;
        }
    }
}
```
⚠️ Two things they check: **`while`, not `if`** (spurious wakeups / lost races), and `PulseAll` vs
`Pulse`. Then say: *"in production I'd just use `Channel<T>` or `BlockingCollection<T>`."*

### 9.3 Async throttle / rate limiter
```csharp
private readonly SemaphoreSlim _limiter = new(maxConcurrency);
async Task<T> RunAsync<T>(Func<Task<T>> work)
{
    await _limiter.WaitAsync(ct);
    try { return await work(); }
    finally { _limiter.Release(); }
}
```

### 9.4 Fix this race (they may show you buggy code)
```csharp
// BUG: check-then-act is not atomic
if (!_dict.ContainsKey(k)) _dict.Add(k, Create(k));
// FIX
_dict.GetOrAdd(k, static key => Create(key));      // ConcurrentDictionary
```

---

## 10. Your honest positioning on this topic

Your CV's concurrency evidence is **distributed** (Kafka, consumer groups, Redis Streams, SignalR),
not **in-process low-level threading**. Bridge them explicitly — this framing is true and strong:

> *"Most of my concurrency work has been at the distributed level — 200,000 events a day through
> Kafka with consumer-group partitioning, ordering guarantees per key, idempotent consumers, and
> backpressure. The principles carry down to in-process: partition so each worker owns its state,
> single-writer where you can, bounded buffers with an explicit policy for what happens when they
> fill. In-process I use `async/await` and `Channel<T>` day to day, `Interlocked` and `SemaphoreSlim`
> where I need them, and I'm deliberate about not allocating in hot paths."*

Then, if pressed on depth, be honest: *"I've not written a lock-free ring buffer in anger — I've read
the Disruptor design and understand the mechanics, but I'd not claim production experience of it."*

---

## 11. Rapid-fire (answer in one line each)

1. Process vs thread → isolated address space vs shared memory within a process.
2. Context switch cost → ~1–10 µs, plus cache pollution.
3. `Thread.Sleep(0)` vs `Thread.Yield()` vs `Thread.Sleep(1)` → yield to same-priority ready thread /
   any thread on same core / actual timed sleep (~15 ms granularity by default).
4. Foreground vs background thread → keeps process alive vs doesn't.
5. `lock` reentrancy → yes for `Monitor`, no for `SemaphoreSlim`.
6. Atomic types in .NET → reads/writes of ≤ pointer-size are atomic; `long`/`double` are **not**
   guaranteed atomic on 32-bit.
7. Memory barrier → prevents reordering; `Volatile.Read/Write`, `Thread.MemoryBarrier()`.
8. `ThreadLocal<T>` / `[ThreadStatic]` → per-thread state; `AsyncLocal<T>` for flowing state across
   `await` (how correlation IDs travel).
9. Immutable data → the cheapest concurrency strategy; no synchronisation needed.
10. `CancellationTokenSource.CreateLinkedTokenSource` → combine caller cancellation with a timeout.
11. `Task.Delay` vs `Thread.Sleep` → non-blocking vs blocks the thread.
12. `TaskScheduler` → decides *where* continuations run; WPF's is the dispatcher-backed one.
13. Reader-writer vs lock → only worth it when reads massively dominate and the critical section is
    non-trivial; otherwise plain `lock` is faster.
14. Idempotency → the distributed-systems answer to at-least-once delivery.
15. How do you test concurrent code → stress/soak tests with many iterations, deterministic unit tests
    around the state machine, `Interlocked` counters to assert invariants, run under load with
    thread-count variation, and code review for lock ordering. **Say honestly: concurrency bugs are
    found by design discipline more than by tests.**
