# 11 — Part 3 Mega-Drill: 100 Mutations, Question Right Next to Its Answer

This is Drill D (`06-practice-plan.md`), scaled up. The core table in `03-design-playbook.md` has 14 routes — memorize that one first. This file is for the day before the interview: **volume practice**, so no phrasing surprises you today.

## How to use this (no code — this is a SPEAKING drill)

1. Cover the **→ Answer** line right under each rule with your hand or a sheet of paper.
2. Read the rule out loud.
3. Say, out loud, in one sentence: *"That's a `<kind of rule>`, so it lives in `<method/array>`."*
4. Only then uncover the answer. Right → move on. Wrong or hesitant → reread the matching row in `03-design-playbook.md`, say it again, move on.
5. Target pace: under 20 seconds per item. If a whole category feels shaky, that's your last-hour reading, not this whole file.

**Short on time? Do this instead:** categories 1–6 (scoring, ordering, suits, deck, winners, legality) are the highest-value 50. Do those, then jump straight to the **Advanced** section at the end — those are the ones that separate a strong candidate from an average one.

**A note on the answers below:** most fixes are genuine one-liners, lifted straight from the shapes in your `Concepts` project. Wherever a rule is **bigger than a one-liner**, the answer says so explicitly and explains *why* — that flag, not the code, is the actual skill: knowing in advance that something needs new state or a structural change, instead of hunting for a line to edit that doesn't exist.

---

## 1. Scoring / points (→ `PointsOf` / `BasePoints`)

**1.** Number cards score double their face value.
→ **`PointsOf`.** `default: return int.Parse(card.Rank) * 2;` — only the fall-through case for plain numbers changes; faces, ace, and joker stay whatever they already were.

**2.** Face cards (J/Q/K) are all worth 10.
→ **`PointsOf`.** `if (card.Rank is "J" or "Q" or "K") return 10;` — three cases collapse into one.

**3.** Face cards keep 11/12/13, but Aces are worth 15.
→ **`PointsOf`.** Leave J/Q/K exactly as they are; only the Ace case changes: `if (card.Rank == "A") return 15;`

**4.** Spades count double.
→ **`PointsOf`.** `if (card.Suit == "S") points *= 2;` — one multiplier line, after the base value is computed.

**5.** Any red card (hearts or diamonds) scores a +2 bonus.
→ **`PointsOf`.** `if (card.Suit is "H" or "D") points += 2;`

**6.** Jokers are worth −5 (a penalty, not a bonus).
→ **`PointsOf`.** `if (card.IsJoker) return -5;` — as an early return at the very top, same shape as the existing "joker = 20" example, just negative.

**7.** Every card's value is its rank strength, squared.
→ **`PointsOf`.** `int v = card.Strength + 1; return v * v;` — the `+1` matters: `Strength` is 0-indexed (Ace=0), but "value" should start at 1, not 0.

**8.** The 2 of clubs specifically is worth 50 (one named "trap card").
→ **`PointsOf`.** `if (card.Rank == "2" && card.Suit == "C") return 50;` — **must be the very first line**, before the general rule, or the general rule would answer first and this line would never run.

**9.** Cards 2 through 5 score zero — they're "dead cards."
→ **`PointsOf`.** `if (card.Strength is >= 1 and <= 4) return 0;` — `Strength` for "2".."5" is 1..4 (Ace is 0, so "2" is index 1).

**10.** In Blackjack, a joker is "wild": it counts as whatever value (0–11) gets the hand closest to 21 without busting.
→ **`BasePoints` + `BestTotal` — a genuine two-step change, not one line.** Give the joker a flexible starting value like an ace (11 up front in `BasePoints`), then let it join the SAME "drop by 10 while busting" loop that already exists for aces in `BestTotal` — just count jokers alongside `aces` in that loop's counter. **Why this isn't a bigger rewrite:** the soft-ace mechanism already generalizes to "any flexible card," so a joker is just one more thing that's flexible, not a new mechanism.

---

## 2. Rank ordering (→ `Ranks.Order`, a data move)

**11.** Aces are high, for comparison purposes only.
→ **`Ranks.Order`.** Move `"A"` next to `"JOKER"`: `{ "2",...,"K","A","JOKER" }`

