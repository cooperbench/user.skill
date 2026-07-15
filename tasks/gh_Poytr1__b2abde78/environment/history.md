> DEVELOPER

In the todo page, for "Ackowledge/resolve" it should automatically ack and resolve all the historic releases, has it already been implemented?

> AGENT

Let me check the current implementation of the acknowledge/resolve functionality in the todo page.

> TOOL

tool_use Agent
id: toolu_bdrk_01H7edxjDUMZuhM3HREamvbg
```json
{
  "description": "Explore todo page ack/resolve",
  "subagent_type": "Explore",
  "prompt": "In this project, find the \"todo\" page implementation in the web/ frontend directory. I need to understand:\n1. What does the \"Acknowledge\" or \"Resolve\" action do when clicked?\n2. Does it only ack/resolve the single release, or does it also automatically ack/resolve all older/historic releases for the same project?\n3. What API endpoint does it call, and what does the backend handler do?\n\nSearch for relevant code in web/src/ (components, pages, hooks related to \"todo\", \"ack\", \"resolve\", \"acknowledge\") and in the Go backend (API handlers for ack/resolve). Be thorough - check both frontend and backend.",
  "model": "sonnet"
}
```

> TOOL

tool_result
id: toolu_bdrk_01H7edxjDUMZuhM3HREamvbg
```
Here is a complete picture of how the Acknowledge and Resolve actions work, from UI through to database.

---

## Todo page: Acknowledge / Resolve flow

### Relevant files

- `/Users/pc/web3/ReleaseBeacon/web/app/todo/page.tsx` — the page component
- `/Users/pc/web3/ReleaseBeacon/web/lib/api/client.ts` — frontend API client
- `/Users/pc/web3/ReleaseBeacon/internal/api/todos.go` — HTTP handlers
- `/Users/pc/web3/ReleaseBeacon/internal/api/server.go` — route registration
- `/Users/pc/web3/ReleaseBeacon/internal/api/pgstore.go` — database implementation

---

### 1. What does each button do?

The page renders different action buttons depending on the current filter status:

**When viewing `pending` todos:**
- **Acknowledge** — calls `handleAcknowledge(id)`, which always passes `cascade = true`
- **Dismiss** — opens a confirmation dialog then calls `handleResolve(id, false)` (cascade is explicitly `false`)

**When viewing `acknowledged` todos:**
- **Resolve** — calls `handleResolve(id)` with default `cascade = true`
- **Undo** — confirmation dialog then calls `handleReopen(id)` (moves back to pending)

**When viewing `resolved` todos:**
- **Reopen** — confirmation dialog then calls `handleReopen(id)`

---

### 2. Does it cascade to older releases?

**Yes for Acknowledge (from pending view)** — `cascade = true` is hardcoded:
```ts
await todosApi.acknowledge(id, true);  // cascade always true
```

**No for Dismiss** — `cascade = false` is hardcoded:
```ts
onConfirm: () => handleResolve(todo.id, false),  // cascade explicitly false
```

**Yes for […]

> AGENT

Yes, it's already implemented. When you click **Acknowledge** on a pending todo, it passes `cascade=true`, which makes the backend automatically acknowledge all older pending todos for the same source/project. Similarly, **Resolve** from the acknowledged view cascades to all older pending and acknowledged todos.

The only action that doesn't cascade is **Dismiss**, which explicitly sets `cascade=false` to only affect the single release.