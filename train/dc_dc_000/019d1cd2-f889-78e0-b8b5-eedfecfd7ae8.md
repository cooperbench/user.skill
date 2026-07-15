> DEVELOPER

You are an independent reviewer. Critique the plan against the actual repository.

        Project directory:
        /Users/user_c042661f/Documents/announcement-video

        Idea:
Unified timeline model + effects system + text overlays + transitions. Major evolution of the editing model:

PART 1 - FLAT TRACK MODEL: Replace the current hardcoded track types (video/audio/overlay) with a flat numbered track stack. Visual tracks V1-Vn stack bottom to top. Audio tracks A1-An. Any visual clip can go on any visual track. Each track has properties: scale, fit (cover/contain/manual), opacity, blend mode. The current background (output.background) becomes a clip on V1 with fit:cover. The current video track becomes V2 with scale:0.95. Overlays go on V3+. Text goes on V4+. Users can add/remove/reorder tracks freely. timeline.json gets a tracks array.

PART 2 - EFFECTS SYSTEM: Preset library of entrance/exit/continuous animations stored per-clip in timeline.json as entrance:{type,duration}, exit:{type,duration}, continuous:{type,intensity}. Effects registry maps type names to React components in shared/effects/. Entrances: slide-up/down/left/right, zoom-in, zoom-spin, pulse, fade, flip, bounce. Exits: slide-down, zoom-out, flip, fade-out, shrink, dissolve. Continuous: ken-burns, float, glitch, slow-zoom, drift. Timeline visualization: wedge indicators at clip edges for entrance/exit, subtle pattern for continuous. ClipPanel: dropdown selectors with duration/intensity sliders.

PART 3 - TRANSITIONS: Between adjacent clips using @remotion/transitions. Types: crossfade, wipe, slide-push, zoom-through. Stored in timeline.json on the later clip as transition:{type,duration}. Visualized on timeline as overlap region between clips. Selector in ClipPanel.

PART 4 - TEXT OVERLAYS: Text clips on visual tracks with content/font/size/color/position/animation. Rendered as React components by Remotion. Editable in ClipPanel with text formatting controls. Timeline shows text content preview in the clip bar.

PART 5 - TIMELINE UI: Update react-timeline-editor to show flat track stack. Track headers show V1/V2/A1 labels with track property controls. Clip bars show: asset name, effect indicators (entrance/exit wedges, continuous pattern), text preview for text clips, waveforms for audio. Drag clips between tracks. Add/remove/reorder tracks.

CONSTRAINTS: All config in timeline.json (AI-editable). Shared compositions in shared/ used by both viewer and remotion. Effects are composable React components. Migrate existing timeline.yaml-era data to new format. Keep Python tools working.

        Plan:
        # Implementation Plan: Unified Track Model, Effects, Transitions & Text Overlays

## Overview

**Goal:** Replace the hardcoded 3-track model (video/audio/overlay) with a flat numbered track stack (V1-Vn, A1-An), add a per-clip effects system with entrance/exit/continuous animations, add inter-clip transitions via `@remotion/transitions`, add text overlay clips, and update the timeline UI to reflect all of the above.

**Current state:** The repo has a JSON-driven timeline (`timeline.json`) with 3 hardcoded track types, a shared composition layer (`shared/compositions/`), a viewer editor (`viewer/src/`) using `@xzdarcy/react-timeline-editor`, Remotion Studio for preview/render, and Python CLI tools. Effects are currently split: fade_in/fade_out live in clip.effects, but entrance/exit/continuous animations are hardcoded per-asset in `VideoTrack.tsx:246-255` via `EFFECT_BY_ASSET`. There are no transitions, no text clips, and tracks cannot be added/removed/reordered.

**Key constraints:**
- `timeline.json` stays AI-editable and is the source of truth
- Shared compositions in `shared/` used by both viewer and remotion
- Python tools (`tools/*.py`) must keep working
- Existing timeline data must migrate cleanly
- `asset-registry.json` unchanged except for new asset registrations

**Scope:** ~50 files touched across shared types, compositions, viewer UI, remotion config, and Python tools. Organized into 5 phases matching the 5 parts of the spec.

---

## Phase 1: Flat Track Model

### Step 1: Define new types and track schema
**Scope:** Small
1. **Update** `shared/types.ts:1-69` — Add `TrackDefinition` type with `id` (e.g. "V1", "A1"), `kind` ("visual" | "audio"), `label?`, `scale?`, `fit?` ("cover" | "contain" | "manual"), `opacity?`, `blendMode?`. Add `tracks: TrackDefinition[]` to `TimelineConfig`. Change `TimelineClip.track` from `TimelineTrack` literal union to `string` (track ID reference). Add `clipType` field: "media" | "text" | "hold". Remove the `TimelineTrack` type alias.
2. **Update** `shared/serialize.ts:1-69` — Add `tracks` to allowed top-level keys in `validateSerializedConfig()`. Add `TRACK_DEFINITION_FIELDS` ordered list for serialization. Update `serializeForDisk()` to include tracks array.

### Step 2: Write migration logic
**Scope:** Medium
1. **Add** `shared/migrate.ts` — Function `migrateToFlatTracks(config: any): TimelineConfig` that:
   - If `config.tracks` exists, return as-is (already migrated)
   - Otherwise, synthesize default tracks: `V1` (background, fit:cover), `V2` (video, scale:0.95), `V3` (overlay), `A1` (audio)
   - Remap `clip.track`: "video" → "V2", "audio" → "A1", "overlay" → "V3"
   - Move `output.background` + `output.background_scale` into a new clip on V1 with `clipType: "hold"`, `hold: <timeline duration>`, `fit: "cover"`
   - Remove `output.background` and `output.background_scale` from output
2. **Call** migration in `remotion/src/load-config.ts:40-60` after loading JSON, and in `viewer/src/timeline-data.ts` inside `loadTimelineJson()`.
3. **Run** migration on `timeline.json` once and commit the migrated file.

### Step 3: Update editor-utils for flat tracks
**Scope:** Medium
1. **Update** `shared/editor-utils.ts:1-154` — Remove `TRACK_ORDER` constant. Add helpers: `getVisualTracks(config)`, `getAudioTracks(config)`, `getTrackById(config, id)`, `addTrack(config, track, position?)`, `removeTrack(config, trackId)`, `reorderTracks(config, trackIds[])`. Update `splitClipAtPlayhead()` and other clip functions to work with string track IDs.
2. **Update** `shared/config-utils.ts:1-65` — Remove any hardcoded track type assumptions. `getTimelineDurationInFrames()` should iterate all clips regardless of track type.

### Step 4: Update compositions for flat tracks
**Scope:** Large
1. **Rewrite** `shared/compositions/TimelineRenderer.tsx:1-37` — Instead of filtering by hardcoded track names, iterate `config.tracks` in order. For each visual track, render clips sorted by `at`. For each audio track, render audio clips. Apply track-level properties (scale, fit, opacity, blendMode) as a wrapper `<div>` around each track's clips.
2. **Merge** `VideoTrack.tsx`, `OverlayTrack.tsx`, and `Background.tsx` into a single `shared/compositions/VisualClip.tsx` component. A visual clip renders based on asset type (video/image) and clip properties (position, scale, fit). Remove `EFFECT_BY_ASSET` — effects will come from clip data in Phase 2.
3. **Keep** `AudioTrack.tsx` mostly as-is but update to accept any track ID.
4. **Delete** `Background.tsx` (background is now a clip on V1).

### Step 5: Update viewer data model
**Scope:** Large
1. **Update** `viewer/src/timeline-data.ts:1-393` — `configToRows()` now creates one `TimelineRow` per track from `config.tracks`. Row ID = track ID. `rowsToConfig()` maps back. `ClipMeta` gains track ID. `inferTrackType()` replaced by track selection UI.
2. **Update** `viewer/src/App.tsx:1-820` — `materializeData()`, `handleAssetDrop()`, `handleDeleteClip()` all use track IDs. Track headers show V1/V2/A1 labels. Add track management UI (add/remove/reorder) in a sidebar or toolbar.

### Step 6: Update Python tools
**Scope:** Medium
1. **Update** `tools/common.py` — `load_timeline()` calls a Python-side migration equivalent: if no `tracks` key, synthesize defaults and remap clip track fields. Add `get_track_by_id()`, `get_visual_tracks()`, `get_audio_tracks()`.
2. **Update** `tools/view.py` — Group clips by track ID instead of hardcoded type. Show track labels in text output.
3. **Update** `tools/place.py` — Accept `--track V2` instead of inferring from type. Default to V2 for video assets.
4. **Update** `tools/render.py` — No changes needed if Remotion handles rendering (it reads timeline.json directly). For ffmpeg engine, update track iteration.

