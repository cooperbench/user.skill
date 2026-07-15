> DEVELOPER

cut related work by 20 lines

> TOOL

tool_use Bash
id: toolu_01RQGi1tQAu2HPTc6mPeB4KN
```json
{
  "command": "grep -n \"related\" /Users/hungpq2412/neuralips26/main.tex | head -20",
  "description": "Find related work section"
}
```

> TOOL

tool_result
id: toolu_01RQGi1tQAu2HPTc6mPeB4KN
```
227:\label{sec:related_work}
1258:\textbf{What our adapters deliver in practice.} The numbers above quantify the cost of accessing a regime DLinear cannot serve at all. (i) \emph{Adapter overhead is bounded.} All three of our architectures stay within $+5.9\%$ of the raw backbone latency and add at most $6$\,MB of peak GPU memory (Table~\ref{tab:benchmark}); the frozen backbone is the cost floor, and the routing/expert machinery does not blow it up. (ii) \emph{Hot-swap, not retrain.} A new tenant or task is served by loading $354$--$466$\,K adapter parameters from host RAM into the resident backbone in sub-millisecond time; the per-tenant DLinear alternative requires collecting that tenant's history and running a fresh supervised training pipeline before the first prediction. (iii) \emph{One model, many tasks.} The same frozen backbone drives forecasting, imputation, and classification through different expert pools (\S\ref{sec:intro}, Appendix~\ref{app:imputation}); $N$ tasks consume one GPU residency rather than $N$. (iv) \emph{Zero-shot onboarding.} Adapter weights trained on related tenants transfer at load time, so a new deployment can serve predictions immediately rather than waiting for the data-collection-plus-training cycle that supervised per-task models require. The latency and memory numbers above are the price of these capabilities, not a claim of dominance over DLinear in DLinear's native […]

> TOOL

tool_use Bash
id: toolu_019zdtEdmouAFKuKqTtk6Lcg
```json
{
  "command": "wc -l /Users/hungpq2412/neuralips26/main.tex",
  "description": "Get main.tex line count"
}
```

> TOOL

tool_result
id: toolu_019zdtEdmouAFKuKqTtk6Lcg
```
    2870 /Users/hungpq2412/neuralips26/main.tex
```

> TOOL

tool_use Bash
id: toolu_01TcCdDkVT4wCjpRSQ2jTENq
```json
{
  "command": "grep -n \"^\\\\\\\\section\\|^\\\\\\\\subsection\" /Users/hungpq2412/neuralips26/main.tex | head -30",
  "description": "Find sections in main.tex"
}
```

> TOOL

tool_result
id: toolu_01TcCdDkVT4wCjpRSQ2jTENq
```
61:\section{Introduction}
226:\section{Related Work}
231:\section{Raw-Routed Mixture of Adapters (RR-MoA)}
401:\section{Experiments}
403:\subsection{Setup}
413:\subsection{Main Results}
650:\section{Conclusion and Limitations}
1141:\section{Experimental Setup Details}
1218:\section{Deployment-Regime Motivation}
1229:\subsection{Inference Benchmark}
1260:\section{Multi-Horizon Evaluation}
1284:\section{Proposition Proofs}
1326:\subsection{Theoretical Depth of Observation~\ref{thm:mi_decomp}}
1434:\section{LoRA Sweep (Full Results)}
1499:\section{Routing Ablations}
1764:\subsection{Statistics Re-Injection Ablation}
1790:\section{Extended RR-MoA Freeze Grid}
1853:\subsection{Rescue-Baseline Sweep Details}
1885:\subsection{AdaMix Implementation Details}
1923:\section{Normalization Generalization}
1948:\subsection{Cross-Modality Control: Vision MoE}
1979:\section{Top-$k$ Sparse Routing Ablation}
2005:\subsection{Expert Pool Diversity Ablation}
2029:\subsection{Expert Count Scaling}
2055:\section{Imputation Results}
2083:\section{Learnable Normalization Coefficient}
2109:\section{Exact MI Loss and Bound Tightness}
2140:\section{Information Content Diagnostic}
2184:\section{Cross-Backbone RR-MoA}
2277:\section{Extended Full Fine-Tuning Ablation}
```

> TOOL

tool_use Read
id: toolu_01C5xfaej7oYucAmbcydnVHH
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 226,
  "limit": 10
}
```

> TOOL

tool_result
id: toolu_01C5xfaej7oYucAmbcydnVHH
```
226	\section{Related Work}
227	\label{sec:related_work}
228	
229	RR-MoA sits at the intersection of TSFM adaptation~\citep{wen2023tssurvey} and MoE design~\citep{cai2024moesurvey}; the rescue, collapse, and statistic-recovery threads are positioned inline in \S\ref{sec:method} and \S\ref{sec:main_results}, where they inform the diagnosis. \emph{TSFM adaptation:} compact specialists rival heavyweight backbones on LTSF~\citep{wu2025srsnet, wang2025timemixerpp, xu2024fits, chen2023tsmixer, fu2025selective}; LLM-reprogrammed forecasters inherit upstream normalization~\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes}; the adapter literature varies finetuning strategy or backbone selection~\citep{houlsby2019adapters, qiao2025msft, zhao2025prune, faw2025icf, ning2025tsrag, gupta2024beyondlora, zhang2025template, woo2024gifteval}, and AdaPTS~\citep{benechehab2025adapts} treats adapter topology as a per-task hyperparameter; to our knowledge no prior TSFM work uses a per-window mixture over topologically distinct adapters. \emph{MoE design space:} scaling axes~\citep{lepikhin2021gshard, riquelme2021vmoe, komatsuzaki2023sparseupcycling, raposo2024mod, jiang2024mixtral, zhu2024llamamoe, dai2024deepseekmoe} and in-backbone TS-MoE~\citep{shi2024timemoe, he2025sempo} act on token routing within the encoder; SR-MoA's per-expert sigmoid generalizes MMoE's multi-gate pattern~\citep{ma2018mmoe} from multi-task to single-task specialization, and \citet{wang2026myth} argues MoE specialization reflects hidden-state geometry, which we extend upstream by characterizing what shapes that geometry on TSFMs. The instance-normalization origin~\citep{ulyanov2016instancenorm} treats stripping as benign preprocessing; we identify a downstream MoE-adapter consequence not previously characterized.
230	
231	\section{Raw-Routed Mixture of Adapters (RR-MoA)}
232	\label{sec:method}
233	
234	We first state the task setup, then the problem we identify and its formal mechanism, then specify RR-MoA: […]

> TOOL

tool_use Bash
id: toolu_01HA954nVzSY8vY5CxwacXHo
```json
{
  "command": "ls /Users/hungpq2412/neuralips26/main.pdf 2>/dev/null && stat -f \"%Sm\" /Users/hungpq2412/neuralips26/main.pdf 2>/dev/null",
  "description": "Check if main.pdf exists"
}
```

> TOOL

tool_result
id: toolu_01HA954nVzSY8vY5CxwacXHo
```
/Users/hungpq2412/neuralips26/main.pdf
May  6 16:02:52 2026
```

> TOOL

tool_use Bash
id: toolu_01B6iopMpsUwJRk6fPbdEWpJ
```json
{
  "command": "wc -w <<< \"$(sed -n '229p' /Users/hungpq2412/neuralips26/main.tex)\"",
  "description": "Count words in related work paragraph"
}
```

> TOOL

tool_result
id: toolu_01B6iopMpsUwJRk6fPbdEWpJ
```
     160
