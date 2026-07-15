> DEVELOPER

related work currently ends at line 148. Ideally it should end at 100, save the rest for the subsequent sections. Plan cuts but maintain cohesive discussions and omit no in-text citations

> TOOL

tool_use Bash
id: toolu_01TP419GcbMiR5CWCDpPyTEW
```json
{
  "command": "find /Users/hungpq2412/neuralips26 -name \"main.tex\" -not -path \"*/node_modules/*\" 2>/dev/null | head -5",
  "description": "Find main.tex file"
}
```

> TOOL

tool_result
id: toolu_01TP419GcbMiR5CWCDpPyTEW
```
/Users/hungpq2412/neuralips26/main.tex
```

> TOOL

tool_use Bash
id: toolu_014ebuPZLZWzxEWKV3kHgjV1
```json
{
  "command": "grep -n \"section\\|Related Work\\|RelatedWork\" /Users/hungpq2412/neuralips26/main.tex | head -30",
  "description": "Find section markers in main.tex"
}
```

> TOOL

tool_result
id: toolu_014ebuPZLZWzxEWKV3kHgjV1
```
61:\section{Introduction}
228:\section{Related Work}
241:\section{Raw-Routed Mixture of Adapters (RR-MoA)}
244:We first state the task setup, then the problem we identify and its formal mechanism, then specify RR-MoA: a per-window mixture in which the router reads the raw, pre-normalization signal while the experts consume the frozen TSFM's hidden states. Cost, expert pool, and deployment implications close the section.
252:This collapse is upstream of the optimization-induced collapse that existing rescues target -- load balancing~\citep{shazeer2017outrageously, fedus2022switch}, z-loss~\citep{zoph2022stmoe}, ReLU routing~\citep{wang2025remoe}, and expert-choice~\citep{zhou2022expertchoice} -- and is not addressed by prior MoE-adapter~\citep{wang2022adamix, wu2024mole}, MoE routing-collapse~\citep{chi2022representation, wu2024mhmoe, puigcerver2024softmoe, panda2024densebackprop, hua2025inputaware, guo2025expertspec}, or time-series-normalization~\citep{liu2022nonstationary, fan2023dishts, liu2023san, ye2024fan, dai2024ddn, berthelier2026revin, zou2025ibnorm} work (positioned in detail in \S\ref{sec:related_work}). We next formalize the loss (Observation~\ref{thm:mi_decomp}) and define a training-free predictor $R(\mathcal{D})$ for it; the rest of the section then specifies RR-MoA, the answer to the problem with $u(\mathbf{x})\!=\!\mathbf{x}$, and \S\ref{sec:main_results} verifies the answer with eight causal controls and a $720$-run rescue sweep (Table~\ref{tab:rescue}).
411:\section{Experiments}
413:\subsection{Setup}
423:\subsection{Main Results}
428:\subsubsection*{Fixed adapters underperform; standard MoE collapses}
510:\subsubsection*{$R(\mathcal{D})$ makes three predictions, and all three hold}
518:\subsubsection*{Optimization-side rescues fail; raw-input fixes transfer}
526:\subsubsection*{RR-MoA leads the seven-baseline suite}
563:\section{Conclusion and Limitations}
1043:\renewcommand{\thetable}{\Alph{section}.\arabic{table}}
1044:\renewcommand{\thefigure}{\Alph{section}.\arabic{figure}}
1046:\@addtoreset{table}{section}
1047:\@addtoreset{figure}{section}
1054:\section{Experimental Setup Details}
1131:\section{Deployment-Regime Motivation}
1142:\subsection{Inference Benchmark}
1173:\section{Multi-Horizon Evaluation} […]

> TOOL

tool_use Read
id: toolu_01QC1AzyexijCMjZDxNYLDVj
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 228,
  "limit": 15
}
```

> TOOL

