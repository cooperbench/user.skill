[DEVELOPER]: qa 529 531

[AGENT]: Both issues hit the Phase 0a short-circuit — the current HEAD matches the last `qa:completed` marker SHA for both, and no `--force`/`--no-cache` was passed. --- ## QA Review for Issue #529 ### Prior QA Still Valid QA already completed at commit `2e17ce21b920af702a1140537cb13526913eef22` on 2026-04-23T04:12:00Z — no changes since last run. Current HEAD (`2e17ce21b920af702a1140537cb13526913eef22`) matches the previously reviewed commit. **Prior Verdict:** NEEDS_VERIFICATION To force a full re-run, use: `/qa 529 --force` or `/qa 529 --no-cache` --- *QA short-circuited: prior run at same SHA is still valid* --- ## QA Review for Issue #531 ### Prior QA Still Valid QA already completed at commit `d45eee4f9d1f1c77aa97a5d7f304edac95f32875` on 2026-04-23T00:00:00Z — no changes since last run. Current HEAD (`d45eee4f9d1f1c77aa97a5d7f304edac95f32875`) matches the previously reviewed commit. **Prior Verdict:** NEEDS_VERIFICATION To force a full re-run, use: `/qa 531 --force` or `/qa 531 --no-cache` --- *QA short-circuited: prior run at same SHA is still valid* --- Both issues are on open PRs (#547 for 529, #546 for 531) with prior QA verdict `NEEDS_VERIFICATION`. Use `--force` if you want fresh runs, or resolve the pending verification items on the existing QA comments.

[DEVELOPER]: can you veerify?

[AGENT]: Running fresh QA with `--force` on both issues.

[AGENT]: Both branches are synced and 0 commits behind main. Let me gather the diff and AC details for both.

[AGENT]: Red flag on 531: `.claude/skills/docs/SKILL.md` changed 15 lines but `skills/docs/SKILL.md` and `templates/skills/docs/SKILL.md` each changed 157 lines. Let me dig into that.

[AGENT]: All three docs/SKILL.md files are identical at HEAD — the stat divergence is because they were in different states on main. Let me verify.

[AGENT]: Let me examine the actual changes for both issues.

[AGENT]: Both prior QAs were `NEEDS_VERIFICATION` solely due to in-progress CI builds — and CI has now completed cleanly on both PRs (8/8 SUCCESS each). I verified the ACs literally against the diffs; let me post the verdict upgrade as a follow-up comment.

[AGENT]: Verification complete. Both issues are `READY_FOR_MERGE`. **#529** (feat(qa): manual-test AC enforcement) — all 6 ACs MET, 8/8 CI green, 3-dir sync clean, CHANGELOG entry present. One non-blocking nit: case-sensitive awk at SKILL.md:1843 while its upstream grep is case-insensitive — noted for follow-up. **#531** (feat(docs-skill): infra/scaffold classifier) — all 4 ACs MET, 8/8 CI green, 3-dir sync fixed (docs/SKILL.md was diverged on main, now byte-identical at 458 lines), CHANGELOG entry present. Updated comments posted on both issues with verdict `READY_FOR_MERGE` and phase markers emitted. Added `ready-for-review` labels.

[DEVELOPER]: any gaps?

[AGENT]: Let me look adversarially for gaps that the structured QA pass may have missed.

[AGENT]: Yes — one real bug in #529, several scope-edge gaps in #531. **#529 — real bug in the detection filter (not caught by prior QA)** The jq filter in the SKILL.md snippet: ``` '[.comments[].body | select(contains("SEQUANT_PHASE") and contains("spec"))] | last' ``` On the #529 issue itself, this matches **5 different comments** (spec plan, NOT_FOUND QA, exec progress, QA review, QA re-verification) because every one of them contains both `SEQUANT_PHASE` and the word `spec`. `.last` returns the most recent QA comment — not the spec plan — so AC extraction runs against the wrong body. Real failure mode the moment the gate is invoked. Fix: anchor on the phase marker literal — `contains("\"phase\":\"spec\"")`. One-line change, same spot in the SKILL.md snippet, needs to land in all three skill dirs. Two smaller #529 nits (one already noted): - Awk on the line below the grep is case-sensitive while the grep is `-iE`. Mixed-case spec text is detected but its AC-ID won't be extracted. - Awk assumes `### AC-N` headers — /spec output does use this format today (verified in #529's own spec comment), so it works, but it's an undocumented coupling. **#531 — scope edges, not bugs** - `package\.json$` isn't start-anchored; matches […]

