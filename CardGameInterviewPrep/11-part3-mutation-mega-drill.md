# 11 — Part 3 Mega-Drill: 100 Mutations, All Rule Homes

This is Drill D (`06-practice-plan.md`), scaled up. The core table in `03-design-playbook.md` has 14 routes — memorize that one first. This file is for the day before the interview: **volume practice**, so no phrasing surprises you tomorrow.

## How to use this (no code — this is a SPEAKING drill)

1. Cover Part B (the answer key) with your hand, a sheet of paper, or by not scrolling down.
2. Read ONE rule from Part A out loud.
3. Say, out loud, in one sentence: *"That's a `<kind of rule>`, so it lives in `<method/array>`."*
4. Only then check Part B. Right → move on. Wrong or hesitant → reread the matching row in `03-design-playbook.md`, say it again, move on.
5. Target pace: under 20 seconds per item. If a whole category feels shaky, that's your last-hour reading, not this whole file.

**Short on time? Do this instead:** categories 1–6 (scoring, ordering, suits, deck, winners, legality) are the highest-value 50. Do those, then jump straight to the **Advanced** section at the end — those are the ones that separate a strong candidate from an average one.

**Reading Part B:** the `Home` column is the one-sentence answer — the method or array the rule belongs to. The `Fix` column is the smallest edit that makes it true; where it's genuinely a one-liner, that's real C# lifted straight from your `Concepts` project's shapes. Where a row says "NEW —", that's a deliberate flag: it's not a one-liner, and knowing that *in advance* is the actual skill.

---

## PART A — THE RULES (say the answer before you look)

### 1. Scoring / points (→ `PointsOf` / `BasePoints`)
1. Number cards score double their face value.
2. Face cards (J/Q/K) are all worth 10.
3. Face cards keep 11/12/13, but Aces are worth 15.
4. Spades count double.
5. Any red card (hearts or diamonds) scores a +2 bonus.
6. Jokers are worth −5 (a penalty, not a bonus).
7. Every card's value is its rank strength, squared.
8. The 2 of clubs specifically is worth 50 (one named "trap card").
9. Cards 2 through 5 score zero — they're "dead cards."
10. In Blackjack, a joker is "wild": it counts as whatever value (0–11) gets the hand closest to 21 without busting.

### 2. Rank ordering (→ `Ranks.Order`, a data move)
11. Aces are high, for comparison purposes only.
12. The joker now ranks BELOW the ace — the weakest card in the deck.
13. Rank order is reversed entirely: King is lowest, 2 is highest.
14. Face cards outrank each other in reverse: K < Q < J.
15. Two specific ranks swap places: 5s now outrank Kings.
16. You're given a full custom order for this round: 7,8,9,10,J,Q,K,A,2,3,4,5,6.
17. Ties in rank are now broken by whichever card was DEALT first.
18. Number cards are all equal strength; only aces and face cards have real order.

### 3. Suit order / tie-break (→ `Suits.Strength` + one compare)
19. Suits break ties: clubs weakest, spades strongest.
20. Reverse that: spades weakest, clubs strongest.
21. Only diamonds are special: they beat a tie; every other suit stays equal to every other.
22. The suit tie-break only applies in the LAST round of the game.
23. A player may choose which suit is "trump" for tie-breaking before the round starts.
24. Suits break ties only between two cards of different color; same-color ties stay ties.

### 4. Deck composition (→ `Deck` constructor)
25. Use two decks shuffled together.
26. Remove one entire suit before playing.
27. Remove all face cards — number cards only.
28. Add FOUR jokers instead of two.
29. Play with a 40-card deck (strip 8s, 9s, and 10s).
30. One specific card is simply missing from the deck (someone "lost" the Ace of Spades).
31. Combine two decks, but include only ONE joker total, not two per deck.
32. The deck must automatically reshuffle its discard pile once it drops below 10 cards.
33. The deck must start in a fixed, known order for testing — not randomly shuffled.
34. Certain ranks are duplicated extra times (4 extra Aces added) — no longer a "standard" deck at all.

