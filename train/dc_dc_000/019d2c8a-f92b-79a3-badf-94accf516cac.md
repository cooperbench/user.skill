> DEVELOPER

Review the implementation against the success criteria.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace/reigh-app

        Idea:
Light megaplan: Consolidate all TimelineData construction into a single canonical builder function. Currently there are multiple code paths that build TimelineData objects (buildDataFromCurrentRegistry, buildTimelineData, patchRegistry hand-assembly) and they don't all go through migration/deduplication. The fix is to make one function that guarantees consistent tracks/clips/config, and route all construction through it. This will eliminate the duplicate key bugs (V3 tracks, cascading -dup- clip IDs) at the structural level.

        Approved plan:
        # Implementation Plan: Canonical TimelineData Builder

## Overview

**Goal:** Consolidate all TimelineData construction into a single canonical builder so that migration, deduplication, and signature computation are guaranteed by construction — eliminating structural bugs (duplicate tracks, cascading `-dup-` clip IDs) at the source.

**Current state:** There are three places that assemble a `TimelineData` object:
1. **`buildTimelineData()`** (`timeline-data.ts:330`) — async, full rebuild with URL resolution
2. **`buildDataFromCurrentRegistry()`** (`timeline-save-utils.ts:19`) — sync, reuses existing registry/resolved URLs
3. **`patchRegistry()` inline literal** (`useTimelineSave.ts:331-352`) — sync, manually spreads fields

All three *do* call migration, but they do it independently. Additionally, `configToRows` (line 163) and `resolveTimelineConfig` in `config-utils.ts` (line 82) each call `migrateToFlatTracks` internally, so the async path migrates **3 times** (caller → resolver → configToRows) and sync paths migrate **2 times** (caller → configToRows). The inline literal in `patchRegistry` is the most fragile — it manually assembles 12 fields and mutates `signature` after construction.

**Key insight from audit:** Migration is not actually being skipped today — all paths call `migrateToFlatTracks`. The real problems are: (a) redundant multi-migration across `configToRows` and `resolveTimelineConfig`, (b) the inline assembly in `patchRegistry` is brittle and doesn't match the other two builders, (c) no single function guarantees all fields are consistently derived.

**Constraints:**
- `buildTimelineData` must stay async (URL resolution)
- `buildDataFromCurrentRegistry` and `patchRegistry` must stay sync (called in React callbacks)
- `patchRegistry` needs to update registry + resolved registry without re-resolving URLs

**Design boundary (DECISION-003):** `resolvedConfig` derivation remains caller-specific because of the sync/async split. The async path (`buildTimelineData`) resolves URLs via the network; the sync paths (`buildDataFromCurrentRegistry`, `patchRegistry`) reuse existing resolved data from `current`. The assembler centralizes the *object shape* and *derived fields* (rows, meta, effects, tracks, clipOrder, signature) but does not own resolvedConfig construction. This is an inherent constraint, not a gap.

**Migration call sites being updated (all 4):**

| Call site | File | Line | Action |
|-----------|------|------|--------|
| `configToRows` | `timeline-data.ts` | 163 | Remove internal migration (Step 2) |
| `resolveTimelineConfig` | `config-utils.ts` | 82 | Remove internal migration (Step 2) |
| `buildTimelineData` | `timeline-data.ts` | 336 | Keep — this is the entry-point migration |
| `buildDataFromCurrentRegistry` | `timeline-save-utils.ts` | 27 | Keep — this is the entry-point migration |
| `patchRegistry` (implicit via `configToRows`) | `useTimelineSave.ts` | 329 | Replace with explicit migration before assembler call (Step 5) |

After this change, migration happens exactly once per construction path: at the entry-point caller, never inside helpers.

## Phase 1: Foundation — builder + migration cleanup

### Step 1: Extract a sync `assembleTimelineData` function (`timeline-data.ts`)
**Scope:** Medium
1. **Create** a new exported function `assembleTimelineData` in `timeline-data.ts` (~line 330) that takes all pre-computed parts and returns `TimelineData`. This is the single place that stamps out the object shape and computes the signature.
   ```ts
   export function assembleTimelineData(parts: {
     config: TimelineConfig;      // must already be migrated
     configVersion: number;
     registry: AssetRegistry;
     resolvedConfig: ResolvedTimelineConfig;
     output: TimelineOutput;
     assetMap: Record<string, string>;
   }): TimelineData {
     const rowData = configToRows(parts.config);
     return {
       ...parts,
       rows: rowData.rows,
       meta: rowData.meta,
       effects: rowData.effects,
       tracks: rowData.tracks,
       clipOrder: rowData.clipOrder,
       signature: getConfigSignature(parts.resolvedConfig),
     };
   }
   ```
2. **Key invariant:** `config` passed in must already be migrated. Add a JSDoc comment making this contract explicit.
3. **No callers yet** — this step just adds the function and its types.

### Step 2: Remove migration from internal helpers (`timeline-data.ts:163`, `config-utils.ts:82`)
**Scope:** Small
1. **In `configToRows`** (`timeline-data.ts:160`): Remove line 163 (`const migratedConfig = migrateToFlatTracks(config)`) and use `config` directly. Rename the local variable references from `migratedConfig` to `config`.
2. **In `resolveTimelineConfig`** (`config-utils.ts:77`): Remove line 82 (`const migratedConfig = migrateToFlatTracks(config)`) and use `config` directly. Rename the local variable references from `migratedConfig` to `config`. Remove the `migrateToFlatTracks` import if now unused.
3. **Rationale:** Migration should happen exactly once at the entry point, not re-applied by every internal helper. After this change:
   - `configToRows` converts config→rows (no migration)
   - `resolveTimelineConfig` resolves asset URLs (no migration)
   - Entry-point callers own migration
4. **Risk:** If any caller was relying on these helpers to migrate for them, this would break. Audit confirms: `configToRows` is called by `buildTimelineData` (pre-migrates at line 336), `buildDataFromCurrentRegistry` (pre-migrates at line 27), and `patchRegistry` (will pre-migrate after Step 5). `resolveTimelineConfig` is only called by `buildTimelineData` (pre-migrates at line 336). All callers pre-migrate.
5. **Defense-in-depth:** The `getUniqueClipId` fallback inside `configToRows` (line 177) is kept — it logs a warning if a duplicate clip ID somehow survives, catching bugs upstream.

### Step 3: Run tests after migration removal
**Scope:** Small
1. **Run** `npx vitest run` scoped to video-editor tests to confirm the migration removal didn't break anything.
2. This is the cheapest validation checkpoint — catches any caller that was depending on internal migration.

## Phase 2: Route all construction through the builder

### Step 4: Refactor `buildTimelineData` (`timeline-data.ts:330-356`)
**Scope:** Small
1. **Rewrite** to delegate to `assembleTimelineData`:
   ```ts
   export const buildTimelineData = async (
     config: TimelineConfig,
     registry: AssetRegistry,
     urlResolver?: UrlResolver,
     configVersion = 1,
   ): Promise<TimelineData> => {
     const migratedConfig = migrateToFlatTracks(config);
     migratedConfig.tracks = migratedConfig.tracks ?? [];
     const resolvedConfig = await resolveTimelineConfig(migratedConfig, registry, urlResolver);
     return assembleTimelineData({
       config: migratedConfig,
       configVersion,
       registry,
       resolvedConfig,
       output: { ...migratedConfig.output },
       assetMap: buildAssetMap(registry),
     });
   };
   ```
2. **Verify** that `loadTimelineJsonFromProvider` (line 358) delegates to `buildTimelineData` and needs no changes.

### Step 5: Refactor `buildDataFromCurrentRegistry` (`timeline-save-utils.ts:19-56`)
**Scope:** Small
1. **Rewrite** to delegate to `assembleTimelineData`:
   ```ts
   export function buildDataFromCurrentRegistry(
     config: TimelineConfig,
     current: TimelineData,
   ): TimelineData {
     const migrated = migrateToFlatTracks(config);
     const tracks = migrated.tracks ?? [];
     const resolvedConfig = {
       output: { ...migrated.output },
       tracks,
       clips: migrated.clips.map((clip) => ({
         ...clip,
         assetEntry: clip.asset ? current.resolvedConfig.registry[clip.asset] : undefined,
       })),
       registry: { ...current.resolvedConfig.registry },
     };
     return assembleTimelineData({
       config: migrated,
       configVersion: current.configVersion,
       registry: { ...current.registry },
       resolvedConfig,
       output: { ...migrated.output },
       assetMap: Object.fromEntries(
         Object.entries(current.registry.assets ?? {}).map(([id, entry]) => [id, entry.file]),
       ),
     });
   }
   ```

### Step 6: Refactor `patchRegistry` inline literal (`useTimelineSave.ts:303-359`)
**Scope:** Medium — most impactful change
1. **Replace** the inline TimelineData literal (lines 331-352) with a call to `assembleTimelineData`. Add explicit migration at the entry point (previously handled implicitly by `configToRows`).
   ```ts
   const nextConfig = migrateToFlatTracks({
     ...current.config,
     customEffects: current.config.customEffects
       ? { ...current.config.customEffects }
       : undefined,
   });
   const nextResolvedConfig = {
     ...current.resolvedConfig,
     registry: nextResolvedRegistry,
     clips: nextConfig.clips.map((clip) => ({
       ...clip,
       assetEntry: clip.asset ? nextResolvedRegistry[clip.asset] : undefined,
     })),
   };
   const nextData = assembleTimelineData({
     config: nextConfig,
     configVersion: current.configVersion,
     registry: nextRegistry,
     resolvedConfig: nextResolvedConfig,
     output: nextConfig.output,
     assetMap: Object.fromEntries(
       Object.entries(nextRegistry.assets ?? {}).map(([id, entry]) => [id, entry.file]),
     ),
   });
   ```
2. **Remove** the manual `nextData.signature = getConfigSignature(...)` mutation — the assembler handles it.
3. **Note on `resolvedConfig.clips`:** The old code used `current.resolvedConfig.clips` (pre-existing resolved clips). The new code rebuilds from `nextConfig.clips` (migrated config clips) with `assetEntry` lookups. This is more correct — it ensures resolved clips reflect the migrated config, not stale resolved state. The old `configToRows(nextConfig)` call already rebuilt rows from scratch, so clip identity was already not preserved across patches.

## Phase 3: Tests

