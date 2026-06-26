---
name: generate-ai-industry-lesson
description: Generate, expand, revise, or validate complete industry-focused AI lessons and chapters from an AI curriculum or outline. Use when Codex must write practical Applied AI, Generative AI, LLM, RAG, agent, model-training, LoRA/QLoRA, post-training, MLOps, AI safety, inference, multimodal, or Machine Learning Engineering lessons with business context, runnable implementation, tools, tests, evaluation, deployment, production concerns, projects, and interview preparation. Also use when converting a topic or outline item into a detailed lesson file, continuing a multi-lesson course, or checking whether an AI lesson is sufficiently complete and production-ready.
---

# Generate AI Industry Lesson

Generate one complete, practical chapter at a time. Treat the lesson as professional engineering training, not as an outline, glossary, research survey, or framework tutorial.

Apply this progression:

```text
Understand → Connect → Retrieve → Build → Operate → Retain
```

- **Understand:** Explain the business purpose, concepts, architecture, and tradeoffs.
- **Connect:** Link every new concept to prior knowledge and the cumulative project.
- **Retrieve:** Require closed-book recall, prediction, and self-explanation throughout.
- **Build:** Produce a working implementation and tests.
- **Operate:** Evaluate, secure, deploy, monitor, debug, and control cost.
- **Retain:** Add cumulative review and a spaced-retrieval plan.

## Start with the local curriculum

Read [source-routing.md](references/source-routing.md) before selecting lesson scope.

For a lesson-generation request:

- Identify the exact topic in the detailed outline.
- Read its corresponding lesson entry in the detailed lesson plan.
- Read broader curriculum context only when needed for prerequisites, sequencing, role relevance, or tools.
- Preserve the curriculum's GenAI-first learning order unless the user requests a different order.
- Do not modify an outline or curriculum file when the user requests a new lesson file.

If the requested topic is ambiguous, infer the narrowest useful lesson from adjacent curriculum entries. Ask only when different interpretations would materially change the lesson.

## Determine the lesson type

Read [lesson-types.md](references/lesson-types.md) and select the closest type:

- Concept and architecture
- Application engineering
- Data and retrieval
- Model training or post-training
- Agent and tool workflow
- Evaluation, safety, or security
- Production, MLOps, or infrastructure
- Classical ML or deep learning
- System design or capstone

Use the common lesson structure, then apply the selected type's additional requirements.

## Research changing information

Browse current primary sources when the lesson contains information likely to change, including:

- Model APIs and capabilities
- SDK methods
- Library versions and configuration
- Cloud services
- Agent protocols
- MLOps or serving tools
- Security standards
- Regulations
- Current industry practices

Prefer:

- Official product documentation
- Official framework documentation
- Standards bodies
- Original papers only when needed to explain a method
- Current employer job descriptions when validating industry relevance

Do not rely on third-party tutorials for technical truth when official documentation exists.

Record an exact “verified on” date for changing technical details. Do not invent version numbers, prices, benchmark results, or hardware requirements.

## Plan before writing

Create an internal lesson contract:

- Lesson title
- Primary role or roles
- Prerequisite lessons
- Business problem
- Learner outcome
- Project increment
- Required tools
- Acceptance metrics
- Production endpoint
- Next lesson connection

Keep one primary business scenario throughout the chapter. Introduce secondary examples only when they clarify a tradeoff.

Select one primary tool for each capability. Mention alternatives in a comparison section instead of implementing many equivalent frameworks.

## Write the complete lesson

Follow [lesson-template.md](references/lesson-template.md). The standard lesson structure is the
dynamic hybrid template: classify each module as **Concept-build**, **Hybrid**, or
**Implementation** before writing. Preserve full conceptual depth and full runnable
implementation; remove duplicate scaffolding, not knowledge.
Read [cognitive-learning-design.md](references/cognitive-learning-design.md) and use its
two-layer learning architecture.

Mandatory principles:

- Begin with prior-knowledge activation and a lesson map.
- Segment the essential path into five to nine learning modules.
- Limit each module to one central question and a manageable concept set.
- Use worked-example fading: worked example, guided completion, independent transfer.
- Include closed-book retrieval every 20–30 minutes of expected study.
- Add cumulative retrieval after every two or three modules.
- Define terminology at first use; move the complete glossary to reference material.
- Mark essential, production, specialist, and reference content.
- Write full explanations, not bullet-only notes.
- Define every new technical term when first used.
- Explain why a concept matters before showing how to configure it.
- Connect every major concept to the business problem.
- Include architecture and data flow.
- Establish a baseline before introducing an AI or optimization technique.
- Use realistic data contracts and API contracts.
- Provide runnable or directly implementable code.
- Explain code in cohesive sections; do not narrate every trivial line.
- Add verification after each implementation milestone.
- Include normal, boundary, failure, and adversarial cases.
- Separate software testing from model or system evaluation.
- Measure quality, latency, throughput, resource use, and cost where relevant.
- Include security, privacy, permissions, and auditability.
- Include deployment, observability, rollback, and incident considerations.
- End with an assignment that requires independent application.
- Include interview questions and concise answer expectations.
- Connect the lesson to the next curriculum topic.
- End with a one-page mental model, retrieval prompts, and a spaced-review schedule.

Use unnumbered Markdown headings unless the user requests numbered chapters.

## Implement code at production-learning quality

When writing code:

- Use a coherent project layout.
- Include filenames before code blocks.
- Use typed Python where practical.
- Validate external inputs.
- Keep secrets in environment variables or a secret manager.
- Add explicit error classes.
- Add timeouts and bounded retries for network operations.
- Make write operations idempotent where retries are possible.
- Use structured logging.
- Add unit and integration tests.
- Pin or constrain dependencies when reproducibility matters.
- Include configuration examples without real credentials.
- Include Docker and CI configuration when deployment is in lesson scope.

