> DEVELOPER

seeds (∗/∗∗/∗∗∗ for p<0.05/0.01/0.001). 

[Image #1]

Is this rendering error

> TOOL

tool_use Bash
id: toolu_019CGgiRQbrNeRh3tt5morgE
```json
{
  "command": "grep -n \"App\\.\" /home/<USER>/neuralips26/main.tex | head -30",
  "description": "Find App. references in main.tex"
}
```

> TOOL

tool_result
id: toolu_019CGgiRQbrNeRh3tt5morgE
```
246:\textbf{Task setup.} Given a window $\mathbf{x}\in\mathbb{R}^{T\times c}$ ($T{=}512$, $c$ channels), forecasting predicts $\mathbf{y}\in\mathbb{R}^{h\times c}$ at horizons $h\in\{96,192,336,720\}$ under MSE loss (imputation uses the same formalism with $\mathbf{y}$ as the reconstruction target). A pretrained TSFM acts as a feature extractor $f_\theta:\mathbb{R}^{T\times c}\to\mathbb{R}^{P\times d}$ ($P$ patches of dim $d$) with $\theta$ \emph{frozen} ($\nabla_\theta\!\equiv\!0$); we train only an adapter $g_\phi:\mathbb{R}^{P\times d}\to\mathbb{R}^{h\times c}$ with a small parameter budget ($|\phi|\leq 500$K), so that many task-specific adapters can be hot-swapped onto a single shared backbone (App.~\ref{app:deployment}). A \emph{per-window mixture of adapters} replaces $g_\phi$ with $K$ experts $\{\mathrm{Expert}_j\}_{j=1}^K$ plus a router $G_\psi$ that returns a sparse weight $\widetilde{w}\in\Delta^{K-1}$ supported on a Top-$k$ subset ($k\leq K$), giving $\hat{\mathbf{y}}=\sum_{j} \widetilde{w}_j\,\mathrm{Expert}_j(f_\theta(\mathbf{x}))$ trained by $\min_{\phi,\psi}\,\mathbb{E}\,\|\hat{\mathbf{y}}-\mathbf{y}\|_2^2$.
419:\textbf{Baselines.} Four tiers, kept separate to avoid confounding frozen-vs-unfrozen and adapter-vs-from-scratch comparisons: \emph{frozen-adapter} (three fixed adapters; $5$-expert independent ensemble; AdaMix~\citep{wang2022adamix}); \emph{frozen PEFT} (LoRA~\citep{hu2022lora}, $108$-run sweep, App.~\ref{app:lora_sweep}; TRACE~\citep{li2025trace}); \emph{unfrozen} (full fine-tuning, all blocks, best of $5$ heads $\times 2$ LRs; extended schedules in App.~\ref{app:extended_ft}); \emph{from-scratch calibration} (DLinear~\citep{zeng2023dlinear}).
421:\textbf{Training and statistics.} Adam ($\eta{=}10^{-3}$), MSE loss, $15$ epochs, batch $128$; $5$ seeds for the core grid, $3$ for ablations. Significance via Wilcoxon signed-rank, Bonferroni-corrected over 6 datasets $\times$ 5 seeds ($^{*}\!/^{**}\!/^{***}$ for $p{<}0.05/0.01/0.001$). Full hyperparameters […]

> TOOL

tool_use Bash
id: toolu_01QcT6LLDJeEUTvbRbxJJtEW
```json
{
  "command": "grep -n \"Full hyperparameters\" /home/<USER>/neuralips26/main.tex",
  "description": "Find the specific paragraph"
}
```

> TOOL

tool_result
id: toolu_01QcT6LLDJeEUTvbRbxJJtEW
```
421:\textbf{Training and statistics.} Adam ($\eta{=}10^{-3}$), MSE loss, $15$ epochs, batch $128$; $5$ seeds for the core grid, $3$ for ablations. Significance via Wilcoxon signed-rank, Bonferroni-corrected over 6 datasets $\times$ 5 seeds ($^{*}\!/^{**}\!/^{***}$ for $p{<}0.05/0.01/0.001$). Full hyperparameters in App.~\ref{app:setup}; on acceptance we release the code, the $5{,}463$ per-run JSONs, and a \texttt{verify.py} script that re-derives all $107$ numeric claims within tolerance ($234.8$ measured GPU-hours on a single A10G; license + per-backbone breakdown in the Paper Checklist).
```

> TOOL

tool_use Bash
id: toolu_014oKVChCuHfSye8C26K37E6
```json
{
  "command": "grep -n \"app:setup\" /home/<USER>/neuralips26/main.tex | head -10",
  "description": "Find app:setup label"
}
```

> TOOL

tool_result
id: toolu_014oKVChCuHfSye8C26K37E6
```
407:\textbf{Cost, expert pool, deployment.} The router is a Conv1d gate of $853$ parameters ($0.4\%$ of one expert head, ${<}10^{-3}$ of the frozen backbone); with $k{=}2$ of $K{=}5$ active per window, RR-MoA adds two adapter forward passes plus the gate to one frozen TSFM forward. The expert pool itself comprises $K{=}5$ topologically distinct adapters (mean-pool, last-token, max-pool, attention-pool, Conv1d-pool), spanning pooling families with distinct expressivity regimes for transformer-based sequence models~\citep{ennadir2025pooling}; architectural diversity is critical, since five identical experts (same topology, different initialization) degrade MSE by $8$--$15\%$ (Appendix~\ref{app:diversity}; pseudocode in Algorithm~\ref{alg:rrmoa}, Appendix~\ref{app:setup}). Because the backbone is strictly frozen, a single TSFM held in GPU memory can be shared across many tenants while per-task adapter pools (${\sim}500$K params each) hot-swap from host RAM, an arrangement DLinear and per-dataset-from-scratch baselines cannot match (Appendix~\ref{app:benchmark}).
417:\textbf{Backbones.} Five backbones spanning three normalization regimes: (i)~learnable-affine RevIN-inside-encoder MOMENT-small/large~\citep{goswami2024moment} (internal RevIN~\citep{kim2021revin}); (ii)~Moirai~\citep{woo2024moirai} and Moirai-MoE, which use RMSNorm internally with only non-learnable per-instance I/O scaling (no learnable-affine RevIN inside the encoder pipeline); (iii)~Chronos~\citep{ansari2024chronos} (T5-style, no instance normalization) and Timer-XL~\citep{liu2025timerxl} (LayerNorm only, no instance normalization) as no-instance-normalization negative controls (per-backbone normalization specifications in Appendix~\ref{app:setup}, \S\ref{sec:cross_backbone}). The collapse mechanism predicts that only regime~(i) is vulnerable: routing signal is destroyed […]

> TOOL

tool_use Bash
id: toolu_017Y2m4BZFm2Pj6T7d3PCxjB
```json
{
  "command": "grep -n \"\\\\\\\\section\\|\\\\\\\\appendix\\|app:setup\\|app:deployment\\|app:lora_sweep\" /home/<USER>/neuralips26/main.tex | head -30",
  "description": "Check appendix structure and labels"
}
```

> TOOL

tool_result
id: toolu_017Y2m4BZFm2Pj6T7d3PCxjB
```
61:\section{Introduction}
66:Standard TSFM adapters apply the \emph{same} regression head to every window (Figure~\ref{fig:problem_overview}a): flatten-then-project for MOMENT~\citep{goswami2024moment} and PatchTST~\citep{nie2023patchtst}, an autoregressive residual block for TimesFM~\citep{das2024timesfm}. Real time series mix heterogeneous regimes whose \emph{shape} variation (periodicity, trends, level shifts, change points) survives instance normalization and lives in the hidden states across layers~\citep{wilinski2025tsfm_representations, pandey2025tsfm_semantics}, motivating a per-window mixture of topologically distinct expert heads with a learned router. Keeping the backbone frozen is also what makes deployment practical: a shared TSFM in GPU memory serves many tenants through lightweight per-task adapters hot-swapped from host RAM, an arrangement per-dataset models like DLinear~\citep{zeng2023dlinear} cannot match (Appendices~\ref{app:deployment},~\ref{app:benchmark}).
228:\section{Related Work}
241:\section{Raw-Routed Mixture of Adapters (RR-MoA)}
246:\textbf{Task setup.} Given a window $\mathbf{x}\in\mathbb{R}^{T\times c}$ ($T{=}512$, $c$ channels), forecasting predicts $\mathbf{y}\in\mathbb{R}^{h\times c}$ at horizons $h\in\{96,192,336,720\}$ under MSE loss (imputation uses the same formalism with $\mathbf{y}$ as the reconstruction target). A pretrained TSFM acts as a feature extractor $f_\theta:\mathbb{R}^{T\times c}\to\mathbb{R}^{P\times d}$ ($P$ patches of dim $d$) with $\theta$ \emph{frozen} ($\nabla_\theta\!\equiv\!0$); we train only an adapter $g_\phi:\mathbb{R}^{P\times d}\to\mathbb{R}^{h\times c}$ with a small parameter budget ($|\phi|\leq 500$K), so that many task-specific adapters can be hot-swapped onto a single shared backbone (App.~\ref{app:deployment}). A \emph{per-window mixture of adapters} replaces $g_\phi$ with $K$ […]

> AGENT

Not a rendering error. `App.~\ref{app:setup}` correctly resolves to "App. A" because `\label{app:setup}` is attached to the first appendix section (`\section{Experimental Setup Details}` at line 1057, immediately after `\appendix` at line 1045). LaTeX numbers appendix sections with letters, so it renders as **A**.

The semicolon after "A" is just punctuation continuing the sentence ("…in App. A; on acceptance we release…"). Both the reference and the punctuation are intentional and correct.

> DEVELOPER

what is this writing implying: " (∗/∗∗/∗∗∗ for p<0.05/0.01/0.001)"

> AGENT

It's a legend for significance markers: a single asterisk (∗) marks results significant at p<0.05, two (∗∗) at p<0.01, and three (∗∗∗) at p<0.001. So when you see ∗/∗∗/∗∗∗ next to a number elsewhere in the paper, it tells you which p-value threshold the Wilcoxon signed-rank (Bonferroni-corrected) test cleared.

> DEVELOPER

so it is a style ?

> AGENT

Yes — it's a notational convention (a common style in stats/ML papers) for compactly annotating significance levels next to results, rather than writing out the p-value each time.

> DEVELOPER

conclusion part is really short relative to intro. cut intro a bit, add back a bit to conclusion (which currently reads quite compact)

> TOOL

tool_use Bash
id: toolu_01PxZpPRkwPhK5g6Y18BdZkv
```json
{
  "command": "grep -n \"^\\\\\\\\section\\|^\\\\\\\\appendix\" /home/<USER>/neuralips26/main.tex | head -20",
  "description": "Find section boundaries"
}
```

> TOOL

tool_result
id: toolu_01PxZpPRkwPhK5g6Y18BdZkv
```
61:\section{Introduction}
228:\section{Related Work}
241:\section{Raw-Routed Mixture of Adapters (RR-MoA)}
411:\section{Experiments}
565:\section{Conclusion and Limitations}
1045:\appendix
1057:\section{Experimental Setup Details}
1134:\section{Deployment-Regime Motivation}
1176:\section{Multi-Horizon Evaluation}
1200:\section{Proposition Proofs}
1350:\section{LoRA Sweep (Full Results)}
1415:\section{Routing Ablations}
1728:\section{Extended RR-MoA Freeze Grid}
1861:\section{Normalization Generalization}
1917:\section{Top-$k$ Sparse Routing Ablation}
1993:\section{Imputation Results}
2021:\section{Learnable Normalization Coefficient}
2047:\section{Exact MI Loss and Bound Tightness}
2078:\section{Information Content Diagnostic}
2197:\section{Cross-Backbone RR-MoA}
```

> TOOL

tool_use Read
id: toolu_01VGr2CJ1RSxm4WwdChmKK9s
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 61,
  "limit": 170
}
```

> TOOL

tool_result
id: toolu_01VGr2CJ1RSxm4WwdChmKK9s
```
61	\section{Introduction}
62	\label{sec:intro}
63	
64	Time series foundation models (TSFMs) such as MOMENT~\citep{goswami2024moment}, TimesFM~\citep{das2024timesfm}, Chronos~\citep{ansari2024chronos}, Timer-XL~\citep{liu2025timerxl,liu2024timer}, and Moirai~\citep{woo2024moirai} now provide pretrained representations for time series, alongside further pretrained variants~\citep{lee2024units, rasul2024lagllama, ekambaram2024ttm}, observability-domain deployments~\citep{cohen2025toto}, tokenization-free flow-matching forecasters~\citep{liu2025sundial}, and a parallel route that reprograms pretrained LLMs as forecasters~\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes, pan2024s2ipllm, liu2024unitime}, with recent designs pushing to billion-parameter scales~\citep{shi2024timemoe, liu2026timers1}. Using one of these backbones on a downstream task still requires attaching a lightweight adapter head that maps hidden states to predictions; this paper studies the adapter, holding the backbone fixed.
65	
66	Standard TSFM adapters apply the \emph{same} regression head to every window (Figure~\ref{fig:problem_overview}a): flatten-then-project for MOMENT~\citep{goswami2024moment} and PatchTST~\citep{nie2023patchtst}, an autoregressive residual block for TimesFM~\citep{das2024timesfm}. Real time series mix heterogeneous regimes whose \emph{shape} variation (periodicity, trends, level shifts, change points) survives instance normalization and lives in the hidden states across layers~\citep{wilinski2025tsfm_representations, pandey2025tsfm_semantics}, motivating a per-window mixture of topologically distinct expert heads with a learned router. Keeping the backbone frozen is also what makes deployment practical: a shared TSFM in GPU memory serves many tenants through lightweight per-task adapters hot-swapped from host RAM, an arrangement per-dataset models like DLinear~\citep{zeng2023dlinear} cannot match (Appendices~\ref{app:deployment},~\ref{app:benchmark}).
67	
68	This natural mixture-of-experts […]

> TOOL

tool_use Read
id: toolu_01WvHSPSiqbHHv9pH9u7wYPG
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 565,
  "limit": 100
}
```

> TOOL

tool_result
id: toolu_01WvHSPSiqbHHv9pH9u7wYPG
```
565	\section{Conclusion and Limitations}
566	\vspace{-1.0em}
567	
568	{\looseness=-1 We identified \emph{normalization-induced routing collapse}: the same $(\mu,\sigma)$ stripping that lets TSFMs handle distribution shift removes the signal a downstream MoE router needs. Observation~\ref{thm:mi_decomp} formalizes the loss, $R(\mathcal{D})$ predicts it ($\rho{=}{-}0.88$), eight causal controls rule out optimization/geometry/paradigm alternatives, and three interventions confirm it: RR-MoA ($54/54$), SR-MoA ($+13$--$42\%$), Residual-IA\textsuperscript{+} ($107/123$). \textbf{Limitations:} specific to $(\mu,\sigma)$-stripping normalizers; classification, anomaly detection, and learned expert pools remain open.\label{page:end_main}}
569	\bibliographystyle{plainnat}
570	\begin{thebibliography}{20}
571	
572	\bibitem[Dosovitskiy et~al.(2021)]{dosovitskiy2021vit}
573	Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby.
574	\newblock An image is worth 16x16 words: Transformers for image recognition at scale.
575	\newblock In \textit{International Conference on Learning Representations (ICLR)}, 2021.
576	
577	\bibitem[Goswami et~al.(2024)]{goswami2024moment}
578	Mononito Goswami, Konrad Szafer, Arjun Choudhry, Yifu Cai, Shuo Li, and Artur Dubrawski.
579	\newblock {MOMENT}: A family of open time-series foundation models.
580	\newblock In \textit{Proceedings of the 41st International Conference on Machine Learning (ICML)}, volume 235 of \textit{PMLR}, pages 16115--16152, 2024.
581	
582	\bibitem[Das et~al.(2024)]{das2024timesfm}
583	Abhimanyu Das, Weihao Kong, Rajat Sen, and Yichen Zhou.
584	\newblock A decoder-only […]

> AGENT

Looking at the intro/conclusion balance now.

> TOOL

tool_use Bash
id: toolu_016Zaq9WB2RsSDKPYvVkXxQe
```json
{
  "command": "awk 'NR==568' /home/<USER>/neuralips26/main.tex | wc -w",
  "description": "Count words in conclusion paragraph"
}
```

> TOOL

tool_result
id: toolu_016Zaq9WB2RsSDKPYvVkXxQe
```
      64
```

> TOOL

tool_use Bash
id: toolu_01AeYzZyYyH3YyMEJyihmqPB
```json
{
  "command": "awk 'NR>=64 && NR<=79' /home/<USER>/neuralips26/main.tex | wc -w",
  "description": "Count words in intro"
}
```

> TOOL

tool_result
id: toolu_01AeYzZyYyH3YyMEJyihmqPB
```
     645
```

> AGENT

Intro is 645 words, conclusion is 64 words. Big imbalance. Trimming intro's citation-heavy first paragraph and expanding the conclusion.

> TOOL

tool_use Edit
id: toolu_01Xp2jLRmTD58L5quHYCeGgw
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "Time series foundation models (TSFMs) such as MOMENT~\\citep{goswami2024moment}, TimesFM~\\citep{das2024timesfm}, Chronos~\\citep{ansari2024chronos}, Timer-XL~\\citep{liu2025timerxl,liu2024timer}, and Moirai~\\citep{woo2024moirai} now provide pretrained representations for time series, alongside further pretrained variants~\\citep{lee2024units, rasul2024lagllama, ekambaram2024ttm}, observability-domain deployments~\\citep{cohen2025toto}, tokenization-free flow-matching forecasters~\\citep{liu2025sundial}, and a parallel route that reprograms pretrained LLMs as forecasters~\\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes, pan2024s2ipllm, liu2024unitime}, with recent designs pushing to billion-parameter scales~\\citep{shi2024timemoe, liu2026timers1}. Using one of these backbones on a downstream task still requires attaching a lightweight adapter head that maps hidden states to predictions; this paper studies the adapter, holding the backbone fixed.",
  "new_string": "Time series foundation models (TSFMs) such as MOMENT~\\citep{goswami2024moment}, TimesFM~\\citep{das2024timesfm}, Chronos~\\citep{ansari2024chronos}, Timer-XL~\\citep{liu2025timerxl,liu2024timer}, and Moirai~\\citep{woo2024moirai} now provide pretrained representations for time series, alongside a growing ecosystem of pretrained variants and LLM-reprogrammed forecasters~\\citep{lee2024units, rasul2024lagllama, ekambaram2024ttm, cohen2025toto, liu2025sundial, jin2024timellm, zhou2023onefitsall, liu2024autotimes, pan2024s2ipllm, liu2024unitime, shi2024timemoe, liu2026timers1}. Using one of these backbones on a downstream task still requires attaching a lightweight adapter head that maps hidden states to predictions; this paper studies the adapter, holding the backbone fixed."
}
```

> TOOL

tool_result
id: toolu_01Xp2jLRmTD58L5quHYCeGgw
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01X1bN7jFA8mYSijegfJnVLT
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "{\\looseness=-1 We identified \\emph{normalization-induced routing collapse}: the same $(\\mu,\\sigma)$ stripping that lets TSFMs handle distribution shift removes the signal a downstream MoE router needs. Observation~\\ref{thm:mi_decomp} formalizes the loss, $R(\\mathcal{D})$ predicts it ($\\rho{=}{-}0.88$), eight causal controls rule out optimization/geometry/paradigm alternatives, and three interventions confirm it: RR-MoA ($54/54$), SR-MoA ($+13$--$42\\%$), Residual-IA\\textsuperscript{+} ($107/123$). \\textbf{Limitations:} specific to $(\\mu,\\sigma)$-stripping normalizers; classification, anomaly detection, and learned expert pools remain open.\\label{page:end_main}}",
  "new_string": "{\\looseness=-1 We identified \\emph{normalization-induced routing collapse}: the same $(\\mu,\\sigma)$ stripping that lets TSFMs handle distribution shift removes the signal a downstream MoE router needs. Observation~\\ref{thm:mi_decomp} formalizes the loss, $R(\\mathcal{D})$ predicts it ($\\rho{=}{-}0.88$), eight causal controls rule out optimization/geometry/paradigm alternatives, and three interventions confirm it: RR-MoA ($54/54$), SR-MoA ($+13$--$42\\%$), Residual-IA\\textsuperscript{+} ($107/123$). The diagnosis reframes a failure that prior MoE work treats as optimization (load balancing, z-loss, expert-choice) as one of \\emph{router input}: $11$ optimization-side rescues recover at most $10.9\\%$ MSE on the same grid where changing only the routing signal recovers $54$--$80\\%$, with the optimizer and frozen backbone untouched. Because $R(\\mathcal{D})$ is computable from raw windows alone, the fix comes with a pre-training go/no-go test, and the strictly frozen backbone preserves the multi-tenant deployment regime […]

> TOOL

tool_result
id: toolu_01X1bN7jFA8mYSijegfJnVLT
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01VSu8Ztdi16fM9ZXHxFQvbM
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/build1.log 2>&1; tail -25 /tmp/build1.log",
  "description": "Compile main.tex first pass"
}
```

> TOOL

tool_result
id: toolu_01VSu8Ztdi16fM9ZXHxFQvbM
```
></home/<USER>/Library/texmf/fonts/type1/public/amsfonts/cm/cmmi8.pfb></Us
ers/hungpq2412/Library/texmf/fonts/type1/public/amsfonts/cm/cmmi9.pfb></home/<USER>
ungpq2412/Library/texmf/fonts/type1/public/amsfonts/cm/cmr10.pfb></home/<USER>
2412/Library/texmf/fonts/type1/public/amsfonts/cm/cmr5.pfb></home/<USER>/L
ibrary/texmf/fonts/type1/public/amsfonts/cm/cmr6.pfb></home/<USER>/Library
/texmf/fonts/type1/public/amsfonts/cm/cmr7.pfb></home/<USER>/Library/texmf
/fonts/type1/public/amsfonts/cm/cmr8.pfb></home/<USER>/Library/texmf/fonts
/type1/public/amsfonts/cm/cmr9.pfb></home/<USER>/Library/texmf/fonts/type1
/public/amsfonts/cm/cmsy10.pfb></home/<USER>/Library/texmf/fonts/type1/pub
lic/amsfonts/cm/cmsy5.pfb></home/<USER>/Library/texmf/fonts/type1/public/a
msfonts/cm/cmsy6.pfb></home/<USER>/Library/texmf/fonts/type1/public/amsfon
ts/cm/cmsy7.pfb></home/<USER>/Library/texmf/fonts/type1/public/amsfonts/cm
/cmsy8.pfb></home/<USER>/Library/texmf/fonts/type1/public/amsfonts/cm/cmsy
9.pfb></home/<USER>/Library/texmf/fonts/type1/public/amsfonts/cm/cmti7.pfb
></home/<USER>/Library/texmf/fonts/type1/public/amsfonts/cm/cmti8.pfb></Us
ers/hungpq2412/Library/texmf/fonts/type1/public/amsfonts/cm/cmti9.pfb></home/<USER>
ungpq2412/Library/texmf/fonts/type1/public/amsfonts/symbols/msbm10.pfb></usr/lo
cal/texlive/2026basic/texmf-dist/fonts/type1/public/cm-super/sftt1000.pfb></usr
/local/texlive/2026basic/texmf-dist/fonts/type1/urw/helvetic/uhvr8a.pfb></usr/l
ocal/texlive/2026basic/texmf-dist/fonts/type1/urw/times/utmb8a.pfb></usr/local/
texlive/2026basic/texmf-dist/fonts/type1/urw/times/utmbi8a.pfb></usr/local/texl
ive/2026basic/texmf-dist/fonts/type1/urw/times/utmr8a.pfb></usr/local/texlive/2
026basic/texmf-dist/fonts/type1/urw/times/utmri8a.pfb>
Output written on main.pdf (52 pages, 912526 bytes).
Transcript written on main.log.
```

> TOOL

tool_use Bash
id: toolu_01CLrjPBVppJzSWgVMB4S1So
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/build2.log 2>&1; grep -E \"(Output written|! |Warning.*[Uu]ndefined)\" /tmp/build2.log | head -10",
  "description": "Second pass for refs"
}
```

