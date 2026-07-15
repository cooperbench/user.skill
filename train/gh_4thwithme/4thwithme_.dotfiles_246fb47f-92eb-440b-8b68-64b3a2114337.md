---
session_id: "4thwithme/.dotfiles|246fb47f-92eb-440b-8b68-64b3a2114337"
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme/.dotfiles
start_time: "2026-04-01T09:51:25.557Z"
n_turns: 4
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

hey i need to to tell devops guys what we need for opensearch setup... we have added it in this branch locally, but now we need to spin up it in aws...tell me the parameters i have right now and what features do i use

> AGENT

Here's everything DevOps needs:

---

## AWS OpenSearch Setup Requirements

### Version
- **OpenSearch 2.11.0** (must match — we use ML Commons plugin features tied to this version)

### Required Plugins
- **ML Commons** (built-in) — used for neural search model hosting
- **k-NN** (built-in) — FAISS engine for vector similarity search

### Cluster ML Settings (applied at runtime by our bootstrap CLI)
```
plugins.ml_commons.only_run_on_ml_node = false
plugins.ml_commons.model_access_control_enabled = true
plugins.ml_commons.native_memory_threshold = 99
```

### Instance Sizing
- Local dev uses `-Xms2g -Xmx2g` JVM heap. Production needs more — the ML model (`huggingface/sentence-transformers/all-distilroberta-v1`) generates 768-dimension vectors and runs inference on ingest.
- Recommend **ml.m5.xlarge** or higher for data nodes if running model on data nodes (we set `only_run_on_ml_node=false`).

### Index Configuration
- **Index name**: `products-neural-search` (configurable via `OPENSEARCH_INDEX_NAME` env var)
- **Shards**: 3
- **Replicas**: 1
- **k-NN enabled**: `index.knn = true`
- **ef_search**: 512
- **Vector field**: `product_embedding` — 768 dimensions, HNSW algorithm, FAISS engine, L2 space type, ef_construction=512, m=48

### Pipelines (created by our bootstrap CLI)
1. **Ingest pipeline** `products-neural-pipeline` — text_embedding processor, maps `combined_text_for_embedding` -> `product_embedding`
2. **Search pipeline** `hybrid-search-pipeline` — normalization-processor with min_max normalization, arithmetic_mean combination, weights `[0.1, 0.9]`

### ML Model
- **Model**: `huggingface/sentence-transformers/all-distilroberta-v1` v1.0.1
- **Format**: TORCH_SCRIPT (default, also supports ONNX)
- **Output dimension**: 768
- Model is registered, deployed, and managed via our CLI: `npm run cli:dev -- bootstrap-neural-search`

### Environment Variables Needed
| Variable | Example | Description |
|---|---|---|
| `OPENSEARCH_HOST` | `https://search-xxx.us-east-1.es.amazonaws.com` | Domain endpoint |
| `OPENSEARCH_USERNAME` | `admin` | Fine-grained access control user |
| `OPENSEARCH_PASSWORD` | `***` | Password |
| `OPENSEARCH_INDEX_NAME` | `products-neural-search` | Index name |
| `OPENSEARCH_NEURAL_CACHE_TTL` | `3600` | Search cache TTL (seconds) |
| `OPENSEARCH_DASHBOARDS_URL` | `https://.../_dashboards` | Dashboards URL (for health checks) |

### Security
- Local dev runs with `plugins.security.disabled=true`. AWS OpenSearch Service has security built-in — use **fine-grained access control** with IAM or internal user DB.
- The app authenticates via basic auth (username/password).

### Health Check
- App calls `GET /_cluster/health` on startup and exposes it via the health module.

### Key Consideration for AWS
AWS OpenSearch Service may restrict ML Commons model registration. If using **Amazon OpenSearch Serverless** or a managed domain, verify that:
1. Custom model upload via `_plugins/_ml/models/_register` is supported on your instance type
2. The instance type supports ML inference workloads
3. You may need **ml nodes** specifically if the domain doesn't allow `only_run_on_ml_node=false`

Alternatively, consider **Amazon OpenSearch with ML nodes** or **SageMaker integration** if custom model hosting is restricted on standard data nodes.

> DEVELOPER

we do the same 
  - Local dev uses -Xms2g -Xmx2g JVM heap. Production needs more — the ML model (huggingface/sentence-transformers/all-distilroberta-v1) generates 768-dimension vectors and runs inference on ingest.                                                                   
  - Recommend ml.m5.xlarge or higher for data nodes if running model on data nodes (we set only_run_on_ml_node=false).

