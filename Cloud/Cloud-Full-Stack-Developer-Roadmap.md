# Cloud Roadmap for a Full-Stack Developer

This guide combines the cloud skills a full-stack developer should learn across AWS, Azure, and Google Cloud Platform (GCP), including AI/ML services.

The goal is not to memorize every service. The goal is to understand how cloud applications are deployed, secured, monitored, scaled, and connected to managed services.

## 1. Main Cloud Skillset

A full-stack developer should focus on:

```text
Frontend Hosting
+ Backend/API Hosting
+ Database
+ Object Storage
+ Authentication
+ Networking
+ CI/CD
+ Monitoring
+ Security
+ Cost Control
+ AI/ML Services
+ Infrastructure as Code
```

These are the core areas used in real production applications.

## 2. Same Concepts Across AWS, Azure, and GCP

| Area | What You Learn | AWS | Azure | GCP |
|---|---|---|---|---|
| Frontend hosting | Static apps, CDN, HTTPS | S3 + CloudFront | Static Web Apps / Blob + CDN | Firebase Hosting / Cloud Storage + CDN |
| Backend hosting | APIs, services, containers | Lambda, ECS, App Runner | App Service, Functions, Container Apps | Cloud Run, App Engine, Cloud Functions |
| Virtual machines | Full server control | EC2 | Virtual Machines | Compute Engine |
| Containers | Run packaged apps | ECS / EKS | Container Apps / AKS | Cloud Run / GKE |
| Kubernetes | Container orchestration | EKS | AKS | GKE |
| Relational database | PostgreSQL, MySQL, SQL Server | RDS / Aurora | Azure SQL / Azure Database for PostgreSQL | Cloud SQL / AlloyDB |
| NoSQL database | Flexible document/key-value data | DynamoDB | Cosmos DB | Firestore / Bigtable |
| Object storage | Images, files, documents, backups | S3 | Blob Storage | Cloud Storage |
| Identity and access | Users, roles, service permissions | IAM, Cognito | Entra ID, RBAC, Managed Identity | IAM, Identity Platform |
| Secrets | API keys, passwords, tokens | Secrets Manager | Key Vault | Secret Manager |
| Networking | Private networks, subnets, routing | VPC | Virtual Network | VPC |
| DNS | Domain management | Route 53 | Azure DNS | Cloud DNS |
| Load balancing | Route traffic to services | Elastic Load Balancing | Azure Load Balancer / Application Gateway | Cloud Load Balancing |
| Queue/events | Async jobs, background processing | SQS, SNS, EventBridge | Service Bus, Event Grid | Pub/Sub, Eventarc |
| CI/CD | Build and deploy from Git | CodePipeline / GitHub Actions | Azure DevOps / GitHub Actions | Cloud Build / GitHub Actions |
| Monitoring | Logs, metrics, alerts | CloudWatch | Azure Monitor | Cloud Monitoring |
| Infrastructure as Code | Create cloud resources from code | Terraform / CDK / CloudFormation | Terraform / Bicep | Terraform |

## 3. How a Cloud Application Works Together

A normal production full-stack application looks like this:

```text
User
 -> DNS
 -> CDN / Load Balancer
 -> Frontend App
 -> Backend API
 -> Auth Service
 -> Database
 -> Object Storage
 -> Queue / Background Worker
 -> Monitoring / Logs / Alerts
 -> Cost and Security Controls
```

Example deployment flow:

```text
Developer pushes code to GitHub
 -> CI/CD pipeline builds frontend and backend
 -> Backend Docker image goes to a container registry
 -> Backend deploys to App Runner / App Service / Cloud Run
 -> Frontend deploys to static hosting/CDN
 -> Backend reads secrets from secret manager
 -> Backend connects to managed database
 -> User uploads files to object storage
 -> Long-running work goes to queue
 -> Worker processes background jobs
 -> Logs and metrics go to monitoring
```

## 4. AI/ML Cloud Services for Full-Stack Developers

For a full-stack developer, AI/ML usually means adding AI capabilities to applications. You do not need to start with deep model training or GPU infrastructure.

| AI/ML Area | What You Learn | AWS | Azure | GCP |
|---|---|---|---|---|
| Generative AI / LLM apps | Chat, summarization, extraction, classification | Amazon Bedrock | Microsoft Foundry / Azure OpenAI | Vertex AI / Gemini |
| ML platform | Train, deploy, manage models | SageMaker AI | Azure Machine Learning | Vertex AI |
| RAG / knowledge search | Chat with documents and private data | Bedrock Knowledge Bases / OpenSearch | Azure AI Search | Vertex AI Search / Vector Search |
| Embeddings | Convert text into searchable vectors | Bedrock / Titan Embeddings | Azure OpenAI Embeddings | Vertex AI Embeddings |
| Document extraction | Read invoices, PDFs, forms | Textract | Document Intelligence | Document AI |
| Vision AI | Image analysis, labels, OCR | Rekognition | Azure AI Vision | Cloud Vision |
| Speech | Speech-to-text and text-to-speech | Transcribe / Polly | Azure Speech | Speech-to-Text / Text-to-Speech |
| Translation | Translate app content | Translate | Azure Translator | Cloud Translation |
| AI safety | Content filters and safety controls | Bedrock Guardrails | Azure AI Content Safety | Vertex AI safety settings |
| AI monitoring | Track usage, latency, quality, cost | CloudWatch + Bedrock logs | Azure Monitor + Foundry tools | Cloud Monitoring + Vertex AI tools |

## 5. Typical AI Full-Stack Architecture

```text
Frontend
 -> Backend API
 -> Auth
 -> AI Service / LLM
 -> Vector Search
 -> Database
 -> Object Storage
 -> Queue / Worker
 -> Logs / Metrics / Cost Monitoring
```

Example RAG application:

