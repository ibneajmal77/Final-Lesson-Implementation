# Recommendation and Search Stack Production Implementation Guide

Project codename: `ListingMatch`

Build a production-style recommendation, search, and ranking system for e-commerce listings. The system should support lexical and dense search, candidate generation, near-duplicate listing discovery, personalization, reranking, offline evaluation, online-style experiment readouts, feedback-loop monitoring, and low-latency serving.

This is not only a recommender notebook and not only a vector-search demo. It is a ranking system. The proof is that you can explain and operate the full retrieval-to-ranking lifecycle: data contracts, baselines, candidate recall, ranking quality, latency, feedback bias, experiment design, release gates, and business trade-offs.

## Source alignment

This guide is aligned to the local curriculum and roadmap documents:

- `AI-Industry-Roadmap-and-Projects.md`: `ListingMatch` e-commerce deep-learning project and search/ranking role branch.
- `deep-research-report.md`: compressed portfolio project "Recommendation and search stack" with MovieLens, BM25+dense retrieval, candidate generation, ranking model, evaluation report, service API, and experiment memo.
- `AI-Industry-Curriculum.md`: retrieval foundations, BM25, embeddings, reranking, classical ML, production ML, deep learning, search/ranking engineer, and recommender systems engineer expectations.
- `AI-Industry-Complete-Lesson-Coverage-Map.md`: Lesson 12 semantic retrieval, Lessons 37-39 ML and deep learning, and Lesson 49 search and recommendation specialization.
- `AI-Industry-Detailed-Lessons.md`: labelled search evaluation, hybrid retrieval, reranking, online experimentation, and low-latency serving outcomes.

The project should connect earlier retrieval work with later ML/deep-learning work. It should prove that the learner understands when simple lexical retrieval, matrix factorization, nearest-neighbour embeddings, boosted trees, or neural rerankers are the right tool.

## Evidence and verification vocabulary

Use these terms consistently:

- `item`: A product, movie, listing, document, or entity that can be searched or recommended.
- `query`: A user search text or structured browse request.
- `user profile`: Explicit and derived user preferences available at request time.
- `interaction event`: View, click, save, add-to-cart, purchase, rating, skip, hide, or negative signal.
- `candidate generator`: A fast method that returns a broad set of potentially relevant items.
- `candidate set`: The deduplicated set passed to reranking.
- `ranker`: A model or rule system that orders candidates for a request.
- `reranker`: A higher-cost model used on a smaller candidate set.
- `retrieval index`: Lexical, dense, hybrid, or ANN index used for candidate generation.
- `relevance label`: Human, behavioral, or synthetic judgment used for evaluation.
- `feedback policy`: Rules for converting behavior into training or evaluation labels.
- `experiment unit`: User, session, query, listing, tenant, or request unit assigned to a variant.
- `serving policy`: Versioned rules for candidate generation, ranking, filtering, diversity, exploration, and fallbacks.
- `release candidate`: Versioned index, feature, model, policy, and service tuple proposed for launch.

## 1. Production outcome

The final system should allow a reviewer to:

1. Ingest a catalogue and interaction dataset.
2. Build lexical, dense, hybrid, collaborative-filtering, and content-based candidate generators.
3. Train or configure a ranking model.
4. Evaluate recall, NDCG, MRR, MAP, precision, diversity, coverage, novelty, latency, and business proxy metrics.
5. Compare baselines against a candidate ranking stack.
6. Serve search and recommendation APIs.
7. Produce online-style experiment readouts without claiming real randomized production traffic if none exists.
8. Detect feedback bias, popularity bias, cold-start weaknesses, and offline/online metric mismatch.
9. Release with documented gates and rollback.
10. Explain why the chosen method beats simpler alternatives for the target workflow.

The system is production-ready when a reviewer can run a query, inspect candidate generation, inspect reranking features, trace the ranked result list, review offline and online-style metrics, trigger a bad release, and see rollback evidence.

## 2. Business problem, users, scope, and non-goals

### Business problem

E-commerce teams need relevant search and recommendations, but relevance is not a single model score. A user may search with text, browse by category, compare near-duplicates, expect personalized results, or need diversity and freshness. A naive vector search can return semantically similar but wrong items. A naive recommender can overfit popularity, amplify feedback bias, and fail cold-start items. A high-quality ranking stack must combine retrieval, recommendation, filtering, reranking, experimentation, and monitoring.

`ListingMatch` solves this by building a measured two-stage system:

- Stage 1 retrieves enough good candidates quickly.
- Stage 2 ranks candidates using relevance, personalization, business constraints, diversity, freshness, and safety controls.

### Primary users

