# UserSimBench v0 — OdysSim (OSim) add-on findings

**Question.** OSim-8B was the **best specialized user simulator in prior work** (τ-USI 75.6, with
near-human reactivity D4≈93 on customer-service τ-bench). Does that specialization *transfer* to
driving a coding agent — i.e., is the purpose-built user-sim less "easy mode" than the frontier
models?

**Setup.** Hosted `cmu-lti/osim-8b` and `cmu-lti/osim-4b` (Qwen3-8B/4B, MIT) on Modal via vLLM
(OpenAI-compatible), using OSim's **native role-swapped format** (system = developer social-context
/ persona; the agent's turns as input; the model generates the next *developer* turn). Same 54
held-out points, same move classifier, same metrics as the frontier run.

## Leaderboard (OSim vs frontier)

Real developers: approve **24%**, critical **33%**; lucky-guess line (Σp²) **0.163**.

| simulator | MoveFid↑ | CondAgree↑ | approve% (24) | critical% (33) |
|---|---|---|---|---|
| **osim-8b** / generic | **56.5** | 0.208 | 9.4% | 9.4% |
| **osim-8b** / distilled | 55.8 | 0.222 | 42.6% | **16.7%** |
| osim-4b / generic | 55.1 | 0.111 | 24.1% | 11.1% |
| osim-4b / distilled | 48.7 | 0.259 | 57.4% | 13.0% |
| deepseek-v3.1 / distilled | 53.9 | 0.315 | 42.6% | 9.3% |
| gpt-5 / distilled | 45.5 | 0.278 | 38.9% | 3.7% |
| gemini-3.1-pro / distilled | 41.4 | **0.333** | 72.2% | 3.7% |
| gpt-5 / generic | 52.4 | 0.189 | 24.5% | 11.3% |
| _[ref] prior_sampler_ | _84.3_ | _0.185_ | _20.4%_ | _35.2%_ |

## Findings

**1. The specialized simulator wins move-mix fidelity.** OSim-8B tops every live model on MoveFid
(56.5 / 55.8) — its training objective (match the *distribution* of human behavior) transfers
directly. It produces the most realistic overall *blend* of moves.

**2. OSim is the least "easy mode" — its anti-sycophancy partially transfers.** OSim-8B/distilled is
**critical 16.7%** — the highest of any live model, ~½ of the real 33% rate, vs the frontier models'
3.7–11.3%. And OSim-8B doesn't over-approve: generic it approves just **9.4%** (it *asks questions*
40% of the time instead). So the human-like reactivity OSim was trained for (D4≈93 on τ-bench) does
carry into coding: it pushes back and probes where the frontier models rubber-stamp. This is the
clearest positive-transfer result in the suite.

**3. …but it loses on situational precision (CondAgree).** Every OSim run scores **below** the best
frontier-with-profile on right-move-right-place: OSim-8B 0.208–0.222, OSim-4B 0.111–0.259, vs
DeepSeek 0.315 / GPT-5 0.278 / Gemini 0.333. OSim has the right *temperament* but less coding-
specific *aim* — unsurprising, since it was trained on customer-service/social distributions, not
coding sessions. (OSim-4B/generic at 0.111 even falls **below** the 0.163 lucky-guess line — no
situational skill without a persona.)

**4. Size and persona.** 8B > 4B (higher, more stable MoveFid; 4B/generic CondAgree collapses). The
persona profile helps OSim-4B's situational accuracy a lot (0.111→0.259) and mainly raises OSim-8B's
*criticality* (9.4→16.7%) rather than its CondAgree.

## Bottom line — what transfers

User-sim ability splits into two transferable-but-separate skills:
- **Temperament** (human-like reactivity, *not* being a yes-man) — **OSim transfers this best**; the
  purpose-built simulator is the least easy-mode model tested.
- **Situational aim** (the right move at the right coding moment) — a **frontier model + the user's
  profile** transfers this best.

No single model has both. The best coding user-simulator would pair OSim's temperament with a
profile-conditioned frontier model's aim — or fine-tune a specialized model like OSim on real
coding sessions (e.g. SWE-chat) to add the coding-specific situational skill it currently lacks.

## Caveats

Same as v0 (54 moments, 9 users, one generation per cell, single Haiku move-classifier, request-
side only). Additionally: OSim is served zero-shot in its native role-swapped format with our
persona as the social-context system prompt — a different (model-appropriate) interface than the
frontier models' inline prompt, so cross-model gaps reflect interface + model together, not model
alone. Hosting: `osim-eval` on Modal (`kevinli020508`), Qwen3 thinking disabled, `<think>` stripped.