```text
User uploads PDF
 -> File stored in object storage
 -> Worker extracts text from document
 -> Text is chunked into smaller sections
 -> Embeddings are created
 -> Embeddings are stored in vector search
 -> User asks a question
 -> Backend searches relevant document chunks
 -> Backend sends context + question to LLM
 -> LLM returns answer with supporting context
```

## 6. Best Learning Path

Follow this order:

1. Deploy a frontend app with custom domain and HTTPS.
2. Deploy a backend API.
3. Connect a managed PostgreSQL or MySQL database.
4. Add object storage for file uploads.
5. Add authentication and authorization.
6. Add CI/CD from GitHub.
7. Add logs, metrics, and alerts.
8. Add queue-based background jobs.
9. Add secrets management.
10. Add AI API integration.
11. Add RAG with document upload and vector search.
12. Add Infrastructure as Code with Terraform or Bicep.
13. Learn scaling, backups, disaster recovery, and cost optimization.

## 7. Recommended Project to Learn Everything

Build one real project:

```text
AI Document Assistant
```

Features:

- User login
- Upload PDF/documents
- Store files in object storage
- Extract document text
- Save metadata in database
- Generate embeddings
- Search documents using vector search
- Ask questions using an LLM
- Show citations or source chunks
- Process long jobs with a queue and worker
- Deploy frontend and backend to cloud
- Use secret manager for API keys
- Add logs, metrics, and alerts
- Use CI/CD for automatic deployment
- Use Terraform or Bicep for infrastructure

This one project covers most practical full-stack cloud skills.

## 8. Recommended Stack by Cloud

### AWS

```text
React/Next.js
+ App Runner or Lambda
+ RDS PostgreSQL
+ S3
+ Cognito
+ SQS
+ Bedrock
+ OpenSearch or Bedrock Knowledge Bases
+ CloudWatch
+ Secrets Manager
+ Terraform or AWS CDK
```

### Azure

```text
React/Next.js
+ App Service or Container Apps
+ Azure Database for PostgreSQL
+ Blob Storage
+ Entra ID
+ Service Bus
+ Microsoft Foundry / Azure OpenAI
+ Azure AI Search
+ Azure Monitor
+ Key Vault
+ Bicep or Terraform
```

### GCP

```text
React/Next.js
+ Cloud Run
+ Cloud SQL or Firestore
+ Cloud Storage
+ Identity Platform
+ Pub/Sub
+ Vertex AI / Gemini
+ Vertex AI Search or Vector Search
+ Cloud Monitoring
+ Secret Manager
+ Terraform
```

## 9. What to Prioritize

For a full-stack developer, prioritize:

```text
Cloud Deployment
 -> Managed Database
 -> Object Storage
 -> Authentication
 -> CI/CD
 -> Monitoring
 -> Security
 -> AI API Integration
 -> RAG
 -> Infrastructure as Code
```

Do not start with:

- Training large models
- GPU clusters
- Advanced ML theory
- Multi-cloud architecture
- Complex Kubernetes

Learn those later only if your job or project needs them.

## 10. Production Checklist

Before calling a cloud app production-ready, check:

- HTTPS is enabled.
- Domain is configured.
- Secrets are not stored in code.
- Database has backups.
- Object storage permissions are restricted.
- IAM permissions follow least privilege.
- Logs are available.
- Metrics and alerts are configured.
- CI/CD pipeline is working.
- Rollback plan exists.
- Costs are monitored.
- AI usage is rate-limited.
- AI prompts and outputs avoid leaking private data.
- Long-running AI jobs use queues/workers.
- Infrastructure is documented or managed as code.

## 11. Complete Phase-by-Phase Cloud Production Plan

This plan covers cloud delivery from every practical perspective: business, product, architecture, frontend, backend, data, AI, security, privacy, networking, infrastructure, DevOps, SRE, QA, cost, compliance, support, governance, and long-term operations. Use it as a complete execution checklist for AWS, Azure, GCP, or a provider-neutral cloud project.

### Perspective Coverage Map

| Perspective | What it protects | Required outputs |
|---|---|---|
| Business | Value, timeline, budget, customer impact, operational fit | Business case, success metrics, cost target, launch goal |
| Product | User workflows, scope, acceptance criteria, release priorities | PRD, user journeys, MVP scope, backlog, acceptance criteria |
| UX/frontend | User experience, responsive behavior, accessibility, error recovery | UI flows, design system, frontend deployment plan, edge-state inventory |
| Backend/API | Contracts, performance, reliability, data access, integrations | API contracts, service boundaries, error model, scaling strategy |
| Cloud architecture | Provider choice, managed services, hosting model, resilience | Architecture diagram, Well-Architected review, ADRs |
| Infrastructure | Networks, compute, storage, databases, identity, environments | Terraform/Bicep/CDK modules, environment matrix, resource inventory |
| Security | IAM, secrets, network exposure, encryption, vulnerabilities | Threat model, IAM design, secret policy, security scan reports |
| Privacy/compliance | PII, consent, retention, data residency, audit requirements | Data map, compliance checklist, retention policy, audit evidence |
| DevOps | CI/CD, environments, release automation, rollback | Pipelines, deployment runbook, rollback plan, release checklist |
| SRE/operations | Monitoring, alerting, incident response, availability, recovery | Dashboards, alerts, SLOs, incident runbook, DR plan |
| QA/testing | Functional quality, regression safety, integration confidence | Test matrix, E2E tests, contract tests, load tests, smoke tests |
| Data | Schema design, migration safety, backup, recovery, quality | Data model, migration plan, backup policy, restore tests |
| AI/ML | Prompt safety, model usage, RAG quality, token cost, latency | AI architecture, eval set, guardrails, cost controls, monitoring |
| Cost/finance | Hosting cost, AI cost, data transfer, scaling expense | Cost estimate, budgets, alerts, tagging strategy, optimization plan |
| Support | Diagnosability, user issue handling, escalation, known issues | Support runbook, debug metadata, admin tools, escalation path |
| Legal/procurement | Licenses, cloud contracts, vendor terms, data processing | Vendor review, license review, DPA/SCC review if needed |
| Governance | Ownership, approvals, standards, risk control | RACI, risk register, decision log, review gates |

