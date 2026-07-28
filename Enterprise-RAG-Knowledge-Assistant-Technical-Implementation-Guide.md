# Enterprise RAG Knowledge Assistant Technical Implementation Guide

Updated: July 23, 2026

This is the hands-on build guide for the **Enterprise RAG Knowledge Assistant**. Its normative
requirements are defined in the companion
[Enterprise RAG Knowledge Assistant Production Implementation Guide](Enterprise-RAG-Knowledge-Assistant-Production-Implementation-Guide.md).
If the two guides conflict, the production guide wins. Update both guides in the same pull request
when a requirement or architecture decision changes.

This guide turns those requirements into an executable repository, implementation stages,
commands, tests, evaluation gates, operational evidence, and a reviewer-ready proof path. It
builds an internal assistant over enterprise policies, product manuals, contracts, and procedures
using only public, synthetic, or explicitly approved corpora.

Relevant local curriculum sources:

- [Deep research report](deep-research-report.md), which identifies Enterprise RAG as Project 2.
- [AI Industry Roadmap and Projects](AI-Industry-Roadmap-and-Projects.md), especially Phase 2.
- [Complete AI Industry Lesson Coverage and Production Plan](AI-Industry-Complete-Lesson-Coverage-Map.md),
  especially Lessons 12-18 and portfolio coverage.
- [AI Industry Curriculum](AI-Industry-Curriculum.md), especially the enterprise RAG project.
- [AI Industry Detailed Lessons](AI-Industry-Detailed-Lessons.md), especially document ingestion,
  semantic retrieval, production RAG, evaluation, security, and operations.
- [SupportOps Technical Implementation Guide](SupportOps-AI-Copilot-Technical-Implementation-Guide.md)
  for the predecessor project's build-and-evidence convention.
- [SupportOps completed documentation](supportops-ai-copilot/docs/architecture.md) for the
  architecture, contracts, stage records, reports, runbooks, learning notes, and progress-log
  pattern that this project adapts.

## How to use this guide

Build one stage at a time. Every stage uses the same contract:

1. Read the objective and prerequisites.
2. Create only the listed files and contracts.
3. Implement the steps in order.
4. Run the commands and tests.
5. Inspect the required telemetry.
6. Commit the evidence and stage record.
7. Move on only when every `Done when` item is true.

The fastest useful vertical slice is:

```text
upload synthetic document
-> store immutable source object
-> parse and chunk
-> build lexical and dense indexes
-> search with tenant and ACL filters
-> rerank authorized chunks
-> answer from an evidence packet
-> show exact citations
-> record feedback and trace
```

Do not start by optimizing generation. Retrieval quality, permission enforcement, provenance,
freshness, and citation validity are the system's foundation.

## 0. Scope, non-goals, and prerequisites

### In scope

- Multi-tenant users, groups, roles, and document ACLs.
- PDF, HTML, EML email, DOCX, XLSX, TXT, and Markdown ingestion.
- OCR routing for scanned PDF pages and images.
- Table-aware extraction and provenance.
- English as the canonical first-release language, with language recorded on every parsed block.
- Immutable source objects, document versions, stable chunk identities, and content hashes.
- PostgreSQL full-text search plus pgvector as the default hybrid index.
- Lexical, dense, reciprocal-rank-fusion hybrid, and cross-encoder-reranked retrieval.
- Permission filters before candidates are returned, reranked, cached, or sent to a model.
- Evidence packets, grounded generation, exact-version citations, and controlled abstention.
- Incremental indexing, update propagation, access revocation, and deletion propagation.
- Retrieval and answer evaluation as separate systems, plus a BEIR-style public benchmark adapter.
- Feedback, observability, cost accounting, security tests, CI/CD, rollback, restore, and pilot.
- An optional secure, read-only MCP search surface after the ordinary API is complete.

### Non-goals for the first production-style version

- Autonomous write actions or model-controlled permissions.
- Medical, legal, financial, or safety-critical decision making.
- Training an embedding, reranker, or generation model.
- Graph RAG, agentic web research, multimodal generation, or knowledge-graph construction.
- Kubernetes, OpenSearch, or a distributed vector database.
- Perfect parsing of every proprietary file format.
- Multilingual production claims without language-specific lexical, embedding, reranking, UX, and
  evaluation evidence.

OpenSearch is a later scale adapter. It must implement the same retrieval interface and pass the
same ACL, quality, freshness, and deletion tests before it can replace the PostgreSQL default.

### Local prerequisites

Install:

- Git.
- Python 3.12.
- `uv`.
- Docker with Docker Compose.
- Node.js LTS and npm.
- At least 12 GB available RAM and 20 GB free disk for the full local stack.
- Optional local generation-provider credentials. Mock generation is the default in tests.

Tesseract OCR runs inside the worker image, so a host installation is not required.

Before starting, be able to explain:

- HTTP request and response basics.
- Tables, primary keys, foreign keys, indexes, transactions, and migrations.
- Authentication versus authorization.
- Why retrieved document text is untrusted.
- Precision, recall, MRR, nDCG, latency percentiles, and a labeled evaluation case.

### Pre-build discovery gate

Before Stage 1:

1. Select one bounded employee knowledge workflow and its current non-AI search/manual fallback.
2. Identify employees, knowledge owners, compliance/search admins, platform/security operators, and
   escalation/recourse owners.
3. Measure or define a plan to measure baseline task success/time, zero results, reformulations,
   escalations, source freshness, and cost.
4. Approve the public/synthetic/authorized pilot corpus, licenses, classifications, owners, and
   prohibited source classes.
5. Define authority, effective-date, conflict, staleness, legal-hold, and deletion policies.
6. Define in-scope formats, languages, query types, pilot cohort, non-goals, success/guardrail/SLO/
   cost metrics, stop conditions, and human recourse.
7. Create `docs/product-requirements.md`, `docs/metric-tree.md`, `docs/risk-register.md`, and the
   initial `docs/source-register.md`.
8. Map every `RAG-*` requirement to an acceptance criterion and evidence owner.

Do not create a source connector, embed a document, or select a generation provider until the data
access assumptions and corpus use are at least `locally verified`.

### Canonical executable stack

| Layer | Canonical choice |
|---|---|
| Language and package tool | Python 3.12 and `uv` |
| API and validation | FastAPI and Pydantic v2 |
| Authentication | OIDC discovery/JWKS with `PyJWT[crypto]`; explicitly gated local adapter |
| ORM and migrations | SQLAlchemy 2 and Alembic |
| Primary database | PostgreSQL 16 |
| Dense index | pgvector with cosine distance |
| Lexical index | PostgreSQL `tsvector`, GIN, and `websearch_to_tsquery` |
| Hybrid fusion | Application-layer weighted reciprocal rank fusion |
| Queue and cache | Redis and RQ |
| Source object storage | S3-compatible storage; MinIO locally |
| Parsing | PyMuPDF, Beautiful Soup, python-docx, openpyxl, and format-specific adapters |
| OCR | Tesseract through `pytesseract`; OCR only pages that need it |
| Malware scanning | ClamAV daemon through a project-owned `MalwareScanner` adapter |
| Embeddings | `sentence-transformers` behind `EmbeddingProvider` |
| Default embedding model | `sentence-transformers/all-MiniLM-L6-v2`, 384 dimensions |
| Reranking | `sentence-transformers` cross-encoder behind `Reranker` |
| Default reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| Generation | Provider-neutral `GenerationProvider`; deterministic mock plus hosted HTTP adapter |
| Web | React, Vite, and TypeScript |
| Tests and quality | pytest, Ruff, mypy, and Playwright |
| Telemetry | OpenTelemetry, Prometheus, Grafana, and structured JSON logs |
| Local runtime | Docker Compose |
| Reference cloud | AWS: ECS Fargate, RDS PostgreSQL/pgvector, ElastiCache, S3, ALB/ACM, Secrets Manager |
| Optional MCP | Official Python `mcp` package, streamable HTTP transport, OIDC client assertion |

Model names are replaceable configuration, not business logic. The embedding and reranker require
both an immutable upstream revision and a verified local artifact-manifest SHA-256. A mutable model
name such as `main` or `latest` is invalid outside an explicitly insecure local experiment. Record
the model ID, revision, manifest digest, library version, and runtime device in every index build
and query trace.

## 1. Final system and invariants

The runtime has four application services:

- `api`: identity-aware upload, catalog, search, answer, feedback, and administration endpoints.
- `worker`: parsing, OCR, chunking, embedding, indexing, deletion, and evaluation jobs.
- `web`: employee search/answer UI and knowledge-owner operations UI.
- `mcp`: optional read-only search adapter with the same authorization service as the API.

It depends on PostgreSQL/pgvector, Redis, MinIO, a local embedding model, a local reranker, and an
optional hosted generation provider.

```mermaid
flowchart LR
    U[Employee or knowledge owner] --> W[React web]
    W --> A[FastAPI API]
    A --> ID[Trusted identity and ACL service]
    A --> P[(PostgreSQL + pgvector + FTS)]
    A --> R[(Redis)]
    A --> O[(S3 or MinIO)]
    A --> Q[RQ queues]
    Q --> K[Ingestion and eval workers]
    K --> O
    K --> P
    A --> H[Hybrid retrieval]
    H --> ID
    H --> P
    H --> X[Cross-encoder reranker]
    X --> C[Context and evidence packet]
    C --> G[Generation gateway]
    G --> V[Citation and grounding validator]
    V --> A
    A --> T[Logs, metrics, traces, and cost]
    M[Read-only MCP client] --> S[MCP search adapter]
    S --> ID
    S --> H
```

Non-negotiable invariants:

- Deny access when identity, tenant, group membership, ACL, or version status is uncertain.
- Apply permissions in database candidate queries, before reranking and context assembly.
- Never trust a client-supplied tenant, role, group, or ACL decision.
- Every chunk maps to an immutable source object, document version, parser version, and exact span.
- A citation resolves to the same authorized document version and span used for the answer.
- Retrieved text is data, never an instruction source.
- Unknown, conflicting, stale, or insufficient evidence causes abstention or a clarification.
- Reprocessing, updates, access changes, and deletion are idempotent and observable.
- Retrieval and answer quality are evaluated separately.
- Every answer records the query, identity scope hash, index version, embedding model, reranker,
  prompt, generation model, citations, latency, and cost.

## 2. Starter quality gates

These are portfolio-grade **starting gates**, not universal business truth. Calibrate them with a
representative labeled set and record any change in an architecture decision and eval changelog.
Security gates marked zero-tolerance cannot be relaxed to make a release pass.

| Area | Starter gate |
|---|---|
| ACL isolation | 0 unauthorized documents in candidates, cache entries, context, answer, citation, or MCP output |
| Revocation | denied at query time immediately; permission-aware caches invalidated within 60 seconds |
| Delete propagation | source, chunks, indexes, and user-visible citations removed within 5 minutes at P95 |
| Index freshness | 95% of documents up to 100 pages searchable within 5 minutes of accepted upload |
| Provenance | 1.00 of sampled release chunks reconstruct source, exact version/span, parser, chunker, and ACL lineage |
| Ingestion idempotency | 1.00 of duplicate/replay/update/delete lifecycle tests pass |
| Business retrieval | Recall@10 >= 0.85, MRR@10 >= 0.65, nDCG@10 >= 0.75 |
| Reranker | nDCG@10 improves by >= 0.03 over hybrid on the calibration set or is disabled |
| Citation validity | 1.00 of release-set citations resolve to the exact authorized indexed version and span |
| Citation correctness | >= 0.95 citations support their associated claims |
| Citation coverage | >= 0.95 factual claims have at least one supporting citation |
| Groundedness | >= 0.90 on the approved answer rubric |
| Answer correctness | >= 0.85 on answerable business cases |
| Abstention | >= 0.95 recall on unanswerable cases; <= 0.15 false-refusal rate on answerable cases |
| Incorrect non-abstention | <= 0.05 on the unanswerable/conflict release set |
| Injection and poisoning | 0 critical safety-set failures |
| Search latency | warmed P95 <= 750 ms for top-10 hybrid plus reranking in the reference environment |
| Answer latency | warmed P95 <= 5 seconds in the reference environment |
| Query availability | 99.5% during declared pilot service hours |
| Availability exercise | API remains searchable without generation; failed jobs are recoverable from DLQ |
| Cost | configurable pilot budget; initial alert at USD 0.05 per generated answer |

Record hardware, corpus size, provider, concurrency, and warm/cold status beside every latency
number. Never compare unqualified benchmark numbers.

## 3. Build order

1. Repository, reproducible tooling, and local dependencies.
2. API configuration, health, readiness, logging, and correlation IDs.
3. Relational schema and migrations.
4. Identity, tenancy, groups, roles, and deny-by-default ACLs.
5. Object storage, document catalog, versions, and upload.
6. Parsing, OCR, tables, normalization, deduplication, and provenance.
7. Chunk strategies and chunking experiments.
8. Embedding interface and dense index.
9. PostgreSQL lexical index, hybrid fusion, and retrieval comparison.
10. Permission-filtered retrieval.
11. Cross-encoder reranking and context/evidence assembly.
12. Provider-neutral grounded generation, citations, and abstention.
13. Async indexing, updates, deletion, retry, DLQ, and reconciliation.
14. Search/answer APIs and conversation boundaries.
15. Agent-free employee UI, owner operations UI, and feedback.
16. Separate ingestion, retrieval, reranking, answer, citation, and safety evals.
17. Security hardening against injection, poisoning, leakage, and abuse.
18. Reliability, caching, observability, cost, and SLOs.
19. Optional secure read-only MCP search.
20. CI/CD gates.
21. Production-like deployment, rollback, backup, restore, and disaster recovery.
22. Limited pilot and feedback-to-eval improvement loop.

Each stage should be a small pull request whose tests and evidence stand alone.

## 4. Beginner milestones

| Milestone | Working output | Main concept | Requirement proof |
|---|---|---|---|
| M0 | Reproducible repo and test command | packaging, lint, types, tests | engineering baseline |
| M1 | Health/readiness API and local dependencies | services and configuration | operational baseline |
| M2 | Tenant/user/group/document schema | relational design and migrations | RAG-AUTH-01 |
| M3 | Authorized document upload to MinIO | object storage and trust boundaries | RAG-ING-01 |
| M4 | Parsed, versioned document with provenance | parsing, OCR, tables | RAG-ING-01 |
| M5 | Chunk experiment report | chunk quality and identifiers | RAG-ING-01 |
| M6 | Dense search | embeddings and pgvector | RAG-RET-01 |
| M7 | Lexical, dense, and hybrid comparison | FTS and RRF | RAG-RET-01 |
| M8 | ACL-filtered retrieval | pre-retrieval permission enforcement | RAG-AUTH-01/02 |
| M9 | Reranked evidence packet | reranking and context budgets | RAG-RET-01 |
| M10 | Cited, abstaining answer | grounded generation | RAG-CIT-01, RAG-ABS-01 |
| M11 | Idempotent async update/delete | queues, lifecycle, reconciliation | RAG-ING-02 |
| M12 | Search and answer UI with feedback | product workflow | product evidence |
| M13 | Layered eval reports and BEIR adapter | failure attribution | RAG-EVAL-01 |
| M14 | Security suite | injection, poisoning, leakage | RAG-SEC-01 |
| M15 | Traces, dashboards, cost, cache, DLQ | production operations | RAG-OPS-01 |
| M16 | Optional read-only MCP search | controlled integration | RAG-AUTH-02 |
| M17 | CI, deployment, rollback, restore | release engineering | operational evidence |
| M18 | Pilot report and improvement loop | product decision making | final proof |

If you are new, complete M0-M10 before adding conversational history, MCP, or deployment.

## 5. Target repository and artifact manifest

Create this repository:

```text
enterprise-rag-knowledge-assistant/
  README.md
  pyproject.toml
  uv.lock
  alembic.ini
  .env.example
  .gitignore
  .dockerignore
  docker-compose.yml
  Dockerfile.api
  Dockerfile.worker
  Dockerfile.mcp
  Dockerfile.web
  .github/
    workflows/
      ci.yml
      release.yml
  apps/
    api/
      enterprise_rag_api/
        __init__.py
        main.py
        settings.py
        dependencies.py
        middleware.py
        errors.py
        readiness.py
        auth/
          oidc.py
          local.py
        routes/
          health.py
          sources.py
          documents.py
          jobs.py
          search.py
          answers.py
          feedback.py
          metrics.py
          compliance.py
          admin.py
        schemas/
          common.py
          sources.py
          documents.py
          search.py
          answers.py
          feedback.py
          compliance.py
          admin.py
    worker/
      enterprise_rag_worker/
        __init__.py
        main.py
        queues.py
        processes/
          ingest.py
          delete.py
          evaluate.py
          maintenance.py
        jobs/
          ingest.py
          delete.py
          reconcile.py
          evaluate.py
    mcp/
      enterprise_rag_mcp/
        __init__.py
        server.py
        auth.py
        tools.py
    web/
      package.json
      package-lock.json
      vite.config.ts
      src/
        api/
        components/
        pages/
          EmployeeSearchPage.tsx
          KnowledgeOwnerPage.tsx
          OperatorConsolePage.tsx
          ComplianceEvidencePage.tsx
        types/
  packages/
    domain/
      enterprise_rag_domain/
        __init__.py
        enums.py
        errors.py
        identity.py
        documents.py
        retrieval.py
        evidence.py
        services/
          authorization.py
          document_lifecycle.py
          answer_policy.py
    db/
      enterprise_rag_db/
        __init__.py
        base.py
        session.py
        models.py
        repositories/
          identities.py
          documents.py
          chunks.py
          jobs.py
          queries.py
          publications.py
          evidence_bundles.py
        migrations/
          env.py
          versions/
    object_store/
      enterprise_rag_object_store/
        __init__.py
        base.py
        s3.py
        keys.py
    ingestion/
      enterprise_rag_ingestion/
        __init__.py
        contracts.py
        normalize.py
        deduplicate.py
        provenance.py
        parsers/
          base.py
          pdf.py
          html.py
          email.py
          docx.py
          spreadsheet.py
          text.py
          ocr.py
        connectors/
          base.py
          s3_prefix.py
        malware/
          base.py
          clamav.py
        chunkers/
          base.py
          fixed.py
          structure_aware.py
          table_aware.py
    embeddings/
      enterprise_rag_embeddings/
        __init__.py
        base.py
        sentence_transformers.py
        registry.py
    retrieval/
      enterprise_rag_retrieval/
        __init__.py
        contracts.py
        filters.py
        lexical.py
        dense.py
        fusion.py
        rerank.py
        context.py
        service.py
        adapters/
          postgres.py
          opensearch.py
    generation/
      enterprise_rag_generation/
        __init__.py
        contracts.py
        gateway.py
        providers/
          mock.py
          hosted_http.py
        prompts/
          grounded_answer.v1.md
          query_rewrite.v1.md
        citations.py
        abstention.py
    evals/
      enterprise_rag_evals/
        __init__.py
        contracts.py
        runner.py
        reports.py
        scoring/
          ingestion.py
          retrieval.py
          answers.py
          citations.py
          safety.py
        adapters/
          beir.py
          bm25_eval.py
        datasets/
          business_queries.jsonl
          unanswerable_queries.jsonl
          acl_cases.jsonl
          injection_cases.jsonl
          poisoning_cases.jsonl
          fixtures/
    observability/
      enterprise_rag_observability/
        __init__.py
        logging.py
        metrics.py
        tracing.py
        cost.py
    reliability/
      enterprise_rag_reliability/
        __init__.py
        cache.py
        retries.py
        idempotency.py
        dlq.py
        reconciliation.py
  infra/
    prometheus/
      prometheus.yml
    grafana/
      provisioning/
      dashboards/
    minio/
      policies/
    staging/
      docker-compose.staging.yml
      env.example
    terraform/
      aws/
        versions.tf
        providers.tf
        variables.tf
        main.tf
        outputs.tf
        modules/
          network/
          ecr/
          s3/
          rds_pgvector/
          elasticache/
          ecs_services/
          alb_tls/
          secrets/
          observability/
          backup/
  configs/
    chunking.yaml
    retrieval.yaml
    eval-gates.yaml
    pricing.yaml
    pilot.yaml
  scripts/
    seed_demo.py
    smoke.ps1
    load_smoke.py
    backup.ps1
    restore-drill.ps1
    deployment-smoke.ps1
  tests/
    api/
    db/
    domain/
    ingestion/
    embeddings/
    retrieval/
    generation/
    evals/
    security/
    reliability/
    observability/
    mcp/
    ci/
    e2e/
      operator-compliance.spec.ts
  docs/
    README.md
    product-requirements.md
    workflow-map.md
    metric-tree.md
    risk-register.md
    pilot-plan.md
    architecture.md
    data-flow-and-trust-boundaries.md
    api-contracts.md
    compliance-evidence-bundle-contract.md
    data-contracts.md
    data-model.md
    ingestion-contract.md
    retrieval-contract.md
    acl-model.md
    source-register.md
    system-card.md
    dataset-card.md
    benchmark-card.md
    vendor-assessment.md
    retention-policy.md
    provider-data-disclosure.md
    threat-model.md
    feedback-to-eval-loop.md
    learning-notes.md
    progress-log.md
    adr/
      0001-system-boundaries.md
      0002-retrieval-backends.md
      ...
    reports/
      business-baseline-report.md
      ingestion-report.md
      retrieval-benchmark-report.md
      generation-citation-report.md
      permission-eval-report.md
      security-red-team-report.md
      eval-report.md
      freshness-delete-report.md
      chunking-experiment.md
      beir-benchmark-report.md
      cost-performance-report.md
      load-failure-report.md
      capacity-report.md
      release-report.md
      pilot-report.md
    runbooks/
      observability-slo.md
      incident-response.md
      permission-revocation.md
      delete-propagation.md
      source-quarantine.md
      provider-outage.md
      rollback.md
      reindex.md
      backup-restore.md
    stages/
      stage-01-repository-platform.md
      stage-02-api-foundation.md
      ...
      stage-22-pilot-improvement.md
```