> TOOL

tool_result
id: toolu_01CLrjPBVppJzSWgVMB4S1So
```
Output written on main.pdf (52 pages, 912526 bytes).
```

> TOOL

tool_use Bash
id: toolu_01F3U3aitYUzx819DWFgkcuv
```json
{
  "command": "grep -n \"page:end_main\" main.aux",
  "description": "Check end-of-main page"
}
```

> TOOL

tool_result
id: toolu_01F3U3aitYUzx819DWFgkcuv
```
165:\newlabel{page:end_main}{{5}{10}{Conclusion and Limitations}{section.5}{}}
```

> TOOL

tool_use Bash
id: toolu_0124QvEh7XEPynZYyz8sTtao
```json
{
  "command": "awk 'NR==568' /home/<USER>/neuralips26/main.tex | wc -w; awk 'NR>=64 && NR<=79' /home/<USER>/neuralips26/main.tex | wc -w",
  "description": "Count words after edit"
}
```

> TOOL

tool_result
id: toolu_0124QvEh7XEPynZYyz8sTtao
```
     171
     633
```

> AGENT

End of main is now on page 10 — need to verify this is still within limits.

> TOOL

tool_use Bash
id: toolu_016guuUVuCidMxxFaDBJLqER
```json
{
  "command": "git stash; pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/orig.log 2>&1; grep \"page:end_main\" main.aux; git stash pop",
  "description": "Check pre-edit page"
}
```