### Master Phase Overview

| Phase | Name | Primary question | Main outputs | Exit gate |
|---|---|---|---|---|
| 0 | Initiation and constraints | Why are we building this cloud system? | Business case, stakeholders, constraints, risks | Sponsor approves goal, budget, timeline, and success metrics |
| 1 | Cloud provider and strategy | Which cloud and service model fit best? | Provider decision, region plan, service model ADR | Cloud choice is justified by product, team, compliance, and cost |
| 2 | Product and workload discovery | What workloads, users, data, and workflows exist? | PRD, workload inventory, data classification, acceptance criteria | Critical flows and workload requirements are approved |
| 3 | Architecture and service design | How will the system be structured? | Architecture diagram, service boundaries, integration plan | Architecture review passes Well-Architected concerns |
| 4 | Accounts, subscriptions, projects, and governance | How is the cloud estate controlled? | Account/subscription/project layout, IAM baseline, tagging policy | Environments and ownership are isolated and governed |
| 5 | Networking and connectivity | How will traffic enter, leave, and stay private? | VPC/VNet design, DNS, TLS, ingress/egress, firewall rules | Network paths are documented, private where needed, and testable |
| 6 | Identity, access, and secrets | Who and what can access resources? | IAM roles, service identities, secret stores, rotation plan | Least privilege and secret handling are verified |
| 7 | Infrastructure as Code foundation | Can infrastructure be reproduced safely? | Terraform/Bicep/CDK modules, state management, CI checks | Clean IaC plan/apply works in non-production |
| 8 | Compute and application hosting | Where do frontend, backend, workers, and jobs run? | Hosting setup, container/serverless/VM plan, autoscaling | Apps deploy successfully with health checks |
| 9 | Data stores, storage, and migration | Where does data live and how is it protected? | Database/storage setup, schema, migrations, backup policy | Backup, restore, migration, and access tests pass |
| 10 | Messaging, events, and background work | How is async work processed reliably? | Queue/event architecture, worker plan, retry/DLQ policy | Failed jobs are retried, dead-lettered, and observable |
| 11 | CI/CD and environment promotion | How does code reach production safely? | Build pipeline, deploy pipeline, preview/staging/prod flow | Automated build, test, deploy, smoke, and rollback pass |
| 12 | Security hardening | Is the system secure enough for real users and data? | Threat model, scans, encryption, CSP, WAF, vulnerability policy | No high/critical unresolved security issues remain |
| 13 | Privacy, compliance, and audit readiness | Does data handling satisfy obligations? | Data map, retention, residency, audit logs, compliance evidence | Compliance owner approves launch readiness |
| 14 | Observability and operations | Can the team see and diagnose production behavior? | Logs, metrics, traces, dashboards, alerts, SLOs | Test incidents generate useful alerts and dashboards |
| 15 | Performance, scale, and reliability | Will the system survive expected load and failures? | Load test, scaling policy, DR plan, resilience tests | Performance and recovery targets pass |
| 16 | AI/ML and RAG readiness, if applicable | Are AI features safe, useful, measurable, and cost-controlled? | Prompt design, eval set, guardrails, vector strategy, AI monitoring | Quality, safety, latency, and cost thresholds pass |
| 17 | Cost management and optimization | Is spending visible and controlled? | Budgets, alerts, tags, unit cost model, optimization backlog | Cost owner approves budget and alerting |
| 18 | QA, release candidate, and go-live | Is the release ready for users? | Test report, release checklist, runbooks, go/no-go decision | Product, engineering, QA, security, DevOps, and support approve |
| 19 | Post-launch stabilization | What did production reveal? | Launch report, defect triage, metric review, support summary | Blocking issues are resolved or actively mitigated |
| 20 | Long-term maintenance and evolution | Can the platform stay healthy? | Upgrade calendar, security cadence, cost reviews, roadmap | Ongoing ownership and maintenance cadence are active |

### Phase 0: Initiation and Constraints

| Area | Required actions |
|---|---|
| Business | Define the business problem, expected value, target users, budget, delivery date, and operational impact. |
| Product | Define the initial scope, critical workflows, user roles, non-goals, and measurable outcomes. |
| Engineering | Identify existing systems, legacy dependencies, backend constraints, frontend constraints, integration needs, team skills, and migration pressure. |
| Security/compliance | Identify data sensitivity, regulated data, customer commitments, audit requirements, encryption needs, and access constraints. |
| Operations | Define uptime expectations, support hours, incident severity levels, release windows, recovery expectations, and rollback expectations. |
| Deliverables | Project brief, stakeholder map, assumption log, constraint list, initial risk register, success metrics. |
| Verification | Stakeholders agree on why the system exists, what success means, and which constraints cannot be violated. |
| Exit gate | No provider or architecture decision starts until goal, budget, timeline, and owners are explicit. |

### Phase 1: Cloud Provider and Strategy

| Area | Required actions |
|---|---|
| Provider choice | Compare AWS, Azure, and GCP against team skill, current company ecosystem, managed service fit, compliance, region availability, AI needs, and cost. |
| Service model | Decide static hosting, serverless, containers, managed platform, Kubernetes, VMs, or hybrid based on operational capacity and workload needs. |
| Region strategy | Choose primary region, secondary region if needed, latency targets, data residency, disaster recovery distance, and service availability. |
| Multi-cloud | Avoid multi-cloud unless there is a real regulatory, acquisition, resiliency, or vendor-risk requirement. |
| Governance | Decide landing zone/account structure, environment separation, naming standards, tagging, budget ownership, and access approval process. |
| Deliverables | Provider ADR, service model ADR, region decision, landing zone outline, high-level cost estimate. |
| Verification | Provider choice is defensible from business, technical, compliance, cost, and hiring perspectives. |
| Exit gate | The team can explain why this cloud and this service model are better than the alternatives for this project. |

