> DEVELOPER

Let's now review the main article Passes by Passes to see if we're making a broad transition and to make sure that we are smoothly linking the parts.

> TOOL

tool_use Bash
id: toolu_01BEToM4fUF1WVdRmzCoHNGe
```json
{
  "command": "wc -l /home/<USER>/neuralips26/main.tex",
  "description": "Count lines in main.tex"
}
```

> TOOL

tool_result
id: toolu_01BEToM4fUF1WVdRmzCoHNGe
```
    2862 /home/<USER>/neuralips26/main.tex
```

> TOOL

tool_use Bash
id: toolu_01JoLq6mpPzZJmEg6SZWXM7W
```json
{
  "command": "grep -n -E \"^\\\\\\\\(section|subsection|subsubsection|begin\\\\{abstract\\\\}|end\\\\{abstract\\\\})\" /home/<USER>/neuralips26/main.tex",
  "description": "Find all section structure in main.tex"
}
```

> TOOL

tool_result
id: toolu_01JoLq6mpPzZJmEg6SZWXM7W
```
57:\begin{abstract}
59:\end{abstract}
61:\section{Introduction}
228:\section{Related Work}
238:\section{Raw-Routed Mixture of Adapters (RR-MoA)}
392:\section{Experiments}
394:\subsection{Setup}
404:\subsection{Main Results}
409:\subsubsection*{Diagnosis: adapters underperform, MoE collapses}
491:\subsubsection*{Mechanism: instance normalization strips the routing signal}
505:\subsubsection*{Standard rescues fail; the raw-input principle generalizes}
511:\subsubsection*{Headline numbers}
550:\section{Conclusion and Limitations}
1042:\section{Experimental Setup Details}
1119:\section{Deployment-Regime Motivation}
1130:\subsection{Inference Benchmark}
1159:\section{Multi-Horizon Evaluation}
1183:\section{Proposition Proofs}
1225:\subsection{Theoretical Depth of Observation~\ref{thm:mi_decomp}}
1333:\section{LoRA Sweep (Full Results)}
1398:\section{Routing Ablations}
1683:\subsection{Statistics Re-Injection Ablation}
1709:\section{Extended RR-MoA Freeze Grid}
1772:\subsection{Rescue-Baseline Sweep Details}
1804:\subsection{AdaMix Implementation Details}
1842:\section{Normalization Generalization}
1867:\subsection{Cross-Modality Control: Vision MoE}
1898:\section{Top-$k$ Sparse Routing Ablation}
1924:\subsection{Expert Pool Diversity Ablation}
1948:\subsection{Expert Count Scaling}
1974:\section{Imputation Results}
2002:\section{Learnable Normalization Coefficient}
2028:\section{Exact MI Loss and Bound Tightness}
2059:\section{Information Content Diagnostic}
2178:\section{Cross-Backbone RR-MoA}
2271:\section{Extended Full Fine-Tuning Ablation}
2337:\section{Closing the DLinear Gap}
2398:\subsection{Residual-IA: Closing the Remaining Gap}
2618:\subsubsection*{Residual-IA\textsuperscript{+}: closing the remaining gap to 5/6}
2694:\subsubsection*{Multi-horizon generalization: H${\in}\{96, 192, 336, 720\}$}
2721:\subsubsection*{Cross-backbone generalization: does Residual-IA\textsuperscript{+} depend on RevIN?}
2797:\subsection{SR-RIA\textsuperscript{+}: Self-Routed Residual-IA\textsuperscript{+}}
2823:\subsection{Pure Raw-MLP MoE Ablation: Quantifying the TSFM's Contribution}
```

> AGENT

I'll review the paper section by section, checking transitions and narrative flow. Let me start with the opening (abstract + intro).

> TOOL

tool_use Read
id: toolu_019xD1TuFLU8D26MwktmbfhP
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 57,
  "limit": 230
}
```

> TOOL

tool_result
id: toolu_019xD1TuFLU8D26MwktmbfhP
```
57	\begin{abstract}
58	Many time series foundation models (TSFMs) adapt to a target dataset by attaching a single trainable head to a frozen backbone. A single head is one-size-fits-all, yet target series mix heterogeneous regimes that a single head may underfit. The natural upgrade is to replace the single head with a mixture-of-experts (MoE) head whose router dispatches each window to a specialist. This upgrade fails on instance-normalized backbones, a dominant TSFM design class that strips each window's mean and variance before encoding. We call this failure \emph{normalization-induced routing collapse}. Once joint training makes even one backbone transformer block trainable, routing entropy falls to $0.000$. Every input is sent to a single expert; the rest are never activated. A $720$-run sweep across standard MoE rescue mechanisms recovers at most $10.9\%$ MSE, $2.7\times$ worse than our causal intervention. The failure is in the router's input, not its optimization. We formalize this via a mutual-information decomposition. The resulting signal-ratio statistic is computable before training and predicts dataset vulnerability (Spearman $\rho{=}{-}0.88$, $p{<}0.002$). The diagnosis prescribes a minimal causal intervention: \emph{Raw-Routed Mixture of Adapters} (RR-MoA) routes on the raw, pre-normalization input. RR-MoA sets a new state of the art for […]

> AGENT

Now let me read the Method section and key Experiment transitions.

> TOOL

tool_use Read
id: toolu_01GihAQ9n3ymagMWMtgVicQd
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 380,
  "limit": 170
}
```

> TOOL

tool_result
id: toolu_01GihAQ9n3ymagMWMtgVicQd
```
380	\end{cases}
381	\end{aligned}
382	\label{eq:rrmoa}
383	\end{equation}
384	where $G_\psi: \mathbb{R}^{T} \to \mathbb{R}^K$ is a small Conv1d\,+\,pooling\,+\,linear gate ($853$ params) operating directly on the raw time series, $\mathcal{T} \subset \{1,\ldots,K\}$ is the set of Top-$k$ indices, and each $\mathrm{Expert}_j$ is a canonical adapter head. By construction $\sum_j \widetilde{w}_j = 1$ with support only on $\mathcal{T}$, so only $k$ of $K$ experts execute per sample. With $K{=}5$, $k{=}2$ we obtain $40\%$ of the dense expert FLOPs while retaining $63\%$ of the dense MSE improvement over the best fixed adapter (\S\ref{sec:topk}). Routing on raw input preserves the temporal statistics (trend, amplitude, volatility) that RevIN strips away.
385	
386	\textbf{Inference cost and deployment.} The router is a Conv1d gate of $853$ parameters ($0.4\%$ of one expert head, ${<}10^{-3}$ of the frozen backbone). With $k{=}2$ of $K{=}5$ experts active per window, RR-MoA adds two adapter forward passes plus the gate to one frozen TSFM forward; the unselected $K{-}k$ experts do not execute. Because the backbone is strictly frozen, a single TSFM held in GPU memory can be shared across many tenants while per-task adapter pools (${\sim}500$K params each) are hot-swapped from host RAM, an arrangement DLinear and per-dataset-from-scratch baselines […]

