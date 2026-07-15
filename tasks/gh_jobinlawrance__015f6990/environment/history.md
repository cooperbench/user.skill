> DEVELOPER

what's pending?

> TOOL

tool_use Bash
id: toolu_01Nhg8rn4znwZAXAftWA8Ets
```json
{
  "command": "git status --short && echo \"---\" && git log --oneline -10",
  "description": "Check git status and recent commits"
}
```

> TOOL

tool_result
id: toolu_01Nhg8rn4znwZAXAftWA8Ets
```
?? PONYTAIL-DEBT.md
?? graphify-out/
---
523765f Revert "build(brew): migrate deprecated brews -> homebrew_casks"
e79e823 build(brew): migrate deprecated brews -> homebrew_casks
0e550b1 ci(apt): retry .deb download to survive goreleaser asset churn
7a34cfe docs+build: tb->tinyraven CLI map, importable API collection, go install
d85cc35 style: gofmt local_test.go + datasource/registry.go
a24ab66 build(brew): install shell completions from tinyraven binary
5d2069e refactor: rebrand tr -> tinyraven; fix module path to ravencloak-org/tiny
b8524d5 refactor: rename CLI binary tr -> tinyraven (coreutils collision)
a14f442 feat(serve): SIGHUP reloads project registry without restart
80efab7 fix(local): make tr local stop/start visible + unhangable
```

> TOOL

tool_use Bash
id: toolu_01LDEdHqxtLejc4v2UZGhdqK
```json
{
  "command": "grep -n -A2 \"^#\\|status\\|Status\\|TODO\\|pending\" MILESTONE.md 2>/dev/null | head -80",
  "description": "Scan MILESTONE.md for phase status markers"
}
```

> TOOL

tool_result
id: toolu_01LDEdHqxtLejc4v2UZGhdqK
```
1:# TinyRaven — Development Milestones
2-
3-> Condensed milestone summary per phase. Each phase has a clear deliverable and success criteria.
--
8:## Phase 1 — MVP: Core Ingestion + Query
9-**Timeline:** Weeks 1–2  
10-**Deliverable:** Working `tr local` dev environment — events in, query results out
--
12:### Must Ship
13-- [x] Go HTTP server (`net/http` + `chi` router)
14-- [x] `POST /v0/events` — JSON / NDJSON ingestion
--
24:### Success Criteria
25-```bash
26-curl -X POST localhost:8000/v0/events?name=events \
--
29:# → 202 {"successful_rows":1,"quarantined_rows":0}  (ack-on-buffer ADR 0004; quarantine ADR 0018)
30-
31-curl "localhost:8000/v0/pipes/user_metrics.json?user_id=alice" \
--
33:# → [{"user_id":"alice","count":1}]
34-```
35-
--
38:## Phase 2 — API Publishing + Deployment
39-**Timeline:** Weeks 3–4  
40-**Deliverable:** Production-ready query API + deployable project via `tr deploy`
--
42:### Must Ship
43-- [x] Full SQL param type support: `String`, `DateTime`, `Int64`, `Float64`, `UUID`, `Boolean` (+ Int32/Date/DateTime64)
44-- [x] Auto-generated OpenAPI docs from pipe registry (ADR 0017, `/v0/openapi.json`)
--
55:### Success Criteria
56-```bash
57-tr deploy
58:# ✓ Validated 2 datasources, 3 pipes
59:# ✓ Applied 1 migration: ALTER TABLE events ADD COLUMN country String DEFAULT ''
60:# ✓ Published 3 endpoints
61-
62-curl localhost:8000/v0/metrics
63:# # HELP tinyraven_requests_total...
64:# tinyraven_requests_total{pipe="user_metrics"} 42
65-```
66- […]

> TOOL

tool_use Bash
id: toolu_01WTs3j843c6WnT32TNpytY5
```json
{
  "command": "grep -n \"^\\- \\[ \\]\" MILESTONE.md",
  "description": "List unchecked milestone items"
}
```

> TOOL

tool_result
id: toolu_01WTs3j843c6WnT32TNpytY5
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01M4A8w2F72XV4LFt29FMs4P
```json
{
  "command": "grep -n \"\\[ \\]\" MILESTONE.md",
  "description": "Find unchecked checkbox items anywhere in file"
}
```

> TOOL

tool_result
id: toolu_01M4A8w2F72XV4LFt29FMs4P
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01UvToL2xXq5QtheDEUEYoTQ
```json
{
  "command": "wc -l MILESTONE.md; tail -60 MILESTONE.md",
  "description": "Show tail of MILESTONE.md for current phase status"
}
```

> TOOL

tool_result
id: toolu_01UvToL2xXq5QtheDEUEYoTQ
```
     228 MILESTONE.md
