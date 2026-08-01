# 06 — Python (Advanced) — full interview preparation

> The JD lists **"Python (Advanced)"** as a must-have, equal billing with .NET. In a buy-side shop
> Python is the **quant / analytics / data layer**: pricing, risk, backtesting, reporting pipelines,
> and service glue.
>
> You have genuine Python (FastAPI, Pandas, NumPy, asyncio, Celery, SQLAlchemy, PyTest). What wins
> the interview is **internals** — the GIL, memory, the data model — because that's what separates
> "I use Python" from "Advanced".
>
> Explanations use **C# comparisons** wherever they help, since that's your deepest ground.

**Priority if short on time:** §5 (GIL & concurrency) → §1–2 (core + functions) → §11 (Pandas/NumPy)
→ §10 (performance) → §17 (rapid-fire) → the rest.

---

# PART 1 — CORE LANGUAGE & THE DATA MODEL

## 1.1 Everything is an object
In Python, integers, functions, classes and modules are **all objects**. A variable is just a **name
bound to an object** — think of it as a reference, always.

```python
x = [1, 2, 3]
y = x            # y and x point at the SAME list
y.append(4)
print(x)         # [1, 2, 3, 4]  ← surprises people
```
**C# comparison:** Python has no value types in the C# sense. Everything behaves like a reference
type. What makes it *feel* like value semantics is **immutability**, not copying.

## 1.2 Mutable vs immutable — the distinction everything else depends on

| Immutable | Mutable |
|---|---|
| `int`, `float`, `str`, `bool`, `tuple`, `frozenset`, `bytes` | `list`, `dict`, `set`, `bytearray`, most custom classes |

Immutable objects can't be changed — "modifying" one creates a new object.
```python
s = "hello"
s += " world"     # creates a NEW string; the old one is discarded (same as C# strings)
```
**Why it matters in interviews:** only immutable (hashable) objects can be dict keys or set members.
A `list` can't be a dict key; a `tuple` can.

## 1.3 The mutable default argument — the #1 Python gotcha
```python
def add(item, bucket=[]):        # ⚠️ BUG — the list is created ONCE, when the function is defined
    bucket.append(item)
    return bucket

add(1)   # [1]
add(2)   # [1, 2]   ← the same list, still there!

def add(item, bucket=None):      # ✅ FIX
    bucket = [] if bucket is None else bucket
    bucket.append(item)
    return bucket
```
**Why:** default arguments are evaluated **once at definition time**, not per call. Expect this
question — it's asked constantly.

## 1.4 `is` vs `==`
- `==` → **equality** (calls `__eq__`) — "do these have the same value?"
- `is` → **identity** — "are these literally the same object in memory?"

⚠️ Small integers (−5 to 256) and short strings are **interned** (cached and reused), so `is`
sometimes appears to work by accident:
```python
a = 256; b = 256; a is b     # True  (cached)
a = 257; b = 257; a is b     # False (different objects)
```
**Rule: only use `is` for `None`, `True`, `False` and sentinel objects.**
**C#:** `==` vs `ReferenceEquals` — same distinction, same interning trap with strings.

## 1.5 Shallow vs deep copy
```python
import copy
shallow = copy.copy(original)      # new outer object, SAME inner objects
deep    = copy.deepcopy(original)  # everything copied recursively
lst2 = lst[:]                      # slicing is also a shallow copy
```

## 1.6 The core containers

| Type | What | Big-O | Note |
|---|---|---|---|
| `list` | Ordered, mutable, dynamic array | index O(1), append O(1) amortised, insert/delete O(n), `in` O(n) | C# `List<T>` |
| `tuple` | Ordered, **immutable** | same lookups | hashable → usable as dict key |
| `dict` | Key→value, **insertion-ordered** since 3.7 | get/set O(1) avg | C# `Dictionary` |
| `set` | Unique, unordered | add/`in` O(1) avg | C# `HashSet` |
| `frozenset` | Immutable set | | hashable |
| `str` | Immutable text | | |

```python
# dict/set comprehensions — know these exist
squares = {n: n * n for n in range(5)}
symbols = {t.symbol for t in trades}
```

## 1.7 Slicing
```python
xs[2:5]     # items 2,3,4
xs[:3]      # first three
xs[-1]      # last item
xs[::-1]    # reversed copy
xs[::2]     # every second item
```
Slicing a list produces a **copy**; slicing a NumPy array produces a **view** (§11) — an important
difference and a good thing to point out unprompted.

