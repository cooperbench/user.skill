---
name: terse-status-check
description: When a long-running agent task is in progress and the user wants to know its status — they send a 2–4 word lowercase question, no punctuation (except an occasional question mark).
---

# Terse status check

When background tasks are running and the user wants an update, they send the shortest possible question. No context, no politeness. Just the check.

**Trigger**: Agent has been running a long task (E2E tests, parallel subagents) and hasn't reported back yet.

**Pattern**: 2–4 words, lowercase, optional question mark, no period.

**Examples**:
- `are they running?`
- `still running?`
- `is it now running`
- `how is the testing`
- `did you check`
- `whats taking so long`

If the answer is not what they expected (e.g., agent confirms still running but user believes it's been too long): follow up with a vague but pointed correction: `well its been more i think`
