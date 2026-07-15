> DEVELOPER

are we having this exact sentence: ""﻿Today, every public TSFM benchmark uses a single static head ""

> AGENT

No. That exact sentence is not in the paper. The closest variants are: - `main.tex:58` — "Standard adapters use a single static head." - `main.tex:66` — "The standard TSFM benchmark protocols~\citep{...} use a single static head that pools hidden states and projects them to the forecast horizon..." - `main.tex:109` — "TSFM adapters today use a single static head for every input window" - `main.tex:221` — "Today's TSFM benchmarks use a single static head over hidden states." Want me to replace one of these with "Today, every public TSFM benchmark uses a single static head"?

> DEVELOPER

" "Today's TSFM benchmarks use a single static head over hidden states."" is this factually correct ? can you use exa mcp to look for academic evidence

> AGENT

I'll search for academic evidence on TSFM benchmark adapter/head architectures.

> AGENT

Yes, factually correct — but with an important nuance. **Direct evidence:** 1. **MOMENT** (`ForecastingHead`, ICML'24) — `nn.Flatten` over hidden states `(B, 64, d_model)` then a single `nn.Linear(head_nf, forecast_horizon)`. One static linear head per task. 2. **PatchTST** (ICLR'23) — `FlattenHead` does `flatten` → single `nn.Linear(nf, target_window)`. The `Time-Series-Library` (12K-star de-facto LTSF benchmark host) and the official `PatchTST` repo both implement it identically. 3. **TimesFM** — output patches via a single linear projection from hidden dim to a fixed patch-of-future-values; one head, used at every decoding step. 4. **Chronos / Chronos-Bolt** — single output projection (token vocabulary in v1, quantile head in Bolt). One head. 5. **Moirai** — one mixture-distribution head over hidden states. **Caveat / nuance worth being careful about:** - "TSFM benchmarks" is slightly ambiguous. The *models* (MOMENT, TimesFM, Chronos, Moirai) all ship a single static head over hidden states. The *benchmark protocols* used to evaluate them (LTSF Informer split, Time-Series-Library, GIFT-Eval) inherit that — they evaluate models that each have one head, but the benchmark itself doesn't mandate it. - **PatchTST has an `individual=True` option** that gives one separate linear head per channel — still static (no per-window routing), still trained jointly, but not literally "a single" head if a reviewer reads it strictly. - Moirai's distribution head is technically a mixture, but it's still one fixed head applied to every input window. **Recommended phrasing fix** to avoid a pedantic reviewer: replace "single static head" with "a single static head" (already what you have on line 221) or, more precisely, "a single fixed head with no per-window adaptation". The claim "no per-window mixture / no input-dependent head selection" is the load-bearing part for your framing, and that *is* universally true across the models you cite. Sentence as written on line 221 is defensible.

> DEVELOPER

why that still reads quite over-generalisation to me

> AGENT

You're right — the sentence reads as a sweeping factual claim about the entire benchmark ecosystem, when the actual load-bearing claim is narrower (no input-dependent head selection / no per-window mixture). Let me suggest tighter alternatives: **Current (line 221, figure caption):** > "Today's TSFM benchmarks use a single static head over hidden states." **Sources of over-generalization:** 1. "Today's TSFM benchmarks" — sounds like a survey of all benchmarks; what's true is the *models commonly evaluated on them*. 2. "single static head" — Moirai uses a mixture-distribution head; PatchTST has a per-channel `individual=True` variant. Strictly, "single" can be picked apart. 3. "over hidden states" — TimesFM/Chronos decoder-only models project from the last decoder state, fine, but the framing implies a uniform pipeline. **Tighter alternatives (pick one):** - *Most defensible, narrowest claim:* "Standard TSFM adapters apply a single fixed head to every input window, with no input-dependent routing." (matches what your paper actually attacks) - *Closer to the original but hedged:* "Public TSFM checkpoints (MOMENT, TimesFM, Chronos, Moirai) ship with a single fixed forecasting head; none route different windows to different heads." - *Pure mechanism framing:* "These models use one fixed head per task, applied identically to every window." The third is the most reviewer-proof — it drops "benchmark," drops "static" (mild jargon collision with "static graph"), and drops "hidden states" (irrelevant detail for the figure caption). It states the *property* (one head, applied uniformly) that your MoE extension breaks. Want me to swap line 221 — and similarly tighten lines 58, 66, and 109 — to one of these?

