# Learning Environment for Production AI Engineering

## Lesson metadata

| Field | Value |
|---|---|
| Curriculum position | First shared core lesson |
| Primary roles | Applied AI Engineer, Generative AI Engineer, LLM Engineer, Machine Learning Engineer, MLOps Engineer |
| Difficulty | Beginner to intermediate |
| Estimated study time | 4-6 hours |
| Estimated implementation time | 4-8 hours |
| Prerequisite lessons | None |
| Project increment | Reproducible `ai-industry-labs` repository |
| Primary tools | Python, uv, Git, Docker, Docker Compose, Ruff, mypy, pytest, pre-commit, GitHub Actions |
| Supporting tools | Pydantic Settings, pip-audit, PostgreSQL, Redis |
| Technical details verified | June 25, 2026 |

## Why this lesson exists

An AI system cannot be production-ready when the team cannot reproduce its environment.
Model quality attracts attention, but production failures often begin much earlier:

- One developer has a different Python version.
- A package update changes behavior without review.
- A secret is stored in source control.
- Tests pass locally but fail in continuous integration.
- A container contains tools and files that are unnecessary at runtime.
- Local databases are configured differently on every workstation.
- Nobody can identify which dependency set produced a deployed result.

This lesson establishes the engineering base used by every later lesson. The repository created
here will grow into the support-ticket backend, LLM application, RAG system, agent workflow,
training pipeline, and production AI platform.

The objective is not to learn every feature of Python packaging, Git, Docker, or CI. The
objective is to create one dependable workflow that the rest of the course can reuse.

Do not use this exact stack blindly when an employer already has a supported internal platform.
In that situation, preserve the principles from this lesson while using the organization's
standard package manager, container registry, CI system, and secret manager.

## Business problem

### Organization

A customer-support software company is starting an Applied AI program. Several engineers will
build classifiers, LLM assistants, retrieval systems, and model-training experiments.

### Current workflow

Each engineer currently:

- Installs Python manually.
- Uses an untracked set of packages.
- Stores local configuration differently.
- Runs services directly on the host.
- Tests code only before a demonstration.
- Shares setup instructions through chat messages.

### Pain point

A prototype works on its author's laptop but cannot be reproduced reliably by another engineer
or by CI. The team loses time diagnosing environment differences instead of evaluating the AI
system.

### Inputs

- Source code
- Project metadata
- Dependency constraints
- Lockfile
- Environment variables
- Local service configuration
- CI workflow

### Outputs

- Reproducible local Python environment
- Validated application configuration
- Machine-readable health report
- Tested container image
- Local PostgreSQL and Redis services
- Automated quality checks
- CI result

### Constraints

- Development must work on Windows, macOS, and Linux.
- No real secret may be committed.
- The runtime image must not run as root.
- The project must be rebuildable from committed files.
- CI must not require a paid model API.
- A fresh developer should reach a passing health check using the README.

### Risk level

Low business risk, but high foundational importance. A poor environment design propagates into
every later AI project.

### Baseline

The current baseline is an informal setup:

```text
Install Python
→ pip install packages from memory
→ copy a colleague's .env file
→ run a script
→ debug machine-specific failures
```

### Success metrics

- Fresh-clone setup succeeds without undocumented steps.
- `uv lock --check` confirms that project metadata and lockfile agree.
- Linting, formatting, type checking, tests, and dependency audit pass.
- The health command behaves consistently locally and inside Docker.
- CI runs on Windows and Linux.
- Git history contains no real credentials.
- Runtime configuration is validated before application work begins.

## Learning outcomes

After completing the lesson, you will be able to:

- Explain the difference between dependency constraints and a lockfile.
- Pin a supported Python minor version for a project.
- Create and synchronize an isolated environment with uv.
- Separate runtime and development dependencies.
- Load typed configuration from environment variables.
- Prevent local secret files and generated artifacts from entering Git.
- Configure Ruff, mypy, pytest, and pre-commit.
- Build a non-root, multi-stage Docker image.
- run PostgreSQL and Redis with Docker Compose.
- Create a cross-platform GitHub Actions workflow.
- Diagnose common environment, dependency, Docker, and CI failures.
- Defend the environment design in a technical interview.

## Prerequisites

### Knowledge

- Basic command-line navigation
- Basic understanding of files and directories
- Basic Python syntax is helpful but not required

### Software

- Git
- Docker Desktop or Docker Engine with the Compose plugin
- A terminal:
  - PowerShell on Windows
  - Bash or another POSIX-compatible shell on macOS or Linux
- A code editor

### Accounts

- A GitHub account is required only for the CI and pull-request portion.

### Hardware

- No GPU is required.
- Allocate enough local memory for one Python container, PostgreSQL, and Redis.

### Paid services

None. This lesson deliberately avoids paid AI APIs.

## Key terminology

### Runtime

The Python interpreter and operating environment in which the application executes.

### Virtual environment

An isolated directory containing a Python interpreter context and project-specific packages.
It prevents one project's packages from changing another project's environment.

### Dependency constraint

A rule in `pyproject.toml` describing an acceptable package-version range, such as
`pydantic>=2,<3`.

### Dependency resolution

The process of selecting exact package versions that satisfy all direct and transitive
constraints.

### Lockfile

A generated file recording the exact resolved dependency graph. The project uses `uv.lock`.
The uv documentation recommends committing it so installations remain consistent across
machines.

### Synchronization

Installing the package set described by the lockfile into the project environment. With uv,
`uv sync` performs exact synchronization by default and removes packages not represented in
the lockfile.

### Development dependency

A package needed to build, test, lint, or inspect the project but not required by the running
application.

### Environment variable

A key-value setting supplied outside the source code, such as `AI_LABS_LOG_LEVEL=DEBUG`.

### Secret

A credential or sensitive value that grants access, such as an API key, database password, or
private token. A secret is not merely configuration; it requires restricted storage, access,
rotation, and audit controls.

### Container image

An immutable application filesystem and configuration template created by a container build.

### Container

A running instance of an image.

### Docker Compose

A declarative way to define and run multiple related local services, networks, volumes, and
configuration.

### Continuous integration

