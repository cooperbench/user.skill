---
session_id: "8c02b305-e7a0-4bdf-970e-c5c3088e513e:subagents"
developer: "dc:dc_000"
split: train
source: dataclaw
repo: peteromallet/my-dataclaw-data
start_time: "2026-04-13T22:55:00.886Z"
n_turns: 73
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

In this workspace, the user has a UI where clicking into a "shot" should already know whether it will be "batch" or "timeline" mode. I need to find: 1. How shots are fetched (look for fetch/query related to shots, batches, timelines) 2. Any logic that determines whether a shot is batch vs timeline 3. The component(s) that handle clicking into a shot Search thoroughly across all repos/packages in /Users/user_c042661f/Documents/reigh-workspace. Look for keywords like "batch", "timeline", "shot", "mode" in combination. Check for React components, API routes, fetch calls, queries, etc. Report file paths and relevant code snippets.

> AGENT

I'll conduct a thorough search across the workspace to find how shots are fetched and how the batch vs timeline mode is determined. Let me start by exploring the repository structure and then searching for relevant code.

> AGENT

Let me get a better overview of the workspace structure:

> AGENT

Now let me search for files related to shots, batches, and timelines in the main app directory:

> AGENT

Good! Now let me look more specifically at the shot-related components and routes:

> AGENT

Now let me look at the ShotsPage and understand how shots are fetched and displayed:

> AGENT

Now let me look at how shots are clicked and look for any batch/timeline mode logic:

> AGENT

Let me search more specifically for where shots are opened/clicked and check for batch vs timeline mode determination:

> AGENT

Let me look at the CreateShotModal to understand where shots are created and configured:

> AGENT

Let me look at the useShotSelection hook and examine the SortableShotItem component to understand how clicking on shots works:

> AGENT

Now let me look at the VideoShotDisplay and check for mode logic there:

> AGENT

Now let me search specifically for where "batch" vs "timeline" mode is determined. Let me check the ShotEditor components:

> AGENT

Let me search more broadly for mode determination logic:

> AGENT

Let me look at the ShotImageManager to see where the generationMode prop comes from in ShotsPage:

> AGENT

Good! Now let me look at the types to see how generationMode is defined:

> AGENT

Perfect! Now let me trace back to see where shots are opened from different tools. Let me check how the VideoTravelToolPage and other tools determine which mode to use:

> AGENT

Let me look at the ShotEditorLayout to see how the mode is determined there:

> AGENT

Now let me look at the TimelineSection where the generationMode is displayed/changed:

> AGENT

Let me continue reading this file and look at ShotImagesEditor:

> AGENT

Let me search for where the generationMode is stored or passed when opening a shot. Let me check the shot fetching logic:

> AGENT

Now let me check the Shot type definition to see if there's any mode property:

> AGENT

Now let me check where the shot's generationMode is determined. Let me look for useModeReadiness or similar logic:

> AGENT

Let me search for where the generationMode is actually set when opening a shot. Let me check the ShotEditorModel or similar:

> AGENT

Let me check the useShotEditorController:

> AGENT

Let me continue reading and look for generationMode initialization:

> AGENT

Let me search for where the generationMode is initialized from the generationModeSettings:

> AGENT

Let me search more specifically for the provider that manages generationMode:

> AGENT

Let me search for where generationMode hooks are defined:

> AGENT

Now let me search for the useGenerationModeSettings function definition in the provider:

> AGENT

Perfect! Now let me look at the useShotSettings hook to see where generationMode is stored:

> AGENT

Great! Now let me check the VideoTravelSettings type to see its properties:

> AGENT

Perfect! Now let me read the full VideoTravelSettings definition:

> AGENT

Perfect! Now I have the full picture. Let me create a summary with all the relevant code paths. Let me also check if there's a ShotListDisplay that shows the shot clicking:

> AGENT

Let me check the VideoTravelPageModel to understand the shot selection flow:

> AGENT

