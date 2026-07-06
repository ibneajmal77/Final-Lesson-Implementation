# 06 — The 7-Day Practice Plan

Assumes ~60–120 minutes per day around work. Day 7 = the day before the interview. **Every drill: speak your narration OUT LOUD in English.** The talking is graded as much as the code — train the mouth, not just the fingers.

## Plain English version

Practice is not just writing code. Practice has three parts:

1. Type the basic skeleton until it feels familiar.
2. Explain out loud where each rule belongs.
3. Run mock interviews where rules change.

Do not wait until the code is perfect before running it. Run small pieces often.

Simple practice session:

1. Type `Card` and `Deck`.
2. Check that the deck has 52 cards.
3. Add `Player` and `Deal`.
4. Check that drawing 5 cards leaves 47.
5. Add one game rule, like scoring.

Small repeated practice is better than one long confused session.

## The drills

**Drill A — Cold start (the core drill).**
Blank file → `Ranks`, `Suits`, `Card`, `Deck` (build/shuffle/draw), `Check` helper, 4+ checks, running green. No peeking at the reference.
Targets: Day 2 ≤ 12 min · Day 5 ≤ 10 min · Day 7 ≤ 8 min.
Setup: `mkdir drill && cd drill && dotnet new console`, then type into `Program.cs`.

**Drill B — Mock exam.** One of `mocks/mock1-3.md`, 60 minutes, strict. Best run with Claude as interviewer (prompt in `README.md`); solo works if you gate the reveals honestly. Grade with the rubric below immediately after.

**Drill C — Variant storm.** Open your finished mock code, have Claude fire 6–8 mutations one at a time, ~5 minutes each, full R5 ritual every time. Builds the "rules keep changing" reflex better than anything else.

**Drill D — Routing quiz (10 minutes, daily warm-up).** No code. Hear/read a rule change, answer aloud: *which method changes, what's the edit*. The table in `03` is the answer key. With Claude: "Routing quiz: fire 10 rule changes at me."

**Drill E — Doc sprint.** 5 lookups on learn.microsoft.com, each under 90 seconds, starting from a search box: `List<T>.RemoveAt` · `Enumerable.GroupBy` · `Random.Next(int)` · `string.Join` · `Enumerable.OrderBy`. Trains legal unblocking for the day someone asks for a method you forgot.

## The week

| Day | Time | Do |
|---|---|---|
| **1 (today)** | ~90 min | Read `01`–`03`. Run `csharp/Skeleton` (`dotnet run`). Retype the skeleton once **with the reference open** — feel the shape. |
| **2** | ~90 min | Drill D (warm-up) · Drill A ×2 (target ≤12 min) · read `04` Tier A · read `07` (OOP/C# — mostly naming what you already do). |
| **3** | ~2 h | **Mock 1** (Drill B) · grade yourself · compare with `csharp/Mock1Solution` + its `NOTES.md` — specifically: did your mutations land in the same *places*? |
| **4** | ~90 min | Drill D · Drill C (variant storm on your Mock 1 code) · Drill E · read the book notes `08` + `09`. |
| **5** | ~2 h | Drill A ×1 (target ≤10 min) · **Mock 2** (war/battle — different muscle: loops + policy replacement) · grade. |
| **6** | ~2 h | Drill D · **Mock 3** (classification + wildcards, the hardest) · grade · skim `04` Tier B/C so nothing feels alien. |
| **7 (day before)** | ~45 min | Drill A ×1 (should be ≤8 min and boring) · reread `05` only · prepare the room/checklist · stop early. Sleep is a performance drug. |

Weak on something after a mock? Swap the next day's Drill C target to exactly that weakness. Ahead of schedule? Run `mocks/mock4.md` through `mocks/mock6.md` for Blackjack-lite, Crazy Eights-lite, and Trick-taking-lite practice.

## Self-grading rubric (after every mock — score honestly, out loud)

| Axis | 4 | 3 | 2 | 1 |
|---|---|---|---|---|
| **Understanding** | Restated every part in own words; questions changed what you built; assumptions typed as comments | Restated; asked decent questions | Started coding from a half-read spec; backtracked once | Built the wrong thing for >5 min |
| **Think-aloud** | Intent narrated *before* typing, trade-offs named | Mostly narrated; some silent stretches | Silent >2 min repeatedly; narration is after-the-fact | Silence, or narrating literally every keystroke |
| **Clean code** | Every rule has one home; you could answer Drill D questions about your own file instantly | Minor duplication; one rule leaked into two places | Point values hard-coded at call sites; winner assumes no ties | Spaghetti; a mutation required touching 4+ spots |
| **Velocity** | All parts + a bonus mutation, runnable throughout | All three parts done, some polish skipped | Part 3 half-done | Stuck in Part 2 |
| **Testing & unblocking** | Check helper by min 5; red→green on every mutation; doc lookup <90s when stuck | Checks exist; reran often | First run after 20+ min; debugging by staring | Never verified; flailed when stuck |

**Ready for the real thing** = two consecutive mocks scoring ≥17/20 with no axis below 3, and cold start ≤10 minutes. That's achievable by Day 6 on this plan.

## Dry run: what one practice block looks like

If you have 45 minutes instead of 2 hours:

1. 5 minutes: Drill D. Say where each rule lands: points, ordering, winner, deck, or turn loop.
2. 12 minutes: Cold start. Type `Ranks`, `Suits`, `Card`, `Deck`, and `Check`.
3. 20 minutes: Take one mock Part 2 only. Do not do mutations yet.
4. 5 minutes: Grade yourself on two axes only: clean code and testing.
5. 3 minutes: Write one weakness: "I mixed rank strength and points" or "I forgot to return tied winners."

That is still useful practice. The goal is repeated feedback, not one perfect long session.
