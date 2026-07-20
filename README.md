# UserBench (`cooperbench/user.skill`)

Harbor eval + train pools for measuring how well an agent can stand in for a real software engineer mid coding-agent session.

**Branch:** `kevin` · **Live site:** https://userbench.vercel.app · **Upstream:** `cooperbench/user.skill` (not AlienKevin/user-simulator)

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
scripts/               Distill / validate / report drivers
modal_app/             Modal training + serving for OSim models
results/               Legacy validation outputs (v0-era demos)
```

Website source lives on branch **`benchmark-website`** (`web/`).

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

## Data & ethics

Source streams include public SWE-chat (ODC-BY), Entire checkpoint pushes, GitHub session dumps,
and DataClaw donors. Honor removal requests by deleting matching `users/<slug>/` and related tasks.