### Step 7: Validate Phase 1
**Scope:** Small
1. **Run** migration on current `timeline.json`, verify output structure.
2. **Start** Remotion Studio, verify preview renders correctly with migrated data.
3. **Start** viewer, verify timeline shows tracks correctly, clips are editable.
4. **Run** `python3 tools/view.py` and `python3 tools/view.py --summary`, verify output.
5. **Test** drag-and-drop between tracks in viewer.

---

## Phase 2: Effects System

### Step 8: Define effects types and registry
**Scope:** Medium
1. **Update** `shared/types.ts` — Replace `TimelineEffect` with:
   ```typescript
   entrance?: { type: string; duration: number };
   exit?: { type: string; duration: number };
   continuous?: { type: string; intensity: number };
   ```
   These go directly on `TimelineClip` (not nested in `effects`). Keep `effects` for backward compat during migration, then remove.
2. **Create** `shared/effects/index.ts` — Effects registry mapping type names to React components. Export `entranceEffects`, `exitEffects`, `continuousEffects` as `Record<string, ComponentType>`.
3. **Create** `shared/effects/entrances.tsx` — slide-up, slide-down, slide-left, slide-right, zoom-in, zoom-spin, pulse, fade, flip, bounce. Each is a React wrapper component that applies CSS transforms/opacity based on frame progress.
4. **Create** `shared/effects/exits.tsx` — slide-down, zoom-out, flip, fade-out, shrink, dissolve.
5. **Create** `shared/effects/continuous.tsx` — ken-burns, float, glitch, slow-zoom, drift.

### Step 9: Integrate effects into rendering
**Scope:** Medium
1. **Update** `shared/compositions/VisualClip.tsx` (from Step 4) — Look up entrance/exit/continuous from clip data. Wrap clip render in the appropriate effect components from the registry. Remove `EFFECT_BY_ASSET` and `combineEffects()` from old `VideoTrack.tsx`.
2. **Update** `shared/compositions/Effects.tsx:1-35` — Deprecate `useClipOpacity()` in favor of the entrance/exit system. The `fade` entrance and `fade-out` exit replace fade_in/fade_out.
3. **Migrate** existing `EFFECT_BY_ASSET` mappings into clip-level effect data in `timeline.json` via the migration script (update `shared/migrate.ts`).

### Step 10: Add effects UI to viewer
**Scope:** Medium
1. **Update** `viewer/src/ClipPanel.tsx:1-190` — Add entrance/exit/continuous sections with dropdown selectors (populated from registry) and duration/intensity sliders.
2. **Update** `viewer/src/App.tsx` — `handleSelectedClipChange()` now handles entrance/exit/continuous fields. Serialize these in `rowsToConfig()`.
3. **Update** timeline clip rendering in `App.tsx`'s `getActionRender()` — Add wedge indicators at clip start (entrance) and end (exit). Add subtle pattern/icon for continuous effects.

### Step 11: Update serialization and Python
**Scope:** Small
1. **Update** `shared/serialize.ts` — Add `entrance`, `exit`, `continuous` to `TIMELINE_CLIP_FIELDS`.
2. **Update** `tools/common.py` — Recognize new fields in timeline JSON. `view.py` shows effect names in clip display.

### Step 12: Validate Phase 2
**Scope:** Small
1. **Verify** each entrance animation renders correctly in Remotion Studio.
2. **Verify** each exit and continuous effect.
3. **Test** effect selection in ClipPanel updates timeline.json and preview.
4. **Verify** Python `view.py` displays effects.

---

## Phase 3: Transitions

### Step 13: Add @remotion/transitions dependency
**Scope:** Small
1. **Install** `@remotion/transitions` in both `remotion/` and `viewer/` (or shared if hoisted).
2. **Update** `shared/types.ts` — Add to `TimelineClip`:
   ```typescript
   transition?: { type: string; duration: number };
   ```

### Step 14: Implement transition rendering
**Scope:** Medium
1. **Create** `shared/transitions/index.ts` — Registry mapping type names (crossfade, wipe, slide-push, zoom-through) to `@remotion/transitions` presentation objects.
2. **Update** `shared/compositions/TimelineRenderer.tsx` — For adjacent visual clips on the same track where the later clip has a `transition`, use `<TransitionSeries>` from `@remotion/transitions` instead of plain `<Sequence>`. Calculate overlap region based on `transition.duration`.

### Step 15: Add transition UI
**Scope:** Medium
1. **Update** `viewer/src/ClipPanel.tsx` — Add transition section with type dropdown and duration slider. Only shown when clip has an adjacent predecessor on the same track.
2. **Update** timeline rendering in `App.tsx` — Visualize transition as overlap region between adjacent clips (shaded area or connecting element).

### Step 16: Update serialization and Python
**Scope:** Small
1. **Update** `shared/serialize.ts` — Add `transition` to `TIMELINE_CLIP_FIELDS`.
2. **Update** `tools/common.py` and `tools/view.py` — Recognize and display transitions.

### Step 17: Validate Phase 3
**Scope:** Small
1. **Test** each transition type between two clips in Remotion Studio.
2. **Test** transition UI in viewer — select, change duration, preview.
3. **Verify** Python tools handle transitions without errors.

---

## Phase 4: Text Overlays

### Step 18: Define text clip type
**Scope:** Small
1. **Update** `shared/types.ts` — Add text-specific fields to `TimelineClip`:
   ```typescript
   text?: {
     content: string;
     fontFamily?: string;
     fontSize?: number;
     color?: string;
     backgroundColor?: string;
     align?: "left" | "center" | "right";
     bold?: boolean;
     italic?: boolean;
   };
   ```
   Text clips use `clipType: "text"`, live on visual tracks, and use `hold` for duration plus `x`, `y` for positioning.

### Step 19: Implement text rendering
**Scope:** Medium
1. **Create** `shared/compositions/TextClip.tsx` — React component that renders text with styling from clip.text properties. Supports entrance/exit/continuous effects (reuses Phase 2 system). Positioned absolutely using clip x/y/width/height.
2. **Update** `shared/compositions/TimelineRenderer.tsx` — When rendering visual track clips, check `clipType === "text"` and render `TextClip` instead of `VisualClip`.

### Step 20: Add text editing UI
**Scope:** Medium
1. **Update** `viewer/src/ClipPanel.tsx` — When a text clip is selected, show text content editor (textarea), font family dropdown, font size slider, color picker, alignment buttons, bold/italic toggles.
2. **Update** `viewer/src/App.tsx` — Add "Add Text" button/tool that creates a text clip on the selected visual track. Timeline clip bars show text content preview (truncated).
3. **Update** `viewer/src/timeline-data.ts` — Handle text clip serialization in `configToRows()` and `rowsToConfig()`.

### Step 21: Validate Phase 4
**Scope:** Small
1. **Create** a text clip via UI, verify it renders in preview.
2. **Edit** text properties, verify live update.
3. **Apply** entrance/exit effects to text clip, verify rendering.
4. **Verify** Python tools display text clips correctly.

---

## Phase 5: Timeline UI Polish

### Step 22: Track management UI
**Scope:** Medium
1. **Update** `viewer/src/App.tsx` — Add track header area showing V1/V2/A1 labels. Add buttons: add visual track, add audio track, remove empty track, reorder tracks (drag or up/down arrows). Track property controls in header: scale slider, fit dropdown, opacity slider, blend mode dropdown.
2. **Ensure** drag-and-drop between tracks works: dragging a clip from V2 to V3 updates `clip.track`.

### Step 23: Enhanced clip bar rendering
**Scope:** Medium
1. **Update** `getActionRender()` in `viewer/src/App.tsx` — Show: asset name, entrance wedge (angled left edge if entrance effect), exit wedge (angled right edge if exit effect), subtle pattern/icon for continuous effects, text preview for text clips, waveform visualization for audio clips (stretch goal — can defer).
2. **Style** transition overlap regions between adjacent clips.

### Step 24: Final integration validation
**Scope:** Medium
1. **Full end-to-end test:** Create a timeline with V1 background, V2 video clips with effects and transitions, V3 image overlay, V4 text overlay, A1 audio. Verify preview in viewer and Remotion Studio.
2. **Run** all Python tools against the new timeline format.
3. **Render** final output with `python3 tools/render.py`.
4. **Test** round-trip: edit in viewer → save → reload → verify no data loss.

---

