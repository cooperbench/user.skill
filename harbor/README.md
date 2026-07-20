# UserBench Harbor packaging

Generators and metadata for the public Harbor eval packages.

| Package | Hub | Notes |
|---------|-----|-------|
| `userbench/UserBench` | [Hub](https://hub.harborframework.com/datasets/userbench/UserBench) | Zero-train baseline (620 tasks) |
| `userbench/UserBench-train400` | [Hub](https://hub.harborframework.com/datasets/userbench/UserBench-train400) | Same 620 held tasks + `/sim/train/` (400 human-turns) |

## Full train pools (this repo)

`../train_pools/` holds the **complete leak-safe train corpus** per developer
(`session.ts < T*` and `max(turn.ts) < T*`, where `T* = min(held.session.ts)`).

Harbor twins **subsample** from that pool at publish time:

- **train400** — `sqrt_two_stage`, budget 400 (shipped)
- **train1000+** — same pool + sampler, larger budget (future)

Do not put the full pools into the baseline Hub package.

## Scripts

| Script | Role |
|--------|------|
| `scripts/prototype_train400_sampler.py` | Allocator + T* cutoff helpers |
| `scripts/export_train_pools.py` | Export full T*-filtered pools → `train_pools/` |
| `scripts/build_train400_tasks.py` | Sample budget N from pools → Harbor task dirs |

On the build host these currently read cohort artifacts under
`/data/swesimbench-v2-harbor/` (`clean_manifest.json`, `clean_sessions.jsonl`,
`datasets/eval-620`).

## Plans

See `plans/` for sampling design, leakage audit, and the count-agnostic instruction draft.