tool_result
id: toolu_01QC1AzyexijCMjZDxNYLDVj
```
228	\section{Related Work}
229	\label{sec:related_work}
230	
231	We position RR-MoA against four threads: TSFM adaptation, MoE in foundation models, MoE routing collapse and rescue, and time-series normalization.
232	
233	\textbf{TSFM Adaptation.} Beyond the broad survey of~\citet{wen2023tssurvey}, a complementary line shows that compact task-specific models match or beat heavyweight pretrained backbones on LTSF benchmarks~\citep{wu2025srsnet, wang2025timemixerpp, xu2024fits, chen2023tsmixer, fu2025selective}: that lightweight raw-input models are competitive is itself evidence that the per-window raw signal carries most of the predictability our diagnostic $R(\mathcal{D})$ exploits (\S\ref{sec:diagnosis}). LLM-reprogrammed forecasters~\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes} inherit per-window normalization upstream of the backbone, so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is attached. We focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a lightweight module to a frozen TSFM~\citep{hu2022lora, houlsby2019adapters, goswami2024moment}; recent variations explore multi-scale finetuning~\citep{qiao2025msft}, importance-based LoRA selection~\citep{li2025trace}, input-representation adaptation~\citep{benechehab2025adapts}, structured pruning~\citep{zhao2025prune}, in-context tuning~\citep{faw2025icf}, retrieval-augmented adaptation~\citep{ning2025tsrag}, and Chronos-specific PEFT~\citep{gupta2024beyondlora}; complementary work computes transferability scores for backbone selection (TEMPLATE, \citealp{zhang2025template}) or provides a unified evaluation suite (GIFT-Eval, \citealp{woo2024gifteval}). These vary the finetuning \textit{strategy} while leaving per-input adapter \textit{topology} fixed; AdaPTS reports the best of several variants per dataset/horizon, treating adapter choice as a per-task hyperparameter rather than per-window […]

> TOOL

tool_use Bash
id: toolu_014L6uHVXfhUP4CeXju8GVzJ
```json
{
  "command": "grep -n \"linenumber\\|lineno\\|nolinenumbers\" /Users/hungpq2412/neuralips26/main.tex | head -10",
  "description": "Check if line numbering is active"
}
```

> TOOL

tool_result
id: toolu_014L6uHVXfhUP4CeXju8GVzJ
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01G8cT7Ra9aCmVeDC9Rrm9TX
```json
{
  "command": "grep -n \"lineno\\|linenum\\|\\\\\\\\linenumber\\|\\\\\\\\modulolinenumbers\" /Users/hungpq2412/neuralips26/*.sty 2>/dev/null | head -10; ls /Users/hungpq2412/neuralips26/*.sty 2>/dev/null",
  "description": "Check style files for line numbering"
}
```

> TOOL

tool_result
id: toolu_01G8cT7Ra9aCmVeDC9Rrm9TX
```
6:%   lineno package
405:    \RequirePackage{lineno}
406:    \linenumbers
408:    % fix incompatibilities between lineno and amsmath, if required, by
409:    % transparently wrapping linenomath environments around amsmath
417:                          {\linenomath\csname old#1\endcsname}%
418:                          {\csname oldend#1\endcsname\endlinenomath}%
/Users/hungpq2412/neuralips26/neurips_2026.sty
```

> TOOL

tool_use Bash
id: toolu_0181SFZyGEdG8qZGW5JRv3fr
```json
{
  "command": "ls -la /Users/hungpq2412/neuralips26/main.pdf 2>/dev/null; find /Users/hungpq2412/neuralips26 -maxdepth 2 -name \"main.pdf\" 2>/dev/null",
  "description": "Check for compiled PDF"
}
```

> TOOL

tool_result
id: toolu_0181SFZyGEdG8qZGW5JRv3fr
```
-rw-r--r--@ 1 hungpq2412  staff  910547 May  6 15:10 /Users/hungpq2412/neuralips26/main.pdf
/Users/hungpq2412/neuralips26/main.pdf
```

> TOOL

tool_use Bash
id: toolu_01APueHUFYWBg9ynLsA3ustV
```json
{
  "command": "pdftotext -layout -f 4 -l 5 main.pdf - 2>/dev/null | head -200",
  "description": "Extract text with layout from pages 4-5"
}
```

> TOOL

tool_result
id: toolu_01APueHUFYWBg9ynLsA3ustV
```
134   Concurrent work eliminates the external router (AoE [42], Routing-Free MoE [44]) or replaces
135   softmax+load-balance with eigenbasis routing (ERMoE [43]); in our setting (§4.2), self-gated experts
136   on raw input match RR-MoA, while the same architecture on hidden states collapses. Wang et al. [49]
137   argues MoE specialization reflects hidden-state geometry; we extend this upstream by identifying
138   what shapes that geometry on TSFMs.
139   Normalization in Time Series. Instance normalization originated in style transfer [92]; RevIN [21]
140   adapts it to forecasting distribution shift; DishTS [33], SAN [93], and Non-stationary Transform-
141   ers [35] partially recover stripped statistics; FAN [34] extends beyond (µ, σ) to Fourier components;
142   DDN [65] normalizes jointly in time and frequency. Berthelier et al. [48] concurrently show sev-
143   eral RevIN components are redundant, and Zou et al. [50] argue variance-centric normalization is
144   suboptimal because identical-(µ, σ) representations can encode different task-relevant content. We
145   identify a specific MoE consequence not characterized in prior literature: when stripped statistics
146   carry the routing signal in a downstream MoE adapter, instance normalization collapses the router to
147   a single expert under unfreezing, distinct from the optimization-induced collapse standard rescues
148 […]

> TOOL

tool_use Bash
id: toolu_01JnCU9SkqgSf1Jszn7DntpP
```json
{
  "command": "pdftotext -layout -f 3 -l 4 /Users/hungpq2412/neuralips26/main.pdf - 2>/dev/null | sed -n '1,200p'",
  "description": "Get pages 3-4 with line numbers"
}
```

> TOOL

tool_result
id: toolu_01JnCU9SkqgSf1Jszn7DntpP
```
                                  (a)                                                  TSFM adapters use the same head for every window
                                                                                     FROZEN
                                                                                                                 H1
                                                                           Frozen TSFM Backbone                                Single static
                                                                             (MOMENT, Moirai)
                                                                                                                 H2
                                                                                                                               adapter head             ŷ
                                                                                                                 H3
                                                                           Instance Normalization (RevIN)
                             Input windows X (distinct per-window stats)

                                  (b)                             A natural MoE adapter collapses to a single expert on instance-normalized TSFMs
                                                                                     FROZEN
                                                                                                                                       E1
                                                                                                            H1                         E2      unused
                                                                           Frozen TSFM Backbone
                                                                             (MOMENT, Moirai)
                                                                                                            H2        Router           E3      unused
                                                                                                                                                             ŷ
                                                                                                            H3
                                                                           Instance Normalization (RevIN)                              E4      unused
                                         Input windows X                                                                               E5      unused




      Figure 1: Problem overview. (a) TSFM adapters use the same head for every window. (b) The
      natural mixture-of-experts extension fails on instance-normalized TSFMs under unfreezing: entropy
      collapses (0.000±0.000) and the remaining experts receive no gradient. Same backbone, different
      heads.

88    TSFM Adaptation. Beyond the broad survey of Wen et al. [40], a complementary line shows that
89    compact task-specific models match or beat heavyweight pretrained backbones on LTSF bench-
90    marks [62, 63, 69, 76, 77]: that lightweight raw-input models are competitive is itself evidence
91    that the per-window raw signal carries most of the predictability our diagnostic R(D) exploits (§3).
92    LLM-reprogrammed forecasters [70–72] inherit per-window normalization upstream of the backbone,
93    so the routing-collapse mechanism we identify applies whenever a downstream MoE […]

> TOOL

tool_use Bash
id: toolu_01E9D5bx5kgZ4Y7MXukSV5mt
```json
{
  "command": "pdftotext -layout -f 2 -l 3 /Users/hungpq2412/neuralips26/main.pdf - 2>/dev/null | sed -n '80,200p'",
  "description": "Find Related Work section header in PDF"
}
```

> TOOL

tool_result
id: toolu_01E9D5bx5kgZ4Y7MXukSV5mt
```
                                         Input windows X                                                                               E5      unused




      Figure 1: Problem overview. (a) TSFM adapters use the same head for every window. (b) The
      natural mixture-of-experts extension fails on instance-normalized TSFMs under unfreezing: entropy
      collapses (0.000±0.000) and the remaining experts receive no gradient. Same backbone, different
      heads.

88    TSFM Adaptation. Beyond the broad survey of Wen et al. [40], a complementary line shows that
89    compact task-specific models match or beat heavyweight pretrained backbones on LTSF bench-
90    marks [62, 63, 69, 76, 77]: that lightweight raw-input models are competitive is itself evidence
91    that the per-window raw signal carries most of the predictability our diagnostic R(D) exploits (§3).
92    LLM-reprogrammed forecasters [70–72] inherit per-window normalization upstream of the backbone,
93    so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is
94    attached. We focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a
95    lightweight module to a frozen TSFM [2, 15, 16]; recent variations explore multi-scale finetuning [24],
96    importance-based LoRA selection [25], input-representation adaptation [27], structured pruning [28],
97    in-context tuning [29], retrieval-augmented adaptation [59], and Chronos-specific PEFT [26]; comple-
98    mentary work computes transferability scores for backbone selection […]

> AGENT

Let me see the Method section to understand where citations might already be referenced.

> TOOL

tool_use Read
id: toolu_016tDJaAspGMJVYjDFW3HkCJ
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 241,
  "limit": 150
}
```

> TOOL

tool_result
id: toolu_016tDJaAspGMJVYjDFW3HkCJ
```
241	\section{Raw-Routed Mixture of Adapters (RR-MoA)}
242	\label{sec:method}
243	
244	We first state the task setup, then the problem we identify and its formal mechanism, then specify RR-MoA: a per-window mixture in which the router reads the raw, pre-normalization signal while the experts consume the frozen TSFM's hidden states. Cost, expert pool, and deployment implications close the section.
245	
246	\textbf{Task setup.} Given a window $\mathbf{x}\in\mathbb{R}^{T\times c}$ ($T{=}512$, $c$ channels), forecasting predicts $\mathbf{y}\in\mathbb{R}^{h\times c}$ at horizons $h\in\{96,192,336,720\}$ under MSE loss (imputation uses the same formalism with $\mathbf{y}$ as the reconstruction target). A pretrained TSFM acts as a feature extractor $f_\theta:\mathbb{R}^{T\times c}\to\mathbb{R}^{P\times d}$ ($P$ patches of dim $d$) with $\theta$ \emph{frozen} ($\nabla_\theta\!\equiv\!0$); we train only an adapter $g_\phi:\mathbb{R}^{P\times d}\to\mathbb{R}^{h\times c}$ with a small parameter budget ($|\phi|\leq 500$K), so that many task-specific adapters can be hot-swapped onto a single shared backbone (App.~\ref{app:deployment}). A \emph{per-window mixture of adapters} replaces $g_\phi$ with $K$ experts $\{\mathrm{Expert}_j\}_{j=1}^K$ plus a router $G_\psi$ that returns a sparse weight $\widetilde{w}\in\Delta^{K-1}$ supported on a Top-$k$ subset ($k\leq K$), giving $\hat{\mathbf{y}}=\sum_{j} \widetilde{w}_j\,\mathrm{Expert}_j(f_\theta(\mathbf{x}))$ trained by $\min_{\phi,\psi}\,\mathbb{E}\,\|\hat{\mathbf{y}}-\mathbf{y}\|_2^2$.
247	
248	\textbf{Problem statement.} The standard MoE recipe~\citep{shazeer2017outrageously, fedus2022switch} lets the router $G_\psi$ read the backbone's hidden states $f_\theta(\mathbf{x})$, and this is […]

> AGENT

I'll plan this without TaskCreate since it's a focused analysis task. Let me check the Experiments section to identify natural homes for moved citations.

> TOOL

tool_use Read
id: toolu_01DMSLKujjH6S1XQVQpMM6nn
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 411,
  "limit": 160
}
```

> TOOL

tool_result
id: toolu_01DMSLKujjH6S1XQVQpMM6nn
```
411	\section{Experiments}
412	
413	\subsection{Setup}
414	
415	\textbf{Datasets and tasks.} Six LTSF benchmarks (ETTh1/h2/m1/m2~\citep{zhou2021informer}, Weather, Electricity~\citep{wu2021autoformer}) spanning hourly to 15-minute sampling and $7$--$321$ channels, with chronological splits and channel-wise normalization~\citep{nie2023patchtst}. We evaluate forecasting at $H{=}96$ primary (multi-horizon in Appendix~\ref{app:horizon}) and $20\%$-masked imputation.
416	
417	\textbf{Backbones.} Five backbones spanning three normalization regimes: (i)~learnable-affine RevIN-inside-encoder MOMENT-small/large~\citep{goswami2024moment} (internal RevIN~\citep{kim2021revin}); (ii)~Moirai~\citep{woo2024moirai} and Moirai-MoE, which use RMSNorm internally with only non-learnable per-instance I/O scaling (no learnable-affine RevIN inside the encoder pipeline); (iii)~Chronos~\citep{ansari2024chronos} (T5-style, no instance normalization) and Timer-XL~\citep{liu2025timerxl} (LayerNorm only, no instance normalization) as no-instance-normalization negative controls (per-backbone normalization specifications in Appendix~\ref{app:setup}, \S\ref{sec:cross_backbone}). The collapse mechanism predicts that only regime~(i) is vulnerable: routing signal is destroyed by RevIN's learnable-affine normalization upstream of the encoder, whereas non-learnable I/O scaling preserves the (M,$\Sigma$) statistics in the hidden states the router reads. MOMENT-small is primary. Primary results use a strictly frozen backbone; freeze-level ablations follow.
418	
419	\textbf{Baselines.} Four tiers, kept separate to avoid confounding frozen-vs-unfrozen and adapter-vs-from-scratch comparisons: \emph{frozen-adapter} (three fixed adapters; $5$-expert independent ensemble; AdaMix~\citep{wang2022adamix}); \emph{frozen PEFT} (LoRA~\citep{hu2022lora}, $108$-run sweep, App.~\ref{app:lora_sweep}; TRACE~\citep{li2025trace}); \emph{unfrozen} (full fine-tuning, all blocks, best of $5$ heads $\times 2$ LRs; extended schedules in App.~\ref{app:extended_ft}); \emph{from-scratch calibration} (DLinear~\citep{zeng2023dlinear}).
420 […]

