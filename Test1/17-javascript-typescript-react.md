# 17 — JavaScript, TypeScript, React & Angular — in plain words

> **Read this one first, before anything else in this file:**
>
> The JD asks for *"JavaScript with frameworks — **Medium** level"*. Medium. Not advanced. React is
> never even named. **This is a backend/desktop role.** You do **not** need to be a React expert.
>
> What you need is: understand the ideas well enough to explain them simply, and have honest,
> confident answers if they probe. Budget **90 minutes**, not a day.
>
> Everything below is explained by comparing it to **C# / .NET**, which you already know deeply.
> That's the fastest route into your memory.

---

## 0. FIRST — the honest calibration line (use this if frontend comes up)

Your CV lists a lot of frontend. If your real depth is thinner, **say so early and simply**. It costs
you nothing and protects you completely:

> *"Quick note on the front end — I've worked across React, Angular and Vue on the platforms I've
> built, but I'd describe myself as a backend-heavy full stack engineer. I'm comfortable building and
> reviewing UI code and I understand the architecture side — component design, state management,
> build tooling, micro-frontends. But my real depth is .NET, distributed systems and data. If you
> need someone whose primary craft is front end, I'm not that person; if you need someone who can
> work across the stack with backend depth, that's me."*

**Why this is the right move:** interviewers don't punish honest calibration — they punish discovering
a gap themselves. And for *this* role, backend depth is what they're buying anyway. Saying it out
loud actually strengthens your positioning.

⚠️ Related: consider softening the frontend claims on your CV (see `02` §6). "React 19, Angular 2–20,
Vue 3" invites a drill you don't need.

---

# PART 1 — JAVASCRIPT (the language underneath everything)

## 1.1 The one-paragraph mental model

JavaScript runs in a browser (or Node.js). It is **single-threaded** — one thing at a time — but it
never sits and waits. When something slow happens (a network call), JS hands it off and carries on;
when the result arrives, the callback goes in a queue and runs when the thread is free.

**C# comparison:** it's like an app with **one** UI thread and no thread pool. Everything is
`async/await` on that one thread. If you block it, the whole page freezes — exactly like blocking
the WPF dispatcher (`05` §7). **That comparison alone answers half of the JS questions you'll get.**

## 1.2 `var` vs `let` vs `const` — know this cold, it's the most-asked JS question

| | Scope | Can reassign? | Hoisting |
|---|---|---|---|
| `var` | **function** scope | yes | hoisted, value is `undefined` |
| `let` | **block** scope `{}` | yes | hoisted but unusable before declaration ("temporal dead zone") |
| `const` | **block** scope | **no** | same as `let` |

**Simple answer to give:** *"Use `const` by default, `let` when you need to reassign, and never `var`
— `var` is function-scoped, which causes surprising bugs in loops."*

⚠️ **`const` does not mean immutable.** It means the *variable* can't be re-pointed. The object it
points at can still change:
```js
const user = { name: "Awais" };
user.name = "Ali";        // ✅ allowed — we changed the object
user = { name: "Ali" };   // ❌ error — we tried to re-point the variable
```
**C# comparison:** `const` here behaves like `readonly` on a reference field — the reference is
fixed, the object isn't.

## 1.3 `==` vs `===`

- `===` compares **value and type**. No surprises.
- `==` converts types first, and the rules are strange: `0 == "0"` is true, `null == undefined` is
  true, `"" == 0` is true.

**Answer:** *"Always `===`. The only common exception is `x == null`, which conveniently checks for
both `null` and `undefined`."*

## 1.4 `null` vs `undefined`
- `undefined` = "nobody set this yet" (the default).
- `null` = "someone deliberately set this to nothing".
- **C#:** both are roughly `null`, but JS splits "never assigned" from "assigned nothing".

## 1.5 Truthy and falsy
Falsy values (everything else is truthy): `false`, `0`, `""`, `null`, `undefined`, `NaN`.
⚠️ Gotcha: `[]` and `{}` are **truthy**. And `if (count)` is a bug when `count` can legitimately be 0
— use `if (count !== undefined)` or `??`.

```js
const name = input ?? "default";   // ?? only falls back on null/undefined  ✅ safer
const name = input || "default";   // || also falls back on 0 and ""       ⚠️ common bug
const city = user?.address?.city;  // ?. optional chaining — no crash if address is missing
```
**C#:** `??` and `?.` are literally the same operators you use in C#. Easy win.

