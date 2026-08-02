# 17 — JAVASCRIPT, TYPESCRIPT & REACT, IN PLAIN ENGLISH

> **Read this box first.**
>
> The job asks for *"JavaScript with frameworks — **Medium** level"*. Medium. Not advanced.
> React is never even named. **This is a backend and desktop role.**
>
> You do not need to be a React expert. You need to explain the ideas simply and answer honestly
> if they probe. Budget **90 minutes**, not a day.
>
> Every idea below is explained by comparing it to **C# / .NET**, which you already know deeply.
> That's the fastest route into your memory.

**Format used throughout:**
**Q:** what they ask → **Say:** the words you speak → **Remember:** the hook.

---

# EASY MEMORY NOTES

Read this first. Start with the short phrase. Say the simple line. Add the last column only if they
ask for more.

| Remember | Say it simply | If they ask more |
|---|---|---|
| **One thread** | JavaScript has one main thread. | Slow I/O is handled by the runtime and callbacks run later. |
| **Promises before timers** | Promise callbacks run before timer callbacks. | This is the event loop order. |
| **`const` locks name** | `const` stops reassignment, not object changes. | The object can still be mutated. |
| **Use `===`** | Use strict equality to avoid weird conversions. | `x == null` is the only common exception. |
| **Promise = Task** | A Promise is like a C# `Task`. | It represents a value that will arrive later. |
| **Types disappear** | TypeScript types are not runtime checks. | Validate real API data at the boundary. |
| **UI from state** | React shows the UI for the current state. | Change state, React redraws what changed. |
| **Do not mutate state** | Make a new state value instead of changing the old one. | This helps React know it must re-render. |
| **Effect = outside work** | `useEffect` is for fetches, timers, and subscriptions. | Clean up subscriptions and timers. |
| **Keep frontend short** | This role only needs medium frontend depth. | Move the interview back to .NET, data, and real-time systems. |

---

# PART 0 — THE HONEST CALIBRATION LINE (use it if frontend comes up)

Your CV lists a lot of frontend. If your real depth is thinner, **say so early and simply.**
It costs you nothing and protects you completely.

> *"Quick note on the front end — I've worked across React, Angular and Vue on the platforms I've
> built, but I'd describe myself as a backend-heavy full stack engineer. I'm comfortable building and
> reviewing UI code and I understand the architecture side — component design, state management,
> build tooling. But my real depth is .NET, distributed systems and data. If you need someone whose
> primary craft is front end, I'm not that person. If you need someone who can work across the stack
> with backend depth, that's me."*

**Why this works:** interviewers don't punish honest calibration. They punish *discovering* a gap
themselves. And for this role backend depth is what they're buying anyway.

---

# PART 0.5 — THE 10 JAVASCRIPT ANSWERS THAT WIN

| # | The question | Simple answer |
|---|---|---|
| 1 | **Is JS single-threaded?** | "Yes. It has one main thread, but slow I/O runs outside it." |
| 2 | **The event loop** | "JavaScript runs normal code first, then promises, then timers." |
| 3 | **`var` / `let` / `const`** | "Use `const` first, `let` when reassignment is needed, and avoid `var`." |
| 4 | **Is `const` immutable?** | "No. The name cannot point somewhere else, but the object can still change." |
| 5 | **`==` vs `===`** | "Use `===` so JavaScript does not convert types behind your back." |
| 6 | **Array methods** | "`map`, `filter`, and `reduce` are like LINQ methods." |
| 7 | **A Promise is…** | "A Promise is like a C# `Task`: a value that arrives later." |
| 8 | **`this`** | "Normal functions get `this` from how they are called. Arrow functions keep the outside `this`." |
| 9 | **TypeScript at runtime** | "TypeScript types disappear at runtime, so validate real API data." |
| 10 | **React in one line** | "React shows the UI for the current state." |

---

# PART 1 — JAVASCRIPT: THE LANGUAGE

## 1.1 The mental model

JavaScript runs in a browser or in Node.js. It has **one thread**. But it never blocks and waits.
When something slow happens — a network call — JS hands it off to the runtime and carries on.
When the result arrives, the callback goes into a queue and runs when the thread is free.

**Say:** *"It's like an application with one UI thread and no thread pool. Everything is async on that
one thread. Block it and the whole page freezes — exactly like blocking the WPF dispatcher."*

**Remember:** **One thread. Never waits. Never block it.**

---

## 1.2 `var` vs `let` vs `const`

| | Scope | Reassign? | Before declaration |
|---|---|---|---|
| `var` | **whole function** | yes | exists, value is `undefined` |
| `let` | **the block `{ }`** | yes | error — "temporal dead zone" |
| `const` | **the block `{ }`** | **no** | same as `let` |

```js
const user = { name: "Awais" };
user.name = "Ali";        // fine — we changed the object
user = { name: "Ali" };   // ERROR — we tried to re-point the variable
```

**Say:** *"`const` by default, `let` when I need to reassign, never `var`. And `const` isn't
immutability — it fixes the variable, not the object. It's `readonly` on a reference field in C#."*

**Remember:** **`const` locks the label, not the thing.**

---

## 1.3 `==` vs `===`

`===` compares **value and type**, no surprises.
`==` converts types first, and the rules are strange: `0 == "0"` is true, `"" == 0` is true,
`null == undefined` is true.

**Say:** *"Always `===`. The only exception I use is `x == null`, which checks for `null` and
`undefined` in one go."*

---

## 1.4 `null` vs `undefined`

- `undefined` = "nobody set this yet" — the default.
- `null` = "someone deliberately set this to nothing".