- Shoppers searching or browsing products.
- Marketplace operators reviewing duplicate or near-duplicate listings.
- Merchandising teams tuning category, freshness, and business constraints.
- ML engineers evaluating ranking and recommendation models.
- Search engineers operating indexes, relevance labels, and latency budgets.
- Product managers reviewing experiment results and launch decisions.
- Trust and safety reviewers checking blocked, restricted, or duplicate items.

### Initial domain

Use one of these practical domains:

- MovieLens-style recommendation benchmark for user-item interactions.
- E-commerce listing catalogue with text, category, seller, price, brand, and image metadata where available.
- Synthetic e-commerce catalogue plus MovieLens interaction path if no public listing dataset is selected.

The recommended portfolio shape is:

- MovieLens or equivalent for recommendation evaluation.
- Product listing or item catalogue for search, semantic matching, and near-duplicate discovery.
- Optional category taxonomy and seller metadata for filters, constraints, and slices.

### Required scope

The first production-style release must include:

- Catalogue ingestion and normalization.
- Interaction-event ingestion.
- Dataset and label documentation.
- Lexical BM25 baseline.
- Dense embedding baseline.
- Hybrid retrieval.
- ANN index or FAISS local baseline.
- Collaborative-filtering recommender baseline.
- Content-based recommender baseline.
- Candidate generation service.
- Deduplication and near-duplicate detection path.
- Ranking or reranking model.
- Feature pipeline for ranking features.
- Offline evaluation harness.
- Online-style experiment readout.
- Search API.
- Recommendation API.
- Similar-item API.
- Explanation/debug endpoint for candidate and ranking traces.
- Low-latency serving target.
- Observability and cost report.
- Release gates and rollback plan.

### Explicit non-goals for the first release

Do not attempt:

- A full marketplace platform.
- Real-time ad auction logic.
- Real production A/B testing without users.
- Reinforcement learning recommender optimization.
- Unbounded personalization using sensitive data.
- Full multimodal listing understanding unless image embeddings are an explicit extension.
- Large-scale distributed ANN infrastructure.
- A generic search engine for every domain.
- Claiming business lift without a valid experiment or a clearly labelled simulation.

## 3. Business outcomes and metric tree

### Primary outcome

Users find relevant items faster and receive useful recommendations while the platform can measure relevance, diversity, latency, and business trade-offs.

### Business metrics

- Search success rate proxy.
- Click-through rate proxy.
- Add-to-cart or conversion proxy.
- Rating prediction quality for MovieLens-style benchmark.
- Duplicate listing review time saved.
- Zero-result rate.
- Reformulation rate.
- Time to first relevant result.
- Coverage of long-tail items.
- Cost per ranked request.
- Latency within product budget.

### Retrieval metrics

- Recall at K.
- Precision at K.
- MRR.
- MAP.
- NDCG at K.
- Candidate recall at K.
- Filter correctness.
- Query coverage.
- Zero-result rate.
- Index freshness.
- Retrieval latency.

### Recommendation metrics

- Hit rate at K.
- Recall at K.
- Precision at K.
- NDCG at K.
- MAP at K.
- Rating RMSE or MAE where appropriate.
- Coverage.
- Diversity.
- Novelty.
- Serendipity proxy.
- Popularity bias.
- Cold-start performance.
- User and item segment performance.

### Ranking metrics

- NDCG at K.
- MRR.
- Pairwise accuracy.
- Calibration of relevance probability.
- Business-weighted utility.
- Diversity-adjusted relevance.
- Constraint violation rate.
- Reranker latency.
- Feature missingness.
- Slice regressions.

### Online-style metrics

Use simulated or replay-based metrics honestly:

- Interleaving win rate where applicable.
- Counterfactual or replay estimate if logged propensities exist.
- Session success proxy.
- Click model caveats.
- Guardrail latency.
- Guardrail diversity.
- Guardrail seller or item exposure concentration.
- Experiment power estimate.
- Launch, hold, or iterate decision.

### Guardrail metrics

- Restricted item leakage.
- Cross-tenant or private-item leakage if tenancy is implemented.
- Duplicate suppression false positives.
- Duplicate suppression false negatives.
- Personalization disabled fallback rate.
- Cold-start fallback quality.
- Feedback ingestion lag.
- Index freshness lag.
- Rollback duration.

## 4. What production-ready means

`ListingMatch` is production-ready when:

