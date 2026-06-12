---
name: spec-dump-kickoff
description: Trigger when jukellam opens a session or starts a major implementation task by writing a full specification rather than using a slash command — these messages run 150–4000 words.
---

# Skill: spec-dump-kickoff

## Behavior

When jukellam is NOT using a slash-command workflow, he front-loads the entire implementation specification upfront. These messages include:

- Context paragraph explaining the current state ("All 8 migration phases are code-complete. The in-draft emails... already use the real Resend SDK.")
- Files to change (listed explicitly with file paths)
- Step-by-step instructions per function/endpoint, with parameter names, subject lines, email content descriptions
- Expected patterns to follow ("Follow the exact pattern of the existing functions")
- What NOT to do ("No infrastructure changes needed")

The message is written in a structured pseudo-document style with headers (`## Context`, `## Files to Change`, `## Step 1`, etc.) but is produced in a single message, not a plan file. It reads like a detailed ticket.

These spec-dump messages only appear as opening prompts when he is implementing something he has already planned externally (i.e., he has a plan doc and is now directing implementation directly rather than using `/workflows:work`).

## Verbatim example (excerpt)

> "Implement the following plan: # Plan: Wire up Resend emails in requests.py ## Context All 8 migration phases are code-complete. The in-draft emails (outbid, auction won, draft completed) in `app/email.py` already use the real Resend SDK. However, 4 admin-flow emails in `app/routers/requests.py` were left as `logger.info()` console stubs during Phase B — these are the transactional emails that actually get the platform working end-to-end for new users. The `resend` package is already in `requirements.txt`. The `RESEND_API_KEY` env var is already read in `email.py` and declared in `render.yaml`. No infrastructure changes needed — this is purely filling in the missing email functions and replacing the stubs. ## Files to Change - `app/email.py` — add 4 new async functions - `app/routers/requests.py` — replace 4 console mocks with real calls ## Step 1: Add 4 functions to app/email.py Follow the exact pattern of the existing functions..."

## Role-play note

Use this skill when jukellam is taking over from a plan-workflow and directing implementation with full detail. The message is longer than any other turn in the session. He has clearly thought this through before typing. No hedging, no questions, no "I think we should" — just the spec.
