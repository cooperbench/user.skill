---
name: error-dump-silent
description: When something breaks, user pastes raw terminal/browser output with zero commentary — the paste IS the bug report
---

The user does not explain what they were doing, does not say "I got this error", does not ask a question. The raw artifact is the entire message. Sometimes the error message is duplicated (copy-pasted from a toast that repeated). Sometimes a single stray character ("c") appears at the end as an accidental keystroke.

**Trigger**: any runtime failure — server error, TypeScript compile error, browser JS exception, API returning wrong content type.

**Pattern**:
```
<raw terminal output or browser error, verbatim>
```

**Examples**:
> `Failed to load patterns`
> `Error: Failed to load patterns`

> `Failed to load trends`
> `Error: Unexpected token '<', "<!doctype "... is not valid JSON\`
> `Failed to load trends`
> `Error: Unexpected token '<', "<!doctype "... is not valid JSON`

> `installHook.js:1 TypeError: Cannot read properties of undefined (reading 'length')`
> `    at sme (index-BNFdBs5N.js:231:46440)\`
> `    if (e.snapshots.length === 0)`

> `[background] Git available - will extract git metadata`
> `2026-02-25T15:12:30.299Z [INFO] [pagerank] PageRank cache invalidated`
> `[background] Embedding 286/286...`
> `[background] Code index failed: Found field not in schema: metadata at row 0`
> `c`

The agent is expected to diagnose and fix without being told what broke.
