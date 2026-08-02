# 10 — AZURE, DEVOPS & CI/CD, IN PLAIN ENGLISH

> The job says *"Azure (preferred)"* and *"Agile and DevOps/CI-CD"*.
>
> ⚠️ **This is your strongest area, and the risk here is the opposite of every other file:
> over-answering.** Keep each answer to **30–45 seconds**, then stop and offer depth.
> Nobody is worried you can't do cloud. Don't spend interview minutes proving it.

---

# EASY MEMORY NOTES

Read this first. Start with the short phrase. Say the simple line. Add the last column only if they
ask for more.

| Remember | Say it simply | If they ask more |
|---|---|---|
| **Ask where it runs** | First ask: on-prem, Azure, or hybrid? | Finance often has data-residency rules. |
| **Three event tools** | Service Bus for important messages, Event Hubs for streams, Event Grid for notifications. | Service Bus has queues, topics, and dead-letter queues. |
| **Build once** | Build once, then move the same package through environments. | Config changes by environment; the build does not. |
| **DB changes are risky** | Database migrations are the hardest part of release. | Add, backfill, switch, then remove old schema later. |
| **Deploy is not release** | You can deploy code without turning it on. | Feature flags, blue/green, and canary help rollback. |
| **No secrets** | Use identity instead of storing passwords. | Managed identity and Key Vault reduce secret risk. |
| **Desktop rollout** | Desktop apps need installation and updates. | MSI/MSIX, signing, Intune/SCCM, staged rollout. |
| **Watch the system** | Use metrics, logs, and traces together. | Correlation IDs connect one request across services. |
| **No market-hours deploy** | In finance, release timing matters. | Change approval and separation of duties also matter. |

---

# PART 0 — THE 8 ANSWERS THAT WIN

| # | The question | Full answer in simple words |
|---|---|---|
| 1 | **Any hosting question** | "First I ask where the system runs today: on-prem, Azure, or hybrid. A financial client may have data-residency and network constraints, so the right architecture depends on that answer." |
| 2 | **Service Bus vs Event Hubs vs Event Grid** | "Service Bus is for important business messages and workflows. Event Hubs is for very high-volume streams. Event Grid is for lightweight notifications that something happened." |
| 3 | **The CI/CD principle** | "Build once, then move the same package through dev, test, and production. Environment-specific settings come from config or secrets, not from rebuilding the code." |
| 4 | **The hard part of CI/CD** | "Database migrations are the risky part because rollback is hard. I change schema in safe steps: add, backfill, run compatible code, switch reads, and remove old fields later." |
| 5 | **Deployment strategies** | "Blue/green gives quick rollback by switching traffic. Canary rolls out to a small group first. Feature flags let me deploy code without releasing the feature immediately." |
| 6 | **The finance twist** | "In finance I also consider release windows, change approval, and separation of duties. I would not deploy during market hours unless there is a controlled emergency process." |
| 7 | **The desktop twist** | "A WPF desktop app is a distribution problem. It needs MSI or MSIX, code signing, versioning, update channels, staged rollout, and a rollback story for users who cannot restart immediately." |
| 8 | **Data residency** | "For an Abu Dhabi financial client I would ask where data is allowed to live. Some workloads may need to stay on-prem or in approved regions, while analytics or dev/test may use cloud." |

---

# PART 1 — HOW TO ANSWER CLOUD QUESTIONS IN *THIS* INTERVIEW

The job description says **Windows development**, **WPF**, **real-time**. That's an on-prem-flavoured
shop.

❌ **Don't** reflexively answer *"I'd put it in Container Apps with Terraform and ArgoCD."*
✅ **Do** ask: *"Where does this run today — on-prem, Azure, or hybrid?"* — then answer for their
reality.

**Say this once, and it does a lot of work:**
> *"Financial institutions in the Gulf commonly run hybrid — regulated workloads on-prem or in a
> sovereign region, with cloud for analytics, dev/test and non-sensitive workloads. **Data residency
> is a real constraint**, both regulatory and internal policy. So I'd want to know where the line sits
> before designing anything."*

**Mentioning data residency unprompted is a strong signal for an Abu Dhabi financial client.**

---

