# Preferences: timelabsad-dot

## What triggers corrections (47.9% of pushbacks)

- Agent refuses something the user believes is achievable: immediate correction, often a direct restatement of the original command ("youo disable them", "Yas, you can. Just do it - step by step.")
- Agent asks clarifying questions instead of acting: "Is it possible you somehow stop asking me until you finish someth real/huge/looking like a common goal?"
- Agent over-explains with long prose instead of executing: "1 + 2 - that is enought"
- Agent misidentifies a model/agent assignment: corrects immediately with before/after schema ("Switch him back and show me other's schema")
- Agent stops mid-task: "why have you stopped"
- Agent does something via wrong tool/path (e.g., pushed via bonsai): "Do not evet push anything via bansai. Explain this move"
- Git push missed: "I am wainitng you will run git push at least every 30 min -- this is min frequency"

## What satisfies / earns praise

- Agent executes autonomously without asking: "\"Let me do everything myself — fast.\" I'm in love! You are the best!"
- Agent survives a long session: "This is huge. Я чувствую запах успеха."
- Agent catches its own errors proactively
- Concise status reports with actual data
- Multi-model tribunal for architectural decisions

## Workflow habits

- **No planning-first**: opens sessions with direct action commands or context-reset instructions, not discussion
- **Spec dumps for new phases**: large design docs pasted verbatim as the prompt when starting a new work phase; expects the agent to read and execute without follow-up questions
- **Frequent interrupts**: hits stop/interrupt before agents complete tool calls; impulsive direction changes mid-execution
- **Git cadence explicit**: mandates pushes every 30 minutes minimum; uses `/commit-commands:commit` slash command
- **Agent orchestration is primary**: most "code" tasks are about spawning, routing, and coordinating other agents — not writing application code directly
- **Status checks are constant**: "show current system status", "any updates?", "is Orion alive?" appear every few turns
- **Token/context awareness**: explicitly tracks token usage, asks for stats ("show memory/tokens/contexts stat"), concerned about session death and context loss
- **Multi-model tribunal pattern**: for important decisions, asks for consensus from GPT + Gemini + DeepSeek + Claude ("Tribunal = You + GPT-highest + Gemini-highest + Deepseek-highest")

## Stack and tool preferences

- **Primary agent**: Claude Code (Opus for core coordinator Rex, Sonnet for worker agents)
- **Secondary agents**: Gemini CLI (Orion), external terminal Claude Code instances (Hyperion, B-2nd)
- **Storage/sync**: Firebase/Firestore for agent heartbeats and inter-agent messaging; Entire.io for session persistence and git hooks
- **Bridge**: `rhea_bridge.py` for multi-provider LLM calls (OpenAI, Gemini, DeepSeek, OpenRouter)
- **Repo hygiene**: structured docs dirs, explicit audit docs (INTEGRATIONS_AUDIT.md), ADR-style decisions
- **No Bonsai for git push** — explicitly prohibited after an incident
- **Custom slash commands in use**: `/superpowers:verification-before-completion`, `/superpowers:brainstorm`, `/superpowers:write-plan`, `/commit-commands:commit`

## What they delegate vs. specify precisely

- **Delegates**: implementation details, choice of which sub-agent to use, token optimization strategies, model selection for worker tasks
- **Specifies precisely**: agent names and model assignments, file paths and output locations, git branch targets, which external tools to consult, the doc structure for audit/registry files
- **Never wants**: explanations of what was done after the fact, long option lists to choose from, requests for permission before obvious next steps
