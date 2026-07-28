# AI Industry Roadmap — All Perspectives, with Original Industry-Level Projects

Updated: July 28, 2026

Companion to:
- [AI-Industry-Curriculum.md](AI-Industry-Curriculum.md)
- [AI-Industry-Detailed-Outline.md](AI-Industry-Detailed-Outline.md)
- [AI-Industry-Detailed-Lessons.md](AI-Industry-Detailed-Lessons.md)
- [AI-Industry-Complete-Lesson-Coverage-Map.md](AI-Industry-Complete-Lesson-Coverage-Map.md)

This file does three things the others do not:
1. Turns the 40-lesson curriculum into a **time-phased journey** (what to do, in what order).
2. Attaches the **best current course** to each phase (researched June 2026).
3. Gives an **original, portfolio-grade project** for each phase and each role — not the generic "PDF chatbot" everyone builds.

---

## 0. How to use this roadmap

### The one rule: Learn → Build → Operate
For every phase you (1) learn the concepts from a course, (2) build an original project, (3) operate it — meaning you add tests, evaluation, security, monitoring, deployment, and a cost report. A project without step 3 is a tutorial, not a portfolio piece.

### Think of it like a real job, not a course
A junior engineer is handed a messy business problem and has to ship something that works, is safe, and is measurable. Every project below is written as a **business scenario**, the way a real ticket would arrive. You play the engineer.

### Two portfolio strategies — use both
- **One evolving flagship.** One system that grows across phases (the curriculum already does this with a customer-operations platform). It proves depth.
- **Diverse satellites.** Smaller standalone projects in *different industries* (legal, health, insurance, logistics, finance, e-commerce). They prove range and stop your portfolio looking like one demo.

The projects below are deliberately spread across industries so your portfolio shows range.

### Parallel .NET Applied AI proof lane

Python remains the primary teaching and experimentation language. The .NET lane is a **parallel proof lane**, not a replacement curriculum and not a requirement to rebuild every project twice. Its purpose is to prove that the learner can carry the same AI contracts, safety controls, evaluation discipline, and observability into an enterprise ASP.NET Core environment.

Use one evolving C# service, `Atlas.DotNet`, across the phases below:

| Curriculum touchpoint | Minimum .NET evidence |
|---|---|
| Lessons 09 and 11 / Phase 1 | ASP.NET Core endpoint using a provider-neutral chat abstraction such as `Microsoft.Extensions.AI.IChatClient`; streamed responses; typed business DTOs; schema validation; cancellation; model/provider metadata; token and cost capture |
| Lesson 14 / Phase 2 | Permission-aware retrieval adapter, hybrid/vector search integration, citations, abstention, and retrieval-versus-generation evaluation on the same cases as the Python implementation |
| Lessons 17-18 / Phase 4 | Bounded workflow, governed session/durable memory, tool authorization outside the model, one MCP client or server, exact-action approval, idempotency, and an audit record |
| Lessons 30-31 / Phase 8 | Managed identity or equivalent workload identity, resilience and provider failover policy, OpenTelemetry traces/metrics/logs, deployment, dashboards, SLOs, and rollback evidence |
| Lesson 40 / capstone | One end-to-end business path that can run through the .NET service with contract and evaluation parity; it does not need feature-for-feature parity with the Python platform |

`Microsoft.Extensions.AI` is the preferred provider-neutral abstraction boundary for basic .NET model access when the selected provider supports it. Semantic Kernel can be used where it earns its complexity. If a selected Microsoft Agent Framework capability or any dependency is in preview, keep that capability an **optional, version-pinned spike**, record its support status and migration risk in an ADR, and make the durable evidence the architecture, contracts, tests, and controls rather than allegiance to one framework.

### The "Ship Standard" — what makes a project industry-level
This is your curriculum's own project checklist. **Every** project on this roadmap must ship with all of it. Don't repeat it per project — just hold every project to it:

```
☐ Business problem + target user        ☐ Automated tests: unit/integration/failure/security/eval
☐ Functional + non-functional reqs      ☐ Security threat model
☐ Architecture diagram                  ☐ Docker + Docker Compose
☐ Data contracts + API contracts        ☐ CI pipeline (GitHub Actions)
☐ Baseline (the dumb version first)      ☐ Deployment + rollback instructions
☐ Evaluation dataset + thresholds        ☐ Logs, metrics, traces (observability)
☐ Cost + latency measurements            ☐ Failure-recovery plan
☐ README explaining the tradeoffs you made and why
```

