# Applied AI Problem Discovery

## Lesson brief

| Item | Detail |
|---|---|
| What you learn | How to discover, frame, score, and govern Applied AI opportunities before anyone builds a model. |
| What you build | A reproducible discovery package for Northstar Support: stakeholder map, workflow map, baseline, use-case register, risk register, ROI scenario, build/buy ADR, PRD, pilot plan, and a small validation CLI. |
| Why it matters | Most failed AI projects start with a model idea before proving a workflow need, measurable value, acceptable risk, and operational ownership. |
| Primary roles | Applied AI Engineer, Forward-Deployed AI Engineer, AI Product Manager, AI Solutions Architect. |
| Prerequisites | Lessons 01-06; Python basics; Pydantic; pytest; basic product, API, database, and deployment vocabulary. |
| Tools | Process diagrams, stakeholder interviews, PRDs, ADRs, risk registers, ROI spreadsheets, Python, Pydantic, PyYAML, pytest. |
| Estimated time | 8-11 hours study, 8-14 hours implementation. |
| Final deliverable | A tested Applied AI discovery package that recommends one controlled pilot and documents rejected alternatives. |
| Carries forward | Lesson 08 assumes this lesson has selected a support-drafting pilot with measurable value, human approval, and clear non-goals. |
| Verified | Local curriculum scope and code compatibility verified June 28, 2026. No provider-specific API behavior is used in this lesson. |

This is a discovery and system-design lesson, not a model-building lesson. The core skill is deciding whether AI should be used, where it should be used, and what must be true before implementation starts.

## Business target

Northstar Support receives a leadership request: "Use AI to improve customer support productivity." The request is too broad. The team must convert it into a narrow, measurable, low-enough-risk pilot.

| Area | Decision |
|---|---|
| Current workflow | Support agents search policy documents, inspect order data, write replies, and wait for team leads on high-risk cases. Discovery evidence is scattered across interviews, tickets, spreadsheets, and dashboards. |
| Target workflow | The team produces a discovery package that identifies the bottleneck, compares AI and non-AI options, recommends one pilot, defines human-control boundaries, and states go/no-go criteria before model work begins. |
| Inputs | Stakeholder interviews, workflow steps, ticket volumes, handling-time samples, quality-review samples, error costs, data availability, legal/security constraints, candidate interventions. |
| Outputs | Current-state workflow, baseline, use-case register, rejected use cases, risk register, PRD, ROI scenario, build/buy ADR, pilot plan, operational checklist. |
| Constraints | No real customer PII in lesson artifacts; no autonomous customer-facing actions; no AI recommendation without a non-AI alternative; no ROI claim without baseline evidence. |
| Risk level | Medium-to-high. Discovery mistakes can waste budget, automate the wrong work, create unsafe incentives, or hide legal and customer-impact risks. |
| Acceptance metrics | AI use tied to a measured workflow bottleneck; high-impact actions retain human approval; non-AI fallback exists; rejected use cases are documented; success metrics and stop conditions are explicit. |

Non-goals:

- This lesson does not build an LLM, RAG system, agent, or provider integration.
- This lesson does not choose a final model vendor.
- This lesson does not automate refunds, credits, account changes, or customer-facing commitments.
- This lesson does not treat a scoring spreadsheet as an automatic approval decision.

## Starting checkpoint

You should already know:

- How a Python project is structured and tested.
- How APIs, databases, logs, and deployment boundaries appear in production systems.
- Why user workflows and data contracts matter before implementation.
- Why high-consequence decisions need explicit human control.

Required setup:

- Python 3.11 or newer.
- A virtual environment.
- No paid model account.
- No real customer data.

Answer before continuing:

- What is the difference between an executive request and a validated business problem?
- What current-state baseline would you need before claiming productivity improvement?
- Which support actions must require human approval?
- What non-AI solution might solve the same support bottleneck?
- What would make this project a "stop" even if the demo looked impressive?

## System map and build roadmap

### Source compliance contract

| Source requirement | Where handled |
|---|---|
| User and stakeholder discovery | Modules 1-2; stakeholder map; interview guide. |
| Workflow mapping | Modules 1-3; workflow-step schema and current-state map. |
| Pain-point and bottleneck analysis | Modules 2-3; baseline and failure-path evidence. |
| Current-state baseline | Module 3; baseline metrics and measurement rules. |
| Automation versus decision support | Modules 4-5; solution-selection and human-control design. |
| Human-in-the-loop boundaries | Module 5; control modes and approval design. |
| AI suitability | Module 4; suitability filter and rejected alternatives. |
| Build versus buy | Module 7; ADR and decision memo. |
| Risk classification | Module 5; risk register and scoring dimensions. |
| Product requirements | Module 7; PRD template. |
| Success and adoption metrics | Module 6; metric hierarchy. |
| Cost and expected return | Module 6; ROI scenario model. |
| Domain and regulatory constraints | Modules 5, 7, security/governance section. |
| Required tools | System roadmap, modules, implementation, assignment. |
| Practical deliverables | Module 7, practical assignment, production checklist. |

### Concept map

```text
executive request
  -> stakeholder discovery
  -> current workflow
  -> baseline and bottleneck
  -> candidate interventions
  -> AI suitability test
  -> risk and human-control design
  -> metrics and ROI scenario
  -> build/buy/partner decision
  -> PRD and pilot plan
  -> go / revise / stop decision
```

Decision rule:

```text
Do not ask "Can we use AI here?"
Ask "Which workflow outcome needs improvement, what evidence proves it, and which intervention is safest and most valuable?"
```

### Project architecture

```text
discovery YAML package
  -> Pydantic validation
  -> baseline and use-case scoring
  -> risk/readiness classification
  -> artifact completeness checks
  -> CLI JSON report
  -> PRD / ADR / pilot plan
```

The implementation is intentionally not an AI prototype. It is a reproducible decision package. That is the correct build artifact for discovery.

### Trust boundaries

| Boundary | Rule |
|---|---|
| Stakeholder claims | Treat as hypotheses until supported by workflow evidence. |
| Baseline data | Record source, measurement window, and owner. Do not invent ROI from weak data. |
| Customer data | Use synthetic or aggregated examples in discovery artifacts. |
| AI recommendation | Keep scoring advisory. Business and risk owners make decisions. |
| Human-control design | Authorization and approval are product controls, not model preferences. |
| Vendor information | Treat claims as inputs to due diligence, not proof of fit. |

### State ownership

| State | Owner |
|---|---|
| Workflow map | Product owner with support operations review. |
| Baseline metrics | Operations analytics / finance. |
| Risk register | Product, security, legal, support operations. |
| Use-case register | Applied AI team. |
| PRD and pilot plan | Product owner. |
| Go/no-go decision | Accountable business owner and risk owner. |

### Failure boundaries

| Failure | Boundary |
|---|---|
| Weak baseline | Pause ROI claims; collect better evidence. |
| High-risk automation request | Redesign as decision support or reject. |
| Data not available or not permitted | Redesign workflow or choose non-AI path. |
| Positive ROI but low readiness | Research/data cleanup before pilot. |
| Good demo but no adoption path | Stop or redesign with users. |

### Tool choices

| Capability | Selected tool | Why selected | Alternative / switch point |
|---|---|---|---|
| Artifact schemas | Pydantic | Typed, testable discovery records. | JSON Schema for language-neutral contracts. |
| Scenario input | YAML | Easy for product and engineering review. | Spreadsheet for finance-facing scenario work. |
| Scoring and validation | Python + pytest | Reproducible, auditable, CI-friendly. | Notebook only for exploration, not source of truth. |
| Workflow map | Markdown table / diagram | Reviewable in PRs and documents. | Miro/Lucidchart for workshops. |
| PRD / ADR / risk register | Markdown templates | Versioned with the project. | Product-management tools after adoption. |

### Project structure

```text
applied-ai-discovery/
├── pyproject.toml
├── discovery/
│   └── response-drafting-package.yaml
├── ai_discovery/
│   ├── __init__.py
│   ├── schemas.py
│   ├── scoring.py
│   ├── artifacts.py
│   └── cli.py
└── tests/
    ├── test_schemas.py
    ├── test_scoring.py
    ├── test_artifacts.py
    └── test_cli.py
```

### Environment setup

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "applied-ai-discovery"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "pydantic>=2.7,<3.0",
  "pyyaml>=6,<7"
]