**12.** The joker now ranks BELOW the ace — the weakest card in the deck.
→ **`Ranks.Order`.** `{ "JOKER","A","2",...,"K" }`

**13.** Rank order is reversed entirely: King is lowest, 2 is highest.
→ **`Ranks.Order`.** `Order = Ranks.Order.Reverse().ToArray();` (or write the reversed literal directly).

**14.** Face cards outrank each other in reverse: K < Q < J.
→ **`Ranks.Order`.** Swap J/Q/K's three positions only; everything else in the array stays put.

**15.** Two specific ranks swap places: 5s now outrank Kings.
→ **`Ranks.Order`.** Swap just those two entries' positions.

**16.** You're given a full custom order for this round: 7,8,9,10,J,Q,K,A,2,3,4,5,6.
→ **`Ranks.Order`.** Replace the whole array with the given sequence — still one array, just every entry moved.

**17.** Ties in rank are now broken by whichever card was DEALT first.
→ **NOT `Ranks.Order` — this is a deliberate trap.** Rank *order* answers "which rank is stronger," but this rule needs a completely different piece of information: *when* a card was dealt. That doesn't exist anywhere yet. **The fix:** add a field to `Card` (or track it externally, e.g. a `Dictionary<Card,int>` of deal order), something like `public int DealOrder;`, set once when the card is actually dealt. Then in the comparator: only consult `DealOrder` as the tie-breaker *after* `Strength` already came back equal. **Why this matters:** if you go looking for "the array to edit" on this one, you'll waste real minutes, because there isn't one — recognizing that *before* you start typing is the actual point of this drill item.

**18.** Number cards are all equal strength; only aces and face cards have real order.
→ **`Ranks.Strength`, not the array itself.** Don't try to cram this into `Ranks.Order` by repeating values — instead, special-case it in the `Strength` FUNCTION: `if (int.TryParse(rank, out _)) return 1;` before falling through to the normal `Array.IndexOf` lookup for named ranks. **Why this is different from the other rows above:** every other rank-ordering mutation here is "rearrange the array." This one can't be — an array position is unique per entry, but this rule wants *many* entries to share one strength value. That's a function change, not a data move.

---

## 3. Suit order / tie-break (→ `Suits.Strength` + one compare)

**19.** Suits break ties: clubs weakest, spades strongest.
→ **`Suits.Strength` + the comparator.** `Strength = {"C","D","H","S"}`; in the comparator: `if (a.Strength == b.Strength) return Suits.Of(a.Suit).CompareTo(Suits.Of(b.Suit));` — your kit's own baseline example.

**20.** Reverse that: spades weakest, clubs strongest.
→ **`Suits.Strength`.** `Strength = {"S","H","D","C"}` — same array, reversed.

**21.** Only diamonds are special: they beat a tie; every other suit stays equal to every other.
→ **`Suits.Of`.** Not a 4-entry array this time — a tiny custom function: `public static int Of(string s) => s == "D" ? 1 : 0;` Every non-diamond suit now compares equal to every other non-diamond suit, which is exactly what "only diamonds are special" means.

**22.** The suit tie-break only applies in the LAST round of the game.
→ **The comparator, guarded.** Wrap the *existing* suit-compare block in one condition: `if (isLastRound) { ...suit compare... }` — nothing about the suit array or the rank check changes, just when the extra compare step runs.

**23.** A player may choose which suit is "trump" for tie-breaking before the round starts.
→ **A new field + the comparator.** Add `string TieBreakSuit;`, set once at round start (not per-comparison). Then: `if (a.Suit == TieBreakSuit) return 1; if (b.Suit == TieBreakSuit) return -1;` — no full ordering array needed, just "is this suit THE trump."

**24.** Suits break ties only between two cards of different color; same-color ties stay ties.
→ **The comparator, guarded.** `bool IsRed(string s) => s is "H" or "D"; if (IsRed(a.Suit) != IsRed(b.Suit)) { ...suit compare... }` — an extra condition wrapping the same suit-compare logic you already have.

---

## 4. Deck composition (→ `Deck` constructor)

**25.** Use two decks shuffled together.
→ **`Deck` constructor.** `new Deck(deckCount: 2)` — the parameter already exists for exactly this.

