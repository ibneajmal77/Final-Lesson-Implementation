# Lesson Template

Use a two-layer structure:

- **Learning path:** cognitively sequenced modules for first-pass understanding and retention.
- **Reference and production depth:** complete implementation and operational material.

Use every required section unless genuinely inapplicable. Explain omissions.

## Lesson title

Use a precise capability-oriented title.

## Lesson metadata

Include:

- Primary role or roles
- Difficulty
- Estimated study time
- Estimated implementation time
- Prerequisite lessons
- Project increment
- Tools
- Verified date for changing technical details

## How to use this lesson

Explain:

- Essential first pass
- Hands-on path
- Production/reference path
- Suggested study sessions
- Where to stop and retrieve before continuing

## Why this lesson exists

Explain:

- Industry use
- Business value
- Where it appears in production
- Roles that need it
- When it should not be used

## Business problem

Define:

- Organization and user
- Current workflow
- Pain point
- Inputs and outputs
- Constraints
- Risk level
- Baseline
- Success metrics

## Learning outcomes

Use measurable verbs such as implement, evaluate, diagnose, compare, deploy, and defend.

## Prerequisites

List:

- Knowledge
- Previous lessons
- Software
- Accounts or services
- Hardware
- Data

Provide a fallback for unavailable paid services or GPUs where practical.

## Activate prior knowledge

Ask three to five questions connecting the lesson to prerequisites. Do not answer them
immediately.

## Lesson concept map

Show:

- Prior concepts
- New concepts
- Build artifact
- Production outcome
- Next lesson dependency

## Learning module map

List five to nine modules. For each, include:

- Central question
- Estimated time
- New concepts
- Practice artifact

## Essential learning modules

For every module, use:

### Module question

Ask one prediction or diagnostic question.

### Concepts

Introduce three to seven concepts. Define terms at first use.

### Mental model

Use one concise explanation or visual.

### Worked example

Demonstrate the complete reasoning and verification.

### Guided practice

Provide a completion task with hints.

### Independent practice

Provide a non-identical transfer task.

### Retrieval checkpoint

Ask three to five closed-book questions.

### Misconception check

Correct at least one likely misconception.

### Connection

Link the module to previous and next concepts.

After every two or three modules, add a cumulative retrieval checkpoint.

## Reference glossary

Collect all terminology for later lookup. Do not require reading it before the modules.

## Cumulative mental model

Reconstruct the complete lesson flow after the modules.

## Architecture and data flow

Include:

- Component diagram
- Request, data, or training flow
- Trust boundaries
- State ownership
- Failure boundaries

Use Mermaid only when the rendering environment supports it; otherwise use a compact text diagram.

## Design decisions

Compare:

- Selected approach
- Deterministic baseline
- Main alternatives
- Selection criteria
- Tradeoffs

## Tooling

For each selected tool, state:

- Purpose
- Why selected
- Important APIs or configuration
- Limitations
- Alternative
- When the alternative is preferable

## Project structure

Show the files created or changed.

## Environment setup

Include:

- Dependencies
- Environment variables
- Services
- Configuration
- Docker setup when relevant
- Verification command

Never include real credentials.

## Data contract

Include:

- Input schema
- Output schema
- Valid example
- Invalid example
- Boundary example
- Validation
- Provenance
- Privacy
- Versioning

For training, include split and leakage rules. For APIs, include idempotency and compatibility.

## Establish the baseline

Implement or define the simplest valid baseline. Record its evaluation method.

## Minimal working implementation

Build the smallest end-to-end vertical slice.

For every milestone:

- State the goal.
- Show the relevant file.
- Explain the important logic.
- Provide a verification step.
- Describe the expected result.

Use worked-example fading:

- Fully worked vertical slice
- Partially completed extension
- Independent transfer task

## Production implementation

Add:

- Typed configuration
- Validation
- Error handling
- Timeouts
- Bounded retries
- Idempotency
- Logging
- Authentication and authorization
- Persistence
- Concurrency controls
- Tests
- Observability

Include only controls relevant to the architecture, but explain any omitted production concern.

## Testing

Separate:

- Unit tests
- Integration tests
- Contract tests
- End-to-end tests
- Data tests
- Security tests
- Failure tests

State what each category protects.

## Evaluation

Define:

- Held-out evaluation data
- Functional metrics
- Model or system metrics
- Business metrics
- Latency and throughput
- Resource use
- Cost
- Safety and security gates

Include a comparison table with empty result fields if the lesson is not being executed.

Never fabricate measured results.

## Failure modes and debugging

Use a table:

| Symptom | Likely causes | Diagnostic evidence | Corrective action | Prevention |
|---|---|---|---|---|

Include normal operational failures and topic-specific failures.

## Security, privacy, and governance

Cover:

- Threats
- Trust boundaries
- Identity
- Permissions
- Sensitive data
- Secrets
- Audit logs
- Retention and deletion
- Human approval
- Applicable standards

Show where controls are enforced.

## Performance and cost

Cover relevant dimensions:

- Time complexity
- Memory
- CPU or GPU
- Network
- Storage
- Batch size
- Concurrency
- Caching
- Latency
- Throughput
- Unit economics

Provide a measurement procedure.

## Deployment

Include:

- Packaging
- Configuration
- Infrastructure
- Health checks
- Migration
- Release strategy
- Canary or shadow deployment
- Rollback

## Observability and operations

Define:

- Logs
- Metrics
- Traces
- Dashboards
- Alerts
- Ownership
- Runbook
- Incident response

Connect operational metrics to quality and business outcomes.

## Practical assignment

Require the learner to extend or transfer the implementation.

Specify:

- Scenario
- Requirements
- Constraints
- Required artifacts
- Acceptance criteria
- Optional stretch goals

The assignment must require transfer to a different case or constraint. It must not be a copy of
the worked example.

## Interview preparation

Include:

- Concept questions
- Coding or implementation questions
- Debugging scenarios
- System-design questions
- Tradeoff questions
- Strong-answer expectations

Do not provide memorized slogans as answers.

## One-page memory sheet

Include:

- Central mental model
- Key relationships
- Decision table
- Five common misconceptions
- Essential commands or formulas

## Retrieval bank

Include ten to twenty closed-book prompts spanning:

- Recall
- Explanation
- Prediction
- Diagnosis
- Comparison
- Transfer

## Spaced-review plan

Define retrieval tasks for:

- One day
- Three days
- One week
- Three to four weeks

## Production-readiness checklist

Use actionable checkboxes covering:

- Data
- Code
- Tests
- Evaluation
- Security
- Performance
- Deployment
- Monitoring
- Cost
- Rollback
- Documentation

## Lesson summary

Summarize:

- Concepts learned
- Capability built
- Important tradeoffs
- Common mistakes
- Production outcome
- Next lesson
