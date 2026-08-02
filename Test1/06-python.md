# 06 — PYTHON, IN PLAIN ENGLISH

> **How to use this file**
>
> Every item is written the same way:
>
> **Q:** the question they ask
> **Say:** the exact words you speak (short — say it, then stop)
> **Remember:** a one-line hook so it sticks
>
> Read the **Say** lines out loud. Reading silently does not stick; speaking does.
>
> **If you only have 30 minutes:** read Part 0, then Part 5 (the GIL), then Part 16 (rapid-fire).

---

# PART 0 — THE 10 PYTHON ANSWERS THAT WIN

If you remember nothing else, remember these ten. Each one is a full answer on its own.

| # | The question | The answer, in one breath |
|---|---|---|
| 1 | **What is the GIL?** | "Only one thread can run Python code at a time. So threads help with waiting (network, disk), but not with heavy maths. For heavy maths I use processes, or NumPy — which drops the lock and runs in C." |
| 2 | **CPU work vs waiting work?** | "**Waiting → asyncio or threads. Working → processes or NumPy.**" |
| 3 | **The asyncio trap** | "One blocking call freezes everything. It's one thread. If I must call something slow and blocking, I push it out with `asyncio.to_thread`." |
| 4 | **Money** | "Never float. `Decimal`, or whole pennies as integers. Float is fine for statistics, never for cash." |
| 5 | **Mutable default argument** | "`def f(x, items=[])` is a bug. The list is made once, when the function is defined, and every call shares it. Use `None` and create it inside." |
| 6 | **`is` vs `==`** | "`==` asks 'same value'. `is` asks 'literally the same object'. Only use `is` for `None`, `True`, `False`." |
| 7 | **Type hints** | "They're not checked when the code runs. They're erased. Exactly like TypeScript. So I validate real data at the edges with Pydantic." |
| 8 | **Big file / big data** | "Generators. `yield` one row at a time, constant memory, no matter how big the file is." |
| 9 | **Slow pandas** | "Never loop over rows. Vectorise — one operation over the whole column. It's 10 to 100 times faster because it runs in C." |
| 10 | **Python in a .NET shop** | "Python does analytics, quant and ML. It sits behind a versioned HTTP or gRPC contract, so .NET stays the system of record." |

---

# PART 1 — THE BASICS, EXPLAINED SIMPLY

## 1.1 Everything is an object, and names are labels

Think of a variable as a **sticky label**, not a box.

```python
x = [1, 2, 3]
y = x           # you stuck a SECOND label on the SAME list
y.append(4)
print(x)        # [1, 2, 3, 4]  — one list, two labels
```

**Say:** *"In Python a variable is a name pointing at an object. Two names can point at the same object. So changing it through one name shows up in the other."*

**Remember:** **Labels, not boxes.**

**Coming from C#:** everything behaves like a reference type. There are no structs.

---

## 1.2 Mutable vs immutable — the idea everything else rests on

**Immutable** = cannot be changed. You get a new object instead.
**Mutable** = can be changed in place.

| Cannot change | Can change |
|---|---|
| `int`, `float`, `str`, `bool`, `tuple`, `frozenset`, `bytes` | `list`, `dict`, `set`, `bytearray`, your own classes |

```python
s = "hello"
s += " world"     # this made a NEW string. The old one is thrown away.
```

**Q: Why does this matter?**
**Say:** *"Only immutable things can be dictionary keys or go in a set, because they're hashable. A tuple can be a key. A list cannot."*

**Remember:** **Can't change it → can be a key.**

---

## 1.3 The mutable default argument (asked constantly)

```python
def add(item, bucket=[]):     # BUG
    bucket.append(item)
    return bucket

add(1)   # [1]
add(2)   # [1, 2]   <- the same list came back!
```

**Why:** the `[]` is created **once**, when Python reads the `def` line. Not on each call.

```python
def add(item, bucket=None):   # FIX
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

**Say:** *"Defaults are evaluated once at definition time, not per call. So a mutable default is shared by every call. The fix is `None` plus create it inside."*

**Remember:** **Defaults are made once. Never default to `[]` or `{}`.**

---

## 1.4 `is` vs `==`

- `==` → **same value?**
- `is` → **same object in memory?**

```python
a = 256; b = 256; a is b     # True
a = 257; b = 257; a is b     # False
```

**Why the weirdness:** Python pre-makes the small integers −5 to 256 and reuses them. It's an optimisation, not a rule.

**Say:** *"`==` is value, `is` is identity. I only use `is` for `None`, `True`, `False` and sentinel objects. Small integers are cached, which makes `is` look like it works by accident."*

**Remember:** **`is` is only ever for `None`.**

---

## 1.5 Copying

```python
import copy

b = a                 # not a copy at all — same object, second label
b = a[:]              # shallow copy of a list
b = list(a)           # shallow copy
b = copy.copy(a)      # shallow copy
b = copy.deepcopy(a)  # full copy, all the way down
```

**Shallow** = new outer container, **same inner objects**.
**Deep** = everything copied recursively.

**Say:** *"A shallow copy gives me a new list but the items inside are still shared. If the items are mutable and I'll change them, I need `deepcopy`."*

**Remember:** **Shallow copies the shelf, not the books.**

---

## 1.6 The containers you need to know

| Type | What it is | Speed | Use it for |
|---|---|---|---|
| `list` | Ordered, changeable | index fast, `in` **slow** (checks each item) | A sequence of things |
| `tuple` | Ordered, **fixed** | same | A record; a dictionary key |
| `dict` | Key → value | lookup **fast** | Lookups by ID |
| `set` | Unique items, no order | `in` **fast** | "Have I seen this?" / dedupe |
| `frozenset` | A set you can't change | | A set used as a key |
| `str` | Text, fixed | | |

**Q: `x in my_list` vs `x in my_set`?**
**Say:** *"A list has to walk every item — that's O(n). A set hashes straight to the answer — that's O(1). If I'm checking membership in a loop, I convert to a set first. That single change often takes a function from minutes to seconds."*

**Remember:** **Checking membership? Use a set.**

---

## 1.7 Slicing

```python
xs[2:5]     # items 2, 3, 4   (stop is NOT included)
xs[:3]      # first three
xs[-1]      # last one
xs[-2:]     # last two
xs[::-1]    # reversed copy
xs[::2]     # every second item
```

**Remember:** **`start:stop:step` — stop is never included.**

Important detail worth saying unprompted: **slicing a list gives you a copy. Slicing a NumPy array gives you a view onto the same memory.** Change the NumPy slice and you change the original.

---

## 1.8 Truthy and falsy

These count as **False**: `False`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None`.
Everything else is True.

