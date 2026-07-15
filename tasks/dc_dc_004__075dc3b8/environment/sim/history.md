[DEVELOPER]: Implement the following plan: # Plan: Trailing space stability during drag ## Context When dragging an item to become the last in the timeline, two related bugs cause "jumpiness": 1. **Coordinate system jump on commit** — `fullMax` changes at drag-end because `trailingEffectiveEnd` (a floor computed from committed positions) grows when the last image moves right. On commit, everything rescales — a discrete pixel snap. 2. **Trailing slot appears mid-drag** — `shouldShowTrailingSlot` can flip from false→true mid-drag when the dragged item (which has a video) becomes the live-last image. The `TrailingEndpoint` handle and segment strip slot appear suddenly — a structural jump. ### Why the coordinate system jumps `trailingEffectiveEnd = max(committed image frames) + trailingDefaultOffset` feeds into `getTimelineDimensions` as a pending-frame floor. During drag this floor uses committed (pre-drag) positions, so `rawDimensions.fullMax` stays fixed. At commit, `framePositions` updates and the floor grows → `fullMax` grows → everything rescales. Two sub-cases: **Explicit endpoint** (`TRAILING_ENDPOINT_KEY` in `framePositions`): The endpoint already provides `fullMax` directly. The floor is redundant AND harmful — it inflates `fullMax` whenever `lastImageFrame + 17 > TRAILING_ENDPOINT_KEY`. Fix: skip the floor when `TRAILING_ENDPOINT_KEY` exists. **No explicit endpoint** (live trailing video only): The floor is the only source of trailing space. When […]

[AGENT]: Let me read both files to understand the current code before making changes.

[AGENT]: I have a clear picture of both files. Let me make the three changes from the plan.

[AGENT]: Now let me verify with `tsc --noEmit`:

[AGENT]: Zero type errors. All three changes are in: 1. **`useTimelineOrchestrator.ts` ~line 213** — Skip `trailingEffectiveEnd` floor when `TRAILING_ENDPOINT_KEY` exists in `framePositions`. This prevents the redundant floor from inflating `fullMax` and causing a coordinate-system snap on commit. 2. **`useTimelineOrchestrator.ts` ~line 287** — Extend frozen `fullMax` with `currentDragFrame + trailingDefaultOffset` during drag when there's no explicit endpoint but there is a trailing video. This makes the coordinate system grow monotonically during drag instead of snapping on commit. 3. **`TimelineContainer.tsx` ~line 312** — Freeze `shouldShowTrailingSlot` at drag start using a ref. Prevents the trailing endpoint handle and segment strip slot from appearing/disappearing mid-drag when the live-last image changes.

[DEVELOPER]: The trailing segments, the kind of empty trailing segment thing doesn't show until you actually let go of what you're dragging That is when you have the trailing segment thing activated.

[AGENT]: Let me check how `imagePositions` is computed — it feeds the trailing segment rendering.

[AGENT]: I see the issue. During drag, `imagePositions` uses live drag positions. When the live-last image moves past the committed trailing endpoint, the trailing segment gets a negative duration and disappears. Let me check how the strip renders the trailing segment to confirm.

[AGENT]: Let me look at the exact JSX section I need to modify.

[AGENT]: Got it. The problem is that during drag, `imagePositions` (live) can cause the live-last image frame to exceed the committed `trailingEndFrame`, producing a negative-duration segment that renders as nothing. The fix is to freeze the `trailingSegmentMode` data during drag, same pattern as `shouldShowTrailingSlot`. Two edits in `TimelineContainer.tsx`:

[AGENT]: Now replace the inline computation with the frozen value:

[AGENT]: Zero type errors. Here's the fix: The `trailingSegmentMode` data passed to `SegmentOutputStrip` was computed from live `imagePositions` during drag. When the live-last image's frame exceeded the committed `trailingEndFrame`, the segment got a negative duration and rendered as nothing (zero width). I extracted the computation into a `useMemo` in the component body and applied the same ref-based freeze pattern used for `shouldShowTrailingSlot` — update the ref only when not dragging, use the frozen value during drag. This keeps the trailing segment strip stable at its pre-drag position/size throughout the entire drag.