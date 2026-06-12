# Persona: nodo

## Background (inferred)

- **Role**: Founding engineer or senior IC at a small startup (`entireio`) building developer tooling (inferred)
- **Seniority**: High — demonstrates deep Go knowledge (interface composition, generics, `exec.CommandContext`, `golangci-lint` directives, cobra command trees), reviews PRs autonomously, writes precise protocol specifications, and catches subtle bugs like context deadline propagation and shell injection in test helpers
- **Domain expertise**: CLI tooling in Go, AI agent integration, git hook systems, plugin/extensibility protocols, subprocess management
- **Company context**: Building `entireio` — a product that integrates multiple AI coding agents (Claude Code, Cursor, Gemini CLI, OpenCode, Factory AI Droid) through a unified CLI (inferred from repo structure)

## Attitude toward the agent

- **Trusting but verifying**: delegates large implementation tasks without hand-holding, but consistently cross-checks output against code review findings from a separate review agent
- **Correction-heavy**: 30.2% of mid-session prompts are corrections; rarely praises — a non-pushback is often just silence or "yes" / "continue"
- **Does not re-explain**: when correcting, gives the precise review comment or the exact diff fragment, trusts the agent to understand the rest
- **Workflow-delegating, not step-by-step-supervising**: feeds full spec plans ("Implement the following plan: # Plan: ...") then mostly interrupts to steer or fix specific issues

## Tone

- Matter-of-fact, no pleasantries beyond an occasional "please"
- No praise, no encouragement, no "great job"
- Gets more detailed in corrections when the agent misses the point the first time
- Uses rhetorical "What do you think about this comment..." to get the agent to engage with a review finding before assigning the fix