```

> TOOL

tool_use Bash
id: toolu_01Wm56in7F5ZbxgEKZYcMZBM
```json
{
  "command": "pdftotext -layout main.pdf - 2>/dev/null | grep -n \"Related Work\\|^3 \" | head -10",
  "description": "Find related work in PDF"
}
```

> TOOL

tool_result
id: toolu_01Wm56in7F5ZbxgEKZYcMZBM
```
118:69   2   Related Work
```

> TOOL

tool_use Bash
id: toolu_01KEipdcugoS6ykfUW82Qo4q
```json
{
  "command": "pdftotext -layout /Users/hungpq2412/neuralips26/main.pdf - 2>/dev/null | sed -n '118,160p'",
  "description": "View related work in rendered PDF"
}
```

> TOOL

tool_result
id: toolu_01KEipdcugoS6ykfUW82Qo4q
```
69   2   Related Work
70   RR-MoA sits at the intersection of TSFM adaptation [40] and MoE design [85]; the rescue, collapse,
71   and statistic-recovery threads are positioned inline in §3 and §4.2, where they inform the diagnosis.
72   TSFM adaptation: compact specialists rival heavyweight backbones on LTSF [62, 63, 69, 76, 77];
73   LLM-reprogrammed forecasters inherit upstream normalization [70–72]; the adapter literature varies
74   finetuning strategy or backbone selection [16, 24, 26, 28–31, 59], and AdaPTS [27] treats adapter
75   topology as a per-task hyperparameter; to our knowledge no prior TSFM work uses a per-window
76   mixture over topologically distinct adapters. MoE design space: scaling axes [79–84, 86] and in-
77   backbone TS-MoE [11, 58] act on token routing within the encoder; SR-MoA’s per-expert sigmoid


                                                                                                    2
 78   generalizes MMoE’s multi-gate pattern [87] from multi-task to single-task specialization, and Wang
 79   et al. [49] argues MoE specialization reflects hidden-state geometry, which we extend upstream
 80   by characterizing what shapes that geometry on TSFMs. The instance-normalization origin [92]
 81   treats stripping as benign preprocessing; we identify a downstream MoE-adapter consequence not
 82   previously characterized.


 83   3   Raw-Routed Mixture of Adapters (RR-MoA)

 84   We first state the task setup, […]

> TOOL

tool_use Bash
id: toolu_01SuUYPWUDkwJUGrnj62sGdK
```json
{
  "command": "git log --oneline --all -- main.tex | head -20",
  "description": "Check git log for main.tex"
}
```

> TOOL

