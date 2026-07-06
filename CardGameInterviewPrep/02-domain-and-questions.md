# 02 — The Card Domain + Clarifying-Question Bank

## Simple version

A single card carries three different ideas. People mix them up all the time, so keep them apart in your head:

1. **Rank order** = how strong a card is. Example: a Q beats a 7.
2. **Points** = how many score points a card is worth. Example: a Q could be worth 12 in one game and 10 in another.
3. **Suit** = the symbol: C, D, H, or S. Suits usually have no "strength" order — unless the game says they do.

Keep these three ideas separate in your code too.

Quick example:

`QD` means "queen of diamonds."
- Its **rank** is Q.
- Its **suit** is D.
- Its **points** depend on which game you're playing.

So when a rule changes, ask yourself which idea it touches:
- "A queen is worth 10" → that's **points**.
- "A queen beats a jack" → that's **rank order**.
- "Diamonds score double" → that's a **scoring rule**.

## Things to memorize about the card domain

**Rank is not the same as points.** This is the most important idea in the whole prep:

- **Ordering (strength)** answers "which card wins?" → keep it in ONE array: `Ranks.Order`. The default from their PDF is: `A 2 3 4 5 6 7 8 9 10 J Q K JOKER` (ace is LOW).
- **Points (score)** answers "how much is this card worth?" → keep it in ONE method: `PointsOf(card)`. Each game sets its own values (in some games J/Q/K = 10, in others they're 11/12/13).

Almost every rule change touches only ONE of these two. If your code mixes them together, every small change becomes a big rewrite.

**Suit** — just a set of 4 with no order: ♣ ♦ ♥ ♠ (C, D, H, S). Don't compare suits until a rule forces you to. When that happens, add a `Suits.Strength` array, the same way you did for ranks.

**Joker** — it has a rank but **no suit** (set suit to `null`). Handle it as a special case in three places:
- Display: show it as `"JOKER"`.
- Building the deck: leave it out unless asked (default count is 2).
- Suit rules: a joker can never count as "a diamond."

**Deck** — be ready for different setups: standard 52 · with jokers 54 · several decks combined · stripped decks (e.g. "remove all the 2s"). Handle all of these with **constructor parameters** — never make new classes for them.

**Shuffle** — use Fisher–Yates (only 4 lines, and every possible order is equally likely). Allow a seed so you can reproduce the same shuffle while debugging — and say out loud that you'd remove the seed for a real game.

**Deal** — two styles:
- **Round-robin**: one card to each player, then go around again.
- **Block**: give each player all 5 cards at once.

After a fair shuffle, both give the same odds. Say that out loud, pick round-robin (it's what a real dealer does), and move on. Any leftover cards just stay in the deck.

**Running out of cards** — three ways to handle it:
- Throw an error (the starter default — fail loudly).
- Reshuffle the discard pile.
- End the game.

Don't pick one up front. Ask **only when it actually matters** in the game.

## The question bank

★ = if you only get to ask five questions in the whole interview, ask these five.

**Deck & setup (ask during Part 1 — keep it under ~60 seconds)**
- ★ "Jokers in the deck for this part, or a standard 52?" (Their PDF contradicts itself on 13 vs 14, so this is a fair question.)
- ★ "Is letter display okay — `QD`, `10H`, `JOKER` — or do you want the symbols?"
- "Just one deck, right?" (only ask if something hints otherwise)

**Ordering (Part 1, or the first time you compare cards)**
- ★ "Confirming from the intro doc: ace is LOW in this game?"
- "Joker beats king, like the doc says?"

**Scoring (ask when Part 2 starts — not before)**
- ★ "Point values: is A=1? Are J, Q, K = 11/12/13, or all 10? What about the joker?"
- "Highest total wins, correct?"

**Ties (Part 2)**
- ★ "If two players tie for best, do they both win, or is there a tie-breaker?"

**Game flow (Part 2, only if there's a loop)**
- "Fixed number of rounds, or play until the deck/piles run out?"
- "If the draw pile empties mid-game: reshuffle the discards, or stop?"

**Output**
- "Do you want an exact output format, or is a readable summary fine?"

## How to ask questions well

1. **Read the whole part first, then restate it in one sentence.** For example: *"So: deal five cards to three players, add up the values, highest sum wins — right?"* They actually grade you on this restatement.
2. **At most ~3 questions per part, ~90 seconds total.** Their doc says plainly: don't waste time on preamble.
3. **Ask each question when its part arrives.** Asking scoring questions during Part 1 just wastes your own time.
4. **If they say "up to you":** pick the simplest option, say it out loud, and write it as a comment — `// assume: tied players share the win`. Interviewers grade whether you're **clear about it**, not which option you pick. A written assumption is also a note you can find again 20 minutes later.

## Safe defaults (when they say "your choice")

| Question | Default | Why it's safe |
|---|---|---|
| Jokers? | Leave them out; add a constructor flag | Matches "13 ranks / 52 cards"; the flag makes adding them later easy |
| Joker count | 2 | Their PDF image shows exactly 2 |
| Ace | LOW | Their doc says so directly |
| Display | Letters `QD` | Fast to type; symbols are just cosmetic |
| Deal style | Round-robin | What a real dealer does; same odds after a shuffle anyway |
| Ties | All tied players win (return a list) | Simplest correct behavior; easy to upgrade to a tie-breaker |
| Empty deck | Throw a clear error | Failing loudly beats corrupt data; easy to switch to reshuffle later |
| Leftover cards | Stay in the deck | No rule uses them |

## Walk-through: rank, points, and suit are all different

Hand: `AD QD 5H`.

Default high-score points:
- `AD`: rank is ace, strength is low, worth 1 point.
- `QD`: rank is queen, strength is above jack, worth 12 or 10 points depending on the game.
- `5H`: strength is the 5's spot in `Ranks.Order`, worth 5 points.

Now a rule change: "diamonds count double."
- `AD` becomes 2 points.
- `QD` becomes 24 (if Q=12) or 20 (if face cards are 10).
- `5H` stays 5 (it's a heart, not a diamond).

Notice what **didn't** change: the rank order. A queen still beats a 5. Only the scoring changed — so the only thing your code should change is `PointsOf(Card)`.
