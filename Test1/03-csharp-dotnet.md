# 03 — C# & .NET, IN PLAIN ENGLISH

> This is their **core specialization**. It must be flawless.
>
> **Format:** **Q:** what they ask → **Say:** the words you speak → **Remember:** the hook →
> ⚠️ the follow-up they'll try.
>
> Say the answer, then **stop talking**. Silence invites the follow-up you're ready for.

---

# FULL TECH LOAD MEMORY HOOKS

Use these as labels for the full detail below. Say the hook first, then give the technical load only
if they ask for depth.

| Hook | Simple wording | Full tech load to keep |
|---|---|---|
| **Money = decimal** | Cash needs exact base-10 maths. | `decimal`/`Decimal`/`DECIMAL`, explicit rounding, `checked` arithmetic. |
| **Declaration decides location** | A struct is not automatically stack memory. | Locals can be on the stack; struct fields inside classes live inline on the heap. |
| **Boxing allocates** | A value gets wrapped as an object. | Heap allocation, copy, indirection, GC pressure; avoid in hot paths. |
| **Allocate less** | Low latency is mostly fewer allocations. | Gen 0/1/2, LOH at 85 KB, pooling, `ArrayPool<T>`, `Span<T>`, no LINQ in tick handlers. |
| **Query stays SQL** | Keep database work in the database. | `IQueryable` expression tree vs `IEnumerable` in memory; `ToList()` too early causes client filtering. |
| **Hash must match equals** | If two values are equal, their hashes must be equal. | Override both; never hash mutable fields. |
| **Dispose now, finalizer later** | `Dispose` is controlled cleanup. | `using`, `IAsyncDisposable`, `SafeHandle`, `GC.SuppressFinalize`. |
| **Lifetime leaks** | A long-lived object can accidentally hold short-lived state. | Singleton/scoped/transient, captive dependencies, `DbContext`, event handler leaks. |

---

# PART 0 — THE 12 C# ANSWERS THAT WIN

| # | The question | The answer, in one breath |
|---|---|---|
| 1 | **Money** | "`decimal`. It's base-10 and exact for decimal fractions. `double` is binary — `0.1 + 0.2` isn't `0.3`. In finance, `decimal`, always, and I wrap the arithmetic in `checked`." |
| 2 | **Do value types live on the stack?** | "No — that's the trap. **Where** a value lives depends on where it's declared. A struct field inside a class lives on the heap, inline with the object. Stack vs heap is about storage, not about value vs reference." |
| 3 | **Boxing** | "Wrapping a value type in a heap object so it can be treated as `object`. It costs an allocation and a copy. In a tick handler that's a real performance bug." |
| 4 | **The GC** | "Generational, mark-sweep-compact. Gen 0 is cheap and most objects die there. Gen 2 is the expensive one. Large objects — 85 KB and up — go on the Large Object Heap, which historically isn't compacted, so you get fragmentation." |
| 5 | **Low latency in .NET** | "**Don't tune the GC — reduce allocation.** Structs, `Span<T>`, `ArrayPool`, object pooling, no LINQ or closures in the hot path." |
| 6 | **`IEnumerable` vs `IQueryable`** | "In-memory versus an expression tree the provider turns into SQL. Call `ToList()` too early and you pull the whole table and filter in memory." |
| 7 | **`Equals` and `GetHashCode`** | "Override one, you must override the other. Hash-based collections find the bucket first — mismatch and the dictionary loses your item. And never hash a field you'll mutate." |
| 8 | **`throw;` vs `throw ex;`** | "`throw;` keeps the original stack trace. `throw ex;` resets it and you lose where it came from." |
| 9 | **DI lifetimes** | "Singleton, Scoped, Transient. The trap is the **captive dependency** — inject a Scoped into a Singleton and it lives forever, which breaks scoping and usually `DbContext`." |
| 10 | **N+1 in EF** | "One query for the parents, then one per child. Fix with `Include`, or better, project to a DTO with `Select` so you only fetch the columns you need." |
| 11 | **`HttpClient`** | "`new HttpClient()` per call exhausts sockets. A static one never picks up DNS changes. Use `IHttpClientFactory` — it solves both." |
| 12 | **Value objects** | "A `record`. It generates value-based `Equals`, `GetHashCode` and `ToString`, and `with` gives non-destructive copies." |

