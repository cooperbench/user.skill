---
name: log-paste-debug
description: Triggers when a runtime failure occurs. cteyton pastes raw server logs verbatim (timestamps, PIDs, API routes, error messages) with a brief lead sentence. No trimming, no annotation. Classified as failure_report pushback (6.1% of prompts).
---

# Verbatim log paste for runtime failures

When something fails at runtime, cteyton pastes the entire log output without editing it. The format is:

1. One brief lead sentence naming which component or action triggered the failure (sometimes zero setup — the log just appears).
2. Raw log block: `[Timestamp] [Component] Message` lines, including proxy routes, SSE connections, error codes, and stack traces.
3. Sometimes a URL reference at the end if it's a known endpoint.

The agent is expected to diagnose and fix from the raw log. No further explanation is offered.

## Verbatim examples

> `"I've run a remediation with cursor but got these errors: [Remediation] Plan-first pipeline: 5 errors, 6 suggestions, 4 AI invocations, provider: cursor [Remediation] Phase 1: Planning error fixes (5 issues) [Cursor Agent] Spawning: agent -p --output-format json (prompt via stdin, 17687 chars, cwd: /Users/cedricteyton/Code/agents-md-evaluator/tmp/clones/agents-eval-aTBoB5) [Bun.serve]: request timed out after 10 seconds. Pass idleTimeout to configure. [Proxy] GET /api/remediation/8227bedf-5752-4b17-80f6-62d8e7c4def5/progress -> http://localhost:REDACTED [13:45:07.973] [API] GET /api/remediation/8227bedf-5752-4b17-80f6-62d8e7c4def5/progress [RemediationSSE] Connected for job 8227bedf-5752-4b17-80f6-62d8e7c4def5 (2 connections)..."`

> `"Can you investiage these runtime errors when running Cursor Agent CLI ? can you maybe logs more output of the command? [Proxy] GET /api/remediation/9e063482-f731-4e87-a95d-2e07081bead2/progress -> http://localhost:3001/api/remediation/9e063482-f731-4e87-a95d-2e07081bead2/progress..."`

> `"I got this issues when running 'OpenAI Codex' [11:35:44.030] [API] GET /api/remediation/eeab8e50-3eee-42da-b2af-a42b2c6b4b9f/progress [RemediationSSE] Connected for job eeab8e50..."`

> `"It only logs score but it's not updated in DB"` — (short failure report when the behavior is observable without a log)

> `"Are you sure? Check http://localhost:3000/evaluation/dd283666-3a94-43cd-8565-7dff030c01d1?tab=summary\n[Image: image/png]"` — (log + screenshot combo)

## Key traits

- Typo present in one example: `"investiage"` — not corrected.
- Lead sentence may end with `?` when asking for more logging: `"can you maybe logs more output of the command?"`.
- Uses first-person past tense: `"I've run"`, `"I got"`, `"I cannot re-run"`.
- Does NOT format logs into code blocks — raw text inline.
