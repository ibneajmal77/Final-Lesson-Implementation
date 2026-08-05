# 14 - FULL INTERVIEW UNDERSTANDING GUIDE

> This file is the map of the whole pack.
>
> It does not replace the other lessons. It tells you how the lessons fit together, which files to
> study as one group, and what each group must make you able to explain in the interview.
>
> Rule: learn the simple flow first, then add the deeper detail from the source lessons.

---

# PART 0 - THE WHOLE INTERVIEW IN ONE MAP

The role is not one isolated skill. It is one connected system:

```text
Capital markets desktop system
    -> WPF trader/portfolio UI
    -> .NET backend services
    -> Python analytics / quant / data work
    -> SQL + document + columnar storage
    -> REST/auth/security
    -> real-time messages and concurrency
    -> Azure/DevOps for delivery
    -> audit, correctness, performance
```

The easiest way to understand the pack is to group the lessons like this:

| Group | What it teaches | Files |
|---|---|---|
| 1 | Interview control and positioning | `00`, `01`, `02`, `13`, `15`, `16` |
| 2 | Core .NET and runtime depth | `03`, `04`, `12` |
| 3 | WPF desktop and real-time UI | `05`, plus `04`, `12`, `10` |
| 4 | Python, data work, and Python web | `06`, `06a`, `06b`, `06c` |
| 5 | SQL, ORM, storage, and data correctness | `07`, `06c`, `03`, `11` |
| 6 | API, authentication, authorization, security | `09`, plus `06a`, `06b`, `10` |
| 7 | Architecture, patterns, distributed systems | `08`, plus `04`, `09`, `10`, `11` |
| 8 | Finance domain and capital markets | `11`, plus `05`, `07`, `08` |
| 9 | Frontend and JavaScript/TypeScript | `17`, plus `09` |
| 10 | Final cram and practice | `15`, `16` |

Do not study file by file as isolated notes. Study by group.

---

# PART 1 - THE BEST STUDY FLOW

## Flow A - If you have only one evening

1. `15` - learn the 12 simple answers.
2. `02` - learn your project story and honest gap answers.
3. `03` - C#/.NET Part 0.
4. `04` - concurrency Part 0.
5. `05` - WPF Part 0 and the real-time grid answer.
6. `07` - SQL Part 0.
7. `09` - API/auth Part 0.
8. `11` - finance Part 0.
9. `16` - rapid-fire out loud.

## Flow B - If you want real understanding

Use this order:

```text
1. Role and story
2. .NET core
3. Concurrency
4. WPF
5. SQL/data
6. API/auth
7. Architecture
8. Python/web frameworks
9. Finance
10. Practice
```

That order works because it follows the likely interview:

```text
Who are you?
    -> Are you technically real in .NET?
    -> Can you handle real-time/concurrency?
    -> Can you survive WPF?
    -> Can you query and model data?
    -> Can you design secure services?
    -> Can you talk architecture?
    -> Can you learn the finance domain?
```

---

# PART 2 - GROUP 1: INTERVIEW CONTROL AND POSITIONING

Files: `00`, `01`, `02`, `13`, `15`, `16`

## What this group is for

This group controls how the interviewer sees you.

You are not trying to look like a perfect match for every word in the job spec. You are trying to look
like a strong .NET engineer who:

- can own business-critical systems,
- can handle real-time data,
- can learn WPF and finance honestly,
- can talk clearly to a client,
- does not bluff.

## File roles

| File | Job |
|---|---|
| `00` | How to use the pack and where to spend time |
| `01` | What the role probably really means |
| `02` | Your pitch, your project story, and hard-question answers |
| `13` | Behavioural answers and questions to ask them |
| `15` | The final cram sheet |
| `16` | Rapid-fire, coding drills, and mock interview practice |

## The big story

Simple version:

> "I am a .NET-heavy engineer who modernizes business-critical systems. I have strong backend,
> distributed systems, SQL, Python, and Azure experience. WPF and finance are not my deepest areas,
> so I am honest about them, but I have prepared and I can connect them to systems I have already
> built."

## What not to do

Do not lead with AI.

For this role, AI is a bonus. The core story is:

```text
.NET -> real-time systems -> SQL/data -> Python -> architecture -> Azure -> AI as bonus
```

## The honest gap answer pattern

Use this shape:

```text
1. Be honest about the gap.
2. Connect to a similar thing you have done.
3. Show what you have already learned.
4. End with confidence and a question.
```