```python
if not orders:        # good — "if the list is empty"
if not count:         # BUG if 0 is a real value!
if count is None:     # correct
```

**Remember:** **Empty means false. So does zero — that's the bug.**

---

## 1.9 The everyday tools

```python
for i, item in enumerate(items, start=1):   # index + value
for a, b in zip(list_a, list_b):            # walk two lists together

sorted(trades, key=lambda t: t.price, reverse=True)   # returns a NEW list
trades.sort(key=lambda t: t.price)                    # sorts in place, returns None

any(t.qty > 100 for t in trades)     # is at least one true?
all(t.price > 0 for t in trades)     # are they all true?
sum(t.qty for t in trades)
max(trades, key=lambda t: t.notional)

", ".join(names)          # join a list into a string
"a,b,c".split(",")        # split a string into a list
```

**Q: `sorted()` vs `.sort()`?**
**Say:** *"`sorted` returns a new list and works on anything iterable. `.sort()` changes the list in place and returns `None` — assigning its result is a classic bug. Both are stable, so equal items keep their original order."*

**Remember:** **`sorted` gives back. `.sort()` changes in place and gives `None`.**

---

## 1.10 f-strings

```python
f"{price:,.2f}"      # 1,234.57  — thousands separator, 2 decimals
f"{ratio:.1%}"       # 12.3%
f"{value=}"          # value=42  — debug shortcut
f"{name:>10}"        # right-aligned in 10 characters
```

---

## 1.11 The walrus operator and `match` (shows you're current)

```python
if (n := len(data)) > 100:        # assign AND test in one go
    print(f"{n} rows is a lot")

match event:                       # Python 3.10+ — structural pattern matching
    case {"type": "trade", "qty": qty} if qty > 0:
        book(qty)
    case {"type": "cancel"}:
        cancel()
    case _:
        ignore()
```

**Say:** *"`match` is structural pattern matching — it destructures as well as compares, so it's closer to C#'s pattern matching than to a switch."*

---

# PART 2 — FUNCTIONS, CLOSURES, DECORATORS

## 2.1 Arguments

```python
def f(a, b=2, *args, key=None, **kwargs): ...
#     |   |      |        |         |
#     |   |      |        |         +-- any extra named args, as a dict
#     |   |      |        +------------ must be passed by name
#     |   |      +--------------------- any extra positional args, as a tuple
#     |   +---------------------------- has a default
#     +-------------------------------- required
```

**Q: Is Python pass-by-value or pass-by-reference?**
**Say:** *"Neither, exactly. It passes the object. If I rebind the parameter inside, the caller sees nothing. If I mutate the object, the caller sees it. So: rebinding is private, mutating is shared."*

**Remember:** **Rebind = private. Mutate = shared.**

---

## 2.2 Closures

A closure is a function that **remembers the variables around it**, even after the outer function has ended.

```python
def make_counter():
    count = 0
    def inc():
        nonlocal count      # without this: UnboundLocalError
        count += 1
        return count
    return inc

next_id = make_counter()
next_id()   # 1
next_id()   # 2
```

**Why `nonlocal`:** assigning to a name inside a function makes it *local* by default. `nonlocal` says "no, use the one from the enclosing function". `global` does the same for module level.

**The loop trap:**
```python
fns = [lambda: i for i in range(3)]
[f() for f in fns]                   # [2, 2, 2]  — they all see the FINAL i
fns = [lambda i=i: i for i in range(3)]   # fix: capture now via a default
```

**Remember:** **Closures capture the variable, not its value at the time.**

---

## 2.3 Decorators

**Say first, plainly:** *"A decorator is a function that takes a function and returns a new function that wraps it. `@thing` above a function is just shorthand for `f = thing(f)`."*

```python
import functools, time

def timed(fn):
    @functools.wraps(fn)              # keeps the original name and docstring
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            print(f"{fn.__name__} took {time.perf_counter() - start:.3f}s")
    return wrapper

@timed
def price_book(): ...
```

A decorator **that takes arguments** needs three layers:

```python
def retry(times=3, backoff=0.2):
    def decorator(fn):
        @functools.wraps(fn)
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

**Q: Why `functools.wraps`?**
**Say:** *"Without it the wrapper replaces the original's name, docstring and signature. That breaks logging, documentation and anything that inspects the function — including some frameworks."*

**Q: What's this in C# terms?** (say this — it lands well)
**Say:** *"It's the same job as a MediatR pipeline behaviour, an ASP.NET middleware or filter, or the Decorator pattern around a service. Cross-cutting concerns wrapped around a call."*

**Remember:** **`@x` means `f = x(f)`. Always `functools.wraps`.**

---

## 2.4 `functools`

```python
@functools.lru_cache(maxsize=1024)     # remembers results by argument
def yield_curve(date): ...

@functools.cache                       # 3.9+, same but unlimited
partial_price = functools.partial(price, currency="USD")   # pre-fill an argument
```

**The gotcha to raise yourself:** *"`lru_cache` holds strong references to the arguments and the results. An unbounded cache on a method keeps `self` alive forever — that's a real memory leak, and I've seen it in production."*

---

# PART 3 — CLASSES AND OBJECTS

## 3.1 A class, with the parts that matter

```python
class Order:
    exchange = "LSE"                # CLASS variable — shared by every instance

    def __init__(self, id, symbol, qty):
        self.id = id                # INSTANCE variables — one per object
        self.symbol = symbol
        self.qty = qty

    def __repr__(self):                     # for developers / debugging
        return f"Order({self.id!r}, {self.symbol!r}, {self.qty})"

    def __str__(self):                      # for users / printing
        return f"{self.qty} {self.symbol}"

    def __eq__(self, other):
        return isinstance(other, Order) and self.id == other.id

    def __hash__(self):                     # MUST be defined if __eq__ is
        return hash(self.id)
```

**Q: Class variable vs instance variable?** *(commonly asked, easy to fumble)*
**Say:** *"A class variable is shared by all instances — it lives on the class. An instance variable belongs to one object. The trap is a mutable class variable, like a list: every instance appends to the same list. Same bug as the mutable default argument."*

**Q: `__str__` vs `__repr__`?**
**Say:** *"`__str__` is the friendly version for users — that's what `print` uses. `__repr__` is the unambiguous version for developers — that's what the REPL and the debugger show, and what you see inside a list. If I only write one, I write `__repr__`, because `str` falls back to it."*

**Remember:** **`repr` = for me. `str` = for them.**

**Q: What happens if I define `__eq__` and not `__hash__`?**
**Say:** *"Python sets `__hash__` to `None` and the object becomes unhashable — it can't go in a set or be a dict key. It's exactly the C# rule that if you override `Equals` you must override `GetHashCode`, but with a louder failure."*

---

## 3.2 `@property`, `@staticmethod`, `@classmethod`

```python
class Position:
    @property
    def market_value(self):          # looks like an attribute, runs like a method
        return self.qty * self.price

    @classmethod
    def from_dict(cls, d):           # receives the CLASS — alternative constructor
        return cls(**d)

    @staticmethod
    def is_valid(symbol):            # receives nothing — just lives here for tidiness
        return bool(symbol)
