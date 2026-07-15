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

[DEVELOPER]: if not, please improve that

[AGENT]: I’ll improve the skill itself so future surveys answer “merge vs delete vs keep” explicitly. The change should make `keep` mean “preserve because it’s active/protected,” not a vague substitute for deciding whether branch work should land.

[AGENT]: I’m editing the skill to add a “landing decision” pass, replace the vague recent-work `keep` default with `rebase-and-PR` / `merge-then-delete` where appropriate, and make the survey table show that decision directly.

[AGENT]: The first patch missed exact wording in one section, so I’m applying this in smaller chunks against the current file.

[DEVELOPER]: is it now clear and to the point? is the decision making rubric obvious? Is it action oriented? The goal is to get everything onto main or ditch it

[AGENT]: I’ll do one pass as an editor now, against that exact goal: every branch should end as landed on `main`, deliberately parked, or ditched. If the text still leaves room for passive “keep,” I’ll tighten it.

[AGENT]: The new classification section is much better, but the walk-through and reporting sections still contain old `inspect` language. I’m removing that so the end state is unmistakably “land it or drop it, with explicit parked exceptions.”

[AGENT]: There are a couple of leftover old terms in stash cross-reference and an abbreviated table label. I’m cleaning those so the vocabulary stays consistent.

[AGENT]: Yes, it’s now clear and action-oriented. I updated [SKILL.md](/Users/user_c042661f/Documents/poms_skills/cleanup-loose-branches/SKILL.md:16) so the core goal is explicit: **get every loose piece of work onto `main` or ditch it**. The rubric now requires one of these outcomes per branch: `delete`, `merge-then-delete`, `rebase-and-PR`, `cherry-pick-then-delete`, or `keep`. I also tightened `keep`: it now means genuinely parked/protected/active/open-PR work, not “this branch has recent commits.” Recent valuable branches without PRs should now be classified as either direct merge candidates or PR-needed candidates. The old “inspect” escape hatch is mostly removed from final recommendations. It can only appear as internal investigation language; if the agent genuinely cannot decide, it must say `uncertain` and name the blocker.

[DEVELOPER]: now run it again

[AGENT]: Running the updated survey now. This pass will classify each loose branch as land, PR, cherry-pick, park, or delete, instead of treating “keep” as the default for recent work.

[AGENT]: The checkout is clean, no stashes, and the only registered worktree is the current branch. I’m now computing branch-specific ahead/behind, cherry uniqueness, conflict counts, and diff shape for each loose local/remote branch.

[AGENT]: The landing shape is: one large active cloud branch, two clean smaller branches, and one stale/conflicted branch. I’m checking same-file history and commit subjects now so the recommendations say whether to merge, PR, or drop.

[AGENT]: I’ve got enough signal for the updated table: the old per-milestone branch is superseded by merged/recovered history, the cloud branch is large and PR-worthy, sandbox is a small merge candidate, and tiebreaker is test-heavy enough to send through PR/CI.

[AGENT]: Read-only survey rerun with the updated rubric. I did not change refs. ``` REC WHERE BRANCH AHEAD/BEHIND AGE PR REASON delete local+remote megaplan/per-milestone-rob... 6/61 10d #28 ✓ superseded by PR #28 + newer main history; 8 conflict markers; do not merge merge-then-delete local+remote sandbox-fingerprint 1/2 35h none small valuable runtime-safety patch, 4 files / 39 lines, merge-tree clean rebase-and-PR local+remote tiebreaker-tests 2/2 35h none valuable but 639-line test recovery; merge-tree clean, should get CI/review rebase-and-PR local+remote megaplan/cloud-runtime-corr... 10/0 11m none large active cloud/runtime change, 25 files / 2273 insertions; merge-tree clean but needs PR/CI ``` Stashes: none. Prunable worktrees: none. Current checkout: clean, on `megaplan/cloud-runtime-correctness-sprint`. Open PRs: none. Counts: `1 delete-able / 1 merge / 2 PR-needed / 0 cherry-pick / 0 parked / 0 stashes / 0 prunable worktrees`. My strong recommendation: - Delete `megaplan/per-milestone-robustness-20260503` locally and remotely. - Merge `sandbox-fingerprint` to `main`, then delete local+remote branch. - Open PRs for `tiebreaker-tests` and `megaplan/cloud-runtime-correctness-sprint`. - Nothing should just sit around as “keep.”