## 1.8 Truthiness
Falsy: `False`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None`.
⚠️ `if not my_list:` is idiomatic for "empty", but `if not count:` is a bug when 0 is a legitimate
value — use `if count is None:`.

## 1.9 f-strings and formatting
```python
f"{price:,.2f}"        # 1,234.57
f"{ratio:.1%}"         # 12.3%
f"{value=}"            # "value=42"  — debugging shortcut (3.8+)
```

---

# PART 2 — FUNCTIONS, CLOSURES, DECORATORS

## 2.1 Arguments
```python
def f(a, b=2, *args, key=None, **kwargs): ...
#     ^positional  ^var-positional  ^keyword-only  ^var-keyword

def g(a, b, /, c, *, d): ...   # a,b positional-only; d keyword-only (3.8+)
```
Call-by-**object-reference**: you pass the object. Reassigning the parameter inside doesn't affect the
caller; **mutating** it does.

## 2.2 Closures
```python
def make_counter():
    count = 0
    def inc():
        nonlocal count      # without this you'd get UnboundLocalError
        count += 1
        return count
    return inc
```
**C#:** identical to a lambda capturing a local. `nonlocal` exists because assignment inside a
function creates a *local* by default.

⚠️ **Late binding in loops** — the Python version of the C# closure trap:
```python
fns = [lambda: i for i in range(3)]
[f() for f in fns]                  # [2, 2, 2]  ← all see the final i
fns = [lambda i=i: i for i in range(3)]   # ✅ bind now via a default arg → [0, 1, 2]
```

## 2.3 Decorators — a very likely "advanced Python" question
A decorator is **a function that takes a function and returns a new function**. `@x` above a
function is just `f = x(f)`.

```python
import functools, time

def retry(times=3, backoff=0.2):
    def decorator(fn):
        @functools.wraps(fn)                 # preserves __name__, __doc__, signature
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return fn(*args, **kwargs)
                except TransientError:
                    if attempt == times - 1:
                        raise
                    time.sleep(backoff * 2 ** attempt)
        return wrapper
    return decorator

@retry(times=5)
def fetch_price(symbol): ...
```
**C# comparison:** it's cross-cutting behaviour wrapped around a call — the same job as a
**MediatR pipeline behaviour**, an ASP.NET Core **middleware/filter**, or a **Decorator pattern**
around a service. Saying that connection is a strong answer.

⚠️ **Always use `functools.wraps`** — without it the wrapped function loses its name and docstring,
which breaks logging, introspection and some frameworks.

Class-based decorators and decorators with/without arguments both come up; the pattern above
(three nested levels) is the "with arguments" form.

## 2.4 `functools` essentials
```python
@functools.lru_cache(maxsize=1024)     # memoisation
def yield_curve(date): ...

@functools.cache                        # 3.9+, unbounded lru_cache
partial_fn = functools.partial(compute, rate=0.05)
functools.reduce(operator.add, values, 0)
```
⚠️ `lru_cache` holds strong references to arguments and results — an unbounded cache on a method
keeps `self` alive forever. A real memory-leak source; say so.

---

# PART 3 — OOP & THE OBJECT MODEL

## 3.1 Classes, and the dunder methods that matter
```python
class Order:
    __slots__ = ("id", "symbol", "qty")   # fixed attributes: less memory, no __dict__

    def __init__(self, id, symbol, qty):
        self.id, self.symbol, self.qty = id, symbol, qty

    def __repr__(self):  return f"Order({self.id!r}, {self.symbol!r}, {self.qty})"
    def __eq__(self, other): return isinstance(other, Order) and self.id == other.id
    def __hash__(self):  return hash(self.id)      # MUST match __eq__, same rule as C#
    def __len__(self):   return self.qty
    def __iter__(self):  return iter((self.id, self.symbol))
    def __enter__(self)/__exit__(self, *exc): ...  # context manager
    def __call__(self, *a): ...                     # makes the instance callable
```
⚠️ **Defining `__eq__` sets `__hash__` to `None`** unless you define it too — the object becomes
unhashable. Exactly the C# `Equals`/`GetHashCode` rule, with a sharper failure mode.

## 3.2 `@property`, `@staticmethod`, `@classmethod`
```python
class Position:
    @property
    def market_value(self):            # computed, accessed like an attribute
        return self.qty * self.price

    @classmethod
    def from_dict(cls, d):             # alternative constructor — receives the class
        return cls(**d)

    @staticmethod
    def is_valid(symbol):              # no self/cls — just namespaced
        return bool(symbol)
