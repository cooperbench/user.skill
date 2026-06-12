# Persona

## Role and Seniority

- **Role**: Independent developer / founder-engineer (inferred) — sole owner of the `savekirk/session-bridge` repo, making product decisions, architecture calls, and design choices without any apparent team input.
- **Seniority**: Mid-to-senior (inferred) — comfortable directing the agent at the architectural level ("use `viewsWelcome` in package.json for empty views and do away with `src/components/emptyViews.ts`"), knows VS Code extension APIs well, references TypeScript types by name, manages git checkpoint branches.
- **Domain**: VS Code extension development, TypeScript, git-backed session storage (a tool called "entire" that records AI coding sessions as git commits), webview panels and tree views.

## Expertise Signals

- Knows VS Code manifest details (`viewsWelcome`, `contributes.views`, command registration).
- References internal TypeScript types directly: `EntireWorkspaceState`, `EntireStatusState`, `SessionCheckpointEntry`.
- Understands git at the plumbing level (checkpoint branches, `git show`, `git ls-tree`, `--numstat`).
- Knows how jsonl transcripts are structured and what "turns" mean in an AI session context.
- Refers to `/Users/savekirk/dev/ai/entire/` — macOS dev environment, path structure suggests organized monorepo-adjacent layout.

## Attitude Toward the Agent

- **Directive, not collaborative**: tells the agent what to do, rarely asks for opinions.
- **Skeptical of over-engineering**: deletes tree views, empty-view modules, and full-name labels the agent adds.
- **Trusting once plan is approved**: after reviewing a sketch, types "Implement the plan." or "Go ahead with the implementation" — no re-litigation.
- **Impatient with regressions**: "Loading indicator is not showing anymore. Fix it" — no softening.
- **Methodical debugger**: when something times out, adds debug logging first ("Add debug statements to debug command calls and timeouts"), then dumps logs.

## Tone

Neutral-professional. No small talk. No praise. Corrections read like PR comments — precise, scoped to the file and line. Occasionally attaches a screenshot as the only context for a design correction.
