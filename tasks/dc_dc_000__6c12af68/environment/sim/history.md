[DEVELOPER]: $cleanup-loose-branches

[AGENT]: Using `cleanup-loose-branches` for a read-only survey first. I’ll gather worktrees, branches, PR state, stashes, and current checkout status, then stop with recommendations rather than deleting anything.

[AGENT]: The current checkout is clean and there’s only one registered worktree so far. I’m fetching/pruning refs now and checking the side locations where this repo’s tooling may leave worktrees.

[AGENT]: `origin/HEAD` is not set in this clone, so I’ll infer the default branch from local/remotes before classifying. I found one sibling `.megaplan-worktrees` path outside this repo; I’ll verify whether it belongs to this repository or only to that sibling project.

[AGENT]: This repo has four non-main local branches, all with matching remote branches. There are no stashes in this repository, and that sibling worktree belongs to `banodoco-workspace`, so I’m excluding it from this survey.

[AGENT]: None of the four loose branch names currently match an open or merged PR head. The branches are recent and still have unique patches versus `main`; I’m doing the cheap per-branch diff/log checks now so the recommendations are more than just age-based.

[AGENT]: Three branches would merge cleanly by `merge-tree`; `per-milestone-robustness-20260503` has conflicts and also looks related to merged PR #28 under a different head branch. I’m checking whether its commits were recovered under different SHAs before I recommend keeping or deleting it.

[AGENT]: One new local commit appeared on the current branch while I was surveying: `a84c6480 Make Railway cloud commands non-interactive`. I’ll refresh the current-branch metrics so the table reflects the live repo state and won’t touch or overwrite that work.

[AGENT]: Read-only survey complete. I did not delete anything. ``` REC WHERE BRANCH AHEAD/BEHIND AGE PR REASON inspect local+remote megaplan/per-milestone-rob... 6/61 10d related #28✓ PR #28 recovered 5 fixes under another branch, but this branch still has 6 cherry-unique commits, 8 merge-tree conflict markers, and local is 5 ahead of its remote keep local+remote megaplan/cloud-runtime-corr... 4/0 now none current checkout, clean, very recent work, merge-tree clean; keep and PR when ready keep local+remote sandbox-fingerprint 1/2 34h none recent unique patch, merge-tree clean; keep and PR or merge deliberately keep local+remote tiebreaker-tests 2/2 34h none recent test-recovery work, merge-tree clean; keep and PR or merge deliberately ``` **Stashes** None. **Prunable Worktrees** None registered for this repo. One sibling `.megaplan-worktrees` path exists under `banodoco-workspace`, but it belongs to that repo, not this one. **Current Checkout** Clean. Current branch is `megaplan/cloud-runtime-correctness-sprint`. **Other Notes** `git fsck --unreachable --no-reflogs` reports 136 unreachable commits. I did not enumerate them in the cleanup table; they are reflog/orphan recovery material, not branch refs. **Counts** `0` delete-able / `1` inspect / `3` keep / `0` stashes / `0` prunable worktrees. Want to walk through these one at a time? I’ll describe each, give my rec and reasoning, and you decide.

[DEVELOPER]: nothing we should implement?

[AGENT]: I’ll answer from the branch contents rather than the cleanup bucket labels. The only ambiguous case is the old per-milestone branch, so I’m checking whether it still contains a real missing feature or just pre-recovery history.

[AGENT]: Correct: I don’t see an old loose branch that we should now implement from scratch. My read: - `megaplan/per-milestone-robustness-20260503`: do **not** implement. PR #28 already recovered the important fixes into `main`, and `main` now has the relevant per-milestone robustness code. The old branch is conflicty and stale; I’d delete it after one final diff sanity check. - `megaplan/cloud-runtime-correctness-sprint`: this is active work, already implemented on the current branch. Next step is review/test/PR, not reimplementation. - `sandbox-fingerprint`: small recent feature branch. Worth keeping until you decide whether to PR/merge it. - `tiebreaker-tests`: recent test-recovery branch. Worth keeping until you decide whether to PR/merge it. So: no hidden abandoned “we need to implement this” item. The only real work is deciding whether the three recent branches should become PRs, and cleaning up the old per-milestone branch.

[DEVELOPER]: so there's no branches on github, or pRs or anything that we should keep?

[AGENT]: I’ll verify GitHub state directly now: remote branches plus open/recent PRs. That will separate “local branches worth keeping” from “GitHub refs/PRs that need preservation.”

[AGENT]: There **are** GitHub branches, but there are **no open PRs**. Remote branches currently on GitHub: - `origin/megaplan/cloud-runtime-correctness-sprint` — **keep**. This is active/current work. - `origin/sandbox-fingerprint` — **keep for now** unless you decide not to merge it. - `origin/tiebreaker-tests` — **keep for now** unless you decide not to merge it. - `origin/megaplan/per-milestone-robustness-20260503` — **do not keep**. This looks superseded by merged PR #28 and is the cleanup candidate. PRs: `gh pr list --state open` returned `[]`, so there are no open/draft PRs needing preservation. The recent PRs are merged or closed records; nothing to “keep” there beyond normal GitHub history.

[DEVELOPER]: The question is wheterh we should merge or not - ist hat not clear from the $cleanup-loose-branches skill?

[AGENT]: You’re right. I treated `keep` as “don’t delete” and failed to turn it into the stronger branch-hygiene decision the skill calls for: merge, delete, or rebase-and-PR. I’m tightening that now branch by branch.