The `docs/` directory is implementation evidence, not decoration. Adapt the completed SupportOps
pattern: each stage record includes goal, guide mapping, files changed, runtime flow, failure
behavior, tests, verification commands, verified facts, unverified facts, and the next stage.

The artifact manifest is:

| Artifact | Owner stage | Required contents |
|---|---:|---|
| Product requirements | Pre-build | users, workflow, baseline, metrics, non-goals, risks |
| Architecture and decisions | 1 onward | boundaries, diagrams, ADRs, versioned decisions |
| API/data/ingestion/retrieval/ACL contracts | 2-10 | schemas, errors, state rules, trust boundaries |
| Chunking experiment | 7 | corpus, strategies, metrics, choice, failures |
| Layered eval reports | 16 | ingestion, retrieval, answers/citations, safety |
| BEIR report | 16 | adapter, dataset, reproducibility, business-transfer caveat |
| Threat/system/dataset cards | 17 | data, model, retrieval, user, vendor, residual risks |
| Cost/SLO/incident reports | 18 | measurements, budgets, alerts, response |
| Rollback and restore runbooks | 21 | exact commands, decisions, evidence from drill |
| Pilot and feedback loop | 22 | scope, metrics, failures, decision, next release |
| Learning notes and progress log | every stage | what was learned, what failed, verified evidence |

## Part 1 - Repository and local platform

### Stage 1.1 - Reproducible repository and dependencies

**Objective**

Create a fresh-clone repository with pinned dependencies, deterministic quality commands, and
local PostgreSQL/pgvector, Redis, and MinIO.

**Prerequisites**

- Local tools from Section 0.
- No model-provider key is required.

**Technology**

- Python 3.12, `uv`, Docker Compose, PostgreSQL 16 with pgvector, Redis, and MinIO.

**Files**

- `pyproject.toml`, `uv.lock`, `.env.example`, `.gitignore`, `.dockerignore`.
- `docker-compose.yml`, `Dockerfile.api`, `Dockerfile.worker`.
- Package `__init__.py` files and initial `tests/test_repository.py`.
- `docs/architecture.md`, `docs/learning-notes.md`, `docs/progress-log.md`.
- `docs/stages/stage-01-repository-platform.md`.

**Contracts**

- Python packages import without application side effects.
- Secrets are absent from source and `.env.example`.
- Service names are stable: `postgres`, `redis`, `minio`, `clamav`, `api`, `worker-ingest`,
  `worker-delete`, `worker-eval`, `worker-maintenance`, `web`, and optional `mcp`.
- PostgreSQL has the `vector` extension.

**Implementation steps**

1. Initialize the repository and configure `[tool.uv.workspace]` members/build metadata for each
   app/package shown above; do not depend on an ad hoc `PYTHONPATH`.
2. Add runtime dependencies for FastAPI, Pydantic settings, SQLAlchemy, psycopg, Alembic,
   pgvector, Redis, RQ, boto3, parsers, sentence-transformers, HTTP, and telemetry.
3. Add pytest, coverage, Ruff, mypy, testcontainers, and property-based test dependencies.
4. Configure Ruff and mypy strictly for production packages; document temporary exclusions.
5. Add Compose health checks for Postgres, Redis, and MinIO.
6. Initialize the `vector` extension during database startup.
7. Pin container tags and Python dependencies; record why any floating development tag remains.
8. Add a no-secret scan to the local quality command.

Minimum `.env.example` names:

```env
APP_ENV=local
APP_NAME=enterprise-rag-knowledge-assistant
AUTH_MODE=oidc
OIDC_ISSUER_URL=
OIDC_AUDIENCE=enterprise-rag-api
OIDC_DISCOVERY_URL=
OIDC_ALLOWED_ALGORITHMS=RS256,ES256
OIDC_TENANT_CLAIM=tenant_id
OIDC_GROUPS_CLAIM=groups
OIDC_JWKS_CACHE_TTL_SECONDS=300
INSECURE_LOCAL_AUTH_ENABLED=false
DATABASE_URL=postgresql+psycopg://rag:rag@localhost:5432/rag
REDIS_URL=redis://localhost:6379/0
S3_ENDPOINT_URL=http://localhost:9000
S3_REGION=us-east-1
S3_SOURCE_BUCKET=enterprise-rag-sources
S3_DERIVED_BUCKET=enterprise-rag-derived
S3_ACCESS_KEY_ID=
S3_SECRET_ACCESS_KEY=
MALWARE_SCANNER=clamav
CLAMAV_HOST=localhost
CLAMAV_PORT=3310
MALWARE_SCAN_REQUIRED=true
INSECURE_MALWARE_SCAN_BYPASS=false
SUPPORTED_LANGUAGES=en
LANGUAGE_MIN_CONFIDENCE=0.85
EMBEDDING_MODEL_ID=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_MODEL_REVISION=
EMBEDDING_MODEL_MANIFEST_SHA256=
EMBEDDING_DIMENSION=384
RERANKER_MODEL_ID=cross-encoder/ms-marco-MiniLM-L-6-v2
RERANKER_MODEL_REVISION=
RERANKER_MODEL_MANIFEST_SHA256=
GENERATION_PROVIDER=mock
GENERATION_BASE_URL=
GENERATION_MODEL=
GENERATION_API_KEY=
MCP_ENABLED=false
MCP_TRANSPORT=streamable-http
MCP_BIND_HOST=127.0.0.1
MCP_PORT=8100
MCP_OIDC_ISSUER_URL=
MCP_OIDC_AUDIENCE=enterprise-rag-mcp
MCP_REQUIRED_SCOPE=knowledge.search
MCP_ALLOWED_CLIENT_IDS=
MCP_MAX_RESULTS=10
MCP_MAX_RESPONSE_BYTES=65536
MCP_REQUEST_TIMEOUT_SECONDS=5
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
LOG_LEVEL=INFO
```

**Commands**

```powershell
mkdir enterprise-rag-knowledge-assistant
cd enterprise-rag-knowledge-assistant
git init
uv init --package
uv add fastapi uvicorn pydantic pydantic-settings python-multipart sqlalchemy "psycopg[binary]" alembic pgvector
uv add "PyJWT[crypto]" redis rq boto3 httpx pymupdf beautifulsoup4 python-docx openpyxl pillow pytesseract clamd
uv add sentence-transformers rank-bm25 lingua-language-detector python-json-logger prometheus-client opentelemetry-api
uv add opentelemetry-sdk opentelemetry-exporter-otlp opentelemetry-instrumentation-fastapi
uv add --optional mcp mcp
uv add --dev pytest pytest-asyncio pytest-cov testcontainers ruff mypy hypothesis
docker compose up -d postgres redis minio clamav
docker compose ps
uv run ruff check .
uv run mypy apps packages
uv run pytest
```

**Tests**

- Dependency lock exists and a clean environment can install it.
- Every Python package imports.
- PostgreSQL accepts a query and reports the `vector` extension.
- Redis responds to `PING`.
- MinIO bucket creation and a put/get/delete round trip work.
- `.env.example` contains no secret value.

**Observability**

- Compose health status exposes dependency readiness.
- Startup logs include app version and configuration profile, never secrets.

**Evidence**

- Record exact tool/container versions and command output in the stage record.
- Add the initial architecture, learning note, and progress-log entry.

**Done when**

- A fresh clone can run `uv sync`, all three dependencies become healthy, and lint/type/test pass.
- No application code depends on an unpinned provider SDK.

## Part 2 - API foundation

### Stage 2.1 - Configuration, errors, health, and readiness

**Objective**

Build a typed API shell with centralized configuration, correlation IDs, controlled errors, and
dependency-aware readiness.

**Prerequisites**

- Stage 1 `Done when` criteria are locally verified.

**Technology**

- FastAPI, Pydantic Settings, SQLAlchemy, Redis, boto3, and structured JSON logging.

**Files**

- `apps/api/enterprise_rag_api/{main,settings,dependencies,middleware,errors}.py`.
- `apps/api/enterprise_rag_api/readiness.py`.
- `apps/api/enterprise_rag_api/routes/health.py`.
- `apps/api/enterprise_rag_api/schemas/common.py`.
- `tests/api/test_health.py`, `tests/api/test_readiness_capabilities.py`.
- `docs/api-contracts.md`, `docs/stages/stage-02-api-foundation.md`.

**Contracts**

- `GET /health` proves only the API process is alive.
- `GET /ready` reports `search`, `ingest`, `delete`, `answer`, `eval`, and optional `mcp`
  capability states plus dependency states. `GET /ready?capability=<name>` applies the requested
  capability's contract.
- Search hard dependencies are database/schema, authorization configuration, a validated compatible
  current index, and the verified query-embedding artifact. Redis cache and reranker are soft
  dependencies with documented fallbacks.
- Ingest hard dependencies are database, Redis/RQ, source and derived object buckets, ClamAV,
  verified embedding artifact, and a fresh `worker-ingest` heartbeat. OCR/Tesseract is hard only
  when an enabled source claims OCR.
- Delete hard dependencies are database, Redis/RQ, object storage, and a fresh isolated
  `worker-delete` heartbeat. Evaluation requires its pinned datasets/index and `worker-eval`.
- Answer requires search. A failed optional generation provider produces `degraded` search-only
  behavior, never a fabricated answer. MCP is `disabled` when not configured and is not an overall
  failure; when enabled, its package, OIDC config, transport, limits, and search capability are hard.
- Aggregate readiness returns `503` only when the core search capability is `not_ready`; a requested
  hard capability returns `503` when that capability is unavailable. Soft loss returns `200` with
  `degraded` and machine-readable reasons.
- Every response has `X-Request-Id`; every error uses `{code, message, request_id, details}`.
- Configuration validates URLs, bucket names, model IDs, dimensions, timeouts, and feature flags.

**Implementation steps**

1. Create one cached settings object loaded only from environment.
2. Add request-ID middleware that accepts only syntactically safe IDs or creates a UUID.
3. Add exception classes and handlers without internal stack traces in responses.
4. Implement time-bounded checks independently and classify each result as `hard`, `soft`, or
   `disabled` for each capability.
5. Verify that the current index is published, validation-approved, schema-compatible, ACL-complete,
   and built with the configured embedding dimension/revision/digest.
6. Track worker heartbeats by isolated pool and reject stale heartbeats after the configured window.
7. Return `200`/`503` with aggregate status, capability map, dependency map, current-index version,
   checked-at time, and safe reason codes.
8. Add startup checks that embedding/reranker revisions and artifact-manifest digests are present
   and that embedding dimension matches the current index/database.
9. Document response schemas, hard/soft matrices, and status codes.

**Commands**

```powershell
uv run uvicorn enterprise_rag_api.main:app --reload --app-dir apps/api
uv run pytest tests/api/test_health.py tests/api/test_readiness_capabilities.py
```

**Tests**

- Health returns `200` without touching dependencies.
- Search returns `503` without a validated compatible current index even when dependencies answer.
- Every hard dependency fails only its declared capabilities; every soft dependency produces the
  declared degraded state.
- Stale ingest/delete/eval worker heartbeats are distinguished and the delete pool cannot be
  represented by an ingest heartbeat.
- Disabled MCP is healthy for aggregate readiness; enabled-but-misconfigured/uninstalled MCP is
  `not_ready`.
- Generation failure leaves search ready and answer degraded.
- Each dependency failure returns controlled details without secrets, object keys, or provider
  payloads.
- Request IDs propagate into success responses, errors, and logs.
- Secret values are redacted from validation errors and logs.

**Observability**

- Emit readiness duration and dependency state.
- Log startup configuration as a safe allowlist.

**Evidence**

- Add API examples and error schema to `docs/api-contracts.md`.
- Record ready, degraded, no-current-index, stale-worker, and intentionally not-ready verifications.

**Done when**

- API startup, liveness, capability readiness, current-index, hard/soft dependency, error,
  request-ID, and redaction tests pass.

## Part 3 - Relational schema and migrations

### Stage 3.1 - Core data model, vector extension, and lifecycle constraints

**Objective**

Create the relational source of truth for identity, documents, versions, chunks, indexing,
queries, answers, feedback, evaluations, cost, and audit.

**Prerequisites**

- Stages 1-2 `Done when` criteria are locally verified.

**Technology**

- SQLAlchemy 2, Alembic, PostgreSQL 16, pgvector, generated `tsvector`, GIN, and HNSW.

**Files**

- `packages/db/enterprise_rag_db/{base,session,models}.py`.
- Repository modules and Alembic configuration/migrations.
- `tests/db/test_models.py`, `tests/db/test_migrations.py`.
- `docs/data-model.md`, `docs/adr/0003-data-model-and-index-foundation.md`.
- `docs/stages/stage-03-data-model.md`.

**Contracts**

Minimum tables:

| Table | Essential responsibility |
|---|---|
| `tenants` | hard business-data boundary |
| `subjects` | stable tenant reference to a user or service identity and its lifecycle state |
| `groups`, `subject_group_revisions` | identity-provider groups plus versioned membership snapshots used for replay |
| `roles`, `subject_roles` | product administration privileges assigned to subjects |
| `sources` | approved owner, classification, connector, ACL, refresh, and retention policy |
| `source_checkpoints` | connector cursor, upstream revision, counts, status, and idempotency |
| `documents` | stable logical document |
| `document_versions` | immutable content identity, source revision, hashes, and provenance |
| `document_version_state_events` | append-only lifecycle transitions and actor/reason |
| `document_version_state_projection` | rebuildable current-state/version projection |
| `acl_revisions`, `acl_entries` | immutable permission snapshots with allow/deny entries for subject, group, role, attribute policy, or tenant-public scope |
| `raw_objects` | immutable logical raw-artifact identity and quarantine policy |
| `artifact_object_versions` | every raw/derived S3 bucket, key, version ID, hash, size, retention lock |
| `object_deletion_evidence` | per-object-version attempt, result, exception, verifier, and timestamp |
| `parse_runs` | parser/OCR versions, status, warnings, metrics |
| `chunks` | stable chunk identity, exact text, offsets, provenance, FTS vector |
| `chunk_embeddings` | chunk/model/vector tuple |
| `index_versions` | candidate/published configuration, corpus snapshot, status, counts, and compatibility |
| `index_publication_approvals` | immutable candidate approval, evidence hash, approver, and decision |
| `ingestion_runs`, `ingestion_events` | idempotency key, attempts, durable state transitions, heartbeat, error, and publication outcome |
| `query_requests`, `retrieval_runs` | trusted identity-scope hash, query/config versions, backend activity, and latency |
| `retrieval_candidates` | rank/score by retriever and fused result |
| `evidence_packets` | bounded authorized context and exact version/hash references |
| `generation_runs`, `answers` | prompt/model/context/cost/validation plus immutable answer or abstention outcome |
| `citations` | answer claim, chunk, document version, span |
| `feedback` | rating, issue category, corrected citation, comment |
| `content_issues` | owner-routed source gap, staleness, conflict, parse, or citation issue |
| `eval_datasets`, `eval_cases`, `eval_runs`, `eval_results` | versioned evaluation lineage |
| `cost_events` | feature/model/tenant usage and configured price |
| `audit_logs` | security-sensitive and administrative actions |
| `evidence_bundles`, `evidence_bundle_items` | scoped compliance export manifest and immutable evidence references |
| `outbox_events` | transactionally published lifecycle work |

Required constraints:

- Every tenant-owned row has non-null `tenant_id`.
- Every identity-bearing reference uses `subject_id` and a controlled `subject_type`; service
  identities are not represented as fake users.
- Document-version payload fields are immutable as soon as intake is accepted: tenant/document/
  source identity, version number, upstream revision, source object/version/hash, media type,
  owner, parser-policy input, and created time cannot be updated. Processing state is not one of
  those fields; workers append guarded `document_version_state_events` and update only the
  rebuildable state projection.
- Unique `(tenant_id, document_id, version_number)`.
- Unique source checksum per document version.
- Unique `(chunk_id, embedding_model_id, embedding_model_revision)`.
- ACL subject type and subject ID form a validated pair; `allow`/`deny` effect, normalized
  attribute-policy reference, policy version, source ACL revision, effective time, and expiry are
  explicit. Deny precedence is enforced by the canonical authorization predicate.
- Source checkpoint/run identity is unique by source, upstream revision/checkpoint, operation, and pipeline
  policy.
- The mutable active-version pointer lives on `documents` (or an equivalent publication route),
  not on `document_versions`, and points only to a validated, approved, promoted index generation.
- Citations reference a chunk and its exact document version.
- Evidence packets reference one authorization-scope hash and contain only chunks that passed that
  scope's predicate.
- Lifecycle states are controlled enums with guarded transitions.

**Implementation steps**

1. Model UUID primary keys, timezone-aware timestamps, and explicit foreign-key deletion rules.
2. Create the `vector` extension in a migration.
3. Store the configured 384-dimension vector and add an HNSW cosine index.
4. Generate a weighted English `tsvector` from title, heading path, body, and table text; add GIN.
5. Add indexes beginning with `tenant_id` for tenant-scoped access paths.
6. Add optimistic version columns to mutable lifecycle records.
7. Reject SQLAlchemy dirty updates to immutable version payload columns; express lifecycle changes
   as append-only state events and test projection rebuild.
