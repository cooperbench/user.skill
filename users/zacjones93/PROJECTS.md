# Projects — zacjones93

## wodsmith/thewodapp ★ dominant (100% of sessions)

**What it is**: A Cloudflare-native competition management SaaS for CrossFit and fitness events.
Organizers create competitions, manage athlete registrations, set up scoring events, collect
payments via Stripe Connect, and run video submission reviews. Athletes register, pay, submit
videos, and see their leaderboard standing.

**Tech stack**:
- Frontend + backend: TanStack Start (React, file-based routing)
- ORM: Drizzle ORM
- Database: PlanetScale MySQL (dev branch for schema changes)
- Runtime: Cloudflare Workers + Cloudflare Workflows
- Payments: Stripe Connect (platform fees passed to customers)
- Monorepo tool: pnpm workspaces
- App path: `apps/wodsmith-start/src/`

**Recurring work themes** (from session openers):

1. **Competition scoring and penalties** — Most complex domain work. Implements CrossFit-style
   penalty framework: minor/major penalty types, percentage-based deductions (15–40% for major),
   time vs rep scoring distinctions, video submission review workflow with `verificationStatus`
   and `penaltyType` columns, public leaderboard penalty indicators.

2. **Athlete registration and transfers** — Registration status states (active/removed/pending
   transfer), purchase transfers between athletes, team vs individual registration, division
   selection, removal alerts.

3. **Video submission review UX** — Submission windows, per-movement no-rep logging, review
   status tracking (`reviewed_at`, `reviewed_by`), organizer review queue with progress
   indicators.

4. **Git hygiene** — Very high volume of commit/push/PR commands. Opens PRs, pulls PR comments,
   addresses them, repeats. Uses `gh` CLI.

5. **Stripe/payment debugging** — Fee calculation mismatches between UI and Stripe dashboard,
   webhook processing errors, platform vs processing fee display.

6. **ADR-driven development** — Maintains `docs/adr/` with numerically-prefixed ADRs (0001–0004+)
   that serve as executable specs. ADR-0004 covers the CrossFit penalty framework implementation.

**Key files referenced repeatedly**:
- `apps/wodsmith-start/src/routes/compete/organizer/$competitionId/athletes.tsx`
- `apps/wodsmith-start/src/routes/compete/organizer/$competitionId/events/$eventId/submissions/$submissionId.tsx`
- `apps/wodsmith-start/src/db/schemas/competitions.ts`
- `apps/wodsmith-start/src/server-fns/video-submission-fns.ts`
- `apps/wodsmith-start/src/workflows/stripe-checkout-workflow.ts`
- `apps/wodsmith-start/src/components/competition-leaderboard-table.tsx`

**Skills wired into repo** (`.claude/skills/`):
- `test` — testing router (integration-first)
- `unit-test` — TDD unit test patterns
- `team-memory` — Cloudflare Worker semantic memory store
- `adr-skill` — ADR generation as executable agent specs
- `my-pr-comments` — `gh` CLI PR comment fetching

**Branch naming convention** (inferred): `zacjones93/wod-NNN-slug`
