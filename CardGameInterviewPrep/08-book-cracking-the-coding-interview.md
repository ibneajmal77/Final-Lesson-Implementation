# 08 — Book Notes: "Cracking the Coding Interview" (Gayle Laakmann McDowell)

These are distilled notes oriented to the FF screen — what to take from the book and what to deliberately skip. If you own the book (6th edition), the pages worth real time are marked ★.

## Why FF recommends this book — the headline fact

Chapter 7 (Object-Oriented Design), **question 7.1, is "Deck of Cards"**: *design the data structures for a generic deck of cards, and explain how you would subclass them to implement blackjack.* That is essentially Part 1 of your interview plus a variant question. FF isn't recommending 700 pages of algorithms — they're pointing at this chapter.

## Plain English version

You do not need to study the whole book for this interview.

The useful parts are:

1. Object-oriented design, especially the deck-of-cards question.
2. Big O basics, so you can explain that deck operations are small and simple.
3. Testing habits, so you can prove your code works while coding.
4. Interview process habits, especially speaking clearly.

Simple idea:

The book may put card value inside a card subclass, like `BlackjackCard`. This kit usually puts value inside the game, like `PointsOf(Card)`, because the same card can be worth different points in different games.

Example: `QH` can be 12 in one game, 10 in another game, and only a rank comparison in Battle.

## Chapter relevance map

| Chapter | Topic | Relevance to FF screen | What to take |
|---|---|---|---|
| I–V (intro) | The process, behind the scenes, assessment | Medium | Interviewers grade the *process*: communication, structure, recovery from mistakes — matches FF's five axes exactly |
| VI | Big O | **High** | Enough to describe your own code's complexity confidently (see `07`) |
| 1 | Arrays & Strings | Medium | You live in lists and strings here; nothing exotic needed |
| 2 | Linked Lists | Low | Skip for this screen |
| 3 | Stacks & Queues | Medium | Piles ARE stacks/queues — know when each models a pile (see `07`) |
| 4 | Trees & Graphs | Low | Skip |
| 5 | Bit Manipulation | Low | Skip |
| 6 | Math & Logic Puzzles | Low | Skip (card probability trivia is possible small talk, not the exam) |
| **7** ★ | **Object-Oriented Design** | **Highest — this is the one** | The OOD method below + question 7.1 |
| 8 | Recursion & DP | Low | Only echo: "recursive war" in Mock 2 M2 — a simple self-call |
| 9 | System Design | Low | Skip |
| 10 | Sorting & Searching | Medium-low | Use the library sort with a key selector; never hand-roll |
| 11 ★ | Testing | **High** | Their testing mindset maps 1:1 to your `Check`-first discipline |
| Behavioral | Your stories | Medium | The 30-second intro; one project story in situation→action→result shape |

## The parts to actually study

### 1. The OOD method (chapter 7) — adapted to your interview

CtCI's approach to any object-oriented design question:

1. **Handle ambiguity** — the requirements are deliberately incomplete; ask who uses it and how. → This is your clarifying-question bank (`02`). In FF's format the "ambiguity" arrives as future rule changes, so the answer is designs that keep rules swappable (`03`).
2. **Define the core objects** — for cards this lands on exactly your skeleton: `Card`, `Deck`, `Player`, `Game`.
3. **Analyze relationships** — has-a vs is-a: Game *has* a deck and players; a variant game *is a* Game with one behavior overridden. Composition first (`07`).
4. **Investigate actions** — the verbs become methods: shuffle, draw, deal, score, resolve winners. Verbs that are *rules* (score, compare) get their own small methods, because rules change.

**Question 7.1's canonical answer vs your skeleton:** the book's solution makes `Card` abstract with a `value()` method and subclasses like `BlackjackCard` overriding it. Your skeleton reaches the same goal with a `virtual PointsOf(Card)` on the *game* instead — because in FF's format the game's rules change, not the card's identity. Both are defensible; be ready to say why yours puts the variability in the game: *"the card is a fact; what it's worth is a game rule, so the rule lives in the game."* If the interviewer steers toward subclassing cards, follow their steer without arguing.

### 2. Big O (intro chapter) — the six facts

O(1) indexed access · O(n) scans (`Sum`, `GroupBy`, Fisher–Yates) · O(n log n) sorting · `RemoveAt(0)` O(n) vs end O(1) · nested loops multiply · with n=52, say "linear in deck size" and move on. Deeper study of this chapter is not needed for this screen.

### 3. Testing (chapter 11) — their checklist, your habit

The book's method for "test this function": normal case → extremes (empty, one, many) → illegal input → state-dependent cases. Mapped to cards: fresh deck of 52 → empty deck draw throws → joker (the "illegal-looking" value) displays and scores → tie (the state case) returns multiple winners. You already run these as `Check` lines; the book gives you the vocabulary: *"let me cover the extreme cases before moving on."*

### 4. Process & behavioral chapters — three usable points

- Interviewers assess the path, not just the destination: a narrated wrong-turn-plus-recovery scores *better* than silent perfection. This is FF's "think aloud" axis in book form.
- Mistakes are recoverable if you catch them yourself — which is what the visible PASS/FAIL checks do for you.
- Prepare the 30-second intro (name, years, stack, what you build) and ONE project story shaped situation → action → result. FF's doc says don't linger here, so short and ready beats deep and improvised.

## What to consciously skip this week — and the reason

Trees, graphs, dynamic programming, bit manipulation, linked lists: FF's own prep doc says *"skip the algorithm tricks."* Every hour there is an hour not spent on cold-start drills and mocks, which is what this screen actually measures. If you keep interviewing elsewhere after FF, come back to those chapters then.

## If you only give this book 2 hours

1. Chapter 7 intro + question 7.1 and its solution (★, ~40 min)
2. Chapter 11 testing intro (~20 min)
3. Big O chapter, skim for the table and examples (~30 min)
4. "The Interview Process" intro chapters, skim (~30 min)

Everything else this week: your kit covers it closer to the actual exam.

## Dry run: CtCI deck design vs this interview

CtCI-style thought:
- A `Card` can have a `Value()`.
- A `BlackjackCard` can override `Value()`.

This kit's thought:
- A `Card` is just a fact: rank and suit.
- The game decides what that card means.

Example: `QH`.
- In High Score Part 2, `QH` may be 12.
- After a mutation, `QH` may be 10.
- In Battle, `QH` is not "points" at all; it is compared by rank strength.

So for this interview, putting points in `Game.PointsOf(Card)` is easier to mutate than putting points permanently inside `Card`.
