# Phase 00 - Engineering Foundation

## 1. Phase Purpose

Phase 00 builds the professional engineering foundation for the Atlas AI Platform.

This phase does not start with LLM calls, RAG, agents, fine-tuning, or advanced AI features. That is intentional. A serious Gen AI system needs a strong backend foundation before model calls are added. Without this foundation, the project becomes a fragile chatbot demo instead of an industry-ready AI platform.

The purpose of Phase 00 is to create the project skeleton, development environment, backend API foundation, configuration system, database connection, migration system, logging, error handling, testing setup, Docker environment, and clean module boundaries.

Everything later depends on this phase:

- The LLM gateway needs configuration, logging, retries, and tests.
- RAG needs database tables, background jobs, and storage boundaries.
- Agents need state persistence, audit logs, and service-layer rules.
- Tool calling needs validation, authorization, and error handling.
- Evaluation needs reproducible tests and data models.
- Safety needs request tracing and policy enforcement points.
- Deployment needs Docker, health checks, config, logs, and migration discipline.

If Phase 00 is weak, every later AI feature becomes harder to build, debug, test, and explain in interviews.

## 2. What This Phase Builds

By the end of Phase 00, the project should have:

- A clean repository structure.
- A Python package layout.
- A FastAPI backend app.
- A health endpoint.
- Typed configuration management.
- Environment variable loading.
- Structured error handling.
- Structured logging.
- Request id or trace id support.
- PostgreSQL database connection.
- SQLAlchemy setup.
- Alembic migration setup.
- Basic database base model conventions.
- Redis connection placeholder.
- Worker application skeleton.
- Test setup with pytest.
- Unit and integration test folders.
- Docker Compose for local infrastructure.
- Code quality tools.
- A clear rule for where future Gen AI modules will fit.

This phase is complete only when a developer can run the system locally, call the health endpoint, run tests, run database migrations, and understand where new features belong.

## 3. Beginner-Friendly Definition Of Engineering Foundation

An engineering foundation is the base structure that allows a software product to grow safely.

A weak foundation is when code is placed anywhere, settings are hard-coded, errors are random, tests are missing, database changes are manual, and logs are hard to read.

A strong foundation is when:

- Code has clear folders.
- Configuration is centralized.
- APIs have predictable responses.
- Database changes are versioned.
- Errors are consistent.
- Logs explain what happened.
- Tests can run automatically.
- Local development is repeatable.
- Future modules can be added without rewriting the whole project.

For an AI platform, this foundation matters even more because AI features introduce extra uncertainty:

- Model output can be inconsistent.
- Provider APIs can fail.
- Prompts can regress.
- Retrieval can return wrong context.
- Agents can choose wrong tools.
- Token cost can spike.
- Safety checks can block or miss risky behavior.

The foundation gives you the control points to handle these problems.

## 4. Real Industry Example

Imagine a company builds a support AI assistant.

Bad version:

```text
One Python file
-> receives user question
-> sends question directly to LLM
-> returns response
```

This works for a demo, but it cannot answer serious production questions:

- Which customer tenant asked this?
- Which model answered?
- What did it cost?
- What prompt was used?
- Was the answer logged?
- Did the system check permissions?
- Was the database migration applied?
- Can the team reproduce the bug?
- Can tests run without calling the real LLM?
- Can the system be deployed safely?

Good version:

```text
FastAPI request
-> request id assigned
-> config loaded
-> auth placeholder resolved
-> service function called
-> database session managed
-> response schema validated
-> structured logs written
-> errors formatted consistently
-> tests cover behavior
```

This good version is what Phase 00 creates.

## 5. What You Must Understand Before Coding

Before coding this phase, understand these core concepts.

### 5.1 Repository

A repository is the folder that contains the project source code, tests, configuration, documentation, and infrastructure files.

Example:

```text
atlas-ai-platform/
  apps/
  packages/
  tests/
  infra/
  docs/
```

The repository should tell a developer where things belong.

### 5.2 Application

An application is a runnable entry point.

In Atlas, examples are:

- API app.
- Worker app.
- Evaluation runner app.
- Model server app.
- Web app.

In Phase 00, we create the API app and worker skeleton first.

### 5.3 Package

A package is reusable code grouped by responsibility.

Examples:

- `packages/core` for shared utilities.
- `packages/db` for database setup.
- `packages/auth` for authentication later.
- `packages/model_gateway` for LLM calls later.

Packages prevent random code mixing.

### 5.4 Module

A module is a Python file inside a package.

Example:

```text
packages/core/config.py
packages/core/errors.py
packages/db/session.py
```

Each module should have one clear purpose.

### 5.5 API

An API is the contract between frontend or external clients and backend code.

Example health endpoint:

```text
GET /api/v1/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "atlas-api",
  "environment": "local"
}
```

### 5.6 Configuration

Configuration means environment-specific values used by the application.

Examples:

```text
DATABASE_URL
REDIS_URL
LOG_LEVEL
APP_ENV
OPENAI_API_KEY later
```

Configuration should not be hard-coded in business logic.

### 5.7 Environment Variable

An environment variable is a value provided outside the code.

Example:

```text
DATABASE_URL=postgresql+psycopg://atlas:atlas@localhost:5432/atlas
```

The same code can run locally, in staging, and in production by changing environment variables.

### 5.8 Database Migration

A database migration is a versioned change to the database schema.

Example:

- Add `tenants` table.
- Add `users` table.
- Add `documents` table later.

Alembic is commonly used with SQLAlchemy to manage migrations.

### 5.9 Structured Logging

Structured logging means logs are written as machine-readable fields instead of random text.

Bad log:

```text
Something failed
```

Good log:

```json
{
  "level": "error",
  "event": "request_failed",
  "request_id": "req_123",
  "path": "/api/v1/health",
  "error_code": "internal_error"
}
```

Structured logs are important for production debugging.

### 5.10 Error Handling

Error handling means converting failures into consistent responses.

Example:

```json
{
  "error": {
    "code": "config.invalid",
    "message": "Application configuration is invalid.",
    "request_id": "req_123"
  }
}
```

Later, when an LLM fails, RAG fails, or an agent tool fails, the same error system will be used.

### 5.11 Test

A test is code that proves expected behavior.

Test examples:

- Health endpoint returns 200.
- Config loads correctly.
- Invalid config fails.
- Error envelope shape is correct.
- Database connection works.

For Gen AI, tests become even more important because AI behavior can change.

## 6. Concepts You Cannot Learn From The Code

Section 5 was vocabulary. This is the reasoning underneath it.

None of this appears in a file. You can build every item in Phase 00 correctly and still not know why the API is versioned, why `pool_pre_ping` exists, or why a health check that queries the database can take down a healthy service. Each rule in this phase comes from an idea with a name, and knowing the name is what lets you apply the rule somewhere this document never mentions.

### 6.1 The Twelve-Factor App

Most of Phase 00's configuration rules come from one well-known set of principles for building services that deploy repeatably. The ones this phase applies:

| Principle | How Phase 00 applies it |
|---|---|
| **Config in the environment** | Settings come from environment variables, never from code |
| **Strict dev/prod parity** | The same code runs in local, test, staging, production — only config differs |
| **Explicit dependencies** | `pyproject.toml` declares everything; nothing relies on what happens to be installed |
| **Backing services are attached resources** | Postgres and Redis are URLs, so swapping local for managed is a config change |
| **Logs are event streams** | The app writes to stdout; it does not manage log files or rotation |
| **Processes are stateless** | Nothing important lives in process memory, so any instance can serve any request |
| **Disposability** | Fast startup, graceful shutdown — see 6.7 |

"Environment parity" is the one beginners underestimate. Every difference between your machine and production is a category of bug that can only be found in production. This is the actual argument for Docker Compose in Phase 00 — not convenience, but shrinking the gap.

### 6.2 Coupling And Cohesion

Section 9 argues for package boundaries. These are the two words that make the argument precise.

**Cohesion** is how strongly the things inside one module belong together. **Coupling** is how much one module depends on the internals of another. The goal is always high cohesion, low coupling.

```text
Low cohesion:   utils.py containing date math, an HTTP client, and a password hasher
High cohesion:  packages/core/config.py containing only configuration

High coupling:  packages/db imports from apps/api/routes to read a request object
Low coupling:   apps/api calls packages/db through a documented function
```

This is why the phase states that `apps/api` may call packages but packages must not import route files. That rule is not style — a cycle between modules means neither can be tested, reused, or extracted alone. When Phase 01 puts every provider call behind one package, it is buying low coupling: the rest of the platform depends on an interface, not on a vendor.