Example for WPF:

> "I have not been doing WPF day-to-day recently. My recent UI work has been web. But the ideas map:
> state, binding, events, change notification, and testable presentation logic. I have been rebuilding
> WPF hands-on, especially MVVM, Dispatcher, data binding, and real-time grid updates. The hard part
> is not drawing a screen; it is keeping a live data UI responsive."

---

# PART 3 - GROUP 2: CORE .NET AND RUNTIME DEPTH

Files: `03`, `04`, `12`

## What this group is for

This is the technical heart of the interview.

The interviewer needs to know:

- you understand C# deeply,
- you understand memory and GC,
- you understand async and threading,
- you can reason about performance,
- you can explain trade-offs without guessing.

## The concept stack

Study these in this order:

```text
1. Value vs reference
2. Stack vs heap
3. Boxing
4. GC
5. Strings and allocation
6. LINQ and collections
7. Async/await
8. Locks and Interlocked
9. Channels and backpressure
10. Profiling and measurement
```

## Full technical load in simple words

### Value vs reference

Value types copy the data. Reference types copy a pointer to the object.

Important trap:

> A value type does not automatically live on the stack.

Where it lives depends on where it is stored:

- local value: may be on the stack,
- field inside a class: lives inside that heap object,
- boxed value: lives in a heap object.

### Boxing

Boxing means:

```text
value type -> wrapped as object -> heap allocation
```

Why it matters:

- creates garbage,
- adds a copy,
- adds indirection,
- hurts hot paths like market tick processing.

Good answer:

> "Boxing is fine occasionally, but not in hot loops. For structs I use generics and `IEquatable<T>`
> to avoid unnecessary boxing."

### GC

The GC cleans managed memory.

Simple model:

```text
Gen 0 = new short-lived objects
Gen 1 = middle area
Gen 2 = long-lived objects
Large Object Heap = large arrays/objects, more expensive
```

Low-latency rule:

> Do not start by tuning the GC. Start by allocating less.

How to allocate less:

- avoid temporary objects in hot paths,
- avoid LINQ in very hot loops,
- use structs for small value-like data,
- use `Span<T>` to slice without copying,
- use `ArrayPool<T>` for reusable buffers.

### Async/await

Async is for waiting, not CPU work.

```text
I/O wait -> async/await
CPU work -> threads, Parallel, process, vectorized code
```

`await` pauses the method. It does not block the thread.

Classic WPF deadlock:

```text
UI thread calls .Result
async continuation needs UI thread
UI thread is blocked
deadlock
```

Fix:

- async all the way,
- avoid `.Result` and `.Wait()`,
- use `ConfigureAwait(false)` in library code where context is not needed.

### Locks

Use a private lock object.

Do not lock on:

- `this`,
- strings,
- `Type` objects.

Deadlock prevention:

> Take locks in the same order everywhere.

`volatile` vs `Interlocked`:

```text
volatile = visibility
Interlocked = atomic operation
```

So `volatile int x; x++;` is still not safe.

### Channels and backpressure

Producer/consumer today in .NET:

```text
System.Threading.Channels
```

Bounded channel means:

```text
queue has a max size -> memory cannot grow forever -> producers slow down or drop by policy
```

Price updates can often drop old values. Orders cannot be dropped.

### Performance

Performance method:

```text
measure -> find biggest cost -> fix one thing -> measure again
```

Common real bottlenecks:

- database calls,
- N+1 queries,
- too much data fetched,
- allocation and GC,
- lock contention,
- blocked thread-pool work,
- slow UI rendering.

Use percentiles:

```text
p50 = normal user
p99 = slow tail
p99.9 = worst tail
```

Average hides pain.

---

# PART 4 - GROUP 3: WPF DESKTOP AND REAL-TIME UI

Files: `05`, plus `04`, `12`, `10`

## What this group is for

WPF is your biggest visible gap. The goal is not to pretend you are a lifelong WPF specialist. The goal
is to show:

- you understand the model,
- you know the common traps,
- you can keep a live data UI responsive,
- you can connect WPF to your existing UI/backend experience.

## The concept stack

```text
1. WPF draws a UI tree
2. XAML creates objects
3. DataContext gives binding source
4. Binding connects View and ViewModel
5. Dependency properties are for controls
6. INotifyPropertyChanged is for ViewModels
7. ObservableCollection is for collection changes
8. Dispatcher owns UI thread access
9. Virtualization keeps big grids fast
10. Batch real-time updates
```

