# START HERE — Luxoft Senior Full Stack Developer (Abu Dhabi, VR-122402)

**Candidate:** Muhammad Awais
**Role:** Senior Full Stack Developer — Abu Dhabi, UAE · permanent
**Specialization:** C#/VB.NET · **Industry:** BCM (Banking & Capital Markets)
**Budget:** AED 25,000–35,000 gross/month
**Recruiter:** Yevheniia Zlatieva (DXC/Luxoft)

## ⏰ THE TIMELINE

| Stage | When | Format | What it decides |
|---|---|---|---|
| **1. Technical discussion** | **Mon 03 Aug 2026, 17:00 Dubai — 1 hour** | Video, *"code exercise could be done"* | Are you technically real? |
| 2. Hiring manager discussion | TBD, after stage 1 | Video | Seniority, ownership, communication |
| 3. Final client discussion | TBD | Video with the Abu Dhabi client | Domain fit, client-facing polish |

**You have Fri evening + Sat + Sun + Mon daytime. ~3 days.** Plan below is built for exactly that.

---

## 1. The one-paragraph read on your situation

This is **not** the AI/cloud role your CV is optimised for. It is a **.NET + Python + real-time data
role in capital markets**, with **WPF (desktop) listed as Advanced** — almost certainly a
portfolio/order management or trading-adjacent system for an Abu Dhabi financial institution.
Your .NET depth, distributed systems, Python, SQL, design patterns and Azure are **direct hits**.
Your three gaps are **WPF, low-level multithreading fluency, and financial domain**. Close those
and you're strong. Ignore them and round 1 will expose you.

**Monday is 1 hour.** Realistically that's ~10 min intro/project walkthrough, ~30 min deep technical
Q&A, ~10 min code exercise, ~10 min your questions. Optimise for *that*, not for a 5-hour exam.

---

## 2. Priority order — where your hours go

| # | Topic | File | Monday weight | Why |
|---|---|---|---|---|
| 🔴 1 | **Project walkthrough** (your 3-min story) | `02` §4 | Very high | Guaranteed first question. Sets the whole tone. |
| 🔴 2 | **C# / .NET internals** | `03` | Very high | Their core specialization. Must be flawless. |
| 🔴 3 | **Multithreading & real-time** | `04` | Very high | Explicit must-have; loved in trading interviews. |
| 🔴 4 | **WPF / desktop** | `05` | High | Listed *Advanced*; zero on your CV. Biggest risk. |
| 🟠 5 | **Design patterns + coding exercise** | `08` A/B, `16` B | High | "Code exercise could be done" — be ready. |
| 🟠 6 | **SQL** (+ MongoDB, columnar) | `07` | High | Explicit must-have; classic Luxoft screen topic. |
| 🟠 7 | **Python advanced** | `06` | **High** | Listed *Advanced* — equal billing with .NET. Internals (GIL, memory) are what get tested. |
| 🟡 7b | JS / TypeScript / React | `17` | Low (~90 min) | Listed *Medium* only. But your CV claims a lot here — read `17` §0 for the calibration line. |
| 🟡 8 | System design / SOA / distributed | `08` | Medium | Your strength — go deep if invited. |
| 🟡 9 | REST + auth protocols | `09` | Medium | Easy points, don't fumble. |
| 🟡 10 | Azure / DevOps / CI-CD | `10` | Low-med | Your strength. Keep answers *short*. |
| 🟢 11 | Finance domain | `11` | Low Mon, **high for stage 3** | Show curiosity Monday; master before client round. |
| 🟢 12 | Performance & profiling | `12` | Low-med | Nice-to-have = cheap differentiator. |
| 🟢 13 | Behavioural / STAR | `13` | Low Mon, **high stage 2** | Decides the offer later. |

---

## 3. File map

```
00-START-HERE.md ..................... this file: plan, schedule, how to use the pack
01-role-decoded.md ................... what the JD really means, likely client, Luxoft context
02-gap-analysis-positioning.md ....... CV vs JD, your narrative, 3-min project story, gap scripts
03-csharp-dotnet.md .................. C#, CLR, GC, memory, LINQ, EF — Q&A + code
04-multithreading-concurrency.md ..... threads, TPL, async, locks, lock-free, real-time — Q&A + code
05-wpf-desktop.md .................... WPF/XAML/MVVM zero → interview-ready + the build project
06-python.md ......................... advanced Python, GIL, asyncio, pandas/numpy — Q&A + code
07-sql-databases.md .................. SQL tuning, indexes, isolation, MongoDB, columnar/time-series
08-design-patterns-architecture.md ... GoF + enterprise patterns, algorithms, 3 design walkthroughs
09-rest-api-security.md .............. REST design, OAuth2/OIDC/JWT/Kerberos/mTLS — Q&A
10-azure-devops.md ................... Azure services, CI/CD, IaC, observability — Q&A
11-finance-domain.md ................. instruments, order lifecycle, OMS/EMS/PMS, FIX, P&L, risk, quant
12-performance-profiling.md .......... profiling .NET & Python, benchmarking, load testing
13-behavioural-and-questions.md ...... STAR stories, their questions, your questions, follow-up email
15-cheatsheet-cram.md ................ ⭐ rapid revision — read Monday afternoon, keep open on the call
16-mock-drills.md .................... 95 rapid-fire Qs + 8 coding exercises + mock interview scripts
17-javascript-typescript-react.md .... JS/TS/React/Angular in plain words, built on C# comparisons
```

