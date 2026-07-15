> SYSTEM

# AGENTS.md instructions for /home/entity/projects/EntityProcess/agentv <INSTRUCTIONS> # AgentV Agent Guide This file is the root index for repo-facing agent instructions. It carries baseline rules that always apply plus a [Routing](#routing) table that maps your change to the deeper `.agents/*.md` guide you must read **before** starting that work. The rules in this file are a summary; each linked guide is authoritative for its area, so a matching Routing trigger means "read the guide," not "the summary is enough." Read [STRATEGY.md](STRATEGY.md) plus [ROADMAP.md](ROADMAP.md) before making product-boundary calls. ## Product Direction AgentV aims to be the repo-native, workspace-native evaluation framework for AI agents. - Repo-native evals: run against real repos, multi-repo workspaces, setup scripts, and existing harnesses. - Zero-infra local to CI: keep the default path lightweight so the same eval contract works on a laptop and in CI. - Portable run artifacts: treat run bundles, traces, and summaries as the source of truth for comparison, gating, and export. - Adapter boundaries: integrate with Phoenix, Harbor, Opik, and provider-specific systems through narrow adapters instead of absorbing their concepts into core. - AI-native extensibility: keep the core small and composable so engineers and coding agents can extend it with plugins, wrappers, and harness-specific glue. […]

> DEVELOPER

create orphan dogfood branch in agentv-private repo with screenshots i manually took in https://github.com/EntityProcess/agentv-private/issues/14. also update index.md for any recent orphan branches not included there. merge your changes to remote main for the index.md

> AGENT

I’ll handle this as repo workflow/evidence work. First I’m going to read the required AgentV workflow and verification guides, then I’ll inspect both the public checkout and the private evidence repo state before touching branches.

> AGENT

I created a Beads task `av-l5qi` for the evidence publishing work and read the AgentV workflow/verification rules. The public checkout is currently `main` behind `origin/main` with an untracked `replay-contract/`, so I’ll avoid touching that unrelated state and work in the private repo.

> AGENT

I’m using the GitHub workflow guidance as well because the source screenshots are attached to a private GitHub issue and the task includes pushing/merging remote branch state. Next I’m locating the `agentv-private` checkout or cloning it if needed, then I’ll inspect issue 14’s attachments.

> AGENT

The private repo is present at `/home/entity/projects/EntityProcess/agentv-private`, and `gh` is authenticated with repo access. I’m fetching that repo now and reading the current index format plus issue 14 attachment metadata so the evidence branch matches the existing convention.

> AGENT

The `agentv-private` checkout is currently on an existing evidence branch with many untracked files, so I’m going to avoid that checkout for edits. I’ll create a separate temporary worktree for `main` and use a separate isolated clone/worktree for the orphan evidence branch.

> AGENT

Issue 14 contains two image attachments: “Transcript” and “Tool Calls.” The private repo already has a large set of orphan-style `evidence/*` branches; I’m going to generate the missing index entries from remote branch metadata rather than trusting only local branch refs, because several recent remote branches are not checked out locally.

> AGENT

The current `index.md` was last refreshed on July 4 and is missing July 5-6 branches. I’m preparing a new orphan evidence branch for issue 14 first, then I’ll regenerate the index from all `origin/*` heads so the new branch and the recent missing branches land together.

> AGENT

The orphan checkout exists; the cleanup command hit Git’s “nothing tracked yet” case, which is harmless for a fresh root branch. I’m checking the temp branch contents before adding the issue screenshots and manifest.

> AGENT

I’m adding a compact README on the orphan branch with the issue link, capture date, source context, and a short description for each screenshot. The screenshot binaries will be downloaded directly from GitHub’s attachment URLs into a `screenshots/` folder.

> AGENT

The raw attachment URLs return 404 without authenticated GitHub request headers, which is common for private issue uploads. I’m retrying through the authenticated `gh` token path and will verify the resulting image metadata before committing anything.

> AGENT

The evidence branch now has the two PNG screenshots and a README manifest. I’m committing and pushing it as an orphan/root branch, then I’ll refresh `index.md` from the remote refs including that new branch.

> AGENT

The new orphan branch is pushed at commit `5ff2118`. I’m refreshing the index worktree’s remote refs now, then I’ll replace the table mechanically from `origin` heads sorted by commit timestamp.

> AGENT

The regenerated `index.md` adds the new issue 14 branch plus the missing July 5-6 evidence branches. I’m doing a markdown whitespace check, committing only `index.md`, and pushing that commit as a fast-forward update to `origin/main` in the private repo.

> AGENT

The index commit was pushed directly to `agentv-private` `main` as requested: `f8fe3f9`. I’m running final verification now: confirming the evidence branch is a root commit, confirming remote `main` points at the index refresh, and checking worktree status so I can distinguish my temp work from pre-existing local state.

> AGENT

Final checks passed: the evidence branch has a single root commit with exactly the README and two screenshots, and `origin/main` now points at the index refresh commit. I’m closing the Beads task and doing the final status checks.

> AGENT

The Beads task is closed. I’m removing only the temporary worktrees/clones I created under `/tmp`; the pre-existing dirty `agentv-private` checkout and the public repo’s untracked `replay-contract/` are left untouched.

> AGENT

Done. Evidence branch created and pushed: `evidence/issue-14-phoenix-transcript-traces-2026-07-06` Commit: `5ff2118` URL: https://github.com/EntityProcess/agentv-private/tree/evidence/issue-14-phoenix-transcript-traces-2026-07-06 It contains: - `README.md` - `screenshots/transcript.png` - `screenshots/tool-calls.png` Updated `index.md` for recent missing orphan/evidence branches, including the new issue 14 branch, and pushed it to remote `main`. Index commit on `main`: `f8fe3f9` Verification run: - Confirmed evidence branch root commit is `5ff2118`. - Confirmed remote `main` points to `f8fe3f9`. - Ran `git diff --check` on `index.md`. - Verified both screenshots downloaded as PNGs with expected dimensions. Left untouched: - Public `agentv` checkout is still behind `origin/main` with pre-existing untracked `replay-contract/`. - Existing `agentv-private` checkout still has its pre-existing untracked files.