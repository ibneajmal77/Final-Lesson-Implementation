# Applied AI Problem Discovery

## Lesson metadata

| Field | Value |
|---|---|
| Curriculum position | Core Lesson 07 |
| Primary roles | Applied AI Engineer, Forward-Deployed AI Engineer, AI Product Manager, AI Solutions Architect |
| Supporting roles | Generative AI Engineer, Machine Learning Engineer, AI Evaluation Engineer, AI Governance Specialist |
| Difficulty | Intermediate |
| Estimated study time | 6-8 hours |
| Estimated implementation time | 6-10 hours |
| Prerequisite lessons | Lessons 01-06 |
| Project increment | Applied AI discovery package for customer-support operations |
| Primary tools | Workflow diagrams, product requirements, architecture decision records, risk register, cost model, Python |
| Technical guidance verified | June 25, 2026 |

## Why this lesson exists

Applied AI engineering begins before selecting a model, writing a prompt, or creating a vector
database.

The first responsibility is to determine:

- Which business problem exists
- Which users and affected people are involved
- Whether the problem is important enough to solve
- Whether AI is appropriate
- Which parts should remain deterministic or human-controlled
- How success and failure will be measured
- Whether the expected value justifies the cost and risk

Many unsuccessful AI projects reverse this order:

```text
Choose a model
→ build a demonstration
→ search for a use case
→ discover missing data or workflow access
→ discover quality is difficult to measure
→ discover the business cannot tolerate the failure mode
```

This lesson teaches the correct order:

```text
Understand the workflow
→ measure the baseline
→ identify the decision or task
→ examine non-AI alternatives
→ define acceptable behavior
→ select the smallest sufficient solution
→ design evaluation and controls
→ run a bounded pilot
```

NIST's AI Risk Management Framework Playbook places context mapping before measurement and
management. It explicitly recommends documenting intended purpose, users, operational context,
positive and negative impacts, human roles, requirements, limitations, and non-AI alternatives.
The Playbook also says it is voluntary guidance rather than a universal checklist. As of
June 25, 2026, NIST states that AI RMF 1.0 is being updated; use the current version together
with applicable organizational and legal requirements.

This lesson does not train a model. Its production output is a decision package strong enough
for engineering, product, security, legal, operations, and domain stakeholders to approve,
reject, or reshape an AI initiative.

## Business problem

### Organization

Northstar Support operates customer service for a subscription software product. It handles
approximately 50,000 support cases each month across email, web chat, and an internal ticketing
system.

### Users

- Customers seeking help
- Front-line support agents
- Support supervisors
- Quality-assurance reviewers
- Product specialists
- Security and privacy teams
- Finance and operations leaders

### Affected people

The user and the affected person are not always the same. A supervisor may use an AI-generated
recommendation, but the customer is affected by the resulting response, delay, escalation, or
refund decision.

### Current workflow

```text
Customer submits request
→ routing queue receives ticket
→ agent reads ticket
→ agent identifies issue and urgency
→ agent searches policies and product documentation
→ agent checks customer and order information
→ agent drafts answer
→ agent escalates or requests approval when needed
→ response is sent
→ ticket is closed or reopened
→ quality team samples completed cases
```

### Observed problems

- Initial classification is inconsistent.
- Agents spend significant time searching across several knowledge sources.
- Drafting repetitive responses increases handling time.
- New agents miss escalation rules.
- Refund and account-change actions require careful authorization.
- Management has incomplete data about avoidable rework.
- The company does not have a reliable evaluation set for AI-generated answers.

### Executive request

> "Use AI to automate customer support and reduce cost by 40%."

That request is not yet a valid engineering problem. It does not define:

- Which tasks should be automated
- Which errors are acceptable
- Which actions require human judgment
- Which data is available
- Which customer groups may be affected differently
- Which result represents success
- What happens when the system is uncertain or unavailable

### Discovery objective

Produce a decision package that identifies a valuable, measurable, and controllable first AI
use case. The package must also document rejected ideas and explain why they should not be built
yet.

### Constraints

- The organization operates in the United States and serves customers in multiple regions.
- Customer messages can contain personal and confidential information.
- Financial actions require authorization.
- Policy content changes weekly.
- The first pilot must be reversible.
- Existing agents and ticket systems must continue operating.
- The pilot cannot use customer-facing autonomous responses.
- The team has three months for a first controlled release.

### Risk level

Mixed. Drafting and search assistance are lower consequence when an agent reviews the result.
Autonomous financial or account actions have higher consequence and require stronger controls.

## Learning outcomes

After completing this lesson, you will be able to:

- Identify users, operators, owners, and affected stakeholders.
- Interview stakeholders without turning requests directly into features.
- Map a current business workflow and its failure paths.
- Establish time, cost, quality, and risk baselines.
- Separate symptoms from root causes.
- Define an AI problem using explicit inputs, outputs, decisions, and constraints.
- Compare deterministic software, rules, search, classical ML, LLMs, RAG, tools, agents,
  fine-tuning, multimodal systems, and human work.
- Identify tasks where AI should not be used.
- Define human-review and human-approval boundaries.
- Create measurable business, product, system, and risk metrics.
- Build a risk register and use-case triage model.
- Estimate first-year value, cost, ROI, and payback using scenarios rather than false precision.
- Compare build, buy, and hybrid approaches.
- Write product requirements, architecture decisions, and a pilot plan.
- Define go, revise, and stop criteria before implementation begins.
- Defend an Applied AI proposal in an interview or stakeholder review.

## Prerequisites

### Knowledge

- Production Python fundamentals
- API concepts
- SQL and data modelling
- Testing fundamentals
- Basic understanding of authentication and authorization

### Completed project capabilities

Lessons 01-06 should have produced:

- A reproducible repository
- Typed Python code
- Automated tests
- A backend service
- PostgreSQL and Redis
- Basic user, tenant, ticket, and conversation data models

### Software

- Python 3.13
- uv
- Git
- Markdown editor
- Diagramming tool or Mermaid-compatible editor
- Spreadsheet application

### Data

Use synthetic support data in this lesson. Do not import real customer conversations into a
discovery exercise without approved access, purpose, retention, and privacy controls.

## Key terminology

### Business outcome

A measurable organizational result, such as lower handling time, fewer repeat contacts, higher
resolution rate, or reduced policy violations.

### User task

A specific action performed by a person or system, such as locating the relevant refund policy
for a ticket.

### Workflow

The sequence of people, systems, decisions, inputs, outputs, handoffs, and exceptions required
to complete a business process.

### Bottleneck

A step that limits workflow performance because of capacity, delay, rework, or dependence on
scarce expertise.

### Baseline

The measured performance of the current process or simplest existing solution. An AI system
must be compared with a baseline rather than with an imagined perfect process.

### Counterfactual

The likely outcome if the project is not built. The counterfactual may include process
improvement, better search, additional training, or no change.

### Decision support

A system that provides information or recommendations while a responsible person makes the
decision.

### Automation

A system that performs a task or action with limited or no human intervention.

### Human in the loop

A broad phrase describing human participation in an AI workflow. It is insufficient by itself.
The design must state who reviews what, at which point, with which authority, and within what
time limit.

### Human review

A person examines AI output before it is used. Review may be advisory and does not necessarily
authorize a consequential action.

### Human approval

A person with appropriate authority explicitly authorizes a proposed action.

### Human override

A person can stop, reverse, or replace system behavior.

### Abstention

The system declines to provide a result when evidence, confidence, authorization, or operating
conditions are insufficient.

### Escalation

The workflow transfers a task to a person or team with greater authority or expertise.

### Reversibility

The degree to which an action can be undone and its effects repaired.

### Risk tolerance

The amount and type of risk an organization is willing to accept for a defined use case. It is
an organizational decision, not a model property.

### Total cost of ownership

The complete cost across discovery, implementation, data, model use, infrastructure,
integration, evaluation, security, monitoring, human review, support, and change management.

### Pilot

A bounded production or production-like test designed to validate assumptions before broad
deployment.

### Go/no-go criteria

Predefined evidence thresholds used to approve, revise, pause, or stop a project.

## Mental model

An Applied AI problem is a sociotechnical system, not a prompt.

```text
People
  + workflow
  + data
  + policies
  + software
  + model behavior
  + incentives
  + operating environment
  = actual AI system
```

The model may be one small component:

```text
User request
→ deterministic validation
→ authorized data access
→ retrieval or model inference
→ output validation
→ human review or approval
→ business action
→ feedback and monitoring
```

Discovery asks five questions in order:

```text
Is the problem real?
→ Is the workflow understood?
→ Is the outcome measurable?
→ Is AI the smallest sufficient solution?
→ Can the risk be controlled in operation?
```

If any answer is unknown, the next activity should reduce uncertainty rather than increase
implementation complexity.

## Architecture and discovery flow

```text
Stakeholder interviews
        │
        ▼
Current-state workflow map
        │
        ├── time and volume measurements
        ├── error and rework analysis
        ├── data and access inventory
        └── risk and policy constraints
        │
        ▼
Problem statements and candidate interventions
        │
        ├── non-AI process improvement
        ├── deterministic software or rules
        ├── search
        ├── predictive ML
        ├── LLM or RAG
        └── controlled tool workflow
        │
        ▼
Value, feasibility, and risk triage
        │
        ▼
Selected pilot use case
        │
        ├── product requirements
        ├── evaluation plan
        ├── human-control design
        ├── architecture decision
        └── cost and rollout plan
        │
        ▼
Go, revise, or stop
```

