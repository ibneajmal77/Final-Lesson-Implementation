# Recommendation and Search Stack Technical Implementation Guide

Project codename: `ListingMatch`

This guide turns the production plan into an executable build sequence for a recommendation, search, and ranking system. The target system supports catalogue ingestion, interaction events, lexical search, dense retrieval, hybrid retrieval, collaborative filtering, content-based recommendation, near-duplicate detection, ranking, reranking, offline evaluation, online-style experiment analysis, low-latency serving, observability, and rollback.

## How to use this guide

Build the project in stages:

1. Data contracts and snapshots.
2. Baselines.
3. Candidate generation.
4. Ranking features and models.
5. Evaluation gates.
6. Serving APIs.
7. Experiment readouts.
8. Observability, bias monitoring, and rollback.

Do not start with a neural ranker. Start with measurable baselines and labelled evaluation sets. A reviewer should be able to see where relevance improved, where it regressed, and what operational trade-offs were accepted.

## 0. Scope, non-goals, and prerequisites

### In scope

The implementation must include:

- Catalogue ingestion.
- Interaction-event ingestion.
- Dataset snapshots and time-based splits.
- Relevance label set for search.
- Duplicate and similar-item labels.
- Popularity baseline.
- BM25 search baseline.
- Dense embedding retrieval.
- Hybrid retrieval.
- Collaborative-filtering baseline.
- Content-based recommendation.
- Candidate generation service.
- Candidate merge and deduplication.
- Ranking feature pipeline.
- Ranker or reranker.
- Offline evaluation harness.
- Online-style experiment memo.
- Search API.
- Recommendation API.
- Similar-item API.
- Event ingestion API.
- Ranking trace API.
- Release gate and rollback records.
- Observability and latency report.

### Non-goals for the first production-style version

Do not build:

- Real marketplace checkout.
- Ad auction infrastructure.
- Full real-time feature store.
- Reinforcement-learning recommender.
- Full-scale distributed ANN service.
- Real user A/B test unless actual randomized traffic exists.
- Multimodal image matching unless selected as an explicit extension.
- Sensitive-attribute personalization.

### Local prerequisites

Use a pinned stack:

- Python 3.11 or 3.12.
- FastAPI.
- Pydantic.
- SQLAlchemy or SQLModel.
- Alembic.
- PostgreSQL.
- Redis.
- OpenSearch or Elasticsearch, or local BM25 substitute for minimal path.
- FAISS for dense retrieval.
- sentence-transformers.
- scikit-learn.
- LightGBM, XGBoost, or CatBoost.
- PyTorch or Transformers for optional deep model.
- MLflow.
- Polars or pandas.
- OpenTelemetry.
- Prometheus.
- Docker and Docker Compose.

Optional:

- ONNX Runtime.
- Optuna.
- Evidently or custom drift checks.
- Grafana.
- k6, Locust, or a simple load-test runner.

### Pre-build discovery gate

Create:

- `docs/problem-statement.md`
- `docs/product-requirements.md`
- `docs/metric-tree.md`
- `docs/experiment-design.md`
- `docs/ranking-policy.md`
- `docs/feedback-policy.md`
- `docs/evidence-package.md`

Answer:

- Which item domain is used?
- Which interaction dataset is used?
- Which user journeys are in scope?
- Which metrics decide launch?
- Which metrics are guardrails?
- Which splits prevent leakage?
- Which candidate sources are required?
- Which fallback behavior is expected?
- Which online metrics are simulated versus real?

### Canonical executable stack

Use this repository shape:

- `apps/api`: FastAPI service for search, recommendations, events, traces, admin release APIs.
- `apps/worker`: background jobs for ingestion, indexing, evaluations, reports, and releases.
- `packages/listingmatch-contracts`: Pydantic contracts.
- `packages/listingmatch-db`: database models, migrations, repositories.
- `packages/listingmatch-ingestion`: catalogue and interaction loaders.
- `packages/listingmatch-retrieval`: BM25, dense, hybrid, ANN, merge, deduplication.
- `packages/listingmatch-recs`: popularity, collaborative filtering, content-based, similar-item.
- `packages/listingmatch-ranking`: features, ranker, reranker, ranking policy.
- `packages/listingmatch-evals`: retrieval, recommendation, ranking, duplicate, latency, and experiment evaluation.
- `packages/listingmatch-observability`: traces, metrics, redaction, cost.
- `infra`: Docker Compose, OpenSearch, Prometheus, Grafana, deployment assets.
- `docs`: living docs and runbooks.
- `reports`: generated evidence.

## 1. Final system and invariants

### Final system

Runtime components:

- API service.
- Worker.
- PostgreSQL.
- Redis.
- Search backend.
- FAISS or ANN index.
- Model artifact store.
- MLflow.
- Prometheus and optional Grafana.

Offline components:

- Ingestion jobs.
- Index builders.
- Feature builders.
- Training jobs.
- Evaluation jobs.
- Experiment readout generator.

### Core invariants

Data invariants:

- Every item has a stable `item_id`.
- Every interaction has event time, event type, user or anonymous profile, item, and source.
- Every dataset snapshot is immutable.
- Every evaluation references a snapshot, label set, index version, feature version, and model version.
- Time-based splits use event time, not ingestion time.