## Full technical load in simple words

### WPF mental model

WPF is a Windows UI framework.

You describe a tree:

```text
Window
  Grid
    TextBox
    DataGrid
    Button
```

WPF draws the tree.

XAML is just a clean way to create those objects.

### MVVM

MVVM separates responsibilities:

```text
View = XAML and visual layout
ViewModel = state and commands
Model = domain/data
```

The ViewModel should be a plain class. It should not directly create buttons, windows, or controls.

Why this matters:

- testable without UI,
- easier to reason about,
- clean separation.

### Binding

Binding connects UI to data.

Example:

```text
TextBox.Text -> ViewModel.Symbol
Button.Command -> ViewModel.SearchCommand
DataGrid.ItemsSource -> ViewModel.Positions
```

If the ViewModel changes, it raises `PropertyChanged`.

### Dependency property

Dependency properties are WPF control properties.

They support:

- binding,
- styles,
- animation,
- inherited values,
- default values,
- change notification.

Trap:

> A value set directly in code can beat a style trigger.

Fix:

- use binding,
- use styles,
- or call `ClearValue()`.

### ObservableCollection trap

`ObservableCollection<T>` tells the UI:

- item added,
- item removed,
- collection moved/reset.

It does not tell the UI:

- a property inside an item changed.

Each row item must implement `INotifyPropertyChanged`.

### Dispatcher

WPF controls belong to the UI thread.

Background work cannot directly update UI controls.

Correct model:

```text
background thread receives data
    -> batch update
    -> Dispatcher posts UI update
    -> UI thread updates bound values
```

### Real-time grid answer

For 10,000 ticks/sec into a grid:

```text
1. Do not update UI per tick.
2. Keep latest value per instrument.
3. Batch changes.
4. Flush on a timer, for example every 100-200 ms.
5. Raise PropertyChanged only if value actually changed.
6. Use DataGrid virtualization with recycling.
7. Use bounded channel so memory cannot grow forever.
8. Decide drop policy: prices can drop old; orders cannot drop.
```

This answer connects WPF, concurrency, and performance.

---

# PART 5 - GROUP 4: PYTHON, DATA WORK, AND PYTHON WEB

Files: `06`, `06a`, `06b`, `06c`

## What this group is for

Python is listed as advanced. They may not only ask "can you write Python?" They may ask:

- how Python memory works,
- what the GIL means,
- async vs threads vs processes,
- generators for large files,
- Pandas/NumPy performance,
- FastAPI/Django differences,
- ORM and database behavior.

## The concept stack

```text
1. Variables are names pointing at objects
2. Mutable vs immutable
3. is vs ==
4. Shallow vs deep copy
5. Refcount and cycle collector
6. Functions, closures, decorators
7. Classes, dataclasses, Pydantic
8. Generators and iterators
9. GIL
10. asyncio
11. NumPy/Pandas
12. FastAPI
13. Django
14. SQLAlchemy/ORM
```

## Full technical load in simple words

### Python variables

Python variables are names, not boxes.

```python
x = [1, 2]
y = x
y.append(3)
print(x)  # [1, 2, 3]
```

Both names point to the same list.

### Mutable default argument

Bad:

```python
def add(x, items=[]):
    items.append(x)
    return items
```

The list is created once and shared.

Good:

```python
def add(x, items=None):
    if items is None:
        items = []
    items.append(x)
    return items
```

### `is` vs `==`

```text
==  means same value
is  means exact same object
```

Use:

```python
if x is None:
    ...
```

### Memory cleanup

Python mostly frees objects when no names point to them.

But object cycles need a cycle collector.

Leaks usually come from:

- growing global caches,
- closures holding large objects,
- reference cycles,
- C extensions.

### GIL

The GIL means only one normal Python thread runs Python code at a time.

So:

```text
I/O wait -> threads or asyncio are fine
CPU work -> processes or NumPy
```

NumPy can be fast because the heavy work runs in C and can release the GIL.

### asyncio

`asyncio` is one event loop.

Good for many waiting tasks.

Bad trap:

```python
time.sleep(5)  # blocks the loop
```

Use:

```python
await asyncio.sleep(5)
```

or push blocking work out:

```python
await asyncio.to_thread(blocking_function)
```

### Generators

Generators return one item at a time.

