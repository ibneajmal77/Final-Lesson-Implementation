# 02 — YOUR POSITIONING & THE HARD QUESTIONS

> ⚠️ **This is the most important file in the pack.** Read it twice. **Say the scripts out loud.**
>
> Everything else teaches you facts. This one decides whether they believe you.

---

# PART 0 — THE 5 THINGS THIS FILE GIVES YOU

| # | Thing | Where |
|---|---|---|
| 1 | **Your 60-second pitch** | Part 3 |
| 2 | **Your 3-minute project story** | Part 4 |
| 3 | **The WPF honest answer** | Part 5.1 |
| 4 | **The finance honest answer** | Part 5.2 |
| 5 | **The calibration line that changes the tone of the whole interview** | Part 2 |

---

# PART 1 — WHERE YOU ACTUALLY STAND

Rating = how you'd score **under real questioning**, not how it looks on paper.

| Requirement | Your evidence | Score |
|---|---|---|
| 8+ years engineering / architecture | 9+ years, architecture ownership, ADRs | 🟢 5/5 |
| **.NET (C#) Advanced** | Framework 4.x → .NET 10, ASP.NET Core, EF Core, DDD/CQRS, MediatR, Polly, gRPC, SignalR | 🟢 5/5 |
| **WPF Advanced** | **Nothing.** | 🔴 **1/5** |
| **Windows development** | .NET Framework era, PowerShell, Windows-hosted services. No desktop/MSI story | 🟠 2/5 |
| **Python Advanced** | FastAPI, asyncio, Pandas, NumPy, Celery, SQLAlchemy, PyTest | 🟢 4/5 |
| JavaScript + framework (*Medium*) | React, Angular, Vue, TypeScript, micro-frontends | 🟢 5/5 — ⚠️ **over-qualified. Don't over-talk it** |
| SQL | SQL Server, Azure SQL, PostgreSQL, window functions, execution plans, index design | 🟢 4.5/5 |
| MongoDB / unstructured | MongoDB, Cosmos DB, DynamoDB across three roles | 🟢 4.5/5 |
| **Real-time & multithreaded** | Kafka 200K/day <100 ms, SignalR, Redis Streams, Channels — but **distributed**, not **in-process threading** | 🟠 **3/5** |
| Distributed design | SAGA, outbox, idempotency, CQRS, event sourcing, DDD | 🟢 5/5 |
| Azure | **AZ-305 certified**, deep service list, IaC | 🟢 5/5 |
| Solution architecture | ADRs, design reviews, C4, tech lead | 🟢 4.5/5 |
| Agile + DevOps | Azure DevOps, GH Actions, Terraform, quality gates | 🟢 5/5 |
| Design patterns & algorithms | Patterns excellent. **Algorithms unproven** | 🟠 3.5/5 |
| REST + auth protocols | OpenAPI, OAuth2/PKCE, OIDC, SAML, JWT/JWKS, mTLS | 🟢 5/5 |
| **Financial domain** | **None.** Logistics, airline, healthcare, media | 🔴 **1/5** |
| Columnar databases | Parquet only; no kdb+/ClickHouse/columnstore story | 🟠 2/5 |

**Summary: 11 strong, 5 medium, 2 weak. That is a hireable profile with two known holes.**

⚠️ **Your job on Monday:** be **undeniable** on the 11, **credible** on the 5, and **honest and
fast-learning** on the 2.

---

# PART 2 — THE CREDIBILITY RISK NOBODY WILL WARN YOU ABOUT

Your CV lists an enormous surface area — .NET, Node, Python, React, Angular, Vue, Blazor, Kafka,
Kubernetes, Terraform, eight vector databases, six agent frameworks…

⚠️ **An experienced interviewer's first instinct with a CV that broad is: *"how much of this is
real?"*** They will pick two or three items and drill until you break. **It's a test of honesty as
much as knowledge.**

## Your defence — the depth-first rule

> **When asked about anything on your CV, answer with one specific project, one specific problem, one
> specific decision, and what you'd do differently. Never answer with a definition.**

❌ *"Yes, we used Kafka. It's a distributed log with topics and partitions and consumer groups…"*

✅ *"On the 7X platform we ran Kafka on Event Hubs for editorial and billing events — about 200,000 a
day. The interesting problem was **ordering**: billing events had to stay ordered per subscription, so
I keyed partitions on subscription ID rather than event type. That cost us hot partitions when one big
customer spiked, so we…"*

**The second answer is unfakeable. It also makes them stop drilling, because they can hear it's
real.**

## The corollary — pre-emptive calibration

**Volunteer your own levels, early. It buys enormous trust.**

> *"Quick calibration so I don't waste your time: my deepest areas are .NET backend, distributed and
> event-driven systems, and Azure. Python and SQL are strong and hands-on.*
>
> *On WPF I'll be honest — I've been in web UI for years, and I've been rebuilding WPF hands-on
> recently rather than claiming it as day-job depth. And I've no capital markets background, which
> I'd want to talk about."*

⚠️ **Say that in the first five minutes and the whole interview changes tone** — from interrogation to
conversation. **Interviewers reward calibrated candidates, because calibrated candidates are safe to
put in front of a client.**

---

# PART 3 — YOUR REPOSITIONED NARRATIVE

## The problem

Your CV headline is **"Senior Full Stack AI Engineer"**. For this role that works **against** you.
It says: *will get bored on our WPF grid* · *wants to do LLMs, not order management* · *not a core
.NET person any more*.

## The fix — your headline for this process

> **"Senior .NET engineer who modernises enterprise platforms — desktop and services — with real-time
> data at the core, and a Python, analytics and cloud toolkit alongside it."**

## 🎤 Your 60-second pitch (memorise the *shape*, not the words)

> *"I'm a senior engineer with just over nine years, and **.NET has been the constant the whole way** —
> ASP.NET MVC and WCF in the early years, .NET 9 today.*
>
> *The thread through my career is **modernising business-critical platforms without breaking them**.
> At Calrom I moved airline reservation modules off .NET Framework and WCF onto ASP.NET Core with CQRS
> and event sourcing — live, mission-critical, with an audit requirement the old monolith couldn't
> meet. At GAC I architected the logistics platform — booking, cargo manifest and compliance — as
> .NET microservices with DDD, integrated with SAP and partner EDI. At my current client I lead
> backend architecture across content, billing and subscription domains, plus a real-time event
> pipeline doing around **200,000 events a day under 100 milliseconds**.*
>
> *Alongside .NET I use Python — FastAPI services, Pandas and NumPy — and I'm **Azure Solutions
> Architect Expert** certified.*
>
> *I've also spent the last couple of years on production AI work, **which I mention last on
> purpose**: it's a tool I can bring when it's useful, not the thing I'm looking for.*
>
> *What draws me to this role is the combination — real-time data, a proper desktop client, and a
> domain where the numbers actually have to be right. That's the kind of engineering I like."*

**Why it works:**
- Opens with .NET **and tenure in .NET** — kills "he's drifted to AI".
- "Modernising without breaking" maps exactly onto what they most likely need.
- Three concrete, **quantified** projects.
- ⚠️ **Defuses the AI question before they ask it.**
- Closes on **their** values: real-time, desktop, correctness.

**Timing: 60–75 seconds.** ⚠️ **Practise until you can say it without rushing. Record it.**

---

# PART 4 — THE 3-MINUTE PROJECT WALKTHROUGH (guaranteed question)

They **will** ask: *"Tell me about your current project — architecture, your role, the tech."*

## The structure: C.A.R.D.S.

| Step | Content | Time |
|---|---|---|
| **C**ontext | What the business does, who uses it, why it matters | 20 s |
| **A**rchitecture | The shape: services, data, integration, frontend | 60 s |
| **R**ole | ***Your*** specific ownership and decisions | 40 s |
| **D**ifficulty | **One hard problem, and how you solved it** | 45 s |
| **S**hould-have-done | What you'd change with hindsight | 15 s |

## The draft — say it out loud, then rewrite in your own words

> **Context:** *"7X is an enterprise technology and media platform in the UAE. I own the content,
> billing and subscription domains, plus the platform's real-time event pipeline."*
>
> **Architecture:** *"Backend is .NET 9 with Clean Architecture — Minimal APIs, CQRS via MediatR,
> EF Core over PostgreSQL as the system of record, Cosmos DB for globally distributed content, Redis
> for cache. Events flow through Kafka on Azure Event Hubs, roughly 200,000 a day. There's a
> federated GraphQL gateway unifying the .NET and Python services so the frontends deploy
> independently. Runs on Azure Container Apps, deployed with Terraform."*
>
> **Role:** *"I lead backend architecture — I own the ADRs, run design reviews, set the code-review
> standard, mentor the mid-level engineers. Concretely, I made the calls on the bounded contexts, the
> persistence choice per access pattern, and the resilience strategy."*
>
> **Difficulty:** *"The hardest problem was billing consistency. Billing touches four services and we
> had no distributed transactions. I implemented **SAGA with compensating transactions plus the outbox
> pattern**, with idempotency keys on every consumer. The failure mode we hit in testing was **partial
> compensation** — a compensating step itself failing — so we made compensations idempotent and
> replayable, and added a dead-letter path with a reconciliation job. The result is that a downstream
> failure degrades one workflow instead of cascading."*
>
> **Should-have-done:** *"With hindsight I'd have introduced the outbox from day one rather than
> retrofitting it, and I'd have added contract tests earlier."*

⚠️ **Practise the handoff.** End with: ***"— happy to go deeper on any part of that."***
It hands them the wheel and signals confidence.

⚠️ **Keep AI to one clause, or omit it entirely.** If they ask, you have plenty. If they don't, don't
spend your three minutes there.

## The backup story: GAC logistics — arguably better for this audience

Booking, cargo manifest and compliance as DDD bounded contexts · CQRS + EF Core · REST for partners,
gRPC for latency-critical internal calls · SAP and customs EDI integration via Service Bus · **Polly
circuit breakers on flaky partner endpoints** · SAGA across booking, cargo and compliance · SQL Server
for transactions, Mongo for country-varying documents · **Pact contract tests blocking breaking
changes**.

⚠️ **Say this connection out loud — it's one of your strongest moves:**
> *"The shape of that isn't far from order routing — **external partners you don't control, messages
> you must not lose or duplicate, and a compliance trail somebody will interrogate later.**"*

---

# PART 5 — SCRIPTS FOR THE HARD QUESTIONS

## 5.1 🔴 "How much WPF have you done?" — **assume this is asked**

⚠️ **Do not bluff.** The interviewer very likely maintains a WPF codebase and will detect it in two
questions.

> *"Straight answer: WPF isn't where my last few years have been — I've been in web UI, React and
> Angular, and Blazor for internal dashboards.*
>
> *What I do have is **the underlying model**. WPF's MVVM, data binding and change notification are
> the same ideas I use daily — `INotifyPropertyChanged` is conceptually what Angular's change
> detection and React's state model do. Binding, commands, converters and view-model discipline aren't
> new concepts to me.*
>
> *And since seeing this role I've been hands-on again. I built a small WPF app with a **real-time
> positions grid** — 5,000 rows, price ticks off a background thread about 20 times a second, MVVM
> with `ObservableCollection`, dispatcher marshalling, UI virtualisation.*
>
> ***That surfaced the real problem**: you can't raise a property-changed event per tick or you flood
> the dispatcher queue. So I conflated to the latest price per instrument and flushed the batch on a
> timer.*
>
> *So — I wouldn't claim ten years of WPF. I'd claim I know the platform's model, I'm actively
> hands-on, and with my .NET depth I'd be productive quickly. **If that's a hard blocker, better we
> both know now — but I don't think WPF is where the difficulty in this system lives.**"*

**Why this works:** honest → transferable depth → **evidence of action this week** → confident close →
subtly reframes WPF as the easy part.
⚠️ **The specific technical detail — dispatcher flooding, conflation, timer flush — is what proves you
actually did it.** A vague claim proves nothing.

**Then be ready for the drill.** `05` is what they'll ask next.

## 5.2 🔴 "You have no financial services background."

> *"That's right — my domains have been logistics, airline reservations, healthcare and enterprise
> media.*
>
> *What I'd say is that **the airline work at Calrom is closer than it looks**: mission-critical
> reservation and inventory systems, real-time seat and fare availability, integration with GDS and
> IATA partners over legacy protocols, and a compliance requirement that pushed us to event sourcing
> for a replayable audit trail.*
>
> ***Inventory under concurrency, external partners you don't control, and an auditor who needs to know
> why a number is what it is** — structurally that isn't far from orders, positions and executions.*
>
> *I've started reading into the domain properly — order lifecycle, OMS versus EMS versus PMS, FIX,
> the basics of NAV and P&L. **I know that's reading, not experience.** But I've picked up two complex
> domains from scratch before, and in both cases what mattered was sitting with the people who use the
> system. I'd expect the same here."*

⚠️ **Then turn it into a question — this converts a weakness into engagement:**
> *"Can I ask — how much domain knowledge does the team expect on day one versus picking up? And are
> the engineers close to the portfolio managers and traders, or is there a BA layer in between?"*

## 5.3 🟠 "Your CV is very AI-focused. Why this role?"

> *"Fair observation. The last two years I've done a lot of production AI, and I'm glad I did — but
> **what I actually enjoyed was the engineering**: making it a real production service with
> evaluation, tracing, cost control and release discipline. Not the model work itself.*
>
> *The constant across my whole career is .NET and building platforms that have to be correct and stay
> up.*
>
> *This role appeals because it's that engineering, in a domain where correctness genuinely matters and
> the data is real-time. And honestly, **capital markets is where I'd like to go deep** — real
> technical difficulty and real longevity, versus chasing whatever the current AI framework is. If AI
> becomes useful to the platform later I can bring it, but **I'm applying as a .NET engineer**."*

## 5.4 🟠 "VB.NET is in the specialization. Do you know it?"

> *"I haven't written VB.NET professionally — my .NET Framework years were C#. It's **the same CLR,
> the same base library, the same semantics**, so reading and maintaining it wouldn't be a problem;
> it's syntax on top of a runtime I know deeply.*
>
> *Is there a VB.NET component in the estate, or is that tag more about the C#/.NET specialization
> generally?"*

*(That last question is genuinely useful — it may just be Luxoft's internal taxonomy.)*

## 5.5 🟠 "You've moved jobs fairly often."

**Calm, non-defensive. Frame it as deliberate progression, never dissatisfaction.**

> *"Two of the moves were relocation-driven — I moved from Pakistan to the UAE, and my first UAE role
> was that move itself. That was a genuinely good platform build, but the opportunity at my current
> client was a step up into owning backend architecture end to end rather than one workstream, and it
> came up sooner than I'd planned.*
>
> *Before those, I was three years at Merik and three at Calrom — so **the longer pattern is that I
> stay where the work is substantial**. What I'm looking for now is exactly that: a long-horizon
> platform where depth compounds. Which is part of the appeal of a permanent role here."*

⚠️ **Never criticise a past employer or client. Not once, not mildly.**

## 5.6 "Why leave your current role? Why Luxoft?"

> *"Nothing's wrong where I am — I'd leave on good terms. Two reasons.*
>
> ***Permanence and depth**: I want to be on one serious platform for years rather than moving between
> engagements.*
>
> ***And the work itself**: real-time systems in capital markets is a harder and more durable
> engineering problem than what I'm building now.*
>
> *On Luxoft specifically — **I already work in the consultancy-embedded-at-client model and I'm good
> at it.** I'm on-site with my client today and did the same across multiple engagements at Merik. The
> difference is Luxoft's depth in financial services, which means the engagement isn't a one-off —
> there's a domain and a career path behind it."*

## 5.7 "Your biggest weakness?"

**Pick something true, bounded, and already being worked on.**

> *"Breadth versus depth. I've deliberately gone wide — .NET, Python, front-end, cloud, AI — and it's
> made me useful. But I've noticed the risk: I can end up the person who knows enough about everything
> rather than the deepest person in the room on anything.*
>
> ***That's actually part of why this role appeals** — I want to go deep in one domain. Practically, I
> manage it now by picking one area a quarter to go properly deep on, rather than adding another
> tool."*

⚠️ **Why this is the right answer:** it's honest, it **directly answers the credibility concern from
Part 2**, and it makes your breadth read as a considered choice rather than scattergun.

---

# PART 6 — CV TAILORING (30 minutes, before Monday)

You don't need a rewrite. You need a **repositioned top third.** The interviewer will have your CV
open in front of them.

| Change | From | To |
|---|---|---|
| **Title line** | "Senior Full Stack AI Engineer · Generative AI & Microservices" | **"Senior Full Stack Engineer · .NET & C# · Real-Time & Distributed Systems · Python · Azure"** |
| **First summary sentence** | "Senior Full Stack AI Engineer with 9+ years…" | "Senior .NET engineer with 9+ years building and modernising business-critical enterprise platforms — real-time, event-driven and transactional." |
| **Where AI sits** | Sentence 3 of 5 | **The last sentence. One line.** |
| **Competencies grid** | AI items first | .NET Platform Architecture · Event-Driven & Real-Time · DDD & CQRS · Distributed Systems · Solution Architecture … **then** AI |
| **Add (only if you build the app)** | — | *"Desktop/Windows: WPF & XAML (MVVM, data binding, Dispatcher — currently rebuilding hands-on), Windows Services"* |
| **Add one Calrom bullet** | — | *"real-time seat/fare inventory under concurrency"* — surfaces your closest-to-trading experience |

⚠️ **Do not add WPF as a bare skill-list item.** Bare-listing something you can't defend is the
fastest way to lose a technical interviewer's trust. **The parenthetical honesty above is what makes
it safe — and it's actually more impressive than a bare claim.**

---

# PART 7 — YOUR THREE SENTENCES, IF YOU REMEMBER NOTHING ELSE

1. *"**.NET has been the constant for nine years** — I modernise business-critical platforms without
   breaking them."*

2. *"My deepest areas are .NET backend, distributed and real-time event systems, and Azure. Python and
   SQL are strong and hands-on. **On WPF and capital markets I'll tell you exactly where I stand.**"*

3. *"**I work embedded at clients today** — that's the model I'm good at."*