8. Make audit, publication-approval, and state-event records append-only at the repository layer.
9. Write a downgrade decision for every migration; do not automatically downgrade destructive
   data migrations.
10. Draw relationships, immutable/mutable field ownership, and state transitions in
    `docs/data-model.md`.

**Commands**

```powershell
uv run alembic revision --autogenerate -m "create enterprise rag core schema"
uv run alembic upgrade head
uv run pytest tests/db
```

**Tests**

- Migrations apply to an empty database and upgrade from the previous revision.
- Required constraints reject cross-tenant and version-mismatched relationships.
- Vector insert/query and FTS query work.
- Active version cannot point to a failed or deleted index version.
- Attempts to mutate any frozen document-version payload field fail; valid state transitions append
  events and rebuild to the same current-state projection.
- Destructive cascades follow the documented retention contract.
- Repository queries require tenant scope.

**Observability**

- Record migration version, duration, row counts, and lock time.
- Slow-query logs redact query text and document content.

**Evidence**

- Commit an ER diagram, table dictionary, indexes, retention behavior, and migration verification.

**Done when**

- A fresh database is reproducible, all constraints and indexes are tested, and no tenant-owned
  repository method can run without an explicit tenant scope.

## Part 4 - Identity, tenancy, roles, and ACLs

### Stage 4.1 - Deny-by-default authorization service

**Objective**

Implement `RAG-AUTH-01` and the foundation of `RAG-AUTH-02`: trusted identity context and
deny-by-default document authorization that retrieval can apply inside candidate queries.

**Prerequisites**

- Stage 3 schema and repository `Done when` criteria are locally verified.

**Technology**

- `PyJWT[crypto]`, OIDC discovery/JWKS over bounded `httpx`, FastAPI dependencies, the domain
  authorization service, PostgreSQL ACL predicates, and an explicitly insecure local adapter.

**Files**

- `packages/domain/enterprise_rag_domain/{identity,enums}.py`.
- `packages/domain/enterprise_rag_domain/services/authorization.py`.
- `packages/db/enterprise_rag_db/repositories/identities.py`.
- `apps/api/enterprise_rag_api/auth/{oidc,local}.py`, API identity dependency, and admin routes.
- `tests/api/test_oidc_auth.py`, `tests/api/test_local_auth_gate.py`.
- `tests/domain/test_authorization.py`, `tests/security/test_tenant_acl.py`.
- `docs/acl-model.md`, `docs/stages/stage-04-identity-acl.md`.

**Contracts**

`IdentityContext` contains:

```python
@dataclass(frozen=True)
class IdentityContext:
    tenant_id: UUID
    subject_id: UUID
    subject_type: Literal["user", "service"]
    group_ids: frozenset[UUID]
    role_names: frozenset[str]
    policy_attributes: Mapping[str, str]
    auth_time: datetime
    identity_version: str
    group_membership_revision: str
    authorization_policy_version: str
```

- `AUTH_MODE=oidc` is the default. The adapter loads the configured discovery document, requires
  exact `iss`, expected `aud`, `exp`, `iat`, `sub`, `kid`, and an algorithm in the configured
  `RS256,ES256` allowlist, then verifies the signature against cached JWKS. It rejects `none`,
  symmetric downgrade, missing claims, unknown keys, stale discovery, and ambiguous tenant maps.
- `OIDC_DISCOVERY_URL` must be HTTPS outside local mode and its returned `issuer` must exactly match
  `OIDC_ISSUER_URL`. Discovery/JWKS calls use five-second timeouts, response-size limits, TLS
  validation, and the configured cache TTL. Key rotation refreshes once on an unknown `kid`; a
  second miss denies.
- `sub` maps to a tenant-scoped `subject_id`; the tenant claim maps through a server-owned issuer/
  external-tenant table. Signed group claims are accepted only when the configured claim and
  freshness policy allow them; otherwise groups load server-side.
- `policy_attributes` contains only allowlisted, normalized, integrity-protected values evaluated by
  deterministic policy code; raw client attributes never become authorization facts.
- The local adapter requires all three conditions: `APP_ENV=local`, `AUTH_MODE=local`, and
  `INSECURE_LOCAL_AUTH_ENABLED=true`. It accepts only `X-Dev-Subject-Id` and
  `X-Dev-Tenant-Id`, then loads roles/groups server-side. Startup fails if this switch is true in
  staging/production or if arbitrary role/group headers are configured.
- Document access is allowed only by an active same-tenant allow entry matching the user, one of
  the trusted groups, an authorized role/attribute, or `tenant_public`, with no applicable active
  deny. Explicit deny overrides allow for sources whose canonical policy requires deny entries.
- Group nesting is resolved from the authoritative identity graph with cycle/depth limits; stale or
  incomplete group state fails closed.
- Product roles authorize operations; document ACLs authorize content. Admin role alone does not
  silently grant document content access unless policy explicitly says so.
- Disabled user/service subjects, deleted groups, expired ACLs, wrong tenants, and unknown subjects
  deny access.

**Implementation steps**

1. Implement the OIDC discovery/JWKS adapter with strict config validation, cache, rotation refresh,
   and controlled `401` errors that reveal no claim or key detail.
2. Implement the triple-gated local adapter and a startup assertion that makes accidental insecure
   deployment impossible.
3. Validate issuer, audience, signature, algorithm, required times, tenant/subject mapping, and
   subject state; load groups server-side or from signed, freshness-bounded claims.
4. Build one authorization predicate function, including effect precedence, effective/expiry
   time, source ACL revision, and policy version, used by lexical, dense, citation, export, cache,
   administration, and MCP paths.
5. Add ACL grant/revoke endpoints for knowledge owners with audit records.
6. Increment `identity_version`/`acl_version` on relevant changes for cache invalidation.
7. Reject any route that accepts client-selected `tenant_id`, `role`, or `group_ids` as authority.
8. Add a test matrix across two tenants, user/service subjects, groups, roles, document states, and
   ACL expiry.

**Commands**

```powershell
uv run pytest tests/api/test_oidc_auth.py tests/api/test_local_auth_gate.py
uv run pytest tests/domain/test_authorization.py tests/security/test_tenant_acl.py
```

**Tests**

- Missing, expired, wrong-audience, and disabled identity fails.
- Wrong issuer/algorithm/signature, missing `kid`, unknown key after one refresh, stale discovery,
  invalid tenant mapping, and unreachable JWKS all deny.
- JWKS cache and one-time key-rotation refresh are deterministic and bounded.
- Every partial local-switch combination fails; staging/production refuses to start with insecure
  local authentication enabled.
- Cross-tenant access always fails, including guessed UUIDs.
- User/group/role/public allow, explicit-deny precedence, nested-group, effective, and expiry ACLs
  produce only their documented cases.
- Revocation denies the next query even if an old result was cached.
- Admin operations and document-reading permission remain distinct.
- Property-based combinations never produce an allow without a same-tenant active match.

**Observability**

- Count allow/deny decisions by reason without logging document text or group lists.
- Audit grants, revocations, role changes, identity failures, and break-glass use.

**Evidence**

- `docs/acl-model.md` includes truth table, trust boundaries, cache effects, and revocation flow.
- `docs/runbooks/permission-revocation.md` defines source event, cache/index checks, SLO measurement,
  escalation, and confirmed-absence evidence.
- Attach the complete cross-tenant/ACL test matrix to the stage record.

**Done when**

- `RAG-AUTH-01` is demonstrably deny-by-default and every downstream content path can consume the
  same trusted predicate.

## Part 5 - Upload, object storage, versions, and provenance

### Stage 5.1 - Authorized document intake and immutable source storage

**Objective**

Implement the source half of `RAG-ING-01`: register an approved source, run one bounded S3-prefix
connector or accept an authorized upload, store immutable bytes, create a document version,
preserve origin metadata, and enqueue processing transactionally.

**Prerequisites**

- Stages 1-4 `Done when` criteria are locally verified.
- The caller is a knowledge owner or ingestion service identity and can assign only ACLs they are
  authorized to manage.

**Technology**

- FastAPI streaming uploads, boto3 S3 interface, MinIO, ClamAV `INSTREAM` through `clamd`,
  PostgreSQL, SHA-256, and transactional outbox.

**Files**

- `packages/object_store/enterprise_rag_object_store/{base,s3,keys}.py`.
- `packages/ingestion/enterprise_rag_ingestion/connectors/{base,s3_prefix}.py`.
- `packages/ingestion/enterprise_rag_ingestion/malware/{base,clamav}.py`.
- `packages/domain/enterprise_rag_domain/documents.py`.
- `packages/domain/enterprise_rag_domain/services/document_lifecycle.py`.
- Source/document schemas/routes and source/document repositories.
- `tests/api/test_sources.py`, `test_document_upload.py`,
  `tests/ingestion/test_source_storage.py`, `test_s3_prefix_connector.py`.
- `tests/ingestion/test_ooxml_validation.py`, `test_clamav_scanner.py`.
- `docs/ingestion-contract.md`, `docs/source-register.md`.
- `docs/stages/stage-05-upload-provenance.md`.

**Contracts**

- `POST /v1/sources` registers owner, classification, connector type/config reference, source ACL
  revision, refresh policy, retention, and enabled/quarantine state.
- `POST /v1/sources/{source_id}/syncs` starts an idempotent bounded connector sync.
- `POST /v1/documents:ingest` creates the logical document and version 1 from a streamed file or
  approved manifest.
- `POST /v1/documents/{document_id}:reprocess` creates a candidate version under an approved new
  pipeline configuration; content updates use another ingest event with a new upstream revision.
- `GET /v1/sources/{source_id}` and `GET /v1/documents/{document_id}` return only authorized
  catalog metadata.
- The default connector lists objects only under one preconfigured allowlisted S3/MinIO
  bucket/prefix using a least-privilege credential reference. It cannot accept arbitrary endpoints,
  buckets, URLs, redirects, or credentials from a sync request.
- Object keys are server-generated:
  `tenant/{tenant_id}/document/{document_id}/version/{version_id}/source/{sha256}`.
- The database stores object version ID, ETag, SHA-256, media type, byte count, original filename,
  source system, source URI, source timestamp, uploader, and ingestion policy.
- Accepted formats and size/page limits are allowlisted. The starter limit is 50 MiB per object.
- Generic archives (`.zip`, `.tar`, `.tar.gz`, `.7z`, `.rar`) are not documents and are rejected.
  DOCX/XLSX are ZIP-based OOXML packages, so they are accepted only after validating the ZIP
  signature, `[Content_Types].xml`, expected Office relationships/parts, allowlisted part names,
  uncompressed byte/part-count/compression-ratio limits, and path safety. Macro-enabled
  `.docm`/`.xlsm`, embedded packages, traversal names, encrypted parts, and external relationships
  are rejected in v1; no relationship may trigger a network fetch.
- `MALWARE_SCAN_REQUIRED=true` outside tests. `ClamAvScanner` streams bounded bytes to the configured
  daemon, records engine/signature-database version and result, and returns only `clean`,
  `infected`, or `unavailable`. Infected, timeout, protocol-error, or unavailable results enter
  quarantine and cannot create a processable document version/outbox event.
- `INSECURE_MALWARE_SCAN_BYPASS=true` is permitted only with `APP_ENV=local`; any staging/
  production startup with the bypass fails.
- Every raw or derived object write records bucket, key, returned S3 `VersionId`, ETag, hash, size,
  artifact class, retention/legal-hold metadata, and owning document version. An ETag is not a
  substitute for a version ID or content hash.
- A completed response means bytes and metadata are durable and a job is scheduled, not indexed.
- An `Idempotency-Key` plus tenant and content hash returns the original intake result.

**Implementation steps**

1. Implement source registration and approval/quarantine state; store only a secret reference, not
   connector credentials.
2. Implement the S3-prefix connector with checkpointed listing, upstream version IDs/ETags,
   destination allowlist, bounded objects/bytes/time, and least-privilege read identity.
3. Stream the request or connector object to a bounded temporary file while calculating SHA-256;
   never buffer an unbounded upload in memory.
4. Validate extension, declared media type, detected signature, decompression limits, and file
   size. Reject generic archives; route claimed OOXML through the strict package validator.
5. Scan with `ClamAvScanner` before publishing to the clean source bucket. A deterministic fake is
   injectable only in tests. Quarantine every non-clean result with safe audit metadata.
6. Write clean content to a separate versioned, private artifact bucket with server-side
   encryption and persist the exact returned S3 version record transactionally/reconcilably.
7. Insert source sync/checkpoint, logical document, immutable version, source object, initial ACLs,
   ingestion job, and
   outbox event in a transaction. Compensate or reconcile an orphan object if the transaction fails.
8. Do not overwrite an object key. New content always creates a new version.
9. Record external connector cursor/version fields even when the first source is manual upload.
10. Add an operator-only endpoint to view sync/job state, never to download inaccessible content.

**Commands**

```powershell
uv run pytest tests/api/test_sources.py tests/api/test_document_upload.py
uv run pytest tests/ingestion/test_source_storage.py tests/ingestion/test_s3_prefix_connector.py
uv run pytest tests/ingestion/test_ooxml_validation.py tests/ingestion/test_clamav_scanner.py
uv run python scripts/seed_demo.py --documents
```

**Tests**

- Authorized upload creates exactly one source object, version, job, and outbox event.
- Approved connector sync is checkpointed and cannot leave its configured endpoint/bucket/prefix.
- Disabled/quarantined sources and unapproved owners cannot publish searchable work.
- Retried upload with the same idempotency key does not duplicate any of them.
- Duplicate and out-of-order connector revisions are idempotent and preserve the newest approved
  source state.
- Generic archives reject while valid bounded DOCX/XLSX pass; malformed OOXML, traversal,
  compression bomb, macro-enabled, embedded, encrypted, and external-relationship fixtures reject.
- The EICAR fixture quarantines, clean input passes, and ClamAV timeout/unavailable/protocol errors
  fail closed. The bypass cannot start outside local mode.
- Every successful object put persists its exact S3 version ID and hash; a missing version record
  prevents publication.
- Cross-tenant and unauthorized owner upload or read fail.
- Database failure after object write becomes a detectable orphan and reconciliation removes it.
- A new version never mutates or aliases the previous version's source object.

**Observability**

- Measure upload bytes, duration, validation/scanner results, storage errors, and orphan count.
- Measure source sync objects/bytes/checkpoint/lag, destination denials, and quarantine results.
- Audit uploader/connector identity, source/sync/document/version IDs, source hash, ACL assignment,
  and idempotency outcome.

**Evidence**

- `docs/ingestion-contract.md` records limits, state transitions, object-key rules, and failures.
- `docs/source-register.md` lists only approved/synthetic corpus origins and licenses.
- `docs/runbooks/source-quarantine.md` covers disablement, review, cleanup, re-enable approval, and
  one-source containment.
- The stage record includes a MinIO object-version screenshot or CLI listing with no sensitive data.

**Done when**

- Source registration and bounded sync are controlled, bytes are immutable and traceable, retries
  are idempotent, unauthorized intake fails, and every accepted object has a durable job or
  reconcilable outbox event.

## Part 6 - Parsing, OCR, tables, normalization, and deduplication

### Stage 6.1 - Versioned document parsing pipeline

**Objective**

Turn an immutable source object into a normalized document representation while retaining page,
heading, cell, character, parser, OCR, and source provenance.

**Prerequisites**

- Stage 5 intake and source-object round trips work.

**Technology**

- PyMuPDF, Beautiful Soup, python-docx, openpyxl, Pillow, Tesseract, language detection, and
  format-specific parser interfaces.

**Files**

- `packages/ingestion/enterprise_rag_ingestion/contracts.py`.
- Parser modules, `normalize.py`, `deduplicate.py`, and `provenance.py`.
- Parser fixtures under `tests/ingestion/fixtures/`.
- `tests/ingestion/test_parsers.py`, `test_ocr.py`, `test_tables.py`, `test_deduplication.py`.
- `docs/stages/stage-06-parsing.md`.

**Contracts**

All parsers return the same typed intermediate representation:

```python
class ParsedBlock(BaseModel):
    block_id: str
    kind: Literal["heading", "paragraph", "list", "table", "caption", "code"]
    text: str
    page_number: int | None
    heading_path: list[str]
    source_locator: dict[str, str | int]
    table: list[list[str]] | None
    language: str | None

class ParsedDocument(BaseModel):
    document_version_id: UUID
    parser_name: str
    parser_version: str
    ocr_engine_version: str | None
    detected_language: str | None
    language_confidence: float | None
    language_status: Literal["eligible", "needs_language_review"]
    blocks: list[ParsedBlock]
    warnings: list[str]
    content_hash: str
```

- PDF text extraction runs before OCR. OCR is used only when a page has too little usable text or
  the page is explicitly image-only.
- Table cells remain structured and also produce a deterministic row/column text rendering.
- EML parsing preserves message/attachment provenance, never fetches remote content, and processes
  allowlisted attachments only within configured count, depth, size, and decompression limits.
- Headers, footers, repeated boilerplate, control characters, and whitespace are normalized with a
  versioned policy. Original source bytes remain unchanged.
- Exact duplicates share a content fingerprint but retain source/version records.
- Near-duplicate detection initially reports candidates; it does not silently delete content.
- Password-protected, corrupted, unsupported, or low-confidence content enters `needs_review`.
- V1 is English-only: `SUPPORTED_LANGUAGES=en`, Tesseract uses the pinned `eng` data artifact, and
  the detector threshold starts at `0.85`. Confident English is `eligible`; confidently non-English,
  low-confidence, or materially mixed-language content becomes `needs_language_review` and cannot
  chunk, embed, publish, or reach generation. V1 does not translate content or silently force an
  English FTS/embedding route.

**Implementation steps**

1. Select a parser by detected media type, not filename alone.
2. Sandbox parsing in the worker container with CPU, memory, file, and wall-time limits.
3. Extract blocks in reading order and preserve page/section/cell locators.
4. Compute page-level text density; route only qualifying pages through OCR.
5. Record OCR language, confidence, engine version, language-data digest, and image coordinates.
6. Detect language over bounded representative blocks, record detector/version/confidence and
   material mixed-language signals, and apply the English-only eligibility gate before chunking.
7. Normalize deterministically and compute raw, normalized, and block hashes.
8. Flag suspicious hidden text, repeated instructions, macros, external links, and metadata as
   security signals without letting them change execution.
9. Save parser output as a versioned derived object and its summary in PostgreSQL.
10. Make parse output replaceable by `parser_version` while the source version stays immutable.

**Commands**

```powershell
uv run pytest tests/ingestion/test_parsers.py tests/ingestion/test_ocr.py
uv run pytest tests/ingestion/test_tables.py tests/ingestion/test_deduplication.py
```

**Tests**

- Golden fixtures cover text PDF, scanned PDF, mixed PDF, HTML, EML email with a safe attachment,
  DOCX, XLSX, TXT, and Markdown.
- Page, heading, character, and cell locators round-trip to the source fixture.
- OCR is skipped for high-text pages and invoked for image-only pages.
- A table preserves row/column meaning after normalization.
- Corrupted, encrypted, oversized-page, and parser-timeout cases fail safely into review.
- Same source/parser version is byte-for-byte deterministic.
- Exact duplicates are detected; near duplicates are reported but not auto-merged.
- English fixtures above threshold proceed. Spanish/French, unknown/low-confidence, and materially
  mixed fixtures remain non-searchable and create no chunks, embeddings, FTS rows, or answer
  context. Code/product identifiers inside an otherwise English document do not cause a false block.

**Observability**

- Emit pages/blocks/tables, OCR pages/confidence, detected-language/status (bounded labels), parse
  duration, warning class, and failure class.
- Trace object download, parser, OCR, normalization, and derived-object write separately.

**Evidence**

