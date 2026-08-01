# 01 — The Role, Decoded

> Goal: walk into Monday knowing what they actually want, better than they've written it down.

---

## 1. The posting, as written

| Field | Value |
|---|---|
| Title | Senior Full Stack Developer |
| Location | Abu Dhabi, UAE (permanent, on-site/hybrid — confirm) |
| Specialization tag | **C#/VB.NET** |
| Industry tag | **BCM** |
| Seniority | Senior |
| Request ID | VR-122402 |
| English | **C1 Advanced** |
| Budget (from recruiter) | **AED 25,000–35,000 gross/month** |

**Must-haves:** 8+ yrs software engineering / solution architecture · .NET (C#, **WPF**) *Advanced* ·
**Python** *Advanced* · JavaScript + a framework *Medium* · SQL · MongoDB or similar unstructured
data · **real-time and multithreaded systems** · distributed design · Azure (preferred) · solution
architecture · Agile + DevOps/CI-CD · **design patterns and algorithms** · REST APIs with auth
protocols · **Windows development**.

**Nice-to-haves:** performance testing & profiling · **columnar** and relational DBs · SOA frameworks ·
**financial mathematics** · **Portfolio / Order / Execution Management Systems** · financial optimization.

---

## 2. What "BCM" means and why it matters

**BCM = Banking & Capital Markets** — Luxoft's financial services vertical. Luxoft (a DXC Technology
company) is one of the largest specialist engineering suppliers to investment banks and asset
managers globally; they're known for Murex, Calypso, and bespoke trading/risk/portfolio platforms.

That single tag reframes the whole posting. Combine it with the nice-to-haves — *Portfolio/Order/
Execution Management Systems*, *financial mathematics*, *financial optimization*, *columnar
databases* — and the picture is unambiguous:

> **This is a buy-side (asset management / investment) technology role.** You will be building or
> extending a system that holds portfolios, generates and routes orders, tracks executions, and
> computes risk/performance analytics — with a **Windows desktop front-end in WPF**, a **Python**
> analytics/quant layer, **SQL + document + columnar** storage, and **real-time multithreaded**
> market-data handling.

