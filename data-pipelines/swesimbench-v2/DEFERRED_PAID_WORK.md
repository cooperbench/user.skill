# Deferred paid work

The canonical cohort, 100-point ATIF sample, and Harbor `tasks/` package are rebuilt without external model calls. The following steps intentionally remain deferred because they spend judge/model API credits.

## 1. Label the full cohort and recompute chance

```bash
cd /data/swesimbench-v2-harbor   # private cohort artifacts on Seoul
RUN_GOLD=1 python3 prepare.py
python3 compute_chance_line.py
# from this repo:
python3 data-pipelines/swesimbench-v2/build_agentic.py --dataset tasks --all --cond noprofile
# Profiles are harness-side (Harbor --skill), not a second task twin.
```

`RUN_GOLD=1` makes one pinned Gemini judge classification per current evaluation point. Rebuilding Harbor tasks afterward embeds those labels in each hidden `gold.json`. Use the micro or macro-developer chance value from `chance_line.json` explicitly when aggregating; `aggregate_agentic.py` no longer accepts the stale 0.489 default.

## 2. Label the 100-point ATIF sample

```bash
cd /data/swesimbench-v2-harbor
RUN_GOLD=1 N_POINTS=100 python3 build_atif_sample.py
python3 make_tasks_v2.py
```

The current sample is structurally complete but has `gold_move: null` by design. `make_tasks_v2.py` refuses to emit scored tasks until paid labels exist.

## 3. Run model evaluations

```bash
harbor run --path tasks --agent <agent> --model <model>
# optional developer profile as a Harbor skill:
#   --skill path/to/profile-skill-dir
```

Each task's verifier also invokes the pinned judge for the predicted message. Record the resulting job directory, then aggregate with the chance line from the same cohort:

```bash
python3 data-pipelines/swesimbench-v2/aggregate_agentic.py <job-dir> tasks \
  --chance <value-from-chance_line.json> \
  --condition noprofile
```
