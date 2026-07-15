> DEVELOPER

$cleanup-loose-branches

> AGENT

Using `cleanup-loose-branches` for a read-only survey first. I’ll gather worktrees, branches, PR state, stashes, and current checkout status, then stop with recommendations rather than deleting anything.

> AGENT

The current checkout is clean and there’s only one registered worktree so far. I’m fetching/pruning refs now and checking the side locations where this repo’s tooling may leave worktrees.

> AGENT

`origin/HEAD` is not set in this clone, so I’ll infer the default branch from local/remotes before classifying. I found one sibling `.megaplan-worktrees` path outside this repo; I’ll verify whether it belongs to this repository or only to that sibling project.

> AGENT

This repo has four non-main local branches, all with matching remote branches. There are no stashes in this repository, and that sibling worktree belongs to `banodoco-workspace`, so I’m excluding it from this survey.

> AGENT

None of the four loose branch names currently match an open or merged PR head. The branches are recent and still have unique patches versus `main`; I’m doing the cheap per-branch diff/log checks now so the recommendations are more than just age-based.

> AGENT

Three branches would merge cleanly by `merge-tree`; `per-milestone-robustness-20260503` has conflicts and also looks related to merged PR #28 under a different head branch. I’m checking whether its commits were recovered under different SHAs before I recommend keeping or deleting it.

> AGENT

One new local commit appeared on the current branch while I was surveying: `a84c6480 Make Railway cloud commands non-interactive`. I’ll refresh the current-branch metrics so the table reflects the live repo state and won’t touch or overwrite that work.

> AGENT

Read-only survey complete. I did not delete anything. ``` REC WHERE BRANCH AHEAD/BEHIND AGE PR REASON inspect local+remote megaplan/per-milestone-rob... 6/61 10d related #28✓ PR #28 recovered 5 fixes under another branch, but this branch still has 6 cherry-unique commits, 8 merge-tree conflict markers, and local is 5 ahead of its remote keep local+remote megaplan/cloud-runtime-corr... 4/0 now none current checkout, clean, very recent work, merge-tree clean; keep and PR when ready keep local+remote sandbox-fingerprint 1/2 34h none recent unique patch, merge-tree clean; keep and PR or merge deliberately keep local+remote tiebreaker-tests 2/2 34h none recent test-recovery work, merge-tree clean; keep and PR or merge deliberately ``` **Stashes** None. **Prunable Worktrees** None registered for this repo. One sibling `.megaplan-worktrees` path exists under `banodoco-workspace`, but it belongs to that repo, not this one. **Current Checkout** Clean. Current branch is `megaplan/cloud-runtime-correctness-sprint`. **Other Notes** `git fsck --unreachable --no-reflogs` reports 136 unreachable commits. I did not enumerate them in the cleanup table; they are reflog/orphan recovery material, not branch refs. **Counts** `0` delete-able / `1` inspect / `3` keep / `0` stashes / `0` prunable worktrees. Want to walk through these one at a time? I’ll describe each, give my rec and reasoning, and you decide.