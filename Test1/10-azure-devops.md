# 10 — Azure, DevOps & CI/CD

> JD: *"Microsoft Azure experience (preferred)"*, *"Agile and DevOps/CI-CD knowledge"*.
> **This is your strongest area and you're AZ-305 certified.** The risk here is the opposite of the
> other files: **over-answering**. Keep answers to 30–45 seconds, then stop and offer depth.

---

## 1. How to answer cloud questions in *this* interview

The JD says "Windows development", WPF, real-time, on-prem-flavoured. So:

❌ *"I'd deploy it to Container Apps with ArgoCD and Terraform…"* (as a reflex answer to everything)
✅ *"Where does this run today — on-prem, Azure, hybrid?"* then answer for **their** world.

Financial institutions in the Gulf frequently run **hybrid**: regulated workloads on-prem or in a
sovereign region, with cloud for analytics, dev/test and non-sensitive workloads. Data residency is
a real constraint (UAE data-residency rules, plus internal policy). **Mentioning data residency
unprompted is a strong signal for an Abu Dhabi financial client.**

---

## 2. Azure services — the map you already know, ordered for this role

| Need | Service | One-line why |
|---|---|---|
| Host .NET APIs | App Service / Container Apps / AKS | App Service for simple, Container Apps for serverless containers + KEDA scaling, AKS when you need full control |
| Event-driven compute | Functions (incl. **Durable Functions** for orchestration/SAGA) | |
| Messaging | **Service Bus** (queues/topics, sessions for ordering, DLQ), **Event Hubs** (high-throughput streaming, Kafka protocol), Event Grid (reactive events) | Know which is which — a very common question |
| Relational | **Azure SQL** (elastic pools, geo-replication, Always Encrypted), PostgreSQL Flexible Server | |
| Document/NoSQL | Cosmos DB (partition key + RU/s design, change feed, consistency levels) | |
| Cache | Azure Cache for Redis | cache-aside, pub/sub, distributed lock |
| Storage | Blob (hot/cool/archive tiers, immutable/**WORM** storage — *matters for regulatory retention*) | |
| Identity | **Entra ID**, managed identities, **workload identity federation**, Entra External ID | "no secrets at all" |
| Secrets | Key Vault (+ rotation, RBAC, Private Endpoint) | |
| API layer | API Management (products, policies, quotas, self-hosted gateway for on-prem) | |
| Networking | VNet, Private Endpoints, Front Door, App Gateway + WAF, ExpressRoute (for a bank's on-prem link) | |
| Observability | Monitor, Log Analytics + **KQL**, Application Insights | |
| Governance | Azure Policy, Blueprints, Management Groups, Defender for Cloud, Cost Management | |
| Analytics | Synapse / Fabric, Data Factory, Databricks | if the analytics conversation comes up |

**Cosmos DB consistency levels** (a classic AZ-305 question): Strong → Bounded Staleness → Session
(default) → Consistent Prefix → Eventual. Trade latency/availability against consistency.

**Service Bus vs Event Hubs vs Event Grid** — the answer:
> *"Service Bus is enterprise messaging: queues, topics, sessions for ordered processing per key,
> dead-letter queues, transactions — for commands and workflows I can't lose. Event Hubs is a
> high-throughput ingestion stream with partitions and consumer offsets, Kafka-compatible — for
> telemetry and market-data-scale volume. Event Grid is a lightweight reactive event router for
> 'something happened' notifications."*

---

## 3. Well-Architected Framework (name the five pillars — AZ-305 vocabulary)
**Reliability · Security · Cost Optimisation · Operational Excellence · Performance Efficiency.**
Answer design questions against these pillars and you sound like an architect rather than a coder.

---

## 4. CI/CD

**Pipeline stages to describe:** build → unit tests → static analysis (SonarQube) + secret scan →
package/containerise → **container image scan (Trivy)** + sign (Cosign) → deploy dev → integration/
contract tests → deploy QA (approval gate) → **DB migration** → deploy prod (approval) → smoke tests →
automated rollback.

**Points that read as senior:**
- **Build once, promote the same artefact** through environments. Never rebuild per environment;
  configuration comes from the environment, not the build.
- **Database migrations are the hard part.** Expand/contract: add nullable column → backfill → deploy
  code that writes both → switch reads → drop old. Never a breaking migration in the same release as
  the code that needs it.
- **Deployment strategies**: blue/green (instant switch + rollback), canary (percentage rollout),
  rolling, **feature flags** to decouple deploy from release. In finance add: **release windows**
  (never during market hours), change approval/CAB, and **segregation of duties** — the person who
  writes the code can't be the only one approving prod. Saying that shows regulatory awareness.
- **Desktop CI/CD is different** — that's the twist for this role: building an MSI/MSIX, code signing
  the binaries (EV certificate), versioning, an auto-update channel, and staged rollout to user
  groups. Deploying a desktop app to 200 traders is a *distribution* problem, not a `kubectl apply`.
  **Raise this yourself — it shows you've thought about their actual world.**
- **IaC**: Terraform (modules, remote state, `plan` review in PR) or Bicep/ARM in a pure-Microsoft
  shop. Idempotent, reviewed, no click-ops.
- **Branching**: trunk-based with short-lived branches and feature flags (preferred) vs GitFlow
  (release-train shops). Say which and why — for a regulated release cadence GitFlow-ish still shows up.
- **Quality gates**: coverage threshold, no new critical Sonar issues, no high/critical CVEs.

---

## 5. Observability

- **OpenTelemetry** for traces/metrics/logs; structured logging with **correlation/trace IDs**
  propagated across every hop (W3C `traceparent`).
- **RED** (Rate, Errors, Duration) for services; **USE** (Utilisation, Saturation, Errors) for
  resources; golden signals.
- **SLIs/SLOs with error budgets and burn-rate alerting**; alert on symptoms users feel, not on CPU.
- Desktop telemetry: crash reporting, client-side latency, feature usage — the client app needs
  observability too, and most teams neglect it. Another good unprompted point.
- KQL example (Application Insights) — being able to write one is a small flex:
  ```kql
  requests
  | where timestamp > ago(1h) and success == false
  | summarize count() by name, resultCode
  | order by count_ desc
  ```

---

## 6. Agile / delivery — keep it short and concrete
Scrum vs Kanban (fixed sprints and commitments vs flow and WIP limits — pick per team). Your habits to
name: refinement and estimation, definition of done, ADRs for decisions, design reviews, PR standards,
pairing on risky changes, blameless post-incident reviews, runbooks. In a client-embedded consultancy
role: **status transparency and no surprises** is the delivery skill they're buying.

---

## 7. Rapid-fire

1. IaaS vs PaaS vs SaaS → you manage OS+ vs runtime managed vs product.
2. Managed identity vs service principal → Azure-managed credentials, no secrets vs manually managed.
3. Availability zones vs regions → intra-region fault isolation vs geographic DR.
4. RPO vs RTO → data loss tolerance vs downtime tolerance.
5. Scale up vs out; **KEDA** for event-driven autoscaling on queue depth.
6. Private Endpoint vs Service Endpoint → private IP in your VNet vs optimised public route.
7. Blob tiers & immutability → cost tiers; WORM for regulatory retention.
8. Cost control → right-sizing, reserved instances/savings plans, autoscale-to-zero, tagging +
   showback, budget alerts.
9. Terraform state → remote backend with locking; never local; `plan` reviewed in PR.
10. Secret rotation → Key Vault + short-lived credentials + workload identity federation = no secrets
    in pipelines.
11. Zero-downtime deploy for a stateful service → rolling with readiness probes, connection draining,
    backwards-compatible schema.
12. Hybrid connectivity → ExpressRoute/VPN, self-hosted APIM gateway, Azure Arc, on-prem data gateway.