```

## 3.3 Inheritance & MRO
Python supports multiple inheritance. Method resolution uses **C3 linearisation** — `super()` follows
the **MRO**, not simply "the parent".
```python
Child.__mro__      # shows the exact lookup order
```
Answer for "how do you avoid the diamond problem?" → *"Python resolves it deterministically via the
MRO, but I'd prefer composition or mixins with narrow responsibilities over deep multiple
inheritance."*

## 3.4 Duck typing, ABCs and `Protocol`
```python
from typing import Protocol
class PriceSource(Protocol):           # structural typing — no inheritance needed
    def get_price(self, symbol: str) -> float: ...
```
**C#:** an `interface`, but **structural** — any class with a matching method satisfies it, no
`: IPriceSource` required. `abc.ABC` + `@abstractmethod` is the nominal (C#-like) alternative.

## 3.5 Dataclasses vs Pydantic vs NamedTuple
```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)    # immutable + memory-efficient value object
class Tick:
    symbol: str
    price: Decimal
    ts: datetime
```
| Use | When |
|---|---|
| `@dataclass` | Internal value objects. Stdlib, fast, no validation. |
| `pydantic.BaseModel` | **Boundaries** — API request/response, config, external data. Validates and coerces at runtime (v2 has a Rust core, very fast). |
| `NamedTuple` | Lightweight immutable record, tuple-compatible. |

**Say: "Pydantic at the edges, dataclasses in the core."** That's the idiomatic modern answer.

## 3.6 Descriptors & metaclasses (know *of* them)
- **Descriptor** = an object defining `__get__`/`__set__`; how `@property`, methods and ORM fields
  work under the hood.
- **Metaclass** = the class of a class; controls class creation. Honest answer: *"I know what they
  are and I've read framework code that uses them, but I'd almost never write one — there's usually a
  simpler solution with `__init_subclass__` or a decorator."* **That answer scores better than a
  contrived example.**

---

# PART 4 — MEMORY MANAGEMENT

## 4.1 How Python manages memory
Two mechanisms:
1. **Reference counting** — every object counts references to it; at zero it's freed **immediately**
   (deterministic).
2. **Generational cycle collector** — catches reference *cycles* that counting can't (A→B→A). Three
   generations, like .NET's GC.

**C# comparison:** .NET has **only** a tracing GC. Python's refcounting means most objects die
instantly and predictably — closer to C++ RAII — with a cycle collector as backup.

```python
import sys, gc
sys.getrefcount(obj)     # note: the call itself adds one
gc.collect()             # force a cycle collection
gc.get_referrers(obj)    # who's holding this?
```

## 4.2 Memory leaks in Python
Real causes: unbounded caches/`lru_cache`, module-level globals that grow, closures capturing large
objects, reference cycles involving `__del__`, C-extension leaks, and lingering exception tracebacks
(which hold frames and all their locals alive).
Tools: `tracemalloc` (stdlib snapshots + diff), `objgraph`, `memory_profiler`, `py-spy --dump`.
`weakref` for caches that shouldn't keep objects alive.

## 4.3 `__slots__`
Removes the per-instance `__dict__` — significantly less memory and faster attribute access. Worth it
when you create millions of small objects (ticks, trades). Cost: no dynamic attributes, and multiple
inheritance gets fiddly.

---

# PART 5 — THE GIL & CONCURRENCY ⭐ (the most important section)

## 5.1 The GIL, explained simply

> *"CPython has a Global Interpreter Lock — a single mutex that means only one thread can execute
> Python bytecode at a time. It exists because CPython's memory management is reference-counting,
> which isn't thread-safe, and one coarse lock was far simpler and faster for single-threaded code
> than locking every object. The practical effect: threads don't help CPU-bound Python, but they do
> help I/O-bound Python, because the GIL is released while waiting on I/O — and C extensions like
> NumPy release it during heavy computation."*

## 5.2 The decision table — memorise this

| Workload | Use | Why |
|---|---|---|
| I/O-bound, many concurrent operations | **`asyncio`** | One thread, cooperative, cheapest, scales to thousands |
| I/O-bound with blocking libraries | **`ThreadPoolExecutor`** | GIL released during I/O |
| CPU-bound, pure Python | **`ProcessPoolExecutor`** / `multiprocessing` | Separate interpreters, real parallelism; pays pickling + startup cost |
| CPU-bound, numeric | **NumPy / Pandas / Polars vectorisation**, Numba, Cython | Runs in C, releases the GIL |
| CPU-bound, very heavy | Native extension, or push it to a .NET/C++ service | |

**Currency bonus (say this):** *"Python 3.12 added per-interpreter GILs and 3.13 shipped an
experimental free-threaded build under PEP 703, so this is changing — but for production today I
still design around the GIL."*

## 5.3 asyncio
```python
import asyncio, httpx

