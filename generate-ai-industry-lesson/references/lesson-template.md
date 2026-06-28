# Lesson Template

Use this template for every substantial lesson unless the user explicitly asks for a different structure.

The standard is:

```text
full conceptual understanding
+ full runnable implementation
+ production judgment
+ retention support
- repeated academic scaffolding
```

Do not compress concepts to make a lesson feel lean. Remove duplicate framing, not knowledge.

## Source compliance contract

Before drafting or revising a lesson, extract a private source compliance contract from the
curriculum and lesson-plan files. This contract is not usually a learner-facing section. It is a
generation and review checklist that prevents source requirements from being accidentally dropped.

The contract must include:

- required concepts and terminology;
- required tools and services;
- guided implementation tasks;
- business implementation or project deliverable;
- evaluation criteria and acceptance evidence;
- production concerns;
- practical assignment requirements;
- interview preparation scope;
- prerequisite and next-lesson boundaries.

For each source requirement, decide where it belongs:

- **Essential module:** concept or skill the learner must understand during the main path.
- **Project artifact:** code, data, test, report, or configuration the learner must build.
- **Production/reference layer:** operational concern, comparison table, checklist, or runbook item.
- **Manual/optional path:** tool or experiment that is useful but not required for the runnable core.
- **Deferred boundary:** item that belongs to a later lesson and must be named as a non-goal or bridge.

Do not silently omit a required source tool or concern. If a source-required item is not implemented
directly, mention it in one of these ways:

- as an optional/manual experiment;
- as an alternative tool with switching criteria;
- as a production or governance checklist item;
- as a next-lesson dependency;
- as an explicit non-goal with rationale.

Examples:

- If the source lists Jupyter but the lesson uses scripts for reproducibility, mention Jupyter as an
  optional controlled-experiment notebook while keeping scripts as the source of truth.
- If the source lists a hosted model API but the current lesson is not the API-integration lesson,
  allow manually recorded hosted results and defer automated provider integration to the next lesson.
- If the source lists regional availability or provider data policy, include them in the
  model-selection memo, security section, or production-readiness checklist.

## Core design

Every lesson must be built around one coherent business scenario and one cumulative project increment.

Use a dynamic module system:

- **Concept-build module:** for topics where the learner needs deep conceptual understanding.
- **Hybrid module:** for topics where concept and implementation must be taught together.
- **Implementation module:** for topics where the main work is building, testing, operating, or deploying a component.

Classify each module before writing. Do not force every topic into the same repeated substructure.

## Readability and concept-teaching standard

Preserve technical vocabulary, but do not introduce it as isolated terminology. Teach every important
concept through this progression:

```text
plain idea
  -> technical name
  -> concrete business example
  -> production consequence
  -> implementation or test
```

For foundation, architecture, model, retrieval, agent, security, and infrastructure lessons, write the
explanation so a learner can first form a mental picture, then attach the correct technical language.
Do not reduce the technical depth. Reduce the cognitive friction.

Use this prose pattern whenever a concept is non-trivial:

```text
Start with: "What is happening in plain terms?"
Then define: "The technical term is ..."
Then show: "In this lesson's business workflow, this appears when ..."
Then warn: "The common failure is ..."
Then connect: "The code/test makes this visible by ..."
```

Avoid these patterns:

- term lists without explanation;
- table-only teaching for first exposure;
- jumping from a definition directly into a large code block;
- assuming a learner understands why a component exists because its name is familiar;
- explaining model internals without connecting them to observable product behavior;
- adding implementation before the learner knows what the implementation is trying to make visible.

Before substantial code, add a short bridge paragraph:

```text
This code does not build the whole system. It makes <concept> observable by <artifact/test>.
```

This is required for all future lessons. The target reading experience is:

```text
understand the concept
  -> see why it matters
  -> inspect the implementation
  -> verify behavior
  -> remember the decision rule
```

## Universal lesson structure

