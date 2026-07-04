# Mock Exam 1 — "High Score" (the classic shape)

Run this one first. It is the highest-probability Part-2 shape for this interview.

Mind-map first: in `10-mind-map-and-mental-code.md`, read "Mock 1 mind map: High Score" before starting the timer.

## Plain English version

This mock is about the simplest card-game shape:

1. Give each player cards.
2. Convert each card into points.
3. Add each player's points.
4. Highest total wins.

The most important method is `PointsOf(Card)`. Most rule changes in this mock change how one card scores.

Simple example:

If Alice has `AH 10D`, her score is 1 + 10 = 11 before diamond rules. If diamonds double, `10D` becomes 20, so Alice becomes 21. The hand did not change. Only the scoring rule changed.

## How to run
- **Best:** new Claude session → *"Act as my FF card-game interviewer. Use mocks/mock1.md. 60 minutes, reveal parts on schedule, drop mutations one at a time, then grade me with the rubric in 06-practice-plan.md."*
- **Solo:** strict 60:00 timer. Reveal each section only at its time gate. Speak your narration out loud anyway — the talking is half the exam. One file, run every 2–3 minutes.
- Do **not** open `csharp/Mock1Solution` until you're done.

---

## PART 1 — reveal at 0:00 (target: demo green by 0:15)

> Model a playing card and a deck.
> - A card has a rank and a suit. Ranks low→high: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, JOKER. Suits: clubs, diamonds, hearts, spades. Jokers have no suit.
> - Display a card as rank + suit (e.g. `QD` or `Q♦`); a joker displays as `JOKER`.
> - Build a standard 52-card deck (no jokers for now). Support: shuffle, draw one card, draw n cards.
> - Demonstrate: print the deck size, shuffle, draw 5 cards and show them, show the remaining count.

*(Good clarifying questions here: jokers out for now, confirmed? Letter display okay? Ace low, per the intro doc?)*

---

## PART 2 — reveal when your Part 1 demo runs (target: green by 0:38)

> Now build the game **High Score**:
> - 3 players. Deal 5 cards to each (round-robin).
> - Card points: A=1, number cards = face value, J=11, Q=12, K=13.
> - A hand's score is the sum of its card points. The highest hand wins.
> - Print each player's hand and score, then announce the winner.
> - If players tie for the best score, they all win (for now).

*(Questions worth asking: exact output format? tie = shared win, confirmed?)*

---

## PART 3 — mutations. Reveal ONE at a time, ~5 minutes apart, starting 0:38.

**M1 (0:38):**
> Rule change: J, Q and K are now each worth **10** points.

**M2 (0:43):**
> New rule: **diamond** cards count **double**.

**M3 (0:48):**
> Add both jokers to the deck. A joker is worth **20** points.

**M4 (0:53 — bonus if time):**
> Ties are no longer shared: each tied player draws **one extra card** and scores are compared again. Repeat until there is a single winner. If the deck runs out, the remaining tied players share the win.

Apply the R5 ritual (`05`) to every mutation: Restate → Route → Red (update the check, see it fail) → Rewrite → Rerun + report.

---

## Dry run example

Part 2 sample hands:

- Alice: `AH 10D 3S 4C 2H`
- Bob: `KS 2C 5D 6H 7S`
- Cara: `QD JC 2D 3H 4S`

Before mutations:
- Alice = 1 + 10 + 3 + 4 + 2 = 20.
- Bob = 13 + 2 + 5 + 6 + 7 = 33.
- Cara = 12 + 11 + 2 + 3 + 4 = 32.
- Bob wins.

After M1, J/Q/K are 10:
- Bob = 10 + 2 + 5 + 6 + 7 = 30.
- Cara = 10 + 10 + 2 + 3 + 4 = 29.

After M2, diamonds double:
- Alice's `10D` becomes 20, so Alice = 30.
- Bob's `5D` becomes 10, so Bob = 35.
- Cara's `2D` becomes 4, so Cara = 31.

This is why scoring belongs in `PointsOf`: the hands did not change, only the scoring rule changed.

## Afterwards
1. Final run; score yourself with the `06` rubric, out loud.
2. Close the interview properly, as practice: *"With more time I'd …"* (one sentence).
3. Open `csharp/Mock1Solution/Program.cs` + `NOTES.md`. Compare **where** your mutations landed, not just whether they work. Same homes as the reference = the design skill is sinking in.
4. Optional: ask Claude — *"Review my mock 1 attempt against the reference and the rubric"* (paste your code).
