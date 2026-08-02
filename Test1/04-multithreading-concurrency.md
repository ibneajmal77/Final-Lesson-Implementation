# 04 — MULTITHREADING & REAL-TIME, IN PLAIN ENGLISH

> The job says **"real-time and multithreaded systems expertise"** as a must-have.
> In a capital-markets team this is *the* round that separates candidates. Expect **15–20 minutes**
> on this alone.
>
> **Format:** **Q:** what they ask → **Say:** the words you speak → **Remember:** the hook.

---

# FULL TECH LOAD MEMORY HOOKS

Use these as labels for the full detail below. Say the hook first, then expand only where the
interviewer pushes.

| Hook | Simple wording | Full tech load to keep |
|---|---|---|
| **Waiting is not working** | I/O uses async; CPU uses threads. | `async/await` for network/disk/db waits; thread pool, `Parallel`, PLINQ or dedicated threads for compute. |
| **Await returns** | `await` does not block a thread. | Compiler state machine, continuation, synchronization context, UI resume rules. |
| **UI deadlock loop** | Blocking the UI blocks the continuation. | `.Result`/`.Wait()` on WPF thread plus captured context; fix with async all the way or library `ConfigureAwait(false)`. |
| **Volatile is visibility** | It is not atomic. | Prevents reordering/stale reads; `Interlocked` for read-modify-write and compare-and-swap. |
| **Lock order wins** | Deadlock prevention is mostly order. | Coffman conditions, break circular wait, timeouts, smaller lock scope. |
| **Bounded means backpressure** | A full queue is a signal, not a surprise. | `System.Threading.Channels`, bounded capacity, drop policy, producer/consumer cancellation. |
| **Single writer** | One owner per piece of state. | Partition by instrument/account to avoid shared mutable state and reduce locking. |
| **Conflate the grid** | Latest value matters more than every tick. | Latest per instrument, batch, flush on timer, equality guard, virtualized UI. |
| **p99 beats average** | Tail latency is what hurts. | Measure p50/p99/p99.9, coordinated omission, load shape, market-open spikes. |

---

# PART 0 — THE 10 CONCURRENCY ANSWERS THAT WIN

| # | The question | The answer, in one breath |
|---|---|---|
| 1 | **The framing (say this first, always)** | "**Waiting is not working.** If I'm waiting on network or disk, that's `async/await`. If I have real computation to spread across cores, that's threads or `Parallel`. Using async for CPU work buys nothing; using threads for waiting wastes a megabyte of stack each." |
| 2 | **What does `await` actually do?** | "The compiler turns the method into a state machine. At an `await` the method returns to its caller and the rest is registered as a continuation. **No thread is blocked while waiting.**" |
| 3 | **The classic deadlock** | "`.Result` on the UI thread. The UI thread blocks; the continuation needs the UI thread; neither can move. Fix: async all the way up, or `ConfigureAwait(false)` in the library." |
| 4 | **`volatile`** | "It stops reordering and forces a read from memory. It does **not** make anything atomic. `x++` on a volatile field is still a race — that needs `Interlocked`." |
| 5 | **Preventing deadlock** | "**Consistent lock ordering.** That's the practical answer — you break the circular-wait condition." |
| 6 | **Producer/consumer in .NET today** | "`System.Threading.Channels`, bounded. A bounded channel *is* backpressure." |
| 7 | **10,000 ticks a second into a grid** | "Don't touch the UI per tick. Conflate to the latest per instrument, batch, and flush on a timer." |
| 8 | **The best architectural answer** | "**Single-writer principle.** Partition by instrument so each partition is owned by one thread. You get parallelism without shared mutable state, and most locking disappears." |
| 9 | **Latency** | "Percentiles, never averages. p50, p99, p99.9. An average hides exactly the tail that hurts you." |
| 10 | **Low-latency .NET** | "**Reduce allocation, don't tune the GC.** Structs, `Span<T>`, `ArrayPool`, object pooling, no LINQ or closures in the tick handler." |