**26.** Remove one entire suit before playing.
→ **`Deck` constructor — needs a new parameter, not just a new argument.** There's no `stripSuits` yet, only `stripRanks`. **The fix:** add `string[] stripSuits = null` mirroring the existing pattern, and guard the suit loop the same way ranks are already guarded: `if (skipSuits == null || !skipSuits.Contains(suit))`. **Why it's slightly bigger than row 25:** the CAPABILITY doesn't exist yet — you're extending the constructor's shape, not just calling it differently.

**27.** Remove all face cards — number cards only.
→ **`Deck` constructor.** `new Deck(stripRanks: new[] {"J","Q","K"})` — already supported.

**28.** Add FOUR jokers instead of two.
→ **`Deck` constructor.** Change the two hardcoded `_cards.Add(new Card("JOKER", null));` lines to a small loop: `for (int j = 0; j < 4; j++) _cards.Add(new Card("JOKER", null));`

**29.** Play with a 40-card deck (strip 8s, 9s, and 10s).
→ **`Deck` constructor.** `new Deck(stripRanks: new[] {"8","9","10"})` — already supported.

**30.** One specific card is simply missing from the deck (someone "lost" the Ace of Spades).
→ **`Deck` constructor, after building.** `_cards.RemoveAll(c => c.Rank == "A" && c.Suit == "S");` — build the deck normally, then remove the one exact card.

**31.** Combine two decks, but include only ONE joker total, not two per deck.
→ **`Deck` constructor's structure, not just its parameters.** Right now, the joker-adding block lives *inside* the `for (int d = 0; d < deckCount; d++)` loop, so it runs once per deck. **The fix:** move that block *outside* the loop, so it runs exactly once regardless of `deckCount`. **Why this is worth calling out:** it's a two-line move, but it's easy to miss that the CURRENT placement is the bug — reread your own deck-building loop before assuming "just add a parameter" is enough.

**32.** The deck must automatically reshuffle its discard pile once it drops below 10 cards.
→ **Two homes: `Deck` gains a method, and the play loop calls it.** Add `Reshuffle(discards)` to `Deck` (already sketched as an idea in `Core.cs` — take the discard pile back in, then `Shuffle()` again). Then, in whatever loop draws cards each turn: `if (Deck.Count < 10) Deck.Reshuffle(discardPile);` **Why this needs two edits, not one:** the *capability* (reshuffling) lives in `Deck`; the *decision of when* to do it lives in the game loop. Conflating them means either `Deck` starts making game decisions it shouldn't, or the game loop starts reaching into `Deck`'s internals.

**33.** The deck must start in a fixed, known order for testing — not randomly shuffled.
→ **`Deck` constructor.** `new Deck(seed: 42)` — already supported; a seed makes `Shuffle()` deterministic, it doesn't skip shuffling.

**34.** Certain ranks are duplicated extra times (4 extra Aces added) — no longer a "standard" deck at all.
→ **`Deck` constructor, after building.** `for (int k = 0; k < 4; k++) _cards.Add(new Card("A", "C"));` (or whichever suit makes sense to you) — **worth saying out loud:** the deck is no longer built purely FROM `Ranks.Order` at this point; you're deliberately breaking the "one source of truth" pattern, so name that trade-off rather than let it look like an oversight.

---

## 5. Winner / tie-resolution (→ `Winners()` / `ResolveWinners()` / a pool-based helper)

**35.** Ties are no longer shared: each tied player draws one card, repeat until one winner (you already built this one).
→ **`Winners()` override + a pool-based helper.** `BestAmong(pool)` (parameterized on a shrinking pool, not always the full player list) inside `while (contenders.Count > 1 && Deck.Count >= contenders.Count)` — this is `TieBreakDrawGame`, already built and verified.

**36.** Ties are broken by whoever holds the single highest card in hand — no redraw.
→ **`Winners()`.** Among the tied group only: `.OrderByDescending(p => p.Hand.Max(c => c.Strength)).First()` — no loop, no redraw, just one more sort key.

**37.** On a tie, replay the ENTIRE hand from scratch, but only for the tied players.
→ **`Winners()` — genuinely bigger than a one-liner.** This isn't "add extra cards" (row 35) — it's "deal a brand-new hand." You'd call `Deal(5)` again, but only for the players still in `contenders`, then re-score from zero. **Say this out loud in the interview:** *"This is a structural change, not a line edit — I need to re-deal for a subset of players, which `Deal` doesn't currently support since it always deals to everyone."* Naming that BEFORE you start typing is worth real credit.

