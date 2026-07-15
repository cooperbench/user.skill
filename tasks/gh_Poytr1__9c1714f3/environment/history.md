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

> DEVELOPER

But we found a bug that after acknowledging the latest, the older one still pops up why?

> AGENT

Let me dig into the cascade logic to find the bug.

> TOOL

tool_use Read
id: toolu_bdrk_01CxHGS3FuBfbdyJfWXLWqVr
```json
{
  "file_path": "/Users/pc/web3/ReleaseBeacon/internal/api/pgstore.go",
  "offset": 1640,
  "limit": 100
}
```

> TOOL

tool_result
id: toolu_bdrk_01CxHGS3FuBfbdyJfWXLWqVr
```
1640			&t.CreatedAt, &t.AcknowledgedAt, &t.ResolvedAt,
1641			&t.ProjectID, &t.ProjectName, &t.Version, &t.Provider, &t.Repository, &t.TodoType, &t.Urgency, &t.ReleasedAt,
1642		)
1643		if err != nil {
1644			return nil, fmt.Errorf("get todo: %w", err)
1645		}
1646		return &t, nil
1647	}
1648	
1649	func (s *PgStore) AcknowledgeTodo(ctx context.Context, id string, cascade bool) error {
1650		tag, err := s.pool.Exec(ctx,
1651			`UPDATE release_todos SET status = 'acknowledged', acknowledged_at = NOW() WHERE id = $1`, id)
1652		if err != nil {
1653			return fmt.Errorf("acknowledge todo: %w", err)
1654		}
1655		if tag.RowsAffected() == 0 {
1656			return fmt.Errorf("todo not found")
1657		}
1658	
1659		if cascade {
1660			// Also acknowledge older pending todos for the same source/project.
1661			_, _ = s.pool.Exec(ctx, `
1662				UPDATE release_todos SET status = 'acknowledged', acknowledged_at = NOW()
1663				WHERE id != $1 AND status = 'pending'
1664				AND (
1665					(release_id IS NOT NULL AND release_id IN (
1666						SELECT r2.id FROM releases r2
1667						JOIN releases r1 ON r1.source_id = r2.source_id
1668						JOIN release_todos t1 ON t1.release_id = r1.id
1669						WHERE t1.id = $1 AND r2.created_at <= r1.created_at AND r2.id != r1.id
1670					))
1671					OR
1672					(semantic_release_id IS NOT NULL AND semantic_release_id IN […]

> AGENT

Now let me check how todos are created — specifically whether new todos are created for releases that come in *after* the acknowledge action, which would bypass the cascade.

> TOOL

tool_use Grep
id: toolu_bdrk_01Qi7zUWMRG13iNCw4MvhSNo
```json
{
  "pattern": "CreateReleaseTodo|CreateSemanticReleaseTodo",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_bdrk_01Qi7zUWMRG13iNCw4MvhSNo
```
Found 9 files
internal/stealth/store_test.go
internal/stealth/store.go
internal/routing/worker.go
internal/api/pgstore.go
internal/agent/orchestrator.go
docs/plans/2026-04-01-stealth-mode-plan.md
internal/agent/orchestrator_test.go
internal/routing/worker_test.go
docs/plans/2026-03-10-todo-feature.md
```

> TOOL

tool_use Grep
id: toolu_bdrk_01LV448DiaugMxbK8EVdZ21G
```json
{
  "pattern": "CreateReleaseTodo|CreateSemanticReleaseTodo",
  "path": "/Users/pc/web3/ReleaseBeacon/internal/routing/worker.go",
  "output_mode": "content",
  "-C": 5
}
```

> TOOL

tool_result
id: toolu_bdrk_01LV448DiaugMxbK8EVdZ21G
```
22-	ListSourceSubscriptions(ctx context.Context, sourceID string) ([]models.Subscription, error)
23-	GetChannel(ctx context.Context, id string) (*models.NotificationChannel, error)
24-	GetProject(ctx context.Context, id string) (*models.Project, error)
25-	GetPreviousRelease(ctx context.Context, sourceID string, beforeVersion string) (*models.Release, error)
26-	EnqueueAgentRun(ctx context.Context, projectID, trigger, version string) error
27:	CreateReleaseTodo(ctx context.Context, releaseID string) (string, error)
28-	HasReleaseGate(ctx context.Context, projectID string) (bool, error)
29-}
30-
31-// NotifyWorker is a River worker that processes NotifyJobArgs.
32-// It looks up the release, finds all source-level subscriptions, resolves
--
107-			}
108-		}
109-	}
110-
111-	// Create a TODO for this release (idempotent — safe for retries).
112:	todoID, todoErr := w.store.CreateReleaseTodo(ctx, release.ID)
113-	if todoErr != nil {
114-		slog.Error("create release todo failed", "release_id", release.ID, "err", todoErr)
115-		// Continue — notification delivery is primary responsibility.
116-	}
117-
```

> AGENT

I see the issue. Let me check if the `CreateReleaseTodo` respects previously acknowledged state — i.e., if you acknowledge the latest, and then a *re-notification* or retry creates a todo for an older release, does it skip it?

> TOOL

tool_use Read
id: toolu_bdrk_01LAf9xFepRn6b7FLwn5nmio
```json
{
  "file_path": "/Users/pc/web3/ReleaseBeacon/internal/api/pgstore.go",
  "limit": 30,
  "offset": 1731
}
```

> TOOL

tool_result
id: toolu_bdrk_01LAf9xFepRn6b7FLwn5nmio
```
1731	// CreateReleaseTodo inserts a TODO for a source release. Returns the todo ID.
1732	// Uses ON CONFLICT DO UPDATE for idempotency.
1733	func (s *PgStore) CreateReleaseTodo(ctx context.Context, releaseID string) (string, error) {
1734		var id string
1735		err := s.pool.QueryRow(ctx,
1736			`INSERT INTO release_todos (release_id) VALUES ($1)
1737			 ON CONFLICT (release_id) WHERE release_id IS NOT NULL DO UPDATE SET release_id = EXCLUDED.release_id
1738			 RETURNING id`, releaseID).Scan(&id)
1739		if err != nil {
1740			return "", fmt.Errorf("create release todo: %w", err)
1741		}
1742		return id, nil
1743	}
1744	
1745	// CreateSemanticReleaseTodo inserts a TODO for a semantic release. Returns the todo ID.
1746	// Uses ON CONFLICT DO UPDATE for idempotency.
1747	func (s *PgStore) CreateSemanticReleaseTodo(ctx context.Context, semanticReleaseID string) (string, error) {
1748		var id string
1749		err := s.pool.QueryRow(ctx,
1750			`INSERT INTO release_todos (semantic_release_id) VALUES ($1)
1751			 ON CONFLICT (semantic_release_id) WHERE semantic_release_id IS NOT NULL DO UPDATE SET semantic_release_id = EXCLUDED.semantic_release_id
1752			 RETURNING id`, semanticReleaseID).Scan(&id)
1753		if err != nil {
1754			return "", fmt.Errorf("create semantic release todo: %w", err)
1755		}
1756		return id, nil
1757	}
1758	
1759	// --- Onboard Store ---
1760	

<system-reminder>
Whenever you read a file, […]

> AGENT

Now let me check the cascade query more carefully. The issue is in the cascade condition — it uses `r2.created_at <= r1.created_at`. But what if the "older" release's `release_todos.release_id` is NULL (i.e., the todo is a semantic_release todo, not a release todo)? The `OR` branches are mutually exclusive based on which ID is set. Let me look at a different angle — what if the problem is that some todos have a `semantic_release_id` and others have a `release_id` for the same project?

> TOOL

tool_use Grep
id: toolu_bdrk_01GeZF7G9ZScxkHvyrbZyvUV
```json
{
  "pattern": "release_todos",
  "glob": "*.sql",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_bdrk_01GeZF7G9ZScxkHvyrbZyvUV
```
No files found
```

> TOOL

tool_use Grep
id: toolu_bdrk_01CTHgskEp2W8WCg59GKGFxY
```json
{
  "glob": "*.go",
  "output_mode": "content",
  "pattern": "CREATE TABLE release_todos|release_todos\"",
  "path": "/Users/pc/web3/ReleaseBeacon/internal"
}
```

> TOOL

tool_result
id: toolu_bdrk_01CTHgskEp2W8WCg59GKGFxY
```
No matches found
```