# Cognitive Learning Design

Use this reference when generating or revising every lesson.

## Core principle

Optimize the lesson for:

```text
Understand → Connect → Retrieve → Apply → Retain
```

Technical completeness is necessary but insufficient. A learner must be able to reconstruct the
main ideas without looking, connect them to prior knowledge, and apply them to a new problem.

## Two-layer design

Write every substantial lesson in two layers.

### Learning path

The first layer teaches the essential capability through 5–9 modules. It contains:

- Prior-knowledge activation
- A lesson map
- Small concept sets
- Mental models
- Worked examples
- Guided practice
- Independent practice
- Retrieval checkpoints
- Cumulative review
- Transfer to the business project

### Reference and production depth

The second layer preserves:

- Complete terminology
- Full code and configuration
- Alternatives
- Production hardening
- Security
- Performance
- Deployment
- Debugging
- Detailed reference tables

Label reference material clearly so learners can defer it during the first pass.

## Lesson opening

Start with:

- Why the capability matters
- One coherent business problem
- What the learner will build
- Three to five prior-knowledge questions
- A concept map showing how the lesson connects to earlier and later lessons
- A module map with estimated time and concrete output

Do not start with a long glossary.

## Module size

Limit each module to:

- One central question
- Three to seven new concepts
- One primary mental model
- One worked example
- One guided task
- One independent or transfer task
- Three to five closed-book retrieval questions

If a section exceeds this, split it or move details to reference material.

## Module sequence

Use this sequence:

```text
Activate
→ Explain
→ Demonstrate
→ Guide
→ Independent attempt
→ Retrieve
→ Connect
```

### Activate

Ask a prediction or prior-knowledge question before explanation. The question should expose the
knowledge gap without requiring the learner to already know the answer.

### Explain

Introduce the smallest useful set of concepts. Define terms where they are used.

### Demonstrate

Provide one fully worked example with reasoning and verification.

### Guide

Give a partially scaffolded task. Include hints but not the complete answer immediately.

### Independent attempt

Require a similar but non-identical task.

### Retrieve

Ask closed-book questions. Avoid recognition-only questions. Prefer:

- Explain from memory
- Draw the flow
- Predict behavior
- Diagnose a failure
- Compare alternatives

### Connect

State:

- What prior concept this module used
- What new relationship was established
- What next module depends on it

## Worked-example fading

Use three stages for important procedures:

- Fully worked example
- Completion problem with missing steps
- Independent transfer problem

Do not jump directly from explanation to a large independent project.

## Retrieval and spacing

Include:

- Immediate retrieval after each module
- Cumulative retrieval after every two or three modules
- End-of-lesson closed-book reconstruction
- A spaced-review plan for approximately:
  - One day
  - Three days
  - One week
  - Three to four weeks

Each review should retrieve, not merely reread.

## Interleaving

After introducing related alternatives, mix them in decision exercises.

Examples:

- Prompting versus RAG versus fine-tuning
- Greedy versus sampling
- Batch versus online inference
- Rules versus ML versus LLM

Ask the learner to select an approach from context rather than practise one method repeatedly.

## Concept maps

Use a small visual when three or more concepts interact.

Keep it stable throughout the lesson. Add concepts to the same map rather than introducing
unrelated diagrams.

## Signalling

Mark content as:

- **Essential:** required for the learning outcome
- **Production:** required to operate the capability
- **Specialist:** role-dependent depth
- **Reference:** lookup material

Do not present all content as equally important.

## Code learning

For substantial code:

- Explain the architecture before the code.
- Build one vertical slice.
- Split code into milestones.
- Verify each milestone.
- Ask the learner to predict output before execution.
- Include one debugging task.
- Include one modification task.
- Move large complete listings to the reference layer when they interrupt concept learning.

Avoid more than two large code blocks in one learning module.

## Terminology

Define a term immediately before or during first use.

Keep the full glossary in the reference layer. Do not ask learners to memorize a glossary before
using the concepts.

## Misconceptions

Every module should identify at least one likely misconception and correct it.

Use:

```text
Misconception → Why it seems plausible → Correct model → Test case
```

## Memory artifacts

End every lesson with:

- One-page mental model
- Ten to twenty retrieval prompts
- Key decision table
- Common misconception list
- Spaced-review schedule
- One transfer problem

## Cognitive quality gate

Reject or revise a lesson when:

- More than ten terms appear before the first worked example.
- Practice is delayed until the final third.
- A learner reads more than approximately 20–30 minutes without retrieval.
- Modules introduce more than seven tightly coupled new concepts.
- The lesson lacks prediction, self-explanation, or recall.
- The assignment merely copies the worked example.
- Detailed reference content interrupts the essential learning sequence.
- The lesson has no spaced-review plan.
- The lesson has no cumulative concept map.
- The lesson cannot be summarized from memory using one page.

## Cognitive review score

Score zero to two:

- Prior-knowledge activation
- Segmentation
- Concept load
- Worked examples
- Guided practice
- Independent transfer
- Retrieval practice
- Cumulative connection
- Misconception correction
- Spaced review

Require at least 18 out of 20 and no zero in retrieval, segmentation, or transfer.
