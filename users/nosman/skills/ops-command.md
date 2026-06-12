---
name: ops-command
description: >
  Trigger: server needs restarting, app needs launching, or a command needs running.
  nosman issues terse imperative commands to the agent as if it were a terminal operator.
---

# ops-command

nosman treats Claude Code as a shell operator for running the app and server. When he needs
an operational action taken, he issues a short lowercase imperative with no elaboration. These
are not coding tasks — they are live environment management commands.

He also forwards task notification XML blocks verbatim when a background task completes,
expecting the agent to read the output file and continue.

## Verbatim examples

```
restart the server to pick up the backend changes
```

```
restart the server
```

```
start the app again
```

```
run the new subcommand so that we can see the data in sqlite
```

```
First, just run the command to reindex the checkpoints
```

```
git status
```

```
open http://localhost:19006
```

```
migrate --events ~/claude-hooks.ndjson --db ~/.claude/hook-handler.db
```

```
Restart the server so we can test it
```

The pattern is: `[optional short context phrase] + [verb] + [what]`. Never more than one sentence.
When the prior command produced a task notification, he pastes the XML block as the entire message.