```text
# Lesson title

## Lesson brief
## Business target
## Starting checkpoint
## System map and build roadmap

## [Concept-build / Hybrid / Implementation] module 1: Topic
## [Concept-build / Hybrid / Implementation] module 2: Topic
## [Concept-build / Hybrid / Implementation] module 3: Topic
## [Concept-build / Hybrid / Implementation] module 4: Topic
## [Concept-build / Hybrid / Implementation] module 5: Topic
## Optional module 6-9 when needed

## Reference glossary
## Full test suite
## Experiment playbook
## Evaluation and acceptance
## Model-selection or system-decision memo
## Failure modes and debugging
## Security, privacy, and governance
## Performance and cost
## Deployment and operations
## Bridge to the next lesson
## Practical assignment
## Interview preparation
## Mastery check
## Production-readiness checklist
## Lesson summary
## Official references
```

Use five to nine modules. A short lesson can use five. A deep foundation, RAG, agent, model-training, or production lesson should usually use seven to nine.

## Lesson title

Use a precise capability-oriented title.

Good:

```text
Foundation Models and LLM Fundamentals
Model API Integration and Multi-Provider Reliability
Embeddings and Semantic Retrieval
```

Avoid vague titles such as `Introduction`, `Advanced AI`, or `Project`.

## Lesson brief

This replaces separate metadata, learning outcomes, prerequisites, and "how to use this lesson" sections.

Use a compact table:

```text
| Item | Detail |
|---|---|
| What you learn | ... |
| What you build | ... |
| Why it matters | ... |
| Primary roles | ... |
| Prerequisites | ... |
| Tools | ... |
| Estimated time | ... |
| Final deliverable | ... |
| Carries forward | ... |
| Verified | Date checked for changing technical details |
```

Keep this section short. Do not repeat the business case here.

## Business target

This replaces separate "why this lesson exists" and "business problem" sections.

Include:

```text
Current workflow:
Target workflow:
Inputs:
Outputs:
Constraints:
Risk level:
Acceptance metrics:
Non-goals:
```

Non-goals are required. They prevent lesson drift into later lessons.

Examples:

```text
Non-goals:
- This lesson does not build RAG.
- This lesson does not fine-tune a model.
- This lesson does not deploy an autonomous agent.
```

## Starting checkpoint

This replaces long prerequisite and prior-knowledge activation sections.

Include:

```text
You should already know:
Required setup:
Answer before continuing:
- Question 1
- Question 2
- Question 3
```

Use three to five prior-knowledge questions. They must connect to previous lessons or required assumptions.

## System map and build roadmap

This is required before the modules. It gives the learner the full system shape before code begins.

Include these subsections:

```text
### Concept map
### Project architecture
### Trust boundaries
### State ownership
### Failure boundaries
### Tool choices
### Project structure
### Environment setup
### Data/API contract
### Baseline
### Build milestones
### Implementation assembly checklist
```

Use only the subsections that are relevant, but never omit:

- Concept map
- Project architecture
- Trust boundaries
- Build milestones
- Implementation assembly checklist

### Concept map

Show the conceptual flow the learner must understand.

Example:

```text
text
  -> tokenizer
  -> token IDs
  -> embeddings
  -> transformer blocks
  -> logits
  -> decoding
  -> output
  -> evaluation
```

### Project architecture

Show the project flow the learner will build.

Example:

```text
synthetic cases
  -> schema validation
  -> model runner
  -> result store
  -> evaluator
  -> report
```

### Trust boundaries

Identify where data, model output, user input, tools, external APIs, and logs become risky.

Do not write generic security text. Tie each boundary to the lesson system.

### Tool choices

For each major tool, state:

```text
Purpose:
Why selected:
Important limitation:
Alternative:
When to switch:
```

Select one primary tool for each capability. Mention alternatives in a table instead of implementing many equivalent frameworks.

Every source-required tool must be accounted for. Classify each as:

- implemented in the core project;
- used manually or optionally;
- mentioned as an alternative;
- deferred to a later lesson;
- rejected for this lesson with a reason.

### Project structure