- Add a parser capability matrix, golden-fixture inventory, and known limitations to the ingestion
  contract and dataset card.
- Record at least one OCR and one table failure analysis in the stage document.

**Done when**

- Every supported English format produces deterministic typed blocks with verifiable provenance;
  non-English/uncertain language and every unsupported parse are explicitly non-searchable.

## Part 7 - Chunk identities and chunking experiments

### Stage 7.1 - Structure-aware default selected by evaluation

**Objective**

Implement multiple chunkers, give every chunk stable provenance, and choose the default from
measured retrieval results rather than intuition.

**Prerequisites**

- Stage 6 produces normalized blocks and locators.
- A starter labeled set has at least 30 representative questions and relevance judgments.

**Technology**

- Pure Python chunker interface, tokenizer-aware budgets, JSONL experiment datasets, and retrieval
  scoring utilities.

**Files**

- Chunker interface and fixed, structure-aware, and table-aware implementations.
- `packages/ingestion/enterprise_rag_ingestion/provenance.py`.
- `tests/ingestion/test_chunkers.py`.
- `packages/evals/enterprise_rag_evals/datasets/chunking_queries.jsonl`.
- `docs/reports/chunking-experiment.md`, `docs/stages/stage-07-chunking.md`.

**Contracts**

`ChunkRecord` includes:

- Stable `chunk_id` derived from tenant, document version, strategy version, locator, and text hash.
- `document_id`, `document_version_id`, `raw_object_id`, and `parent_chunk_id`.
- Exact text and normalized text hash.
- Page range, heading path, block IDs, character spans, and table cell ranges.
- Content kind, language, ACL snapshot/version, parser version, chunker name/version.
- Token count and neighboring chunk IDs.

Implement:

- Fixed-window baseline with overlap.
- Structure-aware heading/paragraph/list chunker.
- Table-aware chunks with title/header repetition and row grouping.
- Optional parent-child metadata, but no hidden parent content may bypass ACLs.

**Implementation steps**

1. Define fixed experiment splits and relevance judgments before comparing strategies.
2. Generate chunks for each strategy with the same parsed versions and embedding model.
3. Enforce a starter target of 200-450 tokens, 10-15% overlap only where structure requires it,
   and hard maximum below the configured context budget. Treat these as experiment parameters.
4. Keep headings with their content and never split a table row from its required headers.
5. Reject empty, boilerplate-only, duplicate, and provenance-less chunks.
6. Evaluate recall@k, nDCG@k, index size, duplicate-result rate, context efficiency, and failure
   examples.
7. Select and version the default; document why losing strategies lost.
8. Require a new experiment and index version before changing chunk configuration.

**Commands**

```powershell
uv run pytest tests/ingestion/test_chunkers.py
uv run python -m enterprise_rag_evals.runner chunking --config configs/chunking.yaml
```

**Tests**

- Chunk generation is deterministic and IDs remain stable for unchanged inputs/configuration.
- Every output span resolves to exact source blocks and version.
- Heading, list, table, OCR, and oversize-paragraph fixtures preserve meaning; a non-English or
  uncertain-language parsed document is rejected before the chunker is invoked.
- Chunk boundaries and overlap never leak text from another document or ACL scope.
- Reprocessing does not duplicate chunks.

**Observability**

- Emit chunks/document, token distribution, overlap rate, dropped-block reasons, strategy/version,
  and time per page.

**Evidence**

- `docs/reports/chunking-experiment.md` contains dataset, hypotheses, parameters, metrics, plots/tables,
  failures, chosen strategy, and reproducible command.

**Done when**

- A measured, versioned default beats or justifiably matches the fixed baseline and every chunk
  retains exact-version provenance.

## Part 8 - Embeddings and dense index

### Stage 8.1 - Versioned embedding interface and pgvector search

**Objective**

Create deterministic batch embedding and authorization-filtered pgvector search without coupling
domain logic to a particular model library.

**Prerequisites**

- Stage 7 produces validated chunk records.

**Technology**

- `sentence-transformers`, pgvector, cosine similarity, local model cache, and HNSW.

**Files**

- `packages/embeddings/enterprise_rag_embeddings/{base,sentence_transformers,registry}.py`.
- `packages/retrieval/enterprise_rag_retrieval/dense.py`.
- Embedding repository and worker batch helper.
- `tests/retrieval/test_dense.py`, `tests/embeddings/test_provider.py`.
- `docs/stages/stage-08-dense-index.md`.

**Contracts**

```python
class EmbeddingProvider(Protocol):
    @property
    def descriptor(self) -> EmbeddingDescriptor: ...
    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]: ...
    def embed_queries(self, texts: Sequence[str]) -> list[list[float]]: ...
```

`EmbeddingDescriptor` contains model ID, immutable revision/digest, dimension, normalization,
distance function, library version, and maximum sequence length.

- Default model is `sentence-transformers/all-MiniLM-L6-v2`, 384 dimensions, normalized vectors,
  cosine search.
- `EMBEDDING_MODEL_REVISION` is an immutable upstream commit/revision and
  `EMBEDDING_MODEL_MANIFEST_SHA256` is the SHA-256 of a canonical manifest containing every local
  artifact filename, size, and SHA-256. Both are mandatory outside an insecure local experiment.
- Query and document methods stay distinct even when the initial model treats them identically.
- Embeddings are keyed by chunk ID plus full descriptor; changing any descriptor creates a new
  index version.
- Dense retrieval uses the canonical Stage 4 tenant, lifecycle, and ACL predicate before ranking
  and limiting candidates. Part 10 later proves parity and zero leakage across every retrieval and
  downstream surface; it does not add authorization after an unsafe retriever already exists.

**Implementation steps**

1. Resolve/download the model only in an explicit image-build/artifact-acquisition step using the
   configured immutable revision; generate the canonical file manifest and fail the build if its
   digest differs from configuration.
2. At runtime load with local-files-only behavior, recompute/verify the manifest digest, and refuse
   startup on a missing revision, missing file, digest mismatch, dimension mismatch, or mutable
   revision.
3. Validate dimension and finite values before database insert.
4. Batch by token/record limit with bounded memory and deterministic input order.
5. Upsert by the unique chunk/model key.
6. Implement exact cosine search for tests and HNSW search for runtime.
7. Record search parameters (`ef_search`, limit, filters) in the query trace.
8. Provide a deterministic fake provider for unit tests.
9. Benchmark batch throughput and quality on CPU; do not require a GPU.

**Commands**

```powershell
uv run pytest tests/embeddings tests/retrieval/test_dense.py
uv run python -m enterprise_rag_evals.runner retrieval --retriever dense --dataset business
```

**Tests**

- Mock provider is deterministic; real-provider smoke test validates descriptor/dimension.
- Missing/mutable revision, missing digest, modified artifact, and manifest mismatch fail build or
  runtime before an index/query can use the model.
- Same chunk and descriptor never produce duplicate rows.
- Non-finite, wrong-dimension, partial-batch, and model-load failures are controlled.
- Dense results contain only the trusted identity's authorized chunks in the requested tenant and
  active index version, including same-tenant deny cases.
- Known semantic query fixture retrieves its relevant chunk.
- Approximate results stay within the documented recall tolerance of exact search.

**Observability**

- Measure embed batch size/tokens/duration, model-load duration, failures, vector count, index size,
  dense-search latency, and candidate count.

**Evidence**

- Record descriptor, artifact checksum, host hardware, throughput, index parameters, and dense
  baseline metrics in the stage record.

**Done when**

- Dense indexing is repeatable and versioned; dense search is authorization-filtered and measured
  against an exact-search test and labeled query set.

## Part 9 - Lexical, dense, and hybrid retrieval

### Stage 9.1 - PostgreSQL FTS and reciprocal rank fusion

**Objective**

Implement lexical retrieval and compare lexical, dense, hybrid, and reranked candidates under one
typed contract, satisfying the measurable foundation of `RAG-RET-01`.

**Prerequisites**

- Stages 7-8 `Done when` criteria are locally verified.

**Technology**

- PostgreSQL FTS, pgvector, weighted reciprocal rank fusion (RRF), and query normalization.

**Files**

- `packages/retrieval/enterprise_rag_retrieval/{contracts,lexical,dense,fusion,service}.py`.
- `tests/retrieval/test_lexical.py`, `test_fusion.py`, `test_service.py`.
- `docs/retrieval-contract.md`, `docs/stages/stage-09-hybrid-retrieval.md`.

**Contracts**

```python
class RetrievalRequest(BaseModel):
    query: str
    identity: IdentityContext
    top_k: int = Field(ge=1, le=50)
    filters: RetrievalFilters
    index_version: str

class Candidate(BaseModel):
    chunk_id: UUID
    document_version_id: UUID
    lexical_rank: int | None
    lexical_score: float | None
    dense_rank: int | None
    dense_score: float | None
    fused_score: float
```

- `identity` is attached by trusted server middleware after token and server-side membership
  validation. It is not part of the public request-body schema.
- FTS weights title/heading higher than body/table text.
- The runtime lexical score is PostgreSQL `ts_rank_cd`; do not label it BM25.
- A deterministic `rank-bm25` adapter supplies the required offline BM25 comparison baseline over
  the same versioned corpus. It is not the production query path.
- Query parsing uses bounded `websearch_to_tsquery`; syntax errors cannot become SQL.
- Both runtime retrievers apply the trusted `IdentityContext` through the canonical tenant,
  lifecycle, and ACL predicate before ranking and candidate limits.
- Dense and lexical lists each retrieve a configurable candidate pool, initially 50.
- RRF uses `score = sum(weight / (k + rank))`, initially `k=60`, with weights recorded in config.
- Raw FTS, BM25-baseline, and cosine scores are not directly added.
- Filters are allowlisted structured fields; arbitrary SQL or user-provided operators are forbidden.

**Implementation steps**

1. Build lexical repository queries using bound parameters and the generated GIN index.
2. Normalize Unicode and whitespace; preserve exact identifiers, codes, and quoted phrases.
3. Retrieve lexical and dense candidates concurrently under one timeout budget.
4. Fuse by stable chunk ID and preserve component ranks/scores for explanation and evaluation.
5. Deterministically tie-break by fused score, best component rank, then chunk ID.
6. Add bounded optional synonym/query rewrite hooks, disabled by default and versioned.
7. Build the offline BM25 baseline and compare BM25, PostgreSQL FTS, dense, and hybrid on identical
   query judgments.
8. Store the full retriever configuration hash with every query run.

**Commands**

```powershell
uv run pytest tests/retrieval/test_lexical.py tests/retrieval/test_fusion.py
uv run python -m enterprise_rag_evals.runner retrieval --retriever bm25_eval --dataset business
uv run python -m enterprise_rag_evals.runner retrieval --retriever lexical --dataset business
uv run python -m enterprise_rag_evals.runner retrieval --retriever dense --dataset business
uv run python -m enterprise_rag_evals.runner retrieval --retriever hybrid --dataset business
```

**Tests**

- Exact product code and rare phrase favor lexical; paraphrase fixture favors dense.
- Hybrid contains the union and calculates RRF from ranks exactly.
- Empty, huge, malformed, stopword-only, and adversarial query inputs are bounded.
- Filter values are parameterized and cannot alter SQL.
- Same-tenant denied chunks never appear in either component list or the fused union.
- Timeout in one retriever produces the documented degraded path or a controlled failure.
- Stable inputs/configuration produce stable ordering.

**Observability**

- Trace lexical, dense, and fusion spans with pool size, returned count, duration, timeout, and
  configuration version.
- Measure empty-result rate, lexical/dense overlap, and rank movement without high-cardinality
  labels such as query text or chunk ID.

**Evidence**

- `docs/retrieval-contract.md` specifies ranking, filters, tie-breaking, limits, timeouts, and
  degraded behavior.
- Record the BM25/FTS/dense/hybrid baseline table and query-level failure examples.

**Done when**

- Lexical, dense, and hybrid retrieval share one contract, are reproducible, and have separate
  measured results on the same labeled set.

## Part 10 - Pre-retrieval permission filters

### Stage 10.1 - Authorized candidates only

**Objective**

Complete `RAG-AUTH-02`: unauthorized document versions must never enter candidate lists,
reranking, context, citations, caches, traces, exports, or MCP results.

**Prerequisites**

- The Stage 4 authorization predicate and Stage 9 retrieval-service `Done when` criteria are
  locally verified.

**Technology**

- PostgreSQL `EXISTS`/join ACL predicates, trusted identity context, query plans, and security
  regression datasets.

**Files**

- `packages/retrieval/enterprise_rag_retrieval/filters.py`.
- Permission-aware PostgreSQL adapter and repository queries.
- `tests/security/test_retrieval_acl.py`, `tests/retrieval/test_filter_plans.py`.
- `packages/evals/enterprise_rag_evals/datasets/acl_cases.jsonl`.
- `docs/stages/stage-10-permission-retrieval.md`.

**Contracts**

- The API creates `RetrievalRequest.identity` from trusted middleware; JSON input cannot set it.
- Both lexical and dense SQL include tenant, active version, lifecycle state, and ACL predicates
  before `ORDER BY` and `LIMIT`.
- Post-filtering an unauthorized top-k list is prohibited.
- Citation resolution repeats authorization against the current identity and active policy.
- Permission-aware cache keys include tenant, user/subject-scope hash, ACL version, index version,
  query/config hash, and result limit.
- ACL revocation increments a version and invalidates matching cache namespaces.

**Implementation steps**

1. Express one reviewed SQL predicate for active ACL matches and reuse it in both retrieval paths.
2. Bind the current server-side identity and effective time.
3. Apply filters before ANN/FTS ranking and candidate limits; verify with `EXPLAIN`.
4. Record only a non-reversible identity-scope hash in query traces.
5. Add invariant assertions at retrieval output, reranker input, context input, and citation output.
6. Make cache reads revalidate ACL/index version; never cache across tenants.
7. Build an adversarial corpus with identically worded public and restricted documents in two
   tenants so accidental leakage is easy to detect.
8. Fail closed if group lookup, ACL query, cache metadata, or version state is unavailable.

**Commands**

```powershell
uv run pytest tests/security/test_retrieval_acl.py
uv run python -m enterprise_rag_evals.runner permissions --dataset acl
```

**Tests**

- Direct IDs, semantic similarity, exact phrase, filters, pagination, caches, and citations cannot
  reveal inaccessible documents.
- Results are correct for user, group, role, tenant-public, expired, revoked, and deleted ACLs.
- Identical chunk text in two tenants never crosses the tenant boundary.
- A revoke denies the next uncached and cached query.
- Authorization dependency failure returns a controlled denial, never unfiltered search.
- SQL-plan assertions show ACL conditions occur inside candidate-producing queries.

**Observability**

- Count candidate queries, deny reasons, cache ACL-version misses, and invariant violations.
- A suspected unauthorized candidate produces a security alert and aborts the whole response.

**Evidence**

- Store the adversarial ACL dataset, zero-leak test report, reviewed query plans, and revocation
  timing in the stage record and security eval report.

**Done when**

- The zero-tolerance ACL gate passes for every retrieval and cache path, and authorization failure
  is demonstrably fail-closed.

## Part 11 - Reranking, context assembly, and evidence packets

### Stage 11.1 - Cross-encoder reranking and bounded evidence

**Objective**

Rerank only authorized candidates, diversify redundant results, and assemble a token-bounded,
provenance-complete evidence packet for generation.

**Prerequisites**

- Stage 10 returns authorized hybrid candidates only.

**Technology**

- `sentence-transformers` cross-encoder, maximum marginal relevance or deterministic diversity
  rules, and tokenizer-aware context assembly.

**Files**

- `packages/retrieval/enterprise_rag_retrieval/{rerank,context}.py`.
- `packages/domain/enterprise_rag_domain/evidence.py`.
- `tests/retrieval/test_rerank.py`, `tests/retrieval/test_context.py`.
- `docs/stages/stage-11-rerank-context.md`.

**Contracts**

```python
class EvidenceItem(BaseModel):
    evidence_id: str
    chunk_id: UUID
    document_id: UUID
    document_version_id: UUID
    title: str
    text: str
    source_locator: dict[str, str | int]
    content_hash: str
    retrieval: dict[str, float | int | None]
    acl_version: str

class EvidencePacket(BaseModel):
    query_run_id: UUID
    query: str
    items: list[EvidenceItem]
    token_count: int
    retriever_config_version: str
    reranker_descriptor: str
    index_version: str
```

- Default reranker is `cross-encoder/ms-marco-MiniLM-L-6-v2` behind `Reranker`.
- `RERANKER_MODEL_REVISION` and `RERANKER_MODEL_MANIFEST_SHA256` follow the same immutable
  acquisition, canonical-manifest, local-files-only runtime, and fail-closed checks as Stage 8.
- Reranker input contains query and authorized candidate text only.
- Reranker scores reorder; they never create new candidates or override authorization.
- Default rerank pool is 30 and final evidence count is at most 8, within a configured token budget.
- Evidence IDs are random response-local identifiers, not authorization bypass tokens.
- Context retains exact chunk text and source locators; adjacent expansion repeats ACL/version checks.
- Contradictory evidence is preserved and labeled rather than silently collapsed.

**Implementation steps**

1. Implement deterministic fake and local cross-encoder rerankers behind one interface.
2. Acquire the exact configured revision at image build, verify the canonical artifact-manifest
   digest again at runtime, and record model ID/revision/digest/library/device with every query.
3. Batch candidate pairs with bounded text length and timeout.
4. Apply deterministic tie-breaking and a simple diversity cap per document/heading.
5. Assemble evidence in reranked order until the token budget is reached.
6. Preserve enough neighboring context only through an authorized chunk lookup.
7. Detect likely conflicting facts, stale versions, duplicate spans, and insufficient evidence.
8. Return a typed packet; generation cannot accept loose strings or arbitrary document text.

**Commands**

```powershell
uv run pytest tests/retrieval/test_rerank.py tests/retrieval/test_context.py
uv run python -m enterprise_rag_evals.runner retrieval --retriever hybrid_rerank --dataset business
```

**Tests**

- Reranker receives exactly the authorized candidate IDs and cannot add another ID.
- Missing/mutable revision or altered reranker artifact makes reranking not ready; it cannot be
  silently loaded under the same descriptor.
- Timeout follows the documented hybrid-only fallback and marks degraded mode.
- Context respects item/token/per-document limits and stable tie-breaking.
- Source locators and hashes are unchanged from stored chunks.
- Neighbor expansion cannot cross document/version/ACL boundaries.
- Duplicate and conflicting fixtures produce documented flags.
- Reranking meets the starter improvement gate or configuration disables it.

**Observability**

- Measure rerank pool, duration, fallback, rank movement, evidence token count, truncation, duplicate
  rate, document diversity, and conflict flags.

**Evidence**

- Add reranker descriptor, ablation table, latency, quality delta, and failure cases to the
  retrieval eval report and stage record.

**Done when**

- The evidence packet is authorized, bounded, reproducible, provenance-complete, and reranking is
  justified by measured value.

## Part 12 - Grounded generation, citations, and abstention

### Stage 12.1 - Provider-neutral answer pipeline

**Objective**

Implement `RAG-CIT-01`, `RAG-ABS-01`, and the generation half of `RAG-SEC-01`: answer only from an
authorized evidence packet, cite exact source spans, and abstain when evidence is insufficient.

**Prerequisites**

- Stage 11 produces typed evidence packets.
- The mock provider is used until all non-provider tests pass.

**Technology**

- Pydantic structured outputs, Markdown prompt assets, provider-neutral HTTP gateway, citation
  resolver, and deterministic validation.

**Files**

