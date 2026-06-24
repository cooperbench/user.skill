# UserSimBench v0 — findings

**Question.** Does user-simulator skill measured on customer-service tasks (τ-bench, in
Sim2Real-USI and OdysSim) transfer to *driving a real coding agent*? We score three frontier
models that prior work also evaluated, on 54 held-out user-action turns from 9 real SWE-chat
developers, holding the real agent trajectory fixed and comparing the **conversational move** the
simulator makes to the real developer's.

**Reference — real developers (n=54).** move mix: approve 24%, new_work 20%, refine_redirect 15%,
bug_report 13%, pushback 11%, interrupt 9%, question 6%. So **approve% = 0.241** and
**critical% (pushback+interrupt+bug_report) = 0.333** — real developers spend a *third* of their
turns telling the agent something is wrong. Marginal CondAgree ceiling Σpᵢ² = **0.163** (the best
per-turn move-agreement obtainable from the move-mix alone, with no conditional skill).

## Leaderboard

| simulator | MoveFid↑ | CondAgree↑ | conditional-skill (CondAgree−Σp²) | approve% (real .241) | critical% (real .333) |
|---|---|---|---|---|---|
| deepseek-v3.1 / distilled | **53.9** | 0.315 | **+0.152** | 0.426 | 0.093 |
| deepseek-v3.1 / generic | 39.8 | 0.189 | +0.026 | 0.491 | 0.057 |
| gpt-5 / distilled | 45.5 | 0.278 | +0.115 | 0.389 | 0.037 |
| gpt-5 / generic | 52.4 | 0.189 | +0.026 | **0.245** | 0.113 |
| gemini-3.1-pro / distilled | 41.4 | **0.333** | **+0.170** | 0.722 | 0.037 |
| gemini-3.1-pro / generic | 49.0 | 0.278 | +0.115 | 0.667 | 0.111 |
| _[ref] prior_sampler_ | _84.3_ | _0.185_ | _+0.022_ | _0.204_ | _0.352_ |
| _[ref] majority / always_approve_ | _4.9_ | _0.241_ | _+0.078_ | _1.0_ | _0.0_ |

## Findings

**1. The easy-mode gap replicates in coding — and is worse.** Every simulator over-approves and
under-criticises. Real developers are critical on **33%** of turns; the best simulator manages
**11%** (gpt-5/generic) and most land at **4–9%** — i.e. simulators reproduce only **11–34%** of
real critical feedback. Approval inflates from a real 24% to **39–72%**. This is exactly the
"easy mode" Sim2Real-USI found on τ-bench (over-cooperation, suppressed pushback), now confirmed
on real coding sessions, where the deficit is *larger* (τ-bench sims inflated agent success
~14pp; here critical feedback collapses by 2–9×). A coding agent evaluated against any of these
simulators would look far more competent than real developers would let it.

**2. Distribution-match (MoveFid) alone is gameable — you must read the pair.** `prior_sampler`,
which just samples from the real move-mix, **tops MoveFid at 84.3** while having essentially no
conditional skill (CondAgree 0.185 ≈ Σp² 0.163) and never knowing *when* to make a move. The
frontier models score MoveFid 40–54 — *below the dumb sampler* — because they skew the
distribution toward approval. So MoveFid rewards matching the marginal; real fidelity is the pair
**(CondAgree above Σp², approve%/critical% calibrated to real)**. v0's reference design makes this
visible rather than letting a single number hide it.

**3. Conditional skill is real, and the distilled persona folder is what delivers it.** Every
model beats the marginal ceiling Σp²=0.163, and the **distilled folder lifts CondAgree for all
three** (deepseek +0.126, gpt-5 +0.089, gemini +0.055) to ~0.28–0.33 — roughly **2× chance**. This
is `user.skill`'s core claim, now measured on *behaviour* (which move, when) rather than word
overlap, where the earlier single-message signal was saturated. The folder tells the simulator
*which* move the real developer would make here; that part works.

**4. Transfer from prior work is partial and selective.**
- **DeepSeek-V3.1** (Sim2Real-USI's *best* simulator) transfers as the most **personalizable** one:
  largest folder lift (+14.1 MoveFid, +0.126 CondAgree) and the top distilled MoveFid (53.9). Its
  prior-work strength — responsiveness to conditioning — carries over.
- **GPT-5** ("stronger ≠ better simulator") replicates: middling CondAgree, but notably its
  *uninstructed* approve rate (0.245) is almost perfectly calibrated to real (0.241) — yet it still
  under-produces critical feedback (0.113). Raw capability buys calibration, not criticality.
- **Gemini-3.1-Pro** (OdysSim's *most human-like* model on the HumT raw-text probe) **anti-transfers**:
  it is the **worst** easy-mode offender (approve 0.67–0.72, ~3× real, critical 0.037). Surface
  human-likeness ≠ behavioural fidelity — fluent agreeableness *is* the easy-mode failure. This is
  the sharpest transfer result: the model that looks most human in isolation behaves least like a
  real developer in the loop.

**5. The folder fixes *which* move, not *how often it approves*.** Persona distillation improves
conditional agreement but does **not** cure over-cooperation — and for gpt-5/gemini it *amplifies*
approval (Δapprove +0.14 / +0.06 vs generic). Knowing the user's voice and move-mix is not enough;
the sycophancy bias is orthogonal and needs an explicit move-rate/calibration mechanism (the repo's
v5 move-sampling pre-stage, or fine-tuning) on top of the folder.

## Bottom line

User-sim strength is **not** a single transferable scalar. "Best simulator on τ-bench" (DeepSeek)
transfers as *trainability*; "strongest model" (GPT-5) transfers as *calibration*; "most human-like
text" (Gemini) **negatively** predicts coding fidelity. And the failure mode prior work named on
customer-service — easy-mode over-cooperation — is **universal and larger** for coding-agent users.
v0 measures all of this cheaply and offline, and its (MoveFid, CondAgree−Σp², approve/critical
calibration) design resists the marginal-matching gaming that a single distribution score invites.

## Caveats

- **n=54** points, 9 users, single temperature-0.7 seed per cell → treat gaps < ~0.05 CondAgree as
  noise; the easy-mode effect (Δcritical −0.22 to −0.30) is far larger than that.
- **Move classifier** is Claude-Haiku-4.5 (the repo's instrument); none of the three test models is
  Claude, but the labeller is a single judge — a multi-judge check is a v0.1 item.
- **Request-side only.** v0 holds the real agent fixed; it does not yet measure whether a simulator
  *driving* a live agent changes task outcomes (the v1 closed-loop / success-inflation track).
- **A true per-turn human ceiling** for CondAgree needs multiple real continuations per point; v0
  uses Σpᵢ² as the principled "no-conditional-skill" reference instead.
