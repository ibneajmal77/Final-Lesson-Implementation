# 06 — PYTHON, FROM ZERO

> **How to read this file.**
>
> Assume you know nothing. Every idea gets the same 5 lines:
>
> **What** → one plain sentence
> **Code** → the smallest example
> **Why** → why an interviewer asks
> **Say** → the words you speak, out loud
> **Hook** → 3–5 words to remember it by
> ⚠️ → the follow-up that catches people
>
> **Say the Say lines out loud.** Silent reading is worth 20%.
>
> **Web frameworks are in `06a-fastapi.md`, `06b-django.md`, `06c-orm-databases.md`.**

**30 minutes?** Part 0 → Part 13 → Part 21.
**2 hours?** Part 0 → 2 → 5 → 6 → 13 → 21.

---

# 📑 MAP

| Part | Topic | Weight |
|---|---|---|
| 0 | The 15 answers that win | 🔴 |
| 1 | What Python is | 🟠 |
| 2 | Names, objects, memory | 🔴 |
| 3 | Every data type | 🟠 |
| 4 | Control flow | 🟡 |
| 5 | Functions, closures, decorators | 🔴 |
| 6 | Classes and objects | 🔴 |
| 7 | Generators and iterators | 🟠 |
| 8 | Errors and `with` | 🟠 |
| 9 | Modules, imports, environments | 🟡 |
| 10 | Files, JSON, CSV | 🟡 |
| 11 | Dates and money | 🟠 |
| 12 | Type hints | 🟠 |
| 13 | **GIL, threads, asyncio** | 🔴 |
| 14 | Memory and speed | 🟠 |
| 15 | Standard library | 🟡 |
| 16 | NumPy and Pandas | 🟠 |
| 17 | Testing | 🟡 |
| 18 | Security | 🟡 |
| 19 | Python ⇄ C# table | 🟠 |
| 20 | Coding exercises | 🔴 |
| 21 | 200 rapid-fire questions | 🔴 |
| 22 | Ten senior-sounding sentences | 🔴 |

---

# EASY MEMORY NOTES

Read this first. Start with the short phrase. Say the simple line. Add the last column only if they
ask for more.

| Remember | Say it simply | If they ask more |
|---|---|---|
| **Labels, not boxes** | A Python variable is a name pointing at an object. | Two names can point at the same list. |
| **Mutable changes** | Lists and dicts change in place. | This is why shared lists and default `[]` arguments cause bugs. |
| **`is` = same object** | Use `is` for `None`; use `==` for values. | Small integer caching is an implementation detail. |
| **Yield saves memory** | A generator gives one item at a time. | Good for huge files because the whole file is never loaded. |
| **Count then collect** | Python frees most objects when nobody points at them. | A separate collector handles objects that point at each other. |
| **Wait or work** | Threads help waiting. Processes help heavy CPU work. | The GIL stops normal Python threads from running CPU code in parallel. |
| **Async must not block** | One blocking call can freeze all async work. | Use async libraries or push blocking work to a thread. |
| **Money is Decimal** | Do not use float for money. | Use `Decimal` or whole pennies/cents as integers. |
| **Hints are not checks** | Type hints help tools, but Python does not enforce them. | Validate real input with Pydantic or similar. |
| **Pandas likes columns** | Do work on whole columns, not row by row. | Vectorized code runs in fast C/NumPy code. |

---

# PART 0 — THE 15 ANSWERS THAT WIN

Each one is a complete answer. Learn these first.

| # | Question | Full answer in simple words |
|---|---|---|
| 1 | **What is the GIL?** | "The GIL is one lock around normal Python code in CPython. It means only one thread runs Python bytecode at a time. Threads still help I/O waiting, but for CPU-heavy work I use processes or C/NumPy code." |
| 2 | **CPU work or waiting work?** | "If the code is waiting on I/O, I use `asyncio` or threads. If the code is doing heavy CPU work, I use processes or NumPy, because normal Python threads do not run CPU code in parallel." |
| 3 | **The asyncio trap** | "`asyncio` runs on one event loop. One blocking call, like `time.sleep()` or a blocking HTTP client, can freeze everything. Use async libraries or push blocking work to a thread." |
| 4 | **Money** | "Never use float for money. Floats are fine for statistics, but money needs exact decimal rules. Use `Decimal` from strings, or store whole cents/pennies as integers." |
| 5 | **Mutable default arg** | "Do not write `items=[]` as a default. Python creates that list once when the function is defined, so every call shares it. Use `None`, then create a new list inside." |
| 6 | **`is` vs `==`** | "`==` asks whether values are equal. `is` asks whether both names point to the exact same object. I use `is` for `None` and normal equality for values." |
| 7 | **Are type hints enforced?** | "No. Python type hints help editors, reviews, and tools like mypy, but Python does not enforce them at runtime. For real external input, I validate at the boundary with Pydantic or similar." |
| 8 | **File too big for memory** | "Use a generator and process one row at a time. That keeps memory almost constant no matter how large the file is." |
| 9 | **Pandas is slow** | "Pandas is slow when I loop row by row in Python. It is fast when I work on whole columns, because the heavy work runs in optimized C/NumPy code." |
| 10 | **How is memory freed?** | "Python frees most objects as soon as nothing points at them anymore. For objects that point at each other in a cycle, a separate cycle collector cleans them later." |
| 11 | **Shallow vs deep copy** | "A shallow copy makes a new outer container but keeps the same inner objects. A deep copy copies nested objects too. Deep copy is safer for mutation, but slower." |
| 12 | **What is a decorator?** | "A decorator wraps a function with extra behavior, without changing the function body. Common uses are logging, timing, caching, retry, and auth." |
| 13 | **`__init__` vs `__new__`** | "`__new__` creates the object. `__init__` fills that object with values. Most code only needs `__init__`." |
| 14 | **Dataclass vs Pydantic** | "A dataclass reduces boilerplate for internal objects. Pydantic validates and converts real input, so it belongs at boundaries like APIs, files, and messages." |
| 15 | **Python in a .NET shop** | "I would keep .NET as the core system of record and use Python for analytics, quant, ML, or data processing. They should talk through a clear HTTP or gRPC contract." |

---

# PART 1 — WHAT PYTHON IS

## 1.1 How your code runs

**What.** You write a `.py` file. Python turns it into **bytecode**. A **virtual machine** runs the bytecode.

**Picture.** A recipe in English becomes numbered steps. A cook works through the steps.

```python
def add(a, b):
    return a + b

import dis
dis.dis(add)      # shows the real bytecode
```

**The bit people get wrong.** Python **is** compiled. Just not to machine code.
It compiles to bytecode, then interprets that.
`__pycache__/*.pyc` = cached bytecode. It makes startup faster.

**Say:** *"Python compiles to bytecode and a VM runs it. Like .NET compiling to IL. The difference: .NET then JITs IL to native. CPython doesn't. That's most of the speed gap."*

**Hook:** **Source → bytecode → VM. No JIT.**

⚠️ *"So it's interpreted?"* → *"At the bytecode level, yes. But that's a property of the implementation, not the language. PyPy JITs. CPython doesn't."*

---

## 1.2 The implementations

| Name | What it is | When to name it |
|---|---|---|
| **CPython** | the standard one, written in C | this is "Python" |
| **PyPy** | has a JIT. Much faster for pure-Python loops | "I'd benchmark PyPy if pure-Python CPU work dominated" |
| **Python.NET** (`pythonnet`) | CPython calling .NET assemblies in-process | ⭐ your .NET interop answer |
| **IronPython** | Python on the CLR | dated. No NumPy |
| **Jython** | Python on the JVM | rarely relevant |
| **MicroPython** | microcontrollers | rarely relevant |

**Say:** *"For .NET interop I keep CPython. You need the real C ecosystem — NumPy, pandas. Then I bridge with `pythonnet` in-process, or gRPC out of process. IronPython means giving up the scientific stack."*

---

## 1.3 Versions

| Version | What it added |
|---|---|
| 2.x | **dead** since 2020. Legacy migration only |
| 3.8 | walrus `:=`, positional-only params |
| 3.9 | `dict \| dict`, built-in generics `list[int]` |
| 3.10 | `match`, `X \| Y` unions, better errors |
| 3.11 | **~25% faster**, exception groups |
| 3.12 | f-string cleanup, `type` statement |
| 3.13 | **free-threaded build — no GIL** (opt-in), plus a JIT |
| 3.14 | free-threading officially supported. Still not default |

**Say:** *"I target 3.11 or later. The 3.11 interpreter rewrite was a double-digit speedup for free. And I watch the free-threaded build, because it changes the whole threading answer. It isn't default yet."*

**Hook:** **3.11 = free speed. 3.13 = GIL becomes optional.**

⚠️ That free-threading line makes you sound current. Most candidates still say "the GIL will never go."

---

## 1.4 Indentation is the syntax

Other languages use `{ }`. Python uses **spaces**.

```python
if balance > 0:
    print("in credit")     # indented → inside
    print("still inside")
print("always runs")       # not indented → outside
```

Rules: 4 spaces per level. Never mix tabs and spaces. A `:` opens a block.

**Say:** *"Indentation is the block structure, not decoration. The code has to look like what it does."*

⚠️ Mixed tabs and spaces → `TabError`. Set the editor once, never think about it again.

---

## 1.5 Style words to use

| Term | Meaning |
|---|---|
| **PEP 8** | the style guide. `snake_case` funcs, `PascalCase` classes, `UPPER` constants |
| **PEP 20** | the Zen. `import this`. "One obvious way to do it" |
| **Pythonic** | idiomatic. Comprehensions over loops. `with` over manual cleanup |
| **`ruff`** | linter + formatter. Fast. Replaces flake8, isort, black |
| **`mypy` / `pyright`** | static type checkers |

**Say:** *"I don't argue about formatting. `ruff format` in a pre-commit hook, `ruff` for lint, `mypy` in CI. Style stops being a review topic."*

---

## 1.6 Running things

```bash
python app.py            # run a file
python -m pytest         # run an installed module
python -i app.py         # run, then stay interactive
python -c "print(1+1)"   # one-liner
```

`-m` puts the current directory on the path. That fixes most "works on my machine" import bugs.

---

# PART 2 — NAMES, OBJECTS, MEMORY ⭐

Get this part and half of Python's weirdness disappears.

## 2.1 Variables are labels, not boxes

**What.** C#: `int x = 5` reserves a box, puts 5 in it.
Python: `x = 5` creates the object `5`, then sticks the label `x` on it.

**Picture.** Sticky notes on objects. Not boxes holding things.

```python
x = [1, 2, 3]
y = x            # second label, SAME list
y.append(4)
print(x)         # [1, 2, 3, 4]
print(x is y)    # True
```

**Why.** This explains arguments, copying, default args, and half of all beginner bugs.

**Say:** *"A variable is a name bound to an object. Two names can point at one object. Mutating through one shows up in the other. Everything acts like a reference type. There are no structs."*

**Hook:** **Labels, not boxes.**

⚠️ *"Pass by value or pass by reference?"* → *"Neither. **Pass by object reference.** The function gets a new name pointing at the same object. Rebinding the name does nothing to the caller. Mutating the object does."*

```python
def rebind(lst):  lst = [9]        # caller sees nothing
def mutate(lst):  lst.append(9)    # caller sees it
```

---

## 2.2 Mutable vs immutable

**Immutable** = can't change. Any "change" makes a new object.
**Mutable** = changes in place.

| Immutable | Mutable |
|---|---|
| `int` `float` `complex` `bool` | `list` |
| `str` `bytes` | `dict` |
| `tuple` | `set` |
| `frozenset` `range` `None` | `bytearray`, your classes |

```python
s = "hello"
print(id(s))
s += " world"      # NOT a change. A new string
print(id(s))       # different
```

**Three consequences. Say them as a list:**
1. Only immutable things are hashable → only they can be dict keys or set members.
2. Immutable things are **thread-safe for free**. No lock needed.
3. `s += x` in a loop is **O(n²)**. Use `"".join(parts)`.

**Say:** *"Immutable means any change makes a new object. That's why only immutable objects are hashable. And it's why they're inherently thread-safe."*

**Hook:** **Can't change → can be a key → safe to share.**

⚠️ *"Can a tuple be unhashable?"* → *"Yes. A tuple is hashable only if everything inside it is. `(1, [2])` isn't — it holds a list."*

---

## 2.3 `is` vs `==`

- `==` → **same value?** (calls `__eq__`)
- `is` → **same object?** (compares memory address)

