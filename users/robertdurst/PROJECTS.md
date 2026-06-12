---
name: projects-robertdurst
description: Repos and projects for robertDurst, inferred from session prompts
metadata:
  type: project
---

# Projects: robertDurst

## Brickell-Research/caffeine_lang *(dominant — 100% of sessions)*

**What it is:** A Gleam-based compiler and DSL for SLO management. Users write `.caffeine` files (blueprints + expectations) that the compiler validates and transforms into Terraform HCL for observability vendors.

**Tech stack:**
- **Compiler:** Gleam (compiles to both Erlang and JavaScript targets)
- **LSP server:** TypeScript/Deno (`lsp_server.ts`, 980+ lines), with Gleam intelligence modules compiled to `.mjs`
- **CLI:** Gleam (`caffeine_cli`)
- **Output:** Terraform HCL for Datadog, Honeycomb, Dynatrace, NewRelic

**Compiler pipeline:**
```
Tokenizer → Parser → Validator → Lowering → Linker → Semantic Analyzer → Codegen
```

**Key packages:**
- `caffeine_lang/` — the core compiler (frontend, linker, analysis, codegen)
- `caffeine_lsp/` — 20 Gleam LSP intelligence modules (diagnostics, hover, completion, go-to-def, etc.)
- `caffeine_cli/` — CLI entrypoint

**Recurring themes in sessions:**
- **Refactoring the compiler for simplicity:** Eliminating duplicate type hierarchies (`ParsedType` vs `AcceptedTypes`), redundant IR fields (`values` + `artifact_data`), vendor boilerplate across codegen modules.
- **LSP feature development:** Adding dependency relation go-to-definition and squiggle diagnostics for missing relations. Cross-file workspace indexing.
- **Correctness verification:** Spinning up 10-agent fleets to verify new LSP diagnostic code against real AST structures.
- **Assume/Guarantee SLO model:** Exploring formal methods for SLO dependency composition (serial/parallel math, error budgets, assume/guarantee contracts) as a Caffeine language feature.

**File paths seen in sessions:**
- `/Users/rdurst/BrickellResearch/caffeine/` (root)
- `caffeine_lang/src/caffeine_lang/compiler.gleam`
- `caffeine_lang/src/caffeine_lang/frontend/parser.gleam`
- `caffeine_lang/src/caffeine_lang/frontend/validator.gleam`
- `caffeine_lang/src/caffeine_lang/linker/ir.gleam`
- `caffeine_lang/src/caffeine_lang/analysis/semantic_analyzer.gleam`
- `caffeine_lang/src/caffeine_lang/analysis/dependency_validator.gleam`
- `caffeine_lang/src/caffeine_lang/codegen/datadog.gleam` (and honeycomb, dynatrace, newrelic)
- `caffeine_lsp/src/caffeine_lsp/diagnostics.gleam`
- `caffeine_lsp/src/caffeine_lsp/definition.gleam`
- `lsp_server.ts`