> DEVELOPER

pick the most reviewer-proof of course right ?

> AGENT

Picking the third option — "These models use one fixed head per task, applied identically to every window." — and applying it consistently across all four locations.

> AGENT

All four locations updated: - **L58** (abstract): "Standard adapters use one fixed head per task, applied identically to every window." - **L66** (intro): "Public TSFM checkpoints~\citep{...} use one fixed head per task that pools hidden states and projects them to the forecast horizon, applied identically to every window..." - **L109** (figure banner): "TSFM adapters use one fixed head, applied identically to every window" - **L221** (figure caption): "TSFM adapters use one fixed head per task, applied identically to every window." The phrasing now describes the *property the paper attacks* (one fixed head, no per-window selection) rather than making a sweeping survey claim about "every benchmark." It's tight against MOMENT/PatchTST/TimesFM/Chronos/Moirai (all of which match this description) and survives PatchTST's `individual=True` variant since "per task" still allows per-channel parameterization.

> DEVELOPER

Public TSFM checkpoints still sound over-generalisating. We had many TSFM that does not use fixed head per task is that correct (verify with exa mcp paper search first)

> AGENT

Verifying first.

> AGENT

You are correct — there are notable counterexamples that break the universal claim: **Counterexamples found:** 1. **Time-MoE** (ICLR'25 Spotlight, Shi et al. 2024): explicitly uses **multi-resolution forecasting with separate prediction heads for each resolution** — not one fixed head per task. Different output projections handle different horizon lengths. 2. **Moirai** (Woo et al. 2024): uses **multiple input/output projection layers, each tailored to a specific frequency** — frequency-routed heads, not one fixed head. 3. **TimesFM 2.5** (Das et al.): adds a **separate ~30M-parameter quantile forecasting head** alongside the point head — multiple heads. 4. **Moirai-MoE** (ICML'25): uses sparse MoE *inside the transformer* (token-level expert routing in FFNs). Output projection is single, but the model architecture is explicitly an input-conditioned mixture. So the claim "Public TSFM checkpoints use one fixed head per task, applied identically to every window" is **factually wrong** as a blanket statement. Time-MoE picks a head by resolution; Moirai picks by frequency; TimesFM 2.5 has multiple co-trained heads. **What's still true and load-bearing for your paper:** - None of these models do **per-window, input-content-driven head selection** (i.e., none route based on the raw signal content within a single window's distribution). - Time-MoE's resolution selection is a *metadata* choice (the user/horizon picks the head), not a learned router on the input. - Moirai's frequency selection is also metadata-driven. - The *adapter literature* you actually compete with (LoRA, AdaMix, TRACE, MOMENT's `ForecastingHead`) does use one fixed head per task. **Tightened phrasing options:** - *Most accurate:* "Standard adapters for TSFM downstream evaluation use one fixed head per task (e.g., MOMENT's `ForecastingHead`, PatchTST's `FlattenHead`, LoRA-tuned linear projections), with no input-content-driven head selection." - *Shorter, still accurate:* "Standard TSFM adapters use a fixed head with no input-dependent routing — the same head is applied to every window." - *Shortest:* "Standard TSFM adapters apply the …

> DEVELOPER

"no input-content-driven routing" is unnecessarily complex

> AGENT

Simpler alternatives that say the same thing: - *"Standard TSFM adapters use the same head for every window."* - *"Standard TSFM adapters apply one head to all windows."* - *"Standard TSFM adapters use a single head, regardless of the input."* - *"Standard TSFM adapters use a fixed head; no per-window selection."* The first is the cleanest — concrete, no jargon, and accurate (it makes no claim about "per task" or "per benchmark"; it just says the head doesn't change with the window, which is the property your MoE breaks). Want me to apply *"use the same head for every window"* across all four locations?

> DEVELOPER

let's do it

> AGENT

All four locations updated: - **L58** (abstract): "Standard adapters use the same head for every window." - **L66** (intro): "Standard TSFM adapters~\citep{...} pool hidden states and project them to the forecast horizon through the same head for every window..." - **L109** (figure banner): "TSFM adapters use the same head for every window" - **L221** (figure caption): "TSFM adapters use the same head for every window."

> AGENT

Committed and pushed as `bf98315`.