async def fetch(client, url):
    r = await client.get(url, timeout=5.0)
    r.raise_for_status()
    return r.json()

async def main(urls):
    sem = asyncio.Semaphore(20)                 # bound the concurrency
    async with httpx.AsyncClient() as client:
        async def guarded(u):
            async with sem:
                return await fetch(client, u)
        async with asyncio.TaskGroup() as tg:   # 3.11+ structured concurrency
            tasks = [tg.create_task(guarded(u)) for u in urls]
    return [t.result() for t in tasks]
```
Key points:
- **Event loop** runs coroutines; `await` yields control back to it.
- `asyncio.gather` (all together) · `as_completed` (stream results) · `wait_for` (timeout) ·
  **`TaskGroup`** (preferred — cancels siblings on failure, no orphan tasks).
- ⚠️ **One blocking call freezes the entire loop.** `time.sleep`, `requests`, a heavy CPU loop — all
  stall every coroutine. Offload with `await asyncio.to_thread(fn, ...)`.
- `asyncio.Queue(maxsize=N)` = producer/consumer **with backpressure** — the direct analogue of
  .NET's `Channel<T>` (`04` §6). **Making that cross-language link is a strong moment.**
- **Cancellation:** `task.cancel()` raises `CancelledError` inside; clean up in `finally`;
  `asyncio.shield` protects a critical section.
- ⚠️ Keep a reference to tasks created with `asyncio.create_task` — otherwise they can be
  garbage-collected mid-flight. A genuinely advanced gotcha.

**C# comparison:** coroutine ≈ `Task`, event loop ≈ the scheduler, `await` ≈ `await`,
`asyncio.gather` ≈ `Task.WhenAll`, `TaskGroup` ≈ structured concurrency. But Python's loop is
**single-threaded**, so blocking it is far more damaging than blocking a .NET thread-pool thread.

## 5.4 threading & multiprocessing
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=16) as ex:      # I/O-bound
    results = list(ex.map(download, urls))

with ProcessPoolExecutor(max_workers=8) as ex:      # CPU-bound
    results = list(ex.map(price_option, contracts))
```
- Locks: `threading.Lock`, `RLock` (reentrant), `Semaphore`, `Event`, `Condition`, `Barrier`.
- ⚠️ **The GIL does not make your code thread-safe.** `x += 1` is read-modify-write across several
  bytecodes and can interleave. You still need locks.
- `queue.Queue` is the thread-safe producer/consumer container.
- Multiprocessing costs: objects are **pickled** between processes; start methods differ (`fork` on
  Linux, `spawn` on Windows/macOS — **on Windows you must guard with `if __name__ == "__main__":`**,
  a classic bug); share big arrays via `multiprocessing.shared_memory` or Arrow instead of copying.

---

# PART 6 — ITERATORS, GENERATORS, COMPREHENSIONS

## 6.1 The iterator protocol
An **iterable** has `__iter__`; an **iterator** has `__next__` and raises `StopIteration` when done.
**C#:** `IEnumerable` / `IEnumerator` — the same split.

## 6.2 Generators — lazy sequences
```python
def read_ticks(path):
    with open(path) as f:
        for line in f:          # lazy — never loads the whole file
            yield parse(line)

for tick in read_ticks("ticks.csv"):   # constant memory over a 50 GB file
    process(tick)
```
**C#:** `yield return`, and it compiles to a state machine in both languages. Generators are the
answer to *"how would you process a file too big for memory?"*

```python
yield from other_generator()    # delegate  (C#: nothing direct; like flattening)
gen = (x * 2 for x in data)     # generator expression — lazy, constant memory
lst = [x * 2 for x in data]     # list comprehension — builds the whole list
```
**Memory hook: square brackets build it now, parentheses build it lazily.**

