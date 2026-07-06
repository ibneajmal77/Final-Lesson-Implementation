# 07 — OOP & C# Fundamentals This Interview Actually Uses

## Plain English version

This file explains the C# and OOP words you may need to say during the interview.

You do not need fancy theory. You need simple meanings:

- **Encapsulation:** keep deck cards private, so outside code cannot damage the deck.
- **Abstraction:** call `Deal()` without caring how the deck loops internally.
- **Inheritance / polymorphism:** only use these if a second version of a rule really needs to exist.
- **Composition:** a game has a deck; a player has a hand.
- **LINQ:** use simple helpers like `Sum`, `Where`, `GroupBy`, and `OrderBy`.

Simple example:

`ScoreHand(player)` can be one line:

```csharp
return player.Hand.Sum(PointsOf);
```

That means: for every card in the hand, call `PointsOf`, then add the results.

You write C# daily, so this file is not "learn C#." It does two jobs:
1. **Name the concepts you already use**, so you can say them out loud — the interview grades "consistent application of coding principles," and naming the principle while applying it is how that gets seen.
2. **Sharpen the exact language features, collections and LINQ operators** card games touch, so nothing costs you a syntax pause on the day.

---

## The four OOP pillars, card-game edition

| Pillar | Where it lives in the skeleton | Say-line for the interview |
|---|---|---|
| **Encapsulation** | `Deck._cards` is `private`; the only doors are `Shuffle`/`Draw` | "The deck owns its cards — outside code can't reorder or corrupt it." |
| **Abstraction** | `Main` calls `Deal`/`Winners`; it has no idea Fisher–Yates exists | "The game exposes what it does, not how." |
| **Inheritance** | `Game.PointsOf` is `virtual`; a variant game `override`s it | "I inherit to *change one behavior*, not to reuse fields." |
| **Polymorphism** | The same `ScoreHand` call does different things per game class; a `Func<Card,int>` delegate is polymorphism without a class | "This call site never changes — only the rule behind it does." |

## Composition over inheritance

- `Game` **has a** `Deck`; `Player` **has a** hand. Has-a → field. Is-a-with-different-behavior → maybe a subclass.
- Smell to avoid: `JokerDeck : Deck` just to add two cards. Deck *contents* are data → a constructor parameter (`includeJokers`), never a subclass.
- Keep inheritance one level deep in a timed exercise. Deeper hierarchies are where velocity goes to die.

## SOLID — one card-game line each

Use these when explaining an improvement ("with more time I'd…"), not as decoration.

- **S**ingle responsibility — `Deck` changes when deck rules change, never when scoring does. One reason to change per class.
- **O**pen/closed — a second scoring variant is *added* (override / delegate), not edited into every call site. Interview pragmatism: the FIRST variant edits the method in place; the SECOND triggers the extraction. That's the rule of two from `03`.
- **L**iskov substitution — any game subclass must keep the contracts: `Winners` still returns *all* tied players, `Draw` still throws on empty.
- **I**nterface segregation — small public surfaces. `Deck` needs three members, not twelve "just in case."
- **D**ependency inversion — `ScoreHand` depends on the `PointsOf` abstraction, not on values inlined at call sites. That indirection is exactly what makes mutations one-line edits.

## Coupling & cohesion (the words behind the routing table)

- **High cohesion:** everything about "what a card is worth" sits in one method. The routing table in `03` is literally a cohesion map of your file.
- **Low coupling:** printing knows nothing about point values; scoring knows nothing about `Console`. Test yourself: could you change the display format without touching a rule? Could you change a rule without touching display?

---

## C# features in the skeleton — recognize them, and their error messages

| Feature | In the skeleton | Worth knowing |
|---|---|---|
| Get-only auto-property | `public string Rank { get; }` | Settable only in the constructor → cards are immutable |
| Expression-bodied member | `public int Count => _cards.Count;` | `=>` form of a one-line member |
| `static class` | `Ranks`, `Suits` | No instances — pure rule data + helpers |
| `sealed` | `sealed class Card` | "Nobody inherits this" — say it's deliberate |
| `virtual` / `override` | `virtual int PointsOf(Card)` | The polymorphism hook; `base.PointsOf(c)` calls the original |
| Optional + named args | `new Deck(includeJokers: true)` | Reads like documentation at the call site |
| Nullable value type | `int? seed` | `seed.HasValue` / `seed.Value` |
| String interpolation + alignment | `$"{p.Name,-6} {score,3}"` | `-6` left-pads name, `3` right-aligns number — instant tables |
| Tuple swap | `(a, b) = (b, a)` | The 1-line Fisher–Yates swap |
| Method group | `Players.Max(ScoreHand)` | A method name where a lambda fits |
| Collection initializer | `{ "C", "D", "H", "S" }` | Rule data in one glance |

