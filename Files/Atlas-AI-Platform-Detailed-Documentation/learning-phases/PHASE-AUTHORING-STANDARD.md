# Atlas Phase Document — Authoring Standard

This is the standard every learning-phase document must follow, for Phase 02 through Phase 25.

Hand this file to whoever writes a phase, together with a short per-phase brief. This file covers the rules that never change. The brief covers what is specific to that phase — its tickets, its source sections, and the conflicts already found in it. `HOW-TO-WRITE-phase-02-prompt-system.md` is the worked example of such a brief.

Reference implementations, already written to this standard:

```text
phase-00-engineering-foundation.md   48 sections
phase-01-llm-gateway.md              49 sections
```

Read one of them end to end before writing. Everything below is easier to follow after seeing it done.

---

## 1. What A Phase Document Is

A **lesson**, not a specification.

The reader must finish able to *build* the phase and able to *explain* it — why it exists, what it costs, how it fails, and what it would take to prove it works. If the document only tells them what to type, it has failed even if the code runs.

Three tests for any section you write:

```text
Does it say WHY before WHAT?
Could a reader defend this decision in an interview?
Is there anything here they could not have got from reading the code?
```

## 2. Inputs To Read Before Writing

| Source | Use |
|---|---|
| The previous phase document | Template, house style, and what your phase inherits |
| `00-Atlas-Documentation-Map.md` | Phase list, execution order, scope freeze |
| `01-Atlas-Technical-Master-Blueprint.md` | Architecture and the design section for your phase |
| `02-Atlas-Coverage-Matrix.md` | Which topics are yours vs. a later phase |
| `04-Atlas-Database-Schema-Specification.md` | Implementation-ready columns, constraints, indexes |
| `05-Atlas-Standards-Crosswalk.md` | OWASP / AISVS / NIST / OpenTelemetry names — reuse them, never coin your own |
| `06-Atlas-Implementation-Tickets.md` | Your tickets and their acceptance proofs |
| `10-Atlas-Operations-Runbooks.md` | The incidents your phase must make survivable |
| `08-Atlas-Frontend-UX-Specification.md` | The screens your API must feed |

## 3. Non-Negotiable Rules

**1. Trace every claim.** Open with a source-document table. If you design something the source set implies but never specifies, say so plainly. An invention that reads like a citation is the worst defect in this documentation set.

**2. Resolve conflicts in writing.** State it, quote both sides, recommend one, name the alternative, tell the reader to record a decision. Never silently pick.

**3. Every example must actually work.** Any identifier a configuration block references must be defined in that block. Trace every copied example through your own algorithm before enshrining it.

**4. Name the owning phase for everything deferred.** "Later" is not an answer. "Phase 07" is.

**5. Reuse existing names.** Search the source set before coining an attribute, error code, status, or column name.

**6. Do not fear repetition.** This is teaching. A concept explained in context, restated in a glossary, and shown as a worked example is three passes for a reader who does not have it yet — not duplication. Keep the definitions section *and* the glossary. Keep the implementation sequence *and* the checklist.

**7. No meta-commentary about the document.** No structure-mapping tables, no self-indexes of your own divergences. Argue each divergence where the decision is made.

**8. Length is not the target.** Completeness is. A short phase gets a short document.

## 4. The Conceptual Layer — The Requirement Most Likely To Be Missed

Every phase document must contain a section titled **"Concepts You Cannot Learn From The Code"**, placed immediately after the vocabulary section and before the business perspective. See Phase 00 §6 and Phase 01 §8.

### 4.1 The Rule

> If a concept falls inside this phase's scope but cannot be expressed as a file, a test, or a migration, it must be in this document — because there is nowhere else the learner will ever encounter it.

A learner can implement a phase perfectly and never learn why it is shaped that way. Code teaches *what*. Only the document can teach *why*, and only for the phase where that why first becomes visible.

### 4.2 How To Derive Your Phase's List

Do not guess. Run this procedure.

