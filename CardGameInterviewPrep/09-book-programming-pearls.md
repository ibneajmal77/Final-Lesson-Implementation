# 09 — Book Notes: "Programming Pearls" (Jon Bentley)

Distilled notes oriented to the FF screen. *Programming Pearls* is a set of short essays ("columns") about thinking before coding — FF recommends it for exactly the skill their doc calls "thinking outside the box." Column numbers below follow the 2nd edition.

## Plain English version

You do not need the whole book for the interview. The useful idea is this:

Good code often starts with the right data shape.

In this kit, the best example is `Ranks.Order`. Instead of writing many comparison rules, you keep the order in one array. If aces become high, you move `"A"` in that one array.

Simple example:

Bad mental model: "I need many `if` statements for every rank."

Better mental model: "I need one ordered list of ranks, then I can ask where a rank appears in that list."

The interview benefit is speed. When a rule changes, you know what data or method to change.

## The headline connection

Your entire design playbook (`03`) is Bentley's **Column 3** applied to cards: *when code is full of repetitive logic, the fix is usually a better data representation, not more code.* `Ranks.Order` — one array giving ordering, display and mutation-in-one-line — is a textbook "data structures program." If you internalize one idea from this book, it's that one.

## Dry run: data beats repeated logic

Bad shape:

```csharp
if (rank == "A") return 1;
if (rank == "2") return 2;
if (rank == "3") return 3;
// many more branches
```

Better shape for ordering:

```csharp
public static readonly string[] Order =
    { "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K" };

public static int Strength(string rank) => Array.IndexOf(Order, rank);
```

Mutation: "aces are high."
- Bad shape: hunt through comparison code.
- Data shape: move `"A"` near the end of the array.

That is the Programming Pearls lesson in this kit: choose the representation that makes the next rule change small.

## Column relevance map

| Column | Theme | Relevance | Takeaway for the FF screen |
|---|---|---|---|
| 1 — Cracking the Oyster | Define the problem before solving it | **High** | The stated problem is often not the real one; a few questions up front save the build. Your `02` question bank is this column as a checklist |
| 2 — Aha! Algorithms | Insight via looking at the problem differently | Medium | When a mutation feels big, re-ask "what is this rule *about*?" — it usually names its own home |
| 3 — Data Structures Programs ★ | **Replace repetitive code with data** | **Highest** | Rules as arrays/tables; position = strength; one source of truth |
| 4 — Writing Correct Programs | Invariants, reasoning about loops | Medium | Fisher–Yates in one sentence: "everything from position i+1 up is already final" — being able to *say* why a loop is right |
| 5 — A Small Matter of Programming ★ | Scaffolding, assertions, testing small pieces | **High** | Your `Check` helper IS Bentley's scaffolding: tiny, visible, always running |
| 6 — Perspective on Performance | Layered performance thinking | Low | n = 52; know why you're *not* optimizing |
| 7 — The Back of the Envelope | Quick estimation | Medium | Sanity-check outputs in your head: 52 − 3×5 = 37 left after the deal — takes two seconds, catches real bugs |
| 8 — Algorithm Design Techniques | Divide & conquer, scanning | Low | Skip this week |
| 9 — Code Tuning / 10 — Squeezing Space | Micro-optimization | Low | The senior answer is knowing when NOT to |
| 11 — Sorting | Sorting wisdom | Low-med | Use the library sort with a key; never hand-roll one live |
| 12 — A Sample Problem ★ | Random sampling & permutations | **High** | The swap-based random permutation here is your `Deck.Shuffle` — Fisher–Yates, uniform over all orderings |
| 13 — Searching / 14 — Heaps / 15 — Strings of Pearls | Structures & strings | Low | Skip this week |

## The five Pearls habits to carry into the interview room

1. **Restate before you code** (Col 1). A minute spent restating Part 2 in your own words routinely saves ten minutes of building the wrong game. This is also FF's first grading axis, so the habit scores twice.
2. **Prefer data to logic** (Col 3). Every time you're about to write a chain of `if (rank == ...)`, ask: is this a table? Rank order, suit order, point values, category ladders (Mock 3) — all tables. Say-line: *"I'd rather maintain an array than an if-chain."*
3. **Keep scaffolding running** (Col 5). Small self-checks that print on every run — cheap, visible, and they catch the mutation you half-applied. Bentley's point: programmers who test tiny pieces early are faster *overall*, which is FF's velocity axis.
4. **Envelope-check the output** (Col 7). Glance at every demo run: deck counts add up? scores plausible for 5 cards? A two-second mental estimate is the fastest test you own.
5. **Simplicity is a decision** (the book's through-line). Shorter, plainer code has fewer places for bugs to live — in this interview, every abstraction you *don't* build in Part 1 is time you own in Part 3. Narrate restraint: *"I'm keeping this simple until a second variant forces the abstraction."*

## One worked example of "the Pearls move" in your interview

Mutation M3 in Mock 3: *"jokers are wild."* The panic version writes special cases through the detection code. The Pearls version re-asks what the rule is about (Col 2): a joker just *changes what the hand's rank groups look like*. So: transform the hand first (joker joins your most frequent rank), then run the **unchanged** detection. One preprocessing step, zero changes to the logic that already worked. When a change feels like it touches everything — look for the representation move that makes it touch one thing.

## How this book and your kit line up

| Pearls idea | Where it already lives in the kit |
|---|---|
| Problem definition (Col 1) | `02` question bank; the restate step in `05`'s R5 ritual |
| Data beats logic (Col 3) | `03` design playbook, the routing table |
| Scaffolding (Col 5) | The `Check` helper in the skeleton |
| Estimation (Col 7) | The "envelope-check the demo" habit above |
| Random permutation (Col 12) | `Deck.Shuffle`, seeded for reproducibility |

If you own the book: read Columns 1, 3, 5 and 12 (★) — roughly an hour total, all four pay off directly on the day.
