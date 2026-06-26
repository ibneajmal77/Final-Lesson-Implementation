# Source Routing

## Purpose

Use the local curriculum files to determine scope, order, tools, business projects, role relevance, and expected depth before generating a lesson.

## Locate sources

The skill normally resides at:

```text
Final-Lesson-Implementation/
├── AI-Industry-Curriculum.md
├── AI-Industry-Detailed-Outline.md
├── AI-Industry-Detailed-Lessons.md
└── generate-ai-industry-lesson/
```

Resolve the following paths relative to the skill folder:

- `../AI-Industry-Detailed-Outline.md`
- `../AI-Industry-Detailed-Lessons.md`
- `../AI-Industry-Curriculum.md`

The files may be renamed or relocated. If a relative path is absent, search the parent directory for the closest corresponding filename before asking the user.

## Priority

Apply sources in this order:

- User's current request
- Detailed outline
- Detailed lesson plan
- Broad curriculum
- Current official external documentation

The user's explicit scope and output requirements override local defaults. Do not let an older curriculum statement override a current user instruction.

## Read selectively

For one lesson:

- Search the detailed outline for the exact topic and its parent section.
- Read the matching section, adjacent prerequisite topic, and next topic.
- Search the detailed lesson plan for the matching lesson title and read the complete entry.
- Read the broad curriculum only for role mapping, tool classification, capstone continuity, or missing context.

Do not load all curriculum files into context when targeted searches provide sufficient information.

## Use each source correctly

### Detailed outline

Use for:

- Complete topic and subtopic coverage
- Learning order
- Tools
- Role branches
- Portfolio sequence
- Interview scope

Do not turn the outline bullets directly into the final lesson. Expand and connect them.

### Detailed lesson plan

Use for:

- Employment outcome
- Business problem
- Objectives
- Required concepts
- Guided implementation
- Assignment
- Evaluation
- Production concerns
- Interview preparation

Treat it as a lesson contract, not finished prose.

### Broad curriculum

Use for:

- Industry rationale
- Role relationships
- Shared technology stack
- Required versus role-dependent tools
- Capstone architecture
- Job-readiness gates

## Missing topic

If the requested topic is not present:

- Find its nearest parent domain.
- Determine whether it is required by current industry roles.
- Verify current relevance with primary sources.
- Add only the minimum prerequisites and adjacent topics needed.
- State that the lesson is an extension to the existing curriculum.

Do not silently expand the curriculum with research-only material.

## Source integrity

- Do not overwrite any source file while generating a lesson.
- Preserve the user's ordering unless instructed otherwise.
- Do not copy large sections verbatim; synthesize them into a coherent chapter.
- Keep local file links correct in generated outputs.
