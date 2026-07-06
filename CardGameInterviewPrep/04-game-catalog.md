# 04 — The Game Catalog (everything they can plausibly ask)

Every game below can be built on the same skeleton (`Card`, `Deck`, `Player`, one game class). Tier A games are the ones most likely to show up in Part 2 of a 60-minute, 3-part screen — drill these. Tier B games are possible. Tier C games are here just so nothing on the day feels totally new.

If you have trouble picturing a game, read `10-mind-map-and-mental-code.md` first. It breaks each game family down into objects, state, one action, rule homes, and an end condition.

## Simple version

Don't try to memorize every card game by name. Instead, learn the common **shapes**:

1. **High Score:** deal cards, add up points, highest total wins.
2. **Battle / War:** players flip cards each round; the stronger card wins the round.
3. **Best Hand:** figure out what the hand is — like a pair or three of a kind.
4. **Blackjack Lite:** get as close to a target number as you can without going over.
5. **Crazy Eights Lite:** you can only play a card if it matches the rank or suit.
6. **Trick Taking:** each player plays one card, then the best card wins the "trick."

When you read a prompt, first ask: "Which shape is this?" Then build the methods that match that shape.

Quick example:

If the prompt says "must follow suit," it's Trick Taking. You'll need `LegalCards` and `WinnerOfTrick`.

---

## Tier A — drill these until they're boring

### A1. High Score (deal & add up) — *the classic; Mock 1*
- **Rules:** deal K cards to N players; a hand's score = sum of its card points; highest total wins.
- **Loop:** `Deal(5)` → `ScoreHand` for each player → `Winners()` → print.
- **Tests you on:** keeping ordering and points separate, and handling ties.
- **Common changes they'll ask for:** face-card values change (11/12/13 ↔ all 10) · one suit doubles or goes negative · jokers join with fixed points · lowest total wins · tie → each tied player draws a card · "only your best 3 of 5 cards count."

### A2. War / Battle (compare one card per round) — *Mock 2*
- **Rules:** 2 players split the deck; each round both flip their top card; the stronger rank takes both; play N rounds; whoever won the most cards wins.
- **Loop:** `for round in 1..N: a=pileA.Draw(); b=pileB.Draw(); compare Strength; award`.
- **Tests you on:** the comparator, the round loop, and tracking piles (your hand vs. the cards you've won).
- **Common changes they'll ask for:** ace flips to high · a tie triggers a "war" (1 card down + 1 up, winner takes all, repeats) · suits start breaking ties (which **replaces** the war rule — removing behavior is a skill too) · play until the piles are empty · jokers beat everything · two jokers clash (no suit → discard).

### A3. Best Hand (classification) — *Mock 3*
- **Rules:** deal 5 cards to each of 4 players; Three of a Kind > One Pair > High Card; if two players have the same category, the higher set rank wins.
- **Key trick:** `hand.GroupBy(c => c.Rank)` then look at the group sizes. Store category strength as **an ordered list kept as data** (a list or int), so adding "Two Pair" later means renumbering one line — not rewriting all your comparisons.
- **Tests you on:** classification and comparing multi-part results (category, then rank, then kicker).
- **Common changes they'll ask for:** add Two Pair · Flush beats everything (`GroupBy(Suit)`) · jokers are wild (count as a copy of your most common rank — say the simplification out loud) · kicker comparison · straights (be careful: ace is low).

---

## Tier B — read the loop shape once, be ready

### B1. Blackjack-lite (21)
- **Practice mock:** `mocks/mock4.md`.
- Deal 2 cards, add up toward 21, A = 1 **or** 11 (count your aces, add 10 if it still fits), J/Q/K = 10; the player hits based on a strategy, the dealer hits while under 17; going over = bust = lose.
- **Tests you on:** the flexible-ace math — write `BestTotal(hand)` as one method.
- **Changes:** dealer hits on soft 17 · 5-card charlie wins · jokers = 0 or a blackjack wildcard · target changes to 24.

### B2. Crazy Eights / matching-shedding (UNO with real cards)
- **Practice mock:** `mocks/mock5.md`.
- Deal 5 each, flip one card to a discard pile; on your turn, play a card that matches the top card's **rank or suit**, otherwise draw; first player to empty their hand wins.
- **Tests you on:** the `IsPlayable(card, top)` check, rotating turns, and running out of draw cards (reshuffle the discards!).
- **Changes:** 8s are wild (choose a suit) · jokers skip the next player · 2s force a draw-two · reverse direction (turn order = index math — keep it in one place).
- **C# trap:** never remove from a `List` you're looping over with `foreach`. Find the card first, then remove it by reference after the loop.

### B3. Trick-taking lite (Whist)
- **Practice mock:** `mocks/mock6.md`.
- 4 players, deal out all the cards; the lead player plays a card, everyone else must follow that suit if they can; the highest card of the **led suit** wins the trick — unless a **trump** suit was set.
- **Tests you on:** this is where suit ordering and "must follow suit" legality live.
- **Changes:** trump suit changes each round · jokers are the highest trumps · score by how many tricks you won.

---

## Tier C — one-line shapes so nothing feels alien

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

---

## The big pattern (why drilling Tier A covers everything)

Every card game boils down to the same five decisions. When you see ANY new rules on the day, map them to these before you write code:

1. **Setup** — what's in the deck, how many cards go to whom → `Deck` constructor + `Deal`
2. **Turn structure** — all at once (war), rotating (eights), or none (high score) → the one play loop
3. **Legality** — what is a player allowed to do → `IsPlayable` check (in many games, everything is legal)
4. **Resolution** — who takes the trick / cards / points → a comparator or classifier
5. **End + winner** — when does it stop, who won → loop condition + `Winners`

If you can name where each of these five lives in your file, you can absorb any change they throw at you.

## Walk-through: how to spot the game shape

When you read a prompt, ignore the game's name at first and figure out its shape:

Prompt: "Each player gets 5 cards. Best pair or high card wins."
- Shape: hand classification.
- Methods you'll need: `ClassifyHand`, `CompareHands`, `Winners`.
- Closest mock: `mocks/mock3.md`.

Prompt: "Players take turns playing a card that matches the rank or suit."
- Shape: matching/shedding.
- Methods you'll need: `IsPlayable`, `TakeTurn`, turn-index update.
- Closest mock: `mocks/mock5.md`.

Prompt: "Everyone plays one card; the highest card of the led suit wins."
- Shape: trick taking.
- Methods you'll need: `LegalCards`, `WinnerOfTrick`, leader update.
- Closest mock: `mocks/mock6.md`.

This step should take less than 30 seconds. It tells you which methods to create before you start writing code.