---

# PART 1 — THE FRAME TO SET UP FRONT

**Say this once, early, and it correctly frames every question that follows:**

> *"There are two different problems people both call concurrency.*
>
> *One is **waiting** — you're blocked on a network, a disk or a database. The right tool is
> `async/await`, which frees the thread while you wait.*
>
> *The other is **working** — you have real computation to parallelise. The right tool is the thread
> pool, `Parallel`, PLINQ, or a dedicated thread.*
>
> *Using async for CPU work buys you nothing. Using threads for waiting wastes about a megabyte of
> stack each and kills scalability."*

**Remember:** **Waiting → async. Working → threads.**

---

# PART 2 — THREAD vs THREADPOOL vs TASK

| | `Thread` | `ThreadPool` | `Task` |
|---|---|---|---|
| Cost | ~1 MB stack, expensive to create | Reused, pre-warmed | An abstraction *over* the pool |
| Control | Priority, foreground/background, name | Little | Rich: continuations, cancellation, exceptions, results |
| Use when | Long-running and dedicated — **a market-data receive thread** | Short work items | **Almost always** |

**Three facts worth knowing:**

1. **Threads are foreground by default** and keep the process alive. Thread-pool threads are
   background.
2. **The pool grows slowly** past its minimum — roughly **one new thread per 500 ms**. That causes
   **thread pool starvation**: block pool threads on I/O and latency collapses because replacements
   arrive at a crawl. **Naming this earns senior credit.**
3. **`Task.Run` over `Task.Factory.StartNew`.** `StartNew` with an async delegate returns
   `Task<Task>` and needs `.Unwrap()` — a classic bug. Use `StartNew` only for
   `TaskCreationOptions.LongRunning`, which gives you a dedicated thread rather than a pool thread.

```csharp
// A dedicated, long-lived feed handler — a legitimate use of a raw Thread
var t = new Thread(ReceiveLoop) {
    IsBackground = true, Priority = ThreadPriority.AboveNormal, Name = "MarketDataRx"
};
t.Start();
```

---

# PART 3 — async/await

## 3.1 What `await` actually does

**Say:** *"The compiler rewrites the method into a state machine. When it hits an `await` on something
that isn't finished, the method **returns to its caller** and the rest of the method is registered as
a continuation on that task. When the task completes, the continuation is scheduled — back onto the
captured synchronization context if there is one, otherwise onto the thread pool. **No thread is
blocked while waiting.** That's the whole point."*

## 3.2 `ConfigureAwait(false)`

**Say:** *"It tells the awaiter not to marshal the continuation back to the captured context.
In **library** code you want it — it avoids an unnecessary context switch and it prevents deadlocks.
In **WPF or UI** code you generally *do* want the context, so you can touch the UI after the await.
ASP.NET Core has no synchronization context, so there it doesn't matter."*

## 3.3 The classic async deadlock — very likely in a desktop shop

```csharp
private void Button_Click(object s, RoutedEventArgs e)
{
    var data = LoadAsync().Result;        // ← blocks the UI thread
}
private async Task<string> LoadAsync()
{
    await _http.GetStringAsync(url);      // captures the UI synchronization context
    return "done";                        // ← this continuation needs the UI thread… which is blocked
}
```

**Say:** *"The UI thread is blocked inside `.Result`. The continuation is queued to run on the UI
thread. Neither can proceed — that's the deadlock. Two fixes: `await` all the way up, or
`ConfigureAwait(false)` inside the library method. **The rule is: never call `.Result` or `.Wait()`
on a UI thread.**"*

**Remember:** **Block the thread the continuation needs, and you deadlock.**

## 3.4 `async void`

**Say:** *"Only for event handlers, because the signature is fixed. Otherwise it's poison — you can't
await it, you can't catch its exceptions (they're raised on the sync context and usually take the
process down), and you can't compose it. Even in an event handler I wrap the body in a try/catch."*

## 3.5 Everything else, ready to go