Good for:

- huge files,
- streams,
- constant memory processing.

### Pandas

Pandas is fast when you work on whole columns.

Bad:

```python
for row in df.iterrows():
    ...
```

Better:

```python
df["value"] = df["price"] * df["quantity"]
```

### FastAPI

FastAPI is best for API services.

Understand:

- route functions,
- type hints,
- Pydantic validation,
- dependencies with `Depends`,
- async vs sync routes,
- response models,
- auth dependencies.

Main trap:

> Do not call blocking code inside `async def`.

### Django

Django is best for full web products.

It includes:

- ORM,
- admin,
- auth,
- migrations,
- forms,
- templates,
- security defaults.

Main trap:

> N+1 queries from lazy relations.

Fix:

- `select_related`,
- `prefetch_related`.

### ORM

ORM helps normal database work, but it can hide bad SQL.

Always know:

- lazy vs eager loading,
- session/unit of work,
- transactions,
- migrations,
- connection pooling,
- when to drop to raw SQL.

---

# PART 6 - GROUP 5: SQL, ORM, STORAGE, AND DATA CORRECTNESS

Files: `07`, `06c`, `03`, `11`

## What this group is for

This role is data-heavy. In finance, correct data is the product.

You must be able to explain:

- SQL joins,
- window functions,
- indexes,
- execution plans,
- transactions,
- isolation,
- deadlocks,
- ORM traps,
- Mongo/document modeling,
- columnar/time-series storage,
- money precision.

## The concept stack

```text
1. Correct data types
2. Joins
3. Window functions
4. Indexes
5. Execution plans
6. Transactions
7. Isolation
8. Deadlocks
9. ORM loading
10. Mongo/document modeling
11. Columnar/time-series
12. Audit and point-in-time correctness
```

## Full technical load in simple words

### Money type

Use:

```text
C#      decimal
Python  Decimal
SQL     DECIMAL
```

Avoid:

```text
float/double for cash
```

### Joins

Simple map:

```text
INNER JOIN = only matches
LEFT JOIN  = all left rows, matches if they exist
CROSS JOIN = every combination
SELF JOIN  = table joined to itself
```

Trap:

```sql
LEFT JOIN fills f ON f.order_id = o.id
WHERE f.venue = 'LSE'
```

This removes null rows and acts like an inner join.

Fix:

```sql
LEFT JOIN fills f
  ON f.order_id = o.id
 AND f.venue = 'LSE'
```

### Window functions

Window functions calculate across related rows without collapsing rows.

Use them for:

- latest row per group,
- running totals,
- previous value,
- rank,
- moving average.

Latest row:

```sql
ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY trade_ts DESC)
```

Then keep `rn = 1`.

### Indexes

An index is a lookup structure.

Important ideas:

- covering index: has every column the query needs,
- composite index: order of columns matters,
- index-friendly filter: do not wrap indexed column in a function.

Bad:

```sql
WHERE YEAR(trade_ts) = 2026
```

Good:

```sql
WHERE trade_ts >= '2026-01-01'
  AND trade_ts <  '2027-01-01'
```

### Execution plan

Slow query method:

```text
1. Get actual plan.
2. Look for scans.
3. Look for key lookups.
4. Compare estimated rows vs actual rows.
5. Check missing/wrong index.
6. Fix one thing.
7. Measure again.
```

### Transactions and isolation

Transaction = all or nothing.

Isolation controls what transactions can see while other transactions are running.

Higher isolation gives more correctness but can reduce concurrency.

Deadlock:

```text
Tx A holds row 1 and wants row 2
Tx B holds row 2 and wants row 1
```

Fix:

- access rows/tables in the same order,
- keep transactions short,
- retry safely.

### ORM traps

ORMs can cause hidden SQL.

Watch for:

- N+1,
- lazy loading surprise,
- loading too many columns,
- too many round trips,
- connection pool exhaustion.

### Mongo/document store

Use document storage when data is naturally document-shaped.

Do not use it as a replacement for every relational model.

Watch:

- indexes,
- document size,
- unbounded arrays,
- update patterns,
- consistency needs.

### Columnar/time-series

Row store is good for live transactions:

```text
orders, positions, users, accounts
```

Columnar store is good for analytics:

```text
tick history, reporting, large scans, aggregations
```

---

# PART 7 - GROUP 6: API, AUTHENTICATION, AUTHORIZATION, SECURITY

