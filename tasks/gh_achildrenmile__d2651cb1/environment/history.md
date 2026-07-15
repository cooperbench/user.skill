> DEVELOPER

check the bundesland bezirksauswertungskarte. wien has in it white lines. remove that. https://github.com/achildrenmile/bosarsalog/issues/15

> AGENT

Let me look at the issue and the relevant code.

> AGENT

The issue has 3 parts: 1. Remove white lines (internal district borders) within Wien 2. Hide download button when printing 3. Make footer smaller when printing Let me look at the relevant files.

> AGENT

Now let me see the Wien Bundesland border path and find where the download button and footer are rendered.

> AGENT

Let me get the Wien Bundesland border path to use as a replacement.

> AGENT

Now let me check the Layout.tsx footer.

> AGENT

Let me check for all download buttons across both pages.

> AGENT

Good. Now I have all the information. Let me make all 3 fixes: 1. **Wien white lines** - Replace Wien's multi-ring path with the single outer boundary 2. **Hide download buttons when printing** - Add `@media print` CSS 3. **Smaller footer when printing** - Add `@media print` CSS

> AGENT

Now add the print CSS and update the generation script.

> AGENT

Now update the generation script to use the Bundesland outer boundary for Wien instead of merging all sub-district rings.

> AGENT

Actually, `allOuterRings` still contains 23 separate outer rings for Wien's sub-districts. The correct fix in the generation script is to use the Bundesland boundary. Let me fix this properly.

> AGENT

Now add the proper fix — after the BL borders are computed, replace Wien's path with the BL boundary.

> AGENT

Wait — the entries are already written to `lines` before the BL section. I need to move this fix before the TS output generation. Let me check the script flow.

> AGENT

Right — the BL entries are computed *after* the BEZIRK_PATHS are already written to `lines`. I need to restructure so the BL data is fetched first, then Wien's entry is fixed, then both are written. Let me move the BL processing before the TS output.

> AGENT

Now let me verify the build works.

> AGENT

Clean build. Let me verify the final state of all changed files.

> AGENT

Everything looks good. Here's a summary of the 3 changes for issue #15: **1. Wien white lines removed** (`client/src/data/bezirkPaths.ts`): - Replaced Wien's multi-ring SVG path (23 separate rings for 23 sub-districts) with the single Bundesland outer boundary path. The internal district boundaries no longer show as white lines. **2. Download buttons hidden when printing** (`client/src/index.css`): - Added `@media print` rule that hides all elements with `data-no-export="true"` — this covers all download buttons on both ReportsPage and AggregatedReportsPage. **3. Footer smaller when printing** (`client/src/index.css`): - Added `@media print` rule that reduces footer padding and font size. **4. Generation script updated** (`scripts/generate-bezirk-paths.mjs`): - Moved Bundesland border processing before BEZIRK_PATHS output, so Wien's path is replaced with the BL outer boundary before writing. This ensures re-running the script won't reintroduce the white lines.