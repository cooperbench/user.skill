> DEVELOPER

audit this style guideline, apply what made senses, minimal changes are recommended but I want the sharp logical writing without abrupt transioning: "# Style Reproduction Prompt

Below is a prompt designed to reproduce this paper's writing style. The original is dense, mechanism-first academic prose with a distinctive rhythm built on contrast, formal definitions, and quantitative anchoring.

---

## Prompt: Write in the "Mechanism-First Diagnostic" Academic Style

You are writing in a compact, technically dense academic style typical of top-tier ML venues (NeurIPS/ICLR). The tone is confident but never breathless, formal but never stuffy. Every paragraph earns its place. Adhere to the following:

### Voice and Register
- Use **first-person plural** throughout ("We define", "We identify", "We address this gap by..."). Never use "I"; never use "the authors".
- Use **British spellings** consistently: *localise, characterise, behaviour, generalise, analyse, modelling*.
- **No contractions.** No hedging filler ("it is worth noting that", "interestingly"). No throat-clearing.
- Confidence is calibrated through verb choice: *suggests, indicates, validates, mediates, underlies, captures*. Reserve *shows* and *proves* for results that genuinely warrant them.

### Sentence Architecture
- Favour **medium-length sentences (15–30 words)** built around a single load-bearing clause, often elaborated by a colon, semicolon, or em-dash.
  - Pattern: […]

> AGENT

I'll audit this style guide and apply the parts that fit, focusing on transitions and logical flow. Let me first audit it, then check the current state of `main.tex`.

> TOOL

tool_use Bash
id: toolu_01JYPEUAjhtErTMf46xZQTG9
```json
{
  "command": "wc -l main.tex && git log --oneline -10",
  "description": "Check main.tex size and recent commit history"
}
```

> TOOL

tool_result
id: toolu_01JYPEUAjhtErTMf46xZQTG9
```
    2866 main.tex
126c9d2 docs(body): smooth section transitions and tighten intro/method prose
1cc3119 docs(body): rebalance distribution; add Problem Setup, Notation table, failure-mode, reproducibility statement
42e23bd fix(abstract_portal): take 10.9% out of math mode so OpenReview renders the percent sign
18c793f docs(abstract): surface SR-MoA, fix backbone count to five, mark R(D) as pre-training computable
20aa945 docs(abstract): rework opening to motivate MoE upgrade and scope normalization class
efe1393 fix(srmoa_fig): polish Figure F.1 labels and tighten causal_controls column
a7c1eef docs(sec4.2): reorganize Main Results into 4 subsubsections; compress prose
2a17007 docs(abstract+checklist): trim abstract sub-clauses; replace em-dashes in checklist
0ade817 docs(math+fig): correct Obs-1 tightness paragraph, expose 12-row factor in 720 arithmetic, polish Residual-IA+ figure
1f0c179 docs(refs): prune 8 orphan bibitems, add 36 NeurIPS-tier citations with argumentative hooks (57 -> 93)
```

> TOOL

tool_use Bash
id: toolu_01W8ZK89iYsLX4fdvcDSAqpa
```json
{
  "command": "grep -n \"^\\\\\\\\section\\|^\\\\\\\\subsection\\|^\\\\\\\\subsubsection\" main.tex | head -50",
  "description": "Map main.tex section structure"
}
```

> TOOL

tool_result
id: toolu_01W8ZK89iYsLX4fdvcDSAqpa
```
61:\section{Introduction}
228:\section{Related Work}
240:\section{Raw-Routed Mixture of Adapters (RR-MoA)}
394:\section{Experiments}
396:\subsection{Setup}
406:\subsection{Main Results}
411:\subsubsection*{Diagnosis: adapters underperform, MoE collapses}
493:\subsubsection*{Mechanism: instance normalization strips the routing signal}
509:\subsubsection*{Standard rescues fail; the raw-input principle generalizes}
515:\subsubsection*{Headline numbers}
554:\section{Conclusion and Limitations}
1046:\section{Experimental Setup Details}
1123:\section{Deployment-Regime Motivation}
1134:\subsection{Inference Benchmark}
1163:\section{Multi-Horizon Evaluation}
1187:\section{Proposition Proofs}
1229:\subsection{Theoretical Depth of Observation~\ref{thm:mi_decomp}}
1337:\section{LoRA Sweep (Full Results)}
1402:\section{Routing Ablations}
1687:\subsection{Statistics Re-Injection Ablation}
1713:\section{Extended RR-MoA Freeze Grid}
1776:\subsection{Rescue-Baseline Sweep Details}
1808:\subsection{AdaMix Implementation Details}
1846:\section{Normalization Generalization}
1871:\subsection{Cross-Modality Control: Vision MoE}
1902:\section{Top-$k$ Sparse Routing Ablation}
1928:\subsection{Expert Pool Diversity Ablation}
1952:\subsection{Expert Count Scaling}
1978:\section{Imputation Results}
2006:\section{Learnable Normalization Coefficient}
2032:\section{Exact MI Loss and Bound Tightness}
2063:\section{Information Content Diagnostic}
2182:\section{Cross-Backbone RR-MoA}
2275:\section{Extended Full Fine-Tuning Ablation}
2341:\section{Closing the DLinear Gap}
2402:\subsection{Residual-IA: Closing the Remaining Gap}
2622:\subsubsection*{Residual-IA\textsuperscript{+}: closing the remaining gap to 5/6}
2698:\subsubsection*{Multi-horizon generalization: H${\in}\{96, 192, 336, 720\}$}
2725:\subsubsection*{Cross-backbone generalization: does Residual-IA\textsuperscript{+} depend on RevIN?}
2801:\subsection{SR-RIA\textsuperscript{+}: Self-Routed Residual-IA\textsuperscript{+}}
2827:\subsection{Pure Raw-MLP MoE Ablation: Quantifying the TSFM's Contribution}
```