### Trust boundaries

- Customer messages may contain untrusted instructions and sensitive data.
- Ticket-system access is governed by user and service permissions.
- Knowledge sources may contain obsolete or malicious content.
- Vendor systems may process or retain submitted data.
- A model recommendation does not grant business authority.
- Financial and account actions cross a consequential-action boundary.

### State ownership

| State | Owner |
|---|---|
| Business goal | Executive sponsor and product owner |
| Workflow definition | Operations owner |
| Policy and escalation rules | Domain and compliance owners |
| Data access | Data owner and security |
| Risk acceptance | Accountable business and risk owner |
| Technical architecture | Engineering owner |
| Evaluation set | Evaluation owner and domain reviewers |
| Deployment decision | Product, engineering, security, operations, and risk approvers |

### Failure boundaries

- If the baseline is unreliable, pause ROI conclusions.
- If required data cannot be accessed lawfully or operationally, reject or redesign the use case.
- If errors are not detectable before harm, reduce automation.
- If the action is not reversible, require stronger approval and testing.
- If the project cannot define a measurable outcome, do not begin model optimization.

## Discovery artifacts

The lesson produces:

```text
discovery/
├── README.md
├── stakeholder-map.md
├── interview-guide.md
├── current-state-workflow.md
├── baseline-metrics.csv
├── problem-statements.md
├── use-case-register.yaml
├── risk-register.md
├── build-buy-analysis.md
├── product-requirements.md
├── architecture-decision.md
├── evaluation-plan.md
├── pilot-plan.md
├── go-no-go.md
└── response-drafting-scenario.yaml
src/
└── ai_industry_labs/
    └── discovery/
        ├── __init__.py
        ├── models.py
        ├── scoring.py
        └── cli.py
tests/
├── test_discovery_models.py
└── test_discovery_scoring.py
```

## Environment setup

Continue in the `ai-industry-labs` repository created in Lesson 01.

Create the directories.

PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path `
    discovery, `
    src\ai_industry_labs\discovery, `
    tests | Out-Null
```

POSIX shell:

```bash
mkdir -p discovery src/ai_industry_labs/discovery tests
```

Add the YAML parser used by the scenario CLI:

```powershell
uv add "pyyaml>=6,<7"
uv sync --locked
```

Verify the inherited engineering foundation:

```powershell
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

Do not add a model SDK for this lesson. The absence of a model dependency is intentional:
discovery must reach a justified pilot decision before implementation commits to a model
provider.

## Design decisions

### Start with workflow evidence, not model capability

Model demonstrations answer:

> Can a model produce an impressive output?

Discovery must answer:

> Can a controlled system improve this workflow for these users under these constraints?

### Use one primary pilot

Selecting many use cases at once prevents clear evaluation and ownership. This lesson will
select one pilot:

> Evidence-backed response drafting for support agents, with human approval before sending.

### Keep higher-consequence actions out of the first pilot

Autonomous refunds and account changes are rejected for the first pilot. The system may retrieve
relevant policy and propose an action, but an authorized employee must approve it.

### Use scoring for consistency, not automatic decision making

A score can make assumptions visible. It cannot replace stakeholder judgment, legal analysis,
or risk acceptance.

### Require a non-AI alternative

Every candidate use case must be compared with at least one non-AI or simpler alternative.

## Tooling

| Tool | Purpose | Why selected | Limitation |
|---|---|---|---|
| Markdown | Versioned discovery artifacts | Reviewable with code and architecture | Less convenient than specialist product tools for workshops |
| Mermaid or diagram tool | Workflow and architecture diagrams | Makes handoffs and control boundaries visible | Diagrams become stale without ownership |
| Spreadsheet | Baseline and scenario modelling | Accessible to business stakeholders | Formulas and assumptions require review |
| Python | Reproducible scoring and ROI calculations | Testable, versioned, and auditable | Cannot decide risk tolerance |
| Pydantic | Validate use-case records | Prevents incomplete or invalid entries | A valid schema does not guarantee a good proposal |
| Git | Review and history | Creates decision traceability | Sensitive discovery material may need restricted repositories |
| NIST AI RMF Playbook | Context and risk framing | Current official U.S. voluntary guidance | Not a legal classification or complete organizational policy |

## Discovery operating principles

### Separate request, need, and solution

| Layer | Example |
|---|---|
| Request | "Automate support with AI" |
| Need | Reduce repetitive work while maintaining policy compliance |
| Measurable problem | Agents spend 4.8 minutes searching and drafting per eligible case |
| Candidate solution | Search, templates, RAG-assisted draft, workflow redesign, or combination |

### Ask for evidence

Replace:

> "Agents waste a lot of time."

With:

> "How many cases were sampled? What was median search time? How was rework measured?"

### Look for incentives and displacement

An AI system can optimize one metric while moving work elsewhere:

- Faster initial response may increase reopened cases.
- Higher automation may increase supervisor review.
- Lower handling time may reduce customer satisfaction.
- More suggestions may increase agent cognitive load.

### Treat abstention as a valid product outcome

The system should not be forced to answer every case. A high-quality workflow may:

- Draft routine answers
- Request missing information
- Escalate policy ambiguity
- Refuse unsupported financial actions

## Stakeholder discovery

### Stakeholder map

**`discovery/stakeholder-map.md`**

```markdown
# Stakeholder Map

| Stakeholder | Role in workflow | Goals | Risks and concerns | Decision authority | Required involvement |
|---|---|---|---|---|---|
| Customer | Requests support | Accurate and timely resolution | Wrong advice, privacy, unfair treatment | Can accept, reject, or complain | Usability and feedback research |
| Support agent | Operates assistant | Faster evidence and drafting | Automation bias, added review work | Sends response within policy | Discovery, pilot, continuous feedback |
| Supervisor | Handles escalation | Policy compliance and queue performance | Hidden errors and unauthorized actions | Approves exceptions | Requirements and pilot approval |
| Quality reviewer | Audits completed cases | Consistency and root-cause data | Weak evaluation coverage | Defines review rubric | Evaluation design |
| Product owner | Owns outcome | Adoption and business value | Feature without measurable impact | Prioritization | Full lifecycle |
| Security | Protects systems and data | Least privilege and traceability | Data leakage and tool abuse | Security approval | Architecture and testing |
| Privacy or legal | Reviews data use | Lawful and limited processing | Retention, vendor use, consent | Policy approval | Before data use and launch |
| Engineering | Builds and operates | Reliable maintainable system | Undefined requirements and scope | Technical implementation | Full lifecycle |
| Finance | Reviews economics | Defensible cost and benefit | Optimistic ROI assumptions | Budget approval | Scenario review |
```

### Interview guide

Do not ask only:

> "What AI features do you want?"

Ask questions that reveal workflow evidence.

**`discovery/interview-guide.md`**

```markdown
# Stakeholder Interview Guide

## Workflow

- Walk me through the last real case from start to finish.
- Which systems and documents did you use?
- Where did you wait?
- Where did you repeat work?
- Which decisions required judgment?
- Which actions required approval?
- What happened when information was missing?

## Volume and time

- How many cases follow this path?
- What are the median and high-percentile handling times?
- How much time is search, reading, drafting, approval, and rework?
- Does the workload vary by channel, product, language, or customer tier?

## Quality and failures

- What counts as a correct resolution?
- What errors occur most often?
- Which errors are expensive or harmful?
- How are reopened tickets and complaints recorded?
- Which failures are detectable before the customer is affected?

## Data and systems

- What data is required?
- Who owns it?
- How current is it?
- Which permissions apply?
- What information must never be sent to a third party?

## Human control

- Which tasks can be suggested?
- Which tasks can be automated?
- Who can approve consequential actions?
- How quickly can a person intervene?
- Can an action be reversed?

## Success and adoption

- Which metric should improve?
- Which metric must not get worse?
- What would make agents ignore the system?
- What evidence would justify stopping the pilot?
```

### Interview technique

Use:

- Real examples rather than hypothetical preferences
- Neutral questions
- Follow-up questions about exceptions
- Direct workflow observation
- Samples from different user groups and performance levels

Avoid:

- Leading users toward the planned solution
- Treating managers as substitutes for front-line users
- Ignoring affected customers
- Recording sensitive data without approval
- Promising automation before feasibility analysis

## Current-state workflow mapping

### Workflow table

**`discovery/current-state-workflow.md`**

```markdown
# Current-State Support Workflow