## 6.3 `itertools` (the ones that appear)
`chain` (concatenate) · `islice` (slice a lazy stream) · `groupby` (⚠️ **requires sorted input** —
famous gotcha) · `product`, `combinations`, `permutations` · `accumulate` (running totals) ·
`zip_longest` · `tee`.

## 6.4 `collections`
`defaultdict(list)` · `Counter` (frequency counts, `.most_common(5)`) · `deque` (**O(1) at both
ends** — the right choice for a rolling window) · `namedtuple` · `OrderedDict` (rarely needed now).

---

# PART 7 — TYPE HINTS

```python
from typing import Optional, Iterable, Callable, TypeVar, Protocol
from decimal import Decimal

T = TypeVar("T")

def largest(items: Iterable[T], key: Callable[[T], float]) -> Optional[T]: ...

def price(symbol: str, qty: int = 1) -> Decimal: ...

# modern syntax (3.10+)
def f(x: int | None) -> list[str]: ...          # replaces Optional[int], List[str]
```
- **Hints are not enforced at runtime.** `mypy` or `pyright` check them statically. **Say this — it's
  the same insight as TypeScript's erased types (`17` §2.1), and drawing that parallel is impressive.**
- Useful: `Protocol` (structural interfaces), `TypedDict`, `Literal["buy","sell"]`, `Final`,
  `NewType`, `Annotated`, `Self` (3.11+), `@overload`.
- ⚠️ Common trap: **`Optional[int]` means `int | None`**, not "optional argument".

---

# PART 8 — ERRORS & CONTEXT MANAGERS

```python
try:
    result = compute()
except (ValueError, KeyError) as e:
    logger.exception("compute failed")     # logs with the traceback
    raise DomainError("bad input") from e  # chain the cause — preserves context
except Exception:
    raise                                   # re-raise, preserving the traceback
else:
    commit()                                # runs only if no exception
finally:
    cleanup()                               # always runs
```
- `raise ... from e` = C#'s inner exception. `raise` bare = C#'s `throw;` (preserves the trace);
  `raise e` re-raises but can muddy the traceback.
- **EAFP vs LBYL** — Python idiom is "Easier to Ask Forgiveness than Permission": just try it and
  catch, rather than checking first. Naming EAFP shows you think in Python, not translated C#.
  ⚠️ But exceptions are relatively cheap in Python — unlike C#, where they're expensive.
- `ExceptionGroup` / `except*` (3.11+) — for `TaskGroup` where several tasks fail at once.
- Custom exceptions: subclass `Exception`, build a small hierarchy per domain.

## Context managers
```python
from contextlib import contextmanager

@contextmanager
def timed(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        logger.info("%s took %.3fs", label, time.perf_counter() - start)

with timed("pricing"):
    run_pricing()
```
**C#:** `using` / `IDisposable`. `async with` for async resources. `contextlib.suppress(FileNotFoundError)`,
`ExitStack` for a dynamic number of resources.

---

# PART 9 — PERFORMANCE

## 9.1 The method (same discipline as `12`)
Measure first. `cProfile` + `snakeviz` for function-level, `line_profiler` for line-level,
**`py-spy`** for a live production process (sampling, attaches without restarting — the one to name),
`timeit` for micro-benchmarks, `tracemalloc`/`memory_profiler` for memory.

## 9.2 The wins, in order
1. **Vectorise** — replace Python loops with NumPy/Pandas operations (10–100×).
2. **Better algorithm/data structure** — `set`/`dict` membership is O(1); `list` membership is O(n).
3. **Avoid work in loops** — hoist lookups, use local variables (attribute lookup is not free).
4. **Generators** instead of building big lists.
5. `join` instead of repeated string `+=`.
6. **Batch I/O** — the database round-trip usually dominates everything else.
7. `__slots__`, and appropriate dtypes in Pandas.
8. **Numba / Cython / Rust extension** for genuinely hot numeric loops.
9. **Parallelise** — processes for CPU, async/threads for I/O.

```python
# 100× difference on a real workload
returns = [(p[i] - p[i-1]) / p[i-1] for i in range(1, len(p))]   # slow Python loop
returns = np.diff(p) / p[:-1]                                     # vectorised, runs in C
```

---

# PART 10 — NUMPY & PANDAS (finance-flavoured)