> AGENT

Let me audit the transition zones — section openings and boundaries are where abrupt jumps live.

> TOOL

tool_use Read
id: toolu_01CsDRSMKamSxCQcM2z7TV8q
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 61,
  "limit": 170
}
```

> TOOL

tool_result
id: toolu_01CsDRSMKamSxCQcM2z7TV8q
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
id: toolu_013DT9jzpriCkxr26zqDVuMG
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 228,
  "limit": 270
}
```

> TOOL

tool_result
id: toolu_013DT9jzpriCkxr26zqDVuMG
```
228	\section{Related Work}
229	
230	We position RR-MoA against four threads: TSFM adaptation, MoE in foundation models, MoE routing collapse and rescue, and time-series normalization.
231	
232	\textbf{TSFM Adaptation.} For broader context we refer to the survey by~\citet{wen2023tssurvey}. A complementary line shows that compact task-specific models match or beat heavyweight pretrained backbones on LTSF benchmarks~\citep{wu2025srsnet, wang2025timemixerpp, xu2024fits, chen2023tsmixer, fu2025selective}: that lightweight raw-input models are competitive is itself evidence that the per-window raw signal carries most of the predictability our diagnostic $R(\mathcal{D})$ exploits (\S\ref{sec:diagnosis}). LLM-reprogrammed forecasters~\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes} inherit per-window normalization upstream of the backbone, so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is attached. We focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a lightweight module to a frozen TSFM~\citep{hu2022lora, houlsby2019adapters, goswami2024moment}; recent variations explore multi-scale finetuning~\citep{qiao2025msft}, importance-based LoRA selection~\citep{li2025trace}, input-representation adaptation~\citep{benechehab2025adapts}, structured pruning~\citep{zhao2025prune}, in-context tuning~\citep{faw2025icf}, retrieval-augmented adaptation~\citep{ning2025tsrag}, and Chronos-specific PEFT~\citep{gupta2024beyondlora}; complementary work computes transferability scores for backbone selection (TEMPLATE, \citealp{zhang2025template}) or provides a unified evaluation suite (GIFT-Eval, \citealp{woo2024gifteval}). These vary the finetuning \textit{strategy} while leaving per-input adapter \textit{topology} fixed; AdaPTS reports the best of several variants per dataset/horizon, treating adapter choice as a per-task hyperparameter rather […]

> TOOL

tool_use Read
id: toolu_018oKWtVAg6xJFRcxXtFrJvj
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 497,
  "limit": 170
}
```

> TOOL

