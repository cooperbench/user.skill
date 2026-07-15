> DEVELOPER

we recently reorganise 4.2. 

Should we call subsection 4.2.1, 4.2.2 etc ?

> DEVELOPER

we recently reorganise 4.2. 

Should we call subsection 4.2.1, 4.2.2 etc ? what is neurips recommended or required

> TOOL

tool_use Bash
id: toolu_01Sb3oeHTZ15Ry1wSn8cJ7kp
```json
{
  "command": "ls /Users/hungpq2412/neuralips26/*.sty /Users/hungpq2412/neuralips26/neurips* 2>/dev/null",
  "description": "Find NeurIPS style files"
}
```

> TOOL

tool_result
id: toolu_01Sb3oeHTZ15Ry1wSn8cJ7kp
```
/Users/hungpq2412/neuralips26/neurips_2026.sty
/Users/hungpq2412/neuralips26/neurips_2026.sty
```

> TOOL

tool_use Bash
id: toolu_01EtA3k6L6Bj5PWxqX5f1TU2
```json
{
  "command": "grep -nE \"subsubsection|paragraph|subsection\" /Users/hungpq2412/neuralips26/main.tex | head -50",
  "description": "Check current sectioning usage in main.tex"
}
```

> TOOL

tool_result
id: toolu_01EtA3k6L6Bj5PWxqX5f1TU2
```
74:\paragraph{Contributions.}
388:\subsection{Setup}
398:\subsection{Main Results}
403:\subsubsection*{Diagnosis: adapters underperform, MoE collapses}
485:\subsubsection*{Mechanism: instance normalization strips the routing signal}
499:\subsubsection*{Standard rescues fail; the raw-input principle generalizes}
527:\subsubsection*{Headline numbers}
1061:\paragraph{Backbone specifications.} MOMENT-small ($d{=}512$, 8 encoder blocks, internal RevIN with learnable affine); MOMENT-large ($d{=}1024$, 24 blocks, internal RevIN with learnable affine); Moirai ($d{=}384$, 6 blocks, RMSNorm internally with non-learnable per-instance I/O scaling, no learnable-affine norm inside the encoder); Moirai-MoE ($d{=}384$, 6 blocks, RMSNorm internally with sparse internal experts and non-learnable per-instance I/O scaling); Chronos ($d{=}512$, 6 encoder blocks, T5 RMSNorm internally, no instance normalization); Timer-XL ($d{=}1024$, 8 blocks, LayerNorm internally, no instance normalization). Throughout, ``full fine-tuning'' means \emph{all} encoder blocks are unfrozen (8/8 for MOMENT-small, 24/24 for MOMENT-large, 6/6 for Moirai/Moirai-MoE/Chronos, 8/8 for Timer-XL).
1063:\paragraph{Training hyperparameters.} Adam optimizer, learning rate $10^{-3}$, MSE loss, batch size $128$, $15$ epochs. Final reported numbers are 15-epoch test MSE. Core multi-seed grids use seeds $\{42, 43, 44, 45, 46\}$ ($n{=}5$); ablations use seeds $\{42, 43, 44\}$ ($n{=}3$). Channel-wise StandardScaler normalization~\citep{zhou2021informer, nie2023patchtst} is applied to all inputs.
1065:\paragraph{Per-baseline configurations.}
1076:\paragraph{RR-MoA pseudocode.}
1105:\subsection{Inference Benchmark}
1200:\subsection{Theoretical Depth of Observation~\ref{thm:mi_decomp}}
1635:\subsection{Statistics Re-Injection Ablation}
1724:\subsection{Rescue-Baseline Sweep Details}
1756:\subsection{AdaMix Implementation Details}
1819:\subsection{Cross-Modality Control: Vision MoE}
1876:\subsection{Expert Pool Diversity Ablation}
1900:\subsection{Expert Count […]

> TOOL

tool_use Bash
id: toolu_01Ky53rAj1AVKxpMFkZWfYsg
```json
{
  "command": "grep -nE \"subsubsection|paragraph|subsection|secnumdepth|tocdepth|section\" /Users/hungpq2412/neuralips26/neurips_2026.sty | head -40",
  "description": "Check sectioning in style file"
}
```

> TOOL

tool_result
id: toolu_01Ky53rAj1AVKxpMFkZWfYsg
```
105:\newcommand{\acksection}{\section*{Acknowledgments and Disclosure of Funding}}
107:  \acksection
178:% sections with less space
179:\providecommand{\section}{}
180:\renewcommand{\section}{%
181:  \@startsection{section}{1}{\z@}%
186:\providecommand{\subsection}{}
187:\renewcommand{\subsection}{%
188:  \@startsection{subsection}{2}{\z@}%
193:\providecommand{\subsubsection}{}
194:\renewcommand{\subsubsection}{%
195:  \@startsection{subsubsection}{3}{\z@}%
200:\providecommand{\paragraph}{}
201:\renewcommand{\paragraph}{%
202:  \@startsection{paragraph}{4}{\z@}%
207:\providecommand{\subparagraph}{}
208:\renewcommand{\subparagraph}{%
209:  \@startsection{subparagraph}{5}{\z@}%
214:\providecommand{\subsubsubsection}{}
215:\renewcommand{\subsubsubsection}{%
244:% paragraph formatting
```

> TOOL

tool_use Bash
id: toolu_01XYzD8EYWgVQURWPv7zEzdG
```json
{
  "command": "ls /Users/hungpq2412/neuralips26/ | grep -iE \"instruction|format|guide|author|template\" 2>/dev/null",
  "description": "Look for NeurIPS author instructions"
}
```

> TOOL

tool_result
id: toolu_01XYzD8EYWgVQURWPv7zEzdG
```
rmit-slide-template.pptx
slide_generation_instruction.json
template-slide.pptx
template_code
```

> TOOL

tool_use Read
id: toolu_01JZfNAmB5jHjwqPed7qn7sG
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/neurips_2026.sty",
  "limit": 230,
  "offset": 175
}
```

> TOOL

tool_result
id: toolu_01JZfNAmB5jHjwqPed7qn7sG
```
175	% Force \footnotesize to be no smaller than 8pt
176	\renewcommand{\footnotesize}{\fontsize{8pt}{9.5pt}\selectfont}
177	
178	% sections with less space
179	\providecommand{\section}{}
180	\renewcommand{\section}{%
181	  \@startsection{section}{1}{\z@}%
182	                {-2.0ex \@plus -0.5ex \@minus -0.2ex}%
183	                { 1.5ex \@plus  0.3ex \@minus  0.2ex}%
184	                {\large\bf\raggedright}%
185	}
186	\providecommand{\subsection}{}
187	\renewcommand{\subsection}{%
188	  \@startsection{subsection}{2}{\z@}%
189	                {-1.8ex \@plus -0.5ex \@minus -0.2ex}%
190	                { 0.8ex \@plus  0.2ex}%
191	                {\normalsize\bf\raggedright}%
192	}
193	\providecommand{\subsubsection}{}
194	\renewcommand{\subsubsection}{%
195	  \@startsection{subsubsection}{3}{\z@}%
196	                {-1.5ex \@plus -0.5ex \@minus -0.2ex}%
197	                { 0.5ex \@plus  0.2ex}%
198	                {\normalsize\bf\raggedright}%
199	}
200	\providecommand{\paragraph}{}
201	\renewcommand{\paragraph}{%
202	  \@startsection{paragraph}{4}{\z@}%
203	                {1.5ex \@plus 0.5ex \@minus 0.2ex}%
204	                {-1em}%
205	                {\normalsize\bf}%
206	}
207	\providecommand{\subparagraph}{}
208	\renewcommand{\subparagraph}{%
209	  \@startsection{subparagraph}{5}{\z@}%
210	                {1.5ex \@plus 0.5ex \@minus 0.2ex}%
211	                {-1em}%
212	                {\normalsize\bf}%
213	}
214	\providecommand{\subsubsubsection}{}
215	\renewcommand{\subsubsubsection}{%
216	  \vskip5pt{\noindent\normalsize\rm\raggedright}%
217	}
218	
219	% float placement
220	\renewcommand{\topfraction      }{0.85}
221	\renewcommand{\bottomfraction   }{0.4}
222	\renewcommand{\textfraction     }{0.1}
223	\renewcommand{\floatpagefraction}{0.7}
224	
225	\newlength{\@neuripsabovecaptionskip}\setlength{\@neuripsabovecaptionskip}{7\p@}
226	\newlength{\@neuripsbelowcaptionskip}\setlength{\@neuripsbelowcaptionskip}{\z@}
227	
228	\setlength{\abovecaptionskip}{\@neuripsabovecaptionskip}
229	\setlength{\belowcaptionskip}{\@neuripsbelowcaptionskip}
230	
231	% swap above/belowcaptionskip lengths for tables
232	\renewenvironment{table}
233	  {\setlength{\abovecaptionskip}{\@neuripsbelowcaptionskip}%
234	   \setlength{\belowcaptionskip}{\@neuripsabovecaptionskip}%
235	   \@float{table}}
236	  {\end@float}
237	
238	% footnote formatting
239	\setlength{\footnotesep }{6.65\p@}
240	\setlength{\skip\footins}{9\p@ \@plus 4\p@ \@minus 2\p@}
241	\renewcommand{\footnoterule}{\kern-3\p@ \hrule width 12pc \kern 2.6\p@}
242	\setcounter{footnote}{0}
243 […]

> AGENT

Let me verify via the official NeurIPS 2026 handbook rather than rely on memory.

> TOOL

tool_use ToolSearch
id: toolu_01KvhddBPt5YB9oPNBDtL6Lx
```json
{
  "query": "select:WebFetch,WebSearch",
  "max_results": 5
}
```

> TOOL

tool_result
id: toolu_01KvhddBPt5YB9oPNBDtL6Lx
```
{
  "type": "tool_reference",
  "tool_name": "WebFetch"
}
{
  "type": "tool_reference",
  "tool_name": "WebSearch"
}
```

> TOOL

tool_use WebFetch
id: toolu_01PZ2BWYv9iJVqd2HSEJAogL
```json
{
  "url": "https://neurips.cc/Conferences/2026/PaperInformation/StyleFiles",
  "prompt": "Does NeurIPS 2026 require, recommend, allow, or discourage the use of \\subsubsection (numbered as 4.2.1, 4.2.2 etc.) within section subsections? What is said about sectioning depth, headings, or paragraph headings?"
}
```

> TOOL

tool_use WebSearch
id: toolu_01K6L2FoRsEp8xUmqN1n6UpC
```json
{
  "query": "NeurIPS 2026 author guidelines subsubsection paragraph heading formatting style"
}
```

> TOOL

tool_result ERROR
id: toolu_01PZ2BWYv9iJVqd2HSEJAogL
```
Request failed with status code 404
```

> TOOL

tool_result
id: toolu_01K6L2FoRsEp8xUmqN1n6UpC
```
Web search results for query: "NeurIPS 2026 author guidelines subsubsection paragraph heading formatting style"

Links: [{"title":"Formatting Instructions For NeurIPS 2026 - Overleaf, Online LaTeX Editor","url":"https://www.overleaf.com/latex/templates/formatting-instructions-for-neurips-2026/bjdwqfdkyftc"},{"title":"Formatting Instructions For NeurIPS 2026 Anonymous Author(s) Affiliation","url":"https://www.overleaf.com/latex/templates/formatting-instructions-for-neurips-2026/bjdwqfdkyftc.pdf"},{"title":"Formatting Instructions For NeurIPS 2026 David S. Hippocampus∗","url":"http://web.uvic.ca/~nmehta/incentives_and_machine_learning_spring2026/neurips_2026.pdf"},{"title":"Main Track Handbook 2026","url":"https://neurips.cc/Conferences/2026/MainTrackHandbook"},{"title":"NeurIPS 2026 LaTeX Template | Download & Formatting Guide | Underleaf","url":"https://www.underleaf.ai/templates/neurips"},{"title":"Author and Submission Instructions","url":"https://neurips.cc/Conferences/2015/PaperInformation/AuthorSubmissionInstructions"},{"title":"NeurIPS 2026 Evaluations & Datasets Track Call for Papers","url":"https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets"},{"title":"NeurIPS 2026 Call for Position Papers","url":"https://neurips.cc/Conferences/2026/CallForPositionPapers"},{"title":"NeurIPS 2026 Evaluations & Datasets FAQ","url":"https://neurips.cc/Conferences/2026/EvaluationsDatasetsFAQ"},{"title":"Call for Papers 2026","url":"https://neurips.cc/Conferences/2026/CallForPapers"}]

I found the NeurIPS 2026 author guidelines. Let me search for more specific information about heading and paragraph formatting styles, particularly for subsubsections.

Links: [{"title":"Formatting Instructions For NeurIPS 2026 - Overleaf, Online LaTeX Editor","url":"https://www.overleaf.com/latex/templates/formatting-instructions-for-neurips-2026/bjdwqfdkyftc"},{"title":"Formatting Instructions For NeurIPS 2026 Anonymous Author(s) Affiliation","url":"https://www.overleaf.com/latex/templates/formatting-instructions-for-neurips-2026/bjdwqfdkyftc.pdf"},{"title":"Formatting Instructions For NeurIPS 2026 David S. Hippocampus∗","url":"http://web.uvic.ca/~nmehta/incentives_and_machine_learning_spring2026/neurips_2026.pdf"},{"title":"NeurIPS 2026 LaTeX Template | Download & Formatting Guide | Underleaf","url":"https://www.underleaf.ai/templates/neurips"},{"title":"Main Track Handbook 2026","url":"https://neurips.cc/Conferences/2026/MainTrackHandbook"},{"title":"NeurIPS 2026 LaTeX Template + neurips_2026.sty (Free Download) | TypeTeX","url":"https://www.typetex.app/templates/neurips"},{"title":"Formatting Instructions For NeurIPS 2025","url":"https://arxiv.org/html/2506.15953v1"},{"title":"NeurIPS 2026 LaTeX Template | Free Download & Preview","url":"https://tools.useoctree.com/templates/neurips-2026"},{"title":"Formatting Instructions For NeurIPS 2023","url":"https://media.neurips.cc/Conferences/NeurIPS2023/Styles/neurips_2023.tex"},{"title":"NeurIPS Template | Format, Structure, and Guide","url":"https://scispace.com/templates/neurips--template-c3lczqjki2mz5xq"}]

Let me search for more detailed information about the heading styles in NeurIPS 2026, particularly for subsubsections.

Links: [{"title":"Formatting Instructions For NeurIPS 2026 - Overleaf, Online LaTeX Editor","url":"https://www.overleaf.com/latex/templates/formatting-instructions-for-neurips-2026/bjdwqfdkyftc"},{"title":"Formatting […]

> TOOL

tool_use WebFetch
id: toolu_011t6HTdA3dKF2tLTeNpMepF
```json
{
  "url": "http://web.uvic.ca/~nmehta/incentives_and_machine_learning_spring2026/neurips_2026.pdf",
  "prompt": "What does the NeurIPS 2026 formatting instructions say about headings — specifically about subsubsections, third-level headings, and the use of \\paragraph vs \\subsubsection? Quote exact wording about heading levels, numbering, and any recommendation for sub-sub-section depth."
}
```

> TOOL

tool_result
id: toolu_011t6HTdA3dKF2tLTeNpMepF
```
I appreciate your question, but I must inform you that the content provided appears to be a compressed PDF file containing binary data rather than readable text about NeurIPS 2026 formatting instructions.

The material shows PDF stream objects with FlateDecode compression, making it impossible to extract meaningful information about heading guidelines, subsubsections, or \paragraph vs \subsubsection recommendations.

To obtain the actual NeurIPS 2026 formatting guidelines, I'd recommend:

1. Visiting the official NeurIPS conference website directly
2. Downloading the uncompressed formatting template or style guide
3. Checking the conference's LaTeX or Word formatting documentation

If you have access to the uncompressed formatting document, I'd be happy to analyze it and provide the specific guidance you're seeking about heading levels and sectioning commands.

[Binary content (application/pdf, 151.6KB) also saved to /Users/hungpq2412/.claude/projects/-Users-hungpq2412-neuralips26/eebce0b6-1568-4ebd-a8ec-3737217b1b89/tool-results/webfetch-1777979417060-zrxnc0.pdf]
```

> TOOL

tool_use Read
id: toolu_01XUDmGbdcVKgniq5ZEdnUgt
```json
{
  "file_path": "/Users/hungpq2412/.claude/projects/-Users-hungpq2412-neuralips26/eebce0b6-1568-4ebd-a8ec-3737217b1b89/tool-results/webfetch-1777979417060-zrxnc0.pdf",
  "pages": "3-7"
}
```

> TOOL

tool_result
id: toolu_01XUDmGbdcVKgniq5ZEdnUgt
```
PDF pages extracted: 3 page(s) from /Users/hungpq2412/.claude/projects/-Users-hungpq2412-neuralips26/eebce0b6-1568-4ebd-a8ec-3737217b1b89/tool-results/webfetch-1777979417060-zrxnc0.pdf (151.6KB)
```

> TOOL

tool_use Read
id: toolu_0193dzXpeN2j2k7iYdfSSJQ6
```json
{
  "file_path": "/Users/hungpq2412/.claude/projects/-Users-hungpq2412-neuralips26/eebce0b6-1568-4ebd-a8ec-3737217b1b89/tool-results/webfetch-1777979417060-zrxnc0.pdf",
  "pages": "1-2"
}
```

> TOOL

tool_result
id: toolu_0193dzXpeN2j2k7iYdfSSJQ6
```
PDF pages extracted: 2 page(s) from /Users/hungpq2412/.claude/projects/-Users-hungpq2412-neuralips26/eebce0b6-1568-4ebd-a8ec-3737217b1b89/tool-results/webfetch-1777979417060-zrxnc0.pdf (151.6KB)
```

> AGENT

NeurIPS 2026 has no rule either way; both forms are explicitly legal. The official template (page 2 of the formatting instructions) demonstrates all three options side-by-side in Section 3 "Headings": numbered first/second/third-level, plus the inline `\paragraph` form. They're shown as equivalent stylistic choices, not a hierarchy of preference. There's no requirement to use or avoid `4.2.1`-style numbering.

**Practical recommendation: keep `\subsubsection*` (your current state).** Numbered subsubsections are unusual in NeurIPS papers — most use either the unnumbered starred form or `\paragraph{}` for inline bold runs (which you already use at lines 1061/1063/1065/1076 for "Backbone specifications.", "Training hyperparameters.", etc.). Switching to numbered `4.2.1–4.2.4` would:
- add visual clutter and a small amount of vertical space (you're already over 9 pages per `todo.md`)
- only pay off if you need to `\ref` them from elsewhere in the body — `\subsubsection*` can't be cross-referenced

Switch to numbered only if you find yourself wanting to write "see §4.2.3"; otherwise the current `\subsubsection*` is the right call. If you want to reclaim a bit more space, downgrade them to `\paragraph{Diagnosis.}` etc. — that's the most compact option and matches the rest of §4.

Sources:
- [Formatting Instructions For NeurIPS 2026 (PDF, p.2 §3 Headings)](http://web.uvic.ca/~nmehta/incentives_and_machine_learning_spring2026/neurips_2026.pdf)
- […]

> DEVELOPER

We exceeded strictly 9 pages Intro is quite long, even spill over results

> AGENT

Let me look at the current intro to see what's tightenable.

> TOOL

tool_use Bash
id: toolu_015BQxyfu72EhKkKYJWG4XEc
```json
{
  "command": "grep -nE \"^\\\\\\\\section|^\\\\\\\\subsection|^\\\\\\\\subsubsection|^\\\\\\\\appendix|^\\\\\\\\bibliography|^\\\\\\\\end\\\\{document\\\\}\" /Users/hungpq2412/neuralips26/main.tex | head -40",
  "description": "Map document structure"
}
```

> TOOL

tool_result
id: toolu_015BQxyfu72EhKkKYJWG4XEc
```
61:\section{Introduction}
228:\section{Related Work}
238:\section{Raw-Routed Mixture of Adapters (RR-MoA)}
386:\section{Experiments}
388:\subsection{Setup}
398:\subsection{Main Results}
403:\subsubsection*{Diagnosis: adapters underperform, MoE collapses}
485:\subsubsection*{Mechanism: instance normalization strips the routing signal}
499:\subsubsection*{Standard rescues fail; the raw-input principle generalizes}
527:\subsubsection*{Headline numbers}
564:\section{Conclusion and Limitations}
570:\bibliographystyle{plainnat}
1046:\appendix
1058:\section{Experimental Setup Details}
1094:\section{Deployment-Regime Motivation}
1105:\subsection{Inference Benchmark}
1134:\section{Multi-Horizon Evaluation}
1158:\section{Proposition Proofs}
1200:\subsection{Theoretical Depth of Observation~\ref{thm:mi_decomp}}
1308:\section{LoRA Sweep (Full Results)}
1373:\section{Routing Ablations}
1635:\subsection{Statistics Re-Injection Ablation}
1661:\section{Extended RR-MoA Freeze Grid}
1724:\subsection{Rescue-Baseline Sweep Details}
1756:\subsection{AdaMix Implementation Details}
1794:\section{Normalization Generalization}
1819:\subsection{Cross-Modality Control: Vision MoE}
1850:\section{Top-$k$ Sparse Routing Ablation}
1876:\subsection{Expert Pool Diversity Ablation}
1900:\subsection{Expert Count Scaling}
1926:\section{Imputation Results}
1954:\section{Learnable Normalization Coefficient}
1980:\section{Exact MI Loss and Bound Tightness}
2011:\section{Information Content Diagnostic}
2130:\section{Cross-Backbone RR-MoA}
2223:\section{Extended Full Fine-Tuning Ablation}
2289:\section{Closing the DLinear Gap}
2350:\subsection{Residual-IA: Closing the Remaining Gap}
2570:\subsubsection*{Residual-IA\textsuperscript{+}: closing the remaining gap to 5/6}
2646:\subsubsection*{Multi-horizon generalization: H${\in}\{96, 192, 336, 720\}$}
```

> TOOL

tool_use Bash
id: toolu_01KPkJsL8BMeXV3bCegG4mkd
```json
{
  "command": "awk 'NR>=70 && NR<=400 {print NR\": \"$0}' /Users/hungpq2412/neuralips26/main.tex | head -200",
  "description": "Read intro region of main.tex"
}
```

> TOOL

tool_result
id: toolu_01KPkJsL8BMeXV3bCegG4mkd
```
70: The failure is specific to learnable-affine instance normalization placed inside the encoder pipeline. Backbones such as Moirai, which apply only non-learnable per-instance I/O scaling and use RMSNorm internally (rather than RevIN-style learnable-affine normalization upstream of the encoder), do not collapse (\S\ref{sec:cross_backbone}), and standard MoE rescue mechanisms (load balancing, entropy regularization, z-loss, ReLU routing, expert-choice) recover at most $10.9\%$ MSE, still $2.7\times$ worse than RR-MoA (Table~\ref{tab:rescue}), because the problem lies in the router's \emph{input}, not its optimization.
71: 
72: Because the diagnosis pinpoints normalization as the cause, the fix principle is direct. \emph{Raw-Routed Mixture of Adapters} (RR-MoA) routes on the raw, pre-normalization input $\mathbf{X}_\text{raw}$ while keeping the backbone strictly frozen; only the router and five canonical expert heads are trainable. The same principle predicts a \emph{Frozen Paradox}: unfreezing triggers co-adaptation collapse (Proposition~\ref{prop:frozen}), so within a fixed MoE architecture frozen should match or beat unfrozen, which we confirm empirically (frozen best on $4/6$, unfrozen-wins bounded at $\leq 13\%$).
73: 
74: \paragraph{Contributions.}
75: \begin{itemize}[leftmargin=1.2em, itemsep=0.15em, topsep=0.2em]
76: \item We identify \emph{normalization-induced routing collapse}: an architectural failure mode of MoE adapters on instance-normalized TSFMs that is upstream of the optimization-induced collapses targeted by Switch~\citep{fedus2022switch}, ST-MoE~\citep{zoph2022stmoe}, ReMoE~\citep{wang2025remoe}, and Expert-Choice~\citep{zhou2022expertchoice}. Eight […]

> TOOL

tool_result
id: toolu_01XuECPZKKDqkqGyFmM1hXx4
```
61	\section{Introduction}
62	\label{sec:intro}
63	
64	Time series foundation models (TSFMs) such as MOMENT~\citep{goswami2024moment}, TimesFM~\citep{das2024timesfm}, Chronos~\citep{ansari2024chronos}, Timer-XL~\citep{liu2025timerxl,liu2024timer}, and Moirai~\citep{woo2024moirai} now provide pretrained representations for time series, alongside further pretrained variants~\citep{lee2024units, rasul2024lagllama, ekambaram2024ttm}, observability-domain TSFMs deployed at scale~\citep{cohen2025toto}, and continuous flow-matching forecasters such as Sundial~\citep{liu2025sundial} that bypass tokenization entirely. A parallel adaptation route reprograms pretrained LLMs as forecasters: Time-LLM~\citep{jin2024timellm} reprograms patch embeddings into the LLM token space, GPT4TS~\citep{zhou2023onefitsall} freezes the LLM's transformer blocks and tunes only positional and layer-norm parameters, AutoTimes~\citep{liu2024autotimes} casts forecasting as autoregressive next-token prediction, S$^2$IP-LLM~\citep{pan2024s2ipllm} attaches semantic prompts derived from the LLM's own embedding space, and UniTime~\citep{liu2024unitime} unifies cross-domain forecasting via natural-language domain instructions. Recent designs push toward billion-parameter scales~\citep{shi2024timemoe, liu2026timers1}. Using one of these backbones on a downstream task still requires attaching a lightweight adapter head that maps hidden states to predictions; this paper studies the adapter, holding the backbone fixed.
65	
66	Standard TSFM adapters apply a lightweight regression head on encoder outputs through the same head for every window (Figure~\ref{fig:problem_overview}a) -- flatten-then-project for MOMENT~\citep{goswami2024moment} and PatchTST~\citep{nie2023patchtst}, an autoregressive residual block for TimesFM~\citep{das2024timesfm}. Real time series mix heterogeneous regimes (quiet baselines, seasonal excursions, abrupt shape changes), and instance normalization handles only the […]

> TOOL

tool_use Read
id: toolu_01XuECPZKKDqkqGyFmM1hXx4
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 61,
  "limit": 85
}
```

> AGENT

Let me check the current build to see exactly where the page-9 boundary lands.

> TOOL

tool_use Bash
id: toolu_018kk1VJRKjRoivTZeQNScGM
```json
{
  "command": "pdflatex -interaction=nonstopmode -draftmode main.tex > /tmp/pdflatex1.log 2>&1 && pdflatex -interaction=nonstopmode main.tex > /tmp/pdflatex2.log 2>&1; echo \"EXIT=$?\"; tail -5 /tmp/pdflatex2.log",
  "description": "Rebuild main.tex to get current pagination"
}
```

> TOOL

tool_result
id: toolu_018kk1VJRKjRoivTZeQNScGM
```
EXIT=0
texlive/2026basic/texmf-dist/fonts/type1/urw/times/utmbi8a.pfb></usr/local/texl
ive/2026basic/texmf-dist/fonts/type1/urw/times/utmr8a.pfb></usr/local/texlive/2
026basic/texmf-dist/fonts/type1/urw/times/utmri8a.pfb>
Output written on main.pdf (51 pages, 884828 bytes).
Transcript written on main.log.
```

> TOOL

tool_use Bash
id: toolu_01Dx1NASf4DqSEsDSwGU8hDy
```json
{
  "command": "grep -E \"Overfull|Underfull\" /tmp/pdflatex2.log | head -5; echo \"---\"; grep -nE \"^[A-Za-z]+: |\\\\\\\\bibliography|^\\\\\\\\appendix\" /tmp/pdflatex2.log | head -10; echo \"---\"; pdfinfo main.pdf 2>/dev/null | head -10",
  "description": "Get PDF metadata"
}
```

> TOOL

tool_result
id: toolu_01Dx1NASf4DqSEsDSwGU8hDy
```
Underfull \vbox (badness 10000) has occurred while \output is active
Underfull \vbox (badness 10000) has occurred while \output is active [4]
Underfull \hbox (badness 2503) in paragraph at lines 1073--1074
Underfull \vbox (badness 10000) has occurred while \output is active
Underfull \vbox (badness 10000) has occurred while \output is active [31
---
---
Title:           
Subject:         
Keywords:        
Author:          
Creator:         LaTeX with hyperref
Producer:        pdfTeX-1.40.29
CreationDate:    Tue May  5 18:11:43 2026 +07
ModDate:         Tue May  5 18:11:43 2026 +07
Custom Metadata: yes
Metadata Stream: no
```

> TOOL

tool_use Bash
id: toolu_015FnDbiJwyvzmJzWu9pn4EG
```json
{
  "command": "python3 -c \"\nimport subprocess, re\nout = subprocess.check_output(['pdftotext', '-layout', 'main.pdf', '-'], cwd='/Users/hungpq2412/neuralips26').decode('utf-8', 'ignore')\npages = out.split('\\f')\nfor i, p in enumerate(pages[:12], 1):\n    # First 200 chars and last 200 chars\n    head = p.strip().split('\\n')[0] if p.strip() else '<empty>'\n    tail_lines = [l for l in p.strip().split('\\n') if l.strip()][-1:] if p.strip() else ['<empty>']\n    print(f'--- Page {i} ---')\n    print(f'  HEAD: {head[:120]}')\n    print(f'  TAIL: {tail_lines[0][:120] if tail_lines else \\\"<empty>\\\"}')\n\"",
  "description": "Show start/end of first 12 pages"
}
```

> TOOL

tool_result
id: toolu_015FnDbiJwyvzmJzWu9pn4EG
```
--- Page 1 ---
  HEAD: Raw-Routed Mixture of Adapters: A Causal
  TAIL:      Submitted to 40th Conference on Neural Information Processing Systems (NeurIPS 2026). Do not distribute.
--- Page 2 ---
  HEAD: 37   S2 IP-LLM [74] attaches semantic prompts derived from the LLM’s own embedding space, and
  TAIL:                                                        2
--- Page 3 ---
  HEAD: (a)                                                  TSFM adapters use the same head for every window
  TAIL:                                                                                     3
--- Page 4 ---
  HEAD: 131   routing [19], then to vision via V-MoE [80] (the architectural precedent for our cross-modality control
  TAIL:                                                            4
--- Page 5 ---
  HEAD: PATH A: E MBEDDINGS                                             Mean Pool
  TAIL:                                                                       5
--- Page 6 ---
  HEAD: 215   seven-method baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full
  TAIL:                                                           6
--- Page 7 ---
  HEAD: Table 1: Freeze-level ablation (test MSE, mean±std, 3 seeds {42, 43, 44}, H=96). RR-MoA (sparse
  TAIL:                                                                              7
--- Page 8 ---
  HEAD: 263   The Frozen Paradox. If normalization-driven gradient co-adaptation drives collapse, then within
  TAIL:                                                         8
--- Page 9 ---
  HEAD: 315   gates σk (Xraw ) and outperforms RR-MoA by 13–42% on all 6 datasets (252 runs, six backbones;
  TAIL:                                                                 9
--- Page 10 ---
  HEAD: Table 4: Baseline comparison (MOMENT-small, […]

> AGENT

Let me look at §4.2 prose density and apply cuts.

> TOOL

tool_use Read
id: toolu_01R2HAXzB8N2TdVTacw7umim
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 386,
  "limit": 180
}
```

> TOOL

tool_result
id: toolu_01R2HAXzB8N2TdVTacw7umim
```
386	\section{Experiments}
387	
388	\subsection{Setup}
389	
390	\textbf{Datasets and tasks.} Six LTSF benchmarks (ETTh1/h2/m1/m2~\citep{zhou2021informer}, Weather, Electricity~\citep{wu2021autoformer}) spanning hourly to 15-minute sampling and $7$--$321$ channels, with chronological splits and channel-wise normalization~\citep{nie2023patchtst}. We evaluate forecasting at $H{=}96$ primary (multi-horizon in Appendix~\ref{app:horizon}) and $20\%$-masked imputation.
391	
392	\textbf{Backbones.} Five backbones spanning three normalization regimes: (i)~learnable-affine RevIN-inside-encoder MOMENT-small/large~\citep{goswami2024moment} (internal RevIN~\citep{kim2021revin}); (ii)~Moirai~\citep{woo2024moirai} and Moirai-MoE, which use RMSNorm internally with only non-learnable per-instance I/O scaling (no learnable-affine RevIN inside the encoder pipeline); (iii)~Chronos~\citep{ansari2024chronos} (T5-style, no instance normalization) and Timer-XL~\citep{liu2025timerxl} (LayerNorm only, no instance normalization) as no-instance-normalization negative controls (per-backbone normalization specifications in Appendix~\ref{app:setup}, \S\ref{sec:cross_backbone}). The collapse mechanism predicts that only regime~(i) is vulnerable: routing signal is destroyed by RevIN's learnable-affine normalization upstream of the encoder, whereas non-learnable I/O scaling preserves the (M,$\Sigma$) statistics in the hidden states the router reads. MOMENT-small is primary. Primary results use a strictly frozen backbone; freeze-level ablations follow.
393	
394	\textbf{Baselines.} Four tiers, kept separate to avoid confounding frozen-vs-unfrozen and adapter-vs-from-scratch comparisons: \emph{frozen-adapter} (three fixed adapters; $5$-expert independent ensemble; AdaMix~\citep{wang2022adamix}); \emph{frozen PEFT} (LoRA~\citep{hu2022lora}, $108$-run sweep, App.~\ref{app:lora_sweep}; TRACE~\citep{li2025trace}); \emph{unfrozen} (full fine-tuning, all blocks, best of $5$ heads $\times 2$ LRs; extended schedules in App.~\ref{app:extended_ft}); \emph{from-scratch calibration} (DLinear~\citep{zeng2023dlinear}).
395 […]

> DEVELOPER

cuts should not reduce our intext citations

> AGENT

Understood — cuts will preserve every `\citep`/`\citet`. I'll compress prose only (joining sentences, dropping redundant adjectives/parentheticals) while keeping all citation keys.

> TOOL

tool_use Edit
id: toolu_01XpyFn6gUvaGhzvoRs4KW1R
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "Time series foundation models (TSFMs) such as MOMENT~\\citep{goswami2024moment}, TimesFM~\\citep{das2024timesfm}, Chronos~\\citep{ansari2024chronos}, Timer-XL~\\citep{liu2025timerxl,liu2024timer}, and Moirai~\\citep{woo2024moirai} now provide pretrained representations for time series, alongside further pretrained variants~\\citep{lee2024units, rasul2024lagllama, ekambaram2024ttm}, observability-domain TSFMs deployed at scale~\\citep{cohen2025toto}, and continuous flow-matching forecasters such as Sundial~\\citep{liu2025sundial} that bypass tokenization entirely. A parallel adaptation route reprograms pretrained LLMs as forecasters: Time-LLM~\\citep{jin2024timellm} reprograms patch embeddings into the LLM token space, GPT4TS~\\citep{zhou2023onefitsall} freezes the LLM's transformer blocks and tunes only positional and layer-norm parameters, AutoTimes~\\citep{liu2024autotimes} casts forecasting as autoregressive next-token prediction, S$^2$IP-LLM~\\citep{pan2024s2ipllm} attaches semantic prompts derived from the LLM's own embedding space, and UniTime~\\citep{liu2024unitime} unifies cross-domain forecasting via natural-language domain instructions. Recent designs push toward billion-parameter scales~\\citep{shi2024timemoe, liu2026timers1}. Using one of these backbones on a downstream task still requires attaching a lightweight adapter head that maps hidden states to predictions; this paper studies the adapter, holding the backbone fixed.",
  "new_string": "Time series foundation models (TSFMs) such as MOMENT~\\citep{goswami2024moment}, TimesFM~\\citep{das2024timesfm}, Chronos~\\citep{ansari2024chronos}, Timer-XL~\\citep{liu2025timerxl,liu2024timer}, and Moirai~\\citep{woo2024moirai} now provide pretrained representations for time series, alongside further pretrained variants~\\citep{lee2024units, rasul2024lagllama, ekambaram2024ttm}, observability-domain deployments~\\citep{cohen2025toto}, tokenization-free flow-matching forecasters~\\citep{liu2025sundial}, and a parallel route that reprograms pretrained LLMs as forecasters via patch-to-token reprogramming~\\citep{jin2024timellm}, layer-norm-only tuning~\\citep{zhou2023onefitsall}, autoregressive next-token forecasting~\\citep{liu2024autotimes}, semantic […]

> TOOL

tool_result
id: toolu_01XpyFn6gUvaGhzvoRs4KW1R
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01MNWUZfhifq37xL5woVF8WP
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "Standard TSFM adapters apply a lightweight regression head on encoder outputs through the same head for every window (Figure~\\ref{fig:problem_overview}a) -- flatten-then-project for MOMENT~\\citep{goswami2024moment} and PatchTST~\\citep{nie2023patchtst}, an autoregressive residual block for TimesFM~\\citep{das2024timesfm}. Real time series mix heterogeneous regimes (quiet baselines, seasonal excursions, abrupt shape changes), and instance normalization handles only the scale-and-offset component of that heterogeneity; residual \\emph{shape} heterogeneity (periodicity, trends, level shifts, change points) is encoded in the hidden states across layers, as recent probing analyses of MOMENT and related TSFMs have reported~\\citep{wilinski2025tsfm_representations, pandey2025tsfm_semantics}. This residual heterogeneity motivates a per-window mixture of expert adapters: a pool of topologically distinct heads with a learned router that assigns each window to the most suitable one. Keeping the backbone frozen while training only the adapter is also what makes deployment practical: a shared TSFM in GPU memory can serve many tenants through lightweight per-task adapters hot-swapped from host RAM, an arrangement that per-dataset models like DLinear~\\citep{zeng2023dlinear} cannot match (Appendices~\\ref{app:deployment},~\\ref{app:benchmark}).",
  "new_string": "Standard TSFM adapters apply a lightweight regression head on encoder outputs through the same head for every window (Figure~\\ref{fig:problem_overview}a): flatten-then-project for MOMENT~\\citep{goswami2024moment} and PatchTST~\\citep{nie2023patchtst}, an autoregressive residual block for TimesFM~\\citep{das2024timesfm}. Real time […]

> TOOL

tool_result
id: toolu_01MNWUZfhifq37xL5woVF8WP
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01BNR5axjrvU7Pqt3gayL2cM
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "This natural mixture-of-experts approach fails on TSFMs that use instance normalization once any backbone layers are unfrozen (Figure~\\ref{fig:problem_overview}b). When the AdaMix-style adapter pool~\\citep{wang2022adamix} is combined with a learned hidden-state softmax router and Switch-style load balancing~\\citep{fedus2022switch}, and applied to MOMENT with RevIN, routing entropy drops to zero in most unfrozen configurations (Table~\\ref{tab:adamix}). The router learns to send every window to the same expert, and the remaining experts are never used. The mechanism is what we call \\emph{normalization-induced routing collapse}: RevIN~\\citep{kim2021revin} strips the per-window mean and variance that the router needs to distinguish input regimes (formalized in Observation~\\ref{thm:mi_decomp}; signal-ratio diagnostic in Figure~\\ref{fig:signal_ratio}), leaving it with homogenized hidden states. Even with the backbone frozen, hidden-state routing still underperforms; with the backbone unfrozen, the dominant expert receives larger gradients which reshape the backbone to serve it even more, closing a co-adaptation feedback loop within tens of training steps (Figure~\\ref{fig:trajectory}).",
  "new_string": "This natural mixture-of-experts approach fails on TSFMs that use instance normalization once any backbone layers are unfrozen (Figure~\\ref{fig:problem_overview}b). Combining an AdaMix-style adapter pool~\\citep{wang2022adamix} with a learned hidden-state softmax router and Switch-style load balancing~\\citep{fedus2022switch} on MOMENT with RevIN drops routing entropy to zero in […]

> TOOL

tool_result
id: toolu_01BNR5axjrvU7Pqt3gayL2cM
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_0132YGMWrjNywvX6zLse5KSt
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "The failure is specific to learnable-affine instance normalization placed inside the encoder pipeline. Backbones such as Moirai, which apply only non-learnable per-instance I/O scaling and use RMSNorm internally (rather than RevIN-style learnable-affine normalization upstream of the encoder), do not collapse (\\S\\ref{sec:cross_backbone}), and standard MoE rescue mechanisms (load balancing, entropy regularization, z-loss, ReLU routing, expert-choice) recover at most $10.9\\%$ MSE, still $2.7\\times$ worse than RR-MoA (Table~\\ref{tab:rescue}), because the problem lies in the router's \\emph{input}, not its optimization.",
  "new_string": "The failure is specific to learnable-affine instance normalization inside the encoder pipeline: Moirai, which uses only non-learnable per-instance I/O scaling with internal RMSNorm, does not collapse (\\S\\ref{sec:cross_backbone}), and standard MoE rescue mechanisms (load balancing, entropy regularization, z-loss, ReLU routing, expert-choice) recover at most $10.9\\%$ MSE, $2.7\\times$ worse than RR-MoA (Table~\\ref{tab:rescue}): the problem is in the router's \\emph{input}, not its optimization."
}
```

> TOOL

tool_result
id: toolu_0132YGMWrjNywvX6zLse5KSt
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01JZYrqeZn7MiHJYUyhdSqWg
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\item We identify \\emph{normalization-induced routing collapse}: an architectural failure mode of MoE adapters on instance-normalized TSFMs that is upstream of the optimization-induced collapses targeted by Switch~\\citep{fedus2022switch}, ST-MoE~\\citep{zoph2022stmoe}, ReMoE~\\citep{wang2025remoe}, and Expert-Choice~\\citep{zhou2022expertchoice}. Eight causal controls (RevIN ablation, BatchNorm/GroupNorm swaps, router-input interpolation, vision cross-modality, and others) converge on the normalizer as cause.\n\\item We formalize the mechanism via a mutual-information decomposition (Observation~\\ref{thm:mi_decomp}) and derive a tractable signal-ratio predictor $R(\\mathcal{D})$ that anticipates which datasets benefit from raw routing at Spearman $\\rho{=}{-}0.88$ ($p{<}0.002$), including boundary cases where it correctly does not (Traffic, $R{=}0.14$). The predictor generalizes across three normalization families, five backbones, and a vision modality.\n\\item We propose RR-MoA, the \\textbf{minimal causal intervention}: changing only the router's input from normalized hidden states to $\\mathbf{X}_\\text{raw}$, with no change to the optimizer, the experts, or the frozen backbone. RR-MoA wins $54/54$ cells against AdaMix (the same architecture with collapsed routing), strictly dominates $11$ optimization-side rescue mechanisms ($720$ runs; best rescue recovers $\\leq 10.9\\%$, RR-MoA $2.7{\\times}$ better), and is not subsumed by naive $(\\mu,\\sigma)$ re-injection ($+42$--$239\\%$ MSE; $11/18$ cells re-collapse). Two architecturally distinct variants confirm the principle generalizes beyond RR-MoA's specific router: \\textbf{SR-MoA} (self-routed, no external router; outperforms […]

> TOOL

tool_result
id: toolu_01JZYrqeZn7MiHJYUyhdSqWg
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> AGENT

Now compress §4.2 prose without dropping any citation.

> TOOL

tool_use Edit
id: toolu_01NvqThdnVCX1qgCGgi1yRSZ
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "RR-MoA's case rests on three claims: fixed-topology adapters are suboptimal, the natural MoE remedy collapses on instance-normalized backbones, and the collapse cannot be recovered by standard rescue mechanisms. We establish each in turn before comparing against the seven-baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full fine-tuning, DLinear).",
  "new_string": "RR-MoA's case rests on three claims: fixed-topology adapters are suboptimal, the natural MoE remedy collapses on instance-normalized backbones, and standard rescue mechanisms cannot recover it. We establish each before comparing against the seven-baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full fine-tuning, DLinear)."
}
```

> TOOL

tool_result
id: toolu_01NvqThdnVCX1qgCGgi1yRSZ
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01KYqFFF7bm1vnDeELu58yXY
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "{\\looseness=-1 \\textbf{Why does standard MoE routing fail?} We examine AdaMix~\\citep{wang2022adamix} with a learned hidden-state softmax router, an established sparsely-gated MoE recipe~\\citep{fedus2022switch} (Appendix~\\ref{app:adamix_details}). Table~\\ref{tab:adamix} shows AdaMix collapses to a single expert whenever backbone layers are unfrozen: entropy reaches $0.000\\pm0.000$ in 7/12 unfrozen configurations; the remaining 5 stay below $0.55$ (vs.\\ max ${\\approx}1.61$) with $\\sigma$ up to $0.71$, indicating stochastic collapse rather than stable partial routing. The green rows isolate the cause: disabling RevIN inside MOMENT recovers entropy to $0.66$--$1.32$ (BatchNorm1d/GroupNorm produce the same collapse, Appendix~\\ref{app:norm_generalization}). The causal contrast is sharpest cross-backbone (Figure~\\ref{fig:causal_contrast}): under identical last-4 unfreezing on identical data, MOMENT entropy crashes to $0.000$ in ${\\sim}40$ steps while Timer-XL (no RevIN) stays at $1.60$ for $400$ steps, opposite trajectories from the same code.}",
  "new_string": "{\\looseness=-1 \\textbf{Why does standard MoE routing fail?} We examine AdaMix~\\citep{wang2022adamix} with a learned hidden-state softmax router, an established sparsely-gated MoE recipe~\\citep{fedus2022switch} (Appendix~\\ref{app:adamix_details}). Table~\\ref{tab:adamix} shows AdaMix collapses to a single expert whenever backbone layers are unfrozen: entropy reaches $0.000\\pm0.000$ in 7/12 unfrozen configurations; the remaining 5 stay below $0.55$ (max ${\\approx}1.61$) with $\\sigma$ up to $0.71$, indicating stochastic collapse. Disabling RevIN inside MOMENT recovers entropy to $0.66$--$1.32$ […]

> TOOL

tool_result
id: toolu_01KYqFFF7bm1vnDeELu58yXY
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01JdDuwoAzbvuA84hsP26Yg4
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "{\\looseness=-1 \\textbf{The Frozen Paradox.} If normalization-driven gradient co-adaptation drives collapse, then within a fixed MoE architecture frozen should match or beat unfrozen. Empirically, frozen RR-MoA beats \\emph{full fine-tuning} (all 8 blocks, best of 5 heads $\\times$ 2 LRs) by $12$--$79\\%$ on all 6 LTSF datasets (Figure~\\ref{fig:frozen_paradox}). The headline gap (frozen+MoE vs.\\ unfrozen+single-head) decomposes into \\emph{(M1)} an MoE architectural advantage ($26$--$79\\%$, isolated by Table~\\ref{tab:rrmoa} at fixed freeze level) and \\emph{(M2)} a smaller within-architecture freeze effect ($\\leq 13\\%$, non-unidirectional: frozen best on $4/6$, light unfreezing wins by ${\\leq}13\\%$ on the other two; SR-MoA replicates the $4/6$ pattern, Table~\\ref{tab:self_routed}). Proposition~\\ref{prop:frozen} attributes M2 to gradient co-adaptation: a Router-Detached Gradient Flow ablation degrades MSE by $+35$--$100\\%$ (Appendix~\\ref{app:routing_ablations}), and disabling RevIN recovers full-FT by $54$--$61\\%$ (Appendix~\\ref{app:extended_ft}), pinning the mechanism on normalization not optimization. A $90$-config tune (LR $10^{-5}$--$10^{-6}$, $100$ epochs, cosine+warmup, layerwise decay) still loses by $51$--$71\\%$.}",
  "new_string": "{\\looseness=-1 \\textbf{The Frozen Paradox.} If normalization-driven gradient co-adaptation drives collapse, frozen should match or beat unfrozen within a fixed MoE architecture. Frozen RR-MoA beats \\emph{full fine-tuning} (all 8 blocks, best of 5 heads $\\times$ 2 LRs) by $12$--$79\\%$ on all 6 LTSF datasets (Figure~\\ref{fig:frozen_paradox}). The headline gap […]

> TOOL

tool_result
id: toolu_01JdDuwoAzbvuA84hsP26Yg4
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_015G5NaQeP2v5KsqJ1JvqHpw
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\textbf{Why RevIN destroys routing.} Each window decomposes into mean $M_i$, scale $\\Sigma_i$, shape $\\mathbf{S}_i = (\\mathbf{x}_i - M_i)/\\Sigma_i$; RevIN keeps $\\mathbf{S}_i$ and discards $(M_i,\\Sigma_i)$. The chain rule quantifies how much routing signal lives in the discarded part.",
  "new_string": "\\textbf{Why RevIN destroys routing.} Each window decomposes into mean $M_i$, scale $\\Sigma_i$, shape $\\mathbf{S}_i = (\\mathbf{x}_i - M_i)/\\Sigma_i$; RevIN keeps $\\mathbf{S}_i$ and discards $(M_i,\\Sigma_i)$. The chain rule quantifies the routing signal in the discarded part."
}
```

> TOOL

tool_result
id: toolu_015G5NaQeP2v5KsqJ1JvqHpw
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01FWQt7wUYLcRA5vdNU6eiSa
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "{\\looseness=-1 Two distinct gains feed the headline: residual shape heterogeneity rewards diverse experts on RevIN-normalized hidden states (Q1; $26$--$79\\%$ over the best fixed adapter, Table~\\ref{tab:rrmoa}), while the signal-ratio $\\rho{=}{-}0.88$ localizes \\emph{dispatch} information in the stripped statistics (Q2; explains both raw-routing benefit and Traffic's correct null result). The Pure Raw-MLP MoE ablation (Appendix~\\ref{app:raw_mlp_moe}) separates ``MoE with raw router'' from ``ensemble with raw input''.}",
  "new_string": "{\\looseness=-1 Two gains feed the headline: residual shape heterogeneity rewards diverse experts on RevIN-normalized hidden states (Q1; $26$--$79\\%$ over the best fixed adapter, Table~\\ref{tab:rrmoa}); the signal-ratio $\\rho{=}{-}0.88$ localizes \\emph{dispatch} information in the stripped statistics (Q2; explains both raw-routing benefit and Traffic's null). The Pure Raw-MLP MoE ablation (Appendix~\\ref{app:raw_mlp_moe}) separates ``MoE with raw router'' from ``ensemble with raw input''.}"
}
```

> TOOL

tool_result
id: toolu_01FWQt7wUYLcRA5vdNU6eiSa
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> AGENT

Now rebuild and check pagination.

> TOOL

tool_use Bash
id: toolu_01VTjo4PzSBqL8ZCs4aMzuee
```json
{
  "command": "pdflatex -interaction=nonstopmode -draftmode main.tex > /tmp/p1.log 2>&1 && pdflatex -interaction=nonstopmode main.tex > /tmp/p2.log 2>&1; echo \"EXIT=$?\"; tail -3 /tmp/p2.log",
  "description": "Rebuild after intro+results compression"
}
```

> TOOL

tool_result
id: toolu_01VTjo4PzSBqL8ZCs4aMzuee
```
EXIT=0
026basic/texmf-dist/fonts/type1/urw/times/utmri8a.pfb>
Output written on main.pdf (51 pages, 883289 bytes).
Transcript written on main.log.
```

> TOOL

tool_use Bash
id: toolu_01TfCuq9DhEw3ojCexHVmbiQ
```json
{
  "command": "python3 -c \"\nimport subprocess\nout = subprocess.check_output(['pdftotext', '-layout', 'main.pdf', '-']).decode('utf-8','ignore')\npages = out.split('\\f')\nfor i, p in enumerate(pages[:11], 1):\n    head = p.strip().split('\\n')[0] if p.strip() else '<empty>'\n    print(f'p{i}: {head[:100]}')\n\"",
  "description": "Check page boundaries after first cuts"
}
```

> TOOL

tool_result
id: toolu_01TfCuq9DhEw3ojCexHVmbiQ
```
p1: Raw-Routed Mixture of Adapters: A Causal
p2: 37   still requires attaching a lightweight adapter head that maps hidden states to predictions; thi
p3: (a)                                                  TSFM adapters use the same head for every windo
p4: 127   time series, MoE has been used within TSFM backbones to scale capacity, with experts placed
p5: PATH A: E MBEDDINGS                                             Mean Pool
p6: 206   4     Experiments
p7: Table 1: Freeze-level ablation (test MSE, mean±std, 3 seeds {42, 43, 44}, H=96). RR-MoA (sparse
p8: 256   other two; SR-MoA replicates 4/6, Table F.2). Proposition 1 attributes M2 to gradient co-adapt
p9: Table 3: Eight causal controls. Each rules out a competing explanation; the only mechanism
p10: 319   backbones (Appendix P.1); SR-RIA+ hits 6/6 (Appendix P.2); a TSFM-free Pure Raw-MLP MoE
p11: 369    [8] Xu Liu, Juncheng Liu, Gerald Woo, Taha Aksu, Yuxuan Liang, Roger Zimmermann, Chenghao
```

> TOOL

tool_use Read
id: toolu_01RU4hBdxKKrzXw4KPcaCawN
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 238,
  "limit": 150
}
```

> TOOL

tool_result
id: toolu_01RU4hBdxKKrzXw4KPcaCawN
```
238	\section{Raw-Routed Mixture of Adapters (RR-MoA)}
239	\label{sec:method}
240	
241	\begin{figure}[t!]
242	\centering
243	\resizebox{\columnwidth}{!}{%
244	\begin{tikzpicture}[
245	    >=Stealth,
246	    % -- Node styles --
247	    box/.style={rectangle, draw=black!70, rounded corners=2pt, fill=white,
248	        minimum height=0.75cm, font=\small, align=center, line width=0.7pt},
249	    frozenbox/.style={box, draw=blue!60, fill=blue!4, minimum width=2.6cm, minimum height=1.4cm},
250	    gatebox/.style={box, draw=orange!70, fill=orange!4, minimum width=2.0cm, minimum height=0.9cm},
251	    hiddenbox/.style={box, draw=blue!50, fill=blue!3, minimum width=1.4cm},
252	    topkbox/.style={box, draw=orange!60, fill=orange!3, minimum width=1.3cm},
253	    expertactive/.style={box, draw=orange!75!black, fill=orange!18, line width=1.0pt, minimum width=2.0cm, minimum height=0.65cm, font=\small\bfseries, text=black},
254	    expertinactive/.style={box, draw=gray!45, fill=gray!8, minimum width=2.0cm, minimum height=0.65cm, font=\small, text=black},
255	    sumnode/.style={circle, draw=black!70, fill=white, minimum size=0.65cm, font=\normalsize, line width=0.7pt},
256	    outputbox/.style={box, draw=teal!60, fill=teal!4, minimum width=1.2cm},
257	    % -- Arrow styles --
258	    bluearr/.style={->, line width=0.8pt, color=blue!55},
259	    orangearr/.style={->, line width=0.8pt, color=orange!70},
260	    dashedarr/.style={->, line width=0.8pt, color=orange!70, densely dashed},
261	    grayarr/.style={->, line width=0.7pt, color=gray!50},
262	    outarr/.style={->, line width=0.8pt, color=teal!60},
263	]
264	
265	% ====== INPUT (left) ======
266	\node[box, minimum width=1.4cm, minimum height=1.0cm] (input) at (0, 0) {
267	    $\mathbf{X}_\mathrm{raw}$\\[-2pt]
268	    {\scriptsize raw input}\\[-2pt]
269	    {\scriptsize 512 steps}
270	};
271	
272	% ====== PATH A: FROZEN TSFM (top) ======
273	\node[frozenbox] (tsfm) at (3.5, 1.8) {
274	    \textbf{Frozen TSFM}\\[-1pt]
275	    \textbf{Backbone}\\[-1pt]
276	    {\scriptsize\color{red!60} no gradients}
277	}; […]

> TOOL

tool_use Edit
id: toolu_01MjgZhVTrH6W2kxbnEUTiuM
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "An \\emph{adapter} $g_\\phi: \\mathbb{R}^{B \\times T \\times d} \\rightarrow \\mathbb{R}^{B \\times h}$ maps a pretrained backbone's hidden states (batch $B$, sequence length $T$, hidden dim $d$) to forecasts of horizon $h$, with $n_g \\leq 500{,}000$ trainable parameters. (We use lowercase $h$ for forecast horizon to disambiguate from $\\mathbf{H}_\\mathrm{FM}$ below, the backbone hidden state.) The goal of per-window routing is to select, for each input window, the subset of expert adapters best suited to that window's characteristics, so that a quiet baseline and a volatile spike are handled by different adapter topologies rather than forced through the same head. As shown in the introduction, this fails when the router reads normalized hidden states, because RevIN removes the per-window statistics that distinguish input regimes. \\textbf{RR-MoA} avoids this by splitting the information into two streams: the frozen TSFM produces deep embeddings $\\mathbf{H}$ for the experts, while a separate lightweight gate reads the \\textit{raw, pre-normalization} input $\\mathbf{X}_\\text{raw}$ to decide which experts to activate:",
  "new_string": "An \\emph{adapter} $g_\\phi: \\mathbb{R}^{B \\times T \\times d} \\rightarrow \\mathbb{R}^{B \\times h}$ maps a pretrained backbone's hidden states (batch $B$, sequence length $T$, hidden dim $d$) to forecasts of […]

> TOOL

tool_result
id: toolu_01MjgZhVTrH6W2kxbnEUTiuM
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01XKv8qNiXdWQEhVLutmppBi
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "where $G_\\psi: \\mathbb{R}^{T} \\to \\mathbb{R}^K$ is a small Conv1d\\,+\\,pooling\\,+\\,linear gate ($853$ params) operating directly on the raw time series, $\\mathcal{T} \\subset \\{1,\\ldots,K\\}$ is the set of Top-$k$ expert indices, and each $\\mathrm{Expert}_j$ is a canonical adapter head. By construction $\\sum_j \\widetilde{w}_j = 1$ with support only on $\\mathcal{T}$, so only $k$ of $K$ experts contribute per sample (the remaining $K{-}k$ are masked out and do not execute). With $K{=}5$, $k{=}2$ we obtain $40\\%$ of the dense ($k{=}K$) expert FLOPs while retaining $63\\%$ of the dense MSE improvement over the best fixed adapter (\\S\\ref{sec:topk}). The raw input preserves the temporal statistics (trend, amplitude, volatility) that RevIN strips away, enabling per-sample routing that reflects the physical characteristics of each time series window.",
  "new_string": "where $G_\\psi: \\mathbb{R}^{T} \\to \\mathbb{R}^K$ is a small Conv1d\\,+\\,pooling\\,+\\,linear gate ($853$ params) operating directly on the raw time series, $\\mathcal{T} \\subset \\{1,\\ldots,K\\}$ is the set of Top-$k$ indices, and each $\\mathrm{Expert}_j$ is a canonical adapter head. By construction $\\sum_j \\widetilde{w}_j = 1$ with support only on $\\mathcal{T}$, so only $k$ of $K$ experts execute per sample. With $K{=}5$, $k{=}2$ we obtain $40\\%$ of the dense expert FLOPs while […]

> TOOL

tool_result
id: toolu_01XKv8qNiXdWQEhVLutmppBi
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01CF84352VVP8nwY4EC8VuoV
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\textbf{Expert pool.} We maintain $K{=}5$ topologically distinct expert adapters (mean-pool, last-token, max-pool, attention-pool, Conv1d-pool), spanning pooling families recently shown to span distinct expressivity regimes for transformer-based sequence models across NLP, vision, and time series~\\citep{ennadir2025pooling}. Architectural diversity is critical: replacing the five distinct heads with five identical experts (same topology, different initialization) degrades MSE by $8$--$15\\%$ (Appendix~\\ref{app:diversity}). Pseudocode in Algorithm~\\ref{alg:rrmoa} (Appendix~\\ref{app:setup}). We now empirically validate that this targeted fix recovers routing diversity, beats the seven-method baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full fine-tuning, DLinear), and that its predictions hold under eight causal controls.",
  "new_string": "\\textbf{Expert pool.} We maintain $K{=}5$ topologically distinct expert adapters (mean-pool, last-token, max-pool, attention-pool, Conv1d-pool), spanning pooling families with distinct expressivity regimes for transformer-based sequence models~\\citep{ennadir2025pooling}. Architectural diversity is critical: five identical experts (same topology, different initialization) degrade MSE by $8$--$15\\%$ (Appendix~\\ref{app:diversity}). Pseudocode in Algorithm~\\ref{alg:rrmoa} (Appendix~\\ref{app:setup}). We now validate that this fix recovers routing diversity, beats the seven-method baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full fine-tuning, DLinear), and holds under eight causal controls."
}
```

> TOOL

tool_result
id: toolu_01CF84352VVP8nwY4EC8VuoV
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> AGENT

Now compress the §4.2 closing paragraphs.

> TOOL

tool_use Edit
id: toolu_01RNCxexjFkQarczwhZwgHWX
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "RR-MoA beats every baseline at $p{<}0.001$; the no-router independent ensemble is $37$--$46\\%$ worse. \\textbf{Closing the DLinear gap.} DLinear (49K params, from scratch) outperforms frozen adapters in absolute MSE (Table~\\ref{tab:baselines}, grey rows); k-NN/Ridge diagnostics attribute this to information loss in the normalization--encoding pipeline (Appendix~\\ref{app:diagnostic}). Restoring raw access \\emph{at the expert level} closes it: \\textbf{Residual-IA\\textsuperscript{+}} matches or beats DLinear on $6/6$ datasets at $H{=}96$ and $107/123$ cells across six backbones (Appendix~\\ref{app:gate_pathology}); SR-RIA\\textsuperscript{+} hits $6/6$ (Appendix~\\ref{app:sr_ria}); a TSFM-free Pure Raw-MLP MoE localizes the TSFM's contribution (Appendix~\\ref{app:raw_mlp_moe}).\n\n{\\looseness=-1 \\textbf{Cross-backbone, task, horizon.}\\label{sec:cross_backbone}\\label{sec:topk} RR-MoA wins on every instance-normalized backbone (MOMENT-small/large $26$--$79\\%/32$--$75\\%$, Moirai $12$--$29\\%$, Moirai-MoE~\\citep{liu2025moiraimoe} $37$--$90\\%$); LayerNorm-only Chronos and Timer-XL~\\citep{liu2025timerxl} show no collapse. Top-$2$, imputation ($7/8$), $24/24$ horizons, and Residual-IA\\textsuperscript{+} ($6{\\times}5{\\times}4$) confirm robustness (Tables~\\ref{tab:cross_backbone}--\\ref{tab:horizon}; Appendices~\\ref{app:topk},~\\ref{app:imputation},~\\ref{app:gate_pathology}).}",
  "new_string": "RR-MoA beats every baseline at $p{<}0.001$; the no-router independent ensemble is $37$--$46\\%$ worse. \\textbf{Closing the DLinear gap.} DLinear (49K params, from scratch) outperforms frozen adapters in absolute MSE (Table~\\ref{tab:baselines}, grey rows); k-NN/Ridge diagnostics attribute this to information loss in the normalization--encoding pipeline (Appendix~\\ref{app:diagnostic}). Restoring raw access \\emph{at the expert level} closes it: \\textbf{Residual-IA\\textsuperscript{+}} matches or beats DLinear on $6/6$ datasets at $H{=}96$ and $107/123$ cells across six backbones (Appendix~\\ref{app:gate_pathology}); SR-RIA\\textsuperscript{+} hits […]

> TOOL

tool_result
id: toolu_01RNCxexjFkQarczwhZwgHWX
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01CCgqJXQGnLZ57W79nGybHa
```json
{
  "command": "pdflatex -interaction=nonstopmode -draftmode main.tex > /tmp/p1.log 2>&1 && pdflatex -interaction=nonstopmode main.tex > /tmp/p2.log 2>&1; tail -2 /tmp/p2.log; python3 -c \"\nimport subprocess\nout = subprocess.check_output(['pdftotext', '-layout', 'main.pdf', '-']).decode('utf-8','ignore')\npages = out.split('\\f')\nfor i, p in enumerate(pages[:11], 1):\n    head = p.strip().split('\\n')[0] if p.strip() else '<empty>'\n    print(f'p{i}: {head[:100]}')\n\"",
  "description": "Rebuild and check pagination"
}
```

> TOOL

tool_result
id: toolu_01CCgqJXQGnLZ57W79nGybHa
```
Output written on main.pdf (51 pages, 882385 bytes).
Transcript written on main.log.
p1: Raw-Routed Mixture of Adapters: A Causal
p2: 37   still requires attaching a lightweight adapter head that maps hidden states to predictions; thi
p3: (a)                                                  TSFM adapters use the same head for every windo
p4: 127   time series, MoE has been used within TSFM backbones to scale capacity, with experts placed
p5: PATH A: E MBEDDINGS                                             Mean Pool
p6: 207   Backbones. Five backbones spanning three normalization regimes: (i) learnable-affine RevIN-ins
p7: Table 2: AdaMix routing collapse (entropy max ≈1.609). Under unfreezing, entropy →0.000.
p8: 260   to flip sign across input regimes, i.e., expert specialization, which is satisfied by the topo
p9: Table 3: Eight causal controls. Each rules out a competing explanation; the only mechanism
p10: 311   absolute MSE (Table 4, grey rows); k-NN/Ridge diagnostics attribute this to information loss i
p11: 361    [7] Gerald Woo, Chenghao Liu, Akshat Kumar, Caiming Xiong, Silvio Savarese, and Doyen Sahoo.
```

> TOOL

tool_use Bash
id: toolu_017RwZNCS4YaepYm9VGVr2zp
```json
{
  "command": "python3 -c \"\nimport subprocess\nout = subprocess.check_output(['pdftotext', '-layout', 'main.pdf', '-']).decode('utf-8','ignore')\npages = out.split('\\f')\nprint('=== PAGE 9 last 15 lines ===')\nprint('\\n'.join([l for l in pages[8].split('\\n') if l.strip()][-15:]))\nprint()\nprint('=== PAGE 10 first 20 lines ===')\nprint('\\n'.join([l for l in pages[9].split('\\n') if l.strip()][:20]))\n\"",
  "description": "Inspect page-9/page-10 boundary"
}
```

> TOOL

tool_result
id: toolu_017RwZNCS4YaepYm9VGVr2zp
```
=== PAGE 9 last 15 lines ===
anchors.
     Method                                         ETTh1                    ETTm1                 Weather           p-value
     Best fixed adapter                        1.254 ± 0.026            1.148 ± 0.035          0.528 ± 0.018       <0.001∗∗∗
     Best LoRA (108-run sweep)                 1.154 ± 0.000            0.956 ± 0.072          0.600 ± 0.052       <0.001∗∗∗
     TRACE (frozen)                            1.195 ± 0.026            1.014 ± 0.073          0.457 ± 0.015       <0.001∗∗∗
     Ind. Ensemble (5 experts)                 1.081 ± 0.021            1.049 ± 0.032          0.509 ± 0.024       <0.001∗∗∗
     AdaMix (frozen)                           1.109 ± 0.031            1.008 ± 0.012          0.459 ± 0.017       <0.001∗∗∗
     Full fine-tuning (all unfrozen)           1.060 ± 0.059            0.871 ± 0.029          0.468 ± 0.009       <0.001∗∗∗
     RR-MoA (Top-2, frozen)                    0.680 ± 0.027            0.564 ± 0.059         0.276 ± 0.017             —
     DLinear (from scratch)                    0.416 ± 0.002            0.322 ± 0.004          0.208 ± 0.003            —
     PatchTST/64† [13]                             0.370                    0.274                  0.149                —
     iTransformer‡ [14]                            0.386                    0.334                  0.174                —
      †
          Trained from scratch, L=512; ‡ trained from scratch, L=96. Included for absolute MSE context.
                                                                    9

=== PAGE 10 first 20 lines ===
311   absolute MSE (Table 4, grey rows); k-NN/Ridge diagnostics attribute this to information loss in
312   the normalization–encoding pipeline (Appendix M). Restoring raw access at the expert level closes
313   it: Residual-IA+ matches or beats DLinear on 6/6 datasets at H=96 and 107/123 […]

> TOOL

tool_use Read
id: toolu_013dvAN2mdwe2UrzQceA45yZ
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 563,
  "limit": 25
}
```

> TOOL

tool_result
id: toolu_013dvAN2mdwe2UrzQceA45yZ
```
563	\vspace{-0.5em}
564	\section{Conclusion and Limitations}
565	\vspace{-0.4em}
566	
567	\textbf{Diagnosis and fix.} We identified \emph{normalization-induced routing collapse}: MoE adapters on instance-normalized TSFMs collapse to a single expert because the same per-window normalization handling distribution shift also strips the $(\mu,\sigma)$ statistics the router needs. Observation~\ref{thm:mi_decomp} formalizes the loss as a mutual-information gap, $R(\mathcal{D})$ predicts it at $\rho{=}{-}0.88$ ($p{<}0.002$), and eight causal controls (Table~\ref{tab:causal_controls}) rule out optimization, geometry, and routing-paradigm explanations. Three architecturally distinct interventions confirm the diagnosis: RR-MoA wins $54/54$ cells ($26$--$79\%$); SR-MoA drops the external router and beats RR-MoA by $13$--$42\%$; Residual-IA\textsuperscript{+} closes the DLinear gap on $107/123$ cross-backbone cells. The mechanism replicates on ResNet/ViT MoE with InstanceNorm (Appendix~\ref{app:vision_moe}) and is absent from LayerNorm-only Timer-XL ($4$--$9\%$, $15$--$100{\times}$ smaller).
568	
569	\textbf{Limitations and outlook.} The diagnosis is specific to per-window normalizers that strip $(\mu,\sigma)$ (RevIN, BatchNorm1d, GroupNorm, InstanceNorm); LayerNorm- and RMSNorm-only backbones need no fix. $R(\mathcal{D})$ is a monotone proxy, not a sharp threshold; intermediate-$R$ behavior at varying freeze levels is open. Evaluation covers forecasting and imputation; classification and anomaly detection remain. The fix needs raw input at routing time (available in adapter-style finetuning, not API-served models); the pool is fixed at five hand-coded experts (learned […]

> TOOL

tool_use Edit
id: toolu_01THpEuy2unxPtQTf1DE7vvx
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\textbf{Diagnosis and fix.} We identified \\emph{normalization-induced routing collapse}: MoE adapters on instance-normalized TSFMs collapse to a single expert because the same per-window normalization handling distribution shift also strips the $(\\mu,\\sigma)$ statistics the router needs. Observation~\\ref{thm:mi_decomp} formalizes the loss as a mutual-information gap, $R(\\mathcal{D})$ predicts it at $\\rho{=}{-}0.88$ ($p{<}0.002$), and eight causal controls (Table~\\ref{tab:causal_controls}) rule out optimization, geometry, and routing-paradigm explanations. Three architecturally distinct interventions confirm the diagnosis: RR-MoA wins $54/54$ cells ($26$--$79\\%$); SR-MoA drops the external router and beats RR-MoA by $13$--$42\\%$; Residual-IA\\textsuperscript{+} closes the DLinear gap on $107/123$ cross-backbone cells. The mechanism replicates on ResNet/ViT MoE with InstanceNorm (Appendix~\\ref{app:vision_moe}) and is absent from LayerNorm-only Timer-XL ($4$--$9\\%$, $15$--$100{\\times}$ smaller).\n\n\\textbf{Limitations and outlook.} The diagnosis is specific to per-window normalizers that strip $(\\mu,\\sigma)$ (RevIN, BatchNorm1d, GroupNorm, InstanceNorm); LayerNorm- and RMSNorm-only backbones need no fix. $R(\\mathcal{D})$ is a monotone proxy, not a sharp threshold; intermediate-$R$ behavior at varying freeze levels is open. Evaluation covers forecasting and imputation; classification and anomaly detection remain. The fix needs raw input at routing time (available in adapter-style finetuning, not API-served models); the pool is fixed at five hand-coded experts (learned pools are open). $R(\\mathcal{D})$ is portable: […]

> TOOL

tool_result
id: toolu_01THpEuy2unxPtQTf1DE7vvx
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_011dbgVM8BnTXhL5YhFbtwKS
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "RR-MoA beats every baseline at $p{<}0.001$; the no-router independent ensemble is $37$--$46\\%$ worse. \\textbf{Closing the DLinear gap.} DLinear (49K params, from scratch) outperforms frozen adapters in absolute MSE (Table~\\ref{tab:baselines}, grey rows); k-NN/Ridge diagnostics attribute this to information loss in the normalization--encoding pipeline (Appendix~\\ref{app:diagnostic}). Restoring raw access \\emph{at the expert level} closes it: \\textbf{Residual-IA\\textsuperscript{+}} matches or beats DLinear on $6/6$ datasets at $H{=}96$ and $107/123$ cells across six backbones (Appendix~\\ref{app:gate_pathology}); SR-RIA\\textsuperscript{+} hits $6/6$ (Appendix~\\ref{app:sr_ria}); a TSFM-free Pure Raw-MLP MoE localizes the TSFM contribution (Appendix~\\ref{app:raw_mlp_moe}).\n\n{\\looseness=-1 \\textbf{Cross-backbone, task, horizon.}\\label{sec:cross_backbone}\\label{sec:topk} RR-MoA wins on every instance-normalized backbone (MOMENT-small/large $26$--$79\\%/32$--$75\\%$, Moirai $12$--$29\\%$, Moirai-MoE~\\citep{liu2025moiraimoe} $37$--$90\\%$); LayerNorm-only Chronos and Timer-XL~\\citep{liu2025timerxl} show no collapse. Top-$2$, imputation ($7/8$), $24/24$ horizons, and Residual-IA\\textsuperscript{+} ($6{\\times}5{\\times}4$) confirm robustness (Tables~\\ref{tab:cross_backbone}--\\ref{tab:horizon}; App.~\\ref{app:topk},~\\ref{app:imputation},~\\ref{app:gate_pathology}).}",
  "new_string": "RR-MoA beats every baseline at $p{<}0.001$; the no-router ensemble is $37$--$46\\%$ worse. \\textbf{Closing the DLinear gap.} DLinear (49K params, from scratch) outperforms frozen adapters in absolute MSE (Table~\\ref{tab:baselines}, grey rows); k-NN/Ridge diagnostics attribute this to information loss in the normalization--encoding pipeline (Appendix~\\ref{app:diagnostic}). Restoring raw access \\emph{at the expert level} closes it: \\textbf{Residual-IA\\textsuperscript{+}} matches or beats DLinear on $6/6$ datasets at $H{=}96$ and $107/123$ cells across six backbones (App.~\\ref{app:gate_pathology}); SR-RIA\\textsuperscript{+} hits $6/6$ […]

> TOOL

tool_result
id: toolu_011dbgVM8BnTXhL5YhFbtwKS
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01MkGiDL9v44RcQfq1iAmzg5
```json
{
  "command": "pdflatex -interaction=nonstopmode -draftmode main.tex > /tmp/p1.log 2>&1 && pdflatex -interaction=nonstopmode main.tex > /tmp/p2.log 2>&1; tail -2 /tmp/p2.log; python3 -c \"\nimport subprocess\nout = subprocess.check_output(['pdftotext', '-layout', 'main.pdf', '-']).decode('utf-8','ignore')\npages = out.split('\\f')\nfor i, p in enumerate(pages[:11], 1):\n    head = p.strip().split('\\n')[0] if p.strip() else '<empty>'\n    print(f'p{i}: {head[:100]}')\nprint()\nprint('=== p9 last 8 ===')\nprint('\\n'.join([l for l in pages[8].split('\\n') if l.strip()][-8:]))\nprint('=== p10 first 12 ===')\nprint('\\n'.join([l for l in pages[9].split('\\n') if l.strip()][:12]))\n\"",
  "description": "Rebuild and re-check pagination"
}
```

> TOOL

tool_result
id: toolu_01MkGiDL9v44RcQfq1iAmzg5
```
Output written on main.pdf (51 pages, 882294 bytes).
Transcript written on main.log.
p1: Raw-Routed Mixture of Adapters: A Causal
p2: 37   still requires attaching a lightweight adapter head that maps hidden states to predictions; thi
p3: (a)                                                  TSFM adapters use the same head for every windo
p4: 127   time series, MoE has been used within TSFM backbones to scale capacity, with experts placed
p5: PATH A: E MBEDDINGS                                             Mean Pool
p6: 207   Backbones. Five backbones spanning three normalization regimes: (i) learnable-affine RevIN-ins
p7: Table 2: AdaMix routing collapse (entropy max ≈1.609). Under unfreezing, entropy →0.000.
p8: 260   to flip sign across input regimes, i.e., expert specialization, which is satisfied by the topo
p9: Table 3: Eight causal controls. Each rules out a competing explanation; the only mechanism
p10: 311   (Table 4, grey rows); k-NN/Ridge diagnostics attribute this to information loss in the normali
p11: 361    [7] Gerald Woo, Chenghao Liu, Akshat Kumar, Caiming Xiong, Silvio Savarese, and Doyen Sahoo.

=== p9 last 8 ===
     Full fine-tuning (all unfrozen)           1.060 ± 0.059            0.871 ± 0.029          0.468 ± 0.009       <0.001∗∗∗
     RR-MoA (Top-2, frozen)                    0.680 ± 0.027            0.564 ± 0.059         0.276 ± 0.017             —
     DLinear (from scratch)                    0.416 ± […]

> AGENT

The remaining 18 lines on page 10 need to migrate to page 9. Page 9 holds two tables (causal controls + baselines). Cleanest move: relocate Table 3 (causal controls) to the appendix and replace with a one-sentence prose summary, keeping the same `\ref{tab:causal_controls}` so all in-text references resolve.

> TOOL

tool_use Read
id: toolu_01JzACM2GmtR8BAqAR5uwLMZ
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 1373,
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_01JzACM2GmtR8BAqAR5uwLMZ
```
1373	\section{Routing Ablations}
1374	\label{app:routing_ablations}
1375	
1376	We isolate which property of the raw-input router is doing the work via two ablations: (i) replace the router's raw input with the RevIN-normalized version of the same signal, holding everything else fixed, and (ii) shuffle the temporal ordering inside each window before feeding it to the router. Together they distinguish ``the router needs raw access'' from ``the router needs $(\mu,\sigma)$ specifically.''
1377	
1378	\begin{table}[!htbp]
1379	\centering
1380	\caption{\textbf{Rawness vs.\ bypass} (frozen, Top-2, 3 seeds). RevIN router reads the same input after per-window normalization. Stripping statistics degrades MSE by 60--88\%.}
1381	\label{tab:router_input}
1382	\small
1383	\begin{tabular}{@{}lccc@{}}
1384	\toprule
1385	Dataset & Raw router (main) & RevIN router & Degradation ($\Delta\%$, $\uparrow$ worse) \\
1386	\midrule
1387	ETTh1   & $\mathbf{0.690 \pm 0.021}$ & $1.101 \pm 0.008$ & $\mathbf{+59.6\%}$ \\
1388	ETTm1   & $\mathbf{0.571 \pm 0.073}$ & $1.077 \pm 0.020$ & $\mathbf{+88.6\%}$ \\
1389	Weather & $\mathbf{0.289 \pm 0.008}$ & $0.542 \pm 0.026$ & $\mathbf{+87.5\%}$ \\
1390	\bottomrule
1391	\end{tabular}
1392	\end{table}
1393	
1394	\definecolor{srback}{RGB}{33,118,189}
1395	\definecolor{srraw}{RGB}{46,139,87}
1396	\definecolor{srgate}{RGB}{217,119,49}
1397	\definecolor{srout}{RGB}{38,166,154}
1398	
1399	\begin{figure}[!htbp]
1400	\centering
1401	\resizebox{0.95\columnwidth}{!}{%
1402	\begin{tikzpicture}[
```

> TOOL

tool_use Edit
id: toolu_01UYgq9ftvyKVxcj1wSVXLwQ
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\textbf{The principle is architecture-agnostic.} Three router-level controls validate that any router reading raw input suffices. \\textbf{SR-MoA} (Figure~\\ref{fig:srmoa_arch}; cf.~\\citealp{lv2025aoe,liu2026routingfree,cheng2025ermoe}) drops the external router for per-expert sigmoid gates $\\sigma_k(\\mathbf{X}_\\mathrm{raw})$ and \\emph{outperforms} RR-MoA by $13$--$42\\%$ on all 6 datasets ($252$ runs, six backbones; Table~\\ref{tab:self_routed}), also replicating the Frozen Paradox ($4/6$). Gating the same architecture on hidden states degrades by $+87$--$768\\%$ ($p{=}0.016$); on Timer-XL the same comparison yields only $+4$--$9\\%$, $15$--$100{\\times}$ smaller. \\textbf{AdaMix-Raw} (Appendix~\\ref{app:adamix_details}) swaps AdaMix's router input only and recovers entropy to $1.41$--$1.57$ and MSE by $41$--$88\\%$ on all 12 cells. \\textbf{Residual-IA\\textsuperscript{+}} (Appendix~\\ref{app:gate_pathology}, Figure~\\ref{fig:residual_ia_arch}) extends the principle to the expert level (shared NLinear raw branch + gated backbone residual). Table~\\ref{tab:causal_controls} summarizes all eight controls.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{\\textbf{Eight causal controls.} Each rules out a competing explanation; the only mechanism consistent with all 8 is that \\emph{instance normalization strips the per-window $(\\mu,\\sigma)$ signal the router needs}.}\n\\label{tab:causal_controls}\n\\footnotesize\n\\setlength{\\tabcolsep}{4pt}\n\\begin{tabular}{@{}cl >{\\raggedright\\arraybackslash}p{3.3cm} >{\\raggedright\\arraybackslash}p{5.95cm}@{}}\n\\toprule\n\\# & \\textbf{Control} & \\textbf{Hypothesis (rejected)} & \\textbf{Observed result} $\\Rightarrow$ \\textbf{verdict} \\\\\n\\midrule\nC1 & RevIN ablation & Collapse is intrinsic to MoE itself, not caused by normalization & Entropy $0.000 \\to 0.66$--$1.32$ when RevIN disabled (Table~\\ref{tab:adamix}) {\\small$\\Rightarrow$} RevIN is \\emph{necessary} for collapse \\\\\nC2 & MOMENT vs Timer-XL & Architecture, not normalization, […]

> TOOL

tool_result
id: toolu_01UYgq9ftvyKVxcj1wSVXLwQ
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> AGENT

Now insert the moved Table 3 (with its label) at the start of the routing-ablations appendix.

> TOOL

tool_use Edit
id: toolu_012rJxG8BCb2opWe87h9N3K5
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\section{Routing Ablations}\n\\label{app:routing_ablations}\n\nWe isolate which property of the raw-input router is doing the work via two ablations: (i) replace the router's raw input with the RevIN-normalized version of the same signal, holding everything else fixed, and (ii) shuffle the temporal ordering inside each window before feeding it to the router. Together they distinguish ``the router needs raw access'' from ``the router needs $(\\mu,\\sigma)$ specifically.''",
  "new_string": "\\section{Routing Ablations}\n\\label{app:routing_ablations}\n\\label{app:causal_controls}\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{\\textbf{Eight causal controls.} Each rules out a competing explanation; the only mechanism consistent with all 8 is that \\emph{instance normalization strips the per-window $(\\mu,\\sigma)$ signal the router needs}.}\n\\label{tab:causal_controls}\n\\footnotesize\n\\setlength{\\tabcolsep}{4pt}\n\\begin{tabular}{@{}cl >{\\raggedright\\arraybackslash}p{3.3cm} >{\\raggedright\\arraybackslash}p{5.95cm}@{}}\n\\toprule\n\\# & \\textbf{Control} & \\textbf{Hypothesis (rejected)} & \\textbf{Observed result} $\\Rightarrow$ \\textbf{verdict} \\\\\n\\midrule\nC1 & RevIN ablation & Collapse is intrinsic to MoE itself, not caused by normalization & Entropy $0.000 \\to 0.66$--$1.32$ when RevIN disabled (Table~\\ref{tab:adamix}) {\\small$\\Rightarrow$} RevIN is \\emph{necessary} for collapse \\\\\nC2 & MOMENT vs Timer-XL & Architecture, not normalization, causes collapse & Opposite trajectories with identical code, only norm differs (Fig.~\\ref{fig:causal_contrast}) {\\small$\\Rightarrow$} normalization is \\emph{sufficient} \\\\\nC3 & BatchNorm1d / GroupNorm & Collapse is unique to RevIN; other per-window normalizers are immune & All three per-window normalizers collapse identically (App.~\\ref{app:norm_generalization}) {\\small$\\Rightarrow$} any norm that strips […]

> TOOL

tool_result
id: toolu_012rJxG8BCb2opWe87h9N3K5
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01FpzLNYGcf5mvzJnqXSET4s
```json
{
  "command": "pdflatex -interaction=nonstopmode -draftmode main.tex > /tmp/p1.log 2>&1 && pdflatex -interaction=nonstopmode main.tex > /tmp/p2.log 2>&1; echo \"EXIT=$?\"; tail -2 /tmp/p2.log; echo \"---\"; grep -E \"multiply defined|undefined refer|LaTeX Warning: Reference\" /tmp/p2.log | head -5; echo \"---\"; python3 -c \"\nimport subprocess\nout = subprocess.check_output(['pdftotext', '-layout', 'main.pdf', '-']).decode('utf-8','ignore')\npages = out.split('\\f')\nfor i, p in enumerate(pages[:11], 1):\n    head = p.strip().split('\\n')[0] if p.strip() else '<empty>'\n    print(f'p{i}: {head[:100]}')\nprint()\nprint('=== p9 last 8 ===')\nprint('\\n'.join([l for l in pages[8].split('\\n') if l.strip()][-8:]))\nprint('=== p10 first 6 ===')\nprint('\\n'.join([l for l in pages[9].split('\\n') if l.strip()][:6]))\n\"",
  "description": "Rebuild and inspect after Table 3 move"
}
```

> TOOL

tool_result
id: toolu_01FpzLNYGcf5mvzJnqXSET4s
```
EXIT=0
Output written on main.pdf (50 pages, 882420 bytes).
Transcript written on main.log.
---
---
p1: Raw-Routed Mixture of Adapters: A Causal
p2: 37   still requires attaching a lightweight adapter head that maps hidden states to predictions; thi
p3: (a)                                                  TSFM adapters use the same head for every windo
p4: 127   time series, MoE has been used within TSFM backbones to scale capacity, with experts placed
p5: PATH A: E MBEDDINGS                                             Mean Pool
p6: 207   Backbones. Five backbones spanning three normalization regimes: (i) learnable-affine RevIN-ins
p7: Table 2: AdaMix routing collapse (entropy max ≈1.609). Under unfreezing, entropy →0.000.
p8: 260   to flip sign across input regimes, i.e., expert specialization, which is satisfied by the topo
p9: 311   Traffic’s null). The Pure Raw-MLP MoE ablation (Appendix P.3) separates “MoE with raw router”
p10: 347    [2] Mononito Goswami, Konrad Szafer, Arjun Choudhry, Yifu Cai, Shuo Li, and Artur Dubrawski.
p11: 395   [16] Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin De Laroussilh

=== p9 last 8 ===
340   on a normalized backbone can compute it pre-training, surfacing an upstream architectural cause
341   downstream rescues have so far blocked.
342   References
343    [1] Alexey Dosovitskiy, Lucas Beyer, Alexander […]

> AGENT

Body now fits on 9 pages. Verifying claim-numerics still pass and no refs broken.

> TOOL

tool_use Bash
id: toolu_01HBRg7pFTFSwDVidxKTDtFm
```json
{
  "command": "grep -E \"Warning.*[Rr]eference|undefined\" /tmp/p2.log | head -5; echo \"---verify.py---\"; python3 evidence_vm/verify.py 2>&1 | tail -3",
  "description": "Check refs + verify.py"
}
```

> TOOL

tool_result
id: toolu_01HBRg7pFTFSwDVidxKTDtFm
```
---verify.py---
Ran 107 checks against 54 RR-MoA + 54 AdaMix JSON files.
PASS: all 107 numeric claims in main.tex Tables 3-5, tab:baselines LoRA row, tab:horizon DLinear gaps, tab:backbone cross-backbone percentages, learnable alpha, imputation wins, and MI tightness match within tolerance (MSE 0.005, entropy 0.01, pct 1.0pp).
RR-MoA wins: 27/27
```

> AGENT

Body is now within the 9-page NeurIPS limit (body content + start of references on page 9; references don't count toward the limit). All 107 verify.py checks still pass; no broken refs.

**Changes made (citations preserved everywhere):**
- **Intro** (§1): collapsed the 5-LLM-as-forecaster catalog into one sentence with the same `\citep` keys; tightened paragraphs 2–4 (instance-norm, AdaMix collapse, Moirai-doesn't-collapse); compressed the 3 contributions bullets.
- **Method** (§3): trimmed prose around adapter definition, gating equation, and expert pool.
- **Results** (§4.2): tightened all four subsubsections — diagnosis prose, Frozen Paradox, Headline Numbers, DLinear-gap closing, cross-backbone summary.
- **Conclusion** (§5): minor tightening.
- **Table 3 (causal controls)** moved from §4.2 to App.~\ref{app:routing_ablations} (now also labeled `app:causal_controls`); replaced in body with one-sentence summary that still references all eight controls and the table label, so every existing `\ref{tab:causal_controls}` still resolves.

PDF: 50 pages total, body ends on page 9.

> DEVELOPER

let's quantitatively measure the word count and analyse the distribution of content in our paper, is it balanced and good

> TOOL

tool_use Bash
id: toolu_0137fpLojeak1485cfzeBp6G
```json
{
  "command": "python3 << 'EOF'\nimport re, subprocess\n\nwith open('main.tex') as f:\n    src = f.read()\n\n# Find boundaries by section command line numbers\nlines = src.split('\\n')\nsections = []  # (name, start_line)\nfor i, l in enumerate(lines):\n    m = re.match(r'\\\\section\\*?\\{([^}]+)\\}', l.strip())\n    if m: sections.append((m.group(1), i))\n    if l.strip().startswith(r'\\appendix'): sections.append(('__APPENDIX__', i))\n    if l.strip().startswith(r'\\bibliography') or l.strip().startswith(r'\\begin{thebibliography}'): sections.append(('__BIB__', i))\n\n# Cut body = section[0] .. __BIB__/__APPENDIX__ first\ndef section_text(start, end):\n    block = '\\n'.join(lines[start:end])\n    # Strip TikZ pictures, tables, equations, comments — they aren't word-count \"prose\"\n    block = re.sub(r'%.*', '', block)\n    block = re.sub(r'\\\\begin\\{tikzpicture\\}.*?\\\\end\\{tikzpicture\\}', '', block, flags=re.S)\n    block = re.sub(r'\\\\begin\\{table\\*?\\}.*?\\\\end\\{table\\*?\\}', '', block, flags=re.S)\n    block = re.sub(r'\\\\begin\\{figure\\*?\\}.*?\\\\end\\{figure\\*?\\}', '', block, flags=re.S)\n    block = re.sub(r'\\\\begin\\{equation\\*?\\}.*?\\\\end\\{equation\\*?\\}', '', block, flags=re.S)\n    block = re.sub(r'\\\\begin\\{align\\*?\\}.*?\\\\end\\{align\\*?\\}', '', block, flags=re.S)\n    block = re.sub(r'\\\\begin\\{algorithm\\*?\\}.*?\\\\end\\{algorithm\\*?\\}', '', block, flags=re.S)\n    block = re.sub(r'\\\\begin\\{proof\\}.*?\\\\end\\{proof\\}', '', block, flags=re.S)\n    block = re.sub(r'\\$[^$]*\\$', ' MATH ', block)\n    block = re.sub(r'\\\\cite[a-z]*\\{[^}]*\\}', ' CITE ', block)\n    block = re.sub(r'\\\\ref\\{[^}]*\\}', ' REF ', block)\n    block = re.sub(r'\\\\label\\{[^}]*\\}', '', block)\n    block = re.sub(r'\\\\[A-Za-z]+\\*?', ' ', block)\n    block = re.sub(r'[{}]', ' ', block)\n    words = re.findall(r'\\b[A-Za-z][A-Za-z\\-]+\\b', block)\n    return len(words)\n\n# Word counts per top-level body section\nprint(f\"{'Section':<55}{'words':>8}  {'%':>6}\")\nprint('-'*72)\nbody_total = 0\nbody_sections = []\nfor i, (name, start) in enumerate(sections):\n    if name in ('__APPENDIX__', '__BIB__'): break\n    end = sections[i+1][1] if i+1 < len(sections) else len(lines)\n […]

> TOOL

tool_result
id: toolu_0137fpLojeak1485cfzeBp6G
```
Section                                                   words       %
------------------------------------------------------------------------
Introduction                                                532   23.2%
Related Work                                               1153   50.2%
Raw-Routed Mixture of Adapters (RR-MoA)                     164    7.1%
Experiments                                                 353   15.4%
Conclusion and Limitations                                   94    4.1%
------------------------------------------------------------------------
BODY TOTAL                                                 2296  100.0%

Appendix Section                                          words
------------------------------------------------------------------------
Experimental Setup Details                                  275
Deployment-Regime Motivation                                298
Multi-Horizon Evaluation                                     25
Proposition Proofs                                          539
LoRA Sweep (Full Results)                                   270
Routing Ablations                                           274
Extended RR-MoA Freeze Grid                                 113
Normalization Generalization                                433
Top-$k$ Sparse Routing Ablation                             146
Imputation Results                                           60
Learnable Normalization Coefficient                         118
Exact MI Loss and Bound Tightness                           125
Information Content Diagnostic                               69
Cross-Backbone RR-MoA                                        91
Extended Full Fine-Tuning Ablation                           75
Closing the DLinear Gap                                    1217
------------------------------------------------------------------------
APPENDIX TOTAL                                             4128

BODY total = 2296 words   APPENDIX total = 4128 words
Body:Appendix ratio = 1 : 1.80
```

> AGENT

## Word distribution

| Body section | Words | % of body |
|---|---:|---:|
| Introduction | 532 | 23.2% |
| Related Work | **1153** | **50.2%** |
| Method (RR-MoA) | 164 | 7.1% |
| Experiments | 353 | 15.4% |
| Conclusion | 94 | 4.1% |
| **Body total** | **2296** | 100% |

Appendix: 4128 words across 16 sections. Body:Appendix ≈ 1:1.80. Largest appendix block is §P Closing the DLinear Gap at 1217 words (30% of appendix); next are §D Proofs (539) and §H Normalization Generalization (433).

## Verdict: body is unbalanced

A typical NeurIPS body sits roughly at **Intro 15–20% / Related Work 10–15% / Method 25–30% / Experiments 30–40% / Conclusion <5%**. Yours:

- **Related Work eats half the body (50%, ~1150 words).** That is roughly 3× the conventional share. The four mini-paragraphs (TSFM Adaptation, MoE in FMs, MoE Collapse and Rescue, Normalization in TS) read more like a survey than a positioning section.
- **Method is starved (7%, 164 words of prose).** Figures/equations carry the load, but the actual textual description of RR-MoA is thinner than the contributions list in the intro.
- **Experiments is also light (15%, 353 words).** Tables […]

> DEVELOPER

plan improvements toward more balanced without dropping in-text citations or messing with them

> AGENT

## Rebalancing plan — preserve every `\citep`/`\citet`, no page-limit regressions

**Target distribution** (typical NeurIPS):
| Section | Current | Target | Δ words |
|---|---:|---:|---:|
| Introduction | 532 (23%) | ~440 (~20%) | **−90** |
| Related Work | 1153 (50%) | ~600 (~27%) | **−550** |
| Method | 164 (7%) | ~340 (~15%) | **+175** |
| Experiments | 353 (15%) | ~640 (~28%) | **+285** |
| Conclusion | 94 (4%) | ~85 (~4%) | flat |
| **Total** | 2296 | ~2105 | **−190** (≈ ½ page recovered) |

Note: this both rebalances *and* recovers space, since cuts in Related Work outweigh the additions in Method/Experiments. That ½-page buffer is what funds the Method/Experiments expansion without re-spilling onto page 10.

---

### Step 1 — Compress Related Work by ~550 words (no citation loss)

Each `\citep`/`\citet` key stays. The cuts are descriptive clauses ("X reprograms patch embeddings into the LLM token space", "Y achieves competitive forecasting with only 10k parameters via frequency-domain interpolation") that paraphrase each cited work's contribution. The pattern is to convert "X~\citep{x} does <one-line description>" into bare list-citations grouped by theme.

Per-paragraph targets:
- **TSFM Adaptation** (~510 → ~250 words): merge the […]

> DEVELOPER

let's do it the safe way

> AGENT

Starting Step 1 — Related Work compression. First, baseline the citation count so we can verify nothing is dropped.

> TOOL

tool_use Bash
id: toolu_01Dk65VamC5yUrkSa1kUnGrP
```json
{
  "command": "grep -oP '\\\\cite[a-z]*\\{[^}]+\\}' main.tex | sort -u > /tmp/cite_keys_before.txt && wc -l /tmp/cite_keys_before.txt && cp main.tex /tmp/main.tex.bak.step1",
  "description": "Baseline citation count + backup"
}
```

> TOOL

tool_result
id: toolu_01Dk65VamC5yUrkSa1kUnGrP
```
      92 /tmp/cite_keys_before.txt
```

> TOOL

tool_use Read
id: toolu_01CByCsvBbxjTtj8LYp99Tn7
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 228,
  "limit": 12
}
```

> TOOL

tool_result
id: toolu_01CByCsvBbxjTtj8LYp99Tn7
```
228	\section{Related Work}
229	
230	\textbf{TSFM Adaptation.} For broader context on transformer-based time-series models we refer the reader to the survey by~\citet{wen2023tssurvey}. Outside the TSFM-with-adapter paradigm, a complementary line of work shows that compact task-specific models can match or beat heavyweight pretrained backbones on standard LTSF benchmarks: SRSNet~\citep{wu2025srsnet} learns selective patch-level representations, TimeMixer++~\citep{wang2025timemixerpp} unifies multiple analytical tasks under multi-scale pattern mixing, FITS~\citep{xu2024fits} achieves competitive forecasting with only $10$k parameters via frequency-domain interpolation, TSMixer~\citep{chen2023tsmixer} uses an all-MLP architecture, and~\citet{fu2025selective} trains existing models with timestep-selective losses. The fact that such lightweight raw-input models compete with TSFMs is itself evidence that the per-window raw signal carries most of the predictability we exploit in our diagnostic $R(\mathcal{D})$ (\S\ref{sec:diagnosis}). A parallel adaptation route reprograms pretrained LLMs as forecasters~\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes}: like RevIN-equipped TSFMs, these inherit per-window normalization upstream of the backbone, so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is attached. Here we focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a lightweight module to a frozen TSFM and tunes it on downstream data: LoRA~\citep{hu2022lora}, bottleneck adapters~\citep{houlsby2019adapters}, or a linear probe~\citep{goswami2024moment}. Recent variations explore multi-scale finetuning~\citep{qiao2025msft}, importance-based LoRA selection~\citep{li2025trace}, input-representation adaptation~\citep{benechehab2025adapts}, structured […]

> AGENT

Baseline: 92 unique citation keys. Backup saved. Now editing paragraph 1 (TSFM Adaptation).

> TOOL

tool_use Edit
id: toolu_01TZ3JhHXHrYr5LacXWm23P2
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\textbf{TSFM Adaptation.} For broader context on transformer-based time-series models we refer the reader to the survey by~\\citet{wen2023tssurvey}. Outside the TSFM-with-adapter paradigm, a complementary line of work shows that compact task-specific models can match or beat heavyweight pretrained backbones on standard LTSF benchmarks: SRSNet~\\citep{wu2025srsnet} learns selective patch-level representations, TimeMixer++~\\citep{wang2025timemixerpp} unifies multiple analytical tasks under multi-scale pattern mixing, FITS~\\citep{xu2024fits} achieves competitive forecasting with only $10$k parameters via frequency-domain interpolation, TSMixer~\\citep{chen2023tsmixer} uses an all-MLP architecture, and~\\citet{fu2025selective} trains existing models with timestep-selective losses. The fact that such lightweight raw-input models compete with TSFMs is itself evidence that the per-window raw signal carries most of the predictability we exploit in our diagnostic $R(\\mathcal{D})$ (\\S\\ref{sec:diagnosis}). A parallel adaptation route reprograms pretrained LLMs as forecasters~\\citep{jin2024timellm, zhou2023onefitsall, liu2024autotimes}: like RevIN-equipped TSFMs, these inherit per-window normalization upstream of the backbone, so the routing-collapse mechanism we identify applies whenever a downstream MoE adapter is attached. Here we focus on the adapter literature most relevant to RR-MoA. The standard recipe attaches a lightweight module to a frozen TSFM and tunes it on downstream data: LoRA~\\citep{hu2022lora}, bottleneck adapters~\\citep{houlsby2019adapters}, or a linear probe~\\citep{goswami2024moment}. Recent variations explore multi-scale finetuning~\\citep{qiao2025msft}, importance-based LoRA selection~\\citep{li2025trace}, input-representation […]

> TOOL

tool_result
id: toolu_01TZ3JhHXHrYr5LacXWm23P2
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01N7h7ppqQU8v95rzY4eUKDk
```json
{
  "command": "grep -oP '\\\\cite[a-z]*\\{[^}]+\\}' main.tex | sort -u > /tmp/cite_keys_after1.txt; diff /tmp/cite_keys_before.txt /tmp/cite_keys_after1.txt; echo \"===\"; wc -l /tmp/cite_keys_after1.txt",
  "description": "Verify no citation keys lost after ¶1"
}
```

> TOOL

tool_result
id: toolu_01N7h7ppqQU8v95rzY4eUKDk
```
9d8
< \citep{chen2023tsmixer}
25c24
< \citep{houlsby2019adapters}
---
> \citep{hu2022lora, houlsby2019adapters, goswami2024moment}
62d60
< \citep{wang2025timemixerpp}
67,68c65
< \citep{wu2025srsnet}
< \citep{xu2024fits}
---
> \citep{wu2025srsnet, wang2025timemixerpp, xu2024fits, chen2023tsmixer, fu2025selective}
81d77
< \citet{fu2025selective}
===
      88 /tmp/cite_keys_after1.txt
```

> TOOL

tool_use Bash
id: toolu_01RyrDaZxzxN6gNuEKEstXam
```json
{
  "command": "python3 -c \"\nimport re\nwith open('/tmp/main.tex.bak.step1') as f: b = f.read()\nwith open('main.tex') as f: a = f.read()\ndef keys(s): \n    return sorted({k.strip() for m in re.findall(r'\\\\\\\\cite[a-z]*\\{([^}]+)\\}', s) for k in m.split(',')})\nkb, ka = keys(b), keys(a)\nprint(f'before: {len(kb)} unique keys; after: {len(ka)} unique keys')\nprint(f'lost: {sorted(set(kb)-set(ka))}')\nprint(f'added: {sorted(set(ka)-set(kb))}')\n\"",
  "description": "Per-key citation diff (split multi-cites)"
}
```

> TOOL

tool_result
id: toolu_01RyrDaZxzxN6gNuEKEstXam
```
before: 91 unique keys; after: 91 unique keys
lost: []
added: []
```

> AGENT

All 91 unique keys preserved (true count after splitting multi-key cites). Continuing to ¶2.

> TOOL

tool_result
id: toolu_01JxjsBF7yV2J5QdHr5C3Yws
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01JxjsBF7yV2J5QdHr5C3Yws
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\textbf{MoE in Foundation Models.} Mixture-of-experts routing originated with the sparsely-gated layer of~\\citet{shazeer2017outrageously}, which introduced the noisy top-$k$ softmax gate and load-balancing loss our \\texttt{tab:rescue} sweep ablates, and was subsequently scaled to large language models via GShard's capacity-factor and automatic-sharding formulation~\\citep{lepikhin2021gshard} and Switch Transformers' single-expert routing~\\citep{fedus2022switch}, then to vision via V-MoE~\\citep{riquelme2021vmoe} (the architectural precedent for our cross-modality control in \\S\\ref{app:vision_moe}). Subsequent designs explore orthogonal axes of the design space: sparse upcycling~\\citep{komatsuzaki2023sparseupcycling} converts dense pretrained checkpoints into MoE models post-hoc, mixture-of-depths~\\citep{raposo2024mod} routes tokens to skip layers rather than to experts, open-weight LLMs such as Mixtral~\\citep{jiang2024mixtral} and LLaMA-MoE~\\citep{zhu2024llamamoe} demonstrate that MoE scales practically at deployment, and DeepSeekMoE~\\citep{dai2024deepseekmoe} achieves expert specialization through fine-grained segmentation and shared-expert isolation, an alternative to our architectural-diversity approach. We refer to~\\citet{cai2024moesurvey} for a comprehensive survey. In time series, MoE has been used \\emph{within} TSFM backbones to scale capacity, with experts placed inside the backbone architecture: Moirai-MoE~\\citep{liu2025moiraimoe} routes individual tokens to data-driven experts that automatically specialize across diverse time series patterns, and Time-MoE~\\citep{shi2024timemoe} uses sparse activation to reach billions of parameters. SEMPO~\\citep{he2025sempo} adopts a closely related routing-on-TSFM design at a different granularity: tokens are routed to dataset-specific prompt-experts for […]

> TOOL

tool_use Bash
id: toolu_0144yGrvHqP6yXaD2Ghv27or
```json
{
  "command": "python3 -c \"\nimport re\nwith open('/tmp/main.tex.bak.step1') as f: b = f.read()\nwith open('main.tex') as f: a = f.read()\ndef keys(s): return sorted({k.strip() for m in re.findall(r'\\\\\\\\cite[a-z]*\\{([^}]+)\\}', s) for k in m.split(',')})\nkb, ka = keys(b), keys(a)\nprint(f'before: {len(kb)}; after: {len(ka)}; lost: {sorted(set(kb)-set(ka))}; added: {sorted(set(ka)-set(kb))}')\n\"",
  "description": "Verify citations after ¶2"
}
```

> TOOL

tool_result
id: toolu_0144yGrvHqP6yXaD2Ghv27or
```
before: 91; after: 91; lost: []; added: []
```

> TOOL

tool_use Edit
id: toolu_01QySwKb6UKY8yzYfWXpcBV9
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\textbf{MoE routing collapse and rescue.} Existing diagnoses of routing collapse cluster, broadly, into three threads. \\emph{Optimization-side}: load-balancing losses~\\citep{fedus2022switch}, z-loss~\\citep{zoph2022stmoe}, and AdaMix's hidden-state router~\\citep{wang2022adamix} target training dynamics; \\citet{guo2025expertspec} further argue that the standard load-balance loss itself causes expert overlap and propose orthogonality and variance regularizers. \\emph{Representation-geometry}: \\citet{chi2022representation} attribute collapse to token clustering around expert centroids that emerges \\emph{during} routing learning and propose hyperspherical routing scores; \\citet{wu2024mhmoe} split each token into sub-tokens to raise expert activation. \\emph{Architectural / paradigm}: \\citet{zhou2022expertchoice} invert the token--expert paradigm via Expert-Choice routing, Soft MoE~\\citep{puigcerver2024softmoe} replaces hard top-$k$ assignment with a fully-differentiable soft mixture of all tokens, \\citet{wang2025remoe} replace top-$k$ with ReLU gating, \\citet{panda2024densebackprop} restore a dense gradient to the router under sparse forward passes to mitigate load imbalance, and \\citet{hua2025inputaware} decouple the router from the task objective so that routing decisions reflect input structure rather than task gradients. Our setting differs from all three: the routing signal is structurally absent from the router's input \\emph{by design of an upstream architectural normalizer (RevIN)}, before training dynamics, geometry, or routing-paradigm choices can act. Sweeping five rescue families spanning the optimization and routing-paradigm threads (load balancing, z-loss, Expert-Choice, ReLU […]

> TOOL

tool_result
id: toolu_01QySwKb6UKY8yzYfWXpcBV9
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_015jN5odaCYZBfxzFtMySsRU
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "{\\looseness=-1 \\textbf{Normalization in Time Series.} The instance-level normalization that RevIN extends to time series originated in style transfer~\\citep{ulyanov2016instancenorm}; RevIN~\\citep{kim2021revin} adapts it to mitigate distribution shift in forecasting; DishTS~\\citep{fan2023dishts}, SAN~\\citep{liu2023san}, and Non-stationary Transformers~\\citep{liu2022nonstationary} partially recover stripped statistics; FAN~\\citep{ye2024fan} extends instance normalization beyond $(\\mu,\\sigma)$ to dominant Fourier components; DDN~\\citep{dai2024ddn} dynamically normalizes in both time and frequency domains via wavelet decomposition. Concurrently, \\citet{berthelier2026revin} independently show that several RevIN components are redundant or detrimental, and \\citet{zou2025ibnorm} argue that variance-centric normalization (BatchNorm, LayerNorm, RMSNorm) is suboptimal for representation learning because two representations with identical mean and variance can encode different amounts of task-relevant information. We identify a specific, mechanistic consequence of this principle that has not been characterized in the MoE literature: when the stripped statistics carry the \\emph{routing} signal in a downstream MoE adapter, instance normalization causes the router to collapse to a single expert under unfreezing, a failure mode distinct from the optimization-induced collapse studied in standard MoE rescue literature. Section~\\ref{sec:method} formalizes this diagnosis and presents the minimal architectural fix it implies.}",
  "new_string": "{\\looseness=-1 \\textbf{Normalization in Time Series.} Instance normalization originated in style transfer~\\citep{ulyanov2016instancenorm}; RevIN~\\citep{kim2021revin} adapts it to forecasting distribution shift; DishTS~\\citep{fan2023dishts}, […]

> TOOL

tool_result
id: toolu_015jN5odaCYZBfxzFtMySsRU
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01Kz9XEdCiG6ME9G7xvJSuD8
```json
{
  "command": "python3 -c \"\nimport re\nwith open('/tmp/main.tex.bak.step1') as f: b = f.read()\nwith open('main.tex') as f: a = f.read()\ndef keys(s): return sorted({k.strip() for m in re.findall(r'\\\\\\\\cite[a-z]*\\{([^}]+)\\}', s) for k in m.split(',')})\nkb, ka = keys(b), keys(a)\nprint(f'before: {len(kb)}; after: {len(ka)}; lost: {sorted(set(kb)-set(ka))}; added: {sorted(set(ka)-set(kb))}')\n\" && pdflatex -interaction=nonstopmode -draftmode main.tex > /tmp/p1.log 2>&1 && pdflatex -interaction=nonstopmode main.tex > /tmp/p2.log 2>&1; tail -2 /tmp/p2.log; python3 evidence_vm/verify.py 2>&1 | tail -2",
  "description": "Verify Step 1 (citations + build + verify.py)"
}
```

> TOOL

tool_result
id: toolu_01Kz9XEdCiG6ME9G7xvJSuD8
```
before: 91; after: 91; lost: []; added: []
Output written on main.pdf (50 pages, 879954 bytes).
Transcript written on main.log.
PASS: all 107 numeric claims in main.tex Tables 3-5, tab:baselines LoRA row, tab:horizon DLinear gaps, tab:backbone cross-backbone percentages, learnable alpha, imputation wins, and MI tightness match within tolerance (MSE 0.005, entropy 0.01, pct 1.0pp).
RR-MoA wins: 27/27
```

> TOOL

tool_use Bash
id: toolu_01Su6XTDYPyQpqTHt67UjVhG
```json
{
  "command": "python3 << 'EOF'\nimport re, subprocess\nwith open('main.tex') as f: src = f.read()\nlines = src.split('\\n')\nsections = []\nfor i, l in enumerate(lines):\n    m = re.match(r'\\\\section\\*?\\{([^}]+)\\}', l.strip())\n    if m: sections.append((m.group(1), i))\n    if l.strip().startswith(r'\\appendix'): sections.append(('__APPENDIX__', i))\n    if l.strip().startswith(r'\\bibliography') or l.strip().startswith(r'\\begin{thebibliography}'): sections.append(('__BIB__', i))\ndef section_text(start, end):\n    block = '\\n'.join(lines[start:end])\n    block = re.sub(r'%.*', '', block)\n    for env in ['tikzpicture','table\\*?','figure\\*?','equation\\*?','align\\*?','algorithm\\*?','proof']:\n        block = re.sub(rf'\\\\begin{{{env}}}.*?\\\\end{{{env}}}', '', block, flags=re.S)\n    block = re.sub(r'\\$[^$]*\\$', ' ', block)\n    block = re.sub(r'\\\\cite[a-z]*\\{[^}]*\\}', ' CITE ', block)\n    block = re.sub(r'\\\\ref\\{[^}]*\\}', ' REF ', block)\n    block = re.sub(r'\\\\label\\{[^}]*\\}', '', block)\n    block = re.sub(r'\\\\[A-Za-z]+\\*?', ' ', block)\n    block = re.sub(r'[{}]', ' ', block)\n    return len(re.findall(r'\\b[A-Za-z][A-Za-z\\-]+\\b', block))\nbody_total = 0\nbody_sections = []\nfor i, (name, start) in enumerate(sections):\n    if name in ('__APPENDIX__', '__BIB__'): break\n    end = sections[i+1][1] if i+1 < len(sections) else len(lines)\n    wc = section_text(start, end)\n    body_sections.append((name, wc))\n    body_total += wc\nfor name, wc in body_sections:\n    print(f\"{name:<55}{wc:>6}  {100*wc/body_total:>5.1f}%\")\nprint(f\"{'BODY TOTAL':<55}{body_total:>6}\")\nEOF",
  "description": "Re-measure body distribution after Step 1"
}
```

> TOOL

tool_result
id: toolu_01Su6XTDYPyQpqTHt67UjVhG
```
<stdin>:13: SyntaxWarning: invalid escape sequence '\*'
<stdin>:13: SyntaxWarning: invalid escape sequence '\*'
<stdin>:13: SyntaxWarning: invalid escape sequence '\*'
<stdin>:13: SyntaxWarning: invalid escape sequence '\*'
<stdin>:13: SyntaxWarning: invalid escape sequence '\*'
Introduction                                              521   29.6%
Related Work                                              754   42.8%
Raw-Routed Mixture of Adapters (RR-MoA)                   142    8.1%
Experiments                                               262   14.9%
Conclusion and Limitations                                 84    4.8%
BODY TOTAL                                               1763
```

> TOOL

tool_use Bash
id: toolu_01MtbFZMCTRx5B368jd8JLqz
```json
{
  "command": "python3 -c \"\nimport subprocess\nout = subprocess.check_output(['pdftotext', '-layout', 'main.pdf', '-']).decode('utf-8','ignore')\npages = out.split('\\f')\nfor i, p in enumerate(pages[:11], 1):\n    head = p.strip().split('\\n')[0] if p.strip() else '<empty>'\n    print(f'p{i}: {head[:90]}')\nprint()\nprint('=== p9 last 6 ===')\nprint('\\n'.join([l for l in pages[8].split('\\n') if l.strip()][-6:]))\n\"",
  "description": "Check page-9 boundary after Step 1"
}
```

> TOOL

tool_result
id: toolu_01MtbFZMCTRx5B368jd8JLqz
```
p1: Raw-Routed Mixture of Adapters: A Causal
p2: 37   still requires attaching a lightweight adapter head that maps hidden states to predic
p3: (a)                                                  TSFM adapters use the same head for e
p4: PATH A: E MBEDDINGS                                 Mean Pool
p5: 157   to select which experts to activate:
p6: 201   Diagnosis: adapters underperform, MoE collapses
p7: 1.75                                              log K = 1.609 (max entropy)
p8: 254   not the bypass. The interpolation xα = (1−α)xraw + α RevIN(xraw ) shows a phase tran
p9: 290   Cross-backbone, task, horizon. RR-MoA wins on every instance-normalized backbone (MO
p10: 340        time series foundation models with sparse mixture of experts. In Proceedings of
p11: 387   [24] Zhongzheng Qiao, Chenghao Liu, Yiming Zhang, Ming Jin, Quang Pham, Qingsong Wen

=== p9 last 6 ===
335    [7] Gerald Woo, Chenghao Liu, Akshat Kumar, Caiming Xiong, Silvio Savarese, and Doyen Sahoo.
336        Unified training of universal time series forecasting transformers. In Proceedings of the 41st
337        International Conference on Machine Learning (ICML), 2024.
338    [8] Xu Liu, Juncheng Liu, Gerald Woo, Taha Aksu, Yuxuan Liang, Roger Zimmermann, Chenghao
339        Liu, Junnan Li, Silvio Savarese, Caiming Xiong, and Doyen Sahoo. Moirai-MoE: Empowering
                                                         9
```

> AGENT

Step 1 complete: Related Work 50.2% → 42.8%, body ends comfortably on p9, citations preserved (91/91), 107/107 verify.py checks pass. Now proceeding to Steps 2 + 3 (expand Method + Experiments). Backup current state.

> TOOL

tool_use Bash
id: toolu_01F6n4m5ghYjPTfXfLVRaLn3
```json
{
  "command": "cp main.tex /tmp/main.tex.bak.step2",
  "description": "Backup before Step 2"
}
```

> TOOL

tool_result
id: toolu_01F6n4m5ghYjPTfXfLVRaLn3
```
(Bash completed with no output)
```

> TOOL

tool_use Read
id: toolu_01AsqUe2dDimd1VGT25RkLxZ
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 380,
  "limit": 8
}
```

> TOOL

tool_result
id: toolu_01AsqUe2dDimd1VGT25RkLxZ
```
380	\label{eq:rrmoa}
381	\end{equation}
382	where $G_\psi: \mathbb{R}^{T} \to \mathbb{R}^K$ is a small Conv1d\,+\,pooling\,+\,linear gate ($853$ params) operating directly on the raw time series, $\mathcal{T} \subset \{1,\ldots,K\}$ is the set of Top-$k$ indices, and each $\mathrm{Expert}_j$ is a canonical adapter head. By construction $\sum_j \widetilde{w}_j = 1$ with support only on $\mathcal{T}$, so only $k$ of $K$ experts execute per sample. With $K{=}5$, $k{=}2$ we obtain $40\%$ of the dense expert FLOPs while retaining $63\%$ of the dense MSE improvement over the best fixed adapter (\S\ref{sec:topk}). Routing on raw input preserves the temporal statistics (trend, amplitude, volatility) that RevIN strips away.
383	
384	\textbf{Expert pool.} We maintain $K{=}5$ topologically distinct expert adapters (mean-pool, last-token, max-pool, attention-pool, Conv1d-pool), spanning pooling families with distinct expressivity regimes for transformer-based sequence models~\citep{ennadir2025pooling}. Architectural diversity is critical: five identical experts (same topology, different initialization) degrade MSE by $8$--$15\%$ (Appendix~\ref{app:diversity}). Pseudocode in Algorithm~\ref{alg:rrmoa} (Appendix~\ref{app:setup}). We now validate that this fix recovers routing diversity, beats the seven-method baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full fine-tuning, DLinear), and holds under eight causal controls.
385	
386	\section{Experiments}
387	
```

> TOOL

tool_use Edit
id: toolu_018B7k1DAYnGunDyR1WrqNEo
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\textbf{Expert pool.} We maintain $K{=}5$ topologically distinct expert adapters (mean-pool, last-token, max-pool, attention-pool, Conv1d-pool), spanning pooling families with distinct expressivity regimes for transformer-based sequence models~\\citep{ennadir2025pooling}. Architectural diversity is critical: five identical experts (same topology, different initialization) degrade MSE by $8$--$15\\%$ (Appendix~\\ref{app:diversity}). Pseudocode in Algorithm~\\ref{alg:rrmoa} (Appendix~\\ref{app:setup}). We now validate that this fix recovers routing diversity, beats the seven-method baseline suite (fixed adapters, LoRA, TRACE, independent ensembles, AdaMix, full fine-tuning, DLinear), and holds under eight causal controls.",
  "new_string": "\\textbf{Inference cost and deployment.} The router is a Conv1d gate of $853$ parameters ($0.4\\%$ of one expert head, ${<}10^{-3}$ of the frozen backbone). With $k{=}2$ of $K{=}5$ experts active per window, RR-MoA adds two adapter forward passes plus the gate to one frozen TSFM forward; the unselected $K{-}k$ experts do not execute. Because the backbone is strictly frozen, a single TSFM held in GPU memory can be shared across many tenants while per-task adapter pools (${\\sim}500$K params each) are hot-swapped from host RAM, an arrangement DLinear and per-dataset-from-scratch baselines cannot match (Appendix~\\ref{app:benchmark}).\n\n\\textbf{Routing dynamics.} In trained RR-MoA the router learns a non-degenerate per-window dispatch: routing entropy stays in $[1.0, 1.57]$ (vs.\\ $\\log K{=}1.609$ ceiling), […]

> TOOL

tool_result
id: toolu_018B7k1DAYnGunDyR1WrqNEo
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> AGENT

Now Step 3: expand §4.2 (60-80 words per subsubsection).

> TOOL

tool_use Read
id: toolu_017uSUxN77W1KK5ZsWYX8XR3
```json
{
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "offset": 464,
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_017uSUxN77W1KK5ZsWYX8XR3
```
464	\bottomrule
465	\end{tabular}
466	\end{table}
467	
468	{\looseness=-1 \textbf{Why does standard MoE routing fail?} We examine AdaMix~\citep{wang2022adamix} with a learned hidden-state softmax router, an established sparsely-gated MoE recipe~\citep{fedus2022switch} (Appendix~\ref{app:adamix_details}). Table~\ref{tab:adamix} shows AdaMix collapses to a single expert whenever backbone layers are unfrozen: entropy reaches $0.000\pm0.000$ in 7/12 unfrozen configurations; the remaining 5 stay below $0.55$ (max ${\approx}1.61$) with $\sigma$ up to $0.71$, indicating stochastic collapse. Disabling RevIN inside MOMENT recovers entropy to $0.66$--$1.32$ (BatchNorm1d/GroupNorm collapse identically, Appendix~\ref{app:norm_generalization}). The contrast is sharpest cross-backbone (Figure~\ref{fig:causal_contrast}): under identical last-4 unfreezing on identical data, MOMENT entropy crashes to $0.000$ in ${\sim}40$ steps while Timer-XL (no RevIN) stays at $1.60$ for $400$ steps.}
469	
470	\begin{figure}[!htbp]
471	\centering
472	\includegraphics[width=0.60\columnwidth]{figures/causal_contrast.pdf}
473	\vspace{-6pt}
474	\caption{\textbf{Causal contrast: MOMENT vs Timer-XL} (ETTh1, last-4 unfreezing). Solid: unfrozen; MOMENT entropy collapses $0.51{\to}0.000$ in ${\sim}40$ steps; Timer-XL holds ${\approx}1.60$ for $400$ steps. Dashed: frozen controls. Dotted: $\log K{=}1.609$ ceiling. Same code, same data, only normalization differs. Per-step entropy and per-expert gradient-norm trajectories are in Figure~\ref{fig:trajectory} (Appendix~\ref{app:adamix_details}).}
475	\label{fig:causal_contrast}
476	\end{figure}
477	
478	In contrast, \textbf{RR-MoA} maintains healthy entropy ($1.0$--$1.57$) and wins \textbf{54/54} configurations with $26$--$79\%$ MSE improvements over the best fixed adapter. On Traffic ($R{=}0.14$) RR-MoA […]

> TOOL

tool_use Edit
id: toolu_01USbQ4uaNPUjPw9ECxoUVP8
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "{\\looseness=-1 \\textbf{Why does standard MoE routing fail?} We examine AdaMix~\\citep{wang2022adamix} with a learned hidden-state softmax router, an established sparsely-gated MoE recipe~\\citep{fedus2022switch} (Appendix~\\ref{app:adamix_details}). Table~\\ref{tab:adamix} shows AdaMix collapses to a single expert whenever backbone layers are unfrozen: entropy reaches $0.000\\pm0.000$ in 7/12 unfrozen configurations; the remaining 5 stay below $0.55$ (max ${\\approx}1.61$) with $\\sigma$ up to $0.71$, indicating stochastic collapse. Disabling RevIN inside MOMENT recovers entropy to $0.66$--$1.32$ (BatchNorm1d/GroupNorm collapse identically, Appendix~\\ref{app:norm_generalization}). The contrast is sharpest cross-backbone (Figure~\\ref{fig:causal_contrast}): under identical last-4 unfreezing on identical data, MOMENT entropy crashes to $0.000$ in ${\\sim}40$ steps while Timer-XL (no RevIN) stays at $1.60$ for $400$ steps.}",
  "new_string": "{\\looseness=-1 \\textbf{Why does standard MoE routing fail?} We examine AdaMix~\\citep{wang2022adamix} with a learned hidden-state softmax router, an established sparsely-gated MoE recipe~\\citep{fedus2022switch} (Appendix~\\ref{app:adamix_details}). Table~\\ref{tab:adamix} shows AdaMix collapses to a single expert whenever backbone layers are unfrozen: entropy reaches $0.000\\pm0.000$ in 7/12 unfrozen configurations; the remaining 5 stay below $0.55$ (max ${\\approx}1.61$) with $\\sigma$ up to $0.71$. The high seed-variance distinguishes \\emph{stochastic} collapse (router commits to one expert per run, but to different experts across seeds) from \\emph{stable} partial routing (which would yield low $\\sigma$ at intermediate entropy); the […]

> TOOL

tool_result
id: toolu_01USbQ4uaNPUjPw9ECxoUVP8
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01AdLBPXAFJKfeUVcB5m1Sgr
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "When routing signal lives entirely in the stripped statistics ($(M,\\Sigma)\\perp\\!\\!\\!\\perp S$; Appendix~\\ref{app:proofs}), $I(X;E){-}I(S;E){=}H(E)$: RevIN destroys the entire routing distribution. The signal ratio $R(\\mathcal{D}) = [\\mathrm{Var}(M)+\\mathrm{Var}(\\Sigma)]/\\overline{\\mathrm{Var}(S)}$ is a tractable monotone proxy, computable from raw dataset statistics before any training; the bound is empirically tight (Appendix~\\ref{app:mi_tightness}) and learnable $\\alpha{<}0.5$ on $30/30$ runs (Appendix~\\ref{app:learnable_alpha}). $R(\\mathcal{D})$ predicts raw-routing benefit at Spearman $\\rho{=}{-}0.88$ ($p{<}0.002$, $n{=}9$; Figure~\\ref{fig:signal_ratio}), whereas $H(E\\mid S)$ does not ($\\rho{=}{-}0.12$); Traffic ($R{=}0.14$) is a boundary, Solar ($R{=}0.06$) the one outlier (Appendix~\\ref{app:routing_ablations}).",
  "new_string": "When routing signal lives entirely in the stripped statistics ($(M,\\Sigma)\\perp\\!\\!\\!\\perp S$; Appendix~\\ref{app:proofs}), $I(X;E){-}I(S;E){=}H(E)$: RevIN destroys the entire routing distribution. The signal ratio $R(\\mathcal{D}) = [\\mathrm{Var}(M)+\\mathrm{Var}(\\Sigma)]/\\overline{\\mathrm{Var}(S)}$ is a tractable monotone proxy, computable from raw dataset statistics before any training; the bound is empirically tight (Appendix~\\ref{app:mi_tightness}) and learnable $\\alpha{<}0.5$ on $30/30$ runs (Appendix~\\ref{app:learnable_alpha}). $R(\\mathcal{D})$ predicts raw-routing benefit at Spearman $\\rho{=}{-}0.88$ ($p{<}0.002$, $n{=}9$; Figure~\\ref{fig:signal_ratio}), whereas $H(E\\mid S)$ does not ($\\rho{=}{-}0.12$); Traffic ($R{=}0.14$) is a boundary, Solar ($R{=}0.06$) the one outlier (Appendix~\\ref{app:routing_ablations}). The discriminating power lies in the boundary case: the most likely competing explanation is that $R(\\mathcal{D})$ proxies generic ``hard dataset'' signal-to-noise, but Traffic has high overall predictability (DLinear MSE $0.41$) yet low […]

> TOOL

tool_result
id: toolu_01AdLBPXAFJKfeUVcB5m1Sgr
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_013AH1WZikAYK3C1pv7SC9q3
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "\\textbf{The principle is architecture-agnostic.} Three router-level controls validate that any router reading raw input suffices. \\textbf{SR-MoA} (Figure~\\ref{fig:srmoa_arch}; cf.~\\citealp{lv2025aoe,liu2026routingfree,cheng2025ermoe}) drops the external router for per-expert sigmoid gates $\\sigma_k(\\mathbf{X}_\\mathrm{raw})$ and \\emph{outperforms} RR-MoA by $13$--$42\\%$ on all 6 datasets ($252$ runs, six backbones; Table~\\ref{tab:self_routed}), also replicating the Frozen Paradox ($4/6$). Gating the same architecture on hidden states degrades by $+87$--$768\\%$ ($p{=}0.016$); on Timer-XL the same comparison yields only $+4$--$9\\%$, $15$--$100{\\times}$ smaller. \\textbf{AdaMix-Raw} (Appendix~\\ref{app:adamix_details}) swaps AdaMix's router input only and recovers entropy to $1.41$--$1.57$ and MSE by $41$--$88\\%$ on all 12 cells. \\textbf{Residual-IA\\textsuperscript{+}} (Appendix~\\ref{app:gate_pathology}, Figure~\\ref{fig:residual_ia_arch}) extends the principle to the expert level (shared NLinear raw branch + gated backbone residual).",
  "new_string": "\\textbf{The principle is architecture-agnostic.} Three router-level interventions cross-cut the design space: each varies a different axis (router architecture, router input, expert architecture) while holding the others fixed, so a common improvement isolates the raw-input axis as causal. \\textbf{SR-MoA} (Figure~\\ref{fig:srmoa_arch}; cf.~\\citealp{lv2025aoe,liu2026routingfree,cheng2025ermoe}) drops the external router for per-expert sigmoid gates $\\sigma_k(\\mathbf{X}_\\mathrm{raw})$ and \\emph{outperforms} RR-MoA by $13$--$42\\%$ on all 6 datasets ($252$ runs, six backbones; Table~\\ref{tab:self_routed}), also replicating the Frozen Paradox ($4/6$). Gating the same architecture on hidden states degrades by $+87$--$768\\%$ ($p{=}0.016$); on Timer-XL […]

> TOOL

tool_result
id: toolu_013AH1WZikAYK3C1pv7SC9q3
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01TSCVy91HcvX5ohadgNCnXw
```json
{
  "replace_all": false,
  "file_path": "/Users/hungpq2412/neuralips26/main.tex",
  "old_string": "{\\looseness=-1 \\textbf{Cross-backbone, task, horizon.}\\label{sec:cross_backbone}\\label{sec:topk} RR-MoA wins on every instance-normalized backbone (MOMENT-small/large $26$--$79\\%/32$--$75\\%$, Moirai $12$--$29\\%$, Moirai-MoE~\\citep{liu2025moiraimoe} $37$--$90\\%$); LayerNorm-only Chronos and Timer-XL~\\citep{liu2025timerxl} show no collapse. Top-$2$, imputation ($7/8$), $24/24$ horizons, and Residual-IA\\textsuperscript{+} ($6{\\times}5{\\times}4$) confirm robustness (Tables~\\ref{tab:cross_backbone}--\\ref{tab:horizon}; App.~\\ref{app:topk},~\\ref{app:imputation},~\\ref{app:gate_pathology}).}",
  "new_string": "{\\looseness=-1 \\textbf{Cross-backbone, task, horizon.}\\label{sec:cross_backbone}\\label{sec:topk} RR-MoA wins on every instance-normalized backbone tested (MOMENT-small/large $26$--$79\\%/32$--$75\\%$, Moirai $12$--$29\\%$, Moirai-MoE~\\citep{liu2025moiraimoe} $37$--$90\\%$), and LayerNorm-only Chronos and Timer-XL~\\citep{liu2025timerxl} show no collapse — the predicted negative-control split. Beyond forecasting at $H{=}96$, RR-MoA wins $7/8$ imputation cells (App.~\\ref{app:imputation}) and $24/24$ multi-horizon cells across $H{\\in}\\{96,192,336,720\\}$ (Tables~\\ref{tab:cross_backbone}--\\ref{tab:horizon}); Residual-IA\\textsuperscript{+} additionally generalizes across the $6{\\times}5{\\times}4$ dataset $\\times$ backbone $\\times$ horizon grid (App.~\\ref{app:gate_pathology}). Together these confirm the diagnosis is task-, horizon-, and backbone-portable rather than tied to the specific MOMENT$+$RevIN combination on which it was first observed.}"
}
```

> TOOL

tool_result
id: toolu_01TSCVy91HcvX5ohadgNCnXw
```
The file /Users/hungpq2412/neuralips26/main.tex has been updated successfully.
```

> AGENT

Now verify everything: build, page count, citations, claim numerics.

> TOOL

tool_use Bash
id: toolu_01SCS6EysaQBv82iibMmo8ys
```json
{
  "command": "python3 -c \"\nimport re\nwith open('/tmp/main.tex.bak.step1') as f: orig = f.read()\nwith open('main.tex') as f: cur = f.read()\ndef keys(s): return sorted({k.strip() for m in re.findall(r'\\\\\\\\cite[a-z]*\\{([^}]+)\\}', s) for k in m.split(',')})\nko, kc = keys(orig), keys(cur)\nprint(f'orig: {len(ko)}; current: {len(kc)}; lost: {sorted(set(ko)-set(kc))}; added: {sorted(set(kc)-set(ko))}')\n\" && pdflatex -interaction=nonstopmode -draftmode main.tex > /tmp/p1.log 2>&1 && pdflatex -interaction=nonstopmode main.tex > /tmp/p2.log 2>&1; tail -2 /tmp/p2.log; python3 evidence_vm/verify.py 2>&1 | tail -2; echo \"---pages---\"; python3 -c \"\nimport subprocess\nout = subprocess.check_output(['pdftotext', '-layout', 'main.pdf', '-']).decode('utf-8','ignore')\npages = out.split('\\f')\nfor i, p in enumerate(pages[:11], 1):\n    head = p.strip().split('\\n')[0] if p.strip() else '<empty>'\n    print(f'p{i}: {head[:90]}')\nprint()\nprint('=== p9 last 4 ===')\nprint('\\n'.join([l for l in pages[8].split('\\n') if l.strip()][-4:]))\n\"",
  "description": "Verify Step 2+3 (cites, build, page9, verify.py)"
}
```

> TOOL

tool_result
id: toolu_01SCS6EysaQBv82iibMmo8ys
```
orig: 91; current: 91; lost: []; added: []
Output written on main.pdf (50 pages, 882854 bytes).
Transcript written on main.log.
PASS: all 107 numeric claims in main.tex Tables 3-5, tab:baselines LoRA row, tab:horizon DLinear gaps, tab:backbone cross-backbone percentages, learnable alpha, imputation wins, and MI tightness match within tolerance (MSE 0.005, entropy 0.01, pct 1.0pp).
RR-MoA wins: 27/27
---pages---
p1: Raw-Routed Mixture of Adapters: A Causal
p2: 37   still requires attaching a lightweight adapter head that maps hidden states to predic
p3: (a)                                                  TSFM adapters use the same head for e
p4: PATH A: E MBEDDINGS                                 Mean Pool
p5: 157   to select which experts to activate:
p6: 201   Baselines. Four tiers, kept separate to avoid confounding frozen-vs-unfrozen and ada
p7: Table 2: AdaMix routing collapse (entropy max ≈1.609). Under unfreezing, entropy →0.000.
p8: 252   Mechanism: instance normalization strips the routing signal
p9: 304   Traffic’s null). The Pure Raw-MLP MoE ablation (Appendix P.3) separates “MoE with ra
p10: 339   References
p11: 389   [15] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean 

=== p9 last 4 ===
336   pool is fixed at five hand-coded experts (learned pools are open). R(D) is portable: any MoE-adapter
337 […]

> TOOL

tool_use Bash
id: toolu_01GU8VmrR4Am5nJBc7XbukkD
```json
{
  "command": "python3 << 'EOF'\nimport re\nwith open('main.tex') as f: src = f.read()\nlines = src.split('\\n')\nsections = []\nfor i, l in enumerate(lines):\n    m = re.match(r'\\\\section\\*?\\{([^}]+)\\}', l.strip())\n    if m: sections.append((m.group(1), i))\n    if l.strip().startswith(r'\\appendix'): sections.append(('__APPENDIX__', i))\n    if l.strip().startswith(r'\\bibliography') or l.strip().startswith(r'\\begin{thebibliography}'): sections.append(('__BIB__', i))\n\ndef section_text(start, end):\n    block = '\\n'.join(lines[start:end])\n    block = re.sub(r'%.*', '', block)\n    for env in ['tikzpicture', r'table\\*?', r'figure\\*?', r'equation\\*?', r'align\\*?', r'algorithm\\*?', 'proof']:\n        block = re.sub(rf'\\\\begin{{{env}}}.*?\\\\end{{{env}}}', '', block, flags=re.S)\n    block = re.sub(r'\\$[^$]*\\$', ' M ', block)\n    block = re.sub(r'\\\\cite[a-z]*\\{[^}]*\\}', ' C ', block)\n    block = re.sub(r'\\\\ref\\{[^}]*\\}', ' R ', block)\n    block = re.sub(r'\\\\label\\{[^}]*\\}', '', block)\n    block = re.sub(r'\\\\[A-Za-z]+\\*?', ' ', block)\n    block = re.sub(r'[{}]', ' ', block)\n    return len(re.findall(r'\\b[A-Za-z][A-Za-z\\-]+\\b', block))\n\nprint(f\"{'Section':<55}{'words':>7}  {'%':>6}\")\nprint('-'*72)\nbody_total = 0\nbody_sections = []\nfor i, (name, start) in enumerate(sections):\n    if name in ('__APPENDIX__', '__BIB__'): break\n    end = sections[i+1][1] if i+1 < len(sections) else len(lines)\n    wc = section_text(start, end)\n    body_sections.append((name, wc))\n    body_total += wc\nfor name, wc in body_sections:\n    print(f\"{name:<55}{wc:>7}  {100*wc/body_total:>5.1f}%\")\nprint('-'*72)\nprint(f\"{'BODY TOTAL':<55}{body_total:>7}\")\nEOF",
  "description": "Final balanced-body word distribution"
}
```

> TOOL

tool_result
id: toolu_01GU8VmrR4Am5nJBc7XbukkD
```
Section                                                  words       %
------------------------------------------------------------------------
Introduction                                               485   27.0%
Related Work                                               693   38.7%
Raw-Routed Mixture of Adapters (RR-MoA)                    199   11.1%
Experiments                                                334   18.6%
Conclusion and Limitations                                  82    4.6%
------------------------------------------------------------------------
BODY TOTAL                                                1793
```

> AGENT

All gates pass. Final state:

| Section | Before | After | Δ |
|---|---:|---:|---:|
| Introduction | 23.2% | 27.0% | (relative ↑ from RW shrink) |
| **Related Work** | **50.2%** | **38.7%** | **−11.5pp** |
| **Method** | **7.1%** | **11.1%** | **+4.0pp** |
| **Experiments** | **15.4%** | **18.6%** | **+3.2pp** |
| Conclusion | 4.1% | 4.6% | flat |

**Verification gates (all green):**
- 91/91 unique citation keys preserved (no `\citep`/`\citet` dropped or modified)
- LaTeX builds clean, body fits on page 9 (conclusion's last line on p9, References starts p10)
- 107/107 verify.py numeric claims still pass
- PDF: 50 pages total

**What changed:**
- **Related Work** (4 paragraphs): collapsed per-cite vignettes into grouped citations while keeping the AdaMix/AdaPTS/SEMPO/MoLE positioning sentences and the three-thread MoE-collapse classification intact.
- **Method §3** (+2 paragraphs): added "Inference cost and deployment" (router param count, FLOPs share, hot-swap deployment) and "Routing dynamics" (entropy band, naive-rescue forward reference).
- **Experiments §4.2** (+1–2 sentences per subsubsection): explained stochastic-vs-stable collapse signature, added the SNR-falsification interpretation of the Traffic boundary case, framed the three architecture-agnostic interventions as a 3-axis cross-cut, and expanded the cross-backbone summary into per-axis (backbone / task / horizon) […]

> DEVELOPER

another round of review please to check the quantitative measures again

> TOOL

tool_use Bash
id: toolu_01AJdT46THZZYQXAHoLjo7dM
```json
{
  "command": "python3 << 'EOF'\nimport re, subprocess\n\nwith open('main.tex') as f: src = f.read()\nlines = src.split('\\n')\n\n# Find sections\nsections = []\nfor i, l in enumerate(lines):\n    m = re.match(r'\\\\section\\*?\\{([^}]+)\\}', l.strip())\n    if m: sections.append(('section', m.group(1), i))\n    m = re.match(r'\\\\subsection\\*?\\{([^}]+)\\}', l.strip())\n    if m: sections.append(('subsection', m.group(1), i))\n    m = re.match(r'\\\\subsubsection\\*?\\{([^}]+)\\}', l.strip())\n    if m: sections.append(('subsubsection', m.group(1), i))\n    if l.strip().startswith(r'\\appendix'): sections.append(('marker', '__APPENDIX__', i))\n    if l.strip().startswith(r'\\bibliography') or l.strip().startswith(r'\\begin{thebibliography}'): sections.append(('marker', '__BIB__', i))\n\ndef section_text(start, end):\n    block = '\\n'.join(lines[start:end])\n    block = re.sub(r'%.*', '', block)\n    for env in ['tikzpicture', r'table\\*?', r'figure\\*?', r'equation\\*?', r'align\\*?', r'algorithm\\*?', 'proof']:\n        block = re.sub(rf'\\\\begin{{{env}}}.*?\\\\end{{{env}}}', '', block, flags=re.S)\n    block = re.sub(r'\\$[^$]*\\$', ' M ', block)\n    block = re.sub(r'\\\\cite[a-z]*\\{[^}]*\\}', ' C ', block)\n    block = re.sub(r'\\\\ref\\{[^}]*\\}', ' R ', block)\n    block = re.sub(r'\\\\label\\{[^}]*\\}', '', block)\n    block = re.sub(r'\\\\[A-Za-z]+\\*?', ' ', block)\n    block = re.sub(r'[{}]', ' ', block)\n    return len(re.findall(r'\\b[A-Za-z][A-Za-z\\-]+\\b', block))\n\ndef cite_count(start, end):\n    block = '\\n'.join(lines[start:end])\n    return len(re.findall(r'\\\\cite[a-z]*\\{[^}]+\\}', block))\n\n# Top-level body sections\nprint(f\"{'Body section':<55}{'words':>7}  {'%':>6}  {'cites':>6}\")\nprint('-'*78)\ntop_idx = [i for i, s in enumerate(sections) if s[0] == 'section']\nappendix_idx = next((i for i, s in enumerate(sections) if s[1] == '__APPENDIX__'), None)\nbib_idx = next((i for i, s in enumerate(sections) if s[1] == '__BIB__'), None)\n\nbody_total = 0\nbody_top = []\nfor k, ti in enumerate(top_idx):\n    if appendix_idx is not None and ti >= appendix_idx: […]

> TOOL

tool_result
id: toolu_01AJdT46THZZYQXAHoLjo7dM
```
Body section                                             words       %   cites
------------------------------------------------------------------------------
Introduction                                               485   20.3%      26
Related Work                                               693   29.1%      52
Raw-Routed Mixture of Adapters (RR-MoA)                    199    8.3%       1
Experiments                                                334   14.0%      23
Conclusion and Limitations                                 674   28.3%       0
------------------------------------------------------------------------------
BODY TOTAL                                                2385  100.0%

Sub-breakdown of Experiments (§4):
  subsection     Setup                                               49w   12c
  subsection     Main Results                                        46w    0c
  subsubsection  Diagnosis: adapters underperform, MoE collapses    265w    2c
  subsubsection  Mechanism: instance normalization strips the routing signal   212w    0c
  subsubsection  Standard rescues fail; the raw-input principle generalizes    49w    5c
  subsubsection  Headline numbers                                    29w    4c

Appendix section                                         words   cites
------------------------------------------------------------------------
------------------------------------------------------------------------
APPENDIX TOTAL                                               0

Body:Appendix word ratio = 1 : 0.00
```

> AGENT

Bug in my script — Conclusion bleeds into bibliography region. Fixing measurement.

> TOOL

tool_use Bash
id: toolu_01G96duhpDuoWBy54KJ7cNVh
```json
{
  "command": "python3 << 'EOF'\nimport re\nwith open('main.tex') as f: src = f.read()\nlines = src.split('\\n')\n\ndef find_first(pattern):\n    for i, l in enumerate(lines):\n        if re.match(pattern, l.strip()): return i\n    return len(lines)\n\nappendix_line = find_first(r'\\\\appendix\\b')\nbib_line = find_first(r'\\\\(bibliographystyle|bibliography\\{|begin\\{thebibliography\\})')\n\ndef section_text(start, end):\n    block = '\\n'.join(lines[start:end])\n    block = re.sub(r'%.*', '', block)\n    for env in ['tikzpicture', r'table\\*?', r'figure\\*?', r'equation\\*?', r'align\\*?', r'algorithm\\*?', 'proof']:\n        block = re.sub(rf'\\\\begin{{{env}}}.*?\\\\end{{{env}}}', '', block, flags=re.S)\n    block = re.sub(r'\\$[^$]*\\$', ' M ', block)\n    block = re.sub(r'\\\\cite[a-z]*\\{[^}]*\\}', ' C ', block)\n    block = re.sub(r'\\\\ref\\{[^}]*\\}', ' R ', block)\n    block = re.sub(r'\\\\label\\{[^}]*\\}', '', block)\n    block = re.sub(r'\\\\[A-Za-z]+\\*?', ' ', block)\n    block = re.sub(r'[{}]', ' ', block)\n    return len(re.findall(r'\\b[A-Za-z][A-Za-z\\-]+\\b', block))\n\ndef cite_count(start, end):\n    block = '\\n'.join(lines[start:end])\n    return len(re.findall(r'\\\\cite[a-z]*\\{[^}]+\\}', block))\n\n# Body: \\section before \\appendix\nbody_secs = [(re.match(r'\\\\section\\*?\\{([^}]+)\\}', l.strip()).group(1), i)\n             for i, l in enumerate(lines)\n             if i < appendix_line and re.match(r'\\\\section\\*?\\{', l.strip())]\n\n# Add appendix line as artificial end-of-body\nbody_secs_with_end = body_secs + [('__END__', appendix_line)]\n\nprint(f\"=== BODY (lines 1..{appendix_line}, before \\\\appendix) ===\")\nprint(f\"{'Section':<55}{'words':>7}  {'%':>6}  {'cites':>6}\")\nprint('-'*78)\nbody_total = 0\nbody_data = []\nfor (name, start), (_, nxt) in zip(body_secs, body_secs_with_end[1:]):\n    wc = section_text(start, nxt)\n    cc = cite_count(start, nxt)\n    body_data.append((name, wc, cc))\n    body_total += wc\nfor name, wc, cc in body_data:\n    print(f\"{name:<55}{wc:>7}  {100*wc/body_total:>5.1f}%  {cc:>6}\")\nprint('-'*78)\nprint(f\"{'BODY TOTAL':<55}{body_total:>7}  100.0%\")\nprint()\n\n# Sub-breakdown of §4 Experiments\nprint(\"=== Experiments §4 sub-breakdown ===\")\nexp_idx = next((i for i, (n, _) in […]

> TOOL

tool_result
id: toolu_01G96duhpDuoWBy54KJ7cNVh
```
=== BODY (lines 1..1027, before \appendix) ===
Section                                                  words       %   cites
------------------------------------------------------------------------------
Introduction                                               485   20.3%      26
Related Work                                               693   29.1%      52
Raw-Routed Mixture of Adapters (RR-MoA)                    199    8.3%       1
Experiments                                                334   14.0%      23
Conclusion and Limitations                                 674   28.3%       0
------------------------------------------------------------------------------
BODY TOTAL                                                2385  100.0%

=== Experiments §4 sub-breakdown ===
  subsection     Setup                                                      49w   12c
  subsection     Main Results                                               46w    0c
  subsubsection  Diagnosis: adapters underperform, MoE collapses           265w    2c
  subsubsection  Mechanism: instance normalization strips the routing signal   212w    0c
  subsubsection  Standard rescues fail; the raw-input principle generalizes    49w    5c
  subsubsection  Headline numbers                                           29w    4c

=== APPENDIX (lines 1027..551) ===
Appendix section                                         words   cites
------------------------------------------------------------------------
------------------------------------------------------------------------
APPENDIX TOTAL                                               0

Body:Appendix word ratio = 1 : 0.00
Total citations in body: 102 | in appendix: 0

=== Pagination check ===
p9 last 2: ['338   downstream rescues have so far blocked.', '                                                                         9']
p10 first 2: ['339   References', '340    [1] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai,']
```

> TOOL

tool_use Bash
id: toolu_01EWRm58qbZuUXr6KdT1PzNz
```json
{
  "command": "python3 << 'EOF'\nimport re, subprocess\nwith open('main.tex') as f: src = f.read()\nlines = src.split('\\n')\n\nbib_line = next((i for i, l in enumerate(lines) if re.match(r'\\\\(bibliographystyle|begin\\{thebibliography\\})', l.strip())), len(lines))\nappendix_line = next((i for i, l in enumerate(lines) if re.match(r'\\\\appendix\\b', l.strip())), len(lines))\nend_of_app = next((i for i, l in enumerate(lines) if re.match(r'\\\\end\\{document\\}', l.strip())), len(lines))\n\ndef section_text(start, end):\n    block = '\\n'.join(lines[start:end])\n    block = re.sub(r'%.*', '', block)\n    for env in ['tikzpicture', r'table\\*?', r'figure\\*?', r'equation\\*?', r'align\\*?', r'algorithm\\*?', 'proof']:\n        block = re.sub(rf'\\\\begin{{{env}}}.*?\\\\end{{{env}}}', '', block, flags=re.S)\n    block = re.sub(r'\\$[^$]*\\$', ' M ', block)\n    block = re.sub(r'\\\\cite[a-z]*\\{[^}]*\\}', ' C ', block)\n    block = re.sub(r'\\\\ref\\{[^}]*\\}', ' R ', block)\n    block = re.sub(r'\\\\label\\{[^}]*\\}', '', block)\n    block = re.sub(r'\\\\[A-Za-z]+\\*?', ' ', block)\n    block = re.sub(r'[{}]', ' ', block)\n    return len(re.findall(r'\\b[A-Za-z][A-Za-z\\-]+\\b', block))\n\ndef cite_count(start, end):\n    return len(re.findall(r'\\\\cite[a-z]*\\{[^}]+\\}', '\\n'.join(lines[start:end])))\n\n# BODY: \\section's between line 0 and bib_line\nbody_secs = [(re.match(r'\\\\section\\*?\\{([^}]+)\\}', l.strip()).group(1), i)\n             for i, l in enumerate(lines[:bib_line])\n             if re.match(r'\\\\section\\*?\\{', l.strip())]\nbody_secs_with_end = body_secs + [('__END__', bib_line)]\n\nprint(f\"BODY (lines 1..{bib_line}):\")\nprint(f\"{'Section':<55}{'words':>6}  {'%':>6}  {'cites':>5}\")\nprint('-'*78)\nbody_total = 0\nbody_data = []\nfor (name, start), (_, nxt) in zip(body_secs, body_secs_with_end[1:]):\n    wc = section_text(start, nxt); cc = cite_count(start, nxt)\n    body_data.append((name, wc, cc)); body_total += wc\nfor name, wc, cc in body_data:\n    print(f\"{name:<55}{wc:>6}  {100*wc/body_total:>5.1f}%  {cc:>5}\")\nprint('-'*78)\nprint(f\"{'BODY TOTAL':<55}{body_total:>6}\")\n\n# APPENDIX\nprint(f\"\\nAPPENDIX (lines {appendix_line}..{end_of_app}):\")\nprint(f\"{'Section':<55}{'words':>6}  {'cites':>5}\")\nprint('-'*72)\napp_secs = [(re.match(r'\\\\section\\*?\\{([^}]+)\\}', l.strip()).group(1), i)\n            for i, l in enumerate(lines)\n […]

> TOOL

tool_result
id: toolu_01EWRm58qbZuUXr6KdT1PzNz
```
BODY (lines 1..551):
Section                                                 words       %  cites
------------------------------------------------------------------------------
Introduction                                              485   27.0%     26
Related Work                                              693   38.7%     52
Raw-Routed Mixture of Adapters (RR-MoA)                   199   11.1%      1
Experiments                                               334   18.6%     23
Conclusion and Limitations                                 82    4.6%      0
------------------------------------------------------------------------------
BODY TOTAL                                               1793

APPENDIX (lines 1027..2818):
Section                                                 words  cites
------------------------------------------------------------------------
Experimental Setup Details                                237      5
Deployment-Regime Motivation                              283      0
Multi-Horizon Evaluation                                   21      0
Proposition Proofs                                        471      3
LoRA Sweep (Full Results)                                 243      1
Routing Ablations                                         238      2
Extended RR-MoA Freeze Grid                                88      1
Normalization Generalization                              415      3
Top-$k$ Sparse Routing Ablation                           115      1
Imputation Results                                         54      0
Learnable Normalization Coefficient                       101      0
Exact MI Loss and Bound Tightness                         104      4
Information Content Diagnostic                             69      0
Cross-Backbone RR-MoA                                      89      2
Extended Full Fine-Tuning Ablation                         69      0
Closing the DLinear Gap                                   992      0
------------------------------------------------------------------------
APPENDIX TOTAL                                           3589     22

Body:Appendix = 1 : 2.00
Total cites: body=102 | appendix=22

§4 Experiments sub-breakdown (lines 389..545):
  subsection     Setup                                                49w  12c
  subsection     Main Results                                         46w   0c
  subsubsection  Diagnosis: adapters underperform, MoE collapses     265w   2c
  subsubsection  Mechanism: instance normalization strips the rou    212w   0c
  subsubsection  Standard rescues fail; the raw-input principle g     49w   5c
  subsubsection  Headline numbers                                     29w   4c

Pagination: PDF has 51 pages
Body content ends […]

> TOOL

tool_use Bash
id: toolu_01UkR1fTSGSi7NuLUxRbqNYe
```json
{
  "command": "python3 << 'EOF'\nimport re\nwith open('main.tex') as f: lines = f.read().split('\\n')\n# Lines 509 (Headline numbers) to 545 (end of §4)\nblock = '\\n'.join(lines[509:545])\nprint(block[:200])\nprint(\"...\")\nprint(block[-200:])\nprint()\n# Strip tables\nb = re.sub(r'\\\\begin\\{table\\*?\\}.*?\\\\end\\{table\\*?\\}', '', block, flags=re.S)\nb = re.sub(r'%.*', '', b)\nb = re.sub(r'\\$[^$]*\\$', ' M ', b)\nb = re.sub(r'\\\\cite[a-z]*\\{[^}]*\\}', ' C ', b)\nb = re.sub(r'\\\\ref\\{[^}]*\\}', ' R ', b)\nb = re.sub(r'\\\\label\\{[^}]*\\}', '', b)\nb = re.sub(r'\\\\[A-Za-z]+\\*?', ' ', b)\nb = re.sub(r'[{}]', ' ', b)\nprint(f\"After stripping: {len(re.findall(r'[A-Za-z][A-Za-z\\-]+', b))} words\")\nprint(f\"Stripped text preview:\")\nprint(' '.join(b.split())[:500])\nEOF",
  "description": "Debug §4.2 Headline subsection word count"
}
```

> TOOL

tool_result
id: toolu_01UkR1fTSGSi7NuLUxRbqNYe
```
{\looseness=-1 Two gains feed the headline: residual shape heterogeneity rewards diverse experts on RevIN-normalized hidden states (Q1; $26$--$79\%$ over the best fixed adapter, Table~\ref{tab:rrmoa}
...
athology}). Together these confirm the diagnosis is task-, horizon-, and backbone-portable rather than tied to the specific MOMENT$+$RevIN combination on which it was first observed.}

\vspace{-0.5em}

After stripping: 28 words
Stripped text preview:
=-1 Two gains feed the headline: residual shape heterogeneity rewards diverse experts on RevIN-normalized hidden states (Q1; M -- M p < 0.001 M 37 M 46\ =-1 Cross-backbone, task, horizon. RR-MoA wins on every instance-normalized backbone tested (MOMENT-small/large M --$79\ -0.5em
```

> TOOL

tool_use Bash
id: toolu_015Vs4JuTt3GGCw1iwv9mcCd
```json
{
  "command": "awk 'NR>=540 && NR<=546 {print NR\": \"$0}' main.tex",
  "description": "Inspect lines after Table 4"
}
```

> TOOL

tool_result
id: toolu_015Vs4JuTt3GGCw1iwv9mcCd
```
540: 
541: RR-MoA beats every baseline at $p{<}0.001$; the no-router ensemble is $37$--$46\%$ worse. \textbf{Closing the DLinear gap.} DLinear (49K params, from scratch) outperforms frozen adapters in absolute MSE (Table~\ref{tab:baselines}, grey rows); k-NN/Ridge diagnostics attribute this to information loss in the normalization--encoding pipeline (Appendix~\ref{app:diagnostic}). Restoring raw access \emph{at the expert level} closes it: \textbf{Residual-IA\textsuperscript{+}} matches or beats DLinear on $6/6$ datasets at $H{=}96$ and $107/123$ cells across six backbones (App.~\ref{app:gate_pathology}); SR-RIA\textsuperscript{+} hits $6/6$ (App.~\ref{app:sr_ria}); a TSFM-free Pure Raw-MLP MoE localizes the TSFM contribution (App.~\ref{app:raw_mlp_moe}).
542: 
543: {\looseness=-1 \textbf{Cross-backbone, task, horizon.}\label{sec:cross_backbone}\label{sec:topk} RR-MoA wins on every instance-normalized backbone tested (MOMENT-small/large $26$--$79\%/32$--$75\%$, Moirai $12$--$29\%$, Moirai-MoE~\citep{liu2025moiraimoe} $37$--$90\%$), and LayerNorm-only Chronos and Timer-XL~\citep{liu2025timerxl} show no collapse — the predicted negative-control split. Beyond forecasting at $H{=}96$, RR-MoA wins $7/8$ imputation cells (App.~\ref{app:imputation}) and $24/24$ multi-horizon cells across $H{\in}\{96,192,336,720\}$ (Tables~\ref{tab:cross_backbone}--\ref{tab:horizon}); Residual-IA\textsuperscript{+} additionally generalizes across the $6{\times}5{\times}4$ dataset $\times$ backbone $\times$ horizon grid (App.~\ref{app:gate_pathology}). Together these confirm the diagnosis is task-, horizon-, and backbone-portable rather than tied to the specific MOMENT$+$RevIN combination on which it was first observed.}
544: 
545: \vspace{-0.5em}
546: \section{Conclusion and Limitations}
```

> TOOL

tool_use Bash
id: toolu_018Zs9qBYp9KYZ1bF7PnPmKY
```json
{
  "command": "python3 << 'EOF'\nimport re\nwith open('main.tex') as f: lines = f.read().split('\\n')\n# Slice file-lines 509..544 (inclusive of subsubsection header through cross-backbone)\nblock = '\\n'.join(lines[508:544])\n# Step-by-step to find where words disappear\nprint(f\"Step 0 (raw): {len(re.findall(r'[A-Za-z]+', block))} alphabetic tokens\")\nb = re.sub(r'%.*', '', block); print(f\"Step 1 (no comments): {len(re.findall(r'[A-Za-z]+', b))}\")\nb = re.sub(r'\\\\begin\\{table\\*?\\}.*?\\\\end\\{table\\*?\\}', '', b, flags=re.S); print(f\"Step 2 (no tables): {len(re.findall(r'[A-Za-z]+', b))}\")\nb2 = re.sub(r'\\$[^$]*\\$', ' M ', b); print(f\"Step 3 (no math): {len(re.findall(r'[A-Za-z]+', b2))}\")\nb3 = re.sub(r'\\\\cite[a-z]*\\{[^}]*\\}', ' C ', b2); print(f\"Step 4 (no cite): {len(re.findall(r'[A-Za-z]+', b3))}\")\nb4 = re.sub(r'\\\\ref\\{[^}]*\\}', ' R ', b3); print(f\"Step 5 (no ref): {len(re.findall(r'[A-Za-z]+', b4))}\")\nb5 = re.sub(r'\\\\label\\{[^}]*\\}', '', b4); print(f\"Step 6 (no label): {len(re.findall(r'[A-Za-z]+', b5))}\")\nb6 = re.sub(r'\\\\[A-Za-z]+\\*?', ' ', b5); print(f\"Step 7 (no \\\\cmd): {len(re.findall(r'[A-Za-z]+', b6))}\")\nb7 = re.sub(r'[{}]', ' ', b6); print(f\"Step 8 (no braces): {len(re.findall(r'[A-Za-z]+', b7))}\")\nprint()\nprint(\"Step-7 output (first 500 chars):\")\nprint(b6[:500])\nEOF",
  "description": "Step-by-step regex debug"
}
```

> TOOL

tool_result
id: toolu_018Zs9qBYp9KYZ1bF7PnPmKY
```
Step 0 (raw): 452 alphabetic tokens
Step 1 (no comments): 202
Step 2 (no tables): 60
Step 3 (no math): 52
Step 4 (no cite): 52
Step 5 (no ref): 52
Step 6 (no label): 45
Step 7 (no \cmd): 41
Step 8 (no braces): 41

Step-7 output (first 500 chars):
 {Headline numbers}

{ =-1 Two gains feed the headline: residual shape heterogeneity rewards diverse experts on RevIN-normalized hidden states (Q1;  M -- M p{<}0.001 M 37 M 46\

{ =-1  {Cross-backbone, task, horizon.} RR-MoA wins on every instance-normalized backbone tested (MOMENT-small/large  M --$79\
```

> AGENT

Bug found in my script: `%.*` regex was eating after `\%` (escaped percent) too. Re-measuring with the fix.

> TOOL

tool_use Bash
id: toolu_01Ghw4ny1N6K7qZ39cc3Q3S5
```json
{
  "command": "python3 << 'EOF'\nimport re, subprocess\nwith open('main.tex') as f: src = f.read()\nlines = src.split('\\n')\n\nbib_line = next((i for i, l in enumerate(lines) if re.match(r'\\\\(bibliographystyle|begin\\{thebibliography\\})', l.strip())), len(lines))\nappendix_line = next((i for i, l in enumerate(lines) if re.match(r'\\\\appendix\\b', l.strip())), len(lines))\nend_of_app = next((i for i, l in enumerate(lines) if re.match(r'\\\\end\\{document\\}', l.strip())), len(lines))\n\ndef section_text(start, end):\n    block = '\\n'.join(lines[start:end])\n    # FIX: only strip comments where % is NOT preceded by backslash\n    block = re.sub(r'(?<!\\\\)%.*', '', block)\n    for env in ['tikzpicture', r'table\\*?', r'figure\\*?', r'equation\\*?', r'align\\*?', r'algorithm\\*?', 'proof']:\n        block = re.sub(rf'\\\\begin{{{env}}}.*?\\\\end{{{env}}}', '', block, flags=re.S)\n    block = re.sub(r'\\$[^$]*\\$', ' M ', block)\n    block = re.sub(r'\\\\cite[a-z]*\\{[^}]*\\}', ' C ', block)\n    block = re.sub(r'\\\\ref\\{[^}]*\\}', ' R ', block)\n    block = re.sub(r'\\\\label\\{[^}]*\\}', '', block)\n    block = re.sub(r'\\\\[A-Za-z]+\\*?', ' ', block)\n    block = re.sub(r'[{}]', ' ', block)\n    return len(re.findall(r'\\b[A-Za-z][A-Za-z\\-]+\\b', block))\n\ndef cite_count(start, end):\n    return len(re.findall(r'\\\\cite[a-z]*\\{[^}]+\\}', '\\n'.join(lines[start:end])))\n\n# BODY sections\nbody_secs = [(re.match(r'\\\\section\\*?\\{([^}]+)\\}', l.strip()).group(1), i)\n             for i, l in enumerate(lines[:bib_line])\n             if re.match(r'\\\\section\\*?\\{', l.strip())]\nbody_ends = [s[1] for s in body_secs[1:]] + [bib_line]\n\nprint(\"=\"*78)\nprint(f\"BODY (lines 1..{bib_line})\")\nprint(\"=\"*78)\nprint(f\"{'Section':<55}{'words':>6}  {'%':>6}  {'cites':>5}\")\nprint('-'*78)\nbody_total = 0; body_data = []\nfor (name, start), nxt in zip(body_secs, body_ends):\n    wc = section_text(start, nxt); cc = cite_count(start, nxt)\n    body_data.append((name, wc, cc)); body_total += wc\nfor name, wc, cc in body_data:\n    print(f\"{name:<55}{wc:>6}  {100*wc/body_total:>5.1f}%  {cc:>5}\")\nprint('-'*78)\nprint(f\"{'BODY TOTAL':<55}{body_total:>6}          {sum(c for _,_,c […]

> TOOL

tool_result
id: toolu_01Ghw4ny1N6K7qZ39cc3Q3S5
```
==============================================================================
BODY (lines 1..551)
==============================================================================
Section                                                 words       %  cites
------------------------------------------------------------------------------
Introduction                                              616   19.0%     26
Related Work                                              693   21.3%     52
Raw-Routed Mixture of Adapters (RR-MoA)                   402   12.4%      1
Experiments                                              1350   41.6%     23
Conclusion and Limitations                                186    5.7%      0
------------------------------------------------------------------------------
BODY TOTAL                                               3247            102

§4 Experiments sub-breakdown
------------------------------------------------------------------------------
  subsection     Setup                                                 219w  12c
  subsection     Main Results                                           46w   0c
  subsubsection  Diagnosis: adapters underperform, MoE collapses       395w   2c
  subsubsection  Mechanism: instance normalization strips the routi    247w   0c
  subsubsection  Standard rescues fail; the raw-input principle gen    238w   5c
  subsubsection  Headline numbers                                      204w   4c
  (sum of §4 sub-blocks: 1349w)

==============================================================================
APPENDIX (lines 1027..2818)
==============================================================================
Section                                                 words  cites
------------------------------------------------------------------------
Experimental Setup Details                                237      5
Deployment-Regime Motivation                              439      0
Multi-Horizon Evaluation                                   69      0
Proposition Proofs                                        729      3
LoRA Sweep (Full Results)                                 370      1
Routing Ablations                                         687      2
Extended RR-MoA Freeze Grid                               340      1
Normalization Generalization                              415      3
Top-$k$ Sparse Routing Ablation                           301      1
Imputation Results                                        116      0
Learnable Normalization Coefficient                       101      0
Exact MI Loss and Bound Tightness                         243      4
Information Content Diagnostic                            175      0
Cross-Backbone RR-MoA                                     158      2
Extended Full Fine-Tuning Ablation                        227      0
Closing the DLinear Gap                                  3009      0
------------------------------------------------------------------------
APPENDIX TOTAL                                           7616     22

Body:Appendix word ratio = 1 : 2.35
```

> AGENT

## Round-2 review: corrected measurement

**I have to flag this honestly: the previous percentages were wrong.** My measurement script had a bug — the comment-stripping regex `%.*` was treating `\%` (escaped percent in MSE deltas like `26\%`) as the start of a LaTeX comment and deleting everything after it on the line. This systematically undercounted any section dense with percentage figures (Method, Experiments, Conclusion). Related Work — which uses fewer percent signs — was undercounted least, so it falsely appeared to dominate.

### Corrected body distribution

| Section | Words | % of body | Cites | Cite density |
|---|---:|---:|---:|---:|
| Introduction | 616 | 19.0% | 26 | 1 / 24w |
| Related Work | 693 | **21.3%** | 52 | 1 / 13w |
| Method (RR-MoA) | 402 | 12.4% | 1 | 1 / 402w |
| Experiments | 1350 | **41.6%** | 23 | 1 / 59w |
| Conclusion | 186 | 5.7% | 0 | — |
| **Body total** | **3247** | 100% | 102 | 1 / 32w |

### §4 Experiments sub-distribution

| Block | Words | Cites |
|---|---:|---:|
| Setup | 219 | 12 |
| […]