> AGENT

Let me read the conclusion and appendix transitions, plus check the method→experiments junction more carefully.

> TOOL

tool_use Read
id: toolu_01R872eKiVjWPuoT6gcBWyD1
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 285,
  "limit": 110
}
```

> TOOL

tool_result
id: toolu_01R872eKiVjWPuoT6gcBWyD1
```
285	\node[hiddenbox] (hidden) at (6.8, 1.8) {
286	    $\mathbf{H}$\\[-2pt]
287	    {\scriptsize hidden}\\[-2pt]
288	    {\scriptsize states}
289	};
290	
291	% ====== PATH B: CONV1D GATE (bottom) ======
292	\node[gatebox] (gate) at (3.5, -1.8) {
293	    \textbf{Conv1d Gate}\\[-2pt]
294	    {\scriptsize 853 params}
295	};
296	
297	% Top-K
298	\node[topkbox] (topk) at (6.8, -1.8) {
299	    \textbf{Top-2}\\[-2pt]
300	    {\scriptsize sparse}
301	};
302	
303	% ====== EXPERT POOL (right) ======
304	\node[expertinactive] (e1) at (9.8, 3.2) {Mean Pool};
305	\node[expertactive]   (e2) at (9.8, 2.0) {\textbf{Last Token}};
306	\node[expertinactive] (e3) at (9.8, 0.8) {Max Pool};
307	\node[expertactive]   (e4) at (9.8, -0.4) {\textbf{Attention}};
308	\node[expertinactive] (e5) at (9.8, -1.6) {Conv1d};
309	
310	% Expert pool bracket label. Use a plain right-side bracket (vertical line with
311	% small inward end caps at top and bottom) instead of a curly brace, because the
312	% brace's mid-curl bumps out right at Max Pool's vertical center and reads as a
313	% second bracket starting there.
314	\draw[gray!60, line width=0.6pt, line cap=round]
315	    (10.95, 3.55) -- (11.05, 3.55) -- (11.05, -1.95) -- (10.95, -1.95);
316	% Center the label under the bracket and pull inward so it never crosses the
317 […]

> TOOL

tool_use Read
id: toolu_014YKmUdtJjXxXyDmxbzEZLb
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 549,
  "limit": 200
}
```

> TOOL

tool_result
id: toolu_014YKmUdtJjXxXyDmxbzEZLb
```
549	\vspace{-0.5em}
550	\section{Conclusion and Limitations}
551	\vspace{-0.4em}
552	
553	{\looseness=-1 \textbf{Diagnosis and fix.} We identified \emph{normalization-induced routing collapse}: instance-normalized TSFMs collapse a downstream MoE adapter to one expert because the same $(\mu,\sigma)$ stripping that handles distribution shift removes the routing signal. Observation~\ref{thm:mi_decomp} formalizes the loss, $R(\mathcal{D})$ predicts it ($\rho{=}{-}0.88$), and eight causal controls rule out optimization, geometry, and routing-paradigm explanations; three interventions confirm it -- RR-MoA ($54/54$), SR-MoA ($+13$--$42\%$), Residual-IA\textsuperscript{+} ($107/123$). \textbf{Limitations.} The diagnosis is specific to per-window $(\mu,\sigma)$-stripping normalizers; $R(\mathcal{D})$ is a proxy not a threshold; classification/anomaly detection and learned expert pools remain open.\label{page:end_main}}
554	\bibliographystyle{plainnat}
555	\begin{thebibliography}{20}
556	
557	\bibitem[Dosovitskiy et~al.(2021)]{dosovitskiy2021vit}
558	Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby.
559	\newblock An image is worth 16x16 words: Transformers for image recognition at scale.
560	\newblock In \textit{International Conference on Learning Representations (ICLR)}, 2021.
561	
562	\bibitem[Goswami et~al.(2024)]{goswami2024moment}
563	Mononito Goswami, Konrad Szafer, Arjun Choudhry, Yifu Cai, Shuo Li, and Artur Dubrawski.
564	\newblock {MOMENT}: A family of open time-series foundation models.
565	\newblock In \textit{Proceedings of the 41st International Conference on Machine Learning (ICML)}, volume […]

> AGENT

Now let me check the appendix structure and key transitions.

> TOOL

tool_use Bash
id: toolu_01Q6hhVWAPwYXPhZzXukaqQY
```json
{
  "command": "grep -n -E \"^(\\\\\\\\appendix|\\\\\\\\section|\\\\\\\\subsection)\" /home/<USER>/neuralips26/main.tex | head -80",
  "description": "Find appendix marker and section structure"
}
```

> TOOL

tool_result
id: toolu_01Q6hhVWAPwYXPhZzXukaqQY
```
61:\section{Introduction}
228:\section{Related Work}
238:\section{Raw-Routed Mixture of Adapters (RR-MoA)}
392:\section{Experiments}
394:\subsection{Setup}
404:\subsection{Main Results}
550:\section{Conclusion and Limitations}
1030:\appendix
1042:\section{Experimental Setup Details}
1119:\section{Deployment-Regime Motivation}
1130:\subsection{Inference Benchmark}
1159:\section{Multi-Horizon Evaluation}
1183:\section{Proposition Proofs}
1225:\subsection{Theoretical Depth of Observation~\ref{thm:mi_decomp}}
1333:\section{LoRA Sweep (Full Results)}
1398:\section{Routing Ablations}
1683:\subsection{Statistics Re-Injection Ablation}
1709:\section{Extended RR-MoA Freeze Grid}
1772:\subsection{Rescue-Baseline Sweep Details}
1804:\subsection{AdaMix Implementation Details}
1842:\section{Normalization Generalization}
1867:\subsection{Cross-Modality Control: Vision MoE}
1898:\section{Top-$k$ Sparse Routing Ablation}
1924:\subsection{Expert Pool Diversity Ablation}
1948:\subsection{Expert Count Scaling}
1974:\section{Imputation Results}
2002:\section{Learnable Normalization Coefficient}
2028:\section{Exact MI Loss and Bound Tightness}
2059:\section{Information Content Diagnostic}
2178:\section{Cross-Backbone RR-MoA}
2271:\section{Extended Full Fine-Tuning Ablation}
2337:\section{Closing the DLinear Gap}
2398:\subsection{Residual-IA: Closing the Remaining Gap}
2797:\subsection{SR-RIA\textsuperscript{+}: Self-Routed Residual-IA\textsuperscript{+}}
2823:\subsection{Pure Raw-MLP MoE Ablation: Quantifying the TSFM's Contribution}
```