Show the final file tree.

Every file shown should either appear in a module or be clearly marked optional.

### Environment setup

Include:

- dependencies;
- environment variables;
- local services;
- Docker or Compose when relevant;
- verification command;
- no real credentials.

### Data/API contract

Include:

- input schema;
- output schema;
- valid example;
- invalid example;
- boundary example;
- validation rule;
- provenance;
- privacy;
- versioning.

For model training, include split and leakage rules. For APIs, include idempotency and compatibility rules.

### Baseline

Always establish the simplest useful baseline before adding AI or optimization.

The baseline can be:

- deterministic rules;
- keyword/rule classifier;
- SQL query;
- non-RAG search;
- simple model;
- existing workflow measurement.

State what the baseline proves and what it does not prove.

### Build milestones

Map modules to concrete artifacts:

```text
| Module | Type | Concept focus | Implementation artifact | Tests |
|---|---|---|---|---|
```

### Implementation assembly checklist

Required.

Include:

```text
At the end of this lesson, your project should contain:
- file or directory
- file or directory

After each module, run:
- command

The final verification command is:
- command

The final expected artifact is:
- report/API/model/index/deployment/etc.
```

This prevents copy-paste implementation gaps.

## Module type A: Concept-build module

Use when the topic is mainly conceptual.

Examples:

- tokenization;
- embeddings;
- attention;
- transformer blocks;
- model lifecycle;
- leakage;
- calibration;
- retrieval scoring;
- gradient descent;
- quantization.

Structure:

```text
## Concept-build module N: Topic

### Core question
### Key concepts
### Connected dry run
### Mental model
### Worked example
### Mini-implementation
### Tests
### Verify
### Module completion checkpoint
### Common misconception
### Guided practice and independent transfer
### Recall
```

### Core question

Ask one question the learner should be able to answer after the module.

### Key concepts

Place this section before the mental model. Its job is to give the learner the vocabulary needed to
understand the mental model without feeling lost.

Define terms at first use. Do not rely only on the glossary.

For each important concept, explain:

```text
Concept/term:
Why it matters:
Very simple example:
```

Write these explanations as if explaining the term to a layperson, while preserving the correct
technical language. The learner should build a strong understanding of the definitions before seeing
the mental model.

Good:

```text
Concept/term: Logit
Why it matters: The model uses logits to score possible next tokens before choosing what to generate.
Very simple example: If the prompt is "refund requires", the model may give " evidence" a higher
score than " banana".
```

Weak:

```text
Logit: unnormalized score.
```

The weak version is technically true, but it is not enough for first exposure.

For every major concept, teach the idea in this order. You do not have to use these exact labels in
the learner-facing prose, but the explanation must contain this logic:

```text
Plain idea:
Technical definition:
Business/workflow example:
Production consequence:
Failure mode:
Implementation or demo that makes it observable:
```

Use tables for comparison or lookup, not as the only explanation of a new idea.

### Connected dry run

Place this section after Key concepts and before the mental model when the module has a process,
pipeline, lifecycle, model-internal flow, data flow, runtime flow, or several definitions that only
make sense together.

Its job is to connect the definitions into one simple start-to-end example. The learner should be
able to say, "I know the terms, and now I can see how they work together."

Use one example from the lesson's business workflow. Walk through it slowly:

Start with this overview table:

```text
Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | ... | ... |
| 2 | ... | ... |
| 3 | ... | ... |
```

Then write the deeper walkthrough with matching step numbers:

```text
Input or situation:
Step 1: what changes?
Step 2: what changes next?
Step 3: what does the system/model/component have now that it did not have before?
Step 4: which key concept is active here?
Step 5: what can go wrong?
Final state: what has been achieved, and what has not been proven?
```

The dry run must be deeper than a short example. It should explicitly show:

- a compact step table before the detailed explanation;
- matching step numbers in the detailed walkthrough;
- the object/state before the step;
- the object/state after the step;
- which key concept is being used;
- why that step matters for the project;
- what misunderstanding or production failure it prevents.