> AGENT

Let me verify which citations in Related Work are duplicated vs. unique, since duplicates can be cut without preservation work.

> TOOL

tool_use Bash
id: toolu_01DKAwL7iVkc4j68JYHsP58b
```json
{
  "command": "for cit in wen2023tssurvey wu2025srsnet wang2025timemixerpp xu2024fits chen2023tsmixer fu2025selective jin2024timellm zhou2023onefitsall liu2024autotimes hu2022lora houlsby2019adapters goswami2024moment qiao2025msft li2025trace benechehab2025adapts zhao2025prune faw2025icf ning2025tsrag gupta2024beyondlora zhang2025template woo2024gifteval wang2022adamix shazeer2017outrageously lepikhin2021gshard fedus2022switch riquelme2021vmoe komatsuzaki2023sparseupcycling raposo2024mod jiang2024mixtral zhu2024llamamoe dai2024deepseekmoe cai2024moesurvey liu2025moiraimoe shi2024timemoe he2025sempo wu2024mole ma2018mmoe zoph2022stmoe guo2025expertspec chi2022representation wu2024mhmoe zhou2022expertchoice puigcerver2024softmoe wang2025remoe panda2024densebackprop hua2025inputaware lv2025aoe liu2026routingfree cheng2025ermoe wang2026myth ulyanov2016instancenorm kim2021revin fan2023dishts liu2023san liu2022nonstationary ye2024fan dai2024ddn berthelier2026revin zou2025ibnorm; do count=$(grep -c \"$cit\" main.tex); printf \"%-32s %s\\n\" \"$cit\" \"$count\"; done | sort -k2 -n",
  "description": "Count occurrences of each related-work citation in main.tex"
}
```

> TOOL

tool_result
id: toolu_01DKAwL7iVkc4j68JYHsP58b
```
benechehab2025adapts             2
cai2024moesurvey                 2
chen2023tsmixer                  2
dai2024deepseekmoe               2
faw2025icf                       2
fu2025selective                  2
gupta2024beyondlora              2
he2025sempo                      2
houlsby2019adapters              2
jiang2024mixtral                 2
komatsuzaki2023sparseupcycling   2
lepikhin2021gshard               2
ma2018mmoe                       2
ning2025tsrag                    2
qiao2025msft                     2
raposo2024mod                    2
riquelme2021vmoe                 2
ulyanov2016instancenorm          2
wang2025timemixerpp              2
wang2026myth                     2
wen2023tssurvey                  2
woo2024gifteval                  2
wu2025srsnet                     2
xu2024fits                       2
zhang2025template                2
zhao2025prune                    2
zhu2024llamamoe                  2
berthelier2026revin              3
cheng2025ermoe                   3
chi2022representation            3
dai2024ddn                       3
guo2025expertspec                3
hua2025inputaware                3
jin2024timellm                   3
liu2023san                       3
liu2024autotimes                 3
liu2026routingfree               3
lv2025aoe                        3
panda2024densebackprop           3
puigcerver2024softmoe            3
shi2024timemoe                   3
wu2024mhmoe                      3
wu2024mole                       3
zhou2023onefitsall               3
zou2025ibnorm                    3
fan2023dishts                    4
li2025trace                      4
liu2022nonstationary             4
liu2025moiraimoe                 4
shazeer2017outrageously          4
ye2024fan                        4
hu2022lora                       5
kim2021revin                     5
wang2025remoe                    5
zhou2022expertchoice             5
zoph2022stmoe                    5
goswami2024moment                7
fedus2022switch                  9
wang2022adamix                   10
```

> TOOL

tool_use Bash
id: toolu_01NEjarBFrPk1wCmA7AB2vqS
```json
{
  "command": "grep -n \"wen2023tssurvey\" main.tex; echo \"---\"; grep -n \"wu2025srsnet\" main.tex; echo \"---\"; grep -n \"ma2018mmoe\" main.tex; echo \"---\"; grep -n \"fedus2022switch\" main.tex",
  "description": "Verify citation locations"
}
```

> TOOL

tool_result
id: toolu_01NEjarBFrPk1wCmA7AB2vqS
```
233:\textbf{TSFM Adaptation.} Beyond the broad survey of~\citet{wen2023tssurvey}, a complementary line shows that compact task-specific models match or beat heavyweight pretrained backbones on LTSF benchmarks~\citep{wu2025srsnet, wang2025timemixerpp, xu2024fits, chen2023tsmixer, fu2025selective}: that lightweight raw-input models are competitive is itself evidence that the per-window raw signal carries most of the predictability our diagnostic $R(\mathcal{D})$ exploits (\S\ref{sec:diagnosis}). LLM-reprogrammed forecasters~\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes} inherit per-window normalization upstream of the backbone, so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is attached. We focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a lightweight module to a frozen TSFM~\citep{hu2022lora, houlsby2019adapters, goswami2024moment}; recent variations explore multi-scale finetuning~\citep{qiao2025msft}, importance-based LoRA selection~\citep{li2025trace}, input-representation adaptation~\citep{benechehab2025adapts}, structured pruning~\citep{zhao2025prune}, in-context tuning~\citep{faw2025icf}, retrieval-augmented adaptation~\citep{ning2025tsrag}, and Chronos-specific PEFT~\citep{gupta2024beyondlora}; complementary work computes transferability scores for backbone selection (TEMPLATE, \citealp{zhang2025template}) or provides a unified evaluation suite (GIFT-Eval, \citealp{woo2024gifteval}). These vary the finetuning \textit{strategy} while leaving per-input adapter \textit{topology} fixed; AdaPTS reports the best of several variants per dataset/horizon, treating adapter choice as a per-task hyperparameter rather than per-window routing. We instead route over heterogeneous expert topologies per window; the closest precedent in spirit is mixture-of-adapters in the LLM setting (AdaMix~\citep{wang2022adamix} mixes copies of one adapter type, whereas […]

> AGENT

I have the full picture. Let me verify the cross-reference from §3 line 252 to Related Work that we'll need to update.

> TOOL

tool_use Bash
id: toolu_01GUmZGZPJA2JmiNB8xroWon
```json
{
  "command": "grep -n \"ref{sec:related_work}\" main.tex",
  "description": "Find all references to related work section"
}
```

> TOOL

tool_result
id: toolu_01GUmZGZPJA2JmiNB8xroWon
```
252:This collapse is upstream of the optimization-induced collapse that existing rescues target -- load balancing~\citep{shazeer2017outrageously, fedus2022switch}, z-loss~\citep{zoph2022stmoe}, ReLU routing~\citep{wang2025remoe}, and expert-choice~\citep{zhou2022expertchoice} -- and is not addressed by prior MoE-adapter~\citep{wang2022adamix, wu2024mole}, MoE routing-collapse~\citep{chi2022representation, wu2024mhmoe, puigcerver2024softmoe, panda2024densebackprop, hua2025inputaware, guo2025expertspec}, or time-series-normalization~\citep{liu2022nonstationary, fan2023dishts, liu2023san, ye2024fan, dai2024ddn, berthelier2026revin, zou2025ibnorm} work (positioned in detail in \S\ref{sec:related_work}). We next formalize the loss (Observation~\ref{thm:mi_decomp}) and define a training-free predictor $R(\mathcal{D})$ for it; the rest of the section then specifies RR-MoA, the answer to the problem with $u(\mathbf{x})\!=\!\mathbf{x}$, and \S\ref{sec:main_results} verifies the answer with eight causal controls and a $720$-run rescue sweep (Table~\ref{tab:rescue}).
```

> AGENT

Now I have everything I need. Here's the plan.

## Plan: cut Related Work from PDF lines 88–148 to 88–100

### Audit summary

The four-paragraph Related Work currently runs **60 PDF lines** and contains **~55 unique citations**. Of those:

- **28 are duplicated** in §3 (lines 248, 252) or §4 (lines 419, 459, 522, 524, 561). Dropping them from Related Work loses no in-text citation.
- **27 are orphans** that appear *only* in Related Work + bibliography. These must be preserved in the rewritten paragraph (or moved to a downstream section).

Orphans to preserve:
- *TSFM/adapter:* `wen2023tssurvey`, `wu2025srsnet`, `wang2025timemixerpp`, `xu2024fits`, `chen2023tsmixer`, `fu2025selective`, `jin2024timellm`, `zhou2023onefitsall`, `liu2024autotimes`, `houlsby2019adapters`, `qiao2025msft`, `benechehab2025adapts`, `zhao2025prune`, `faw2025icf`, `ning2025tsrag`, `gupta2024beyondlora`, `zhang2025template`, `woo2024gifteval`
- *MoE:* `lepikhin2021gshard`, `riquelme2021vmoe`, `komatsuzaki2023sparseupcycling`, `raposo2024mod`, `jiang2024mixtral`, `zhu2024llamamoe`, `dai2024deepseekmoe`, `cai2024moesurvey`, `shi2024timemoe`, `he2025sempo`, `ma2018mmoe`, `wang2026myth`
- *Normalization:* `ulyanov2016instancenorm`

### Approach

Replace the four-paragraph thread-by-thread structure with **one compact paragraph** (≤12 PDF lines) that packs the 27 orphans into dense citation lists with a one-clause role marker per cluster. The duplicated citations are simply deleted: §3 line 252 and §4 already carry their narrative weight, so nothing moves — they vanish from §2 only.

Cluster structure (one sentence each, ~2–3 PDF lines per cluster):

1. **TSFM adaptation cluster** […]

> DEVELOPER

was this directly relevant to our discussion theme: "  Lost (intentionally): detailed per-paper contrast (e.g.,
   AdaPTS treats adapter choice as per-task
  hyperparameter; SEMPO routes prompt-experts at token
  level; the "no prior per-window topology mixture in TSFM
   literature" novelty claim — recoverable as
  half-sentence if budget allows)."

> AGENT

You're right to push back. Two of the three are core, not peripheral:

1. **AdaPTS contrast (per-task vs per-window)** — directly relevant. It's the cleanest way to state what RR-MoA does that the closest TSFM-adapter peer doesn't. Cutting it weakens the positioning, not just the prose.

2. **"No prior per-window topology mixture in TSFM literature" novelty claim** — *most* relevant. This is the contribution statement, not flavor. Demoting it to "recoverable if budget allows" was a mistake — it should be load-bearing in any related work, even at 12 lines.

3. **SEMPO contrast (token-level vs window-level)** — moderately relevant. SEMPO is the closest in-TSFM mixture, and "token-level prompt mixture vs per-window adapter mixture" is the right axis to put it on. Worth keeping if budget permits, but the role marker "in-backbone TS-MoE" already covers it categorically.

**Revised plan:** keep #1 and #3 in the compressed paragraph, treat #2 as the compressible item. The TSFM adaptation cluster ends with one short clause carrying both: *"AdaPTS treats adapter choice as a per-task hyperparameter; we are the first per-window mixture over topologically distinct adapters on a frozen TSFM."* That's ~1.5 lines and covers the contribution claim explicitly. The remaining 27 orphans pack around […]

> DEVELOPER

no let cut more from the intro currently  start at 30 and ends at 80 (50 lines), it should ideally be about 38 pages

> AGENT

Let me read the current intro in the PDF and source.

> TOOL

tool_use Bash
id: toolu_01CEDDWeJcxohhVvnHt2qx8N
```json
{
  "command": "pdftotext -layout -f 1 -l 3 /Users/hungpq2412/neuralips26/main.pdf - 2>/dev/null | sed -n '1,150p'",
  "description": "Read the intro section from PDF"
}
```

> TOOL

tool_result
id: toolu_01CEDDWeJcxohhVvnHt2qx8N
```
            Raw-Routed Mixture of Adapters: A Causal
          Intervention for Routing Collapse in Time Series
                         Foundation Models


                                                  Anonymous Author(s)
                                                      Affiliation
                                                       Address
                                                        email



                                                         Abstract

 1             Many time series foundation models (TSFMs) adapt to a target dataset by attaching
 2             a single trainable head to a frozen backbone. A single head is one-size-fits-all,
 3             yet target series mix heterogeneous regimes that a single head may underfit. The
 4             natural upgrade is to replace the single head with a mixture-of-experts (MoE) head
 5             whose router dispatches each window to a specialist. This upgrade fails on instance-
 6             normalized backbones, a dominant TSFM design class that strips each window’s
 7             mean and variance before encoding. We call this failure normalization-induced
 8             routing collapse. Once joint training makes even one backbone transformer block
 9             trainable, routing entropy falls to 0.000. Every input is sent to a single expert;