Retrieval invariants:

- Candidate generation is measured separately from reranking.
- Candidate source and score are retained in trace.
- Filtered or restricted items cannot reach reranking.
- Dense index version and embedding model version are recorded together.
- Hybrid scoring policy is versioned.

Recommendation invariants:

- Cold-start user and cold-start item paths are explicit.
- Popularity baseline is always available as fallback.
- Feedback events are not treated as unbiased labels without policy.
- Recommendations record candidate source and policy version.

Ranking invariants:

- Ranker features must be available at serving time.
- Feature missingness is measured.
- Ranker and feature versions are recorded in every served trace.
- Business boosts and diversity constraints are policy-controlled.
- A release cannot promote if restricted-item leakage is nonzero.

Experiment invariants:

- Online-style metrics must state whether they are real, simulated, replayed, or interleaved.
- Experiment unit must be documented.
- Variant assignment must be stable for the declared unit.
- Launch recommendation must include guardrails and caveats.

## 2. Starter quality gates

Search gates:

- BM25 baseline is implemented.
- Dense baseline is implemented.
- Hybrid retrieval is compared against BM25 and dense.
- Candidate recall at K does not regress against current route.
- NDCG at K does not regress beyond tolerance.
- MRR does not regress beyond tolerance.
- Filter correctness passes.
- Zero restricted items leak.

Recommendation gates:

- Popularity baseline is implemented.
- Collaborative filtering baseline is implemented.
- Content-based baseline is implemented.
- Hit rate or recall at K does not regress.
- NDCG at K does not regress.
- Coverage and diversity stay above thresholds.
- Cold-start fallback passes minimum quality.
- Popularity concentration does not exceed threshold unless approved.

Ranking gates:

- Feature consistency tests pass.
- Ranker improves primary metric or has a documented trade-off.
- Slice regressions are below threshold.
- p95 latency stays within budget.
- Feature missingness stays within threshold.
- Model can fall back to safe route.

Experiment gates:

- Experiment memo is attached.
- Metric definitions are fixed before reading results.
- Offline and online-style results are separated.
- Caveats are explicit.
- Rollback target exists.

## 3. Build order

1. Repository and local stack.
2. Data contracts and schema.
3. Catalogue ingestion.
4. Interaction ingestion.
5. Label sets and splits.
6. BM25 baseline.
7. Dense retrieval baseline.
8. Hybrid retrieval.
9. Recommendation baselines.
10. Similar-item and duplicate detection.
11. Candidate service.
12. Feature pipeline.
13. Ranker or reranker.
14. Evaluation harness and release gates.
15. Serving APIs.
16. Experiment readout.
17. Observability and latency reports.
18. Release and rollback.
19. Final evidence package.

## 4. Beginner milestones

Milestone 1:

- Items and interactions can be loaded.
- Dataset snapshots are created.
- Time split exists.

Milestone 2:

- BM25 search returns results.
- Dense retrieval returns results.
- Evaluation report compares both.

Milestone 3:

- Popularity, collaborative, and content-based recommenders return top K.
- Recommendation metrics are computed.

Milestone 4:

- Candidate service merges and deduplicates sources.
- Similar-item endpoint works.

Milestone 5:

- Ranker scores candidates.
- Ranking trace explains the result list.

Milestone 6:

- Experiment memo and release report are generated.
- Bad candidate can be rolled back.

## 5. Target repository and artifact manifest

### Repository structure

```text
listingmatch/
  README.md
  pyproject.toml
  requirements.txt
  requirements-dev.txt
  docker-compose.yml
  .env.example
  apps/
    api/
      listingmatch_api/
        __init__.py
        main.py
        settings.py
        dependencies.py
        auth.py
        routes/
          health.py
          search.py
          recommendations.py
          similar.py
          events.py
          traces.py
          admin.py
    worker/
      listingmatch_worker/
        __init__.py
        main.py
        queues.py
        jobs/
          ingest_catalogue.py
          ingest_interactions.py
          build_indexes.py
          train_recommenders.py
          train_ranker.py
          run_evals.py
          release.py
          rollback.py
          reports.py
  packages/
    listingmatch-contracts/
      listingmatch_contracts/
        __init__.py
        items.py
        interactions.py
        labels.py
        retrieval.py
        recommendations.py
        ranking.py
        experiments.py
        releases.py
        telemetry.py
    listingmatch-db/
      listingmatch_db/
        __init__.py
        models.py
        repositories.py
        session.py
        migrations/
    listingmatch-ingestion/
      listingmatch_ingestion/
        __init__.py
        catalogue.py
        interactions.py
        normalization.py
        snapshots.py
        splits.py
    listingmatch-retrieval/
      listingmatch_retrieval/
        __init__.py
        bm25.py
        embeddings.py
        faiss_index.py
        hybrid.py
        filters.py
        merge.py
        dedupe.py
    listingmatch-recs/
      listingmatch_recs/
        __init__.py
        popularity.py
        collaborative.py
        content_based.py
        similar_items.py
        cold_start.py
    listingmatch-ranking/
      listingmatch_ranking/
        __init__.py
        features.py
        train.py
        ranker.py
        reranker.py
        policy.py
        constraints.py
        traces.py
    listingmatch-evals/
      listingmatch_evals/
        __init__.py
        retrieval.py
        recommendation.py
        ranking.py
        duplicates.py
        slices.py
        latency.py
        experiments.py
        gates.py
        reports.py
    listingmatch-observability/
      listingmatch_observability/
        __init__.py
        tracing.py
        metrics.py
        logging.py
        redaction.py
  infra/
    docker/
      Dockerfile.api
      Dockerfile.worker
    opensearch/
      opensearch.yml
    prometheus/
      prometheus.yml
    grafana/
      dashboards/
      provisioning/
  data/
    raw/
    processed/
    snapshots/
    labels/
  docs/
    problem-statement.md
    product-requirements.md
    metric-tree.md
    architecture.md
    data-model.md
    search-contract.md
    recommendation-contract.md
    ranking-policy.md
    feedback-policy.md
    evaluation-plan.md
    experiment-design.md
    security-and-governance.md
    observability-cost.md
    deployment-runbook.md
    rollback-runbook.md
    progress-log.md
  reports/
    evals/
    experiments/
    release/
    latency/
    bias/
  tests/
    api/
    db/
    ingestion/
    retrieval/
    recommendations/
    ranking/
    evals/
    release/
    security/
```