### 6.3 ACID And Transaction Boundaries

Databases give four guarantees, and knowing them tells you what you must handle yourself.

- **Atomicity** — all of a transaction happens, or none of it does.
- **Consistency** — constraints hold before and after.
- **Isolation** — concurrent transactions do not see each other's partial work.
- **Durability** — committed data survives a crash.

Isolation is the one with a dial. PostgreSQL defaults to *read committed*: you only see committed data, but two reads inside one transaction can return different results if someone else commits between them. Stricter levels exist and cost concurrency.

The practical rule: **a transaction should cover one unit of business meaning, and nothing slow.** Later phases make this concrete and expensive — Phase 01 explicitly forbids holding a transaction open across a model call, because a 30-second network wait would pin a database connection the whole time.

### 6.4 Connection Pools And Why They Exhaust

Opening a database connection is expensive, so a pool keeps a set open and lends them out. `pool_size` is how many are kept; `max_overflow` is how many extra may be opened under load.

Pool exhaustion is one of the most common production failures, and its symptom is misleading: requests hang rather than error. It happens when connections are borrowed and not returned — a session left unclosed, or a transaction held open across a slow external call.

`pool_pre_ping` exists because a pooled connection can be silently dead: a database restart or an idle-timeout firewall kills it, the pool does not notice, and the next borrower gets a broken socket. Pre-ping tests the connection before lending it.

This is the mechanism behind the phase's rule to use one central session dependency rather than creating sessions freely. Scattered sessions are how connections leak.

### 6.5 The N+1 Query Problem

Fetch 100 documents, then loop and fetch each one's owner: that is 1 query plus 100 more. It looks fine on ten rows in development and falls over on ten thousand in production.

It is worth knowing in Phase 00 even though there are no queries yet, because ORMs cause it by default — lazy loading makes the extra queries invisible in the code. The fix is to load related data deliberately in one query. The habit to build now is *counting queries*, not just checking that results look right.

### 6.6 API Versioning And Backward Compatibility

The phase mandates `/api/v1` without saying why. The why is that published interfaces cannot change freely once anyone depends on them.

**Semantic versioning** communicates intent in a version number: MAJOR for breaking changes, MINOR for backward-compatible additions, PATCH for fixes. A URL prefix like `/api/v1` is the MAJOR component made visible.

What counts as breaking is narrower than people expect:

| Change | Breaking? |
|---|---|
| Adding an optional response field | No |
| Adding a required request field | **Yes** |
| Removing or renaming a response field | **Yes** |
| Making validation stricter | **Yes** — previously accepted requests now fail |
| Changing an error code's meaning | **Yes** — clients branch on codes |

That last row is why the phase insists error codes are stable while messages may change. It is also why Phase 01 defines a fixed error-code catalogue: a frontend that shows a "retry" button for `ai.provider_timeout` is depending on that string as much as on any field.

### 6.7 Graceful Shutdown And Health Check Semantics

When a container platform stops your process it sends SIGTERM, waits, then sends SIGKILL. That gap is your chance to finish in-flight requests, close connections, and exit cleanly. Ignoring it means every deploy drops live requests.

This is the other half of why liveness and readiness are separate endpoints:

- **Liveness** answers "is this process alive?" If it fails, the platform **restarts** you.
- **Readiness** answers "should traffic come here right now?" If it fails, the platform **stops sending traffic** but leaves you running.

Confusing them causes a specific and nasty outage. If liveness checks the database and the database has a brief hiccup, every instance reports unhealthy, every instance is killed and restarted simultaneously, and a recoverable database blip becomes a total outage. Readiness may check dependencies. Liveness must not.

Readiness is also what makes zero-downtime deploys possible: a new instance stays out of rotation until it reports ready.

### 6.8 The Testing Pyramid And Test Doubles

The pyramid describes proportion: many fast unit tests, fewer integration tests, very few end-to-end tests. Fast tests get run; slow tests get skipped, and a skipped test protects nothing.

The vocabulary for fake objects is worth precision, because Phase 01 depends on the last one:

| Double | What it does |
|---|---|
| **Stub** | Returns canned answers |
| **Fake** | A real but simplified implementation |
| **Mock** | Asserts that it was called correctly |
| **Spy** | Records calls for later inspection |

Phase 01's mock provider is really a *fake* — a working implementation that returns deterministic responses and simulates timeouts and outages. That distinction matters: a stub cannot simulate a timeout, and simulating failure is the entire reason it exists.

Two properties make tests trustworthy, and both are set up in this phase: **isolation** (tests do not share state or depend on order) and **determinism** (same input, same result, every run). A flaky test is worse than no test — it trains the team to ignore red.

### 6.9 Observability: Three Pillars, And Cardinality

- **Logs** — discrete events. What happened.
- **Metrics** — aggregated numbers over time. How much, how often, how slow.
- **Traces** — one request's path across components. Where the time went.

Phase 00 builds logs and the correlation id that later makes traces possible. Phase 01 adds metrics and span attributes.

The concept that stops a costly mistake is **cardinality**: the number of distinct values a label can take. Metrics are cheap because they aggregate. Adding a label with unbounded values — user id, request id, full URL — creates a separate time series per value and can overwhelm a metrics backend.

```text
Safe label:      status_code, route_key, provider_name   (tens of values)
Dangerous label: user_id, request_id, ai_run_id          (unbounded)
```

High-cardinality identifiers belong in logs and traces, which are built for them. This is why Phase 01's metrics are labelled by route and provider, while `ai_run_id` appears only in log lines and span attributes.

### 6.10 Security Principles Behind The Config Rules

**Least privilege** — every component gets the minimum access it needs. The application's database user does not need permission to drop tables.

**Defense in depth** — no single control is trusted alone. Secrets stay out of code *and* out of logs *and* out of error responses.

**Secret rotation** — credentials must be replaceable without a code change. This only works if secrets are read from the environment, which is the operational reason behind the rule, beyond "hard-coding is bad".

**Blast radius** — the damage one compromise causes. A leaked provider key is bad; a leaked key that also grants billing access is worse. This is why Phase 01 scopes credentials per provider rather than sharing one.

### 6.11 Migration Discipline: Expand And Contract

Schema changes and code deploys are not simultaneous. For a moment, old code runs against a new schema, or the reverse. A migration that is safe alone can break that window.

The pattern is **expand and contract**:

```text
Expand:   add the new column, nullable, write to both old and new
Migrate:  backfill existing rows
Contract: switch reads to the new column, then drop the old one
```

Three deploys instead of one, and no downtime. Renaming a column in a single migration guarantees that whichever runs first — code or migration — is broken until the other catches up.

This is why the phase insists migrations are reviewed like code, and why Phase 01's deferred foreign keys use exactly this shape: create the column as a nullable soft reference, then harden it into a constraint in a later migration once the referenced table exists.

### 6.12 The Six To Carry Forward

```text
1. Config in the environment, parity across envs -> the whole settings design
2. High cohesion, low coupling                   -> package boundaries and the no-cycles rule
3. Transactions stay short and mean one thing    -> never hold one across a network call
4. Liveness restarts you; readiness reroutes     -> never check dependencies in liveness
5. Fast, isolated, deterministic tests get run   -> the fake provider Phase 01 depends on
6. Expand and contract                           -> every schema change from here on
```

If a rule in Sections 13 through 23 looks like arbitrary ceremony, its reason is almost always here.

## 7. Business Perspective

From a business perspective, Phase 00 proves that the project is not a toy.

Companies care about:

- Can this system be maintained by a team?
- Can it be deployed repeatedly?
- Can errors be debugged?
- Can database changes be tracked?
- Can new features be added safely?
- Can we control costs later?
- Can we audit behavior later?
- Can we test before release?

Phase 00 creates the skeleton that supports those business concerns.

Business value of this phase:

- Reduces future technical debt.
- Makes onboarding easier.
- Reduces production failure risk.
- Makes architecture explainable.
- Creates confidence before adding expensive AI calls.

## 8. User Perspective

The end user does not directly care about package layout, Docker, Alembic, or pytest.

But the user benefits because:

- The app starts reliably.
- Errors are understandable.
- Requests do not randomly fail.
- Later AI features can be trusted more.
- Uploads, chat, agents, and evaluation dashboards will have a stable backend.

In Phase 00, the visible user-facing feature is small:

```text
The system is online and healthy.
```

That health check is the first proof that the backend is running.

## 9. Architecture Perspective

### 9.1 Why Modular Monolith

Section 6.2 gives the vocabulary this argument rests on: high cohesion, low coupling.

