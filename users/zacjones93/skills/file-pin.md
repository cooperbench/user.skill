---
name: file-pin
description: How Zac pins exact files and exclusions — uses @path for monorepo-relative references, references line numbers, and repeatedly excludes db/index.ts from commits.
---

Zac navigates by file path, not by description. He references exact files with `@` prefix
and sometimes includes line numbers. He also has a persistent exclusion: `db/index.ts` is
never to be committed unless explicitly requested.

**Trigger**: Any message containing `@apps/...`, a line number, or "ignore the db/index.ts" /
"leave db/index.ts alone".

## Examples

**@path reference with domain correction:**
> "@apps/wodsmith-start/src/routes/compete/organizer/$competitionId/events/$eventId/submissions/$submissionId.tsx the corrected score is showing up as a number -48450 206550... for time scored events we need to ADD time. for reps we need to subtract reps."

**Line number pinning:**
> "In `@apps/wodsmith-start/src/db/schemas/competitions.ts` around lines 169 - 173, The unique constraint on (eventId, userId, divisionId) prevents re-registration..."

**File exclusion in commit:**
> "commit your work, ignore the db/index.ts"
> "commit your changes, leave db/index.ts alone"
> "commit code you changed" (implicitly excludes db/index.ts based on prior instructions)

**Route-relative URL for debugging:**
> "this url just looks like the workout edit page on a competition... http://localhost:REDACTED"
> "http://localhost:REDACTED this review page doesn't actually exist."

## Behavior notes

- `db/index.ts` has persistent uncommitted changes (likely environment-specific config) — treat it as always-excluded from staging
- The `@` prefix is a monorepo shorthand pointing to `apps/wodsmith-start/src/...`
- When Zac gives a localhost URL, he wants the agent to look at the route file for that path, not literally fetch the URL
- Line numbers from Zac's messages may be slightly off; treat them as approximate anchors
