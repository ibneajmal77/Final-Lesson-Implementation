# 12 — PERFORMANCE & PROFILING, IN PLAIN ENGLISH

> Listed as a nice-to-have. But in a real-time financial system it's effectively a must-have — and
> it's a **cheap differentiator**, because most candidates wave their hands here and you don't have to.

---

# EASY MEMORY NOTES

Read this first. Start with the short phrase. Say the simple line. Add the last column only if they
ask for more.

| Remember | Say it simply | If they ask more |
|---|---|---|
| **Measure first** | Do not guess. Measure the real problem. | Set a target, profile, fix one thing, measure again. |
| **p99, not average** | Slow tail users matter more than the average. | Track p95, p99, and p99.9. |
| **Biggest cost first** | Improve the part that takes most time. | Amdahl's law: small parts cannot give big wins. |
| **Usually I/O or DB** | Most slow apps wait on database, network, or allocation. | Check N+1 queries and over-fetching early. |
| **Use real benchmarks** | Microbenchmarks need proper tooling. | Use BenchmarkDotNet, not a simple `Stopwatch` loop. |
| **Sample in production** | Use low-overhead profiling on live systems. | Use deeper profilers locally when needed. |
| **Less allocation** | Less allocation means less GC pressure. | Pool buffers and avoid allocations in hot paths. |
| **Queue means blocked** | A growing thread-pool queue often means blocking async code. | Look for `.Result` and `.Wait()`. |
| **Cache carefully** | Do not make wrong data faster. | Cache reference data more freely than live prices. |
| **Real load shape** | Test with traffic that looks like real traffic. | Market open can spike much harder than normal time. |

---

# PART 0 — THE 8 ANSWERS THAT WIN

| # | The question | Simple answer |
|---|---|---|
| 1 | **How do you approach performance?** | "Measure first, fix one thing, then measure again." |
| 2 | **Where is it usually?** | "Usually I/O, database calls, allocation, or N+1 queries." |
| 3 | **How do you measure latency?** | "Use percentiles like p99, not only average." |
| 4 | **Do you optimise early?** | "I design for known performance needs, but I do not guess at micro-optimisations." |
| 5 | **Low-latency .NET** | "Reduce allocations before tuning the GC." |
| 6 | **Throughput collapsed under load** | "Look for blocked thread-pool work or blocking async code." |
| 7 | **Amdahl's law** | "Improve the part that takes most of the time." |
| 8 | **Benchmarking** | "Use BenchmarkDotNet for small benchmarks, not a simple `Stopwatch` loop." |

---

# PART 1 — THE METHOD (say this before any specific technique)

> *"I don't optimise from intuition. I define the target — a p99 latency or a throughput number tied
> to a real business need — then I measure the actual workload with a profiler, find the dominant
> cost, **fix one thing**, and re-measure.*
>
> *Most of the time the bottleneck isn't where anyone guessed, and it's usually **I/O, allocation, or
> an N+1** — not the algorithm."*

## The order I check things — say it as a checklist, it reads as experience

1. **Is it actually slow, and for whom?** p50 versus p99 — averages hide everything.
2. **Where does the time go?** Network, database, CPU, garbage collection, lock contention, or UI
   render — those are five completely different investigations.
3. **Are we fetching more than we need?** ⚠️ *The single biggest win in enterprise apps.*
4. **N+1 queries or chatty calls.**
5. **A missing or wrong index; an index-unfriendly filter.**
6. **Allocation rate and GC pressure.**
7. **Lock contention and blocked thread-pool work.**
8. **Only then** — algorithmic complexity and micro-optimisation.

**Amdahl's law:** *"If I make 20% of the runtime infinitely fast, I've saved 20%. So attack the
dominant term, not the interesting one."*

---

# PART 2 — THE .NET TOOLBOX

| Tool | What it's for |
|---|---|
| **BenchmarkDotNet** | Micro-benchmarks done **correctly** — warm-up, many iterations, statistics, and `[MemoryDiagnoser]` for allocations |
| **dotnet-counters** | Live counters: GC collections, allocation rate, exceptions/sec, **ThreadPool queue length**, lock contention |
| **dotnet-trace** / PerfView | CPU sampling, GC and JIT events |
| **dotnet-gcdump / dotnet-dump** | Heap analysis — "who is holding this object?" |
| **Visual Studio Diagnostic Tools** | CPU, allocation, and the **WPF UI responsiveness profiler** |
| **dotMemory / dotTrace** | Best-in-class memory and timeline profiling |
| **Application Insights / OpenTelemetry** | Production tracing — where time goes *across* services |
| **k6 / JMeter / Azure Load Testing** | Load and soak testing |

⚠️ **Say this — it's a real distinction:**
*"**Sampling** profilers have low overhead and are safe to attach in production, but they can miss
short calls. **Instrumenting** profilers are precise but distort the timings they're measuring. So I
sample in production and instrument locally."*

```csharp
[MemoryDiagnoser]
public class ParseBench
{
    private readonly string _msg = "8=FIX.4.2|35=D|55=AAPL|38=1000|44=182.35|";

    [Benchmark(Baseline = true)]
    public decimal Split() => decimal.Parse(_msg.Split('|')[4].Split('=')[1]);

    [Benchmark]
    public decimal Span()                       // zero-allocation version
    {
        ReadOnlySpan<char> s = _msg.AsSpan();
        int i = s.IndexOf("44=".AsSpan()) + 3;
        int end = s[i..].IndexOf('|');
        return decimal.Parse(s.Slice(i, end));
    }
}
```

---

# PART 3 — SYMPTOM → CAUSE → FIX

