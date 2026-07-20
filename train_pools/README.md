# UserBench leak-safe train pools

Full per-developer **train** corpora for the public UserBench eval
([`userbench/UserBench@v2`](https://hub.harborframework.com/datasets/userbench/UserBench):
62 developers × 10 held tasks).

## Leakage invariant (always)

For each developer, let `T* = min(held_sessions[].ts)` (manifest session timestamp).

A train session is included **only if**:

1. `session.ts < T*`, **and**
2. `max(turn.ts) < T*`

Never include train sessions that wall-clock-overlap or follow the earliest held
session. This is stricter than the cohort’s session-start split alone.

## Layout

```text
train_pools/
  README.md
  _registry.json
  <slug>/                 # e.g. gh_winksaville, dc_dc_000
    _meta.json            # T*, session index, turn totals
    sessions.jsonl.gz     # one JSON object per eligible session
                          # (large developers may use sessions_XXX.jsonl.gz shards)
```

Each sessions JSONL line:

```json
{"sid","ts","repo","n","max_turn_ts","turns":[{"role","text","ts"},...]}
```

`n` is the human-target user-turn count (same units as the clean cohort
`train_sessions[].n`). Texts are policy-scrubbed.

## Harbor Hub variants

This directory is the **full pool**. Harbor twins **subsample** at publish time:

| Hub package | Budget | Sampler |
|-------------|-------:|---------|
| `userbench/UserBench-train400` | 400 human-turns | `sqrt_two_stage` |
| *(future)* `UserBench-train1000` etc. | 1000+ | same pool + sampler |

Packaging writes contiguous **prefixes** (through the *k*-th human turn,
including intervening AGENT/TOOL/SYSTEM) into each task’s `/sim/train/`.
The zero-train baseline `userbench/UserBench@v2` is unchanged and does **not**
ship this pool.

## Stats (this export)

| | |
|--|--:|
| Developers | 62 |
| Eligible sessions | 10438 |
| Eligible human-turns | 94026 |

See `_registry.json` for per-developer `T*` and sizes.
