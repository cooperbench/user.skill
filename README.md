# User.skill / SWESimBench

Role-playable developer profiles + Harbor eval tasks for simulating real software engineers from public coding-agent traces.

**Branch:** `kevin` · **Live site:** https://swesimbench.vercel.app

## Layout

```text
tasks/                 Harbor eval packages (2,723 held-out prediction points)
data-pipelines/        Scrape, cohort, and task-build scripts (no private corpora)
  claude-crawl/        GitHub .claude/.codex discovery + harvest + cohort_policy
  swesimbench-v2/      Clean cohort builders, QC, Harbor emitters, templates
users/                 Distilled developer folders (persona/style/skills) — migrating to Agent Skills
simulator/             Generic simulator skills (push-back, interrupt, …)
bench/                 CondAgree / next-action prediction harness + taxonomy
scripts/               Distill / validate / report drivers
modal_app/             Modal training + serving for OSim models
results/               Legacy validation outputs (v0-era demos)
```

Private session corpora, digests, and holdout splits are **not** in git (S3 / Seoul `/data`). See `AGENTS.md`.

## Quick start

```bash
# Run Harbor eval (profiles optional, as skills)
harbor run --path tasks --agent <agent> --model <model>

# Distill / validate user folders (needs hydrated data/)
python3 scripts/prepare_data.py --swe-chat /path/to/SWE-chat
python3 scripts/distill.py --all
python3 scripts/validate.py --users 10
```

## Profiles vs tasks

Eval tasks contain conversation history only. Developer profiles belong on the **agent harness** and will be Agent Skills–compatible (`SKILL.md` dirs). Inject with Harbor `--skill` / `agents[].skills` — do not bake a withprofile task twin.

## Still missing / next cleanup

| Gap | Why |
|---|---|
| `profiles/` (or skill-format `users/`) | Explicit Agent Skills packaging of per-developer profiles |
| `docs/` | Park `FINDINGS.md`, taxonomy notes, design write-ups out of root |
| `jobs/` | Checked-in Harbor job YAMLs (±profile skill injections) |
| Entire scrape pipeline | Only `claude-crawl` is here; ClickHouse/Entire harvest still Seoul-local (`/data/entire-backfill`) |
| Slim `results/` | Archive or drop v0 demo HTML/JSON once CondAgree blob is canonical |
| Path portability | Several `data-pipelines/` scripts still hardcode `/data/...` |

## Data & ethics

Source streams include public SWE-chat (ODC-BY), Entire checkpoint pushes, GitHub session dumps, and DataClaw donors. Honor removal requests by deleting matching `users/<slug>/` and related tasks.
