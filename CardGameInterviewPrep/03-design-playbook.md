# 03 — The Design Playbook (the skill they're actually testing)

## Simple version

This file teaches the single most important habit: **every rule should live in one place.**

Bad code spreads the same rule across many spots. When you need to change it, you have to hunt everywhere — and a small change turns into a big headache.

Good code puts each rule in one obvious method or array:

- Rank strength lives in `Ranks.Order`.
- A card's score lives in `PointsOf(Card)`.
- A hand's score lives in `ScoreHand(Player)`.
- Winner logic lives in `Winners()` or `ResolveWinners()`.
- Whether a card can be played lives in `IsPlayable(...)` or `LegalCards(...)`.
- Moving to the next turn lives in one turn-update method.

Quick example:

Rule change: "J, Q, K are now worth 10."

That's not about the deck. It's not about display. It's about **scoring**. So you change `PointsOf(Card)` and nothing else.

That's the main skill this interview tests.

The interview is designed to punish one thing: **rules scattered all over the code.** When they say "J/Q/K are worth 10 now" and you have to search through five different places, you lose time and confidence. When the rule lives in one method, you edit one line, run it again, and say "still passing." That difference *is* the exam.

## The one design rule

> **Every game rule lives in exactly one place — and you can name that place before you even look.**

Here's where each rule lives, based on the skeleton (`csharp/Skeleton/Program.cs`):

| Kind of rule | Home | Form |
|---|---|---|
| Which card beats which | `Ranks.Order` | one string array — position = strength |
| Suit strength (only if a rule creates it) | `Suits` | add a matching array + `Strength()` |
| What one card scores | `PointsOf(Card)` | one method: switch + modifiers |
| How a hand scores | `ScoreHand(player)` | one method (usually `Sum(PointsOf)`) |
| Who wins | `Winners()` / `WinnersAmong(pool)` | one method that **returns a List** — ties are real |
| What's in the deck | `Deck` constructor | parameters, never subclasses |
| Turn/round flow | one `Play()` loop | while/for with a named end condition |
| Can this card be played (matching games) | `IsPlayable(card, top)` | one true/false method |

Notice: **ordering and points live in different homes.** `Strength` answers "which card wins," `PointsOf` answers "how much is it worth." Games change these two things independently, so the code keeps them separate too.

## The change-routing table — memorize this

Practice: cover the right two columns, read the left column aloud, and answer from memory (`06`, Drill D).

| The interviewer says | Home | Typical edit |
|---|---|---|
| "Aces are high now" | `Ranks.Order` | move `"A"` to just before `"JOKER"` |
| "Joker beats everything" | `Ranks.Order` | it's already last = strongest; done |
| "J, Q, K are each worth 10" | `PointsOf` | merge the three cases into one |
| "Diamonds count double" | `PointsOf` | one multiplier line (`if (card.Suit == "D") points *= 2;`) |
| "Jokers are worth 20" | `PointsOf` | early return at the top |
| "Lowest score wins" | `Winners` | change `Max` → `Min` |
| "Suits break ties: C < D < H < S" | new `Suits.Strength` + the one comparison spot | add array + one extra compare level |
| "Use two decks / no jokers / remove all 2s" | `Deck` constructor | loop count / flag / skip condition |
| "Deal 7 cards / 5 players" | the `Main` call site | just change the arguments — if this needs real surgery, your design already failed |
| "On a tie, tied players draw one extra card" | winner resolution | loop around `WinnersAmong` (see Mock 1, M4) |
| "Empty draw pile → reshuffle discards" | `Deck` + a discard list | add a `Reshuffle(cards)` method |
| "Play to 50 points instead of 10 rounds" | the play loop | change the while condition |
| "8s are wild / jokers are wild" | `IsPlayable` / the classification method | branch at the top |
| "Show hands sorted by rank" | display code only | `OrderBy(c => c.Strength)` **at the print spot** — don't change the actual hand unless asked |