**38.** Second place also earns a small consolation point — winner logic now has tiers, not just first place.
→ **`Winners()`'s return shape changes.** A single "the winners" list isn't enough anymore — you need at least two tiers. Return something richer, e.g. a tuple `(List<Player> Winners, List<Player> RunnersUp)`, or a small result type with a rank number per player. **Why this counts as bigger:** every CALLER of `Winners()` (printing, checks) now needs updating too, since the return type itself changed — that ripple is worth mentioning out loud.

**39.** A tie for LAST place eliminates that player.
→ **A new method, mirroring `Winners()`.** `int worst = pool.Min(ScoreHand); return pool.Where(p => ScoreHand(p) == worst).ToList();` — literally `Winners()` with `Max` swapped for `Min`, given its own name (e.g. `Losers()`) since it answers a different question.

**40.** The winner is whoever is closest to a target number without going over — not whoever has the highest raw score.
→ **`Winners()`.** `Players.Where(p => ScoreHand(p) <= Target).OrderByDescending(ScoreHand).First()` — the same "closest without busting" shape as Blackjack's `BestTotal`, just applied to picking a winner instead of an ace value.

**41.** On a tie, whoever has MORE cards in hand automatically wins — no redraw needed.
→ **`Winners()`, among the tied group.** `.OrderByDescending(p => p.Hand.Count).First()` — one more sort key, no loop.

**42.** A win must be by a margin of at least 5 points, or it's declared a draw for everyone.
→ **`Winners()`, after finding the best score.** `if (best - secondBest < 5) return contenders; // declared a draw` — you need the SECOND-best score too, not just the best, so this touches how you compute `best` as well (you now need the top two distinct scores, not just the top one).

---

## 6. Legality / playability (→ `IsPlayable` / `LegalCards`)

**43.** 8s are wild and playable on anything.
→ **`IsPlayable`.** `if (card.Rank == "8") return true;` — already built, a branch at the top.

**44.** You may play any card of the same COLOR as the top card (red/black), not the same suit.
→ **`IsPlayable`.** `bool IsRed(Card c) => c.Suit is "H" or "D"; return IsRed(card) == IsRed(top);`

**45.** You may play any card numerically ADJACENT to the top card's rank, regardless of suit.
→ **`IsPlayable`.** `return Math.Abs(card.Strength - top.Strength) == 1;`

**46.** Face cards are always playable, no matter what.
→ **`IsPlayable`.** `if (card.Rank is "J" or "Q" or "K") return true;` — one more branch at the top, same shape as the wild-8 branch.

**47.** You may never play the same exact rank twice in a row across your own turns.
→ **`IsPlayable` — needs new state that doesn't exist yet.** The predicate currently only looks at `card`, `top`, and `currentSuit` — none of those remember what a PLAYER did last time. **The fix:** add `string LastPlayedRank;` per player, updated after every play, and check it alongside the existing rank/suit match: `&& card.Rank != player.LastPlayedRank`. **Why this is a real trap:** every other legality mutation in this section is "one more condition using data `IsPlayable` already receives." This one needs the SIGNATURE (or the surrounding state) to grow, because the rule depends on history, not just the current card and top.

