[DEVELOPER]: Implement the following plan: # Plan: Timeline Positioning Cleanup ## Context After auditing the full timeline positioning pipeline, three dead-code/memoization issues were found. The most impactful: `pairInfo` is computed bare (no `useMemo`) in `useComputedTimelineData`, allocating a new array every render. During drag this fires every animation frame, cascades into `pairInfoWithPending` in `TimelineContainer`, and causes `SegmentOutputStrip` + the pair region render loop to see new prop references every frame. The other two are pure dead code: `calculateFinalPosition` is an identity function left from removed snapping logic, and `shotId` is passed into `useComputedTimelineData` and immediately voided. Not in scope: `imageOnlyPositions` triple-computation (all memoized, actual cost trivial), `forceUpdate` zoom hack (valid workaround for stale `containerWidth` after layout), `dynamicPositions()` call-per-render (drag positions must update every frame — unavoidable). --- ## Changes — 2 files primary, 1 call site ### `useComputedTimelineData.ts` **1. Memoize `pairInfo`** (line 32): ```ts // Before: const pairInfo = getPairInfo(currentPositions); // After: const pairInfo = useMemo(() => getPairInfo(currentPositions), [currentPositions]); ``` **2. Remove dead `shotId` param** — 3 locations in this file: - Interface line 10: delete `shotId: string;` - Destructure line 26: remove `shotId: _shotId,` - Line 31: remove `void _shotId;` --- ### `useTimelineDrag.ts` **3. Delete `calculateFinalPosition`** (lines 135–137) entirely — it […]

[AGENT]: I'll read all three files in parallel first.

[AGENT]: All three files read. Making all edits now — changes are independent so I'll do them in parallel.

[AGENT]: All edits applied. Now let me run verification — type check and grep checks in parallel.

[AGENT]: All three checks pass: 1. `npx tsc --noEmit` — zero errors 2. `calculateFinalPosition` in `src/` — zero results (fully removed) 3. `shotId` in `useComputedTimelineData.ts` — zero results (fully removed) **Summary of changes:** - **`useComputedTimelineData.ts`** — Memoized `pairInfo` with `useMemo` (was bare computation, allocating a new array every render/drag frame), removed dead `shotId` parameter - **`useTimelineDrag.ts`** — Deleted identity function `calculateFinalPosition`, inlined its two call sites to use `targetFrame`/`calculateTargetFrame` directly, removed from dep array - **`useTimelineOrchestrator.ts`** — Removed `shotId` from `useComputedTimelineData` call site

[DEVELOPER]: Is it now holistically beautifully?

[AGENT]: Yes — clean removal of dead code (`calculateFinalPosition`, `shotId` passthrough) and the `pairInfo` memoization plugs the one real perf leak in the drag pipeline. Three files touched, net lines deleted, zero new abstractions. Looks good.

[DEVELOPER]: push this to github

[AGENT]: Lots of other unstaged changes in the working tree. I'll stage only the three files from this plan and commit.

[AGENT]: Pushed to `main` as `3e10b49d`.

[DEVELOPER]: Can you see, um, on the following, um, shot that I'm showing now? Um- b19f23ad-f3ed-415c-ba0d-fe2d7a65f0fa It has an image at position zero that has a video associated with it then it has one at position one that has no video and then it has one at the final position that has a video again but the one at the very first position the video isn't showing for some reason can you try to understand why that could be and the interesting thing is that if I move the one, the final image back to position two then the video reappears again but I'm gonna leave it broken just so you can see what the data looks like can you look inside try to understand what's happening

[AGENT]: Let me investigate the data and rendering logic for this shot.

[AGENT]: Good data. The DB shows 3 videos at pair 0 (variants) and 1 video with `pair_shot_generation_id` pointing to the **last** image (frame 38). Let me dig into the slot-matching logic to understand why pair 0's video disappears.

[AGENT]: I can see the slot-matching logic. Let me check the actual child generation params to see if `segment_index` is present — that's how `isSegment()` filters at line 368.

[AGENT]: Found the critical clue. The child generations under the parent (`d516fd93`) show: | child | child_order | pair_shot_gen | segment_index | join_index | |-------|-------------|---------------|---------------|------------| | `6d9c2971` | 0 | `f63be396` (frame 0) | **null** | **0** | | `3e936942` | 0 | `f63be396` (frame 0) | **null** | **0** | | `14825655` | 0 | `f63be396` (frame 0) | **0** | null | | `ae174702` | 1 | `e40e428c` (frame 38) | **1** | null | The `isSegment` filter at line 368 checks `typeof params?.segment_index === 'number'`. Two of the three pair-0 children have `join_index` instead of `segment_index` — those get filtered out. But `14825655` does have `segment_index=0`, so it should survive. Let me dig deeper into the display pipeline.

[AGENT]: I don't think you need to move it — I can see the data in its broken state. Let me check one more thing: I need to verify how the parent generation is found (the `shot_final_videos` view) and the exact flow from `useShotImagesEditorModel` to the strip.

[AGENT]: Good — the view has `OR EXISTS (SELECT 1 FROM generations c WHERE c.parent_generation_id = g.id)`, so the parent `d516fd93` IS found (it has children). The parent selection is fine. Let me look at the rendering layer now — specifically how `TimelineContainer` passes data to `SegmentOutputStrip` and whether `trailingSegmentMode` or `shouldShowTrailingSlot` affects things.

[AGENT]: I've traced through the entire slot-matching and rendering pipeline and on paper everything should work — the pair 0 video (14825655) maps to slot 0 correctly. But something at runtime must be different from what I'm calculating. Let me add targeted instrumentation to see exactly what's happening.

[AGENT]: I've traced the entire pipeline on paper and everything should work — but something at runtime must differ. Let me add targeted debug logging so we can see exactly what's happening.

[AGENT]: Now add a log in `buildDisplaySlots`:

[AGENT]: And one in the positioned slots output:

[AGENT]: Now open the browser console, navigate to that shot, and look for `[SegSlotDebug]` logs. They'll show: 1. **inputs** — the segments that survived `isSegment` filter, position maps, slot count 2. **slotAssignment** — which children got assigned to which slots, and which were orphaned 3. **buildDisplaySlots** — the remapping from raw slots via live positions to display indices 4. **displaySlots** — the final slots that get rendered Can you check the console and paste the `[SegSlotDebug]` output? That'll instantly reveal where the pair 0 video drops out of the pipeline.