| Step | Actor | Input | Action | System | Output | Median time | Failure or rework | Control |
|---|---|---|---|---|---|---:|---|---|
| Intake | Customer | Message | Submit case | Support portal | Ticket | 1 min | Missing account details | Required fields |
| Triage | Queue or agent | Ticket | Assign category and urgency | Ticket system | Routed case | 1.2 min | Incorrect category | Supervisor review sample |
| Investigate | Agent | Ticket and account | Understand issue | Ticket and customer systems | Issue hypothesis | 2.5 min | Missing context | Ask customer |
| Search | Agent | Issue hypothesis | Find policy and product evidence | Wiki and docs | Evidence | 2.1 min | Stale or conflicting content | Escalate |
| Draft | Agent | Evidence | Compose response | Ticket editor | Draft | 2.7 min | Policy omission | Agent review |
| Approve | Supervisor when required | Proposed exception | Approve or reject | Ticket system | Decision | 4-30 min wait | Incomplete justification | Approval policy |
| Send | Agent | Approved response | Send | Ticket system | Customer response | 0.4 min | Wrong recipient or content | Confirmation |
| Follow-up | Customer and agent | Response | Reopen or close | Ticket system | Outcome | Variable | Repeat contact | Quality review |
```

### Workflow measurement rules

- Measure work time separately from queue time.
- Report median and percentiles, not only averages.
- Segment by case type, channel, language, region, and customer tier where appropriate.
- Record sample size and measurement period.
- Do not infer quality from speed alone.

### Failure-path map

```text
Ticket received
├── missing customer context → request information
├── known routine issue → standard resolution
├── conflicting policy → supervisor escalation
├── suspected security incident → security queue
├── refund request → policy check and authorized approval
└── unsupported request → specialist team
```

Discovery must represent these paths. Designing only the happy path creates unsafe automation.

## Establish the baseline

### Baseline dimensions

Measure at least:

- Volume
- Handling time
- Queue time
- Search time
- Drafting time
- First-contact resolution
- Reopen rate
- Escalation rate
- Policy-compliance rate
- Customer satisfaction
- Agent acceptance or workload
- Cost per resolved case

### Synthetic baseline data

**`discovery/baseline-metrics.csv`**

```csv
segment,monthly_cases,median_handle_minutes,p90_handle_minutes,median_search_minutes,median_draft_minutes,reopen_rate,escalation_rate,policy_error_rate,cost_per_case_usd
password_reset,12000,6.2,11.5,0.8,1.9,0.04,0.02,0.01,4.10
billing_question,9000,12.8,25.0,3.4,3.1,0.09,0.12,0.04,8.75
refund_request,5000,16.4,34.0,4.2,3.6,0.11,0.38,0.06,12.20
technical_issue,18000,19.7,45.0,5.8,4.0,0.17,0.31,0.08,15.60
security_concern,1000,28.0,60.0,6.0,4.5,0.08,0.92,0.03,24.00
account_closure,5000,11.0,21.0,2.5,2.8,0.06,0.20,0.03,7.90
```

These values are illustrative synthetic data, not measured company results.

### Baseline quality

Ask:

- Is the metric definition consistent across teams?
- Is handling time distorted by idle time?
- Are policy errors sampled or comprehensively recorded?
- Are reopened cases linked to the original response?
- Are customer outcomes available after ticket closure?
- Does the data exclude contractor or regional workflows?

An unreliable baseline does not justify an invented ROI estimate. It creates a discovery task:
improve measurement first.

## Problem formulation

### Weak problem statement

> Use an LLM to automate support.

### Strong problem statement

> For English-language billing and account-support tickets that do not involve security
> incidents or discretionary financial exceptions, reduce median agent search and drafting time
> by 30% while keeping policy-error and reopen rates no worse than the current baseline. The
> system may retrieve approved evidence and generate an editable draft. An authenticated agent
> must approve every customer-facing response during the pilot.

### Problem-statement template

```text
For [user]
performing [task]
in [operating context],
improve [business outcome]
from [baseline]
to [target]
without degrading [guardrail metrics].

The system receives [inputs]
and produces [outputs].

It may [allowed behavior].
It must not [prohibited behavior].

When [uncertainty, missing evidence, risk, or failure condition],
it must [abstain, request information, or escalate].
```

### Define inputs and outputs

| Element | Pilot definition |
|---|---|
| Input | Ticket text, authorized account metadata, approved policies, product documentation |
| Output | Evidence list, structured issue summary, editable response draft, escalation recommendation |
| Allowed | Search approved sources, summarize evidence, draft non-binding response |
| Prohibited | Send response, issue refund, modify account, expose unauthorized documents |
| Abstain when | Evidence conflicts, policy is missing, security concern exists, identity is unclear |
| Escalate to | Supervisor, billing specialist, security team, or product specialist |

## Root-cause analysis

Do not assume every delay is a model problem.

### Example root causes

| Symptom | Possible root cause | Likely intervention |
|---|---|---|
| Agents search for a long time | Documentation is fragmented | Search and content governance |
| Drafts are inconsistent | No standard response structure | Templates and deterministic validation |
| Escalations are slow | Approval queue is understaffed | Workflow and staffing change |
| Policies are missed | Documents are stale | Ownership and publication process |
| Classification is inconsistent | Categories overlap | Taxonomy redesign or classifier |
| Refund errors occur | Authorization is unclear | Policy engine and approval control |

### Five-whys example

```text
Why are billing tickets reopened?
→ The answer omitted an eligibility condition.

Why was the condition omitted?
→ The agent used an outdated article.

Why was the outdated article discoverable?
→ Search indexes all versions equally.

Why are old versions not removed?
→ Documentation has no effective-date metadata or delete workflow.

Why is there no delete workflow?
→ Content governance was never assigned.
```

The first fix is content governance and retrieval freshness, not fine-tuning.

## Candidate use cases

Create a candidate register before selecting the pilot.

| Candidate | User task | Possible approach | Value hypothesis | Main risk |
|---|---|---|---|---|
| Ticket classification | Assign category and urgency | Rules plus ML or LLM classification | Reduce triage time | Misrouting |
| Knowledge search | Locate relevant policy | Hybrid search | Reduce search time | Stale or unauthorized evidence |
| Response drafting | Draft evidence-backed reply | RAG plus LLM | Reduce drafting time | Hallucination or policy omission |
| Missing-info detection | Identify required customer details | Rules plus structured LLM output | Reduce back-and-forth | Incorrect requirements |
| Escalation suggestion | Recommend specialist queue | Rules plus classifier | Reduce wrong escalation | Under-escalation |
| Refund execution | Issue refund automatically | Tool-using agent | Reduce handling time | Financial loss and unauthorized action |
| Quality review | Sample and score closed cases | Rules plus model-assisted review | Expand QA coverage | Biased or unreliable scoring |
| Voice triage | Transcribe and route calls | Speech plus workflow | Reduce queue time | Consent and transcription error |

## Solution-selection framework

Select the smallest sufficient method.

### Deterministic software

Use when:

- Rules are explicit
- Inputs are structured
- Exact behavior is required
- Errors are unacceptable

Examples:

- Required-field validation
- Authorization
- Refund limits
- Data-retention enforcement
- Schema validation

### Rules

Use when:

- Domain experts can express stable conditions
- Auditability is important
- The rule set remains manageable

Example:

```text
IF issue_type = "security_concern"
THEN route_to = "security"
AND prohibit_response_draft = true
```

### Search

Use when:

- The task is to find current information
- The source of truth changes
- Evidence must be shown

Examples:

- Policy lookup
- Product documentation
- Similar resolved cases

### Classical machine learning

Use when:

- Historical labelled data exists
- Output is a prediction, score, class, or ranking
- The problem has stable features and metrics

Examples:

- Escalation likelihood
- SLA breach risk
- Ticket category

### Foundation-model API

Use when:

- Inputs are unstructured language or multimodal content
- The task requires extraction, summarization, drafting, or flexible interpretation
- Output can be validated or reviewed

### RAG

Use when:

- Answers require current or private evidence
- Citations are valuable
- Knowledge changes more frequently than the model

### Tool calling

Use when:

- The system must query or act through external systems
- Arguments can be validated
- Permissions are enforced outside the model

### Controlled agent workflow

Use when:

- A task requires multiple conditional steps
- State and recovery are explicit
- Step, cost, and permission limits can be enforced

Do not use an open-ended agent when a deterministic workflow is sufficient.

### Fine-tuning

Use when:

- Stable behavior, style, structure, or task patterns are not reliably achieved through
  prompting, retrieval, or tools
- Sufficient high-quality data and evaluation exist

Do not use fine-tuning to store frequently changing policy facts.

### Multimodal model

Use when:

- The workflow depends on images, scanned forms, audio, or video

### Human work

Retain human work when:

- Judgment depends on context not available to the system
- The action is high consequence
- Error detection is weak
- Data or legal conditions are unresolved
- The task is rare enough that automation has poor economics

### Hybrid solution

The selected pilot is hybrid:

```text
Deterministic authorization
+ permission-aware search
+ LLM extraction and drafting
+ schema validation
+ human approval
+ feedback and monitoring
```

## AI suitability test

Reject or redesign the AI use case when several of these conditions apply:

- The problem has no measured baseline.
- The business goal is primarily headcount reduction without workflow analysis.
- Required data is unavailable, unlawful to use, or too poor.
- Correct output cannot be defined or reviewed.
- Errors are high consequence and not detectable before impact.
- The workflow changes faster than the system can be maintained.
- A deterministic rule or process change solves the problem.
- The organization cannot assign operational ownership.
- The expected volume does not justify implementation and review cost.
- The user cannot contest or correct the result.
- The system would create incentives to hide failures.

## Use-case triage model

The scoring tool below helps compare candidates. It is not a legal risk assessment and must not
make the final decision automatically.

### Typed use-case record

**`src/ai_industry_labs/discovery/models.py`**

```python
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class SolutionType(StrEnum):
    PROCESS = "process"
    DETERMINISTIC = "deterministic"
    RULES = "rules"
    SEARCH = "search"
    CLASSICAL_ML = "classical_ml"
    LLM = "llm"
    RAG = "rag"
    TOOL_WORKFLOW = "tool_workflow"
    FINE_TUNING = "fine_tuning"
    MULTIMODAL = "multimodal"
    HUMAN = "human"
    HYBRID = "hybrid"


