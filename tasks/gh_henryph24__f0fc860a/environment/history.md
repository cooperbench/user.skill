> DEVELOPER

cut related work by 20 lines

> TOOL

tool_use Bash
id: toolu_01RQGi1tQAu2HPTc6mPeB4KN
```json
{
  "command": "grep -n \"related\" /home/<USER>/neuralips26/main.tex | head -20",
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
  "command": "wc -l /home/<USER>/neuralips26/main.tex",
  "description": "Get main.tex line count"
}
```

> TOOL

tool_result
id: toolu_019zdtEdmouAFKuKqTtk6Lcg
```
    2870 /home/<USER>/neuralips26/main.tex
```

> TOOL

tool_use Bash
id: toolu_01TcCdDkVT4wCjpRSQ2jTENq
```json
{
  "command": "grep -n \"^\\\\\\\\section\\|^\\\\\\\\subsection\" /home/<USER>/neuralips26/main.tex | head -30",
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
  "file_path": "/home/<USER>/neuralips26/main.tex",
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
  "command": "ls /home/<USER>/neuralips26/main.pdf 2>/dev/null && stat -f \"%Sm\" /home/<USER>/neuralips26/main.pdf 2>/dev/null",
  "description": "Check if main.pdf exists"
}
```

> TOOL

tool_result
id: toolu_01HA954nVzSY8vY5CxwacXHo
```
/home/<USER>/neuralips26/main.pdf
May  6 16:02:52 2026
```

> TOOL

tool_use Bash
id: toolu_01B6iopMpsUwJRk6fPbdEWpJ
```json
{
  "command": "wc -w <<< \"$(sed -n '229p' /home/<USER>/neuralips26/main.tex)\"",
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
  "command": "pdftotext -layout /home/<USER>/neuralips26/main.pdf - 2>/dev/null | sed -n '118,160p'",
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
Author: Hung Phan (Henry) <<REDACTED_EMAIL>>
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
  "command": "grep -n \"elated\\|positioning\" /home/<USER>/neuralips26/main.tex | head -15",
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
  "command": "pdftotext -layout /home/<USER>/neuralips26/main.pdf - 2>/dev/null | sed -n '115,125p'",
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