# UserBench-train400

Twin of the public UserBench eval with **leak-safe prior-session context**.

Same **620 held tasks** / **62 developers** as [`userbench/UserBench@v2`](https://hub.harborframework.com/datasets/userbench/UserBench) (history, gold, verifier unchanged). Each task additionally ships earlier sessions for that developer under `/sim/train/`, totaling **400 human user-turns** sampled with **sqrt two-stage**.

## What the agent sees

| Path | Role |
|------|------|
| `/sim/history.md` | Held conversation so far (identical to baseline) |
| `/sim/train/_index.json` | Index of packed prior sessions (ids, timestamps, repos, turn takes, paths) |
| `/sim/train/<sid>.md` | Contiguous **prefixes** of those sessions (same `> DEVELOPER` / `> AGENT` format) |
| `/sim/answer.txt` | Where the agent writes the next developer message |

The instruction is **count-agnostic**: it points at `/sim/train/` without hardcoding “400”. The turn budget is a publish-time sampler parameter.

## Leakage invariant

For each developer let `T* = min(held_sessions[].ts)` (manifest session timestamp).

Every packed train session satisfies:

1. `session.ts < T*`
2. `max(turn.ts) < T*`

This is stricter than the cohort’s session-start train/held split alone. Sessions that wall-clock-overlap the earliest held session are **never** included.

QC on this package: **0 / 620** tasks violate `max(turn.ts) < T*`.

## Sampling

1. Start from the developer’s **full leak-safe train pool** (all sessions/turns passing the T* rule).
2. Allocate exactly **400** human-turns with `sqrt_two_stage` (time-stratified session pick, then contiguous-prefix waterfill).
3. Emit prefixes through the *k*-th human turn (including intervening AGENT/TOOL/SYSTEM), with the same ~200-word-per-turn truncation as eval history.

The full pools (not just the 400-turn subsample) live in the GitHub repo under `train_pools/` so future Hub variants (e.g. **train1000**) can resample from the **same** T*-filtered corpus without changing the leakage rule.

## Scale

| | |
|---|---|
| Developers | **62** |
| Tasks | **620** (10 per developer; same selection as baseline) |
| Condition | `train400` |
| Train budget | 400 human-turns / developer (shared across that developer’s 10 tasks) |

## Task naming

Same short IDs as baseline (Harbor `org/name`):

```text
userbench/<username>__<hash>
```

Versioning is via Harbor tags on this package (e.g. `@v2`). Digests differ from the noprofile baseline; consume via the dataset ref below so baseline `UserBench@v2` stays pinned to zero-train digests.

## Keywords

`userbench` · `user-simulation` · `coding-agents` · `move-prediction` · `train400`

## How to reference

| What | Ref |
|---|---|
| This twin | `userbench/UserBench-train400@v2` (also `latest`) |
| Zero-train baseline | `userbench/UserBench@v2` |
| Hub | https://hub.harborframework.com/datasets/userbench/UserBench-train400 |
| Full train pools (GitHub) | https://github.com/AlienKevin/user-simulator/tree/main/train_pools |

```bash
harbor run -d userbench/UserBench-train400@v2 -a <agent> -m <model>
```

## Links

- Site / dataset EDA: https://userbench.vercel.app
- Baseline package README: sibling `UserBench` (noprofile, no `/sim/train/`)