### Required artifact outputs

Generate:

- `reports/evals/retrieval-report.md`
- `reports/evals/recommendation-report.md`
- `reports/evals/ranking-report.md`
- `reports/evals/duplicate-report.md`
- `reports/experiments/experiment-readout.md`
- `reports/release/release-report.md`
- `reports/release/rollback-report.md`
- `reports/latency/latency-report.md`
- `reports/bias/feedback-bias-report.md`
- `reports/final-evidence-manifest.json`

### Required source-controlled docs

Keep updated:

- Architecture.
- Data model.
- Search contract.
- Recommendation contract.
- Ranking policy.
- Feedback policy.
- Evaluation plan.
- Experiment design.
- Security and governance.
- Observability and cost.
- Deployment runbook.
- Rollback runbook.

## 6. Data model

### Core tables

Catalogue:

- `items`
- `item_versions`
- `categories`
- `sellers`
- `item_attributes`
- `item_text`
- `item_availability`
- `item_policy_flags`

Users and sessions:

- `users`
- `anonymous_profiles`
- `sessions`
- `user_profile_features`

Interactions and labels:

- `interaction_events`
- `interaction_snapshots`
- `relevance_labels`
- `duplicate_labels`
- `label_sets`
- `split_manifests`

Indexes and features:

- `embedding_models`
- `item_embeddings`
- `bm25_indexes`
- `dense_indexes`
- `hybrid_policies`
- `feature_sets`
- `feature_snapshots`

Models and policies:

- `candidate_policies`
- `recommender_models`
- `ranker_models`
- `ranking_policies`
- `duplicate_thresholds`
- `model_artifacts`

Serving and experiments:

- `release_candidates`
- `deployments`
- `experiment_definitions`
- `experiment_assignments`
- `ranking_traces`
- `candidate_traces`
- `exposure_events`
- `release_events`
- `rollback_events`

Operations:

- `audit_events`
- `outbox_events`
- `dead_letters`
- `reconciliation_findings`

### Required constraints

- `items.item_id` is stable.
- `item_versions` cannot be mutated after snapshot creation.
- `interaction_events.occurred_at` is required.
- `split_manifests` must record split method and cutoff timestamp.
- `dense_indexes.embedding_model_id` is required.
- `ranking_policies.ranker_model_id` references a registered ranker or documented rule policy.
- `release_candidates` must reference candidate policy, index versions, feature set, ranking policy, and evaluation run.
- `deployments` must reference approved release candidates.
- `experiment_assignments` must be stable for the declared experiment unit.
- `ranking_traces` must include request ID, policy version, model version, index versions, and latency breakdown.

### Example release tuple

```json
{
  "catalogue_snapshot_id": "catalogue-20260728-001",
  "interaction_snapshot_id": "interactions-20260728-001",
  "label_set_id": "labels-search-v4",
  "embedding_model_version": "all-MiniLM-L6-v2",
  "bm25_index_version": "bm25-20260728-001",
  "dense_index_version": "dense-20260728-002",
  "candidate_policy_version": "candidate-policy-v7",
  "feature_set_version": "rank-features-v9",
  "ranker_version": "lgbm-ranker-v4",
  "ranking_policy_version": "rank-policy-v12",
  "experiment_id": "exp-search-v5",
  "service_image_digest": "sha256:...",
  "evaluation_run_id": "eval-20260728-006",
  "deployment_id": "deploy-20260728-002"
}
```

### Data invariants

- A feature snapshot cannot contain events after the split cutoff for training.
- A ranking model cannot be released if feature generation differs between training and serving.
- A dense index cannot be queried if the embedding model version is unknown.
- A recommendation result cannot include unavailable or restricted items.
- A duplicate label must distinguish `duplicate`, `near_duplicate`, `related`, `not_duplicate`, and `unsure`.
- A release cannot be approved without offline metrics and latency results.