- `Task.WhenAll` for fan-out. `Task.WhenAny` for first-wins or a timeout.
- **Thread a `CancellationToken` through every async API you write.** Non-negotiable at senior level.
- `IAsyncEnumerable<T>` + `await foreach` for streaming results — a tick stream, for example.
- `TaskCompletionSource<T>` bridges callback or event-based APIs into tasks. Use
  `RunContinuationsAsynchronously` so continuations don't run inline on your I/O thread.
- **Async is not parallelism.** `await a; await b;` is sequential. `await Task.WhenAll(a, b)` is
  concurrent. *(Same distinction as `Promise.all` in JS — see `17` §1.7.)*

---

# PART 4 — LOCKS: PICK THE RIGHT ONE

| Primitive | Scope | Cost | Use it for |
|---|---|---|---|
| `lock` / `Monitor` | In-process | Cheap uncontended (~20 ns) | The default |
| `Interlocked` | In-process | Cheapest — one CPU instruction | Counters, compare-and-swap |
| `SemaphoreSlim` | In-process, has `WaitAsync` | Cheap | Throttling, and **the only async-friendly lock** |
| `Mutex` | **Cross-process**, named | Expensive (kernel) | Enforcing a single app instance |
| `ReaderWriterLockSlim` | In-process | Moderate | Many readers, rare writer |
| `SpinLock` | In-process | Burns CPU | Only extremely short, uncontended sections |
| `ManualResetEventSlim` | Signalling | — | Wait for a signal |

## 4.1 The rules

- `lock(x)` is `Monitor.Enter/Exit` in a try/finally. **It is reentrant** for the same thread.
- ⚠️ **Never lock on:** `this`, a `Type`, or a **`string`** (interned, so it's shared globally — any
  other code can lock the same object and deadlock you). Always a dedicated
  `private readonly object _gate = new();`
- ⚠️ **You cannot `await` inside a `lock`.** The compiler forbids it, because `Monitor` has thread
  affinity — the thread that releases must be the thread that acquired. Use `SemaphoreSlim`:

```csharp
private readonly SemaphoreSlim _gate = new(1, 1);

async Task UpdateAsync(CancellationToken ct)
{
    await _gate.WaitAsync(ct);
    try { await DoWorkAsync(ct); }
    finally { _gate.Release(); }        // ALWAYS release in finally
}
```

## 4.2 `volatile` vs `Interlocked`

**Q: What does `volatile` actually guarantee?**
**Say:** *"It stops the compiler, JIT and CPU reordering reads and writes around that field, and it
forces a read from memory rather than a register. **It does not make anything atomic.**
`volatile int x; x++;` is still a race, because that's a read, a modify and a write. For that I need
`Interlocked.Increment`."*

**Remember:** **`volatile` = visibility. `Interlocked` = atomicity. They are not the same.**

```csharp
Interlocked.Increment(ref _messageCount);
Interlocked.Exchange(ref _latestPrice, newPrice);

// Compare-and-swap — the basis of every lock-free algorithm
long original, updated;
do {
    original = _max;
    updated  = Math.Max(original, candidate);
} while (Interlocked.CompareExchange(ref _max, updated, original) != original);
```

---

# PART 5 — THE FAILURE MODES

Define each crisply. They may just ask you to define them.

| Problem | Definition | Prevention |
|---|---|---|
| **Race condition** | The result depends on the timing of unsynchronised access | Lock, atomic operations, or immutability |
| **Deadlock** | Two threads each hold a lock the other needs. Forever | **Consistent lock ordering** (the main answer), lock timeouts, smaller lock scope, no nested locks |
| **Livelock** | Threads are busy but making no progress — endlessly retrying and backing off | Randomised backoff |
| **Starvation** | One thread never gets the resource | Fair locks, don't abuse priorities |
| **Priority inversion** | A low-priority thread holds a lock a high-priority thread needs | Priority inheritance; avoid mixing priorities |
| **Torn read** | A non-atomic read of something bigger than a word sees half old, half new | `Interlocked.Read`, a lock, or make it a reference to an immutable object |
| **False sharing** | Two hot variables share a 64-byte cache line, so cores keep invalidating each other | Pad to cache-line size |
| **Thread pool starvation** | Blocking calls eat pool threads faster than replacements are injected | Never block on async. Async all the way |

