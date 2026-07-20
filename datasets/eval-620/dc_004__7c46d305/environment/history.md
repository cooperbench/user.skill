> DEVELOPER

Implement the following plan:

# Plan: Fix drag-swap preview and drop-zone alignment

## Context

Two linked bugs when dragging an image from position 1 (frame 0) rightward:

1. **Swap partner doesn't move during drag.** The item originally at position 2 doesn't move
   to frame 0 until drop.
2. **Dragged item renders far right of the drop-zone indicator.** The pair-region gap
   indicator stays at frame 0 while the thumbnail follows the cursor.

Both bugs have a single root cause in `useTimelineDrag.ts`.

---

## Root Cause

`calculateDragPositions` (single-item path, line 221) calls:

```ts
return applyFluidTimeline(newPositions, dragState.activeId, finalPosition, undefined, …);
```

`excludeId` is `undefined`, so `shrinkOversizedGaps` includes the dragged item in its
sort-then-normalize pass. Its invariant: **"first sorted item always at frame 0"**. The
dragged item starts at frame 0, sorts first for the entire rightward drag, and gets forced
straight back to 0 — cancelling its motion in `currentPositions`.

Consequences:
- `currentPositions.get(draggedItem) = 0` throughout drag → pair region stuck at frame 0
- Swap partner barely moves because gap recalculation is based on positions that haven't changed
- Dragged thumbnail uses independent `originalPixel + dragOffset.x` cursor path → it follows
  the cursor correctly → divergence = full drag distance ("far to […]

> TOOL

tool_use Read
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTimelineDrag.ts
```

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTimelineDrag.ts
```

> AGENT

Now let me verify with `tsc`:

> TOOL

tool_use Bash
```json
npx tsc --noEmit 2>&1 | head -20
```

> AGENT

Zero type errors. The fix is in — passing `dragState.activeId` as the `excludeId` parameter so `shrinkOversizedGaps` excludes the dragged item from its sort-then-normalize pass. This means:

1. **Swap partner moves immediately**: remaining items get normalized with the leftmost snapped to frame 0
2. **Drop-zone indicator tracks the thumbnail**: the dragged item keeps its target frame position throughout the drag