**Say:** *"C# has one `null`. JavaScript splits 'never assigned' from 'assigned nothing'."*

---

## 1.5 Truthy, falsy, and the three operators that save you

Falsy: `false`, `0`, `""`, `null`, `undefined`, `NaN`. Everything else is truthy —
**including `[]` and `{}`**, which surprises people.

```js
const name = input ?? "default";    // ?? only falls back on null/undefined   ✅
const name = input || "default";    // || ALSO falls back on 0 and ""         ⚠️ common bug
const city = user?.address?.city;   // ?. no crash if address is missing
count ??= 0;                        // assign only if null/undefined
```

**Say:** *"`??` and `?.` are literally the same operators as C#. `||` is the trap — it treats `0` and
empty string as missing, which is a real bug when zero is a valid value."*

**Remember:** **`??` for missing. `||` for falsy. They are not the same.**

---

## 1.6 The event loop (the classic "how does it work" question)

**Say this, it's simple and correct:**

> *"JavaScript has one thread. Slow things like network calls are handed to the runtime. When they
> finish, their callbacks go into a queue. The event loop takes the next callback whenever the thread
> is free. So JS is single-threaded but non-blocking. If I run a long loop nothing else happens —
> the page freezes. Same problem as blocking the WPF dispatcher."*

If they push further: **microtasks (promises) run before macrotasks (`setTimeout`)**, and *all*
microtasks drain before the next macrotask.

```js
console.log("1");
setTimeout(() => console.log("2"), 0);            // macrotask — last
Promise.resolve().then(() => console.log("3"));   // microtask — before the timer
console.log("4");
// Output: 1, 4, 3, 2
```

**Remember: sync → promises → timers.**

**Q: `setTimeout(fn, 0)` — does it run immediately?**
**Say:** *"No. It runs after the current synchronous code and after all pending promises. The zero is
a minimum delay, not a guarantee."*

---

## 1.7 Promises and async/await

A Promise is a placeholder for a value that isn't ready yet. **It's a `Task<T>`.**
States: **pending** → **fulfilled** or **rejected**.

```js
async function loadUser(id) {
  try {
    const res = await fetch(`/api/users/${id}`);
    if (!res.ok) throw new Error(res.status);     // fetch does NOT throw on 404/500!
    return await res.json();
  } catch (err) {
    console.error(err);
    throw err;
  }
}

await Promise.all([a, b, c]);        // C#: Task.WhenAll — all must succeed, fails fast
await Promise.allSettled([a, b]);    // never rejects; reports each outcome
await Promise.race([a, timeout]);    // C#: Task.WhenAny — first to settle wins
await Promise.any([a, b]);           // first to SUCCEED wins
```

**Q: The single most-missed gotcha?**
**Say:** *"`fetch` does not throw on a 404 or a 500. It only rejects on a network failure. You have to
check `res.ok` yourself. That surprises everyone coming from `HttpClient`, which has
`EnsureSuccessStatusCode`."*

**Q: Sequential vs parallel?**
```js
const a = await fetchA();  const b = await fetchB();     // sequential — 2 seconds
const [a, b] = await Promise.all([fetchA(), fetchB()]);  // parallel — 1 second
```
**Remember:** **Two awaits in a row is sequential. `Promise.all` is parallel.**

**Q: Unhandled rejection?**
**Say:** *"A rejected promise nobody catches. In Node it crashes the process by default in modern
versions. Always `.catch` or wrap in try/catch — same discipline as an unobserved `Task` exception."*

---

## 1.8 `this` — made simple

**Say:** *"In a normal `function`, `this` depends on **how it was called**. In an **arrow function**,
`this` is whatever it was in the surrounding code — arrows don't have their own `this`."*

```js
const obj = {
  name: "book",
  normal() { console.log(this.name); },          // "book" — called as obj.normal()
  arrow: () => console.log(this.name),           // undefined — took `this` from outside
};

setTimeout(obj.normal, 0);          // undefined — lost its owner
setTimeout(() => obj.normal(), 0);  // "book" — arrow keeps the call intact
```

**The practical answer at medium level:** *"Use arrow functions in callbacks and you almost never
have a `this` problem."* Don't go deeper unless asked.

## 1.9 `call`, `apply`, `bind` (they may ask — it was missing before)

```js
greet.call(obj, "hi", "there");   // run now, `this` = obj, args listed
greet.apply(obj, ["hi", "there"]); // run now, `this` = obj, args as an Array
const bound = greet.bind(obj);     // returns a NEW function permanently bound to obj
```

**Remember:** **Call = Comma. Apply = Array. Bind = Bound for later.**

---

## 1.10 Closures

A function that **remembers the variables around it**, even after the outer function has finished.

```js
function makeCounter() {
  let count = 0;                // stays alive because the inner function uses it
  return () => ++count;
}
const next = makeCounter();
next(); // 1
next(); // 2
```

**Say:** *"Exactly a C# lambda capturing a local variable. Same concept, and the same memory-leak
risk if the closure outlives what it captured."*

---

## 1.11 Hoisting

**Say:** *"Declarations are processed before the code runs. A `var` exists from the top of its
function with the value `undefined`. `let` and `const` exist too but you can't touch them until the
declaration line — that gap is the temporal dead zone, and touching it throws. Function declarations
are fully hoisted, so you can call them before they appear."*

---

## 1.12 Prototypes and classes (was missing — a real interview topic)

**Say:** *"JavaScript doesn't have classes underneath. Every object has a hidden link to another
object — its prototype. When you ask for a property that isn't there, JS walks up that chain until it
finds it or reaches null. That's prototypal inheritance. The `class` keyword added in ES6 is
**syntax sugar** over exactly this — it isn't a new inheritance model."*