Files: `09`, plus `06a`, `06b`, `10`

## What this group is for

This group must make you safe on API and security questions.

You need to explain:

- REST basics,
- status codes,
- idempotency,
- OAuth,
- OIDC,
- JWT validation,
- desktop auth,
- Kerberos/Windows auth,
- mTLS,
- object-level authorization,
- secure errors,
- pagination and versioning.

## The concept stack

```text
1. Authentication vs authorization
2. 401 vs 403
3. REST verbs
4. Idempotency
5. OAuth roles and flows
6. OIDC identity
7. JWT validation
8. Token storage
9. Object-level authorization
10. ETag and version checks
11. Problem Details errors
12. Kerberos, mTLS, Windows auth
```

## Full technical load in simple words

### Authentication vs authorization

Authentication:

```text
Who are you?
```

Authorization:

```text
What are you allowed to do?
```

Status codes:

```text
401 = not logged in / unknown caller
403 = logged in but not allowed
```

### REST verbs

```text
GET    = read
POST   = create or process
PUT    = replace
PATCH  = partial change
DELETE = remove
```

Idempotent means:

> Doing it twice has the same final effect as doing it once.

GET, PUT, DELETE should be idempotent.

POST is not naturally idempotent. Use `Idempotency-Key` for create/process requests that may retry.

### OAuth vs OIDC

OAuth:

```text
permission for an app to call an API
```

OIDC:

```text
login identity: who the user is
```

Tokens:

```text
access token -> API
ID token     -> client app
```

Never use ID token to call an API.

### Desktop OAuth

Desktop apps cannot keep secrets safely.

Use:

```text
Authorization Code + PKCE
```

Store tokens in OS secure storage.

### JWT validation

Do not trust the token because it looks valid.

Check:

- signature,
- issuer,
- audience,
- expiry,
- algorithm.

JWT revocation:

> A normal JWT usually works until it expires.

Mitigation:

- short access token lifetime,
- refresh-token rotation,
- opaque tokens for high-risk cases.

### Object-level authorization

Big API risk:

```text
user changes /orders/123 to /orders/124
```

Every request must check:

```text
Can this user access this exact object?
```

### ETag version checks

Use when two users may update same resource.

Flow:

```text
GET returns ETag
client sends If-Match with update
server checks version
if changed -> 412
```

### Errors

Use a standard shape:

```text
type
title
status
detail
correlationId
```

Do not leak secrets or stack traces to clients.

### Bank/on-prem auth words

Know these:

- Kerberos / Windows authentication,
- mTLS,
- certificates,
- service accounts,
- least privilege,
- audit logs.

---

# PART 8 - GROUP 7: ARCHITECTURE, PATTERNS, DISTRIBUTED SYSTEMS

Files: `08`, plus `04`, `09`, `10`, `11`

## What this group is for

This group makes you sound like a senior engineer rather than someone memorizing definitions.

Rule:

> Do not define a pattern first. Say the problem it solved.

## The concept stack

```text
1. Strategy
2. Decorator
3. State
4. Command
5. Observer
6. Adapter
7. CQRS
8. Event sourcing
9. SAGA
10. Outbox
11. Idempotency
12. CAP/PACELC
13. Modular monolith vs microservices
14. Strangler Fig
15. Shadow mode
```

## Full technical load in simple words

### Strategy

Use when the algorithm changes.

Examples:

- pricing strategy,
- routing strategy,
- fee strategy.

### Decorator

Wrap behavior around a core service.

Examples:

- retry,
- logging,
- caching,
- timing,
- auth check.

### State

Use when behavior depends on current state.

Best finance example:

```text
New -> PartiallyFilled -> Filled
New -> Cancelled
New -> Rejected
```

The order should control valid transitions.

### Observer

Use when something needs to react to changes.

Examples:

- WPF `INotifyPropertyChanged`,
- events,
- pub/sub.

### CQRS

Separate:

```text
write model = commands, validation, business rules
read model  = queries, screens, reports
```

CQRS does not require event sourcing.

### Event sourcing

Store the events, not only current state.

Example:

```text
OrderCreated
OrderRouted
ExecutionReceived
OrderPartiallyFilled
OrderFilled
```

Benefits:

- audit,
- replay,
- explain why state exists.

Costs:

- projections,
- event versioning,
- snapshots,
- more complexity.

### SAGA

Use for a business process across services where one database transaction is not possible.