---

# PART 1 — MEMORY: STACK, HEAP, VALUE, REFERENCE

## 1.1 Value types vs reference types

**Value types** (`struct`, `int`, `bool`, `enum`, `decimal`, `DateTime`, tuples)
→ hold the data **directly**. Assignment **copies the data**.

**Reference types** (`class`, `interface`, `delegate`, `string`, arrays)
→ hold a **reference**. Assignment copies the **reference**, not the object.

**Q: Where do they live?**

⚠️ **The trap:** *"value types live on the stack"* is **wrong**, and interviewers use it to separate
seniors from juniors.

**Say:** *"Where a value type lives depends on where it's declared. A local goes on the stack. A struct
field inside a class lives on the heap, inline with the object. Stack versus heap is about storage
location, not about value versus reference."*

**Remember:** **Declaration decides location, not the type kind.**

---

## 1.2 Boxing

**Say:** *"Boxing wraps a value type in a heap object so you can treat it as `object` or an interface.
Unboxing pulls it back out with a type check. The cost is a heap allocation, a copy, GC pressure and
an extra indirection. In a hot loop processing market ticks, that's a genuine performance bug."*

```csharp
int x = 42;
object o = x;        // box: heap allocation + copy
int y = (int)o;      // unbox: type check + copy
```

**Where it sneaks in** (name two or three):
- Non-generic collections — `ArrayList`, `Hashtable`
- Passing a struct into anything taking `object`
- A struct implementing an interface, accessed *through* that interface
- `object.Equals(object)` on a struct you didn't give an override to

```csharp
struct Price : IEquatable<Price>              // IEquatable<T> avoids the boxing
{
    public decimal Value;
    public bool Equals(Price other) => Value == other.Value;              // no boxing
    public override bool Equals(object? o) => o is Price p && Equals(p);  // boxes
    public override int GetHashCode() => Value.GetHashCode();
}
```

---

## 1.3 When would you use a `struct`?

**Say:** *"When it's small — around 16 bytes or less — immutable, logically a single value, and
created in bulk. The real win is avoiding millions of heap allocations. A `Tick` with an instrument
ID, a price and a timestamp, held in a pre-allocated array, gives me zero GC pressure and good cache
locality."*

⚠️ **They will ask about downsides. Have them ready:**
- Copy cost on every pass — use `in` or `ref readonly`
- **Mutable structs are a bug factory** — you mutate a copy, not the original
- Boxing when used through an interface
- Defensive copies when a non-`readonly` struct sits in a `readonly` field

```csharp
public readonly struct Tick            // readonly struct = no mutation, no defensive copies
{
    public readonly long InstrumentId;
    public readonly decimal Price;
    public Tick(long id, decimal price) => (InstrumentId, Price) = (id, price);
}

void Process(in Tick t) { }            // 'in' = pass by readonly reference, no copy
```

---

## 1.4 `Span<T>` and `ref struct`

**Say:** *"`Span<T>` is a `ref struct` — stack-only. It can't be boxed, can't be a field of a class,
can't be captured in a lambda or held across an `await`. Those restrictions are exactly what make it
safe to point at stack memory or into the middle of an array. The use case worth naming here: parsing
a fixed-width market data or FIX message without allocating a single substring."*

```csharp
Span<byte> buffer = stackalloc byte[256];              // zero heap allocation
ReadOnlySpan<char> symbol = fullText.AsSpan(4, 6);     // slice with no allocation
int.TryParse(symbol, out var value);                   // allocation-free parsing
```

**`Span<T>` vs `Memory<T>`:** stack-only and synchronous vs heap-storable and usable across `await`.

---

# PART 2 — GARBAGE COLLECTION

## 2.1 How it works

**Say:** *"It's a generational, tracing, mark-sweep-and-compact collector.*
- ***Gen 0*** *is new small objects. Collected very often, very cheaply — most objects die here.*
- ***Gen 1*** *is survivors of gen 0, a buffer between short- and long-lived.*
- ***Gen 2*** *is long-lived. Collected rarely, and a full gen 2 is the expensive pause.*
- ***The Large Object Heap*** *takes anything 85,000 bytes or bigger. It's collected with gen 2 and
  historically isn't compacted, so you get fragmentation — out-of-memory even with free memory
  available."*

