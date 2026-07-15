---
session_id: 7ff0be99-eecf-4ca7-bfdc-774b703836be
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme
start_time: "2026-03-22T13:38:43.825Z"
n_turns: 2
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

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
