# Mock Exam 6 - "Trick Taking Lite" (follow suit + trump)

This one practices per-turn legality, led suit, trick resolution, and a trump mutation. The key methods are `LegalCards(player, ledSuit)` and `WinnerOfTrick(plays)`.

Mind-map first: in `10-mind-map-and-mental-code.md`, read "Mock 6 mind map: Trick Taking Lite" before starting the timer.

## Plain English version

This mock is about following suit and winning a trick.

One player leads with a card. That card's suit becomes the led suit. Other players must play that suit if they have it.

Simple example:

Alice leads `7H`, so hearts are led.

If Bob has `2H QS`, Bob must play `2H`. He cannot play `QS` because he has a heart.

After everyone plays one card, the best allowed card wins the trick.

The most important methods are `LegalCards` and `WinnerOfTrick`. Rule changes usually affect trump, ace order, or joker rules.

## How to run
- Same rules as Mock 1: strict 60:00 timer, reveal parts only at the gates, narrate out loud, run every 2-3 minutes.
- Start from a blank `Program.cs`. Use the usual skeleton first.
- Use a deterministic strategy: each player plays the lowest legal card by rank strength.

---

## PART 1 - reveal at 0:00 (target: demo green by 0:12)

> Build the usual foundation:
> - `Card`, `Deck`, `Shuffle`, `Draw`, `Draw(n)`.
> - Standard 52-card deck, no jokers for now.
> - Display like `QD`, `10H`, or `JOKER`.
> - Demonstrate drawing 5 cards and printing the remaining count.

*(Good questions: no jokers for now? Ace low, per the intro doc? Letter display okay?)*

---

## PART 2 - reveal when Part 1 runs (target: green by 0:38)

> Build **Trick Taking Lite**:
> - 4 players.
> - Deal 5 cards to each.
> - Play 5 tricks.
> - The leader plays first. For trick 1, Player 0 leads. After that, the previous trick winner leads.
> - The suit of the first card played is the **led suit**.
> - Each later player must follow the led suit if they have at least one card of that suit. If they cannot, they may play any card.
> - No trump suit for now.
> - The highest-ranked card of the led suit wins the trick. Ace is low.
> - Each trick winner gets 1 point. After 5 tricks, highest score wins. Ties possible.
> - Print each trick's plays and winner.

*(Questions worth asking: deterministic card choice okay? What if players tie on points? For this part, tied players share the win.)*

Design target:
- `LegalCards(Player p, string ledSuit)` owns follow-suit legality.
- `ChooseCard(Player p, string ledSuit)` owns the simple strategy.
- `WinnerOfTrick(List<Play> plays, string ledSuit)` owns trick resolution.
- A `Play` can be a tiny class/record holding player and card, or a tuple if that is faster.

---

## PART 3 - mutations, one at a time from 0:38

**M1 (0:38):**
> Rule change: spades are now **trump**. Any spade beats any non-spade. If multiple spades are played, highest spade wins. If no spades are played, highest card of the led suit still wins.

*(Route: `WinnerOfTrick`. Follow-suit legality does not change.)*

**M2 (0:43):**
> New rule: the trump suit changes every trick in this cycle: C, D, H, S, then repeat.

*(Route: a `TrumpSuitForTrick(trickNumber)` helper or one array. Do not hard-code spades in several branches.)*

**M3 (0:48):**
> New rule: aces are now HIGH for trick resolution.

*(Route: `Ranks.Order`. Do not touch scoring or follow-suit logic.)*

**M4 (0:53 - bonus):**
> Add both jokers. A joker can always be played, even if the player could follow suit. A joker is the highest trump. If two jokers are played in the same trick, the first joker played wins.

*(Route: deck flag, legality exception, and `WinnerOfTrick`. Joker has no suit, so guard every suit comparison.)*

---

## Dry run example

Part 2 sample trick:

- Alice leads `7H`, so led suit is hearts.
- Bob has `2H QS 9D`, so Bob must play a heart. With lowest-legal strategy, Bob plays `2H`.
- Cara has no hearts, so Cara may play anything.
- Dan has `KH 3C`, so Dan must play `KH`.

Winner without trump:
- Only led-suit cards can win.
- Hearts played: `7H`, `2H`, `KH`.
- `KH` is highest, so Dan wins the trick and leads next.

After M1, spades are trump:
- If Cara could not follow suit and played `3S`, that spade beats every heart.
- If two spades are played, highest spade wins.

After M4, joker:
- A joker can always be played.
- First joker wins if multiple jokers appear in the same trick.

This mock is about keeping follow-suit legality separate from trick-winning comparison.

## Afterwards
1. Grade with the rubric in `06-practice-plan.md`.
2. Check whether follow-suit legality and trick-winning comparison stayed separate.
3. If the trump mutation made you edit more than `WinnerOfTrick` plus one trump helper, your comparison rule was probably scattered.
