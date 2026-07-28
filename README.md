# UserBench (`cooperbench/user.skill`)

Harbor eval + train pools for measuring how well an agent can stand in for a real software engineer mid coding-agent session.

**Live site:** https://userbench.vercel.app · **Upstream:** `cooperbench/user.skill` (not AlienKevin/user-simulator)

| Hub package | Ref | Contents |
|---|---|---|
| Baseline | [`userbench/UserBench@v2`](https://hub.harborframework.com/datasets/userbench/UserBench) | 62 developers × 10 tasks (620), history only |
| Train twin | [`userbench/UserBench-train400@v2`](https://hub.harborframework.com/datasets/userbench/UserBench-train400) | Same 620 held tasks + leak-safe `/sim/train/` (400 human-turns) |

## Layout

```text
datasets/eval-620/     Public Harbor eval cut (620 tasks; short ids username__hash)
tasks/                 Symlink → datasets/eval-620 (for `harbor run --path tasks`)
train_pools/           Full T*-filtered train corpora per developer (Hub twins subsample)
packages/              Harbor dataset.toml + READMEs for UserBench / UserBench-train400
harbor/                Publish scripts, plans (train400, leakage audit)
train/                 Scrubbed train-split sessions as markdown (legacy / research)
data-pipelines/        Scrape, cohort, and task-build scripts (no private corpora)
  claude-crawl/        GitHub .claude/.codex discovery + harvest + cohort_policy
  swesimbench-v2/      Clean cohort builders, QC, Harbor emitters, templates
users/                 Distilled developer folders (persona/style/skills)
simulator/             Generic simulator skills (push-back, interrupt, …)
bench/                 CondAgree / next-action prediction harness + taxonomy
analysis/              Misprediction / homogeneity analysis + report source
scripts/               Distill / validate / report drivers (incl. ghost_predict.py baseline)
modal_app/             Modal training + serving for OSim models
web/                   Next.js site (userbench.vercel.app)
results/               Validation outputs
```

## Quick start

```bash
# Run the public 620-task Harbor eval
harbor run --path tasks --agent <agent> --model <model>

# Or pull from Hub
harbor run -d userbench/UserBench@v2 --agent <agent> --model <model>
harbor run -d userbench/UserBench-train400@v2 --agent <agent> --model <model>
```

## Task naming

Tasks use short ids `username__hash` (Hub: `userbench/<username>__<hash>`). GitHub developers drop the `gh_` prefix in the published name; DataClaw ids stay `dc_*`.

## Train pools vs Hub twins

`train_pools/` keeps **every** session/turn that passes the leakage rule
(`session.ts < T*` and `max(turn.ts) < T*`, `T* = min(held.session.ts)` per developer).
Harbor packages **subsample** at publish time (`sqrt_two_stage`); they do not ship the full pool.
See `harbor/plans/` and `train_pools/README.md`.

## Profiles vs tasks

Eval tasks contain conversation history only. Developer profiles belong on the **agent harness**
(`--skill` / `agents[].skills`) — do not bake a withprofile task twin.

## Website

Next.js site under `web/`, live at https://userbench.vercel.app. An older next-action leaderboard
is at `/v1`. The multi-label act annotator lives at
[`/annotator`](https://userbench.vercel.app/annotator) (dashboard: `/annotator/dashboard`), and the
misprediction report at `/misprediction`.

Compaction/continuation summaries (e.g. "This session is being continued…") are filtered out of
labeling targets at sample build time (`web/scripts/build_annotator_sample.py`).

---

# Distilling user folders

**Distilling real developers from their AI-coding trajectories into role-playable "user folders".**

Originally built on the [SWE-chat dataset](https://huggingface.co/datasets/SALT-NLP/SWE-chat)
(5,851 real coding sessions). For every user with ≥6 trajectories (99 users, 3,713 sessions), we
distill a folder of skills and persona files such that a coding agent (e.g. Claude Code) given that
folder can **role-play the user**: produce the requests, corrections, and pushback the real user
would have produced.

```
                ┌────────────────────┐
 SWE-chat   ──> │ 1. prepare_data.py │ ──> data/digests/<user>.json   (train sessions)
 parquet        │    split & digest  │ ──> data/holdout/<user>.json   (held-out test sessions)
                └────────────────────┘
                ┌────────────────────┐
 digests    ──> │ 2. distill.py      │ ──> users/<user>/
                │  /distill-user     │       USER.md PERSONA.md STYLE.md PREFERENCES.md
                │  (claude -p)       │       PROJECTS.md stats.json skills/*.md
                └────────────────────┘
                ┌────────────────────┐
 holdout    ──> │ 3. validate.py     │ ──> results/validation_results.json
 + folders      │  /roleplay-user    │ ──> results/report.html
                │  (claude -p)       │
                └────────────────────┘
```

## The user folder

`users/<user_slug>/` is structured like a Claude Code project folder for a persona:

| File | Contents |
|---|---|
| `USER.md` | Entry point: who this user is + how to role-play them (loaded first, like a CLAUDE.md) |
| `PERSONA.md` | Background, expertise level, domains, communication style |
| `STYLE.md` | How they literally type: length, language(s), casing, punctuation, verbatim example prompts |
| `PREFERENCES.md` | What they correct, reject, or praise; pacing; workflow habits (tests, commits, plans) |
| `PROJECTS.md` | The repos they work in, with goals and domain context |
| `skills/*.md` | Recurring behaviors distilled as skills (trigger → behavior), e.g. `terse-iterator.md` |
| `stats.json` | Quantitative fingerprint (intent/pushback distributions, prompt lengths, languages, repos) |

## Distillation pipeline (is itself a Claude Code skill)

`.claude/skills/distill-user/SKILL.md` defines the whole procedure. Run interactively:

```
/distill-user data/digests/<user>.json users/<user>/
```

or batch over all users (8-way parallel `claude -p`):

```bash
python3 scripts/prepare_data.py --swe-chat /path/to/SWE-chat        # build digests + holdout
python3 scripts/distill.py --all                                    # distill every eligible user
```

## Validation pipeline

**Task: held-out next-message prediction.** For each held-out session we pick prediction points
(real user turns ≥2). The role-play agent sees the real conversation up to that point and must
produce the user's next message. We compare to what the real user actually typed, under three
conditions:

| Condition | Folder given to role-play agent |
|---|---|
| `distilled` | the user's own distilled folder |
| `generic` | none (a generic developer) |
| `wrong` | a different user's folder (specificity control) |
| `ghost` | none — the opencode ghost-text predictor (`scripts/ghost_predict.py`), opt in with `--ghost` |

**Metrics** (per generated vs. real message):

1. **Semantic similarity** — sentence-transformers embedding cosine (`all-MiniLM-L6-v2`),
   with TF-IDF char/word n-gram cosine as a dependency-free fallback.
2. **LLM judge** — Claude scores content match and style/voice match (0–100) given the
   conversation context.
3. **Style fingerprints** — length ratio and language match (the cheapest tells: a Spanish-language
   one-liner user should not be simulated by 200-word English paragraphs).

The distillation is validated if `distilled` beats both `generic` (folder adds information) and
`wrong` (the information is user-specific, not just "how developers talk").

```bash
python3 scripts/validate.py --users 10 --points-per-session 3
python3 scripts/report.py            # results/report.html
```

**Not covered (future work):** response-side validation — re-running the coding agent from the
repo state at each point and comparing agent responses under simulated vs. real users requires
checkpointed repo states; SWE-chat's `checkpoints`/`commits` tables make this possible later.

## Data & ethics

Source streams include public SWE-chat (ODC-BY, PII-redacted by the dataset authors), Entire
checkpoint pushes, GitHub session dumps, and DataClaw donors. User folders describe public GitHub
activity; `user_id`s are public usernames already present in the source datasets. Honor removal
requests by deleting the matching `users/<slug>/` folder and related tasks.