Atlas starts as a modular monolith.

Definition:

A modular monolith is one deployable backend application with clear internal module boundaries.

It is not a messy monolith. It has separate packages for separate responsibilities.

Why this is the right first architecture:

- One developer can run it locally.
- Debugging is simpler.
- Database transactions are easier.
- No network calls between internal services yet.
- You still learn clean architecture.
- Later, packages can be extracted into services if needed.

Initial runtime:

```text
web frontend
api backend
worker backend
postgres
redis
vector database later
```

### 9.2 Foundation Architecture Diagram

```text
Developer
  -> runs Docker Compose
      -> PostgreSQL
      -> Redis
  -> starts API app
      -> loads settings
      -> configures logging
      -> connects database
      -> registers routes
      -> exposes health endpoint
  -> runs tests
      -> unit tests
      -> integration tests
```

### 9.3 Where Phase 00 Fits In The Full Atlas System

Phase 00 is under every later phase.

```text
Phase 00 Foundation
  -> Phase 01 Model Gateway
  -> Phase 02 Prompt System
  -> Phase 03 Structured Outputs
  -> Phase 04 Ingestion
  -> Phase 05 Embeddings
  -> Phase 06 RAG
  -> Phase 07 Evaluation
  -> Phase 08 Tool Calling
  -> Phase 09 Agents
  -> Phase 10 Memory
  -> Phase 11 Safety
  -> later phases
```

Every later module imports from the foundation:

- `core.config`
- `core.errors`
- `core.logging`
- `db.session`
- `db.models`
- `tests.fixtures`

### 9.4 Architectural Boundaries

Phase 00 should establish these boundaries:

```text
apps/api owns HTTP routes and request handling.
apps/worker owns background job entry point.
packages/core owns shared infrastructure utilities.
packages/db owns database setup and migrations.
packages/auth will own users, tenants, roles later.
packages/model_gateway will own model calls later.
packages/retrieval will own embeddings, vector search, hybrid search, and reranking later.
packages/rag will own RAG answer orchestration, grounding, and citations later.
packages/agents will own agent workflows later.
```

Important rule:

`apps/api` can call packages. Packages should not depend on API route files.

This avoids circular design.

## 10. Technical Scope Of Phase 00

### 10.1 In Scope

Build now:

- Project root files.
- Python dependency management.
- FastAPI app startup.
- Health endpoint.
- Settings class.
- Environment variable loading.
- Logging setup.
- Request id middleware.
- Error envelope.
- Database connection.
- SQLAlchemy base.
- Alembic setup.
- Basic migration.
- Redis client placeholder.
- Worker entry point.
- Test configuration.
- Docker Compose.
- README setup instructions.

### 10.2 Out Of Scope

Do not build yet:

- LLM provider calls.
- Prompt management.
- RAG.
- Agents.
- Tool calling.
- File upload.
- Embeddings.
- Fine-tuning.
- Model serving.
- Multimodal.
- Voice.

However, Phase 00 must prepare clean places for those future modules.

## 11. Recommended Libraries And Why

### 11.1 Python

Python is the main backend language.

Why:

- Strong AI ecosystem.
- Strong API ecosystem.
- Easy integration with ML libraries.
- Common in Gen AI engineering jobs.
- Works with FastAPI, Pydantic, SQLAlchemy, PyTorch, Transformers, and evaluation tools.

### 11.2 FastAPI

FastAPI is used for the backend API.

Why:

- Modern Python web framework.
- Good async support.
- Uses Pydantic for schemas.
- Generates OpenAPI docs.
- Common in AI backend projects.
- Easy to test.

Used in Phase 00 for:

- Creating the API app.
- Health endpoint.
- Middleware.
- Error handlers.

### 11.3 Pydantic

Pydantic is used for validation and settings.

Why:

- Validates API request/response schemas.
- Validates environment settings.
- Later validates structured LLM outputs.
- Reduces bugs from wrong data shapes.

Used in Phase 00 for:

- Settings class.
- API response schemas.
- Error envelope schemas.

Later used for:

- Tool schemas.
- Agent plans.
- Structured AI outputs.
- Evaluation result schemas.

### 11.4 SQLAlchemy

SQLAlchemy is used for relational database access.

Why:

- Industry-standard Python ORM.
- Works with PostgreSQL.
- Supports transactions.
- Integrates with Alembic.
- Lets you map database tables to Python classes.

Used in Phase 00 for:

- Database engine.
- Session management.
- Base model.

### 11.5 Alembic

Alembic is used for database migrations.

Why:

- Tracks schema changes.
- Allows repeatable database setup.
- Prevents manual database drift.
- Standard with SQLAlchemy.

Used in Phase 00 for:

- Initial migration setup.
- Creating base database metadata.

### 11.6 PostgreSQL

PostgreSQL is the primary database.

Why:

- Reliable relational database.
- Strong JSON support.
- Good indexing.
- Works with pgvector later.
- Common in production systems.

Used in Phase 00 for:

- Connection setup.
- Migration testing.

Later used for:

- Tenants.
- Users.
- Documents.
- AI runs.
- Agents.
- Evaluations.
- Safety logs.

### 11.7 Redis

Redis is used for cache, queues, rate limits, and temporary state.

Why:

- Fast in-memory store.
- Common for queues.
- Useful for request throttling.
- Useful for background workers.

Used in Phase 00 for:

- Connection placeholder.
- Docker Compose service.

Later used for:

- Worker queue.
- Rate limiting.
- idempotency keys.
- temporary agent state.

### 11.8 pytest

pytest is used for automated tests.

Why:

- Simple and powerful.
- Standard in Python projects.
- Supports fixtures.
- Works for unit and integration tests.

Used in Phase 00 for:

- Health endpoint test.
- Settings test.
- Error handling test.

### 11.9 httpx

httpx is used as an HTTP client.

Why:

- Supports sync and async usage.
- FastAPI tests often use HTTP clients.
- Later used for model provider calls and external tools.

Used in Phase 00 for:

- API testing support.

### 11.10 ruff

ruff is used for linting and formatting checks.

Why:

- Very fast.
- Replaces many Python lint tools.
- Helps keep style consistent.

Used in Phase 00 for:

- Code quality baseline.

### 11.11 mypy Or pyright

Type checking helps catch errors before runtime.

Why:

- AI systems pass many structured objects around.
- Type errors become expensive later.
- Tool schemas and structured outputs benefit from strong typing.

Used in Phase 00 for:

- Basic type-checking foundation.

### 11.12 Docker And Docker Compose

Docker packages services into containers. Docker Compose runs multiple services locally.

Why:

- Repeatable local environment.
- Easy Postgres and Redis setup.
- Similar to production container deployment.

Used in Phase 00 for:

- Running Postgres.
- Running Redis.
- Optionally running API and worker.

## 12. Folder Structure To Create

Recommended Phase 00 structure:

```text
atlas-ai-platform/
  README.md
  pyproject.toml
  .env.example
  .gitignore
  docker-compose.yml

  apps/
    api/
      __init__.py
      main.py
      lifespan.py
      middleware/
        __init__.py
        request_id.py
      routes/
        __init__.py
        health.py
      schemas/
        __init__.py
        health.py
        errors.py
      dependencies/
        __init__.py
        database.py

    worker/
      __init__.py
      main.py
      jobs/
        __init__.py

  packages/
    core/
      __init__.py
      config.py
      errors.py
      logging.py
      ids.py
      time.py
      result.py

    db/
      __init__.py
      base.py
      session.py
      models/
        __init__.py
      repositories/
        __init__.py
      migrations/
        env.py
        script.py.mako
        versions/

    auth/
      __init__.py

    model_gateway/
      __init__.py

    prompts/
      __init__.py

    ingestion/
      __init__.py

    retrieval/
      __init__.py

    rag/
      __init__.py

    agents/
      __init__.py

    tools/
      __init__.py

    safety/
      __init__.py

    evals/
      __init__.py

    observability/
      __init__.py

  tests/
    conftest.py
    unit/
      test_config.py
      test_errors.py
    integration/
      test_health_api.py
      test_database.py

  infra/
    docker/
    ci/

  docs/
    architecture/
    runbooks/
    decisions/
```

## 13. File Responsibilities

### 13.1 `apps/api/main.py`

Purpose:

- Create FastAPI app.
- Register middleware.
- Register routes.
- Register error handlers.
- Attach lifespan startup/shutdown.

Should contain:

- `create_app()` function.
- App metadata.
- Route registration.

Should not contain:

- Business logic.
- Direct database queries.
- Direct model calls.
- Hard-coded config.