[project.optional-dependencies]
dev = ["pytest>=8.0,<10.0"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Run:

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
pytest
python -m ai_discovery.cli discovery/response-drafting-package.yaml
```

### Data/API contract

The discovery package is a local YAML contract with these record groups:

- `stakeholders`: who uses, owns, reviews, or funds the workflow.
- `workflow_steps`: current work, systems, time, volume, outputs, failures.
- `baselines`: measured current-state facts.
- `use_cases`: candidate interventions and economic assumptions.
- `risks`: failure modes, controls, owners, and response.
- `selected_use_case`: the proposed pilot.
- `rejected_use_cases`: documented alternatives.
- `success_metrics`: how the pilot will be judged.
- `non_ai_fallback`: how the workflow works if AI is unavailable or rejected.
- `pilot_scope`: who, where, and when the pilot runs.

Privacy rule: discovery examples must be synthetic, aggregated, or approved for internal training use. Do not paste real support tickets into lesson artifacts.

### Baseline

The baseline is the current workflow measured before AI. It must include:

- volume;
- handling time;
- error or rework rate;
- escalation rate;
- customer-impact measure;
- cost or capacity estimate;
- measurement window and source.

The baseline proves what currently happens. It does not prove that AI will improve it.

### Build milestones

| Module | Type | Concept focus | Implementation artifact | Tests |
|---|---|---|---|---|
| 1 | Concept-build | Request versus problem | Schemas for stakeholders/workflows/use cases | Schema tests |
| 2 | Hybrid | Stakeholders and workflow map | Discovery package sections | Artifact tests |
| 3 | Hybrid | Baseline and bottlenecks | Baseline fields and evidence rules | Schema tests |
| 4 | Hybrid | Solution options and AI suitability | Solution-type and suitability logic | Scoring tests |
| 5 | Hybrid | Risk and human control | Risk dimensions and control modes | Scoring/artifact tests |
| 6 | Hybrid | ROI and metrics | Business-case calculator | Scoring tests |
| 7 | Implementation | PRD, ADR, pilot package | Artifact validator | Artifact tests |
| 8 | Implementation | CLI and operating path | CLI report | CLI tests |

### Implementation assembly checklist

Create these files:

- `pyproject.toml`
- `ai_discovery/__init__.py`
- `ai_discovery/schemas.py`
- `ai_discovery/scoring.py`
- `ai_discovery/artifacts.py`
- `ai_discovery/cli.py`
- `discovery/response-drafting-package.yaml`
- tests under `tests/`

After each implementation module, run:

```bash
pytest
```

Final verification:

```bash
python -m ai_discovery.cli discovery/response-drafting-package.yaml
```

Expected final artifact: a JSON report containing the selected use case, value scenario, risk/readiness scores, recommendation, and artifact completeness findings.

## Concept-build module 1: From executive request to testable business problem

### Core question

How do you turn "we need AI" into a measurable workflow problem?

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Executive request | The initial ask from leadership. It is a starting signal, not a validated problem. | "Use AI to reduce support cost." |
| Business outcome | The measurable result the organization wants. It keeps the project tied to value. | "Reduce average handle time by 12% without increasing refund-policy errors." |
| User task | The work a person performs inside the workflow. AI should support a task, not an abstract department. | "Find the correct refund policy and draft a reply." |
| Workflow | The sequence of steps, systems, people, and decisions that produces an outcome. | Ticket intake -> policy lookup -> order check -> draft -> review -> reply. |
| Bottleneck | The slow, expensive, or error-prone part of the workflow. It identifies where intervention may help. | Agents spend six minutes searching policy. |
| Baseline | The measured current state before changes. It prevents fake improvement claims. | Current average handle time is 14.2 minutes. |
| Non-AI alternative | A non-model intervention that may solve the problem. It prevents unnecessary AI complexity. | Better templates and policy search. |

### Connected dry run

Start with one vague request and convert it into a testable problem.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | Leadership asks for AI. | Executive request |
| 2 | The team identifies the business outcome. | Business outcome |
| 3 | The team names the user task. | User task |
| 4 | The team maps the workflow around the task. | Workflow |
| 5 | Evidence reveals a bottleneck. | Bottleneck, baseline |
| 6 | A non-AI alternative is documented. | Non-AI alternative |
| 7 | The problem statement becomes testable. | Problem formulation |

Step 1: leadership asks for AI.

The request is:

```text
Use AI to make support more efficient.
```

This is too broad. It does not say which user, which task, which metric, which risk, or which workflow step.

Step 2: the team identifies the outcome.

The team asks: "What would improve if this worked?" A better outcome is:

```text
Reduce support-agent drafting and policy-search time without increasing policy errors.
```

Now the work has a measurable direction.

Step 3: the team names the user task.

The user is the support agent. The task is not "do support." The task is:

```text
Find relevant policy evidence and draft a safe response for agent review.
```

Step 4: the team maps the workflow.

The agent receives a ticket, reads the customer's issue, searches policy, checks order data, drafts a reply, and escalates risky cases.

Step 5: evidence reveals the bottleneck.

Interviews and timing samples show that policy lookup and first-draft writing take the most time.

Step 6: a non-AI alternative is documented.

The team records:

```text
Improve policy search, templates, and agent training.
```

If this non-AI option solves the problem cheaply, AI may not be necessary.

Step 7: the problem becomes testable.

The final problem statement is:

```text
Support agents spend too much time finding policy evidence and writing first drafts for refund-related tickets. We will test whether evidence-backed draft assistance reduces handle time without increasing unsupported refund claims.
```

This can now be measured, challenged, or rejected.

### Mental model

Applied AI discovery is a funnel:

```text
request
  -> outcome
  -> user task
  -> workflow evidence
  -> bottleneck
  -> candidate intervention
  -> risk controls
  -> pilot decision
```

Do not skip the middle. If the team jumps from request to model, it may optimize the wrong step, automate risky work, or build a system users will not adopt.

### Worked example

Weak problem:

```text
Use an LLM to answer refund questions.
```

Strong problem:

```text
Support agents handling refund-related tickets spend a median 6.4 minutes searching policy and drafting the first reply. The pilot will test an evidence-backed draft assistant that never sends customer responses automatically and requires human approval for refund-related commitments.
```

The strong version names user, workflow step, baseline, intervention, guardrail, and evaluation target.

### Mini-implementation

This code does not build AI. It makes discovery artifacts typed and testable so weak assumptions become visible.

```python
# ai_discovery/__init__.py
"""Applied AI discovery package validation and scoring."""
```

```python
# ai_discovery/schemas.py
from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


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


class ControlMode(StrEnum):
    DECISION_SUPPORT = "decision_support"
    HUMAN_REVIEW = "human_review"
    HUMAN_APPROVAL = "human_approval"
    AUTOMATION = "automation"
    PROHIBITED = "prohibited"


class Stakeholder(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=2)
    role: str = Field(min_length=2)
    goals: list[str] = Field(min_length=1)
    concerns: list[str] = Field(default_factory=list)
    decision_authority: bool = False
    required_for_pilot: bool = True


class WorkflowStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=3)
    actor: str = Field(min_length=2)
    system: str = Field(min_length=2)
    input: str = Field(min_length=3)
    output: str = Field(min_length=3)
    average_minutes: float = Field(ge=0)
    monthly_volume: int = Field(ge=0)
    failure_modes: list[str] = Field(default_factory=list)


class BaselineMetric(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=3)
    current_value: float = Field(ge=0)
    unit: str = Field(min_length=1)
    source: str = Field(min_length=3)
    measurement_window: str = Field(min_length=3)
    owner: str = Field(min_length=2)


class UseCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=3, max_length=120)
    user: str = Field(min_length=3, max_length=120)
    business_outcome: str = Field(min_length=10, max_length=500)
    workflow_step: str = Field(min_length=3)
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
    control_mode: ControlMode
    non_ai_alternative: str = Field(min_length=5, max_length=500)
    owner: str = Field(min_length=2)

    @model_validator(mode="after")
    def validate_value_scenario(self) -> "UseCase":
        if self.expected_error_rate > self.baseline_error_rate:
            raise ValueError(
                "expected_error_rate cannot exceed baseline_error_rate in the expected-value scenario"
            )
        if self.solution_type != SolutionType.HUMAN and not self.non_ai_alternative:
            raise ValueError("a non-AI alternative is required")
        return self


class RiskRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    risk: str = Field(min_length=3)
    cause: str = Field(min_length=3)
    affected_party: str = Field(min_length=2)
    impact: str = Field(min_length=3)
    detection: str = Field(min_length=3)
    preventive_control: str = Field(min_length=3)
    response: str = Field(min_length=3)
    owner: str = Field(min_length=2)


class DiscoveryPackage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    package_id: str = Field(min_length=3)
    business_problem: str = Field(min_length=20)
    stakeholders: list[Stakeholder] = Field(min_length=1)
    workflow_steps: list[WorkflowStep] = Field(min_length=1)
    baselines: list[BaselineMetric] = Field(min_length=1)
    use_cases: list[UseCase] = Field(min_length=1)
    selected_use_case: str = Field(min_length=3)
    rejected_use_cases: list[str] = Field(default_factory=list)
    risks: list[RiskRecord] = Field(min_length=1)
    success_metrics: list[str] = Field(min_length=1)
    non_ai_fallback: str = Field(min_length=5)
    pilot_scope: str = Field(min_length=5)
    approval_owner: str = Field(min_length=2)
    notes: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_selected_use_case(self) -> "DiscoveryPackage":
        names = {use_case.name for use_case in self.use_cases}
        if self.selected_use_case not in names:
            raise ValueError("selected_use_case must match a use case name")
        if not any(stakeholder.decision_authority for stakeholder in self.stakeholders):
            raise ValueError("at least one stakeholder must have decision authority")
        return self
```

### Tests

```python
# tests/test_schemas.py
import pytest

from ai_discovery.schemas import ControlMode, SolutionType, UseCase


def valid_use_case_data() -> dict[str, object]:
    return {
        "name": "Evidence-backed response drafting",
        "user": "Support agent",
        "business_outcome": "Reduce search and drafting time without increasing policy errors",
        "workflow_step": "Draft first response",
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
        "control_mode": ControlMode.HUMAN_APPROVAL,
        "non_ai_alternative": "Improve policy search, templates, and agent training",
        "owner": "Support operations",
    }


def test_valid_use_case_is_accepted() -> None:
    use_case = UseCase.model_validate(valid_use_case_data())
    assert use_case.name == "Evidence-backed response drafting"
    assert use_case.control_mode == ControlMode.HUMAN_APPROVAL


def test_expected_error_cannot_exceed_baseline() -> None:
    data = valid_use_case_data()
    data["expected_error_rate"] = 0.12
    with pytest.raises(ValueError):
        UseCase.model_validate(data)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("adoption_rate", 1.5),
        ("consequence", 6),
        ("minutes_saved_per_case", -1),
    ],
)
def test_out_of_range_values_are_rejected(field: str, value: object) -> None:
    data = valid_use_case_data()
    data[field] = value
    with pytest.raises(ValueError):
        UseCase.model_validate(data)