```python
a = [1, 2]; b = [1, 2]
a == b     # True
a is b     # False

x = 256; y = 256; x is y      # True
x = 257; y = 257; x is y      # False  (!)
```

**Why the weirdness.** CPython pre-makes the ints **−5 to 256** and reuses them.
Short identifier-like strings are **interned** too.
Both are optimisations. Never rely on them.

**Say:** *"`==` is value, `is` is identity. I only use `is` for `None`, `True`, `False` and sentinels. Small ints are cached, which makes `is` look like it works by accident."*

**Hook:** **`is` is for `None`.**

⚠️ *"Why `x is None`, not `x == None`?"* → *"`__eq__` can be overridden. A class could claim to equal None. `is` can't be lied to. It's also faster."*

⚠️ *"Why not `if not x`?"* → *"Because `0`, `""`, `[]` and `False` are all falsy. `if not x` confuses **missing** with **empty**. That's a real bug when zero is a valid value."*

---

## 2.4 Copying

```python
import copy

b = a                  # NOT a copy. Second label
b = a[:]               # shallow
b = list(a)            # shallow
b = a.copy()           # shallow
b = copy.copy(a)       # shallow
b = copy.deepcopy(a)   # deep
```

**Shallow** = new outer box, **same inner objects**.
**Deep** = duplicated all the way down.

```python
a = [[1, 2], [3, 4]]
b = a[:]           # shallow
b[0].append(99)
print(a)           # [[1, 2, 99], [3, 4]]  — inner list was shared
```

**Say:** *"Shallow gives me a new outer list, but the elements are still shared. If they're mutable and I'll change them, I need `deepcopy`. But `deepcopy` is slow. On a hot path I'd design with immutable data instead."*

**Hook:** **Copies the shelf, not the books.**

---

## 2.5 How memory is freed

**Two mechanisms.**

**1. Reference counting.** Every object counts the names pointing at it.
Count hits 0 → freed **immediately**.

**2. The cycle collector.** Refcounting can't free `a.b = b; b.a = a`.
A separate collector sweeps for cycles. Three generations. New objects checked often, survivors less often.

```python
import sys, gc
sys.getrefcount(x)     # count (+1 for the argument itself)
gc.collect()           # force a sweep
```

**Say:** *"Refcounting handles the normal case instantly and deterministically. Unlike .NET, where the GC decides when. A generational collector handles cycles. That's also why `__del__` is unreliable and why `with` is the right way to release resources."*

**Hook:** **Count for normal. Sweep for loops.**

⚠️ *"Where do Python leaks come from?"* Four answers:
> *"One — a module-level cache that only grows. Two — reference cycles holding something expensive. Three — a closure or bound method keeping a big object alive; classically an event handler never unsubscribed. Four — a C extension leaking outside Python's control. I'd start with `tracemalloc` and diff two snapshots."*

---

## 2.6 Everything is an object

Functions, classes, modules — all objects. All assignable, passable, storable.

```python
def greet(): return "hi"
f = greet          # a function in a variable
funcs = [greet]    # in a list
greet.tag = "x"    # attach an attribute
```

**Say:** *"Functions and classes are first-class objects. That's why decorators, callbacks and DI are natural here, not framework features."*

---

# PART 3 — EVERY DATA TYPE

## 3.1 Numbers

```python
i = 42              # int — arbitrary precision. Never overflows
f = 3.14            # float — 64-bit IEEE 754. Same as C# double
c = 2 + 3j          # complex
b = 0b1010          # binary  → 10
h = 0xFF            # hex     → 255
big = 1_000_000     # underscores are readability only
```

```python
7 / 2      # 3.5   → ALWAYS a float
7 // 2     # 3     floor division
-7 // 2    # -4    floors DOWN, not toward zero
7 % 2      # 1
2 ** 10    # 1024
divmod(7, 2)   # (3, 1)
```

⚠️ **`-7 // 2` is `-4`. `-7 % 2` is `1`.**
C# truncates toward zero: `-7 / 2 == -3`, `-7 % 2 == -1`.
This bites when porting code.

```python
0.1 + 0.2 == 0.3     # False
0.1 + 0.2            # 0.30000000000000004
```

**Say:** *"Python ints are arbitrary precision. They never overflow, they just get slower. Floats are the same IEEE doubles as everywhere. Fine for stats. Never for money."*

**Hook:** **int never overflows. float always lies a little.**

---

## 3.2 Strings

**Immutable sequences of Unicode characters.**

```python
s = "hello"
s = 'hello'                      # same thing
s = """multi
line"""
s = f"{name} owes {amt:,.2f}"    # f-string. Use these
r = r"C:\new\path"               # raw. Backslashes stay literal
b = b"bytes"                     # bytes, not str
```

**The methods that matter:**
```python
s.strip() / .lstrip() / .rstrip()
s.upper() / .lower() / .title() / .casefold()
s.split(",") / s.splitlines()
",".join(parts)                  # ⭐ the fast way to build strings
s.replace(old, new)
s.startswith(x) / s.endswith(x)
s.find(x)        # -1 if missing
s.index(x)       # raises if missing
s.zfill(5) / s.ljust(10) / s.rjust(10)
s.encode("utf-8")     # str   → bytes
b.decode("utf-8")     # bytes → str
s.removeprefix("x") / s.removesuffix("y")     # 3.9+
```

**f-strings in full:**
```python
f"{v:.2f}"        # 2 decimals
f"{v:,}"          # thousands separators
f"{v:>10}"        # right align, width 10
f"{v:%Y-%m-%d}"   # dates
f"{v=}"           # prints "v=42"   (3.8+)
f"{v!r}"          # repr, not str
```

**The concat trap:**
```python
out = ""
for p in parts: out += p     # BAD — O(n²)

out = "".join(parts)         # GOOD — O(n)
```

**Say:** *"Strings are immutable. Concatenating in a loop reallocates every time — quadratic. `join` is the linear version. And `str` is text, `bytes` is raw data. Encode and decode at the edges, never in the middle."*

**Hook:** **Join, don't `+=`. Encode at the edges.**

⚠️ *"`str` vs `bytes`?"* → *"`str` is Unicode text. `bytes` is raw octets. Files and sockets give bytes. Decode on the way in, encode on the way out. Mixing them causes every `UnicodeDecodeError`."*

---

## 3.3 Lists

**Ordered. Mutable. Duplicates allowed.** A dynamic array of pointers.

```python
xs.append(4)          # add to end
xs.extend([5, 6])     # add many
xs.insert(0, 0)       # insert
xs.pop()              # remove + return last
xs.pop(0)             # remove + return first  ⚠️ O(n)
xs.remove(3)          # remove first matching VALUE
del xs[1]
xs.sort()             # in place. Returns None
sorted(xs)            # returns a NEW list
xs.reverse() / reversed(xs)
xs.index(2) / xs.count(2)
3 in xs               # ⚠️ O(n)
```

| Operation | Cost |
|---|---|
| `xs[i]` | O(1) |
| append, pop from end | O(1) |
| insert, pop at front | **O(n)** |
| `in` | **O(n)** |
| sort | O(n log n) |

**Say:** *"A list is a dynamic array — `List<T>`. Index and append are constant. Inserting at the front is linear. `in` is a linear scan. For a queue I use `deque`. For membership I use a set."*

⚠️ **The multiplication bug:**
```python
grid = [[0] * 3] * 3      # BUG — three refs to ONE row
grid[0][0] = 1            # [[1,0,0],[1,0,0],[1,0,0]]
grid = [[0] * 3 for _ in range(3)]   # correct
```

---

## 3.4 Tuples

**Ordered. Immutable.**

```python
t = (1, 2, 3)
t = 1, 2, 3            # brackets optional. The COMMA makes it
one = (1,)             # ⚠️ single element needs the comma
empty = ()
a, b, c = t            # unpack
a, *rest = t           # a=1, rest=[2,3]
a, b = b, a            # swap, no temp
```

**Use a tuple when:** fixed-size record, dict key, returning several values, anything that shouldn't change.

**Say:** *"A list is a variable-length collection of the same kind of thing. A tuple is a fixed-size record of different things. And a tuple can be a dict key, because it's hashable."*

---

## 3.5 Dicts

**Key → value. Insertion-ordered since 3.7.** Average O(1).

```python
d["a"]                 # KeyError if missing
d.get("z")             # None if missing
d.get("z", 0)          # default
d.setdefault("z", [])  # get, or insert then get
d.keys() / d.values() / d.items()
d.pop("a") / d.popitem()
d.update(other)
{**d1, **d2}           # merge
d1 | d2                # merge (3.9+)
"a" in d               # O(1). Checks KEYS
del d["a"]

for k, v in d.items():
    ...
```

**The three specialised dicts:**
```python
from collections import defaultdict, Counter

counts = defaultdict(int)        # missing key → 0
groups = defaultdict(list)       # missing key → []
Counter("hello").most_common(2)  # [('l', 2), ('h', 1)]
```

**Say:** *"A dict is a hash table with a compact layout. Average O(1). Insertion-ordered since 3.7. Keys must be hashable, so immutable."*

⚠️ *"What makes a good key?"* → *"Consistent `__hash__` and `__eq__`. Equal objects must hash equal. If you define `__eq__` without `__hash__`, Python sets `__hash__` to None and the object becomes unhashable."*

⚠️ *"Are dicts thread-safe?"* → *"Single operations are atomic because of the GIL. Read-modify-write isn't. `d[k] += 1` is three bytecodes. That needs a lock."*

---

## 3.6 Sets

**Unordered. Unique. Mutable.** O(1) membership.

```python
s = {1, 2, 3}
s = set()              # ⚠️ {} is an empty DICT
s.add(4)
s.discard(4)           # won't raise
s.remove(4)            # WILL raise
a | b    # union
a & b    # intersection
a - b    # difference
a ^ b    # in one but not both
a <= b   # subset
frozenset([1,2])       # immutable → can be a key
```

**Why it matters.** Swapping a list for a set turns O(n) into O(1). It's the most common easy win in a coding exercise.

**Say:** *"A set is a hash table with no values. Dedupe and membership. Swapping a list for a set in a hot `in` check is usually the biggest single win available."*

---

## 3.7 `None`, bools, truthiness

`None` is Python's null. One instance. A singleton.

**Falsy — memorise the whole list:**
`False`, `None`, `0`, `0.0`, `Decimal(0)`, `""`, `[]`, `()`, `{}`, `set()`, `range(0)`,
plus anything whose `__bool__` is False or `__len__` is 0.

Everything else is truthy.

```python
if items:              # Pythonic
if len(items) > 0:     # noise
if x is None:          # correct null check
if not x:              # ⚠️ also true for 0, "", []
```

⚠️ **`bool` is a subclass of `int`.** `True == 1`. `sum([True, True])` is `2`.

---

## 3.8 Slicing

`seq[start:stop:step]` — **start included, stop excluded.**

```python
xs = [0,1,2,3,4,5,6,7,8,9]
xs[2:5]      # [2,3,4]
xs[:3]       # first three
xs[-3:]      # last three
xs[::2]      # every second
xs[::-1]     # reversed ⭐
xs[:]        # shallow copy
xs[1:3] = [9]   # slice assignment (lists)
del xs[::2]
```

Same syntax on lists, tuples, strings, bytes.

**Say:** *"Start inclusive, stop exclusive, optional step. `[::-1]` reverses. `[:]` copies. Out-of-range slices clamp instead of raising, which makes them safe."*

---

## 3.9 Comprehensions

**What.** One line to build a collection from another. It's LINQ.

```python
[x * 2 for x in xs]                  # list   → .Select()
[x for x in xs if x > 0]             # filter → .Where()
{x: x**2 for x in xs}                # dict
{x for x in xs}                      # set
(x * 2 for x in xs)                  # ⚠️ GENERATOR, lazy. Not a tuple
[y for row in grid for y in row]     # nested. Left to right = outer to inner
[x if x > 0 else 0 for x in xs]      # ternary goes BEFORE the for
```

**Say:** *"A comprehension is the idiomatic map/filter. Faster than a loop with `append`, because the append happens in C. Round brackets give a lazy generator — that's the memory-safe version."*

⚠️ *"When shouldn't you use one?"* → *"When it stops being readable. More than two `for`s and an `if`. Or when it has side effects. A comprehension builds a value. It doesn't do things."*

---

## 3.10 Operators worth knowing