### 13.2 `apps/api/routes/health.py`

Purpose:

- Expose health endpoints.

Endpoints:

```text
GET /api/v1/health
GET /api/v1/health/live
GET /api/v1/health/ready
```

Definitions:

- Liveness means the process is running.
- Readiness means the app can serve traffic because dependencies are available.

Readiness should eventually check:

- Database connection.
- Redis connection.
- Required configuration.

### 13.3 `apps/api/middleware/request_id.py`

Purpose:

- Add a request id to every request.
- Return request id in response header.
- Make request id available to logs.

Why important:

When an AI response fails later, you need to connect frontend error, backend log, AI run, retrieval trace, and tool call trace.

### 13.4 `apps/api/schemas/errors.py`

Purpose:

- Define standard API error response shape.

Example:

```json
{
  "error": {
    "code": "internal_error",
    "message": "Something went wrong.",
    "details": {},
    "request_id": "req_123"
  }
}
```

### 13.5 `packages/core/config.py`

Purpose:

- Define typed application settings.
- Load values from environment variables.
- Validate required configuration.

Future importance:

- Model provider keys.
- Model route settings.
- Token limits.
- Cost budgets.
- Safety policy toggles.
- Deployment environment.

### 13.6 `packages/core/errors.py`

Purpose:

- Define application exceptions.
- Give every error a code.
- Separate expected domain errors from unexpected system errors.

Example error categories:

```text
validation_error
not_found
permission_denied
conflict
rate_limited
external_provider_failed
ai_output_invalid
safety_blocked
```

### 13.7 `packages/core/logging.py`

Purpose:

- Configure structured logs.
- Add environment, service name, request id, and trace id.

Future importance:

- AI run debugging.
- Agent trace debugging.
- Retrieval debugging.
- Cost monitoring.

### 13.8 `packages/db/session.py`

Purpose:

- Create database engine.
- Create session factory.
- Provide dependency for API requests.

### 13.9 `packages/db/base.py`

Purpose:

- Define SQLAlchemy declarative base.
- Define shared base columns if desired.

Common base fields:

```text
id
created_at
updated_at
```

### 13.10 `apps/worker/main.py`

Purpose:

- Provide worker entry point.
- Later load job queue.
- Later execute ingestion, embedding, eval, and fine-tuning jobs.

In Phase 00, it can be a skeleton that starts and logs successfully.

## 14. Configuration Design In Detail

### 14.1 Settings Groups

Settings should be grouped logically.

Application settings:

```text
APP_NAME
APP_ENV
DEBUG
LOG_LEVEL
API_PREFIX
```

Database settings:

```text
DATABASE_URL
DATABASE_POOL_SIZE
DATABASE_MAX_OVERFLOW
DATABASE_ECHO
```

Redis settings:

```text
REDIS_URL
```

Security settings:

```text
JWT_SECRET later
ENCRYPTION_KEY later
CORS_ORIGINS
```

AI settings reserved for later:

```text
DEFAULT_CHAT_MODEL
DEFAULT_EMBEDDING_MODEL
MODEL_REQUEST_TIMEOUT_SECONDS
MAX_MODEL_INPUT_TOKENS
DAILY_AI_COST_LIMIT
```

### 14.2 Why Typed Settings Matter

Without typed settings, bugs appear late.

Example problem:

```text
DATABASE_POOL_SIZE=abc
```

If settings are plain strings, the application may fail only when handling traffic. With typed settings, startup fails immediately.

### 14.3 Local `.env.example`

The project should include `.env.example`.

Example:

```text
APP_NAME=atlas-ai-platform
APP_ENV=local
DEBUG=true
LOG_LEVEL=INFO
API_PREFIX=/api/v1
DATABASE_URL=postgresql+psycopg://atlas:atlas@localhost:5432/atlas
REDIS_URL=redis://localhost:6379/0
CORS_ORIGINS=http://localhost:3000
DEFAULT_CHAT_MODEL=not-used-in-phase-00
DEFAULT_EMBEDDING_MODEL=not-used-in-phase-00
```

Rules:

- `.env.example` documents required variables.
- Real `.env` should not be committed.
- Secrets should not appear in docs or logs.

## 15. API Foundation Design

### 15.1 API Versioning

Section 6.6 explains what actually counts as a breaking change — the list is narrower than most people expect.

Use versioned routes from the beginning.

Recommended prefix:

```text
/api/v1
```

Why:

- Allows future breaking changes.
- Helps frontend and backend coordinate.
- Looks professional in portfolio and interviews.

### 15.2 Health Endpoints

Section 6.7 explains why liveness and readiness must stay separate, and the outage that follows from confusing them.

#### `GET /api/v1/health/live`

Purpose:

- Confirms the process is alive.

Should not depend on database.

Example response:

```json
{
  "status": "alive",
  "service": "atlas-api"
}
```

#### `GET /api/v1/health/ready`

Purpose:

- Confirms the app is ready to serve real traffic.

Should check:

- Database can respond.
- Redis can respond later.
- Required config exists.

Example response:

```json
{
  "status": "ready",
  "checks": {
    "database": "ok",
    "redis": "ok"
  }
}
```

#### `GET /api/v1/health`

Purpose:

- Simple combined health response for local development.

### 15.3 OpenAPI Documentation

FastAPI automatically provides OpenAPI docs.

Use:

```text
/docs
/openapi.json
```

Why important:

- Frontend developers can inspect API contracts.
- API behavior is easier to test.
- Later AI endpoints become documented.

## 16. Error Handling Design

### 16.1 Error Categories

Create application-level error categories early.

Recommended categories:

```text
bad_request
validation_error
not_authenticated
permission_denied
not_found
conflict
rate_limited
external_service_error
ai_provider_error
ai_output_invalid
safety_blocked
internal_error
```

Even if some categories are used later, define the pattern now.

### 16.2 Application Error Object

Application errors should include:

```text
code
message
status_code
details
```

Example:

```text
code: documents.not_found
message: Document not found.
status_code: 404
```

### 16.3 Why Error Codes Matter

Human-readable messages can change. Error codes are stable.

Frontend can use error codes to show correct UI behavior.

Examples:

```text
permission_denied -> show access message
safety_blocked -> show safety explanation
ai_provider_error -> offer retry
rate_limited -> show wait message
```

### 16.4 Global Error Handlers

The API should register handlers for:

- Application errors.
- Request validation errors.
- Unexpected exceptions.

Unexpected exceptions should return a generic message but log full details internally.

## 17. Logging And Request Tracing

### 17.1 Why Logging Matters More In AI Systems

In normal backend systems, logs tell you what code failed.

In AI systems, logs also help answer:

- What prompt was used?
- What model was called?
- What was retrieved?
- What did the agent do?
- Which tool was called?
- How many tokens were used?
- Which safety check blocked the response?

Phase 00 starts this by adding structured request logs.

### 17.2 Request Id

Each request should have a request id.

Sources:

- Use incoming `X-Request-ID` if provided.
- Otherwise generate a new id.

Return it in response header:

```text
X-Request-ID: req_123
```

### 17.3 Trace Id

A trace id connects work across services and jobs.

Example:

```text
RAG API request
-> retrieval call
-> model call
-> safety check
-> database write
```

All should share the same trace id when possible.

### 17.4 Log Fields

Recommended fields:

```text
timestamp
level
service
environment
request_id
trace_id
tenant_id later
user_id later
method
path
status_code
latency_ms
error_code
```

### 17.5 What Not To Log

Do not log:

- Passwords.
- API keys.
- Raw secrets.
- Full sensitive documents.
- Full prompts if they contain confidential data.
- Full model outputs if policy forbids it.

## 18. Database Foundation

### 18.1 Database Connection

The API needs a database session per request.

Typical flow:

```text
request starts
-> dependency opens database session
-> route calls service
-> service uses repository
-> transaction commits or rolls back
-> session closes
```

### 18.2 SQLAlchemy Engine

Section 6.4 explains pool exhaustion and why `pool_pre_ping` exists.

The engine manages database connections.

Important settings:

```text
DATABASE_URL
pool_size
max_overflow
pool_pre_ping
```

`pool_pre_ping` helps detect broken connections.

### 18.3 Session Factory

A session factory creates database sessions.

Rules:

- Do not create random sessions all over the code.
- Use a central session dependency.
- Keep transaction boundaries clear.

### 18.4 Base Model Convention

Common database fields:

```text
id: UUID or string id
created_at: timestamp
updated_at: timestamp
```

For tenant-owned tables later:

```text
tenant_id
created_by_user_id
```

### 18.5 First Migration

