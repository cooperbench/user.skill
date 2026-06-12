---
name: Pavel401 — Preferences
---

# Preferences

## Pushback distribution

| Type | Rate | What it means |
|---|---|---|
| Non-pushback | 41.3% | Accepts output and moves on — short confirmations or new sub-tasks |
| Correction | 39.4% | Output was wrong or incomplete; he redirects with specifics |
| Failure report | 17.4% | Something broke at runtime; he pastes logs or symptom |
| Takeover | 0.9% | He takes over the action himself (e.g., authorized a force-push) |
| Rejection | 0.9% | Hard no — the agent did something unacceptable |

## What triggers corrections

- Agent produces output without first planning when he asked to plan first.
- Agent reads more files or uses more tokens than needed after context is already loaded.
- Agent explains what it did at the end instead of just doing it.
- Agent implements something that partially misses the spec (e.g., delete dialog not appearing, wrong field null).
- Agent makes a false positive claim (hallucinated issues in code review output).
- Agent implements something in the wrong place (e.g., context building in the wrong service layer).
- Agent produces overly broad output when he wanted targeted changes.

## What triggers failure reports

- Raw paste of application logs, stdout, or JSON with no wrapper or preamble.
- Symptom statement: "delete repo is not working", "look at the api.log it has so many issues", "it's not popping up when the delete icon is clicked on".
- Stats that look wrong: pastes the bad output inline ("99 files\n624 functions\n67 classes\n780,431,213 lines — the lines are wrong").
- Curl commands with full headers pasted verbatim.

## What satisfies him

- Short, direct answers that match his spec exactly.
- Agent proactively warns about cost or risk before executing.
- Agent reads only what it needs, not the whole codebase.
- Clean, minimal UX — "Make the flow minimal and clean UX".
- Agent writes plan.md / updates CLAUDE.md without being asked twice.
- Agent compares approaches or benchmarks against competitors when he explicitly asks.

## Workflow habits

- **Plan first**: says "first plan it" before any substantial implementation. Will interrupt if the agent starts executing without a plan.
- **Interrupt-heavy**: monitors tool calls live and kills them with `[Request interrupted by user for tool use]` when they over-run.
- **Token-budget aware**: explicitly tracks token usage in the conversation, tells the agent to stop reading when context is full.
- **Update CLAUDE.md**: expects the agent to maintain a running CLAUDE.md with architecture context; corrects if it falls behind.
- **Paste-and-fix**: after encountering CodeRabbit output, pastes the CodeRabbit findings verbatim and asks the agent to implement the fixes.
- **Debug by log paste**: does not narrate errors — pastes the raw log and expects the agent to diagnose.
- **No summaries needed**: does not ask "what did you do?" — he reads the diff himself.
- **Stack**: Python/FastAPI + Neo4j + Firebase/Firestore + TypeScript/Next.js + pydantic-ai + tree-sitter. Does not introduce new frameworks without discussion.
- **Cost sensitivity**: explicitly objects when the agent uses expensive orchestration patterns unnecessarily ("just burned so much money for no reason").
- **Commits / git**: low frequency in sessions (~2.5% git intent). Does not drive commit workflow himself — delegates to agent. Was surprised when agent force-pushed / rewrote git history.
- **Test coverage**: almost absent from sessions (0.8% test intent). Does not write or request tests in observed sessions.