class UseCase(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    user: str = Field(min_length=3, max_length=120)
    business_outcome: str = Field(min_length=10, max_length=500)
    solution_type: SolutionType
    monthly_volume: int = Field(ge=0)
    minutes_saved_per_case: float = Field(ge=0, le=120)
    adoption_rate: float = Field(ge=0, le=1)
    loaded_labor_cost_per_hour: float = Field(gt=0)
    baseline_error_rate: float = Field(ge=0, le=1)
    expected_error_rate: float = Field(ge=0, le=1)
    error_cost: float = Field(ge=0)
    implementation_cost: float = Field(ge=0)
    monthly_recurring_cost: float = Field(ge=0)
    monthly_oversight_cost: float = Field(ge=0)
    consequence: int = Field(ge=1, le=5)
    autonomy: int = Field(ge=1, le=5)
    data_sensitivity: int = Field(ge=1, le=5)
    uncertainty: int = Field(ge=1, le=5)
    irreversibility: int = Field(ge=1, le=5)
    evidence_quality: int = Field(ge=1, le=5)
    data_readiness: int = Field(ge=1, le=5)
    integration_readiness: int = Field(ge=1, le=5)
    human_approval_required: bool
    non_ai_alternative: str = Field(min_length=5, max_length=500)

    @model_validator(mode="after")
    def validate_expected_error(self) -> "UseCase":
        if self.expected_error_rate > self.baseline_error_rate:
            raise ValueError(
                "Expected error rate cannot exceed baseline in the value scenario. "
                "Use a downside scenario separately."
            )
        return self
```

### Value and triage calculations

**`src/ai_industry_labs/discovery/scoring.py`**

```python
from dataclasses import dataclass

from ai_industry_labs.discovery.models import UseCase


@dataclass(frozen=True)
class BusinessCase:
    annual_labor_benefit: float
    annual_error_avoidance: float
    annual_total_benefit: float
    first_year_total_cost: float
    first_year_net_value: float
    first_year_roi: float | None
    monthly_net_after_launch: float
    payback_months: float | None
    risk_score: int
    readiness_score: int


def calculate_business_case(use_case: UseCase) -> BusinessCase:
    annual_cases_used = use_case.monthly_volume * 12 * use_case.adoption_rate
    annual_hours_saved = annual_cases_used * use_case.minutes_saved_per_case / 60
    annual_labor_benefit = (
        annual_hours_saved * use_case.loaded_labor_cost_per_hour
    )

    errors_avoided = annual_cases_used * (
        use_case.baseline_error_rate - use_case.expected_error_rate
    )
    annual_error_avoidance = errors_avoided * use_case.error_cost
    annual_total_benefit = annual_labor_benefit + annual_error_avoidance

    annual_operating_cost = 12 * (
        use_case.monthly_recurring_cost + use_case.monthly_oversight_cost
    )
    first_year_total_cost = use_case.implementation_cost + annual_operating_cost
    first_year_net_value = annual_total_benefit - first_year_total_cost

    first_year_roi = (
        first_year_net_value / first_year_total_cost
        if first_year_total_cost > 0
        else None
    )

    monthly_benefit = annual_total_benefit / 12
    monthly_net_after_launch = monthly_benefit - (
        use_case.monthly_recurring_cost + use_case.monthly_oversight_cost
    )
    payback_months = (
        use_case.implementation_cost / monthly_net_after_launch
        if monthly_net_after_launch > 0
        else None
    )

    risk_score = (
        use_case.consequence
        + use_case.autonomy
        + use_case.data_sensitivity
        + use_case.uncertainty
        + use_case.irreversibility
    )
    readiness_score = (
        use_case.evidence_quality
        + use_case.data_readiness
        + use_case.integration_readiness
    )

    return BusinessCase(
        annual_labor_benefit=annual_labor_benefit,
        annual_error_avoidance=annual_error_avoidance,
        annual_total_benefit=annual_total_benefit,
        first_year_total_cost=first_year_total_cost,
        first_year_net_value=first_year_net_value,
        first_year_roi=first_year_roi,
        monthly_net_after_launch=monthly_net_after_launch,
        payback_months=payback_months,
        risk_score=risk_score,
        readiness_score=readiness_score,
    )


def triage_recommendation(
    business_case: BusinessCase,
    *,
    human_approval_required: bool,
) -> str:
    if business_case.readiness_score < 7:
        return "research: improve evidence, data, or integration readiness"

    if business_case.risk_score >= 20 and not human_approval_required:
        return "reject: consequence requires stronger human control"

    if business_case.first_year_net_value <= 0:
        return "revise: current value scenario does not justify first-year cost"

    if business_case.risk_score >= 17:
        return "controlled-pilot: narrow scope and require approval"

    return "pilot: proceed with defined guardrails and evaluation"
```

### Why this model is intentionally simple

- It exposes assumptions.
- It supports scenario comparison.
- It does not claim to predict actual model quality.
- It does not convert organizational risk tolerance into an automatic truth.
- It keeps value and risk visible as separate dimensions.

Do not combine value and risk into one "AI score." A high-value, high-risk use case requires
different governance from a low-value, low-risk use case.

### Tests

**`tests/test_discovery_models.py`**

```python
import pytest

from ai_industry_labs.discovery.models import SolutionType, UseCase


def valid_data() -> dict[str, object]:
    return {
        "name": "Evidence-backed response drafting",
        "user": "Support agent",
        "business_outcome": (
            "Reduce search and drafting time without increasing policy errors"
        ),
        "solution_type": SolutionType.HYBRID,
        "monthly_volume": 18000,
        "minutes_saved_per_case": 3.5,
        "adoption_rate": 0.60,
        "loaded_labor_cost_per_hour": 34.0,
        "baseline_error_rate": 0.08,
        "expected_error_rate": 0.06,
        "error_cost": 18.0,
        "implementation_cost": 120000.0,
        "monthly_recurring_cost": 8000.0,
        "monthly_oversight_cost": 4000.0,
        "consequence": 3,
        "autonomy": 1,
        "data_sensitivity": 4,
        "uncertainty": 3,
        "irreversibility": 2,
        "evidence_quality": 4,
        "data_readiness": 4,
        "integration_readiness": 4,
        "human_approval_required": True,
        "non_ai_alternative": (
            "Improve search, policy templates, and agent training"
        ),
    }


def test_valid_use_case_is_accepted() -> None:
    use_case = UseCase.model_validate(valid_data())

    assert use_case.solution_type is SolutionType.HYBRID
    assert use_case.human_approval_required is True


def test_expected_error_cannot_exceed_baseline_in_expected_scenario() -> None:
    data = valid_data()
    data["expected_error_rate"] = 0.20

    with pytest.raises(ValueError):
        UseCase.model_validate(data)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("monthly_volume", -1),
        ("adoption_rate", 1.1),
        ("consequence", 0),
        ("data_readiness", 6),
    ],
)
def test_out_of_range_values_are_rejected(field: str, value: object) -> None:
    data = valid_data()
    data[field] = value

    with pytest.raises(ValueError):
        UseCase.model_validate(data)
```

**`tests/test_discovery_scoring.py`**

```python
from ai_industry_labs.discovery.models import SolutionType, UseCase
from ai_industry_labs.discovery.scoring import (
    calculate_business_case,
    triage_recommendation,
)


def response_drafting_use_case() -> UseCase:
    return UseCase(
        name="Evidence-backed response drafting",
        user="Support agent",
        business_outcome="Reduce search and drafting time without increasing policy errors",
        solution_type=SolutionType.HYBRID,
        monthly_volume=18000,
        minutes_saved_per_case=3.5,
        adoption_rate=0.60,
        loaded_labor_cost_per_hour=34.0,
        baseline_error_rate=0.08,
        expected_error_rate=0.06,
        error_cost=18.0,
        implementation_cost=120000.0,
        monthly_recurring_cost=8000.0,
        monthly_oversight_cost=4000.0,
        consequence=3,
        autonomy=1,
        data_sensitivity=4,
        uncertainty=3,
        irreversibility=2,
        evidence_quality=4,
        data_readiness=4,
        integration_readiness=4,
        human_approval_required=True,
        non_ai_alternative="Improve search, policy templates, and agent training",
    )


def test_business_case_calculates_positive_benefit() -> None:
    result = calculate_business_case(response_drafting_use_case())

    assert result.annual_labor_benefit > 0
    assert result.annual_error_avoidance > 0
    assert result.first_year_net_value > 0
    assert result.risk_score == 13
    assert result.readiness_score == 12
    assert triage_recommendation(
        result,
        human_approval_required=True,
    ).startswith("pilot")


def test_low_readiness_requires_research() -> None:
    use_case = response_drafting_use_case().model_copy(
        update={
            "evidence_quality": 2,
            "data_readiness": 2,
            "integration_readiness": 2,
        }
    )
    result = calculate_business_case(use_case)

    assert triage_recommendation(
        result,
        human_approval_required=use_case.human_approval_required,
    ).startswith("research")


def test_high_risk_autonomy_is_rejected_without_approval() -> None:
    use_case = response_drafting_use_case().model_copy(
        update={
            "consequence": 5,
            "autonomy": 5,
            "data_sensitivity": 4,
            "uncertainty": 4,
            "irreversibility": 4,
            "human_approval_required": False,
        }
    )
    result = calculate_business_case(use_case)

    assert triage_recommendation(
        result,
        human_approval_required=use_case.human_approval_required,
    ).startswith("reject")