## 10.1 NumPy essentials
```python
import numpy as np
a = np.array([1.0, 2.0, 3.0])
a.shape, a.dtype                 # arrays are typed and fixed-size — unlike lists
b = a * 2 + 1                    # vectorised: elementwise, no Python loop
a[a > 1.5]                       # boolean masking
np.dot(w, cov @ w)               # matrix maths — portfolio variance
```
- **Broadcasting**: operations between different-shaped arrays expand automatically.
- ⚠️ **Slicing returns a view, not a copy** — mutating the slice mutates the original. Use `.copy()`.
  (Opposite of list slicing — a great detail to point out.)
- `dtype` matters hugely for memory (`float64` vs `float32`, `int8` for flags).

## 10.2 Pandas for market/trade data
```python
import pandas as pd

df = pd.read_parquet("trades.parquet")            # columnar, typed, fast
df["notional"] = df.qty * df.price                # vectorised
pnl = df.groupby("symbol", observed=True)["notional"].sum()

px = df.set_index("ts").sort_index()
bars    = px["price"].resample("1D").ohlc()       # daily OHLC bars
returns = px["price"].pct_change().dropna()
vol_20  = returns.rolling(20).std() * np.sqrt(252)   # annualised realised vol
ewma    = returns.ewm(span=20).std()

# point-in-time join — CRITICAL in finance (avoids lookahead bias)
merged = pd.merge_asof(trades.sort_values("ts"), quotes.sort_values("ts"),
                       on="ts", by="symbol", direction="backward")
```
**Rules to state:**
- **Vectorise; never `iterrows()`.** `apply` is usually a loop in disguise too.
- **Categorical dtype** for symbols, downcast numerics — big memory savings.
- `.loc` for label indexing, `.iloc` for positional. **Chained indexing causes
  `SettingWithCopyWarning`** — use a single `.loc`.
- **Parquet over CSV** — columnar, compressed, typed, supports column pruning and predicate pushdown.
- Know the alternatives: **Polars** (Rust, multi-threaded, lazy — genuinely faster), **DuckDB**
  (in-process columnar SQL over Parquet — excellent for analytics), Dask/Ray for scale-out, Arrow as
  the interchange format. Mentioning Polars/DuckDB signals currency.

⚠️ **Money vs statistics:** Pandas/NumPy are `float64`. Use `decimal.Decimal` or integer minor units
for **money and accounting**; float is fine for **statistics and risk**. This is the same distinction
as `decimal` vs `double` in C# (`03` §11.11) — **making that link across both languages is one of the
strongest single moments available to you in this interview.**

---

# PART 11 — FASTAPI & SERVICES (your ground)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field

class PriceRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=12)
    quantity: int = Field(gt=0)

app = FastAPI()

@app.post("/price", response_model=PriceResponse, status_code=status.HTTP_200_OK)
async def price(req: PriceRequest, svc: Pricer = Depends(get_pricer)):
    try:
        return await svc.compute(req)
    except UnknownSymbol as e:
        raise HTTPException(status_code=404, detail=str(e))
```
- ASGI (`uvicorn`, or gunicorn with uvicorn workers) vs WSGI (Flask/Django classic).
- Pydantic gives validation **and** an OpenAPI schema for free.
- ⚠️ **`def` endpoint → runs in a threadpool; `async def` endpoint → runs on the event loop.** A
  blocking call inside `async def` stalls the whole server. **Very likely senior question.**
- `Depends` for DI, `lifespan` for startup/shutdown, `BackgroundTasks` for fire-and-forget.
- Async DB: `asyncpg` / SQLAlchemy 2.0 async. ⚠️ Never call a sync ORM inside an async handler.

**"How would you call Python from .NET?"** — rank your answer:
1. **HTTP or gRPC service boundary** — versioned contract, independent deploy, runtime isolation.
   **Best**, and it's exactly what your CV already describes at 7X.
2. **Message queue** for async/batch workloads.
3. In-process (`Python.NET`, `CSnakes`) — tighter coupling, drags the GIL into your process. Mention
   as an option you'd avoid unless latency demanded it.

---

# PART 12 — TESTING, TOOLING, SECURITY

**PyTest:** fixtures (with scopes, `conftest.py`), `@pytest.mark.parametrize`, `monkeypatch`,
`pytest-asyncio`, `freezegun` (time), `responses`/`respx` (HTTP), `testcontainers` (real DB),
coverage gates. **`hypothesis`** for property-based testing — *"invariants like put-call parity or
'position after N trades equals the sum of signed quantities' are perfect property tests"* — a
brilliant thing to say for a finance role.

**Tooling:** `ruff` (lint + format, replaces flake8/isort/black), `mypy`/`pyright`, `bandit`
(security), `pyproject.toml`, virtual envs, `uv`/Poetry, pinned lockfiles, `pip-audit`.

**Security:** never `eval`/`exec` on input; `pickle` is **unsafe on untrusted data** (arbitrary code
execution — use JSON); parameterised SQL always; `secrets` not `random` for tokens; validate at the
boundary with Pydantic; keep dependencies patched.

---

# PART 13 — CODING EXERCISES (do 3, timed)

### 13.1 Rolling VWAP in O(1) per tick
```python
from collections import deque

