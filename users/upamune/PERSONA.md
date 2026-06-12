# Persona

## Identity

- **GitHub handle**: upamune
- **Language default**: Japanese (59%), English (41%); code-switches fluidly within a single message
- **Location / setup** (inferred): macOS, Apple Silicon (darwin-arm64 compile targets visible in build commands); Bun runtime as primary JS engine

## Role and seniority (inferred)

Experienced systems-oriented TypeScript developer, likely senior IC or indie hacker. Signals:
- Arrives with fully-formed architecture plans (CoW overlay FS, adapter patterns, manifest serialization) rather than asking for design guidance
- Reads SDK source to understand missing features (`agentfs-sdk` lacks OverlayFS → self-implements)
- Knows Bun internals, SQLite adapter nuances, Vercel AI SDK streaming/tool-call contract
- References CI YAML, type errors by `TS2345` code, and `@ts-expect-error` directives fluently

## Domain

Building `zi`: a terminal coding-agent CLI that wraps an LLM with FS isolation (Copy-on-Write overlay over real filesystem, SQLite-backed delta layer) and multi-provider AI (Anthropic, OpenAI, Kimi via Vercel AI SDK). The project is infrastructural, not product-facing.

## Attitude toward the agent

**Mostly trusting, occasionally micromanaging.** Delegates large implementation blocks freely—hands the agent a 1000-word spec and says "Implement the following plan." Does not ask for explanations of agent choices. However:
- Issues sharp one-line corrections when the agent misses workflow steps ("branch 切って" after agent starts committing without branching)
- Interrupts mid-run with `[Request interrupted by user]` without explanation
- Pushes back via raw log paste when CI fails—expects the agent to parse it; no hand-holding

Persona annotation from dataset: **Expert Nitpicker** (57%), **Vague Requester** (29%), **Mind Changer** (14%). The nitpicker side shows in workflow corrections; the vague side shows in terse mid-session pivots ("実装しよう", "お願い").
