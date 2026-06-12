---
name: schmalle-preferences
description: What schmalle corrects, what satisfies him, workflow habits, tool preferences, and pushback triggers.
---

## Pushback distribution
| Type | Rate |
|------|------|
| Non-pushback (accepted) | 55.5% |
| Correction | 32.7% |
| Failure report | 11.8% |

He corrects nearly 1-in-3 agent outputs. A further 1-in-9 is a straight failure report (something visually broken).

## What triggers corrections

1. **Partial scope**: Agent does A but misses B. Example: removes columns but doesn't update `getCriticalityBadge` dead code. Or adds access control to one page but not the related one.
2. **Wrong target**: After doing X, agent outputs insights about X instead of moving to Y. Schmalle ignores the insight and immediately asks for Y.
3. **UI not reflecting code change**: The agent reports "build successful" but the feature isn't visible in the running UI. He screenshots it and says "i dont see the change".
4. **Scope creep in wrong direction**: Agent explains architecture or adds extra columns/features he didn't ask for. He corrects with "please remove X" or "rename X to Y".
5. **Plan output ≠ implementation**: If the agent's plan describes one approach but the implementation diverges, he either silently lets it through or pastes the specific delta finding and says "fix this".

## What triggers failure reports

1. **Visual bugs**: NaN in pagination, wrong badge color, missing column, wrong error message replacing the whole page.
2. **Broken flows**: Approving an exception still shows it pending; clicking a button throws a JavaScript error.
3. **Build errors**: Gradle compile failure after a change. He pastes or screenshots the error and says "fix this error please, propose first a careful fixing plan" or just attaches the image.
4. **Mismatch between backend and UI**: Data exists in backend but UI shows 0 / empty / wrong value.

## What satisfies him (non-pushback)

- "yes" — simple affirmation after an agent asks a clarifying question.
- Silent next-task pivot — moves directly to the next feature without acknowledgment.
- Single-character "A" or "b" — selecting an option from a numbered list the agent presented.
- Pasting the next plan-paste — means the previous implementation was accepted and he's starting the next feature.

## Workflow habits

**Planning first, always.** Schmalle never says "add feature X" and expects the agent to design and implement in one shot for complex features. He runs `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.tasks`, then copies the resulting plan as his implementation prompt. The plan contains exact file paths, line numbers, and code snippets.

**Does not ask for explanations.** He rarely asks "why does this work?" or "explain this to me." He uses `/understand` intents mainly for security review summaries or to read task output files — not for learning.

**Test-driven? No.** Only 0.8% of prompts are test intent. He writes Playwright E2E tests via speckit once (for login + navigation), not as a continuous habit.

**Commit cadence: not visible.** No git intents in the dataset beyond 0.4%. He doesn't ask the agent to commit or push.

**Interrupts freely.** He cancels agent tool calls mid-run with `[Request interrupted by user for tool use]` — 10+ times in 247 prompts. He doesn't wait politely.

**Security review workflow.** He runs full security audits using parallel sub-agents (the agent spins up 4 concurrent reviewers for different dimensions). He then pastes each individual finding back as a separate prompt for implementation. This is his security sprint pattern.

**Docs maintenance.** He occasionally asks the agent to update `/docs` to match current implementation after a feature sprint.

## Tool/stack preferences visible in prompts

- **Backend**: Kotlin, Micronaut, JPA/Hibernate, Flyway, MariaDB, Gradle
- **Frontend**: Astro, React (TSX), Bootstrap, Axios, Playwright
- **Security**: OWASP Top 10, BCrypt, JWT/JWKS, WebAuthn, OAuth OIDC, HttpOnly cookies, CSP
- **Cloud**: AWS S3, CrowdStrike Falcon API, EC2 instance metadata
- **CLI tooling**: Custom Kotlin CLI with PicoCLI, S3 integration, speckit slash commands
- **Testing**: Playwright (E2E, Edge + Chrome), credentials via 1Password CLI injection
- **Secrets**: 1Password for credentials, environment variables for JWT/encryption secrets, no hardcoded defaults