```js
class Instrument {
  #isin;                                   // # = genuinely private field
  constructor(symbol) { this.symbol = symbol; }
  describe() { return this.symbol; }       // lives on the prototype, shared by all instances
  static create(s) { return new Instrument(s); }
  get display() { return this.symbol.toUpperCase(); }
}

class Equity extends Instrument {
  constructor(symbol, sector) {
    super(symbol);                         // must come before using `this`
    this.sector = sector;
  }
}
```

**Remember:** **Prototype chain = lookup by walking up. `class` is sugar over it.**

---

## 1.13 The array methods you must recognise

```js
arr.map(x => x * 2)                  // transform     → C# .Select()
arr.filter(x => x > 10)              // keep some     → C# .Where()
arr.reduce((sum, x) => sum + x, 0)   // fold          → C# .Aggregate()
arr.find(x => x.id === 5)            // first match   → C# .FirstOrDefault()
arr.findIndex(...)                   //               → C# .FindIndex()
arr.some(...) / arr.every(...)       //               → C# .Any() / .All()
arr.includes(x)                      //               → C# .Contains()
arr.flat() / arr.flatMap(...)        //               → C# .SelectMany()
arr.sort((a, b) => a - b)            // ⚠️ IN PLACE, and sorts as STRINGS by default
arr.slice(1, 3)                      // copy a section — does NOT change the original
arr.splice(1, 2)                     // ⚠️ REMOVES items — CHANGES the original
```

**Remember:** **JS array methods are LINQ with different names.** And **`slice` copies, `splice`
cuts.**

**Q: The sort trap?**
**Say:** *"`[10, 9, 1].sort()` gives `[1, 10, 9]` because it converts to strings. Numbers always need
a comparator: `.sort((a, b) => a - b)`. And it sorts in place, which surprises people expecting LINQ's
immutability."*

---

## 1.14 Spread, destructuring, rest

```js
const merged = { ...defaults, ...overrides };   // copy and override — SHALLOW
const copy = [...arr];                          // shallow copy of an array
const [first, second, ...rest] = myArray;       // destructure with rest
const { name, age = 18, address: { city } = {} } = user;  // with default and nesting
function f(...args) {}                          // rest parameter — C#'s params
```

**Say:** *"Spread is a shallow copy. Nested objects are still shared — the same as `MemberwiseClone`
in C#. If I need a real deep copy, `structuredClone(obj)` is now built in."*

---

## 1.15 Objects, Map and Set (was missing)

```js
Object.keys(o) / Object.values(o) / Object.entries(o)
Object.freeze(o)             // shallow — top-level properties become read-only

const m = new Map();         // ANY type as a key, keeps insertion order, has .size
m.set(objKey, value); m.get(objKey); m.has(k); m.delete(k);

const s = new Set([1, 2, 2]);   // unique values
[...new Set(arr)]               // the idiomatic way to dedupe an array
```

**Q: Object vs Map?**
**Say:** *"An object only takes string or symbol keys, and it inherits from `Object.prototype` so
there are inherited keys to worry about. A `Map` takes any key including an object, preserves
insertion order, and has a real `.size`. For a genuine dictionary I use `Map`; for a record with known
fields I use an object. `Map` is `Dictionary<K,V>`, `Set` is `HashSet<T>`."*

---

## 1.16 Numbers — and the finance-relevant trap

```js
0.1 + 0.2                   // 0.30000000000000004
0.1 + 0.2 === 0.3           // false
Number.MAX_SAFE_INTEGER     // 9007199254740991 — beyond this, integers lose precision
10n ** 20n                  // BigInt for exact large integers
```

**Say (this lands well in a capital-markets interview):**
*"JavaScript has one number type — a 64-bit float. There is no decimal. So money in the browser is
handled either as integer minor units, or as a string from the API, or with a library like
decimal.js. Never do currency arithmetic in raw JS floats. It's the same reason I use `decimal` in C#
and `Decimal` in Python."*

**Also:** `NaN !== NaN` — use `Number.isNaN(x)`. And `typeof NaN` is `"number"`.

---

## 1.17 Modules — ESM vs CommonJS (was missing)

```js
// ESM — the modern standard, works in browsers and Node
export function calc() {}
export default Thing;
import { calc } from "./calc.js";

// CommonJS — older Node
module.exports = { calc };
const { calc } = require("./calc");
```

**Say:** *"ESM is static — imports are resolved before the code runs, which is what makes tree-shaking
possible. CommonJS is dynamic — `require` is a function call at runtime. ESM is the standard now;
CommonJS is what you meet in older Node code. Mixing them is the source of most Node build pain."*

---

## 1.18 The DOM and events (was missing)

```js
document.querySelector(".row");
el.addEventListener("click", handler);
el.removeEventListener("click", handler);   // must be the SAME function reference
```

**Q: Event bubbling and delegation?**
**Say:** *"An event fires on the element, then bubbles up through its ancestors. There's also a
capture phase going down first, but bubbling is what you use. **Event delegation** means putting one
listener on the parent instead of one on every child — you check `event.target` to see which child was
clicked. For a table with 5,000 rows that's one listener instead of five thousand. `e.stopPropagation()`
halts the bubble, `e.preventDefault()` cancels the default browser behaviour."*

**Remember:** **One listener on the parent beats a thousand on the children.**

---

## 1.19 Debounce and throttle

**Say:** *"Debounce waits until the user **stops** — good for a search box. Throttle runs **at most
once per interval** — good for scroll or a price feed. In WPF I'd solve the same problem by batching
onto a `DispatcherTimer`."*