---

## 4. THE 3-DAY PLAN

### 🌙 Friday evening (tonight, 2–3 h) — *orientation + the thing that takes longest to sink in*
1. Read `01-role-decoded.md` and `02-gap-analysis-positioning.md` (45 min).
2. **Write and say out loud** your 3-minute project walkthrough from `02` §4 (45 min).
   Record yourself on your phone. Play it back. Redo it. This is the highest-ROI hour of the weekend.
3. Skim `05-wpf-desktop.md` §1–4 so WPF concepts start marinating overnight (30 min).
4. Set up the WPF project skeleton (`dotnet new wpf`) so Saturday starts with code, not setup (15 min).

### ☀️ Saturday (6–7 h) — *the two hard gaps*
| Block | Time | What |
|---|---|---|
| AM-1 | 2.5 h | **Build the WPF app** (`05` §12). Real-time DataGrid, MVVM, background ticks. Actually run it. |
| AM-2 | 1 h | `05` §5–11 Q&A — read *after* building; it will now make sense. |
| PM-1 | 2 h | `04-multithreading-concurrency.md` end to end. Write the code samples yourself. |
| PM-2 | 1 h | `03-csharp-dotnet.md` §1–6 (CLR, GC, value vs reference, boxing, `struct`). |
| Night | 30 m | `15-cheatsheet-cram.md` skim. Sleep on it. |

### ☀️ Sunday (6–7 h) — *breadth + the exercise + polish*
| Block | Time | What |
|---|---|---|
| AM-1 | 1.5 h | `03` rest + `07-sql-databases.md`. Write 5 SQL queries by hand (`07` §9). |
| AM-2 | 1.5 h | `08` Part A patterns + `16` Part B coding — **solve 3 on paper, timed 25 min each**. |
| PM-1 | 2 h | `06-python.md` (§5 GIL first, it's the big one) + `09-rest-api-security.md`. |
| PM-1b | 1 h | `17-javascript-typescript-react.md` — read §0 and Part 7 twice; skim the rest once. |
| PM-2 | 1.5 h | `11-finance-domain.md` — read twice. Then `08` §C4 design walkthrough **out loud**. |
| Night | 1 h | `16` Part A rapid-fire (target 70+/95), then `16` §C3 self-run mock, camera on. |

### 🎯 Monday (interview 17:00 Dubai)
| Time | What |
|---|---|
| Morning, 2 h | `15-cheatsheet-cram.md` cover to cover. Then `16` Part A rapid-fire — out loud, no notes. |
| 14:00, 1 h | Re-run your 60-sec pitch 3×. Re-read `02` §5 (gap scripts) and `13` §4 (your questions). |
| 15:30 | **Tech check:** camera, mic, lighting, headphones, link works, IDE open, screen-share tested. |
| 16:00 | Light food. Water on desk. Phone silent. Close Slack/email. |
| 16:40 | Notes on screen: 1-page cram sheet + your 5 questions + your pitch bullets. Nothing else. |
| 16:55 | Join. Camera on, smile, breathe. |

---

## 5. The homework that changes everything

**Build a small WPF app on Saturday morning. Timebox 2.5 hours.** Full instructions: `05` §12.

You cannot credibly claim "Advanced WPF" from reading alone. But after building this you can honestly
say *"I've been hands-on in WPF recently building a real-time positions grid"* — and answer ~20
interview questions from lived experience instead of theory: data binding, `INotifyPropertyChanged`,
`ObservableCollection`, dispatcher marshalling, UI virtualisation, throttling high-frequency updates,
MVVM, commands, converters, and the classic *"how do you update the UI from a background thread at
20 ticks/second without freezing it?"* — which is **exactly** the question a capital-markets desktop
team asks.

---

## 6. Three rules for the whole process

1. **Lead with .NET, not AI.** Your CV reads "Senior Full Stack **AI** Engineer". This role wants a
   .NET craftsman who handles real-time data and desktop UIs. Reorder the story: .NET → distributed/
   real-time → Python/SQL → *then* AI as a bonus. See `02` §3.
2. **Never bluff on WPF or finance.** Name what you've done, show transferable depth, show the
   learning already started. In a capital-markets interview the interviewer *is* the domain expert.
   Exact wording in `02` §5.
3. **Quantify.** 200K events/day, <100 ms, 99.99% delivery, sub-2s RAG, sub-second APIs at peak,
   90%+ coverage, environments in <5 min. Say these numbers out loud — most candidates can't.

---

## 7. Known unknowns (don't invent answers to these)

- **The end client is not named in the posting.** "BCM" = Luxoft's Banking & Capital Markets vertical.
  Treat any guess as a hypothesis — ask them directly (question #2 in `14`).
- **VB.NET** appears in the specialization tag but nowhere in the requirements — likely a legacy
  component or just Luxoft's internal taxonomy. Have a one-line answer ready (`02` §5).
- The ChatGPT link you shared could not be read (client-side rendered, no content retrievable).
  If it contained specific questions or notes, paste the text and I'll fold it in.
