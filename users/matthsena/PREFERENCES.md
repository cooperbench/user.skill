# Preferences — matthsena

## Pushback Distribution

- **non_pushback:** 44.4% — accepts agent output and continues
- **correction:** 40.7% — redirects after (sometimes minimal) acceptance
- **failure_report:** 13.6% — pastes raw error output or screenshot
- **rejection:** 1.2% — outright refusal is rare

Corrections are the dominant pushback mode. He rarely outright rejects; instead he briefly affirms then adds "mas..." (but...) to redirect.

## What Triggers Corrections

- Agent adds itself as git co-author — **hardcoded reflex**, corrects every time
- Agent commits everything in one commit instead of semantic groups
- UI displays unnecessary information (e.g., engine name in session list)
- Wrong directory name (`.data` vs `.reef`, `data` vs `.data`)
- Feature works differently than his mental model of how UX should flow
- Agent claims something is working when he can see it isn't (screenshot evidence)
- Engine/model shows free-text input when a selector would be better
- Cursor doesn't move to expected position after file selection

## What Satisfies Him

- "perfeito funcionou assim perfeitamente" — it works exactly as imagined
- "legal!" / "muito bom!!" — brief positive before next request
- Clean code review results (no Critical/High findings)
- Commits successfully grouped by feature with no co-author line

## Workflow Patterns

**Planning:** Uses pre-authored "Implement the following plan:" dumps as session openers for major features. These plans are detailed Markdown with tables, code snippets, and file-by-file breakdowns — likely written in a separate planning session. Once the plan is dumped, he expects full implementation with no questions.

**Review loop:** After any significant change: "ok now run code reviewer agent again" → agent finds issues → "yes fix them all and commit without coauthor" → "make again code review" → repeat until clean.

**Testing:** Doesn't write tests himself; delegates to the agent with broad instructions ("implement comprehensive E2E and unit tests"). Verifies by running tests and pasting the raw output back.

**Commits:** Semantic grouping is important — "faça o commit de forma semantica, ou seja, ao inves de commitar tudo de uma vez, faça por grupo de funcionalidades". Hates bundled commits.

**Debug style:** Often opens a debug session by pasting a screenshot or raw terminal output and nothing else, expecting the agent to interpret it.

**Interrupting:** Freely interrupts long tool operations. "[Request interrupted by user for tool use]" is not a signal of frustration — just impatience with waiting.

**Naming/branding:** Iterates on product names during development. Changes directory names mid-build when a better idea occurs.

## Stack Preferences

- **Runtime:** Bun (not Node.js) — `bun run`, `bun test`, `bun add`
- **Testing:** `bun:test` (Jest-compatible), tests colocated with source
- **Framework:** React + Ink (terminal UI)
- **Language:** TypeScript
- **AI engines:** Claude Code primary; was exploring Gemini CLI but removed it after persistent bugs
- **Voice:** arecord (Linux) + OpenAI Whisper for transcription
- **Commits:** no co-author, semantic grouping, present-tense imperative messages
