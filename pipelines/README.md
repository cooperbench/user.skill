# Pipelines (synced from Seoul `/data`)

Scrape/cohort **scripts only** (no clones, corpus, clean_sessions, or generated datasets).

| Dir | Seoul source | Highlights |
|---|---|---|
| `claude-crawl/` | `/data/claude-crawl` | harvest/enumerate/treeprobe/census + `cohort_policy.py` |
| `entire-backfill/` | `/data/entire-backfill` | full-fidelity Entire checkpoint harvester (no message caps) |
| `swesimbench-v2-harbor/` | `/data/swesimbench-v2-harbor` | `build_clean_cohort.py`, QC, task builders, tests, `task_template/` |

Many scripts hardcode `/data/...` paths; adjust before running off Seoul.

Before refreshing v2, rebuild Entire shards with
`entire-backfill/harvest.py` and DataClaw with
`claude-crawl/reparse_dataclaw.py`. The clean builder rejects legacy
300/400-word source records that do not declare `text_fidelity: full`.
