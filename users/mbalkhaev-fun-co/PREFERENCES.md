# Preferences: mbalkhaev-fun-co

## What satisfies them
- Agent makes the change and it works. No further discussion needed.
- Agent continues working without being asked (reduces "продолжай" pressure).
- Short, action-confirming responses (not summaries).
- Correct routing architecture without being told how to design it.

## What triggers correction (21% of prompts)
- **Path mismatch**: agent uses full path where relative is expected, or vice versa: "view history передает полный путь, а на странице используется относительный"
- **Wrong architectural choice**: agent routes endpoints incorrectly → "сделай нормальное api путь"
- **Scope mismatch**: agent fixes desktop but user wanted TUI: "исправь все tui ошибки"
- **Incomplete sprint pivot**: after a sprint closes, user opens the next objective immediately without acknowledging the closed one: "А теперь надо значительно улучшить Code..."

## What triggers failure report (23% of prompts)
- Agent declares success → endpoint still returns HTML: "все еще я делаю bun run build && yep gui и получаю <!doctype html>..."
- Paste of raw error with no commentary — the error is the report.
- Repeated failure: sends the same error again, sometimes prepended with "все еще" or "теперь куча" (now a bunch of).

## Workflow habits
- **No planning phase**: jumps straight to the task, no "let's plan first" behavior.
- **No test-driven**: the only test prompt was "тест текущей и проанализуй где еще можем использовать" — exploratory, not TDD.
- **No commit discipline visible**: one git-intent session about a directory confusion; no explicit commit requests observed.
- **Delegates broadly, corrects specifically**: gives high-level goal, lets agent decide implementation, then fires a precise correction if one thing is wrong.
- **Does not ask for explanations**: zero "why does this work?" or "explain this to me" prompts in the training set.
- **Interrupts when wrong**: `[Request interrupted by user]` and `[Request interrupted by user for tool use]` — cuts the agent off, doesn't wait for it to finish.
- **Runs server manually**: uses `bun run build && yep gui` and `yep api` from terminal, then pastes output if broken.
- **Background tasks acknowledged minimally**: task-notification messages are forwarded verbatim ("Read the output file to retrieve the result: /tmp/claude/...") — no added commentary.

## Stack preferences (evidenced)
- Bun (runtime + package manager)
- Turbo (monorepo build)
- Vite + React + TypeScript (desktop GUI)
- TUI package (separate from desktop)
- API server exposed on port 3838
- Prefers `/api/` prefix on all API endpoints
- Uses `yep` CLI commands: `yep gui`, `yep api`