```

### Use-case register

**`discovery/use-case-register.yaml`**

```yaml
use_cases:
  - name: "Evidence-backed response drafting"
    user: "Support agent"
    proposed_solution: "Hybrid retrieval, LLM drafting, validation, and human approval"
    non_ai_alternative: "Improve search, policy templates, and agent training"
    expected_value: "Reduce search and drafting time"
    guardrail: "Policy error and reopen rates must not worsen"
    prohibited_actions:
      - "Send a response automatically"
      - "Issue a refund"
      - "Modify an account"
    status: "pilot_candidate"

  - name: "Autonomous refund execution"
    user: "Support operations"
    proposed_solution: "Tool-using agent"
    non_ai_alternative: "Improve approval workflow and refund tooling"
    expected_value: "Reduce refund handling time"
    guardrail: "No unauthorized or incorrect financial action"
    prohibited_actions: []
    status: "rejected_for_first_pilot"
    rejection_reason: "High-consequence action with insufficient evidence and control maturity"
```

## Risk classification

### Risk is use-case specific

The same model can be low consequence in one workflow and high consequence in another.

Examples:

- Drafting an internal summary: lower consequence
- Sending legal or medical advice: higher consequence
- Suggesting a refund: moderate to high consequence
- Executing a refund: higher consequence

### Triage dimensions

| Dimension | Low | High |
|---|---|---|
| Consequence | Minor inconvenience | Financial, legal, safety, rights, or significant customer impact |
| Autonomy | Suggestion only | Executes action without approval |
| Data sensitivity | Public information | Personal, confidential, regulated, or secret data |
| Uncertainty | Output easily verified | Correctness difficult to determine |
| Irreversibility | Easy to undo | Difficult or impossible to repair |
| Scale | Small controlled pilot | Large population or repeated high-volume use |

### Risk register

**`discovery/risk-register.md`**

```markdown
# Applied AI Risk Register

| Risk | Cause | Affected party | Impact | Detection | Preventive control | Response | Owner |
|---|---|---|---|---|---|---|---|
| Unsupported answer | Missing or irrelevant evidence | Customer and agent | Wrong guidance | Citation and human review | RAG, abstention, evaluation | Escalate and correct | Product owner |
| Unauthorized evidence | Permission filter failure | Customer or employee | Confidentiality breach | Access tests and audit | Pre-retrieval authorization | Disable feature and investigate | Security |
| Automation bias | Agent trusts fluent draft | Customer | Missed policy condition | Edit and error analysis | Source display and training | Increase review and narrow scope | Operations |
| Stale policy | Old document remains indexed | Customer | Incorrect answer | Freshness checks | Version and delete workflow | Reindex and review affected cases | Knowledge owner |
| Cost overrun | Long context or high usage | Organization | Budget impact | Cost dashboard | Token and rate budgets | Route or pause | Engineering |
| Unequal quality | Evaluation misses subgroup | Customer segment | Disparate service quality | Segmented evaluation | Representative testing | Revise data or scope | Evaluation owner |
| Vendor data exposure | Provider terms or configuration | Customer | Privacy incident | Vendor audit | Approved settings and contracts | Incident response | Privacy owner |
```

### Human-control design

Use explicit levels:

| Level | System behavior | Human role |
|---|---|---|
| Assist | Find and summarize evidence | Agent decides and writes |
| Draft | Produce editable response | Agent reviews and sends |
| Recommend | Propose escalation or action | Authorized person decides |
| Execute with approval | Prepare exact tool action | Authorized person approves |
| Autonomous execution | Execute within policy | Human monitors and can override |

The first pilot stops at **Draft**.

### Approval design

An approval must show:

- Proposed action or response
- Evidence used
- Relevant policy
- Data affected
- Expected consequence
- Model and prompt version
- Expiration time
- Approver identity

A generic "approve AI" button is not meaningful control.

## Define product requirements

**`discovery/product-requirements.md`**

```markdown
# Product Requirements: Evidence-Backed Support Drafting Pilot

## User

English-language support agents handling billing and account questions.

## Problem

Agents spend substantial time finding current policy evidence and drafting repetitive answers.

## Outcome

Reduce median search and drafting time by at least 30% for eligible cases.

## Guardrails

- Policy-error rate must not exceed the current baseline.
- Reopen rate must not exceed the current baseline.
- Unauthorized documents must never appear.
- No response may be sent without agent approval.

## Inputs

- Ticket text
- Authorized account metadata
- Current approved knowledge sources

## Outputs

- Structured issue summary
- Retrieved evidence with source identifiers
- Editable response draft
- Abstention or escalation reason

## Allowed behavior

- Search approved sources
- Summarize evidence
- Draft a response
- Ask the agent to obtain missing information

## Prohibited behavior

- Send a response
- Issue a refund
- Modify an account
- Use unauthorized customer or employee data
- Hide missing or conflicting evidence

## Service targets

- Median end-to-end response under 8 seconds during the pilot
- 99% successful request handling during staffed pilot hours
- Per-case cost tracked and limited by policy

## Human control

The agent reviews, edits, and explicitly sends every response.

## Feedback

Record accept, edit, reject, abstain, escalation, and final ticket outcome.

## Exclusions

- Security incidents
- Legal threats
- High-value refunds
- Unsupported languages
- Cases without verified customer identity
```

### Functional and non-functional requirements

Functional requirements describe behavior:

- Retrieve approved evidence
- Draft a response
- Show citations
- Accept edits
- Record feedback

Non-functional requirements describe operating qualities:

- Latency
- Availability
- Security
- Privacy
- Auditability
- Cost
- Accessibility
- Maintainability

## Metrics

### Metric hierarchy

```text
Business outcome
└── Product behavior
    └── AI system quality
        └── Component and operational health
```

### Business metrics

- Cost per resolved case
- Median resolution time
- First-contact resolution
- Reopen rate
- Escalation rate
- Customer satisfaction

### Product metrics

- Agent adoption
- Draft acceptance
- Edit distance or edit effort
- Rejection rate
- Abstention rate
- Time saved
- Human-review time

### AI system metrics

- Answer correctness
- Policy compliance
- Groundedness
- Citation accuracy
- Completeness
- Unsupported-claim rate
- Escalation correctness

### Operational metrics

- Latency
- Availability
- Error rate
- Token usage
- Cost per request
- Retrieval failures
- Provider failures

### Guardrail metrics

Guardrails prevent optimization of one metric at the expense of another:

- Policy-error rate
- Reopen rate
- Privacy or access incidents
- High-risk under-escalation
- Agent workload
- Quality by customer segment

### Metric specification

Every metric needs:

- Definition
- Numerator and denominator
- Data source
- Owner
- Collection frequency
- Segment
- Baseline
- Target
- Alert or stop threshold

Example:

```text
Metric: Draft acceptance rate
Definition: Eligible AI drafts sent after zero or minor edits
Numerator: Accepted drafts
Denominator: Generated drafts presented to agents
Data source: Draft feedback table
Frequency: Daily during pilot
Segments: Case type, agent tenure, language
Purpose: Product usefulness
Not a quality guarantee: High acceptance can still reflect automation bias
```

## Return-on-investment analysis

### Benefits

Possible benefits:

- Labor time saved
- Avoided rework
- Reduced error cost
- Faster onboarding
- Higher support capacity
- Improved customer retention

Do not count the same benefit twice. If time saved is converted into capacity rather than staff
reduction, describe it as capacity.

### Costs

Include:

- Discovery and design
- Engineering
- Data preparation
- Integration
- Evaluation
- Model API or GPU
- Storage and network
- Security and privacy review
- Human review
- Monitoring
- Support
- Training and change management
- Vendor contracts
- Incident response

### Scenario model

Use:

- Conservative scenario
- Expected scenario
- Upside scenario
- Downside or failure scenario

Do not present a single point estimate as certainty.

### Example formulas

```text
Annual labor benefit =
monthly eligible cases
× adoption rate
× minutes saved
÷ 60
× loaded hourly cost
× 12

Annual error avoidance =
annual eligible cases
× (baseline error rate - expected error rate)
× average error cost

First-year net value =
annual benefit
- implementation cost
- annual operating cost