```

**Say:** *"`@property` is a computed attribute — no brackets when you read it. `@classmethod` gets the class, so it's how you write alternative constructors like `from_dict`. `@staticmethod` gets neither — it's a plain function grouped with the class."*

**Remember:** **property = computed. classmethod = alternative constructor. staticmethod = just filed here.**

---

## 3.3 Inheritance and `super()`

```python
class Equity(Instrument):
    def __init__(self, symbol, sector):
        super().__init__(symbol)        # call the parent's __init__
        self.sector = sector
```

**Q: Python has multiple inheritance. What about the diamond problem?**
**Say:** *"Python resolves it deterministically using the MRO — the method resolution order, computed by C3 linearisation. You can see it with `Child.__mro__`, and `super()` walks that order rather than simply going to 'the parent'. But in practice I'd prefer composition, or narrow mixins, over deep multiple inheritance."*

**Remember:** **`super()` follows the MRO, not 'the parent'.**

---

## 3.4 Private, protected — the conventions

```python
self.public      # anyone
self._internal   # convention: "please don't touch". Nothing enforces it.
self.__private   # name mangling: becomes _ClassName__private
```

**Say:** *"Python has no real access modifiers. A single underscore is a convention meaning internal. A double underscore triggers name mangling, which exists to avoid collisions in subclasses, not to provide security. The culture is 'we're all adults here'."*

---

## 3.5 Duck typing, `Protocol` and `ABC`

```python
from typing import Protocol

class PriceSource(Protocol):                 # structural — no inheritance needed
    def get_price(self, symbol: str) -> float: ...

from abc import ABC, abstractmethod

class Repo(ABC):                             # nominal — you must inherit
    @abstractmethod
    def save(self, x): ...
```

**Say:** *"Duck typing means: if it has the method, it works — Python doesn't check the declared type. `Protocol` is a structural interface: any class with a matching method satisfies it, no inheritance required. `ABC` with `@abstractmethod` is the nominal version, closer to a C# interface. I use `Protocol` for boundaries I don't own and `ABC` when I want to force a contract."*

**Remember:** **Protocol = shape. ABC = family tree.**

---

## 3.6 Dataclasses vs Pydantic vs NamedTuple

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)     # immutable + memory-efficient
class Tick:
    symbol: str
    price: Decimal
    ts: datetime
```

| Use | When |
|---|---|
| `@dataclass` | Internal value objects. Standard library, fast, **no validation**. |
| `pydantic.BaseModel` | **The edges** — API requests, config, anything from outside. Validates and converts at runtime. |
| `NamedTuple` | A tiny immutable record that also behaves like a tuple. |

**Say the line:** *"Pydantic at the edges, dataclasses in the core."*

---

## 3.7 `__slots__`

**Say:** *"By default every instance carries a dictionary of its attributes. `__slots__` removes that — less memory and faster attribute access. It's worth it when you make millions of small objects like ticks or trades. The cost is that you can't add attributes dynamically."*

---

## 3.8 Descriptors and metaclasses

**Say (this honest answer scores better than a contrived example):**
*"A descriptor is an object with `__get__` and `__set__` — it's how `@property`, methods and ORM fields work underneath. A metaclass is the class of a class; it controls how classes are made. I know what they are and I've read framework code that uses them, but I'd almost never write one — `__init_subclass__` or a decorator is usually simpler and easier for the next person to read."*

---

# PART 4 — MEMORY

## 4.1 How Python frees memory

Two mechanisms:

1. **Reference counting.** Every object counts how many names point at it. When the count hits zero it is freed **immediately**.
2. **Cycle collector.** Reference counting can't free A→B→A. A generational collector sweeps those up periodically.

**Say:** *"Python counts references, so most objects die the instant the last name goes away — that's deterministic, more like C++ than .NET. The generational garbage collector is a backup that only exists to break reference cycles. .NET, by contrast, has only a tracing collector."*

**Remember:** **Counting first, cycle collector as backup.**

## 4.2 Where leaks come from

- Caches that never evict — especially `lru_cache` with no `maxsize`
- Module-level globals that keep growing
- Closures holding on to something large
- Reference cycles involving `__del__`
- Exception tracebacks kept alive (they hold every local in every frame)

**Tools to name:** `tracemalloc` (take two snapshots and diff them), `objgraph`, `memory_profiler`, `py-spy --dump` on a live process. `weakref` for a cache that shouldn't keep things alive.

---

# PART 5 — THE GIL AND CONCURRENCY ⭐ (the most important part)

## 5.1 The GIL in plain words

**Say exactly this:**

> *"CPython has a Global Interpreter Lock — one lock that means only one thread can execute Python bytecode at a time. It exists because memory is managed by reference counting, and updating those counts isn't thread-safe. One coarse lock was far simpler and faster for single-threaded code than locking every object.*
>
> *The practical effect: threads don't speed up heavy computation, but they do help when you're waiting — because the lock is released during I/O. And C extensions like NumPy release it while they compute."*

**Remember:** **One lock. Waiting is fine, computing is not.**

## 5.2 The decision table — memorise this

| What you're doing | Use | Why |
|---|---|---|
| **Waiting** on lots of network calls | **`asyncio`** | One thread, cheapest, scales to thousands |
| **Waiting**, but the library is blocking | **`ThreadPoolExecutor`** | The lock is released while waiting |
| **Computing**, plain Python | **`ProcessPoolExecutor`** | Separate processes = real parallelism. Costs pickling + startup. |
| **Computing**, numbers | **NumPy / Pandas / Polars** | Runs in C and releases the lock |
| **Computing**, extremely heavy | Native extension, or hand it to .NET/C++ | |

**The currency line (say it):** *"Python 3.12 added per-interpreter GILs and 3.13 shipped an experimental free-threaded build under PEP 703. So this is genuinely changing — but for anything in production today I still design around the GIL."*

## 5.3 asyncio

```python
import asyncio, httpx

async def fetch(client, url):
    r = await client.get(url, timeout=5.0)
    r.raise_for_status()
    return r.json()

async def main(urls):
    sem = asyncio.Semaphore(20)                  # never more than 20 at once
    async with httpx.AsyncClient() as client:
        async def guarded(u):
            async with sem:
                return await fetch(client, u)
        async with asyncio.TaskGroup() as tg:    # 3.11+ — structured concurrency
            tasks = [tg.create_task(guarded(u)) for u in urls]
    return [t.result() for t in tasks]
```