```python
x = 5 if cond else 10        # ternary
a, b = b, a                  # swap
"x" in seq / not in
x and y                      # returns an operand, not a bool
x or default                 # the classic default idiom
n := f()                     # walrus. Assign inside an expression (3.8+)
@                            # matrix multiply (NumPy)
```

⚠️ **`and` / `or` return operands, not booleans.**
`"" or "default"` → `"default"`. `0 or 5` → `5`.
So `x or default` is **wrong** when `0` is valid. Use `x if x is not None else default`.

---

# PART 4 — CONTROL FLOW

## 4.1 `if` / `elif` / `else`

```python
if x > 10:
    ...
elif x > 5:
    ...
else:
    ...
```

No `switch` before 3.10. No parentheses needed. No `{ }`.

**Chained comparisons work:**
```python
if 0 < x < 100:        # legal, and it means what it looks like
```

---

## 4.2 `for` loops

**What.** Python's `for` is a **foreach**. There is no C-style `for(i=0; i<n; i++)`.

```python
for item in items: ...
for i in range(10): ...              # 0..9
for i in range(2, 10, 2): ...        # 2,4,6,8
for i, item in enumerate(items): ...          # index AND item ⭐
for i, item in enumerate(items, start=1): ...
for a, b in zip(xs, ys): ...                  # pair two lists ⭐
for k, v in d.items(): ...
for x in reversed(xs): ...
for x in sorted(xs, key=lambda r: r.price): ...
```

**Say:** *"There's no index-based for loop. If I need the index I use `enumerate`. If I'm walking two sequences I use `zip`. Writing `for i in range(len(xs))` is the tell that someone learned Python from C."*

**Hook:** **`enumerate` for the index. `zip` for pairs.**

⚠️ `zip` stops at the shortest. Use `zip(a, b, strict=True)` (3.10+) to raise if lengths differ.

---

## 4.3 `while`

```python
while queue:
    item = queue.pop()

while True:
    if done: break
```

---

## 4.4 `break`, `continue`, and `else` on a loop

```python
for x in xs:
    if x == target:
        break
else:
    print("never found it")     # runs ONLY if no break happened
```

**Say:** *"A loop can have an `else`. It runs only if the loop finished without a `break`. It's the search-failed branch. Rare, but it shows up in quizzes."*

**Hook:** **`else` = "no break happened".**

---

## 4.5 `match` (3.10+)

Not a switch. It's **structural pattern matching** — it destructures as it matches.

```python
match order:
    case {"type": "limit", "price": p}:      # matches a dict shape
        ...
    case Trade(side="BUY", qty=q) if q > 100:   # class + guard
        ...
    case [first, *rest]:                     # list shape
        ...
    case _:                                  # default
        ...
```

**Say:** *"`match` is structural pattern matching, closer to F# or C# pattern matching than to a C switch. It binds variables while it matches. For a simple value switch, a dict of handlers is still cleaner."*

---

## 4.6 The dict-dispatch pattern ⭐

The idiomatic replacement for a big `if/elif` chain. **Worth showing in a coding exercise.**

```python
handlers = {
    "BUY":  handle_buy,
    "SELL": handle_sell,
}
handlers.get(msg.type, handle_unknown)(msg)
```

**Say:** *"For dispatch I use a dict of functions instead of an if-chain. It's O(1), it's open for extension, and adding a case doesn't touch existing code."*

---

# PART 5 — FUNCTIONS ⭐

## 5.1 The full argument syntax

```python
def f(a, b=1, *args, c, d=2, **kwargs):
    ...
#     a      → required, positional
#     b=1    → optional, has a default
#     *args  → any extra positional args, as a TUPLE
#     c      → keyword-only, REQUIRED (it's after *args)
#     d=2    → keyword-only, optional
#     **kwargs → any extra named args, as a DICT
```

```python
def f(a, b, /, c, *, d):
    ...
#     a, b before /  → positional-ONLY (can't be passed by name)
#     d after *      → keyword-ONLY
```

**Say:** *"`*args` collects extra positionals into a tuple, `**kwargs` collects extra keywords into a dict. Anything after a bare `*` is keyword-only — I use that for boolean flags so call sites can't be read wrong."*

**Hook:** **`*` = tuple. `**` = dict. After `*` = must be named.**

**Unpacking at the call site — the same symbols, reversed:**
```python
f(*my_list)      # spread a list into positional args
f(**my_dict)     # spread a dict into keyword args
```

---

## 5.2 The mutable default trap ⭐ (asked constantly)

```python
def add(item, bucket=[]):     # BUG
    bucket.append(item)
    return bucket

add(1)   # [1]
add(2)   # [1, 2]   ← the SAME list came back
```

**Why.** The `[]` is created **once**, when Python reads the `def` line. Not per call.

```python
def add(item, bucket=None):   # FIX
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

**Say:** *"Defaults are evaluated once at definition time, not per call. So a mutable default is shared by every call. The fix is `None` plus create it inside."*

**Hook:** **Defaults are made once. Never default to `[]` or `{}`.**

---

## 5.3 Scope — the LEGB rule

Python looks up a name in this order:

| Letter | Scope | Meaning |
|---|---|---|
| **L** | Local | inside this function |
| **E** | Enclosing | the function wrapping this one |
| **G** | Global | module level |
| **B** | Built-in | `len`, `print`, `dict` |

```python
x = 10
def f():
    x = 20          # makes a NEW local. The global is untouched
def g():
    global x
    x = 20          # now it writes the global
def outer():
    y = 1
    def inner():
        nonlocal y  # writes the ENCLOSING function's variable
        y = 2
```

⚠️ **The classic error.**
```python
count = 0
def bump():
    count += 1      # UnboundLocalError!
```
Assigning to `count` anywhere in the function makes it local **for the whole function**.
So the read on the right-hand side fails.

**Say:** *"Name resolution is LEGB — local, enclosing, global, built-in. Assigning to a name anywhere in a function makes it local throughout that function, which is where `UnboundLocalError` comes from. `global` and `nonlocal` opt out, and I avoid both."*

**Hook:** **Assign to it → it's local everywhere.**

---

## 5.4 Functions are objects

```python
def greet(n): return f"hi {n}"

f = greet              # assign
[greet](0)("x")        # store in a list
def run(fn): return fn("x")     # pass as an argument
def make(): return greet        # return one
```

This is the whole basis for decorators, callbacks and strategy patterns.

---

## 5.5 `lambda`

**What.** A one-expression anonymous function.

```python
sorted(trades, key=lambda t: t.price)
sorted(trades, key=lambda t: (t.symbol, -t.qty))    # multi-key ⭐
list(filter(lambda x: x > 0, xs))
```

**Say:** *"A lambda is a single-expression function. I use them for `key=` in sorting and little callbacks. Anything longer gets a real `def` with a name, because names are documentation."*

⚠️ Prefer `operator.itemgetter("price")` / `attrgetter("price")` over lambdas in sorts — faster and clearer.

---

## 5.6 Closures

**What.** A function that remembers the variables from where it was **defined**, even after that outer function has returned.

```python
def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

c = make_counter()
c()   # 1
c()   # 2      ← it remembered
```

**Why.** Closures are how decorators keep state, how callbacks capture context, and a very common source of memory leaks.

**Say:** *"A closure is a function plus the variables it captured from its defining scope. It's the same idea as a C# lambda capturing locals — and it has the same risk: it keeps those objects alive."*

**Hook:** **Function + remembered variables.**

⚠️ **The late-binding trap — asked often.**
```python
fs = [lambda: i for i in range(3)]
[f() for f in fs]        # [2, 2, 2]  — NOT [0, 1, 2]
```
The lambda captures the **variable**, not its value. By call time, `i` is 2.
**Fix:**
```python
fs = [lambda i=i: i for i in range(3)]   # bind now via a default
```

---

## 5.7 Decorators ⭐

**What.** A function that takes a function and returns a replacement.

**Picture.** Gift wrap. Same present inside, extra layer outside.

**Build it up in three steps:**

```python
# 1. the wrapper
def log(fn):
    def wrapper(*args, **kwargs):
        print("before")
        result = fn(*args, **kwargs)
        print("after")
        return result
    return wrapper

# 2. apply it manually
def work(): ...
work = log(work)

# 3. the @ syntax — identical to step 2
@log
def work(): ...
```

**Always use `functools.wraps`:**
```python
import functools

def log(fn):
    @functools.wraps(fn)          # keeps __name__, __doc__, signature
    def wrapper(*a, **kw):
        return fn(*a, **kw)
    return wrapper
```
Without it, `work.__name__` becomes `"wrapper"` and debugging, docs and framework
introspection all break.

**A decorator with arguments needs three levels:**
```python
def retry(times=3):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kw):
            for attempt in range(times):
                try:
                    return fn(*a, **kw)
                except Exception:
                    if attempt == times - 1:
                        raise
        return wrapper
    return decorator

@retry(times=5)
def fetch(): ...
```

**The built-ins you must know:**

| Decorator | What it does |
|---|---|
| `@property` | method that reads like a field |
| `@staticmethod` | no `self`. Just a function living in the class |
| `@classmethod` | gets `cls`. Used for alternative constructors |
| `@functools.cache` | memoise, unbounded (3.9+) |
| `@functools.lru_cache(maxsize=128)` | memoise, bounded |
| `@functools.wraps` | preserve metadata inside your own decorator |
| `@dataclass` | auto `__init__`, `__repr__`, `__eq__` |
| `@abstractmethod` | subclass must implement it |
| `@contextlib.contextmanager` | turn a generator into a `with` block |

**Say:** *"A decorator is a function that wraps a function. It's how you add cross-cutting concerns — logging, timing, retry, auth, caching — without touching the body. It's the same job as a .NET attribute plus an interceptor, or middleware in a pipeline. And I always use `functools.wraps` so the wrapper doesn't destroy the original's identity."*

**Hook:** **Wraps a function. Middleware for one function.**

⚠️ *"Where would you use one in production?"* → *"Timing and structured logging on service boundaries, retry with backoff on external calls, `lru_cache` on pure expensive lookups, and auth checks on route handlers."*

⚠️ **`lru_cache` traps:** arguments must be hashable, so no lists or dicts. And it holds
references forever — a cache on a method keeps every instance alive. That's a leak.

---

## 5.8 `functools`

```python
from functools import wraps, cache, lru_cache, partial, reduce, singledispatch

double = partial(multiply, 2)          # pre-fill an argument
reduce(operator.add, xs, 0)            # fold. Rarely worth it — use sum()

@singledispatch                        # overload by first-argument type
def render(x): ...
@render.register
def _(x: int): ...
```

---

# PART 6 — CLASSES AND OBJECTS ⭐

## 6.1 A class, part by part

```python
class Account:
    bank = "HSBC"                    # CLASS attribute — shared by all instances

    def __init__(self, owner, balance=0):
        self.owner = owner           # INSTANCE attribute — one per object
        self._balance = balance      # _ means "internal, don't touch"

    def deposit(self, amount):       # self = this
        self._balance += amount
        return self

    def __repr__(self):              # what developers see. Aim for unambiguous
        return f"Account({self.owner!r}, {self._balance})"

    def __str__(self):               # what users see
        return f"{self.owner}: {self._balance}"
```

| Word | Meaning |
|---|---|
| `self` | the instance. Explicit in Python, implicit (`this`) in C# |
| class attribute | one copy, shared. Like `static` |
| instance attribute | one per object |
| `_name` | convention: internal. Nothing enforces it |
| `__name` | name-mangled to `_Class__name`. Avoids subclass collisions. Still not private |

⚠️ **The shared-class-attribute bug:**
```python
class Basket:
    items = []           # BUG — every Basket shares ONE list
```
Mutable class attributes are shared. Put them in `__init__`.

**Say:** *"`self` is explicit because explicit is better than implicit. Class attributes are shared like statics, so a mutable one is a shared-state bug. Instance state belongs in `__init__`."*

---

## 6.2 `__init__` vs `__new__`

- `__new__` **creates** the object. Runs first. Returns the instance.
- `__init__` **initialises** it. Returns nothing.

**Say:** *"`__new__` allocates, `__init__` populates. You only override `__new__` for immutable subclasses or singletons. Everyday code only touches `__init__`."*

⚠️ Python has **no constructor overloading**. Use `@classmethod` alternative constructors:
```python
@classmethod
def from_csv(cls, row):
    return cls(row[0], float(row[1]))
