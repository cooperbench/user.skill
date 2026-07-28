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
`claude-crawl/reparse_dataclaw.py`. Rebuild committed crawl transcripts with
`claude-crawl/reparse_crawl.py`; its existing compact corpus is used only to
recover session ownership and repository metadata. The clean builder rejects legacy
300/400-word source records that do not declare `text_fidelity: full`.

The validated live-ref Entire rebuild is stored privately at
`s3://swe-sim-private-use1-999404134598/scrapes/entire-backfill/corpus-full-v4/`.
Hydrate it to `/data/entire-backfill/corpus-full-v4/`, or set
`ENTIRE_CORPUS_GLOB` to the hydrated `*.jsonl` path before running the clean
builder.
