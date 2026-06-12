---
name: expert-correction
description: User delivers a precise, evidence-backed technical correction including line numbers, variable names, and the correct fix. Triggered when agent produces subtly wrong logic, dead code, or wrong API usage.
---

When the agent makes a real technical mistake, dipasqualew does not just say "that's wrong." They deliver the full analysis: what the code actually does, why it's wrong, and what the correct approach is. The feedback is structured with `Status:` labels, line references, and a `Recommendation:` clause.

This is the Expert Nitpicker persona (77% of sessions). They catch bugs the agent does not.

## Example

Submitted as an opening prompt after reviewing CI output:

```
Feedback:

⚠️ Script works locally (via gh pr view) and in GitHub Actions (via env vars)
Status: 🟡 partial

The GitHub Actions path reads GITHUB_REF_NAME and splits on '/'. For a
pull_request event, GITHUB_REF_NAME is set to 'refs/pull/{number}/merge' —
splitting on '/' gives ['refs', 'pull', '{number}', 'merge']. Taking index [0]
yields 'refs', which is not a digit, so the env-var path always falls through to
the gh CLI path. The correct env var to use is GITHUB_REF (same value) with
index [2], or the dedicated GITHUB_EVENT_PATH to read the PR number from the
event payload.

❔ Dead code: comment_data dict built but never used in post_diff_comment
Status: ❌ violation

Lines 303-312 construct a comment_data dict including conditional start_line
logic for multi-line ranges, but this dict is never passed to gh api. The actual
gh api call at line 314 hardcodes individual -f flags and always uses
finding.location.line as the 'line' parameter, ignoring end_line entirely for
the API call. Recommendation: either remove the dead dict and document the
limitation, or use the dict to conditionally add -F start_line=... flags.
```

Also appears as a short one-liner when the fix is obvious:

```
I think you need to use $CLAUDE_PLUGIN_ROOT
```

Or as numbered feedback on a help output:

```
$ vibx --help
bun <command>
...

1. I think `compile` messes up the $0? Hardcode "vibx" or use "filename"?
2. Add a `symlink` script - builds, and then if the branch is main, symlinks to
   ~/.local/bin/vibx; if it is not main, symlinks to ~/.local/bin/vibx-dev
```
