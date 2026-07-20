> DEVELOPER

Implement the following plan:

# Plan: Timeline Positioning Cleanup

## Context

After auditing the full timeline positioning pipeline, three dead-code/memoization issues were
found. The most impactful: `pairInfo` is computed bare (no `useMemo`) in `useComputedTimelineData`,
allocating a new array every render. During drag this fires every animation frame, cascades into
`pairInfoWithPending` in `TimelineContainer`, and causes `SegmentOutputStrip` + the pair region
render loop to see new prop references every frame.

The other two are pure dead code: `calculateFinalPosition` is an identity function left from
removed snapping logic, and `shotId` is passed into `useComputedTimelineData` and immediately
voided.

Not in scope: `imageOnlyPositions` triple-computation (all memoized, actual cost trivial),
`forceUpdate` zoom hack (valid workaround for stale `containerWidth` after layout),
`dynamicPositions()` call-per-render (drag positions must update every frame — unavoidable).

---

## Changes — 2 files primary, 1 call site

### `useComputedTimelineData.ts`

**1. Memoize `pairInfo`** (line 32):
```ts
// Before:
const pairInfo = getPairInfo(currentPositions);

// After:
const pairInfo = useMemo(() => getPairInfo(currentPositions), [currentPositions]);
```

**2. Remove dead `shotId` param** — 3 locations in this file:
- Interface line 10: delete `shotId: string;`
- Destructure line 26: remove `shotId: _shotId,`
- Line 31: remove `void _shotId;`

---

### `useTimelineDrag.ts`

**3. Delete `calculateFinalPosition`** (lines 135–137) entirely — it […]

> AGENT

I'll read all three files in parallel first.

> TOOL

tool_use Read
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useComputedTimelineData.ts
```

> TOOL

tool_use Read
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTimelineDrag.ts
```

> TOOL

tool_use Read
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTimelineOrchestrator.ts
```

> AGENT

All three files read. Making all edits now — changes are independent so I'll do them in parallel.

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useComputedTimelineData.ts
```

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useComputedTimelineData.ts
```

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useComputedTimelineData.ts
```

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTimelineDrag.ts
```

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTimelineDrag.ts
```

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTimelineDrag.ts
```

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTimelineDrag.ts
```

> TOOL

tool_use Edit
```json
reigh/src/tools/travel-between-images/components/Timeline/hooks/useTimelineOrchestrator.ts
```

> AGENT

All edits applied. Now let me run verification — type check and grep checks in parallel.

> TOOL

tool_use Bash
```json
npx tsc --noEmit 2>&1 | head -30
```

> TOOL

tool_use Grep
```json
pattern=calculateFinalPosition path=reigh/src
```

> TOOL

tool_use Grep
```json
pattern=shotId path=reigh/src/tools/travel-between-images/components/Timeline/hooks/useComputedTimelineData.ts
```

> AGENT

All three checks pass:

1. `npx tsc --noEmit` — zero errors
2. `calculateFinalPosition` in `src/` — zero results (fully removed)
3. `shotId` in `useComputedTimelineData.ts` — zero results (fully removed)

**Summary of changes:**

- **`useComputedTimelineData.ts`** — Memoized `pairInfo` with `useMemo` (was bare computation, allocating a new array every render/drag frame), removed dead `shotId` parameter
- **`useTimelineDrag.ts`** — Deleted identity function `calculateFinalPosition`, inlined its two call sites to use `targetFrame`/`calculateTargetFrame` directly, removed from dep array
- **`useTimelineOrchestrator.ts`** — Removed `shotId` from `useComputedTimelineData` call site