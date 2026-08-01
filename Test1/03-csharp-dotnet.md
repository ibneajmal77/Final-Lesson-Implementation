# 03 — C# & .NET Internals (Deep)

> Format: **Q** → tight answer → `code` → ⚠️ the gotcha they follow up with.
> If you can answer everything here you are above the bar for a senior .NET interview.

---

## 1. Memory model: stack, heap, value vs reference

**Q: Difference between value types and reference types?**

- **Value types** (`struct`, `int`, `bool`, `enum`, `decimal`, `DateTime`, tuples): hold data
  directly, copied on assignment, live wherever they're declared — stack if a local, **inline inside
  the containing object on the heap** if a field.
- **Reference types** (`class`, `interface`, `delegate`, `string`, arrays): the variable holds a
  *reference*; the object lives on the heap. Assignment copies the reference, not the object.

⚠️ **The classic trap:** *"value types live on the stack"* is **wrong** and interviewers use it to
separate seniors from juniors. Say instead: *"where a value type lives depends on where it's declared
— a struct field inside a class lives on the heap, inline with the object. Stack vs heap is about
storage location, not about value vs reference."*

**Q: What is boxing? Why does it matter?**

Boxing = wrapping a value type in a heap object to treat it as `object`/an interface. Unboxing =
extracting it back with a type check.

```csharp
int x = 42;
object o = x;        // box: heap allocation + copy
int y = (int)o;      // unbox: type check + copy
```

Cost: heap allocation + GC pressure + indirection + cache misses. In a hot loop processing market
ticks, boxing is a real performance bug.

Where it sneaks in: non-generic collections (`ArrayList`, `Hashtable`), `string.Format`/interpolation
into `object` params, `struct` implementing an interface accessed *through* the interface,
`Enum.HasFlag` (pre-.NET Core 3), `object.Equals(object)` on a struct without overriding.

```csharp
// Avoiding boxing on struct comparison:
struct Price : IEquatable<Price>          // IEquatable<T> avoids boxing
{
    public decimal Value;
    public bool Equals(Price other) => Value == other.Value;   // no boxing
    public override bool Equals(object? o) => o is Price p && Equals(p); // boxes
    public override int GetHashCode() => Value.GetHashCode();
}
```

**Q: When would you use a `struct` instead of a `class`?**

Microsoft's guidance + the real reason: when it's small (≤16 bytes rule of thumb), immutable,
logically a single value, and short-lived/allocated in bulk. Real win: avoiding millions of heap
allocations. E.g. a `Tick { long InstrumentId; decimal Price; long TimestampTicks; }` in a market
data feed — as a struct in a pre-allocated array you get zero GC pressure and cache locality.

⚠️ Follow-up: *"downsides?"* → copy cost on every pass (use `in`/`ref readonly`), mutable structs are
a bug factory (a copy gets mutated, not the original), boxing when used via interfaces, and defensive
copies when a non-`readonly` struct is held in a `readonly` field.

```csharp
public readonly struct Tick          // readonly struct → compiler prevents mutation,
{                                    // no defensive copies
    public readonly long InstrumentId;
    public readonly decimal Price;
    public Tick(long id, decimal price) => (InstrumentId, Price) = (id, price);
}

void Process(in Tick t) { }          // 'in' = pass by readonly reference, no copy
```

**Q: `ref struct` / `Span<T>`?**

`ref struct` (e.g. `Span<T>`, `ReadOnlySpan<T>`) is **stack-only** — cannot be boxed, cannot be a
field of a class, cannot be captured in a lambda or used across `await`. That restriction is what
makes it safe to point at stack memory or into the middle of an array.

```csharp
Span<byte> buffer = stackalloc byte[256];     // no heap allocation at all
ReadOnlySpan<char> symbol = fullText.AsSpan(4, 6);   // slice with zero allocation
```

Use case worth naming: parsing a fixed-width market data or FIX message without allocating substrings.
`ReadOnlySpan<char>` + `int.TryParse(span, out ...)` gives you allocation-free parsing.

---

## 2. Garbage collection

**Q: Explain .NET GC.**

Generational, mark-and-sweep-and-compact, tracing collector.

- **Gen 0** — new small objects. Collected very often, very cheap. Most objects die here
  ("generational hypothesis").
- **Gen 1** — survivors of gen 0; a buffer between short- and long-lived.
- **Gen 2** — long-lived. Collected rarely; a full gen-2 collection is the expensive one.
- **LOH (Large Object Heap)** — objects **≥ 85,000 bytes**. Collected with gen 2, and historically
  **not compacted** (you can opt in via `GCSettings.LargeObjectHeapCompactionMode`). Causes
  fragmentation → OOM even with free memory available.
