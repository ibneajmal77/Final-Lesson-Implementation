# How To Write Phase 02 - Prompt System

## 1. What You Are Being Asked To Produce

One file:

```text
learning-phases/phase-02-prompt-system.md
```

It is a **lesson**, not a specification. A reader should finish it able to build the prompt system *and* able to explain, in an interview, why prompts are versioned assets, why a prompt change is a production change, and how anyone knows whether a new prompt is better than the old one.

The two documents already written are your template and your quality bar:

```text
learning-phases/phase-00-engineering-foundation.md   (48 sections, ~3,500 lines)
learning-phases/phase-01-llm-gateway.md              (49 sections, ~4,200 lines)
```

Read Phase 01 completely before you write anything. Length is not the target — completeness is. Phase 02 is a smaller phase than Phase 01 and may legitimately come out shorter.

## 2. Read These First, In This Order

| Document | What you need from it |
|---|---|
| `learning-phases/phase-01-llm-gateway.md` | The template, the house style, and what Phase 02 inherits |
| `00-Atlas-Documentation-Map.md` | Phase list, execution order, the standard-structure requirement |
| `01-Atlas-Technical-Master-Blueprint.md` §16 | Prompt system design: types, lifecycle, rendering, variables, testing, optimization |
| `01-…-Blueprint.md` §11.5 | `prompt_templates`, `prompt_versions`, `prompt_test_cases` field lists |
| `04-Atlas-Database-Schema-Specification.md` §6.1–6.2 | Implementation-ready columns, constraints, indexes |
| `06-Atlas-Implementation-Tickets.md` P02-001…P02-008 | The eight tickets and their acceptance proofs |
| `02-Atlas-Coverage-Matrix.md` §7 | Which prompt topics are Phase 02 vs Phase 07 vs Phase 20 |
| `05-Atlas-Standards-Crosswalk.md` | OWASP LLM01 and LLM07 map directly onto prompts |
| `10-Atlas-Operations-Runbooks.md` §7, §8 | Bad RAG answer and prompt injection runbooks reference prompt versions |
| `08-Atlas-Frontend-UX-Specification.md` | The Prompts screen your API must feed |

## 3. Non-Negotiable Rules

**Trace every claim to a source document.** Open with a source table like Phase 01 §2. If you design something the source set implies but never specifies, say so explicitly — do not let an invention look like a citation.

**When two source documents conflict, resolve it in writing.** State the conflict, quote both sides, recommend one option, name the alternative, and instruct the reader to record a decision. Phase 01 §18.2 and §4.1 are the pattern to copy. Section 6 below lists the conflicts already found for you.

**Every example must actually work.** If you write a configuration block, every identifier it references must be defined in the same block. A worked example that would fail on first run teaches the reader something false.

**Say what is deferred and to which phase.** Phase 02 is adjacent to Phase 03 (structured outputs), Phase 07 (evaluation), Phase 11 (safety), and Phase 20 (optimization). Draw those lines explicitly.

**No meta-commentary about the document itself.** No "what this document adds", no self-index of divergences, no structure-mapping tables. Argue each divergence where it occurs and move on.

**Do not fear repetition.** This is a teaching document. A concept explained in context, restated in a glossary, and shown again as a worked example is not duplication — it is three passes for a reader who does not have it yet. Keep the definitions section *and* the glossary. Keep the implementation sequence *and* the checklist.

## 4. The Requirement That Is Easiest To Miss

Phase 00 and Phase 01 each have a section called **"Concepts You Cannot Learn From The Code"** (Phase 00 §6, Phase 01 §8). Phase 02 must have one too, and it is the most important section you will write.

The rule: **if a concept falls inside this phase's scope but cannot be expressed as a file, a test, or a migration, it must be in the document — because there is nowhere else the learner will ever encounter it.**