### Phase 2: Product and Workload Discovery

| Area | Required actions |
|---|---|
| Product | Document users, roles, user journeys, acceptance criteria, feature priorities, launch scope, and post-launch backlog. |
| Workloads | Inventory frontend, backend APIs, background jobs, scheduled jobs, file processing, AI tasks, databases, caches, queues, third-party integrations, and admin tools. |
| Traffic | Estimate users, requests per second, peak load, file sizes, data volume, AI token usage, background job volume, and growth assumptions. |
| Data | Classify data by sensitivity, retention, residency, ownership, backup needs, deletion needs, and sharing restrictions. |
| QA | Convert product requirements into test scenarios, failure cases, browser/device needs, API contract needs, and load test assumptions. |
| Deliverables | PRD, workload inventory, traffic estimate, data classification, test scenario map, acceptance criteria. |
| Verification | Every workload has owner, runtime target, data dependency, security classification, scaling assumption, and failure expectation. |
| Exit gate | Architecture cannot proceed until workloads and data requirements are clear enough to size and secure. |

### Phase 3: Architecture and Service Design

| Area | Required actions |
|---|---|
| Architecture | Draw end-to-end architecture: DNS, CDN, load balancer, frontend, API, auth, database, storage, queues, workers, AI services, observability, and CI/CD. |
| Boundaries | Define service boundaries, API contracts, data ownership, sync vs async flows, integration points, and failure isolation. |
| Resilience | Decide redundancy, health checks, retries, timeouts, circuit breakers, idempotency, backup/restore, and DR approach. |
| Security | Identify trust boundaries, public/private resources, IAM roles, network exposure, encryption, and secret paths. |
| Operations | Define deployment units, scaling model, maintenance windows, SLOs, alerts, on-call expectations, and runbook needs. |
| Deliverables | Architecture diagram, sequence diagrams for critical flows, ADRs, API contracts, data flow diagram, resilience plan. |
| Verification | Architecture is reviewed against operational excellence, security, reliability, performance, cost, and sustainability. |
| Exit gate | The architecture has no undocumented critical path, hidden public exposure, or ownerless component. |

### Phase 4: Accounts, Subscriptions, Projects, and Governance

| Area | Required actions |
|---|---|
| Structure | Create or define cloud accounts/subscriptions/projects for dev, test, staging, production, shared services, logging, and security if needed. |
| Ownership | Assign owners for each environment, resource group, workload, budget, IAM role, and deployment pipeline. |
| Policies | Define naming, tagging/labeling, approved regions, approved services, encryption rules, public access rules, backup rules, and deletion protection. |
| Access | Establish break-glass access, admin roles, developer roles, CI/CD roles, read-only audit roles, and approval workflow. |
| Audit | Enable cloud audit logs, billing exports, security posture tools, and configuration history. |
| Deliverables | Cloud estate layout, governance policy, tag policy, access policy, audit logging baseline. |
| Verification | Production is isolated from development, all resources are owned and tagged, and privileged access is controlled. |
| Exit gate | No production resources are created in an unmanaged or ownerless cloud environment. |

### Phase 5: Networking and Connectivity

| Area | Required actions |
|---|---|
| DNS/TLS | Configure domain strategy, DNS zones, certificates, HTTPS, redirect rules, HSTS, and certificate renewal. |
| Network layout | Design VPC/VNet, subnets, route tables, NAT, private endpoints, service endpoints, load balancers, and ingress/egress paths. |
| Public exposure | Decide which services are public, private, internal-only, partner-facing, or admin-only. |
| Security controls | Add firewall rules, security groups/NSGs, WAF where needed, DDoS protection if needed, and egress restrictions. |
| Connectivity | Plan VPN, private connectivity, database private access, third-party allowlists, webhook access, and local developer access. |
| Deliverables | Network diagram, DNS plan, TLS plan, firewall rules, ingress/egress policy, connectivity test plan. |
| Verification | Direct traffic paths, blocked traffic paths, and private resource access are tested. |
| Exit gate | No database, secret store, internal API, or admin surface is publicly exposed by accident. |

### Phase 6: Identity, Access, and Secrets

| Area | Required actions |
|---|---|
| User identity | Choose Cognito, Entra ID, Identity Platform, Auth0, custom auth, or existing enterprise identity based on user base and compliance. |
| Service identity | Use managed identities/service accounts/roles for workloads instead of static credentials whenever possible. |
| IAM | Apply least privilege for developers, CI/CD, runtime services, databases, storage, queues, AI services, and observability. |
| Secrets | Store secrets in Secrets Manager, Key Vault, or Secret Manager; define rotation, access logging, and emergency revocation. |
| Authorization | Define RBAC/ABAC, tenant boundaries, admin roles, object-level permissions, and backend enforcement. |
| Deliverables | IAM matrix, identity flow, secret inventory, rotation policy, permission tests. |
| Verification | Permission tests prove services can only access required resources and denied access fails safely. |
| Exit gate | No long-lived privileged key, shared admin credential, or hard-coded secret remains. |

### Phase 7: Infrastructure as Code Foundation

