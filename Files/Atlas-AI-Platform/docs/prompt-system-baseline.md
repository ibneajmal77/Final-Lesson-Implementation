# Prompt System Baseline

Phase 02 baseline captured with local PostgreSQL and the mock provider.

| Measure | Baseline |
|---|---:|
| Prompt template creation | row in `prompt_templates` plus audit event |
| Prompt version creation | immutable `draft` row in `prompt_versions` |
| Draft activation | refused with `prompts.version_not_approved` |
| Approved activation | active version promoted and previous active demoted to `approved` |
| Activation audit | `audit_events` row with incoming and outgoing version metadata |
| Prompt tests | stored cases render and execute through the gateway mock provider |
| AI run attribution | `ai_runs.prompt_version_id` and prompt span attributes populated |
| Optimizer seam | candidate remains `draft` and cannot be approved or activated |

Run the current proof set with:

```bash
python -m alembic upgrade head
python -m pytest tests/prompts tests/api/test_prompts.py tests/migrations/test_phase02_migrations.py
python -m pytest
python -m ruff check .
python -m mypy apps packages
```