```js
const debounce = (fn, ms) => {
  let t;
  return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
};
```

---

## 1.20 Web Workers and real-time (relevant to this role)

**Say:** *"If I genuinely need to compute something heavy in the browser without freezing the page, I
move it to a **Web Worker** — a separate thread that talks to the main thread by message passing, with
no shared memory. It's the browser's answer to the same problem the GIL creates in Python: one thread
can't do everything."*

**For live data:** *"For streaming prices to a browser I'd use **WebSockets** — full duplex, low
overhead — or **SignalR** if the backend is .NET, since it handles reconnection and transport
fallback for me. **Server-Sent Events** if the flow is one-way only. And on the client I'd conflate
and batch updates exactly like I would in WPF: don't re-render per tick, coalesce to the latest per
instrument and flush on an interval."*

**That answer connects the frontend to the real job. Use it.**

---

## 1.21 Storage, and CORS (both were missing)

| | Lives for | Size | Sent to server? |
|---|---|---|---|
| `localStorage` | Forever, until cleared | ~5 MB | No |
| `sessionStorage` | The tab | ~5 MB | No |
| Cookie | Its expiry | ~4 KB | **Yes, every request** |

**Say:** *"Tokens go in an `HttpOnly`, `Secure`, `SameSite` cookie, not `localStorage` — anything in
`localStorage` is readable by any injected script, so one XSS is a total compromise."*

**Q: What is CORS?**
**Say:** *"The browser blocks a page on one origin from reading a response from a different origin
unless the server opts in with `Access-Control-Allow-Origin` headers. For anything non-simple the
browser first sends an `OPTIONS` preflight. Important detail: **CORS is a browser rule, not server
security** — it protects users, it doesn't protect the API. The API still needs its own
authentication and authorisation."*

**Remember:** **CORS protects the user's browser, not your server.**

---

## 1.22 Memory leaks in JS

**Say:** *"The usual causes are listeners that are never removed, timers that are never cleared,
closures holding a big object, and detached DOM nodes still referenced by JS. `WeakMap` and
`WeakRef` exist for caches that shouldn't keep things alive. It's the same class of problem as event
handler leaks in WPF."*

---

# PART 2 — TYPESCRIPT

## 2.1 What it is, in one sentence

**Say:** *"TypeScript is JavaScript plus a type system that runs at compile time. It compiles to plain
JavaScript and **the types disappear at runtime** — they exist to catch mistakes in the editor and
the build, not to enforce anything when the code runs."*

**That last part is the key insight and a common question.** If JSON arrives from an API with the
wrong shape, TypeScript will not save you. That's why people add runtime validation with **Zod** at
the boundaries.

**Say the cross-language link — it's a strong moment:**
*"It's the identical model to Python's type hints. Erased at runtime, checked by a separate tool,
so you validate real data at the boundary — Zod in TypeScript, Pydantic in Python."*

---

## 2.2 The basic types

```ts
let name: string = "Awais";
let age: number = 34;                  // one number type — no int/decimal/float
let ok: boolean = true;
let ids: number[] = [1, 2, 3];
let pair: [string, number] = ["a", 1];  // tuple — fixed length, fixed types
let anything: any;                      // ⚠️ turns checking OFF
let safe: unknown;                      // ✅ must be narrowed before use
function fail(): never { throw new Error(); }   // never returns
```

**Q: `any` vs `unknown`?** *(a favourite)*
**Say:** *"`any` disables type checking entirely — it's contagious and dangerous. `unknown` says
'I don't know yet, so prove it before you use it'. Always prefer `unknown` at a boundary."*

**Remember:** **`any` = "I give up". `unknown` = "prove it first".**

---

## 2.3 `interface` vs `type`

- `interface` can be **re-opened** and added to (declaration merging). `type` cannot.
- `type` can do things `interface` can't: unions, intersections, mapped and conditional types.

**Say:** *"I use `interface` for object shapes others might extend, and `type` for unions and anything
computed. In practice either works for most cases — the team should just be consistent."*
That's the honest senior answer. Interviewers don't want dogma here.

---

## 2.4 Union types and narrowing — the most useful TS idea

```ts
type Status = "new" | "filled" | "cancelled";     // only these three strings allowed

function describe(x: string | number) {
  if (typeof x === "string") return x.toUpperCase();  // TS knows it's a string here
  return x.toFixed(2);                                // and a number here
}
```

**Say:** *"This is narrowing — TypeScript follows my `if` checks and works out the type in each
branch. I can narrow with `typeof`, `instanceof`, `in`, a literal check, or a custom type guard
written `function isX(v): v is X`. It's the same idea as pattern matching in C#."*

---

## 2.5 Discriminated unions — the one advanced pattern worth knowing

```ts
type Result =
  | { kind: "ok"; value: number }
  | { kind: "error"; message: string };

function handle(r: Result) {
  switch (r.kind) {                   // the 'kind' field tells TS which shape it is
    case "ok":    return r.value;     // TS knows .value exists
    case "error": return r.message;   // TS knows .message exists
  }
}
```

**Say:** *"A shared literal field acts as a tag, so the compiler knows exactly which shape you have in
each branch — and it will tell you if you forget a case. It's the type-safe way to model 'one of
several possibilities': order states, API results, connection states. If I remember one advanced
TypeScript pattern, it's this one."*

**Great answer to:** *"How would you model an order's state in TypeScript?"*

---

## 2.6 Generics

```ts
function first<T>(items: T[]): T | undefined { return items[0]; }

function byId<T extends { id: number }>(items: T[], id: number) {   // constraint
  return items.find(i => i.id === id);
}
```