[DEVELOPER]: could it be fixed in this session?

[AGENT]: Yes. Here's the plan before I touch code: **Fix design** 1. Spec-comment filter in all three `qa/SKILL.md` copies: swap the two `contains()` substring checks for a single literal match on the phase-marker JSON. - Before: `contains("SEQUANT_PHASE") and contains("spec")` - After: `contains("\"phase\":\"spec\"")` 2. While in the same block, fix the already-noted awk case-sensitivity: add `BEGIN{IGNORECASE=1}` so the extractor matches the `-iE` grep above it. **Scope** - Three files: `.claude/skills/qa/SKILL.md`, `skills/qa/SKILL.md`, `templates/skills/qa/SKILL.md`. - No CHANGELOG entry — still under the unreleased #529 feature, which hasn't shipped. - New commit on top of the existing `feature/529-...` branch (no amend), push to origin, let CI run. PR #547 is still open so it auto-picks up. **Why a new commit, not amend** - PR #547 is already pushed; amending would require force-push and hit the no-force-push hook. Want me to go ahead?

[DEVELOPER]: yes

[AGENT]: Verify all three are identical and the old patterns are gone.

[AGENT]: Let me verify the new jq filter actually works against the real issue 529 comments before committing.

[AGENT]: Fixed filter matches exactly 1 comment (the spec plan) vs the old filter's 5. Now committing.

[AGENT]: Pushed `8c7642a` to `feature/529-...`. PR #547 auto-picks up the new commit; CI will re-run. **Summary** - Spec-comment jq filter swapped from two loose `contains()` checks to a literal `contains("\"phase\":\"spec\"")` match. Verified live against issue 529: old filter matched 5 comments, new filter matches 1 (the spec plan). - Awk got `BEGIN{IGNORECASE=1}` to match the `-iE` grep above it. - Same edit applied byte-for-byte to all three `qa/SKILL.md` copies; `diff -q` confirms sync. - New commit on top of `2e17ce2`, no amend, no force-push.

[DEVELOPER]: can you fix the 531 gaps?

[AGENT]: Yes. Brief plan before I touch code: 1. Infra classifier regex (line 152): add `cts|cjs|mts` to the config extension group, and add a `(ts|js)config\.json$` pattern for tsconfig/jsconfig. 2. Bullet description (lines ~130): mirror the same additions. 3. Remove the stale "User-Facing Documentation" bullet list — dead text now that the default fallback routes to developer-tool. 4. Skip the `package\.json$` non-anchor "gap" — matching subdir `package.json` in monorepos is actually desirable. 5. No CHANGELOG bump; still under the same unreleased #531 entry. 6. New commit on top of `d45eee4`, push to origin. PR #546 auto-picks it up. Proceeding.

[AGENT]: All three are byte-identical; I can apply the same edits to each.

[AGENT]: Verifying sync and that edits landed.

[AGENT]: All three files updated identically: - New regex extensions (`cts|cjs|mts`) and `(ts|js)config\.json$` at line 150 - `tsconfig.json`/`jsconfig.json` bullet at line 132 - Replaced stale "User-Facing Documentation" section with a single fall-through note at line 138 - `User-Facing Documentation` header is gone (0 matches in all three)

[AGENT]: Pushed `7128c44` to `feature/531-...`. PR #546 auto-picks up the new commit; CI will re-run. **Summary of 531 follow-up** - Regex: added `cts|cjs|mts` to config-extension group; added `(ts|js)config\.json$` for TypeScript/JavaScript project configs. - Description bullet: mirrored the new coverage. - Removed the stale "User-Facing Documentation" section header + bullets; replaced with a single fall-through note. - Skipped the `package\.json$` non-anchor "gap" — monorepo subdir matching is desirable. - 3-dir sync verified byte-identical; new commit on top of `d45eee4`, no amend.