- **POH (Pinned Object Heap)** — .NET 5+, for pinned buffers, keeps pinning out of the normal heap.

Phases: **mark** (trace from roots — statics, stack locals, CPU registers, GC handles, f-reachable
queue) → **sweep/compact** (reclaim, move survivors, update references) → promote survivors.

**Q: Workstation vs Server GC?**

- **Workstation**: one heap, lower latency, tuned for client apps. Default for desktop.
- **Server**: one heap + one dedicated GC thread **per logical core**, much higher throughput,
  longer individual pauses. Default for ASP.NET Core. `<ServerGarbageCollection>true</...>`.
- **Background/concurrent GC**: gen 2 collection runs largely concurrently with the app to shorten
  pauses.

⚠️ **Great answer for this role:** *"For a real-time trading desktop I'd care about pause time more
than throughput — workstation + background GC, and more importantly reduce allocation in the hot path
so gen 2 rarely runs at all: object pooling, `ArrayPool<T>`, structs for ticks, avoiding LINQ and
closures in the tick handler. In .NET 9 the new adaptive DATAS mode for server GC also matters for
memory footprint."*

**Q: `IDisposable` vs finalizer?**

- `IDisposable.Dispose()` — **deterministic** cleanup of *unmanaged* or expensive resources, called
  by you or `using`.
- **Finalizer** (`~Type()`) — safety net run by the GC's finalizer thread, **non-deterministic**.
  Objects with finalizers survive an extra GC cycle (they go on the finalization queue, get
  resurrected to f-reachable, then collected next time). Never write one unless you directly hold an
  unmanaged handle — and prefer `SafeHandle`.

The canonical pattern:

```csharp
public class Connection : IDisposable
{
    private bool _disposed;
    private SafeHandle? _handle;

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);   // we cleaned up; skip the finalizer
    }

    protected virtual void Dispose(bool disposing)
    {
        if (_disposed) return;
        if (disposing) { _handle?.Dispose(); }   // managed resources
        // unmanaged cleanup here
        _disposed = true;
    }
}
```

`IAsyncDisposable` + `await using` when cleanup itself is async (e.g. flushing a network stream).

**Q: How do you find and fix a memory leak in .NET?**

Managed "leaks" are really **unintentional retention**. Top causes, in the order I'd check:
1. **Event handler subscriptions** — subscriber can't be collected because the publisher holds a
   reference. The #1 leak in WPF/desktop apps. Fix: unsubscribe, or weak event pattern.
2. **Static collections / caches** that grow forever. Fix: bounded cache, `MemoryCache` with eviction.
3. **Long-lived timers / background tasks** capturing objects.
4. **Captured closures** keeping a big graph alive.
5. Undisposed `IDisposable`s holding native memory.
6. **LOH fragmentation** presenting as OOM.

Tooling to name: `dotnet-counters` (live GC/alloc rates) → `dotnet-gcdump` / `dotnet-dump` → analyse
in Visual Studio diagnostic tools, PerfView, or dotMemory. Technique: take two snapshots under steady
load, diff, look at **retention paths / GC roots** for the type that grew.

---

## 3. Strings

- `string` is **immutable** and a reference type. Every "modification" allocates.
- **Interning**: literals share one instance in the intern pool; `string.Intern` for runtime strings.
- `StringBuilder` for loops/concatenation; not for 2–3 concatenations (`+` compiles to
  `string.Concat`, which is fine and often faster for small fixed counts).
- `==` on `string` is **value equality** (operator overload), unlike other reference types.
- `ReferenceEquals(a,b)` may be true for identical literals due to interning — a favourite trick Q.
- Comparison: use `StringComparison` explicitly. `Ordinal` for identifiers/symbols (fast, culture-free),
  `OrdinalIgnoreCase` for case-insensitive lookups, culture-aware only for user-facing sorting.
  ⚠️ In finance, always `Ordinal` for instrument symbols/tickers — culture rules can reorder or
  equate things you don't expect (the classic Turkish `I`/`ı` bug).

---

## 4. LINQ & collections

**Q: `IEnumerable<T>` vs `IQueryable<T>`?**

- `IEnumerable<T>` — **in-memory**, delegate-based, executes LINQ-to-Objects. Once you're on
  `IEnumerable`, everything after it runs on the client.
- `IQueryable<T>` — builds an **expression tree**, translated by a provider (EF Core) into SQL.

