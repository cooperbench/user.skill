[DEVELOPER]: seeds (∗/∗∗/∗∗∗ for p<0.05/0.01/0.001). [Image #1] Is this rendering error

[AGENT]: Not a rendering error. `App.~\ref{app:setup}` correctly resolves to "App. A" because `\label{app:setup}` is attached to the first appendix section (`\section{Experimental Setup Details}` at line 1057, immediately after `\appendix` at line 1045). LaTeX numbers appendix sections with letters, so it renders as **A**. The semicolon after "A" is just punctuation continuing the sentence ("…in App. A; on acceptance we release…"). Both the reference and the punctuation are intentional and correct.

[DEVELOPER]: what is this writing implying: " (∗/∗∗/∗∗∗ for p<0.05/0.01/0.001)"

[AGENT]: It's a legend for significance markers: a single asterisk (∗) marks results significant at p<0.05, two (∗∗) at p<0.01, and three (∗∗∗) at p<0.001. So when you see ∗/∗∗/∗∗∗ next to a number elsewhere in the paper, it tells you which p-value threshold the Wilcoxon signed-rank (Bonferroni-corrected) test cleared.

[DEVELOPER]: so it is a style ?

[AGENT]: Yes — it's a notational convention (a common style in stats/ML papers) for compactly annotating significance levels next to results, rather than writing out the p-value each time.

[DEVELOPER]: conclusion part is really short relative to intro. cut intro a bit, add back a bit to conclusion (which currently reads quite compact)

[AGENT]: Looking at the intro/conclusion balance now.

[AGENT]: Intro is 645 words, conclusion is 64 words. Big imbalance. Trimming intro's citation-heavy first paragraph and expanding the conclusion.

[AGENT]: End of main is now on page 10 — need to verify this is still within limits.

[AGENT]: Done. Build clean, no page regression (end-of-main stays on page 10, same as before). - Intro: 645 → 633 words. Compacted the citation cluster in paragraph 1 (merged the "variants / observability / flow-matching / LLM-reprogrammed / billion-scale" sub-categories into a single umbrella phrase, citations preserved). - Conclusion: 64 → 171 words. Added two sentences after the evidence summary: one reframing the contribution against optimization-side rescues (the 10.9% vs 54–80% contrast), one on the practical payoff ($R(\mathcal{D})$ as a pre-training go/no-go test + frozen-backbone deployment regime). Limitations expanded from one clause to two sentences (called out which backbones don't need the fix; added longer-horizon regimes alongside classification/anomaly detection).

[DEVELOPER]: recompile

[AGENT]: Build clean. 52 pages total, main content ends on page 10 (unchanged).

[DEVELOPER]: frame our problem identification as a contribution because we discover this problem shall we ?

[AGENT]: Contribution 1 already does this ("We identify *normalization-induced routing collapse*, an architectural failure mode … upstream of the optimization-induced collapses targeted by Switch/ST-MoE/ReMoE/Expert-Choice"), but the phrasing is modest. We could strengthen it by elevating "discovery of a new failure mode" to its own headline contribution (separate from the mechanism formalization in C2), and mirroring that framing in the abstract and the new conclusion paragraph — the tradeoff is that "we discovered a new problem" can read as overclaiming if reviewers feel the failure is a known MoE collapse in disguise (the eight controls + Table~\ref{tab:rescue} push back against this, but the framing has to be careful). Want me to (a) just upgrade the contribution-1 wording in the intro, or (b) propagate "problem discovery" framing through abstract → intro → conclusion?

[DEVELOPER]: the paths to the problem identification

[AGENT]: The discovery path has three legs in the paper: 1. **Natural-extension failure**: Standard MoE recipe (AdaMix pool + hidden-state softmax router + Switch load-balancing) on MOMENT+RevIN → entropy collapses to 0.000 in most unfrozen configs. *We didn't go looking for this; the natural baseline broke.* 2. **Rule-out via optimization rescues**: $11$ MoE-collapse fixes from the literature (load balancing, z-loss, ReLU routing, expert-choice, …) recover at most $10.9\%$ MSE — establishing that this is *not* the optimization-induced collapse those papers target. 3. **Causal localization**: Eight controls (RevIN ablation, BatchNorm/GroupNorm swaps, router-input interpolation, MOMENT-vs-Timer-XL, vision cross-modality, $(\mu,\sigma)$ re-injection, AdaMix-Raw, Residual-IA) converge on the normalizer as cause; the predictor $R(\mathcal{D})$ then generalizes the diagnosis pre-training. Should the contribution bullet be reframed around this *path* (failure → rule-out → localization), instead of just "we identify the failure mode"? That makes the discovery story explicit and pre-empts the "this is just standard MoE collapse" reviewer pushback. Want me to draft the reworked C1?

[DEVELOPER]: take a look at this paper @/Users/hungpq2412/Downloads/Vy_Nguyen_NeurIPS_2026\ \(35\).pdf

[AGENT]: Read it. It's structurally aligned with what you were asking about — it makes "Problem Formulation" an explicit, named contribution. Direct parallels to ours: | Their paper (CAC) | Our paper (RR-MoA) | |---|---| | **C1 Problem Formulation:** "unsupported commitment" — control failure ≠ knowledge failure; introduce *commit-abstain margin* | **C1 should be:** *normalization-induced routing collapse* — input failure ≠ optimization failure; introduce *signal-ratio* $R(\mathcal{D})$ | | **C2 Mechanistic Finding:** sparse CAC subset; "accumulate-yet-undercorrect" pattern | **C2:** MI decomposition + 8 causal controls localizing the normalizer | | **C3 Policy Improvement:** lightweight MLP on CAC activations | **C3:** RR-MoA / SR-MoA / Residual-IA⁺ | What they do well that we could adopt: 1. **Name the phenomenon, name the metric.** "Unsupported commitment" + "commit-abstain margin" are paired in C1. We have the phenomenon name ("normalization-induced routing collapse") but bury the metric ($R(\mathcal{D})$) in C2 — pulling it up into C1 ties discovery to measurement, mirroring their formulation. 2. **Sharp dichotomy framing.** "Control failure rather than knowledge failure" is one line and immediately separates them from the detection/abstention literature. Our analog: "router-input failure rather than router-optimization failure" — directly rules out Switch/ST-MoE/ReMoE/Expert-Choice. 3. **Conclusion echoes the framing.** Their conclusion opens with the […]