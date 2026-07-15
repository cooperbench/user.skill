> DEVELOPER

subtitle named such as: "Headline numbers", "Generalization and falsifiable boundary"

> AGENT

Your message looks truncated — I see only "subtitle named such as: 'Headline numbers', 'Generalization and falsifiable boundary'" without a verb/instruction. Just so we're on the same page, in `main.tex` (Section 4 Main Results) I see four `\subsubsection*` titles plus one bold paragraph header acting as a fifth title: - L428 `\subsubsection*{Diagnosis: adapters underperform, MoE collapses}` - L510 `\subsubsection*{Empirical verification of the mechanism}` - L518 `\subsubsection*{Standard rescues fail; the raw-input principle generalizes}` - L526 `\subsubsection*{Headline numbers}` - L561 `\textbf{Generalization and falsifiable boundary.}` (paragraph-level, not a real subsubsection) What would you like me to do — promote `Generalization and falsifiable boundary` to a `\subsubsection*` to match the others, rename them, add new ones, or something else?

> DEVELOPER

they are bad, review all such sub title (same level) and come up with new ones

> AGENT

Surveyed all 8 same-level subtitles (4 in §4 main body + 1 paragraph-header acting as one + 3 in App. K). Each existing title is either bare-topic ("Headline numbers"), generic-noun-pair ("Generalization and falsifiable boundary"), or wordy/two-clause ("Standard rescues fail; the raw-input principle generalizes"). Aim: parallel form across the §4 arc — each subtitle is an assertive claim with a verb, not a topic label. Drop blog-style ("Headline") and vague generic-nouns ("Generalization", "Empirical verification of the mechanism"). ## Proposed replacements ### §4 Main Results (the narrative arc) | L | Current | Proposed | |---|---|---| | 428 | Diagnosis: adapters underperform, MoE collapses | **Fixed adapters underperform; standard MoE collapses** | | 510 | Empirical verification of the mechanism | **$R(\mathcal{D})$ makes three predictions, and all three hold** | | 518 | Standard rescues fail; the raw-input principle generalizes | **Optimization-side rescues fail; raw-input fixes transfer** | | 526 | Headline numbers | **RR-MoA leads the seven-baseline suite** | | 561 | \textbf{Generalization and falsifiable boundary.} (bold paragraph) | **The diagnosis transfers, and predicts where it should not** | ### Appendix K (Residual-IA gap-closing) | L | Current | Proposed | |---|---|---| | 2634 | Residual-IA⁺: closing the remaining gap to […]