**48.** On the very first turn, any card is legal (there's no top card yet).
→ **`IsPlayable`, guarded.** `if (top == null) return true;` — one line at the very top of the method.

**49.** A player who cannot play must draw THREE cards, not one.
→ **The turn method's "draw" branch, not `IsPlayable`.** Change the draw count from `1` to `3` wherever the "can't play, so draw" logic lives — legality itself doesn't change at all.

**50.** Two matching-rank cards may be played together in a single turn if you hold both.
→ **Two homes: the turn method changes, `IsPlayable` doesn't.** The legality PREDICATE for a single card is unchanged — the ACTION taken on a turn now removes 2 matching cards instead of 1, which lives in whatever method actually executes a turn. **Why this is worth flagging:** it's tempting to go looking for the fix inside `IsPlayable` since the rule mentions "playable" cards, but the real change is entirely in the turn-taking method's logic, not the legality check.

---

## 7. Turn order / direction (→ `AdvanceTurn` / the turn loop)

**51.** A Queen reverses direction.
→ **The `Direction` field.** `Direction = -Direction;` — already built; `AdvanceTurn`'s double-mod already wraps negative directions correctly.

**52.** Playing a specific rank makes the SAME player go again.
→ **The turn loop.** Simply skip the `Current = AdvanceTurn(...)` call for this turn — no new state needed, just a conditional skip of the usual advance step.

**53.** A Jack skips the next TWO players, not one.
→ **The `AdvanceTurn` call site.** `Current = AdvanceTurn(AdvanceTurn(Current, n, Direction), n, Direction);` — call it twice (or add a `steps` parameter) instead of once.

**54.** Turn order each round is decided by a drawn card (highest goes first), not fixed rotation.
→ **A new per-round step — not `AdvanceTurn` at all.** `order = players.OrderByDescending(p => p.LastDraw.Strength).ToList();` **Why this is different from rows 51–53:** those all still use the SAME turn-order mechanism (an index + direction), just nudged. This rule replaces the mechanism's SOURCE entirely — turn order now comes from a fresh ranking every round, not from advancing an index at all.

**55.** The round/trick winner leads next.
→ **`LeaderIndex`.** `LeaderIndex = winnerIndex;` — already the Trick Taking default; worth remembering as the pattern if a *different* game later needs the same idea.

**56.** Direction reverses automatically every 3 rounds, with no card triggering it.
→ **The play loop.** `if (roundNumber % 3 == 0) Direction = -Direction;` — a scheduled check instead of a card-triggered one, same field either way.

---

## 8. Classification (Best Hand) (→ `BestHand.Classify` + the `Ladder` array)

**57.** Add Two Pair, between One Pair and Three of a Kind.
→ **`Ladder` + `Classify`.** Insert `"Two Pair"` into the ladder array at the right position; detect it via `groups[0].Size == 2 && groups[1].Size == 2` (after your existing sort by group size).

**58.** Add Flush — all 5 cards the same suit — beats everything.
→ **`Ladder` (top slot) + `Classify`.** `hand.All(c => c.Suit == hand[0].Suit)` — checked on the ORIGINAL hand, not the grouped-by-rank data, since a flush is about suits, not rank groups.

**59.** Add Full House — a pair plus a three-of-a-kind together.
→ **`Ladder` + `Classify`.** `groups[0].Size == 3 && groups[1].Size == 2` — same group-size check style as Two Pair, just a different combination.

**60.** Add Four of a Kind.
→ **`Ladder` + `Classify`.** `groups[0].Size == 4`

**61.** Add a Straight — 5 consecutive strengths, any suits.
→ **A genuinely NEW method — the one detector in this whole file that isn't `GroupBy`-based.** Everything else in Best Hand works by grouping same-rank cards; a straight is about *consecutive* ranks, which needs sorting and a gap check instead:
```csharp
bool IsStraight(List<Card> hand)
{
    var s = hand.Select(c => c.Strength).OrderBy(x => x).ToList();
    for (int i = 1; i < s.Count; i++)
        if (s[i] != s[i - 1] + 1) return false;
    return true;
}
```
**Why this is worth flagging on its own:** if you go looking to extend `GroupBy` logic for this one, you'll spend real minutes forcing a shape that doesn't fit — recognizing "this needs sorted-and-consecutive, not grouped" is the actual skill being tested.

**62.** Add a Straight Flush — a Straight that's also a Flush.
→ **Combines rows 58 + 61.** `IsStraight(hand) && IsFlush(hand)` — one more `Ladder` slot above both; no new detection logic, just both existing checks ANDed together.

**63.** Same category, same defining rank, same kicker too → confirm it's a true shared tie.
→ **`Compare`'s `TieBreakers` walk.** If the loop exhausts every comparison with no difference found, `return 0;` — already handled correctly if you built the walk as a loop rather than a fixed number of comparisons.

**64.** The exact hand `2, 7, Q, J, K` of mixed suits is a special named hand that auto-wins regardless of everything else.
→ **Top of `Classify`, before any grouping happens.** One named-hand check — compare the exact 5 ranks — that returns a fixed top-tier result immediately, before the normal `GroupBy` logic ever runs.

---

## 9. Trump (Trick Taking) (→ `WinnerOfTrick`'s tier function)

**65.** Spades are trump.
→ **`WinnerOfTrick`'s tier function.** `trump: "S"` — already built and working.

**66.** Trump rotates every trick: C, D, H, S, repeat.
→ **A new helper feeding the same tier function.** `string TrumpFor(int trickNo) => Suits.All[trickNo % 4];` — `WinnerOfTrick` itself doesn't change at all, just what gets passed in as `trump`.

**67.** This particular trick has NO trump, even though one is set for the game.
→ **The call site, not the method.** `WinnerOfTrick(plays, ledSuit, trump: null)` for just this one trick.

**68.** TWO suits are trump at once (both hearts and spades beat everything else).
→ **The tier function itself changes shape.** A single `string trump` can't represent two suits. `Func<Card,int> tier = c => trumps.Contains(c.Suit) ? 2 : (c.Suit == ledSuit ? 1 : 0);` where `trumps` is now a `HashSet<string>` instead of one string. **Why this is more than "pass a different value":** the PARAMETER TYPE changes, so every call site needs updating too — worth naming that ripple.

**69.** Trump isn't fixed — it's whatever suit the leader just led, every trick.
→ **The tier function collapses to something simpler.** `Func<Card,int> tier = c => c.Suit == ledSuit ? 1 : 0;` — no separate trump concept is needed at all here, since "trump" and "led suit" are now always the same thing.

**70.** If nobody plays the led suit or trump, the first card played wins by default.
→ **No code change — confirm the behavior, don't build new logic for it.** `OrderByDescending` is a stable sort, so when every play ties at tier 0, `.First()` already returns whichever was played first (play order is preserved). Say this out loud rather than adding a redundant tie-break.

---

## 10. Special-card actions (Crazy Eights style) (→ a pending-state field + `IsPlayable` / turn loop)

**71.** 2s force the next player to draw two cards and lose their turn.
→ **A new `PendingDraw` counter.** Set it to `2` when a 2 is played; served at the very top of the NEXT turn (draw that many, clear the counter, advance without letting them play).

**72.** Jokers can always be played and skip the next player.
→ **`IsPlayable` (already true for jokers) + a new `PendingSkip` flag.** `PendingSkip = true;` set when a joker lands; served the same way as `PendingDraw` — check it first, at the top of the next turn.

**73.** A 4 lets the current player immediately go again.
→ **The turn loop.** Simply don't call `AdvanceTurn` this turn — no new state needed.

**74.** A Queen reverses direction.
→ **The `Direction` field.** `Direction = -Direction;`

**75.** An Ace lets the player announce a new current suit (a second wild rank, alongside 8s).
→ **Generalize your existing `ChooseSuit` helper — don't copy-paste a second one.** `if (card.Rank is "8" or "A") { ...ChooseSuit... }` — one method serving both wild ranks, since the "pick a new current suit" logic is identical either way.

**76.** Playing two same-rank cards back to back forces EVERY other player to draw one card.
→ **A new "last two plays" check.** Track the last rank played; if it matches the current one: `foreach (var other in otherPlayers) other.Hand.Add(Deck.Draw());` **Why this needs new state:** nothing currently remembers what the PREVIOUS play was — you need at least one more field to compare against.

**77.** A black Jack lets you swap hands with any opponent.
→ **The biggest structural change in this whole category.** `(playerA.Hand, playerB.Hand) = (playerB.Hand, playerA.Hand);` — the same tuple-swap trick used in `Shuffle`, but this time swapping two PLAYERS' entire hands directly, not cards within one list. **Worth saying out loud:** this is the one mutation here that reaches across two different players' state at once, rather than modifying one player's hand or one piece of shared game state.

**78.** A player whose hand reaches 10 cards is eliminated from the round.
→ **A new elimination check in the turn loop.** `if (p.Hand.Count >= 10) eliminated.Add(p);` — checked after every hand-growing action (a draw, a forced-draw penalty), not just once.

---

## 11. Round structure / end condition (→ the play loop's while condition)

**79.** Play until the draw pile is empty, not a fixed round count.
→ **The play loop's `while`.** `while (Deck.Count > 0) PlayRound();`

**80.** Play a fixed 10 rounds no matter what.
→ **The play loop's `for`.** `for (int r = 0; r < 10; r++) PlayRound();` — often already the default shape; confirm rather than rebuild.

**81.** Stop the instant one player reaches zero cards, however many rounds that took.
→ **The play loop's `while`.** `while (!Players.Any(p => p.Hand.Count == 0)) PlayRound();`

**82.** Best of 3 games — first to win 2 games wins the match.
→ **A new OUTER loop wrapping the existing one.** `int gamesWon = 0; while (gamesWon < 2) { PlayOneGame(); if (winnerThisGame) gamesWon++; }` **Why this counts as more than a tweak:** you're not changing the round loop at all — you're wrapping the WHOLE existing game in a new loop one level up, which is a different kind of edit than adjusting a condition.

**83.** Sudden death: the game ends the instant any player reaches a target score, even mid-round.
→ **Inside the round loop, not just at the end.** `if (p.Score >= Target) return p;` — checked immediately after each point is awarded, not after the round finishes.

**84.** If regulation ends tied, play one extra round at a time ("overtime") until someone is strictly ahead.
→ **A new loop, positioned after the fixed rounds finish.** `while (TopScorers().Count > 1) PlayOneRound();` — the normal round loop is untouched; this is an additional loop that only runs if regulation ended tied.

---

## 12. Display-only traps (touch NOTHING but the print statement)

**85.** Show each hand sorted by rank.
→ **The `Console.WriteLine` call only.** `hand.OrderBy(c => c.Strength)` at print time — `Hand` itself stays exactly as dealt.

**86.** Print suits as symbols (♣ ♦ ♥ ♠) instead of letters.
→ **A print-time lookup, not the `Suit` field.** `suit switch { "C" => "♣", "D" => "♦", "H" => "♥", "S" => "♠" }`

**87.** Print the joker as **JOKER** surrounded by stars.
→ **The print line only.** `"**" + card + "**"`

**88.** Group the printed hand by suit, clubs first.
→ **The `Console.WriteLine` call only.** `hand.OrderBy(c => c.Suit)` at print time — never resort `Hand` itself.

---

# ADVANCED ROUND — the ones that actually separate strong from average

## 13. Multi-home mutations (two rule homes in ONE sentence)

Each of these reads like a single rule but actually needs edits in TWO places. Missing either one means you only implemented half the sentence — say both homes out loud before touching any code.

**89.** Aces are high, AND worth 15 points instead of 1.
→ **Home 1 — `Ranks.Order`:** move `"A"` next to `"JOKER"` (this is about ORDER — who beats whom in a comparison).
→ **Home 2 — `PointsOf`:** `if (card.Rank == "A") return 15;` (this is about VALUE — what the card scores).
**Why it's two homes:** "aces are high" and "aces are worth 15" sound like one idea because they're both about aces, but your own kit's design principle is that ordering and points are DIFFERENT concepts on purpose — that's exactly why this sentence needs two separate edits.

**90.** Diamonds are trump for trick resolution, AND diamonds score double for the point tally.
→ **Home 1 — `WinnerOfTrick`'s tier function:** `trump: "D"` (who wins the trick).
→ **Home 2 — `PointsOf`:** `if (card.Suit == "D") points *= 2;` (how many points the trick/hand is worth).
**Why it's two homes:** these are two completely separate systems (trick-winning vs. score-counting) that happen to both mention diamonds — treat them as two unrelated one-line edits, not one combined edit.

**91.** Lowest score wins, AND jokers are wild for classification.
→ **Home 1 — `Winners()`:** `Max` becomes `Min`.
→ **Home 2 — `BestHand`'s `MakeJokersWild` preprocessing:** unchanged logic, just now also feeding into a lowest-wins comparison.
**Why it's two homes:** this sentence is really describing two DIFFERENT mocks' mutations glued together (Mock 1's "lowest wins" and Mock 3's "jokers wild") — recognizing that they don't interact with each other is as important as fixing each one.

**92.** 8s are wild, AND playing an 8 also skips the next player.
→ **Home 1 — `IsPlayable`:** already true (the wild-8 branch already exists).
→ **Home 2 — the turn loop:** `PendingSkip = true;` set specifically when an 8 is the card played.
**Why it's two homes:** "wild" (which cards are LEGAL to play) and "skip" (what happens to TURN ORDER afterward) are unrelated systems — one predicate, one turn-loop side-effect.

**93.** Suits break ties, AND the tie-break suit rotates every round like trump does.
→ **Home 1 — a new `Suits.Strength` array** (or a comparator using `Suits.Of`).
→ **Home 2 — a rotation helper shaped exactly like `TrumpFor(trickNo)`** from row 66, feeding which suit is currently "on top" into that same comparator.
**Why it's two homes:** the comparator logic (row 19) and the rotation logic (row 66) are each things you've already built separately elsewhere — this rule just asks you to plug one into the other.

**94.** Face cards are worth 10 — except diamonds, which keep their OLD value and ALSO count double.
→ **One home (`PointsOf`), but the ORDER of the `if`s inside it is the entire trick:**
```csharp
public override int PointsOf(Card card)
{
    if (card.Rank is "J" or "Q" or "K")
        return card.Suit == "D" ? OldFaceValue(card.Rank) * 2 : 10;
    return base.PointsOf(card);
}
```
**Why this is worth its own detailed entry even though it's "one home":** it's easy to write this backwards — applying the new value (10) and THEN doubling it, giving 20 instead of the correct "old value, doubled." Trace through one example before typing: a diamond Queen's OLD value was 12, so this rule should give `12 * 2 = 24`, NOT `10 * 2 = 20`. Reading the rule slowly (twice) is cheaper than debugging the wrong branch order live.

---

## 14. Clarifying-question traps (the fix is a QUESTION, not code)

For every rule below, the correct FIRST move is to ask, out loud, before writing anything. If the interviewer won't clarify further (or you're practicing solo), state your assumption as a one-line comment and move on — don't silently guess.