A learner can implement a prompt registry perfectly and still not know what in-context learning is, why few-shot examples work, or why moving one sentence in a prompt can change output quality measurably. Those are Phase 02's ideas. If you leave them out, they are simply never taught.

For Phase 02, that section must cover at least:

**How prompting actually works**
- In-context learning: why a model can perform a task from examples without weight updates
- Zero-shot, few-shot, and why example *selection and ordering* changes results
- Why instructions at the start and end of a prompt carry more weight than the middle
- Chain-of-thought: what "think step by step" does mechanically, and when it does nothing
- Why models follow format instructions inconsistently — the setup for Phase 03

**The instruction hierarchy**
- System vs. developer vs. user roles, and that this is a *convention the model was trained on*, not an enforced security boundary
- Why "user text must never be treated as system instructions" is a design rule, not a model guarantee
- Where this connects to prompt injection (name the risk, leave defenses to Phase 11)

**Prompts as production assets**
- Why a prompt change is a deploy: it changes behavior with no code review, no type check, no compiler
- Prompt drift, and why a prompt tuned to one model silently degrades on another
- Why prompt text belongs in a versioned store rather than a source file — and the honest counter-argument
- Config-as-data versus config-as-code, and the audit consequences of each

**Measuring a prompt change**
- Why "it looks better" is not evidence
- Baseline vs. candidate; holdout sets; why you cannot evaluate on examples you tuned against
- Sample size intuition: why 5 examples prove nothing and why small differences need many cases
- Regression versus improvement, and why a prompt fix for one case often breaks another

**Token economics of prompts**
- A prompt's cost is paid on every single request, forever
- The tradeoff between few-shot examples and per-request cost
- Stable-prefix construction and why it pairs with Phase 01 §8.5's KV cache mechanism

Close it as Phase 01 does, with a short "carry these forward" list, and add inline pointers from the sections whose decisions the theory explains.

## 5. Structure To Follow

Mirror Phase 01. Adapt names as needed; do not drop the load-bearing ones.

```text
1.  Phase Purpose
2.  Source Documents Used
3.  What This Phase Builds
4.  What Phase 02 Assumes From Phases 00 and 01   <- include blocking prerequisites
5.  Beginner-Friendly Definition Of A Prompt System
6.  Real Industry Example
7.  What You Must Understand Before Coding         <- vocabulary
8.  Concepts You Cannot Learn From The Code        <- Section 4 above; mandatory
9.  Business Perspective
10. User Perspective
11. Architecture Perspective
12. Technical Scope: In And Out
13. Recommended Libraries And Why
14. Folder Structure To Create
15. File Responsibilities
16. Prompt Data Contracts
17. Database Objects
18. Migration Plan And Deferred Foreign Keys
19. Prompt Lifecycle And Governance
20. Prompt Rendering And Variable Validation
21. Prompt Testing
22. API Design
23. Observability
24. Safety And Security Perspective
25. Multi-Tenancy
26. Evaluation Perspective
27. Testing Strategy
28. Implementation Sequence
29. Detailed Data Flows
30. Failure Modes And Fixes
31. Operations Perspective
32. Frontend Surface
33. Common Mistakes
34. Ticket Mapping
35. Quality Gates And Done Criteria
36. Portfolio Evidence
37. Interview Perspective
38. Glossary
39. Build Checklist
40. Connection To Phase 03
41. Final Mental Model
```

The map's §"Standard Structure For Every Learning Phase" lists 21 topics. This skeleton covers all of them in a richer arrangement, which is what Phases 00 and 01 already do. Follow the two written phases; consistency across the set matters more than matching the map's list literally.

## 6. Conflicts Already Found — You Must Resolve These

Four real conflicts exist in the source set for Phase 02. Handle each in the Phase 01 §18.2 style.

### 6.1 `prompt_test_cases` is missing from the implementation-ready schema

Ticket P02-001 requires "prompt template/version/**test case** tables". The blueprint §11.5 defines `prompt_test_cases` with fields:

