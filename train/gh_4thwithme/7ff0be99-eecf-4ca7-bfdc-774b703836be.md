> DEVELOPER

how to delete old zelliz sessions?

> AGENT

To delete Zellij sessions:

**List sessions:**
```sh
zellij list-sessions
```

**Delete a specific session:**
```sh
zellij delete-session <session-name>
```

**Delete all sessions:**
```sh
zellij delete-all-sessions
```

**Kill (force) a running session first if needed:**
```sh
zellij kill-session <session-name>
# or kill all
zellij kill-all-sessions
```

Dead/exited sessions accumulate in `~/.cache/zellij/` — `delete-all-sessions` clears those.