**Step 1 — List what the phase builds.** Every table, module, endpoint, and policy.

**Step 2 — For each one, ask:** *what must a reader know to make a good decision here that is not visible in the artifact itself?* A timeout value implies queueing theory. A cost column implies unit economics. A `region` field implies data-residency law.

**Step 3 — Sweep six categories.** Most phases have something in at least four:

| Category | The question |
|---|---|
| **Mechanism** | How does the underlying technology actually work, such that this design follows? |
| **Economics** | What does this cost, per what unit, and what is the real tradeoff? |
| **Failure and reliability** | How does this break at scale, and what is the theory behind the defenses? |
| **Measurement** | How would anyone prove this works or got better? What makes that hard here? |
| **Governance and law** | What words in this design come from contracts or regulation? |
| **Human and organizational** | What does this change about how a team works, reviews, or is on call? |

**Step 4 — Apply the interview test.** *Could someone build this correctly and still fail a reasonable interview question about it?* If yes, that question's answer belongs in your section.

**Step 5 — Cut anything that is not this phase's.** Attention mechanisms belong where token cost first appears, not in every phase after. State each concept once, in the phase where the reader first needs it, and reference it later.

### 4.3 Format

- One subsection per concept, ordered from mechanism outward to governance.
- Lead with the mechanism, then the consequence, then *the specific design decision in this document it explains*. That last link is what makes it a lesson instead of a lecture.
- Diagrams and small tables over long prose.
- Close with a "carry these forward" list of five or six lines.
- Add **inline pointers** from the sections whose decisions the theory explains — for example, the timeout section points back at queueing theory. Aim for six to twelve pointers.

### 4.4 Seed Lists Per Phase

Starting points, not complete lists. Run the procedure in 4.2 regardless.

| Phase | Concepts that exist nowhere in the code |
|---|---|
| 02 Prompt System | In-context learning; few-shot ordering effects; instruction hierarchy as a trained convention, not a security boundary; prompt drift across models; holdout sets and sample size; per-request token economics |
| 03 Structured Outputs | Constrained decoding and grammar-based sampling; why models violate format instructions; schema evolution and compatibility; repair-versus-retry economics; validation as a trust boundary |
| 04 Document Ingestion | PDF text layers vs. scanned images; OCR error characteristics; chunking theory and why boundaries destroy meaning; encoding and normalization; idempotent reprocessing |
| 05 Embeddings And Vector DB | Vector space semantics; cosine vs. dot vs. euclidean; curse of dimensionality; ANN recall-vs-latency (HNSW, IVF); why changing the embedding model forces a full reindex |
| 06 RAG And Citations | Precision vs. recall; MRR and NDCG; bi-encoder vs. cross-encoder; lost-in-the-middle; grounding vs. plausibility; why a citation must be verified, not just emitted |
| 07 Evaluation | Construct validity; inter-annotator agreement; LLM-judge biases (position, verbosity, self-preference); significance and sample size; train/test contamination; Goodhart's law |
| 08 Tool Calling | Capability vs. authority; the confused deputy problem; idempotency keys; dry-run semantics; blast radius; why validation must live outside the model |
| 09 Agents | State machines vs. free-form loops; ReAct; termination and halting; error compounding across steps; the principal-agent problem; human-in-the-loop economics |
| 10 Agent Memory | Working vs. episodic vs. semantic memory; forgetting as a feature; information loss in summarization; memory poisoning; retention and right-to-erasure |
| 11 Safety | Direct vs. indirect prompt injection; why filtering is not a security boundary; defense in depth; the false-positive/false-negative tradeoff; threat modeling; dual-use |
| 12 Multimodal | Image patching and tokenization; resolution vs. cost; OCR vs. vision tradeoffs; visual grounding; modality gaps |
| 13 Voice AI | Sample rates and codecs; streaming ASR latency vs. accuracy; word error rate; diarization; barge-in and turn-taking; real-time budgets |
| 14 Fine-Tuning | Transfer learning; catastrophic forgetting; the low-rank hypothesis behind LoRA; overfitting; when fine-tuning beats RAG and when it loses; data quality over quantity |
| 15 Model Serving | Throughput vs. latency; continuous batching; quantization tradeoffs; KV-cache memory math; cold start; autoscaling stateful GPU workloads |
| 16 Classical ML | Bias-variance; feature leakage; class imbalance; calibration; why an LLM is the wrong tool for tabular prediction; interpretability |
| 17 Search And Ranking | BM25 and TF-IDF; hybrid fusion and reciprocal rank fusion; learning-to-rank; position bias; cold start; online vs. offline metrics |
| 18 Deployment And Monitoring | Progressive delivery (canary, blue-green); error-budget policy; alert fatigue; MTTR; blameless postmortems; why dashboards decay |
| 19 Capstone | Architecture decision records; system narrative; demo design; articulating tradeoffs under questioning |
| 20 LLM Optimization | Amdahl's law; cache hit rate and invalidation; batch vs. online economics; distillation; profile before optimizing |
| 21 MCP | Protocol and capability negotiation; trust boundaries; supply-chain risk; schema drift; least-privilege credentials |
| 22 Multi-Agent | Coordination cost; deadlock and livelock; consensus; emergent behavior; why one good agent usually beats several |
| 23 Advanced RAG | Query decomposition; multi-hop reasoning; graph vs. vector retrieval; recursive summarization; retrieval evaluation depth |
| 24 Generative Media | Diffusion basics; the prompt-to-image gap; provenance and C2PA; deepfake risk; licensing and copyright; moderation tradeoffs |
| 25 Governance | AI risk frameworks; model and system cards; auditability; the regulatory landscape; accountability vs. explainability; incident disclosure duty |

