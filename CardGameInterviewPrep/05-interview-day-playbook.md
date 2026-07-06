# 05 — Interview-Day Playbook

## Simple version

On interview day, your job is to be clear and steady.

Do this for every part:

1. Read the whole part.
2. Say the rule back in your own words.
3. Ask only the important questions.
4. Name where the rule will live in the code.
5. Write a small working version.
6. Run it.
7. Add or update a small check.

Quick example:

Interviewer says: "Diamonds count double."

You say: "That's a card scoring rule, so I'll change `PointsOf(Card)` and add a check for `5D = 10`."

That's the behavior they want to see: understand it, route it, code it, test it.

## 30-minutes-before checklist

- Quiet room, water ready, phone silenced and **out of reach** (you'll be sharing your screen with your camera on).
- Close every window except: the HackerRank tab, and **one** browser tab on https://learn.microsoft.com (docs are allowed; an open LLM tab is an automatic fail even if you never use it — don't have one open anywhere).
- Test your mic, camera, and screen share in the meeting tool.
- Have a 30-second intro ready (name, years of experience, current stack, one sentence on what you build). Their doc says clearly: don't spend time here.
- Do NOT cram new material on the day. You already know this.

## The 60-minute clock

| Time | What you're doing | What you're saying |
|---|---|---|
| 0:00–0:02 | Intro (30s), open Part 1, read it fully | "Let me read this completely first." |
| 0:02–0:04 | Restate Part 1 + ask ≤3 questions (bank in `02`) | "So: a card with a rank and suit, a 52-card deck, shuffle and deal — and per the intro doc, ace is low, correct?" |
| 0:04–0:16 | **Muscle-memory zone**: Ranks → Suits → Card → Deck → Check helper → run | Say one sentence about each class as you start it. |
| 0:16–0:18 | Part 1 demo runs green; read Part 2 fully, restate it, ask scoring/tie questions | "Foundation verified. Reading part two…" |
| 0:18–0:36 | Game class: Deal → PointsOf → ScoreHand → Winners → demo + checks | "Point values live in one method — they tend to change." |
| 0:36–0:38 | Part 2 demo green; breathe; read Part 3 | |
| 0:38–0:55 | Handle changes one at a time, using the **R5 ritual** (below), rerun after each | |
| 0:55–0:60 | Final run, quick naming/cleanup pass, closing line | "With more time I'd pull the scoring into a strategy and add proper unit tests." |

Running ~5 minutes behind is normal. Running 10+ minutes behind → use the behind-schedule plan below.

## The R5 ritual for every rule change

1. **Restate** — "New rule: diamonds count double. So a 5♦ is 10 points now."
2. **Route** — "That's card scoring — it's `PointsOf`, nothing else knows about points."
3. **Red** — update the matching `Check` first, run it, and watch it FAIL. ("The check now expects 10 — currently failing, good.")
4. **Rewrite** — make the one-line edit.
5. **Rerun + report** — "All green again, and the demo shows doubled diamonds."

Thirty seconds of routine, huge grading payoff. Practice it in every mock.

## Think-aloud phrasebook (rehearse these out loud, in English, every drill)

**Starting a part**
- "Let me restate this in my own words to make sure I've got it…"
- "My plan: two small classes and a demo — Card and Deck first."

**While designing**
- "I'll keep the rank order as a data array, so if the ordering rule changes it's a one-line edit."
- "Ordering and point values are different rules, so they live in different places."
- "Winners returns a list, because ties are a real possibility."
- "I'm choosing the simple version for now; if a second variant shows up I'll pull out a strategy — not before."

**On a rule change**
- "That rule lands in `PointsOf` — nothing else needs to change."
- "I'll update the check first so we can watch it fail, then fix it."
- "This one replaces the war rule, so I'm deleting that branch instead of keeping dead code."

**When stuck (this is graded, so don't hide it)**
- "I don't remember the exact signature — let me check the docs quickly." *(then actually search learn.microsoft.com, under 90 seconds)*
- "Let me print the state each round to see where it goes wrong."
- "I'll seed the shuffle so this run is repeatable while I debug."

**Closing a part**
- "Done and verified. One thing I'd improve with more time: …" *(pick from: pull scoring into a strategy · a proper test project · an enum for ranks · split into files · input validation)*

## Behind-schedule plan

- Say it, don't hide it: "I'm behind — I'll simplify the tie-break to a shared win and leave a TODO, so we reach the last requirement."
- Stub it out with a comment, but keep the program **running**. A running program with a named shortcut beats a broken program with an elegant half-feature. Their doc grades you on completing all three parts.
- Never rewrite from scratch mid-exam. Never argue with a rule change.
- If a compile error won't budge after 2 minutes: comment the block out, get back to green, then re-approach it.

## C# pitfalls for exactly this exam

1. **Use one `Random` instance** as a field. `new Random()` inside a loop → identical time-based seeds → identical "shuffles."
2. **Only call `int.Parse(card.Rank)` in the `default:` branch** — after A/J/Q/K/JOKER are handled. `"JOKER"` will happily throw at runtime, not at compile time.
3. **Never remove from a `List` while looping over it with `foreach`** (`InvalidOperationException`). Shedding games hit this: find the card, remove it after the loop, or loop over a copy (`.ToList()`).
4. **`using System.Linq;`** — forgetting it makes `Sum`/`Where`/`GroupBy` look like they "don't exist." Learn to recognize that error message instantly.
5. **`OrderByDescending(...).First()` on an empty sequence throws** — guard against it, or use `FirstOrDefault` knowing it can return null.
6. **Integer division** when splitting piles or averaging (52/3 = 17).
7. Suit symbols (♥) may print as `??` in some consoles — using letters `C D H S` avoids it; if you want symbols locally: `Console.OutputEncoding = System.Text.Encoding.UTF8;`.
8. The tuple swap `(a, b) = (b, a)` is the fastest Fisher–Yates swap and looks clean.

## HackerRank environment notes (C#)

- One file, classic `static void Main` — exactly the skeleton's shape. Extra classes go in the same file; use `// ===== banner comments =====` as your "files."
- No debugger. Your debugger is `Console.WriteLine` + the `Check` helper + a seeded RNG. That's why we drill them.
- Run early, run often — every 2–3 minutes. The run button is your compile check; don't type for 10 minutes on faith.
- The output pane shows compile errors with line numbers — read the **first** error, fix it, rerun (later errors are usually just cascade noise).
- If the environment offers a language-version dropdown, any modern C# is fine — the skeleton avoids exotic syntax on purpose.

## Hard rules

- **No LLM anywhere** — automatic fail. Docs, Google, official references: allowed and expected.
- Don't over-polish Part 1 — its only job is to make Parts 2–3 fast.
- The narration is half the exam. A silent perfect solution scores worse than a talked-through good one.

## Walk-through: one rule change, spoken out loud

Interviewer says: "New rule: diamonds count double."

You say:

1. "Let me restate: a 5D now scores 10, but a 5H still scores 5."
2. "That's card scoring, so it belongs in `PointsOf`, not in dealing or winner logic."
3. "I'll update a check first: `PointsOf(new Card("5", "D")) == 10`."
4. Run it, and expect it to fail if the old code is still active.
5. Add `if (card.Suit == "D") points *= 2;` after the base points are known.
6. Rerun and say: "All checks pass again."

That short script is enough. Don't over-explain every keystroke — narrate your intent and where the rule goes.