> TOOL

tool_use ToolSearch
id: toolu_01Bj2WAg8S83BcCMbAHe9ZVT
```json
{
  "query": "select:TaskCreate,TaskUpdate,TaskList",
  "max_results": 3
}
```

> TOOL

tool_result
id: toolu_01Bj2WAg8S83BcCMbAHe9ZVT
```
{
  "type": "tool_reference",
  "tool_name": "TaskCreate"
}
{
  "type": "tool_reference",
  "tool_name": "TaskUpdate"
}
{
  "type": "tool_reference",
  "tool_name": "TaskList"
}
```

> TOOL

tool_use TaskCreate
id: toolu_018VUowJxpdSCmsCnkQuHPbE
```json
{
  "subject": "Review Pass 1: Abstract → Intro",
  "description": "Check that abstract sets up intro themes and the intro opens by picking up exactly where the abstract leaves off.",
  "activeForm": "Reviewing abstract→intro transition"
}
```

> TOOL

tool_result
id: toolu_018VUowJxpdSCmsCnkQuHPbE
```
Task #1 created successfully: Review Pass 1: Abstract → Intro
```

> TOOL

tool_use TaskCreate
id: toolu_01VENgAG6YQkMKk6VUWVqyDD
```json
{
  "subject": "Review Pass 2: Intro → Related Work",
  "description": "Verify the contributions list (lines 75-79) flows into the Related Work and that related work is positioned around RR-MoA's diagnosis claim.",
  "activeForm": "Reviewing intro→related-work transition"
}
```

> TOOL

tool_result
id: toolu_01VENgAG6YQkMKk6VUWVqyDD
```
Task #2 created successfully: Review Pass 2: Intro → Related Work
```

> TOOL

tool_use TaskCreate
id: toolu_01624CBBBrqKGo1437ob9mKa
```json
{
  "subject": "Review Pass 3: Related Work → Method",
  "description": "Check that §3 Method opens off the related-work positioning and that the problem setup, equation 1, and architectural intro are linked smoothly.",
  "activeForm": "Reviewing related-work→method transition"
}
```

> TOOL

tool_result
id: toolu_01624CBBBrqKGo1437ob9mKa
```
Task #3 created successfully: Review Pass 3: Related Work → Method
```

> TOOL

tool_use TaskCreate
id: toolu_01GinQRRdetqq1srBQhbqwzU
```json
{
  "subject": "Review Pass 4: Method → Experiments",
  "description": "Verify the closing line of method (line 390) sets up Setup→Main Results, and that the four claim threads are clearly previewed.",
  "activeForm": "Reviewing method→experiments transition"
}
```

> TOOL

tool_result
id: toolu_01GinQRRdetqq1srBQhbqwzU
```
Task #4 created successfully: Review Pass 4: Method → Experiments
```

> TOOL

tool_use TaskCreate
id: toolu_01Tf7u3tHyErWsQHGCMQQ4Vx
```json
{
  "subject": "Review Pass 5: Within Main Results subsection transitions",
  "description": "Check the four \\subsubsection*{} arcs: Diagnosis → Mechanism → Standard rescues → Headline numbers. Make sure each opens by referencing the prior block.",
  "activeForm": "Reviewing main-results subsection arcs"
}
```

> TOOL

tool_result
id: toolu_01Tf7u3tHyErWsQHGCMQQ4Vx
```
Task #5 created successfully: Review Pass 5: Within Main Results subsection transitions
```

> AGENT

API Error: Stream idle timeout - partial response received

> TOOL

tool_use TaskCreate
id: toolu_011rFewA7xWyc8hjotWZ5sMq
```json
{
  "subject": "Review Pass 6: Main Results → Conclusion",
  "description": "Verify the closing of §4 (lines 543-547) flows into the Conclusion+Limitations on line 553.",
  "activeForm": "Reviewing main-results→conclusion transition"
}
```

> TOOL

tool_result
id: toolu_011rFewA7xWyc8hjotWZ5sMq
```
Task #6 created successfully: Review Pass 6: Main Results → Conclusion
```

> TOOL

tool_use TaskCreate
id: toolu_01JfiuAqsRaTww7uxoAVHZbX
```json
{
  "subject": "Review Pass 7: Conclusion + Appendix linkage",
  "description": "Check that the conclusion is the genuine close of the body and that the appendix sections (App A: Setup → App P: DLinear gap) open in a coherent order with cross-references back to the body.",
  "activeForm": "Reviewing body→appendix linkage"
}
```

> TOOL

tool_result
id: toolu_01JfiuAqsRaTww7uxoAVHZbX
```
Task #7 created successfully: Review Pass 7: Conclusion + Appendix linkage
```

> TOOL

tool_use TaskCreate
id: toolu_01UxpEzqjtFvrkoUja5Tt7av
```json
{
  "subject": "Synthesize findings + propose targeted edits",
  "description": "Aggregate per-pass observations into a concise list of (a) transitions that already work, (b) rough edges that need a sentence-level fix, (c) any missing forward/backward pointers between sections.",
  "activeForm": "Synthesizing findings"
}
```

> TOOL

tool_result
id: toolu_01UxpEzqjtFvrkoUja5Tt7av
```
Task #8 created successfully: Synthesize findings + propose targeted edits
```

> TOOL

tool_use TaskUpdate
id: toolu_01RwumyUzrQMVTmiAYRVNRhT
```json
{
  "taskId": "1",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01RwumyUzrQMVTmiAYRVNRhT
```
Updated task #1 status
```

> AGENT

Let me check the appendix opening and a few key cross-section transitions.

> TOOL

tool_use Read
id: toolu_01WZeCqQn1jGY6DjhB9XK8As
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 1025,
  "limit": 100
}
```

> TOOL