### Outbox and reconciliation

Outbox events:

- `catalogue_ingest_requested`
- `interaction_ingest_requested`
- `label_set_validation_requested`
- `bm25_index_build_requested`
- `dense_index_build_requested`
- `recommender_training_requested`
- `ranker_training_requested`
- `evaluation_requested`
- `release_requested`
- `rollback_requested`
- `report_generation_requested`

Reconciliation checks:

- Snapshot exists but no split manifest exists.
- Index record exists but index is not queryable.
- Ranking policy references missing model.
- Release candidate approved but deployment route not updated.
- Experiment assignment exists without exposure logging.
- Interaction events are delayed beyond SLA.
- Rollback event exists without rollback report.

## 7. API contracts

### Search request

```json
{
  "query": "noise cancelling headphones",
  "user_id": "user_123",
  "session_id": "session_abc",
  "filters": {
    "category": "electronics.audio.headphones",
    "price_max": 150,
    "availability": "in_stock"
  },
  "limit": 20,
  "debug": false
}
```

### Search response

```json
{
  "request_id": "req_01J5...",
  "results": [
    {
      "item_id": "item_000123",
      "rank": 1,
      "score": 0.923,
      "title": "Wireless Noise Cancelling Headphones",
      "price": 89.99
    }
  ],
  "ranking_policy_version": "rank-policy-v12",
  "latency_ms": 91
}
```

### Recommendation request

```json
{
  "user_id": "user_123",
  "session_id": "session_abc",
  "context": {
    "page": "home",
    "category": null
  },
  "limit": 20,
  "debug": false
}
```

### Similar-item request

```json
{
  "item_id": "item_000123",
  "mode": "similar",
  "limit": 20,
  "include_duplicate_candidates": true
}
```

### Event ingestion request

```json
{
  "event_id": "evt_01J5...",
  "user_id": "user_123",
  "session_id": "session_abc",
  "item_id": "item_000123",
  "event_type": "click",
  "request_id": "req_01J5...",
  "position": 3,
  "occurred_at": "2026-07-28T10:03:00Z"
}
```

### Ranking trace response

```json
{
  "request_id": "req_01J5...",
  "candidate_sources": [
    {"source": "bm25", "count": 100, "latency_ms": 18},
    {"source": "dense", "count": 100, "latency_ms": 24},
    {"source": "collaborative", "count": 50, "latency_ms": 8}
  ],
  "feature_set_version": "rank-features-v9",
  "ranker_version": "lgbm-ranker-v4",
  "ranking_policy_version": "rank-policy-v12",
  "index_versions": {
    "bm25": "bm25-20260728-001",
    "dense": "dense-20260728-002"
  },
  "latency_ms": {
    "candidate_generation": 52,
    "feature_lookup": 16,
    "reranking": 11,
    "total": 91
  }
}
```

### Minimum API surface

Application APIs:

- `GET /search`
- `GET /recommendations/home`
- `GET /recommendations/item/{item_id}/similar`
- `POST /events`
- `GET /items/{item_id}`
- `GET /healthz`
- `GET /readyz`
- `GET /metrics`

Admin APIs:

- `POST /admin/ingest/catalogue`
- `POST /admin/ingest/interactions`
- `POST /admin/labels`
- `POST /admin/indexes/build`
- `POST /admin/models/train-ranker`
- `POST /admin/evals/run`
- `POST /admin/releases`
- `POST /admin/releases/{id}/approve`
- `POST /admin/releases/{id}/canary`
- `POST /admin/releases/{id}/rollback`
- `GET /admin/traces/{request_id}`
- `GET /admin/experiments/{experiment_id}/readout`

### Capability-aware readiness

Readiness should report:

```json
{
  "status": "ready",
  "capabilities": {
    "database": "ready",
    "redis": "ready",
    "bm25_index": "ready",
    "dense_index": "ready",
    "ranker": "ready",
    "event_ingestion": "ready",
    "experiment_assignment": "ready",
    "metrics": "ready"
  }
}
```

Search should degrade to BM25 if dense retrieval is unavailable and the policy allows it.

## 8. Stage 1 - Reproducible repository and dependencies

### Objective

Create a local project that can run consistently.

### Implement

- Repository skeleton.
- Dependency files.
- Docker Compose with PostgreSQL, Redis, OpenSearch or substitute, Prometheus, and optional Grafana.
- `.env.example`.
- Health and readiness routes.
- Test command.
- README with local setup.

### Tests and commands

Provide:

```powershell
python -m pytest
python -m mypy packages apps
docker compose config
docker compose up
```

### Done when

- Services boot locally.
- Health checks pass.
- Tests run.
- No secrets are committed.

## 9. Stage 2 - Data contracts, schema, and migrations

### Objective

Create durable contracts for items, interactions, labels, snapshots, indexes, models, traces, and releases.

### Implement

- Pydantic contracts.
- Database models.
- Alembic migrations.
- Seed data for a small catalogue and sample users.
- Snapshot tables.
- Release tables.
- Trace tables.
- Tests for constraints.

