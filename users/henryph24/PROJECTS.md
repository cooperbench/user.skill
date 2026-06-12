# PROJECTS — henryph24

## henryph24/neuralips26 ★ (dominant — 100% of sessions)

**What it is:** A NeurIPS 2026 paper submission. The paper proposes **Raw-Routed Mixture of Adapters
(RR-MoA)** for Time Series Foundation Models — it diagnoses that RevIN normalization causes routing
collapse in standard MoE adapters, and fixes it by routing on raw pre-normalization input while
keeping the TSFM backbone strictly frozen.

**Submission deadline:** ~May 2026 (NeurIPS 2026). Active coding window: April 5–18, 2026.

**Tech stack:**
- Python / PyTorch (main experiment script: `run_rr_moa.py`)
- LaTeX / NeurIPS 2026 style (`main.tex`, `neurips_2026.sty`)
- RACE VM: AWS A10G GPU (23 GB VRAM), `ec2-13-238-161-176.ap-southeast-2.compute.amazonaws.com`
- SSH key: `hungphanphd.pem` (repo root, `chmod 400`)
- tmux for experiment sessions; `.log` files for progress
- Overleaf + GitHub sync for PDF preview
- Exa MCP for academic literature search
- GPT-4o for simulated reviewer scoring

**Key methods in the paper:**
- **RR-MoA** — Raw-Routed Mixture of Adapters (headline method; 20/21 wins across forecasting +
  imputation, 56% avg MSE improvement)
- **AAS** — Adapter Architecture Search (discovers expert pool via LLM-guided NAS)
- **T-ZCP** — Temporal Zero-Cost Proxies (training-free architecture scoring)
- **AdaMix** — the baseline MoE that collapses under RevIN (routing entropy → 0.000)

**Datasets used:** ETTh1, ETTh2, ETTm1, ETTm2, Weather, Electricity, Exchange, Solar (LSTF benchmarks)

**Baselines compared:** DLinear, PatchTST, LoRA, TRACE, independent ensembles; backbones:
MOMENT-small/large, Moirai, Moirai-MoE, Chronos, Timer-XL

**Recurring experiment themes:**
- Multi-seed sweeps (3 seeds) across 6+ datasets × 3 freeze levels
- Expert count scaling (K = 3, 5, 7, 10)
- Entropy regularization ablations (λ = 0.01, 0.1, 1.0)
- Cross-backbone generalization (5–6 backbones)
- Router architecture variants (Conv1d, FFT-Router, SSR [μ,σ])
- RDGF, RR-LoRA, CASR, IA-Gating (advanced architectural experiments)
- Multi-horizon forecasting (multiple prediction lengths)
- Imputation task (swapping forecasting head)

**LaTeX pain points:** NeurIPS page limit (9 pages), appendix ordering (must come after references),
bibliography style (IEEE numeric `[1]`), duplicate appendix sections from rapid rewrites,
broken `\ref{}` pointers, math formatting errors in equations.

**Target score:** 8+ for "solid acceptance"; 9 for "Spotlight or Oral"; current work is a
persistent push upward after each reviewer critique.