**Say:** *"Identical concept to C#, almost identical syntax. `where T : ...` becomes `T extends ...`."*

---

## 2.7 Utility types

```ts
interface Order { id: number; symbol: string; qty: number; price: number; }

Partial<Order>              // everything optional      — patch/update payloads
Required<Order>             // everything required
Readonly<Order>             // everything readonly
Pick<Order, "id" | "qty">   // just those fields
Omit<Order, "price">        // everything except price
Record<string, number>      // a dictionary             — C# Dictionary<string,int>
ReturnType<typeof fn>       // the return type of fn
Awaited<T>                  // unwraps a Promise
```

**Remember:** **`Partial`, `Pick`, `Omit`, `Record` are 90% of what you'll ever use.**

## 2.8 `keyof`, `typeof` and mapped types (one level deeper, if pressed)

```ts
type OrderKey = keyof Order;                  // "id" | "symbol" | "qty" | "price"
const defaults = { a: 1, b: 2 };
type Defaults = typeof defaults;              // lift a VALUE into a TYPE
type Nullable<T> = { [K in keyof T]: T[K] | null };   // a mapped type
```

**Say:** *"`keyof` gives you the union of a type's keys, `typeof` lifts a value into the type world,
and a mapped type transforms every property. That's how `Partial` and `Readonly` are implemented —
they're not magic, they're mapped types in the standard library."*

## 2.9 Everything else worth one line

- **`strict: true`** in `tsconfig.json` — turns on all the good checks including `strictNullChecks`,
  which makes `null` and `undefined` explicit, like C#'s nullable reference types. **Always on.**
- `email?: string` means `string | undefined`.
- `x as Order` is a **type assertion** — you're telling the compiler to trust you. No runtime check.
- `x!` is the non-null assertion — same "trust me", same risk. Prefer a real check.
- **`enum`** — TS has it, but it generates runtime code. Most teams now use a union of string literals.
  Saying that shows currency.
- `satisfies` (4.9+) — check a value matches a type *without* widening it.
- `.d.ts` files — types for JS libraries that don't ship their own.
- **Zod** — runtime validation that also produces the TS type. The standard answer to
  *"types disappear at runtime, so how do you trust API data?"*

---

# PART 3 — REACT

## 3.1 The mental model, in plain words

**Say:** *"React builds UI out of components. A component is a function that takes data — props —
and returns what should appear on screen. When the data changes, React re-runs the function and
updates only the parts of the real page that actually differ."*

**The one sentence:** **UI = f(state).** You don't manipulate the screen. You describe what it should
look like, and React works out the change.

**Your best bridge — say this, it strengthens your WPF story too:**

| React | WPF |
|---|---|
| Component | UserControl / View |
| Props | Values passed in |
| State (`useState`) | View-model property + `INotifyPropertyChanged` |
| Re-render on state change | Binding updates the UI on `PropertyChanged` |
| Virtual DOM diffing | WPF's own dirty-region rendering |
| `useEffect` cleanup | `Dispose()` |
| Context | A DI-injected singleton |

---

## 3.2 Components and props

```jsx
function PriceTag({ symbol, price }) {          // props arrive as one object
  return <div>{symbol}: {price.toFixed(2)}</div>;
}

<PriceTag symbol="AAPL" price={182.35} />
```

- **JSX** is HTML-looking syntax that compiles to function calls. It's not a template language.
- **Props are read-only.** A component never modifies its own props. Data flows **down**.
- To send data **up**, the parent passes a function down and the child calls it.

**Remember:** **Props down, events up.**

---

## 3.3 The hooks that matter (there are only about six)

### `useState` — local state
```jsx
const [count, setCount] = useState(0);
setCount(count + 1);           // fine for simple cases
setCount(prev => prev + 1);    // ✅ safer when the new value depends on the old
```

**Q: Why isn't `count` updated right after `setCount`?** *(very common)*
**Say:** *"State updates are batched and asynchronous. Reading the variable immediately after gives me
the old value, because the component hasn't re-run yet. That's why the updater form `setX(prev => ...)`
exists — it's the safe way when the new value depends on the previous one."*

### `useEffect` — run code after render
```jsx
useEffect(() => {
  const timer = setInterval(tick, 1000);
  return () => clearInterval(timer);   // cleanup — on unmount, or before the next run
}, []);                                 // dependency array
```

The dependency array decides when it runs:
- `[]` → once after the first render (like a constructor / `OnLoaded`)
- `[userId]` → whenever `userId` changes
- *omitted* → after **every** render (usually a bug)

**Say about the cleanup:** *"Returning a function is how you unsubscribe. Without it you leak timers
and subscriptions. **It's `Dispose()`.**"*

**The modern point, and it marks you as current rather than someone who learned React in 2019:**
*"The React team's guidance now is that you need `useEffect` less than you think. It's for
synchronising with something outside React — a subscription, a timer, a WebSocket. Data fetching
belongs in a library like TanStack Query, and anything derivable from existing state should just be
calculated during render, not stored in state."*

### `useRef` — a box that survives re-renders without causing one
```jsx
const inputRef = useRef(null);       // grab a DOM element
const renderCount = useRef(0);       // or hold a mutable value
```
**Remember:** **State re-renders. Ref doesn't.**

### `useMemo` / `useCallback` — caching
- `useMemo` caches a **computed value**. `useCallback` caches a **function**.
- **Honest senior answer:** *"I don't reach for them by default. They add complexity and have their
  own cost. I use them when profiling shows a real problem, or when a function is a dependency of an
  effect. And React 19's compiler increasingly handles this automatically."*

