---
name: plan-command-kickoff
description: How jeevanpillay opens a session — fires a slash command pointing at a plan or research file, with zero preamble. Trigger when starting a new task or session with this user.
---

jeevanpillay almost never opens a session with prose. The first message is either a bare slash command with an `@`-file arg, or a short imperative pointing to a plan. He never explains context — the plan file contains it.

**Patterns**:
- `/implement_plan @thoughts/shared/plans/<date>-<slug>.md`
- `/create_plan @thoughts/shared/research/<date>-<slug>.md`
- `/research_codebase <inline question referencing @files>`
- `/improve_plan @thoughts/shared/plans/<date>-<slug>.md <optional constraint>`
- `/oneshot_merge` (to kick off a merge session with no other context)

**Examples**:

```
/implement_plan @thoughts/shared/plans/2026-04-07-dotlightfast-context-indexing.md
```

```
/create_plan @thoughts/shared/research/2026-04-05-trpc-client-error-propagation-next-step.md for both apps/platform and apps/app
```

```
/improve_plan @thoughts/shared/plans/2026-04-07-dotlightfast-context-indexing.md also ensure better naming and ensure that this will eventually allow us to migrate easily to full dynamic repo style + pinecone embedding for the whole of the repo for data.
```

When he does open with prose, it's a one-liner imperative referencing file paths:
```
find me the events -> entity page resturctre plan/research
```

```
proceed with deep rename of "codemode" to "climode"
```
