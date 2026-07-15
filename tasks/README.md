# SWESimBench v2 Harbor tasks

1,525 held-out prediction points across 68 developers (Opus 4.6 era, ≥2026-02-05).

Sources: Entire (+ SWE-chat), GitHub `.claude`/`.codex` crawl, DataClaw.
SpecStory excluded. Policy `swesimbench-v2-cohort-policy-2026-07-13.15`.

Each task directory:

```text
<task_id>/
  task.toml
  instruction.md
  environment/Dockerfile
  environment/history.md
  tests/{gold.json,test.sh,verify.py}
```

Also: `_manifest.json`, `_cohort_meta.json`.

`history.md` turns use markdown blockquote role labels (`> DEVELOPER`, `> AGENT`, …)
with newline-preserving bodies (tables/fences stay intact). The Dockerfile copies
`history.md` into `/sim/history.md` at runtime.

Developer profiles are **not** baked into tasks. Inject them as Harbor skills at job time:

```bash
harbor run --path tasks --agent <agent> --model <model> --skill path/to/profile-skill
```

Builders and cohort scripts: `../data-pipelines/swesimbench-v2/`.