tool_result
id: toolu_01WZeCqQn1jGY6DjhB9XK8As
```
1025	\newblock In \textit{Advances in Neural Information Processing Systems (NeurIPS)}, 2023.
1026	
1027	\end{thebibliography}
1028	
1029	\newpage
1030	\appendix
1031	\renewcommand{\thetable}{\Alph{section}.\arabic{table}}
1032	\renewcommand{\thefigure}{\Alph{section}.\arabic{figure}}
1033	\makeatletter
1034	\@addtoreset{table}{section}
1035	\@addtoreset{figure}{section}
1036	\makeatother
1037	\setcounter{table}{0}
1038	\setcounter{figure}{0}
1039	
1040	% Routing entropy figure moved to main text (Figure 2)
1041	
1042	\section{Experimental Setup Details}
1043	\label{app:setup}
1044	
1045	\paragraph{Notation.} Table~\ref{tab:notation} consolidates symbols used across \S\ref{sec:method}--\S\ref{sec:main_results}, Observation~\ref{thm:mi_decomp}, and Appendix~\ref{app:proofs}.
1046	
1047	\begin{table}[!htbp]
1048	\centering
1049	\caption{\textbf{Notation.} Symbols used throughout the paper.}
1050	\label{tab:notation}
1051	\small
1052	\setlength{\tabcolsep}{6pt}
1053	\begin{tabular}{@{}ll@{}}
1054	\toprule
1055	\textbf{Symbol} & \textbf{Meaning} \\
1056	\midrule
1057	\multicolumn{2}{@{}l}{\emph{Data and task}} \\
1058	$\mathbf{x}\in\mathbb{R}^{T\times c}$ & Input window: $T{=}512$ time steps, $c$ channels \\
1059	$\mathbf{y}\in\mathbb{R}^{h\times c}$ & Forecast target at horizon $h\in\{96,192,336,720\}$ \\
1060	$\hat{\mathbf{y}}$ & Model prediction \\
1061	$M_i, \Sigma_i, \mathbf{S}_i$ & Per-window mean, scale, RevIN-normalized shape ($\mathbf{S}_i{=}(\mathbf{x}_i{-}M_i)/\Sigma_i$) \\
1062	\midrule
1063	\multicolumn{2}{@{}l}{\emph{Backbone and adapter}} \\
1064	$f_\theta:\mathbb{R}^{T\times c}\to\mathbb{R}^{P\times d}$ & Pretrained TSFM feature extractor; $\theta$ frozen ($\nabla_\theta\equiv 0$) \\
1065	$\mathbf{H}{=}f_\theta(\mathbf{x})$ & Backbone hidden states ($P$ patches of dim $d$) \\
1066	$g_\phi:\mathbb{R}^{P\times d}\to\mathbb{R}^{h\times c}$ & Adapter; $|\phi|\leq 500$K trainable params \\
1067	\midrule
1068	\multicolumn{2}{@{}l}{\emph{Mixture and routing}} \\
1069	$K$ & Total expert […]

> AGENT

I have enough to do the synthesis. Let me complete the review passes and write up findings.

> TOOL

tool_use TaskUpdate
id: toolu_01FhPHihWQk8gfLenNkP2wwd
```json
{
  "taskId": "1",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01FhPHihWQk8gfLenNkP2wwd
```
Updated task #1 status
```

> TOOL

tool_use TaskUpdate
id: toolu_01K1SqUnXo6dUyFWvsZ9etuh
```json
{
  "taskId": "2",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01K1SqUnXo6dUyFWvsZ9etuh
```
Updated task #2 status
```

> TOOL

tool_use TaskUpdate
id: toolu_015UmqLRmJowZk1sgQbef3X3
```json
{
  "taskId": "3",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_015UmqLRmJowZk1sgQbef3X3
```
Updated task #3 status
```

> TOOL

tool_use TaskUpdate
id: toolu_01JNqT1u64d3rMgKqsn3KpUQ
```json
{
  "taskId": "4",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01JNqT1u64d3rMgKqsn3KpUQ
```
Updated task #4 status
```

> TOOL

tool_use TaskUpdate
id: toolu_01XVcWJGhsiQB3GxwLzfAXU4
```json
{
  "taskId": "5",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01XVcWJGhsiQB3GxwLzfAXU4
```
Updated task #5 status
```

> TOOL

tool_use TaskUpdate
id: toolu_012pka3caNLbsJv3qWYNfyqv
```json
{
  "taskId": "6",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_012pka3caNLbsJv3qWYNfyqv
```
Updated task #6 status
```

> TOOL

tool_use TaskUpdate
id: toolu_01KfoXeMyPGGJWt9cBehfh4S
```json
{
  "taskId": "7",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01KfoXeMyPGGJWt9cBehfh4S
```
Updated task #7 status
```

> TOOL

tool_use TaskUpdate
id: toolu_01RafvoyzsgnrtrX69HDaJW1
```json
{
  "taskId": "8",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01RafvoyzsgnrtrX69HDaJW1
```
Updated task #8 status
```

> AGENT

## Pass-by-pass transition review

### Transitions that already work
1. **Related Work → Method (line 236 → 238)**: closes with "Section~\ref{sec:method} formalizes this and presents the minimal architectural fix." Clean forward pointer.
2. **Method → Experiments (line 390 → 392)**: ends "We now validate that this fix recovers routing diversity, beats the seven-method baseline suite [...] and holds under eight causal controls." The verbs preview the four claim blocks.
3. **Setup → Main Results (line 404 → 407)**: explicit roadmap "RR-MoA's case rests on three claims: ..."
4. **Headline → Conclusion (line 547 → 553)**: the boundary-case remark ($R(\mathcal{D})$ as an a-priori go/no-go test) lands naturally on "Diagnosis and fix."

### Rough edges worth a sentence-level fix

| # | Where | Issue | Suggested fix |
|---|---|---|---|
| 1 | **Intro paras 1–3** (lines 64–68) | Intro restates the abstract almost beat-for-beat for ~half a page (single-head adapter → MoE upgrade → RevIN collapse). Conventional but page-9 budget is tight. | Tighten para 2 or merge it into para 1; you don't need two passes at "single head is one-size-fits-all". |
| 2 | **Intro → Related Work (line 79 → 230)** | Related Work dives straight into "TSFM […]

> TOOL

tool_use TaskUpdate
id: toolu_01HMJVAhh5HxpPqdtR45Y9Mf
```json
{
  "taskId": "8",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01HMJVAhh5HxpPqdtR45Y9Mf
```
Updated task #8 status
```

> AGENT

Want me to apply edges 2/3/4/5 in `main.tex` and recompile, or would you like to review the wording first?

> DEVELOPER

let's do it

> TOOL

tool_use Read
id: toolu_01BMyszLetiD1zs8HZr3s7gU
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 228,
  "limit": 3
}
```

> TOOL

tool_result
id: toolu_01BMyszLetiD1zs8HZr3s7gU
```
228	\section{Related Work}
229	
230	\textbf{TSFM Adaptation.} For broader context we refer to the survey by~\citet{wen2023tssurvey}. A complementary line shows that compact task-specific models match or beat heavyweight pretrained backbones on LTSF benchmarks~\citep{wu2025srsnet, wang2025timemixerpp, xu2024fits, chen2023tsmixer, fu2025selective}: that lightweight raw-input models are competitive is itself evidence that the per-window raw signal carries most of the predictability our diagnostic $R(\mathcal{D})$ exploits (\S\ref{sec:diagnosis}). LLM-reprogrammed forecasters~\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes} inherit per-window normalization upstream of the backbone, so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is attached. We focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a lightweight module to a frozen TSFM~\citep{hu2022lora, houlsby2019adapters, goswami2024moment}; recent variations explore multi-scale finetuning~\citep{qiao2025msft}, importance-based LoRA selection~\citep{li2025trace}, input-representation adaptation~\citep{benechehab2025adapts}, structured pruning~\citep{zhao2025prune}, in-context tuning~\citep{faw2025icf}, retrieval-augmented adaptation~\citep{ning2025tsrag}, and Chronos-specific PEFT~\citep{gupta2024beyondlora}; complementary work computes transferability scores for backbone selection (TEMPLATE, \citealp{zhang2025template}) or provides a unified evaluation suite (GIFT-Eval, \citealp{woo2024gifteval}). These vary the finetuning \textit{strategy} while leaving per-input adapter \textit{topology} fixed; AdaPTS reports the best of several variants per dataset/horizon, treating adapter choice as a per-task hyperparameter rather than per-window routing. We instead route over heterogeneous expert topologies per window; the closest precedent in spirit is mixture-of-adapters in the LLM […]

> AGENT

Edge 2: add positioning lead to Related Work.

> TOOL

tool_use Edit
id: toolu_01FdAXCAYgVxgqj5mg3h8t2w
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "\\section{Related Work}\n\n\\textbf{TSFM Adaptation.} For broader context we refer to the survey by~\\citet{wen2023tssurvey}.",
  "new_string": "\\section{Related Work}\n\nWe position RR-MoA against four threads: TSFM adaptation, MoE in foundation models, MoE routing collapse and rescue, and time-series normalization.\n\n\\textbf{TSFM Adaptation.} For broader context we refer to the survey by~\\citet{wen2023tssurvey}."
}
```

> TOOL

tool_result
id: toolu_01FdAXCAYgVxgqj5mg3h8t2w
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> AGENT

Edge 3: fix "three claims" roadmap mismatch.

> TOOL

tool_use Edit
id: toolu_012wiA3N8GUKf3q7W6jqRj9Q
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "RR-MoA's case rests on three claims: fixed-topology adapters are suboptimal, the natural MoE remedy collapses on instance-normalized backbones, and standard rescue mechanisms cannot recover it. We establish each before comparing against the seven-baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full fine-tuning, DLinear).",
  "new_string": "RR-MoA's case rests on three claims and the mechanism that explains them: fixed-topology adapters are suboptimal, the natural MoE remedy collapses on instance-normalized backbones, and standard rescue mechanisms cannot recover it. We establish each in turn before comparing against the seven-baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full fine-tuning, DLinear)."
}
```

> TOOL

tool_result
id: toolu_012wiA3N8GUKf3q7W6jqRj9Q
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> AGENT

Edge 4: bridge from Diagnosis to Mechanism.

> TOOL

tool_use Edit
id: toolu_01MNFNdJPqftWu9oe6xXhTH8
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "\\subsubsection*{Mechanism: instance normalization strips the routing signal}\n\\label{sec:diagnosis}\n\n\\textbf{Why RevIN destroys routing.} Each window decomposes into mean $M_i$, scale $\\Sigma_i$, shape $\\mathbf{S}_i = (\\mathbf{x}_i - M_i)/\\Sigma_i$; RevIN keeps $\\mathbf{S}_i$ and discards $(M_i,\\Sigma_i)$. The chain rule quantifies the routing signal in the discarded part.",
  "new_string": "\\subsubsection*{Mechanism: instance normalization strips the routing signal}\n\\label{sec:diagnosis}\n\nHaving established the empirical pattern (RR-MoA wins, AdaMix collapses, frozen $\\succeq$ unfrozen), we now formalize \\emph{why} routing on RevIN-normalized hidden states fails.\n\n\\textbf{Why RevIN destroys routing.} Each window decomposes into mean $M_i$, scale $\\Sigma_i$, shape $\\mathbf{S}_i = (\\mathbf{x}_i - M_i)/\\Sigma_i$; RevIN keeps $\\mathbf{S}_i$ and discards $(M_i,\\Sigma_i)$. The chain rule quantifies the routing signal in the discarded part."
}
```

> TOOL

tool_result
id: toolu_01MNFNdJPqftWu9oe6xXhTH8
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> AGENT

Edge 5: re-frame the rescue-baseline opener as mechanism-first.

> TOOL

tool_use Edit
id: toolu_014T9yk4UuRBwfMKnKE4gG6J
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "\\textbf{Rescue-baseline sweep.} To rule out under-tuning, we sweep five standard MoE rescue families (Switch load-balance~\\citep{fedus2022switch}, ST-MoE z-loss~\\citep{zoph2022stmoe}, entropy regularization, ReMoE ReLU routing~\\citep{wang2025remoe}, expert-choice routing~\\citep{zhou2022expertchoice}) over $12$ configurations $\\times$ 6 datasets $\\times$ 2 freeze levels $\\times$ 5 seeds $= 720$ run-cells (Table~\\ref{tab:rescue}, Appendix~\\ref{app:rescue_details}).",
  "new_string": "\\textbf{Rescue-baseline sweep.} The mechanism predicts that interventions targeting optimization will fail because the router's input distribution is the bottleneck, not its objective. We test this directly by sweeping five standard MoE rescue families (Switch load-balance~\\citep{fedus2022switch}, ST-MoE z-loss~\\citep{zoph2022stmoe}, entropy regularization, ReMoE ReLU routing~\\citep{wang2025remoe}, expert-choice routing~\\citep{zhou2022expertchoice}) over $12$ configurations $\\times$ 6 datasets $\\times$ 2 freeze levels $\\times$ 5 seeds $= 720$ run-cells (Table~\\ref{tab:rescue}, Appendix~\\ref{app:rescue_details})."
}
```

> TOOL

tool_result
id: toolu_014T9yk4UuRBwfMKnKE4gG6J
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use TaskCreate
id: toolu_01Bg2oAW24MM7TTLH7EVLLxp
```json
{
  "subject": "Apply edges 2/3/4/5 to main.tex",
  "description": "Apply the four sentence-level edits to main.tex: positioning lead in Related Work, three-claims roadmap fix, Diagnosis→Mechanism bridge, mechanism-first rescue opener.",
  "activeForm": "Applying edges to main.tex",
  "metadata": {
    "status_init": "in_progress"
  }
}
```

> TOOL

tool_result
id: toolu_01Bg2oAW24MM7TTLH7EVLLxp
```
Task #9 created successfully: Apply edges 2/3/4/5 to main.tex
```

> TOOL

tool_use TaskCreate
id: toolu_018zogwa7rwF7J2bQeG7eXHu
```json
{
  "subject": "Recompile main.tex and verify build",
  "description": "Run pdflatex twice and confirm no errors. Per feedback_recompile_main.md the build must succeed before reporting done.",
  "activeForm": "Recompiling main.tex"
}
```

> TOOL

tool_result
id: toolu_018zogwa7rwF7J2bQeG7eXHu
```
Task #10 created successfully: Recompile main.tex and verify build
```

> TOOL

tool_use TaskUpdate
id: toolu_015AodykQb1o2RsBnuwdasbf
```json
{
  "taskId": "9",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_015AodykQb1o2RsBnuwdasbf
```
Updated task #9 status
```

> TOOL

tool_use TaskUpdate
id: toolu_018rgqfGWcVWzmKLEVLoCxjo
```json
{
  "taskId": "10",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_018rgqfGWcVWzmKLEVLoCxjo
```
Updated task #10 status
```

> TOOL

tool_use Bash
id: toolu_01PdHcnsfTExxj9afESTdLiq
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/pdflatex1.log 2>&1; echo \"EXIT=$?\"; tail -25 /tmp/pdflatex1.log",
  "description": "First pdflatex pass",
  "timeout": 180000
}
```

> TOOL

tool_result
id: toolu_01PdHcnsfTExxj9afESTdLiq
```
EXIT=0
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
Output written on main.pdf (52 pages, 909230 bytes).
Transcript written on main.log.
```

> AGENT

First pass clean (52 pages). Running second pass for cross-refs.

> TOOL

tool_use Bash
id: toolu_015Nc1qVoCLfwRo7XTTuMm7e
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/pdflatex2.log 2>&1; echo \"EXIT=$?\"; grep -E \"Output written|Error|Warning: Reference|Warning: Citation\" /tmp/pdflatex2.log | tail -25",
  "description": "Second pdflatex pass for refs",
  "timeout": 180000
}
```

> TOOL

tool_result
id: toolu_015Nc1qVoCLfwRo7XTTuMm7e
```
EXIT=0
Output written on main.pdf (52 pages, 909230 bytes).
```

> TOOL

tool_use Bash
id: toolu_011N224hvgHcE24dgkxP5iuC
```json
{
  "command": "grep -cE \"Warning: Reference|Warning: Citation\" /tmp/pdflatex2.log; grep -E \"label.*page|Overfull|Underfull\" /tmp/pdflatex2.log | head -5",
  "description": "Check warnings"
}
```

> TOOL

tool_result
id: toolu_011N224hvgHcE24dgkxP5iuC
```
0
Underfull \vbox (badness 10000) has occurred while \output is active
Underfull \vbox (badness 10000) has occurred while \output is active [2]
Underfull \vbox (badness 1939) has occurred while \output is active
Underfull \vbox (badness 1939) has occurred while \output is active [3
Underfull \hbox (badness 1142) in paragraph at lines 549--550
```

> TOOL

tool_use Bash
id: toolu_018yFKsnJHiFhbCeFytbtf1o
```json
{
  "command": "python3 evidence_vm/verify.py 2>&1 | tail -3",
  "description": "Run verify.py to confirm numerics still match",
  "timeout": 60000
}
```

> TOOL

tool_result
id: toolu_018yFKsnJHiFhbCeFytbtf1o
```
Ran 107 checks against 54 RR-MoA + 54 AdaMix JSON files.
PASS: all 107 numeric claims in main.tex Tables 3-5, tab:baselines LoRA row, tab:horizon DLinear gaps, tab:backbone cross-backbone percentages, learnable alpha, imputation wins, and MI tightness match within tolerance (MSE 0.005, entropy 0.01, pct 1.0pp).
RR-MoA wins: 27/27
```

> TOOL

tool_use TaskUpdate
id: toolu_01M1qDpY9Tugmv8WFCPcanmU
```json
{
  "taskId": "10",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01M1qDpY9Tugmv8WFCPcanmU
```
Updated task #10 status
```

> AGENT

All four edges applied; pdflatex builds clean (52 pages, 0 errors, 0 ref/citation warnings); verify.py exits 0 on all 107 checks.

**Edits applied:**
- `main.tex:230` — added "We position RR-MoA against four threads: ..." as Related Work lead.
- `main.tex:409` — roadmap reads "three claims and the mechanism that explains them" (matches the four `\subsubsection*{}` blocks).
- `main.tex:493–494` — added bridge sentence opening the Mechanism subsection ("Having established the empirical pattern... we now formalize *why*...").
- `main.tex:509` — rescue-baseline opener reframed mechanism-first ("The mechanism predicts that interventions targeting optimization will fail because the router's input distribution is the bottleneck, not its objective. We test this directly...").

Edge 1 (intro redundancy) and edge 6 (Q1/Q2 labels) and edge 7 (§3 internal flow) were left alone — flag if you want me to take a pass at any of them.

> DEVELOPER

any abrupt transitioning

> AGENT

Let me scan for remaining abrupt transitions across the body.

> TOOL

tool_use Read
id: toolu_017n7AihRP64w5UFmi6cjpjy
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 395,
  "limit": 20
}
```

> TOOL

tool_result
id: toolu_017n7AihRP64w5UFmi6cjpjy
```
395	
396	\subsection{Setup}
397	
398	\textbf{Datasets and tasks.} Six LTSF benchmarks (ETTh1/h2/m1/m2~\citep{zhou2021informer}, Weather, Electricity~\citep{wu2021autoformer}) spanning hourly to 15-minute sampling and $7$--$321$ channels, with chronological splits and channel-wise normalization~\citep{nie2023patchtst}. We evaluate forecasting at $H{=}96$ primary (multi-horizon in Appendix~\ref{app:horizon}) and $20\%$-masked imputation.
399	
400	\textbf{Backbones.} Five backbones spanning three normalization regimes: (i)~learnable-affine RevIN-inside-encoder MOMENT-small/large~\citep{goswami2024moment} (internal RevIN~\citep{kim2021revin}); (ii)~Moirai~\citep{woo2024moirai} and Moirai-MoE, which use RMSNorm internally with only non-learnable per-instance I/O scaling (no learnable-affine RevIN inside the encoder pipeline); (iii)~Chronos~\citep{ansari2024chronos} (T5-style, no instance normalization) and Timer-XL~\citep{liu2025timerxl} (LayerNorm only, no instance normalization) as no-instance-normalization negative controls (per-backbone normalization specifications in Appendix~\ref{app:setup}, \S\ref{sec:cross_backbone}). The collapse mechanism predicts that only regime~(i) is vulnerable: routing signal is destroyed by RevIN's learnable-affine normalization upstream of the encoder, whereas non-learnable I/O scaling preserves the (M,$\Sigma$) statistics in the hidden states the router reads. MOMENT-small is primary. Primary results use a strictly frozen backbone; freeze-level ablations follow.
401	
402	\textbf{Baselines.} Four tiers, kept separate to avoid confounding frozen-vs-unfrozen and adapter-vs-from-scratch comparisons: \emph{frozen-adapter} (three fixed adapters; $5$-expert independent ensemble; AdaMix~\citep{wang2022adamix}); \emph{frozen PEFT} (LoRA~\citep{hu2022lora}, $108$-run sweep, App.~\ref{app:lora_sweep}; TRACE~\citep{li2025trace}); \emph{unfrozen} (full fine-tuning, all blocks, best of $5$ heads $\times 2$ LRs; extended schedules in App.~\ref{app:extended_ft}); \emph{from-scratch calibration} (DLinear~\citep{zeng2023dlinear}).
403	
404	\textbf{Training […]

> TOOL

tool_use Read
id: toolu_014LDs5gc95UgsBkPRpgxK8z
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 486,
  "limit": 75
}
```

> TOOL

tool_result
id: toolu_014LDs5gc95UgsBkPRpgxK8z
```
486	\begin{proposition}[Gradient Co-Adaptation Drives Entropy Collapse]
487	\label{prop:frozen}
488	Consider a $2$-expert MoE with backbone $\mathbf{h}{=}A\mathbf{x}$, router $p{=}\sigma(\mathbf{w}^\top\mathbf{h})$, loss $\ell{=}p\,\ell_1{+}(1{-}p)\,\ell_2$. Under gradient descent on $(A,\mathbf{w})$: \textup{(i)} the dominant expert's loss decreases faster ($\dot{\ell}_k \propto {-}p_k\|\nabla_\mathbf{h}\ell_k\|^2$), and $\dot{p}$ amplifies whichever expert currently has lower loss, creating self-reinforcing collapse toward $p{\in}\{0,1\}$; \textup{(ii)} freezing $A$ removes the co-adaptation feedback through the backbone (full non-collapse additionally requires $(\ell_1{-}\ell_2)$ to flip sign across input regimes, i.e., expert specialization, which is satisfied by the topologically distinct RR-MoA pool). Proof in Appendix~\ref{app:proofs}.
489	\end{proposition}
490	
491	{\looseness=-1 \textit{Remark.} Proposition~\ref{prop:frozen} covers linear $A\mathbf{x}$; Figure~\ref{fig:trajectory}b confirms it in the full 8-block Transformer within ${\sim}50$ steps. Independent ensembles are $37$--$46\%$ worse (Table~\ref{tab:baselines}): learned routing, not mere diversity, drives gains.}
492	
493	\subsubsection*{Mechanism: instance normalization strips the routing signal}
494	\label{sec:diagnosis}
495	
496	Having established the empirical pattern (RR-MoA wins, AdaMix collapses, frozen $\succeq$ unfrozen), we now formalize \emph{why} routing on RevIN-normalized hidden states fails.
497	
498	\textbf{Why RevIN destroys routing.} Each window decomposes into mean $M_i$, scale $\Sigma_i$, shape $\mathbf{S}_i = (\mathbf{x}_i - M_i)/\Sigma_i$; RevIN keeps $\mathbf{S}_i$ and discards $(M_i,\Sigma_i)$. The chain rule quantifies the routing signal in the discarded part.
499	
500	\begin{observation}[Routing Information Loss […]

> AGENT

Found four more rough transitions. Applying:

**A. Headline numbers opener (line 517):** Q1/Q2 tags appear without ever being defined; replace with prose.

> TOOL

tool_use Edit
id: toolu_01VRJVEThdJEgJBtZhd7D42H
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "{\\looseness=-1 Two gains feed the headline: residual shape heterogeneity rewards diverse experts on RevIN-normalized hidden states (Q1; $26$--$79\\%$ over the best fixed adapter, Table~\\ref{tab:rrmoa}); the signal-ratio $\\rho{=}{-}0.88$ localizes \\emph{dispatch} information in the stripped statistics (Q2; explains both raw-routing benefit and Traffic's null). The Pure Raw-MLP MoE ablation (Appendix~\\ref{app:raw_mlp_moe}) separates ``MoE with raw router'' from ``ensemble with raw input''.}",
  "new_string": "{\\looseness=-1 Two complementary gains feed the headline. First, residual shape heterogeneity rewards diverse experts on RevIN-normalized hidden states ($26$--$79\\%$ over the best fixed adapter, Table~\\ref{tab:rrmoa}). Second, the signal-ratio $\\rho{=}{-}0.88$ localizes \\emph{dispatch} information in the stripped statistics, explaining both raw-routing benefit and Traffic's null. The Pure Raw-MLP MoE ablation (Appendix~\\ref{app:raw_mlp_moe}) separates ``MoE with raw router'' from ``ensemble with raw input''.}"
}
```

> TOOL

tool_result
id: toolu_01VRJVEThdJEgJBtZhd7D42H
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> AGENT

**B. Setup → Main Results (line 404 → 406):** Setup ends mid-sentence on logistics ("234.8 GPU-hours..."), then we hit the Main Results header cold. Add a one-clause connective inside the roadmap.

> TOOL

tool_use Edit
id: toolu_01ViEra1b2zcA3zBVNj68cVh
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "RR-MoA's case rests on three claims and the mechanism that explains them: fixed-topology adapters are suboptimal, the natural MoE remedy collapses on instance-normalized backbones, and standard rescue mechanisms cannot recover it. We establish each in turn before comparing against the seven-baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full fine-tuning, DLinear).",
  "new_string": "With this setup fixed, we now turn to the empirical case for RR-MoA, which rests on three claims and the mechanism that explains them: fixed-topology adapters are suboptimal, the natural MoE remedy collapses on instance-normalized backbones, and standard rescue mechanisms cannot recover it. We establish each in turn before comparing against the seven-baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full fine-tuning, DLinear)."
}
```

> TOOL

tool_result
id: toolu_01ViEra1b2zcA3zBVNj68cVh
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> AGENT

**C. Remark → Mechanism (line 491 → 493):** the Remark closes on "ensembles vs routing"; the bridge sentence I added on line 496 is good but the Remark itself is tangential to it. Tighten the Remark so it lands on the same theme the next subsection picks up.

> TOOL

tool_use Edit
id: toolu_01QhdaHstTP6xQAns5xYcHpN
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "{\\looseness=-1 \\textit{Remark.} Proposition~\\ref{prop:frozen} covers linear $A\\mathbf{x}$; Figure~\\ref{fig:trajectory}b confirms it in the full 8-block Transformer within ${\\sim}50$ steps. Independent ensembles are $37$--$46\\%$ worse (Table~\\ref{tab:baselines}): learned routing, not mere diversity, drives gains.}",
  "new_string": "{\\looseness=-1 \\textit{Remark.} Proposition~\\ref{prop:frozen} covers linear $A\\mathbf{x}$; Figure~\\ref{fig:trajectory}b confirms it in the full 8-block Transformer within ${\\sim}50$ steps. Independent ensembles are $37$--$46\\%$ worse (Table~\\ref{tab:baselines}), so learned routing -- not mere diversity -- drives the gains, which raises the question of \\emph{what} the router needs to read.}"
}
```