## 1.6 The event loop (the one "how does it work" question)

**Explain it like this — simple and correct:**
> *"JavaScript has one thread. Slow things like network calls are handed to the runtime, and when
> they finish, their callbacks are put in a queue. The event loop takes the next callback from the
> queue whenever the thread is free. So JS is single-threaded but non-blocking. If you run a long
> loop, nothing else happens — the page freezes — which is the same problem as blocking the WPF
> dispatcher thread."*

If they push further: **microtasks** (promises) run before **macrotasks** (`setTimeout`), and all
microtasks drain before the next macrotask.
```js
console.log("1");
setTimeout(() => console.log("2"), 0);   // macrotask — runs last
Promise.resolve().then(() => console.log("3"));  // microtask — runs before setTimeout
console.log("4");
// Output: 1, 4, 3, 2
```
That output order is a classic interview question. **Memory hook: "sync → promises → timers."**

## 1.7 Promises & async/await

A **Promise** is a placeholder for a value that isn't ready yet. **C#: it's a `Task<T>`.**
States: pending → fulfilled or rejected.

```js
// async/await — identical in spirit to C#
async function loadUser(id) {
  try {
    const res = await fetch(`/api/users/${id}`);
    if (!res.ok) throw new Error(res.status);
    return await res.json();
  } catch (err) {
    console.error(err);
    throw err;
  }
}

await Promise.all([a, b, c]);      // C#: Task.WhenAll — all must succeed
await Promise.allSettled([a, b]);  // never rejects; tells you each outcome
await Promise.race([a, timeout]);  // C#: Task.WhenAny — first one wins
```
⚠️ `fetch` does **not** throw on a 404 or 500 — you must check `res.ok` yourself. Common gotcha.

## 1.8 `this` — the confusing one, made simple

**Simple rule:** in a normal `function`, `this` depends on **how it was called**. In an **arrow
function**, `this` is whatever it was in the surrounding code — arrows don't have their own `this`.

**Practical takeaway:** *"Use arrow functions in callbacks and you almost never have a `this`
problem."* That's the whole answer at medium level. Don't go deeper unless asked.

## 1.9 Closures

A function that "remembers" the variables around it, even after the outer function has finished.

```js
function makeCounter() {
  let count = 0;                 // stays alive because the inner function uses it
  return () => ++count;
}
const next = makeCounter();
next(); // 1
next(); // 2
```
**C#:** exactly a lambda capturing a local variable (`03` §5). Same concept, same memory-leak risk.

## 1.10 The array methods you must recognise
```js
arr.map(x => x * 2)          // transform      → C# .Select()
arr.filter(x => x > 10)      // keep some      → C# .Where()
arr.reduce((sum, x) => sum + x, 0)  // fold    → C# .Aggregate()
arr.find(x => x.id === 5)    // first match    → C# .FirstOrDefault()
arr.some(...) / arr.every(...)  //             → C# .Any() / .All()
arr.sort((a, b) => a - b)    // ⚠️ sorts IN PLACE and sorts as strings by default
```
**Memory hook: JS array methods are LINQ with different names.** `map`=`Select`, `filter`=`Where`,
`reduce`=`Aggregate`, `find`=`FirstOrDefault`. If you remember only that, you can read any JS code.

## 1.11 Spread, destructuring, modules
```js
const merged = { ...defaults, ...overrides };   // copy + override (shallow!)
const [first, second] = myArray;                 // destructuring
const { name, age = 18 } = user;                 // with a default

export function calc() {}      // ES module export
import { calc } from "./calc"; // import
```
⚠️ Spread is a **shallow** copy — nested objects are still shared. Same as `MemberwiseClone` in C#.

---

# PART 2 — TYPESCRIPT

## 2.1 What it is, in one sentence

> *"TypeScript is JavaScript plus a type system that runs at compile time. It compiles to plain
> JavaScript, and the types disappear at runtime — they exist to catch mistakes in the editor and
> the build, not to enforce anything when the code runs."*

**That last part is the key insight and a common question.** There is **no runtime type checking**.
If JSON arrives from an API with the wrong shape, TypeScript will not save you — which is why people
add runtime validation with **Zod** at the boundaries.

**C# comparison:** it's like having C#'s compiler checking a dynamically-typed language, but with the
type information stripped out before the program runs. Types are a *development* tool, not a runtime
guarantee.

