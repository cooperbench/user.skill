> DEVELOPER

We should address this issue: https://github.com/armelhbobdad/bmad-module-skill-forge/issues/427 . We may need party mode or advanced elicitation.

> AGENT

I'll start by looking at the issue to understand what we're addressing.

> AGENT

This is a design problem, as the issue itself notes — it needs new signals that aren't in the current manifest-only flow. Before I bring in party mode or advanced elicitation, let me understand the surrounding pipeline so the design discussion is grounded in what's actually feasible. Let me explore.

> AGENT

I've mapped the terrain. Here's the crucial finding that reframes the whole issue: ## The deeper problem: the script can't see the signals it would need The issue proposes new signals (grammar files, repo name/topics, directory structure). But the pipeline **only fetches manifests** — `step-auto-scope.md` clones with `--filter=blob:none --sparse-checkout` restricted to `package.json`/`Cargo.toml`/`pyproject.toml`. `skf-shape-detect.py` receives only manifest *paths*. So none of the proposed signals (`.pest`/`.lalrpop` files, GitHub topics, `src/parser/` tree) are available where classification happens today. That makes #427 not a one-line heuristic tweak but a **3-layer design problem**: | Layer | Question | Current state | |---|---|---| | **Signal acquisition** | What new inputs do we fetch, and how (sparse-checkout more paths? GitHub API for topics? scan dir structure)? | Manifests only | | **Classification** | How does `language-reference` fire from *producer* signals without false-positiving every repo with a `src/parser/` dir? | Inverted (consumer deps only) | | **Downstream usefulness** | `language-reference` → `full-library` unconditionally, and there's **no multi-corpus concept** — so even if it fires, the resulting skill (compiler code with no Book/std-docs) may be low-value | scope_type enum doesn't even include a language notion | The issue's own acceptance note concedes this: *"likely also needs the multi-corpus concept […]

> AGENT

You chose party mode. Let me convene the roundtable on this design problem.

> AGENT

The roundtable is convened. I'll bring in **Winston** (Architect), **John** (PM), and **Mary** (Analyst) on this — exactly the three lenses the problem needs.

> AGENT

Here's the roundtable. --- 🏗️ **Winston:** Let me get to the whiteboard, because the way you've framed this — three layers — is exactly right, and the most important architectural move here is to *not* treat them as one purchase. **Layer 1 — signal acquisition, by blast radius.** Cheapest: scan the manifest contents we already have. Zero new I/O, no network, no auth — but the *weakest* signal, and it does nothing for `rust-lang/rust` whose top-level manifest is a workspace stub. Middle: widen sparse-checkout to grammar-file globs (`*.pest`, `*.lalrpop`, `*.y`, `*.g4`). Blast radius contained to the fetch step we already own; a `.pest` file is a *near-certain producer signal* — grammar files are how you build a language, not consume one. Most expensive: a GitHub API call for topics. This is the one I'd push back on hardest — it makes GitHub a hard dependency of classification, introduces auth/rate-limit/offline failure modes, and that liability outlives this issue. Ranked by signal-quality-per-unit-blast-radius: **grammar-file globs win.** **Can we fire from manifests we ALREADY fetch?** Partially — invert the *interpretation*. Today "depends on pest → language-reference." Replace with "manifest declares parsing/grammar metadata about *itself*." That catches the easy half (well-tagged parsing libs) but `rust-lang/rust` […]