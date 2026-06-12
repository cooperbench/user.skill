# Preferences: heath0xFF

## What satisfies him

- Agent does the full job without asking clarifying questions
- Short confirmations: "yes" / "yep!" signal satisfaction and he moves on immediately
- Agent presents findings as structured numbered/bulleted reports (he reads them carefully)
- Agent challenges its own prior work with paranoid review framing
- Agent gives him a single command to run ("run cargo clippy") and he runs it, then forwards output

## What triggers correction (20% of prompts)

- **Mixed priority rationale**: Challenges when agent bundles unrelated severity items together.
  > "why would you fix those 5 first? seems to be a mix of critical and non critical?"
- **Partial fixes**: Prefers complete fixes over staged rollouts.
  > "why not just fix them all?"
- **Scope creep into unasked editing**: Immediately catches agent editing files when the session was
  discussion-only.
  > "ok now i see you've modified a lot of files -- what you been doing?"
- **Wrong repo target**: Agent applied changes to the wrong repo.
  > "oh in hchat and not the hombrew tap repo. let me fix that"
- **Symbol vs labeled button**: Prefers explicit text labels for UI over icon symbols.
  > "instead of the symbol, just make it a button in the settings menu that says \"reload config\""
- **Agent pauses mid-task for attribution**: Pasted task-notification output back when agent
  reported partial progress and moved on — he keeps it moving himself

## What triggers failure reports / rejection (rare, ~1.3% each)

- **Regression from agent change**: Reports specific bug caused by agent's edits with exact code diffs.
- **Unauthorized file changes**: Hard rejection when agent edits files during a chat-only session.

## Workflow habits

- **No planning phase** for small features. Jumps straight to "let's add X" or "fix the high and
  medium priority issues you outlined."
- **Plans for bigger features**: "i'd like to build a feature that enables the ability to use
  openrouter. let's plan that out" — the plan happens, then he approves, then execution.
- **Review first, then fix**: Launches paranoid review agents, reads findings, then issues fix commands.
- **Git at the end of a work block**: Commits and tags at natural completion points.
  - Asks about tags rather than commanding them: "think we should push a new tag? 0.3.4?"
- **Division of labor**: He does one manual step himself ("i did step 1") and hands the rest off.
- **No tests in practice**: Only 2.7% of prompts are test intent. Runs `cargo clippy` for quality.
- **Agent code percentage**: 92.6% — he writes almost nothing himself; agent handles all code.

## Tool and stack preferences visible in prompts

- **Rust** (only language in the project)
- **egui/eframe** for UI
- **tokio** for async
- **reqwest** for HTTP
- **rusqlite** with bundled SQLite
- **serde + toml** for config
- **OpenAI-compatible APIs**: Ollama (local), OpenRouter, generic endpoints
- **macOS**: All file paths are `/Users/heath/...`; distributes via Homebrew tap
- **GitHub Actions** for CI/CD and Homebrew formula automation
- Prefers OS-level keyring over plaintext credential storage (agrees with agent's security recs)
- Prefers text labels over icons in UI ("reload config" button, not ⟳ symbol)

## Explanation preferences

- Does not ask "why" proactively; reads agent reports on his own
- Asks "walk me through" when he wants a conceptual explanation of something the app does
  > "ok so walk me through how i switch from the default of ollama locally to openrouter"
- Asks "what happens when" for edge case understanding
  > "what happens when someone, in their config, has say the default endpoint but also has one or more [[saved.endpoints]]?"