@src/modules/cli/commands/bootstrap-neural-search.command.ts ..check code...and use deep analizis..you did bad job re do it

> AGENT

Here's the corrected, code-derived spec:

---

## AWS OpenSearch — What We Actually Use

### Engine & Client
- **OpenSearch 2.11.0**
- **Client**: `@opensearch-project/opensearch` v3.5.1
- **Auth**: Basic auth (username/password)
- **Local dev**: security plugin disabled

### ML Model (hosted inside OpenSearch)
- **Model**: `huggingface/sentence-transformers/all-distilroberta-v1` v1.0.1
- **Format**: TORCH_SCRIPT (also supports ONNX)
- **Vector dimension**: 768
- **Runs on data nodes** (`only_run_on_ml_node=false`)
- **Model ID resolved dynamically** every 5 minutes at runtime

### Cluster Settings (applied by bootstrap CLI)
```
plugins.ml_commons.only_run_on_ml_node = false
plugins.ml_commons.model_access_control_enabled = true
plugins.ml_commons.native_memory_threshold = 99
```

### Index: `products-neural-search`
- **Shards**: 3, **Replicas**: 1
- **k-NN enabled**: `index.knn = true`
- **ef_search**: 512
- **Default pipeline**: `products-neural-pipeline`
- **~40 mapped fields** including 3 nested types (`colors`, `default_unit_prices`, `colors.rbgs`)
- **Vector field**: `product_embedding` — 768 dims, HNSW, FAISS engine, L2 space, ef_construction=512, m=48
- **Document count**: ~25,600 products (from `styles_mv`)
- **Vector memory estimate**: 768 dims x 4 bytes x 30k docs ≈ ~90MB just for vectors

### Pipelines

**Ingest pipeline** `products-neural-pipeline`:
- `text_embedding` processor
- Maps `combined_text_for_embedding` → `product_embedding`
- Runs on every bulk index operation (embedding generated at ingest time)

**Search pipeline** `hybrid-search-pipeline`:
- `normalization-processor`
- Normalization: `min_max`
- Combination: `arithmetic_mean`
- **Weights**: `[0.1, 0.9]` — 10% BM25, 90% neural

### Query Pattern: Hybrid Search
- Uses OpenSearch `hybrid` query combining:
  1. **BM25 bool** — match on `name` (boost 0.1), `condensed_features` (boost 0.3), plus dynamic boosts for brand/color/size/price/gender
  2. **Neural k-NN** — `product_embedding` with `k = size * 5`
- **Collapse** on `product_id` (dedup)
- **min_score**: 0.4
- **Default result limit**: 15 (max 50)
- **Max query length**: 500 chars

### Bulk Indexing
- **Default batch size**: 60
- **Default concurrency**: 2
- **Max batch size**: 1,000
- **Max concurrency**: 20
- Model registration/deploy polling: 10s interval, 120 attempts (~20 min timeout)

### Health Checks
- `GET /_cluster/health` — called on startup + exposed via `/health` endpoint
- `GET {OPENSEARCH_DASHBOARDS_URL}/api/status` — Dashboards availability check

### Environment Variables (6 total)
| Variable | Example |
|---|---|
| `OPENSEARCH_HOST` | `https://search-xxx.us-east-1.es.amazonaws.com` |
| `OPENSEARCH_USERNAME` | `master_user` |
| `OPENSEARCH_PASSWORD` | `***` |
| `OPENSEARCH_INDEX_NAME` | `products-neural-search` |
| `OPENSEARCH_NEURAL_CACHE_TTL` | `3600` (seconds) |
| `OPENSEARCH_DASHBOARDS_URL` | `https://.../_dashboards` |

### Bootstrap Command
```bash
npm run cli:dev -- bootstrap-neural-search --cleanup -b 100 -c 4
```
Steps: configure cluster → register model group → register model → deploy model → create ingest pipeline → create search pipeline → create index → bulk index all products.

### AWS-Specific Concerns
1. **ML Commons model registration** (`_plugins/_ml/models/_register`) must be supported — verify instance type allows it
2. We set `only_run_on_ml_node=false` — if AWS domain enforces dedicated ML nodes, either add ML nodes or adjust
3. Local dev disables security plugin — AWS has built-in security, just provide credentials
4. No TLS config in code — AWS OpenSearch endpoints are HTTPS by default, client should work as-is