- Generation contracts, gateway, mock and hosted HTTP providers.
- `prompts/grounded_answer.v1.md`, prompt registry, citations, and abstention policy.
- `tests/generation/test_gateway.py`, `test_grounding.py`, `test_citations.py`,
  `test_abstention.py`.
- `docs/system-card.md`, `docs/stages/stage-12-generation.md`.

**Contracts**

```python
class AnswerClaim(BaseModel):
    claim_id: str
    text: str
    evidence_ids: Annotated[list[str], MinLen(1)]

class ModelAnswerPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["answered", "abstained", "needs_clarification"]
    claims: list[AnswerClaim]
    abstention_reason_code: AbstentionReason | None
    missing_information_codes: list[MissingInformationCode]
    warning_codes: list[AnswerWarning]

class RenderedGroundedAnswer(BaseModel):
    status: Literal["answered", "abstained", "needs_clarification"]
    answer_markdown: str  # created only by the deterministic server renderer
    claims: list[ValidatedClaim]
    citations: list[RenderedCitation]
```

- The provider returns only `ModelAnswerPlan`; there is no provider-controlled `answer_markdown`,
  introduction, conclusion, link, citation label, or free-form warning/abstention field.
- For `answered`, at least one ordered claim is required and every claim has evidence. For
  `abstained`/`needs_clarification`, claims must be empty and only controlled reason/missing-
  information codes are allowed.
- The server validates and sanitizes each claim, resolves evidence, then renders the answer
  deterministically from the ordered validated claims plus server-generated citation markers.
  Abstention text, clarification questions, headings, warnings, and links come from versioned
  server templates keyed by controlled codes.
- Provider input is system/developer instructions plus a serialized `EvidencePacket` inside an
  explicit untrusted-data boundary.
- The model receives opaque evidence IDs and must associate every factual claim with at least one.
- The local validator rejects unknown fields, unknown IDs, inaccessible/currently revoked evidence,
  version/hash mismatch, evidence-less claims, invalid state/claim combinations, invalid schema,
  raw HTML/links, or claim text outside configured bounds.
- Citation rendering resolves server-side to document title, version, page/heading/cell/span, and
  authorized preview.
- The deterministic answer policy can force abstention before or after generation based on no
  evidence, low retrieval support, conflict, staleness, unsupported claims, or validator failure.
- Provider output never changes permissions, retrieves more documents, calls a tool, or writes data.

**Implementation steps**

1. Define `GenerationProvider.generate_structured()` with timeout, usage, provider/model descriptor,
   raw response ID, and controlled error classes.
2. Implement a deterministic mock that covers answered, abstained, malformed, and injected cases.
3. Implement one hosted HTTP adapter configured by base URL, API key, model, timeout, and schema
   capability; keep provider-specific request mapping inside the adapter.
4. Render the versioned prompt with the user question, safe answer policy, and evidence packet.
5. State that evidence may contain malicious instructions and must only support factual content.
6. Parse `ModelAnswerPlan` with `extra="forbid"`, then run deterministic state, claim, citation
   existence, authorization, version, span, and coverage validation.
7. Render `RenderedGroundedAnswer` only from validated claims and server templates; escape Markdown
   metacharacters in claim text and create citation links only through the authorized API route.
8. Force controlled abstention on validation failure; never return or store an unvalidated provider
   draft as an answer.
9. Store prompt hash/version, provider/model/route revision, evidence IDs/hashes, validated plan,
   renderer version, rendered-output hash, validation result, tokens, latency, and cost.

**Commands**

```powershell
uv run pytest tests/generation
uv run python -m enterprise_rag_evals.runner answers --provider mock --dataset business
uv run python -m enterprise_rag_evals.runner answers --provider mock --dataset unanswerable
```

**Tests**

- Every returned factual claim has valid, authorized, exact-version evidence.
- Unknown, fabricated, duplicate, stale, deleted, and cross-tenant evidence IDs reject.
- Prompt injection inside a retrieved chunk cannot reveal prompt, change policy, or add tools.
- No/weak/conflicting evidence triggers abstention or clarification.
- Provider timeout, rate limit, invalid schema, and validator failure return controlled states.
- Mock and hosted adapters implement the same contract.
- Citation preview repeats authorization and fails after revocation.
- Provider output containing `answer_markdown`, free-form warning/abstention text, raw link/HTML, or
  any unknown field rejects.
- The rendered answer equals the deterministic renderer's exact output for the stored validated
  claims; property tests prove no parallel free-form answer path exists.

**Observability**

- Trace prompt render, provider call, schema validation, citation validation, and answer policy.
- Measure answer/abstain/clarify, validation failures by reason, evidence count/tokens, provider
  latency/tokens/cost, citation coverage, and groundedness eval result.
- Never log full evidence or raw prompt by default.

**Evidence**

- `docs/system-card.md` records capabilities, limitations, provider/data flow, abstention policy,
  human-use boundary, and residual risk.
- Stage evidence includes an answer, an abstention, an injection rejection, and exact source-span
  resolution.

**Done when**

- Only validated grounded answers leave the service, all citations resolve under current
  authorization, and the abstention gates pass on the starter sets.

## Part 13 - Async indexing, updates, deletion, retry, and reconciliation

### Stage 13.1 - Idempotent document lifecycle

**Objective**

Implement `RAG-ING-02`: durable, idempotent queue processing with version activation, update and
delete propagation, retry policy, dead-letter recovery, and periodic reconciliation.

**Prerequisites**

- Stages 5-12 components work synchronously in tests.

**Technology**

- Redis, RQ, PostgreSQL outbox, leases/heartbeats, state machines, and reconciliation jobs.

**Files**

- Worker queues/main and jobs for ingest, delete, reconcile, and evaluate.
- Reliability idempotency, retry, DLQ, and reconciliation modules.
- Job routes/schemas and outbox publisher.
- `tests/reliability/test_jobs.py`, `test_outbox.py`, `test_delete_propagation.py`.
- `docs/stages/stage-13-async-lifecycle.md`.

**Contracts**

Lifecycle:

```text
uploaded -> queued -> parsing -> parsed -> chunking -> embedding -> indexing
         -> validating -> candidate_ready -> awaiting_publication_approval
         -> approved -> promoted -> active
any processing state -> failed_retryable -> queued
any processing state -> failed_terminal | needs_review
candidate_ready/awaiting_publication_approval -> rejected
active -> superseded
active/superseded -> delete_requested -> deleting -> deleted | deletion_blocked_retention
```

- Job identity is `(tenant_id, document_version_id, operation, pipeline_config_hash)`.
- At-least-once delivery is assumed; each step is idempotent and restartable.
- Ingest, deletion, evaluation, and maintenance run in separate RQ queues and OS/container worker
  pools with independent concurrency, resource limits, service identities, heartbeats, retries, and
  DLQs. Deletion has reserved capacity and cannot be starved by ingestion or eval load.
- Validation creates a non-queryable candidate. It cannot become active until an authorized
  operator records an immutable publication approval containing candidate/config/eval/evidence
  hashes, base current-index version, decision/reason, approver, and timestamp.
- `POST /v1/admin/index-generations/{id}:approve` records approval; a separate
  `POST /v1/admin/index-generations/{id}:promote` transaction rechecks approval freshness,
  compatibility, zero critical gates, and unchanged base index before atomically switching the
  current route. Workers cannot self-approve or auto-promote.
- The old active version remains searchable until the new version activates, then becomes
  superseded atomically.
- Delete first revokes visibility in the source-of-truth query path, then removes derived rows and
  objects asynchronously. Failed physical cleanup does not restore visibility.
- Deletion enumerates every database-tracked raw/derived `(bucket,key,version_id)` and reconciles it
  with S3 `ListObjectVersions` for the document prefixes. It explicitly deletes every object version
  and delete marker by `VersionId`, then verifies no unexcepted version remains. A legal hold,
  Object Lock, or documented retention rule creates `deletion_blocked_retention` evidence with
  authority, reason, expiry/review date, and inaccessible tombstone; it is never reported as fully
  deleted.
- Access-control changes take effect independently of re-embedding.
- Starter P95 freshness/delete SLA is five minutes; security revocation is immediate at query time.

**Implementation steps**

1. Publish outbox events only after the intake transaction commits.
2. Use a short database lease and heartbeat so crashed jobs can be reclaimed.
3. Persist step checkpoints and output hashes; skip verified completed work on retry.
4. Classify transient storage/database/provider/resource failures separately from terminal parse,
   validation, or policy failures.
5. Apply bounded exponential backoff with jitter; after the configured attempts, write a DLQ record
   with safe error details.
6. Validate chunk/vector/FTS counts, dimensions, ACLs, retrieval/eval gates, model digests, and
   version state, then create the candidate evidence hash and await audited approval/promotion.
7. Update via new immutable version; never index partially into the active version.
8. Tombstone visibility transactionally, invalidate caches, remove index/database derivatives,
   delete every tracked and discovered S3 raw/derived version/delete marker, and persist per-version
   verification or retention-exception evidence.
9. Run a reconciliation job comparing database state, object keys, embeddings, index rows, outbox,
   queue registry, and expired leases.
10. Provide safe operator retry/reconcile endpoints with role checks and audit logs.

**Commands**

```powershell
uv run rq worker ingestion --name worker-ingest --url redis://localhost:6379/0
uv run rq worker deletion --name worker-delete --url redis://localhost:6379/0
uv run rq worker evaluation --name worker-eval --url redis://localhost:6379/0
uv run rq worker maintenance --name worker-maintenance --url redis://localhost:6379/0
uv run pytest tests/reliability/test_jobs.py tests/reliability/test_outbox.py
uv run pytest tests/reliability/test_delete_propagation.py
```

**Tests**

- Delivering any event twice produces one logical result.
- Worker crash at every checkpoint resumes without partial active content.
- Candidate remains invisible without approval; stale/wrong-base/self approval fails; audited
  approval plus promote activates atomically and old version stops appearing.
- Saturating ingestion/eval leaves reserved deletion capacity; queues, DLQs, credentials, and
  heartbeats cannot be substituted across pools.
- Delete immediately hides content and removes chunks/vectors plus all tracked/discovered MinIO/S3
  object versions and delete markers within the measured SLA.
- Legal-hold/Object-Lock fixtures remain inaccessible, record exact exceptions, and cannot produce
  a false `deleted` completion state.
- ACL-only change needs no re-embedding and invalidates permission-aware caches.
- Retryable failures back off; terminal failures do not loop; exhausted jobs enter DLQ.
- Reconciliation finds and safely repairs orphan objects, missing embeddings, stale leases, and
  unsent outbox events.
- Concurrent update/delete has a deterministic guarded outcome.

**Observability**

- Metrics: queue depth/age, job state, attempts, heartbeat age, stage duration, DLQ count, freshness
  lag, delete lag, reconciliation drift, and activation failures.
- Trace each job with document/version, pipeline hash, checkpoint, and safe error code.

**Evidence**

- Create `docs/reports/freshness-delete-report.md` with P50/P95/max across normal, retry, crash, update,
  ACL-change, and delete cases.
- Record a DLQ replay and a reconciliation repair in the stage document.

**Done when**

- At-least-once delivery cannot duplicate or expose partial content, and update/delete/revocation
  behavior meets the starter gates with recoverable failures.

## Part 14 - Search, answer, and conversation APIs

### Stage 14.1 - Stable product contracts

**Objective**

Expose permission-aware employee, owner, operator, and compliance contracts without leaking
implementation details or allowing conversation history or evidence exports to become authority.

**Prerequisites**

- Stages 4-13 `Done when` criteria are locally verified.

**Technology**

- FastAPI, Pydantic, cursor pagination, HTTP problem/error schema, and optional server-sent events
  for answer progress.

**Files**

- Document, job, search, answer, admin-publication, and compliance evidence-bundle schemas/routes.
- Query/answer repositories and service orchestration.
- `tests/api/test_search.py`, `tests/api/test_answers.py`, `tests/api/test_citations.py`,
  `tests/api/test_publication_admin.py`, `tests/api/test_compliance_evidence_bundles.py`.
- `docs/api-contracts.md`, `docs/stages/stage-14-product-api.md`.

**Contracts**

Minimum endpoints:

| Endpoint | Behavior |
|---|---|
| `POST /v1/sources` | register an approved source |
| `GET /v1/sources`, `GET /v1/sources/{id}` | authorized source catalog/state |
| `POST /v1/sources/{id}/syncs` | start an idempotent incremental source sync |
| `POST /v1/documents:ingest` | authorized intake |
| `POST /v1/documents/{id}:reprocess` | immutable candidate reprocessing |
| `DELETE /v1/documents/{id}` | tombstone and async deletion |
| `GET /v1/documents` | authorized catalog only |
| `GET /v1/documents/{id}/versions/{version}` | authorized metadata |
| `GET /v1/ingestion-runs/{id}` | tenant-scoped processing/publication state |
| `POST /v1/search` | authorized hybrid/reranked chunks |
| `POST /v1/answers` | grounded answer or abstention |
| `GET /v1/answers/{id}` | authorized stored answer |
| `GET /v1/citations/{citation_id}` | reauthorized exact span |
| `POST /v1/feedback` | user evaluation of search/answer/citation |
| `GET /v1/metrics/product` | authorized product/adoption metrics |
| `GET /v1/metrics/quality` | authorized retrieval/answer/citation metrics |
| `GET /v1/metrics/operations` | authorized freshness/error/latency/queue metrics |
| `GET /v1/metrics/cost` | authorized cost metrics |
| `POST /v1/admin/index-generations/{id}:approve` | audited operator approval of an exact candidate/evidence hash |
| `POST /v1/admin/index-generations/{id}:promote` | revalidated atomic current-index switch |
| `POST /v1/admin/index-generations/{id}:reject` | audited rejection with controlled reason |
| `POST /v1/admin/dlq/{job_id}:replay` | bounded audited replay to the originating isolated pool |
| `POST /v1/compliance/evidence-bundles` | create a tenant/release/source/requirement/time-scoped bundle job |
| `GET /v1/compliance/evidence-bundles/{id}` | read scoped build state and signed manifest hash |
| `GET /v1/compliance/evidence-bundles/{id}/download` | reauthorize and stream the immutable bundle |
| `GET /health`, `GET /ready` | process and dependency state |

- Requests have bounded query length, filters, history turns, and result count.
- Search response separates result snippets, scores/ranks, provenance, freshness, and warnings.
- Answer response exposes state, claims/citations, warnings, version tuple, and request ID.
- Conversation history is untrusted context used only for explicit query rewriting; every turn
  performs fresh retrieval and authorization.
- Do not automatically reuse old citations or evidence after ACL/index/version changes.
- Idempotency keys apply to upload, delete, feedback, and optional async-answer creation.
- Operator publication requests bind candidate ID/config hash, current-base index, release/eval
  evidence hashes, approver subject, decision/reason, and optimistic version. Promotion rejects
  missing/stale/self approval, changed base index, failed critical gate, or incompatible schema.
- Evidence-bundle scope is server-intersected with the compliance reviewer's tenant/source role and
  contains a signed manifest of release/version tuple, requirement traceability, approved eval/
  permission/security/freshness/cost reports, publication approvals, scoped audit/incident records,
  and artifact hashes. Raw documents, queries, evidence text, user feedback comments, secrets, and
  inaccessible-source existence are excluded by default. Every bundle item records classification,
  redaction, source hash, and authorization decision.

**Implementation steps**

1. Separate transport schemas from domain types and repository rows.
2. Use opaque cursor pagination; never expose raw SQL offsets as authorization state.
3. Centralize query validation, allowed filters, rate-limit identity, and request budgets.
4. Add synchronous search and answer first; optional SSE streams only status and validated final
   output, never unvalidated token text.
5. Store a conversation summary/query rewrite only with consent and retention controls.
6. Include safe `degraded_mode` indicators when reranking or generation is unavailable.
7. Implement operator approve/reject/promote and origin-queue DLQ replay with separation of duties,
   optimistic concurrency, immutable audit, and revalidation.
8. Build evidence bundles asynchronously, encrypt them, sign/hash the manifest, apply retention,
   create a short-lived subject-bound download handle, and reauthorize both status and download.
9. Generate and test OpenAPI; maintain request/response/error examples.

**Commands**

```powershell
uv run pytest tests/api/test_search.py tests/api/test_answers.py tests/api/test_citations.py
uv run pytest tests/api/test_publication_admin.py tests/api/test_compliance_evidence_bundles.py
powershell -File scripts/smoke.ps1 -BaseUrl http://localhost:8000
```

**Tests**

- Happy, empty, abstained, clarification, degraded, timeout, rate-limit, and invalid-filter cases.
- Every route tests missing identity, wrong tenant, revoked ACL, deleted version, and guessed ID.
- Pagination cannot skip permission filtering or reveal totals for inaccessible content.
- Conversation injection cannot set tenant/group/filter or reuse revoked evidence.
- SSE, if enabled, emits no unvalidated partial answer.
- OpenAPI schema snapshot changes only intentionally.
- Operator/owner/employee/compliance role-confusion, stale approval, self-approval, wrong candidate
  hash, concurrent promotion, and replay-to-wrong-pool cases fail.
- Evidence bundles include only the requested authorized scope, have reproducible manifest hashes,
  omit content/sensitive fields by default, deny guessed/expired/cross-tenant downloads, and audit
  creation/download.

**Observability**

- Request metrics by route/status/degraded state, bounded user/tenant dimensions, latency, and
  response size.
- Query and answer traces link without storing raw private content in default telemetry.

**Evidence**

- `docs/api-contracts.md` contains exact schemas, statuses, errors, examples, auth, idempotency,
  pagination, and degraded behavior.

**Done when**

- A client can complete the full authorized workflow from upload through exact citation using a
  stable, tested OpenAPI contract; operator promotion and compliance evidence export are executable
  and independently authorized.

## Part 15 - Web UI and feedback

### Stage 15.1 - Employee, knowledge-owner, operator, and compliance workflows

**Objective**

Build a simple trustworthy UI that distinguishes search evidence from generated answers, exposes
freshness and permissions clearly, and captures structured feedback.

**Prerequisites**

- Stage 14 API contracts are stable.

**Technology**

- React, Vite, TypeScript, accessible HTML, API-generated types, and Playwright.

**Files**

- Web pages/components/API/types from the target tree.
- Feedback schemas/routes and repository.
- `tests/e2e/search-answer.spec.ts`, `tests/e2e/operator-compliance.spec.ts`,
  `tests/api/test_feedback.py`.
- `docs/feedback-to-eval-loop.md`, `docs/stages/stage-15-ui-feedback.md`.

**Contracts**

Employee views:

- Search box with allowed filters and recent queries.
- Search results showing title, exact snippet, version/freshness, source locator, and access-safe
  metadata.
- Answer panel clearly labeled AI-generated, with claim-level citation controls.
- Abstention/clarification/degraded/error states.
- Citation preview that fetches the authorized exact span on demand.
- Feedback: helpful/not helpful, wrong answer, missing result, wrong ranking, wrong citation, stale
  source, access concern, unsafe content, and optional comment.

Knowledge-owner views:

- Upload and version creation.
- ACL preview and assignment.
- Processing status/warnings.
- Reprocess, delete, and DLQ/escalation status.
- Source/version/chunk summary, never a raw permission bypass.

Operator console:

- Isolated ingest/delete/eval/maintenance queue depth, heartbeat, DLQ, freshness, and deletion lag.
- Candidate validation/eval/evidence hashes with approve, reject, and separately confirmed promote.
- Current/prior index compatibility, reindex/reconcile controls, kill switches, and audited replay.
- No operator shortcut to read content that its document ACL does not authorize.

Compliance evidence view:

- Scope builder for allowed release, time range, sources, requirements, and evidence categories.
- Bundle state, manifest/hash/signature, redaction/classification summary, retention expiry, and
  authorized download.
- Permission/security gate status, publication approvals, incidents/exceptions, and explicit
  `not verified` items without raw private content.

**Implementation steps**

Create the Vite application once, add the declared dependencies, commit `package-lock.json`, and use
`npm ci` for every reproducible install thereafter.

1. Generate TypeScript types from OpenAPI and fail CI on drift.
2. Build search-only workflow before answer generation.
3. Render answer claims and citations from structured fields; sanitize Markdown and external links.
4. Show version date, indexing freshness, warnings, and answer abstention reason.
5. Make loading, empty, partial/degraded, denied, expired-session, and retry states explicit.
6. Meet keyboard navigation, focus, semantic label, color contrast, and screen-reader basics.
7. Make feedback idempotent and associate it with query/answer/citation/config versions.
8. Build operator confirmation/revalidation states and compliance bundle scope/status/download
   screens from generated OpenAPI types.
9. Never send a document body, query, bundle contents, or feedback comment to analytics.

**Commands**

```powershell
cd apps/web
npm ci
npm run lint
npm run test
npm run build
npx playwright test
```

**Tests**

- Employee can search, inspect source, ask, see citations, abstention, and submit feedback.
- Knowledge owner can upload, inspect processing, add an authorized version, and request delete.
- Wrong tenant/revoked ACL/expired session becomes a safe denied state with no stale screen content.
- Markdown/script/link injection is sanitized.
- Keyboard-only critical path and accessible names pass automated checks.
- Feedback retries do not duplicate records.
- Operator E2E proves candidate approve then separate promote, stale approval rejection, isolated
  queue/DLQ display, and full audit receipt.
- Compliance E2E proves scoped bundle creation/download, manifest verification, redaction summary,
  expired-handle denial, and absence of unauthorized/raw content.

**Observability**

- Product events: search submitted, result opened, answer requested, citation opened, abstained,
  feedback category, upload completion, and owner retry.
- Events contain IDs/config versions and coarse timing, not raw query/document/answer text.

**Evidence**

- Add screenshots or a short synthetic-data demo and accessibility results to the stage record.
- `docs/feedback-to-eval-loop.md` defines triage, privacy, labeling, deduplication, and promotion to
  eval cases.

**Done when**

- All four personas complete independently authorized workflows without hidden API knowledge, all
  states are explicit, evidence export is scoped/audited, and feedback can become versioned eval data.

## Part 16 - Layered evaluation and BEIR adapter

### Stage 16.1 - Failure-attributable evaluation system

**Objective**

Implement `RAG-EVAL-01`: evaluate ingestion, permissions, retrieval, reranking, answers, citations,
abstention, safety, latency, freshness, and cost as separate layers, then run an end-to-end report.

**Prerequisites**

- Stages 6-15 `Done when` criteria are locally verified.
- Labels come from public/synthetic/approved documents with dataset provenance.

**Technology**

- JSONL datasets, pytest-compatible scorers, deterministic runner, optional human rubric review,
  and a BEIR-format adapter.

**Files**

- Eval contracts, runner, reports, scoring modules, BEIR adapter, and datasets from the target tree.
- `tests/evals/test_scoring.py`, `test_runner.py`, `test_beir_adapter.py`.
- `docs/reports/ingestion-report.md`, `docs/reports/retrieval-benchmark-report.md`,
  `docs/reports/generation-citation-report.md`, `docs/reports/permission-eval-report.md`,
  `docs/reports/security-red-team-report.md`, `docs/reports/beir-benchmark-report.md`,
  `docs/reports/eval-report.md`, and `docs/dataset-card.md`.
- `docs/stages/stage-16-evaluation.md`.

**Contracts**

Each case contains:

```json
{
  "case_id": "business_001",
  "query": "How long are approved vendor records retained?",
  "identity_fixture": "tenant_a_employee",
  "relevant": [
    {"document_version_ref": "retention-policy:v3", "chunk_ref": "section-4"}
  ],
  "answerable": true,
  "reference_claims": ["Approved vendor records are retained for seven years."],
  "required_citation_refs": ["retention-policy:v3#section-4"],
  "tags": ["policy", "exact-version", "single-hop"]
}
```

Dataset partitions:

- Ingestion golden fixtures with block/span/table/OCR expectations.
- Business retrieval queries with graded relevance.
- Difficult queries: identifiers, negation, ambiguity, multi-section, conflicts, stale versions,
  and table questions; language-policy fixtures separately prove non-English content/query handling
  is safe and makes no multilingual quality claim.
- Unanswerable/clarification set.
- ACL isolation set.
- Injection and poisoning set.
- Feedback-mined candidate set quarantined from test labels until review.

Layer metrics:

| Layer | Metrics |
|---|---|
| Ingestion | block/span/table exactness, OCR character/field accuracy, parse coverage, warning rate |
| Retrieval | Recall@k, Precision@k, MRR@k, nDCG@k, zero-result rate |
| Reranking | nDCG delta, relevant rank movement, latency delta |
| Context | evidence recall, redundancy, token efficiency, conflict preservation |
| Answer | correctness rubric, groundedness, completeness, false-claim rate |
| Citation | validity, correctness/entailment, factual-claim coverage, exact-version rate |
| Abstention | precision, recall, false refusal, unsafe-answer rate |
| Permissions | unauthorized candidates/context/citations/cache/MCP count |
| Operations | P50/P95 latency, freshness/delete lag, error/degraded rate, cost |

**Implementation steps**

1. Version datasets, labels, corpus snapshot, code, index, model artifacts, prompts, scorers, and
   environment in every eval run.
2. Separate retrieval runs from answer runs so a generation change cannot hide retrieval failure.
3. Implement deterministic exact/IR scorers first; document any model-judge prompt, calibration,
   variance, and human audit.
4. Add 95% bootstrap confidence intervals when the set is large enough; show raw numerator and
   denominator for safety/ACL results regardless.
5. Compare fixed-window vs structure/table-aware chunking; lexical vs dense vs hybrid vs reranked;
   mock vs hosted answer route where applicable.
6. Implement BEIR import/export mapping to the retrieval interface. Run one small public dataset,
   report standard IR metrics, and explicitly state that public benchmark quality does not prove
   business-corpus quality.
7. Fail release on starter-gate regression, zero-tolerance failure, missing lineage, or statistically
   unclear degradation requiring review.
8. Generate Markdown and machine-readable JSON reports.
9. Require failure-cluster notes and owner/action for every failed gate.

**Commands**

```powershell
uv run pytest tests/evals
uv run python -m enterprise_rag_evals.runner ingestion --dataset golden
uv run python -m enterprise_rag_evals.runner retrieval --dataset business --compare all
uv run python -m enterprise_rag_evals.runner answers --dataset business
uv run python -m enterprise_rag_evals.runner safety --dataset all
uv run python -m enterprise_rag_evals.runner beir --dataset scifact --retriever hybrid
```

**Tests**

- Hand-calculated examples validate every scorer and tie rule.
- Dataset schema, unique IDs, valid relevance refs, source licenses, and split separation validate.
- Same fixture/config produces same deterministic metrics.
- ACL and critical safety failures always fail regardless of average score.
- Answer scoring cannot run without pinned evidence/corpus and retrieval lineage.
- BEIR adapter preserves query/document/relevance IDs and reports unsupported fields.
- Report generator includes configuration, denominators, failures, and comparison baseline.

**Observability**

- Eval run duration, case count, failures by layer/tag, model calls/cost, and artifact versions.
- Keep eval traffic/cost separate from product dashboards and budgets.

**Evidence**

- Generate the named ingestion, retrieval, answer/citation, permission, safety, BEIR, and combined
  reports plus the dataset card.
- Reports include thresholds, confidence/limitations, failure clusters, launch recommendation, and
  open risks.

**Done when**

- A reviewer can attribute a failed answer to ingestion, retrieval, reranking, context, generation,
  citation, permission, or operations, and CI can enforce the calibrated gates.

## Part 17 - Security, privacy, injection, and poisoning

### Stage 17.1 - Threat-driven controls and adversarial tests

**Objective**

Complete `RAG-SEC-01` and harden every trust boundary: users, identity provider, uploads, parsers,
retrieved content, model provider, UI, operators, MCP clients, dependencies, and telemetry.

**Prerequisites**

- The full local workflow and layered safety dataset exist.

**Technology**

- Threat modeling, content-type validation, parser sandboxing, prompt/data separation, Pydantic,
  rate limiting, secret management, dependency/container scanning, audit, and log redaction.

**Files**

- Security middleware, sanitization/redaction helpers, upload inspection, answer policy controls.
- `tests/security/` suites for auth, ACL, upload, injection, poisoning, exfiltration, logs, UI, MCP,
  and abuse.
- `docs/threat-model.md`, `docs/system-card.md`, `docs/dataset-card.md`,
  `docs/provider-data-disclosure.md`, and `docs/reports/security-red-team-report.md`.
- `docs/stages/stage-17-security.md`.

**Contracts**

Threats and required controls:

| Threat | Required control |
|---|---|
| Cross-tenant or ACL leakage | trusted identity, pre-retrieval filters, fail closed, invariant tests |
| Direct prompt injection | fixed instructions, structured output, no model authority |
| Indirect injection in documents | untrusted evidence boundary, instruction-neutralization policy, safety set |
| Corpus poisoning | approved source/owner, scanner, provenance, review/quarantine, anomaly signals |
| Malicious files/parser exploit | signatures, limits, sandbox, patched parser images, no macros/network |
| Citation spoofing | server-generated IDs, exact version/hash/span resolution |
| Stale/deleted content | active-version filter, tombstone first, cache invalidation, reconciliation |
| Model/provider exfiltration | data minimization, provider allowlist, retention contract, egress restriction |
| XSS/unsafe links | sanitization, CSP, link allow/ warning, no raw HTML |
| SQL/filter injection | typed allowlisted filters and bound parameters |
| Denial of service | size/page/token/result/rate/concurrency/time limits and backpressure |
| Secret leakage | secret manager/env injection, redaction, scanning, rotation |
| Supply-chain compromise | lockfiles, artifact checksums, SBOM, dependency/container scanning |
| Operator misuse | least privilege, separation of duties, append-only audit, break-glass process |

- Retrieved content is factual evidence only. It cannot alter system policy, request tools, select
  tenants, expand ACLs, reveal hidden prompts, or choose model/provider configuration.
- Sources require an approved owner and classification. Untrusted external connectors quarantine
  content until policy checks pass.
- Provider payload is minimized to query plus authorized evidence needed for the task.
- Retention rules cover source bytes, parsed derivatives, chunks, query/answer records, feedback,
  provider logs, traces, backups, and deletion exceptions.

**Implementation steps**

1. Draw assets, actors, data flows, trust boundaries, abuse cases, controls, and residual risks.
2. Create a malicious corpus: hidden text, white-on-white instructions, Unicode obfuscation,
   prompt-extraction requests, fake citations, poisoned titles, conflicting policies, and data
   exfiltration instructions.
3. Add deterministic input and output controls; use a model safety check only as defense in depth.
4. Sandbox parser workers as non-root, read-only filesystem where possible, no unnecessary network,
   resource limits, and isolated temporary storage.
5. Apply CSP/security headers, Markdown sanitization, and safe download disposition.
6. Add route/user/tenant quotas and separate upload, indexing, search, answer, admin, and MCP limits.
7. Redact query/document/evidence/prompt content from routine logs; define approved debug capture
   with time-bound access and deletion.
8. Generate an SBOM and run dependency, secret, and container scans in CI.
9. Document encryption in transit/at rest, key ownership/rotation, provider data handling, and
   break-glass audit.
10. Review threats again before pilot and after every new source connector or tool surface.

**Commands**

```powershell
uv run pytest tests/security
uv run python -m enterprise_rag_evals.runner safety --dataset injection
uv run python -m enterprise_rag_evals.runner safety --dataset poisoning
```

**Tests**

- All ACL and tenant matrices remain zero-leak.
- Direct/indirect injection cannot change policy, reveal hidden instructions, invoke tools, or
  exfiltrate other evidence.
- Poisoned or unapproved source remains quarantined and absent from indexes.
- Malformed/oversized/recursive/macro-enabled files and parser resource exhaustion fail safely.
- Logs, traces, metrics, UI, errors, DLQ, and reports contain no configured secret or sentinel PII.
- XSS, unsafe URL, SQL/filter injection, cache confusion, and rate-limit tests pass.
- Revoked/deleted evidence cannot resolve through old answers or citations.
- Security test failures cannot be waived by an average quality score.

**Observability**

- Alert on authorization invariant violation, malware/poisoning signal, critical safety failure,
  unusual upload/answer volume, repeated denied access, secret-scan failure, and stale deletion.
- Security logs contain identities and object IDs needed for investigation, not private content.

**Evidence**

- Threat model lists control owner, test, residual risk, review date, and incident path.
- System/dataset cards document source approval, provider data sharing, intended use, limitations,
  and prohibited use.
- Vendor assessment and retention policy record provider eligibility, outbound fields, storage,
  subprocessors, deletion, encryption, audit, legal hold, and open approvals.
- Store the zero-critical-failure safety result in
  `docs/reports/security-red-team-report.md`.

**Done when**

- All zero-tolerance security gates pass, red-team failures have owners, and high residual risks
  block pilot or have explicit production-guide-approved acceptance.

## Part 18 - Reliability, caching, observability, cost, and SLOs

### Stage 18.1 - Operable and degradable runtime

**Objective**

Implement `RAG-OPS-01`: make one document and one query traceable end to end, keep authorization
correct under caching/failure, enforce budgets, and operate against measurable SLOs.

**Prerequisites**

- Stages 13 and 17 establish lifecycle and security behavior.

**Technology**

- Redis permission-aware cache, bounded retries/circuit breakers, OpenTelemetry, Prometheus,
  Grafana, JSON logs, and provider price configuration.

**Files**

- Reliability cache/retry/DLQ modules.
- Observability logging, metrics, tracing, and cost modules.
- Prometheus and Grafana configuration/dashboards.
- `tests/reliability/test_cache.py`, `test_degraded_modes.py`, `tests/observability/`.
- `docs/reports/cost-performance-report.md`, `docs/runbooks/observability-slo.md`,
  `docs/runbooks/incident-response.md`.
- `docs/stages/stage-18-operations.md`.

**Contracts**

Cache rules:

- Cache only normalized query embeddings, authorized retrieval result IDs, and safe catalog
  metadata. Generated answers are not cached in the first pilot.
- Retrieval key includes tenant, non-reversible identity-scope hash, ACL version, index version,
  embedding/reranker/retriever configuration, normalized query hash, filters, and limit.
- Cache values contain IDs and versions, not an authorization decision that outlives its version.
- Cache hits recheck current identity/ACL/index version and citation access.
- TTL starts at five minutes; ACL/delete events invalidate earlier.

Degraded modes:

- Generation unavailable: search and evidence remain available.
- Reranker unavailable: authorized hybrid results with a visible warning.
- One retriever unavailable: documented single-retriever result or controlled failure.
- Redis unavailable: uncached search and direct queue-health failure; never bypass authorization.
- Object storage unavailable: existing indexed search may work; upload/source preview is unavailable.
- PostgreSQL unavailable: not ready; no stale permission decisions served.

Every query/answer records a version tuple:

```text
application, schema, corpus snapshot, index, parser, chunker,
embedding model/revision, lexical config, fusion config,
reranker/revision, context policy, prompt, generation provider/model,
authorization/ACL version, evaluator version
```

**Implementation steps**

1. Add OpenTelemetry context propagation API -> database/cache -> retrieval -> reranker -> provider,
   and API -> queue -> worker -> storage/index.
2. Create structured log fields: request/trace/job/query/answer IDs, tenant, safe user hash,
   document/version, stage, configuration versions, state, error code.
3. Define low-cardinality Prometheus metrics and prohibit document, query, user, or chunk IDs as
   labels.
4. Add operations, ingestion/freshness, retrieval, answer/citation, permissions/security, product,
   and cost dashboards.
5. Store cost events using versioned price configuration; label estimates as estimates and
   reconcile provider billing where available.
6. Implement permission-aware cache and invalidation events.
7. Add timeouts, bounded retries, circuit breakers, concurrency limits, queue backpressure, and
   load shedding per dependency.
8. Define starter SLIs/SLOs, error budgets, alert thresholds, severity, owner, and runbook link.
9. Run failure and modest load exercises in the reference environment.

**Commands**

```powershell
docker compose up -d prometheus grafana
uv run pytest tests/reliability tests/observability
uv run python scripts/load_smoke.py --queries 100 --concurrency 5
```

**Tests**

- Cache keys separate tenant, identity scope, ACL/index/config version, filter, and result limit.
- Revoke/delete invalidates or makes old cache entries unusable within the gate.
- Dependency failures produce only documented degraded states and never disable ACLs/citations.
- Retries occur only for safe transient operations and respect total time budgets.
- One trace connects upload through activation and query through answer/citation/cost.
- Metrics have bounded labels; logs/traces pass redaction sentinels.
- Cost calculation handles unknown prices explicitly rather than returning zero.
- Load smoke meets stated latency gates in the recorded reference environment.

**Observability**

Required metrics include:

- Upload/parse/OCR/chunk/embed/index counts, duration, errors, queue age, freshness, deletion lag.
- Lexical/dense candidate count and latency, fusion overlap, rerank latency/fallback, evidence tokens.
- Search/answer latency, error, abstain, citation validation, provider tokens/cost.
- ACL deny/invariant, cache hit/miss/invalidation, rate limit, circuit state, DLQ/reconciliation drift.
- Feedback categories, result opens, citation opens, and pilot adoption.

**Evidence**

- Export dashboard JSON, a linked trace, `docs/reports/load-failure-report.md`,
  `docs/reports/capacity-report.md`, SLO table, cost-by-feature report, and incident exercise.
- The SLO runbook explains measurement windows and reference environment.

**Done when**

- The version tuple and cost are visible for one answer, caches preserve authorization, documented
  degraded modes work, and starter SLO/alert exercises have evidence.

## Part 19 - Optional secure read-only MCP search

### Stage 19.1 - Controlled knowledge tools

**Objective**

If the project claims Lesson 18/MCP evidence, expose the proven search/citation service through MCP
without adding write capability, permission choice, arbitrary query execution, or model-controlled
identity. Skip this stage explicitly as `planned` when MCP is outside the selected release scope.

**Prerequisites**

- Ordinary API authorization, retrieval, citations, security, and observability are complete.
- MCP is feature-flagged off by default.

**Technology**

- Optional `mcp` Python extra, streamable HTTP transport, OIDC client/delegated tokens, the existing
  retrieval service, rate limits, and audit.

**Files**

- `apps/mcp/enterprise_rag_mcp/{server,auth,tools}.py`.
- `Dockerfile.mcp`.
- `tests/mcp/test_tools.py`, `tests/security/test_mcp_acl.py`.
- MCP contract section in `docs/api-contracts.md`.
- `docs/stages/stage-19-readonly-mcp.md`.

**Contracts**

Expose only:

- `search_knowledge(query, filters?, limit?)`: returns authorized snippets, exact provenance,
  freshness, and opaque citation handles.
- `get_citation(citation_handle)`: reauthorizes and returns the exact approved span.

Do not expose:

- Upload, update, delete, ACL, reindex, raw object download, raw SQL, arbitrary filter expression,
  generic HTTP fetch, shell, file access, provider calls, or administrative metrics.

Security rules:

