---
name: spec-dump-kickoff
description: Opens a new implementation session by pasting a fully pre-written technical plan prefixed with "Implement the following plan:". Triggered when penso has already done the design work himself (in Claude Code plan mode) and wants the agent to execute without further discussion.
---

## Behavior

penso writes the full implementation plan himself — complete with `##` sections, exact file paths, line numbers, code snippets, rationale, constraints, and edge cases — then opens the session with:

```
Implement the following plan: # Plan: <Title>
## Context
…
## 1. <Section>
**Files:** …
**Changes:** …
```

The plan is exhaustive (400–1200 words). It names every file to touch, every function to change, and often includes the exact code or pseudocode to use. There is no preamble, no "hi", no request for feedback on the plan. The plan *is* the message.

## What follows

After pasting, penso says nothing until the agent produces output. If implementation succeeds, he says `"commit, push, create a PR"`. If tests fail, he pastes CI output. Rarely adds mid-session guidance unless the agent misreads a constraint.

## Verbatim examples

**Example 1 (versioning migration, 1173 words):**
> "Implement the following plan: # Plan: Migrate to Date-Based Release Versioning (YYYYMMDD.NN) ## Context Migrate moltis from semver (`v0.10.18`) to date-based versioning (`20260311.01`) matching the arbor project pattern. The user-facing version becomes `YYYYMMDD.NN` (date + daily sequence number). Cargo.toml stays at a static `0.1.0` since Cargo enforces semver, and the real version is injected at build time via `MOLTIS_VERSION` env var. ## 1. Runtime Version Resolution **Files:** - `crates/gateway/src/state.rs` (line 478) …"

**Example 2 (GitHub Copilot Responses API, 698 words):**
> "Implement the following plan: # Fix: GitHub Copilot provider — Responses API support for gpt-5.4+ ## Context GitHub Copilot provider (`crates/providers/src/github_copilot.rs`) hardcodes `/chat/completions` for all models. Newer OpenAI models (gpt-5.4, gpt-5.4-pro, gpt-5.2-pro) only support the Responses API (`/responses`), returning HTTP 400 with `unsupported_api_for_model`. …"
