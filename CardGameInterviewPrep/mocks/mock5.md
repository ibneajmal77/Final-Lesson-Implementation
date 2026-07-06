# Mock Exam 5 - "Crazy Eights Lite" (matching + turn order)

This one practices legality predicates, draw/discard piles, and turn rotation. The key method is `IsPlayable(card, topCard)`.

Mind-map first: in `10-mind-map-and-mental-code.md`, read "Mock 5 mind map: Crazy Eights Lite" before starting the timer.

## Plain English version

This mock is about turns and legal moves.

On your turn, you look at the top discard card. You may play a card if it matches rank or suit.

Simple example:

Top card is `9H`.

Your hand is `2C 5H QS 9D`.

Playable cards:

- `5H`, because it matches hearts.
- `9D`, because it matches rank 9.

The most important method is `IsPlayable(Card card, Card top)`. Rule changes usually add special card effects like wild 8, skip, draw two, or reverse.

## How to run
- Same rules as Mock 1: strict 60:00 timer, reveal parts only at the gates, narrate out loud, run every 2-3 minutes.
- Start from a blank `Program.cs`. Use the usual skeleton first.
- This is a simulation, not an interactive game. Let the program choose the first legal card in a player's hand.

---

## PART 1 - reveal at 0:00 (target: demo green by 0:12)

> Build the usual foundation:
> - `Card`, `Deck`, `Shuffle`, `Draw`, `Draw(n)`.
> - Standard 52-card deck, no jokers for now.
> - Display like `QD`, `10H`, or `JOKER`.
> - Demonstrate drawing 5 cards and printing the remaining count.

*(Good questions: standard 52 for now? Letter display okay? Ace low only matters if a later rule compares ranks.)*

---

## PART 2 - reveal when Part 1 runs (target: green by 0:38)

> Build **Crazy Eights Lite**:
> - 3 players.
> - Deal 5 cards to each.
> - Flip one card from the deck to start a discard pile. If it is an 8, just accept it; no special rule yet.
> - On a turn, the current player may play one card matching the discard top by **rank or suit**.
> - If they have multiple playable cards, play the first one in their hand.
> - If they have no playable card, draw one card. If the drawn card is playable, play it immediately; otherwise keep it.
> - First player with an empty hand wins.
> - Stop after 30 turns if nobody has emptied their hand; winner is the player with the fewest cards. Ties possible.
> - Print each turn: player name, action, discard top, and hand count.

*(Questions worth asking: deterministic strategy okay? What if deck runs out? For this part, stop drawing and continue only if players can play from hand.)*

Design target:
- `IsPlayable(Card card, Card top)` owns the matching rule.
- `TakeTurn(Player p)` owns one player's action.
- Turn order lives in one index update.
- Do not remove from a list inside a `foreach`; find the card first, then remove it.

---

## PART 3 - mutations, one at a time from 0:38

**M1 (0:38):**
> Rule change: 8s are **wild**. An 8 can be played on any top card. After playing an 8, the player chooses a suit. For this simulation, choose the suit they have the most of in hand; if tied, choose C, then D, then H, then S.

*(Route: `IsPlayable` plus a small `CurrentSuit` state. The discard top's printed rank can stay 8, but matching should use the chosen suit.)*

**M2 (0:43):**
> New rule: jokers are in the deck. A joker can be played on anything and forces the next player to skip their turn.

*(Route: deck flag, `IsPlayable`, and turn-advance logic. Joker has no suit, so do not use `card.Suit` blindly.)*

**M3 (0:48):**
> New rule: when a 2 is played, the next player must draw two cards and lose their turn.

*(Route: one pending penalty counter or action flag. Do not copy/paste skip logic in several places.)*

**M4 (0:53 - bonus):**
> Reverse direction when a queen is played. With 3 players, this changes who acts next.

*(Route: turn order only. Add `direction = 1` or `-1`; update the current index in one helper method.)*

---

## Dry run example

Part 2 sample state:

- Discard top: `9H`.
- Alice hand: `2C 5H QS 9D`.

Playable cards:
- `5H` matches suit H.
- `9D` matches rank 9.
- `2C` and `QS` do not match.

With the simple strategy, Alice plays the first playable card in hand order: `5H`.
The new discard top is `5H`.

After M1, 8s are wild:
- If Alice has `8C`, she may play it on any top card.
- Then she chooses a current suit from her remaining hand.

After M2, joker skip:
- If Alice plays `JOKER`, the next player loses their turn.
- The joker has no suit, so matching logic must not assume `card.Suit` exists.

This mock is about keeping `IsPlayable`, card effects, and turn movement separate.

## Afterwards
1. Grade with the rubric in `06-practice-plan.md`.
2. Check whether matching, special-card effects, draw-pile exhaustion, and turn order each had one obvious home.
3. Pay special attention to list mutation. If you removed while enumerating, fix that habit before the real interview.