An automated workflow that validates proposed code changes by running checks in a clean
environment.

### Pre-commit hook

A local automated check triggered before Git creates a commit. It provides fast feedback but
does not replace CI because a developer can bypass local hooks.

### Reproducible build

A build whose inputs are controlled well enough that another environment can create an
equivalent artifact. Exact byte-for-byte reproducibility requires additional controls such as
base-image digests and deterministic build metadata.

## Mental model

Treat the environment as a versioned input to the software, not as personal workstation state.

```text
Source code
    +
Python version
    +
Project metadata
    +
Dependency lockfile
    +
Configuration contract
    +
Container definition
    +
CI workflow
    =
Reproducible engineering environment
```

The main distinction is:

```text
pyproject.toml says what versions are acceptable.
uv.lock says what exact dependency graph was selected.
.venv contains the packages currently installed.
Dockerfile describes the runtime image.
CI proves the project can be rebuilt outside a developer's machine.
```

Deleting `.venv` should not destroy project knowledge. The environment must be recoverable from
the committed project files.

## Architecture and data flow

```text
Developer workstation
│
├── Git repository
│   ├── source code
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── tests
│   ├── Dockerfile
│   ├── compose.yaml
│   └── CI workflow
│
├── uv
│   ├── selects Python 3.13
│   ├── resolves dependencies
│   ├── writes uv.lock
│   └── synchronizes .venv
│
├── Local configuration
│   ├── environment variables
│   └── ignored .env file
│
└── Docker Compose
    ├── PostgreSQL
    ├── Redis
    └── one-off application container

Git push
    ↓
GitHub Actions
    ├── checks lockfile
    ├── installs from lockfile
    ├── lints and formats
    ├── type-checks
    ├── tests
    ├── audits dependencies
    ├── builds image
    └── smoke-tests image
```

### Trust boundaries

- Package indexes are external software-supply-chain inputs.
- Container registries are external artifact sources.
- `.env` contains local configuration and may contain secrets.
- GitHub Actions executes code from the repository.
- CI secrets, when introduced in later lessons, must remain outside workflow source.
- PostgreSQL and Redis accept local connections and must not be exposed publicly.

### State ownership

| State | Owner | Committed? |
|---|---|---:|
| Source and configuration schema | Git | Yes |
| Dependency constraints | `pyproject.toml` | Yes |
| Exact dependency resolution | `uv.lock` | Yes |
| Installed environment | `.venv` | No |
| Local secrets | `.env` or secret store | No |
| Safe configuration example | `.env.example` | Yes |
| Database data | Docker volume | No |
| Built image | Container registry or local Docker | No |
| CI definition | `.github/workflows/ci.yml` | Yes |

### Failure boundaries

- A dependency failure should stop synchronization before tests run.
- Invalid configuration should stop the health command with a non-zero exit code.
- A lint or type error should stop CI before image publication.
- A failed container smoke test should prevent release.
- A local service failure should not be hidden by the application.

## Design decisions

| Decision | Selected approach | Main alternative | Reason |
|---|---|---|---|
| Python version | Python 3.13 minor line | System default Python | Explicit version reduces machine drift while retaining modern library support |
| Package workflow | uv project workflow | pip plus manually managed virtual environment | One tool manages Python selection, locking, synchronization, execution, and build integration |
| Project metadata | `pyproject.toml` | Multiple tool-specific files | Current Python tooling converges on `pyproject.toml` |
| Lockfile | Commit `uv.lock` | Regenerate dependencies on every install | Exact resolution is required for repeatability |
| Configuration | Pydantic Settings | Direct `os.environ` access throughout code | Central typed validation creates one configuration contract |
| Formatting and linting | Ruff | Separate formatter and multiple linters | One fast tool reduces setup complexity |
| Type checking | mypy strict mode | No static checking | AI systems pass complex payloads between components; typed boundaries catch defects earlier |
| Local services | Docker Compose | Manual host installation | Compose gives the team a shared service definition |
| CI | GitHub Actions | Developer-only checks | CI validates the project in a clean environment |
| Container build | Multi-stage, non-root | Full development image as runtime | Smaller attack surface and fewer unnecessary tools |

Python 3.13 is selected for this course environment, not because newer is always worse. AI and
native-extension ecosystems sometimes adopt a new Python release at different speeds. A team
should upgrade intentionally after testing its complete dependency graph.

## Tooling

| Tool | Purpose | Why selected | Limitation | Alternative |
|---|---|---|---|---|
| Python | Primary AI engineering language | Dominant ML and GenAI ecosystem | Runtime and native package compatibility must be managed | C++, Java, Go, or TypeScript for role-specific components |
| uv | Python, dependencies, lockfile, execution | Fast unified project workflow | Teams with established tooling may standardize elsewhere | Poetry, PDM, pip-tools |
| Git | Version control | Industry standard | Does not prevent poor commit practices | Other VCS systems are uncommon in this market |
| GitHub | Pull requests and CI host | Common in interviews and industry | Employer may use GitLab or an internal platform | GitLab, Bitbucket, Azure DevOps |
| Pydantic Settings | Typed environment configuration | Validation and secret types | Configuration loading still needs operational policy | Dynaconf, environs, custom validation |
| Ruff | Linting and formatting | Fast and centralized configuration | Does not replace type checking | Black plus Flake8 or other linters |
| mypy | Static type checking | Mature Python type checker | Dynamic libraries may require stubs or configuration | Pyright |
| pytest | Automated testing | Flexible and widely used | Test quality still depends on design | unittest |
| pre-commit | Local quality hooks | Fast feedback before push | Hooks can be bypassed | CI remains mandatory |
| Docker | Runtime packaging | Consistent artifact across environments | Containers are not full virtual machines or a security boundary by themselves | Platform-specific packaging |
| Docker Compose | Local multi-service environment | Simple shared developer workflow | Not the final production orchestrator | Kubernetes or managed services |
| GitHub Actions | CI automation | Integrated with repository and pull requests | Workflow security requires careful permissions | GitLab CI, Jenkins, Azure Pipelines |
| pip-audit | Dependency vulnerability audit | Simple Python dependency check | Findings require triage and can have no immediate fix | Organization security scanner |

