---
name: preferences
description: gregszero's workflow habits, what satisfies vs. triggers corrections, pushback patterns, and stack preferences
metadata:
  type: user
---

# Preferences

## Pushback distribution

| Type | Rate | What it means |
|------|------|---------------|
| non_pushback | 48.3% | Accepts, usually follows with "commit this" or a next request |
| failure_report | 21.2% | Pastes the raw error; no explanation added |
| correction | 18.5% | Short redirect when agent goes wrong direction |
| takeover | 11.9% | Overrides with a direct command ("commit this") when agent talks too much |

## What satisfies him

- Agent executes the spec exactly as written without asking clarifying questions
- Clean commit with no extra commentary
- Visual result matches what he sketched or screenshotted
- Agent figures out the root cause from a raw stack trace without being told where to look
- Token-efficient solutions — he values avoiding unnecessary LLM overhead

## What triggers corrections

- Agent explains alternatives when the user already decided ("lets create a web_fetch tool just in case..." → agent argues run_code is sufficient → correction)
- Agent refuses to do something the framework already supports (the "remind me" incident: agent said it couldn't schedule — user corrected with evidence the tool exists)
- Wrong visual placement, wrong color, wrong sizing of UI elements
- Summary-heavy responses when the user expected a commit prompt
- Missing the simplest fix and doing something complex instead

## Workflow habits

- **Plan first offline, execute via Claude Code**: Writes full architectural Markdown specs offline, pastes as opening prompt. Does not use Claude Code for planning — only for execution.
- **No test-driven**: Tests appear occasionally (1.8% intent share) and are requested explicitly ("any test to add?") rather than being the default workflow.
- **Commits after each milestone**: Git commands are 18.3% of intents — frequent, short, confirmatory.
- **Interrupts freely**: Kills tool calls mid-run when they go in the wrong direction (11 observed interrupts).
- **Iterates visually on UI**: Posts screenshots to report visual bugs; does not describe pixel values — uses qualitative language ("too bright", "a lil bit to the top").
- **Asks short diagnostic questions after failures**: "why the agent wasnt able to create?", "why stoped?", "should we upgrade the threads etc?"
- **Does not ask for explanations by default**: Wants results. Occasionally asks "what can you do?" or "should we update the docs?" as exploratory, not as a blocker.

## Stack preferences visible in prompts

- Ruby / ActiveRecord / Roda / Puma
- Stimulus JS, Turbo Streams (Hotwire stack)
- Tailwind CSS (CDN in dev), custom CSS design tokens
- SQLite (via ActiveRecord migrations)
- FastMcp gem for MCP tools
- rufus-scheduler + fugit for cron
- Xvfb / xdotool / scrot for headless computer use
- Prefers "lego block" architecture: widgets, tools, skills as self-contained files auto-discovered by the framework
- Dislikes bloat: wants modular prompts, tool groups, context compression — token efficiency matters

## Things he explicitly rejects

- Agent suggesting external workarounds for things the framework should handle natively
- Notifications page (replaced with dropdown)
- Over-verbose agent summaries after completing work
- Separate "pages" for things that should be canvas widgets
- Agent writing code that doesn't auto-discover (prefers convention over configuration)