> TOOL

tool_result
id: toolu_01QhdaHstTP6xQAns5xYcHpN
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use TaskCreate
id: toolu_01DStP7DFPdK5jDy4XDqWnut
```json
{
  "subject": "Apply second-pass abrupt-transition fixes",
  "description": "Apply 4 more transition smoothings: Q1/Q2 prose-rewrite, Setup→MainResults connective, Remark→Mechanism setup, Headline→When-not-help connective. Recompile and verify.",
  "activeForm": "Applying second-pass smoothings"
}
```

> TOOL

tool_result
id: toolu_01DStP7DFPdK5jDy4XDqWnut
```
Task #11 created successfully: Apply second-pass abrupt-transition fixes
```

> TOOL

tool_use TaskUpdate
id: toolu_01LxZvnYFYSmBLC1A11mkXNJ
```json
{
  "taskId": "11",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01LxZvnYFYSmBLC1A11mkXNJ
```
Updated task #11 status
```

> AGENT

**D. Cross-backbone → "When RR-MoA does not help" (line 549 → 551):** the boundary-case discussion lands without a connective from the headline-positive results.

> TOOL

tool_use Edit
id: toolu_01Y2TYwfTQdkJzy7BYBspcBB
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "{\\looseness=-1 \\textbf{When RR-MoA does not help.} The diagnostic predicts a low-$R$ regime where raw routing should not win, and the results respect it: on Traffic ($R{=}0.14$, lowest in the LTSF suite) RR-MoA is statistically indistinguishable from the best fixed adapter and DLinear; Solar ($R{=}0.06$) is the one outlier where R(D) under-predicts a modest gain (App.~\\ref{app:diagnostic}).",
  "new_string": "{\\looseness=-1 \\textbf{When RR-MoA does not help.} The diagnostic should also predict where the method fails, and the results respect that boundary: on Traffic ($R{=}0.14$, lowest in the LTSF suite) RR-MoA is statistically indistinguishable from the best fixed adapter and DLinear; Solar ($R{=}0.06$) is the one outlier where $R(\\mathcal{D})$ under-predicts a modest gain (App.~\\ref{app:diagnostic})."
}
```