### Done when

- Empty database migrates cleanly.
- Seed data is deterministic.
- Snapshot immutability is tested.
- Release tuple can be stored.

## 10. Stage 3 - Catalogue ingestion and normalization

### Objective

Load item data into a stable searchable catalogue.

### Implement

- Catalogue loader.
- Text normalization.
- Category normalization.
- Attribute normalization.
- Availability and policy flags.
- Item versioning.
- Catalogue snapshot generator.
- Dataset card.

### Done when

- Catalogue loads from raw file.
- Items have stable IDs.
- Empty, duplicate, and malformed records are handled.
- Snapshot ID is generated.
- Dataset card is updated.

## 11. Stage 4 - Interaction ingestion, splits, and leakage checks

### Objective

Create valid recommendation data and prevent future leakage.

### Implement

- Interaction loader.
- Event validation.
- Session and user profile records.
- Time-based split generator.
- Negative sampling policy if needed.
- Leakage checks.
- Interaction-event card.
- Feedback policy.

### Done when

- Interaction events load.
- Split manifest records cutoff timestamps.
- Seeded future leakage fails validation.
- Cold-start user and item slices are identified.
- Feedback caveats are documented.

## 12. Stage 5 - Search relevance labels and duplicate labels

### Objective

Create evaluation labels for search and similar-listing quality.

### Implement

- Query set.
- Relevance label schema.
- Label import.
- Duplicate label schema.
- Duplicate review categories.
- Label validation.
- Labeling guide.

### Done when

- At least 50 labelled queries exist for the portfolio path.
- Duplicate labels include positive and negative examples.
- Label distribution is reported.
- Label set version is immutable.

## 13. Stage 6 - BM25 lexical search baseline

### Objective

Build a simple and strong lexical search baseline.

### Implement

- BM25 index build.
- Query parser.
- Metadata filters.
- Result scoring.
- Search endpoint using BM25.
- Index version record.
- Latency measurement.

### Done when

- BM25 returns relevant results for sample queries.
- Filters are applied before response.
- Evaluation computes recall, precision, MRR, and NDCG.
- Query latency is recorded.

## 14. Stage 7 - Dense retrieval and ANN index

### Objective

Add semantic retrieval without assuming it wins.

### Implement

- Embedding model selection.
- Item text assembly.
- Embedding generation.
- FAISS or vector index build.
- Dense search endpoint or internal candidate source.
- Embedding model version.
- Dense index version.
- Latency measurement.

### Done when

- Dense retrieval returns candidates.
- Embedding and index versions are recorded.
- Dense is evaluated against the same labelled queries as BM25.
- Failure cases are documented.

## 15. Stage 8 - Hybrid retrieval and score fusion

### Objective

Combine lexical and dense retrieval with measurable rules.

### Implement

- Score normalization.
- Weighted fusion or reciprocal rank fusion.
- Candidate merge.
- Deduplication.
- Filter preservation.
- Hybrid policy version.
- Hybrid evaluation.

### Done when

- Hybrid retrieval compares against BM25 and dense.
- Merge and dedupe behavior is tested.
- Candidate recall is measured.
- Hybrid policy can be rolled back.

## 16. Stage 9 - Recommendation baselines

### Objective

Build recommender baselines before complex ranking.

### Implement

- Popularity recommender.
- Collaborative-filtering recommender.
- Content-based recommender.
- Similar-item recommender.
- Cold-start fallback.
- Recommendation metrics.
- MovieLens-style evaluation path.

### Done when

- Each baseline returns top K.
- Hit rate, recall, precision, NDCG, MAP, coverage, diversity, and novelty are computed.
- Cold-start cases have defined behavior.
- Popularity bias is measured.

## 17. Stage 10 - Candidate generation service

### Objective

Create a service layer that produces broad candidate sets for ranking.

### Implement

- Candidate source interface.
- BM25 candidate source.
- Dense candidate source.
- Hybrid candidate source.
- Popularity candidate source.
- Collaborative candidate source.
- Content-based candidate source.
- Source quotas.
- Merge and deduplication.
- Candidate trace.

### Done when

- Candidate service returns a merged candidate set.
- Source contribution is visible.
- Candidate recall is measured.
- Candidate latency is measured.
- Restricted and unavailable items are filtered before ranking.

## 18. Stage 11 - Similar-item and duplicate matching

### Objective

Support `ListingMatch` near-duplicate and semantic matching workflow.

### Implement

- Similar-item endpoint.
- Text similarity features.
- Attribute similarity features.
- Embedding similarity.
- Duplicate threshold policy.
- Review labels.
- Duplicate evaluation.
- Side-by-side debug data.

### Done when

- Similar-item endpoint works.
- Duplicate precision and recall are reported.
- Threshold decision is documented.
- False positives and false negatives are sampled.

## 19. Stage 12 - Ranking features and serving consistency

### Objective

Build ranking features that are available at training and serving time.

### Implement

- Feature definitions.
- Query-item features.
- User-item features.
- Item popularity features.
- Freshness features.
- Price/category/seller features.
- Candidate-source features.
- Feature snapshot.
- Training-serving consistency tests.
- Feature missingness metrics.