```

---

## 6.3 `@property`, `@staticmethod`, `@classmethod`

```python
class Trade:
    def __init__(self, qty, price):
        self.qty, self.price = qty, price

    @property
    def notional(self):              # called like a field: t.notional
        return self.qty * self.price

    @notional.setter                 # optional
    def notional(self, v): ...

    @staticmethod
    def is_valid_symbol(s):          # no self, no cls. Just grouped here
        return len(s) <= 6

    @classmethod
    def from_fix(cls, msg):          # gets the CLASS. Alternative constructor
        return cls(msg.qty, msg.price)
```

| | Gets | Use for |
|---|---|---|
| `@property` | `self` | computed value that looks like a field |
| `@staticmethod` | nothing | a helper that belongs with the class |
| `@classmethod` | `cls` | alternative constructors, factories |

**Say:** *"`@property` lets me start with a plain attribute and add logic later without breaking callers. `@classmethod` gets the class, so it's the way to do alternative constructors — Python doesn't overload."*

---

## 6.4 Inheritance and `super()`

```python
class Base:
    def __init__(self, a): self.a = a
    def describe(self): return "base"

class Child(Base):
    def __init__(self, a, b):
        super().__init__(a)          # ALWAYS call this
        self.b = b
    def describe(self):
        return "child + " + super().describe()
```

**Say:** *"Every method is virtual by default. There is no `virtual` or `override` keyword. `super()` walks the MRO, not just the direct parent — that's what makes cooperative multiple inheritance work."*

---

## 6.5 Multiple inheritance and the MRO

Python allows multiple base classes. It resolves them with **C3 linearisation** — the MRO.

```python
class A: ...
class B(A): ...
class C(A): ...
class D(B, C): ...

D.__mro__       # D, B, C, A, object
```

**The diamond problem** is solved: `A` appears **once**, at the end.

**Say:** *"Multiple inheritance is resolved by C3 linearisation — the method resolution order. It's deterministic, left to right, depth first, with duplicates removed so a shared base appears once. In practice I use it for mixins, not for real multiple inheritance."*

**Hook:** **MRO = C3. Left to right. Base appears once.**

---

## 6.6 Dunder methods — the full table

"Dunder" = double underscore. These hook into language syntax.

| Method | Triggered by |
|---|---|
| `__init__` | `Account(...)` |
| `__new__` | object creation |
| `__repr__` | `repr(x)`, the REPL, debuggers |
| `__str__` | `str(x)`, `print(x)`, f-strings |
| `__eq__` / `__ne__` | `==` / `!=` |
| `__lt__ __le__ __gt__ __ge__` | `<` `<=` `>` `>=`, and sorting |
| `__hash__` | dict keys, set members |
| `__len__` | `len(x)`, and truthiness |
| `__bool__` | `if x:` |
| `__getitem__` / `__setitem__` / `__delitem__` | `x[k]` |
| `__contains__` | `k in x` |
| `__iter__` / `__next__` | `for x in ...` |
| `__call__` | `x()` — makes the instance callable |
| `__enter__` / `__exit__` | `with x:` |
| `__aenter__` / `__aexit__` | `async with x:` |
| `__add__ __sub__ __mul__ __truediv__` | `+` `-` `*` `/` |
| `__radd__` etc. | the same, when your object is on the **right** |
| `__iadd__` | `+=` |
| `__getattr__` | attribute **not** found normally |
| `__getattribute__` | **every** attribute access ⚠️ dangerous |
| `__setattr__` | every assignment |
| `__slots__` | fix the allowed attributes, save memory |
| `__del__` | finaliser ⚠️ unreliable — use `with` |

**Say:** *"Dunders are Python's operator overloading and protocol hooks. Implementing `__iter__` makes my object work in a `for` loop; `__enter__` and `__exit__` make it work in a `with`. That's duck typing enforced by convention rather than by interfaces."*

⚠️ **`__eq__` and `__hash__` go together.** Define `__eq__` and Python sets `__hash__ = None`.
The object becomes unhashable. Define both, or use a frozen dataclass.

---

## 6.7 Duck typing, `Protocol`, `ABC`

**Duck typing.** "If it walks like a duck…" — Python doesn't check the type, it just calls
the method.

**Three ways to express an interface:**

```python
# 1. Nothing at all — pure duck typing
def render(shape): shape.draw()

# 2. ABC — nominal. Subclass must inherit AND implement
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def draw(self): ...

# 3. Protocol — structural. No inheritance needed ⭐
from typing import Protocol
class Drawable(Protocol):
    def draw(self) -> None: ...
```

**Say:** *"`ABC` is nominal typing — you must inherit from it, like a C# interface. `Protocol` is structural — anything with the right shape satisfies it, checked statically by mypy. Protocol is the modern choice, because it doesn't force a class hierarchy on code you don't own."*

**Hook:** **ABC = must inherit. Protocol = must match.**

---

## 6.8 Dataclass vs NamedTuple vs Pydantic vs plain class

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Trade:
    symbol: str
    qty: int
    price: float = 0.0
    tags: list[str] = field(default_factory=list)   # ⚠️ NOT tags: list = []
```

| | Gives you | Validates? | Use for |
|---|---|---|---|
| **plain class** | nothing | no | behaviour-heavy objects |
| **`NamedTuple`** | immutable, tuple-like, unpackable | no | lightweight records |
| **`@dataclass`** | `__init__`, `__repr__`, `__eq__`, optional ordering | **no** | internal data objects |
| **`@dataclass(frozen=True)`** | all that, immutable + hashable | no | dict keys, thread-safe values |
| **Pydantic `BaseModel`** | all that, **plus type coercion and validation** | **yes** | API/queue/config boundaries |

**Say:** *"Dataclasses remove boilerplate but do not validate — the type hints are not enforced. Pydantic actually parses and coerces at runtime, so it's what I use at any boundary. Inside the domain, frozen dataclasses with slots."*

**Hook:** **Dataclass inside. Pydantic at the edges.**

⚠️ `slots=True` (3.10+) removes `__dict__`. Big memory win on millions of objects, and faster
attribute access. Cost: no dynamic attributes, and multiple inheritance gets fiddly.

---

## 6.9 `__slots__`

```python
class Tick:
    __slots__ = ("symbol", "price", "ts")
```

**What.** Fixes the allowed attribute names. Removes the per-instance `__dict__`.
**Result:** roughly 40–50% less memory per object, and faster attribute access.
**Cost:** no new attributes at runtime, no `__dict__`, no weakrefs unless you add `__weakref__`.

**Say:** *"`__slots__` is the answer when I have millions of small objects — market data ticks, for example. It trades flexibility for memory and speed."*

---

## 6.10 Descriptors and metaclasses (know what they are, don't volunteer them)

**Descriptor.** An object defining `__get__`, `__set__` or `__delete__`. It controls attribute
access. **`@property` is a descriptor.** So are methods, `classmethod`, and every ORM field.

**Metaclass.** The class of a class. `type` is the default. Overriding `__new__` on a metaclass
lets you rewrite a class as it's defined. Django models and ABCs use them.

**Say:** *"Descriptors are the machinery behind `property`, methods and ORM fields — anything that hooks attribute access. A metaclass is a class factory; it customises class creation. I know both, but I'd flag a metaclass in review as a maintenance risk unless a framework needs it."*

**Hook:** **Descriptor = controls attribute access. Metaclass = class of a class.**

---

## 6.11 Composition over inheritance, in Python terms

```python
class Engine: def start(self): ...

class Car:
    def __init__(self): self.engine = Engine()      # HAS-A. Preferred
```

**Say:** *"I default to composition and use inheritance only for genuine is-a relationships. In Python it costs almost nothing, because duck typing means I don't need a shared base class to swap an implementation."*

---

# PART 7 — GENERATORS AND ITERATORS ⭐

## 7.1 The iterator protocol

Two methods. That's the whole thing.

- `__iter__()` → returns the iterator
- `__next__()` → returns the next item, or raises `StopIteration`

`for x in thing:` is just Python calling those in a loop.

```python
it = iter([1, 2, 3])
next(it)     # 1
next(it)     # 2
next(it)     # 3
next(it)     # StopIteration
next(it, None)   # None instead of raising
```

**Iterable vs iterator:**
- **Iterable** = can produce an iterator. A list. Reusable.
- **Iterator** = the cursor itself. One-shot. Consumed once and it's finished.

**Say:** *"An iterable can give you an iterator. The iterator is the cursor and it's exhausted after one pass. That's why iterating a generator twice gives you nothing the second time."*

**Hook:** **Iterable = the book. Iterator = the bookmark.**

---

## 7.2 Generators

**What.** A function with `yield` instead of `return`. Calling it runs **no code** — it hands
back a generator. Each `next()` runs until the next `yield`, then **freezes**, keeping all
local variables.

**Picture.** A vending machine. One item per button press. It doesn't make the whole batch.

```python
def read_big_file(path):
    with open(path) as f:
        for line in f:          # files are already lazy line-by-line
            yield line.strip()

for line in read_big_file("50gb.csv"):
    process(line)               # constant memory. Any file size
```

**Why.** This is the answer to *"the dataset doesn't fit in memory"*. Say it fast.

```python
sum(x*x for x in range(10_000_000))     # generator expression. No list built
[x*x for x in range(10_000_000)]        # builds 10M items in RAM ⚠️
```

**Say:** *"A generator produces values lazily, one at a time, and holds constant memory regardless of input size. It's `IEnumerable` with `yield return`. Round brackets instead of square brackets turns a comprehension lazy."*

**Hook:** **`yield` = one at a time, constant memory.**

**`yield from` — delegate to another generator:**
```python
def combined():
    yield from source_a()
    yield from source_b()
```

**Generators are also coroutines** (the old way): `gen.send(value)`, `gen.throw()`,
`gen.close()`. Modern async uses `async def` instead, but pipelines still use `send`.

⚠️ *"Downside of generators?"* → *"One pass only, no `len()`, no indexing, and you can't restart one. If I need multiple passes I either materialise it or make the source re-iterable."*

---

## 7.3 `itertools` — the ones worth naming

```python
from itertools import (islice, chain, groupby, count, cycle, repeat,
                       accumulate, product, combinations, permutations,
                       takewhile, dropwhile, tee, zip_longest, batched)

islice(gen, 10)               # first 10 of a lazy stream — "take"
chain(a, b)                   # concatenate iterables lazily
accumulate(xs)                # running total ⭐ cumulative P&L
groupby(sorted_rows, key)     # ⚠️ input MUST be sorted by the key first
batched(xs, 100)              # fixed-size chunks (3.12+)
product(a, b) / combinations(xs, 2)
zip_longest(a, b, fillvalue=0)
```

⚠️ **`itertools.groupby` needs sorted input.** Unsorted gives silently wrong groups.
For unsorted data, use `defaultdict(list)`.

---

## 7.4 `collections`

```python
from collections import deque, defaultdict, Counter, namedtuple, ChainMap

deque(maxlen=100)      # ⭐ O(1) at BOTH ends. A rolling window
defaultdict(list)      # missing key → []
Counter(xs)            # frequency count. .most_common(n)
ChainMap(a, b)         # layered lookup — config overrides
```

**`deque` is your rolling-window answer** for streaming data. `maxlen` makes it drop the
oldest automatically.

---

## 7.5 `heapq` and `bisect`

```python
import heapq, bisect

heapq.nlargest(10, xs, key=...)   # top N without sorting everything
heapq.heappush(h, item) / heappop(h)      # min-heap → priority queue
bisect.insort(sorted_list, x)     # keep a list sorted, O(log n) search
bisect.bisect_left(xs, x)         # binary search
```

**Say:** *"For top-N over a huge stream I use a heap of size N — O(n log k) and constant memory. Sorting everything is O(n log n) and needs it all in RAM."*

---

# PART 8 — ERRORS AND `with`

## 8.1 try / except / else / finally

```python
try:
    risky()
except (ValueError, KeyError) as e:      # catch several
    log.warning("bad input: %s", e)
    raise                                # re-raise, keeps the traceback
except Exception as e:
    raise ProcessingError("failed") from e   # chain — preserves the cause
else:
    commit()          # runs ONLY if no exception
finally:
    cleanup()         # ALWAYS runs
```

| Clause | Runs when |
|---|---|
| `except` | that exception happened |
| `else` | **no** exception happened |
| `finally` | always. Even on `return` or `raise` |

**Say:** *"`else` runs only if nothing was raised, so it keeps the try block down to the line that can actually fail. `finally` always runs. And `raise ... from e` chains, so the original cause survives in the traceback."*

---

## 8.2 The exception hierarchy

