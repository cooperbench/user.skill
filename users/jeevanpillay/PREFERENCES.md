# Preferences — jeevanpillay

## Pushback distribution

| Type | Rate |
|---|---|
| non_pushback | 65.5% |
| correction | 28.3% |
| failure_report | 3.5% |
| rejection | 2.7% |

Corrections are the dominant friction. Most are small redirects mid-flow, not full rejections.

## What triggers corrections

- **Wrong linter**: Agent uses ESLint → "no eslint. its' biome. correct type that. any is bad."
- **Committing secrets**: Agent includes `.vercel/.env.development.local` → "hmm did you say .vercel/.env.development.locao?"
- **Nullable types as solutions**: "rethink this. orgIg nullable + create pending are both imo bad solutions. nullable orgId in gatewayInstallation will cause code smells all throughout our app."
- **Incomplete scope**: Agent commits only the feature branch files, user wants broader: "i think we should commit the answer message sidebar avatar searcn all that too. basically all the stuff expect for the thought"
- **Overconfident agent claims**: "are you 100% sure of these concerns?" — challenges agent when it sounds definitive without sufficient evidence.
- **Agent explains too much before acting**: User interrupts with "[Request interrupted by user for tool use]" or re-issues the command directly.
- **Architecture misses the vision**: Agent proposes a pragmatic solution, user wants "the most superintelligent infrastructure" / "100x improvement".
- **Not cleaning up symlinks**: "dont forge tto clean up symlik in @.claude/skills/"
- **Research when user wants code**: "do not run research. just create this route for me."

## What triggers rejections

- Agent about to commit but user has changed their mind: "undo. no! im fixeing the keys."
- Agent's research result seems stale/wrong: "okay i think this is my browser error. all good. delete resrach"
- Agent does git without user triggering it at wrong time: "run commit again" (rejection → retry)

## What satisfies

- Brief, confident summaries before merging
- Phased implementation with verification between phases
- Following existing patterns from other files in the codebase
- `/oneshot_merge` succeeding cleanly
- Build/typecheck passing

## Workflow habits

**Plan-first, always.** The sequence is invariant:
1. `/research_codebase` to investigate
2. `/create_plan` from research doc
3. `/improve_plan` if needed
4. `/implement_plan` (phase by phase or all at once)
5. `/oneshot_merge` to ship

**Does not write code directly** in prompts — delegates all implementation to the agent through plan files stored at `@thoughts/shared/plans/` and `@thoughts/shared/research/`.

**No explanations needed** — doesn't ask "how does X work?" unless there's a discrepancy to investigate. When curious, asks as a one-line question: "question, when does this become it's own 'pinecone' pipeline?"

**Interrupts freely** — will cut off an agent mid-task if the direction looks wrong or a better idea surfaces. No apology.

**Test cadence**: Rarely asks for unit tests. Validates via "build/check/typechcek" (Turborepo build + Biome lint + tsc). No test-driven approach — ships and verifies via Sentry/dev server.

**Commit style**: Delegates to `/oneshot_merge` and `/commit`. Never writes commit messages manually. Expects the agent to handle branching and PRs.

**Stack non-negotiables** (inferred from corrections):
- Biome (not ESLint) for linting
- Radix UI primitives
- tRPC for API layer
- Never commit `.env` files
- No nullable orgId / no pending states as workarounds
- Co-Authored-By must be preserved in git history rewrites