⚠️ The interview trap:

```csharp
// BAD: ToList() materialises the whole table, then filters in memory
var bad = db.Orders.ToList().Where(o => o.Status == "Filled");

// GOOD: filter translated into SQL WHERE
var good = await db.Orders.Where(o => o.Status == "Filled").ToListAsync();
```

**Q: Deferred vs immediate execution?**

LINQ operators are lazy — the query runs when enumerated. `ToList/ToArray/Count/First/Any/Sum` force
execution. Consequence: enumerate twice → query runs twice; and a captured variable changed between
definition and enumeration changes the result.

**Q: Complexity of the main collections?**

| Collection | Lookup | Insert | Notes |
|---|---|---|---|
| `List<T>` | O(n) search, O(1) index | O(1) amortised append | Contiguous → cache friendly |
| `Dictionary<K,V>` | O(1) avg | O(1) avg | Hash + buckets; O(n) worst on collisions |
| `HashSet<T>` | O(1) avg | O(1) avg | Set ops |
| `SortedDictionary<K,V>` | O(log n) | O(log n) | Red-black tree |
| `SortedList<K,V>` | O(log n) | O(n) insert | Array-backed, less memory, fast index |
| `Queue`/`Stack<T>` | — | O(1) | |
| `LinkedList<T>` | O(n) | O(1) at node | Rarely worth it — poor cache locality |
| `ConcurrentDictionary` | O(1) avg | O(1) avg | Striped locks; lock-free reads |
| `ImmutableList<T>` | O(log n) | O(log n) | Tree-backed, structural sharing |

**Q: Why must you override `GetHashCode` when you override `Equals`?**

Because hash-based collections locate an item by bucket first. Two "equal" objects with different
hash codes land in different buckets → `Dictionary`/`HashSet` will fail to find your item. Rules:
equal objects **must** have equal hash codes; the hash must be stable for the object's lifetime as a
key (**never hash on a mutable field** — mutate it and the object is lost inside the dictionary).

```csharp
public override int GetHashCode() => HashCode.Combine(Symbol, Venue);
```

`record` types generate value-based `Equals`/`GetHashCode`/`ToString` for you — a good answer to
*"how would you make a value object?"*.

---

## 5. Delegates, events, closures

- **Delegate** = type-safe function pointer; multicast by nature (`+=`).
- **Event** = a delegate with restricted access — outside the declaring type you can only `+=`/`-=`,
  not invoke or assign. That encapsulation is *the* reason events exist.
- `Func<>`/`Action<>`/`Predicate<>` are the built-in generic delegates.

⚠️ **Closure capture in a loop** — perennial interview question:

```csharp
// C# 5+ : foreach variable is per-iteration → prints 0,1,2 (any order)
foreach (var i in Enumerable.Range(0,3)) tasks.Add(Task.Run(() => Console.WriteLine(i)));

// for-loop variable is ONE variable, shared → often prints 3,3,3
for (int i = 0; i < 3; i++) tasks.Add(Task.Run(() => Console.WriteLine(i)));

// Fix: copy into a per-iteration local
for (int i = 0; i < 3; i++) { int local = i; tasks.Add(Task.Run(() => Console.WriteLine(local))); }
```

Closures allocate a compiler-generated class holding the captured variables — relevant in hot paths.

**Q: Why do events cause memory leaks?**
The publisher holds a strong reference to the subscriber's target object. If the publisher outlives
the subscriber (a long-lived service, or a WPF static/singleton view-model) the subscriber never gets
collected. Fixes: unsubscribe in `Dispose`/`Unloaded`, use `WeakEventManager` (WPF), or expose
`IObservable`/`IDisposable` subscriptions.

---

## 6. Generics, inheritance, modern C#

**Q: Covariance and contravariance?**
- `out T` (**covariant**) — you can use a more-derived type: `IEnumerable<Derived>` → `IEnumerable<Base>`.
  Only valid for output positions.
- `in T` (**contravariant**) — more-generic type accepted: `IComparer<Base>` → `IComparer<Derived>`.
  Only valid for input positions.
- Mnemonic: **out = producer, in = consumer.**
- ⚠️ Arrays are *covariant but unsafely so* — `object[] a = new string[1]; a[0] = 42;` compiles and
  throws `ArrayTypeMismatchException` at runtime. Generics fixed this.