Perfect! Now I have enough information to create a comprehensive report. Let me compile the findings: ## Summary I've thoroughly searched the reigh-app codebase to understand how shots are fetched and how the batch vs timeline mode is determined when clicking into a shot. Here are the key findings: ### 1. **Shot Fetching Logic** **File: `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/hooks/shots/useShotsQueries.ts`** - `useListShots()` is the primary hook that fetches all shots for a project (lines 21-128) - Queries the `shots` table ordered by position, then fetches all `shot_generations` in a single batch query - Returns shot data with computed stats: `imageCount`, `positionedImageCount`, `unpositionedImageCount`, `hasUnpositionedImages` - Each shot is enriched with its `images` array (of type `GenerationRow`) **File: `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/domains/generation/types/shot.ts`** - `Shot` type has NO `mode` property stored in the database - Shot structure: `id`, `name`, `created_at`, `updated_at`, `project_id`, `aspect_ratio`, `position`, `settings` ### 2. **How Batch vs Timeline Mode is Determined** The mode is **NOT** determined by the shot itself, but by **per-shot settings** stored in the `shots.settings` JSON column. **File: `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/settings.ts` (line 83)** ```typescript export interface VideoTravelSettings { // ... other fields generationMode: 'batch' | 'by-pair' | 'timeline'; // Line 83 // ... default is 'timeline' (line 178) } ``` **File: `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/providers/VideoTravelSettingsProvider.tsx` (lines 409-417)** ```typescript export function useGenerationModeSettings() { const { settings, handlers } = useVideoTravelSettings(); return useMemo(() => ({ generationMode: settings.generationMode || 'timeline', // Default is 'timeline' videoControlMode: settings.videoControlMode || 'batch', setGenerationMode: handlers.handleGenerationModeChange, setVideoControlMode: handlers.handleVideoControlModeChange, }), [settings.generationMode, settings.videoControlMode, handlers]); } ``` ### 3. **Component Flow When Clicking Into a Shot** **File: `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/pages/ShotsPage.tsx`** - Uses `useShotSelection()` hook which sets `currentShotId` when a shot is clicked - Hardcodes `generationMode="batch"` when displaying `ShotImageManager` (line 79) **File: `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/VideoGallery/SortableShotItem.tsx`** - `onSelectShot()` callback is triggered on click (line 250) - Simply calls the parent's `onSelectShot` handler **File: `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/pages/shots/hooks/useShotSelection.ts`** - `handleSelectShot()` sets the `currentShotId` in context (lines 68-70) - Fetches images for the selected shot via `useShotImages(shotId)` (line 36) ### 4. **Settings Fetching When Opening a Shot** **File: `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/hooks/settings/useShotSettings.ts`** - `useShotSettings()` hook loads settings for a specific shot from the database (lines 55-57) - Uses `useAutoSaveSettings()` which queries the tool settings stored in the `shots.settings` JSON - Falls back to inherited defaults if the shot doesn't have specific settings (lines 59-76) **File: `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/ShotEditor/useShotEditorController.ts`** - Bootstrap phase calls `useShotEditorBootstrap()` (lines 102-183) which calls: - `useGenerationModeSettings()` to get the current mode (line 112) - `useShotSettings()` to load shot-specific settings - The mode is then passed to `TimelineSection` (line 149) ### 5. **Key Insight: The […]

> DEVELOPER

In /Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/, I need to understand how clicking into a shot works on the Video Travel tool page. Specifically: 1. Find the shot list/gallery component that shows shots before you click into one 2. Find the click handler that selects a shot 3. Find where generationMode (batch vs timeline) is determined when entering a shot 4. Find the ShotEditor or similar component that renders after a shot is selected 5. Look for any fetch/query that loads shot settings (especially generationMode) either before or after clicking into a shot Key files to check: - components/VideoGallery/ directory - components/ShotEditor/ directory - hooks/settings/ directory - The main page component for the video travel tool Report the exact file paths, line numbers, and relevant code for the flow from "shot list" -> "click shot" -> "determine mode" -> "render editor".

