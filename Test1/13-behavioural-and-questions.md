# 13 — Behavioural Stories & Your Questions

> Compact by design — your priority is technical. This matters most for **stage 2 (hiring manager)**
> and **stage 3 (client)**, but a few of these come up on Monday too.

---

## 1. STAR, in one line
**S**ituation (10s) → **T**ask (10s) → **A**ction (**60s — the bulk, and all "I", not "we"**) →
**R**esult (**15s, with a number**). Then stop.

---

## 2. Eight stories from your actual CV — one line of scaffolding each, fill in from memory

| # | Story | Use it for |
|---|---|---|
| 1 | **Calrom: reservation modules off .NET Framework/WCF → ASP.NET Core, CQRS + event sourcing** because the monolith couldn't produce a replay-capable audit trail | Legacy modernisation · architecture ownership · **the best finance-adjacent story you have** |
| 2 | **7X billing consistency**: four services, no distributed transactions → SAGA + compensations + outbox + idempotency keys; hit partial-compensation failures in testing and made compensations idempotent and replayable | Hardest technical problem · distributed systems · rigour |
| 3 | **7X real-time pipeline**: Kafka on Event Hubs, 200K events/day, <100 ms, consumer-group partitioning, 99.99% delivery | Real-time · scale · quantified |
| 4 | **GAC: unreliable customs/partner endpoints** stalling the booking pipeline → Polly circuit breakers + retries, SAGA across booking/cargo/compliance | Resilience · integrating with systems you don't control |
| 5 | **GAC: Pact consumer-driven contract tests** so a breaking schema change failed the build instead of becoming a partner incident | Quality engineering · preventing production incidents |
| 6 | **Merik: on-prem → Azure migrations** across client engagements; monoliths → .NET 5/6 on AKS; release cadence monthly → weekly | Cloud · delivery improvement · client-facing |
| 7 | **Mentoring**: two engineers onto the DDD/CQRS codebase at GAC; set the code-review standard and authored the ADRs at 7X | Leadership · seniority |
| 8 | **Merik/7X client-facing**: scoping, estimating, presenting architecture options to client stakeholders, on-site delivery | **Luxoft cares about this a lot** — you're being hired to sit with a client |

**Have ready:** a **failure** story (what went wrong, what you owned, what changed afterwards — never
blame anyone), a **disagreement** story (technical conflict resolved with data or a spike, not
seniority), and a **tight deadline** story (what you cut and how you communicated the trade-off).

---

## 3. Questions they'll ask, with the shape of your answer

| Question | Shape |
|---|---|
| Biggest technical challenge | Story 2 or 1. Lead with the constraint, not the tech. |
| Disagreement with a colleague | Listened → reframed as a trade-off → agreed a test/spike → went with the data. |
| A production incident you caused | Own it fully, describe the fix, then the **systemic** change (test, alert, guardrail). |
| How do you mentor? | Code review as teaching, pairing on risky work, ADRs so decisions are learnable. |
| How do you handle unclear requirements? | Ask who the user is and what decision the output supports; prototype; short feedback loop. |
| Why Luxoft / why leaving? | Permanence + depth in one serious platform; already good at the embedded-consultant model; Luxoft's financial-services depth means a domain, not a one-off engagement. |
| Salary | *"Yevheniia shared the 25–35k range and it works. I'd focus on fit today."* Later: aim at the top of band given 9 yrs + AZ-305; clarify whether housing/flights/medical/schooling are inside or outside the number, plus visa, relocation from Dubai, and gratuity. |
| Notice period / start date | Know your exact notice. Be precise, not vague. |
| Weakness | Breadth vs depth — deliberate, aware of the risk, now picking one area a quarter to go deep. Part of why this role appeals. |

⚠️ Never criticise a current or past employer or client. Not once.

---

## 4. Questions **you** ask (pick 3 for Monday, save the rest)

**Technical (best for Monday):**
1. Is this greenfield or extending an existing platform? What's the split between the desktop client,
   the services behind it, and the Python/analytics side? *(This one tells you how to aim everything
   else — ask it early if you get the chance.)*
2. Where does WPF sit — one flagship app or several tools? Is any of the estate still .NET Framework?
3. What's the hardest technical problem the team has right now?
4. How real-time is real-time here — is this streaming prices to a desk, or more analytics and
   batch cycles?
5. What does the testing and release process look like for the desktop client specifically?

**Role & team (better for stages 2–3):**
6. Who's the end client, and what does the team composition look like?
7. How much domain knowledge is expected on day one versus picked up on the job? How close are
   engineers to the portfolio managers or traders?
8. What does success look like for this person at six months?
9. How does Luxoft support engineers embedded at a client — career path, training, domain onboarding?
10. What's the on-site expectation in Abu Dhabi, and how does the team work day to day?

**Never ask on Monday:** salary, holidays, remote policy, promotion timelines.

---

## 5. Closing the call

> *"Thanks — this was a good conversation. Honestly, this is the kind of engineering I want to be
> doing: real-time, correctness-critical, with a proper desktop client and a domain where the numbers
> matter. I'm aware WPF and capital markets are where I'd be building up, and I'd rather be straight
> about that than oversell — but the .NET, distributed systems and data side is exactly my ground.
> What are the next steps?"*

---

## 6. Follow-up email (send within 4 hours, to Yevheniia; keep it 6 lines)

> Subject: Thank you — Senior Full Stack Developer technical discussion
>
> Hi Yevheniia,
>
> Thank you for arranging today's technical discussion — please pass my thanks to [interviewer name]
> as well. I enjoyed it, particularly the discussion around [one specific technical topic they raised].
>
> It reinforced my interest in the role: the combination of real-time data, a .NET desktop client and
> a domain where correctness genuinely matters is exactly the kind of engineering I want to be doing.
> [Optional, one line: *"On the WPF point that came up — I've been rebuilding hands-on with a
> real-time positions grid, and I'm happy to share it if useful."*]
>
> I'd be glad to move to the next stage whenever suits.
>
> Kind regards,
> Muhammad Awais

**Write down the interviewer's name in the first 60 seconds of the call** — you'll want it for this
email and you will not remember it afterwards.
