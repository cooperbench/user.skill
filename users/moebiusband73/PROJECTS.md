# Projects: moebiusband73

## ClusterCockpit/cc-backend ★ dominant (94.1% of sessions)

**What it is:** Go backend for the ClusterCockpit HPC job monitoring suite. Ingests job events
and node state updates via REST and NATS, stores metric time-series in an in-memory store with
WAL/parquet persistence, serves a GraphQL API and web UI, backed by SQLite for job metadata.

**Production scale:** ~20M job rows in SQLite (80 GB), 5800+ checkpoint files (~22 GB),
512 GB RAM server, clusters named "fritz", "woody", multiple subclusters.

**User's recurring work:**
- **Metricstore internals**: WAL sharding, checkpoint correctness, parquet archiving row-group
  limits, memory explosion fixes, bufio buffering, bufferPool lifecycle.
- **SQLite optimization**: Covering index design, expression indexes, partial indexes, query
  planner behavior with/without ANALYZE, `cache_size`/`soft_heap_limit` tuning,
  `rows.Close()` memory leaks, context propagation for query timeout.
- **Stats/query performance**: `buildStatsQuery` hangs, GROUP BY index ordering,
  `COUNT(DISTINCT)` cost, request-scoped stats cache, histogram query parallelization.
- **NATS API**: Channel-based worker pools, health check parity with REST handler,
  configurable semaphores, shutdown correctness.
- **Config/schema evolution**: `ResampleConfig` policy-based rewrite, WAL as default format,
  interval field removal, JSON schema kept in sync with Go structs.
- **Release management**: ReleaseNotes updates, migration version bumps (saw versions 10–14),
  GoReleaser config, CLI flags (`-optimize-db`, `-cleanup-checkpoints`).
- **Resampling**: LTTB vs. AVERAGE vs. SIMPLE, per-user policy (low/medium/high), GraphQL
  `resampleAlgo` enum, policy-derived `MinimumPoints`.

**Key files referenced:**
- `pkg/metricstore/` — walCheckpoint.go, checkpoint.go, archive.go, lineprotocol.go,
  metricstore.go, query.go, level.go, config.go, parquetArchive.go
- `internal/repository/` — stats.go, jobQuery.go, job.go, node.go, dbConnection.go,
  migration.go, migrations/sqlite3/
- `internal/api/` — nats.go, rest.go, node.go
- `internal/graph/` — schema.resolvers.go, stats_cache.go
- `internal/config/` — config.go, schema.go
- `cmd/cc-backend/` — cli.go, main.go, server.go
- `web/frontend/src/` — Svelte components

## ClusterCockpit/cc-metric-store (5.9% of sessions)

**What it is:** Standalone metric time-series store (separate repo from cc-backend; cc-backend
embeds it as a package but the repo also stands alone).

**User's work here:**
- Integrating swaggo/swag for API docs.
- Updating README to match current implementation.
- Updating release notes.
- `go.mod` dependency bumps.

**Relationship to cc-backend:** cc-backend imports the metricstore package. User sometimes
updates both in the same session via `replace` directives in `go.mod`.