Section 6.11's expand-and-contract pattern governs every schema change from here on.

The first migration may create no business tables yet or may create a minimal system table.

Recommended minimal table:

```text
system_migrations_check
  id
  name
  created_at
```

However, it is also acceptable for Phase 00 to only prove migration infrastructure exists.

## 19. Worker Foundation

### 19.1 Why Workers Exist

Some tasks should not run inside HTTP requests.

Examples later:

- PDF parsing.
- OCR.
- Embedding thousands of chunks.
- Batch evaluations.
- Fine-tuning jobs.
- Long agent workflows.

If these run inside the API request, users will wait too long and the API may timeout.

### 19.2 Worker In Phase 00

Phase 00 should create a worker skeleton.

It should:

- Start successfully.
- Load config.
- Configure logging.
- Connect to Redis later.
- Have a place for jobs.

### 19.3 Future Worker Job Types

Future jobs:

```text
ingest_document
extract_text
run_ocr
chunk_document
generate_embeddings
run_eval_suite
prepare_fine_tune_dataset
run_fine_tune_job
summarize_conversation
cleanup_old_runs
```

## 20. Docker Compose Foundation

### 20.1 Why Docker Compose

Docker Compose lets the project run local dependencies consistently.

Instead of manually installing Postgres and Redis, the developer runs one command.

Example services:

```text
postgres
redis
api optional
worker optional
```

### 20.2 PostgreSQL Service

Should define:

```text
image: postgres
ports: 5432:5432
environment:
  POSTGRES_USER
  POSTGRES_PASSWORD
  POSTGRES_DB
volumes:
  postgres_data
```

### 20.3 Redis Service

Should define:

```text
image: redis
ports: 6379:6379
```

### 20.4 Health Checks

Docker services should have health checks when practical.

Why:

- API should not start before database is ready.
- CI can detect unhealthy dependencies.

## 21. Testing Foundation

### 21.1 Test Types In Phase 00

Section 6.8 covers the pyramid, the difference between a stub and a fake, and why flaky tests are worse than none.

Phase 00 should include:

- Unit tests.
- Integration tests.
- Basic API tests.
- Config tests.
- Error handling tests.

### 21.2 Unit Test Examples

Unit tests do not require external infrastructure.

Examples:

```text
test_settings_loads_default_values
test_invalid_environment_fails
test_application_error_has_code
test_error_response_shape
test_request_id_is_generated
```

### 21.3 Integration Test Examples

Integration tests may require database or app startup.

Examples:

```text
test_health_endpoint_returns_ok
test_ready_endpoint_checks_database
test_database_session_opens
test_migrations_apply
```

### 21.4 Why Tests Matter For Later Gen AI

Later AI features need non-AI tests and AI evaluation tests.

Phase 00 creates the testing habit.

Examples later:

- Test model gateway with fake provider.
- Test invalid JSON structured output.
- Test RAG returns citations.
- Test agent stops after max steps.
- Test tool permission is enforced.
- Test prompt injection does not execute tool.

Without Phase 00 test setup, later AI work becomes guesswork.


## 22. Implementation Sequence From Empty Folder To Working Foundation

This section explains the build flow in the order a developer should implement it.

### Step 1: Create Repository Root

Create the root folder:

```text
atlas-ai-platform/
```

Add root files:

```text
README.md
pyproject.toml
.env.example
.gitignore
docker-compose.yml
```

Why:

- `README.md` explains how to run the project.
- `pyproject.toml` defines Python dependencies and tooling.
- `.env.example` documents required environment variables.
- `.gitignore` prevents secrets and generated files from being committed.
- `docker-compose.yml` runs local infrastructure.

### Step 2: Choose Python Version

Recommended:

```text
Python 3.11 or Python 3.12
```

Why:

- Modern typing support.
- Better performance.
- Better library support.
- Common in current backend projects.

### Step 3: Create Virtual Environment

A virtual environment isolates project dependencies from global Python packages.

Example command:

```text
python -m venv .venv
```

Activation on Windows PowerShell:

```text
.\.venv\Scripts\Activate.ps1
```

Why:

- Avoids dependency conflicts.
- Keeps project reproducible.
- Prevents accidental use of globally installed packages.

### Step 4: Add Dependency Management

Runtime dependencies:

```text
fastapi
uvicorn
pydantic
pydantic-settings
sqlalchemy
alembic
psycopg
redis
httpx
python-dotenv
```

Development dependencies:

```text
pytest
pytest-asyncio
ruff
mypy or pyright
coverage
```

Later AI dependencies should not be added in Phase 00 unless needed.

Future AI dependencies:

```text
openai
anthropic
transformers
sentence-transformers
langgraph
mlflow
peft
torch
qdrant-client
```

Why not add all AI libraries now:

- Keeps Phase 00 lightweight.
- Avoids dependency complexity before architecture is ready.
- Makes each later phase teach its own tools clearly.

### Step 5: Create Package Folders

Create:

```text
apps/
packages/
tests/
infra/
docs/
```

Then create skeleton packages:

```text
packages/core
packages/db
packages/auth
packages/model_gateway
packages/prompts
packages/ingestion
packages/retrieval
packages/rag
packages/agents
packages/tools
packages/memory
packages/safety
packages/evals
packages/observability
```

Each package gets an `__init__.py` file.

Why:

- Makes Python import paths clear.
- Prepares the project for later phases.
- Shows the architecture before every feature is built.

### Step 6: Build Settings Class

Create:

```text
packages/core/config.py
```

The settings class should include:

```text
app_name
app_env
debug
log_level
api_prefix
database_url
redis_url
cors_origins
```

Rules:

- Use Pydantic settings.
- Validate required values.
- Use default values only for safe local behavior.
- Never include real secrets in code.

Learning point:

This is the first place where Python typing and production configuration meet.

### Step 7: Build Logging Setup

Create:

```text
packages/core/logging.py
```

It should configure:

- Log level.
- Service name.
- Environment.
- Request id support.
- JSON-like structure if possible.

Minimum useful log fields:

```text
timestamp
level
event
service
environment
request_id
```

Learning point:

Logs are not print statements. Logs are operational evidence.

### Step 8: Build Error Classes

Create:

```text
packages/core/errors.py
```

Define a base application error.

Fields:

```text
code
message
status_code
details
```

Create common subclasses:

```text
BadRequestError
NotFoundError
PermissionDeniedError
ConflictError
ExternalServiceError
InternalAppError
```

Reserve future AI errors:

```text
AIProviderError
AIOutputValidationError
SafetyBlockedError
ToolExecutionError
```

Learning point:

Good AI platforms need predictable failure behavior because model calls and external tools fail often.

### Step 9: Build API App Factory

Create:

```text
apps/api/main.py
```

Use an app factory:

```text
create_app() -> FastAPI
```

Why app factory:

- Easier testing.
- Cleaner configuration.
- Easier future dependency injection.
- Avoids import-time side effects.

The app factory should:

- Load settings.
- Configure logging.
- Create FastAPI app.
- Add middleware.
- Register error handlers.
- Register routes.

### Step 10: Add Request ID Middleware

Create:

```text
apps/api/middleware/request_id.py
```

Behavior:

```text
if request has X-Request-ID, use it
else generate new request id
attach id to request state
add X-Request-ID to response
include it in logs
```

Why:

Later one user complaint can be traced through:

```text
frontend request
backend logs
ai_run record
retrieval trace
agent step
tool call
safety check
```

### Step 11: Add Health Routes

Create:

```text
apps/api/routes/health.py
```

Endpoints:

```text
GET /api/v1/health/live
GET /api/v1/health/ready
GET /api/v1/health
```

Implementation detail:

- Liveness should be simple.
- Readiness should check dependencies.
- In Phase 00, readiness should at least check database when database is configured.

### Step 12: Add Error Handlers

Global error handlers should convert exceptions to standard responses.

Handle:

- Application errors.
- FastAPI/Pydantic validation errors.
- Unexpected exceptions.

Unexpected exception response should be safe:

```json
{
  "error": {
    "code": "internal_error",
    "message": "An unexpected error occurred.",
    "details": {},
    "request_id": "req_123"
  }
}
```

Full stack trace should be logged internally, not returned to user.

### Step 13: Build Database Session

Create:

```text
packages/db/session.py
```

Responsibilities:

- Create engine from `DATABASE_URL`.
- Create session factory.
- Provide `get_db_session()` dependency.
- Support testing override.

Important decision:

For FastAPI, you can choose sync or async SQLAlchemy.

Recommended first choice:

```text
sync SQLAlchemy for simpler learning
```

