---
name: plan-dump-execute
description: How alishakawaguchi opens implementation tasks — pastes a complete pre-written markdown plan starting with "Implement the following plan:" and expects silent execution. Trigger when the session opens with a large structured specification.
---

# plan-dump-execute

alishakawaguchi designs all non-trivial implementations in plan mode before the execution session begins. The opening prompt of an implementation session is a verbatim paste of the exported plan — a structured markdown document with `# Title`, `## Context`, `## Root Cause Analysis`, `## Changes`, `### Step N`, tables, and code fences showing exact before/after diffs.

The phrase "Implement the following plan:" is almost always the literal opener. The plan is self-contained: it names exact file paths, line numbers, function signatures, and verification commands. The user does not expect questions; they expect execution.

## Behavior pattern

- No greeting, no preamble
- Paste begins with "Implement the following plan:" followed immediately by `# PlanTitle`
- Plan includes `## Context`, `## Changes`, code blocks with `// Before:` and `// After:`, and a `## Verification` section ending with a bash command (usually `mise run fmt && mise run lint && mise run test:ci`)
- Plan often includes a note at the end: "If you need specific details from before exiting plan mode..., read the full transcript at: /Users/alisha/.claude/projects/..."
- No follow-up questions; if the agent asks a question mid-execution, the user either ignores it or pastes the next slash command

## Examples

**Example 1 (opening of an implementation session):**
```
Implement the following plan: # Fix: Droid Token Usage Offset Mismatch ## Context `calculateTokenUsage` in `manual_commit_condensation.go` has a bug for Droid transcripts. The `startOffset` parameter is a raw JSONL line count (from `countTranscriptItems`), but it's used as an index into the array returned by `ParseDroidTranscriptFromBytes`, which filters out non-message entries...
```

**Example 2 (shorter, in-session when the plan is compact):**
```
update main.go to have two players roll dice and then print out winner
```
(When the task is simple enough, the "plan" is a single imperative sentence — same pattern, compressed.)