# PART 2 — THE AZURE MAP, ORDERED FOR THIS ROLE

| Need | Service | Why |
|---|---|---|
| Host .NET APIs | App Service / Container Apps / AKS | App Service for simple; Container Apps for serverless containers with KEDA; AKS when you need full control |
| Event-driven compute | Functions, and **Durable Functions** for orchestration and SAGA | |
| Messaging | **Service Bus**, **Event Hubs**, **Event Grid** | Know which is which — a very common question |
| Relational | **Azure SQL** — elastic pools, geo-replication, Always Encrypted | |
| Document | Cosmos DB — partition key design, RU/s, change feed | |
| Cache | Azure Cache for Redis | Cache-aside, pub/sub, distributed lock |
| Storage | Blob — hot/cool/archive tiers, and **immutable WORM storage** | ⚠️ *WORM matters for regulatory retention* |
| Identity | **Entra ID**, managed identities, **workload identity federation** | "No secrets at all" |
| Secrets | Key Vault, with rotation and Private Endpoint | |
| API layer | API Management — products, policies, quotas, **self-hosted gateway for on-prem** | |
| Networking | VNet, Private Endpoints, App Gateway + WAF, **ExpressRoute** for a bank's on-prem link | |
| Observability | Monitor, Log Analytics with **KQL**, Application Insights | |
| Governance | Azure Policy, Management Groups, Defender for Cloud, Cost Management | |

## The messaging question — memorise this answer

**Say:**
> *"**Service Bus** is enterprise messaging — queues, topics, **sessions for ordered processing per
> key**, dead-letter queues, transactions. That's for commands and workflows I can't lose.*
>
> ***Event Hubs** is a high-throughput ingestion stream with partitions and consumer offsets, and it's
> Kafka-compatible. That's for telemetry and market-data-scale volume.*
>
> ***Event Grid** is a lightweight reactive router for 'something happened' notifications."*

## Cosmos DB consistency levels (a classic AZ-305 question)

**Strong → Bounded Staleness → Session (the default) → Consistent Prefix → Eventual.**
You're trading latency and availability against consistency.

## The Well-Architected pillars — name them

**Reliability · Security · Cost Optimisation · Operational Excellence · Performance Efficiency.**
**Say:** *"I'd answer a design question against those five pillars."* It makes you sound like an
architect rather than a coder.

---

# PART 3 — CI/CD

## 3.1 The pipeline, described end to end

> build → unit tests → static analysis and secret scan → package or containerise →
> **image scan and sign** → deploy to dev → integration and contract tests → deploy QA (approval) →
> **database migration** → deploy prod (approval) → smoke tests → automated rollback

## 3.2 The four points that read as senior

**1. Build once, promote the same artefact.**
*"Never rebuild per environment. The binary that goes to production is byte-for-byte the one that
passed the tests. Configuration comes from the environment, not from the build."*

**2. Database migrations are the hard part.**
*"**Expand and contract.** Add the nullable column, backfill it, deploy code that writes to both, then
switch reads, then drop the old one. **Never ship a breaking migration in the same release as the code
that needs it** — because then you can't roll either one back."*

**3. Deployment strategy.**
*"Blue/green gives an instant switch and instant rollback. Canary rolls out to a percentage.
**Feature flags decouple deploying from releasing**, which is the one that changes how a team works."*

⚠️ **Then add the finance layer — this is what distinguishes you:**
*"In a regulated shop you also have **release windows — never during market hours** — change approval,
and **separation of duties**: the person who wrote the code should not be the only person approving
production."*
**That sentence shows regulatory awareness without being asked.**

**4. ⚠️ Desktop CI/CD is a different problem — raise this yourself.**
*"Deploying a desktop app to 200 traders is a **distribution** problem, not a deployment one. You're
building an MSI or MSIX, **code signing with an EV certificate**, versioning, running an auto-update
channel, and staging the rollout by user group — usually pushed through SCCM or Intune. And you need a
rollback story when a trader can't restart mid-session."*

**Raising that unprompted shows you've thought about their actual world, not a generic cloud one.**

## 3.3 The rest

