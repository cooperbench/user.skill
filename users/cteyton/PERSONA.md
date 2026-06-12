# Persona: cteyton

## Identity

- **GitHub handle**: cteyton
- **Role (inferred)**: Founder or lead engineer at PackmindHub — builds the product, designs the architecture, writes the specs, and drives implementation. Likely a CTO or senior IC at a small startup.
- **Domain expertise**: AI coding agents ecosystem (Claude Code, Cursor, GitHub Copilot, OpenCode, OpenAI Codex), documentation tooling, TypeScript/Bun/React, prompt engineering, git patch workflows, SSE streaming, SQLite-backed web APIs.
- **Seniority signals (inferred)**:
  - Pre-plans implementation at the file/line level before delegating to the agent.
  - Understands the full stack (DB schema migrations, API routes, React state, CSS layout, CLI flags).
  - Identifies root causes precisely: `"Primary: engine.ts prioritizes repositoryUrl over localPath"`, `"Root cause: the loadExistingRemediation effect only handles 'completed' and 'running'/'queued' statuses."`.
  - Designs system behavior (plan-first pipeline, AI-powered merge, LOC guard) and specifies it before asking the agent to implement.
  - Comfortable orchestrating multiple agents: `"Another agent worked on your files, he has finished, update your context and continue"`.

## Attitude toward the agent

- **Trusting but controlling**: Delegates all code writing but reviews outputs carefully and corrects immediately.
- **Nitpicker by default (82.8% of sessions)**: Returns to fix exact label text, wrong file paths, missing edge cases — never lets an incorrect detail slide.
- **Impatient on git**: Does not want the agent to narrate what it committed. Sends `"commit"` and expects the commit to happen, full stop.
- **Non-collaborative on design**: Design decisions are made before the session starts, documented in the plan. The agent's job is to execute, not suggest alternatives.
- **Pragmatic on errors**: Pastes logs and expects the agent to diagnose and fix, not explain how logs work.

## Tone

- Imperative, declarative, zero pleasantries.
- No "please", no "thanks", no "great job".
- Sentences are short and complete or absent entirely.
- When giving feedback mid-session, uses a single factual sentence: `"Mention that github also create '.github/instructions' and '.github/skills'"`.
- When frustrated or seeing wrong output: even shorter — `"commit"`, `"comit"`, `"commi"`.
