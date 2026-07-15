# SWESimBench v2 — Harbor task datasets

Canonical Harbor packages for the clean cohort eval, two conditions:

| Dataset | Tasks | Condition |
|---|---:|---|
| `withprofile-full/` | 2,723 | Agent may read `/sim/profile.md` (distilled developer style) |
| `noprofile-full/` | 2,723 | Same points, no profile file in the instruction |

Each leaf directory is one Harbor task:

```text
<task_id>/
  task.toml              # Harbor task metadata
  instruction.md         # agent brief
  environment/
    Dockerfile
    sim/
      history.md         # conversation so far ([DEVELOPER]/[AGENT]/…)
      profile.md         # withprofile only
  tests/
    gold.json            # hidden gold developer message (+ optional move)
    test.sh / verify.py  # Harbor verifier
```

Shared manifests at the dataset root:

- `_manifest.json` — `{task, dev, point_id}` for every task
- `_cohort_meta.json` — policy / cohort fingerprints and counts

## Run with Harbor

From a Harbor checkout (paths relative to this repo):

```bash
harbor run \
  --path pipelines/swesimbench-v2-harbor/datasets/withprofile-full \
  --agent <your-agent> \
  --model <your-model>
```

Same for `noprofile-full`. Aggregation helpers live one directory up (`aggregate_agentic.py`, `DEFERRED_PAID_WORK.md`).

## Notes

- Tasks predict the developer’s **next message** given prior turns on disk (agentic read of `history.md`), not a stuffed single-prompt transcript.
- Gold move labels may still be pending paid judge labeling; see `../DEFERRED_PAID_WORK.md`.
- Pipeline builders that emit these trees: `../build_agentic.py`, `../prepare.py`.