If you can't show the eval dataset, the threat model, and the cost number, the project is not done.

### Build in public
Push every project to GitHub with a real README. Write a short post per project ("what broke and how I fixed it"). This *is* your interview material.

---

## 1. The roadmap at a glance

| Phase | Focus (curriculum lessons) | Learn from | Original flagship project | What it proves |
|---|---|---|---|---|
| **0** | Engineering foundations (1–6) | Your Lessons 1–6 + FastAPI/backend resources | **CargoEvents** — multi-tenant logistics events backend | You can build a real backend before adding AI |
| **1** | Applied AI + LLM apps (7–11) | Ed Donner (Udemy) / Grigorev Buildcamp; Huyen book | **ClauseScan** — contract-review assistant | You can ship an LLM feature with guardrails |
| **2** | Embeddings + RAG (12–14) | LLM Zoomcamp (free); Buildcamp | **MedPolicy Navigator** — clinical-guidelines RAG | You can build grounded, cited, access-controlled retrieval |
| **3** | Evaluation + feedback (15, 31) | Hamel & Shreya "AI Evals" (Maven) | **EvalForge** — eval platform for your own apps | You can prove quality, not just claim it |
| **4** | Tools, agents, MCP (16–18) | HF Agents + MCP courses; DeepLearning.AI Agentic AI | **OpsPilot** — cloud-cost remediation agent | You can build a *safe* acting agent (human approval, audit) |
| **5** | Model adaptation / post-training (19–25) | Karpathy Zero-to-Hero; HF LLM Course; Unsloth course | **DomainTune** — SFT→LoRA→QLoRA→DPO pipeline | You can adapt and serve an open model |
| **6** | Multimodal + voice (26–27) | HF Audio + CV courses; LiveKit voice course | **ClaimVision** + **VoiceTriage** | You can handle documents, images, and live audio |
| **7** | Safety, security, governance (28–29) | AI Red Teaming (Udemy); OWASP GenAI Top-10 | **GuardRail Gateway** — AI security gateway + governance pack | You can defend a system and document risk |
| **8** | Production, cloud, MLOps, serving (30–36) | MLOps Zoomcamp; Made With ML; vLLM course | **ModelMesh** — gateway + vLLM serving + LLMOps on K8s | You can run AI in production at scale |
| **9** | Classical ML + deep learning (37–39) | Andrew Ng ML + DL specializations; ML Zoomcamp; fast.ai | **ChurnGuard** + **ListingMatch** | You can choose ML over LLMs when it's the right tool |
| **★** | Capstone (40) | Everything | **Atlas** — defensible enterprise platform | You can integrate and defend a full system |

The .NET lane runs across Phases 1, 2, 4, 8, and the capstone. Phase 8 also offers `IncidentPilot`, an optional AIOps satellite for learners targeting SRE, MLOps, platform, or operations-heavy roles.

**Employable checkpoint:** after Phases 0–4 you can apply for **Junior Applied AI / Generative AI Engineer** roles. Phases 5–9 + a role branch take you to mid/senior and specialist tracks.

---

## 2. Phase-by-phase

> Format for each phase: **Goal → Learn → Build (the original project) → The hard parts that make it real → Proof → Time.**

### Phase 0 — Engineering foundations (Lessons 1–6)
**Goal:** Be a real backend engineer before you touch a model. This is the cluster most AI courses skip — your edge is not skipping it.