## Execution Order

### Foundation (do first)
1. Step 1 (types) → Step 2 (migration) → Step 3 (editor-utils) — These establish the new data model.

### Rendering (after foundation)
2. Step 4 (compositions) — Verify Remotion renders correctly with new model.
3. Step 6 (Python tools) — Can run in parallel with Step 5.

### Viewer (after rendering works)
4. Step 5 (viewer data model) → Step 7 (validate Phase 1).

### Effects (after Phase 1 validated)
5. Step 8 (effects types) → Step 9 (rendering) → Step 10 (UI) → Step 11 (serialization) → Step 12 (validate).

### Transitions (after effects)
6. Step 13 (dependency) → Step 14 (rendering) → Step 15 (UI) → Step 16 (serialization) → Step 17 (validate).

### Text (after transitions, or in parallel)
7. Step 18 (types) → Step 19 (rendering) → Step 20 (UI) → Step 21 (validate).

### Polish (last)
8. Step 22 (track UI) → Step 23 (clip bars) → Step 24 (final validation).

## Validation Order

1. **After Step 2:** Run migration on current timeline.json, inspect output manually.
2. **After Step 4:** `npx remotion studio` — verify preview renders.
3. **After Step 5:** Start viewer, verify timeline loads and clips are interactive.
4. **After Step 7:** Full Phase 1 validation (viewer + studio + Python).
5. **After Step 9:** Test each effect in Remotion Studio.
6. **After Step 12:** Full Phase 2 validation.
7. **After Step 14:** Test transitions in Remotion Studio.
8. **After Step 19:** Test text clip rendering.
9. **After Step 24:** Full end-to-end validation.


        Plan metadata:
        {
  "version": 1,
  "timestamp": "2026-03-23T23:30:00Z",
  "hash": "sha256:e4305876b79bb3923755f13c6364c9b25920891021b44010d4aea944767b9fe6",
  "questions": [
    "Should the background truly become a clip on V1, or should it remain a special output-level property? Making it a clip means it shows in the timeline UI and can be trimmed/moved (more flexible but more complex). Keeping it as output.background is simpler but inconsistent with the flat track model.",
    "For the effects system, should entrance/exit/continuous fields replace the existing clip.effects array (which currently holds fade_in/fade_out), or live alongside it? The plan assumes replacing it and treating 'fade' as an entrance type and 'fade-out' as an exit type.",
    "For transitions using @remotion/transitions, the library expects clips to be wrapped in <TransitionSeries> which changes the rendering model significantly. Currently clips are independent <Sequence> elements. Should we only use TransitionSeries for clips that actually have transitions, or restructure all visual clip rendering to always use TransitionSeries?",
    "The react-timeline-editor library (@xzdarcy/react-timeline-editor) \u2014 does it support arbitrary track counts and drag-between-tracks natively, or will we need to work around limitations? This could significantly affect the Phase 5 effort.",
    "For text overlays, should the text styling be inline in timeline.json (as proposed) or should text styles be defined as reusable presets (e.g. 'title', 'subtitle', 'caption') referenced by name? Inline is simpler and more AI-editable; presets reduce repetition."
  ],
  "success_criteria": [
    "timeline.json has a tracks array with V1-Vn visual tracks and A1-An audio tracks, and all clips reference tracks by ID",
    "Existing timeline data migrates automatically \u2014 no manual JSON editing required to upgrade",
    "Background renders as a clip on V1 with fit:cover (or equivalent if kept as output property)",
    "Video clips on V2+ render with correct scale, fit, and opacity from track properties",
    "All 10 entrance effects, 6 exit effects, and 5 continuous effects render correctly in Remotion",
    "Effects are stored per-clip in timeline.json as entrance/exit/continuous objects",
    "ClipPanel shows effect dropdowns with duration/intensity controls",
    "Timeline clip bars show entrance/exit wedge indicators and continuous effect patterns",
    "Transitions between adjacent clips render using @remotion/transitions with 4 types: crossfade, wipe, slide-push, zoom-through",
    "Transition overlap regions are visible in the timeline UI",
    "Text clips render styled text on visual tracks with configurable font/size/color/position",
    "Text clips support entrance/exit/continuous effects",
    "ClipPanel shows text editing controls when a text clip is selected",
    "Tracks can be added, removed, and reordered in the viewer UI",
    "Clips can be dragged between tracks in the viewer",
    "Python tools (view.py, place.py, render.py) work with the new timeline format",
    "Round-trip editing works: viewer save \u2192 reload \u2192 no data loss",
    "Remotion Studio and viewer both render the same composition from shared/ components",
    "python3 tools/render.py produces correct output with the new format"
  ],
  "assumptions": [
    "The @xzdarcy/react-timeline-editor library supports dynamic row counts \u2014 we can add/remove rows at runtime. If it doesn't support drag-between-rows natively, we'll implement it via onDragEnd handlers that move clip data between rows.",
    "Background will become a clip on V1 (consistent with flat model) unless the user prefers otherwise. The migration creates this clip automatically.",
    "The existing fade_in/fade_out in clip.effects will be migrated to the new entrance/exit system. 'fade' entrance with the same duration replaces fade_in; 'fade-out' exit replaces fade_out.",
    "The EFFECT_BY_ASSET hardcoded mappings in VideoTrack.tsx will be migrated into clip-level effect data in timeline.json, then the hardcoded map is deleted.",
    "TransitionSeries will only wrap clips that have transitions \u2014 other clips continue using plain Sequence rendering to minimize disruption.",
    "Text clips use the same positioning model as current overlays (x, y, width, height, opacity) plus a text{} object for styling.",
    "The clipType field ('media' | 'text' | 'hold') is needed to distinguish rendering behavior since track type alone doesn't determine it.",
    "Python migration runs automatically on load (like the TS side) \u2014 if timeline.json lacks a tracks array, tools synthesize defaults. A one-time migration script also exists to permanently update the file.",
    "Blend modes on tracks map to CSS mix-blend-mode and are a nice-to-have \u2014 if they cause rendering issues in Remotion's video renderer, they can be deferred.",
    "Waveform visualization in audio clip bars is a stretch goal and not required for success."
  ],
  "structure_warnings": []
}

        Plan structure warnings from validator:
        []

        Existing flags:
        []

        Requirements:
        - Consider whether the plan is at the right level of abstraction.
        - Reuse existing flag IDs when the same concern is still open.
        - `verified_flag_ids` should list previously addressed flags that now appear resolved.
        - Focus on concrete issues that would cause real problems.
        - Robustness level: standard. Use balanced judgment. Flag significant risks, but do not spend flags on minor polish or executor-obvious boilerplate.
        - Verify that the plan remains aligned with the user's original intent.
        - Verify that the plan follows the expected structure: one H1 title, `## Overview`, numbered `## Step N:` sections with file references and numbered substeps, plus `## Execution Order` or `## Validation Order`. Missing structure should be flagged as category `completeness` with severity_hint `likely-significant`.
        - Flag scope creep explicitly when the plan grows beyond the original idea or recorded user notes. Use the phrase "Scope creep:" in the concern.
        - Assign severity_hint carefully. Implementation details the executor will naturally resolve should usually be `likely-minor`.

> AGENT

