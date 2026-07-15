---
session_id: "4thwithme/.dotfiles|232d3fbd-dc10-44ae-aa7b-2c114a5d9085"
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme/.dotfiles
start_time: "2026-03-22T13:43:50.038Z"
n_turns: 2
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

how to attach to the seesion in zellij? only names, or i can use index?

> AGENT

Both. You can attach by name or by index:

```sh
zellij attach <session-name>
zellij attach --index <n>   # 0-based index
```

To list sessions with their indices:
```sh
zellij list-sessions
```
