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

## Core design

Every lesson must be built around one coherent business scenario and one cumulative project increment.

Use a dynamic module system:

- **Concept-build module:** for topics where the learner needs deep conceptual understanding.
- **Hybrid module:** for topics where concept and implementation must be taught together.
- **Implementation module:** for topics where the main work is building, testing, operating, or deploying a component.

Classify each module before writing. Do not force every topic into the same repeated substructure.

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
### Mental model
### Key concepts
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

### Mental model

Give a clear conceptual model before code. Use a diagram when relationships matter.

### Key concepts

Define terms at first use. Do not rely only on the glossary.

For every major concept, include:

```text
Definition:
Mental model:
Example:
Production consequence:
Failure mode:
Implementation or demo:
```

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

### Concept model

Explain the technical idea deeply enough to support implementation and interview reasoning.

### Product consequence

Connect the concept to the business workflow, user risk, cost, latency, quality, or reliability.

### Build

Show exact files and complete code for the relevant component.

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
Design decision:
Complete code:
Test:
Runtime verification:
Failure drill:
Operational concern:
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

- one coherent business scenario;
- concept map and project architecture;
- five to nine classified modules;
- every major concept has definition, mental model, example, production consequence, failure mode, and implementation/demo;
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
- source files are not overwritten unless explicitly requested.
