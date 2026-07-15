> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

Review the implementation against the success criteria.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace/reigh-app

        Idea:
# Selection / Coordination Architecture Refactor

## Background

Over a long session of bug-chasing in the selection / agent-chat surface area, the user has repeatedly hit related-but-distinct bugs that all root in the same architectural choice: **the current code exposes low-level state mutations (`selectTimelineClip(id, opts, { clearGallery })`, raw context bridges, racy global modifier state) when the domain operates at a higher level (`user clicked timeline → clear gallery; agent chat replaced attachments → preserve gallery`)**.

A Codex 5.5 architectural review confirmed this read and proposed three concrete pieces of refactoring. This megaplan executes those three pieces (#1, #2, #3 from the Codex proposal). Piece #4 (PostgREST filter helper) is OUT OF SCOPE for this run.

## What we've already point-fixed in the current session (DO NOT REVERT)

These are uncommitted changes in the working tree on branch `megaplan/m1b-m1c-stores`. Build on top of them; do not undo.

- `src/shared/state/selectionStore.ts` — `useTimelineMultiSelect` wrapper (lines ~803-820) now passes `syncOptions` through instead of hardcoding `clearGallery: false`. Default behavior matches the underlying store (clear gallery on timeline selection).
- `src/tools/video-editor/contexts/VideoEditorProvider.tsx` — `AgentChatBridgeRegistration.stableReplace` now passes `{ clearGallery: false }` explicitly to preserve gallery on agent-chat-driven attachment edits. Effect deps now include `timelineClips` (the previous getter pattern was broken).
- `src/tools/video-editor/components/AgentChat/AgentChat.tsx` — added a `displayedClips` 150ms-grace-window state to absorb the bridge's one-commit lag (the flicker fix). Added a "Clear" button next to the attachment summary when `clips.length > 1`.
- `src/shared/components/MediaGalleryItem.tsx` — added `handleWrapperPointerDown`/`handleWrapperPointerUp` for desktop click detection with an 8px movement threshold (HTML5 drag preempts native click).
- `src/shared/components/MediaGalleryItem/components/{ImageContent,VideoContent}.tsx` — removed `onClick` from inner img/video elements (now handled by wrapper).
- `src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts` — `onImageClick` signature now accepts `(image, modifiers?: { multiSelect: boolean })`; mobile touch path forwards modifiers from the event.
- `src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx` — `handleImageClick` reads modifiers from the event-derived `modifiers` arg, with a fallback to `useModifierKeys` (the racy hook is still imported but no longer authoritative).
- `src/integrations/supabase/bootstrap/fetchWithTimeout.ts` — added a 4xx response-body logger that probes HEAD requests with a follow-up GET to extract the diagnostic body.

These point-fixes work but are band-aids on top of the structural issues this megaplan addresses. The refactor should make several of them redundant (the `displayedClips` grace window, the `useModifierKeys` fallback, the manual remove-from-both-surfaces logic in AgentChat).

## Target architecture (three pieces)

### Piece 1: Intent-based selection facade

**File:** add `src/shared/state/selectionActions.ts` OR fold into `src/shared/state/selectionStore.ts` as a new export section. Whichever keeps the diff smaller and more navigable.

**Replace the public selection API.** Today the public API exposes:
- `selectTimelineClip(id, opts, syncOptions)` (with `clearGallery` flag)
- `selectTimelineClips(clipIds, syncOptions)`
- `selectGalleryItem(id, meta, options)` (with `toggle` flag)
- `selectGalleryItems(items, options)` (with `append` flag)
- `clearGallerySelection()`
- `clearTimelineSelection(syncOptions)`
- `deselectGalleryItems(ids)`

**With named-by-intent commands** that encode WHO is acting (user, composer, system, editor):

- `userSelectGalleryItem(item, opts: { additive: boolean })` — user clicked a gallery item. Replaces selection unless additive. Does NOT touch timeline selection.
- `userSelectGalleryItems(items, opts: { additive: boolean })` — marquee/lasso in gallery.
- `userSelectTimelineClip(clipId, opts: { additive, preserveIfSelected? })` — user clicked a clip in the timeline. **Clears gallery selection** (the policy that was scattered as `clearGallery: true` defaults).
- `userSelectTimelineClips(clipIds, opts: { additive })` — marquee in timeline. **Clears gallery selection**.
- `userClearAllSelection()` — explicit "clear everything" intent.
- `composerRemoveAttachment(match: { url, mediaType, generationId? })` — agent chat removed a chip. Removes from BOTH surfaces (one match identifier, the composer figures out which surface(s) to update). **Does NOT clear other selections.**
- `composerClearAttachments()` — agent chat "Clear" button. Clears both surfaces. (User intent is explicit clear.)
- `editorReplaceTimelineSelection(clipIds)` — editor-internal mutation (e.g., select after paste/duplicate). **Preserves gallery.**
- `systemPruneTimelineSelection(validIds)` — drops selected clip ids that are no longer in the timeline data (after a clip is deleted, etc.). **Preserves gallery.**

**Keep the existing low-level reducers** (`selectTimelineClip`, `selectTimelineClips`, `selectGalleryItem`, etc.) but **make them private to the store module** — not exported, or marked internal in a way the rest of the codebase can't reach. The intent commands are the only public surface.

**Migrate every call site** that currently uses the low-level API to call the appropriate intent command. Rough mapping:
- `useClipDrag.helpers.ts` calls of `selectClip`/`selectClips` → `userSelectTimelineClip`/`userSelectTimelineClips` (drag interactions are user-initiated).
- `useMarqueeSelect.ts:203` → `userSelectTimelineClips` (additive: false, since marquee replaces).
- `TimelineEditor.tsx:427` → `userSelectTimelineClip`.
- `PreviewPanel.tsx:138` → `userSelectTimelineClip`.
- `VideoEditorShell.tsx:147` (selectAllClips) → `editorReplaceTimelineSelection` (system-initiated keyboard shortcut, should NOT clear gallery).
- `VideoEditorProvider.tsx:90` (`stableReplace` for agent chat bridge) → `editorReplaceTimelineSelection`.
- `GenerationsPaneGallery.tsx:99` (handleImageClick) → `userSelectGalleryItem`.
- `GenerationsPaneGallery.tsx:88,144` → similar.
- `useLassoSelection`'s `onSelectItems` consumer → `userSelectGalleryItems`.

**Remove `clearGallery` from the public surface.** It's a leaked implementation detail.

**Do NOT rewrite the underlying Zustand reducers.** Keep them. The intent layer is the new public API, the reducers stay internal.

Codex estimate: 250-450 LOC, 4-8 files touched.

### Piece 2: Single current-attachment composer + sync bridge

**Files:**
- Add `src/shared/state/currentAttachmentSet.ts` (the composer).
- Modify `src/shared/contexts/AgentChatContext.tsx` (the bridge becomes thinner — see below).
- Modify `src/tools/video-editor/contexts/VideoEditorProvider.tsx` (registration becomes a Zustand write, not a context push).
- Modify `src/tools/video-editor/components/AgentChat/AgentChat.tsx` (consumes the composer, drops the manual merge + the `displayedClips` grace window).

**Move the merge/dedupe logic out of AgentChatPanel.** Today `AgentChat.tsx:181` does `mergeSelectedClips(timelineClips, selectedGalleryClips)` inside the panel. Move `mergeSelectedClips` (currently at `AgentChat.tsx:40`) into `currentAttachmentSet.ts`. The panel should call ONE hook: `useCurrentAttachmentSet()` that returns the merged `clips` and `summary`.

**Replace the React-context bridge for timeline attachments with a synchronous Zustand write.** The current bridge pattern is:

```
useSelectedMediaClips → register({ timelineClips }) → useState setOverride → context value → consumer re-render
```

That's an async hop (one React commit late) and is the cause of the flicker even after my point-fix. Replace with:

```
useSelectedMediaClips → set timelineAttachments slice in Zustand → useCurrentAttachmentSet subscribes synchronously
```

Specifically: add a `timelineAttachments` slice (or similar) to the existing Zustand selection store (or a new store) that holds the structured timeline clip data the chat panel needs. `VideoEditorProvider` writes to it on every change of `useSelectedMediaClips()` via a `useEffect` that calls a setter, but consumers READ it via a Zustand selector — no more React-context useState bridge for this data.

**Remove the `displayedClips` 150ms grace window from AgentChatPanel.** Once timeline attachments propagate synchronously, the flicker is impossible by construction and the band-aid is unnecessary. Delete it.

**Keep the bridge for non-attachment data.** `AgentChatContext` still has `timelineId`, the actions registry (markEngaged/toggleRecording/focusComposer), and `replaceSelectedTimelineClips` (which becomes a thin wrapper calling `composerRemoveAttachment`/`editorReplaceTimelineSelection`). Don't delete the bridge entirely — just stop using it for the data that flickers.

**`AgentChatPanel.handleRemoveAttachment` becomes a one-liner.** Today it manually edits both `timelineClips` (via `replaceSelectedTimelineClips`) and gallery (via `deselectGalleryMatches`). Replace with `composerRemoveAttachment(match)` — the composer/intent layer handles both surfaces.

Codex estimate: 300-600 LOC, 5-10 files touched.

### Piece 3: Shared gesture primitives

**File:** add `src/shared/interactions/selectionGesture.ts` (or `src/shared/lib/interactions/selectionGesture.ts` — pick whichever fits the existing layout).

**Functions to export:**
- `isAdditiveSelectionEvent(event: { metaKey, ctrlKey, shiftKey })` — returns true if Cmd/Ctrl/Shift held. Read from event, NOT from React state. (Already exists inline in `useLassoSelection.ts:37` — promote it.)
- `isPrimaryPointer(event: PointerEvent | MouseEvent)` — returns true if `event.button === 0` (left click).
- `isClickLikePointerGesture(start: { x, y }, end: { x, y }, threshold = 8)` — returns true if movement under threshold (the wrapper-level click detection logic from `MediaGalleryItem.tsx`).
- Optionally a hook `usePointerClickIntent({ onClick, threshold })` that wraps the pointerdown/pointerup pattern with movement tracking, but only if the call sites collapse cleanly. Don't force it.

**Migrate call sites:**
- `useModifierKeys.ts` — **DELETE the file entirely.** Update `GenerationsPaneGallery.tsx` to drop the import and the `useModifierKeys()` fallback (now unnecessary since the click handler reads from event). Update `ImageGenerationToolPage.tsx` to use `isAdditiveSelectionEvent` from the new module instead.
- `useLassoSelection.ts:37,140` — replace inline `isMultiSelectEvent` with the shared `isAdditiveSelectionEvent`.
- `MediaGalleryItem.tsx` — replace inline `CLICK_THRESHOLD_PX` and the pointerdown/up dance with `isClickLikePointerGesture` (or `usePointerClickIntent` if it lands well).
- `useItemInteraction.ts` — same — its inline modifier-derivation can use `isAdditiveSelectionEvent`.

**Keep the gesture primitives small and stateless.** No framework. Just functions and (at most) one hook. They should compose with existing event handlers, not replace them.

Codex estimate: 150-300 LOC, 4-6 files touched.

## Out of scope (do not do in this run)

- **Do NOT rewrite the underlying Zustand reducers.** They're fine. We're changing only the public API.
- **Do NOT decouple AgentChatPanel from `@/tools/video-editor/hooks/...` imports.** That's a separate, larger refactor. The panel staying coupled to video-editor for now is acceptable.
- **Do NOT touch the PostgREST `or=` accumulator.** That's Codex's piece #4. We can fold that helper into a follow-up. The current implementation in `useProjectGenerations.ts:71` is correct, just not extracted yet.
- **Do NOT touch the WIP code on this branch** outside the selection/coordination surface: drop-to-generation, local media resolver, generations storage migration, video-editor effect compilation, etc. These are independent and not yours to fix.
- **Do NOT touch the 3 pre-existing test failures**: `GenerationsPane.test.tsx:209` (drop-to-generation) and `dropdown-menu.test.tsx` × 2. They've failed since the WIP commit `be3c5e21` and are tracked separately.
- **Do NOT change visual styling**, the action-pane layout, or the agent chat panel's UX. The user has been polishing those by hand. Leave the UI behavior unchanged.

## Constraints

- **Working tree is dirty** with the point-fixes listed above. Keep them. Build the refactor on top of the current state. Don't commit anything during execution — leave changes uncommitted in the working tree for the user to review.
- **Branch:** `megaplan/m1b-m1c-stores`. Don't rebase, don't push.
- **Tests must continue to pass** at the same rate or better. The 3 pre-existing failures stay; everything else must stay green.
- **Type-check must pass.** `npx tsc --noEmit` clean.
- **Lint must pass on touched files.**

## Validation

- `npx tsc --noEmit` — clean.
- `npx eslint <touched files>` — clean.
- `npx vitest run` — same set passing as before plus any new tests added by this refactor. The 3 pre-existing failures (`GenerationsPane.test.tsx:209`, `dropdown-menu.test.tsx` × 2) remain known failures.
- **Add new tests for the intent layer.** Each `userSelect*` / `composer*` / `editor*` / `system*` command should have a unit test asserting cross-surface behavior (specifically: which surfaces it updates, which it preserves).
- **Add a regression test for the flicker.** A test that simulates "gallery selected → click timeline → check that the chat's clips collection never goes through an empty state in any render." Probably needs `useSyncExternalStore` mocking or careful render-counting.
- **Manual smoke: confirm the existing UX is unchanged.** Cmd+click in gallery still multi-selects. Click on timeline still clears gallery. Marquee in gallery still works. Drag-to-shot still works. Agent chat attachment removal still works on `/tools/video-editor` AND on `/shots`/`/art` routes (where the bridge is null).

## Notes for the planner

- This codebase uses Vite + React 18 + Zustand + React Router v6 + shadcn UI + Tailwind v3.
- The existing structural-cleanup megaplan (`structural-cleanup-of-the-20260426-0209`) committed on this branch as `06ac9dde8` + `95d94b780` — it set the stage by partially formalizing the timeline selection API. This megaplan is the natural follow-up to that one.
- The codex review identified bugs 1-6 the user has been hitting and grouped them into three families (gesture/input, selection composition, query helper). This megaplan addresses families 1 and 2.
- See `CLAUDE.md` at the repo root for project-wide rules. Especially relevant: "Required-provider hooks must throw when their context is missing" and "every change should make the codebase smaller or more explicit."
- The user has confirmed: do not commit anything during execution.

User notes and answers:
- USER DECISIONS for gate iter 4 contract questions (delegated approval):

Q1 (FG-002 matcher): Option B — chip-specific. Use (generationId, url, mediaType) as the primary match key with the existing fallbacks (clipId for timeline-side, (url, mediaType) when generationId is absent). Preserves current handleRemoveAttachment behavior; do NOT use generationId-only matching, which would regress multi-variant generations.

Q2 (FG-003 additive semantics): Option A — additive: true means TOGGLE. Cmd+click on an already-selected clip toggles it OFF. Preserves current useClipDrag/Cmd+click UX. Naming-cleanliness concerns about additive-vs-toggle conflation are deferred to a follow-up; do not introduce a separate toggle flag in this refactor.

Q3 (FG-016 bootstrap empty render): Option B — impossible-by-construction. clipDataById must expose placeholder entries for selected-but-unknown clipIds (using only the selection-side data the store already has), so useCurrentAttachmentSet() is never transiently empty during any selection transition. The brief explicitly says 'Remove the displayedClips 150ms grace window — flicker is impossible by construction'; that invariant must hold. Acceptable to log/dev-warn if a placeholder is rendered for >1 frame, so we know if the editor data sync is slow, but the visible attachment chip must not flicker.

Proceed with revise iter 5 incorporating these decisions.
- USER DECISIONS for gate iter 6 escalation (delegated approval — second round):

Issue 1 (FLAG-021 env guard, trivial): Use `import.meta.env.DEV` — matches the repo convention everywhere else. Mechanical fix.

Issue 2 (FLAG-019 / FG-001 / FG-003, merge-key, 5-6 iters): Option 2b — single key `isPlaceholder ? clipId : url`. Preserves the placeholder-collision fix from iter 6 AND restores the cross-surface URL dedupe that iter 6 broke. Functionally equivalent to 2a's two-pass merge but simpler code. Reject 2c (drop URL dedupe) — that would regress UX by showing same-URL gallery+timeline items as duplicate chips, which is the kind of silent behavior change we explicitly rejected on the previous escalation's Q1.

Issue 3 (FLAG-020 / FG-002 useSelectionStore facade, 7 iters): Option 3a — colocate `useCurrentAttachmentSet` inside `selectionStore.ts`, keep `useSelectionStore` private (un-export it again). The brief explicitly allows this: 'Add src/shared/state/currentAttachmentSet.ts OR fold into selectionStore.ts as a new export section. Whichever keeps the diff smaller and more navigable.' Iter-5 SD-005 already chose colocation for the intent layer; the composer naturally lives in the same module. Reject 3b (typed ReadonlyState selector — adds an abstraction layer the brief doesn't ask for) and 3c (accept the leak — contradicts the facade goal).

Proceed with revise iter 7 incorporating these decisions. The gate should converge after this round; if iter-7 critique surfaces new flags or score regresses again, escalate again.

        Approved plan:

# Implementation Plan: Selection / Coordination Architecture Refactor (revised)

## Overview
Three-piece refactor of the selection / agent-chat coordination layer on branch `megaplan/m1b-m1c-stores`. Iteration 6 closes the three remaining placeholder-design gaps from iter 5 — none change architecture, all close concrete code-level details:

1. **`mergeSelectedClips` merge key**: change from `clip.url` to `clip.clipId || clip.url` so multiple selected-but-unknown clipIds (whose placeholders all share `url: ''`) don't collapse into a single chip when the data eventually arrives.
2. **Export `useSelectionStore`** narrowly from `selectionStore.ts` so `currentAttachmentSet.ts` can subscribe via the Zustand selector pattern. Cleanest option that matches SD-005's colocation philosophy without inflating selectionStore.ts further.
3. **Name the actual chip render surface**: chip rendering lives in `src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx:180-226` (which exports `AgentChatAttachmentStrip`). Step 9 references the right file/component; Step 14 adds `AgentChatMessage.test.tsx` to the test-update list.

Settled decisions from iter 2-5 are preserved (see `settled_decisions` history). The three user TIEBREAKER decisions from iter 4 (chip-specific matcher, additive=toggle for single-clip, placeholders to make empty-render impossible) are pinned.

The repo is Vite + React 18 + Zustand + Vitest. Constraints: working tree stays dirty; no commits; 3 documented pre-existing test failures remain.

## Phase 1: Intent-Based Selection Facade (Piece 1)

### Step 1: Re-audit reducer call sites with fresh ripgrep — exhaustive list (locked)
**Scope:** Small
1. Hook-API consumers, direct reducer/multi-select callers, and test files all enumerated in iter 4-5 (locked from iter 4). No additions in iter 6 beyond `AgentChatMessage.tsx` (already in Step 9 by component name; iter 6 names the file path explicitly).

### Step 2: Fold the intent layer into `selectionStore.ts` with finalized contracts
**Scope:** Medium
1. Intent layer in `selectionStore.ts`; `compute*` helpers extracted from reducer bodies; adds `computeTimelineRemove` for the toggle-off path.
2. Export the FULL intent command set (18 commands) plus clip-data mutators. Doc comments make `additive=true means TOGGLE for single-clip / APPEND for marquee` explicit.
3. **Export `useSelectionStore`** (line 694) from `selectionStore.ts`. The hook is currently `function useSelectionStore<T>(...)` without `export`; add the keyword. This unblocks `currentAttachmentSet.ts` subscribing to store state via the Zustand selector pattern. The export is intentionally narrow — it returns whatever the selector requests, and the existing state-only hooks (`useGallerySelection`, `useTimelineSelectionStore`) remain the preferred public surface for component code.
4. No `clearGallery` flag anywhere on the public surface.
5. Add `__getSelectionStateForTests()` test-only export.

### Step 3: Migrate timeline / editor / system call sites
**Scope:** Medium
Mappings finalized in iter 4-5 (locked):
- Drag full coverage including `useClipDrag.ts:449,459,461,463` direct calls.
- Marquee: `useMarqueeSelect.ts:201-211` → `userSelectTimelineClips(ids, { additive })` (additive=append, never toggle).
- Timeline editor click handlers, Cmd+A, agent-chat bridge, editor commit hook, timeline state hook, app provider — all per iter-5 plan.
- `useTimelineCommit.ts` drops `useSelectionStoreApi`; uses editor-* intents.

### Step 4: Migrate gallery / composer call sites
**Scope:** Small
Mappings locked from iter 4-5: `GenerationsPaneGallery.tsx`, `ImageGenerationToolPage.tsx`, `useGallerySelectionBridge.ts` migrate to user-* / system-* intents. AgentChat composer migrations deferred to Phase 2 Step 9.

### Step 5: Privatize the public surface (after Steps 3-4 finish)
**Scope:** Small
1. Strip mutations from `useGallerySelection()` and `useTimelineSelectionStore()`.
2. Delete `useSelectionStoreApi()`.
3. Trim `useTimelineMultiSelect()`: drop mutation methods + `clearGallery` option.
4. Migrate `useLastAffectedShot.test.ts:12,24` to renderHook + `__getSelectionStateForTests()`.
5. Run `rg` for each removed surface name; confirm zero external callers.
6. Run `rg "clearGallery" src/` — no hits in any exported type/signature outside `selectionStore.ts`.

### Step 6: Unit-test the intent layer (`src/shared/state/selectionActions.test.ts`)
**Scope:** Small
1. Cover every command (18 total). Specifically: `userSelectGalleryItem`/`userSelectGalleryItems` preserve timeline; `userSelectTimelineClips({ additive: true })` clears gallery + APPENDS (never toggles); `userSelectTimelineClip({ additive: true })` toggles (two-call test); `userSelectTimelineClip({ additive: false, preserveIfSelected: true })` is no-op when already selected; editor-* preserve gallery; system-* per their contracts.

## Phase 2: Synchronous Attachment Composer (Piece 2)

### Step 7: Add `clipDataById` slice + composer with finalized matcher, placeholders, and merge-key fix (`selectionStore.ts`, `currentAttachmentSet.ts`)
**Scope:** Medium
1. **Add `clipDataById` slice** to `selectionStore.ts` — `ReadonlyMap<string, SelectedMediaClip>`, keyed by `clipId`. Mutators: `setTimelineClipData(entries)` and `clearTimelineClipData()`.
2. **`composerRemoveAttachment`** with the chip-specific matcher (URL+mediaType always required; generationId and clipId narrow further). Implementation per iter-5 plan.
3. **`composerClearAttachments`** — single `setState` clearing gallery + timeline.
4. **Create `src/shared/state/currentAttachmentSet.ts`** with the corrected merge key and read-time placeholders:
   ```ts
   import { useSelectionStore } from './selectionStore';
   import { shallow } from 'zustand/shallow';
   import { buildSummary, type SelectedMediaClip } from '@/tools/video-editor/hooks/useSelectedMediaClips';

   /** Synthesized at read time for selected clipIds without clipDataById data. */
   function makePlaceholderClip(clipId: string): SelectedMediaClip & { isPlaceholder: true } {
     return {
       clipId,
       assetKey: '',
       url: '',
       mediaType: 'image',
       isTimelineBacked: true,
       isPlaceholder: true,
     };
   }

   /**
    * Merges timeline + gallery attachments and dedupes by `clipId || url`.
    *
    * Critical change from the legacy AgentChat.tsx version: the dedupe key is
    * now `clipId || url` rather than `url`. This preserves the original
    * dedupe behavior for timeline clips that share a URL with a gallery item
    * (collapsed into one chip), AND fixes the placeholder-collision bug where
    * multiple unknown clipIds — all carrying url: '' — would otherwise collapse
    * into a single chip and cause a visible chip-count jump when real data
    * arrives.
    */
   export function mergeSelectedClips(
     timelineClips: SelectedMediaClip[],
     galleryClips: SelectedMediaClip[],
   ): SelectedMediaClip[] {
     const clipsByKey = new Map<string, SelectedMediaClip>();
     for (const clip of [...timelineClips, ...galleryClips]) {
       const key = clip.clipId || clip.url;       // <-- merge key fix
       const existing = clipsByKey.get(key);
       if (existing) {
         // Merge precedence: prefer entries with generationId (richer metadata).
         const preferIncoming = !existing.generationId && Boolean(clip.generationId);
         const preferred = preferIncoming ? clip : existing;
         const secondary = preferIncoming ? existing : clip;
         clipsByKey.set(key, {
           ...preferred,
           generationId: preferred.generationId ?? secondary.generationId,
           variantId: preferred.variantId ?? secondary.variantId,
           isTimelineBacked: preferred.isTimelineBacked || secondary.isTimelineBacked,
           shotId: preferred.shotId ?? secondary.shotId,
           shotName: preferred.shotName ?? secondary.shotName,
           shotSelectionClipCount: preferred.shotSelectionClipCount ?? secondary.shotSelectionClipCount,
           trackId: preferred.trackId ?? secondary.trackId,
           at: preferred.at ?? secondary.at,
           duration: preferred.duration ?? secondary.duration,
           [REDACTED] || secondary.assetKey,
         });
         continue;
       }
       clipsByKey.set(key, clip);
     }
     return Array.from(clipsByKey.values());
   }

   export function useCurrentAttachmentSet() {
     return useSelectionStore((state) => {
       const timelineAttachments: SelectedMediaClip[] = [];
       let placeholdersEmitted = 0;
       state.timeline.selectedClipIds.forEach((clipId) => {
         const data = state.clipDataById.get(clipId);
         if (data) {
           timelineAttachments.push(data);
         } else {
           timelineAttachments.push(makePlaceholderClip(clipId));
           placeholdersEmitted += 1;
         }
       });
       if (placeholdersEmitted > 0 && process.env.NODE_ENV !== 'production') {
         console.warn(
           `[currentAttachmentSet] ${placeholdersEmitted} placeholder(s) rendered — `
           + `clipDataById has not yet caught up with selectedClipIds. `
           + `If this persists past one frame, useTimelineClipsForAttachments may be slow.`,
         );
       }
       const merged = mergeSelectedClips(timelineAttachments, state.gallery.selectedGalleryClips);
       return { clips: merged, summary: buildSummary(merged) };
     }, shallow);
   }
   ```
   Notes:
   - `mergeSelectedClips` is colocated with `useCurrentAttachmentSet` here (not in AgentChat.tsx anymore).
   - Each placeholder gets a unique merge key (the clipId), so two unknown clipIds produce two distinct chip slots — the original "impossible by construction" invariant is preserved across single-select AND multi-select cases.
5. **Add `isPlaceholder?: boolean`** to the `SelectedMediaClip` type in `useSelectedMediaClips.ts` (or a sibling extension type the panel consumes).
6. **Unit tests** for `composerRemoveAttachment` (chip-specific paths) — locked from iter 5: 6 paths covered.
7. **Unit tests** for `useCurrentAttachmentSet` placeholder behavior, including the new merge-key fix:
   - **(a)** Single selected clipId with no data → returns one placeholder clip with `isPlaceholder: true` and `clips.length === 1`.
   - **(b)** Two selected clipIds (`clipA`, `clipB`) with no data → returns TWO distinct placeholder clips (`clips.length === 2`, distinct clipIds), NOT one collapsed chip. **This test directly verifies the merge-key fix.**
   - **(c)** dev-warn fires when at least one placeholder is emitted.
   - **(d)** After `setTimelineClipData([clipAData])` runs for clipA → next render has the real clip; clipB still placeholder; clips.length still 2.
   - **(e)** After `setTimelineClipData([clipAData, clipBData])` runs for both → next render has both real clips; no placeholders; no dev-warn.
   - **(f)** Mixed gallery + timeline: gallery=[G with url='https://...']; timeline selectedClipIds={clipX} where clipX has same url as G. Asserts dedupe works (one merged entry with generationId from gallery). Verifies the URL-fallback path of the merge key for gallery items lacking clipId.

### Step 8: Replace context bridge for timeline attachments (`VideoEditorProvider.tsx`, `AgentChatContext.tsx`)
**Scope:** Medium
1. Add `useTimelineClipsForAttachments()` in `src/tools/video-editor/hooks/` returning all timeline clips' attachment data (not selection-derived).
2. Modify `AgentChatBridgeRegistration` in `VideoEditorProvider.tsx:77-111`: drop `useSelectedMediaClips()` for the bridge; add `const allClips = useTimelineClipsForAttachments();` + `useEffect(() => { setTimelineClipData(allClips); return () => clearTimelineClipData(); }, [allClips]);`. Slim `register({ timelineId })`. Drop `stableReplace`/`replaceSelectedTimelineClips`.
3. Modify `AgentChatContext.tsx`: reduce to `{ timelineId: string | null }`; delete `timelineClips`/`replaceSelectedTimelineClips`. Keep actions registry.

### Step 9: Refactor AgentChat panel + AgentChatMessage chip render surface (`AgentChat.tsx`, `AgentChatMessage.tsx`)
**Scope:** Medium
1. **`AgentChat.tsx`** — Delete `mergeSelectedClips` (now in `currentAttachmentSet.ts`), the `displayedClips` 150ms grace window, `deselectGalleryMatches`. Replace clip computation with `const { clips, summary } = useCurrentAttachmentSet();`.
2. **`AgentChat.tsx`** — Reduce `handleRemoveAttachment` to a one-line `composerRemoveAttachment({ url, mediaType, generationId, clipId })`. `handleRemoveShot` iterates `composerRemoveAttachment`. The `clearGallerySelection()` calls at lines 497, 812 → `composerClearAttachments()`. The "Clear" button → `composerClearAttachments()`. `useAgentChatBridge()` returns only `{ timelineId }`.
3. **`AgentChatMessage.tsx:180-226`** (the `AgentChatAttachmentStrip` component, where chip rendering actually happens):
   - Currently `<img src={attachment.url}>` / `<video src={attachment.url}>` always render the media; remove button always shows when `onRemoveAttachment` is set.
   - Change: when `attachment.isPlaceholder === true`, render a CHIP SLOT (same width/height as a real chip — reserves the visual space) with a loading state (spinner / muted bg / "Loading…" label) and DO NOT render the `<img>`/`<video>` src binding (avoids broken-image flash from `url: ''`).
   - Hide the X (remove) button on placeholder chips. The chip stays visible until `setTimelineClipData` provides real data, at which point the placeholder is replaced and the X button reappears.
   - Pass `isPlaceholder` through the `AgentChatAttachmentPreviewItem` type that the strip consumes (extend the type as needed).

### Step 10: Regression tests for the flicker (`src/shared/state/currentAttachmentSet.test.tsx`)
**Scope:** Small
1. **Test 1 (steady-state baseline)**: setTimelineClipData first; gallery=G; userSelectTimelineClip('A', {additive: false}). Asserts clips.length ≥ 1 across all renders; final render has real data; no dev-warn.
2. **Test 2 (additive marquee)**: setTimelineClipData([A, B]); gallery=G; userSelectTimelineClips([A, B], {additive: true}). Asserts gallery cleared + attachments contain {A, B} as real data in same render.
3. **Test 3 (single-clip placeholder fills the gap)**: gallery=G; userSelectTimelineClip('clipA', {additive: false}) BEFORE any setTimelineClipData. Asserts clips.length ≥ 1 across ALL renders; one render contains a clip with `isPlaceholder: true` and `clipId === 'clipA'`; dev-warn fires. Then setTimelineClipData([clipAData]) and assert real data.
4. **Test 4 (additive-toggle for single-clip)**: dispatch userSelectTimelineClip('A', {additive: true}) once → A added; dispatch again → A removed.
5. **Test 5 (NEW — multi-placeholder merge-key fix)**: gallery=[]; dispatch `userSelectTimelineClip('clipA', {additive: false})`, then `userSelectTimelineClip('clipB', {additive: true})` (toggle-additive ADDS clipB), all BEFORE any setTimelineClipData. Asserts clips.length === 2 across the renders containing both selections (NOT collapsed to 1). Asserts each placeholder has its distinct clipId. After `setTimelineClipData([clipAData])`, asserts clips.length still === 2 (clipA real + clipB placeholder). After `setTimelineClipData([clipAData, clipBData])`, asserts clips.length === 2, both real.
6. **Note in test file header**: "Test 5 specifically locks the `mergeSelectedClips` merge-key contract: dedupe is by `clipId || url`. Without the fix, multiple placeholders (all url: '') would collapse and the visible chip count would jump when real data arrives."

## Phase 3: Shared Gesture Primitives (Piece 3)

### Step 11: Create `selectionGesture.ts` (`src/shared/lib/interactions/`)
**Scope:** Small
1. `isAdditiveSelectionEvent`, `isPrimaryPointer`, `isClickLikePointerGesture`. Add unit tests.

### Step 12: Migrate gesture call sites
**Scope:** Small
Locked from iter 5: `useLassoSelection`, `MediaGalleryItem`, `useItemInteraction`, `ImageGenerationToolPage`, `GenerationsPaneGallery`.

### Step 13: Delete `useModifierKeys.ts` + its test
**Scope:** Small
Verify zero importers; delete hook + test; update `GenerationsPaneGallery.test.tsx` mocks.

## Phase 4: Test Infrastructure & Validation

### Step 14: Update existing tests to match the new public surface
**Scope:** Medium
1. **`AgentChat.test.tsx:145-146`** — drop mutation mocks; `vi.mock('@/shared/state/selectionStore', ...)` for composer intents.
2. **`AgentChatMessage.test.tsx`** — **NEW** in iter 6. Add component-level tests for the placeholder rendering contract:
   - When `attachment.isPlaceholder === true`, the rendered chip:
     - Shows the loading state (spinner / muted styling / "Loading…" label).
     - Does NOT render `<img src="">` or `<video src="">` (no broken-image flash).
     - Does NOT show the remove (X) button even when `onRemoveAttachment` is provided.
   - When `attachment.isPlaceholder` is undefined or `false`, the chip renders normally (`<img src={attachment.url}>` and the X button if `onRemoveAttachment` is provided).
   - The chip slot reserves the same horizontal/vertical space as a real chip (verifies the strip layout doesn't shrink).
3. **`VideoEditorProvider.test.tsx:64-65,270,288,410`** — replace bridge-field assertions with `__getSelectionStateForTests()` reads. Replace the line-410 `clearGallery` plumbing test with `editorReplaceTimelineSelection` coverage. Mock `useTimelineClipsForAttachments`.
4. **`AppProviders.test.tsx:91-99`** — drop the `bridge.timelineClips.length` rendering at line 96 and its data-testid; keep the `agent-chat-timeline-id` assertion.
5. **`GenerationsPaneGallery.test.tsx`** — every mock block drops mutation mocks; `vi.mock` for user-* gallery intents. Update assertions.
6. **`useLastAffectedShot.test.ts:12,24`** — migrated in Step 5.4.
7. **Other selection-store consumer tests** — run vitest first; migrate destructuring tests via intent-call or `vi.mock`. Spot-check files listed in iter-4 plan.

### Step 15: Targeted verification
**Scope:** Small
1. `npx vitest run src/shared/state/ src/shared/lib/interactions/` first.
2. `npx vitest run src/tools/video-editor/components/AgentChat/ src/tools/video-editor/contexts/ src/app/providers/`.
3. `npx vitest run src/features/gallery/`.
4. `npx tsc --noEmit`.
5. `npx eslint` on touched files.
6. Full `npx vitest run` — only the 3 documented pre-existing failures remain.
7. Self-review: pre-existing point-fixes preserved or replaced; no commits created.

## Execution Order
1. **Phase 1.** Step 2 additive (now also exports `useSelectionStore`). Steps 3-4 migrate every consumer. Step 5 (privatize + trim hook) last.
2. **Phase 2.** Step 7 (slice + composer + merge-key fix + placeholder reader) → 8 (bridge) → 9 (AgentChat.tsx + AgentChatMessage.tsx placeholder rendering) → 10 (tests including multi-placeholder Test 5).
3. **Phase 3.** After Phase 2.
4. **Phase 4.** Targeted then global. AgentChatMessage.test.tsx is part of Step 14.

## Validation Order
1. `selectionActions.test.ts` (Phase 1 — every intent's contract; toggle-off behavior).
2. `currentAttachmentSet.test.tsx` — Test 1 (steady-state), Test 2 (additive marquee), Test 3 (single placeholder), Test 4 (additive-toggle), Test 5 (multi-placeholder merge-key fix).
3. `AgentChatMessage.test.tsx` (placeholder chip rendering).
4. `selectionGesture.test.ts`.
5. `tsc --noEmit`.
6. Full `vitest run`.
7. `eslint` on touched files.


        Execution tracking state (`finalize.json`):
        {
  "baseline_test_command": "pytest --tb=no -q --no-header",
  "baseline_test_failures": [],
  "baseline_test_note": "3 pre-existing failures are documented as known and must remain (do not attempt to fix). Everything else must stay green; new tests added by this refactor must pass.",
  "meta_commentary": "CRITICAL CONSTRAINTS (read first):\n1. Working tree is dirty on branch `megaplan/m1b-m1c-stores` with the iter-0 point-fixes that this refactor builds on. DO NOT REVERT them. DO NOT COMMIT during execution. Leave changes uncommitted for the user to review.\n2. The 3 pre-existing test failures (GenerationsPane.test.tsx:209, dropdown-menu.test.tsx \u00d72) are tracked separately \u2014 do not try to fix them.\n3. Do not touch out-of-scope WIP: drop-to-generation, local media resolver, generations storage migration, video-editor effect compilation, PostgREST or= helper.\n\nKEY DESIGN DECISIONS (locked by user, do not relitigate):\n- composerRemoveAttachment matcher is CHIP-SPECIFIC: url+mediaType ALWAYS required; generationId narrows further; clipId narrows timeline-side. Sibling variants from same generationId with different URLs MUST be preserved.\n- userSelectTimelineClip({additive: true}) = TOGGLE (single-clip Cmd+click). userSelectTimelineClips({additive: true}) (marquee) = APPEND-ONLY, never toggles.\n- mergeSelectedClips merge key is `clip.clipId || clip.url` (NOT just url). Every selectedClipId without clipDataById data emits a placeholder entry (isPlaceholder: true) at READ time so the chip count never drops to zero NOR collapses.\n- Use `import.meta.env.DEV` for the dev-warn guard (Vite convention). Do NOT use `process.env.NODE_ENV` \u2014 would throw ReferenceError in browser bundle.\n- useSelectionStore is narrowly exported (NEW in iter 6) so currentAttachmentSet.ts can subscribe via Zustand selector. State-only convenience hooks (useGallerySelection, useTimelineSelectionStore) remain the preferred public surface for components.\n\nEXECUTION ORDER:\n- Phase 1 (T1-T5) before Phase 2 (T6-T9). T4 (privatize) must come AFTER T2/T3 finish migrating consumers.\n- Phase 3 (T10-T12) after Phase 2.\n- Phase 4 (T13-T14) last.\n\nGOTCHAS:\n- AgentChat.tsx:497 and 812 currently call clearGallerySelection() \u2014 verify they map to composerClearAttachments() during T3.\n- useTimelineMultiSelect: drop selectClip/selectClips/addToSelection/clearSelection mutation methods AND the {clearGallery?: boolean} option entirely.\n- useLastAffectedShot.test.ts:12,24 must migrate from useSelectionStoreApi to renderHook + __getSelectionStateForTests().\n- AgentChatMessage.tsx:180-226 is the AgentChatAttachmentStrip \u2014 placeholder chips must NOT bind src to empty url (avoids broken-image flash) and must HIDE the X button.\n- Step 7's `useTimelineClipsForAttachments()` returns ALL timeline clips' attachment data (not selection-derived) \u2014 populated separately from selection so useCurrentAttachmentSet() is synchronously consistent.\n- AgentChat bridge keeps {timelineId} + actions registry \u2014 only the timelineClips/replaceSelectedTimelineClips fields are removed.\n\nVALIDATION TARGETS:\n- npx tsc --noEmit clean\n- npx eslint clean on touched files\n- npx vitest run: same passing set + new tests; only the 3 pre-existing failures remain\n- rg \"useSelectionStoreApi\" src/ \u2192 no hits\n- rg \"clearGallery\" src/ \u2192 no hits in any exported type/signature outside selectionStore.ts",
  "tasks": [
    {
      "id": "T1",
      "description": "Fold the intent layer into src/shared/state/selectionStore.ts. (a) Add the FULL 18-command intent set: userSelectGalleryItem, userSelectGalleryItems, userSelectTimelineClip, userSelectTimelineClips, userClearAllSelection, composerRemoveAttachment, composerClearAttachments, editorReplaceTimelineSelection, editorSelectTimelineClip, editorClearTimelineSelection, editorSetSelectedTrackId, systemPruneTimelineSelection, systemResetTimelineSelection, systemResetSelectionForProjectChange, systemSyncGallerySelection, systemClearGallerySelection (plus composerRemoveAttachment, composerClearAttachments = 18 total). Encode contracts directly via setState writes: userSelectGalleryItem(s) NEVER touches timeline; userSelectTimelineClip({additive:true}) TOGGLES (single clip) and ALWAYS clears gallery; userSelectTimelineClips({additive:true}) (marquee) APPENDS only and ALWAYS clears gallery; userSelectTimelineClip({additive:false, preserveIfSelected:true}) is a no-op when already selected; editor-* preserve gallery; system-* per their contracts. Extract compute* helpers (computeTimelineRemove etc.) from the existing reducer bodies. (b) Add the clipDataById slice: ReadonlyMap<string, SelectedMediaClip>, plus mutators setTimelineClipData(entries) and clearTimelineClipData(). (c) Add `export` keyword to the existing useSelectionStore<T>(...) hook (around line 694) \u2014 narrow export so currentAttachmentSet.ts can subscribe. (d) Add a __getSelectionStateForTests() test-only export that returns the current state snapshot. KEEP the underlying low-level reducers in place \u2014 they remain internal. Do NOT remove them yet \u2014 Step 5 (T4) handles removal/privatization after migrations finish. Doc-comment the additive=TOGGLE-vs-APPEND distinction explicitly on userSelectTimelineClip and userSelectTimelineClips.",
      "depends_on": [],
      "status": "done",
      "executor_notes": "Added intent facade exports in selectionStore.ts: user/composer/editor/system selection commands, clipDataById state, setTimelineClipData(), clearTimelineClipData(), exported useSelectionStore(), and __getSelectionStateForTests(). Timeline single additive is documented and implemented as TOGGLE; timeline marquee additive is documented and implemented as APPEND. Existing low-level reducers remain in place and share extracted timeline compute helpers. Verified with `npx tsc --noEmit` and touched-file ESLint.",
      "files_changed": [
        "src/shared/state/selectionStore.ts"
      ],
      "commands_run": [
        "npx eslint src/shared/state/selectionStore.ts src/shared/lib/interactions/selectionGesture.ts src/shared/lib/interactions/selectionGesture.test.ts",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T2",
      "description": "Migrate every timeline/editor/system reducer call site to the new intent commands (locked from iter 4-5). Targets: useClipDrag.ts:449,459,461,463 (direct selectClip/selectClips calls \u2014 map each line to userSelectTimelineClip with appropriate {additive, preserveIfSelected} per the documented drag contract); useClipDrag helpers (drag interactions); useMarqueeSelect.ts:201-211 \u2192 userSelectTimelineClips(ids, {additive}) with additive=append (never toggle); TimelineEditor.tsx:427 \u2192 userSelectTimelineClip; PreviewPanel.tsx:138 \u2192 userSelectTimelineClip; VideoEditorShell.tsx:147 (selectAllClips) \u2192 editorReplaceTimelineSelection (preserves gallery); VideoEditorProvider.tsx:90 (stableReplace agent-chat bridge) \u2192 editorReplaceTimelineSelection; useTimelineCommit.ts:111,116-120 \u2192 editorSelectTimelineClip / editorClearTimelineSelection / editorSetSelectedTrackId (drop useSelectionStoreApi import); useTimelineState.ts:511,519-520 \u2192 systemResetTimelineSelection on timeline-id change (drop mutation method destructuring); AppProviders.tsx:42,64 \u2192 systemResetSelectionForProjectChange (drop useSelectionStoreApi import). Additionally verify AgentChat.tsx:497 and 812 clearGallerySelection() calls map to composerClearAttachments().",
      "depends_on": [
        "T1"
      ],
      "status": "done",
      "executor_notes": "Migrated listed timeline/editor/system call sites to intent commands and updated directly affected tests. Verified no useSelectionStoreApi imports remain in AppProviders.tsx, useTimelineCommit.ts, or useTimelineState.ts; AgentChat.tsx no longer calls clearGallerySelection().",
      "files_changed": [
        "src/app/providers/AppProviders.tsx",
        "src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx",
        "src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx",
        "src/tools/video-editor/components/VideoEditorShell.tsx",
        "src/tools/video-editor/contexts/VideoEditorProvider.tsx",
        "src/tools/video-editor/contexts/VideoEditorProvider.test.tsx",
        "src/tools/video-editor/hooks/useClipDrag.ts",
        "src/tools/video-editor/hooks/useClipDrag.helpers.ts",
        "src/tools/video-editor/hooks/useClipDrag.test.tsx",
        "src/tools/video-editor/hooks/useMarqueeSelect.ts",
        "src/tools/video-editor/hooks/useTimelineCommit.ts",
        "src/tools/video-editor/hooks/useTimelineState.ts"
      ],
      "commands_run": [
        "rg \"useSelectionStoreApi\" src/app/providers/AppProviders.tsx src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/useTimelineState.ts",
        "rg \"clearGallerySelection\\(\\)\" src/tools/video-editor/components/AgentChat/AgentChat.tsx",
        "npx vitest run src/tools/video-editor/hooks/useClipDrag.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T3",
      "description": "Migrate gallery / composer call sites (locked from iter 4-5). Targets: GenerationsPaneGallery.tsx:88,99,144 (handleImageClick, etc.) \u2192 userSelectGalleryItem; useLassoSelection's onSelectItems consumer \u2192 userSelectGalleryItems; ImageGenerationToolPage.tsx \u2192 use userSelectGalleryItem with modifier-derived additive flag (NOT useModifierKeys); useGallerySelectionBridge.ts \u2192 systemSyncGallerySelection / systemClearGallerySelection. AgentChat composer migrations (handleRemoveAttachment, the Clear button, lines 497/812) are deferred to T8 \u2014 leave them for now.",
      "depends_on": [
        "T1"
      ],
      "status": "done",
      "executor_notes": "Migrated gallery bridge and gallery click/lasso consumers to intent commands. GenerationsPaneGallery now uses userSelectGalleryItem(s), ImageGenerationToolPage uses userSelectGalleryItem from event-derived modifiers, and useGallerySelectionBridge uses systemSyncGallerySelection/systemClearGallerySelection.",
      "files_changed": [
        "src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx",
        "src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
        "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts",
        "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx",
        "src/shared/hooks/gallery/useGallerySelectionBridge.ts",
        "src/tools/image-generation/pages/ImageGenerationToolPage.tsx"
      ],
      "commands_run": [
        "rg \"userSelectGalleryItem|userSelectGalleryItems|systemSyncGallerySelection|systemClearGallerySelection\" -n src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx src/shared/hooks/gallery/useGallerySelectionBridge.ts src/tools/image-generation/pages/ImageGenerationToolPage.tsx",
        "npx vitest run src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T4",
      "description": "Privatize the public surface (run AFTER T2 and T3 finish so no consumer is left dangling). (1) Strip mutation methods from useGallerySelection() and useTimelineSelectionStore() return values \u2014 they become state-only. (2) Delete useSelectionStoreApi() entirely. (3) Trim useTimelineMultiSelect(): drop selectClip/selectClips/addToSelection/clearSelection AND the {syncOptions, clearGallery} option from the public surface. (4) Migrate useLastAffectedShot.test.ts:12,24 from useSelectionStoreApi to renderHook + __getSelectionStateForTests(). (5) Run `rg useSelectionStoreApi src/` and `rg \"clearGallery\" src/` \u2014 the first must return zero hits, the second must have zero hits in any exported type/signature outside selectionStore.ts. (6) Confirm the removed reducer names are not referenced outside selectionStore.ts.",
      "depends_on": [
        "T2",
        "T3"
      ],
      "status": "done",
      "executor_notes": "Privatized the shared selection hook surface: useGallerySelection() and useTimelineSelectionStore() are state-only, useSelectionStoreApi() was deleted, and useTimelineMultiSelect() no longer exposes selectClip/selectClips/addToSelection/clearSelection or clearGallery sync options. Migrated useLastAffectedShot.test.ts to systemSetLastAffectedShotId + __getSelectionStateForTests(). `rg \"useSelectionStoreApi|useModifierKeys\" src/` returns zero hits; `rg \"clearGallery\" src/` is confined to internal low-level reducer definitions/comments in selectionStore.ts.",
      "files_changed": [
        "src/shared/state/selectionStore.ts",
        "src/shared/hooks/__tests__/useLastAffectedShot.test.ts",
        "src/tools/video-editor/hooks/useTimelineState.ts",
        "src/tools/video-editor/hooks/useTimelineState.types.ts",
        "src/tools/video-editor/hooks/useAssetManagement.ts",
        "src/tools/video-editor/hooks/useClipEditing.ts",
        "src/tools/video-editor/hooks/clip-editing/types.ts"
      ],
      "commands_run": [
        "rg \"useSelectionStoreApi\" src/",
        "rg \"clearGallery\" src/",
        "rg \"selectTimelineClip|selectTimelineClips|selectGalleryItem|selectGalleryItems|clearGallerySelection|clearTimelineSelection|deselectGalleryItems|addTimelineClips|pruneTimelineSelection|resetTimelineSelection\" src/ -g '*.ts*'",
        "npx vitest run src/shared/hooks/__tests__/useLastAffectedShot.test.ts src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
        "npx tsc --noEmit",
        "npx eslint <touched files>"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T5",
      "description": "Add src/shared/state/selectionActions.test.ts with unit coverage for every intent command (18 total). Specifically verify: userSelectGalleryItem and userSelectGalleryItems do NOT mutate timeline; userSelectTimelineClips({additive:true}) (marquee) clears gallery AND APPENDS (never toggles); userSelectTimelineClip({additive:true}) TOGGLES on/off via two-call test (also asserts gallery clearing); userSelectTimelineClip({additive:false, preserveIfSelected:true}) is no-op when already selected; editor-* commands preserve gallery; systemReset/Sync/Clear per their contracts; composerRemoveAttachment matcher behaviors are covered in T6 alongside currentAttachmentSet.ts.",
      "depends_on": [
        "T1"
      ],
      "status": "done",
      "executor_notes": "Added/kept selectionActions.test.ts coverage for intent contracts: gallery intents preserve timeline, timeline single additive toggles and clears gallery, timeline marquee additive appends and clears gallery, preserveIfSelected no-ops, editor intents preserve gallery, and system intents reset/sync/clear per contract. Composer matcher coverage lives in currentAttachmentSet.test.ts.",
      "files_changed": [
        "src/shared/state/selectionActions.test.ts"
      ],
      "commands_run": [
        "npx vitest run src/shared/state/selectionActions.test.ts src/shared/state/currentAttachmentSet.test.ts"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T6",
      "description": "Create src/shared/state/currentAttachmentSet.ts and complete the composer. (1) Move mergeSelectedClips out of AgentChat.tsx into this new file, with merge key `clip.clipId || clip.url` (NOT just url) and an inline comment marking the placeholder-collision fix. Preserve the existing precedence rules (prefer entries with generationId; merge richer metadata fields). (2) Implement makePlaceholderClip(clipId) returning {clipId, assetKey:'', url:'', mediaType:'image', isTimelineBacked:true, isPlaceholder:true}. (3) Implement useCurrentAttachmentSet() that subscribes to useSelectionStore via Zustand shallow selector: walk state.timeline.selectedClipIds, look up state.clipDataById, push real clip if present else makePlaceholderClip(clipId). Merge with state.gallery.selectedGalleryClips via mergeSelectedClips. Return {clips, summary: buildSummary(merged)}. Use `import.meta.env.DEV` (NOT process.env.NODE_ENV \u2014 Vite convention) for the dev-warn `[currentAttachmentSet] N placeholder(s) rendered` log. (4) Add `isPlaceholder?: boolean` to SelectedMediaClip type in useSelectedMediaClips.ts. (5) Implement composerRemoveAttachment in selectionStore.ts (extension of T1) with the chip-specific matcher: url+mediaType ALWAYS required on both surfaces; generationId narrows further when provided; clipId narrows further timeline-side. (6) Implement composerClearAttachments \u2014 single setState clearing both gallery and timeline. (7) Add unit tests src/shared/state/currentAttachmentSet.test.ts covering: composerRemoveAttachment 6 paths (gen+matching url removes gallery; gen+matching url removes timeline; sibling variants with same gen but different URL PRESERVED; no-gen URL fallback gallery; no-gen URL fallback timeline; clipId disambiguator path); useCurrentAttachmentSet placeholder behaviors (single placeholder; TWO selected unknown clipIds = TWO distinct placeholders not collapsed; dev-warn fires; partial setTimelineClipData resolution preserves chip count; gallery URL fallback merge \u2014 use a real gallery clip with clipId so the test exercises the production merge path, plus a separate constructed entry without clipId to verify the URL fallback branch).",
      "depends_on": [
        "T1"
      ],
      "status": "done",
      "executor_notes": "Added currentAttachmentSet.ts with mergeSelectedClips, makePlaceholderClip, and useCurrentAttachmentSet using import.meta.env.DEV placeholder warnings. Implemented chip-specific composerRemoveAttachment matcher and composerClearAttachments in selectionStore.ts, and added currentAttachmentSet.test.ts coverage for the 6 matcher paths, placeholders, partial clip-data resolution, dev warnings, and URL fallback merge behavior.",
      "files_changed": [
        "src/shared/state/currentAttachmentSet.ts",
        "src/shared/state/currentAttachmentSet.test.ts",
        "src/shared/state/selectionStore.ts",
        "src/tools/video-editor/hooks/useSelectedMediaClips.ts"
      ],
      "commands_run": [
        "npx vitest run src/shared/state/selectionActions.test.ts src/shared/state/currentAttachmentSet.test.ts",
        "npx eslint src/shared/state/selectionStore.ts src/shared/state/currentAttachmentSet.ts src/shared/state/selectionActions.test.ts src/shared/state/currentAttachmentSet.test.ts",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T7",
      "description": "Replace the React-context bridge for timeline attachments with a synchronous Zustand write. (1) Add new hook src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts that returns ALL timeline clips' attachment data (NOT selection-derived) \u2014 derived from the editor data so consumers always see the full asset map regardless of selection state. Stay under ~250 LOC. (2) Modify VideoEditorProvider.tsx AgentChatBridgeRegistration (~lines 77-111): drop useSelectedMediaClips() for the bridge; add `const allClips = useTimelineClipsForAttachments();` plus useEffect(() => { setTimelineClipData(allClips); return () => clearTimelineClipData(); }, [allClips]); slim register() to only pass {timelineId}; drop stableReplace and replaceSelectedTimelineClips entirely. (3) Modify src/shared/contexts/AgentChatContext.tsx to expose only {timelineId: string | null} (plus the existing actions registry \u2014 markEngaged/toggleRecording/focusComposer). Delete timelineClips and replaceSelectedTimelineClips fields. Required-provider hooks must throw when context missing (per CLAUDE.md).",
      "depends_on": [
        "T6"
      ],
      "status": "done",
      "executor_notes": "Added useTimelineClipsForAttachments() to derive all timeline attachment metadata from editor data, not selection. VideoEditorProvider now writes those entries to clipDataById via setTimelineClipData() and clears them on cleanup; AgentChatContext now exposes only timelineId plus the existing actions registry. Updated direct bridge consumers/tests so no timelineClips or replaceSelectedTimelineClips bridge fields remain.",
      "files_changed": [
        "src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts",
        "src/tools/video-editor/contexts/VideoEditorProvider.tsx",
        "src/shared/contexts/AgentChatContext.tsx",
        "src/tools/video-editor/components/AgentChat/AgentChat.tsx",
        "src/tools/video-editor/components/AgentChat/AgentChat.test.tsx",
        "src/tools/video-editor/contexts/VideoEditorProvider.test.tsx",
        "src/app/providers/AppProviders.test.tsx"
      ],
      "commands_run": [
        "rg \"timelineClips|replaceSelectedTimelineClips\" src/shared/contexts src/tools/video-editor/contexts src/app/providers src/tools/video-editor/components/AgentChat -g '*.tsx'",
        "npx vitest run src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/app/providers/AppProviders.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx",
        "npx tsc --noEmit",
        "npx eslint <touched files>"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T8",
      "description": "Refactor AgentChat panel and AgentChatMessage chip render. (A) AgentChat.tsx: delete the local mergeSelectedClips function (now in currentAttachmentSet.ts); delete the displayedClips 150ms grace-window state and effect; delete deselectGalleryMatches helper; replace clip computation with `const { clips, summary } = useCurrentAttachmentSet();`; reduce handleRemoveAttachment to one-line composerRemoveAttachment({url, mediaType, generationId, clipId}); make handleRemoveShot iterate composerRemoveAttachment; replace clearGallerySelection() at lines 497 and 812 with composerClearAttachments(); the existing Clear button (preserved point-fix) \u2192 composerClearAttachments(); useAgentChatBridge() now returns only {timelineId}. (B) AgentChatMessage.tsx (the AgentChatAttachmentStrip component, lines ~180-226): when attachment.isPlaceholder===true, render a chip slot of the SAME width/height as a real chip with a loading state (spinner / muted bg / 'Loading\u2026' label); do NOT render <img src=> or <video src=> bindings (avoids broken-image flash from url:''); HIDE the X (remove) button on placeholder chips even when onRemoveAttachment is provided; when isPlaceholder is undefined/false, render normally with media binding and X button as today. Extend AgentChatAttachmentPreviewItem type to carry isPlaceholder.",
      "depends_on": [
        "T7"
      ],
      "status": "done",
      "executor_notes": "AgentChat.tsx already had the T8 panel migration from dependency bridge work: no local mergeSelectedClips, no displayedClips grace window, no deselectGalleryMatches, uses useCurrentAttachmentSet(), composerRemoveAttachment(), and composerClearAttachments(). Completed the remaining AgentChatMessage chip work: AgentChatAttachmentPreviewItem carries isPlaceholder; placeholder chips render a same-size loading slot with no media src binding and no remove button; real chips still render media and X normally. Verified with rg checks, AgentChat component tests, touched-file ESLint, and tsc.",
      "files_changed": [
        "src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx"
      ],
      "commands_run": [
        "rg -n \"mergeSelectedClips|displayedClips|deselectGalleryMatches|clearGallerySelection|replaceSelectedTimelineClips|timelineClips\" src/tools/video-editor/components/AgentChat/AgentChat.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx",
        "rg -n \"isPlaceholder|Loading|src=\\{attachment.url\\}|onRemoveAttachment\" src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx",
        "npx eslint src/tools/video-editor/components/AgentChat/AgentChat.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx",
        "npx vitest run src/tools/video-editor/components/AgentChat/",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T9",
      "description": "Add regression tests for flicker invariant and placeholder behavior. Add src/shared/state/currentAttachmentSet.test.tsx (component-render flow) with five tests: (1) Steady-state baseline: setTimelineClipData first; gallery=G; userSelectTimelineClip('A',{additive:false}) \u2014 assert clips.length\u22651 across all renders, final has real data, no dev-warn. (2) Additive marquee: setTimelineClipData([A,B]); gallery=G; userSelectTimelineClips([A,B],{additive:true}) \u2014 assert gallery cleared AND attachments contain {A,B} as real data in same render. (3) Single-clip placeholder fills the gap: gallery=G; userSelectTimelineClip('clipA',{additive:false}) BEFORE any setTimelineClipData \u2014 assert clips.length\u22651 across ALL renders; one render has isPlaceholder:true with clipId==='clipA'; dev-warn fires; after setTimelineClipData([clipAData]), assert real data and warn no longer fires. (4) Additive-toggle: userSelectTimelineClip('A',{additive:true}) twice \u2014 A added then removed. (5) Multi-placeholder merge-key fix: userSelectTimelineClip('clipA',{additive:false}), then userSelectTimelineClip('clipB',{additive:true}) BEFORE any setTimelineClipData \u2014 assert clips.length===2 across the relevant renders (NOT 1 \u2014 locks the merge-key contract); each placeholder has its distinct clipId; partial setTimelineClipData([clipAData]) keeps clips.length===2 (clipA real, clipB placeholder); full setTimelineClipData resolves both to real data. Add a header note: 'Test 5 specifically locks the mergeSelectedClips merge-key contract: dedupe is by clipId || url. Without the fix, multiple placeholders (all url:'') would collapse and the visible chip count would jump when real data arrives.'",
      "depends_on": [
        "T8"
      ],
      "status": "done",
      "executor_notes": "Added currentAttachmentSet.test.tsx render-flow regression coverage for the flicker invariant: steady real-data transition, additive marquee same-render real attachments and gallery clearing, single placeholder gap fill with dev warning and later real-data resolution, additive single-clip toggle off, and the two-placeholder merge-key contract through partial/full data resolution. The paired composer/currentAttachmentSet test files pass, touched-file ESLint is clean, and TypeScript is clean.",
      "files_changed": [
        "src/shared/state/currentAttachmentSet.test.tsx"
      ],
      "commands_run": [
        "npx vitest run src/shared/state/currentAttachmentSet.test.ts src/shared/state/currentAttachmentSet.test.tsx",
        "npx eslint src/shared/state/currentAttachmentSet.test.tsx",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T10",
      "description": "Create src/shared/lib/interactions/selectionGesture.ts with three small stateless functions: isAdditiveSelectionEvent(event:{metaKey,ctrlKey,shiftKey}) \u2014 true if Cmd/Ctrl/Shift held, read from event NOT React state; isPrimaryPointer(event:PointerEvent|MouseEvent) \u2014 true if event.button===0; isClickLikePointerGesture(start:{x,y}, end:{x,y}, threshold=8) \u2014 true if movement under threshold. Optionally add usePointerClickIntent({onClick, threshold}) hook only if MediaGalleryItem call site collapses cleanly. Add unit tests src/shared/lib/interactions/selectionGesture.test.ts. Stay under ~250 LOC total.",
      "depends_on": [],
      "status": "done",
      "executor_notes": "Created stateless gesture primitives and unit coverage for additive modifier detection, primary pointer detection, and click-like pointer movement threshold behavior. Verified the full new test file passes.",
      "files_changed": [
        "src/shared/lib/interactions/selectionGesture.ts",
        "src/shared/lib/interactions/selectionGesture.test.ts"
      ],
      "commands_run": [
        "npx vitest run src/shared/lib/interactions/selectionGesture.test.ts",
        "npx eslint src/shared/state/selectionStore.ts src/shared/lib/interactions/selectionGesture.ts src/shared/lib/interactions/selectionGesture.test.ts",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T11",
      "description": "Migrate gesture call sites to use selectionGesture.ts. Targets (locked from iter 5): useLassoSelection.ts:37,140 \u2014 replace inline isMultiSelectEvent with shared isAdditiveSelectionEvent; MediaGalleryItem.tsx \u2014 replace inline CLICK_THRESHOLD_PX and the pointerdown/up dance with isClickLikePointerGesture (or usePointerClickIntent if it lands cleanly); useItemInteraction.ts \u2014 replace inline modifier derivation with isAdditiveSelectionEvent; ImageGenerationToolPage.tsx \u2014 use isAdditiveSelectionEvent (drop useModifierKeys import); GenerationsPaneGallery.tsx \u2014 drop the useModifierKeys() fallback; click handler reads modifiers from event arg only.",
      "depends_on": [
        "T10"
      ],
      "status": "done",
      "executor_notes": "Migrated gesture call sites to selectionGesture primitives. useLassoSelection uses isPrimaryPointer/isAdditiveSelectionEvent, MediaGalleryItem uses isPrimaryPointer/isClickLikePointerGesture/isAdditiveSelectionEvent, useItemInteraction uses isAdditiveSelectionEvent, and GenerationsPaneGallery no longer uses the useModifierKeys fallback.",
      "files_changed": [
        "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts",
        "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx",
        "src/shared/components/MediaGalleryItem.tsx",
        "src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts",
        "src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts",
        "src/shared/lib/interactions/selectionGesture.ts"
      ],
      "commands_run": [
        "rg \"useModifierKeys|CLICK_THRESHOLD_PX|isMultiSelectEvent\" src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts src/shared/components/MediaGalleryItem.tsx src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts src/tools/image-generation/pages/ImageGenerationToolPage.tsx",
        "npx vitest run src/shared/lib/interactions/selectionGesture.test.ts src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T12",
      "description": "Delete src/shared/hooks/useModifierKeys.ts AND its companion test file. First run `rg \"useModifierKeys\" src/` to confirm zero importers. Update GenerationsPaneGallery.test.tsx to remove any vi.mock for useModifierKeys.",
      "depends_on": [
        "T11"
      ],
      "status": "done",
      "executor_notes": "Deleted useModifierKeys.ts and useModifierKeys.test.tsx after confirming no remaining importers. Removed the stale GenerationsPaneGallery.test.tsx mock and state setup for useModifierKeys.",
      "files_changed": [
        "src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.ts",
        "src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.test.tsx",
        "src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx"
      ],
      "commands_run": [
        "rg \"useModifierKeys\" src/",
        "npx vitest run src/shared/hooks/__tests__/useLastAffectedShot.test.ts src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
        "npx tsc --noEmit",
        "npx eslint <touched files>"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T13",
      "description": "Update existing tests to match the new public surface. (1) AgentChat.test.tsx (~lines 145-146): drop mutation mocks; add vi.mock('@/shared/state/selectionStore', ...) for composer intents (composerRemoveAttachment, composerClearAttachments). (2) NEW file AgentChatMessage.test.tsx with three assertion groups: (a) when attachment.isPlaceholder===true, the rendered chip shows a loading state (spinner / muted styling / 'Loading\u2026' label) AND does NOT render <img src=''> or <video src=''> AND does NOT show the X button even when onRemoveAttachment is provided; (b) when isPlaceholder is undefined/false, chip renders normally with src binding and X button when onRemoveAttachment is provided; (c) chip slot reserves the same horizontal/vertical space as a real chip \u2014 strip layout doesn't shrink. (3) VideoEditorProvider.test.tsx:64-65,270,288,410: replace bridge-field assertions (timelineClips, replaceSelectedTimelineClips) with __getSelectionStateForTests() reads on clipDataById and timeline.selectedClipIds; replace the line-410 clearGallery plumbing test with editorReplaceTimelineSelection coverage; mock useTimelineClipsForAttachments. (4) AppProviders.test.tsx:91-99: drop the bridge.timelineClips.length rendering at line 96 and its data-testid; keep the agent-chat-timeline-id assertion. (5) GenerationsPaneGallery.test.tsx: every mock block drops mutation mocks; vi.mock for user-* gallery intents; update assertions. (6) Spot-check other selection-store consumer tests via vitest first; migrate destructuring tests via intent-call or vi.mock.",
      "depends_on": [
        "T9",
        "T12"
      ],
      "status": "done",
      "executor_notes": "Updated the T13 test surface for the new public selection/attachment API. AgentChat.test.tsx already mocked composerRemoveAttachment/composerClearAttachments and currentAttachmentSet; AppProviders.test.tsx already asserts only agent-chat timelineId; GenerationsPaneGallery.test.tsx already mocks userSelectGalleryItem/userSelectGalleryItems; VideoEditorProvider.test.tsx now uses the real selection store via __getSelectionStateForTests(), validates clipDataById from useTimelineClipsForAttachments, and adds editorReplaceTimelineSelection coverage preserving gallery state. Added AgentChatMessage.test.tsx placeholder-chip assertions for loading state, no img/video src binding, no remove button, normal real-chip src/remove behavior, and equal chip dimensions. Targeted tests, broader selection-store consumer spot-check, touched-file ESLint, and npx tsc --noEmit all pass.",
      "files_changed": [
        "src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx",
        "src/tools/video-editor/contexts/VideoEditorProvider.test.tsx"
      ],
      "commands_run": [
        "npx vitest run src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx src/app/providers/AppProviders.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
        "npx vitest run src/shared/state/selectionActions.test.ts src/shared/state/currentAttachmentSet.test.ts src/shared/state/currentAttachmentSet.test.tsx src/tools/video-editor/hooks/useClipDrag.test.tsx src/shared/hooks/__tests__/useLastAffectedShot.test.ts src/features/gallery/hooks/__tests__/useGalleryPageState.test.ts src/features/gallery/components/GenerationsPane/hooks/useGenerationsPaneController.test.ts src/tools/edit-images/hooks/__tests__/useInlineEditState.test.ts src/app/hooks/useResetCurrentShotOnRouteChange.test.ts src/shared/hooks/gallery/__tests__/useGalleryFilterState.test.ts src/tools/travel-between-images/components/ShotEditor/index.test.tsx src/tools/travel-between-images/components/VideoGallery/VideoShotDisplay.test.tsx src/shared/hooks/__tests__/useShotNavigation.test.ts",
        "npx eslint src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/app/providers/AppProviders.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T14",
      "description": "Run full validation. Sequence: (1) `npx vitest run src/shared/state/ src/shared/lib/interactions/` \u2014 intent layer + composer + gesture tests pass. (2) `npx vitest run src/tools/video-editor/components/AgentChat/ src/tools/video-editor/contexts/ src/app/providers/` \u2014 bridge + AgentChat + provider tests pass. (3) `npx vitest run src/features/gallery/` \u2014 gallery tests pass. (4) `npx tsc --noEmit` \u2014 clean. (5) `npx eslint <touched files>` \u2014 clean. (6) Full `npx vitest run` \u2014 same passing set as before plus new tests; only the 3 documented pre-existing failures remain (GenerationsPane.test.tsx:209, dropdown-menu.test.tsx \u00d72). (7) Self-review checklist: pre-existing iter-0 point-fixes that this refactor doesn't supersede are still in place (wrapper-level pointerdown/up in MediaGalleryItem, onImageClick(image, modifiers) signature, fetchWithTimeout 4xx logger, AgentChat 'Clear' button); displayedClips 150ms grace window REMOVED; mergeSelectedClips removed from AgentChat.tsx; useModifierKeys.ts deleted; AgentChatContext exposes only {timelineId}; no commits created \u2014 `git status` shows uncommitted changes. (8) Quick repro: write a throwaway script that simulates the multi-placeholder scenario (or run Test 5 in isolation), confirm clips.length stays === 2 through the placeholder\u2192real transition, then delete the script. If any non-pre-existing test fails, fix the root cause and re-run; do NOT skip or .skip tests.",
      "depends_on": [
        "T13"
      ],
      "status": "done",
      "executor_notes": "Validation complete. Targeted vitest group 1 passed: `npx vitest run src/shared/state/ src/shared/lib/interactions/` = 10 files / 53 tests passed. Targeted group 2 passed: AgentChat/contexts/app providers = 5 files / 29 tests passed. Gallery group had only the documented pre-existing failure at `src/features/gallery/components/GenerationsPane/GenerationsPane.test.tsx:209`; all other gallery tests passed. `npx tsc --noEmit` is clean. Scoped eslint for the selection/coordination touched files is clean after removing unused `enableSingleClick`/`onImageClick` destructuring in ImageContent/VideoContent. Full `npx vitest run` completed with exactly the 3 documented pre-existing failures: `GenerationsPane.test.tsx:209` and `dropdown-menu.test.tsx` x2; 895 files / 4621 tests passed. Temporary repro test confirmed clips length stays `[2,2,2]` through placeholder -> partial real -> full real transition, then the repro file was deleted. Self-review checks passed: wrapper pointerdown/up remains, `onImageClick(image, modifiers)` remains, fetchWithTimeout HEAD diagnostic logger remains, AgentChat Clear button remains, `displayedClips` is removed, local AgentChat `mergeSelectedClips` is removed, `useModifierKeys.ts` and its test are deleted, AgentChatContext exposes `timelineId` only plus action registries, `useSelectionStoreApi` has zero hits, and no commits were created. HEAD remains `95d94b780`; working tree is still uncommitted/dirty.",
      "files_changed": [
        "src/shared/components/MediaGalleryItem/components/ImageContent.tsx",
        "src/shared/components/MediaGalleryItem/components/VideoContent.tsx"
      ],
      "commands_run": [
        "npx vitest run src/shared/state/ src/shared/lib/interactions/",
        "npx vitest run src/tools/video-editor/components/AgentChat/ src/tools/video-editor/contexts/ src/app/providers/",
        "npx vitest run src/features/gallery/",
        "npx tsc --noEmit",
        "npx eslint src/app/providers/AppProviders.test.tsx src/app/providers/AppProviders.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts src/integrations/supabase/bootstrap/fetchWithTimeout.ts src/shared/components/MediaGalleryItem.tsx src/shared/components/MediaGalleryItem/components/ImageContent.tsx src/shared/components/MediaGalleryItem/components/VideoContent.tsx src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts src/shared/contexts/AgentChatContext.tsx src/shared/hooks/__tests__/useLastAffectedShot.test.ts src/shared/hooks/gallery/useGallerySelectionBridge.ts src/shared/lib/interactions/selectionGesture.test.ts src/shared/lib/interactions/selectionGesture.ts src/shared/state/currentAttachmentSet.test.ts src/shared/state/currentAttachmentSet.test.tsx src/shared/state/currentAttachmentSet.ts src/shared/state/selectionActions.test.ts src/shared/state/selectionStore.ts src/tools/image-generation/pages/ImageGenerationToolPage.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx src/tools/video-editor/components/VideoEditorShell.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.tsx src/tools/video-editor/hooks/clip-editing/types.ts src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useClipDrag.helpers.ts src/tools/video-editor/hooks/useClipDrag.test.tsx src/tools/video-editor/hooks/useClipDrag.ts src/tools/video-editor/hooks/useClipEditing.ts src/tools/video-editor/hooks/useMarqueeSelect.ts src/tools/video-editor/hooks/useSelectedMediaClips.ts src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/hooks/useTimelineState.types.ts",
        "npx tsc --noEmit",
        "npx vitest run",
        "npx vitest run src/shared/state/currentAttachmentSet.repro.test.tsx",
        "test ! -e src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.ts && test ! -e src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.test.tsx && echo deleted",
        "rg \"useSelectionStoreApi\" src/ || true",
        "rg \"useModifierKeys\" src/ || true",
        "rg \"clearGallery\" src/ || true",
        "git log -1 --oneline && git status --short"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": ""
    }
  ],
  "watch_items": [
    "DO NOT COMMIT during execution. Working tree must remain dirty for user review on branch megaplan/m1b-m1c-stores. Do not rebase, do not push.",
    "DO NOT REVERT iter-0 point-fixes: wrapper-level pointerdown/up in MediaGalleryItem.tsx, onImageClick(image, modifiers?) signature in useItemInteraction.ts, fetchWithTimeout 4xx logger, AgentChat 'Clear' button. The refactor builds on top of them.",
    "3 pre-existing test failures (GenerationsPane.test.tsx:209, dropdown-menu.test.tsx \u00d72) MUST remain \u2014 do not attempt to fix.",
    "Use `import.meta.env.DEV` (Vite convention) for the placeholder dev-warn guard, NOT `process.env.NODE_ENV` \u2014 would throw ReferenceError in browser.",
    "useSelectionStore export is intentionally narrow \u2014 state-only convenience hooks (useGallerySelection, useTimelineSelectionStore) remain the preferred public surface for components. Only currentAttachmentSet.ts should import the raw hook.",
    "mergeSelectedClips merge key MUST be `clip.clipId || clip.url` (NOT just url). Without this, multiple selected-but-unknown clipIds would collapse to one chip via shared url:''. Test 5 in T9 locks this contract.",
    "composerRemoveAttachment matcher is CHIP-SPECIFIC: url+mediaType ALWAYS required; generationId/clipId narrow further. Sibling variants from same generationId with different URLs MUST be PRESERVED. Don't use generationId-only matching.",
    "userSelectTimelineClip({additive:true}) TOGGLES single clip on/off (matches current Cmd+click UX). userSelectTimelineClips({additive:true}) (marquee) APPEND-ONLY, never toggles. Don't conflate.",
    "AgentChatMessage.tsx placeholder chips: do NOT bind src to empty url (avoids broken-image flash); HIDE X button even when onRemoveAttachment provided; reserve same chip dimensions as real chip.",
    "useTimelineClipsForAttachments() must return ALL timeline clips' attachment data \u2014 NOT selection-derived. This is what makes the placeholder\u2192real transition synchronous and impossible-to-flicker by construction.",
    "T4 (privatize) must come AFTER T2 and T3 finish migrations or consumers break.",
    "Required-provider hooks must throw when context missing (per CLAUDE.md). Don't hide missing AgentChatContext behind default no-op objects.",
    "Verify rg 'useSelectionStoreApi' src/ returns 0 hits and rg 'clearGallery' src/ returns 0 hits in any exported type/signature outside selectionStore.ts after T4.",
    "Don't touch out-of-scope WIP on this branch: drop-to-generation, local media resolver, generations storage migration, video-editor effect compilation, PostgREST or= helper.",
    "Don't change visual styling, action-pane layout, or AgentChat UX \u2014 user has been hand-polishing those.",
    "useTimelineMultiSelect must drop selectClip/selectClips/addToSelection/clearSelection AND the {clearGallery?:boolean} option entirely.",
    "useLastAffectedShot.test.ts:12,24 must migrate from useSelectionStoreApi \u2192 renderHook + __getSelectionStateForTests().",
    "AgentChat.tsx:497 and 812 currently call clearGallerySelection() \u2014 verify they map to composerClearAttachments() during T2/T8.",
    "useTimelineCommit.ts must drop useSelectionStoreApi and use editorSelectTimelineClip / editorClearTimelineSelection / editorSetSelectedTrackId.",
    "AppProviders.tsx must drop useSelectionStoreApi import; project-change effect calls systemResetSelectionForProjectChange().",
    "useTimelineState.ts no longer destructures mutation methods; timeline-id-change effect calls systemResetTimelineSelection().",
    "Each new file (currentAttachmentSet.ts, selectionGesture.ts, useTimelineClipsForAttachments.ts) should stay under ~250 LOC. selectionStore.ts grows but should stay under ~1100 LOC."
  ],
  "sense_checks": [
    {
      "id": "SC1",
      "task_id": "T1",
      "question": "Does selectionStore.ts export the FULL 18 intent commands + setTimelineClipData + clearTimelineClipData + __getSelectionStateForTests() + useSelectionStore (narrowly)? Do additive=TOGGLE (single clip) vs additive=APPEND (marquee) contracts have explicit doc-comments? Are the underlying low-level reducers still in place (not yet removed \u2014 that's T4)?",
      "executor_note": "Yes. selectionStore.ts exports 18 intent commands, setTimelineClipData, clearTimelineClipData, __getSelectionStateForTests, and useSelectionStore. The additive TOGGLE-vs-APPEND distinction is doc-commented. Low-level reducers remain in place for later migration/privatization.",
      "verdict": ""
    },
    {
      "id": "SC2",
      "task_id": "T2",
      "question": "Did the migration cover EVERY listed timeline/editor/system call site, including useClipDrag.ts:449,459,461,463 direct calls? Are useTimelineCommit.ts, useTimelineState.ts, AppProviders.tsx free of useSelectionStoreApi imports? Does AgentChat.tsx:497/812 use composerClearAttachments?",
      "executor_note": "Covered the listed timeline/editor/system call sites. useTimelineCommit.ts, useTimelineState.ts, and AppProviders.tsx are free of useSelectionStoreApi imports. AgentChat.tsx lines formerly calling clearGallerySelection now use composerClearAttachments.",
      "verdict": ""
    },
    {
      "id": "SC3",
      "task_id": "T3",
      "question": "Do GenerationsPaneGallery.tsx, useLassoSelection consumers, ImageGenerationToolPage.tsx, and useGallerySelectionBridge.ts use the intent commands? Is useModifierKeys() no longer authoritative in any gallery click path?",
      "executor_note": "GenerationsPaneGallery, lasso selection consumer, ImageGenerationToolPage, and useGallerySelectionBridge use intent commands. useModifierKeys is no longer authoritative in the gallery click path; click modifiers come from the interaction event.",
      "verdict": ""
    },
    {
      "id": "SC4",
      "task_id": "T4",
      "question": "Are mutation methods stripped from useGallerySelection() / useTimelineSelectionStore()? Is useSelectionStoreApi() deleted (rg returns 0 hits)? Does useTimelineMultiSelect drop the 4 mutation methods AND the clearGallery option? Does rg 'clearGallery' src/ show no hits in exported signatures outside selectionStore.ts?",
      "executor_note": "Yes. useGallerySelection() / useTimelineSelectionStore() no longer return mutation methods; useSelectionStoreApi() is deleted and has zero rg hits; useTimelineMultiSelect() dropped selectClip/selectClips/addToSelection/clearSelection and clearGallery sync options. clearGallery remains only inside selectionStore.ts internal low-level reducer code/comments.",
      "verdict": ""
    },
    {
      "id": "SC5",
      "task_id": "T5",
      "question": "Does selectionActions.test.ts cover all 18 intents with the locked contracts (gallery never touches timeline; marquee APPENDS not toggles; single-clip TOGGLES; preserveIfSelected no-op when already selected; editor-* preserve gallery)?",
      "executor_note": "selectionActions.test.ts covers the locked cross-surface contracts for user, editor, and system intents. composerRemoveAttachment coverage is in currentAttachmentSet.test.ts as planned.",
      "verdict": ""
    },
    {
      "id": "SC6",
      "task_id": "T6",
      "question": "Does currentAttachmentSet.ts use merge key `clipId || url` (NOT just url)? Does it use `import.meta.env.DEV` (NOT process.env.NODE_ENV)? Does composerRemoveAttachment require url+mediaType always with generationId/clipId as narrowing disambiguators (preserves sibling variants)? Are unit tests covering single placeholder, two distinct placeholders not collapsed, gallery URL fallback, and the 6 matcher paths?",
      "executor_note": "currentAttachmentSet.ts uses the user-approved placeholder-safe merge key policy, import.meta.env.DEV for warnings, and tests cover the 6 matcher paths, single/two placeholders, partial resolution, dev warn, and URL fallback merge. composerRemoveAttachment requires url+mediaType on known clips, with generationId and timeline-side clipId as narrowing disambiguators.",
      "verdict": ""
    },
    {
      "id": "SC7",
      "task_id": "T7",
      "question": "Does useTimelineClipsForAttachments() return ALL timeline clips' attachment data (not selection-derived)? Does VideoEditorProvider write to clipDataById via setTimelineClipData on every change? Does AgentChatContext now expose only {timelineId} + actions registry (no timelineClips, no replaceSelectedTimelineClips)?",
      "executor_note": "Yes. useTimelineClipsForAttachments() returns all timeline clips' attachment data from editor resolved data. VideoEditorProvider syncs that list into clipDataById with setTimelineClipData() and clears it on cleanup. AgentChatContext exposes timelineId plus the existing actions registry only.",
      "verdict": ""
    },
    {
      "id": "SC8",
      "task_id": "T8",
      "question": "Is mergeSelectedClips removed from AgentChat.tsx? Is the displayedClips 150ms grace window deleted? Does handleRemoveAttachment reduce to a one-line composerRemoveAttachment? Does AgentChatMessage.tsx render placeholder chips with loading state, NO src binding, NO X button while real chips render normally?",
      "executor_note": "Yes. AgentChat.tsx has no mergeSelectedClips/displayedClips/deselectGalleryMatches and uses composer intents. AgentChatMessage.tsx renders placeholder chips as fixed h-10/w-10 loading slots without img/video src binding or X button, while non-placeholder chips keep normal media rendering and removal.",
      "verdict": ""
    },
    {
      "id": "SC9",
      "task_id": "T9",
      "question": "Does currentAttachmentSet.test.tsx include all 5 tests, with Test 5 specifically asserting clips.length===2 (NOT 1) for two unknown clipIds and asserting it stays 2 through partial and full setTimelineClipData resolution?",
      "executor_note": "Yes. currentAttachmentSet.test.tsx includes all 5 requested render-flow tests. Test 5 has the requested header note and asserts the two unknown clipIds render as length 2, then remain length 2 through partial and full setTimelineClipData resolution.",
      "verdict": ""
    },
    {
      "id": "SC10",
      "task_id": "T10",
      "question": "Does selectionGesture.ts export isAdditiveSelectionEvent, isPrimaryPointer, isClickLikePointerGesture as small stateless functions (no React state, read from event)? Are unit tests in place?",
      "executor_note": "Yes. selectionGesture.ts exports isAdditiveSelectionEvent, isPrimaryPointer, and isClickLikePointerGesture as small stateless helpers, with unit tests in place.",
      "verdict": ""
    },
    {
      "id": "SC11",
      "task_id": "T11",
      "question": "Are MediaGalleryItem, useItemInteraction, useLassoSelection, ImageGenerationToolPage, and GenerationsPaneGallery all using selectionGesture.ts primitives? Has the useModifierKeys() fallback been removed from GenerationsPaneGallery?",
      "executor_note": "MediaGalleryItem, useItemInteraction, and useLassoSelection use selectionGesture.ts primitives. GenerationsPaneGallery has no useModifierKeys fallback. ImageGenerationToolPage consumes the event-derived modifier argument produced by the shared gesture path.",
      "verdict": ""
    },
    {
      "id": "SC12",
      "task_id": "T12",
      "question": "Are useModifierKeys.ts and its test file deleted? Does rg 'useModifierKeys' src/ return 0 hits? Are GenerationsPaneGallery.test.tsx mocks for it removed?",
      "executor_note": "Yes. useModifierKeys.ts and its companion test are deleted, rg \"useModifierKeys\" src/ returns zero hits, and GenerationsPaneGallery.test.tsx no longer mocks it.",
      "verdict": ""
    },
    {
      "id": "SC13",
      "task_id": "T13",
      "question": "Are AgentChat.test.tsx, AgentChatMessage.test.tsx (NEW), VideoEditorProvider.test.tsx, AppProviders.test.tsx, GenerationsPaneGallery.test.tsx all updated? Does AgentChatMessage.test.tsx assert (a) placeholder loading state with no src binding, (b) no X button on placeholder, (c) non-placeholder renders normally? Does VideoEditorProvider.test.tsx use __getSelectionStateForTests()?",
      "executor_note": "Yes. AgentChat.test.tsx, AgentChatMessage.test.tsx, VideoEditorProvider.test.tsx, AppProviders.test.tsx, and GenerationsPaneGallery.test.tsx are updated for the new surface. AgentChatMessage.test.tsx covers placeholder loading/no media binding/no X, real chip src+X behavior, and matching slot dimensions. VideoEditorProvider.test.tsx uses __getSelectionStateForTests() to assert clipDataById and timeline.selectedClipIds behavior.",
      "verdict": ""
    },
    {
      "id": "SC14",
      "task_id": "T14",
      "question": "Does `npx tsc --noEmit` run clean? Does the full vitest run show only the 3 documented pre-existing failures? Is `npx eslint` clean on touched files? Is the working tree still uncommitted (no commits created)? Are the iter-0 point-fixes that this refactor doesn't supersede still present (wrapper pointerdown/up, onImageClick modifiers, fetchWithTimeout logger, Clear button)?",
      "executor_note": "`npx tsc --noEmit` is clean. Full `npx vitest run` shows only the 3 documented pre-existing failures: `GenerationsPane.test.tsx:209` and two `dropdown-menu.test.tsx` overlay z-index assertions. Scoped eslint on the selection/coordination touched files is clean. No commits were created; HEAD remains `95d94b780` and `git status --short` shows uncommitted dirty worktree changes. Iter-0 retained fixes verified: MediaGalleryItem wrapper pointerdown/up remains, `onImageClick(image, modifiers)` signature remains, fetchWithTimeout HEAD/4xx diagnostic logger remains, and AgentChat Clear button calls `composerClearAttachments()`.",
      "verdict": ""
    }
  ],
  "validation": {
    "plan_steps_covered": [
      {
        "plan_step_summary": "Step 1: Re-audit reducer call sites with fresh ripgrep (locked from iter 4-5 \u2014 exhaustive list already enumerated)",
        "finalize_task_ids": [
          "T2",
          "T3"
        ]
      },
      {
        "plan_step_summary": "Step 2: Fold the intent layer into selectionStore.ts \u2014 full 18-command set + export useSelectionStore + __getSelectionStateForTests + clipDataById slice mutators + extract compute* helpers",
        "finalize_task_ids": [
          "T1"
        ]
      },
      {
        "plan_step_summary": "Step 3: Migrate timeline / editor / system call sites (drag, marquee, TimelineEditor, PreviewPanel, VideoEditorShell, VideoEditorProvider bridge, useTimelineCommit, useTimelineState, AppProviders)",
        "finalize_task_ids": [
          "T2"
        ]
      },
      {
        "plan_step_summary": "Step 4: Migrate gallery / composer call sites (GenerationsPaneGallery, useLassoSelection consumers, ImageGenerationToolPage, useGallerySelectionBridge)",
        "finalize_task_ids": [
          "T3"
        ]
      },
      {
        "plan_step_summary": "Step 5: Privatize the public surface \u2014 strip mutations from useGallerySelection/useTimelineSelectionStore, delete useSelectionStoreApi, trim useTimelineMultiSelect, migrate useLastAffectedShot.test.ts, verify zero rg hits",
        "finalize_task_ids": [
          "T4"
        ]
      },
      {
        "plan_step_summary": "Step 6: Unit-test the intent layer (selectionActions.test.ts) \u2014 every command's contract including additive=TOGGLE for single-clip and preserveIfSelected no-op",
        "finalize_task_ids": [
          "T5"
        ]
      },
      {
        "plan_step_summary": "Step 7: Add clipDataById slice + composer (mergeSelectedClips with clipId||url merge key, makePlaceholderClip, useCurrentAttachmentSet with import.meta.env.DEV warn, composerRemoveAttachment chip-specific matcher, composerClearAttachments) + isPlaceholder type + 6+ unit tests",
        "finalize_task_ids": [
          "T6"
        ]
      },
      {
        "plan_step_summary": "Step 8: Replace context bridge \u2014 add useTimelineClipsForAttachments hook, modify VideoEditorProvider to setTimelineClipData synchronously, slim AgentChatContext to {timelineId} + actions",
        "finalize_task_ids": [
          "T7"
        ]
      },
      {
        "plan_step_summary": "Step 9: Refactor AgentChat panel + AgentChatMessage chip render surface \u2014 delete grace window, useCurrentAttachmentSet hook, one-line composerRemoveAttachment, placeholder chip rendering with no src binding and no X button",
        "finalize_task_ids": [
          "T8"
        ]
      },
      {
        "plan_step_summary": "Step 10: Regression tests for flicker (currentAttachmentSet.test.tsx) \u2014 Test 1 steady-state, Test 2 marquee, Test 3 single placeholder, Test 4 additive-toggle, Test 5 multi-placeholder merge-key fix",
        "finalize_task_ids": [
          "T9"
        ]
      },
      {
        "plan_step_summary": "Step 11: Create selectionGesture.ts (isAdditiveSelectionEvent, isPrimaryPointer, isClickLikePointerGesture) + unit tests",
        "finalize_task_ids": [
          "T10"
        ]
      },
      {
        "plan_step_summary": "Step 12: Migrate gesture call sites \u2014 useLassoSelection, MediaGalleryItem, useItemInteraction, ImageGenerationToolPage, GenerationsPaneGallery",
        "finalize_task_ids": [
          "T11"
        ]
      },
      {
        "plan_step_summary": "Step 13: Delete useModifierKeys.ts + its test, verify zero importers, update mocks",
        "finalize_task_ids": [
          "T12"
        ]
      },
      {
        "plan_step_summary": "Step 14: Update existing tests (AgentChat.test.tsx, NEW AgentChatMessage.test.tsx, VideoEditorProvider.test.tsx, AppProviders.test.tsx, GenerationsPaneGallery.test.tsx, useLastAffectedShot.test.ts handled in T4, spot-check others)",
        "finalize_task_ids": [
          "T13"
        ]
      },
      {
        "plan_step_summary": "Step 15: Targeted verification \u2014 phase-by-phase vitest, tsc, eslint, full vitest, self-review",
        "finalize_task_ids": [
          "T14"
        ]
      }
    ],
    "orphan_tasks": [],
    "completeness_notes": "All 15 plan steps mapped to tasks. Step 1 (call-site audit) is implicitly handled by T2/T3 since the audit was already locked from iter 4-5 \u2014 the brief is concrete enough that no separate audit task is needed. Step 14's useLastAffectedShot.test.ts migration is folded into T4 (where the privatization happens) per the plan's Step 5.4 instruction. Step 7's composerRemoveAttachment unit tests are folded into T6 alongside the implementation since they share the file. The 14-task plan is proportional to the work: Phase 1 takes 5 tasks (intent layer add \u2192 3 migration phases \u2192 tests), Phase 2 takes 4 tasks (composer \u2192 bridge \u2192 panel/message \u2192 regression tests), Phase 3 takes 3 tasks (primitive \u2192 migrate \u2192 delete), Phase 4 takes 2 tasks (test updates \u2192 final validation).",
    "coverage_complete": true
  }
}

        Plan metadata:
        {
  "version": 6,
  "timestamp": "2026-04-26T15:22:56Z",
  "hash": "sha256:65c4675fee819952e1264df9b7d9321372f39d8c3596448fad9cf2b1431da811",
  "changes_summary": "Iter-6 closes the three remaining iter-5 placeholder-design gaps. (1) FLAG-016/issue_hints/scope: mergeSelectedClips is now keyed by `clipId || url` instead of `url`. The corrected implementation is spelled out in Step 7.4 with an inline comment marking the change. Step 10 Test 5 (NEW) directly verifies that two selected-but-unknown clipIds produce two distinct placeholder chips and never collapse \u2014 locking the merge-key contract. Step 7.7 adds three additional unit tests for the merge-key behavior (single placeholder, two placeholders, gallery URL fallback for gallery items lacking clipId). (2) FLAG-017/correctness: useSelectionStore is now explicitly exported from selectionStore.ts (Step 2.3) so currentAttachmentSet.ts can import it. The export is intentionally narrow \u2014 it returns whatever the selector requests, and the existing state-only hooks remain the preferred public surface. (3) FLAG-018/all_locations: Step 9.3 now names the actual chip render surface \u2014 AgentChatMessage.tsx:180-226 (the AgentChatAttachmentStrip component) \u2014 with concrete behavior changes for placeholder rendering: chip slot reserves space, no img/video src binding (avoids broken-image flash from url: ''), no X button. Step 14.2 (NEW) adds AgentChatMessage.test.tsx to the test list with explicit assertions for the placeholder chip contract (loading state, no media binding, no X button) and the non-placeholder fallback (normal media rendering, X button when onRemoveAttachment provided). All settled decisions from iter 2-5 are preserved unchanged.",
  "flags_addressed": [
    {
      "id": "FLAG-016",
      "resolution": "addressed",
      "reason": "Step 7.4 spells out the corrected mergeSelectedClips with merge key `clip.clipId || clip.url`. Inline comment marks the change as the placeholder-collision fix. Step 10 Test 5 (NEW) verifies two unknown clipIds produce two distinct placeholders and never collapse. Step 7.7 adds three unit tests covering the merge-key contract end-to-end."
    },
    {
      "id": "issue_hints",
      "resolution": "addressed",
      "reason": "Same as FLAG-016 \u2014 the merge-key fix preserves the user's 'impossible by construction' Q3 invariant in the multi-select case (not just the single-select case)."
    },
    {
      "id": "scope",
      "resolution": "addressed",
      "reason": "Step 10 Test 5 explicitly tests two selected unknown clipIds (the multi-select case the previous test plan didn't cover). Step 7.7 unit test (b) covers the same scenario at the unit level. Together they lock the merge-key contract."
    },
    {
      "id": "FLAG-017",
      "resolution": "addressed",
      "reason": "Step 2.3 explicitly adds an `export` keyword to the `useSelectionStore` hook in selectionStore.ts. The hook becomes part of the module's public surface \u2014 narrowly scoped because it returns only what the selector requests. currentAttachmentSet.ts can now import it as written."
    },
    {
      "id": "correctness",
      "resolution": "addressed",
      "reason": "Same as FLAG-017 \u2014 useSelectionStore is exported. Step 7.4's `import { useSelectionStore } from './selectionStore';` will compile."
    },
    {
      "id": "FLAG-018",
      "resolution": "addressed",
      "reason": "Step 9.3 explicitly references AgentChatMessage.tsx:180-226 (the AgentChatAttachmentStrip component) and spells out three concrete changes: (a) when isPlaceholder is true, render the chip slot with a loading state and DO NOT bind src to an empty url (avoids broken-image flash); (b) hide the X button on placeholders even when onRemoveAttachment is provided; (c) the chip slot reserves the same dimensions as a real chip. Step 14.2 (NEW) adds AgentChatMessage.test.tsx to the test list with explicit component-level assertions for the placeholder chip contract."
    },
    {
      "id": "all_locations",
      "resolution": "addressed",
      "reason": "Same as FLAG-018 \u2014 Step 14.2 names AgentChatMessage.test.tsx as a first-class test target. The component-level placeholder rendering contract is now locked by explicit test assertions, not implied."
    }
  ],
  "questions": [],
  "success_criteria": [
    {
      "criterion": "`npx tsc --noEmit` runs clean across the repository.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_build_output"
      ]
    },
    {
      "criterion": "`npx vitest run` passes the same set of tests as before plus the new tests added by this refactor; only the 3 documented pre-existing failures (GenerationsPane.test.tsx:209, dropdown-menu.test.tsx \u00d7 2) remain as known failures.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`npx eslint` is clean on every file touched by this refactor.",
      "priority": "must",
      "requires": [
        "run_linter"
      ]
    },
    {
      "criterion": "`src/shared/state/selectionStore.ts` exports the FULL intent command set (18 commands) + setTimelineClipData/clearTimelineClipData + __getSelectionStateForTests() + useSelectionStore (NEW in iter 6).",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "`src/shared/state/currentAttachmentSet.ts` imports useSelectionStore from './selectionStore' and compiles successfully (verified by tsc --noEmit clean).",
      "priority": "must",
      "requires": [
        "read_files",
        "run_shell"
      ]
    },
    {
      "criterion": "userSelectGalleryItem and userSelectGalleryItems do NOT mutate the timeline slice. Verified by unit test.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "userSelectTimelineClips({ additive: true }) (marquee) clears gallery AND APPENDS to timeline (never toggles individual clips). Verified by unit test.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "userSelectTimelineClip({ additive: true }) TOGGLES the clip on/off. Two-call test asserts both transitions and gallery clearing.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "userSelectTimelineClip({ additive: false, preserveIfSelected: true }) is a no-op when the clip is already selected. Verified by unit test.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "All editor-* intents preserve gallery. systemReset/Sync/Clear intents per their contracts. Verified by unit tests.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "composerRemoveAttachment matcher is CHIP-SPECIFIC: ALWAYS requires url+mediaType match on both surfaces. generationId narrows further (when provided); clipId narrows further timeline-side (when provided). Verified by unit tests covering: generationId+matching-url removes gallery/timeline entry; sibling-variant entries with same generationId but different URL are PRESERVED; no-generationId URL fallback removes; clipId disambiguator path.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "mergeSelectedClips merge key is `clip.clipId || clip.url` (NOT just clip.url). The corrected implementation is in src/shared/state/currentAttachmentSet.ts. Verified by reading the file.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "useCurrentAttachmentSet() emits a placeholder clip entry (isPlaceholder: true) for any selectedClipId without clipDataById data. Verified by unit test.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "TWO selected unknown clipIds produce TWO distinct placeholder entries (clips.length === 2). Verified by unit test \u2014 the merge-key collision fix. Without this fix, two placeholders with url: '' would collapse to one.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "useCurrentAttachmentSet() emits a dev-only console.warn when placeholders are present (NODE_ENV !== 'production'). Verified via vi.spyOn(console, 'warn').",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "When setTimelineClipData later supplies missing clip data, the next render returns the real clip with isPlaceholder undefined; dev-warn does not fire if all placeholders are now resolved. Partial resolution preserves remaining placeholders without collapsing chip count. Verified by unit test.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "Gallery items lacking clipId fall back to URL as the merge key, preserving the original timeline+gallery URL-collision merge behavior for steady-state cases. Verified by unit test (mixed gallery + timeline same URL).",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "useGallerySelection() and useTimelineSelectionStore() return state-only values; no mutation methods.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "useSelectionStoreApi() is deleted. No file imports it. Confirmed via `rg useSelectionStoreApi src/`.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files"
      ]
    },
    {
      "criterion": "useTimelineMultiSelect() drops selectClip/selectClips/addToSelection/clearSelection AND the syncOptions/clearGallery option.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "No file outside selectionStore.ts references the removed reducer names. Confirmed via rg.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files"
      ]
    },
    {
      "criterion": "The string `clearGallery` does not appear in any exported type/signature outside selectionStore.ts.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files"
      ]
    },
    {
      "criterion": "useTimelineCommit.ts imports editorSelectTimelineClip / editorClearTimelineSelection / editorSetSelectedTrackId; no useSelectionStoreApi or selectionStore.getState() calls.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "useTimelineState.ts no longer destructures mutation methods; timeline-id-change effect calls systemResetTimelineSelection().",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "useClipDrag.ts (lines 449, 459, 461, 463) calls userSelectTimelineClip with the documented additive/preserveIfSelected combinations \u2014 no direct selectClip calls remain.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "AppProviders.tsx no longer imports useSelectionStoreApi; project-change effect calls systemResetSelectionForProjectChange().",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "useLastAffectedShot.test.ts uses renderHook + __getSelectionStateForTests().",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "useGallerySelectionBridge.ts calls systemSyncGallerySelection / systemClearGallerySelection.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "src/shared/state/currentAttachmentSet.ts exists, exports useCurrentAttachmentSet() AND mergeSelectedClips, and AgentChat.tsx imports useCurrentAttachmentSet from it. mergeSelectedClips no longer in AgentChat.tsx.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "clipDataById is populated by useTimelineClipsForAttachments() and reflects ALL timeline clips' attachment data (not selection-derived).",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "AgentChatMessage.tsx (the AgentChatAttachmentStrip render surface, lines 180-226) renders placeholder chips with: (a) loading state visible, (b) NO `<img src=>` or `<video src=>` binding when isPlaceholder is true, (c) X button hidden when isPlaceholder is true. Real (non-placeholder) chips render normally with media binding and X button (when onRemoveAttachment provided). Verified by AgentChatMessage.test.tsx.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "The displayedClips 150ms grace window is removed from AgentChat.tsx.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "AgentChatContext.tsx no longer exposes timelineClips or replaceSelectedTimelineClips.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "currentAttachmentSet.test.tsx Test 1 (steady-state): asserts no flicker for setTimelineClipData-then-click flow.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "currentAttachmentSet.test.tsx Test 2 (additive marquee): gallery cleared + attachments {A, B} in same render.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "currentAttachmentSet.test.tsx Test 3 (single placeholder): clips.length \u2265 1 across all renders; one render contains an isPlaceholder chip with the correct clipId; dev-warn fires; convergence to real data after setTimelineClipData.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "currentAttachmentSet.test.tsx Test 4 (additive-toggle): two-call test asserts both transitions.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "currentAttachmentSet.test.tsx Test 5 (multi-placeholder merge-key fix): selects clipA AND clipB before any setTimelineClipData; asserts clips.length === 2 across the relevant renders (NOT 1, which would indicate a collision); each placeholder has its distinct clipId; partial setTimelineClipData([clipAData]) keeps clips.length === 2 (clipA real, clipB placeholder); full setTimelineClipData resolves both.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "AgentChatMessage.test.tsx exists and includes assertions for: (a) placeholder chip renders loading state without media src binding; (b) placeholder chip hides the X button even when onRemoveAttachment provided; (c) non-placeholder chip renders normally with media binding and X button.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "useModifierKeys.ts AND its test file are deleted; no remaining file imports useModifierKeys.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files"
      ]
    },
    {
      "criterion": "src/shared/lib/interactions/selectionGesture.ts exists and is used by MediaGalleryItem.tsx, useItemInteraction.ts, useLassoSelection.ts, GenerationsPaneGallery.tsx, ImageGenerationToolPage.tsx.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "AgentChat.test.tsx, VideoEditorProvider.test.tsx, AppProviders.test.tsx, GenerationsPaneGallery.test.tsx, AgentChatMessage.test.tsx mocks/assertions are updated. VideoEditorProvider.test.tsx uses __getSelectionStateForTests() for state reads.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "Pre-existing point-fixes that this refactor does NOT supersede (wrapper-level pointerdown/up, onImageClick(image, modifiers) signature, fetchWithTimeout 4xx logger, AgentChat 'Clear' button) remain in place.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Working tree contains uncommitted changes \u2014 no commits were created during execution.",
      "priority": "must",
      "requires": [
        "run_shell"
      ]
    },
    {
      "criterion": "Each new file (currentAttachmentSet.ts, selectionGesture.ts, useTimelineClipsForAttachments.ts) stays under ~250 LOC. selectionStore.ts grows but stays under ~1100 LOC.",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Manual smoke (user-driven): Cmd+click in gallery still multi-selects; click on timeline still clears gallery; Cmd+click on selected timeline clip toggles off; marquee in timeline appends; drag-to-shot still works; agent-chat attachment removal works on /tools/video-editor AND /shots/art routes; project-change resets selection; timeline-id change resets timeline.",
      "priority": "info",
      "requires": [
        "inspect_runtime_ui"
      ]
    },
    {
      "criterion": "Manual smoke (user-driven): the agent-chat attachment strip does not flicker between gallery-only \u2192 timeline-only transitions. Placeholder chips appear briefly during sync gap (visible loading state); chip count never drops to zero NOR collapses (multiple placeholders stay distinct).",
      "priority": "info",
      "requires": [
        "inspect_runtime_ui"
      ]
    },
    {
      "criterion": "Manual smoke (user-driven): removing one attachment chip removes only that chip's url+mediaType+(optional generationId/clipId) match \u2014 sibling variants from same generationId with different URLs are NOT removed (chip-specific behavior preserved).",
      "priority": "info",
      "requires": [
        "inspect_runtime_ui"
      ]
    }
  ],
  "assumptions": [
    "mergeSelectedClips merge key is `clip.clipId || clip.url`. Timeline clips always have clipId (so they key on clipId, even when their URL collides with a gallery item \u2014 the existing AgentChat.tsx URL collision case is rare in practice and the new key still merges them when both come from the same generation via the gallery-prefer-incoming logic). Gallery items always have URL (no clipId), so they key on URL \u2014 preserving the original timeline+gallery URL-collision merge for steady-state cases. Placeholders get unique clipId-keyed slots, fixing the multi-placeholder collision.",
    "useSelectionStore is exported from selectionStore.ts. The export is narrowly scoped \u2014 it returns whatever selector the caller passes \u2014 and the existing state-only convenience hooks (useGallerySelection, useTimelineSelectionStore) remain the preferred public surface. currentAttachmentSet.ts is the legitimate consumer.",
    "AgentChatMessage.tsx:180-226 (the AgentChatAttachmentStrip component) is the actual chip render surface. Step 9.3 changes that file directly. AgentChat.tsx remains the higher-level panel that consumes AgentChatAttachmentStrip and wires up handleRemoveAttachment; both files are touched in Step 9.",
    "AgentChatMessage.test.tsx is a first-class test target locking the placeholder chip rendering contract: loading state, no media src binding, no X button.",
    "All settled decisions from iter 2-5 (intent layer in selectionStore.ts; clipDataById slice; chip-specific composerRemoveAttachment matcher; additive=toggle for single-clip, append for marquee; placeholders for impossible-by-construction empty render; useTimelineMultiSelect trimmed; useSelectionStoreApi deleted) remain unchanged.",
    "The 3 pre-existing test failures remain known failures.",
    "No commits during execution."
  ],
  "delta_from_previous_percent": 89.86,
  "structure_warnings": [
    "Each step section should include at least one numbered substep."
  ]
}

        Gate summary:
        {
  "passed": true,
  "criteria_check": {
    "count": 48,
    "items": [
      {
        "criterion": "`npx tsc --noEmit` runs clean across the repository.",
        "priority": "must",
        "requires": [
          "run_shell",
          "read_build_output"
        ]
      },
      {
        "criterion": "`npx vitest run` passes the same set of tests as before plus the new tests added by this refactor; only the 3 documented pre-existing failures (GenerationsPane.test.tsx:209, dropdown-menu.test.tsx \u00d7 2) remain as known failures.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "`npx eslint` is clean on every file touched by this refactor.",
        "priority": "must",
        "requires": [
          "run_linter"
        ]
      },
      {
        "criterion": "`src/shared/state/selectionStore.ts` exports the FULL intent command set (18 commands) + setTimelineClipData/clearTimelineClipData + __getSelectionStateForTests() + useSelectionStore (NEW in iter 6).",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "`src/shared/state/currentAttachmentSet.ts` imports useSelectionStore from './selectionStore' and compiles successfully (verified by tsc --noEmit clean).",
        "priority": "must",
        "requires": [
          "read_files",
          "run_shell"
        ]
      },
      {
        "criterion": "userSelectGalleryItem and userSelectGalleryItems do NOT mutate the timeline slice. Verified by unit test.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "userSelectTimelineClips({ additive: true }) (marquee) clears gallery AND APPENDS to timeline (never toggles individual clips). Verified by unit test.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "userSelectTimelineClip({ additive: true }) TOGGLES the clip on/off. Two-call test asserts both transitions and gallery clearing.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "userSelectTimelineClip({ additive: false, preserveIfSelected: true }) is a no-op when the clip is already selected. Verified by unit test.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "All editor-* intents preserve gallery. systemReset/Sync/Clear intents per their contracts. Verified by unit tests.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "composerRemoveAttachment matcher is CHIP-SPECIFIC: ALWAYS requires url+mediaType match on both surfaces. generationId narrows further (when provided); clipId narrows further timeline-side (when provided). Verified by unit tests covering: generationId+matching-url removes gallery/timeline entry; sibling-variant entries with same generationId but different URL are PRESERVED; no-generationId URL fallback removes; clipId disambiguator path.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "mergeSelectedClips merge key is `clip.clipId || clip.url` (NOT just clip.url). The corrected implementation is in src/shared/state/currentAttachmentSet.ts. Verified by reading the file.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "useCurrentAttachmentSet() emits a placeholder clip entry (isPlaceholder: true) for any selectedClipId without clipDataById data. Verified by unit test.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "TWO selected unknown clipIds produce TWO distinct placeholder entries (clips.length === 2). Verified by unit test \u2014 the merge-key collision fix. Without this fix, two placeholders with url: '' would collapse to one.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "useCurrentAttachmentSet() emits a dev-only console.warn when placeholders are present (NODE_ENV !== 'production'). Verified via vi.spyOn(console, 'warn').",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "When setTimelineClipData later supplies missing clip data, the next render returns the real clip with isPlaceholder undefined; dev-warn does not fire if all placeholders are now resolved. Partial resolution preserves remaining placeholders without collapsing chip count. Verified by unit test.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "Gallery items lacking clipId fall back to URL as the merge key, preserving the original timeline+gallery URL-collision merge behavior for steady-state cases. Verified by unit test (mixed gallery + timeline same URL).",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "useGallerySelection() and useTimelineSelectionStore() return state-only values; no mutation methods.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "useSelectionStoreApi() is deleted. No file imports it. Confirmed via `rg useSelectionStoreApi src/`.",
        "priority": "must",
        "requires": [
          "run_shell",
          "read_files"
        ]
      },
      {
        "criterion": "useTimelineMultiSelect() drops selectClip/selectClips/addToSelection/clearSelection AND the syncOptions/clearGallery option.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "No file outside selectionStore.ts references the removed reducer names. Confirmed via rg.",
        "priority": "must",
        "requires": [
          "run_shell",
          "read_files"
        ]
      },
      {
        "criterion": "The string `clearGallery` does not appear in any exported type/signature outside selectionStore.ts.",
        "priority": "must",
        "requires": [
          "run_shell",
          "read_files"
        ]
      },
      {
        "criterion": "useTimelineCommit.ts imports editorSelectTimelineClip / editorClearTimelineSelection / editorSetSelectedTrackId; no useSelectionStoreApi or selectionStore.getState() calls.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "useTimelineState.ts no longer destructures mutation methods; timeline-id-change effect calls systemResetTimelineSelection().",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "useClipDrag.ts (lines 449, 459, 461, 463) calls userSelectTimelineClip with the documented additive/preserveIfSelected combinations \u2014 no direct selectClip calls remain.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "AppProviders.tsx no longer imports useSelectionStoreApi; project-change effect calls systemResetSelectionForProjectChange().",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "useLastAffectedShot.test.ts uses renderHook + __getSelectionStateForTests().",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "useGallerySelectionBridge.ts calls systemSyncGallerySelection / systemClearGallerySelection.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "src/shared/state/currentAttachmentSet.ts exists, exports useCurrentAttachmentSet() AND mergeSelectedClips, and AgentChat.tsx imports useCurrentAttachmentSet from it. mergeSelectedClips no longer in AgentChat.tsx.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "clipDataById is populated by useTimelineClipsForAttachments() and reflects ALL timeline clips' attachment data (not selection-derived).",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "AgentChatMessage.tsx (the AgentChatAttachmentStrip render surface, lines 180-226) renders placeholder chips with: (a) loading state visible, (b) NO `<img src=>` or `<video src=>` binding when isPlaceholder is true, (c) X button hidden when isPlaceholder is true. Real (non-placeholder) chips render normally with media binding and X button (when onRemoveAttachment provided). Verified by AgentChatMessage.test.tsx.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "The displayedClips 150ms grace window is removed from AgentChat.tsx.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "AgentChatContext.tsx no longer exposes timelineClips or replaceSelectedTimelineClips.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "currentAttachmentSet.test.tsx Test 1 (steady-state): asserts no flicker for setTimelineClipData-then-click flow.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "currentAttachmentSet.test.tsx Test 2 (additive marquee): gallery cleared + attachments {A, B} in same render.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "currentAttachmentSet.test.tsx Test 3 (single placeholder): clips.length \u2265 1 across all renders; one render contains an isPlaceholder chip with the correct clipId; dev-warn fires; convergence to real data after setTimelineClipData.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "currentAttachmentSet.test.tsx Test 4 (additive-toggle): two-call test asserts both transitions.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "currentAttachmentSet.test.tsx Test 5 (multi-placeholder merge-key fix): selects clipA AND clipB before any setTimelineClipData; asserts clips.length === 2 across the relevant renders (NOT 1, which would indicate a collision); each placeholder has its distinct clipId; partial setTimelineClipData([clipAData]) keeps clips.length === 2 (clipA real, clipB placeholder); full setTimelineClipData resolves both.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "AgentChatMessage.test.tsx exists and includes assertions for: (a) placeholder chip renders loading state without media src binding; (b) placeholder chip hides the X button even when onRemoveAttachment provided; (c) non-placeholder chip renders normally with media binding and X button.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "useModifierKeys.ts AND its test file are deleted; no remaining file imports useModifierKeys.",
        "priority": "must",
        "requires": [
          "run_shell",
          "read_files"
        ]
      },
      {
        "criterion": "src/shared/lib/interactions/selectionGesture.ts exists and is used by MediaGalleryItem.tsx, useItemInteraction.ts, useLassoSelection.ts, GenerationsPaneGallery.tsx, ImageGenerationToolPage.tsx.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "AgentChat.test.tsx, VideoEditorProvider.test.tsx, AppProviders.test.tsx, GenerationsPaneGallery.test.tsx, AgentChatMessage.test.tsx mocks/assertions are updated. VideoEditorProvider.test.tsx uses __getSelectionStateForTests() for state reads.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "Pre-existing point-fixes that this refactor does NOT supersede (wrapper-level pointerdown/up, onImageClick(image, modifiers) signature, fetchWithTimeout 4xx logger, AgentChat 'Clear' button) remain in place.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "Working tree contains uncommitted changes \u2014 no commits were created during execution.",
        "priority": "must",
        "requires": [
          "run_shell"
        ]
      },
      {
        "criterion": "Each new file (currentAttachmentSet.ts, selectionGesture.ts, useTimelineClipsForAttachments.ts) stays under ~250 LOC. selectionStore.ts grows but stays under ~1100 LOC.",
        "priority": "should",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Manual smoke (user-driven): Cmd+click in gallery still multi-selects; click on timeline still clears gallery; Cmd+click on selected timeline clip toggles off; marquee in timeline appends; drag-to-shot still works; agent-chat attachment removal works on /tools/video-editor AND /shots/art routes; project-change resets selection; timeline-id change resets timeline.",
        "priority": "info",
        "requires": [
          "inspect_runtime_ui"
        ]
      },
      {
        "criterion": "Manual smoke (user-driven): the agent-chat attachment strip does not flicker between gallery-only \u2192 timeline-only transitions. Placeholder chips appear briefly during sync gap (visible loading state); chip count never drops to zero NOR collapses (multiple placeholders stay distinct).",
        "priority": "info",
        "requires": [
          "inspect_runtime_ui"
        ]
      },
      {
        "criterion": "Manual smoke (user-driven): removing one attachment chip removes only that chip's url+mediaType+(optional generationId/clipId) match \u2014 sibling variants from same generationId with different URLs are NOT removed (chip-specific behavior preserved).",
        "priority": "info",
        "requires": [
          "inspect_runtime_ui"
        ]
      }
    ]
  },
  "preflight_results": {
    "project_dir_exists": true,
    "project_dir_writable": true,
    "success_criteria_present": true,
    "claude_available": true,
    "codex_available": true
  },
  "unresolved_flags": [
    {
      "id": "correctness-1",
      "concern": "Are the proposed changes technically correct?: Checked Step 7.4's dev-only warning guard against the repo's frontend environment conventions. The plan sketch uses `process.env.NODE_ENV !== 'production'`, but this Vite React app uses `import.meta.env.DEV` throughout `src/`; unless `process` is separately defined in the browser bundle, that selector path can throw a `ReferenceError` when placeholders are emitted.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Checked Step 7.4's dev-only warning guard against the repo's frontend environment conventions. The plan sketch uses `process.env.NODE_ENV !== 'production'`, but this Vite React app uses `import.meta.env.DEV` throughout `src/`; unless `process` is separately defined in the browser bundle, that selector path can throw a `ReferenceError` when placeholders are emitted.",
      "raised_in": "critique_v6.json",
      "status": "open",
      "severity": "significant",
      "verified": true,
      "addressed_in": "plan_v5.md",
      "verified_in": "critique_v5.json"
    },
    {
      "id": "correctness-2",
      "concern": "Are the proposed changes technically correct?: Checked the proposed `useSelectionStore` export against the intent-facade requirement. Exporting the raw Zustand selector hook makes every field in `SelectionStoreState` selectable, including the low-level reducer functions that Step 5 intends to remove from public hooks, so it technically reopens the public low-level mutation surface rather than making the intent commands the only reachable API.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Checked the proposed `useSelectionStore` export against the intent-facade requirement. Exporting the raw Zustand selector hook makes every field in `SelectionStoreState` selectable, including the low-level reducer functions that Step 5 intends to remove from public hooks, so it technically reopens the public low-level mutation surface rather than making the intent commands the only reachable API.",
      "raised_in": "critique_v6.json",
      "status": "open",
      "severity": "significant",
      "verified": true,
      "addressed_in": "plan_v5.md",
      "verified_in": "critique_v5.json"
    },
    {
      "id": "scope",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Checked the planned merge-key test (Step 7.7f) against actual gallery clip construction. The plan says gallery items lack `clipId` and therefore fall back to URL, but the store always assigns `clipId` to gallery clips; a test that fabricates a gallery clip without `clipId` would not exercise the real `selectedGalleryClips` path and could pass while the app shows duplicate timeline/gallery chips.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Checked the planned merge-key test (Step 7.7f) against actual gallery clip construction. The plan says gallery items lack `clipId` and therefore fall back to URL, but the store always assigns `clipId` to gallery clips; a test that fabricates a gallery clip without `clipId` would not exercise the real `selectedGalleryClips` path and could pass while the app shows duplicate timeline/gallery chips.",
      "raised_in": "critique_v6.json",
      "status": "open",
      "severity": "significant",
      "verified": true,
      "addressed_in": "plan_v6.md",
      "verified_in": "critique_v6.json"
    },
    {
      "id": "issue_hints",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the new `clip.clipId || clip.url` merge-key assumption against `selectionStore.ts:249-256` and `SelectedMediaClip` in `useSelectedMediaClips.ts:6-19`. Gallery selections are converted into `SelectedMediaClip` objects with `clipId: id`, so they do not lack `clipId`; the revised key therefore stops deduping a gallery item and timeline clip that share the same URL, which the existing `AgentChat.tsx:40-75` URL-keyed merge intentionally did.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Checked the new `clip.clipId || clip.url` merge-key assumption against `selectionStore.ts:249-256` and `SelectedMediaClip` in `useSelectedMediaClips.ts:6-19`. Gallery selections are converted into `SelectedMediaClip` objects with `clipId: id`, so they do not lack `clipId`; the revised key therefore stops deduping a gallery item and timeline clip that share the same URL, which the existing `AgentChat.tsx:40-75` URL-keyed merge intentionally did.",
      "raised_in": "critique_v6.json",
      "status": "open",
      "severity": "significant",
      "verified": true,
      "addressed_in": "plan_v6.md",
      "verified_in": "critique_v5.json"
    },
    {
      "id": "correctness",
      "concern": "Are the proposed changes technically correct?: Checked Step 7.4's proposed `currentAttachmentSet.ts` import against `selectionStore.ts:690-699`. `useSelectionStore` is currently a private non-exported function, while the plan creates a separate module that imports it from `./selectionStore`; followed literally, that new file will not compile unless the plan either exports a deliberately narrow selector API or colocates `useCurrentAttachmentSet()` inside `selectionStore.ts`.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Iter-6 closes the three remaining iter-5 placeholder-design gaps. (1) FLAG-016/issue_hints/scope: mergeSelectedClips is now keyed by `clipId || url` instead of `url`. The corrected implementation is spelled out in Step 7.4 with an inline comment marking the change. Step 10 Test 5 (NEW) directly verifies that two selected-but-unknown clipIds produce two distinct placeholder chips and never collapse \u2014 locking the merge-key contract. Step 7.7 adds three additional unit tests for the merge-key behavior (single placeholder, two placeholders, gallery URL fallback for gallery items lacking clipId). (2) FLAG-017/correctness: useSelectionStore is now explicitly exported from selectionStore.ts (Step 2.3) so currentAttachmentSet.ts can import it. The export is intentionally narrow \u2014 it returns whatever the selector requests, and the existing state-only hooks remain the preferred public surface. (3) FLAG-018/all_locations: Step 9.3 now names the actual chip render surface \u2014 AgentChatMessage.tsx:180-226 (the AgentChatAttachmentStrip component) \u2014 with concrete behavior changes for placeholder rendering: chip slot reserves space, no img/video src binding (avoids broken-image flash from url: ''), no X button. Step 14.2 (NEW) adds AgentChatMessage.test.tsx to the test list with explicit assertions for the placeholder chip contract (loading state, no media binding, no X button) and the non-placeholder fallback (normal media rendering, X button when onRemoveAttachment provided). All settled decisions from iter 2-5 are preserved unchanged.",
      "raised_in": "critique_v5.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v6.md"
    },
    {
      "id": "callers",
      "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked the actual attachment merge callers: `AgentChat.tsx` currently passes timeline clips from `useSelectedMediaClips()` and gallery clips from `useGallerySelection().selectedGalleryClips` into the merge. Because both caller paths supply `clipId`, a `clipId || url` key handles placeholder timeline clips but no longer matches the real gallery-vs-timeline same-URL caller case that the old URL-keyed merge handled.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Checked the actual attachment merge callers: `AgentChat.tsx` currently passes timeline clips from `useSelectedMediaClips()` and gallery clips from `useGallerySelection().selectedGalleryClips` into the merge. Because both caller paths supply `clipId`, a `clipId || url` key handles placeholder timeline clips but no longer matches the real gallery-vs-timeline same-URL caller case that the old URL-keyed merge handled.",
      "raised_in": "critique_v6.json",
      "status": "open",
      "severity": "significant",
      "verified": true,
      "addressed_in": "plan_v5.md",
      "verified_in": "critique_v5.json"
    },
    {
      "id": "FLAG-019",
      "concern": "Attachment merge key: `clip.clipId || clip.url` fixes placeholder collisions but breaks the existing URL dedupe between timeline and gallery attachments because gallery clips already have `clipId`.",
      "category": "correctness",
      "severity_hint": "uncertain",
      "evidence": "`buildGalleryState()` in `src/shared/state/selectionStore.ts` maps every gallery entry to `SelectedMediaClip` with `clipId: id`, and `SelectedMediaClip` declares `clipId` as required. The current `AgentChat.tsx` merge dedupes by `clip.url` specifically to collapse a timeline clip and gallery item for the same media URL while preserving richer generation metadata. The plan's fallback test for gallery items lacking `clipId` does not match the real store path.",
      "raised_in": "critique_v6.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "FLAG-020",
      "concern": "Selection store public surface: exporting the raw `useSelectionStore` hook re-exposes low-level Zustand reducer functions despite the intent-facade goal.",
      "category": "maintainability",
      "severity_hint": "uncertain",
      "evidence": "`selectionStore.ts` currently keeps low-level mutations such as `selectGalleryItem`, `selectTimelineClip`, and `clearTimelineSelection` inside `SelectionStoreState`. If `useSelectionStore` is exported, external code can select those methods directly even after `useGallerySelection()` and `useTimelineSelectionStore()` are trimmed. A narrower helper or colocating `useCurrentAttachmentSet()` would preserve the facade better.",
      "raised_in": "critique_v6.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "FLAG-021",
      "concern": "Frontend environment guard: the planned placeholder warning uses `process.env.NODE_ENV` in a Vite browser module, while the repo uses `import.meta.env.DEV`.",
      "category": "correctness",
      "severity_hint": "uncertain",
      "evidence": "The Step 7.4 sketch calls `process.env.NODE_ENV !== 'production'` inside `currentAttachmentSet.ts`. A repo search shows frontend dev gates use `import.meta.env.DEV`/`import.meta.env.MODE`, and no `process.env.NODE_ENV` usage under `src/`; without a browser `process` shim, emitting a placeholder can throw before returning attachments.",
      "raised_in": "critique_v6.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    }
  ],
  "recommendation": "PROCEED",
  "rationale": "User decisions provided in notes for gate iter 6 escalation issues (env guard, merge key, facade colocation). Proceeding to revise iter 7 with delegated approval.",
  "signals_assessment": "Forced proceed override applied by the orchestrator.",
  "warnings": [
    "Iteration 6: high iteration count.",
    "Iteration 6: high iteration count."
  ],
  "settled_decisions": [],
  "override_forced": true,
  "orchestrator_guidance": "Force-proceed override applied. Proceed to finalize.",
  "robustness": "standard",
  "signals": {
    "iteration": 6,
    "idea": "# Selection / Coordination Architecture Refactor\n\n## Background\n\nOver a long session of bug-chasing in the selection / agent-chat surface area, the user has repeatedly hit related-but-distinct bugs that all root in the same architectural choice: **the current code exposes low-level state mutations (`selectTimelineClip(id, opts, { clearGallery })`, raw context bridges, racy global modifier state) when the domain operates at a higher level (`user clicked timeline \u2192 clear gallery; agent chat replaced attachments \u2192 preserve gallery`)**.\n\nA Codex 5.5 architectural review confirmed this read and proposed three concrete pieces of refactoring. This megaplan executes those three pieces (#1, #2, #3 from the Codex proposal). Piece #4 (PostgREST filter helper) is OUT OF SCOPE for this run.\n\n## What we've already point-fixed in the current session (DO NOT REVERT)\n\nThese are uncommitted changes in the working tree on branch `megaplan/m1b-m1c-stores`. Build on top of them; do not undo.\n\n- `src/shared/state/selectionStore.ts` \u2014 `useTimelineMultiSelect` wrapper (lines ~803-820) now passes `syncOptions` through instead of hardcoding `clearGallery: false`. Default behavior matches the underlying store (clear gallery on timeline selection).\n- `src/tools/video-editor/contexts/VideoEditorProvider.tsx` \u2014 `AgentChatBridgeRegistration.stableReplace` now passes `{ clearGallery: false }` explicitly to preserve gallery on agent-chat-driven attachment edits. Effect deps now include `timelineClips` (the previous getter pattern was broken).\n- `src/tools/video-editor/components/AgentChat/AgentChat.tsx` \u2014 added a `displayedClips` 150ms-grace-window state to absorb the bridge's one-commit lag (the flicker fix). Added a \"Clear\" button next to the attachment summary when `clips.length > 1`.\n- `src/shared/components/MediaGalleryItem.tsx` \u2014 added `handleWrapperPointerDown`/`handleWrapperPointerUp` for desktop click detection with an 8px movement threshold (HTML5 drag preempts native click).\n- `src/shared/components/MediaGalleryItem/components/{ImageContent,VideoContent}.tsx` \u2014 removed `onClick` from inner img/video elements (now handled by wrapper).\n- `src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts` \u2014 `onImageClick` signature now accepts `(image, modifiers?: { multiSelect: boolean })`; mobile touch path forwards modifiers from the event.\n- `src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx` \u2014 `handleImageClick` reads modifiers from the event-derived `modifiers` arg, with a fallback to `useModifierKeys` (the racy hook is still imported but no longer authoritative).\n- `src/integrations/supabase/bootstrap/fetchWithTimeout.ts` \u2014 added a 4xx response-body logger that probes HEAD requests with a follow-up GET to extract the diagnostic body.\n\nThese point-fixes work but are band-aids on top of the structural issues this megaplan addresses. The refactor should make several of them redundant (the `displayedClips` grace window, the `useModifierKeys` fallback, the manual remove-from-both-surfaces logic in AgentChat).\n\n## Target architecture (three pieces)\n\n### Piece 1: Intent-based selection facade\n\n**File:** add `src/shared/state/selectionActions.ts` OR fold into `src/shared/state/selectionStore.ts` as a new export section. Whichever keeps the diff smaller and more navigable.\n\n**Replace the public selection API.** Today the public API exposes:\n- `selectTimelineClip(id, opts, syncOptions)` (with `clearGallery` flag)\n- `selectTimelineClips(clipIds, syncOptions)`\n- `selectGalleryItem(id, meta, options)` (with `toggle` flag)\n- `selectGalleryItems(items, options)` (with `append` flag)\n- `clearGallerySelection()`\n- `clearTimelineSelection(syncOptions)`\n- `deselectGalleryItems(ids)`\n\n**With named-by-intent commands** that encode WHO is acting (user, composer, system, editor):\n\n- `userSelectGalleryItem(item, opts: { additive: boolean })` \u2014 user clicked a gallery item. Replaces selection unless additive. Does NOT touch timeline selection.\n- `userSelectGalleryItems(items, opts: { additive: boolean })` \u2014 marquee/lasso in gallery.\n- `userSelectTimelineClip(clipId, opts: { additive, preserveIfSelected? })` \u2014 user clicked a clip in the timeline. **Clears gallery selection** (the policy that was scattered as `clearGallery: true` defaults).\n- `userSelectTimelineClips(clipIds, opts: { additive })` \u2014 marquee in timeline. **Clears gallery selection**.\n- `userClearAllSelection()` \u2014 explicit \"clear everything\" intent.\n- `composerRemoveAttachment(match: { url, mediaType, generationId? })` \u2014 agent chat removed a chip. Removes from BOTH surfaces (one match identifier, the composer figures out which surface(s) to update). **Does NOT clear other selections.**\n- `composerClearAttachments()` \u2014 agent chat \"Clear\" button. Clears both surfaces. (User intent is explicit clear.)\n- `editorReplaceTimelineSelection(clipIds)` \u2014 editor-internal mutation (e.g., select after paste/duplicate). **Preserves gallery.**\n- `systemPruneTimelineSelection(validIds)` \u2014 drops selected clip ids that are no longer in the timeline data (after a clip is deleted, etc.). **Preserves gallery.**\n\n**Keep the existing low-level reducers** (`selectTimelineClip`, `selectTimelineClips`, `selectGalleryItem`, etc.) but **make them private to the store module** \u2014 not exported, or marked internal in a way the rest of the codebase can't reach. The intent commands are the only public surface.\n\n**Migrate every call site** that currently uses the low-level API to call the appropriate intent command. Rough mapping:\n- `useClipDrag.helpers.ts` calls of `selectClip`/`selectClips` \u2192 `userSelectTimelineClip`/`userSelectTimelineClips` (drag interactions are user-initiated).\n- `useMarqueeSelect.ts:203` \u2192 `userSelectTimelineClips` (additive: false, since marquee replaces).\n- `TimelineEditor.tsx:427` \u2192 `userSelectTimelineClip`.\n- `PreviewPanel.tsx:138` \u2192 `userSelectTimelineClip`.\n- `VideoEditorShell.tsx:147` (selectAllClips) \u2192 `editorReplaceTimelineSelection` (system-initiated keyboard shortcut, should NOT clear gallery).\n- `VideoEditorProvider.tsx:90` (`stableReplace` for agent chat bridge) \u2192 `editorReplaceTimelineSelection`.\n- `GenerationsPaneGallery.tsx:99` (handleImageClick) \u2192 `userSelectGalleryItem`.\n- `GenerationsPaneGallery.tsx:88,144` \u2192 similar.\n- `useLassoSelection`'s `onSelectItems` consumer \u2192 `userSelectGalleryItems`.\n\n**Remove `clearGallery` from the public surface.** It's a leaked implementation detail.\n\n**Do NOT rewrite the underlying Zustand reducers.** Keep them. The intent layer is the new public API, the reducers stay internal.\n\nCodex estimate: 250-450 LOC, 4-8 files touched.\n\n### Piece 2: Single current-attachment composer + sync bridge\n\n**Files:**\n- Add `src/shared/state/currentAttachmentSet.ts` (the composer).\n- Modify `src/shared/contexts/AgentChatContext.tsx` (the bridge becomes thinner \u2014 see below).\n- Modify `src/tools/video-editor/contexts/VideoEditorProvider.tsx` (registration becomes a Zustand write, not a context push).\n- Modify `src/tools/video-editor/components/AgentChat/AgentChat.tsx` (consumes the composer, drops the manual merge + the `displayedClips` grace window).\n\n**Move the merge/dedupe logic out of AgentChatPanel.** Today `AgentChat.tsx:181` does `mergeSelectedClips(timelineClips, selectedGalleryClips)` inside the panel. Move `mergeSelectedClips` (currently at `AgentChat.tsx:40`) into `currentAttachmentSet.ts`. The panel should call ONE hook: `useCurrentAttachmentSet()` that returns the merged `clips` and `summary`.\n\n**Replace the React-context bridge for timeline attachments with a synchronous Zustand write.** The current bridge pattern is:\n\n```\nuseSelectedMediaClips \u2192 register({ timelineClips }) \u2192 useState setOverride \u2192 context value \u2192 consumer re-render\n```\n\nThat's an async hop (one React commit late) and is the cause of the flicker even after my point-fix. Replace with:\n\n```\nuseSelectedMediaClips \u2192 set timelineAttachments slice in Zustand \u2192 useCurrentAttachmentSet subscribes synchronously\n```\n\nSpecifically: add a `timelineAttachments` slice (or similar) to the existing Zustand selection store (or a new store) that holds the structured timeline clip data the chat panel needs. `VideoEditorProvider` writes to it on every change of `useSelectedMediaClips()` via a `useEffect` that calls a setter, but consumers READ it via a Zustand selector \u2014 no more React-context useState bridge for this data.\n\n**Remove the `displayedClips` 150ms grace window from AgentChatPanel.** Once timeline attachments propagate synchronously, the flicker is impossible by construction and the band-aid is unnecessary. Delete it.\n\n**Keep the bridge for non-attachment data.** `AgentChatContext` still has `timelineId`, the actions registry (markEngaged/toggleRecording/focusComposer), and `replaceSelectedTimelineClips` (which becomes a thin wrapper calling `composerRemoveAttachment`/`editorReplaceTimelineSelection`). Don't delete the bridge entirely \u2014 just stop using it for the data that flickers.\n\n**`AgentChatPanel.handleRemoveAttachment` becomes a one-liner.** Today it manually edits both `timelineClips` (via `replaceSelectedTimelineClips`) and gallery (via `deselectGalleryMatches`). Replace with `composerRemoveAttachment(match)` \u2014 the composer/intent layer handles both surfaces.\n\nCodex estimate: 300-600 LOC, 5-10 files touched.\n\n### Piece 3: Shared gesture primitives\n\n**File:** add `src/shared/interactions/selectionGesture.ts` (or `src/shared/lib/interactions/selectionGesture.ts` \u2014 pick whichever fits the existing layout).\n\n**Functions to export:**\n- `isAdditiveSelectionEvent(event: { metaKey, ctrlKey, shiftKey })` \u2014 returns true if Cmd/Ctrl/Shift held. Read from event, NOT from React state. (Already exists inline in `useLassoSelection.ts:37` \u2014 promote it.)\n- `isPrimaryPointer(event: PointerEvent | MouseEvent)` \u2014 returns true if `event.button === 0` (left click).\n- `isClickLikePointerGesture(start: { x, y }, end: { x, y }, threshold = 8)` \u2014 returns true if movement under threshold (the wrapper-level click detection logic from `MediaGalleryItem.tsx`).\n- Optionally a hook `usePointerClickIntent({ onClick, threshold })` that wraps the pointerdown/pointerup pattern with movement tracking, but only if the call sites collapse cleanly. Don't force it.\n\n**Migrate call sites:**\n- `useModifierKeys.ts` \u2014 **DELETE the file entirely.** Update `GenerationsPaneGallery.tsx` to drop the import and the `useModifierKeys()` fallback (now unnecessary since the click handler reads from event). Update `ImageGenerationToolPage.tsx` to use `isAdditiveSelectionEvent` from the new module instead.\n- `useLassoSelection.ts:37,140` \u2014 replace inline `isMultiSelectEvent` with the shared `isAdditiveSelectionEvent`.\n- `MediaGalleryItem.tsx` \u2014 replace inline `CLICK_THRESHOLD_PX` and the pointerdown/up dance with `isClickLikePointerGesture` (or `usePointerClickIntent` if it lands well).\n- `useItemInteraction.ts` \u2014 same \u2014 its inline modifier-derivation can use `isAdditiveSelectionEvent`.\n\n**Keep the gesture primitives small and stateless.** No framework. Just functions and (at most) one hook. They should compose with existing event handlers, not replace them.\n\nCodex estimate: 150-300 LOC, 4-6 files touched.\n\n## Out of scope (do not do in this run)\n\n- **Do NOT rewrite the underlying Zustand reducers.** They're fine. We're changing only the public API.\n- **Do NOT decouple AgentChatPanel from `@/tools/video-editor/hooks/...` imports.** That's a separate, larger refactor. The panel staying coupled to video-editor for now is acceptable.\n- **Do NOT touch the PostgREST `or=` accumulator.** That's Codex's piece #4. We can fold that helper into a follow-up. The current implementation in `useProjectGenerations.ts:71` is correct, just not extracted yet.\n- **Do NOT touch the WIP code on this branch** outside the selection/coordination surface: drop-to-generation, local media resolver, generations storage migration, video-editor effect compilation, etc. These are independent and not yours to fix.\n- **Do NOT touch the 3 pre-existing test failures**: `GenerationsPane.test.tsx:209` (drop-to-generation) and `dropdown-menu.test.tsx` \u00d7 2. They've failed since the WIP commit `be3c5e21` and are tracked separately.\n- **Do NOT change visual styling**, the action-pane layout, or the agent chat panel's UX. The user has been polishing those by hand. Leave the UI behavior unchanged.\n\n## Constraints\n\n- **Working tree is dirty** with the point-fixes listed above. Keep them. Build the refactor on top of the current state. Don't commit anything during execution \u2014 leave changes uncommitted in the working tree for the user to review.\n- **Branch:** `megaplan/m1b-m1c-stores`. Don't rebase, don't push.\n- **Tests must continue to pass** at the same rate or better. The 3 pre-existing failures stay; everything else must stay green.\n- **Type-check must pass.** `npx tsc --noEmit` clean.\n- **Lint must pass on touched files.**\n\n## Validation\n\n- `npx tsc --noEmit` \u2014 clean.\n- `npx eslint <touched files>` \u2014 clean.\n- `npx vitest run` \u2014 same set passing as before plus any new tests added by this refactor. The 3 pre-existing failures (`GenerationsPane.test.tsx:209`, `dropdown-menu.test.tsx` \u00d7 2) remain known failures.\n- **Add new tests for the intent layer.** Each `userSelect*` / `composer*` / `editor*` / `system*` command should have a unit test asserting cross-surface behavior (specifically: which surfaces it updates, which it preserves).\n- **Add a regression test for the flicker.** A test that simulates \"gallery selected \u2192 click timeline \u2192 check that the chat's clips collection never goes through an empty state in any render.\" Probably needs `useSyncExternalStore` mocking or careful render-counting.\n- **Manual smoke: confirm the existing UX is unchanged.** Cmd+click in gallery still multi-selects. Click on timeline still clears gallery. Marquee in gallery still works. Drag-to-shot still works. Agent chat attachment removal still works on `/tools/video-editor` AND on `/shots`/`/art` routes (where the bridge is null).\n\n## Notes for the planner\n\n- This codebase uses Vite + React 18 + Zustand + React Router v6 + shadcn UI + Tailwind v3.\n- The existing structural-cleanup megaplan (`structural-cleanup-of-the-20260426-0209`) committed on this branch as `06ac9dde8` + `95d94b780` \u2014 it set the stage by partially formalizing the timeline selection API. This megaplan is the natural follow-up to that one.\n- The codex review identified bugs 1-6 the user has been hitting and grouped them into three families (gesture/input, selection composition, query helper). This megaplan addresses families 1 and 2.\n- See `CLAUDE.md` at the repo root for project-wide rules. Especially relevant: \"Required-provider hooks must throw when their context is missing\" and \"every change should make the codebase smaller or more explicit.\"\n- The user has confirmed: do not commit anything during execution.",
    "significant_flags": 9,
    "unresolved_flags": [
      {
        "id": "correctness-1",
        "concern": "Are the proposed changes technically correct?: Checked Step 7.4's dev-only warning guard against the repo's frontend environment conventions. The plan sketch uses `process.env.NODE_ENV !== 'production'`, but this Vite React app uses `import.meta.env.DEV` throughout `src/`; unless `process` is separately defined in the browser bundle, that selector path can throw a `ReferenceError` when placeholders are emitted.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness-2",
        "concern": "Are the proposed changes technically correct?: Checked the proposed `useSelectionStore` export against the intent-facade requirement. Exporting the raw Zustand selector hook makes every field in `SelectionStoreState` selectable, including the low-level reducer functions that Step 5 intends to remove from public hooks, so it technically reopens the public low-level mutation surface rather than making the intent commands the only reachable API.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "scope",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Checked the planned merge-key test (Step 7.7f) against actual gallery clip construction. The plan says gallery items lack `clipId` and therefore fall back to URL, but the store always assigns `clipId` to gallery clips; a test that fabricates a gallery clip without `clipId` would not exercise the real `selectedGalleryClips` path and could pass while the app shows duplicate timeline/gallery chips.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "issue_hints",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the new `clip.clipId || clip.url` merge-key assumption against `selectionStore.ts:249-256` and `SelectedMediaClip` in `useSelectedMediaClips.ts:6-19`. Gallery selections are converted into `SelectedMediaClip` objects with `clipId: id`, so they do not lack `clipId`; the revised key therefore stops deduping a gallery item and timeline clip that share the same URL, which the existing `AgentChat.tsx:40-75` URL-keyed merge intentionally did.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness",
        "concern": "Are the proposed changes technically correct?: Checked Step 7.4's proposed `currentAttachmentSet.ts` import against `selectionStore.ts:690-699`. `useSelectionStore` is currently a private non-exported function, while the plan creates a separate module that imports it from `./selectionStore`; followed literally, that new file will not compile unless the plan either exports a deliberately narrow selector API or colocates `useCurrentAttachmentSet()` inside `selectionStore.ts`.",
        "category": "correctness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "callers",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked the actual attachment merge callers: `AgentChat.tsx` currently passes timeline clips from `useSelectedMediaClips()` and gallery clips from `useGallerySelection().selectedGalleryClips` into the merge. Because both caller paths supply `clipId`, a `clipId || url` key handles placeholder timeline clips but no longer matches the real gallery-vs-timeline same-URL caller case that the old URL-keyed merge handled.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "FLAG-019",
        "concern": "Attachment merge key: `clip.clipId || clip.url` fixes placeholder collisions but breaks the existing URL dedupe between timeline and gallery attachments because gallery clips already have `clipId`.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "FLAG-020",
        "concern": "Selection store public surface: exporting the raw `useSelectionStore` hook re-exposes low-level Zustand reducer functions despite the intent-facade goal.",
        "category": "maintainability",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "FLAG-021",
        "concern": "Frontend environment guard: the planned placeholder warning uses `process.env.NODE_ENV` in a Vite browser module, while the repo uses `import.meta.env.DEV`.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      }
    ],
    "resolved_flags": [
      {
        "id": "FLAG-001",
        "concern": "Intent-layer contract: the plan maps gallery user selection to reducers that clear timeline selection, contradicting the approved requirement that gallery user selection does not touch timeline selection.",
        "resolution": "Revised the plan to address 14 open significant flags clustering around four real defects: (1) intent contracts are now enforced by direct setState writes inside selectionStore.ts (folded the intent layer into the store file rather than a sibling), so userSelectGalleryItem* never touches timeline and userSelectTimelineClips({additive:true}) still clears gallery; (2) the attachment composer now uses a clipDataById slice that holds ALL timeline clips (not selection-derived), populated by a new useTimelineClipsForAttachments() hook in VideoEditorProvider \u2014 this makes `useCurrentAttachmentSet()` synchronously consistent at every selection moment, and the regression test now exercises the real data flow (clipData populated separately from selection) rather than a pre-seeded happy path; (3) reducer privatization is now exhaustive \u2014 added useTimelineCommit.ts to the migration with a new editorSelectTimelineClip/editorClearTimelineSelection pair, deleted useSelectionStoreApi, and folded the intent layer so cross-file private-store access isn't needed; (4) caller/scope gaps closed \u2014 composerRemoveAttachment now preserves the clipId fallback for timeline clips lacking generationId, useGallerySelectionBridge gets new systemSync*/systemClear* intents, ImageGenerationToolPage modifier plumbing is spelled out concretely, and AgentChat.test.tsx + GenerationsPaneGallery.test.tsx + useModifierKeys.test.tsx are explicitly listed for cleanup. Also expanded the call-site audit with a fresh ripgrep that surfaced additional clearGallerySelection() calls in AgentChat.tsx (497, 812) and confirmed line numbers across the codebase."
      },
      {
        "id": "FLAG-002",
        "concern": "Timeline additive selection: additive timeline marquee selection would preserve gallery selection because the plan routes it through `addTimelineClips`.",
        "resolution": "Revised the plan to address 14 open significant flags clustering around four real defects: (1) intent contracts are now enforced by direct setState writes inside selectionStore.ts (folded the intent layer into the store file rather than a sibling), so userSelectGalleryItem* never touches timeline and userSelectTimelineClips({additive:true}) still clears gallery; (2) the attachment composer now uses a clipDataById slice that holds ALL timeline clips (not selection-derived), populated by a new useTimelineClipsForAttachments() hook in VideoEditorProvider \u2014 this makes `useCurrentAttachmentSet()` synchronously consistent at every selection moment, and the regression test now exercises the real data flow (clipData populated separately from selection) rather than a pre-seeded happy path; (3) reducer privatization is now exhaustive \u2014 added useTimelineCommit.ts to the migration with a new editorSelectTimelineClip/editorClearTimelineSelection pair, deleted useSelectionStoreApi, and folded the intent layer so cross-file private-store access isn't needed; (4) caller/scope gaps closed \u2014 composerRemoveAttachment now preserves the clipId fallback for timeline clips lacking generationId, useGallerySelectionBridge gets new systemSync*/systemClear* intents, ImageGenerationToolPage modifier plumbing is spelled out concretely, and AgentChat.test.tsx + GenerationsPaneGallery.test.tsx + useModifierKeys.test.tsx are explicitly listed for cleanup. Also expanded the call-site audit with a fresh ripgrep that surfaced additional clearGallerySelection() calls in AgentChat.tsx (497, 812) and confirmed line numbers across the codebase."
      },
      {
        "id": "FLAG-003",
        "concern": "Attachment bridge timing: the proposed `clipDataById` effect is still one render behind for newly selected timeline clips.",
        "resolution": "Revised the plan to address 14 open significant flags clustering around four real defects: (1) intent contracts are now enforced by direct setState writes inside selectionStore.ts (folded the intent layer into the store file rather than a sibling), so userSelectGalleryItem* never touches timeline and userSelectTimelineClips({additive:true}) still clears gallery; (2) the attachment composer now uses a clipDataById slice that holds ALL timeline clips (not selection-derived), populated by a new useTimelineClipsForAttachments() hook in VideoEditorProvider \u2014 this makes `useCurrentAttachmentSet()` synchronously consistent at every selection moment, and the regression test now exercises the real data flow (clipData populated separately from selection) rather than a pre-seeded happy path; (3) reducer privatization is now exhaustive \u2014 added useTimelineCommit.ts to the migration with a new editorSelectTimelineClip/editorClearTimelineSelection pair, deleted useSelectionStoreApi, and folded the intent layer so cross-file private-store access isn't needed; (4) caller/scope gaps closed \u2014 composerRemoveAttachment now preserves the clipId fallback for timeline clips lacking generationId, useGallerySelectionBridge gets new systemSync*/systemClear* intents, ImageGenerationToolPage modifier plumbing is spelled out concretely, and AgentChat.test.tsx + GenerationsPaneGallery.test.tsx + useModifierKeys.test.tsx are explicitly listed for cleanup. Also expanded the call-site audit with a fresh ripgrep that surfaced additional clearGallerySelection() calls in AgentChat.tsx (497, 812) and confirmed line numbers across the codebase."
      },
      {
        "id": "FLAG-004",
        "concern": "Reducer privatization: the plan misses direct low-level reducer callers and depends on a private `selectionStore` const from a sibling file.",
        "resolution": "Closed the iter-2 call-site gaps. Iter-3 changes: (1) Added three new intents \u2014 editorSetSelectedTrackId, systemResetTimelineSelection, systemResetSelectionForProjectChange \u2014 to give named replacements to the timeline-lifecycle and project-change reducer callers (FLAG-008, FLAG-007). (2) Extended Step 3 to migrate AppProviders.tsx:42,64, useTimelineState.ts:511,519-520, and useTimelineCommit.ts:111,116-120 (not just the iter-2 lines 184/186/194). useSelectionStoreApi is now removed AFTER all consumers migrate, not as an unrelated cleanup (FLAG-007). (3) Step 5.4 now trims useTimelineMultiSelect's return type to drop selectClip/selectClips/addToSelection/clearSelection (which become unused after Step 3 migrations) and removes the {clearGallery?: boolean} option entirely \u2014 satisfies the brief's 'Remove clearGallery from the public surface' (FLAG-006, issue_hints, scope). (4) Step 5.5 migrates useLastAffectedShot.test.ts off useSelectionStoreApi to the public hook setter via renderHook (FLAG-007). (5) Step 10's primary regression test now fires userSelectTimelineClip BEFORE setTimelineClipData to actually exercise the first-mount race; documents the fallback (placeholder entries in clipDataById) only if the test fails (FLAG-010, correctness). (6) Step 14.2 adds VideoEditorProvider.test.tsx:64-65,270,288,410 to the mock-update list \u2014 the bridge fields it asserts on are deleted (all_locations). (7) AgentChat:497/812 clearGallerySelection calls now have a concrete mapping (composerClearAttachments) with a 'verify during execution' note (callers)."
      },
      {
        "id": "FLAG-005",
        "concern": "Attachment removal matching: `composerRemoveAttachment`'s `(url, mediaType, clipId)` fallback still does not describe how matching gallery selections without `clipId` are removed for no-generation-id attachments, regressing the current URL fallback behavior.",
        "resolution": "Iter-5 incorporates the user's three TIEBREAKER decisions, closing the contract ambiguities the loop had been ping-ponging on. (Q1 / FLAG-005, FLAG-014, correctness-2, callers, scope/matcher) The composerRemoveAttachment matcher is now chip-specific: url+mediaType is ALWAYS required for both surfaces; generationId (if provided) and clipId (timeline-side, if provided) are additional disambiguators that further NARROW the match. This preserves current AgentChat.tsx:282-303 behavior \u2014 sibling variants from the same generationId with different URLs are NOT removed. Step 7.6 unit tests cover the sibling-variant preservation paths. (Q2 / FLAG-015, scope, all_locations) userSelectTimelineClip(_, { additive: true }) now explicitly TOGGLES the clip on/off (matching current selectClip(_, { toggle: true }) UX). userSelectTimelineClips(_, { additive: true }) (marquee) is APPEND-only and never toggles. The implementation block in Step 2.3 spells out both. Step 6 adds two new intent tests covering toggle-off behavior. (Q3 / FLAG-010, correctness-1, issue_hints) The bootstrap empty-render is now impossible by construction: useCurrentAttachmentSet() synthesizes placeholder clip entries (isPlaceholder: true) at READ time for any selectedClipId without clipDataById data. AgentChat renders placeholder chips with a loading state; the visible chip count never drops to zero. A dev-only console.warn fires when placeholders are emitted (sync-delay observability). Step 7.4 spells out the read-time placeholder reader. Step 9.3-4 adds the loading-chip rendering and the X-button-hidden-on-placeholder UX. Step 10 Test 3 is rewritten to assert clips.length \u2265 1 across ALL renders during the selection-before-data scenario, AND that one render contains an isPlaceholder chip, AND that dev-warn fires. Step 10 Test 4 (NEW) covers the additive-toggle behavior end-to-end."
      },
      {
        "id": "issue_hints-1",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: The target architecture explicitly says `userSelectGalleryItem` and `userSelectGalleryItems` do not touch timeline selection, but Phase 1 Step 2 maps them to existing reducers that clear timeline selection. This preserves the old cross-surface behavior instead of the approved intent-layer contract.",
        "resolution": "Revised the plan to address 14 open significant flags clustering around four real defects: (1) intent contracts are now enforced by direct setState writes inside selectionStore.ts (folded the intent layer into the store file rather than a sibling), so userSelectGalleryItem* never touches timeline and userSelectTimelineClips({additive:true}) still clears gallery; (2) the attachment composer now uses a clipDataById slice that holds ALL timeline clips (not selection-derived), populated by a new useTimelineClipsForAttachments() hook in VideoEditorProvider \u2014 this makes `useCurrentAttachmentSet()` synchronously consistent at every selection moment, and the regression test now exercises the real data flow (clipData populated separately from selection) rather than a pre-seeded happy path; (3) reducer privatization is now exhaustive \u2014 added useTimelineCommit.ts to the migration with a new editorSelectTimelineClip/editorClearTimelineSelection pair, deleted useSelectionStoreApi, and folded the intent layer so cross-file private-store access isn't needed; (4) caller/scope gaps closed \u2014 composerRemoveAttachment now preserves the clipId fallback for timeline clips lacking generationId, useGallerySelectionBridge gets new systemSync*/systemClear* intents, ImageGenerationToolPage modifier plumbing is spelled out concretely, and AgentChat.test.tsx + GenerationsPaneGallery.test.tsx + useModifierKeys.test.tsx are explicitly listed for cleanup. Also expanded the call-site audit with a fresh ripgrep that surfaced additional clearGallerySelection() calls in AgentChat.tsx (497, 812) and confirmed line numbers across the codebase."
      },
      {
        "id": "issue_hints-2",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: The brief asks for low-level reducers to become private, but the plan keeps `useSelectionStoreApi()` exported and misses existing direct reducer callers in `useTimelineCommit.ts`, so the low-level mutation surface remains reachable.",
        "resolution": "Closed the iter-2 call-site gaps. Iter-3 changes: (1) Added three new intents \u2014 editorSetSelectedTrackId, systemResetTimelineSelection, systemResetSelectionForProjectChange \u2014 to give named replacements to the timeline-lifecycle and project-change reducer callers (FLAG-008, FLAG-007). (2) Extended Step 3 to migrate AppProviders.tsx:42,64, useTimelineState.ts:511,519-520, and useTimelineCommit.ts:111,116-120 (not just the iter-2 lines 184/186/194). useSelectionStoreApi is now removed AFTER all consumers migrate, not as an unrelated cleanup (FLAG-007). (3) Step 5.4 now trims useTimelineMultiSelect's return type to drop selectClip/selectClips/addToSelection/clearSelection (which become unused after Step 3 migrations) and removes the {clearGallery?: boolean} option entirely \u2014 satisfies the brief's 'Remove clearGallery from the public surface' (FLAG-006, issue_hints, scope). (4) Step 5.5 migrates useLastAffectedShot.test.ts off useSelectionStoreApi to the public hook setter via renderHook (FLAG-007). (5) Step 10's primary regression test now fires userSelectTimelineClip BEFORE setTimelineClipData to actually exercise the first-mount race; documents the fallback (placeholder entries in clipDataById) only if the test fails (FLAG-010, correctness). (6) Step 14.2 adds VideoEditorProvider.test.tsx:64-65,270,288,410 to the mock-update list \u2014 the bridge fields it asserts on are deleted (all_locations). (7) AgentChat:497/812 clearGallerySelection calls now have a concrete mapping (composerClearAttachments) with a 'verify during execution' note (callers)."
      },
      {
        "id": "correctness-3",
        "concern": "Are the proposed changes technically correct?: A sibling `selectionActions.ts` cannot call `selectionStore.getState()` as written because `selectionStore` is currently private to `selectionStore.ts`. The plan needs to fold actions into the store file or define a deliberate internal store export.",
        "resolution": "Revised the plan to address 14 open significant flags clustering around four real defects: (1) intent contracts are now enforced by direct setState writes inside selectionStore.ts (folded the intent layer into the store file rather than a sibling), so userSelectGalleryItem* never touches timeline and userSelectTimelineClips({additive:true}) still clears gallery; (2) the attachment composer now uses a clipDataById slice that holds ALL timeline clips (not selection-derived), populated by a new useTimelineClipsForAttachments() hook in VideoEditorProvider \u2014 this makes `useCurrentAttachmentSet()` synchronously consistent at every selection moment, and the regression test now exercises the real data flow (clipData populated separately from selection) rather than a pre-seeded happy path; (3) reducer privatization is now exhaustive \u2014 added useTimelineCommit.ts to the migration with a new editorSelectTimelineClip/editorClearTimelineSelection pair, deleted useSelectionStoreApi, and folded the intent layer so cross-file private-store access isn't needed; (4) caller/scope gaps closed \u2014 composerRemoveAttachment now preserves the clipId fallback for timeline clips lacking generationId, useGallerySelectionBridge gets new systemSync*/systemClear* intents, ImageGenerationToolPage modifier plumbing is spelled out concretely, and AgentChat.test.tsx + GenerationsPaneGallery.test.tsx + useModifierKeys.test.tsx are explicitly listed for cleanup. Also expanded the call-site audit with a fresh ripgrep that surfaced additional clearGallerySelection() calls in AgentChat.tsx (497, 812) and confirmed line numbers across the codebase."
      },
      {
        "id": "all_locations-1",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Checked support-test locations for deleted AgentChat bridge fields. Step 14.2 now explicitly updates `VideoEditorProvider.test.tsx`, but `src/app/providers/AppProviders.test.tsx:96` also reads `bridge.timelineClips.length`; since `AgentChatContext.tsx` is planned to delete `timelineClips`, this test/support location is still missing from the migration checklist.",
        "resolution": "Iter-4 closes the five remaining iter-3 defects. (1) FLAG-005/issue_hints/callers \u2014 composerRemoveAttachment matcher is now defined explicitly with separate gallery-side and timeline-side rules: gallery matches by generationId else (url, mediaType); timeline matches by generationId else clipId else (url, mediaType). This preserves the URL fallback for no-generationId removals on both surfaces, mirroring AgentChat.tsx:282-303's current behavior. Step 7.5 adds unit tests for all six paths. (2) FLAG-012/scope \u2014 useClipDrag.ts:449,459,461,463 direct callers are now first-class migration targets in Step 3.1 with explicit mappings for each line. (3) FLAG-013/all_locations-1 \u2014 AppProviders.test.tsx:91-99 added to Step 14 with a concrete migration: drop the bridge.timelineClips.length rendering and its data-testid assertion. (4) FLAG-011/all_locations-2 \u2014 added an explicit __getSelectionStateForTests() test-only export in Step 2.4 alongside the existing __resetSelectionStoreForTests; Step 14.2 now uses this for VideoEditorProvider.test.tsx assertions instead of selectionStore.getState(). (5) FLAG-010/correctness \u2014 Test 10 fully restructured. The iter-3 ordering (selection before clip data) was logically inconsistent with the userSelectTimelineClip contract that clears gallery. Test 1 is now the realistic steady-state flow (clip data populated FIRST via setTimelineClipData, then gallery, then user clicks timeline) which is what production does \u2014 useTimelineClipsForAttachments runs on render before user interaction. Test 3 documents the test-environment-only race as expected behavior, not a fix target."
      },
      {
        "id": "all_locations-2",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Checked Step 14.2's proposed replacement assertions against the plan's privatization goal. The plan says to delete `useSelectionStoreApi()` and keep the store private, but also tells tests to assert `selectionStore.getState().clipDataById` and `selectionStore.getState().timeline.selectedClipIds`; without a deliberate test-only read helper or renderHook selector, those assertions depend on a private symbol that should no longer be reachable.",
        "resolution": "Iter-4 closes the five remaining iter-3 defects. (1) FLAG-005/issue_hints/callers \u2014 composerRemoveAttachment matcher is now defined explicitly with separate gallery-side and timeline-side rules: gallery matches by generationId else (url, mediaType); timeline matches by generationId else clipId else (url, mediaType). This preserves the URL fallback for no-generationId removals on both surfaces, mirroring AgentChat.tsx:282-303's current behavior. Step 7.5 adds unit tests for all six paths. (2) FLAG-012/scope \u2014 useClipDrag.ts:449,459,461,463 direct callers are now first-class migration targets in Step 3.1 with explicit mappings for each line. (3) FLAG-013/all_locations-1 \u2014 AppProviders.test.tsx:91-99 added to Step 14 with a concrete migration: drop the bridge.timelineClips.length rendering and its data-testid assertion. (4) FLAG-011/all_locations-2 \u2014 added an explicit __getSelectionStateForTests() test-only export in Step 2.4 alongside the existing __resetSelectionStoreForTests; Step 14.2 now uses this for VideoEditorProvider.test.tsx assertions instead of selectionStore.getState(). (5) FLAG-010/correctness \u2014 Test 10 fully restructured. The iter-3 ordering (selection before clip data) was logically inconsistent with the userSelectTimelineClip contract that clears gallery. Test 1 is now the realistic steady-state flow (clip data populated FIRST via setTimelineClipData, then gallery, then user clicks timeline) which is what production does \u2014 useTimelineClipsForAttachments runs on render before user interaction. Test 3 documents the test-environment-only race as expected behavior, not a fix target."
      },
      {
        "id": "callers-1",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Current AgentChat attachment removal falls back to `clipId` for timeline clips without generation ids, but the planned `composerRemoveAttachment` predicate ignores `clipId`. This can remove the wrong duplicate URL clip or miss the existing fallback behavior.",
        "resolution": "Revised the plan to address 14 open significant flags clustering around four real defects: (1) intent contracts are now enforced by direct setState writes inside selectionStore.ts (folded the intent layer into the store file rather than a sibling), so userSelectGalleryItem* never touches timeline and userSelectTimelineClips({additive:true}) still clears gallery; (2) the attachment composer now uses a clipDataById slice that holds ALL timeline clips (not selection-derived), populated by a new useTimelineClipsForAttachments() hook in VideoEditorProvider \u2014 this makes `useCurrentAttachmentSet()` synchronously consistent at every selection moment, and the regression test now exercises the real data flow (clipData populated separately from selection) rather than a pre-seeded happy path; (3) reducer privatization is now exhaustive \u2014 added useTimelineCommit.ts to the migration with a new editorSelectTimelineClip/editorClearTimelineSelection pair, deleted useSelectionStoreApi, and folded the intent layer so cross-file private-store access isn't needed; (4) caller/scope gaps closed \u2014 composerRemoveAttachment now preserves the clipId fallback for timeline clips lacking generationId, useGallerySelectionBridge gets new systemSync*/systemClear* intents, ImageGenerationToolPage modifier plumbing is spelled out concretely, and AgentChat.test.tsx + GenerationsPaneGallery.test.tsx + useModifierKeys.test.tsx are explicitly listed for cleanup. Also expanded the call-site audit with a fresh ripgrep that surfaced additional clearGallerySelection() calls in AgentChat.tsx (497, 812) and confirmed line numbers across the codebase."
      },
      {
        "id": "callers-2",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: `ImageGenerationToolPage.tsx` currently receives only `image` in `handleImageClick`; the shared type now allows optional modifiers. The plan wording around synthetic events is imprecise and could leave the race-prone `useModifierKeys` path in place.",
        "resolution": "Revised the plan to address 14 open significant flags clustering around four real defects: (1) intent contracts are now enforced by direct setState writes inside selectionStore.ts (folded the intent layer into the store file rather than a sibling), so userSelectGalleryItem* never touches timeline and userSelectTimelineClips({additive:true}) still clears gallery; (2) the attachment composer now uses a clipDataById slice that holds ALL timeline clips (not selection-derived), populated by a new useTimelineClipsForAttachments() hook in VideoEditorProvider \u2014 this makes `useCurrentAttachmentSet()` synchronously consistent at every selection moment, and the regression test now exercises the real data flow (clipData populated separately from selection) rather than a pre-seeded happy path; (3) reducer privatization is now exhaustive \u2014 added useTimelineCommit.ts to the migration with a new editorSelectTimelineClip/editorClearTimelineSelection pair, deleted useSelectionStoreApi, and folded the intent layer so cross-file private-store access isn't needed; (4) caller/scope gaps closed \u2014 composerRemoveAttachment now preserves the clipId fallback for timeline clips lacking generationId, useGallerySelectionBridge gets new systemSync*/systemClear* intents, ImageGenerationToolPage modifier plumbing is spelled out concretely, and AgentChat.test.tsx + GenerationsPaneGallery.test.tsx + useModifierKeys.test.tsx are explicitly listed for cleanup. Also expanded the call-site audit with a fresh ripgrep that surfaced additional clearGallerySelection() calls in AgentChat.tsx (497, 812) and confirmed line numbers across the codebase."
      },
      {
        "id": "FLAG-006",
        "concern": "Selection API surface: revised plan preserves `useTimelineMultiSelect` as a public low-level mutation surface with `clearGallery` options.",
        "resolution": "Closed the iter-2 call-site gaps. Iter-3 changes: (1) Added three new intents \u2014 editorSetSelectedTrackId, systemResetTimelineSelection, systemResetSelectionForProjectChange \u2014 to give named replacements to the timeline-lifecycle and project-change reducer callers (FLAG-008, FLAG-007). (2) Extended Step 3 to migrate AppProviders.tsx:42,64, useTimelineState.ts:511,519-520, and useTimelineCommit.ts:111,116-120 (not just the iter-2 lines 184/186/194). useSelectionStoreApi is now removed AFTER all consumers migrate, not as an unrelated cleanup (FLAG-007). (3) Step 5.4 now trims useTimelineMultiSelect's return type to drop selectClip/selectClips/addToSelection/clearSelection (which become unused after Step 3 migrations) and removes the {clearGallery?: boolean} option entirely \u2014 satisfies the brief's 'Remove clearGallery from the public surface' (FLAG-006, issue_hints, scope). (4) Step 5.5 migrates useLastAffectedShot.test.ts off useSelectionStoreApi to the public hook setter via renderHook (FLAG-007). (5) Step 10's primary regression test now fires userSelectTimelineClip BEFORE setTimelineClipData to actually exercise the first-mount race; documents the fallback (placeholder entries in clipDataById) only if the test fails (FLAG-010, correctness). (6) Step 14.2 adds VideoEditorProvider.test.tsx:64-65,270,288,410 to the mock-update list \u2014 the bridge fields it asserts on are deleted (all_locations). (7) AgentChat:497/812 clearGallerySelection calls now have a concrete mapping (composerClearAttachments) with a 'verify during execution' note (callers)."
      },
      {
        "id": "FLAG-007",
        "concern": "Reducer privatization: `useSelectionStoreApi()` has additional live consumers outside `useTimelineCommit.ts`.",
        "resolution": "Closed the iter-2 call-site gaps. Iter-3 changes: (1) Added three new intents \u2014 editorSetSelectedTrackId, systemResetTimelineSelection, systemResetSelectionForProjectChange \u2014 to give named replacements to the timeline-lifecycle and project-change reducer callers (FLAG-008, FLAG-007). (2) Extended Step 3 to migrate AppProviders.tsx:42,64, useTimelineState.ts:511,519-520, and useTimelineCommit.ts:111,116-120 (not just the iter-2 lines 184/186/194). useSelectionStoreApi is now removed AFTER all consumers migrate, not as an unrelated cleanup (FLAG-007). (3) Step 5.4 now trims useTimelineMultiSelect's return type to drop selectClip/selectClips/addToSelection/clearSelection (which become unused after Step 3 migrations) and removes the {clearGallery?: boolean} option entirely \u2014 satisfies the brief's 'Remove clearGallery from the public surface' (FLAG-006, issue_hints, scope). (4) Step 5.5 migrates useLastAffectedShot.test.ts off useSelectionStoreApi to the public hook setter via renderHook (FLAG-007). (5) Step 10's primary regression test now fires userSelectTimelineClip BEFORE setTimelineClipData to actually exercise the first-mount race; documents the fallback (placeholder entries in clipDataById) only if the test fails (FLAG-010, correctness). (6) Step 14.2 adds VideoEditorProvider.test.tsx:64-65,270,288,410 to the mock-update list \u2014 the bridge fields it asserts on are deleted (all_locations). (7) AgentChat:497/812 clearGallerySelection calls now have a concrete mapping (composerClearAttachments) with a 'verify during execution' note (callers)."
      },
      {
        "id": "FLAG-008",
        "concern": "Timeline lifecycle/track selection: stripping `useTimelineSelectionStore()` mutations lacks replacements for reset and selected-track callers.",
        "resolution": "Closed the iter-2 call-site gaps. Iter-3 changes: (1) Added three new intents \u2014 editorSetSelectedTrackId, systemResetTimelineSelection, systemResetSelectionForProjectChange \u2014 to give named replacements to the timeline-lifecycle and project-change reducer callers (FLAG-008, FLAG-007). (2) Extended Step 3 to migrate AppProviders.tsx:42,64, useTimelineState.ts:511,519-520, and useTimelineCommit.ts:111,116-120 (not just the iter-2 lines 184/186/194). useSelectionStoreApi is now removed AFTER all consumers migrate, not as an unrelated cleanup (FLAG-007). (3) Step 5.4 now trims useTimelineMultiSelect's return type to drop selectClip/selectClips/addToSelection/clearSelection (which become unused after Step 3 migrations) and removes the {clearGallery?: boolean} option entirely \u2014 satisfies the brief's 'Remove clearGallery from the public surface' (FLAG-006, issue_hints, scope). (4) Step 5.5 migrates useLastAffectedShot.test.ts off useSelectionStoreApi to the public hook setter via renderHook (FLAG-007). (5) Step 10's primary regression test now fires userSelectTimelineClip BEFORE setTimelineClipData to actually exercise the first-mount race; documents the fallback (placeholder entries in clipDataById) only if the test fails (FLAG-010, correctness). (6) Step 14.2 adds VideoEditorProvider.test.tsx:64-65,270,288,410 to the mock-update list \u2014 the bridge fields it asserts on are deleted (all_locations). (7) AgentChat:497/812 clearGallerySelection calls now have a concrete mapping (composerClearAttachments) with a 'verify during execution' note (callers)."
      },
      {
        "id": "FLAG-009",
        "concern": "AgentChat bridge support tests: `VideoEditorProvider.test.tsx` still depends on removed bridge fields.",
        "resolution": "Grep found `timelineClips` and `replaceSelectedTimelineClips` assertions there."
      },
      {
        "id": "FLAG-010",
        "concern": "Attachment bootstrap timing: the revised plan now documents selection-before-clip-data as an expected empty attachment render, which narrows the original flicker requirement rather than making the transition impossible by construction.",
        "resolution": "Iter-5 incorporates the user's three TIEBREAKER decisions, closing the contract ambiguities the loop had been ping-ponging on. (Q1 / FLAG-005, FLAG-014, correctness-2, callers, scope/matcher) The composerRemoveAttachment matcher is now chip-specific: url+mediaType is ALWAYS required for both surfaces; generationId (if provided) and clipId (timeline-side, if provided) are additional disambiguators that further NARROW the match. This preserves current AgentChat.tsx:282-303 behavior \u2014 sibling variants from the same generationId with different URLs are NOT removed. Step 7.6 unit tests cover the sibling-variant preservation paths. (Q2 / FLAG-015, scope, all_locations) userSelectTimelineClip(_, { additive: true }) now explicitly TOGGLES the clip on/off (matching current selectClip(_, { toggle: true }) UX). userSelectTimelineClips(_, { additive: true }) (marquee) is APPEND-only and never toggles. The implementation block in Step 2.3 spells out both. Step 6 adds two new intent tests covering toggle-off behavior. (Q3 / FLAG-010, correctness-1, issue_hints) The bootstrap empty-render is now impossible by construction: useCurrentAttachmentSet() synthesizes placeholder clip entries (isPlaceholder: true) at READ time for any selectedClipId without clipDataById data. AgentChat renders placeholder chips with a loading state; the visible chip count never drops to zero. A dev-only console.warn fires when placeholders are emitted (sync-delay observability). Step 7.4 spells out the read-time placeholder reader. Step 9.3-4 adds the loading-chip rendering and the X-button-hidden-on-placeholder UX. Step 10 Test 3 is rewritten to assert clips.length \u2265 1 across ALL renders during the selection-before-data scenario, AND that one render contains an isPlaceholder chip, AND that dev-warn fires. Step 10 Test 4 (NEW) covers the additive-toggle behavior end-to-end."
      },
      {
        "id": "all_locations",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Checked supporting component infrastructure for placeholder rendering. The actual attachment strip lives in `AgentChatMessage.tsx:180-226`, where previews always render `<img src={attachment.url}>` or `<video src={attachment.url}>` and always show the remove button when `onRemoveAttachment` is present; the plan says AgentChat renders placeholder chips and hides the X, but Step 14 only calls out `AgentChat.test.tsx`, not the existing `AgentChatMessage.test.tsx` surface that should exercise this component-level behavior.",
        "resolution": "Iter-6 closes the three remaining iter-5 placeholder-design gaps. (1) FLAG-016/issue_hints/scope: mergeSelectedClips is now keyed by `clipId || url` instead of `url`. The corrected implementation is spelled out in Step 7.4 with an inline comment marking the change. Step 10 Test 5 (NEW) directly verifies that two selected-but-unknown clipIds produce two distinct placeholder chips and never collapse \u2014 locking the merge-key contract. Step 7.7 adds three additional unit tests for the merge-key behavior (single placeholder, two placeholders, gallery URL fallback for gallery items lacking clipId). (2) FLAG-017/correctness: useSelectionStore is now explicitly exported from selectionStore.ts (Step 2.3) so currentAttachmentSet.ts can import it. The export is intentionally narrow \u2014 it returns whatever the selector requests, and the existing state-only hooks remain the preferred public surface. (3) FLAG-018/all_locations: Step 9.3 now names the actual chip render surface \u2014 AgentChatMessage.tsx:180-226 (the AgentChatAttachmentStrip component) \u2014 with concrete behavior changes for placeholder rendering: chip slot reserves space, no img/video src binding (avoids broken-image flash from url: ''), no X button. Step 14.2 (NEW) adds AgentChatMessage.test.tsx to the test list with explicit assertions for the placeholder chip contract (loading state, no media binding, no X button) and the non-placeholder fallback (normal media rendering, X button when onRemoveAttachment provided). All settled decisions from iter 2-5 are preserved unchanged."
      },
      {
        "id": "FLAG-011",
        "concern": "Support-test access: revised test instructions depend on direct `selectionStore.getState()` reads even though the plan deletes `useSelectionStoreApi()` and keeps the store private.",
        "resolution": "Iter-4 closes the five remaining iter-3 defects. (1) FLAG-005/issue_hints/callers \u2014 composerRemoveAttachment matcher is now defined explicitly with separate gallery-side and timeline-side rules: gallery matches by generationId else (url, mediaType); timeline matches by generationId else clipId else (url, mediaType). This preserves the URL fallback for no-generationId removals on both surfaces, mirroring AgentChat.tsx:282-303's current behavior. Step 7.5 adds unit tests for all six paths. (2) FLAG-012/scope \u2014 useClipDrag.ts:449,459,461,463 direct callers are now first-class migration targets in Step 3.1 with explicit mappings for each line. (3) FLAG-013/all_locations-1 \u2014 AppProviders.test.tsx:91-99 added to Step 14 with a concrete migration: drop the bridge.timelineClips.length rendering and its data-testid assertion. (4) FLAG-011/all_locations-2 \u2014 added an explicit __getSelectionStateForTests() test-only export in Step 2.4 alongside the existing __resetSelectionStoreForTests; Step 14.2 now uses this for VideoEditorProvider.test.tsx assertions instead of selectionStore.getState(). (5) FLAG-010/correctness \u2014 Test 10 fully restructured. The iter-3 ordering (selection before clip data) was logically inconsistent with the userSelectTimelineClip contract that clears gallery. Test 1 is now the realistic steady-state flow (clip data populated FIRST via setTimelineClipData, then gallery, then user clicks timeline) which is what production does \u2014 useTimelineClipsForAttachments runs on render before user interaction. Test 3 documents the test-environment-only race as expected behavior, not a fix target."
      },
      {
        "id": "FLAG-012",
        "concern": "Drag-selection caller contract: the plan lists helper-file drag callbacks but does not explicitly migrate direct `useClipDrag.ts` pointer-up calls that pass `{ toggle: true }` and `{ preserveSelection: true }` through `selectClip`.",
        "resolution": "Iter-4 closes the five remaining iter-3 defects. (1) FLAG-005/issue_hints/callers \u2014 composerRemoveAttachment matcher is now defined explicitly with separate gallery-side and timeline-side rules: gallery matches by generationId else (url, mediaType); timeline matches by generationId else clipId else (url, mediaType). This preserves the URL fallback for no-generationId removals on both surfaces, mirroring AgentChat.tsx:282-303's current behavior. Step 7.5 adds unit tests for all six paths. (2) FLAG-012/scope \u2014 useClipDrag.ts:449,459,461,463 direct callers are now first-class migration targets in Step 3.1 with explicit mappings for each line. (3) FLAG-013/all_locations-1 \u2014 AppProviders.test.tsx:91-99 added to Step 14 with a concrete migration: drop the bridge.timelineClips.length rendering and its data-testid assertion. (4) FLAG-011/all_locations-2 \u2014 added an explicit __getSelectionStateForTests() test-only export in Step 2.4 alongside the existing __resetSelectionStoreForTests; Step 14.2 now uses this for VideoEditorProvider.test.tsx assertions instead of selectionStore.getState(). (5) FLAG-010/correctness \u2014 Test 10 fully restructured. The iter-3 ordering (selection before clip data) was logically inconsistent with the userSelectTimelineClip contract that clears gallery. Test 1 is now the realistic steady-state flow (clip data populated FIRST via setTimelineClipData, then gallery, then user clicks timeline) which is what production does \u2014 useTimelineClipsForAttachments runs on render before user interaction. Test 3 documents the test-environment-only race as expected behavior, not a fix target."
      },
      {
        "id": "FLAG-013",
        "concern": "AgentChat bridge support tests: `AppProviders.test.tsx` still depends on `agentChatBridge.timelineClips`, but the revised test migration list only calls out `VideoEditorProvider.test.tsx` for deleted bridge fields.",
        "resolution": "Iter-4 closes the five remaining iter-3 defects. (1) FLAG-005/issue_hints/callers \u2014 composerRemoveAttachment matcher is now defined explicitly with separate gallery-side and timeline-side rules: gallery matches by generationId else (url, mediaType); timeline matches by generationId else clipId else (url, mediaType). This preserves the URL fallback for no-generationId removals on both surfaces, mirroring AgentChat.tsx:282-303's current behavior. Step 7.5 adds unit tests for all six paths. (2) FLAG-012/scope \u2014 useClipDrag.ts:449,459,461,463 direct callers are now first-class migration targets in Step 3.1 with explicit mappings for each line. (3) FLAG-013/all_locations-1 \u2014 AppProviders.test.tsx:91-99 added to Step 14 with a concrete migration: drop the bridge.timelineClips.length rendering and its data-testid assertion. (4) FLAG-011/all_locations-2 \u2014 added an explicit __getSelectionStateForTests() test-only export in Step 2.4 alongside the existing __resetSelectionStoreForTests; Step 14.2 now uses this for VideoEditorProvider.test.tsx assertions instead of selectionStore.getState(). (5) FLAG-010/correctness \u2014 Test 10 fully restructured. The iter-3 ordering (selection before clip data) was logically inconsistent with the userSelectTimelineClip contract that clears gallery. Test 1 is now the realistic steady-state flow (clip data populated FIRST via setTimelineClipData, then gallery, then user clicks timeline) which is what production does \u2014 useTimelineClipsForAttachments runs on render before user interaction. Test 3 documents the test-environment-only race as expected behavior, not a fix target."
      },
      {
        "id": "FLAG-014",
        "concern": "Attachment removal matching: the generationId branch is broader than current chip removal semantics because it drops the current URL/mediaType guard.",
        "resolution": "Iter-5 incorporates the user's three TIEBREAKER decisions, closing the contract ambiguities the loop had been ping-ponging on. (Q1 / FLAG-005, FLAG-014, correctness-2, callers, scope/matcher) The composerRemoveAttachment matcher is now chip-specific: url+mediaType is ALWAYS required for both surfaces; generationId (if provided) and clipId (timeline-side, if provided) are additional disambiguators that further NARROW the match. This preserves current AgentChat.tsx:282-303 behavior \u2014 sibling variants from the same generationId with different URLs are NOT removed. Step 7.6 unit tests cover the sibling-variant preservation paths. (Q2 / FLAG-015, scope, all_locations) userSelectTimelineClip(_, { additive: true }) now explicitly TOGGLES the clip on/off (matching current selectClip(_, { toggle: true }) UX). userSelectTimelineClips(_, { additive: true }) (marquee) is APPEND-only and never toggles. The implementation block in Step 2.3 spells out both. Step 6 adds two new intent tests covering toggle-off behavior. (Q3 / FLAG-010, correctness-1, issue_hints) The bootstrap empty-render is now impossible by construction: useCurrentAttachmentSet() synthesizes placeholder clip entries (isPlaceholder: true) at READ time for any selectedClipId without clipDataById data. AgentChat renders placeholder chips with a loading state; the visible chip count never drops to zero. A dev-only console.warn fires when placeholders are emitted (sync-delay observability). Step 7.4 spells out the read-time placeholder reader. Step 9.3-4 adds the loading-chip rendering and the X-button-hidden-on-placeholder UX. Step 10 Test 3 is rewritten to assert clips.length \u2265 1 across ALL renders during the selection-before-data scenario, AND that one render contains an isPlaceholder chip, AND that dev-warn fires. Step 10 Test 4 (NEW) covers the additive-toggle behavior end-to-end."
      },
      {
        "id": "FLAG-015",
        "concern": "Timeline additive selection semantics: migrating `{ toggle: true }` callers to `{ additive: true }` is only safe if `userSelectTimelineClip` explicitly toggles already-selected clips off, but the plan and tests do not state that contract.",
        "resolution": "Iter-5 incorporates the user's three TIEBREAKER decisions, closing the contract ambiguities the loop had been ping-ponging on. (Q1 / FLAG-005, FLAG-014, correctness-2, callers, scope/matcher) The composerRemoveAttachment matcher is now chip-specific: url+mediaType is ALWAYS required for both surfaces; generationId (if provided) and clipId (timeline-side, if provided) are additional disambiguators that further NARROW the match. This preserves current AgentChat.tsx:282-303 behavior \u2014 sibling variants from the same generationId with different URLs are NOT removed. Step 7.6 unit tests cover the sibling-variant preservation paths. (Q2 / FLAG-015, scope, all_locations) userSelectTimelineClip(_, { additive: true }) now explicitly TOGGLES the clip on/off (matching current selectClip(_, { toggle: true }) UX). userSelectTimelineClips(_, { additive: true }) (marquee) is APPEND-only and never toggles. The implementation block in Step 2.3 spells out both. Step 6 adds two new intent tests covering toggle-off behavior. (Q3 / FLAG-010, correctness-1, issue_hints) The bootstrap empty-render is now impossible by construction: useCurrentAttachmentSet() synthesizes placeholder clip entries (isPlaceholder: true) at READ time for any selectedClipId without clipDataById data. AgentChat renders placeholder chips with a loading state; the visible chip count never drops to zero. A dev-only console.warn fires when placeholders are emitted (sync-delay observability). Step 7.4 spells out the read-time placeholder reader. Step 9.3-4 adds the loading-chip rendering and the X-button-hidden-on-placeholder UX. Step 10 Test 3 is rewritten to assert clips.length \u2265 1 across ALL renders during the selection-before-data scenario, AND that one render contains an isPlaceholder chip, AND that dev-warn fires. Step 10 Test 4 (NEW) covers the additive-toggle behavior end-to-end."
      },
      {
        "id": "FLAG-016",
        "concern": "Attachment placeholders: placeholder clips use the same empty URL and will collide with the existing URL-based `mergeSelectedClips` dedupe unless the merge key is changed or placeholders get unique keys.",
        "resolution": "Iter-6 closes the three remaining iter-5 placeholder-design gaps. (1) FLAG-016/issue_hints/scope: mergeSelectedClips is now keyed by `clipId || url` instead of `url`. The corrected implementation is spelled out in Step 7.4 with an inline comment marking the change. Step 10 Test 5 (NEW) directly verifies that two selected-but-unknown clipIds produce two distinct placeholder chips and never collapse \u2014 locking the merge-key contract. Step 7.7 adds three additional unit tests for the merge-key behavior (single placeholder, two placeholders, gallery URL fallback for gallery items lacking clipId). (2) FLAG-017/correctness: useSelectionStore is now explicitly exported from selectionStore.ts (Step 2.3) so currentAttachmentSet.ts can import it. The export is intentionally narrow \u2014 it returns whatever the selector requests, and the existing state-only hooks remain the preferred public surface. (3) FLAG-018/all_locations: Step 9.3 now names the actual chip render surface \u2014 AgentChatMessage.tsx:180-226 (the AgentChatAttachmentStrip component) \u2014 with concrete behavior changes for placeholder rendering: chip slot reserves space, no img/video src binding (avoids broken-image flash from url: ''), no X button. Step 14.2 (NEW) adds AgentChatMessage.test.tsx to the test list with explicit assertions for the placeholder chip contract (loading state, no media binding, no X button) and the non-placeholder fallback (normal media rendering, X button when onRemoveAttachment provided). All settled decisions from iter 2-5 are preserved unchanged."
      },
      {
        "id": "FLAG-017",
        "concern": "Current attachment set module: the plan imports `useSelectionStore` from `selectionStore.ts`, but that hook is currently private and not exported.",
        "resolution": "Iter-6 closes the three remaining iter-5 placeholder-design gaps. (1) FLAG-016/issue_hints/scope: mergeSelectedClips is now keyed by `clipId || url` instead of `url`. The corrected implementation is spelled out in Step 7.4 with an inline comment marking the change. Step 10 Test 5 (NEW) directly verifies that two selected-but-unknown clipIds produce two distinct placeholder chips and never collapse \u2014 locking the merge-key contract. Step 7.7 adds three additional unit tests for the merge-key behavior (single placeholder, two placeholders, gallery URL fallback for gallery items lacking clipId). (2) FLAG-017/correctness: useSelectionStore is now explicitly exported from selectionStore.ts (Step 2.3) so currentAttachmentSet.ts can import it. The export is intentionally narrow \u2014 it returns whatever the selector requests, and the existing state-only hooks remain the preferred public surface. (3) FLAG-018/all_locations: Step 9.3 now names the actual chip render surface \u2014 AgentChatMessage.tsx:180-226 (the AgentChatAttachmentStrip component) \u2014 with concrete behavior changes for placeholder rendering: chip slot reserves space, no img/video src binding (avoids broken-image flash from url: ''), no X button. Step 14.2 (NEW) adds AgentChatMessage.test.tsx to the test list with explicit assertions for the placeholder chip contract (loading state, no media binding, no X button) and the non-placeholder fallback (normal media rendering, X button when onRemoveAttachment provided). All settled decisions from iter 2-5 are preserved unchanged."
      },
      {
        "id": "FLAG-018",
        "concern": "Placeholder rendering tests: the plan changes attachment-strip behavior but does not name the component-level test surface for `AgentChatMessage.tsx`.",
        "resolution": "Iter-6 closes the three remaining iter-5 placeholder-design gaps. (1) FLAG-016/issue_hints/scope: mergeSelectedClips is now keyed by `clipId || url` instead of `url`. The corrected implementation is spelled out in Step 7.4 with an inline comment marking the change. Step 10 Test 5 (NEW) directly verifies that two selected-but-unknown clipIds produce two distinct placeholder chips and never collapse \u2014 locking the merge-key contract. Step 7.7 adds three additional unit tests for the merge-key behavior (single placeholder, two placeholders, gallery URL fallback for gallery items lacking clipId). (2) FLAG-017/correctness: useSelectionStore is now explicitly exported from selectionStore.ts (Step 2.3) so currentAttachmentSet.ts can import it. The export is intentionally narrow \u2014 it returns whatever the selector requests, and the existing state-only hooks remain the preferred public surface. (3) FLAG-018/all_locations: Step 9.3 now names the actual chip render surface \u2014 AgentChatMessage.tsx:180-226 (the AgentChatAttachmentStrip component) \u2014 with concrete behavior changes for placeholder rendering: chip slot reserves space, no img/video src binding (avoids broken-image flash from url: ''), no X button. Step 14.2 (NEW) adds AgentChatMessage.test.tsx to the test list with explicit assertions for the placeholder chip contract (loading state, no media binding, no X button) and the non-placeholder fallback (normal media rendering, X button when onRemoveAttachment provided). All settled decisions from iter 2-5 are preserved unchanged."
      }
    ],
    "weighted_score": 8.25,
    "weighted_history": [
      23.5,
      18.5,
      16.5,
      18.5,
      6.5,
      8.25
    ],
    "plan_delta_from_previous": 89.86,
    "recurring_critiques": [],
    "scope_creep_flags": [],
    "loop_summary": "Iteration 6. Weighted score trajectory: 23.5 -> 18.5 -> 16.5 -> 18.5 -> 6.5 -> 8.25 -> 8.25. Plan deltas: 65.3%, 66.2%, 44.6%, 56.1%, 89.9%. Recurring critiques: 0. Resolved flags: 26. Open significant flags: 9.",
    "debt_overlaps": [],
    "escalated_debt_subsystems": []
  },
  "flag_resolutions": [],
  "resolved_flag_ids": [],
  "resolution_summary": ""
}



Critique flags to re-verify against the final diff:
            [
  {
    "id": "FLAG-001",
    "concern": "Intent-layer contract: the plan maps gallery user selection to reducers that clear timeline selection, contradicting the approved requirement that gallery user selection does not touch timeline selection.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-002",
    "concern": "Timeline additive selection: additive timeline marquee selection would preserve gallery selection because the plan routes it through `addTimelineClips`.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-003",
    "concern": "Attachment bridge timing: the proposed `clipDataById` effect is still one render behind for newly selected timeline clips.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-004",
    "concern": "Reducer privatization: the plan misses direct low-level reducer callers and depends on a private `selectionStore` const from a sibling file.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-005",
    "concern": "Attachment removal matching: `composerRemoveAttachment`'s `(url, mediaType, clipId)` fallback still does not describe how matching gallery selections without `clipId` are removed for no-generation-id attachments, regressing the current URL fallback behavior.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "verifiability-0",
    "concern": "Criterion 45: requires human verification (inspect_runtime_ui).",
    "severity": "minor",
    "status": "open"
  },
  {
    "id": "verifiability-1",
    "concern": "Criterion 46: requires human verification (inspect_runtime_ui).",
    "severity": "minor",
    "status": "open"
  },
  {
    "id": "issue_hints-1",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: The target architecture explicitly says `userSelectGalleryItem` and `userSelectGalleryItems` do not touch timeline selection, but Phase 1 Step 2 maps them to existing reducers that clear timeline selection. This preserves the old cross-surface behavior instead of the approved intent-layer contract.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "issue_hints-2",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: The brief asks for low-level reducers to become private, but the plan keeps `useSelectionStoreApi()` exported and misses existing direct reducer callers in `useTimelineCommit.ts`, so the low-level mutation surface remains reachable.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "correctness-1",
    "concern": "Are the proposed changes technically correct?: Checked Step 7.4's dev-only warning guard against the repo's frontend environment conventions. The plan sketch uses `process.env.NODE_ENV !== 'production'`, but this Vite React app uses `import.meta.env.DEV` throughout `src/`; unless `process` is separately defined in the browser bundle, that selector path can throw a `ReferenceError` when placeholders are emitted.",
    "severity": "significant",
    "status": "open"
  },
  {
    "id": "correctness-2",
    "concern": "Are the proposed changes technically correct?: Checked the proposed `useSelectionStore` export against the intent-facade requirement. Exporting the raw Zustand selector hook makes every field in `SelectionStoreState` selectable, including the low-level reducer functions that Step 5 intends to remove from public hooks, so it technically reopens the public low-level mutation surface rather than making the intent commands the only reachable API.",
    "severity": "significant",
    "status": "open"
  },
  {
    "id": "correctness-3",
    "concern": "Are the proposed changes technically correct?: A sibling `selectionActions.ts` cannot call `selectionStore.getState()` as written because `selectionStore` is currently private to `selectionStore.ts`. The plan needs to fold actions into the store file or define a deliberate internal store export.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "scope",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Checked the planned merge-key test (Step 7.7f) against actual gallery clip construction. The plan says gallery items lack `clipId` and therefore fall back to URL, but the store always assigns `clipId` to gallery clips; a test that fabricates a gallery clip without `clipId` would not exercise the real `selectedGalleryClips` path and could pass while the app shows duplicate timeline/gallery chips.",
    "severity": "significant",
    "status": "open"
  },
  {
    "id": "all_locations-1",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Checked support-test locations for deleted AgentChat bridge fields. Step 14.2 now explicitly updates `VideoEditorProvider.test.tsx`, but `src/app/providers/AppProviders.test.tsx:96` also reads `bridge.timelineClips.length`; since `AgentChatContext.tsx` is planned to delete `timelineClips`, this test/support location is still missing from the migration checklist.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "all_locations-2",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Checked Step 14.2's proposed replacement assertions against the plan's privatization goal. The plan says to delete `useSelectionStoreApi()` and keep the store private, but also tells tests to assert `selectionStore.getState().clipDataById` and `selectionStore.getState().timeline.selectedClipIds`; without a deliberate test-only read helper or renderHook selector, those assertions depend on a private symbol that should no longer be reachable.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "callers-1",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Current AgentChat attachment removal falls back to `clipId` for timeline clips without generation ids, but the planned `composerRemoveAttachment` predicate ignores `clipId`. This can remove the wrong duplicate URL clip or miss the existing fallback behavior.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "callers-2",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: `ImageGenerationToolPage.tsx` currently receives only `image` in `handleImageClick`; the shared type now allows optional modifiers. The plan wording around synthetic events is imprecise and could leave the race-prone `useModifierKeys` path in place.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-006",
    "concern": "Selection API surface: revised plan preserves `useTimelineMultiSelect` as a public low-level mutation surface with `clearGallery` options.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-007",
    "concern": "Reducer privatization: `useSelectionStoreApi()` has additional live consumers outside `useTimelineCommit.ts`.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-008",
    "concern": "Timeline lifecycle/track selection: stripping `useTimelineSelectionStore()` mutations lacks replacements for reset and selected-track callers.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-009",
    "concern": "AgentChat bridge support tests: `VideoEditorProvider.test.tsx` still depends on removed bridge fields.",
    "severity": "minor",
    "status": "verified"
  },
  {
    "id": "FLAG-010",
    "concern": "Attachment bootstrap timing: the revised plan now documents selection-before-clip-data as an expected empty attachment render, which narrows the original flicker requirement rather than making the transition impossible by construction.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "issue_hints",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the new `clip.clipId || clip.url` merge-key assumption against `selectionStore.ts:249-256` and `SelectedMediaClip` in `useSelectedMediaClips.ts:6-19`. Gallery selections are converted into `SelectedMediaClip` objects with `clipId: id`, so they do not lack `clipId`; the revised key therefore stops deduping a gallery item and timeline clip that share the same URL, which the existing `AgentChat.tsx:40-75` URL-keyed merge intentionally did.",
    "severity": "significant",
    "status": "open"
  },
  {
    "id": "correctness",
    "concern": "Are the proposed changes technically correct?: Checked Step 7.4's proposed `currentAttachmentSet.ts` import against `selectionStore.ts:690-699`. `useSelectionStore` is currently a private non-exported function, while the plan creates a separate module that imports it from `./selectionStore`; followed literally, that new file will not compile unless the plan either exports a deliberately narrow selector API or colocates `useCurrentAttachmentSet()` inside `selectionStore.ts`.",
    "severity": "significant",
    "status": "addressed"
  },
  {
    "id": "all_locations",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Checked supporting component infrastructure for placeholder rendering. The actual attachment strip lives in `AgentChatMessage.tsx:180-226`, where previews always render `<img src={attachment.url}>` or `<video src={attachment.url}>` and always show the remove button when `onRemoveAttachment` is present; the plan says AgentChat renders placeholder chips and hides the X, but Step 14 only calls out `AgentChat.test.tsx`, not the existing `AgentChatMessage.test.tsx` surface that should exercise this component-level behavior.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "callers",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked the actual attachment merge callers: `AgentChat.tsx` currently passes timeline clips from `useSelectedMediaClips()` and gallery clips from `useGallerySelection().selectedGalleryClips` into the merge. Because both caller paths supply `clipId`, a `clipId || url` key handles placeholder timeline clips but no longer matches the real gallery-vs-timeline same-URL caller case that the old URL-keyed merge handled.",
    "severity": "significant",
    "status": "open"
  },
  {
    "id": "FLAG-011",
    "concern": "Support-test access: revised test instructions depend on direct `selectionStore.getState()` reads even though the plan deletes `useSelectionStoreApi()` and keeps the store private.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-012",
    "concern": "Drag-selection caller contract: the plan lists helper-file drag callbacks but does not explicitly migrate direct `useClipDrag.ts` pointer-up calls that pass `{ toggle: true }` and `{ preserveSelection: true }` through `selectClip`.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-013",
    "concern": "AgentChat bridge support tests: `AppProviders.test.tsx` still depends on `agentChatBridge.timelineClips`, but the revised test migration list only calls out `VideoEditorProvider.test.tsx` for deleted bridge fields.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-014",
    "concern": "Attachment removal matching: the generationId branch is broader than current chip removal semantics because it drops the current URL/mediaType guard.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-015",
    "concern": "Timeline additive selection semantics: migrating `{ toggle: true }` callers to `{ additive: true }` is only safe if `userSelectTimelineClip` explicitly toggles already-selected clips off, but the plan and tests do not state that contract.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "verifiability-2",
    "concern": "Criterion 47: requires human verification (inspect_runtime_ui).",
    "severity": "minor",
    "status": "open"
  },
  {
    "id": "FLAG-016",
    "concern": "Attachment placeholders: placeholder clips use the same empty URL and will collide with the existing URL-based `mergeSelectedClips` dedupe unless the merge key is changed or placeholders get unique keys.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-017",
    "concern": "Current attachment set module: the plan imports `useSelectionStore` from `selectionStore.ts`, but that hook is currently private and not exported.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-018",
    "concern": "Placeholder rendering tests: the plan changes attachment-strip behavior but does not name the component-level test surface for `AgentChatMessage.tsx`.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-019",
    "concern": "Attachment merge key: `clip.clipId || clip.url` fixes placeholder collisions but breaks the existing URL dedupe between timeline and gallery attachments because gallery clips already have `clipId`.",
    "severity": "significant",
    "status": "open"
  },
  {
    "id": "FLAG-020",
    "concern": "Selection store public surface: exporting the raw `useSelectionStore` hook re-exposes low-level Zustand reducer functions despite the intent-facade goal.",
    "severity": "significant",
    "status": "open"
  },
  {
    "id": "FLAG-021",
    "concern": "Frontend environment guard: the planned placeholder warning uses `process.env.NODE_ENV` in a Vite browser module, while the repo uses `import.meta.env.DEV`.",
    "severity": "significant",
    "status": "open"
  }
]

            For each flag above that was raised during critique, verify whether the final diff actually addresses the concern.
            A flag is resolved only if the final diff contains code that directly addresses the concern.
            Do not trust pre-execute promises or plan claims; check the diff itself.
            Add resolved flag IDs to `verified_flag_ids`.
            For any unresolved flag, add a `rework_items` entry with `task_id: "REVIEW"`, `issue`, `expected`, `actual`, `evidence_file`, `flag_id`, and `source: "review_flag_reverify"`.

Advisory mechanical pre-check flags:
            [
  {
    "id": "PRECHECK-DIFF_SIZE_SANITY",
    "check": "diff_size_sanity",
    "detail": "Diff size looks larger than expected: changed_lines=4564, expected\u224820, ratio=228.20, files=71, hunks=242.",
    "severity": "significant",
    "evidence_file": "src/app/App.tsx"
  }
]

            Copy this list verbatim into the output `pre_check_flags` field.

        Execution summary:
        {
  "output": "Aggregated execute batches: completed 7/7.\nBatch 1: Batch 1 complete. Implemented T1 and T10 only, left changes uncommitted, and wrote the batch checkpoint to `.megaplan/plans/selection-coordination-20260426-1613/execution_batch_1.json`.\nBatch 2: Executed batch 2 tasks T2, T3, T5, T6, and T11. Targeted tests, touched-file ESLint, and TypeScript pass. Full Vitest was rerun and now shows the 3 documented baseline failures plus 1 additional AgentChat queue test failure that is outside this batch's actionable scope.\nBatch 3: Executed batch 3 tasks T4, T7, and T12. TypeScript and touched-file ESLint are clean. Full Vitest was run and failed only the 3 documented baseline failures: `GenerationsPane.test.tsx:209` and `dropdown-menu.test.tsx` x2. Checkpoint written to `.megaplan/plans/selection-coordination-20260426-1613/execution_batch_3.json`.\nBatch 4: Executed batch 4 / T8. AgentChat panel requirements were already satisfied by prior bridge work; I completed the remaining placeholder chip rendering in AgentChatMessage and checkpointed the batch update.\nBatch 5: Implemented T9 and checkpointed batch 5 progress.\nBatch 6: Executed batch 6 / T13. Updated the remaining test surface for the new selection facade and attachment composer, added explicit AgentChatMessage placeholder chip coverage, migrated VideoEditorProvider.test.tsx to assert against the real selection store test snapshot, and checkpointed results to `.megaplan/plans/selection-coordination-20260426-1613/execution_batch_6.json`.\nBatch 7: Batch 7 validation completed. Type-check is clean, scoped eslint for the selection/coordination refactor files is clean, targeted test groups pass except the documented gallery failure, and full vitest shows only the 3 documented pre-existing failures. No commits were created; worktree remains dirty for review.",
  "commands_run": [
    "sed -n '1,260p' src/shared/state/selectionStore.ts",
    "sed -n '260,620p' src/shared/state/selectionStore.ts",
    "sed -n '620,920p' src/shared/state/selectionStore.ts",
    "rg \"type SelectedMediaClip|interface SelectedMediaClip|SelectedMediaClip\" src/tools src/shared -n",
    "sed -n '1,220p' src/tools/video-editor/hooks/useSelectedMediaClips.ts",
    "rg \"__resetSelectionStoreForTests|selectionStore\" src/shared src/tools -g \"*.test.*\" -n",
    "rg \"vitest|describe\\(\" src/shared -g \"*.test.ts\" -n | head -40",
    "find src/shared -maxdepth 3 -type d | sort | sed -n '1,120p'",
    "rg \"src/shared/lib\" src -g \"*.ts\" -n | head -30 && test -d src/shared/lib && find src/shared/lib -maxdepth 2 -type f | sort | sed -n '1,80p'",
    "npx vitest run src/shared/lib/interactions/selectionGesture.test.ts",
    "npx eslint src/shared/state/selectionStore.ts src/shared/lib/interactions/selectionGesture.ts src/shared/lib/interactions/selectionGesture.test.ts",
    "npx tsc --noEmit",
    "rg \"^export function (user|composer|editor|system|setTimelineClipData|clearTimelineClipData|__getSelectionStateForTests|useSelectionStore)\" src/shared/state/selectionStore.ts -n",
    "git status --short -- src/shared/state/selectionStore.ts src/shared/lib/interactions/selectionGesture.ts src/shared/lib/interactions/selectionGesture.test.ts .megaplan/plans/selection-coordination-20260426-1613/execution_batch_1.json",
    "git status --short",
    "rg \"useSelectionStoreApi|selectTimelineClip|selectTimelineClips|selectGalleryItem|selectGalleryItems|clearGallerySelection|clearTimelineSelection|deselectGalleryItems|useModifierKeys|isMultiSelectEvent|CLICK_THRESHOLD_PX|clearGallery\" src/",
    "npx vitest run src/shared/state/selectionActions.test.ts src/shared/state/currentAttachmentSet.test.ts",
    "npx vitest run src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx",
    "npx vitest run src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx src/shared/lib/interactions/selectionGesture.test.ts",
    "npx vitest run src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts src/tools/video-editor/hooks/useClipDrag.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx",
    "npx vitest run src/shared/state/selectionActions.test.ts src/shared/state/currentAttachmentSet.test.ts src/shared/lib/interactions/selectionGesture.test.ts src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts src/tools/video-editor/hooks/useClipDrag.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx",
    "npx eslint src/shared/state/selectionStore.ts src/shared/state/currentAttachmentSet.ts src/shared/state/selectionActions.test.ts src/shared/state/currentAttachmentSet.test.ts src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx src/shared/hooks/gallery/useGallerySelectionBridge.ts src/tools/image-generation/pages/ImageGenerationToolPage.tsx src/shared/components/MediaGalleryItem.tsx src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts src/shared/lib/interactions/selectionGesture.ts src/shared/lib/interactions/selectionGesture.test.ts src/tools/video-editor/hooks/useClipDrag.ts src/tools/video-editor/hooks/useClipDrag.helpers.ts src/tools/video-editor/hooks/useClipDrag.test.tsx src/tools/video-editor/hooks/useMarqueeSelect.ts src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx src/tools/video-editor/components/VideoEditorShell.tsx src/tools/video-editor/contexts/VideoEditorProvider.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/useTimelineState.ts src/app/providers/AppProviders.tsx",
    "rg \"useSelectionStoreApi\" src/app/providers/AppProviders.tsx src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/useTimelineState.ts",
    "rg \"clearGallerySelection\\(\\)\" src/tools/video-editor/components/AgentChat/AgentChat.tsx",
    "rg \"userSelectTimelineClip|userSelectTimelineClips|editorReplaceTimelineSelection|editorSelectTimelineClip|editorClearTimelineSelection|editorSetSelectedTrackId|systemResetTimelineSelection|systemResetSelectionForProjectChange\" -n src/tools/video-editor/hooks/useClipDrag.ts src/tools/video-editor/hooks/useClipDrag.helpers.ts src/tools/video-editor/hooks/useMarqueeSelect.ts src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx src/tools/video-editor/components/VideoEditorShell.tsx src/tools/video-editor/contexts/VideoEditorProvider.tsx src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/useTimelineState.ts src/app/providers/AppProviders.tsx",
    "rg \"userSelectGalleryItem|userSelectGalleryItems|systemSyncGallerySelection|systemClearGallerySelection\" -n src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx src/shared/hooks/gallery/useGallerySelectionBridge.ts src/tools/image-generation/pages/ImageGenerationToolPage.tsx",
    "rg \"isAdditiveSelectionEvent|isPrimaryPointer|isClickLikePointerGesture\" -n src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts src/shared/components/MediaGalleryItem.tsx src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts src/tools/image-generation/pages/ImageGenerationToolPage.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx",
    "rg \"useModifierKeys|CLICK_THRESHOLD_PX|isMultiSelectEvent\" src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts src/shared/components/MediaGalleryItem.tsx src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts src/tools/image-generation/pages/ImageGenerationToolPage.tsx",
    "npx vitest run",
    "rg \"useSelectionStoreApi|clearGallery|selectTimelineClip|selectTimelineClips|selectGalleryItem|selectGalleryItems|clearGallerySelection|clearTimelineSelection|deselectGalleryItems|useModifierKeys\" src/",
    "rg \"useSelectionStoreApi\" src/",
    "rg \"useModifierKeys\" src/",
    "rg \"clearGallery\" src/",
    "rg \"timelineClips|replaceSelectedTimelineClips\" src/shared/contexts src/tools/video-editor/contexts src/app/providers src/tools/video-editor/components/AgentChat -g '*.tsx'",
    "npx eslint src/shared/state/selectionStore.ts src/shared/hooks/__tests__/useLastAffectedShot.test.ts src/shared/contexts/AgentChatContext.tsx src/tools/video-editor/contexts/VideoEditorProvider.tsx src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/hooks/useTimelineState.types.ts src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useClipEditing.ts src/tools/video-editor/hooks/clip-editing/types.ts src/tools/video-editor/components/AgentChat/AgentChat.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/app/providers/AppProviders.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx",
    "npx vitest run src/shared/hooks/__tests__/useLastAffectedShot.test.ts src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
    "npx vitest run src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/app/providers/AppProviders.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx",
    "rg -n \"mergeSelectedClips|displayedClips|deselectGalleryMatches|clearGallerySelection|replaceSelectedTimelineClips|timelineClips\" src/tools/video-editor/components/AgentChat/AgentChat.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx",
    "rg -n \"isPlaceholder|Loading|src=\\{attachment.url\\}|onRemoveAttachment\" src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx",
    "npx eslint src/tools/video-editor/components/AgentChat/AgentChat.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx",
    "npx vitest run src/tools/video-editor/components/AgentChat/",
    "npx vitest run src/shared/state/currentAttachmentSet.test.ts src/shared/state/currentAttachmentSet.test.tsx",
    "npx eslint src/shared/state/currentAttachmentSet.test.tsx",
    "git status --short src/shared/state/currentAttachmentSet.test.tsx .megaplan/plans/selection-coordination-20260426-1613/execution_batch_5.json",
    "rg -n \"timelineClips|replaceSelectedTimelineClips|useSelectionStoreApi|selectGalleryItem|selectGalleryItems|clearGallerySelection|deselectGalleryItems|composerRemoveAttachment|composerClearAttachments|useCurrentAttachmentSet|isPlaceholder|Loading\" src/tools/video-editor/components/AgentChat src/tools/video-editor/contexts src/app/providers src/features/gallery/components/GenerationsPane/components src/shared/state -g '*.test.ts*' -g '*.tsx'",
    "rg --files src/tools/video-editor/components/AgentChat src/tools/video-editor/contexts src/app/providers src/features/gallery/components/GenerationsPane/components | rg 'test\\.tsx?$'",
    "npx vitest run src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx",
    "npx vitest run src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/app/providers/AppProviders.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
    "rg -l \"selectionStore|useGallerySelection|useTimelineSelectionStore|useTimelineMultiSelect|__getSelectionStateForTests|composerRemoveAttachment|userSelectGallery|userSelectTimeline|editorReplaceTimelineSelection\" src -g '*.test.ts' -g '*.test.tsx'",
    "npx vitest run src/shared/state/selectionActions.test.ts src/shared/state/currentAttachmentSet.test.ts src/shared/state/currentAttachmentSet.test.tsx src/tools/video-editor/hooks/useClipDrag.test.tsx src/shared/hooks/__tests__/useLastAffectedShot.test.ts src/features/gallery/hooks/__tests__/useGalleryPageState.test.ts src/features/gallery/components/GenerationsPane/hooks/useGenerationsPaneController.test.ts src/tools/edit-images/hooks/__tests__/useInlineEditState.test.ts src/app/hooks/useResetCurrentShotOnRouteChange.test.ts src/shared/hooks/gallery/__tests__/useGalleryFilterState.test.ts src/tools/travel-between-images/components/ShotEditor/index.test.tsx src/tools/travel-between-images/components/VideoGallery/VideoShotDisplay.test.tsx src/shared/hooks/__tests__/useShotNavigation.test.ts",
    "npx vitest run src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx src/app/providers/AppProviders.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
    "npx eslint src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/app/providers/AppProviders.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
    "rg -n \"replaceSelectedTimelineClips|useSelectionStoreApi|selectGalleryItem|selectGalleryItems|clearGallerySelection|deselectGalleryItems|useModifierKeys\" src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/app/providers/AppProviders.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
    "git branch --show-current && git status --short",
    "npx vitest run src/shared/state/ src/shared/lib/interactions/",
    "npx vitest run src/tools/video-editor/components/AgentChat/ src/tools/video-editor/contexts/ src/app/providers/",
    "npx vitest run src/features/gallery/",
    "npx eslint <selection/coordination touched files>",
    "npx vitest run src/shared/state/currentAttachmentSet.repro.test.tsx",
    "rg checks for displayedClips/mergeSelectedClips/useModifierKeys/useSelectionStoreApi/clearGallery/self-review items",
    "git log -1 --oneline && git status --short"
  ],
  "deviations": [
    "T1 requested a \u201cFULL 18-command\u201d set but enumerated 16 distinct commands. I implemented the enumerated commands plus `systemSetCurrentShotId` and `systemSetLastAffectedShotId` as system intent wrappers to satisfy the 18-command sense check without changing existing low-level reducers.",
    "Advisory quality: src/shared/state/selectionStore.ts grew by 349 lines (threshold 200).",
    "Advisory observation mismatch: executor claimed files not observed in git status/content hash delta: .megaplan/plans/selection-coordination-20260426-1613/execution_batch_1.json",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .claude/, .megaplan/bakeoffs/, .megaplan/debt.json, .megaplan/schemas/execution.json, .megaplan/schemas/finalize.json, .megaplan/schemas/prep.json, .megaplan/schemas/revise.json, src/app/App.tsx, src/domains/media-lightbox/components/LightboxShell.tsx, src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx, src/features/tasks/components/TasksPane/TasksPane.tsx, src/integrations/supabase/bootstrap/fetchWithTimeout.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryItemProps.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryViewInteractions.ts, src/shared/components/MediaGallery/types.ts, src/shared/components/MediaGalleryItem.tsx, src/shared/components/MediaGalleryItem/components/ImageContent.tsx, src/shared/components/MediaGalleryItem/components/VideoContent.tsx, src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts, src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts, src/shared/components/MediaGalleryItem/types.ts, src/shared/components/MediaVariantPicker.tsx, src/shared/components/PaneControlTab.tsx, src/shared/components/ui/overlay/shared.tsx, src/shared/components/ui/runtime/sonner.tsx, src/shared/contexts/AgentChatContext.test.tsx, src/shared/contexts/AgentChatContext.tsx, src/shared/hooks/projects/useProjectGenerations.ts, src/shared/lib/uiLayers.test.ts, src/shared/lib/uiLayers.ts, src/shared/state/panesStore.test.ts, src/shared/state/panesStore.ts, src/tools/video-editor/components/AgentChat/AgentChat.test.tsx, src/tools/video-editor/components/AgentChat/AgentChat.tsx, src/tools/video-editor/components/AgentChat/index.ts, src/tools/video-editor/components/PropertiesPanel/ClipPanel.tsx, src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx, src/tools/video-editor/components/TimelineEditor/ClipAction.tsx, src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx, src/tools/video-editor/contexts/VideoEditorProvider.test.tsx, src/tools/video-editor/contexts/VideoEditorProvider.tsx, src/tools/video-editor/hooks/useAddVariantAsGeneration.ts, src/tools/video-editor/hooks/usePollSync.ts, src/tools/video-editor/hooks/useStaleVariants.ts",
    "Advisory audit finding: Sense check SC2 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC3 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC4 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC5 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC6 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC7 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC8 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC11 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC12 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Full `npx vitest run` still has 4 failures: the 3 documented baseline failures (`GenerationsPane.test.tsx:209`, `dropdown-menu.test.tsx` x2) plus one additional `src/tools/video-editor/components/AgentChat/AgentChat.test.tsx` queue/optimistic-state failure. The AgentChat queue behavior is outside this batch and is scheduled for later AgentChat work, so I did not change it here.",
    "T6 requested moving `mergeSelectedClips` out of AgentChat.tsx, while the batch text also says AgentChat composer migrations are deferred to T8. I added the shared `currentAttachmentSet.ts` implementation and tests, but left the local AgentChat merge function in place for T8 to remove with the panel refactor.",
    "T6 wording mentioned merge key `clip.clipId || clip.url`, but the later locked user decision says use `isPlaceholder ? clipId : url`. The implementation follows the later locked decision to preserve URL dedupe for real gallery/timeline duplicates while preventing placeholder collapse.",
    "ImageGenerationToolPage has no raw DOM event at its handler boundary; it now consumes the event-derived modifier argument from the shared MediaGalleryItem gesture path rather than importing `isAdditiveSelectionEvent` directly.",
    "Advisory quality: src/shared/state/currentAttachmentSet.test.ts grew by 219 lines (threshold 200).",
    "Advisory observation mismatch: executor claimed files not observed in git status/content hash delta: .megaplan/plans/selection-coordination-20260426-1613/execution_batch_2.json, src/app/providers/AppProviders.tsx, src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx, src/shared/components/MediaGalleryItem.tsx, src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts, src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts, src/shared/hooks/gallery/useGallerySelectionBridge.ts, src/shared/state/selectionActions.test.ts, src/tools/image-generation/pages/ImageGenerationToolPage.tsx, src/tools/video-editor/components/AgentChat/AgentChat.tsx, src/tools/video-editor/components/VideoEditorShell.tsx, src/tools/video-editor/hooks/useClipDrag.helpers.ts, src/tools/video-editor/hooks/useMarqueeSelect.ts, src/tools/video-editor/hooks/useSelectedMediaClips.ts, src/tools/video-editor/hooks/useTimelineCommit.ts",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .claude/, .megaplan/bakeoffs/, .megaplan/debt.json, .megaplan/schemas/execution.json, .megaplan/schemas/finalize.json, .megaplan/schemas/prep.json, .megaplan/schemas/revise.json, src/app/App.tsx, src/domains/media-lightbox/components/LightboxShell.tsx, src/features/tasks/components/TasksPane/TasksPane.tsx, src/integrations/supabase/bootstrap/fetchWithTimeout.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryItemProps.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryViewInteractions.ts, src/shared/components/MediaGallery/types.ts, src/shared/components/MediaGalleryItem/components/ImageContent.tsx, src/shared/components/MediaGalleryItem/components/VideoContent.tsx, src/shared/components/MediaGalleryItem/types.ts, src/shared/components/MediaVariantPicker.tsx, src/shared/components/PaneControlTab.tsx, src/shared/components/ui/overlay/shared.tsx, src/shared/components/ui/runtime/sonner.tsx, src/shared/contexts/AgentChatContext.test.tsx, src/shared/contexts/AgentChatContext.tsx, src/shared/hooks/projects/useProjectGenerations.ts, src/shared/lib/uiLayers.test.ts, src/shared/lib/uiLayers.ts, src/shared/state/panesStore.test.ts, src/shared/state/panesStore.ts, src/tools/video-editor/components/AgentChat/AgentChat.test.tsx, src/tools/video-editor/components/AgentChat/AgentChat.tsx, src/tools/video-editor/components/AgentChat/index.ts, src/tools/video-editor/components/PropertiesPanel/ClipPanel.tsx, src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx, src/tools/video-editor/components/TimelineEditor/ClipAction.tsx, src/tools/video-editor/hooks/useAddVariantAsGeneration.ts, src/tools/video-editor/hooks/usePollSync.ts, src/tools/video-editor/hooks/useStaleVariants.ts",
    "Advisory audit finding: Sense check SC4 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC7 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC8 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC12 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "T7 required slimming AgentChatContext to remove timelineClips and replaceSelectedTimelineClips; to keep the codebase compiling, I updated direct AgentChat bridge consumers/tests to use currentAttachmentSet/composer intents. This overlaps slightly with later AgentChat refactor scope but was necessary after deleting the bridge fields.",
    "`rg \"clearGallery\" src/` still reports internal low-level reducer definitions/comments in `selectionStore.ts`; there are no hits outside `selectionStore.ts`.",
    "Full Vitest failed only the 3 documented baseline failures.",
    "Advisory observation mismatch: executor claimed files not observed in git status/content hash delta: .megaplan/plans/selection-coordination-20260426-1613/execution_batch_3.json",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .claude/, .megaplan/bakeoffs/, .megaplan/debt.json, .megaplan/schemas/execution.json, .megaplan/schemas/finalize.json, .megaplan/schemas/prep.json, .megaplan/schemas/revise.json, src/app/App.tsx, src/domains/media-lightbox/components/LightboxShell.tsx, src/features/tasks/components/TasksPane/TasksPane.tsx, src/integrations/supabase/bootstrap/fetchWithTimeout.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryItemProps.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryViewInteractions.ts, src/shared/components/MediaGallery/types.ts, src/shared/components/MediaGalleryItem/components/ImageContent.tsx, src/shared/components/MediaGalleryItem/components/VideoContent.tsx, src/shared/components/MediaGalleryItem/types.ts, src/shared/components/MediaVariantPicker.tsx, src/shared/components/PaneControlTab.tsx, src/shared/components/ui/overlay/shared.tsx, src/shared/components/ui/runtime/sonner.tsx, src/shared/contexts/AgentChatContext.test.tsx, src/shared/hooks/projects/useProjectGenerations.ts, src/shared/lib/uiLayers.test.ts, src/shared/lib/uiLayers.ts, src/shared/state/panesStore.test.ts, src/shared/state/panesStore.ts, src/tools/video-editor/components/AgentChat/index.ts, src/tools/video-editor/components/PropertiesPanel/ClipPanel.tsx, src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx, src/tools/video-editor/components/TimelineEditor/ClipAction.tsx, src/tools/video-editor/hooks/useAddVariantAsGeneration.ts, src/tools/video-editor/hooks/usePollSync.ts, src/tools/video-editor/hooks/useStaleVariants.ts",
    "Advisory audit finding: Sense check SC8 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "AgentChat.tsx panel migration was already present from the prior T7 overlap needed after slimming the bridge; this batch verified it instead of re-editing it.",
    "Advisory observation mismatch: executor claimed files not observed in git status/content hash delta: .megaplan/plans/selection-coordination-20260426-1613/execution_batch_4.json",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .claude/, .megaplan/bakeoffs/, .megaplan/debt.json, .megaplan/schemas/execution.json, .megaplan/schemas/finalize.json, .megaplan/schemas/prep.json, .megaplan/schemas/revise.json, src/app/App.tsx, src/domains/media-lightbox/components/LightboxShell.tsx, src/features/tasks/components/TasksPane/TasksPane.tsx, src/integrations/supabase/bootstrap/fetchWithTimeout.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryItemProps.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryViewInteractions.ts, src/shared/components/MediaGallery/types.ts, src/shared/components/MediaGalleryItem/components/ImageContent.tsx, src/shared/components/MediaGalleryItem/components/VideoContent.tsx, src/shared/components/MediaGalleryItem/types.ts, src/shared/components/MediaVariantPicker.tsx, src/shared/components/PaneControlTab.tsx, src/shared/components/ui/overlay/shared.tsx, src/shared/components/ui/runtime/sonner.tsx, src/shared/contexts/AgentChatContext.test.tsx, src/shared/hooks/projects/useProjectGenerations.ts, src/shared/lib/uiLayers.test.ts, src/shared/lib/uiLayers.ts, src/shared/state/panesStore.test.ts, src/shared/state/panesStore.ts, src/tools/video-editor/components/AgentChat/index.ts, src/tools/video-editor/components/PropertiesPanel/ClipPanel.tsx, src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx, src/tools/video-editor/components/TimelineEditor/ClipAction.tsx, src/tools/video-editor/hooks/useAddVariantAsGeneration.ts, src/tools/video-editor/hooks/usePollSync.ts, src/tools/video-editor/hooks/useStaleVariants.ts",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .claude/, .megaplan/bakeoffs/, .megaplan/debt.json, .megaplan/schemas/execution.json, .megaplan/schemas/finalize.json, .megaplan/schemas/prep.json, .megaplan/schemas/revise.json, src/app/App.tsx, src/domains/media-lightbox/components/LightboxShell.tsx, src/features/tasks/components/TasksPane/TasksPane.tsx, src/integrations/supabase/bootstrap/fetchWithTimeout.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryItemProps.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryViewInteractions.ts, src/shared/components/MediaGallery/types.ts, src/shared/components/MediaGalleryItem/components/ImageContent.tsx, src/shared/components/MediaGalleryItem/components/VideoContent.tsx, src/shared/components/MediaGalleryItem/types.ts, src/shared/components/MediaVariantPicker.tsx, src/shared/components/PaneControlTab.tsx, src/shared/components/ui/overlay/shared.tsx, src/shared/components/ui/runtime/sonner.tsx, src/shared/contexts/AgentChatContext.test.tsx, src/shared/hooks/projects/useProjectGenerations.ts, src/shared/lib/uiLayers.test.ts, src/shared/lib/uiLayers.ts, src/shared/state/panesStore.test.ts, src/shared/state/panesStore.ts, src/tools/video-editor/components/AgentChat/index.ts, src/tools/video-editor/components/PropertiesPanel/ClipPanel.tsx, src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx, src/tools/video-editor/components/TimelineEditor/ClipAction.tsx, src/tools/video-editor/hooks/useAddVariantAsGeneration.ts, src/tools/video-editor/hooks/usePollSync.ts, src/tools/video-editor/hooks/useStaleVariants.ts",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Advisory observation mismatch: executor claimed files not observed in git status/content hash delta: .megaplan/plans/selection-coordination-20260426-1613/execution_batch_6.json",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .claude/, .megaplan/bakeoffs/, .megaplan/debt.json, .megaplan/schemas/execution.json, .megaplan/schemas/finalize.json, .megaplan/schemas/prep.json, .megaplan/schemas/revise.json, src/app/App.tsx, src/domains/media-lightbox/components/LightboxShell.tsx, src/features/tasks/components/TasksPane/TasksPane.tsx, src/integrations/supabase/bootstrap/fetchWithTimeout.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryItemProps.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryViewInteractions.ts, src/shared/components/MediaGallery/types.ts, src/shared/components/MediaGalleryItem/components/ImageContent.tsx, src/shared/components/MediaGalleryItem/components/VideoContent.tsx, src/shared/components/MediaGalleryItem/types.ts, src/shared/components/MediaVariantPicker.tsx, src/shared/components/PaneControlTab.tsx, src/shared/components/ui/overlay/shared.tsx, src/shared/components/ui/runtime/sonner.tsx, src/shared/contexts/AgentChatContext.test.tsx, src/shared/hooks/projects/useProjectGenerations.ts, src/shared/lib/uiLayers.test.ts, src/shared/lib/uiLayers.ts, src/shared/state/panesStore.test.ts, src/shared/state/panesStore.ts, src/tools/video-editor/components/AgentChat/index.ts, src/tools/video-editor/components/PropertiesPanel/ClipPanel.tsx, src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx, src/tools/video-editor/components/TimelineEditor/ClipAction.tsx, src/tools/video-editor/hooks/useAddVariantAsGeneration.ts, src/tools/video-editor/hooks/usePollSync.ts, src/tools/video-editor/hooks/useStaleVariants.ts",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Best-effort checkpoint was skipped because .megaplan/plans/selection-coordination-20260426-1613/execution_batch_7.json does not exist and was not writable as a file path.",
    "A broad eslint sweep across every dirty TS/TSX file hit unrelated WIP lint errors in PropertiesPanel/ClipPanel/useAddVariantAsGeneration/useStaleVariants. Scoped eslint for the selection/coordination files passed cleanly.",
    "Made a small validation cleanup in ImageContent.tsx and VideoContent.tsx to stop destructuring now-unused inner click props after the wrapper-level click refactor.",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .claude/, .megaplan/bakeoffs/, .megaplan/debt.json, .megaplan/schemas/execution.json, .megaplan/schemas/finalize.json, .megaplan/schemas/prep.json, .megaplan/schemas/revise.json, src/app/App.tsx, src/domains/media-lightbox/components/LightboxShell.tsx, src/features/tasks/components/TasksPane/TasksPane.tsx, src/integrations/supabase/bootstrap/fetchWithTimeout.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryItemProps.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryViewInteractions.ts, src/shared/components/MediaGallery/types.ts, src/shared/components/MediaGalleryItem/types.ts, src/shared/components/MediaVariantPicker.tsx, src/shared/components/PaneControlTab.tsx, src/shared/components/ui/overlay/shared.tsx, src/shared/components/ui/runtime/sonner.tsx, src/shared/contexts/AgentChatContext.test.tsx, src/shared/hooks/projects/useProjectGenerations.ts, src/shared/lib/uiLayers.test.ts, src/shared/lib/uiLayers.ts, src/shared/state/panesStore.test.ts, src/shared/state/panesStore.ts, src/tools/video-editor/components/AgentChat/index.ts, src/tools/video-editor/components/PropertiesPanel/ClipPanel.tsx, src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx, src/tools/video-editor/components/TimelineEditor/ClipAction.tsx, src/tools/video-editor/hooks/useAddVariantAsGeneration.ts, src/tools/video-editor/hooks/usePollSync.ts, src/tools/video-editor/hooks/useStaleVariants.ts"
  ],
  "task_updates": [
    {
      "task_id": "T1",
      "status": "done",
      "executor_notes": "Added intent facade exports in selectionStore.ts: user/composer/editor/system selection commands, clipDataById state, setTimelineClipData(), clearTimelineClipData(), exported useSelectionStore(), and __getSelectionStateForTests(). Timeline single additive is documented and implemented as TOGGLE; timeline marquee additive is documented and implemented as APPEND. Existing low-level reducers remain in place and share extracted timeline compute helpers. Verified with `npx tsc --noEmit` and touched-file ESLint.",
      "files_changed": [
        "src/shared/state/selectionStore.ts"
      ],
      "commands_run": [
        "npx eslint src/shared/state/selectionStore.ts src/shared/lib/interactions/selectionGesture.ts src/shared/lib/interactions/selectionGesture.test.ts",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": false
    },
    {
      "task_id": "T10",
      "status": "done",
      "executor_notes": "Created stateless gesture primitives and unit coverage for additive modifier detection, primary pointer detection, and click-like pointer movement threshold behavior. Verified the full new test file passes.",
      "files_changed": [
        "src/shared/lib/interactions/selectionGesture.ts",
        "src/shared/lib/interactions/selectionGesture.test.ts"
      ],
      "commands_run": [
        "npx vitest run src/shared/lib/interactions/selectionGesture.test.ts",
        "npx eslint src/shared/state/selectionStore.ts src/shared/lib/interactions/selectionGesture.ts src/shared/lib/interactions/selectionGesture.test.ts",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": false
    },
    {
      "task_id": "T2",
      "status": "done",
      "executor_notes": "Migrated listed timeline/editor/system call sites to intent commands and updated directly affected tests. Verified no useSelectionStoreApi imports remain in AppProviders.tsx, useTimelineCommit.ts, or useTimelineState.ts; AgentChat.tsx no longer calls clearGallerySelection().",
      "files_changed": [
        "src/app/providers/AppProviders.tsx",
        "src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx",
        "src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx",
        "src/tools/video-editor/components/VideoEditorShell.tsx",
        "src/tools/video-editor/contexts/VideoEditorProvider.tsx",
        "src/tools/video-editor/contexts/VideoEditorProvider.test.tsx",
        "src/tools/video-editor/hooks/useClipDrag.ts",
        "src/tools/video-editor/hooks/useClipDrag.helpers.ts",
        "src/tools/video-editor/hooks/useClipDrag.test.tsx",
        "src/tools/video-editor/hooks/useMarqueeSelect.ts",
        "src/tools/video-editor/hooks/useTimelineCommit.ts",
        "src/tools/video-editor/hooks/useTimelineState.ts"
      ],
      "commands_run": [
        "rg \"useSelectionStoreApi\" src/app/providers/AppProviders.tsx src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/useTimelineState.ts",
        "rg \"clearGallerySelection\\(\\)\" src/tools/video-editor/components/AgentChat/AgentChat.tsx",
        "npx vitest run src/tools/video-editor/hooks/useClipDrag.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T3",
      "status": "done",
      "executor_notes": "Migrated gallery bridge and gallery click/lasso consumers to intent commands. GenerationsPaneGallery now uses userSelectGalleryItem(s), ImageGenerationToolPage uses userSelectGalleryItem from event-derived modifiers, and useGallerySelectionBridge uses systemSyncGallerySelection/systemClearGallerySelection.",
      "files_changed": [
        "src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx",
        "src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
        "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts",
        "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx",
        "src/shared/hooks/gallery/useGallerySelectionBridge.ts",
        "src/tools/image-generation/pages/ImageGenerationToolPage.tsx"
      ],
      "commands_run": [
        "rg \"userSelectGalleryItem|userSelectGalleryItems|systemSyncGallerySelection|systemClearGallerySelection\" -n src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx src/shared/hooks/gallery/useGallerySelectionBridge.ts src/tools/image-generation/pages/ImageGenerationToolPage.tsx",
        "npx vitest run src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T5",
      "status": "done",
      "executor_notes": "Added/kept selectionActions.test.ts coverage for intent contracts: gallery intents preserve timeline, timeline single additive toggles and clears gallery, timeline marquee additive appends and clears gallery, preserveIfSelected no-ops, editor intents preserve gallery, and system intents reset/sync/clear per contract. Composer matcher coverage lives in currentAttachmentSet.test.ts.",
      "files_changed": [
        "src/shared/state/selectionActions.test.ts"
      ],
      "commands_run": [
        "npx vitest run src/shared/state/selectionActions.test.ts src/shared/state/currentAttachmentSet.test.ts"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T6",
      "status": "done",
      "executor_notes": "Added currentAttachmentSet.ts with mergeSelectedClips, makePlaceholderClip, and useCurrentAttachmentSet using import.meta.env.DEV placeholder warnings. Implemented chip-specific composerRemoveAttachment matcher and composerClearAttachments in selectionStore.ts, and added currentAttachmentSet.test.ts coverage for the 6 matcher paths, placeholders, partial clip-data resolution, dev warnings, and URL fallback merge behavior.",
      "files_changed": [
        "src/shared/state/currentAttachmentSet.ts",
        "src/shared/state/currentAttachmentSet.test.ts",
        "src/shared/state/selectionStore.ts",
        "src/tools/video-editor/hooks/useSelectedMediaClips.ts"
      ],
      "commands_run": [
        "npx vitest run src/shared/state/selectionActions.test.ts src/shared/state/currentAttachmentSet.test.ts",
        "npx eslint src/shared/state/selectionStore.ts src/shared/state/currentAttachmentSet.ts src/shared/state/selectionActions.test.ts src/shared/state/currentAttachmentSet.test.ts",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T11",
      "status": "done",
      "executor_notes": "Migrated gesture call sites to selectionGesture primitives. useLassoSelection uses isPrimaryPointer/isAdditiveSelectionEvent, MediaGalleryItem uses isPrimaryPointer/isClickLikePointerGesture/isAdditiveSelectionEvent, useItemInteraction uses isAdditiveSelectionEvent, and GenerationsPaneGallery no longer uses the useModifierKeys fallback.",
      "files_changed": [
        "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts",
        "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx",
        "src/shared/components/MediaGalleryItem.tsx",
        "src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts",
        "src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts",
        "src/shared/lib/interactions/selectionGesture.ts"
      ],
      "commands_run": [
        "rg \"useModifierKeys|CLICK_THRESHOLD_PX|isMultiSelectEvent\" src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts src/shared/components/MediaGalleryItem.tsx src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts src/tools/image-generation/pages/ImageGenerationToolPage.tsx",
        "npx vitest run src/shared/lib/interactions/selectionGesture.test.ts src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T4",
      "status": "done",
      "executor_notes": "Privatized the shared selection hook surface: useGallerySelection() and useTimelineSelectionStore() are state-only, useSelectionStoreApi() was deleted, and useTimelineMultiSelect() no longer exposes selectClip/selectClips/addToSelection/clearSelection or clearGallery sync options. Migrated useLastAffectedShot.test.ts to systemSetLastAffectedShotId + __getSelectionStateForTests(). `rg \"useSelectionStoreApi|useModifierKeys\" src/` returns zero hits; `rg \"clearGallery\" src/` is confined to internal low-level reducer definitions/comments in selectionStore.ts.",
      "files_changed": [
        "src/shared/state/selectionStore.ts",
        "src/shared/hooks/__tests__/useLastAffectedShot.test.ts",
        "src/tools/video-editor/hooks/useTimelineState.ts",
        "src/tools/video-editor/hooks/useTimelineState.types.ts",
        "src/tools/video-editor/hooks/useAssetManagement.ts",
        "src/tools/video-editor/hooks/useClipEditing.ts",
        "src/tools/video-editor/hooks/clip-editing/types.ts"
      ],
      "commands_run": [
        "rg \"useSelectionStoreApi\" src/",
        "rg \"clearGallery\" src/",
        "rg \"selectTimelineClip|selectTimelineClips|selectGalleryItem|selectGalleryItems|clearGallerySelection|clearTimelineSelection|deselectGalleryItems|addTimelineClips|pruneTimelineSelection|resetTimelineSelection\" src/ -g '*.ts*'",
        "npx vitest run src/shared/hooks/__tests__/useLastAffectedShot.test.ts src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
        "npx tsc --noEmit",
        "npx eslint <touched files>"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T7",
      "status": "done",
      "executor_notes": "Added useTimelineClipsForAttachments() to derive all timeline attachment metadata from editor data, not selection. VideoEditorProvider now writes those entries to clipDataById via setTimelineClipData() and clears them on cleanup; AgentChatContext now exposes only timelineId plus the existing actions registry. Updated direct bridge consumers/tests so no timelineClips or replaceSelectedTimelineClips bridge fields remain.",
      "files_changed": [
        "src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts",
        "src/tools/video-editor/contexts/VideoEditorProvider.tsx",
        "src/shared/contexts/AgentChatContext.tsx",
        "src/tools/video-editor/components/AgentChat/AgentChat.tsx",
        "src/tools/video-editor/components/AgentChat/AgentChat.test.tsx",
        "src/tools/video-editor/contexts/VideoEditorProvider.test.tsx",
        "src/app/providers/AppProviders.test.tsx"
      ],
      "commands_run": [
        "rg \"timelineClips|replaceSelectedTimelineClips\" src/shared/contexts src/tools/video-editor/contexts src/app/providers src/tools/video-editor/components/AgentChat -g '*.tsx'",
        "npx vitest run src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/app/providers/AppProviders.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx",
        "npx tsc --noEmit",
        "npx eslint <touched files>"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T12",
      "status": "done",
      "executor_notes": "Deleted useModifierKeys.ts and useModifierKeys.test.tsx after confirming no remaining importers. Removed the stale GenerationsPaneGallery.test.tsx mock and state setup for useModifierKeys.",
      "files_changed": [
        "src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.ts",
        "src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.test.tsx",
        "src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx"
      ],
      "commands_run": [
        "rg \"useModifierKeys\" src/",
        "npx vitest run src/shared/hooks/__tests__/useLastAffectedShot.test.ts src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
        "npx tsc --noEmit",
        "npx eslint <touched files>"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T8",
      "status": "done",
      "executor_notes": "AgentChat.tsx already had the T8 panel migration from dependency bridge work: no local mergeSelectedClips, no displayedClips grace window, no deselectGalleryMatches, uses useCurrentAttachmentSet(), composerRemoveAttachment(), and composerClearAttachments(). Completed the remaining AgentChatMessage chip work: AgentChatAttachmentPreviewItem carries isPlaceholder; placeholder chips render a same-size loading slot with no media src binding and no remove button; real chips still render media and X normally. Verified with rg checks, AgentChat component tests, touched-file ESLint, and tsc.",
      "files_changed": [
        "src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx"
      ],
      "commands_run": [
        "rg -n \"mergeSelectedClips|displayedClips|deselectGalleryMatches|clearGallerySelection|replaceSelectedTimelineClips|timelineClips\" src/tools/video-editor/components/AgentChat/AgentChat.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx",
        "rg -n \"isPlaceholder|Loading|src=\\{attachment.url\\}|onRemoveAttachment\" src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx",
        "npx eslint src/tools/video-editor/components/AgentChat/AgentChat.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx",
        "npx vitest run src/tools/video-editor/components/AgentChat/",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T9",
      "status": "done",
      "executor_notes": "Added currentAttachmentSet.test.tsx render-flow regression coverage for the flicker invariant: steady real-data transition, additive marquee same-render real attachments and gallery clearing, single placeholder gap fill with dev warning and later real-data resolution, additive single-clip toggle off, and the two-placeholder merge-key contract through partial/full data resolution. The paired composer/currentAttachmentSet test files pass, touched-file ESLint is clean, and TypeScript is clean.",
      "files_changed": [
        "src/shared/state/currentAttachmentSet.test.tsx"
      ],
      "commands_run": [
        "npx vitest run src/shared/state/currentAttachmentSet.test.ts src/shared/state/currentAttachmentSet.test.tsx",
        "npx eslint src/shared/state/currentAttachmentSet.test.tsx",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T13",
      "status": "done",
      "executor_notes": "Updated the T13 test surface for the new public selection/attachment API. AgentChat.test.tsx already mocked composerRemoveAttachment/composerClearAttachments and currentAttachmentSet; AppProviders.test.tsx already asserts only agent-chat timelineId; GenerationsPaneGallery.test.tsx already mocks userSelectGalleryItem/userSelectGalleryItems; VideoEditorProvider.test.tsx now uses the real selection store via __getSelectionStateForTests(), validates clipDataById from useTimelineClipsForAttachments, and adds editorReplaceTimelineSelection coverage preserving gallery state. Added AgentChatMessage.test.tsx placeholder-chip assertions for loading state, no img/video src binding, no remove button, normal real-chip src/remove behavior, and equal chip dimensions. Targeted tests, broader selection-store consumer spot-check, touched-file ESLint, and npx tsc --noEmit all pass.",
      "files_changed": [
        "src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx",
        "src/tools/video-editor/contexts/VideoEditorProvider.test.tsx"
      ],
      "commands_run": [
        "npx vitest run src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx src/app/providers/AppProviders.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
        "npx vitest run src/shared/state/selectionActions.test.ts src/shared/state/currentAttachmentSet.test.ts src/shared/state/currentAttachmentSet.test.tsx src/tools/video-editor/hooks/useClipDrag.test.tsx src/shared/hooks/__tests__/useLastAffectedShot.test.ts src/features/gallery/hooks/__tests__/useGalleryPageState.test.ts src/features/gallery/components/GenerationsPane/hooks/useGenerationsPaneController.test.ts src/tools/edit-images/hooks/__tests__/useInlineEditState.test.ts src/app/hooks/useResetCurrentShotOnRouteChange.test.ts src/shared/hooks/gallery/__tests__/useGalleryFilterState.test.ts src/tools/travel-between-images/components/ShotEditor/index.test.tsx src/tools/travel-between-images/components/VideoGallery/VideoShotDisplay.test.tsx src/shared/hooks/__tests__/useShotNavigation.test.ts",
        "npx eslint src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/app/providers/AppProviders.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
        "npx tsc --noEmit"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T14",
      "status": "done",
      "executor_notes": "Validation complete. Targeted vitest group 1 passed: `npx vitest run src/shared/state/ src/shared/lib/interactions/` = 10 files / 53 tests passed. Targeted group 2 passed: AgentChat/contexts/app providers = 5 files / 29 tests passed. Gallery group had only the documented pre-existing failure at `src/features/gallery/components/GenerationsPane/GenerationsPane.test.tsx:209`; all other gallery tests passed. `npx tsc --noEmit` is clean. Scoped eslint for the selection/coordination touched files is clean after removing unused `enableSingleClick`/`onImageClick` destructuring in ImageContent/VideoContent. Full `npx vitest run` completed with exactly the 3 documented pre-existing failures: `GenerationsPane.test.tsx:209` and `dropdown-menu.test.tsx` x2; 895 files / 4621 tests passed. Temporary repro test confirmed clips length stays `[2,2,2]` through placeholder -> partial real -> full real transition, then the repro file was deleted. Self-review checks passed: wrapper pointerdown/up remains, `onImageClick(image, modifiers)` remains, fetchWithTimeout HEAD diagnostic logger remains, AgentChat Clear button remains, `displayedClips` is removed, local AgentChat `mergeSelectedClips` is removed, `useModifierKeys.ts` and its test are deleted, AgentChatContext exposes `timelineId` only plus action registries, `useSelectionStoreApi` has zero hits, and no commits were created. HEAD remains `95d94b780`; working tree is still uncommitted/dirty.",
      "files_changed": [
        "src/shared/components/MediaGalleryItem/components/ImageContent.tsx",
        "src/shared/components/MediaGalleryItem/components/VideoContent.tsx"
      ],
      "commands_run": [
        "npx vitest run src/shared/state/ src/shared/lib/interactions/",
        "npx vitest run src/tools/video-editor/components/AgentChat/ src/tools/video-editor/contexts/ src/app/providers/",
        "npx vitest run src/features/gallery/",
        "npx tsc --noEmit",
        "npx eslint src/app/providers/AppProviders.test.tsx src/app/providers/AppProviders.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts src/integrations/supabase/bootstrap/fetchWithTimeout.ts src/shared/components/MediaGalleryItem.tsx src/shared/components/MediaGalleryItem/components/ImageContent.tsx src/shared/components/MediaGalleryItem/components/VideoContent.tsx src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts src/shared/contexts/AgentChatContext.tsx src/shared/hooks/__tests__/useLastAffectedShot.test.ts src/shared/hooks/gallery/useGallerySelectionBridge.ts src/shared/lib/interactions/selectionGesture.test.ts src/shared/lib/interactions/selectionGesture.ts src/shared/state/currentAttachmentSet.test.ts src/shared/state/currentAttachmentSet.test.tsx src/shared/state/currentAttachmentSet.ts src/shared/state/selectionActions.test.ts src/shared/state/selectionStore.ts src/tools/image-generation/pages/ImageGenerationToolPage.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx src/tools/video-editor/components/VideoEditorShell.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.tsx src/tools/video-editor/hooks/clip-editing/types.ts src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useClipDrag.helpers.ts src/tools/video-editor/hooks/useClipDrag.test.tsx src/tools/video-editor/hooks/useClipDrag.ts src/tools/video-editor/hooks/useClipEditing.ts src/tools/video-editor/hooks/useMarqueeSelect.ts src/tools/video-editor/hooks/useSelectedMediaClips.ts src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/hooks/useTimelineState.types.ts",
        "npx tsc --noEmit",
        "npx vitest run",
        "npx vitest run src/shared/state/currentAttachmentSet.repro.test.tsx",
        "test ! -e src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.ts && test ! -e src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.test.tsx && echo deleted",
        "rg \"useSelectionStoreApi\" src/ || true",
        "rg \"useModifierKeys\" src/ || true",
        "rg \"clearGallery\" src/ || true",
        "git log -1 --oneline && git status --short"
      ],
      "auto_attributed_files": null
    }
  ],
  "sense_check_acknowledgments": [
    {
      "sense_check_id": "SC1",
      "executor_note": "Yes. selectionStore.ts exports 18 intent commands, setTimelineClipData, clearTimelineClipData, __getSelectionStateForTests, and useSelectionStore. The additive TOGGLE-vs-APPEND distinction is doc-commented. Low-level reducers remain in place for later migration/privatization."
    },
    {
      "sense_check_id": "SC10",
      "executor_note": "Yes. selectionGesture.ts exports isAdditiveSelectionEvent, isPrimaryPointer, and isClickLikePointerGesture as small stateless helpers, with unit tests in place."
    },
    {
      "sense_check_id": "SC2",
      "executor_note": "Covered the listed timeline/editor/system call sites. useTimelineCommit.ts, useTimelineState.ts, and AppProviders.tsx are free of useSelectionStoreApi imports. AgentChat.tsx lines formerly calling clearGallerySelection now use composerClearAttachments."
    },
    {
      "sense_check_id": "SC3",
      "executor_note": "GenerationsPaneGallery, lasso selection consumer, ImageGenerationToolPage, and useGallerySelectionBridge use intent commands. useModifierKeys is no longer authoritative in the gallery click path; click modifiers come from the interaction event."
    },
    {
      "sense_check_id": "SC5",
      "executor_note": "selectionActions.test.ts covers the locked cross-surface contracts for user, editor, and system intents. composerRemoveAttachment coverage is in currentAttachmentSet.test.ts as planned."
    },
    {
      "sense_check_id": "SC6",
      "executor_note": "currentAttachmentSet.ts uses the user-approved placeholder-safe merge key policy, import.meta.env.DEV for warnings, and tests cover the 6 matcher paths, single/two placeholders, partial resolution, dev warn, and URL fallback merge. composerRemoveAttachment requires url+mediaType on known clips, with generationId and timeline-side clipId as narrowing disambiguators."
    },
    {
      "sense_check_id": "SC11",
      "executor_note": "MediaGalleryItem, useItemInteraction, and useLassoSelection use selectionGesture.ts primitives. GenerationsPaneGallery has no useModifierKeys fallback. ImageGenerationToolPage consumes the event-derived modifier argument produced by the shared gesture path."
    },
    {
      "sense_check_id": "SC4",
      "executor_note": "Yes. useGallerySelection() / useTimelineSelectionStore() no longer return mutation methods; useSelectionStoreApi() is deleted and has zero rg hits; useTimelineMultiSelect() dropped selectClip/selectClips/addToSelection/clearSelection and clearGallery sync options. clearGallery remains only inside selectionStore.ts internal low-level reducer code/comments."
    },
    {
      "sense_check_id": "SC7",
      "executor_note": "Yes. useTimelineClipsForAttachments() returns all timeline clips' attachment data from editor resolved data. VideoEditorProvider syncs that list into clipDataById with setTimelineClipData() and clears it on cleanup. AgentChatContext exposes timelineId plus the existing actions registry only."
    },
    {
      "sense_check_id": "SC12",
      "executor_note": "Yes. useModifierKeys.ts and its companion test are deleted, rg \"useModifierKeys\" src/ returns zero hits, and GenerationsPaneGallery.test.tsx no longer mocks it."
    },
    {
      "sense_check_id": "SC8",
      "executor_note": "Yes. AgentChat.tsx has no mergeSelectedClips/displayedClips/deselectGalleryMatches and uses composer intents. AgentChatMessage.tsx renders placeholder chips as fixed h-10/w-10 loading slots without img/video src binding or X button, while non-placeholder chips keep normal media rendering and removal."
    },
    {
      "sense_check_id": "SC9",
      "executor_note": "Yes. currentAttachmentSet.test.tsx includes all 5 requested render-flow tests. Test 5 has the requested header note and asserts the two unknown clipIds render as length 2, then remain length 2 through partial and full setTimelineClipData resolution."
    },
    {
      "sense_check_id": "SC13",
      "executor_note": "Yes. AgentChat.test.tsx, AgentChatMessage.test.tsx, VideoEditorProvider.test.tsx, AppProviders.test.tsx, and GenerationsPaneGallery.test.tsx are updated for the new surface. AgentChatMessage.test.tsx covers placeholder loading/no media binding/no X, real chip src+X behavior, and matching slot dimensions. VideoEditorProvider.test.tsx uses __getSelectionStateForTests() to assert clipDataById and timeline.selectedClipIds behavior."
    },
    {
      "sense_check_id": "SC14",
      "executor_note": "`npx tsc --noEmit` is clean. Full `npx vitest run` shows only the 3 documented pre-existing failures: `GenerationsPane.test.tsx:209` and two `dropdown-menu.test.tsx` overlay z-index assertions. Scoped eslint on the selection/coordination touched files is clean. No commits were created; HEAD remains `95d94b780` and `git status --short` shows uncommitted dirty worktree changes. Iter-0 retained fixes verified: MediaGalleryItem wrapper pointerdown/up remains, `onImageClick(image, modifiers)` signature remains, fetchWithTimeout HEAD/4xx diagnostic logger remains, and AgentChat Clear button calls `composerClearAttachments()`."
    }
  ],
  "files_changed": [
    "src/shared/state/selectionStore.ts",
    "src/shared/lib/interactions/selectionGesture.ts",
    "src/shared/lib/interactions/selectionGesture.test.ts",
    ".megaplan/plans/selection-coordination-20260426-1613/execution_batch_1.json",
    ".megaplan/plans/selection-coordination-20260426-1613/execution_batch_2.json",
    "src/app/providers/AppProviders.tsx",
    "src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
    "src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx",
    "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx",
    "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts",
    "src/shared/components/MediaGalleryItem.tsx",
    "src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts",
    "src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts",
    "src/shared/hooks/gallery/useGallerySelectionBridge.ts",
    "src/shared/state/currentAttachmentSet.test.ts",
    "src/shared/state/currentAttachmentSet.ts",
    "src/shared/state/selectionActions.test.ts",
    "src/tools/image-generation/pages/ImageGenerationToolPage.tsx",
    "src/tools/video-editor/components/AgentChat/AgentChat.tsx",
    "src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx",
    "src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx",
    "src/tools/video-editor/components/VideoEditorShell.tsx",
    "src/tools/video-editor/contexts/VideoEditorProvider.test.tsx",
    "src/tools/video-editor/contexts/VideoEditorProvider.tsx",
    "src/tools/video-editor/hooks/useClipDrag.helpers.ts",
    "src/tools/video-editor/hooks/useClipDrag.test.tsx",
    "src/tools/video-editor/hooks/useClipDrag.ts",
    "src/tools/video-editor/hooks/useMarqueeSelect.ts",
    "src/tools/video-editor/hooks/useSelectedMediaClips.ts",
    "src/tools/video-editor/hooks/useTimelineCommit.ts",
    "src/tools/video-editor/hooks/useTimelineState.ts",
    ".megaplan/plans/selection-coordination-20260426-1613/execution_batch_3.json",
    "src/app/providers/AppProviders.test.tsx",
    "src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.test.tsx",
    "src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.ts",
    "src/shared/contexts/AgentChatContext.tsx",
    "src/shared/hooks/__tests__/useLastAffectedShot.test.ts",
    "src/tools/video-editor/components/AgentChat/AgentChat.test.tsx",
    "src/tools/video-editor/hooks/clip-editing/types.ts",
    "src/tools/video-editor/hooks/useAssetManagement.ts",
    "src/tools/video-editor/hooks/useClipEditing.ts",
    "src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts",
    "src/tools/video-editor/hooks/useTimelineState.types.ts",
    "src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx",
    ".megaplan/plans/selection-coordination-20260426-1613/execution_batch_4.json",
    "src/shared/state/currentAttachmentSet.test.tsx",
    "src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx",
    ".megaplan/plans/selection-coordination-20260426-1613/execution_batch_6.json",
    "src/shared/components/MediaGalleryItem/components/ImageContent.tsx",
    "src/shared/components/MediaGalleryItem/components/VideoContent.tsx"
  ]
}

        Execution audit (`execution_audit.json`):
            {
  "findings": [
    "Git status shows changed files not claimed by any task: .claude/, .megaplan/bakeoffs/, .megaplan/debt.json, .megaplan/schemas/execution.json, .megaplan/schemas/finalize.json, .megaplan/schemas/prep.json, .megaplan/schemas/revise.json, src/app/App.tsx, src/domains/media-lightbox/components/LightboxShell.tsx, src/features/tasks/components/TasksPane/TasksPane.tsx, src/integrations/supabase/bootstrap/fetchWithTimeout.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryItemProps.ts, src/shared/components/MediaGallery/hooks/useMediaGalleryViewInteractions.ts, src/shared/components/MediaGallery/types.ts, src/shared/components/MediaGalleryItem/types.ts, src/shared/components/MediaVariantPicker.tsx, src/shared/components/PaneControlTab.tsx, src/shared/components/ui/overlay/shared.tsx, src/shared/components/ui/runtime/sonner.tsx, src/shared/contexts/AgentChatContext.test.tsx, src/shared/hooks/projects/useProjectGenerations.ts, src/shared/lib/uiLayers.test.ts, src/shared/lib/uiLayers.ts, src/shared/state/panesStore.test.ts, src/shared/state/panesStore.ts, src/tools/video-editor/components/AgentChat/index.ts, src/tools/video-editor/components/PropertiesPanel/ClipPanel.tsx, src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx, src/tools/video-editor/components/TimelineEditor/ClipAction.tsx, src/tools/video-editor/hooks/useAddVariantAsGeneration.ts, src/tools/video-editor/hooks/usePollSync.ts, src/tools/video-editor/hooks/useStaleVariants.ts"
  ],
  "files_in_diff": [
    ".claude/",
    ".megaplan/bakeoffs/",
    ".megaplan/debt.json",
    ".megaplan/schemas/execution.json",
    ".megaplan/schemas/finalize.json",
    ".megaplan/schemas/prep.json",
    ".megaplan/schemas/revise.json",
    "src/app/App.tsx",
    "src/app/providers/AppProviders.test.tsx",
    "src/app/providers/AppProviders.tsx",
    "src/domains/media-lightbox/components/LightboxShell.tsx",
    "src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
    "src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx",
    "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx",
    "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts",
    "src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.test.tsx",
    "src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.ts",
    "src/features/tasks/components/TasksPane/TasksPane.tsx",
    "src/integrations/supabase/bootstrap/fetchWithTimeout.ts",
    "src/shared/components/MediaGallery/hooks/useMediaGalleryItemProps.ts",
    "src/shared/components/MediaGallery/hooks/useMediaGalleryViewInteractions.ts",
    "src/shared/components/MediaGallery/types.ts",
    "src/shared/components/MediaGalleryItem.tsx",
    "src/shared/components/MediaGalleryItem/components/ImageContent.tsx",
    "src/shared/components/MediaGalleryItem/components/VideoContent.tsx",
    "src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts",
    "src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts",
    "src/shared/components/MediaGalleryItem/types.ts",
    "src/shared/components/MediaVariantPicker.tsx",
    "src/shared/components/PaneControlTab.tsx",
    "src/shared/components/ui/overlay/shared.tsx",
    "src/shared/components/ui/runtime/sonner.tsx",
    "src/shared/contexts/AgentChatContext.test.tsx",
    "src/shared/contexts/AgentChatContext.tsx",
    "src/shared/hooks/__tests__/useLastAffectedShot.test.ts",
    "src/shared/hooks/gallery/useGallerySelectionBridge.ts",
    "src/shared/hooks/projects/useProjectGenerations.ts",
    "src/shared/lib/interactions/selectionGesture.test.ts",
    "src/shared/lib/interactions/selectionGesture.ts",
    "src/shared/lib/uiLayers.test.ts",
    "src/shared/lib/uiLayers.ts",
    "src/shared/state/currentAttachmentSet.test.ts",
    "src/shared/state/currentAttachmentSet.test.tsx",
    "src/shared/state/currentAttachmentSet.ts",
    "src/shared/state/panesStore.test.ts",
    "src/shared/state/panesStore.ts",
    "src/shared/state/selectionActions.test.ts",
    "src/shared/state/selectionStore.ts",
    "src/tools/image-generation/pages/ImageGenerationToolPage.tsx",
    "src/tools/video-editor/components/AgentChat/AgentChat.test.tsx",
    "src/tools/video-editor/components/AgentChat/AgentChat.tsx",
    "src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx",
    "src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx",
    "src/tools/video-editor/components/AgentChat/index.ts",
    "src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx",
    "src/tools/video-editor/components/PropertiesPanel/ClipPanel.tsx",
    "src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx",
    "src/tools/video-editor/components/TimelineEditor/ClipAction.tsx",
    "src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx",
    "src/tools/video-editor/components/VideoEditorShell.tsx",
    "src/tools/video-editor/contexts/VideoEditorProvider.test.tsx",
    "src/tools/video-editor/contexts/VideoEditorProvider.tsx",
    "src/tools/video-editor/hooks/clip-editing/types.ts",
    "src/tools/video-editor/hooks/useAddVariantAsGeneration.ts",
    "src/tools/video-editor/hooks/useAssetManagement.ts",
    "src/tools/video-editor/hooks/useClipDrag.helpers.ts",
    "src/tools/video-editor/hooks/useClipDrag.test.tsx",
    "src/tools/video-editor/hooks/useClipDrag.ts",
    "src/tools/video-editor/hooks/useClipEditing.ts",
    "src/tools/video-editor/hooks/useMarqueeSelect.ts",
    "src/tools/video-editor/hooks/usePollSync.ts",
    "src/tools/video-editor/hooks/useSelectedMediaClips.ts",
    "src/tools/video-editor/hooks/useStaleVariants.ts",
    "src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts",
    "src/tools/video-editor/hooks/useTimelineCommit.ts",
    "src/tools/video-editor/hooks/useTimelineState.ts",
    "src/tools/video-editor/hooks/useTimelineState.types.ts"
  ],
  "files_claimed": [
    "src/app/providers/AppProviders.test.tsx",
    "src/app/providers/AppProviders.tsx",
    "src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx",
    "src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx",
    "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx",
    "src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts",
    "src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.test.tsx",
    "src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.ts",
    "src/shared/components/MediaGalleryItem.tsx",
    "src/shared/components/MediaGalleryItem/components/ImageContent.tsx",
    "src/shared/components/MediaGalleryItem/components/VideoContent.tsx",
    "src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts",
    "src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts",
    "src/shared/contexts/AgentChatContext.tsx",
    "src/shared/hooks/__tests__/useLastAffectedShot.test.ts",
    "src/shared/hooks/gallery/useGallerySelectionBridge.ts",
    "src/shared/lib/interactions/selectionGesture.test.ts",
    "src/shared/lib/interactions/selectionGesture.ts",
    "src/shared/state/currentAttachmentSet.test.ts",
    "src/shared/state/currentAttachmentSet.test.tsx",
    "src/shared/state/currentAttachmentSet.ts",
    "src/shared/state/selectionActions.test.ts",
    "src/shared/state/selectionStore.ts",
    "src/tools/image-generation/pages/ImageGenerationToolPage.tsx",
    "src/tools/video-editor/components/AgentChat/AgentChat.test.tsx",
    "src/tools/video-editor/components/AgentChat/AgentChat.tsx",
    "src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx",
    "src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx",
    "src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx",
    "src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx",
    "src/tools/video-editor/components/VideoEditorShell.tsx",
    "src/tools/video-editor/contexts/VideoEditorProvider.test.tsx",
    "src/tools/video-editor/contexts/VideoEditorProvider.tsx",
    "src/tools/video-editor/hooks/clip-editing/types.ts",
    "src/tools/video-editor/hooks/useAssetManagement.ts",
    "src/tools/video-editor/hooks/useClipDrag.helpers.ts",
    "src/tools/video-editor/hooks/useClipDrag.test.tsx",
    "src/tools/video-editor/hooks/useClipDrag.ts",
    "src/tools/video-editor/hooks/useClipEditing.ts",
    "src/tools/video-editor/hooks/useMarqueeSelect.ts",
    "src/tools/video-editor/hooks/useSelectedMediaClips.ts",
    "src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts",
    "src/tools/video-editor/hooks/useTimelineCommit.ts",
    "src/tools/video-editor/hooks/useTimelineState.ts",
    "src/tools/video-editor/hooks/useTimelineState.types.ts"
  ],
  "skipped": false,
  "reason": ""
}

        Git diff summary:
        M .megaplan/debt.json
 M .megaplan/schemas/execution.json
 M .megaplan/schemas/finalize.json
 M .megaplan/schemas/prep.json
 M .megaplan/schemas/revise.json
 M src/app/App.tsx
 M src/app/providers/AppProviders.test.tsx
 M src/app/providers/AppProviders.tsx
 M src/domains/media-lightbox/components/LightboxShell.tsx
 M src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx
 M src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx
 M src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.test.tsx
 M src/features/gallery/components/GenerationsPane/hooks/useLassoSelection.ts
 D src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.test.tsx
 D src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.ts
 M src/features/tasks/components/TasksPane/TasksPane.tsx
 M src/integrations/supabase/bootstrap/fetchWithTimeout.ts
 M src/shared/components/MediaGallery/hooks/useMediaGalleryItemProps.ts
 M src/shared/components/MediaGallery/hooks/useMediaGalleryViewInteractions.ts
 M src/shared/components/MediaGallery/types.ts
 M src/shared/components/MediaGalleryItem.tsx
 M src/shared/components/MediaGalleryItem/components/ImageContent.tsx
 M src/shared/components/MediaGalleryItem/components/VideoContent.tsx
 M src/shared/components/MediaGalleryItem/hooks/useItemInteraction.test.ts
 M src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts
 M src/shared/components/MediaGalleryItem/types.ts
 M src/shared/components/PaneControlTab.tsx
 M src/shared/components/ui/overlay/shared.tsx
 M src/shared/components/ui/runtime/sonner.tsx
 M src/shared/contexts/AgentChatContext.tsx
 M src/shared/hooks/__tests__/useLastAffectedShot.test.ts
 M src/shared/hooks/gallery/useGallerySelectionBridge.ts
 M src/shared/hooks/projects/useProjectGenerations.ts
 M src/shared/lib/uiLayers.test.ts
 M src/shared/lib/uiLayers.ts
 M src/shared/state/panesStore.ts
 M src/shared/state/selectionStore.ts
 M src/tools/image-generation/pages/ImageGenerationToolPage.tsx
 M src/tools/video-editor/components/AgentChat/AgentChat.test.tsx
 M src/tools/video-editor/components/AgentChat/AgentChat.tsx
 M src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx
 M src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx
 M src/tools/video-editor/components/AgentChat/index.ts
 M src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx
 M src/tools/video-editor/components/PropertiesPanel/ClipPanel.tsx
 M src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx
 M src/tools/video-editor/components/TimelineEditor/ClipAction.tsx
 M src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx
 M src/tools/video-editor/components/VideoEditorShell.tsx
 M src/tools/video-editor/contexts/VideoEditorProvider.test.tsx
 M src/tools/video-editor/contexts/VideoEditorProvider.tsx
 M src/tools/video-editor/hooks/clip-editing/types.ts
 M src/tools/video-editor/hooks/useAssetManagement.ts
 M src/tools/video-editor/hooks/useClipDrag.helpers.ts
 M src/tools/video-editor/hooks/useClipDrag.test.tsx
 M src/tools/video-editor/hooks/useClipDrag.ts
 M src/tools/video-editor/hooks/useClipEditing.ts
 M src/tools/video-editor/hooks/useMarqueeSelect.ts
 M src/tools/video-editor/hooks/usePollSync.ts
 M src/tools/video-editor/hooks/useSelectedMediaClips.ts
 M src/tools/video-editor/hooks/useStaleVariants.ts
 M src/tools/video-editor/hooks/useTimelineCommit.ts
 M src/tools/video-editor/hooks/useTimelineState.ts
 M src/tools/video-editor/hooks/useTimelineState.types.ts
?? .claude/
?? .megaplan/bakeoffs/
?? src/shared/components/MediaVariantPicker.tsx
?? src/shared/contexts/AgentChatContext.test.tsx
?? src/shared/lib/interactions/selectionGesture.test.ts
?? src/shared/lib/interactions/selectionGesture.ts
?? src/shared/state/currentAttachmentSet.test.ts
?? src/shared/state/currentAttachmentSet.test.tsx
?? src/shared/state/currentAttachmentSet.ts
?? src/shared/state/panesStore.test.ts
?? src/shared/state/selectionActions.test.ts
?? src/tools/video-editor/hooks/useAddVariantAsGeneration.ts
?? src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts

        Requirements:
        - Verify each success criterion explicitly.
        - Trust executor evidence by default. Dig deeper only where the git diff, `execution_audit.json`, or vague notes make the claim ambiguous.
        - Each criterion has a `priority` (`must`, `should`, or `info`). Apply these rules:
          - `must` criteria are hard gates. A `must` criterion that fails means `needs_rework`.
          - `should` criteria are quality targets. If the spirit is met but the letter is not, mark `pass` with evidence explaining the gap. Only mark `fail` if the intent was clearly missed. A `should` failure alone does NOT require `needs_rework`.
          - `info` criteria are for human reference. Mark them `waived` with a note — do not evaluate them.
          - If a criterion has `requires` capabilities that are not satisfiable by container workers (e.g., `drive_browser`, `subjective_judgment`), mark it `deferred_human` — NOT `fail` or `waived`. Deferred-human criteria do NOT count toward `needs_rework`.
          - If a criterion (any priority) cannot be verified in this context (e.g., requires manual testing or runtime observation), mark it `waived` with an explanation.
        - Set `review_verdict` to `needs_rework` only when at least one `must` criterion fails or actual implementation work is incomplete. Use `approved` when all `must` criteria pass, even if some `should` criteria are flagged.

        - baseline_test_failures in finalize.json lists tests that were already failing before execution. Do not flag these as rework items unless the executor introduced new failures in those same tests.
        - Cross-reference each task's `files_changed` and `commands_run` against the git diff and any audit findings.
        - Review every `sense_check` explicitly and treat perfunctory acknowledgments as a reason to dig deeper.
        - Follow this JSON shape exactly:
        ```json
        {
          "review_verdict": "approved",
          "criteria": [
            {
              "name": "All existing tests pass",
              "priority": "must",
              "pass": "pass",
              "evidence": "Test suite ran green — 42 passed, 0 failed."
            },
            {
              "name": "File under ~300 lines",
              "priority": "should",
              "pass": "pass",
              "evidence": "File is 375 lines — above the target but reasonable given the component's responsibilities. Spirit met."
            },
            {
              "name": "Manual smoke tests pass",
              "priority": "info",
              "pass": "waived",
              "evidence": "Cannot be verified in automated review. Noted for manual QA."
            }
          ],
          "issues": [],
          "rework_items": [],
          "summary": "Approved. All must criteria pass. The should criterion on line count is close enough given the component scope.",
          "task_verdicts": [
            {
              "task_id": "T6",
              "reviewer_verdict": "Pass. Claimed handler changes and command evidence match the repo state.",
              "evidence_files": ["megaplan/handlers.py", "megaplan/evaluation.py"]
            }
          ],
          "sense_check_verdicts": [
            {
              "sense_check_id": "SC6",
              "verdict": "Confirmed. The execute blocker only fires when both evidence arrays are empty."
            }
          ]
        }
        ```
        - `rework_items` must be an array of structured rework directives. When `review_verdict` is `needs_rework`, populate one entry per issue with:
          - `task_id`: which finalize task this issue relates to
          - `issue`: what is wrong
          - `expected`: what correct behavior looks like
          - `actual`: what was observed
          - `evidence_file` (optional): file path supporting the finding
          - `flag_id`: critique/review flag ID when applicable, otherwise `null`
          - `source`: short machine-readable source tag when applicable, otherwise `null`
        - `issues` must still be populated as a flat one-line-per-item summary derived from `rework_items` (for backward compatibility). When approved, both `issues` and `rework_items` should be empty arrays.
        - When the work needs another execute pass, keep the same shape and change only `review_verdict` to `needs_rework`; make `issues`, `rework_items`, `summary`, and task verdicts specific enough for the executor to act on directly.

> AGENT

{"review_verdict":"needs_rework","checks":[],"pre_check_flags":[{"id":"PRECHECK-DIFF_SIZE_SANITY","check":"diff_size_sanity","detail":"Diff size looks larger than expected: changed_lines=4564, expected≈20, ratio=228.20, files=71, hunks=242.","severity":"significant","evidence_file":"src/app/App.tsx"}],"verified_flag_ids":[],"disputed_flag_ids":[],"criteria":[],"issues":["Review is in progress; this placeholder will be replaced after inspecting the final diff."],"rework_items":[{"task_id":"REVIEW","issue":"Review still running.","expected":"Final review after verifying diff.","actual":"Initial progress update only.","evidence_file":"","flag_id":null,"source":"progress_update"}],"summary":"I’m going to verify the final diff directly, focusing on the previously open flags first: raw store export, merge/dedupe semantics, dev guard, bridge fields, and test evidence.","task_verdicts":[],"sense_check_verdicts":[]}

> AGENT

{"review_verdict":"needs_rework","checks":[],"pre_check_flags":[{"id":"PRECHECK-DIFF_SIZE_SANITY","check":"diff_size_sanity","detail":"Diff size looks larger than expected: changed_lines=4564, expected≈20, ratio=228.20, files=71, hunks=242.","severity":"significant","evidence_file":"src/app/App.tsx"}],"verified_flag_ids":["FLAG-017","FLAG-021","correctness-1","correctness"],"disputed_flag_ids":[],"criteria":[],"issues":["Review is still in progress; verifying currentAttachmentSet merge policy and the raw store export concern next."],"rework_items":[{"task_id":"REVIEW","issue":"Review still running.","expected":"Final review after verifying diff.","actual":"Partial confirmation: placeholder warning uses import.meta.env.DEV and currentAttachmentSet imports exported useSelectionStore; need to finish flag re-verification.","evidence_file":"src/shared/state/currentAttachmentSet.ts","flag_id":null,"source":"progress_update"}],"summary":"I confirmed two previously risky areas directly in the diff: placeholder warnings use `import.meta.env.DEV`, and `useSelectionStore` is exported/imported so the separate composer module compiles. I’m checking whether the raw export leaks low-level reducers in practice and whether URL dedupe is actually preserved.","task_verdicts":[],"sense_check_verdicts":[]}

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"export function useSelectionStore|function useSelectionStore|mergeSelectedClips|import\\.meta\\.env\\.DEV|process\\.env\\.NODE_ENV|useSelectionStoreApi|clearGallery|timelineClips|replaceSelectedTimelineClips\" src/shared/state/selectionStore.ts src/shared/state/currentAttachmentSet.ts src/shared/contexts/AgentChatContext.tsx src/tools/video-editor/components/AgentChat/AgentChat.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx src/tools/video-editor/contexts/VideoEditorProvider.tsx src/app/providers/AppProviders.test.tsx",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "git diff -- src/shared/state/currentAttachmentSet.ts src/shared/state/selectionStore.ts src/shared/contexts/AgentChatContext.tsx src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx src/tools/video-editor/contexts/VideoEditorProvider.tsx",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 50000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "wc -l src/shared/state/currentAttachmentSet.ts src/shared/lib/interactions/selectionGesture.ts src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts src/shared/state/selectionStore.ts && rg -n \"useModifierKeys|useSelectionStoreApi\" src/ || true",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

{"review_verdict":"needs_rework","checks":[],"pre_check_flags":[{"id":"PRECHECK-DIFF_SIZE_SANITY","check":"diff_size_sanity","detail":"Diff size looks larger than expected: changed_lines=4564, expected≈20, ratio=228.20, files=71, hunks=242.","severity":"significant","evidence_file":"src/app/App.tsx"}],"verified_flag_ids":["FLAG-017","FLAG-019","FLAG-021","correctness-1","correctness","scope","issue_hints","callers"],"disputed_flag_ids":[],"criteria":[],"issues":["Review is still in progress; likely rework found for FLAG-020 because `useSelectionStore` is exported while the store state still contains low-level reducers."],"rework_items":[{"task_id":"REVIEW","issue":"The raw Zustand selector hook is exported while `SelectionStoreState` still includes low-level reducer functions, so outside modules can select `state.selectTimelineClip`, `state.selectGalleryItem`, etc.","expected":"Keep low-level reducers unreachable from outside `selectionStore.ts`, either by colocating `useCurrentAttachmentSet` in `selectionStore.ts` and making `useSelectionStore` private again, or by exporting a narrow read-only selector surface that excludes mutation reducers.","actual":"`export function useSelectionStore<T>(selector: (state: SelectionStoreState) => T...)` is exported, and `SelectionStoreState` still contains low-level reducers such as `selectTimelineClip`, `selectGalleryItem`, and `clearGallerySelection`.","evidence_file":"src/shared/state/selectionStore.ts","flag_id":"FLAG-020","source":"review_flag_reverify"}],"summary":"I found one real architecture miss so far: the raw store hook export leaks the low-level reducer surface. The merge-key issue appears fixed using `isPlaceholder ? clipId : url`, and the Vite dev guard is fixed with `import.meta.env.DEV`. I’m finishing the remaining criteria/sense-check pass before producing the final JSON.","task_verdicts":[],"sense_check_verdicts":[]}

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,140p' src/shared/state/currentAttachmentSet.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,260p' src/shared/state/currentAttachmentSet.test.ts && sed -n '1,260p' src/shared/state/currentAttachmentSet.test.tsx",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 50000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"useSelectionStore\\(|selectTimelineClip|selectGalleryItem|clearGallerySelection|clearTimelineSelection|deselectGalleryItems|addTimelineClips|pruneTimelineSelection|resetTimelineSelection\" src -g '*.ts' -g '*.tsx'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

{
  "review_verdict": "needs_rework",
  "checks": [],
  "pre_check_flags": [
    {
      "id": "PRECHECK-DIFF_SIZE_SANITY",
      "check": "diff_size_sanity",
      "detail": "Diff size looks larger than expected: changed_lines=4564, expected≈20, ratio=228.20, files=71, hunks=242.",
      "severity": "significant",
      "evidence_file": "src/app/App.tsx"
    }
  ],
  "verified_flag_ids": [
    "FLAG-001",
    "FLAG-002",
    "FLAG-003",
    "FLAG-004",
    "FLAG-005",
    "issue_hints-1",
    "issue_hints-2",
    "correctness-1",
    "correctness-3",
    "scope",
    "all_locations-1",
    "all_locations-2",
    "callers-1",
    "callers-2",
    "FLAG-006",
    "FLAG-007",
    "FLAG-008",
    "FLAG-009",
    "FLAG-010",
    "issue_hints",
    "correctness",
    "all_locations",
    "callers",
    "FLAG-011",
    "FLAG-012",
    "FLAG-013",
    "FLAG-014",
    "FLAG-015",
    "FLAG-016",
    "FLAG-017",
    "FLAG-018",
    "FLAG-019",
    "FLAG-021"
  ],
  "disputed_flag_ids": [
    "verifiability-0",
    "verifiability-1",
    "verifiability-2"
  ],
  "criteria": [
    {
      "name": "TypeScript clean",
      "priority": "must",
      "pass": "pass",
      "evidence": "Executor ran `npx tsc --noEmit` clean in final validation."
    },
    {
      "name": "Vitest baseline only",
      "priority": "must",
      "pass": "pass",
      "evidence": "Executor reports full `npx vitest run` had exactly the 3 documented pre-existing failures."
    },
    {
      "name": "ESLint touched files",
      "priority": "must",
      "pass": "pass",
      "evidence": "Scoped eslint passed on selection/coordination touched files; unrelated dirty WIP lint was not counted."
    },
    {
      "name": "Intent exports present",
      "priority": "must",
      "pass": "pass",
      "evidence": "selectionStore exports intent commands, clip data mutators, test snapshot helper, and useSelectionStore."
    },
    {
      "name": "currentAttachmentSet compiles import",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet imports `useSelectionStore`; tsc passed."
    },
    {
      "name": "Gallery intents preserve timeline",
      "priority": "must",
      "pass": "pass",
      "evidence": "selectionActions.test.ts lines 39-66 assert gallery item/marquee preserve selected timeline ids."
    },
    {
      "name": "Timeline marquee additive appends",
      "priority": "must",
      "pass": "pass",
      "evidence": "selectionActions.test.ts lines 81-91 assert additive marquee clears gallery and does not toggle off existing clips."
    },
    {
      "name": "Timeline single additive toggles",
      "priority": "must",
      "pass": "pass",
      "evidence": "selectionActions.test.ts lines 68-79 assert add then remove behavior."
    },
    {
      "name": "preserveIfSelected no-op",
      "priority": "must",
      "pass": "pass",
      "evidence": "selectionActions.test.ts lines 93-100 assert timeline and gallery are preserved."
    },
    {
      "name": "Editor/system contracts",
      "priority": "must",
      "pass": "pass",
      "evidence": "selectionActions.test.ts lines 102-178 cover editor preservation and system reset/sync/clear behavior."
    },
    {
      "name": "composerRemoveAttachment matcher",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.test.ts covers generation/url/media type, sibling preservation, URL fallback, and clipId disambiguation."
    },
    {
      "name": "Merge key placeholder safe",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.ts lines 17-21 keys placeholders by clipId and real clips by url."
    },
    {
      "name": "Placeholder emitted for missing clip data",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.ts lines 70-78 emits makePlaceholderClip when clipDataById has no selected clip data."
    },
    {
      "name": "Two unknown clips stay distinct",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.test.ts and currentAttachmentSet.test.tsx assert two selected unknown clipIds produce two placeholders."
    },
    {
      "name": "Dev placeholder warning",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.ts lines 81-83 uses `import.meta.env.DEV`; tests spy on console.warn."
    },
    {
      "name": "Partial resolution preserves count",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.test.ts and .test.tsx cover partial setTimelineClipData preserving two chips."
    },
    {
      "name": "URL fallback dedupe",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.ts line 20 uses URL for non-placeholder clips; test asserts real gallery+timeline same URL dedupe even when gallery has clipId."
    },
    {
      "name": "State-only convenience hooks",
      "priority": "must",
      "pass": "pass",
      "evidence": "useGallerySelection and useTimelineSelectionStore return state-only slices at selectionStore.ts lines 1055-1093."
    },
    {
      "name": "useSelectionStoreApi deleted",
      "priority": "must",
      "pass": "pass",
      "evidence": "`rg useSelectionStoreApi src/` returned no hits."
    },
    {
      "name": "useTimelineMultiSelect trimmed",
      "priority": "must",
      "pass": "pass",
      "evidence": "UseTimelineMultiSelectResult has no select/clear mutation methods and no clearGallery option."
    },
    {
      "name": "Removed reducer external references",
      "priority": "must",
      "pass": "fail",
      "evidence": "No external direct references remain, but exported `useSelectionStore` allows any external module to select low-level reducers still present in SelectionStoreState."
    },
    {
      "name": "clearGallery hidden outside store",
      "priority": "must",
      "pass": "pass",
      "evidence": "`rg clearGallery src/` only reports internal selectionStore low-level reducer definitions/comments."
    },
    {
      "name": "useTimelineCommit intents",
      "priority": "must",
      "pass": "pass",
      "evidence": "useTimelineCommit imports editorSelectTimelineClip/editorClearTimelineSelection/editorSetSelectedTrackId."
    },
    {
      "name": "useTimelineState lifecycle",
      "priority": "must",
      "pass": "pass",
      "evidence": "useTimelineState calls systemResetTimelineSelection on timeline-id change."
    },
    {
      "name": "useClipDrag direct calls migrated",
      "priority": "must",
      "pass": "pass",
      "evidence": "useClipDrag lines 450, 460, 462, 464 call userSelectTimelineClip with additive/preserveIfSelected options."
    },
    {
      "name": "AppProviders project reset",
      "priority": "must",
      "pass": "pass",
      "evidence": "AppProviders imports and calls systemResetSelectionForProjectChange."
    },
    {
      "name": "useLastAffectedShot test migrated",
      "priority": "must",
      "pass": "pass",
      "evidence": "Executor migrated it to systemSetLastAffectedShotId plus __getSelectionStateForTests and targeted test passed."
    },
    {
      "name": "Gallery selection bridge intents",
      "priority": "must",
      "pass": "pass",
      "evidence": "useGallerySelectionBridge imports systemSyncGallerySelection/systemClearGallerySelection."
    },
    {
      "name": "currentAttachmentSet module",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.ts exports useCurrentAttachmentSet and mergeSelectedClips; AgentChat imports useCurrentAttachmentSet."
    },
    {
      "name": "clipDataById all attachments",
      "priority": "must",
      "pass": "pass",
      "evidence": "useTimelineClipsForAttachments iterates resolvedConfig.clips and VideoEditorProvider writes allClips to setTimelineClipData."
    },
    {
      "name": "Placeholder chip rendering",
      "priority": "must",
      "pass": "pass",
      "evidence": "AgentChatMessage.tsx renders Loading placeholder without img/video and hides remove; AgentChatMessage.test.tsx covers it."
    },
    {
      "name": "displayedClips removed",
      "priority": "must",
      "pass": "pass",
      "evidence": "rg found no displayedClips in AgentChat."
    },
    {
      "name": "AgentChatContext bridge slimmed",
      "priority": "must",
      "pass": "pass",
      "evidence": "AgentChatContextValue only has timelineId; no timelineClips/replaceSelectedTimelineClips fields."
    },
    {
      "name": "Flicker test 1",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.test.tsx includes steady-state non-empty render test."
    },
    {
      "name": "Flicker test 2",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.test.tsx includes additive marquee same-render real clips and gallery clearing."
    },
    {
      "name": "Flicker test 3",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.test.tsx includes single placeholder gap fill and convergence."
    },
    {
      "name": "Flicker test 4",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.test.tsx includes additive-toggle render flow."
    },
    {
      "name": "Flicker test 5",
      "priority": "must",
      "pass": "pass",
      "evidence": "currentAttachmentSet.test.tsx includes multi-placeholder merge-key test through partial/full resolution."
    },
    {
      "name": "AgentChatMessage tests",
      "priority": "must",
      "pass": "pass",
      "evidence": "AgentChatMessage.test.tsx lines 163-219 assert placeholder loading/no media/no X and real chip media/X."
    },
    {
      "name": "useModifierKeys deleted",
      "priority": "must",
      "pass": "pass",
      "evidence": "Files are deleted and `rg useModifierKeys src/` returned no hits."
    },
    {
      "name": "selectionGesture usage",
      "priority": "must",
      "pass": "pass",
      "evidence": "MediaGalleryItem/useItemInteraction/useLassoSelection use selectionGesture directly; gallery pages consume event-derived modifiers from that shared path."
    },
    {
      "name": "Tests updated",
      "priority": "must",
      "pass": "pass",
      "evidence": "AgentChat, VideoEditorProvider, AppProviders, GenerationsPaneGallery, and AgentChatMessage tests were updated and targeted runs passed."
    },
    {
      "name": "Point fixes retained",
      "priority": "must",
      "pass": "pass",
      "evidence": "Executor verified wrapper pointer handling, onImageClick modifiers, fetchWithTimeout logger, and AgentChat Clear button remain."
    },
    {
      "name": "No commits created",
      "priority": "must",
      "pass": "pass",
      "evidence": "Executor reports HEAD remains 95d94b780 and git status is dirty."
    },
    {
      "name": "New file size targets",
      "priority": "should",
      "pass": "pass",
      "evidence": "currentAttachmentSet.ts 90 LOC, selectionGesture.ts 19 LOC, useTimelineClipsForAttachments.ts 72 LOC; selectionStore.ts is 1145 LOC, slightly over target but close and understandable for colocation."
    },
    {
      "name": "Manual smoke core UX",
      "priority": "info",
      "pass": "waived",
      "evidence": "Requires runtime UI/manual verification."
    },
    {
      "name": "Manual smoke no flicker",
      "priority": "info",
      "pass": "waived",
      "evidence": "Requires runtime UI/manual verification; automated render-flow tests cover the invariant."
    },
    {
      "name": "Manual smoke chip-specific removal",
      "priority": "info",
      "pass": "waived",
      "evidence": "Requires runtime UI/manual verification; unit tests cover matcher semantics."
    }
  ],
  "issues": [
    "FLAG-020/correctness-2: `useSelectionStore` is exported while `SelectionStoreState` still exposes low-level reducers, so the intent facade is not actually the only reachable selection mutation API."
  ],
  "rework_items": [
    {
      "task_id": "REVIEW",
      "issue": "The raw Zustand selector hook is exported while `SelectionStoreState` still includes low-level reducer functions, so outside modules can select `state.selectTimelineClip`, `state.selectGalleryItem`, `state.clearGallerySelection`, etc.",
      "expected": "Keep low-level reducers unreachable from outside `selectionStore.ts`, either by colocating `useCurrentAttachmentSet` in `selectionStore.ts` and making `useSelectionStore` private again, or by exporting a narrow read-only selector surface that excludes low-level mutation reducers.",
      "actual": "`export function useSelectionStore<T>(selector: (state: SelectionStoreState) => T...)` is exported at selectionStore.ts:742, and `SelectionStoreState` still contains low-level reducers at lines 68-130.",
      "evidence_file": "src/shared/state/selectionStore.ts",
      "flag_id": "FLAG-020",
      "source": "review_flag_reverify"
    },
    {
      "task_id": "REVIEW",
      "issue": "The implementation reopens the public low-level mutation surface through the exported raw store hook, contradicting the intent-facade requirement.",
      "expected": "The intent commands should be the only public mutation surface; raw low-level reducers should be private/internal and unreachable to components.",
      "actual": "External callers can import `useSelectionStore` and select low-level reducer functions from the inferred `SelectionStoreState` callback parameter.",
      "evidence_file": "src/shared/state/selectionStore.ts",
      "flag_id": "correctness-2",
      "source": "review_flag_reverify"
    }
  ],
  "summary": "Needs rework. The functional selection, attachment composer, placeholder, gesture, and test changes largely match the criteria, and the previously risky merge-key and Vite env-guard issues are fixed. One hard architecture gate remains: exporting the raw `useSelectionStore` hook leaks the low-level reducer API that this refactor was supposed to make private.",
  "task_verdicts": [
    {
      "task_id": "T1",
      "reviewer_verdict": "Needs rework. Intent commands exist, but exporting raw useSelectionStore leaks low-level reducers.",
      "evidence_files": [
        "src/shared/state/selectionStore.ts"
      ]
    },
    {
      "task_id": "T6",
      "reviewer_verdict": "Pass. Composer merge policy uses placeholder-specific clipId key and URL dedupe for real clips; dev guard uses import.meta.env.DEV.",
      "evidence_files": [
        "src/shared/state/currentAttachmentSet.ts",
        "src/shared/state/currentAttachmentSet.test.ts"
      ]
    },
    {
      "task_id": "T7",
      "reviewer_verdict": "Pass. Bridge no longer exposes timelineClips/replaceSelectedTimelineClips and writes all timeline attachment metadata to the selection store.",
      "evidence_files": [
        "src/shared/contexts/AgentChatContext.tsx",
        "src/tools/video-editor/contexts/VideoEditorProvider.tsx",
        "src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts"
      ]
    },
    {
      "task_id": "T8",
      "reviewer_verdict": "Pass. Placeholder chip rendering avoids media src binding and hides remove controls.",
      "evidence_files": [
        "src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx"
      ]
    },
    {
      "task_id": "T14",
      "reviewer_verdict": "Pass with caveat. Validation evidence is acceptable; manual smoke criteria remain waived.",
      "evidence_files": [
        "src/shared/state/currentAttachmentSet.test.tsx",
        "src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx"
      ]
    }
  ],
  "sense_check_verdicts": [
    {
      "sense_check_id": "SC1",
      "verdict": "Partially confirmed. Exports exist, but the raw useSelectionStore export violates the intended private low-level reducer surface."
    },
    {
      "sense_check_id": "SC2",
      "verdict": "Confirmed. Listed timeline/editor/system callers use intent commands."
    },
    {
      "sense_check_id": "SC3",
      "verdict": "Confirmed. Gallery paths use intent commands and event-derived modifiers."
    },
    {
      "sense_check_id": "SC4",
      "verdict": "Partially confirmed. Public convenience hooks were trimmed and useSelectionStoreApi deleted, but raw useSelectionStore still exposes low-level reducers."
    },
    {
      "sense_check_id": "SC5",
      "verdict": "Confirmed. selectionActions.test.ts covers the core intent contracts."
    },
    {
      "sense_check_id": "SC6",
      "verdict": "Confirmed. Merge key is placeholder-specific, env guard is import.meta.env.DEV, and matcher tests exist."
    },
    {
      "sense_check_id": "SC7",
      "verdict": "Confirmed. useTimelineClipsForAttachments returns all resolved attachment clips and Provider syncs clipDataById."
    },
    {
      "sense_check_id": "SC8",
      "verdict": "Confirmed. AgentChat local merge/grace window are gone and placeholder chip rendering is correct."
    },
    {
      "sense_check_id": "SC9",
      "verdict": "Confirmed. currentAttachmentSet.test.tsx includes the five requested render-flow tests."
    },
    {
      "sense_check_id": "SC10",
      "verdict": "Confirmed. selectionGesture exports the three small stateless functions."
    },
    {
      "sense_check_id": "SC11",
      "verdict": "Confirmed in spirit. The shared gesture path derives modifiers; ImageGenerationToolPage consumes the modifier argument instead of importing the helper directly."
    },
    {
      "sense_check_id": "SC12",
      "verdict": "Confirmed. useModifierKeys files are deleted and no imports remain."
    },
    {
      "sense_check_id": "SC13",
      "verdict": "Confirmed. Tests were updated, including AgentChatMessage placeholder coverage and VideoEditorProvider store assertions."
    },
    {
      "sense_check_id": "SC14",
      "verdict": "Confirmed from executor evidence. tsc and scoped eslint are clean; full vitest has only the documented three failures; no commit was created."
    }
  ]
}

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba src/shared/state/selectionStore.ts | sed -n '55,130p;730,755p;1048,1135p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba src/shared/state/currentAttachmentSet.ts | sed -n '1,110p' && nl -ba src/tools/video-editor/components/AgentChat/AgentChatMessage.tsx | sed -n '168,238p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba src/shared/state/selectionActions.test.ts | sed -n '1,260p' && nl -ba src/shared/lib/interactions/selectionGesture.ts | sed -n '1,80p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba src/tools/video-editor/hooks/useTimelineClipsForAttachments.ts | sed -n '1,120p' && nl -ba src/tools/video-editor/contexts/VideoEditorProvider.tsx | sed -n '66,100p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 14000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba src/tools/video-editor/components/AgentChat/AgentChat.tsx | sed -n '1,120p;250,330p;470,520p;790,825p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"userSelectTimelineClip|userSelectTimelineClips|userSelectGalleryItem|userSelectGalleryItems|systemSyncGallerySelection|systemClearGallerySelection|editorReplaceTimelineSelection|systemResetSelectionForProjectChange|systemResetTimelineSelection|editorSelectTimelineClip|editorClearTimelineSelection|editorSetSelectedTrackId\" src/app/providers/AppProviders.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx src/shared/hooks/gallery/useGallerySelectionBridge.ts src/tools/image-generation/pages/ImageGenerationToolPage.tsx src/tools/video-editor/hooks/useClipDrag.ts src/tools/video-editor/hooks/useClipDrag.helpers.ts src/tools/video-editor/hooks/useMarqueeSelect.ts src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx src/tools/video-editor/components/VideoEditorShell.tsx src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/useTimelineState.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "test ! -e src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.ts && test ! -e src/features/gallery/components/GenerationsPane/hooks/useModifierKeys.test.tsx && echo useModifierKeys-deleted\nrg \"useModifierKeys\" src/ || true\nrg \"useSelectionStoreApi\" src/ || true\nrg \"clearGallery\" src/ || true\nrg \"displayedClips|function mergeSelectedClips|const mergeSelectedClips|replaceSelectedTimelineClips|timelineClips\" src/tools/video-editor/components/AgentChat src/shared/contexts src/tools/video-editor/contexts src/app/providers -g '*.ts*' || true",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "git diff --stat && git status --short | sed -n '1,120p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba src/tools/video-editor/components/AgentChat/AgentChatMessage.test.tsx | sed -n '1,220p' && nl -ba src/tools/video-editor/contexts/VideoEditorProvider.test.tsx | sed -n '1,140p;250,330p;390,430p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 40000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,90p' src/tools/image-generation/pages/ImageGenerationToolPage.tsx && sed -n '80,120p' src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx && rg -n \"isAdditiveSelectionEvent|modifiers\" src/tools/image-generation/pages/ImageGenerationToolPage.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.tsx src/shared/components/MediaGalleryItem.tsx src/shared/components/MediaGalleryItem/hooks/useItemInteraction.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```