| Area | Required actions |
|---|---|
| Tooling | Choose Terraform, Bicep, CDK, CloudFormation, or Pulumi based on team standards and cloud provider. |
| State | Configure remote state, locking, encryption, workspace/environment separation, and state access controls. |
| Modules | Build reusable modules for network, compute, database, storage, IAM, secrets, observability, and CI/CD. |
| Validation | Add formatting, linting, security scanning, policy checks, plan review, and drift detection. |
| Promotion | Define how infrastructure changes move from dev to staging to production. |
| Deliverables | IaC repo/modules, backend state config, CI validation, environment variables, plan/apply runbook. |
| Verification | A clean environment can be created and destroyed where appropriate from code, with reviewed plans. |
| Exit gate | Manual console-created production resources are exceptions, documented, and tracked for IaC import or retirement. |

### Phase 8: Compute and Application Hosting

| Area | Required actions |
|---|---|
| Frontend | Deploy static frontend to CDN/static hosting or SSR frontend to managed/server/container hosting with cache and route fallback rules. |
| Backend | Deploy APIs to serverless, containers, managed app services, Kubernetes, or VMs based on workload and operational needs. |
| Workers | Deploy background workers, scheduled jobs, and long-running processors separately from request/response APIs. |
| Containers | Define Dockerfile, base image policy, image scanning, registry, tagging, build cache, and runtime config. |
| Health | Add health checks, readiness checks, startup checks, graceful shutdown, autoscaling metrics, and deployment probes. |
| Deliverables | Hosting environment, container registry, deployment manifests, health endpoints, autoscaling policy, runtime config. |
| Verification | Frontend, API, and workers deploy from pipeline, pass health checks, and expose only intended endpoints. |
| Exit gate | No workload reaches production without health checks, logs, config separation, and rollback path. |

### Phase 9: Data Stores, Storage, and Migration

| Area | Required actions |
|---|---|
| Database | Choose relational, NoSQL, cache, search, vector, or analytical stores based on access patterns and consistency needs. |
| Schema | Design schemas, indexes, constraints, migrations, seed data, tenant partitioning, and retention rules. |
| Storage | Configure object buckets/containers with private defaults, lifecycle rules, encryption, versioning, malware scanning if needed, and signed URL policy. |
| Backup | Enable automated backups, point-in-time restore, retention, restore testing, and deletion protection. |
| Migration | Define zero-downtime migration rules, rollback rules, data backfill strategy, and compatibility between old/new app versions. |
| Deliverables | Data model, migration scripts, storage policy, backup policy, restore test report, data access tests. |
| Verification | Restore from backup works, migrations are reversible or safely forward-only, and object storage is not publicly readable unless intentional. |
| Exit gate | Production data launch is blocked until backup, restore, migration, and access controls are proven. |

### Phase 10: Messaging, Events, and Background Work

| Area | Required actions |
|---|---|
| Async design | Decide queues, topics, event buses, schedulers, streams, and worker concurrency for long-running or unreliable tasks. |
| Reliability | Implement retries, backoff, idempotency keys, dead-letter queues, poison message handling, deduplication, and timeout policy. |
| Observability | Track message age, queue depth, worker errors, DLQ count, retry count, processing duration, and failed payload metadata. |
| Security | Restrict queue access, encrypt messages, avoid sensitive payloads where possible, and control event publisher/subscriber permissions. |
| Deliverables | Queue/event architecture, worker code, retry/DLQ policy, async test cases, operational dashboard. |
| Verification | Failed jobs are retried, dead-lettered, visible in dashboards, and recoverable without data corruption. |
| Exit gate | No critical long-running process depends on a user request staying open or a manually watched job. |

### Phase 11: CI/CD and Environment Promotion

| Area | Required actions |
|---|---|
| CI | Run install, lint, typecheck, unit tests, integration tests, IaC validation, security scans, build, and artifact upload. |
| CD | Deploy to preview/dev/staging/production using versioned artifacts and environment-specific config. |
| Promotion | Promote the same artifact across environments instead of rebuilding differently for production when possible. |
| Release safety | Add smoke tests, approvals for production, canary/blue-green if needed, feature flags, and automated rollback triggers where feasible. |
| Traceability | Tag releases with commit SHA, build number, image digest, IaC version, migration version, and deploy actor. |
| Deliverables | CI/CD pipelines, artifact registry, deployment environments, smoke tests, release notes, rollback automation. |
| Verification | A test change can move through pipeline to staging and roll back without manual cloud-console work. |
| Exit gate | Production deploys are repeatable, traceable, and reversible. |

### Phase 12: Security Hardening

| Area | Required actions |
|---|---|
| Threat model | Review users, attackers, trust boundaries, public endpoints, admin functions, data stores, third-party services, and AI paths. |
| Application security | Test XSS, CSRF, SSRF, injection, auth bypass, broken access control, insecure uploads, dependency vulnerabilities, and unsafe redirects. |
| Cloud security | Review IAM, public buckets, public databases, security groups, private endpoints, encryption, key management, audit logs, and admin access. |
| Edge/security services | Configure WAF, rate limiting, bot protection, DDoS protection, security headers, and CSP where appropriate. |
| Supply chain | Scan dependencies, containers, IaC, secrets, licenses, and build pipeline permissions. |
| Deliverables | Threat model, vulnerability reports, remediation plan, WAF/rate-limit policy, security headers, secret scan report. |
| Verification | Security findings are severity-ranked, blocking findings are fixed, and risk acceptances are explicit. |
| Exit gate | No unresolved high/critical vulnerability, exposed secret, public private-data store, or known auth bypass remains. |

### Phase 13: Privacy, Compliance, and Audit Readiness

| Area | Required actions |
|---|---|
| Data map | Document PII, sensitive data, regulated data, log data, analytics data, AI prompts, AI outputs, files, and backups. |
| Consent | Implement cookie consent, analytics consent, AI data usage consent, marketing consent, and preference management if needed. |
| Retention | Define retention, deletion, export, anonymization, backup expiration, and legal hold behavior. |
| Residency | Confirm region placement, cross-region replication, vendor subprocessors, and customer contractual restrictions. |
| Audit | Enable audit logs for identity, admin actions, data access, deployments, secret access, and infrastructure changes. |
| Deliverables | Data map, privacy review, retention policy, audit log plan, compliance evidence, customer/security questionnaire answers. |
| Verification | Compliance owner can trace where sensitive data enters, moves, rests, is logged, is backed up, and is deleted. |
| Exit gate | Production launch is blocked if data handling violates customer, legal, or regulatory requirements. |