> AGENT

I'll help you understand the click-into-shot flow in the Video Travel tool. Let me systematically explore the structure and trace the data flow.

> AGENT

Now let me look at the directory structure more clearly and find the main page component:

> AGENT

Great! Let me examine the key files in order:

> AGENT

Now let me look at the page model to understand the flow better, and check the shot selection/editor relationship:

> AGENT

Now let me check the ShotListView to see how it connects to the click handler:

> AGENT

Now let me check the useShotNavigation hook to see how it navigates:

> AGENT

Now let me check the ShotEditorView to see how it handles the shot and generationMode:

> AGENT

Now let me check the VideoTravelSettingsProvider to understand how the generationMode is determined:

> AGENT

Now let me check the useShotSettings hook to see where generationMode gets loaded:

> AGENT

Let me continue reading this file and check the SortableShotItem:

> AGENT

Let me check the VideoShotDisplay component to see the click handler:

> AGENT

Perfect! Now let me check the useVideoTravelSettingsHandlers to see how generationMode is determined/changed:

> AGENT

Perfect! Now let me get the rest of that file and check the ShotEditorController to see how generationMode is used:

> AGENT

Now let me create a comprehensive summary document by checking the flow more carefully. Let me look at how the generationMode is displayed/used in the UI:

> AGENT

Perfect! Now I have a comprehensive understanding. Let me create the final report: ## Complete Flow: Clicking into a Shot in the Video Travel Tool Based on my thorough analysis of the codebase, here's the exact flow from shot list to editor with generationMode determination: --- ### **1. Shot List / Gallery Component** **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/VideoGallery/ShotListDisplay.tsx` - **Lines 38-144:** `ShotListDisplay` component renders the gallery grid - **Line 121:** Click handler `onSelectShot={() => onSelectShot(shot)}` on `SortableShotItem` **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/VideoGallery/VideoShotDisplay.tsx` - **Lines 231-234:** The actual click handler that triggers navigation ```typescript const handleClick = () => { if (isTempShot) return; onSelectShot(); }; ``` - **Line 250:** Attached via `onClick={handleClick}` on the card div --- ### **2. Shot Selection / Navigation Handler** **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/pages/ShotListView.tsx` - **Lines 224-227:** `handleShotSelect` callback ```typescript const handleShotSelect = useCallback((shot: Shot) => { setShowVideosViewRaw(false); navigateToShot(shot, { scrollToTop: false }); }, [setShowVideosViewRaw, navigateToShot]); ``` - **Line 350:** Passed to `ShotListDisplay` as `onSelectShot={handleShotSelect}` **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/hooks/shots/useShotNavigation.ts` - **Lines 82-105:** `navigateToShot` function that: - Sets `fromShotClick: true` in route state (line 96) - Passes `shotData: shot` for optimistic updates (line 97) - Navigates to the shot URL with hash (line 93: `travelShotUrl(shot.id)`) - Does NOT directly call `setCurrentShotId()` to avoid render jitter (comment at lines 85-92) --- ### **3. Page-Level Router (Resolution of Which View to Show)** **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/pages/VideoTravelToolPage.tsx` - **Lines 30-50:** Reads navigation state and extracts shot data: - `viaShotClick = location.state?.fromShotClick === true` (line 32) - `shotFromState = location.state?.shotData` (line 33) - `isNewlyCreatedShot = location.state?.isNewlyCreated === true` (line 34) - **Lines 79-87:** `useSelectedShotResolution` resolves which shot to edit: - Determines `shotToEdit` (the shot object to pass to editor) - Determines `shouldShowEditor` (boolean: show editor or list?) - **Lines 130-146:** Routes to correct view: - If `shouldShowEditor && shotToEdit`, renders `ShotEditorView` (line 63) - Otherwise renders `ShotListView` (line 84) --- ### **4. generationMode is Loaded (Before Editor Renders)** **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/hooks/settings/useShotSettings.ts` - **Lines 55-87:** `useShotSettings` hook loads settings from DB: - Calls `useAutoSaveSettings` with `shotId` (line 79) - Fetches from Supabase table `shots.settings` (referenced in `useAutoSaveSettings`) - Merges with inherited defaults for new shots (lines 59-76) - **Lines 178-227:** Settings persistence: - Loads shot-specific settings from DB - Includes `generationMode` field (defaults to 'timeline' if not found) **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/settings.ts` - **Line 83:** Type definition: `generationMode: 'batch' | 'by-pair' | 'timeline'` - **Line 178:** Default: `generationMode: 'timeline' as const` --- ### **5. Settings Provider Wraps Editor** **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/pages/ShotEditorView.tsx` - **Lines 209-247:** Wraps editor with `VideoTravelSettingsProvider`: ```typescript […]

