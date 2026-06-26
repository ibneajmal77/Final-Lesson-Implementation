# Lesson Quality Standard

Use this as the final gate.

## Completeness

The lesson must include:

- Business context
- Learning outcomes
- Prerequisites
- Concepts and terminology
- Architecture
- Tool decisions
- Data or API contracts
- Baseline
- Working implementation
- Tests
- Evaluation
- Debugging
- Security and privacy
- Performance and cost
- Deployment
- Observability
- Assignment
- Interview preparation
- Checklist
- Summary and next step

## Depth

Reject the lesson if it:

- Merely restates outline bullets
- Defines terms without applying them
- Shows configuration without explaining behavior
- Provides code without architecture or evaluation
- Provides architecture without implementation
- Calls a notebook prototype production-ready
- Lists tools without choosing and using one
- Uses generic security or monitoring advice

## Industry relevance

Require:

- A recognizable business workflow
- A production owner or user
- Measurable success
- Real operational constraints
- Tools appropriate to the role
- A reason for every major technology choice

Remove:

- Research details that do not affect implementation or interviews
- Unused frameworks
- Exotic methods before standard approaches
- Complexity added only to appear advanced

## Code quality

Verify:

- Names are consistent.
- Imports and APIs are real.
- Code blocks identify files.
- Configuration is typed where practical.
- Inputs are validated.
- Network calls have timeouts.
- Retries are bounded and safe.
- Secrets are externalized.
- Errors are observable.
- Tests cover failure paths.

## Evaluation integrity

Verify:

- A baseline exists.
- Held-out data is defined.
- Training and test data are separated.
- Metrics match the task.
- RAG retrieval and generation are separated.
- Agent actions are evaluated, not only final text.
- Security and safety tests are included.
- Unexecuted values are not presented as measured.
- Limitations are stated.

## Production integrity

Verify:

- Identity and authorization are outside model discretion.
- Tenant and document permissions are enforced before context construction.
- Write operations are idempotent when retryable.
- Consequential actions require appropriate approval.
- Resource, step, time, and spending limits exist where relevant.
- Deployment includes health checks and rollback.
- Monitoring includes quality and business outcomes, not only infrastructure.
- Sensitive telemetry is protected.

## Teaching quality

Verify:

- The lesson begins with prior-knowledge activation.
- The lesson has five to nine cognitively manageable modules.
- Each module has one central question.
- Each module introduces no more than approximately seven tightly related concepts.
- New ideas are introduced in prerequisite order.
- The lesson uses one coherent scenario.
- Explanations precede complex code.
- Worked examples fade into guided and independent practice.
- Each build milestone has a verification step.
- Retrieval appears throughout, not only at the end.
- Cumulative retrieval connects modules.
- Common misconceptions are corrected.
- The assignment requires transfer, not copying.
- Interview questions test reasoning.
- The lesson includes a one-page memory model.
- The lesson includes a spaced-review plan.

## Current-information integrity

Verify:

- Changing claims were checked against official current sources.
- Exact verification date is recorded.
- Version-specific code identifies the version or compatibility range.
- Prices and benchmark numbers are either sourced and dated or omitted.
- Regulations are described with jurisdiction and effective date.

## File integrity

Verify:

- Curriculum source files remain unchanged unless explicitly requested.
- The lesson has a unique, descriptive filename.
- Local links resolve.
- External sources are linked.
- No credentials, tokens, personal data, or proprietary content are included.

## Final scoring

Score each category from zero to two:

- Business relevance
- Conceptual clarity
- Implementation completeness
- Testing
- Evaluation
- Security and privacy
- Production operations
- Performance and cost
- Interview usefulness
- Reproducibility
- Cognitive segmentation
- Retrieval and retention

Interpretation:

- `22–24`: Ready
- `19–21`: Revise minor gaps
- `14–18`: Incomplete
- `<14`: Rewrite

Do not call the lesson complete below 22, when any mandatory section is absent, or when
retrieval, segmentation, or transfer scores zero.
