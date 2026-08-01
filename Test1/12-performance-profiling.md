# 12 — Performance, Profiling & Optimisation

> JD nice-to-have: *"performance testing and profiling"*. In a real-time financial system this is
> effectively a must-have. It's also a cheap differentiator — most candidates wave their hands here.

---

## 1. The method (say this before any specific technique)

> *"I don't optimise from intuition. I define the target — a p99 latency or a throughput number tied
> to a business need — then measure the real workload with a profiler, find the dominant cost, fix one
> thing, and re-measure. Most of the time the bottleneck isn't where anyone guessed, and it's usually
> I/O, allocation, or an N+1, not the algorithm."*

**The order I check things** (say it as a checklist — it reads as experience):
1. Is it actually slow, and for whom? p50 vs p99 — averages hide everything.
2. Where does the time go — network, database, CPU, GC, lock contention, UI render?
3. Data volume: are we fetching more than we need? (Biggest single win in enterprise apps.)
4. N+1 queries / chatty calls.
5. Missing or wrong index; non-SARGable predicate.
6. Allocation rate and GC pressure.
7. Lock contention and thread-pool starvation.
8. Only then: algorithmic complexity and micro-optimisation.

**Amdahl's law** — optimising 20% of the runtime caps your gain at 20%. Attack the dominant term.

---

## 2. .NET profiling toolbox

| Tool | Use |
|---|---|
| **BenchmarkDotNet** | Micro-benchmarks done *correctly* — warm-up, multiple iterations, statistics, `[MemoryDiagnoser]` for allocations. ⚠️ Never benchmark with `Stopwatch` in a loop and quote the number. |
| **dotnet-counters** | Live counters: GC gen counts, alloc rate, exceptions/sec, **ThreadPool queue length**, lock contention |
| **dotnet-trace** / PerfView | CPU sampling, ETW events, GC and JIT events |
| **dotnet-dump / dotnet-gcdump** | Heap analysis, retention paths, "who's holding this object" |
| **Visual Studio Diagnostic Tools** | CPU usage, allocation, and the **WPF-specific** UI responsiveness/rendering profiler |
| **dotMemory / dotTrace (JetBrains)** | Best-in-class memory and timeline profiling |
| **Application Insights / OpenTelemetry** | Production distributed tracing — where the time goes *across* services |
| **k6 / JMeter / Azure Load Testing** | Load and soak testing (your CV already lists these) |

**Sampling vs instrumenting profilers:** sampling has low overhead and is safe in production but can
miss short calls; instrumentation is precise but distorts timings and slows the app. Say which and why.

```csharp
[MemoryDiagnoser]
public class ParseBench
{
    private readonly string _msg = "8=FIX.4.2|35=D|55=AAPL|38=1000|44=182.35|";

    [Benchmark(Baseline = true)]
    public decimal Split() => decimal.Parse(_msg.Split('|')[4].Split('=')[1]);

    [Benchmark]
    public decimal Span()          // zero-allocation version
    {
        ReadOnlySpan<char> s = _msg.AsSpan();
        int i = s.IndexOf("44=".AsSpan()) + 3;
        int end = s[i..].IndexOf('|');
        return decimal.Parse(s.Slice(i, end));
    }
}
```

---

## 3. Common .NET performance problems and their fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| High gen-0 rate, sawtooth memory | Allocation in a hot loop | Structs, `Span<T>`, `ArrayPool`, object pooling, remove LINQ/closures from the hot path |
| Gen-2 / LOH growth, OOM with free memory | LOH fragmentation (objects ≥85 KB) | Pool large buffers, reduce large-array churn, `LargeObjectHeapCompactionMode` as a last resort |
| Latency spikes every few seconds | Full GC pauses | Reduce allocations; background GC; check for large object graphs surviving to gen 2 |
| Throughput collapses under load, high queue length | **Thread-pool starvation** from blocking on async | Async all the way; never `.Result`/`.Wait()`; raise `MinThreads` only as a stopgap |
| CPU high but little work done | Lock contention, spinning, false sharing | Reduce critical sections, partition state, `Interlocked`, pad hot fields |
| Slow first request | JIT + cold cache | Warm-up path, ReadyToRun/AOT, tiered PGO |
| Database time dominates | N+1, missing index, over-fetching | Projection, `AsNoTracking`, covering index, batching |
| Chatty service calls | Per-item remote calls | Batch endpoints, caching, denormalised read model |
| Memory grows forever | Event handler / static cache retention | Unsubscribe, bounded cache, weak references (`03` §2) |

