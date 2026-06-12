---
name: spec-dump-kickoff
description: For large architectural refactors, user opens with a full pre-written markdown spec (200–600 words) covering context, unified interface design, file-by-file changes. Trigger: session opening for a major refactor where the plan is already decided.
---

# spec-dump-kickoff

For major refactors, ravwojdyla writes the entire plan ahead of the session and pastes it as the opening message. The spec is structured markdown with headers (`## Context`, `## Unified ClassName`, `### 1. file/path.py`), Python code blocks showing the target interface, and bullet lists of file-level actions.

The opening line is always a command: `"Implement the following plan:"`.

## Structure of spec dumps

1. `# Plan: <Title>` as a heading
2. `## Context` — why the change is needed
3. `## Unified <Class/Interface>` — target API as a Python code block
4. `### 1. <file_path>` through `### N. <file_path>` — per-file bullet actions
5. Sometimes ends with a `## Steps` section listing the order of operations

## Verbatim example (opening line + structure)

> `"Implement the following plan: # Plan: Merge StepMeta into StepSpec, delete step.py ## Context The execution framework has three layers: `StepMeta` (identity/hashing), `StepSpec` (meta + fn + resources), and `Step` (deferred execution). The `Step` API (`step.py`) with its `defer`/`resolve_deferred` machinery is being removed as too magic..."`

## Notes

- The spec is entirely pre-written; the user does not draft it live in the session.
- After the dump, mid-session messages revert to terse `"ok,"` corrections.
- The spec represents the user's final decision — agent is not expected to question the design.
