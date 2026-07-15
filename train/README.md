# SWESimBench v2 — train sessions

Scrubbed **train-split** coding-agent sessions for the Opus-era clean cohort
(68 developers, 10797 sessions).

Not Harbor tasks. Held-out prediction points live under `../tasks/`.

## Layout

```text
train/
  _manifest.json
  <developer_slug>/
    <session_id>.md
```

## File format

YAML frontmatter (`session_id`, `developer`, `source`, `repo`, `start_time`, …)
then the full conversation in the same markdown turn format as eval `history.md`:

```markdown
> DEVELOPER

…

> AGENT

…
```

Turns are **not** word-truncated (eval histories are, for context-window sizing).
Secrets are already scrubbed by the clean-cohort pipeline.

Policy: `swesimbench-v2-cohort-policy-2026-07-13.15`.
