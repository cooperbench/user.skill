# UserSimBench v0 — move-fidelity eval for coding-agent user simulators

v0 turns `user.skill` from a *method* (distill real developers into role-playable folders)
into a *benchmark*: a cheap, reproducible, offline test of **how human-like a user simulator
is when driving a coding agent** — and, specifically, whether it falls into the *easy-mode*
failure (collapse into "looks good, continue") that prior work found for customer-service
user simulators on τ-bench.

## What it measures

For each held-out **user-action turn** (a real prompt/interrupt with ≥1 preceding agent turn),
we show the candidate simulator the **real conversation prefix** — so the agent's trajectory is
held fixed and any divergence is purely the simulator's — and ask it to write the developer's
next message. We label that message's conversational **move** with the repo's 7-move speech-act
classifier and compare to what the real developer did.

We score the **move**, not the exact words, because single-message text fidelity is *saturated*
(`results/ceiling.json`: a real held-out message scores realism 29.1 while the simulator scores
*higher*, 38.8; real-vs-real 2AFC discrimination ≈ 0.54 ≈ chance). One message barely identifies
a user; the signal is in *which move* they make and at what rate.

### Metrics (per model × condition)

| metric | meaning | direction |
|---|---|---|
| **MoveFid** | mean per-move Sørensen–Dice between the simulator's and the real developer's move distributions, ×100 (the USI "D-dimension" construction, applied to coding moves) | ↑ |
| **1−TVD** | histogram intersection of the two move distributions | ↑ |
| **CondAgree** | per-turn fraction where the simulator's move equals the real developer's move | ↑ |
| **approve%** / **critical%** | rate of `approve_proceed` vs `{pushback, interrupt, bug_report}` | compare to real |
| **Δapprove / Δcritical** | signed gap vs the real developer — **the easy-mode signal** | →0 |

### References (computed from the real labels, no API calls)

- **always_approve** — easy-mode positive control; should bottom out MoveFid and max approve%.
- **majority** — always the most common real move; CondAgree floor = p_max.
- **prior_sampler** — samples moves from the *real population distribution*. Its MoveFid is ≈100
  by construction, but its CondAgree ≈ Σpᵢ² (the **marginal ceiling**: the best you can do knowing
  only the move-mix, with no conditional skill). A simulator only demonstrates *conditional* skill
  by beating Σpᵢ².

The pair **(MoveFid, CondAgree vs Σpᵢ²)** is the headline: MoveFid alone is gameable by matching
the marginal (prior_sampler proves it), so a real simulator must also raise CondAgree above Σpᵢ²
*without* inflating approve% above the real rate.

## Models

Routed through OpenRouter so any model can be the simulator. v0 ships three that prior user-sim
work also evaluated, to test transfer from customer-service to coding:

| key | OpenRouter id | prior-work standing |
|---|---|---|
| `deepseek-v3.1` | `deepseek/deepseek-chat-v3.1` | Sim2Real-USI **best** simulator (USI 76.0) |
| `gpt-5` | `openai/gpt-5` | Sim2Real-USI GPT-5.x (USI ≈ 70.9); "stronger ≠ better simulator" |
| `gemini-3.1-pro` | `google/gemini-3.1-pro-preview` | OdysSim **most human-like** frontier model (HumT) |

Conditions: **distilled** (the user's own `users/<slug>/` folder pasted inline) vs **generic**
(no folder). The move classifier is `anthropic/claude-haiku-4.5` (the repo's `JUDGE_MODEL` family);
none of the three test models is Claude, so judge-family bias is minimal.

## Data

The 9 stratified validation users × their chronologically held-out sessions (54 prediction points).
Holdout is regenerated from a pinned SWE-chat parquet via `scripts/prepare_data.py`; the split is
identical to the committed `folder_v5*` run (54/54 gold messages match — no train/test leakage,
since the distilled folders never saw these sessions).

## Run

```bash
echo "OPENROUTER_API_KEY=sk-or-..." > .env       # gitignored
python3 scripts/prepare_data.py --swe-chat /path/to/SWE-chat
python3 bench/v0.py                               # cached/resumable -> bench/results/v0_summary.json
python3 bench/v0.py --limit 6                      # smoke test
```

Cost: ~700 OpenRouter calls (324 generations + ~378 move labels) ≈ a few US$.

## What v0 is not (yet)

Offline and request-side: it scores the *moves the simulated user produces*, holding the real
agent fixed. The **closed-loop** track — let the simulator drive a live Claude Code from the
reconstructed repo state and test whether task *outcomes* match real users (USI-style success
inflation) — is prototyped in `scripts/session_sim.py` + `scripts/session_compare.py` and is the
**v1** headline once an outcome grader (build/test pass) is added. A true per-turn **human
ceiling** for CondAgree needs multiple real continuations per point; v0 uses the marginal ceiling
Σpᵢ² as the principled reference.