> TOOL

tool_result
id: toolu_016guuUVuCidMxxFaDBJLqER
```
Saved working directory and index state WIP on main: 657bc20 chore(submission): prepare anonymous double-blind code archive for NeurIPS 2026
\newlabel{page:end_main}{{5}{10}{Conclusion and Limitations}{section.5}{}}
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   main.tex

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (19a188727c8bb81bb19ec5cf9bc86b188e0ad873)
```

> TOOL

tool_use Bash
id: toolu_01STCgHxDsdmXKojVpVxt2XZ
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/final.log 2>&1; grep \"page:end_main\" main.aux; grep -c \"Output written\" /tmp/final.log",
  "description": "Recompile after restore"
}
```

> TOOL

tool_result
id: toolu_01STCgHxDsdmXKojVpVxt2XZ
```
\newlabel{page:end_main}{{5}{10}{Conclusion and Limitations}{section.5}{}}
1
```

> AGENT

Done. Build clean, no page regression (end-of-main stays on page 10, same as before).

- Intro: 645 → 633 words. Compacted the citation cluster in paragraph 1 (merged the "variants / observability / flow-matching / LLM-reprogrammed / billion-scale" sub-categories into a single umbrella phrase, citations preserved).
- Conclusion: 64 → 171 words. Added two sentences after the evidence summary: one reframing the contribution against optimization-side rescues (the 10.9% vs 54–80% contrast), one on the practical payoff ($R(\mathcal{D})$ as a pre-training go/no-go test + frozen-backbone deployment regime). Limitations expanded from one clause to two sentences (called out which backbones don't need the fix; added longer-horizon regimes alongside classification/anomaly detection).

> DEVELOPER

recompile

> TOOL

tool_use Bash
id: toolu_01RKKbWuYdXmTTAp2yx7sYUy
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/recompile.log 2>&1; pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/recompile2.log 2>&1; grep -E \"(Output written|! LaTeX Error|! Emergency|Undefined control)\" /tmp/recompile2.log | head -5; grep \"page:end_main\" main.aux",
  "description": "Recompile main.tex twice for refs"
}
```

