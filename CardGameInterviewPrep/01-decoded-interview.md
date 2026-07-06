# 01 — What This Interview Actually Is

## Plain English version

This interview is not mainly a puzzle interview. It is a fast coding exercise. You will build one card-game program in three parts. After you finish one part, the interviewer gives you a new rule. You must change your code without breaking everything.

What they are grading:

1. Did you understand the rule before coding?
2. Did you speak your thinking out loud?
3. Did you write clean code where every rule has one clear place?
4. Did you keep the program running?
5. Did you test small pieces as you worked?

Simple example:

If Part 2 says "highest score wins," you should build `PointsOf`, `ScoreHand`, and `Winners`. If Part 3 says "lowest score wins," the winner rule changes, not the card or deck classes.

The real goal is to stay calm, name where the rule belongs, change that one place, and run again.

## Hard facts from their prep doc

- HackerRank environment, screen shared, camera on. **Using an LLM = automatic fail.** Documentation and Google **are allowed** — looking things up fast is a graded skill, so we drill it.
- One problem, **three separate cumulative parts**. Budget roughly 60 minutes → ~15 min Part 1, ~18 min Part 2, ~18 min Part 3, small buffer.
- Their own words: *"not a typical LeetCode puzzle… a fast-paced implementation task… like a simulator, where the rules keep changing as you code."*
- Allowed languages: Python, JS, TS, C#, C++, Go, Java (Java discouraged). You chose **C#** — good: it's your daily language, and fluency beats brevity here.

## Translate their doc into behavior

| Their words | What you actually do |
|---|---|
| "Understand the problem… ask clarifying questions" | Read the part fully, restate it in one sentence, ask ≤3 high-impact questions (bank in `02`), then code. |
| "Think aloud" | Narrate **intent before typing**, not after. Phrasebook in `05`. Silence longer than ~2 minutes is a lost point. |
| "Clean code… recognize specific areas for improvement" | Rules-as-data + small policy methods (`03`). At the end of each part, say ONE improvement you'd make with more time. Rehearse that sentence — it's free points. |
| "Progress / efficient execution… complete all three parts" | Code must be runnable every 2–3 minutes. Never polish Part 1 while Part 3 exists. |
| "Testing & optimizing… quickly unblock yourself… documentation" | 3-line `Check` helper printing PASS/FAIL from minute ~5. Seeded `Random` while debugging. Practice 90-second doc lookups. |
| "Do not spend much time on the intro" | 30-second self-intro, then ask to see Part 1. Save every minute for code. |
| "Rules keep changing" | This is the real exam. The whole design playbook (`03`) exists so each change lands in exactly one method. |

## What the Card Game Introduction PDF is quietly telling you

These details are in the PDF **on purpose** — they are the traps:

1. **Ace is the LOWEST rank.** Order: A, 2, …, 10, J, Q, K, JOKER. Most people's instinct is ace-high. Bake ace-low in as the default, and expect "aces are high now" as a Part-3 mutation.
2. **JOKER is listed as a rank above K** — yet the doc says "there are 13 ranks" while listing 14 values. That contradiction is a ready-made clarifying question: *"You list JOKER among the ranks but say 13 ranks, and jokers have no suit — should my standard deck be 52 cards, with jokers optional?"* Asking this shows you actually read the spec.
3. **Jokers have no suit.** That breaks naive display (`rank + suit` would print `JOKERnull`), naive deck building (13×4 would create suited jokers), and any suit-based rule. Special-case jokers from minute one.
4. **Suits are explicitly unordered.** Do not build suit comparison until asked — but expect *"suits now break ties"* as a mutation. When it comes, you add one small array (same pattern as ranks) — see the routing table in `03`.
5. **Display format is rank + suit**, e.g. `2♥`, `10♦`, `Q♦`. Implement `ToString()` in the first minutes. Letters (`QD`, `10H`) are usually accepted — confirm with one quick question.
6. The deck image in their PDF shows **exactly 2 jokers** — that's the default joker count.

## The three-part shape to expect

Based on the doc's structure and how this format is commonly run:

- **Part 1 — Card + Deck.** Model the card, build a 52-card deck, shuffle, draw/deal. This is nearly always the same → make it pure muscle memory (`csharp/Skeleton`, cold-start drill in `06`).
- **Part 2 — an actual game.** Deal to N players, then either score-and-compare (most common), a round loop (war-style), or hand classification (pairs/three-of-a-kind). Catalog in `04`.
- **Part 3 — rapid rule mutations.** 2–4 changes, ~5 minutes each: point values change, a suit gets special treatment, jokers enter, tie rules appear, ordering flips. Each should be a small edit **if** your Part 1–2 structure is right.

## The 5 grading axes — what the interviewer writes down

1. **Understanding** — did you restate the problem and ask questions that changed what you built?
2. **Think-aloud** — could they follow your reasoning without asking?
3. **Clean code** — is every rule in one obvious place? Names clear? No duplicated logic?
4. **Velocity** — did all three parts get done, runnable the whole way?
5. **Testing & unblocking** — did you prove your code works as you went, and get unstuck via docs/prints without flailing?

The rubric in `06-practice-plan.md` turns these into a 1–4 self-score after every mock.

## Dry run: what one part feels like

Interviewer says: "Deal 5 cards to 3 players. Highest total wins."

You should do this out loud:

1. Restate: "I need a deck, 3 players, 5 cards each, then score each hand and return all highest-scoring players."
2. Ask: "Are face cards 11/12/13 or all 10? If tied, do tied players share the win?"
3. Code only the homes you need: `Deck`, `Player.Hand`, `Deal(5)`, `PointsOf`, `ScoreHand`, `Winners`.
4. Add a check: if Alice has `AH 9C` and Bob has `KH 2D`, Alice is 10 and Bob is 15 with K=13, so Bob wins.
5. When a rule changes, name the home before typing. "J/Q/K are 10 now" means `PointsOf` only.

That is the interview rhythm: restate, ask, route, code, check, rerun.