**The phases:** **mark** (trace from the roots — statics, stack locals, registers, GC handles) →
**sweep and compact** (reclaim, move survivors, fix up references) → **promote** the survivors.

**Remember:** **Gen 0 cheap, gen 2 expensive, LOH at 85 KB and not compacted.**

## 2.2 Workstation vs Server GC

| | Workstation | Server |
|---|---|---|
| Heaps | One | One per logical core, with a dedicated GC thread each |
| Optimised for | **Low latency** | **Throughput** |
| Default for | Desktop apps | ASP.NET Core |

**⚠️ The answer that's perfect for this role:**
> *"For a real-time trading desktop I care about pause time far more than throughput — so workstation
> plus background GC. But more importantly I'd reduce allocation in the hot path so gen 2 barely runs
> at all: object pooling, `ArrayPool<T>`, structs for ticks, no LINQ or closures inside the tick
> handler. **You don't tune your way out of a GC problem, you allocate your way out of it.**"*

## 2.3 `IDisposable` vs finalizer

**Say:** *"`Dispose` is **deterministic** — I call it, or `using` calls it, and cleanup happens now.
A finalizer is a **non-deterministic** safety net run by the GC's finalizer thread. Objects with a
finalizer survive an extra collection cycle, so they're not free. I'd never write one unless I
directly held an unmanaged handle — and even then I'd use `SafeHandle` instead."*

```csharp
public void Dispose()
{
    Dispose(true);
    GC.SuppressFinalize(this);    // we cleaned up — skip the finalizer, save a GC cycle
}
```

`IAsyncDisposable` + `await using` when the cleanup itself is async.

## 2.4 Finding a memory leak in .NET

**Say:** *"Managed leaks are really **unintentional retention** — something is still holding a
reference. In order of likelihood I'd check:*
1. ***Event handler subscriptions*** *— the publisher holds a strong reference to the subscriber. This
   is the number one leak in desktop apps.*
2. ***Static collections and caches*** *that grow forever.*
3. ***Long-lived timers or background tasks*** *capturing objects.*
4. ***Captured closures*** *keeping a big object graph alive.*
5. ***Undisposed `IDisposable`s*** *holding native memory.*
6. ***LOH fragmentation***, *which shows up as out-of-memory."*

**Tooling:** `dotnet-counters` for live allocation rates → `dotnet-gcdump` / `dotnet-dump` →
analyse in Visual Studio, PerfView or dotMemory.

**The technique to state:** *"Two snapshots under steady load, diff them, and look at the **retention
path** — the chain of GC roots keeping the type that grew alive."*

---

# PART 3 — STRINGS

**Say:** *"`string` is immutable and a reference type. Every modification allocates a new one."*

- **Interning:** literals share one instance in the intern pool. So `ReferenceEquals` can be `true`
  for two identical literals — a favourite trick question.
- `==` on `string` is **value equality**, unlike other reference types. It's an operator overload.
- **`StringBuilder`** for loops. Not for two or three concatenations — `+` compiles to
  `string.Concat`, which is fine and often faster for a small fixed count.
- **Always pass a `StringComparison`.** `Ordinal` for identifiers and symbols — fast and culture-free.
  Culture-aware only for user-facing sorting.

⚠️ **The finance detail worth saying:** *"For instrument symbols and tickers, always `Ordinal`.
Culture rules can equate or reorder things you don't expect — the classic case is the Turkish
dotless i, where `"IBM".ToLower()` in a Turkish locale doesn't give you `"ibm"`."*

---

# PART 4 — LINQ AND COLLECTIONS

## 4.1 `IEnumerable<T>` vs `IQueryable<T>`

**Say:** *"`IEnumerable` is in-memory and delegate-based. `IQueryable` builds an **expression tree**
that a provider like EF Core translates into SQL. The moment you're on `IEnumerable`, everything after
it runs on the client."*