## 5. Standard Structure

Adapt the names in the middle to your phase. Do not drop the load-bearing ones.

```text
1.  Phase Purpose
2.  Source Documents Used
3.  What This Phase Builds
4.  What This Phase Assumes From Previous Phases    <- include blocking prerequisites
5.  Beginner-Friendly Definition
6.  Real Industry Example
7.  What You Must Understand Before Coding          <- vocabulary
8.  Concepts You Cannot Learn From The Code         <- Section 4; mandatory
9.  Business Perspective
10. User Perspective
11. Architecture Perspective
12. Technical Scope: In And Out
13. Recommended Libraries And Why
14. Folder Structure To Create
15. File Responsibilities
16. Data Contracts
17. Database Objects
18. Migration Plan And Deferred Foreign Keys
19-25. Phase-specific design sections
26. API Design
27. Observability
28. Safety And Security Perspective
29. Multi-Tenancy
30. Evaluation Perspective
31. Testing Strategy
32. Implementation Sequence                         <- numbered steps, Step 0 = decisions
33. Detailed Data Flows
34. Failure Modes And Fixes
35. Operations Perspective
36. Frontend Surface
37. Common Mistakes
38. Ticket Mapping
39. Quality Gates And Done Criteria
40. Portfolio Evidence
41. Interview Perspective
42. Glossary
43. Build Checklist
44. Connection To The Next Phase
45. Final Mental Model
```

The map's "Standard Structure For Every Learning Phase" lists 21 topics. This skeleton covers all 21 in a richer arrangement, which is what Phases 00 and 01 already do. Follow the written phases — consistency across the set matters more than matching the map's list literally.

Numbering must be contiguous, and every `Section N.M` cross-reference must resolve. Use `§` for references to *other* documents so they survive renumbering.

## 6. Conflict Protocol

Conflicts between the source documents are common. Every one you find must be handled like this:

```text
1. State the conflict plainly, with a table of who says what.
2. Quote both sides.
3. Explain the consequence of not resolving it.
4. Recommend one option and give the reason.
5. Name the acceptable alternative.
6. Say what is NOT acceptable, if something obvious would be wrong.
7. Instruct the reader to write a decision record.
```

