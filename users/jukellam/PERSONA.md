---
name: jukellam-persona
description: Background, domain expertise, seniority signals, and attitude toward the agent.
---

# Persona

## Role and seniority (inferred)

Solo side-project developer, likely a software engineer or technical product person by day. (inferred) He is comfortable reasoning about FastAPI dependency injection, SQLite WAL transaction isolation, Pydantic v2, pytest fixtures, and Python async patterns — he can read and evaluate detailed technical findings and recognize when they are correct. But he is not the one writing the architecture docs or code-review findings; he lets the agent do that, then reviews them. He treats the agent as a senior peer engineer who does the actual implementation.

## Domain

Fantasy football. Specifically building `dispersal-draft`, a multi-tenant FastAPI + SQLite webapp for running fantasy auction drafts. The project spans:

- Draft lifecycle management (lobby → active → paused → complete)
- Token-based auth hierarchy (super admin → commissioner → manager)
- Background tasks for auction expiry
- Email delivery via Resend SDK
- Deployment on Render
- Dynasty startup draft type with trading system (direct trades, commissioner trades, secondary sale auctions)

He is deeply familiar with this codebase after many weeks of sessions. He references specific files by exact name (`CLAUDE.md`, `Website Migration.md`, `app/state_db.py`) and PR numbers (`PR #2`, `PR #3`).

## Attitude toward the agent

**Trusting by default, corrective when lost.** He delegates large amounts of work (entire migration phases, full spec implementation) without micromanaging steps. But when the agent misunderstands the goal — building the trading system when he wanted the startup draft UI — he catches it and corrects clearly, if sometimes bluntly. He will paste entire subagent-generated technical findings back as correction messages rather than rephrasing them, trusting that the agent can process the wall of text.

**Tool-aware.** He uses compound-engineering workflow commands fluently and knows that `/workflows:plan` → `/workflows:work` is his standard loop. He notices when a skill is missing ("Unknown skill: workflow:brainstorm"). He interrupts tool calls mid-run when he realizes he needs to pivot.

**Light tester.** He does "light testing to verify the app works" and reports bugs found on Windows. He does not write tests himself; he delegates that to the agent and checks the count.

## Tone

Friendly but businesslike. Uses "Thank you" occasionally. Addresses technical problems directly without hedging. Informal enough to leave typos. Not frustrated or impatient in text, though he does interrupt mid-run.
