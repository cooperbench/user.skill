---
name: discord-feedback-dump
description: Starts a feature/bug session by pasting raw Discord chat logs from Moltis users. Triggered when penso collects user feedback from the Discord server and wants to batch-address all issues. He pastes the full transcript with timestamps, usernames, and follow-up messages intact.
---

## Behavior

penso copies a Discord conversation verbatim — timestamps, usernames, follow-up messages, emoji — and pastes it as the session or turn opener. He then adds a short directive asking the agent to plan or implement fixes for everything in the transcript.

The transcript is the spec. The agent is expected to:
1. Parse all distinct issues from the chat
2. Prioritize and plan fixes
3. Implement them (or plan them first, then implement on `"Please implement all"`)

## Opening directive pattern

```
Someone on Discord installed Moltis, this is a list of feedback. Plan to fix or improve any of his issues:
[raw Discord transcript]
```

## Follow-up after planning

After the agent produces a plan (with issue analysis, effort estimates, priorities), penso sends:
> "Please implement all"

## Verbatim example (opener)

> "Someone on Discord installed Moltis, this is a list of feedback. Plan to fix or improve any of his issues: [12:51 PM]David Cumps : Sort LLM preferred model list alphabetical Voice: Local faster-whisper support? ElevenLabs Scribe, configured, Test: "Error: Invalid constraint" Add more channels? Slack. (Or add note it can be configured later) Identity emoji list is cut off Summary - Tailscale with warning icon, Installed but not connected (didn't have an option to configure this during setup) …"

## Verbatim example (follow-up)

> "Please implement all"

## Reading Discord channel for new info

penso also uses Discord as a research source mid-session:
> "Reading Discord I got: Hey, I just upgraded an instance to moltis from openclaw and I'm struggling to setup the telegram bot…"
