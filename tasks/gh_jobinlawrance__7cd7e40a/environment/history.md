> DEVELOPER

what's pending?

> TOOL

tool_use Bash
id: toolu_01NjqeWmVX2cimTVhctKFJoL
```json
{
  "command": "git log --oneline -5 2>/dev/null; echo \"---FILES---\"; ls -la; echo \"---STATUS---\"; git status --short",
  "description": "Check repo state and pending work"
}
```

> TOOL

tool_result
id: toolu_01NjqeWmVX2cimTVhctKFJoL
```
06dd040 fix(#71): tr deploy bootstraps on default DB; drop 100% parity claims
d7faf7a site: real p50/p95/p99 + throughput on benchmark; drop illustrative Tinybird
3f6293a fix(site): live dashboard on Bklit charts (Bar + AreaChart), verified locally
d55b596 fix(site): live dashboard on Recharts (visx BarYAxis overflowed)
fbbcf24 feat: live dashboard on /use-cases + CORS on API
---FILES---
total 16512
drwxr-xr-x@  44 jobinlawrance  staff     1408 Jul  1 21:02 .
drwxr-xr-x  251 jobinlawrance  staff     8032 Jun 29 08:36 ..
drwxr-x---    4 jobinlawrance  staff      128 Jun 29 11:55 .claude
-rw-r--r--@   1 jobinlawrance  staff      907 Jun 30 15:32 .coderabbit.yaml
-rw-r--r--@   1 jobinlawrance  staff     6148 Jul  1 19:15 .DS_Store
drwxr-xr-x    7 jobinlawrance  staff      224 Jun 29 10:12 .entire
-rw-r--r--@   1 jobinlawrance  staff      658 Jun 30 15:32 .env.example
drwxr-xr-x@  18 jobinlawrance  staff      576 Jul  2 00:15 .git
drwxr-xr-x@   4 jobinlawrance  staff      128 Jun 30 15:32 .github
-rw-r--r--@   1 jobinlawrance  staff      195 Jun 30 15:32 .gitignore
-rw-r--r--@   1 jobinlawrance  staff     8650 Jun 30 16:03 .goreleaser.yaml
drwxr-xr-x@   2 jobinlawrance  staff       64 Jun 29 08:36 .mcp_data
drwxr-xr-x@   6 jobinlawrance  staff      192 Jul  1 22:32 .serena
-rw-r--r--@   1 jobinlawrance  staff     1996 Jun 30 15:32 app.json
-rw-r--r--@   1 jobinlawrance  staff     1702 Jun 30 15:32 app.yaml
-rw-r--r--@   1 jobinlawrance  staff […]

> TOOL

tool_use Bash
id: toolu_01Eikaz3hKgTjGBtW4yyxpXS
```json
{
  "command": "gh pr list --state open 2>/dev/null | head -20; echo \"---ISSUES---\"; gh issue list --state open --limit 30 2>/dev/null | head -40",
  "description": "List open PRs and issues"
}
```

> TOOL

tool_result
id: toolu_01Eikaz3hKgTjGBtW4yyxpXS
```
---ISSUES---
70	OPEN	📌 Status & Roadmap (read me first) — pre-alpha, v0.3.2	documentation	2026-06-30T20:49:35Z
68	OPEN	Multi-node tr HA (out of MVP scope — tracking)	area:infra	2026-06-29T05:57:18Z
67	OPEN	API docs UI at /tr/v1/docs (embedded, off by default)	area:api	2026-06-29T05:54:38Z
66	OPEN	Per-pipe query caching: CACHE_TTL directive → CH query_cache	area:query	2026-06-29T05:51:32Z
65	OPEN	API versioning: /v0 frozen mirror, /tr/v1 for native endpoints	area:api	2026-06-29T05:45:30Z
64	OPEN	Resource-token materialization on tr deploy	area:cli	2026-06-29T05:52:56Z
63	OPEN	JWT browser tokens (HS256) for direct browser pipe access	area:api	2026-06-29T05:38:01Z
62	OPEN	Pipe response format + limits + pagination	area:query	2026-06-29T05:40:06Z
61	OPEN	.pipe template control flow ({% if/for %}) via expr-lang/expr	area:query	2026-06-29T05:03:43Z
60	OPEN	ClickHouse connection: managed (spin) vs BYO + masked status	area:cli	2026-06-29T04:27:07Z
59	OPEN	Per-pipe query result caching via ClickHouse query_cache	area:query	2026-06-29T04:27:05Z
58	OPEN	Opt-in --auto-schema (infer datasource from first event)	area:ingestion	2026-06-29T04:19:59Z
57	OPEN	tr branch create --with-sample N (fixture load)	area:cli	2026-06-29T04:17:09Z
56	OPEN	tr branch rm / prune — explicit branch DB lifecycle	area:cli	2026-06-29T04:17:07Z
55	OPEN	Bootstrap admin token on first init	area:cli	2026-06-29T04:12:19Z
54	OPEN	Disk WAL for at-least-once ingestion	area:ingestion	2026-06-29T04:09:31Z
53	OPEN	Full Tinybird template […]