**Q: Abstract class vs interface (modern C#)?**
Abstract class: shared *state* + shared implementation, single inheritance, can have constructors and
protected members. Interface: contract, multiple inheritance, now supports **default implementations**
(C# 8) and **static abstract members** (C# 11, enables generic math). Rule of thumb: "is-a with shared
state" → abstract class; "can-do capability" → interface. In DI-heavy code, interfaces win because
they're mockable and don't couple you to a hierarchy.

**Q: Modern C# features you actually use?** (Be ready — it signals currency.)

```csharp
// records: immutable value objects with value equality
public record Order(string Symbol, decimal Qty, decimal Price)
{
    public decimal Notional => Qty * Price;
}
var amended = order with { Qty = 500 };            // non-destructive mutation

// pattern matching
var fee = order switch
{
    { Notional: > 1_000_000 } => 0.0005m,
    { Symbol: "AAPL" or "MSFT" } => 0.001m,
    _ => 0.002m
};

// nullable reference types: compile-time null-safety (<Nullable>enable</Nullable>)
string? maybe = null;
int len = maybe?.Length ?? 0;

// required + init: immutable-after-construction with object initialiser syntax
public class Config { public required string Endpoint { get; init; } }

// primary constructors (C# 12), collection expressions (C# 12)
public class Service(IRepo repo) { public Task Get() => repo.LoadAsync(); }
int[] xs = [1, 2, 3, ..other];
```

**Q: What's the difference between .NET Framework, .NET Core, and .NET 5+?**
.NET Framework 4.8 — Windows-only, in-place OS-serviced, end of the line (still supported, no new
features). .NET Core → cross-platform, side-by-side, open source, faster. .NET 5+ unified the naming
and the BCL. **.NET 8 and 10 are LTS (3 yrs); 9 is STS (18 months).** For a WPF shop: WPF and
WinForms *are* supported on modern .NET (Windows-only), so a legacy WPF app can be migrated off
Framework — a very likely conversation in this interview.

---

## 7. Exceptions

- `throw;` preserves the original stack trace; `throw ex;` **resets** it. Classic gotcha.
- Catch only what you can handle. Don't catch `Exception` to log-and-swallow.
- **Exception filters** run *before* the stack unwinds — better diagnostics:
  ```csharp
  catch (SqlException ex) when (ex.Number == 1205)   // deadlock victim → retry
  ```
- Exceptions are **expensive** (stack capture, unwinding). Never use them for control flow in a hot
  loop — use `TryParse`/`TryGetValue` patterns.
- `AggregateException` from `Task.WaitAll`/`.Result`; `await` unwraps to the first inner exception.
- Custom exceptions: derive from `Exception`, add the three constructors, keep them meaningful.

---

## 8. Dependency injection & lifetimes

| Lifetime | Meaning | Trap |
|---|---|---|
| **Singleton** | One for app lifetime | Must be thread-safe. **Captive dependency**: injecting a Scoped/Transient into a Singleton keeps it alive forever and breaks scoping. |
| **Scoped** | One per request/scope | In a desktop app there's no ambient request — create scopes explicitly (`IServiceScopeFactory`). Critical for `DbContext`. |
| **Transient** | New every resolve | Cheap objects only; transient `IDisposable`s resolved from the root container are held until the container dies. |

`IHttpClientFactory` exists because raw `new HttpClient()` per call exhausts sockets (TIME_WAIT) and
a static `HttpClient` never picks up DNS changes. Say that — it's a common senior question.

---

## 9. Entity Framework Core

**Q: How does change tracking work?**
`DbContext` keeps an identity map of tracked entities with original values; `SaveChanges` diffs them
and generates SQL. `AsNoTracking()` skips it → significantly faster and less memory for read-only
queries. `DbContext` is **not thread-safe** and should be short-lived.

**Q: The N+1 problem?**
One query for the parent list, then one query per child access (lazy loading). Fix with `Include`/
`ThenInclude` (eager), projection to a DTO with `Select` (best — fetches only needed columns), or
`AsSplitQuery()` when a single join causes cartesian explosion.

```csharp
// Best: projection — one query, minimal columns, no tracking overhead
var rows = await db.Orders
    .Where(o => o.Date == today)
    .Select(o => new OrderRow(o.Id, o.Symbol, o.Qty, o.Trader.Name))
    .AsNoTracking()
    .ToListAsync(ct);
```

**Q: Optimistic vs pessimistic concurrency in EF Core?**
Optimistic: a `[Timestamp]`/`rowversion` concurrency token included in the `WHERE` of the `UPDATE`;
0 rows affected → `DbUpdateConcurrencyException` → you resolve (client wins / store wins / merge).
Pessimistic: DB locks (`UPDLOCK`, `SELECT ... FOR UPDATE`) via raw SQL — EF has no first-class API.
For an order-management system, optimistic concurrency on the order aggregate is the standard answer.

**Q: When would you use Dapper instead?**
Hot read paths, complex hand-tuned SQL, reporting queries, or where the object graph mapping is a
liability. Your CV already says "EF Core for writes, Dapper for reporting reads" — that is exactly
the answer they want, so say it with the reason: *"write side benefits from the unit of work and
change tracking; the read side benefits from full control of the SQL and no tracking overhead."*

**Other EF points:** migrations & zero-downtime (expand/contract pattern — add nullable column,
backfill, switch code, drop old), compiled queries (`EF.CompileAsyncQuery`) for hot repeated queries,
`DbContextPool` for high throughput, `ExecuteUpdateAsync`/`ExecuteDeleteAsync` (EF7+) for set-based
operations without loading entities.

---

## 10. SOLID — with one-line real examples (be ready to give *examples*, not definitions)

| | Principle | Your example |
|---|---|---|
| **S** | Single responsibility | Split an order service that both validated *and* persisted *and* published — validation moved to a rules component, publishing to an outbox dispatcher |
| **O** | Open/closed | New partner integrations added as new `IPartnerAdapter` implementations, no changes to the routing engine |
| **L** | Liskov substitution | A `ReadOnlyRepository` that throws on `Add` violates it — split the interface instead |
| **I** | Interface segregation | Don't force a market-data consumer to implement an `ISubscribe`+`IPublish`+`IAdmin` mega-interface |
| **D** | Dependency inversion | Domain layer defines `IPriceSource`; the infrastructure project implements it against the vendor SDK — Clean Architecture's dependency rule |

---

## 11. Rapid-fire — answer each in one sentence

1. `const` vs `readonly` → `const` is compile-time, baked into callers (versioning hazard across
   assemblies); `readonly` is set at runtime in the constructor.
2. `ref` vs `out` vs `in` → must be initialised before / must be assigned inside / read-only by
   reference (no copy).
3. `virtual`/`override` vs `new` → polymorphic dispatch vs hiding (dispatch depends on the *static*
   type — a classic trick question).
4. `IEnumerable` vs `IEnumerator` → the sequence vs the cursor over it.
5. `yield return` → compiler-generated state machine producing a lazy sequence.
6. `sealed` → prevents inheritance; enables devirtualisation, a small perf win.
7. `static` constructor → runs once, lazily, thread-safely before first use.
8. `params`, optional args → optional-arg defaults are baked into the **caller** — another versioning
   hazard.
9. `is` vs `as` → boolean test (with pattern matching) vs cast-or-null.
10. `checked`/`unchecked` → overflow throws vs wraps. **In finance code, wrap money arithmetic in
    `checked`.**
11. `decimal` vs `double` → **`decimal` for money** (base-10, 28–29 sig digits, exact for decimal
    fractions); `double` for scientific/statistical maths (binary floating point, `0.1 + 0.2 != 0.3`).
    ⚠️ *Expect this question in a capital-markets interview and get it right instantly.*
12. `Span<T>` vs `Memory<T>` → stack-only, sync-only vs heap-storable, usable across `await`.
13. `ValueTask` vs `Task` → avoid an allocation when the result is usually already available (cache
    hits); don't await it twice.
14. `ArrayPool<T>.Shared` → rent/return buffers to avoid LOH allocations. Always return in a `finally`.
15. `IOptions` vs `IOptionsSnapshot` vs `IOptionsMonitor` → singleton / per-scope reload /
    push-notified reload.
16. Reflection cost → slow; cache `MethodInfo`, or use source generators / compiled expressions.
17. `unsafe`/`fixed` → pointer arithmetic and pinning; used for interop and extreme perf.
18. `partial` → split a type across files; how designers and source generators contribute code.
19. Extension method → static method on a static class with `this` on the first parameter; resolved
    at compile time, so no polymorphism.
20. `async` return types → `Task`, `Task<T>`, `ValueTask<T>`, `IAsyncEnumerable<T>`, and `void`
    (**only** for event handlers — see `04`).

---

## 12. Three things to say that make you sound senior

1. *"I'd measure before optimising — BenchmarkDotNet for micro, a profiler for the real workload."*
2. *"The choice depends on the access pattern"* — then name the pattern. Works for collections,
   storage, caching, everything.
3. *"That's a correctness-versus-throughput trade-off"* — and state which side the business is on.
   In capital markets it's **always correctness**, and saying so shows domain instinct.