{"flags":[{"id":"flag-text-clip-model-incomplete","concern":"Phase 4's text-clip model does not fit the current load/save pipeline. The repo currently requires every clip to carry an asset ID and only serializes the existing clip fields, but the plan adds `clipType`/`text` without defining how those clips survive validation and resolution.","category":"correctness","severity_hint":"likely-significant","evidence":"`shared/types.ts:8-23` makes `asset` required on every `TimelineClip`. `shared/serialize.ts:3-19,45-57` only allows the current clip keys and would reject new `clipType`/`text` fields unless explicitly added. Both loaders eagerly resolve every clip asset and throw on missing assets in `viewer/src/timeline-data.ts:130-139` and `remotion/src/load-config.ts:83-92`."},{"id":"flag-overlay-editor-omitted","concern":"Phase 1 misses the existing WYSIWYG overlay editing path. Flattening tracks and removing `output.background_scale` will break overlay/text editing unless `OverlayEditor` is redesigned, but the plan never includes that file.","category":"completeness","severity_hint":"likely-significant","evidence":"`viewer/src/OverlayEditor.tsx:63-77` only reads `row-overlay` and filters to clips with `track === 'overlay'`. Its coordinate math depends on `backgroundScale` in `viewer/src/OverlayEditor.tsx:107-119`. `viewer/src/App.tsx:748-756` passes `data.output.background_scale` directly into that editor. The plan changes the background model and track model but does not mention `viewer/src/OverlayEditor.tsx`."},{"id":"flag-ffmpeg-path-underestimated","concern":"Step 6 understates the Python/renderer work. The legacy ffmpeg engine is tightly coupled to the current `video/audio/overlay` model and to `output.background` / `output.background_scale`, so the proposed schema change would break `tools/render.py` unless it is redesigned, not just lightly updated.","category":"correctness","severity_hint":"likely-significant","evidence":"`tools/render.py:95-107` hard-codes `video`, `audio`, and `overlay` clip partitions. `tools/render.py:122-125` and `tools/render.py:304-316` still composite `output.background` and `output.background_scale`. Overlay composition is also hard-coded in `tools/render.py:201-229`. The plan says 'No changes needed if Remotion handles rendering' for `tools/render.py`, but the success criteria still require `python3 tools/render.py` to work."},{"id":"flag-asset-drop-track-targeting-missing","concern":"Phase 1 does not solve how a newly imported asset gets assigned to a specific Vn/An track. The current drag/drop flow only knows coarse track type and ignores row position, so arbitrary track counts need new targeting UX or drop logic.","category":"completeness","severity_hint":"likely-significant","evidence":"`viewer/src/AssetPanel.tsx:100-103` only writes `asset-key` and `track-type` into drag data. `viewer/src/App.tsx:467-480` computes drop time from X only and does not inspect Y/row hit-testing. `viewer/src/App.tsx:374-449` then routes the new clip through hard-coded `video`/`audio`/`overlay` branches. The plan says `handleAssetDrop()` will use track IDs, but it does not cover the missing track-selection/drop-target mechanism."},{"id":"flag-plan-structure-mismatch","concern":"The plan structure does not match the required format. It uses phase sections with `### Step N` subsections instead of top-level numbered `## Step N:` sections.","category":"completeness","severity_hint":"likely-significant","evidence":"The submitted plan has `## Phase 1`, `## Phase 2`, etc., and nests steps under `### Step 1`, `### Step 2`, rather than using the required sequence of `## Step N:` sections."}],"verified_flag_ids":[],"disputed_flag_ids":[]}

> TOOL

tool_use exec_command
```json
{
  "cmd": "pwd && rg --files",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
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
  "cmd": "git status --short",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba shared/types.ts | sed -n '1,220p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
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
  "cmd": "nl -ba shared/compositions/TimelineRenderer.tsx | sed -n '1,220p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
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
  "cmd": "nl -ba viewer/src/timeline-data.ts | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 5000
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
  "cmd": "nl -ba viewer/src/App.tsx | sed -n '1,320p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 7000
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
  "cmd": "nl -ba viewer/src/App.tsx | sed -n '320,760p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 9000
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
  "cmd": "nl -ba viewer/src/ClipPanel.tsx | sed -n '1,320p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 7000
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
  "cmd": "nl -ba shared/editor-utils.ts | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 6000
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
  "cmd": "nl -ba shared/config-utils.ts | sed -n '1,220p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
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
  "cmd": "nl -ba shared/serialize.ts | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 5000
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
  "cmd": "nl -ba remotion/src/load-config.ts | sed -n '1,240p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
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
  "cmd": "nl -ba tools/common.py | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 5000
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
  "cmd": "nl -ba tools/view.py | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 5000
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
  "cmd": "nl -ba tools/place.py | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 6000
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
  "cmd": "nl -ba tools/render.py | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 6000
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
  "cmd": "nl -ba shared/compositions/VideoTrack.tsx | sed -n '1,320p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 7000
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
  "cmd": "nl -ba shared/compositions/OverlayTrack.tsx | sed -n '1,280p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 6000
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
  "cmd": "nl -ba shared/compositions/Background.tsx | sed -n '1,220p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
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
  "cmd": "nl -ba shared/compositions/Effects.tsx | sed -n '1,220p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
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
  "cmd": "cat viewer/package.json",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
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
  "cmd": "cat remotion/package.json",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
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
  "cmd": "nl -ba timeline.json | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 7000
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
  "cmd": "nl -ba timeline.yaml | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 7000
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
  "cmd": "rg -n \"row-video|row-overlay|row-audio|overlay\" viewer/src shared remotion/src tools | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 7000
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
  "cmd": "rg -n \"EFFECT_BY_ASSET|fade_in|fade_out|background_scale|background\" shared viewer remotion/src tools | sed -n '1,320p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 7000
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
  "cmd": "nl -ba viewer/src/timeline-data.ts | sed -n '260,460p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 6000
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
  "cmd": "nl -ba viewer/src/OverlayEditor.tsx | sed -n '1,320p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
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
  "cmd": "nl -ba viewer/src/AssetPanel.tsx | sed -n '1,340p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 9000
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
  "cmd": "nl -ba tools/view.py | sed -n '260,520p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 9000
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
  "cmd": "nl -ba remotion/src/CompositionVideo.tsx | sed -n '1,220p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
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
  "cmd": "nl -ba remotion/src/Root.tsx | sed -n '1,220p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
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
  "cmd": "nl -ba viewer/src/RemotionPreview.tsx | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 5000
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
  "cmd": "nl -ba remotion/server.mjs | sed -n '1,320p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
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
  "cmd": "nl -ba tools/render.py | sed -n '260,380p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 5000
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
  "cmd": "nl -ba tools/migrate_yaml_to_json.py | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 7000
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
  "cmd": "rg -n \"onRowDrag|row drag|onActionMoveEnd|row\" viewer/node_modules/@xzdarcy/react-timeline-editor -g '*.d.ts' -g '*.ts' -g '*.js' | sed -n '1,220p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 7000
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
  "cmd": "rg -n \"drag.*row|row.*drag|onActionMoveEnd|editorData\" viewer/node_modules/@xzdarcy/react-timeline-editor/dist/index.d.ts viewer/node_modules/@xzdarcy/react-timeline-editor/dist/*.d.ts | sed -n '1,220p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 7000
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
  "cmd": "nl -ba remotion/src/timeline/Timeline.tsx | sed -n '1,240p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 5000
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
  "cmd": "nl -ba remotion/setup-public.sh | sed -n '1,220p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
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
  "cmd": "rg -n \"track|background|effects|clips\" tools/cli.py tools/search.py tools/ingest.py tools/imagegen.py tools/tts.py | sed -n '1,220p'",
  "workdir": "/Users/user_c042661f/Documents/announcement-video",
  "yield_time_ms": 1000,
  "max_output_tokens": 5000
}
```

> TOOL

tool_result exec_command
```
null
```

> DEVELOPER

You are an independent reviewer. Critique the plan against the actual repository.

        Project directory:
        /Users/user_c042661f/Documents/announcement-video

        Idea:
Unified timeline model + effects system + text overlays + transitions. Major evolution of the editing model:

PART 1 - FLAT TRACK MODEL: Replace the current hardcoded track types (video/audio/overlay) with a flat numbered track stack. Visual tracks V1-Vn stack bottom to top. Audio tracks A1-An. Any visual clip can go on any visual track. Each track has properties: scale, fit (cover/contain/manual), opacity, blend mode. The current background (output.background) becomes a clip on V1 with fit:cover. The current video track becomes V2 with scale:0.95. Overlays go on V3+. Text goes on V4+. Users can add/remove/reorder tracks freely. timeline.json gets a tracks array.

PART 2 - EFFECTS SYSTEM: Preset library of entrance/exit/continuous animations stored per-clip in timeline.json as entrance:{type,duration}, exit:{type,duration}, continuous:{type,intensity}. Effects registry maps type names to React components in shared/effects/. Entrances: slide-up/down/left/right, zoom-in, zoom-spin, pulse, fade, flip, bounce. Exits: slide-down, zoom-out, flip, fade-out, shrink, dissolve. Continuous: ken-burns, float, glitch, slow-zoom, drift. Timeline visualization: wedge indicators at clip edges for entrance/exit, subtle pattern for continuous. ClipPanel: dropdown selectors with duration/intensity sliders.

PART 3 - TRANSITIONS: Between adjacent clips using @remotion/transitions. Types: crossfade, wipe, slide-push, zoom-through. Stored in timeline.json on the later clip as transition:{type,duration}. Visualized on timeline as overlap region between clips. Selector in ClipPanel.

PART 4 - TEXT OVERLAYS: Text clips on visual tracks with content/font/size/color/position/animation. Rendered as React components by Remotion. Editable in ClipPanel with text formatting controls. Timeline shows text content preview in the clip bar.