> TOOL

tool_use Bash
id: toolu_01N21sy1G5aVD1w14j6wdHGd
```json
{
  "command": "gh issue list --state open --limit 100 2>/dev/null | wc -l; echo \"---ROADMAP #70---\"; gh issue view 70 2>/dev/null | head -80",
  "description": "Count issues and read roadmap"
}
```

> TOOL

tool_result
id: toolu_01N21sy1G5aVD1w14j6wdHGd
```
      69
---ROADMAP #70---
title:	📌 Status & Roadmap (read me first) — pre-alpha, v0.3.2
state:	OPEN
author:	jobinlawrance (Jobin Lawrance)
labels:	documentation
comments:	0
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	70
--
**TinyRaven is pre-alpha** (current release: v0.3.2). Open-source, self-hosted, drop-in Tinybird-compatible analytics backend in Go over OSS ClickHouse. Apache 2.0, permanent (ADR 0022). This issue is the single source of truth for "what works / what doesn't / what's next" — pinned so you don't have to dig.

## Works today
- **Ingest:** `POST /v0/events` (NDJSON, batched via in-process Gatherer → ClickHouse), per-row validation + quarantine.
- **Query:** `GET /v0/pipes/{name}.{json,csv,ndjson}` with `{{Type(param, default)}}` templating + `{% if/elif/else %}` control flow; params bound as ClickHouse query parameters (no string interpolation).
- **Ad-hoc SQL:** `GET/POST /v0/sql` (read-only, ADMIN).
- **Introspection:** `GET /v0/datasources`, `/v0/datasources/{name}`, `/v0/pipes`, `/v0/pipes/{name}`.
- **Auth:** scoped tokens (`tr token create`; ADMIN / `APPEND:<ds>` / `READ:<pipe>`).
- **Workflow:** git-versioned `.datasource`/`.pipe` files, `tr deploy` (with `--check` dry-run, `--branch`), branching = one ClickHouse DB per git branch, materialized views, breaking-migration path (shadow → backfill → `EXCHANGE TABLES`).
- **Ops:** Prometheus metrics, `/health` + `/ready`, `pipe_stats` observability table, per-pipe rate limiting, OpenAPI docs UI (`TR_DOCS_ENABLED`). […]

> AGENT

No open PRs. **68 open issues** (v0.3.2 pre-alpha). Repo way past "pre-code" — CLAUDE.md stale.

**Pending by area:**

**API (`/v0` parity + native)**
- #67 API docs UI at `/tr/v1/docs` (embedded, off default)
- #65 API versioning: `/v0` frozen mirror + `/tr/v1` native
- #63 JWT browser tokens (HS256) for direct browser pipe access
- #62 Pipe response format + limits + pagination

**Query engine**
- #66 / #59 Per-pipe query caching → CH `query_cache` (dupe-ish, two issues)
- #61 `.pipe` template flow (`{% if/for %}`) via expr-lang/expr

**CLI (`tr`)**
- #64 Resource-token materialization on `tr deploy`
- #60 ClickHouse conn: managed (spin) vs BYO + masked status
- #57 `tr branch create --with-sample N` fixture load
- #56 `tr branch rm / prune` lifecycle
- #55 Bootstrap admin token on first run

**Ingestion**
- #58 Opt-in `--auto-schema` (infer datasource)
- #54 Disk WAL at-least-once ingestion

**Infra (out of MVP)**
- #68 Multi-node HA (tracking only)

Rest (#40–53) compressed — mostly deploy targets (DO/railway/heroku/k8s), BI connectors, migrate-from-Tinybird docs.

**Roadmap "Next" (#70):** close `/v0` parity gaps (copy pipes, list/CRUD, output formats) → replication/multi-node → 1.0 hardening.

Want me pick highest-leverage next task, or drill one area?