## Project structure

Create the following repository:

```text
ai-industry-labs/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── ai_industry_labs/
│       ├── __init__.py
│       ├── config.py
│       └── health.py
├── tests/
│   ├── test_config.py
│   └── test_health.py
├── .dockerignore
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── compose.yaml
├── Dockerfile
├── pyproject.toml
├── README.md
└── uv.lock
```

`uv.lock` is generated by uv. Do not create or edit it manually.

## Environment setup

### Install and verify prerequisites

Use the official installation instructions for your operating system:

- Python environment manager: <https://docs.astral.sh/uv/getting-started/installation/>
- Git: <https://git-scm.com/downloads>
- Docker: <https://docs.docker.com/get-docker/>

Verify:

```powershell
git --version
docker version
docker compose version
uv --version
```

On macOS or Linux, the same verification commands work in a POSIX shell.

If uv is not installed, its official installation documentation currently provides:

PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS or Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For a managed corporate environment, prefer the organization's approved package repository.
Review remote install scripts before executing them.

### Create the repository

PowerShell:

```powershell
New-Item -ItemType Directory -Path ai-industry-labs
Set-Location ai-industry-labs
git init -b main
uv init --package
uv python pin 3.13
```

POSIX shell:

```bash
mkdir ai-industry-labs
cd ai-industry-labs
git init -b main
uv init --package
uv python pin 3.13
```

The uv project workflow creates project metadata and later creates `.venv` and `uv.lock` when a
project command such as `uv sync`, `uv run`, or `uv lock` executes.

### Add dependencies

```powershell
uv add "pydantic>=2,<3" "pydantic-settings>=2,<3"
uv add --dev "pytest>=8,<10" "ruff>=0.11,<1" "mypy>=1,<3" "pre-commit>=4,<5" "pip-audit>=2,<3"
```

The broad ranges express compatibility policy. The generated `uv.lock` records the exact
versions used by this project.

### Use the final project metadata

Replace the generated `pyproject.toml` with the following.

**`pyproject.toml`**

```toml
[project]
name = "ai-industry-labs"
version = "0.1.0"
description = "Production engineering foundation for an industry-focused AI curriculum"
readme = "README.md"
requires-python = ">=3.13,<3.14"
dependencies = [
    "pydantic>=2,<3",
    "pydantic-settings>=2,<3",
]

[project.scripts]
ai-labs-health = "ai_industry_labs.health:main"

[dependency-groups]
dev = [
    "mypy>=1,<3",
    "pip-audit>=2,<3",
    "pre-commit>=4,<5",
    "pytest>=8,<10",
    "ruff>=0.11,<1",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/ai_industry_labs"]

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "RUF"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
python_version = "3.13"
strict = true
packages = ["ai_industry_labs"]
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
addopts = ["-q", "--strict-markers"]
testpaths = ["tests"]
```

Synchronize and verify the lockfile:

```powershell
uv lock
uv sync --locked
uv lock --check
```

The `--locked` option prevents a command from silently changing an out-of-date lockfile. This
behavior is particularly useful in CI.

## Data contract

This lesson's data contract is the application's configuration input and health-report output.

### Configuration input

| Variable | Type | Required | Default | Sensitive |
|---|---|---:|---|---:|
| `AI_LABS_SERVICE_NAME` | constrained string | No | `ai-industry-labs` | No |
| `AI_LABS_ENVIRONMENT` | enum | No | `local` | No |
| `AI_LABS_LOG_LEVEL` | enum | No | `INFO` | No |
| `AI_LABS_DATABASE_URL` | PostgreSQL DSN | No | local development URL | Contains credential |
| `AI_LABS_REDIS_URL` | Redis DSN | No | local development URL | Potentially |
| `AI_LABS_EXTERNAL_API_KEY` | secret string | No | unset | Yes |

### Valid configuration

```dotenv
AI_LABS_SERVICE_NAME=ai-industry-labs
AI_LABS_ENVIRONMENT=local
AI_LABS_LOG_LEVEL=INFO
AI_LABS_DATABASE_URL=postgresql://ai_labs:local-development-only@localhost:5432/ai_labs
AI_LABS_REDIS_URL=redis://localhost:6379/0
```

### Invalid configuration

```dotenv
AI_LABS_SERVICE_NAME=
AI_LABS_ENVIRONMENT=somewhere
AI_LABS_LOG_LEVEL=VERBOSE
AI_LABS_DATABASE_URL=not-a-database-url
```

The application must fail before performing work.

### Boundary configuration

Test:

- A service name with exactly 64 characters
- A blank service name
- An unknown environment
- An empty optional API key
- URLs containing special characters
- Environment-variable case behavior on Windows

### Health output

```json
{
  "status": "ok",
  "service": "ai-industry-labs",
  "environment": "local",
  "python_version": "3.13.x",
  "platform": "windows",
  "database_configured": true,
  "redis_configured": true,
  "external_api_key_configured": false,
  "generated_at": "2026-06-25T12:00:00Z"
}
```

The report indicates whether a secret is configured but never returns the secret.

### Provenance and versioning

- Configuration schema changes are reviewed through Git.
- `.env.example` documents safe keys without real secrets.
- `.env` remains local and ignored.
- Later lessons will move production secrets into a cloud secret manager.

## Establish the baseline

Before implementing the standardized environment, record the baseline:

| Check | Informal environment | Standardized target |
|---|---|---|
| Python version known | Often unclear | Exactly one minor line |
| Dependency graph recorded | No | `uv.lock` committed |
| Fresh setup documented | Partial | One README workflow |
| Configuration validated | No | Typed startup validation |
| Tests automated | No | Local hooks and CI |
| Container build | No | Tested non-root image |
| Local services | Manual | Compose definition |
| Dependency audit | Ad hoc | CI command |

Do not fabricate baseline timing. Measure it when completing the assignment.

## Minimal working implementation

### Create the package

**`src/ai_industry_labs/__init__.py`**

```python
"""Industry-focused AI engineering labs."""

__version__ = "0.1.0"
```

### Implement typed configuration

**`src/ai_industry_labs/config.py`**

