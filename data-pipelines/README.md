# Data pipelines

Scrape / discover / cohort / task-build scripts (no private corpora; those stay in S3).

| Dir | Role |
|---|---|
| `claude-crawl/` | GitHub `.claude` / `.codex` discovery, harvest, census, `cohort_policy.py` |
| `swesimbench-v2/` | Clean cohort build, QC, Harbor task emitters, templates, tests |

Public UserBench Harbor tasks live at repo-root `datasets/eval-620/` (`tasks/` symlink). Full train pools at `train_pools/`.

Many scripts still hardcode `/data/...` paths from the Seoul workstation — adjust before running elsewhere.

| `swesimbench-v2/pii_redaction/` | Joe-aligned Presidio + TruffleHog post-pass for release scrubbing |
| `swesimbench-v2/meta/pii_scrub_*.json` | Small scrub verify/report summaries (not full corpora) |
