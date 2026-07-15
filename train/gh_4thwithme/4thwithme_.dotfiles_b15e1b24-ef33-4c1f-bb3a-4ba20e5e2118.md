> DEVELOPER

analyze changes in this branch regarding opensearch setup< and give me main points what was done.
than put as separated section in details what we need to setup and how in opensearch what are we going to use

> AGENT

Here's the full analysis:

---

## What Was Done — Main Points

**1. OpenSearch infrastructure added**
- `OpensearchService` — low-level client wrapper: index CRUD, bulk indexing, ML model lifecycle (register/deploy/undeploy/delete), ingest & search pipeline management
- `OpensearchNeuralService` — high-level product search: hybrid neural+BM25 queries, query enhancement (brand/color/size/gender/price detection), product document transformation
- `OpensearchModule` — NestJS module wiring both services

**2. ML model pipeline (HuggingFace)**
- Model: `huggingface/sentence-transformers/all-distilroberta-v1` (v1.0.1, TORCH_SCRIPT)
- Model group: `neural-search-model-group`
- Ingest pipeline: `products-neural-pipeline` — auto-generates `product_embedding` from `combined_text_for_embedding` on document ingest
- Search pipeline: `hybrid-search-pipeline` — min_max normalization, arithmetic_mean combination, weights [BM25=0.2, Neural=0.8]

**3. Two CLI bootstrap commands**
- `setup-neural-search` — registers model group, model, deploys it, creates both pipelines (skippable steps)
- `bootstrap-neural-search` — full end-to-end: cluster settings → model → pipelines → index creation → bulk product sync with concurrency control and graceful shutdown

**4. REST API — `/api/v1/neural-search`**
- `GET /neural-search?q=...` — free-text neural search
- `GET /neural-search/use-case/:useCase` — business use-case search (Onboarding, Trade Shows, Events, Gifting, Uniforming, Spirit Wear, etc.)
- `GET /neural-search/view` — HTML debug page with product cards

**5. Local dev environment**
- Docker Compose: OpenSearch 2.11.0 node + OpenSearch Dashboards 2.11.0 on ports `9201`/`5601`
- ML commons pre-configured in Docker: `only_run_on_ml_node=false`, memory threshold 99%, 2GB heap

**6. New env vars**: `OPENSEARCH_HOST`, `OPENSEARCH_USERNAME`, `OPENSEARCH_PASSWORD`, `OPENSEARCH_INDEX_NAME`, `OPENSEARCH_NEURAL_CACHE_TTL`, `OPENSEARCH_DASHBOARDS_URL`

---

## OpenSearch Setup — What Needs to Be Done and How

### Step 1 — Cluster ML Settings

