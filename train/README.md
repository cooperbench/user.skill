# SWESimBench v2 — train sessions

Scrubbed **train-split** coding-agent sessions for the Opus-era clean cohort
(68 developers, 10797 sessions).

Not Harbor tasks. Held-out prediction points live under `../tasks/`.

## Layout

```text
train/
  _manifest.json      # cohort summary
  _sessions.jsonl     # per-session metadata (source, repo, start_time, path, …)
  <developer_slug>/
    <session_id>.md   # pure conversation markdown
```

## File format

Session `.md` files match eval `history.md` turn formatting — no YAML frontmatter:

```markdown
> DEVELOPER

…

> AGENT

…
```

Look up `session_id` / `source` / `repo` / `start_time` in `_sessions.jsonl`.

Turns are **not** word-truncated (eval histories are, for context-window sizing).
Secrets are already scrubbed by the clean-cohort pipeline.

Policy: `swesimbench-v2-cohort-policy-2026-07-13.15`.