### 5. Winner / tie-resolution (→ `Winners()` / `ResolveWinners()` / a pool-based helper)
35. Ties are no longer shared: each tied player draws one card, repeat until one winner (you already built this one).
36. Ties are broken by whoever holds the single highest card in hand — no redraw.
37. On a tie, replay the ENTIRE hand from scratch, but only for the tied players.
38. Second place also earns a small consolation point — winner logic now has tiers, not just first place.
39. A tie for LAST place eliminates that player.
40. The winner is whoever is closest to a target number without going over — not whoever has the highest raw score.
41. On a tie, whoever has MORE cards in hand automatically wins — no redraw needed.
42. A win must be by a margin of at least 5 points, or it's declared a draw for everyone.

### 6. Legality / playability (→ `IsPlayable` / `LegalCards`)
43. 8s are wild and playable on anything.
44. You may play any card of the same COLOR as the top card (red/black), not the same suit.
45. You may play any card numerically ADJACENT to the top card's rank, regardless of suit.
46. Face cards are always playable, no matter what.
47. You may never play the same exact rank twice in a row across your own turns.
48. On the very first turn, any card is legal (there's no top card yet).
49. A player who cannot play must draw THREE cards, not one.
50. Two matching-rank cards may be played together in a single turn if you hold both.

### 7. Turn order / direction (→ `AdvanceTurn` / the turn loop)
51. A Queen reverses direction.
52. Playing a specific rank makes the SAME player go again.
53. A Jack skips the next TWO players, not one.
54. Turn order each round is decided by a drawn card (highest goes first), not fixed rotation.
55. The round/trick winner leads next.
56. Direction reverses automatically every 3 rounds, with no card triggering it.

### 8. Classification / category ladder — Best Hand (→ `BestHand.Classify` + the `Ladder` array)
57. Add Two Pair, between One Pair and Three of a Kind.
58. Add Flush — all 5 cards the same suit — beats everything.
59. Add Full House — a pair plus a three-of-a-kind together.
60. Add Four of a Kind.
61. Add a Straight — 5 consecutive strengths, any suits.
62. Add a Straight Flush — a Straight that's also a Flush.
63. Same category, same defining rank, same kicker too → confirm it's a true shared tie.
64. The exact hand `2, 7, Q, J, K` of mixed suits is a special named hand that auto-wins regardless of everything else.

### 9. Trump / suit power — Trick Taking (→ `WinnerOfTrick`'s tier function)
65. Spades are trump.
66. Trump rotates every trick: C, D, H, S, repeat.
67. This particular trick has NO trump, even though one is set for the game.
68. TWO suits are trump at once (both hearts and spades beat everything else).
69. Trump isn't fixed — it's whatever suit the leader just led, every trick.
70. If nobody plays the led suit or trump, the first card played wins by default.

### 10. Special-card actions — Crazy-eights-style (→ a pending-state field + `IsPlayable` / turn loop)
71. 2s force the next player to draw two cards and lose their turn.
72. Jokers can always be played and skip the next player.
73. A 4 lets the current player immediately go again.
74. A Queen reverses direction.
75. An Ace lets the player announce a new current suit (a second wild rank, alongside 8s).
76. Playing two same-rank cards back to back forces EVERY other player to draw one card.
77. A black Jack lets you swap hands with any opponent.
78. A player whose hand reaches 10 cards is eliminated from the round.

### 11. Round structure / end condition (→ the play loop's while condition)
79. Play until the draw pile is empty, not a fixed round count.
80. Play a fixed 10 rounds no matter what.
81. Stop the instant one player reaches zero cards, however many rounds that took.
82. Best of 3 games — first to win 2 games wins the match.
83. Sudden death: the game ends the instant any player reaches a target score, even mid-round.
84. If regulation ends tied, play one extra round at a time ("overtime") until someone is strictly ahead.

### 12. Display-only traps (touch NOTHING but the print statement)
85. Show each hand sorted by rank.
86. Print suits as symbols (♣ ♦ ♥ ♠) instead of letters.
87. Print the joker as **JOKER** surrounded by stars.
88. Group the printed hand by suit, clubs first.

---

## ADVANCED ROUND — the ones that actually separate strong from average

### 13. Multi-home mutations (two rule homes in ONE sentence)
89. Aces are high, AND worth 15 points instead of 1.
90. Diamonds are trump for trick resolution, AND diamonds score double for the point tally.
91. Lowest score wins, AND jokers are wild for classification.
92. 8s are wild, AND playing an 8 also skips the next player.
93. Suits break ties, AND the tie-break suit rotates every round like trump does.
94. Face cards are worth 10 — except diamonds, which keep their OLD value and ALSO count double.

### 14. Clarifying-question traps (the right first move is a question, not code)
95. "Face cards score double." (Double of what — their old value, or a flat 10?)
96. "Add a wild card." (Wild for scoring, classification, legality — or all three?)
97. "The best hand wins now," said mid-interview after you built a scoring (not classification) game. (Full redesign, or just relabel "highest score"?)
98. "A new player joins mid-game." (Dealt in from now, or does the hand restart?)
99. "Cards are dealt face up now." (A rule change, or only display/narration?)
100. "It's a tie," with no other context, after several unrelated mutations. (Tie in score? Category? Trick count?)

---

## PART B — ANSWER KEY

### 1. Scoring / points

| # | Home | Fix |
|---|---|---|
| 1 | `PointsOf` | `default: return int.Parse(card.Rank) * 2;` |
| 2 | `PointsOf` | `if (card.Rank is "J" or "Q" or "K") return 10;` |
| 3 | `PointsOf` | keep J/Q/K as-is; `if (card.Rank == "A") return 15;` |
| 4 | `PointsOf` | `if (card.Suit == "S") points *= 2;` |
| 5 | `PointsOf` | `if (card.Suit is "H" or "D") points += 2;` |
| 6 | `PointsOf` | `if (card.IsJoker) return -5;` (early return, top of method) |
| 7 | `PointsOf` | `int v = card.Strength + 1; return v * v;` |
| 8 | `PointsOf` | `if (card.Rank == "2" && card.Suit == "C") return 50;` — **must be the very first line**, before the general rule |
| 9 | `PointsOf` | `if (card.Strength is >= 1 and <= 4) return 0;` (`Strength` for "2".."5" is 1..4) |
| 10 | `BasePoints` + `BestTotal` | joker gets a flexible value like an ace (start at 11), then joins the same "drop by 10 while busting" loop — no new loop, just count it alongside `aces` |

### 2. Rank ordering

| # | Home | Fix |
|---|---|---|
| 11 | `Ranks.Order` | move `"A"` next to `"JOKER"`: `{ "2",...,"K","A","JOKER" }` |
| 12 | `Ranks.Order` | `{ "JOKER","A","2",...,"K" }` |
| 13 | `Ranks.Order` | `Order = Ranks.Order.Reverse().ToArray();` (or write the reversed literal) |
| 14 | `Ranks.Order` | swap J/Q/K's three positions only |
| 15 | `Ranks.Order` | swap just those two entries' positions |
| 16 | `Ranks.Order` | replace the whole array with the given sequence |
| 17 | **NOT** `Ranks.Order` — a real trap | **NEW —** needs a field on `Card`, e.g. `public int DealOrder;` set when dealt, compared only when `Strength` ties |
| 18 | `Ranks.Strength`, not the array | `if (int.TryParse(rank, out _)) return 1;` before the normal `Array.IndexOf` lookup — a custom function, not a pure array move |

### 3. Suit order / tie-break

| # | Home | Fix |
|---|---|---|
| 19 | `Suits.Strength` + comparator | `Strength = {"C","D","H","S"}`; in the comparator: `if (a.Strength == b.Strength) return Suits.Of(a.Suit).CompareTo(Suits.Of(b.Suit));` |
| 20 | `Suits.Strength` | `Strength = {"S","H","D","C"}` |
| 21 | `Suits.Of` | `public static int Of(string s) => s == "D" ? 1 : 0;` (custom function, not `Array.IndexOf`) |
| 22 | the comparator, guarded | wrap the existing suit-compare in `if (isLastRound) { ... }` |
| 23 | new field + comparator | `string TieBreakSuit;` set once at round start; `if (a.Suit == TieBreakSuit) return 1;` |
| 24 | the comparator, guarded | `bool IsRed(string s) => s is "H" or "D"; if (IsRed(a.Suit) != IsRed(b.Suit)) { ...suit compare... }` |

### 4. Deck composition

| # | Home | Fix |
|---|---|---|
| 25 | `Deck` ctor | `new Deck(deckCount: 2)` |
| 26 | `Deck` ctor | **NEW —** add a `stripSuits` param mirroring `stripRanks`: `if (skipSuits == null` + `!skipSuits.Contains(suit))` |
| 27 | `Deck` ctor | `new Deck(stripRanks: new[] {"J","Q","K"})` |
| 28 | `Deck` ctor | change the two hardcoded `Add(new Card("JOKER", null))` lines to a `for (int j = 0; j < 4; j++)` loop |
| 29 | `Deck` ctor | `new Deck(stripRanks: new[] {"8","9","10"})` |
| 30 | `Deck` ctor, after building | `_cards.RemoveAll(c => c.Rank == "A" && c.Suit == "S");` |
| 31 | `Deck` ctor structure | move the `if (includeJokers) { ... }` block **outside** the `for (int d = 0; d < deckCount; d++)` loop so it runs once, not per deck |
| 32 | `Deck` + the play loop | add `Reshuffle(discards)` (already sketched in `Core.cs`); call site: `if (Deck.Count < 10) Deck.Reshuffle(discardPile);` |
| 33 | `Deck` ctor | `new Deck(seed: 42)` — already supported, just always pass one |
| 34 | `Deck` ctor, after building | `for (int k = 0; k < 4; k++) _cards.Add(new Card("A", "C"));` — no longer built purely from `Ranks.Order` |

### 5. Winner / tie-resolution

| # | Home | Fix |
|---|---|---|
| 35 | `Winners()` override + pool helper | `BestAmong(pool)` + `while (contenders.Count > 1 && Deck.Count >= contenders.Count)` — you already built this (`TieBreakDrawGame`) |
| 36 | `Winners()` | among the tied group: `.OrderByDescending(p => p.Hand.Max(c => c.Strength)).First()` — no loop needed |
| 37 | `Winners()` — **bigger than a one-liner** | call `Deal(5)` again for just the tied players, then re-score; say out loud this is structural, not a line edit |
| 38 | `Winners()`'s return shape | return a richer result, e.g. `(List<Player> Winners, List<Player> RunnersUp)` |
| 39 | new method, mirrors `Winners()` | `int worst = pool.Min(ScoreHand); return pool.Where(p => ScoreHand(p) == worst).ToList();` |
| 40 | `Winners()` | `Players.Where(p => ScoreHand(p) <= Target).OrderByDescending(ScoreHand).First()` |
| 41 | `Winners()`, among the tied group | `.OrderByDescending(p => p.Hand.Count).First()` |
| 42 | `Winners()`, after finding the best | `if (best - secondBest < 5) return contenders; // declared a draw` |

### 6. Legality / playability

| # | Home | Fix |
|---|---|---|
| 43 | `IsPlayable` | `if (card.Rank == "8") return true;` (already built) |
| 44 | `IsPlayable` | `bool IsRed(Card c) => c.Suit is "H" or "D"; return IsRed(card) == IsRed(top);` |
| 45 | `IsPlayable` | `return Math.Abs(card.Strength - top.Strength) == 1;` |
| 46 | `IsPlayable` | `if (card.Rank is "J" or "Q" or "K") return true;` — one more branch at the top |
| 47 | `IsPlayable` — **needs new state** | `string LastPlayedRank;` per player, checked alongside the rank/suit match |
| 48 | `IsPlayable`, guarded | `if (top == null) return true;` |
| 49 | the turn method's "draw" branch | change the draw count from `1` to `3` |
| 50 | the turn method, not `IsPlayable` | legality predicate is unchanged; the action removes 2 matching cards instead of 1 — **two homes, not one** |

### 7. Turn order / direction

| # | Home | Fix |
|---|---|---|
| 51 | `Direction` field | `Direction = -Direction;` (already built) |
| 52 | the turn loop | skip the `Current = AdvanceTurn(...)` call entirely this turn |
| 53 | `AdvanceTurn` call site | `Current = AdvanceTurn(AdvanceTurn(Current, n, Direction), n, Direction);` |
| 54 | a new per-round step | `order = players.OrderByDescending(p => p.LastDraw.Strength).ToList();` — a different turn-order *source*, not `AdvanceTurn` |
| 55 | `LeaderIndex` | `LeaderIndex = winnerIndex;` (already the Trick Taking default) |
| 56 | the play loop | `if (roundNumber % 3 == 0) Direction = -Direction;` |

### 8. Classification (Best Hand)

| # | Home | Fix |
|---|---|---|
| 57 | `Ladder` + `Classify` | insert `"Two Pair"`; detect via `groups[0].Size == 2 && groups[1].Size == 2` |
| 58 | `Ladder` (top slot) + `Classify` | `hand.All(c => c.Suit == hand[0].Suit)` on the **original** hand |
| 59 | `Ladder` + `Classify` | `groups[0].Size == 3 && groups[1].Size == 2` |
| 60 | `Ladder` + `Classify` | `groups[0].Size == 4` |
| 61 | **NEW method**, not `GroupBy` | see code below the table |
| 62 | combines 58 + 61 | `IsStraight(hand) && IsFlush(hand)` — one more `Ladder` slot above both |
| 63 | `Compare`'s `TieBreakers` walk | if the loop exhausts with no difference, `return 0;` (already handled if built right) |
| 64 | top of `Classify`, before grouping | one named-hand `if` checking the exact 5 ranks, returning a fixed top result |

Item 61, in full — this is the one detection method in the whole file that ISN'T `GroupBy`-based:
```csharp
bool IsStraight(List<Card> hand)
{
    var s = hand.Select(c => c.Strength).OrderBy(x => x).ToList();
    for (int i = 1; i < s.Count; i++)
        if (s[i] != s[i - 1] + 1) return false;
    return true;
}
```

### 9. Trump (Trick Taking)

| # | Home | Fix |
|---|---|---|
| 65 | `WinnerOfTrick`'s tier function | `trump: "S"` (already built) |
| 66 | new helper feeding the tier function | `string TrumpFor(int trickNo) => Suits.All[trickNo % 4];` |
| 67 | the call site | `WinnerOfTrick(plays, ledSuit, trump: null)` for this trick only |
| 68 | the tier function itself | `Func<Card,int> tier = c => trumps.Contains(c.Suit) ? 2 : (c.Suit == ledSuit ? 1 : 0);` where `trumps` is a `HashSet<string>` |
| 69 | the tier function collapses | `Func<Card,int> tier = c => c.Suit == ledSuit ? 1 : 0;` — trump state isn't needed at all |
| 70 | no change — confirm, don't build | `OrderByDescending` is a stable sort; `.First()` already picks the first play among equals |

### 10. Special-card actions (Crazy Eights style)

| # | Home | Fix |
|---|---|---|
| 71 | new `PendingDraw` counter | set to `2` when a 2 is played; served at the top of the next turn, then cleared |
| 72 | `IsPlayable` (already true) + `PendingSkip` | `PendingSkip = true;` when a joker is played |
| 73 | the turn loop | don't call `AdvanceTurn` this turn |
| 74 | `Direction` field | `Direction = -Direction;` |
| 75 | your existing `ChooseSuit` helper | generalize the wild-8 branch: `if (card.Rank is "8" or "A") { ...ChooseSuit... }` — one method, not a copy-paste second one |
| 76 | new "last two plays" check | if the last two ranks match: `foreach (var other in otherPlayers) other.Hand.Add(Deck.Draw());` |
| 77 | directly swaps `Player.Hand` — **biggest one here** | `(playerA.Hand, playerB.Hand) = (playerB.Hand, playerA.Hand);` — the same tuple-swap trick as `Shuffle` |
| 78 | new elimination check in the turn loop | `if (p.Hand.Count >= 10) eliminated.Add(p);` |

### 11. Round structure / end condition

| # | Home | Fix |
|---|---|---|
| 79 | the play loop's `while` | `while (Deck.Count > 0) PlayRound();` |
| 80 | the play loop's `for` | `for (int r = 0; r < 10; r++) PlayRound();` (often already the default) |
| 81 | the play loop's `while` | `while (!Players.Any(p => p.Hand.Count == 0)) PlayRound();` |
| 82 | a new OUTER loop | `int gamesWon = 0; while (gamesWon < 2) { PlayOneGame(); if (winnerThisGame) gamesWon++; }` |
| 83 | inside the round loop | `if (p.Score >= Target) return p;` — checked mid-round, not just at the end |
| 84 | after the fixed rounds | `while (TopScorers().Count > 1) PlayOneRound();` |

### 12. Display-only traps

| # | Home | Fix |
|---|---|---|
| 85 | the `Console.WriteLine` call only | `hand.OrderBy(c => c.Strength)` at print time; `Hand` itself untouched |
| 86 | a print-time lookup | `suit switch { "C" => "♣", "D" => "♦", "H" => "♥", "S" => "♠" }` |
| 87 | the print line only | `"**" + card + "**"` |
| 88 | the `Console.WriteLine` call only | `hand.OrderBy(c => c.Suit)` at print time; never resort `Hand` itself |

---

## Advanced round — answer key

### 13. Multi-home mutations — TWO homes each. Missing either one means you only did half the rule.

| # | Home 1 | Home 2 |
|---|---|---|
| 89 | `Ranks.Order` — move `"A"` | `PointsOf` — `if (card.Rank == "A") return 15;` |
| 90 | `WinnerOfTrick` tier — `trump: "D"` | `PointsOf` — `if (card.Suit == "D") points *= 2;` |
| 91 | `Winners()` — `Max` → `Min` | `BestHand`'s `MakeJokersWild` preprocessing |
| 92 | `IsPlayable` — already true for 8s | turn loop — `PendingSkip = true;` when an 8 is played |
| 93 | new `Suits.Strength` array | a rotation helper shaped just like `TrumpFor(trickNo)` |
| 94 | `PointsOf`, faces → 10 first | **then** a diamond branch reading the OLD value: see code below |

Item 94, in full — order of the `if`s is the whole trick:
```csharp
public override int PointsOf(Card card)
{
    if (card.Rank is "J" or "Q" or "K")
        return card.Suit == "D" ? OldFaceValue(card.Rank) * 2 : 10;
    return base.PointsOf(card);
}
```

### 14. Clarifying-question traps — the fix is a QUESTION, not code. If forced to guess, state the assumption as a one-line comment.

| # | Ask this | If forced, assume |
|---|---|---|
| 95 | "Double the printed value, or double a flat number?" | `// ASSUMPTION: doubling applies to the existing PointsOf value` |
| 96 | "Wild for scoring, classification, or legality — or all three?" | `// ASSUMPTION: wild applies to classification only, per the mock's own wording` |
| 97 | "Full redesign to hand-classification, or just relabel 'highest score' as 'best hand'?" | `// ASSUMPTION: keeping the existing scoring shape; 'best hand' = highest ScoreHand` |
| 98 | "Dealt in from now, or does the hand restart for everyone?" | `// ASSUMPTION: new player gets a fresh hand dealt now; others unaffected` |
| 99 | "Is this a rule change, or only display/narration?" | `// ASSUMPTION: display only — no method other than ToString/print changes` |
| 100 | "Tie in score, category, or trick count?" | `// ASSUMPTION: tie refers to whichever system the last 2 mutations touched` |
