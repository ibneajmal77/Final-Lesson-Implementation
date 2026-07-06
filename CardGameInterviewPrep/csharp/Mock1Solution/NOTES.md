# Mock 1 — Evolution Notes

`Program.cs` shows the FINAL state. This file shows how it **grew**, step by step — because the skill being graded is *where changes land*, not the final code. Compare your attempt step by step against this.

## [P1] Part 1 (minutes ~2–15) — the muscle-memory zone

Typed: `Ranks`, `Suits`, `Card`, `Deck`, `Check` helper, first checks, run → green.

**Say:** *"Rank order is a data array — position is strength, so ordering changes are one-line edits. Deck builds from that same array: one source of truth."*

## [P2] Part 2 (minutes ~18–36) — the game

Added `HighScoreGame` with `Deal`, `PointsOf`, `ScoreHand`, `Winners`, `PrintStandings`.

At this stage `PointsOf` was:

```csharp
case "A": points = 1;  break;
case "J": points = 11; break;
case "Q": points = 12; break;
case "K": points = 13; break;
default:  points = int.Parse(card.Rank); break;
```

and `Winners()` was the plain version (no pool parameter):

```csharp
public List<Player> Winners()
{
    int best = Players.Max(ScoreHand);
    return Players.Where(p => ScoreHand(p) == best).ToList();
}
```

**Say:** *"Point values live in one method — in these exercises they always change. Winners returns a list, because ties are a real case."*

## [M1] "J, Q, K are each worth 10" → touched: `PointsOf` only

Three cases collapse into one fall-through. **First**: updated the check to expect `Q = 10`, ran it, watched it FAIL, then fixed, then PASS.

**Say:** *"That's the red-green loop on a rule change — the check is the requirement, so it changes first."*

## [M2] "Diamonds count double" → touched: `PointsOf` only

One line at the bottom: `if (card.Suit == "D") points *= 2;`

**Say:** *"Scoring now reads the suit for the first time — but still only one method knows about points."*

## [M3] "Jokers in, worth 20" → touched: `Deck` ctor flag (already existed) + `PointsOf` early return

`if (card.IsJoker) return 20;` at the top — before the suit check, which also answers "is a joker doubled if…?" — it can't be, it has no suit. Added checks: joker = 20, deck = 54.

**Say:** *"Early return for the special case; the joker never reaches the suit logic because it has no suit — matches the intro doc."*

## [M4] "Tie → one extra card each, repeat" → the only structural change of the day

`Winners()` alone can't express a retry loop over a shrinking pool. So:

1. Generalized `Winners()` → `WinnersAmong(List<Player> pool)` (same body, parameterized).
2. Added `ResolveWinners()`: loop while >1 contender and the deck can serve them; each pass deals one card to each contender and re-evaluates **among contenders only**.
3. Edge case stated as an assumption: deck runs out → remaining contenders share the win.

**Say:** *"I'm generalizing winners to take a pool so the tie-break can reuse it — this is the 'rule of two' moment: the second use of the logic is what justifies the refactor."*

## Plain English version

This file explains how Mock 1 changes over time.

Think of it like this:

1. First you build cards and a deck.
2. Then you deal cards and score hands.
3. Then each new rule changes one clear place.

The main lesson:

Do not rewrite the whole program when a rule changes. Find the correct rule home.

Examples:

- "Face cards are 10" changes `PointsOf`.
- "Diamonds double" also changes `PointsOf`.
- "Jokers exist" changes the `Deck` setup and `PointsOf`.
- "Ties draw extra cards" changes winner resolution.

If your code changes in many places for one small rule, the rule is spread out too much.

## Dry run: final Mock 1 scoring

Use this hand after all mutations:

- Alice: `QD 5D JOKER 2H 3C`

Final rules:
- J/Q/K are worth 10.
- Diamonds double.
- Joker is worth 20.

Step by step:
- `QD`: queen is 10, diamond doubles to 20.
- `5D`: 5 doubles to 10.
- `JOKER`: 20, no suit logic applies.
- `2H`: 2.
- `3C`: 3.

Alice total = 20 + 10 + 20 + 2 + 3 = 55.

Code homes:
- `Deck` explains why jokers exist.
- `PointsOf` explains every single-card value above.
- `ScoreHand` only sums `PointsOf`.
- `ResolveWinners` only handles ties after scores exist.

If your solution needs special joker or diamond code inside `ScoreHand`, the scoring rule leaked too far.

## Common mistakes this reference avoids — check your attempt for them

| Mistake | Cost |
|---|---|
| Rank values hard-coded in `ScoreHand` AND in printing AND in comparisons | M1 becomes a hunt across the file |
| A second list of rank names inside `Deck` | "Add jokers" now has two truths to update |
| `Winners` returning a single `Player` | M4 forces a signature change that ripples to every caller |
| `int.Parse(card.Rank)` before excluding JOKER/faces | Runtime crash the moment jokers enter (M3) |
| Skipping the failing-check step on mutations | Loses the cheapest "testing" points in the exam |
| Silent 2-minute refactor during M4 | The interviewer can't grade what you don't narrate |
