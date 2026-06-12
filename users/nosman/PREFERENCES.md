# nosman — Preferences

## What he corrects (51% of turns are corrections)

- **Wrong DB table or data source**: catches the agent using an old table after a schema migration;
  always names the correct model explicitly ("use CheckpointSessionMetadata, not checkpointSession")
- **Scope creep or unnecessary complexity**: will redirect if the agent over-engineers a solution
- **UI layout and visual hierarchy**: corrects spacing, borders, colors, font weight, element
  positioning with specific language ("get rid of the line", "make the background white",
  "file tree should be UNDER the open items and side-by-side with the dialog")
- **Wrong assumptions about uniqueness or relationships**: corrects DB constraint design
  ("It should not be unique. Each session can have multiple checkpoints and commits.")
- **Direction changes after seeing result**: pivots entire tech stack when a new option seems
  better ("I think electron would be a better fit")
- **Server/process state**: notices when server is stale and asks for restart; notices when the
  wrong branch or process is being targeted

## What triggers failure reports (13.8%)

- UI not working as expected after a "done" claim ("the checkpoints ui is not updating anymore")
- Visual bugs visible on screen ("still bad on dark mode: [Image: image/png]")
- Missing data in the DB that should be present ("i still see ellipses")
- Scrolling / navigation not functioning

## What satisfies him

- Single-word acceptances: `yes`, `ok`
- Occasionally extends with next instruction immediately: "Great now create a new tab..."
- Silence (no pushback) = accepted
- Rarely gives explicit praise; acceptance is functional

## Workflow habits

- **Planning-first for large features**: writes or pastes a full architecture plan before
  implementation; plan includes file-by-file action table, code snippets, interface specs
- **Open items as a bug/TODO tracker**: maintains a running list of open items, delegates them
  via "Please work on the following open items:" — a recurring structured handoff pattern
- **Operational commands are frequent**: `restart the server`, `start the app`, `git status`,
  `run the new subcommand` — treats the agent as a terminal operator, not just a coder
- **Tests by observation**: asks the agent to run the server, then checks the live UI himself;
  rarely asks for unit tests (test intent: 1.7%)
- **Interrupts freely**: cancels mid-execution when direction changes; `[Request interrupted by user]`
  appears multiple times across sessions
- **Does not ask for explanations**: understand intent is 10.8% — he asks "why" occasionally when
  something looks wrong, not to learn but to diagnose
- **Commits infrequently during sessions**: git intent is 3.5%; mostly asks "what recently changed"

## Tool and stack preferences

- **Electron** over web-only frameworks (pivoted from Expo to Electron for desktop access)
- **Mantine** as UI component library ("Let's use mantine whenever we can moving forward")
- **SQLite + Prisma** for structured data (migrated from NDJSON flat files)
- **TypeScript** throughout (all specs use `.ts`/`.tsx` extensions)
- **Express + WebSocket** for the local API server
- **No unit tests** — validates by running the live app
- **FTS5** for full-text search in SQLite
- **diff2html** for showing diffs (though pushed back on dark mode styling)
- **Markdown rendering** done properly, not raw strings ("render it properly instead of as a raw string")

## Pushback distribution

| Type | Rate |
|---|---|
| correction | 51.1% |
| non_pushback | 35.2% |
| failure_report | 13.8% |
