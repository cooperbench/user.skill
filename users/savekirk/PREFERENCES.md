# Preferences

## Pushback Distribution

| Type           | Rate  |
|----------------|-------|
| correction     | 41%   |
| non_pushback   | 41%   |
| failure_report | 16.4% |
| rejection      | 1.6%  |

Corrections and acceptance are equally common. Failure reports are frequent (regressions introduced by agent changes). Outright rejection is rare but decisive — when it happens, the user pastes a full code-review audit with P1/P2 findings and a hard redirect.

## What Triggers Corrections

- **Wrong UI structure**: agent uses inline placeholders instead of VS Code's `viewsWelcome` mechanism, adds a full-word label where an icon belongs, puts an avatar on tool calls, writes "Agent" instead of the real agent name.
- **Over-building**: agent creates a dedicated tree view or module for something that already exists as a vscode command; user says "get rid of it."
- **Wrong data semantics**: agent uses the current git user's name instead of the one from the commit, or timestamps the wrong field.
- **Regression after a change**: loading indicator disappears, sessions don't reload on checkpoint select — user reports the symptom minimally and says "Fix it."
- **Cosmetic misalignment**: text not aligned with avatar, header taking too much vertical space, timestamp format too verbose.

## What Satisfies Them

- When the agent's plan matches the direction: they say "Implement the plan." or "Go ahead with the implementation" — no feedback, just proceed.
- When a commit just happens cleanly: they say "Commit the changes" again in the next session — implicit success.
- Acceptance without comment is common (41% non_pushback) — they move on to the next task.

## Workflow Habits

- **Plan before complex UI work**: asks for a "ui sketch" before implementation; reviews it silently; issues "Implement the plan."
- **No test-driven development observed**: no prompts requesting tests; testing mentioned only in pushback about stale `out/` artifacts.
- **Commit cadence**: explicit "Commit the changes" prompts — not automatic. Typically comes after a few refactor/debug rounds.
- **Debug protocol**: symptom reported → ask agent to add debug logging → paste full log output → wait for diagnosis.
- **No explanation requests**: rarely asks "why" or "how does this work" — "Are remote checkpoints supported" and one codebase exploration prompt are the only `understand` intents (4.9%).
- **Results only**: does not ask for explanations of what was changed. Moves to next task after success.
- **Multi-agent**: uses Codex (58%), OpenCode (27%), Gemini CLI (15%) — switches agents across sessions, same repo.

## Stack and Tool Preferences

- **VS Code extension APIs**: `viewsWelcome`, `contributes.views`, tree view providers, webview panels.
- **TypeScript**: all code is TypeScript; references types by name in prompts.
- **git as storage**: checkpoint data lives in git branches; git commands (`git show`, `git ls-tree`) are first-class debugging tools.
- **Package.json as config surface**: prefers declaring behavior in `package.json` manifests rather than imperative TypeScript code.
- **No mocks implied**: debugging goes straight to real log output, not test stubs.
