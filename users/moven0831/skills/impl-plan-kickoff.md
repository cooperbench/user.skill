---
name: impl-plan-kickoff
description: >
  Triggered when starting a new implementation session. moven0831 opens with a full
  "Implement the following plan:" markdown block containing context, changes, file targets,
  code snippets, and verification steps — the entire plan written during brainstorming mode.
---

When beginning implementation, moven0831 does not say "please code X". Instead they paste a
complete, structured plan block generated during the planning phase:

**Structure**:
```
Implement the following plan:

# <Plan title>

## Context
<Why this fix is needed and what went wrong>

## Changes

### 1. Fix `<file path>`
<What to change, with before/after code snippet>

### 2. Fix `<other file>`
<Change description>

## Verification
1. <How to test step 1>
2. <How to test step 2>
3. <Expected outcome>


If you need specific details from before exiting plan mode (like exact code snippets, error
messages, or content you generated), read the full transcript at: /Users/moventsai/.claude/projects/<project>/<session-id>.jsonl
```

**Key traits**:
- Always starts with `Implement the following plan:` (literal string)
- Plan title is a short `# Fix:` or `# Plan:` heading
- Contains exact file paths (not just "the relay file")
- Includes TypeScript code snippets with correct syntax
- Lists numbered verification steps with specific curl commands or expected output
- Ends with a transcript path hint for plan-mode context recovery
- No preamble — the plan block is the entire message

**Verbatim opening** (truncated):
```
Implement the following plan:

# Fix: UserState not synced after on-chain signup

## Context

During E2E testing, `POST /api/signup` fails with `@unirep/core:UserState user is not signed up`.
The `UserState` is created and synced before the `userSignUp` transaction is submitted on-chain.
After `tx.wait()`, the UserState's in-memory DB hasn't re-synced to pick up the signup event,
so `latestTransitionedEpoch()` throws.

## Fix

**File**: `packages/relay/src/routes/anonbook-signup.ts` (line 62-71)

Add `await userState.waitForSync()` after `await tx.wait()` ...
```
