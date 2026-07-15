# SWESimBench v2 — Harbor task dataset

Canonical Harbor packages for the clean cohort eval (**noprofile** only).

| Dataset | Tasks | Notes |
|---|---:|---|
| `noprofile-full/` | 2,723 | Conversation context on disk; no baked-in developer profile |

Developer profiles belong in the **agent harness** (e.g. Harbor `--skill` / `agents[].skills`), not in the task image. Do not reintroduce a `withprofile-*` task twin for the same points.

Each leaf directory is one Harbor task:

```text
<task_id>/
  task.toml
  instruction.md
  environment/
    Dockerfile
    sim/
      history.md         # conversation so far ([DEVELOPER]/[AGENT]/…)
  tests/
    gold.json
    test.sh / verify.py
```

Dataset root also has `_manifest.json` and `_cohort_meta.json`.

## Run with Harbor

```bash
harbor run \
  --path pipelines/swesimbench-v2-harbor/datasets/noprofile-full \
  --agent <your-agent> \
  --model <your-model>
```

To supply a developer profile dynamically, inject it as a Harbor skill at job/trial time (see Harbor `--skill` / `environment.skills_dir`), rather than baking `/sim/profile.md` into the task.

Aggregation helpers live one directory up (`aggregate_agentic.py`, `DEFERRED_PAID_WORK.md`).
