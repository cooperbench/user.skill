> DEVELOPER

Why the `Recent Activity` doesn't have the up-to-dated releases? https://changelogue-app.azurewebsites.net/

> AGENT

Let me investigate the Recent Activity feature to understand how it works and why it might not show up-to-date releases.

> TOOL

tool_use Task
id: toolu_01BrQDt2sbAr9NgBHBYWDtcu
```json
{
  "subagent_type": "Explore",
  "prompt": "Explore the codebase to understand how \"Recent Activity\" works on the dashboard/home page. Look for:\n\n1. The frontend component that renders \"Recent Activity\" - search in web/ directory\n2. The API endpoint that feeds recent activity data\n3. The backend handler/query that fetches recent activity\n4. How releases are stored and queried for recency\n\nSearch for terms like \"recent activity\", \"RecentActivity\", \"recent_activity\", \"activity\" in both frontend and backend code. Also look at the main dashboard page component.\n\nBe very thorough - check the API routes, database queries, and frontend data fetching.",
  "description": "Explore Recent Activity feature"
}
```

> TOOL

tool_use WebFetch
id: toolu_01MaX4LizYqmrbC6uLMF4Gzz
```json
{
  "url": "https://changelogue-app.azurewebsites.net/",
  "prompt": "What does the Recent Activity section show? List any releases shown, their dates, and any other relevant information about what's displayed on the dashboard."
}
```

> TOOL

tool_result
id: toolu_01MaX4LizYqmrbC6uLMF4Gzz
```
Based on the provided web page content, there is **no Recent Activity section visible** in the data. The content consists entirely of:

- Next.js framework boilerplate (React Server Components serialization format)
- Theme/dark mode initialization script
- Layout and routing configuration
- Metadata: the page title is **"Changelogue"** with a description of **"Agent-driven release intelligence platform"**
- Standard 404 error page template
- Font and stylesheet references

The scraped content does not include any rendered dashboard data, releases, dates, or activity information. This appears to be just the initial HTML shell/framework payload of the page, before any dynamic content (such as releases or activity feeds) would be loaded client-side via JavaScript. The actual dashboard content would require JavaScript execution to render.
```

> TOOL

