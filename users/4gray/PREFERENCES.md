---
name: PREFERENCES
---

# Preferences: 4gray

## What triggers corrections (pushback_distribution: correction 45.9%)

- Agent reports "verified and working" but the visual change is not visible in the screenshot.
- CSS overrides that don't penetrate Angular Material's MDC internals (common source of multi-turn correction loops).
- Layout elements that regress after a different fix (e.g. hover effect disappears after color token change).
- Wrong position or scope for a UI element (e.g. clear button in global header instead of view header — "that violates the mental model").
- Element size inconsistency: too big, too much padding, wrong density compared to the rest of the app.
- Hardcoded colors instead of theme tokens — especially when light/dark theme switching breaks.

## What triggers failure reports (pushback_distribution: failure_report 13%)

- Agent says something is done, user checks the running app, it is still broken.
- Stack traces / console errors pasted verbatim with "here are the logs:" or "can you check why i get that error:".
- Visual regression introduced by a fix (e.g. element invisible in DOM but not on screen).

## What satisfies

- Terse approval follows when the visual matches expectation: "good", "nice", "perfect", "i like your recommendation, do it".
- "i like your recommendation" + "do it" = agent suggestion was validated and user wants immediate implementation.
- A brainstorm result ending in "like that idea" or "do it for primary option" means the user has decided.

## Workflow habits

- **Plan first**: Opens complex or multi-file tasks with "/plan mode" or "create a plan first". Does not want the agent to start coding before alignment.
- **Brainstorm before deciding**: Uses `sc-brainstorm` skill to explore design options; then picks one and says "do it" or "implement primary option".
- **Test by running app**: Does not read diffs. Judges output by screenshots from the running Electron app or Chrome devtools via `agent-browser`.
- **Screenshot as pushback**: Sends an image with zero commentary — the image itself is the correction message.
- **Multi-point sessions**: A session often has 2–5 distinct sub-issues tackled in sequence, sometimes mid-session pivots.
- **Skill as constraint**: Invoking a skill (`frontend-design`, `sc-brainstorm`, `electron`) is a hard constraint, not a suggestion — the agent must actually use it.
- **No stashing**: Explicitly stops the agent from git-stashing: "do not stash, just lint".
- **Commits by request**: Only asks for a commit explicitly — "Please commit all of my changes so we can make a PR."
- **Documentation**: Asks for README updates and docs when new tools/servers are added.

## Stack and tool preferences

- Angular Material components with custom CSS tokens, not alternatives.
- Nx monorepo workspace conventions — `@libs/...` path aliases.
- Electron + `agent-browser` CLI for live app inspection and screenshots.
- Custom Claude Code skills: `frontend-design`, `sc-brainstorm`, `electron`, `userinterface-wiki`, `stalker-portal`.
- TypeScript file size limit: 300 lines ideal, 350–400 maximum (has added this to CLAUDE.md).
- Prefers segmented toggle buttons over tabs for mode switching.
- Prefers inline search bars that match the app's existing search style over new UI patterns.

## What they explicitly reject

- Generic "AI-generated" UI aesthetics — wants unique, opinionated design inspired by apps like Gitbutler, Raycast, macOS Spotlight.
- Hardcoded color values — wants CSS custom properties / design tokens.
- Overly large Angular Material elements (too much density) — always asks to reduce density.
- Agent marking something complete when it visually isn't — will call it out bluntly.