## 2.2 The basic types
```ts
let name: string = "Awais";
let age: number = 34;                 // one number type — no int/decimal/float distinction
let ok: boolean = true;
let ids: number[] = [1, 2, 3];
let pair: [string, number] = ["a", 1];   // tuple
let anything: any;        // ⚠️ turns type checking OFF — avoid
let safe: unknown;        // ✅ like 'any' but you must check before using it
function fail(): never {} // never returns (always throws or loops forever)
```
**`any` vs `unknown` — a favourite question.** `any` disables checking entirely (dangerous).
`unknown` says "I don't know the type yet, so you must narrow it before use" (safe).
**Memory hook: `any` = "I give up". `unknown` = "prove it first". Always prefer `unknown`.**

## 2.3 `interface` vs `type`

Both describe a shape. Practical differences:
- `interface` can be **re-opened** and added to (declaration merging); `type` cannot.
- `type` can do things `interface` can't: unions, intersections, mapped/conditional types.

**Answer to give:** *"I use `interface` for object shapes that others might extend, and `type` for
unions and anything computed. In practice either works for most cases — the team should just be
consistent."* That's the honest, senior answer; interviewers don't want dogma here.

## 2.4 Union types & narrowing — the most useful TS idea
```ts
type Status = "new" | "filled" | "cancelled";   // only these three strings are allowed

function describe(x: string | number) {
  if (typeof x === "string") return x.toUpperCase();  // TS knows it's a string here
  return x.toFixed(2);                                 // and a number here
}
```
This is **narrowing**: TypeScript follows your `if` checks and works out the type. Ways to narrow:
`typeof`, `instanceof`, `in`, a literal check, or a custom type guard (`function isX(v): v is X`).

**C# comparison:** unions are like a much more flexible version of an enum, and narrowing is like
pattern matching (`is Type t`) in C#.

## 2.5 Discriminated unions — the pattern worth knowing by name
```ts
type Result =
  | { kind: "ok"; value: number }
  | { kind: "error"; message: string };

function handle(r: Result) {
  switch (r.kind) {                  // the 'kind' field tells TS which shape it is
    case "ok":    return r.value;    // TS knows .value exists
    case "error": return r.message;  // TS knows .message exists
  }
}
```
**Why it matters:** it's the type-safe way to model "one of several possibilities" — states, API
results, order statuses. If you remember **one** advanced TS pattern, remember this one. It's also a
great answer to *"how would you model an order's state in TypeScript?"*

## 2.6 Generics
```ts
function first<T>(items: T[]): T | undefined {
  return items[0];
}
first([1, 2, 3]);     // T is number
first(["a", "b"]);    // T is string

// with a constraint — T must have an id
function byId<T extends { id: number }>(items: T[], id: number) {
  return items.find(i => i.id === id);
}
```
**C#:** identical concept and almost identical syntax — `<T>` and `where T : ...` becomes
`T extends ...`. You already understand this; just note the keyword difference.

## 2.7 Utility types (the ones that come up)
```ts
interface Order { id: number; symbol: string; qty: number; price: number; }

Partial<Order>            // all fields optional      — for update/patch payloads
Required<Order>           // all fields required
Readonly<Order>           // all fields readonly
Pick<Order, "id"|"qty">   // just those fields
Omit<Order, "price">      // everything except price
Record<string, number>    // a dictionary            — C# Dictionary<string,int>
ReturnType<typeof fn>     // the return type of fn
```
**Memory hook: Partial / Pick / Omit / Record are 90% of what you'll ever use.** Learn those four
and you can read most real TypeScript.