### Phase 14: Observability and Operations

| Area | Required actions |
|---|---|
| Logs | Centralize structured application logs, access logs, audit logs, deployment logs, worker logs, and AI usage logs where allowed. |
| Metrics | Track request rate, error rate, latency, saturation, CPU/memory, DB connections, queue depth, storage growth, cache hit rate, and AI usage. |
| Traces | Add distributed tracing across frontend, API, database, queues, workers, third-party calls, and AI calls where useful. |
| Alerts | Define actionable alerts for downtime, high error rate, high latency, failed deploy, failed backups, queue backlog, cost spike, and security events. |
| SLOs | Define availability, latency, error rate, job completion, backup success, and recovery objectives. |
| Runbooks | Document incident response, escalation, rollback, data restore, secret rotation, queue replay, and cloud provider outage handling. |
| Deliverables | Dashboards, alert rules, SLOs, log queries, incident runbooks, on-call/escalation policy. |
| Verification | Simulated failures create useful alerts with enough context for the right owner to respond. |
| Exit gate | Production cannot launch as a black box. Logs, metrics, alerts, and ownership must exist first. |

### Phase 15: Performance, Scale, and Reliability

| Area | Required actions |
|---|---|
| Load | Test expected, peak, and stress traffic for frontend, API, database, storage, queues, workers, and AI calls. |
| Scaling | Configure autoscaling, concurrency, connection pools, rate limits, quotas, worker scaling, and database capacity. |
| Caching | Add CDN caching, API caching, database caching, object cache headers, invalidation rules, and stale data strategy. |
| Resilience | Test degraded database, slow third-party API, AI timeout, queue backlog, storage failure, partial region outage, and bad deploy. |
| Recovery | Define RTO, RPO, backup restore, failover, manual recovery, and disaster recovery exercise schedule. |
| Deliverables | Load test report, scaling policy, cache policy, reliability test report, DR plan, recovery test evidence. |
| Verification | The system meets agreed latency, throughput, availability, RTO, and RPO targets under realistic conditions. |
| Exit gate | Critical workloads must survive expected peak load and common dependency failures without data loss. |

### Phase 16: AI/ML and RAG Readiness, If Applicable

| Area | Required actions |
|---|---|
| Use case | Define whether AI is chat, summarization, extraction, classification, recommendations, document search, or automation. |
| Model/provider | Choose Bedrock, Azure OpenAI/Foundry, Vertex AI/Gemini, OpenAI API, or another provider based on quality, latency, privacy, region, and cost. |
| RAG | Design ingestion, parsing, chunking, embeddings, vector store, metadata filters, retrieval, reranking, citations, and refresh/delete behavior. |
| Safety | Add prompt injection defenses, content filters, PII handling, jailbreak testing, output validation, rate limits, and human review for risky actions. |
| Evaluation | Build eval datasets for correctness, groundedness, refusal quality, latency, cost, and regression testing. |
| Operations | Track token usage, model latency, model errors, retrieval quality, cost per user/action, provider quota, and fallback behavior. |
| Deliverables | AI architecture, prompt catalog, eval suite, safety checklist, vector schema, AI monitoring dashboard, cost guardrails. |
| Verification | AI output quality, grounding, safety, privacy, latency, and cost are measured instead of assumed. |
| Exit gate | No AI feature launches without evaluation, guardrails, logging policy, rate limits, and user-facing failure behavior. |

### Phase 17: Cost Management and Optimization

| Area | Required actions |
|---|---|
| Budget | Define monthly budget, launch budget, scale budget, AI budget, data transfer budget, and alert thresholds. |
| Tagging | Enforce tags/labels for owner, environment, service, cost center, project, data class, and lifecycle. |
| Visibility | Enable billing exports, cost dashboards, anomaly detection, budget alerts, and unit cost tracking. |
| Optimization | Review idle resources, oversized databases, NAT/data transfer cost, log volume, storage lifecycle, CDN hit rate, AI token usage, and reserved/committed discounts. |
| Governance | Define who approves new paid services, large scale changes, GPU/AI usage, and production capacity increases. |
| Deliverables | Cost model, cost dashboard, budget alerts, tagging policy, optimization backlog, approval process. |
| Verification | Cost owner can explain expected spend by environment, service, feature, user, and growth scenario. |
| Exit gate | Production launch requires budget alerts and ownership for every meaningful cost driver. |

### Phase 18: QA, Release Candidate, and Go-Live

| Area | Required actions |
|---|---|
| QA | Complete unit, integration, E2E, contract, accessibility, performance, security, smoke, and rollback tests. |
| Product | Confirm acceptance criteria, launch scope, known limitations, support notes, and success metrics. |
| Security/compliance | Confirm final scan results, risk acceptances, audit logging, data handling, and access controls. |
| DevOps | Confirm production config, DNS/TLS, deployment pipeline, rollback, backups, dashboards, alerts, and runbooks. |
| Support | Prepare help docs, known issue list, escalation path, customer messaging, and debug process. |
| Release | Run go/no-go meeting, freeze risky changes, deploy release candidate, run smoke tests, monitor, and communicate launch status. |
| Deliverables | Test report, release checklist, launch plan, rollback plan, runbooks, go/no-go decision, release notes. |
| Verification | Release candidate is deployed to staging, tested like production, and approved by all required owners. |
| Exit gate | Go-live proceeds only when product, engineering, QA, security, DevOps, support, and business owners approve. |

