# Lesson Types

Select the closest lesson type and add its requirements to the common template.

## Concept and architecture

Emphasize:

- Mental models
- Component boundaries
- Data and control flow
- Decision criteria
- Tradeoff tables
- Small executable demonstrations

Do not stop at theory. Include a minimal implementation or architecture exercise.

## Application engineering

Emphasize:

- User workflow
- API and data contracts
- Backend integration
- Structured outputs
- Persistence
- Human review
- Feedback
- Product and business metrics

Require an end-to-end vertical slice.

## Data and retrieval

Emphasize:

- Provenance
- Validation
- Chunking or transformation
- Index design
- Permissions
- Freshness
- Delete propagation
- Independent retrieval evaluation

Require labelled queries or data-quality checks.

## Model training or post-training

Emphasize:

- Untouched baseline
- Data splits and leakage prevention
- Tokenization and templates
- Training objective
- Hyperparameters
- Checkpoints
- GPU memory
- Experiment tracking
- Before-and-after behavior
- Safety regression
- Artifact registration
- Serving

Never evaluate on training data.

For LoRA or QLoRA, require target modules, rank, scaling, trainable parameters, memory comparison, adapter handling, and serving choice.

For preferences, require rubric, pair quality, reference behavior, over-optimization checks, and refusal/over-refusal evaluation.

## Agent and tool workflow

Emphasize:

- Explicit state
- Tool schemas
- Read versus write actions
- Argument validation
- Identity and permissions
- Idempotency
- Approval
- Retry and compensation
- Step, time, and spending limits
- Complete traces

Require task-completion and invalid-action evaluation.

Do not use multi-agent architecture without a demonstrated need.

## Evaluation, safety, or security

Emphasize:

- Threat or behavior taxonomy
- Representative and adversarial datasets
- Rubrics
- Deterministic checks
- Human review
- Statistical uncertainty
- Regression gates
- Incident workflows

Require evidence that a control prevents or detects a specific failure.

## Production, MLOps, or infrastructure

Emphasize:

- Reproducibility
- Identity
- Networking
- Configuration
- Registries and lineage
- CI/CD
- Resource limits
- SLOs
- Failure injection
- Canary, shadow, and rollback
- Capacity and cost

Require operational commands and verification.

## Classical ML or deep learning

Emphasize:

- Problem formulation
- Simple baseline
- Feature or representation pipeline
- Train/validation/test separation
- Leakage
- Metric choice
- Calibration where relevant
- Error and subgroup analysis
- Batch and online serving
- Drift and retraining

Compare against a non-ML or simpler model baseline.

## System design or capstone

Emphasize:

- Requirements
- Scale assumptions
- Component ownership
- Data contracts
- Trust boundaries
- Failure modes
- Quality and business metrics
- Build-versus-buy decisions
- Cost
- Migration and rollout

Require architecture decisions and explicit rejected alternatives.