**Caching strategy vocabulary:** cache-aside (most common), read-through, write-through,
write-behind; **invalidation** (TTL, event-driven, versioned keys); stampede protection
(single-flight/lock or jittered TTL); and the honest caveat — *"cache invalidation is where the bugs
live, so in a financial system I cache reference data aggressively and prices never."*

---

## 4. WPF/desktop performance (see also `05` §7–8)

- Binding errors are silent and expensive — check the Output window; `PresentationTraceSources`.
- Virtualisation on, recycling mode, no `StackPanel` as items panel.
- Freeze brushes/geometries; reduce visual tree depth; `BitmapCache` for complex static visuals.
- Batch and conflate updates; never touch the UI per message.
- Measure with the VS **UI responsiveness** profiler: look at frame time, layout/render passes, and
  time spent in the dispatcher queue.
- Perceived performance matters: virtualise + show a skeleton/loading state; do work at
  `DispatcherPriority.Background` so input stays responsive.

---

## 5. Python profiling (`06` cross-ref)
`cProfile` + `snakeviz` (function-level), `line_profiler` (line-level), `memory_profiler`/`tracemalloc`,
**`py-spy`** (sampling, attaches to a running process — the production tool), `timeit` for micro.
Fixes: vectorise with NumPy/Pandas, avoid `iterrows`/`apply`, use categorical dtypes, use Parquet,
move hot loops to NumPy/Numba/Cython, and parallelise CPU work across processes (GIL).

---

## 6. Load & resilience testing
- **Load** (expected), **stress** (find the breaking point), **soak/endurance** (memory leaks and
  resource exhaustion over hours), **spike** (sudden burst — market open!), **capacity planning**.
- Model realistic workloads: market open/close spikes are not uniform traffic.
- Measure **percentiles, not averages**; watch for **coordinated omission** in your load tool.
- Track saturation signals: queue depth, thread-pool queue length, connection pool exhaustion, DB
  wait stats — these predict failure before latency does.
- **Chaos**: kill a dependency, add latency, drop the feed — verify graceful degradation and that the
  UI clearly shows stale data rather than silently lying.

---

## 7. Answers to have ready

**"How would you approach a report that takes 60 seconds?"**
> *"First I'd check whether it's the query, the transfer, or the rendering — that's three different
> problems. Assuming the query: capture the actual execution plan, look for scans on large tables,
> key lookups, and estimate-vs-actual row errors. Usually it's a missing covering index or a
> non-SARGable predicate like a function wrapped around a date column. If the query is genuinely
> heavy, I'd ask whether it belongs on the OLTP store at all — a pre-aggregated read model,
> a materialised/indexed view, or a columnar store for the analytics side. And I'd check whether the
> user actually needs 100,000 rows in a grid, because paging or aggregating is often the real fix."*

**"A user says the app is slow. What do you do?"**
> *"Get specifics first: which screen, what data, how often, is it slow for everyone or one user, and
> when did it start. Then reproduce with their data volume. Then measure. 'Slow' with no measurement
> is where teams waste weeks."*

**"Do you optimise early?"**
> *"I design for the known non-functional requirements from the start — data volumes, latency targets,
> access patterns — because those are architectural and expensive to retrofit. But I don't
> micro-optimise code before measuring. Choosing the right data structure and the right storage is
> design; shaving nanoseconds is optimisation."* (This threads the needle perfectly — it's the answer
> that avoids both "premature optimisation is the root of all evil" cliché and reckless hand-waving.)
