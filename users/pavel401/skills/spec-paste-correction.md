---
name: spec-paste-correction
description: How Pavel401 corrects the agent when output is wrong or incomplete — pastes a precise spec referencing exact file paths and line numbers, or pastes CodeRabbit/external review output and asks for fixes.
---

# spec-paste-correction

When the agent's output misses the mark, Pavel401 does not give vague feedback. He either:
1. Writes a surgical correction citing `@file.py:line` format, or
2. Pastes structured output from an external tool (CodeRabbit, BugViper itself) verbatim and asks the agent to implement the changes.

He never re-explains the whole context — he assumes the agent retains it.

## Pattern

- Corrections reference exact file paths and line numbers: `In \`@api/routers/ingestion.py\`: - Line 41: ...`
- He may paste a plan.md / table format spec he wrote offline, then say "implement this"
- When pasting CodeRabbit output, he asks "DO in line comments with code as well ." or "Verify each finding against the current code and only fix it if needed."

## Examples

**Example 1** — surgical line-level correction:
```
In `@api/routers/ingestion.py`:
- Line 41: The code accesses user["uid"] directly which can raise KeyError; change the extraction in the ingestion route to use user.get("uid") and add an explicit check that uid is present (e.g., if not uid: raise an HTTPException/return a clear error), or update get_current_user to return a typed model (e.g., a Pydantic User model) guaranteeing uid and then read user.uid; ensure the change touches the uid assignment and any downstream uses so missing or invalid uid yields a clear, handled error rather than an unhandled KeyError.
```

**Example 2** — pasting CodeRabbit output and asking for fix:
```
`18-30`: **`github_access_token` is stored in plaintext in Firestore.**
...
DO in line comments with code as well .
```

**Example 3** — specifying a new behavior with UX detail:
```
Once I click on the start it should automatically create the repo document in the firestore with the status as syncing . When synced it should be synced , if failed it should be failed . After clicking the start it should close the fialog and push the repo to ingested with the badge and Ingesting circular loader . Make the flow minimal and clean UX
```

**Example 4** — pasting structured plan sections as correction:
```
## Files to Modify

| File | Section | Change |
|---|---|---|
| `deepagent/models/agent_schemas.py` | 1 | Add `confidence`, `ai_fix` to `Issue`; add `FileSummary`; extend `ReviewResults` |
...
```
