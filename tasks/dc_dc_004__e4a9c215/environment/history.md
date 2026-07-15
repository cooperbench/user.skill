> DEVELOPER

Implement the following plan: # Plan: Unify drag-stability mechanisms with `useDragStable` ## Context The timeline currently has three separate ad-hoc mechanisms for "hold a stable value during drag, update it when drag ends": | Location | Mechanism | Purpose | |---|---|---| | `useTimelineOrchestrator` | `dragStartDimensionsRef` + `useEffect` | Freeze/grow `fullMin`/`fullMax` so pixel positions don't jump | | `TimelineContainer` | `shouldShowTrailingSlotRef` inline render-phase write | Freeze trailing slot visibility so it doesn't flash | | `useEndpointDrag` | writes to `dragStartDimensionsRef` on mousedown/mouseup | Communication channel to keep orchestrator dimensions frozen | All three are instances of the same pattern: **"snapshot a value at the start of drag, hold it (or merge it monotonically) during drag, release it when drag ends."** They should share one implementation. Additionally, `dragStartDimensionsRef` in `useEndpointDrag` is redundant: the mousemove handler reads `dragStartDimensionsRef.current?.fullMin ?? fullMin` — but `fullMin` in the closure IS the same value the ref was written with on mousedown. The ref is pure overhead. ### The unified abstraction ```ts // useDragStable<T>(live, isDragging, merge?) → T // - When not dragging: return live (and update snapshot) // - When dragging: return merge(snapshot, live) [default merge = identity = pure freeze] ``` `merge = Math.max` → monotonic […]

> AGENT

Let me read the key files first.

> AGENT

I have all the context I need. Let me implement the four changes.

> AGENT

Now update `useTimelineOrchestrator.ts` — remove `dragStartDimensionsRef`, the `useEffect` for dimension freezing, the `if (isDraggingAnything && ...)` block, and replace with `useDragStable`:

> AGENT

Remove `dragStartDimensionsRef`:

> AGENT

Now replace the `useEffect` block + the `isDraggingAnything` dimension freeze with `useDragStable`:

> AGENT

Now remove `dragStartDimensionsRef` from the `useEndpointDrag` call site:

> AGENT

Now update `useEndpointDrag.ts` — remove `dragStartDimensionsRef` from interface, props, and body:

> AGENT

Remove the `dragStartDimensionsRef` write on mousedown and replace the frozen reads in the mousemove handler:

> AGENT

Remove `dragStartDimensionsRef.current = null` on mouseup:

> AGENT

Remove `dragStartDimensionsRef` from the `useCallback` deps:

> AGENT

Now update `TimelineContainer.tsx` — replace the `shouldShowTrailingSlotRef` inline code with `useDragStable`:

> AGENT

Now let me verify `useRef` isn't used elsewhere in TimelineContainer after removing it from the import:

> AGENT

Good, `useRef` is no longer used in that file. Now let's type-check:

> AGENT

Zero type errors. Let me do a quick sanity check on the final state of all four files:

> AGENT

Everything looks clean. Let me also verify `fullMax` isn't used before it's declared (since we removed `let fullMax` and now have `const fullMax` via `useDragStable`, but `useTimelineDrag` takes `fullMax` from `rawDimensions`):

> AGENT

Good — `useTimelineDrag` still gets `rawDimensions.fullMin/fullMax/fullRange` (the raw values), and the stabilized `fullMin/fullMax/fullRange` are computed after it. This is correct: the drag hook works in raw coordinate space, and the orchestrator exposes the stabilized values to the rest of the UI. Here's a summary of what was done: **New file: `useDragStable.ts`** — A 19-line generic hook that snapshots a value when drag starts and optionally merges it monotonically during drag. Three modes: - `merge = Math.max` → monotonic growth (for `fullMax`) - `merge = Math.min` → monotonic shrink (for `fullMin`) - No merge → strict freeze (for `shouldShowTrailingSlot`) **`useTimelineOrchestrator.ts`** — Removed: - `dragStartDimensionsRef` ref - The `useEffect` that snapshotted dimensions on drag start (one-render-lag issue) - The `if (isDraggingAnything && dragStartDimensionsRef.current)` block - `dragStartDimensionsRef` from the `useEndpointDrag` call Replaced with two `useDragStable` calls (render-phase, zero lag) plus a `trailingExtendedMax` computation that factors in the trailing preview extent. **`useEndpointDrag.ts`** — Removed `dragStartDimensionsRef` from interface, destructuring, mousedown write, mouseup clear, mousemove reads, and deps array. The `frozenFullMin`/`frozenFullRange` reads were replaced with direct closure values (`fullMin`/`fullRange`), which are identical since the ref was just a redundant copy of the closure captures. **`TimelineContainer.tsx`** — Replaced the 6-line `shouldShowTrailingSlotRef` inline pattern with a single `useDragStable` […]