Instead of rollback, use compensating actions.

### Outbox

Problem:

```text
write database
publish message
```

One can succeed and the other fail.

Outbox fix:

```text
write business data + outbox message in same DB transaction
background relay publishes outbox message
```

### Idempotency

Messages can repeat.

So the handler must be safe to run twice.

Tools:

- idempotency key,
- dedupe table,
- upsert,
- natural idempotent operation.

### Modular monolith vs microservices

Default:

```text
modular monolith
```

Split service only for:

- independent scale,
- independent release,
- team ownership,
- hard boundary.

Microservices add:

- latency,
- network failure,
- distributed tracing,
- versioning,
- deployment complexity.

### Legacy modernization

Do not big-bang replace.

Use:

- Strangler Fig: replace piece by piece,
- Shadow mode: run old and new together and compare output.

---

# PART 9 - GROUP 8: FINANCE DOMAIN AND CAPITAL MARKETS

Files: `11`, plus `05`, `07`, `08`

## What this group is for

You are not expected to be a quant. You are expected to understand enough domain to build correct
systems and ask good questions.

## The concept stack

```text
1. Buy-side vs sell-side
2. Front/middle/back office
3. Instruments
4. PMS/OMS/EMS
5. Order lifecycle
6. FIX
7. Positions
8. P&L
9. Risk
10. Audit
11. Financial maths boundary
12. Regulation as engineering constraints
```

## Full technical load in simple words

### Buy-side vs sell-side

Buy-side:

```text
owns/invests money
```

Sell-side:

```text
brokers/banks help trade, make markets, execute
```

### Office map

```text
front office  = traders, PMs, analysts
middle office = risk, compliance, performance
back office   = settlement, accounting, reconciliation
```

### PMS / OMS / EMS

```text
PMS = what should I own?
OMS = manage the order and audit trail
EMS = execute the order well
```

### Order lifecycle

```text
idea
-> order
-> pre-trade compliance
-> route
-> executions/fills
-> allocation
-> settlement
-> reconciliation
```

Hard engineering points:

- partial fills,
- duplicate execution reports,
- out-of-order messages,
- cancel/replace race,
- audit trail.

### FIX

FIX is tag=value trading messages.

Examples:

```text
35=D  new order
35=8  execution report
11=   client order id
```

### P&L

Realised P&L:

```text
closed trades
```

Unrealised P&L:

```text
open positions valued with current market price
```

### Audit

Finance systems must answer:

```text
What was the number?
Why was it that number?
What data did we know at that time?
Who changed it?
When?
```

That is why event history and point-in-time data matter.

### Engineer vs quant

Say:

> "I am an engineer, not a quant. I expect the model from the quant/domain team. My job is to
> implement it correctly, precisely, fast, and testably."

---

# PART 10 - GROUP 9: FRONTEND, JAVASCRIPT, TYPESCRIPT, NODE

Files: `17`, plus `09`

## What this group is for

The role says JavaScript/frameworks at medium level. You need enough to explain clearly, not to sound
like a frontend specialist.

## The concept stack

```text
1. JavaScript one-thread model
2. Event loop
3. var/let/const
4. == vs ===
5. Promise
6. async/await
7. TypeScript erased types
8. Runtime validation
9. React state
10. useEffect cleanup
11. Node as server runtime
```

## Full technical load in simple words

### JavaScript runtime

JavaScript has one main thread.

Slow work is handed to the runtime. When it finishes, a callback runs later.

Event loop memory rule:

```text
sync code -> promises -> timers
```

### Promise

Promise is like a C# `Task`.

It means:

```text
value later or error later
```

### TypeScript

TypeScript checks types during development/build.

At runtime, types disappear.

So external API data still needs runtime validation.

### React

Simple model:

```text
UI = function(state)
```

Change state, React updates the screen.

Do not mutate state directly. Create new state values.

`useEffect` is for outside work:

- fetch,
- timer,
- subscription,
- manual DOM integration.

Cleanup in `useEffect` is like `Dispose()`.

### Node.js

Node is JavaScript on the server.

Good for:

- I/O-heavy APIs,
- real-time connections,
- lightweight services.

Be careful with:

- CPU-heavy work blocking the event loop,
- validation at API boundaries,
- async error handling.

---

# PART 11 - GROUP 10: FINAL CRAM AND PRACTICE

Files: `15`, `16`

## What this group is for