### Step 7: Add regression tests for `assembleTimelineData` and `buildDataFromCurrentRegistry` (`timeline-save-utils.test.ts`)
**Scope:** Medium
1. **Create** `src/tools/video-editor/lib/timeline-save-utils.test.ts` with:
   - **Test: `assembleTimelineData` produces consistent output** — pass a known config with 2 tracks and 3 clips, verify all 12 fields are present and signature matches `getConfigSignature(resolvedConfig)`.
   - **Test: duplicate track IDs are deduplicated** — pass config with duplicate track IDs through `migrateToFlatTracks` → `assembleTimelineData`, verify tracks are unique.
   - **Test: cascading `-dup-` clip IDs are cleaned** — pass config with clip IDs like `clip-1-dup-1-dup-2`, verify output clips have clean IDs.
   - **Test: `buildDataFromCurrentRegistry` preserves registry from current** — pass a new config and a mock `current` TimelineData, verify the output uses `current.registry` and `current.resolvedConfig.registry`.
   - **Test: `buildDataFromCurrentRegistry` migrates config** — pass config with duplicate tracks, verify output config has deduplicated tracks.
2. **These are pure function tests** — no React hooks or DOM needed, so they run fast and don't need `renderHook`.

### Step 8: Update test helper and run full suite
**Scope:** Small
1. **Update** `makeTimelineData()` in `useTimelineHistory.test.ts` (lines 49-76) — can either use `assembleTimelineData` or remain a standalone mock. Per DECISION-002, keeping it standalone is fine since it's test code. No change required unless it breaks.
2. **Run** `npx vitest run --reporter=verbose` for all video-editor tests:
   - `useTimelineHistory.test.ts`
   - `useTimelineTrackManagement.test.ts`
   - `render-bounds.validation.test.ts`
   - New `timeline-save-utils.test.ts`
3. **Fix** any breakage.

### Step 9: Manual smoke test
**Scope:** Small
1. **Load** a timeline with known V3 data (duplicate tracks) — confirm no duplicate key warnings in console.
2. **Upload** an asset (triggers `patchRegistry` path) — confirm no `-dup-` cascading in clip IDs.
3. **Undo/redo** several times — confirm data roundtrips cleanly through `buildDataFromCurrentRegistry`.

## Execution Order
1. Steps 1-2 (add assembler, remove migration from helpers) — foundation with no caller changes.
2. Step 3 (test checkpoint) — validate migration removal is safe before proceeding.
3. Steps 4-6 in sequence (refactor each caller one at a time).
4. Steps 7-8 (tests) — after all callers are routed through assembler.
5. Step 9 (manual smoke test) — final validation.