### `useContext` — avoid passing props through many layers
```jsx
const ThemeContext = createContext("light");
const theme = useContext(ThemeContext);
```
**Say:** *"Context is for low-frequency values — theme, current user, locale. Every consumer re-renders
when it changes, so it's a poor fit for fast-moving data like prices. It's like a DI-injected
singleton."*

### `useReducer` — when state transitions get complicated
```jsx
const [state, dispatch] = useReducer(reducer, initialState);
dispatch({ type: "fill", qty: 100 });
```
**Say:** *"When the next state depends on the current state in several ways, a reducer keeps all the
transitions in one place. It's a state machine — which is exactly how you'd model an order
lifecycle."*

### The Rules of Hooks (they will check this)
1. Only call hooks at the **top level** — never inside `if`, a loop, or a nested function.
2. Only call them from React components or custom hooks.

**Q: Why?**
**Say:** *"React tracks hooks by **call order**, not by name. Skip one behind an `if` and the order
shifts, so state gets attached to the wrong hook."* **That "why" is what separates a good answer from
a memorised one.**

---

## 3.4 Keys in lists — a guaranteed question

```jsx
{orders.map(o => <Row key={o.id} order={o} />)}    // ✅ stable, unique
{orders.map((o, i) => <Row key={i} />)}            // ⚠️ index — breaks on reorder/insert
```

**Say:** *"Keys let React match items between renders. With index keys, inserting at the top makes
React think every row changed — you get the wrong state in the wrong row and unnecessary re-renders.
Use a stable unique ID. Index is only safe if the list never reorders."*

---

## 3.5 Re-rendering, explained simply

A component re-renders when its **state** changes, its **props** change, its **parent** re-renders, or
a **context** it uses changes.

**Say:** *"Re-rendering isn't the same as updating the page. React runs the function, compares the new
output with the old — that's reconciliation, the virtual DOM diff — and only touches the real DOM
where something actually differs."*

To reduce unnecessary re-renders: `React.memo` on the component, stable props via `useCallback`/
`useMemo`, keep state as low as possible, and split components so a fast-changing piece of state
doesn't re-render the whole tree.

---

## 3.6 Controlled vs uncontrolled inputs

- **Controlled:** React state is the source of truth (`value={x} onChange={...}`). Preferred.
- **Uncontrolled:** the DOM holds the value; you read it with a ref.

**Say:** *"Controlled is two-way binding. Uncontrolled is reading `TextBox.Text` directly."*

---

## 3.7 State management — the architecture answer (your comfort zone)

**Say:** *"I'd start with local component state, lift it up when it's shared, and use context for
low-frequency global values like the current user or theme. I only add a state library when there's
genuine shared client state — Redux Toolkit or Zustand. The big shift is that most of what people used
to put in Redux was actually **server** state, and that belongs in a data-fetching library like
TanStack Query or RTK Query, which handles caching, refetching and staleness for you."*

**That's a genuinely senior answer, and it's architectural rather than syntactic — which plays to your
strength.**

---

## 3.8 Everything else, one line each

- **Error boundaries** — catch render errors in a subtree so the whole app doesn't die. Class
  components only, or a library. *"A try/catch around a region of UI."*
- **StrictMode** in development deliberately runs effects twice, to expose missing cleanup.
- **Fragments** `<>...</>` — group children without adding a DOM node.
- **Portals** — render into a different part of the DOM. Modals and tooltips.
- **`lazy` + `Suspense`** — code-split a component and show a fallback while it loads.
- **Server Components** — render on the server, ship no JS for that component. *"Smaller bundles,
  server-side data fetching, client components only where you need interactivity."*
- **Custom hooks** — any function starting with `use` that calls other hooks. How you share logic.
  *"Extracting a shared service."*
- **Testing** — React Testing Library: test what the user sees and does, not internal state.
- **React 19** — the compiler auto-memoises, plus `use()` and Actions for forms.

---

# PART 4 — ANGULAR (30 seconds, only if they ask)

Angular is a **full framework**, not a library. Routing, HTTP, forms and DI are all built in.

**Say:** *"Angular is the most C#-like frontend framework — constructor dependency injection exactly
like ASP.NET Core, TypeScript-first, decorators like attributes, and a module/component/service
structure like a layered .NET app. RxJS observables are its async streams, the same shape as Rx.NET,
and Signals since v16 are the modern reactive primitive replacing a lot of that."*

**React vs Angular in one sentence:** *"React is a library — you assemble your own stack, more
flexible. Angular is an opinionated framework with DI, routing and forms included, which suits large
enterprise teams that want consistency. I've worked with both, and Angular's structure feels natural
coming from .NET."*

---

# PART 5 — RAPID-FIRE: 110 QUESTIONS

Cover the right column. Say the answer out loud.

### JavaScript — language (1–30)