Alternative:

```text
async SQLAlchemy for high-concurrency design
```

Pragmatic recommendation:

Start sync unless the project already strongly uses async database patterns. LLM calls are external and can still be async later, but database complexity should stay understandable at first.

### Step 14: Build SQLAlchemy Base

Create:

```text
packages/db/base.py
```

Define:

- Declarative base.
- Common mixins.
- Timestamp helpers.

Potential mixins:

```text
IdMixin
TimestampMixin
TenantMixin later
SoftDeleteMixin later
```

### Step 15: Add Alembic

Initialize migrations under:

```text
packages/db/migrations
```

Configure Alembic to read:

- Database URL from settings.
- SQLAlchemy metadata from `packages/db/base.py`.

Rules:

- Never manually edit production database schema.
- Every schema change gets a migration.
- Migrations should be reviewed.

### Step 16: Add Docker Compose

Create services:

```text
postgres
redis
```

Optional in Phase 00:

```text
api
worker
```

Keep local development simple.

Example flow:

```text
docker compose up -d postgres redis
alembic upgrade head
uvicorn apps.api.main:create_app --factory --reload
```

### Step 17: Add Worker Skeleton

Create:

```text
apps/worker/main.py
```

Minimum behavior:

- Load settings.
- Configure logging.
- Print/log worker started.
- Provide placeholder for future job registration.

Future behavior:

- Connect to Redis queue.
- Register ingestion jobs.
- Register evaluation jobs.
- Register fine-tuning jobs.

### Step 18: Add Tests

Create test files:

```text
tests/unit/test_config.py
tests/unit/test_errors.py
tests/integration/test_health_api.py
tests/integration/test_database.py
```

Minimum tests:

- Settings load.
- Health endpoint returns 200.
- Request id header exists.
- Error response shape is consistent.
- Database readiness works when DB is available.

### Step 19: Add Code Quality Commands

In `pyproject.toml`, define commands or document them:

```text
ruff check .
ruff format .
pytest
mypy packages apps
```

Why:

- Prevents style drift.
- Makes CI easy later.
- Creates professional habits.

### Step 20: Update README

README should explain:

- Project purpose.
- Requirements.
- Setup steps.
- Environment variables.
- Running local infrastructure.
- Running API.
- Running tests.
- Running migrations.
- Folder structure.

A good README matters for portfolio review.

## 23. Data Flow In Phase 00

### 23.1 API Health Request Flow

```text
Developer opens browser or sends HTTP request
-> GET /api/v1/health
-> FastAPI receives request
-> request id middleware attaches request id
-> health route executes
-> settings provide service/environment name
-> response schema validates output
-> response returned with request id header
-> structured log records request
```

### 23.2 Readiness Request Flow

```text
GET /api/v1/health/ready
-> middleware adds request id
-> route calls database readiness check
-> database session executes simple query
-> optional Redis ping later
-> response returns ready or not ready
-> logs include dependency status
```

### 23.3 Error Flow

```text
request enters API
-> route or service raises ApplicationError
-> global error handler catches it
-> error response schema is created
-> request id is included
-> structured log is written
-> frontend receives predictable error
```

### 23.4 Migration Flow

```text
developer changes database model
-> creates Alembic migration
-> reviews generated SQL
-> runs migration locally
-> tests pass
-> migration committed
-> CI applies migration in test database
-> staging applies migration before deployment
```

## 24. API Contracts In Phase 00

### 24.1 Health Response Schema

Fields:

```text
status
service
environment
version optional
checks optional
```

Example:

```json
{
  "status": "ok",
  "service": "atlas-api",
  "environment": "local"
}
```

### 24.2 Readiness Response Schema

Fields:

```text
status
checks
```

Example:

```json
{
  "status": "ready",
  "checks": {
    "database": "ok",
    "redis": "not_configured"
  }
}
```

### 24.3 Error Response Schema

Fields:

```text
error.code
error.message
error.details
error.request_id
```

Example:

```json
{
  "error": {
    "code": "health.database_unavailable",
    "message": "Database is not ready.",
    "details": {
      "dependency": "postgres"
    },
    "request_id": "req_abc"
  }
}
```

## 25. Database Objects In Phase 00

Phase 00 can stay light on business tables.

### 25.1 Optional `system_status_checks` Table

Purpose:

- Prove migrations and database access work.

Fields:

```text
id
name
created_at
```

This table is optional. If you prefer, Phase 00 can create only migration infrastructure and wait for tenant/user tables in the auth phase.

### 25.2 Alembic Version Table

Alembic creates:

```text
alembic_version
```

Purpose:

- Stores current migration version.

This table proves schema versioning is active.

## 26. Python Concepts Learned In Phase 00

### 26.1 Imports And Packages

You learn how Python finds modules and packages.

Example:

```text
from packages.core.config import Settings
```

This matters later because a large AI project has many modules.

### 26.2 Type Hints

Type hints describe expected data types.

Example:

```text
def get_settings() -> Settings
```

Why important:

- Helps catch errors.
- Makes code easier to understand.
- Helps IDE autocomplete.
- Helps structured AI schemas later.

### 26.3 Classes

Classes group data and behavior.

Used for:

- Settings.
- Errors.
- Database models.
- Service classes later.
- Provider adapters later.

### 26.4 Dependency Injection

Dependency injection means passing dependencies into code instead of creating them randomly inside functions.

FastAPI supports dependency injection.

Example uses:

- Database session.
- Current user later.
- Tenant context later.
- Model gateway client later.

Why important:

- Easier testing.
- Easier swapping real provider with fake provider.
- Cleaner architecture.

### 26.5 Context Managers

Context managers manage setup and cleanup.

Used for:

- Database sessions.
- Lifespan startup/shutdown.
- Test fixtures.

### 26.6 Exceptions

Exceptions represent failure.

Professional code does not let every exception leak randomly. It converts expected failures into known application errors.

### 26.7 Environment-Based Behavior

The app behaves differently in:

```text
local
test
staging
production
```

But the code should remain mostly the same.

## 27. Backend Concepts Learned In Phase 00

### 27.1 Request-Response Lifecycle

Every HTTP API call has:

```text
request
validation
handler
service logic
response
```

### 27.2 Middleware

Middleware runs before and after route handlers.

Used for:

- Request id.
- Logging.
- CORS.
- Authentication later.
- Rate limiting later.

### 27.3 Schema Validation

API schemas prevent invalid inputs and unclear outputs.

FastAPI with Pydantic gives this automatically.

### 27.4 Database Sessions

A database session tracks database operations.

Wrong session management can cause:

- Connection leaks.
- Uncommitted changes.
- Broken tests.
- Production instability.

### 27.5 Migrations

Migrations make schema changes repeatable.

In AI systems, many tables are added over time:

- documents.
- chunks.
- embeddings.
- AI runs.
- agent steps.
- tool calls.
- eval results.

Alembic keeps those changes controlled.

## 28. Gen AI Perspective In Phase 00

Phase 00 does not call models yet, but it prepares the system for Gen AI.

### 28.1 Why Not Call LLM First

A beginner often wants to start with:

```text
input -> OpenAI -> output
```

That is useful for a small experiment, but not enough for industry work.

An industry system needs:

- Model gateway.
- Prompt versioning.
- Structured output validation.
- AI run logging.
- Cost tracking.
- Evaluation.
- Safety.
- Retry and timeout handling.
- Provider abstraction.

Phase 00 creates the backend foundation where those features will live.

### 28.2 AI-Ready Decisions Made In Phase 00

Decisions:

- Use Pydantic because later model outputs need schemas.
- Use structured logging because later AI traces need debugging.
- Use request ids because later model calls need traceability.
- Use database migrations because later AI records need schema control.
- Use modular packages because later RAG/agents/safety need boundaries.
- Use tests because later AI behavior needs regression checks.
- Use Docker because later vector DB and workers need repeatable setup.

### 28.3 Future AI Hooks Created By Phase 00

Future hooks:

```text
packages/model_gateway -> LLM and embedding calls
packages/prompts -> prompt templates and versions
packages/evals -> evaluation datasets and scores
packages/safety -> input/output checks
packages/retrieval -> embeddings, vector search, hybrid search, reranking
packages/rag -> answer generation, grounding, context packing, citations
packages/agents -> state machines and tools
packages/observability -> AI traces and cost records
```

## 29. Safety And Security Perspective In Phase 00

### 29.1 Security Starts Before AI

Security should not be added at the end.

Phase 00 starts security by creating:

- Config discipline.
- Secret separation.
- Error response safety.
- Logging rules.
- Folder boundaries.
- Request tracing.