### Phase 19: Post-Launch Stabilization

| Area | Required actions |
|---|---|
| Monitoring | Watch availability, latency, errors, queue backlog, database health, cost, AI usage, Core Web Vitals, and support tickets. |
| Triage | Prioritize defects by user impact, data loss risk, security risk, business impact, and workaround availability. |
| Product | Compare actual behavior to success metrics and identify friction, drop-offs, and missing workflows. |
| Engineering | Fix launch blockers, reliability issues, performance regressions, telemetry gaps, and scaling surprises. |
| Support | Update known issues, help docs, troubleshooting paths, and escalation rules. |
| Deliverables | Launch report, defect triage board, metric review, cost review, support summary, stabilization backlog. |
| Verification | Blocking defects are resolved or mitigated and launch metrics are understood. |
| Exit gate | Hypercare ends only when operational metrics are stable and support volume is acceptable. |

### Phase 20: Long-Term Maintenance and Evolution

| Area | Required actions |
|---|---|
| Ownership | Keep owners current for services, dashboards, budgets, security, data, IaC, CI/CD, and support runbooks. |
| Upgrades | Schedule framework, runtime, database, Terraform/provider, container base image, cloud SDK, dependency, and AI model upgrades. |
| Security | Continue vulnerability scans, access reviews, secret rotation, dependency updates, threat-model refreshes, and incident postmortems. |
| Reliability | Review SLOs, incident history, DR tests, backup restores, alert quality, scaling policies, and capacity trends. |
| Cost | Review monthly spend, anomalies, unit economics, idle resources, log volume, storage lifecycle, and AI token usage. |
| Product | Retire stale features, clean old flags, evolve roadmap, review customer feedback, and measure ongoing value. |
| Deliverables | Maintenance calendar, quarterly health review, upgrade plan, cost review, security review, roadmap refresh. |
| Verification | The system remains secure, observable, affordable, recoverable, and deployable after launch. |
| Exit gate | Cloud ownership continues as an active process, not a one-time project. |

### RACI by Phase

| Phase | Accountable | Responsible contributors | Consulted | Informed |
|---|---|---|---|---|
| 0. Initiation | Sponsor | Product, engineering lead | Security, finance, operations | Stakeholders |
| 1. Provider strategy | Engineering lead | Cloud architect, DevOps | Security, finance, compliance | Product, leadership |
| 2. Discovery | Product owner | UX, engineering, QA | Support, analytics, security | Stakeholders |
| 3. Architecture | Cloud architect | Frontend, backend, DevOps | Security, SRE, data owner | Product, leadership |
| 4. Governance | Platform/cloud owner | DevOps, security | Finance, compliance | Engineering |
| 5. Networking | Cloud/network owner | DevOps, security | Backend, compliance | Engineering |
| 6. IAM/secrets | Security owner | DevOps, backend, frontend | Compliance | Engineering, leadership |
| 7. IaC | DevOps/platform owner | Cloud architect, security | Engineering | Product |
| 8. Hosting | Engineering lead | Frontend, backend, DevOps | SRE, security | Product |
| 9. Data/storage | Data/backend owner | Backend, DevOps | Security, compliance | Product |
| 10. Messaging | Backend owner | Backend, DevOps, SRE | QA, product | Engineering |
| 11. CI/CD | DevOps owner | Frontend, backend, QA | Security | Product |
| 12. Security | Security owner | Engineering, DevOps | Compliance, legal | Leadership |
| 13. Compliance | Compliance/legal owner | Security, data owner | Product, engineering | Leadership |
| 14. Observability | SRE/DevOps owner | Backend, frontend, support | Security, product | Engineering |
| 15. Performance | Engineering lead | DevOps, backend, frontend, QA | Product, SRE | Leadership |
| 16. AI/RAG | AI feature owner | Backend, data, frontend, security | Legal, compliance, product | Leadership |
| 17. Cost | Finance/cloud owner | DevOps, engineering | Product, leadership | Stakeholders |
| 18. Go-live | Release manager | DevOps, QA, engineering | Security, support, product | All stakeholders |
| 19. Stabilization | Product and engineering leads | Support, QA, DevOps | Security, analytics | Leadership |
| 20. Maintenance | Engineering manager | DevOps, security, QA, product | Finance, support | Leadership |

### Non-Negotiable Cloud Release Gates

| Gate | Required evidence |
|---|---|
| Business gate | Business case, success metrics, budget, timeline, and accountable sponsor are approved. |
| Architecture gate | Architecture diagram, service decisions, region strategy, service boundaries, and Well-Architected review are complete. |
| Governance gate | Accounts/subscriptions/projects, owners, tags, policies, access model, and audit logging are in place. |
| Security gate | Threat model, IAM review, secret scan, dependency/container/IaC scans, encryption, WAF/rate limits where needed, and no high/critical unresolved findings. |
| Data gate | Data classification, backup, restore test, migrations, retention, storage permissions, and access rules are approved. |
| Compliance gate | Privacy map, residency, consent, audit logging, vendor review, and retention/deletion requirements are approved. |
| Quality gate | Lint, typecheck, unit, integration, E2E, contract, smoke, accessibility, security, and production build checks pass. |
| Performance gate | Load tests, autoscaling, cache policy, latency targets, AI latency if applicable, and recovery targets pass. |
| Observability gate | Logs, metrics, traces, dashboards, alerts, SLOs, and runbooks are verified with simulated failures. |
| Cost gate | Budgets, alerts, tags, cost dashboard, AI usage controls, and owner approval are complete. |
| Deployment gate | CI/CD, staging parity, artifact versioning, smoke tests, rollback drill, and launch checklist are complete. |
| Support gate | Known issues, support runbook, escalation path, debug metadata, and customer communication are ready. |

### Phase Artifact Index