```

### Verify

```bash
pytest tests/test_schemas.py
```

### Module completion checkpoint

At this point, your project should:

- define the discovery data contract;
- validate one use case;
- reject impossible or out-of-range assumptions;
- explain why a business problem is not the same thing as a model request.

### Common misconception

Misconception: "The business problem is already clear because leadership requested AI."

Why it seems plausible: Leadership usually knows real pain exists.

Correct model: Leadership may know pain exists, but discovery must identify the user task, bottleneck, baseline, risk, and non-AI alternative.

Test case: If the team cannot name the workflow step and baseline, the problem is not ready.

### Guided practice and independent transfer

- Guided: Rewrite "automate support with AI" into a problem statement with user, workflow step, baseline, outcome, and guardrail.
- Independent transfer: Apply the same structure to invoice review, sales call summarization, or internal IT helpdesk triage.

### Recall

- What is the difference between an executive request and a business outcome?
- Why is a baseline required before ROI?
- What does a non-AI alternative protect against?
- Why should discovery artifacts be typed and testable?

## Hybrid module 2: Stakeholder discovery and workflow mapping

### Core question

Whose work changes, and what actually happens before, during, and after the proposed AI step?

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Stakeholder | A person or group affected by the workflow or decision. Missing stakeholders create adoption and risk surprises. | Support agents, team leads, customers, legal, finance. |
| Decision authority | The person or group allowed to approve scope, budget, or risk. It prevents unclear ownership. | The support VP approves the pilot scope. |
| Current-state workflow | The workflow as it works today, not as the process document claims. It reveals real bottlenecks. | Agents copy policy text manually because search is poor. |
| Failure path | A route through the workflow where work fails, loops, escalates, or creates harm. | Draft goes to lead review because refund evidence is missing. |
| Handoff | A transfer of work between people or systems. Handoffs often create delay and missing context. | Agent escalates to billing specialist. |
| Shadow work | Unofficial work people do to make a broken process function. It often reveals the true system. | Agents keep personal policy notes. |

### Connected dry run

Trace one ticket through stakeholder discovery and workflow mapping.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | The team identifies everyone affected. | Stakeholder |
| 2 | The team separates users from decision owners. | Decision authority |
| 3 | Interviews capture what people actually do. | Current-state workflow |
| 4 | The workflow map records steps, systems, inputs, and outputs. | Workflow step |
| 5 | Loops and escalations are marked. | Failure path |
| 6 | Informal workarounds are recorded. | Shadow work |
| 7 | The team chooses which step is in pilot scope. | Workflow boundary |

Step 1: the team identifies affected people.

Support agents use the tool. Team leads review risky responses. Customers are affected by replies. Legal and security care about policy and data. Finance cares about cost assumptions.

Step 2: users and decision owners are separated.

Agents may know the workflow best, but the support VP may own the pilot decision. Both are needed.

Step 3: interviews capture real work.

The team asks agents to walk through a recent refund ticket. The goal is not to confirm the official process. The goal is to find what actually happens.

Step 4: the workflow map records the current state.

A useful row includes actor, system, input, output, average time, volume, and failure modes.

Step 5: failure paths are marked.

When evidence is missing, the agent escalates. When policy is unclear, a lead reviews. These loops matter because AI may amplify them if they are ignored.

Step 6: shadow work is documented.

Agents may use personal notes because policy search is slow. That is not a user flaw. It is evidence of a system gap.

Step 7: pilot scope is narrowed.

The team chooses "evidence-backed first-draft assistance for refund tickets" rather than "automate support."

### Concept model

Discovery is not just interviewing people. It is building a shared evidence map:

```text
stakeholders
  -> goals and concerns
  -> current workflow
  -> failure paths
  -> pilot boundary
```

Every stakeholder adds a different constraint. Agents reveal friction. Operations reveals volumes. Legal and security reveal risk. Finance challenges ROI. Customers experience the outcome.

### Product consequence

If the team interviews only executives, it may build a system that optimizes reporting instead of real agent work. If it interviews only agents, it may miss governance and budget constraints. The pilot needs both workflow truth and decision authority.

### Worked example

Stakeholder map:

| Stakeholder | Goal | Concern | Required involvement |
|---|---|---|---|
| Support agent | Faster safe replies | Tool adds review work | Workflow interviews and pilot feedback |
| Team lead | Lower escalation load | Unsafe drafts | Approval design |
| Customer | Correct reply | Wrong refund promise | Customer-impact metrics |
| Legal/security | Policy and privacy | PII leakage, commitments | Risk review |
| Finance | Defensible value | Inflated ROI | Scenario review |

### Build

Add stakeholder and workflow sections to `discovery/response-drafting-package.yaml` later in Module 8. For now, design them with these fields:

```text
stakeholders:
  - name
  - role
  - goals
  - concerns
  - decision_authority

workflow_steps:
  - name
  - actor
  - system
  - input
  - output
  - average_minutes
  - monthly_volume
  - failure_modes
```

### Tests

The schema tests from Module 1 enforce required fields. Module 7 adds completeness checks across the whole package.

### Experiment

Interview two simulated users with conflicting incentives:

| Interviewee | Likely emphasis | Evidence to request |
|---|---|---|
| Support manager | Handle time, staffing, escalation | Volume, backlog, QA scores |
| Support agent | Search friction, unclear policy, tooling | Screen-share workflow, recent tickets |

Failure signal: both interviews describe different workflows and nobody can produce baseline data.

### Interpret results

Different stakeholder stories are not a problem by themselves. They are discovery evidence. The problem is making an implementation decision before reconciling them.

### Verify

```bash
pytest tests/test_schemas.py
```

### Module completion checkpoint

At this point, your project should:

- identify affected stakeholders;
- distinguish users from decision owners;
- define a current-state workflow shape;
- explain at least one failure path and one workaround.

### Failure drill

Failure: The workflow map shows only the happy path.

Evidence: No escalations, exceptions, rework, or human review are represented.

Fix: Ask for recent failed cases and map them separately.

Prevention: Require every workflow map to include at least one failure path.

### Common misconception

Misconception: "A workflow diagram from documentation is enough."

Why it seems plausible: Official process documents look authoritative.

Correct model: Actual work often includes workarounds, queues, and exceptions not captured in documentation.

### Guided practice and independent transfer

- Guided: Map the current refund-ticket workflow in five to eight steps.
- Independent transfer: Map an internal IT password-reset workflow and mark where AI would be forbidden.

### Recall

- Why should affected people and decision owners both be interviewed?
- What is a failure path?
- Why is shadow work useful evidence?
- What fields make a workflow step measurable?

## Hybrid module 3: Baseline, bottlenecks, and measurable evidence

### Core question

What current-state evidence is required before you can claim an AI pilot created value?

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Baseline metric | A measured current-state value. It is the comparison point for improvement. | Average handle time is 14.2 minutes. |
| Measurement window | The period used for measurement. It prevents cherry-picking. | Last full calendar month. |
| Bottleneck | The constrained or slowest high-value part of the workflow. It tells where intervention may help. | Policy lookup takes 6.4 minutes. |
| Error cost | The estimated cost of mistakes or rework. It makes quality visible in ROI. | Unsupported refund promise costs $18 in rework on average. |
| Counterfactual | What would happen without the AI system. It prevents crediting AI for unrelated process changes. | New templates alone might reduce handle time. |
| Evidence quality | How reliable the baseline is. Weak evidence should lower readiness. | Dashboard samples are better than anecdotes. |

### Connected dry run

Follow one metric from raw observation to baseline evidence.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | The team picks a workflow step to measure. | Bottleneck |
| 2 | It defines a baseline metric. | Baseline metric |
| 3 | It records source and measurement window. | Measurement window |
| 4 | It estimates cost of errors and rework. | Error cost |
| 5 | It compares against a non-AI path. | Counterfactual |
| 6 | It rates whether the evidence is strong enough. | Evidence quality |
| 7 | Weak evidence becomes a discovery task, not an ROI claim. | Readiness |

Step 1: the team chooses the step.

The workflow map shows policy lookup and first-draft writing as time-consuming.

Step 2: a baseline metric is defined.

The metric is:

```text
Median time from ticket open to first draft for refund-related tickets.
```

Step 3: the measurement source is recorded.

The team uses helpdesk timestamps and a sampled screen-share study from the last month. The source matters because self-reported time is weaker than system timestamps.

Step 4: error cost is estimated.

Quality review shows unsupported refund language creates rework. The team assigns a conservative rework cost for scenario comparison.

Step 5: the counterfactual is documented.

The team asks: "What if we only improved templates and policy search?" This prevents the AI pilot from taking credit for process fixes.

Step 6: evidence quality is rated.

If the data is sampled, stale, or incomplete, readiness goes down.

Step 7: weak evidence blocks false precision.

When baseline evidence is weak, the right next step is measurement, not an AI demo.

### Concept model

Baseline evidence connects the workflow to business value:

```text
workflow step
  -> measured baseline
  -> bottleneck
  -> candidate intervention
  -> expected delta
  -> evaluation plan
