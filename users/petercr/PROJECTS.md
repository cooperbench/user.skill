# Projects — petercr

## petercr/ccw ★ (dominant — 100% of sessions)

**What petercr does here:** Builds and iterates the frontend of a web application. Sessions span UI polish (responsive layouts, favicon, theming), creative feature work (WebGL water shader), bug fixing (browser caching, CSP errors, mobile layout), and git housekeeping (branch management, PRs).

**Tech stack (inferred from prompts):**
- Framework: TanStack Start (SSR/SSG React meta-framework)
- Routing: TanStack Router
- Language: TypeScript / TSX
- Styling: Vanilla Extract (CSS-in-TS; component style names like `headerPill`, `formCard`, `shaderContainer`, `homeContainer`)
- CMS: Sanity (referenced for OG image URL)
- Shader: `@paper-design/shaders-react` (Water shader, WebGL)
- Tooling: Vite (dev server on port 3000), Vitest
- Design: Penpot (accessed via MCP)
- Browser testing: Chrome MCP

**Monorepo structure (inferred):**
- `apps/frontend/` — main frontend app
  - `src/components/` — React components (Header, WaterShader, GlobalLayout, FavIcons)
  - `src/pages/` — page components (Home)
  - `src/lib/` — utilities (seo.ts, meta.ts)
  - `public/` — static assets (favicon files, SVGs)
- `apps/frontend/src/routes/` — TanStack Router route files

**Recurring themes across sessions:**
- **Favicon and cache busting:** renaming files with version suffixes, handling Chrome's favicon cache, dark-mode favicon swap
- **Responsive layout polish:** max-width breakpoints (desktop, 4K), margin/padding tweaks, mobile-specific fixes (`dvh`)
- **Theming (light/dark):** propagated via `data-theme` on `<html>`, toggled via `matchMedia`, applied to shader colors and favicons
- **Accessibility:** `prefers-reduced-motion` for the shader, semantic considerations
- **WebGL water shader integration:** z-index layering, lazy loading, performance, reduced-motion gate
- **Git workflow:** every session ends with a commit to a feature branch and a PR to main
- **MCP tooling:** Penpot for design specs, Chrome for visual verification

**Issue references:**
- Issue #27: Water shader feature (referenced in opening prompt and ultraplan)
- Issue #41: PR for favicon/theming work (referenced in pushback examples)
