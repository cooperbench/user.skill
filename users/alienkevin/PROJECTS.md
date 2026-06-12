# Projects: AlienKevin

## marin-community/marin ★ DOMINANT (100% of sessions)

AlienKevin works exclusively in this repo across all 15 sessions.

**What he does here**: Reproduces agentic SFT training runs from published papers, runs evaluation pipelines on TerminalBench and SWE-bench, manages TPU cluster resources on the Iris cluster, and tracks all progress via GitHub issue comments.

**Tech stack**:
- Training: Levanter (JAX-based), `SimpleSFTConfig`, HuggingFace model import/export
- Infrastructure: Iris cluster (NOT Ray), v5p-32/64/256 TPU slices, GCS (`gs://marin-us-central1/`)
- Eval: Harbor eval runner, Daytona cloud sandboxes, TerminalBench 2.0, TB-Lite, SWE-bench
- Models: Qwen3-8B base, Nemotron-Terminal-8B (from Qwen3-8B SFT), OpenThoughts-Agent SFT
- Datasets: `DCAgent/exp_tas_optimal_combined_traces` (32K), `DCAgent2/GLM-4.7-r2egym_sandboxes-maxeps-131k` (131K)
- Benchmarks: Terminal-Bench 2.0 (89 tasks), TB-Lite (100 tasks, then discovered to be truncated to 58 in some releases), SWE-bench
- Monitoring: WandB, `uv run scripts/ray/cluster.py`, `gcloud storage ls/cat`
- Git: Multiple worktrees — `~/marin-harbor` (main eval), `~/marin-agentic-sft` (32K SFT branch `kevin/agentic-sft`), `~/marin-agentic-sft-131k` (131K branch `kevin/agentic-sft-131k`)

**Recurring experiments**:
- `exp3490`: Reproduce NemotronTerminal-8B on TB2 and TB-Lite (GitHub issue #3490)
- `exp3490b`: Full SFT of Nemotron traces, 5% and 100% data subsets
- `exp3896`: Reproduce OpenThoughts-Agent 32K SFT (GitHub issue #3896)
- `exp3897`: Reproduce OpenThoughts-Agent 131K SFT (GitHub issue #3897)

**Recurring themes**:
- Context length scaling (32K → 131K) with YaRN RoPE, gradient offloading, v5p-256
- Think-token normalization: `<think>` vs `<|start_think|>` — a recurring source of eval quality bugs
- Checkpoint resumption across TPU regions (MARIN_PREFIX must match region)
- Daytona sandbox concurrency: only 1 Harbor eval job at a time
- Paper-to-reproduction gap: tracking ±2–7 percentage point differences and root-causing them
