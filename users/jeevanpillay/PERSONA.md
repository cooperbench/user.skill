# Persona — jeevanpillay

## Role and background

**Founder / lead engineer** (inferred) of `lightfastai` — an AI-native developer tooling company. Builds both the product (`lightfast`) and the internal autonomous coding agent (`climode`) that implements `lightfast`. This means he is simultaneously the product designer, architect, and the operator of the AI system.

Operates on macOS (evidenced by "option + k in mac", `/private/tmp/claude-501/` paths in task notifications, Clerk OAuth routes).

## Expertise

- **TypeScript / Next.js monorepo**: Fluent. Knows tRPC, Tanstack Query, Inngest, Clerk, Sentry, Biome, Turborepo, oRPC, SuperJSON, Radix UI, Tailwind deeply.
- **Observability and error architecture**: Spends significant effort on Sentry integration, correlation IDs, tRPC middleware, structured logging (pino), and async error propagation.
- **AI-native workflows**: Designs autonomous planning loops (`Ralph`), state-machine agents, spec-driven implementation pipelines.
- **Product intuition**: Evaluates architecture against "mission goals", "long-term maintainability", and "developer productivity" — not just correctness.

## Seniority signals

- References advanced patterns (neverthrow, edge-native nanoid, ALS context propagation, pinecone embeddings) without explanation.
- Pushes back on nullable orgId as "code smells all throughout our app" — understands downstream consequences.
- Distinguishes between tRPC client vs. server errors and questions Sentry best practices at that boundary.
- Knows git history rewriting (`filter-branch`/`filter-repo`) and force-pushes across branches as routine.

## Attitude toward the agent

**Trusting but impatient.** Delegates large, multi-phase implementation entirely to the agent without step-by-step supervision. Doesn't ask for explanations unless something looks wrong. Will interrupt mid-execution without warning. Validates output with "nice", "beautiful!", "it worked! nice." — brief positive signals before moving on. Escalates to "ultrathink" when dissatisfied rather than providing detailed critique. Challenges agent architectural opinions with "are you 100% sure of these concerns?" and "re-evaluate."

Treats the agent as a fast pair programmer who should already know the codebase, not a tool that needs hand-holding.
