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

> DEVELOPER

I want problem formulation to read very explicitly. Mention of any specific ram number is not good

> TOOL

tool_use Read
id: toolu_01Mfj9oXYkHAHpfMb9Dg49EX
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
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
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "We now formalize the adapter problem and specify RR-MoA: a per-window mixture in which the router reads the raw, pre-normalization signal while the experts consume the frozen TSFM's hidden states. Cost, expert pool, and deployment implications close the section.\n\n\\textbf{Problem setup.} Given a window $\\mathbf{x}\\in\\mathbb{R}^{T\\times c}$ ($T{=}512$, $c$ channels), forecasting predicts $\\mathbf{y}\\in\\mathbb{R}^{h\\times c}$ at horizons $h\\in\\{96,192,336,720\\}$ under MSE loss (imputation uses the same formalism with $\\mathbf{y}$ as the reconstruction target). A pretrained TSFM acts as a feature extractor $f_\\theta:\\mathbb{R}^{T\\times c}\\to\\mathbb{R}^{P\\times d}$ ($P$ patches of dim $d$) with $\\theta$ \\emph{frozen} ($\\nabla_\\theta\\!\\equiv\\!0$); we train only an adapter $g_\\phi:\\mathbb{R}^{P\\times d}\\to\\mathbb{R}^{h\\times c}$ with $|\\phi|\\leq 500$K, capping per-task storage at ${\\sim}2$\\,MB to enable the multi-tenant hot-swap regime (App.~\\ref{app:deployment}). A \\emph{per-window mixture of adapters} replaces $g_\\phi$ with $K$ experts $\\{\\mathrm{Expert}_j\\}_{j=1}^K$ plus a router $G_\\psi$ that returns a sparse weight $\\widetilde{w}\\in\\Delta^{K-1}$ supported on a Top-$k$ subset ($k\\leq K$), giving $\\hat{\\mathbf{y}}=\\sum_{j} \\widetilde{w}_j\\,\\mathrm{Expert}_j(f_\\theta(\\mathbf{x}))$ trained by $\\min_{\\phi,\\psi}\\,\\mathbb{E}\\,\\|\\hat{\\mathbf{y}}-\\mathbf{y}\\|_2^2$. The design question is what signal $G_\\psi$ should read: prior work routes on the hidden states $f_\\theta(\\mathbf{x})$, which fails on instance-normalized TSFMs (\\S\\ref{sec:main_results}).",
  "new_string": "We first state the task setup, then the problem we identify, then specify RR-MoA: a per-window mixture in which […]

> TOOL

tool_result
id: toolu_011cG5bM5GoA7DmCe1cRgGYW
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01Le5eHrM5xCTo9QJB3sJcSC
```json
{
  "command": "grep -n \"sec:related\\|sec:diagnosis\\|sec:main_results\" /home/<USER>/neuralips26/main.tex | head -10",
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
  "command": "grep -n \"section{Related\\|label{sec:related\" /home/<USER>/neuralips26/main.tex",
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
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "it is not addressed by prior MoE-collapse, MoE-adapter, or time-series-normalization work (\\S\\ref{sec:related}).",
  "new_string": "it is not addressed by prior MoE-collapse, MoE-adapter, or time-series-normalization work (\\S\\ref{sec:related_work})."
}
```

> TOOL