First-year ROI =
first-year net value
÷ first-year total cost
```

### Sensitivity analysis

The business case is usually most sensitive to:

- Eligible volume
- Actual adoption
- Minutes saved after review
- Human-oversight cost
- Model and retrieval cost
- Quality regressions
- Integration scope

Change each assumption and show how the conclusion moves.

## Build, buy, or hybrid

### Build

Advantages:

- Greater control
- Custom workflow and permissions
- Flexible evaluation
- Reduced provider lock-in at the application layer

Costs:

- Engineering and operations ownership
- Security responsibility
- Longer time to market

### Buy

Advantages:

- Faster initial deployment
- Vendor-supported features
- Lower initial engineering effort

Costs:

- Integration limits
- Vendor lock-in
- Data-policy constraints
- Less control over updates and evaluation

### Hybrid

Use hosted model and managed infrastructure while retaining:

- Application logic
- Permissions
- Retrieval
- Evaluation
- Prompt and model routing
- Observability
- Business workflow

The pilot selects hybrid.

### Vendor assessment

Evaluate:

- Required capability
- Data retention and training policy
- Regional processing
- Security attestations
- Identity and access integration
- Logging and audit
- Model versioning
- Rate limits and availability
- Pricing and cost predictability
- Contract and exit terms
- Portability

Do not select a vendor only from benchmark scores.

## Data contract

The discovery package uses three data contracts.

### Baseline metric record

| Field | Type | Rule |
|---|---|---|
| `segment` | string | Stable business-defined case segment |
| `monthly_cases` | integer | Non-negative and tied to a measurement period |
| `median_handle_minutes` | number | Non-negative; excludes or identifies queue time |
| `p90_handle_minutes` | number | Must be at least the median |
| `median_search_minutes` | number | Non-negative |
| `median_draft_minutes` | number | Non-negative |
| `reopen_rate` | number | Between zero and one |
| `escalation_rate` | number | Between zero and one |
| `policy_error_rate` | number | Between zero and one |
| `cost_per_case_usd` | number | Non-negative; calculation method documented |

### Use-case scenario record

The `UseCase` Pydantic model defines the machine-readable contract. Required groups are:

- Identity: name, user, outcome, solution type
- Value: volume, time, adoption, labor cost, error cost
- Cost: implementation, recurring operation, human oversight
- Risk: consequence, autonomy, data sensitivity, uncertainty, irreversibility
- Readiness: evidence, data, integration
- Control: human approval and non-AI alternative

### Valid record

The `response-drafting-scenario.yaml` example is valid because:

- All rates are between zero and one.
- Expected error is no higher than the baseline in the stated expected scenario.
- Scores remain within one to five.
- A non-AI alternative is present.
- Human control is explicit.

### Invalid record

```yaml
name: "Draft"
user: ""
business_outcome: "Use AI"
solution_type: "magic"
monthly_volume: -1
adoption_rate: 1.5
baseline_error_rate: 0.05
expected_error_rate: 0.20
human_approval_required: false
non_ai_alternative: ""
```

The record fails identity, enum, range, scenario, and alternative requirements.

### Boundary records

Test:

- Zero eligible monthly volume
- Zero minutes saved
- Zero implementation cost
- Expected error equal to baseline
- Risk and readiness scores at one and five
- First-year net value exactly zero
- Negative monthly net after launch

### Provenance

Every input assumption must include, in its human-readable supporting artifact:

- Source
- Measurement period
- Owner
- Confidence
- Scenario
- Last review date

The YAML file contains calculation inputs; it does not replace the evidence supporting them.

### Privacy

Use aggregated or synthetic data. If record-level data is required:

- Limit fields to the discovery purpose.
- Obtain data-owner approval.
- Use controlled storage.
- Remove direct identifiers where possible.
- Define retention and deletion.
- Do not include raw customer text in the Git repository.

## Build-buy analysis

**`discovery/build-buy-analysis.md`**

```markdown
# Build, Buy, or Hybrid Decision

## Decision

Use a hybrid approach for the pilot.

## Build internally

- Ticket-system integration
- Identity and permissions
- Document ingestion
- Retrieval and citations
- Prompt and workflow logic
- Evaluation
- Feedback
- Audit and monitoring

## Buy or consume as managed service

- Foundation-model inference
- Managed PostgreSQL and object storage
- Cloud monitoring

## Revisit self-hosting when

- Volume makes managed inference materially more expensive
- Data constraints require private hosting
- Model customization becomes strategically important
- The team can operate GPU infrastructure reliably
```

## Architecture options

### Option A — Better process and templates

```text
Agent
→ improved search and approved templates
→ manual response
```

Use as the non-AI baseline.

### Option B — Direct LLM drafting

```text
Ticket
→ LLM
→ draft
→ agent
```

Rejected because current private policy evidence and citations are missing.

### Option C — RAG-assisted drafting

```text
Authenticated agent
→ authorized ticket and customer context
→ permission-aware retrieval
→ evidence and citations
→ LLM draft
→ schema and policy validation
→ agent review
→ send
→ feedback and outcome
```

Selected for the pilot.

### Option D — Autonomous support agent

```text
Customer
→ agent loop
→ search and tools
→ send and execute actions
```

Rejected for the first pilot because controls, evaluation, and operational maturity are
insufficient.

### Architecture decision record

**`discovery/architecture-decision.md`**

```markdown
# ADR: Select RAG-Assisted Human-Approved Drafting

## Status

Proposed for pilot.

## Context

Support agents spend measurable time finding current policies and drafting routine answers.
Policies change frequently and responses require evidence.

## Decision

Use permission-aware hybrid retrieval and a hosted language model to create an editable draft.
An authenticated agent must approve every response.

## Rejected alternatives

- Direct LLM drafting: lacks current private evidence and citations.
- Fine-tuning as knowledge storage: policy changes too frequently.
- Autonomous sending: consequence and evaluation maturity are unacceptable.
- Process-only change: retained as the baseline but expected to provide less drafting support.

## Consequences

- Requires document governance and retrieval evaluation.
- Adds model-provider cost and privacy review.
- Retains human workload for review.
- Provides a reversible first deployment.

## Revisit when

- Evaluation demonstrates stable quality.
- Human review data is available.
- Incident and rollback procedures have been tested.
```

## Evaluation plan before implementation

Discovery must define evaluation before the team sees prototype results.

**`discovery/evaluation-plan.md`**

```markdown
# Evaluation Plan

## Offline dataset

- Representative eligible cases
- Difficult and ambiguous cases
- Policy-conflict cases
- Missing-information cases
- Security and out-of-scope cases
- Segments by issue type and agent experience

## Baselines

- Current human workflow
- Improved search and templates
- RAG-assisted draft

## Quality measures

- Policy correctness
- Citation correctness
- Completeness
- Unsupported claims
- Appropriate abstention
- Appropriate escalation

## Product measures

- Time to approved response
- Draft acceptance and edit effort
- Agent satisfaction
- Reopen rate

## Safety and security

- Unauthorized-document access
- Prompt injection
- Sensitive-data disclosure
- Incorrect non-escalation

## Release gates

- No critical access-control failure
- Policy-error rate no worse than baseline
- Reopen rate no worse than baseline
- Measurable reduction in search and drafting time
- Agent review remains mandatory
```

## Pilot design

### Pilot scope

- English-language billing and account questions
- Volunteer or selected trained agents
- Staffed business hours
- Human approval for every output
- No autonomous action
- Limited model and token budget
- Existing workflow remains available

### Pilot stages

```text
Offline evaluation
→ internal shadow mode
→ limited agent pilot
→ expanded pilot
→ production decision
```

### Shadow mode

The system generates a result but does not show it to the agent or affect the customer. Compare:

- Proposed category
- Evidence
- Draft
- Escalation decision

Shadow mode supports evaluation without influencing the workflow.

### Limited agent pilot

Agents can:

- View evidence
- Edit draft
- Reject draft
- Escalate
- Report an issue

The product records:

- Time
- Edits
- acceptance or rejection
- Evidence used
- Final outcome

### Stop conditions

Stop or pause when:

- Unauthorized content is exposed.
- A critical security incident occurs.
- Policy-error rate exceeds the threshold.
- High-risk cases are not escalated.
- Review workload exceeds the expected benefit.
- Cost per successful case exceeds the approved limit.
- Users cannot understand or contest output.

### Pilot plan

**`discovery/pilot-plan.md`**

```markdown
# Pilot Plan

## Duration

Four weeks after offline and shadow evaluation pass.

## Participants

- 20 trained support agents
- 2 supervisors
- 2 quality reviewers
- Product, engineering, evaluation, security, and privacy owners

## Eligible cases

- English billing questions
- English account questions
- Verified identity
- No security or legal escalation

## Controls

- Human approval
- Source display
- Abstention
- Rate and spending limits
- Audit logs
- Daily quality sample
- Immediate disable switch

## Decision points

- End of offline evaluation
- End of shadow week
- End of limited pilot
- Production recommendation
```

## Go, revise, or stop decision

**`discovery/go-no-go.md`**

```markdown
# Go, Revise, or Stop Criteria

## Go to controlled pilot

- Baseline data is reliable.
- Eligible workflow is narrow and documented.
- Required data access is approved.
- Offline quality meets thresholds.
- Security and privacy reviews pass.
- Human approval is implemented.
- Cost is within the pilot budget.

## Revise

- Value is plausible but data or integration readiness is weak.
- Quality is close to target but failure slices are unclear.
- Human review takes too long.
- Architecture requires narrower scope.

## Stop

- Non-AI process change provides equivalent value at lower risk.
- Required data use is not acceptable.
- High-consequence errors cannot be detected before impact.
- The project has no accountable operator.
- First-year value remains negative under credible scenarios.
- The system conflicts with organizational or legal requirements.
```

## Minimal implementation

The minimum implementation for this lesson is not an AI prototype. It is a validated decision
package and reproducible scenario calculator.

### Add project dependency

The repository from Lesson 01 already uses Pydantic. No new runtime dependency is required.

### Add package files

**`src/ai_industry_labs/discovery/__init__.py`**

```python
"""Tools for reproducible Applied AI discovery analysis."""
```

Use the `models.py` and `scoring.py` implementations shown earlier.

### Add a CLI

**`src/ai_industry_labs/discovery/cli.py`**

```python
import argparse
import json
from pathlib import Path

import yaml

from ai_industry_labs.discovery.models import UseCase
from ai_industry_labs.discovery.scoring import (
    calculate_business_case,
    triage_recommendation,
)


