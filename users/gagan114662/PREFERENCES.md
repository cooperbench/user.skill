---
slug: gagan114662
type: preferences
---

# Preferences

## What triggers corrections (17.4% of prompts)

- **Wrong provider assumption**: agent defaults to Gemini when user wants Claude Code + Codex.
  Correction: `even telegram isnt starting and this was supposed to work with claude code and
  codex not gemini`
- **API key vs auth token confusion**: agent says "API key", user corrects to auth token
  immediately. `with auth token not api key`
- **Over-explaining authentication**: agent lists all auth options; user just says what they want.
  `i wanna autheticate with codex cli`
- **False positive "it's working"**: agent claims a service is live; user proves otherwise by
  pasting a failed task notification or hitting the URL directly.

## What triggers failure reports (21.7% of prompts)

- Pasting a `<task-notification>` with `status: failed` — no added commentary.
- Pasting the URL with "this is not working" or "is down".
- Pasting a follow-up task notification (even on success) to make agent read the actual output.

## What satisfies (60.9% non-pushback)

- Agent follows the constraint exactly (right provider, right auth method).
- Background tasks complete successfully (user reads the output via task notification).
- One-word or format-exact agent replies to probes ("yes" is sufficient confirmation).
- The daemon URL is actually accessible and shows the right services.

## Workflow habits

- **Not planning-first**: jumps straight into running things; discovers issues by hitting URLs
  or watching background task status.
- **Not test-driven**: no mention of test suites; validates by live integration (run it and
  check the dashboard).
- **Plugin/skill-configured**: has a structured session wrap-up skill (/wrap-up) and a
  systematic debugging skill; invokes them by pasting the full skill text when needed.
- **Short feedback loop**: sessions median 2 turns, 12 seconds — fires a command, checks output,
  corrects or moves on. No extended dialog.
- **Background-task pattern**: issues build commands as background tasks, then pastes the
  notification to read results rather than waiting inline.
- **Interrupts when agent is too slow or wrong direction**: does not let agents finish rambling
  responses; just interrupts and redirects.

## Stack preferences visible in prompts

- **Primary LLMs**: Claude Code (Anthropic) + Codex (OpenAI) — NOT Gemini
- **Auth style**: OAuth auth tokens, not API keys, for Anthropic
- **Telegram**: Teloxide/Telegram bot integration via bot token
- **Build toolchain**: Cargo (Rust), release builds (`--release`)
- **Local dev**: `http://127.0.0.1:50051/` as the dashboard/API endpoint
- **Dashboard**: web UI for managing agents and providers
