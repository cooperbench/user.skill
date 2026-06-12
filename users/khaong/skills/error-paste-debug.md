---
name: error-paste-debug
description: When something fails, khaong pastes the raw output — error text, log lines, git output, test failure paths — with minimal or zero explanatory commentary, then either asks a targeted question or just lets the paste speak for itself.
---

# Error Paste Debug

khaong does not paraphrase errors. They paste the exact terminal output and may append a single short observation or question, or nothing at all.

This applies to: git failures, CI log links, E2E artifact paths, JSON log dumps, hook output, test runner output.

## Patterns

- Raw error + "HALP" (rare, signals genuine alarm)
- Raw error + "why?" (most common diagnostic opener)
- CI link only (agent is expected to fetch and triage)
- Artifact directory path only ("next run: /Users/alex/workspace/cli/e2e/artifacts/2026-02-26T14-20-34")
- Verbose JSON log dump + specific question about one field
- Repeating the error hash to add context: "it also always seems to be this same hash, I think? > git status / fatal: unable to read e53647ba..."

## Examples

After git gc fails:
> `> git gc`
> `fatal: bad tree object 082c2c4495629bd585a0a11807b4e0ede9a99753`
> `fatal: failed to run repack`
>
> `HALP`

After a CI run fails:
> `main branch tests failing - why? https://github.com/entireio/cli/actions/runs/21662191208/job/62449194626`

After a worktree issue:
> `uh oh - it just happened again`
>
> `I did a git read-tree HEAD to resolve`

After the stop hook dumps logs:
> `I did a add/commit/push... then the stop hook barfed after the file copies to .entire/metadata`

Pointing to a new artifact run:
> `next run: /Users/alex/workspace/cli/e2e/artifacts/2026-02-26T14-20-34`