- Every ranking result can be traced to candidate sources, feature values, model version, policy version, and index version.
- Lexical, dense, hybrid, collaborative, and content-based baselines are compared before a more complex model is accepted.
- Candidate recall is measured separately from final ranking.
- Offline metrics are not presented as business lift.
- Online-style readouts clearly state whether they are simulated, replayed, interleaved, or actually randomized.
- Feedback data is versioned and bias-aware.
- Time-based splits prevent leakage.
- Cold-start users and cold-start items have explicit fallback behavior.
- Index rebuild, model release, ranking policy release, and rollback are documented.
- Latency is measured at retrieval, feature assembly, reranking, and response stages.
- Restricted, unavailable, or duplicate items are filtered before final results.
- A failed release can be rolled back to the previous model, index, or policy version.

## 5. Non-negotiable requirements

1. Baselines first: popularity, lexical BM25, dense retrieval, collaborative filtering, and content-based methods must be implemented or explicitly scoped.
2. Candidate/ranker separation: measure candidate recall independently from final ranking quality.
3. Time-aware evaluation: use temporal splits for interaction data where possible.
4. Leakage checks: prevent future interactions, labels, or post-event metadata from entering training features.
5. Ranking traceability: every served result list must record model, feature, index, policy, and candidate source versions.
6. Feedback policy: implicit feedback must not be treated as unbiased ground truth without caveats.
7. Low-latency design: expensive reranking runs only on bounded candidate sets.
8. Release gates: quality, latency, coverage, diversity, guardrail, and slice gates must block bad releases.
9. Online honesty: simulated online metrics must be labelled as simulation or replay.
10. Rollback: index, model, feature, and policy rollback must be possible and tested.
11. Security: restricted or unavailable listings cannot appear in final results.
12. Evidence: evaluation report, experiment memo, service API, and ranking trace proof must exist.

## 6. Core journeys and required UX

### Search journey

The user should be able to:

1. Submit a keyword query.
2. Receive ranked results with category, price, seller, rating, and availability metadata.
3. Apply filters.
4. See spelling, synonym, or query-understanding behavior where implemented.
5. Receive no-result handling or fallback suggestions.

Required operator/debug UX:

- Query debug view.
- Lexical, dense, and hybrid candidate lists.
- Reranker feature view.
- Final ranking explanation.
- Latency breakdown.
- Zero-result and reformulation report.

### Recommendation journey

The user should be able to:

1. Open a homepage, listing page, or user profile route.
2. Receive personalized or contextual recommendations.
3. Receive reasonable fallback recommendations for cold-start cases.
4. Avoid seeing unavailable, restricted, or exact-duplicate listings.

Required operator/debug UX:

- User profile summary.
- Candidate source mix.
- Popularity, collaborative, and content-based comparison.
- Diversity and coverage metrics.
- Cold-start behavior.
- Feedback event trace.

### Similar-listing and duplicate-review journey

The marketplace operator should be able to:

1. Select a listing.
2. See semantically similar listings.
3. See likely duplicates and near-duplicates.
4. Review similarity evidence.
5. Mark duplicate, not duplicate, related, or unsure.
6. Feed reviewed labels into future evaluation.

Required operator/debug UX:

- Side-by-side listing comparison.
- Text similarity.
- Attribute similarity.
- Embedding similarity.
- Image similarity if implemented.
- Duplicate threshold report.
- Review queue metrics.

### Ranking experiment journey

The product or ML reviewer should be able to:

1. Compare current production against candidate.
2. Inspect offline metric deltas.
3. Inspect slice deltas.
4. Inspect latency and cost deltas.
5. Inspect online-style experiment readout.
6. Decide launch, hold, iterate, or roll back.

Required UX:

- Experiment memo.
- Metric table.
- Confidence interval or uncertainty note.
- Segment analysis.
- Offline/online mismatch risks.
- Launch recommendation.

## 7. Governance, access, and ranking policy

### Ranking invariants

- A request cannot rank items the user is not allowed to see.
- Unavailable or restricted items must be filtered before final response.
- Exact duplicate suppression must run before final ranking when enabled.
- Business boosts must be versioned and visible in the ranking policy.
- Sponsored or paid placement, if simulated, must be clearly separated from organic relevance.
- Personalization must be disable-able and must have a fallback.
- Sensitive user attributes must not be used unless the policy explicitly allows them.
- A ranker cannot use features that are unavailable at serving time.
- Feature freshness must be checked before release.
- Ranking traces must be retained long enough for debugging and experiment analysis.

### Candidate generation policy

The candidate policy must define:

- Candidate sources.
- Number of candidates per source.
- Merge and deduplication rules.
- Filter order.
- Score normalization.
- Fallback order.
- Cold-start behavior.
- Latency budget.
- Cache policy.

### Ranking policy

The ranking policy must define:

- Ranker version.
- Feature set version.
- Model version.
- Business constraints.
- Diversity constraints.
- Exploration setting.
- Personalization setting.
- Tie-breaking rule.
- Restricted-item filter.
- Duplicate suppression threshold.
- Latency timeout and fallback.

