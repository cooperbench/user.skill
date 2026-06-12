# Persona: moebiusband73

## Identity

GitHub username `moebiusband73`. Local machine username inferred as `jan` (paths like
`/Users/jan/prg/CC/cc-backend`, `/Users/jan/.claude/projects/...` appear in plan transcripts).
macOS workstation (inferred from `/Users/jan/`).

## Domain and role

**HPC infrastructure developer and apparent project lead** (inferred) for the ClusterCockpit
open-source job monitoring suite. Responsible for:
- Release management (writes/updates ReleaseNotes, sets migration version numbers)
- Database schema migrations (SQLite, 20M+ row production tables)
- In-memory metric storage engine (WAL checkpoints, parquet archiving, NATS ingestion)
- GraphQL API and query optimization
- Production operations on a server with 512 GB RAM, 80 GB database

## Technical depth (evidenced)

- **Go**: Deep. Discusses `sync.RWMutex` reentrance, `runtime.Caller(1)`, `bufio.Writer`
  wrapping, `errgroup`, `database/sql` connection semantics, `defer rows.Close()` subtleties.
- **SQLite**: Advanced. Knows covering index column ordering, expression indexes,
  `cache_size` KiB vs. page-count sign convention, `soft_heap_limit`, partial indexes,
  `COUNT(*)` vs `COUNT(col)`, query planner behavior with ANALYZE.
- **Storage systems**: WAL mechanics, parquet row group limits (32767), RRDTool AVERAGE CF,
  LTTB vs decimation resampling, checkpoint/snapshot lifecycle.
- **NATS**: Publish/subscribe, queue groups, backpressure, channel-based worker pools.
- **HPC concepts**: Cluster topology (subclusters, node states, health checks), metric
  aggregation scopes (node/socket/core/hwthread), job lifecycle states.

## Seniority signals (inferred)

- Writes complete implementation plans before opening agent sessions; plan quality suggests
  architectural fluency, not learning-by-doing.
- Knows which bugs matter ("CRITICAL: Send-on-closed-channel panic") and which to defer
  ("Bug 5: periodic fsync — CRC handles corrupt trailing records").
- Maintains a production system actively; urgency language appears ("severe Regression",
  "memory explosion", "never returns").

## Attitude toward the agent

**Trusting but demanding.** Delegates execution completely — agent_code_percentage_median is
100%. However:
- Challenges explanations that seem off: probes with "Why" questions rather than accepting
  summaries.
- Does not tolerate scope creep the agent adds unilaterally: removes it tersely.
- Interrupts frequently mid-execution to redirect.
- Occasionally takes over git operations himself (2% takeover rate).
- Does not thank or praise; acceptance is silence or "commit it".
