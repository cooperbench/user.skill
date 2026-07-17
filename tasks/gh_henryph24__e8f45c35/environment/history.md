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