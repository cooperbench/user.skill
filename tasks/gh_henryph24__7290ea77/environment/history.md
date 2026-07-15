> DEVELOPER

subtitle named such as: "Headline numbers", "Generalization and falsifiable boundary"

> TOOL

tool_use Bash
id: toolu_019DpKy5sssdKfZgX8pXTb8e
```json
{
  "command": "grep -n \"Headline\\|falsifiable boundary\\|paragraph{\" main.tex | head -100",
  "description": "Find subtitle paragraphs in main.tex"
}
```

> TOOL

tool_result
id: toolu_019DpKy5sssdKfZgX8pXTb8e
```
512:Observation~\ref{thm:mi_decomp} and $R(\mathcal{D})$ make three testable predictions: the bound is empirically tight, $R(\mathcal{D})$ predicts raw-routing benefit across datasets, and the predictor respects a falsifiable boundary distinct from a generic-SNR explanation. We verify each in turn, then turn to the rescues the mechanism predicts must fail.
514:\textbf{$R(\mathcal{D})$ predicts raw-routing benefit and respects a falsifiable boundary.} The bound is empirically tight (Appendix~\ref{app:mi_tightness}) and the learnable mixing coefficient satisfies $\alpha{<}0.5$ on $30/30$ runs (Appendix~\ref{app:learnable_alpha}). $R(\mathcal{D})$ predicts raw-routing benefit at Spearman $\rho{=}{-}0.88$ ($p{<}0.002$, $n{=}9$; Figure~\ref{fig:signal_ratio}), whereas the conditional entropy $H(E\mid S)$ does not ($\rho{=}{-}0.12$); Traffic ($R{=}0.14$) is a boundary, Solar ($R{=}0.06$) the one outlier (Appendix~\ref{app:routing_ablations}). The discriminating power lies in the boundary case: the most likely competing explanation is that $R(\mathcal{D})$ proxies generic ``hard dataset'' signal-to-noise, but Traffic has high overall predictability (DLinear MSE $0.41$) yet low $R$, and RR-MoA correctly does not improve there, falsifying the SNR alternative. $R(\mathcal{D})$ is therefore actionable pre-training: practitioners can compute it from raw dataset statistics to predict whether raw routing will help on a new dataset.
526:\subsubsection*{Headline numbers}
561:{\looseness=-1 \textbf{Generalization and falsifiable boundary.}\label{sec:cross_backbone}\label{sec:topk} The diagnosis transfers: RR-MoA wins on every instance-normalized backbone (MOMENT-small/large $26$--$79\%/32$--$75\%$, Moirai $12$--$29\%$, Moirai-MoE~\citep{liu2025moiraimoe} $37$--$90\%$); LayerNorm-only Chronos and Timer-XL~\citep{liu2025timerxl} show […]

> TOOL

tool_use Bash
id: toolu_01U6Ug3L4DuZmgH8snmppTFV
```json
{
  "command": "grep -n \"subsubsection\\*\\|subsection{\" main.tex | head -50",
  "description": "Find subsubsection and subsection headings"
}
```

> TOOL

tool_result
id: toolu_01U6Ug3L4DuZmgH8snmppTFV
```
413:\subsection{Setup}
423:\subsection{Main Results}
428:\subsubsection*{Diagnosis: adapters underperform, MoE collapses}
510:\subsubsection*{Empirical verification of the mechanism}
518:\subsubsection*{Standard rescues fail; the raw-input principle generalizes}
526:\subsubsection*{Headline numbers}
1142:\subsection{Inference Benchmark}
1239:\subsection{Theoretical Depth of Observation~\ref{thm:mi_decomp}}
1699:\subsection{Statistics Re-Injection Ablation}
1788:\subsection{Rescue-Baseline Sweep Details}
1820:\subsection{AdaMix Implementation Details}
1883:\subsection{Cross-Modality Control: Vision MoE}
1940:\subsection{Expert Pool Diversity Ablation}
1964:\subsection{Expert Count Scaling}
2414:\subsection{Residual-IA: Closing the Remaining Gap}
2634:\subsubsection*{Residual-IA\textsuperscript{+}: closing the remaining gap to 5/6}
2710:\subsubsection*{Multi-horizon generalization: H${\in}\{96, 192, 336, 720\}$}
2737:\subsubsection*{Cross-backbone generalization: does Residual-IA\textsuperscript{+} depend on RevIN?}
2815:\subsection{SR-RIA\textsuperscript{+}: Self-Routed Residual-IA\textsuperscript{+}}
2841:\subsection{Pure Raw-MLP MoE Ablation: Quantifying the TSFM's Contribution}
```

> TOOL

tool_use Read
id: toolu_01RjTHBGaS6DppzZywNzH5Pg
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 420,
  "limit": 160
}
```

> TOOL

tool_result
id: toolu_01RjTHBGaS6DppzZywNzH5Pg
```
420	
421	\textbf{Training and statistics.} Adam ($\eta{=}10^{-3}$), MSE loss, $15$ epochs, batch $128$; $5$ seeds for the core grid, $3$ for ablations. Significance via Wilcoxon signed-rank, Bonferroni-corrected over 6 datasets $\times$ 5 seeds ($^{*}\!/^{**}\!/^{***}$ for $p{<}0.05/0.01/0.001$). Full hyperparameters in App.~\ref{app:setup}; on acceptance we release the code, the $5{,}463$ per-run JSONs, and a \texttt{verify.py} script that re-derives all $107$ numeric claims within tolerance ($234.8$ measured GPU-hours on a single A10G; license + per-backbone breakdown in the Paper Checklist).
422	
423	\subsection{Main Results}
424	\label{sec:main_results}
425	
426	With this setup fixed, we now turn to the empirical verification of the mechanism formalized in \S\ref{sec:mechanism} (Observation~\ref{thm:mi_decomp}, $R(\mathcal{D})$). The case rests on three claims that the mechanism predicts and that we test in turn: fixed-topology adapters are suboptimal, the natural MoE remedy collapses on instance-normalized backbones, and standard rescue mechanisms cannot recover it. We then compare against the seven-baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full fine-tuning, DLinear).
427	
428	\subsubsection*{Diagnosis: adapters underperform, MoE collapses}
429	
430	{\looseness=-1 \textbf{RR-MoA vs.\ fixed adapters.} Table~\ref{tab:rrmoa} compares Top-2 RR-MoA against the best fixed adapter, using the \emph{same five expert heads} in all rows. Across the primary 6-dataset LTSF grid $\times$ 3 […]

> AGENT

Your message looks truncated — I see only "subtitle named such as: 'Headline numbers', 'Generalization and falsifiable boundary'" without a verb/instruction.

Just so we're on the same page, in `main.tex` (Section 4 Main Results) I see four `\subsubsection*` titles plus one bold paragraph header acting as a fifth title:

- L428 `\subsubsection*{Diagnosis: adapters underperform, MoE collapses}`
- L510 `\subsubsection*{Empirical verification of the mechanism}`
- L518 `\subsubsection*{Standard rescues fail; the raw-input principle generalizes}`
- L526 `\subsubsection*{Headline numbers}`
- L561 `\textbf{Generalization and falsifiable boundary.}` (paragraph-level, not a real subsubsection)

What would you like me to do — promote `Generalization and falsifiable boundary` to a `\subsubsection*` to match the others, rename them, add new ones, or something else?