### Feedback policy

The feedback policy must define:

- Which events are collected.
- Which events become labels.
- Which events are only diagnostics.
- How negative feedback is interpreted.
- How position bias is handled.
- Whether propensities are logged.
- How bot or low-quality events are filtered.
- How delayed conversions are joined.
- How reviewed duplicate labels are retained.

## 8. Reference architecture and project boundaries

### Recommended stack

Minimal local path:

- FastAPI for service API.
- PostgreSQL for catalogue, interactions, labels, experiments, and audit.
- Redis for cache and request tracing.
- OpenSearch or Elasticsearch for BM25 and hybrid search, or a local BM25 substitute for the minimal path.
- FAISS for local dense retrieval.
- sentence-transformers for item embeddings.
- scikit-learn for baselines.
- LightGBM, XGBoost, or CatBoost for ranking model.
- PyTorch or Transformers for optional deep text model.
- MLflow for experiment tracking.
- Docker Compose for local dependencies.
- OpenTelemetry and Prometheus for observability.

Full production-style path:

- OpenSearch or Elasticsearch with lexical and vector support.
- ANN index with rebuild and publication flow.
- Feature pipeline using Polars, pandas, or a workflow orchestrator.
- ONNX export for transformer or ranking model where applicable.
- FastAPI service with low-latency inference.
- Batch scoring and online scoring paths.
- CI/CD with evaluation gates.
- Staging deployment, canary release, and rollback.
- Monitoring dashboard for relevance, latency, feedback, drift, and cost.

### Component responsibilities

Ingestion service:

- Loads catalogue, item metadata, interactions, labels, and review outcomes.
- Normalizes text, categories, and attributes.
- Assigns stable item and user IDs.

Index builder:

- Builds lexical index.
- Builds dense embedding index.
- Publishes index versions.
- Records index lineage.

Candidate service:

- Executes BM25, dense, hybrid, popularity, collaborative-filtering, and content-based candidate generators.
- Merges, deduplicates, filters, and returns candidate traces.

Feature service:

- Computes ranking features consistently for training and serving.
- Tracks feature freshness and missingness.

Ranker service:

- Scores candidate lists.
- Applies constraints, diversity, and tie-breaking.
- Emits ranking traces.

Experiment service:

- Assigns variants for simulated or real online-style tests.
- Stores exposure, click, conversion, and guardrail metrics.
- Produces experiment readouts.

Evaluation harness:

- Runs retrieval, recommendation, ranking, duplicate, latency, and slice evaluations.
- Generates release reports.

### Durable handoff and reconciliation

Use durable state for:

- Dataset version.
- Interaction snapshot.
- Label set.
- Embedding model version.
- Index build version.
- Feature set version.
- Model version.
- Ranking policy version.
- Experiment assignment.
- Release candidate.

Reconciliation jobs should detect:

- Index version exists but is not queryable.
- Model version exists but no release record references it.
- Candidate release is approved but route still points to old policy.
- Interaction events are ingested but not included in a labelled snapshot.
- Duplicate-review labels exist but evaluation set was not regenerated.
- Feature set was updated without serving contract update.

### Documentation and evidence system

Required living documents:

- `docs/problem-statement.md`
- `docs/product-requirements.md`
- `docs/architecture.md`
- `docs/data-model.md`
- `docs/search-contract.md`
- `docs/recommendation-contract.md`
- `docs/ranking-policy.md`
- `docs/feedback-policy.md`
- `docs/evaluation-plan.md`
- `docs/experiment-design.md`
- `docs/security-and-governance.md`
- `docs/observability-cost.md`
- `docs/deployment-runbook.md`
- `docs/rollback-runbook.md`
- `docs/progress-log.md`

Required generated evidence:

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

## 9. Data, event, and API contracts

### Item contract

```json
{
  "item_id": "item_000123",
  "title": "Wireless Noise Cancelling Headphones",
  "description": "Over-ear headphones with active noise cancelling and USB-C charging.",
  "category": "electronics.audio.headphones",
  "brand": "ExampleSound",
  "seller_id": "seller_42",
  "price": 89.99,
  "currency": "USD",
  "availability": "in_stock",
  "created_at": "2026-07-28T10:00:00Z",
  "updated_at": "2026-07-28T10:00:00Z",
  "policy_flags": []
}
```

### Interaction event contract

```json
{
  "event_id": "evt_01J5...",
  "user_id": "user_123",
  "session_id": "session_abc",
  "item_id": "item_000123",
  "event_type": "click",
  "query": "noise cancelling headphones",
  "position": 3,
  "ranking_policy_version": "rank-policy-v12",
  "experiment_id": "exp-search-v5",
  "variant": "candidate",
  "occurred_at": "2026-07-28T10:03:00Z"
}
```