> TOOL

tool_result
id: toolu_01RKKbWuYdXmTTAp2yx7sYUy
```
Output written on main.pdf (52 pages, 912526 bytes).
\newlabel{page:end_main}{{5}{10}{Conclusion and Limitations}{section.5}{}}
```

> AGENT

Build clean. 52 pages total, main content ends on page 10 (unchanged).

> DEVELOPER

frame our problem identification as a contribution because we discover this problem shall we ?

> AGENT

Contribution 1 already does this ("We identify *normalization-induced routing collapse*, an architectural failure mode … upstream of the optimization-induced collapses targeted by Switch/ST-MoE/ReMoE/Expert-Choice"), but the phrasing is modest. We could strengthen it by elevating "discovery of a new failure mode" to its own headline contribution (separate from the mechanism formalization in C2), and mirroring that framing in the abstract and the new conclusion paragraph — the tradeoff is that "we discovered a new problem" can read as overclaiming if reviewers feel the failure is a known MoE collapse in disguise (the eight controls + Table~\ref{tab:rescue} push back against this, but the framing has to be careful).

Want me to (a) just upgrade the contribution-1 wording in the intro, or (b) propagate "problem discovery" framing through abstract → intro → conclusion?

> DEVELOPER

the paths to the problem identification

> AGENT

