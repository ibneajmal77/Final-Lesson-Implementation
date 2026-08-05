# Model Gateway Baseline

Phase 01 baseline captured with the mock provider and local PostgreSQL.

| Measure | Baseline |
|---|---:|
| Successful chat request | 1 `ai_runs` row, status `succeeded` |
| Embedding request | vectors returned in input order |
| Retry behavior | timeout-once scenario succeeds with one `ai_runs` row and two attempts |
| Fallback behavior | unavailable primary route falls back once after policy revalidation |
| Cost tracking | token cost lines written to `cost_records` |

Run the current proof set with:

```bash
python -m alembic upgrade head
python -m pytest tests/model_gateway tests/migrations tests/api/test_model_gateway.py
python -m ruff check .
python -m mypy apps packages
```