### 29.2 Secrets Safety

Rules:

- `.env` is not committed.
- `.env.example` has fake values only.
- Secrets do not appear in logs.
- Provider keys will later be read only from secure config.

### 29.3 Error Safety

Do not return internal stack traces to users.

Bad:

```text
Database password failed for user atlas with connection string...
```

Good:

```json
{
  "error": {
    "code": "internal_error",
    "message": "An unexpected error occurred."
  }
}
```

### 29.4 Logging Safety

Logs must be useful but not reckless.

Do log:

- Request id.
- Route.
- Status code.
- Latency.
- Error code.

Do not log:

- Passwords.
- API keys.
- Raw private documents.
- Sensitive prompts.

## 30. Evaluation Perspective In Phase 00

Evaluation later measures AI quality. Phase 00 creates the technical testing base.

### 30.1 Difference Between Software Tests And AI Evaluations

Software test:

```text
Given input X, function returns exactly Y.
```

AI evaluation:

```text
Given input X, model output is judged for correctness, groundedness, citation accuracy, safety, and usefulness.
```

Phase 00 starts with software tests. AI evaluations begin later.

### 30.2 What To Verify In Phase 00

Verify:

- App starts.
- Settings load.
- Health endpoint works.
- Error shape is stable.
- Request id exists.
- Database session works.
- Migrations can run.
- Docker dependencies start.

### 30.3 Why This Supports Future Evaluations

Future evaluation runners will need:

- Config.
- Database.
- Logging.
- Test fixtures.
- Repeatable commands.

Phase 00 provides those.

## 31. Operations Perspective

### 31.1 What Operations Means

Operations means running the system reliably after coding.

It includes:

- Starting services.
- Health checks.
- Logs.
- Metrics.
- Migrations.
- Backups later.
- Deployment later.
- Debugging incidents.

### 31.2 Operational Questions Phase 00 Should Answer

Questions:

- How do I start the API?
- How do I start Postgres and Redis?
- How do I know the API is alive?
- How do I know the API is ready?
- How do I run migrations?
- How do I run tests?
- Where are logs?
- How do I configure the app?

If Phase 00 cannot answer these, it is not complete.

### 31.3 Health Checks And Deployment

Later deployment systems need health endpoints.

Kubernetes, container platforms, and load balancers commonly use:

- Liveness checks.
- Readiness checks.

This is why Phase 00 adds them now.

## 32. Developer Experience Perspective

Developer experience matters because hard-to-run projects die early.

A new developer should be able to:

1. Clone the repo.
2. Create virtual environment.
3. Install dependencies.
4. Copy `.env.example` to `.env`.
5. Start Docker services.
6. Run migrations.
7. Start API.
8. Open health endpoint.
9. Run tests.

If this takes unclear manual guessing, improve README and scripts.

## 33. Implementation Details For Future Compatibility

### 33.1 Use Interfaces For Future Swapping

Even in Phase 00, design with interfaces in mind.

Examples later:

```text
ModelProvider interface
VectorStore interface
ObjectStorage interface
Queue interface
Tool interface
SafetyChecker interface
Evaluator interface
```

Do not overbuild these in Phase 00, but leave the package structure ready.

### 33.2 Avoid Global Side Effects

Bad:

```text
database engine created at import time with hard-coded URL
```

Better:

```text
settings loaded intentionally
engine created by database module
app factory wires dependencies
```

Why:

- Tests can override settings.
- CLI tools can reuse packages.
- Worker can load same config.

### 33.3 Keep Business Logic Out Of Routes

Routes should handle HTTP concerns.

Service modules should handle business logic.

In Phase 00, there is little business logic, but the pattern should start early.

Bad future pattern:

```text
route uploads document, parses PDF, chunks text, calls embeddings, stores vectors
```

Good future pattern:

```text
route validates request
-> calls ingestion service
-> ingestion service creates job
-> worker processes job
```

## 34. Example Minimal API Flow Without Full Code

This is not implementation code, but it explains how the pieces fit.

```text
create_app()
  -> settings = get_settings()
  -> configure_logging(settings)
  -> app = FastAPI(...)
  -> app.add_middleware(RequestIdMiddleware)
  -> register_exception_handlers(app)
  -> app.include_router(health_router, prefix=settings.api_prefix)
  -> return app
```

Health route:

```text
GET /health
  -> read settings
  -> return HealthResponse(status='ok', service=settings.app_name)
```

Readiness route:

```text
GET /health/ready
  -> open database session
  -> execute SELECT 1
  -> ping Redis if enabled
  -> return dependency status
```

Error handling:

```text
service raises AppError
  -> exception handler catches it
  -> builds ErrorResponse
  -> logs error_code and request_id
  -> returns HTTP response
```

## 35. Common Mistakes In Phase 00

### Mistake 1: Starting With LLM Code

Problem:

- No structure.
- No logging.
- No tests.
- No traceability.

Fix:

- Build backend foundation first.

### Mistake 2: Hard-Coding Secrets

Problem:

- Security risk.
- Hard to deploy.
- Hard to rotate keys.

Fix:

- Use environment variables and secret manager later.

### Mistake 3: No Migrations

Problem:

- Database schema changes become manual.
- Team members have different database states.

Fix:

- Use Alembic from the start.

### Mistake 4: Random Folder Structure

Problem:

- RAG, agents, tools, and safety code mix together.
- Code becomes difficult to maintain.

Fix:

- Use clear package boundaries.

### Mistake 5: Only Manual Testing

Problem:

- Every change requires clicking around.
- Bugs return.

Fix:

- Add automated tests immediately.

### Mistake 6: Logging Full Sensitive Data

Problem:

- Private data leaks into logs.

Fix:

- Log metadata and identifiers, not raw sensitive content.

## 36. Failure Modes And Fixes

### 36.1 App Does Not Start

Possible causes:

- Missing environment variable.
- Bad import path.
- Dependency not installed.
- Wrong Python version.

Fixes:

- Validate settings at startup.
- Keep README updated.
- Use consistent run command.
- Add startup test.

### 36.2 Database Connection Fails

Possible causes:

- Postgres container not running.
- Wrong `DATABASE_URL`.
- Database not created.
- Network or port mismatch.

Fixes:

- Check Docker Compose status.
- Use readiness endpoint.
- Add database integration test.
- Document local setup clearly.

### 36.3 Migrations Fail

Possible causes:

- Alembic cannot import metadata.
- Database URL missing.
- Migration conflict.
- Model changed but migration missing.

Fixes:

- Configure Alembic carefully.
- Run migrations in CI.
- Review migration scripts.

### 36.4 Tests Are Flaky

Possible causes:

- Shared global state.
- Tests depend on real time.
- Tests depend on external services without isolation.
- Database not cleaned between tests.

Fixes:

- Use fixtures.
- Use test database.
- Use fake providers later.
- Keep unit tests independent.

### 36.5 Logs Are Useless

Possible causes:

- No request id.
- Random print statements.
- Missing error codes.
- Excessive noisy logs.

Fixes:

- Structured logging.
- Request id middleware.
- Clear error codes.
- Logging policy.

## 37. Quality Gates For Phase 00

Phase 00 should not be considered done until all quality gates pass.

### 37.1 Functional Gates

- API starts locally.
- Health endpoint returns success.
- Readiness endpoint checks database.
- Worker skeleton starts.
- Docker Compose starts Postgres and Redis.
- Alembic migration command works.

### 37.2 Code Quality Gates

- Linter passes.
- Formatter passes.
- Type checker passes or is configured.
- No hard-coded secrets.
- No direct print debugging in application code.

### 37.3 Test Gates

- Unit tests pass.
- Integration tests pass.
- Health endpoint test passes.
- Error envelope test passes.
- Config test passes.

### 37.4 Documentation Gates

README includes:

- Setup.
- Run commands.
- Test commands.
- Migration commands.
- Folder structure.
- Environment variables.

### 37.5 AI-Readiness Gates

- `packages/model_gateway` placeholder exists.
- `packages/prompts` placeholder exists.
- `packages/evals` placeholder exists.
- `packages/safety` placeholder exists.
- `packages/retrieval` placeholder exists for embeddings/search/reranking.
- `packages/rag` placeholder exists for grounded answer orchestration/citations.
- `packages/agents` placeholder exists.
- Logging includes request id.
- Error system includes future AI error categories.

## 38. What To Avoid Building Too Early

Avoid adding these before foundation is stable:

- Full user management.
- Complex frontend dashboard.
- Real LLM provider calls.
- Vector database.
- Agent framework.
- Fine-tuning pipeline.
- Kubernetes.
- Complex observability stack.