**95.** "Face cards score double."
→ **Ask:** "Double of what — their existing `PointsOf` value, or a flat number like 10?" **Why it's ambiguous:** "double" only means something once you know the starting number, and this interview has already shown face-card values changing between mutations (11/12/13 vs. flat 10) — so "double" could reasonably mean either.
→ **If forced to assume:** `// ASSUMPTION: doubling applies to the current PointsOf value, whatever it presently is`

**96.** "Add a wild card."
→ **Ask:** "Wild for scoring, for hand classification, for legality (what you're allowed to play) — or all three?" **Why it's ambiguous:** "wild" has meant three completely different things across the games in this kit (a wild 8 changes what's LEGAL to play; a wild joker changes hand CLASSIFICATION; neither one, by default, changes points).
→ **If forced to assume:** `// ASSUMPTION: wild applies to classification only, matching how jokers-wild worked in Mock 3`

**97.** "The best hand wins now," said mid-interview, after you'd already built a scoring (sum-of-points) game, not a classification game.
→ **Ask:** "Do you want a full switch to hand-classification (pairs, three of a kind, etc.), or just relabel what 'wins' means while keeping the scoring I already have?" **Why it's ambiguous:** this phrase is the EXACT wording used for a totally different game shape (Best Hand) — hearing it after building High Score should make you suspicious you're being asked to pivot, not just rename something.
→ **If forced to assume:** `// ASSUMPTION: keeping the existing scoring shape; "best hand" here just means highest ScoreHand, not a full redesign`