### Who is the client, probably?
Abu Dhabi + buy-side + large multi-team programme ("expanding across the Middle East with multiple
initiatives", teams of "frontend and backend engineers, data professionals, architects, analysts, and
project managers") points to a **sovereign wealth fund, a large asset manager, or a bank's investment
arm** — the well-known Abu Dhabi names are ADIA, Mubadala, ADQ, ADCB, FAB, ADIB, Lunate, Abu Dhabi
Investment Office. **Do not name-guess in the interview.** Treat it as a hypothesis and *ask*
(question #2 in `14`). Guessing wrong sounds sloppy; asking sounds engaged.

### Why the client matters for your prep
Buy-side desktop teams care about, in this order: **correctness of numbers**, **latency/responsiveness
under load**, **auditability**, **not breaking the traders' screens**. Frame every technical answer
against those four values and you will sound like you belong there.

---

## 3. Decoding each must-have — what they're really testing

| JD line | What they'll actually ask | Your file |
|---|---|---|
| ".NET (C#, WPF) **Advanced**" | GC, memory, async, LINQ, EF *and* XAML/binding/MVVM/Dispatcher | `03`, `05` |
| "**Python** Advanced" | GIL, asyncio vs threads vs processes, pandas/numpy vectorisation, packaging | `06` |
| "JavaScript with frameworks (**Medium**)" | Light. React/Angular basics, maybe a web portal alongside the desktop app. **Your strongest area — will barely be tested.** | `15` |
| "SQL proficiency" | Joins, window functions, indexes, execution plans, a live query | `07` |
| "MongoDB or similar unstructured data" | Document modelling, when NOT to use it, indexes, aggregation | `07` §7 |
| "**Real-time and multithreaded systems**" | Threads vs tasks, locks, race conditions, deadlock, lock-free, producer/consumer, backpressure | `04` |
| "Distributed design understanding" | CAP, eventual consistency, idempotency, messaging, failure modes | `08` |
| "Microsoft Azure (preferred)" | Which services, why, how you deploy. **Easy points for you.** | `10` |
| "Solution architecture background" | Can you own a design end-to-end and defend trade-offs | `08` |
| "Agile and DevOps/CI-CD" | Your process, branching, release cadence, quality gates | `10` |
| "**Design patterns and algorithms**" | GoF patterns *with real examples*, plus a coding exercise (complexity, data structures) | `08` §6, `16` |
| "REST APIs with authentication protocols" | REST maturity, versioning, OAuth2/OIDC/JWT, mTLS, maybe Kerberos/Windows auth | `09` |
| "**Windows development**" | WPF, Windows Services, MSI/ClickOnce deploy, Windows auth, Win perf counters | `05` §11 |

### The four phrases that should make you sit up
1. **"WPF (Advanced)"** — not a footnote. Desktop is the primary UI. Your CV has none. → `05`.
2. **"Real-time and multithreaded"** — market data. Expect concurrency questions with teeth. → `04`.
3. **"Windows development"** — this is an on-prem/desktop-heavy shop, not a pure cloud shop. Adjust
   your instinct to answer everything with "I'd put it in Azure Container Apps".
4. **"Portfolio/Order/Execution Management Systems"** — the domain. Nice-to-have on paper, decisive
   in the client round. → `11`.

---

## 4. What the mismatch tells you (this is the key insight)

Your CV is a **cloud-native, event-driven, AI/microservices** CV. The JD is a **desktop + real-time
data + quant + on-prem-leaning** JD. Two possible readings:

- **Reading A (likely):** it's a *modernisation* programme. Existing WPF/.NET Framework desktop
  estate + SQL, being extended with Python analytics, REST services, MongoDB, and Azure. They need
  someone who knows the *old* world **and** can bring the *new* one. **That's you** — you've
  literally done "modernised legacy .NET Framework / ASP.NET MVC monoliths into .NET 5/6 microservices"
  (Merik) and "migrating core modules off legacy .NET Framework / WCF" (Calrom). **Make this your
  pitch.** See `02` §3.
- **Reading B:** they want a pure desktop/real-time engineer and your cloud/AI depth is irrelevant.
  Less likely given "solution architecture", "distributed design", "Azure", "REST APIs", "MongoDB",
  "DevOps/CI-CD" are all must-haves. But if the interview leans this way, pivot hard to `04`+`05` and
  keep cloud answers to one sentence.

**Diagnose which reading is true in the first 10 minutes** by asking (naturally, when invited to ask):
> *"Is this a greenfield build, or extending an existing platform? And roughly what's the split
> between the desktop client, the services behind it, and the Python/analytics side?"*

Their answer tells you where to aim every subsequent answer. It's the single most valuable question
you can ask early.

---

## 5. Luxoft / DXC context — who is actually interviewing you

- **Luxoft is a consultancy** (DXC Technology company). You'd be a **Luxoft employee deployed to a
  client** in Abu Dhabi. Exactly the model you're in today (USS IT Consultants → onsite at 7X) and
  did at Merik. **Say this out loud in the interview — it's a real advantage.**
- **Stage 1 (Monday)** is Luxoft's own technical assessor: a senior engineer or tech lead. Their job
  is *"is this person technically real and can I put them in front of the client?"*
- **Stage 2** hiring manager: seniority, ownership, communication, delivery track record.
- **Stage 3** client discussion: domain interest, fit with their team, client-facing polish.
- They screen hard for **English C1** and for the ability to talk to non-technical stakeholders.
  Your CV's "Client Engineering & Forward-Deployed Delivery" section is directly on point — make sure
  it comes up.

**Consequence:** Luxoft's assessor is measuring risk. Every "I don't know, but here's how I'd find
out / here's the closest thing I've done" answer *reduces* their risk. Every bluff *increases* it,
because the client round will catch it and that embarrasses them.

---

## 6. The compensation frame (for stage 2, not Monday)

- Band: **AED 25,000–35,000/month gross** = AED 300k–420k/year, tax-free.
- Abu Dhabi package questions to clarify later: housing allowance in or out of that number?
  Annual flights, medical, visa, schooling, relocation from Dubai, gratuity/end-of-service.
- **Monday: do not discuss money.** If asked, defer warmly: *"Yevheniia shared the range and it works
  for me — I'd rather focus on the technical fit today."*
- Full negotiation guidance in `14` §4.

---

## 7. Five things to have in your head walking in

1. This is **capital markets, buy-side, desktop-heavy, real-time**.
2. Your headline is **".NET engineer who modernises platforms"**, not "AI engineer".
3. Your three risk areas are **WPF, threading depth, finance domain** — you have prepared answers for
   all three, including honest ones.
4. Their four values: **correct numbers, responsive under load, auditable, don't break the desk.**
5. You're being hired **by a consultancy, for a client** — client-facing credibility counts as much
   as code.
