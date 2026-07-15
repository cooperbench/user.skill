> DEVELOPER

You are a code reviewer. Your job is to review code changes and provide actionable feedback.

---

Input: branch

---

## Determining What to Review

Based on the input provided, determine which type of review to perform:

1. **No arguments (default)**: Review all uncommitted changes
   - Run: `git diff` for unstaged changes
   - Run: `git diff --cached` for staged changes
   - Run: `git status --short` to identify untracked (net new) files

2. **Commit hash** (40-char SHA or short hash): Review that specific commit
   - Run: `git show branch`

3. **Branch name**: Compare current branch to the specified branch
   - Run: `git diff branch...HEAD`

4. **PR URL or number** (contains "github.com" or "pull" or looks like a PR number): Review the pull request
   - Run: `gh pr view branch` to get PR context
   - Run: `gh pr diff branch` to get the diff

Use best judgement when processing input.

---

## Gathering Context

**Diffs alone are not enough.** After getting the diff, read the entire file(s) being modified to understand the full context. Code that looks wrong in isolation may be correct given surrounding logic—and vice versa.

- Use the diff to identify which files changed
- Use `git status --short` […]

> AGENT

I'll start by determining the base branch and getting the diff for the current branch.

> AGENT

There are uncommitted changes too. Let me get those and also read the full files being modified.

> AGENT

Now let me find and read the full files involved in this branch, including the Go-side agent implementation and the embedded plugin source.

> AGENT

The committed diff only touches `.entire/settings.json` and `.opencode/plugins/entire.ts`. The Go files exist but weren't modified in this branch - let me check if they were added in this branch.

> AGENT

So the branch only adds `.opencode/plugins/entire.ts` (new file) and modifies `.entire/settings.json`. The Go files under `cmd/entire/cli/agent/opencode/` already exist on `main`. Let me read the plugin source files and relevant context to review properly.

> AGENT

Now let me understand the relationship between the two `.ts` files and check how the template is used during installation.

> AGENT

Now let me look at the `.entire/settings.json` change more carefully, and check if the plugin file in `.opencode/` should be `.gitignore`d:

> AGENT

Let me check how other agents' plugins are handled — specifically, are similar agent config directories committed to the repo?

> AGENT

Now let me check the uncommitted change more carefully — the `.cwd(directory)` addition:

> AGENT

Now let me check the `localDev` path — the plugin uses `OPENCODE_PROJECT_DIR` as an environment variable. Let me verify this is set somewhere:

> AGENT

Now let me check whether the `callHookSync` function has a shell injection concern with `ENTIRE_CMD`:

> AGENT

Let me also check whether this `.opencode/plugins/entire.ts` is the instance generated for local development (since the repo has `local_dev: true`):

> AGENT

The committed version has `ENTIRE_CMD = "entire"` (production mode), while the template has `__ENTIRE_CMD__`. Let me also check if there's a `.gitignore` for the `.opencode` directory or if this file is meant to be committed:

> AGENT

The `.opencode/.gitignore` ignores `node_modules`, `package.json`, `bun.lock`, and `.gitignore` itself — but not the `plugins/` directory, which is why the plugin file gets committed. Now let me check if other agents' similar generated files are committed or ignored:

> AGENT

Now let me check one more thing about the `callHookSync` function — the `sh -c` construction with string interpolation could be a concern if `ENTIRE_CMD` contains spaces (which it does in localDev mode: `go run ${OPENCODE_PROJECT_DIR}/cmd/entire/main.go`):

> AGENT

Now let me look at the `messageStore` for potential memory leak concerns and the overall event flow:

> AGENT

I have enough context now. Let me compile my review.

---

## Review: `feat/opencode-support` branch

### Summary

This branch adds an OpenCode plugin file (`.opencode/plugins/entire.ts`) to the repo and reorders keys in `.entire/settings.json`. The Go-side agent implementation already exists on `main`; this branch adds the generated plugin instance for use during development.

There are also **uncommitted changes** that add `.cwd(directory)` to the `callHook` async function in both the repo plugin and the embedded template — these should likely be part of this branch.

---

### Issues

#### 1. Bug: `callHook` (async) missing `.cwd(directory)` — partially fixed in uncommitted changes

**File:** `.opencode/plugins/entire.ts:25`, `cmd/entire/cli/agent/opencode/entire_plugin.ts:25`

The committed version of `callHook` does not set `cwd`:

```ts
await $`echo ${json} | ${ENTIRE_CMD} hooks opencode ${hookName}`.quiet().nothrow()
```

The `callHookSync` variant correctly sets `cwd: directory` (line 41). Without `.cwd(directory)`, the async hook will run in whatever the shell's default cwd is, which may not be the project directory. This could cause `entire hooks` to fail to locate the git repo.

The uncommitted working copy has the fix (`.cwd(directory)`), but it hasn't been committed yet. **This fix should be committed as part of the branch.**

#### 2. Behavior: `.entire/settings.json` key reorder is noise

**File:** `.entire/settings.json`

The only change […]