```

Without a baseline, a demo can feel useful while creating no measurable value.

### Product consequence

Northstar should not claim productivity improvement from "agents liked the demo." Adoption and satisfaction matter, but value needs measured time, quality, and cost changes.

### Worked example

Baseline table:

| Metric | Current value | Source | Window | Owner |
|---|---:|---|---|---|
| Refund ticket monthly volume | 18,000 | Helpdesk analytics | Last 30 days | Support ops |
| Median policy lookup + drafting time | 6.4 min | Screen-share sample | Two-week sample | Support ops |
| Unsupported refund language rate | 8% | QA sample | Last month | QA lead |
| Escalation rate | 22% | Helpdesk tags | Last month | Team leads |

### Build

Baseline records are captured in the YAML package in Module 8 and validated by `DiscoveryPackage`.

### Tests

The schema requires every baseline metric to include a source, measurement window, and owner.

### Experiment

Take one baseline metric and ask:

| Question | Good answer |
|---|---|
| Where did it come from? | Named system or sampled study. |
| How recent is it? | Measurement window recorded. |
| Who owns it? | Person or team named. |
| What can bias it? | Known limitation stated. |

Failure signal: metric has a precise number but no source.

### Interpret results

Precise numbers are not necessarily better. A rough measured range is better than an invented exact ROI.

### Verify

```bash
pytest tests/test_schemas.py
```

### Module completion checkpoint

At this point, your project should:

- define baseline metrics with source and window;
- identify at least one bottleneck;
- separate baseline evidence from target assumptions;
- state a non-AI counterfactual.

### Failure drill

Failure: ROI is calculated from guessed time savings.

Evidence: No current handle-time source exists.

Fix: Run a short measurement study before ROI.

Prevention: Require baseline source and measurement window in every discovery package.

### Common misconception

Misconception: "A pilot can prove value without baseline because users will know if it helps."

Correct model: User feedback helps explain adoption, but measured baseline is required for value claims.

### Guided practice and independent transfer

- Guided: Define three baseline metrics for support drafting.
- Independent transfer: Define baseline metrics for contract review or sales-call summarization.

### Recall

- What makes a baseline metric auditable?
- Why does counterfactual matter?
- What should happen when evidence quality is weak?
- How can a bottleneck differ from the loudest complaint?

## Hybrid module 4: Candidate interventions and AI suitability

### Core question

How do you choose between process change, deterministic software, rules, search, ML, LLMs, RAG, tools, agents, fine-tuning, and human operations?

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Candidate intervention | A possible change to the workflow. Comparing candidates prevents model-first thinking. | Better templates, search, RAG draft assistant, or human QA. |
| Decision support | AI assists a human decision but does not take final action. | Draft a reply for agent review. |
| Automation | The system takes action without human approval. It raises risk. | Auto-send a refund approval. |
| Deterministic solution | A predictable software or process fix. It is often safer and cheaper than AI. | Route tickets by keyword rules. |
| AI suitability | A check that asks whether AI is necessary, useful, and controllable. | Use AI only if language variability matters and output can be reviewed. |
| Rejected alternative | A documented option not selected. It prevents repeated debate and shows judgment. | Reject autonomous refund agent for first pilot. |

### Connected dry run

Compare four possible interventions for the same bottleneck.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | The team names the bottleneck. | Candidate intervention |
| 2 | A non-AI process fix is considered. | Deterministic/process solution |
| 3 | A rules/search option is considered. | Rules, search |
| 4 | A decision-support AI option is considered. | Decision support |
| 5 | A high-autonomy option is rejected. | Automation, rejected alternative |
| 6 | Suitability is checked against data, risk, reviewability, and value. | AI suitability |
| 7 | The selected pilot is narrowed. | Pilot scope |

Step 1: the bottleneck is policy-backed drafting.

Agents spend time finding evidence and writing first drafts.

Step 2: process fix is considered.

The team could improve policy templates and training. This is cheap and safe. It may be enough for some cases.

Step 3: rules/search is considered.

The team could improve search and route refund tickets to policy snippets. This is predictable and easier to govern.

Step 4: decision-support AI is considered.

An AI draft assistant can summarize evidence and produce a first draft for agent review. It handles varied language but must be validated and reviewed.

Step 5: high-autonomy automation is rejected.

An autonomous agent that approves refunds is too risky for the first pilot.

Step 6: suitability is checked.

AI may be justified because support tickets are variable language tasks and the draft can be reviewed before customer impact.

Step 7: the pilot is narrowed.

The team selects:

```text
Evidence-backed response drafting for refund-related tickets, human approval required.
```

### Concept model

Use a ladder of complexity:

```text
process improvement
  -> deterministic software
  -> rules/search
  -> classical ML
  -> hosted LLM
  -> RAG
  -> tool workflow
  -> controlled agent
  -> fine-tuning
  -> multimodal
```

Move up the ladder only when simpler options do not satisfy the workflow need.

### Product consequence

Choosing the wrong solution type can create avoidable cost and risk. A rules-based routing fix may be better than an LLM. A draft assistant may be better than an autonomous agent.

### Worked example

| Option | Fits? | Reason |
|---|---|---|
| Better templates | Partial | Low risk, but does not solve policy lookup. |
| Improved search | Strong baseline | Helps evidence access. |
| Direct LLM drafting | Weak | Can hallucinate without evidence. |
| RAG-assisted drafting | Strong candidate | Uses evidence and keeps agent approval. |
| Autonomous refund agent | Reject | High consequence and irreversible actions. |

### Build

The `SolutionType` enum and `UseCase` schema encode the candidate type and require a non-AI alternative.

### Tests

The schema test rejects invalid or unsupported assumptions. Scoring tests later show how risk/readiness affect the recommendation.

### Experiment

For each candidate, answer:

```text
What problem does it solve?
What simpler option might solve it?
What data does it need?
How is output reviewed?
What action is prohibited?
```

Failure signal: the use case cannot explain why a simpler option is insufficient.

### Interpret results

"AI can do it" is not a selection criterion. The relevant criteria are value, control, reviewability, data readiness, and operational fit.

### Verify

```bash
pytest tests/test_schemas.py
```

### Module completion checkpoint

At this point, your project should:

- list candidate interventions;
- document rejected alternatives;
- distinguish decision support from automation;
- justify why the selected pilot needs AI at all.

### Failure drill

Failure: The team selects RAG before testing search or templates.

Evidence: No simpler option is documented.

Fix: Add a non-AI and search baseline to the use-case register.

Prevention: Require rejected alternatives in every discovery package.

### Common misconception

Misconception: "The best AI system is the most autonomous one."

Correct model: The best first pilot is often decision support with human approval and narrow scope.

### Guided practice and independent transfer

- Guided: Compare rules, search, LLM, RAG, and human work for refund drafting.
- Independent transfer: Compare candidate interventions for invoice exception triage.

### Recall

- Why should simpler interventions be considered first?
- What is the difference between decision support and automation?
- Why document rejected alternatives?
- When is AI suitability weak?

## Hybrid module 5: Risk classification and human-control design

### Core question

Which actions require human review, human approval, override, abstention, or rejection?

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Consequence | Severity if the system is wrong. It drives control requirements. | Wrong refund approval creates financial and policy risk. |
| Autonomy | How much action the system takes without a person. Higher autonomy raises risk. | Drafting is lower autonomy than sending. |
| Data sensitivity | How sensitive the data is. It affects privacy and access controls. | Customer order and billing data are sensitive. |
| Uncertainty | How hard it is to know whether the output is correct. It affects review and abstention. | Missing policy evidence increases uncertainty. |
| Irreversibility | How hard it is to undo an action. It affects approval requirements. | Sending a customer commitment is harder to undo than drafting. |
| Human review | A person checks output before use. It catches quality problems. | Agent reviews draft text. |
| Human approval | A person explicitly approves a consequential action. It gates risk. | Team lead approves refund-related promise. |
| Abstention | The system refuses to answer fully when evidence is missing. It prevents fake certainty. | Ask for order date instead of approving refund. |

### Connected dry run

Classify one risky refund-drafting use case.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | The team identifies possible harm. | Consequence |
| 2 | It checks whether the system acts or only assists. | Autonomy |
| 3 | It marks sensitive data. | Data sensitivity |
| 4 | It asks whether correctness can be verified. | Uncertainty |
| 5 | It checks whether mistakes are reversible. | Irreversibility |
| 6 | It selects review and approval controls. | Human review, human approval |
| 7 | It defines when the system must abstain. | Abstention |
| 8 | It records owner, detection, prevention, and response. | Risk register |

Step 1: possible harm is named.

The system could draft an unsupported refund promise.

Step 2: autonomy is checked.

The selected pilot drafts for an agent. It does not send to the customer. Autonomy is low.

Step 3: sensitive data is marked.

Tickets and orders may contain names, emails, addresses, payment context, and account details.

Step 4: uncertainty is assessed.

If policy evidence is missing, the system cannot safely recommend eligibility.

Step 5: reversibility is assessed.

A draft is reversible. A sent customer promise is not easily reversible.

Step 6: human control is chosen.

The agent reviews every draft. Refund-related commitments require human approval.

Step 7: abstention is defined.

If required evidence is missing, the system asks for missing information instead of drafting a confident decision.

Step 8: risk response is assigned.

The risk register names owner, detection, preventive control, and incident response.

### Concept model

Risk is not a generic label on "AI." It is specific to:

```text
task + data + user + autonomy + consequence + reversibility + controls
```

The same model output can be low risk as a draft and high risk as an automatic action.

### Product consequence

Northstar can pilot draft assistance because a human remains in control. It should not pilot autonomous refunds because consequence and irreversibility are too high.

### Worked example

| Action | Control mode |
|---|---|
| Suggest category | Human review |
| Draft reply | Human review |
| Mention missing evidence | Human review |
| Promise refund eligibility | Human approval |
| Issue refund | Prohibited in first pilot |
| Change account status | Prohibited in first pilot |

### Build

The `ControlMode` enum and risk fields in `UseCase` make control boundaries explicit.

### Tests

Module 6 scoring tests reject high-risk autonomy without human approval.

### Experiment

Take one candidate action and ask:

```text
If this is wrong, who is harmed?
Can a person catch it before impact?
Can it be undone?
Who approves it?
What evidence is required?
```

Failure signal: the system has an action but no approval owner.

### Interpret results

High value does not cancel high risk. High-value, high-risk work may need stronger controls, a narrower pilot, or rejection.

### Verify

```bash
pytest tests/test_schemas.py
```

### Module completion checkpoint

At this point, your project should:

- score risk dimensions for each use case;
- define control mode;
- specify abstention conditions;
- assign risk owners.

### Failure drill

Failure: The design says "human in the loop" but not what the human does.

Evidence: No review criteria, approval owner, or override process.

Fix: Specify review, approval, override, and escalation.

Prevention: Treat "human in the loop" as incomplete until roles and decisions are explicit.

### Common misconception

Misconception: "Human review means the system is safe."

Correct model: Human review is only useful if the reviewer has time, evidence, authority, and clear criteria.

### Guided practice and independent transfer

- Guided: Classify support-drafting actions by review, approval, prohibited, or abstain.
- Independent transfer: Classify actions for HR resume screening or medical appointment triage.

### Recall

- What is the difference between human review and human approval?
- Why is reversibility important?
- Why is risk use-case specific?
- When should a system abstain?

## Hybrid module 6: Metrics, ROI, adoption, and go/no-go evidence

### Core question

How do you estimate expected value without pretending discovery math is a forecast?

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Value scenario | A transparent calculation of possible benefit and cost. It is not a promise. | 3.5 minutes saved per adopted case. |
| Labor benefit | Estimated value from time saved or capacity created. It should avoid double-counting. | Fewer minutes per ticket. |
| Error avoidance | Estimated value from fewer mistakes or rework. It makes quality visible. | Fewer unsupported refund drafts. |
| Operating cost | Recurring cost after launch. It includes model, review, monitoring, and maintenance. | Monthly provider cost plus oversight. |
| Payback period | Time needed for benefits to recover implementation cost. | Implementation cost divided by monthly net value. |
| Adoption metric | Measures whether users actually use and accept the workflow. | Percentage of eligible tickets where agents use the draft. |
| Go/no-go criteria | Predefined decision rules for proceed, revise, or stop. | Stop if unsupported claims increase. |

### Connected dry run

Run one candidate through an ROI and readiness scenario.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | The team enters baseline volume and time savings. | Labor benefit |
| 2 | It enters expected error-rate change. | Error avoidance |
| 3 | It adds implementation and operating costs. | Operating cost |
| 4 | It calculates first-year net value and ROI. | Value scenario |
| 5 | It calculates payback period. | Payback period |
| 6 | It combines risk and readiness evidence. | Risk score, readiness score |
| 7 | It produces a recommendation with caveats. | Go/no-go criteria |

Step 1: labor benefit is estimated.

If 18,000 cases per month are eligible, adoption is 60%, and the tool saves 3.5 minutes per used case, the team can estimate annual hours saved.

Step 2: error avoidance is estimated.

If unsupported refund language falls from 8% to 6%, the scenario estimates avoided rework.

Step 3: costs are added.

Implementation, model usage, oversight, evaluation, and maintenance are included. Omitting oversight makes ROI look falsely high.

Step 4: first-year net value is calculated.

The scenario subtracts first-year costs from annual benefit.

Step 5: payback is calculated.

If monthly net value after launch is positive, implementation cost can be divided by monthly net value.

Step 6: risk and readiness remain separate.

The team does not merge all numbers into one magic AI score. A profitable but high-risk case may still require a controlled pilot or rejection.

Step 7: recommendation is produced.

The recommendation is advisory:

```text
controlled-pilot: narrow scope and require approval
```

Humans still decide.

### Concept model

Discovery math should make assumptions visible:

```text
volume
  x adoption
  x minutes saved
  x labor cost
  + error avoidance
  - implementation and operating cost
  -> value scenario