| Artifact | Created in phase | Owner | Purpose |
|---|---|---|---|
| Project brief | 0 | Sponsor/product | Explain goal, value, constraints, and success metrics. |
| Provider ADR | 1 | Engineering/cloud architect | Justify AWS, Azure, GCP, or hybrid choice. |
| Service model ADR | 1 | Engineering/cloud architect | Explain serverless/container/managed/Kubernetes/VM choice. |
| Workload inventory | 2 | Engineering/product | List all frontend, backend, data, AI, async, and integration workloads. |
| Data classification | 2 | Security/compliance | Define data sensitivity and protection requirements. |
| Architecture diagram | 3 | Cloud architect | Show complete system structure and traffic/data flow. |
| Landing zone plan | 4 | Platform/cloud owner | Define account/subscription/project layout and governance. |
| Network diagram | 5 | Network/cloud owner | Document ingress, egress, private access, DNS, and TLS. |
| IAM matrix | 6 | Security owner | Prove least privilege by user and service identity. |
| Secret inventory | 6 | Security/DevOps | Track secret storage, access, rotation, and revocation. |
| IaC modules | 7 | DevOps/platform | Reproduce infrastructure safely. |
| Hosting runbook | 8 | DevOps/engineering | Document app deployment and runtime behavior. |
| Data model and migrations | 9 | Backend/data owner | Protect schema changes and data consistency. |
| Backup/restore report | 9 | DevOps/data owner | Prove recoverability. |
| Queue/DLQ policy | 10 | Backend/SRE | Make async work reliable and recoverable. |
| CI/CD pipeline | 11 | DevOps | Automate build, test, deploy, and rollback. |
| Threat model | 12 | Security | Identify and mitigate cloud/application risks. |
| Privacy/compliance map | 13 | Compliance/security | Track sensitive data obligations. |
| Observability dashboard | 14 | SRE/DevOps | Diagnose production behavior. |
| Load test report | 15 | QA/engineering | Validate scale and performance assumptions. |
| AI eval suite | 16 | AI/backend owner | Measure AI quality, safety, latency, and cost. |
| Cost dashboard | 17 | Finance/cloud owner | Monitor and control spend. |
| Release checklist | 18 | Release manager | Execute go-live safely. |
| Launch report | 19 | Product/engineering | Capture production results and follow-up work. |
| Maintenance calendar | 20 | Engineering manager | Keep cloud platform healthy after launch. |

### Final Validation From Every Perspective

| Perspective | Final production question |
|---|---|
| Business | Does the cloud system meet the agreed business goal within budget and timeline? |
| Product | Can every target user complete every critical workflow with clear success and failure handling? |
| Frontend | Is the UI deployed securely, cached correctly, accessible, responsive, and observable? |
| Backend | Are APIs reliable, versioned, secure, tested, and scaled for expected load? |
| Data | Are schemas, migrations, backups, restores, retention, and access rules proven? |
| AI/ML | Are prompts, retrieval, evals, guardrails, monitoring, latency, and token costs controlled? |
| Cloud architecture | Are service choices, regions, boundaries, resilience, and failure modes documented? |
| Networking | Are DNS, TLS, ingress, egress, private access, and firewall rules correct? |
| IAM/security | Is least privilege enforced for users, services, CI/CD, secrets, storage, databases, and AI services? |
| Privacy/compliance | Is sensitive data handled, logged, stored, retained, deleted, and audited correctly? |
| QA | Would automated checks fail on a broken critical flow, contract, deploy, rollback, or security issue? |
| DevOps | Can the system be built, deployed, promoted, rolled back, and recreated from documented automation? |
| SRE | Are alerts actionable, dashboards useful, SLOs defined, and runbooks tested? |
| Cost | Are budgets, alerts, tags, unit costs, data transfer, logs, and AI spend visible? |
| Support | Can support diagnose user issues, identify release version, escalate correctly, and explain known limitations? |
| Legal/procurement | Are vendors, licenses, data terms, AI terms, and asset rights reviewed? |
| Governance | Are owners, risks, decisions, approvals, and maintenance obligations explicit? |

### Roadmap Summary

| Stage | Phases | Output |
|---|---|---|
| Strategy | 0-3 | Business case, provider decision, workload discovery, architecture |
| Cloud foundation | 4-7 | Governance, networking, IAM, secrets, Infrastructure as Code |
| Application foundation | 8-11 | Hosting, data, queues, workers, CI/CD, environment promotion |
| Hardening | 12-15 | Security, privacy, observability, performance, reliability |
| AI readiness | 16 | AI/RAG safety, quality, monitoring, and cost control if applicable |
| Launch readiness | 17-18 | Cost controls, QA, release candidate, go-live approval |
| Operations | 19-20 | Stabilization, long-term maintenance, upgrades, cost/security reviews |

## 12. Final Recommendation

Pick one cloud first:

- Choose AWS for the largest cloud ecosystem and broad job market.
- Choose Azure for Microsoft, .NET, enterprise, and corporate environments.
- Choose GCP for containers, data, AI/ML, Firebase, and Google ecosystem tools.

After learning one cloud well, the others become easier because most concepts are the same with different service names.

The practical target is:

```text
Build, deploy, secure, monitor, scale, and improve full-stack applications using managed cloud services and AI APIs.
```

## Official References

- AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- Azure Well-Architected Framework: https://learn.microsoft.com/en-us/azure/well-architected/what-is-well-architected-framework
- Google Cloud Well-Architected Framework: https://docs.cloud.google.com/architecture/framework
- Amazon Bedrock: https://docs.aws.amazon.com/bedrock/
- Amazon SageMaker AI: https://docs.aws.amazon.com/sagemaker/
- Microsoft Foundry: https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-ai-foundry
- Google Vertex AI: https://cloud.google.com/vertex-ai/docs
