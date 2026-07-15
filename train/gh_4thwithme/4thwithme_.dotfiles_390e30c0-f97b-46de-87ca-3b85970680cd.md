> DEVELOPER

how t oattach to the tmux session?

> AGENT

```bash
tmux attach
```

Or if there are multiple sessions:

```bash
tmux ls                    # list sessions
tmux attach -t <session>   # attach to specific one
```