---

## Phase 5 — Connectors + Community
**Timeline:** Weeks 9+  
**Deliverable:** Production readiness, ecosystem integrations

### Must Ship
> Connectors = ClickHouse-native engines declared in `.datasource`, not built services — see `docs/adr/0019-connectors-via-clickhouse-engines.md`. `tr deploy` creates the CH objects; ClickHouse does the pulling.
- [x] Kafka source: `.datasource` template for `ENGINE = Kafka(...)` + MV (CH runs the consumer)
- [x] S3 / files: `.datasource` templates for `s3()` / `url()` / `file()` + `ENGINE = S3`
- [x] PostgreSQL: `ENGINE = PostgreSQL(...)` / `postgresql()` table function, optional CDC via `MaterializedPostgreSQL`
- [x] BI tool compatibility: Metabase, Apache Superset, Grafana, DBeaver connect via ClickHouse HTTP interface
- [x] Integration test suite (end-to-end: ingest → materialize → query)
- [x] Load test benchmarks: target ≥ 10k events/s on single `t3.large`
- [x] Optional dashboard template — **separate repo** (`tinyraven/dashboard-template`, Next.js + Recharts). Core stays API-first with **no built-in dashboard** (CLAUDE.md); this is an external, opt-in starter that talks to the API, not a bundled feature.

### Success Criteria
```bash
# Kafka source in .datasource file (CH-native engine — ADR 0019)
ENGINE = Kafka
ENGINE_KAFKA_BROKER_LIST = kafka:9092
ENGINE_KAFKA_TOPIC_LIST = events
ENGINE_KAFKA_GROUP_NAME = tinyraven
ENGINE_KAFKA_FORMAT = JSONEachRow
# […]

> TOOL

tool_use Bash
id: toolu_01FnU7HGb7WAJa8XoBdBi8Ar
```json
{
  "command": "cat PONYTAIL-DEBT.md 2>/dev/null | head -100",
  "description": "Show ponytail debt ledger contents"
}
```

> TOOL

tool_result
id: toolu_01FnU7HGb7WAJa8XoBdBi8Ar
```
# Ponytail debt ledger

Deliberate simplifications marked with `ponytail:` comments, collected so a
deferral can't quietly become permanent. Regenerate: `grep -rnE '(#|//) ?ponytail:' .`

`no-trigger` = the comment names a ceiling but no upgrade path / revisit trigger —
those are the ones that silently rot (or are pure invariant notes; see the tail note).

## CLI / serve

- `cmd/tinyraven/serve.go:31` — global per-token rate limit. **ceiling:** single global default. **upgrade:** per-pipe `RATE_LIMIT` + shared httprate-redis store (ADR 0015/0031).
- `cmd/tinyraven/project.go:52` — mtime poll watcher (1s tick). **ceiling:** zero-dep poll. **upgrade:** fsnotify.

## clickhouse

- `internal/clickhouse/ddl.go:101` — MergeTree engine options. **ceiling:** only SORTING_KEY/PARTITION_KEY/TTL mapped. **upgrade:** add other MergeTree params when a datasource needs them.
- `internal/clickhouse/ddl.go:183` — S3 table auth. **ceiling:** static-key form only. **upgrade:** IAM roles / session tokens / named collections via deploy-time CH config.
- `internal/clickhouse/ddl.go:315` — query resource caps. **ceiling:** not baked onto CH user (stay per-query). **upgrade:** bake `SETTINGS … = N` on the user only if per-endpoint variance stops mattering.
- `internal/clickhouse/client.go:255` — `coerceValue` type coverage. **ceiling:** Int128/256, Decimal, Array/Map/Tuple pass through to the driver. **upgrade:** widen here when a real schema needs it.
- `internal/clickhouse/ddl.go:281` — db name backtick-quoted, […]

> AGENT

All 5 milestone phases checked off in `MILESTONE.md`. Real pending stuff:

**Uncommitted:**
- `PONYTAIL-DEBT.md` — untracked (44 debt markers logged, 23 no-trigger)
- `graphify-out/` — untracked

**Actual open work (from debt ledger, no upgrade trigger set — could rot):**
- `composeSQL` naive — single/linear pipes only, no multi-node support
- params tracked on endpoint node only, upstream nodes report empty
- `Schedule`/`COPY_SCHEDULE` parsed but not executed — no in-process scheduler, no `/v0/jobs` surface (gap #8)
- rate limit: global only, no per-pipe override, in-memory not Redis-backed (ADR 0015/0031)
- sqlproxy readonly via query flag, not server-side profile (ADR 0011)

Want me to commit the debt ledger, or dig into one of these gaps?