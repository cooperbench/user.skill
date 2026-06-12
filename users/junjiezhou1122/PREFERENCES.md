# Preferences: junjiezhou1122

## Pushback distribution

- **Correction 46.5%**: Most common — agent went in the wrong direction, not just failed
- **Failure report 25.6%**: Pastes raw error output or screenshot, signals "this broke"
- **Non-pushback 27.9%**: Accepts output and moves on or gives next command

## What triggers corrections

- Agent builds something he didn't ask for (e.g., adds a Chairman chat input when he only wanted read-only monitoring)
- Agent explains a concept he already understands instead of acting
- Agent proposes architecture he disagrees with without being asked for opinions
- Agent implements in a way that violates the conceptual model (e.g., linear instead of hierarchical, missing the "company org chart" metaphor)
- Agent uses wrong tooling (SDK when he wants Claude Code, opencode when things are broken)
- Agent misses an explicit constraint from an earlier message

## What satisfies

- Terse confirmations that the agent understood and did it: agent reports minimal summary + system state
- Working output that matches his mental model ("成功了 但...")
- Agent that asks zero clarifying questions and just makes decisions
- Spec-driven commits: plan → commit-per-feature rhythm

## Workflow habits

- **Spec-first**: writes or asks for a full plan doc before implementation ("先不改代码", "只plan不写代码")
- **Spec-driven development**: references `.specify/specs/` directory, uses numbered specs (001, 002, 003)
- **Brainstorm-first when unsure**: "我们先brainstorming一下设计一下" before committing to direction
- **Interrupts freely**: does not wait for agent to complete if it's heading wrong
- **Does not do code review**: delegates all implementation; cares about behavior not line-by-line code
- **Screenshots as bug reports**: attaches `[Image: image/png]` alongside or instead of text description
- **Commit cadence**: asks to commit after each working milestone ("commit一下", "你先规划一下 然后每实现一个commit一下！")
- **No test mentions**: zero references to tests, CI, or test-driven development in this dataset
- **Does not ask for explanations of implementation**: asks "why" only for architectural decisions ("为啥mcp server就可以通信呀")

## Tech stack preferences (visible in prompts)

- **Backend**: Bun + Hono (chosen after rejecting Next.js, debated Go/Rust)
- **Frontend**: React + Vite + Tailwind
- **AI**: Claude Code (`claude --dangerously-skip-permissions`), Claude API via `@anthropic-ai/sdk`
- **Protocol**: MCP for agent tool injection, WebSocket for real-time log streaming
- **Version control**: Git, commits via agent command
- **Prefers**: TypeScript over Go/Rust for AI tooling because "claude code or other tools they all use typescript!"
- **Rejects**: SDK-driven agent control (wants subprocess-based Claude Code), interactive TUIs for autonomous agents (rejected opencode because it asks questions)
