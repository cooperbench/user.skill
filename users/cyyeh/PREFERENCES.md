---
name: cyyeh-preferences
description: What satisfies cyyeh, what triggers corrections, workflow habits, and stack preferences
---

# Preferences

## Pushback Distribution

- **non_pushback 47.1%** — nearly half of all responses are accepted without correction
- **correction 26.3%** — a specific constraint was missed; one-line fix instruction follows
- **failure_report 18.7%** — fix didn't work; error or screenshot re-pasted or "still the same issue"
- **takeover 6.3%** — user takes over execution directly, usually on git ops
- **rejection 1.7%** — output rejected outright: "I don't want subagent final answer shown in ui at all"

## What Satisfies

- Agent executes the task and commits without being asked
- Design doc is produced before implementation for "big feature alert" / "new feature alert" requests
- Git commands complete cleanly without agent asking for confirmation
- UI matches pixel-level spec (width, height, icon placement)
- Bug fix removes the symptom on first try

## What Triggers Corrections

- Agent misses a specific UI constraint visible in the screenshot (most common)
- Agent works in wrong branch/worktree ("you should not be in main branch, work in litellm-proxy worktree")
- Agent updates files that were not in scope ("only update bifrost/config.example.json, bifrost/README.md and backend/.env.example")
- Agent repeats data from a subagent verbatim instead of synthesizing ("After sql-analyst returns, do NOT repeat the data tables or numbers")
- Readme or docs not updated when they should have been ("I don't see readme updated")
- Agent modifies `.env` instead of `.env.example`

## What Triggers Failure Reports

- Fix applied but bug reproduces: "still the same issue", "still breaks:", "built docker, but found the same issue"
- Error message appears that wasn't there before
- UI element still wrong after fix: "but I found this when I build a docker-compose service in another linux machine"
- Pasting full stack trace or backend log when error surfaces again

## What Triggers Takeover

- Git operation stalls or agent hesitates to merge: user issues one combined command ("create new branch and commit and push and merge")
- Used when git output is unclear or agent creates wrong branch structure

## What Triggers Rejection

- Agent adds something the user explicitly didn't want
- Agent updates files that were out of scope

## Workflow Habits

- **Design-first for large features**: Always requests design doc before implementation. Never asks agent to implement without a plan in hand.
- **Plan paste then execute**: After design/plan is written (sometimes by the agent, sometimes externally), pastes the full "Implement the following plan:" block to kick off implementation.
- **Frequent, small commits**: Commits after each meaningful change. Doesn't batch unrelated changes.
- **Branch-per-feature**: Creates a new branch for each feature or fix. Uses worktrees.
- **No TDD**: test intent is only 1% of prompts; testing is not a default workflow step.
- **README/docs update as an afterthought**: Asks for readme/docs updates mid-session or as a final step, not upfront.
- **Interrupts freely**: "[Request interrupted by user]" appears multiple times — stops the agent if output is going the wrong direction.
- **Systematic-debugging as escalation**: When repeated fix attempts fail (~3+ failures), pastes the systematic-debugging skill doc as a hard reset to process.

## Stack and Tool Preferences

- **LLM**: Uses Claude (anthropic/sonnet by default), experiments with OpenAI-compatible models via bifrost
- **Backend**: Python / FastAPI / uvicorn / DuckDB / Claude Agent SDK
- **Frontend**: React / TypeScript / Vite
- **Infra**: Docker / docker-compose / Render for deployment
- **Observability**: Langfuse
- **LLM Gateway**: Bifrost
- **Skills system**: Uses superpowers-marketplace skills (systematic-debugging, writing-plans, brainstorming, finishing-a-development-branch, subagent-driven-development)
- **Chart libraries**: Plotly (default), vega-lite (alternative), Recharts (used in duckdb-web)
- **i18n**: English + Traditional Chinese (zh-TW)
- **No preference for verbose logging**: explicitly removed logging.basicConfig and prefers `print()` statements
