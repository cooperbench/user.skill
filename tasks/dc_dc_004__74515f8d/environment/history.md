> DEVELOPER

Implement the following plan:

# Plan: Trailing space stability during drag

## Context

When dragging an item to become the last in the timeline, two related bugs cause "jumpiness":

1. **Coordinate system jump on commit** — `fullMax` changes at drag-end because
   `trailingEffectiveEnd` (a floor computed from committed positions) grows when the last
   image moves right. On commit, everything rescales — a discrete pixel snap.

2. **Trailing slot appears mid-drag** — `shouldShowTrailingSlot` can flip from false→true
   mid-drag when the dragged item (which has a video) becomes the live-last image. The
   `TrailingEndpoint` handle and segment strip slot appear suddenly — a structural jump.

### Why the coordinate system jumps

`trailingEffectiveEnd = max(committed image frames) + trailingDefaultOffset` feeds into
`getTimelineDimensions` as a pending-frame floor. During drag this floor uses committed
(pre-drag) positions, so `rawDimensions.fullMax` stays fixed. At commit, `framePositions`
updates and the floor grows → `fullMax` grows → everything rescales.

Two sub-cases:

**Explicit endpoint** (`TRAILING_ENDPOINT_KEY` in `framePositions`): The endpoint already
provides `fullMax` directly. The floor is redundant AND harmful — it inflates `fullMax`
whenever `lastImageFrame + 17 > TRAILING_ENDPOINT_KEY`. Fix: skip the floor when
`TRAILING_ENDPOINT_KEY` exists.

**No explicit endpoint** (live trailing video only): The floor is the only source of trailing
space. When […]

> AGENT

Let me read both files to understand the current code before making changes.

> TOOL

tool_use Read
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTimelineOrchestrator.ts
```

> TOOL

tool_use Read
```json
reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> AGENT

I have a clear picture of both files. Let me make the three changes from the plan.

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTimelineOrchestrator.ts
```

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTimelineOrchestrator.ts
```

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> AGENT

Now let me verify with `tsc --noEmit`:

> TOOL

tool_use Bash
```json
npx tsc --noEmit 2>&1 | head -40
```

> TOOL

tool_use Bash
```json
npx tsc --noEmit 2>&1 | head -40
```

> AGENT

Zero type errors. All three changes are in:

1. **`useTimelineOrchestrator.ts` ~line 213** — Skip `trailingEffectiveEnd` floor when `TRAILING_ENDPOINT_KEY` exists in `framePositions`. This prevents the redundant floor from inflating `fullMax` and causing a coordinate-system snap on commit.

2. **`useTimelineOrchestrator.ts` ~line 287** — Extend frozen `fullMax` with `currentDragFrame + trailingDefaultOffset` during drag when there's no explicit endpoint but there is a trailing video. This makes the coordinate system grow monotonically during drag instead of snapping on commit.

3. **`TimelineContainer.tsx` ~line 312** — Freeze `shouldShowTrailingSlot` at drag start using a ref. Prevents the trailing endpoint handle and segment strip slot from appearing/disappearing mid-drag when the live-last image changes.

> DEVELOPER

The trailing segments, the kind of empty trailing segment thing doesn't show until you actually let go of what you're dragging That is when you have the trailing segment thing activated.

> AGENT

Let me check how `imagePositions` is computed — it feeds the trailing segment rendering.

> TOOL

tool_use Read
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTrailingEndpoint.ts
```

> AGENT

I see the issue. During drag, `imagePositions` uses live drag positions. When the live-last image moves past the committed trailing endpoint, the trailing segment gets a negative duration and disappears. Let me check how the strip renders the trailing segment to confirm.

> TOOL

tool_use Grep
```json
pattern=trailingSegmentMode path=reigh/src/tools/travel-between-images/components/Timeline/SegmentOutputStrip.tsx
```

> TOOL

tool_use Read
```json
reigh/src/tools/travel-between-images/components/Timeline/SegmentOutputStrip.tsx
```

> TOOL

tool_use Grep
```json
pattern=trailingSegmentMode path=reigh/src/tools/travel-between-images/components/Timeline/hooks/useSegmentOutputStrip.ts
```

> AGENT

Let me look at the exact JSX section I need to modify.

> TOOL

tool_use Read
```json
reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> TOOL

