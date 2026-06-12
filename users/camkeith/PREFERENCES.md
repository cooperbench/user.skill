# PREFERENCES — camkeith

## Pushback distribution

| Type | Rate |
|------|------|
| Correction | 48.8% |
| Non-pushback (acceptance) | 32.3% |
| Failure report | 15.7% |
| Takeover | 2.4% |
| Rejection | 0.8% |

He corrects almost half of all agent outputs. This is structural — he's a vague requester who fills in precision *after* seeing the result.

## What triggers correction

- **Wrong metric / stat:** "shows the number of commits instead of the number of contributions frmo github"
- **Visual alignment off:** Sends a screenshot. No further words needed.
- **Behavior not matching the spec:** If a fix doesn't work after agent claims it does, he repeats the failure flatly: "it still doesn't change the speed"
- **Agent over-explains or adds unsolicited content:** Ignores the explanation, issues the next command
- **Agent uses wrong approach:** Redirects with the correct one: "no i think you just remove the padding above it"

## What triggers failure reports

- Fix applied but bug still visible in browser ("I still see the white boxes")
- Deployed app behaves differently from localhost
- Agent output doesn't appear on screen after claimed change ("Yes, it is running, but I still don't see the changes on the home page cam code")

## What satisfies him

- "good it works." — minimal, positive, moves on immediately
- "all of them sound good." — approves a list without reading deeply
- "go ahead" — delegated, no further input
- "continue" — restarting after interruption

## Workflow habits

- **No planning phase.** Opens with a task, no design doc, no discussion. Exception: uses the brainstorming plugin occasionally for design questions.
- **Screenshot-first iteration.** Visual changes are reviewed via screenshot; text descriptions are rare.
- **Frequent interruptions.** Uses `[Request interrupted by user]` when agent takes too long. Follows up with "continue" if he wants it to resume.
- **Git at end of session.** Commits are batched: "commit by feature and push to main" or "commit and push everything" — always at session end, never mid-task.
- **No test-driven development observed.** No mention of tests, test suites, or CI in any prompt.
- **Asks for explanation only when blocked:** "is this token read only?", "what is this one?" — only when he genuinely doesn't know what to do next.
- **Pastes what the agent needs raw:** Error logs, build configs, LinkedIn blobs — no curation, no commentary.

## Stack / tool preferences visible in prompts

- **Next.js** (App Router, `npm run dev`, `.next/`)
- **AWS App Runner + CloudFront + ACM** for deployment
- **GitHub GraphQL API** for contribution data
- **Grok / xAI** (`XAI_API_KEY`) as the chatbot backend
- **LangGraph / LangChain** for AI agents
- **Tailwind CSS** (references `w-72`, `w-96`, `gap-2.5`, `lg:`)
- **Claude Code** exclusively (100% of sessions)

## What he does NOT want

- Long explanations after completing a task
- Agent adding features he didn't ask for
- Agent asking clarifying questions when the screenshot answers them
- Verbose commit messages (just "commit and push" is sufficient)
- Agent diverging from his spec — especially on UI layout
