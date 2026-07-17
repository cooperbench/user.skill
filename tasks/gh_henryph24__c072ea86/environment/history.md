> DEVELOPER

I think writing on the problem setup is not good. Is the problem our contribution as well because look like it is not seen in the literature ?

> TOOL

tool_use Bash
id: toolu_014ivczXcAWz1vLMsnSdGoHe
```json
{
  "command": "find /home/<USER>/neuralips26 -name \"main.tex\" -not -path \"*/node_modules/*\" -not -path \"*/.git/*\" 2>/dev/null | head -5",
  "description": "Find main.tex location"
}
```

> TOOL

tool_result
id: toolu_014ivczXcAWz1vLMsnSdGoHe
```
/home/<USER>/neuralips26/main.tex
```

> TOOL

tool_use Bash
id: toolu_019T4UMoUoxkwG1kCx3YC9vH
```json
{
  "command": "grep -n \"Problem Setup\\|problem_setup\\|sec:problem\\|problem-setup\" /home/<USER>/neuralips26/main.tex",
  "description": "Find Problem Setup section"
}
```

> TOOL

tool_result
id: toolu_019T4UMoUoxkwG1kCx3YC9vH
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01DHH9zMDCBtpNqnuDawcD1x
```json
{
  "command": "grep -n \"\\\\\\\\section\\|\\\\\\\\subsection\" /home/<USER>/neuralips26/main.tex | head -40",
  "description": "List all section headers"
}
```

> TOOL

tool_result
id: toolu_01DHH9zMDCBtpNqnuDawcD1x
```
61:\section{Introduction}
228:\section{Related Work}
240:\section{Raw-Routed Mixture of Adapters (RR-MoA)}
396:\section{Experiments}
398:\subsection{Setup}
408:\subsection{Main Results}
560:\section{Conclusion and Limitations}
1052:\section{Experimental Setup Details}
1129:\section{Deployment-Regime Motivation}
1140:\subsection{Inference Benchmark}
1171:\section{Multi-Horizon Evaluation}
1195:\section{Proposition Proofs}
1237:\subsection{Theoretical Depth of Observation~\ref{thm:mi_decomp}}
1345:\section{LoRA Sweep (Full Results)}
1410:\section{Routing Ablations}
1697:\subsection{Statistics Re-Injection Ablation}
1723:\section{Extended RR-MoA Freeze Grid}
1786:\subsection{Rescue-Baseline Sweep Details}
1818:\subsection{AdaMix Implementation Details}
1856:\section{Normalization Generalization}
1881:\subsection{Cross-Modality Control: Vision MoE}
1912:\section{Top-$k$ Sparse Routing Ablation}
1938:\subsection{Expert Pool Diversity Ablation}
1962:\subsection{Expert Count Scaling}
1988:\section{Imputation Results}
2016:\section{Learnable Normalization Coefficient}
2042:\section{Exact MI Loss and Bound Tightness}
2073:\section{Information Content Diagnostic}
2192:\section{Cross-Backbone RR-MoA}
2285:\section{Extended Full Fine-Tuning Ablation}
2351:\section{Closing the DLinear Gap}
2412:\subsection{Residual-IA: Closing the Remaining Gap}
2813:\subsection{SR-RIA\textsuperscript{+}: Self-Routed Residual-IA\textsuperscript{+}}
2839:\subsection{Pure Raw-MLP MoE Ablation: Quantifying the TSFM's Contribution}
```

> TOOL

tool_use Bash
id: toolu_01CRH1ShGDA8jiwC412WBytB
```json
{
  "command": "grep -n -i \"problem\" /home/<USER>/neuralips26/main.tex | head -30",
  "description": "Find problem-related text"
}
```

> TOOL