| # | Q | A |
|---|---|---|
| 1 | `var` / `let` / `const` | Function-scoped / block-scoped / block-scoped and not reassignable |
| 2 | Is `const` immutable? | No — the variable can't be re-pointed; the object can still change |
| 3 | Temporal dead zone | The gap before a `let`/`const` declaration where touching it throws |
| 4 | Hoisting | Declarations processed first; `var` is `undefined`, `let`/`const` unusable |
| 5 | `==` vs `===` | Type coercion vs strict. Always `===` |
| 6 | `null` vs `undefined` | Deliberately empty vs never set |
| 7 | Falsy values | `false`, `0`, `""`, `null`, `undefined`, `NaN` |
| 8 | Are `[]` and `{}` truthy? | Yes — a classic surprise |
| 9 | `??` vs `\|\|` | `??` only on null/undefined; `\|\|` also on `0` and `""` |
| 10 | `?.` | Optional chaining — no crash if the middle is missing |
| 11 | `typeof null` | `"object"` — a famous historical bug |
| 12 | `NaN === NaN` | `false`. Use `Number.isNaN(x)` |
| 13 | `0.1 + 0.2` | `0.30000000000000004` — one float number type, no decimal |
| 14 | Money in JS | Integer minor units, or a string from the API, or decimal.js. Never raw floats |
| 15 | `BigInt` | Exact arbitrarily large integers: `10n` |
| 16 | Prototype | Every object links to another; missing properties are looked up the chain |
| 17 | Is `class` a real class? | No — syntax sugar over prototypes |
| 18 | `#field` | A genuinely private class field |
| 19 | `this` in a normal function | Depends on how it was called |
| 20 | `this` in an arrow function | Taken from the surrounding scope; arrows have none of their own |
| 21 | `call` / `apply` / `bind` | Run with args listed / args as an array / return a bound copy |
| 22 | Closure | A function that remembers the variables around it |
| 23 | IIFE | A function defined and called immediately — old-style module scoping |
| 24 | Spread `{...x}` | Shallow copy and merge |
| 25 | Deep clone | `structuredClone(obj)` |
| 26 | Destructuring | `const { a, b = 1 } = obj` — pull fields out with defaults |
| 27 | Rest parameter | `function f(...args)` — C#'s `params` |
| 28 | Template literal | `` `Hello ${name}` `` — C#'s `$""` |
| 29 | `Object.freeze` | Shallow — nested objects are still mutable |
| 30 | Strict mode | `"use strict"` — stricter rules; ESM is always strict |

### JavaScript — collections and async (31–58)

| # | Q | A |
|---|---|---|
| 31 | `map` / `filter` / `reduce` | `Select` / `Where` / `Aggregate` |
| 32 | `find` / `some` / `every` | `FirstOrDefault` / `Any` / `All` |
| 33 | `flatMap` | `SelectMany` |
| 34 | `slice` vs `splice` | Copies a section vs removes/inserts and mutates |
| 35 | `sort` trap | Sorts in place, and as strings by default. Always pass `(a,b)=>a-b` |
| 36 | Dedupe an array | `[...new Set(arr)]` |
| 37 | `Map` vs object | Any key type, ordered, real `.size` vs string keys only. `Map` = `Dictionary` |
| 38 | `Set` | `HashSet<T>` — unique values, fast membership |
| 39 | `WeakMap` | Keys don't stop garbage collection — for caches |
| 40 | `Object.entries` | `[key, value]` pairs, handy with `map` |
| 41 | Is JS single-threaded? | Yes — one thread, non-blocking via the event loop |
| 42 | Event loop | Slow work is handed off; callbacks queue and run when the thread is free |
| 43 | Microtask vs macrotask | Promises before timers. **Sync → promises → timers** |
| 44 | `setTimeout(fn, 0)` | Runs after the sync code and after all pending promises |
| 45 | `setTimeout` vs `setInterval` | Once after a delay vs repeatedly. Always clear them |
| 46 | Promise | A placeholder for a future value — C#'s `Task<T>` |
| 47 | Promise states | Pending → fulfilled or rejected. Settles once, permanently |
| 48 | `Promise.all` | All must succeed; fails fast — `Task.WhenAll` |
| 49 | `allSettled` / `race` / `any` | All outcomes / first to settle / first to succeed |
| 50 | Two `await`s in a row | Sequential. Use `Promise.all` for parallel |
| 51 | Does `fetch` throw on 404? | **No** — check `res.ok` yourself |
| 52 | Unhandled rejection | A rejected promise nobody caught; crashes modern Node |
| 53 | `async` function returns | Always a Promise, even if you return a plain value |
| 54 | `for await (const x of stream)` | Async iteration — like `await foreach` |
| 55 | Generators in JS | `function*` and `yield` — same idea as C# `yield return` |
| 56 | Debounce vs throttle | Wait until it stops vs at most once per interval |
| 57 | Web Worker | A real second thread; message passing, no shared memory |
| 58 | Live data to a browser | WebSockets, or SignalR with a .NET backend. SSE if one-way |

### JavaScript — browser and platform (59–70)

| # | Q | A |
|---|---|---|
| 59 | Event bubbling | The event travels up through the ancestors after firing |
| 60 | Event capturing | The phase going down before it reaches the target |
| 61 | Event delegation | One listener on the parent; check `event.target`. Scales to huge lists |
| 62 | `stopPropagation` vs `preventDefault` | Stop the bubble vs cancel the browser's default action |
| 63 | `removeEventListener` gotcha | Needs the same function reference — an inline arrow can't be removed |
| 64 | ESM vs CommonJS | Static `import`, tree-shakeable vs dynamic `require` |
| 65 | Tree shaking | Dropping unused exports at build time — only possible with static imports |
| 66 | `localStorage` vs `sessionStorage` vs cookie | Forever / per tab / sent with every request |
| 67 | Where do tokens go? | An `HttpOnly` `Secure` `SameSite` cookie — never `localStorage` |
| 68 | What is CORS? | Browser rule: cross-origin reads need server opt-in headers |
| 69 | Does CORS secure my API? | **No** — it protects the user's browser. The API still needs authn/authz |
| 70 | JS memory leaks | Listeners never removed, timers never cleared, detached DOM nodes, big closures |

### TypeScript (71–88)