> DEVELOPER

I need to deeply understand the settings data pipeline for shots in this app. There are two paths that fetch the same `shots.settings` column: **Path 1**: `useListShots` in `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/hooks/shots/useShotsQueries.ts` — does `select('*')` from shots table **Path 2**: `useShotSettings` → `useAutoSaveSettings` → `useToolSettings` — fetches shot settings separately I need to understand Path 2 in detail. Please trace through these files thoroughly: 1. `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/hooks/settings/useToolSettings.ts` — how does it fetch? What query key? What does it return? 2. `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/settings/hooks/useAutoSaveSettings.ts` — full file, how does it consume useToolSettings? How does it handle entity changes, loading, ready states? 3. `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/settings/hooks/autoSaveSettingsLoaders.ts` — the loader hooks 4. `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/hooks/settings/useShotSettings.ts` — how it wraps autoSaveSettings 5. `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/hooks/settings/inheritedDefaults.ts` or similar — the session inherited defaults logic For each file, report: - What it fetches from DB (table, columns, query key) - What transformations/normalizations it applies - What state it manages - What it returns - How it interacts with the layer above/below Also check: are there any other consumers of useToolSettings or useAutoSaveSettings across the codebase? How many tools use this pattern? Report file paths, line numbers, and key code snippets.

> AGENT

I'll trace through the settings data pipeline for shots systematically. Let me start by examining each file in the sequence you've provided.

> AGENT

Now let me look for the inheritedDefaults file and search for other consumers of these hooks:

> AGENT

Now let me read the inheritedDefaults file and look at a few other tool settings to understand usage patterns:

> AGENT

Now let me check how useListShots works with Path 1, and examine the settings fetching and normalization logic:

> DEVELOPER

I need to understand how shot data flows from `useListShots` through the app to the shot editor. The key question is: when you click a shot in the list, how does the shot object (including its `settings` column) get passed to the editor? Please trace through these files: 1. `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/hooks/shots/useShotsQueries.ts` — what does useListShots return? What's the React Query key? 2. `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/pages/ShotListView.tsx` — how is the shot passed to the click handler? 3. `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/hooks/shots/useShotNavigation.ts` — what does navigateToShot do with the shot data? 4. `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/pages/VideoTravelToolPage.tsx` — how is shotFromState extracted and used? 5. `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/hooks/settings/useSelectedShotResolution.ts` — how does it resolve shotToEdit? 6. `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/pages/ShotEditorView.tsx` — what does it pass to VideoTravelSettingsProvider? Also check: - What React Query keys does useListShots use vs what useToolSettings uses? Are they related at all? - Is the `shots` array from useListShots available in the editor context, or is it only the single `shotToEdit` object? - Does `shotToEdit.settings` contain the full raw settings JSON, or has it been stripped/transformed? Report file paths, line numbers, and key code snippets.

> AGENT

I'll trace through this shot data flow systematically. Let me start by reading these files in parallel.

> AGENT

Let me find the actual settings fetching implementation:

> AGENT

Now let me check what React Query keys are used in `useToolSettings` and how they compare to `useListShots`:

> AGENT

Let me find the useToolSettings definition:

> AGENT

