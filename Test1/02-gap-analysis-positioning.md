# 02 — Gap Analysis & Positioning

> This is the most important file in the pack. Read it twice. Say the scripts out loud.

---

## 1. Honest match matrix: your CV vs their must-haves

Rating = how you'd score **under real questioning**, not how it looks on paper.

| Requirement | Your evidence | Score | Action |
|---|---|---|---|
| 8+ yrs engineering / solution architecture | 9+ yrs, 2016→now, incl. architecture ownership & ADRs | 🟢 5/5 | Lead with it |
| .NET (C#) Advanced | .NET Framework 4.x → .NET 10, ASP.NET Core, EF Core, DDD/CQRS, MediatR, Polly, gRPC, SignalR | 🟢 5/5 | Your anchor. Must be flawless — `03` |
| **WPF Advanced** | **Nothing.** Closest: Blazor components, Angular/React MVVM-ish patterns, XAML-adjacent nothing | 🔴 1/5 | **Build the app + `05`. Honest script §5.1** |
| **Windows development** | .NET Framework era work, PowerShell, Windows-hosted services; no explicit desktop/MSI/Windows-service story | 🟠 2/5 | Reframe via `05` §11 |
| Python Advanced | FastAPI, asyncio, Pandas/NumPy/Scikit-learn, Celery, SQLAlchemy, PyTest, ML pipelines | 🟢 4/5 | Solid. Shore up GIL/async internals — `06` |
| JavaScript + framework (Medium) | React 19, Angular 2–20, Vue 3, TS depth, micro-frontends | 🟢 5/5 | Over-qualified. **Don't over-talk it.** |
| SQL | SQL Server/Azure SQL/PostgreSQL, T-SQL, window functions, CTEs, execution plans, partitioning, index design | 🟢 4.5/5 | Practise writing queries by hand — `07` §9 |
| MongoDB / unstructured | MongoDB, Cosmos DB, DynamoDB across 3 roles | 🟢 4.5/5 | Strong |
| **Real-time & multithreaded** | Kafka/Event Hubs 200K events/day <100ms, SignalR, Redis Streams, async/await, Channels — but **distributed** real-time, not **in-process** threading | 🟠 3/5 | **Biggest technical prep win. `04`** |
| Distributed design | SAGA, outbox, idempotency, CQRS, event sourcing, DDD, multi-cloud | 🟢 5/5 | Genuine strength |
| Azure | **AZ-305 certified**, deep service list, IaC, AKS/Container Apps | 🟢 5/5 | Certification is a real differentiator |
| Solution architecture | ADRs, design reviews, C4, quality-attribute analysis, tech lead roles | 🟢 4.5/5 | Strong |
| Agile + DevOps/CI-CD | Azure DevOps, GH Actions, Terraform, ArgoCD, quality gates, blue/green | 🟢 5/5 | Strong — keep answers short |
| Design patterns & algorithms | Patterns: excellent (GoF, DDD, enterprise). **Algorithms: unproven** — no competitive-programming signal | 🟠 3.5/5 | Do `16` coding problems |
| REST + auth protocols | OpenAPI 3.1, OAuth2/PKCE, OIDC, SAML, JWT/JWKS, mTLS, APIM | 🟢 5/5 | Strong |
| **Financial domain** | **None.** Logistics, airline, healthcare, media | 🔴 1/5 | `11` + honest script §5.2 |
| Columnar DBs | Parquet mentioned; no ClickHouse/kdb+/Snowflake/columnstore story | 🟠 2/5 | `07` §8 — learn the concept, be honest |
| Perf testing & profiling | k6, JMeter, Azure Load Testing, BenchmarkDotNet listed; less evidence of *profiler-driven* desktop/app tuning | 🟠 3/5 | `12` — cheap differentiator |

**Summary:** 11 strong, 5 medium, 2 weak. That is a **hireable profile with two known holes**.
Your job Monday is to be undeniable on the 11, credible on the 5, and *honest + fast-learning* on the 2.

---

## 2. The credibility risk nobody will tell you about

Your CV lists an enormous surface area — .NET, Node, Python, React, Angular, Vue, Blazor, Power
Platform, Kafka, K8s, Terraform, 8 vector databases, 6 agent frameworks, LangChain, MLflow…

An experienced interviewer's first instinct with a CV that broad is: **"how much of this is real?"**
They will pick two or three items and drill until you break. That is a *test of honesty as much as
knowledge*.

**Your defence — the depth-first rule:**
> When asked about anything on your CV, answer with **one specific project, one specific problem, one
> specific decision, and what you'd do differently.** Never answer with a definition.

❌ *"Yes, we used Kafka. It's a distributed log with topics and partitions and consumer groups…"*
✅ *"On the 7X platform we ran Kafka on Event Hubs for editorial and billing events — about 200K a day.
The interesting problem was ordering: billing events had to stay ordered per subscription, so I keyed
partitions on subscription ID rather than event type. That cost us hot partitions when one big
customer spiked, so we…"*

The second answer is unfakeable. It also makes them stop drilling, because they can hear it's real.

**And the corollary — pre-emptive calibration.** Early on, volunteer your own levels. It buys enormous
trust:
> *"Quick calibration so I don't waste your time: my deepest areas are .NET backend, distributed and
> event-driven systems, and Azure. Python and SQL are strong and hands-on. On WPF I'm honest —
> I've been in web UI for years and I've been rebuilding my WPF hands-on recently rather than
> claiming it as day-job depth. And I've no capital markets background, which I'd want to talk about."*

Say that in the first five minutes and the whole interview changes tone — from interrogation to
conversation. Interviewers reward calibrated candidates because calibrated candidates are safe to
deploy at a client.

---

## 3. Your repositioned narrative

### The problem
Your CV headline is **"Senior Full Stack AI Engineer"**. For this role that headline works *against*
you: it says "will get bored on our WPF grid", "wants to do LLMs, not order management", and "not a
core .NET person any more".

### The fix — your new headline (for this process only)
> **"Senior .NET engineer who modernises enterprise platforms — desktop and services — with real-time
> data at the core, and a Python/analytics and cloud toolkit alongside it."**

### Your 60-second pitch (memorise the shape, not the words)

> *"I'm a senior engineer with just over nine years, and .NET has been the constant the whole way —
> from ASP.NET MVC and WCF in the early years through to .NET 9 today.*
>
> *The thread through my career is modernising business-critical platforms without breaking them. At
> Calrom I moved airline reservation modules off .NET Framework and WCF onto ASP.NET Core with CQRS
> and event sourcing — mission-critical, live, with an audit requirement the old monolith couldn't
> meet. At GAC I architected the logistics platform — booking, cargo manifest and compliance — as
> .NET microservices with DDD, and integrated it with SAP and partner EDI. At my current client I
> lead backend architecture on .NET across content, billing and subscription domains, plus a real-time
> event pipeline doing around 200,000 events a day under 100 milliseconds.*
>
> *Alongside .NET I use Python — FastAPI services, Pandas and NumPy for analytics and ML inference —
> and I'm Azure Solutions Architect Expert certified. I've also spent the last couple of years doing
> production AI work, which I mention last on purpose: it's a tool I can bring when it's useful, not
> the thing I'm looking for.*
>
> *What draws me to this role is the combination — real-time data, a proper desktop client, and a
> domain where the numbers actually have to be right. That's the kind of engineering I like."*

**Why this works:**
- Opens with .NET and *tenure* in .NET (kills "he's drifted to AI").
- "Modernising without breaking" maps exactly to Reading A in `01` §4.
- Three concrete, quantified projects.
- Python + Azure cert covered.
- **Defuses the AI question before they ask it** — "I mention it last on purpose".
- Closes on *their* values: real-time, desktop, correctness.

**Timing:** 60–75 seconds. Practise until you can do it without rushing. Record it.

---

## 4. The 3-minute project walkthrough (guaranteed question)

They *will* ask: *"Tell me about your current project — architecture, your role, the tech."*
Luxoft's stage-3-style interviews lean heavily on this. Have **one** project ready in depth. Use
**7X (current)** as primary and **GAC logistics** as backup if they want something less AI-flavoured.

**Structure — C.A.R.D.S.:**

| Step | Content | ~Time |
|---|---|---|
| **C**ontext | What the business does, who uses it, why it matters | 20 s |
| **A**rchitecture | The shape: services, data, integration, frontend | 60 s |
| **R**ole | *Your* specific ownership and decisions | 40 s |
| **D**ifficulty | One hard problem, and how you solved it | 45 s |
| **S**houldhavedone | What you'd change with hindsight | 15 s |

**Draft (7X) — say it out loud, then rewrite in your own words:**

> **C:** *"7X is an enterprise technology and media platform in the UAE — composable digital products.
> The parts I own are the content, billing and subscription domains, plus the platform's real-time
> event pipeline."*
>
> **A:** *"Backend is .NET 9 with Clean Architecture — Minimal APIs and ASP.NET Core, CQRS via MediatR,
> EF Core over PostgreSQL as the system of record, with Cosmos DB for globally-distributed content
> and Redis for cache and session. Events flow through Kafka on Azure Event Hubs — roughly 200K a
> day. There's a GraphQL federated gateway on Node that unifies the .NET domain APIs and some Python
> services into one typed schema, so the React, Angular and Vue frontends can deploy independently.
> Runs on Azure Container Apps and AWS EKS, deployed with Terraform and ArgoCD."*
>
> **R:** *"I lead backend architecture: I own the ADRs, run design reviews, set the code-review
> standard, and mentor the mid-level engineers. Concretely, I made the calls on the bounded contexts,
> the persistence choices per access pattern, and the resilience strategy."*
>
> **D:** *"The hardest problem was billing consistency. Billing touches four services, and we had no
> distributed transactions. I implemented SAGA with compensating transactions plus the outbox pattern
> on Service Bus for exactly-once effects, with idempotency keys on every consumer. The failure mode
> we hit in testing was partial compensation — a compensating step itself failing — so we made
> compensations idempotent and replayable and added a dead-letter path with a reconciliation job.
> The result is that a downstream failure degrades one workflow instead of cascading."*
>
> **S:** *"With hindsight I'd have introduced the outbox from day one rather than retrofitting it, and
> I'd have invested in contract tests earlier — we added Pact later than we should have."*

**Practise the handoff:** end with *"— happy to go deeper on any part of that."* It hands them the
wheel and signals confidence.

⚠️ **In the 7X walkthrough, keep AI to one clause or omit it entirely on Monday.** If they ask, you
have plenty. If they don't, don't spend your 3 minutes there.

### Backup walkthrough: GAC logistics (use if they want non-AI / more domain-transactional)
Booking, cargo manifest, compliance as DDD bounded contexts on .NET 6 · CQRS + EF Core · REST
(OpenAPI 3.1) for partners, gRPC for latency-critical internal calls, GraphQL for dashboards · SAP
ERP / Dynamics 365 / customs EDI integration via Logic Apps + Service Bus with CloudEvents · Polly
circuit breakers on flaky partner endpoints · SAGA across booking/cargo/compliance · SQL Server for
transactions, Mongo for country-varying documents, DynamoDB for high-write tracking, Redis for
reference data · AKS primary + ECS Fargate DR · Pact contract tests blocking breaking changes.

**Why this one is arguably better for this audience:** partner integrations, transactional
correctness, compliance, mixed storage, resilience against unreliable external systems — that is
*structurally the same problem shape* as an order management system talking to brokers and custodians.
Say that connection out loud: *"the shape of it isn't far from order routing — external partners you
don't control, messages you must not lose or duplicate, and a compliance trail."*

---

## 5. Scripts for the hard questions

### 5.1 🔴 "How much WPF have you done?" *(assume this is asked)*

**Do not bluff.** The interviewer likely maintains a WPF codebase and will detect it in two questions.

> *"Straight answer: WPF isn't where my last few years have been — I've been in web UI, React and
> Angular, and Blazor for internal dashboards. What I do have is the underlying model. WPF's MVVM,
> data binding and change notification are the same ideas I use daily — `INotifyPropertyChanged` is
> conceptually what Angular's change detection and React's state model do, and I've built shared
> component libraries and design systems across three frameworks, so binding, commands, converters
> and view-model discipline aren't new concepts to me.*
>
> *Since seeing this role I've been hands-on again — I built a small WPF app with a real-time
> positions grid: 5,000 rows, price ticks coming off a background thread about 20 times a second,
> MVVM with `ObservableCollection`, dispatcher marshalling, and UI virtualisation so it doesn't fall
> over. That surfaced the real problems — you can't raise a property-changed event per tick or you
> flood the dispatcher queue, so I batched updates on a `Channel` and flushed on a timer.*
>
> *So: I'd not claim ten years of WPF. I'd claim I know the platform's model, I'm actively hands-on,
> and with my .NET depth I'd be productive in it quickly. If that's a hard blocker, better we both
> know now — but I don't think WPF is where the difficulty in this system lives."*

**Why this works:** honest → transferable depth → *evidence of action this week* → confident close →
subtly reframes WPF as the easy part. The specific technical detail (dispatcher flooding, batching on
a Channel) proves you actually did it.

**Then be ready for the follow-up drill** — `05` §5–10 covers what they'll ask next.

### 5.2 🔴 "You have no financial services background."

> *"That's right — my domains have been logistics, airline reservations, healthcare and enterprise
> media. What I'd say is that the airline work at Calrom is closer than it looks: mission-critical
> reservation and inventory systems, real-time seat and fare availability, integration with GDS and
> IATA NDC partners over legacy protocols, and a compliance requirement that pushed us to event
> sourcing for a replayable audit trail. Bookings and inventory under concurrency, external partners
> you don't control, and an auditor who needs to know why a number is what it is — structurally
> that's not far from orders, positions and executions.*
>
> *I've started reading into the domain properly — order lifecycle, OMS versus EMS versus a portfolio
> management system, FIX, the basics of NAV and P&L attribution. I know that's reading, not
> experience. But I've picked up two complex domains from scratch before — airline distribution and
> customs/logistics compliance — and in both cases the thing that mattered was sitting with the
> people who use the system. I'd expect the same here."*

**Then turn it into a question** — this converts a weakness into engagement:
> *"Can I ask — how much domain knowledge does the team expect on day one versus picking it up? And
> are the engineers close to the portfolio managers/traders, or is there a BA layer in between?"*

### 5.3 🟠 "Your CV is very AI-focused. Why this role?"

> *"Fair observation. The last two years I've done a lot of production AI, and I'm glad I did — but
> what I actually enjoyed about it was the engineering: making it a real production service with
> evaluation, tracing, cost control and release discipline, rather than the model work itself. The
> constant across my whole career is .NET and building platforms that have to be correct and stay up.*
>
> *This role appeals because it's that engineering, in a domain where correctness genuinely matters
> and the data is real-time. And honestly, capital markets is where I'd like to go deep — it's a
> domain with real technical difficulty and real longevity, versus chasing whatever the current AI
> framework is. If AI is useful to the platform later I can bring it, but I'm applying as a .NET
> engineer."*

### 5.4 🟠 "VB.NET is in the specialization. Do you know it?"

> *"I haven't written VB.NET professionally — my .NET Framework years were C#. It's the same CLR,
> same BCL, same framework semantics, so reading it and maintaining it wouldn't be a problem; it's
> syntax on top of a runtime I know deeply. Is there a VB.NET component in the estate, or is that
> tag more about the C#/.NET specialization generally?"*

(That last question is genuinely useful — it may just be Luxoft's internal taxonomy.)

### 5.5 🟠 "You've moved jobs fairly often. Why?" *(GAC was ~10 months)*

Have a calm, non-defensive answer. Frame around *deliberate progression*, not dissatisfaction.

> *"Two of the moves were relocation-driven — I moved from Pakistan to the UAE, and my first UAE role
> at GAC was the move itself. That role was a genuinely good platform build, but the opportunity at
> my current client was a step up into owning backend architecture end to end rather than one
> workstream, and it came up sooner than I'd planned. Before those, I was three years at Merik and
> three years at Calrom, so the longer pattern is that I stay where the work is substantial. What I'm
> looking for now is exactly that — somewhere with a long-horizon platform where depth compounds,
> which is part of the appeal of a permanent role here rather than another short consulting stint."*

⚠️ Never criticise a past employer or client. Not once, not mildly.

### 5.6 "Why are you leaving your current role?" / "Why Luxoft?"

> *"Nothing's wrong where I am — I'd leave on good terms. Two reasons. First, permanence and depth:
> I want to be on one serious platform for years rather than moving between engagements. Second, the
> work itself — real-time systems in capital markets is a harder and more durable engineering problem
> than what I'm building now. On Luxoft specifically: I already work in the consultancy-embedded-at-
> client model and I'm good at it — I'm on-site with my client today and did the same across multiple
> engagements at Merik. The difference is Luxoft's depth in financial services, which means the
> engagement isn't a one-off; there's a domain and a career path behind it."*

### 5.7 "What's your biggest weakness?" *(stage 2, but be ready)*
Pick something true, bounded and already being worked on. Suggested:
> *"Breadth versus depth. I've deliberately gone wide — .NET, Python, front-end, cloud, AI — and it's
> made me useful, but I've noticed the risk: I can end up the person who knows enough about
> everything rather than the deepest person in the room on anything. That's actually part of why this
> role appeals — I want to go deep in one domain. Practically, I manage it now by picking one area a
> quarter to go properly deep on rather than adding another tool."*

(Note: this is honest, it *directly answers* the credibility concern from §2, and it makes your
breadth read as a considered choice rather than a scattergun.)

---

## 6. CV tailoring — do this before Monday (30 min)

You don't need a rewrite, just a **repositioned top third**. The interviewer will have your CV open.

| Change | From | To |
|---|---|---|
| **Title line** | "Senior Full Stack AI Engineer · .NET & Cloud · Generative AI & Microservices" | **"Senior Full Stack Engineer · .NET & C# · Real-Time & Distributed Systems · Python · Azure"** |
| **Summary sentence 1** | "Senior Full Stack AI Engineer with 9+ years…" | "Senior .NET engineer with 9+ years building and modernising business-critical enterprise platforms — real-time, event-driven, and transactional." |
| **Summary: AI position** | Sentence 3 of 5 | Move to the **last** sentence, one line |
| **Core competencies grid** | AI items first (3 of the first 3) | Reorder: .NET Platform Architecture · Event-Driven & Real-Time Systems · Domain-Driven Design & CQRS · Distributed Systems · Polyglot Data · Solution Architecture … *then* AI items |
| **Skills: add a line** | — | Under .NET: *"Desktop/Windows: WPF & XAML (MVVM, data binding, Dispatcher — currently rebuilding hands-on), Windows Services, Blazor"* — **only if you build the app**, and word it exactly this honestly |
| **Add** | — | One line in the Calrom bullet: *"real-time seat/fare inventory under concurrency"* — surfaces your closest-to-trading experience |

⚠️ **Do not add WPF as a bare skill-list item.** Bare-listing something you can't defend is the single
fastest way to lose a technical interviewer's trust. The parenthetical honesty above is what makes it
safe — and it's actually *more* impressive than a bare claim.

---

## 7. Your three sentences, if you remember nothing else

1. *".NET has been the constant for nine years — I modernise business-critical platforms without
   breaking them."*
2. *"My deepest areas are .NET backend, distributed and real-time event systems, and Azure; Python
   and SQL are strong and hands-on; on WPF and capital markets I'll tell you exactly where I stand."*
3. *"I work embedded at clients today — that's the model I'm good at."*
