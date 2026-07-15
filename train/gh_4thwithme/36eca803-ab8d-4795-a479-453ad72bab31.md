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
