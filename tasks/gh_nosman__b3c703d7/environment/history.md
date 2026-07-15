> DEVELOPER

Gossamer is an ai session manage built on top of entireio. Debug in the search results page why hits from worktrees don't show up in the appropriate repo. A hit from a worktree should be grouped under the repo it comes from. [Image #4] This checkpoints-visualization hit should be shown under the results from the gossamer-cli repo

> AGENT

Let me look at how search results are grouped by repo.

> AGENT

Now I see the issue. The `enrich_hits` SQL joins sessions to repos via `s.cwd = r.directory OR s.cwd LIKE r.directory || '/%'`, but a worktree's `cwd` is a sibling path, not a subdirectory. Let me check the DB schema for how worktrees are tracked.

> AGENT

Now I need to see how sessions are indexed — specifically, how `cwd` is set for worktree sessions, and whether `repo_id` is populated reliably.

> AGENT

Now I see the bug. In `enrich_hits` (line 785-795 of `search.rs`), the SQL joins sessions to repositories using: ```sql LEFT JOIN repositories r ON (s.cwd = r.directory OR s.cwd LIKE r.directory || '/%') ``` This fails for worktrees because their `cwd` is a sibling path (e.g. `/Users/.../gossamer-checkpoints-visualization`) not a subdirectory of the registered repo (`/Users/.../gossamer`). However, `sessions.repo_id` is already correctly resolved during indexing via `RepoResolver` which uses git remote URL matching. The fix is to add `s.repo_id = r.id` as the primary join condition.

> AGENT

Now build and install to verify it compiles:

> AGENT

Clean build. The fix is a one-line addition to the JOIN condition in `enrich_hits`: `s.repo_id = r.id` is checked first. Since `repo_id` is set by `RepoResolver` during indexing via git remote URL matching (which correctly identifies worktrees as belonging to their parent repo), hits from worktrees will now resolve to the correct `repo_name` and get grouped under the right repo header in search results.