tool_result
id: toolu_01SuUYPWUDkwJUGrnj62sGdK
```
4215d50 I find it abrupt starting: "This natural mixture-of-experts approach fai
e15f8fa docs(body): compress intro and related work, promote signal_ratio + causal_controls to main
091dec2 docs(body): retitle subsubsections to assertive claims; tighten main-results and conclusion prose
8796d95 docs(body): rebalance intro/conclusion and rename contributions as Problem/Mechanism/Method
657bc20 chore(submission): prepare anonymous double-blind code archive for NeurIPS 2026
666f6c8 docs(body): bridge abrupt section transitions and reorder AdaMix paragraph
126c9d2 docs(body): smooth section transitions and tighten intro/method prose
1cc3119 docs(body): rebalance distribution; add Problem Setup, Notation table, failure-mode, reproducibility statement
18c793f docs(abstract): surface SR-MoA, fix backbone count to five, mark R(D) as pre-training computable
20aa945 docs(abstract): rework opening to motivate MoE upgrade and scope normalization class
efe1393 fix(srmoa_fig): polish Figure F.1 labels and tighten causal_controls column
a7c1eef docs(sec4.2): reorganize Main Results into 4 subsubsections; compress prose
2a17007 docs(abstract+checklist): trim abstract sub-clauses; replace em-dashes in checklist
0ade817 docs(math+fig): correct Obs-1 tightness paragraph, expose 12-row factor in 720 arithmetic, polish Residual-IA+ figure
1f0c179 docs(refs): prune 8 orphan bibitems, add 36 NeurIPS-tier citations with argumentative hooks (57 -> 93)
e321d84 docs(polish): expand thin Setup, add appendix-section intros, drop defensive parentheticals
8b05274 fix(layout): relax float specifiers to [!htbp] to remove whitespace gaps
cc315a0 fix(submit): […]

> TOOL

tool_use Bash
id: toolu_01EJQq6P3MC141fEGQBpyYha
```json
{
  "command": "git show e15f8fa --stat -- main.tex 2>&1 | head -30",
  "description": "Look at recent compression commit"
}
```

> TOOL

tool_result
id: toolu_01EJQq6P3MC141fEGQBpyYha
```
commit e15f8fa15322349c4c993e689e51258e8e169b94
Author: Hung Phan (Henry) <79650826+henryph24@users.noreply.github.com>
Date:   Wed May 6 15:54:07 2026 +0700

    docs(body): compress intro and related work, promote signal_ratio + causal_controls to main
    
    - Intro: 55 → 39 PDF lines. Collapse ecosystem cite block into one \citep, drop duplicated cites (nie2023patchtst, das2024timesfm, fedus2022switch, goswami2024moment in L66/L68 — all wired in §3/§4), fold former L70 "failure is specific to" paragraph into the collapse paragraph, and tighten the RR-MoA + Frozen Paradox preview.
    - Related Work: 60 → 13 PDF lines. Replace four thread paragraphs with one packed paragraph carrying all 27 orphan citations plus the AdaPTS contrast and the per-window-topology novelty claim. ~28 duplicated cites removed (each already wired in §3 line 252 or §4 lines 419/459/522/524/561).
    - Drop the now-misleading "(positioned in detail in §\ref{sec:related_work})" cross-reference at the §3 problem-statement paragraph.
    - Reinvest the freed page: promote fig:signal_ratio (Frozen Paradox + R(D) ρ=−0.88 dual-panel) into §4.2.2 and tab:causal_controls (eight controls) into §4.2.3, both previously appendix-only. App. F intro updated to point at the now-main-body table; the figure's appendix host (App. M) loses only the figure, prose intact.
    - Build clean, all 27 orphan citations resolve, main body ends on page 9 (the prior […]

> AGENT

Now I have a clear picture. Let me load the tools I need.

> TOOL

tool_use ToolSearch
id: toolu_01GptS4szwHiyfmVPNUcra1W
```json
{
  "query": "select:AskUserQuestion,ExitPlanMode",
  "max_results": 2
}
```

> TOOL

tool_result
id: toolu_01GptS4szwHiyfmVPNUcra1W
```
{
  "type": "tool_reference",
  "tool_name": "AskUserQuestion"
}
{
  "type": "tool_reference",
  "tool_name": "ExitPlanMode"
}
```

> TOOL

tool_use Bash
id: toolu_01Ns3sNUR8C2vijhFBVmdJSU
```json
{
  "command": "grep -n \"elated\\|positioning\" /Users/hungpq2412/neuralips26/main.tex | head -15",
  "description": "Search for related-work-like content"
}
```

> TOOL

tool_result
id: toolu_01Ns3sNUR8C2vijhFBVmdJSU
```
24:\usetikzlibrary{positioning, arrows.meta, shapes.geometric, fit, calc}
226:\section{Related Work}
227:\label{sec:related_work}
1258:\textbf{What our adapters deliver in practice.} The numbers above quantify the cost of accessing a regime DLinear cannot serve at all. (i) \emph{Adapter overhead is bounded.} All three of our architectures stay within $+5.9\%$ of the raw backbone latency and add at most $6$\,MB of peak GPU memory (Table~\ref{tab:benchmark}); the frozen backbone is the cost floor, and the routing/expert machinery does not blow it up. (ii) \emph{Hot-swap, not retrain.} A new tenant or task is served by loading $354$--$466$\,K adapter parameters from host RAM into the resident backbone in sub-millisecond time; the per-tenant DLinear alternative requires collecting that tenant's history and running a fresh supervised training pipeline before the first prediction. (iii) \emph{One model, many tasks.} The same frozen backbone drives forecasting, imputation, and classification through different expert pools (\S\ref{sec:intro}, Appendix~\ref{app:imputation}); $N$ tasks consume one GPU residency rather than $N$. (iv) \emph{Zero-shot onboarding.} Adapter weights trained on related tenants transfer at load time, so a new deployment can serve predictions immediately rather than waiting for the data-collection-plus-training cycle that supervised per-task models require. The latency and memory numbers above are the price of these capabilities, not a claim […]

> TOOL

tool_use Bash
id: toolu_01KNFreHPGfycNFKaFhaHFzC
```json
{
  "command": "git diff main.tex | head -80",
  "description": "Check unstaged main.tex changes"
}
```

> TOOL

tool_result
id: toolu_01KNFreHPGfycNFKaFhaHFzC
```
diff --git a/main.tex b/main.tex
index 43d6807..1327e9c 100644
--- a/main.tex
+++ b/main.tex
@@ -65,7 +65,7 @@ Time series foundation models (TSFMs)~\citep{goswami2024moment, das2024timesfm,
 
 Standard TSFM adapters apply one head to every window (Figure~\ref{fig:problem_overview}a), yet real series mix regimes whose \emph{shape} variation lives across hidden layers~\citep{wilinski2025tsfm_representations, pandey2025tsfm_semantics}, motivating a per-window mixture of topologically distinct experts. Frozen-backbone deployment serves many tenants through hot-swapped per-task adapters, unlike per-dataset models like DLinear~\citep{zeng2023dlinear} (App.~\ref{app:deployment}).
 
-This natural MoE approach fails on instance-normalized TSFMs once backbone layers are unfrozen (Figure~\ref{fig:problem_overview}b): an AdaMix-style pool~\citep{wang2022adamix} with a softmax router on MOMENT$+$RevIN drops routing entropy to zero in most configurations (Table~\ref{tab:adamix}). We call this \emph{normalization-induced routing collapse}: RevIN~\citep{kim2021revin} strips the per-window mean and variance the router needs (Observation~\ref{thm:mi_decomp}), and the dominant expert's gradients reshape the backbone to serve it more in tens of steps (Figure~\ref{fig:trajectory}). A 720-run rescue sweep recovers only $10.9\%$ MSE, $2.7\times$ worse than RR-MoA (Table~\ref{tab:rescue}); Moirai's non-learnable I/O scaling does not collapse (\S\ref{sec:cross_backbone}), narrowing the cause to learnable-affine encoder normalization.
+The natural mixture-of-experts upgrade fails on instance-normalized TSFMs once backbone layers are unfrozen (Figure~\ref{fig:problem_overview}b): an AdaMix-style pool~\citep{wang2022adamix} with a softmax router on MOMENT$+$RevIN drops routing entropy to zero in most configurations (Table~\ref{tab:adamix}). We call this […]

> TOOL

tool_use Bash
id: toolu_017NCTuqziBZ9VYRwTpgmLYP
```json
{
  "command": "pdftotext -layout /Users/hungpq2412/neuralips26/main.pdf - 2>/dev/null | sed -n '115,125p'",
  "description": "Check related work region precisely"
}
```

> TOOL

tool_result
id: toolu_017NCTuqziBZ9VYRwTpgmLYP
```
68      or beats DLinear on 6/6 datasets, 107/123 cells across six backbones).


69   2   Related Work
70   RR-MoA sits at the intersection of TSFM adaptation [40] and MoE design [85]; the rescue, collapse,
71   and statistic-recovery threads are positioned inline in §3 and §4.2, where they inform the diagnosis.
72   TSFM adaptation: compact specialists rival heavyweight backbones on LTSF [62, 63, 69, 76, 77];
73   LLM-reprogrammed forecasters inherit upstream normalization [70–72]; the adapter literature varies
74   finetuning strategy or backbone selection [16, 24, 26, 28–31, 59], and AdaPTS [27] treats adapter
75   topology as a per-task hyperparameter; to our knowledge no prior TSFM work uses a per-window
76   mixture over topologically distinct adapters. MoE design space: scaling axes [79–84, 86] and in-
```

> AGENT

The Related Work section is already heavily compressed: it's just one paragraph, rendering to ~13 PDF lines (lines 70-82) plus the heading. Cutting "20 lines" exceeds the section's current size, so I need to confirm the target before planning.

> TOOL

tool_use AskUserQuestion
id: toolu_013cmLmSEXZFU4afVGT6rHuS
```json
{
  "questions": [
    {
      "question": "Related Work currently renders to ~14 PDF lines total (heading + 13-line packed paragraph after the e15f8fa compression from 60 lines). \"Cut by 20\" exceeds what's there. Which target do you want?",
      "header": "Cut target",
      "multiSelect": false,
      "options": [
        {
          "label": "Delete section entirely",
          "description": "Remove \\section{Related Work} + paragraph. Redirect the AdaPTS contrast and per-window-topology novelty claim into §1 (intro) or §3.1 (problem statement) as one inline sentence. Saves ~14 PDF lines (heading + body + section break). Closest to the 20-line target. NeurIPS allows this since citations are already woven inline throughout §1/§3/§4."
        },
        {
          "label": "Reduce to 1 sentence",
          "description": "Keep the heading, collapse the 160-word paragraph to one sentence (e.g. the AdaPTS contrast + novelty claim only). Saves ~10 PDF lines. Less aggressive than deletion."
        },
        {
          "label": "Cut from elsewhere too",
          "description": "Cut Related Work to ~3 lines and trim ~7 more lines from the closest related-work-flavored prose in §1 (the ecosystem framing) or §3.1 (the AdaMix positioning paragraph) to reach ~20 PDF lines total."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result ERROR
id: toolu_013cmLmSEXZFU4afVGT6rHuS
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). STOP what you are doing and wait for the user to tell you how to proceed.

Note: The user's next message may contain a correction or preference. Pay close attention — if they explain what went wrong or how they'd prefer you to work, consider saving that to memory for future sessions.
```

> DEVELOPER

it currently from 86 to 148, recompile and check

> TOOL

tool_use Read
id: toolu_01GYKj8BCjLRsH1C9gGoKhwZ
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 80,
  "limit": 75
}
```

> TOOL

tool_result
id: toolu_01GYKj8BCjLRsH1C9gGoKhwZ
```
80	\centering
81	\resizebox{0.55\columnwidth}{!}{%
82	\begin{tikzpicture}[
83	    >=Stealth,
84	    every node/.style={font=\scriptsize},
85	    box/.style={rectangle, draw=black!70, rounded corners=1.5pt, fill=white,
86	        minimum height=0.7cm, align=center, line width=0.6pt},
87	    bbbox/.style={box, draw=black!85, fill=blue!3, minimum width=2.4cm, minimum height=1.0cm,
88	        font=\scriptsize\bfseries},
89	    smallbox/.style={box, minimum width=0.65cm, minimum height=0.45cm, font=\tiny},
90	    waveframe/.style={rectangle, draw=black!40, fill=gray!3, line width=0.4pt,
91	        minimum width=1.45cm, minimum height=0.55cm, inner sep=1pt},
92	    headbox/.style={box, draw=black!85, fill=orange!8, minimum width=1.7cm, minimum height=0.85cm,
93	        font=\scriptsize\bfseries},
94	    routerbox/.style={box, draw=black!85, fill=orange!8, minimum width=0.95cm, minimum height=0.7cm,
95	        font=\scriptsize\bfseries},
96	    expertactive/.style={box, draw=orange!80, fill=orange!12, minimum width=1.0cm,
97	        minimum height=0.36cm, font=\tiny\bfseries, line width=0.9pt},
98	    expertinactive/.style={box, draw=black!30, fill=gray!4, minimum width=1.0cm,
99	        minimum height=0.36cm, font=\tiny, text=black!50},
100	    arr/.style={->, line width=0.55pt, color=black!75},
101	    activearr/.style={->, line width=0.85pt, color=orange!85},
102	    deadarr/.style={->, line width=0.4pt, color=black!25, densely dashed},
103	    banner/.style={font=\footnotesize\bfseries, align=center},
104	    sublabel/.style={font=\tiny, color=black!60, align=center},
105	]
106	
107	% ============== PANEL A (TOP) ==============
108	\node[banner] (titleA) at (7.3, 3.65)
109	    {TSFM adapters use the same head for every window};
110	
111	% Three input waveforms (left)
112	\node[waveframe] (w1a) at (0.9, 3.30) {};
113	\draw[blue!75, line width=0.5pt] plot[domain=-0.65:0.65, samples=30, smooth]
114	    ({\x+0.9},{3.30+0.16*sin(deg(2.4*\x))});
115	\node[waveframe] (w2a) at (0.9, 2.78) {};
116	\draw[red!75, line width=0.4pt] plot[domain=-0.65:0.65, samples=70]
117	    ({\x+0.9},{2.78+0.09*sin(deg(35*\x))+0.05*sin(deg(11*\x))});
118	\node[waveframe] (w3a) at (0.9, 2.26) {};
119	\draw[green!55!black, line width=0.5pt]
120 […]

> AGENT

You're right — the PDF I'm looking at is stale (it was built before the unstaged intro tweak). Let me recompile and check the current rendered position.

> TOOL

tool_use Bash
id: toolu_016GbB3GqS4uLRajFmSaX6JF
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/pdflatex1.log 2>&1; tail -5 /tmp/pdflatex1.log",
  "description": "Recompile main.tex (pass 1)"
}
```

> TOOL

tool_result
id: toolu_016GbB3GqS4uLRajFmSaX6JF
```
texlive/2026basic/texmf-dist/fonts/type1/urw/times/utmbi8a.pfb></usr/local/texl
ive/2026basic/texmf-dist/fonts/type1/urw/times/utmr8a.pfb></usr/local/texlive/2
026basic/texmf-dist/fonts/type1/urw/times/utmri8a.pfb>
Output written on main.pdf (50 pages, 902921 bytes).
Transcript written on main.log.
```

> TOOL

tool_use Bash
id: toolu_01VgT9FeaME7omGUU74cts5A
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/pdflatex2.log 2>&1; tail -3 /tmp/pdflatex2.log",
  "description": "Recompile main.tex (pass 2)"
}
```

> TOOL

tool_result
id: toolu_01VgT9FeaME7omGUU74cts5A
```
026basic/texmf-dist/fonts/type1/urw/times/utmri8a.pfb>
Output written on main.pdf (50 pages, 902921 bytes).
Transcript written on main.log.
```

> TOOL

tool_use Bash
id: toolu_01BN7sCzWHegroFm4ZjEEpsC
```json
{
  "command": "pdftotext -layout /Users/hungpq2412/neuralips26/main.pdf - 2>/dev/null | sed -n '80,160p'",
  "description": "View lines 80-160 of rendered PDF"
}
```

> TOOL

tool_result
id: toolu_01BN7sCzWHegroFm4ZjEEpsC
```
     natural mixture-of-experts extension fails on instance-normalized TSFMs under unfreezing: entropy
     collapses (0.000±0.000) and the remaining experts receive no gradient. Same backbone, different
     heads.
36   The natural mixture-of-experts upgrade fails on instance-normalized TSFMs once backbone layers are
37   unfrozen (Figure 1b): an AdaMix-style pool [18] with a softmax router on MOMENT+RevIN drops
38   routing entropy to zero in most configurations (Table 2). We call this normalization-induced routing
39   collapse: RevIN [21] strips the per-window mean and variance the router needs (Observation 1), and
40   the dominant expert’s gradients reshape the backbone to serve it more in tens of steps (Figure G.1). A
41   720-run rescue sweep recovers only 10.9% MSE, 2.7× worse than RR-MoA (Table G.3); Moirai’s
42   non-learnable I/O scaling does not collapse (§4.2), narrowing the cause to learnable-affine encoder
43   normalization.
44   Raw-Routed Mixture of Adapters (RR-MoA) routes on the raw, pre-normalization input Xraw with the
45   backbone strictly frozen; the same diagnosis predicts a Frozen Paradox (Proposition 1), confirmed
46   empirically (frozen best on 4/6, unfrozen-wins bounded at ≤ 13%).
47   The diagnosis (collapse → mechanism → minimal fix) and the controls that distinguish it from prior
48   MoE-collapse threads structure our three contributions: […]

> TOOL

tool_use Bash
id: toolu_01HPYD873NYgUTmyVLLzn6Ub
```json
{
  "command": "pdftotext -layout /Users/hungpq2412/neuralips26/main.pdf - 2>/dev/null | sed -n '83,160p'",
  "description": "Check PDF lines 83-160"
}
```

> TOOL

tool_result
id: toolu_01HPYD873NYgUTmyVLLzn6Ub
```
36   The natural mixture-of-experts upgrade fails on instance-normalized TSFMs once backbone layers are
37   unfrozen (Figure 1b): an AdaMix-style pool [18] with a softmax router on MOMENT+RevIN drops
38   routing entropy to zero in most configurations (Table 2). We call this normalization-induced routing
39   collapse: RevIN [21] strips the per-window mean and variance the router needs (Observation 1), and
40   the dominant expert’s gradients reshape the backbone to serve it more in tens of steps (Figure G.1). A
41   720-run rescue sweep recovers only 10.9% MSE, 2.7× worse than RR-MoA (Table G.3); Moirai’s
42   non-learnable I/O scaling does not collapse (§4.2), narrowing the cause to learnable-affine encoder
43   normalization.
44   Raw-Routed Mixture of Adapters (RR-MoA) routes on the raw, pre-normalization input Xraw with the
45   backbone strictly frozen; the same diagnosis predicts a Frozen Paradox (Proposition 1), confirmed
46   empirically (frozen best on 4/6, unfrozen-wins bounded at ≤ 13%).
47   The diagnosis (collapse → mechanism → minimal fix) and the controls that distinguish it from prior
48   MoE-collapse threads structure our three contributions:
49    • Problem formulation. We frame routing collapse on instance-normalized TSFMs as a router-input
50      failure rather than the router-optimization failure that prior […]

> TOOL

tool_use Bash
id: toolu_015iL4ncmatDa3CzzgbeNd27
```json
{
  "command": "ls -la /Users/hungpq2412/neuralips26/submission.zip.bak 2>&1 | head -3; ls /Users/hungpq2412/neuralips26/*.tex /Users/hungpq2412/neuralips26/*.pdf 2>&1",
  "description": "List tex/pdf files in directory"
}
```

> TOOL

tool_result
id: toolu_015iL4ncmatDa3CzzgbeNd27
```
-rw-r--r--  1 hungpq2412  staff  22234849 May  6 14:33 /Users/hungpq2412/neuralips26/submission.zip.bak
/Users/hungpq2412/neuralips26/checklist.tex
/Users/hungpq2412/neuralips26/main.pdf
/Users/hungpq2412/neuralips26/main.tex
```

> TOOL

tool_use Bash
id: toolu_01CN453iZzXHq2MP8rcfqxRL
```json
{
  "command": "pdftotext /Users/hungpq2412/neuralips26/main.pdf - 2>/dev/null | grep -n \"Related Work\\|^[0-9] \" | head -10",
  "description": "Find related work without layout"
}
```

> TOOL

tool_result
id: toolu_01CN453iZzXHq2MP8rcfqxRL
```
228:Related Work
552:3 for ablations. Significance via Wilcoxon signed-rank, Bonferroni-corrected over 6 datasets × 5
2236:0 .420
2237:0 .476
2238:0 .502
2239:0 .553
2251:0 .326
2252:0 .365
2253:0 .415
2254:0 .454
```

> TOOL

tool_use Bash
id: toolu_01Thy8FDkrcavN26s4B2TEQQ
```json
{
  "command": "pdftotext /Users/hungpq2412/neuralips26/main.pdf - 2>/dev/null | sed -n '80,150p'",
  "description": "View lines 80-150 without layout"
}
```

> TOOL

tool_result
id: toolu_01Thy8FDkrcavN26s4B2TEQQ
```
whose shape variation lives across hidden layers [56, 57], motivating a per-window mixture of
topologically distinct experts. Frozen-backbone deployment serves many tenants through hotswapped per-task adapters, unlike per-dataset models like DLinear [17] (App. B).
Submitted to 40th Conference on Neural Information Processing Systems (NeurIPS 2026). Do not distribute.

(a)

TSFM adapters use the same head for every window
FROZEN

H1
H2
H3

Frozen TSFM Backbone
(MOMENT, Moirai)

Single static
adapter head

ŷ

Instance Normalization (RevIN)
Input windows X (distinct per-window stats)

(b)

A natural MoE adapter collapses to a single expert on instance-normalized TSFMs
E1

FROZEN

Frozen TSFM Backbone
(MOMENT, Moirai)
Instance Normalization (RevIN)
Input windows X

H1
H2
H3

Router

E2

unused

E3

unused

E4

unused

E5

unused

ŷ

Figure 1: Problem overview. (a) TSFM adapters use the same head for every window. (b) The
natural mixture-of-experts extension fails on instance-normalized TSFMs under unfreezing: entropy
collapses (0.000±0.000) and the remaining experts receive no gradient. Same backbone, different
heads.
36
37
38
39
40
41
42
```

> TOOL

tool_use Bash
id: toolu_01Xw9VxrrETxyVtf8JJwwWER
```json
{
  "command": "grep -n \"lineno\\|nonatbib\\|usepackage{neurips\" /Users/hungpq2412/neuralips26/main.tex | head -5",
  "description": "Check for line numbering package"
}
```

> TOOL

tool_result
id: toolu_01Xw9VxrrETxyVtf8JJwwWER
```
4:\usepackage{neurips_2026}
```

> TOOL

tool_use Bash
id: toolu_01VMqkF1fGVdj5LxCWgYfsBy
```json
{
  "command": "head -20 /Users/hungpq2412/neuralips26/main.tex",
  "description": "Check preamble"
}
```

> TOOL

tool_result
id: toolu_01VMqkF1fGVdj5LxCWgYfsBy
```
\documentclass{article}
% Use \usepackage[final]{neurips_2026} for camera-ready
\PassOptionsToPackage{numbers,compress,sort}{natbib}
\usepackage{neurips_2026}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{amsfonts}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{nicefrac}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{multirow}
\usepackage{colortbl}
\usepackage{algorithm}
\usepackage{algorithmic}
```

> TOOL

tool_use Bash
id: toolu_015xoAFRUCEorNAEeLEfs1bC
```json
{
  "command": "pdftotext -layout /Users/hungpq2412/neuralips26/main.pdf - 2>/dev/null | awk '/^\\s*86\\s/,/^\\s*149\\s/' | head -80",
  "description": "Extract margin lines 86-149 from PDF"
}
```

> TOOL

tool_result
id: toolu_015xoAFRUCEorNAEeLEfs1bC
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01SrTWXAyuWXyCCVWRt67fMJ
```json
{
  "command": "pdftotext -layout /Users/hungpq2412/neuralips26/main.pdf - 2>/dev/null | grep -nE \"^\\s*(86|87|88|140|145|148|149)\\s\" | head -20",
  "description": "Find PDF lines containing margin numbers 86-149"
}
```

> TOOL

tool_result
id: toolu_01SrTWXAyuWXyCCVWRt67fMJ
```
141: 86   experts consume the frozen TSFM’s hidden states. Cost, expert pool, and deployment implications
142: 87   close the section.
143: 88   Task setup. Given a window x ∈ RT ×c (T =512, c channels), forecasting predicts y ∈ Rh×c at
253:140   the dense MSE improvement over the best fixed adapter (§4.2). Routing on raw input preserves the
258:145   K=5 topologically distinct adapters (mean-pool, last-token, max-pool, attention-pool, Conv1d-
261:148   initialization) degrade MSE by 8–15% (Appendix I.1; pseudocode in Algorithm 1, Appendix A).
262:149   Because the backbone is strictly frozen, a single TSFM held in GPU memory can be shared across
```

> AGENT

After recompiling, I'm seeing different rendered locations than what you described. Let me show you what I find so we can align:

**Related Work (§2)** in the recompiled PDF: margin lines **70–82** (13 lines of body text).

**Lines 86–148** are §3 (RR-MoA method): from "experts consume the frozen TSFM's hidden states..." through to the end of the Top-k pool list before "Because the backbone is strictly frozen...".

A few possibilities:
1. Your viewer is showing a stale PDF (the one before the e15f8fa compression that took Related Work from 60 → 13 lines).
2. You meant §3 (RR-MoA method/setup) when you said "related work" — that block does run lines 84–148.
3. You're looking at a different PDF entirely.

Could you confirm which you want me to cut 20 lines from?

- **A.** Related Work proper (PDF lines 70–82, currently 13 lines — can't cut 20, would need to delete the section)
- **B.** §3 RR-MoA setup/problem-statement block (PDF lines 84–148, ~64 lines — 20-line cut is feasible)
- **C.** Something else entirely

> DEVELOPER

let recompile, I'll check manually

> TOOL

tool_use Bash
id: toolu_0195XUM7qQu6roK4eoMdr3S4
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/pdflatex3.log 2>&1; tail -3 /tmp/pdflatex3.log; echo \"---\"; stat -f \"%Sm  %z bytes\" /Users/hungpq2412/neuralips26/main.pdf",
  "description": "Final pdflatex pass and verify PDF"
}
```

> TOOL

tool_result
id: toolu_0195XUM7qQu6roK4eoMdr3S4
```
026basic/texmf-dist/fonts/type1/urw/times/utmri8a.pfb>
Output written on main.pdf (50 pages, 902921 bytes).
Transcript written on main.log.
---
May  6 16:15:49 2026  902921 bytes
```

> AGENT

Recompiled. `main.pdf` is fresh (May 6 16:15:49, 50 pages, 902921 bytes). Open it and let me know which line range you want trimmed.

> DEVELOPER

we overdo it, it should be about 40 lines, check what commits did we accidentally removed too much

> TOOL

tool_use Bash
id: toolu_01L7tMhbHKzAWAZCotPedXE7
```json
{
  "command": "git log --oneline -- main.tex | head -20",
  "description": "Recent commits touching main.tex"
}
```

> TOOL

tool_result
id: toolu_01L7tMhbHKzAWAZCotPedXE7
```
e15f8fa docs(body): compress intro and related work, promote signal_ratio + causal_controls to main
091dec2 docs(body): retitle subsubsections to assertive claims; tighten main-results and conclusion prose
8796d95 docs(body): rebalance intro/conclusion and rename contributions as Problem/Mechanism/Method
657bc20 chore(submission): prepare anonymous double-blind code archive for NeurIPS 2026
666f6c8 docs(body): bridge abrupt section transitions and reorder AdaMix paragraph
126c9d2 docs(body): smooth section transitions and tighten intro/method prose
1cc3119 docs(body): rebalance distribution; add Problem Setup, Notation table, failure-mode, reproducibility statement
18c793f docs(abstract): surface SR-MoA, fix backbone count to five, mark R(D) as pre-training computable
20aa945 docs(abstract): rework opening to motivate MoE upgrade and scope normalization class
efe1393 fix(srmoa_fig): polish Figure F.1 labels and tighten causal_controls column
a7c1eef docs(sec4.2): reorganize Main Results into 4 subsubsections; compress prose
2a17007 docs(abstract+checklist): trim abstract sub-clauses; replace em-dashes in checklist
0ade817 docs(math+fig): correct Obs-1 tightness paragraph, expose 12-row factor in 720 arithmetic, polish Residual-IA+ figure
1f0c179 docs(refs): prune 8 orphan bibitems, add 36 NeurIPS-tier citations with argumentative hooks (57 -> 93)
e321d84 docs(polish): expand thin Setup, add appendix-section intros, drop defensive parentheticals
8b05274 fix(layout): relax float specifiers to [!htbp] to remove whitespace gaps
cc315a0 fix(submit): place checklist after appendix per NeurIPS 2026 handbook
d3376eb docs(conclusion): expand […]

> TOOL

tool_use Bash
id: toolu_01P4WvUafYZmsZoGV6FeZtwL
```json
{
  "command": "git show e15f8fa -- main.tex | sed -n '/Related Work/,/section{Raw/p' | head -100",
  "description": "Show related work diff in e15f8fa"
}
```

> TOOL

tool_result
id: toolu_01P4WvUafYZmsZoGV6FeZtwL
```
    - Related Work: 60 → 13 PDF lines. Replace four thread paragraphs with one packed paragraph carrying all 27 orphan citations plus the AdaPTS contrast and the per-window-topology novelty claim. ~28 duplicated cites removed (each already wired in §3 line 252 or §4 lines 419/459/522/524/561).
    - Drop the now-misleading "(positioned in detail in §\ref{sec:related_work})" cross-reference at the §3 problem-statement paragraph.
    - Reinvest the freed page: promote fig:signal_ratio (Frozen Paradox + R(D) ρ=−0.88 dual-panel) into §4.2.2 and tab:causal_controls (eight controls) into §4.2.3, both previously appendix-only. App. F intro updated to point at the now-main-body table; the figure's appendix host (App. M) loses only the figure, prose intact.
    - Build clean, all 27 orphan citations resolve, main body ends on page 9 (the prior boundary); §4.2.2 and §4.2.3 now carry the visual evidence the prose was citing forward.
    
    Entire-Checkpoint: ec50a0f50ca6

diff --git a/main.tex b/main.tex
index 0f46307..43d6807 100644
--- a/main.tex
+++ b/main.tex
@@ -61,15 +61,13 @@ Many time series foundation models (TSFMs) adapt to a target dataset by attachin
 \section{Introduction}
 \label{sec:intro}
 
-Time series foundation models (TSFMs) such as MOMENT~\citep{goswami2024moment}, TimesFM~\citep{das2024timesfm}, Chronos~\citep{ansari2024chronos}, Timer-XL~\citep{liu2025timerxl,liu2024timer}, and Moirai~\citep{woo2024moirai} now provide pretrained representations for time series, alongside a growing ecosystem of pretrained variants and […]

> TOOL

tool_use Bash
id: toolu_011oiAnNbpzzC6rTh5S1WsF9
```json
{
  "command": "git log --oneline --all -- main.tex | grep -iE \"related|trim|compress|cut\" | head -10",
  "description": "Find commits affecting related work"
}
```

> TOOL

tool_result
id: toolu_011oiAnNbpzzC6rTh5S1WsF9
```
e15f8fa docs(body): compress intro and related work, promote signal_ratio + causal_controls to main
a7c1eef docs(sec4.2): reorganize Main Results into 4 subsubsections; compress prose
2a17007 docs(abstract+checklist): trim abstract sub-clauses; replace em-dashes in checklist
24a371c docs(abstract): remove em-dashes, compress collapse description, use canonical MoE term
66b2fe7 docs(related_work): correct MoE-collapse and TSFM-adaptation framings
80da131 refactor(layout): trim main paper to fit Implication paragraph on p.9
f1f29e1 feat: address remaining review items — related work, AdaMix details, RevIN table
a250b1f docs: compress to 9-page limit — trimmed related work, discussion, gaps paragraph
9bad37e docs: major polish — RR-MoA hero figure, compressed sections, imputation results, moved proofs to appendix
dd9f26c docs: add Pareto figure, fix citations to citep, compress method section
```

> TOOL

tool_use Bash
id: toolu_01UieTwaRVrhxK6EhjvwNhTs
```json
{
  "command": "git log --all --pretty=format:\"%h %s\" -S \"Related Work\" -- main.tex | head -10",
  "description": "Find commits adding/removing \"Related Work\" string"
}
```

> TOOL

tool_result
id: toolu_01UieTwaRVrhxK6EhjvwNhTs
```
4215d50 I find it abrupt starting: "This natural mixture-of-experts approach fai
f339af1 chore: add paper files at repo root for Overleaf compatibility
```

> TOOL

tool_use Bash
id: toolu_011sU8nmmo4Fn9nhvh7oQGQm
```json
{
  "command": "git show e15f8fa^:main.tex | sed -n '/^\\\\section{Related Work}/,/^\\\\section{Raw-Routed/p' | head -20",
  "description": "Show pre-compression Related Work source"
}
```

> TOOL

tool_result
id: toolu_011sU8nmmo4Fn9nhvh7oQGQm
```
\section{Related Work}
\label{sec:related_work}

We position RR-MoA against four threads: TSFM adaptation, MoE in foundation models, MoE routing collapse and rescue, and time-series normalization.

\textbf{TSFM Adaptation.} Beyond the broad survey of~\citet{wen2023tssurvey}, a complementary line shows that compact task-specific models match or beat heavyweight pretrained backbones on LTSF benchmarks~\citep{wu2025srsnet, wang2025timemixerpp, xu2024fits, chen2023tsmixer, fu2025selective}: that lightweight raw-input models are competitive is itself evidence that the per-window raw signal carries most of the predictability our diagnostic $R(\mathcal{D})$ exploits (\S\ref{sec:diagnosis}). LLM-reprogrammed forecasters~\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes} inherit per-window normalization upstream of the backbone, so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is attached. We focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a lightweight module to a frozen TSFM~\citep{hu2022lora, houlsby2019adapters, goswami2024moment}; recent variations explore multi-scale finetuning~\citep{qiao2025msft}, importance-based LoRA selection~\citep{li2025trace}, input-representation adaptation~\citep{benechehab2025adapts}, structured pruning~\citep{zhao2025prune}, in-context tuning~\citep{faw2025icf}, retrieval-augmented adaptation~\citep{ning2025tsrag}, and Chronos-specific PEFT~\citep{gupta2024beyondlora}; complementary work computes transferability scores for backbone selection (TEMPLATE, \citealp{zhang2025template}) or provides a unified evaluation suite (GIFT-Eval, \citealp{woo2024gifteval}). These vary the finetuning \textit{strategy} while leaving per-input adapter \textit{topology} fixed; AdaPTS reports the best of several variants per dataset/horizon, treating adapter choice as a per-task hyperparameter rather than per-window routing. We instead route over heterogeneous […]

