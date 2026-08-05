# Atlas AI Platform - Frontend UX Specification

## 1. Purpose

This document specifies the Atlas web console from an implementation perspective.

The frontend should feel like an enterprise AI operations console, not a marketing website. It should be dense, clear, searchable, filterable, and useful for repeated work.

## 2. Global UX Rules

- Use authenticated app shell with left navigation and top tenant selector.
- Every table supports loading, empty, error, filtered-empty, and pagination states.
- Every AI workflow exposes trace ids or run ids for debugging.
- Risky actions show explicit confirmation and approval status.
- Generated answers show citations and evidence, not only final text.
- Admin-only features are hidden and also blocked by backend permissions.
- Long-running jobs show status, progress, retry, and error reason.
- Do not expose hidden system prompts or provider secrets in the UI.

## 3. Navigation

Primary nav:

```text
Dashboard
Chat
Documents
Agents
Approvals
Prompts
Evaluations
Models
Safety
Media
Voice
Observability
Governance
Admin
```

## 4. Dashboard Screen

### 4.1 Purpose

Show system health and recent AI activity.

### 4.2 Main Components

- KPI row: AI runs today, cost today, p95 RAG latency, safety blocks, failed jobs.
- Queue cards: ingestion queue, eval queue, media generation queue.
- Recent AI runs table.
- Pending approvals panel.
- Evaluation health panel.
- Safety incidents panel.

### 4.3 Filters

- Tenant.
- Time range.
- Use case.
- Model route.
- Status.

### 4.4 Empty States

- No AI runs yet: show link to upload document or run first chat query.
- No approvals: show clean empty state.
- No eval runs: show link to create/import dataset.

## 5. Chat And RAG Screen

### 5.1 Layout

Three-pane layout:

```text
left: conversations
center: message thread
right: evidence and trace drawer
```

### 5.2 Message States

- User message pending.
- Assistant streaming response.
- Assistant final response.
- Model error.
- Safety blocked response.
- Not enough information response.

### 5.3 Citation Behavior

Each cited claim should link to:

- Document title.
- Page number.
- Chunk id.
- Supporting excerpt.
- Confidence/support label.

Right drawer tabs:

```text
Sources
Retrieval Trace
AI Run
Feedback
```

### 5.4 Retrieval Trace View

Show:

- Original query.
- Rewritten query.
- Retrieval strategy.
- Filters.
- Top-k chunks.
- Initial score.
- Rerank score.
- Included in context yes/no.
- Knowledge index version.

### 5.5 Feedback Controls

- Thumbs up/down.
- Incorrect answer.
- Missing citation.
- Wrong citation.
- Unsafe answer.
- Comment.

Feedback should create a record linked to answer id and AI run id.

## 6. Documents Screen

### 6.1 Document List

Columns:

```text
title
collection
status
source type
chunk count
embedding status
created by
created at
actions
```

Filters:

- Collection.
- Status.
- MIME type.
- Uploaded by.
- Date range.

Actions:

- View.
- Reingest.
- Delete.
- Export metadata.

### 6.2 Upload Flow

States:

```text
select file
validate file
uploading
queued
processing
processed
failed
```

Failed state shows:

- Error code.
- Error message.
- Retry/reingest action.

### 6.3 Document Detail

Tabs:

```text
Overview
Extracted Text
Chunks
Embeddings
Lineage
Audit
```

Chunk viewer should show:

- Chunk text.
- Page range.
- Token count.
- Metadata.
- Embedding model.
- Active/deleted status.

## 7. Agents Screen

### 7.1 Agent Definitions

List columns:

```text
name
status
allowed tools
max steps
requires approval
last run
```

### 7.2 Agent Run Detail

Use a trace timeline.

Each step shows:

- Step number.
- Step type.
- Status.
- Input summary.
- Output summary.
- Tool call link.
- AI run link.
- Cost and latency.

Step types:

```text
classify_task
retrieve_context
create_plan
validate_plan
execute_tool
verify_result
request_approval
final_answer
```

### 7.3 Agent Error States

Show explicit stop reason:

- Max steps exceeded.
- Tool permission denied.
- Approval rejected.
- Safety blocked.
- Provider failed.
- Verification failed.

## 8. Approval Queue

### 8.1 List View

Columns:

```text
risk level
requested action
requested by
agent run
created at
expires at
status
```

Filters:

- Risk level.
- Tool name.
- Agent.
- Status.
- Requesting user.

### 8.2 Approval Detail

Show:

