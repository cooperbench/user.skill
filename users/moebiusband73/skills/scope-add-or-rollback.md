---
name: scope-add-or-rollback
description: >
  Trigger: agent completes a change but missed a related update (ReleaseNotes, docs, config
  schema), OR agent added something the user didn't want. User either extends scope with "Also
  …" or rolls it back with a terse reversal command.
---

## Scope addition ("Also …")

When the agent finishes code but omits a documentation or config-schema update, the user
adds it with a short "Also" sentence. This is the #1 correction pattern (16.8% of prompts).

**Examples:**
> `Also update the ReleaseNotes with the recent changes`

> `Also add a section in the README.md discussing and documenting the new db options.`

> `Also updaten the documentation and config schema to reflect the new options`

> `Also set MinimumPoints automatically based on the policy`

> `Also add a notice about the new checkpointreader tool to the ReleaseNotes`

## Scope rollback (terse reversal)

When the agent adds something the user didn't ask for, the user removes it with a short
imperative — often referencing the exact feature by name.

**Examples:**
> `Remove Queue group support again`

> `Consolidate all migrations after 10 to one migration 11.`

> `Make the checkpoints option also option also optional`
(Typo-laden but clear intent: make the field optional in the schema.)

## Pattern

Additions use "Also". Rollbacks use a direct imperative without "Also". Both are short
(3–12 words). Neither explains why — the user expects the agent to understand from context.
