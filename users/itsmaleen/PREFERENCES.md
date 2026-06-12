# Preferences

## Pushback distribution

- **Non-pushback (acceptance)**: 40.4% — agent output accepted without correction
- **Correction**: 38.5% — redirects the agent to a different or more specific approach
- **Failure report**: 21.2% — pastes new error output showing the fix didn't work

## What triggers corrections

- Agent edits the wrong component or file ("no this was incorrect, I wanted the change to be in ChatInput")
- Agent uses a nonsensical icon or name ("instead of a lobster icon, use something that makes more sense")
- Agent's explanation doesn't address the actual error ("how does that relate to this error?")
- Agent over-engineers or adds unnecessary features ("why do we need an export functions?")
- Agent commits or works outside the expected scope ("you don't need to go outside of this foler")
- Agent's fix works in tests but fails in CI — triggers failure report + log paste

## What satisfies them

- Correct behavior in CI/GitHub Actions (the only real acceptance test for signing workflows)
- Agent following conventional commit format ("proper message (following standard)") without prompting for the format itself
- Phase 1 tests pass → immediate "yes continue with phase 2"
- Accurate plan that can be reviewed in a markdown file

## Workflow habits

- **No planning on simple tasks**: Dives straight in for small UI/layout changes.
- **Planning on complex multi-step work**: Explicitly requests a plan file ("start planning", "let me review the plan for") before implementing multi-phase features like console-line persistence.
- **Phase-gated implementation**: Explicitly steps through phases, testing each before approving the next.
- **Investigate-before-edit**: On regression bugs, often instructs "Don't make any edits but investigate what happened."
- **Push-to-test**: Frequently pushes after CI fixes specifically to test the GitHub Actions run ("yes and push the changes so I can test").
- **No explanations needed on happy path**: Accepts results without asking the agent to explain what it did.
- **Asks clarifying questions on agent proposals**: Picks apart numbered lists to reject or question individual items.

## Stack / tooling preferences

- **Bun** runtime (references `bun run sign:mac`)
- **electron-builder** for packaging macOS apps
- **GitHub Actions** for CI
- **SQLite** + FTS5 for persistence
- **@tanstack/react-virtual** for virtualization (explicitly mentioned and approved)
- **Conventional commits** format (expects it by default)
- Prefers external references over invented solutions ("look into how this project does it")
