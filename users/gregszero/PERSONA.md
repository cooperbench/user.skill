---
name: persona
description: gregszero's background, expertise, seniority signals, and attitude toward the agent
metadata:
  type: user
---

# Persona

## Role (inferred)

Indie developer / founder building his own AI-first productivity framework. Works on a single repo (`gregszero/open-fang`) exclusively. No teammates visible in the data — solo project. The framework is the product, not a side tool.

## Technical background

**Strong expertise:**
- Ruby (ActiveRecord, Roda, Sinatra patterns, concerns, zeitwerk, jobs, migrations — writes idiomatic Ruby in spec-dumps)
- Web frameworks: Roda, Rack, Puma, Turbo Streams / Stimulus JS, ERB
- AI tooling: Claude Code, MCP tools, FastMcp gem, Claude API, streaming JSON events
- Architecture: event buses, background jobs, SSE, canvas-based UIs, widget systems

**Comfortable with:**
- Tailwind CSS / custom CSS design tokens, HSL-based theming, dark/light mode
- SQLite / ActiveRecord migrations
- Shell tools, Xvfb, headless Linux environments
- OAuth2 flows (Gmail integration)
- Cron expressions, scheduler patterns (rufus-scheduler, fugit)

**Approach to AI agents:**
- Treats Claude Code as a contractor: gives detailed specs, expects full execution, checks results visually
- Pre-authors plans offline (often as structured Markdown with ## headings, tables, code blocks), then pastes them as opening prompts
- Does NOT want the agent to think out loud or explain its decisions
- Does NOT want the agent to refuse things the framework already supports

## Seniority signals (inferred)

Senior / experienced. Writes migration schemas, model concerns, job patterns, and MCP tool structures from scratch with fluency. Designs token-efficiency improvements himself (modular prompts, tool groups, context compression). References specific gem versions, spots root-cause bugs in stack traces.

## Attitude toward the agent

- **Expects execution**: pastes a plan → wants it done
- **Skeptical of summaries**: accepts work with "commit this", not with "great, here's what I did"
- **Corrects confidently**: when something is wrong visually or functionally, gives a precise short redirect
- **Impatient with over-explanation**: the `correction` pushback pattern shows him overriding when the agent offers alternatives instead of acting
- **Names the inner agent "Ned"**: refers to the embedded AI in his framework as "Ned" (separate from Claude Code itself)
- **Tolerates failures calmly**: pastes errors without frustration markers, just "it doesn't work" or raw stderr
