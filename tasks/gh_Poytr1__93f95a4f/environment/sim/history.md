[DEVELOPER]: Please apply the similar filter ribbon of releases page to the subscriptions page, include the release chanel and the release type

[AGENT]: Let me start by exploring the current implementation of both pages to understand the filter ribbon on the releases page and the subscriptions page structure.

[AGENT]: Now let me read the key files in detail.

[AGENT]: Now let me check the Subscription type and understand what fields are available for filtering, and also look at the subscriptions API.

[AGENT]: Now I have a clear picture. The subscriptions page needs a `FilterBar` added with filters for: 1. **Release Channel** (the notification channel — `channel_id`) 2. **Release Type** (`source_release` or `semantic_release`) The filtering will be client-side since the subscriptions API just returns all subscriptions. Let me also check the subscriptions API to confirm.

[AGENT]: Good — the subscriptions API fetches all at once (no server-side filtering), so the filtering will be client-side. Now I'll implement the changes.

[AGENT]: Now wrap the page in Suspense and add the filter logic:

[AGENT]: Now add the filter config and client-side filtering logic. I need to add it after the `sourcesMap` SWR and before the state declarations:

[AGENT]: Now add the FilterBar between the header and the loading/content section:

[AGENT]: Now I need to make sure the grouped subscriptions use the filtered list, and that selection logic works with filtered results. The `grouped` memo already uses `subscriptions`, which now points to the filtered list. Let me also clear selections when filters change. Let me verify the final state:

[AGENT]: Now let me typecheck to verify it compiles.

[AGENT]: TypeScript compilation succeeded with no errors. Here's what I did: **Added a filter ribbon to the subscriptions page** (`web/app/subscriptions/page.tsx`) matching the releases page pattern: 1. **Imported** `FilterBar`, `FilterConfig` from `@/components/filters/filter-bar` and `useFilterParams` from `@/components/filters/use-filter-params` 2. **Added two filters:** - **Channel** — select filter populated from the channels API, filters by `channel_id` - **Type** — select filter with options "Source Release" and "Semantic Release", filters by subscription `type` 3. **Client-side filtering** — since the subscriptions API returns all results at once, filtering is applied in a `useMemo` before grouping 4. **Wrapped in `<Suspense>`** — required by `useFilterParams` which reads URL search params (same pattern as the releases page) The filter state syncs to URL query params (`?channel=...&type=...`), just like the releases page.