# 00 — The Complete Guide (everything, in one place, in simple words)

This one file ties all the lessons together into a single path: what the interview is, how to picture any card game, the one design idea that everything rests on, exactly how to start coding, how to handle rule changes, what to do on the day, and how to practice. Read it top to bottom once. After that, use it as your map.

The other files (`01`–`10`, the mocks, the skeleton) go deeper on each topic. This file is the trunk; they are the branches.

---

## Part 0 — The one sentence that explains everything

> You build a small card game while the interviewer keeps changing the rules. You pass by putting **each rule in exactly one place**, so every change is a small edit — not a rewrite.

That's it. Everything below serves that one sentence. If you remember nothing else, remember that.

---

## Part 1 — What this interview actually is

This is **not** a puzzle/LeetCode interview. It's a fast **building** exercise. In their own words: *"a fast-paced implementation task… like a simulator, where the rules keep changing as you code."*

**The shape:**
- Platform: **HackerRank**, screen shared, camera on.
- **One** problem, split into **3 cumulative parts** (each part builds on the last).
- Total time: about **60 minutes** → roughly 15 min Part 1, 18 min Part 2, 18 min Part 3, small buffer.
- Your language: **C#** (it's your daily language — fluency beats cleverness here).

**The three parts you should expect:**
1. **Part 1 — Card + Deck.** Model a card, build a 52-card deck, shuffle, deal. This part is almost always the same, so you make it pure muscle memory.
2. **Part 2 — a real game.** Deal to players, then score-and-compare, or a round loop, or hand classification.
3. **Part 3 — rapid rule changes.** 2–4 changes, ~5 minutes each: point values change, a suit gets special treatment, jokers appear, tie rules appear, ordering flips. Each should be a *small* edit **if** your Part 1–2 structure was clean.

**They grade 5 things (this is literally what the interviewer writes down):**
1. **Understanding** — did you restate the problem and ask questions that changed what you built?
2. **Think-aloud** — could they follow your reasoning without asking?
3. **Clean code** — is every rule in one obvious place? Clear names? No duplicated logic?
4. **Velocity** — did all three parts get done, and stay runnable the whole time?
5. **Testing & unblocking** — did you prove it works as you went, and get unstuck with docs/prints instead of flailing?

**Two hard rules that never bend:**
- **Using any LLM = automatic fail.** But **documentation and Google are allowed and expected** — looking things up fast is a graded skill, so practice it.
- **The narration is half the exam.** A silent perfect solution scores worse than a talked-through good one.

**The rhythm of every part** (memorize this loop): **restate → ask → route → code → check → rerun.**

---

## Part 2 — First, picture the game (don't code yet)

Before writing anything, imagine the table like a short movie. Ask these 5 questions:

