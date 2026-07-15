> DEVELOPER

I think writing on the problem setup is not good. Is the problem our contribution as well because look like it is not seen in the literature ?

> TOOL

tool_use Bash
id: toolu_014ivczXcAWz1vLMsnSdGoHe
```json
{
  "command": "find /Users/hungpq2412/neuralips26 -name \"main.tex\" -not -path \"*/node_modules/*\" -not -path \"*/.git/*\" 2>/dev/null | head -5",
  "description": "Find main.tex location"
}
```

> TOOL

tool_result
id: toolu_014ivczXcAWz1vLMsnSdGoHe
```
/Users/hungpq2412/neuralips26/main.tex
```

> TOOL

tool_use Bash
id: toolu_019T4UMoUoxkwG1kCx3YC9vH
```json
{
  "command": "grep -n \"Problem Setup\\|problem_setup\\|sec:problem\\|problem-setup\" /Users/hungpq2412/neuralips26/main.tex",
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
  "command": "grep -n \"\\\\\\\\section\\|\\\\\\\\subsection\" /Users/hungpq2412/neuralips26/main.tex | head -40",
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
  "command": "grep -n -i \"problem\" /Users/hungpq2412/neuralips26/main.tex | head -30",
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
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
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
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
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
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
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

> DEVELOPER

I want problem formulation to read very explicitly. Mention of any specific ram number is not good

> TOOL

tool_use Read
id: toolu_01Mfj9oXYkHAHpfMb9Dg49EX
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 243,
  "limit": 5
}
```

> TOOL

tool_result
id: toolu_01Mfj9oXYkHAHpfMb9Dg49EX
```
243	We now formalize the adapter problem and specify RR-MoA: a per-window mixture in which the router reads the raw, pre-normalization signal while the experts consume the frozen TSFM's hidden states. Cost, expert pool, and deployment implications close the section.
244	
245	\textbf{Problem setup.} Given a window $\mathbf{x}\in\mathbb{R}^{T\times c}$ ($T{=}512$, $c$ channels), forecasting predicts $\mathbf{y}\in\mathbb{R}^{h\times c}$ at horizons $h\in\{96,192,336,720\}$ under MSE loss (imputation uses the same formalism with $\mathbf{y}$ as the reconstruction target). A pretrained TSFM acts as a feature extractor $f_\theta:\mathbb{R}^{T\times c}\to\mathbb{R}^{P\times d}$ ($P$ patches of dim $d$) with $\theta$ \emph{frozen} ($\nabla_\theta\!\equiv\!0$); we train only an adapter $g_\phi:\mathbb{R}^{P\times d}\to\mathbb{R}^{h\times c}$ with $|\phi|\leq 500$K, capping per-task storage at ${\sim}2$\,MB to enable the multi-tenant hot-swap regime (App.~\ref{app:deployment}). A \emph{per-window mixture of adapters} replaces $g_\phi$ with $K$ experts $\{\mathrm{Expert}_j\}_{j=1}^K$ plus a router $G_\psi$ that returns a sparse weight $\widetilde{w}\in\Delta^{K-1}$ supported on a Top-$k$ subset ($k\leq K$), giving $\hat{\mathbf{y}}=\sum_{j} \widetilde{w}_j\,\mathrm{Expert}_j(f_\theta(\mathbf{x}))$ trained by $\min_{\phi,\psi}\,\mathbb{E}\,\|\hat{\mathbf{y}}-\mathbf{y}\|_2^2$. The design question is what signal $G_\psi$ should read: prior work routes on the hidden states $f_\theta(\mathbf{x})$, which fails on instance-normalized TSFMs (\S\ref{sec:main_results}).
246	
247	\begin{figure}[t!]
```

> TOOL

