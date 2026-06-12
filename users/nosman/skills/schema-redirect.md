---
name: schema-redirect
description: >
  Trigger: agent uses a stale or wrong DB table/model after a schema migration.
  nosman names the wrong entity, names the correct one, and issues the refactor as a single sentence.
---

# schema-redirect

After a DB schema migration, nosman checks the live data and catches when the agent still
references the old table. He does not explain the migration history — he just names both the
wrong entity and the correct replacement, then tells the agent to refactor.

The correction is concise (one or two sentences). He does not soften it or ask why it happened.

## Verbatim examples

```
The controller is fetching from the OLD checkpointSession table. Instead of using that table, we should be using the new V2 tables, in this case CheckpointSessionMetadata. Refactor the sessions UI and controller to use this new table.
```

```
Now that we're using the CheckpointSessionMetadata models, let's get the summary field from CheckpointSessionMetadata.Summary.Intent, and rename the summary table column to intent.
```

```
The sessions field should be a one-to-many relationship with SessionLink, so add a foreign key from SessionLink into CheckpointMetadata. Create a foreignKey form CheckpointMetadata to tokenUsage for the token_usage field. Finally, create a join table from SessionLink to FilePath for the files_touched field.
```

Note: he also self-corrects when he gives the agent wrong information:

```
I gave you the wrong file structure, here is the real one: 3c/e589c58321/
└── 0/
    ├── content_hash.txt
    ...
```