### Relevance label contract

```json
{
  "label_id": "label_001",
  "query_id": "query_009",
  "item_id": "item_000123",
  "label": 3,
  "label_scale": "0_to_3",
  "source": "human_judgment",
  "annotator_id": "ann_04",
  "created_at": "2026-07-28T10:10:00Z"
}
```

### Candidate trace contract

```json
{
  "request_id": "req_01J5...",
  "query": "noise cancelling headphones",
  "candidate_sources": [
    {"source": "bm25", "count": 100, "latency_ms": 18},
    {"source": "dense", "count": 100, "latency_ms": 24},
    {"source": "collaborative", "count": 50, "latency_ms": 8}
  ],
  "merged_count": 180,
  "deduped_count": 145,
  "filtered_count": 132,
  "candidate_policy_version": "candidate-policy-v7"
}
```

### Ranking trace contract

```json
{
  "request_id": "req_01J5...",
  "ranking_policy_version": "rank-policy-v12",
  "feature_set_version": "rank-features-v9",
  "ranker_version": "lgbm-ranker-v4",
  "index_versions": {
    "bm25": "bm25-20260728-001",
    "dense": "dense-20260728-002"
  },
  "result_count": 20,
  "latency_ms": {
    "candidate_generation": 52,
    "feature_lookup": 16,
    "reranking": 11,
    "total": 91
  }
}
```

### Minimum API surface

Public or application APIs:

- `GET /search`
- `GET /recommendations/home`
- `GET /recommendations/item/{item_id}/similar`
- `POST /events`
- `GET /items/{item_id}`

Operator and reviewer APIs:

- `POST /admin/ingest/catalogue`
- `POST /admin/ingest/interactions`
- `POST /admin/indexes/build`
- `POST /admin/evals/run`
- `POST /admin/releases`
- `POST /admin/releases/{id}/approve`
- `POST /admin/releases/{id}/canary`
- `POST /admin/releases/{id}/rollback`
- `GET /admin/traces/{request_id}`
- `GET /admin/experiments/{experiment_id}/readout`

## 10. Candidate generation, ranking, and recommendation lifecycle

### End-to-end flow

1. Ingest catalogue.
2. Ingest interactions.
3. Normalize text and structured attributes.
4. Build train, validation, test, and time-based splits.
5. Build lexical index.
6. Build dense embeddings and ANN index.
7. Build collaborative-filtering candidate generator.
8. Build content-based candidate generator.
9. Merge and deduplicate candidates.
10. Compute training and serving features.
11. Train or configure ranker.
12. Evaluate retrieval, recommendation, ranking, duplicate detection, slices, latency, and cost.
13. Submit release candidate.
14. Approve, canary, promote, or roll back.
15. Monitor feedback, drift, bias, freshness, and latency.

### Candidate generators

Required:

- Popularity baseline.
- BM25 lexical search.
- Dense embedding retrieval.
- Hybrid retrieval.
- Similar-item retrieval.
- Collaborative filtering.
- Content-based recommendation.

Optional:

- Two-tower model.
- Graph-based co-view or co-purchase retrieval.
- Query expansion.
- Category-specific rankers.
- Image embedding similarity.

### Ranking stages

Use a staged architecture:

1. Retrieve 100 to 1000 candidates quickly.
2. Merge and deduplicate.
3. Apply hard filters.
4. Compute bounded feature set.
5. Rerank top candidates.
6. Apply business, diversity, and exploration policy.
7. Return top K.
8. Emit trace and exposure event.

### Release tuple

Every release must identify:

```text
catalogue_snapshot_id
interaction_snapshot_id
label_set_id
embedding_model_version
bm25_index_version
dense_index_version
candidate_policy_version
feature_set_version
ranker_version
ranking_policy_version
experiment_id
service_image_digest
evaluation_run_id
deployment_id
```

## 11. Evaluation and release gates

### Required datasets

Search:

- Labelled query set.
- Query taxonomy.
- Head, torso, and tail query slices.
- Zero-result and ambiguous-query cases.
- Category and metadata filter cases.

Recommendation:

- MovieLens-style user-item interaction dataset.
- Time-based train, validation, and test split.
- Cold-start user slice.
- Cold-start item slice.
- Popularity-decile slices.
- Optional negative-sampling policy.

Duplicate and similar listings:

- Exact duplicate cases.
- Near-duplicate cases.
- Related but not duplicate cases.
- Same title but different item cases.
- Same item with changed seller or price cases.