```

Then evaluate separately:

```text
value scenario + risk + readiness + adoption path -> decision
```

### Product consequence

Northstar should not approve a pilot because ROI is positive alone. The pilot must also have data readiness, control design, owner commitment, and stop conditions.

### Worked example

| Metric | Example |
|---|---:|
| Monthly volume | 18,000 |
| Adoption | 60% |
| Minutes saved per adopted case | 3.5 |
| Loaded labor cost | $34/hour |
| Baseline error rate | 8% |
| Expected error rate | 6% |
| Implementation cost | $120,000 |
| Monthly recurring + oversight | $12,000 |

### Build

```python
# ai_discovery/scoring.py
from __future__ import annotations

from dataclasses import dataclass

from ai_discovery.schemas import ControlMode, UseCase


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
    annual_labor_benefit = annual_hours_saved * use_case.loaded_labor_cost_per_hour

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


def triage_recommendation(use_case: UseCase, business_case: BusinessCase) -> str:
    if business_case.readiness_score < 7:
        return "research: improve evidence, data, or integration readiness"

    high_risk = business_case.risk_score >= 17
    lacks_control = use_case.control_mode not in {
        ControlMode.HUMAN_REVIEW,
        ControlMode.HUMAN_APPROVAL,
    }
    if high_risk and lacks_control:
        return "reject: risk requires stronger human control"

    if business_case.first_year_net_value <= 0:
        return "revise: current value scenario does not justify first-year cost"

    if business_case.risk_score >= 17:
        return "controlled-pilot: narrow scope and require approval"

    return "pilot: proceed with defined guardrails and evaluation"
```

### Tests

```python
# tests/test_scoring.py
from ai_discovery.schemas import ControlMode, SolutionType, UseCase
from ai_discovery.scoring import calculate_business_case, triage_recommendation


def response_drafting_use_case(**overrides: object) -> UseCase:
    data: dict[str, object] = {
        "name": "Evidence-backed response drafting",
        "user": "Support agent",
        "business_outcome": "Reduce search and drafting time without increasing policy errors",
        "workflow_step": "Draft first response",
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
        "control_mode": ControlMode.HUMAN_APPROVAL,
        "non_ai_alternative": "Improve policy search, templates, and agent training",
        "owner": "Support operations",
    }
    data.update(overrides)
    return UseCase.model_validate(data)


def test_business_case_calculates_value_and_scores() -> None:
    use_case = response_drafting_use_case()
    result = calculate_business_case(use_case)
    assert result.annual_total_benefit > 0
    assert result.first_year_total_cost == 264000
    assert result.risk_score == 13
    assert result.readiness_score == 12
    assert triage_recommendation(use_case, result) == "pilot: proceed with defined guardrails and evaluation"


def test_low_readiness_requires_research() -> None:
    use_case = response_drafting_use_case(evidence_quality=1, data_readiness=2, integration_readiness=2)
    result = calculate_business_case(use_case)
    assert triage_recommendation(use_case, result).startswith("research")


def test_high_risk_without_control_is_rejected() -> None:
    use_case = response_drafting_use_case(
        consequence=5,
        autonomy=5,
        data_sensitivity=5,
        uncertainty=4,
        irreversibility=4,
        control_mode=ControlMode.AUTOMATION,
    )
    result = calculate_business_case(use_case)
    assert triage_recommendation(use_case, result).startswith("reject")
```

### Experiment

Create three scenarios:

| Scenario | Change | Expected decision effect |
|---|---|---|
| Conservative | Lower adoption and savings | ROI may become weak. |
| Riskier | Increase autonomy and consequence | Human control required. |
| Low readiness | Lower evidence/data/integration scores | Research before pilot. |

Failure signal: the decision does not change when assumptions change.

### Interpret results

A scenario model is useful only if it is sensitive to assumptions. If every input produces "go," the model is a sales document, not a decision tool.

### Verify

```bash
pytest tests/test_scoring.py
```

### Module completion checkpoint

At this point, your project should:

- calculate value and cost separately;
- calculate risk and readiness separately;
- produce a recommendation without automatic approval;
- explain why ROI is a scenario, not a forecast.

### Failure drill

Failure: ROI looks high because review cost is omitted.

Evidence: Monthly oversight cost is zero despite mandatory human review.

Fix: Add reviewer time, QA, monitoring, and maintenance.

Prevention: Require recurring and oversight cost fields.

### Common misconception

Misconception: "Positive ROI means the AI project should proceed."

Correct model: Positive ROI is necessary but not sufficient. Risk, readiness, controls, adoption, and fallback also matter.

### Guided practice and independent transfer

- Guided: Change adoption from 60% to 20% and explain the decision impact.
- Independent transfer: Build a scenario for AI-assisted invoice exception triage.

### Recall

- Why should labor benefit and error avoidance be separated?
- What does payback period measure?
- Why keep risk separate from ROI?
- What should happen when readiness is low?

## Implementation module 7: Discovery package, PRD, ADR, and pilot plan

### Purpose

The discovery work must produce a decision package, not a pile of notes. The package should be reviewable by product, engineering, support operations, finance, security, and legal.

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| PRD | Product Requirements Document. It defines user, problem, scope, requirements, constraints, and metrics. | "Draft assistance for refund tickets only." |
| ADR | Architecture Decision Record. It records a decision and rejected alternatives. | Select RAG-assisted drafting; reject autonomous agent. |
| Risk register | A table of risks, causes, controls, owners, and responses. It turns risk into operational work. | Unsupported refund claim -> block and human review. |
| Pilot plan | A controlled rollout plan. It limits blast radius and creates decision points. | Two teams, shadow mode first, four weeks. |
| Go/no-go criteria | Explicit proceed/revise/stop rules. It prevents moving forward because of demo excitement. | Stop if unsupported claims increase. |
| Artifact completeness | A check that required discovery evidence exists. It prevents missing sections from being ignored. | Package fails if no non-AI fallback exists. |

### Connected dry run

Assemble one discovery package and check whether it is review-ready.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | The team summarizes the selected pilot. | PRD |
| 2 | It records options and rejected alternatives. | ADR |
| 3 | It documents risks and owners. | Risk register |
| 4 | It defines rollout stages and stop conditions. | Pilot plan |
| 5 | It states go/revise/stop criteria. | Go/no-go criteria |
| 6 | A validator checks missing artifacts. | Artifact completeness |
| 7 | Reviewers can approve, revise, or stop. | Decision package |

Step 1: the PRD names the pilot.

The PRD says the pilot supports evidence-backed drafting for refund tickets. It excludes autonomous sending, refund issuance, and account changes.

Step 2: the ADR records the decision.

The ADR compares process-only, direct LLM drafting, RAG-assisted drafting, and autonomous agent. It selects the controlled drafting pilot and rejects the agent.

Step 3: the risk register assigns owners.

Every major risk has detection, prevention, response, and owner. "We will monitor it" is not enough.

Step 4: the pilot plan limits exposure.

The pilot starts in shadow mode, then a limited agent pilot, then go/revise/stop.

Step 5: go/no-go criteria are written before launch.

The team defines what counts as success, what requires revision, and what stops the pilot.

Step 6: validation checks completeness.

The CLI can flag missing baselines, risk owners, selected use case, or fallback.

Step 7: reviewers make the decision.

The package informs the decision. It does not make the decision automatically.

### Design decision

Use a structured YAML package and a validator rather than a spreadsheet-only process. Spreadsheets remain useful for finance review, but the canonical discovery package should be versioned, testable, and reviewable.

### Build

```python
# ai_discovery/artifacts.py
from __future__ import annotations