tool_use Edit
id: toolu_011cG5bM5GoA7DmCe1cRgGYW
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "We now formalize the adapter problem and specify RR-MoA: a per-window mixture in which the router reads the raw, pre-normalization signal while the experts consume the frozen TSFM's hidden states. Cost, expert pool, and deployment implications close the section.\n\n\\textbf{Problem setup.} Given a window $\\mathbf{x}\\in\\mathbb{R}^{T\\times c}$ ($T{=}512$, $c$ channels), forecasting predicts $\\mathbf{y}\\in\\mathbb{R}^{h\\times c}$ at horizons $h\\in\\{96,192,336,720\\}$ under MSE loss (imputation uses the same formalism with $\\mathbf{y}$ as the reconstruction target). A pretrained TSFM acts as a feature extractor $f_\\theta:\\mathbb{R}^{T\\times c}\\to\\mathbb{R}^{P\\times d}$ ($P$ patches of dim $d$) with $\\theta$ \\emph{frozen} ($\\nabla_\\theta\\!\\equiv\\!0$); we train only an adapter $g_\\phi:\\mathbb{R}^{P\\times d}\\to\\mathbb{R}^{h\\times c}$ with $|\\phi|\\leq 500$K, capping per-task storage at ${\\sim}2$\\,MB to enable the multi-tenant hot-swap regime (App.~\\ref{app:deployment}). A \\emph{per-window mixture of adapters} replaces $g_\\phi$ with $K$ experts $\\{\\mathrm{Expert}_j\\}_{j=1}^K$ plus a router $G_\\psi$ that returns a sparse weight $\\widetilde{w}\\in\\Delta^{K-1}$ supported on a Top-$k$ subset ($k\\leq K$), giving $\\hat{\\mathbf{y}}=\\sum_{j} \\widetilde{w}_j\\,\\mathrm{Expert}_j(f_\\theta(\\mathbf{x}))$ trained by $\\min_{\\phi,\\psi}\\,\\mathbb{E}\\,\\|\\hat{\\mathbf{y}}-\\mathbf{y}\\|_2^2$. The design question is what signal $G_\\psi$ should read: prior work routes on the hidden states $f_\\theta(\\mathbf{x})$, which fails on instance-normalized TSFMs (\\S\\ref{sec:main_results}).",
  "new_string": "We first state the task setup, then the problem we identify, then specify RR-MoA: a per-window mixture in which […]

> TOOL

tool_result
id: toolu_011cG5bM5GoA7DmCe1cRgGYW
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01Le5eHrM5xCTo9QJB3sJcSC
```json
{
  "command": "grep -n \"sec:related\\|sec:diagnosis\\|sec:main_results\" /Users/hungpq2412/neuralips26/main.tex | head -10",
  "description": "Verify section labels exist"
}
```

> TOOL

tool_result
id: toolu_01Le5eHrM5xCTo9QJB3sJcSC
```
232:\textbf{TSFM Adaptation.} Beyond the broad survey of~\citet{wen2023tssurvey}, a complementary line shows that compact task-specific models match or beat heavyweight pretrained backbones on LTSF benchmarks~\citep{wu2025srsnet, wang2025timemixerpp, xu2024fits, chen2023tsmixer, fu2025selective}: that lightweight raw-input models are competitive is itself evidence that the per-window raw signal carries most of the predictability our diagnostic $R(\mathcal{D})$ exploits (\S\ref{sec:diagnosis}). LLM-reprogrammed forecasters~\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes} inherit per-window normalization upstream of the backbone, so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is attached. We focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a lightweight module to a frozen TSFM~\citep{hu2022lora, houlsby2019adapters, goswami2024moment}; recent variations explore multi-scale finetuning~\citep{qiao2025msft}, importance-based LoRA selection~\citep{li2025trace}, input-representation adaptation~\citep{benechehab2025adapts}, structured pruning~\citep{zhao2025prune}, in-context tuning~\citep{faw2025icf}, retrieval-augmented adaptation~\citep{ning2025tsrag}, and Chronos-specific PEFT~\citep{gupta2024beyondlora}; complementary work computes transferability scores for backbone selection (TEMPLATE, \citealp{zhang2025template}) or provides a unified evaluation suite (GIFT-Eval, \citealp{woo2024gifteval}). These vary the finetuning \textit{strategy} while leaving per-input adapter \textit{topology} fixed; AdaPTS reports the best of several variants per dataset/horizon, treating adapter choice as a per-task hyperparameter rather than per-window routing. We instead route over heterogeneous expert topologies per window; the closest precedent in spirit is mixture-of-adapters in the LLM setting (AdaMix~\citep{wang2022adamix} mixes copies of one adapter type, whereas […]

> TOOL

tool_use Bash
id: toolu_011zQHusXYvimv1KtConSJfc
```json
{
  "command": "grep -n \"section{Related\\|label{sec:related\" /Users/hungpq2412/neuralips26/main.tex",
  "description": "Check related work label"
}
```

> TOOL

tool_result
id: toolu_011zQHusXYvimv1KtConSJfc
```
228:\section{Related Work}
```

> TOOL

tool_use Edit
id: toolu_0146wMC6KsL6mGvTqMNtspSa
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "it is not addressed by prior MoE-collapse, MoE-adapter, or time-series-normalization work (\\S\\ref{sec:related}).",
  "new_string": "it is not addressed by prior MoE-collapse, MoE-adapter, or time-series-normalization work (\\S\\ref{sec:related_work})."
}
```

