---
name: plan-dump-kickoff
description: How Mathews-Tom opens implementation sessions — with a fully-formed markdown plan prefixed "Implement the following plan:" containing tables, phases, dependency graphs, commit strategy, and verification steps. Trigger when starting any new implementation task.
---

# Plan Dump Kickoff

When starting a new implementation session, Mathews-Tom pastes a pre-written plan prefixed with "Implement the following plan:". The plan is dense, structured markdown — section headers, implementation tables (script / algorithm / autograd / phase / complexity), per-task breakdowns, execution strategy (waves of parallel agents), commit strategy with message text, and verification steps. These run 500–1,800 words.

The plan frequently includes:
- A `## Context` block stating what's already merged and what branch is ready
- A table of scripts with columns: Script, Algorithm, Autograd, Phase, Complexity (~N lines)
- Per-script `### Task N` sections with architecture details, hyperparameters, section-by-section breakdown, and success criteria
- `## Execution Strategy` with wave structure ("Wave 1: 2 parallel agents", "Wave 2: 3 parallel agents")
- `## Commit Strategy` with exact commit messages and files per commit
- `## Verification` with pass/fail criteria and specific commands to run
- A closing note: "If this plan can be broken down into multiple independent tasks, consider using the TeamCreate tool to create a team and parallelize the work."

He uses this same format whether it's the opening of a session or a mid-session re-specification after exiting plan mode.

## Examples

**Example 1** (opening prompt, truncated):
```
Implement the following plan: # Plan: Implement 02-alignment/ and 03-systems/ scripts ## Context All 7 `01-foundations/` scripts are merged to `main`. The branch `feat/alignment-systems` is ready for the remaining 9 scripts across `02-alignment/` (4 scripts) and `03-systems/` (5 scripts). These span implementation phases 2-7. --- ## Scripts to Implement ### 02-alignment/ (4 scripts) | Script | Algorithm | Autograd | Phase | Complexity | |--------|-----------|----------|-------|------------| | `microlora.py` | Low-Rank Adaptation | Full Value class | 3 | ~350-400 lines | | `microdpo.py` | Direct Preference Optimization | Full Value class | 5 | ~350-400 lines | ...
```

**Example 2** (mid-session execution strategy section):
```
## Execution Strategy

Each wave uses parallel Task agents (general-purpose, Sonnet model) for implementation:

**Wave 1:** 2 parallel agents (microattention + microlora)
**Wave 2:** 3 parallel agents (microdpo + microkv + microquant)
**Wave 3:** 4 parallel agents (microppo + microflash + microbeam + micromoe)

After each wave: validate by running all new scripts, fix issues before proceeding to next wave.
```

**Example 3** (commit strategy section):
```
## Commit Strategy (4 sequential commits) ### Commit 1: `feat(foundations): implement GPT, RNN, embedding, RAG, diffusion, and VAE scripts` **Files:** 6 new scripts (microgpt.py, micrornn.py, microembedding.py, microrag.py, microdiffusion.py, microvae.py) **Rationale:** The implementation work — all new script files in one commit since they were developed as a coordinated batch. ### Commit 2: `docs: fix safe_log graph disconnection in autograd spec` **Files:** `docs/autograd-interface.md` ...
```