```text
id, tenant_id, prompt_template_id, name,
input_json, expected_behavior, expected_output_json, created_at
```

But `04-Atlas-Database-Schema-Specification.md` §6 defines only `prompt_templates` and `prompt_versions`. The implementation-ready document is missing a table the ticket demands.

You must produce the full column/constraint/index specification for it yourself, in the schema document's own style, and mark it clearly as filling a gap. Decide and justify: does a test case attach to a *template* (survives version changes — the blueprint's choice) or to a *version* (pinned, but must be copied forward)?

### 6.2 The lifecycle has eight stages; the schema allows five statuses

Blueprint §16.2:

```text
draft -> local test -> eval dataset test -> review -> approved -> active -> monitored -> retired
```

Schema §6.2 check constraint:

```sql
check (status in ('draft','testing','approved','active','retired'))
```

"local test", "review", and "monitored" are not statuses. Are they stages that map onto `testing` and `active`, or are they missing states? Recommended resolution: treat the eight as *lifecycle stages* and the five as *persisted statuses*, and publish the mapping table explicitly. If you disagree, argue it — but do not leave a reader to discover that the diagram and the constraint disagree.

### 6.3 Nothing enforces one active version per template

`prompt_versions` has `unique(prompt_template_id, version_number)` — which prevents duplicate version numbers and nothing else. Two versions of the same template can both be `active`, and then "prompt registry finds active version" (blueprint §16.3) is undefined behavior.

Phase 01 solved the identical problem for routes with a partial unique index. Apply the same pattern:

```sql
create unique index uq_prompt_versions_one_active
on prompt_versions(prompt_template_id)
where status = 'active';
```

State it as a gap you are closing, and add a migration test that proves activating a second version fails.

### 6.4 Prompt optimization tables exist only in the blueprint

Blueprint §16.6 defines `prompt_optimization_jobs` and `prompt_optimization_candidates`. Neither appears in the schema specification. Ticket P02-008 asks only for "a placeholder for prompt optimization jobs" with the proof "candidate prompt remains draft".

Recommended: do not build these tables in Phase 02. Document them as Phase 20 work, and satisfy P02-008 with the *rule* rather than the machinery — an optimizer may only ever create `draft` versions and can never activate one. That rule is the part with teaching value.

### 6.5 Also carry forward from Phase 01

- **`ai_runs.prompt_version_id` foreign key.** Phase 01 created it as a nullable soft reference. Phase 02 creates `prompt_versions`, so Phase 02 owns the migration that hardens it. This is ticket P02-007 and it is easy to forget.
- **`use_case` vocabulary.** `prompt_templates.use_case` must use the same values as `model_routes.use_case`. Phase 01 §7.4 ratified `chat, classification, rag_answer, embedding, llm_judge`, treating `classifier` and `judge` as historical aliases. Do not introduce a third spelling.
- **The identity-table prerequisite.** `prompt_templates.owner_user_id` and `prompt_versions.created_by_user_id` reference `users`. Phase 01 §4.1 documents the unresolved question of whether Phase 00 creates the identity tables. Same blocker, same resolution.

## 7. Scope

**In scope:** prompt template and version tables; test case table; the registry that resolves a use case to the active version; the renderer with required-variable validation; the lifecycle and its status transitions; activation gated on approved status; storing `prompt_version_id` on every `ai_run`; prompt CRUD, versioning, and activation APIs; a prompt test runner; audit records on activation.

**Out of scope, and say which phase owns each:** output schema validation and repair loops (Phase 03); retrieval and context packing (Phase 06); scoring, judges, and eval datasets (Phase 07); prompt injection defenses and PII (Phase 11); automatic prompt optimization (Phase 20); the prompt admin UI (Phase 19).

The line worth stating: **Phase 02 owns what text is sent and which version was used. It does not own whether the answer was good.**

## 8. Tickets

