---
name: baotoq-preferences
description: What baotoq corrects, what satisfies him, workflow habits, and tool/stack preferences
---

## Pushback distribution

- **non_pushback:** 81.5% — accepts agent output most of the time
- **failure_report:** 9.6% — pastes a review/audit section when agent signals it's waiting
- **correction:** 7.4% — blunt redirects or re-issued slash commands
- **rejection:** 1.5% — issues new slash command without comment, abandoning agent's current path

## What triggers corrections

1. **Agent asking a question instead of acting:** when the agent says "Want me to run X instead?" he replies with the action content directly, not with "yes"
2. **Agent waiting for all subagents before presenting:** he injects individual subagent results as soon as they're available, not waiting for a batch summary
3. **Phase numbering mistakes or wrong routing:** immediately re-issues the correct command
4. **Agent presenting options when user wants one specific thing:** `"no i want to deeply check the previous implementation"`
5. **Agent completing a milestone boundary and not proceeding:** he issues the next `/gsd:` command

## What triggers rejections (no comment)

- Agent starting the wrong workflow (issues correct slash command with no explanation)
- Agent outputting status when user expects a command dispatch

## What satisfies him

- Structured output with severity tables: `| CRITICAL | N | ... |`
- Wave-based parallel execution completing all plans cleanly
- Verification passing: `6/6 must-haves`
- Phase summaries with commit hashes
- Agent that loads its own context from `@file` references without being told what to read

## Workflow habits

**Planning → Execution → Verification → Audit → Complete cycle:**
1. `/gsd:plan-phase N --auto` — research + plan with verification loop
2. `/gsd:execute-phase N` — wave-based parallel execution via subagents
3. `/gsd:audit-milestone` — requirements coverage + integration check
4. `/gsd:complete-milestone vX.Y` — archive + git tag
5. `/gsd:new-milestone` — start next cycle

**Automation preference:** Always uses `--auto` flag to skip prompts. Uses `--gaps` and `--gaps-only` flags for gap closure passes. Uses `--no-transition` to suppress cross-phase confirmation gates.

**Context management:** Starts new sessions frequently (often after hitting usage limits). Uses `/clear` to reset context between milestones. References `@file` paths rather than pasting file contents.

**Interruption pattern:** Interrupts in-progress sessions when quota runs out (`"You're out of extra usage · resets 3am (Asia/Saigon)"`). Resumes by re-issuing the same slash command.

**No explanations requested:** Does not ask the agent to explain its reasoning or teach him concepts. Exception: `"what is agentic ai"` — a rare curiosity question, likely testing GSD system on a novel topic.

**Test cadence:** Tests are tracked in intent distribution (2.2%) — he doesn't run tests himself; the GSD workflow includes test gates in the execute-phase verification pass.

**Commit cadence:** Follows conventional commits (`feat(25.1-10): create branded auth login page`). Commits happen per plan, tracked in subagent summaries.

**Planning first:** Always plans before executing. Never skips the `plan-phase` → `execute-phase` sequence.

## Tool/stack preferences (evidenced)

- **.NET 10 + ASP.NET Core** for backend (strongly typed with Vogen IDs, FluentResults, SmartEnum)
- **Next.js 14 + TypeScript + shadcn/ui** for frontend (Biome for linting)
- **MassTransit** for messaging with EF Core outbox pattern
- **Keycloak** for OIDC auth (not NextAuth custom providers)
- **Kustomize** for K8s manifest management (base + overlays/dev pattern)
- **ArgoCD** app-of-apps for GitOps
- **SealedSecrets** for secret management in Git
- **1Password** for CI/CD secrets (`load-secrets-action`)
- **Claude Code** as the AI agent runtime, GSD as the workflow orchestration layer
- **Paperclip** as the multi-agent platform (heartbeat model, PAPERCLIP_* env vars)
