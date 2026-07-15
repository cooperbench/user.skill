[DEVELOPER]: Implement the following plan: # Plan: Carry forward dimension scores when --skip-slow omits detectors ## Context When `--skip-slow` is used, slow detector phases (duplication) don't run. Their potentials are 0, so the scoring engine omits the dimension entirely. The overall score is reweighted without it — producing a different number than a full scan. The user wants skipped dimensions to use their last known score instead. ## Approach In `_update_objective_health()` (the single place `state["dimension_scores"]` is written), save the previous dimension scores before overwriting, then carry forward any mechanical dimensions that were present before but are absent from the new computation. Mark them `"carried_forward": True`. Recompute overall/strict/objective scores from the augmented set. ## Changes ### 1. `desloppify/engine/state_internal/scoring.py` — `_update_objective_health()` **Before line 148** (where `state["dimension_scores"]` is assigned): - Save `prev_dim_scores = dict(state.get("dimension_scores", {}))` **After line 158** (after building `state["dimension_scores"]`): - Loop through `prev_dim_scores`. For each dim not in the new scores AND not subjective (check: no `"subjective_assessment"` key in `detectors`), copy it in with `"carried_forward": True`. **After line 160** (after the strict alias loop): - If any dims were carried forward, recompute the 4 scores: - `overall_score`: `compute_health_score(state["dimension_scores"])` — reads `score` key (lenient) - `strict_score`: build temp dict with `score` swapped to […]

[AGENT]: Now let me check the scoring module for `compute_health_score` and `compute_score_bundle` signatures.

[AGENT]: Let me check how the `not_scanned` flag flows through the scorecard projection.

[AGENT]: Now I have all the context I need. Let me implement the two changes. **Change 1: scoring.py** — carry forward missing mechanical dimensions from previous scan.

[AGENT]: **Change 2: scan_reporting_dimensions.py** — add `carried_forward` to entries and display with `⟲ prior scan` marker.

[AGENT]: Now add the display branch for carried-forward entries:

[AGENT]: Now let me run the tests to verify nothing is broken.

[AGENT]: All 2373 tests pass. Let me verify the changes look correct by reading the final state of both files.

[AGENT]: Both changes are in place and all tests pass. Here's a summary: **`desloppify/engine/state_internal/scoring.py`** (~20 lines added): - Saves `prev_dim_scores` before overwriting `state["dimension_scores"]` - After building new scores, loops through previous dimensions — any mechanical dimension missing from the new computation gets carried forward with `"carried_forward": True` - If any dims were carried forward, recomputes all 4 score channels (`overall`, `strict`, `objective`, `verified_strict`) from the augmented dimension set using `compute_health_score` - Otherwise uses the bundle values as before (no-op path) **`desloppify/app/commands/scan/scan_reporting_dimensions.py`** (~10 lines added): - Propagates `carried_forward` flag through `scorecard_dimension_entries()` - Adds a display branch that renders carried-forward dimensions normally (bar + score + strict) with a dim-colored `⟲ prior scan` suffix, instead of the `─── skipped ───` message

[DEVELOPER]: test it

[AGENT]: Good — full scan baseline is set. Duplication is at 96.5%. Now let me run with `--skip-slow`:

[AGENT]: Working as expected: - **Duplication** shows `96.5% (strict 96.5%) ⟲ prior scan` — carried forward from the full scan - **Overall score** stayed at `90.1` (was `90.1` in full scan) — consistent - **Objective score** is `94.2` vs `94.3` in full scan — the tiny difference is from Test health shifting slightly (`87.8% → 87.5%` due to 1 extra test coverage finding), not from duplication being dropped - The `⟲ prior scan` marker is visible and dim-colored next to the Duplication row

[DEVELOPER]: is thisapproach ebatufiully structured?

[AGENT]: Honestly, no. A couple things bother me: **1. Two score-computation paths.** The normal case uses `bundle.*` and the carry-forward case manually calls `compute_health_score` four times with hand-built dicts. That's fragile — if the bundle logic evolves, these diverge silently. **2. Duplicated display formatting.** The `carried_forward` branch in the display code copy-pastes the bar+score+strict line from the normal branch, just with a different suffix. **3. Presentation flag in engine data.** `"carried_forward": True` lives inside `state["dimension_scores"]` — that's UI concern leaking into the scoring engine's data structure. A cleaner version would: - Do the carry-forward **before** `compute_score_bundle`, by injecting synthetic potentials for the missing dimensions, so there's one scoring path - Or, simpler: just do the carry-forward + recompute, but extract the suffix logic in the display so there's no duplicated formatting Want me to clean up option 2 (the quick win — eliminate the duplicated display line and move the flag to a less intrusive spot)? Or option 1 (the deeper refactor — make it invisible to the scoring engine)?