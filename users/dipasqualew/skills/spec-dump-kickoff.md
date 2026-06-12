---
name: spec-dump-kickoff
description: User opens a new task with a complete implementation plan — often 200–685 words of structured markdown. Triggered when starting a major feature or migration.
---

For large new features, dipasqualew writes the full plan themselves (or generates it in a prior session) and pastes it as the opening message, prefixed with "Implement the following plan:" or similar. The plan includes: context section, scope/phases, directory structure in ASCII tree, per-component specs, and a testing strategy.

They do not ask the agent to plan. They plan; the agent implements.

## Example (abbreviated)

```
Implement the following plan: # Plan: Refactor Python Scripts to TypeScript CLI (vibx)

## Context
The vibereq plugin currently uses 4 Python scripts for checkpoint/intent management
and PR reviews. Converting to a compiled TypeScript CLI (`vibx`) will:
- Eliminate Python dependency
- Enable single-binary distribution via `bun build --compile`
- Establish bun monorepo structure for future apps

## Scope
### Python Scripts to Convert
1. `plugins/vibereq/scripts/get-checkpoint-folders.py`
2. `plugins/vibereq/scripts/intent.py`
3. `plugins/vibereq/scripts/get-intents.py`
4. `plugins/vibereq/scripts/run-review.py`

## Implementation
### Phase 1: Monorepo Setup
Create bun workspace structure:
```
vibereq-vibx-app/
├── package.json
├── apps/
│   └── cli/
│       ├── src/
│       │   ├── index.ts
│       │   ├── commands/
│       │   └── lib/
│       └── tests/
```
...
```

The plan may also appear as a mid-session message to restart after a context-limit exit, preceded by a note pointing to the full transcript JSONL file for state recovery.
