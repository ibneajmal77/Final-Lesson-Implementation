# FF Card-Game Interview — Prep Kit

Everything here is built from the two PDFs you received (the prep doc and the Card Game Introduction), plus the known shape of this interview format: **HackerRank, screen shared, one problem in 3 cumulative parts, rules change while you code.**

Your language: **C#** (.NET 9 installed on this machine).
Your timeline: **~1 week** — the 7-day plan is in `06-practice-plan.md`.

## The kit

## Plain English version

This folder is a practice kit for one interview style: you build a card game while the interviewer changes the rules. The main skill is not memorizing many games. The main skill is knowing where each rule should live in your code.

Use the kit like this:

1. First read `10-mind-map-and-mental-code.md`. It teaches you how to see the game in your head before writing code.
2. Then run `csharp/Skeleton`. This shows the basic `Card`, `Deck`, `Player`, and `Game` shape.
3. Then read `03-design-playbook.md`. This teaches where rule changes go.
4. Then practice one mock at a time. Do not rush. First understand the game, then code it.

Simple example:

If the rule says "diamonds count double," do not change the deck, the player, or the winner code. Change only the scoring method, usually `PointsOf(Card)`.

That is the whole idea of the kit: make each future rule change small.

| File | What it gives you | Read when |
|---|---|---|
| `01-decoded-interview.md` | What every line of their PDFs actually means for your behavior | Day 1 |
| `02-domain-and-questions.md` | The card domain + the clarifying-question bank (with safe defaults) | Day 1 |
| `03-design-playbook.md` | THE core skill: the OOP design where every rule change is a one-line edit, plus the change-routing table | Day 1, reread often |
| `04-game-catalog.md` | Every game they can plausibly ask, ranked by likelihood, each with its known mutation twists | Day 2 |
| `05-interview-day-playbook.md` | Minute-by-minute plan, think-aloud phrasebook, C# pitfalls, HackerRank notes | Day 2, reread Day 7 |
| `06-practice-plan.md` | The 7-day schedule, all drills, and the self-grading rubric | Day 1 |
| `07-oop-and-csharp-fundamentals.md` | The OOP concepts (pillars, SOLID, composition), C# features, collections and LINQ this interview actually uses — each with a say-line | Day 2 |
| `08-book-cracking-the-coding-interview.md` | Distilled notes on the first recommended book — its ch. 7.1 is literally "design a deck of cards" | Day 3–4 |
| `09-book-programming-pearls.md` | Distilled notes on the second recommended book — problem definition, rules-as-data, scaffolding | Day 3–4 |
| `10-mind-map-and-mental-code.md` | The mental map for playing each game in your head before writing code | Read whenever the kit feels hard |
| `mocks/mock1.md` … `mock6.md` | Six full scripted exams with timed rule mutations | Days 3, 5, 6, extras |
| `csharp/Skeleton/` | The runnable "muscle memory zone" — what you must be able to type from a blank file in under 10 minutes | Day 1 |
| `csharp/Mock1Solution/` | Worked final solution for Mock 1 + `NOTES.md` showing exactly where each rule change landed | After you attempt Mock 1 |

## Quick start (today, ~60 min)

```powershell
cd C:\Users\muhammad.awais\CardGameInterviewPrep\csharp\Skeleton
dotnet run
```

Then read `01`, `02`, `03`, and retype the skeleton yourself once with the reference open.

## Using Claude as your training partner

During the **real interview, any LLM use = automatic fail.** Before it, I'm your sparring partner. Useful prompts through the week:

- `Act as my FF card-game interviewer. Use mocks/mock1.md. 60 minutes, reveal parts on schedule, then grade me with the rubric in 06-practice-plan.md.`
- `Routing quiz: fire 10 rule changes at me one at a time; I'll answer where each lands before touching code.`
- `Variant storm: I have my Mock 1 code open. Fire mutations at me one at a time, 5 minutes each.`
- `Review my attempt against csharp/Mock1Solution and the rubric.` (paste your code)
- `Show me the reference solution for mock 2 / mock 3 / mock 4 / mock 5 / mock 6.` (after you attempt them)

If you ever want the skeleton mirrored in Python as a reference, just ask.

## Dry-run reading path

If the full kit feels heavy, read it in this order and stop after each dry run:

1. Read `10-mind-map-and-mental-code.md` first. Do not code yet; just picture the game table.
2. Run `csharp/Skeleton` once. Watch only these facts: deck starts at 52, drawing 5 leaves 47, each player gets 5 cards, highest score wins.
3. Read `03-design-playbook.md`, then do this mental mutation: "diamonds double." Answer: only `PointsOf(Card)` changes.
4. Open `mocks/mock1.md`. For Part 2, imagine Alice has `AH 10D`, Bob has `KS 2C`. Alice scores 11 if `10D` is worth 10; Bob scores 15 if K is worth 13. Bob wins. After M1, K becomes 10, so Bob scores 12. Same hand, different rule, one method changes.
5. Only after that, start timed practice. The first pass is for understanding, not speed.
