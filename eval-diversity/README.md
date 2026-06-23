# eval-diversity

**Does user simulation *with user profiles* generate more diverse trajectories than a
generic (profile-less) simulator — without sacrificing realism?**

The claim has two parts, and they must travel together (diversity alone is gameable by
turning up temperature):

- **H1 — entropy:** profile-conditioned rollouts spread wider than the no-profile baseline,
  *and beat a raised-temperature baseline* (so the diversity is structured, not just noise).
- **H2 — distance-to-real:** the profile-generated distribution sits *closer to the real
  user distribution* than the baseline does (profiles recover real heterogeneity, not random
  entropy). Measured at the population level (MMD / Fréchet) against a pool of real messages.
- **Realism guard:** diversity goes up while the LLM realism score stays flat.

## Design

Fix the task, vary the *user* — so diversity is attributable to the persona, not the task.

| Arm | Simulator input | Runs per seed |
|---|---|---|
| `baseline-T` | generic "you are a developer" | K |
| `baseline-Thigh` | generic, higher temperature (see caveat) | K |
| `profile` | one `users/<slug>/` folder per run | K (one slug each) |

Every arm gets K runs per seed so **within-seed** diversity (the clean H1 test) is comparable.

## Run

```bash
# 1. roll out: simulator <-> agent loop, agent acts on the checked-out repo per seed
python3 eval-diversity/rollout.py \
    --seeds eval-diversity/seeds.example.json \
    --profiles me me-v2 --k 4
#    -> eval-diversity/rollouts.jsonl   (resumable; one line per rollout)

# 2. score
python3 eval-diversity/score.py --realism \
    --real-turns eval-diversity/real_turns.json
#    -> eval-diversity/diversity_results.json
```

`--realism` and `--real-turns` are optional (they cost extra LLM calls / need real data).

## Metrics (in score.py)

Diversity is measured on **three representations** of each rollout — words can vary while
patches stay identical (the agent washes out the persona), and only the patch metric catches
that:

| Representation | Metric |
|---|---|
| user turns (embedded) | **Vendi score** (= effective # of distinct trajectories) + mean pairwise cosine distance |
| final `git diff` (embedded) | Vendi + mean pairwise cosine distance |
| structure | Shannon entropy of the #turns distribution |

Plus optional `realism_mean` (standalone plausibility judge) and `distance_to_real`
(MMD always; Fréchet if `scipy` is installed).

## Seeds

`seeds.example.json` shows the format: `{id, repo, repo_dir, task}`. `repo_dir` must be a
**git checkout** at the base state — the driver `git reset --hard && git clean -fd` before
and after each rollout, so every rollout starts identical and the recorded `final_diff` is
exactly that rollout's contribution.

## `real_turns.json` (for H2)

A flat JSON list of real developer messages, e.g. extracted from `data/holdout/` once it is
regenerated (`scripts/prepare_data.py`). Used only as the reference cloud for MMD/Fréchet.

## Caveats / known limits

- **Temperature:** `claude -p` exposes no `--temperature`, so `baseline-Thigh` currently
  runs the *same* settings as `baseline-T` (it then measures the simulator's intrinsic
  run-to-run spread — a useful floor, but not a true high-temp control). For a real
  high-temp baseline, swap `simulate_user_turn` to an Anthropic SDK call with `temperature`.
- **Grounding for H2:** each real SWE-chat session is unique, so there is no "many real
  users, same task" — H2 is therefore a *population-level* distribution match, not per-seed.
- **Cost:** full rollouts run a real agent with tools per turn. Start with few seeds + small K.

## How this serves the project goal

This is the cheap upstream proxy for the synthetic-data goal: if profiles raise effective
diversity **and** move the distribution toward real **while realism holds**, it justifies the
expensive downstream test (distill a small coder on baseline-data vs profile-data, eval on
held-out real) and feeds the planned human pairwise annotation ("which set is more
diverse / realistic").
