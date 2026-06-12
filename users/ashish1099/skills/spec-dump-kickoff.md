---
name: spec-dump-kickoff
description: Opens a session by pasting a complete pre-written implementation plan — triggered whenever starting a non-trivial coding task.
---

ashish1099 arrives at most sessions with the design already done. The opening message begins
with the literal phrase **"Implement the following plan:"** followed by a full GitHub-flavored
markdown document containing: a `## Context` section explaining the bug or gap, a `## Plan`
section with numbered sub-steps each targeting a specific file and line range, exact Go code
snippets showing the before/after, and a `## Verification` checklist (build, test, manual).

The plan is written before launching the agent — it is not composed interactively. The agent's
role is execution only. ashish1099 does not ask for a design, does not invite the agent to
propose alternatives, and does not frame the message as a question.

**Example 1 (condensed):**
> "Implement the following plan: # Fix: `gfetch cat` doesn't show global ssh_known_hosts
> ## Context When using directory-mode config with a `global.yaml` that sets `ssh_known_hosts`,
> the `gfetch cat` command doesn't display the global value. …
> ## Plan ### 1. Add global defaults to `Config` struct **File:** `pkg/config/config.go`
> Add a `Defaults` field … ```go type Config struct { Defaults *RepoDefaults … } ``` …
> ## Verification 1. Create a directory-mode config … 2. Run `gfetch cat --config <dir>` …"

**Example 2 (condensed):**
> "Implement the following plan: # Enhance `SanitizeName` to Handle All Non-Alphanumeric
> Characters ## Context `SanitizeName` in `pkg/gsync/openvox.go` converts Git ref names …
> ## Changes ### 1. Rewrite `SanitizeName` … Replace `strings.NewReplacer` with `strings.Map`
> using an allowlist approach … ### 2. Add test cases … Add to `TestSanitizeName` table …"
