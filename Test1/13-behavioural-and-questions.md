# 13 — BEHAVIOURAL & YOUR QUESTIONS, IN PLAIN ENGLISH

> Short by design. Your priority is technical. This matters most for **stage 2 (hiring manager)** and
> **stage 3 (client)** — but a few come up in the first round too.

---

# PART 0 — THE 6 RULES

| # | Rule | Why |
|---|---|---|
| 1 | **Answer, then stop talking.** | Over-talking is the most common way seniors lose points. Silence is the interviewer's turn. |
| 2 | **Say "I", not "we".** | They're assessing *you*. "We" hides what you actually did. |
| 3 | **End with a number.** | "Release cadence went from monthly to weekly." Numbers are memorable and most candidates have none. |
| 4 | **Never criticise a past employer or client.** | Not once. It's the fastest way to become a risk. |
| 5 | **Own failures fully, then describe the systemic fix.** | "I caused it, here's what I changed so it can't recur" is a senior answer. Blame is a junior one. |
| 6 | **Write the interviewer's name down in the first 60 seconds.** | You will not remember it afterwards, and you need it for the follow-up email. |

---

# PART 1 — STAR, IN ONE LINE

**S**ituation *(10 seconds)* → **T**ask *(10 seconds)* → **A**ction *(**60 seconds — the bulk, all
"I"**)* → **R**esult *(**15 seconds, with a number**)*. **Then stop.**

⚠️ **The mistake to avoid:** spending 90 seconds on the situation. The interviewer doesn't need the
backstory. They need to know **what you personally did**.

---

# PART 2 — YOUR EIGHT STORIES

One line of scaffolding each — fill in the detail from memory.

| # | The story | Use it for |
|---|---|---|
| **1** | **Calrom** — moved reservation modules off .NET Framework/WCF onto ASP.NET Core with CQRS and **event sourcing**, because the monolith couldn't produce a replay-capable audit trail | Legacy modernisation · architecture ownership · ⚠️ **your best finance-adjacent story** |
| **2** | **7X billing consistency** — four services, no distributed transactions → SAGA with compensations, outbox, idempotency keys. Hit partial-compensation failures in testing and made the compensations idempotent and replayable | Hardest technical problem · distributed systems · **rigour** |
| **3** | **7X real-time pipeline** — Kafka on Event Hubs, **200,000 events a day, under 100 ms, 99.99% delivery**, consumer-group partitioning | Real-time · scale · **quantified** |
| **4** | **GAC** — unreliable customs and partner endpoints stalling the booking pipeline → Polly circuit breakers and retries, SAGA across booking, cargo and compliance | Resilience · integrating with systems you don't control |
| **5** | **GAC** — Pact consumer-driven contract tests, so a breaking schema change failed the build instead of becoming a partner incident | Quality engineering · preventing incidents |
| **6** | **Merik** — on-prem to Azure migrations, monoliths to .NET 5/6 on AKS, release cadence **monthly → weekly** | Cloud · delivery improvement · client-facing |
| **7** | **Mentoring** — brought two engineers onto the DDD/CQRS codebase, set the code-review standard, authored the ADRs | Leadership · seniority |
| **8** | **Client-facing** — scoping, estimating, presenting architecture options to client stakeholders, on-site delivery | ⚠️ **Luxoft cares about this a lot** — you're being hired to sit with a client |

## The three you must also have ready

- **A failure.** What went wrong, what you owned, what changed afterwards. **Never blame anyone.**
- **A disagreement.** Resolved with data or a timeboxed spike — not by seniority.
- **A tight deadline.** What you cut, and **how you communicated the trade-off**.

---

# PART 3 — THEIR QUESTIONS, AND THE SHAPE OF YOUR ANSWER

| They ask | The shape |
|---|---|
| **Biggest technical challenge** | Story 2 or 1. **Lead with the constraint, not the technology.** |
| **A disagreement with a colleague** | Listened → reframed it as a trade-off → agreed a spike → went with the data. |
| **A production incident you caused** | Own it fully → the immediate fix → then **the systemic change** (a test, an alert, a guardrail). |
| **How do you mentor?** | Code review as teaching · pairing on risky work · ADRs so decisions are learnable. |
| **Unclear requirements?** | Ask who the user is and **what decision the output supports**. Prototype. Short feedback loop. |
| **Why Luxoft / why leaving?** | Permanence and depth in one serious platform. Already good at the embedded-consultant model. Luxoft's financial-services depth means a **domain**, not a one-off engagement. |
| **Salary** | *"Yevheniia shared the range and it works for me — I'd rather focus on the technical fit today."* **Do not discuss money in round one.** |
| **Notice period** | Know your **exact** notice. Be precise, not vague. |
| **Weakness** | Breadth versus depth — deliberate, aware of the risk, and now picking one area a quarter to go deep on. **Part of why this role appeals.** |