10             the rest are never activated. A 720-run sweep across standard MoE rescue mecha-
11             nisms recovers at most 10.9% MSE, 2.7× worse than our causal intervention. The
12             failure is in the router’s input, not its optimization. We formalize this via a mutual-
13             information decomposition. The resulting signal-ratio statistic is computable before
14 […]

> TOOL

tool_use Read
id: toolu_01NRJjzrPe6qM7RQmFkZfpfV
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 61,
  "limit": 100
}
```

> TOOL

tool_result
id: toolu_01NRJjzrPe6qM7RQmFkZfpfV
```
61	\section{Introduction}
62	\label{sec:intro}
63	
64	Time series foundation models (TSFMs) such as MOMENT~\citep{goswami2024moment}, TimesFM~\citep{das2024timesfm}, Chronos~\citep{ansari2024chronos}, Timer-XL~\citep{liu2025timerxl,liu2024timer}, and Moirai~\citep{woo2024moirai} now provide pretrained representations for time series, alongside a growing ecosystem of pretrained variants and LLM-reprogrammed forecasters~\citep{lee2024units, rasul2024lagllama, ekambaram2024ttm, cohen2025toto, liu2025sundial, jin2024timellm, zhou2023onefitsall, liu2024autotimes, pan2024s2ipllm, liu2024unitime, shi2024timemoe, liu2026timers1}. Using one of these backbones on a downstream task still requires attaching a lightweight adapter head that maps hidden states to predictions; this paper studies the adapter, holding the backbone fixed.
65	
66	Standard TSFM adapters apply the \emph{same} regression head to every window (Figure~\ref{fig:problem_overview}a): flatten-then-project for MOMENT~\citep{goswami2024moment} and PatchTST~\citep{nie2023patchtst}, an autoregressive residual block for TimesFM~\citep{das2024timesfm}. Real time series mix heterogeneous regimes whose \emph{shape} variation (periodicity, trends, level shifts, change points) survives instance normalization and lives in the hidden states across layers~\citep{wilinski2025tsfm_representations, pandey2025tsfm_semantics}, motivating a per-window mixture of topologically distinct expert heads with a learned router. Keeping the backbone frozen is also what makes deployment practical: a shared TSFM in GPU memory serves many tenants through lightweight per-task adapters hot-swapped from host RAM, an arrangement per-dataset models like DLinear~\citep{zeng2023dlinear} cannot match (Appendices~\ref{app:deployment},~\ref{app:benchmark}).
67	
68	This natural mixture-of-experts approach fails on instance-normalized TSFMs once any backbone layers are unfrozen (Figure~\ref{fig:problem_overview}b). […]

> AGENT

Have everything I need. Here's the cut plan for the Intro.

## Plan: cut Intro from PDF lines 30–84 (55 lines) to ~38 lines

### Current shape

| Source line | Role | PDF lines | Lines |
|---|---|---|---|
| L64 | TSFM intro + ecosystem citation list | 30–34 | 5 |
| L66 | Per-window mixture motivation + deployment | 35–42 | 8 |
| L68 | Collapse statement (entropy → 0; co-adaptation) | 43–51 | 9 |
| L70 | "Failure is specific to learnable-affine…" + rescue numbers + Moirai | 52–56 | 5 |
| L72 | RR-MoA fix + Frozen Paradox preview | 57–62 | 6 |
| L74 | "Three contributions" lead-in | 63–64 | 2 |
| L76 | **Bullet 1**: Problem formulation | 65–70 | 6 |
| L77 | **Bullet 2**: Experimental results | 71–77 | 7 |
| L78 | **Bullet 3**: Causal intervention | 78–84 | 7 |
| | | | **55** |

### Where the redundancy lives

- **Bullet 1** repeats the "720-run / 10.9% / 2.7× / input-not-optimization" content already in L70 + abstract.
- **Bullet 3** repeats the RR-MoA + SR-MoA + Residual-IA⁺ summary already […]

> DEVELOPER

We want to keep the contribution bullet, compress the earlier parts of the intro

> AGENT

Got it — bullets stay, pre-bullet prose absorbs all the cuts.

## Revised Plan: keep bullets (lines 63–84, 22 lines), compress prose lines 30–62 from 33 lines to ~14 lines

### Target arithmetic

| Block | Lines | Action |
|---|---|---|
| Pre-bullet prose (L64, L66, L68, L70, L72) | 33 | **cut to ~14** |
| Lead-in (L74) | 2 | keep (or trim to 1) |
| Bullets 1–3 (L76–L78) | 22 | **keep verbatim** |
| **Total** | **57** | **~38** |

Cut required: ~19 lines from 33 (≈58%). All from the five prose paragraphs.

### Per-paragraph compression plan