**The four Coffman conditions for deadlock:** mutual exclusion, hold-and-wait, no preemption, and
**circular wait**. Quote them, then say: *"In practice we break circular wait with a global lock
ordering."* That's a strong, complete answer.

---

# PART 6 — CONCURRENT COLLECTIONS & PRODUCER/CONSUMER

| Type | Use it for |
|---|---|
| `ConcurrentDictionary<K,V>` | Thread-safe map. ⚠️ `GetOrAdd`'s factory **can run more than once** — keep it cheap and idempotent, or store a `Lazy<T>` |
| `ConcurrentQueue/Stack/Bag<T>` | Lock-free-ish collections |
| `BlockingCollection<T>` | Classic bounded producer/consumer, blocking API |
| **`System.Threading.Channels`** | **The modern async producer/consumer — the answer to give** |
| `ImmutableList` / `ImmutableDictionary` | Snapshot semantics; readers never lock |

## 6.1 Channels — learn this, it maps straight onto market data

```csharp
var channel = Channel.CreateBounded<Tick>(new BoundedChannelOptions(10_000)
{
    FullMode = BoundedChannelFullMode.DropOldest,   // for prices, newest wins
    SingleReader = true,
    SingleWriter = false
});

// Producer — the feed handler thread
await channel.Writer.WriteAsync(tick, ct);

// Consumer
await foreach (var tick in channel.Reader.ReadAllAsync(ct))
    ProcessTick(tick);
```

⚠️ **Say this out loud. It's the single best answer to "how would you handle a high-frequency feed?":**

> *"A bounded channel with a drop-oldest policy. For prices, backpressure that blocks the producer is
> the wrong answer — I can't slow the exchange down, and a stale price is worthless anyway. So I bound
> the buffer and drop stale ticks, keeping the latest per instrument.*
>
> *For **orders** I'd do the exact opposite: never drop, apply real backpressure, and persist —
> because every order message matters."*

**Why that answer works:** it shows you understand that **the domain drives the concurrency policy**.
That's exactly what a capital-markets interviewer is listening for.

**Remember:** **Prices: drop oldest. Orders: never drop.**

---

# PART 7 — PARALLELISM FOR CPU WORK

```csharp
Parallel.For(0, n, i => Compute(i));
Parallel.ForEach(items, new ParallelOptions { MaxDegreeOfParallelism = 8 }, Process);
await Parallel.ForEachAsync(items, ct, async (x, t) => await ProcessAsync(x, t));   // .NET 6+
var results = source.AsParallel().WithDegreeOfParallelism(4).Where(...).ToArray();  // PLINQ
```

**Four things to say:**
- ⚠️ **`Parallel` is *slower* for small workloads** — partitioning and coordination cost more than the
  work.
- **Aggregation must be thread-safe.** Use the `localInit`/`localFinally` overload, or `Interlocked` —
  never a shared `sum += x`.
- Exceptions surface as an `AggregateException`.
- **Amdahl's law** — speedup is capped by the serial fraction. Worth quoting if they ask
  *"will more cores help?"*

---

# PART 8 — REAL-TIME .NET (the differentiator section)

If they're doing market data or an OMS, these points make you sound like you've been there.

1. **GC pauses are the enemy — reduce allocation, don't tune the GC.**
   Structs, `Span<T>`, `ArrayPool<T>`, object pooling, pre-sized collections, no LINQ or closures in
   the tick handler, no string concatenation in logging (structured logging with `{Placeholders}`, and
   check `IsEnabled` first).

