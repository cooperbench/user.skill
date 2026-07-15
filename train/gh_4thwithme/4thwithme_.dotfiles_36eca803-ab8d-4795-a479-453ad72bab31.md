---
session_id: "4thwithme/.dotfiles|36eca803-ab8d-4795-a479-453ad72bab31"
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme/.dotfiles
start_time: "2026-03-22T14:23:09.330Z"
n_turns: 2
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

how to clean history in terminal in tmux? like cntrl+k

> AGENT

In tmux, `Ctrl+K` from your terminal emulator won't clear the scrollback buffer. Here are the options:

**Clear screen only (like `clear`):**
```
Ctrl+L
```

**Clear screen + scrollback buffer:**
```bash
clear && tmux clear-history
```
Or bind it:
```bash
# In ~/.tmux.conf
bind -n C-k send-keys "clear && tmux clear-history" Enter
```

**Just clear tmux scrollback (from command line):**
```bash
tmux clear-history
```

**From tmux command mode:**
```
Prefix + :  →  clear-history
```

The key distinction: `Ctrl+L` only clears the visible screen. `tmux clear-history` wipes the scrollback buffer too.