class RollingVwap:
    def __init__(self, size: int):
        self._w, self._size = deque(), size
        self._notional = self._qty = 0.0

    def add(self, price: float, qty: float) -> float:
        self._w.append((price, qty))
        self._notional += price * qty; self._qty += qty
        if len(self._w) > self._size:
            p, q = self._w.popleft()
            self._notional -= p * q; self._qty -= q     # O(1), not O(n)
        return self._notional / self._qty if self._qty else 0.0
```
**Narrate:** `deque` gives O(1) at both ends; running sums avoid recomputing the window.

### 13.2 Group trades and compute P&L
```python
from collections import defaultdict

def realised_pnl(trades):
    pos, cost, pnl = defaultdict(float), defaultdict(float), defaultdict(float)
    for t in trades:
        signed = t.qty if t.side == "BUY" else -t.qty
        if pos[t.symbol] == 0 or (pos[t.symbol] > 0) == (signed > 0):
            new = pos[t.symbol] + signed
            cost[t.symbol] = (cost[t.symbol] * pos[t.symbol] + t.price * signed) / new
            pos[t.symbol] = new
        else:
            closing = min(abs(signed), abs(pos[t.symbol]))
            pnl[t.symbol] += (t.price - cost[t.symbol]) * closing * (1 if pos[t.symbol] > 0 else -1)
            pos[t.symbol] += signed
    return dict(pnl)
```

### 13.3 Stream a huge file without loading it
```python
def largest_trades(path, n=10):
    import heapq
    with open(path) as f:
        return heapq.nlargest(n, (parse(line) for line in f), key=lambda t: t.notional)