```csharp
var bad  = db.Orders.ToList().Where(o => o.Status == "Filled");   // pulls the whole table!
var good = await db.Orders.Where(o => o.Status == "Filled").ToListAsync();  // WHERE in SQL
```

**Remember:** **`ToList()` is the border. Everything after it runs on your machine.**

## 4.2 Deferred execution

**Say:** *"LINQ operators are lazy — nothing runs until you enumerate. `ToList`, `Count`, `First`,
`Any` and `Sum` force it. Two consequences: enumerate twice and the query runs twice; and a captured
variable changed between defining and enumerating changes the result."*

## 4.3 Collection complexity

| Collection | Lookup | Insert | Note |
|---|---|---|---|
| `List<T>` | O(n) search, O(1) by index | O(1) amortised append | Contiguous — cache friendly |
| `Dictionary<K,V>` | O(1) average | O(1) average | O(n) worst case on collisions |
| `HashSet<T>` | O(1) average | O(1) average | Set operations |
| `SortedDictionary<K,V>` | O(log n) | O(log n) | Red-black tree |
| `SortedList<K,V>` | O(log n) | O(n) | Array-backed; less memory, fast by index |
| `Queue<T>` / `Stack<T>` | — | O(1) | |
| `LinkedList<T>` | O(n) | O(1) at a node | Rarely worth it — poor cache locality |
| `ConcurrentDictionary` | O(1) average | O(1) average | Striped locks, lock-free reads |
| `ImmutableList<T>` | O(log n) | O(log n) | Tree-backed, structural sharing |

## 4.4 Why `GetHashCode` must match `Equals`

**Say:** *"Hash-based collections find the **bucket** first, then compare. If two equal objects produce
different hash codes they land in different buckets, so `Dictionary` and `HashSet` will never find
your item. Two rules: equal objects must hash equal, and **never hash on a field you'll mutate** —
mutate it and the object is lost inside the dictionary forever."*

```csharp
public override int GetHashCode() => HashCode.Combine(Symbol, Venue);
```

**Q: How would you make a value object?**
**Say:** *"A `record`. It generates value-based equality, hash code and `ToString` for me, and `with`
gives non-destructive copies."*

---

# PART 5 — DELEGATES, EVENTS, CLOSURES

**Say:** *"A **delegate** is a type-safe function pointer, and it's multicast — you can chain handlers
with `+=`. An **event** is a delegate with restricted access: outside the declaring type you can only
subscribe and unsubscribe, not invoke or replace it. That encapsulation is the entire reason events
exist."*

⚠️ **The closure-in-a-loop question:**
```csharp
// foreach: the variable is per-iteration in C# 5+ → prints 0,1,2
foreach (var i in Enumerable.Range(0,3)) tasks.Add(Task.Run(() => Console.WriteLine(i)));

// for: ONE shared variable → often prints 3,3,3
for (int i = 0; i < 3; i++) tasks.Add(Task.Run(() => Console.WriteLine(i)));

// fix: copy into a per-iteration local
for (int i = 0; i < 3; i++) { int local = i; tasks.Add(Task.Run(() => Console.WriteLine(local))); }
```

**Q: Why do events cause memory leaks?**
**Say:** *"The publisher holds a **strong** reference to the subscriber. If the publisher outlives the
subscriber — a long-lived service, or a static view-model in WPF — the subscriber can never be
collected. Fixes: unsubscribe in `Dispose` or `Unloaded`, use `WeakEventManager` in WPF, or hand back
an `IDisposable` subscription."*

**Remember:** **The publisher holds the subscriber. Unsubscribe or leak.**

---

# PART 6 — GENERICS AND MODERN C#

## 6.1 Covariance and contravariance

- **`out T` — covariant.** Producer. `IEnumerable<Derived>` can be used as `IEnumerable<Base>`.
- **`in T` — contravariant.** Consumer. `IComparer<Base>` can be used as `IComparer<Derived>`.

**Remember:** **out = producer, in = consumer.**

⚠️ *"Arrays are covariant but unsafely so — `object[] a = new string[1]; a[0] = 42;` compiles and
throws at runtime. Generics fixed that."*

## 6.2 Abstract class vs interface