- `MCP_ENABLED=false` is the default and the API/worker images need not install the extra. When
  enabled, `Dockerfile.mcp` runs `uv sync --extra mcp`; startup fails unless the package,
  streamable-HTTP transport, bind/port, HTTPS edge, issuer, audience, required
  `knowledge.search` scope, non-empty client allowlist, timeout, result, and response-byte limits
  all validate.
- Deployed MCP accepts only TLS-terminated streamable HTTP. The token must match
  `MCP_OIDC_ISSUER_URL`/`MCP_OIDC_AUDIENCE`, an allowed client ID, and required scope; delegated user
  identity must be integrity-protected and mapped server-side. Stdio is local development only.
- Tenant/user/groups come from an authenticated trusted host assertion or delegated token, never
  tool arguments or model text.
- Tool schemas allowlist filters and cap query length, limit, response bytes, calls/minute, and
  execution time.
- Search and citation call the same domain services as the API.
- Citation handles are short-lived, scoped to tenant/user/ACL/index version, and non-forgeable.
- Tool descriptions explicitly say returned text is untrusted evidence, not instructions.

**Implementation steps**

1. Keep MCP transport/auth mapping outside the retrieval domain.
2. Install the optional extra only in the MCP image and validate the complete enabled/disabled
   configuration at startup/readiness.
3. Validate issuer/audience/scope/client allowlist and map delegated identity server-side.
4. Reject unknown fields and any tenant/identity/ACL parameter.
5. Call the same permission-filtered retrieval and current citation resolver.
6. Bound/sanitize content; return no hidden prompt, internal score details, object keys, or secrets.
7. Audit tool name, safe identity, request ID, configuration versions, result count, and denies.
8. Add kill switch, per-client allowlist, and separate rate/concurrency limits.
9. Threat-model confused deputy, replay, forged citation, prompt injection, result exfiltration, and
   compromised client cases.

**Commands**

```powershell
uv run pytest tests/mcp tests/security/test_mcp_acl.py
docker compose up --build mcp
```

**Tests**

- Tool arguments cannot select tenant, user, groups, ACL, raw SQL, object keys, or excess limits.
- API and MCP return the same authorized result IDs for the same trusted identity.
- Cross-tenant, revoked, expired-handle, replay, guessed-handle, and disabled-client cases fail.
- Retrieved injection text remains data and cannot cause another tool call or permission expansion.
- Rate, size, timeout, feature flag, and kill switch work.
- Disabled mode works without the optional package; every missing/invalid enabled-mode dependency
  or OIDC/transport/limit setting fails startup/readiness.
- Audit/redaction and zero-unauthorized-output gates pass.

**Observability**

- MCP request/tool/result/deny/timeout/rate metrics and linked retrieval traces.
- Alert on repeated forged identity/handle attempts or authorization invariant failures.

**Evidence**

- Document exact tool schemas, authentication, scopes, limits, threats, and kill switch.
- Record a same-identity API/MCP parity test and adversarial denial suite.

**Done when**

- When enabled, MCP adds only two read-only, bounded, audited tools and cannot bypass any API
  authorization, retrieval, citation, cache, or safety control.

## Part 20 - CI/CD and release gates

### Stage 20.1 - Reproducible, evidence-gated delivery

**Objective**

Prevent code, schema, index, model, prompt, security, and evaluation regressions from reaching a
release candidate.

**Prerequisites**

- All local quality/eval commands are deterministic or explicitly separated as hosted tests.

**Technology**

- GitHub Actions, service containers, Docker BuildKit, artifact/SBOM scans, migration checks, and
  signed/versioned release metadata.

**Files**

- `.github/workflows/ci.yml`, `.github/workflows/release.yml`.
- Dockerfiles, smoke scripts, eval-gate config, and release manifest generator.
- `tests/ci/`.
- `docs/stages/stage-20-ci-cd.md`.

**Contracts**

Pull-request jobs:

1. Lockfile/install integrity and license/secret scan.
2. Ruff formatting/check and mypy.
3. Unit tests with coverage.
4. PostgreSQL/pgvector, Redis, and MinIO integration tests.
5. Alembic upgrade from empty and previous release plus schema-drift check.
6. Parser fixture and idempotency tests.
7. Retrieval/ACL/citation/safety eval smoke with deterministic models.
8. Web lint/test/build and critical Playwright flow.
9. MCP security tests.
10. API/worker/web/MCP image builds, vulnerability scan, and SBOM.

Release-candidate jobs additionally run full labeled evals, staging migration/deployment smoke,
freshness/delete tests, backup verification, and manual approval. Hosted generation eval is a
protected, budgeted job, never an unreviewed fork pull-request job.

**Implementation steps**

1. Cache only dependency/model artifacts keyed by lock/digest; never cache secrets or test data
   across trust boundaries.
2. Pin actions by immutable version/commit according to repository policy.
3. Use least-privilege short-lived credentials and protected environments.
4. Upload machine-readable reports, coverage, SBOM, images, and release manifest with retention.
5. Fail on any critical ACL/security test, missing lineage, migration error, gate regression, or
   high-severity unaccepted vulnerability.
6. Build once and promote the same image digest from staging.
7. Create release manifest with code/image/schema/index/parser/chunker/embedding/reranker/prompt/
   provider/evaluator versions and rollback compatibility.
8. Require branch protection and independent review for security, migrations, and gate changes.

**Commands**

```powershell
uv run ruff format --check .
uv run ruff check .
uv run mypy apps packages
uv run pytest --cov=apps --cov=packages
docker compose config
docker compose build api worker web mcp
```

**Tests**

- A deliberate lint, type, unit, migration, ACL, eval, web, scan, and image failure blocks CI.
- CI has no real provider key in untrusted contexts.
- Release artifact digest matches staging-tested digest.
- Gate/config changes appear in reviewable diff and release manifest.
- Generated docs/reports are clearly marked and reproducible.

**Observability**

- Track CI duration, flake/retry, gate deltas, artifact digests, deployment status, and rollback
  rate.

**Evidence**

- Store a green run, an intentionally blocked critical test, release manifest, SBOM, scan result,
  and branch-protection screenshot/record.

**Done when**

- No release candidate can bypass tests, migrations, ACL/security gates, eval gates, artifact
  lineage, image scanning, or protected promotion.

## Part 21 - Deployment, rollback, reindex, backup, restore, and DR

### Stage 21.1 - Production-like local and staging deployment

**Objective**

Deploy the same immutable application artifacts through local and staging environments, then prove
application, configuration, index, database, prompt/model, and feature rollback paths.

**Prerequisites**

- Stage 20 release artifacts exist.

**Technology**

- Docker Compose locally and on a controlled staging Linux host, container registry, TLS reverse
  proxy/load balancer, managed-equivalent PostgreSQL/pgvector, Redis, S3, secrets, and telemetry.

**Files**

- Complete Compose and staging Compose/env example; add working Terraform modules for the chosen
  target, or mark infrastructure as code explicitly `planned` and `not verified` rather than
  checking in empty stubs.
- Build/deployment/smoke/backup/restore scripts.
- `docs/runbooks/rollback.md`, `docs/runbooks/reindex.md`,
  `docs/runbooks/backup-restore.md`, `docs/runbooks/incident-response.md`.
- `docs/stages/stage-21-deployment-dr.md`.

**Contracts**

- Local Compose runs `api`, `worker`, `web`, optional `mcp`, `postgres`, `redis`, `minio`,
  `prometheus`, and `grafana`.
- Staging uses synthetic/approved data, TLS, private dependencies, secret injection, persistent
  volumes/backups, and the same migration/release process intended for production.
- API and worker run non-root, with read-only filesystems where practical, resource limits,
  health checks, and graceful shutdown.
- Index version is an explicit route/alias. Build and validate a new index before atomic activation.
- PostgreSQL and object storage are authoritative; Redis/queues/caches are rebuildable.
- Starter portfolio RPO is 24 hours and RTO is 4 hours; calibrate to the business and record the
  actual restore result.

**Implementation steps**

1. Build and push immutable images; create a signed release manifest.
2. Provision network boundaries, database/pgvector, Redis, S3 bucket/versioning/lifecycle, secret
   store, telemetry, TLS, and backups.
3. Run backward-compatible migrations before application promotion.
4. Deploy worker before enabling new ingestion schema; deploy API/web/MCP behind feature flags.
5. Run health/readiness, upload-index-search-answer-citation, ACL, update/delete, and dashboard
   smoke tests.
6. Run full release evals against staging configuration.
7. Canary by tenant/source/category, monitor SLO/security/cost, then expand.
8. Test kill switches for generation, ingestion, MCP, reranker, and new index route.
9. Practice application image rollback, configuration rollback, prompt/provider route rollback,
   and index alias rollback. Prefer forward-fix for destructive database migrations.
10. Back up PostgreSQL and object metadata/versions; document Redis reconstruction.
11. Restore into an isolated environment, run migrations/reconciliation, rebuild or verify indexes,
   and execute ACL plus citation smoke tests.
12. Run a disaster scenario: database loss, object-store inconsistency, corrupted index, leaked
   provider key, or bad ACL release.

**Commands**

```powershell
docker compose up --build
powershell -File scripts/smoke.ps1
powershell -File scripts/deployment-smoke.ps1 -Environment staging
powershell -File scripts/backup.ps1 -Environment staging
powershell -File scripts/restore-drill.ps1 -Environment isolated-restore
```

**Tests**

- Fresh local start completes the synthetic workflow.
- Staging smoke proves tenant/ACL isolation and exact citation.
- New index is invisible until validation and atomic activation.
- Application/index/prompt/provider/feature rollback preserves search and permissions.
- Restore reaches a consistent corpus, active versions, ACLs, citations, and audit state.
- Missing Redis can be rebuilt without authoritative-data loss.
- Delete tombstones and retention obligations survive backup/restore.
- Secret rotation and generation/MCP kill switches work.

**Observability**

- Deployment markers, image/schema/index/config versions, canary health, migration duration, backup
  age, restore duration, reconciliation drift, and rollback events.

**Evidence**

- Runbooks contain exact prerequisites, commands, decision points, validation, abort criteria,
  owners, communication, and post-action review.
- Store staging smoke, rollback drill, reindex drill, backup integrity, restore timing, RPO/RTO
  result, and remaining gaps. Mark cloud-unverified claims as `not verified`.

**Done when**

- Staging passes gates using promoted artifacts, every high-risk rollback has been exercised, and an
  isolated restore meets or honestly reports against the starter RPO/RTO.

## Part 22 - Pilot and continuous improvement

### Stage 22.1 - Limited rollout and feedback-to-eval loop

**Objective**

Run a narrow, reversible pilot that measures business value, retrieval/answer quality, safety,
freshness, UX, latency, and cost, then makes an evidence-backed expand/iterate/rollback/stop decision.

**Prerequisites**

- Staging, security, eval, runbook, and restore evidence is accepted.
- The production guide's pilot entry criteria are met.

**Technology**

- Feature flags, tenant/source allowlists, dashboards, structured feedback, weekly failure review,
  and versioned eval datasets.

**Files**

- Pilot feature/config service and metrics endpoints.
- Feedback mining/eval-candidate workflow.
- `docs/reports/pilot-report.md`, `docs/feedback-to-eval-loop.md`.
- `docs/stages/stage-22-pilot-improvement.md`.

**Contracts**

- Start with one tenant/group, 25-100 approved documents, a small trained user cohort, and no
  autonomous actions.
- Feature flags independently control upload sources, generation, reranking, MCP, and pilot cohort.
- Baseline is the current keyword/manual knowledge workflow measured on the same task set.
- Feedback is evidence, not automatically a label. A reviewer verifies source, expected result,
  privacy, duplication, and train/test placement.
- No prompt/model/index/chunker/retriever change reaches pilot without versioned eval and release
  gates.

Pilot metrics:

- Search success/result-open rate and time to first useful source.
- Recall/ranking on sampled judged pilot queries.
- Answer helpfulness, correctness, groundedness, abstention, citation open/correctness.
- Zero unauthorized retrieval/context/citation and zero critical injection failures.
- Freshness/delete SLA, P95 search/answer latency, availability/degraded rate.
- Cost per search, generated answer, useful answer, and active user.
- Adoption, repeat usage, owner processing failures, feedback categories, and support burden.

**Implementation steps**

1. Define pilot users, sources, data classification, baseline, metrics, gates, owner, support path,
   duration, and stop conditions before enablement.
2. Seed dashboards and test alerts/kill switches.
3. Enable search first, then generation, then optional MCP only after earlier evidence is healthy.
4. Review rejected/low-rated answers, zero results, bad ranks, wrong citations, false abstentions,
   parser warnings, stale versions, and access concerns at least weekly.
5. Cluster failures by ingestion/retrieval/rerank/context/generation/citation/permission/UX/ops.
6. Promote reviewed representative failures to a quarantined candidate set, then a versioned
   difficult or safety set without contaminating the fixed test split.
7. Propose one controlled change, run ablation and gates, release behind a flag, and monitor.
8. Write the decision with business, quality, safety, cost, UX, and operational evidence.

**Commands**

```powershell
uv run python -m enterprise_rag_evals.runner release --config configs/pilot.yaml
uv run python -m enterprise_rag_evals.runner feedback-candidates --since 7d
```

**Tests**

- Non-pilot users/sources cannot access pilot features.
- Each flag and global kill switch changes only its documented surface.
- Feedback mining redacts/discards prohibited data and does not modify fixed labels automatically.
- Pilot dashboards reconcile with database events and cost records.
- Stop condition causes controlled disablement while ordinary source search/manual workflow remains.

**Observability**

- Pilot dashboard covers every listed metric with cohort/config version and no raw content.
- Alerts route to named owners and link to runbooks.

**Evidence**

- Pilot report states scope, baseline, data, versions, metrics, failures, incidents, user findings,
  cost, limitations, decision, and prioritized next work.
- Feedback-loop document shows at least one failure becoming a reviewed eval case and measured fix.

**Done when**

- The pilot decision is evidence-backed and reversible, no critical gate failed, and improvement
  occurs through versioned cases and releases rather than untracked prompt tuning.

## Part 23 - Documentation governance and canonical stage IDs

The production guide is the requirements authority. This technical guide is the build authority.
Living repository contracts are the implementation authority. Generated reports describe a
specific run; stage snapshots describe what was proved at a point in time. Never quietly use a
stale stage note to override a current contract.

Document classes:

| Class | Examples | Change rule |
|---|---|---|
| Living authoritative contract | architecture, API, data, ingestion, retrieval, ACL | update with implementation in the same PR |
| Architecture decision record | model/index/cache/provider choices | append a superseding decision; keep history |
| Immutable stage snapshot | `docs/stages/stage-*.md` | correct factual errors visibly; do not rewrite history |
| Generated report | eval, cost, freshness/delete, benchmark | regenerate with run/config/data lineage |
| Operational runbook | SLO, incident, rollback, reindex, backup/restore | review and exercise on schedule |
| Learning/progress record | learning notes, progress log | append verified work, failures, and open questions |

Use this evidence vocabulary consistently:

- `planned`: specified, no implementation claim.
- `implemented`: code/config exists, verification not yet recorded.
- `locally verified`: reproducible verification passed in the reference local environment.
- `externally verified`: passed in staging or an independent environment.
- `operationally proven`: exercised successfully during a controlled pilot or real operation.

Do not write "production ready" as an evidence level. State exactly what was verified and where.

Every stage snapshot uses these stable headings:

1. Status and evidence level.
2. Goal.
3. Guide and requirement mapping.
4. Runtime flow.
5. Files changed.
6. Contracts and data.
7. Failure behavior.
8. Tests.
9. Verification commands.
10. Verified evidence.
11. Not verified.
12. Learning questions.
13. Next stage.

Canonical stage IDs never drift from guide Parts:

| Stage ID | Guide Part | Stage record |
|---:|---:|---|
| 01 | 1 | `stage-01-repository-platform.md` |
| 02 | 2 | `stage-02-api-foundation.md` |
| 03 | 3 | `stage-03-data-model.md` |
| 04 | 4 | `stage-04-identity-acl.md` |
| 05 | 5 | `stage-05-upload-provenance.md` |
| 06 | 6 | `stage-06-parsing.md` |
| 07 | 7 | `stage-07-chunking.md` |
| 08 | 8 | `stage-08-dense-index.md` |
| 09 | 9 | `stage-09-hybrid-retrieval.md` |
| 10 | 10 | `stage-10-permission-retrieval.md` |
| 11 | 11 | `stage-11-rerank-context.md` |
| 12 | 12 | `stage-12-generation.md` |
| 13 | 13 | `stage-13-async-lifecycle.md` |
| 14 | 14 | `stage-14-product-api.md` |
| 15 | 15 | `stage-15-ui-feedback.md` |
| 16 | 16 | `stage-16-evaluation.md` |
| 17 | 17 | `stage-17-security.md` |
| 18 | 18 | `stage-18-operations.md` |
| 19 | 19 | `stage-19-readonly-mcp.md` |
| 20 | 20 | `stage-20-ci-cd.md` |
| 21 | 21 | `stage-21-deployment-dr.md` |
| 22 | 22 | `stage-22-pilot-improvement.md` |

Do not create combined stage records. A pull request may implement two stages, but each retains its
own contract, evidence level, unverified list, and progress entry.

## Part 24 - Minimal and full build paths

### Smallest complete portfolio build

The smallest defensible build still includes:

1. Reproducible Python repository and Docker Compose.
2. FastAPI health/readiness and typed errors.
3. PostgreSQL/pgvector schema and migrations.
4. Two tenants, user/service subjects, groups, document ACLs, and zero-leak tests.
5. MinIO upload with immutable object/version/checksum/provenance.
6. PDF, HTML, EML, DOCX, XLSX, TXT, and Markdown adapter contracts; at minimum PDF, HTML, and text
   implemented with a tested OCR/table path.
7. Fixed and structure-aware chunkers with a small comparison report.
8. Local sentence-transformer embeddings and pgvector dense search.
9. PostgreSQL FTS plus RRF hybrid retrieval.
10. Pre-retrieval ACL filters.
11. Local cross-encoder reranking and bounded evidence packet.
12. Deterministic mock plus one hosted generation adapter, exact citations, and abstention.
13. RQ ingestion/update/delete jobs with retry, DLQ, and reconciliation.
14. Search/answer/citation APIs and a simple employee UI.
15. At least 50 labeled business queries, 20 unanswerable cases, 20 ACL cases, and 20
    injection/poisoning cases. These are starter dataset sizes, not statistical sufficiency claims.
16. Separate retrieval and answer/citation reports; one small BEIR adapter run.
17. Threat model, security tests, structured logs, core metrics/traces, and cost events.
18. CI gates, full local Compose, rollback/reindex/restore notes, and final proof commands.

MCP, a hosted staging environment, full dashboards, broad format fidelity, and an operational pilot
may remain explicitly `planned` in the smallest build. If omitted, do not call the project
externally verified or operationally proven.

### Full production-style path

The full path completes all 22 stages and adds:

1. All listed format adapters and parser sandbox controls.
2. Larger representative labeled sets with independent relevance review.
3. OCR/table accuracy studies and near-duplicate review workflow.
4. Query classification/rewrite/decomposition only when eval proves value.
5. Parent-child or hierarchical retrieval only when the simple hybrid path has a measured gap.
6. Provider route/fallback comparison and billing reconciliation.
7. Staging with private managed-equivalent dependencies and a restore drill.
8. Optional secure MCP rollout after API parity and adversarial testing when MCP evidence is in
   scope.
9. Pilot cohort, business baseline, user research, incident exercise, and evidence-backed decision.
10. OpenSearch adapter only when PostgreSQL scale/latency evidence justifies it.

### OpenSearch later-scale decision