PART 5 - TIMELINE UI: Update react-timeline-editor to show flat track stack. Track headers show V1/V2/A1 labels with track property controls. Clip bars show: asset name, effect indicators (entrance/exit wedges, continuous pattern), text preview for text clips, waveforms for audio. Drag clips between tracks. Add/remove/reorder tracks.

CONSTRAINTS: All config in timeline.json (AI-editable). Shared compositions in shared/ used by both viewer and remotion. Effects are composable React components. Migrate existing timeline.yaml-era data to new format. Keep Python tools working.

        Plan:
        # Implementation Plan: Unified Track Model, Effects, Transitions & Text Overlays

## Overview

**Goal:** Replace the hardcoded 3-track model (video/audio/overlay) with a flat numbered track stack (V1-Vn, A1-An), add a per-clip effects system with entrance/exit/continuous animations, add inter-clip transitions via `@remotion/transitions`, add text overlay clips, and update the timeline UI to reflect all of the above.

**Current state:** The repo has a JSON-driven timeline (`timeline.json`) with 3 hardcoded track types, a shared composition layer (`shared/compositions/`), a viewer editor (`viewer/src/`) using `@xzdarcy/react-timeline-editor`, Remotion Studio for preview/render, and Python CLI tools. Effects are currently split: fade_in/fade_out live in clip.effects, but entrance/exit/continuous animations are hardcoded per-asset in `VideoTrack.tsx` via `EFFECT_BY_ASSET`. There are no transitions, no text clips, and tracks cannot be added/removed/reordered.

**Key constraints:**
- `timeline.json` stays AI-editable and is the source of truth
- Shared compositions in `shared/` used by both viewer and remotion
- Python tools (`tools/*.py`) must keep working
- Existing timeline data must migrate cleanly
- `asset-registry.json` unchanged except for new asset registrations

**Scope:** ~50 files touched across shared types, compositions, viewer UI, remotion config, and Python tools.

---

## Step 1: Define new types and track schema (`shared/types.ts`, `shared/serialize.ts`)
**Scope:** Medium

1. **Update** `shared/types.ts:1-37` — Add `TrackDefinition` type with `id` (e.g. "V1", "A1"), `kind` ("visual" | "audio"), `label?`, `scale?`, `fit?` ("cover" | "contain" | "manual"), `opacity?`, `blendMode?`. Add `tracks: TrackDefinition[]` to `TimelineConfig`. Change `TimelineClip.track` from `TimelineTrack` literal union to `string` (track ID reference). Add `clipType?: "media" | "text" | "hold"` field. Make `asset` optional (`asset?: string`) — text and hold clips may not reference an asset. Add text styling fields:
   ```typescript
   text?: {
     content: string;
     fontFamily?: string;
     fontSize?: number;
     color?: string;
     backgroundColor?: string;
     align?: "left" | "center" | "right";
     bold?: boolean;
     italic?: boolean;
   };
   ```
   Add effect fields directly on `TimelineClip`:
   ```typescript
   entrance?: { type: string; duration: number };
   exit?: { type: string; duration: number };
   continuous?: { type: string; intensity: number };
   transition?: { type: string; duration: number };
   ```
   Remove the `TimelineTrack` type alias. Update `ResolvedTimelineClip` so `assetEntry` is optional (undefined for text/hold clips without assets).

2. **Update** `shared/serialize.ts:3-19` — Add `clipType`, `text`, `entrance`, `exit`, `continuous`, `transition` to `TIMELINE_CLIP_FIELDS`. Update `serializeClipForDisk()` to handle optional `asset` — only include `asset` in output when present. Update `validateSerializedConfig()` (`serialize.ts:46-48`) to accept `"clips,output,tracks"` as valid top-level keys (in addition to `"clips,output"` for pre-migration files). Add `TRACK_DEFINITION_FIELDS` ordered list for track serialization.

## Step 2: Write migration logic (`shared/migrate.ts`)
**Scope:** Medium

1. **Create** `shared/migrate.ts` — Function `migrateToFlatTracks(config: any): TimelineConfig` that:
   - If `config.tracks` exists, return as-is (already migrated)
   - Otherwise, synthesize default tracks: `V1` (background, fit:cover), `V2` (video, scale:0.95), `V3` (overlay), `A1` (audio)
   - Remap `clip.track`: "video" → "V2", "audio" → "A1", "overlay" → "V3"
   - Move `output.background` + `output.background_scale` into a new clip on V1 with `clipType: "hold"`, `hold: <timeline duration>`, `fit: "cover"`, `asset: <background asset id>`
   - Remove `output.background` and `output.background_scale` from output
   - Migrate existing `clip.effects` (fade_in/fade_out) to `entrance`/`exit` fields: `{fade_in: N}` → `entrance: {type: "fade", duration: N}`, `{fade_out: N}` → `exit: {type: "fade-out", duration: N}`
   - Migrate `EFFECT_BY_ASSET` hardcoded mappings (from `VideoTrack.tsx`) into clip-level effect data by asset ID lookup

2. **Update** loaders to call migration and handle optional assets:
   - `remotion/src/load-config.ts:83-92` — Call `migrateToFlatTracks()` after loading JSON. Change asset resolution loop to skip clips where `clip.asset` is undefined (text clips, hold clips without assets). Set `assetEntry` to `undefined` for those clips.
   - `viewer/src/timeline-data.ts:130-139` — Same: call migration in `loadTimelineJson()`, skip asset resolution for clips without `asset` field.

3. **Run** migration on `timeline.json` once and commit the migrated file.

## Step 3: Update editor-utils and config-utils (`shared/editor-utils.ts`, `shared/config-utils.ts`)
**Scope:** Medium

1. **Update** `shared/editor-utils.ts:1-154` — Remove `TRACK_ORDER` constant. Add helpers: `getVisualTracks(config)`, `getAudioTracks(config)`, `getTrackById(config, id)`, `addTrack(config, track, position?)`, `removeTrack(config, trackId)`, `reorderTracks(config, trackIds[])`. Update `splitClipAtPlayhead()` and other clip functions to work with string track IDs instead of `TimelineTrack` union.

2. **Update** `shared/config-utils.ts:1-65` — Remove any hardcoded track type assumptions. `getTimelineDurationInFrames()` should iterate all clips regardless of track type.

## Step 4: Update compositions for flat tracks (`shared/compositions/`)
**Scope:** Large

1. **Rewrite** `shared/compositions/TimelineRenderer.tsx:1-37` — Instead of filtering by hardcoded track names, iterate `config.tracks` in order. For each visual track, render clips sorted by `at`. For each audio track, render audio clips. Apply track-level properties (scale, fit, opacity, blendMode) as a wrapper `<div>` around each track's clips.

2. **Merge** `VideoTrack.tsx`, `OverlayTrack.tsx`, and `Background.tsx` into a single `shared/compositions/VisualClip.tsx` component. A visual clip renders based on asset type (video/image) and clip properties (position, scale, fit). Remove `EFFECT_BY_ASSET` — effects come from clip data (migrated in Step 2).

3. **Create** `shared/compositions/TextClip.tsx` — React component that renders text with styling from `clip.text` properties. Positioned absolutely using clip `x`/`y`/`width`/`height`. Reuses the effects system (entrance/exit/continuous wrappers applied in Step 9).

4. **Update** `TimelineRenderer.tsx` — When rendering visual track clips, check `clipType`: render `TextClip` for `"text"`, `VisualClip` for `"media"` and `"hold"`.

5. **Keep** `AudioTrack.tsx` mostly as-is but update to accept any track ID string.

6. **Delete** `Background.tsx` (background is now a clip on V1).

## Step 5: Update OverlayEditor for flat tracks (`viewer/src/OverlayEditor.tsx`)
**Scope:** Medium

1. **Update** `OverlayEditor.tsx:63-77` — Replace the hardcoded `rows.find(row => row.id === "row-overlay")` with iteration over all visual track rows (V3+). Filter to clips on any visual track that have positional properties (`x`/`y` defined), not just `track === 'overlay'`. This makes the editor work for overlays and text clips on any visual track.

2. **Update** `OverlayEditor.tsx:107-119` — The `backgroundScale` prop currently comes from `output.background_scale`. After migration, the background is a clip on V1 and `output.background_scale` is removed. Replace `backgroundScale` with a value derived from the V2 track's `scale` property (passed from App.tsx). Specifically:
   - `App.tsx:748-756` currently passes `data.output.background_scale` — change this to read the V2 track definition's `scale` (defaulting to 0.95).
   - The coordinate math in `computeLayout()` stays the same; only the source of the scale value changes.