tool_result
id: toolu_018oKWtVAg6xJFRcxXtFrJvj
```
497	
498	\textbf{Why RevIN destroys routing.} Each window decomposes into mean $M_i$, scale $\Sigma_i$, shape $\mathbf{S}_i = (\mathbf{x}_i - M_i)/\Sigma_i$; RevIN keeps $\mathbf{S}_i$ and discards $(M_i,\Sigma_i)$. The chain rule quantifies the routing signal in the discarded part.
499	
500	\begin{observation}[Routing Information Loss Under Instance Normalization]
501	\label{thm:mi_decomp}
502	Let $X$ be a random input window, $E \in \{1,\ldots,K\}$ the expert assignment produced by any deterministic router, $S = (X - M)/\Sigma$ the RevIN-normalized shape. \emph{(i) Exact decomposition:} $I(X;E) - I(S;E) = I(M,\Sigma;E\mid S) \geq 0$. \emph{(ii) Quantitative bound (no independence assumption):} $I(X;E) - I(S;E) \geq I(M,\Sigma;E) - I(M,\Sigma;S)$, with $\varepsilon := I(M,\Sigma;S) \geq 0$ capturing residual leakage of stripped statistics through the shape; equality iff $(M,\Sigma) \perp\!\!\!\perp S \mid E$.
503	\end{observation}
504	
505	When routing signal lives entirely in the stripped statistics ($(M,\Sigma)\perp\!\!\!\perp S$; Appendix~\ref{app:proofs}), $I(X;E){-}I(S;E){=}H(E)$: RevIN destroys the entire routing distribution. The signal ratio $R(\mathcal{D}) = [\mathrm{Var}(M)+\mathrm{Var}(\Sigma)]/\overline{\mathrm{Var}(S)}$ is a tractable monotone proxy, computable from raw dataset statistics before any training; the bound is empirically tight (Appendix~\ref{app:mi_tightness}) and learnable $\alpha{<}0.5$ on $30/30$ runs (Appendix~\ref{app:learnable_alpha}). $R(\mathcal{D})$ predicts raw-routing benefit at Spearman $\rho{=}{-}0.88$ ($p{<}0.002$, $n{=}9$; Figure~\ref{fig:signal_ratio}), whereas $H(E\mid S)$ does not ($\rho{=}{-}0.12$); Traffic ($R{=}0.14$) is a boundary, […]

> AGENT

Let me check the abstract and conclusion regions for any other transition issues.

> TOOL

tool_use Read
id: toolu_01WiEPhWVuVWc3gSTejVwfXW
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 1,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_01WiEPhWVuVWc3gSTejVwfXW
```
1	\documentclass{article}
2	% Use \usepackage[final]{neurips_2026} for camera-ready
3	\PassOptionsToPackage{numbers,compress,sort}{natbib}
4	\usepackage{neurips_2026}
5	\usepackage[utf8]{inputenc}
6	\usepackage[T1]{fontenc}
7	\usepackage{hyperref}
8	\usepackage{url}
9	\usepackage{booktabs}
10	\usepackage{amsfonts}
11	\usepackage{amsmath}
12	\usepackage{amssymb}
13	\usepackage{nicefrac}
14	\usepackage{microtype}
15	\usepackage{xcolor}
16	\usepackage{graphicx}
17	\usepackage{multirow}
18	\usepackage{colortbl}
19	\usepackage{algorithm}
20	\usepackage{algorithmic}
21	\usepackage{enumitem}
22	\usepackage{pgfplots}
23	\usepackage{tikz}
24	\usetikzlibrary{positioning, arrows.meta, shapes.geometric, fit, calc}
25	\pgfdeclarelayer{background}
26	\pgfsetlayers{background,main}
27	\usepackage{pifont}
28	\usepackage{amsthm}
29	\newcommand{\cmark}{\ding{51}}
30	\newcommand{\xmark}{\ding{55}}
31	\newtheorem{definition}{Definition}
32	\newtheorem{proposition}{Proposition}
33	\newtheorem{observation}{Observation}
34	\newcommand{\nonterminal}[1]{\texttt{#1}}
35	\pgfplotsset{compat=1.18}
36	
37	\title{Raw-Routed Mixture of Adapters: A Causal Intervention for Routing Collapse in Time Series Foundation Models}
38	
39	\author{
40	  Anonymous Author 1 \\
41	  Anonymous Institution\\
42	  \texttt{<REDACTED_EMAIL>}
43	  \And
44	  Anonymous Author 2 \\
45	  Anonymous Institution\\
46	  \texttt{<REDACTED_EMAIL>}
47	  \And
48	  Anonymous Author 3 \\
49	  Anonymous Institution\\
50	  \texttt{<REDACTED_EMAIL>}
51	}
52	
53	\begin{document}
54	
55	\maketitle
56	
57	\begin{abstract}
58	Many time series foundation models (TSFMs) adapt to a target dataset by attaching a single trainable head to a frozen backbone. A single head is one-size-fits-all, yet target series mix heterogeneous regimes that a single head may underfit. The natural upgrade is to replace the single head with a mixture-of-experts (MoE) head […]

> AGENT

Now I have the picture. The paper is already heavily edited and most of the style guide's principles are present. Let me give you my audit and apply the two targeted improvements I see.

## Audit: what to apply, what to skip

**Already present (no change needed):**
- First-person plural, calibrated verbs (*identifies, formalizes, predicts*), gap-identification frame, Definition/Observation/Proposition blocks, italicise-on-first-use, quantitative anchoring with ranges, three-bullet contributions, bridge clauses at section borders ("With this setup fixed", "Having established the empirical pattern", "Because the diagnosis pinpoints").
- `\bf{Run-in headers.}` tightly packaged with bolded one-line claims followed by 2–4 sentences of evidence — already the dominant pattern in §4.
- Avoidance of "delve/showcase/leverage/novel/robust" — already clean.

**Skip (conflicts with project conventions):**
- "Use em-dashes for parenthetical insertions" — your `feedback_minimise_emdash` says the opposite. Project preference wins.
- "Bolded one-line **Finding** blocks" — paper uses Observation/Proposition; restructuring would be churn.
- "British spellings" — paper uses "normalization" / "behavior" throughout; switching now is pure churn with no clarity gain.
- "Begin with 'Yet' instead of 'However'" — stylistic, not load-bearing.

**Apply (two clear, minimal wins):**
1. **Throat-clearing opener in Related Work** (l. 232): "For broader context we refer to the survey by..." is exactly […]

> TOOL

tool_use Edit
id: toolu_01KMQhZztde3tD2XLUY9zVKm
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "\\textbf{TSFM Adaptation.} For broader context we refer to the survey by~\\citet{wen2023tssurvey}. A complementary line shows that compact task-specific models match or beat heavyweight pretrained backbones on LTSF benchmarks",
  "new_string": "\\textbf{TSFM Adaptation.} Beyond the broad survey of~\\citet{wen2023tssurvey}, a complementary line shows that compact task-specific models match or beat heavyweight pretrained backbones on LTSF benchmarks"
}
```

> TOOL

tool_result
id: toolu_01KMQhZztde3tD2XLUY9zVKm
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_017ZAnGZrm8XeTe3KsfMhmeV
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "degrade MSE by $8$--$15\\%$ (Appendix~\\ref{app:diversity}). Pseudocode in Algorithm~\\ref{alg:rrmoa} (Appendix~\\ref{app:setup}). Because the backbone is strictly frozen,",
  "new_string": "degrade MSE by $8$--$15\\%$ (Appendix~\\ref{app:diversity}; pseudocode in Algorithm~\\ref{alg:rrmoa}, Appendix~\\ref{app:setup}). Because the backbone is strictly frozen,"
}
```

> TOOL

tool_result
id: toolu_017ZAnGZrm8XeTe3KsfMhmeV
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> AGENT

Now rebuild to verify the LaTeX still compiles cleanly.

> TOOL

tool_use Bash
id: toolu_01PnJH33qQSsjzdGPzrbMWJr
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/pdflatex.log 2>&1; tail -30 /tmp/pdflatex.log",
  "description": "Recompile main.tex to verify build"
}
```

> TOOL

tool_result
id: toolu_01PnJH33qQSsjzdGPzrbMWJr
```
fonts/cmextra/cmex9.pfb></home/<USER>/Library/texmf/fonts/type1/public/ams
fonts/cm/cmmi10.pfb></home/<USER>/Library/texmf/fonts/type1/public/amsfont
s/cm/cmmi12.pfb></home/<USER>/Library/texmf/fonts/type1/public/amsfonts/cm
/cmmi5.pfb></home/<USER>/Library/texmf/fonts/type1/public/amsfonts/cm/cmmi
6.pfb></home/<USER>/Library/texmf/fonts/type1/public/amsfonts/cm/cmmi7.pfb
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
Output written on main.pdf (51 pages, 908217 bytes).
Transcript written on main.log.
```

> AGENT

Build clean (51 pages). Let me also make sure `verify.py` still passes — neither edit touched a numeric claim, but worth confirming.

> TOOL

tool_use Bash
id: toolu_01Cp2fk1nJf3GXorpiHRzWLQ
```json
{
  "command": "python3 evidence_vm/verify.py 2>&1 | tail -5",
  "description": "Run verify.py to confirm 107 numeric claims still pass"
}
```

> TOOL

tool_result
id: toolu_01Cp2fk1nJf3GXorpiHRzWLQ
```
Ran 107 checks against 54 RR-MoA + 54 AdaMix JSON files.
PASS: all 107 numeric claims in main.tex Tables 3-5, tab:baselines LoRA row, tab:horizon DLinear gaps, tab:backbone cross-backbone percentages, learnable alpha, imputation wins, and MI tightness match within tolerance (MSE 0.005, entropy 0.01, pct 1.0pp).
RR-MoA wins: 27/27
```

> AGENT

Both edits applied, build passes, verify.py 107/107 green.

**Summary of changes:**
- `main.tex:232` — replaced "For broader context we refer to the survey by..." with "Beyond the broad survey of..." inlined into the next clause. Removes a throat-clearing opener; preserves the citation.
- `main.tex:390` — collapsed the standalone "Pseudocode in Algorithm~\ref{alg:rrmoa} (Appendix~\ref{app:setup})." sentence into the preceding `(Appendix~\ref{app:diversity}; pseudocode ..., Appendix~\ref{app:setup})` parenthetical. The cost / expert-pool / deployment thread now runs uninterrupted into "Because the backbone is strictly frozen,..."

Net effect: two fewer sentences, no claims touched. The rest of the style guide is either already satisfied or conflicts with project conventions (em-dash minimisation, US spellings, Observation/Proposition over Finding) and was correctly left alone.