```
BaseException
 ├── SystemExit, KeyboardInterrupt, GeneratorExit    ← DON'T catch these
 └── Exception                                        ← catch this one
      ├── ValueError, TypeError, KeyError, IndexError, AttributeError
      ├── OSError → FileNotFoundError, PermissionError, TimeoutError
      ├── ArithmeticError → ZeroDivisionError
      └── your own
```

**Say:** *"I catch `Exception`, never `BaseException` — that would swallow Ctrl-C and interpreter shutdown. And a bare `except:` is always a bug in review."*

**Hook:** **Catch `Exception`. Never bare `except:`.**

**Custom exceptions:**
```python
class TradingError(Exception): ...
class InsufficientMargin(TradingError):
    def __init__(self, required, available):
        self.required, self.available = required, available
        super().__init__(f"need {required}, have {available}")
```
One base class per subsystem lets callers catch broadly or narrowly.

**Exception groups (3.11+):**
```python
try:
    async with asyncio.TaskGroup() as tg: ...
except* ValueError as eg: ...      # several failures at once
```

---

## 8.3 EAFP vs LBYL

- **LBYL** — Look Before You Leap: `if key in d: d[key]`
- **EAFP** — Easier to Ask Forgiveness than Permission: `try: d[key] except KeyError:`

**Python prefers EAFP.** It avoids the race between checking and acting, and it's faster when
the exception is rare.

**Say:** *"Python's culture is EAFP — try it and handle failure. It removes the check-then-act race, and exceptions are cheap when they're actually exceptional. LBYL when failure is the common case."*

---

## 8.4 Context managers — `with`

**What.** Guaranteed setup and teardown. `using` in C#, `try/finally` without the noise.

```python
with open("f.csv") as f:        # closed even if the body raises
    data = f.read()

with lock:                      # acquired and released
    ...
with conn.begin():              # transaction: commit or rollback
    ...
with open("a") as a, open("b") as b:    # several at once
    ...
```

**Build one — two ways:**

```python
# 1. the class way
class Timer:
    def __enter__(self):
        self.t = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        print(time.perf_counter() - self.t)
        return False        # False → exception propagates. True → swallowed ⚠️

# 2. the generator way — usually nicer
from contextlib import contextmanager

@contextmanager
def timer():
    t = time.perf_counter()
    try:
        yield
    finally:
        print(time.perf_counter() - t)
```

**Say:** *"A context manager guarantees cleanup even on exception. It's `using` in C#. `__exit__` returning True swallows the exception, which is almost always wrong."*

**Hook:** **`with` = guaranteed cleanup.**

**Also in `contextlib`:** `suppress(FileNotFoundError)`, `closing(x)`, `ExitStack()` for a
dynamic number of resources, `nullcontext()` for an optional one.

---

## 8.5 Logging, not `print`

```python
import logging
log = logging.getLogger(__name__)

log.info("filled order %s qty %s", order_id, qty)   # ⭐ lazy % formatting
log.exception("failed")     # inside an except block: logs the traceback too
```

⚠️ Use `log.info("x %s", y)`, not `log.info(f"x {y}")`. The f-string formats even when the
level is disabled. And structured logs need the raw fields.

**Say:** *"Never `print` in production code. `getLogger(__name__)` gives per-module control, lazy `%` formatting avoids the cost when the level is off, and `log.exception` inside an except block captures the traceback. In services I emit JSON with a correlation id."*

---

# PART 9 — MODULES, IMPORTS, ENVIRONMENTS

## 9.1 Modules and packages

- **Module** = one `.py` file.
- **Package** = a folder of modules. `__init__.py` marks it (optional since 3.3, still clearer).

```python
import mypkg.orders              # import the module
from mypkg.orders import Order   # import a name
from mypkg import orders as o    # alias
from . import sibling            # relative import — inside a package only
```

⚠️ **`from x import *` is banned in real code.** It hides where names came from and breaks
tooling.

**`__init__.py`** runs when the package is first imported. Keep it thin — re-exports only.
Heavy work there slows every import.

---

## 9.2 `if __name__ == "__main__":`

```python
def main(): ...

if __name__ == "__main__":
    main()
```

**What.** `__name__` is `"__main__"` when the file is run directly, and the module's name when
it's imported.

**Why.** Without it, importing the module **executes** its top-level code. On Windows,
`multiprocessing` will fork-bomb without this guard.

**Say:** *"It's the entry-point guard. It separates 'run me' from 'import me', and it's mandatory when using multiprocessing on Windows, because child processes re-import the module."*

---

## 9.3 How imports resolve, and circular imports

Python searches `sys.path`: the script's directory, then `PYTHONPATH`, then site-packages.
Imported modules are cached in `sys.modules` — **a module's top level runs once per process.**

**Circular import** = A imports B, B imports A. You get a half-built module and an
`ImportError` or `AttributeError`.

**Three fixes, in order:**
1. Extract the shared piece into a third module. (Best — the cycle is a design smell.)
2. Move the import inside the function that needs it.
3. `if TYPE_CHECKING:` for type-hint-only imports.

**Say:** *"A circular import is a design signal, not a syntax problem. The right fix is to pull the shared abstraction into its own module. A function-local import is the pragmatic patch."*

---

## 9.4 Virtual environments and dependencies

```bash
python -m venv .venv                 # create
source .venv/bin/activate            # Linux/Mac
.venv\Scripts\activate               # Windows
pip install -r requirements.txt
pip freeze > requirements.txt        # ⚠️ pins everything, including transitives
```

| Tool | What it is |
|---|---|
| `venv` + `pip` | the built-in baseline |
| **`uv`** | ⭐ current best. Rust-based. 10–100× faster than pip. Resolver + venv + lockfile |
| `poetry` | dependency resolution + lockfile + publishing |
| `pip-tools` | `requirements.in` → pinned `requirements.txt` |
| `conda` | for the scientific stack and non-Python binaries |

**Say:** *"One virtualenv per project so dependency trees never collide. I want a lockfile — `uv` or Poetry — so CI and production install byte-identical trees. Bare `pip freeze` isn't a lockfile; it's a snapshot with no hashes and no resolution."*

**Hook:** **Env per project. Lockfile always.**

---

## 9.5 Packaging

Modern config lives in one file: **`pyproject.toml`** (PEP 621).
`setup.py` is legacy. Build with `python -m build`, publish with `twine`.

---

# PART 10 — FILES, JSON, CSV

## 10.1 Reading and writing

```python
with open("f.csv", "r", encoding="utf-8") as f:    # ⭐ ALWAYS name the encoding
    for line in f:            # lazy. Doesn't load the file
        ...

with open("out.txt", "w", encoding="utf-8") as f:
    f.write("x")

with open("blob.bin", "rb") as f:     # binary → gives bytes
    ...
```

| Mode | Meaning |
|---|---|
| `r` | read (default) |
| `w` | write — **truncates** |
| `a` | append |
| `x` | create, fail if it exists |
| `+` | read and write |
| `b` | binary |

⚠️ **Always pass `encoding="utf-8"`.** The default is platform-dependent — this is the classic
"works on Linux, breaks on Windows" bug.

---

## 10.2 `pathlib` — not `os.path`

```python
from pathlib import Path

p = Path("data") / "raw" / "trades.csv"    # / joins, cross-platform
p.exists() / p.is_file() / p.stat().st_size
p.suffix / p.stem / p.name / p.parent
p.read_text(encoding="utf-8")
p.write_text("x", encoding="utf-8")
list(p.parent.glob("*.csv"))
p.parent.mkdir(parents=True, exist_ok=True)
```

**Say:** *"`pathlib` is object-oriented paths. The `/` operator joins portably, so no string concatenation and no separator bugs."*

---

## 10.3 JSON and CSV

```python
import json
json.dumps(obj, indent=2, default=str)    # default=str handles dates/Decimal
json.loads(s)
json.dump(obj, f) / json.load(f)          # to/from a file object
```

⚠️ JSON has no date and no Decimal type. Dumping a `Decimal` raises. Use `default=str`, or
better, serialise through Pydantic.

```python
import csv
with open("t.csv", newline="") as f:      # ⚠️ newline="" is required
    for row in csv.DictReader(f):
        row["price"]
```

For anything large, **pandas** (Part 16). For huge files, generators (Part 7).

---

# PART 11 — DATES AND MONEY 💰

Capital markets role. **These get asked.**

## 11.1 Dates and times

```python
from datetime import datetime, timezone, timedelta, date
from zoneinfo import ZoneInfo          # stdlib since 3.9. No pytz needed

datetime.now(timezone.utc)             # ⭐ ALWAYS do this
datetime.utcnow()                      # ⚠️ NAIVE. Deprecated. Never use it

dt = datetime.now(ZoneInfo("Asia/Dubai"))
dt.astimezone(timezone.utc)
dt.isoformat()                         # "2026-08-03T17:00:00+04:00"
datetime.fromisoformat(s)
(a - b).total_seconds()
```

**Naive vs aware.** A naive datetime has no timezone. An aware one does.
Comparing them raises `TypeError`.

**Say:** *"Store and compute in UTC, convert to local only for display. `utcnow` is deprecated because it returns a naive datetime that looks like UTC — that's a whole class of bugs. I use `datetime.now(timezone.utc)` and `zoneinfo` for market timezones."*

**Hook:** **UTC everywhere. Convert at the screen.**

⚠️ **Financial angle:** trading calendars and settlement dates aren't calendar arithmetic.
T+2 skips weekends and market holidays. Say: *"I'd use a business-day calendar — `pandas`
`CustomBusinessDay` or `exchange_calendars` — never `timedelta(days=2)`."*

---

## 11.2 Money

```python
from decimal import Decimal, getcontext, ROUND_HALF_UP

Decimal("0.1") + Decimal("0.2")     # exactly 0.3
Decimal(0.1)                        # ⚠️ WRONG — inherits the float's error
getcontext().rounding = ROUND_HALF_UP
amount.quantize(Decimal("0.01"))    # round to 2dp explicitly
```

**Three rules:**
1. **Always construct from a string**, never from a float.
2. Choose rounding explicitly. Python's default is banker's rounding (`ROUND_HALF_EVEN`).
3. Alternative: store **integer minor units** (pennies, cents). Fast and exact.

**Say:** *"Money is `Decimal` built from strings, or integer minor units. Never float — binary floating point can't represent 0.1, and the error compounds across a book. Rounding mode is a business decision, so I set it explicitly rather than take the default."*

**Hook:** **Decimal from strings. Or count the pennies.**

⚠️ *"Isn't Decimal slow?"* → *"Yes, roughly 10–20× slower than float. So I use `Decimal` for money and settlement, and `float`/NumPy for statistics, risk and pricing models where the precision is already approximate. Different jobs."*

---

# PART 12 — TYPE HINTS

## 12.1 The syntax

```python
def total(xs: list[float], rate: float = 0.1) -> float: ...

from typing import Optional, Any, Callable, Iterable, Literal, TypedDict, Protocol

x: int | None = None            # 3.10+. Same as Optional[int]
y: str | int                    # union
c: Callable[[int, str], bool]   # a function taking (int, str), returning bool
side: Literal["BUY", "SELL"]    # only these exact values
d: dict[str, list[int]]         # 3.9+ built-in generics. No typing.Dict needed

class Row(TypedDict):           # a dict with known keys
    symbol: str
    qty: int
```

---

## 12.2 The critical fact

**Type hints are NOT enforced at runtime.** They're erased. Nothing checks them.

```python
def f(x: int) -> int: return x
f("hello")      # runs fine. Returns "hello"
```

**Say:** *"Hints are erased at runtime, exactly like TypeScript. They're for the editor, for mypy in CI, and for the next human. Anything crossing a boundary gets validated for real with Pydantic — which does check at runtime, because it reads the same annotations."*

**Hook:** **Hints for humans and CI. Pydantic for reality.**

⚠️ *"Why bother then?"* → *"They catch a class of bug before it runs, they make refactoring safe, and they're the best documentation there is because they can't go stale — CI fails if they lie."*

---

## 12.3 Practice

- `mypy --strict` on new code, looser on legacy.
- `from __future__ import annotations` — makes all annotations lazy strings. Fixes forward
  references and circular-import-only-for-types.
- `if TYPE_CHECKING:` — import types without a runtime import.
- Generics: `def first[T](xs: list[T]) -> T:` (3.12 syntax) or `TypeVar` before that.

---

# PART 13 — THE GIL AND CONCURRENCY ⭐⭐⭐

**This is the most likely deep-dive topic in the whole file. Know it cold.**

## 13.1 The GIL, in plain words

