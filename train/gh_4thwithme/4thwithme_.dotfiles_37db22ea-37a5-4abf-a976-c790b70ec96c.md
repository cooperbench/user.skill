> DEVELOPER

do we have context7 here as plugin skill? on PC for user, or in the repo?

> AGENT

Context7 is **available in the marketplace** (`external_plugins/context7`) but **not installed**. It's not in your installed plugins.

To install it, run `/plugins` in Claude Code and search for "context7", or install it via the CLI.

> DEVELOPER

ok i have installed this in the repo< can you copy it to the my user in the pc here?

> AGENT

Two changes needed: add context7 to `enabledPlugins` in user `settings.json`, and add a user-scope entry in `installed_plugins.json`.

> AGENT

Now add the user-scope entry to `installed_plugins.json`:

> AGENT

Done. Run `/reload-plugins` to apply. Context7 is now user-scoped — active across all projects.

> DEVELOPER

i question.. ia have installed plugins, skills, output style for my user oon pc... but i have multiple PCs, how to share it within them?

> AGENT

No native sync — Claude Code doesn't have a cloud sync feature yet.

**Best approach: dotfiles git repo**

Key files to sync:
```
~/.claude/settings.json          # output style, hooks, enabledPlugins
~/.claude/plugins/installed_plugins.json  # plugin registry
~/.claude/skills/                # custom skills
~/.claude/keybindings.json       # keybindings
```

**What NOT to sync:**
- `~/.claude/plugins/cache/` — re-downloaded automatically on each machine
- `~/.claude/sessions/`, `~/.claude/history.jsonl` — machine-local
- `~/.claude/projects/` — memory is machine-local (or sync separately if you want)

**Setup:**
1. Create a private GitHub repo (e.g. `dotfiles`)
2. Copy those files in, commit + push
3. On each new PC: clone repo, symlink or copy files to `~/.claude/`

**Caveat on `installed_plugins.json`:** The `installPath` entries point to `~/.claude/plugins/cache/` which is the same path on all machines (assuming same username). After copying the file, run `/reload-plugins` — Claude Code will re-download any missing cache entries automatically.

Want me to set up the dotfiles structure for you?

> DEVELOPER

but .claude lives not in the .config/ this is the place where all my dotfiles lives

> AGENT

Simplest fix: symlink `~/.claude` → `~/.config/claude`.

```bash
# Move it into your dotfiles location
mv ~/.claude ~/.config/claude

# Symlink back so Claude Code finds it
ln -s ~/.config/claude ~/.claude
```

Then in your dotfiles repo, track `~/.config/claude/` normally. On each new PC:
```bash
# After cloning dotfiles to ~/.config/
ln -s ~/.config/claude ~/.claude
```

Claude Code always looks at `~/.claude` — the symlink satisfies that, while the actual files live where your dotfiles manager expects them.

> DEVELOPER

go for it

> AGENT

Done.

```
~/.claude  →  /Users/4thwithme/.config/claude
```

Now just track `~/.config/claude/` in your dotfiles repo. On each new PC after cloning:
```bash
ln -s ~/.config/claude ~/.claude
```

> DEVELOPER

so if i want to change smth.. i need to change it where? where si cosurce of truth?

> AGENT

`~/.config/claude/` — that's the source of truth now.

`~/.claude` is just a pointer to it. Any changes via Claude Code UI, `/plugin`, settings, etc. all write to `~/.config/claude/` automatically through the symlink.
