# Projects

## Mathews-Tom/no-magic ★ (dominant — 100% of sessions)

**What the user does here**: Designs and builds an educational ML repository implementing foundational ML algorithms from scratch in Python. Each script is a self-contained pedagogical unit covering one algorithm, with no external dependencies. Mathews-Tom acts as the architect and project lead — he writes the implementation specs, orchestrates multi-agent implementation waves, validates results, and manages the git workflow.

**Tech stack**: Python 3 (stdlib only — `os`, `math`, `random`, `urllib.request`, `collections`). No pip packages. Scripts run standalone with `python script.py`.

**Repository structure**:
```
01-foundations/   — 7 scripts (BPE tokenizer, embeddings, GPT, RNN/GRU, RAG, diffusion, VAE)
02-alignment/     — 4 scripts (LoRA, DPO, PPO, MoE)
03-systems/       — 5 scripts (attention variants, KV cache, quantization, flash attention, beam search)
docs/             — implementation.md, autograd-interface.md, overview
CONTRIBUTING.md   — comment density standard, section header format, quality checklist
.claude/CLAUDE.md — agent instructions (gitignored)
```

**Canonical conventions (enforced by Mathews-Tom)**:
- `from __future__ import annotations` as first import
- `random.seed(42)` after imports
- Section headers: `# === SECTION NAME ===`
- File thesis as top docstring (one sentence)
- Data auto-download via `urllib` + local cache (gitignored)
- `if __name__ == "__main__":` guard
- 30–40% comment/blank line density
- 100 char max line width, 4-space indent, f-strings
- Runtime < 7 minutes on M-series Mac
- Zero external imports

**Canonical autograd**: A `Value` scalar autograd class defined in `docs/autograd-interface.md`. All scripts that need autograd reimplement it from scratch inline — no shared module, no imports.

**Training dataset**: `names.txt` from Karpathy's makemore repo (auto-downloaded, gitignored). Used by all language-modeling scripts.

**Reference architecture**: Karpathy's microgpt gist is the canonical GPT-2 reference (RMSNorm not LayerNorm, no biases, ReLU not GELU). Attribution preserved in file headers.

**Phase sequencing**: Scripts are organized by implementation phases (1–7) based on dependency complexity:
- Phase 1: BPE tokenizer (no autograd)
- Phase 2: Attention, Embedding (forward-pass only)
- Phase 3: GPT, LoRA (full autograd)
- Phase 5: DPO, PPO (full autograd)
- Phase 6: KV cache, quantization, flash attention (inference-focused)
- Phase 7: MoE, beam search (most complex)

**Recurring implementation themes**:
- Pedagogical clarity over performance — comments explain the WHY, not just the WHAT
- Explicit math-to-code mappings in comments (e.g., `z = mu + exp(0.5 * log_var) * epsilon`)
- Comparison tables in output (before/after, with/without, architecture variants)
- "Signpost" comments pointing to production-scale equivalents (e.g., "production tokenizers use 50K+ merges")
- Hybrid autograd/plain-float patterns where training uses `Value` and inference uses plain floats

**Git workflow**: Feature branches (`feat/alignment-systems`, `feat/foundations`) → multiple semantic commits → PR to main → validate by running all new scripts → merge. Mathews-Tom merges PRs himself after reviewing validation output.
