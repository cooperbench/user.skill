---
name: persona-robertdurst
description: Background, expertise, role, and attitude for robertDurst
metadata:
  type: user
---

# Persona: robertDurst

## Role and seniority (inferred)

Founder-level IC at Brickell Research (inferred). Not an employee following specs — he *sets* the architectural direction and decides what to build next. Operates with high autonomy and context; no manager approval loop visible.

## Domain expertise

**Deep:**
- Compiler architecture — knows the full pipeline: tokenizer → parser → validator → lowering → linker → semantic analyzer → codegen. Talks fluently about ASTs, IRs, artifact graphs, semantic phases.
- Gleam language — reads and writes Gleam fluently; spots boilerplate and redundancy at a glance.
- LSP protocol — understands `textDocument/hover`, diagnostics, cross-file reference tracking, debouncing patterns.
- SRE / SLOs — knows error budgets, composite SLO math (serial vs. parallel dependencies), assume/guarantee contracts.
- Terraform codegen — understands provider configs, HCL resource generation.

**Working knowledge:**
- TypeScript/Deno (the LSP server wrapper layer)
- Multi-agent orchestration (team agents, parallel task fans)

## Attitude toward the agent

**Expert Nitpicker** (annotated persona, 50% of sessions). Trusts the agent to explore and implement, but verifies everything. Spawns parallel verification fleets. Pushes back firmly when the agent over-explains, stalls for clarification, or produces subtly wrong code.

**Vague Requester** (annotated persona, 33% of sessions). Often opens with a broad directive ("kick off a bunch of teams that look into how to make the compiler pipeline here simpler and more concise") and sharpens requirements mid-session once agents surface constraints.

**Mind Changer** (annotated persona, 17%). Will pivot or add scope mid-session: "ok, can we now go back to our list?" / "lets first do A + B + C."

## Communication style summary

Speaks to the agent like a senior engineer directing a junior colleague: expects initiative, hates hand-holding questions, values brevity and correctness over completeness. Will forward raw agent output as context rather than paraphrase it — expects the agent to process it directly.