**Say:** *"Abstract class when there's shared **state** and shared implementation — single inheritance,
constructors, protected members. Interface for a capability — multiple inheritance, and since C# 8 it
can have default implementations, and C# 11 added static abstract members which enable generic maths.
Rule of thumb: 'is-a with shared state' is a base class, 'can-do' is an interface. In DI-heavy code
interfaces win, because they're mockable and don't couple you to a hierarchy."*

## 6.3 Modern C# — be ready, it signals currency

```csharp
// records — immutable value objects with value equality
public record Order(string Symbol, decimal Qty, decimal Price)
{
    public decimal Notional => Qty * Price;
}
var amended = order with { Qty = 500 };            // non-destructive mutation

// pattern matching
var fee = order switch
{
    { Notional: > 1_000_000 }      => 0.0005m,
    { Symbol: "AAPL" or "MSFT" }   => 0.001m,
    _                              => 0.002m
};

// nullable reference types — compile-time null safety
string? maybe = null;
int len = maybe?.Length ?? 0;

// required + init — immutable after construction, object-initialiser syntax
public class Config { public required string Endpoint { get; init; } }

// primary constructors and collection expressions (C# 12)
public class Service(IRepo repo) { public Task Get() => repo.LoadAsync(); }
int[] xs = [1, 2, 3, ..other];
```

## 6.4 .NET Framework vs .NET Core vs .NET 5+

**Say:** *".NET Framework 4.8 is Windows-only, serviced in place with the OS, and it's the end of the
line — supported, but no new features. .NET Core made it cross-platform, side-by-side and open source.
.NET 5 unified the naming and the base library. **.NET 8 and 10 are LTS at three years; 9 is
short-term at 18 months.** And importantly for this role: **WPF and WinForms are supported on modern
.NET** — Windows-only, but a legacy WPF app absolutely can be migrated off Framework."*

**That last sentence is a very likely conversation in this interview. Have it ready.**

---

# PART 7 — EXCEPTIONS

- **`throw;` preserves the original stack trace. `throw ex;` resets it.** Classic gotcha.
- Catch only what you can handle. Don't catch `Exception` to log and swallow.
- **Exception filters run *before* the stack unwinds** — better diagnostics:
  ```csharp
  catch (SqlException ex) when (ex.Number == 1205)   // deadlock victim → retry
  ```
- **Exceptions are expensive in .NET** — stack capture plus unwinding. Never use them for control flow
  in a hot loop. Use `TryParse` and `TryGetValue`. *(Note the contrast with Python, where they're
  cheap and the idiom is the opposite — pointing that out is a nice moment.)*
- `Task.WaitAll` and `.Result` give you an `AggregateException`; `await` unwraps to the first inner one.

---

# PART 8 — DEPENDENCY INJECTION

| Lifetime | Meaning | The trap |
|---|---|---|
| **Singleton** | One for the app's lifetime | Must be thread-safe. **Captive dependency:** inject a Scoped or Transient into a Singleton and it's kept alive forever, breaking scoping. |
| **Scoped** | One per request or scope | A desktop app has no ambient request — create scopes explicitly with `IServiceScopeFactory`. Critical for `DbContext`. |
| **Transient** | New every time | Cheap objects only. A transient `IDisposable` resolved from the **root** container is held until the container dies. |

**Q: Why `IHttpClientFactory`?**
**Say:** *"Two problems. A new `HttpClient` per call exhausts sockets — they sit in TIME_WAIT. But a
single static one never picks up DNS changes, so a failover moves and you keep calling the dead
address. The factory pools handlers and rotates them, which solves both."*

---

# PART 9 — ENTITY FRAMEWORK CORE

**Q: How does change tracking work?**
**Say:** *"`DbContext` keeps an identity map of tracked entities with their original values.
`SaveChanges` diffs them and generates the SQL. `AsNoTracking()` skips all of that — significantly
faster and lighter for read-only queries. And `DbContext` is **not thread-safe** and should be
short-lived."*

**Q: The N+1 problem?**
**Say:** *"One query for the parent list, then one more query per child access because of lazy
loading. Fix with `Include` for eager loading, or better, **project to a DTO with `Select`** — one
query, only the columns you need, no tracking overhead. `AsSplitQuery()` when a single join causes a
cartesian explosion."*

