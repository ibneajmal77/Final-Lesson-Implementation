# Phase 02 Prompt System Decisions

Phase 02 implements the prompt system without taking on Phase 07 evaluation storage or Phase 20 optimizer jobs.

## Decisions

- `audit_events` is created in Phase 02 because prompt activation needs a durable promotion record and no earlier migration owned the table.
- Prompt rendering uses strict placeholder substitution for `${name}` and `{{ name }}`. Jinja-style control flow is intentionally not added.
- Prompt versions use the five persisted statuses from the schema: `draft`, `testing`, `approved`, `active`, and `retired`.
- Test cases attach to templates, not versions, so the same cases can compare an active baseline and a candidate version.
- The database enforces one active version per template with `uq_prompt_versions_one_active`.
- `ai_runs.prompt_version_id` is hardened with a foreign key once `prompt_versions` exists.
- Optimizer-created versions are drafts only. The optimizer seam cannot approve or activate, and approval also refuses optimizer-created versions.

## Deferred

- Prompt optimization job and candidate tables are Phase 20 work.
- Stored evaluation runs, judge scores, statistical comparisons, and trend history are Phase 07 work.
- Structured-output enforcement for `output_schema_json` and `expected_output_json` is Phase 03 work.