| Ticket | Task | Acceptance Proof |
|---|---|---|
| P02-001 | Add prompt template/version/test case tables | Migration applies |
| P02-002 | Build prompt registry and renderer | Render test passes |
| P02-003 | Validate required prompt variables | Missing variable test fails safely |
| P02-004 | Add prompt CRUD/version/activate endpoints | Contract tests pass |
| P02-005 | Add prompt test runner | Prompt test cases execute |
| P02-006 | Activation requires approved status | Draft activation blocked |
| P02-007 | Store `prompt_version_id` in `ai_runs` | Trace links to prompt version |
| P02-008 | Placeholder for prompt optimization jobs | Candidate prompt remains draft |

Phase-level verification commands from the tickets document:

```text
alembic upgrade head
pytest tests/prompts tests/api/test_prompts.py
```

Map every ticket to the sections that satisfy it, as Phase 01 §42 does.

## 9. What Phase 01 Hands You

```text
A gateway that accepts messages          -> rendered prompts become those messages
ai_runs.prompt_version_id                -> nullable column waiting for your FK
gen_ai.prompt.name / gen_ai.prompt.version -> span attributes already emitted, currently empty
A deterministic mock provider            -> prompt tests need no provider key
Route selection by use case              -> a prompt can target the right model
Cost and latency baselines               -> so a prompt change's cost impact is measurable
```

That last one carries the argument for the phase ordering: because Phase 01 measured first, a prompt that adds 400 tokens to every request shows up immediately as a cost regression. Make this point explicitly — it is the clearest illustration in the whole curriculum of why measurement precedes change.

## 10. Quality Bar

The document is done when:

```text
[ ] Every claim traces to a source document, or is flagged as new
[ ] All four conflicts in Section 6 are stated and resolved with a recommendation
[ ] "Concepts You Cannot Learn From The Code" covers everything in Section 4
[ ] Inline pointers connect that theory to the decisions it explains
[ ] prompt_test_cases has a full column/constraint/index specification
[ ] The one-active-version constraint is specified with a migration test
[ ] The ai_runs.prompt_version_id foreign key migration is specified
[ ] use_case values match Phase 01's ratified vocabulary
[ ] Every configuration example is complete and would load without error
[ ] Deferred items name their owning phase
[ ] All eight tickets map to sections
[ ] The document has a glossary AND a definitions section
[ ] Section numbering is contiguous and every cross-reference resolves
[ ] A reader who has finished Phase 01 can start Phase 02 with no missing prerequisite
```

## 11. Mistakes Made Writing Phase 01 — Do Not Repeat Them

**A configuration example with dangling references.** The route config referenced three routes that were never defined. It read correctly and would have failed on first run. Before you publish any config block, check that every identifier it mentions exists in it.

**Copying a source document's value without checking it works.** The private RAG route was copied from the routing document with a `use_case` that made it unreachable by the router — and the data-flow section then documented that broken behavior as if intended. When you copy an example, trace it through your own algorithm before you enshrine it.

**Renaming things the crosswalk already named.** Span attributes were invented (`atlas.ai_run_id`) when the crosswalk already defined them (`atlas.ai_run.id`). Search the source set for a name before you coin one.

**Cutting teaching content in the name of removing duplication.** Definitions, glossaries, and worked examples that repeat each other are the *method*, not waste. Apply DRY to code, not to lessons.

**Writing about the document instead of the subject.** Structure-mapping tables and self-indexes of divergences add length and teach nothing. Put the argument where the decision is.

## 12. First Three Steps

1. Read `phase-01-llm-gateway.md` end to end. Note how each section opens with why the thing exists before saying what it is.
2. Read blueprint §16 and schema §6.1–6.2 together, in one sitting, with Section 6 of this document beside you. Confirm the four conflicts yourself rather than trusting this list.
3. Draft the source-document table and the scope section first. If you cannot fill in "out of scope, owned by phase N" for prompt optimization, safety, and evaluation, re-read the coverage matrix before writing anything else.
