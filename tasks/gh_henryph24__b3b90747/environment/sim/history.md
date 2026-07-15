> DEVELOPER

cut related work by 20 lines

> AGENT

Now I have a clear picture. Let me load the tools I need.

> AGENT

The Related Work section is already heavily compressed: it's just one paragraph, rendering to ~13 PDF lines (lines 70-82) plus the heading. Cutting "20 lines" exceeds the section's current size, so I need to confirm the target before planning.

> DEVELOPER

it currently from 86 to 148, recompile and check

> AGENT

You're right — the PDF I'm looking at is stale (it was built before the unstaged intro tweak). Let me recompile and check the current rendered position.

> AGENT

After recompiling, I'm seeing different rendered locations than what you described. Let me show you what I find so we can align: **Related Work (§2)** in the recompiled PDF: margin lines **70–82** (13 lines of body text). **Lines 86–148** are §3 (RR-MoA method): from "experts consume the frozen TSFM's hidden states..." through to the end of the Top-k pool list before "Because the backbone is strictly frozen...". A few possibilities: 1. Your viewer is showing a stale PDF (the one before the e15f8fa compression that took Related Work from 60 → 13 lines). 2. You meant §3 (RR-MoA method/setup) when you said "related work" — that block does run lines 84–148. 3. You're looking at a different PDF entirely. Could you confirm which you want me to cut 20 lines from? - **A.** Related Work proper (PDF lines 70–82, currently 13 lines — can't cut 20, would need to delete the section) - **B.** §3 RR-MoA setup/problem-statement block (PDF lines 84–148, ~64 lines — 20-line cut is feasible) - **C.** Something else entirely

> DEVELOPER

let recompile, I'll check manually

> AGENT

Recompiled. `main.pdf` is fresh (May 6 16:15:49, 50 pages, 902921 bytes). Open it and let me know which line range you want trimmed.

> DEVELOPER

we overdo it, it should be about 40 lines, check what commits did we accidentally removed too much

> AGENT

Found it. **e15f8fa** is the over-cut commit (May 6 15:54). It collapsed Related Work from **60 → 13 PDF lines** by replacing 4 thread paragraphs with one packed paragraph. The 4 deleted paragraphs (each ~10–14 PDF lines) were: | Thread | Lines | Key content | |---|---|---| | **TSFM Adaptation** | ~14 | wen2023 survey, compact specialists, adapter recipe variants, AdaPTS, AdaMix-vs-RR-MoA topology contrast, novelty claim | | **MoE in Foundation Models** | ~14 | Shazeer/GShard/Switch/V-MoE, design axes, in-backbone TS-MoE (Moirai-MoE/Time-MoE/SEMPO), MoLE, MMoE, axis-orthogonality claim | | **MoE routing collapse and rescue** | ~13 | 3 threads (optimization/geometry/architectural), 11-rescue distinction, concurrent AoE/Routing-Free/ERMoE, Wang myth | | **Normalization in Time Series** | ~9 | RevIN, DishTS/SAN/NST/FAN/DDN, redundancy/IBNorm, our specific MoE consequence | Plus a 1-line lead-in. To hit ~40 PDF lines we need ~27 lines back. Three reasonable restorations: - **A. Most differentiating** — restore *TSFM Adaptation* + *MoE collapse and rescue* threads in full (these carry the AdaMix/AdaPTS contrast and the rescue-thread distinction), drop the other two. ~28 lines added → ~41 total. - **B. Balanced** — restore all 4 threads but trim each by ~40% (keep one or two anchor citations per thread + the differentiation sentence). ~27 lines […]