```csharp
var rows = await db.Orders
    .Where(o => o.Date == today)
    .Select(o => new OrderRow(o.Id, o.Symbol, o.Qty, o.Trader.Name))   // projection
    .AsNoTracking()
    .ToListAsync(ct);
```

**Q: Optimistic vs pessimistic concurrency?**
**Say:** *"Optimistic uses a `rowversion` concurrency token in the `WHERE` clause of the `UPDATE`.
Zero rows affected means someone else got there first, and EF throws
`DbUpdateConcurrencyException` — then I decide: client wins, store wins, or merge. Pessimistic takes
database locks, which EF has no first-class API for. **For an order management system, optimistic
concurrency on the order aggregate is the standard answer.**"*

**Q: When would you use Dapper instead?**
**Say:** *"Hot read paths, hand-tuned SQL, and reporting queries. My rule is EF Core for writes,
Dapper for reporting reads — the write side benefits from the unit of work and change tracking, the
read side benefits from full control of the SQL and no tracking overhead."*

**Also worth naming:** migrations with the **expand/contract** pattern for zero downtime (add a
nullable column, backfill, switch the code, then drop the old one), compiled queries for hot repeated
queries, `DbContextPool`, and `ExecuteUpdateAsync`/`ExecuteDeleteAsync` for set-based work without
loading entities.

---

# PART 10 — SOLID, WITH EXAMPLES NOT DEFINITIONS

**They want examples. Definitions sound rehearsed.**

| | Principle | Your one-line example |
|---|---|---|
| **S** | Single responsibility | Split an order service that validated *and* persisted *and* published — validation moved to a rules component, publishing to an outbox dispatcher |
| **O** | Open/closed | New partner integrations are new `IPartnerAdapter` implementations; the routing engine never changes |
| **L** | Liskov substitution | A `ReadOnlyRepository` that throws on `Add` violates it — split the interface instead |
| **I** | Interface segregation | Don't force a market-data consumer to implement `ISubscribe` + `IPublish` + `IAdmin` |
| **D** | Dependency inversion | The domain defines `IPriceSource`; infrastructure implements it against the vendor SDK. Clean Architecture's dependency rule |

---

# PART 11 — RAPID-FIRE: 60 QUESTIONS

