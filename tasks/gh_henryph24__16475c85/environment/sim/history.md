> DEVELOPER

related work currently ends at line 148. Ideally it should end at 100, save the rest for the subsequent sections. Plan cuts but maintain cohesive discussions and omit no in-text citations

> AGENT

Let me see the Method section to understand where citations might already be referenced.

> AGENT

I'll plan this without TaskCreate since it's a focused analysis task. Let me check the Experiments section to identify natural homes for moved citations.

> AGENT

Let me verify which citations in Related Work are duplicated vs. unique, since duplicates can be cut without preservation work.

> AGENT

I have the full picture. Let me verify the cross-reference from §3 line 252 to Related Work that we'll need to update.

> AGENT

Now I have everything I need. Here's the plan. ## Plan: cut Related Work from PDF lines 88–148 to 88–100 ### Audit summary The four-paragraph Related Work currently runs **60 PDF lines** and contains **~55 unique citations**. Of those: - **28 are duplicated** in §3 (lines 248, 252) or §4 (lines 419, 459, 522, 524, 561). Dropping them from Related Work loses no in-text citation. - **27 are orphans** that appear *only* in Related Work + bibliography. These must be preserved in the rewritten paragraph (or moved to a downstream section). Orphans to preserve: - *TSFM/adapter:* `wen2023tssurvey`, `wu2025srsnet`, `wang2025timemixerpp`, `xu2024fits`, `chen2023tsmixer`, `fu2025selective`, `jin2024timellm`, `zhou2023onefitsall`, `liu2024autotimes`, `houlsby2019adapters`, `qiao2025msft`, `benechehab2025adapts`, `zhao2025prune`, `faw2025icf`, `ning2025tsrag`, `gupta2024beyondlora`, `zhang2025template`, `woo2024gifteval` - *MoE:* `lepikhin2021gshard`, `riquelme2021vmoe`, `komatsuzaki2023sparseupcycling`, `raposo2024mod`, `jiang2024mixtral`, `zhu2024llamamoe`, `dai2024deepseekmoe`, `cai2024moesurvey`, `shi2024timemoe`, `he2025sempo`, `ma2018mmoe`, `wang2026myth` - *Normalization:* `ulyanov2016instancenorm` ### Approach Replace the four-paragraph thread-by-thread structure with **one compact paragraph** (≤12 PDF lines) that packs the 27 orphans into dense citation lists with a one-clause role marker per cluster. The duplicated citations are simply deleted: §3 line 252 and §4 already carry their narrative weight, so nothing moves — they vanish from §2 only. Cluster structure (one sentence each, ~2–3 PDF lines per cluster): 1. **TSFM adaptation cluster** […]

> DEVELOPER

was this directly relevant to our discussion theme: " Lost (intentionally): detailed per-paper contrast (e.g., AdaPTS treats adapter choice as per-task hyperparameter; SEMPO routes prompt-experts at token level; the "no prior per-window topology mixture in TSFM literature" novelty claim — recoverable as half-sentence if budget allows)."

> AGENT

You're right to push back. Two of the three are core, not peripheral: 1. **AdaPTS contrast (per-task vs per-window)** — directly relevant. It's the cleanest way to state what RR-MoA does that the closest TSFM-adapter peer doesn't. Cutting it weakens the positioning, not just the prose. 2. **"No prior per-window topology mixture in TSFM literature" novelty claim** — *most* relevant. This is the contribution statement, not flavor. Demoting it to "recoverable if budget allows" was a mistake — it should be load-bearing in any related work, even at 12 lines. 3. **SEMPO contrast (token-level vs window-level)** — moderately relevant. SEMPO is the closest in-TSFM mixture, and "token-level prompt mixture vs per-window adapter mixture" is the right axis to put it on. Worth keeping if budget permits, but the role marker "in-backbone TS-MoE" already covers it categorically. **Revised plan:** keep #1 and #3 in the compressed paragraph, treat #2 as the compressible item. The TSFM adaptation cluster ends with one short clause carrying both: *"AdaPTS treats adapter choice as a per-task hyperparameter; we are the first per-window mixture over topologically distinct adapters on a frozen TSFM."* That's ~1.5 lines and covers the contribution claim explicitly. The remaining 27 orphans pack around […]

> DEVELOPER

no let cut more from the intro currently start at 30 and ends at 80 (50 lines), it should ideally be about 38 pages

> AGENT

Let me read the current intro in the PDF and source.

> AGENT

Have everything I need. Here's the cut plan for the Intro. ## Plan: cut Intro from PDF lines 30–84 (55 lines) to ~38 lines ### Current shape | Source line | Role | PDF lines | Lines | |---|---|---|---| | L64 | TSFM intro + ecosystem citation list | 30–34 | 5 | | L66 | Per-window mixture motivation + deployment | 35–42 | 8 | | L68 | Collapse statement (entropy → 0; co-adaptation) | 43–51 | 9 | | L70 | "Failure is specific to learnable-affine…" + rescue numbers + Moirai | 52–56 | 5 | | L72 | RR-MoA fix + Frozen Paradox preview | 57–62 | 6 | | L74 | "Three contributions" lead-in | 63–64 | 2 | | L76 | **Bullet 1**: Problem formulation | 65–70 | 6 | | L77 | **Bullet 2**: Experimental results | 71–77 | 7 | | L78 | **Bullet 3**: Causal intervention | 78–84 | 7 | | | | | **55** | ### Where the redundancy lives - **Bullet 1** repeats the "720-run / 10.9% / 2.7× / input-not-optimization" content already in L70 + abstract. - **Bullet 3** repeats the RR-MoA + SR-MoA + Residual-IA⁺ summary already […]