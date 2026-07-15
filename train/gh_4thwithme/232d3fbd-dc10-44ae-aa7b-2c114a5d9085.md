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