**L64 — TSFM ecosystem intro (5 lines → 2 lines).** Keep the 18-citation ecosystem block (it's a few rendered chars and signals scope) but drop the named-backbone enumeration and the "alongside a growing ecosystem of pretrained variants and LLM-reprogrammed forecasters" connector. Rewrite:

> Time series foundation models (TSFMs)~\citep{goswami2024moment, das2024timesfm, ansari2024chronos, liu2025timerxl, liu2024timer, woo2024moirai, lee2024units, rasul2024lagllama, ekambaram2024ttm, cohen2025toto, liu2025sundial, jin2024timellm, zhou2023onefitsall, liu2024autotimes, pan2024s2ipllm, liu2024unitime, shi2024timemoe, liu2026timers1} adapt to downstream tasks via a lightweight adapter head; this paper studies the adapter, holding the backbone fixed.

**L66 — per-window mixture motivation + deployment (8 lines → ~4 lines).** Drop the "flatten-then-project […]

> DEVELOPER

let's go

> AGENT

Executing now. Let me verify a couple of cross-references first to avoid breaking them.

> TOOL

tool_use Bash
id: toolu_018zCFQBJBFDYSJxQyUHG4eD
```json
{
  "command": "grep -n \"ref{app:benchmark}\\|ref{app:deployment}\" main.tex | head -10",
  "description": "Check usage of app:deployment and app:benchmark labels"
}
```

> TOOL

tool_result
id: toolu_018zCFQBJBFDYSJxQyUHG4eD
```
66:Standard TSFM adapters apply the \emph{same} regression head to every window (Figure~\ref{fig:problem_overview}a): flatten-then-project for MOMENT~\citep{goswami2024moment} and PatchTST~\citep{nie2023patchtst}, an autoregressive residual block for TimesFM~\citep{das2024timesfm}. Real time series mix heterogeneous regimes whose \emph{shape} variation (periodicity, trends, level shifts, change points) survives instance normalization and lives in the hidden states across layers~\citep{wilinski2025tsfm_representations, pandey2025tsfm_semantics}, motivating a per-window mixture of topologically distinct expert heads with a learned router. Keeping the backbone frozen is also what makes deployment practical: a shared TSFM in GPU memory serves many tenants through lightweight per-task adapters hot-swapped from host RAM, an arrangement per-dataset models like DLinear~\citep{zeng2023dlinear} cannot match (Appendices~\ref{app:deployment},~\ref{app:benchmark}).
246:\textbf{Task setup.} Given a window $\mathbf{x}\in\mathbb{R}^{T\times c}$ ($T{=}512$, $c$ channels), forecasting predicts $\mathbf{y}\in\mathbb{R}^{h\times c}$ at horizons $h\in\{96,192,336,720\}$ under MSE loss (imputation uses the same formalism with $\mathbf{y}$ as the reconstruction target). A pretrained TSFM acts as a feature extractor $f_\theta:\mathbb{R}^{T\times c}\to\mathbb{R}^{P\times d}$ ($P$ patches of dim $d$) with $\theta$ \emph{frozen} ($\nabla_\theta\!\equiv\!0$); we train only an adapter $g_\phi:\mathbb{R}^{P\times d}\to\mathbb{R}^{h\times c}$ with a small parameter budget ($|\phi|\leq 500$K), so that many task-specific adapters can be hot-swapped onto a single shared backbone (App.~\ref{app:deployment}). A \emph{per-window mixture of adapters} replaces $g_\phi$ with $K$ experts $\{\mathrm{Expert}_j\}_{j=1}^K$ plus a router $G_\psi$ that returns […]

> TOOL

tool_use Bash
id: toolu_01X7g6YbDvVGXEAPGA6oPPx7
```json
{
  "command": "grep -c \"nie2023patchtst\\|das2024timesfm\\|fedus2022switch\" main.tex; echo \"---\"; for c in nie2023patchtst das2024timesfm fedus2022switch; do echo \"$c:\"; grep -n \"$c\" main.tex | head -3; done",
  "description": "Verify duplicates of cites we plan to drop"
}
```

> TOOL

tool_result
id: toolu_01X7g6YbDvVGXEAPGA6oPPx7
```
16
---
nie2023patchtst:
66:Standard TSFM adapters apply the \emph{same} regression head to every window (Figure~\ref{fig:problem_overview}a): flatten-then-project for MOMENT~\citep{goswami2024moment} and PatchTST~\citep{nie2023patchtst}, an autoregressive residual block for TimesFM~\citep{das2024timesfm}. Real time series mix heterogeneous regimes whose \emph{shape} variation (periodicity, trends, level shifts, change points) survives instance normalization and lives in the hidden states across layers~\citep{wilinski2025tsfm_representations, pandey2025tsfm_semantics}, motivating a per-window mixture of topologically distinct expert heads with a learned router. Keeping the backbone frozen is also what makes deployment practical: a shared TSFM in GPU memory serves many tenants through lightweight per-task adapters hot-swapped from host RAM, an arrangement per-dataset models like DLinear~\citep{zeng2023dlinear} cannot match (Appendices~\ref{app:deployment},~\ref{app:benchmark}).
248:\textbf{Problem statement.} The standard MoE recipe~\citep{shazeer2017outrageously, fedus2022switch} lets the router $G_\psi$ read the backbone's hidden states $f_\theta(\mathbf{x})$, and this is the choice taken by the closest TSFM-adapter precedent, AdaMix~\citep{wang2022adamix}. We show that on TSFMs equipped with instance normalization (RevIN~\citep{kim2021revin}, the de facto standard for distribution-shift handling in MOMENT~\citep{goswami2024moment}, PatchTST~\citep{nie2023patchtst}, and TimesFM~\citep{das2024timesfm}) this choice has a structural failure mode not previously characterized: the router's input is missing, by construction of an upstream architectural normalizer, the per-window first- and second-order statistics that distinguish regimes (formalized in Observation~\ref{thm:mi_decomp}), so $G_\psi$ collapses to a single expert and the […]

> AGENT

Confirmed safe to drop those duplicates. Executing the edits now.

> TOOL

tool_use Edit
id: toolu_01Qe5TNhhkBpchyenh5iujTv
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "Time series foundation models (TSFMs) such as MOMENT~\\citep{goswami2024moment}, TimesFM~\\citep{das2024timesfm}, Chronos~\\citep{ansari2024chronos}, Timer-XL~\\citep{liu2025timerxl,liu2024timer}, and Moirai~\\citep{woo2024moirai} now provide pretrained representations for time series, alongside a growing ecosystem of pretrained variants and LLM-reprogrammed forecasters~\\citep{lee2024units, rasul2024lagllama, ekambaram2024ttm, cohen2025toto, liu2025sundial, jin2024timellm, zhou2023onefitsall, liu2024autotimes, pan2024s2ipllm, liu2024unitime, shi2024timemoe, liu2026timers1}. Using one of these backbones on a downstream task still requires attaching a lightweight adapter head that maps hidden states to predictions; this paper studies the adapter, holding the backbone fixed.",
  "new_string": "Time series foundation models (TSFMs)~\\citep{goswami2024moment, das2024timesfm, ansari2024chronos, liu2025timerxl, liu2024timer, woo2024moirai, lee2024units, rasul2024lagllama, ekambaram2024ttm, cohen2025toto, liu2025sundial, jin2024timellm, zhou2023onefitsall, liu2024autotimes, pan2024s2ipllm, liu2024unitime, shi2024timemoe, liu2026timers1} adapt to downstream tasks via a lightweight adapter head; this paper studies the adapter, holding the backbone fixed."
}
```

> TOOL

tool_result
id: toolu_01Qe5TNhhkBpchyenh5iujTv
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01CpBuSLYaiMty9nZ2UMhozn
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "Standard TSFM adapters apply the \\emph{same} regression head to every window (Figure~\\ref{fig:problem_overview}a): flatten-then-project for MOMENT~\\citep{goswami2024moment} and PatchTST~\\citep{nie2023patchtst}, an autoregressive residual block for TimesFM~\\citep{das2024timesfm}. Real time series mix heterogeneous regimes whose \\emph{shape} variation (periodicity, trends, level shifts, change points) survives instance normalization and lives in the hidden states across layers~\\citep{wilinski2025tsfm_representations, pandey2025tsfm_semantics}, motivating a per-window mixture of topologically distinct expert heads with a learned router. Keeping the backbone frozen is also what makes deployment practical: a shared TSFM in GPU memory serves many tenants through lightweight per-task adapters hot-swapped from host RAM, an arrangement per-dataset models like DLinear~\\citep{zeng2023dlinear} cannot match (Appendices~\\ref{app:deployment},~\\ref{app:benchmark}).",
  "new_string": "Standard TSFM adapters apply one head to every window (Figure~\\ref{fig:problem_overview}a), yet real series mix regimes whose \\emph{shape} variation (periodicity, trends, level shifts) lives across hidden layers~\\citep{wilinski2025tsfm_representations, pandey2025tsfm_semantics}, motivating a per-window mixture of topologically distinct experts. Keeping the backbone frozen is also the practical deployment enabler: one TSFM serves many tenants through hot-swapped per-task adapters, unlike per-dataset models such as DLinear~\\citep{zeng2023dlinear} (App.~\\ref{app:deployment})."
}
```

