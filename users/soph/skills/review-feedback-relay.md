---
name: review-feedback-relay
description: Trigger when Soph pastes external code review feedback (from human colleagues, automated reviewers, or CI tools) verbatim into the chat, often prefaced with "I got this feedback" or "I also got this feedback", and expects the agent to act on it directly.
---

# Review feedback relay

Soph regularly receives code review feedback from colleagues or tools (copilot, subagent reviewers, CI) and pastes it verbatim into the session. The wrapper is minimal — usually a single sentence like "I got this feedback for the changes in this branch:" or "I also got this feedback:" — followed by the raw review text.

The agent is expected to:
1. Read the feedback text
2. Apply the fix or address the concern without asking for further clarification
3. If the feedback is a false positive or already fixed, say so briefly

Soph sometimes adds a short opinion after the feedback: "But I also wonder: …", "can you fix:" — these are additional constraints, not the full ask.

**Example 1:**
> "I got this feedback for the changes in this branch: I reckon we are missing calling logging.WithAgent to add the agent to the context"

**Example 2:**
> "I also got this feedback:\n\nThe test suite for ParseCheckpoint should include test cases for invalid checkpoint IDs to verify that the validation works correctly. Consider adding test cases for: checkpoint IDs that are too short (e.g., \"abc123\")…"

**Example 3 (with Soph's own opinion appended):**
> "I also got this feedback: Consider adding an integration test that specifically reproduces the bug scenario…\n\nBut I also wonder: The bug was code that was doing to much, so having a test that checks a checkpoint isn't made feels a bit strange."