1. **Who are the players?**
2. **Where are the cards?** (each player's hand, the deck, any piles)
3. **Whose turn is it?**
4. **What is one player allowed to do?**
5. **How do we know who won?**

Then turn the answers into code pieces:
- People → `Player`
- A card → `Card`
- The remaining cards → `Deck`
- The rules → methods like `PointsOf`, `IsPlayable`, `WinnerOfTrick`

**Simple rule of thumb:** if a noun sticks around, it's probably a field or class. If a verb happens, it's probably a method.
- "Player has a hand" → `Player.Hand`
- "Deck can draw" → `Deck.Draw()`
- "A card scores differently per game" → `Game.PointsOf(Card)`
- "You may only play a matching card" → `IsPlayable(card, top)`

**The universal game map** — every prompt fills in this shape:

```
Game
├─ Setup     → what deck? how many players? how many cards each?
├─ State     → hands, deck count, optional piles, optional turn index/leader/direction
├─ One action→ deal one / draw one / play one / compare one / score one hand
├─ Rule homes→ points=PointsOf · order=Ranks.Order · legal=IsPlayable · winner=Winners · turn=AdvanceTurn
└─ End       → fixed rounds? empty hand? empty deck? highest score?
```

If you can fill this map out loud in 30 seconds, you can write the code.

---

## Part 3 — Know the card domain (three ideas people mix up)

A single card carries **three separate ideas**. Keeping them apart is the whole game:

1. **Rank order** = how strong a card is. A Q beats a 7.
2. **Points** = how many score points a card is worth. A Q might be 12 in one game, 10 in another.
3. **Suit** = the symbol: C, D, H, S. Suits normally have **no** strength order — unless a rule says so.

Example: `QD` = "queen of diamonds." Its **rank** is Q, its **suit** is D, its **points** depend on the game.

So when a rule changes, first decide which idea it touches:
- "A queen is worth 10" → **points**
- "A queen beats a jack" → **rank order**
- "Diamonds score double" → a **scoring rule** (points again)

**The single most important distinction: rank ≠ points.**
- **Ordering (strength)** answers "which card wins?" → lives in ONE array: `Ranks.Order`.
- **Points (score)** answers "how much is it worth?" → lives in ONE method: `PointsOf(card)`.

Games change these two things **independently**, so your code keeps them independent.

**Facts to bake in (these come straight from their PDF, and several are traps):**
- **Ace is LOW.** Order: `A 2 3 4 5 6 7 8 9 10 J Q K JOKER`. Most people assume ace-high — don't. Expect "aces are high now" as a Part-3 change.
- **Joker has a rank but NO suit** (use `null`). Special-case it in: display (show `"JOKER"`), deck building (leave it out unless asked; default count is **2**), and any suit rule (a joker is never "a diamond").
- **Their PDF contradicts itself**: it lists JOKER among ranks but says "13 ranks." That's a ready-made clarifying question — asking it shows you read the spec.
- **Suits are unordered** — don't build suit comparison until a rule demands it. When it does, add a small `Suits.Strength` array, same pattern as ranks.
- **Display is rank + suit** (`QD`, `10H`, `JOKER`). Letters are usually fine; confirm with one quick question.

**Other domain pieces to be ready for:**
- **Deck compositions:** standard 52 · with jokers 54 · multiple decks · stripped ("remove all 2s"). All are **constructor parameters**, never new classes.
- **Shuffle:** Fisher–Yates (4 lines, every order equally likely). Seed it while debugging; say you'd remove the seed for real play.
- **Deal:** round-robin (one card each, go around) vs block (all at once). After a fair shuffle they're identical — say that, pick round-robin (real-dealer behavior), move on. Leftover cards stay in the deck.
- **Running out of cards:** three options — throw an error (default: fail loud), reshuffle the discards, or end the game. Decide **only when it matters**, not before.

---

## Part 4 — THE core idea: every rule has one home

This is the skill they're really testing. Bad code spreads one rule across many places, so a small change becomes a hunt. Good code puts each rule in one obvious spot.

> **Every game rule lives in exactly one place — and you can name that place before you even look.**

**The homes (memorize this table):**

| Kind of rule | Home | Form |
|---|---|---|
| Which card beats which | `Ranks.Order` | one string array — position = strength |
| Suit strength (only if a rule creates it) | `Suits` | add a matching array + `Strength()` |
| What one card scores | `PointsOf(Card)` | one method: switch + modifiers |
| How a hand scores | `ScoreHand(player)` | one method (usually `Sum(PointsOf)`) |
| Who wins | `Winners()` | one method that **returns a List** — ties are real |
| What's in the deck | `Deck` constructor | parameters, never subclasses |
| Turn/round flow | one `Play()` loop | with a named end condition |
| Can this card be played | `IsPlayable(card, top)` | one true/false method |

**Why this works:** when the interviewer says "J/Q/K are worth 10 now," you don't hunt through five files. You say "that's points → `PointsOf`," edit one line, rerun, and say "still green." That contrast **is** the exam.

**The deeper reason (from the two recommended books):**
- *Programming Pearls* Column 3: **replace repetitive code with data.** `Ranks.Order` is one array giving you ordering + display + one-line changes. Whenever you're about to write a chain of `if (rank == ...)`, ask: *is this a table?* Rank order, suit order, point values, category ladders — all tables.
- *Cracking the Coding Interview* Chapter 7.1 is literally "design a deck of cards." Its method: handle ambiguity (ask questions) → define core objects (`Card`, `Deck`, `Player`, `Game`) → analyze relationships (has-a vs is-a) → investigate actions (verbs become methods). The book puts card value inside a `BlackjackCard` subclass; **you** put it in `Game.PointsOf` instead, because *"the card is a fact; what it's worth is a game rule, so the rule lives in the game."* Be ready to say that sentence.

---

## Part 5 — How to start coding (the first 10 minutes, exactly)

This exact sequence is your cold-start drill. After a week it should take **8–10 minutes** from a blank file. Say one sentence out loud as you begin each piece.

1. **Usings:** `using System;` / `using System.Collections.Generic;` / `using System.Linq;`
2. **`Ranks`** — the `Order` array + `Strength()`. *Say: "rank order as data, so ordering changes are one-line edits."*
3. **`Suits`** — the 4-entry array. *Say: "unordered per the doc, so no strength here — yet."*
4. **`Card`** — two properties, `IsJoker`, `Strength`, `ToString` (joker special case).
5. **`Deck`** — constructor that builds **from `Ranks.Order`**, Fisher–Yates `Shuffle`, `Draw()` that throws when empty, `Draw(n)`.
6. **`Check` helper** (3 lines) + first checks: deck is 52, `QD` displays, ace is low.
7. **Run it.** All green. *Say: "Foundation verified — ready for the game part."*

**This is the actual skeleton you're typing** (from `csharp/Skeleton/Program.cs`) — study it until it's automatic:

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public static class Ranks
{
    // LOW -> HIGH. Ace is LOW per the intro doc. JOKER sits above K.
    public static readonly string[] Order =
        { "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "JOKER" };

    public static int Strength(string rank) => Array.IndexOf(Order, rank);
}

public static class Suits
{
    public static readonly string[] All = { "C", "D", "H", "S" }; // no Strength yet
}

public sealed class Card
{
    public string Rank { get; }
    public string Suit { get; }                       // null for jokers

    public Card(string rank, string suit) { Rank = rank; Suit = suit; }

    public bool IsJoker => Rank == "JOKER";
    public int Strength => Ranks.Strength(Rank);
    public override string ToString() => IsJoker ? "JOKER" : Rank + Suit;
}

public class Deck
{
    private readonly List<Card> _cards = new List<Card>();
    private readonly Random _rng;

    public Deck(bool includeJokers = false, int? seed = null)
    {
        _rng = seed.HasValue ? new Random(seed.Value) : new Random();

        foreach (var suit in Suits.All)          // built FROM Ranks.Order = one source of truth
            foreach (var rank in Ranks.Order)
                if (rank != "JOKER")
                    _cards.Add(new Card(rank, suit));

        if (includeJokers)
        {
            _cards.Add(new Card("JOKER", null));
            _cards.Add(new Card("JOKER", null));  // the PDF pictures exactly 2
        }
    }

    public int Count => _cards.Count;

    public void Shuffle()
    {
        for (int i = _cards.Count - 1; i > 0; i--)      // Fisher–Yates: O(n), uniform
        {
            int j = _rng.Next(i + 1);
            (_cards[i], _cards[j]) = (_cards[j], _cards[i]);
        }
    }

    public Card Draw()
    {
        if (_cards.Count == 0)
            throw new InvalidOperationException("Cannot draw from an empty deck.");
        var top = _cards[_cards.Count - 1];             // draw from the END: O(1)
        _cards.RemoveAt(_cards.Count - 1);
        return top;
    }

    public List<Card> Draw(int n) => Enumerable.Range(0, n).Select(_ => Draw()).ToList();
}

public class Player
{
    public string Name { get; }
    public List<Card> Hand { get; } = new List<Card>();
    public Player(string name) { Name = name; }
    public string ShowHand() => string.Join(" ", Hand);
}

public class Game
{
    public List<Player> Players { get; }
    public Deck Deck { get; }

    public Game(IEnumerable<string> names, bool includeJokers = false, int? seed = null)
    {
        Players = names.Select(n => new Player(n)).ToList();
        Deck = new Deck(includeJokers, seed);
        Deck.Shuffle();
    }

    public void Deal(int cardsEach)
    {
        for (int round = 0; round < cardsEach; round++)   // round-robin
            foreach (var p in Players)
                p.Hand.Add(Deck.Draw());
    }

    // ---- policy methods: rule changes land HERE, nowhere else ----
    // Strength = who outranks whom; PointsOf = what a card scores. Different homes.
    public virtual int PointsOf(Card card) => card.Strength + 1;   // A=1 ... K=13, JOKER=14
    public virtual int ScoreHand(Player p) => p.Hand.Sum(PointsOf);

    public List<Player> Winners()
    {
        int best = Players.Max(ScoreHand);
        return Players.Where(p => ScoreHand(p) == best).ToList();   // ties stay visible
    }
}

public static class Program
{
    private static int _failures = 0;

    private static void Check(bool ok, string label)     // 3-line test harness
    {
        Console.WriteLine((ok ? "PASS  " : "FAIL  ") + label);
        if (!ok) _failures++;
    }

    public static void Main()
    {
        Check(new Deck().Count == 52, "standard deck has 52 cards");
        Check(new Deck(includeJokers: true).Count == 54, "joker deck has 54 cards");
        Check(new Card("Q", "D").ToString() == "QD", "card displays rank + suit");
        Check(new Card("JOKER", null).ToString() == "JOKER", "joker displays without suit");
        Check(Ranks.Strength("A") < Ranks.Strength("2"), "ace is LOW");
        Check(Ranks.Strength("JOKER") > Ranks.Strength("K"), "joker outranks king");

        var deck = new Deck(seed: 42);
        deck.Shuffle();
        var five = deck.Draw(5);
        Check(five.Count == 5 && deck.Count == 47, "drawing 5 leaves 47");

        var game = new Game(new[] { "Alice", "Bob", "Cara" }, seed: 42);
        game.Deal(5);
        foreach (var p in game.Players)
            Console.WriteLine($"{p.Name,-6} score {game.ScoreHand(p),3}   {p.ShowHand()}");
        Console.WriteLine("Winner(s): " + string.Join(", ", game.Winners().Select(w => w.Name)));

        Console.WriteLine(_failures == 0 ? "ALL CHECKS PASSED" : _failures + " CHECK(S) FAILED");
    }
}
```

**Testing is the cheapest points in the exam.** That 3-line `Check` helper gives visible PASS/FAIL proof on every run — start it around minute 5. Seed the RNG (`new Random(42)`) while debugging so runs repeat; say you'd unseed for real play. Test edges on purpose: empty deck throws, joker displays with no suit, a tie returns two winners.

---

## Part 6 — The game shapes (so no prompt feels new)

Don't memorize game names. Learn the **6 shapes**. When you read a prompt, ignore the name and ask "which shape is this?" — then build the methods for that shape. This should take under 30 seconds.

| Shape | In one line | Methods you'll need | Practice mock |
|---|---|---|---|
| **High Score** | deal, add up points, highest wins | `PointsOf`, `ScoreHand`, `Winners` | mock1 |
| **Battle / War** | flip a card each round, stronger wins the round | `CompareCards`, `PlayRound`, `Winner` | mock2 |
| **Best Hand** | classify the hand (pair, three of a kind) | `ClassifyHand`, `CompareResults`, `Winners` | mock3 |
| **Blackjack Lite** | get close to a target without going over | `BestTotal`, `IsBust`, `ShouldHitDealer`, `Winner` | mock4 |
| **Crazy Eights Lite** | play a card matching rank or suit, else draw | `IsPlayable`, `TakeTurn`, `AdvanceTurn` | mock5 |
| **Trick Taking** | each plays one card, best card wins the trick | `LegalCards`, `WinnerOfTrick`, leader update | mock6 |

**The key techniques per shape:**
- **High Score:** just `hand.Sum(PointsOf)`. Stresses the rank-vs-points split and ties.
- **War:** watch your piles (draw pile vs won pile); the comparator + round loop. A `Queue<T>` models a pile naturally.
- **Best Hand:** `hand.GroupBy(c => c.Rank)` then look at group sizes. Keep category strength as **data** (an ordered list), so adding "Two Pair" later renumbers one line.
- **Blackjack:** the flexible ace (1 or 11) → write `BestTotal(hand)` as one method (count aces, add 10 if it still fits).
- **Crazy Eights:** `IsPlayable(card, top)` = matches rank or suit; rotate turns with index math in **one** place. **Trap:** never remove from a `List` you're `foreach`-ing — find the card, remove after the loop.
- **Trick Taking:** this is where "must follow suit" legality and suit/trump comparison live.

**Why drilling these covers everything — every game is the same 5 decisions:**
1. **Setup** → `Deck` constructor + `Deal`
2. **Turn structure** (all at once / rotating / none) → the one play loop
3. **Legality** (what may a player do) → `IsPlayable`
4. **Resolution** (who takes the trick/cards/points) → comparator or classifier
5. **End + winner** → loop condition + `Winners`

---

## Part 7 — Handling rule changes: the R5 ritual

Part 3 is a stream of rule changes. For **every single one**, run this 30-second routine out loud. It's practiced in every mock and it's the strongest signal you can send.

1. **Restate** — "New rule: diamonds count double. So a 5♦ is 10 points now."
2. **Route** — "That's card scoring → `PointsOf`, nothing else knows about points."
3. **Red** — update the matching `Check` first, run it, watch it **FAIL**. ("The check now expects 10 — failing, good.")
4. **Rewrite** — make the one-line edit.
5. **Rerun + report** — "All green again, and the demo shows doubled diamonds."

**The change-routing table — drill this until you can answer from memory** (cover the right columns, read the left aloud):

| The interviewer says | Home | Typical edit |
|---|---|---|
| "Aces are high now" | `Ranks.Order` | move `"A"` to just before `"JOKER"` |
| "Joker beats everything" | `Ranks.Order` | it's already last = strongest; done |
| "J, Q, K are each worth 10" | `PointsOf` | merge the three cases into one |
| "Diamonds count double" | `PointsOf` | one line: `if (card.Suit == "D") points *= 2;` |
| "Jokers are worth 20" | `PointsOf` | early return at the top |
| "Lowest score wins" | `Winners` | change `Max` → `Min` |
| "Suits break ties: C < D < H < S" | new `Suits.Strength` + the one compare spot | add array + one extra compare level |
| "Two decks / no jokers / remove all 2s" | `Deck` constructor | loop count / flag / skip condition |
| "Deal 7 cards / 5 players" | the `Main` call site | just change arguments — if this needs surgery, your design failed |
| "On a tie, tied players draw one extra card" | winner resolution | loop around the winner logic |
| "Empty draw pile → reshuffle discards" | `Deck` + a discard list | add a `Reshuffle(cards)` method |
| "Play to 50 points instead of 10 rounds" | the play loop | change the while condition |
| "8s are wild / jokers are wild" | `IsPlayable` / classification | branch at the top |
| "Show hands sorted by rank" | display code only | `OrderBy(c => c.Strength)` **at the print spot** — don't change the hand |

That last row is a classic trap: **display rules change what you show, not the underlying data.**

**The "Pearls move" for a change that feels huge:** re-ask *what the rule is actually about*. Example — "jokers are wild" in Best Hand feels like it touches all your detection code. But a joker just *changes what the hand's rank groups look like*. So transform the hand first (the joker joins your most frequent rank), then run the **unchanged** detection. One preprocessing step, zero changes to logic that already worked.

---

## Part 8 — The rule of two (don't over-build)

Under time pressure, **do not** build abstractions for changes that haven't happened yet.

- **First version of a behavior** → just edit the method in place.
- **Second version needed at the same time** ("support both old and new scoring") → *now* extract it: a delegate parameter or a small subclass. Say it aloud: *"Two scoring rules need to coexist now, so I'm lifting `PointsOf` into a strategy — one line to swap them."*

Saying *when you would* abstract is worth as much as doing it — it earns the "recognize areas for improvement" credit for free.

**Both extremes lose:**
- **Over-engineering** (kills your clock): interfaces in the first 20 minutes, enums with parsing ceremony before any rule needs them, name-dropping patterns, building suit ordering/tie-breaks/discard piles *before they're asked*.
- **Under-engineering** (wrecks Part 3): rank values hard-coded everywhere, `if (rank=="J"||rank=="Q"...)` copied into three methods, winner logic that assumes one winner, a second separate list of rank names, loose magic strings instead of the `Ranks`/`Suits` constants.

**Why strings for ranks instead of an enum?** Deliberate choice — defend it if asked: the `Order` array already gives ordering + display + one-line changes; an enum adds `ToString` mapping for `"10"`/`JOKER` and parse ceremony — cost with no benefit at this size. (An enum is fine too; what's graded is that you chose *on purpose*.)

---

## Part 9 — The OOP & C# words to say out loud

You write C# daily, so this isn't "learn C#" — it's "name what you already do," because the interview grades *consistent application of principles*, and naming the principle while applying it is how they see it.

**The four OOP pillars, card edition:**
- **Encapsulation** — `Deck._cards` is private; only `Shuffle`/`Draw` touch it. *"The deck owns its cards — outside code can't corrupt it."*
- **Abstraction** — `Main` calls `Deal`/`Winners` and has no idea Fisher–Yates exists. *"The game exposes what it does, not how."*
- **Inheritance** — `PointsOf` is `virtual`; a variant game overrides it. *"I inherit to change one behavior, not to reuse fields."*
- **Polymorphism** — the same `ScoreHand` call does different things per game; a `Func<Card,int>` is polymorphism without a class. *"This call site never changes — only the rule behind it does."*

**Composition over inheritance:** `Game` **has a** `Deck`; `Player` **has a** hand. Has-a → field. Deck *contents* are data → a constructor flag (`includeJokers`), never a `JokerDeck` subclass. Keep inheritance one level deep in a timed exercise.

**SOLID, one line each** (use these when explaining "with more time I'd…"):
- **S** — `Deck` changes only when deck rules change. One reason to change per class.
- **O** — a second scoring variant is *added* (override/delegate), not edited into every call site. (That's the rule of two.)
- **L** — any game subclass keeps the contracts: `Winners` still returns all tied players, `Draw` still throws on empty.
- **I** — small public surfaces; `Deck` needs three members, not twelve "just in case."
- **D** — `ScoreHand` depends on the `PointsOf` abstraction, not inlined values. That indirection is exactly what makes changes one-line edits.

**Coupling & cohesion:** high cohesion = everything about "what a card is worth" sits in one method (the routing table is a cohesion map). Low coupling = printing knows nothing about points; scoring knows nothing about `Console`.

**Collections — which one, when:**
- `List<T>` — hands, decks (the workhorse). `RemoveAt(0)` is O(n) → draw from the END; never remove inside `foreach`.
- `Dictionary<K,V>` — point tables when a switch grows. `dict["missing"]` throws → use `TryGetValue`.
- `Queue<T>` — war piles (Dequeue the top, Enqueue winnings to the bottom).
- `Stack<T>` — a discard pile where only the top matters.
- Array — fixed rule data (`Ranks.Order`).

**The LINQ you'll actually use:** `Sum(PointsOf)` · `Max`/`Min` (lowest-wins = swap to `Min`) · `Where` · `Select` · `OrderBy`/`ThenBy` (for *display*) · `GroupBy` (pairs/trips in one call) · `Any`/`All` (flush = `All(c => c.Suit == first)`) · `Count(pred)` · `FirstOrDefault` (returns null — check it) · `ToList` (freeze before mutating) · `string.Join`. **Deferred execution:** a LINQ query is a recipe re-cooked each time you enumerate — `ToList()` freezes it; do that before mutating the source.

**Big-O in one sentence:** deck size is 52, nothing here is a performance problem, and saying so is the senior move. *"Everything is linear in deck size, and n is 52 — I'm optimizing for readability and changeability instead."*

**Errors:** fail loud at bad state (`throw new InvalidOperationException("Cannot draw from an empty deck.")`) — a clear crash beats a silent wrong answer. Don't wrap game logic in `try/catch` (you'd hide the bugs you need to see).

---

## Part 10 — Interview day: the minute-by-minute plan

**30 minutes before:**
- Quiet room, water, phone silenced and **out of reach**.
- Close everything except the HackerRank tab and **one** docs tab (learn.microsoft.com). An open LLM tab anywhere = fail even if unused.
- Test mic/camera/screen share. Have a 30-second intro ready (name, years, stack, one sentence on what you build). Don't linger there.
- Do **not** cram new material. You already know this.

**The 60-minute clock:**

| Time | What you're doing | What you're saying |
|---|---|---|
| 0:00–0:02 | Intro (30s), open Part 1, read it fully | "Let me read this completely first." |
| 0:02–0:04 | Restate Part 1 + ≤3 questions | "So: card with rank and suit, 52-card deck, shuffle and deal — and per the doc, ace is low, right?" |
| 0:04–0:16 | **Muscle memory:** Ranks → Suits → Card → Deck → Check → run | one sentence per class as you start it |
| 0:16–0:18 | Part 1 runs green; read Part 2, restate, ask scoring/tie questions | "Foundation verified. Reading part two…" |
| 0:18–0:36 | Game class: Deal → PointsOf → ScoreHand → Winners → demo + checks | "Point values live in one method — they tend to change." |
| 0:36–0:38 | Part 2 green; breathe; read Part 3 | |
| 0:38–0:55 | Rule changes one at a time, full **R5 ritual**, rerun after each | |
| 0:55–0:60 | Final run, quick cleanup, closing line | "With more time I'd pull scoring into a strategy and add proper unit tests." |

Running ~5 minutes behind is normal.

**Ask questions well:**
- Read the whole part first, then restate it in one sentence — *they grade the restatement.*
- Max ~3 questions per part, ~90 seconds. Ask each question **when its part arrives** (scoring questions during Part 1 waste your own clock).
- If they say "up to you": pick the simplest option, say it, and write it as a comment — `// assume: tied players share the win`. They grade the *explicitness*, not the choice.

**Safe defaults when they say "your choice":**

| Question | Default | Why it's safe |
|---|---|---|
| Jokers? | Exclude; constructor flag | Matches "52 cards"; flag makes adding them later trivial |
| Joker count | 2 | The PDF pictures 2 |
| Ace | LOW | The doc says so |
| Display | Letters `QD` | Fast to type; symbols are cosmetic |
| Deal style | Round-robin | Real-dealer behavior; same odds after shuffle |
| Ties | All tied players win (return a list) | Simplest correct; upgrades cleanly |
| Empty deck | Throw a clear error | Fail loud beats corrupt state |
| Leftover cards | Stay in the deck | No rule uses them |

**When stuck (this is graded — don't hide it):**
- "I don't remember the exact signature — checking the docs quickly." *(then actually search, under 90s)*
- "Let me print the state each round to see where it goes wrong."
- "I'll seed the shuffle so this run is repeatable while I debug."

**If you fall behind (10+ min):** say it, don't hide it. "I'm behind — I'll simplify the tie-break to a shared win and leave a TODO, so we reach the last requirement." Stub with a comment but keep the program **running** — a running program with a named shortcut beats a broken elegant half-feature. Never rewrite from scratch mid-exam. If a compile error resists 2 minutes: comment it out, get green, re-approach.

---

## Part 11 — C# traps for exactly this exam

1. **One `Random` instance** as a field. `new Random()` inside a loop → identical time-based seeds → identical "shuffles."
2. **Only `int.Parse(card.Rank)` in the `default:` branch** — after A/J/Q/K/JOKER are handled. `"JOKER"` throws at runtime, not compile time.
3. **Never remove from a `List` inside `foreach`** (`InvalidOperationException`). Shedding games hit this: find the card, remove after the loop, or iterate a copy (`.ToList()`).
4. **`using System.Linq;`** — forgetting it makes `Sum`/`Where`/`GroupBy` "not exist." Recognize that error instantly.
5. **`OrderByDescending(...).First()` on an empty sequence throws** — guard it, or use `FirstOrDefault` knowing it can be null.
6. **Integer division** when splitting piles (52/3 = 17).
7. **Suit symbols (♥) may print as `??`** — letters `C D H S` sidestep it; for symbols locally: `Console.OutputEncoding = System.Text.Encoding.UTF8;`.
8. **Tuple swap `(a, b) = (b, a)`** is the cleanest Fisher–Yates swap.

**Two error messages to recognize on sight:**
- *"'List<Card>' does not contain a definition for 'Sum'"* → you forgot `using System.Linq;`
- *"Collection was modified; enumeration operation may not execute"* → you removed from a list inside `foreach`.

**HackerRank environment:** one file, classic `static void Main`. Extra classes go in the same file — use `// ===== banner comments =====` as your "files." No debugger — your debugger is `Console.WriteLine` + the `Check` helper + seeded RNG. Run every 2–3 minutes; the run button is your compile check. Read the **first** compile error (later ones are usually cascade noise).

---

## Part 12 — A full worked example (route → edit → verify)

Starting rule: A=1, J=11, Q=12, K=13.

```csharp
public int PointsOf(Card card)
{
    if (card.Rank == "A") return 1;
    if (card.Rank == "J") return 11;
    if (card.Rank == "Q") return 12;
    if (card.Rank == "K") return 13;
    return int.Parse(card.Rank);
}
```

Interviewer: **"J, Q, K are now worth 10."**

1. **Restate:** "`QD` used to score 12, now it must score 10."
2. **Route:** "This is points — not ordering, not deck construction → `PointsOf`."
3. **Red:** update the check to expect 10, run, watch it fail.
4. **Rewrite:** one line —
   ```csharp
   if (card.Rank == "J" || card.Rank == "Q" || card.Rank == "K") return 10;
   ```
5. **Rerun:** `PointsOf(new Card("Q","D")) == 10` → green.

If you had to touch printing, dealing, or winner logic for this, the rule had leaked into the wrong place.

**And with real hands** (Mock 1 style):
```
Alice: AH 10D    Bob: KS 2C
With K=13:  Alice = 1+10 = 11,  Bob = 13+2 = 15  → Bob wins.
After "J/Q/K = 10":  Bob = 10+2 = 12  → Bob still wins, but ONLY PointsOf changed.
```
Same hand, different rule, one method touched. That's the whole point.

---

## Part 13 — How to practice (the 7-day plan)

Practice is three things, not one: (1) type the skeleton until it's automatic, (2) explain out loud where each rule lives, (3) run mocks where rules change. **Speak your narration out loud, in English, every time** — the talking is graded as much as the code.

**The drills:**
- **A — Cold start (core):** blank file → Ranks, Suits, Card, Deck, Check, 4+ checks, running green. No peeking. Target: Day 2 ≤12 min · Day 5 ≤10 min · Day 7 ≤8 min.
- **B — Mock exam:** one mock, 60 minutes, strict, then self-grade immediately.
- **C — Variant storm:** open your finished mock code, fire 6–8 rule changes one at a time (~5 min each), full R5 every time. Best reflex-builder there is.
- **D — Routing quiz (10 min daily warm-up):** no code. Hear a rule change, answer aloud which method changes and the edit. The routing table is the answer key.
- **E — Doc sprint:** 5 lookups on learn.microsoft.com, each under 90 seconds (`List<T>.RemoveAt`, `Enumerable.GroupBy`, `Random.Next(int)`, `string.Join`, `Enumerable.OrderBy`).

**The week:**

| Day | Do |
|---|---|
| **1** | Read this guide + `01`–`03`. Run the skeleton (`dotnet run`). Retype it once with the reference open. |
| **2** | Drill D · Drill A ×2 (≤12 min) · read `04` Tier A · read `07`. |
| **3** | **Mock 1** · grade yourself · compare with `Mock1Solution` + its `NOTES.md`: did your changes land in the same *places*? |
| **4** | Drill D · Drill C on your Mock 1 code · Drill E · read book notes `08` + `09`. |
| **5** | Drill A ×1 (≤10 min) · **Mock 2** (war — loops + policy replacement) · grade. |
| **6** | Drill D · **Mock 3** (classification + wildcards, the hardest) · grade · skim Tier B/C. |
| **7** | Drill A ×1 (≤8 min, boring) · reread the interview-day plan only · prep the room · stop early. Sleep is a performance drug. |

**Self-grade after every mock** (1–4 each, be honest): Understanding · Think-aloud · Clean code · Velocity · Testing & unblocking.

**"Ready" = two mocks in a row scoring ≥17/20, no axis below 3, and cold start ≤10 minutes.** Achievable by Day 6.

---

## Part 14 — The one-screen cheat sheet

**Rhythm every part:** restate → ask (≤3) → route → code → check → rerun.

**Rhythm every rule change (R5):** Restate → Route → Red (check fails) → Rewrite (one line) → Rerun.

**Rule homes:** strength=`Ranks.Order` · card points=`PointsOf` · hand score=`ScoreHand` · winner=`Winners` (returns a List) · deck contents=`Deck` constructor · legality=`IsPlayable` · turn=`AdvanceTurn`.

**Never forget:** ace is LOW · joker has no suit · suits unordered until asked · Winners returns a **list** (ties are real) · rank ≠ points · display rules don't change state · one `Random` field · don't remove inside `foreach` · run every 2–3 minutes · narrate before typing · no LLM ever, docs are fine.

**When lost:** ignore mutations → make ONE example work → print state after each step → put every rule in a named method → only then handle the next change.

**The whole exam in one line:** *put each rule in one place, name that place out loud before you touch it, edit one line, rerun, say "still green."*

---

# Appendices — the full detail (nothing lost)

The main guide above is the readable trunk. These appendices reproduce the exact lists, tables, and worked mind maps from the individual lessons, so this one file is complete on its own.

## Appendix A — The full clarifying-question bank (word for word)

Say these out loud, in these words. ★ = if you only have time for five questions across the whole interview, ask these five.

**Deck & setup (ask during Part 1 — keep to ~60 seconds)**
- ★ "Jokers in the deck for this part, or standard 52?" (their PDF's 13-vs-14 contradiction makes this legitimate)
- ★ "Is letter display okay — `QD`, `10H`, `JOKER` — or do you want the symbols?"
- "One deck, right?" (only if anything hints otherwise)

**Ordering (Part 1 or first time you compare cards)**
- ★ "Confirming from the intro doc: ace is LOW for this game?"
- "Joker outranks king, per the doc?"

**Scoring (ask when Part 2 arrives — not earlier)**
- ★ "Point values: A=1? J, Q, K = 11/12/13 or all 10? Joker?"
- "Highest total wins, correct?"

**Ties (Part 2)**
- ★ "If two players tie for best, do they share the win, or is there a tie-break?"

**Flow (Part 2, only if a loop exists)**
- "Fixed number of rounds, or play until the deck/piles are empty?"
- "If the draw pile empties mid-game: reshuffle discards, or stop?"

**Output**
- "Any exact output format you want, or is a readable summary fine?"

## Appendix B — Tier C games (one-line shapes so nothing feels alien)

You won't drill these, but reading them once means no prompt on the day is completely new.

| Game | Loop shape in one line | The twist it adds |
|---|---|---|
| Go Fish | ask an opponent for a rank → take it or "go fish" (draw); 4 of a rank = a "book" | querying a hand by rank (`GroupBy` again) |
| Memory / Concentration | grid of face-down cards; flip 2; equal ranks = keep them | position-based state, not hands |
| Snap | flip in turn onto a pile; equal rank to the previous card → first to call takes the pile | watching for a condition on consecutive cards |
| Baccarat-ish | sum the hand **mod 10**, closest to 9 wins | modular scoring in `ScoreHand` |
| Rummy-lite | collect melds: sets (same rank ×3) or runs (consecutive strength, same suit) | run detection = sort by `Strength`, check for gaps |
| President / Scum | play cards ≥ the previous play; otherwise pass | a legality check again |
| Elevens (solitaire) | remove pairs that add up to 11 | pair search over points |
| Most-of-a-suit | deal, count your longest suit | `GroupBy(Suit).Max(g => g.Count())` |

Also worth knowing the **known mutations** for the Tier A/B games you *will* drill:
- **High Score:** face-card values change · a suit doubles/negates · jokers enter with fixed points · lowest-wins · tie → extra card each · "best 3 of the 5 cards count."
- **War:** ace flips high · tie triggers "war" (1 down + 1 up, recursive) · suits start breaking ties (**replacing** the war rule) · play until piles empty · jokers beat all · two jokers collide (no suit → discard).
- **Best Hand:** insert Two Pair · Flush beats everything (`GroupBy(Suit)`) · jokers wild · kicker comparison · straights (ace-low).
- **Blackjack:** dealer hits soft 17 · 5-card charlie wins · jokers = 0 or blackjack wildcard · target changes to 24.
- **Crazy Eights:** 8s wild (choose suit) · jokers skip next · 2s force draw-two · reverse direction.
- **Trick-taking:** trump suit changes each round · jokers are highest trumps · scoring per trick count.

## Appendix C — The full self-grading rubric (score 1–4 after every mock)

| Axis | 4 | 3 | 2 | 1 |
|---|---|---|---|---|
| **Understanding** | Restated every part in own words; questions changed what you built; assumptions typed as comments | Restated; asked decent questions | Started coding from a half-read spec; backtracked once | Built the wrong thing for >5 min |
| **Think-aloud** | Intent narrated *before* typing, trade-offs named | Mostly narrated; some silent stretches | Silent >2 min repeatedly; narration is after-the-fact | Silence, or narrating literally every keystroke |
| **Clean code** | Every rule has one home; you could answer routing questions about your own file instantly | Minor duplication; one rule leaked into two places | Point values hard-coded at call sites; winner assumes no ties | Spaghetti; a mutation required touching 4+ spots |
| **Velocity** | All parts + a bonus mutation, runnable throughout | All three parts done, some polish skipped | Part 3 half-done | Stuck in Part 2 |
| **Testing & unblocking** | Check helper by min 5; red→green on every mutation; doc lookup <90s when stuck | Checks exist; reran often | First run after 20+ min; debugging by staring | Never verified; flailed when stuck |

**Ready for the real thing** = two consecutive mocks scoring ≥17/20 with no axis below 3, and cold start ≤10 minutes. Achievable by Day 6.

## Appendix D — The per-mock mind maps (play each game in your head)

For each: a mental movie, the state it needs, the code homes, a worked example, and where mutations route.

### Mock 1 — High Score
```
Movie: Shuffle. Deal 5 to Alice, Bob, Cara. Sum each hand. Highest total wins.
State:  Player { Name, Hand: List<Card> }
Homes:  Deal(cardsEach) · PointsOf(card) · ScoreHand(player)=Sum(PointsOf) · Winners()=max, return all tied
Example: Alice AH 10D, Bob KS 2C. If K=13: Alice=11, Bob=15 → Bob.
         If J/Q/K become 10: Bob=12 → still Bob, but only PointsOf changed.
```

### Mock 2 — Battle / War
```
Movie: Split deck into two draw piles. Each round both flip top card, stronger rank takes both
       into won pile. Repeat 10 rounds. Most won cards wins.
State:  BattlePlayer { Name, DrawPile, WonPile } ; Game { DiscardPile for tied rounds }
Homes:  CompareCards(a,b) · PlayRound() · PlayGame() · Winner()=compare won-pile counts
Example: Alice flips 9H, Bob flips QD. Q strength > 9 → Bob.WonPile gets 9H and QD.
Routes:  Aces high → Ranks.Order · War on tie → tie branch in Compare/PlayRound
         Suit breaks tie → CompareCards · Jokers → Ranks.Order + joker edge case
```

### Mock 3 — Best Hand
```
Movie: Deal 5 each. Group cards by rank. Group of 3 = Three of a Kind, group of 2 = One Pair,
       else High Card. Compare category first, then defining rank.
State:  HandResult { CategoryName, CategoryStrength, DefiningRankStrength, optional kicker }
Homes:  ClassifyHand(hand)→HandResult · CompareResults(a,b)=category,rank,kicker · Winners()
Example: Alice 7H 7S 7D QC 2H → groups: 7→3, Q→1, 2→1 → Three of a Kind, defining rank 7.
Routes:  Two Pair → category ladder · Flush → ClassifyHand · Joker wild → preprocessing inside
         ClassifyHand · Kicker → HandResult gets another comparison field
```

### Mock 4 — Blackjack Lite
```
Movie: Deal 2 to player and dealer. Each draws toward a stand value. Aces = 1 or 11.
       Best total = highest total ≤ target. Over target = bust. Closest without busting wins.
State:  Player { Name, Hand } ; Game { Target=21, StandAt=17 }
Homes:  BasePoints(card) · BestTotal(hand)=ace logic · IsBust(hand)=BestTotal>Target
        · ShouldHitDealer()=dealer policy · Winner()=bust/charlie/total comparison
Example: Hand AH 6D. Ace as 1 → 7; ace as 11 → 17. Best total ≤ 21 is 17.
Routes:  Dealer hits soft 17 → ShouldHitDealer/IsSoftTotal · 5-card charlie → Winner
         Joker=0 → BasePoints · Target 24 → Target field, not a magic number
```

### Mock 5 — Crazy Eights Lite
```
Movie: There's a discard top card. Current player plays a card matching rank or suit, else draws
       (plays the drawn card if it matches, otherwise keeps it). Move to next player.
       First empty hand wins.
State:  Game { Players, Deck, DiscardPile, CurrentPlayerIndex, Direction,
                PendingSkip/PendingDraw, CurrentSuit if a wild 8 was played }
Homes:  IsPlayable(card, top)=rank/suit/wild · ChooseCard(player)=first legal
        · TakeTurn(player)=play or draw · AdvanceTurn()=index+direction
        · ApplyCardEffect(card)=skip, draw-two, reverse
Example: Top 9H. Alice hand 2C 5H QS 9D. 5H matches suit, 9D matches rank. First playable is 5H
         → Alice plays 5H, new top is 5H.
Routes:  8 wild → IsPlayable + CurrentSuit · Joker skip → IsPlayable + ApplyCardEffect
         2 draw-two → ApplyCardEffect · Queen reverse → AdvanceTurn/Direction
```

### Mock 6 — Trick Taking Lite
```
Movie: Leader plays a card; its suit is the led suit. Others must follow suit if they can.
       After everyone plays one card, pick the trick winner. Winner scores 1 and leads next.
State:  Player { Name, Hand, Score } ; Play { Player, Card } ;
        Game { LeaderIndex, TrickNumber, TrumpSuit optional }
Homes:  LegalCards(player, ledSuit)=follow-suit rule · ChooseCard(player, ledSuit)=lowest legal
        · WinnerOfTrick(plays)=led-suit/trump comparison · PlayTrick()=one complete trick
Example: Alice leads 7H (led suit H). Bob has 2H QS → must play 2H. Cara has no hearts → anything.
         Dan has KH 3C → must play KH. Without trump, highest heart wins → Dan (KH).
Routes:  Spades trump → WinnerOfTrick · Changing trump → TrumpSuitForTrick
         Aces high → Ranks.Order · Joker always legal → LegalCards + WinnerOfTrick
```

**Before typing any game, run this 5-question checklist:** (1) What are my objects? (almost always Card, Deck, Player, Game) (2) What state changes? (3) What is one full action? (one deal / round / turn / trick / classification) (4) Where does each rule live? (5) What tiny check proves this? Then type the smallest version that makes the movie run.

**If you feel lost — emergency simplification:** ignore mutations → make one example work → print state after each step → put every rule in a named method → only then handle the next mutation. Example: don't understand Crazy Eights yet? Test only this — Top = 9H, Hand = 2C 5H QS 9D, `IsPlayable` should return true for 5H and 9D only. Once that works, the bigger game becomes easy because the rule has a home.

## Appendix E — C# features in the skeleton (recognize each, and its say-line)

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

## Appendix F — Book takeaways in detail

**Cracking the Coding Interview (chapter/relevance):** Highest value is **Chapter 7 (Object-Oriented Design), question 7.1 = "Deck of Cards"** — essentially your Part 1 plus a variant. Also **High: Big O** (describe your own code confidently) and **Chapter 11 Testing** (normal case → extremes (empty/one/many) → illegal input → state-dependent cases; maps 1:1 to your `Check` lines). Medium: the process/behavioral intros (they grade the *path*, so a narrated wrong-turn-plus-recovery beats silent perfection). **Skip** this week: trees, graphs, DP, bit manipulation, linked lists. *If you only give it 2 hours:* Ch. 7 intro + 7.1 (~40 min), Ch. 11 testing (~20 min), Big O skim (~30 min), process intros skim (~30 min).

**Programming Pearls (column/relevance):** The headline is **Column 3 — Data Structures Programs: replace repetitive code with data.** Your `Ranks.Order` is the textbook example. Also ★: **Column 1** (define the problem before solving — your question bank), **Column 5** (scaffolding = your `Check` helper), **Column 12** (random permutation = Fisher–Yates `Shuffle`). The five habits to carry in: (1) restate before you code, (2) prefer data to logic — "I'd rather maintain an array than an if-chain," (3) keep scaffolding running, (4) **envelope-check the output** — glance at every demo: 52 − 3×5 = 37 left after the deal; a two-second mental estimate is the fastest test you own, (5) simplicity is a decision — narrate restraint. *If you own it:* read Columns 1, 3, 5, 12 (~1 hour).

## Appendix G — Using Claude as your training partner (before the day only)

During the **real interview, any LLM use = automatic fail.** Beforehand, useful prompts through the week:
- "Act as my FF card-game interviewer. Use `mocks/mock1.md`. 60 minutes, reveal parts on schedule, then grade me with the rubric."
- "Routing quiz: fire 10 rule changes at me one at a time; I'll answer where each lands before touching code."
- "Variant storm: I have my Mock 1 code open. Fire mutations at me one at a time, 5 minutes each."
- "Review my attempt against `csharp/Mock1Solution` and the rubric." (paste your code)
- "Show me the reference solution for mock 2 / 3 / 4 / 5 / 6." (after you attempt them)

**Quick start (today, ~60 min):**
```powershell
cd C:\Users\<you>\CardGameInterviewPrep\csharp\Skeleton
dotnet run
```
Then read `01`, `02`, `03`, and retype the skeleton yourself once with the reference open.