Two error messages to recognize instantly:
- *"'List<Card>' does not contain a definition for 'Sum'"* → you forgot `using System.Linq;`
- *"Collection was modified; enumeration operation may not execute"* → you removed from a list inside `foreach` over it.

## Collections — which one, when

| Type | Card-game use | Trap |
|---|---|---|
| `List<T>` | Hands, decks — the workhorse | `RemoveAt(0)` is O(n) → draw from the END; never remove inside `foreach` |
| `Dictionary<K,V>` | Point tables when a `switch` grows: `new Dictionary<string,int> { {"J",10}, {"Q",10} }` | `dict["missing"]` throws → `TryGetValue` |
| `Queue<T>` | War piles: `Dequeue()` the top, `Enqueue()` winnings to the bottom — models a pile naturally | Can't index into the middle |
| `Stack<T>` | A discard pile where only the top matters (Crazy Eights) | `Peek` vs `Pop` |
| Array | Fixed rule data (`Ranks.Order`) | Fixed size — right for rules, wrong for hands |
| `HashSet<T>` | "Have I seen this rank?" | Unordered |

## LINQ — the 12 operators that cover every card game

| Operator | Card one-liner |
|---|---|
| `Sum` | `hand.Sum(PointsOf)` |
| `Max` / `Min` | `Players.Max(ScoreHand)` — "lowest wins" mutation = swap to `Min` |
| `Where` | `Players.Where(p => ScoreHand(p) == best)` |
| `Select` | `names.Select(n => new Player(n))` |
| `OrderBy` + `ThenBy` | `hand.OrderBy(c => c.Strength)` — sorted *display*, don't mutate the hand |
| `OrderByDescending(...).First()` | Best card — throws on empty, guard it |
| `GroupBy` | `hand.GroupBy(c => c.Rank)` — pairs/trips detection in one call |
| `Any` / `All` | `groups.Any(g => g.Count() == 3)` · `hand.All(c => c.Suit == first)` (flush) |
| `Count(pred)` | `hand.Count(c => c.Suit == "D")` |
| `FirstOrDefault` | Returns `null` for classes when nothing matches — check it |
| `ToList` | Materialize before mutating the source, or the query re-runs |
| `string.Join` | `string.Join(" ", hand)` — calls each card's `ToString` |

**Deferred execution in one sentence:** a LINQ query is a *recipe*, re-cooked every time you enumerate it — `ToList()` freezes the result; do that before you mutate the underlying collection.

## Big-O — the one paragraph you need

Deck size is 52; nothing here is a performance problem, and saying so correctly is the senior move. Know these if asked: Fisher–Yates is O(n); `Array.IndexOf` over 14 ranks is a constant (a `Dictionary` lookup would be O(1) — mention it, don't build it); `GroupBy`/`Sum` are O(n); library sort is O(n log n); `RemoveAt(0)` is O(n) which is why the skeleton draws from the end. Answer template: *"Everything is linear in deck size, and n is 52 — I'm optimizing for readability and changeability instead."*

## Errors & defensive style for a timed exercise

- **Fail loud at bad state:** `throw new InvalidOperationException("Cannot draw from an empty deck.")` — a clear crash beats a silent wrong answer.
- `ArgumentException` = the caller passed something bad; `InvalidOperationException` = the object is in the wrong state for the call. One sentence, correct usage, done.
- Do **not** wrap game logic in `try/catch` — you'd be hiding the bugs you need to see. No input validation ceremonies unless a part asks for input.

## Testing shape (vocabulary for what you already do)

- Even a one-line check has **arrange–act–assert**: build the card, compute the points, compare.
- **Determinism:** randomness is the enemy of verification → seeded `Random` while developing, said out loud.
- **Edge probes** worth their 20 seconds: empty deck throws · joker displays `JOKER` · a forced tie returns two winners.
- On every mutation: change the check FIRST (red), then the code (green). The `Check` helper makes this visible to the interviewer on every run.

## Dry run: how LINQ behaves on one hand

Hand: `7H 7S QD 2C 9H`.

```csharp
var score = hand.Sum(PointsOf);
```

Dry run:
- `PointsOf(7H)` returns 7.
- `PointsOf(7S)` returns 7.
- `PointsOf(QD)` returns 12, or 10 if the face-card mutation happened.
- `PointsOf(2C)` returns 2.
- `PointsOf(9H)` returns 9.
- `Sum` adds those returned numbers.

For classification:

```csharp
var groups = hand.GroupBy(c => c.Rank);
```

Dry run:
- Rank `7` has 2 cards.
- Rank `Q` has 1.
- Rank `2` has 1.
- Rank `9` has 1.

That means "One Pair" with defining rank `7`. The hand did not change; `GroupBy` only gave you a useful view of it.