That last row is a classic trap: display rules change what you **show**, not the underlying data.

## Live-refactor rule: the rule of two

Under time pressure, do **not** build fancy structures for changes that haven't happened yet.

- **First version of a behavior** → just edit the method in place.
- **Second version needed at the same time** (e.g. "support both the old and new scoring") → *now* pull it out: a delegate parameter, or a small subclass. Say it out loud: *"Two scoring rules need to work at once now, so I'm lifting `PointsOf` into a strategy — one line to swap them."*

Saying *when you would* create the abstraction is worth as much as actually doing it — it earns you their "recognize areas for improvement" credit for free.

## Overengineering vs underengineering — both lose

**Overengineering warning signs (wastes your time):**
- Interfaces (`ICardComparer`, `IScoringStrategy`) in the first 20 minutes
- Enums with parsing/display ceremony before any rule needs them
- Name-dropping design patterns with no change that calls for them
- Building suit ordering, tie-breaks, or discard piles **before anyone asks**

**Underengineering warning signs (wrecks Part 3):**
- Rank values hard-coded at every comparison spot
- `if (rank == "J" || rank == "Q" ...)` copied into three methods
- Winner logic that assumes exactly one winner (ties WILL happen)
- Building the deck from a second, separate list of rank names (keep one source of truth: build the deck **from** `Ranks.Order`)
- Loose "magic" strings inline instead of the `Ranks`/`Suits` constants

**Why use strings for ranks instead of an enum?** This is a deliberate choice — defend it out loud if asked: the `Order` array already gives you ordering + display + one-line changes. An enum would add `ToString` mapping for `"10"`/`JOKER` plus parsing ceremony — cost with no real benefit at this size. Typo risk is covered by the PASS/FAIL checks. (An enum is fine too; what's graded is that you chose on purpose.)

## The first 10 minutes, step by step

This exact sequence is the cold-start drill in `06`. After a week of practice it should take ≤8–10 minutes:

1. `using System;` / `using System.Collections.Generic;` / `using System.Linq;`
2. `Ranks` — the `Order` array + `Strength()` (say: *"rank order as data — ordering changes become one-line edits"*)
3. `Suits` — the 4-entry array (say: *"unordered per the doc, so no strength here — yet"*)
4. `Card` — two properties, `IsJoker`, `Strength`, `ToString` (with the joker special case)
5. `Deck` — constructor that builds **from `Ranks.Order`**, a Fisher–Yates `Shuffle`, `Draw()` that throws when empty, and `Draw(n)`
6. `Check` helper (3 lines) + first checks: deck is 52, `QD` displays right, ace is low
7. **Run it.** All green. Say: *"Foundation verified — ready for the game part."*

## Testing rules (the cheapest points in the exam)

```csharp
private static void Check(bool ok, string label)
{
    Console.WriteLine((ok ? "PASS  " : "FAIL  ") + label);
    if (!ok) _failures++;
}
```

- Three lines, no test framework, visible proof on every run. Start it around minute 5.
- **When a rule changes, update the check first**, watch it FAIL, fix the code, watch it PASS. That 30-second loop, narrated out loud, is the strongest "I test my code" signal you can send.
- Seed the random generator (`new Random(42)`) while debugging so each run is repeatable — and mention you'd remove the seed for a real game.
- Test the edge cases on purpose: empty deck throws, a joker displays with no suit, a tie returns two winners.

## Walk-through: route a change before writing any code

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

Change: "J, Q, K are now worth 10."

Walk-through:
1. Concrete example: `QD` used to score 12, now it must score 10.
2. Route it: this is **points** — not ordering, not deck building.
3. Edit one method:

```csharp
if (card.Rank == "J" || card.Rank == "Q" || card.Rank == "K") return 10;
```

4. Rerun the check: `PointsOf(new Card("Q", "D")) == 10`.

If you had to touch printing, dealing, or winner logic for this change, it means the rule had leaked into the wrong place.
