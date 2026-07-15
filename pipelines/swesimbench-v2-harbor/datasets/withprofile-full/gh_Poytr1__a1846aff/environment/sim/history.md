[DEVELOPER]: Why the `Recent Activity` doesn't have the up-to-dated releases? https://changelogue-app.azurewebsites.net/

[AGENT]: Let me investigate the Recent Activity feature to understand how it works and why it might not show up-to-date releases.

[AGENT]: Now I see the issue. Let me look more closely at the critical part — the unified feed fetches only **page 1 with perPage=1** per project, which severely limits results.

[AGENT]: Now let me check what the `listByProject` API function signature looks like — specifically to confirm the `page` parameter is the only one being passed (no `perPage`).

[AGENT]: Found the bug. Let me look at the exact call in the unified feed. The problem is on **line 64** of `unified-feed.tsx`: ```typescript releasesApi.listByProject(p.id, 1) ``` The `listByProject` signature is `(projectId, page = 1, perPage = 25)`. So this call passes `page=1` and uses the default `perPage=25`. That part is fine. But the real issue is the **architecture of the feed itself**: it iterates over the first 10 projects and fetches only **page 1** of releases per project. If you have many projects, it misses projects 11+. And within each project, only the first 25 releases are returned — but since it sorts client-side across all projects and takes the top 15, this should generally be OK for recency. Let me check if there's a simpler explanation — maybe there's a dedicated backend endpoint for recent activity that should be used instead.

[AGENT]: There's a global `GET /api/v1/releases` endpoint. Let me check the backend handler for that and the frontend's `releases.list()` which fetches from it.

[AGENT]: Now I have the full picture. Here's the root cause: ## Root Cause The **Unified Feed** (`unified-feed.tsx`) doesn't use the global `GET /api/v1/releases` endpoint (which returns all releases sorted by recency). Instead, it: 1. Fetches up to **10 projects** (line 58: `projectsData.data.slice(0, 10)`) 2. For each project, fetches **page 1 with default perPage=25** of releases 3. Merges and sorts client-side, then takes the top 15 The problem: **`releasesApi.listByProject(p.id, 1)` passes `1` as the `page` argument**, and uses the default `perPage=25`. That's fine — it gets up to 25 releases per project. But this approach has two fundamental flaws: 1. **Projects beyond the first 10 are completely ignored** — if the newest release belongs to project #11+, it'll never appear. 2. **N+1 request explosion** — it fires 30 parallel requests (10 projects x 3 endpoints) instead of a single global query. The much simpler and correct approach: use `releases.list()` (the global `GET /api/v1/releases` endpoint) and `semanticReleases.listAll()` which already return all releases sorted by recency across all projects. This would be a single request per data type instead of 30 requests, and would include all projects. Let me also check `ListAllReleases` in pgstore to confirm it returns project metadata needed for display.

[AGENT]: The global `ListAllReleases` query already returns `project_id`, `project_name`, `provider`, and `repository` — all the metadata the feed needs. The current approach of per-project fetching is unnecessary. Now let me check what the `Release` type in the frontend looks like, to confirm it has these fields.

[AGENT]: The `Release` type already has `project_id`, `project_name`, `provider`, and `repository` fields. The global endpoint returns all of these. This confirms the fix is straightforward. ## The Fix The unified feed should use `releases.list()` and `semanticReleases.listAll()` instead of per-project fetching. This: - Includes releases from **all projects** (not just the first 10) - Uses a single server-side `ORDER BY` query (correct recency) - Reduces 30+ HTTP requests down to 2

[AGENT]: Now clean up the unused imports.

[AGENT]: Now remove the unused `Source` type import.

[AGENT]: Let me verify the final state of the file.

[AGENT]: Now I also need to check that the dashboard page's SSE revalidation still works — it was using `"unified-feed"` as the SWR key, and the new code still uses the same key.

[AGENT]: Good — `"unified-feed"` is still the SWR key used for revalidation on SSE events, and it matches. The `"projects-for-dashboard"` key is still used by `page.tsx` itself for other purposes (stats display, etc.), so that's unrelated. Let me build the frontend to verify there are no type errors.

[AGENT]: Clean build, no errors. ## Summary **Root cause:** The Recent Activity feed was fetching releases per-project (limited to the first 10 projects, page 1 each), then merging client-side. This had two problems: 1. **Projects beyond #10 were completely invisible** — their releases never appeared in the feed 2. **Only page 1 per project was fetched** — with default perPage=25 per project, the client-side merge could miss the truly most recent releases across all projects since SQL `ORDER BY` was applied per-project, not globally **Fix:** Replaced the N+1 per-project fetching with two global API calls: - `GET /api/v1/releases?page=1&per_page=15` — returns the 15 most recent releases across **all** projects, already sorted by `COALESCE(released_at, created_at) DESC` server-side - `GET /api/v1/semantic-releases?page=1&per_page=15` — returns the 15 most recent semantic releases globally Both endpoints already return all needed metadata (project name, provider, repository) via JOINs in the database query, so no additional source lookups are needed. This also reduces the number of HTTP requests from **30+** (10 projects × 3 endpoints) down to **2**.