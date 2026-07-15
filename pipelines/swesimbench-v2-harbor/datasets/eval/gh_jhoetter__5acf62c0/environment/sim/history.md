[DEVELOPER]: Repository: /Users/jhoetter/repos/bim-ai. Start from current pushed main. Wave 26-D ownership: BIR-N10 final-package readiness. You are not alone in the codebase; do not revert others' edits, avoid unrelated dirty files, and accommodate concurrent changes. Do not ask the user about removals; record cleanup candidates in spec/bim-integrity-removal-followups.md if needed and keep moving. Goal: once K02/K04/K07 are done or locally reflected, make target-house final package readiness pass from committed evidence. If other workers are not done, prepare readiness automation and exact blockers without waiting on user. Update tracker/status/evidence. Run final-package tests and tracker audit. Commit locally, do not push. Final response: commit hash, final-package status, files, tests, blockers if any.

[AGENT]: I’ll inspect the current branch, local dirt, and the tracker/spec layout first so I can separate existing work from the BIR-N10 changes I make. After that I’ll wire readiness against the committed evidence and only touch the narrow status/evidence files needed.

[AGENT]: The worktree is already dirty with unrelated app/package changes and target-house evidence edits, so I’ll avoid sweeping operations. I’m going to fetch `origin/main` and compare it to local `main`; if local main is behind, I’ll use that as a blocker rather than merging over concurrent edits.

[AGENT]: Fetch completed cleanly and local `main` is still aligned with `origin/main`; the remaining changes are local worktree edits. I’m reading the BIR tracker rows and final-package code paths now to see whether K02/K04/K07 are already represented or still need blocker reporting.

[AGENT]: The committed tracker currently has exactly four incomplete rows: `BIR-K02`, `BIR-K04`, `BIR-K07`, and `BIR-N10`. Since no W26-A/B/C completion is present locally, I’m going to make the final package report those upstream exchange blockers explicitly and keep `BIR-N10` blocked rather than pretending readiness passed.

[AGENT]: The current final-package gates are green for evidence, performance, clean-pass, geometry, methodology, rehearsal, and live responsiveness. The only failure is tracker completion, but the manifest does not yet isolate `BIR-K02/K04/K07` as upstream exchange blockers for W26-D, so I’m going to add that dependency summary and update the tracker/status text accordingly.

[AGENT]: I’m going to edit the final-package script and its tests now. The change is scoped to making `BIR-K02/K04/K07` first-class final-package dependencies, so a W26-D run shows the exact upstream rows that still prevent `--require-ready`.

[AGENT]: The code now exposes upstream exchange dependencies. I’m updating the tracker language so W26-D’s status says exactly why `BIR-N10` is still Partial when W26-A/B/C have not landed.

[AGENT]: I’m regenerating the tracker status from the edited tracker, then I’ll run the focused final-package tests and the readiness command. I’ll use an output directory outside the repo for the readiness command so the run does not leave new untracked package artifacts in the worktree.