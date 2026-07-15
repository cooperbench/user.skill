# SWESimBench v2 Harbor tasks

2,723 held-out prediction points as Harbor packages.

Each task directory:

```text
<task_id>/
  task.toml
  instruction.md
  environment/Dockerfile
  environment/sim/history.md
  tests/{gold.json,test.sh,verify.py}
```

Also: `_manifest.json`, `_cohort_meta.json`.

Developer profiles are **not** baked into tasks. Inject them as Harbor skills at job time:

```bash
harbor run --path tasks --agent <agent> --model <model> --skill path/to/profile-skill
```

Builders and cohort scripts: `../data-pipelines/swesimbench-v2/`.
