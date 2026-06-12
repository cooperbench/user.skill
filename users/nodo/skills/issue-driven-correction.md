---
name: issue-driven-correction
description: Correction by pasting a code review comment verbatim in a triple-backtick block. Triggered whenever nodo has a review finding to address — either from a review agent or from their own read of the diff.
---

When the agent's output has a problem that was identified in a code review (or noticed by nodo directly), nodo does not explain the issue in their own words. They paste the review comment verbatim, wrapped in triple backticks, preceded by a terse directive. They send one issue at a time, with escalating preambles if there are multiple.

**Pattern variants:**

First issue:
```
Fix this comment: ```<review comment text>```
```

Subsequent issues (same session):
```
Another comment: ```<review comment text>```
Another one: ```<review comment text>```
there a few more comments to fix: ```<review comment text>```
```

Direct observation without preamble (when pointing at their own diff):
```
In cmd/entire/cli/strategy/manual_commit_hooks.go I see this diff: ```<diff>``` that doesn't look right, I think we should just take what is present in main and use the `As*` method instead of type assertion
```

**Verbatim examples:**

> `"Fix this comment: \`\`\`Discovery uses context.Background() at startup\n  hooks_cmd.go:29 — Combined with #1, CLI startup hangs for N * forever if N binaries on PATH are unresponsive. Pass a bounded context (e.g., 5s total for\n  discovery).\`\`\`"`

> `"Another one: \`\`\`The reference implementation is missing the get-session-id subcommand, which is listed as \"Always Required\" in the protocol documentation. When the CLI calls GetSessionID(), the binary will print \"unknown subcommand: get-session-id\" to stderr and exit with code 1.\`\`\`"`

> `"there a few more comments to fix: \`\`\`No execution timeout on external binary calls\n  external/external.go:396-425 — The run() method uses exec.CommandContext but 16 callers pass context.Background() with no deadline.\`\`\`"`

> `"please fix the (2) critical issue about limiting stdout"`