from ai_discovery.schemas import ControlMode, DiscoveryPackage
from ai_discovery.scoring import calculate_business_case


def selected_use_case(package: DiscoveryPackage):
    for use_case in package.use_cases:
        if use_case.name == package.selected_use_case:
            return use_case
    raise ValueError("selected use case not found")


def validate_discovery_package(package: DiscoveryPackage) -> list[str]:
    findings: list[str] = []

    if not package.rejected_use_cases:
        findings.append("rejected use cases are missing")

    if len(package.baselines) < 3:
        findings.append("at least three baseline metrics are recommended")

    if not package.non_ai_fallback.strip():
        findings.append("non-AI fallback is missing")

    risk_owners = {risk.owner for risk in package.risks}
    if not risk_owners:
        findings.append("risk owners are missing")

    use_case = selected_use_case(package)
    business_case = calculate_business_case(use_case)

    if business_case.risk_score >= 17 and use_case.control_mode not in {
        ControlMode.HUMAN_REVIEW,
        ControlMode.HUMAN_APPROVAL,
    }:
        findings.append("high-risk use case lacks human review or approval")

    if business_case.readiness_score < 7:
        findings.append("selected use case readiness is too low for pilot")

    if "stop" not in " ".join(package.success_metrics).lower():
        findings.append("success metrics should include stop conditions")

    return findings


def prd_summary(package: DiscoveryPackage) -> dict[str, object]:
    use_case = selected_use_case(package)
    return {
        "problem": package.business_problem,
        "selected_use_case": use_case.name,
        "user": use_case.user,
        "business_outcome": use_case.business_outcome,
        "control_mode": use_case.control_mode.value,
        "non_ai_fallback": package.non_ai_fallback,
        "pilot_scope": package.pilot_scope,
        "approval_owner": package.approval_owner,
    }
```

### Unit tests

```python
# tests/test_artifacts.py
from tests.test_cli import valid_package

from ai_discovery.artifacts import prd_summary, validate_discovery_package
from ai_discovery.schemas import DiscoveryPackage


def test_complete_package_has_no_findings() -> None:
    package = DiscoveryPackage.model_validate(valid_package())
    assert validate_discovery_package(package) == []


def test_missing_rejected_use_cases_is_flagged() -> None:
    data = valid_package()
    data["rejected_use_cases"] = []
    package = DiscoveryPackage.model_validate(data)
    assert "rejected use cases are missing" in validate_discovery_package(package)


def test_prd_summary_contains_selected_pilot() -> None:
    package = DiscoveryPackage.model_validate(valid_package())
    summary = prd_summary(package)
    assert summary["selected_use_case"] == "Evidence-backed response drafting"
    assert summary["control_mode"] == "human_approval"
```

### Verify in runtime

```bash
pytest tests/test_artifacts.py
```

### Module completion checkpoint

At this point, your project should:

- validate package completeness;
- summarize the selected PRD scope;
- reject missing alternatives or controls;
- explain the decision package to non-engineering reviewers.

### Failure drill

Failure: The ADR says "use AI" but does not list rejected alternatives.

Evidence: No process/search/human option is compared.

Fix: Add an alternatives table with rejection rationale.

Prevention: Artifact validation requires `rejected_use_cases`.

### Production note

In a real organization, the package should be reviewed by support operations, product, security, legal, finance, and engineering before implementation starts.

### Guided practice and independent transfer

- Guided: Write the ADR context, decision, rejected alternatives, and consequences for the support-drafting pilot.
- Independent transfer: Write a PRD and ADR for AI-assisted claims intake.

### Recall

- What is the difference between a PRD and an ADR?
- Why does a risk register need owners?
- Why should stop conditions be defined before the pilot?
- What does artifact completeness prove and not prove?

## Implementation module 8: CLI validation, evaluation report, and operating path

### Purpose

The discovery package should run in a repeatable way. A CLI report makes assumptions visible and lets reviewers reproduce the recommendation.

### Key concepts

| Concept/term | Why it matters | Very simple example |
|---|---|---|
| Discovery package | The structured source of truth for the proposed pilot. | `response-drafting-package.yaml`. |
| CLI report | A reproducible report generated from package data. It prevents hand-edited decision summaries. | JSON report with ROI and recommendation. |
| Validation finding | A warning that the package is incomplete or unsafe. | "Rejected use cases are missing." |
| Operating cadence | The recurring process for review, update, and decision. | Weekly pilot review with support ops and risk owner. |
| Rollback path | The way to return to the old workflow if the pilot fails. | Disable draft assistance and use templates/search. |
| Decision log | The record of decisions, owners, dates, and evidence. | "June 28: proceed to shadow pilot." |

### Connected dry run

Run the package through the CLI and interpret the result.

Dry-run map:

| Step | What happens | Concepts being used |
|---:|---|---|
| 1 | The CLI loads the YAML package. | Discovery package |
| 2 | Pydantic validates the structure. | Schema validation |
| 3 | The selected use case is scored. | ROI, risk, readiness |
| 4 | The package is checked for missing artifacts. | Validation finding |
| 5 | A recommendation is produced. | CLI report |
| 6 | Reviewers use the report in the operating cadence. | Decision log |
| 7 | Rollback remains available if the pilot fails. | Rollback path |

Step 1: the CLI loads YAML.

The file contains stakeholders, workflow, baseline, use cases, risks, and pilot scope.

Step 2: schema validation runs.

Invalid fields fail immediately. This catches missing owners, impossible rates, and malformed values.

Step 3: the selected use case is scored.

The CLI calculates benefit, cost, ROI, payback, risk, and readiness.

Step 4: completeness checks run.

The CLI checks whether rejected use cases, baselines, fallback, risk owners, and stop conditions exist.

Step 5: a recommendation is generated.

The output might say:

```text
pilot: proceed with defined guardrails and evaluation
```

or:

```text
research: improve evidence, data, or integration readiness
```

Step 6: reviewers use the report.

The report supports a human decision. It is not an automatic green light.

Step 7: rollback remains explicit.

If the pilot fails, the workflow returns to templates, search, and manual drafting.

### Design decision

Use JSON output for the CLI report because it can be saved, diffed, audited, and consumed by CI or dashboards.

### Build

```python
# ai_discovery/cli.py
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from ai_discovery.artifacts import prd_summary, selected_use_case, validate_discovery_package
from ai_discovery.schemas import DiscoveryPackage
from ai_discovery.scoring import calculate_business_case, triage_recommendation