def load_use_case(path: Path) -> UseCase:
    with path.open(encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return UseCase.model_validate(data)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate one Applied AI discovery scenario."
    )
    parser.add_argument("use_case", type=Path)
    args = parser.parse_args()

    use_case = load_use_case(args.use_case)
    result = calculate_business_case(use_case)
    recommendation = triage_recommendation(
        result,
        human_approval_required=use_case.human_approval_required,
    )

    print(
        json.dumps(
            {
                "use_case": use_case.name,
                "annual_total_benefit": round(result.annual_total_benefit, 2),
                "first_year_total_cost": round(result.first_year_total_cost, 2),
                "first_year_net_value": round(result.first_year_net_value, 2),
                "first_year_roi": (
                    round(result.first_year_roi, 4)
                    if result.first_year_roi is not None
                    else None
                ),
                "payback_months": (
                    round(result.payback_months, 2)
                    if result.payback_months is not None
                    else None
                ),
                "risk_score": result.risk_score,
                "readiness_score": result.readiness_score,
                "recommendation": recommendation,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The CLI uses PyYAML. Add it:

```powershell
uv add "pyyaml>=6,<7"
```

### Example scenario

**`discovery/response-drafting-scenario.yaml`**

```yaml
name: "Evidence-backed response drafting"
user: "Support agent"
business_outcome: "Reduce search and drafting time without increasing policy errors"
solution_type: "hybrid"
monthly_volume: 18000
minutes_saved_per_case: 3.5
adoption_rate: 0.60
loaded_labor_cost_per_hour: 34.0
baseline_error_rate: 0.08
expected_error_rate: 0.06
error_cost: 18.0
implementation_cost: 120000.0
monthly_recurring_cost: 8000.0
monthly_oversight_cost: 4000.0
consequence: 3
autonomy: 1
data_sensitivity: 4
uncertainty: 3
irreversibility: 2
evidence_quality: 4
data_readiness: 4
integration_readiness: 4
human_approval_required: true
non_ai_alternative: "Improve search, policy templates, and agent training"
```

Run:

```powershell
uv run python -m ai_industry_labs.discovery.cli discovery/response-drafting-scenario.yaml
```

The output is an input-dependent scenario, not a forecast or promise.

## Production implementation

### Version assumptions

Every value model must record:

- Source
- Date
- Owner
- Confidence
- Scenario
- Review status

### Require independent review

At least one reviewer should not be the proposal author. Review:

- Baseline definitions
- Data access assumptions
- Benefit calculations
- Risk controls
- Excluded users
- Stop criteria

### Maintain a decision log

Record:

- Decision
- Date
- Participants
- Evidence
- Alternatives
- Dissent
- Conditions for revisiting

### Protect discovery data

- Use access-controlled repositories for sensitive material.
- Remove customer content from diagrams and examples.
- Aggregate operational metrics where possible.
- Do not copy production data into personal spreadsheets.
- Apply retention and deletion policy.

### Assign owners

A proposal without owners is incomplete.

| Responsibility | Required owner |
|---|---|
| Business outcome | Product or operations |
| Workflow | Operations |
| Data | Data owner |
| Model and application | Engineering |
| Evaluation | Evaluation or QA |
| Security | Security |
| Privacy or legal | Appropriate control owner |
| Production operation | Service owner |
| Budget | Business sponsor |

## Testing

### Software tests

Test:

- Use-case schema validation
- Invalid rates and scores
- ROI calculations
- Zero-cost and zero-benefit cases
- Low-readiness recommendation
- High-risk autonomous recommendation
- YAML loading errors

### Artifact completeness tests

Create a simple review checklist:

- Stakeholders identified
- Current workflow documented
- Baseline source recorded
- Non-AI alternative present
- Prohibited behavior defined
- Metrics and guardrails defined
- Human-control point defined
- Risk owner assigned
- Pilot and stop criteria defined

### Consistency tests

Check:

- Product target matches ROI assumptions.
- Eligible volume matches baseline segments.
- Architecture supports prohibited behaviors.
- Evaluation cases cover stated risks.
- Pilot excludes out-of-scope users and cases.

### Adversarial review

Ask a reviewer to argue:

- The project should not be built.
- The benefit assumptions are wrong.
- The selected metric can be gamed.
- Human review is ineffective.
- A simpler solution is better.
- The pilot excludes an important affected group.

The proposal should improve after this review.

## Evaluation

This lesson evaluates discovery quality, not model quality.

| Dimension | Evidence | Acceptance criterion | Result |
|---|---|---|---|
| Problem reality | Workflow observations and baseline | Bottleneck supported by data | |
| User coverage | Stakeholder map | Users, operators, and affected people represented | |
| Baseline quality | Metric definitions and source | Sample, period, and limitations documented | |
| AI suitability | Solution comparison | Non-AI and simpler alternatives evaluated | |
| Product clarity | Requirements | Inputs, outputs, allowed, prohibited, and escalation behavior explicit | |
| Risk control | Risk register | Owners, controls, detection, and response defined | |
| Human control | Workflow | Review or approval authority explicit | |
| Economics | Scenario model | Costs and assumptions reviewable | |
| Evaluation readiness | Evaluation plan | Quality, business, safety, and operational metrics defined | |
| Pilot quality | Pilot plan | Narrow, reversible, monitored, and stoppable | |
| Decision quality | ADR and go/no-go | Rejected alternatives and revisit conditions recorded | |

### Business acceptance

A discovery package is successful even when it recommends:

- Process improvement instead of AI
- More data collection
- A smaller pilot
- Stronger human control
- Delaying or stopping the project

The purpose is decision quality, not project approval.

## Failure modes and debugging

| Symptom | Likely causes | Diagnostic evidence | Corrective action | Prevention |
|---|---|---|---|---|
| Proposal begins with a model | Technology-first planning | No measured workflow problem | Return to user and workflow interviews | Require problem statement before architecture |
| ROI appears extremely high | Benefits double-counted or oversight omitted | Formula review | Separate capacity, labor, and error benefits | Independent finance review |
| Baseline has one average | Variation and queue time hidden | Raw distribution differs | Use median, percentiles, and segments | Metric specification |
| Users say they want full automation | Incentive or framing bias | Exceptions reveal risk | Observe real cases and map consequences | Ask about failures and approvals |
| Pilot cannot define success | Vague business goal | No target or guardrail | Rewrite measurable problem | Require go/no-go criteria |
| "Human in loop" adds no safety | Reviewer lacks evidence, time, or authority | High rubber-stamp rate | Show sources and exact action; train reviewers | Measure review quality |
| AI improves speed but reopens rise | Local metric optimization | Outcome data | Add reopen guardrail and root-cause analysis | Metric hierarchy |
| Search problem is called an LLM problem | Documentation is fragmented | Search-time evidence | Fix content governance and retrieval first | Root-cause analysis |
| Vendor selected from demo | Operational needs ignored | Missing security and cost analysis | Run vendor assessment | Decision record |
| Use case needs unavailable data | Feasibility assumption | Data owner rejects access | Redesign or stop | Data inventory during discovery |
| Low adoption | Workflow friction or distrust | Agent feedback and usage | Improve UX, evidence, training, or scope | Co-design and pilot |
| High-risk cases enter pilot | Eligibility rules incomplete | Incident or audit | Add deterministic routing and tests | Explicit exclusions |
| Scoring tool decides automatically | False precision | Stakeholders defer to score | Separate score from decision authority | Document model limitation |
| Stakeholders disagree on correctness | Undefined policy | Reviewer disagreement | Resolve domain policy before modelling | Rubric workshop |
| Pilot result does not generalize | Sample too narrow | Segment performance differs | Expand representative evaluation carefully | Sampling plan |
| Regulatory review arrives late | Constraint discovery omitted | Launch blocked | Include legal and domain owners early | Stakeholder map |

## Security, privacy, and governance

### Threats during discovery

- Sensitive customer examples copied into documents
- Production data placed in uncontrolled spreadsheets
- Vendor receives data before approval
- Architecture assumes model output grants permission
- High-risk use is disguised as a low-risk pilot
- Risk owner is not assigned

### Controls

- Use synthetic examples until access is approved.
- Classify discovery artifacts.
- Limit repository access.
- Redact personal information.
- Record data purpose and retention.
- Enforce authorization in deterministic systems.
- Require security and privacy review before external data transfer.
- Define incident and disable procedures before pilot.

### NIST alignment

This lesson primarily supports:

- **Map:** purpose, context, users, impacts, alternatives, human roles, requirements, and risk
- **Measure planning:** metrics, limits, test procedures, affected groups, and documentation
- **Govern preparation:** owners, decision rights, policies, and review
- **Manage preparation:** prioritized controls, monitoring, and response

Do not claim that completing this lesson alone constitutes AI RMF compliance.

### Legal and regulatory constraints

Discovery should identify:

- Jurisdictions
- Sector rules
- Privacy requirements
- Contract requirements
- Employment or consumer-impact concerns
- Accessibility obligations
- Recordkeeping

The engineering team should not invent legal conclusions. Route questions to authorized legal
and compliance owners.

## Performance and cost

### Discovery cost

Track:

- Stakeholder hours
- Data-analysis hours
- Engineering spike hours
- Security and privacy review
- Vendor evaluation
- Prototype and evaluation cost

### Model operating cost

Estimate:

- Requests
- Input and output volume
- Retrieval
- Model inference
- Storage
- Network
- Monitoring
- Human review

### Latency budget

For the pilot:

```text
Request validation       0.1 s
Authorized retrieval     1.5 s
Reranking                0.5 s
Model generation         5.0 s
Output validation        0.3 s
Network and margin       0.6 s
--------------------------------
Target median            8.0 s
```

These are design allocations, not measured results.

### Capacity assumptions

Record:

- Eligible monthly cases
- Peak requests per minute
- Average input and output size
- Adoption ramp
- Human-review capacity
- Vendor rate limits

### Cost guardrail

Define:

```text
Cost per successful approved draft =
total system and review cost
÷ drafts accepted and used successfully
```

Cost per API request is insufficient because failed or rejected requests provide no business
value.

## Deployment and operational path

The discovery package itself should follow a controlled approval workflow:

```text
Draft
→ domain review
→ data review
→ evaluation review
→ security and privacy review
→ finance review
→ pilot approval
```

### Versioning

- Tag approved discovery package versions.
- Record assumptions and data dates.
- Link implementation work to the approved version.
- Reopen discovery when scope, users, data, or actions change.

### Change triggers

Reassess when:

- The model or provider changes materially.
- A new user population is added.
- Autonomous action is introduced.
- New sensitive data is used.
- Policy or regulation changes.
- Metrics reveal unexpected impacts.

### Rollback

The pilot must support:

- Feature disable
- Return to the existing workflow
- Reversal of reversible actions
- Preservation of audit records
- Notification of affected teams

## Observability and operations plan

Discovery defines what later production monitoring must include.

### Logs

- Request and workflow identifiers
- User and tenant identity
- Model, prompt, and retrieval versions
- Evidence identifiers
- Human approval
- Escalation
- Error category

Do not log unnecessary customer content.

### Metrics

- Volume and eligibility
- Adoption
- Acceptance and edit effort
- Abstention and escalation
- Quality and guardrails
- Latency
- Availability
- Cost
- Security events

### Feedback

Capture:

- Helpful or unhelpful
- Accepted, edited, or rejected
- Incorrect evidence
- Missing policy
- Unsafe or inappropriate behavior
- Final case outcome

### Ownership

Every dashboard and alert must have an owner and response procedure.

## Practical assignment

### Scenario

Choose one support workflow:

- Billing question
- Technical troubleshooting
- Account closure
- Quality review
- Voice triage

Produce a complete Applied AI discovery package.

### Requirements

- Interview at least three simulated or real authorized stakeholders.
- Map the current workflow and failure paths.
- Define baseline metrics and limitations.
- Create at least five candidate interventions.
- Include at least two non-AI alternatives.
- Reject at least one AI use case with a documented reason.
- Select one narrow pilot.
- Define allowed, prohibited, abstention, and escalation behavior.
- Create a risk register.
- Create conservative, expected, upside, and downside cost scenarios.
- Write product requirements.
- Write an architecture decision.
- Define offline, shadow, and limited-pilot stages.
- Define go, revise, and stop criteria.

### Required artifacts

- Stakeholder map
- Interview notes with sensitive data removed
- Current-state workflow
- Baseline dataset or measurement plan
- Root-cause analysis
- Use-case register
- Solution-selection matrix
- Risk register
- Human-control design
- Product requirements
- Metric specification
- Cost model
- Build-buy analysis
- Architecture decision
- Evaluation plan
- Pilot plan
- Go/no-go document
- Executive summary

### Acceptance criteria

- The problem is supported by workflow evidence.
- AI is not assumed to be the only solution.
- The selected pilot is narrow and reversible.
- High-consequence actions retain appropriate human authority.
- Metrics connect model behavior to business outcomes.
- Cost assumptions are reviewable.
- Security, privacy, and domain constraints are identified.
- Rejected ideas are documented.
- The decision can be defended without showing a model demo.

### Stretch goals

- Conduct a workshop with operations and security.
- Add subgroup and accessibility considerations.
- Create a vendor request-for-information checklist.
- Build a small dashboard from synthetic baseline data.
- Run a pre-mortem: imagine the pilot failed and identify why.

## Interview preparation

### Concept questions

**When should AI not be used?**

A strong answer discusses lack of a real measured problem, deterministic alternatives, poor or
unlawful data, high-consequence undetectable errors, weak ownership, poor economics, and lack of
user recourse.

**What is a useful baseline?**

A strong answer identifies the current process or simplest alternative, defines the metric,
sample, segments, time period, limitations, and connection to the desired business outcome.

**What is the difference between decision support and automation?**

A strong answer describes who retains authority, whether an action occurs automatically, and
how review, approval, override, and accountability work.

**Why is high model accuracy insufficient?**

A strong answer connects operational context, error costs, subgroup performance, workflow
integration, security, latency, adoption, and business outcomes.

### Case questions

**A manager asks for an AI agent to issue refunds automatically. How do you respond?**

Clarify:

- Refund policy
- Value and volume
- Authorization
- Error cost
- Reversibility
- Fraud risk
- Data access
- Existing approval workflow
- Evidence and evaluation

Propose a staged path:

```text
Policy retrieval
→ refund recommendation
→ exact proposed action
→ authorized approval
→ limited execution
→ evidence-based automation decision
```

**Agents spend time searching policies. Should you fine-tune a model?**

Usually not first. Evaluate content governance, search, freshness, access control, hybrid
retrieval, and citations. Fine-tuning is not an appropriate store for frequently changing
policy facts.

### Calculation question

**How do you estimate ROI?**

Explain:

- Eligible volume
- Adoption
- Time or error benefit
- Loaded labor cost
- Implementation cost
- Recurring infrastructure
- Human review
- Support and change management
- Conservative and downside scenarios

Avoid claiming that saved minutes automatically become cash savings.

### System-design question

**Design a first pilot for AI-assisted support.**

A strong answer includes:

- Narrow eligible cases
- Current baseline
- Non-AI baseline
- RAG and citations
- Human approval
- Deterministic authorization
- Evaluation data
- Shadow mode
- Quality and guardrail metrics
- Feedback
- Cost limits
- Stop and rollback controls

### Behavioral question

**Tell me about a time you recommended not building a requested AI feature.**

Use:

- Context
- Evidence
- Stakeholder concern
- Alternative
- Decision
- Outcome
- What changed afterward

The goal is to show judgment rather than resistance to innovation.

## Production-readiness checklist

- [ ] Users, operators, owners, and affected people are identified.
- [ ] Current workflow and exception paths are documented.
- [ ] Baseline definitions, sample, period, and limitations are recorded.
- [ ] Root causes are separated from symptoms.
- [ ] The problem statement defines inputs, outputs, and context.
- [ ] Allowed and prohibited behavior are explicit.
- [ ] Abstention and escalation behavior are explicit.
- [ ] At least one non-AI alternative is evaluated.
- [ ] Deterministic controls are separated from model behavior.
- [ ] Candidate use cases include value, feasibility, and risk.
- [ ] A high-risk use case is rejected or narrowed where appropriate.
- [ ] Human review and approval authority are explicit.
- [ ] Consequential actions remain appropriately controlled.
- [ ] Business, product, model, operational, and guardrail metrics are defined.
- [ ] Metric sources and owners are assigned.
- [ ] Cost model includes implementation, operation, and human oversight.
- [ ] Conservative and downside scenarios exist.
- [ ] Build, buy, and hybrid options are compared.
- [ ] Vendor data and exit conditions are reviewed.
- [ ] Data access, privacy, retention, and deletion are identified.
- [ ] Security and misuse risks have controls and owners.
- [ ] Evaluation is designed before implementation.
- [ ] Pilot is narrow, reversible, monitored, and stoppable.
- [ ] Shadow mode is used where appropriate.
- [ ] Go, revise, and stop criteria are approved.
- [ ] Rollback to the existing workflow is possible.
- [ ] Discovery assumptions are versioned.
- [ ] Revisit triggers are defined.
- [ ] An independent reviewer challenged the proposal.
- [ ] Executive and technical summaries agree.

## Lesson summary

Applied AI problem discovery determines whether an AI project deserves to exist and how it can
be introduced safely.

You learned to:

- Start from users, workflow, and outcomes
- Measure the current process
- Identify root causes
- Compare AI with simpler alternatives
- Select the smallest sufficient solution
- Separate model capability from business authority
- Define human-control boundaries
- Create value, risk, and readiness evidence
- Design evaluation before implementation
- Build a reversible pilot with stop criteria

The selected first use case is:

> Permission-aware, evidence-backed response drafting for eligible support cases, with mandatory
> agent approval and no autonomous financial or account action.

This lesson also rejected premature autonomous refund execution. Rejecting or narrowing a use
case is a successful discovery outcome when evidence and controls are insufficient.

The next lesson, **Foundation Models and LLM Fundamentals**, will explain how language models
behave and how to select models for the pilot without confusing model capability with complete
system quality.

## Official references

- NIST AI Risk Management Framework Playbook:
  <https://airc.nist.gov/airmf-resources/playbook/>
- NIST AI RMF Playbook — Map:
  <https://airc.nist.gov/airmf-resources/playbook/map/>
- NIST AI RMF Playbook — Measure:
  <https://airc.nist.gov/airmf-resources/playbook/measure/>
- NIST AI Risk Management Framework:
  <https://www.nist.gov/itl/ai-risk-management-framework>
- NIST Generative AI Profile:
  <https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence>