```python
from enum import StrEnum
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class RuntimeEnvironment(StrEnum):
    LOCAL = "local"
    TEST = "test"
    CONTAINER = "container"
    CI = "ci"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AI_LABS_",
        extra="ignore",
    )

    service_name: str = Field(
        default="ai-industry-labs",
        min_length=1,
        max_length=64,
        pattern=r"^[a-z0-9][a-z0-9-]*$",
    )
    environment: RuntimeEnvironment = RuntimeEnvironment.LOCAL
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    database_url: PostgresDsn = PostgresDsn(
        "postgresql://ai_labs:local-development-only@localhost:5432/ai_labs"
    )
    redis_url: RedisDsn = RedisDsn("redis://localhost:6379/0")
    external_api_key: SecretStr | None = None
```

Pydantic Settings reads missing field values from environment variables and validates them
against the declared types. The `AI_LABS_` prefix prevents collisions with unrelated process
configuration.

### Implement the health report

**`src/ai_industry_labs/health.py`**

```python
import json
import platform
from datetime import UTC, datetime

from pydantic import BaseModel, ValidationError

from ai_industry_labs.config import Settings


class HealthReport(BaseModel):
    status: str
    service: str
    environment: str
    python_version: str
    platform: str
    database_configured: bool
    redis_configured: bool
    external_api_key_configured: bool
    generated_at: datetime


def build_health_report(settings: Settings | None = None) -> HealthReport:
    current = settings or Settings()

    return HealthReport(
        status="ok",
        service=current.service_name,
        environment=current.environment.value,
        python_version=platform.python_version(),
        platform=platform.system().lower(),
        database_configured=bool(current.database_url),
        redis_configured=bool(current.redis_url),
        external_api_key_configured=current.external_api_key is not None,
        generated_at=datetime.now(UTC),
    )


def main() -> int:
    try:
        report = build_health_report()
    except ValidationError as exc:
        safe_errors = [
            {
                "field": ".".join(str(part) for part in error["loc"]),
                "type": error["type"],
            }
            for error in exc.errors(include_url=False)
        ]
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": "invalid_configuration",
                    "details": safe_errors,
                },
                indent=2,
            )
        )
        return 2

    print(report.model_dump_json(indent=2))
    return 0
```

The health command validates configuration and reports environment metadata. It deliberately
does not connect to PostgreSQL or Redis yet; connection handling belongs in later backend and
observability lessons.

### Generate the lockfile and run

```powershell
uv lock
uv sync --locked
uv run ai-labs-health
```

Expected properties:

- Exit code is zero.
- Output is valid JSON.
- Python version begins with `3.13`.
- No password or API key appears.

PowerShell verification:

```powershell
$result = uv run ai-labs-health | ConvertFrom-Json
if ($result.status -ne 'ok') { throw 'Health check failed' }
if (-not $result.python_version.StartsWith('3.13')) { throw 'Unexpected Python version' }
```

POSIX verification:

```bash
uv run ai-labs-health
test "$?" -eq 0
```

## Production implementation

### Add safe configuration examples

**`.env.example`**

```dotenv
AI_LABS_SERVICE_NAME=ai-industry-labs
AI_LABS_ENVIRONMENT=local
AI_LABS_LOG_LEVEL=INFO
AI_LABS_DATABASE_URL=postgresql://ai_labs:local-development-only@localhost:5432/ai_labs
AI_LABS_REDIS_URL=redis://localhost:6379/0
# AI_LABS_EXTERNAL_API_KEY=replace-locally-never-commit-real-values
```

Copy it locally:

PowerShell:

```powershell
Copy-Item .env.example .env
```

POSIX:

```bash
cp .env.example .env
```

### Ignore local and generated state

**`.gitignore`**

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# Environments and configuration
.venv/
.env
.env.*
!.env.example

# Test and tool caches
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# Editors and operating systems
.idea/
.vscode/
.DS_Store
Thumbs.db

# Local data and generated artifacts
data/
artifacts/
*.log
```

Do not rely on `.gitignore` after a secret has already been committed. Remove the secret from
the repository, rotate it immediately, and follow the organization's history-remediation
process.

### Add tests

**`tests/test_config.py`**

```python
import pytest
from pydantic import ValidationError

from ai_industry_labs.config import RuntimeEnvironment, Settings


def test_settings_use_safe_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AI_LABS_SERVICE_NAME", raising=False)
    monkeypatch.delenv("AI_LABS_ENVIRONMENT", raising=False)

    settings = Settings(_env_file=None)

    assert settings.service_name == "ai-industry-labs"
    assert settings.environment is RuntimeEnvironment.LOCAL
    assert settings.external_api_key is None


def test_settings_read_prefixed_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_LABS_SERVICE_NAME", "ticket-assistant")
    monkeypatch.setenv("AI_LABS_ENVIRONMENT", "ci")
    monkeypatch.setenv("AI_LABS_LOG_LEVEL", "WARNING")

    settings = Settings(_env_file=None)

    assert settings.service_name == "ticket-assistant"
    assert settings.environment is RuntimeEnvironment.CI
    assert settings.log_level == "WARNING"


def test_settings_reject_blank_service_name(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_LABS_SERVICE_NAME", "")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_settings_reject_unknown_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_LABS_ENVIRONMENT", "unknown")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
```

**`tests/test_health.py`**

```python
import json

import pytest

from ai_industry_labs.config import Settings
from ai_industry_labs.health import build_health_report, main


