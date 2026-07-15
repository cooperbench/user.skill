---
session_id: f114cd15-f7cf-4efd-ac6b-c54c87db98e0
developer: "gh:Poytr1"
split: train
source: entire
repo: sentioxyz/changelogue
start_time: "2026-02-26T02:41:57.563213Z"
n_turns: 25
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

In the release page, we sould be able to see the release notes(if any) and have the link to the provider like dockerhub and github page

> AGENT

I'll start by understanding the current state of the codebase, particularly the release page and related components.

> AGENT

Let me start by exploring the current release page and related components.

> AGENT

Good, I have a clear picture now. Here's what I found: **Current state:** - The `IngestionResult` struct has a `Changelog` field, but it's **never persisted** — the `PgStore.IngestRelease()` only marshals `result.Metadata` (a separate map) into `raw_data`, so GitHub release notes are captured but silently lost. - **No URLs** are captured from either GitHub or Docker Hub during ingestion. - The release detail page shows version, timestamps, provider badge, and raw data — but no release notes section and no link to the provider page. Before I jump into a design, let me ask a clarifying question:

> AGENT

Good. Now the second key question:

> AGENT

Here's the design: ## Design: Release Notes & Provider Links on Release Page ### Backend Changes 1. **Fix `Changelog` persistence** — In `IngestRelease()`, include `result.Changelog` in the `raw_data` JSON (e.g., as a `"changelog"` key) so GitHub release notes are actually stored. 2. **Store `html_url` in raw_data** — While we won't add a column, capture the GitHub release `html_url` from the webhook payload into `raw_data` as well, for reference. ### Frontend Changes 3. **Construct provider URLs client-side** — Use a helper that builds the correct URL from `provider + repository + version`: - GitHub: `https://github.com/{repo}/releases/tag/{version}` - Docker Hub: `https://hub.docker.com/r/{repo}/tags?name={version}` 4. **Display on release detail page**: - Add a "View on {Provider}" external link button in the header area - Add a "Release Notes" card that renders `raw_data.changelog` as markdown (if present), or shows "No release notes available" otherwise 5. **Display on releases list page** — Add an external link icon in each row linking to the provider ### No schema changes needed — we use the existing `raw_data` JSONB column. Does this design look good to move forward with?

> AGENT

Let me read the key files I need to modify, then implement the changes.

> AGENT

Now I have the full picture. Let me create tasks and implement the changes.

> AGENT

### Task 1: Fix changelog persistence The bug is in `IngestRelease` — it only marshals `result.Metadata` but ignores `result.Changelog`. I'll merge the changelog into the raw_data map.

> AGENT

### Task 2: Add provider link and release notes to release detail page

> AGENT

Now add the `getProviderUrl` helper and update the header to include the external link, plus add the release notes card.

> AGENT

Now add the "View on Provider" link in the header area, right after the provider/repository/version chips row.

> AGENT

Now add the Release Notes card between the info grid and the raw data section.

> AGENT

### Task 3: Add provider link to releases list page I'll add an external link icon column to each row in the releases table.

> AGENT

Add the helper function and a header column, plus the link cell in each row.

> AGENT

Now add the column header.

> AGENT

Now add the link cell at the end of each row, before the closing `</tr>`.

> AGENT

Now let me verify the changes compile correctly.

> AGENT

All tests pass. Let me also verify the frontend compiles.

> AGENT

All checks pass — Go tests and TypeScript compilation both succeed. Let me review the final state of the modified files.

> AGENT

Looks like there are changes in `web/app/projects/page.tsx` and `web/lib/api/client.ts` that are unrelated (perhaps from prior work). Let me just confirm my changes look correct on the files I touched.

> AGENT

Everything looks clean. Here's a summary of what was done: ## Changes Summary ### Backend: Fix changelog persistence **`internal/ingestion/pgstore.go`** — The `IngestRelease` function was only marshaling `result.Metadata` (which was usually empty) into `raw_data`. Now it merges both `Metadata` and `Changelog` into the raw_data JSON blob, storing release notes under the `"changelog"` key. ### Frontend: Release detail page **`web/components/releases/release-detail.tsx`**: - Added a **"View on GitHub"** / **"View on Docker Hub"** link in the header area (orange accent, with external link icon) - Added a **Release Notes** card below the info grid that renders `raw_data.changelog` as preformatted text, or shows "No release notes available" if absent - URLs are constructed client-side from provider + repository + version ### Frontend: Releases list page **`web/app/releases/page.tsx`**: - Added an **external link icon** column at the end of each row, linking to the provider page for that release ### What this means: - **New GitHub releases** ingested after this change will have their release notes persisted and visible on the detail page - **All releases** (GitHub and Docker Hub) will have clickable links to their provider pages - Existing releases without changelog data will show "No release notes available"

> DEVELOPER

commit changes and push

> AGENT

There are extra unrelated changes (`web/app/projects/page.tsx`, `web/lib/api/client.ts`, `web/package.json`, `web/package-lock.json`, and an untracked design doc). I'll only commit the files related to this feature.

> AGENT

Committed and pushed — `9c92c61` on `main`. Three files changed: - `internal/ingestion/pgstore.go` — changelog now persisted in raw_data - `web/app/releases/page.tsx` — external link icon column in list - `web/components/releases/release-detail.tsx` — "View on Provider" link + Release Notes card