tool_use Read
```json
reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> AGENT

Got it. The problem is that during drag, `imagePositions` (live) can cause the live-last image frame to exceed the committed `trailingEndFrame`, producing a negative-duration segment that renders as nothing. The fix is to freeze the `trailingSegmentMode` data during drag, same pattern as `shouldShowTrailingSlot`.

Two edits in `TimelineContainer.tsx`:

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> AGENT

Now replace the inline computation with the frozen value:

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> TOOL

tool_use Bash
```json
npx tsc --noEmit 2>&1 | head -20
```

> AGENT

Zero type errors. Here's the fix:

The `trailingSegmentMode` data passed to `SegmentOutputStrip` was computed from live `imagePositions` during drag. When the live-last image's frame exceeded the committed `trailingEndFrame`, the segment got a negative duration and rendered as nothing (zero width).

I extracted the computation into a `useMemo` in the component body and applied the same ref-based freeze pattern used for `shouldShowTrailingSlot` — update the ref only when not dragging, use the frozen value during drag. This keeps the trailing segment strip stable at its pre-drag position/size throughout the entire drag.

> DEVELOPER

Okay, there's a few strange things happening, especially with the empty space one or with them in general. It feels like there is, you know, when I grab the trailing space one and move it to the previous space, it leaves like a gap between the final video on the trailing space. The trailing space one jumps out really far to the right. You know beyond the end of it. Like it feels like the calculation is wrong. And when I move the trailing space one to the right it overlaps with when I moved the last one to the right it overlaps with the trailing space. It feels like we're getting some kind of calculations wrong here or maybe they're overcomplicated Can you check to understand if they can be simplified? Or what's going on here? Or if it's difficult to understand because of some structural issue for example

> AGENT

Let me dig into the trailing space coordinate system code thoroughly to understand what's going on.

> TOOL

tool_use Task
```json
I need to understand the trailing space / trailing endpoint coordinate system in this timeline component. There are bugs where:
1. Moving the last image left leaves a gap between the final video and trailing space
2. The trailing space jumps far to the right beyond the end
3. Moving the last image r
```

> AGENT

The analysis is clear. The core problem: the `trailingSegmentModeRef` freeze I added uses frozen frame values (committed positions from drag start) but they get rendered with the live `fullRange` — producing gaps, overlaps, and jumps. The freeze was solving one problem (disappearing segment) but creating three worse ones.

The fix: remove the freeze entirely, compute `trailingSegmentMode` live, and make it endpoint-drag-aware so the strip follows the handle in real time.

> TOOL

tool_use Read
```json
reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> TOOL

tool_use Grep
```json
pattern=frozenTrailingSegmentMode path=reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> AGENT

Good, two spots. Now replace the frozen computation with a live, endpoint-drag-aware one:

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> AGENT

Now update the JSX reference:

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> AGENT

Now clean up the unused `useRef` import if it's no longer needed — let me check if `useRef` is still used elsewhere in this file:

> TOOL

tool_use Grep
```json
pattern=useRef path=reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> AGENT

Good, `useRef` is still used by the `shouldShowTrailingSlot` freeze. Now type-check:

> TOOL

tool_use Bash
```json
npx tsc --noEmit 2>&1 | head -20
```

> AGENT

Zero errors. Let me verify the final state of both changed files is coherent:

> TOOL

tool_use Read
```json
reigh/src/tools/travel-between-images/components/Timeline/TimelineContainer/TimelineContainer.tsx
```

> AGENT

Here's what changed and why:

**What was wrong:** The `trailingSegmentModeRef` freeze captured frame positions at drag start but those frozen frames were rendered with the live `fullRange` coordinate system. This mismatch caused:
- **Gap** when dragging the last image left (frozen `imageFrame=50` rendered at 62% while the live image was at 50%)
- **Overlap** when dragging the last image right (frozen duration=17 frames but live gap was only 7)  
- **Jump** on endpoint drag (handle moved live but strip stayed at frozen pre-drag position)

**The fix:** Removed the ref-based freeze entirely. `trailingSegmentMode` is now computed live from `imagePositions` (which already tracks drag-preview positions). Two key improvements:

1. **Endpoint-drag-aware** — during endpoint drag, uses `endpointDragFrame` (live handle position) instead of committed `trailingEndFrame`, so the strip follows the handle in real time
2. **Graceful negative-duration handling** — if an image is dragged past the endpoint (`liveEndFrame <= imageFrame`), returns `undefined` instead of producing a negative-width segment

What's still frozen (and working correctly): `shouldShowTrailingSlot` visibility flag — prevents the trailing slot container from appearing/disappearing mid-drag.