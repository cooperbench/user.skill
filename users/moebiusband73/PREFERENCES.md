# Preferences: moebiusband73

## Pushback distribution

| Type | Rate | Meaning |
|------|------|---------|
| non_pushback | 74.3% | Accepts and continues |
| correction | 16.8% | Redirects agent with new/modified instruction |
| failure_report | 6.9% | Pastes logs; agent missed something in production |
| takeover | 2.0% | Does git operation himself |

## What triggers corrections

1. **Agent omits a related doc/release-notes update.** Agent finishes code; user adds:
   `"Also update the ReleaseNotes with the recent changes"`. Happens repeatedly.
2. **Agent adds scope the user didn't ask for.** Immediate rollback:
   `"Remove Queue group support again"`.
3. **Agent's technical explanation is subtly off.** User probes with "Why" chain:
   `"Why is the option cache-size-mb set to DB size / max-open-connections and not to DB size."`
4. **Agent summary diverges from what user sees in production.** Pasted log with numbers
   contradicting the agent's claim triggers "Investigate the issue and fix it."
5. **Agent uses old/file-based approach when a policy-based one exists:**
   `"What about the policy based approach? Investigate and also replace the file based
   configuration with the resample method and policy as done in the API already."`

## What triggers failure reports

- Regressions between sessions: performance degradation, startup time blowup, timeout in prod.
- Logs always pasted verbatim with actual timing numbers and file:line references.
- No apology or softening; just the log and "Investigate the issue and fix it."

## What triggers takeover

- Git commit when agent seems to be stuck in a loop or hasn't committed after completing work.
  `"commit it"` appears twice as takeover; the user apparently just ran it himself.

## What satisfies

- Silent acceptance: no follow-up = success.
- Short positive confirmation is rare; `"Yes please add a clarification to the README"` is
  about as warm as it gets.
- Agent moving to "commit it" prompt is the signal the user considers implementation done.

## Workflow habits

- **Plan-before-execute.** Writes exhaustive plans in plan mode, then opens a session with
  `"Implement the following plan:"` and the full plan text. Almost never improvises a large
  change without a pre-written plan.
- **Session turns are short.** Median 2 turns, median duration ~5 min. Most sessions:
  plan dump → agent executes → user says "commit it" or corrects once.
- **Commits are terse and frequent.** Uses agent for commits with `"commit it"` / `"commit the
  changes"` / `"commit this"`. Occasionally does it manually (takeover).
- **No test-driven development.** Test intent is 0.9%; tests appear in verification blocks
  inside plans (`go test ./...`) but the user rarely asks for new tests.
- **Documentation is in scope.** Every significant code change is expected to update
  ReleaseNotes, README, and/or config schema. Agent omitting these is the #1 correction trigger.
- **Release management cadence.** Regularly opens sessions to update ReleaseNotes, set
  migration version numbers, add sections for upcoming releases (1.5.1, 1.5.2, 1.5.3).
- **Config schema kept in sync.** Changes to struct fields must be reflected in JSON schema;
  agent is expected to do this without being told — if it doesn't, user adds `"Also updaten
  the documentation and config schema to reflect the new options"`.
- **Explain on request only.** Does not ask for explanations by default. When curious:
  `"Explain how Fix 3 works and why this is an improvement"`.

## Stack preferences (evidenced)

- Go (primary language)
- SQLite with direct PRAGMA tuning (not an ORM abstraction fan)
- NATS for messaging
- Parquet for cold storage
- WAL format preferred over JSON for checkpoints (explicitly changed default)
- GraphQL (gqlgen) for API
- Svelte for frontend (mentioned indirectly)
- `squirrel` query builder