> TOOL

tool_result
id: toolu_01Y2TYwfTQdkJzy7BYBspcBB
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> AGENT

Now recompile and verify.

> TOOL

tool_use Bash
id: toolu_01CHZxwUp5MBxz62fSadajRH
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/pdflatex3.log 2>&1; echo \"EXIT=$?\"; grep -E \"Output written|Error\" /tmp/pdflatex3.log | tail -5",
  "description": "Recompile after second-pass fixes",
  "timeout": 180000
}
```

> TOOL

tool_result
id: toolu_01CHZxwUp5MBxz62fSadajRH
```
EXIT=0
Output written on main.pdf (52 pages, 909365 bytes).
```

> TOOL

tool_use Bash
id: toolu_015DNBDF1Q3KQZX2R1SGaXsV
```json
{
  "command": "python3 evidence_vm/verify.py 2>&1 | tail -2",
  "description": "Verify numerics",
  "timeout": 60000
}
```

> TOOL

tool_result
id: toolu_015DNBDF1Q3KQZX2R1SGaXsV
```
PASS: all 107 numeric claims in main.tex Tables 3-5, tab:baselines LoRA row, tab:horizon DLinear gaps, tab:backbone cross-backbone percentages, learnable alpha, imputation wins, and MI tightness match within tolerance (MSE 0.005, entropy 0.01, pct 1.0pp).
RR-MoA wins: 27/27
```

> TOOL

tool_use TaskUpdate
id: toolu_01KkfSpKstuy1LD8eu6mUmJX
```json
{
  "taskId": "11",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01KkfSpKstuy1LD8eu6mUmJX
```
Updated task #11 status
```

> AGENT

Four more abrupt transitions smoothed; build clean (52 pages); verify.py exits 0 on 107 checks.

**Smoothings applied (second pass):**
- **`main.tex:409`** Setup→MainResults: added "With this setup fixed, we now turn to the empirical case for RR-MoA, ..." so the roadmap doesn't crash into the Setup logistics.
- **`main.tex:491`** Diagnosis remark: ends on "...which raises the question of *what* the router needs to read", teeing up the Mechanism subsection that follows.
- **`main.tex:517`** Headline numbers: dropped the undefined "Q1/Q2" tags; rewrote as "First, ... Second, ..." prose.
- **`main.tex:551`** When-RR-MoA-doesn't-help: rephrased opener so the boundary-case paragraph reads as the natural complement to the headline-positive results, not a fresh topic.

Remaining minor candidates I left alone (flag if you want any):
- Intro paras 1–3 redundancy with abstract (would need real cuts, not a sentence add).
- §3 method internal flow (4 bold heads — felt list-y, but each is genuinely a separate concern).
- §3 first paragraph after Figure 2 still says "as shown in the introduction"; could be tightened to the local context.