3. **Update** `OverlayEditor.tsx` to also support text clips — when a text clip is being dragged/resized, update the same `x`/`y`/`width`/`height` fields.

## Step 6: Update viewer data model and drop targeting (`viewer/src/timeline-data.ts`, `viewer/src/App.tsx`, `viewer/src/AssetPanel.tsx`)
**Scope:** Large

1. **Update** `viewer/src/timeline-data.ts:149+` — `configToRows()` now creates one `TimelineRow` per track from `config.tracks`. Row ID = track ID (e.g. "V1", "V2", "A1"). `rowsToConfig()` maps back. `ClipMeta` gains optional `clipType`, `text`, `entrance`, `exit`, `continuous`, `transition` fields. Remove `inferTrackType()`. Handle clips without `asset` (text/hold clips) in resolution — set `assetEntry` to undefined.

2. **Update** `viewer/src/AssetPanel.tsx:100-103` — In `onDragStart`, continue setting `asset-key` and `track-type` in drag data. Add a `target-track` data field that defaults to empty (will be populated by drop-target hit-testing).

3. **Update** `viewer/src/App.tsx:467-482` — Implement Y-axis hit-testing in `onTimelineDrop()`. Use the drop event's `clientY` relative to the timeline rows to determine which track row was targeted. Pass the resolved track ID to `handleAssetDrop()` instead of coarse `trackType`.

4. **Update** `viewer/src/App.tsx:366-454` — Rewrite `handleAssetDrop()` to accept a track ID string. Remove the hardcoded `"video"`/`"audio"`/`"overlay"` branching. Instead:
   - Look up the target track definition from `config.tracks`
   - For visual tracks: create clip with positional defaults appropriate to the track (V1-V2 get from/to, V3+ get hold/x/y/width/height)
   - For audio tracks: create clip with from/to/volume
   - Insert the action into the row matching the target track ID
   - If no specific track is targeted, fall back to: video assets → first available V track with no position data, audio assets → first A track, images → V3+

5. **Update** `viewer/src/App.tsx` — Track management UI: add/remove/reorder tracks via a sidebar or toolbar. Each track header shows V1/V2/A1 labels with track property controls (scale, fit, opacity, blend mode dropdowns/sliders). Add "Add Text" button that creates a text clip on the selected visual track.

## Step 7: Update Python tools for flat tracks (`tools/common.py`, `tools/view.py`, `tools/place.py`, `tools/render.py`)
**Scope:** Large

1. **Update** `tools/common.py` — `load_timeline()` calls a Python-side migration equivalent: if no `tracks` key, synthesize default tracks and remap clip track fields. Add `get_track_by_id()`, `get_visual_tracks()`, `get_audio_tracks()`. Handle clips without `asset` field (text/hold clips) — skip asset resolution for those.

2. **Update** `tools/view.py` — Group clips by track ID instead of hardcoded type. Show track labels in text output. Display effect names, transitions, and text content in clip display.

3. **Update** `tools/place.py` — Accept `--track V2` instead of inferring from type. Default to V2 for video assets, A1 for audio.

4. **Rewrite** `tools/render.py:95-316` ffmpeg engine — The `build_ffmpeg_command()` function hardcodes `video`/`audio`/`overlay` partitions and `output.background`/`output.background_scale`. This requires a substantial rewrite:
   - Replace the three hardcoded clip lists (`video_clips`, `audio_clips`, `overlay_clips`) with iteration over `config.tracks`: partition clips by track using `clip.track` matching track IDs.
   - For visual tracks: iterate tracks in order (V1 first = bottom layer). Each visual track's clips get composited. V1 clips render full-frame (fit:cover). V2+ clips render scaled per track properties.
   - Remove the dedicated background compositing block (`render.py:304-316`) — V1 clip handling replaces it.
   - Overlay compositing (`render.py:201-229`) becomes generic: any visual track with clips that have `x`/`y` positioning gets overlay-composited on top of lower tracks.
   - Audio tracks: iterate all A-tracks, same logic as current but keyed by track ID.
   - Skip text clips in ffmpeg path (text rendering in ffmpeg is out of scope — log a warning). Remotion handles text natively.
   - Skip entrance/exit/continuous effects in ffmpeg (only fade_in/fade_out were supported; log a warning for others). Preserve basic fade support by checking `entrance.type === "fade"` and `exit.type === "fade-out"`.

## Step 8: Validate Phase 1 — flat track model
**Scope:** Small

1. **Run** migration on current `timeline.json`, verify output structure has `tracks` array and clips reference track IDs.
2. **Start** Remotion Studio, verify preview renders correctly with migrated data.
3. **Start** viewer, verify timeline shows tracks correctly, clips are editable, overlay editor works.
4. **Run** `python3 tools/view.py` and `python3 tools/view.py --summary`, verify output.
5. **Test** drag-and-drop onto specific tracks in viewer — verify Y-axis targeting works.
6. **Test** `python3 tools/render.py --engine ffmpeg --dry-run` — verify ffmpeg command builds correctly with new track model.

## Step 9: Implement effects system (`shared/effects/`)
**Scope:** Medium

1. **Create** `shared/effects/index.ts` — Effects registry mapping type names to React components. Export `entranceEffects`, `exitEffects`, `continuousEffects` as `Record<string, ComponentType>`.
2. **Create** `shared/effects/entrances.tsx` — slide-up, slide-down, slide-left, slide-right, zoom-in, zoom-spin, pulse, fade, flip, bounce. Each is a React wrapper component that applies CSS transforms/opacity based on frame progress.
3. **Create** `shared/effects/exits.tsx` — slide-down, zoom-out, flip, fade-out, shrink, dissolve.
4. **Create** `shared/effects/continuous.tsx` — ken-burns, float, glitch, slow-zoom, drift.

## Step 10: Integrate effects into rendering (`shared/compositions/`)
**Scope:** Medium

1. **Update** `shared/compositions/VisualClip.tsx` (from Step 4) — Look up entrance/exit/continuous from clip data. Wrap clip render in the appropriate effect components from the registry. Remove `EFFECT_BY_ASSET` and `combineEffects()` from old `VideoTrack.tsx`.
2. **Update** `shared/compositions/TextClip.tsx` (from Step 4) — Same effect wrapping for text clips.
3. **Update** `shared/compositions/Effects.tsx:1-35` — Deprecate `useClipOpacity()` in favor of the entrance/exit system. The `fade` entrance and `fade-out` exit replace fade_in/fade_out.

## Step 11: Add effects UI to viewer (`viewer/src/ClipPanel.tsx`, `viewer/src/App.tsx`)
**Scope:** Medium

1. **Update** `viewer/src/ClipPanel.tsx:1-190` — Add entrance/exit/continuous sections with dropdown selectors (populated from registry) and duration/intensity sliders.
2. **Update** `viewer/src/App.tsx` — `handleSelectedClipChange()` now handles entrance/exit/continuous fields. Serialize these in `rowsToConfig()`.
3. **Update** timeline clip rendering in `App.tsx`'s `getActionRender()` — Add wedge indicators at clip start (entrance) and end (exit). Add subtle pattern/icon for continuous effects.

## Step 12: Validate Phase 2 — effects
**Scope:** Small

1. **Verify** each entrance animation renders correctly in Remotion Studio.
2. **Verify** each exit and continuous effect.
3. **Test** effect selection in ClipPanel updates timeline.json and preview.
4. **Verify** Python `view.py` displays effects.

## Step 13: Add transitions (`@remotion/transitions`)
**Scope:** Small

1. **Install** `@remotion/transitions` in both `remotion/` and `viewer/` (or shared if hoisted).
2. Types already added in Step 1 (`transition` field on `TimelineClip`).

## Step 14: Implement transition rendering (`shared/transitions/`, `shared/compositions/TimelineRenderer.tsx`)
**Scope:** Medium

1. **Create** `shared/transitions/index.ts` — Registry mapping type names (crossfade, wipe, slide-push, zoom-through) to `@remotion/transitions` presentation objects.
2. **Update** `shared/compositions/TimelineRenderer.tsx` — For adjacent visual clips on the same track where the later clip has a `transition`, use `<TransitionSeries>` from `@remotion/transitions` instead of plain `<Sequence>`. Calculate overlap region based on `transition.duration`.

## Step 15: Add transition UI (`viewer/src/ClipPanel.tsx`, `viewer/src/App.tsx`)
**Scope:** Medium

