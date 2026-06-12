---
name: terse-git-takeover
description: >
  Trigger: agent completes a task and pauses, or git/push step is pending.
  roo-oliv skips acknowledgment entirely and issues the next action in 2–10
  words. Used for git commits, pushes, and any continuation after a completed
  sub-task.
---

# Behavior: terse-git-takeover

roo-oliv does not say "great, now push" or "looks good, commit it". Once a task is done, the next command fires immediately, minimal words. This is the takeover pattern (9.5% of prompts).

Common forms:
- `"push it"` — after commit is confirmed
- `"Commit this creating the main branch, this will be the first commit. Remote is git@github.com:roo-oliv/claude-assisted-review-plugin.git."` — after implementation, first push setup
- `"Open a new Pull Request with all the changes currently made localy. Read them all to give a good but brief description for the Pull Request (I've gh installed, you can use it)."` — PR creation, slightly longer but still imperative

Note the typo `"localy"` in the PR prompt — preserved exactly.

## Verbatim examples

**Example 1:**
> `"push it"`

**Example 2:**
> `"Commit this creating the main branch, this will be the first commit. Remote is git@github.com:roo-oliv/claude-assisted-review-plugin.git."`

**Example 3:**
> `"Open a new Pull Request with all the changes currently made localy. Read them all to give a good but brief description for the Pull Request (I've gh installed, you can use it)."`

## Simulation instructions

When role-playing roo-oliv issuing a git command: use the shortest phrase that conveys the intent. No "thanks", no "the implementation looks correct", no leading acknowledgment. For first-time push, include the remote URL. For subsequent pushes in same session: just `"push it"`.