---

# PART 4 — THE TWO HONEST ANSWERS (know the shape, not a script)

## WPF

> *"I haven't been in WPF recently — I've been in web UI for years. But the model is the same one I use
> daily: MVVM, binding and change notification are exactly what Angular and React do with a different
> vocabulary.*
>
> *And I've been rebuilding hands-on recently — a real-time positions blotter, 5,000 rows, 20 ticks a
> second, `ObservableCollection`, dispatcher marshalling, virtualisation. What I learned is that you
> **have to** batch onto a channel and flush on a timer, or you flood the dispatcher and the UI dies.*
>
> *I'd be productive quickly. And honestly, WPF isn't where the difficulty in a system like this
> lives."*

## Finance

> *"No capital markets background — I want to be straight about that.*
>
> *But airline reservations at Calrom is closer than it looks: mission-critical inventory under
> concurrency, GDS and IATA partner integration, and a compliance requirement that's exactly why we
> chose event sourcing.*
>
> *I've started on the domain — order lifecycle, OMS versus EMS versus PMS, FIX, NAV. And I've learned
> two hard domains from scratch before.*
>
> ***How much domain knowledge do you expect on day one, versus picking it up?***"

⚠️ **Both answers end well:** the WPF one ends with a reframe, the finance one ends with a question.
**Never let an honest answer end on the gap.**

---

# PART 5 — QUESTIONS **YOU** ASK

**Pick three for the first round. Save the rest.**

## Technical — best for round one

1. ⚠️ **"Is this greenfield, or extending an existing platform? And what's the split between the
   desktop client, the services behind it, and the Python/analytics side?"**
   *Ask this early. The answer tells you where to aim every subsequent answer. It's the single most
   valuable question you can ask.*
2. *"Where does WPF sit — one flagship app, or several tools? And is any of the estate still .NET
   Framework?"*
3. *"What's the hardest technical problem the team has right now?"*
4. *"How real-time is real-time here — streaming prices to a desk, or more analytics and batch
   cycles?"*
5. *"What does testing and release look like for the desktop client specifically?"*

## Role and team — better for stages 2 and 3

6. *"Who's the end client, and what does the team look like day to day?"*
7. *"How much domain knowledge is expected on day one? How close do engineers sit to the portfolio
   managers and traders?"*
8. *"What does success look like for this person at six months?"*
9. *"How does Luxoft support engineers embedded at a client — career path, training, domain
   onboarding?"*

⚠️ **Never ask in round one:** salary, holidays, remote policy, promotion timelines.

---

# PART 6 — CLOSING THE CALL

> *"Thanks — this was a good conversation. Honestly, this is the kind of engineering I want to be
> doing: real-time, correctness-critical, with a proper desktop client and a domain where the numbers
> actually matter.*
>
> *I'm aware WPF and capital markets are where I'd be building up, and I'd rather be straight about
> that than oversell — but the .NET, distributed systems and data side is exactly my ground.*
>
> ***What are the next steps?***"

---

# PART 7 — THE FOLLOW-UP EMAIL

**Send within four hours. Keep it six lines.**

> **Subject:** Thank you — Senior Full Stack Developer technical discussion
>
> Hi Yevheniia,
>
> Thank you for arranging today's technical discussion — please pass my thanks to **[interviewer
> name]** as well. I enjoyed it, particularly the discussion around **[one specific technical topic
> they raised]**.
>
> It reinforced my interest in the role: the combination of real-time data, a .NET desktop client and
> a domain where correctness genuinely matters is exactly the kind of engineering I want to be doing.
>
> I'd be glad to move to the next stage whenever suits.
>
> Kind regards,
> Muhammad Awais

⚠️ **The two blanks are the whole point.** A generic thank-you email is worthless. Naming the
interviewer and one specific topic proves you were present and engaged.

**So: write the interviewer's name and one topic down during the call.**
