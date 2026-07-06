# Mock Exam 4 - "Blackjack Lite" (target total + soft aces)

This one practices a different scoring shape: the best legal total under a target, not just "sum and compare." The key method is `BestTotal(hand)`.

Mind-map first: in `10-mind-map-and-mental-code.md`, read "Mock 4 mind map: Blackjack Lite" before starting the timer.

## Plain English version

This mock is about getting close to a target number without going over.

The hard part is ace scoring:

- Ace can be 1.
- Ace can also be 11.
- Use the best total that does not go over the target.

Simple example:

`AH 6D` can be 7 or 17. Since 17 is still under 21, the best total is 17.

The most important method is `BestTotal(hand)`. Rule changes usually affect ace logic, dealer hit logic, target number, or winner logic.

## How to run
- Same rules as Mock 1: strict 60:00 timer, reveal parts only at the gates, narrate out loud, run every 2-3 minutes.
- Start from a blank `Program.cs`. Use the usual skeleton, then build the game logic on top.
- Do not overbuild casino blackjack. Implement only the rules in the prompt.

---

## PART 1 - reveal at 0:00 (target: demo green by 0:12)

> Model the usual foundation:
> - `Card` with rank and suit. Ranks low-to-high: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, JOKER.
> - Suits: clubs, diamonds, hearts, spades. Jokers have no suit.
> - Display like `QD`, `10H`, or `JOKER`.
> - Build a standard 52-card deck, shuffle it, draw one card, draw n cards.
> - Demonstrate: print deck size, shuffle, draw 5, show remaining count.

*(Good questions: no jokers for now, correct? Letter display okay? Ace low for ordering, even though scoring will treat it specially?)*

---

## PART 2 - reveal when Part 1 runs (target: green by 0:38)

> Build **Blackjack Lite**:
> - Two participants: `Player` and `Dealer`.
> - Deal 2 cards to each, alternating one card at a time.
> - Card points: number cards = face value, J/Q/K = 10.
> - An ace may count as 1 or 11. Choose the highest hand total that is <= 21. If every total is over 21, use the lowest total.
> - The player hits until their best total is at least 17.
> - The dealer hits until their best total is at least 17.
> - Bust means total > 21. If both bust, no winner. If one busts, the other wins. Otherwise, higher total wins; equal totals tie.
> - Print both hands, both totals, and the winner.

*(Questions worth asking: dealer hits on exactly 17 or stands? For this part, stand on 17. What happens if both bust? For this part, no winner.)*

Design target:
- Put single-card point logic in `BasePoints(Card)`.
- Put ace handling in `BestTotal(Player)`.
- Put outcome logic in `Winner()`.

---

## PART 3 - mutations, one at a time from 0:38

**M1 (0:38):**
> Rule change: the dealer now hits on **soft 17**. A soft 17 is a total of 17 where at least one ace is currently counted as 11.

*(Route: dealer hit policy, not card scoring. Add `IsSoftTotal(hand, 17)` or make `BestTotal` return enough info.)*

**M2 (0:43):**
> New rule: **5-card charlie**. Any non-busted hand with 5 or more cards wins immediately, even against 21. If both have 5-card charlie, compare totals as normal.

*(Route: winner resolution. Do not scatter this rule through the hit loop unless you must stop drawing early.)*

**M3 (0:48):**
> Add both jokers to the deck. A joker is worth **0** points and does not help create a soft hand.

*(Route: deck constructor flag plus `BasePoints`. Ace logic should not change.)*

**M4 (0:53 - bonus):**
> The target changes from 21 to **24**. Dealer still stands on hard 17, still hits soft 17. Use the same code shape with a `Target` field or parameter.

*(Route: replace magic number `21` with one named value. If this takes more than one or two edits, note where the constant leaked.)*

---

## Dry run example

Part 2 sample hands:

- Player: `AH 6D`
- Dealer: `10C 7S`

Player total:
- Ace can be 1 or 11.
- `AH 6D` can be 7 or 17.
- Best total <= 21 is 17, so player stands.

Dealer total:
- `10C 7S` is 17, so dealer stands.
- Equal totals mean tie.

Soft 17 after M1:
- Dealer has `AH 6D`.
- Total is 17 only because ace is 11, so it is soft 17.
- Dealer must hit.

Joker after M3:
- `JOKER AH 6D` is still best total 17, because joker is 0 and does not create softness.

This mock is about keeping `BestTotal`, dealer hit policy, and winner resolution separate.

## Afterwards
1. Grade with the rubric in `06-practice-plan.md`.
2. Check whether the target number, ace handling, dealer policy, and winner rules each had one obvious home.
3. Ask yourself: did `BestTotal` stay understandable after mutations, or did ace logic leak into printing and winner code?
