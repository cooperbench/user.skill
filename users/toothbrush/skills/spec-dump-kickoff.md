---
name: spec-dump-kickoff
description: How toothbrush opens large implementation tasks — submits a complete, pre-authored plan with file names, function signatures, line numbers, and code snippets. Trigger when starting a session with a new feature or multi-step change.
---

# Skill: spec-dump-kickoff

toothbrush arrives with the architecture already designed. Opening prompts for non-trivial tasks are self-contained implementation plans: markdown-headed sections (`## Context`, `## Plan`, `### Step N`), specific file paths with line numbers, exact function signatures, and often Go code snippets. The agent is expected to execute the plan verbatim; no design discussion follows.

**Pattern**:
```
Implement the following plan: # <Title>
## Context
<2-4 sentence explanation of what exists and why this change is needed>
## Plan
### Step N: <verb phrase> (<file>)
<precise instruction with optional code>
```

**Example 1** (short form):
> "Implement the following plan: # Move shell completion prompt from `enable` to new `curl-bash-post-install` command ## Context The CLI's `enable` command currently includes an optional shell-completion installation prompt. Now that we have an `install.sh` script (curl|bash installer) that calls `entire curl-bash-post-install` after installing the binary, we need a dedicated hidden command for that post-install step. For now it should just do the interactive completion prompt. We'll remove the completion logic from `enable`. ## Changes ### 1. Create `newCurlBashPostInstallCmd()` in `cmd/entire/cli/setup.go`…"

**Example 2** (one-liner task, same delegate-and-execute mode):
> "Ensure that JSON parsing of .entire/settings.json is strict - fail if any unrecognised keys are present."

**Key signals**:
- Uses `Implement the following plan:` as a literal prefix on large tasks
- Plan includes `## Context` explaining the current state and motivation
- Steps are numbered and tied to specific files and line numbers
- Code snippets are included inline in the plan
- No question asked; execution expected immediately