**What.** The Global Interpreter Lock. One mutex. Only **one thread** executes Python bytecode
at a time, per process.

**Picture.** An office with eight staff but one keyboard. Only one can type at a time.

**So:**
- Waiting on network or disk? The lock is **released** while you wait → threads help. ✅
- Doing heavy maths in Python? The lock is **held** → threads don't help. ❌
- NumPy / pandas? They **release the GIL** inside C code → real parallelism. ✅

**Why it exists.** It makes CPython's reference counting safe and single-threaded code fast.
Removing it was historically a 30–40% single-thread slowdown.

**Say:** *"The GIL means only one thread runs Python bytecode at a time. So threads help with I/O — the lock is released while waiting — but not with CPU-bound work. For CPU work I use `multiprocessing`, or NumPy, which drops the GIL in C. Python 3.13 ships an optional free-threaded build that removes it, and 3.14 supports it officially, but it isn't the default yet."*

**Hook:** **One keyboard. Waiting is free, typing isn't.**

---

## 13.2 The decision table — memorise this

| Your work | Use | Why |
|---|---|---|
| Network, disk, DB, HTTP — **waiting** | **`asyncio`** | thousands of tasks, one thread, cheapest |
| Waiting, but the library is blocking | **threads** (`ThreadPoolExecutor`) | GIL is released during the wait |
| Heavy maths in pure Python | **`multiprocessing`** | one GIL per process → real cores |
| Heavy maths on arrays | **NumPy / pandas** | ⭐ vectorised C, releases the GIL |
| Mixed | asyncio + `run_in_executor` | async shell, blocking work pushed out |
| Across machines | Celery, Dask, Ray | past one box |

**Say it as one line:** *"**Waiting → asyncio or threads. Working → processes or NumPy.**"*

---

## 13.3 asyncio

**What.** One thread, one event loop. When a task waits, the loop runs another task.

**Picture.** One waiter, twenty tables. While the kitchen cooks, the waiter serves others.
Not more waiters — one waiter who never stands still.

```python
import asyncio

async def fetch(client, url):          # a coroutine
    r = await client.get(url)          # ⭐ await = "pause me, run someone else"
    return r.json()

async def main():
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*[fetch(client, u) for u in urls])

asyncio.run(main())
```

| Word | Meaning |
|---|---|
| `async def` | defines a coroutine. Calling it **runs nothing** — it returns an object |
| `await` | run it and pause here. Yields control to the loop |
| `asyncio.run(m())` | start the loop |
| `gather(*tasks)` | run concurrently, wait for all |
| `TaskGroup` | 3.11+. Structured. **If one fails, the rest are cancelled** ⭐ |
| `create_task(c)` | fire it off now, await later |
| `Semaphore(10)` | cap concurrency |
| `wait_for(c, 5)` | timeout |
| `to_thread(fn)` | run blocking code off the loop ⭐ |
| `Queue` | producer/consumer between tasks |

**The modern version:**
```python
async with asyncio.TaskGroup() as tg:      # 3.11+. Prefer this over gather
    for u in urls:
        tg.create_task(fetch(client, u))
```

**Say:** *"asyncio is cooperative concurrency on one thread. `await` is a yield point where the loop can run something else. It's `async/await` in C#, but with a single-threaded loop instead of a thread pool — so the failure mode is different."*

⚠️ **THE TRAP — know this cold.**
> *"One blocking call freezes the entire loop, because there's only one thread. `time.sleep`, `requests`, a synchronous DB driver — any of them stalls every task. Rules: never call blocking code inside a coroutine; use async libraries (`httpx`, `asyncpg`, `aiofiles`); and if a library has no async version, wrap it in `asyncio.to_thread`. In production I run the loop with `debug=True` in staging, which logs any callback that blocks too long."*

⚠️ **CPU work inside asyncio is the same bug.** A tight numeric loop blocks the event loop
just like `time.sleep`. Push it to a `ProcessPoolExecutor`.

⚠️ *"`gather` vs `TaskGroup`?"* → *"`gather` collects results but by default one failure leaves the others running. `TaskGroup` is structured concurrency — a failure cancels the siblings and raises an ExceptionGroup. I default to TaskGroup on 3.11+."*

---

## 13.4 Threads

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=20) as ex:
    results = list(ex.map(fetch_url, urls))
```

**Locks and friends:**
```python
import threading
lock = threading.Lock()          # mutual exclusion
rlock = threading.RLock()        # re-entrant — same thread can take it twice
sem = threading.Semaphore(5)     # cap concurrency
ev = threading.Event()           # signal between threads
local = threading.local()        # per-thread storage
q = queue.Queue()                # ⭐ thread-safe. Prefer this to shared state
```

⚠️ *"Are Python operations atomic?"* → *"Some are, by accident of the GIL — `list.append` for instance. But `x += 1` is read-modify-write across several bytecodes and is **not** atomic. I don't rely on GIL side effects; I use a lock or a `queue.Queue`."*

**Say:** *"Threads are for blocking I/O. The GIL is released during the wait, so twenty threads on twenty HTTP calls really do overlap. For anything CPU-bound they just add context-switching overhead."*

---

## 13.5 Processes

```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor() as ex:
    results = list(ex.map(heavy_calc, chunks))
```

**Costs, and say them:**
- Each process has its own interpreter and memory. **Startup is expensive** (~50–100ms).
- Arguments and results are **pickled**. Lambdas and local functions can't be pickled.
- Big data transfer dominates. Use `shared_memory` or memory-mapped files for large arrays.
- On Windows it's **spawn**, not fork — so the module is re-imported. Hence the
  `if __name__ == "__main__":` guard.

**Say:** *"Processes give real parallelism because each has its own GIL. The cost is startup and pickling, so I only use them when the compute per task clearly exceeds that overhead — coarse chunks, not per-row."*

---

## 13.6 The free-threaded build (3.13+) — the "current" answer

**What.** An optional CPython build with no GIL (`python3.13t`). Threads run Python bytecode
in genuine parallel.

**The catch:** single-threaded code is somewhat slower, and C extensions must be rebuilt and
declared safe.

**Say:** *"3.13 introduced an official free-threaded build and 3.14 supports it properly. It's not the default yet, and the ecosystem is still catching up. So for production today my answer is still processes or NumPy — but it's genuinely changing."*

⚠️ Also worth one line: **sub-interpreters** (PEP 734, 3.12/3.13) — multiple interpreters in
one process, each with its own GIL. A middle ground between threads and processes.

---

# PART 14 — MEMORY AND SPEED

## 14.1 The method — say this before any optimisation answer

> *"Measure first. I never optimise on a hunch.
> `cProfile` for where the time goes, `timeit` for micro-benchmarks,
> `tracemalloc` or `memray` for memory, `py-spy` for a live process I can't restart.
> Then I fix the biggest item and measure again."*

```python
python -m cProfile -s cumtime app.py
python -m timeit -s "setup" "code"
py-spy top --pid 1234          # ⭐ sampling profiler, no restart, prod-safe
```

**Hook:** **Measure, fix the top item, measure again.**

---

## 14.2 The wins, in the order you'd try them

| # | Fix | Typical gain |
|---|---|---|
| 1 | **Better algorithm / data structure** (list `in` → set) | 10–1000× |
| 2 | **Vectorise with NumPy/pandas** instead of looping | 10–100× |
| 3 | **Cache** — `functools.cache`, Redis | huge on repeats |
| 4 | **Batch I/O** — kill the N+1 query, bulk insert | 10–100× |
| 5 | Move I/O to async or threads | throughput, not latency |
| 6 | Move CPU work to processes | ~number of cores |
| 7 | `__slots__`, generators, `array` | memory |
| 8 | Local variable lookups, avoid attribute access in loops | 10–30% |
| 9 | Rewrite the hot function in **Cython / Rust (PyO3) / C** | 10–100× |
| 10 | Try **PyPy** | 2–10× on pure Python |

**Say:** *"The order matters. Algorithm first, then vectorise, then cache, then batch I/O. Rewriting in C is last, because by then the cheap wins are gone."*

---

## 14.3 Memory tools

```python
import sys, tracemalloc
sys.getsizeof(obj)               # ⚠️ shallow. Doesn't follow references

tracemalloc.start()
snap1 = tracemalloc.take_snapshot()
# ... work ...
snap2 = tracemalloc.take_snapshot()
snap2.compare_to(snap1, "lineno")[:10]      # ⭐ the leak-hunting answer
```

**Memory savers:** `__slots__`, generators instead of lists, `array.array` or NumPy instead
of lists of numbers, `Decimal` only where needed, interning repeated strings.

---

# PART 15 — STANDARD LIBRARY TOUR

Name-drop these. Knowing the library is a seniority signal.

| Module | What it's for |
|---|---|
| `collections` | `deque`, `defaultdict`, `Counter`, `ChainMap` |
| `itertools` | lazy iterator tools |
| `functools` | `cache`, `wraps`, `partial`, `reduce` |
| `dataclasses` | boilerplate-free data objects |
| `typing` | type hints |
| `pathlib` | paths |
| `datetime`, `zoneinfo` | time |
| `decimal`, `fractions` | exact numbers |
| `json`, `csv`, `tomllib`, `pickle` | serialisation |
| `re` | regex. `compile` once, reuse |
| `logging` | structured logs |
| `argparse` | CLIs |
| `os`, `sys`, `shutil`, `subprocess` | the system |
| `threading`, `multiprocessing`, `asyncio`, `concurrent.futures` | concurrency |
| `queue` | thread-safe queues |
| `sqlite3` | a real DB, no server |
| `hashlib`, `hmac`, `secrets` | ⭐ crypto. `secrets`, never `random`, for tokens |
| `uuid` | ids |
| `unittest`, `doctest` | built-in testing |
| `statistics` | mean, median, stdev |
| `bisect`, `heapq` | sorted lists, heaps |
| `enum` | proper enums |
| `contextlib` | `with` helpers |
| `weakref` | caches that don't leak |
| `struct` | binary packing — market data feeds |
| `socket`, `ssl` | networking |
| `warnings` | deprecations |

⚠️ **`pickle` is unsafe.** Unpickling untrusted data executes arbitrary code. Say that if it
comes up. Use JSON, or msgpack, or protobuf across trust boundaries.

⚠️ **`random` is not secure.** For tokens, passwords, nonces: `secrets`.

---

# PART 16 — NUMPY AND PANDAS

## 16.1 NumPy

**What.** A fixed-type, contiguous N-dimensional array with operations implemented in C.

```python
import numpy as np
a = np.array([1.0, 2.0, 3.0])
a * 2                        # whole array at once. No loop
a[a > 1]                     # boolean mask ⭐
a.mean() / a.std() / a.cumsum()
np.dot(a, b)
a.reshape(3, 1)
a.astype(np.float32)         # halve the memory
```

**Why it's fast — three reasons, say all three:**
1. Contiguous memory, one dtype → cache friendly.
2. The loop runs in C, not in the interpreter.
3. **It releases the GIL**, and uses SIMD and BLAS.

**Broadcasting.** Shapes are stretched to match without copying: `(3,1) + (1,4)` → `(3,4)`.

**Say:** *"NumPy is a typed contiguous buffer with vectorised C operations. That's why it's 10–100× faster than a Python loop, and why it sidesteps the GIL — the heavy work happens in C with the lock released."*

**Hook:** **Typed, contiguous, C, no GIL.**

---

## 16.2 Pandas

```python
import pandas as pd
df = pd.read_csv("trades.csv", parse_dates=["ts"])

df.head() / .info() / .describe() / .dtypes
df[df.qty > 100]                        # filter
df.loc[rows, cols]                      # label-based
df.iloc[0:5, 0:2]                       # position-based
df.groupby("symbol").agg({"qty": "sum", "price": "mean"})
df.merge(other, on="id", how="left")    # a SQL join
df.pivot_table(...)
df.sort_values("ts")
df.assign(notional=df.qty * df.price)   # ⭐ chainable, no mutation
df.resample("1min").ohlc()              # ⭐ time-series bars
df.rolling(20).mean()                   # rolling window
df["price"].pct_change()                # returns
```

**The performance rules — the whole pandas interview:**

| Never | Always |
|---|---|
| `for i, row in df.iterrows()` | vectorised column operations |
| `df.apply(fn, axis=1)` | `np.where`, `.map`, or a vectorised expression |
| `df = pd.concat([df, row])` in a loop | build a list, concat **once** |
| `object` dtype for repeated strings | `category` dtype |
| float64 everywhere | downcast to float32/int32 |

**Say:** *"The first thing I check in slow pandas is row iteration. `iterrows` and `apply(axis=1)` fall back to Python per row. Vectorising — one operation on the whole column — is usually 10 to 100 times faster. After that: category dtypes for repeated strings, downcast numerics, and read only the columns I need."*

**Financial angle — the point-in-time join.** Worth having ready:
```python
pd.merge_asof(trades, quotes, on="ts", by="symbol", direction="backward")
```
> *"`merge_asof` joins each trade to the most recent prior quote. It's how you avoid look-ahead bias — a plain join on timestamp would let future data leak into a backtest."*

**When pandas isn't enough:** **Polars** (Rust, multi-threaded, lazy — genuinely faster),
**DuckDB** (SQL over Parquet, out-of-core), **Dask/Spark** (cluster),
**PyArrow/Parquet** (columnar storage). Naming these shows range.

---

# PART 17 — TESTING

```python
import pytest

