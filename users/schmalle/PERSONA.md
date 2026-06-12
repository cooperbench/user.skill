---
name: schmalle-persona
description: Background, expertise, role, seniority, and attitude of schmalle toward the agent.
---

## Role (inferred)
Solo founder/owner-developer of secman — a production vulnerability-management platform deployed at a corporate customer (`secman.covestro.net`). Not a hobbyist: the system handles 800 000+ CrowdStrike vulnerabilities, real production JWT secrets, WebAuthn, OAuth OIDC, MCP API keys, and SMTP credentials. He is the architect, developer, security auditor, and product owner simultaneously.

## Seniority (inferred)
**Senior full-stack with a security specialization.** Evidence:
- Independently authors correct, detailed fix plans for complex issues (FK cascades, Hibernate lazy-loading, JWT `alg:none` root-cause, PKCE flows, SSE heartbeats, YAML duplicate-key shadowing).
- Knows OWASP Top 10 by heart; cites CWE numbers in his own prompts.
- Understands Micronaut DI, Kotlin coroutines, JPA/Hibernate lifecycle, Flyway migrations, React hydration, Vite bundle splitting.
- Has strong AWS intuition (shared accounts, IAM, S3 path-style addressing).
- Cross-references frontend TypeScript interfaces against backend Kotlin DTOs by memory.

## Domain
- **Primary**: Application security (OWASP, JWT, JWKS, CSP, rate-limiting, injection)
- **Secondary**: Cloud vulnerability management (CrowdStrike Falcon API, AWS EC2 asset tracking)
- **Tertiary**: Enterprise software delivery (requirement reviews, alignment dashboards, release gating)

## Language background (inferred)
Non-native English speaker, likely German-speaking (European timezone reference "resets 3pm Europe/Berlin"; corporate customer Covestro is German). Typed fast with minimal proofreading: "ownershop", "execption", "dont", "havent", "depencenies", "Doamin" (typo for Domain), "fi" (fix), "prio" (priority).

## Attitude toward the agent

**Trusting but quick to correct.** Schmalle grants the agent full autonomy on implementation once a plan is in place — he rarely asks to review code before it runs. But he verifies in the live UI and reports back immediately when something is visually wrong, doesn't compile, or produces an unexpected behavior.

- **When satisfied**: Silent acceptance, or "yes", or moves directly to the next task. No praise.
- **When dissatisfied**: Short, factual redirect. "this is wrong", "i dont see the change in the UI", "please fix this", "fix all findings". Never angry, always task-focused.
- **When changing mind**: No explanation of why; just issues the new instruction as if the previous one never happened.
- **Trust level**: High for code generation, low for "insight" summaries (he ignores `★ Insight` blocks and jumps to the next task).

## Planning workflow
Uses a custom speckit slash-command system (`/speckit.specify`, `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`) that generates structured markdown implementation plans. He exits plan mode, then copies the plan back verbatim as his opening prompt for a new session.
