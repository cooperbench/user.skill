> DEVELOPER

my ghosty has limited history length how to expand it?

> AGENT

In Ghostty, add this to your config file (`~/.config/ghostty/config`):

```
scrollback-limit = 100000
```

Default is 10,000 lines. Set to `0` for unlimited (uses more memory).