tool_result
id: toolu_0146wMC6KsL6mGvTqMNtspSa
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_0117xnNdxLRTrJScMx7kdKYc
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "\\section{Related Work}\n\nWe position RR-MoA against four threads:",
  "new_string": "\\section{Related Work}\n\\label{sec:related_work}\n\nWe position RR-MoA against four threads:"
}
```

> TOOL

tool_result
id: toolu_0117xnNdxLRTrJScMx7kdKYc
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
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
(/home/<USER>/Library/texmf/tex/generic/pgfplots/pgfplots.errorbars.code.t
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
  "file_path": "/home/<USER>/neuralips26/main.tex",
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
  "command": "grep -n \"^\\\\\\\\textbf\\|^\\\\\\\\paragraph\\|^\\\\\\\\section\\|^\\\\\\\\subsection\" /home/<USER>/neuralips26/main.tex | awk -F: '$1>=240 && $1<=400' | head -30",
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
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "old_string": "\\textbf{Problem statement (this paper).} The standard MoE recipe lets the router $G_\\psi$ read the backbone's hidden states $f_\\theta(\\mathbf{x})$. We claim, and this paper establishes, that on instance-normalized TSFMs this choice has a structural failure mode not previously characterized: the router's input is missing, by construction of an upstream architectural normalizer, the per-window statistics that distinguish regimes, so $G_\\psi$ collapses to a single expert and the remaining $K{-}1$ experts receive no gradient. We name this failure \\emph{normalization-induced routing collapse} and state it as the central problem of this work: \\emph{given a frozen instance-normalized TSFM, find the routing input $u(\\mathbf{x})$ such that the per-window mixture $\\sum_j G_\\psi(u(\\mathbf{x}))_j\\,\\mathrm{Expert}_j(f_\\theta(\\mathbf{x}))$ trains without entropy collapse and improves over a single static head.} The collapse is upstream of the optimization-induced collapse that load-balance, z-loss, ReLU-routing, and expert-choice rescues target (Table~\\ref{tab:rescue}); it is not addressed by prior MoE-collapse, MoE-adapter, or time-series-normalization work (\\S\\ref{sec:related_work}). Sections~\\ref{sec:diagnosis} and~\\ref{sec:main_results} answer the problem with $u(\\mathbf{x})\\!=\\!\\mathbf{x}$ (the raw, pre-normalization window) and verify the answer with eight causal controls.",
  "new_string": "\\textbf{Problem statement (this paper).} The standard MoE recipe~\\citep{shazeer2017outrageously, fedus2022switch} lets the router $G_\\psi$ read the backbone's hidden states $f_\\theta(\\mathbf{x})$, and this is the choice […]

> TOOL

tool_result
id: toolu_01AKSw5kcxLbvg1WoPaHj9Fo
```
The file /home/<USER>/neuralips26/main.tex has been updated successfully.
```

> AGENT

Now verify all citations exist in the bibliography and the build is clean.

> TOOL

tool_use Bash
id: toolu_015AzptuRhjQWY1GPsssnJGT
```json
{
  "command": "grep -n \"\\\\\\\\bibitem{shazeer2017outrageously\\\\|\\\\\\\\bibitem{fedus2022switch\\\\|\\\\\\\\bibitem{wang2022adamix\\\\|\\\\\\\\bibitem{kim2021revin\\\\|\\\\\\\\bibitem{goswami2024moment\\\\|\\\\\\\\bibitem{nie2023patchtst\\\\|\\\\\\\\bibitem{das2024timesfm\\\\|\\\\\\\\bibitem{zoph2022stmoe\\\\|\\\\\\\\bibitem{wang2025remoe\\\\|\\\\\\\\bibitem{zhou2022expertchoice\\\\|\\\\\\\\bibitem{wu2024mole\\\\|\\\\\\\\bibitem{chi2022representation\\\\|\\\\\\\\bibitem{wu2024mhmoe\\\\|\\\\\\\\bibitem{puigcerver2024softmoe\\\\|\\\\\\\\bibitem{panda2024densebackprop\\\\|\\\\\\\\bibitem{hua2025inputaware\\\\|\\\\\\\\bibitem{guo2025expertspec\\\\|\\\\\\\\bibitem{liu2022nonstationary\\\\|\\\\\\\\bibitem{fan2023dishts\\\\|\\\\\\\\bibitem{liu2023san\\\\|\\\\\\\\bibitem{ye2024fan\\\\|\\\\\\\\bibitem{dai2024ddn\\\\|\\\\\\\\bibitem{berthelier2026revin\\\\|\\\\\\\\bibitem{zou2025ibnorm\" /home/<USER>/neuralips26/main.tex | wc -l",
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
  "command": "grep -c \"bibitem\" /home/<USER>/neuralips26/main.tex; grep -n \"thebibliography\\|\\\\\\\\bibitem\" /home/<USER>/neuralips26/main.tex | head -5",
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
  "command": "for k in shazeer2017outrageously fedus2022switch wang2022adamix kim2021revin goswami2024moment nie2023patchtst das2024timesfm zoph2022stmoe wang2025remoe zhou2022expertchoice wu2024mole chi2022representation wu2024mhmoe puigcerver2024softmoe panda2024densebackprop hua2025inputaware guo2025expertspec liu2022nonstationary fan2023dishts liu2023san ye2024fan dai2024ddn berthelier2026revin zou2025ibnorm; do\n  if grep -q \"\\\\\\\\bibitem.*{$k}\" /home/<USER>/neuralips26/main.tex; then\n    echo \"OK   $k\"\n  else\n    echo \"MISS $k\"\n  fi\ndone",
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

> DEVELOPER

how logically structured is our entire paper now

> TOOL

tool_use Bash
id: toolu_01WQPDFoWQegb7sQ195TZqUg
```json
{
  "command": "grep -n \"^\\\\\\\\section\\|^\\\\\\\\subsection\\|^\\\\\\\\textbf{\" /home/<USER>/neuralips26/main.tex | awk -F: '$1<=560' | sed 's/{Given.*//; s/{We.*//; s/{The.*//; s/{Beyond.*//; s/{Sparsely.*//; s/{Existing.*//; s/{Instance.*//; s/{Trained.*//; s/{Per-window.*//; s/{Standard.*//; s/{Real.*//; s/{This natural.*//; s/{The failure.*//; s/{Because.*//; s/{The diagnosis.*//; s/{Time series.*//'",
  "description": "Map main-body skeleton"
}
```

> TOOL

tool_result
id: toolu_01WQPDFoWQegb7sQ195TZqUg
```
61:\section{Introduction}
228:\section{Related Work}
233:\textbf{TSFM Adaptation.} Beyond the broad survey of~\citet{wen2023tssurvey}, a complementary line shows that compact task-specific models match or beat heavyweight pretrained backbones on LTSF benchmarks~\citep{wu2025srsnet, wang2025timemixerpp, xu2024fits, chen2023tsmixer, fu2025selective}: that lightweight raw-input models are competitive is itself evidence that the per-window raw signal carries most of the predictability our diagnostic $R(\mathcal{D})$ exploits (\S\ref{sec:diagnosis}). LLM-reprogrammed forecasters~\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes} inherit per-window normalization upstream of the backbone, so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is attached. We focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a lightweight module to a frozen TSFM~\citep{hu2022lora, houlsby2019adapters, goswami2024moment}; recent variations explore multi-scale finetuning~\citep{qiao2025msft}, importance-based LoRA selection~\citep{li2025trace}, input-representation adaptation~\citep{benechehab2025adapts}, structured pruning~\citep{zhao2025prune}, in-context tuning~\citep{faw2025icf}, retrieval-augmented adaptation~\citep{ning2025tsrag}, and Chronos-specific PEFT~\citep{gupta2024beyondlora}; complementary work computes transferability scores for backbone selection (TEMPLATE, \citealp{zhang2025template}) or provides a unified evaluation suite (GIFT-Eval, \citealp{woo2024gifteval}). These vary the finetuning \textit{strategy} while leaving per-input adapter \textit{topology} fixed; AdaPTS reports the best of several variants per dataset/horizon, treating adapter choice as a per-task hyperparameter rather than per-window routing. We instead route over heterogeneous expert topologies per window; the closest precedent in spirit is mixture-of-adapters in the LLM setting (AdaMix~\citep{wang2022adamix} mixes copies of one […]

> TOOL

tool_use Read
id: toolu_01GdX34oVymCrpLWNewBMcVA
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 498,
  "limit": 10
}
```

> TOOL

tool_result
id: toolu_01GdX34oVymCrpLWNewBMcVA
```
498	\end{proposition}
499	
500	{\looseness=-1 \textit{Remark.} Proposition~\ref{prop:frozen} covers linear $A\mathbf{x}$; Figure~\ref{fig:trajectory}b confirms it in the full 8-block Transformer within ${\sim}50$ steps. Independent ensembles are $37$--$46\%$ worse (Table~\ref{tab:baselines}), so learned routing -- not mere diversity -- drives the gains, which raises the question of \emph{what} the router needs to read.}
501	
502	\subsubsection*{Mechanism: instance normalization strips the routing signal}
503	\label{sec:diagnosis}
504	
505	We answer that question by tracing the routing signal through the encoder pipeline. The empirical pattern (RR-MoA wins, AdaMix collapses, frozen $\succeq$ unfrozen) has a single causal explanation if RevIN removes precisely the per-window statistics a hidden-state router would need; we now formalize that loss.
506	
507	\textbf{Why RevIN destroys routing.} Each window decomposes into mean $M_i$, scale $\Sigma_i$, shape $\mathbf{S}_i = (\mathbf{x}_i - M_i)/\Sigma_i$; RevIN keeps $\mathbf{S}_i$ and discards $(M_i,\Sigma_i)$. The chain rule quantifies the routing signal in the discarded part.
```

> TOOL

tool_use Bash
id: toolu_01BTaSFa5gARCDFWunBmqiWE
```json
{
  "command": "grep -n \"^\\\\\\\\section\\|^\\\\\\\\subsection\\|^\\\\\\\\subsubsection\\|^\\\\\\\\paragraph\" /home/<USER>/neuralips26/main.tex | awk -F: '$1>=415 && $1<=566'",
  "description": "Map experiments substructure"
}
```

> TOOL

tool_result
id: toolu_01BTaSFa5gARCDFWunBmqiWE
```
415:\subsection{Main Results}
420:\subsubsection*{Diagnosis: adapters underperform, MoE collapses}
502:\subsubsection*{Mechanism: instance normalization strips the routing signal}
518:\subsubsection*{Standard rescues fail; the raw-input principle generalizes}
526:\subsubsection*{Headline numbers}
```

> TOOL

tool_use Read
id: toolu_01TjitheiuWAbaJECWYso8cZ
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 560,
  "limit": 35
}
```

> TOOL

tool_result
id: toolu_01TjitheiuWAbaJECWYso8cZ
```
560	\textbf{Closing the DLinear gap.} DLinear (49K params, from scratch) outperforms frozen adapters in absolute MSE (Table~\ref{tab:baselines}, grey rows); k-NN/Ridge diagnostics attribute this to information loss in the normalization--encoding pipeline (Appendix~\ref{app:diagnostic}). The same raw-input principle that fixes routing closes the expert-level gap: \textbf{Residual-IA\textsuperscript{+}} matches or beats DLinear on $6/6$ datasets at $H{=}96$ and $107/123$ cells across six backbones (App.~\ref{app:gate_pathology}); SR-RIA\textsuperscript{+} hits $6/6$ (App.~\ref{app:sr_ria}); a TSFM-free Pure Raw-MLP MoE localizes the TSFM contribution (App.~\ref{app:raw_mlp_moe}).
561	
562	{\looseness=-1 \textbf{Cross-backbone, task, horizon.}\label{sec:cross_backbone}\label{sec:topk} The diagnosis must also transfer beyond the seven-baseline grid. RR-MoA wins on every instance-normalized backbone tested (MOMENT-small/large $26$--$79\%/32$--$75\%$, Moirai $12$--$29\%$, Moirai-MoE~\citep{liu2025moiraimoe} $37$--$90\%$), and LayerNorm-only Chronos and Timer-XL~\citep{liu2025timerxl} show no collapse — the predicted negative-control split. Beyond forecasting at $H{=}96$, RR-MoA wins $7/8$ imputation cells (App.~\ref{app:imputation}) and $24/24$ multi-horizon cells across $H{\in}\{96,192,336,720\}$ (Tables~\ref{tab:cross_backbone}--\ref{tab:horizon}); Residual-IA\textsuperscript{+} additionally generalizes across the $6{\times}5{\times}4$ dataset $\times$ backbone $\times$ horizon grid (App.~\ref{app:gate_pathology}). Together these confirm the diagnosis is task-, horizon-, and backbone-portable rather than tied to the specific MOMENT$+$RevIN combination on which it was first observed.}
563	
564	{\looseness=-1 \textbf{When RR-MoA does not help.} The diagnostic should also predict where the method fails, and the results respect that boundary: on Traffic ($R{=}0.14$, lowest in […]

> AGENT

## Honest assessment of the logical structure

**Overall:** the paper has a strong, falsifiable spine — Problem → Mechanism → Fix → Verification — and the chain closes end-to-end. There are three structural frictions worth addressing.

### What works (the chain you've built)

| Link | Where | Evidence |
|---|---|---|
| ① Failure exists | §1 ¶3, Fig 1, Tab adamix | entropy 0 on AdaMix+RevIN |
| ② Distinct from optimization-induced | §1 ¶4, Tab rescue | 720-run sweep, ≤10.9%, 2.7× worse |
| ③ Caused by normalization | §4 Mechanism + 8 causal controls | RevIN swaps, vision, $R(\mathcal{D})$ |
| ④ Formal mechanism | Observation 1, MI decomposition, $\rho{=}{-}0.88$ | quantitative |
| ⑤ Minimal fix works | §3 Architecture + §4 headline | 54/54 RR-MoA wins |
| ⑥ Generalizes | §4 cross-backbone/horizon/imputation | 5 backbones, 24/24 horizons |
| ⑦ Falsifiable | §4 "When RR-MoA does not help" | Traffic ($R{=}0.14$), LayerNorm-only no collapse |

Every link has at least one experiment behind it, and the predictor $R(\mathcal{D})$ commits to a *prior* go/no-go test that the empirical results respect (Traffic correctly negative). Three converging interventions (RR-MoA / SR-MoA / Residual-IA⁺) from one principle is […]

> DEVELOPER

plan that out

> TOOL

tool_use Read
id: toolu_01Pooqwkhp7PumthjpHM77Qw
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 498,
  "limit": 62
}
```

> TOOL

tool_result
id: toolu_01Pooqwkhp7PumthjpHM77Qw
```
498	\end{proposition}
499	
500	{\looseness=-1 \textit{Remark.} Proposition~\ref{prop:frozen} covers linear $A\mathbf{x}$; Figure~\ref{fig:trajectory}b confirms it in the full 8-block Transformer within ${\sim}50$ steps. Independent ensembles are $37$--$46\%$ worse (Table~\ref{tab:baselines}), so learned routing -- not mere diversity -- drives the gains, which raises the question of \emph{what} the router needs to read.}
501	
502	\subsubsection*{Mechanism: instance normalization strips the routing signal}
503	\label{sec:diagnosis}
504	
505	We answer that question by tracing the routing signal through the encoder pipeline. The empirical pattern (RR-MoA wins, AdaMix collapses, frozen $\succeq$ unfrozen) has a single causal explanation if RevIN removes precisely the per-window statistics a hidden-state router would need; we now formalize that loss.
506	
507	\textbf{Why RevIN destroys routing.} Each window decomposes into mean $M_i$, scale $\Sigma_i$, shape $\mathbf{S}_i = (\mathbf{x}_i - M_i)/\Sigma_i$; RevIN keeps $\mathbf{S}_i$ and discards $(M_i,\Sigma_i)$. The chain rule quantifies the routing signal in the discarded part.
508	
509	\begin{observation}[Routing Information Loss Under Instance Normalization]
510	\label{thm:mi_decomp}
511	Let $X$ be a random input window, $E \in \{1,\ldots,K\}$ the expert assignment produced by any deterministic router, $S = (X - M)/\Sigma$ the RevIN-normalized shape. \emph{(i) Exact decomposition:} $I(X;E) - I(S;E) = I(M,\Sigma;E\mid S) \geq 0$. \emph{(ii) Quantitative bound (no […]

> TOOL

tool_use Read
id: toolu_01BHrM3k4R7h6tsiuSLoNAD5
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 377,
  "limit": 22
}
```

> TOOL

tool_result
id: toolu_01BHrM3k4R7h6tsiuSLoNAD5
```
377	\label{fig:framework}
378	\vspace{-0.8em}
379	\end{figure}
380	
381	\label{sec:rrmoa}
382	
383	\textbf{Architecture.} Per-window routing should dispatch a quiet baseline and a volatile spike to different expert topologies, but doing so requires the router to see the per-window statistics that distinguish regimes -- exactly what RevIN strips. RR-MoA splits the two needs into two streams: the frozen TSFM produces embeddings $\mathbf{H}{=}f_\theta(\mathbf{x})$ for the experts, while a lightweight gate reads the \textit{raw, pre-normalization} input $\mathbf{X}_\text{raw}$ to select which experts to activate:
384	\begin{equation}
385	\begin{aligned}
386	\mathbf{Y} &= \sum_{j=1}^{K} \widetilde{w}_j \cdot \text{Expert}_j(\mathbf{H}_\text{FM}), \qquad
387	\mathcal{T} = \mathrm{TopK}\!\bigl(G_\psi(\mathbf{X}_\text{raw}),\, k\bigr), \\
388	\widetilde{w}_j &= \begin{cases}
389	\dfrac{\exp\!\bigl(G_\psi(\mathbf{X}_\text{raw})_j\bigr)}{\sum_{j'\in\mathcal{T}}\exp\!\bigl(G_\psi(\mathbf{X}_\text{raw})_{j'}\bigr)}, & j\in\mathcal{T},\\[4pt]
390	0, & j\notin\mathcal{T}.
391	\end{cases}
392	\end{aligned}
393	\label{eq:rrmoa}
394	\end{equation}
395	where $G_\psi: \mathbb{R}^{T} \to \mathbb{R}^K$ is a small Conv1d\,+\,pooling\,+\,linear gate ($853$ params) operating directly on the raw time series, $\mathcal{T} \subset \{1,\ldots,K\}$ is the set of Top-$k$ indices, and each $\mathrm{Expert}_j$ is a canonical adapter head. By construction $\sum_j \widetilde{w}_j = 1$ with support only on $\mathcal{T}$, so only $k$ of $K$ experts execute per sample. With $K{=}5$, $k{=}2$ we obtain $40\%$ of the dense expert FLOPs while retaining $63\%$ of the dense MSE improvement over the best […]

> TOOL

tool_use Read
id: toolu_01B8gHS6JvaDGjmAnm1ie3tt
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 418,
  "limit": 85
}
```

> TOOL

tool_result
id: toolu_01B8gHS6JvaDGjmAnm1ie3tt
```
418	With this setup fixed, we now turn to the empirical case for RR-MoA, which rests on three claims and the mechanism that explains them: fixed-topology adapters are suboptimal, the natural MoE remedy collapses on instance-normalized backbones, and standard rescue mechanisms cannot recover it. We establish each in turn before comparing against the seven-baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full fine-tuning, DLinear).
419	
420	\subsubsection*{Diagnosis: adapters underperform, MoE collapses}
421	
422	{\looseness=-1 \textbf{RR-MoA vs.\ fixed adapters.} Table~\ref{tab:rrmoa} compares Top-2 RR-MoA against the best fixed adapter, using the \emph{same five expert heads} in all rows. Across the primary 6-dataset LTSF grid $\times$ 3 freeze levels $\times$ 3 seeds $=$ \textbf{54 configurations}, RR-MoA wins all 54 with tight standard deviations.}
423	
424	\begin{table}[!htbp]
425	\centering
426	\caption{\textbf{Freeze-level ablation} (test MSE, mean$\pm$std, 3 seeds $\{42,43,44\}$, H=96). RR-MoA (sparse Top-2 routing over 5 experts) vs.\ the best single-head adapter from $\{$linear, attention, conv$\}$ trained with the same protocol. ``MSE $\Delta\%$ vs.\ single-head'' is the relative MSE change of RR-MoA over the single-head baseline; negative $=$ lower MSE $=$ better. RR-MoA wins \textbf{27/27} paired (cell, seed) comparisons in this table; combined with Appendix~\ref{app:extended_rrmoa} the score is \textbf{54/54} across […]

> AGENT

## Plan: move Observation 1 + R(D) formalization into §3

### Goal
Make §3 (Method) self-contained by promoting the formal mechanism out of §4.2, so a reader sees the failure mode named (Problem statement) → formalized (Observation 1, $R(\mathcal{D})$) → answered (RR-MoA architecture) within one section. §4 becomes purely empirical verification.

### Target §3 structure (after move)

| # | Block | Status | Content |
|---|---|---|---|
| 1 | Bridge sentence | edit | Add "and its formal mechanism" |
| 2 | **Task setup** | unchanged | Notation, $f_\theta$, $g_\phi$, MoA formalism |
| 3 | **Problem statement** | unchanged | Names failure, formal problem in `quote`, citations |
| 4 | **Mechanism (formal)** | **NEW** | $M,\Sigma,S$ decomposition, Observation 1, $R(\mathcal{D})$ definition |
| 5 | Figure 2 (RR-MoA arch) | unchanged | Architecture diagram |
| 6 | **Architecture** | unchanged | Eq. \ref{eq:rrmoa}, Conv1d gate, Top-$k$ |
| 7 | "Why the router behaves" | **DELETE** | Currently pulls §4 numbers forward; redundant once Obs 1 is in §3 |
| 8 | Cost, expert pool, deployment | unchanged | Pool diversity, hot-swap |

### Source content to move (from §4.2, lines 502–516)

| Line […]