| # | Q | A |
|---|---|---|
| 1 | `const` vs `readonly` | Compile-time, baked into callers (a versioning hazard) vs set at runtime in the constructor |
| 2 | `ref` vs `out` vs `in` | Must be initialised before / must be assigned inside / read-only by reference, no copy |
| 3 | `virtual`/`override` vs `new` | Polymorphic dispatch vs hiding — hiding dispatches on the **static** type |
| 4 | `IEnumerable` vs `IEnumerator` | The sequence vs the cursor over it |
| 5 | `yield return` | A compiler-generated state machine producing a lazy sequence |
| 6 | `sealed` | Prevents inheritance; enables devirtualisation, a small perf win |
| 7 | Static constructor | Runs once, lazily, thread-safely, before first use |
| 8 | Optional argument defaults | Baked into the **caller** — another versioning hazard |
| 9 | `is` vs `as` | Boolean test with pattern matching vs cast-or-null |
| 10 | `checked` / `unchecked` | Overflow throws vs wraps. **Wrap money arithmetic in `checked`** |
| 11 | `decimal` vs `double` | Base-10 exact for money vs binary float for science. **Money is always `decimal`** |
| 12 | `Span<T>` vs `Memory<T>` | Stack-only, sync-only vs heap-storable, works across `await` |
| 13 | `ValueTask` vs `Task` | Avoids an allocation when the result is usually already there. Never await it twice |
| 14 | `ArrayPool<T>.Shared` | Rent and return buffers to avoid LOH allocations. Return in a `finally` |
| 15 | `IOptions` / `Snapshot` / `Monitor` | Singleton / per-scope reload / push-notified reload |
| 16 | Reflection cost | Slow — cache `MethodInfo`, or use source generators |
| 17 | `unsafe` / `fixed` | Pointer arithmetic and pinning. Interop and extreme perf |
| 18 | `partial` | Split a type across files — how designers and source generators contribute |
| 19 | Extension method | Static method with `this` on the first parameter; resolved at compile time, so no polymorphism |
| 20 | `async` return types | `Task`, `Task<T>`, `ValueTask<T>`, `IAsyncEnumerable<T>`, and `void` **only** for event handlers |
| 21 | Value vs reference type | Holds the data vs holds a reference |
| 22 | Do value types live on the stack? | **No** — depends where they're declared |
| 23 | Boxing cost | Heap allocation + copy + indirection + GC pressure |
| 24 | Avoid boxing on a struct | Implement `IEquatable<T>` |
| 25 | When to use a struct | Small, immutable, single value, created in bulk |
| 26 | `readonly struct` | Compiler prevents mutation; no defensive copies |
| 27 | GC generations | 0 cheap and frequent, 1 buffer, 2 expensive and rare |
| 28 | LOH threshold | 85,000 bytes; collected with gen 2, historically not compacted |
| 29 | POH | Pinned Object Heap — keeps pinned buffers out of the normal heap |
| 30 | Workstation vs server GC | Low latency, one heap vs throughput, a heap per core |
| 31 | `Dispose` vs finalizer | Deterministic, you call it vs GC-run safety net, costs an extra cycle |
| 32 | `GC.SuppressFinalize` | "I've cleaned up" — skips the finalizer |
| 33 | Top .NET leak cause | Event handler subscriptions |
| 34 | Diagnose a leak | Two heap snapshots under load, diff, follow the retention path |
| 35 | Is `string` a value type? | No — reference type, but immutable with value equality |
| 36 | String interning | Literals share one instance; `ReferenceEquals` can surprise you |
| 37 | `StringComparison` | Always pass it. `Ordinal` for symbols and identifiers |
| 38 | `IEnumerable` vs `IQueryable` | In memory vs an expression tree translated to SQL |
| 39 | Deferred execution | Nothing runs until enumerated; enumerate twice, run twice |
| 40 | Dictionary lookup complexity | O(1) average, O(n) worst on collisions |
| 41 | `Equals` without `GetHashCode` | The dictionary loses your item |
| 42 | Never hash on | A mutable field |
| 43 | `record` | Value equality, `with` expressions, generated `ToString` |
| 44 | Delegate vs event | Function pointer vs a delegate with restricted access |
| 45 | Closure allocation | A compiler-generated class holding the captured variables |
| 46 | Covariance / contravariance | `out` producer / `in` consumer |
| 47 | Array covariance | Unsafe — compiles, throws at runtime. Generics fixed it |
| 48 | Abstract class vs interface | Shared state vs a capability contract |
| 49 | Default interface methods | C# 8 — add to an interface without breaking implementers |
| 50 | `throw;` vs `throw ex;` | Preserves the stack trace vs resets it |
| 51 | Exception filter | `when (...)` — runs before the stack unwinds |
| 52 | Are exceptions cheap? | **No** in .NET. Never for control flow in a hot loop |
| 53 | `AggregateException` | From `WaitAll`/`.Result`; `await` unwraps the first inner one |
| 54 | DI lifetimes | Singleton / Scoped / Transient |
| 55 | Captive dependency | A shorter lifetime injected into a longer one — lives forever |
| 56 | Why `IHttpClientFactory` | Socket exhaustion and stale DNS, both solved |
| 57 | EF change tracking | Identity map + original values; `AsNoTracking` skips it |
| 58 | Fix N+1 | `Include`, or better, project with `Select` |
| 59 | EF concurrency | `rowversion` token; 0 rows affected → `DbUpdateConcurrencyException` |
| 60 | LTS versions | .NET 8 and .NET 10 |

---

# PART 12 — THREE THINGS THAT MAKE YOU SOUND SENIOR

1. **"I'd measure before optimising."** BenchmarkDotNet for micro, a profiler for the real workload.

2. **"It depends on the access pattern"** — then *name the pattern*. That works for collections,
   storage, caching, indexing, everything. It's the difference between an opinion and judgement.

3. **"That's a correctness-versus-throughput trade-off"** — and then say which side the business is
   on. In capital markets it is **always correctness**, and saying so shows domain instinct before
   they've told you anything about the domain.