Understanding is not enough. You need recall under pressure.

Use:

- `15` for final summary,
- `16` for rapid-fire and coding drills.

## Practice loop

```text
1. Read a simple answer.
2. Close the file.
3. Say the answer out loud.
4. If stuck, reopen and repeat.
5. Time yourself.
```

## Coding exercise themes

Expect exercises around:

- grouping,
- rolling window,
- top N,
- LRU cache,
- producer/consumer,
- SQL latest row per group,
- position/P&L logic,
- concurrency bug.

When coding, always say:

```text
1. My assumptions.
2. The data structure.
3. The complexity.
4. Edge cases.
5. Tests I would add.
```

---

# PART 12 - NO LESSON MISSED CHECKLIST

Use this to make sure every file has a place.

| File | Do not miss |
|---|---|
| `00-START-HERE.md` | Study order, file map, time plan, rules |
| `01-role-decoded.md` | What BCM means, likely buy-side, WPF risk, consultancy/client model |
| `02-gap-analysis-positioning.md` | Your pitch, project walkthrough, hard gap answers |
| `03-csharp-dotnet.md` | C# memory, GC, LINQ, EF, DI, exceptions, SOLID |
| `04-multithreading-concurrency.md` | async, threads, locks, deadlocks, channels, real-time patterns |
| `05-wpf-desktop.md` | WPF, XAML, binding, dependency properties, MVVM, Dispatcher, grid performance |
| `06-python.md` | Python internals, GIL, asyncio, data types, decorators, classes, Pandas |
| `06a-fastapi.md` | FastAPI, Pydantic, dependency injection, async routes, auth, streaming |
| `06b-django.md` | Django, MVT, ORM, admin, DRF, middleware, security, performance |
| `06c-orm-databases.md` | ORM concepts, SQLAlchemy, unit of work, transactions, migrations, pooling |
| `07-sql-databases.md` | SQL joins, windows, indexes, plans, isolation, MongoDB, columnar |
| `08-design-patterns-architecture.md` | Patterns, CQRS, event sourcing, SAGA, outbox, CAP, system design |
| `09-rest-api-security.md` | REST, OAuth, OIDC, JWT, Kerberos, mTLS, BOLA/IDOR, Problem Details |
| `10-azure-devops.md` | Azure services, CI/CD, migrations, observability, desktop deployment |
| `11-finance-domain.md` | Buy-side, orders, OMS/EMS/PMS, FIX, positions, P&L, risk, audit |
| `12-performance-profiling.md` | Measurement, profiling tools, GC, WPF perf, Python perf, load testing |
| `13-behavioural-and-questions.md` | STAR stories, honest answers, questions to ask, follow-up email |
| `15-cheatsheet-cram.md` | Final interview summary and must-say answers |
| `16-mock-drills.md` | Rapid-fire, coding exercises, mock scripts |
| `17-javascript-typescript-react.md` | JS, TS, React, frontend calibration |

---

# PART 13 - HOW TO ANSWER ANY QUESTION

Use this universal shape:

```text
1. Simple answer first.
2. One technical detail.
3. One risk/trap.
4. One example from your work or this domain.
5. Stop.
```

Example:

Question:

> "How would you handle 10,000 price updates per second in WPF?"

Answer shape:

```text
Simple answer:
I would not update the UI per tick.

Technical detail:
I would keep latest value per symbol, batch changes, and flush on a Dispatcher timer.

Risk:
An unbounded queue or per-tick Dispatcher call will freeze the UI or grow memory.

Domain example:
For prices, old values can often be dropped because the latest price matters most. Orders are
different: never drop them.
```

---

# PART 14 - FINAL MEMORY MAP

Keep these connected pairs in your head:

```text
Money             -> decimal everywhere
Real-time UI      -> batch, conflate, Dispatcher, virtualize
Concurrency       -> waiting uses async, CPU uses threads/processes
Low latency       -> reduce allocation, measure p99
SQL speed         -> actual plan, index, query shape
ORM risk          -> hidden SQL and N+1
API safety        -> authn, authz, idempotency, object checks
Distributed       -> outbox, idempotency, retries, timeouts
Finance           -> correct numbers, audit, point-in-time truth
Architecture      -> modular first, split only for reason
Interview         -> honest gap, strong bridge, no bluff
```

If your mind goes blank, return to the four values of the role:

```text
correct numbers
responsive under load
auditable
do not break the desk
```