2. **Object pooling.** `ObjectPool<T>` or `ArrayPool<T>.Shared` for buffers, so per-message
   allocations don't hammer gen 0 at 50,000 a second.

3. **Ring buffers / the LMAX Disruptor pattern.** A pre-allocated circular array with sequence
   numbers, no locks, single writer, designed around CPU cache behaviour.
   **Naming LMAX in a capital-markets interview is a genuine signal.**

4. **The single-writer principle — the best architectural answer here.**
   **Say:** *"If only one thread ever writes a piece of state, most locking disappears. So I partition
   by instrument or account, and each partition is single-threaded. That gives me parallelism across
   partitions **without shared mutable state**. It's the same idea as Kafka partitioning by key, which
   is where I've applied it at scale."*

5. **Latency is percentiles, never averages.** p50, p99, p99.9, and talk about **tail latency**.
   Mention `HdrHistogram` and coordinated omission if you want to go a level deeper.

6. **Warm-up.** First calls are slow — JIT and cold caches. Pre-JIT the hot path, or use
   ReadyToRun / Native AOT.

7. **Batching and coalescing.** Don't push every tick to the UI. Conflate to the latest per instrument
   and flush on a timer. *(This is the same problem as `05` §7 — the WPF side of the same coin.)*

---

# PART 9 — CODE TO BE ABLE TO WRITE ON THE SPOT

### 9.1 Thread-safe singleton
```csharp
public sealed class Cache
{
    private static readonly Lazy<Cache> _instance =
        new(() => new Cache(), LazyThreadSafetyMode.ExecutionAndPublication);
    public static Cache Instance => _instance.Value;
    private Cache() { }
}
```
**Also know:** the plain `static readonly` field version works too, because the CLR guarantees
thread-safe static initialisation. And be ready to explain **why double-checked locking needs a
`volatile` field** — without it, the reference can be published before the constructor finishes.

### 9.2 Bounded blocking queue (the classic whiteboard problem)
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
            while (_q.Count == _capacity) Monitor.Wait(_gate);   // release the lock and wait
            _q.Enqueue(item);
            Monitor.PulseAll(_gate);                             // wake the consumers
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
⚠️ **Two things they're checking:** **`while`, not `if`** (spurious wakeups and lost races), and
`PulseAll` versus `Pulse`. Then say: *"In production I'd just use `Channel<T>` or
`BlockingCollection<T>` — but it's worth knowing what's underneath."*

