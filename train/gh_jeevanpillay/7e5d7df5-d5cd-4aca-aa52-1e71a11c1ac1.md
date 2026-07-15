> DEVELOPER

/create_plan @thoughts/shared/research/2026-04-14-marketing-integrations-page.md

> TOOL

<command-message>create_plan</command-message>
<command-name>/create_plan</command-name>
<command-args>@thoughts/shared/research/2026-04-14-marketing-integrations-page.md</command-args>

> AGENT

Good — I have enough context. The sitemap actually lives in `apps/www/src/app/sitemap.ts` (research doc assumed wrong ownership — that's a useful correction).

Here's my proposed plan structure before I write the detailed version. Please review:

## Overview
Build a marketing `/integrations` index and `/integrations/<id>` detail pages on `apps/www`, modelled on Linear, reusing the fumadocs-mdx content pipeline. Ship GitHub detail first; Vercel/Linear as follow-on MDX. Add top-level `Integrations` nav.

## Proposed Phases

**Phase 1 — Content pipeline foundation**
Schema (`IntegrationPageSchema`), collection registration, fumadocs loader + `getIntegrationPage/Pages`, url-type, `ProviderId` import from `@repo/app-providers` client bundle.

**Phase 2 — SEO infrastructure**
`buildIntegrationJsonLd` builder (using `WebPage` + `SoftwareApplication` cross-reference — resolving the open question), `emitIntegrationSeo` in seo-bundle, canonical URL regex.

**Phase 3 — MDX components**
`IntegrationHero`, `IntegrationFeatureGrid`, `IntegrationScreenshot` wired into `mdx-components.tsx`. Helper `getProviderIcon(providerId)` that resolves icons from `IntegrationLogoIcons` (14 providers) with `PROVIDER_DISPLAY` fallback.

**Phase 4 — Index page**
`/integrations/page.tsx` with `force-static`, FAQ block, JSON-LD, grid of 3 cards (GitHub, Vercel, Linear) — coming-soon badges sourced from `PROVIDER_DISPLAY.comingSoon` or MDX `status` override. PostHog click event with `providerId`.

**Phase 5 — Detail page + GitHub content**
`[slug]/page.tsx`, `opengraph-image.tsx`, `loading.tsx`/`not-found.tsx`, MDX at `apps/www/src/content/integrations/github.mdx`, CTA PostHog event. No prev/next nav (integrations aren't chronological).

**Phase 6 — Wiring**
Top-level `Integrations` in `INTERNAL_NAV`, sitemap entries in `apps/www/src/app/sitemap.ts`.

## Resolutions for research "Open Questions"

1. **JSON-LD entity type** → `WebPage` as primary entity with a nested `SoftwareApplication` reference for the integration (provider app), plus `FAQPage` and `BreadcrumbList`. Reasoning: integrations are marketing pages describing a capability, not products themselves; Lightfast is the primary `Organization`, provider is the integrated app.
2. **Sitemap** → Direct update to `apps/www/src/app/sitemap.ts` (correcting the research doc's assumption that it was in `apps/app`).
3. **Fumadocs search** → Defer. Not wired for blog/changelog either; not a regression.
4. **Featured image pipeline** → v1 uses existing `/images/github-banner.png` and `/images/vercel-integration-placeholder.png`; Linear gets placeholder referencing provider icon. Production pipeline is a follow-up.
5. **MDX component shapes** → Locked in Phase 3; prop surface driven by GitHub's needs.

## What We're NOT Doing
- RSS/Atom feeds
- Prev/next navigation
- Auto-generating pages from `PROVIDERS` registry
- Per-integration waitlist forms (reuse generic `WaitlistCTA`)
- Vercel/Linear/Sentry/Apollo detail MDX (follow-up PRs)
- Fumadocs search indexing
- Remotion featured-image templates

Does this phasing work? Specifically confirm:
- **(a)** JSON-LD choice: `WebPage` + nested `SoftwareApplication` — or do you want me to research this further before locking?
- **(b)** Nav: top-level `INTERNAL_NAV` entry (as research decided), keeping Pricing/Early Access/Docs/Integrations ordering?
- **(c)** Index initial cards: GitHub, Vercel, Linear only — or include Sentry/Apollo from `PROVIDERS` registry as coming-soon cards?
- **(d)** OK to update `apps/www/src/app/sitemap.ts` (the www app owns it, not apps/app as the research doc stated)?

> DEVELOPER

makes perfect sense. this is great start!

> AGENT

Plan written to `thoughts/shared/plans/2026-04-14-marketing-integrations-page.md`.

Six phases, each with separated automated and manual success criteria. Key decisions locked in the plan:

- **Schema**: `IntegrationPageSchema` extends `BasePageSchema` (not `ContentPageSchema`) — `providerId` optional, `tagline`, `category`, `status` override, optional `faq`, `updatedAt` only.
- **JSON-LD**: `WebPage` as primary + nested `SoftwareApplication` (`@id: #integrated-app`) when `providerId` is present, plus `FAQPage` and `BreadcrumbList`.
- **Nav placement**: `Integrations` between `Pricing` and `Early Access` in `INTERNAL_NAV` (top-level, not Resources dropdown).
- **Sitemap**: direct edit to `apps/www/src/app/sitemap.ts` (not `apps/app` as research doc stated).
- **Initial content**: GitHub full MDX + Vercel/Linear lean stub MDX for 3 index cards.
- **Analytics**: PostHog event with `providerId` from day 1, with fallback if PostHog not yet wired in `apps/www`.

Flagged assumptions in the plan that need a quick verify-in-code during Phase 1 rather than blocking the plan:
- `@repo/app-providers/client` export path exposes `providerSlugSchema` and `PROVIDER_DISPLAY`.
- `SoftwareApplication` type is exported from `@vendor/seo/json-ld` (fallback: structural shape).
- PostHog provider is mounted in `apps/www` (fallback: land analytics in a follow-up).

Review and let me know what to adjust — phase boundaries, success criteria specificity, or any scope that's wrong.
