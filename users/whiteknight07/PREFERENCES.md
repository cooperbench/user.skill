# Preferences — Whiteknight07

## What satisfies him

- Agent that acts immediately without asking clarifying questions
- Parallel subagent execution ("as many sub-agents as you want")
- Complete results ("Everything", "I need it done right now")
- Short, direct status updates when he asks for them
- Agent that uses Opus model for subagents when explicitly asked
- Agent that uses bun instead of npm (corrects this exactly once, expects it to stick)
- Bold, creative redesigns — he gives "all the freedom in the world"
- Confirmations like "yes please" or "yes pls do it" mean he's happy with the plan, proceed immediately

## What triggers corrections (43.9% of pushbacks)

- **Agent asking multiple clarifying questions** instead of acting: he cuts off with a direct command or pastes a bulk answer dump
- **Agent over-explaining** with long "★ Insight" blocks after completing a task: he ignores them and fires the next command
- **Agent defaulting to npm** when the project uses bun
- **Agent failing to find a file that clearly exists**: triggers blunt correction ("what are you smoking")
- **Agent getting too expensive**: triggers pivot to "give me a prompt to paste elsewhere"
- **Agent producing a plan when he wanted immediate action**: he says "Go ahead and do phases 1, 2, and 3... I need it done right now"
- **Agent being verbose when he just wants a status check**: "just give me the status dont do anything"

## What triggers failure reports (14.6% of pushbacks)

- Pastes raw terminal/SSH error output verbatim as the entire response — no description, no commentary
- The terminal prompt (`[stavan@s216 AiTutor]$`) and the error are the full message

## Workflow habits

- **Vague-then-correct**: opens sessions with a broad high-level directive, lets the agent plan/explore, then steers with short corrections
- **No planning phase**: skips alignment; fires the task immediately; corrects in flight
- **Not test-driven**: testing is an afterthought (4.7% intent) — mentioned only when the agent hasn't run tests before committing
- **Commit-happy**: expects agent to commit and push after any significant work; uses "commit and push", "commit and pish" (typo), "stash"
- **Interrupts freely**: cancels agent mid-task with `[Request interrupted by user]` when taking too long
- **Delegates documentation fully**: asks agent to write README, SYSTEM_OVERVIEW, API reference, all docs
- **Pastes professor/external scripts verbatim** and asks agent to adapt them to his project
- **Uses `!` prefix** for bash commands in some agent interfaces
- **Does not ask for explanations**: wants results, not narration — agent's "★ Insight" blocks get ignored

## Stack preferences

- Bun (never npm)
- Claude Opus subagents for large tasks
- Parallel worktrees when feasible
- PM2 for process management
- PostgreSQL (via Docker container on university server)
- React Router, Express, Better Auth, Prisma
- Apache httpd (not nginx) on the UBC server