Reason:

If the foundation is not stable, adding complexity hides basic design problems.

## 39. How This Phase Connects To Phase 01

Phase 01 is the LLM Gateway.

Phase 00 prepares Phase 01 by providing:

- `packages/model_gateway` folder.
- Config system for provider keys and model names.
- Logging system for model calls.
- Error system for provider failures.
- Test setup for fake provider tests.
- API structure for future model endpoints.
- Database structure for future `ai_runs` table.

Phase 01 will add:

- Chat model interface.
- Embedding model interface later.
- Provider adapter.
- Mock adapter.
- Token tracking.
- Cost tracking.
- AI run persistence.

## 40. What You Should Be Able To Explain After Phase 00

You should be able to explain:

- Why a Gen AI platform should not start with random LLM calls.
- What FastAPI does.
- What Pydantic does.
- What SQLAlchemy does.
- What Alembic does.
- Why PostgreSQL is used.
- Why Redis is useful.
- Why Docker Compose matters.
- What a request id is.
- Why structured logging matters.
- Why error envelopes matter.
- Why tests are required before AI features.
- How the folder structure supports future RAG, agents, safety, and evaluation.

## 41. Interview Perspective

### 41.1 How To Present Phase 00 In An Interview

Say:

```text
I started by building a production-oriented Python backend foundation instead of directly calling an LLM. I used FastAPI for APIs, Pydantic for validation and settings, SQLAlchemy and Alembic for database access and migrations, PostgreSQL as the system of record, Redis for future queues and rate limiting, structured logging with request ids for traceability, and pytest for automated testing. I organized the code as a modular monolith so later AI modules like RAG, agents, safety, model gateway, and evaluation have clean boundaries.
```

### 41.2 Interview Questions This Phase Prepares You For

Questions:

- Why did you choose FastAPI?
- Why use Pydantic?
- How do you manage environment config?
- How do you handle database migrations?
- What is the difference between liveness and readiness?
- How do you structure a Python backend project?
- How do you avoid circular imports?
- How do you make a project testable?
- How do you prepare a backend for AI features?
- Why should model calls go through a gateway later?

### 41.3 Strong Answers To Know

Question:

```text
Why not call the LLM directly from a route?
```

Strong answer:

```text
Because direct model calls from routes make the system hard to test, monitor, control, and evolve. I prefer a model gateway so all providers, retries, timeouts, token usage, cost tracking, structured output validation, and logging are centralized.
```

Question:

```text
Why do you need migrations in an AI project?
```

Strong answer:

```text
AI systems still need reliable data models. Documents, chunks, embeddings, prompts, AI runs, agent steps, tool calls, safety checks, and evaluations all require schema changes. Migrations keep those changes repeatable across local, staging, and production.
```

Question:

```text
Why are request ids important?
```

Strong answer:

```text
A request id lets me connect a user-facing problem to backend logs, AI run records, retrieval traces, tool calls, safety checks, and evaluation cases. This is essential for debugging AI behavior in production.
```

## 42. Portfolio Evidence From Phase 00

After implementing Phase 00, portfolio evidence should include:

- Clean repository structure screenshot or tree.
- README with setup instructions.
- Running health endpoint.
- Passing test output.
- Docker Compose running Postgres and Redis.
- Alembic migration history.
- Example structured error response.
- Example structured log with request id.

This evidence proves you can build more than notebooks and demos.

## 43. Practical Build Checklist

Use this checklist while implementing.

```text
[ ] Create repository root
[ ] Create pyproject.toml
[ ] Create .env.example
[ ] Create .gitignore
[ ] Create apps/api
[ ] Create apps/worker
[ ] Create packages/core
[ ] Create packages/db
[ ] Create future package placeholders
[ ] Add FastAPI app factory
[ ] Add health routes
[ ] Add request id middleware
[ ] Add settings class
[ ] Add logging setup
[ ] Add application error classes
[ ] Add error response schemas
[ ] Add global error handlers
[ ] Add database engine/session
[ ] Add SQLAlchemy base
[ ] Add Alembic setup
[ ] Add Docker Compose for Postgres and Redis
[ ] Add worker skeleton
[ ] Add pytest config
[ ] Add unit tests
[ ] Add integration tests
[ ] Add lint/format/type commands
[ ] Add README instructions
[ ] Verify local run
[ ] Verify tests
[ ] Verify migrations
```

## 44. Definition Glossary

### API

A contract that allows one software system to communicate with another.

### Backend

Server-side code that handles business logic, database access, APIs, background jobs, security, and integrations.

### FastAPI

A Python framework for building HTTP APIs with automatic validation and OpenAPI documentation.

### Pydantic

A Python library for validating data using type hints.

### SQLAlchemy

A Python database toolkit and ORM used to work with relational databases.

### Alembic

A migration tool that tracks database schema changes over time.

### PostgreSQL

A production-grade relational database.

### Redis

A fast in-memory data store often used for queues, caching, locks, and rate limiting.

### Docker

A tool for packaging applications or infrastructure services into containers.

### Docker Compose

A tool for running multiple containers together locally.

### Migration

A versioned database schema change.

### Middleware

Code that runs around HTTP requests before and after route handlers.

### Request ID

A unique id attached to a request so logs and traces can be connected.

### Structured Logging

Logging as fields instead of unstructured text.

### Unit Test

A test for a small piece of code without external dependencies.

### Integration Test

A test that checks multiple pieces working together, such as API plus database.

### Modular Monolith

One deployable application organized into clear internal modules.

### Service Boundary

A rule that defines what a module owns and how other modules should interact with it.

### Dependency Injection

Passing dependencies into code instead of creating them directly inside functions.

## 45. Mini Examples For Understanding

### 45.1 Bad Folder Design

```text
main.py
utils.py
ai.py
database.py
helpers.py
```

Problem:

- Everything becomes mixed.
- Hard to know where new code belongs.
- Hard to test.

### 45.2 Better Folder Design

```text
apps/api/routes/
packages/core/
packages/db/
packages/model_gateway/
packages/rag/
packages/agents/
```

Benefit:

- Clear ownership.
- Easier to extend.
- Easier to explain.

### 45.3 Bad Config

```text
DATABASE_URL = "postgresql://user:pass@localhost/db"
```

Problem:

- Secret in code.
- Cannot easily switch environments.

### 45.4 Better Config

```text
DATABASE_URL comes from environment
Settings validates it at startup
```

Benefit:

- Secure.
- Deployable.
- Testable.

### 45.5 Bad Error

```text
return {"error": "failed"}
```

Problem:

- No code.
- No request id.
- Hard to debug.

### 45.6 Better Error

```json
{
  "error": {
    "code": "database.unavailable",
    "message": "Database is not ready.",
    "request_id": "req_123"
  }
}
```

Benefit:

- Frontend can react.
- Developer can trace.
- User gets stable response.

## 46. Production Mindset For Phase 00

Even though this is the first phase, think like production from the start.

Production-minded decisions:

- Use health checks.
- Use migrations.
- Use config validation.
- Use structured errors.
- Use request ids.
- Use test fixtures.
- Use dependency boundaries.
- Use Docker Compose.
- Avoid secrets in code.
- Avoid direct provider calls from routes.

These decisions are small now and expensive later if skipped.

## 47. Phase 00 Done Criteria

Phase 00 is done when all of these are true:

1. Repository structure exists.
2. API app starts.
3. Worker skeleton starts.
4. Health endpoint works.
5. Readiness endpoint can check dependencies.
6. Settings load from environment.
7. `.env.example` is complete.
8. Structured logging is configured.
9. Request id middleware works.
10. Error envelope is consistent.
11. Database connection is configured.
12. Alembic migrations are configured.
13. Docker Compose starts Postgres and Redis.
14. Unit tests pass.
15. Integration tests pass.
16. README explains setup and commands.
17. Future AI package placeholders exist.
18. No real secrets are committed.
19. No LLM code is mixed into routes.
20. The next phase can add the model gateway cleanly.

## 48. Final Mental Model

Phase 00 is the foundation layer of the Atlas AI Platform.

It teaches that professional Gen AI engineering is not only about prompts and models. It is also about systems.

The correct mental model is:

```text
Strong backend foundation
-> controlled model gateway
-> reliable prompts
-> structured outputs
-> searchable knowledge
-> grounded RAG
-> measurable evaluation
-> safe tools
-> controlled agents
-> monitored production system
```

If you understand and implement Phase 00 properly, every later AI topic becomes easier to build, test, debug, deploy, and explain.
