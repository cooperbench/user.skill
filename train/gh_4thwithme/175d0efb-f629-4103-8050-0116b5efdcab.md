> DEVELOPER

compinit:527: no such file or directory: /opt/homebrew/share/zsh/site-functions/_alacritty

> AGENT

Fix: remove or recreate the stale completion symlink.

```bash
rm /opt/homebrew/share/zsh/site-functions/_alacritty
```

Then restart your shell. If you still use Alacritty and want completions back:

```bash
brew reinstall alacritty
```

> TOOL

<bash-input>rm /opt/homebrew/share/zsh/site-functions/_alacritty</bash-input>

> TOOL

<bash-stdout>(Bash completed with no output)</bash-stdout><bash-stderr></bash-stderr>