**Learn:** Your own Lessons 1–6 (they're stronger here than most paid courses). Supplement backend depth with a production-FastAPI resource and the PostgreSQL docs.

**Build — `CargoEvents`:**
> *Scenario:* A freight company gets shipment status updates from 5 carriers via webhooks. They need one clean, multi-tenant API that ingests, validates, stores, and exposes those events — and never lets Carrier A see Carrier B's data.

- FastAPI service, Pydantic validation, PostgreSQL + SQLAlchemy/Alembic, Redis cache.
- Auth + role-based access, idempotent webhook ingestion, background workers, streaming endpoint, OpenAPI docs.
- Multi-tenant row isolation, full pytest suite, Docker Compose, GitHub Actions CI.

**Hard parts that make it real:** idempotency on retried webhooks; cross-tenant access tests that must fail correctly; migrations that run on a fresh DB.

**Proof:** fresh-clone → `docker compose up` → health checks pass; CI green; cross-tenant test suite passes. **Time:** 3–5 weeks.

---

### Phase 1 — Applied AI + LLM applications (Lessons 7–11)
**Goal:** Ship your first LLM feature with structured output, human approval, cost tracking, and traceability.

**Learn:** Ed Donner's *AI Engineer Core Track* (Udemy) or Grigorev's *AI Engineering Buildcamp* (Maven). Read Chip Huyen's *AI Engineering* alongside.

**Build — `ClauseScan` (legal):**
> *Scenario:* A small legal team spends hours reading vendor contracts. They want a tool that reads a contract, labels each clause (indemnity, termination, liability cap…), extracts key terms (parties, dates, amounts), flags risky clauses, and drafts a plain-English summary — but a lawyer must approve before anything is final.

- Multi-provider model gateway (so you're not locked to one vendor), streaming UI/API.
- Schema-constrained extraction (invalid JSON can never reach business logic), classification, risk flags, draft + human-approval gate.
- Prompt registry with versions, regression test suite, token/cost tracking per request.

**Hard parts:** untrusted contract text must be separated from your instructions (injection awareness); define abstention ("I'm not sure" beats a confident wrong answer); measure classification quality on a labeled set.

**Proof:** every output traces to a prompt + model version; no auto-action without approval; a metrics page with cost-per-document. **Time:** 4–6 weeks.

**Parallel .NET proof:** implement one ClauseScan API path in ASP.NET Core behind `IChatClient`: streaming with cancellation, typed output validation before business logic, provider/model metadata, and a provider-neutral error contract. On Azure, prefer Entra ID/managed identity where supported rather than embedding provider keys. Reuse the Python lane's golden cases so the result is comparable, not merely another demo.

---

### Phase 2 — Embeddings + production RAG (Lessons 12–14)
**Goal:** Build retrieval that is grounded, cited, access-controlled, and *evaluated* — not vibes-based.

**Learn:** **LLM Zoomcamp** (free, project-based) is the ideal fit here. Continue Buildcamp if enrolled.

**Build — `MedPolicy Navigator` (healthcare):**
> *Scenario:* Nurses and admin staff can't quickly find answers across clinical guidelines, drug formularies, and internal procedures. Wrong answers are dangerous, and some documents are restricted to clinicians.

- Multi-format ingestion (PDF/HTML/tables), chunking comparison, hybrid retrieval (BM25 + dense) + cross-encoder reranking.
- Citations on every factual sentence; **abstention** when evidence is missing; role-based access so admin can't retrieve clinician-only content.
- Incremental indexing + delete propagation; retrieval observability.
- **Evaluate retrieval and generation separately:** recall@k, MRR, nDCG, context relevance, groundedness, citation accuracy.
- After the classic RAG baseline passes, add one bounded **agentic retrieval** path for a genuinely multi-part question: plan subqueries, retrieve in parallel or iteratively, rerank, verify evidence coverage, and stop at explicit query/step/time/token limits. Compare it with classic RAG on quality, latency, and cost; do not assume the agentic path wins.

**Hard parts:** failure attribution (was it ingestion, retrieval, rerank, or generation that failed?); unauthorized documents must *never* enter the context window.

**Proof:** an eval report with the metrics above; a test proving restricted docs never leak; a classic-versus-agentic retrieval decision record. The .NET lane adds the same authorization filters, citations, and core evaluation cases through an ASP.NET Core retrieval endpoint. **Time:** 5–7 weeks.

---

### Phase 3 — Evaluation + feedback engineering (Lessons 15, 31)
**Goal:** Become the person who can say "this change made it 8% better" with evidence. This is the single most underrated, most hireable skill.

**Learn:** **Hamel Husain & Shreya Shankar — "AI Evals for Engineers & PMs"** (Maven). Best-in-class. Their free *Mastering LLMs* archive too.

**Build — `EvalForge` (tooling):**
> *Scenario:* Your team keeps changing prompts, models, and retrieval settings and arguing about whether things improved. Build the platform that ends the arguing.

- Versioned golden datasets (with difficult-case mining and contamination checks).
- Deterministic checks (schema, exact-match, citation verification) **and** calibrated LLM-as-judge (pointwise + pairwise, with bias controls).
- Human-review queue with rubrics and inter-annotator agreement.
- CI quality gates (a bad prompt fails the build) + a regression dashboard with slice-level reporting and cost/latency.

**Hard parts:** judge calibration against human labels; making evals run automatically in CI so quality can't silently regress.

**Proof:** a PR that gets *blocked* by a failing eval gate; a dashboard comparing two model versions on the same dataset. **Time:** 4–6 weeks. *(Wire this back into ClauseScan and MedPolicy.)*

The same golden cases and release thresholds apply to the .NET proof path. Language-specific unit tests may differ, but schema validity, safety, retrieval, latency, and cost evidence must remain comparable.

---

### Phase 4 — Tools, agents, and MCP (Lessons 16–18) — **Junior-ready after this**
**Goal:** Build an agent that *takes actions* safely: permissions, human approval, audit, step/spend limits.

**Learn:** **Hugging Face Agents Course + MCP Course** (free, certs); DeepLearning.AI **Agentic AI (Andrew Ng)** and **AI Agents in LangGraph**; Anthropic Academy for MCP.

**Build — `OpsPilot` (FinOps / DevOps):**
> *Scenario:* A company wastes cloud spend on idle resources. They want an agent that scans billing + resource APIs, finds waste, and proposes fixes — but it must **never** delete or resize anything without a human clicking approve.

- Tools: billing read, resource inventory, a *write* tool (resize/stop) gated behind approval.
- Explicit workflow as a state machine (not a free-roaming agent): plan → propose → await approval → act → verify → compensate on failure.
- One tool exposed via a **secured MCP server** with identity propagation; full audit trail; step, time, and spend limits.
- Governed memory: separate request context, session state, durable workflow state, user preferences, and retrieval-backed memory; define read/write policy, provenance, consent, expiry, correction, and deletion. Memory is not an unbounded transcript.

**Hard parts:** the write action is the whole point — unauthorized or duplicate actions must be impossible; compensation/rollback when a step half-fails; task-completion + invalid-action metrics.

**Proof:** a test suite where the agent *tries* an unapproved write and is blocked; an audit log for one full run; memory read/write/expiry/deletion tests. The .NET lane implements one bounded workflow plus one MCP boundary in C#, with authorization enforced by ordinary application policy rather than model instructions. **Time:** 5–7 weeks.

> **🎯 Checkpoint:** Phases 0–4 + ClauseScan/MedPolicy/OpsPilot in your portfolio = ready to apply for **Junior Applied AI / GenAI Engineer**.

---

### Phase 5 — Model adaptation & post-training (Lessons 19–25)
**Goal:** Stop treating models as black boxes. Train, adapt, and serve your own.

**Learn:** **Karpathy "Neural Networks: Zero to Hero"** (build a GPT + tokenizer from scratch — free) for true understanding; **Hugging Face LLM Course** fine-tuning chapters; "LLM Fine-Tuning: HuggingFace & Unsloth" (Udemy) for LoRA/QLoRA/DPO/GRPO hands-on.

**Build — `DomainTune` (pick one vertical, e.g., financial-filing tagging or radiology-report structuring):**
> *Scenario:* A general model won't reliably follow your domain's format, terminology, and policy. Adapt an open model so it does — and prove the adaptation was worth it.

- Build and validate an instruction dataset (chat templates, label masks, leakage checks).
- Run the ladder: **SFT → LoRA → QLoRA → DPO**, tracked in MLflow, adapters in a registry.
- Comparison report: base vs. prompted vs. RAG vs. LoRA vs. DPO on the same eval set, plus GPU-memory, training-time, latency, and cost-per-task.
- Safety/behavior regression check; serving endpoint.

**Hard parts:** knowing *when not to fine-tune* (the report should sometimes conclude "RAG was enough"); catastrophic forgetting and safety regression.

**Proof:** the comparison table with numbers; reproducible training config; versioned adapter artifacts. **Time:** 7–10 weeks.

---

### Phase 6 — Multimodal, document & voice AI (Lessons 26–27)
**Goal:** Handle the inputs real businesses actually have: scanned forms, photos, and phone calls.

**Learn:** **Hugging Face Audio Course + Computer Vision Course** (free); **LiveKit "Building AI Voice Agents for Production"** (free).

**Build A — `ClaimVision` (insurance):**
> *Scenario:* A claims team manually reviews claim forms, damage photos, and voicemail. Automate the intake with evidence and human review for low-confidence cases.
- OCR + layout/key-value extraction on forms; vision model on damage photos; speech-to-text on voicemails; evidence-linked summary; confidence-based routing to humans.

**Build B — `VoiceTriage` (real-time):**
> *Scenario:* An inbound line triages callers before a human picks up.
- Streaming STT→LLM→TTS (LiveKit/Deepgram), barge-in/interruption handling, tool calls mid-call, human escalation, recording-consent disclosure, end-to-end latency budget.

**Hard parts:** evaluating extraction and visual understanding *separately*; voice latency and turn-taking; consent/privacy on recordings and images.

**Proof:** evidence links to source page/region; a measured end-to-end voice latency number. **Time:** 6–8 weeks.

---

### Phase 7 — Safety, security, privacy, governance (Lessons 28–29)
**Goal:** Be the engineer who can attack the system *and* document its risk. Required for trust in any enterprise.

**Learn:** **"AI Red Teaming & LLM Hacking"** (Udemy, uses Microsoft's AI Red Team labs); **OWASP GenAI Top-10 (2025)** + Promptfoo red-team docs as your frameworks.

**Build — `GuardRail Gateway` (cross-cutting):**
> *Scenario:* Your OpsPilot/Atlas agent handles confidential data and can trigger actions. Wrap it in a security layer and prove it holds.

- Threat model + adversarial test set: direct/indirect prompt injection, jailbreaks, system-prompt leakage, data exfiltration, tool abuse.
- PII detection + redaction, content/policy checks, a tool-permission service (authorization lives *outside* the model), rate/spend controls, audit logs.
- Security regression suite that runs in CI.
- **Governance pack:** model card, system card, dataset card, risk register, NIST AI RMF / OWASP mapping, incident + human-oversight plan.

**Hard parts:** indirect injection through retrieved/tool content; making authorization impossible for the model to talk its way around.

**Proof:** a red-team report with attacks that *fail*; the governance documents. **Time:** 5–7 weeks.

---

### Phase 8 — Production, cloud, MLOps, serving & inference (Lessons 30–36)
**Goal:** Run all of the above in production: reliable, observable, cost-controlled, on real infrastructure.

**Learn:** **MLOps Zoomcamp** (free) + **Made With ML** (Goku Mohandas) for the MLOps spine; **DeepLearning.AI × Red Hat "Fast & Efficient LLM Inference with vLLM"** for serving/optimization.

**Build — `ModelMesh` (platform):**
> *Scenario:* Many teams each wire up their own model calls, with no shared tracing, cost control, or safety. Build the governed platform they share.

- Multi-provider model gateway: routing, provider/model fallback, semantic + prefix caching, per-tenant cost attribution, request/spend limits.
- Self-host your DomainTune adapters on **vLLM**: continuous batching, KV/prefix cache, quantization (INT8/INT4), LoRA serving.
- Deploy to one cloud + **Kubernetes** (Terraform IaC, secrets, autoscaling, GPU scheduling).
- Full observability (OpenTelemetry GenAI conventions + Prometheus + Grafana); LLMOps pipeline (MLflow, registries, canary release, automated rollback).
- Load test + capacity plan + a hosted-vs-self-hosted cost report.
- Required architecture ADR: compare a modular monolith, event-driven workers, and separately deployable microservices for the model gateway, ingestion/retrieval, evaluation, and agent execution. Decide from measured scaling, failure-isolation, security, data-ownership, deployment, and team-ownership needs, and include an evolutionary extraction plan. Do not choose microservices just because the system contains AI.

**Hard parts:** measuring quality *after every optimization* (quantization can quietly degrade output); canary + rollback that actually works; cost-per-successful-task, not just cost-per-token.

**Proof:** a load-test report (TTFT, tokens/sec, p95 latency, GPU util) + a cost comparison + a demonstrated rollback. **Time:** 8–12 weeks.

**Parallel .NET proof:** expose one ModelMesh business path through ASP.NET Core using the provider-neutral interface established in Phase 1. Use Entra ID/managed identity where the selected Azure services support it, preserve tenant authorization through retrieval and tools, and emit correlated model, retrieval, tool, cost, and approval telemetry. Because GenAI telemetry conventions and integrations continue to evolve, pin package/convention versions and keep a small internal telemetry contract that can be remapped.

**Optional satellite — `IncidentPilot` (AIOps / SRE):**
> *Scenario:* On-call engineers lose time correlating API failures, queue backlogs, deployment changes, model-provider errors, and retrieval degradation. Build an evidence-linked incident assistant that helps investigate; it does not become an unsupervised production administrator.

- Start with deterministic RED signals (rate, errors, duration) and USE signals (utilization, saturation, errors), alert rules, deployment events, and runbooks. Add anomaly detection and event correlation only after this baseline is measurable.
- Correlate logs, metrics, traces, queue state, provider status, model/retrieval evaluation regressions, and recent changes into a time-bounded incident timeline.
- Produce ranked root-cause **hypotheses** with links to supporting and contradicting telemetry; retrieve relevant runbook steps; draft an incident update and postmortem.
- Keep read-only investigation separate from action. Any restart, scale, rollback, feature-flag, or traffic-routing tool requires normal authorization, exact arguments, human approval, idempotency, verification, and compensation/rollback.
- Evaluate alert-noise reduction, evidence precision, hypothesis top-k recall on seeded incidents, time-to-triage, false-action rate, latency, and cost. Include an insufficient-evidence outcome.

**IncidentPilot proof:** three seeded failure drills (for example provider throttling, queue saturation, and retrieval-quality regression), a reconstructed timeline, an evidence-backed hypothesis report, a human-approved runbook simulation in a non-production environment, and a red-team test proving telemetry text cannot inject an unauthorized action. **Additional time:** 3–5 weeks; optional unless the target role is SRE/MLOps/platform.

---

### Phase 9 — Classical ML + deep learning (Lessons 37–39)
**Goal:** Know when a boosted tree beats an LLM. Many business problems are cheaper, faster, and more reliable without generative AI.

**Learn:** **Andrew Ng Machine Learning Specialization** + **Deep Learning Specialization**; **ML Zoomcamp** (free, project-based); **fast.ai** for hands-on DL.

**Build A — `ChurnGuard` (SaaS/telecom, classical ML):**
> *Scenario:* Predict which customers will cancel next month so retention can intervene.
- Feature pipeline, baselines → XGBoost/LightGBM, calibration, threshold selection by business cost, batch + online inference, drift monitoring, retraining trigger, canary release.

**Build B — `ListingMatch` (e-commerce, deep learning):**
> *Scenario:* Auto-classify product listings and find near-duplicates/semantic matches.
- Non-neural baseline → embeddings → fine-tuned transformer; evaluation slices; ONNX export + serving; latency/cost report.

**Hard parts:** leakage prevention and time-based splits; calibration; proving the simple model was or wasn't enough. **Time:** 7–10 weeks.

---

### ★ Capstone — Enterprise Applied AI platform (Lesson 40)
**Goal:** Integrate everything into one system you can defend in an interview.

**Build — `Atlas` (choose your vertical):**
> *Scenario:* One company, one real workflow, end to end. Pick a domain you didn't use yet (e.g., HR/recruiting, real estate, manufacturing) and build the platform that runs a valuable workflow for them.

Combine: tenant auth → ingestion → hybrid RAG with citations → structured extraction → tool-using workflow with MCP + human approval → a fine-tuned adapter served on vLLM → multi-provider routing → security + governance → cloud + K8s deployment → observability + cost dashboards → canary + rollback → **a business-outcome report** (time saved, cost, quality).

The .NET lane is complete when one valuable Atlas workflow runs end to end through `Atlas.DotNet` with the same external contract, authorization boundary, core golden cases, trace correlation, and approval policy as the primary implementation. Contract/evaluation parity matters; duplicating every internal component does not.

**Proof (the interview kit):** PRD, architecture decision records—including the modular-monolith/event-driven-worker/microservice decision and an extraction trigger—threat model, eval report, model/system/dataset cards, load + failure-injection reports, business-outcome report, a .NET contract/evaluation parity report when that lane is selected, and a 10-minute technical presentation. **Time:** 6–10 weeks.

---

## 3. All-perspectives — role branches

After the core (Phases 0–4) plus the phases each role needs, pick **one primary branch + one supporting branch**. Don't do all at once. Each branch has a *distinctive* capstone so your portfolio signals that role.

| Role perspective | Do these phases deeply | Distinctive capstone project |
|---|---|---|
| **Applied AI Engineer** | 0–4, 7, 8, + Atlas | `Atlas` with a real user-facing UI + measured business outcomes |
| **Generative AI Engineer** | 1–6, 7, 8 | A multi-model, **multimodal** GenAI product (text + image + voice in one) |
| **LLM Engineer** | 5, 8 (serving) + Karpathy from-scratch | Train a small GPT from scratch **and** ship `DomainTune` end-to-end with serving |
| **Post-Training Engineer** | 5 (deep) + data work (16) | Reward-model + **DPO/GRPO** pipeline with a data flywheel and safety evals |
| **MLOps / ML Platform Engineer** | 8 (deep), 3, 5 | `ModelMesh` on K8s + Terraform + continuous-training pipeline |
| **Machine Learning Engineer** | 9 (deep), 8 | `ChurnGuard` + `ListingMatch` fully productionized with drift + retraining |
| **AI Inference Engineer** | 8 (serving/inference) | vLLM/SGLang optimization study: quantization + batching + a full benchmark report |
| **AI Security Engineer** | 7 (deep), 4 | `GuardRail` + a red-team CTF writeup against your own agent |
| **AI Evaluation Engineer** | 3 (deep), 15 | `EvalForge` extended to agent + safety evals with human-review ops |
| **AI Data Engineer** | 16 + foundations | Auditable training-data pipeline: contracts, PII redaction, dedup, DVC, Airflow/Spark |
| **Search & Ranking Engineer** | 2 (deep) | Learning-to-rank search service with online A/B evaluation |
| **Recommender Systems Engineer** | 9 + 2 | Candidate-generation + ranking recsys with feedback-loop evaluation |
| **NLP Engineer** | 1, 2, 5 | Information-extraction/NER pipeline + fine-tuned classifier, multilingual eval |
| **Computer Vision Engineer** | 6 (deep), 9 | Detection/segmentation system with labeling, augmentation, edge/cloud serving |
| **Speech & Audio Engineer** | 6 (voice, deep) | Streaming ASR + diarization + `VoiceTriage` with real-time latency targets |
| **Multimodal AI Engineer** | 6 (deep) | `ClaimVision` extended: vision-language + audio-language + document retrieval |
| **Forward-Deployed / Solutions Architect** | 0–4, 8 | Deploy `Atlas` for a mock "customer" + architecture + adoption + ROI docs |
| **.NET Applied AI / Enterprise Integration Engineer** | 0–4, 8 + the parallel .NET lane | `Atlas.DotNet`: ASP.NET Core model gateway + RAG + controlled tools/MCP + Entra/workload identity + OpenTelemetry, with contract/eval parity |
| **AI SRE / AIOps Engineer** | 3, 4, 8 + the optional satellite | `IncidentPilot` with RED/USE baselines, evidence-linked investigation, failure drills, and approval-gated remediation |

---

## 4. Portfolio, proof, and interview prep (Lessons 52–57 territory)

- **GitHub:** one repo per project, each with the Ship Standard checklist visibly satisfied in the README.
- **Writeups:** for each project, a short post: the business problem, your architecture decision, what broke, the eval numbers, the cost. This is what you talk about in interviews.
- **The metrics habit:** never say "it works." Say "94% schema validity, groundedness 0.91, p95 latency 1.8s, $0.012/task." Recruiters and senior engineers filter for this.
- **Interview tracks:** coding/Python, SQL, applied-AI case design, and (for training roles) LLM/model-training questions. Practice them against the projects you actually built.
- **.NET lane evidence:** include the ASP.NET Core OpenAPI contract, provider adapter tests, streaming cancellation test, structured-output validation failures, managed/workload identity diagram, retrieval authorization test, MCP/tool approval test, trace screenshot, deployment/rollback runbook, and contract/eval parity report. One coherent service is stronger than many thin C# ports.
- **Architecture evidence:** include the decision forces, rejected alternatives, current boundary, measurable extraction triggers, event/API contracts, failure modes, and migration path in the required architecture ADR.
- **IncidentPilot evidence (optional):** include seeded incident fixtures, RED/USE dashboard, timeline reconstruction, evidence links, hypothesis-evaluation results, authorization/approval tests, and the incident/postmortem bundle. Label simulated remediation clearly; do not imply autonomous production control.

---

## 5. Timelines

| Track | Phases | Part-time (10–15 hrs/wk) | Outcome |
|---|---|---|---|
| **Fast track to employable** | 0–4 + 1 role branch | ~5–7 months | Junior Applied AI / GenAI Engineer |
| **Full core** | 0–9 | ~10–14 months | Mid-level, broad |
| **Specialist** | Core + deep branch + capstone | ~14–18 months | Senior / specialist (LLM, MLOps, inference, security) |

Full-time roughly halves these. Don't rush the Ship Standard to hit a date — one fully-operated project beats three half-built demos.

The .NET lane is best done in parallel for roughly 2–4 hours per week after Phase 1, reusing contracts and golden cases rather than replaying the whole curriculum. `IncidentPilot` adds 3–5 weeks only for learners who select that optional satellite.

---

## 6. Anti-patterns to avoid

- **Tutorial hell / "another PDF chatbot."** Every project here is a *business scenario* in a named industry for exactly this reason.
- **Skipping Phase 0.** The foundations are your edge; most candidates can't build a clean multi-tenant backend.
- **No evaluation.** If you can't measure it, you can't defend it. Phase 3 is non-negotiable.
- **Doing all branches at once.** One primary + one supporting. Depth signals competence; breadth-without-depth signals a bootcamp.
- **Fine-tuning by default.** Phase 5's best output is sometimes "RAG was enough." Knowing *when not to* is the senior signal.
- **Framework-first.** Learn the protocol/data flow/failure modes before the framework abstraction; frameworks churn.
- **Rebuilding everything in two languages.** The .NET lane proves transfer through one end-to-end path and parity evidence; it is not a second copy of every notebook and service.
- **Preview-as-foundation.** A preview agent framework may be explored behind an adapter, but pin it, record the risk, and keep core contracts and controls framework-neutral.
- **Inflating the shared core with every AI specialty.** Diffusion-based media generation, general reinforcement learning, and symbolic or neuro-symbolic AI remain optional role-specific extensions until a target job or project requires them.
- **Unsupervised self-healing.** IncidentPilot may recommend actions, but consequential writes remain externally authorized, approval-gated, bounded, verified, and auditable.

---

## 7. Project index (all original projects)

| # | Project | Industry | Core skill it proves | Phase |
|---|---|---|---|---|
| 1 | **CargoEvents** | Logistics | Production multi-tenant backend | 0 |
| 2 | **ClauseScan** | Legal | LLM feature with guardrails | 1 |
| 3 | **MedPolicy Navigator** | Healthcare | Grounded, cited, access-controlled RAG | 2 |
| 4 | **EvalForge** | Tooling | Evaluation engineering | 3 |
| 5 | **OpsPilot** | FinOps/DevOps | Safe acting agent + MCP | 4 |
| 6 | **DomainTune** | Finance/Health | SFT/LoRA/QLoRA/DPO + serving | 5 |
| 7 | **ClaimVision** | Insurance | Multimodal document/vision/speech | 6 |
| 8 | **VoiceTriage** | Telephony | Real-time voice agent | 6 |
| 9 | **GuardRail Gateway** | Security | Red-teaming + governance | 7 |
| 10 | **ModelMesh** | Platform | Cloud/K8s/MLOps/vLLM serving | 8 |
| 11 | **ChurnGuard** | SaaS/Telecom | Classical ML in production | 9 |
| 12 | **ListingMatch** | E-commerce | Deep learning + embeddings | 9 |
| 13 *(optional)* | **IncidentPilot** | SRE / Platform Operations | Evidence-linked AIOps investigation + approval-gated remediation | 8 |
| ★ | **Atlas** | Your choice | Full integration + business outcome | Capstone |

Build these and you have a portfolio that covers every perspective in the curriculum — and looks nothing like anyone else's.