### Done when

- Feature set version is recorded.
- Training and serving feature functions match.
- Missing features have fallback behavior.
- Future-only features fail leakage tests.

## 20. Stage 13 - Ranker and reranker

### Objective

Improve ranking quality on bounded candidate sets.

### Implement

- Baseline rule ranker.
- LightGBM, XGBoost, CatBoost, or neural ranker.
- Optional cross-encoder reranker for search.
- Model training script.
- MLflow tracking.
- Model artifact export.
- Optional ONNX export.
- Ranking policy.
- Constraint and diversity post-processing.

### Done when

- Ranker can score candidates.
- Ranker version is registered.
- Ranker is evaluated against baseline.
- Reranker latency is measured.
- Ranking trace includes feature and model versions.

## 21. Stage 14 - Evaluation harness and release gates

### Objective

Make release decisions evidence-based.

### Implement

- Retrieval metrics.
- Recommendation metrics.
- Ranking metrics.
- Duplicate metrics.
- Slice evaluation.
- Latency evaluation.
- Guardrail gates.
- Release report generator.
- Gate comparator.
- Baseline comparison.

### Done when

- A good candidate passes gates.
- A bad candidate fails gates.
- Candidate compares to current deployment and simple baselines.
- Report includes metric deltas and caveats.
- Release cannot approve without required reports.

## 22. Stage 15 - Serving APIs and ranking traces

### Objective

Expose product-facing and reviewer-facing APIs.

### Implement

- Search API.
- Recommendation API.
- Similar-item API.
- Event ingestion API.
- Trace lookup API.
- Readiness route.
- Metrics route.
- Request ID middleware.
- Cache policy.
- Timeout and fallback behavior.

### Done when

- APIs return expected schemas.
- Every result list has a trace.
- Search can degrade to BM25.
- Recommendation can degrade to popularity.
- Event ingestion records exposures and interactions.
- p95 latency is measured.

## 23. Stage 16 - Online-style experiment readout

### Objective

Practice launch decisions without overstating evidence.

### Implement

- Experiment definition.
- Variant assignment.
- Exposure logging.
- Offline result comparison.
- Replay or simulation analysis.
- Guardrail metrics.
- Segment analysis.
- Power or uncertainty note.
- Experiment memo generator.

### Done when

- Experiment unit is documented.
- Variants are stable for the unit.
- Memo clearly separates offline, replay, simulation, and real online evidence.
- Launch recommendation is explicit.

## 24. Stage 17 - Feedback bias, exposure, and drift monitoring

### Objective

Monitor the failure modes that recommender systems often hide.

### Implement

- Event ingestion lag metric.
- Exposure distribution.
- Popularity concentration.
- Position-bias report.
- Cold-start report.
- Feature drift.
- Query drift.
- Item catalogue freshness.
- Label delay report.
- Feedback-bias report.

### Done when

- Feedback-bias report is generated.
- Exposure concentration is visible.
- Cold-start quality is tracked.
- Drift checks can alert or block retraining.
- Delayed labels are documented.

## 25. Stage 18 - Observability, latency, and cost

### Objective

Make ranking requests operable.

### Implement

- OpenTelemetry spans.
- Prometheus metrics.
- Structured logs.
- Redaction.
- Latency breakdown.
- Candidate source timing.
- Feature timing.
- Reranker timing.
- Cost estimate.
- Dashboards.

### Done when

- One request is traceable end to end.
- Latency report breaks down candidate, feature, rerank, and total time.
- Cost report estimates index build, storage, and serving cost.
- Sensitive event data is redacted from logs.

## 26. Stage 19 - Release, canary, and rollback

### Objective

Prove the stack can recover from bad relevance or bad latency releases.

### Implement

- Release candidate table.
- Approval policy.
- Deployment route.
- Canary or shadow mode.
- Rollback endpoint.
- Rollback for index, model, feature, ranking policy, and service image.
- Smoke tests.
- Rollback report.

### Done when

- Release cannot approve without gates.
- Canary candidate can receive a bounded traffic slice or simulated slice.
- Bad candidate rolls back.
- Route points to previous release tuple.
- Smoke tests pass after rollback.
- Rollback report is generated.

## 27. Stage 20 - Security and governance tests

### Objective

Prevent ranking from exposing invalid or restricted items.

### Implement

- Restricted-item filter tests.
- Unavailable-item filter tests.
- Debug trace authorization tests.
- Event validation tests.
- PII minimization checks.
- Ranking-policy audit tests.
- Release approval tests.
- Rollback authorization tests.

### Done when

- Restricted items never appear in final results.
- Unavailable items are filtered.
- Debug traces require operator access.
- Event payloads reject invalid fields.
- Release and rollback actions are audited.

## 28. Documentation governance and stage records

### Stage record format

Each stage should create or update:

```markdown
# Stage NN - Name

## Objective

## Implemented

## Tests

## Evidence

## Open risks

## Next step
```

### Canonical stage IDs

Use:

- `LM-01-repo`
- `LM-02-schema`
- `LM-03-catalogue`
- `LM-04-interactions`
- `LM-05-labels`
- `LM-06-bm25`
- `LM-07-dense`
- `LM-08-hybrid`
- `LM-09-recs-baselines`
- `LM-10-candidates`
- `LM-11-duplicates`
- `LM-12-features`
- `LM-13-ranker`
- `LM-14-evals-gates`
- `LM-15-serving`
- `LM-16-experiment`
- `LM-17-feedback-bias`
- `LM-18-observability`
- `LM-19-release-rollback`
- `LM-20-security`

### Documentation checks

Before final review:

- Every stage has a record.
- Every metric has a definition.
- Every release has a tuple.
- Every report references source snapshots.
- Every online claim is labelled as real, replayed, or simulated.
- Every ranking policy is versioned.

## 29. Minimal and full build paths

### Smallest complete portfolio build

The smallest complete build may use:

- Local catalogue file.
- MovieLens small dataset.
- Local BM25 implementation.
- FAISS.
- scikit-learn nearest-neighbour or matrix-factorization substitute.
- LightGBM or rule ranker.
- Simulated online-style experiment.
- Docker Compose.

It must still include:

- Search labels.
- Duplicate labels.
- Time-based splits.
- Baseline comparisons.
- Candidate recall.
- Ranking traces.
- Release gates.
- Rollback.
- Experiment memo.

### Full production-style path

The full path adds:

- OpenSearch or Elasticsearch.
- Larger MovieLens or public catalogue dataset.
- ANN index publication flow.
- MLflow model registry.
- ONNX export where useful.
- Grafana dashboards.
- CI/CD release gates.
- Staging deployment and canary.
- Load test report.

## 30. Requirement traceability matrix

### Production requirement crosswalk

| Requirement | Evidence |
|---|---|
| Two-stage candidate and ranking system | Candidate service, ranker, ranking trace |
| Search stack | BM25, dense, hybrid, reranked retrieval report |
| Recommendation stack | Popularity, collaborative, content-based reports |
| MovieLens-style benchmark | Recommendation evaluation report |
| Near-duplicate listing match | Similar-item API and duplicate report |
| Offline metrics | Retrieval, recommendation, ranking reports |
| Online-style evaluation | Experiment readout |
| Low-latency serving | Latency report and API traces |
| Feedback bias controls | Feedback-bias report |
| Release and rollback | Release and rollback reports |
| Service API | Search, recommendation, similar, event, trace endpoints |

### Curriculum crosswalk

| Curriculum area | Implementation evidence |
|---|---|
| Lesson 12 embeddings and semantic retrieval | BM25, dense, hybrid, reranker, labelled query eval |
| Lesson 15 evaluation | Label sets, metrics, gates, experiment memo |
| Lesson 37 ML foundations | Splits, leakage checks, baselines, uncertainty, ranking metrics |
| Lesson 38 production ML | Feature consistency, batch/online serving, drift, rollback |
| Lesson 39 deep learning | Embeddings, optional transformer/reranker, ONNX export |
| Lesson 49 search and recommendation | Candidate generation, recommendation, learning to rank, feedback bias, online-style metrics |

### Requirement-to-evidence manifest

Create `reports/final-evidence-manifest.json`:

```json
{
  "project": "ListingMatch",
  "requirements": [
    {
      "id": "search-evaluation",
      "status": "met",
      "evidence": ["reports/evals/retrieval-report.md"]
    },
    {
      "id": "recommendation-evaluation",
      "status": "met",
      "evidence": ["reports/evals/recommendation-report.md"]
    },
    {
      "id": "online-style-experiment",
      "status": "met",
      "evidence": ["reports/experiments/experiment-readout.md"]
    }
  ]
}
```

## 31. Test strategy

### Unit tests

Cover:

- Text normalization.
- Split generation.
- Leakage checks.
- BM25 scoring wrapper.
- Dense index query wrapper.
- Hybrid score fusion.
- Candidate merge and dedupe.
- Recommendation metric functions.
- Ranking metric functions.
- Feature generation.
- Ranking policy application.
- Gate comparators.

### Integration tests

Cover:

- Catalogue ingest to snapshot.
- Interaction ingest to split.
- Label import to evaluation.
- BM25 build to search endpoint.
- Dense index build to search endpoint.
- Candidate generation to ranker.
- Recommendation endpoint to event logging.
- Similar-item endpoint to duplicate report.
- Release candidate to approval.
- Bad release to rollback.

### API tests

Cover:

- `GET /search`
- `GET /recommendations/home`
- `GET /recommendations/item/{item_id}/similar`
- `POST /events`
- `GET /admin/traces/{request_id}`
- Admin release endpoints.
- Health, readiness, and metrics.

### Evaluation tests

Cover:

- Candidate improves NDCG and passes.
- Candidate regresses NDCG and fails.
- Candidate improves NDCG but fails diversity.
- Candidate leaks restricted item and fails.
- Candidate exceeds latency budget and fails.
- Candidate lacks rollback target and fails.
- Experiment memo missing caveat and fails doc check.

### Security tests

Cover:

- Restricted items filtered.
- Unavailable items filtered.
- Debug trace access denied to non-operator.
- Invalid event payload rejected.
- PII redaction in logs.
- Release approval authorization.
- Rollback authorization.