tool_result
id: toolu_01CRH1ShGDA8jiwC412WBytB
```
66:Standard TSFM adapters apply the \emph{same} regression head to every window (Figure~\ref{fig:problem_overview}a): flatten-then-project for MOMENT~\citep{goswami2024moment} and PatchTST~\citep{nie2023patchtst}, an autoregressive residual block for TimesFM~\citep{das2024timesfm}. Real time series mix heterogeneous regimes whose \emph{shape} variation (periodicity, trends, level shifts, change points) survives instance normalization and lives in the hidden states across layers~\citep{wilinski2025tsfm_representations, pandey2025tsfm_semantics}, motivating a per-window mixture of topologically distinct expert heads with a learned router. Keeping the backbone frozen is also what makes deployment practical: a shared TSFM in GPU memory serves many tenants through lightweight per-task adapters hot-swapped from host RAM, an arrangement per-dataset models like DLinear~\citep{zeng2023dlinear} cannot match (Appendices~\ref{app:deployment},~\ref{app:benchmark}).
68:This natural mixture-of-experts approach fails on instance-normalized TSFMs once any backbone layers are unfrozen (Figure~\ref{fig:problem_overview}b). Combining an AdaMix-style adapter pool~\citep{wang2022adamix} with a hidden-state softmax router and Switch-style load balancing~\citep{fedus2022switch} on MOMENT$+$RevIN drops routing entropy to zero in most unfrozen configurations (Table~\ref{tab:adamix}): every window is sent to one expert and the rest are never used. We call this \emph{normalization-induced routing collapse}: RevIN~\citep{kim2021revin} strips the per-window mean and variance the router needs to distinguish regimes (formalized in Observation~\ref{thm:mi_decomp}; signal-ratio diagnostic in Figure~\ref{fig:signal_ratio}). Even frozen, hidden-state routing underperforms; unfrozen, the dominant expert's larger gradients reshape the backbone to serve it […]

> TOOL

tool_use Read
id: toolu_01XzyKfz4AsphvaxrrJAQcqs
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 240,
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_01XzyKfz4AsphvaxrrJAQcqs
```
240	\section{Raw-Routed Mixture of Adapters (RR-MoA)}
241	\label{sec:method}
242	
243	We now formalize the adapter problem and specify RR-MoA: a per-window mixture in which the router reads the raw, pre-normalization signal while the experts consume the frozen TSFM's hidden states. Cost, expert pool, and deployment implications close the section.
244	
245	\textbf{Problem setup.} Given a window $\mathbf{x}\in\mathbb{R}^{T\times c}$ ($T{=}512$, $c$ channels), forecasting predicts $\mathbf{y}\in\mathbb{R}^{h\times c}$ at horizons $h\in\{96,192,336,720\}$ under MSE loss (imputation uses the same formalism with $\mathbf{y}$ as the reconstruction target). A pretrained TSFM acts as a feature extractor $f_\theta:\mathbb{R}^{T\times c}\to\mathbb{R}^{P\times d}$ ($P$ patches of dim $d$) with $\theta$ \emph{frozen} ($\nabla_\theta\!\equiv\!0$); we train only an adapter $g_\phi:\mathbb{R}^{P\times d}\to\mathbb{R}^{h\times c}$ with $|\phi|\leq 500$K, capping per-task storage at ${\sim}2$\,MB to enable the multi-tenant hot-swap regime (App.~\ref{app:deployment}). A \emph{per-window mixture of adapters} replaces $g_\phi$ with $K$ experts $\{\mathrm{Expert}_j\}_{j=1}^K$ plus a router $G_\psi$ that returns a sparse weight $\widetilde{w}\in\Delta^{K-1}$ supported on a Top-$k$ subset ($k\leq K$), giving $\hat{\mathbf{y}}=\sum_{j} \widetilde{w}_j\,\mathrm{Expert}_j(f_\theta(\mathbf{x}))$ trained by $\min_{\phi,\psi}\,\mathbb{E}\,\|\hat{\mathbf{y}}-\mathbf{y}\|_2^2$. The design question is what signal $G_\psi$ should read: prior work routes on the hidden states $f_\theta(\mathbf{x})$, which fails on instance-normalized TSFMs (\S\ref{sec:main_results}).
246	
247	\begin{figure}[t!]
248	\centering
249	\resizebox{\columnwidth}{!}{%
250	\begin{tikzpicture}[
251	    >=Stealth,
252	    % -- […]

> TOOL

tool_use Read
id: toolu_01Hw6viYb37VwfNKouD9Uyh7
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 61,
  "limit": 170
}
```

> TOOL

tool_result
id: toolu_01Hw6viYb37VwfNKouD9Uyh7
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
id: toolu_01BbxFq7EWyhFcMkAP592rk1
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 228,
  "limit": 15
}
```

> TOOL

tool_result
id: toolu_01BbxFq7EWyhFcMkAP592rk1
```
228	\section{Related Work}
229	
230	We position RR-MoA against four threads: TSFM adaptation, MoE in foundation models, MoE routing collapse and rescue, and time-series normalization.
231	
232	\textbf{TSFM Adaptation.} Beyond the broad survey of~\citet{wen2023tssurvey}, a complementary line shows that compact task-specific models match or beat heavyweight pretrained backbones on LTSF benchmarks~\citep{wu2025srsnet, wang2025timemixerpp, xu2024fits, chen2023tsmixer, fu2025selective}: that lightweight raw-input models are competitive is itself evidence that the per-window raw signal carries most of the predictability our diagnostic $R(\mathcal{D})$ exploits (\S\ref{sec:diagnosis}). LLM-reprogrammed forecasters~\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes} inherit per-window normalization upstream of the backbone, so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is attached. We focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a lightweight module to a frozen TSFM~\citep{hu2022lora, houlsby2019adapters, goswami2024moment}; recent variations explore multi-scale finetuning~\citep{qiao2025msft}, importance-based LoRA selection~\citep{li2025trace}, input-representation adaptation~\citep{benechehab2025adapts}, structured pruning~\citep{zhao2025prune}, in-context tuning~\citep{faw2025icf}, retrieval-augmented adaptation~\citep{ning2025tsrag}, and Chronos-specific PEFT~\citep{gupta2024beyondlora}; complementary work computes transferability scores for backbone selection (TEMPLATE, \citealp{zhang2025template}) or provides a unified evaluation suite (GIFT-Eval, \citealp{woo2024gifteval}). These vary the finetuning \textit{strategy} while leaving per-input adapter \textit{topology} fixed; AdaPTS reports the best of several variants per dataset/horizon, treating adapter choice as a per-task hyperparameter rather than per-window routing. We […]

> AGENT

You're right on both counts. The failure mode (normalization-induced routing collapse) **is** one of your contributions; the intro lists it as contribution 1 (line 76) and related work explicitly claims it as "not characterized in prior literature" (line 238). But the current "Problem setup." paragraph (line 245) reads as a generic formalization of per-window mixture-of-adapters, with the failure relegated to a forward-pointing parenthetical ("prior work routes on hidden states, which fails on instance-normalized TSFMs"). That framing hides the contribution: the reader sees a textbook MoA setup, not a novel problem statement.

Two ways to fix it, with the main tradeoff:

1. **Split into "Task setup" (standard formalism) + "Problem statement" (novel failure mode you identify).** Owns the contribution where the method begins, and matches the contribution-1 claim in the intro. Costs ~6-10 lines.
2. **Rewrite the existing paragraph to lead with the unsolved problem, with the formalism in service of it.** Same length, but the reader hits "what's broken and unaddressed" before "here is notation."

I'd recommend (1): the failure mode deserves its own labelled paragraph since you build a whole diagnosis around it (Observation 1, $R(\mathcal{D})$, eight causal controls). Want me to draft it?