### 9.3 Async throttle
```csharp
private readonly SemaphoreSlim _limiter = new(maxConcurrency);

async Task<T> RunAsync<T>(Func<Task<T>> work, CancellationToken ct)
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

# PART 10 — YOUR HONEST POSITIONING

Your concurrency evidence is **distributed** (Kafka, consumer groups, Redis Streams, SignalR), not
**in-process low-level threading**. Bridge them explicitly. This framing is true and it's strong:

> *"Most of my concurrency work has been at the distributed level — 200,000 events a day through
> Kafka, with consumer-group partitioning, ordering guarantees per key, idempotent consumers and
> backpressure. The principles carry straight down to in-process: partition so each worker owns its
> state, single-writer wherever you can, and bounded buffers with an explicit policy for what happens
> when they fill.*
>
> *In-process I use `async/await` and `Channel<T>` day to day, `Interlocked` and `SemaphoreSlim` where
> I need them, and I'm deliberate about not allocating in hot paths."*

**If pressed on depth, be honest:** *"I haven't written a lock-free ring buffer in anger. I've read
the Disruptor design and I understand the mechanics, but I wouldn't claim production experience of
it."*

**That honesty reduces their risk. A bluff increases it — and the client round will find it.**

---

# PART 11 — RAPID-FIRE: 45 QUESTIONS

| # | Q | A |
|---|---|---|
| 1 | Process vs thread | Isolated address space vs shared memory inside one process |
| 2 | Context switch cost | Roughly 1–10 microseconds, plus cache pollution |
| 3 | Foreground vs background thread | Keeps the process alive vs doesn't |
| 4 | `Thread.Sleep(0)` vs `Yield()` | Yield to a same-priority ready thread vs any thread on the same core |
| 5 | `Task.Delay` vs `Thread.Sleep` | Non-blocking vs blocks the thread |
| 6 | Thread vs Task | An OS thread vs a unit of work scheduled on the pool |
| 7 | Thread pool injection rate | About one new thread per 500 ms past the minimum |
| 8 | Thread pool starvation | Blocking pool threads on I/O; replacements arrive too slowly |
| 9 | `Task.Run` vs `StartNew` | Prefer `Run`; `StartNew` with async returns `Task<Task>` |
| 10 | `LongRunning` | Gives a dedicated thread instead of a pool thread |
| 11 | What does `await` do? | State machine; returns to the caller; the rest becomes a continuation |
| 12 | Does `await` block a thread? | **No** — that's the entire point |
| 13 | `ConfigureAwait(false)` | Don't marshal back to the captured context. Use in libraries |
| 14 | The async deadlock | `.Result` on the UI thread + a continuation needing that thread |
| 15 | `async void` | Event handlers only — otherwise unawaitable and uncatchable |
| 16 | `Task.WhenAll` vs `WhenAny` | All complete vs the first one |
| 17 | Is async parallelism? | No. `await a; await b;` is sequential |
| 18 | `IAsyncEnumerable` | Streaming async results — `await foreach` |
| 19 | `TaskCompletionSource` | Bridge a callback API into a Task |
| 20 | `CancellationToken` | Thread it through every async API you write |
| 21 | Linked cancellation | `CreateLinkedTokenSource` — combine caller cancellation with a timeout |
| 22 | `lock` reentrancy | Yes for `Monitor`. **No** for `SemaphoreSlim` |
| 23 | Never lock on | `this`, a `Type`, or a **string** (interned and globally shared) |
| 24 | Can you `await` inside a `lock`? | No — use `SemaphoreSlim.WaitAsync` |
| 25 | `volatile` guarantees | Ordering and visibility. **Not** atomicity |
| 26 | Atomic increment | `Interlocked.Increment` |
| 27 | Compare-and-swap | `Interlocked.CompareExchange` — the basis of lock-free code |
| 28 | Atomic in .NET | Reads/writes up to pointer size. `long`/`double` **not** guaranteed on 32-bit |
| 29 | Memory barrier | Prevents reordering — `Volatile.Read/Write`, `Thread.MemoryBarrier()` |
| 30 | Race condition | The result depends on unsynchronised timing |
| 31 | Deadlock, in one line | Each holds what the other needs |
| 32 | Preventing deadlock | **Consistent lock ordering** |
| 33 | Coffman conditions | Mutual exclusion, hold-and-wait, no preemption, circular wait |
| 34 | Livelock | Busy but not progressing |
| 35 | False sharing | Two hot variables in one cache line; cores invalidate each other |
| 36 | `ConcurrentDictionary.GetOrAdd` gotcha | The factory can run more than once |
| 37 | `Channel<T>` bounded | Backpressure, with an explicit full policy |
| 38 | Producer/consumer today | `System.Threading.Channels` |
| 39 | Market data backpressure | Drop oldest for prices; never drop for orders |
| 40 | Single-writer principle | Partition state so one thread owns it — locking disappears |
| 41 | `ThreadLocal` / `AsyncLocal` | Per-thread state vs state that flows across `await` (correlation IDs) |
| 42 | Immutable data | The cheapest concurrency strategy — no synchronisation at all |
| 43 | `Parallel.For` on small work | Slower — overhead exceeds the work |
| 44 | Latency measurement | Percentiles: p50, p99, p99.9. **Never averages** |
| 45 | How do you test concurrent code? | Stress and soak tests, deterministic unit tests around the state machine, `Interlocked` counters asserting invariants, and code review for lock ordering. **Be honest: concurrency bugs are found by design discipline more than by tests** |
