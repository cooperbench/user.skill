# SWESimBench v2 — Harbor task dataset

| Dataset | Tasks | Notes |
|---|---:|---|
| `eval/` | 2,723 | Held-out prediction points; conversation context on disk |

Developer profiles are **not** part of the task. Inject them at job time as Harbor skills (`--skill` / `agents[].skills`) in Agent Skills format.

Each leaf directory is one Harbor task:

```text
<task_id>/
  task.toml
  instruction.md
  environment/
    Dockerfile
    sim/
      history.md
  tests/
    gold.json
    test.sh / verify.py
```

Dataset root also has `_manifest.json` and `_cohort_meta.json`.

## Run with Harbor

```bash
harbor run \
  --path pipelines/swesimbench-v2-harbor/datasets/eval \
  --agent <your-agent> \
  --model <your-model>
```

Aggregation helpers live one directory up (`aggregate_agentic.py`, `DEFERRED_PAID_WORK.md`).