## Validation Order
1. After Step 2: run existing tests to confirm removing migration from `configToRows` and `resolveTimelineConfig` doesn't break anything.
2. After each of Steps 4-6: run existing tests to catch regressions incrementally.
3. After Step 7: run new regression tests for the assembler and sync construction paths.
4. Step 8: full test suite.
5. Step 9: manual smoke test for the specific bugs this addresses.


        Execution tracking state (`finalize.json`):
        {
  "tasks": [
    {
      "id": "T1",
      "description": "Extract sync `assembleTimelineData` function in `timeline-data.ts` (~line 330). Takes pre-computed parts (config, configVersion, registry, resolvedConfig, output, assetMap), calls `configToRows(config)` to derive rows/meta/effects/tracks/clipOrder, computes signature via `getConfigSignature(resolvedConfig)`, returns complete TimelineData. Add JSDoc noting config must already be migrated. No callers yet.",
      "depends_on": [],
      "status": "done",
      "executor_notes": "Extracted exported sync `assembleTimelineData` helper in `timeline-data.ts`. It accepts the precomputed parts (`config`, `configVersion`, `registry`, `resolvedConfig`, `output`, `assetMap`), derives `rows`/`meta`/`effects`/`tracks`/`clipOrder` via `configToRows(config)`, and returns a complete `TimelineData` with `signature` computed from `getConfigSignature(resolvedConfig)`. Added JSDoc that the incoming config must already be migrated. Verified with `npx tsc --noEmit`.",
      "files_changed": [
        "src/tools/video-editor/lib/timeline-data.ts"
      ],
      "commands_run": [
        "npx tsc --noEmit"
      ],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T2",
      "description": "Remove internal migration from `configToRows` (timeline-data.ts:163) and `resolveTimelineConfig` (config-utils.ts:82). In both, delete the `migrateToFlatTracks` call and use `config` directly. Remove unused `migrateToFlatTracks` import from config-utils.ts if applicable. Keep the `getUniqueClipId` fallback in configToRows (line 177) as defense-in-depth. GATE WARNING: Before editing config-utils.ts, grep for all callers of `resolveTimelineConfig` to verify assumption #6 (only called by buildTimelineData).",
      "depends_on": [
        "T1"
      ],
      "status": "done",
      "executor_notes": "Verified assumption #6 with a repo grep: `resolveTimelineConfig(` is only called from `buildTimelineData` in `timeline-data.ts`. Removed the internal `migrateToFlatTracks` call from `configToRows` and updated all former `migratedConfig` reads to `config`, while preserving the `getUniqueClipId` fallback unchanged as defense-in-depth. Removed the now-unused `migrateToFlatTracks` import and internal migration from `src/tools/video-editor/lib/config-utils.ts`, and updated the remaining references there to use `config` directly. Verified with `npx tsc --noEmit`.",
      "files_changed": [
        "src/tools/video-editor/lib/timeline-data.ts",
        "src/tools/video-editor/lib/config-utils.ts"
      ],
      "commands_run": [
        "rg -n \"resolveTimelineConfig\\(\" src",
        "npx tsc --noEmit"
      ],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T3",
      "description": "Run existing video-editor tests (`npx vitest run` scoped to video-editor) to validate migration removal from T2 is safe. All tests must pass before proceeding.",
      "depends_on": [
        "T2"
      ],
      "status": "done",
      "executor_notes": "Ran the existing `src/tools/video-editor` test suite with `npx vitest run --config config/testing/vitest.config.ts $(rg --files src/tools/video-editor | rg '\\.(test|spec)\\.(ts|tsx)$')`. All 9 existing video-editor test files passed without modification: 31 tests passed, 0 failed. This validates that the T2 migration removal did not introduce regressions in the current video-editor test surface.",
      "files_changed": [],
      "commands_run": [
        "npx vitest run --config config/testing/vitest.config.ts $(rg --files src/tools/video-editor | rg '\\.(test|spec)\\.(ts|tsx)$')"
      ],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T4",
      "description": "Refactor `buildTimelineData` (timeline-data.ts:330-356) to delegate to `assembleTimelineData`. Keep migration at entry point, keep async URL resolution via `resolveTimelineConfig`, then pass all parts to assembler. Verify `loadTimelineJsonFromProvider` (line 358) delegates to `buildTimelineData` and needs no changes.",
      "depends_on": [
        "T3"
      ],
      "status": "done",
      "executor_notes": "Refactored `buildTimelineData` in `src/tools/video-editor/lib/timeline-data.ts` to migrate at the entry point, resolve URLs asynchronously via `resolveTimelineConfig`, and then delegate final `TimelineData` construction to `assembleTimelineData`. `loadTimelineJsonFromProvider` was inspected and left unchanged; it still delegates to `buildTimelineData`. Verified with `npx tsc --noEmit` and the existing scoped video-editor test suite (`9` files, `31` tests, all passing).",
      "files_changed": [
        "src/tools/video-editor/lib/timeline-data.ts"
      ],
      "commands_run": [
        "npx tsc --noEmit",
        "npx vitest run --config config/testing/vitest.config.ts $(rg --files src/tools/video-editor | rg '\\.(test|spec)\\.(ts|tsx)$')"
      ],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T5",
      "description": "Refactor `buildDataFromCurrentRegistry` (timeline-save-utils.ts:19-56) to delegate to `assembleTimelineData`. Keep migration at entry point, rebuild resolvedConfig from current's resolved registry, pass all parts to assembler. Import assembleTimelineData from timeline-data.ts.",
      "depends_on": [
        "T3"
      ],
      "status": "done",
      "executor_notes": "Refactored `buildDataFromCurrentRegistry` in `src/tools/video-editor/lib/timeline-save-utils.ts` to migrate once at entry, rebuild `resolvedConfig` from `current.resolvedConfig.registry`, reuse `current.registry` as the source registry, and delegate all `TimelineData` assembly to `assembleTimelineData`. The output shape stays centralized through the canonical builder. Verified with `npx tsc --noEmit` and the existing scoped video-editor test suite (`9` files, `31` tests, all passing).",
      "files_changed": [
        "src/tools/video-editor/lib/timeline-save-utils.ts"
      ],
      "commands_run": [
        "npx tsc --noEmit",
        "npx vitest run --config config/testing/vitest.config.ts $(rg --files src/tools/video-editor | rg '\\.(test|spec)\\.(ts|tsx)$')"
      ],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T6",
      "description": "Refactor `patchRegistry` inline literal (useTimelineSave.ts:303-359) to delegate to `assembleTimelineData`. Add explicit `migrateToFlatTracks` call at entry point. Rebuild resolvedConfig.clips from nextConfig.clips (not stale current.resolvedConfig.clips). Remove manual `nextData.signature = getConfigSignature(...)` mutation. CAUTION: This changes resolvedConfig.clips derivation \u2014 verify clips with resolved assetEntry fields still work correctly.",
      "depends_on": [
        "T3"
      ],
      "status": "done",
      "executor_notes": "Refactored the `patchRegistry` path in `src/tools/video-editor/hooks/useTimelineSave.ts` to call `migrateToFlatTracks` explicitly at the entry point, rebuild `resolvedConfig.clips` from `migratedConfig.clips` using `nextResolvedRegistry` lookups, and delegate final object construction to `assembleTimelineData`. The manual `nextData.signature = ...` mutation was removed because signature now comes from the assembler. Verified with `npx tsc --noEmit` and the existing scoped video-editor test suite (`9` files, `31` tests, all passing), which covers the normal save/editor flows without exposing a regression from the fresh clip-assetEntry derivation.",
      "files_changed": [
        "src/tools/video-editor/hooks/useTimelineSave.ts"
      ],
      "commands_run": [
        "npx tsc --noEmit",
        "npx vitest run --config config/testing/vitest.config.ts $(rg --files src/tools/video-editor | rg '\\.(test|spec)\\.(ts|tsx)$')"
      ],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T7",
      "description": "Create `src/tools/video-editor/lib/timeline-save-utils.test.ts` with 5 regression tests: (1) assembleTimelineData produces consistent output with correct signature, (2) duplicate track IDs are deduplicated through migrate\u2192assemble, (3) cascading `-dup-` clip IDs are cleaned, (4) buildDataFromCurrentRegistry preserves registry from current, (5) buildDataFromCurrentRegistry migrates config with duplicate tracks. Pure function tests only \u2014 no renderHook or DOM.",
      "depends_on": [
        "T4",
        "T5",
        "T6"
      ],
      "status": "done",
      "executor_notes": "Added `src/tools/video-editor/lib/timeline-save-utils.test.ts` with 5 pure-function regression tests that cover: (1) `assembleTimelineData` output shape and signature correctness, (2) duplicate track-id deduplication through `migrateToFlatTracks` followed by `assembleTimelineData`, (3) cascading `-dup-` clip-id cleanup through migrate plus assemble, (4) `buildDataFromCurrentRegistry` preserving `current.registry` and `current.resolvedConfig.registry`, and (5) `buildDataFromCurrentRegistry` migrating duplicate-track configs before assembly. The file uses only local fixtures and pure helpers; it does not use `renderHook`, React, or DOM utilities. Verified with `npx tsc --noEmit` and `npx vitest run --config config/testing/vitest.config.ts src/tools/video-editor/lib/timeline-save-utils.test.ts` (5 tests passed).",
      "files_changed": [
        "src/tools/video-editor/lib/timeline-save-utils.test.ts"
      ],
      "commands_run": [
        "npx tsc --noEmit",
        "npx vitest run --config config/testing/vitest.config.ts src/tools/video-editor/lib/timeline-save-utils.test.ts"
      ],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T8",
      "description": "Run full video-editor test suite (`npx vitest run --reporter=verbose`): useTimelineHistory.test.ts, useTimelineTrackManagement.test.ts, render-bounds.validation.test.ts, and new timeline-save-utils.test.ts. Check if `makeTimelineData()` in useTimelineHistory.test.ts needs updates. Fix any breakage.",
      "depends_on": [
        "T7"
      ],
      "status": "done",
      "executor_notes": "Ran `npx vitest run --config config/testing/vitest.config.ts --reporter=verbose` against `useTimelineHistory.test.ts`, `useTimelineTrackManagement.test.ts`, `render-bounds.validation.test.ts`, and `timeline-save-utils.test.ts`. All 4 files passed with 25/25 tests green. Reviewed `makeTimelineData()` in `useTimelineHistory.test.ts`; its manual `TimelineData` fixture still matches the current shape and did not require updates.",
      "files_changed": [],
      "commands_run": [
        "npx vitest run --config config/testing/vitest.config.ts --reporter=verbose src/tools/video-editor/hooks/useTimelineHistory.test.ts src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts src/tools/video-editor/lib/render-bounds.validation.test.ts src/tools/video-editor/lib/timeline-save-utils.test.ts",
        "rg -n \"makeTimelineData|TimelineData\" src/tools/video-editor/hooks/useTimelineHistory.test.ts",
        "sed -n '49,88p' src/tools/video-editor/hooks/useTimelineHistory.test.ts"
      ],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T9",
      "description": "Final validation: (1) Grep for any remaining TimelineData object literals outside assembleTimelineData (except test mocks) \u2014 none should exist. (2) Grep for migrateToFlatTracks calls \u2014 should only appear in entry-point callers (buildTimelineData, buildDataFromCurrentRegistry, patchRegistry block), not in configToRows or resolveTimelineConfig. (3) Verify success criteria are met.",
      "depends_on": [
        "T8"
      ],
      "status": "done",
      "executor_notes": "Verified by grep that production full-shape `TimelineData` construction is centralized through `assembleTimelineData()` in exactly three caller paths: `buildTimelineData`, `buildDataFromCurrentRegistry`, and the `patchRegistry` flow. The only remaining production `TimelineData`-typed object literals are spread-based clones over existing data in `useTimelineSave.ts` and `preserveUploadingClips()`; they are not alternate construction paths from config/registry and do not bypass migration or deduplication. Verified by grep that `migrateToFlatTracks()` appears in production only at the intended entry points (`src/tools/video-editor/lib/timeline-data.ts`, `src/tools/video-editor/lib/timeline-save-utils.ts`, and `src/tools/video-editor/hooks/useTimelineSave.ts`), with the only extra matches in `timeline-save-utils.test.ts`. Success criteria are met.",
      "files_changed": [],
      "commands_run": [
        "rg -n \"TimelineData|assembleTimelineData|signature:\\s|getConfigSignature\\(|clipOrder:\\s|configVersion:\\s\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'",
        "rg -n \"migrateToFlatTracks\\(\" src/tools/video-editor",
        "sed -n '110,145p' src/tools/video-editor/hooks/useTimelineSave.ts",
        "sed -n '430,470p' src/tools/video-editor/lib/timeline-data.ts",
        "rg -n \"as TimelineData|: TimelineData\\s*=|return \\{\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'",
        "rg -n \"signature:\\s\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'",
        "rg -n \"assembleTimelineData\\(\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'"
      ],
      "evidence_files": [],
      "reviewer_verdict": ""
    }
  ],
  "watch_items": [
    "DEBT registry-patch-testing: patchRegistry() still lacks full integration test coverage (hook requires renderHook + mock context). Pure-function tests on assembleTimelineData partially mitigate. Do not make this worse \u2014 if any new untested paths are introduced, flag them.",
    "Assumption #6 verification: Before T2, grep to confirm resolveTimelineConfig (config-utils.ts) is only called by buildTimelineData. If another caller exists, removing its internal migration would silently pass unmigrated config.",
    "T6 changes resolvedConfig.clips derivation: Old code used current.resolvedConfig.clips (stale resolved clips). New code rebuilds from nextConfig.clips with assetEntry lookups. Verify this doesn't break clips whose resolved assetEntry differs from a fresh lookup.",
    "Migration idempotency assumption: The plan assumes migrateToFlatTracks is idempotent. If removing double-migration causes behavior changes, the migration function has side effects on already-migrated data \u2014 investigate before proceeding.",
    "getUniqueClipId fallback (configToRows line 177): Must be preserved as defense-in-depth. If it fires after these changes, it means migration missed something \u2014 treat as a bug, not expected behavior.",
    "Do not introduce new TimelineData object literals in production code \u2014 all construction must go through assembleTimelineData.",
    "DEBT items that touch adjacent code: clip-param-schema-evolution, conflict-resolution, optimistic-locking \u2014 none should be made worse by this change."
  ],
  "sense_checks": [
    {
      "id": "SC1",
      "task_id": "T1",
      "question": "Does assembleTimelineData return all 12 fields of TimelineData (config, configVersion, registry, resolvedConfig, output, assetMap, rows, meta, effects, tracks, clipOrder, signature)? Is the signature computed from resolvedConfig, not config?",
      "executor_note": "Confirmed `assembleTimelineData` returns all 12 `TimelineData` fields: `config`, `configVersion`, `registry`, `resolvedConfig`, `output`, `assetMap`, `rows`, `meta`, `effects`, `tracks`, `clipOrder`, and `signature`. The signature is computed from `resolvedConfig`, not `config`.",
      "verdict": ""
    },
    {
      "id": "SC2",
      "task_id": "T2",
      "question": "Was assumption #6 verified (resolveTimelineConfig only called by buildTimelineData)? Are all references to `migratedConfig` updated to `config` in both configToRows and resolveTimelineConfig? Is the migrateToFlatTracks import removed from config-utils.ts if unused?",
      "executor_note": "Assumption #6 was verified by grep: `resolveTimelineConfig(` is only called by `buildTimelineData`. All `migratedConfig` references in both `configToRows` and shared `resolveTimelineConfig` were updated to `config`, and the unused `migrateToFlatTracks` import was removed from `config-utils.ts`.",
      "verdict": ""
    },
    {
      "id": "SC3",
      "task_id": "T3",
      "question": "Do all existing video-editor tests pass without modification after migration removal?",
      "executor_note": "Yes. All existing video-editor tests passed without modification after the migration removal: 9 test files and 31 tests passed under the scoped `vitest` run.",
      "verdict": ""
    },
    {
      "id": "SC4",
      "task_id": "T4",
      "question": "Does buildTimelineData still produce identical output for the same inputs? Does loadTimelineJsonFromProvider still work without changes?",
      "executor_note": "Yes. `buildTimelineData` now delegates to `assembleTimelineData` after the existing entry-point migration and async `resolveTimelineConfig` call. `loadTimelineJsonFromProvider` was not changed and still delegates to `buildTimelineData`. Compile and scoped video-editor tests passed unchanged.",
      "verdict": ""
    },
    {
      "id": "SC5",
      "task_id": "T5",
      "question": "Does buildDataFromCurrentRegistry correctly reuse current.registry and current.resolvedConfig.registry (not rebuilding from scratch)? Does it still produce the same output shape?",
      "executor_note": "Yes. `buildDataFromCurrentRegistry` now reuses `current.registry` and `current.resolvedConfig.registry` rather than rebuilding those registries from scratch, while still rebuilding `resolvedConfig.clips` from the migrated config and returning the same `TimelineData` shape via `assembleTimelineData`.",
      "verdict": ""
    },
    {
      "id": "SC6",
      "task_id": "T6",
      "question": "Is the manual `nextData.signature = ...` mutation removed? Does the new resolvedConfig.clips derivation (from nextConfig.clips) produce equivalent results to the old approach (from current.resolvedConfig.clips) for the normal case?",
      "executor_note": "Yes. The manual `nextData.signature = ...` mutation was removed. `patchRegistry` now rebuilds `resolvedConfig.clips` from `nextConfig` after explicit migration, attaching asset entries from `nextResolvedRegistry`, which is equivalent to the old behavior for the normal case but avoids relying on stale `current.resolvedConfig.clips`. Compile and existing scoped video-editor tests passed after the change.",
      "verdict": ""
    },
    {
      "id": "SC7",
      "task_id": "T7",
      "question": "Do the 5 test cases cover: (1) output shape consistency, (2) duplicate track dedup, (3) cascading -dup- cleanup, (4) registry preservation, (5) config migration? Are they pure function tests with no React/DOM dependencies?",
      "executor_note": "Yes. The new test file contains 5 pure-function cases covering output shape consistency, duplicate track deduplication, cascading `-dup-` cleanup, registry preservation, and config migration. It uses no React, `renderHook`, or DOM dependencies, and the targeted run passed with 5/5 tests.",
      "verdict": ""
    },
    {
      "id": "SC8",
      "task_id": "T8",
      "question": "Does the full test suite pass? Did makeTimelineData() in useTimelineHistory.test.ts require updates, and if so, were they minimal?",
      "executor_note": "Yes. The requested verbose video-editor test suite passed cleanly: 4 files and 25 tests green. `makeTimelineData()` in `useTimelineHistory.test.ts` was inspected after the run and did not require any updates.",
      "verdict": ""
    },
    {
      "id": "SC9",
      "task_id": "T9",
      "question": "Grep confirms: (a) no TimelineData object literals outside assembleTimelineData (except test mocks), (b) migrateToFlatTracks only called at entry points, not in configToRows or resolveTimelineConfig?",
      "executor_note": "Yes. Grep confirms there are no alternate production full-shape `TimelineData` construction paths outside `assembleTimelineData()`; the only remaining `TimelineData`-typed literals are spread-based clones over existing data, not config/registry assembly. Grep also confirms `migrateToFlatTracks()` appears in production only at the intended entry points (`buildTimelineData`, `buildDataFromCurrentRegistry`, and the `patchRegistry` path), with extra matches only in test coverage.",
      "verdict": ""
    }
  ],
  "meta_commentary": "Execution guidance:\n\n**Critical pre-flight (T2):** Before removing migration from resolveTimelineConfig, grep for all its callers. The plan assumes only buildTimelineData calls it. If wrong, you'll silently break another path.\n\n**T4/T5/T6 are independent** after T3 passes \u2014 execute them in parallel or any order. T6 is the highest-risk change (most code, behavioral change in resolvedConfig.clips derivation). Consider running tests after each individually.\n\n**T6 behavioral change:** The old patchRegistry used `current.resolvedConfig.clips` (stale). The new code rebuilds clips from `nextConfig.clips` with fresh assetEntry lookups. This is theoretically more correct but could surface differences if any clip's resolved state was manually patched or transformed after initial resolution. Watch for this in testing.\n\n**The unresolved flag (registry-patch-testing):** patchRegistry lacks automated regression tests because it's a React hook callback requiring full context mocking. The gate accepted this gap. If during execution you find a clean way to extract testable logic from the patchRegistry path, do it \u2014 but don't block on it. The assembler tests + defense-in-depth getUniqueClipId fallback are the safety net.\n\n**Migration idempotency:** The entire plan relies on migrateToFlatTracks being idempotent. If removing double-migration causes test failures in T3, investigate whether migration has side effects on already-migrated data before trying to fix the tests.\n\n**Settled decisions (do not revisit):** DECISION-001 (sync assembler is canonical), DECISION-002 (test helpers may construct manually), DECISION-003 (resolvedConfig derivation stays caller-specific), DECISION-004 (migration removed from both configToRows and resolveTimelineConfig)."
}

        Plan metadata:
        {
  "version": 2,
  "timestamp": "2026-03-26T23:31:33Z",
  "hash": "sha256:ac213774a3a8bc9e64e1347f5939818e20066eac5e37776bee4b2e6fd02b379c",
  "changes_summary": "**Flag `timeline-builder-double-migration`:** Added `resolveTimelineConfig` in `config-utils.ts:82` as a fourth migration call site to be cleaned up in Step 2. The plan now enumerates all 4 internal migration calls (configToRows, resolveTimelineConfig, plus the 2 entry-point callers that are kept) in a table in the Overview. Step 2 now explicitly removes migration from both `configToRows` AND `resolveTimelineConfig`.\n\n**Flag `timeline-builder-not-canonical`:** Added an explicit \"Design boundary (DECISION-003)\" paragraph in the Overview explaining why `resolvedConfig` derivation remains caller-specific (sync/async split is inherent) and what the assembler does vs doesn't centralize. This is now a stated design choice, not an unstated gap.\n\n**Flag `timeline-builder-missing-regression-tests`:** Added Step 7 with 5 specific test cases for `assembleTimelineData` and `buildDataFromCurrentRegistry` in a new `timeline-save-utils.test.ts` file. These are pure function tests that cover: consistent output shape, duplicate track dedup, cascading dup-ID cleanup, registry preservation, and config migration. Updated success criteria to include the new tests.",
  "flags_addressed": [
    "timeline-builder-double-migration",
    "timeline-builder-not-canonical",
    "timeline-builder-missing-regression-tests"
  ],
  "questions": [
    "Are there any other internal helpers (beyond `configToRows` and `resolveTimelineConfig`) that call `migrateToFlatTracks`? The audit found these two plus the entry-point callers, but if there are others (e.g., in serialization or export paths), they would also need updating."
  ],
  "success_criteria": [
    "Only one function (`assembleTimelineData`) stamps out TimelineData objects \u2014 all other construction paths delegate to it",
    "No TimelineData object literal `{ config: ..., rows: ..., ... }` exists outside `assembleTimelineData` (except test mocks per DECISION-002)",
    "`migrateToFlatTracks` is called exactly once per construction path \u2014 removed from `configToRows` (timeline-data.ts:163) and `resolveTimelineConfig` (config-utils.ts:82), kept only at entry-point callers",
    "All existing video-editor tests pass without modification (other than test helper updates)",
    "New regression tests in `timeline-save-utils.test.ts` cover: assembler output consistency, duplicate track dedup, cascading dup-ID cleanup, registry preservation, and config migration",
    "No duplicate-key React warnings when loading V3 timeline data",
    "No cascading `-dup-` clip ID suffixes after registry patches"
  ],
  "assumptions": [
    "Migration (`migrateToFlatTracks`) is idempotent \u2014 running it twice on already-migrated data produces identical output. This is assumed true based on the implementation (dedup is stable, track/clip transforms are no-ops on clean data) and is what makes removing the multi-migration safe.",
    "The `patchRegistry` path can safely rebuild rows/meta/effects from config via `configToRows` rather than preserving them from `current`. This is what it already does today (line 329 calls `configToRows(nextConfig)`).",
    "TimelineData is only constructed in browser-side code within the video-editor tool. No edge functions or workers build TimelineData objects.",
    "The `getUniqueClipId` fallback inside `configToRows` (line 177) is kept as defense-in-depth even after migration handles dedup \u2014 it logs a warning if it ever fires, which means migration missed something.",
    "Test helpers may continue to construct TimelineData manually (DECISION-002). The key invariant is that production code uses the assembler.",
    "`resolveTimelineConfig` in `config-utils.ts` is only called via the wrapper in `timeline-data.ts`, which is only called by `buildTimelineData`. No other code path calls the config-utils version directly."
  ],
  "structure_warnings": [],
  "delta_from_previous_percent": 40.5
}

        Gate summary:
        {
  "passed": true,
  "criteria_check": {
    "count": 7,
    "items": [
      "Only one function (`assembleTimelineData`) stamps out TimelineData objects \u2014 all other construction paths delegate to it",
      "No TimelineData object literal `{ config: ..., rows: ..., ... }` exists outside `assembleTimelineData` (except test mocks per DECISION-002)",
      "`migrateToFlatTracks` is called exactly once per construction path \u2014 removed from `configToRows` (timeline-data.ts:163) and `resolveTimelineConfig` (config-utils.ts:82), kept only at entry-point callers",
      "All existing video-editor tests pass without modification (other than test helper updates)",
      "New regression tests in `timeline-save-utils.test.ts` cover: assembler output consistency, duplicate track dedup, cascading dup-ID cleanup, registry preservation, and config migration",
      "No duplicate-key React warnings when loading V3 timeline data",
      "No cascading `-dup-` clip ID suffixes after registry patches"
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
      "id": "timeline-builder-missing-regression-tests",
      "concern": "Timeline data validation: The revised plan still leaves the highest-risk path, `patchRegistry()`, without automated regression coverage. The new pure-function tests cover `assembleTimelineData` and `buildDataFromCurrentRegistry`, but the duplicate-ID bug is explicitly expected to reproduce through the registry-patch flow, and that path still relies on manual smoke testing only.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "`patchRegistry()` contains distinct behavior beyond plain assembly in [/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/video-editor/hooks/useTimelineSave.ts:303], including rebuilding `nextResolvedRegistry`, preserving `src`, and committing with `{ save: false }` through [/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/video-editor/hooks/useTimelineSave.ts:358]. A repo-wide test search still shows no tests invoking `patchRegistry()` or `useTimelineSave()`, so Step 7 does not cover the exact path called out in Step 9.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    }
  ],
  "recommendation": "PROCEED",
  "rationale": "The plan is solid after iteration 2. The remaining flag (missing `patchRegistry` regression tests) is an executor-level detail, not a planning blocker. `patchRegistry` is a React hook callback that requires `renderHook` + mock context to test properly \u2014 the plan correctly identifies this as harder to unit-test and compensates with: (a) pure-function tests for the assembler it now delegates to, (b) manual smoke testing for the integration path, and (c) the defense-in-depth `getUniqueClipId` fallback that warns if dedup fails. The executor can add a `patchRegistry` integration test if feasible, but requiring it in the plan would be over-specifying.",
  "signals_assessment": "Weighted score dropped sharply from 4.25 to 1.5 across iterations, with 2 of 3 significant flags resolved. Plan delta was 40.5% \u2014 substantial but justified by the three flags addressed (double-migration fix, design boundary documentation, new test cases). No recurring critiques. No scope creep. Preflight clean. The single remaining flag is a completeness concern about hook-level test coverage, not a correctness or architectural issue.",
  "warnings": [
    "The executor should verify assumption #6 (resolveTimelineConfig is only called by buildTimelineData) with a grep before removing its internal migration \u2014 if another caller exists, it would silently receive unmigrated config.",
    "Step 6 changes resolvedConfig.clips derivation from current.resolvedConfig.clips to rebuilding from nextConfig.clips \u2014 verify this doesn't change behavior for clips with resolved assetEntry fields that differ from what a fresh lookup would produce."
  ],
  "settled_decisions": [
    {
      "id": "DECISION-001",
      "decision": "A sync assembleTimelineData function is the canonical builder for TimelineData objects.",
      "rationale": "Accepted in iteration 1, unchanged in iteration 2. All flags accepted the core design."
    },
    {
      "id": "DECISION-002",
      "decision": "Test helpers may construct TimelineData manually without routing through the assembler.",
      "rationale": "Coupling tests to implementation makes them brittle. Production code is the enforcement boundary."
    },
    {
      "id": "DECISION-003",
      "decision": "resolvedConfig derivation remains caller-specific (async resolves URLs, sync reuses existing).",
      "rationale": "Inherent constraint of the sync/async split. Explicitly documented in the plan as a design boundary, not a gap."
    },
    {
      "id": "DECISION-004",
      "decision": "Migration is removed from both configToRows AND resolveTimelineConfig, leaving exactly one migration per entry-point caller.",
      "rationale": "Resolved the double-migration flag. All 4 call sites enumerated and accounted for in the plan table."
    }
  ],
  "override_forced": false,
  "orchestrator_guidance": "Plan passed gate and preflight. Proceed to finalize. Verify unresolved flags against the plan and project code before accepting.",
  "robustness": "standard",
  "signals": {
    "iteration": 2,
    "idea": "Light megaplan: Consolidate all TimelineData construction into a single canonical builder function. Currently there are multiple code paths that build TimelineData objects (buildDataFromCurrentRegistry, buildTimelineData, patchRegistry hand-assembly) and they don't all go through migration/deduplication. The fix is to make one function that guarantees consistent tracks/clips/config, and route all construction through it. This will eliminate the duplicate key bugs (V3 tracks, cascading -dup- clip IDs) at the structural level.",
    "significant_flags": 1,
    "unresolved_flags": [
      {
        "id": "timeline-builder-missing-regression-tests",
        "concern": "Timeline data validation: The revised plan still leaves the highest-risk path, `patchRegistry()`, without automated regression coverage. The new pure-function tests cover `assembleTimelineData` and `buildDataFromCurrentRegistry`, but the duplicate-ID bug is explicitly expected to reproduce through the registry-patch flow, and that path still relies on manual smoke testing only.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      }
    ],
    "resolved_flags": [
      {
        "id": "timeline-builder-double-migration",
        "concern": "Timeline data migration: The plan does not actually achieve its stated \"migrate exactly once\" invariant on the async load path. `buildTimelineData()` already migrates before resolving, but the shared `resolveTimelineConfig()` helper migrates again internally, and the plan never updates that helper.",
        "resolution": "**Flag `timeline-builder-double-migration`:** Added `resolveTimelineConfig` in `config-utils.ts:82` as a fourth migration call site to be cleaned up in Step 2. The plan now enumerates all 4 internal migration calls (configToRows, resolveTimelineConfig, plus the 2 entry-point callers that are kept) in a table in the Overview. Step 2 now explicitly removes migration from both `configToRows` AND `resolveTimelineConfig`.\n\n**Flag `timeline-builder-not-canonical`:** Added an explicit \"Design boundary (DECISION-003)\" paragraph in the Overview explaining why `resolvedConfig` derivation remains caller-specific (sync/async split is inherent) and what the assembler does vs doesn't centralize. This is now a stated design choice, not an unstated gap.\n\n**Flag `timeline-builder-missing-regression-tests`:** Added Step 7 with 5 specific test cases for `assembleTimelineData` and `buildDataFromCurrentRegistry` in a new `timeline-save-utils.test.ts` file. These are pure function tests that cover: consistent output shape, duplicate track dedup, cascading dup-ID cleanup, registry preservation, and config migration. Updated success criteria to include the new tests."
      },
      {
        "id": "timeline-builder-not-canonical",
        "concern": "Timeline data assembly: The proposed `assembleTimelineData()` centralizes the outer `TimelineData` object literal, but it still leaves `resolvedConfig` and `assetMap` derivation split across multiple callers. That means the plan does not fully deliver on the stated goal of one canonical construction path that guarantees consistent tracks/clips/config by construction.",
        "resolution": "**Flag `timeline-builder-double-migration`:** Added `resolveTimelineConfig` in `config-utils.ts:82` as a fourth migration call site to be cleaned up in Step 2. The plan now enumerates all 4 internal migration calls (configToRows, resolveTimelineConfig, plus the 2 entry-point callers that are kept) in a table in the Overview. Step 2 now explicitly removes migration from both `configToRows` AND `resolveTimelineConfig`.\n\n**Flag `timeline-builder-not-canonical`:** Added an explicit \"Design boundary (DECISION-003)\" paragraph in the Overview explaining why `resolvedConfig` derivation remains caller-specific (sync/async split is inherent) and what the assembler does vs doesn't centralize. This is now a stated design choice, not an unstated gap.\n\n**Flag `timeline-builder-missing-regression-tests`:** Added Step 7 with 5 specific test cases for `assembleTimelineData` and `buildDataFromCurrentRegistry` in a new `timeline-save-utils.test.ts` file. These are pure function tests that cover: consistent output shape, duplicate track dedup, cascading dup-ID cleanup, registry preservation, and config migration. Updated success criteria to include the new tests."
      }
    ],
    "weighted_score": 1.5,
    "weighted_history": [
      4.25
    ],
    "plan_delta_from_previous": 40.5,
    "recurring_critiques": [],
    "scope_creep_flags": [],
    "loop_summary": "Iteration 2. Weighted score trajectory: 4.25 -> 1.5. Plan deltas: 40.5%. Recurring critiques: 0. Resolved flags: 2. Open significant flags: 1.",
    "debt_overlaps": [],
    "escalated_debt_subsystems": []
  }
}

        Settled decisions (verify the executor implemented these correctly):
- DECISION-001: A sync assembleTimelineData function is the canonical builder for TimelineData objects. (Accepted in iteration 1, unchanged in iteration 2. All flags accepted the core design.)
- DECISION-002: Test helpers may construct TimelineData manually without routing through the assembler. (Coupling tests to implementation makes them brittle. Production code is the enforcement boundary.)
- DECISION-003: resolvedConfig derivation remains caller-specific (async resolves URLs, sync reuses existing). (Inherent constraint of the sync/async split. Explicitly documented in the plan as a design boundary, not a gap.)
- DECISION-004: Migration is removed from both configToRows AND resolveTimelineConfig, leaving exactly one migration per entry-point caller. (Resolved the double-migration flag. All 4 call sites enumerated and accounted for in the plan table.)


        Execution summary:
        {
  "output": "Aggregated execute batches: completed 7/7.\nBatch 1: Implemented batch 1 task T1 by extracting `assembleTimelineData` in `src/tools/video-editor/lib/timeline-data.ts` and verified the new helper with a TypeScript compile.\nBatch 2: Implemented batch 2 task T2 by removing internal migration from `configToRows` and shared `resolveTimelineConfig`, after verifying the shared resolver is only called by `buildTimelineData`. TypeScript compile remains clean.\nBatch 3: Completed batch 3 task T3. The existing scoped video-editor test suite passed unchanged after the T2 migration removal: 9 test files, 31 tests, all passing.\nBatch 4: Completed batch 4 tasks T4-T6. All remaining production `TimelineData` construction paths in this batch now delegate to `assembleTimelineData`, `loadTimelineJsonFromProvider` was left unchanged, and the existing scoped video-editor test suite still passes: 9 files, 31 tests.\nBatch 5: Completed batch 5 task T7 by adding `src/tools/video-editor/lib/timeline-save-utils.test.ts` with 5 pure-function regression tests covering assembler output consistency, duplicate track deduplication, cascading clip-id cleanup, registry preservation, and config migration. TypeScript compile and the new targeted test file both pass.\nBatch 6: Executed batch 6 task T8. The requested verbose video-editor test suite passed cleanly: 4 files, 25 tests, 0 failures. `makeTimelineData()` in `useTimelineHistory.test.ts` was inspected and did not require updates. Checkpointed the batch result to `.megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_6.json`.\nBatch 7: Executed batch 7 task T9. Final validation passed: production full-shape `TimelineData` construction is centralized through `assembleTimelineData()` call sites in `timeline-data.ts`, `timeline-save-utils.ts`, and `useTimelineSave.ts`, with no alternate config/registry assembly paths found. Production `migrateToFlatTracks()` usage is limited to the intended entry points (`buildTimelineData`, `buildDataFromCurrentRegistry`, and the `patchRegistry` flow), with extra matches only in test coverage. Success criteria are met. Checkpointed the result to `.megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_7.json`.",
  "files_changed": [
    "src/tools/video-editor/lib/timeline-data.ts",
    "src/tools/video-editor/lib/config-utils.ts",
    "src/tools/video-editor/lib/timeline-save-utils.ts",
    "src/tools/video-editor/hooks/useTimelineSave.ts",
    "src/tools/video-editor/lib/timeline-save-utils.test.ts",
    ".megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_6.json",
    ".megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_7.json"
  ],
  "commands_run": [
    "rg -n \"type TimelineData|interface TimelineData|buildTimelineData|configToRows|getConfigSignature\" src/tools/video-editor/lib/timeline-data.ts",
    "sed -n '1,260p' src/tools/video-editor/lib/timeline-data.ts",
    "sed -n '260,460p' src/tools/video-editor/lib/timeline-data.ts",
    "sed -n '318,390p' src/tools/video-editor/lib/timeline-data.ts",
    "git diff -- src/tools/video-editor/lib/timeline-data.ts",
    "rg -n '\"packageManager\"|\"typecheck\"|\"tsc\"' package.json",
    "sed -n '1,140p' package.json",
    "npx tsc --noEmit",
    "test -w .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_1.json && echo writable || echo not-writable",
    "if [ -f .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_1.json ]; then sed -n '1,220p' .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_1.json; fi",
    "rg -n \"resolveTimelineConfig\\(\" src",
    "sed -n '1,220p' src/tools/video-editor/lib/config-utils.ts",
    "sed -n '140,230p' src/tools/video-editor/lib/timeline-data.ts",
    "git diff -- src/tools/video-editor/lib/timeline-data.ts src/tools/video-editor/lib/config-utils.ts",
    "sed -n '150,220p' src/tools/video-editor/lib/timeline-data.ts && sed -n '1,120p' src/tools/video-editor/lib/config-utils.ts",
    "test -w .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_2.json && echo writable || echo not-writable",
    "if [ -f .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_2.json ]; then sed -n '1,220p' .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_2.json; fi",
    "rg --files src/tools/video-editor | rg '\\.(test|spec)\\.(ts|tsx)$'",
    "git status --short",
    "npx vitest run --config config/testing/vitest.config.ts $(rg --files src/tools/video-editor | rg '\\.(test|spec)\\.(ts|tsx)$')",
    "test -w .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_3.json && echo writable || echo not-writable",
    "if [ -f .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_3.json ]; then sed -n '1,220p' .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_3.json; fi",
    "sed -n '340,440p' src/tools/video-editor/lib/timeline-data.ts",
    "sed -n '1,220p' src/tools/video-editor/lib/timeline-save-utils.ts",
    "sed -n '260,390p' src/tools/video-editor/hooks/useTimelineSave.ts",
    "sed -n '1,120p' src/tools/video-editor/hooks/useTimelineSave.ts",
    "rg -n \"configToRows|getConfigSignature|assembleTimelineData|buildDataFromCurrentRegistry|migrateToFlatTracks\" src/tools/video-editor/hooks/useTimelineSave.ts src/tools/video-editor/lib/timeline-save-utils.ts src/tools/video-editor/lib/timeline-data.ts",
    "git diff -- src/tools/video-editor/lib/timeline-data.ts src/tools/video-editor/lib/timeline-save-utils.ts src/tools/video-editor/hooks/useTimelineSave.ts",
    "test -w .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_4.json && echo writable || echo not-writable",
    "if [ -f .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_4.json ]; then sed -n '1,220p' .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_4.json; fi",
    "sed -n '1,220p' src/tools/video-editor/lib/serialize.test.ts",
    "sed -n '1,260p' src/tools/video-editor/lib/migrate.ts",
    "rg -n \"interface AssetRegistry|type AssetRegistry|interface ResolvedTimelineConfig|type ResolvedTimelineConfig|interface TimelineClip|type TimelineClip|interface TimelineConfig|type TimelineConfig|interface TrackDefinition|type TrackDefinition\" src/tools/video-editor/types src/tools/video-editor -g '*.ts'",
    "sed -n '1,260p' src/tools/video-editor/types/index.ts",
    "npx vitest run --config config/testing/vitest.config.ts src/tools/video-editor/lib/timeline-save-utils.test.ts",
    "test -w .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_5.json && echo writable || echo not-writable",
    "if [ -f .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_5.json ]; then sed -n '1,220p' .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_5.json; fi",
    "npx vitest run --config config/testing/vitest.config.ts --reporter=verbose src/tools/video-editor/hooks/useTimelineHistory.test.ts src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts src/tools/video-editor/lib/render-bounds.validation.test.ts src/tools/video-editor/lib/timeline-save-utils.test.ts",
    "rg -n \"makeTimelineData|TimelineData\" src/tools/video-editor/hooks/useTimelineHistory.test.ts",
    "sed -n '49,88p' src/tools/video-editor/hooks/useTimelineHistory.test.ts",
    "test -w .megaplan/plans/light-megaplan-consolidate-20260327-0022 && echo writable || echo not-writable",
    "ls -la .megaplan/plans/light-megaplan-consolidate-20260327-0022",
    "cat .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_5.json",
    "date -u +%Y-%m-%dT%H:%M:%SZ",
    "cat .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_6.json",
    "rg -n \"TimelineData|assembleTimelineData|signature:\\s|getConfigSignature\\(|clipOrder:\\s|configVersion:\\s\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'",
    "rg -n \"migrateToFlatTracks\\(\" src/tools/video-editor",
    "sed -n '110,145p' src/tools/video-editor/hooks/useTimelineSave.ts",
    "sed -n '430,470p' src/tools/video-editor/lib/timeline-data.ts",
    "rg -n \"as TimelineData|: TimelineData\\s*=|return \\{\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'",
    "rg -n \"signature:\\s\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'",
    "rg -n \"assembleTimelineData\\(\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'",
    "cat .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_7.json"
  ],
  "deviations": [
    "Advisory audit finding: Git status shows changed files not claimed by any task: .megaplan/debt.json, .megaplan/plans/light-megaplan-consolidate-20260327-0022",
    "Advisory audit finding: Sense check SC2 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC3 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC4 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC5 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC6 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC7 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC8 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .megaplan/debt.json, .megaplan/plans/light-megaplan-consolidate-20260327-0022",
    "Advisory audit finding: Sense check SC3 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC4 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC5 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC6 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC7 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC8 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory: done tasks rely on commands_run without files_changed (FLAG-006 softening): T3",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .megaplan/debt.json, .megaplan/plans/light-megaplan-consolidate-20260327-0022",
    "Advisory audit finding: Sense check SC4 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC5 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC6 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC7 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC8 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .megaplan/debt.json, .megaplan/plans/light-megaplan-consolidate-20260327-0022",
    "Advisory audit finding: Sense check SC7 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC8 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory quality: src/tools/video-editor/lib/timeline-save-utils.test.ts grew by 239 lines (threshold 200).",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .megaplan/debt.json, .megaplan/plans/light-megaplan-consolidate-20260327-0022",
    "Advisory audit finding: Sense check SC8 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory observation mismatch: executor claimed files not observed in git status/content hash delta: .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_6.json",
    "Advisory: done tasks rely on commands_run without files_changed (FLAG-006 softening): T8",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .megaplan/debt.json, .megaplan/plans/light-megaplan-consolidate-20260327-0022",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory observation mismatch: executor claimed files not observed in git status/content hash delta: .megaplan/plans/light-megaplan-consolidate-20260327-0022/execution_batch_7.json",
    "Advisory: done tasks rely on commands_run without files_changed (FLAG-006 softening): T9",
    "Advisory audit finding: Git status shows changed files not claimed by any task: .megaplan/debt.json, .megaplan/plans/light-megaplan-consolidate-20260327-0022"
  ],
  "task_updates": [
    {
      "task_id": "T1",
      "status": "done",
      "executor_notes": "Extracted exported sync `assembleTimelineData` helper in `timeline-data.ts`. It accepts the precomputed parts (`config`, `configVersion`, `registry`, `resolvedConfig`, `output`, `assetMap`), derives `rows`/`meta`/`effects`/`tracks`/`clipOrder` via `configToRows(config)`, and returns a complete `TimelineData` with `signature` computed from `getConfigSignature(resolvedConfig)`. Added JSDoc that the incoming config must already be migrated. Verified with `npx tsc --noEmit`.",
      "files_changed": [
        "src/tools/video-editor/lib/timeline-data.ts"
      ],
      "commands_run": [
        "npx tsc --noEmit"
      ]
    },
    {
      "task_id": "T2",
      "status": "done",
      "executor_notes": "Verified assumption #6 with a repo grep: `resolveTimelineConfig(` is only called from `buildTimelineData` in `timeline-data.ts`. Removed the internal `migrateToFlatTracks` call from `configToRows` and updated all former `migratedConfig` reads to `config`, while preserving the `getUniqueClipId` fallback unchanged as defense-in-depth. Removed the now-unused `migrateToFlatTracks` import and internal migration from `src/tools/video-editor/lib/config-utils.ts`, and updated the remaining references there to use `config` directly. Verified with `npx tsc --noEmit`.",
      "files_changed": [
        "src/tools/video-editor/lib/timeline-data.ts",
        "src/tools/video-editor/lib/config-utils.ts"
      ],
      "commands_run": [
        "rg -n \"resolveTimelineConfig\\(\" src",
        "npx tsc --noEmit"
      ]
    },
    {
      "task_id": "T3",
      "status": "done",
      "executor_notes": "Ran the existing `src/tools/video-editor` test suite with `npx vitest run --config config/testing/vitest.config.ts $(rg --files src/tools/video-editor | rg '\\.(test|spec)\\.(ts|tsx)$')`. All 9 existing video-editor test files passed without modification: 31 tests passed, 0 failed. This validates that the T2 migration removal did not introduce regressions in the current video-editor test surface.",
      "files_changed": [],
      "commands_run": [
        "npx vitest run --config config/testing/vitest.config.ts $(rg --files src/tools/video-editor | rg '\\.(test|spec)\\.(ts|tsx)$')"
      ]
    },
    {
      "task_id": "T4",
      "status": "done",
      "executor_notes": "Refactored `buildTimelineData` in `src/tools/video-editor/lib/timeline-data.ts` to migrate at the entry point, resolve URLs asynchronously via `resolveTimelineConfig`, and then delegate final `TimelineData` construction to `assembleTimelineData`. `loadTimelineJsonFromProvider` was inspected and left unchanged; it still delegates to `buildTimelineData`. Verified with `npx tsc --noEmit` and the existing scoped video-editor test suite (`9` files, `31` tests, all passing).",
      "files_changed": [
        "src/tools/video-editor/lib/timeline-data.ts"
      ],
      "commands_run": [
        "npx tsc --noEmit",
        "npx vitest run --config config/testing/vitest.config.ts $(rg --files src/tools/video-editor | rg '\\.(test|spec)\\.(ts|tsx)$')"
      ]
    },
    {
      "task_id": "T5",
      "status": "done",
      "executor_notes": "Refactored `buildDataFromCurrentRegistry` in `src/tools/video-editor/lib/timeline-save-utils.ts` to migrate once at entry, rebuild `resolvedConfig` from `current.resolvedConfig.registry`, reuse `current.registry` as the source registry, and delegate all `TimelineData` assembly to `assembleTimelineData`. The output shape stays centralized through the canonical builder. Verified with `npx tsc --noEmit` and the existing scoped video-editor test suite (`9` files, `31` tests, all passing).",
      "files_changed": [
        "src/tools/video-editor/lib/timeline-save-utils.ts"
      ],
      "commands_run": [
        "npx tsc --noEmit",
        "npx vitest run --config config/testing/vitest.config.ts $(rg --files src/tools/video-editor | rg '\\.(test|spec)\\.(ts|tsx)$')"
      ]
    },
    {
      "task_id": "T6",
      "status": "done",
      "executor_notes": "Refactored the `patchRegistry` path in `src/tools/video-editor/hooks/useTimelineSave.ts` to call `migrateToFlatTracks` explicitly at the entry point, rebuild `resolvedConfig.clips` from `migratedConfig.clips` using `nextResolvedRegistry` lookups, and delegate final object construction to `assembleTimelineData`. The manual `nextData.signature = ...` mutation was removed because signature now comes from the assembler. Verified with `npx tsc --noEmit` and the existing scoped video-editor test suite (`9` files, `31` tests, all passing), which covers the normal save/editor flows without exposing a regression from the fresh clip-assetEntry derivation.",
      "files_changed": [
        "src/tools/video-editor/hooks/useTimelineSave.ts"
      ],
      "commands_run": [
        "npx tsc --noEmit",
        "npx vitest run --config config/testing/vitest.config.ts $(rg --files src/tools/video-editor | rg '\\.(test|spec)\\.(ts|tsx)$')"
      ]
    },
    {
      "task_id": "T7",
      "status": "done",
      "executor_notes": "Added `src/tools/video-editor/lib/timeline-save-utils.test.ts` with 5 pure-function regression tests that cover: (1) `assembleTimelineData` output shape and signature correctness, (2) duplicate track-id deduplication through `migrateToFlatTracks` followed by `assembleTimelineData`, (3) cascading `-dup-` clip-id cleanup through migrate plus assemble, (4) `buildDataFromCurrentRegistry` preserving `current.registry` and `current.resolvedConfig.registry`, and (5) `buildDataFromCurrentRegistry` migrating duplicate-track configs before assembly. The file uses only local fixtures and pure helpers; it does not use `renderHook`, React, or DOM utilities. Verified with `npx tsc --noEmit` and `npx vitest run --config config/testing/vitest.config.ts src/tools/video-editor/lib/timeline-save-utils.test.ts` (5 tests passed).",
      "files_changed": [
        "src/tools/video-editor/lib/timeline-save-utils.test.ts"
      ],
      "commands_run": [
        "npx tsc --noEmit",
        "npx vitest run --config config/testing/vitest.config.ts src/tools/video-editor/lib/timeline-save-utils.test.ts"
      ]
    },
    {
      "task_id": "T8",
      "status": "done",
      "executor_notes": "Ran `npx vitest run --config config/testing/vitest.config.ts --reporter=verbose` against `useTimelineHistory.test.ts`, `useTimelineTrackManagement.test.ts`, `render-bounds.validation.test.ts`, and `timeline-save-utils.test.ts`. All 4 files passed with 25/25 tests green. Reviewed `makeTimelineData()` in `useTimelineHistory.test.ts`; its manual `TimelineData` fixture still matches the current shape and did not require updates.",
      "files_changed": [],
      "commands_run": [
        "npx vitest run --config config/testing/vitest.config.ts --reporter=verbose src/tools/video-editor/hooks/useTimelineHistory.test.ts src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts src/tools/video-editor/lib/render-bounds.validation.test.ts src/tools/video-editor/lib/timeline-save-utils.test.ts",
        "rg -n \"makeTimelineData|TimelineData\" src/tools/video-editor/hooks/useTimelineHistory.test.ts",
        "sed -n '49,88p' src/tools/video-editor/hooks/useTimelineHistory.test.ts"
      ]
    },
    {
      "task_id": "T9",
      "status": "done",
      "executor_notes": "Verified by grep that production full-shape `TimelineData` construction is centralized through `assembleTimelineData()` in exactly three caller paths: `buildTimelineData`, `buildDataFromCurrentRegistry`, and the `patchRegistry` flow. The only remaining production `TimelineData`-typed object literals are spread-based clones over existing data in `useTimelineSave.ts` and `preserveUploadingClips()`; they are not alternate construction paths from config/registry and do not bypass migration or deduplication. Verified by grep that `migrateToFlatTracks()` appears in production only at the intended entry points (`src/tools/video-editor/lib/timeline-data.ts`, `src/tools/video-editor/lib/timeline-save-utils.ts`, and `src/tools/video-editor/hooks/useTimelineSave.ts`), with the only extra matches in `timeline-save-utils.test.ts`. Success criteria are met.",
      "files_changed": [],
      "commands_run": [
        "rg -n \"TimelineData|assembleTimelineData|signature:\\s|getConfigSignature\\(|clipOrder:\\s|configVersion:\\s\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'",
        "rg -n \"migrateToFlatTracks\\(\" src/tools/video-editor",
        "sed -n '110,145p' src/tools/video-editor/hooks/useTimelineSave.ts",
        "sed -n '430,470p' src/tools/video-editor/lib/timeline-data.ts",
        "rg -n \"as TimelineData|: TimelineData\\s*=|return \\{\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'",
        "rg -n \"signature:\\s\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'",
        "rg -n \"assembleTimelineData\\(\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'"
      ]
    }
  ],
  "sense_check_acknowledgments": [
    {
      "sense_check_id": "SC1",
      "executor_note": "Confirmed `assembleTimelineData` returns all 12 `TimelineData` fields: `config`, `configVersion`, `registry`, `resolvedConfig`, `output`, `assetMap`, `rows`, `meta`, `effects`, `tracks`, `clipOrder`, and `signature`. The signature is computed from `resolvedConfig`, not `config`."
    },
    {
      "sense_check_id": "SC2",
      "executor_note": "Assumption #6 was verified by grep: `resolveTimelineConfig(` is only called by `buildTimelineData`. All `migratedConfig` references in both `configToRows` and shared `resolveTimelineConfig` were updated to `config`, and the unused `migrateToFlatTracks` import was removed from `config-utils.ts`."
    },
    {
      "sense_check_id": "SC3",
      "executor_note": "Yes. All existing video-editor tests passed without modification after the migration removal: 9 test files and 31 tests passed under the scoped `vitest` run."
    },
    {
      "sense_check_id": "SC4",
      "executor_note": "Yes. `buildTimelineData` now delegates to `assembleTimelineData` after the existing entry-point migration and async `resolveTimelineConfig` call. `loadTimelineJsonFromProvider` was not changed and still delegates to `buildTimelineData`. Compile and scoped video-editor tests passed unchanged."
    },
    {
      "sense_check_id": "SC5",
      "executor_note": "Yes. `buildDataFromCurrentRegistry` now reuses `current.registry` and `current.resolvedConfig.registry` rather than rebuilding those registries from scratch, while still rebuilding `resolvedConfig.clips` from the migrated config and returning the same `TimelineData` shape via `assembleTimelineData`."
    },
    {
      "sense_check_id": "SC6",
      "executor_note": "Yes. The manual `nextData.signature = ...` mutation was removed. `patchRegistry` now rebuilds `resolvedConfig.clips` from `nextConfig` after explicit migration, attaching asset entries from `nextResolvedRegistry`, which is equivalent to the old behavior for the normal case but avoids relying on stale `current.resolvedConfig.clips`. Compile and existing scoped video-editor tests passed after the change."
    },
    {
      "sense_check_id": "SC7",
      "executor_note": "Yes. The new test file contains 5 pure-function cases covering output shape consistency, duplicate track deduplication, cascading `-dup-` cleanup, registry preservation, and config migration. It uses no React, `renderHook`, or DOM dependencies, and the targeted run passed with 5/5 tests."
    },
    {
      "sense_check_id": "SC8",
      "executor_note": "Yes. The requested verbose video-editor test suite passed cleanly: 4 files and 25 tests green. `makeTimelineData()` in `useTimelineHistory.test.ts` was inspected after the run and did not require any updates."
    },
    {
      "sense_check_id": "SC9",
      "executor_note": "Yes. Grep confirms there are no alternate production full-shape `TimelineData` construction paths outside `assembleTimelineData()`; the only remaining `TimelineData`-typed literals are spread-based clones over existing data, not config/registry assembly. Grep also confirms `migrateToFlatTracks()` appears in production only at the intended entry points (`buildTimelineData`, `buildDataFromCurrentRegistry`, and the `patchRegistry` path), with extra matches only in test coverage."
    }
  ]
}

        Execution audit (`execution_audit.json`):
            {
  "findings": [
    "Git status shows changed files not claimed by any task: .megaplan/debt.json, .megaplan/plans/light-megaplan-consolidate-20260327-0022"
  ],
  "files_in_diff": [
    ".megaplan/debt.json",
    ".megaplan/plans/light-megaplan-consolidate-20260327-0022",
    "src/tools/video-editor/hooks/useTimelineSave.ts",
    "src/tools/video-editor/lib/config-utils.ts",
    "src/tools/video-editor/lib/timeline-data.ts",
    "src/tools/video-editor/lib/timeline-save-utils.test.ts",
    "src/tools/video-editor/lib/timeline-save-utils.ts"
  ],
  "files_claimed": [
    "src/tools/video-editor/hooks/useTimelineSave.ts",
    "src/tools/video-editor/lib/config-utils.ts",
    "src/tools/video-editor/lib/timeline-data.ts",
    "src/tools/video-editor/lib/timeline-save-utils.test.ts",
    "src/tools/video-editor/lib/timeline-save-utils.ts"
  ],
  "skipped": false,
  "reason": ""
}

        Git diff summary:
        M .megaplan/debt.json
 M src/tools/video-editor/hooks/useTimelineSave.ts
 M src/tools/video-editor/lib/config-utils.ts
 M src/tools/video-editor/lib/timeline-data.ts
 M src/tools/video-editor/lib/timeline-save-utils.ts
?? .megaplan/plans/light-megaplan-consolidate-20260327-0022/
?? src/tools/video-editor/lib/timeline-save-utils.test.ts

        Requirements:
        - Be critical.
        - Verify each success criterion explicitly.
        - Trust executor evidence by default. Dig deeper only where the git diff, `execution_audit.json`, or vague notes make the claim ambiguous.
        - The decisions listed above were settled at the gate stage. Verify that the executor implemented each settled decision correctly. Flag deviations from these decisions, but do not question the decisions themselves.
        - If actual implementation work is incomplete, set top-level `review_verdict` to `needs_rework` so the plan routes back to execute. Use `approved` only when the work itself checks out.
        - Cross-reference each task's `files_changed` and `commands_run` against the git diff and any audit findings.
        - Review every `sense_check` explicitly and treat perfunctory acknowledgments as a reason to dig deeper.
        - Follow this JSON shape exactly:
        ```json
        {
          "review_verdict": "approved",
          "criteria": [
            {
              "name": "Review cross-check completed",
              "pass": true,
              "evidence": "Executor evidence in finalize.json matches the diff and the audit file."
            }
          ],
          "issues": [],
          "summary": "Approved. The executor evidence is consistent and the remaining findings are advisory only.",
          "task_verdicts": [
            {
              "task_id": "T3",
              "reviewer_verdict": "Pass. Review prompt changes match the diff and reference the audit fallback correctly.",
              "evidence_files": ["megaplan/prompts.py"]
            }
          ],
          "sense_check_verdicts": [
            {
              "sense_check_id": "SC3",
              "verdict": "Confirmed. Both review prompts load execution_audit.json with a graceful fallback."
            }
          ]
        }
        ```
        - When the work needs another execute pass, keep the same shape and change only `review_verdict` to `needs_rework`; put the actionable gaps in `issues`, `summary`, and per-task verdicts.

> AGENT

{"review_verdict":"approved","criteria":[{"name":"Review cross-check completed","pass":true,"evidence":"The claimed product-code changes in finalize.json match the actual diff for src/tools/video-editor/lib/timeline-data.ts, src/tools/video-editor/lib/config-utils.ts, src/tools/video-editor/lib/timeline-save-utils.ts, src/tools/video-editor/hooks/useTimelineSave.ts, and src/tools/video-editor/lib/timeline-save-utils.test.ts. execution_audit.json only flags extra .megaplan artifacts, not missing implementation files."},{"name":"Success criterion: canonical TimelineData builder","pass":true,"evidence":"assembleTimelineData was added as the single full-shape constructor in src/tools/video-editor/lib/timeline-data.ts:342, and the three production construction paths now delegate to it from src/tools/video-editor/lib/timeline-data.ts:379, src/tools/video-editor/lib/timeline-save-utils.ts:35, and src/tools/video-editor/hooks/useTimelineSave.ts:332."},{"name":"Success criterion: no alternate production TimelineData object literal construction","pass":true,"evidence":"Repo grep and code inspection show no remaining production full-shape TimelineData literals outside assembleTimelineData. The remaining TimelineData-shaped spreads are clones over existing data in preserveUploadingClips at src/tools/video-editor/lib/timeline-data.ts:435 and in useTimelineSave materialization at src/tools/video-editor/hooks/useTimelineSave.ts:134, not independent config/registry assembly paths."},{"name":"Success criterion: migrateToFlatTracks called once per construction path","pass":true,"evidence":"configToRows no longer migrates at src/tools/video-editor/lib/timeline-data.ts:160, shared resolveTimelineConfig no longer migrates at src/tools/video-editor/lib/config-utils.ts:69, and production migrateToFlatTracks calls are limited to the three intended entry points: src/tools/video-editor/lib/timeline-data.ts:374, src/tools/video-editor/lib/timeline-save-utils.ts:23, and src/tools/video-editor/hooks/useTimelineSave.ts:329."},{"name":"Success criterion: existing video-editor tests pass","pass":true,"evidence":"No diff contradicts the executor's reported green runs for the existing video-editor suite in T3 and the targeted verbose suite in T8. This criterion is satisfied by trusted executor evidence rather than re-execution in review."},{"name":"Success criterion: new regression coverage added","pass":true,"evidence":"src/tools/video-editor/lib/timeline-save-utils.test.ts adds the requested pure-function coverage for assembler output consistency, duplicate track deduplication, cascading duplicate clip-id cleanup, registry preservation, and config migration."},{"name":"Success criterion: no duplicate-key React warnings on V3 timeline load","pass":true,"evidence":"This is satisfied by structural inference from the implemented path: buildTimelineData now migrates before assembly at src/tools/video-editor/lib/timeline-data.ts:374-386, and the new regression test in src/tools/video-editor/lib/timeline-save-utils.test.ts:105-137 verifies duplicate V3-style track IDs are deduplicated before rows/tracks/clipOrder are produced."},{"name":"Success criterion: no cascading -dup- clip ids after registry patches","pass":true,"evidence":"This is satisfied by structural inference from the implemented path: patchRegistry now migrates then assembles at src/tools/video-editor/hooks/useTimelineSave.ts:323-350, and the new regression test in src/tools/video-editor/lib/timeline-save-utils.test.ts:140-170 verifies migrate plus assemble removes cascading -dup- suffixes. Direct hook-level integration coverage is still absent, but the code path now routes through the canonical invariant."},{"name":"Settled decision DECISION-001 implemented","pass":true,"evidence":"A synchronous assembleTimelineData canonical builder exists and is exported from src/tools/video-editor/lib/timeline-data.ts:342."},{"name":"Settled decision DECISION-002 respected","pass":true,"evidence":"Manual TimelineData construction remains allowed in test-only helpers; no production enforcement was added against test mocks, and the existing helper in src/tools/video-editor/hooks/useTimelineHistory.test.ts was intentionally left alone per T8."},{"name":"Settled decision DECISION-003 respected","pass":true,"evidence":"resolvedConfig derivation remains caller-specific: async URL resolution still happens in buildTimelineData via resolveTimelineConfig at src/tools/video-editor/lib/timeline-data.ts:377, while sync callers rebuild resolvedConfig from current state in src/tools/video-editor/lib/timeline-save-utils.ts:25-33 and src/tools/video-editor/hooks/useTimelineSave.ts:336-345."},{"name":"Settled decision DECISION-004 implemented","pass":true,"evidence":"Migration was removed from both configToRows and the shared resolveTimelineConfig helper, leaving only entry-point migration calls in production code."}],"issues":[],"summary":"Approved. The implementation matches the approved plan and the settled design decisions: TimelineData construction is centralized through assembleTimelineData, helper-level double migration is removed, and the required regression tests were added. The only remaining gap is the already-known absence of a direct patchRegistry integration test, but the actual production code now routes that path through the same migrate-plus-assemble invariant that the new regression tests cover.","task_verdicts":[{"task_id":"T1","reviewer_verdict":"Pass. assembleTimelineData was added in timeline-data.ts and returns the full TimelineData shape with signature derived from resolvedConfig.","evidence_files":["src/tools/video-editor/lib/timeline-data.ts"]},{"task_id":"T2","reviewer_verdict":"Pass. Internal migration was removed from both configToRows and the shared resolveTimelineConfig helper, and the single-caller assumption for resolveTimelineConfig holds under repo grep.","evidence_files":["src/tools/video-editor/lib/timeline-data.ts","src/tools/video-editor/lib/config-utils.ts"]},{"task_id":"T3","reviewer_verdict":"Pass. No file changes were expected here; the executor's green existing-suite run is consistent with the diff and there is no contradictory evidence in the changed code.","evidence_files":["src/tools/video-editor/lib/timeline-data.ts","src/tools/video-editor/lib/config-utils.ts","finalize.json"]},{"task_id":"T4","reviewer_verdict":"Pass. buildTimelineData now migrates once, resolves URLs asynchronously, and delegates final assembly to assembleTimelineData. loadTimelineJsonFromProvider still delegates through buildTimelineData unchanged.","evidence_files":["src/tools/video-editor/lib/timeline-data.ts"]},{"task_id":"T5","reviewer_verdict":"Pass. buildDataFromCurrentRegistry now migrates once and delegates to assembleTimelineData while reusing current.registry and current.resolvedConfig.registry for the sync path.","evidence_files":["src/tools/video-editor/lib/timeline-save-utils.ts"]},{"task_id":"T6","reviewer_verdict":"Pass. patchRegistry now performs explicit entry-point migration, rebuilds resolvedConfig.clips from migratedConfig, delegates to assembleTimelineData, and removes the manual signature mutation. The known remaining gap is only missing direct hook-level integration coverage.","evidence_files":["src/tools/video-editor/hooks/useTimelineSave.ts"]},{"task_id":"T7","reviewer_verdict":"Pass. The new regression test file contains the five requested pure-function cases and directly exercises the new canonical builder behavior.","evidence_files":["src/tools/video-editor/lib/timeline-save-utils.test.ts"]},{"task_id":"T8","reviewer_verdict":"Pass. No source changes were required for this task; the executor's targeted verbose suite result is plausible against the final diff, and the useTimelineHistory helper was not changed.","evidence_files":["src/tools/video-editor/lib/timeline-save-utils.test.ts","src/tools/video-editor/hooks/useTimelineHistory.test.ts","finalize.json"]},{"task_id":"T9","reviewer_verdict":"Pass. Grep-level final validation is borne out by the code: production full-shape TimelineData assembly is centralized and production migrateToFlatTracks usage is limited to the intended entry points. The extra .megaplan diff noted by the audit is advisory and unrelated to the implementation files.","evidence_files":["src/tools/video-editor/lib/timeline-data.ts","src/tools/video-editor/lib/timeline-save-utils.ts","src/tools/video-editor/hooks/useTimelineSave.ts","execution_audit.json"]}],"sense_check_verdicts":[{"sense_check_id":"SC1","verdict":"Confirmed. assembleTimelineData in src/tools/video-editor/lib/timeline-data.ts:352-365 returns all 12 TimelineData fields, and signature is computed from resolvedConfig."},{"sense_check_id":"SC2","verdict":"Confirmed. resolveTimelineConfig now has no internal migration in src/tools/video-editor/lib/config-utils.ts:69-116, configToRows now uses config directly in src/tools/video-editor/lib/timeline-data.ts:160-206, and repo grep still shows only the buildTimelineData caller for resolveTimelineConfig."},{"sense_check_id":"SC3","verdict":"Accepted. I did not rerun the suite during review, but the executor's reported existing-suite pass is not contradicted by the observed diff."},{"sense_check_id":"SC4","verdict":"Confirmed. buildTimelineData now delegates to assembleTimelineData after entry-point migration and async resolution, and loadTimelineJsonFromProvider remains unchanged."},{"sense_check_id":"SC5","verdict":"Confirmed. buildDataFromCurrentRegistry reuses current.registry and current.resolvedConfig.registry and still returns the full TimelineData shape through assembleTimelineData."},{"sense_check_id":"SC6","verdict":"Confirmed with a residual coverage note. The manual signature mutation is gone, and patchRegistry now rebuilds resolvedConfig.clips from migratedConfig with fresh assetEntry lookup. Normal-case equivalence follows from the direct nextResolvedRegistry lookup, though there is still no dedicated hook integration test."},{"sense_check_id":"SC7","verdict":"Confirmed. timeline-save-utils.test.ts contains the five requested pure-function regression cases and does not pull in React or DOM helpers."},{"sense_check_id":"SC8","verdict":"Accepted. I did not rerun the verbose suite during review, but the executor's report is consistent with the final code and useTimelineHistory.test.ts needed no change."},{"sense_check_id":"SC9","verdict":"Confirmed. Current grep state matches the executor note: no alternate production full-shape TimelineData constructors remain, and production migrateToFlatTracks calls are restricted to the three entry points."}]}

> TOOL

tool_use update_plan
```json
{
  "explanation": "Reviewing the implementation against the approved plan and success criteria. I’ll cross-check the claimed tasks and sense checks against the actual diff, then produce a verdict with any gaps.",
  "plan": [
    {
      "step": "Inspect git diff and touched files for the TimelineData builder consolidation changes",
      "status": "in_progress"
    },
    {
      "step": "Cross-check each task and settled decision against code and audit artifacts",
      "status": "pending"
    },
    {
      "step": "Verify each success criterion and every sense check, then issue final review verdict",
      "status": "pending"
    }
  ]
}
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "git status --short",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "max_output_tokens": 1200
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
  "cmd": "git diff -- src/tools/video-editor/lib/timeline-data.ts src/tools/video-editor/lib/config-utils.ts src/tools/video-editor/lib/timeline-save-utils.ts src/tools/video-editor/hooks/useTimelineSave.ts src/tools/video-editor/lib/timeline-save-utils.test.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "sed -n '1,260p' src/tools/video-editor/lib/timeline-data.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "sed -n '1,260p' src/tools/video-editor/lib/config-utils.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "sed -n '1,220p' src/tools/video-editor/lib/timeline-save-utils.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "sed -n '1,420p' src/tools/video-editor/hooks/useTimelineSave.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "sed -n '1,260p' src/tools/video-editor/lib/timeline-save-utils.test.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "rg -n \"migrateToFlatTracks\\(\" src/tools/video-editor",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "rg -n \"assembleTimelineData\\(|: TimelineData\\s*=|as TimelineData|signature:\\s|getConfigSignature\\(|clipOrder:\\s|configVersion:\\s\" src/tools/video-editor -g '!**/*.test.ts' -g '!**/*.spec.ts'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "nl -ba src/tools/video-editor/lib/timeline-data.ts | sed -n '150,430p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "nl -ba src/tools/video-editor/lib/timeline-save-utils.ts | sed -n '1,220p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "nl -ba src/tools/video-editor/hooks/useTimelineSave.ts | sed -n '280,360p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "rg -n \"preserveUploadingClips|TimelineData\" src/tools/video-editor/lib/timeline-data.ts src/tools/video-editor/hooks/useTimelineSave.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "nl -ba src/tools/video-editor/lib/timeline-data.ts | sed -n '430,490p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "rg -n \"V3|duplicate key|dup-|migrateToFlatTracks|buildTimelineData\\(|loadTimelineJsonFromProvider\\(\" src/tools/video-editor -g '*.test.ts' -g '*.spec.ts'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "rg -n \"patchRegistry|useTimelineSave\" src/tools/video-editor -g '*.test.ts' -g '*.spec.ts'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "rg -n \"buildDataFromCurrentRegistry\\(|buildTimelineData\\(\" src/tools/video-editor",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "rg -n \"configToRows\\(\" src/tools/video-editor",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
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
  "cmd": "rg -n \"resolveTimelineConfig\\(\" src",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app",
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use update_plan
```json
{
  "explanation": "Diff, grep checks, and the added regression tests align with the executor’s report. I’ve verified the success criteria and settled decisions; the remaining gap is only the already-known absence of direct patchRegistry integration coverage, which does not contradict the implemented code path.",
  "plan": [
    {
      "step": "Inspect git diff and touched files for the TimelineData builder consolidation changes",
      "status": "completed"
    },
    {
      "step": "Cross-check each task and settled decision against code and audit artifacts",
      "status": "completed"
    },
    {
      "step": "Verify each success criterion and every sense check, then issue final review verdict",
      "status": "completed"
    }
  ]
}
```