**How to explain it simply:**
*"There's one thread and an event loop. `await` means 'I'm going to wait — take someone else off the queue'. When my result arrives, the loop comes back to me. It's cooperative: nobody is interrupted, they hand control back voluntarily."*

**The four things to know:**

1. **One blocking call freezes everything.** `time.sleep`, `requests`, a heavy loop — all of them stall every other coroutine. Fix: `await asyncio.to_thread(slow_fn, ...)`.
2. **`TaskGroup` over `gather`.** TaskGroup cancels its siblings when one fails, and can't leave orphan tasks behind.
3. **`asyncio.Queue(maxsize=N)` is backpressure.** When the queue is full, the producer waits. *"This is the direct equivalent of .NET's bounded `Channel<T>`."* ← **say this, it's a strong moment**
4. **Keep a reference to `create_task` results.** The loop only holds a weak reference, so an unreferenced task can be garbage-collected mid-flight. A genuinely advanced gotcha.

**C# mapping:** coroutine ≈ `Task` · event loop ≈ scheduler · `gather` ≈ `Task.WhenAll` · `TaskGroup` ≈ structured concurrency. **But** Python's loop is single-threaded, so blocking it is much worse than blocking a .NET thread-pool thread.

## 5.4 Threads and processes

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=16) as ex:      # waiting work
    results = list(ex.map(download, urls))

with ProcessPoolExecutor(max_workers=8) as ex:      # computing work
    results = list(ex.map(price_option, contracts))
```

**Q: Does the GIL make my code thread-safe?**
**Say:** *"No, and this is the misunderstanding. `x += 1` is read, modify, write — several bytecodes — and a thread switch can land in the middle. You still need locks."*

**Remember:** **The GIL protects the interpreter, not your data.**

**Process costs, all worth mentioning:**
- Objects are **pickled** to cross the process boundary — that's real overhead.
- Linux forks, **Windows and macOS spawn**. On spawn, the module is re-imported, so **you must guard with `if __name__ == "__main__":`** or you'll fork bomb yourself. Classic bug.
- Don't copy big arrays — use `multiprocessing.shared_memory` or Arrow.

**Locks available:** `Lock`, `RLock` (re-entrant), `Semaphore` (N at a time), `Event` (a flag to wait on), `Condition`, `Barrier`. `queue.Queue` is the thread-safe producer/consumer.

---

# PART 6 — GENERATORS AND ITERATORS

## 6.1 The protocol

An **iterable** has `__iter__`. An **iterator** has `__next__` and raises `StopIteration` when it's done.
**C#:** `IEnumerable` and `IEnumerator`. Same split.

## 6.2 Generators — the answer to "the file is too big for memory"

```python
def read_ticks(path):
    with open(path) as f:
        for line in f:          # lazy — never loads the whole file
            yield parse(line)

for tick in read_ticks("50gb.csv"):
    process(tick)               # constant memory
```

**Say:** *"A generator produces values one at a time instead of building a list. Memory stays flat regardless of input size. It's exactly `yield return` in C#, and both compile to a state machine."*

```python
gen = (x * 2 for x in data)     # generator expression — lazy
lst = [x * 2 for x in data]     # list comprehension — builds the whole thing now
```

**Remember:** **Square brackets build it now. Round brackets build it lazily.**

**Q: Generator vs iterator?**
**Say:** *"A generator is just the easy way to write an iterator. Any function with `yield` in it returns a generator, and generators implement the iterator protocol for free."*

## 6.3 `itertools` and `collections`

```python
from itertools import chain, islice, groupby, accumulate, product, combinations

chain(a, b)          # glue sequences together
islice(gen, 10)      # take 10 from a lazy stream
groupby(rows, key)   # WARNING: needs SORTED input — famous gotcha
accumulate(values)   # running totals
```

```python
from collections import defaultdict, Counter, deque, namedtuple

defaultdict(list)    # missing keys create themselves
Counter(symbols)     # frequency counts; .most_common(5)
deque(maxlen=20)     # FAST at BOTH ends — the right tool for a rolling window
```

**Remember:** **`deque` for rolling windows. `Counter` for counting. `defaultdict` to skip the "if key not in" dance.**

## 6.4 `heapq` and `bisect` (worth knowing, often missed)

```python
import heapq
heapq.nlargest(10, trades, key=lambda t: t.notional)   # O(n log k), not a full sort
heapq.heappush(h, item); heapq.heappop(h)              # a priority queue

import bisect
bisect.insort(sorted_prices, p)          # insert while keeping sorted
i = bisect.bisect_left(sorted_ts, target)  # binary search — O(log n)
```

---

# PART 7 — TYPE HINTS

```python
from typing import Optional, Iterable, Callable, TypeVar, Protocol
from decimal import Decimal

def price(symbol: str, qty: int = 1) -> Decimal: ...

def f(x: int | None) -> list[str]: ...        # modern syntax, 3.10+
```

**Q: Are type hints enforced?**
**Say:** *"No. They're erased at runtime — Python won't stop you passing the wrong thing. They exist for the editor and for `mypy` or `pyright` in CI. It's exactly the same model as TypeScript, which is why you validate real external data at the boundary with Pydantic."*

**Remember:** **Hints are documentation the tools can check. Not a runtime guard.**

**Useful ones:** `Protocol` (structural interface), `TypedDict` (a dict with a known shape), `Literal["buy","sell"]`, `Final`, `Annotated`, `Self` (3.11+), `@overload`.

**Trap:** `Optional[int]` means `int | None`. It does **not** mean "optional argument".

---

# PART 8 — ERRORS AND CONTEXT MANAGERS

```python
try:
    result = compute()
except (ValueError, KeyError) as e:
    logger.exception("compute failed")       # logs WITH the traceback
    raise DomainError("bad input") from e    # chain the cause
except Exception:
    raise                                    # re-raise, traceback intact
else:
    commit()                                 # only if nothing was raised
finally:
    cleanup()                                # always