Ranking:

- Candidate set snapshots.
- Feature snapshots.
- Relevance labels or implicit-feedback labels.
- Slice labels by category, price band, seller, popularity, and freshness.

### Starter quality gates

A release candidate must pass:

- Candidate recall at K does not regress.
- NDCG at K does not regress beyond tolerance.
- MRR does not regress beyond tolerance for search.
- Recommendation hit rate or recall at K does not regress beyond tolerance.
- Coverage does not fall below threshold.
- Diversity does not fall below threshold unless explicitly approved.
- Cold-start fallback quality meets threshold.
- Restricted-item leakage is zero.
- Duplicate suppression false-positive and false-negative rates are within threshold.
- p95 latency is within budget.
- Offline/online-style experiment readout is attached.
- Rollback target exists.

### Release comparison rules

Use these rules:

- Candidate must compare against current production and simple baselines.
- Improvements must be reported with uncertainty or repeated-run stability where applicable.
- Offline metrics must not be described as confirmed conversion lift.
- If candidate improves NDCG but reduces diversity or coverage sharply, it must be held or approved with documented trade-off.
- If candidate improves aggregate metrics but fails a critical slice, it must be held.
- If candidate uses a feature unavailable at serving time, it must fail.
- If feedback data is biased or incomplete, the evaluation memo must state the limitation.

### Required experiment memo

The experiment memo must include:

- Hypothesis.
- Primary metric.
- Guardrail metrics.
- Experiment unit.
- Variant definitions.
- Dataset and time window.
- Offline results.
- Online-style or replay results.
- Segment results.
- Bias and leakage caveats.
- Latency and cost results.
- Launch, hold, iterate, or roll back recommendation.

### Minimum benchmark shape

For a portfolio version:

- At least 1000 items.
- At least 100 users for recommendation path where possible.
- At least 5000 interaction events where possible.
- At least 50 labelled search queries.
- At least 100 duplicate or similar-item labels.
- At least 5 slices.
- At least 3 candidate generators.
- At least 2 ranker variants.
- At least 2 latency traffic levels.

## 12. Security, privacy, and governance

### Trust boundaries

Treat these as boundaries:

- Shopper or application client.
- Search and recommendation API.
- Event ingestion.
- Catalogue ingestion.
- Feature store or feature tables.
- Retrieval indexes.
- Ranking model.
- Experiment assignment.
- Operator dashboard.
- Offline training data.
- Monitoring and logs.

### Required controls

- Restricted and unavailable items filtered before response.
- Tenant or seller isolation if multi-tenant data is simulated.
- Input validation for query and filters.
- Rate limits for public APIs.
- PII minimization in user profiles.
- Sensitive user attributes excluded unless explicitly approved.
- Event data retention policy.
- Ranking traces redacted for public logs.
- Model and index version audit.
- Operator-only access to debug traces.
- Release approval audit.
- Rollback audit.

### Governance documents

The repo must include:

- Dataset card.
- Interaction-event card.
- Labeling guide.
- Feedback policy.
- Ranking policy.
- Experiment design memo.
- Bias and fairness caveat.
- Security and privacy checklist.
- Release and rollback policy.

### Prohibited claims

Do not claim:

- Business lift from offline metrics alone.
- Personalization quality without cold-start and bias analysis.
- Search quality from embedding similarity alone.
- Recommendation quality from RMSE alone.
- Production readiness without low-latency serving and rollback.
- Fairness or neutrality without exposure and slice analysis.
- A/B test validity without randomized assignment or clear simulation caveat.
- Duplicate detection quality without reviewed positive and negative examples.

## 13. Observability, feedback, and cost

### Correlation model

Every served request should record:

- `request_id`
- `user_id` or anonymous profile ID
- `session_id`
- `query_id`
- `candidate_policy_version`
- `ranking_policy_version`
- `feature_set_version`
- `ranker_version`
- `index_versions`
- `experiment_id`
- `variant`
- `latency_breakdown`

### Metrics

Service:

- Request rate.
- Error rate.
- p50, p95, and p99 latency.
- Candidate-generation latency.
- Feature-lookup latency.
- Reranking latency.
- Cache hit rate.
- Timeout and fallback rate.

Search:

- Zero-result rate.
- Reformulation rate.
- Query coverage.
- Recall at K.
- NDCG at K.
- MRR.
- Filter usage and correctness.

Recommendation:

- Exposure count.
- Click-through proxy.
- Hit rate at K.
- Coverage.
- Diversity.
- Novelty.
- Popularity concentration.
- Cold-start fallback rate.

Ranking:

- Feature missingness.
- Score distribution.
- Constraint violation rate.
- Ranker fallback rate.
- Slice regressions.

