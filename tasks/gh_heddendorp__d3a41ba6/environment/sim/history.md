[SYSTEM]: # AGENTS.md instructions for /Users/hedde/code/evorto <INSTRUCTIONS> # Repository Guidelines ## Context Discipline - Keep repository knowledge in small, relevant files. - Use this file as the map, not the full manual. - Read the nearest applicable guidance before editing: - root product/system context - module-level `AGENTS.md` - local README files - Update context files when reality changes, assumptions are invalidated, or new constraints are discovered. - Prefer small, accurate updates over large stale manuals. ## Root Context Files - `PRODUCT.md` - product goals, personas, core workflows, domain concepts, and product invariants. - `ARCHITECTURE.md` - high-level system shape, architectural boundaries, and where to look first for common changes. - `QUALITY.md` - behavior-focused verification guidance, Browser/Playwright expectations, and done criteria. Keep these files concise. Put implementation-specific guidance in the nearest module-level `AGENTS.md` or README. ## Project Structure - App code: `src/app/**` - Server runtime and APIs: `src/server/**` - Data layer: `src/db/**` - Shared contracts/types/utilities: `src/shared/**` and `src/types/**` - Unit tests: `*.spec.ts` in `src/**` - Playwright tests: `tests/**` - Legacy e2e reference: `e2e/**` - Assets/public: `public/` - Theming: `src/styles.scss` and `_theme-colors.scss` Start with the nearest applicable module guidance: - `src/app/AGENTS.md` - `src/server/AGENTS.md` - `src/db/AGENTS.md` - `tests/AGENTS.md` More specific guidance may exist deeper in […]

[DEVELOPER]: Update the branch from remote

[AGENT]: I’ll refresh the local repo state and check the current branch/upstream before changing anything, then use the repo’s existing branch-management convention where it fits.

[AGENT]: The checkout is on `main`, currently clean and reported as 2 commits behind `origin/main`. I’m checking whether there is any closer local guidance before fast-forwarding it.

[AGENT]: There are no local modifications to protect, and this is `main`, so the right operation is a straight remote refresh plus fast-forward merge. I’m going to fetch first, then update only if it remains a clean fast-forward.

[AGENT]: Fetch completed cleanly. I’m checking the exact ahead/behind relationship before applying the fast-forward.

[AGENT]: `main` has no local-only commits and is exactly two commits behind `origin/main`, so this is safe to fast-forward.

[AGENT]: The fast-forward succeeded to `origin/main`. I’m doing a final status check so I can report the exact new commit and whether the working tree stayed clean.

[AGENT]: Updated `/Users/hedde/code/evorto` from remote. `main` fast-forwarded from `c1edf30384f` to `70215b09fb2`, bringing in 2 commits from `origin/main`. Final status is clean and aligned with remote: `HEAD...origin/main` is `0 0`. No tests were run since this was only a branch update. <oai-mem-citation> <citation_entries> MEMORY.md:116-116|note=[checked prior evorto branch sync context] MEMORY.md:139-147|note=[confirmed rebase guidance was for stacked PRs not main fast-forward] </citation_entries> <rollout_ids> </rollout_ids> </oai-mem-citation>