## 32. Data and labelling plan

### Catalogue data

Required fields:

- Item ID.
- Title.
- Description.
- Category.
- Availability.
- Price or comparable structured field.

Useful fields:

- Brand.
- Seller.
- Rating.
- Image URL or image embedding.
- Creation date.
- Update date.

### Interaction data

Required events:

- View or exposure.
- Click or rating.

Useful events:

- Save.
- Add-to-cart.
- Purchase.
- Hide.
- Negative feedback.

### Search labels

Create:

- Head queries.
- Torso queries.
- Tail queries.
- Ambiguous queries.
- Filtered queries.
- Zero-result candidates.

Use a 0 to 3 relevance scale or binary labels. Document the scale.

### Duplicate labels

Create examples for:

- Exact duplicate.
- Near duplicate.
- Related but distinct.
- Same title but different item.
- Different title but same product.
- Unsure.

### Recommendation labels

Use implicit or explicit feedback:

- Ratings when available.
- Held-out positive interactions for top-K evaluation.
- Negative sampling policy for ranking where needed.
- Time-based holdout.

Document why the labels are imperfect.

## 33. Operational runbooks

### Dense index unavailable

1. Confirm dense index readiness.
2. Check index version and embedding model.
3. Route hybrid search to BM25-only fallback.
4. Verify search smoke tests.
5. Record incident note.

### Bad ranker release

1. Identify failing metric or slice.
2. Stop canary.
3. Roll back ranking policy and ranker model.
4. Run search and recommendation smoke tests.
5. Verify latency and restricted-item guardrail.
6. Generate rollback report.

### Event ingestion delay

1. Check event ingestion lag.
2. Check queue or database errors.
3. Pause retraining triggers.
4. Mark experiment readout incomplete if exposure or feedback data is missing.
5. Resume after lag returns under threshold.

### Duplicate suppression issue

1. Inspect duplicate threshold.
2. Sample false positives and false negatives.
3. Disable non-critical duplicate suppression if false positives exceed threshold.
4. Keep restricted duplicate suppression active if policy requires it.
5. Regenerate duplicate report.

### Offline and online-style mismatch

1. Compare affected segments.
2. Check feedback bias and position effects.
3. Check metric definition mismatch.
4. Hold launch if primary online-style proxy contradicts offline gain.
5. Update experiment memo.

## 34. Final reviewer proof

The reviewer should be able to run or inspect equivalent commands:

```powershell
python -m pytest
python -m mypy packages apps
docker compose config
docker compose up
```

Then verify:

- Catalogue ingest.
- Interaction ingest.
- Time-based split.
- Label import.
- BM25 index build.
- Dense index build.
- Hybrid retrieval evaluation.
- Recommendation baseline evaluation.
- Candidate generation trace.
- Ranker evaluation.
- Similar-item endpoint.
- Experiment readout.
- Release report.
- Rollback report.

Final evidence files:

- `reports/evals/retrieval-report.md`
- `reports/evals/recommendation-report.md`
- `reports/evals/ranking-report.md`
- `reports/evals/duplicate-report.md`
- `reports/experiments/experiment-readout.md`
- `reports/release/release-report.md`
- `reports/release/rollback-report.md`
- `reports/latency/latency-report.md`
- `reports/bias/feedback-bias-report.md`
- `reports/final-evidence-manifest.json`

## 35. First practical assignment

Build the first useful slice:

1. Load 1000 items.
2. Load interaction data.
3. Create time-based split.
4. Implement popularity recommender.
5. Implement BM25 search.
6. Create 20 labelled queries.
7. Compute recall, MRR, and NDCG.
8. Add `/search`.
9. Add `/recommendations/home`.
10. Log a ranking trace.

This proves the skeleton before dense retrieval, collaborative filtering, neural ranking, or deployment.

## 36. Final definition of done and interview defense

The technical build is complete when:

- Catalogue and interaction ingestion are reproducible.
- Time-based splits and leakage checks exist.
- Search labels and duplicate labels are versioned.
- BM25, dense, and hybrid retrieval are implemented and compared.
- Popularity, collaborative, and content-based recommendation baselines are implemented and compared.
- Candidate generation measures recall and latency.
- Similar-item and duplicate matching are evaluated.
- Ranker or reranker is trained or configured and compared against baselines.
- Serving APIs expose search, recommendations, similar items, events, and traces.
- Ranking traces include candidate source, feature, index, model, and policy versions.
- Offline reports and online-style experiment memo are generated.
- Feedback bias, exposure concentration, cold-start, and latency are monitored.
- Release gates block bad candidates.
- Rollback restores prior model, index, feature, or policy route.
- Final evidence manifest maps claims to reports.

For interview defense, be ready to explain:

- Why the system is two-stage.
- Why BM25, dense, hybrid, collaborative, and content-based baselines matter.
- How candidate recall differs from final ranking quality.
- How time-based splits prevent leakage.
- How feedback bias affects recommendation labels.
- Why offline metrics do not prove business lift.
- How low-latency serving constrains reranking.
- How rollback works for a bad model or index.