```

| You write | It means |
|---|---|
| `raise` (bare) | Re-throw, keep the original traceback. C#'s `throw;` |
| `raise e` | Re-throw, but you can lose context |
| `raise New() from e` | New exception, original attached as the cause. C#'s inner exception |

**Q: EAFP vs LBYL?**
**Say:** *"'Easier to Ask Forgiveness than Permission' — just try it and catch the failure, rather than checking first. That's the Python idiom, partly because exceptions here are cheap, unlike in C# where they're expensive. Naming it EAFP shows you think in Python rather than translated C#."*

**3.11+:** `ExceptionGroup` and `except*` — for when several tasks in a `TaskGroup` fail at once.

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

**Say:** *"A context manager guarantees cleanup. `__enter__` sets up, `__exit__` tears down, and it runs even if an exception is thrown. It's `using` and `IDisposable` in C#. `@contextmanager` lets me write one as a generator — everything before the `yield` is setup, everything after is cleanup."*

Also worth naming: `contextlib.suppress(FileNotFoundError)`, `ExitStack` for a variable number of resources, `async with` for async ones.

---

# PART 9 — DATES, TIMES AND MONEY (finance-critical, was missing)

```python
from datetime import datetime, timezone, date
from zoneinfo import ZoneInfo          # standard library since 3.9
from decimal import Decimal, ROUND_HALF_UP

datetime.now(timezone.utc)             # ALWAYS do this
datetime.utcnow()                      # DON'T — returns a naive datetime, no tzinfo

ny = datetime.now(ZoneInfo("America/New_York"))
utc = ny.astimezone(timezone.utc)

Decimal("0.1") + Decimal("0.2")        # exactly 0.3
0.1 + 0.2                              # 0.30000000000000004
Decimal("1.005").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

**Say:** *"Store and compute in UTC, convert to local only for display. Use timezone-aware datetimes everywhere — `utcnow()` is a trap because it gives you a naive datetime that looks like UTC but isn't tagged, so comparisons go wrong silently. And for money: `Decimal` constructed from a string, never from a float, with explicit rounding. Same rule as `decimal` in C# and `DECIMAL` in SQL."*

**Remember:** **UTC in the system, local at the edge. `Decimal("0.1")`, never `Decimal(0.1)`.**

---

# PART 10 — PERFORMANCE

## 10.1 The method

**Say:** *"Measure first, always. `cProfile` for function-level, `line_profiler` for line-level, and `py-spy` for a live production process — it samples and attaches without a restart, which matters when you can't reproduce it locally. Then fix one thing and measure again."*

## 10.2 The wins, in order

1. **Vectorise** — replace Python loops with NumPy/Pandas. 10–100×.
2. **Better data structure** — `set`/`dict` lookup is O(1), `list` lookup is O(n).
3. **Hoist work out of loops** — attribute lookup isn't free.
4. **Generators** instead of building giant lists.
5. **`"".join(parts)`** instead of `s += x` in a loop.
6. **Batch your I/O** — the database round-trip usually dominates everything else.
7. `__slots__`, and right-sized dtypes in Pandas.
8. **Numba / Cython / Rust extension** for a genuinely hot numeric loop.
9. **Parallelise** — processes for computing, async/threads for waiting.

```python
returns = [(p[i] - p[i-1]) / p[i-1] for i in range(1, len(p))]   # slow
returns = np.diff(p) / p[:-1]                                    # ~100× faster
```

---

# PART 11 — NUMPY AND PANDAS

## 11.1 NumPy

```python
import numpy as np
a = np.array([1.0, 2.0, 3.0])
b = a * 2 + 1              # applies to every element, no Python loop
a[a > 1.5]                 # boolean mask — pick the ones that match
w @ cov @ w                # matrix maths — portfolio variance
```

**Say:** *"A NumPy array is typed and fixed-size, stored as one contiguous block. That's why it's fast — the loop happens in C, and it releases the GIL while it does."*

**Two things to raise yourself:**
- **Slicing gives a view, not a copy.** Change the slice, change the original. Use `.copy()` if you don't want that. *(The opposite of list slicing — a nice detail to point out.)*
- **`dtype` matters enormously** for memory. `float32` is half the size of `float64`.

## 11.2 Pandas for market data

```python
import pandas as pd

df = pd.read_parquet("trades.parquet")
df["notional"] = df.qty * df.price                # vectorised
pnl = df.groupby("symbol", observed=True)["notional"].sum()

px = df.set_index("ts").sort_index()
bars    = px["price"].resample("1D").ohlc()       # daily open/high/low/close
returns = px["price"].pct_change().dropna()
vol_20  = returns.rolling(20).std() * np.sqrt(252)   # annualised realised vol

# point-in-time join — CRITICAL in finance
merged = pd.merge_asof(trades.sort_values("ts"), quotes.sort_values("ts"),
                       on="ts", by="symbol", direction="backward")
```

**The rules to say out loud:**
- **Never `iterrows()`.** It's a slow Python loop. `apply` is usually one in disguise too.
- **Categorical dtype for symbols**, downcast numerics — big memory savings.
- `.loc` for labels, `.iloc` for positions. **Chained indexing causes `SettingWithCopyWarning`** — use one `.loc`.
- **Parquet over CSV** — columnar, typed, compressed, and you can read just the columns you need.
- **`merge_asof` is the point-in-time join.** *"It matches each trade to the quote that was live at that moment, which is how you avoid lookahead bias — accidentally using information from the future in a backtest."*
- Name the alternatives: **Polars** (Rust, multi-threaded, lazy), **DuckDB** (columnar SQL over Parquet, in-process), Arrow as the interchange format. Mentioning these signals currency.

⚠️ **The money line, and it's one of your strongest moments:**
*"Pandas and NumPy are float64. That's fine for statistics and risk. It is not fine for money — for cash and accounting I use `Decimal` or integer minor units. It's the same `decimal` versus `double` rule as C#, and the same `DECIMAL` versus `FLOAT` rule in SQL."*

---

# PART 12 — FASTAPI AND SERVICES

```python
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field

class PriceRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=12)
    quantity: int = Field(gt=0)

app = FastAPI()

@app.post("/price", response_model=PriceResponse)
async def price(req: PriceRequest, svc: Pricer = Depends(get_pricer)):
    try:
        return await svc.compute(req)
    except UnknownSymbol as e:
        raise HTTPException(status_code=404, detail=str(e))
```

**The senior question, and it's very likely:**

**Q: What's the difference between `def` and `async def` for an endpoint?**
**Say:** *"A plain `def` endpoint is run in a thread pool, so blocking code is fine there. An `async def` endpoint runs on the event loop, so one blocking call inside it stalls the entire server for every user. The rule is: if the handler is async, everything it calls must be async — including the database driver."*

**Other points:** `Depends` is dependency injection · `lifespan` for startup/shutdown · Pydantic gives validation *and* an OpenAPI schema free · ASGI (uvicorn) vs the older WSGI (Flask/Django classic) · async DB via `asyncpg` or SQLAlchemy 2.0 async.