Feedback:

- Event ingestion lag.
- Event drop rate.
- Label delay.
- Bot or invalid event rate.
- Position-bias indicators.
- Duplicate review throughput.

Cost:

- Cost per request.
- Cost per ranked result list.
- Embedding-index build cost.
- Reranker CPU or GPU cost.
- Storage cost per index version.

### Dashboards

Build at least:

- Search relevance dashboard.
- Recommendation relevance dashboard.
- Ranking latency dashboard.
- Feedback and event ingestion dashboard.
- Index freshness dashboard.
- Experiment dashboard.
- Bias and exposure dashboard.
- Release and rollback dashboard.

## 14. Reliability, deployment, and rollback

### Required service indicators

Define objectives for:

- Search API availability.
- Recommendation API availability.
- p95 latency.
- Candidate-generation timeout rate.
- Reranker timeout rate.
- Index freshness.
- Event ingestion lag.
- Feature freshness.
- Zero-result rate.
- Rollback duration.

### Degraded modes

Document and test:

- Dense index unavailable.
- BM25 index unavailable.
- Ranker unavailable.
- Feature store unavailable.
- Event ingestion delayed.
- Embedding model unavailable.
- Cache unavailable.
- Experiment assignment service unavailable.
- Catalogue update delayed.

### Fallbacks

Use explicit fallbacks:

- Hybrid search falls back to BM25.
- Dense search falls back to BM25 or popularity.
- Personalized recommendation falls back to contextual or popularity.
- Ranker falls back to rule score.
- Feature-missing case falls back to feature-safe model.
- Duplicate suppression can fail closed for restricted duplicates and fail open for uncertain non-critical duplicates.

### Rollback options

Support rollback for:

- Ranking policy.
- Candidate policy.
- Ranker model.
- Feature set.
- BM25 index version.
- Dense index version.
- Embedding model.
- Experiment variant.
- Service image.

Rollback verification must confirm:

- Route points to previous release tuple.
- Search and recommendation smoke tests pass.
- Restricted-item leakage remains zero.
- Latency returns to budget.
- Event logging still works.
- Rollback report is generated.

## 15. Step-by-step implementation plan

### Phase 0: Discovery, domain, and metrics

- Select MovieLens or equivalent recommendation dataset.
- Select or synthesize listing catalogue.
- Define search, recommendation, similar-item, and duplicate workflows.
- Define primary and guardrail metrics.
- Write experiment design and release tuple.

### Phase 1: Repository, contracts, and local platform

- Create FastAPI services and shared packages.
- Add PostgreSQL, Redis, search backend, and local vector index.
- Add docs and report directories.
- Add tests, linting, and CI skeleton.

### Phase 2: Catalogue and interaction ingestion

- Ingest items.
- Normalize text and attributes.
- Ingest interaction events.
- Add dataset snapshots.
- Add time-based splits.
- Write dataset card and leakage checklist.

### Phase 3: Lexical, dense, and hybrid search

- Implement BM25 baseline.
- Generate embeddings.
- Build FAISS or vector index.
- Combine lexical and dense scores.
- Add filters.
- Evaluate labelled queries.

### Phase 4: Recommendation baselines

- Implement popularity baseline.
- Implement collaborative-filtering baseline.
- Implement content-based recommendation.
- Evaluate hit rate, recall, NDCG, diversity, coverage, novelty, and cold-start slices.

### Phase 5: Candidate generation and near-duplicate detection

- Create candidate service.
- Merge and deduplicate candidate sources.
- Add similar-item endpoint.
- Add duplicate-review labels.
- Evaluate duplicate precision and recall.

### Phase 6: Ranking features and ranker

- Define training and serving features.
- Add feature consistency tests.
- Train LightGBM, XGBoost, CatBoost, or neural ranker.
- Add reranker.
- Evaluate ranking metrics and slices.

### Phase 7: Serving APIs

- Implement search API.
- Implement recommendation API.
- Implement similar-item API.
- Implement event ingestion API.
- Implement debug trace API.
- Add low-latency budget and cache policy.

### Phase 8: Experiment and release gates

- Add release candidates.
- Add offline evaluation gates.
- Add online-style readout.
- Add experiment assignment for simulated or real traffic.
- Add approval workflow.

### Phase 9: Observability, feedback, and bias monitoring

- Add request traces.
- Add exposure and interaction logging.
- Add dashboards.
- Add feedback-bias report.
- Add drift and index freshness monitors.

### Phase 10: Deployment and rollback

- Containerize services.
- Add staging deployment.
- Add canary or shadow mode.
- Add rollback by policy, model, feature, index, and service image.
- Generate release and rollback reports.

