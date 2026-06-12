---
name: cyyeh-persona
description: Background, expertise, and attitude for cyyeh
---

# Persona

## Role and Background

cyyeh is a software engineer building a personal/startup-level AI data agent project (inferred). He works across the full stack: Python FastAPI backend, React/TypeScript frontend, Docker/sidecar infrastructure, LLM integrations (Claude Agent SDK, bifrost LLM gateway, langfuse observability). He owns the entire codebase and ships alone or with one collaborator (wanshicheng). (inferred: founder/solo IC level)

## Domain Expertise

- **Strong**: Python backend (FastAPI, uvicorn, DuckDB), React/TypeScript frontend, Docker/docker-compose, Claude Agent SDK, MCP protocol, LLM routing and proxy layers
- **Solid**: Git workflows (branches, worktrees, PRs, merging), containerization, observability (langfuse)
- **Working knowledge**: OpenAI-compatible APIs, bifrost gateway config, vega-lite/plotly charting, i18n

## Seniority Signals

- Knows what he wants architecturally before describing it; skips prerequisites
- Proposes specific env var naming conventions (`@haiku`, `@opus`, `@sonnet` suffixes) and knows why they're needed
- Identifies failure modes at the right layer (frontend cache vs. backend persistence vs. sidecar streaming)
- Uses Claude Code skills (systematic-debugging, writing-plans, brainstorming) deliberately as process guardrails, not as help requests
- When the agent's answer is wrong, corrects with precision ("only update bifrost/config.example.json, bifrost/README.md and backend/.env.example") rather than vagueness

## Attitude Toward the Agent

- **Largely trusting**: delegates most implementation; lets agent pick how to do it
- **Fast to correct**: if the output misses a specific constraint he sees immediately, he flags in one sentence
- **Not a hand-holder**: never explains context the agent could read from the code
- **Impatient with repeated failures**: after 2–3 failed fix attempts, invokes systematic-debugging skill as a process reset rather than explaining more
- **Takeover-prone on git**: if git commands stall or produce wrong results (~6% of pushbacks), he takes over and issues a combined "create new branch and commit and push and merge" command himself

## Tone

- Lowercase, direct, no pleasantries
- No "please" or "thank you" except occasionally embedded in a task description
- Occasionally uses exclamation for emphasis on a bug: "fix this issue!"
- No emojis, no markdown formatting in his own messages
- English only (100% of sessions); no code-switching observed
