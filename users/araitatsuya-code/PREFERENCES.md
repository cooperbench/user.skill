# PREFERENCES — araitatsuya-code

## What Triggers Correction (22% of prompts)

**1. Agent reports "done" without updating downstream state.**  
After every merge the agent must update issue status and docs. If it doesn't, user immediately prompts:  
> "マージしたのでissueとdocの状態を更新して"  
This pattern repeats verbatim — it is a known gap the user has learned to plug manually.

**2. Agent presents output in a table or markdown format when plain text is needed.**  
User corrects to: "コピペしやすい形式で出して欲しい". Wants output they can paste without cleanup.

**3. Agent addresses optional suggestions alongside required fixes.**  
User cuts scope: "MUSTとSHOULDのみ対応して" — only mandatory items, ignore suggestions.

**4. Agent implementation has architecture violations.**  
When the agent introduces a Clean Architecture violation (e.g., `app.go` importing `internal/infrastructure` directly), user catches it and requests a precise fix specifying the exact interface/DI pattern to use.

**5. Agent produces a PR summary instead of the PR body itself.**  
User wants copy-pasteable output, not a narrative summary of what was done.

## What Satisfies Them

- Agent picks up the next issue and runs the full implement → test → PR cycle without hand-holding.
- Tests cover the right surface: Go table-driven + mock interfaces, React Vitest + act()-wrapped Zustand.
- PRs are small enough to match "1PR = 1Issue" granularity.
- Agent handles GitHub PR review response end-to-end (fetches inline comments, replies, fixes).

## Workflow Habits

- **Issue-driven, phase-labeled.** Work is organized into phases (phase-1, phase-2, …) with GitHub labels. The agent is given one phase at a time via `/next-issue`.
- **Docs as spec.** Implementation references `docs/` directory for specs — the agent is expected to read `docs/04-TASK-LIST.md` etc. without being told each time.
- **Commit message convention.** `refs #<番号>` in commit messages — enforced via slash command templates.
- **Branch naming.** `issue-<番号>-<slug>` — also enforced via templates.
- **No planning step visible.** User doesn't ask "should we do X or Y?" — issues are pre-planned; agent just executes.
- **Interrupts freely.** Cancels agent mid-task when it's heading somewhere wrong; then reissues a tighter command.
- **Asks agent to memorize patterns.** When a workflow (e.g., PR review response) is repeated, asks the agent to save it as a skill or to memory: "ghのレビュー対応をskillにするかコメント返信方法などを記憶しておいて".

## Stack Preferences (from prompts)

- **Go**: Clean Architecture, table-driven tests, repository interface mocks, `go test -v ./internal/...`
- **React**: Vitest + React Testing Library, Zustand (`useShallow` for selector subscriptions), `cd frontend && npx vitest --run`
- **GitHub CLI**: `gh issue list`, `gh issue create`, `gh pr create`, `gh api` for inline comments
- **Wails**: desktop app framework bridging Go backend and React frontend
- **SQLite**: via `go-sqlite3` + `golang-migrate`

## Explanation Preference

Does not ask for explanations of what was done. Reads the diff. Will ask "この記述は？" for something surprising in config, but otherwise wants results, not narration.