Avoid:

- Fake imports or nonexistent APIs
- Ellipses replacing required logic
- Large unexplained code dumps
- Notebook-only architecture for a production lesson
- Hard-coded credentials
- Unbounded agent loops
- Authorization decisions delegated to an LLM
- Metrics without data or measurement procedure

If a full implementation is too large for one chapter, provide a working vertical slice and explicitly identify the extension points. Never claim omitted code is complete.

## Handle data rigorously

For lessons involving data:

- Define the schema.
- Show valid, invalid, and boundary examples.
- Explain acquisition, provenance, consent, and licensing where relevant.
- Add validation, cleaning, deduplication, and PII handling.
- Define train, validation, and test separation.
- Prevent leakage.
- Version the dataset or data contract.
- Include deletion and retention behavior when production data is involved.

For synthetic data, define its source model, generation rules, filtering, and human-quality review.

## Evaluate before claiming success

Use a baseline and an unchanged held-out evaluation set.

Define:

- Functional acceptance criteria
- Model or system quality metrics
- Business metrics
- Latency and throughput metrics
- Resource and cost metrics
- Security and safety checks

Report results as templates or measurement procedures when no execution occurred. Mark illustrative values clearly. Never present fabricated results as measured.

For model changes, compare:

- Existing or deterministic baseline
- Untuned model
- Prompted or RAG system when relevant
- Adapted model
- Production candidate

For RAG, evaluate retrieval separately from generation. For agents, evaluate task completion, tool selection, arguments, invalid actions, recovery, step count, latency, and cost.

## Teach failure diagnosis

For every major implementation, include a debugging table containing:

- Symptom
- Likely causes
- Diagnostic evidence
- Corrective action
- Prevention

Prioritize real industry failures such as:

- Rate limiting and timeouts
- Invalid structured output
- Retrieval permission leakage
- Stale indexes
- Training leakage
- Out-of-memory failures
- NaN loss
- Adapter mismatch
- Agent duplicate actions
- Queue replay
- Model quality regression
- Cost spikes
- Monitoring blind spots

## Apply production and security gates

Read [quality-standard.md](references/quality-standard.md) before finalizing.

At minimum, address:

- Authentication and authorization
- Tenant isolation where relevant
- Secret handling
- PII and sensitive data
- Prompt injection or adversarial input
- Tool permissions
- Sandboxing for execution
- Logging and auditability
- Rate and spending limits
- Deployment strategy
- Monitoring
- Rollback
- Incident response

Do not add generic security paragraphs. Tie controls to the lesson architecture and show where enforcement occurs.

## Create the lesson file

When the user requests file output:

- Default to a `lessons/` directory beside the curriculum files unless the user provides another location.
- Use a lowercase hyphenated filename based on the lesson title.
- Do not overwrite an existing lesson unless explicitly asked.
- If a lesson exists, revise it in place only when requested; otherwise create a clearly named successor.
- Preserve all curriculum and outline source files.

Before writing, inspect nearby lesson files and match their conventions without copying defects.

## Validate the completed lesson

Check the lesson against [quality-standard.md](references/quality-standard.md).
Also apply the cognitive quality gate in
[cognitive-learning-design.md](references/cognitive-learning-design.md).

Reject completion if any of these are missing:

- Clear business problem
- Measurable learning outcomes
- Prerequisites
- Conceptual explanation
- Architecture and data flow
- Working implementation
- Tests
- Evaluation
- Failure diagnosis
- Security and privacy
- Performance or cost
- Production deployment or operational path
- Practical assignment
- Interview preparation
- Production-readiness checklist
- Lesson summary and next step
- Prior-knowledge activation
- Five to nine learning modules
- Module retrieval checkpoints
- Guided and independent practice
- Cumulative retrieval
- One-page memory model
- Spaced-review plan

Also verify:

- Code and prose agree.
- Tool choices are justified.
- No source file was overwritten accidentally.
- Current claims are cited when web research was used.
- Links and local file references are valid.
- No secrets or private data appear in examples.

## Adapt lesson depth

Default to a substantial chapter suitable for independent study and implementation.

If the user requests:

- **Beginner lesson:** Add more intuition, terminology, and guided verification.
- **Advanced lesson:** Compress basics and deepen tradeoffs, internals, scaling, and failure analysis.
- **Interview lesson:** Preserve implementation but expand questions, design cases, and debugging scenarios.
- **Workshop:** Split implementation into timed labs and checkpoints.
- **Reference chapter:** Emphasize decision tables, operational commands, and troubleshooting.

Do not reduce a “complete lesson” to a summary unless the user explicitly requests brevity.

## Maintain continuity across lessons

When generating a sequence:

- Reuse the same business domain and evolving capstone where practical.
- State what is reused from earlier lessons.
- Avoid re-teaching completed prerequisites.
- Refactor earlier project components only when the new lesson justifies it.
- Carry forward evaluation datasets, security controls, observability, and deployment assets.
- Keep names and data contracts consistent.
- End with the exact capability added to the cumulative project.

## Resources

- [source-routing.md](references/source-routing.md): Locate and prioritize curriculum sources.
- [lesson-template.md](references/lesson-template.md): Required chapter structure.
- [lesson-types.md](references/lesson-types.md): Type-specific additions.
- [quality-standard.md](references/quality-standard.md): Final quality and completeness gate.
- [cognitive-learning-design.md](references/cognitive-learning-design.md): Human learning,
  retention, retrieval, and lesson segmentation requirements.
