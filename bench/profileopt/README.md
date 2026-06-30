# SWESimBench

Evaluates **user simulators** — models that role-play the human software engineer in a coding-agent
chat — grounded in real [SWE-chat](https://huggingface.co/datasets/SALT-NLP/SWE-chat) sessions.

- Walkthrough + leaderboard: https://swesimbench.vercel.app
- Public trial data (every generation + move label): https://swesimbench.vercel.app/data

## Metric

**Next-action prediction accuracy** (`accuracy` for short): at each held-out moment, does the simulator
make the same 4-way move the real developer made next? The moves are `approve` / `critical` /
`directive` / `inquiry` (see `taxonomy.py`). Reported as a per-developer macro vs a chance baseline (the
per-developer move-mix collision Σp²). Beating the line means situational skill, not just matching the
developer's overall habits.

## Pipeline

| step | script | output |
|---|---|---|
| **split** | `split_data.py` | `splits.json` — train/val/test with non-overlapping **users AND repos** (connected components of the user↔repo graph), plus a per-developer time split (profile distilled from earlier sessions, scored on later held-out turns). |
| **run** | `run_eval.py` | `experiments/accuracy/{summary,manifest}.json` — for each test developer × held-out moment × simulator × {with-profile, no-profile}: generate the developer's next message, label its move with a single Haiku judge, score accuracy. |
| **analyze** | `analyze_categories.py` | `category_recall.json` — per-move agree-rate, ±profile. |
| | `analyze_verbosity.py` | `verbosity.json` + the confusion matrices. |
| | `mine_cases.py` | `cases.json` — per-developer deltas + the moments where the profile flipped the move. |
| | `ablation_style.py` | `ablation.json` — the real persona vs a content-free "be terse" prefix. |

Backends: OpenRouter (`../orouter.py`) for the general models; Modal (`../osim_backend.py` →
`../../modal_app/serve_osim.py`) for the OSim simulators.

## Taxonomy

`taxonomy.py` is the single source of truth for move classification (the 4-way taxonomy + the judge
prompt). It was chosen by maximizing cross-family inter-judge agreement — Cohen's κ across
Haiku-4.5 / Opus-4.8 / GPT-5: **0.68 (a 7-way taxonomy) → 0.80 (4-way)** — which is why a single cheap
Haiku judge is enough. Method + numbers: `FINDINGS_taxonomy.md`, `crossfamily_confirm.json`.

## Reproduce

The repo ships the prepared data the benchmark runs on: `data/holdout/` (held-out turns),
`data/digests/` (train sessions), and `users/<slug>/` (the distilled developer profiles). To rebuild
them from scratch from public SWE-chat, run `scripts/prepare_data.py` (chronological split into digests
+ holdout) then distill profiles with `scripts/distill.py` + `.claude/skills/distill-user/`.

```bash
pip install -r ../../requirements.txt
export OPENROUTER_API_KEY=...            # or a repo-root .env (OSim rows also need the Modal endpoint)

python split_data.py                     # -> splits.json
python run_eval.py                       # -> experiments/accuracy/summary.json (+ a raw cache, gitignored)
python analyze_categories.py
python analyze_verbosity.py
python mine_cases.py
python ablation_style.py
```

Prompts are reconstructable from the frozen test points + each developer's `users/<slug>/` folder via
`validate.build_prompt` / `osim_backend.build_osim_messages`. The bulky raw trial caches (every
generation + label) are not committed here; they are published openly on Vercel Blob (linked above).

## Layout

- `run_eval.py` — the eval runner.
- `taxonomy.py` — the 4-way move taxonomy + judge.
- `split_data.py` — the leak-free train/val/test split.
- `analyze_*.py`, `mine_cases.py`, `ablation_style.py` — the analyses behind the site.
- `experiments/accuracy/*.json` — the result artifacts.
- `points.py` — held-out point loading + message cleanup.
- `../osim_backend.py`, `../orouter.py`, `../../scripts/validate.py` — backends + prompt helpers.
- `../../scripts/prepare_data.py`, `../../scripts/distill.py` — build the held-out data + distilled profiles (upstream).
- `../../modal_app/` — Modal training + serving for the OSim simulator models.