**98.** "A new player joins mid-game."
→ **Ask:** "Are they dealt a fresh hand starting now, or does the whole hand restart for everyone?" **Why it's ambiguous:** both are plausible "clean" answers, and they have very different implementation costs — one is a few new lines in `Deal`, the other means undoing everyone's progress.
→ **If forced to assume:** `// ASSUMPTION: new player gets a hand dealt starting now; everyone else's hand is untouched`

**99.** "Cards are dealt face up now."
→ **Ask:** "Does this change any game RULE, or is it only about what gets printed/narrated?" **Why it's ambiguous:** "face up" sounds like a rule change but very often is purely cosmetic — many candidates lose time rewriting `Deal` or hand-visibility logic for something that only ever needed a print-statement change.
→ **If forced to assume:** `// ASSUMPTION: display only — no method other than the print/ToString path changes`

**100.** "It's a tie," said with no other context, after several unrelated mutations have already landed.
→ **Ask:** "Tied in score, in category (like Best Hand's classification), or in trick count?" **Why it's ambiguous:** by this point in a real interview you likely have MULTIPLE systems that could produce a "tie" (score totals, hand categories, points won) — resolving the wrong one wastes the whole exchange.
→ **If forced to assume:** `// ASSUMPTION: "tie" refers to whichever system the two most recent mutations were about`
