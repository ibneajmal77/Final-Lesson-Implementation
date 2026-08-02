# 01 — THE ROLE, DECODED

> **Goal:** walk in knowing what they actually want — better than they've written it down.

---

# PART 0 — THE 5 THINGS THIS FILE TELLS YOU

| # | The insight | Why it matters |
|---|---|---|
| 1 | **"BCM" means Banking & Capital Markets.** Combined with "Portfolio/Order/Execution Management" and "columnar databases", this is a **buy-side** technology role. | It reframes the entire job spec |
| 2 | **WPF is not a footnote. Desktop is the primary UI.** | Your biggest risk |
| 3 | **This is most likely a *modernisation* programme** — old .NET estate being extended with Python, REST and Azure. | **That's exactly your story** |
| 4 | **Their four values: correct numbers, responsive under load, auditable, don't break the desk.** | Frame every answer against these |
| 5 | **Luxoft's assessor is measuring risk.** | Honesty reduces it. Bluffing increases it |

---

# PART 1 — THE POSTING, AS WRITTEN

| Field | Value |
|---|---|
| Title | Senior Full Stack Developer |
| Location | Abu Dhabi, UAE (permanent) |
| Specialization tag | **C#/VB.NET** |
| Industry tag | **BCM** |
| English | **C1 Advanced** |
| Budget | AED 25,000–35,000 gross/month |