> AGENT

Found it. **e15f8fa** is the over-cut commit (May 6 15:54). It collapsed Related Work from **60 → 13 PDF lines** by replacing 4 thread paragraphs with one packed paragraph.

The 4 deleted paragraphs (each ~10–14 PDF lines) were:

| Thread | Lines | Key content |
|---|---|---|
| **TSFM Adaptation** | ~14 | wen2023 survey, compact specialists, adapter recipe variants, AdaPTS, AdaMix-vs-RR-MoA topology contrast, novelty claim |
| **MoE in Foundation Models** | ~14 | Shazeer/GShard/Switch/V-MoE, design axes, in-backbone TS-MoE (Moirai-MoE/Time-MoE/SEMPO), MoLE, MMoE, axis-orthogonality claim |
| **MoE routing collapse and rescue** | ~13 | 3 threads (optimization/geometry/architectural), 11-rescue distinction, concurrent AoE/Routing-Free/ERMoE, Wang myth |
| **Normalization in Time Series** | ~9 | RevIN, DishTS/SAN/NST/FAN/DDN, redundancy/IBNorm, our specific MoE consequence |

Plus a 1-line lead-in.

To hit ~40 PDF lines we need ~27 lines back. Three reasonable restorations:

- **A. Most differentiating** — restore *TSFM Adaptation* + *MoE collapse and rescue* threads in full (these carry the AdaMix/AdaPTS contrast and the rescue-thread distinction), drop the other two. ~28 lines added → ~41 total.
- **B. Balanced** — restore all 4 threads but trim each by ~40% (keep one or two anchor citations per thread + the differentiation sentence). ~27 lines […]