> TOOL

tool_result
id: toolu_01CpBuSLYaiMty9nZ2UMhozn
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01J7bSRiFoAGmTFdEY29iZP9
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "This natural mixture-of-experts approach fails on instance-normalized TSFMs once any backbone layers are unfrozen (Figure~\\ref{fig:problem_overview}b). Combining an AdaMix-style adapter pool~\\citep{wang2022adamix} with a hidden-state softmax router and Switch-style load balancing~\\citep{fedus2022switch} on MOMENT$+$RevIN drops routing entropy to zero in most unfrozen configurations (Table~\\ref{tab:adamix}): every window is sent to one expert and the rest are never used. We call this \\emph{normalization-induced routing collapse}: RevIN~\\citep{kim2021revin} strips the per-window mean and variance the router needs to distinguish regimes (formalized in Observation~\\ref{thm:mi_decomp}; signal-ratio diagnostic in Figure~\\ref{fig:signal_ratio}). Even frozen, hidden-state routing underperforms; unfrozen, the dominant expert's larger gradients reshape the backbone to serve it more, closing a co-adaptation loop within tens of steps (Figure~\\ref{fig:trajectory}).\n\nThe failure is specific to learnable-affine instance normalization inside the encoder pipeline: Moirai, which uses only non-learnable per-instance I/O scaling with internal RMSNorm, does not collapse (\\S\\ref{sec:cross_backbone}), and standard MoE rescue mechanisms (load balancing, entropy regularization, z-loss, ReLU routing, expert-choice) recover at most $10.9\\%$ MSE, $2.7\\times$ worse than RR-MoA (Table~\\ref{tab:rescue}): the problem is in the router's \\emph{input}, not its optimization.\n\nBecause the diagnosis pinpoints normalization as the cause, the fix principle is direct. \\emph{Raw-Routed Mixture of Adapters} (RR-MoA) routes on the raw, pre-normalization input […]

> TOOL

tool_result
id: toolu_01J7bSRiFoAGmTFdEY29iZP9
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_013ysZ3pKtVMAmyCWEaZgewp
```json
{
  "command": "grep -n \"AdaPTS\\|adapts2025\\|adaPTS\" main.tex | head; echo \"---bib---\"; grep -n \"benechehab2025adapts\\|adapts\" main.tex | head",
  "description": "Check AdaPTS citation"
}
```

> TOOL

tool_result
id: toolu_013ysZ3pKtVMAmyCWEaZgewp
```
231:\textbf{TSFM Adaptation.} Beyond the broad survey of~\citet{wen2023tssurvey}, a complementary line shows that compact task-specific models match or beat heavyweight pretrained backbones on LTSF benchmarks~\citep{wu2025srsnet, wang2025timemixerpp, xu2024fits, chen2023tsmixer, fu2025selective}: that lightweight raw-input models are competitive is itself evidence that the per-window raw signal carries most of the predictability our diagnostic $R(\mathcal{D})$ exploits (\S\ref{sec:diagnosis}). LLM-reprogrammed forecasters~\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes} inherit per-window normalization upstream of the backbone, so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is attached. We focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a lightweight module to a frozen TSFM~\citep{hu2022lora, houlsby2019adapters, goswami2024moment}; recent variations explore multi-scale finetuning~\citep{qiao2025msft}, importance-based LoRA selection~\citep{li2025trace}, input-representation adaptation~\citep{benechehab2025adapts}, structured pruning~\citep{zhao2025prune}, in-context tuning~\citep{faw2025icf}, retrieval-augmented adaptation~\citep{ning2025tsrag}, and Chronos-specific PEFT~\citep{gupta2024beyondlora}; complementary work computes transferability scores for backbone selection (TEMPLATE, \citealp{zhang2025template}) or provides a unified evaluation suite (GIFT-Eval, \citealp{woo2024gifteval}). These vary the finetuning \textit{strategy} while leaving per-input adapter \textit{topology} fixed; AdaPTS reports the best of several variants per dataset/horizon, treating adapter choice as a per-task hyperparameter rather than per-window routing. We instead route over heterogeneous expert topologies per window; the closest precedent in spirit is mixture-of-adapters in the LLM setting (AdaMix~\citep{wang2022adamix} mixes copies of one adapter type, whereas […]

> AGENT

Now the Related Work edit and the §3 cross-reference fix.

> TOOL

tool_use Edit
id: toolu_01YRzLs4LY8p41FfDkUh8AEv
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\section{Related Work}\n\\label{sec:related_work}\n\nWe position RR-MoA against four threads: TSFM adaptation, MoE in foundation models, MoE routing collapse and rescue, and time-series normalization.\n\n\\textbf{TSFM Adaptation.} Beyond the broad survey of~\\citet{wen2023tssurvey}, a complementary line shows that compact task-specific models match or beat heavyweight pretrained backbones on LTSF benchmarks~\\citep{wu2025srsnet, wang2025timemixerpp, xu2024fits, chen2023tsmixer, fu2025selective}: that lightweight raw-input models are competitive is itself evidence that the per-window raw signal carries most of the predictability our diagnostic $R(\\mathcal{D})$ exploits (\\S\\ref{sec:diagnosis}). LLM-reprogrammed forecasters~\\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes} inherit per-window normalization upstream of the backbone, so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is attached. We focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a lightweight module to a frozen TSFM~\\citep{hu2022lora, houlsby2019adapters, goswami2024moment}; recent variations explore multi-scale finetuning~\\citep{qiao2025msft}, importance-based LoRA selection~\\citep{li2025trace}, input-representation adaptation~\\citep{benechehab2025adapts}, structured pruning~\\citep{zhao2025prune}, in-context tuning~\\citep{faw2025icf}, retrieval-augmented adaptation~\\citep{ning2025tsrag}, and Chronos-specific PEFT~\\citep{gupta2024beyondlora}; complementary work computes transferability scores for backbone selection (TEMPLATE, \\citealp{zhang2025template}) or provides a unified evaluation suite (GIFT-Eval, \\citealp{woo2024gifteval}). These vary the finetuning \\textit{strategy} while leaving per-input adapter \\textit{topology} fixed; AdaPTS reports the best of several variants per dataset/horizon, treating adapter choice as a per-task hyperparameter rather than per-window routing. We […]

> TOOL

tool_result
id: toolu_01YRzLs4LY8p41FfDkUh8AEv
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01JA64G4zrYuXp293YChadYZ
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "or time-series-normalization~\\citep{liu2022nonstationary, fan2023dishts, liu2023san, ye2024fan, dai2024ddn, berthelier2026revin, zou2025ibnorm} work (positioned in detail in \\S\\ref{sec:related_work}).",
  "new_string": "or time-series-normalization~\\citep{liu2022nonstationary, fan2023dishts, liu2023san, ye2024fan, dai2024ddn, berthelier2026revin, zou2025ibnorm} work."
}
```

> TOOL

tool_result
id: toolu_01JA64G4zrYuXp293YChadYZ
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> AGENT

Now compile and verify.

> TOOL

tool_use Bash
id: toolu_013DEvPWR5sUPE1PC81gmmQm
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/build1.log 2>&1; echo \"exit=$?\"; tail -20 /tmp/build1.log",
  "description": "First pdflatex pass"
}
```

> TOOL

tool_result
id: toolu_013DEvPWR5sUPE1PC81gmmQm
```
exit=0
/texmf/fonts/type1/public/amsfonts/cm/cmr7.pfb></Users/hungpq2412/Library/texmf
/fonts/type1/public/amsfonts/cm/cmr8.pfb></Users/hungpq2412/Library/texmf/fonts
/type1/public/amsfonts/cm/cmr9.pfb></Users/hungpq2412/Library/texmf/fonts/type1
/public/amsfonts/cm/cmsy10.pfb></Users/hungpq2412/Library/texmf/fonts/type1/pub
lic/amsfonts/cm/cmsy5.pfb></Users/hungpq2412/Library/texmf/fonts/type1/public/a
msfonts/cm/cmsy6.pfb></Users/hungpq2412/Library/texmf/fonts/type1/public/amsfon
ts/cm/cmsy7.pfb></Users/hungpq2412/Library/texmf/fonts/type1/public/amsfonts/cm
/cmsy8.pfb></Users/hungpq2412/Library/texmf/fonts/type1/public/amsfonts/cm/cmsy
9.pfb></Users/hungpq2412/Library/texmf/fonts/type1/public/amsfonts/cm/cmti7.pfb
></Users/hungpq2412/Library/texmf/fonts/type1/public/amsfonts/cm/cmti8.pfb></Us
ers/hungpq2412/Library/texmf/fonts/type1/public/amsfonts/cm/cmti9.pfb></Users/h
ungpq2412/Library/texmf/fonts/type1/public/amsfonts/symbols/msbm10.pfb></usr/lo
cal/texlive/2026basic/texmf-dist/fonts/type1/public/cm-super/sftt1000.pfb></usr
/local/texlive/2026basic/texmf-dist/fonts/type1/urw/helvetic/uhvr8a.pfb></usr/l
ocal/texlive/2026basic/texmf-dist/fonts/type1/urw/times/utmb8a.pfb></usr/local/
texlive/2026basic/texmf-dist/fonts/type1/urw/times/utmbi8a.pfb></usr/local/texl
ive/2026basic/texmf-dist/fonts/type1/urw/times/utmr8a.pfb></usr/local/texlive/2
026basic/texmf-dist/fonts/type1/urw/times/utmri8a.pfb>
Output written on main.pdf (50 pages, 902407 bytes).
Transcript written on main.log.
```

> TOOL

tool_use Bash
id: toolu_01BBMnKZwoNRE3kSktns9kdg
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/build2.log 2>&1; echo \"exit=$?\"; grep -E \"Warning|Error\" /tmp/build2.log | grep -vi \"font\\|microtype\\|underfull\\|overfull\\|redefin\" | head -30",
  "description": "Second pdflatex pass + warning scan"
}
```

