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