1. **Update** `viewer/src/ClipPanel.tsx` — Add transition section with type dropdown and duration slider. Only shown when clip has an adjacent predecessor on the same track.
2. **Update** timeline rendering in `App.tsx` — Visualize transition as overlap region between adjacent clips (shaded area or connecting element).

## Step 16: Validate Phase 3 — transitions
**Scope:** Small

1. **Test** each transition type between two clips in Remotion Studio.
2. **Test** transition UI in viewer — select, change duration, preview.
3. **Verify** Python tools handle transitions without errors.

## Step 17: Add text editing UI (`viewer/src/ClipPanel.tsx`, `viewer/src/App.tsx`)
**Scope:** Medium

1. **Update** `viewer/src/ClipPanel.tsx` — When a text clip is selected, show text content editor (textarea), font family dropdown, font size slider, color picker, alignment buttons, bold/italic toggles.
2. **Update** `viewer/src/App.tsx` — "Add Text" button (from Step 6) creates a text clip with `clipType: "text"`, no `asset`, and default `text` properties on the selected visual track. Timeline clip bars show text content preview (truncated).
3. **Update** `viewer/src/timeline-data.ts` — Handle text clip serialization in `configToRows()` and `rowsToConfig()` — text clips have no `asset`, use `hold` for duration.

## Step 18: Validate Phase 4 — text overlays
**Scope:** Small

1. **Create** a text clip via UI, verify it renders in preview.
2. **Edit** text properties, verify live update.
3. **Apply** entrance/exit effects to text clip, verify rendering.
4. **Drag/resize** text clip in OverlayEditor, verify positioning updates.
5. **Verify** Python tools display text clips correctly (view.py shows content, render.py skips text in ffmpeg with warning).

## Step 19: Timeline UI polish (`viewer/src/App.tsx`)
**Scope:** Medium

1. **Update** `viewer/src/App.tsx` — Track header area showing V1/V2/A1 labels. Buttons: add visual track, add audio track, remove empty track, reorder tracks (drag or up/down arrows). Track property controls in header: scale slider, fit dropdown, opacity slider, blend mode dropdown.
2. **Ensure** drag-and-drop between tracks works: dragging a clip from V2 to V3 updates `clip.track`.

## Step 20: Enhanced clip bar rendering (`viewer/src/App.tsx`)
**Scope:** Medium

1. **Update** `getActionRender()` in `viewer/src/App.tsx` — Show: asset name (or text preview for text clips), entrance wedge (angled left edge), exit wedge (angled right edge), subtle pattern/icon for continuous effects.
2. **Style** transition overlap regions between adjacent clips.

## Step 21: Final integration validation
**Scope:** Medium

1. **Full end-to-end test:** Create a timeline with V1 background, V2 video clips with effects and transitions, V3 image overlay, V4 text overlay, A1 audio. Verify preview in viewer and Remotion Studio.
2. **Run** all Python tools against the new timeline format.
3. **Render** final output with `python3 tools/render.py` (Remotion) and `python3 tools/render.py --engine ffmpeg` (verify ffmpeg handles new model without crashing).
4. **Test** round-trip: edit in viewer → save → reload → verify no data loss.
5. **Verify** text clips survive round-trip (no asset field, clipType preserved, text properties intact).

---

## Execution Order

### Foundation (Steps 1–3)
1. Step 1 (types + serialization) → Step 2 (migration) → Step 3 (editor-utils) — Establishes the new data model. All downstream work depends on this.

### Rendering + OverlayEditor (Steps 4–5, can partially overlap)
2. Step 4 (compositions) — Verify Remotion renders with new model.
3. Step 5 (OverlayEditor) — Must happen alongside or right after Step 4 since the old overlay row IDs and backgroundScale source change.

### Viewer + Python (Steps 6–7, can run in parallel)
4. Step 6 (viewer data model + drop targeting) — Depends on Steps 1–4.
5. Step 7 (Python tools + ffmpeg rewrite) — Can run in parallel with Step 6.

### Phase 1 validation (Step 8)
6. Step 8 — Gate: everything works with flat tracks before adding effects.

### Effects (Steps 9–12)
7. Step 9 (effects components) → Step 10 (rendering integration) → Step 11 (UI) → Step 12 (validate).

### Transitions (Steps 13–16)
8. Step 13 (dependency) → Step 14 (rendering) → Step 15 (UI) → Step 16 (validate).

### Text UI (Steps 17–18, after Steps 4+9 for rendering support)
9. Step 17 (text editing UI) → Step 18 (validate text).

### Polish (Steps 19–21)
10. Step 19 (track management UI) → Step 20 (clip bars) → Step 21 (final validation).

## Validation Order

