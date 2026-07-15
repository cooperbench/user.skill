# Data pipelines

Scrape / discover / cohort / task-build scripts (no private corpora; those stay in S3).

| Dir | Role |
|---|---|
| `claude-crawl/` | GitHub `.claude` / `.codex` discovery, harvest, census, `cohort_policy.py` |
| `swesimbench-v2/` | Clean cohort build, QC, Harbor task emitters, templates, tests |

Harbor task packages live at repo-root `tasks/` (not here).

Many scripts still hardcode `/data/...` paths from the Seoul workstation — adjust before running elsewhere.