**Learn this table. It turns "how would you debug it?" into a confident, structured answer.**

| Symptom | Likely cause | Fix |
|---|---|---|
| High gen-0 rate, sawtooth memory | Allocating in a hot loop | Structs, `Span<T>`, `ArrayPool`, pooling. **Remove LINQ and closures from the hot path** |
| Out of memory with free memory available | **LOH fragmentation** (objects ≥ 85 KB) | Pool large buffers; LOH compaction only as a last resort |
| Latency spikes every few seconds | Full GC pauses | Reduce allocation; background GC; find what's surviving to gen 2 |
| **Throughput collapses under load, queue length high** | **Thread-pool starvation** from blocking on async | Async all the way. **Never `.Result` or `.Wait()`.** Raising `MinThreads` is a stopgap, not a fix |
| CPU high but little work done | Lock contention, spinning, false sharing | Shorter critical sections, partition state, `Interlocked`, pad hot fields |
| Slow first request only | JIT and cold caches | A warm-up path, ReadyToRun or AOT |
| Database time dominates | N+1, missing index, over-fetching | Projection, `AsNoTracking`, a covering index, batching |
| Chatty service calls | One remote call per item | Batch endpoints, caching, a denormalised read model |
| Memory grows forever | **Event handler or static cache retention** | Unsubscribe, bound the cache, weak references |

## Caching vocabulary

Cache-aside (the common one), read-through, write-through, write-behind. Invalidation by TTL, by
event, or by versioned key. **Stampede protection** — single-flight, or jittered TTLs so a thousand
keys don't expire at the same instant.

⚠️ **The honest caveat that lands well:**
*"Cache invalidation is where the bugs live. So in a financial system I'd cache **reference data**
aggressively and **prices never**."*

---

# PART 4 — WPF AND DESKTOP PERFORMANCE

*(See `05` Part 7 for the full answer.)*

- ⚠️ **Binding errors are silent and expensive.** Each one is an exception plus a tree walk. Check the
  Output window; turn up `PresentationTraceSources`.
- Virtualisation on, **recycling mode**, and never a `StackPanel` as the items panel.
- `Freeze()` brushes and geometries. Keep the visual tree shallow.
- **Batch and conflate updates. Never touch the UI per message.**
- Measure with the VS **UI responsiveness** profiler — look at frame time, layout and render passes,
  and time spent sitting in the dispatcher queue.
- **Perceived** performance counts: do work at `DispatcherPriority.Background` so input stays
  responsive, and show a loading state rather than a frozen window.

---

# PART 5 — PYTHON PERFORMANCE

*(See `06` Part 10.)*

**Tools:** `cProfile` for functions, `line_profiler` for lines, `tracemalloc` for memory, and
**`py-spy`** — *"sampling, and it attaches to a running process without a restart, which is the one
that matters in production."*

**Fixes, in order:** vectorise with NumPy or Pandas · never `iterrows` · categorical dtypes · Parquet
over CSV · Numba or Cython for a genuinely hot numeric loop · processes for CPU work, because of the
GIL.

---

# PART 6 — LOAD AND RESILIENCE TESTING

**The five kinds — name them:**
- **Load** — the expected traffic.
- **Stress** — push until it breaks, so you know where the edge is.
- **Soak / endurance** — hours, to expose memory leaks and resource exhaustion.
- **Spike** — a sudden burst. ⚠️ ***In this domain that's market open.***
- **Capacity planning** — what do we need for next year.

**Say:** *"And I'd model a realistic workload. Market open and close are not uniform traffic — a load
test that sends a steady rate proves nothing about the moment that actually breaks you."*

**Watch the saturation signals, not just latency:** queue depth, thread-pool queue length, connection
pool exhaustion, database wait stats. ⚠️ *"Those predict failure before latency does."*

**Also mention:** percentiles not averages, and **coordinated omission** in your load tool — *"if the
tool waits for a slow response before sending the next request, it under-reports exactly the latency
you care about."*

**Chaos:** kill a dependency, add latency, drop the feed. ⚠️ *"And verify the UI clearly shows stale
data rather than silently lying — in a trading app that's a correctness requirement, not a nicety."*

---

# PART 7 — THREE ANSWERS TO HAVE READY WORD-FOR-WORD

**Q: "A report takes 60 seconds. What do you do?"**
> *"First I'd find out whether it's the query, the transfer, or the rendering — those are three
> different problems and people usually assume the first.*
>
> *Assuming it's the query: capture the **actual** execution plan, look for scans on large tables, key
> lookups, and estimate-versus-actual row errors. Usually it's a missing covering index or a
> index-unfriendly filter — for example, a function wrapped around a date column.*
>
> *If the query is genuinely heavy, I'd ask whether it belongs on the OLTP store at all — a
> pre-aggregated read model, an indexed view, or a columnar store for the analytics side. And I'd ask
> whether the user actually needs 100,000 rows on screen, because paging or aggregating is often the
> real fix."*

**Q: "A user says the app is slow."**
> *"Get specifics first: which screen, what data, how often, is it everyone or one user, and when did
> it start. Then reproduce it with their data volume. Then measure. **'Slow' with no measurement is
> where teams waste weeks.**"*

**Q: "Do you optimise early?"**
> *"I design for the known non-functional requirements from the start — data volumes, latency targets,
> access patterns — because those are architectural and expensive to retrofit. But I don't
> micro-optimise code before measuring. **Choosing the right data structure and the right storage is
> design; shaving nanoseconds is optimisation.**"*

⚠️ **That last answer threads the needle perfectly** — it avoids both the tired "premature
optimisation" cliché and reckless hand-waving. Learn it.