### Phase 11: Portfolio proof

- Generate retrieval report.
- Generate recommendation report.
- Generate ranking report.
- Generate duplicate report.
- Generate experiment memo.
- Generate latency report.
- Generate final evidence manifest.

## 16. Completion evidence checklist

### Product and business

- Problem statement.
- Product requirements.
- Search, recommendation, and duplicate workflows.
- Experiment hypothesis and launch decision.

### Data

- Dataset card.
- Interaction-event card.
- Labeling guide.
- Time-based split.
- Leakage checklist.
- Feedback policy.

### Retrieval

- BM25 baseline.
- Dense baseline.
- Hybrid search.
- Metadata filters.
- Reranking.
- Search evaluation report.

### Recommendation

- Popularity baseline.
- Collaborative-filtering baseline.
- Content-based baseline.
- Candidate generator.
- Recommendation evaluation report.
- Cold-start analysis.

### Ranking

- Feature set.
- Ranker model.
- Ranking policy.
- Reranking trace.
- Ranking evaluation report.
- Slice analysis.

### Duplicate and similar-item matching

- Similar-item endpoint.
- Duplicate labels.
- Duplicate threshold decision.
- Duplicate evaluation report.
- Review workflow.

### Serving and operations

- Search API.
- Recommendation API.
- Similar-item API.
- Event API.
- Debug trace API.
- Low-latency report.
- Observability dashboards.
- Release and rollback reports.

### Governance and portfolio

- Security and privacy checklist.
- Bias and exposure report.
- Experiment memo.
- Final evidence manifest.
- Interview defense notes.

## 17. Industry-level implementation order

Build in this order:

1. Define user workflows and metrics.
2. Build datasets, labels, and time-based splits.
3. Build simple baselines.
4. Measure candidate recall.
5. Build hybrid retrieval and collaborative/content recommendation.
6. Add feature pipeline and ranker.
7. Add serving APIs and traces.
8. Add release gates.
9. Add online-style experiment memo.
10. Add feedback-bias, exposure, and drift monitoring.
11. Add rollback.
12. Add portfolio evidence.

This order prevents the common failure of building an impressive neural ranker before knowing whether the candidate set contains the right items.

## 18. Common failure modes

- Treating embeddings as a complete search system.
- Reporting RMSE but not top-K recommendation quality.
- Optimizing final ranking while candidate recall is poor.
- Using random splits for time-dependent recommendation data.
- Training on future interactions.
- Ignoring position bias in clicks.
- Claiming A/B test results from offline replay.
- Improving head items while hurting long-tail coverage.
- Letting business boosts hide relevance regressions.
- Reranking too many candidates and missing latency targets.
- Returning unavailable or restricted items.
- Suppressing non-duplicate listings as duplicates.
- Evaluating only aggregate metrics and missing category slices.
- Building a service API without ranking traces.
- Releasing a new index without rollback.

## 19. Interview defense questions

Product:

- What user problem does `ListingMatch` solve?
- Which metric is the primary metric and why?
- What is your launch recommendation?
- What did you choose not to build?

Retrieval:

- How did BM25 compare to dense retrieval?
- How did hybrid retrieval merge scores?
- How did you measure candidate recall?
- What happens when the dense index is unavailable?

Recommendation:

- How did popularity, collaborative filtering, and content-based methods compare?
- How did you handle cold-start users and items?
- What feedback bias exists in your data?
- Why is RMSE insufficient for top-K recommendations?

Ranking:

- What features does your ranker use?
- Which features are available at serving time?
- How did the ranker affect diversity and coverage?
- Why did the candidate pass or fail release gates?

Experimentation:

- What is the difference between offline and online metrics?
- What experiment unit would you randomize in production?
- How did you estimate uncertainty?
- What would invalidate the experiment?

Operations:

- How do you roll back a bad ranker?
- How do you roll back a bad index?
- What are your latency budgets?
- How do ranking traces help incident review?

## 20. Final definition of done

`ListingMatch` is done when:

- Catalogue and interaction data are ingested, versioned, and documented.
- Time-based splits and leakage checks are implemented.
- BM25, dense, hybrid, popularity, collaborative, and content-based baselines are evaluated.
- Candidate recall is measured separately from ranking quality.
- A ranker or reranker improves the selected primary metric without unacceptable guardrail regressions.
- Search, recommendation, similar-item, event, and debug APIs work.
- Ranking traces expose candidate source, feature, model, index, and policy versions.
- Offline evaluation, online-style experiment memo, latency report, feedback-bias report, and release report exist.
- A bad release can roll back model, index, feature, or policy version.
- The final evidence package supports the search/ranking and recommender-system interview defense.
