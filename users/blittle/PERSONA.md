# PERSONA

## Background (inferred)

blittle is a self-directed developer building pressy as a personal/side project — a framework for publishing books as PWAs with chapter-by-chapter navigation, offline support, and a paywall system. The project is ambitious in scope (Vite plugin, Cloudflare Workers middleware, Stripe integration, service workers, Preact components) and he is building it mostly solo with Claude Code as his primary pair programmer.

## Domain expertise

- **Frontend frameworks**: fluent in Preact/React (signals, hooks, JSX), Vite plugins, TypeScript, CSS (column layout, scroll, animations, CSS custom properties)
- **PWA / browser APIs**: service workers, IndexedDB, localStorage, sessionStorage, beforeinstallprompt, Fullscreen API, viewport units (dvh)
- **Build tooling**: pnpm workspaces/monorepos, tsup, Rollup, GitHub Actions, pnpm filters
- **Backend/infra**: Cloudflare Pages Functions (Workers), Stripe Checkout and webhooks, GitHub Pages deployments
- **Git**: comfortable branching, rebasing, PR creation — uses Claude to execute git operations

## Role (inferred)

Solo indie developer / founder-mode. Makes all architectural decisions. Treats Claude Code as an executor, not an architect — he writes the plans, Claude implements them.

## Seniority signals

- Writes detailed, technically correct implementation plans with file paths, line numbers, and code snippets before asking Claude to implement
- Immediately spots when Claude's fix is wrong at the architectural level ("Do we need to take a step back and reconsider how we are doing this?")
- Asks "is that the right way to do it?" when something smells off — not because he doesn't know, but because he's checking
- References specific browser quirks (Samsung Galaxy touch behavior, `dvh` vs `vh`, MIME type enforcement for ES modules)
- Knows enough Stripe to ask whether `success_url` is a query param vs config

## Attitude toward the agent

- **Trusting by default**: lets Claude execute long plans without micromanaging each step
- **Switches to skeptical** when things break repeatedly or when the agent summarizes success that doesn't match observed behavior
- **Corrects without ceremony**: doesn't soften redirects — "Get rid of the scroll implementation", "no ugh, you got rid of the stripe and paypal packages"
- **Interrupts freely**: if a tool call looks wrong mid-flight, he cuts it
- **Delegates git operations entirely**: he types "commit this" and expects Claude to handle branch, message, and push

## Tone

Conversational, direct, lowercase in casual messages. Formal only in plan documents he writes himself. No pleasantries. Occasional mild frustration markers: "ugh", ":(", "Still broken". Uses rhetorical questions to signal doubt without demanding an explanation ("is that the right way to do it?").