## 2.8 Other things worth one line each
- `strict: true` in `tsconfig.json` — turns on all the good checks including `strictNullChecks`
  (which makes `null`/`undefined` explicit, like C#'s nullable reference types). **Always on.**
- `?` = optional property: `email?: string` means `string | undefined`.
- `readonly` on properties — compile-time only.
- `enum` — TS has them, but they generate runtime code; most teams now prefer a union of string
  literals (`type Status = "new" | "filled"`). Worth saying — it shows currency.
- `satisfies` (TS 4.9+) — checks a value matches a type *without* widening it. Nice-to-know.
- `.d.ts` declaration files — types for JS libraries that don't ship their own.
- **Zod** — runtime validation that also gives you the TS type. The standard answer to "types
  disappear at runtime, so how do you trust API data?"

---

# PART 3 — REACT

## 3.1 The mental model, in plain words

> *"React is a library for building UI out of components. A component is a function that takes some
> data (props) and returns what should appear on screen. When the data changes, React re-runs the
> function and updates only the parts of the real page that actually changed."*

**The one sentence that captures React:** **UI = f(state)**. You don't manipulate the screen; you
describe what it should look like for the current state, and React does the updating.

**C#/WPF comparison — this is your best bridge:**
| React | WPF |
|---|---|
| Component | UserControl / View |
| Props | Dependency properties passed in |
| State (`useState`) | View-model property + `INotifyPropertyChanged` |
| Re-render on state change | Binding updates the UI on `PropertyChanged` |
| Virtual DOM diffing | WPF's own dirty-region rendering |

**Say that comparison in the interview** — it shows you understand both, and it makes your WPF story
stronger too.

## 3.2 Components and props
```jsx
function PriceTag({ symbol, price }) {        // props come in as an object
  return <div>{symbol}: {price.toFixed(2)}</div>;
}

<PriceTag symbol="AAPL" price={182.35} />     // used like an HTML tag
```
- **JSX** is HTML-looking syntax that compiles to function calls. It's not a template language.
- **Props are read-only.** A component never modifies its own props. Data flows **down**.
- To send data **up**, the parent passes a function down and the child calls it.
  **Memory hook: "props down, events up."**

## 3.3 The hooks you must know (there are only ~5 that matter)

### `useState` — local state
```jsx
const [count, setCount] = useState(0);
setCount(count + 1);           // fine for simple cases
setCount(prev => prev + 1);    // ✅ safer — use when the new value depends on the old one
```
⚠️ **State updates are asynchronous and batched.** Reading `count` right after `setCount` gives you
the *old* value. That's why the `prev =>` form exists. **Very common interview question.**

### `useEffect` — run code after render (side effects)
```jsx
useEffect(() => {
  const timer = setInterval(tick, 1000);
  return () => clearInterval(timer);   // cleanup — runs on unmount or before the next run
}, []);                                 // dependency array
```
The **dependency array** decides when it runs:
- `[]` → once, after the first render (like a constructor / `OnLoaded`)
- `[userId]` → whenever `userId` changes
- *omitted* → after **every** render (usually a bug)

⚠️ **The cleanup function is the #1 thing juniors forget** — it's how you unsubscribe. Without it you
leak timers and subscriptions. **C#: it's `Dispose()`.** Saying that connection is a strong answer.

⚠️ **Modern point worth making:** *"The React team's guidance now is that you probably need `useEffect`
less than you think — it's for synchronising with something outside React, like a subscription or a
timer. Data fetching is better handled by a library like TanStack Query, and anything derivable from
existing state should just be calculated during render, not stored in state."* **That single answer
marks you as current rather than someone who learned React in 2019.**

### `useRef` — a box that survives re-renders without causing one
```jsx
const inputRef = useRef(null);       // grab a DOM element
const renderCount = useRef(0);       // or hold a mutable value
```
**Memory hook: state re-renders, ref doesn't.**

### `useMemo` / `useCallback` — caching
- `useMemo` caches a **computed value**; `useCallback` caches a **function**.
- Both exist to avoid re-doing expensive work or breaking a child's memoisation.
- ⚠️ **Honest senior answer:** *"I don't reach for them by default — they add complexity and have
  their own cost. I use them when profiling shows a real problem, or when a function is a dependency
  of an effect. And React 19's compiler increasingly handles this automatically."*

### `useContext` — avoid passing props through many layers
```jsx
const ThemeContext = createContext("light");
const theme = useContext(ThemeContext);
```
⚠️ Context is for **low-frequency** values (theme, current user, locale). Every consumer re-renders
when it changes, so it's a poor fit for fast-changing data. **C#: it's like a DI-injected singleton.**

### The Rules of Hooks (they will check this)
1. Only call hooks at the **top level** — never inside `if`, loops or nested functions.
2. Only call them from React components or custom hooks.

**Why?** React tracks hooks **by call order**. Skip one with an `if` and the order shifts and state
gets attached to the wrong hook. That "why" is what separates a good answer from a memorised one.

## 3.4 Keys in lists — guaranteed question
```jsx
{orders.map(o => <Row key={o.id} order={o} />)}    // ✅ stable, unique id
{orders.map((o, i) => <Row key={i} />)}            // ⚠️ index — breaks on reorder/insert/delete
```
**Why keys exist:** React uses them to work out which items are the same between renders. With index
keys, inserting at the top makes React think every row changed — you get wrong state in the wrong
row and unnecessary re-renders. **Simple answer: "use a stable unique ID, never the array index,
unless the list never changes order."**

## 3.5 Re-rendering — how to explain it simply
A component re-renders when: its **state** changes, its **props** change, its **parent** re-renders,
or a **context** it uses changes.

Re-rendering is **not** the same as updating the page — React compares the new output with the old
(reconciliation, "virtual DOM diffing") and only touches the real DOM where something differs.

To reduce unnecessary re-renders: `React.memo` on the component, stable props (`useCallback`/
`useMemo`), lift state no higher than it needs to be, and split components so a fast-changing piece
of state doesn't re-render the whole tree.

## 3.6 Controlled vs uncontrolled inputs
- **Controlled:** React state is the source of truth (`value={x} onChange={...}`). Preferred.
- **Uncontrolled:** the DOM holds the value; you read it with a ref.
**C#/WPF:** controlled = two-way binding; uncontrolled = reading `TextBox.Text` directly.

## 3.7 State management — the architecture answer (your comfort zone)
> *"I'd start with local component state, lift it up when it's shared, and use context for
> low-frequency global values like the current user or theme. I only add a state library when there's
> genuine shared client state — Redux Toolkit or Zustand. The big shift is that most of what people
> used to put in Redux was actually **server** state, and that belongs in a data-fetching library
> like TanStack Query or RTK Query, which handles caching, refetching and staleness for you."*

That's a genuinely senior answer and it's architectural, not syntactic — which plays to your strength.

## 3.8 Things worth one line each
- **Error boundaries** — catch render errors in a subtree so the whole app doesn't die. Class
  components only (or a library). **C#: a try/catch around a region of UI.**
- **StrictMode** in development deliberately runs effects twice to expose missing cleanup. Surprises
  people — good to know.
- **Server Components (RSC)** — components that render on the server and ship no JS to the browser.
  Next.js App Router. One line: *"they cut bundle size and let you fetch data server-side, with
  client components only where you need interactivity."*
- **Suspense** — declare a loading fallback while something loads.
- **Custom hooks** — just a function starting with `use` that calls other hooks. How you share logic.
  **C#: extracting a shared service.**
- **Testing** — React Testing Library: test what the user sees and does, not internal state.

---

# PART 4 — ANGULAR (30-second version — only if they ask)

Angular is a **full framework** (not a library like React): routing, HTTP, forms and DI are all
built in and opinionated.

**Why you'll find Angular easy to talk about: it's the most C#-like frontend framework.**
- **Dependency injection** built in — constructor injection, exactly like ASP.NET Core.
- **TypeScript-first**, decorators (`@Component`, `@Injectable`) — like C# attributes.
- Structured into modules/components/services — like a layered .NET app.
- **RxJS observables** for async streams — like `IObservable`/Rx.NET or `IAsyncEnumerable`.
- **Signals** (Angular 16+) are the modern reactive primitive replacing much of RxJS and
  zone.js-based change detection.

**React vs Angular in one sentence:** *"React is a library — you assemble your own stack and it's
more flexible; Angular is a full opinionated framework with DI, routing and forms included, which
suits large enterprise teams that want consistency. I've worked with both; Angular's structure feels
natural coming from .NET."*

---

# PART 5 — 40 QUESTIONS WITH SHORT ANSWERS (cover the right column and test yourself)

### JavaScript
| # | Q | A |
|---|---|---|
| 1 | `var` / `let` / `const` | function-scoped / block-scoped / block-scoped and can't be reassigned |
| 2 | Is `const` immutable? | No — the variable can't be re-pointed; the object can still change |
| 3 | `==` vs `===` | Type coercion vs strict. Always use `===` |
| 4 | `null` vs `undefined` | Deliberately empty vs never set |
| 5 | Falsy values | `false, 0, "", null, undefined, NaN` |
| 6 | `??` vs `\|\|` | `??` only falls back on null/undefined; `\|\|` also on 0 and "" |
| 7 | Is JS single-threaded? | Yes — one thread, but non-blocking via the event loop |
| 8 | Event loop | Slow work is handed off; callbacks queue up and run when the thread is free |
| 9 | Microtask vs macrotask | Promises run before `setTimeout`; sync → promises → timers |
| 10 | What's a Promise | A placeholder for a future value — C#'s `Task<T>` |
| 11 | `Promise.all` vs `allSettled` vs `race` | All must succeed / all outcomes reported / first wins |
| 12 | Does `fetch` throw on 404? | **No** — check `res.ok` yourself |
| 13 | Closure | A function that remembers the variables around it |
| 14 | Arrow vs normal function | Arrows have no own `this` — they use the surrounding one |
| 15 | `map`/`filter`/`reduce` | `Select` / `Where` / `Aggregate` in LINQ |
| 16 | Shallow vs deep copy | Spread `{...x}` is shallow — nested objects still shared |
| 17 | Hoisting | Declarations are moved up; `var` is `undefined`, `let`/`const` are unusable first |
| 18 | Debounce vs throttle | Wait until it stops / run at most once per interval |

### TypeScript
| # | Q | A |
|---|---|---|
| 19 | What is TypeScript | JS + compile-time types; types are erased at runtime |
| 20 | Does TS check types at runtime? | **No** — use Zod for runtime validation of API data |
| 21 | `any` vs `unknown` | "I give up" vs "prove it before using it" — prefer `unknown` |
| 22 | `interface` vs `type` | Interfaces merge/extend; types do unions and computed types |
| 23 | Union type | `string \| number` — one of several allowed types |
| 24 | Narrowing | TS follows your `typeof`/`in`/`instanceof` checks to work out the type |
| 25 | Discriminated union | A shared literal field (`kind`) tells TS which shape it is |
| 26 | Generics | `<T>` — same as C#; `extends` is C#'s `where` constraint |
| 27 | Four utility types | `Partial`, `Pick`, `Omit`, `Record` |
| 28 | `strict: true` | Turns on all checks incl. `strictNullChecks` — always on |
| 29 | Why avoid `enum` | Generates runtime code; string literal unions are lighter |
| 30 | Type guard | `function isOrder(x): x is Order` — teaches TS to narrow |

### React
| # | Q | A |
|---|---|---|
| 31 | What is React in one line | UI = f(state); components are functions of data |
| 32 | Props vs state | Passed in and read-only vs owned by the component and changeable |
| 33 | How do you send data to a parent? | Parent passes a callback down; child calls it. "Props down, events up" |
| 34 | Why is `setState` not immediate? | Updates are batched and async — use `setX(prev => ...)` |
| 35 | `useEffect` dependency array | `[]` once / `[x]` when x changes / omitted every render (usually a bug) |
| 36 | Why return a function from `useEffect`? | Cleanup — unsubscribe/clear timers. It's `Dispose()` |
| 37 | Rules of hooks + why | Top level only, same order every render — React tracks hooks by call order |
| 38 | Why keys in lists? | So React can match items between renders; never use the index |
| 39 | `useMemo` vs `useCallback` | Cache a value vs cache a function; use only when measured |
| 40 | When to reach for Redux? | Rarely — server state belongs in TanStack Query; local state first |

---

# PART 6 — IF THEY ASK YOU TO WRITE CODE (unlikely, but 10 minutes to be safe)

### A debounced search box (the classic small React exercise)
```jsx
function useDebounced(value, delay = 300) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(t);        // cancel the previous timer — the key line
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
**Narrate:** controlled input · custom hook to share logic · the cleanup cancels the old timer, which
is what makes it a debounce · dependency arrays are correct.

### Typing a component in TypeScript
```tsx
interface Props {
  symbol: string;
  price: number;
  onSelect?: (symbol: string) => void;   // optional callback
  children?: React.ReactNode;
}

export function PriceRow({ symbol, price, onSelect }: Props) {
  return <div onClick={() => onSelect?.(symbol)}>{symbol} {price.toFixed(2)}</div>;
}
```
That's genuinely most of what "React with TypeScript" means day to day: **an interface for props**.

---

# PART 7 — YOUR 5 SAFE, HIGH-VALUE ANSWERS

If you remember nothing else from this file, remember these five. They're architectural, they're
true, and they play to your actual strength:

1. **"UI = f(state)"** — React re-runs the component when state changes and updates only what
   differs. Same idea as WPF binding with `INotifyPropertyChanged`.
2. **"Props down, events up"** — one-way data flow is what makes large UIs predictable.
3. **"Most of what teams put in Redux was actually server state"** — that belongs in TanStack Query
   or RTK Query, which handles caching and staleness. Local state first, lift when shared.
4. **"TypeScript's types are erased at runtime"** — so validate at the boundary with Zod. Types
   catch developer mistakes, not bad data.
5. **"My depth is backend"** — say it plainly (§0). For this role that's the right depth to have.