The discovery path has three legs in the paper:

1. **Natural-extension failure**: Standard MoE recipe (AdaMix pool + hidden-state softmax router + Switch load-balancing) on MOMENT+RevIN → entropy collapses to 0.000 in most unfrozen configs. *We didn't go looking for this; the natural baseline broke.*
2. **Rule-out via optimization rescues**: $11$ MoE-collapse fixes from the literature (load balancing, z-loss, ReLU routing, expert-choice, …) recover at most $10.9\%$ MSE — establishing that this is *not* the optimization-induced collapse those papers target.
3. **Causal localization**: Eight controls (RevIN ablation, BatchNorm/GroupNorm swaps, router-input interpolation, MOMENT-vs-Timer-XL, vision cross-modality, $(\mu,\sigma)$ re-injection, AdaMix-Raw, Residual-IA) converge on the normalizer as cause; the predictor $R(\mathcal{D})$ then generalizes the diagnosis pre-training.

Should the contribution bullet be reframed around this *path* (failure → rule-out → localization), instead of just "we identify the failure mode"? That makes the discovery story explicit and pre-empts the "this is just standard MoE collapse" reviewer pushback. Want me to draft the reworked C1?

> DEVELOPER

take a look at this paper @/home/<USER>/Downloads/Vy_Nguyen_NeurIPS_2026\ \(35\).pdf

