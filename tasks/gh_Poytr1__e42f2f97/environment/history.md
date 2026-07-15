> DEVELOPER

Please apply the similar filter ribbon of releases page to the subscriptions page, include the release chanel and the release type

> AGENT

Let me start by exploring the current implementation of both pages to understand the filter ribbon on the releases page and the subscriptions page structure.

> TOOL

tool_use Agent
id: toolu_vrtx_01Rw3rXVJMkmXRmXh4dzY1Pi
```json
{
  "subagent_type": "Explore",
  "description": "Explore filter ribbon components",
  "prompt": "I need to understand the filter ribbon implementation on the releases page and the subscriptions page in a Next.js frontend located at `web/`. \n\n1. Find the releases page and its filter ribbon/filter UI components\n2. Find the subscriptions page\n3. Find any shared filter components or filter-related utilities\n4. Look for how \"release channel\" and \"release type\" filters are implemented\n\nSearch thoroughly across `web/src/` for:\n- Filter components (FilterRibbon, FilterBar, filter chips, etc.)\n- The releases page component\n- The subscriptions page component\n- Any types/enums for release channels and release types\n\nReport file paths, line numbers, and key code snippets for all of these."
}
```

> TOOL

tool_result
id: toolu_vrtx_01Rw3rXVJMkmXRmXh4dzY1Pi
```
Perfect! Now I have enough information. Let me create a comprehensive report with all the findings.

## Summary Report

I've completed a thorough analysis of the filter ribbon implementation across the releases and subscriptions pages in the Next.js frontend. Here are my findings:

### 1. **Filter Components & Architecture**

**Filter Bar Component** (`/Users/pc/web3/ReleaseBeacon/web/components/filters/filter-bar.tsx`, lines 1-289)
- Shared reusable `FilterBar` component used across multiple pages
- Supports three filter types: `"select"`, `"boolean"`, and `"date-range"`
- Features:
  - Active filter chips that can be edited or removed individually
  - Popover UI with search functionality for select filters
  - Date presets (Last 7/30/90 days, Last year)
  - "Add filter" button to add new filters
  - "Clear all" button for bulk removal
  - Dynamic UI that shows available vs active filters

**Filter Params Hook** (`/Users/pc/web3/ReleaseBeacon/web/components/filters/use-filter-params.ts`, lines 1-71)
- Syncs filter state with URL query parameters
- Only allows whitelisted keys to prevent cross-page filter leakage
- Handles pagination reset when navigating between pages
- Maintains defaults during server-side initialization

### 2. **Releases Page Implementation**

**File**: `/Users/pc/web3/ReleaseBeacon/web/app/releases/page.tsx` (lines 1-509)

**Filter Configuration** (lines 59-103):
- Allowed filter keys: `["project", "provider", "urgency", "date", "excluded"]`
- Default filters: `{ excluded: "true" }`
- Five […]

> AGENT

Now let me read the key files in detail.

> TOOL

tool_use Read
id: toolu_vrtx_01P7V4MBbBiu7uoeztA3DZk3
```json
{
  "file_path": "/Users/pc/web3/ReleaseBeacon/web/app/subscriptions/page.tsx"
}
```

> TOOL

tool_use Read
id: toolu_vrtx_012o6dVHcts1tmFYxMxtvKo9
```json
{
  "file_path": "/Users/pc/web3/ReleaseBeacon/web/app/releases/page.tsx"
}
```

> TOOL

tool_use Read
id: toolu_vrtx_01C1kBR55ydFmxMhimxrZ5Mr
```json
{
  "file_path": "/Users/pc/web3/ReleaseBeacon/web/components/filters/filter-bar.tsx"
}
```

> TOOL

tool_result
id: toolu_vrtx_01P7V4MBbBiu7uoeztA3DZk3
```
1	"use client";
2	
3	import { useState, useMemo } from "react";
4	import useSWR, { mutate } from "swr";
5	import {
6	  subscriptions as subsApi,
7	  channels as channelsApi,
8	  projects as projectsApi,
9	  sources as sourcesApi,
10	} from "@/lib/api/client";
11	import type { Source, Subscription } from "@/lib/api/types";
12	import { Plus, Pencil, Trash2, ChevronRight } from "lucide-react";
13	import { Checkbox } from "@/components/ui/checkbox";
14	import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
15	import { ConfirmDialog } from "@/components/ui/confirm-dialog";
16	import { SubscriptionForm } from "@/components/subscriptions/subscription-form";
17	import { useTranslation } from "@/lib/i18n/context";
18	
19	const SUB_TYPE_COLORS: Record<string, { bg: string; text: string }> = {
20	  source_release: { bg: "#1a1a1a", text: "#ffffff" },
21	  semantic_release: { bg: "#2563eb", text: "#ffffff" },
22	};
23	
24	function SubTypeBadge({ type }: { type: string }) {
25	  const colors = SUB_TYPE_COLORS[type] ?? { bg: "#6b7280", text: "#ffffff" };
26	  return (
27	    <span
28	      className="inline-flex items-center rounded-full px-2.5 py-0.5"
29	      style={{
30	        backgroundColor: colors.bg,
31	        color: colors.text,
32	        fontFamily: "var(--font-dm-sans)",
33	        fontSize: "12px",
34	        fontWeight: 500,
35	        lineHeight: "16px",
36	      }}
37	    >
38	      {type}
39	    </span>
40	  );
41 […]

> TOOL

tool_result
id: toolu_vrtx_01C1kBR55ydFmxMhimxrZ5Mr
```
1	"use client";
2	
3	import { useState, useRef, useEffect } from "react";
4	import { X, Plus, Search, Check } from "lucide-react";
5	
6	/* Types */
7	
8	export interface FilterOption {
9	  value: string;
10	  label: string;
11	}
12	
13	export interface FilterConfig {
14	  key: string;
15	  label: string;
16	  type: "select" | "boolean" | "date-range";
17	  options?: FilterOption[];
18	  defaultValue?: string;
19	}
20	
21	export interface FilterBarProps {
22	  filters: FilterConfig[];
23	  value: Record<string, string>;
24	  onChange: (value: Record<string, string>) => void;
25	}
26	
27	/* Date presets */
28	
29	const DATE_PRESETS: FilterOption[] = [
30	  { value: "7d", label: "Last 7 days" },
31	  { value: "30d", label: "Last 30 days" },
32	  { value: "90d", label: "Last 90 days" },
33	  { value: "1y", label: "Last year" },
34	];
35	
36	export function expandDatePreset(preset: string): { date_from: string; date_to?: string } {
37	  const now = new Date();
38	  let from: Date;
39	  switch (preset) {
40	    case "7d":
41	      from = new Date(now.getTime() - 7 * 86400000);
42	      break;
43	    case "30d":
44	      from = new Date(now.getTime() - 30 * 86400000);
45	      break; […]

> TOOL

tool_result
id: toolu_vrtx_012o6dVHcts1tmFYxMxtvKo9
```
1	"use client";
2	
3	import { useState, useEffect, useCallback, Suspense } from "react";
4	import useSWR, { mutate } from "swr";
5	import Link from "next/link";
6	import {
7	  releases as releasesApi,
8	  projects as projectsApi,
9	  agent,
10	} from "@/lib/api/client";
11	import type { ReleaseFilters } from "@/lib/api/client";
12	import { ProviderBadge } from "@/components/ui/provider-badge";
13	import { VersionChip } from "@/components/ui/version-chip";
14	import type { Release } from "@/lib/api/types";
15	import { ExternalLink, Sparkles, Loader2 } from "lucide-react";
16	import { UrgencyPill } from "@/components/ui/urgency-pill";
17	import { useTranslation } from "@/lib/i18n/context";
18	import { FilterBar, FilterConfig, expandDatePreset } from "@/components/filters/filter-bar";
19	import { useFilterParams } from "@/components/filters/use-filter-params";
20	
21	import { timeAgo } from "@/lib/format";
22	
23	const PER_PAGE = 15;
24	const SSE_BASE = process.env.NEXT_PUBLIC_API_URL || "/api/v1";
25	
26	function getProviderUrl(
27	  provider: string,
28	  repository: string,
29	  version: string
30	): string | null {
31	  switch (provider) {
32	    case "github":
33	      return `https://github.com/${repository}/releases/tag/${version}`;
34	    case "dockerhub":
35	      return `https://hub.docker.com/r/${repository}/tags?name=${encodeURIComponent(version)}`;
36	    case "ecr-public":
37	      return `https://gallery.ecr.aws/${repository}`;
38	    case "gitlab":
39	      return `https://gitlab.com/${repository}/-/releases/${version}`;
40	    default:
41	      return null;
42	  }
43	}
44	
45	/* ------------------------------------------------------------------ */
46 […]

> AGENT

Now let me check the Subscription type and understand what fields are available for filtering, and also look at the subscriptions API.

> TOOL

tool_use Read
id: toolu_vrtx_017aP5bFTUT61WYccVdBVYeT
```json
{
  "file_path": "/Users/pc/web3/ReleaseBeacon/web/lib/api/types.ts"
}
```

> TOOL

tool_use Read
id: toolu_vrtx_01BD4pZyA4kXLxSBwBj4AySX
```json
{
  "file_path": "/Users/pc/web3/ReleaseBeacon/web/components/filters/use-filter-params.ts"
}
```

> TOOL

tool_result
id: toolu_vrtx_017aP5bFTUT61WYccVdBVYeT
```
1	// web/lib/api/types.ts
2	
3	// --- Response Envelope ---
4	
5	export interface ApiResponse<T> {
6	  data: T;
7	  meta?: ApiMeta;
8	  error?: ApiError;
9	}
10	
11	export interface ApiMeta {
12	  page: number;
13	  per_page: number;
14	  total: number;
15	}
16	
17	export interface ApiError {
18	  code: string;
19	  message: string;
20	}
21	
22	// --- Domain Models (all IDs are UUID strings) ---
23	
24	export interface Project {
25	  id: string;
26	  name: string;
27	  description?: string;
28	  agent_prompt?: string;
29	  agent_rules?: AgentRules;
30	  created_at: string;
31	  updated_at: string;
32	}
33	
34	export interface AgentRules {
35	  on_major_release?: boolean;
36	  on_minor_release?: boolean;
37	  on_security_patch?: boolean;
38	  version_pattern?: string;
39	}
40	
41	export interface ProjectInput {
42	  name: string;
43	  description?: string;
44	  agent_prompt?: string;
45	  agent_rules?: AgentRules;
46	}
47	
48	export interface Source {
49	  id: string;
50	  project_id: string;
51	  provider: string;
52	  repository: string;
53	  poll_interval_seconds: number;
54	  enabled: boolean;
55	  config?: Record<string, unknown>;
56	  version_filter_include?: string;
57	  version_filter_exclude?: string;
58	  exclude_prereleases?: boolean;
59	  last_polled_at?: string;
60	  last_error?: string;
61	  created_at: string;
62	  updated_at: string;
63	}
64	
65	export interface SourceInput { […]

> TOOL

tool_result
id: toolu_vrtx_01BD4pZyA4kXLxSBwBj4AySX
```
1	"use client";
2	
3	import { useState, useCallback, useEffect } from "react";
4	
5	/**
6	 * useFilterParams syncs a Record<string, string> of filter values with URL query params.
7	 * Only reads/writes params whose keys are in `allowedKeys` to prevent cross-page leakage.
8	 */
9	export function useFilterParams(
10	  allowedKeys: string[],
11	  defaults?: Record<string, string>
12	): {
13	  filters: Record<string, string>;
14	  setFilters: (next: Record<string, string>) => void;
15	  page: number;
16	  setPage: (p: number) => void;
17	} {
18	  const [filters, setFiltersState] = useState<Record<string, string>>(() => {
19	    if (typeof window === "undefined") return defaults ?? {};
20	    const params = new URLSearchParams(window.location.search);
21	    const parsed: Record<string, string> = { ...(defaults ?? {}) };
22	    const allowed = new Set(allowedKeys);
23	    params.forEach((value, key) => {
24	      if (key !== "page" && allowed.has(key)) {
25	        parsed[key] = value;
26	      }
27	    });
28	    return parsed;
29	  });
30	
31	  const [page, setPageState] = useState<number>(() => {
32	    if (typeof window === "undefined") return 1;
33	    const params = new URLSearchParams(window.location.search);
34	    const p = params.get("page");
35	    if (!p) return 1;
36	    // If URL contains params not in this page's allowed set, […]

> AGENT

Now I have a clear picture. The subscriptions page needs a `FilterBar` added with filters for:
1. **Release Channel** (the notification channel — `channel_id`)
2. **Release Type** (`source_release` or `semantic_release`)

The filtering will be client-side since the subscriptions API just returns all subscriptions. Let me also check the subscriptions API to confirm.

> TOOL

tool_use Grep
id: toolu_vrtx_015tNzpA37n29ZdhrHSSwSS7
```json
{
  "pattern": "subscriptions.*list|subs.*list",
  "path": "/Users/pc/web3/ReleaseBeacon/web/lib/api/client.ts",
  "output_mode": "content",
  "-C": 3
}
```

> TOOL

tool_result
id: toolu_vrtx_015tNzpA37n29ZdhrHSSwSS7
```
No matches found
```

> TOOL

tool_use Grep
id: toolu_vrtx_015MAfNS5H5v4UENkU8GnwuW
```json
{
  "pattern": "subscriptions",
  "path": "/Users/pc/web3/ReleaseBeacon/web/lib/api/client.ts",
  "output_mode": "content",
  "-C": 3
}
```

> TOOL

tool_result
id: toolu_vrtx_015MAfNS5H5v4UENkU8GnwuW
```
174-
175-// --- Subscriptions ---
176-
177:export const subscriptions = {
178-  list: (page = 1, perPage = 100) =>
179:    request<ApiResponse<Subscription[]>>(`/subscriptions?page=${page}&per_page=${perPage}`),
180:  get: (id: string) => request<ApiResponse<Subscription>>(`/subscriptions/${id}`),
181-  create: (input: SubscriptionInput) =>
182:    request<ApiResponse<Subscription>>("/subscriptions", {
183-      method: "POST",
184-      body: JSON.stringify(input),
185-    }),
186-  batchCreate: (input: BatchSubscriptionInput) =>
187:    request<ApiResponse<Subscription[]>>("/subscriptions/batch", {
188-      method: "POST",
189-      body: JSON.stringify(input),
190-    }),
191-  update: (id: string, input: SubscriptionInput) =>
192:    request<ApiResponse<Subscription>>(`/subscriptions/${id}`, {
193-      method: "PUT",
194-      body: JSON.stringify(input),
195-    }),
196-  delete: (id: string) =>
197:    request<ApiResponse<null>>(`/subscriptions/${id}`, { method: "DELETE" }),
198-  batchDelete: (input: BatchDeleteSubscriptionInput) =>
199:    request<ApiResponse<null>>("/subscriptions/batch", {
200-      method: "DELETE",
201-      body: JSON.stringify(input),
202-    }),
```

> AGENT

Good — the subscriptions API fetches all at once (no server-side filtering), so the filtering will be client-side. Now I'll implement the changes.

> TOOL

tool_use Edit
id: toolu_vrtx_01PjqsLwaFE1RcLRKVs41PTR
```json
{
  "replace_all": false,
  "file_path": "/Users/pc/web3/ReleaseBeacon/web/app/subscriptions/page.tsx",
  "old_string": "import { useState, useMemo } from \"react\";\nimport useSWR, { mutate } from \"swr\";\nimport {\n  subscriptions as subsApi,\n  channels as channelsApi,\n  projects as projectsApi,\n  sources as sourcesApi,\n} from \"@/lib/api/client\";\nimport type { Source, Subscription } from \"@/lib/api/types\";\nimport { Plus, Pencil, Trash2, ChevronRight } from \"lucide-react\";",
  "new_string": "import { useState, useMemo, Suspense } from \"react\";\nimport useSWR, { mutate } from \"swr\";\nimport {\n  subscriptions as subsApi,\n  channels as channelsApi,\n  projects as projectsApi,\n  sources as sourcesApi,\n} from \"@/lib/api/client\";\nimport type { Source, Subscription } from \"@/lib/api/types\";\nimport { Plus, Pencil, Trash2, ChevronRight } from \"lucide-react\";\nimport { FilterBar, FilterConfig } from \"@/components/filters/filter-bar\";\nimport { useFilterParams } from \"@/components/filters/use-filter-params\";"
}
```

> TOOL

tool_result
id: toolu_vrtx_01PjqsLwaFE1RcLRKVs41PTR
```
The file /Users/pc/web3/ReleaseBeacon/web/app/subscriptions/page.tsx has been updated successfully.
```

> AGENT

Now wrap the page in Suspense and add the filter logic:

> TOOL

tool_use Edit
id: toolu_vrtx_01QXCf6GJPt3jdeRFKtX5rh4
```json
{
  "replace_all": false,
  "file_path": "/Users/pc/web3/ReleaseBeacon/web/app/subscriptions/page.tsx",
  "old_string": "export default function SubscriptionsPage() {\n  const { t } = useTranslation();\n  const { data, isLoading } = useSWR(\"subscriptions\", () => subsApi.list());\n  const { data: channelsData } = useSWR(\"channels-for-sub-list\", () =>\n    channelsApi.list()\n  );\n  const { data: projectsData } = useSWR(\"projects-for-sub-list\", () =>\n    projectsApi.list(1, 100)\n  );",
  "new_string": "export default function SubscriptionsPage() {\n  return (\n    <Suspense>\n      <SubscriptionsPageInner />\n    </Suspense>\n  );\n}\n\nfunction SubscriptionsPageInner() {\n  const { t } = useTranslation();\n  const FILTER_KEYS = [\"channel\", \"type\"];\n  const { filters, setFilters } = useFilterParams(FILTER_KEYS);\n  const { data, isLoading } = useSWR(\"subscriptions\", () => subsApi.list());\n  const { data: channelsData } = useSWR(\"channels-for-sub-list\", () =>\n    channelsApi.list()\n  );\n  const { data: projectsData } = useSWR(\"projects-for-sub-list\", () =>\n    projectsApi.list(1, 100)\n  );"
}
```

> TOOL

tool_result
id: toolu_vrtx_01QXCf6GJPt3jdeRFKtX5rh4
```
The file /Users/pc/web3/ReleaseBeacon/web/app/subscriptions/page.tsx has been updated successfully.
```

> AGENT

Now add the filter config and client-side filtering logic. I need to add it after the `sourcesMap` SWR and before the state declarations:

> TOOL

tool_use Edit
id: toolu_vrtx_01VBG2zY3uPA1b6xyfbqjWaN
```json
{
  "replace_all": false,
  "file_path": "/Users/pc/web3/ReleaseBeacon/web/app/subscriptions/page.tsx",
  "old_string": "  const [createOpen, setCreateOpen] = useState(false);\n  const [editingSub, setEditingSub] = useState<Subscription | null>(null);\n  const [deletingId, setDeletingId] = useState<string | null>(null);\n  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());\n  const [batchDeleteOpen, setBatchDeleteOpen] = useState(false);\n  const [collapsedChannels, setCollapsedChannels] = useState<Set<string>>(new Set());\n\n  const getChannelName = (id: string) =>\n    channelsData?.data.find((c) => c.id === id)?.name ?? id;\n\n  const getChannelType = (id: string) =>\n    channelsData?.data.find((c) => c.id === id)?.type ?? \"\";\n\n  const getProjectName = (id: string) =>\n    projectsData?.data.find((p) => p.id === id)?.name ?? id;\n\n  const getSourceLabel = (id: string) => {\n    const source = sourcesMap?.[id];\n    return source ? `${source.provider}: ${source.repository}` : id;\n  };\n\n  const subscriptions = data?.data ?? [];",
  "new_string": "  const [createOpen, setCreateOpen] = useState(false);\n  const [editingSub, setEditingSub] = useState<Subscription | null>(null);\n  const [deletingId, setDeletingId] = useState<string | null>(null);\n  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());\n  const [batchDeleteOpen, setBatchDeleteOpen] = useState(false);\n  const [collapsedChannels, setCollapsedChannels] = useState<Set<string>>(new Set());\n\n  const getChannelName = (id: string) =>\n    channelsData?.data.find((c) => c.id === id)?.name ?? id;\n\n  const getChannelType = (id: string) =>\n    channelsData?.data.find((c) => c.id === id)?.type ?? \"\";\n\n  const getProjectName = (id: string) =>\n    projectsData?.data.find((p) => p.id === id)?.name ?? id;\n\n  const getSourceLabel = (id: string) => {\n    const source = sourcesMap?.[id];\n […]

> TOOL

tool_result
id: toolu_vrtx_01VBG2zY3uPA1b6xyfbqjWaN
```
The file /Users/pc/web3/ReleaseBeacon/web/app/subscriptions/page.tsx has been updated successfully.
```

> AGENT

Now add the FilterBar between the header and the loading/content section:

> TOOL

tool_use Edit
id: toolu_vrtx_018P1xrga3Gvb2okR6jXhkHg
```json
{
  "replace_all": false,
  "file_path": "/Users/pc/web3/ReleaseBeacon/web/app/subscriptions/page.tsx",
  "old_string": "      </div>\n\n      {isLoading ? (",
  "new_string": "      </div>\n\n      {/* Filters */}\n      <FilterBar filters={filterConfig} value={filters} onChange={setFilters} />\n\n      {isLoading ? ("
}
```

> TOOL

tool_result
id: toolu_vrtx_018P1xrga3Gvb2okR6jXhkHg
```
The file /Users/pc/web3/ReleaseBeacon/web/app/subscriptions/page.tsx has been updated successfully.
```

> AGENT

Now I need to make sure the grouped subscriptions use the filtered list, and that selection logic works with filtered results. The `grouped` memo already uses `subscriptions`, which now points to the filtered list. Let me also clear selections when filters change. Let me verify the final state:

> TOOL

tool_use Read
id: toolu_vrtx_01PqB3xBbBsxq1yRHJqujFt4
```json
{
  "file_path": "/Users/pc/web3/ReleaseBeacon/web/app/subscriptions/page.tsx"
}
```

> TOOL

tool_result
id: toolu_vrtx_01PqB3xBbBsxq1yRHJqujFt4
```
1	"use client";
2	
3	import { useState, useMemo, Suspense } from "react";
4	import useSWR, { mutate } from "swr";
5	import {
6	  subscriptions as subsApi,
7	  channels as channelsApi,
8	  projects as projectsApi,
9	  sources as sourcesApi,
10	} from "@/lib/api/client";
11	import type { Source, Subscription } from "@/lib/api/types";
12	import { Plus, Pencil, Trash2, ChevronRight } from "lucide-react";
13	import { FilterBar, FilterConfig } from "@/components/filters/filter-bar";
14	import { useFilterParams } from "@/components/filters/use-filter-params";
15	import { Checkbox } from "@/components/ui/checkbox";
16	import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
17	import { ConfirmDialog } from "@/components/ui/confirm-dialog";
18	import { SubscriptionForm } from "@/components/subscriptions/subscription-form";
19	import { useTranslation } from "@/lib/i18n/context";
20	
21	const SUB_TYPE_COLORS: Record<string, { bg: string; text: string }> = {
22	  source_release: { bg: "#1a1a1a", text: "#ffffff" },
23	  semantic_release: { bg: "#2563eb", text: "#ffffff" },
24	};
25	
26	function SubTypeBadge({ type }: { type: string }) {
27	  const colors = SUB_TYPE_COLORS[type] ?? { bg: "#6b7280", text: "#ffffff" };
28	  return (
29	    <span
30	      className="inline-flex items-center rounded-full px-2.5 py-0.5"
31	      style={{
32	        backgroundColor: colors.bg,
33	        color: colors.text,
34	        fontFamily: "var(--font-dm-sans)",
35	        fontSize: "12px",
36 […]

> AGENT

Now let me typecheck to verify it compiles.

> TOOL

tool_use Skill
id: toolu_vrtx_01RnhvwDkgKTQ9FtemFqwATP
```json
{
  "skill": "nextjs-typecheck"
}
```

> TOOL

tool_result
id: toolu_vrtx_01RnhvwDkgKTQ9FtemFqwATP
```
Launching skill: nextjs-typecheck
```

> TOOL

tool_use Bash
id: toolu_vrtx_01Qtk9GVizeJWzrbh29pmkGn
```json
{
  "command": "bash /Users/pc/.claude/skills/nextjs-typecheck/scripts/nextjs-typecheck.sh ./web",
  "description": "Run TypeScript type check on Next.js frontend",
  "timeout": 60000
}
```

> TOOL

tool_result
id: toolu_vrtx_01Qtk9GVizeJWzrbh29pmkGn
```
=== TypeScript type check: ./web ===

No type errors found.
```

> AGENT

TypeScript compilation succeeded with no errors.

Here's what I did:

**Added a filter ribbon to the subscriptions page** (`web/app/subscriptions/page.tsx`) matching the releases page pattern:

1. **Imported** `FilterBar`, `FilterConfig` from `@/components/filters/filter-bar` and `useFilterParams` from `@/components/filters/use-filter-params`
2. **Added two filters:**
   - **Channel** — select filter populated from the channels API, filters by `channel_id`
   - **Type** — select filter with options "Source Release" and "Semantic Release", filters by subscription `type`
3. **Client-side filtering** — since the subscriptions API returns all results at once, filtering is applied in a `useMemo` before grouping
4. **Wrapped in `<Suspense>`** — required by `useFilterParams` which reads URL search params (same pattern as the releases page)

The filter state syncs to URL query params (`?channel=...&type=...`), just like the releases page.