Phase 01 §4.1 (identity tables) and §18.2 (migration ordering) are the models. This is the highest-value work a phase author does: it turns a landmine into a decision.

Two conflict types recur:

- **Blocking prerequisite** — your phase needs something an earlier phase does not clearly build. Put it in Section 4 and mark the phase blocked until resolved.
- **Naming drift** — two documents use different names for one thing. Pick the authoritative source, declare the others historical aliases, and say which document should be corrected.

## 7. Scope Boundaries

State in-scope and out-of-scope as two explicit lists. For every out-of-scope item, name the owning phase.

Two rules that prevent scope creep:

- **Create the columns, defer the behavior.** If a later phase needs a field in a table you own, create the field now and say the behavior arrives later. Schemas are designed once.
- **One sentence that draws the line.** Phase 01's is "if the question is *which model and under what limits*, it is Phase 01." Write yours.

## 8. Quality Gate

The document is done when all of these hold:

```text
[ ] Every claim traces to a source document, or is flagged as new
[ ] Every conflict found is stated and resolved with a recommendation
[ ] "Concepts You Cannot Learn From The Code" exists and passes the interview test
[ ] Inline pointers connect that theory to the decisions it explains
[ ] Every configuration example is complete and would load without error
[ ] Every deferred item names its owning phase
[ ] Every ticket maps to the sections that satisfy it
[ ] Acceptance proofs from the tickets appear as real, named tests
[ ] Verification commands from the tickets document are quoted
[ ] Database objects are specified to column, constraint, and index level
[ ] Deferred foreign keys are identified and their hardening migration named
[ ] The document has a glossary AND a definitions section
[ ] Section numbering is contiguous; every cross-reference resolves
[ ] Blocking prerequisites are called out in Section 4, not discovered mid-build
[ ] A reader finishing the previous phase can start this one with nothing missing
```

## 9. Known Pitfalls

Every one of these happened while writing Phase 01.

**Dangling references in a worked example.** A config block referenced three routes that were never defined. It read correctly and would have failed on first run. Check every identifier.

**Copying a source value without tracing it.** A route was copied from the routing document with a field value that made it unreachable by the algorithm this same document specified — and the data-flow section then documented the broken behavior as if intended. Trace copied examples through your own logic.

**Coining a name that already exists.** Span attributes were invented when the crosswalk had already defined them. Search first.

**Cutting teaching content as "duplication".** Glossaries and worked examples that echo earlier sections are the method, not waste. Apply DRY to code, never to lessons.

**Writing about the document instead of the subject.** Structure-mapping tables and self-indexes add length and teach nothing.

**Renumbering with a script and breaking cross-document references.** A rewrite of "Section N" caught four references pointing at *other* documents. Use `§` for external references so this cannot happen.

## 10. The Handoff Kit

To commission a phase, give the author:

```text
1. This file
2. A per-phase brief  (see HOW-TO-WRITE-phase-02-prompt-system.md)
3. The previous phase document
4. The documentation folder
```

The per-phase brief should be short — 200 to 400 lines — and contain only:

```text
- The tickets for this phase and their acceptance proofs
- The exact source sections to read, with pointers
- Conflicts already found, with enough detail to verify independently
- What the previous phase hands over
- This phase's seed concept list from Section 4.4
- The scope line that separates it from adjacent phases
```

Everything else is in this file, and does not need repeating per phase.

## 11. First Three Steps For Any Phase Author

1. Read the previous phase document end to end. Notice that every section opens with why the thing exists before saying what it is.
2. Read your phase's blueprint section and schema section together, in one sitting, with the per-phase brief's conflict list beside you. Verify each conflict yourself rather than trusting the list.
3. Draft three things before anything else: the source-document table, the in/out scope lists, and the concept list from the Section 4.2 procedure. If you cannot fill in "out of scope, owned by phase N" for the two nearest phases, re-read the coverage matrix before writing another word.