- Action summary.
- Full tool arguments.
- Dry-run result if available.
- Evidence/citations.
- Risk explanation.
- Requesting agent/user.
- Audit history.

Actions:

```text
Approve
Reject
Request clarification
Expire
```

Rules:

- Approve/reject requires reviewer permission.
- Decision requires reason for high/critical risk.
- Approved action resumes waiting agent run.

## 9. Prompt Management Screen

Tabs:

```text
Templates
Versions
Test Cases
Eval Results
Optimization Jobs
```

Prompt version detail shows:

- System prompt.
- User template.
- Variables.
- Output schema.
- Model defaults.
- Status.
- Activation history.

Actions:

- Create version.
- Run tests.
- Run eval.
- Request approval.
- Activate approved version.
- Retire version.

## 10. Evaluation Dashboard

### 10.1 Dataset List

Columns:

```text
name
use case
version
case count
status
last run
```

### 10.2 Eval Run Detail

Layout:

```text
top: summary scores
left: filters and tags
center: case results table
right: selected case detail
```

Summary cards:

- Correctness average.
- Groundedness average.
- Citation accuracy.
- Safety failures.
- Cost.
- p95 latency.
- Regression count.

Case table columns:

```text
case id
tags
difficulty
pass/fail
correctness
groundedness
citation accuracy
cost
latency
```

Selected case detail tabs:

```text
Input
Expected
Candidate Output
Baseline Output
Retrieved Context
Judge Explanation
Human Review
```

## 11. Models Screen

Tabs:

```text
Providers
Routes
AI Runs
Costs
Capabilities
```

Route list columns:

```text
use case
provider
model
priority
status
reasoning
prompt caching
restricted data allowed
fallback
```

Route detail shows:

- Capabilities.
- Token limits.
- Reasoning budget.
- Cache configuration.
- Data policy.
- Eval score.
- Cost profile.
- Rollback route.

## 12. Safety Screen

Tabs:

```text
Policies
Safety Checks
Red-Team Runs
Violations
PII
Prompt Injection
```

Violation detail shows:

- Subject type.
- AI run/tool call/agent run.
- Policy violated.
- Severity.
- Action taken.
- Redacted input/output.
- Reviewer notes.

## 13. Media Screen

Tabs:

```text
Generation Jobs
Assets
Safety Review
Feedback
```

Generation job states:

```text
queued
running
completed
blocked
failed
cancelled
```

Asset detail shows:

- Prompt.
- Provider/model.
- Cost.
- Safety status.
- Provenance.
- Download/view link.
- Feedback.

## 14. Voice Screen

Tabs:

```text
Sessions
Transcripts
Summaries
Retention
```

Voice session detail shows:

- Consent status.
- Audio retention deadline.
- Transcript segments.
- Speaker diarization.
- Summary.
- Action items.
- Safety checks.

## 15. Observability Screen

Tabs:

```text
AI Runs
Traces
Costs
Latency
Jobs
Alerts
SLOs
```

AI run detail shows:

- Provider.
- Model.
- Prompt version.
- Operation name.
- Token usage.
- Cache tokens.
- Reasoning tokens.
- Cost.
- Latency.
- Linked RAG/agent/tool/eval records.

## 16. Governance Screen

Tabs:

```text
System Cards
Model Cards
Risk Register
Provider Policies
Incidents
Reviews
Compliance Export
```

Risk register filters:

- Severity.
- Category.
- Owner.
- Status.
- Next review date.

Incident detail shows:

- Severity.
- Timeline.
- Impact.
- Affected route/tool/model.
- Mitigation.
- Root cause.
- Corrective actions.

## 17. Admin Workflows

Admin can:

- Manage users and roles.
- Manage tenant settings.
- Configure model providers.
- Configure model routes.
- Enable/disable tools.
- Register MCP servers.
- Set cost budgets.
- Set retention policies.
- Export tenant data.

All admin actions create audit events.

## 18. Frontend Acceptance Criteria

Frontend is implementation-ready when:

- Every screen has loading, empty, error, and success states.
- Tables support pagination and filters.
- Chat shows citations and retrieval trace.
- Agent page shows step-by-step trace.
- Approval queue can approve/reject risky actions.
- Eval dashboard shows failed cases and judge explanations.
- Model route page shows provider capabilities and data policy.
- Safety page shows violations and red-team results.
- Governance page shows system cards, model cards, risk register, and incidents.
- UI never exposes hidden prompts or secrets to unauthorized users.
