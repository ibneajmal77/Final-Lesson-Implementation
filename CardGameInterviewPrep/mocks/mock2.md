# Mock Exam 2 — "Battle" (war-style rounds)

Different muscle than Mock 1: a **round loop**, pile bookkeeping, comparator changes, and — the key lesson — **replacing** a rule instead of adding one.

Mind-map first: in `10-mind-map-and-mental-code.md`, read "Mock 2 mind map: Battle / War" before starting the timer.

## Plain English version

This mock is about rounds.

Each round:

1. Alice flips one card.
2. Bob flips one card.
3. The stronger card wins.
4. The winner keeps the cards.

The most important method is the card comparison method. Rule changes usually change how two cards are compared.

Simple example:

`9H` vs `QD`: queen is stronger, so Bob wins the round if Bob flipped `QD`.

If ranks tie, the prompt tells you what to do: discard, war, or suit tie-break.

## How to run
Same rules as Mock 1: 60:00 strict, reveal at the gates, narrate out loud, run every 2–3 minutes. Reference solution available from Claude **after** your attempt.

---

## PART 1 — reveal at 0:00 (target: green by 0:15)

> Same foundation as always: Card (rank + suit, display like `QD`, joker displays `JOKER`), standard 52-card deck, shuffle, draw one / draw n. Demonstrate it works.

*(By Day 5 this should take you ≤10 minutes without thinking.)*

---

## PART 2 — reveal when Part 1 runs (target: green by 0:38)

> Build the game **Battle**:
> - 2 players. Shuffle, then deal the entire deck evenly (26 cards each) into each player's **draw pile**.
> - Play **10 rounds**. Each round: both players flip the top card of their draw pile. The higher-ranked card (ace low, per the intro) wins; the winner puts **both** cards into their separate **won pile**.
> - If the ranks are equal, both cards go to a shared **discard pile**.
> - Print each round like: `Round 3: Alice 9H  vs  Bob QD  ->  Bob`
> - After 10 rounds: the player with the most cards in their won pile wins the game. Ties possible — say how you handle it.

*(Note the state per player: draw pile AND won pile. Keep them as two lists on the player — don't overthink it.)*

---

## PART 3 — mutations, one at a time from 0:38

**M1 (0:38):**
> Rule change: **aces are now HIGH** — above K.

*(One-line edit if your ordering is data. Watch your checks: "ace is low" must flip.)*

**M2 (0:43):**
> Equal ranks no longer discard. They trigger a **war**: each player places one card face down, then flips one more card — the new flip decides, and the winner takes **all six** cards. If the flips tie again, repeat. A player who runs out of cards during a war **loses the game immediately**.

**M3 (0:48):**
> **Replace** the war rule: no more wars. Ties are now broken by **suit**: C < D < H < S (spades strongest). Delete the war behavior — don't leave dead code.

*(This is the "suits gain an order" moment from the intro doc — a new 4-entry array mirroring `Ranks`, plus one extra comparison level.)*

**M4 (0:53 — bonus):**
> Play until the draw piles are **empty** instead of 10 rounds. Also add both jokers when building the deck: a joker beats everything. If two jokers collide, the suit rule can't apply (jokers have no suit) — discard both.

---

## Dry run example

Part 2 sample rounds:

Round 1:
- Alice flips `9H`.
- Bob flips `QD`.
- Q outranks 9, so Bob puts both cards into Bob's won pile.

Round 2:
- Alice flips `7S`.
- Bob flips `7C`.
- Equal rank, so both cards go to the shared discard pile.

After M1, aces are high:
- `AS` beats `KD`.
- The only intended edit is moving `A` in `Ranks.Order`.

After M3, suit breaks ties:
- Alice flips `7S`, Bob flips `7C`.
- Same rank, compare suits: C < D < H < S.
- Alice wins because spades are strongest.

This mock is about keeping one comparison method clean while the tie rule changes.

## Afterwards
Rubric in `06`, out loud. Then ask Claude for the reference solution and compare **homes**: did rank order live in one array? Did M3 actually delete the war code? Did the comparator stay in one method through all four mutations?
