# Persona — petercr

## Background and role

petercr (inferred) is a frontend developer working on a personal or small-team web project (`petercr/ccw`). The project uses TanStack Start/Router, React, TypeScript, Vanilla Extract for CSS-in-JS, and Sanity CMS for content — a moderately advanced stack suggesting several years of frontend experience. They are the sole or primary developer; all sessions are in the same repo with no sign of team coordination overhead.

## Domains of expertise

- React component architecture (theming, `useEffect` consolidation, lazy loading)
- CSS/layout (responsive breakpoints, `dvh` vs `vh`, z-index layering)
- Browser APIs and web platform specifics (favicon caching, CSP, `prefers-reduced-motion`, `matchMedia`)
- Git workflow (branches, stash, PRs, force-push instinct for cache busting)
- Web performance basics (Lighthouse, lazy loading, deferred rendering after first paint)
- Web accessibility awareness (reduced-motion, dark mode theming)
- Design tooling (Penpot MCP for design reference)
- MCP tooling (Chrome MCP for visual browser verification, Penpot MCP for design specs)

## Seniority signals

Intermediate-to-senior (inferred). Can interpret raw stack traces and browser console errors, understands CSP directives, knows the difference between `vh` and `dvh`, asks about whether 3 `useEffect`s are needed (suggesting awareness of hook design), and recognises z-index layering problems immediately. However, they delegate heavily and accept Claude's implementation without reviewing code — suggesting they are comfortable with the domain but prefer to stay at the steering level.

## Attitude toward the agent

**Mostly trusting, steers at a high level, corrects specifics.** The annotated persona distribution (71% Vague Requester, 14% Expert Nitpicker) is accurate: petercr gives broad directives and lets Claude figure out the details, but fires off quick corrections when the agent misses scope or acts on the wrong element. They are not micromanaging — they rarely specify file paths in advance — but they notice visual mismatches immediately and correct with a single line. When a debugging rabbit hole grows too wide, they cut it hard and roll back.

## Tone

- Casual, friendly, collaborative
- Never hostile; frustration shows through "umm" or "ok enough of this" rather than criticism
- Affirms good work quickly: "great", "good job", "yes it works now. good job."
- Does not write long explanations; expects Claude to understand from minimal context
