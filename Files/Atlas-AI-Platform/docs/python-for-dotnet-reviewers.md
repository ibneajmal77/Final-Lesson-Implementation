# Python For .NET Reviewers

This project now has inline comments and module docstrings aimed at a reviewer
who knows .NET well but is new to Python.

Start here:

1. `apps/api/app.py` - FastAPI application factory, similar to `Program.cs` plus
   global exception middleware.
2. `apps/api/routes/` - HTTP route modules, similar to controllers.
3. `packages/core/` - settings, errors, logging, and request context.
4. `packages/db/` - SQLAlchemy engine/session setup, ORM models, and Alembic
   migrations. Read this like EF Core models plus migrations.
5. `packages/model_gateway/` - route selection, provider adapters, AI run ledger,
   redaction, retries, fallback, and cost estimates.
6. `packages/prompts/` - prompt templates, immutable versions, rendering,
   approval/activation lifecycle, audit events, and prompt tests.
7. `tests/` - pytest tests. Function names starting with `test_` are discovered
   automatically, and fixtures are injected by parameter name.

Useful Python-to-.NET translations:

- `__init__.py` marks a directory as an importable package.
- `def` declares a function or method.
- `self` is the explicit instance parameter, similar to `this`.
- `async def` declares an awaitable function.
- `@decorator` attaches framework behavior to a function/class, similar to an
  attribute plus registration logic.
- `T | None` is a nullable type hint.
- `list[T]`, `tuple[T, ...]`, and `dict[K, V]` are generic type hints.
- `@dataclass(frozen=True)` is close to an immutable C# record.
- Pydantic `BaseModel` classes are validated API DTOs.
- SQLAlchemy `Mapped[...] = mapped_column(...)` is the ORM column mapping style.
- `with ... as ...` is a context manager, similar to C# `using`.
- `yield` in FastAPI dependencies means setup runs before the endpoint and
  cleanup runs after it.