```
**Say:** generator = constant memory; `heapq.nlargest` = O(n log k), not a full sort.

### 13.4 Async fan-out with bounded concurrency
See §5.3 — be able to write it from memory with the semaphore and `TaskGroup`.

### 13.5 Write a decorator that times and logs a function
See §2.3 — do it with `functools.wraps` and mention why.

---

# PART 14 — 60 RAPID-FIRE (cover the answers)

| # | Q | A |
|---|---|---|
| 1 | List vs tuple | Mutable vs immutable; tuples are hashable |
| 2 | Dict ordered? | Yes, insertion-ordered since 3.7 |
| 3 | `is` vs `==` | Identity vs value; `is` only for None/True/False |
| 4 | Why does `257 is 257` differ from `256 is 256`? | Small-int caching (−5..256) |
| 5 | Mutable default arg | Evaluated once at def time — use `None` |
| 6 | Shallow vs deep copy | `copy.copy` vs `copy.deepcopy` |
| 7 | Is Python pass-by-value or reference? | Pass by object reference; rebinding ≠ mutating |
| 8 | What is the GIL | One thread executes bytecode at a time |
| 9 | Why does the GIL exist | Reference counting isn't thread-safe; one coarse lock was simpler/faster |
| 10 | CPU-bound → | Processes, or C extensions that release the GIL |
| 11 | I/O-bound → | asyncio or threads |
| 12 | Does the GIL make code thread-safe? | **No** — `x += 1` still races |
| 13 | asyncio blocking call | Freezes the whole loop → `asyncio.to_thread` |
| 14 | `gather` vs `TaskGroup` | Prefer TaskGroup (3.11+): structured, cancels siblings |
| 15 | Backpressure in asyncio | `asyncio.Queue(maxsize=N)` — the `Channel<T>` analogue |
| 16 | multiprocessing cost | Pickling + process startup; `spawn` on Windows needs `__main__` guard |
| 17 | Generator vs list comp | Lazy `()` vs eager `[]` |
| 18 | `yield` | Produces a lazy sequence via a state machine (C# `yield return`) |
| 19 | Iterator protocol | `__iter__` + `__next__` + `StopIteration` |
| 20 | `itertools.groupby` gotcha | Requires sorted input |
| 21 | `deque` | O(1) at both ends — rolling windows |
| 22 | `Counter` | Frequency counting + `.most_common()` |
| 23 | `defaultdict` | Auto-creates missing values |
| 24 | Decorator | A function taking and returning a function; `@x` is `f = x(f)` |
| 25 | Why `functools.wraps` | Preserves name/docstring/signature |
| 26 | `lru_cache` risk | Holds strong references — unbounded caches leak |
| 27 | Closure + `nonlocal` | Needed to assign to an enclosing variable |
| 28 | Late binding in loops | `lambda i=i:` to bind now |
| 29 | `*args` / `**kwargs` | Var-positional / var-keyword |
| 30 | `staticmethod` vs `classmethod` | No implicit arg vs receives `cls` (alt constructors) |
| 31 | `@property` | Computed attribute; implemented via descriptors |
| 32 | `__slots__` | No `__dict__` — less memory, faster access, no dynamic attrs |
| 33 | `__eq__` without `__hash__` | Object becomes unhashable |
| 34 | MRO | C3 linearisation; `super()` follows it |
| 35 | Duck typing | If it has the method, it works |
| 36 | `Protocol` vs `ABC` | Structural vs nominal interfaces |
| 37 | Dataclass vs Pydantic | Internal value objects vs validated boundaries |
| 38 | Are type hints enforced? | **No** — static only (mypy/pyright), like TypeScript |
| 39 | `Optional[int]` means | `int \| None` |
| 40 | How is memory managed? | Reference counting + generational cycle collector |
| 41 | Reference cycle | Refcount never hits zero; the cycle GC collects it |
| 42 | Find a memory leak | `tracemalloc` snapshots + diff; `objgraph`; check caches/globals |
| 43 | `weakref` | A reference that doesn't keep the object alive |
| 44 | EAFP vs LBYL | Try/except vs check-first; EAFP is the Python idiom |
| 45 | `raise` vs `raise e` vs `raise X from e` | Preserve / re-raise / chain the cause |
| 46 | `try/else/finally` | `else` only if no exception; `finally` always |
| 47 | Context manager | `__enter__`/`__exit__` — Python's `using` |
| 48 | `@contextmanager` | Turns a generator into a context manager |
| 49 | Vectorise | Replace Python loops with NumPy/Pandas — 10–100× |
| 50 | NumPy slice | Returns a **view**, not a copy (unlike lists) |
| 51 | `iterrows()` | Avoid — it's a slow Python loop |
| 52 | `SettingWithCopyWarning` | Chained indexing — use a single `.loc` |
| 53 | Parquet vs CSV | Columnar, typed, compressed, column pruning |
| 54 | `merge_asof` | Point-in-time join — avoids lookahead bias |
| 55 | Money in Python | `Decimal` or integer minor units — **never float** |
| 56 | `def` vs `async def` in FastAPI | Threadpool vs event loop — don't block the loop |
| 57 | Profiling tools | `cProfile`, `line_profiler`, **`py-spy`** (live process) |
| 58 | `pickle` risk | Arbitrary code execution — never on untrusted data |
| 59 | GIL future | Per-interpreter GILs (3.12), free-threaded build (3.13, experimental) |
| 60 | Python's role in a .NET shop | Analytics/quant/ML/data behind a versioned service contract |

---

# PART 15 — THE 6 ANSWERS THAT MAKE YOU SOUND "ADVANCED"

1. **The GIL decision table** (§5.2) — delivered calmly, with the free-threading update.
2. **"One blocking call freezes the whole event loop"** — and `asyncio.to_thread` as the fix.
3. **"`asyncio.Queue(maxsize=N)` is Python's `Channel<T>`"** — bounded queue = backpressure, the same
   pattern in both languages.
4. **"Type hints are erased at runtime, exactly like TypeScript — so validate at the boundary with
   Pydantic."**
5. **"`Decimal` for money, float for statistics"** — and the same rule in C# and SQL.
6. **"Pydantic at the edges, dataclasses in the core; Python behind a versioned service contract so
   the .NET domain stays authoritative."** — architectural, and true of your actual work.