Now let me check the queryKeys to compare:

> AGENT

Now let me check how many tools actually use these patterns and get a complete picture:

> AGENT

Now let me check the VideoTravelSettingsProvider to understand how it uses settings:

> AGENT

Perfect! Now let me look at the query keys and the debounced settings save to complete the picture:

> AGENT

Perfect. Now let me check the useShotSettings hook to understand how it resolves the shot settings:

> AGENT

Perfect. Now let me get the full picture by checking what travelShotUrl and how shots flow into the provider:

> AGENT

Excellent. Now let me check what the Shot type includes and verify the settings column:

> AGENT

Perfect! Now let me create a comprehensive summary document by tracing through the data flow diagram. Let me check one more critical piece - where shotFromState is passed to editor view:

> AGENT

Now let me check the VideoTravelContent component to see how shotToEdit is passed:

> AGENT

Perfect! Now let me create a comprehensive summary document. Let me gather a few more details about the autoSaveSettingsHelpers:

> AGENT

Excellent. Now I have all the pieces. Let me compile a comprehensive report of the shot data flow. ## Shot Data Flow: Complete Trace I've traced the shot data flow from list click to editor context. Here's the complete picture: ### 1. **useListShots** (Query Layer) **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/hooks/shots/useShotsQueries.ts` (lines 21-128) - **React Query Key:** `queryKeys.shots.list(projectId ?? '', maxImagesPerShot)` (line 28) - **Returns:** Array of `Shot` objects enriched with: - Spreads the raw shot row: `...shot` (line 115) - Adds `images`, `imageCount`, `positionedImageCount`, `unpositionedImageCount`, `hasUnpositionedImages` - **Includes `settings` column** directly from the database row (untransformed raw JSON) ### 2. **ShotListView Click Handler** **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/pages/ShotListView.tsx` (lines 224-232) ```typescript const handleShotSelect = useCallback((shot: Shot) => { const shotSettings = (shot.settings as Record<string, unknown>) ?? {}; console.log('[ModeDebug][ShotSelect] clicking into shot', shot.id, shot.name, { rawSettings: shot.settings, generationMode: (shotSettings?.['travel-between-images'] as Record<string, unknown>)?.generationMode ?? shotSettings?.generationMode ?? 'NOT SET', }); setShowVideosViewRaw(false); navigateToShot(shot, { scrollToTop: false }); }, [setShowVideosViewRaw, navigateToShot]); ``` - The entire `shot` object (with raw settings) is passed to `navigateToShot()` - Settings are accessed as `shot.settings` (raw JSON from DB) ### 3. **useShotNavigation - navigateToShot** **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/hooks/shots/useShotNavigation.ts` (lines 82-105) ```typescript const navigateToShot = useCallback((shot: Shot, options: ShotNavigationOptions = {}) => { const opts = { ...DEFAULT_OPTIONS, ...options }; const targetUrl = travelShotUrl(shot.id); // Hash-based URL: #shotId navigateRef.current(targetUrl, { state: { fromShotClick: true, shotData: shot, // FULL shot object passed in location.state isNewlyCreated: opts.isNewlyCreated }, replace: opts.replace, }); performScroll(opts); closeMobilePanes(opts, isMobileRef.current); }, []); ``` - **Navigation URL:** `#shotId` (hash-based, no query params) - **Navigation State:** `{ fromShotClick: true, shotData: shot, isNewlyCreated: false }` - The entire `shot` object with `settings` field is stored in location.state ### 4. **VideoTravelToolPage - Extract from State** **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/pages/VideoTravelToolPage.tsx` (lines 30-87) ```typescript const location = useLocation(); const viaShotClick = location.state?.fromShotClick === true; const shotFromState = location.state?.shotData; // Extracts shot with raw settings const isNewlyCreatedShot = location.state?.isNewlyCreated === true; // Later, passed to useSelectedShotResolution: const { selectedShot, shotToEdit, shouldShowEditor } = useSelectedShotResolution({ currentShotId, shots, shotFromState, // Passed here isNewlyCreatedShot, hashShotId, hashLoadingGrace, viaShotClick, }); ``` ### 5. **useSelectedShotResolution - Resolution Logic** **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/travel-between-images/hooks/settings/useSelectedShotResolution.ts` (lines 38-107) **shotToEdit resolution (lines 67-88):** ```typescript const shotToEdit = useMemo(() => { // Priority 1: Use shotFromState for newly created shots (not in cache yet) const shotFromStateMatches = shotFromState && ( shotFromState.id === currentShotId || shotFromState.id === hashShotId ); if (viaShotClick && shotFromStateMatches) { return shotFromState as Shot; // USES STATE VERSION (with raw settings) } // Priority 2: Use shot […]

