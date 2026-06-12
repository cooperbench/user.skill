---
name: slash-command-kickoff
description: >
  Trigger: user starts a session or a new work unit with a slash command rather than
  a natural-language description. Fires on ~40% of opening prompts.
---

pc035860 frequently opens sessions or work units with a bare slash command, sometimes with
arguments, sometimes with no additional context at all.

**Pure slash-command openers:**
```
/review-loop gemini
```
```
/doc-update README.md
```
```
/commit --auto
```
```
/simplify last 4 commits
```
```
/commit --auto
```
```
/memory-cleanup
```

**Slash command with spec reference:**
```
/auto-impl @specs/brainstorm/brainstorm-continuous-scroll.md, phase1-2
```
```
/auto-impl @specs/plan/plan-2026-03-09_23-00-28_continuous-scroll-zoom.md

act as one work-unit, start from plan-review phase
```

**Slash command embedded in XML wrapper (Claude Code native format):**
```
<command-message>commit</command-message>
<command-name>/commit</command-name>
<command-args>--auto</command-args>
```

**Mid-session single-word directives (functionally equivalent):**
```
plan
commit
continue
探索
OK
A
2
```

**What it signals:** No discussion needed. Execute the command. If arguments are present,
use them. If the command is bare, use defaults or context from recent history. Never ask
for clarification on a bare `/commit --auto` or `/simplify`.