def test_health_report_is_safe(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_LABS_EXTERNAL_API_KEY", "not-a-real-secret")
    settings = Settings(_env_file=None)

    report = build_health_report(settings)
    serialized = report.model_dump_json()

    assert report.status == "ok"
    assert report.external_api_key_configured is True
    assert "not-a-real-secret" not in serialized


def test_main_returns_zero_and_prints_json(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AI_LABS_ENVIRONMENT", "test")

    exit_code = main()
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output["status"] == "ok"
    assert output["environment"] == "test"


def test_main_rejects_invalid_configuration(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AI_LABS_ENVIRONMENT", "invalid")

    exit_code = main()
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 2
    assert output["error"] == "invalid_configuration"
    assert output["details"][0]["field"] == "environment"
```

Run:

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

Format once when needed:

```powershell
uv run ruff format .
uv run ruff check --fix .
```

Review automated fixes before committing them.

### Configure pre-commit

This configuration uses local hooks so the repository has one dependency source: its locked uv
environment.

**`.pre-commit-config.yaml`**

```yaml
default_install_hook_types:
  - pre-commit
  - pre-push

repos:
  - repo: local
    hooks:
      - id: ruff-check
        name: Ruff lint
        entry: uv run ruff check --fix
        language: system
        types_or: [python, pyi]

      - id: ruff-format
        name: Ruff format
        entry: uv run ruff format
        language: system
        types_or: [python, pyi]

      - id: mypy
        name: mypy
        entry: uv run mypy src
        language: system
        pass_filenames: false
        stages: [pre-push]

      - id: pytest
        name: pytest
        entry: uv run pytest
        language: system
        pass_filenames: false
        stages: [pre-push]
```

Install and test hooks:

```powershell
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
uv run pre-commit run --all-files
```

Pre-commit provides fast local feedback. CI remains authoritative because hooks can be skipped.

### Add a multi-stage container build

The uv Docker guide documents the use of dedicated uv images and partial installs for Docker
layer caching. This example pins the uv version verified for this lesson. In a production
repository, also pin base images by digest through an automated update process.

**`Dockerfile`**

```dockerfile
# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:0.11.24 AS uv

FROM python:3.13-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY --from=uv /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

COPY src ./src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

FROM python:3.13-slim AS runtime

RUN groupadd --system app \
    && useradd --system --gid app --create-home app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER app

CMD ["ai-labs-health"]
```

Why use two Python stages?

- The builder contains uv and build-time state.
- The runtime receives only the synchronized environment.
- Development tools are excluded through `--no-dev`.
- The project is installed non-editably.
- The process runs as a non-root user.

**`.dockerignore`**

```dockerignore
.git
.github
.venv
.env
.env.*
!.env.example
__pycache__
*.pyc
.pytest_cache
.mypy_cache
.ruff_cache
tests
data
artifacts
*.log
```

Build and run:

```powershell
docker build --tag ai-industry-labs:local .
docker run --rm ai-industry-labs:local
```

Expected result: the container prints a valid health report and exits with code zero.

### Add local PostgreSQL and Redis

These services are prepared for later backend lessons. They are not exposed beyond the local
machine.

**`compose.yaml`**

```yaml
name: ai-industry-labs

services:
  postgres:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: ai_labs
      POSTGRES_USER: ai_labs
      POSTGRES_PASSWORD: local-development-only
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ai_labs -d ai_labs"]
      interval: 5s
      timeout: 3s
      retries: 10
    restart: unless-stopped

  redis:
    image: redis:8-alpine
    command: ["redis-server", "--appendonly", "yes"]
    ports:
      - "127.0.0.1:6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 10
    restart: unless-stopped

  app:
    profiles: ["tools"]
    build:
      context: .
    environment:
      AI_LABS_ENVIRONMENT: container
      AI_LABS_DATABASE_URL: postgresql://ai_labs:local-development-only@postgres:5432/ai_labs
      AI_LABS_REDIS_URL: redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    read_only: true
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true

volumes:
  postgres-data:
  redis-data:
```

Start and inspect:

```powershell
docker compose config
docker compose up -d postgres redis
docker compose ps
docker compose --profile tools run --rm app
```

Stop containers while preserving data:

```powershell
docker compose down
```

Remove local database data only when intentionally resetting the lab:

```powershell
docker compose down --volumes
```

The last command is destructive for local database state. Do not use it against an environment
whose data must be preserved.

### Add continuous integration

The current uv GitHub Actions guide recommends the official `astral-sh/setup-uv` action and
shows pinning the action and uv version. The workflow below uses the versions verified on
June 25, 2026.

**`.github/workflows/ci.yml`**

```yaml
name: CI

on:
  pull_request:
  push:
    branches:
      - main

permissions:
  contents: read

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  quality:
    name: Quality - ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        os:
          - ubuntu-latest
          - windows-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v6

      - name: Install uv
        uses: astral-sh/setup-uv@08807647e7069bb48b6ef5acd8ec9567f424441b # v8.1.0
        with:
          version: "0.11.24"
          enable-cache: true

      - name: Install Python
        run: uv python install 3.13

      - name: Verify lockfile
        run: uv lock --check

      - name: Synchronize environment
        run: uv sync --locked --dev

      - name: Lint
        run: uv run ruff check .

      - name: Verify formatting
        run: uv run ruff format --check .

      - name: Type check
        run: uv run mypy src

      - name: Test
        run: uv run pytest

      - name: Audit Python dependencies
        run: uv run pip-audit

  container:
    name: Container smoke test
    runs-on: ubuntu-latest
    needs: quality
    timeout-minutes: 15

    steps:
      - name: Check out repository
        uses: actions/checkout@v6

      - name: Build image
        run: docker build --tag ai-industry-labs:ci .

      - name: Run smoke test
        run: docker run --rm ai-industry-labs:ci
```

The workflow grants only read access to repository contents. Add permissions only when a job
demonstrably needs them.

### Add the developer workflow

**`README.md`**

````markdown
# AI Industry Labs

Production engineering foundation for the industry-focused AI curriculum.

## Requirements

- Git
- Docker with Docker Compose
- uv

## Setup

```shell
uv python install 3.13
uv sync --locked
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

## Verify

```shell
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv run ai-labs-health
```

## Local services

```shell
docker compose up -d postgres redis
docker compose ps
docker compose --profile tools run --rm app
```

## Stop services

```shell
docker compose down
```
````

### Commit the environment

Before committing:

```powershell
git status
git diff --check
uv run pre-commit run --all-files
git add .
git status
git commit -m "build: establish reproducible AI engineering environment"
```

Create feature work on a branch:

```powershell
git switch -c lesson/python-production
```

Use pull requests for review. Protect the main branch when working in a team so CI must pass
before merge.

## Testing strategy

### Unit tests

Protect:

- Configuration defaults
- Environment-variable parsing
- Secret redaction
- Health-report construction
- Failure exit codes

### Integration tests

This lesson's integration checks are:

- Synchronizing from `uv.lock`
- Building the package
- Building the container
- Starting PostgreSQL and Redis
- Running the application container with Compose configuration

Later lessons will add actual database and Redis connection tests.

### Contract tests

The health-report JSON fields form a contract. Downstream automation may depend on:

- `status`
- `service`
- `environment`
- `python_version`
- Secret-presence booleans

Changing these fields requires a deliberate compatibility decision.

### End-to-end test

A clean CI runner:

```text
checks out source
→ installs uv and Python
→ validates lockfile
→ synchronizes packages
→ runs quality checks
→ builds image
→ runs health command inside image
```

### Security tests

- `.env` is ignored.
- The health report does not expose the API key.
- The container runs as a non-root user.
- CI permissions are read-only.
- `pip-audit` checks known Python dependency advisories.

### Failure tests

- Invalid environment name returns exit code 2.
- Empty service name fails validation.
- An outdated lockfile fails `uv lock --check`.
- A formatting difference fails CI.
- A container build failure blocks the smoke-test job.

## Evaluation

No measured results are claimed by this lesson. Complete the table after running the project.

| Metric | Measurement command or procedure | Target | Measured result |
|---|---|---:|---|
| Fresh setup success | Clone into a clean directory and follow README | Pass without undocumented steps | |
| Lockfile consistency | `uv lock --check` | Exit code 0 | |
| Lint | `uv run ruff check .` | 0 violations | |
| Format | `uv run ruff format --check .` | Pass | |
| Type checking | `uv run mypy src` | 0 errors | |
| Tests | `uv run pytest` | All pass | |
| Dependency audit | `uv run pip-audit` | No unaccepted findings | |
| Local health | `uv run ai-labs-health` | Exit code 0 | |
| Container health | `docker run --rm ai-industry-labs:local` | Exit code 0 | |
| Compose services | `docker compose ps` | PostgreSQL and Redis healthy | |
| Secret exposure | Search tracked files and health output | No real secrets | |
| CI | Pull-request checks | Windows and Linux pass | |
| Setup time | Measure clean `uv sync --locked` | Record baseline | |
| Image size | `docker image inspect` | Record and justify | |

### Business metric

Ask a second person to clone the repository and reach a passing container health check. Record:

- Time to first successful run
- Number of undocumented questions
- Number of manual corrections

The initial target is zero undocumented corrections.

## Failure modes and debugging

| Symptom | Likely causes | Diagnostic evidence | Corrective action | Prevention |
|---|---|---|---|---|
| `uv` command not found | Installer path not loaded | `Get-Command uv` or `which uv` fails | Restart shell or add install location to PATH | Verify tools immediately after installation |
| Wrong Python version | Existing environment or pin mismatch | `uv run python --version` differs from `.python-version` | Run `uv python install 3.13`, delete and resync `.venv` if needed | Commit `.python-version` and set `requires-python` |
| `uv lock --check` fails | `pyproject.toml` changed without updating lockfile | Git diff shows dependency change | Run `uv lock`, review, and commit `uv.lock` | Make lock check mandatory in CI |
| Local import works but CI import fails | Untracked package installed locally | `uv sync` removes an undeclared package | Add dependency through `uv add` | Use exact sync and recreate environments regularly |
| Settings unexpectedly read a value | Shell or `.env` contains stale variable | Print non-sensitive environment keys; inspect `.env` | Remove or update stale configuration | Centralize prefix and document precedence |
| Secret appears in logs | Object or exception was serialized carelessly | CI log or local output contains credential | Remove output, rotate secret, remediate history if committed | Use secret types and explicit safe logging |
| Ruff differs between machines | Different unlocked tool versions | `uv run ruff --version` differs | Synchronize from committed lockfile | Run tools through `uv run` |
| mypy reports missing imports | Missing stubs or wrong environment | `uv run mypy -v` shows resolution paths | Install maintained stubs or configure library boundary | Type-check in the locked environment |
| Docker build cannot find package | Project metadata or copy order is wrong | Build log fails during `uv sync` | Confirm source path and build-system configuration | Smoke-test image in CI |
| Container writes fail | Runtime filesystem is read-only | Permission error inside Compose app | Write only to declared temporary or persistent paths | Design explicit writable paths |
| PostgreSQL port is busy | Host already uses 5432 | Docker reports bind failure | Stop conflicting service or change local mapping | Document configurable host ports |
| PostgreSQL remains unhealthy | Invalid volume state or configuration | `docker compose logs postgres` | Inspect logs; intentionally reset local volume if disposable | Use health checks and documented reset process |
| Redis data disappears | Container had no volume or volume was removed | Compose volume absent | Restore or recreate local data | Declare named volume |
| CI passes but local hook fails | Local environment is stale | `uv sync --locked` changes packages | Resynchronize and reinstall hooks | Document one verification command |
| Dependency audit fails | Known advisory in direct or transitive package | `pip-audit` identifies package and advisory | Upgrade, remove, mitigate, or formally accept risk | Schedule dependency updates and audits |
| CI cache grows on self-hosted runner | Cache is never pruned | Disk usage increases | Prune or relocate uv cache | Add runner-specific cache policy |

## Security, privacy, and governance

### Package supply chain

A lockfile provides consistency, not proof of safety. A locked malicious or vulnerable package
remains malicious or vulnerable.

Controls:

- Review direct dependencies.
- Prefer official package indexes and organization mirrors.
- Commit and review lockfile changes.
- Run a dependency audit.
- Generate a software bill of materials when required.
- Upgrade dependencies through reviewed pull requests.

The current uv documentation supports exporting a CycloneDX SBOM:

```powershell
uv export --format cyclonedx1.5 > sbom.cdx.json
```

Treat the SBOM as a generated artifact unless organizational policy requires committing it.

### Secrets

Controls:

- Commit `.env.example`, never `.env`.
- Store production secrets in a managed secret store.
- Use GitHub repository or environment secrets only when CI needs them.
- Do not pass secrets through Docker build arguments.
- Use Docker build secret mounts for private dependency access.
- Redact secrets from logs and exceptions.
- Rotate a secret immediately after exposure.

### Git history

`.gitignore` does not remove an already committed file. If a secret enters history:

- Revoke or rotate it first.
- Notify the security owner.
- Remove it from active files.
- Follow the approved history-remediation process.
- Review logs and downstream copies.

### Container controls

This lesson's runtime:

- Runs as a non-root user.
- Excludes development dependencies.
- Uses a read-only filesystem in Compose.
- Uses `no-new-privileges`.
- Exposes database ports only on loopback.

Containers still share the host kernel. Stronger isolation may be required for untrusted code in
later agent lessons.

### CI controls

- Default workflow permission is `contents: read`.
- No production credentials are required.
- Actions and uv are pinned to reviewed versions.
- Pull-request code must be treated as untrusted.
- Do not expose privileged secrets to workflows triggered by untrusted forks.

### Privacy

This lesson uses no customer data. Continue using synthetic or non-sensitive data until a later
lesson explicitly defines data governance and access controls.

### Licence compliance

Record:

- Direct dependency licences
- Base-image licence and provenance
- Restrictions on models and datasets introduced later

An automated scanner assists review but does not replace legal policy.

## Performance and cost

### Synchronization time

Measure a warm and cold environment:

PowerShell:

```powershell
Measure-Command { uv sync --locked }
uv cache clean
Measure-Command { uv sync --locked }
```

Clearing the cache affects other local uv projects and should be done intentionally.

POSIX:

```bash
time uv sync --locked
```

### Docker build time

```powershell
Measure-Command { docker build --tag ai-industry-labs:benchmark . }
Measure-Command { docker build --tag ai-industry-labs:benchmark . }
```

The second build should benefit from unchanged dependency layers.

### Image size

PowerShell:

```powershell
docker image inspect ai-industry-labs:local --format '{{.Size}}'
```

Record the size and investigate unexpected growth.

### CI cost

This project uses:

- Two quality jobs
- One Docker job
- No paid model calls
- No GPU runner

Reduce unnecessary CI cost by:

- Cancelling superseded runs
- Caching uv packages
- Separating fast quality checks from slower image checks
- Avoiding repeated environment resolution

Do not remove important cross-platform checks merely to optimize a small pipeline.

## Deployment and rollback

This lesson does not deploy a network service. Its production artifact is a smoke-tested
container image that later lessons will extend.

### Package

```powershell
uv build
```

Verify the `dist/` directory contains a wheel and source distribution.

### Build an image tagged with the Git commit

PowerShell:

```powershell
$tag = git rev-parse --short HEAD
docker build --tag "ai-industry-labs:$tag" .
docker run --rm "ai-industry-labs:$tag"
```

POSIX:

```bash
tag="$(git rev-parse --short HEAD)"
docker build --tag "ai-industry-labs:$tag" .
docker run --rm "ai-industry-labs:$tag"
```

### Release strategy

For later deployments:

- Build once in CI.
- Tag the immutable image with the commit SHA.
- Scan it.
- Promote the same artifact between environments.
- Do not rebuild separately for staging and production.

### Rollback

Rollback means redeploying the previously approved image tag. A rollback is possible only when:

- Previous image tags are retained.
- Configuration remains compatible.
- Database migrations are backward-compatible or reversible.
- The deployment process records the last known good version.

## Observability and operations

### Logs

The health command emits machine-readable JSON. Later services will emit structured application
logs.

Do not log:

- API keys
- Passwords
- Complete connection strings
- Customer content

### Metrics

Track:

- CI pass rate
- CI duration
- Fresh setup duration
- Dependency-audit findings
- Container build duration
- Container image size
- Number of undocumented setup corrections

### Traces

Distributed tracing is not useful for this one-process CLI yet. It will be introduced when
requests cross API, retrieval, model, and tool boundaries.

### Alerts

For this repository, actionable alerts are:

- Main branch CI failure
- Dependency security finding
- Container build failure
- Required branch-protection check bypass

### Ownership

Assign:

- Repository owner
- Dependency-update owner
- CI owner
- Security finding owner
- Container base-image owner

### Runbook

When setup or CI fails:

```text
Confirm tool versions
→ verify Python pin
→ run uv lock --check
→ run uv sync --locked
→ run checks individually
→ inspect Docker or CI logs
→ reproduce in a clean environment
→ fix source configuration, not only local state
```

## Practical assignment

### Scenario

You are joining a new Applied AI team. Create the repository that all later AI projects will
use.

### Requirements

- Create the exact project structure from this lesson.
- Use Python 3.13.
- Use uv and commit `uv.lock`.
- Implement typed settings.
- Implement the health command.
- Add unit tests.
- Add Ruff, mypy, pytest, and pre-commit.
- Add a non-root Docker image.
- Add PostgreSQL and Redis through Compose.
- Add Windows and Linux CI.
- Add dependency auditing.
- Document setup and reset procedures.

### Constraints

- Do not use a paid service.
- Do not commit `.env`.
- Do not hard-code a real credential.
- Do not install application dependencies with an undocumented manual command.
- Do not disable checks merely to make CI pass.

### Required artifacts

- Git repository
- `pyproject.toml`
- `uv.lock`
- Source package
- Tests
- `.env.example`
- `.gitignore`
- Pre-commit configuration
- Dockerfile
- Compose file
- CI workflow
- README
- Completed evaluation table
- Short security review

### Acceptance criteria

- A second person can clone and run the project.
- `uv lock --check` passes.
- All quality checks pass.
- Invalid configuration fails safely.
- Health output contains no secrets.
- PostgreSQL and Redis become healthy.
- Container runs as non-root.
- CI passes on Windows and Linux.
- Dependency findings are resolved or documented.
- Setup timing and image size are recorded.

### Stretch goals

- Pin container base images by digest.
- Add a CycloneDX SBOM artifact in CI.
- Add signed commits or organization-required provenance.
- Add an automated dependency-update workflow.
- Test Python 3.13 on multiple operating systems and document platform-specific differences.

## Interview preparation

### Concept questions

**Why commit a lockfile when `pyproject.toml` already lists dependencies?**

A strong answer explains that constraints define acceptable versions, while a lockfile records
the exact resolved direct and transitive graph. The lockfile supports reproducibility and
reviewable upgrades.

**What is the difference between a virtual environment and a container?**

A strong answer explains that a virtual environment isolates Python packages, while a container
packages the application filesystem and process environment. A container still shares the host
kernel and is not automatically secure.

**Why pin a Python minor version?**

A strong answer connects interpreter compatibility, native dependencies, consistent typing and
runtime behavior, and controlled upgrades.

**Why are development dependencies excluded from the runtime image?**

A strong answer covers attack surface, image size, dependency risk, and separation between build
and execution needs.

### Implementation questions

**How would you prove that a developer has an undeclared local dependency?**

Delete or recreate `.venv`, run exact synchronization from the lockfile, and execute tests in CI
or a clean container.

**How should application code read configuration?**

Through a centralized typed settings object. Business modules should not independently read
arbitrary environment variables.

**How do you prevent secrets from appearing in a health endpoint?**

Return presence or connectivity status, never credential values; use secret-aware types and
explicit serialization.

### Debugging scenarios

**Tests pass locally but CI reports `ModuleNotFoundError`. What do you check?**

- Whether the dependency is declared
- Whether the project package is installed
- Source-layout and build configuration
- Differences between local and CI Python versions
- Whether local state contains undeclared packages

**Docker builds locally but fails in CI. What do you check?**

- Build context and ignored files
- Platform-specific files or line endings
- Uncommitted lockfile changes
- Base-image access
- BuildKit requirements
- Architecture compatibility

**A secret was committed and then deleted in the next commit. Is the problem solved?**

No. The secret remains in history and copies may exist in CI logs, forks, or caches. Rotate it
first, notify the owner, and follow history-remediation policy.

### System-design questions

**How would you standardize environments for ten AI teams?**

A strong answer includes supported templates, central CI actions, approved base images,
dependency update automation, secret management, artifact provenance, documentation, and an
upgrade policy without blocking team-specific dependencies.

**When would you choose a managed development environment instead of local Compose?**

When data access, compute requirements, compliance, networking, or workstation consistency
justify a centrally governed environment.

### Tradeoff questions

**Ruff and mypy overlap. Why use both?**

Ruff handles formatting and many static lint rules. mypy analyzes type relationships across
code. Neither substitutes for runtime tests.

**Why not use `latest` tags everywhere?**

Mutable tags make builds change without a source-code review. Use reviewed versions and, for
strong production reproducibility, immutable image digests.

## Production-readiness checklist

- [ ] Python minor version is pinned.
- [ ] `requires-python` matches the pin.
- [ ] Runtime and development dependencies are separated.
- [ ] `uv.lock` is committed.
- [ ] `uv lock --check` passes.
- [ ] A fresh `uv sync --locked` succeeds.
- [ ] `.venv` is ignored.
- [ ] `.env` is ignored.
- [ ] `.env.example` contains no real secrets.
- [ ] Configuration is typed and validated.
- [ ] Secret values are excluded from output and logs.
- [ ] Ruff lint passes.
- [ ] Ruff format check passes.
- [ ] mypy passes.
- [ ] pytest passes.
- [ ] Local pre-commit and pre-push hooks are installed.
- [ ] PostgreSQL health check passes.
- [ ] Redis health check passes.
- [ ] Docker image builds.
- [ ] Runtime container uses a non-root user.
- [ ] Runtime image excludes development dependencies.
- [ ] Container smoke test passes.
- [ ] CI passes on Windows and Linux.
- [ ] CI permissions follow least privilege.
- [ ] Dependency audit is reviewed.
- [ ] Base-image update responsibility is assigned.
- [ ] Setup time is measured.
- [ ] Image size is measured.
- [ ] Rollback artifact strategy is documented.
- [ ] README was tested by someone other than the author.

## Lesson summary

You created the engineering contract that every later AI lesson will depend on:

- Python version is explicit.
- Dependencies are constrained and locked.
- Local configuration is typed.
- Secrets stay outside source control.
- Quality checks run locally and in CI.
- PostgreSQL and Redis have shared local definitions.
- The runtime image is smaller and non-root.
- Environment failures produce observable, actionable evidence.

The most important tradeoff is convenience versus control. The selected workflow adds files and
checks, but it eliminates a large class of hidden workstation state and unreproducible
demonstrations.

Common mistakes include:

- Committing `.venv`
- Omitting the lockfile
- Treating `.env` as a secret manager
- Installing packages outside the project workflow
- Running a development image in production
- Trusting local hooks without CI
- Using mutable image tags without review
- Logging complete configuration objects

The next lesson, **Python for Production AI**, will build on this repository. It will deepen
typing, package design, interfaces, error classification, resource handling, logging, and
testable provider abstractions.

## Official references

- uv project workflow: <https://docs.astral.sh/uv/guides/projects/>
- uv locking and synchronization: <https://docs.astral.sh/uv/concepts/projects/sync/>
- uv with GitHub Actions: <https://docs.astral.sh/uv/guides/integration/github/>
- uv with Docker: <https://docs.astral.sh/uv/guides/integration/docker/>
- uv with pre-commit: <https://docs.astral.sh/uv/guides/integration/pre-commit/>
- Python virtual environments: <https://docs.python.org/3/library/venv.html>
- Ruff configuration: <https://docs.astral.sh/ruff/configuration/>
- mypy configuration: <https://mypy.readthedocs.io/en/stable/config_file.html>
- Pydantic Settings: <https://docs.pydantic.dev/latest/concepts/pydantic_settings/>
- Docker multi-stage builds: <https://docs.docker.com/build/building/multi-stage/>
- Docker build secrets: <https://docs.docker.com/build/building/secrets/>
- Docker Compose quickstart: <https://docs.docker.com/compose/gettingstarted/>
- GitHub Actions for Python: <https://docs.github.com/en/actions/tutorials/build-and-test-code/python>
- GitHub Actions secrets: <https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets>
- pre-commit: <https://pre-commit.com/>