1. **After Step 2:** Run migration on current timeline.json, inspect output manually.
2. **After Step 4:** `npx remotion studio` — verify preview renders.
3. **After Step 5:** Verify overlay editor works with new track model.
4. **After Step 6:** Start viewer, verify timeline loads, clips interactive, drops target correct tracks.
5. **After Step 7:** Run Python tools: `view.py`, `place.py --track V2`, `render.py --engine ffmpeg --dry-run`.
6. **After Step 8:** Full Phase 1 gate (viewer + studio + Python + overlay editor).
7. **After Step 10:** Test each effect in Remotion Studio.
8. **After Step 12:** Full Phase 2 validation.
9. **After Step 14:** Test transitions in Remotion Studio.
10. **After Step 18:** Test text clip creation, editing, rendering, and round-trip.
11. **After Step 21:** Full end-to-end validation.


        Plan metadata:
        {
  "version": 2,
  "timestamp": "2026-03-23T22:39:01Z",
  "hash": "sha256:1836e6456ef3c5795b0e45fa49df63dd09f3ab7cf979196b49241c722fd309be",
  "changes_summary": "Revised the plan to address all 5 significant flags:\n\n1. **Text clip model (flag-text-clip-model-incomplete):** Made `asset` optional on `TimelineClip` in Step 1. Added `clipType`, `text`, and all effect/transition fields to `TIMELINE_CLIP_FIELDS` in serialize.ts. Updated both loaders (remotion load-config.ts:83-92 and viewer timeline-data.ts:130-139) in Step 2 to skip asset resolution for clips without `asset`. Made `assetEntry` optional on `ResolvedTimelineClip`. Threaded text clips through validation, serialization, and round-trip testing.\n\n2. **OverlayEditor omission (flag-overlay-editor-omitted):** Added dedicated Step 5 covering OverlayEditor.tsx adaptation. Replaces hardcoded `row-overlay` lookup with iteration over visual track rows. Replaces `backgroundScale` sourced from `output.background_scale` with V2 track's `scale` property. Extends editor to support text clip drag/resize.\n\n3. **ffmpeg engine underestimated (flag-ffmpeg-path-underestimated):** Expanded Step 7 (Python tools) to include a substantial rewrite of `build_ffmpeg_command()` in render.py:95-316. Details the replacement of hardcoded video/audio/overlay partitions with track-based iteration, removal of the dedicated background compositing block, generic overlay compositing for positioned clips, and explicit handling of text clips (skip with warning) and new effects (fade only in ffmpeg).\n\n4. **Asset drop targeting (flag-asset-drop-track-targeting-missing):** Added explicit drop-target mechanism in Step 6. App.tsx:467-482 gets Y-axis hit-testing to resolve which track row was targeted. handleAssetDrop() rewritten to accept track ID string instead of coarse type. AssetPanel.tsx updated. Fallback logic defined for when no specific track is targeted.\n\n5. **Plan structure (flag-plan-structure-mismatch):** Restructured entire plan from `## Phase N` with `### Step N` to top-level `## Step N:` sections (21 steps total). Added `## Execution Order` and `## Validation Order` sections.",
  "flags_addressed": [
    "flag-text-clip-model-incomplete",
    "flag-overlay-editor-omitted",
    "flag-ffmpeg-path-underestimated",
    "flag-asset-drop-track-targeting-missing",
    "flag-plan-structure-mismatch"
  ],
  "questions": [
    "Should the background truly become a clip on V1, or should it remain a special output-level property? Making it a clip means it shows in the timeline UI and can be trimmed/moved (more flexible but more complex). Keeping it as output.background is simpler but inconsistent with the flat track model.",
    "For transitions using @remotion/transitions, the library expects clips to be wrapped in <TransitionSeries> which changes the rendering model significantly. Currently clips are independent <Sequence> elements. Should we only use TransitionSeries for clips that actually have transitions, or restructure all visual clip rendering to always use TransitionSeries?",
    "The react-timeline-editor library (@xzdarcy/react-timeline-editor) \u2014 does it support arbitrary track counts and drag-between-tracks natively, or will we need to work around limitations? This could significantly affect the Phase 5 effort.",
    "For text overlays, should the text styling be inline in timeline.json (as proposed) or should text styles be defined as reusable presets (e.g. 'title', 'subtitle', 'caption') referenced by name? Inline is simpler and more AI-editable; presets reduce repetition.",
    "For the ffmpeg engine rewrite: should we invest in a full rewrite to handle the new track model, or deprecate the ffmpeg engine (marking it experimental/legacy) and focus effort on the Remotion path? The ffmpeg engine is described as a 'comparison' engine in CLAUDE.md."
  ],
  "success_criteria": [
    "timeline.json has a tracks array with V1-Vn visual tracks and A1-An audio tracks, and all clips reference tracks by ID",
    "Existing timeline data migrates automatically \u2014 no manual JSON editing required to upgrade",
    "Background renders as a clip on V1 with fit:cover",
    "Video clips on V2+ render with correct scale, fit, and opacity from track properties",
    "All 10 entrance effects, 6 exit effects, and 5 continuous effects render correctly in Remotion",
    "Effects are stored per-clip in timeline.json as entrance/exit/continuous objects",
    "ClipPanel shows effect dropdowns with duration/intensity controls",
    "Timeline clip bars show entrance/exit wedge indicators and continuous effect patterns",
    "Transitions between adjacent clips render using @remotion/transitions with 4 types: crossfade, wipe, slide-push, zoom-through",
    "Transition overlap regions are visible in the timeline UI",
    "Text clips render styled text on visual tracks with configurable font/size/color/position",
    "Text clips support entrance/exit/continuous effects",
    "ClipPanel shows text editing controls when a text clip is selected",
    "Tracks can be added, removed, and reordered in the viewer UI",
    "Clips can be dragged between tracks in the viewer via Y-axis hit-testing on drop",
    "Python tools (view.py, place.py, render.py) work with the new timeline format",
    "Round-trip editing works: viewer save \u2192 reload \u2192 no data loss, including for text clips without asset fields",
    "Remotion Studio and viewer both render the same composition from shared/ components",
    "python3 tools/render.py produces correct output with the new format (Remotion engine)",
    "python3 tools/render.py --engine ffmpeg builds valid commands with the new track model (text clips skipped with warning)",
    "OverlayEditor works with flat track model \u2014 reads visual tracks by ID, derives scale from V2 track definition",
    "Text clips survive the full validation/serialization pipeline without asset field",
    "Asset drops target specific tracks via Y-axis hit-testing, with sensible fallbacks"
  ],
  "assumptions": [
    "The @xzdarcy/react-timeline-editor library supports dynamic row counts \u2014 we can add/remove rows at runtime. If it doesn't support drag-between-rows natively, we'll implement it via onDragEnd handlers that move clip data between rows.",
    "Background will become a clip on V1 (consistent with flat model). The migration creates this clip automatically with the existing background asset ID.",
    "The existing fade_in/fade_out in clip.effects will be migrated to the new entrance/exit system. 'fade' entrance with the same duration replaces fade_in; 'fade-out' exit replaces fade_out.",
    "The EFFECT_BY_ASSET hardcoded mappings in VideoTrack.tsx will be migrated into clip-level effect data in timeline.json, then the hardcoded map is deleted.",
    "TransitionSeries will only wrap clips that have transitions \u2014 other clips continue using plain Sequence rendering to minimize disruption.",
    "Text clips use clipType: 'text', have no asset field, and use hold for duration plus x/y for positioning. The same positioning model as current overlays.",
    "Making asset optional on TimelineClip is safe because all existing clips have assets \u2014 only new text/hold clips will omit it. Loaders skip resolution for clips without asset.",
    "The ffmpeg engine will skip text clips (logging a warning) since text rendering in ffmpeg filter graphs is out of scope. Remotion handles text natively. Only basic fade effects are preserved in ffmpeg; other entrance/exit/continuous effects log warnings.",
    "Blend modes on tracks map to CSS mix-blend-mode and are a nice-to-have \u2014 if they cause rendering issues in Remotion's video renderer, they can be deferred.",
    "Waveform visualization in audio clip bars is a stretch goal and not required for success.",
    "OverlayEditor's backgroundScale will be sourced from the V2 track definition's scale property (defaulting to 0.95) instead of output.background_scale, preserving the same coordinate math."
  ],
  "structure_warnings": [
    "Each `## Step N:` section should reference at least one file in backticks."
  ],
  "delta_from_previous_percent": 66.86
}

        Plan structure warnings from validator:
        [
  "Each `## Step N:` section should reference at least one file in backticks."
]

        Existing flags:
        [
  {
    "id": "flag-text-clip-model-incomplete",
    "concern": "Phase 4's text-clip model does not fit the current load/save pipeline. The repo currently requires every clip to carry an asset ID and only serializes the existing clip fields, but the plan adds `clipType`/`text` without defining how those clips survive validation and resolution.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "flag-overlay-editor-omitted",
    "concern": "Phase 1 misses the existing WYSIWYG overlay editing path. Flattening tracks and removing `output.background_scale` will break overlay/text editing unless `OverlayEditor` is redesigned, but the plan never includes that file.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "flag-ffmpeg-path-underestimated",
    "concern": "Step 6 understates the Python/renderer work. The legacy ffmpeg engine is tightly coupled to the current `video/audio/overlay` model and to `output.background` / `output.background_scale`, so the proposed schema change would break `tools/render.py` unless it is redesigned, not just lightly updated.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "flag-asset-drop-track-targeting-missing",
    "concern": "Phase 1 does not solve how a newly imported asset gets assigned to a specific Vn/An track. The current drag/drop flow only knows coarse track type and ignores row position, so arbitrary track counts need new targeting UX or drop logic.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "flag-plan-structure-mismatch",
    "concern": "The plan structure does not match the required format. It uses phase sections with `### Step N` subsections instead of top-level numbered `## Step N:` sections.",
    "status": "addressed",
    "severity": "significant"
  }
]

        Requirements:
        - Consider whether the plan is at the right level of abstraction.
        - Reuse existing flag IDs when the same concern is still open.
        - `verified_flag_ids` should list previously addressed flags that now appear resolved.
        - Focus on concrete issues that would cause real problems.
        - Robustness level: standard. Use balanced judgment. Flag significant risks, but do not spend flags on minor polish or executor-obvious boilerplate.
        - Verify that the plan remains aligned with the user's original intent.
        - Verify that the plan follows the expected structure: one H1 title, `## Overview`, numbered `## Step N:` sections with file references and numbered substeps, plus `## Execution Order` or `## Validation Order`. Missing structure should be flagged as category `completeness` with severity_hint `likely-significant`.
        - Flag scope creep explicitly when the plan grows beyond the original idea or recorded user notes. Use the phrase "Scope creep:" in the concern.
        - Assign severity_hint carefully. Implementation details the executor will naturally resolve should usually be `likely-minor`.

> AGENT

Reviewing the revised plan against the current repo again, focusing on whether the previous concerns are actually closed and whether the remaining plan still matches the code paths that exist today.

> AGENT

{"flags":[{"id":"flag-overlay-scale-model-still-global","concern":"Step 5 still hardcodes a single global preview scale by deriving `OverlayEditor` geometry from V2's `scale`. That preserves the old shared-container behavior, but the proposed model gives each visual track its own scale/fit/opacity/blend settings, so V3+/V4+ overlays and text can no longer be positioned correctly off a V2-only scale.","category":"correctness","severity_hint":"likely-significant","evidence":"Today there is only one shared visual scale because `shared/compositions/TimelineRenderer.tsx:19-32` wraps both video and overlay content in a single transformed container using `output.background_scale`. `viewer/src/OverlayEditor.tsx:107-119` mirrors that with one `backgroundScale` input. The revised plan's Step 5 says to keep that math and source the value from V2, but the new track model explicitly assigns scale/fit per track, not globally."},{"id":"flag-plan-structure-mismatch","concern":"The plan still does not fully meet the required structure because several `## Step N:` sections lack file references in backticks.","category":"completeness","severity_hint":"likely-significant","evidence":"The validator warning is still present: 'Each `## Step N:` section should reference at least one file in backticks.' Validation-only sections such as `## Step 8:`, `## Step 12:`, `## Step 16:`, `## Step 18:`, and `## Step 21:` do not cite any files."}],"verified_flag_ids":["flag-text-clip-model-incomplete","flag-overlay-editor-omitted","flag-ffmpeg-path-underestimated","flag-asset-drop-track-targeting-missing"],"disputed_flag_ids":[]}