> TOOL

tool_result
id: toolu_01BBMnKZwoNRE3kSktns9kdg
```
exit=0
Package hyperref Warning: Token not allowed in a PDF string (Unicode):
Package hyperref Warning: Token not allowed in a PDF string (Unicode):
Package hyperref Warning: Token not allowed in a PDF string (Unicode):
Package hyperref Warning: Token not allowed in a PDF string (Unicode):
Package hyperref Warning: Token not allowed in a PDF string (Unicode):
Package hyperref Warning: Token not allowed in a PDF string (Unicode):
Package hyperref Warning: Token not allowed in a PDF string (Unicode):
Package hyperref Warning: Token not allowed in a PDF string (Unicode):
```

> TOOL

tool_use Bash
id: toolu_01KzHfQiD76Kwwm5HST7oXuc
```json
{
  "command": "grep -E \"Citation .* undefined|LaTeX Warning: Reference\" /tmp/build2.log | head -20; echo \"---pages---\"; grep \"pages\" /tmp/build2.log | tail -2",
  "description": "Check undefined citations or refs"
}
```

> TOOL

tool_result
id: toolu_01KzHfQiD76Kwwm5HST7oXuc
```
---pages---
Output written on main.pdf (50 pages, 902407 bytes).
```

> TOOL

tool_use Bash
id: toolu_01C4Ga8xgcRxRMpMDFWXWHwn
```json
{
  "command": "pdftotext -layout -f 1 -l 4 main.pdf - 2>/dev/null | grep -nE \"^[[:space:]]*[0-9]+[[:space:]]\" | sed -n '25,90p'",
  "description": "Get rendered line numbers around intro and related work"
}
```

> TOOL

tool_result
id: toolu_01C4Ga8xgcRxRMpMDFWXWHwn
```
39:25             self-routed variant (SR-MoA) drops the external router entirely and outperforms
40:26             RR-MoA by 13–42%, and applying the same raw-signal principle at the expert
41:27             level (Residual-IA+ ) closes the gap with DLinear across six backbones × four
42:28             horizons. Code to reproduce all results is provided in the supplementary material.
45:29   1    Introduction
47:30   Time series foundation models (TSFMs) [2–7, 9–12, 47, 64, 70–75] adapt to downstream tasks via a
48:31   lightweight adapter head; this paper studies the adapter, holding the backbone fixed.
49:32   Standard TSFM adapters apply one head to every window (Figure 1a), yet real series mix regimes
50:33   whose shape variation (periodicity, trends, level shifts) lives across hidden layers [56, 57], motivating
51:34   a per-window mixture of topologically distinct experts. Keeping the backbone frozen is also the
85:35   practical deployment enabler: one TSFM serves many tenants through hot-swapped per-task adapters,
86:36   unlike per-dataset models such as DLinear [17] (App. B).
87:37   This natural MoE approach fails on instance-normalized TSFMs once backbone layers are unfrozen
88:38   (Figure 1b): an AdaMix-style pool [18] with a softmax router on MOMENT+RevIN drops routing
89:39   entropy to zero in most configurations (Table 2). We call this normalization-induced […]

> AGENT

Build clean — 41 intro lines vs target ~38. Two short edits to trim 2 more lines.

> TOOL

tool_use Edit
id: toolu_01MC9ecFxpgAU7twt7inocR2
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "Standard TSFM adapters apply one head to every window (Figure~\\ref{fig:problem_overview}a), yet real series mix regimes whose \\emph{shape} variation (periodicity, trends, level shifts) lives across hidden layers~\\citep{wilinski2025tsfm_representations, pandey2025tsfm_semantics}, motivating a per-window mixture of topologically distinct experts. Keeping the backbone frozen is also the practical deployment enabler: one TSFM serves many tenants through hot-swapped per-task adapters, unlike per-dataset models such as DLinear~\\citep{zeng2023dlinear} (App.~\\ref{app:deployment}).",
  "new_string": "Standard TSFM adapters apply one head to every window (Figure~\\ref{fig:problem_overview}a), yet real series mix regimes whose \\emph{shape} variation lives across hidden layers~\\citep{wilinski2025tsfm_representations, pandey2025tsfm_semantics}, motivating a per-window mixture of topologically distinct experts. Frozen-backbone deployment serves many tenants through hot-swapped per-task adapters, unlike per-dataset models like DLinear~\\citep{zeng2023dlinear} (App.~\\ref{app:deployment})."
}
```

> TOOL

tool_result
id: toolu_01MC9ecFxpgAU7twt7inocR2
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01159mz9bHhQV3aFY7CCGjHd
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "This natural MoE approach fails on instance-normalized TSFMs once backbone layers are unfrozen (Figure~\\ref{fig:problem_overview}b): an AdaMix-style pool~\\citep{wang2022adamix} with a softmax router on MOMENT$+$RevIN drops routing entropy to zero in most configurations (Table~\\ref{tab:adamix}). We call this \\emph{normalization-induced routing collapse}: RevIN~\\citep{kim2021revin} strips the per-window mean and variance the router needs (formalized in Observation~\\ref{thm:mi_decomp}; diagnostic in Figure~\\ref{fig:signal_ratio}), and the dominant expert's gradients reshape the backbone to serve it more in tens of steps (Figure~\\ref{fig:trajectory}). A 720-run sweep across standard rescues (load balancing, entropy regularization, z-loss, ReLU routing, expert-choice) recovers only $10.9\\%$ MSE, $2.7\\times$ worse than RR-MoA (Table~\\ref{tab:rescue}); Moirai's non-learnable I/O scaling does not collapse (\\S\\ref{sec:cross_backbone}), narrowing the cause to learnable-affine encoder normalization, not the router's optimization.",
  "new_string": "This natural MoE approach fails on instance-normalized TSFMs once backbone layers are unfrozen (Figure~\\ref{fig:problem_overview}b): an AdaMix-style pool~\\citep{wang2022adamix} with a softmax router on MOMENT$+$RevIN drops routing entropy to zero in most configurations (Table~\\ref{tab:adamix}). We call this \\emph{normalization-induced routing collapse}: RevIN~\\citep{kim2021revin} strips the per-window mean and variance the router needs (Observation~\\ref{thm:mi_decomp}), and the dominant expert's gradients reshape the backbone to serve it more in tens of steps (Figure~\\ref{fig:trajectory}). A 720-run rescue sweep recovers only $10.9\\%$ MSE, $2.7\\times$ […]

> TOOL

tool_result
id: toolu_01159mz9bHhQV3aFY7CCGjHd
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01BLLDVgzKhVMq6pdz6KFMHd
```json
{
  "command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/build3.log 2>&1 && pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/build4.log 2>&1; echo \"exit=$?\"; grep -E \"Citation .* undefined|LaTeX Warning: Reference\" /tmp/build4.log | head; echo \"---\"; grep \"Output written\" /tmp/build4.log",
  "description": "Two more pdflatex passes after trim"
}
```

> TOOL

tool_result
id: toolu_01BLLDVgzKhVMq6pdz6KFMHd
```
exit=0
---
Output written on main.pdf (50 pages, 902371 bytes).
```

> TOOL

tool_use Bash
id: toolu_01XF5HaQdsZACuhdTzetpKX3
```json
{
  "command": "pdftotext -layout -f 1 -l 4 main.pdf - 2>/dev/null | grep -nE \"^[[:space:]]*[0-9]+[[:space:]]\" | sed -n '40,90p'",
  "description": "Verify rendered intro and related work line counts"
}
```

> TOOL

