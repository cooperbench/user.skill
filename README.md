# User.skill

**Distilling real developers from their AI-coding trajectories into role-playable "user folders".**

Built on the [SWE-chat dataset](https://huggingface.co/datasets/SALT-NLP/SWE-chat) (5,851 real
coding sessions). For every user with ≥6 trajectories (99 users, 3,713 sessions), we distill a
folder of skills and persona files such that a coding agent (e.g. Claude Code) given that folder
can **role-play the user**: produce the requests, corrections, and pushback the real user would
have produced.

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

## Repo layout

```
.claude/skills/distill-user/    the distillation procedure (Claude Code skill)
.claude/skills/roleplay-user/   the role-play procedure (Claude Code skill)
scripts/prepare_data.py         SWE-chat -> per-user digests + holdout splits
scripts/distill.py              batch distillation driver (claude -p)
scripts/validate.py             next-message prediction + scoring (--ghost adds the baseline below)
scripts/ghost_predict.py        opencode ghost-text predictor as a baseline condition
scripts/report.py               HTML report from validation results
data/                           digests + holdout (gitignored; regenerable)
users/                          distilled user folders (committed)
results/                        validation outputs (committed)
```

## Data & ethics

Source data is the public SWE-chat dataset (ODC-BY, PII-redacted by the dataset authors).
User folders describe public GitHub activity; `user_id`s are public usernames already present
in the dataset. Honor SWE-chat removal requests by deleting the matching `users/<slug>/` folder.