Must be applied once per cluster. The app does this automatically via `configureClusterMLSettings()`:

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.only_run_on_ml_node": false,
    "plugins.ml_commons.model_access_control_enabled": true,
    "plugins.ml_commons.native_memory_threshold": 99
  }
}
```

**Why**: By default ML tasks only run on dedicated ML nodes. Setting `only_run_on_ml_node=false` allows a single-node cluster (local/staging) to run them on data nodes.

---

### Step 2 — Model Group Registration

```json
POST /_plugins/_ml/model_groups/_register
{
  "name": "neural-search-model-group",
  "description": "Model group for neural search embeddings"
}
```
Returns: `model_group_id`

---

### Step 3 — Model Registration

```json
POST /_plugins/_ml/models/_register
{
  "name": "huggingface/sentence-transformers/all-distilroberta-v1",
  "version": "1.0.1",
  "model_group_id": "<model_group_id>",
  "model_format": "TORCH_SCRIPT"
}
```
Returns: `task_id` — poll `GET /_plugins/_ml/tasks/<task_id>` until `state=COMPLETED`.  
**Note**: Takes several minutes on first run — downloads model from HuggingFace.

---

### Step 4 — Model Deployment

```json
POST /_plugins/_ml/models/<model_id>/_deploy
```
Returns: `task_id` — poll until `COMPLETED`. Model `model_id` is then stored in memory by the app and refreshed every 5 minutes via `@Interval`.

---

### Step 5 — Ingest Pipeline

Converts `combined_text_for_embedding` → `product_embedding` (768-dim vector) on every indexed document:

```json
PUT /_ingest/pipeline/products-neural-pipeline
{
  "description": "Neural search ingest pipeline",
  "processors": [{
    "text_embedding": {
      "model_id": "<model_id>",
      "field_map": {
        "combined_text_for_embedding": "product_embedding"
      }
    }
  }]
}
```

---

### Step 6 — Search Pipeline

Hybrid normalization for combining BM25 + neural scores:

```json
PUT /_search/pipeline/hybrid-search-pipeline
{
  "phase_results_processors": [{
    "normalization-processor": {
      "normalization": { "technique": "min_max" },
      "combination": {
        "technique": "arithmetic_mean",
        "parameters": { "weights": [0.2, 0.8] }
      }
    }
  }]
}
```

Weights: 20% keyword BM25, 80% neural vector. Tunable.

---

### Step 7 — Index Creation

Index `products-neural-search` with KNN enabled:

```json
PUT /products-neural-search
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "index.knn": true,
    "index.knn.algo_param.ef_search": 512,
    "default_pipeline": "products-neural-pipeline"
  },
  "mappings": {
    "properties": {
      "product_embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "name": "hnsw",
          "space_type": "l2",
          "engine": "faiss",
          "parameters": { "ef_construction": 512, "m": 48 }
        }
      },
      "combined_text_for_embedding": { "type": "text" },
      "status": { "type": "keyword" },
      "product_id": { "type": "long" },
      "price": { "type": "float" },
      "price_level": { "type": "short" },
      "product_type": { "type": "keyword" },
      "broad_category_names": { "type": "keyword" },
      "sub_category_names": { "type": "keyword" },
      "brand": { "type": "keyword" },
      "sizes": { "type": "keyword" },
      "colors": {
        "type": "nested",
        "properties": { "name": { "type": "keyword" }, "image_url": { "type": "keyword" } }
      }
      // ... all other fields
    }
  }
}
```

**Key**: `default_pipeline` is set so every bulk ingest auto-triggers embedding generation.

---

### Step 8 — Bulk Product Indexing

Run `bootstrap-neural-search` CLI which:
1. Paginates through `styles_mv` table (MySQL)
2. Transforms each style into an `IOpensearchProduct` document with `combined_text_for_embedding` built from: name, product_type, price_level, brand, condensed_features, style_type, category, manufacturer, sub-categories, decoration_method, features
3. Bulk-indexes in batches (default 60, concurrency 2)
4. OpenSearch ingest pipeline auto-generates vectors on write

```bash
npm run cli:dev -- bootstrap-neural-search --batch-size 60 --concurrency 2
# Full rebuild:
npm run cli:dev -- bootstrap-neural-search --cleanup
```

---

### Summary of Resources Created in OpenSearch

| Resource | Name | Type |
|---|---|---|
| Model group | `neural-search-model-group` | ML model group |
| Model | `all-distilroberta-v1` v1.0.1 | Sentence transformer, 768 dim |
| Ingest pipeline | `products-neural-pipeline` | text_embedding processor |
| Search pipeline | `hybrid-search-pipeline` | normalization-processor |
| Index | `products-neural-search` | KNN index, HNSW/faiss, l2 |

> DEVELOPER

beo.. form devops team what they need to do to spin up opensearch i mean

> AGENT

DevOps needs to do two things: **provision the cluster** and **run the one-time bootstrap**.

---

## DevOps — OpenSearch Setup Checklist

### 1. Provision OpenSearch Cluster

Minimum requirements:
- **Version**: 2.11.0+
- **ML plugin**: must be included (it is in the standard OpenSearch image)
- **Memory**: ≥4GB RAM per node (model loading is heavy — 2GB heap minimum)
- **Single node is fine** for staging; production should have 3+ nodes

If using **AWS OpenSearch Service**:
- Engine version: OpenSearch 2.11
- Instance type: `r6g.large.search` minimum (needs memory for ML)
- Enable ML features: not a separate toggle on AWS — just use a supported instance

If **self-hosted** (Docker/K8s), the local docker-compose is the reference:
```yaml
opensearch:
  image: opensearchproject/opensearch:2.11.0
  environment:
    - discovery.type=single-node          # for single node
    - plugins.security.disabled=true       # or configure TLS properly
    - OPENSEARCH_JAVA_OPTS=-Xms2g -Xmx2g