[DEVELOPER]: any other gaps?

[AGENT]: Let me check a real /spec output to see what verification syntax it actually uses — that's the main thing I can still verify that could reveal a real detection gap in #529.

[AGENT]: Yes — one more real gap in #529 that I missed, caught by cross-referencing against actual /spec output from past issues. **#529 — awk header regex too narrow (real bug)** I sampled 11 past /spec outputs. Header styles in the wild: - `### AC-N` — used in #540, #534, #529, #452, #451 (current awk matches) - `#### AC-N` — used in #495, #490, #413, #393 (**awk does NOT match**) - `**AC-N:**` — used in #363 (**awk does NOT match**) The awk pattern `/^### AC-[0-9]+/` only matches 3-hash headers. On any spec using `####` or `**AC-N:**`, the grep correctly detects "Manual Test" but `ac` never gets set, so `manual_ac_ids` comes back empty — silent detection failure. Fix: broaden to `/^#+ AC-[0-9]+|^\*\*AC-[0-9]+/`. One-line change in the same block I already touched. **#531 — minor nit, not worth a commit** The "Developer Tool Documentation" bullet at line 125 says the category covers `src/commands/`, `bin/`, `src/mcp/` but not `scripts/` — even though the classifier matches `scripts/`. The word "scripts" appears in the description ("CLI commands, MCP tools, scripts") but not as a path. Purely cosmetic; the classifier works correctly. **Systemic (not per-PR)** Both PRs are prompt-only. The gates depend entirely on the /qa and […]

[DEVELOPER]: yes

[AGENT]: First, live test of the new awk pattern against real header styles before editing anything.

[AGENT]: All four header styles captured. Confirming the old pattern would have failed:

[AGENT]: Real-world test on #413's spec (uses `#### AC-N`): new pattern correctly extracts AC-1, AC-2, AC-4 — the three manual-test ACs in that spec. Old pattern would return empty. Applying the fix.

[AGENT]: Three files identical, new pattern at line 1843, zero occurrences of the old pattern. Committing.

[AGENT]: Pushed `07bbc77` to `feature/529-...`. PR #547 auto-picks up; CI will re-run. **Summary** - Awk header regex broadened from `/^### AC-[0-9]+/` to `/^(#+ AC-[0-9]+|\*\*AC-[0-9]+)/`, catching `### / #### / ##### / ## AC-N` and `**AC-N:**`. - Verified live against issue #413's spec (4-hash headers): new pattern extracts AC-1, AC-2, AC-4; old pattern returned empty. - Same edit to all three `qa/SKILL.md` copies; byte-identical sync confirmed. - New commit on top of `8c7642a`, no amend. Two follow-up commits on #529 now: `8c7642a` (filter + case-insensitivity) + `07bbc77` (header regex). One on #531: `7128c44` (classifier breadth + stale-section cleanup).

[DEVELOPER]: any other gaps?

[AGENT]: Yes — one more real one from the motivating example itself, plus a known-low-probability variant. Then diminishing returns. **#529 — `**Verify:**` prefix missing (real; matches the issue's motivating example)** Re-reading the issue body: > During QA of portfolio-2025 #28, AC-5 said verbatim: > > **Verify:** Try saving a Project without media, confirm validation error fires. That spec uses `**Verify:**` (not `**Verification:**`). The current grep catches this specific example only because "try ..., confirm" is also present — but a spec like `**Verify:** Open /foo and check the banner` has no comma/confirm pattern and slips through. Given the feature was motivated by `**Verify:**`-prefixed specs, it's worth adding explicit support. Fix: add `\*\*Verify:\*\*\s*` to the grep alternation group. One-line change, same three files. **#529 — "Browser Test" verification method (low probability, small fix)** /spec enumerates four methods: `Unit Test | Integration Test | Browser Test | Manual Test`. The existing `.tsx` browser-test gate (lines 1704+) covers the common case, but a non-`.tsx` change with `**Verification:** Browser Test` wouldn't trigger either gate. Rare in practice. Fix: add `Browser Test` to both grep and awk alternations. **Not worth fixing (diminishing returns)** - Awk cross-section attribution (e.g., "manual test" appearing in Implementation Notes after the […]