**Must-haves:** 8+ years engineering or solution architecture · **.NET (C#, WPF) — Advanced** ·
**Python — Advanced** · JavaScript + a framework — *Medium* · SQL · MongoDB or similar ·
**real-time and multithreaded systems** · distributed design · Azure (preferred) · solution
architecture · Agile + DevOps/CI-CD · **design patterns and algorithms** · REST APIs with auth
protocols · **Windows development**.

**Nice-to-haves:** performance testing and profiling · **columnar** databases · SOA frameworks ·
**financial mathematics** · **Portfolio / Order / Execution Management Systems** · **financial
optimization**.

---

# PART 2 — WHAT "BCM" MEANS, AND WHY IT REFRAMES EVERYTHING

**BCM = Banking & Capital Markets** — Luxoft's financial services vertical.

Luxoft (a DXC company) is one of the largest specialist engineering suppliers to investment banks and
asset managers globally. They're known for **Murex, Calypso**, and bespoke trading, risk and portfolio
platforms.

⚠️ **That single tag reframes the whole posting.** Combine it with the nice-to-haves —
*Portfolio/Order/Execution Management Systems*, *financial mathematics*, *financial optimization*,
*columnar databases* — and the picture is unambiguous:

> **This is a buy-side technology role.** You'd be building or extending a system that **holds
> portfolios, generates and routes orders, tracks executions, and computes risk and performance
> analytics** — with a **WPF desktop front end**, a **Python** quant/analytics layer, **SQL plus
> document plus columnar** storage, and **real-time multithreaded** market-data handling.

## Who is the client, probably?

Abu Dhabi + buy-side + a large multi-team programme points to a **sovereign wealth fund, a large asset
manager, or a bank's investment arm**. The well-known Abu Dhabi names are ADIA, Mubadala, ADQ, ADCB,
FAB, Lunate.

⚠️ **Do not name-guess in the interview.** Treat it as a hypothesis and **ask**.
**Guessing wrong sounds sloppy. Asking sounds engaged.**

## Why the client type matters for your prep

**Buy-side desktop teams care about, in this order:**

1. **Correctness of the numbers**
2. **Latency and responsiveness under load**
3. **Auditability**
4. **Not breaking the traders' screens**

⚠️ **Frame every technical answer against those four values and you will sound like you belong
there.** They are the reason `decimal`-not-float, conflation-and-batching, and event-sourcing-for-audit
are the strongest cards in this whole pack.

---

# PART 3 — DECODING EACH MUST-HAVE

**What the line says → what they'll actually ask.**

| The job spec says | They'll actually ask about | File |
|---|---|---|
| ".NET (C#, WPF) **Advanced**" | GC, memory, async, LINQ, EF — **and** XAML, binding, MVVM, Dispatcher | `03`, `05` |
| "**Python** Advanced" | **GIL**, asyncio vs threads vs processes, Pandas vectorisation | `06` |
| "JavaScript (**Medium**)" | Light. React basics. ⚠️ **Your strongest area — will barely be tested** | `17` |
| "SQL proficiency" | Joins, window functions, indexes, execution plans, **a live query** | `07` |
| "MongoDB or similar" | Document modelling, **when NOT to use it**, indexes, aggregation | `07` |
| "**Real-time and multithreaded**" | Threads vs tasks, locks, races, deadlock, producer/consumer, backpressure | `04` |
| "Distributed design" | CAP, eventual consistency, idempotency, messaging, failure modes | `08` |
| "Azure (preferred)" | Which services and why. ⚠️ **Easy points — keep it short** | `10` |
| "Solution architecture" | Can you own a design end to end and **defend the trade-offs** | `08` |
| "**Design patterns and algorithms**" | Patterns **with real examples**, plus a coding exercise | `08`, `16` |
| "REST APIs with auth protocols" | REST maturity, versioning, OAuth2/OIDC/JWT, mTLS, **Kerberos** | `09` |
| "**Windows development**" | WPF, Windows Services, MSI/MSIX deployment, Windows auth | `05` |

## ⚠️ The four phrases that should make you sit up

1. **"WPF (Advanced)"** — not a footnote. **Desktop is the primary UI. Your CV has none.** → `05`
2. **"Real-time and multithreaded"** — that means market data. **Expect concurrency questions with
   teeth.** → `04`
3. **"Windows development"** — this is an **on-prem/desktop-heavy shop, not a pure cloud shop**.
   ⚠️ **Adjust your instinct to answer everything with "I'd put it in Azure Container Apps."**
4. **"Portfolio / Order / Execution Management Systems"** — the domain. A nice-to-have on paper,
   **decisive in the client round.** → `11`

---

# PART 4 — WHAT THE MISMATCH TELLS YOU (the key insight)

Your CV is a **cloud-native, event-driven, AI/microservices** CV.
The job spec is a **desktop + real-time data + quant + on-prem-leaning** spec.

**Two possible readings:**

## Reading A — likely. It's a modernisation programme.

An existing WPF/.NET Framework desktop estate plus SQL, being extended with Python analytics, REST
services, MongoDB and Azure. **They need someone who knows the *old* world and can bring the *new*
one.**

⚠️ **That is exactly you.** You've literally done *"modernised legacy .NET Framework and ASP.NET MVC
monoliths into .NET 5/6 microservices"* at Merik, and *"migrated core modules off legacy .NET
Framework and WCF"* at Calrom.

**Make this your pitch.** → `02` Part 3.

## Reading B — less likely. They want a pure desktop/real-time engineer.

Your cloud and AI depth would be largely irrelevant. Less likely, because "solution architecture",
"distributed design", "Azure", "REST APIs", "MongoDB" and "DevOps/CI-CD" are **all listed as
must-haves**.

**But if the interview leans this way:** pivot hard to `04` and `05`, and keep every cloud answer to
one sentence.

## ⭐ How to find out which one is true — in the first ten minutes

**Ask this, naturally, when invited:**

> *"Is this a greenfield build, or extending an existing platform? And roughly what's the split
> between the desktop client, the services behind it, and the Python/analytics side?"*

⚠️ **Their answer tells you where to aim every subsequent answer. It's the single most valuable
question you can ask, and asking it early changes the rest of the hour.**

---

# PART 5 — WHO IS ACTUALLY INTERVIEWING YOU

**Luxoft is a consultancy** (a DXC Technology company). You'd be a **Luxoft employee deployed to a
client** in Abu Dhabi.

⚠️ **That's exactly the model you're in today** — embedded on-site with a client, and the same at
Merik. **Say this out loud in the interview. It's a real advantage and most candidates can't claim
it.**

| Stage | Who | What they're deciding |
|---|---|---|
| **1 — Monday** | A Luxoft senior engineer or tech lead | *"Is this person technically real, and can I put them in front of the client?"* |
| **2** | Hiring manager | Seniority, ownership, communication, delivery track record |
| **3** | The client | Domain interest, team fit, client-facing polish |

They also screen hard for **English C1** and the ability to talk to non-technical stakeholders. Your
client-facing and forward-deployed delivery experience is directly on point — **make sure it comes
up.**

## ⚠️ The consequence — internalise this

**Luxoft's assessor is measuring risk.**

- Every *"I don't know, but here's how I'd find out — and here's the closest thing I've done"*
  **reduces** their risk.
- Every bluff **increases** it — because **the client round will catch it, and that embarrasses
  them.**

**That is why the honest answers in `02` Part 5 are not a fallback. They are the strategy.**

---

# PART 6 — COMPENSATION (for stage 2, not Monday)

- Band: **AED 25,000–35,000/month gross** = AED 300k–420k a year, **tax-free**.
- Questions to clarify **later**: is housing allowance inside or outside that number? Annual flights,
  medical, visa, schooling, relocation from Dubai, end-of-service gratuity.

⚠️ **Monday: do not discuss money.** If asked, defer warmly:
> *"Yevheniia shared the range and it works for me — I'd rather focus on the technical fit today."*

---

# PART 7 — FIVE THINGS TO HAVE IN YOUR HEAD WALKING IN

1. This is **capital markets, buy-side, desktop-heavy, real-time**.
2. Your headline is **".NET engineer who modernises platforms"** — not "AI engineer".
3. Your three risk areas are **WPF, threading depth, and finance domain** — and **you have prepared,
   honest answers for all three**.
4. Their four values: **correct numbers · responsive under load · auditable · don't break the desk.**
5. You're being hired **by a consultancy, for a client** — so **client-facing credibility counts as
   much as code.**