**Q: How would you call Python from .NET?** — rank your answer:
1. **HTTP or gRPC service boundary.** Versioned contract, independent deploys, runtime isolation. **This is the right answer**, and it's what you've actually built.
2. **Message queue** for batch or fire-and-forget work.
3. **In-process** (`Python.NET`, `CSnakes`) — mention it, then say you'd avoid it: it drags the GIL and Python's dependency tree into your .NET process.

---

# PART 13 — TESTING, TOOLING, SECURITY

**PyTest:** fixtures (with scopes, shared via `conftest.py`) · `@pytest.mark.parametrize` for table-driven tests · `monkeypatch` · `pytest-asyncio` · `freezegun` for time · `responses`/`respx` for HTTP · `testcontainers` for a real database in CI.

**The line worth saying for a finance role:**
*"I'd also use `hypothesis` for property-based testing. Financial invariants are perfect for it — put-call parity, or 'the position after N trades equals the sum of the signed quantities'. It generates the edge cases I wouldn't have thought of."*

**Tooling:** `ruff` (lint + format, replaces flake8/isort/black), `mypy` or `pyright`, `bandit` for security, `pyproject.toml`, `uv` or Poetry, pinned lockfiles, `pip-audit`.

**Security:**
- Never `eval` or `exec` on anything from outside.
- **`pickle` is unsafe on untrusted data** — unpickling can execute arbitrary code. Use JSON.
- Parameterised SQL, always.
- `secrets`, not `random`, for tokens.
- Validate at the boundary with Pydantic.

---

# PART 14 — MODULES AND PACKAGING (was missing)

**Q: What does `if __name__ == "__main__":` do?**
**Say:** *"When you run a file directly, Python sets its `__name__` to `\"__main__\"`. When you import it, `__name__` is the module name. So that guard means 'only run this when I'm the entry point, not when I'm imported'. It's also mandatory on Windows for multiprocessing, because spawn re-imports the module."*

**Q: Circular imports — what and how do you fix them?**
**Say:** *"A imports B and B imports A, so one of them sees a half-initialised module. Usually it's a design smell — the shared thing wants to live in a third module. Quick fixes are moving the import inside the function, or importing the module rather than the name. But I'd rather fix the layering."*

**Q: Virtual environments?**
**Say:** *"Each project gets its own isolated set of dependencies, so projects can't break each other. `venv` in the standard library, or `uv` which is much faster. Always with a pinned lockfile so CI and production install exactly what I tested."*

---

# PART 15 — CODING EXERCISES (do three of these, timed)

### 15.1 Rolling VWAP, O(1) per tick
```python
from collections import deque

class RollingVwap:
    def __init__(self, size: int):
        self._w, self._size = deque(), size
        self._notional = self._qty = 0.0

    def add(self, price: float, qty: float) -> float:
        self._w.append((price, qty))
        self._notional += price * qty
        self._qty += qty
        if len(self._w) > self._size:
            p, q = self._w.popleft()
            self._notional -= p * q       # subtract, don't recompute
            self._qty -= q
        return self._notional / self._qty if self._qty else 0.0
```
**Narrate while you write:** *"`deque` because I need to remove from the front in O(1). Running sums so I never recompute the window — the whole thing stays O(1) per tick regardless of window size."*

### 15.2 Realised P&L from a trade list
```python
from collections import defaultdict

def realised_pnl(trades):
    pos, cost, pnl = defaultdict(float), defaultdict(float), defaultdict(float)
    for t in trades:
        signed = t.qty if t.side == "BUY" else -t.qty
        if pos[t.symbol] == 0 or (pos[t.symbol] > 0) == (signed > 0):
            new = pos[t.symbol] + signed                       # adding to the position
            cost[t.symbol] = (cost[t.symbol] * pos[t.symbol] + t.price * signed) / new
            pos[t.symbol] = new
        else:                                                  # closing some of it
            closing = min(abs(signed), abs(pos[t.symbol]))
            pnl[t.symbol] += (t.price - cost[t.symbol]) * closing * (1 if pos[t.symbol] > 0 else -1)
            pos[t.symbol] += signed
    return dict(pnl)
```

### 15.3 Top N from a huge file, constant memory
```python
import heapq

def largest_trades(path, n=10):
    with open(path) as f:
        return heapq.nlargest(n, (parse(line) for line in f), key=lambda t: t.notional)
```
**Say:** *"Generator, so memory is constant. `nlargest` is O(n log k), not a full O(n log n) sort."*

### 15.4 Group things — the pattern that covers half of all exercises
```python
from collections import defaultdict

by_symbol = defaultdict(list)
for t in trades:
    by_symbol[t.symbol].append(t)
```

### 15.5 Async fan-out with a concurrency limit
See §5.3. Be able to write the semaphore + `TaskGroup` version from memory.

### 15.6 A timing decorator
See §2.3. Write it with `functools.wraps` and say why.

---

# PART 16 — RAPID-FIRE: 150 QUESTIONS

Cover the right column. Say the answer out loud. Target 120+.

### A. Core language (1–35)

