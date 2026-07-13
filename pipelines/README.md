# Pipelines (synced from Seoul `/data`)

Scrape/cohort **scripts only** (no clones, corpus, clean_sessions, or generated datasets).

| Dir | Seoul source | Highlights |
|---|---|---|
| `claude-crawl/` | `/data/claude-crawl` | harvest/enumerate/treeprobe/census + `cohort_policy.py` |
| `swesimbench-v2-harbor/` | `/data/swesimbench-v2-harbor` | `build_clean_cohort.py`, QC, task builders, tests, `task_template/` |

Many scripts hardcode `/data/...` paths; adjust before running off Seoul.