Examples where a connected dry run is required:

- text -> tokens -> token IDs -> embeddings -> hidden states;
- hidden states -> logits -> probabilities -> decoding -> output;
- prompt/context -> prefill -> decode -> KV cache -> latency/cost;
- query -> retrieval -> reranking -> context -> grounded answer;
- tool request -> permission check -> tool call -> audit record -> recovery;
- training data -> split -> training -> evaluation -> model-selection decision.

For a simple implementation-only module with one obvious action, this section can be omitted. If the
module has three or more interacting concepts or components, include it.

### Mental model

Give a clear conceptual model after the key concepts section and, when used, after the connected dry
run. Use a diagram when relationships matter. The mental model should connect already introduced
concepts into a working picture, not introduce many new terms for the first time.

### Worked example

Show the concept step by step with reasoning.

### Mini-implementation

Add a small runnable demo that makes the concept observable.

### Tests

Include unit tests when the mini-implementation is code.

### Verify

Give the exact command and expected outcome.

### Module completion checkpoint

Required.

Use:

```text
At this point, your project should:
- contain these files
- pass these tests
- produce this output
- preserve these safety/quality constraints
```

### Common misconception

Use:

```text
Misconception:
Why it seems plausible:
Correct model:
Test case:
```

### Guided practice and independent transfer

Provide:

- one guided task with hints;
- one non-identical transfer task.

### Recall

Ask three to five closed-book questions.

## Module type B: Hybrid module

Use when the topic requires both deep concept and serious implementation.

Examples:

- generation controls;
- context windows;
- structured output;
- retrieval quality;
- agent tool use;
- evaluation;
- safety controls;
- model selection;
- prompt/context engineering.

Structure:

```text
## Hybrid module N: Topic

### Core question
### Key concepts
### Connected dry run
### Concept model
### Product consequence
### Worked example
### Build
### Tests
### Experiment
### Interpret results
### Verify
### Module completion checkpoint
### Failure drill
### Common misconception
### Guided practice and independent transfer
### Recall
```

### Key concepts

Place this section before the concept model. Explain the vocabulary the learner needs before they
see the system/process model.

For each important concept, explain:

```text
Concept/term:
Why it matters:
Very simple example:
```

Use layman-friendly explanations while preserving correct technical language. If a concept is
advanced, explain the plain idea first and then name the term.

### Connected dry run

Required for hybrid modules when the learner must understand how concepts drive behavior before
implementing the component. Use one small business example and trace it through the system from
input to observable output.

Show:

- a `Dry-run map` table with `Step | What happens | Concepts being used`;
- the input or event entering the system;
- the intermediate states created by the model, data contract, runtime, evaluator, or tool;
- where each key concept appears in the flow;
- what the implementation will later make visible or enforce;
- what the flow does not prove.

After the table, use matching numbered step headings in the deeper walkthrough. Keep the example
simple enough to follow, but explain each transition deeply enough that a learner can reconstruct the
process without memorizing the table of terms.

### Concept model

Explain the technical idea deeply enough to support implementation and interview reasoning.

Use the readability standard:

```text
plain idea -> technical name -> business example -> production consequence -> implementation/test
```

Do not list advanced terms before the learner has a simple mental model for the behavior.

### Product consequence

Connect the concept to the business workflow, user risk, cost, latency, quality, or reliability.

### Build

Show exact files and complete code for the relevant component.

Before the first large code block, add a bridge explaining what hidden behavior the code exposes and
why that artifact belongs in the project.

### Tests

Place tests immediately after the code they verify.

### Experiment

Define a concrete experiment:

```text
Input:
Settings:
Metric:
Expected evidence:
Failure signal:
```

### Interpret results

Explain what the experiment proves and what it does not prove.

### Verify

Give the command and expected output.

### Module completion checkpoint

Required.

### Failure drill

Use a realistic failure:

```text
Failure:
Evidence:
Fix:
Prevention:
```

### Common misconception

Required.

### Guided practice and independent transfer