```

---

### 2. Set App Environment Variables

Provide these to the app deployment:

```bash
OPENSEARCH_HOST=https://<opensearch-host>:9200
OPENSEARCH_USERNAME=<username>
OPENSEARCH_PASSWORD=<password>
OPENSEARCH_INDEX_NAME=products-neural-search
OPENSEARCH_NEURAL_CACHE_TTL=3600
OPENSEARCH_DASHBOARDS_URL=https://<dashboards-host>:5601  # optional
```

---

### 3. Run One-Time Bootstrap (after app is deployed)

This is run **once** per environment. It registers the ML model, deploys it, creates pipelines, creates the index, and indexes all products:

```bash
npm run cli:prod -- bootstrap-neural-search
```

- Takes **10–30 minutes** on first run (model download from HuggingFace)
- Needs network access from the cluster to HuggingFace (`huggingface.co`) — **whitelist this if there's egress filtering**
- To rebuild from scratch: add `--cleanup` flag

If it was already partially set up and only pipelines/index need recreation:
```bash
npm run cli:prod -- setup-neural-search --skip-cluster-settings
```

---

### 4. Verify It Worked

```bash
# Cluster health
curl -u admin:pass https://<host>:9200/_cluster/health

# Model is deployed
curl -u admin:pass -X POST https://<host>:9200/_plugins/_ml/models/_search \
  -H 'Content-Type: application/json' \
  -d '{"query":{"match_all":{}}}'

# Index exists and has documents
curl -u admin:pass https://<host>:9200/products-neural-search/_count
```

---

### TL;DR for DevOps

1. Spin up OpenSearch 2.11+ with ≥4GB RAM, ML plugin enabled
2. Set 5 env vars on the app
3. Ensure outbound HTTPS to `huggingface.co` is allowed
4. Run `npm run cli:prod -- bootstrap-neural-search` once
5. Done — app auto-discovers the deployed model on startup

> DEVELOPER

cost for r6g.large.search

> AGENT

**r6g.large.search** — 2 vCPUs, 16 GB RAM (Graviton2)

| Pricing | Cost |
|---|---|
| On-demand | ~$0.167/hr → **~$122/month** |
| 1yr Reserved (no upfront) | ~$0.106/hr → **~$77/month** |
| 1yr Reserved (all upfront) | ~**$67/month** |

Prices vary by region (us-east-1 is typically cheapest).

**Note on sizing**: r6g.large may be overkill just for the ML model (`all-distilroberta-v1` is ~300MB). If budget is tight, `r6g.medium.search` (1 vCPU, 8GB) at ~$60/month on-demand could work for staging. Production with real load → stick with large or go xlarge.

Sources:
- [r6g.large.search pricing — Vantage](https://instances.vantage.sh/aws/opensearch/r6g.large.search)
- [Amazon OpenSearch Service Pricing](https://aws.amazon.com/opensearch-service/pricing/)

> DEVELOPER

can you summarize all data you found into  short agenda for the call

> AGENT

## Call Agenda — OpenSearch / Neural Search Setup

**1. What we're deploying** *(2 min)*
- Neural search feature using OpenSearch + HuggingFace sentence embeddings
- Hybrid search: 80% vector (semantic) + 20% keyword (BM25)
- REST API endpoints ready, CLI bootstrap command ready

**2. DevOps action items** *(5 min)*
- Provision AWS OpenSearch 2.11+ — `r6g.large.search` recommended (~$122/mo on-demand, ~$67/mo reserved)
- Ensure outbound HTTPS to `huggingface.co` is allowed (model download on first bootstrap)
- Set 5 env vars on app deployment: host, username, password, index name, cache TTL

**3. One-time bootstrap** *(3 min)*
- Run `npm run cli:prod -- bootstrap-neural-search` after deploy
- Takes 10–30 min on first run (model download + product indexing)
- Subsequent re-runs use `--cleanup` flag to rebuild from scratch

**4. Verification** *(2 min)*
- Cluster health check via curl
- Confirm model state = `DEPLOYED`
- Confirm product index has documents

**5. Questions / blockers** *(open)*
- Security config (TLS, auth) — currently disabled in local, needs decision for prod
- Reserved instance commitment — 1yr saves ~45%
- Staging vs prod sizing

> DEVELOPER

gimme it as file

> AGENT

`docs/features/neural-search/opensearch-devops-call-agenda.md`