tool_result
id: toolu_01BrQDt2sbAr9NgBHBYWDtcu
```
Perfect! Now I have a complete understanding. Let me create the comprehensive report.

## Report: "Recent Activity" Implementation in ReleaseBeacon Dashboard

---

### **Overview**

The "Recent Activity" feature on the dashboard is called the **Unified Feed** and displays the 15 most recent releases (both raw source releases and AI-analyzed semantic releases) across tracked projects. Data flows are driven by both **periodic polling** (every 30 seconds) and **real-time events** (Server-Sent Events via PostgreSQL notifications).

---

### **1. Frontend Components**

#### **1.1 Main Dashboard Page**
**File:** `/home/<USER>/web3/ReleaseBeacon/web/app/page.tsx`

- Entry point for the dashboard
- Renders the `<UnifiedFeed />` component alongside stats and charts
- Establishes SSE connection to `/api/v1/events` to listen for real-time updates
- On any SSE event, it revalidates SWR cache keys including `"unified-feed"` to trigger a refresh

```typescript
// Lines 26-55: SSE listener setup
useEffect(() => {
  let es: EventSource | null = null;
  function connect() {
    es = new EventSource(`${SSE_BASE}/events`);
    es.onmessage = () => {
      // Revalidate dashboard SWR keys on any event
      mutate((key) => typeof key === "string" && (
        key === "stats" ||
        key.startsWith("trend-") ||
        key === "unified-feed"
      ), undefined, { revalidate: true });
    };
  }
  connect();
}, []);
```

#### **1.2 […]

> AGENT

Now I see the issue. Let me look more closely at the critical part — the unified feed fetches only **page 1 with perPage=1** per project, which severely limits results.

> TOOL

tool_use Read
id: toolu_018mLJEWHpcFju4AXnMbKhCs
```json
{
  "file_path": "/home/<USER>/web3/ReleaseBeacon/web/components/dashboard/unified-feed.tsx"
}
```

> TOOL

tool_result
id: toolu_018mLJEWHpcFju4AXnMbKhCs
```
     1→// web/components/dashboard/unified-feed.tsx
     2→"use client";
     3→
     4→import useSWR from "swr";
     5→import Link from "next/link";
     6→import {
     7→  projects as projectsApi,
     8→  releases as releasesApi,
     9→  sources as sourcesApi,
    10→  semanticReleases as srApi,
    11→} from "@/lib/api/client";
    12→import { VersionChip } from "@/components/ui/version-chip";
    13→import { getProviderIcon } from "@/components/ui/provider-badge";
    14→import { Sparkles } from "lucide-react";
    15→import type { Release, SemanticRelease, Source } from "@/lib/api/types";
    16→import { timeAgo } from "@/lib/format";
    17→import { useTranslation } from "@/lib/i18n/context";
    18→
    19→type FeedItemType =
    20→  | { kind: "release"; data: Release; repository?: string; provider?: string; projectName?: string }
    21→  | { kind: "semantic"; data: SemanticRelease; projectName?: string };
    22→
    23→function getTimestamp(item: FeedItemType): number {
    24→  if (item.kind === "release") {
    25→    return new Date(item.data.released_at ?? item.data.created_at).getTime();
    26→  }
    27→  return new Date(item.data.created_at).getTime();
    28→}
    29→
    30→function getTimeStr(item: FeedItemType): string {
    31→  if (item.kind === "release") {
    32→    return item.data.released_at ?? item.data.created_at;
    33→  }
    34→  return item.data.created_at;
    35→}
    36→
    37→function ProviderIcon({ provider }: { provider: string }) {
    38→  const icon = getProviderIcon(provider);
    39→  if (!icon) return <div className="h-3.5 w-3.5 shrink-0" />;
    40→  return icon({ size: 14, className: "shrink-0 text-text-muted" });
    41→}
    42→
    43→export function UnifiedFeed() {
    44→  const { t } = useTranslation();
    45→ […]

> AGENT

Now let me check what the `listByProject` API function signature looks like — specifically to confirm the `page` parameter is the only one being passed (no `perPage`).

> TOOL

tool_use Read
id: toolu_01Gwq9AEH7dmmEWEhYirKvWk
```json
{
  "file_path": "/home/<USER>/web3/ReleaseBeacon/web/lib/api/client.ts"
}
```

> TOOL

tool_result
id: toolu_01Gwq9AEH7dmmEWEhYirKvWk
```
     1→// web/lib/api/client.ts
     2→import type {
     3→  ApiResponse,
     4→  Project,
     5→  ProjectInput,
     6→  Release,
     7→  Source,
     8→  SourceInput,
     9→  Subscription,
    10→  SubscriptionInput,
    11→  BatchSubscriptionInput,
    12→  BatchDeleteSubscriptionInput,
    13→  NotificationChannel,
    14→  ChannelInput,
    15→  ContextSource,
    16→  ContextSourceInput,
    17→  SemanticRelease,
    18→  AgentRun,
    19→  HealthStatus,
    20→  Stats,
    21→  TrendData,
    22→  DiscoverItem,
    23→  Todo,
    24→  OnboardScan,
    25→  OnboardSelection,
    26→  OnboardApplyResult,
    27→  SuggestionItem,
    28→  RepoItem,
    29→  ReleaseGate,
    30→  ReleaseGateInput,
    31→  VersionReadiness,
    32→  GateEvent,
    33→} from "./types";
    34→
    35→const BASE = process.env.NEXT_PUBLIC_API_URL || "/api/v1";
    36→
    37→async function request<T>(path: string, init?: RequestInit): Promise<T> {
    38→  const res = await fetch(`${BASE}${path}`, {
    39→    headers: { "Content-Type": "application/json", ...init?.headers },
    40→    ...init,
    41→  });
    42→  if (!res.ok) {
    43→    const body = await res.json().catch(() => null);
    44→    throw new Error(body?.error?.message ?? `Request failed: ${res.status}`);
    45→  }
    46→  if (res.status === 204) return null as T;
    47→  return res.json();
    48→}
    49→
    50→// --- Projects ---
    51→
    52→export const projects = {
    53→  list: (page = 1, perPage = 25) =>
    54→    request<ApiResponse<Project[]>>(`/projects?page=${page}&per_page=${perPage}`),
    55→  get: (id: string) =>
    56→    request<ApiResponse<Project>>(`/projects/${id}`),
    57→  create: (input: ProjectInput) =>
    58→    request<ApiResponse<Project>>("/projects", {
    59→      method: "POST",
    60→      body: JSON.stringify(input),
    61→    }),
    62→  update: (id: string, input: ProjectInput) =>
    63→    request<ApiResponse<Project>>(`/projects/${id}`, {
    64→      method: "PUT",
    65→ […]

> AGENT

Found the bug. Let me look at the exact call in the unified feed.

The problem is on **line 64** of `unified-feed.tsx`:

```typescript
releasesApi.listByProject(p.id, 1)
```

The `listByProject` signature is `(projectId, page = 1, perPage = 25)`. So this call passes `page=1` and uses the default `perPage=25`. That part is fine.

But the real issue is the **architecture of the feed itself**: it iterates over the first 10 projects and fetches only **page 1** of releases per project. If you have many projects, it misses projects 11+. And within each project, only the first 25 releases are returned — but since it sorts client-side across all projects and takes the top 15, this should generally be OK for recency.

Let me check if there's a simpler explanation — maybe there's a dedicated backend endpoint for recent activity that should be used instead.

> TOOL

tool_use Grep
id: toolu_01MzNu1FNMy9kb2VcPq81u9o
```json
{
  "pattern": "recent|feed|activity|latest",
  "path": "/home/<USER>/web3/ReleaseBeacon/internal/api",
  "-i": true,
  "output_mode": "content",
  "glob": "*.go"
}
```

> TOOL

tool_use Grep
id: toolu_01C92SaNuCtiegJRzmPDMgiF
```json
{
  "pattern": "releases\\?|/releases",
  "path": "/home/<USER>/web3/ReleaseBeacon/internal/api/server.go",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01C92SaNuCtiegJRzmPDMgiF
```
75:	mux.Handle("GET /api/v1/releases", chain(http.HandlerFunc(releases.List)))
76:	mux.Handle("GET /api/v1/sources/{id}/releases", chain(http.HandlerFunc(releases.ListBySource)))
77:	mux.Handle("GET /api/v1/projects/{projectId}/releases", chain(http.HandlerFunc(releases.ListByProject)))
78:	mux.Handle("GET /api/v1/releases/{id}", chain(http.HandlerFunc(releases.Get)))
```

> TOOL

tool_result
id: toolu_01MzNu1FNMy9kb2VcPq81u9o
```
internal/api/discover.go:88:	// Approximate GitHub Trending: search for repos with recent star activity.
internal/api/pgstore.go:1013:// GetPreviousRelease returns the most recent release for a source that is not
internal/api/pgstore.go:1314:		// Aggregated: keep only the latest todo per grouping key.
```

> AGENT

There's a global `GET /api/v1/releases` endpoint. Let me check the backend handler for that and the frontend's `releases.list()` which fetches from it.

> TOOL

tool_use Read
id: toolu_01CYM3cnBHhjmYUKabmmEqDy
```json
{
  "file_path": "/home/<USER>/web3/ReleaseBeacon/internal/api/releases.go"
}
```

> TOOL

tool_result
id: toolu_01CYM3cnBHhjmYUKabmmEqDy
```
     1→package api
     2→
     3→import (
     4→	"context"
     5→	"net/http"
     6→
     7→	"github.com/sentioxyz/changelogue/internal/models"
     8→)
     9→
    10→// ReleasesStore defines the persistence operations for releases (read-only).
    11→type ReleasesStore interface {
    12→	ListAllReleases(ctx context.Context, page, perPage int, includeExcluded bool) ([]models.Release, int, error)
    13→	ListReleasesBySource(ctx context.Context, sourceID string, page, perPage int, includeExcluded bool) ([]models.Release, int, error)
    14→	ListReleasesByProject(ctx context.Context, projectID string, page, perPage int, includeExcluded bool) ([]models.Release, int, error)
    15→	GetRelease(ctx context.Context, id string) (*models.Release, error)
    16→}
    17→
    18→// ReleasesHandler implements HTTP handlers for the /releases resource.
    19→type ReleasesHandler struct {
    20→	store ReleasesStore
    21→}
    22→
    23→// NewReleasesHandler returns a new ReleasesHandler.
    24→func NewReleasesHandler(store ReleasesStore) *ReleasesHandler {
    25→	return &ReleasesHandler{store: store}
    26→}
    27→
    28→// List handles GET /releases — returns all releases across all projects.
    29→func (h *ReleasesHandler) List(w http.ResponseWriter, r *http.Request) {
    30→	page, perPage := ParsePagination(r)
    31→	includeExcluded := r.URL.Query().Get("include_excluded") == "true"
    32→	releases, total, err := h.store.ListAllReleases(r.Context(), page, perPage, includeExcluded)
    33→	if err != nil {
    34→		RespondError(w, r, http.StatusInternalServerError, "internal_error", "Failed to list releases")
    35→		return
    36→	}
    37→	if releases == nil {
    38→		releases = []models.Release{}
    39→	}
    40→	RespondList(w, r, http.StatusOK, releases, page, perPage, total)
    41→}
    42→
    43→// ListBySource handles GET /sources/{id}/releases — returns […]

> AGENT

Now I have the full picture. Here's the root cause:

## Root Cause

The **Unified Feed** (`unified-feed.tsx`) doesn't use the global `GET /api/v1/releases` endpoint (which returns all releases sorted by recency). Instead, it:

1. Fetches up to **10 projects** (line 58: `projectsData.data.slice(0, 10)`)
2. For each project, fetches **page 1 with default perPage=25** of releases
3. Merges and sorts client-side, then takes the top 15

The problem: **`releasesApi.listByProject(p.id, 1)` passes `1` as the `page` argument**, and uses the default `perPage=25`. That's fine — it gets up to 25 releases per project. But this approach has two fundamental flaws:

1. **Projects beyond the first 10 are completely ignored** — if the newest release belongs to project #11+, it'll never appear.
2. **N+1 request explosion** — it fires 30 parallel requests (10 projects x 3 endpoints) instead of a single global query.

The much simpler and correct approach: use `releases.list()` (the global `GET /api/v1/releases` endpoint) and `semanticReleases.listAll()` which already return all releases sorted by recency across all projects. This would be a single request per data type instead of 30 requests, and would include all projects.

Let me also check `ListAllReleases` in pgstore to confirm it returns project metadata needed for display.

> TOOL

tool_use Grep
id: toolu_018Jy6GeyerzfP5V33FyYwuD
```json
{
  "output_mode": "content",
  "path": "/home/<USER>/web3/ReleaseBeacon/internal/api/pgstore.go",
  "pattern": "func.*ListAllReleases",
  "-A": 80
}
```

> TOOL

tool_result
id: toolu_018Jy6GeyerzfP5V33FyYwuD
```
237:func (s *PgStore) ListAllReleases(ctx context.Context, page, perPage int, includeExcluded bool) ([]models.Release, int, error) {
238-	var total int
239-	if includeExcluded {
240-		err := s.pool.QueryRow(ctx,
241-			`SELECT COUNT(*) FROM releases r
242-			 LEFT JOIN sources s ON r.source_id = s.id`).Scan(&total)
243-		if err != nil {
244-			return nil, 0, fmt.Errorf("count releases: %w", err)
245-		}
246-	} else {
247-		err := s.pool.QueryRow(ctx,
248-			`SELECT COUNT(*) FROM releases r
249-			 LEFT JOIN sources s ON r.source_id = s.id
250-			 WHERE (s.version_filter_include IS NULL OR r.version ~ s.version_filter_include)
251-			   AND (s.version_filter_exclude IS NULL OR r.version !~ s.version_filter_exclude)
252-			   AND (s.exclude_prereleases = false OR r.raw_data->>'prerelease' IS NULL OR r.raw_data->>'prerelease' != 'true')`).Scan(&total)
253-		if err != nil {
254-			return nil, 0, fmt.Errorf("count releases: %w", err)
255-		}
256-	}
257-	offset := (page - 1) * perPage
258-	var rows pgx.Rows
259-	var err error
260-	if includeExcluded {
261-		rows, err = s.pool.Query(ctx,
262-			`SELECT r.id, r.source_id, r.version, COALESCE(r.raw_data,'{}'), r.released_at, r.created_at,
263-			        COALESCE(p.id::text,''), COALESCE(p.name,''), COALESCE(s.provider,''), COALESCE(s.repository,''),
264-			        CASE WHEN
265-			          (s.version_filter_include IS NOT NULL AND r.version !~ s.version_filter_include)
266-			          OR (s.version_filter_exclude IS NOT NULL AND r.version ~ s.version_filter_exclude)
267-			          OR (s.exclude_prereleases = true AND r.raw_data->>'prerelease' […]

> AGENT

The global `ListAllReleases` query already returns `project_id`, `project_name`, `provider`, and `repository` — all the metadata the feed needs. The current approach of per-project fetching is unnecessary.

Now let me check what the `Release` type in the frontend looks like, to confirm it has these fields.

> TOOL

tool_use Grep
id: toolu_01VQ3wNabBnCdGSR7YaGuQYj
```json
{
  "-A": 20,
  "output_mode": "content",
  "path": "/home/<USER>/web3/ReleaseBeacon/web/lib/api/types.ts",
  "pattern": "^export interface Release"
}
```

> TOOL

tool_use Grep
id: toolu_01GEc6oomJkxcfZ8x9iVF9pb
```json
{
  "-A": 15,
  "output_mode": "content",
  "path": "/home/<USER>/web3/ReleaseBeacon/web/lib/api/types.ts",
  "pattern": "^export interface SemanticRelease"
}
```

> TOOL

tool_result
id: toolu_01VQ3wNabBnCdGSR7YaGuQYj
```
76:export interface Release {
77-  id: string;
78-  source_id: string;
79-  version: string;
80-  raw_data?: Record<string, unknown>;
81-  released_at?: string;
82-  created_at: string;
83-  project_id?: string;
84-  project_name?: string;
85-  provider?: string;
86-  repository?: string;
87-  excluded?: boolean;
88-  semantic_release_id?: string;
89-  semantic_release_status?: string;
90-  semantic_release_urgency?: string;
91-}
92-
93-export interface ContextSource {
94-  id: string;
95-  project_id: string;
96-  type: string;
--
339:export interface ReleaseGate {
340-  id: string;
341-  project_id: string;
342-  required_sources?: string[];
343-  timeout_hours: number;
344-  version_mapping?: Record<string, VersionMapping>;
345-  nl_rule?: string;
346-  enabled: boolean;
347-  created_at: string;
348-  updated_at: string;
349-}
350-
351:export interface ReleaseGateInput {
352-  required_sources?: string[];
353-  timeout_hours: number;
354-  version_mapping?: Record<string, VersionMapping>;
355-  nl_rule?: string;
356-  enabled: boolean;
357-}
358-
359-export interface VersionReadiness {
360-  id: string;
361-  project_id: string;
362-  version: string;
363-  status: "pending" | "ready" | "timed_out";
364-  sources_met: string[];
365-  sources_missing: string[];
366-  nl_rule_passed?: boolean;
367-  timeout_at: string;
368-  opened_at?: string;
369-  agent_triggered: boolean;
370-  created_at: string;
371-  updated_at: string;
```

> TOOL

tool_result
id: toolu_01GEc6oomJkxcfZ8x9iVF9pb
```
109:export interface SemanticRelease {
110-  id: string;
111-  project_id: string;
112-  project_name?: string;
113-  version: string;
114-  report?: SemanticReport;
115-  status: string;
116-  error?: string;
117-  created_at: string;
118-  completed_at?: string;
119-}
120-
121-export interface SemanticReport {
122-  subject?: string;
123-  urgency?: string;
124-  urgency_reason?: string;
```

> AGENT

The `Release` type already has `project_id`, `project_name`, `provider`, and `repository` fields. The global endpoint returns all of these. This confirms the fix is straightforward.

## The Fix

The unified feed should use `releases.list()` and `semanticReleases.listAll()` instead of per-project fetching. This:
- Includes releases from **all projects** (not just the first 10)
- Uses a single server-side `ORDER BY` query (correct recency)
- Reduces 30+ HTTP requests down to 2

> TOOL

tool_use Edit
id: toolu_01Q78G4Q5YhTFgSFw1qkLryE
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/web3/ReleaseBeacon/web/components/dashboard/unified-feed.tsx",
  "old_string": "export function UnifiedFeed() {\n  const { t } = useTranslation();\n\n  const { data: projectsData } = useSWR(\"projects-for-dashboard\", () =>\n    projectsApi.list()\n  );\n\n  const { data: feedItems, isLoading } = useSWR(\n    projectsData ? \"unified-feed\" : null,\n    async () => {\n      if (!projectsData?.data?.length) return [];\n\n      const projectMap = new Map(\n        projectsData.data.map((p) => [p.id, p.name])\n      );\n      const projectSlice = projectsData.data.slice(0, 10);\n\n      // Fetch releases, sources, and semantic releases in parallel\n      const [releaseResults, sourceResults, srResults] = await Promise.all([\n        Promise.all(\n          projectSlice.map((p) =>\n            releasesApi.listByProject(p.id, 1).catch(() => null)\n          )\n        ),\n        Promise.all(\n          projectSlice.map((p) =>\n            sourcesApi.listByProject(p.id, 1).catch(() => null)\n          )\n        ),\n        Promise.all(\n          projectSlice.map((p) =>\n            srApi.list(p.id, 1).catch(() => null)\n          )\n        ),\n      ]);\n\n      // Build source lookup maps\n      const sourceMap = new Map<string, string>();\n      const providerMap = new Map<string, string>();\n      const sourceProjectMap = new Map<string, string>();\n      sourceResults\n        .filter((r): r is NonNullable<typeof r> => r !== null)\n        .flatMap((r) => r.data)\n        .forEach((s: Source) => {\n          sourceMap.set(s.id, s.repository);\n          providerMap.set(s.id, s.provider);\n          sourceProjectMap.set(s.id, s.project_id);\n        });\n\n      // Build feed items\n      const items: FeedItemType[] = [];\n\n      releaseResults\n        .filter((r): r is NonNullable<typeof r> => r !== null)\n        .flatMap((r) => r.data)\n        .forEach((rel) => {\n          const projectId = sourceProjectMap.get(rel.source_id);\n          items.push({\n            kind: \"release\",\n            data: rel,\n            repository: sourceMap.get(rel.source_id),\n            provider: providerMap.get(rel.source_id),\n            projectName: projectId ? […]

> TOOL

tool_result
id: toolu_01Q78G4Q5YhTFgSFw1qkLryE
```
The file /home/<USER>/web3/ReleaseBeacon/web/components/dashboard/unified-feed.tsx has been updated successfully.
```

> AGENT

Now clean up the unused imports.

> TOOL

tool_use Edit
id: toolu_014PBpttf15bYPGCPSrCJ74g
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/web3/ReleaseBeacon/web/components/dashboard/unified-feed.tsx",
  "old_string": "import {\n  projects as projectsApi,\n  releases as releasesApi,\n  sources as sourcesApi,\n  semanticReleases as srApi,\n} from \"@/lib/api/client\";",
  "new_string": "import {\n  releases as releasesApi,\n  semanticReleases as srApi,\n} from \"@/lib/api/client\";"
}
```

> TOOL

tool_result
id: toolu_014PBpttf15bYPGCPSrCJ74g
```
The file /home/<USER>/web3/ReleaseBeacon/web/components/dashboard/unified-feed.tsx has been updated successfully.
```

> AGENT

Now remove the unused `Source` type import.

> TOOL

tool_use Edit
id: toolu_01MKptsjHyArfEB8bst7Esfd
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/web3/ReleaseBeacon/web/components/dashboard/unified-feed.tsx",
  "old_string": "import type { Release, SemanticRelease, Source } from \"@/lib/api/types\";",
  "new_string": "import type { Release, SemanticRelease } from \"@/lib/api/types\";"
}
```

> TOOL

tool_result
id: toolu_01MKptsjHyArfEB8bst7Esfd
```
The file /home/<USER>/web3/ReleaseBeacon/web/components/dashboard/unified-feed.tsx has been updated successfully.
```

> AGENT

Let me verify the final state of the file.

> TOOL

tool_use Read
id: toolu_014WzU3KCSR4VVvh3cmCBkYj
```json
{
  "file_path": "/home/<USER>/web3/ReleaseBeacon/web/components/dashboard/unified-feed.tsx"
}
```

> TOOL

tool_result
id: toolu_014WzU3KCSR4VVvh3cmCBkYj
```
     1→// web/components/dashboard/unified-feed.tsx
     2→"use client";
     3→
     4→import useSWR from "swr";
     5→import Link from "next/link";
     6→import {
     7→  releases as releasesApi,
     8→  semanticReleases as srApi,
     9→} from "@/lib/api/client";
    10→import { VersionChip } from "@/components/ui/version-chip";
    11→import { getProviderIcon } from "@/components/ui/provider-badge";
    12→import { Sparkles } from "lucide-react";
    13→import type { Release, SemanticRelease } from "@/lib/api/types";
    14→import { timeAgo } from "@/lib/format";
    15→import { useTranslation } from "@/lib/i18n/context";
    16→
    17→type FeedItemType =
    18→  | { kind: "release"; data: Release; repository?: string; provider?: string; projectName?: string }
    19→  | { kind: "semantic"; data: SemanticRelease; projectName?: string };
    20→
    21→function getTimestamp(item: FeedItemType): number {
    22→  if (item.kind === "release") {
    23→    return new Date(item.data.released_at ?? item.data.created_at).getTime();
    24→  }
    25→  return new Date(item.data.created_at).getTime();
    26→}
    27→
    28→function getTimeStr(item: FeedItemType): string {
    29→  if (item.kind === "release") {
    30→    return item.data.released_at ?? item.data.created_at;
    31→  }
    32→  return item.data.created_at;
    33→}
    34→
    35→function ProviderIcon({ provider }: { provider: string }) {
    36→  const icon = getProviderIcon(provider);
    37→  if (!icon) return <div className="h-3.5 w-3.5 shrink-0" />;
    38→  return icon({ size: 14, className: "shrink-0 text-text-muted" });
    39→}
    40→
    41→export function UnifiedFeed() {
    42→  const { t } = useTranslation();
    43→
    44→  const { data: feedItems, isLoading } = useSWR( […]

> AGENT

Now I also need to check that the dashboard page's SSE revalidation still works — it was using `"unified-feed"` as the SWR key, and the new code still uses the same key.

> TOOL

tool_use Grep
id: toolu_01MD14yPNpo8nNtpT4wFi7WT
```json
{
  "output_mode": "content",
  "path": "/home/<USER>/web3/ReleaseBeacon/web/app/page.tsx",
  "pattern": "unified-feed|projects-for-dashboard"
}
```

> TOOL

tool_result
id: toolu_01MD14yPNpo8nNtpT4wFi7WT
```
8:import { UnifiedFeed } from "@/components/dashboard/unified-feed";
21:  const { data: projectsData, isLoading } = useSWR("projects-for-dashboard", () =>
38:            key === "unified-feed"
```

> AGENT

Good — `"unified-feed"` is still the SWR key used for revalidation on SSE events, and it matches. The `"projects-for-dashboard"` key is still used by `page.tsx` itself for other purposes (stats display, etc.), so that's unrelated.

Let me build the frontend to verify there are no type errors.

> TOOL

tool_use Bash
id: toolu_01Vg7woDmqD4MbCjRDxRDuvW
```json
{
  "command": "cd /home/<USER>/web3/ReleaseBeacon/web && npx tsc --noEmit 2>&1 | head -30",
  "description": "Type-check the frontend",
  "timeout": 60000
}
```

> TOOL

tool_result
id: toolu_01Vg7woDmqD4MbCjRDxRDuvW
```

```

> AGENT

Clean build, no errors.

## Summary

**Root cause:** The Recent Activity feed was fetching releases per-project (limited to the first 10 projects, page 1 each), then merging client-side. This had two problems:

1. **Projects beyond #10 were completely invisible** — their releases never appeared in the feed
2. **Only page 1 per project was fetched** — with default perPage=25 per project, the client-side merge could miss the truly most recent releases across all projects since SQL `ORDER BY` was applied per-project, not globally

**Fix:** Replaced the N+1 per-project fetching with two global API calls:
- `GET /api/v1/releases?page=1&per_page=15` — returns the 15 most recent releases across **all** projects, already sorted by `COALESCE(released_at, created_at) DESC` server-side
- `GET /api/v1/semantic-releases?page=1&per_page=15` — returns the 15 most recent semantic releases globally

Both endpoints already return all needed metadata (project name, provider, repository) via JOINs in the database query, so no additional source lookups are needed.

This also reduces the number of HTTP requests from **30+** (10 projects × 3 endpoints) down to **2**.