def load_package(path: Path) -> DiscoveryPackage:
    with path.open(encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return DiscoveryPackage.model_validate(data)


def build_report(package: DiscoveryPackage) -> dict[str, Any]:
    use_case = selected_use_case(package)
    business_case = calculate_business_case(use_case)
    findings = validate_discovery_package(package)
    recommendation = triage_recommendation(use_case, business_case)
    return {
        "package_id": package.package_id,
        "selected_use_case": use_case.name,
        "prd_summary": prd_summary(package),
        "annual_total_benefit": round(business_case.annual_total_benefit, 2),
        "first_year_total_cost": round(business_case.first_year_total_cost, 2),
        "first_year_net_value": round(business_case.first_year_net_value, 2),
        "first_year_roi": (
            round(business_case.first_year_roi, 4)
            if business_case.first_year_roi is not None
            else None
        ),
        "payback_months": (
            round(business_case.payback_months, 2)
            if business_case.payback_months is not None
            else None
        ),
        "risk_score": business_case.risk_score,
        "readiness_score": business_case.readiness_score,
        "recommendation": recommendation,
        "validation_findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an Applied AI discovery package.")
    parser.add_argument("package", type=Path)
    args = parser.parse_args(argv)
    package = load_package(args.package)
    print(json.dumps(build_report(package), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Example package:

```yaml
# discovery/response-drafting-package.yaml
package_id: "northstar-support-discovery-v1"
business_problem: "Support agents spend too much time finding policy evidence and drafting safe first responses for refund-related tickets."
stakeholders:
  - name: "Support agents"
    role: "Primary user"
    goals: ["Faster safe replies", "Less policy searching"]
    concerns: ["Bad drafts increase review work"]
    decision_authority: false
    required_for_pilot: true
  - name: "Support VP"
    role: "Business owner"
    goals: ["Improve productivity", "Protect customer trust"]
    concerns: ["Inflated ROI", "Unsafe automation"]
    decision_authority: true
    required_for_pilot: true
workflow_steps:
  - name: "Draft first response"
    actor: "Support agent"
    system: "Helpdesk and policy portal"
    input: "Refund-related support ticket"
    output: "First response draft for review"
    average_minutes: 6.4
    monthly_volume: 18000
    failure_modes: ["Policy not found", "Unsupported refund language", "Escalation delay"]
baselines:
  - name: "Refund ticket volume"
    current_value: 18000
    unit: "tickets/month"
    source: "Helpdesk analytics"
    measurement_window: "Last 30 days"
    owner: "Support operations"
  - name: "Policy lookup and first draft time"
    current_value: 6.4
    unit: "minutes"
    source: "Screen-share sample"
    measurement_window: "Two-week sample"
    owner: "Support operations"
  - name: "Unsupported refund language"
    current_value: 0.08
    unit: "rate"
    source: "QA sample"
    measurement_window: "Last 30 days"
    owner: "QA lead"
use_cases:
  - name: "Evidence-backed response drafting"
    user: "Support agent"
    business_outcome: "Reduce search and drafting time without increasing policy errors"
    workflow_step: "Draft first response"
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
    control_mode: "human_approval"
    non_ai_alternative: "Improve policy search, templates, and agent training"
    owner: "Support operations"
selected_use_case: "Evidence-backed response drafting"
rejected_use_cases:
  - "Autonomous refund approval agent"
  - "Direct LLM customer response without evidence"
risks:
  - risk: "Unsupported refund claim"
    cause: "Model drafts a commitment without policy evidence"
    affected_party: "Customer and support organization"
    impact: "Incorrect expectation, rework, financial exposure"
    detection: "QA review and unsupported-claim checks"
    preventive_control: "Human approval required for refund commitments"
    response: "Block output, escalate, revise prompt/evidence policy"
    owner: "Support operations"
success_metrics:
  - "Go: 10% handle-time reduction with no increase in unsupported refund language"
  - "Revise: quality improves but adoption remains below 30%"
  - "Stop: unsupported refund claims increase or agents bypass the workflow"
non_ai_fallback: "Use improved policy search, response templates, and manual review."
pilot_scope: "Four-week shadow pilot followed by limited agent-review pilot for refund-related tickets only."
approval_owner: "Support VP"
notes:
  data_policy: "Use synthetic examples in discovery and approved internal data for pilot review."
```

### Unit tests

```python
# tests/test_cli.py
import json
from pathlib import Path

import yaml

from ai_discovery.cli import build_report, load_package, main
from ai_discovery.schemas import DiscoveryPackage


def valid_package() -> dict[str, object]:
    return {
        "package_id": "northstar-support-discovery-v1",
        "business_problem": "Support agents spend too much time finding policy evidence and drafting safe first responses for refund-related tickets.",
        "stakeholders": [
            {
                "name": "Support agents",
                "role": "Primary user",
                "goals": ["Faster safe replies"],
                "concerns": ["Bad drafts increase review work"],
                "decision_authority": False,
            },
            {
                "name": "Support VP",
                "role": "Business owner",
                "goals": ["Improve productivity"],
                "concerns": ["Inflated ROI"],
                "decision_authority": True,
            },
        ],
        "workflow_steps": [
            {
                "name": "Draft first response",
                "actor": "Support agent",
                "system": "Helpdesk and policy portal",
                "input": "Refund-related support ticket",
                "output": "First response draft for review",
                "average_minutes": 6.4,
                "monthly_volume": 18000,
                "failure_modes": ["Policy not found"],
            }
        ],
        "baselines": [
            {
                "name": "Refund ticket volume",
                "current_value": 18000,
                "unit": "tickets/month",
                "source": "Helpdesk analytics",
                "measurement_window": "Last 30 days",
                "owner": "Support operations",
            },
            {
                "name": "Policy lookup and first draft time",
                "current_value": 6.4,
                "unit": "minutes",
                "source": "Screen-share sample",
                "measurement_window": "Two-week sample",
                "owner": "Support operations",
            },
            {
                "name": "Unsupported refund language",
                "current_value": 0.08,
                "unit": "rate",
                "source": "QA sample",
                "measurement_window": "Last 30 days",
                "owner": "QA lead",
            },
        ],
        "use_cases": [
            {
                "name": "Evidence-backed response drafting",
                "user": "Support agent",
                "business_outcome": "Reduce search and drafting time without increasing policy errors",
                "workflow_step": "Draft first response",
                "solution_type": "hybrid",
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
                "control_mode": "human_approval",
                "non_ai_alternative": "Improve policy search, templates, and agent training",
                "owner": "Support operations",
            }
        ],
        "selected_use_case": "Evidence-backed response drafting",
        "rejected_use_cases": ["Autonomous refund approval agent"],
        "risks": [
            {
                "risk": "Unsupported refund claim",
                "cause": "Model drafts a commitment without policy evidence",
                "affected_party": "Customer and support organization",
                "impact": "Incorrect expectation and rework",
                "detection": "QA review",
                "preventive_control": "Human approval required",
                "response": "Block output and escalate",
                "owner": "Support operations",
            }
        ],
        "success_metrics": [
            "Go: 10% handle-time reduction",
            "Stop: unsupported refund claims increase",
        ],
        "non_ai_fallback": "Use improved policy search, templates, and manual review.",
        "pilot_scope": "Four-week shadow pilot for refund-related tickets.",
        "approval_owner": "Support VP",
    }


def test_package_loads_from_yaml(tmp_path: Path) -> None:
    path = tmp_path / "package.yaml"
    path.write_text(yaml.safe_dump(valid_package()), encoding="utf-8")
    package = load_package(path)
    assert package.selected_use_case == "Evidence-backed response drafting"


def test_report_contains_recommendation() -> None:
    package = DiscoveryPackage.model_validate(valid_package())
    report = build_report(package)
    assert report["recommendation"] == "pilot: proceed with defined guardrails and evaluation"
    assert report["validation_findings"] == []


def test_main_prints_json_report(tmp_path: Path, capsys) -> None:
    path = tmp_path / "package.yaml"
    path.write_text(yaml.safe_dump(valid_package()), encoding="utf-8")
    assert main([str(path)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["selected_use_case"] == "Evidence-backed response drafting"
```

### Verify in runtime

```bash
pytest
python -m ai_discovery.cli discovery/response-drafting-package.yaml
```

### Module completion checkpoint

At this point, your project should:

- load a discovery YAML package;
- validate it;
- calculate scenario value and scores;
- report findings and recommendation;
- preserve human decision authority.

### Failure drill

Failure: CLI report is used as automatic approval.

Evidence: Teams skip stakeholder/risk review because recommendation says "pilot."

Fix: Add approval owner and review sign-off outside the CLI.

Prevention: Report language remains advisory and includes validation findings.

### Production note

Operational path for discovery:

- version every package;
- review changes through pull requests;
- keep sensitive examples out of artifacts;
- record decisions in a decision log;
- revisit assumptions after the pilot;
- rollback to non-AI process if stop conditions trigger.

### Guided practice and independent transfer

- Guided: Run the CLI, then change `adoption_rate` and explain how the report changes.
- Independent transfer: Create a second package for "AI-assisted policy search" and compare recommendations.

### Recall

- What does the CLI prove?
- What does it not prove?
- Why keep recommendations advisory?
- What belongs in the decision log?

### Final cumulative retrieval: complete discovery path

Closed book, reconstruct:

```text
request -> outcome -> workflow -> baseline -> candidates -> risk controls -> ROI -> ADR -> pilot plan
```

Then answer:

- Where could a non-AI solution win?
- Which actions are prohibited?
- Which metric would stop the pilot?
- Which owner approves the pilot?

## Reference glossary

| Term | Meaning |
|---|---|
| Abstention | Choosing not to answer or act when evidence is missing or risk is too high. |
| Adoption metric | A measure of whether users actually use the workflow. |
| Baseline | Current-state measurement before the intervention. |
| Bottleneck | Workflow step that limits speed, quality, cost, or capacity. |
| Build/buy/hybrid | Decision between internal build, managed/vendor solution, or combined path. |
| Counterfactual | What would happen without the AI system. |
| Decision support | System assists a person but does not take final action. |
| Human approval | Explicit human authorization before a consequential action. |
| Human review | Human checks model output before use. |
| Pilot | Limited trial with scope, metrics, controls, and stop conditions. |
| Risk register | Artifact listing risks, controls, owners, detection, and responses. |
| Workflow map | Current-state sequence of actors, systems, inputs, outputs, time, and failures. |

## Full test suite

Command:

```bash
pytest
```

Expected result:

```text
all tests pass
```

Test map:

| Test file | Proves |
|---|---|
| `test_schemas.py` | Use-case fields and validation constraints work. |
| `test_scoring.py` | ROI, risk/readiness, and recommendations respond to assumptions. |
| `test_artifacts.py` | Discovery package completeness checks work. |
| `test_cli.py` | YAML package loads and JSON report is produced. |

What this suite proves:

- The package is structurally valid.
- Calculations are reproducible.
- Missing required artifacts are detectable.
- CLI output is machine-readable.

What this suite does not prove:

- The ROI assumptions are true.
- Users will adopt the workflow.
- A future model will meet quality targets.
- Legal, regulatory, or customer-risk review is complete.

## Experiment playbook

| Experiment | Input | Settings | Metric | Expected evidence | Failure signal |
|---|---|---|---|---|---|
| Baseline sensitivity | Same package with lower minutes saved | Adoption 60%, savings 1 min | Net value | Recommendation becomes weaker | Recommendation never changes |
| Risk control | Same use case with automation | autonomy 5, consequence 5 | Recommendation | Rejects without human control | Automation still approved |
| Readiness gap | Low evidence/data scores | readiness fields 1-2 | Recommendation | Research before pilot | Pilot still recommended |
| Non-AI alternative | Process/search-only candidate | lower cost | Comparative memo | AI not assumed necessary | Non-AI option ignored |
| Stop condition review | Remove "Stop" metric | success metrics incomplete | Validation finding | Finding is raised | Package passes silently |

## Evaluation and acceptance

Held-out evidence for the real pilot should include:

- baseline ticket sample;
- current handle-time measurements;
- QA sample of unsupported claims;
- escalation-rate sample;
- agent interview notes;
- customer-impact categories.

Functional metrics:

- discovery package validates;
- selected use case exists;
- risk register has owners;
- non-AI fallback exists;
- rejected alternatives documented.

Business metrics:

- handle-time reduction;
- escalation-rate change;
- QA error-rate change;
- adoption rate;
- review burden.

Safety/security gates:

- no autonomous refund or account actions;
- no customer-facing output without human review;
- no real PII in lesson artifacts;
- stop conditions defined.

Acceptance threshold:

```text
Proceed to Lesson 08/09 implementation only when:
selected pilot is narrow,
baseline exists,
high-impact actions require human approval,
non-AI fallback exists,
and go/revise/stop criteria are documented.
```

## System-decision memo

Decision: pursue a controlled discovery-to-pilot path for evidence-backed support response drafting.

Candidate or design: hybrid workflow using improved search/templates plus future model-assisted drafting for agent review.

Evidence:

- Refund tickets have high volume.
- Policy lookup and drafting create measurable time cost.
- Unsupported refund language creates review cost.
- Human approval can control customer-impact risk.

Measured strengths:

- Clear user task.
- Reviewable output.
- Existing support workflow can host a controlled pilot.

Measured failures or blocked risks:

- Data quality and policy evidence must be verified before model implementation.
- Autonomous refund action is rejected.
- ROI remains scenario-based until pilot results exist.

Cost/latency notes:

- Discovery uses estimated model operating cost.
- Future lessons will measure token cost and model latency.

Privacy/security notes:

- Use synthetic data in lesson artifacts.
- Real pilot must use approved data handling and access controls.

Operational notes:

- Start in shadow mode.
- Keep non-AI fallback.
- Track stop conditions weekly.

Decision: proceed to foundation-model literacy and model-behavior evaluation, not production deployment.

Next experiment: in Lesson 08, compare candidate model behavior on safe support-drafting cases.

## Failure modes and debugging

| Symptom | Likely causes | Diagnostic evidence | Corrective action | Prevention |
|---|---|---|---|---|
| AI use case has no clear value | Started from model capability | No baseline or workflow step | Reframe around user task | Require baseline before model work |
| ROI is implausibly high | Double-counted savings or omitted oversight | Cost review finds missing review work | Add conservative scenarios | Finance review |
| Users reject pilot | Workflow not mapped from real work | Agents use workaround outside system | Re-interview and redesign | Include users from discovery |
| High-risk action slips into scope | Poor human-control design | PRD allows auto-send or refund action | Move to prohibited or approval path | Control-mode review |
| Pilot cannot be evaluated | Metrics not defined upfront | No go/revise/stop rules | Define metric hierarchy | Release gate |
| Legal/security blocks late | Stakeholders missed | Review happens after implementation | Add early risk review | Stakeholder map includes governance |

## Security, privacy, and governance

Controls tied to this lesson:

- Discovery artifacts use synthetic or aggregated examples.
- Real customer tickets require approved access and retention policy.
- Human approval is mandatory for refund commitments.
- Authorization and approval are product controls, not model instructions.
- Risk register must name owner, detection, prevention, and response.
- Non-AI fallback is required.
- Decision logs record who approved scope and when.

Do not include real names, emails, phone numbers, account IDs, payment details, or proprietary customer content in the lesson package.

## Performance and cost

Discovery cost includes:

- stakeholder interview time;
- workflow measurement;
- analyst/engineering time;
- legal/security review;
- pilot planning.

Future model operating cost should include:

- provider or infrastructure cost;
- token usage;
- evaluation and monitoring;
- human review;
- maintenance;
- incident response;
- retraining or prompt updates where relevant.

Measurement procedure:

1. Estimate current volume and handling time from baseline.
2. Estimate adoption and minutes saved conservatively.
3. Estimate error avoidance separately.
4. Add implementation, recurring, and oversight costs.
5. Run conservative, expected, and downside scenarios.

## Deployment and operations

This lesson's "deployment" is a discovery operating path:

- store the package in version control;
- require review before pilot approval;
- run validation in CI;
- keep decision logs;
- run weekly pilot reviews;
- track go/revise/stop metrics;
- maintain fallback to the non-AI workflow.

Operational practice, not production AI deployment:

```text
discovery package
  -> validation
  -> review
  -> controlled pilot decision
  -> next lesson/model investigation
```

Rollback:

- stop the pilot;
- disable AI-assisted step;
- return to templates/search/manual review;
- preserve incident and evaluation records;
- revise risk controls before reattempting.

## Bridge to the next lesson

Lesson 08 assumes you can now:

- explain the selected support-drafting pilot;
- state why autonomous refund action is out of scope;
- define baseline, value, risk, and readiness assumptions;
- identify non-AI alternatives;
- explain why human approval is required;
- describe what model behavior must be tested before integration.

This is why Lesson 08 studies foundation-model behavior before Lesson 09 integrates hosted APIs.

## Practical assignment

### Scenario

A regional healthcare support team wants to use AI to triage patient portal messages. Leaders ask for "an AI assistant that handles routine messages."

### Requirements

- Map the current workflow.
- Interview at least three stakeholder roles.
- Define baseline metrics.
- Propose at least four candidate interventions.
- Reject at least two alternatives.
- Define risk register and human-control boundaries.
- Estimate value and cost.
- Write PRD, ADR, and pilot plan.

### Constraints

- No autonomous medical advice.
- No patient-facing output without clinician-approved workflow.
- Use synthetic examples only.
- Include non-AI fallback.

### Required artifacts

- Stakeholder map.
- Current-state workflow.
- Baseline metric table.
- Use-case register.
- Risk register.
- ROI scenario.
- Build/buy/hybrid decision.
- Pilot plan.
- Go/revise/stop criteria.

### Acceptance criteria

- AI use is tied to measurable workflow value.
- High-impact actions retain human approval.
- Non-AI fallback exists.
- Rejected alternatives have rationale.
- Metrics include safety and adoption.

### Stretch goals

- Add sensitivity analysis.
- Create a second package for a non-AI search/template improvement.
- Add CI validation for discovery package completeness.

## Interview preparation

### Concept questions

1. When should AI not be used?
   - Strong answer: when baseline is absent, deterministic/process fix suffices, data is unavailable, output cannot be reviewed, risk is high without control, or ownership is missing.
2. What is a useful baseline?
   - Strong answer: measured current-state value with source, window, owner, and known limitations.
3. Difference between decision support and automation?
   - Strong answer: decision support informs a human; automation takes action. Risk and approval requirements differ.

### Coding or implementation questions

1. Design a schema for a use-case register.
   - Include user, workflow step, value assumptions, risk dimensions, control mode, owner, and non-AI alternative.
2. Write a function that flags high-risk automation.
   - Strong answer separates risk score, control mode, and recommendation.

### Debugging questions

1. ROI is positive but pilot fails. What do you inspect?
   - Adoption, workflow fit, baseline quality, review burden, quality failures, omitted costs.
2. Scoring recommends pilot for every use case. What's wrong?
   - Thresholds or inputs are not sensitive; risk/readiness not separated; recommendation logic is weak.

### System-design question

Design the discovery-to-pilot process for AI-assisted support drafting.

Strong answer includes:

- stakeholder discovery;
- workflow map;
- baseline;
- candidate interventions;
- AI suitability;
- risk register;
- human approval;
- PRD/ADR;
- pilot stages;
- go/revise/stop metrics;
- fallback and rollback.

### Tradeoff questions

- Build versus buy for support drafting?
- RAG-assisted drafting versus direct LLM drafting?
- Shadow pilot versus live pilot?
- Human review versus human approval?
- Spreadsheet ROI versus versioned discovery package?

## Mastery check

### One-page memory model

```text
Request:
  "Use AI"

Discovery:
  user -> workflow -> baseline -> bottleneck

Options:
  process -> deterministic -> rules/search -> ML/LLM/RAG/tools/agent -> human/hybrid

Controls:
  risk dimensions -> review/approval/abstention/prohibited

Decision:
  value + readiness + risk + adoption + fallback

Artifacts:
  workflow map + baseline + use-case register + risk register + PRD + ADR + pilot plan
```

### Retrieval bank

- Explain why baseline comes before ROI.
- Draw the discovery funnel from request to pilot.
- Predict what happens if oversight cost is omitted.
- Diagnose a use case with no rejected alternatives.
- Compare decision support and automation.
- Transfer the framework to healthcare triage.
- Explain why non-AI fallback is mandatory.
- Describe a stop condition for the support-drafting pilot.
- Explain why high value does not erase high risk.
- Name three fields required in a risk register.

### Self-assessment

Rate 1-5:

- I can separate executive request from business problem.
- I can map workflow and failure paths.
- I can define baseline metrics.
- I can compare AI and non-AI options.
- I can design human-control boundaries.
- I can calculate and challenge an ROI scenario.
- I can write PRD/ADR/pilot artifacts.
- I can explain when to stop a pilot.

### Spaced-review plan

| Time | Retrieval task |
|---|---|
| 1 day | Recreate the discovery funnel and define each artifact. |
| 3 days | Recalculate ROI with a lower adoption scenario. |
| 1 week | Write a new risk register for a different workflow. |
| 3-4 weeks | Design a full discovery package for a new domain without looking at this lesson. |

## Production-readiness checklist

- [ ] Business outcome is measurable.
- [ ] User task and workflow step are named.
- [ ] Current-state workflow includes failure paths.
- [ ] Baseline metrics have source, window, and owner.
- [ ] Candidate interventions include non-AI alternatives.
- [ ] Rejected alternatives are documented.
- [ ] Risk register has owners and controls.
- [ ] Human review/approval/abstention/prohibited actions are explicit.
- [ ] ROI scenario includes implementation, recurring, and oversight cost.
- [ ] Adoption metrics are defined.
- [ ] PRD and ADR are written.
- [ ] Pilot has scope, stages, controls, and stop conditions.
- [ ] Non-AI fallback exists.
- [ ] Discovery package validates.
- [ ] Decision owner and risk owner have reviewed.
- [ ] Next-lesson handoff is clear.

## Lesson summary

You learned how to turn a broad AI request into a disciplined discovery package. The main result is not a model. It is an evidence-backed decision about whether to proceed, revise, or stop.

You built:

- typed discovery schemas;
- ROI/risk/readiness scoring;
- artifact completeness checks;
- a CLI report;
- a sample Northstar Support discovery package.

Important tradeoffs:

- AI versus process/search/template improvement;
- decision support versus automation;
- human review versus human approval;
- ROI optimism versus conservative scenarios;
- demo excitement versus go/no-go criteria.

What carries forward:

- Lesson 08 uses the selected support-drafting pilot to study foundation-model behavior.
- Lesson 09 integrates model APIs only after the problem, risk, and human-control boundaries are explicit.
- Lesson 10 turns prompt behavior into versioned, tested application components.

## Official references

- NIST AI Risk Management Framework 1.0: https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI RMF Playbook: https://airc.nist.gov/AI_RMF_Knowledge_Base/Playbook
- Local curriculum sources: `AI-Industry-Detailed-Lessons.md`, `AI-Industry-Detailed-Outline.md`, `AI-Industry-Complete-Lesson-Coverage-Map.md`, `AI-Industry-Curriculum.md`.