> TOOL

tool_result
id: toolu_0146wMC6KsL6mGvTqMNtspSa
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_0117xnNdxLRTrJScMx7kdKYc
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\section{Related Work}\n\nWe position RR-MoA against four threads:",
  "new_string": "\\section{Related Work}\n\\label{sec:related_work}\n\nWe position RR-MoA against four threads:"
}
```

> TOOL

tool_result
id: toolu_0117xnNdxLRTrJScMx7kdKYc
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> AGENT

Now compile to verify the build is clean.

> TOOL

tool_use Bash
id: toolu_01T5386YU55wsCBCWQqsQ6tF
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/pdflatex_pass1.log 2>&1; echo \"EXIT=$?\"",
  "description": "Compile main.tex pass 1"
}
```

> TOOL

tool_result
id: toolu_01T5386YU55wsCBCWQqsQ6tF
```
EXIT=0
```

> TOOL

tool_use Bash
id: toolu_01BNwVpjRL4vZyfKFhDjVaV2
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/pdflatex_pass2.log 2>&1; echo \"EXIT=$?\"",
  "description": "Compile main.tex pass 2 to resolve refs"
}
```

> TOOL

tool_result
id: toolu_01BNwVpjRL4vZyfKFhDjVaV2
```
EXIT=0
```

> TOOL

tool_use Bash
id: toolu_01YVjzZWie2dkQeYfSceQjYY
```json
{
  "command": "grep -i \"undefined\\|warning.*ref\\|error\" /tmp/pdflatex_pass2.log | grep -iv \"warning: package\" | head -20",
  "description": "Check for undefined refs / errors"
}
```

> TOOL

tool_result
id: toolu_01YVjzZWie2dkQeYfSceQjYY
```
(/Users/hungpq2412/Library/texmf/tex/generic/pgfplots/pgfplots.errorbars.code.t
```

> TOOL

tool_use Bash
id: toolu_015B1LuFqVWLLrcMN7WYDKrQ
```json
{
  "command": "grep -ci \"no file\\|undefined references\\|unresolved\" /tmp/pdflatex_pass2.log; pdfinfo main.pdf 2>/dev/null | grep -E \"Pages|Title\"",
  "description": "Final build check"
}
```

> TOOL

tool_result
id: toolu_015B1LuFqVWLLrcMN7WYDKrQ
```
0
Title:           
Pages:           52
```

> AGENT

Build is clean (exit 0, no undefined refs, 52 pages). 

Changes to the Problem Setup at `main.tex:243-248`:

- **Renamed** `Problem setup` → split into `Task setup` (formal task formalism) and `Problem statement (this paper)` (the failure mode you identify).
- **Removed** the specific RAM/storage number (`{\sim}2$\,MB`); replaced with "small parameter budget" and "many task-specific adapters can be hot-swapped onto a single shared backbone."
- **Promoted the failure mode to the central problem.** New paragraph names *normalization-induced routing collapse* explicitly, asserts it is "not previously characterized," and states the formal problem as: *given a frozen instance-normalized TSFM, find the routing input $u(\mathbf{x})$ such that the per-window mixture trains without entropy collapse and improves over a single static head.*
- **Forward-points** to §diagnosis and §main_results as the answer ($u(\mathbf{x}){=}\mathbf{x}$, raw window) and to §related_work for the prior-art gap.
- Added `\label{sec:related_work}` so the cross-reference resolves.

The contribution-1 claim in the intro now lands in the method section's own framing, not just as a forward-reference.

> DEVELOPER

is the flow smooth now, problem is very clearly defined and cited ?

> TOOL

tool_use Read
id: toolu_01SByEmhgU464KL2riVTBbhP
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 240,
  "limit": 12
}
```

> TOOL

tool_result
id: toolu_01SByEmhgU464KL2riVTBbhP
```
240	
241	\section{Raw-Routed Mixture of Adapters (RR-MoA)}
242	\label{sec:method}
243	
244	We first state the task setup, then the problem we identify, then specify RR-MoA: a per-window mixture in which the router reads the raw, pre-normalization signal while the experts consume the frozen TSFM's hidden states. Cost, expert pool, and deployment implications close the section.
245	
246	\textbf{Task setup.} Given a window $\mathbf{x}\in\mathbb{R}^{T\times c}$ ($T{=}512$, $c$ channels), forecasting predicts $\mathbf{y}\in\mathbb{R}^{h\times c}$ at horizons $h\in\{96,192,336,720\}$ under MSE loss (imputation uses the same formalism with $\mathbf{y}$ as the reconstruction target). A pretrained TSFM acts as a feature extractor $f_\theta:\mathbb{R}^{T\times c}\to\mathbb{R}^{P\times d}$ ($P$ patches of dim $d$) with $\theta$ \emph{frozen} ($\nabla_\theta\!\equiv\!0$); we train only an adapter $g_\phi:\mathbb{R}^{P\times d}\to\mathbb{R}^{h\times c}$ with a small parameter budget ($|\phi|\leq 500$K), so that many task-specific adapters can be hot-swapped onto a single shared backbone (App.~\ref{app:deployment}). A \emph{per-window mixture of adapters} replaces $g_\phi$ with $K$ experts $\{\mathrm{Expert}_j\}_{j=1}^K$ plus a router $G_\psi$ that returns a sparse weight $\widetilde{w}\in\Delta^{K-1}$ supported on a Top-$k$ subset ($k\leq K$), giving $\hat{\mathbf{y}}=\sum_{j} \widetilde{w}_j\,\mathrm{Expert}_j(f_\theta(\mathbf{x}))$ trained by $\min_{\phi,\psi}\,\mathbb{E}\,\|\hat{\mathbf{y}}-\mathbf{y}\|_2^2$.
247	
248	\textbf{Problem statement (this paper).} The standard MoE recipe lets the router $G_\psi$ read the backbone's hidden states $f_\theta(\mathbf{x})$. We claim, and this paper […]

> TOOL

tool_use Bash
id: toolu_01DXNEzN2sTUCUdYVUdBciFL
```json
{
  "command": "grep -n \"^\\\\\\\\textbf\\|^\\\\\\\\paragraph\\|^\\\\\\\\section\\|^\\\\\\\\subsection\" /Users/hungpq2412/neuralips26/main.tex | awk -F: '$1>=240 && $1<=400' | head -30",
  "description": "List structure of method section"
}
```

> TOOL

tool_result
id: toolu_01DXNEzN2sTUCUdYVUdBciFL
```
241:\section{Raw-Routed Mixture of Adapters (RR-MoA)}
246:\textbf{Task setup.} Given a window $\mathbf{x}\in\mathbb{R}^{T\times c}$ ($T{=}512$, $c$ channels), forecasting predicts $\mathbf{y}\in\mathbb{R}^{h\times c}$ at horizons $h\in\{96,192,336,720\}$ under MSE loss (imputation uses the same formalism with $\mathbf{y}$ as the reconstruction target). A pretrained TSFM acts as a feature extractor $f_\theta:\mathbb{R}^{T\times c}\to\mathbb{R}^{P\times d}$ ($P$ patches of dim $d$) with $\theta$ \emph{frozen} ($\nabla_\theta\!\equiv\!0$); we train only an adapter $g_\phi:\mathbb{R}^{P\times d}\to\mathbb{R}^{h\times c}$ with a small parameter budget ($|\phi|\leq 500$K), so that many task-specific adapters can be hot-swapped onto a single shared backbone (App.~\ref{app:deployment}). A \emph{per-window mixture of adapters} replaces $g_\phi$ with $K$ experts $\{\mathrm{Expert}_j\}_{j=1}^K$ plus a router $G_\psi$ that returns a sparse weight $\widetilde{w}\in\Delta^{K-1}$ supported on a Top-$k$ subset ($k\leq K$), giving $\hat{\mathbf{y}}=\sum_{j} \widetilde{w}_j\,\mathrm{Expert}_j(f_\theta(\mathbf{x}))$ trained by $\min_{\phi,\psi}\,\mathbb{E}\,\|\hat{\mathbf{y}}-\mathbf{y}\|_2^2$.
248:\textbf{Problem statement (this paper).} The standard MoE recipe lets the router $G_\psi$ read the backbone's hidden states $f_\theta(\mathbf{x})$. We claim, and this paper establishes, that on instance-normalized TSFMs this choice has a structural failure mode not previously characterized: the router's input is missing, by construction of an upstream architectural normalizer, the per-window statistics that distinguish regimes, so $G_\psi$ collapses to a single expert and the remaining $K{-}1$ experts receive no gradient. We name this failure \emph{normalization-induced routing […]

> TOOL

tool_use Edit
id: toolu_01AKSw5kcxLbvg1WoPaHj9Fo
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\textbf{Problem statement (this paper).} The standard MoE recipe lets the router $G_\\psi$ read the backbone's hidden states $f_\\theta(\\mathbf{x})$. We claim, and this paper establishes, that on instance-normalized TSFMs this choice has a structural failure mode not previously characterized: the router's input is missing, by construction of an upstream architectural normalizer, the per-window statistics that distinguish regimes, so $G_\\psi$ collapses to a single expert and the remaining $K{-}1$ experts receive no gradient. We name this failure \\emph{normalization-induced routing collapse} and state it as the central problem of this work: \\emph{given a frozen instance-normalized TSFM, find the routing input $u(\\mathbf{x})$ such that the per-window mixture $\\sum_j G_\\psi(u(\\mathbf{x}))_j\\,\\mathrm{Expert}_j(f_\\theta(\\mathbf{x}))$ trains without entropy collapse and improves over a single static head.} The collapse is upstream of the optimization-induced collapse that load-balance, z-loss, ReLU-routing, and expert-choice rescues target (Table~\\ref{tab:rescue}); it is not addressed by prior MoE-collapse, MoE-adapter, or time-series-normalization work (\\S\\ref{sec:related_work}). Sections~\\ref{sec:diagnosis} and~\\ref{sec:main_results} answer the problem with $u(\\mathbf{x})\\!=\\!\\mathbf{x}$ (the raw, pre-normalization window) and verify the answer with eight causal controls.",
  "new_string": "\\textbf{Problem statement (this paper).} The standard MoE recipe~\\citep{shazeer2017outrageously, fedus2022switch} lets the router $G_\\psi$ read the backbone's hidden states $f_\\theta(\\mathbf{x})$, and this is the choice […]

> TOOL

tool_result
id: toolu_01AKSw5kcxLbvg1WoPaHj9Fo
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> AGENT

Now verify all citations exist in the bibliography and the build is clean.

> TOOL

tool_use Bash
id: toolu_015AzptuRhjQWY1GPsssnJGT
```json
{
  "command": "grep -n \"\\\\\\\\bibitem{shazeer2017outrageously\\\\|\\\\\\\\bibitem{fedus2022switch\\\\|\\\\\\\\bibitem{wang2022adamix\\\\|\\\\\\\\bibitem{kim2021revin\\\\|\\\\\\\\bibitem{goswami2024moment\\\\|\\\\\\\\bibitem{nie2023patchtst\\\\|\\\\\\\\bibitem{das2024timesfm\\\\|\\\\\\\\bibitem{zoph2022stmoe\\\\|\\\\\\\\bibitem{wang2025remoe\\\\|\\\\\\\\bibitem{zhou2022expertchoice\\\\|\\\\\\\\bibitem{wu2024mole\\\\|\\\\\\\\bibitem{chi2022representation\\\\|\\\\\\\\bibitem{wu2024mhmoe\\\\|\\\\\\\\bibitem{puigcerver2024softmoe\\\\|\\\\\\\\bibitem{panda2024densebackprop\\\\|\\\\\\\\bibitem{hua2025inputaware\\\\|\\\\\\\\bibitem{guo2025expertspec\\\\|\\\\\\\\bibitem{liu2022nonstationary\\\\|\\\\\\\\bibitem{fan2023dishts\\\\|\\\\\\\\bibitem{liu2023san\\\\|\\\\\\\\bibitem{ye2024fan\\\\|\\\\\\\\bibitem{dai2024ddn\\\\|\\\\\\\\bibitem{berthelier2026revin\\\\|\\\\\\\\bibitem{zou2025ibnorm\" /Users/hungpq2412/neuralips26/main.tex | wc -l",
  "description": "Count matching bibitems"
}
```

> TOOL

tool_result
id: toolu_015AzptuRhjQWY1GPsssnJGT
```
       0
```

> TOOL

tool_use Bash
id: toolu_01Ybe247EyJwn3jDprPQxxev
```json
{
  "command": "grep -c \"bibitem\" /Users/hungpq2412/neuralips26/main.tex; grep -n \"thebibliography\\|\\\\\\\\bibitem\" /Users/hungpq2412/neuralips26/main.tex | head -5",
  "description": "Check bibliography format"
}
```

> TOOL

tool_result
id: toolu_01Ybe247EyJwn3jDprPQxxev
```
93
572:\begin{thebibliography}{20}
574:\bibitem[Dosovitskiy et~al.(2021)]{dosovitskiy2021vit}
579:\bibitem[Goswami et~al.(2024)]{goswami2024moment}
584:\bibitem[Das et~al.(2024)]{das2024timesfm}
589:\bibitem[Ansari et~al.(2024)]{ansari2024chronos}
```

> TOOL

tool_use Bash
id: toolu_01RuEc9tYpzgDUgFb8FJwEay
```json
{
  "command": "for k in shazeer2017outrageously fedus2022switch wang2022adamix kim2021revin goswami2024moment nie2023patchtst das2024timesfm zoph2022stmoe wang2025remoe zhou2022expertchoice wu2024mole chi2022representation wu2024mhmoe puigcerver2024softmoe panda2024densebackprop hua2025inputaware guo2025expertspec liu2022nonstationary fan2023dishts liu2023san ye2024fan dai2024ddn berthelier2026revin zou2025ibnorm; do\n  if grep -q \"\\\\\\\\bibitem.*{$k}\" /Users/hungpq2412/neuralips26/main.tex; then\n    echo \"OK   $k\"\n  else\n    echo \"MISS $k\"\n  fi\ndone",
  "description": "Check each citation key"
}
```

> TOOL

tool_result
id: toolu_01RuEc9tYpzgDUgFb8FJwEay
```
OK   shazeer2017outrageously
OK   fedus2022switch
OK   wang2022adamix
OK   kim2021revin
OK   goswami2024moment
OK   nie2023patchtst
OK   das2024timesfm
OK   zoph2022stmoe
OK   wang2025remoe
OK   zhou2022expertchoice
OK   wu2024mole
OK   chi2022representation
OK   wu2024mhmoe
OK   puigcerver2024softmoe
OK   panda2024densebackprop
OK   hua2025inputaware
OK   guo2025expertspec
OK   liu2022nonstationary
OK   fan2023dishts
OK   liu2023san
OK   ye2024fan
OK   dai2024ddn
OK   berthelier2026revin
OK   zou2025ibnorm
```

> AGENT

All 24 citations resolve. Recompile and verify.

> TOOL

tool_use Bash
id: toolu_01HLKDTzYn2mPCSjcCLbmmN7
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/p1.log 2>&1 && pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/p2.log 2>&1; echo \"EXIT=$?\"; grep -i \"undefined\\|! latex error\\|! emergency\" /tmp/p2.log | head -5; pdfinfo main.pdf 2>/dev/null | grep Pages",
  "description": "Two-pass compile + error check"
}
```

> TOOL

tool_result
id: toolu_01HLKDTzYn2mPCSjcCLbmmN7
```
EXIT=0
Pages:           52
```

> AGENT

Build clean (exit 0, no undefined refs, 52 pages).

**What changed and why:**

1. **Added inline citations at every claim** in the Problem statement — Shazeer/Switch for the standard MoE recipe, AdaMix as the closest TSFM-adapter precedent, RevIN + MOMENT/PatchTST/TimesFM at "instance-normalized TSFMs," Switch+ST-MoE+ReMoE+Expert-Choice at the optimization rescues, and dedicated citation clusters for the three prior-art threads we claim do not address the problem (MoE-adapter, MoE routing-collapse, time-series-normalization). Reviewers can now check the novelty claim without flipping to Related Work.

2. **Pulled out the formal problem into a `quote` block** so the central question is visually unmissable and reads as the section's anchor.

3. **Added forward-ref to Observation 1** at the point where the routing-information-loss claim is first made, so the formalization is signposted at the moment of the claim.

4. **Tightened the closing bridge:** the previous version pointed only to other sections; now it says "the remainder of this section answers the problem with $u(\mathbf{x}){=}\mathbf{x}$" and then lists the verification (§diagnosis, §main_results, 720-run rescue sweep, $2.7\times$ margin). Reader knows exactly what's coming next in this same section vs. what's in later sections.

**Flow now reads:** task setup (notation) → standard MoE recipe and what it does (cited) → claim […]