| # | Q | A |
|---|---|---|
| 71 | What is TypeScript? | JS plus compile-time types; erased at runtime |
| 72 | Does TS check types at runtime? | **No** — use Zod at the boundary |
| 73 | Same model as? | Python type hints — erased, checked by a separate tool |
| 74 | `any` vs `unknown` | "I give up" vs "prove it before you use it". Prefer `unknown` |
| 75 | `never` | The function never returns — throws or loops forever |
| 76 | `interface` vs `type` | Interfaces merge and extend; types do unions and computed types |
| 77 | Union type | `string \| number` |
| 78 | Narrowing | TS follows `typeof` / `in` / `instanceof` checks to work out the type |
| 79 | Type guard | `function isOrder(x): x is Order` — teaches TS to narrow |
| 80 | Discriminated union | A shared literal tag field tells TS which shape it is |
| 81 | Generics | `<T>`; `extends` is C#'s `where` constraint |
| 82 | Four utility types | `Partial`, `Pick`, `Omit`, `Record` |
| 83 | `keyof` | The union of a type's property names |
| 84 | Mapped type | `{ [K in keyof T]: ... }` — how `Partial` is built |
| 85 | `strict: true` | All checks on, including `strictNullChecks`. Always |
| 86 | `x as Order` | A type assertion — no runtime check. Use sparingly |
| 87 | Why avoid `enum`? | It generates runtime code; string literal unions are lighter |
| 88 | `satisfies` | Check against a type without widening the value |

### React (89–110)

| # | Q | A |
|---|---|---|
| 89 | React in one line | **UI = f(state)** — components are functions of data |
| 90 | JSX | HTML-looking syntax that compiles to function calls |
| 91 | Props vs state | Passed in and read-only vs owned by the component and changeable |
| 92 | Send data to a parent? | Parent passes a callback down; the child calls it. **Props down, events up** |
| 93 | Why isn't `setState` immediate? | Batched and async — use `setX(prev => ...)` |
| 94 | `useEffect` dependency array | `[]` once / `[x]` on change / omitted every render (usually a bug) |
| 95 | Why return a function from `useEffect`? | Cleanup — unsubscribe, clear timers. It's `Dispose()` |
| 96 | When do you actually need `useEffect`? | Only to sync with something outside React. Not for data fetching |
| 97 | `useRef` | A mutable box that survives renders and does **not** trigger one |
| 98 | `useMemo` vs `useCallback` | Cache a value vs cache a function. Only when measured |
| 99 | `useContext` | Avoid prop drilling. Low-frequency values only. Like a DI singleton |
| 100 | `useReducer` | Centralise complex state transitions — a state machine |
| 101 | Rules of hooks, and why | Top level only — React tracks hooks by call order |
| 102 | Custom hook | Any function starting with `use` that calls hooks. How you share logic |
| 103 | Why keys in lists? | So React can match items between renders. Never the array index |
| 104 | What causes a re-render? | State, props, parent re-render, or a context change |
| 105 | Reconciliation | Compare new output to old; touch the real DOM only where it differs |
| 106 | `React.memo` | Skip re-rendering when props are unchanged |
| 107 | Controlled vs uncontrolled | React state owns the value vs the DOM owns it |
| 108 | Error boundary | Catches render errors in a subtree. A try/catch around a region of UI |
| 109 | StrictMode double-render | Development only — deliberately exposes missing cleanup |
| 110 | When do you reach for Redux? | Rarely. Server state → TanStack Query. Local state first |

---

# PART 6 — IF THEY ASK YOU TO WRITE CODE (unlikely — 10 minutes to be safe)

### A debounced search box — the classic small exercise
```jsx
function useDebounced(value, delay = 300) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(t);       // cancels the previous timer — THE key line
  }, [value, delay]);
  return debounced;
}

function Search({ onSearch }) {
  const [text, setText] = useState("");
  const query = useDebounced(text);
  useEffect(() => { if (query) onSearch(query); }, [query, onSearch]);
  return <input value={text} onChange={e => setText(e.target.value)} />;
}
```
**Narrate as you write:** *"Controlled input. Custom hook so the logic is reusable. The cleanup
cancels the old timer — that's what makes it a debounce rather than a delay. Dependency arrays
correct."*

### Typing a component in TypeScript
```tsx
interface Props {
  symbol: string;
  price: number;
  onSelect?: (symbol: string) => void;
  children?: React.ReactNode;
}

export function PriceRow({ symbol, price, onSelect }: Props) {
  return <div onClick={() => onSelect?.(symbol)}>{symbol} {price.toFixed(2)}</div>;
}
```
**Say:** *"That's genuinely most of what 'React with TypeScript' means day to day — an interface for
props."*

### Group an array (covers half of all small JS exercises)
```js
const bySymbol = trades.reduce((acc, t) => {
  (acc[t.symbol] ??= []).push(t);
  return acc;
}, {});
// or, modern:
const grouped = Object.groupBy(trades, t => t.symbol);
```

---

# PART 7 — YOUR 5 SAFE, HIGH-VALUE ANSWERS

If you remember nothing else from this file, remember these five. They're architectural, they're
true, and they play to your actual strength.

1. **"UI = f(state)"** — React re-runs the component when state changes and updates only what
   differs. Same idea as WPF binding with `INotifyPropertyChanged`.

2. **"Props down, events up"** — one-way data flow is what makes large UIs predictable.

3. **"Most of what teams put in Redux was actually server state"** — that belongs in TanStack Query
   or RTK Query, which handles caching and staleness. Local state first, lift when shared.

4. **"TypeScript's types are erased at runtime — exactly like Python's type hints"** — so validate at
   the boundary with Zod, the way I'd use Pydantic in Python. Types catch developer mistakes, not bad
   data.

5. **"My depth is backend"** — say it plainly (Part 0). For this role, that's the right depth to have.