- **Infrastructure as code:** Terraform (modules, remote state with locking, `plan` reviewed in the PR)
  or Bicep in a pure-Microsoft shop. *"Idempotent, reviewed, no click-ops."*
- **Branching:** *"Trunk-based with short-lived branches and feature flags is what I prefer. But in a
  regulated release-train shop, GitFlow-ish still shows up, and that's a reasonable fit."*
- **Quality gates:** coverage threshold, no new critical issues, no high or critical CVEs.

---

# PART 4 — OBSERVABILITY

- **OpenTelemetry** for traces, metrics and logs. Structured logging with a **correlation ID
  propagated across every hop** (W3C `traceparent`).
- **RED** for services — Rate, Errors, Duration. **USE** for resources — Utilisation, Saturation,
  Errors.
- **SLIs and SLOs with error budgets and burn-rate alerting.**
  ⚠️ *"And alert on symptoms users feel, not on CPU. CPU at 90% isn't an incident; a p99 above target
  is."*
- ⚠️ **Desktop telemetry — another good unprompted point:**
  *"The client app needs observability too — crash reporting, client-side latency, feature usage. Most
  teams instrument the services and completely neglect the desktop app, so when a trader says 'it was
  slow at 9:31' there's no data."*

**A KQL query — being able to write one is a small flex:**
```kql
requests
| where timestamp > ago(1h) and success == false
| summarize count() by name, resultCode
| order by count_ desc
```

---

# PART 5 — AGILE AND DELIVERY (keep it short and concrete)

**Scrum vs Kanban:** fixed sprints and commitments versus flow with WIP limits. *"Pick per team."*

**Your habits to name, quickly:** refinement and estimation, a real definition of done, **ADRs** for
decisions, design reviews, PR standards, pairing on risky changes, blameless post-incident reviews,
runbooks.

⚠️ **The line that matters for a consultancy role:**
> *"In a client-embedded role, the delivery skill they're actually buying is **status transparency and
> no surprises**. Bad news early is a feature."*

---

# PART 6 — RAPID-FIRE: 25 QUESTIONS

| # | Q | A |
|---|---|---|
| 1 | IaaS / PaaS / SaaS | You manage the OS / the runtime is managed / it's a product |
| 2 | Managed identity vs service principal | Azure-managed credentials, no secrets vs manually managed |
| 3 | Workload identity federation | Trust an external issuer — **no secrets in pipelines at all** |
| 4 | Availability zone vs region | Fault isolation inside a region vs geographic DR |
| 5 | RPO vs RTO | How much data you can lose vs how long you can be down |
| 6 | Service Bus vs Event Hubs | Enterprise messaging you can't lose vs high-throughput streaming |
| 7 | Event Grid | Lightweight "something happened" event routing |
| 8 | Ordered processing in Service Bus | **Sessions**, keyed per entity |
| 9 | Cosmos consistency levels | Strong → Bounded → **Session (default)** → Prefix → Eventual |
| 10 | Cosmos partition key | Decides everything. Avoid a monotonically increasing key |
| 11 | KEDA | Event-driven autoscaling — scale on queue depth, not CPU |
| 12 | Private Endpoint vs Service Endpoint | A private IP in your VNet vs an optimised public route |
| 13 | Blob immutability / WORM | Write-once storage for regulatory retention |
| 14 | Well-Architected pillars | Reliability, Security, Cost, Operations, Performance |
| 15 | Build once, promote | The same artefact through every environment |
| 16 | Zero-downtime migration | Expand and contract |
| 17 | Blue/green vs canary | Instant switch vs percentage rollout |
| 18 | Feature flags | Decouple deploying from releasing |
| 19 | Segregation of duties | The author can't be the only prod approver |
| 20 | Desktop deployment | MSI/MSIX, code signing, update channel, staged rollout |
| 21 | Terraform state | Remote backend with locking. Never local. `plan` reviewed in the PR |
| 22 | Secret rotation | Key Vault plus short-lived credentials plus federation |
| 23 | Correlation ID | Propagate through every hop — W3C `traceparent`, OpenTelemetry |
| 24 | RED vs USE | Rate/Errors/Duration for services; Utilisation/Saturation/Errors for resources |
| 25 | Alert on what? | Symptoms users feel, not CPU |
