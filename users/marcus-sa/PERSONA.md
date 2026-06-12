---
name: marcus-sa-persona
description: Background, expertise, seniority, and attitude toward the agent for marcus-sa.
metadata:
  type: user
---

# Persona: marcus-sa

## Role and domain (inferred)

Founder or technical co-founder (inferred) of a startup building Brain — described as "an operating system for autonomous organizations." He owns both product vision and deep backend implementation. Splits time between osabiohq/osabio (a companion project, likely the go-to-market or client-facing product) and marcus-sa/brain (the platform core).

## Technical seniority (inferred)

Senior-to-principal full-stack engineer with strong systems-thinking instincts. Evidence:
- Designs and critiques distributed systems architecture (Observer agent, Proxy, IAM/DPoP/RAR, graph relationships)
- Reads SurrealDB schema errors from stack traces and fixes them himself
- Knows OAuth 2.0 protocol internals well enough to question why the MCP SDK's built-in OAuth client wasn't used
- References concurrency concepts (`mutex vs semaphore`) without context — exploring at the edges
- Spots when an abstraction is redundant before the agent does
- Runs parallel agents via Conductor and coordinates their output

## Attitude toward the agent

**Demanding but trusting.** He delegates large autonomous tasks (entire feature waves via `/nw:deliver`) and expects the agent to read docs, check tests, follow AGENTS.md conventions — without hand-holding. When the agent misses something he corrects precisely and moves on; he doesn't explain his reasoning unless pressed. He treats the agent as a capable junior colleague who should just know to check related files.

**Skeptical of over-engineering.** He pushes back when the agent adds complexity: "this is super convoluted....", "eliminate whats not needed", "it should not depend on onboarding either". His reflex is to simplify, not abstract.

**Product-opinionated.** He holds strong views on naming ("shouldnt we rename the orchestrator agent to chat agent? because that's literally what it is"), on architecture (prefers server-side over client-side state), and on quality ("lmao, these integration tests are inherntly useless").

## Communication style in longer messages

When he writes more than ~30 words it is usually:
- A spec dump (pasted from a design doc or issue)
- A numbered correction
- A question probing a design decision he suspects is wrong

He never writes pleasantries, never thanks the agent, never wraps up with "let me know if you need anything."