> TOOL

tool_use Bash
id: toolu_01VfUuypPTBTfUznhtVZcnqt
```json
{
  "command": "ls -la \"/home/<USER>/Downloads/Vy_Nguyen_NeurIPS_2026 (35).pdf\"",
  "description": "Check file exists and size"
}
```

> TOOL

tool_result
id: toolu_01VfUuypPTBTfUznhtVZcnqt
```
-rw-r--r--@ 1 hungpq2412  staff  10731625 May  5 13:19 /home/<USER>/Downloads/Vy_Nguyen_NeurIPS_2026 (35).pdf
```

> TOOL

tool_use Read
id: toolu_0164bhbx6DntTkbDXGh2S4Gc
```json
{
  "file_path": "/home/<USER>/Downloads/Vy_Nguyen_NeurIPS_2026 (35).pdf",
  "pages": "1-9"
}
```

> TOOL

tool_result
id: toolu_0164bhbx6DntTkbDXGh2S4Gc
```
PDF pages extracted: 9 page(s) from /home/<USER>/Downloads/Vy_Nguyen_NeurIPS_2026 (35).pdf (10.2MB)
```

> AGENT

Read it. It's structurally aligned with what you were asking about — it makes "Problem Formulation" an explicit, named contribution. Direct parallels to ours:

| Their paper (CAC) | Our paper (RR-MoA) |
|---|---|
| **C1 Problem Formulation:** "unsupported commitment" — control failure ≠ knowledge failure; introduce *commit-abstain margin* | **C1 should be:** *normalization-induced routing collapse* — input failure ≠ optimization failure; introduce *signal-ratio* $R(\mathcal{D})$ |
| **C2 Mechanistic Finding:** sparse CAC subset; "accumulate-yet-undercorrect" pattern | **C2:** MI decomposition + 8 causal controls localizing the normalizer |
| **C3 Policy Improvement:** lightweight MLP on CAC activations | **C3:** RR-MoA / SR-MoA / Residual-IA⁺ |

What they do well that we could adopt:

1. **Name the phenomenon, name the metric.** "Unsupported commitment" + "commit-abstain margin" are paired in C1. We have the phenomenon name ("normalization-induced routing collapse") but bury the metric ($R(\mathcal{D})$) in C2 — pulling it up into C1 ties discovery to measurement, mirroring their formulation.
2. **Sharp dichotomy framing.** "Control failure rather than knowledge failure" is one line and immediately separates them from the detection/abstention literature. Our analog: "router-input failure rather than router-optimization failure" — directly rules out Switch/ST-MoE/ReMoE/Expert-Choice.
3. **Conclusion echoes the framing.** Their conclusion opens with the […]