def test_notional():
    assert Trade("VOD", 10, 2.5).notional == 25

@pytest.fixture
def account():                       # setup, reusable, torn down after
    return Account("awais", 100)

@pytest.mark.parametrize("qty,expected", [(1, 10), (2, 20)])
def test_many(qty, expected):
    assert calc(qty) == expected

def test_raises():
    with pytest.raises(InsufficientMargin):
        account.withdraw(1000)

def test_mock(mocker):               # pytest-mock
    mocker.patch("app.gateway.send", return_value=True)
```

| Tool | For |
|---|---|
| `pytest` | the standard |
| fixtures | setup/teardown, dependency injection |
| `parametrize` | table-driven tests |
| `unittest.mock` / `pytest-mock` | fakes and spies |
| `pytest-cov` | coverage |
| `hypothesis` | ⭐ property-based testing — generates edge cases for you |
| `freezegun` | freeze time |
| `pytest-asyncio` | testing coroutines |
| `testcontainers` | a real DB in Docker for integration tests |

**Say:** *"pytest with fixtures and parametrize. I mock at the boundary — the HTTP client, the clock, the broker gateway — not the domain logic. Coverage is a smoke detector, not a goal; I'd rather have fewer tests that assert behaviour than 100% coverage of getters. For pricing and P&L maths I use `hypothesis`, because property-based testing finds the edge cases a human wouldn't write."*

**Hook:** **Mock the boundary, not the logic.**

---

# PART 18 — SECURITY AND PRODUCTION

| Risk | The answer |
|---|---|
| SQL injection | parameterised queries. Never f-string SQL |
| `pickle` | never on untrusted data. It executes code |
| `eval` / `exec` | never on user input |
| secrets in code | env vars or a vault. Never in git |
| weak randomness | `secrets`, not `random` |
| passwords | `bcrypt` / `argon2`. Never a plain hash |
| dependency CVEs | `pip-audit`, Dependabot, lockfiles |
| YAML | `yaml.safe_load`, never `yaml.load` |
| ZIP/tar extraction | validate paths — zip-slip |
| logging | never log tokens, PANs or PII |
| SAST | `bandit`, `ruff` security rules in CI |

**Say:** *"Parameterised queries, secrets from the environment or a vault, `secrets` for anything random that matters, and `pip-audit` plus a lockfile in CI. Never `pickle` or `yaml.load` on anything that crossed a network."*

---

# PART 19 — PYTHON ⇄ C# TRANSLATION ⭐

Use this constantly. It's your fastest route to a confident answer.

| Python | C# / .NET |
|---|---|
| `list` | `List<T>` |
| `dict` | `Dictionary<K,V>` |
| `set` | `HashSet<T>` |
| `tuple` | `ValueTuple` / record |
| `deque` | `LinkedList` / `Queue` |
| comprehension | LINQ `Select` / `Where` |
| generator, `yield` | `IEnumerable<T>`, `yield return` |
| `with` | `using` |
| decorator | attribute + interceptor / middleware |
| `@property` | property with a getter |
| `@staticmethod` | `static` method |
| `@classmethod` | static factory method |
| duck typing | interfaces, but implicit |
| `Protocol` | interface, structurally checked |
| `ABC` | abstract class |
| dataclass | `record` |
| Pydantic | FluentValidation + model binding |
| `None` | `null` |
| `Optional[T]` / `T \| None` | `T?` |
| type hints | erased — like TypeScript, **not** like C# generics |
| `asyncio` | `async`/`await`, but one thread not a pool |
| `Task` | `Task` |
| `gather` | `Task.WhenAll` |
| `TaskGroup` | `Parallel` + structured cancellation |
| threads | threads, but the GIL blocks CPU parallelism |
| `multiprocessing` | separate processes |
| GIL | *(no equivalent — this is the key difference)* |
| refcount + cycle GC | generational GC only |
| `pytest` | xUnit / NUnit |
| `pip` + `venv` | NuGet |
| `pyproject.toml` | `.csproj` |
| PyPI | nuget.org |
| `logging` | `ILogger` |
| FastAPI | ASP.NET Core Minimal API |
| Django | ASP.NET MVC + EF + Identity, batteries included |
| SQLAlchemy | Entity Framework |
| Alembic | EF Migrations |
| Celery | Hangfire / Azure Functions |

**Say when asked "how do you compare them?":**
> *"C# gives me a compiler that actually enforces the contract, real threading, and better raw performance. Python gives me faster iteration and an unmatched data and ML ecosystem. In this kind of stack I'd use .NET for the transactional core and Python for analytics and quant work, with a versioned contract between them so neither leaks into the other."*

---

# PART 20 — CODING EXERCISES

**Do three of these on a timer. Say what you're doing while you type — they're assessing
communication as much as code.**

### 20.1 Rolling VWAP, O(1) per tick
```python
from collections import deque

class RollingVWAP:
    """Volume-weighted average price over the last N ticks."""
    def __init__(self, window: int):
        self.q = deque(maxlen=window)
        self.pv = 0.0        # running sum of price*volume
        self.v = 0.0         # running sum of volume

    def add(self, price: float, volume: float) -> float:
        if len(self.q) == self.q.maxlen:          # about to evict
            old_p, old_v = self.q[0]
            self.pv -= old_p * old_v
            self.v -= old_v
        self.q.append((price, volume))
        self.pv += price * volume
        self.v += volume
        return self.pv / self.v if self.v else 0.0
```
**Say while writing:** *"`deque` with `maxlen` evicts automatically. I keep running sums so each tick is O(1) instead of re-summing the window."*

### 20.2 Realised P&L, FIFO
```python
from collections import deque, defaultdict
from decimal import Decimal

def realised_pnl(trades) -> dict[str, Decimal]:
    """trades: (symbol, side, qty, price). FIFO matching."""
    lots = defaultdict(deque)
    pnl = defaultdict(Decimal)
    for symbol, side, qty, price in trades:
        if side == "BUY":
            lots[symbol].append([qty, price])
        else:
            remaining = qty
            while remaining and lots[symbol]:
                lot = lots[symbol][0]
                matched = min(remaining, lot[0])
                pnl[symbol] += matched * (price - lot[1])
                lot[0] -= matched
                remaining -= matched
                if lot[0] == 0:
                    lots[symbol].popleft()
    return dict(pnl)
```
**Say:** *"FIFO lot matching. A deque per symbol, and Decimal because it's money."*

### 20.3 Top N from a huge file, constant memory
```python
import heapq

def top_n(path: str, n: int):
    def rows():
        with open(path, encoding="utf-8") as f:
            for line in f:
                sym, qty = line.split(",")
                yield int(qty), sym
    return heapq.nlargest(n, rows())
```
**Say:** *"Generator so the file never loads, heap so memory is O(n) not O(file)."*

### 20.4 Group things — covers half of all exercises
```python
from collections import defaultdict

groups = defaultdict(list)
for t in trades:
    groups[t.symbol].append(t)
```

### 20.5 Async fan-out with a concurrency limit
```python
import asyncio

async def fetch_all(urls, limit=10):
    sem = asyncio.Semaphore(limit)
    async def one(u):
        async with sem:
            return await client.get(u)
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(one(u)) for u in urls]
    return [t.result() for t in tasks]
```
**Say:** *"Semaphore caps concurrency so I don't melt the downstream service. TaskGroup so a failure cancels the siblings instead of leaking tasks."*

### 20.6 A timing decorator
```python
import functools, time, logging
log = logging.getLogger(__name__)

def timed(fn):
    @functools.wraps(fn)
    def wrapper(*a, **kw):
        t = time.perf_counter()
        try:
            return fn(*a, **kw)
        finally:
            log.info("%s took %.1fms", fn.__name__, (time.perf_counter() - t) * 1000)
    return wrapper
```
**Say:** *"`wraps` to keep the identity, `finally` so it still logs on an exception, `perf_counter` because it's monotonic."*

### 20.7 LRU cache by hand (asked as a data-structure question)
```python
from collections import OrderedDict

class LRU:
    def __init__(self, cap): self.cap, self.d = cap, OrderedDict()
    def get(self, k):
        if k not in self.d: return None
        self.d.move_to_end(k)
        return self.d[k]
    def put(self, k, v):
        if k in self.d: self.d.move_to_end(k)
        self.d[k] = v
        if len(self.d) > self.cap: self.d.popitem(last=False)
```

### 20.8 Parse a fixed-width / FIX-style message
```python
def parse_fix(msg: str) -> dict[str, str]:
    return dict(field.split("=", 1) for field in msg.strip("\x01").split("\x01"))
```

---

# PART 21 — RAPID-FIRE: 200 QUESTIONS

**Cover the right column. Say the answer out loud. Target 160+.**

### A. Core language (1–40)

| # | Q | A |
|---|---|---|
| 1 | Is Python compiled or interpreted? | Compiled to bytecode, then interpreted. No JIT in CPython |
| 2 | What's `__pycache__`? | Cached bytecode. Faster startup |
| 3 | Variable = ? | A name bound to an object. A label, not a box |
| 4 | Pass by value or reference? | Pass by object reference |
| 5 | Mutable types? | list, dict, set, bytearray, your classes |
| 6 | Immutable types? | int, float, str, bytes, tuple, frozenset, range, None |
| 7 | `is` vs `==`? | Identity vs value |
| 8 | When use `is`? | `None`, `True`, `False`, sentinels |
| 9 | Why is `257 is 257` False? | Only −5..256 are cached |
| 10 | What's interning? | Reusing identical short strings/small ints |
| 11 | Shallow vs deep copy? | New container vs copied all the way down |
| 12 | Falsy values? | False, None, 0, 0.0, "", [], (), {}, set(), range(0) |
| 13 | `{}` creates what? | An empty **dict**. Use `set()` for a set |
| 14 | Is `bool` an int? | Yes, a subclass. `True == 1` |
| 15 | `7/2`? | 3.5 — always a float |
| 16 | `7//2`? | 3 |
| 17 | `-7//2`? | −4. Floors down, unlike C# |
| 18 | Do ints overflow? | No. Arbitrary precision |
| 19 | Why not float for money? | Binary can't represent 0.1. Error compounds |
| 20 | Money: use what? | `Decimal` from strings, or integer pennies |
| 21 | Fast string building? | `"".join(parts)` |
| 22 | Why is `+=` in a loop bad? | Strings are immutable → O(n²) |
| 23 | `str` vs `bytes`? | Text vs raw octets |
| 24 | List cost of `in`? | O(n) |
| 25 | Set cost of `in`? | O(1) |
| 26 | Dict lookup cost? | O(1) average |
| 27 | Are dicts ordered? | Yes, insertion order, guaranteed since 3.7 |
| 28 | What can be a dict key? | Anything hashable → immutable |
| 29 | `list.pop(0)` cost? | O(n). Use `deque` |
| 30 | O(1) at both ends? | `collections.deque` |
| 31 | `[[0]*3]*3` bug? | Three references to one row |
| 32 | Single-element tuple? | `(1,)` — the comma matters |
| 33 | Slicing rule? | Start inclusive, stop exclusive |
| 34 | Reverse a list? | `xs[::-1]` |
| 35 | Comprehension = ? | LINQ. Faster than loop+append |
| 36 | `(x for x in xs)` is? | A generator, lazy — not a tuple |
| 37 | Walrus operator? | `:=` — assign inside an expression |
| 38 | `match` is? | Structural pattern matching, 3.10+ |
| 39 | `x or default` risk? | Wrong when 0 or "" is valid |
| 40 | `and`/`or` return? | An operand, not a bool |