Required.

### Recall

Required.

## Module type C: Implementation module

Use when the topic is mainly building, operating, or deploying a component.

Examples:

- schemas;
- persistence;
- API wrapper;
- CLI;
- telemetry;
- Docker;
- deployment;
- CI/CD;
- serving infrastructure.

Structure:

```text
## Implementation module N: Capability

### Purpose
### Key concepts
### Connected dry run
### Design decision
### Build
### Unit tests
### Verify in runtime
### Module completion checkpoint
### Failure drill
### Production note
### Guided practice and independent transfer
### Recall
```

For every implementation component, include:

```text
Purpose:
Key concepts when the component introduces important operational vocabulary:
Connected dry run when several implementation pieces interact:
Design decision:
Concept-to-code bridge:
Complete code:
Test:
Runtime verification:
Failure drill:
Operational concern:
```

For implementation modules, the connected dry run can be operational rather than conceptual. Still
start with the same `Dry-run map` table, then explain the matching numbered steps. Example:

```text
CLI command
  -> load config
  -> validate input
  -> call service
  -> write result
  -> emit logs/traces
  -> health check
  -> rollback decision
```

Do not add deployment or cloud tools merely to appear advanced. Include them when they support the lesson outcome or prepare the next lesson.

## Reference glossary

Required for substantial lessons.

Include all important terms for lookup, but do not force the learner to read the glossary before the modules.

Do not use the glossary as a substitute for inline explanation.

## Full test suite

Required.

Include:

```text
Command:
Expected result:
Test map:
What this suite proves:
What this suite does not prove:
```

Separate software tests from model/system evaluation.

## Experiment playbook

Required for AI, ML, retrieval, agent, evaluation, safety, or production lessons.

Use a concrete table:

```text
| Experiment | Input | Settings | Metric | Expected evidence | Failure signal |
|---|---|---|---|---|---|
```

Examples:

- tokenizer comparison;
- greedy versus sampled decoding;
- base versus instruction model;
- context growth;
- missing evidence;
- adversarial instruction;
- structured-output attempt;
- retrieval recall;
- agent invalid action;
- latency and cost report;
- quality regression.

## Evaluation and acceptance

Required.

Include:

- held-out cases;
- functional metrics;
- model/system quality metrics;
- business metrics;
- latency/cost metrics;
- safety/security gates;
- acceptance threshold.

Never fabricate results. Use empty result fields or templates when the lesson is not executed.

## Model-selection or system-decision memo

Required.

Use `Model-selection memo` for model-focused lessons.

Use `System-decision memo` for application, RAG, agent, infrastructure, or MLOps lessons.

Template:

```text
Decision:
Candidate or design:
Evidence:
Measured strengths:
Measured failures:
Blocked risks:
Cost/latency notes:
Privacy/security notes:
Operational notes:
Decision:
Next experiment:
```

When models, providers, data residency, or hosted services are involved, the memo must also account
for source-required deployment and governance factors such as:

- model ID and revision;
- provider or serving location;
- regional availability;
- data-retention and training-on-input policy;
- privacy or enterprise controls;
- rate limits and fallback implications.

## Failure modes and debugging

Required.

Use:

```text
| Symptom | Likely causes | Diagnostic evidence | Corrective action | Prevention |
|---|---|---|---|---|
```

Include topic-specific failures, not only generic operational failures.

## Security, privacy, and governance

Required when the lesson touches data, users, tools, APIs, models, retrieval, agents, deployment, logs, or generated outputs.

Tie controls to the lesson architecture:

- authentication and authorization;
- tenant isolation where relevant;
- sensitive data and PII;
- secret handling;
- prompt injection or adversarial input;
- tool permissions;
- sandboxing;
- audit logs;
- retention and deletion;
- human approval;
- model/provider data policy;
- applicable standards where relevant.

Do not delegate authorization decisions to an LLM.

## Performance and cost

Required.

Include relevant dimensions:

