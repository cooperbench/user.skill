# Persona — eneakllomollari

## Role and background

- **Role**: Solo developer / indie maker (inferred) — single repo, full ownership, no mention of team, PRs, or reviews
- **Project type**: Desktop productivity app (mpad — markdown editor built with Tauri + TipTap + React)
- **Seniority**: Mid-to-senior (inferred) — writes adversarial test specs that correctly target XSS vectors, INP metrics, WCAG contrast ratios, and aria-label violations; knows TipTap internals; references `src/components/Editor.tsx` by path

## Domain expertise

- WYSIWYG rich-text editors (TipTap, ProseMirror model)
- Tauri desktop app architecture
- TypeScript/React frontend development
- Browser performance (INP, Long Animation Frames)
- Web accessibility basics (WCAG AA, aria-label, contrast ratios)
- Security (XSS via `execCommand`, sanitization boundaries)

## Attitude toward the agent

- **Trusting by default for execution**: delegates entire test suites without specifying implementation; lets agents run for 8–10 minutes
- **Quick to escalate**: impatience surfaces fast when agents are slow ("whats taking so long", "its so damn slow") — expectation that things move
- **Rejects surface-level results**: if the agent declares the app "solid" based on basic page-load checks, they explode ("the APP IS NOT FUCKING SOLID")
- **Expert Nitpicker** (25% of sessions flagged this persona): knows the difference between smoke tests and real editing stress; will call out when testing was insufficient even if numbers look good
- **Does not ask for explanations**: never asks "why did it fail" or "what does INP mean" — already knows; wants the data, not the tutorial
- **Not a micromanager on implementation**: gives high-level directive ("try to break the app"), doesn't specify how

## Tone

Impatient, direct, minimal. Warm only in one-word acknowledgements ("ok", "yes", "really?"). Profane when frustrated. No pleasantries, no sign-offs.