Do not migrate because OpenSearch sounds more enterprise. Consider it when measured corpus size,
query volume, FTS features, operational isolation, or latency cannot meet SLOs economically in
PostgreSQL. The adapter must:

- Implement the same `Retriever` and structured-filter contracts.
- Enforce ACLs before candidate limits.
- Preserve stable chunk/document/version IDs and exact citations.
- Support versioned blue/green indexes and delete propagation.
- Match or improve quality, security, freshness, latency, cost, and recovery gates.
- Pass API/PostgreSQL parity cases and all zero-tolerance tests.

Write the decision, migration/reconciliation design, dual-read comparison, rollback, and cost in an
ADR before enabling it.

## Part 25 - Requirement traceability matrix

The canonical requirement definitions live in the production guide. This matrix maps them to
implementation, tests, telemetry, and evidence. Expand it if the production guide adds IDs.

### Production-phase crosswalk

This prevents the production plan and technical stage numbering from drifting:

| Production phase | Technical realization |
|---:|---|
| 0 - Discovery, domain, acceptance | Pre-build discovery gate; Parts 23 and 25 |
| 1 - Repository, contracts, platform | Parts 1-2 and 23 |
| 2 - Identity, tenancy, authorization | Parts 3-4 and 10 |
| 3 - Source registry and raw artifacts | Part 5 |
| 4 - Parsing, OCR, normalization, provenance | Part 6 |
| 5 - Chunking and lexical baseline | Parts 7, 9, and search-only work in Part 14 |
| 6 - Dense, hybrid, reranked retrieval | Parts 8-11 and 16 |
| 7 - Publication, freshness, update, delete | Parts 13, 18, and 21 |
| 8 - Evidence, citations, employee UX | Parts 11, 14, and 15 |
| 9 - Grounded generation and abstention | Part 12 |
| 10 - Evaluation and release gates | Parts 16 and 20 |
| 11 - Observability, feedback, cost | Parts 15 and 18 |
| 12 - Security, privacy, governance | Part 17 |
| 13 - Reliability, load, failure injection | Parts 18 and 21 |
| 14 - Staging and rollback | Parts 20-21 |
| 15 - Controlled pilot | Part 22 |
| 16 - Continuous improvement and operations | Parts 16, 18, 22, and 23 |
| 17 - Portfolio defense | Parts 24, 26, and 30 |

### Requirement-to-evidence traceability

| Requirement | Technical realization | Required test/eval | Primary evidence |
|---|---|---|---|
| `RAG-AUTH-01` deny by default | Parts 4, 10, 14, 19 | identity/ACL truth table, property tests, route/MCP denies | ACL model and security report |
| `RAG-AUTH-02` no unauthorized candidate/context | Parts 9-12, 18-19 | adversarial two-tenant corpus; cache, rerank, context, citation, MCP checks | zero-leak report and reviewed query plans |
| `RAG-ING-01` provenance/versioning | Parts 5-7 | immutable source/version, span round-trip, deterministic chunk IDs | ingestion contract, source register, chunk report |
| `RAG-ING-02` idempotent update/delete SLA | Parts 5, 13, 18, 21 | duplicate delivery, crash checkpoints, update activation, delete/revoke/restore | freshness-delete report, reindex/restore runbooks |
| `RAG-RET-01` measured retrieval | Parts 7-11, 16 | lexical/dense/hybrid/rerank ablation, IR metrics, latency, BEIR adapter | retrieval and BEIR reports |
| `RAG-CIT-01` exact authorized citations | Parts 6-7, 11-12, 14 | valid version/hash/span, claim support/coverage, revoke/delete | answer/citation report and API contract |
| `RAG-ABS-01` controlled abstention | Parts 11-12, 16 | unanswerable, weak/conflicting/stale evidence, false-refusal set | answer report and system card |
| `RAG-EVAL-01` separate layer evals | Part 16 | scorer unit tests, lineage validation, release-gate behavior | ingestion/retrieval/answer/safety reports |
| `RAG-OPS-01` trace/cost/version tuple | Parts 13, 18, 20-22 | linked traces, redaction, metric labels, price/version records | dashboards, cost report, SLO/pilot reports |
| `RAG-SEC-01` untrusted retrieval/injection controls | Parts 6, 12, 17, 19 | injection, poisoning, parser/upload, XSS, exfiltration, MCP | threat model, system/dataset cards, safety report |

For every release candidate, produce a machine-readable traceability manifest with:

```json
{
  "requirement_id": "RAG-CIT-01",
  "implementation_version": "git-sha",
  "tests": ["test_exact_version_span", "test_revoked_citation_denied"],
  "eval_run_id": "eval_...",
  "evidence_paths": ["docs/reports/generation-citation-report.md"],
  "status": "locally verified"
}
```

A requirement is incomplete when code exists but its negative tests or evidence are missing.

## Part 26 - Final reviewer proof

A reviewer should be able to run:

```powershell
git clone $env:ENTERPRISE_RAG_REPOSITORY_URL
cd enterprise-rag-knowledge-assistant
copy .env.example .env
docker compose up --build -d
uv run alembic upgrade head
uv run python scripts/seed_demo.py
uv run pytest
uv run python -m enterprise_rag_evals.runner retrieval --dataset business --compare all
uv run python -m enterprise_rag_evals.runner answers --dataset business --provider mock
uv run python -m enterprise_rag_evals.runner safety --dataset all
powershell -File scripts/smoke.ps1
```

Then, using two synthetic tenants and at least three identities, the reviewer should:

1. Open API docs and the web UI.
2. Upload a text PDF, a scanned page, a table document, and an update.
3. Inspect immutable source/version, parser warnings, chunks, index job, and active version.
4. Search an exact identifier that favors lexical retrieval.
5. Search a paraphrase that favors dense retrieval.
6. Compare lexical, dense, hybrid, and reranked results.
7. Ask an answerable question and resolve every claim citation to exact source version/span.
8. Ask an unanswerable and a conflicting-evidence question and see controlled behavior.
9. Prove a restricted document is absent for an unauthorized user at candidate, context, answer,
   citation, cache, and MCP layers.
10. Revoke access and prove the next query and old citation preview deny access.
11. Upload a new version and prove atomic activation keeps the old version until the new one passes.
12. Delete the document and measure visibility and physical propagation.
13. Inject malicious instructions into an authorized document and prove they remain inert data.
14. Crash/retry a worker job, inspect the DLQ, and run reconciliation.
15. Submit wrong-rank/wrong-citation feedback and show its controlled route to an eval candidate.
16. Follow one upload and answer trace and find the full version tuple, latency, and cost.
17. Inspect eval reports, threat model, system/dataset cards, dashboards, stage evidence, and open
    `not verified` claims.
18. Exercise a feature/index rollback and review a recorded backup/restore drill.

The final proof package contains:

- README with architecture, setup, demo, security boundary, and limitations.
- Architecture/data/API/ingestion/retrieval/ACL contracts and ADRs.
- Source register, product requirements, system card, and dataset card.
- Chunking, ingestion, retrieval, answer/citation, safety, BEIR, freshness/delete, cost, and pilot
  reports.
- Threat model and security test report.
- SLO, incident, rollback, reindex, and backup/restore runbooks.
- Dashboard exports and representative trace.
- Learning notes, progress log, and 22 stage snapshots with honest evidence status.

## Part 27 - Curriculum mapping

| Lesson | How this project uses it | Parts |
|---|---|---|
| 01 - Learning Environment | reproducible Python, lockfile, Compose, stage evidence | 1, 20-21 |
| 02 - Python for Production AI | typed packages, protocols, validation, errors | all implementation Parts |
| 03 - Async and Concurrent AI Services | RQ jobs, outbox, leases, retry, DLQ, backpressure | 13, 18 |
| 04 - Testing and Code Quality | unit/integration/property/security/e2e tests and CI | all, especially 16-20 |
| 05 - API and Backend Engineering | FastAPI contracts, identity, idempotency, pagination | 2, 4-5, 14 |
| 06 - SQL, Data Modeling, and Storage | Postgres, pgvector, FTS, object storage, migrations | 3, 5, 8-10 |
| 07 - Applied AI Problem Discovery | personas, workflow, baseline, pilot metrics | 0, 22 |
| 08 - Foundation Models | model limits, tokens, uncertainty, local encoders | 8, 11-12 |
| 09 - Model API Integration | provider-neutral generation, retries, cost | 12, 18 |
| 10 - Prompt and Context Engineering | evidence boundary, context budget, versioned prompt | 11-12 |
| 11 - Applied LLM Product | complete employee assistant and feedback UX | 12, 14-15 |
| 12 - Embeddings and Semantic Retrieval | dense/lexical/hybrid, metadata filters, reranking, BEIR | 7-11, 16 |
| 13 - Document Ingestion and Chunking | formats, OCR, tables, dedupe, provenance, versions | 5-7, 13 |
| 14 - Production RAG | evidence, citations, abstention, ACLs, freshness, evaluation | 9-18 |
| 15 - AI Evaluation Engineering | layer metrics, datasets, reports, release gates | 16 |
| 16 - AI Data Engineering | source register, dataset lineage, feedback curation | 5-7, 16, 22 |
| 17 - Tool Calling and Controlled Workflows | explicit state machines; no model writes | 13-14 |
| 18 - MCP and Agent Integration | secure read-only MCP after API proof | 19 |
| 19 - PyTorch and Training Fundamentals | sentence-transformer runtime awareness only | optional study |
| 20 - Tokenizers and Training Data | chunk/context token budgets; no training corpus | 7, 11 |
| 21 - Supervised Fine-Tuning | not required; RAG is tested first | out of scope |
| 22 - LoRA and QLoRA | not required | out of scope |
| 23 - Preference Data and DPO | feedback is not automatically preference data | future option |
| 24 - Advanced Post-Training Decisions | eval may conclude retrieval is the right intervention | future decision |
| 25 - Distributed Training | not used | out of scope |
| 26 - Multimodal and Document AI | OCR and tables; no multimodal generation | 6 |
| 27 - Speech, Audio, and Voice AI | not used | out of scope |
| 28 - AI Security and Privacy | ACLs, injection/poisoning, PII, secrets, audit | 4, 10, 17, 19 |
| 29 - Responsible AI and Governance | source approval, system/dataset cards, human-use limits | 17, 22 |
| 30 - Production Architecture and Reliability | queues, idempotency, caching, DLQ, DR | 13, 18, 21 |
| 31 - Observability, Feedback, and Cost | traces, dashboards, feedback, version/cost tuple | 15, 18, 22 |
| 32 - Cloud Deployment and Infrastructure | staging, private dependencies, secrets, backup | 21 |
| 33 - Kubernetes for AI Workloads | not required for this version | future scale option |
| 34 - LLMOps and MLOps | artifact/index/prompt versions, gates, promotion, rollback | 16, 20-22 |
| 35 - Open-Model Serving | local embedding/reranker loading only | 8, 11 |
| 36 - Inference Optimization | batch embeddings, ANN/rerank/context/latency tuning | 8, 11, 18 |
| 37 - Classical ML Foundations | IR metrics and experiment design, not predictive ML | 7, 16 |
| 38 - Production ML | model artifact/version/monitoring patterns | 8, 11, 18 |
| 39 - Deep Learning | encoder/cross-encoder conceptual awareness | 8, 11 |
| 40 - Enterprise Applied AI Capstone | reusable production RAG anchor project | whole project |
| 41 - Applied AI Engineer Specialization | directly supported | whole project |
| 42 - Generative AI Engineer Specialization | ingestion, retrieval, generation, evaluation | 5-18 |
| 43 - LLM Engineer Specialization | partial; no training/adaptation | 11-12, 16 |
| 44 - MLOps and ML Platform Specialization | pipelines, registry-like lineage, CI, deployment | 13, 18, 20-21 |
| 45 - AI Evaluation and Safety Specialization | layered evals, red team, gate calibration | 16-17 |
| 46 - AI Security Specialization | tenant/ACL, injection/poisoning, secure MCP | 4, 10, 17, 19 |
| 47 - Machine Learning Engineer Specialization | partial through retrieval experiments | 7-11, 16 |
| 48 - AI Infrastructure and Inference Specialization | local model runtime, telemetry, capacity | 8, 11, 18, 21 |
| 49 - Search and Recommendation Specialization | strongest direct support | 7-11, 16 |
| 50 - Multimodal AI Specialization | limited OCR/table/document foundation | 6 |
| 51 - Forward-Deployed AI Engineer | source onboarding, customer ACLs, pilot and handoff | 4-7, 21-22 |
| 52 - Coding and Python Interviews | protocols, services, state machines, tests | whole codebase |
| 53 - SQL Interviews | schema, FTS/vector queries, ACL joins, plans | 3, 9-10 |
| 54 - Applied AI Case Interviews | scope, build-vs-buy, metrics, rollout | 0, 16, 22 |
| 55 - LLM and Model Interviews | embeddings, reranking, context, generation, evaluation | 8, 11-12, 16 |
| 56 - AI System Design Interviews | full architecture, reliability, security, DR | whole project |
| 57 - Portfolio Deep-Dive Interviews | evidence, failures, metrics, cost, decisions | 23-30 |

The core lesson claim for this project is Lessons 12-14. The broader mappings are supporting
engineering evidence, not claims that one repository replaces each full lesson.

## Part 28 - Suggested beginner weekly plan

This 22-week plan assumes the learner is studying while building. Compress code scope before
cutting permission, evaluation, deletion, security, or evidence work.

| Week | Build target | Learning focus | Required proof |
|---:|---|---|---|
| 1 | Repo, Python packages, quality commands | uv, modules, pytest, Ruff, mypy | clean install and tests |
| 2 | Compose and health/readiness API | containers, config, HTTP | dependency failure tests |
| 3 | Core schema and migrations | SQL, indexes, transactions | fresh/upgrade migration |
| 4 | Identity, groups, roles, ACL truth table | authn vs authz | cross-tenant property tests |
| 5 | MinIO upload and document versions | object storage, hashes, idempotency | immutable object round trip |
| 6 | Text/HTML/DOCX/email parsing | adapters and typed IR | golden parser fixtures |
| 7 | PDF OCR and tables | page layout, OCR limits, cells | locator round trip |
| 8 | Chunkers and experiment | tokens, structure, relevance | chunking report |
| 9 | Embedding interface and pgvector | vectors, cosine, ANN | dense baseline |
| 10 | PostgreSQL FTS | lexical retrieval and query plans | lexical baseline |
| 11 | RRF hybrid and ACL filters | fusion and pre-filtering | hybrid metrics + zero leak |
| 12 | Reranker and evidence packets | cross-encoders, context budgets | ablation and packet tests |
| 13 | Generation, citations, abstention | structured outputs, grounding | answered/abstained proof |
| 14 | RQ lifecycle, update/delete | at-least-once, outbox, state | crash/retry/delete report |
| 15 | APIs and React UI | contracts, product states, accessibility | e2e user workflow |
| 16 | Retrieval evaluation and BEIR | Recall/MRR/nDCG, benchmarks | retrieval/BEIR reports |
| 17 | Answer/citation/safety evaluation | rubrics, abstention, adversarial sets | gate reports |
| 18 | Security hardening | injection, poisoning, parser/UI abuse | threat model and green suite |
| 19 | Telemetry, cache, cost, reliability | traces, SLOs, degraded modes | trace/dashboard/failure proof |
| 20 | Read-only MCP and CI | controlled tools and delivery gates | parity/security/blocked-CI proof |
| 21 | Staging, rollback, backup/restore | deployment and DR | drills and honest evidence |
| 22 | Pilot package and interview defense | business decision and storytelling | pilot report and demo |

At every week, add one learning-note paragraph:

- What does this technology do?
- Why does this project need it?
- What failed?
- What evidence proves the fix?
- What remains unverified?

## Part 29 - First practical assignment

Before embedding or generation work:

1. Create `enterprise-rag-knowledge-assistant`.
2. Configure Python 3.12, `uv`, Ruff, mypy, and pytest.
3. Start PostgreSQL/pgvector, Redis, and MinIO through Compose.
4. Implement `/health` and dependency-aware `/ready`.
5. Create tenants, subjects, groups, documents, versions, ACL revisions/entries, and raw-object
   tables.
6. Apply the first migration to an empty database.
7. Implement local trusted identity headers guarded by `APP_ENV=local`.
8. Implement a deny-by-default ACL truth table and two-tenant tests.
9. Implement an authorized TXT upload to immutable MinIO object storage.
10. Store SHA-256, media type, size, object version, document version, uploader, and initial ACL.
11. Retry with the same idempotency key and prove no duplicate object/version/job exists.
12. Write:
    - `docs/architecture.md`
    - `docs/data-model.md`
    - `docs/acl-model.md`
    - `docs/ingestion-contract.md`
    - `docs/learning-notes.md`
    - `docs/progress-log.md`
    - stage snapshots 01-05 with honest evidence levels

Verification:

```powershell
docker compose up -d postgres redis minio
uv run alembic upgrade head
uv run ruff check .
uv run mypy apps packages
uv run pytest tests/api tests/db tests/domain tests/security/test_tenant_acl.py
```

After this assignment, the project has a secure data foundation. Only then add parsing, chunks,
embeddings, retrieval, reranking, and generation.

## Part 30 - Final definition of done and interview defense

The project is complete for portfolio purposes only when:

- A fresh clone starts and the reviewer proof works on synthetic/approved data.
- Production requirements map to implementation, negative tests, telemetry, and evidence.
- Unauthorized content is absent before ranking/context and from every downstream surface.
- Sources, versions, parser/chunker/index/model/prompt lineage and exact citations are verifiable.
- Lexical, dense, hybrid, and reranked retrieval have comparable labeled metrics.
- Ingestion, retrieval, answer/citation, permission, safety, freshness/delete, latency, and cost
  reports are separate and reproducible.
- Unanswerable/conflicting/stale/unsafe cases abstain or clarify at calibrated rates.
- Update, ACL revocation, delete, retry, DLQ, reconciliation, cache, rollback, and restore behavior
  has recorded evidence.
- The UI communicates evidence, versions, uncertainty, degraded states, and feedback clearly.
- MCP, if enabled, is read-only, bounded, authenticated, audited, and parity-tested.
- CI protects code, schema, artifacts, security, and eval gates.
- Stage snapshots distinguish planned, implemented, locally verified, externally verified, and
  operationally proven facts.
- The pilot or simulated pilot concludes expand, iterate, rollback, or stop with evidence.

Be ready to answer:

- Why is PostgreSQL FTS plus pgvector the default, and what evidence would justify OpenSearch?
- Which failures came from parsing, chunking, retrieval, reranking, context, generation, or citation?
- How did you label relevance and prevent eval leakage?
- Why did the selected chunker win?
- How do ACLs enter lexical and ANN candidate queries before top-k?
- What happens to cached results after group, ACL, active-version, or delete changes?
- How do you prove a citation points to the exact authorized version and span?
- What triggers abstention, and what is the false-refusal tradeoff?
- How do updates activate atomically and deletes propagate under at-least-once delivery?
- What happens when Redis, reranker, generation provider, object storage, or PostgreSQL fails?
- How do you prevent indirect prompt injection and corpus poisoning?
- What data goes to the hosted provider, and how is it retained?
- What did BEIR tell you, and what did it not tell you about enterprise queries?
- What are P95 latency, freshness, delete lag, and cost per useful answer?
- Which requirement remains only locally verified, and what would external proof require?
- What would you rollback first after a quality regression: index, chunker, retriever, reranker,
  prompt/model route, application, or feature?
- What is the most important failure you found, and which permanent eval case now catches it?

If the system can produce a polished answer but cannot prove authorization, provenance, retrieval
quality, citation validity, freshness, safe failure, cost, and rollback, it is still a RAG demo.