> AGENT

Perfect! Now I have all the information needed. Let me create a comprehensive report. ## Settings Data Pipeline for Shots - Deep Analysis I've thoroughly traced the two paths for fetching shot settings. Here's the complete picture: --- ## **PATH 1: useListShots** **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/hooks/shots/useShotsQueries.ts` (lines 21-128) ### Fetch Pattern - **Query Key:** `queryKeys.shots.list(projectId, maxImagesPerShot)` - **Query:** `SELECT * FROM shots WHERE project_id = ? ORDER BY position` - **Returns:** Full shot objects including `shots.settings` column (JSONB) ### What It Returns The hook returns an array of enriched shot objects: ```typescript { ...shot, // Full shot row (including settings column) images, // Array of mapped GenerationRow objects imageCount, // Count of unique generation_ids positionedImageCount, unpositionedImageCount, hasUnpositionedImages } ``` ### Key Notes - `settings` is fetched as raw JSONB from DB but NOT parsed or extracted - Typically used for gallery/shot list views where full shot data is needed - Images are fetched separately in `shot_generations` to avoid N+1 queries - **Stale time:** 5 minutes --- ## **PATH 2: useToolSettings → useAutoSaveSettings → useShotSettings** This is a **three-layer abstraction** over the core settings fetching logic: ### **Layer 1: useToolSettings** (Low-level fetch + write) **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/hooks/settings/useToolSettings.ts` (lines 145-304) #### Query Pattern - **Query Key:** `queryKeys.settings.tool(toolId, projectId, shotId)` → `['toolSettings', toolId, projectId, shotId]` - **Fetch Strategy:** Cascade resolution (defaults → user → project → shot) - **Query FN:** Calls `fetchToolSettingsSupabase(toolId, { projectId, shotId }, signal)` - **Stale Time:** 10 minutes - **Retry:** 3 times, skips retry for auth_required / cancelled / network #### What It Fetches ```typescript // From toolSettingsService.ts / toolSettingsScopes.ts // THREE parallel queries: 1. SELECT settings FROM users WHERE id = userId // Scope: user 2. SELECT settings FROM projects WHERE id = projectId // Scope: project 3. SELECT settings FROM shots WHERE id = shotId // Scope: shot ``` #### Transformation & Return 1. **Cascade Merge:** `deepMerge({}, defaultSettings, userSettings, projectSettings, shotSettings)` 2. **Returns:** `SettingsFetchResult<T>` ```typescript { settings: T, // Merged, typed settings object hasShotSettings: boolean // Was shotSettings empty? (line 98 in toolSettingsScopes.ts) } ``` 3. **Extraction:** At query time (lines 216-218 in useToolSettings.ts): ```typescript const wrapper = isSettingsWrapper(queryResult); const settings = wrapper ? queryResult.settings : queryResult; const hasShotSettings = wrapper ? queryResult.hasShotSettings : false; ``` #### Write Flow - **Mutation:** `useMutation` on lines 226-275 - **Calls:** `updateToolSettingsSupabase({ scope, id, toolId, patch })` - **Queue:** Global settings write queue (debounced by default, can be immediate) - **RPC:** `update_tool_settings_atomic(p_table_name, p_id, p_tool_id, […]
