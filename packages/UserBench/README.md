# UserBench

**UserBench** is a Harbor eval for how well an agent can stand in for a real software engineer mid coding-agent session.

At each held-out turn, the agent reads the conversation so far (`/sim/history.md`) and writes the **single next developer message** to `/sim/answer.txt`. A judge labels that message into a 4-way **move** taxonomy; reward is **1.0 iff the predicted move matches the gold move** (move-match), else 0.0.

This package is the public **noprofile** cut: tasks ship history only. Developer style profiles are optional Harbor skills at job time (`--skill` / `agents[].skills`), not part of the task instruction.

## Scale (this revision)

| | |
|---|---|
| Developers | **62** (everyone with ≥10 eval points; 6 with &lt;10 dropped) |
| Tasks | **620** (exactly **10** per developer) |
| Condition | noprofile |

## Task selection rule

Same rule as `build_agentic.py --per-dev N`:

1. Start from the held-out eval points in the clean UserBench v2 cohort.
2. Keep developers with **≥10** points; drop the rest.
3. For each remaining developer, sort points by **`environment/history.md` byte size ascending** (equivalent to sorting by `len(context)` in the builder) and take the **first 10**.
4. Sessions may be shared across selected points for a developer. Ties break by legacy task directory name ascending.

## Task naming

Harbor requires `org/name` package refs. Tasks are published as:

```text
userbench/<username>__<hash>
```

Examples:

- GitHub: `userbench/winksaville__aad4a4f9`
- DataClaw (anonymized): `userbench/dc_004__05fe03e7`

Versioning is via Harbor tags only (e.g. `@v2`), not embedded in the task name.

## Keywords

`userbench` · `user-simulation` · `coding-agents` · `move-prediction` · `noprofile`

## Taxonomy / judging

Moves are one of: `approve` · `critical` · `directive` · `inquiry` (fault-first decision rule).

The task verifier classifies the agent’s predicted message (and gold `real` when `gold_move` is null) with a configurable judge (`SIMBENCH_JUDGE`, default Gemini). Published agentic numbers on [userbench.vercel.app/results](https://userbench.vercel.app/results) used **Composer 2.5** as the job-time judge on a **226-point / 10-developer** subset of the older package — those runs are **not** full-620 results.

## Train / held-out split

Each developer has a deep **train** history and a strictly later **held-out** set. Eval tasks are prediction points carved from held-out sessions (noprofile: history for the held conversation only).

## How to reference

| What | Ref |
|---|---|
| Dataset | `userbench/UserBench@v2` (also `latest`) |
| Task | `userbench/<username>__<hash>@v2` |
| Hub | https://hub.harborframework.com/datasets/userbench/UserBench |

```bash
harbor run -d userbench/UserBench@v2 -a <agent> -m <model>
harbor run -p userbench/winksaville__aad4a4f9@v2 -a <agent> -m <model>
```

## Links

- Site / dataset EDA: https://userbench.vercel.app
- Agentic results (10-dev / 226-point slice of the prior package): https://userbench.vercel.app/results
