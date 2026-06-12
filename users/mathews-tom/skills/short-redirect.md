---
name: short-redirect
description: How Mathews-Tom steers mid-session with very short messages — 2–10 word one-liners that continue, redirect, or hand off work without explanation. Trigger for any routine continuation, git operation, or branch/naming correction between heavy plan-dump prompts.
---

# Short Redirect

Between heavy plan-dump prompts, Mathews-Tom sends terse one-liners to continue, redirect, or hand off. These are plain English, no markdown, and assume full shared context. He doesn't re-explain anything.

**Continuation**: `"keep going, don't wait for me"` — signals autonomous mode; do not pause for updates.

**Git operations**: Short imperatives for the entire git workflow:
- `"commit this"`
- `"push and open a detailed PR"`
- `"push the commits and create a detailed PR"`
- `"merge the PR"`
- `"i have merged the pr. Are we done with development of the system."`

**Branch/naming corrections**: When the agent uses the wrong branch name or pattern, corrects with the exact value backtick-quoted:
- `"Use the branch name \`feat/alignment-systems\`"`
- `"Let us create a local branch and start the development of script for the section \`foundations\`"`

**Validation before merge**: Short but slightly more specific:
- `"run all 7 scripts to validate before merging. At the end present the results from each script as a summary."`
- `"test all the newly created scripts and validate everything is working."`

## Examples

**Example 1**: `keep going, don't wait for me`

**Example 2**: `commit this`

**Example 3**: `push and open a detailed PR`

**Example 4**: `merge the PR`

**Example 5**: `Use the branch name \`feat/alignment-systems\``

**Example 6**: `run all 7 scripts to validate before merging. At the end present the results from each script as a summary.`

**Example 7**: `Create a local branch and start working on phase 2 scripts`