| # | Q | A |
|---|---|---|
| 1 | List vs tuple | Changeable vs fixed; a tuple is hashable so it can be a dict key |
| 2 | Are dicts ordered? | Yes, insertion order, guaranteed since 3.7 |
| 3 | `is` vs `==` | Same object vs same value. Use `is` only for `None`/`True`/`False` |
| 4 | Why is `256 is 256` True but `257 is 257` False? | Small integers −5..256 are pre-made and reused |
| 5 | Mutable default argument | Created once at definition; use `None` and build it inside |
| 6 | Shallow vs deep copy | New container, same items vs everything copied recursively |
| 7 | Pass by value or reference? | Neither — pass the object. Rebinding is private, mutating is shared |
| 8 | Falsy values | `False`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None` |
| 9 | `list` vs `set` for `in` | O(n) vs O(1). Convert to a set if you check repeatedly |
| 10 | Why can't a list be a dict key? | It's mutable, so it isn't hashable |
| 11 | `sorted()` vs `.sort()` | New list vs in place; `.sort()` returns `None` |
| 12 | Is Python's sort stable? | Yes — equal items keep their original order. It's Timsort |
| 13 | `enumerate` | Gives index and value together; `start=1` if you want 1-based |
| 14 | `zip` | Walks several sequences in step; stops at the shortest |
| 15 | `zip(*rows)` | Transposes — turns rows into columns |
| 16 | `any` / `all` | At least one true / all true. Both short-circuit |
| 17 | `range` vs `list(range)` | Lazy object vs a real list in memory |
| 18 | String concatenation in a loop | Use `"".join(parts)` — `+=` is O(n²) |
| 19 | `str.split()` with no argument | Splits on any whitespace and drops empties |
| 20 | f-string | Inline formatting: `f"{x:,.2f}"` |
| 21 | Slicing | `start:stop:step`, stop excluded; `[::-1]` reverses |
| 22 | Does slicing copy? | For a list yes; for a NumPy array it's a **view** |
| 23 | `dict.get(k, default)` | Returns the default instead of raising `KeyError` |
| 24 | `dict.setdefault` | Get it, or insert this and return it |
| 25 | Merge two dicts | `{**a, **b}` or `a \| b` (3.9+) |
| 26 | Dict/set comprehension | `{k: v for ...}` and `{x for ...}` |
| 27 | Ternary | `a if cond else b` |
| 28 | Walrus `:=` | Assign inside an expression: `if (n := len(x)) > 5:` |
| 29 | `match` statement | 3.10+ structural pattern matching — destructures, not just compares |
| 30 | `*` and `**` at a call site | Unpack a sequence into arguments / a dict into keyword arguments |
| 31 | Positional-only / keyword-only | `def f(a, /, b, *, c)` — `a` positional only, `c` by name only |
| 32 | `global` vs `nonlocal` | Module-level variable vs the enclosing function's variable |
| 33 | `del x` | Removes the name; the object goes when nothing points at it |
| 34 | Recursion limit | ~1000 by default; Python has no tail-call optimisation |
| 35 | `id()` | The object's identity — what `is` compares |

### B. Functions and decorators (36–52)

| # | Q | A |
|---|---|---|
| 36 | `*args` / `**kwargs` | Extra positional args as a tuple / extra named args as a dict |
| 37 | Closure | A function that remembers the variables around it |
| 38 | Why `nonlocal`? | Assigning creates a local by default; `nonlocal` reuses the outer one |
| 39 | Late binding in a loop | `[lambda: i for i in range(3)]` gives `[2,2,2]`; fix with `lambda i=i:` |
| 40 | Decorator | A function that takes a function and returns a wrapped one; `@x` is `f = x(f)` |
| 41 | Decorator with arguments | Three layers: args → decorator → wrapper |
| 42 | Why `functools.wraps`? | Keeps the name, docstring and signature of the original |
| 43 | `lru_cache` | Memoisation by argument |
| 44 | `lru_cache` risk | Strong references — unbounded, on a method, it keeps `self` alive forever |
| 45 | `functools.partial` | Pre-fills some arguments and gives you a new callable |
| 46 | `lambda` | A one-expression anonymous function |
| 47 | First-class functions | Functions are objects — pass them, store them, return them |
| 48 | `map`/`filter` vs comprehension | Same result; comprehension is more Pythonic and usually clearer |
| 49 | Pure function | Same input → same output, no side effects. Easy to test |
| 50 | Function annotations at runtime | Available in `__annotations__`, but not enforced |
| 51 | Can you overload functions? | Not by signature. Use default args, or `@singledispatch` for by-type |
| 52 | `callable(x)` | Is it something you can call? |

### C. Classes and OOP (53–78)

| # | Q | A |
|---|---|---|
| 53 | Class variable vs instance variable | Shared by all instances vs one per object |
| 54 | The class-variable trap | A mutable class variable is shared — same bug as the mutable default |
| 55 | `__init__` vs `__new__` | Initialises an existing instance vs actually creates it. You almost never touch `__new__` |
| 56 | `self` | The instance, passed explicitly as the first parameter |
| 57 | `__str__` vs `__repr__` | Friendly for users vs unambiguous for developers. Write `repr` first |
| 58 | `__eq__` without `__hash__` | Object becomes unhashable — can't go in a set or dict |
| 59 | Rule for `__hash__` | Equal objects must hash equal; never hash a field you'll mutate |
| 60 | `@property` | A computed attribute, read without brackets |
| 61 | `@classmethod` | Gets the class; used for alternative constructors like `from_dict` |
| 62 | `@staticmethod` | Gets nothing; just a function grouped with the class |
| 63 | `super()` | Calls the next class in the MRO, not simply "the parent" |
| 64 | MRO | Method resolution order, computed by C3 linearisation. See `Cls.__mro__` |
| 65 | Diamond problem | Resolved deterministically by the MRO; still prefer composition |
| 66 | `_x` vs `__x` | Convention "internal" vs name mangling to `_Class__x`. Neither is security |
| 67 | Duck typing | If it has the method, it works. No declared type needed |
| 68 | `Protocol` vs `ABC` | Structural (matching shape) vs nominal (must inherit) |
| 69 | Abstract method | `@abstractmethod` on an `ABC` — instantiating without it raises |
| 70 | `isinstance` vs `type()` | `isinstance` respects inheritance; `type()` is exact. Prefer `isinstance` |
| 71 | `dataclass` | Auto `__init__`, `__repr__`, `__eq__` from annotated fields |
| 72 | `frozen=True` | Makes the dataclass immutable and hashable |
| 73 | Dataclass vs Pydantic | Internal value objects vs validated boundaries |
| 74 | `NamedTuple` | Immutable record that also behaves like a tuple |
| 75 | `__slots__` | Removes the per-instance dict — less memory, faster, no dynamic attributes |
| 76 | Descriptor | An object with `__get__`/`__set__` — how `@property` works underneath |
| 77 | Metaclass | The class of a class; controls class creation. Know of it, rarely write one |
| 78 | Monkey patching | Replacing an attribute at runtime. Useful in tests, dangerous in production |

### D. GIL, async, concurrency (79–102)

| # | Q | A |
|---|---|---|
| 79 | What is the GIL? | One lock; only one thread runs Python bytecode at a time |
| 80 | Why does it exist? | Reference counting isn't thread-safe; one coarse lock was simpler and faster |
| 81 | CPU-bound → | Processes, or C extensions that release the lock |
| 82 | I/O-bound → | asyncio, or threads |
| 83 | Does the GIL make code thread-safe? | **No.** `x += 1` is read-modify-write and can interleave |
| 84 | GIL and NumPy | NumPy releases it during heavy computation, so it genuinely parallelises |
| 85 | Future of the GIL | Per-interpreter GILs in 3.12; experimental free-threaded build in 3.13 (PEP 703) |
| 86 | Thread vs process | Shared memory, cheap, GIL-bound vs isolated memory, real parallelism, pickling cost |
| 87 | asyncio in one sentence | One thread, an event loop, and tasks that voluntarily hand control back at `await` |
| 88 | Blocking call in async code | Freezes the whole loop. Use `await asyncio.to_thread(...)` |
| 89 | `gather` vs `TaskGroup` | Prefer `TaskGroup` (3.11+): structured, cancels siblings, no orphans |
| 90 | `as_completed` | Yields results in the order they finish |
| 91 | Backpressure in asyncio | `asyncio.Queue(maxsize=N)` — Python's `Channel<T>` |
| 92 | Cancellation | `task.cancel()` raises `CancelledError` inside; clean up in `finally` |
| 93 | `create_task` gotcha | Keep a reference or it can be garbage-collected mid-flight |
| 94 | `async with` / `async for` | Async context manager / async iterator |
| 95 | Coroutine vs task | A coroutine is the recipe; a task is it scheduled and running |
| 96 | Timeout | `asyncio.wait_for(coro, timeout=5)` or `asyncio.timeout()` |
| 97 | `ThreadPoolExecutor` | Waiting work with blocking libraries |
| 98 | `ProcessPoolExecutor` | Computing work; pays pickling and startup |
| 99 | Windows multiprocessing bug | `spawn` re-imports the module — guard with `if __name__ == "__main__":` |
| 100 | Sharing big data between processes | `shared_memory` or Arrow — never pickle a huge array |
| 101 | `threading.Lock` vs `RLock` | Plain lock vs one the same thread may take again |
| 102 | Thread-safe queue | `queue.Queue` for threads, `asyncio.Queue` for async |

### E. Generators, iterators, memory (103–118)

| # | Q | A |
|---|---|---|
| 103 | Iterable vs iterator | Has `__iter__` vs has `__next__` and raises `StopIteration` |
| 104 | Generator | A function with `yield`; produces values lazily |
| 105 | Generator vs list comprehension | `()` lazy, constant memory vs `[]` builds it all now |
| 106 | Why use a generator? | Constant memory over a file of any size |
| 107 | `yield from` | Delegates to another generator |
| 108 | Can you re-use a generator? | No — once consumed it's done. Rebuild it or use `itertools.tee` |
| 109 | C# equivalent of `yield` | `yield return` — both compile to a state machine |
| 110 | `itertools.groupby` gotcha | Needs **sorted** input |
| 111 | `deque` | O(1) at both ends — the tool for rolling windows |
| 112 | `Counter` | Frequency counts plus `.most_common(n)` |
| 113 | `defaultdict` | Creates the missing value automatically |
| 114 | `heapq.nlargest` | Top-k in O(n log k) without a full sort |
| 115 | `bisect` | Binary search / insert into a sorted list, O(log n) |
| 116 | How is memory managed? | Reference counting, plus a generational collector for cycles |
| 117 | Reference cycle | Counts never reach zero; only the cycle collector frees it |
| 118 | Finding a leak | `tracemalloc` two snapshots and diff; check caches, globals, closures |

### F. Types, errors, files (119–133)

| # | Q | A |
|---|---|---|
| 119 | Are type hints enforced? | No — erased at runtime. `mypy`/`pyright` check statically, like TypeScript |
| 120 | `Optional[int]` means | `int \| None` — not "optional argument" |
| 121 | `TypedDict` | A dict with a known set of keys and types |
| 122 | `Literal` | Only these exact values: `Literal["buy","sell"]` |
| 123 | `raise` vs `raise e` vs `raise X from e` | Preserve / re-raise / chain the cause |
| 124 | `try/except/else/finally` | `else` runs only if nothing raised; `finally` always runs |
| 125 | EAFP vs LBYL | Try and catch vs check first. EAFP is the Python way |
| 126 | Are exceptions expensive in Python? | Relatively cheap — unlike C#, where they're expensive |
| 127 | Bare `except:` | Catches everything including `KeyboardInterrupt`. Never do it |
| 128 | `ExceptionGroup` / `except*` | 3.11+, for several failures at once from a `TaskGroup` |
| 129 | Custom exceptions | Subclass `Exception`; build a small hierarchy per domain |
| 130 | Context manager | `__enter__`/`__exit__` — Python's `using`. Guarantees cleanup |
| 131 | `@contextmanager` | Write one as a generator: setup, `yield`, cleanup in `finally` |
| 132 | `with open(...)` | Closes the file even if an exception is thrown |
| 133 | `assert` in production | Don't rely on it — `python -O` strips asserts out |

### G. Data, dates, money, ecosystem (134–150)

| # | Q | A |
|---|---|---|
| 134 | Money in Python | `Decimal` from a **string**, or integer minor units. Never float |
| 135 | `0.1 + 0.2` | `0.30000000000000004` — binary floating point can't hold 0.1 exactly |
| 136 | `datetime.utcnow()` | Avoid — it's naive. Use `datetime.now(timezone.utc)` |
| 137 | Timezones | `zoneinfo.ZoneInfo("Europe/London")`; store UTC, convert at display |
| 138 | Vectorise | Replace Python loops with NumPy/Pandas — 10 to 100× |
| 139 | NumPy slicing | Returns a **view**, not a copy — the opposite of a list |
| 140 | Broadcasting | NumPy expands mismatched shapes automatically |
| 141 | `iterrows()` | Avoid — it's a slow Python loop |
| 142 | `SettingWithCopyWarning` | Chained indexing. Use one `.loc` |
| 143 | `.loc` vs `.iloc` | By label vs by position |
| 144 | Parquet vs CSV | Columnar, typed, compressed, read only the columns you need |
| 145 | `merge_asof` | Point-in-time join — avoids lookahead bias in backtests |
| 146 | Polars / DuckDB | Faster modern alternatives — Rust dataframes / in-process columnar SQL |
| 147 | `def` vs `async def` in FastAPI | Thread pool vs event loop — never block the loop |
| 148 | Profiling tools | `cProfile`, `line_profiler`, and **`py-spy`** on a live process |
| 149 | `pickle` risk | Arbitrary code execution on load — never on untrusted data |
| 150 | Python's role in a .NET shop | Analytics, quant and ML behind a versioned service contract |

---

# PART 17 — THE SIX SENTENCES THAT MAKE YOU SOUND ADVANCED

Say these calmly, then stop talking.

1. **"Waiting → asyncio or threads. Computing → processes or NumPy."**
   Then add the free-threading update to show currency.

2. **"One blocking call freezes the entire event loop"** — and `asyncio.to_thread` is the fix.

3. **"`asyncio.Queue(maxsize=N)` is Python's `Channel<T>`"** — a bounded queue *is* backpressure, and it's the same pattern in both languages.

4. **"Type hints are erased at runtime, exactly like TypeScript — so I validate at the boundary with Pydantic."**

5. **"`Decimal` for money, float for statistics"** — same rule as `decimal` vs `double` in C#, and `DECIMAL` vs `FLOAT` in SQL.

6. **"Pydantic at the edges, dataclasses in the core — and Python behind a versioned service contract, so the .NET domain stays authoritative."**