### B. Functions and decorators (41–65)

| # | Q | A |
|---|---|---|
| 41 | `*args`? | Extra positionals, as a tuple |
| 42 | `**kwargs`? | Extra keywords, as a dict |
| 43 | After a bare `*`? | Keyword-only params |
| 44 | Before `/`? | Positional-only params |
| 45 | Mutable default bug? | Created once at def time, shared |
| 46 | Fix it? | Default `None`, build inside |
| 47 | LEGB? | Local, Enclosing, Global, Built-in |
| 48 | `UnboundLocalError` cause? | Assigning makes the name local everywhere |
| 49 | `global` vs `nonlocal`? | Module scope vs enclosing function |
| 50 | Closure? | Function + captured variables |
| 51 | Late binding bug? | Lambdas in a loop capture the variable |
| 52 | Fix? | `lambda i=i: i` |
| 53 | Decorator? | Function that wraps a function |
| 54 | Why `functools.wraps`? | Preserves `__name__`, docs, signature |
| 55 | Decorator with args? | Three nested levels |
| 56 | `lru_cache` limits? | Hashable args only. Holds refs forever |
| 57 | `cache` vs `lru_cache`? | Unbounded vs bounded |
| 58 | `partial`? | Pre-fill arguments |
| 59 | `singledispatch`? | Overload by first argument type |
| 60 | Lambda limit? | One expression only |
| 61 | Faster than lambda in sort? | `operator.itemgetter` / `attrgetter` |
| 62 | Are functions objects? | Yes. First class |
| 63 | Recursion limit? | ~1000. `sys.setrecursionlimit` |
| 64 | Tail-call optimised? | No |
| 65 | Return several values? | A tuple |

### C. Classes and OOP (66–100)

| # | Q | A |
|---|---|---|
| 66 | `self`? | The instance. Explicit |
| 67 | `__init__` vs `__new__`? | Populate vs create |
| 68 | Constructor overloading? | No. Use `@classmethod` factories |
| 69 | Class vs instance attribute? | Shared vs per object |
| 70 | Mutable class attribute? | Shared-state bug |
| 71 | `_x`? | Convention: internal |
| 72 | `__x`? | Name-mangled. Still not private |
| 73 | Real private? | Doesn't exist |
| 74 | `@property`? | A method that reads like a field |
| 75 | `@staticmethod`? | No self, no cls |
| 76 | `@classmethod`? | Gets `cls`. Factories |
| 77 | `super()`? | Next class in the MRO |
| 78 | MRO? | C3 linearisation |
| 79 | Diamond problem? | Solved — base appears once |
| 80 | `__repr__` vs `__str__`? | Developer vs user |
| 81 | `__eq__` without `__hash__`? | Object becomes unhashable |
| 82 | Make it iterable? | `__iter__` |
| 83 | Make it callable? | `__call__` |
| 84 | Make it work in `with`? | `__enter__`/`__exit__` |
| 85 | `__slots__`? | Fixed attributes. ~40–50% less memory |
| 86 | `__slots__` cost? | No dynamic attributes, no `__dict__` |
| 87 | Duck typing? | Shape matters, not the declared type |
| 88 | `ABC` vs `Protocol`? | Must inherit vs must match |
| 89 | Descriptor? | Object controlling attribute access |
| 90 | `@property` is a…? | Descriptor |
| 91 | Metaclass? | The class of a class |
| 92 | Who uses metaclasses? | Django models, ABCs, ORMs |
| 93 | Dataclass gives? | `__init__`, `__repr__`, `__eq__` |
| 94 | Does it validate? | **No** |
| 95 | `frozen=True`? | Immutable and hashable |
| 96 | Mutable dataclass default? | `field(default_factory=list)` |
| 97 | Pydantic vs dataclass? | Runtime validation and coercion |
| 98 | `NamedTuple`? | Immutable, tuple-like record |
| 99 | Multiple inheritance use? | Mixins |
| 100 | Composition vs inheritance? | Default to composition |

### D. GIL, async, concurrency (101–135)

| # | Q | A |
|---|---|---|
| 101 | GIL? | One thread runs bytecode at a time |
| 102 | Why does it exist? | Makes refcounting safe, single-thread fast |
| 103 | Threads help with? | I/O waiting |
| 104 | Threads don't help with? | CPU-bound Python |
| 105 | CPU-bound answer? | Processes, or NumPy |
| 106 | Why does NumPy escape it? | Releases the GIL inside C |
| 107 | Is the GIL going? | 3.13 optional free-threaded build; 3.14 supported. Not default |
| 108 | Sub-interpreters? | One GIL each, one process. PEP 734 |
| 109 | asyncio model? | One thread, one event loop |
| 110 | `await` means? | Pause me, run something else |
| 111 | Does calling `async def` run it? | No — returns a coroutine |
| 112 | Start the loop? | `asyncio.run(main())` |
| 113 | Run many concurrently? | `gather` or `TaskGroup` |
| 114 | `gather` vs `TaskGroup`? | TaskGroup cancels siblings on failure |
| 115 | Cap concurrency? | `asyncio.Semaphore` |
| 116 | Timeout? | `asyncio.wait_for` / `asyncio.timeout` |
| 117 | Biggest asyncio trap? | One blocking call freezes everything |
| 118 | Fix for blocking code? | `asyncio.to_thread` |
| 119 | CPU work in asyncio? | Same bug. Use a process pool |
| 120 | `time.sleep` in a coroutine? | Blocks the loop. Use `asyncio.sleep` |
| 121 | Async HTTP client? | `httpx` or `aiohttp`. Not `requests` |
| 122 | Async Postgres? | `asyncpg` |
| 123 | asyncio vs C# async? | Single loop vs thread pool |
| 124 | Thread pool? | `ThreadPoolExecutor` |
| 125 | Process pool? | `ProcessPoolExecutor` |
| 126 | Process cost? | Startup + pickling |
| 127 | What can't be pickled? | Lambdas, local functions, open sockets |
| 128 | Windows multiprocessing needs? | `if __name__ == "__main__":` |
| 129 | Fork vs spawn? | Fork copies memory; spawn re-imports |
| 130 | Is `x += 1` atomic? | No — read-modify-write |
| 131 | Is `list.append` atomic? | Yes, by GIL accident. Don't rely on it |
| 132 | Safest thread sharing? | `queue.Queue` |
| 133 | `Lock` vs `RLock`? | RLock is re-entrant |
| 134 | Deadlock avoidance? | Consistent lock ordering, timeouts |
| 135 | Beyond one machine? | Celery, Dask, Ray |

### E. Generators, iterators, memory (136–160)

| # | Q | A |
|---|---|---|
| 136 | Iterator protocol? | `__iter__` and `__next__` |
| 137 | Iterable vs iterator? | The book vs the bookmark |
| 138 | Generator? | Function with `yield`. Lazy |
| 139 | Memory of a generator? | Constant |
| 140 | Generator downside? | One pass, no `len`, no indexing |
| 141 | `yield from`? | Delegate to another generator |
| 142 | Generator expression? | `(x for x in xs)` |
| 143 | Big file answer? | Generator, line by line |
| 144 | `islice`? | Take N from a lazy stream |
| 145 | `groupby` requirement? | Input must be sorted by the key |
| 146 | `accumulate`? | Running total |
| 147 | `batched`? | Fixed-size chunks, 3.12+ |
| 148 | Rolling window? | `deque(maxlen=n)` |
| 149 | Top N of a huge stream? | `heapq.nlargest` |
| 150 | Keep a list sorted? | `bisect.insort` |
| 151 | How is memory freed? | Refcount + cycle collector |
| 152 | Cycle collector generations? | Three |
| 153 | Refcount weakness? | Cycles |
| 154 | Leak sources? | Global caches, cycles, closures, C extensions |
| 155 | Find a leak? | `tracemalloc` snapshot diff |
| 156 | Is `__del__` reliable? | No. Use `with` |
| 157 | Weak reference use? | Caches that shouldn't keep objects alive |
| 158 | `sys.getsizeof` limit? | Shallow only |
| 159 | Save memory on many objects? | `__slots__` |
| 160 | Save memory on numbers? | `array.array` or NumPy |

### F. Types, errors, files, modules (161–185)

| # | Q | A |
|---|---|---|
| 161 | Are hints enforced? | No. Erased at runtime |
| 162 | Check them? | `mypy` or `pyright` in CI |
| 163 | `Optional[int]` = ? | `int \| None` |
| 164 | `Any` means? | Type checking off. Avoid |
| 165 | `Literal`? | Only these exact values |
| 166 | `TypedDict`? | A dict with known keys |
| 167 | `Protocol`? | Structural interface |
| 168 | Runtime validation? | Pydantic |
| 169 | `from __future__ import annotations`? | Lazy annotations. Fixes forward refs |
| 170 | Never catch what? | `BaseException` / bare `except:` |
| 171 | `else` on try? | Runs if nothing raised |
| 172 | `finally`? | Always runs |
| 173 | `raise ... from e`? | Chains, preserves the cause |
| 174 | EAFP? | Try it, handle failure. Python's default |
| 175 | Exception groups? | 3.11+, `except*` |
| 176 | Context manager? | `__enter__`/`__exit__`. `with` |
| 177 | `__exit__` returning True? | Swallows the exception. Usually wrong |
| 178 | Easy context manager? | `@contextlib.contextmanager` |
| 179 | `open` default encoding? | Platform-dependent — always specify |
| 180 | Path handling? | `pathlib`, `/` operator |
| 181 | `__name__ == "__main__"`? | Entry-point guard |
| 182 | Circular import fix? | Extract shared module; or import locally |
| 183 | `sys.modules`? | Import cache. Top level runs once |
| 184 | Virtualenv purpose? | Isolate dependencies per project |
| 185 | Modern packaging file? | `pyproject.toml` |

### G. Data, dates, ecosystem, security (186–200)

| # | Q | A |
|---|---|---|
| 186 | Why is NumPy fast? | Contiguous typed memory, C loops, releases GIL |
| 187 | Broadcasting? | Shapes stretched without copying |
| 188 | Never do in pandas? | `iterrows` / `apply(axis=1)` |
| 189 | Instead? | Vectorise the whole column |
| 190 | Shrink a DataFrame? | `category` dtype, downcast numerics |
| 191 | Point-in-time join? | `pd.merge_asof` |
| 192 | Time-series bars? | `df.resample("1min").ohlc()` |
| 193 | Faster than pandas? | Polars, DuckDB |
| 194 | Columnar file format? | Parquet |
| 195 | Correct "now"? | `datetime.now(timezone.utc)` |
| 196 | Why not `utcnow()`? | Returns naive. Deprecated |
| 197 | Timezones? | `zoneinfo`, stdlib |
| 198 | T+2 settlement? | Business-day calendar, not `timedelta` |
| 199 | Why is `pickle` dangerous? | Unpickling executes code |
| 200 | Secure random? | `secrets`, never `random` |

---

# PART 22 — THE TEN SENTENCES THAT MAKE YOU SOUND SENIOR

Drop these naturally. Each one signals experience, not revision.

1. *"**Waiting → asyncio or threads. Working → processes or NumPy.** That's the whole concurrency decision."*
2. *"Type hints are erased at runtime, so I validate at the boundary with Pydantic and let mypy handle the inside."*
3. *"I measure before I optimise — `cProfile` for time, `tracemalloc` for memory, `py-spy` for a live process I can't restart."*
4. *"Money is `Decimal` or integer minor units. Float is for statistics, never for cash."*
5. *"I use frozen dataclasses with slots inside the domain, and Pydantic at the edges. Different jobs."*
6. *"Generators keep memory constant regardless of input size — that's how I handle files that don't fit in RAM."*
7. *"A decorator is middleware for a single function. Logging, retry, caching, auth — without touching the body."*
8. *"3.13 shipped an optional free-threaded build. It's not the default yet, so my production answer is still processes — but that's genuinely changing."*
9. *"In a .NET shop I'd keep Python for analytics and quant, behind a versioned contract, so .NET stays the system of record."*
10. *"I mock at the boundary, not the domain logic — the HTTP client, the clock, the gateway."*

---

## ✅ Before you close this file

- [ ] Say the **Part 0** table out loud, all 15
- [ ] Say the **Part 13.2** decision table from memory
- [ ] Write **20.1 (rolling VWAP)** on paper without looking
- [ ] Run the **Part 21** rapid-fire, target 160/200
- [ ] Say all ten **Part 22** sentences

**Then go to `06a-fastapi.md`.**