tool_result
id: toolu_01XF5HaQdsZACuhdTzetpKX3
```
87:40   dominant expert’s gradients reshape the backbone to serve it more in tens of steps (Figure G.1). A
88:41   720-run rescue sweep recovers only 10.9% MSE, 2.7× worse than RR-MoA (Table G.3); Moirai’s
89:42   non-learnable I/O scaling does not collapse (§4.2), narrowing the cause to learnable-affine encoder
90:43   normalization.
91:44   Raw-Routed Mixture of Adapters (RR-MoA) routes on the raw, pre-normalization input Xraw with the
92:45   backbone strictly frozen; the same diagnosis predicts a Frozen Paradox (Proposition 1), confirmed
93:46   empirically (frozen best on 4/6, unfrozen-wins bounded at ≤ 13%).
94:47   The diagnosis (collapse → mechanism → minimal fix) and the controls that distinguish it from prior
95:48   MoE-collapse threads structure our three contributions:
96:49    • Problem formulation. We frame routing collapse on instance-normalized TSFMs as a router-input
97:50      failure rather than the router-optimization failure that prior MoE work targets [19, 22, 23, 32],
98:51      naming it normalization-induced routing collapse, and introduce a signal-ratio statistic R(D) that
99:52      quantifies dataset vulnerability before training. The dichotomy is empirical: a 720-run sweep
100:53      across 11 optimization-side rescues recovers at most 10.9% MSE, 2.7× worse than the input-side
101:54      intervention this framing prescribes.
102:55    • Experimental results. Eight causal controls […]

> AGENT

Targets hit: intro at 39 lines, related work at 13 lines (vs targets 38 and 12). Final verification on orphan citations and page boundary.

> TOOL

tool_use Bash
id: toolu_01UKrv7qVtgeCXrDiwuvthu2
```json
{
  "command": "for cit in benechehab2025adapts cai2024moesurvey chen2023tsmixer dai2024deepseekmoe faw2025icf fu2025selective gupta2024beyondlora he2025sempo houlsby2019adapters jiang2024mixtral komatsuzaki2023sparseupcycling lepikhin2021gshard ma2018mmoe ning2025tsrag qiao2025msft raposo2024mod riquelme2021vmoe ulyanov2016instancenorm wang2025timemixerpp wang2026myth wen2023tssurvey woo2024gifteval wu2025srsnet xu2024fits zhang2025template zhao2025prune zhu2024llamamoe; do count=$(grep -c \"$cit\" main.tex); printf \"%-32s %s\\n\" \"$cit\" \"$count\"; done | awk '$2==1 {print \"ORPHANED:\", $0}'; echo \"---no orphans means all 27 still cited---\"\ngrep \"page:end_main\" main.tex; echo \"---\"\npdftotext main.pdf - 2>/dev/null | grep -A1 \"Conclusion and Limitations\" | head -3\ngrep -n \"label{page:end_main}\" main.tex",
  "description": "Verify all 27 orphan cites still in text + check main body end page"
}
```

> TOOL

tool_result
id: toolu_01UKrv7qVtgeCXrDiwuvthu2
```
---no orphans means all 27 still cited---
{\looseness=-1 We identified \emph{normalization-induced routing collapse}: the same $(\mu,\sigma)$ stripping that lets TSFMs handle distribution shift removes the signal a downstream MoE router needs. Observation~\ref{thm:mi_decomp} formalizes the loss, $R(\mathcal{D})$ predicts it ($\rho{=}{-}0.88$), eight causal controls rule out optimization/geometry/paradigm alternatives, and three interventions confirm it: RR-MoA ($54/54$), SR-MoA ($+13$--$42\%$), Residual-IA\textsuperscript{+} ($107/123$). The diagnosis reframes a failure prior MoE work treats as optimization as one of \emph{router input}: $11$ optimization-side rescues recover at most $10.9\%$ MSE where changing only the routing signal recovers $54$--$80\%$, with optimizer and frozen backbone untouched; $R(\mathcal{D})$ is computable from raw windows alone, giving a pre-training go/no-go test. \textbf{Limitations:} specific to $(\mu,\sigma)$-stripping normalizers; classification, anomaly detection, longer horizons, and learned expert pools remain open.\label{page:end_main}}
---
Conclusion and Limitations

555:{\looseness=-1 We identified \emph{normalization-induced routing collapse}: the same $(\mu,\sigma)$ stripping that lets TSFMs handle distribution shift removes the signal a downstream MoE router needs. Observation~\ref{thm:mi_decomp} formalizes the loss, $R(\mathcal{D})$ predicts it ($\rho{=}{-}0.88$), eight causal controls rule out optimization/geometry/paradigm alternatives, and three interventions confirm it: RR-MoA ($54/54$), SR-MoA ($+13$--$42\%$), Residual-IA\textsuperscript{+} ($107/123$). The diagnosis reframes a failure prior MoE work treats as optimization as one of \emph{router input}: $11$ optimization-side rescues […]

> TOOL

tool_use Bash
id: toolu_017gCqVS3RwN2rCtCmvSfUgc
```json
{
  "command": "pdftotext main.pdf - 2>/dev/null | awk '/^[[:space:]]*[0-9]+[[:space:]]*$/{p=$1} /Conclusion and Limitations/{print \"Conclusion at p\", p; exit} /^A   Experimental Setup/{print \"Appendix A at p\", p; exit}' \necho \"---\"\n# Find which PDF page contains the conclusion\nfor p in $(seq 1 12); do\n  found=$(pdftotext -layout -f $p -l $p main.pdf - 2>/dev/null | grep -l \"Conclusion and Limitations\" 2>&1 | head -1)\n  if pdftotext -layout -f $p -l $p main.pdf - 2>/dev/null | grep -q \"Conclusion and Limitations\"; then\n    echo \"Conclusion appears on PDF page $p\"\n    break\n  fi\ndone\nfor p in $(seq 1 12); do\n  if pdftotext -layout -f $p -l $p main.pdf - 2>/dev/null | grep -q \"page:end_main\\|^A.*Experimental Setup\\|^Appendix A\"; then\n    echo \"Appendix-A starts on PDF page $p\"\n    break\n  fi\ndone",
  "description": "Find conclusion and appendix start pages"
}
```

> TOOL

tool_result
id: toolu_017gCqVS3RwN2rCtCmvSfUgc
```
Conclusion at p 284
---
Conclusion appears on PDF page 8
```

> TOOL

tool_use Bash
id: toolu_01CvFvJJWWGxUPh4GLWq3g3x
```json
{
  "command": "for p in 8 9 10 11 12; do\n  txt=$(pdftotext -layout -f $p -l $p main.pdf - 2>/dev/null)\n  if echo \"$txt\" | grep -q \"Experimental Setup Details\"; then\n    echo \"Appendix A heading on PDF page $p\"\n  fi\n  if echo \"$txt\" | grep -q \"Conclusion and Limitations\"; then\n    echo \"Conclusion section on PDF page $p\"\n  fi\n  echo \"page $p first line: $(echo \"$txt\" | head -1)\"\ndone",
  "description": "Find which page conclusion ends and appendix begins"
}
```

> TOOL

tool_result
id: toolu_01CvFvJJWWGxUPh4GLWq3g3x
```
Conclusion section on PDF page 8
page 8 first line: 269   (µ, σ) re-injection, these form the eight causal controls (Table F.1); the only mechanism consistent
page 9 first line: 304        International Conference on Machine Learning (ICML), volume 235 of PMLR, pages 16115–
page 10 first line: 353   [17] Ailing Zeng, Muxi Chen, Lei Zhang, and Qiang Xu. Are transformers effective for time series
page 11 first line: 402   [34] Weiwei Ye, Songgaojun Deng, Qiaosha Zou, and Ning Gui. FAN: Frequency adaptive normal-
page 12 first line: 450   [50] Xiandong Zou, Jia Li, Xiaotong Yuan, and Pan Zhou. IBNorm: Information-bottleneck inspired
```

> AGENT

Done. Build clean, no undefined citations, all 27 orphans preserved.

**Results:**

| | Target | Actual | Lines saved |
|---|---|---|---|
| Intro (PDF lines) | 38 | 39 | 16 (55 → 39) |
| Related Work (PDF lines) | 12 | 13 | 47 (60 → 13) |
| Main body ends | page 9 | **page 8** | 1 page freed |

**What changed:**
- Intro: collapsed L64 ecosystem cite block, dropped duplicated `nie2023patchtst`/`das2024timesfm`/`fedus2022switch`, folded former L70 into L68, tightened L72.
- Related Work: replaced 4 paragraphs with one packed paragraph carrying all 27 orphan cites + AdaPTS contrast + "no prior per-window topology mixture" novelty claim.
- §3 line 252: dropped now-misleading `(positioned in detail in §\ref{sec:related_work})` parenthetical.

**Citation integrity:** all 27 orphans (`benechehab2025adapts`, `cai2024moesurvey`, `wen2023tssurvey`, `wang2026myth`, `ulyanov2016instancenorm`, …) still resolve; the ~28 cites I dropped from §2 are all still wired in §3 (line 248, 252) or §4 (lines 419, 459, 522, 524, 561). No bibitem orphaned.

**Next steps:** the page-8 boundary gives you a full extra page of headroom. If you want to spend it, candidates are: restoring the SEMPO contrast in §2, adding a full-FT-vs-RR-MoA mini-table in §4, or extending the eight-control discussion. […]