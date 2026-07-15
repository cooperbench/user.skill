> DEVELOPER

we recently reorganise 4.2. Should we call subsection 4.2.1, 4.2.2 etc ?

> DEVELOPER

we recently reorganise 4.2. Should we call subsection 4.2.1, 4.2.2 etc ? what is neurips recommended or required

> AGENT

Let me verify via the official NeurIPS 2026 handbook rather than rely on memory.

> AGENT

NeurIPS 2026 has no rule either way; both forms are explicitly legal. The official template (page 2 of the formatting instructions) demonstrates all three options side-by-side in Section 3 "Headings": numbered first/second/third-level, plus the inline `\paragraph` form. They're shown as equivalent stylistic choices, not a hierarchy of preference. There's no requirement to use or avoid `4.2.1`-style numbering. **Practical recommendation: keep `\subsubsection*` (your current state).** Numbered subsubsections are unusual in NeurIPS papers — most use either the unnumbered starred form or `\paragraph{}` for inline bold runs (which you already use at lines 1061/1063/1065/1076 for "Backbone specifications.", "Training hyperparameters.", etc.). Switching to numbered `4.2.1–4.2.4` would: - add visual clutter and a small amount of vertical space (you're already over 9 pages per `todo.md`) - only pay off if you need to `\ref` them from elsewhere in the body — `\subsubsection*` can't be cross-referenced Switch to numbered only if you find yourself wanting to write "see §4.2.3"; otherwise the current `\subsubsection*` is the right call. If you want to reclaim a bit more space, downgrade them to `\paragraph{Diagnosis.}` etc. — that's the most compact option and matches the rest of §4. Sources: - [Formatting Instructions For NeurIPS 2026 (PDF, p.2 §3 Headings)](http://web.uvic.ca/~nmehta/incentives_and_machine_learning_spring2026/neurips_2026.pdf) - […]

> DEVELOPER

We exceeded strictly 9 pages Intro is quite long, even spill over results

> AGENT

Let me look at the current intro to see what's tightenable.

> AGENT

Let me check the current build to see exactly where the page-9 boundary lands.

> AGENT

Let me look at §4.2 prose density and apply cuts.

> DEVELOPER

cuts should not reduce our intext citations

> AGENT

Understood — cuts will preserve every `\citep`/`\citet`. I'll compress prose only (joining sentences, dropping redundant adjectives/parentheticals) while keeping all citation keys.

> AGENT

Now compress §4.2 prose without dropping any citation.

> AGENT

Now rebuild and check pagination.

> AGENT

Now compress the §4.2 closing paragraphs.

> AGENT

The remaining 18 lines on page 10 need to migrate to page 9. Page 9 holds two tables (causal controls + baselines). Cleanest move: relocate Table 3 (causal controls) to the appendix and replace with a one-sentence prose summary, keeping the same `\ref{tab:causal_controls}` so all in-text references resolve.

> AGENT

Now insert the moved Table 3 (with its label) at the start of the routing-ablations appendix.

> AGENT

Body now fits on 9 pages. Verifying claim-numerics still pass and no refs broken.

> AGENT

Body is now within the 9-page NeurIPS limit (body content + start of references on page 9; references don't count toward the limit). All 107 verify.py checks still pass; no broken refs. **Changes made (citations preserved everywhere):** - **Intro** (§1): collapsed the 5-LLM-as-forecaster catalog into one sentence with the same `\citep` keys; tightened paragraphs 2–4 (instance-norm, AdaMix collapse, Moirai-doesn't-collapse); compressed the 3 contributions bullets. - **Method** (§3): trimmed prose around adapter definition, gating equation, and expert pool. - **Results** (§4.2): tightened all four subsubsections — diagnosis prose, Frozen Paradox, Headline Numbers, DLinear-gap closing, cross-backbone summary. - **Conclusion** (§5): minor tightening. - **Table 3 (causal controls)** moved from §4.2 to App.~\ref{app:routing_ablations} (now also labeled `app:causal_controls`); replaced in body with one-sentence summary that still references all eight controls and the table label, so every existing `\ref{tab:causal_controls}` still resolves. PDF: 50 pages total, body ends on page 9.

> DEVELOPER

let's quantitatively measure the word count and analyse the distribution of content in our paper, is it balanced and good

> AGENT

## Word distribution | Body section | Words | % of body | |---|---:|---:| | Introduction | 532 | 23.2% | | Related Work | **1153** | **50.2%** | | Method (RR-MoA) | 164 | 7.1% | | Experiments | 353 | 15.4% | | Conclusion | 94 | 4.1% | | **Body total** | **2296** | 100% | Appendix: 4128 words across 16 sections. Body:Appendix ≈ 1:1.80. Largest appendix block is §P Closing the DLinear Gap at 1217 words (30% of appendix); next are §D Proofs (539) and §H Normalization Generalization (433). ## Verdict: body is unbalanced A typical NeurIPS body sits roughly at **Intro 15–20% / Related Work 10–15% / Method 25–30% / Experiments 30–40% / Conclusion <5%**. Yours: - **Related Work eats half the body (50%, ~1150 words).** That is roughly 3× the conventional share. The four mini-paragraphs (TSFM Adaptation, MoE in FMs, MoE Collapse and Rescue, Normalization in TS) read more like a survey than a positioning section. - **Method is starved (7%, 164 words of prose).** Figures/equations carry the load, but the actual textual description of RR-MoA is thinner than the contributions list in the intro. - **Experiments is also light (15%, 353 words).** Tables […]

> DEVELOPER

plan improvements toward more balanced without dropping in-text citations or messing with them

> AGENT

## Rebalancing plan — preserve every `\citep`/`\citet`, no page-limit regressions **Target distribution** (typical NeurIPS): | Section | Current | Target | Δ words | |---|---:|---:|---:| | Introduction | 532 (23%) | ~440 (~20%) | **−90** | | Related Work | 1153 (50%) | ~600 (~27%) | **−550** | | Method | 164 (7%) | ~340 (~15%) | **+175** | | Experiments | 353 (15%) | ~640 (~28%) | **+285** | | Conclusion | 94 (4%) | ~85 (~4%) | flat | | **Total** | 2296 | ~2105 | **−190** (≈ ½ page recovered) | Note: this both rebalances *and* recovers space, since cuts in Related Work outweigh the additions in Method/Experiments. That ½-page buffer is what funds the Method/Experiments expansion without re-spilling onto page 10. --- ### Step 1 — Compress Related Work by ~550 words (no citation loss) Each `\citep`/`\citet` key stays. The cuts are descriptive clauses ("X reprograms patch embeddings into the LLM token space", "Y achieves competitive forecasting with only 10k parameters via frequency-domain interpolation") that paraphrase each cited work's contribution. The pattern is to convert "X~\citep{x} does <one-line description>" into bare list-citations grouped by theme. Per-paragraph targets: - **TSFM Adaptation** (~510 → ~250 words): merge the […]

> DEVELOPER

let's do it the safe way

> AGENT

Starting Step 1 — Related Work compression. First, baseline the citation count so we can verify nothing is dropped.

> AGENT

Baseline: 92 unique citation keys. Backup saved. Now editing paragraph 1 (TSFM Adaptation).

> AGENT

All 91 unique keys preserved (true count after splitting multi-key cites). Continuing to ¶2.

> AGENT

Step 1 complete: Related Work 50.2% → 42.8%, body ends comfortably on p9, citations preserved (91/91), 107/107 verify.py checks pass. Now proceeding to Steps 2 + 3 (expand Method + Experiments). Backup current state.

> AGENT

Now Step 3: expand §4.2 (60-80 words per subsubsection).

> AGENT

Now verify everything: build, page count, citations, claim numerics.

> AGENT

All gates pass. Final state: | Section | Before | After | Δ | |---|---:|---:|---:| | Introduction | 23.2% | 27.0% | (relative ↑ from RW shrink) | | **Related Work** | **50.2%** | **38.7%** | **−11.5pp** | | **Method** | **7.1%** | **11.1%** | **+4.0pp** | | **Experiments** | **15.4%** | **18.6%** | **+3.2pp** | | Conclusion | 4.1% | 4.6% | flat | **Verification gates (all green):** - 91/91 unique citation keys preserved (no `\citep`/`\citet` dropped or modified) - LaTeX builds clean, body fits on page 9 (conclusion's last line on p9, References starts p10) - 107/107 verify.py numeric claims still pass - PDF: 50 pages total **What changed:** - **Related Work** (4 paragraphs): collapsed per-cite vignettes into grouped citations while keeping the AdaMix/AdaPTS/SEMPO/MoLE positioning sentences and the three-thread MoE-collapse classification intact. - **Method §3** (+2 paragraphs): added "Inference cost and deployment" (router param count, FLOPs share, hot-swap deployment) and "Routing dynamics" (entropy band, naive-rescue forward reference). - **Experiments §4.2** (+1–2 sentences per subsubsection): explained stochastic-vs-stable collapse signature, added the SNR-falsification interpretation of the Traffic boundary case, framed the three architecture-agnostic interventions as a 3-axis cross-cut, and expanded the cross-backbone summary into per-axis (backbone / task / horizon) […]

> DEVELOPER

another round of review please to check the quantitative measures again

> AGENT

Bug in my script — Conclusion bleeds into bibliography region. Fixing measurement.

> AGENT

Bug found in my script: `%.*` regex was eating after `\%` (escaped percent) too. Re-measuring with the fix.

> AGENT

## Round-2 review: corrected measurement **I have to flag this honestly: the previous percentages were wrong.** My measurement script had a bug — the comment-stripping regex `%.*` was treating `\%` (escaped percent in MSE deltas like `26\%`) as the start of a LaTeX comment and deleting everything after it on the line. This systematically undercounted any section dense with percentage figures (Method, Experiments, Conclusion). Related Work — which uses fewer percent signs — was undercounted least, so it falsely appeared to dominate. ### Corrected body distribution | Section | Words | % of body | Cites | Cite density | |---|---:|---:|---:|---:| | Introduction | 616 | 19.0% | 26 | 1 / 24w | | Related Work | 693 | **21.3%** | 52 | 1 / 13w | | Method (RR-MoA) | 402 | 12.4% | 1 | 1 / 402w | | Experiments | 1350 | **41.6%** | 23 | 1 / 59w | | Conclusion | 186 | 5.7% | 0 | — | | **Body total** | **3247** | 100% | 102 | 1 / 32w | ### §4 Experiments sub-distribution | Block | Words | Cites | |---|---:|---:| | Setup | 219 | 12 | | […]