# Deferred paid work

The canonical cohort, 100-point ATIF sample, and both Harbor datasets are rebuilt without external model calls. The following steps intentionally remain deferred because they spend judge/model API credits.

## 1. Label the full cohort and recompute chance

```bash
cd /data/swesimbench-v2-harbor
RUN_GOLD=1 python3 prepare.py
python3 compute_chance_line.py
python3 build_agentic.py --dataset noprofile-full --all --cond noprofile
python3 build_agentic.py --dataset withprofile-full --all --cond withprofile
```

`RUN_GOLD=1` makes one pinned Gemini judge classification per current evaluation point. Rebuilding the Harbor datasets afterward embeds those labels in each hidden `gold.json`. Use the micro or macro-developer chance value from `chance_line.json` explicitly when aggregating; `aggregate_agentic.py` no longer accepts the stale 0.489 default.

## 2. Label the 100-point ATIF sample

```bash
cd /data/swesimbench-v2-harbor
RUN_GOLD=1 N_POINTS=100 python3 build_atif_sample.py
python3 make_tasks_v2.py
```

The current sample is structurally complete but has `gold_move: null` by design. `make_tasks_v2.py` refuses to emit scored tasks until paid labels exist.

## 3. Run model evaluations

Run the standard Harbor job command for each desired model against:

- `/data/swesimbench-v2-harbor/datasets/noprofile-full`
- `/data/swesimbench-v2-harbor/datasets/withprofile-full`

Each task's verifier also invokes the pinned judge for the predicted message. Record the resulting job directory, then aggregate with the chance line from the same cohort:

```bash
python3 aggregate_agentic.py <job-dir> <dataset-dir> \
  --chance <value-from-chance_line.json> \
  --condition <noprofile-or-withprofile>
```

Do not aggregate the old `datasets/noprofile-pilot`; it is explicitly marked stale.
