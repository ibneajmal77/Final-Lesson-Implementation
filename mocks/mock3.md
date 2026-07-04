# Mock Exam 3 — "Best Hand" (classification + wildcards)

The hardest of the three: hand **classification**, an ordered category ladder, and joker **wildcards**. If you can do this one calmly, nothing on the real day will scare you.

Mind-map first: in `10-mind-map-and-mental-code.md`, read "Mock 3 mind map: Best Hand" before starting the timer.

## Plain English version

This mock is about recognizing patterns inside a hand.

You are not adding points. You are asking: "What kind of hand is this?"

Examples:

- `7H 7S 7D QC 2H` means Three of a Kind.
- `KH KS 4D 3C 2H` means One Pair.
- `AH 5D 9S JC QH` means High Card.

The most important method is `ClassifyHand`. It should return a result that can be compared against other players' results.

Rule changes usually add a new category, like Two Pair or Flush.

## How to run
Same rules: 60:00 strict, gate the reveals, narrate out loud. Reference solution from Claude after your attempt.

---

## PART 1 — reveal at 0:00 (target: green by 0:12 — you've done this four times now)

> The usual foundation: Card, 52-card deck, shuffle, draw one / draw n, demo.

---

## PART 2 — reveal when Part 1 runs (target: green by 0:38)

> Build **Best Hand**:
> - 4 players, 5 cards each.
> - Hand categories, best to worst: **Three of a Kind** > **One Pair** > **High Card**.
> - The player with the best category wins. Same category → the higher *defining* rank wins (the rank of the triple/pair, or the highest card for High Card). Ace is low. Still tied → shared win.
> - Print each player's hand and its detected category, e.g. `Bob:  7H 7S 7D QC 2H  ->  Three of a Kind (7)`, then the winner.

**Design hints (allowed — this is training):**
- `hand.GroupBy(c => c.Rank)` + group sizes does all detection: any group of 3 → trips; of 2 → pair.
- Represent the category ladder as **data** — e.g. an ordered list of names, category strength = index (exactly the `Ranks.Order` trick again). Evaluate a hand to `(categoryStrength, definingRankStrength)` and compare tuples. Then M1 below costs one inserted line.

---

## PART 3 — mutations, one at a time from 0:38

**M1 (0:38):**
> New category: **Two Pair**, between One Pair and Three of a Kind. Between two Two-Pair hands, the higher top pair wins.

**M2 (0:43):**
> New category: **Flush** — all 5 cards the same suit — beats **everything**.

**M3 (0:48):**
> Add both jokers to the deck. A joker is **wild**: it counts as another copy of the rank you already hold most of. (A hand with a pair of 9s and a joker = three 9s.)

*(A fully general "best possible use of a joker" is out of scope in 5 minutes — implement the stated simplification and SAY the trade-off: "joker joins the most frequent rank; a general optimizer would try all ranks — noting that aloud and moving on.")*

**M4 (0:53 — bonus):**
> Full tie on category **and** defining rank → compare the highest remaining card (the kicker). Still equal → share the win.

---

## Dry run example

Part 2 sample hands:

- Alice: `7H 7S 7D QC 2H` -> Three of a Kind, defining rank 7.
- Bob: `KH KS 4D 3C 2H` -> One Pair, defining rank K.
- Cara: `AH 5D 9S JC QH` -> High Card, defining rank Q if ace is low.

Winner:
- Three of a Kind beats One Pair.
- Alice wins even though Bob's pair is kings.

After M1, Two Pair exists:
- `KH KS 4D 4C 2H` becomes Two Pair.
- It beats One Pair but loses to Three of a Kind.

After M3, joker wild:
- `9H 9S JOKER 3C 2D` should become Three of a Kind, because the joker joins the most frequent rank: 9.

This mock is about turning a hand into a comparable result like `(categoryStrength, definingRankStrength)`.

## Afterwards
Rubric, out loud. The specific things to check against the reference (ask Claude for it):
- Was the category ladder **data** (insertable) or an if/else chain (surgery)?
- Did detection stay in ONE method that returns a comparable result, with printing kept separate?
- Did the joker mutation touch only the detection method, or leak everywhere?