- latency;
- throughput;
- input/output token cost;
- CPU/GPU memory;
- storage;
- network;
- batch size;
- concurrency;
- caching;
- prefill/decode or equivalent phase costs;
- unit economics.

Provide a measurement procedure.

## Deployment and operations

Required for application, API, agent, retrieval, MLOps, production, or capstone lessons.

For conceptual lessons, include a lightweight operational path and clearly mark it as operational practice, not production integration.

Include:

- packaging;
- configuration;
- health checks;
- deployment target;
- rollout;
- rollback;
- logs;
- metrics;
- traces;
- alerts;
- runbook;
- ownership.

Default teaching choice for simple app/API lessons:

- local-first;
- Docker;
- OpenTelemetry;
- one simple cloud deployment target, such as Cloud Run;
- alternatives table for AWS/Azure/Kubernetes/GPU serving when relevant.

Do not force Cloud Run for training, GPU inference, distributed systems, or high-throughput serving lessons.

## Bridge to the next lesson

Required.

State exactly what the next lesson assumes the learner can now do.

Example:

```text
The next lesson assumes you can:
- record model ID and revision
- measure token count and latency
- separate model output from validated output
- identify missing-evidence and unsafe-output failures
```

## Practical assignment

Required.

Include:

```text
### Scenario
### Requirements
### Constraints
### Required artifacts
### Acceptance criteria
### Stretch goals
```

The assignment must require transfer. It must not be a direct copy of the worked example.

## Interview preparation

Required.

Include:

```text
### Concept questions
### Coding or implementation questions
### Debugging questions
### System-design question
### Tradeoff questions
```

For each category, include strong-answer expectations. Do not provide slogans.

## Mastery check

Required.

Use:

```text
### One-page memory model
### Retrieval bank
### Self-assessment
### Spaced-review plan
```

Retrieval prompts must include:

- recall;
- explanation;
- prediction;
- diagnosis;
- comparison;
- transfer.

Spaced review must include:

- one day;
- three days;
- one week;
- three to four weeks.

## Production-readiness checklist

Required.

Use actionable checkboxes covering:

- data;
- code;
- tests;
- evaluation;
- security;
- performance;
- deployment;
- monitoring;
- cost;
- rollback;
- documentation;
- next-lesson handoff.

## Lesson summary

Required.

Summarize:

- concepts learned;
- implementation built;
- important tradeoffs;
- common mistakes;
- production outcome;
- what carries forward.

## Official references

Required when current tools, APIs, libraries, services, standards, or external claims are used.

Use primary sources:

- official product documentation;
- official framework documentation;
- standards bodies;
- original papers when needed.

Record verification date for changing technical details in the lesson brief.

## Final quality gate

Before calling a lesson complete, verify:

- source compliance contract is satisfied;
- every required source concept, tool, guided implementation item, evaluation criterion,
  production concern, assignment requirement, and interview topic is covered or explicitly deferred;
- one coherent business scenario;
- concept map and project architecture;
- five to nine classified modules;
- every major concept has definition, mental model, example, production consequence, failure mode, and implementation/demo;
- process-heavy or interaction-heavy modules include a connected dry run that starts with a `Step | What happens | Concepts being used` table, uses matching numbered walkthrough steps, traces one simple example from start to finish, and shows where each key concept comes into play;
- every non-trivial concept follows the readability progression:
  plain idea -> technical name -> business example -> production consequence -> implementation/test;
- tables support explanations but do not replace first-pass teaching;
- substantial code blocks have concept-to-code bridge paragraphs;
- every major implementation component has purpose, design decision, complete code, test, runtime verification, failure drill, and operational concern;
- module completion checkpoints exist;
- experiment playbook exists;
- decision memo exists;
- bridge to next lesson exists;
- full tests and evaluation are separated;
- security, performance, deployment, and operations are tied to the architecture;
- no unsupported benchmark numbers or fabricated results;
- no secrets or private data;
- original curriculum scope is preserved;
- no required source tool or production concern is omitted silently;
- source files are not overwritten unless explicitly requested.
