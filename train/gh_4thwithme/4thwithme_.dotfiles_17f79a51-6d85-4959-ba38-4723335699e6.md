---
session_id: "4thwithme/.dotfiles|17f79a51-6d85-4959-ba38-4723335699e6"
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme/.dotfiles
start_time: "2026-04-06T16:37:21.075Z"
n_turns: 2
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

my ghosty has limited history length how to expand it?

> AGENT

In Ghostty, add this to your config file (`~/.config/ghostty/config`):

```
scrollback-limit = 100000
```

Default is 10,000 lines. Set to `0` for unlimited (uses more memory).
