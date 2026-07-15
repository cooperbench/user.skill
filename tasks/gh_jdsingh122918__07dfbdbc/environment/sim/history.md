[DEVELOPER]: Lets fix the gh pipeline

[AGENT]: Let me check the current CI pipeline status and configuration.

[AGENT]: The CI has been failing consistently. Let me check the latest failure details.

[AGENT]: 11 clippy errors in the lint job. Let me read all the affected files and fix them.

[AGENT]: Now let me also check the `verdict_name` function signature and the `generate_diff` signature to understand the types.

[AGENT]: Good — `generate_diff` already takes `&Path`, and `verdict_name` takes `&ReviewVerdict`. Now let me also check `apply_patch` signature.

[AGENT]: All the callers already accept `&Path`. Now let me apply all the fixes.

[AGENT]: Now fix the `useless_concat` issues in worker.rs — replace `concat!()` with the raw string directly.

[AGENT]: Now I need to check if `engine.rs` needs a `use std::path::Path` import (it already has `PathBuf` but may need `Path`).

[AGENT]: Need to add `Path` to the main import.

[AGENT]: Now also check if `verdict_name` takes by value or reference — the fix changed `&winner.verdict` to `winner.verdict`, so we need to verify `ReviewVerdict` is `Copy`.

[AGENT]: Now let me run clippy locally to verify all fixes.

[AGENT]: There are additional errors beyond what CI caught. Let me see the full output.

[AGENT]: Lots of dead code in the autoresearch module plus one logic issue. Let me check the autoresearch files.

[AGENT]: These are all dead code issues in the autoresearch module (stub executors from recent commit). The simplest fix is to allow dead code on these since they're stubs intended for future use. Let me read the files.

[AGENT]: The autoresearch module has dead code (stub executors) and one logic bug. Let me check the module structure to find the best place to add `#[allow(dead_code)]`.

[AGENT]: Now fix the remaining issues. Add `#[allow(dead_code)]` for budget and scorer modules, and fix the experiment.rs logic.

[AGENT]: Now fix the `if_same_then_else` issue in experiment.rs.

[AGENT]: Now let me also check if the `git_ops` module has a `head_sha` method that's unused.

[AGENT]: `head_sha` is a trait method — the dead code warning was about a struct method. Let me re-check which exact dead code warnings are left. Let me run clippy again.

[AGENT]: One error left — `head_sha` is never used. Let me find where it's defined.

[AGENT]: The `head_sha` trait method isn't called anywhere in the crate. I'll prefix it with `_` or add an allow. Since it's a trait method intended for future use, let me just add `#[allow(dead_code)]` on the trait.

[AGENT]: Clippy passes clean. Let me also run tests to make sure nothing is broken.

[AGENT]: All tests pass. Let me also verify formatting is clean.

[AGENT]: Now let me do a final verification — clippy, fmt, and tests all pass.

[AGENT]: All clean. Here's a summary of the fixes: **Clippy fixes (11 errors):** 1. **`council/chairman.rs:222`** — Removed needless borrow (`&winner.verdict` → `winner.verdict`) 2. **`council/engine.rs:217,236`** — Changed `&PathBuf` params to `&Path` (added `Path` import) 3. **`council/merge.rs:415`** — Collapsed nested `if` into single condition with `&& let` 4. **`update_check.rs:162`** — Collapsed nested `if let` + `if` into single `if let && ...` 5. **`council/config.rs:364,398,414`** — Used struct literal with `..Default::default()` instead of field reassignment 6. **`council/worker.rs:1449,1630,1648`** — Removed useless `concat!()` wrappers around single string literals **Dead code fixes (autoresearch stubs):** 7. **`autoresearch/mod.rs`** — Added `#[allow(dead_code)]` on `budget` and `scorer` modules 8. **`autoresearch/loop_runner.rs`** — Added `#[allow(dead_code)]` on `LoopGitOps` trait 9. **`autoresearch/experiment.rs:152`** — Refactored identical `if` branches into inverted condition Want me to commit and push this?